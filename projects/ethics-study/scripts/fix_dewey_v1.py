"""
TASK-168: Dewey claims verified=true 반영 (TASK-167 검증 통과 결과)

입력: signal/ethics-study/tester-report-TASK-167.md
- 9개 claim 모두 웹/학술 교차검증 통과 (severity: observation, 치명 결함 없음)

수정 항목:
1. dewey-claim-001 ~ dewey-claim-009 모두 verified=true
2. verification_log 에 다음 항목 append:
   {date: "2026-04-15", method: "web_cross_check", result: "passed"}
"""
import requests

ES_BASE = "http://localhost:9200"
INDEX = "ethics-claims"

VERIFICATION_ENTRY = {
    "date": "2026-04-15",
    "method": "web_cross_check",
    "result": "passed",
}


def es_get(index, doc_id):
    r = requests.get(f"{ES_BASE}/{index}/_doc/{doc_id}")
    return r.json()


def es_update(index, doc_id, body):
    url = f"{ES_BASE}/{index}/_update/{doc_id}"
    r = requests.post(url, json=body, headers={"Content-Type": "application/json"})
    result = r.json()
    if r.status_code not in (200, 201):
        print(f"  ERROR [{r.status_code}] {index}/{doc_id}: {result}")
    else:
        print(f"  OK [{result.get('result', '?')}] {index}/{doc_id}")
    return r.status_code in (200, 201)


def main():
    results = {}
    print("=== TASK-168: dewey claims verified=true 반영 ===")

    for i in range(1, 10):
        claim_id = f"dewey-claim-{i:03d}"
        doc = es_get(INDEX, claim_id)
        if not doc.get("found"):
            print(f"  NOT FOUND: {claim_id}")
            results[claim_id] = "NOT_FOUND"
            continue

        src = doc["_source"]
        current_log = src.get("verification_log") or []

        already_logged = any(
            e.get("date") == VERIFICATION_ENTRY["date"]
            and e.get("method") == VERIFICATION_ENTRY["method"]
            for e in current_log
        )
        new_log = current_log if already_logged else current_log + [VERIFICATION_ENTRY]

        ok = es_update(
            INDEX,
            claim_id,
            {
                "doc": {
                    "verified": True,
                    "verification_log": new_log,
                }
            },
        )
        results[claim_id] = "DONE" if ok else "FAILED"

    print("\n=== 결과 요약 ===")
    for k, v in results.items():
        icon = "V" if v == "DONE" else ("?" if v == "NOT_FOUND" else "X")
        print(f"  [{icon}] {k}: {v}")

    failed = [k for k, v in results.items() if v not in ("DONE",)]
    if failed:
        print(f"\n주의 항목: {len(failed)}")
        for f in failed:
            print(f"  - {f}: {results[f]}")
    else:
        print("\n모든 dewey claim verified 처리 완료")

    # 검증: 업데이트 후 verified=true, log에 해당 entry 존재하는지 재조회
    print("\n=== 사후 검증 ===")
    for i in range(1, 10):
        claim_id = f"dewey-claim-{i:03d}"
        doc = es_get(INDEX, claim_id)
        if not doc.get("found"):
            print(f"  [X] {claim_id}: not found")
            continue
        src = doc["_source"]
        verified = src.get("verified")
        log = src.get("verification_log") or []
        has_entry = any(
            e.get("date") == VERIFICATION_ENTRY["date"]
            and e.get("method") == VERIFICATION_ENTRY["method"]
            and e.get("result") == VERIFICATION_ENTRY["result"]
            for e in log
        )
        status = "V" if (verified is True and has_entry) else "X"
        print(f"  [{status}] {claim_id}: verified={verified}, log_count={len(log)}, has_target_entry={has_entry}")

    return results


if __name__ == "__main__":
    main()
