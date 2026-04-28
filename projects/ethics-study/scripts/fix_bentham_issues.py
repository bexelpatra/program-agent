"""
TASK-031: Fix Bentham data issues identified by Tester Agent (TASK-030)
"""
import requests
import json

ES_BASE = "http://localhost:9200"

def es_update(index, doc_id, body):
    url = f"{ES_BASE}/{index}/_update/{doc_id}"
    r = requests.post(url, json=body, headers={"Content-Type": "application/json"})
    result = r.json()
    if r.status_code not in (200, 201):
        print(f"  ERROR [{r.status_code}] {index}/{doc_id}: {result}")
    else:
        print(f"  OK [{result.get('result', '?')}] {index}/{doc_id}")
    return r.status_code in (200, 201)

def es_delete(index, doc_id):
    url = f"{ES_BASE}/{index}/_doc/{doc_id}"
    r = requests.delete(url)
    print(f"  DELETE [{r.status_code}] {index}/{doc_id}")
    return r.status_code in (200, 201)

def es_index(index, doc_id, body):
    url = f"{ES_BASE}/{index}/_doc/{doc_id}"
    r = requests.put(url, json=body, headers={"Content-Type": "application/json"})
    result = r.json()
    if r.status_code not in (200, 201):
        print(f"  ERROR [{r.status_code}] {index}/{doc_id}: {result}")
    else:
        print(f"  OK [{result.get('result', '?')}] {index}/{doc_id}")
    return r.status_code in (200, 201)

def main():
    results = {}

    # ======================================================
    # 심각 #1: relation-epicurus-bentham 방향 오류
    # 현재 ES에는 이미 relation-bentham-epicurus (올바른 방향)가 있음
    # ======================================================
    print("\n=== 심각 #1: epicurus-bentham 관계 확인 ===")
    r = requests.get(f"{ES_BASE}/ethics-relations/_doc/relation-bentham-epicurus")
    doc = r.json()
    if doc.get("found"):
        src = doc["_source"]
        print(f"  현재: from={src['from_thinker']}, to={src['to_thinker']}, type={src['type']}")
        if src["from_thinker"] == "bentham" and src["to_thinker"] == "epicurus":
            print("  -> 방향이 이미 올바름 (bentham -> epicurus, influenced_by)")
            results["심각_1_relation_epicurus"] = "ALREADY_CORRECT"
        else:
            print("  -> 방향 수정 필요")
            ok = es_update("ethics-relations", "relation-bentham-epicurus", {
                "doc": {
                    "from_thinker": "bentham",
                    "to_thinker": "epicurus",
                    "type": "influenced_by"
                }
            })
            results["심각_1_relation_epicurus"] = "FIXED" if ok else "FAILED"
    else:
        # 혹시 잘못된 ID로 있는지 확인
        r2 = requests.get(f"{ES_BASE}/ethics-relations/_doc/relation-epicurus-bentham")
        if r2.json().get("found"):
            src2 = r2.json()["_source"]
            print(f"  잘못된 ID 발견: from={src2['from_thinker']}, to={src2['to_thinker']}")
            # 올바른 방향으로 새 문서 생성
            new_doc = dict(src2)
            new_doc["id"] = "relation-bentham-epicurus"
            new_doc["from_thinker"] = "bentham"
            new_doc["to_thinker"] = "epicurus"
            ok1 = es_index("ethics-relations", "relation-bentham-epicurus", new_doc)
            ok2 = es_delete("ethics-relations", "relation-epicurus-bentham")
            results["심각_1_relation_epicurus"] = "FIXED" if (ok1 and ok2) else "FAILED"
        else:
            print("  -> 관련 문서 없음 — 건너뜀")
            results["심각_1_relation_epicurus"] = "NOT_FOUND"

    # ======================================================
    # 심각 #2: relation-hume-bentham 방향 오류
    # 현재 ES에는 이미 relation-bentham-hume (올바른 방향)가 있음
    # ======================================================
    print("\n=== 심각 #2: hume-bentham 관계 확인 ===")
    r = requests.get(f"{ES_BASE}/ethics-relations/_doc/relation-bentham-hume")
    doc = r.json()
    if doc.get("found"):
        src = doc["_source"]
        print(f"  현재: from={src['from_thinker']}, to={src['to_thinker']}, type={src['type']}")
        if src["from_thinker"] == "bentham" and src["to_thinker"] == "hume":
            print("  -> 방향이 이미 올바름 (bentham -> hume, influenced_by)")
            results["심각_2_relation_hume"] = "ALREADY_CORRECT"
        else:
            print("  -> 방향 수정 필요")
            ok = es_update("ethics-relations", "relation-bentham-hume", {
                "doc": {
                    "from_thinker": "bentham",
                    "to_thinker": "hume",
                    "type": "influenced_by"
                }
            })
            results["심각_2_relation_hume"] = "FIXED" if ok else "FAILED"
    else:
        r2 = requests.get(f"{ES_BASE}/ethics-relations/_doc/relation-hume-bentham")
        if r2.json().get("found"):
            src2 = r2.json()["_source"]
            new_doc = dict(src2)
            new_doc["id"] = "relation-bentham-hume"
            new_doc["from_thinker"] = "bentham"
            new_doc["to_thinker"] = "hume"
            ok1 = es_index("ethics-relations", "relation-bentham-hume", new_doc)
            ok2 = es_delete("ethics-relations", "relation-hume-bentham")
            results["심각_2_relation_hume"] = "FIXED" if (ok1 and ok2) else "FAILED"
        else:
            print("  -> 관련 문서 없음 — 건너뜀")
            results["심각_2_relation_hume"] = "NOT_FOUND"

    # ======================================================
    # 심각 #3: bentham-panopticon 출판연도 및 원제 오류
    # year: 1787 → 1791
    # title_original: "The Panopticon Writings" → "Panopticon; or, The Inspection-House"
    # ======================================================
    print("\n=== 심각 #3: bentham-panopticon 출판연도/원제 수정 ===")
    ok = es_update("ethics-works", "bentham-panopticon", {
        "doc": {
            "year": 1791,
            "title_original": "Panopticon; or, The Inspection-House"
        }
    })
    results["심각_3_panopticon_year_title"] = "FIXED" if ok else "FAILED"

    # ======================================================
    # 보통 #4: bentham thinker 출생지 표기 수정
    # 스피탈필즈 → 하운즈디치(Houndsditch)
    # ======================================================
    print("\n=== 보통 #4: bentham 출생지 표기 수정 ===")
    # 현재 background 가져오기
    r = requests.get(f"{ES_BASE}/ethics-thinkers/_doc/bentham")
    current_bg = r.json()["_source"]["background"]
    new_bg = current_bg.replace(
        "런던 스피탈필즈(Spitalfields)",
        "런던 하운즈디치(Houndsditch) 인근"
    )
    ok = es_update("ethics-thinkers", "bentham", {
        "doc": {
            "background": new_bg
        }
    })
    results["보통_4_birthplace"] = "FIXED" if ok else "FAILED"

    # ======================================================
    # 보통 #5: bentham-keyword-003 Beccaria 추가
    # ======================================================
    print("\n=== 보통 #5: bentham-keyword-003 Beccaria 추가 ===")
    r = requests.get(f"{ES_BASE}/ethics-keywords/_doc/bentham-keyword-003")
    current_def = r.json()["_source"]["definition"]
    # 프리스틀리 언급 뒤에 베카리아 내용 추가
    beccaria_addition = (
        " 또한 이탈리아 법학자 베카리아(Beccaria)의 '범죄와 형벌(Dei Delitti e delle Pene, 1764)'에도 "
        "유사 표현('la massima felicita divisa nel maggior numero', 최대 다수 사이에 나누어진 최대 행복)이 "
        "먼저 등장했다는 점에서, 이 원리의 기원에 대한 학문적 논의가 존재한다."
    )
    new_def = current_def + beccaria_addition
    ok = es_update("ethics-keywords", "bentham-keyword-003", {
        "doc": {
            "definition": new_def
        }
    })
    results["보통_5_keyword003_beccaria"] = "FIXED" if ok else "FAILED"

    # ======================================================
    # 보통 #6: bentham-claim-006 original_text 보충
    # ======================================================
    print("\n=== 보통 #6: bentham-claim-006 original_text 보충 ===")
    original_text_006 = (
        "The principle of asceticism... approves of actions in as far as they tend to "
        "diminish his happiness; and, as far as this goes, in opposition to that of utility. "
        "... The principle of sympathy and antipathy... approves or disapproves of certain "
        "actions, not on account of their tending to augment the happiness, nor yet on account "
        "of their tending to diminish the happiness of the party whose interest is in question, "
        "but merely because a man finds himself disposed to approve or disapprove of them: "
        "holding up that approbation or disapprobation as a sufficient reason for itself, and "
        "disclaiming the necessity of looking out for any extrinsic ground."
    )
    original_text_ko_006 = (
        "금욕주의의 원리는... 그 사람의 행복을 감소시키는 경향이 있는 한에서 행위를 시인하며, "
        "이 점에서 공리의 원리와 반대된다. ... 공감·반감의 원리는... 문제가 되는 당사자의 행복을 "
        "증가시키는 경향이 있다는 이유로도, 또한 감소시키는 경향이 있다는 이유로도 아닌, "
        "단지 인간이 그것을 시인하거나 부인하도록 경향되어 있다는 이유만으로 특정 행위를 "
        "시인하거나 부인한다. 이는 그러한 시인이나 부인을 그 자체로 충분한 이유로 내세우며, "
        "어떤 외적 근거를 찾을 필요를 부인한다."
    )
    ok = es_update("ethics-claims", "bentham-claim-006", {
        "doc": {
            "original_text": original_text_006,
            "original_text_ko": original_text_ko_006
        }
    })
    results["보통_6_claim006_original_text"] = "FIXED" if ok else "FAILED"

    # ======================================================
    # 보통 #7: bentham-claim-012 original_text 보충
    # ======================================================
    print("\n=== 보통 #7: bentham-claim-012 original_text 보충 ===")
    original_text_012 = (
        "The art of legislation teaches how a multitude of men, composing a community, "
        "may be disposed to pursue that course which upon the whole is the most conducive "
        "to the happiness of the whole community, by means of motives to be applied by the "
        "legislator. ... It is the greatest happiness of the greatest number that is the "
        "measure of right and wrong."
    )
    original_text_ko_012 = (
        "입법술은 공동체를 구성하는 다수의 사람들이, 전체적으로 공동체 전체의 행복에 가장 "
        "기여하는 행로를 추구하도록, 입법자가 적용하는 동기를 통해 어떻게 유도될 수 있는지를 "
        "가르친다. ... 옳고 그름의 척도는 최대 다수의 최대 행복이다."
    )
    ok = es_update("ethics-claims", "bentham-claim-012", {
        "doc": {
            "original_text": original_text_012,
            "original_text_ko": original_text_ko_012
        }
    })
    results["보통_7_claim012_original_text"] = "FIXED" if ok else "FAILED"

    # ======================================================
    # 경미 #8: bentham-panopticon 한국어 제목 수정
    # "판옵티콘 글들" → "판옵티콘; 또는 감시의 집"
    # ======================================================
    print("\n=== 경미 #8: bentham-panopticon 한국어 제목 수정 ===")
    ok = es_update("ethics-works", "bentham-panopticon", {
        "doc": {
            "title": "판옵티콘; 또는 감시의 집"
        }
    })
    results["경미_8_panopticon_title_ko"] = "FIXED" if ok else "FAILED"

    # ======================================================
    # 경미 #9: bentham thinker background에 Beccaria 추가
    # ======================================================
    print("\n=== 경미 #9: bentham background에 Beccaria 추가 ===")
    # 현재 background를 다시 읽음 (이미 #4에서 수정됨)
    r = requests.get(f"{ES_BASE}/ethics-thinkers/_doc/bentham")
    current_bg = r.json()["_source"]["background"]
    new_bg = current_bg.replace(
        "프리스틀리의 '최대 다수의 최대 행복' 원리와 흄의 경험주의, 에피쿠로스의 쾌락주의에 영향을 받았다.",
        "프리스틀리의 '최대 다수의 최대 행복' 원리와 흄의 경험주의, 에피쿠로스의 쾌락주의, 베카리아(Beccaria)의 형법 공리주의에 영향을 받았다."
    )
    if new_bg == current_bg:
        print("  -> 문자열 패턴이 맞지 않음. 직접 Beccaria 구문을 추가합니다.")
        # 마침표로 끝나는 문장이 없을 수 있으니 마지막 문장 수정
        new_bg = current_bg.replace(
            "에피쿠로스의 쾌락주의에 영향을 받았다",
            "에피쿠로스의 쾌락주의, 베카리아(Beccaria)의 형법 공리주의에 영향을 받았다"
        )
    ok = es_update("ethics-thinkers", "bentham", {
        "doc": {
            "background": new_bg
        }
    })
    results["경미_9_background_beccaria"] = "FIXED" if ok else "FAILED"

    # ======================================================
    # 최종: bentham-claim-001~012 모두 verified: true 처리
    # verification_log에 항목 append
    # ======================================================
    print("\n=== 최종: bentham-claim-001~012 verified: true 처리 ===")
    verification_entry = {"date": "2026-04-10", "method": "tester-agent-opus", "result": "verified"}

    for i in range(1, 13):
        claim_id = f"bentham-claim-{i:03d}"
        # 현재 verification_log 읽기
        r = requests.get(f"{ES_BASE}/ethics-claims/_doc/{claim_id}")
        if not r.json().get("found"):
            print(f"  NOT FOUND: {claim_id}")
            results[f"verified_{claim_id}"] = "NOT_FOUND"
            continue
        current_log = r.json()["_source"].get("verification_log", [])
        # 중복 추가 방지
        already_logged = any(
            e.get("date") == verification_entry["date"] and
            e.get("method") == verification_entry["method"]
            for e in current_log
        )
        if already_logged:
            # 그냥 verified: true 만 업데이트
            new_log = current_log
        else:
            new_log = current_log + [verification_entry]

        ok = es_update("ethics-claims", claim_id, {
            "doc": {
                "verified": True,
                "verification_log": new_log
            }
        })
        results[f"verified_{claim_id}"] = "DONE" if ok else "FAILED"

    # ======================================================
    # 최종 요약
    # ======================================================
    print("\n=== 수정 결과 요약 ===")
    for k, v in results.items():
        status_icon = "✓" if v in ("FIXED", "ALREADY_CORRECT", "DONE") else ("?" if v == "NOT_FOUND" else "✗")
        print(f"  {status_icon} {k}: {v}")

    failed = [k for k, v in results.items() if v == "FAILED"]
    if failed:
        print(f"\n실패 항목 수: {len(failed)}")
        for f in failed:
            print(f"  - {f}")
    else:
        print("\n모든 수정 완료!")

    return results

if __name__ == "__main__":
    main()
