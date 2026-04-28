from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


@dataclass
class Marker:
    """본문의 `${...}` 마커 하나를 나타내는 dataclass.

    - raw_token: 원본 마커 문자열 (예: `${1}`, `${hello.png}`). post_loader 가 생성, post_builder 가 소비.
    - kind: "index" (1-based 정수) 또는 "filename" (파일명). post_loader 가 결정.
    - value: index 일 때 양의 정수, filename 일 때 파일명 문자열. post_loader 가 설정.
    - position: 본문(body_markdown) 내 마커의 시작 offset. post_loader 가 `body_markdown.find` 로 계산.
    """

    raw_token: str
    kind: Literal["index", "filename"]
    value: int | str
    position: int


@dataclass
class LoadedPost:
    """폴더 기반 글 하나의 파싱 결과. post_loader 가 생성, post_runner / post_builder 가 소비.

    - title: frontmatter title (필수, 없으면 loader 가 ValueError).
    - category_name: frontmatter category (선택). None 이면 post_builder 에서 categoryId=0.
    - tags: frontmatter tags 리스트. 빈 리스트 허용.
    - body_markdown: frontmatter 이후 본문 markdown 원문. 비어있으면 loader 가 ValueError (dataclass 자체는 단순 저장소).
    - markers: 본문에서 추출된 `${...}` 마커 목록 (등장 순서 보존).
    - images: 폴더 내 이미지 파일명 → 절대경로 매핑. post_loader 가 사전순 수집.
    - folder: 글 폴더 절대경로. post_runner 가 `.published`/`.draft_id`/`.orphan.log`/`.error` 기록에 사용.
    - skip: `.published` 파일이 존재하면 True. post_runner 가 즉시 skip 판정.
    """

    title: str
    category_name: str | None
    tags: list[str]
    body_markdown: str
    markers: list[Marker]
    images: dict[str, Path]
    folder: Path
    skip: bool = False


@dataclass
class UploadedImage:
    """tistory attach.json 응답 1건을 표현. image_uploader 가 생성, post_builder 가 소비.

    - key: tistory CDN key (예: `CL9bz/dJMcahc5bwS/.../img.png`). thumbnail 값으로도 재사용.
    - url: 응답 url 원본 (escape 안 된 상태). 디버깅/로그 용도.
    - filename: 업로드 당시 원본 파일명 (매크로 filename 필드에 삽입).
    - size: 응답 size (bytes).
    - width: 실제 이미지 픽셀 너비 (Pillow 로 로컬 측정).
    - height: 실제 이미지 픽셀 높이 (Pillow 로 로컬 측정).
    - macro: `&amp;` escape 완료 상태의 최종 tistory 매크로 문자열.
      post_builder 는 이 값을 그대로 본문에 치환 (재escape 금지).
    """

    key: str
    url: str
    filename: str
    size: int
    width: int
    height: int
    macro: str


@dataclass
class DraftPayload:
    """POST /manage/drafts 요청 body. post_builder 가 생성, post_saver 가 JSON 직렬화.

    probe-tistory-api.md §2 명명 규약을 엄격히 준수한다 (필드명은 `content`, 다른 변형 금지).

    - title: draft 제목.
    - content: HTML 본문 (tistory 매크로 포함 가능, `&` → `&amp;` escape 완료 상태).
    - tags: 쉼표 구분 문자열 (예: `"자동화,테스트"`).
    - categoryId: 카테고리 ID. 0=카테고리 없음.
    - thumbnail: 대표 이미지 key (선택). 보통 uploads[0].key 또는 None.
    - draftSequence: 기존 draft sequence id. 있으면 업데이트, None 이면 새 draft 생성.
    """

    title: str
    content: str
    tags: str
    categoryId: int
    thumbnail: str | None
    draftSequence: int | None


@dataclass
class RunResult:
    """post_runner.run_post 1회 실행 결과. post_runner 가 생성, 스모크 러너 / 상위 스크립트가 소비.

    - skipped: `.published` 마커로 인해 skip 된 경우 True.
    - draft_sequence: save_draft 성공 시 sequence id. skip/실패 시 None.
    - orphan_images: 부분 업로드 실패 시 이미 올라간 이미지 목록 (사용자 수동 정리 대상).
    - error: 실패 시 간단한 에러 문자열. 성공 시 None.
    """

    skipped: bool
    draft_sequence: int | None
    orphan_images: list[UploadedImage] = field(default_factory=list)
    error: str | None = None


class PartialUploadError(Exception):
    """이미지 업로드 k-th 실패 시 image_uploader 가 raise 하는 예외.

    post_runner 가 catch 해 `.orphan.log` 에 업로드된 이미지를 기록하고 사용자에게 수동 정리를 위임한다.

    - uploaded: 실패 직전까지 성공한 UploadedImage 목록.
    - failed_index: 실패한 이미지의 0-based index.
    - cause: 실패의 원인 예외 (HTTP 4xx/5xx, network 등).
    """

    def __init__(
        self,
        uploaded: list[UploadedImage],
        failed_index: int,
        cause: Exception,
    ) -> None:
        self.uploaded = uploaded
        self.failed_index = failed_index
        self.cause = cause
        super().__init__(
            f"이미지 업로드 부분 실패: {len(uploaded)}/{failed_index + 1} 성공, " f"원인: {cause}"
        )
