"""TASK-159: Galtung 데이터 경량 수정 스크립트 (observation 반영).

수정 항목:
1. galtung-claim-002 original_text: realizations -> realisations (영국식 원문 일치)
2. ethics-keywords에 kw-direct-violence 추가 (부재 시)
3. thinker galtung background: "150권 이상" -> "160권 이상"
4. habermas-influenced-galtung relation evidence 보강
5. 모든 galtung claims verified=true + verification_log 추가
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_CLAIMS, INDEX_KEYWORDS, INDEX_RELATIONS,
)

VERIFICATION_ENTRY = {
    "date": "2026-04-15",
    "method": "web_cross_check",
    "result": "passed",
}


def fix_claim_002_original_text(client):
    """claim-002 original_text: realizations -> realisations."""
    doc = client.get(index=INDEX_CLAIMS, id="galtung-claim-002")["_source"]
    old = doc["original_text"]
    new = old.replace("realizations", "realisations")
    if old == new:
        print("[claim-002] original_text: 이미 realisations (skip)")
        return
    client.update(
        index=INDEX_CLAIMS,
        id="galtung-claim-002",
        doc={"original_text": new},
    )
    print("[claim-002] original_text: realizations -> realisations")


def ensure_kw_direct_violence(client):
    """kw-direct-violence 키워드 문서가 없으면 추가."""
    try:
        client.get(index=INDEX_KEYWORDS, id="kw-direct-violence")
        print("[keyword] kw-direct-violence: 이미 존재 (skip)")
        return
    except Exception:
        pass
    doc = {
        "id": "kw-direct-violence",
        "term": "직접적 폭력",
        "term_en": "Direct Violence",
        "definition": (
            "갈퉁의 폭력 삼분법(직접적·구조적·문화적 폭력) 중 첫 번째 범주로, "
            "특정 가해자가 특정 대상에게 의도적으로 신체적·심리적 상해를 가하는 "
            "가시적 폭력을 뜻한다. 전쟁·살인·폭행·고문·테러 등이 대표 사례이며, "
            "'주체-행위-대상(subject-action-object)' 관계가 명시적으로 드러나는 점에서 "
            "구조적 폭력과 구분된다. 소극적 평화(negative peace)는 직접적 폭력의 부재로 정의된다."
        ),
        "thinker_id": "galtung",
        "work_id": "galtung-violence-peace-research",
        "related_terms": [
            "구조적 폭력",
            "문화적 폭력",
            "폭력의 삼각형",
            "소극적 평화",
        ],
    }
    client.index(index=INDEX_KEYWORDS, id="kw-direct-violence", document=doc)
    print("[keyword] kw-direct-violence: 추가")


def update_background(client):
    """thinker background: 150권 -> 160권."""
    doc = client.get(index=INDEX_THINKERS, id="galtung")["_source"]
    old_bg = doc["background"]
    new_bg = old_bg.replace("150권 이상의 저서", "160권 이상의 저서")
    if old_bg == new_bg:
        print("[thinker] background: 이미 160권 (skip)")
        return
    client.update(index=INDEX_THINKERS, id="galtung", doc={"background": new_bg})
    print("[thinker] background: 150권 -> 160권")


def update_habermas_relation_evidence(client):
    """habermas-influenced-galtung evidence 보강."""
    new_evidence = (
        "Peace by Peaceful Means(1996) Part I 'Peace Theory' 중 대화·담론윤리 기반 "
        "갈등 작업(dialogic conflict work) 논의; Searching for Peace(2002)에서 "
        "강제 없는 의사소통을 TRANSCEND 중재법의 이론적 전제로 수용. "
        "갈퉁은 하버마스의 의사소통합리성을 평화연구 맥락에서 당사자 간 공동 창조적 "
        "대안 탐색의 기반으로 재해석했다."
    )
    client.update(
        index=INDEX_RELATIONS,
        id="habermas-influenced-galtung",
        doc={"evidence": new_evidence},
    )
    print("[relation] habermas-influenced-galtung: evidence 보강")


def mark_claims_verified(client):
    """galtung의 모든 claims verified=true + verification_log append."""
    hits = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "galtung"}},
        size=50,
        _source=["id", "verified", "verification_log"],
    )["hits"]["hits"]
    for h in hits:
        cid = h["_id"]
        src = h["_source"]
        log = src.get("verification_log") or []
        # 중복 방지: 같은 date+method 엔트리가 있으면 skip 추가
        already = any(
            e.get("date") == VERIFICATION_ENTRY["date"]
            and e.get("method") == VERIFICATION_ENTRY["method"]
            for e in log
        )
        if not already:
            log = log + [VERIFICATION_ENTRY]
        client.update(
            index=INDEX_CLAIMS,
            id=cid,
            doc={"verified": True, "verification_log": log},
        )
        print(f"[claim] {cid}: verified=true, log entries={len(log)}")


def main():
    client = get_client()
    try:
        fix_claim_002_original_text(client)
        ensure_kw_direct_violence(client)
        update_background(client)
        update_habermas_relation_evidence(client)
        mark_claims_verified(client)
        # 인덱스 refresh (즉시 검증 가능하도록)
        client.indices.refresh(index=f"{INDEX_THINKERS},{INDEX_CLAIMS},{INDEX_KEYWORDS},{INDEX_RELATIONS}")
        print("\n[done] Galtung 경량 수정 완료")
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
