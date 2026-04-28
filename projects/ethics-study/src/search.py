"""검색 모듈 — 사상가, 키워드, 관계 등을 검색한다."""

from typing import Any, Dict, List

from elasticsearch import Elasticsearch

from src.config import (
    INDEX_CLAIMS,
    INDEX_KEYWORDS,
    INDEX_RELATIONS,
    INDEX_THINKERS,
    INDEX_WORKS,
)
from src.es_client import search_documents


def _hits(result: dict) -> list:
    """ES 검색 결과에서 _source 리스트를 추출한다."""
    return [hit["_source"] for hit in result["hits"]["hits"]]


def search_thinker_by_name(client: Elasticsearch, name: str) -> list:
    """사상가 이름(한글 또는 영문)으로 검색한다."""
    query = {
        "multi_match": {
            "query": name,
            "fields": ["name", "name.keyword", "name_en", "name_en.keyword"],
            "type": "best_fields",
        }
    }
    result = search_documents(client, INDEX_THINKERS, query, size=10)
    return _hits(result)


def get_thinker_full(client: Elasticsearch, thinker_id: str) -> dict:
    """사상가 ID로 종합 정보를 조회한다.

    Returns:
        {
            'thinker': {...},
            'works': [...],
            'claims': [...],
            'keywords': [...],
            'relations': [...]
        }
    """
    # thinker
    thinker_result = search_documents(
        client, INDEX_THINKERS, {"term": {"id": thinker_id}}, size=1
    )
    thinkers = _hits(thinker_result)
    thinker = thinkers[0] if thinkers else None

    # works
    works_result = search_documents(
        client, INDEX_WORKS, {"term": {"thinker_id": thinker_id}}, size=100
    )
    works = _hits(works_result)

    # claims
    claims_result = search_documents(
        client, INDEX_CLAIMS, {"term": {"thinker_id": thinker_id}}, size=100
    )
    claims = _hits(claims_result)

    # keywords
    kw_result = search_documents(
        client, INDEX_KEYWORDS, {"term": {"thinker_id": thinker_id}}, size=100
    )
    keywords = _hits(kw_result)

    # relations (from or to)
    from_result = search_documents(
        client, INDEX_RELATIONS, {"term": {"from_thinker": thinker_id}}, size=100
    )
    to_result = search_documents(
        client, INDEX_RELATIONS, {"term": {"to_thinker": thinker_id}}, size=100
    )
    relations = _hits(from_result) + _hits(to_result)
    # 중복 제거
    seen_ids = set()
    unique_relations = []
    for rel in relations:
        rid = rel.get("id", id(rel))
        if rid not in seen_ids:
            seen_ids.add(rid)
            unique_relations.append(rel)

    return {
        "thinker": thinker,
        "works": works,
        "claims": claims,
        "keywords": keywords,
        "relations": unique_relations,
    }


def search_by_keyword(client: Elasticsearch, keyword: str) -> dict:
    """키워드로 관련 사상가, 주장, 키워드 정의를 검색한다.

    ethics-claims, ethics-keywords, ethics-thinkers 인덱스를 멀티 검색한다.

    Returns:
        {
            'thinkers': [...],
            'claims': [...],
            'keywords': [...]
        }
    """
    # thinkers — 키워드 필드 또는 핵심 사상에서 검색
    thinker_query = {
        "bool": {
            "should": [
                {"term": {"keywords": keyword}},
                {"match": {"core_philosophy": keyword}},
                {"match": {"name": keyword}},
            ]
        }
    }
    thinker_result = search_documents(client, INDEX_THINKERS, thinker_query, size=10)

    # claims — 주장 내용 또는 키워드에서 검색
    claim_query = {
        "bool": {
            "should": [
                {"term": {"keywords": keyword}},
                {"match": {"claim": keyword}},
                {"match": {"explanation": keyword}},
            ]
        }
    }
    claim_result = search_documents(client, INDEX_CLAIMS, claim_query, size=20)

    # keywords — 용어 또는 정의에서 검색
    kw_query = {
        "bool": {
            "should": [
                {"match": {"term": keyword}},
                {"match": {"term_en": keyword}},
                {"match": {"definition": keyword}},
                {"term": {"related_terms": keyword}},
            ]
        }
    }
    kw_result = search_documents(client, INDEX_KEYWORDS, kw_query, size=20)

    return {
        "thinkers": _hits(thinker_result),
        "claims": _hits(claim_result),
        "keywords": _hits(kw_result),
    }


def get_relations(client: Elasticsearch, thinker_id: str) -> dict:
    """특정 사상가의 관계를 조회한다.

    Returns:
        {
            'outgoing': [...],  # from_thinker == thinker_id
            'incoming': [...]   # to_thinker == thinker_id
        }
    """
    from_result = search_documents(
        client, INDEX_RELATIONS, {"term": {"from_thinker": thinker_id}}, size=100
    )
    to_result = search_documents(
        client, INDEX_RELATIONS, {"term": {"to_thinker": thinker_id}}, size=100
    )
    return {
        "outgoing": _hits(from_result),
        "incoming": _hits(to_result),
    }


def get_unverified_claims(client: Elasticsearch) -> list:
    """verified: false인 claim 목록을 반환한다."""
    query = {"term": {"verified": False}}
    result = search_documents(client, INDEX_CLAIMS, query, size=1000)
    return _hits(result)


def search_by_field(client: Elasticsearch, field_id: str) -> list:
    """특정 분야의 사상가 목록을 반환한다."""
    query = {"term": {"field": field_id}}
    result = search_documents(client, INDEX_THINKERS, query, size=100)
    return _hits(result)
