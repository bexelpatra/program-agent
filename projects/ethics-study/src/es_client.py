"""Elasticsearch 클라이언트 모듈 — 연결, 인덱스 관리, 문서 CRUD."""

from typing import Any, Dict, List, Optional

from elasticsearch import Elasticsearch, helpers

from src.config import ES_URL


def get_client() -> Elasticsearch:
    """ES 클라이언트 인스턴스를 반환한다."""
    return Elasticsearch(ES_URL)


def close_client(client: Elasticsearch) -> None:
    """ES 클라이언트 연결을 종료한다."""
    client.close()


# ── 인덱스 관리 ──────────────────────────────────────────────


def index_exists(client: Elasticsearch, index: str) -> bool:
    """인덱스 존재 여부를 확인한다."""
    return client.indices.exists(index=index)


def create_index(
    client: Elasticsearch,
    index: str,
    mappings: Optional[Dict[str, Any]] = None,
    settings: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """인덱스를 생성한다. 이미 존재하면 무시한다."""
    if index_exists(client, index):
        return {"acknowledged": True, "already_exists": True}

    body: Dict[str, Any] = {}
    if settings:
        body["settings"] = settings
    if mappings:
        body["mappings"] = mappings

    return client.indices.create(index=index, body=body)


def delete_index(client: Elasticsearch, index: str) -> Dict[str, Any]:
    """인덱스를 삭제한다. 존재하지 않으면 무시한다."""
    if not index_exists(client, index):
        return {"acknowledged": True, "not_found": True}
    return client.indices.delete(index=index)


# ── 문서 CRUD ────────────────────────────────────────────────


def index_document(
    client: Elasticsearch,
    index: str,
    doc: Dict[str, Any],
    doc_id: Optional[str] = None,
) -> Dict[str, Any]:
    """문서를 인덱싱(생성/업데이트)한다."""
    kwargs: Dict[str, Any] = {"index": index, "body": doc}
    if doc_id:
        kwargs["id"] = doc_id
    return client.index(**kwargs)


def get_document(
    client: Elasticsearch,
    index: str,
    doc_id: str,
) -> Dict[str, Any]:
    """ID로 문서를 조회한다."""
    return client.get(index=index, id=doc_id)


def search_documents(
    client: Elasticsearch,
    index: str,
    query: Dict[str, Any],
    size: int = 10,
) -> Dict[str, Any]:
    """쿼리로 문서를 검색한다."""
    return client.search(index=index, body={"query": query, "size": size})


def delete_document(
    client: Elasticsearch,
    index: str,
    doc_id: str,
) -> Dict[str, Any]:
    """ID로 문서를 삭제한다."""
    return client.delete(index=index, id=doc_id)


def bulk_insert(
    client: Elasticsearch,
    index: str,
    docs: List[Dict[str, Any]],
    id_field: Optional[str] = "id",
) -> tuple:
    """여러 문서를 bulk로 인덱싱한다.

    Args:
        client: ES 클라이언트
        index: 대상 인덱스
        docs: 문서 리스트
        id_field: 문서 내 ID로 사용할 필드명. None이면 자동 생성.

    Returns:
        (성공 건수, 에러 리스트) 튜플
    """
    actions = []
    for doc in docs:
        action = {
            "_index": index,
            "_source": doc,
        }
        if id_field and id_field in doc:
            action["_id"] = doc[id_field]
        actions.append(action)

    return helpers.bulk(client, actions)
