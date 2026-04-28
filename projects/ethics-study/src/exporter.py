"""ES → YAML 익스포터 — Elasticsearch에서 사상가 데이터를 YAML 파일로 export한다."""

import os
from typing import Any, Dict, List, Optional

import yaml
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


def _get_thinker_data(
    client: Elasticsearch, thinker_id: str
) -> Optional[Dict[str, Any]]:
    """특정 사상가의 모든 데이터를 ES에서 조회하여 딕셔너리로 반환한다.

    Returns:
        {
            'thinker': {...},
            'works': [...],
            'claims': [...],
            'keywords': [...],
            'relations': [...]
        }
        사상가를 찾지 못하면 None 반환.
    """
    # thinker
    thinker_result = search_documents(
        client, INDEX_THINKERS, {"term": {"id": thinker_id}}, size=1
    )
    thinkers = _hits(thinker_result)
    if not thinkers:
        return None
    thinker = thinkers[0]

    # works
    works_result = search_documents(
        client, INDEX_WORKS, {"term": {"thinker_id": thinker_id}}, size=200
    )
    works = _hits(works_result)

    # claims
    claims_result = search_documents(
        client, INDEX_CLAIMS, {"term": {"thinker_id": thinker_id}}, size=500
    )
    claims = _hits(claims_result)

    # keywords
    kw_result = search_documents(
        client, INDEX_KEYWORDS, {"term": {"thinker_id": thinker_id}}, size=200
    )
    keywords = _hits(kw_result)

    # relations (from or to)
    from_result = search_documents(
        client, INDEX_RELATIONS, {"term": {"from_thinker": thinker_id}}, size=200
    )
    to_result = search_documents(
        client, INDEX_RELATIONS, {"term": {"to_thinker": thinker_id}}, size=200
    )
    all_relations = _hits(from_result) + _hits(to_result)

    # 중복 제거 (id 기준, id 없으면 object id)
    seen_ids = set()
    unique_relations = []
    for rel in all_relations:
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


def _get_all_thinker_ids(client: Elasticsearch) -> List[str]:
    """ES에서 모든 사상가 ID 목록을 반환한다."""
    result = search_documents(
        client,
        INDEX_THINKERS,
        {"match_all": {}},
        size=1000,
    )
    return [hit["_source"]["id"] for hit in result["hits"]["hits"]]


def _build_yaml_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """ES에서 조회한 데이터를 YAML 출력 형식으로 변환한다.

    loader.py가 다시 로드할 수 있는 형식(socrates.yaml과 동일 구조)으로 구성한다.
    claims의 argument, counterpoint 필드는 ES에 저장된 값 그대로 포함된다.
    """
    yaml_data: Dict[str, Any] = {}

    thinker = data.get("thinker")
    if thinker:
        yaml_data["thinker"] = thinker

    works = data.get("works", [])
    if works:
        # year 기준 정렬
        yaml_data["works"] = sorted(works, key=lambda w: w.get("year") or 0)

    claims = data.get("claims", [])
    if claims:
        # id 기준 정렬
        yaml_data["claims"] = sorted(claims, key=lambda c: c.get("id", ""))

    keywords = data.get("keywords", [])
    if keywords:
        yaml_data["keywords"] = sorted(keywords, key=lambda k: k.get("id", ""))

    relations = data.get("relations", [])
    if relations:
        yaml_data["relations"] = sorted(relations, key=lambda r: r.get("id", ""))

    return yaml_data


def _get_output_path(data_dir: str, thinker: Dict[str, Any]) -> str:
    """사상가 데이터를 바탕으로 출력 파일 경로를 결정한다.

    출력 경로: {data_dir}/{field}/{thinker_id}.yaml
    field 매핑 예시: western_ethics -> western, eastern_ethics -> eastern
    """
    thinker_id = thinker.get("id", "unknown")
    field = thinker.get("field", "unknown")

    # field 이름에서 디렉토리 이름 결정
    # 예: western_ethics -> western, eastern_ethics -> eastern
    # 첫 번째 단어(언더스코어 전)를 디렉토리명으로 사용
    field_dir = field.split("_")[0] if "_" in field else field

    return os.path.join(data_dir, field_dir, f"{thinker_id}.yaml")


def export_thinker(
    client: Elasticsearch,
    thinker_id: str,
    data_dir: str = "data",
) -> Optional[str]:
    """특정 사상가의 데이터를 ES에서 조회하여 YAML 파일로 export한다.

    Args:
        client: ES 클라이언트
        thinker_id: export할 사상가 ID
        data_dir: 출력 디렉토리 (기본값: "data")

    Returns:
        export된 파일 경로. 사상가를 찾지 못하면 None 반환.
    """
    data = _get_thinker_data(client, thinker_id)
    if data is None:
        return None

    thinker = data["thinker"]
    yaml_data = _build_yaml_data(data)

    output_path = _get_output_path(data_dir, thinker)

    # 출력 디렉토리 생성
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(
            yaml_data,
            f,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
        )

    return output_path


def export_all_thinkers(
    client: Elasticsearch,
    data_dir: str = "data",
) -> Dict[str, str]:
    """ES에 등록된 모든 사상가를 YAML로 export한다.

    Args:
        client: ES 클라이언트
        data_dir: 출력 디렉토리 (기본값: "data")

    Returns:
        {thinker_id: output_path} 딕셔너리 (성공한 것만 포함)
    """
    thinker_ids = _get_all_thinker_ids(client)
    results: Dict[str, str] = {}

    for thinker_id in thinker_ids:
        path = export_thinker(client, thinker_id, data_dir)
        if path:
            results[thinker_id] = path

    return results
