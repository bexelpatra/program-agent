"""test_config.py -- config.py 단위 테스트."""

import os

import pytest


class TestConfigConstants:
    """인덱스 상수 및 ES 설정 테스트."""

    def test_six_index_constants_defined(self):
        """6개 인덱스 상수가 정의되어 있어야 한다."""
        from src.config import (
            INDEX_THINKERS,
            INDEX_WORKS,
            INDEX_CLAIMS,
            INDEX_KEYWORDS,
            INDEX_RELATIONS,
            INDEX_FIELDS,
        )

        indices = [
            INDEX_THINKERS,
            INDEX_WORKS,
            INDEX_CLAIMS,
            INDEX_KEYWORDS,
            INDEX_RELATIONS,
            INDEX_FIELDS,
        ]
        assert len(indices) == 6
        for idx in indices:
            assert isinstance(idx, str)
            assert len(idx) > 0

    def test_all_indices_contains_all(self):
        """ALL_INDICES가 6개 인덱스를 모두 포함해야 한다."""
        from src.config import (
            ALL_INDICES,
            INDEX_THINKERS,
            INDEX_WORKS,
            INDEX_CLAIMS,
            INDEX_KEYWORDS,
            INDEX_RELATIONS,
            INDEX_FIELDS,
        )

        assert len(ALL_INDICES) == 6
        assert INDEX_THINKERS in ALL_INDICES
        assert INDEX_WORKS in ALL_INDICES
        assert INDEX_CLAIMS in ALL_INDICES
        assert INDEX_KEYWORDS in ALL_INDICES
        assert INDEX_RELATIONS in ALL_INDICES
        assert INDEX_FIELDS in ALL_INDICES

    def test_es_url_format(self):
        """ES_URL이 http://host:port 형식이어야 한다."""
        from src.config import ES_URL

        assert ES_URL.startswith("http://")
        # host:port 구조 확인
        after_scheme = ES_URL[len("http://") :]
        parts = after_scheme.split(":")
        assert len(parts) == 2
        host, port = parts
        assert len(host) > 0
        assert port.isdigit()

    def test_default_es_host_and_port(self):
        """기본값이 localhost:9200 이어야 한다."""
        from src.config import ES_HOST, ES_PORT

        assert ES_HOST == "localhost"
        assert ES_PORT == 9200

    def test_index_prefix_default(self):
        """기본 인덱스 접두사가 'ethics' 이어야 한다."""
        from src.config import INDEX_PREFIX

        assert INDEX_PREFIX == "ethics"

    def test_indices_start_with_prefix(self):
        """모든 인덱스 이름이 INDEX_PREFIX로 시작해야 한다."""
        from src.config import ALL_INDICES, INDEX_PREFIX

        for idx in ALL_INDICES:
            assert idx.startswith(
                INDEX_PREFIX
            ), f"{idx} does not start with {INDEX_PREFIX}"
