"""TASK-162: 백낙청(baek_nakcheong) 경량 수정.

Tester report (TASK-161) 기반:
1. thinker.background 정확화
   - 서울대 영문과 부임 1962, 유신반대 해직 1974, 복직 1980, 정년 2003
2. 모든 baek_nakcheong claims의 verified=true, verification_log 추가
   (date=2026-04-15, method=web_cross_check, result=passed)
3. kang_mangil ↔ baek_nakcheong 관계 추가 (민족문학론/6·15위 공동 활동)

※ original_text 필드명 통일은 범위 밖 (프로젝트 레벨 이슈).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import (
    INDEX_CLAIMS,
    INDEX_RELATIONS,
    INDEX_THINKERS,
)
from src.es_client import close_client, get_client


VERIFICATION_ENTRY = {
    "date": "2026-04-15",
    "method": "web_cross_check",
    "result": "passed",
}


NEW_BACKGROUND = (
    "대구 출생. 경기고를 졸업하고 미국 브라운 대학교에서 학사, "
    "하버드 대학교에서 영문학 박사학위(1972, D.H. 로렌스 연구)를 받았다. "
    "1962년 서울대학교 영문학과에 부임하여 2003년 정년퇴임할 때까지 재직했으며, "
    "1974년 유신체제에 반대하는 '민주회복 국민선언' 서명 등으로 해직되었다가 "
    "1980년 복직하였다. "
    "1966년 계간지 『창작과비평』을 창간하고 편집인·발행인을 오랜 기간 맡았다. "
    "민족문학론·분단체제론·변혁적 중도주의·87년체제론 등 "
    "한국 사회를 설명하는 독자적 이론 체계를 구축한 문학평론가이자 사회사상가이다. "
    "6·15공동선언실천 남측위원회 상임대표, 한반도평화포럼 공동이사장 등을 역임하며 "
    "통일·평화 운동에 실천적으로 참여했다."
)


def update_thinker_background(client):
    """thinker.background 서울대 재직 기간 정확화."""
    client.update(
        index=INDEX_THINKERS,
        id="baek_nakcheong",
        doc={"background": NEW_BACKGROUND},
    )
    print("[thinker] baek_nakcheong.background 갱신")


def verify_claims(client):
    """모든 baek_nakcheong claims의 verified=true + verification_log append."""
    query = {
        "query": {"term": {"thinker_id": "baek_nakcheong"}},
        "size": 100,
        "_source": ["id", "verified", "verification_log"],
    }
    resp = client.search(index=INDEX_CLAIMS, body=query)
    hits = resp["hits"]["hits"]
    print(f"[claims] {len(hits)}건 조회")

    updated = 0
    for hit in hits:
        doc_id = hit["_id"]
        src = hit["_source"]
        existing_log = src.get("verification_log") or []
        # 중복 방지: 동일 date+method 기존 엔트리가 있으면 추가하지 않음
        already = any(
            e.get("date") == VERIFICATION_ENTRY["date"]
            and e.get("method") == VERIFICATION_ENTRY["method"]
            for e in existing_log
        )
        new_log = existing_log if already else existing_log + [VERIFICATION_ENTRY]
        client.update(
            index=INDEX_CLAIMS,
            id=doc_id,
            doc={
                "verified": True,
                "verification_log": new_log,
            },
        )
        updated += 1
        print(f"  [claim] {doc_id}: verified=true, log={len(new_log)}건")
    return updated


def insert_relations(client):
    """강만길 ↔ 백낙청 관계 추가.

    근거:
    - 두 사람은 민족문학론·통일지향 역사학의 상호보완적 담론 형성자로,
      1970~2000년대 『창작과비평』 지면에서 공동 작업 및 교차 인용.
    - 6·15공동선언실천 남측위원회 등 통일·평화 운동의 시민사회 결성에 공동 참여
      (강만길은 고문·상임고문, 백낙청은 상임대표).
    """
    relations = [
        {
            "from_thinker": "baek_nakcheong",
            "to_thinker": "kang_mangil",
            "type": "collaborated",
            "description": (
                "백낙청은 『창작과비평』 지면 및 6·15공동선언실천 남측위원회 등 "
                "통일·평화 운동에서 강만길과 공동 작업했다. 문학평론(민족문학론) "
                "쪽에서 사회·역사(통일지향 역사학)와 결합하는 공동의 담론 장을 형성했다."
            ),
            "evidence": (
                "『창작과비평』 편집진·필자 구성 및 6·15공동선언실천 남측위원회 "
                "임원 명단(상임대표 백낙청, 고문/상임고문 강만길)"
            ),
        },
        {
            "from_thinker": "kang_mangil",
            "to_thinker": "baek_nakcheong",
            "type": "collaborated",
            "description": (
                "강만길은 통일지향 역사학의 관점에서 백낙청의 분단체제론·민족문학론과 "
                "상호 참조·공동 활동했다. 분단시대의 역사인식과 문학적 실천을 "
                "공동의 담론으로 엮는 데 기여했다."
            ),
            "evidence": (
                "『창작과비평』 공동 기고·대담, 6·15공동선언실천 남측위원회 공동 참여"
            ),
        },
    ]

    inserted = 0
    for rel in relations:
        rel_id = f"{rel['from_thinker']}-{rel['type']}-{rel['to_thinker']}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id}: {result['result']}")
        inserted += 1
    return inserted


def main():
    print("=== TASK-162: 백낙청 경량 수정 시작 ===\n")
    client = get_client()
    try:
        print("[1/3] thinker.background 갱신...")
        update_thinker_background(client)
        print()

        print("[2/3] claims verified=true + verification_log...")
        updated = verify_claims(client)
        print(f"     → {updated}건 갱신\n")

        print("[3/3] kang_mangil ↔ baek_nakcheong 관계 입력...")
        rel_count = insert_relations(client)
        print(f"     → {rel_count}건 입력\n")

        for idx in [INDEX_THINKERS, INDEX_CLAIMS, INDEX_RELATIONS]:
            client.indices.refresh(index=idx)

        print("=== 완료 ===")
        print(f"  - thinker background: 갱신")
        print(f"  - claims verified: {updated}건")
        print(f"  - relations: {rel_count}건")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
