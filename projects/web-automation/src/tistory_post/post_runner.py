"""폴더 기반 임시저장 end-to-end 실행기.

한 폴더(`posts/{YYYY-MM-DD}-{slug}/`)를 받아 post_loader → category_fetcher →
image_uploader → post_builder → post_saver 를 순서대로 실행하고
`.draft_id` / `.published` / `.error` / `.orphan.log` 마커 파일을 관리한다.

에러 롤백 계약 (architecture.md §7, reviewer-report-TASK-025 M7):
    - upload 단계 PartialUploadError → `.orphan.log` 에 JSONL append + `.error` 덮어쓰기
    - build/save 실패 → `.error` 덮어쓰기 (이 시점 업로드 완료분도 orphan 처리)
    - 성공 시 기존 `.error` / `.orphan.log` 삭제 (이전 실패 흔적 제거)
    - retry 없음 — 사용자가 재실행으로 위임 (MVP)
"""

from __future__ import annotations

import json
import logging
import traceback
from datetime import datetime, timezone
from pathlib import Path

from src.tistory_post.category_fetcher import fetch_category_map
from src.tistory_post.image_uploader import upload_images
from src.tistory_post.models import (
    LoadedPost,
    PartialUploadError,
    RunResult,
    UploadedImage,
)
from src.tistory_post.post_builder import build_payload
from src.tistory_post.post_loader import load_post
from src.tistory_post.post_saver import save_draft

logger = logging.getLogger("tistory_post.post_runner")


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _append_orphan_log(folder: Path, images: list[UploadedImage]) -> None:
    """업로드됐으나 draft 에 연결 안 된 이미지들을 JSONL 로 append 한다."""
    path = folder / ".orphan.log"
    ts = _now_iso()
    with path.open("a", encoding="utf-8") as fp:
        for img in images:
            rec = {
                "ts": ts,
                "key": img.key,
                "url": img.url,
                "filename": img.filename,
                "size": img.size,
            }
            fp.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _write_error(folder: Path, phase: str, exc: BaseException) -> None:
    """최근 실패 traceback + phase 를 JSON 1 파일로 덮어쓴다."""
    path = folder / ".error"
    rec = {
        "ts": _now_iso(),
        "phase": phase,
        "exception": type(exc).__name__,
        "message": str(exc),
        "traceback": "".join(
            traceback.format_exception(type(exc), exc, exc.__traceback__)
        ),
    }
    path.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")


def _clear_failure_markers(folder: Path) -> None:
    """성공 재실행 시 이전 실패 흔적을 제거한다."""
    for name in (".error", ".orphan.log"):
        p = folder / name
        if p.exists():
            p.unlink()
            logger.info("성공 재실행으로 %s 삭제", name)


def _read_draft_id(folder: Path) -> int | None:
    path = folder / ".draft_id"
    if not path.exists():
        return None
    try:
        return int(path.read_text(encoding="utf-8").strip())
    except ValueError:
        logger.warning(".draft_id 내용이 정수 아님 — 무시하고 새 draft 생성")
        return None


def _write_draft_id(folder: Path, sequence: int) -> None:
    (folder / ".draft_id").write_text(str(sequence), encoding="utf-8")


def _write_published(folder: Path) -> None:
    (folder / ".published").write_text(_now_iso(), encoding="utf-8")


async def run_post(page, folder: Path, blog_name: str) -> RunResult:
    """폴더 1개를 처리해 임시저장 완료까지 진행한다.

    Args:
        page: 로그인된 Playwright Page (BrowserManager.get_page()).
        folder: 대상 폴더 경로 (`posts/{YYYY-MM-DD}-{slug}/`).

    Returns:
        RunResult — skip/성공/실패 결과.

    Raises:
        `PartialUploadError` 또는 `RuntimeError` 또는 기타 예외.
        예외를 던지기 전 `.orphan.log`/`.error` 마커 파일을 남긴다.
    """
    folder = Path(folder).resolve()
    logger.info("run_post 시작: %s", folder)

    # 1. post_loader — skip 즉시 반환
    loaded: LoadedPost = load_post(folder)
    if loaded.skip:
        logger.info(".published 존재 — skip")
        return RunResult(
            skipped=True, draft_sequence=None, orphan_images=[], error=None
        )

    phase = "load"
    uploaded: list[UploadedImage] = []

    try:
        # 2. 카테고리 맵 조회
        phase = "category"
        category_map = await fetch_category_map(page, blog_name)
        logger.info("카테고리 맵 %d개", len(category_map))

        # 3. 이미지 업로드 (post_loader 가 images dict 구성 순서 — filename 사전순 아님.
        #    post_builder 의 Marker.index 해석은 sorted(images.keys()) 기준이므로
        #    uploader 에 넘기는 Path 리스트 순서는 의미 없음 — macro_by_filename 로 lookup.)
        phase = "upload"
        image_paths = list(loaded.images.values())
        uploaded = await upload_images(page, image_paths)
        logger.info("업로드 완료 %d개", len(uploaded))

        # 4. payload 조립
        phase = "build"
        payload = build_payload(loaded, uploaded, category_map)

        # 5. 기존 draft 있으면 이어서 덮어쓰기
        payload.draftSequence = _read_draft_id(folder)

        # 6. drafts API 저장
        phase = "save"
        sequence = await save_draft(page, payload)

        # 7. 마커 파일 기록
        _write_draft_id(folder, sequence)
        _write_published(folder)
        _clear_failure_markers(folder)

        logger.info("run_post 성공 (sequence=%d)", sequence)
        return RunResult(
            skipped=False,
            draft_sequence=sequence,
            orphan_images=[],
            error=None,
        )

    except PartialUploadError as exc:
        # uploader 가 k-1 개 성공 후 k 번째 실패 — 이미 업로드된 이미지는 orphan
        _append_orphan_log(folder, exc.uploaded)
        _write_error(folder, "upload", exc)
        logger.error(
            "upload 부분 실패 (orphan=%d, failed_index=%d)",
            len(exc.uploaded),
            exc.failed_index,
        )
        raise

    except Exception as exc:
        # build/save 등 upload 이후 단계 실패 — upload 한 이미지 전체가 orphan
        if uploaded:
            _append_orphan_log(folder, uploaded)
        _write_error(folder, phase, exc)
        logger.error("%s 단계 실패: %s", phase, exc)
        raise


__all__ = ["run_post"]
