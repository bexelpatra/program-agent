"""강만길 데이터 수정 스크립트 (TASK-165).

BUG 수정:
1) ethics-relations 의 kang-mangil-rel-001/002 가 참조하는 백낙청 thinker_id 를
   `paek_nakchung` → `baek_nakcheong` 으로 교정한다.
2) 관계 문서의 `_source.id` 필드 누락 보강 (kang-mangil-rel-001~004).

부가 수정:
3) ethics-claims 의 kang_mangil 관련 7건 claim 에 verified=true 및 verification_log
   (date=2026-04-15, method=web_cross_check, result=passed) 추가.

실행 후 증빙으로 ES 재쿼리를 수행해 paek_nakchung 참조 0건 / baek_nakcheong 참조 2건
을 검증 출력한다.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import INDEX_RELATIONS, INDEX_CLAIMS

WRONG_ID = "paek_nakchung"
RIGHT_ID = "baek_nakcheong"

RELATION_IDS = [
    "kang-mangil-rel-001",
    "kang-mangil-rel-002",
    "kang-mangil-rel-003",
    "kang-mangil-rel-004",
]

CLAIM_IDS = [f"kang-mangil-claim-{i:03d}" for i in range(1, 8)]

VERIFICATION_ENTRY = {
    "date": "2026-04-15",
    "method": "web_cross_check",
    "result": "passed",
}


def fix_relations(client):
    fixed_refs = 0
    id_added = 0
    for rid in RELATION_IDS:
        doc = client.get(index=INDEX_RELATIONS, id=rid)["_source"]
        changed = False

        if doc.get("from_thinker") == WRONG_ID:
            doc["from_thinker"] = RIGHT_ID
            fixed_refs += 1
            changed = True
        if doc.get("to_thinker") == WRONG_ID:
            doc["to_thinker"] = RIGHT_ID
            fixed_refs += 1
            changed = True

        if "id" not in doc:
            doc["id"] = rid
            id_added += 1
            changed = True

        if changed:
            client.index(index=INDEX_RELATIONS, id=rid, document=doc)
            print(
                f"[relation] {rid} updated "
                f"(from={doc['from_thinker']}, to={doc['to_thinker']})"
            )
        else:
            print(f"[relation] {rid} 변경 없음")

    print(f"-> 참조 id 교정: {fixed_refs}건, id 필드 보강: {id_added}건")


def fix_claims(client):
    updated = 0
    for cid in CLAIM_IDS:
        doc = client.get(index=INDEX_CLAIMS, id=cid)["_source"]
        doc["verified"] = True
        log = list(doc.get("verification_log") or [])
        # 중복 방지: 같은 date+method 가 이미 있으면 스킵
        already = any(
            (e.get("date") == VERIFICATION_ENTRY["date"]
             and e.get("method") == VERIFICATION_ENTRY["method"])
            for e in log
        )
        if not already:
            log.append(VERIFICATION_ENTRY)
        doc["verification_log"] = log
        client.index(index=INDEX_CLAIMS, id=cid, document=doc)
        updated += 1
        print(f"[claim] {cid}: verified=True, log entries={len(log)}")
    print(f"-> claim 업데이트: {updated}건")


def verify(client):
    print("\n=== 검증 ===")
    # 참조 불일치 재확인
    resp = client.search(
        index=INDEX_RELATIONS,
        size=20,
        query={
            "bool": {
                "should": [
                    {"term": {"from_thinker": WRONG_ID}},
                    {"term": {"to_thinker": WRONG_ID}},
                ]
            }
        },
    )
    wrong_hits = resp["hits"]["total"]["value"]
    print(f"paek_nakchung 참조 문서 수: {wrong_hits} (기대: 0)")

    # kang-mangil-rel-001/002 만 한정해 확인 (해당 두 문서가 BUG 대상)
    resp2 = client.search(
        index=INDEX_RELATIONS,
        size=20,
        query={"ids": {"values": ["kang-mangil-rel-001", "kang-mangil-rel-002"]}},
    )
    right_hits = 0
    for h in resp2["hits"]["hits"]:
        s = h["_source"]
        if RIGHT_ID in (s.get("from_thinker"), s.get("to_thinker")):
            right_hits += 1
    print(
        "kang-mangil-rel-001/002 중 baek_nakcheong 을 참조하는 문서 수: "
        f"{right_hits} (기대: 2)"
    )
    for h in resp2["hits"]["hits"]:
        s = h["_source"]
        print(
            f"  - {h['_id']}: from={s.get('from_thinker')} to={s.get('to_thinker')} "
            f"id_field={s.get('id')}"
        )

    return wrong_hits, right_hits


def main():
    client = get_client()
    try:
        print("=== TASK-165 강만길 데이터 수정 시작 ===\n")
        print("[1] relations 참조 교정 및 id 필드 보강")
        fix_relations(client)
        print("\n[2] claims verification 필드 업데이트")
        fix_claims(client)

        # Refresh so the verification search sees updates immediately
        client.indices.refresh(index=INDEX_RELATIONS)
        client.indices.refresh(index=INDEX_CLAIMS)

        wrong, right = verify(client)
        if wrong == 0 and right == 2:
            print("\n=== SUCCESS: 참조 무결성 복구 확인 ===")
            return 0
        else:
            print("\n=== FAIL: 기대값 불일치 ===")
            return 1
    finally:
        try:
            close_client(client)
        except TypeError:
            close_client()


if __name__ == "__main__":
    sys.exit(main())
