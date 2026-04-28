"""YAML 로더 — YAML 파일에서 사상가 데이터를 읽어 ES에 적재한다."""

import os
from typing import Any, Dict

import yaml
from elasticsearch import Elasticsearch

from src.config import (
    INDEX_CLAIMS,
    INDEX_FIELDS,
    INDEX_KEYWORDS,
    INDEX_RELATIONS,
    INDEX_THINKERS,
    INDEX_WORKS,
)
from src.es_client import bulk_insert, index_document


def load_yaml_file(filepath: str) -> dict:
    """YAML 파일을 읽어 딕셔너리로 반환한다."""
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_thinker_to_es(client: Elasticsearch, data: dict) -> dict:
    """YAML 데이터를 ES에 적재한다.

    thinker, works, claims, keywords, relations 각각 인덱싱한다.
    claims의 thinker_id는 thinker.id로 자동 채운다.
    keywords의 thinker_id도 자동 채운다.
    claims의 argument, counterpoint 필드는 YAML에 있을 경우 그대로 적재된다.

    Returns:
        {'thinkers': 1, 'works': N, 'claims': N, 'keywords': N, 'relations': N}
    """
    result: Dict[str, int] = {
        "thinkers": 0,
        "works": 0,
        "claims": 0,
        "keywords": 0,
        "relations": 0,
    }

    # ── thinker ──
    thinker = data.get("thinker")
    if thinker:
        thinker_id = thinker["id"]
        index_document(client, INDEX_THINKERS, thinker, doc_id=thinker_id)
        result["thinkers"] = 1
    else:
        thinker_id = None

    # ── works ──
    works = data.get("works", [])
    if works:
        for work in works:
            if thinker_id and "thinker_id" not in work:
                work["thinker_id"] = thinker_id
        bulk_insert(client, INDEX_WORKS, works, id_field="id")
        result["works"] = len(works)

    # ── claims ──
    claims = data.get("claims", [])
    if claims:
        for claim in claims:
            if thinker_id and "thinker_id" not in claim:
                claim["thinker_id"] = thinker_id
        bulk_insert(client, INDEX_CLAIMS, claims, id_field="id")
        result["claims"] = len(claims)

    # ── keywords ──
    keywords = data.get("keywords", [])
    if keywords:
        for kw in keywords:
            if thinker_id and "thinker_id" not in kw:
                kw["thinker_id"] = thinker_id
        bulk_insert(client, INDEX_KEYWORDS, keywords, id_field="id")
        result["keywords"] = len(keywords)

    # ── relations ──
    relations = data.get("relations", [])
    if relations:
        bulk_insert(client, INDEX_RELATIONS, relations, id_field="id")
        result["relations"] = len(relations)

    return result


def load_fields_to_es(client: Elasticsearch, filepath: str) -> int:
    """fields.yaml을 읽어 ES에 적재한다.

    Returns:
        적재된 분야 수
    """
    data = load_yaml_file(filepath)
    fields = data.get("fields", [])
    if not fields:
        return 0
    bulk_insert(client, INDEX_FIELDS, fields, id_field="id")
    return len(fields)


def load_all(client: Elasticsearch, data_dir: str) -> dict:
    """data/ 디렉토리의 모든 YAML을 순회하며 ES에 적재한다.

    fields.yaml -> 분야 적재
    각 하위 디렉토리의 *.yaml -> 사상가 적재

    Returns:
        {'fields': N, 'thinkers': N, 'works': N, 'claims': N, 'keywords': N, 'relations': N}
    """
    totals: Dict[str, int] = {
        "fields": 0,
        "thinkers": 0,
        "works": 0,
        "claims": 0,
        "keywords": 0,
        "relations": 0,
    }

    # fields.yaml 로딩
    fields_path = os.path.join(data_dir, "fields.yaml")
    if os.path.exists(fields_path):
        totals["fields"] = load_fields_to_es(client, fields_path)

    # 하위 디렉토리 순회
    for entry in sorted(os.listdir(data_dir)):
        subdir = os.path.join(data_dir, entry)
        if not os.path.isdir(subdir):
            continue
        for filename in sorted(os.listdir(subdir)):
            if not filename.endswith((".yaml", ".yml")):
                continue
            filepath = os.path.join(subdir, filename)
            data = load_yaml_file(filepath)
            counts = load_thinker_to_es(client, data)
            for key, val in counts.items():
                totals[key] += val

    return totals
