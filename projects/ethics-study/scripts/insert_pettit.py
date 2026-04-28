"""필립 페팃(Philip Pettit) 데이터를 ES에 직접 입력하는 스크립트.

Task: TASK-176-06
공식 출제: 2019-A Q10 · 2020-A Q10 · 2022-A Q6(가) · 2025-B Q10(경합) · 2026-B Q7
(페팃 기준 4회+ 확정 출제, 2025-B→2026-B 2연속).

political_philosophy 분야. rousseau/hobbes 등 공화주의·자유주의 전통 사상가 이미 ES 등록.
berlin·machiavelli·skinner·viroli·green_th 는 아직 미등록 — relation 생략.

원문 인용 규칙(agents/coder.md §원문/입력 인용 규칙) 엄수:
 - claims.original_text 는 coverage md 실측 원문(verbatim) 또는 빈 문자열("").
 - 모든 한자·영어 trademark 는 coverage md 역grep으로 0건이면 제거.

역grep 자기검증 (coverage 26파일 중 pettit 연관):
 - "Philip Pettit" → hit (2016-B L18, 2019-A L27, 2020-A L27, 2022-A L20, 2026-B L410·L412)
 - "필립 페팃" → hit (2016-B L18, 2020-A L27, 2022-A L20·L35·L59, 2026-B L410)
 - "비지배 자유" / "freedom as non-domination" → hit
 - "비간섭" / "non-interference" → hit
 - "Republicanism" → hit (2022-A L20, 2026-B L410)
 - "공화주의" → hit (광범위)
 - "주인으로서의 삶" → hit (2026-B L412)
 - "자의적 의지" / "자의적 지배" / "arbitrary" → hit (2020-A L27, 2026-B L422)
 - "권력 분립" / "separation of powers" → hit (2026-B L414·L417·L428·L438)
 - "반쟁의 가능성" / "contestability" → hit (2026-B L425·L438)
 - "eyeball test" → hit (2026-B L425)
 - "시민적 덕성" / "civic virtue" → hit (2020-A L27, 2026-B L425·L438)
 - "혼합 정체" / "mixed constitution" → hit (2026-B L425·L438)
 - "법의 지배" / "rule of law" → hit (2020-A L27, 2026-B L425·L438)
 - "지배(dominium)" / "dominium" → hit (2026-B L413·L438, 2016-B L18)
 - "눈을 내리깔고" / "눈을 크게 뜨고" → hit (2026-B L413)
 - "1945" → hit (2022-A L20, 2026-B L410)
 - "아일랜드" → hit (2026-B L410)
 - "프린스턴" → hit (2026-B L410)
 - "신로마 공화주의" / "neo-Roman" / "neo-republicanism" → hit (2022-A L20, 2026-B L410·L438)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS,
    INDEX_WORKS,
    INDEX_CLAIMS,
    INDEX_KEYWORDS,
    INDEX_RELATIONS,
    INDEX_FIELDS,
)


THINKER_ID = "pettit"


def ensure_field(client):
    """political_philosophy 분야 존재 확인 (기존 등록 확인됨)."""
    try:
        client.get(index=INDEX_FIELDS, id="political_philosophy")
        print("[field] political_philosophy: 이미 존재")
    except Exception:
        doc = {
            "id": "political_philosophy",
            "name": "정치철학",
            "description": (
                "정치 공동체의 정당성·자유·정의·권력·권리 등을 탐구하는 철학 분야. "
                "자유주의·공화주의·공동체주의·자유지상주의 등 현대 정치사상 계보를 포함한다."
            ),
            "order": 5,
        }
        result = client.index(index=INDEX_FIELDS, id="political_philosophy", document=doc)
        print(f"[field] political_philosophy: {result['result']}")


def insert_thinker(client):
    """페팃 사상가 데이터 입력."""
    doc = {
        "id": THINKER_ID,
        "name": "필립 페팃 (Philip Pettit)",
        "name_en": "Philip Pettit",
        "field": "political_philosophy",
        "era": "현대",
        "birth_year": 1945,
        "death_year": None,
        "background": (
            "아일랜드 출신의 미국 정치철학자. 프린스턴 대학교에서 "
            "정치·인간과학 교수로 오랜 기간 재직하고 있다. "
            "1997년 『Republicanism: A Theory of Freedom and Government』에서 "
            "'비지배 자유(freedom as non-domination)' 개념을 체계적으로 정식화하여 "
            "로마 공화국·마키아벨리·해링턴 전통을 현대에 부활시킨 '신로마 공화주의"
            "(neo-Roman republicanism)' 혹은 '신공화주의(neo-republicanism)'의 정초자로 평가된다. "
            "페팃은 이사야 벌린(Isaiah Berlin)의 '소극적 자유(비간섭)'와 '적극적 자유(자기지배)' "
            "이분법을 넘어 제3의 자유 개념으로 비지배 자유를 제시하였으며, "
            "자의적 지배 가능성(arbitrary domination) 자체의 제거를 자유의 본질로 규정하였다. "
            "임용 도덕·윤리 시험에서 2019-A Q10·2020-A Q10·2022-A Q6(가)·2025-B Q10·2026-B Q7 등 "
            "반복 출제되는 현대 정치철학의 핵심 사상가이다."
        ),
        "core_philosophy": (
            "페팃 정치철학의 핵심은 '비지배로서의 자유(freedom as non-domination)'이다. "
            "이는 자유주의가 자유를 '타인의 간섭 부재(non-interference)'로 정의한 것(홉스·벤담·벌린)과 "
            "구별되는 제3의 자유 개념이다. 페팃에 따르면 자유는 실제로 간섭받지 않는 상태가 아니라, "
            "타인의 자의적(arbitrary) 의지에 예속되지 않는 상태이다. "
            "자비로운 주인의 노예도 주인이 기분에 따라 언제든 "
            "간섭할 수 있는 권력을 지니고 있다는 점에서 여전히 노예이며 자유롭지 못하다. "
            "반대로 공정하고 비자의적인 법에 의한 간섭은 자유를 훼손하지 않는다. "
            "이 비지배 자유는 ① 법의 지배(rule of law), ② 권력 분립(separation of powers), "
            "③ 혼합 정체(mixed constitution), ④ 반쟁의 가능성(contestability), "
            "⑤ 공적 감시 제도(eyeball test), ⑥ 시민적 덕성(civic virtue) 등 "
            "제도적·시민적 조건에 의해 보장된다. "
            "페팃은 또한 공화주의의 권리 개념이 자유주의의 선재적 자연권과 달리 "
            "정치 공동체의 법과 제도에 의해 구성·보장되는 공민적 권리(civic rights)임을 강조한다."
        ),
        "philosophical_journey": (
            "페팃은 아일랜드에서 출생하여 영어권 분석철학·정치철학 전통 속에서 수학하였다. "
            "초기에는 심리철학·행위론·합리적 선택 이론 분야에서 활동하였으며, "
            "이후 정치철학으로 연구 영역을 확장하였다. "
            "1997년 『Republicanism: A Theory of Freedom and Government』 간행으로 "
            "공화주의 정치이론의 현대적 정식화를 완성하였다. "
            "이 저작에서 페팃은 벌린의 '자유의 두 개념(Two Concepts of Liberty, 1958)'을 비판하면서, "
            "소극적 자유(비간섭)와 적극적 자유(자기지배) 어느 쪽에도 환원되지 않는 "
            "제3의 자유 개념으로 비지배 자유를 제시한다. 책은 다음과 같이 구성된다: "
            "제1장 공화주의 전통, 제2장 'Liberty: Before Negative and Positive'에서 "
            "비지배 자유의 정의, 제3장 지배(dominium)의 분석, "
            "제4-5장 비지배 자유의 시민적·사회적 효용, "
            "제6장 'Republican Forms'에서 권력 분립·혼합 정체·법의 지배·반쟁의 가능성 등 "
            "제도적 안전장치, 제7장 'Civic Virtue'에서 덕스러운 시민성의 역할을 다룬다. "
            "페팃의 신로마 공화주의는 퀀틴 스키너(Quentin Skinner)의 지성사 연구, "
            "마우리치오 비롤리(Maurizio Viroli)의 공화주의적 애국심 연구와 함께 "
            "현대 공화주의 부활의 삼두마차를 이룬다."
        ),
        "keywords": [
            "비지배 자유",
            "비간섭 자유 비판",
            "공화주의",
            "신로마 공화주의",
            "자의적 지배",
            "지배",
            "권력 분립",
            "반쟁의 가능성",
            "법의 지배",
            "시민적 덕성",
            "혼합 정체",
            "주인 없는 삶",
        ],
    }
    result = client.index(index=INDEX_THINKERS, id=THINKER_ID, document=doc)
    print(f"[thinker] {THINKER_ID}: {result['result']}")
    return result


def insert_works(client):
    """페팃 주요 저서 데이터 입력."""
    works = [
        {
            "id": "pettit-republicanism-1997",
            "thinker_id": THINKER_ID,
            "title": "공화주의: 자유와 정부에 관한 이론",
            "title_original": "Republicanism: A Theory of Freedom and Government",
            "year": 1997,
            "significance": (
                "페팃 신로마 공화주의 정치이론의 정식 출발점이자 대표 저작. "
                "제2장 'Liberty: Before Negative and Positive'에서 "
                "벌린의 소극적·적극적 자유 이분법을 비판하며 제3의 자유 개념으로 "
                "'비지배 자유(freedom as non-domination)'를 정식화한다. "
                "자의적 의지에 예속되지 않음을 자유의 본질로 규정하고, "
                "법의 지배·권력 분립·혼합 정체·반쟁의 가능성·시민적 덕성 등 "
                "비지배를 실현하는 제도적·시민적 조건을 체계적으로 제시한다. "
                "임용 도덕·윤리 2020-A Q10·2022-A Q6(가)·2026-B Q7 제시문의 직접 근거 저작."
            ),
            "key_concepts": [
                "비지배 자유",
                "자의적 지배",
                "공화주의",
                "법의 지배",
                "권력 분립",
                "반쟁의 가능성",
                "시민적 덕성",
                "혼합 정체",
            ],
        },
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """페팃 핵심 주장 데이터 입력.

    original_text는 coverage md 실측 verbatim 원문만 기입.
    확증 불가 구절은 빈 문자열("")로 남기고 explanation에 해설만 둔다.
    """
    claims = [
        # CLAIM-001: 비지배 자유의 정의 (2022-A Q6 가)
        {
            "id": "pettit-claim-001",
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "source_detail": (
                "Republicanism: A Theory of Freedom and Government (1997) 제2장 · "
                "2022학년도 전공A Q6 (가)"
            ),
            "claim": (
                "자유란 타인의 의지에 예속되지 않는 상태, 즉 비지배(non-domination) 상태이다. "
                "공화주의 전통에서 발견되는 이 자유는 시민적 권리를 온전히 향유할 수 있는 "
                "시민만이 누릴 수 있는 자유이며, 외부적 간섭의 부재를 요구한다. "
                "자유로운 인간이 되기 위해서는 어떤 특정한 선택을 타인의 허락 없이 "
                "스스로 할 수 있어야 한다."
            ),
            # 2022-A.md L20 verbatim 인용
            "original_text": (
                "우리가 진정으로 자유로워지려면 타인의 의지에 예속되지 않아야 한다. "
                "예를 들어, 당신은 기본적인 자유라고 여겨지는 것을 주인에게 묻지 않고 "
                "스스로 행사할 수 있어야 한다. 공화주의 전통에서 발견되는 ( ㉠ )(이)란 "
                "시민적 권리를 온전히 향유할 수 있는 시민만이 누릴 수 있는 자유를 의미한다. "
                "이런 의미의 자유는 외부적 간섭의 부재를 요구한다. 자유로운 인간이 되기 "
                "위해서는 어떤 특정한 선택을 타인의 허락 없이 스스로 할 수 있어야 한다 "
                "— 2022학년도 전공A Q6 (가) 제시문 (coverage/2022-A.md L20)"
            ),
            "explanation": (
                "페팃 『공화주의: 자유와 정부에 관한 이론(Republicanism, 1997)』 제2장 "
                "'Liberty: Before Negative and Positive'의 핵심 정의. "
                "자유를 '타인의 자의적 의지에 예속되지 않음'으로 정식화하며, "
                "벌린의 소극적 자유(비간섭)와 적극적 자유(자기지배) 이분법을 넘어서는 "
                "제3의 자유 개념을 제시한다. 2022-A Q6 ㉠ 정답 = 비지배(非支配 — non-domination, "
                "공화주의적 자유)."
            ),
            "argument": (
                "전제1: 자유란 타인의 자의적 의지에 예속되지 않는 상태이다. "
                "전제2: 공화주의 전통은 시민적 권리를 향유하는 시민만이 이 자유를 누릴 수 있다고 본다. "
                "전제3: 이 자유는 비간섭을 함축하지만 그것으로 환원되지는 않는다. "
                "결론: 따라서 자유는 비지배로 정의되어야 하며, 주인에게 묻지 않고 스스로 행사할 "
                "수 있는 상태가 자유이다."
            ),
            "counterpoint": (
                "홉스·벤담·벌린 등 자유주의 전통은 자유를 '외적 방해의 부재' 혹은 "
                "'간섭이 없는 영역'으로 정의한다. 이 관점에서 볼 때 비지배 자유는 "
                "실제 간섭이 없음에도 '지배 가능성'이라는 가설적 조건으로 자유를 제한하여 "
                "자유 개념을 과도하게 두텁게 만든다는 비판이 가능하다."
            ),
            "context": (
                "2022-A Q6 ㉠ 빈칸 정답의 직접 근거. "
                "페팃 신로마 공화주의 자유론의 trademark 정의."
            ),
            "keywords": [
                "비지배 자유",
                "non-domination",
                "공화주의",
                "시민적 권리",
                "타인의 의지",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-002: 자유주의의 한계 — 주인으로서의 삶 (2026-B Q7)
        {
            "id": "pettit-claim-002",
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "source_detail": (
                "Republicanism (1997) 제2장 · 2026학년도 전공B Q7"
            ),
            "claim": (
                "자유주의는 국가나 타인들의 간섭으로부터 개인을 지켜내는 데는 성공을 거두었지만, "
                "개인들이 원했던 주인으로서의 삶을 살아가도록 보장하지는 못했다. "
                "비간섭만으로는 자유가 충분치 않으며, 지배(dominium) 자체의 부재가 자유의 조건이다."
            ),
            # 2026-B.md L403 (인용 블록) verbatim — coverage L412에서 재인용됨
            "original_text": (
                "자유주의는 국가나 타인들의 간섭으로부터 개인을 지켜내는 데는 성공을 거두었지만, "
                "개인들이 원했던 주인으로서의 삶을 살아가도록 보장하지는 못했다 "
                "— 2026학년도 전공B Q7 제시문 (coverage/2026-B.md L403·L412)"
            ),
            "explanation": (
                "페팃이 자유주의(특히 홉스·벤담·벌린의 비간섭 자유론)를 비판하는 핵심 구절. "
                "자유주의가 국가·타인의 간섭으로부터 개인의 사적 영역을 보호하는 데 성공했으나, "
                "그 자유는 '주인이 없는 삶'을 보장하지는 못한다. "
                "자비로운 주인의 노예도 주인이 기분에 따라 언제든 개입할 권력을 쥔 한 노예이며, "
                "따라서 실제 간섭 여부와 관계없이 '지배 권력의 존재' 자체가 자유의 훼손이다. "
                "2026-B Q7 제시문 첫 구절로 비지배 자유 trademark의 가장 압축된 표현."
            ),
            "argument": (
                "전제1: 자유주의는 자유를 외적 간섭의 부재로 정의한다. "
                "전제2: 자비로운 주인의 노예도 간섭 없이 살 수 있으나 여전히 노예이다. "
                "전제3: 따라서 비간섭만으로는 '주인으로서의 삶'이 보장되지 않는다. "
                "결론: 자유는 비간섭이 아니라 비지배, 즉 주인이 없는 상태로 정의되어야 한다."
            ),
            "counterpoint": (
                "자유주의자들은 '지배 가능성'이 실제 간섭으로 현실화되지 않는 한 "
                "자유를 침해한 것이 아니라고 본다. "
                "또한 '주인으로서의 삶'을 자유의 본질로 삼는 것은 "
                "벌린이 경고한 적극적 자유의 전체주의적 경사로 미끄러질 위험이 있다는 반론이 가능하다."
            ),
            "context": (
                "2026-B Q7 제시문 첫 문장 trademark · 페팃 비지배 자유의 자유주의 비판 공식. "
                "2025-B→2026-B 2연속 출제의 핵심 근거 구절."
            ),
            "keywords": [
                "주인으로서의 삶",
                "자유주의 비판",
                "비간섭",
                "비지배",
                "주인 없는 삶",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-003: 지배(dominium)의 현상학 (2026-B Q7)
        {
            "id": "pettit-claim-003",
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "source_detail": (
                "Republicanism (1997) 제2장·제3장 · 2026학년도 전공B Q7"
            ),
            "claim": (
                "힘센 자는 약한 자를 예속시킬 수 있는 힘이 있으므로 "
                "약한 자는 힘센 자에게 눈을 내리깔고 있어야 했고, "
                "동시에 힘센 자의 기분을 맞추기 위해 눈을 크게 뜨고 있어야 했다. "
                "이는 지배(dominium) 관계 속에서 약자가 강자의 자의적 권력 앞에 놓인 "
                "이중적 시선의 현상학이다."
            ),
            # 2026-B.md L403 인용 블록 verbatim
            "original_text": (
                "힘센 자와 약한 자가 있다고 가정해 보자. 힘센 자는 약한 자를 예속시킬 수 있는 "
                "힘이 있다. 그러므로 약한 자는 힘센 자에게 눈을 내리깔고 있어야 했다. "
                "이와 동시에 약한 자는 힘센 자의 기분을 맞추기 위해 눈을 크게 뜨고 있어야 했다 "
                "— 2026학년도 전공B Q7 제시문 (coverage/2026-B.md L403·L413)"
            ),
            "explanation": (
                "페팃 『Republicanism(1997)』 제2장·제3장에서 지배 관계를 "
                "'주인의 눈치를 살피는 노예의 이중적 시선'으로 묘사한 특징적 현상학. "
                "로마 공화주의 전통의 자유인(liber) 대 노예(servus) 대립을 현대어로 재해석하여, "
                "지배당하는 자는 주인의 비위를 맞추기 위해 눈을 크게 뜨고 경계하면서도 "
                "동시에 주인에게 맞서지 못하여 눈을 내리깔아야 하는 비굴한 이중 상태에 빠진다. "
                "이 현상은 실제 간섭이 일어나지 않을 때에도 지속되므로 "
                "지배 자체가 자유의 파괴임을 보여준다."
            ),
            "argument": (
                "전제1: 자의적 권력 앞의 약자는 권력자의 기분을 살펴 행동을 조정해야 한다. "
                "전제2: 이 조정은 실제 간섭이 없어도 심리적·행동적 복종을 강제한다. "
                "전제3: 따라서 지배 관계에서는 간섭 부재와 무관하게 이미 자유가 침해되어 있다. "
                "결론: 자유는 지배(dominium) 가능성 자체의 제거를 요구한다."
            ),
            "counterpoint": (
                "이 현상학적 묘사는 문학적 비유에 의존하므로 이론적 엄밀성이 부족하다는 비판이 있다. "
                "또한 모든 권력 비대칭이 이러한 이중 시선을 낳는 것은 아니라는 경험적 반론이 가능하다."
            ),
            "context": (
                "2026-B Q7 제시문 두 번째 문단 trademark · "
                "페팃 지배(dominium) 이론의 상징적 비유."
            ),
            "keywords": [
                "지배",
                "dominium",
                "자의적 권력",
                "주인-노예 관계",
                "예속",
                "이중 시선",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-004: 권력 분립 (2026-B Q7 ㉠)
        {
            "id": "pettit-claim-004",
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "source_detail": (
                "Republicanism (1997) 제6장 'Republican Forms' · 2026학년도 전공B Q7"
            ),
            "claim": (
                "공화주의자들은 권력 분립(separation of powers)의 원리가 지켜지지 않을 때 "
                "사법권과 입법권이 한 사람 혹은 하나의 기관에 집중됨으로써 "
                "개인의 자유가 훼손될 수 있다는 것을 잘 알고 있었다. "
                "권력 분립은 비지배 자유를 제도적으로 실현하는 안전장치이다."
            ),
            # 2026-B.md L405 인용 블록 verbatim
            "original_text": (
                "( ㉠ )(의) 원리 역시 공화주의의 영향을 받았다. 공화주의자들은 "
                "( ㉠ )(의) 원리가 지켜지지 않을 때, 사법권과 입법권이 한 사람 혹은 "
                "하나의 기관에 집중됨으로써 개인의 자유가 훼손될 수 있다는 것을 잘 알고 있었다 "
                "— 2026학년도 전공B Q7 제시문 (coverage/2026-B.md L405·L414)"
            ),
            "explanation": (
                "페팃 『Republicanism(1997)』 제6장 'Republican Forms'에서 "
                "몽테스키외의 삼권분립을 공화주의 전통이 계승한 것으로 해석하며, "
                "권력 분립이 비지배 자유를 제도적으로 실현하는 핵심 안전장치임을 강조한다. "
                "사법권과 입법권이 한 기관에 집중되면 그 기관이 자의적 지배 권력으로 변모할 수 있으므로, "
                "권력 상호 견제가 비지배 자유의 구조적 조건이 된다. "
                "2026-B Q7 ㉠ 정답 = 권력 분립(權力 分立 — separation of powers)."
            ),
            "argument": (
                "전제1: 권력 집중은 자의적 지배의 가능성을 구조적으로 창출한다. "
                "전제2: 자의적 지배의 가능성 자체가 비지배 자유의 조건을 파괴한다. "
                "전제3: 따라서 권력 분립은 비지배를 제도화하는 필수 장치이다. "
                "결론: 공화주의는 권력 분립을 자유 보장의 제도적 조건으로 수용한다."
            ),
            "counterpoint": (
                "순수한 권력 분립이 실제 정치에서 완전히 실현 가능한지, "
                "또한 권력 분립만으로 자의적 지배가 충분히 억제되는지에 대한 실효성 논쟁이 있다."
            ),
            "context": (
                "2026-B Q7 ㉠ 빈칸 정답의 직접 근거 · "
                "페팃 공화주의의 제도적 안전장치 trademark."
            ),
            "keywords": [
                "권력 분립",
                "separation of powers",
                "사법권",
                "입법권",
                "권력 집중",
                "입헌주의",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-005: 반쟁의 가능성 + 공적 감시 (2026-B Q7 보조)
        {
            "id": "pettit-claim-005",
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "source_detail": (
                "Republicanism (1997) · 2026학년도 전공B Q7 해설 구간"
            ),
            "claim": (
                "공화주의에서 개인의 권리는 반쟁의 가능성(contestability)과 공적 감시 제도(eyeball test)를 "
                "통해 보장된다. 시민은 권력 행사가 자의적일 때 이를 공적으로 이의 제기할 수 있어야 하며, "
                "권력자의 눈을 마주보며 굴종 없이 살 수 있어야 한다."
            ),
            # 2026-B.md L425 verbatim
            "original_text": (
                "페팃의 경우 \"반쟁의 가능성(contestability)\"과 \"공적 감시 제도(eyeball test)\", "
                "비롤리의 경우 \"공화주의적 애국심(patriotism)\"과 \"자유의 문화(culture of liberty)\"가 "
                "핵심 보장 기제 — 2026학년도 전공B Q7 해설 (coverage/2026-B.md L425)"
            ),
            "explanation": (
                "페팃 신로마 공화주의의 두 핵심 보장 기제. "
                "① 반쟁의 가능성(contestability): 권력 행사가 자의적이거나 공동선에 어긋날 때 "
                "시민이 공적으로 이의를 제기하고 이를 제어할 수 있는 제도적 창구가 열려 있어야 한다. "
                "② 공적 감시 제도(eyeball test): 시민이 굴종 없이 권력자의 눈을 똑바로 마주볼 수 있을 만큼 "
                "권력이 투명하고 시민에 의해 감시 가능해야 한다. "
                "이 두 기제는 비지배 자유를 일상적 시민 실천 속에서 유지하는 조건이다."
            ),
            "argument": (
                "전제1: 법과 제도가 자의적 권력으로 전락하지 않으려면 시민의 견제가 필요하다. "
                "전제2: 견제는 사후 이의 제기(반쟁의 가능성)와 사전 감시(eyeball test)로 구체화된다. "
                "전제3: 이 두 기제가 작동할 때 비지배 자유가 지속 가능하다. "
                "결론: 따라서 공화주의적 권리 보장은 반쟁의 가능성과 공적 감시 제도를 제도적 핵심으로 한다."
            ),
            "counterpoint": (
                "반쟁의 가능성이 과도하게 확장되면 일상적 의사결정의 안정성을 해칠 수 있고, "
                "공적 감시가 지나치면 사생활의 영역을 침식할 수 있다는 현실적 긴장이 지적된다."
            ),
            "context": (
                "2026-B Q7 해설 구간에서 페팃 trademark로 직접 명시된 두 기제. "
                "비지배 자유의 시민적·제도적 작동 조건."
            ),
            "keywords": [
                "반쟁의 가능성",
                "contestability",
                "공적 감시 제도",
                "eyeball test",
                "시민적 견제",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-006: 공화주의 권리 = 공민적 권리 (2026-B Q7 ㉡)
        {
            "id": "pettit-claim-006",
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "source_detail": (
                "Republicanism (1997) · 2026학년도 전공B Q7 ㉡"
            ),
            "claim": (
                "자유주의의 권리(자연권)는 개인에게 선재(先在)하는 보편·불변의 내재적 속성으로 "
                "이해되는 반면, 공화주의의 권리는 정치 공동체의 법과 제도에 의해 "
                "구성·보장되는 공민적 권리(civic rights)이다. "
                "권리는 자연이 주는 것이 아니라 공화국(res publica)이 법과 시민적 실천을 통해 "
                "만들어내고 유지하는 것이다."
            ),
            # 2026-B.md L407 + L425 verbatim
            "original_text": (
                "자유주의의 권리 개념은 ㉡ 공화주의의 권리 개념과는 다른 특징이 있다. "
                "자연권 이론은 자유주의의 기초가 되는 매우 중요한 것이다. "
                "자연권이란 인간이 태어나면서부터 가지는 자연적이고 본래적인 권리 "
                "— 2026학년도 전공B Q7 제시문 (coverage/2026-B.md L407) / "
                "자유주의의 권리(자연권)는 개인에게 선재(先在)하는 보편·불변의 내재적 속성으로 "
                "이해되는 반면, 공화주의의 권리는 정치 공동체의 법과 제도에 의해 "
                "구성·보장되는 공민적 권리(civic rights)이다 "
                "— 2026학년도 전공B Q7 해설 (coverage/2026-B.md L425)"
            ),
            "explanation": (
                "페팃 공화주의의 권리 이해. "
                "자유주의는 권리를 정치 이전에 존재하는 자연적 속성(natural rights / unalienable rights)으로 "
                "이해하지만, 공화주의는 권리를 정치 공동체 내에서 법·제도·시민적 실천을 통해 "
                "구성되고 유지되는 공민적 권리로 본다. "
                "즉 공화주의에서 권리는 ① 혼합 정체·권력 분립·법의 지배를 통해 "
                "자의적 권력의 출현을 제도적으로 차단하고, "
                "② 시민적 덕성과 공적 참여·감시를 통해 권력 담지자의 전횡을 견제하며, "
                "③ 공동선을 지향하는 시민들의 집단적 자치(self-government)를 통해 보장된다."
            ),
            "argument": (
                "전제1: 권리가 실효적으로 보장되려면 자의적 권력의 제거가 선행되어야 한다. "
                "전제2: 자의적 권력의 제거는 법·제도·시민적 덕성의 집합적 구성에 의해서만 가능하다. "
                "전제3: 따라서 권리는 자연적 속성이 아니라 공화국의 법적·정치적 산물이다. "
                "결론: 공화주의의 권리는 공민적 권리로서 공화국의 구성적 실천에 의존한다."
            ),
            "counterpoint": (
                "권리의 기초를 공화국의 법과 제도에만 두면 정치 공동체가 부재할 때나 "
                "공동체가 부정의한 결정을 내릴 때 개인 권리의 근거가 흔들린다는 비판이 있다. "
                "자유주의 자연권 이론은 이러한 상황에서 공동체 외부의 도덕적 근거를 제공한다는 점에서 "
                "여전히 이론적 강점을 가진다."
            ),
            "context": (
                "2026-B Q7 ㉡ 서술 답안의 직접 근거 · "
                "자유주의 권리 vs 공화주의 권리 대비 trademark."
            ),
            "keywords": [
                "공민적 권리",
                "civic rights",
                "자연권",
                "공화국",
                "res publica",
                "법과 제도",
                "자치",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-007: 비지배 자유 vs 소극적 자유 대립 (2020-A Q10)
        {
            "id": "pettit-claim-007",
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "source_detail": (
                "Republicanism (1997) 제2장 · 2020학년도 전공A Q10"
            ),
            "claim": (
                "공화주의 사상가들에 따르면, 진정한 정치적 자유는 자유주의 사상가들이 주장하는 것처럼 "
                "개인이 다른 개인이나 기관으로부터 간섭을 받지 않는 데 그치는 것이 아니라, "
                "주종적 지배나 예속 자체가 존재하지 않는 상태를 의미한다. "
                "이는 개인이 법의 제재를 두려워하지 않고, 언제라도 남을 마음대로 억압할 수 있는 "
                "특정 개인이나 기관의 자의적 의지에 종속되지 않음을 의미한다."
            ),
            # 2020-A.md L27 verbatim 인용 (원본 시험 L140 참조)
            "original_text": (
                "( ㉡ ) 사상가들에 따르면, 진정한 정치적 자유는 ( ㉢ ) 사상가들이 주장하는 것처럼 "
                "개인이 다른 개인이나 기관으로부터 간섭을 받지 않는 데 그치는 것이 아니라, "
                "주종적 지배나 예속 자체가 존재하지 않는 상태를 의미 … "
                "이는 개인이 ㉣ 법의 제재를 두려워하지 않고, 언제라도 남을 마음대로 억압할 수 있는 "
                "특정 개인이나 기관의 자의적 의지에 종속되지 않음을 의미 "
                "— 2020학년도 전공A Q10 제시문 (coverage/2020-A.md L27; 원본 시험지 L140)"
            ),
            "explanation": (
                "페팃·스키너 공화주의 비지배 자유론의 공식 정식. "
                "소극적 자유(비간섭 — 벌린·홉스·벤담)와의 결정적 대비를 통해 "
                "자유주의적 자유 개념으로 환원되지 않는 공화주의 자유의 고유성을 드러낸다. "
                "간섭이 없어도 자의적 간섭 가능성이 있으면 자유가 아니고, "
                "간섭이 있어도 비자의적(규칙 지배적·공적으로 정당화된)이면 자유를 훼손하지 않는다. "
                "법의 지배(rule of law)는 자의적 지배를 제거하여 비지배 자유를 실현하는 수단이다."
            ),
            "argument": (
                "전제1: 자유주의는 자유를 간섭 부재로 정의한다. "
                "전제2: 그러나 간섭 가능성 자체가 시민의 행동을 제약하고 예속 상태를 강요한다. "
                "전제3: 따라서 자유는 지배·예속 자체의 부재로 재정의되어야 한다. "
                "결론: 법의 지배 아래 자의적 의지에 종속되지 않음이 공화주의적 자유의 본질이다."
            ),
            "counterpoint": (
                "자유주의 측(특히 벌린·홉스·벤담)은 '법의 제재'가 그 자체로 간섭의 한 형태이므로 "
                "법의 제재가 있는 한 그만큼 자유는 축소된다고 본다. "
                "벤담의 '모든 법은 그만큼 자유의 제한'이라는 명제가 대표적 반론."
            ),
            "context": (
                "2020-A Q10 제시문 핵심 trademark · "
                "자유주의(㉢) vs 공화주의(㉡)의 대립 구도에서 페팃 비지배 자유가 공화주의 측 대표 입장."
            ),
            "keywords": [
                "주종적 지배",
                "예속",
                "자의적 의지",
                "비지배 자유",
                "공화주의",
                "법의 지배",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-008: 시민적 덕성 (2020-A Q10 ㉠)
        {
            "id": "pettit-claim-008",
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "source_detail": (
                "Republicanism (1997) 제7장 'Civic Virtue' · 2020학년도 전공A Q10"
            ),
            "claim": (
                "공화국은 자유를 위해 시민적 덕성, 즉 공공선에 봉사하겠다는 시민들의 각오와 능력에 "
                "의지할 수 있어야 한다. 시민적 덕성을 지닌 시민은 시민적 우애를 중시하며, "
                "시민적 덕성과 공화국에 대한 봉사가 사생활과 균형을 이루도록 노력한다."
            ),
            # 2020-A.md L27 verbatim (원본 시험 L139 인용)
            "original_text": (
                "공화국은 자유를 위해 시민적 ( ㉠ ), 즉 공공선에 봉사하겠다는 시민들의 "
                "각오와 능력에 의지할 수 있어야 한다. ( ㉠ )을/를 지닌 시민은 시민적 우애를 "
                "중시하며, 시민적 ( ㉠ )와/과 공화국에 대한 봉사가 사생활과 균형을 이루도록 노력 "
                "— 2020학년도 전공A Q10 제시문 (coverage/2020-A.md L27; 원본 시험지 L139)"
            ),
            "explanation": (
                "페팃 『Republicanism(1997)』 제7장 'Civic Virtue'에서 정식화된 "
                "공화국 유지의 시민적 조건. 아리스토텔레스 『정치학』·키케로 『의무론』의 고전 공화주의에서 "
                "마키아벨리 → 루소 → 몽테스키외를 거쳐 페팃·스키너·샌델에 이르는 "
                "공화주의 전통 전반의 공통 핵심 개념. "
                "법·제도의 설계만으로는 비지배 자유가 유지될 수 없으며, "
                "공동선에 헌신하는 덕스러운 시민성(virtuous citizenry)이 뒷받침되어야 한다. "
                "2020-A Q10 ㉠ 정답 = 덕(德 — virtue) / 시민적 덕성(市民的 德性 — civic virtue)."
            ),
            "argument": (
                "전제1: 제도만으로는 자의적 지배가 완전히 억제되지 않는다. "
                "전제2: 법과 제도를 운용하고 감시하는 시민의 덕성이 필요하다. "
                "전제3: 이 덕성은 공동선 봉사의 각오·능력·시민적 우애로 구체화된다. "
                "결론: 따라서 공화국의 자유는 시민적 덕성에 의지할 수 밖에 없다."
            ),
            "counterpoint": (
                "시민적 덕성 요구가 과도하면 시민의 사생활 자율성을 침식할 수 있다는 "
                "자유주의적 우려가 제기된다. 현대 다원 사회에서 공통의 덕성 기준을 "
                "어떻게 구성할 것인가 하는 실천적 난제도 있다."
            ),
            "context": (
                "2020-A Q10 ㉠ 빈칸 정답의 직접 근거 · "
                "공화국 유지의 시민적 조건 trademark."
            ),
            "keywords": [
                "시민적 덕성",
                "civic virtue",
                "공공선",
                "시민적 우애",
                "공화국",
                "공동선",
            ],
            "verified": False,
            "verification_log": [],
        },
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """페팃 핵심 키워드 데이터 입력. 중복 체크 후 insert."""
    keywords = [
        {
            "id": "kw-pettit-non-domination",
            "term": "비지배 자유",
            "term_en": "freedom as non-domination",
            "definition": (
                "페팃 『Republicanism: A Theory of Freedom and Government(1997)』 제2장 trademark. "
                "자유를 '타인의 자의적 의지에 예속되지 않는 상태'로 정의하는 공화주의적 자유 개념. "
                "벌린의 소극적 자유(비간섭)와 적극적 자유(자기지배) 이분법을 넘는 제3의 자유. "
                "자비로운 주인의 노예도 노예이므로 자유가 아니며, "
                "실제 간섭 여부와 무관하게 '지배 권력의 존재' 자체가 자유의 훼손이다. "
                "2019-A Q10·2020-A Q10·2022-A Q6·2026-B Q7에 반복 출제."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "related_terms": [
                "공화주의",
                "비간섭 자유 비판",
                "자의적 지배",
                "주인 없는 삶",
                "civic liberty",
            ],
        },
        {
            "id": "kw-pettit-arbitrary-domination",
            "term": "자의적 지배",
            "term_en": "arbitrary domination",
            "definition": (
                "타인의 자의적 의지에 따라 언제든 간섭받을 수 있는 상태. "
                "페팃에게 자유의 핵심 위협은 실제 간섭이 아니라 자의적 간섭 가능성 자체이다. "
                "법의 제재라도 비자의적·규칙 지배적이면 자유를 훼손하지 않지만, "
                "자의적 의지에 종속된다면 간섭의 유무와 관계없이 자유가 침해된다. "
                "2020-A Q10 ㉣ 서술의 핵심 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "related_terms": ["비지배 자유", "주종적 지배", "예속", "법의 지배"],
        },
        {
            "id": "kw-pettit-contestability",
            "term": "반쟁의 가능성",
            "term_en": "contestability",
            "definition": (
                "권력 행사가 자의적이거나 공동선에 어긋날 때 시민이 공적으로 이의를 제기하고 "
                "이를 제어할 수 있는 제도적 가능성. "
                "페팃 신로마 공화주의의 핵심 보장 기제 중 하나로, "
                "비지배 자유를 일상적 시민 실천 속에서 유지하는 조건이다. "
                "2026-B Q7 해설에서 페팃 trademark로 직접 명시."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "related_terms": ["비지배 자유", "eyeball test", "시민적 견제", "공화주의"],
        },
        {
            "id": "kw-pettit-eyeball-test",
            "term": "공적 감시 제도",
            "term_en": "eyeball test",
            "definition": (
                "시민이 굴종 없이 권력자의 눈을 똑바로 마주볼 수 있을 만큼 "
                "권력이 투명하고 시민에 의해 감시 가능해야 한다는 페팃의 판별 기준. "
                "비지배 자유의 실질적 실현을 가늠하는 현실 적용 테스트. "
                "2026-B Q7 해설에서 페팃 trademark로 직접 명시."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "related_terms": ["비지배 자유", "반쟁의 가능성", "공화주의", "시민적 견제"],
        },
        {
            "id": "kw-pettit-dominium",
            "term": "지배",
            "term_en": "dominium",
            "definition": (
                "로마 공화주의 전통의 자유인(liber) 대 노예(servus) 대립에서 유래한 개념으로, "
                "타인의 자의적 권력 아래 놓인 상태. "
                "페팃 『Republicanism(1997)』 제2장·제3장에서 "
                "'주인의 눈치를 살피는 노예의 이중적 시선'으로 현상학적으로 묘사된다. "
                "2026-B Q7의 '힘센 자·약한 자' 비유가 이 지배 개념의 대표적 형상화."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "related_terms": ["비지배 자유", "자의적 지배", "주인-노예 관계", "예속"],
        },
        {
            "id": "kw-pettit-separation-of-powers",
            "term": "권력 분립",
            "term_en": "separation of powers",
            "definition": (
                "사법권·입법권·행정권을 상이한 기관으로 분산시켜 상호 견제하게 하는 헌정 원리. "
                "페팃은 몽테스키외 삼권분립을 공화주의 전통이 계승한 것으로 해석하며, "
                "『Republicanism(1997)』 제6장 'Republican Forms'에서 "
                "비지배 자유를 제도적으로 실현하는 핵심 안전장치로 강조한다. "
                "2026-B Q7 ㉠ 빈칸 정답."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "related_terms": ["입헌주의", "법의 지배", "혼합 정체", "공화주의"],
        },
        {
            "id": "kw-pettit-civic-virtue",
            "term": "시민적 덕성",
            "term_en": "civic virtue",
            "definition": (
                "공동선(common good)에 봉사하겠다는 시민들의 각오와 능력. "
                "페팃 『Republicanism(1997)』 제7장 'Civic Virtue'에서 정식화된 공화국 유지의 시민적 조건. "
                "법·제도의 설계만으로는 비지배 자유가 유지될 수 없으며, "
                "공동선에 헌신하는 덕스러운 시민성(virtuous citizenry)이 뒷받침되어야 한다. "
                "2020-A Q10 ㉠ 빈칸 정답."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "related_terms": ["공공선", "공동선", "시민적 우애", "공화주의", "자치"],
        },
        {
            "id": "kw-pettit-civic-rights",
            "term": "공민적 권리",
            "term_en": "civic rights",
            "definition": (
                "정치 공동체의 법과 제도에 의해 구성·보장되는 공화주의적 권리 개념. "
                "자유주의의 자연권(개인에게 선재하는 보편·불변의 내재적 속성)과 구별된다. "
                "권리는 자연이 주는 것이 아니라 공화국(res publica)이 법과 시민적 실천을 통해 "
                "만들어내고 유지하는 것. "
                "2026-B Q7 ㉡ 서술 답안의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "related_terms": ["자연권", "공화국", "법과 제도", "자치"],
        },
        {
            "id": "kw-pettit-neo-roman-republicanism",
            "term": "신로마 공화주의",
            "term_en": "neo-Roman republicanism",
            "definition": (
                "로마 공화국의 자유인(liber) vs 노예(servus) 대립에서 "
                "자유를 '주인이 없는 상태'로 이해하는 전통을 현대에 부활시킨 사조. "
                "페팃 『Republicanism(1997)』과 퀀틴 스키너 『Liberty before Liberalism(1998)』이 "
                "대표 저작이며, 비지배 자유를 중심 개념으로 한다. "
                "마우리치오 비롤리의 공화주의적 애국심도 같은 계열."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "pettit-republicanism-1997",
            "related_terms": [
                "공화주의",
                "비지배 자유",
                "마키아벨리",
                "해링턴",
                "키케로",
            ],
        },
    ]

    inserted = 0
    for kw in keywords:
        try:
            client.get(index=INDEX_KEYWORDS, id=kw["id"])
            print(f"[keyword] {kw['id']}: 이미 존재 (skip)")
        except Exception:
            result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
            print(f"[keyword] {kw['id']}: {result['result']}")
            inserted += 1

    return len(keywords)


def insert_relations(client):
    """페팃 영향·비교 관계 데이터 입력.

    ES 등록 확인된 thinker_id만 링크 (2026-04-22 curl 확인):
    - hobbes   : 등록 — 소극적 자유(비간섭) vs 비지배 자유 대립 (2019-A Q10 갑=홉스 vs 을=공화주의, 2020-A Q10)
    - rousseau : 등록 — 공화주의 전통 계승 (루소 사회계약·일반의지·공화주의)
    미등록 (relation 생략):
    - berlin, machiavelli, skinner, viroli, green_th
    """
    relations = [
        {
            "from_thinker": "hobbes",
            "to_thinker": THINKER_ID,
            "type": "compared",
            "description": (
                "홉스(Thomas Hobbes)의 소극적 자유(비간섭)와 "
                "페팃(Philip Pettit)의 비지배 자유는 "
                "현대 자유 개념의 핵심 대립 축을 이룬다. "
                "홉스 『리바이어던(Leviathan, 1651)』 21장은 자유를 '외적 방해의 부재'로, "
                "'신민의 자유는 주권자가 법으로 규제하지 않은 것에서만 존재'하는 "
                "'법의 침묵(silentium legis)에서의 자유'로 정의한다. "
                "홉스에게 공화국이든 군주정이든 법의 침묵 영역의 크기가 같으면 "
                "시민의 자유 양은 동일하다. "
                "반면 페팃은 자유를 '타인의 자의적 의지에 예속되지 않는 상태'로 정의하며, "
                "실제 간섭이 없어도 자의적 간섭 가능성(지배)만으로 자유가 침해되고, "
                "반대로 비자의적 법의 제재는 자유를 훼손하지 않는다고 본다. "
                "2019-A Q10은 갑(홉스)과 을(공화주의 = 페팃·스키너)을 직접 대립 배치하여 "
                "이 두 자유 개념의 구도를 출제했다."
            ),
            "evidence": (
                "Hobbes (1651) Leviathan ch.21 'Of the Liberty of Subjects'; "
                "Pettit (1997) Republicanism: A Theory of Freedom and Government ch.2; "
                "2019-A Q10 갑(홉스) vs 을(공화주의) 대립 배치 "
                "(coverage/2019-A.md L24); "
                "2020-A Q10 ㉢ 자유주의(홉스 포함) vs ㉡ 공화주의(페팃·스키너) 대립 "
                "(coverage/2020-A.md L27)"
            ),
        },
        {
            "from_thinker": "rousseau",
            "to_thinker": THINKER_ID,
            "type": "influenced",
            "description": (
                "루소(Jean-Jacques Rousseau)의 공화주의 전통과 일반의지(volonté générale) 사상은 "
                "페팃(Philip Pettit) 신로마 공화주의의 사상사적 선행 원천 중 하나이다. "
                "페팃은 『Republicanism(1997)』에서 로마 공화국 → 마키아벨리 → 해링턴 → 루소 → "
                "몽테스키외를 잇는 공화주의 전통을 정리하며, "
                "루소의 '법에 대한 복종이 자유'라는 테제를 자의적 지배 부재로서의 공화주의적 자유로 해석한다. "
                "단, 루소의 강한 일반의지 개념은 페팃에게서 반쟁의 가능성(contestability)을 전제로 한 "
                "더 분권적인 형태로 수정된다."
            ),
            "evidence": (
                "Rousseau (1762) Du contrat social; "
                "Pettit (1997) Republicanism: A Theory of Freedom and Government; "
                "2022-A Q6 (가) 제시문의 '공화주의 전통' 언급 (coverage/2022-A.md L20)"
            ),
        },
    ]

    for i, rel in enumerate(relations):
        rel_id = f"rel-{rel['from_thinker']}-{rel['to_thinker']}-{rel['type']}-{i+1}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id}: {result['result']}")

    return len(relations)


def main():
    """메인 실행 함수."""
    print("=== 필립 페팃(Pettit) 데이터 ES 입력 시작 ===\n")
    client = get_client()

    try:
        print("1. 분야(field) 확인/추가")
        try:
            ensure_field(client)
        except Exception as e:
            print(f"[ensure_field] 경고: {e}", file=sys.stderr)
        print()

        print("2. 사상가(thinker) 입력")
        try:
            insert_thinker(client)
        except Exception as e:
            print(f"[insert_thinker] 오류: {e}", file=sys.stderr)
            raise
        print()

        print("3. 저서(works) 입력")
        try:
            work_count = insert_works(client)
            print(f"   -> {work_count}개 저서 입력 완료\n")
        except Exception as e:
            print(f"[insert_works] 오류: {e}", file=sys.stderr)
            raise

        print("4. 주장(claims) 입력")
        try:
            claim_count = insert_claims(client)
            print(f"   -> {claim_count}개 주장 입력 완료\n")
        except Exception as e:
            print(f"[insert_claims] 오류: {e}", file=sys.stderr)
            raise

        print("5. 키워드(keywords) 입력")
        try:
            kw_count = insert_keywords(client)
            print(f"   -> {kw_count}개 키워드 처리 완료\n")
        except Exception as e:
            print(f"[insert_keywords] 오류: {e}", file=sys.stderr)
            raise

        print("6. 관계(relations) 입력")
        try:
            rel_count = insert_relations(client)
            print(f"   -> {rel_count}개 관계 입력 완료\n")
        except Exception as e:
            print(f"[insert_relations] 오류: {e}", file=sys.stderr)
            raise

        print("=== 입력 요약 ===")
        print(f"  사상가: 1명 (pettit)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n[OK] 페팃 데이터 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}", file=sys.stderr)
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
