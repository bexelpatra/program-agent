"""test_es_client.py -- es_client.py 단위 테스트 (mock 사용)."""

from unittest.mock import MagicMock, patch

import pytest

from src.es_client import (
    bulk_insert,
    create_index,
    delete_index,
    get_client,
    get_document,
    index_document,
    index_exists,
    search_documents,
    delete_document,
)


@pytest.fixture
def mock_client():
    """Mock Elasticsearch 클라이언트를 반환한다."""
    client = MagicMock()
    client.indices = MagicMock()
    return client


class TestGetClient:
    """get_client 테스트."""

    @patch("src.es_client.Elasticsearch")
    def test_get_client_returns_es_instance(self, mock_es_cls):
        """Elasticsearch 인스턴스를 반환해야 한다."""
        result = get_client()
        mock_es_cls.assert_called_once()
        assert result == mock_es_cls.return_value


class TestIndexExists:
    """index_exists 테스트."""

    def test_index_exists_true(self, mock_client):
        mock_client.indices.exists.return_value = True
        assert index_exists(mock_client, "test-index") is True
        mock_client.indices.exists.assert_called_once_with(index="test-index")

    def test_index_exists_false(self, mock_client):
        mock_client.indices.exists.return_value = False
        assert index_exists(mock_client, "test-index") is False


class TestCreateIndex:
    """create_index 테스트."""

    def test_create_index_new(self, mock_client):
        """새 인덱스 생성 시 indices.create가 호출되어야 한다."""
        mock_client.indices.exists.return_value = False
        mock_client.indices.create.return_value = {"acknowledged": True}

        result = create_index(
            mock_client,
            "test-index",
            mappings={"properties": {"name": {"type": "text"}}},
            settings={"number_of_shards": 1},
        )

        mock_client.indices.create.assert_called_once()
        call_kwargs = mock_client.indices.create.call_args
        assert call_kwargs[1]["index"] == "test-index"
        assert "mappings" in call_kwargs[1]["body"]
        assert "settings" in call_kwargs[1]["body"]

    def test_create_index_already_exists(self, mock_client):
        """이미 존재하는 인덱스는 스킵해야 한다."""
        mock_client.indices.exists.return_value = True

        result = create_index(mock_client, "test-index")

        mock_client.indices.create.assert_not_called()
        assert result["acknowledged"] is True
        assert result["already_exists"] is True

    def test_create_index_no_mappings_no_settings(self, mock_client):
        """mappings/settings 없이도 생성 가능해야 한다."""
        mock_client.indices.exists.return_value = False
        mock_client.indices.create.return_value = {"acknowledged": True}

        create_index(mock_client, "test-index")

        call_kwargs = mock_client.indices.create.call_args
        body = call_kwargs[1]["body"]
        assert "mappings" not in body
        assert "settings" not in body


class TestDeleteIndex:
    """delete_index 테스트."""

    def test_delete_existing_index(self, mock_client):
        mock_client.indices.exists.return_value = True
        mock_client.indices.delete.return_value = {"acknowledged": True}

        result = delete_index(mock_client, "test-index")
        mock_client.indices.delete.assert_called_once_with(index="test-index")

    def test_delete_nonexistent_index(self, mock_client):
        mock_client.indices.exists.return_value = False

        result = delete_index(mock_client, "test-index")
        mock_client.indices.delete.assert_not_called()
        assert result["not_found"] is True


class TestIndexDocument:
    """index_document 테스트."""

    def test_index_document_with_id(self, mock_client):
        """doc_id가 있으면 id 파라미터와 함께 호출해야 한다."""
        doc = {"name": "test"}
        mock_client.index.return_value = {"result": "created"}

        index_document(mock_client, "test-index", doc, doc_id="doc-1")
        mock_client.index.assert_called_once_with(
            index="test-index", body=doc, id="doc-1"
        )

    def test_index_document_without_id(self, mock_client):
        """doc_id가 없으면 id 파라미터 없이 호출해야 한다."""
        doc = {"name": "test"}
        mock_client.index.return_value = {"result": "created"}

        index_document(mock_client, "test-index", doc)
        mock_client.index.assert_called_once_with(index="test-index", body=doc)


class TestSearchDocuments:
    """search_documents 테스트."""

    def test_search_documents_passes_query(self, mock_client):
        """쿼리와 size를 올바르게 전달해야 한다."""
        query = {"match": {"name": "test"}}
        mock_client.search.return_value = {"hits": {"hits": []}}

        search_documents(mock_client, "test-index", query, size=5)
        mock_client.search.assert_called_once_with(
            index="test-index",
            body={"query": query, "size": 5},
        )

    def test_search_documents_default_size(self, mock_client):
        """기본 size가 10이어야 한다."""
        query = {"match_all": {}}
        mock_client.search.return_value = {"hits": {"hits": []}}

        search_documents(mock_client, "test-index", query)
        call_body = mock_client.search.call_args[1]["body"]
        assert call_body["size"] == 10


class TestBulkInsert:
    """bulk_insert 테스트."""

    @patch("src.es_client.helpers")
    def test_bulk_insert_with_id_field(self, mock_helpers, mock_client):
        """id_field가 있으면 _id를 설정해야 한다."""
        docs = [
            {"id": "doc-1", "name": "a"},
            {"id": "doc-2", "name": "b"},
        ]
        mock_helpers.bulk.return_value = (2, [])

        bulk_insert(mock_client, "test-index", docs, id_field="id")

        actions = mock_helpers.bulk.call_args[0][1]
        assert len(actions) == 2
        assert actions[0]["_id"] == "doc-1"
        assert actions[0]["_index"] == "test-index"
        assert actions[0]["_source"] == docs[0]

    @patch("src.es_client.helpers")
    def test_bulk_insert_without_id_field(self, mock_helpers, mock_client):
        """id_field가 None이면 _id를 설정하지 않아야 한다."""
        docs = [{"name": "a"}, {"name": "b"}]
        mock_helpers.bulk.return_value = (2, [])

        bulk_insert(mock_client, "test-index", docs, id_field=None)

        actions = mock_helpers.bulk.call_args[0][1]
        for action in actions:
            assert "_id" not in action

    @patch("src.es_client.helpers")
    def test_bulk_insert_missing_id_field_in_doc(self, mock_helpers, mock_client):
        """문서에 id_field가 없으면 _id를 설정하지 않아야 한다."""
        docs = [{"name": "a"}]  # 'id' 필드 없음
        mock_helpers.bulk.return_value = (1, [])

        bulk_insert(mock_client, "test-index", docs, id_field="id")

        actions = mock_helpers.bulk.call_args[0][1]
        assert "_id" not in actions[0]


class TestGetDocument:
    """get_document 테스트."""

    def test_get_document(self, mock_client):
        mock_client.get.return_value = {"_source": {"name": "test"}}
        result = get_document(mock_client, "test-index", "doc-1")
        mock_client.get.assert_called_once_with(index="test-index", id="doc-1")


class TestDeleteDocument:
    """delete_document 테스트."""

    def test_delete_document(self, mock_client):
        mock_client.delete.return_value = {"result": "deleted"}
        result = delete_document(mock_client, "test-index", "doc-1")
        mock_client.delete.assert_called_once_with(index="test-index", id="doc-1")
