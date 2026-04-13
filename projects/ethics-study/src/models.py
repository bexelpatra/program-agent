"""데이터 모델 — ES 인덱스 매핑 정의 및 인덱스 초기화.

각 인덱스의 매핑을 딕셔너리로 정의하고,
init_all_indices()로 모든 인덱스를 한 번에 생성할 수 있다.
"""

from typing import Any, Dict

from elasticsearch import Elasticsearch

from src.config import (
    INDEX_CLAIMS,
    INDEX_FIELDS,
    INDEX_KEYWORDS,
    INDEX_RELATIONS,
    INDEX_THINKERS,
    INDEX_WORKS,
)
from src.es_client import create_index


# ── 공통 설정 ────────────────────────────────────────────────

# 한국어 텍스트 분석을 위한 인덱스 설정
# nori가 설치된 환경에서는 nori_tokenizer 사용, 아니면 standard로 폴백
INDEX_SETTINGS: Dict[str, Any] = {
    "analysis": {
        "analyzer": {
            "korean": {
                "type": "custom",
                "tokenizer": "nori_tokenizer",
                "filter": ["nori_readingform", "lowercase"],
            }
        }
    }
}

INDEX_SETTINGS_FALLBACK: Dict[str, Any] = {
    "analysis": {
        "analyzer": {
            "korean": {
                "type": "standard",
            }
        }
    }
}


def _text_field(analyzer: str = "korean") -> Dict[str, Any]:
    """한국어 text 필드 매핑을 반환한다."""
    return {"type": "text", "analyzer": analyzer}


def _text_with_keyword(analyzer: str = "korean") -> Dict[str, Any]:
    """text + keyword 서브필드를 가진 매핑을 반환한다."""
    return {
        "type": "text",
        "analyzer": analyzer,
        "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
    }


# ── 인덱스 매핑 정의 ────────────────────────────────────────

THINKERS_MAPPINGS: Dict[str, Any] = {
    "properties": {
        "id": {"type": "keyword"},
        "name": _text_with_keyword("korean"),
        "name_en": _text_with_keyword("standard"),
        "field": {"type": "keyword"},
        "era": {"type": "keyword"},
        "birth_year": {"type": "integer"},
        "death_year": {"type": "integer"},
        "background": _text_field("korean"),
        "core_philosophy": _text_field("korean"),
        "philosophical_journey": _text_field("korean"),
        "keywords": {"type": "keyword"},
    }
}

WORKS_MAPPINGS: Dict[str, Any] = {
    "properties": {
        "id": {"type": "keyword"},
        "thinker_id": {"type": "keyword"},
        "title": _text_with_keyword("korean"),
        "title_original": _text_field("standard"),
        "year": {"type": "integer"},
        "significance": _text_field("korean"),
        "key_concepts": {"type": "keyword"},
    }
}

CLAIMS_MAPPINGS: Dict[str, Any] = {
    "properties": {
        "id": {"type": "keyword"},
        "thinker_id": {"type": "keyword"},
        "work_id": {"type": "keyword"},
        "source_detail": _text_field("korean"),
        "claim": _text_field("korean"),
        "original_text": _text_field("korean"),
        "original_text_ko": _text_field("korean"),
        "explanation": _text_field("korean"),
        "context": _text_field("korean"),
        "argument": _text_field("korean"),
        "counterpoint": _text_field("korean"),
        "keywords": {"type": "keyword"},
        "verified": {"type": "boolean"},
        "verification_log": {
            "type": "nested",
            "properties": {
                "date": {"type": "keyword"},
                "method": {"type": "keyword"},
                "result": {"type": "keyword"},
            },
        },
    }
}

KEYWORDS_MAPPINGS: Dict[str, Any] = {
    "properties": {
        "id": {"type": "keyword"},
        "term": _text_with_keyword("korean"),
        "term_en": _text_with_keyword("standard"),
        "definition": _text_field("korean"),
        "thinker_id": {"type": "keyword"},
        "work_id": {"type": "keyword"},
        "related_terms": {"type": "keyword"},
    }
}

RELATIONS_MAPPINGS: Dict[str, Any] = {
    "properties": {
        "id": {"type": "keyword"},
        "from_thinker": {"type": "keyword"},
        "to_thinker": {"type": "keyword"},
        "type": {"type": "keyword"},
        "description": _text_field("korean"),
        "evidence": _text_field("korean"),
    }
}

FIELDS_MAPPINGS: Dict[str, Any] = {
    "properties": {
        "id": {"type": "keyword"},
        "name": _text_with_keyword("korean"),
        "description": _text_field("korean"),
        "order": {"type": "integer"},
    }
}


# ── 매핑 조회 및 인덱스 초기화 ──────────────────────────────


def get_all_mappings() -> Dict[str, Dict[str, Any]]:
    """인덱스명 -> 매핑 딕셔너리를 반환한다."""
    return {
        INDEX_THINKERS: THINKERS_MAPPINGS,
        INDEX_WORKS: WORKS_MAPPINGS,
        INDEX_CLAIMS: CLAIMS_MAPPINGS,
        INDEX_KEYWORDS: KEYWORDS_MAPPINGS,
        INDEX_RELATIONS: RELATIONS_MAPPINGS,
        INDEX_FIELDS: FIELDS_MAPPINGS,
    }


def _detect_settings(client: Elasticsearch) -> Dict[str, Any]:
    """nori 플러그인 설치 여부에 따라 적절한 인덱스 설정을 반환한다."""
    try:
        # 임시 테스트 인덱스로 nori 가용 여부 확인
        test_idx = "__nori_test__"
        # 이미 존재하면 먼저 삭제
        if client.indices.exists(index=test_idx):
            client.indices.delete(index=test_idx)
        client.indices.create(
            index=test_idx,
            body={"settings": INDEX_SETTINGS},
        )
        # 성공했으면 테스트 인덱스 정리
        client.indices.delete(index=test_idx)
        return INDEX_SETTINGS
    except Exception:
        return INDEX_SETTINGS_FALLBACK


def init_all_indices(client: Elasticsearch) -> None:
    """모든 인덱스를 매핑과 함께 생성한다. 이미 존재하면 스킵."""
    settings = _detect_settings(client)
    for index_name, mappings in get_all_mappings().items():
        create_index(
            client,
            index=index_name,
            mappings=mappings,
            settings=settings,
        )
