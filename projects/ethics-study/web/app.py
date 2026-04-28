"""
Ethics Study Guide - Web UI
FastAPI app for browsing thinkers indexed in Elasticsearch.
"""

import logging
import re

from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from elasticsearch import Elasticsearch
import os

from search import search_all
from markdown_renderer import render as render_markdown, render_with_toc, verify_verbatim

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(__file__)

app = FastAPI(title="Ethics Study Guide")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

es = Elasticsearch(
    "http://localhost:9200",
    verify_certs=False,
)

FIELD_LABELS = {
    "western_ethics": "서양윤리",
    "eastern_ethics": "동양윤리",
    "political_philosophy": "정치철학·사회사상",
}

RELATION_TYPE_LABELS = {
    "influenced": "영향을 줌",
    "influenced_by": "영향을 받음",
    "criticized": "비판함",
    "developed": "발전시킴",
    "synthesized": "종합함",
}


def get_thinker_id_name_map() -> dict[str, str]:
    """Return a dict mapping thinker id → Korean name for all registered thinkers."""
    try:
        resp = es.search(
            index="ethics-thinkers",
            body={
                "size": 200,
                "_source": ["id", "name"],
            },
        )
        mapping: dict[str, str] = {}
        for hit in resp["hits"]["hits"]:
            src = hit["_source"]
            tid = src.get("id") or hit["_id"]
            name = src.get("name", tid)
            mapping[tid] = name
            # Also index by _id in case id field differs
            mapping[hit["_id"]] = name
        return mapping
    except Exception:
        logging.exception("Failed to build thinker id→name map")
        return {}


def get_all_thinkers() -> list[dict]:
    """Fetch all thinkers from ES, sorted by birth_year."""
    resp = es.search(
        index="ethics-thinkers",
        body={
            "size": 200,
            "sort": [{"birth_year": {"order": "asc", "missing": "_last"}}],
            "_source": [
                "id", "name", "name_en", "field", "era",
                "birth_year", "death_year", "core_philosophy", "keywords",
            ],
        },
    )
    thinkers = []
    for hit in resp["hits"]["hits"]:
        src = hit["_source"]
        src.setdefault("id", hit["_id"])
        # Truncate core_philosophy for card preview
        cp = src.get("core_philosophy", "")
        src["core_philosophy_short"] = cp[:120] + "…" if len(cp) > 120 else cp
        src["field_label"] = FIELD_LABELS.get(src.get("field", ""), src.get("field", ""))
        thinkers.append(src)
    return thinkers


def group_by_field(thinkers: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for t in thinkers:
        f = t.get("field", "other")
        groups.setdefault(f, []).append(t)
    return groups


def get_thinker(thinker_id: str) -> dict | None:
    """Fetch a single thinker by ID from ES (all fields)."""
    try:
        resp = es.get(index="ethics-thinkers", id=thinker_id)
        src = resp["_source"]
        src.setdefault("id", resp["_id"])
        src["field_label"] = FIELD_LABELS.get(src.get("field", ""), src.get("field", ""))
        return src
    except Exception:
        logger.exception("Direct get failed for thinker_id=%s, trying search", thinker_id)
        # Try searching by 'id' field if direct get fails
        try:
            resp = es.search(
                index="ethics-thinkers",
                body={"query": {"term": {"id": thinker_id}}, "size": 1},
            )
            hits = resp["hits"]["hits"]
            if not hits:
                return None
            src = hits[0]["_source"]
            src.setdefault("id", hits[0]["_id"])
            src["field_label"] = FIELD_LABELS.get(src.get("field", ""), src.get("field", ""))
            return src
        except Exception:
            logger.exception("Search fallback also failed for thinker_id=%s", thinker_id)
            return None


def get_thinker_works(thinker_id: str) -> list[dict]:
    """Fetch works for a thinker, sorted by year."""
    try:
        resp = es.search(
            index="ethics-works",
            body={
                "size": 100,
                "query": {"term": {"thinker_id": thinker_id}},
                "sort": [{"year": {"order": "asc", "missing": "_last"}}],
                "_source": ["id", "thinker_id", "title", "title_original", "year", "significance", "key_concepts"],
            },
        )
        works = []
        for hit in resp["hits"]["hits"]:
            src = hit["_source"]
            src.setdefault("id", hit["_id"])
            works.append(src)
        return works
    except Exception:
        logger.exception("Failed to fetch works for thinker_id=%s", thinker_id)
        return []


def get_thinker_claims(thinker_id: str) -> list[dict]:
    """Fetch claims for a thinker."""
    try:
        resp = es.search(
            index="ethics-claims",
            body={
                "size": 100,
                "query": {"term": {"thinker_id": thinker_id}},
                "_source": [
                    "id", "thinker_id", "work_id", "source_detail",
                    "claim", "original_text", "explanation",
                    "argument", "counterpoint", "context", "keywords", "verified",
                ],
            },
        )
        claims = []
        for hit in resp["hits"]["hits"]:
            src = hit["_source"]
            src.setdefault("id", hit["_id"])
            claims.append(src)
        return claims
    except Exception:
        logger.exception("Failed to fetch claims for thinker_id=%s", thinker_id)
        return []


def get_thinker_keywords(thinker_id: str) -> list[dict]:
    """Fetch keywords associated with a thinker."""
    try:
        resp = es.search(
            index="ethics-keywords",
            body={
                "size": 100,
                "query": {"term": {"thinker_id": thinker_id}},
                "_source": ["id", "term", "term_en", "definition", "thinker_id", "work_id", "related_terms"],
            },
        )
        keywords = []
        for hit in resp["hits"]["hits"]:
            src = hit["_source"]
            src.setdefault("id", hit["_id"])
            keywords.append(src)
        return keywords
    except Exception:
        logger.exception("Failed to fetch keywords for thinker_id=%s", thinker_id)
        return []


def get_thinker_relations(thinker_id: str) -> list[dict]:
    """Fetch relations where thinker is either from_thinker or to_thinker."""
    try:
        resp = es.search(
            index="ethics-relations",
            body={
                "size": 100,
                "query": {
                    "bool": {
                        "should": [
                            {"term": {"from_thinker": thinker_id}},
                            {"term": {"to_thinker": thinker_id}},
                        ],
                        "minimum_should_match": 1,
                    }
                },
                "_source": ["from_thinker", "to_thinker", "type", "description", "evidence"],
            },
        )

        # Build id→name cache for resolving thinker names
        name_map = get_thinker_id_name_map()
        registered_ids = set(name_map.keys())

        relations = []
        for hit in resp["hits"]["hits"]:
            src = hit["_source"]
            src.setdefault("id", hit["_id"])

            from_id = src.get("from_thinker", "")
            to_id = src.get("to_thinker", "")

            # Resolve human-readable names (fall back to ID if not found)
            src["from_thinker_name"] = name_map.get(from_id, from_id)
            src["to_thinker_name"] = name_map.get(to_id, to_id)

            # Flag whether each thinker is registered (for safe link rendering)
            src["from_thinker_exists"] = from_id in registered_ids
            src["to_thinker_exists"] = to_id in registered_ids

            # Korean label for relation type
            rel_type = src.get("type", "")
            src["type_label"] = RELATION_TYPE_LABELS.get(rel_type, rel_type)

            # Tag direction relative to current thinker
            if from_id == thinker_id:
                src["direction"] = "outgoing"  # this thinker → to_thinker
            else:
                src["direction"] = "incoming"  # from_thinker → this thinker

            relations.append(src)
        return relations
    except Exception:
        logger.exception("Failed to fetch relations for thinker_id=%s", thinker_id)
        return []


# ─────────────────────────────────────────────
# HTML Routes
# ─────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    thinkers = get_all_thinkers()
    groups = group_by_field(thinkers)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "thinkers": thinkers,
            "groups": groups,
            "field_labels": FIELD_LABELS,
            "total": len(thinkers),
        },
    )


@app.get("/thinker/{thinker_id}", response_class=HTMLResponse)
async def thinker_detail(request: Request, thinker_id: str):
    thinker = get_thinker(thinker_id)
    if thinker is None:
        return HTMLResponse(content="<h1>사상가를 찾을 수 없습니다.</h1>", status_code=404)
    works = get_thinker_works(thinker_id)
    claims = get_thinker_claims(thinker_id)
    keywords = get_thinker_keywords(thinker_id)
    relations = get_thinker_relations(thinker_id)
    return templates.TemplateResponse(
        request=request,
        name="thinker.html",
        context={
            "thinker": thinker,
            "thinker_id": thinker_id,
            "works": works,
            "claims": claims,
            "keywords": keywords,
            "relations": relations,
        },
    )


@app.get("/search", response_class=HTMLResponse)
async def search_page(request: Request, q: str = Query(default="")):
    results = search_all(es, q.strip())
    return templates.TemplateResponse(
        request=request,
        name="search.html",
        context={
            "q": q,
            "total": results["total"],
            "claims": results["claims"],
            "keywords": results["keywords"],
            "works": results["works"],
        },
    )


# ─────────────────────────────────────────────
# JSON API Routes
# ─────────────────────────────────────────────

@app.get("/api/thinkers")
async def api_thinkers():
    thinkers = get_all_thinkers()
    return JSONResponse({"total": len(thinkers), "thinkers": thinkers})


@app.get("/api/thinker/{thinker_id}")
async def api_thinker_detail(thinker_id: str):
    thinker = get_thinker(thinker_id)
    if thinker is None:
        return JSONResponse({"error": "Not found"}, status_code=404)
    works = get_thinker_works(thinker_id)
    claims = get_thinker_claims(thinker_id)
    keywords = get_thinker_keywords(thinker_id)
    relations = get_thinker_relations(thinker_id)
    return JSONResponse({
        "thinker": thinker,
        "works": works,
        "claims": claims,
        "keywords": keywords,
        "relations": relations,
    })


@app.get("/api/search")
async def api_search(q: str = Query(default="")):
    results = search_all(es, q.strip())
    return JSONResponse(results)


# ─────────────────────────────────────────────
# Phase A: Exam Document Viewer (study-guide + coverage)
# ─────────────────────────────────────────────

# 기출 산출물 루트 (web/ 의 형제 디렉토리 exam-solutions/).
_EXAM_ROOT = os.path.normpath(
    os.path.join(BASE_DIR, "..", "exam-solutions")
)
_STUDY_GUIDE_DIR = os.path.join(_EXAM_ROOT, "study-guide")
_COVERAGE_DIR = os.path.join(_EXAM_ROOT, "coverage")

# year-slot 형식 검증: YYYY-{A|B} (대문자 정확히).
_EXAM_KEY_RE = re.compile(r"^(\d{4})-([AB])$")

# study-guide 의 문항 헤더만 흡수하는 정규식 (architecture.md L411).
# 변종: "## 문항 N" / "## 문항 서술형 N" / "## 문항 논술형 N" / "## 문항 기입형 N".
# coverage 는 헤더 형식이 분산 (## Q1 [...] · ## N. · 표 only) 이므로 TOC 미생성.
_TOC_PATTERN = re.compile(
    r"^## 문항(?:\s+(?:서술형|논술형|기입형))?\s+\d+",
    re.MULTILINE,
)


def _list_exam_keys() -> list[str]:
    """Return sorted list of `{YYYY}-{A|B}` keys present in BOTH directories."""
    if not (os.path.isdir(_STUDY_GUIDE_DIR) and os.path.isdir(_COVERAGE_DIR)):
        return []
    sg = {f[:-3] for f in os.listdir(_STUDY_GUIDE_DIR)
          if f.endswith(".md") and _EXAM_KEY_RE.match(f[:-3])}
    cv = {f[:-3] for f in os.listdir(_COVERAGE_DIR)
          if f.endswith(".md") and _EXAM_KEY_RE.match(f[:-3])}
    return sorted(sg & cv)


def _read_exam_md(directory: str, key: str) -> str:
    """Read a `{key}.md` file from `directory`. Raises FileNotFoundError if absent."""
    path = os.path.join(directory, f"{key}.md")
    with open(path, encoding="utf-8") as fp:
        return fp.read()


def _extract_toc(md_text: str) -> list[str]:
    """Extract per-question headers from study-guide markdown.

    Returns list of header strings (e.g. "## 문항 1", "## 문항 서술형 2").
    coverage.md 는 헤더 분산으로 호출하지 않는다 (architecture.md L411).
    """
    return _TOC_PATTERN.findall(md_text)


def _log_verbatim(year: str, slot: str, kind: str, md_text: str, html_body: str) -> None:
    """Log 5-class verbatim count comparison for one exam document."""
    counts = verify_verbatim(md_text, html_body)
    mismatches = [k for k, (m, h) in counts.items() if m != h]
    summary = " ".join(f"{k}={m}/{h}" for k, (m, h) in counts.items())
    if mismatches:
        logger.warning(
            "VERBATIM MISMATCH %s/%s/%s: %s (mismatched=%s)",
            year, slot, kind, summary, ",".join(mismatches),
        )
    else:
        logger.info("verbatim %s/%s/%s: %s", year, slot, kind, summary)


@app.get("/exam", response_class=HTMLResponse)
async def list_exams(request: Request):
    """List all exam years/slots having BOTH study-guide and coverage."""
    keys = _list_exam_keys()
    # 카드 그리드용 dict list (연도/슬롯 + 두 link).
    entries = [{"key": k, "year": k[:4], "slot": k[5:]} for k in keys]
    return templates.TemplateResponse(
        request=request,
        name="exam_index.html",
        context={"entries": entries, "total": len(entries)},
    )


@app.get("/exam/{exam_key}", response_class=HTMLResponse)
async def view_exam(request: Request, exam_key: str):
    """Render study-guide + coverage tabs for one `{YYYY}-{A|B}` key."""
    m = _EXAM_KEY_RE.match(exam_key)
    if not m:
        raise HTTPException(status_code=404, detail="Invalid exam key format")
    year, slot = m.group(1), m.group(2)

    try:
        sg_md = _read_exam_md(_STUDY_GUIDE_DIR, exam_key)
        cv_md = _read_exam_md(_COVERAGE_DIR, exam_key)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Exam document not found")

    sg_html, toc = render_with_toc(sg_md)
    cv_html = render_markdown(cv_md)

    # byte-level verbatim 검증 logging (mismatch 시 warning).
    _log_verbatim(year, slot, "study-guide", sg_md, sg_html)
    _log_verbatim(year, slot, "coverage", cv_md, cv_html)

    # 좌측 사이드바용 전체 nav list (현재 page highlight 용).
    nav_keys = _list_exam_keys()

    return templates.TemplateResponse(
        request=request,
        name="exam_detail.html",
        context={
            "exam_key": exam_key,
            "year": year,
            "slot": slot,
            "study_guide_html": sg_html,
            "coverage_html": cv_html,
            "toc": toc,
            "nav_keys": nav_keys,
        },
    )
