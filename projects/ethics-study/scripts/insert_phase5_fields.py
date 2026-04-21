"""Phase 5 신규 분야(peace_studies, unification_edu, civic_edu) 3개를
`ethics-fields` 인덱스에 upsert 하는 스크립트.

- 기존 fields의 최대 order를 조회한 뒤 신규 3개를 max+1, max+2, max+3 연번으로 배정.
- 이미 존재하는 id가 있으면 기존 order를 유지하면서 name/description만 업데이트(upsert).
- 재실행 가능(idempotent).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import INDEX_FIELDS
from src.es_client import close_client, get_client


NEW_FIELDS = [
    {
        "id": "peace_studies",
        "name": "평화학",
        "description": "적극적 평화·구조적 폭력 등 갈퉁 기반 평화연구 분야",
    },
    {
        "id": "unification_edu",
        "name": "통일교육",
        "description": "분단체제론·통일지향 역사학 등 한국 통일 담론",
    },
    {
        "id": "civic_edu",
        "name": "민주시민교육",
        "description": "민주주의와 교육·공적 영역 등 시민성 형성 담론",
    },
]


def get_max_order(client) -> int:
    """ethics-fields 인덱스의 최대 order 값을 반환한다. 비어있으면 0."""
    # 인덱스 존재 확인
    if not client.indices.exists(index=INDEX_FIELDS):
        return 0

    result = client.search(
        index=INDEX_FIELDS,
        body={
            "size": 0,
            "aggs": {"max_order": {"max": {"field": "order"}}},
        },
    )
    max_val = result["aggregations"]["max_order"]["value"]
    if max_val is None:
        return 0
    return int(max_val)


def upsert_field(client, doc: dict) -> str:
    """field 문서를 upsert. 이미 존재하면 기존 order 유지."""
    try:
        existing = client.get(index=INDEX_FIELDS, id=doc["id"])
        # 기존 order 보존
        doc["order"] = existing["_source"].get("order", doc["order"])
        result = client.index(index=INDEX_FIELDS, id=doc["id"], document=doc)
        return f"updated (order={doc['order']}, result={result['result']})"
    except Exception:
        result = client.index(index=INDEX_FIELDS, id=doc["id"], document=doc)
        return f"created (order={doc['order']}, result={result['result']})"


def main() -> None:
    client = get_client()
    try:
        base_order = get_max_order(client)
        print(f"[info] 기존 max order = {base_order}")

        for i, field in enumerate(NEW_FIELDS, start=1):
            doc = dict(field)
            doc["order"] = base_order + i
            status = upsert_field(client, doc)
            print(f"[field] {doc['id']}: {status}")

        # refresh 후 검증
        client.indices.refresh(index=INDEX_FIELDS)
        print("\n[verify] 신규 3개 field 조회:")
        for field in NEW_FIELDS:
            res = client.get(index=INDEX_FIELDS, id=field["id"])
            src = res["_source"]
            print(
                f"  - id={src['id']}, name={src['name']}, "
                f"order={src['order']}, desc={src['description']}"
            )
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
