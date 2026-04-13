"""
TASK-061: Fix Mencius data issues identified by Tester Agent (TASK-060)

심각 이슈 3건:
  S-1. claim-011 work_id 오류 (mencius-jinxin → mencius-mencius)
  S-2. relation mencius→xunzi 방향 오류 (순자가 맹자를 비판한 것)
  S-3. relation mencius→gaozi description 서술 주어 불일치

보통 이슈 1건:
  M-1. claim-004 work_id/source_detail 오류 (공손추편 → 고자편)
"""
import requests
import json
import time

ES_BASE = "http://localhost:9200"


def es_get(index, doc_id):
    """ES 문서 조회."""
    r = requests.get(f"{ES_BASE}/{index}/_doc/{doc_id}")
    return r.json()


def es_update(index, doc_id, body):
    """ES 문서 부분 업데이트."""
    url = f"{ES_BASE}/{index}/_update/{doc_id}"
    r = requests.post(url, json=body, headers={"Content-Type": "application/json"})
    result = r.json()
    if r.status_code not in (200, 201):
        print(f"  ERROR [{r.status_code}] {index}/{doc_id}: {result}")
    else:
        print(f"  OK [{result.get('result', '?')}] {index}/{doc_id}")
    return r.status_code in (200, 201)


def es_delete(index, doc_id):
    """ES 문서 삭제."""
    url = f"{ES_BASE}/{index}/_doc/{doc_id}"
    r = requests.delete(url)
    print(f"  DELETE [{r.status_code}] {index}/{doc_id}")
    return r.status_code in (200, 201)


def es_index(index, doc_id, body):
    """ES 문서 생성/덮어쓰기."""
    url = f"{ES_BASE}/{index}/_doc/{doc_id}"
    r = requests.put(url, json=body, headers={"Content-Type": "application/json"})
    result = r.json()
    if r.status_code not in (200, 201):
        print(f"  ERROR [{r.status_code}] {index}/{doc_id}: {result}")
    else:
        print(f"  OK [{result.get('result', '?')}] {index}/{doc_id}")
    return r.status_code in (200, 201)


def es_search(index, query):
    """ES 검색."""
    url = f"{ES_BASE}/{index}/_search"
    r = requests.post(url, json=query, headers={"Content-Type": "application/json"})
    return r.json()


def main():
    results = {}
    date_str = time.strftime("%Y-%m-%d")

    def make_vlog(note, task_id="TASK-061", method="tester_review_fix", result_val="fixed"):
        """verification_log 항목 생성 (nested object)."""
        return {
            "date": date_str,
            "task_id": task_id,
            "method": method,
            "result": result_val,
            "note": note
        }

    # ======================================================
    # S-1: claim-011 work_id 오류
    # mencius-jinxin(진심편) → mencius-mencius(맹자 전체)
    # 실제 출처: 등문공편(滕文公篇) 하 3.2
    # ======================================================
    print("\n=== S-1: claim-011 work_id 수정 ===")
    doc = es_get("ethics-claims", "mencius-claim-011")
    if doc.get("found"):
        src = doc["_source"]
        print(f"  현재 work_id: {src.get('work_id')}")
        print(f"  현재 source_detail: {src.get('source_detail')}")
        existing_vlog = src.get("verification_log", []) or []
        new_vlog = existing_vlog + [make_vlog("work_id mencius-jinxin→mencius-mencius 수정 (등문공편은 독립 works 미등록). source_detail 확인 완료.")]
        ok = es_update("ethics-claims", "mencius-claim-011", {
            "doc": {
                "work_id": "mencius-mencius",
                "source_detail": "맹자 등문공편(滕文公篇) 하 3.2",
                "verified": True,
                "verification_log": new_vlog
            }
        })
        results["S1_claim011_workid"] = "FIXED" if ok else "FAILED"
    else:
        print("  -> mencius-claim-011 문서 없음")
        results["S1_claim011_workid"] = "NOT_FOUND"

    # ======================================================
    # S-2: relation mencius→xunzi 방향 오류
    # 현재: from=mencius, to=xunzi, type=criticized (맹자가 순자를 비판)
    # 실제: 순자가 맹자를 비판 (순자 성악편)
    # 수정: 기존 삭제 후 xunzi→mencius criticized로 재등록
    # ======================================================
    print("\n=== S-2: relation mencius→xunzi 방향 수정 ===")
    doc = es_get("ethics-relations", "relation-mencius-xunzi-debate")
    if doc.get("found"):
        src = doc["_source"]
        print(f"  현재: from={src['from_thinker']}, to={src['to_thinker']}, type={src['type']}")

        # 기존 잘못된 relation 삭제
        ok1 = es_delete("ethics-relations", "relation-mencius-xunzi-debate")

        # 올바른 방향으로 새 문서 생성: xunzi→mencius criticized
        new_doc = {
            "id": "relation-xunzi-mencius-debate",
            "from_thinker": "xunzi",
            "to_thinker": "mencius",
            "type": "criticized",
            "description": (
                "순자(荀子)는 맹자의 성선설을 정면으로 비판하며 성악설(性惡說)을 주장했다. "
                "순자는 '맹자가 성선을 말하면서 본성(性)과 인위(僞)를 구분하지 못했다'고 비판했다. "
                "두 사상가의 대립은 유가 내부의 가장 근본적인 인성론 논쟁이며, "
                "이후 동아시아 사상사 전체에 걸쳐 반복되는 핵심 주제이다. "
                "맹자는 내적 도덕성의 확충을, 순자는 외적 예의 학습을 강조했다."
            ),
            "strength": "강함",
            "period": "기원전 4~3세기",
            "verified": True,
            "verification_log": f"[{date_str}] TASK-061: 방향 수정 mencius→xunzi를 xunzi→mencius로 변경. 순자가 맹자를 비판한 것이 역사적 사실."
        }
        ok2 = es_index("ethics-relations", "relation-xunzi-mencius-debate", new_doc)
        results["S2_relation_xunzi"] = "FIXED" if (ok1 and ok2) else "FAILED"
    else:
        print("  -> relation-mencius-xunzi-debate 문서 없음")
        results["S2_relation_xunzi"] = "NOT_FOUND"

    # ======================================================
    # S-3: relation mencius→gaozi description 서술 주어 수정
    # 방향: mencius→gaozi criticized (맹자가 고자를 비판) — 방향 자체는 맞음
    # 문제: description이 "고자(告子)는 맹자와 직접 논쟁한..."으로 고자가 주어
    # 수정: "맹자(孟子)는 고자의 성무선악설을..."로 맹자가 주어가 되도록 변경
    # ======================================================
    print("\n=== S-3: relation mencius→gaozi description 수정 ===")
    doc = es_get("ethics-relations", "relation-mencius-gaozi-debate")
    if doc.get("found"):
        src = doc["_source"]
        print(f"  현재 description 시작: {src['description'][:40]}...")
        new_description = (
            "맹자(孟子)는 고자(告子)의 성무선악설(性無善惡說)을 정면으로 논박하며 성선설을 확립했다. "
            "고자가 '식색성야(食色性也, 먹고 싶고 아름다움을 좋아하는 것이 본성)'라 하여 "
            "본성을 자연적 욕구로 보고, '인은 내적이지만 의는 외적(仁內義外)'이라 주장하자, "
            "맹자는 물의 비유(水之就下), 우산의 비유(牛山之木) 등으로 이를 논박했다. "
            "이 논쟁은 맹자 고자편의 핵심 내용이다."
        )
        ok = es_update("ethics-relations", "relation-mencius-gaozi-debate", {
            "doc": {
                "description": new_description,
                "verified": True,
                "verification_log": f"[{date_str}] TASK-061: description 서술 주어를 맹자로 수정하여 from→to 방향(맹자가 고자를 criticized)과 일치시킴."
            }
        })
        results["S3_relation_gaozi"] = "FIXED" if ok else "FAILED"
    else:
        print("  -> relation-mencius-gaozi-debate 문서 없음")
        results["S3_relation_gaozi"] = "NOT_FOUND"

    # ======================================================
    # M-1: claim-004 work_id/source_detail 오류
    # 현재: work_id=mencius-gongsunchou, source_detail="공손추편 상 2.6, 진심편 상 7.21"
    # 실제: 원문은 고자편(告子篇) 상 6.6
    # 수정: work_id=mencius-gaozi, source_detail 첫 출처를 고자편으로 변경
    # ======================================================
    print("\n=== M-1: claim-004 work_id/source_detail 수정 ===")
    doc = es_get("ethics-claims", "mencius-claim-004")
    if doc.get("found"):
        src = doc["_source"]
        print(f"  현재 work_id: {src.get('work_id')}")
        print(f"  현재 source_detail: {src.get('source_detail')}")
        existing_vlog = src.get("verification_log", []) or []
        new_vlog = existing_vlog + [make_vlog("work_id mencius-gongsunchou→mencius-gaozi 수정. source_detail 주 출처를 고자편 6.6으로 정정, 진심편 7.21은 참고로 표시.")]
        ok = es_update("ethics-claims", "mencius-claim-004", {
            "doc": {
                "work_id": "mencius-gaozi",
                "source_detail": "맹자 고자편(告子篇) 상 6.6, 진심편(盡心篇) 상 7.21(참고)",
                "verified": True,
                "verification_log": new_vlog
            }
        })
        results["M1_claim004_workid"] = "FIXED" if ok else "FAILED"
    else:
        print("  -> mencius-claim-004 문서 없음")
        results["M1_claim004_workid"] = "NOT_FOUND"

    # ======================================================
    # 나머지 이슈 없는 claims에 verified: true 설정
    # ======================================================
    print("\n=== 이슈 없는 claims에 verified: true 설정 ===")
    verified_claims = [
        "mencius-claim-001", "mencius-claim-002", "mencius-claim-003",
        "mencius-claim-005", "mencius-claim-006", "mencius-claim-007",
        "mencius-claim-008", "mencius-claim-009", "mencius-claim-010",
        "mencius-claim-012", "mencius-claim-013", "mencius-claim-014",
        "mencius-claim-015", "mencius-claim-016", "mencius-claim-017"
    ]
    verified_ok = 0
    verified_fail = 0
    for claim_id in verified_claims:
        # 기존 verification_log 조회
        cdoc = es_get("ethics-claims", claim_id)
        existing_vlog = []
        if cdoc.get("found"):
            existing_vlog = cdoc["_source"].get("verification_log", []) or []
        new_vlog = existing_vlog + [make_vlog("Tester 검증 합격. 이슈 없음.", result_val="passed")]
        ok = es_update("ethics-claims", claim_id, {
            "doc": {
                "verified": True,
                "verification_log": new_vlog
            }
        })
        if ok:
            verified_ok += 1
        else:
            verified_fail += 1
    results["verified_claims"] = f"{verified_ok} OK, {verified_fail} FAIL"
    print(f"  verified 설정: {verified_ok} OK, {verified_fail} FAIL")

    # ======================================================
    # 나머지 이슈 없는 relations에 verified: true 설정
    # ======================================================
    print("\n=== 이슈 없는 relations에 verified: true 설정 ===")
    verified_relations = [
        "relation-mencius-zhuxi",
        "relation-mencius-wangyangming"
    ]
    rel_ok = 0
    rel_fail = 0
    for rel_id in verified_relations:
        ok = es_update("ethics-relations", rel_id, {
            "doc": {
                "verified": True,
                "verification_log": f"[{date_str}] TASK-061: Tester 검증 합격. 방향/내용 정확."
            }
        })
        if ok:
            rel_ok += 1
        else:
            rel_fail += 1
    results["verified_relations"] = f"{rel_ok} OK, {rel_fail} FAIL"
    print(f"  verified 설정: {rel_ok} OK, {rel_fail} FAIL")

    # confucius→mencius 관계는 insert_confucius.py에서 등록된 것이므로 여기서 처리하지 않음

    # ======================================================
    # 검증: 수정 결과 확인
    # ======================================================
    print("\n=== 수정 결과 검증 ===")

    # claim-011 확인
    doc = es_get("ethics-claims", "mencius-claim-011")
    if doc.get("found"):
        src = doc["_source"]
        print(f"  claim-011 work_id: {src.get('work_id')} (expected: mencius-mencius)")
        print(f"  claim-011 verified: {src.get('verified')}")
        assert src.get("work_id") == "mencius-mencius", "claim-011 work_id 수정 실패!"

    # claim-004 확인
    doc = es_get("ethics-claims", "mencius-claim-004")
    if doc.get("found"):
        src = doc["_source"]
        print(f"  claim-004 work_id: {src.get('work_id')} (expected: mencius-gaozi)")
        print(f"  claim-004 verified: {src.get('verified')}")
        assert src.get("work_id") == "mencius-gaozi", "claim-004 work_id 수정 실패!"

    # relation xunzi→mencius 확인
    doc = es_get("ethics-relations", "relation-xunzi-mencius-debate")
    if doc.get("found"):
        src = doc["_source"]
        print(f"  xunzi→mencius: from={src['from_thinker']}, to={src['to_thinker']}, type={src['type']}")
        assert src["from_thinker"] == "xunzi" and src["to_thinker"] == "mencius", "relation 방향 수정 실패!"

    # 기존 mencius→xunzi가 삭제되었는지 확인
    doc = es_get("ethics-relations", "relation-mencius-xunzi-debate")
    if not doc.get("found"):
        print("  relation-mencius-xunzi-debate: 삭제 확인 OK")
    else:
        print("  WARNING: relation-mencius-xunzi-debate가 아직 존재함!")

    # relation mencius→gaozi description 확인
    doc = es_get("ethics-relations", "relation-mencius-gaozi-debate")
    if doc.get("found"):
        src = doc["_source"]
        print(f"  mencius→gaozi description 시작: {src['description'][:30]}...")
        assert src["description"].startswith("맹자"), "description 서술 주어 수정 실패!"

    # ======================================================
    # 결과 요약
    # ======================================================
    print("\n" + "=" * 60)
    print("수정 결과 요약")
    print("=" * 60)
    for key, val in results.items():
        print(f"  {key}: {val}")

    all_ok = all(
        v in ("FIXED", "ALREADY_CORRECT") or "OK" in str(v)
        for v in results.values()
    )
    print(f"\n최종 결과: {'SUCCESS' if all_ok else 'SOME FAILURES'}")
    return all_ok


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
