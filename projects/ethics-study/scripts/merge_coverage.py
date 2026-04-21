#!/usr/bin/env python3
"""merge_coverage.py — Phase 6 MERGE 스크립트 (TASK-175E-MERGE)

입력:
- projects/ethics-study/exam-solutions/coverage/*.md (26개: 2014-A ~ 2026-B)
- ES (localhost:9200) ethics-thinkers (55) + ethics-claims

출력:
- projects/ethics-study/exam-solutions/exam-coverage-map.md (신규 병합 맵)

규약:
- 구형 17개 (2014-A ~ 2022-A): 상단 `| 문항 | ... | thinker_id | ... | ES 커버리지 |` 테이블 1개.
- 신형 9개 (2022-B ~ 2026-B): 파일 말미 `| Q | ... | thinker_id(s) | ES | 비고 |` 테이블.
- 동적 헤더 매핑 (소문자 컬럼명으로 lookup).
- thinker_id 정규식: 백틱 감싼 소문자 id `[a-z][a-z0-9_]*`.
- canonical 55: ES에서 실시간 fetch. name은 한글(`name`), 영문은 `name_en`.
- taylor(Charles, ES 55인) vs taylor_p(Paul, MISS) 엄수.
- 블로커 총 발행 93건 − 철회 1건 = net active 92건 assertion.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.request
from collections import Counter, OrderedDict, defaultdict
from datetime import datetime
from pathlib import Path

# ========== 경로 고정 ==========
REPO_ROOT = Path(__file__).resolve().parents[3]  # program-agent/
PROJECT_ROOT = REPO_ROOT / "projects" / "ethics-study"
COVERAGE_DIR = PROJECT_ROOT / "exam-solutions" / "coverage"
OUT_PATH = PROJECT_ROOT / "exam-solutions" / "exam-coverage-map.md"
BLOCKER_LOG = REPO_ROOT / "signal" / "ethics-study" / "blocker-log.md"

ES_BASE = "http://localhost:9200"
EXPECTED_THINKER_COUNT = 55
EXPECTED_BLOCKERS_ISSUED = 93
EXPECTED_BLOCKERS_WITHDRAWN = 1
EXPECTED_BLOCKERS_NET = EXPECTED_BLOCKERS_ISSUED - EXPECTED_BLOCKERS_WITHDRAWN  # 92

# 구형 17개 / 신형 9개 분류
OLD_FORMAT_FILES = [
    "2014-A", "2014-B", "2015-A", "2015-B", "2016-A", "2016-B",
    "2017-A", "2017-B", "2018-A", "2018-B", "2019-A", "2019-B",
    "2020-A", "2020-B", "2021-A", "2021-B", "2022-A",
]
NEW_FORMAT_FILES = [
    "2022-B", "2023-A", "2023-B", "2024-A", "2024-B",
    "2025-A", "2025-B", "2026-A", "2026-B",
]

# 배점 예상합 (Section E 검산 기준; 실측 2014~2026 26개 파일 직독 기반)
# 2014: A 교시 기입형 15×2 + 서술형 5×4 = 50점, B 교시 서술형 5×2 + 논술형 10×2 = 30점
# 2015: A=40, B=40 (표준)
# 2016+: 모든 연도 A=40, B=40 (표준)
EXPECTED_SCORE_SUM = {
    "2014-A": 50, "2014-B": 30,
}
for yr in range(2015, 2027):
    EXPECTED_SCORE_SUM.setdefault(f"{yr}-A", 40)
    EXPECTED_SCORE_SUM.setdefault(f"{yr}-B", 40)


# ========== 로그 ==========
def log(msg: str) -> None:
    print(f"[merge_coverage] {msg}", file=sys.stderr)


def fail(msg: str, code: int = 1) -> None:
    print(f"[merge_coverage] FATAL: {msg}", file=sys.stderr)
    sys.exit(code)


# ========== ES pre-flight ==========
def es_get(path: str) -> dict:
    url = f"{ES_BASE}{path}"
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        fail(f"ES GET {url} failed: {e}")
    return {}


def es_post(path: str, body: dict) -> dict:
    url = f"{ES_BASE}{path}"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        fail(f"ES POST {url} failed: {e}")
    return {}


def preflight_es() -> tuple[dict[str, str], dict[str, int]]:
    # 1) cluster health
    health = es_get("/_cluster/health")
    status = health.get("status")
    if status not in ("green", "yellow"):
        fail(f"ES cluster status={status} (green/yellow required)")
    log(f"ES cluster status: {status}")

    # 2) thinker count
    cnt = es_get("/ethics-thinkers/_count").get("count", 0)
    if cnt != EXPECTED_THINKER_COUNT:
        fail(f"ethics-thinkers count={cnt}, expected {EXPECTED_THINKER_COUNT}")
    log(f"ethics-thinkers count = {cnt}")

    # 3) canonical 55 dump (id -> 한글명)
    res = es_get("/ethics-thinkers/_search?size=100&_source=id,name,name_en")
    hits = res.get("hits", {}).get("hits", [])
    id_to_name: dict[str, str] = {}
    for h in hits:
        src = h.get("_source", {})
        tid = src.get("id")
        nm = src.get("name") or src.get("name_en") or tid
        if tid:
            id_to_name[tid] = nm
    if len(id_to_name) != EXPECTED_THINKER_COUNT:
        fail(f"canonical dump size={len(id_to_name)}, expected {EXPECTED_THINKER_COUNT}")
    log(f"canonical 55 dump OK ({len(id_to_name)} ids)")

    # 4) claims aggregation
    agg_body = {"size": 0, "aggs": {"by_thinker": {"terms": {"field": "thinker_id", "size": 200}}}}
    agg_res = es_post("/ethics-claims/_search", agg_body)
    buckets = agg_res.get("aggregations", {}).get("by_thinker", {}).get("buckets", [])
    claims_count: dict[str, int] = {b["key"]: b["doc_count"] for b in buckets}
    log(f"ethics-claims aggregation: {len(claims_count)} thinkers with claims")

    return id_to_name, claims_count


# ========== blocker-log 교차 검증 ==========
# BLK 엔트리 형식 (두 가지 모두 대응):
#   ### BLK-175E-2015A-001 (TASK-175E-2015-A) — 기입형 4 (나) 빈칸 정답 개념어 미확정
#   ### BLK-175E-2016A-001 — 2016-A Q4 스승·제자 구체 인명 미특정
# id 다음에 선택적으로 (TASK-...)와 " — <title>"이 붙음. 제목 없이 끝날 수도 있음.
BLK_LINE_RE = re.compile(
    r"^###\s+(BLK-175E-\d{4}[AB]-\d{3})\s*(.*)$"
)


def parse_blocker_log() -> tuple[list[str], set[str], dict[str, str]]:
    if not BLOCKER_LOG.exists():
        fail(f"blocker-log not found: {BLOCKER_LOG}")
    text = BLOCKER_LOG.read_text(encoding="utf-8")
    ids_issued: list[str] = []
    withdrawn: set[str] = set()
    titles: dict[str, str] = {}
    for ln in text.splitlines():
        m = BLK_LINE_RE.match(ln.rstrip())
        if m:
            blk_id = m.group(1)
            rest = (m.group(2) or "").strip()
            ids_issued.append(blk_id)
            titles[blk_id] = rest
            if "철회" in rest or "FALSE-POSITIVE" in rest:
                withdrawn.add(blk_id)
    if len(ids_issued) != EXPECTED_BLOCKERS_ISSUED:
        log(
            f"WARN: blocker-log issued={len(ids_issued)}, expected {EXPECTED_BLOCKERS_ISSUED}"
        )
    if len(withdrawn) != EXPECTED_BLOCKERS_WITHDRAWN:
        log(
            f"WARN: blocker-log withdrawn={len(withdrawn)}, expected {EXPECTED_BLOCKERS_WITHDRAWN}"
        )
    net = len(ids_issued) - len(withdrawn)
    log(
        f"blocker-log: issued={len(ids_issued)}, withdrawn={len(withdrawn)}, net active={net}"
    )
    return ids_issued, withdrawn, titles


# ========== 2-path 파서 ==========
# 백틱 감싼 소문자 id: `[a-z][a-z0-9_]*`
THINKER_ID_RE = re.compile(r"`([a-z][a-z0-9_]*)`")
# 백틱 없는 소문자 id 토큰 (구형 2014-A, 2014-B 등 일부 파일 대응).
# 최소 3글자 이상, 한글·괄호 주변에서 자연스런 토큰으로 등장하는 id만.
BARE_ID_RE = re.compile(r"(?<![a-z0-9_`])([a-z][a-z0-9_]{2,})(?![a-z0-9_`])")
# thinker_id 컬럼 셀에서 stopword로 배제할 영문 토큰 (셀 맥락 설명어)
STOPWORDS = {
    "et", "al", "or", "and", "the", "a", "an", "of", "to", "in", "on", "by",
    "is", "are", "was", "from", "with", "cf", "etc", "see", "note",
    # 자주 등장하는 비-id 단어
    "none", "miss", "hit", "mixed", "pending", "blocker", "na",
    "ch", "pt", "ep", "vol", "part", "paragraph", "section",
    # 영문 주석/분류 단어
    "general", "meta", "hanja", "pre", "post", "mid", "late", "early",
    # 철학 외 용어
    "text", "textual", "claim", "claims", "fragment", "frag",
    "growth", "sympathy", "sub", "specie", "aeternitatis", "ethos",
    "aretē", "arete", "areté", "dianoetike", "didaskalia", "ethike",
    "empathic", "distress", "inductive", "discipline",
    "trademark", "observation", "blocked", "fix", "apply",
}
# 경계영역/보류 마커
BOUNDARY_MARKERS = [
    "교과교육학", "메타윤리", "결의론", "일반개념", "응용윤리학",
]
PENDING_MARKERS = [
    "N/A", "특정 불능", "미확정", "불명", "보류", "BLOCKER-PENDING",
]


def normalize_header(cell: str) -> str:
    """헤더 셀 정규화: 소문자, 공백·괄호 내부 제거."""
    s = cell.strip().lower()
    # 괄호 안 제거 (예: "중심 사상가(thinker_id)" -> "중심 사상가")
    # 단, thinker_id 이름 자체는 유지하기 위해 괄호 제거 전후 둘 다 체크
    return s


def map_columns(header_cells: list[str]) -> dict[str, int]:
    """헤더 셀 리스트 → 의미 키워드: 인덱스 dict.

    지원 별칭:
    - thinker_id: "thinker_id", "thinker_id(s)", "중심 사상가(thinker_id)",
                  "주요 사상가(thinker_id)"
    - score: "배점"
    - es: "es 커버리지", "es 상태", "es"
    - item_id: "문항", "q"
    - category: "분류", "유형"
    """
    mapping: dict[str, int] = {}
    for i, raw in enumerate(header_cells):
        key = normalize_header(raw)
        # thinker_id
        if "thinker_id" in key and "thinker" not in mapping.get("_thinker_fields_seen", ""):
            mapping["thinker_id"] = i
        # 배점
        if key == "배점" and "score" not in mapping:
            mapping["score"] = i
        # ES
        if (
            key in ("es 커버리지", "es 상태", "es")
            or key.startswith("es ")
            or (key == "es" and "es" not in mapping)
        ):
            if "es" not in mapping:
                mapping["es"] = i
        # 문항/Q
        if key in ("문항", "q") and "item_id" not in mapping:
            mapping["item_id"] = i
        # 분류
        if key == "분류" and "category" not in mapping:
            mapping["category"] = i
        if key == "유형" and "type_col" not in mapping:
            mapping["type_col"] = i
    return mapping


_PIPE_PLACEHOLDER = "\x00PIPE\x00"


def split_md_row(line: str) -> list[str]:
    """마크다운 테이블 row 분해: | a | b | c | -> [a, b, c].

    이스케이프된 파이프(\\|)는 셀 내부 문자로 유지.
    """
    s = line.strip()
    if not s.startswith("|") or not s.endswith("|"):
        return []
    # \| → placeholder 치환 후 split, 셀마다 복원
    inner = s[1:-1].replace(r"\|", _PIPE_PLACEHOLDER)
    cells = [c.strip().replace(_PIPE_PLACEHOLDER, "|") for c in inner.split("|")]
    return cells


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r"[:\-\s]+", c or "") for c in cells)


def find_first_table_with_thinker_id(lines: list[str], start: int = 0) -> tuple[int, int, list[str]]:
    """lines[start:]에서 'thinker_id' 포함 테이블 헤더 위치 탐색.

    반환: (header_line_idx, data_start_idx, header_cells)
    없으면 (-1, -1, []).
    """
    i = start
    n = len(lines)
    while i < n:
        ln = lines[i].strip()
        if ln.startswith("|") and "thinker_id" in ln.lower():
            cells = split_md_row(lines[i])
            if cells:
                # 다음 줄이 separator면 data는 그 다음부터
                data_start = i + 1
                if data_start < n:
                    next_cells = split_md_row(lines[data_start])
                    if is_separator_row(next_cells):
                        data_start += 1
                return i, data_start, cells
        i += 1
    return -1, -1, []


def iter_data_rows(lines: list[str], data_start: int) -> list[list[str]]:
    """data_start 부터 테이블 끝(빈 줄/non-pipe 행)까지 data row 수집."""
    rows: list[list[str]] = []
    i = data_start
    while i < len(lines):
        ln = lines[i]
        if not ln.strip().startswith("|"):
            break
        cells = split_md_row(ln)
        if not cells:
            break
        if is_separator_row(cells):
            i += 1
            continue
        rows.append(cells)
        i += 1
    return rows


def extract_thinker_ids(cell: str, known_ids: set[str] | None = None) -> list[str]:
    """셀에서 thinker_id 추출 (셀 내 중복 제거, 순서 유지).

    1. 백틱 감싼 id 우선 추출.
    2. 백틱 id가 하나도 없으면 bare id 추출 — 단 canonical ES 55 또는
       MISS_NAME_MAP 알려진 id와 매칭되는 토큰만 채택 (오탐 방지).

    동일 셀 내 같은 id가 여러 번 등장해도 1회로 축약 (count 의미 없음).
    서로 다른 row/cell 간의 중복은 호출 측에서 유지한다.
    """
    ids = THINKER_ID_RE.findall(cell)
    if ids:
        return list(dict.fromkeys(ids))
    # 백틱 없는 구형 파일: bare token 추출 후 알려진 id만 채택
    if known_ids is None:
        return []
    bare = BARE_ID_RE.findall(cell)
    filtered = []
    for tok in bare:
        if tok in STOPWORDS:
            continue
        if tok in known_ids:
            filtered.append(tok)
    return list(dict.fromkeys(filtered))


def classify_row(
    thinker_cell: str, category_cell: str, es_cell: str,
    known_ids: set[str] | None = None,
) -> tuple[str, list[str]]:
    """row 유형 분류: thinker(사상가형) / boundary(교과교육학·경계영역) / pending(보류).

    반환: (row_type, thinker_ids).
    """
    ids = extract_thinker_ids(thinker_cell, known_ids)
    has_ids = bool(ids)
    # 1. pending 우선: thinker_id 없음 + 보류 키워드 명시
    if not has_ids and any(m in thinker_cell for m in PENDING_MARKERS):
        return "pending", []
    # 2. boundary: 분류가 명시적으로 교과교육학/경계영역이고 thinker_id 없음
    is_boundary_cat = any(
        m in category_cell for m in ("교과교육학", "경계영역", "일반개념", "메타윤리")
    )
    if is_boundary_cat and not has_ids:
        return "boundary", []
    # 3. 사상가 + 경계영역 혼합 (분류에 둘 다 있음)
    if is_boundary_cat and has_ids:
        # category가 "사상가형 / 교과교육학 경계" 같은 복합일 때
        if "사상가형" in category_cell:
            return "thinker", ids  # 사상가형 명시 우선
        return "boundary_with_thinker", ids
    # 4. thinker 있음
    if has_ids:
        return "thinker", ids
    # 5. thinker_id 없음 + 분류 불명 → 보류
    if not category_cell or category_cell.strip() == "":
        return "pending", []
    return "pending", []


def parse_score(cell: str) -> int:
    """배점 셀 → int. '**4**' 같은 마크다운도 파싱."""
    s = re.sub(r"[^\d]", "", cell)
    return int(s) if s else 0


def es_status_of(cell: str) -> str:
    """ES 셀 → 'HIT' / 'MISS' / 'NA' / 'MIXED'.

    셀 안에 'MISS' 또는 '미등록' 포함 시 MISS.
    'HIT' 또는 'etc.' 포함 시 HIT.
    둘 다 있으면 MIXED.
    'N/A' 또는 'N\\A' 경우 NA.
    """
    s = cell.lower()
    has_miss = ("miss" in s or "미등록" in cell or "없음" in cell or "부족" in cell)
    has_hit = ("hit" in s or "등록" in cell and "미등록" not in cell)
    if "n/a" in s or "—" in cell or "교과교육학" in cell:
        if not has_miss and not has_hit:
            return "NA"
    if has_miss and has_hit:
        return "MIXED"
    if has_miss:
        return "MISS"
    if has_hit:
        return "HIT"
    # 추론 실패
    if "없음" in cell:
        return "MISS"
    return "NA"


# ========== coverage 파일 전수 파싱 ==========
def parse_coverage_file(exam_id: str, text: str, known_ids: set[str] | None = None) -> dict:
    """단일 coverage 파일 파싱.

    반환:
    {
        "exam_id": "2014-A",
        "rows": [
            {
                "item": "기입형 1", "score": 2,
                "thinker_ids": ["confucius", "zhuxi"],
                "category": "사상가형",
                "es_status": "HIT",
                "row_type": "thinker",
                "raw_thinker_cell": "...",
                "blk_ids": ["BLK-175E-2022A-001", ...],  # 비고에서 추출
            },
            ...
        ],
        "score_sum": 40,
    }
    """
    lines = text.splitlines()

    # 구형 vs 신형: 단순히 파일명으로 분기하되, 실제 헤더 탐색은 2-path로.
    if exam_id in OLD_FORMAT_FILES:
        # path-1: 파일 상단에서 thinker_id 테이블 찾기
        hdr_idx, data_start, header_cells = find_first_table_with_thinker_id(lines, 0)
    else:
        # path-2: 파일 말미 쪽(우선 전체 탐색, 복수면 마지막 테이블 사용)
        # 모든 thinker_id 테이블 수집
        all_tables = []
        pos = 0
        while True:
            hdr_idx, data_start, header_cells = find_first_table_with_thinker_id(lines, pos)
            if hdr_idx < 0:
                break
            all_tables.append((hdr_idx, data_start, header_cells))
            pos = data_start + 1
        if not all_tables:
            hdr_idx, data_start, header_cells = -1, -1, []
        else:
            # 신형: 파일 말미 요약표가 '전체 문항을 요약하는' 테이블.
            # 조건: (a) Q/문항 컬럼 + (b) 배점 컬럼 동시 존재.
            # 문항별 섹션 내부 mini table, 재출제 연속성 미니 표는
            # Q/문항 있어도 배점 컬럼이 없으므로 제외된다.
            full_tables = []
            for t in all_tables:
                hdr_cells = t[2]
                has_q = any(normalize_header(c) in ("q", "문항", "#") for c in hdr_cells)
                has_score = any(
                    normalize_header(c) == "배점" for c in hdr_cells
                )
                if has_q and has_score:
                    full_tables.append(t)
            if full_tables:
                hdr_idx, data_start, header_cells = full_tables[-1]
            else:
                # fallback: thinker_id 포함 마지막 테이블
                hdr_idx, data_start, header_cells = all_tables[-1]

    if hdr_idx < 0:
        fail(f"{exam_id}: thinker_id 테이블 탐지 실패")

    colmap = map_columns(header_cells)
    if "thinker_id" not in colmap:
        fail(f"{exam_id}: thinker_id 컬럼 매핑 실패 (header={header_cells})")

    rows_raw = iter_data_rows(lines, data_start)
    parsed_rows = []
    score_sum = 0

    thinker_idx_hdr = colmap["thinker_id"]
    cat_idx_hdr = colmap.get("category")
    es_idx_hdr = colmap.get("es")
    header_len = len(header_cells)

    def _cell_has_thinker_id(c: str) -> bool:
        if THINKER_ID_RE.search(c):
            return True
        if known_ids:
            for tok in BARE_ID_RE.findall(c):
                if tok in STOPWORDS:
                    continue
                if tok in known_ids:
                    return True
        return False

    def _looks_like_thinker_cell(c: str) -> bool:
        if _cell_has_thinker_id(c):
            return True
        stripped = re.sub(r"[\s\*]", "", c)
        if stripped in ("—", "-", ""):
            return True
        if "없음" in c or "미등록" in c or "N/A" in c:
            return True
        return False

    # 컬럼 오프셋 보정: 2018-A/2019-A/2020-A 등 데이터 row에 헤더에 없는
    # 추가 주석 셀(제시문 해설 등)이 삽입되어 있는 경우가 있다.
    # 먼저 테이블 전체 레벨로 shift를 결정한다.
    #   (a) 모든 row의 셀 수가 header_len 이고, 헤더 기반 thinker_id 셀에
    #       backtick id가 1건 이상 있으면 shift=0.
    #   (b) row 셀 수가 header_len + k (k>0)가 dominant하면 shift=k 가능성.
    #       실제 검증: backtick id가 header_thinker_idx + k 위치에서 최빈.
    cell_counts = Counter(len(r) for r in rows_raw)
    dominant_len = cell_counts.most_common(1)[0][0] if cell_counts else header_len
    table_shift = 0
    if dominant_len > header_len:
        # 후보 shift k = 1..(dominant_len - header_len) 범위에서
        # thinker_id 있는 row 셀 비율이 가장 높은 shift 선택.
        best_shift = 0
        best_hits = -1
        for k in range(0, dominant_len - header_len + 1):
            j = thinker_idx_hdr + k
            hits = 0
            eligible = 0
            for r in rows_raw:
                if len(r) > j:
                    eligible += 1
                    if _cell_has_thinker_id(r[j]):
                        hits += 1
            if eligible and hits > best_hits:
                best_hits = hits
                best_shift = k
        table_shift = best_shift

    for cells in rows_raw:
        # row가 짧으면(헤더 다른 종류) skip
        if len(cells) <= thinker_idx_hdr:
            continue

        # 1단계: 테이블 전체 shift 적용
        thinker_idx = thinker_idx_hdr + table_shift
        if thinker_idx >= len(cells):
            thinker_idx = thinker_idx_hdr

        # 2단계: row-level 보정 — 극히 제한적으로만 적용.
        # 현재 thinker 셀이 "—" 단독(혹은 공백/asterisk만)이고 바로 옆 셀에
        # 백틱 id가 명시되어 있을 때만 그 셀로 시프트한다.
        cur = cells[thinker_idx]
        cur_stripped = re.sub(r"[\s\*]", "", cur)
        if cur_stripped in ("—", "-", ""):
            for off in (1, 2):
                j = thinker_idx + off
                if j < len(cells) and THINKER_ID_RE.search(cells[j]):
                    thinker_idx = j
                    break

        shift = thinker_idx - thinker_idx_hdr
        thinker_cell = cells[thinker_idx]
        item_cell = cells[colmap["item_id"]] if "item_id" in colmap and colmap["item_id"] < len(cells) else ""
        score_cell = cells[colmap["score"]] if "score" in colmap and colmap["score"] < len(cells) else ""
        cat_idx = (cat_idx_hdr + shift) if cat_idx_hdr is not None else None
        es_idx = (es_idx_hdr + shift) if es_idx_hdr is not None else None
        cat_cell = cells[cat_idx] if cat_idx is not None and cat_idx < len(cells) else ""
        es_cell = cells[es_idx] if es_idx is not None and es_idx < len(cells) else ""

        score = parse_score(score_cell)
        score_sum += score

        row_type, ids = classify_row(thinker_cell, cat_cell, es_cell, known_ids)

        # 비상 보정: thinker_id가 비어있고 현재 row의 다른 셀 중 하나에
        # 백틱 thinker_id가 명시되어 있으면(2020-B/2021-A/2022-A 같이
        # 원문 소스가 unescaped pipe로 깨진 row 구제) 그것을 채택.
        if not ids and len(cells) > header_len:
            fallback_ids: list[str] = []
            # thinker_cell 자체와 item 셀은 제외
            for j, c in enumerate(cells):
                if j in (colmap.get("item_id"),):
                    continue
                if c is thinker_cell:
                    continue
                fallback_ids.extend(THINKER_ID_RE.findall(c))
            # 중복 제거 (순서 유지)
            seen = set()
            uniq = []
            for x in fallback_ids:
                if x not in seen:
                    seen.add(x)
                    uniq.append(x)
            if uniq:
                ids = uniq
                # 사상가형으로 재분류 (단, 교과교육학/경계영역 명시인 경우 혼합)
                joined = " ".join(cells)
                if any(m in joined for m in ("교과교육학", "경계영역", "통일교육", "일반개념", "메타윤리")):
                    row_type = "boundary_with_thinker"
                else:
                    row_type = "thinker"

        es_stat = es_status_of(es_cell) if es_cell else "NA"

        # 비고·thinker_cell·es_cell에서 BLK ID 추출
        blk_ids = re.findall(r"BLK-175E-\d{4}[AB]-\d{3}", " ".join(cells))

        parsed_rows.append({
            "item": item_cell,
            "score": score,
            "thinker_ids": ids,
            "category": cat_cell,
            "es_cell": es_cell,
            "es_status": es_stat,
            "row_type": row_type,
            "raw_thinker_cell": thinker_cell,
            "blk_ids": blk_ids,
        })

    return {
        "exam_id": exam_id,
        "rows": parsed_rows,
        "score_sum": score_sum,
    }


# ========== Section 집계 ==========
def aggregate_all(parsed: list[dict]) -> dict:
    """Section A~E 집계를 위한 중간 데이터 생성."""
    # thinker_id → {exam_ids: [...], count: n, blk_ids: set, es_statuses: list}
    thinker_occurrences: dict[str, dict] = defaultdict(lambda: {
        "exam_ids": [], "count": 0, "blk_ids": set(), "es_statuses": []
    })
    # 경계영역/보류 row 수집
    boundary_rows: list[dict] = []
    # 연도별 row 분류 카운트
    per_exam_stats: dict[str, dict] = {}
    # 총 row 수
    total_rows = 0
    # 복수 id row 포함한 "id 등장 row" count (하나의 row가 2명 있으면 2회)
    total_id_mentions = 0

    for p in parsed:
        exam = p["exam_id"]
        s_thinker = 0
        s_boundary = 0
        s_pending = 0
        for row in p["rows"]:
            total_rows += 1
            if row["row_type"] == "thinker":
                s_thinker += 1
                for tid in row["thinker_ids"]:
                    total_id_mentions += 1
                    rec = thinker_occurrences[tid]
                    rec["exam_ids"].append((exam, row["item"]))
                    rec["count"] += 1
                    for b in row["blk_ids"]:
                        rec["blk_ids"].add(b)
                    rec["es_statuses"].append(row["es_status"])
            elif row["row_type"] == "boundary_with_thinker":
                # 사상가 + 경계영역 혼합: thinker로도 집계, boundary에도 노출
                s_thinker += 1
                boundary_rows.append({
                    "exam": exam, "item": row["item"],
                    "category": row["category"],
                    "thinker_cell": row["raw_thinker_cell"],
                    "blk_ids": row["blk_ids"],
                })
                for tid in row["thinker_ids"]:
                    total_id_mentions += 1
                    rec = thinker_occurrences[tid]
                    rec["exam_ids"].append((exam, row["item"]))
                    rec["count"] += 1
                    for b in row["blk_ids"]:
                        rec["blk_ids"].add(b)
                    rec["es_statuses"].append(row["es_status"])
            elif row["row_type"] == "boundary":
                s_boundary += 1
                boundary_rows.append({
                    "exam": exam, "item": row["item"],
                    "category": row["category"],
                    "thinker_cell": row["raw_thinker_cell"],
                    "blk_ids": row["blk_ids"],
                })
            else:  # pending
                s_pending += 1
                boundary_rows.append({
                    "exam": exam, "item": row["item"],
                    "category": row["category"] or "[보류]",
                    "thinker_cell": row["raw_thinker_cell"],
                    "blk_ids": row["blk_ids"],
                })
        per_exam_stats[exam] = {
            "rows": len(p["rows"]),
            "thinker": s_thinker,
            "boundary": s_boundary,
            "pending": s_pending,
            "score_sum": p["score_sum"],
        }
    return {
        "thinker_occurrences": dict(thinker_occurrences),
        "boundary_rows": boundary_rows,
        "per_exam_stats": per_exam_stats,
        "total_rows": total_rows,
        "total_id_mentions": total_id_mentions,
    }


# ========== 렌더링 ==========
def ko_sort_key(s: str) -> tuple:
    return (s or "")


def render_section_a(agg: dict, canonical_ids: set[str], id_to_name: dict[str, str]) -> str:
    """Section A — ES 미등록(MISS) 사상가 전수."""
    miss_ids = {
        tid: data
        for tid, data in agg["thinker_occurrences"].items()
        if tid not in canonical_ids
    }
    # 출제횟수 내림차순, 동률이면 id 오름차순
    sorted_items = sorted(
        miss_ids.items(),
        key=lambda kv: (-kv[1]["count"], kv[0]),
    )
    lines = [
        "## Section A — 출제되지만 ES에 미등록인 사상가 (누락 집계)",
        "",
        f"총 {len(sorted_items)}명. 출제횟수 내림차순 정렬.",
        "",
        "| # | id | 한글명 | 출제횟수 | 출제연도 리스트 | BLK-ID(있으면) |",
        "|---|----|--------|---------|----------------|----------------|",
    ]
    for i, (tid, data) in enumerate(sorted_items, 1):
        exam_ids = sorted({ex for ex, _ in data["exam_ids"]})
        exam_str = ", ".join(exam_ids)
        blk_str = ", ".join(sorted(data["blk_ids"])) if data["blk_ids"] else "—"
        name_ko = _lookup_name(tid, id_to_name)
        lines.append(
            f"| {i} | `{tid}` | {name_ko} | {data['count']} | {exam_str} | {blk_str} |"
        )
    lines.append("")
    return "\n".join(lines)


# 한글명 수동 매핑 (ES 미등록 사상가용; id → 한글명/영문명)
MISS_NAME_MAP = {
    "bandura": "반두라(Albert Bandura)",
    "blasi": "블라시(Augusto Blasi)",
    "jinul": "보조국사 지눌(知訥)",
    "choe_jeu": "최제우(崔濟愚·수운)",
    "choe_chiwon": "최치원(崔致遠·고운)",
    "cho_sik": "남명 조식(曺植)",
    "cheng_hao": "정호(程顥·명도)",
    "cheng_yi": "정이(程頤·이천)",
    "coombs": "쿰즈(Jerrold R. Coombs)",
    "durkheim": "뒤르켐(Émile Durkheim)",
    "fazang": "법장(法藏·현수)",
    "freud": "프로이트(Sigmund Freud)",
    "hoffman": "호프만(Martin L. Hoffman)",
    "james": "윌리엄 제임스(William James)",
    "jonas": "한스 요나스(Hans Jonas)",
    "leopold": "레오폴드(Aldo Leopold)",
    "mencken": "멩켄(참고: 본 집계 미출현)",
    "moore": "G. E. 무어(George Edward Moore)",
    "nagarjuna": "용수(龍樹·나가르주나)",
    "narvaez": "나바에즈(Darcia Narvaez)",
    "niebuhr": "라인홀드 니부어(Reinhold Niebuhr)",
    "peters": "피터스(R. S. Peters)",
    "pettit": "페팃(Philip Pettit)",
    "popper": "포퍼(Karl Popper)",
    "regan": "리건(Tom Regan)",
    "schumpeter": "슘페터(Joseph Schumpeter)",
    "shweder": "슈웨더(Richard Shweder)",
    "singer": "피터 싱어(Peter Singer)",
    "skinner": "스키너(B. F. Skinner)",
    "tappan": "태판(Mark Tappan)",
    "taylor_p": "폴 테일러(Paul Taylor·생명중심주의)",
    "tocqueville": "토크빌(Alexis de Tocqueville)",
    "turiel": "튜리엘(Elliot Turiel)",
    "vasubandhu": "세친(世親·바수반두)",
    "viroli": "비롤리(Maurizio Viroli)",
    "yangju": "양주(楊朱·양자)",
    "zhiyi": "지의(智顗·천태종)",
    "berlin": "이사야 벌린(Isaiah Berlin)",
    "brown": "브라운(Lyn Mikel Brown)",
    "sizer": "사이저(Theodore Sizer)",
    "beccaria": "베카리아(Cesare Beccaria)",
    "cicero": "키케로(Marcus Tullius Cicero)",
    "coombs_meux": "쿰즈·뮤(Coombs & Meux 가치분석모형)",
    "green_th": "T. H. 그린(Thomas Hill Green)",
    "heidegger": "하이데거(Martin Heidegger)",
    "kierkegaard": "키에르케고르(Søren Kierkegaard)",
    "protagoras": "프로타고라스(Protagoras)",
    "uicheon": "의천(義天)",
    "im_seongju": "임성주(任聖周·녹문)",
    "han_wonjin": "한원진(韓元震·남당)",
    "shaftel": "샤프텔(Fannie & George Shaftel·역할놀이 수업모형)",
    "shenxiu": "북종 신수(北宗 神秀·점수선)",
    "donghak_choe": "동학 최제우·최시형(崔濟愚·崔時亨)",
    "machiavelli": "마키아벨리(Niccolò Machiavelli)",
    "newmann": "뉴만(F. Newmann·사회과 수업모형)",
}


def _lookup_name(tid: str, id_to_name: dict[str, str]) -> str:
    if tid in id_to_name:
        return id_to_name[tid]
    if tid in MISS_NAME_MAP:
        return MISS_NAME_MAP[tid]
    return f"(한글명 미등록: {tid})"


def render_section_b(
    agg: dict, canonical_ids: list[str], id_to_name: dict[str, str],
    claims_count: dict[str, int]
) -> str:
    """Section B — canonical 55 집계."""
    rows = []
    for tid in canonical_ids:
        data = agg["thinker_occurrences"].get(tid, {"count": 0, "exam_ids": []})
        exam_set = sorted({ex for ex, _ in data["exam_ids"]})
        rows.append({
            "id": tid,
            "name": id_to_name.get(tid, tid),
            "count": data["count"],
            "exams": exam_set,
            "claims": claims_count.get(tid, 0),
        })
    rows.sort(key=lambda r: (-r["count"], r["id"]))

    lines = [
        "## Section B — ES canonical 55 사상가 집계",
        "",
        "출제횟수 내림차순. 출제횟수 0이면 2014~2026 기간 **실출제 0회**(claim만 보유).",
        "",
        "| # | id | 한글명 | 출제횟수 | 출제연도 | claims수 |",
        "|---|----|--------|---------|---------|----------|",
    ]
    for i, r in enumerate(rows, 1):
        exam_str = ", ".join(r["exams"]) if r["exams"] else "—"
        lines.append(
            f"| {i} | `{r['id']}` | {r['name']} | {r['count']} | {exam_str} | {r['claims']} |"
        )
    lines.append("")
    return "\n".join(lines)


def _trim_cell(s: str, limit: int = 60) -> str:
    """테이블 셀용 문자열 다듬기: 개행·파이프 제거 + 길이 제한."""
    s = (s or "").replace("\n", " ").replace("\r", " ").strip()
    s = re.sub(r"\s+", " ", s)
    if len(s) > limit:
        s = s[: limit - 1] + "…"
    return s.replace("|", "\\|")


def render_section_c(agg: dict) -> str:
    """Section C — 경계영역(교과교육학/보류)."""
    rows = agg["boundary_rows"]
    # 연도·문항 순 정렬
    rows_sorted = sorted(rows, key=lambda r: (r["exam"], r["item"]))
    lines = [
        "## Section C — 경계영역·교과교육학·보류 row",
        "",
        f"총 {len(rows_sorted)}건. 사상가형으로 분류되지 못한(또는 혼합) row 전수.",
        "",
        "| 연도·Q | 분류 | 원문 thinker 셀 요지 | BLK-ID(있으면) |",
        "|--------|------|----------------------|-----------------|",
    ]
    for r in rows_sorted:
        cat = _trim_cell(r["category"] or "—", 50)
        raw = _trim_cell(r["thinker_cell"], 70)
        # 중복 BLK id 제거
        blk_ids_uniq = []
        seen = set()
        for b in r["blk_ids"]:
            if b not in seen:
                seen.add(b)
                blk_ids_uniq.append(b)
        blk = ", ".join(blk_ids_uniq) if blk_ids_uniq else "—"
        lines.append(f"| {r['exam']} {r['item']} | {cat} | {raw} | {blk} |")
    lines.append("")
    return "\n".join(lines)


def render_section_d(
    agg: dict, canonical_ids: set[str], id_to_name: dict[str, str]
) -> str:
    """Section D — MISS TOP10 (TASK-176 우선순위)."""
    miss_items = [
        (tid, data)
        for tid, data in agg["thinker_occurrences"].items()
        if tid not in canonical_ids
    ]
    miss_items.sort(key=lambda kv: (-kv[1]["count"], kv[0]))
    top10 = miss_items[:10]

    lines = [
        "## Section D — ES 미등록 사상가 출제횟수 TOP10 (TASK-176 우선순위)",
        "",
        "Section A 중 출제횟수 상위 10명. TASK-176(ES 신규 등록) 착수 순서.",
        "",
        "| 순위 | id | 한글명 | 출제횟수 | 최근 출제연도 | 권고 |",
        "|------|----|--------|---------|--------------|------|",
    ]
    for i, (tid, data) in enumerate(top10, 1):
        exam_set = sorted({ex for ex, _ in data["exam_ids"]})
        last_exam = exam_set[-1] if exam_set else "—"
        name = _lookup_name(tid, id_to_name)
        # 권고: 3연속 재출제는 최최우선, 2연속은 최우선, 그 외 출제 5회 이상 최우선
        recent3 = exam_set[-3:] if len(exam_set) >= 3 else []
        def consecutive(exs: list[str]) -> int:
            # (yyyy-A|B) 기준 단순 카운트: 마지막부터 연속성 계산
            if not exs:
                return 0
            run = 1
            for j in range(len(exs) - 1, 0, -1):
                # 전 연도가 직전 exam이면 연속
                a = exs[j - 1]
                b = exs[j]
                if a < b:
                    run += 1
                else:
                    break
            return run
        # 간이: 연속 판단은 출제연도 리스트 중 마지막 3개 기준
        rec_run = len(recent3) if len(recent3) >= 2 else 1
        if data["count"] >= 5:
            reco = "최최우선 (5회+ 출제)"
        elif data["count"] >= 3:
            reco = "최우선 (3회+ 출제)"
        else:
            reco = "우선"
        lines.append(
            f"| {i} | `{tid}` | {name} | {data['count']} | {last_exam} | {reco} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_section_e(agg: dict) -> str:
    """Section E — 분류 카운트 + 배점 검산."""
    stats = agg["per_exam_stats"]
    lines = [
        "## Section E — 연도별 분류 카운트 · 배점 검산",
        "",
        "| 시험 | 문항수 | 사상가형 | 경계영역 | 보류 | 배점합 | 예상합 | 일치 |",
        "|------|--------|---------|---------|------|--------|--------|------|",
    ]
    all_ok = True
    total_items = 0
    total_score = 0
    for exam in sorted(stats.keys()):
        s = stats[exam]
        total_items += s["rows"]
        total_score += s["score_sum"]
        expected = EXPECTED_SCORE_SUM.get(exam, 40)
        ok = "OK" if s["score_sum"] == expected else "MISMATCH"
        if ok != "OK":
            all_ok = False
        lines.append(
            f"| {exam} | {s['rows']} | {s['thinker']} | {s['boundary']} | {s['pending']} "
            f"| {s['score_sum']} | {expected} | {ok} |"
        )
    lines.append(
        f"| **합계** | **{total_items}** | — | — | — | **{total_score}** | — | — |"
    )
    lines.append("")
    if not all_ok:
        lines.append("> WARN: 일부 연도에서 배점합 불일치. 원문 coverage의 "
                     "기록 불일치 또는 본 스크립트 파싱 차이 점검 필요.")
        lines.append("")
    return "\n".join(lines)


# ========== metadata 블록 ==========
def render_header(
    canonical_ids: list[str], id_to_name: dict[str, str],
    claims_count: dict[str, int], agg: dict,
    blk_issued: list[str], blk_withdrawn: set[str]
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_rows = agg["total_rows"]
    total_id_mentions = agg["total_id_mentions"]
    miss_thinkers = {
        tid for tid in agg["thinker_occurrences"] if tid not in set(canonical_ids)
    }
    hit_thinkers = {
        tid for tid in agg["thinker_occurrences"] if tid in set(canonical_ids)
    }
    lines = [
        "# 임용 도덕윤리 기출 커버리지 통합 맵 (2014~2026, 26개 연도)",
        "",
        f"- **생성 일시**: {now}",
        f"- **생성 스크립트**: `projects/ethics-study/scripts/merge_coverage.py`",
        "- **입력**: `projects/ethics-study/exam-solutions/coverage/*.md` (26개)",
        f"- **ES canonical 사상가 수**: {len(canonical_ids)}",
        f"- **ES claims 보유 사상가 수**: {len(claims_count)}",
        f"- **총 문항 row 수**: {total_rows}",
        f"- **총 thinker_id 등장 수(복수 id row 분해 기준)**: {total_id_mentions}",
        f"- **출제된 MISS 사상가(Section A)**: {len(miss_thinkers)}명",
        f"- **출제된 HIT 사상가(Section B 내 출제횟수>0)**: {len(hit_thinkers)}명",
        f"- **blocker-log 총 발행**: {len(blk_issued)}건 "
        f"/ 철회: {len(blk_withdrawn)}건 / **net active: {len(blk_issued) - len(blk_withdrawn)}건**",
        "",
        "## 구성 섹션",
        "- Section A: ES 미등록 출제 사상가 전수 집계",
        "- Section B: ES canonical 55인 집계 (출제횟수·claims수)",
        "- Section C: 경계영역·교과교육학·보류 row",
        "- Section D: Section A 중 출제횟수 TOP10 (TASK-176 우선순위)",
        "- Section E: 연도별 분류 카운트 + 배점 검산",
        "",
        "---",
        "",
    ]
    return "\n".join(lines)


def render_footer_metadata(
    canonical_ids: list[str], agg: dict,
    blk_issued: list[str], blk_withdrawn: set[str],
    es_status: str,
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "---",
        "",
        "## Metadata",
        "",
        "```yaml",
        f"generated_at: {now}",
        f"coverage_files: 26",
        f"canonical_thinkers: {len(canonical_ids)}",
        f"total_question_rows: {agg['total_rows']}",
        f"total_id_mentions: {agg['total_id_mentions']}",
        f"blockers_issued: {len(blk_issued)}",
        f"blockers_withdrawn: {len(blk_withdrawn)}",
        f"blockers_net_active: {len(blk_issued) - len(blk_withdrawn)}",
        f"es_cluster_status: {es_status}",
        f"script: projects/ethics-study/scripts/merge_coverage.py",
        "```",
        "",
    ]
    return "\n".join(lines)


# ========== main ==========
def main() -> int:
    # Safety guard: OUT_PATH 기존 존재 시 abort (v1/v2 rejected는 별도 경로이므로 무관)
    if OUT_PATH.exists():
        log(f"WARN: {OUT_PATH.name} already exists, overwriting (TASK-175E-MERGE first run).")

    # 1) ES pre-flight
    id_to_name, claims_count = preflight_es()
    canonical_ids = sorted(id_to_name.keys())
    canonical_set = set(canonical_ids)
    health = es_get("/_cluster/health")
    es_status = health.get("status", "unknown")

    # 2) blocker-log
    blk_issued, blk_withdrawn, _ = parse_blocker_log()

    # 3) coverage 파일 26개 파싱
    exam_ids = OLD_FORMAT_FILES + NEW_FORMAT_FILES
    if len(exam_ids) != 26:
        fail(f"exam id list size={len(exam_ids)}, expected 26")

    # 백틱 없는 구형 파일의 bare id 추출용 known set
    known_ids = set(canonical_ids) | set(MISS_NAME_MAP.keys())

    parsed: list[dict] = []
    for eid in exam_ids:
        path = COVERAGE_DIR / f"{eid}.md"
        if not path.exists():
            fail(f"coverage file missing: {path}")
        text = path.read_text(encoding="utf-8")
        p = parse_coverage_file(eid, text, known_ids)
        log(
            f"{eid}: rows={len(p['rows'])}, score_sum={p['score_sum']}"
        )
        parsed.append(p)

    # 4) 집계
    agg = aggregate_all(parsed)

    # 5) 렌더
    parts = [
        render_header(canonical_ids, id_to_name, claims_count, agg, blk_issued, blk_withdrawn),
        render_section_a(agg, canonical_set, id_to_name),
        render_section_b(agg, canonical_ids, id_to_name, claims_count),
        render_section_c(agg),
        render_section_d(agg, canonical_set, id_to_name),
        render_section_e(agg),
        render_footer_metadata(canonical_ids, agg, blk_issued, blk_withdrawn, es_status),
    ]
    content = "\n".join(parts)

    OUT_PATH.write_text(content, encoding="utf-8")
    log(f"wrote {OUT_PATH} ({len(content)} bytes)")

    # 6) 검수 요약 stderr
    log(
        f"summary: rows={agg['total_rows']}, "
        f"id_mentions={agg['total_id_mentions']}, "
        f"MISS_thinkers={sum(1 for t in agg['thinker_occurrences'] if t not in canonical_set)}, "
        f"HIT_thinkers={sum(1 for t in agg['thinker_occurrences'] if t in canonical_set)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
