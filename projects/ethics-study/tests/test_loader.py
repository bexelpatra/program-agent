"""test_loader.py -- loader.py 단위 테스트."""

import os
from unittest.mock import MagicMock, patch, call

import pytest
import yaml

from src.config import (
    INDEX_CLAIMS,
    INDEX_FIELDS,
    INDEX_KEYWORDS,
    INDEX_RELATIONS,
    INDEX_THINKERS,
    INDEX_WORKS,
)
from src.loader import load_yaml_file, load_thinker_to_es, load_fields_to_es, load_all


class TestLoadYamlFile:
    """load_yaml_file 테스트."""

    def test_load_valid_yaml(self, tmp_path):
        """유효한 YAML 파일을 정상적으로 파싱해야 한다."""
        yaml_content = {
            "thinker": {"id": "kant", "name": "칸트"},
            "works": [{"id": "kant-critique", "title": "순수이성비판"}],
        }
        filepath = tmp_path / "test.yaml"
        filepath.write_text(
            yaml.dump(yaml_content, allow_unicode=True), encoding="utf-8"
        )

        result = load_yaml_file(str(filepath))
        assert result["thinker"]["id"] == "kant"
        assert len(result["works"]) == 1

    def test_load_empty_yaml(self, tmp_path):
        """빈 YAML은 None을 반환해야 한다."""
        filepath = tmp_path / "empty.yaml"
        filepath.write_text("", encoding="utf-8")

        result = load_yaml_file(str(filepath))
        assert result is None

    def test_load_nonexistent_file(self):
        """존재하지 않는 파일은 FileNotFoundError를 발생시켜야 한다."""
        with pytest.raises(FileNotFoundError):
            load_yaml_file("/nonexistent/path.yaml")


class TestLoadThinkerToEs:
    """load_thinker_to_es 테스트."""

    @patch("src.loader.bulk_insert")
    @patch("src.loader.index_document")
    def test_loads_thinker(
        self,
        mock_index,
        mock_bulk,
    ):
        """사상가 데이터를 인덱싱해야 한다."""
        client = MagicMock()
        data = {
            "thinker": {"id": "kant", "name": "칸트"},
        }

        result = load_thinker_to_es(client, data)

        mock_index.assert_called_once_with(
            client, INDEX_THINKERS, data["thinker"], doc_id="kant"
        )
        assert result["thinkers"] == 1

    @patch("src.loader.bulk_insert")
    @patch("src.loader.index_document")
    def test_auto_fills_thinker_id_in_claims(self, mock_index, mock_bulk):
        """claims에 thinker_id가 없으면 자동으로 채워야 한다."""
        client = MagicMock()
        data = {
            "thinker": {"id": "kant", "name": "칸트"},
            "claims": [
                {"id": "claim-1", "claim": "도덕법칙은 보편적이다"},
            ],
        }
        mock_bulk.return_value = (1, [])

        load_thinker_to_es(client, data)

        # claims에 thinker_id가 추가되었는지 확인
        assert data["claims"][0]["thinker_id"] == "kant"

    @patch("src.loader.bulk_insert")
    @patch("src.loader.index_document")
    def test_auto_fills_thinker_id_in_works(self, mock_index, mock_bulk):
        """works에 thinker_id가 없으면 자동으로 채워야 한다."""
        client = MagicMock()
        data = {
            "thinker": {"id": "kant", "name": "칸트"},
            "works": [{"id": "w1", "title": "순수이성비판"}],
        }
        mock_bulk.return_value = (1, [])

        load_thinker_to_es(client, data)
        assert data["works"][0]["thinker_id"] == "kant"

    @patch("src.loader.bulk_insert")
    @patch("src.loader.index_document")
    def test_auto_fills_thinker_id_in_keywords(self, mock_index, mock_bulk):
        """keywords에 thinker_id가 없으면 자동으로 채워야 한다."""
        client = MagicMock()
        data = {
            "thinker": {"id": "kant", "name": "칸트"},
            "keywords": [{"id": "kw1", "term": "정언명령"}],
        }
        mock_bulk.return_value = (1, [])

        load_thinker_to_es(client, data)
        assert data["keywords"][0]["thinker_id"] == "kant"

    @patch("src.loader.bulk_insert")
    @patch("src.loader.index_document")
    def test_preserves_existing_thinker_id(self, mock_index, mock_bulk):
        """이미 thinker_id가 있으면 덮어쓰지 않아야 한다."""
        client = MagicMock()
        data = {
            "thinker": {"id": "kant", "name": "칸트"},
            "claims": [
                {"id": "c1", "claim": "test", "thinker_id": "other"},
            ],
        }
        mock_bulk.return_value = (1, [])

        load_thinker_to_es(client, data)
        assert data["claims"][0]["thinker_id"] == "other"

    @patch("src.loader.bulk_insert")
    @patch("src.loader.index_document")
    def test_loads_all_sections(self, mock_index, mock_bulk):
        """모든 섹션을 적재하고 카운트를 반환해야 한다."""
        client = MagicMock()
        data = {
            "thinker": {"id": "kant", "name": "칸트"},
            "works": [{"id": "w1"}, {"id": "w2"}],
            "claims": [{"id": "c1"}],
            "keywords": [{"id": "k1"}, {"id": "k2"}, {"id": "k3"}],
            "relations": [{"id": "r1"}],
        }
        mock_bulk.return_value = (0, [])

        result = load_thinker_to_es(client, data)

        assert result["thinkers"] == 1
        assert result["works"] == 2
        assert result["claims"] == 1
        assert result["keywords"] == 3
        assert result["relations"] == 1

    @patch("src.loader.bulk_insert")
    @patch("src.loader.index_document")
    def test_bulk_called_with_correct_indices(self, mock_index, mock_bulk):
        """각 섹션이 올바른 인덱스에 적재되어야 한다."""
        client = MagicMock()
        data = {
            "thinker": {"id": "kant", "name": "칸트"},
            "works": [{"id": "w1"}],
            "claims": [{"id": "c1"}],
            "keywords": [{"id": "k1"}],
            "relations": [{"id": "r1"}],
        }
        mock_bulk.return_value = (0, [])

        load_thinker_to_es(client, data)

        bulk_calls = mock_bulk.call_args_list
        called_indices = [c[0][1] for c in bulk_calls]
        assert INDEX_WORKS in called_indices
        assert INDEX_CLAIMS in called_indices
        assert INDEX_KEYWORDS in called_indices
        assert INDEX_RELATIONS in called_indices

    @patch("src.loader.bulk_insert")
    @patch("src.loader.index_document")
    def test_no_thinker_section(self, mock_index, mock_bulk):
        """thinker 섹션이 없으면 thinker_id 자동 채움을 하지 않아야 한다."""
        client = MagicMock()
        data = {
            "claims": [{"id": "c1", "claim": "test"}],
        }
        mock_bulk.return_value = (1, [])

        result = load_thinker_to_es(client, data)

        mock_index.assert_not_called()
        assert result["thinkers"] == 0
        assert "thinker_id" not in data["claims"][0]


class TestLoadFieldsToEs:
    """load_fields_to_es 테스트."""

    @patch("src.loader.bulk_insert")
    @patch("src.loader.load_yaml_file")
    def test_loads_fields(self, mock_load_yaml, mock_bulk):
        """fields 데이터를 적재해야 한다."""
        client = MagicMock()
        mock_load_yaml.return_value = {
            "fields": [
                {"id": "western", "name": "서양윤리"},
                {"id": "eastern", "name": "동양윤리"},
            ]
        }
        mock_bulk.return_value = (2, [])

        count = load_fields_to_es(client, "fields.yaml")

        assert count == 2
        mock_bulk.assert_called_once_with(
            client, INDEX_FIELDS, mock_load_yaml.return_value["fields"], id_field="id"
        )

    @patch("src.loader.bulk_insert")
    @patch("src.loader.load_yaml_file")
    def test_empty_fields(self, mock_load_yaml, mock_bulk):
        """fields가 비어있으면 0을 반환해야 한다."""
        client = MagicMock()
        mock_load_yaml.return_value = {"fields": []}

        count = load_fields_to_es(client, "fields.yaml")
        assert count == 0
        mock_bulk.assert_not_called()


class TestLoadAll:
    """load_all 테스트."""

    @patch("src.loader.load_thinker_to_es")
    @patch("src.loader.load_fields_to_es")
    @patch("src.loader.load_yaml_file")
    def test_traverses_directories(
        self, mock_load_yaml, mock_load_fields, mock_load_thinker, tmp_path
    ):
        """하위 디렉토리를 순회하며 YAML을 적재해야 한다."""
        # 디렉토리 구조 생성
        fields_file = tmp_path / "fields.yaml"
        fields_file.write_text(
            yaml.dump({"fields": [{"id": "f1"}]}, allow_unicode=True)
        )

        western = tmp_path / "western"
        western.mkdir()
        (western / "kant.yaml").write_text(yaml.dump({"thinker": {"id": "kant"}}))
        (western / "mill.yaml").write_text(yaml.dump({"thinker": {"id": "mill"}}))

        # 비-YAML 파일은 무시되어야 한다
        (western / "readme.txt").write_text("ignore me")

        mock_load_fields.return_value = 1
        mock_load_yaml.return_value = {"thinker": {"id": "test"}}
        mock_load_thinker.return_value = {
            "thinkers": 1,
            "works": 0,
            "claims": 0,
            "keywords": 0,
            "relations": 0,
        }

        client = MagicMock()
        totals = load_all(client, str(tmp_path))

        # fields 적재 확인
        mock_load_fields.assert_called_once()
        # 사상가 YAML 2개 적재 확인
        assert mock_load_thinker.call_count == 2
        assert totals["fields"] == 1
        assert totals["thinkers"] == 2

    @patch("src.loader.load_thinker_to_es")
    @patch("src.loader.load_fields_to_es")
    @patch("src.loader.load_yaml_file")
    def test_no_fields_yaml(
        self, mock_load_yaml, mock_load_fields, mock_load_thinker, tmp_path
    ):
        """fields.yaml이 없어도 정상 동작해야 한다."""
        subdir = tmp_path / "eastern"
        subdir.mkdir()
        (subdir / "confucius.yaml").write_text(
            yaml.dump({"thinker": {"id": "confucius"}})
        )

        mock_load_yaml.return_value = {"thinker": {"id": "confucius"}}
        mock_load_thinker.return_value = {
            "thinkers": 1,
            "works": 0,
            "claims": 0,
            "keywords": 0,
            "relations": 0,
        }

        client = MagicMock()
        totals = load_all(client, str(tmp_path))

        mock_load_fields.assert_not_called()
        assert totals["fields"] == 0

    @patch("src.loader.load_thinker_to_es")
    @patch("src.loader.load_fields_to_es")
    @patch("src.loader.load_yaml_file")
    def test_handles_yml_extension(
        self, mock_load_yaml, mock_load_fields, mock_load_thinker, tmp_path
    ):
        """*.yml 확장자도 처리해야 한다."""
        subdir = tmp_path / "test"
        subdir.mkdir()
        (subdir / "thinker.yml").write_text(yaml.dump({"thinker": {"id": "t1"}}))

        mock_load_yaml.return_value = {"thinker": {"id": "t1"}}
        mock_load_thinker.return_value = {
            "thinkers": 1,
            "works": 0,
            "claims": 0,
            "keywords": 0,
            "relations": 0,
        }

        client = MagicMock()
        totals = load_all(client, str(tmp_path))

        assert mock_load_thinker.call_count == 1
