"""test_models.py -- models.py 단위 테스트."""

from unittest.mock import MagicMock, patch, call

import pytest

from src.config import (
    INDEX_CLAIMS,
    INDEX_FIELDS,
    INDEX_KEYWORDS,
    INDEX_RELATIONS,
    INDEX_THINKERS,
    INDEX_WORKS,
    ALL_INDICES,
)
from src.models import (
    CLAIMS_MAPPINGS,
    FIELDS_MAPPINGS,
    KEYWORDS_MAPPINGS,
    RELATIONS_MAPPINGS,
    THINKERS_MAPPINGS,
    WORKS_MAPPINGS,
    get_all_mappings,
    init_all_indices,
)


class TestGetAllMappings:
    """get_all_mappings 테스트."""

    def test_returns_six_indices(self):
        """6개 인덱스 매핑을 반환해야 한다."""
        mappings = get_all_mappings()
        assert len(mappings) == 6

    def test_all_index_names_present(self):
        """모든 인덱스 이름이 키로 포함되어야 한다."""
        mappings = get_all_mappings()
        expected = {
            INDEX_THINKERS,
            INDEX_WORKS,
            INDEX_CLAIMS,
            INDEX_KEYWORDS,
            INDEX_RELATIONS,
            INDEX_FIELDS,
        }
        assert set(mappings.keys()) == expected

    def test_each_mapping_has_properties(self):
        """각 매핑에 properties가 포함되어야 한다."""
        mappings = get_all_mappings()
        for index_name, mapping in mappings.items():
            assert "properties" in mapping, f"{index_name} mapping missing 'properties'"


class TestMappingFieldTypes:
    """각 매핑의 필드 타입 검증."""

    def test_thinkers_field_types(self):
        props = THINKERS_MAPPINGS["properties"]
        assert props["id"]["type"] == "keyword"
        assert props["name"]["type"] == "text"
        assert props["field"]["type"] == "keyword"
        assert props["era"]["type"] == "keyword"
        assert props["birth_year"]["type"] == "integer"
        assert props["death_year"]["type"] == "integer"
        assert props["background"]["type"] == "text"
        assert props["core_philosophy"]["type"] == "text"
        assert props["keywords"]["type"] == "keyword"

    def test_works_field_types(self):
        props = WORKS_MAPPINGS["properties"]
        assert props["id"]["type"] == "keyword"
        assert props["thinker_id"]["type"] == "keyword"
        assert props["title"]["type"] == "text"
        assert props["year"]["type"] == "integer"
        assert props["significance"]["type"] == "text"
        assert props["key_concepts"]["type"] == "keyword"

    def test_claims_field_types(self):
        props = CLAIMS_MAPPINGS["properties"]
        assert props["id"]["type"] == "keyword"
        assert props["thinker_id"]["type"] == "keyword"
        assert props["claim"]["type"] == "text"
        assert props["verified"]["type"] == "boolean"
        assert props["verification_log"]["type"] == "nested"

    def test_keywords_field_types(self):
        props = KEYWORDS_MAPPINGS["properties"]
        assert props["id"]["type"] == "keyword"
        assert props["term"]["type"] == "text"
        assert props["definition"]["type"] == "text"
        assert props["related_terms"]["type"] == "keyword"

    def test_relations_field_types(self):
        props = RELATIONS_MAPPINGS["properties"]
        assert props["from_thinker"]["type"] == "keyword"
        assert props["to_thinker"]["type"] == "keyword"
        assert props["type"]["type"] == "keyword"
        assert props["description"]["type"] == "text"

    def test_fields_field_types(self):
        props = FIELDS_MAPPINGS["properties"]
        assert props["id"]["type"] == "keyword"
        assert props["name"]["type"] == "text"
        assert props["description"]["type"] == "text"
        assert props["order"]["type"] == "integer"

    def test_text_with_keyword_subfield(self):
        """text + keyword 서브필드가 있는 필드를 검증한다."""
        # thinkers.name 은 text_with_keyword
        name_field = THINKERS_MAPPINGS["properties"]["name"]
        assert name_field["type"] == "text"
        assert "fields" in name_field
        assert "keyword" in name_field["fields"]
        assert name_field["fields"]["keyword"]["type"] == "keyword"


class TestInitAllIndices:
    """init_all_indices 테스트."""

    @patch("src.models.create_index")
    def test_calls_create_index_six_times(self, mock_create):
        """create_index가 6번 호출되어야 한다."""
        mock_client = MagicMock()
        init_all_indices(mock_client)
        assert mock_create.call_count == 6

    @patch("src.models.create_index")
    def test_passes_correct_index_names(self, mock_create):
        """올바른 인덱스 이름이 전달되어야 한다."""
        mock_client = MagicMock()
        init_all_indices(mock_client)

        called_indices = {c[1]["index"] for c in mock_create.call_args_list}
        expected = {
            INDEX_THINKERS,
            INDEX_WORKS,
            INDEX_CLAIMS,
            INDEX_KEYWORDS,
            INDEX_RELATIONS,
            INDEX_FIELDS,
        }
        assert called_indices == expected

    @patch("src.models.create_index")
    def test_passes_mappings_and_settings(self, mock_create):
        """각 호출에 mappings와 settings가 전달되어야 한다."""
        mock_client = MagicMock()
        init_all_indices(mock_client)

        for c in mock_create.call_args_list:
            assert "mappings" in c[1]
            assert "settings" in c[1]
            assert c[1]["mappings"] is not None
            assert c[1]["settings"] is not None
