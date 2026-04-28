"""test_search.py -- search.py 단위 테스트."""

from unittest.mock import MagicMock, patch, call

import pytest

from src.config import (
    INDEX_CLAIMS,
    INDEX_KEYWORDS,
    INDEX_RELATIONS,
    INDEX_THINKERS,
    INDEX_WORKS,
)
from src.search import (
    _hits,
    search_thinker_by_name,
    get_thinker_full,
    search_by_keyword,
    get_relations,
    get_unverified_claims,
    search_by_field,
)


def _make_es_result(sources):
    """ES 검색 결과 형식의 mock 데이터를 생성한다."""
    return {"hits": {"hits": [{"_source": s} for s in sources]}}


class TestHits:
    """_hits 헬퍼 테스트."""

    def test_extracts_sources(self):
        result = _make_es_result([{"name": "a"}, {"name": "b"}])
        assert _hits(result) == [{"name": "a"}, {"name": "b"}]

    def test_empty_result(self):
        result = _make_es_result([])
        assert _hits(result) == []


class TestSearchThinkerByName:
    """search_thinker_by_name 테스트."""

    @patch("src.search.search_documents")
    def test_query_structure(self, mock_search):
        """multi_match 쿼리를 사용해야 한다."""
        mock_search.return_value = _make_es_result([])
        client = MagicMock()

        search_thinker_by_name(client, "칸트")

        mock_search.assert_called_once()
        args = mock_search.call_args
        assert args[0][1] == INDEX_THINKERS
        query = args[0][2]
        assert "multi_match" in query
        assert query["multi_match"]["query"] == "칸트"
        assert "name" in query["multi_match"]["fields"]

    @patch("src.search.search_documents")
    def test_returns_sources(self, mock_search):
        """_source 리스트를 반환해야 한다."""
        mock_search.return_value = _make_es_result(
            [
                {"id": "kant", "name": "칸트"},
            ]
        )
        client = MagicMock()

        result = search_thinker_by_name(client, "칸트")
        assert len(result) == 1
        assert result[0]["id"] == "kant"


class TestGetThinkerFull:
    """get_thinker_full 테스트."""

    @patch("src.search.search_documents")
    def test_multi_index_query(self, mock_search):
        """여러 인덱스를 조회해야 한다."""
        mock_search.return_value = _make_es_result([])
        client = MagicMock()

        get_thinker_full(client, "kant")

        # thinker, works, claims, keywords, relations(from + to) = 6 calls
        assert mock_search.call_count == 6
        called_indices = [c[0][1] for c in mock_search.call_args_list]
        assert INDEX_THINKERS in called_indices
        assert INDEX_WORKS in called_indices
        assert INDEX_CLAIMS in called_indices
        assert INDEX_KEYWORDS in called_indices
        assert INDEX_RELATIONS in called_indices

    @patch("src.search.search_documents")
    def test_returns_structured_result(self, mock_search):
        """구조화된 결과를 반환해야 한다."""
        thinker_data = {"id": "kant", "name": "칸트"}
        work_data = {"id": "w1", "thinker_id": "kant"}

        def side_effect(client, index, query, size=10):
            if index == INDEX_THINKERS:
                return _make_es_result([thinker_data])
            if index == INDEX_WORKS:
                return _make_es_result([work_data])
            return _make_es_result([])

        mock_search.side_effect = side_effect
        client = MagicMock()

        result = get_thinker_full(client, "kant")

        assert result["thinker"] == thinker_data
        assert len(result["works"]) == 1
        assert "claims" in result
        assert "keywords" in result
        assert "relations" in result

    @patch("src.search.search_documents")
    def test_deduplicates_relations(self, mock_search):
        """중복 관계를 제거해야 한다."""
        rel = {"id": "r1", "from_thinker": "kant", "to_thinker": "plato"}

        call_count = [0]

        def side_effect(client, index, query, size=10):
            if index == INDEX_RELATIONS:
                # from과 to 모두 같은 relation을 반환
                return _make_es_result([rel])
            if index == INDEX_THINKERS:
                return _make_es_result([{"id": "kant"}])
            return _make_es_result([])

        mock_search.side_effect = side_effect
        client = MagicMock()

        result = get_thinker_full(client, "kant")
        # 중복 제거로 1개만 있어야 한다
        assert len(result["relations"]) == 1

    @patch("src.search.search_documents")
    def test_no_thinker_found(self, mock_search):
        """사상가를 찾지 못하면 thinker가 None이어야 한다."""
        mock_search.return_value = _make_es_result([])
        client = MagicMock()

        result = get_thinker_full(client, "nonexistent")
        assert result["thinker"] is None


class TestSearchByKeyword:
    """search_by_keyword 테스트."""

    @patch("src.search.search_documents")
    def test_multi_index_search(self, mock_search):
        """thinkers, claims, keywords 인덱스를 모두 검색해야 한다."""
        mock_search.return_value = _make_es_result([])
        client = MagicMock()

        search_by_keyword(client, "덕")

        assert mock_search.call_count == 3
        called_indices = [c[0][1] for c in mock_search.call_args_list]
        assert INDEX_THINKERS in called_indices
        assert INDEX_CLAIMS in called_indices
        assert INDEX_KEYWORDS in called_indices

    @patch("src.search.search_documents")
    def test_returns_categorized_results(self, mock_search):
        """카테고리별 결과를 반환해야 한다."""

        def side_effect(client, index, query, size=10):
            if index == INDEX_THINKERS:
                return _make_es_result([{"id": "t1", "name": "공자"}])
            if index == INDEX_CLAIMS:
                return _make_es_result([{"id": "c1", "claim": "덕이란..."}])
            if index == INDEX_KEYWORDS:
                return _make_es_result([{"id": "k1", "term": "덕"}])
            return _make_es_result([])

        mock_search.side_effect = side_effect
        client = MagicMock()

        result = search_by_keyword(client, "덕")

        assert len(result["thinkers"]) == 1
        assert len(result["claims"]) == 1
        assert len(result["keywords"]) == 1

    @patch("src.search.search_documents")
    def test_uses_bool_should_queries(self, mock_search):
        """bool.should 쿼리를 사용해야 한다."""
        mock_search.return_value = _make_es_result([])
        client = MagicMock()

        search_by_keyword(client, "test")

        for c in mock_search.call_args_list:
            query = c[0][2]
            assert "bool" in query
            assert "should" in query["bool"]


class TestGetRelations:
    """get_relations 테스트."""

    @patch("src.search.search_documents")
    def test_returns_outgoing_and_incoming(self, mock_search):
        """outgoing과 incoming을 분리해서 반환해야 한다."""
        outgoing = {"id": "r1", "from_thinker": "kant", "to_thinker": "plato"}
        incoming = {"id": "r2", "from_thinker": "hegel", "to_thinker": "kant"}

        def side_effect(client, index, query, size=10):
            if "from_thinker" in str(query):
                return _make_es_result([outgoing])
            return _make_es_result([incoming])

        mock_search.side_effect = side_effect
        client = MagicMock()

        result = get_relations(client, "kant")

        assert len(result["outgoing"]) == 1
        assert len(result["incoming"]) == 1
        assert result["outgoing"][0]["id"] == "r1"
        assert result["incoming"][0]["id"] == "r2"


class TestGetUnverifiedClaims:
    """get_unverified_claims 테스트."""

    @patch("src.search.search_documents")
    def test_query_structure(self, mock_search):
        """verified: false 조건으로 검색해야 한다."""
        mock_search.return_value = _make_es_result([])
        client = MagicMock()

        get_unverified_claims(client)

        query = mock_search.call_args[0][2]
        assert "term" in query
        assert query["term"]["verified"] is False

    @patch("src.search.search_documents")
    def test_searches_claims_index(self, mock_search):
        """claims 인덱스에서 검색해야 한다."""
        mock_search.return_value = _make_es_result([])
        client = MagicMock()

        get_unverified_claims(client)

        assert mock_search.call_args[0][1] == INDEX_CLAIMS

    @patch("src.search.search_documents")
    def test_large_size_limit(self, mock_search):
        """size=1000으로 요청해야 한다."""
        mock_search.return_value = _make_es_result([])
        client = MagicMock()

        get_unverified_claims(client)

        assert mock_search.call_args[1]["size"] == 1000


class TestSearchByField:
    """search_by_field 테스트."""

    @patch("src.search.search_documents")
    def test_searches_thinkers_by_field(self, mock_search):
        """field로 사상가를 검색해야 한다."""
        mock_search.return_value = _make_es_result(
            [
                {"id": "kant", "field": "western"},
            ]
        )
        client = MagicMock()

        result = search_by_field(client, "western")

        assert mock_search.call_args[0][1] == INDEX_THINKERS
        query = mock_search.call_args[0][2]
        assert query["term"]["field"] == "western"
        assert len(result) == 1
