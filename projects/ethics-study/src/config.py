"""설정 모듈 — ES 연결 정보 및 인덱스 이름 관리.

환경변수로 오버라이드 가능:
  ES_HOST, ES_PORT, ES_INDEX_PREFIX
"""

import os


# Elasticsearch 연결 정보
ES_HOST = os.environ.get("ES_HOST", "localhost")
ES_PORT = int(os.environ.get("ES_PORT", "9200"))
ES_URL = f"http://{ES_HOST}:{ES_PORT}"

# 인덱스 이름 상수
INDEX_PREFIX = os.environ.get("ES_INDEX_PREFIX", "ethics")

INDEX_THINKERS = f"{INDEX_PREFIX}-thinkers"
INDEX_WORKS = f"{INDEX_PREFIX}-works"
INDEX_CLAIMS = f"{INDEX_PREFIX}-claims"
INDEX_KEYWORDS = f"{INDEX_PREFIX}-keywords"
INDEX_RELATIONS = f"{INDEX_PREFIX}-relations"
INDEX_FIELDS = f"{INDEX_PREFIX}-fields"

ALL_INDICES = [
    INDEX_THINKERS,
    INDEX_WORKS,
    INDEX_CLAIMS,
    INDEX_KEYWORDS,
    INDEX_RELATIONS,
    INDEX_FIELDS,
]
