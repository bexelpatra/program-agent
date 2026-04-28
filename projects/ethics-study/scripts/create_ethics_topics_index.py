"""ethics-topics ES index 생성 스크립트.

Task: TASK-178 — Phase 6 경계영역 주제 (쟁점 중심) 인덱스 신설.
architecture.md L134-L181 스키마를 ES mapping JSON 으로 변환.
이미 존재 시 skip (idempotent).

매핑 설계 근거 (signal/ethics-study/architecture.md L134-L181):
 - id/name/name_en/category : keyword (정확 일치 검색, aggregation 대상)
 - description              : text (한글 분석기 기본)
 - subtopics/key_issues/keywords             : keyword array
 - related_thinker_ids/related_claim_ids     : keyword array (cross-index join)
 - exam_appearances   : nested (year·question_number·summary 각 개별 검색)
 - verbatim_sources   : nested (file·line·quote 각 개별 검색)

※ 본 스크립트는 schema-레벨 infra 이므로 원문 인용 자기검증 대상 아님
  (architecture.md 지시에 따라 enum 값 및 필드명만 사용).
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client, create_index, index_exists
from src.config import INDEX_PREFIX


INDEX_TOPICS = f"{INDEX_PREFIX}-topics"


TOPICS_MAPPING = {
    "properties": {
        "id": {"type": "keyword"},
        "name": {"type": "keyword"},
        "name_en": {"type": "keyword"},
        "category": {"type": "keyword"},
        "description": {"type": "text"},
        "subtopics": {"type": "keyword"},
        "key_issues": {"type": "keyword"},
        "keywords": {"type": "keyword"},
        "related_thinker_ids": {"type": "keyword"},
        "related_claim_ids": {"type": "keyword"},
        "exam_appearances": {
            "type": "nested",
            "properties": {
                "year": {"type": "keyword"},
                "question_number": {"type": "keyword"},
                "summary": {"type": "text"},
            },
        },
        "verbatim_sources": {
            "type": "nested",
            "properties": {
                "file": {"type": "keyword"},
                "line": {"type": "keyword"},
                "quote": {"type": "text"},
            },
        },
    }
}


def main():
    client = get_client()
    try:
        if index_exists(client, INDEX_TOPICS):
            print(f"[index] {INDEX_TOPICS}: already exists")
            return

        result = create_index(client, INDEX_TOPICS, mappings=TOPICS_MAPPING)
        if result.get("already_exists"):
            print(f"[index] {INDEX_TOPICS}: already exists")
        else:
            print(f"[index] {INDEX_TOPICS}: created")
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
