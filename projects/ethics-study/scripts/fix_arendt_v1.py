"""
TASK-171: Fix Arendt data — light metadata corrections + verification flagging.

Input: signal/ethics-study/tester-report-TASK-170.md

Changes:
 1. CLAIM-007 source_detail: "Postscript" → "Epilogue" (Eichmann in Jerusalem)
 2. CLAIM-009 source_detail: add explicit "Truth and Politics"
    (Between Past and Future, 1968) origin.
 3. All arendt claims (001~009): verified=true, append verification_log entry
    (date=2026-04-15, method=web_cross_check, result=passed).
"""
import requests

ES_BASE = "http://localhost:9200"
INDEX = "ethics-claims"

VERIFICATION_ENTRY = {
    "date": "2026-04-15",
    "method": "web_cross_check",
    "result": "passed",
}

# Explicit new source_detail strings per tester-report-TASK-170 observations 1~2.
SOURCE_DETAIL_UPDATES = {
    "arendt-claim-007": (
        "Eichmann in Jerusalem, Epilogue; Postscript (1964); "
        "The Life of the Mind, Introduction"
    ),
    "arendt-claim-009": (
        "\"Truth and Politics\" (Between Past and Future, 1967/1968); "
        "Lectures on Kant's Political Philosophy; "
        "The Life of the Mind, Vol. 1 Thinking, Introduction"
    ),
}


def es_get(doc_id):
    r = requests.get(f"{ES_BASE}/{INDEX}/_doc/{doc_id}")
    data = r.json()
    if not data.get("found"):
        return None
    return data["_source"]


def es_update(doc_id, doc):
    url = f"{ES_BASE}/{INDEX}/_update/{doc_id}"
    r = requests.post(url, json={"doc": doc}, headers={"Content-Type": "application/json"})
    result = r.json()
    ok = r.status_code in (200, 201)
    tag = result.get("result", "?") if ok else f"ERR {r.status_code}"
    print(f"  [{tag}] {doc_id}")
    if not ok:
        print(f"    body: {result}")
    return ok


def already_logged(log, entry):
    return any(
        e.get("date") == entry["date"]
        and e.get("method") == entry["method"]
        and e.get("result") == entry["result"]
        for e in (log or [])
    )


def main():
    results = {}

    claim_ids = [f"arendt-claim-{i:03d}" for i in range(1, 10)]

    print("=== 1. source_detail 수정 ===")
    for cid, new_sd in SOURCE_DETAIL_UPDATES.items():
        src = es_get(cid)
        if src is None:
            print(f"  NOT FOUND: {cid}")
            results[f"source_detail_{cid}"] = "NOT_FOUND"
            continue
        print(f"  before: {src.get('source_detail')}")
        print(f"  after : {new_sd}")
        ok = es_update(cid, {"source_detail": new_sd})
        results[f"source_detail_{cid}"] = "FIXED" if ok else "FAILED"

    print("\n=== 2. verified=true + verification_log append ===")
    for cid in claim_ids:
        src = es_get(cid)
        if src is None:
            print(f"  NOT FOUND: {cid}")
            results[f"verify_{cid}"] = "NOT_FOUND"
            continue
        log = src.get("verification_log") or []
        if already_logged(log, VERIFICATION_ENTRY):
            new_log = log
            note = "log already present"
        else:
            new_log = log + [VERIFICATION_ENTRY]
            note = "appended"
        ok = es_update(cid, {"verified": True, "verification_log": new_log})
        results[f"verify_{cid}"] = f"DONE ({note})" if ok else "FAILED"

    print("\n=== 결과 요약 ===")
    for k, v in results.items():
        mark = "OK" if v.startswith(("FIXED", "DONE")) else ("?" if v == "NOT_FOUND" else "X")
        print(f"  [{mark}] {k}: {v}")

    failed = [k for k, v in results.items() if v == "FAILED"]
    if failed:
        print(f"\n실패 {len(failed)}건:")
        for f in failed:
            print(f"  - {f}")
        return 1
    print("\n모든 수정 완료")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
