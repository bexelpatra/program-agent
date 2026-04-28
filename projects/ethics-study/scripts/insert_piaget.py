"""장 피아제(Jean Piaget) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS, INDEX_FIELDS
)


def ensure_field(client):
    """도덕발달 분야가 ethics-fields 인덱스에 없으면 추가."""
    try:
        client.get(index=INDEX_FIELDS, id="moral_development")
        print("[field] moral_development: 이미 존재")
    except Exception:
        doc = {
            "id": "moral_development",
            "name": "도덕발달론",
            "description": (
                "아동 및 인간의 도덕 판단과 도덕 행동이 어떻게 발달하는지를 탐구하는 분야. "
                "피아제의 인지발달 기반 도덕발달 이론, 콜버그의 도덕발달 단계론, "
                "길리건의 배려윤리, 나딩스의 배려교육론 등을 포함한다. "
                "도덕심리학, 도덕교육론과 밀접하게 연관되며 임용시험 핵심 영역이다."
            ),
            "order": 4
        }
        result = client.index(index=INDEX_FIELDS, id="moral_development", document=doc)
        print(f"[field] moral_development: {result['result']}")


def insert_thinker(client):
    """피아제 사상가 데이터 입력."""
    doc = {
        "id": "piaget",
        "name": "장 피아제",
        "name_en": "Jean Piaget",
        "field": "moral_development",
        "era": "현대",
        "birth_year": 1896,
        "death_year": 1980,
        "background": (
            "스위스 뇌샤텔에서 태어난 피아제는 어린 시절부터 자연과학에 비범한 재능을 보여 "
            "10세에 흰 참새에 관한 논문을 발표했다. 뇌샤텔 대학교에서 생물학을 전공하여 21세에 박사학위를 받았다. "
            "이후 취리히, 파리 소르본에서 심리학과 철학을 연구하면서 "
            "비네(Alfred Binet)의 지능 검사 표준화 작업에 참여했는데, "
            "아이들의 틀린 답변에서 보이는 체계적 패턴에서 인지 발달 연구의 실마리를 발견했다. "
            "제네바 대학교 루소 연구소에서 오랜 기간 연구하면서 아동의 인지 발달과 도덕 발달을 "
            "방대한 임상적 관찰과 실험을 통해 탐구했다. "
            "1932년 출간한 '아동의 도덕 판단(The Moral Judgment of the Child)'은 "
            "도덕발달론의 초석이 되었으며, 콜버그, 길리건 등 후속 연구자들에게 결정적 영향을 미쳤다. "
            "피아제는 심리학자임과 동시에 인식론자로서, 지식의 발달을 철학적으로 탐구하는 "
            "'발생론적 인식론(genetic epistemology)'의 창시자이기도 하다."
        ),
        "core_philosophy": (
            "피아제 도덕발달론의 핵심은 아동의 도덕적 이해가 타율적 도덕성(heteronomous morality)에서 "
            "자율적 도덕성(autonomous morality)으로 발달한다는 것이다. "
            "타율적 도덕성은 규칙을 어른이 부과한 고정불변의 것으로 여기고, "
            "행동의 결과(물질적 피해)로 잘못을 판단하며, 위반에는 속죄적 처벌(expiatory punishment)이 따른다고 믿는다. "
            "자율적 도덕성은 규칙을 사회적 합의로 이해하고, 행동의 의도(intention)로 옳고 그름을 판단하며, "
            "처벌은 규칙 위반과 논리적으로 연관된 보상적·상호적 처벌(reciprocal punishment)이어야 한다고 본다. "
            "이 발달은 아동의 인지 발달, 특히 자기중심성(egocentrism)의 극복과 탈중심화(decentration)에 달려 있으며, "
            "또래 간 협동(peer cooperation)과 상호적 존경(mutual respect)이 핵심 동인이다. "
            "교육적으로 피아제는 일방적 규칙 부과보다 협동적 활동과 자기 규율을 강조했다."
        ),
        "philosophical_journey": (
            "초기(1920년대): 아동의 언어와 사고, 세계관, 인과성 등에 관한 임상 관찰 연구를 수행했다. "
            "아이들이 어른과는 질적으로 다른 방식으로 세계를 이해함을 발견했다. "
            "중기(1930년대): 1932년 '아동의 도덕 판단'을 출간하여 도덕발달 연구의 체계를 세웠다. "
            "구슬치기 놀이 규칙 연구, 거짓말 연구, 처벌 개념 연구 등을 통해 "
            "도덕적 실재론에서 도덕적 상대주의로의 발달을 기술했다. "
            "인지발달 이론기(1940~60년대): 감각운동기, 전조작기, 구체적 조작기, 형식적 조작기의 "
            "인지발달 단계론을 체계화했다. 동화(assimilation), 조절(accommodation), "
            "평형화(equilibration) 등 인지 발달 메커니즘을 정교화했다. "
            "발생론적 인식론기(1960~80년대): 제네바 국제발생론적인식론연구소를 설립하고(1955), "
            "수학, 논리학, 물리학 등 지식의 발달을 철학적으로 탐구했다. "
            "피아제의 도덕발달 이론은 콜버그에 의해 정교화되고 확장되었으며, "
            "길리건에 의해 배려 윤리 관점에서 비판받았다."
        ),
        "keywords": [
            "도덕적 실재론",
            "자율적 도덕성",
            "타율적 도덕성",
            "내재적 정의",
            "상호적 존경",
            "일방적 존경",
            "인지발달",
            "탈중심화",
            "동화와 조절",
            "자기중심성",
            "협동",
            "속죄적 처벌",
            "보상적 처벌",
            "발생론적 인식론"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="piaget", document=doc)
    print(f"[thinker] piaget: {result['result']}")
    return result


def insert_works(client):
    """피아제 저서 데이터 입력."""
    works = [
        {
            "id": "piaget-moral-judgment",
            "thinker_id": "piaget",
            "title": "아동의 도덕 판단",
            "title_original": "The Moral Judgment of the Child",
            "year": 1932,
            "significance": (
                "피아제 도덕발달론의 핵심 저작으로, 도덕발달 연구의 출발점이 되었다. "
                "구슬치기 규칙 관찰, 이야기 제시를 통한 실험, 아동 면접 등 방대한 임상 연구에 기반하여 "
                "아동의 도덕 판단이 타율적 도덕성에서 자율적 도덕성으로 발달함을 기술했다. "
                "도덕적 실재론(moral realism), 내재적 정의(immanent justice), "
                "의도 vs 결과 판단, 처벌 개념, 분배적 정의, 규칙에 대한 인식 등 "
                "핵심 주제들을 체계적으로 다루었다. "
                "콜버그 도덕발달 단계론의 직접적 선구가 된 저작이다."
            ),
            "key_concepts": [
                "도덕적 실재론", "자율적 도덕성", "타율적 도덕성",
                "내재적 정의", "속죄적 처벌", "보상적 처벌",
                "의도와 결과", "분배적 정의", "협동"
            ]
        },
        {
            "id": "piaget-origins-of-intelligence",
            "thinker_id": "piaget",
            "title": "아동의 지능의 기원",
            "title_original": "The Origins of Intelligence in Children",
            "year": 1936,
            "significance": (
                "감각운동기(sensorimotor stage)의 발달을 상세히 기술한 저작. "
                "생후 2년간 아기의 행동 관찰을 통해 지능이 어떻게 발생하는지를 탐구했다. "
                "도식(schema), 동화(assimilation), 조절(accommodation), 평형화(equilibration) 등 "
                "피아제 인지발달 이론의 핵심 개념들이 처음으로 체계화된 저작이다. "
                "도덕발달을 이해하는 데 필수적인 인지발달 이론의 토대를 제공한다."
            ),
            "key_concepts": [
                "감각운동기", "도식", "동화", "조절", "평형화", "대상 영속성"
            ]
        },
        {
            "id": "piaget-psychology-of-intelligence",
            "thinker_id": "piaget",
            "title": "지능의 심리학",
            "title_original": "The Psychology of Intelligence",
            "year": 1947,
            "significance": (
                "피아제 인지발달 이론의 이론적 종합을 담은 저작. "
                "감각운동기, 전조작기, 구체적 조작기, 형식적 조작기의 4단계 인지발달론을 제시했다. "
                "지능을 생물학적 적응의 특수한 형태로 규정하고, "
                "동화·조절·평형화의 메커니즘으로 인지 발달을 설명했다. "
                "도덕발달 이론의 인지발달론적 기반을 제공한다."
            ),
            "key_concepts": [
                "전조작기", "구체적 조작기", "형식적 조작기",
                "자기중심성", "보존 개념", "가역성"
            ]
        },
        {
            "id": "piaget-science-of-education",
            "thinker_id": "piaget",
            "title": "교육학과 심리학",
            "title_original": "Science of Education and the Psychology of the Child",
            "year": 1969,
            "significance": (
                "피아제가 자신의 심리학 이론을 교육에 적용한 저작. "
                "전통적 교수법(교사 중심, 일방적 지식 전달)의 한계를 비판하고, "
                "아동의 능동적 탐구와 협동학습을 강조하는 진보주의 교육을 지지했다. "
                "도덕교육에서도 일방적 훈육이 아닌 상호 존중과 협동을 통한 자율적 도덕성 발달을 강조했다."
            ),
            "key_concepts": [
                "능동적 학습", "협동학습", "자율성", "진보주의 교육"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """피아제 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 타율적 도덕성 → 자율적 도덕성 발달 단계
        {
            "id": "piaget-claim-001",
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "source_detail": "The Moral Judgment of the Child, Chapter 1",
            "claim": (
                "아동의 도덕 발달은 타율적 도덕성(heteronomous morality)에서 "
                "자율적 도덕성(autonomous morality)으로 이행하는 두 단계를 거친다. "
                "약 10세 이전의 아동은 타율적 도덕성의 단계로, 규칙을 성인이 부과한 "
                "고정불변의 신성한 것으로 보며, 행동의 결과(피해의 크기)로 잘못을 판단한다. "
                "10세 이후에는 자율적 도덕성의 단계로, 규칙을 사회적 합의로 이해하고 "
                "의도(intention)에 따라 도덕 판단을 내린다."
            ),
            "original_text": (
                "We have thus been led to recognize the existence of two distinct moralities in the child, "
                "or rather of two periods in the moral development of the child. "
                "There is first the morality that is a characteristic product of unilateral respect, "
                "where there is constraint and the obligatory element is due to authority — "
                "a morality of heteronomy. And there is a morality in which the fundamental rule is "
                "the principle of reciprocity — a morality of autonomy."
            ),
            "original_text_ko": (
                "우리는 아동에게서 두 가지 뚜렷한 도덕성, "
                "즉 아동 도덕 발달의 두 시기가 있음을 인식하게 되었다. "
                "첫째는 일방적 존경의 특징적 산물인 도덕성으로, 강제와 권위에서 비롯된 의무감을 가지는 "
                "타율적 도덕성이다. 둘째는 상호성의 원리가 근본 규칙인 도덕성, 즉 자율적 도덕성이다."
            ),
            "explanation": (
                "피아제는 아동의 도덕 발달을 두 단계로 구분한다. "
                "타율적 도덕성(도덕적 실재론, 약 5~10세): 규칙은 성인에 의해 부여된 절대적·불변의 것. "
                "행동의 물질적 결과(피해량)로 잘못을 판단(객관적 책임). 위반에는 반드시 처벌이 따름(내재적 정의 신념). "
                "자율적 도덕성(도덕적 상대주의, 약 10세 이후): 규칙은 상호 합의로 만들어지며 변경 가능. "
                "행동의 의도(주관적 책임)로 판단. 처벌은 위반과 논리적으로 연관된 것이어야 함."
            ),
            "argument": (
                "(1) 피아제는 아동들이 구슬치기 규칙을 어떻게 이해하는지 관찰했다. 어린 아동은 규칙을 "
                "어른이 만든 불변의 것으로 보고, 큰 아동은 규칙을 합의로 변경할 수 있다고 인식했다. "
                "(2) 클루치 이야기(큰 피해 vs 작은 피해) 실험에서 어린 아동은 의도와 무관하게 "
                "더 큰 피해를 입힌 쪽이 더 나쁘다고 판단했다. "
                "(3) 이 차이는 인지 발달(특히 자기중심성의 극복)과 사회적 경험(또래와의 협동)에 의해 설명된다."
            ),
            "counterpoint": (
                "콜버그는 피아제의 두 단계를 6단계로 정교화하여 확장했다. "
                "엘스테인(Elstein) 등의 후속 연구는 피아제의 연령 기준이 문화에 따라 다를 수 있음을 보였다. "
                "길리건은 피아제와 콜버그의 도덕발달론이 주로 소년을 연구 대상으로 하여 "
                "배려와 관계 중심의 여성적 도덕 발달을 간과했다고 비판했다. "
                "또한 일부 연구는 어린 아동도 의도를 이해할 수 있음을 보여 피아제의 연령 경계에 의문을 제기했다."
            ),
            "context": (
                "피아제는 아동을 단순히 무지한 어른으로 보는 시각에 반대하며, "
                "아동이 어른과는 질적으로 다른 방식으로 세계와 도덕을 이해한다는 것을 보이려 했다."
            ),
            "keywords": ["타율적 도덕성", "자율적 도덕성", "도덕 발달 단계", "규칙 인식"],
            "verified": False
        },
        # CLAIM-002: 도덕적 실재론(moral realism)
        {
            "id": "piaget-claim-002",
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "source_detail": "The Moral Judgment of the Child, Chapter 2",
            "claim": (
                "도덕적 실재론(moral realism)은 타율적 도덕성 단계 아동의 특징적 믿음으로, "
                "도덕 규칙은 성인의 권위에 의해 주어진 객관적·불변의 실재로서 "
                "인간의 의식이나 의도와 독립하여 존재한다고 여기는 태도이다. "
                "도덕적 실재론의 아동은 규칙 위반에 대한 책임을 행위자의 의도가 아니라 "
                "행위의 결과(객관적 피해의 크기)로 판단한다."
            ),
            "original_text": (
                "Moral realism is the tendency which the child has to regard duty and the value attaching to it "
                "as self-subsistent and independent of the mind, as imposing itself regardless of the circumstances "
                "in which the individual may find himself. Any act that shows obedience to a rule or even to an adult, "
                "regardless of what he may command, is good; any act that does not conform to rules is bad."
            ),
            "original_text_ko": (
                "도덕적 실재론은 아동이 의무와 그에 결부된 가치를 자기 완결적이고 마음으로부터 독립된 것으로, "
                "개인이 처한 상황에 무관하게 부과되는 것으로 여기는 경향이다. "
                "규칙이나 어른에 대한 복종을 보이는 행위는 그가 무엇을 명령하든 선이며, "
                "규칙을 따르지 않는 행위는 악이다."
            ),
            "explanation": (
                "도덕적 실재론은 세 가지 특징을 가진다. "
                "(1) 의무의 객관적·절대적 성격: 규칙은 마음과 무관하게 존재하는 절대적 명령이다. "
                "(2) 문자적 규칙 준수: 규칙의 정신이나 의도보다 문자 그대로의 준수를 중시한다. "
                "(3) 객관적 책임(objective responsibility): 피해의 크기로 잘못의 정도를 판단한다. "
                "이는 타율적 도덕성의 단계에서 나타나며, 아동이 성장하면서 점차 극복된다."
            ),
            "argument": (
                "(1) 어린 아동은 규칙을 '어른이 정해준 것'으로 신성시하며, 변경 불가능하다고 믿는다. "
                "(2) 이야기 실험에서 어린 아동은 의도가 좋았어도 큰 피해를 낸 아이를 "
                "의도가 나쁘지만 작은 피해를 낸 아이보다 더 나쁘다고 판단했다. "
                "(3) 이는 아동의 자기중심성 때문에 다른 사람의 관점(의도)을 파악하지 못하기 때문이다."
            ),
            "counterpoint": (
                "후속 연구들은 3~4세 유아도 의도를 어느 정도 이해할 수 있음을 보여, "
                "피아제의 객관적 책임 판단이 과도하게 일반화되었을 수 있음을 시사했다. "
                "과제의 복잡성을 줄이면 어린 아동도 의도에 따라 판단할 수 있다는 연구 결과도 있다."
            ),
            "context": (
                "피아제는 아동의 규칙 이해를 연구하기 위해 구슬치기 게임의 규칙에 대한 면접과 "
                "다양한 도덕 이야기를 아동에게 들려주는 임상 실험 방법을 사용했다."
            ),
            "keywords": ["도덕적 실재론", "객관적 책임", "의도와 결과", "타율적 도덕성"],
            "verified": False
        },
        # CLAIM-003: 의도 vs 결과 판단
        {
            "id": "piaget-claim-003",
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "source_detail": "The Moral Judgment of the Child, Chapter 2, §2",
            "claim": (
                "도덕 판단의 발달은 행위의 결과(물질적 피해의 크기)를 기준으로 판단하는 "
                "객관적 책임(objective responsibility)에서 행위자의 의도(intention)를 "
                "기준으로 판단하는 주관적 책임(subjective responsibility)으로 이행한다. "
                "자율적 도덕성을 획득한 아동은 같은 행위라도 의도가 나쁘면 더 나쁘게, "
                "의도가 좋으면 덜 나쁘게 판단한다."
            ),
            "original_text": None,
            "original_text_ko": None,
            "explanation": (
                "피아제는 '클루치와 앙리' 이야기를 사용하여 이 판단을 연구했다. "
                "예: 클루치는 어머니를 도우려다 실수로 컵 15개를 깼고, "
                "앙리는 금지된 잼을 훔치려다 컵 1개를 깼다. "
                "어린 아동(타율적 단계)은 클루치(더 큰 피해)가 더 나쁘다고 판단했다. "
                "큰 아동(자율적 단계)은 앙리(나쁜 의도)가 더 나쁘다고 판단했다. "
                "이는 도덕 판단이 객관적 결과 중심에서 주관적 의도 중심으로 발달함을 보여준다."
            ),
            "argument": (
                "(1) 어린 아동은 타인의 마음 상태(의도)를 파악하는 능력이 부족하다(자기중심성). "
                "(2) 자기중심성이 극복되고 탈중심화가 이루어지면 타인의 관점에서 의도를 파악할 수 있다. "
                "(3) 또래와의 협동 관계에서 의도와 상황에 따라 규칙을 유연하게 적용하는 경험이 "
                "주관적 책임 판단 발달을 촉진한다."
            ),
            "counterpoint": (
                "일부 연구는 이야기의 복잡성을 단순화하면 어린 아동도 의도를 고려할 수 있음을 보였다. "
                "피아제의 실험 방법론 자체(복잡한 이야기 제시)가 어린 아동에게 불리했다는 비판이 있다. "
                "또한 문화에 따라 의도보다 결과를 중시하는 전통이 있어, "
                "이 발달 패턴이 보편적이지 않을 수 있다."
            ),
            "context": (
                "피아제는 두 아이가 각각 다른 의도로 행동하여 다른 크기의 피해를 낸 "
                "대비 이야기 쌍(paired stories)을 이용해 도덕 판단 발달을 연구했다."
            ),
            "keywords": ["객관적 책임", "주관적 책임", "의도", "결과", "도덕 판단"],
            "verified": False
        },
        # CLAIM-004: 규칙에 대한 인식 발달 4단계
        {
            "id": "piaget-claim-004",
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "source_detail": "The Moral Judgment of the Child, Chapter 1, §2-3",
            "claim": (
                "아동의 규칙에 대한 인식(consciousness of rules)은 4단계로 발달한다: "
                "(1) 순수 개인적·운동적 단계 — 규칙 없이 개인적 습관에 따라 놀이. "
                "(2) 자기중심적 단계 — 규칙을 모방하지만 혼자 놀며 규칙을 강제적이라 생각하지 않음. "
                "(3) 협동 단계 — 또래와의 상호 통제 시작, 규칙을 알지만 완전히 이해하지 못함. "
                "(4) 법전화 단계 — 규칙을 세세하게 알고 상호 합의로 변경 가능함을 인식."
            ),
            "original_text": None,
            "original_text_ko": None,
            "explanation": (
                "피아제는 구슬치기 게임의 규칙을 아동들이 어떻게 실행하고 이해하는지 관찰했다. "
                "규칙 실행(practice of rules)과 규칙 의식(consciousness of rules)은 "
                "다른 발달 경로를 따른다. 규칙 실행은 4단계(순수 운동 → 자기중심 → 협동 → 법전화)로, "
                "규칙 의식은 2단계(강제적·불변적 → 합의에 의한·변경 가능한)로 발달한다. "
                "어린 아동은 규칙을 실행하지 못하면서도 규칙을 신성불가침한 것으로 여긴다."
            ),
            "argument": (
                "(1) 구슬치기 규칙 관찰에서 어린 아동(2~5세)은 규칙 없이 개인적으로 놀거나 "
                "어른의 규칙을 자기 방식대로 해석했다. "
                "(2) 7~8세 아동은 또래와 게임을 하려 하지만 규칙을 완전히 이해하지 못한다. "
                "(3) 11~12세 아동은 규칙을 정확히 알고 합의에 의해 변경할 수 있음을 이해한다."
            ),
            "counterpoint": (
                "피아제의 구슬치기 연구가 주로 남아를 대상으로 했다는 점에서 "
                "여아의 규칙 발달 양상을 제대로 반영하지 못했다는 비판이 있다. "
                "또한 특정 게임에서 발견된 패턴이 모든 규칙 인식에 일반화될 수 있는지에 대한 의문도 있다."
            ),
            "context": (
                "피아제는 놀이와 규칙 연구를 도덕 발달 연구의 출발점으로 삼았다. "
                "놀이의 규칙을 통해 아동이 사회적 규범을 어떻게 내면화하는지를 파악하려 했다."
            ),
            "keywords": ["규칙 인식", "규칙 발달", "협동", "법전화"],
            "verified": False
        },
        # CLAIM-005: 내재적 정의(immanent justice)
        {
            "id": "piaget-claim-005",
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "source_detail": "The Moral Judgment of the Child, Chapter 4",
            "claim": (
                "내재적 정의(immanent justice)는 어린 아동의 믿음으로, "
                "규칙 위반 행위는 세계 자체로부터 자동적 처벌을 받는다는 신념이다. "
                "타율적 도덕성 단계의 아동은 불행이나 사고가 이전의 잘못에 대한 자동적 징벌이라고 믿는다. "
                "자율적 도덕성으로 발달하면서 이 믿음은 점차 사라진다."
            ),
            "original_text": (
                "What we have called 'immanent justice' consists in an automatic punishment emanating from "
                "things themselves. The child believes that nature itself will punish misdeeds."
            ),
            "original_text_ko": (
                "우리가 '내재적 정의'라고 부르는 것은 사물 자체로부터 나오는 자동적 처벌로 이루어진다. "
                "아동은 자연 자체가 잘못된 행위를 처벌할 것이라고 믿는다."
            ),
            "explanation": (
                "내재적 정의는 우주가 도덕적으로 질서 지어져 있다는 아니미즘적 믿음과 연결된다. "
                "예를 들어, '나쁜 일을 한 아이가 다리를 건너다 넘어지면, 그것이 벌인가?'라는 질문에 "
                "어린 아동들은 '그렇다, 나쁜 일 때문에 벌을 받은 것'이라 대답하는 경향이 있다. "
                "이 믿음은 도덕적 질서가 물리적 세계에 내재해 있다는 생각을 반영한다. "
                "자율적 도덕성이 발달하면 자연 현상은 도덕과 무관한 인과 관계를 따른다고 이해한다."
            ),
            "argument": (
                "(1) 어린 아동은 인과성과 도덕성을 아직 분리하지 못한다. "
                "(2) 권위(어른)에 대한 일방적 존경이 강할수록 규칙 위반에 반드시 처벌이 따른다는 믿음이 강해진다. "
                "(3) 협동과 상호적 관계를 경험하면서 자연 현상이 도덕과 무관하다는 것을 인식하게 된다."
            ),
            "counterpoint": (
                "이 믿음이 문화적으로 보편적인지에 대한 의문이 있다. "
                "일부 전통 문화에서는 성인도 자연의 징벌을 믿는 경우가 있으며, "
                "이는 발달 단계의 문제가 아니라 문화적 신념 체계의 문제일 수 있다."
            ),
            "context": (
                "피아제는 아동의 세계관이 아니미즘적·도덕적으로 질서 지어져 있다는 생각에서 출발했다. "
                "내재적 정의 믿음은 이 세계관의 도덕적 표현이다."
            ),
            "keywords": ["내재적 정의", "자동적 처벌", "아니미즘", "타율적 도덕성"],
            "verified": False
        },
        # CLAIM-006: 일방적 존경 vs 상호적 존경
        {
            "id": "piaget-claim-006",
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "source_detail": "The Moral Judgment of the Child, Chapter 3",
            "claim": (
                "타율적 도덕성은 어른에 대한 일방적 존경(unilateral respect)에 기반하며, "
                "자율적 도덕성은 또래 간의 상호적 존경(mutual respect)에 기반한다. "
                "일방적 존경은 힘의 차이에서 비롯된 의무감과 외경심이고, "
                "상호적 존경은 평등한 관계에서의 호혜성과 협동에서 비롯된 도덕적 의무감이다. "
                "진정한 도덕성의 발달을 위해서는 상호적 존경이 일방적 존경을 대체해야 한다."
            ),
            "original_text": None,
            "original_text_ko": None,
            "explanation": (
                "피아제는 도덕 발달의 사회적 원동력으로 두 가지 사회적 관계를 구분했다. "
                "일방적 존경: 어른-아이 관계처럼 불평등한 관계에서 생기는 일방적인 복종. "
                "이 관계는 타율적 도덕성(규칙은 권위에서 나온다는 믿음)을 낳는다. "
                "상호적 존경: 또래 관계처럼 평등한 관계에서의 쌍방향 존경. "
                "이 관계는 협동, 상호성, 정직의 가치를 발달시키고 자율적 도덕성의 기반이 된다."
            ),
            "argument": (
                "(1) 어른이 일방적으로 규칙을 부과하는 환경에서는 아동이 규칙의 이유를 이해하지 못하고 "
                "외부 권위에 대한 복종으로서의 도덕만을 내면화한다. "
                "(2) 또래와 게임을 협상하고 분쟁을 해결하는 경험에서 상호성·공정성·호혜성의 원리를 터득한다. "
                "(3) 따라서 또래 협동 활동은 도덕 발달의 핵심 촉진 요인이다."
            ),
            "counterpoint": (
                "성인의 권위와 지도가 반드시 타율적 도덕성으로만 이어지는 것은 아니다. "
                "권위주의적 훈육과 민주적 대화를 구분하지 않고 어른-아이 관계 전체를 "
                "일방적 존경으로 규정한 것은 지나친 단순화라는 비판이 있다. "
                "뱅듀라(Bandura)의 사회학습이론은 성인 모델 관찰을 통한 도덕학습도 강조했다."
            ),
            "context": (
                "피아제는 기존의 권위주의적 도덕교육(어른이 규칙을 부과하는 방식)이 "
                "오히려 자율적 도덕성 발달을 저해한다고 비판하며, "
                "교육에서 또래 협동의 중요성을 강조했다."
            ),
            "keywords": ["일방적 존경", "상호적 존경", "협동", "자율적 도덕성", "타율적 도덕성"],
            "verified": False
        },
        # CLAIM-007: 협동과 또래 관계의 도덕 발달 역할
        {
            "id": "piaget-claim-007",
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "source_detail": "The Moral Judgment of the Child, Chapter 3-4",
            "claim": (
                "또래 간 협동(peer cooperation)은 자율적 도덕성 발달의 핵심 동인이다. "
                "어른과의 일방적 관계만으로는 진정한 도덕적 자율성이 발달할 수 없으며, "
                "또래 집단 내에서의 갈등 해결, 협상, 상호 통제 경험이 "
                "호혜성(reciprocity)과 공정성(fairness)의 도덕적 원리를 내면화하게 한다."
            ),
            "original_text": None,
            "original_text_ko": None,
            "explanation": (
                "피아제에 따르면 또래와의 협동적 상호작용은 두 가지 방식으로 도덕 발달을 촉진한다. "
                "(1) 인지적: 또래의 관점과 자신의 관점 차이를 경험함으로써 자기중심성을 극복하고 탈중심화가 이루어진다. "
                "(2) 도덕적: 또래 간 갈등 해결 과정에서 규칙의 상호성, 공정성, 호혜성을 경험적으로 체득한다. "
                "이는 도덕교육에 실천적 함의를 가진다. 일방적 훈육보다 협동 활동이 더 효과적인 도덕교육이다."
            ),
            "argument": (
                "(1) 피아제의 관찰: 또래와 게임을 하는 아동은 규칙에 대해 협상하고 논쟁하며 "
                "상호 통제(mutual control)를 경험한다. "
                "(2) 어른이 부과한 규칙은 '어른이 정한 것'으로만 이해되지만, "
                "또래와 함께 만든 규칙은 왜 그 규칙이 있어야 하는지를 이해하며 따른다. "
                "(3) 이 경험이 자율적·내면화된 도덕성의 토대가 된다."
            ),
            "counterpoint": (
                "또래 관계가 항상 긍정적인 도덕 발달을 가져오지는 않는다. "
                "또래 압력(peer pressure)은 비도덕적 행동을 강화할 수도 있다. "
                "또한 가정에서의 부모-자녀 관계가 도덕 발달에 미치는 영향을 과소평가했다는 비판이 있다."
            ),
            "context": (
                "피아제의 이론은 1930년대 진보주의 교육 운동과 맥을 같이하며, "
                "아동 중심 교육, 협동학습의 이론적 근거가 되었다."
            ),
            "keywords": ["협동", "또래 관계", "호혜성", "공정성", "자율적 도덕성"],
            "verified": False
        },
        # CLAIM-008: 처벌 개념의 발달 (속죄적 → 보상적)
        {
            "id": "piaget-claim-008",
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "source_detail": "The Moral Judgment of the Child, Chapter 4",
            "claim": (
                "처벌 개념의 발달은 속죄적 처벌(expiatory punishment)에서 "
                "보상적·상호적 처벌(reciprocal punishment)로 이행한다. "
                "속죄적 처벌은 위반의 심각성에 비례하는 고통이나 벌로 보상받아야 한다는 관념이고, "
                "보상적 처벌은 위반 행위와 논리적으로 연관된 결과(자연적 결과, 배상 등)가 "
                "더 적절하다는 관념이다."
            ),
            "original_text": None,
            "original_text_ko": None,
            "explanation": (
                "타율적 도덕성 단계의 아동은 규칙을 어기면 외부에서 가해지는 고통 — 속죄적 처벌 —이 "
                "필요하다고 믿는다. 처벌의 내용은 위반과 논리적 연관이 없어도 되며, 단지 충분히 가혹해야 한다. "
                "자율적 도덕성 단계에서는 처벌이 위반 행위와 논리적으로 연결되어야 한다고 생각한다. "
                "예: 빵을 훔친 아이에게 빵을 먹지 못하게 하는 것, 장난감을 망가뜨린 아이에게 배상하게 하는 것. "
                "이는 처벌이 교화와 배상의 기능을 해야 한다는 인식의 발달을 반영한다."
            ),
            "argument": (
                "(1) 피아제의 처벌 이야기 실험: '빵을 훔친 아이에게 어떤 벌이 적절한가?' "
                "어린 아동은 '매를 맞아야 한다'(속죄적)고 답하고, "
                "큰 아동은 '빵을 먹지 못해야 한다' 또는 '배상해야 한다'(보상적)고 답했다. "
                "(2) 보상적 처벌 선호는 호혜성 원리의 이해에서 비롯된다."
            ),
            "counterpoint": (
                "보상적 처벌이 항상 더 교육적 효과가 높은지에 대한 논란이 있다. "
                "일부 상황에서는 속죄적 요소(진지한 반성과 사과)가 관계 회복에 중요할 수 있다. "
                "또한 회복적 정의(restorative justice) 운동은 피아제의 보상적 처벌 개념을 "
                "현대적으로 발전시킨 것으로 볼 수 있다."
            ),
            "context": (
                "피아제는 이 연구를 통해 아동이 단순히 어른의 처벌 개념을 모방하는 것이 아니라 "
                "스스로 정의와 처벌에 대한 관념을 구성한다는 것을 보이려 했다."
            ),
            "keywords": ["속죄적 처벌", "보상적 처벌", "자연적 결과", "상호적 처벌"],
            "verified": False
        },
        # CLAIM-009: 분배적 정의의 발달
        {
            "id": "piaget-claim-009",
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "source_detail": "The Moral Judgment of the Child, Chapter 4, §4-5",
            "claim": (
                "분배적 정의(distributive justice)에 대한 아동의 인식은 "
                "평등(equality)에서 공평(equity)으로 발달한다. "
                "초기에는 절대적 평등(모두 동일하게)을 정의롭다고 여기지만, "
                "발달하면서 개인의 상황과 필요를 고려한 공평 — "
                "예외적 사정이 있는 사람에게 더 많이 주는 것 — 이 더 정의롭다고 인식하게 된다."
            ),
            "original_text": None,
            "original_text_ko": None,
            "explanation": (
                "피아제는 분배 이야기 실험을 통해 이를 연구했다. "
                "예: 어머니가 케이크를 나누어 주는데, 한 아이는 아프고 다른 아이는 건강하다. "
                "어린 아동은 '똑같이 나누어야 한다'(절대적 평등)고 답한다. "
                "큰 아동은 '아픈 아이에게 조금 더 주어야 한다'(공평)고 답한다. "
                "이는 분배 정의의 인식이 기계적 평등에서 필요와 상황을 고려한 공평으로 발달함을 보여준다."
            ),
            "argument": (
                "(1) 협동과 상호적 존경을 경험하면서 개인의 차이와 필요를 이해하게 된다. "
                "(2) 단순 평등보다 높은 수준의 공평 개념은 타인의 관점을 이해하는 능력 — "
                "탈중심화 — 을 전제로 한다. "
                "(3) 이 발달은 인지 발달(탈중심화)과 도덕 발달의 연계를 잘 보여준다."
            ),
            "counterpoint": (
                "공평의 원리가 실제 분배 상황에서 어떻게 적용되어야 하는지는 맥락에 따라 복잡하다. "
                "롤스의 차등원칙과 같이, 공평의 구체적 기준은 더 정교한 이론적 논의를 필요로 한다."
            ),
            "context": (
                "분배적 정의의 발달 연구는 피아제가 도덕 발달을 "
                "단순한 규칙 준수를 넘어 정의 개념의 이해로까지 확장한 연구 영역이다."
            ),
            "keywords": ["분배적 정의", "평등", "공평", "탈중심화"],
            "verified": False
        },
        # CLAIM-010: 자기중심성과 도덕 발달
        {
            "id": "piaget-claim-010",
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "source_detail": "The Moral Judgment of the Child; The Psychology of Intelligence",
            "claim": (
                "자기중심성(egocentrism)은 도덕 발달의 장애물이다. "
                "자기중심성은 이기심과 다르며, 자신의 관점과 타인의 관점을 구별하지 못하는 인지적 상태이다. "
                "자기중심성이 극복되고 탈중심화(decentration)가 이루어질 때 "
                "타인의 의도와 관점을 파악하는 능력이 생기고, 이로써 자율적 도덕성의 발달이 가능해진다."
            ),
            "original_text": None,
            "original_text_ko": None,
            "explanation": (
                "피아제의 자기중심성은 자신을 세계의 중심으로 착각하는 이기적 태도가 아니라, "
                "자신의 관점이 전부라고 믿어 타인의 관점을 파악하지 못하는 인지적 제약이다. "
                "전조작기(2~7세)의 아동은 자기중심적이어서 타인이 다른 관점을 가질 수 있음을 이해하지 못한다. "
                "이 상태에서는 타인의 의도를 파악하지 못하므로 도덕 판단에서도 결과(객관적 피해)에만 의존한다. "
                "구체적 조작기에 탈중심화가 이루어지면 타인의 의도를 이해하고 "
                "상호적 도덕 판단이 가능해진다."
            ),
            "argument": (
                "(1) 세 산 과제(three mountains task): 어린 아동은 다른 위치에서 보면 "
                "산의 모습이 다르게 보인다는 것을 이해하지 못한다. "
                "(2) 이와 동일한 인지적 제약이 타인의 도덕적 의도를 파악하지 못하게 한다. "
                "(3) 협동과 또래 상호작용이 자기중심성을 극복하게 하는 핵심 기제이다."
            ),
            "counterpoint": (
                "최근 발달심리학 연구는 유아도 상당한 수준의 타인 이해 능력을 가지고 있음을 보여, "
                "자기중심성의 극복이 피아제가 제안한 것보다 훨씬 이른 시기에 이루어짐을 시사한다. "
                "비고츠키(Vygotsky)는 자기중심적 언어가 극복되는 것이 아니라 "
                "내적 언어로 전환된다고 주장하며 피아제의 해석에 이의를 제기했다."
            ),
            "context": (
                "피아제의 자기중심성 개념은 인지 발달과 도덕 발달을 연결하는 핵심 고리이다. "
                "인지 발달 없이는 도덕 발달도 제한된다는 피아제의 핵심 주장을 뒷받침한다."
            ),
            "keywords": ["자기중심성", "탈중심화", "조망 수용", "인지 발달", "도덕 발달"],
            "verified": False
        },
        # CLAIM-011: 인지발달과 도덕발달의 관계
        {
            "id": "piaget-claim-011",
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "source_detail": "The Moral Judgment of the Child, Introduction; The Psychology of Intelligence",
            "claim": (
                "도덕 발달은 인지 발달에 의해 제약된다. "
                "특정 수준의 인지 발달이 선행되어야 그에 상응하는 도덕 발달이 가능하다. "
                "구체적 조작기의 인지 능력(탈중심화, 가역성, 보존 개념)이 발달해야 "
                "자율적 도덕성, 상호적 정의 개념, 의도에 따른 판단이 가능해진다. "
                "그러나 인지 발달이 도덕 발달의 필요조건이지 충분조건은 아니다."
            ),
            "original_text": None,
            "original_text_ko": None,
            "explanation": (
                "피아제는 도덕 발달을 인지 발달의 맥락 안에서 이해했다. "
                "감각운동기(0~2세): 규칙 개념 없음. "
                "전조작기(2~7세): 타율적 도덕성 — 자기중심성, 실재론적 규칙 이해. "
                "구체적 조작기(7~11세): 자율적 도덕성 전환기 — 탈중심화, 역할 교환 이해. "
                "형식적 조작기(11세~): 완전한 자율적 도덕성 — 가상적 상황에서의 추상적 도덕 추론. "
                "이 연계는 콜버그가 도덕발달 단계론에서 발전시켰다."
            ),
            "argument": (
                "(1) 자기중심적 아동(전조작기)은 타인의 의도를 파악하지 못하므로 "
                "의도에 따른 도덕 판단이 불가능하다. "
                "(2) 구체적 조작기에 탈중심화가 이루어지면 타인의 관점(의도)을 파악할 수 있다. "
                "(3) 따라서 인지 발달은 도덕 발달의 필요조건이다. "
                "(4) 그러나 높은 인지 능력을 가진 사람이 반드시 높은 도덕성을 가지는 것은 아니므로 "
                "충분조건은 아니다."
            ),
            "counterpoint": (
                "콜버그는 도덕 발달이 인지 발달보다 한 단계 뒤처지는 경향이 있다고 주장하며 "
                "이 관계를 경험적으로 검증했다. "
                "그러나 인지 발달만으로 도덕 발달을 설명하는 접근은 "
                "정서적 요소, 사회적 환경, 문화의 역할을 과소평가한다는 비판이 있다."
            ),
            "context": (
                "피아제는 발생론적 인식론자로서 지식(도덕적 지식 포함)이 어떻게 구성되는지를 "
                "인지 발달의 관점에서 탐구했다."
            ),
            "keywords": ["인지 발달", "도덕 발달", "구체적 조작기", "탈중심화", "인지발달이론"],
            "verified": False
        },
        # CLAIM-012: 도덕교육의 방법론적 함의
        {
            "id": "piaget-claim-012",
            "thinker_id": "piaget",
            "work_id": "piaget-science-of-education",
            "source_detail": "Science of Education and the Psychology of the Child",
            "claim": (
                "효과적인 도덕교육은 일방적 훈육과 규칙 주입이 아니라 "
                "협동, 토론, 자기 규율을 통해 이루어진다. "
                "교사가 일방적으로 도덕 규칙을 부과하면 타율적 도덕성만을 강화하며, "
                "아동 스스로 규칙을 이해하고 만들어 나가는 참여적 경험이 "
                "자율적 도덕성의 발달을 촉진한다."
            ),
            "original_text": None,
            "original_text_ko": None,
            "explanation": (
                "피아제의 도덕교육론은 인지발달 이론의 교육적 적용이다. "
                "전통적 교육: 교사가 도덕 규칙을 권위적으로 부과 → 타율적 도덕성 유지 → 진정한 도덕성 미발달. "
                "피아제 권장 방법: "
                "(1) 협동 활동(cooperative activities): 또래와 함께 문제를 해결하며 상호성을 체험. "
                "(2) 도덕 토론(moral discussion): 도덕적 갈등 상황에서 이유를 논의. "
                "(3) 민주적 학급 운영: 학급 규칙을 학생들이 함께 만들고 관리. "
                "(4) 자연적 결과(natural consequences): 인위적 처벌보다 행위의 자연적 결과를 경험하게 함."
            ),
            "argument": (
                "(1) 권위적 훈육은 규칙에 대한 복종만을 낳고 규칙의 이유를 이해하게 하지 않는다. "
                "(2) 협동 활동에서 아동은 공정성, 호혜성, 상호성의 원리를 직접 경험한다. "
                "(3) 이 경험이 규칙의 정신을 이해하고 내면화하는 기반이 된다."
            ),
            "counterpoint": (
                "협동 중심 도덕교육이 모든 연령과 상황에 적합하지는 않다. "
                "어린 아동이나 심각한 도덕적 일탈 행동에서는 명확한 지도와 한계 설정이 필요하다. "
                "리코나(Lickona)는 인격교육(character education)에서 "
                "직접적 훈육과 역할 모델의 중요성도 강조했다."
            ),
            "context": (
                "피아제의 교육론은 듀이(Dewey)의 진보주의 교육과 맥을 같이하며, "
                "구성주의 교육이론의 이론적 토대가 되었다."
            ),
            "keywords": ["도덕교육", "협동학습", "자율성", "자기 규율", "구성주의"],
            "verified": False
        },
        # CLAIM-013: 동화·조절·평형화 메커니즘
        {
            "id": "piaget-claim-013",
            "thinker_id": "piaget",
            "work_id": "piaget-origins-of-intelligence",
            "source_detail": "The Origins of Intelligence in Children",
            "claim": (
                "인지(및 도덕) 발달은 동화(assimilation), 조절(accommodation), "
                "평형화(equilibration)의 상호작용으로 이루어진다. "
                "동화는 새로운 경험을 기존 도식(schema)에 맞추는 과정이고, "
                "조절은 새로운 경험에 맞게 도식을 수정하는 과정이며, "
                "평형화는 두 과정의 균형 회복을 위한 자기 조절 메커니즘이다."
            ),
            "original_text": None,
            "original_text_ko": None,
            "explanation": (
                "도식(schema): 세계를 이해하는 심리적 틀. "
                "동화: '이것은 개다'라는 도식에 고양이를 '개'라고 부르는 것. "
                "조절: 고양이를 경험하고 기존 도식을 수정하여 고양이와 개를 구분하게 되는 것. "
                "평형화: 동화와 조절의 불균형이 생길 때 균형을 회복하는 과정(인지 발달의 동인). "
                "도덕 발달에서: 기존의 도덕적 규칙 이해(도식)가 새로운 사회적 경험(또래 협동)과 충돌할 때 "
                "조절 과정을 통해 보다 성숙한 도덕 이해로 발전한다."
            ),
            "argument": (
                "(1) 아동은 수동적 수용자가 아니라 능동적으로 지식을 구성하는 존재이다. "
                "(2) 인지 발달(따라서 도덕 발달)은 외부에서 주어지는 것이 아니라 "
                "내적 재구성 과정(equilibration)을 통해 이루어진다. "
                "(3) 이는 구성주의 교육이론의 철학적 토대가 된다."
            ),
            "counterpoint": (
                "평형화 메커니즘이 너무 추상적이어서 경험적으로 검증하기 어렵다는 비판이 있다. "
                "비고츠키(Vygotsky)는 발달이 내적 평형화보다 사회적 상호작용과 언어를 통해 이루어진다고 강조했다."
            ),
            "context": (
                "피아제는 생물학적 적응(환경에 대한 유기체의 적응)을 인지 발달의 모델로 삼았다. "
                "동화·조절·평형화는 생물학적 적응의 심리적 유비(analogy)이다."
            ),
            "keywords": ["동화", "조절", "평형화", "도식", "구성주의", "인지 발달"],
            "verified": False
        },
        # CLAIM-014: 발생론적 인식론과 도덕
        {
            "id": "piaget-claim-014",
            "thinker_id": "piaget",
            "work_id": "piaget-psychology-of-intelligence",
            "source_detail": "The Psychology of Intelligence; 발생론적 인식론 총서",
            "claim": (
                "도덕적 지식(moral knowledge)은 어른이 아이에게 전달하는 것이 아니라 "
                "아이가 능동적으로 구성(construct)하는 것이다. "
                "피아제의 발생론적 인식론에 따르면, 지식은 주체(아동)와 환경(사회적 경험)의 "
                "상호작용을 통해 구성되며, 도덕적 이해도 마찬가지로 발달 단계에 따라 점진적으로 구성된다."
            ),
            "original_text": None,
            "original_text_ko": None,
            "explanation": (
                "발생론적 인식론(genetic epistemology): 지식이 어떻게 발생하고 발달하는지를 탐구. "
                "지식의 구성주의적 관점: 지식은 마음 밖에 존재하는 것을 수동적으로 받아들이는 것이 아니라 "
                "주체가 경험과의 상호작용을 통해 능동적으로 구성한다. "
                "도덕교육의 함의: 도덕 규칙을 외부에서 주입하는 것은 진정한 도덕 이해로 이어지지 않는다. "
                "아동이 도덕적 상황에서 스스로 추론하고 판단하는 경험이 진정한 도덕 이해를 가능하게 한다."
            ),
            "argument": (
                "(1) 같은 규칙을 가르쳐도 아동의 발달 단계에 따라 그 이해 방식이 질적으로 다르다. "
                "(2) 이는 지식이 외부에서 주어지는 것이 아니라 내적으로 구성됨을 보여준다. "
                "(3) 구성주의적 도덕교육은 아동의 발달 단계에 맞는 도덕적 경험과 토론을 제공해야 한다."
            ),
            "counterpoint": (
                "극단적 구성주의는 어른의 지도와 문화적 전수를 과소평가할 수 있다. "
                "비고츠키의 근접발달영역(ZPD) 개념은 적절한 성인의 지도가 발달을 촉진한다고 강조한다. "
                "또한 도덕적 진리가 사회적 합의나 구성의 산물인지, 아니면 객관적 근거가 있는지에 대한 "
                "철학적 논쟁도 있다."
            ),
            "context": (
                "피아제는 칸트의 선험적 인식론과 경험주의적 인식론을 모두 비판하며 "
                "'발달하는 인식론', 즉 지식이 역사적·발달적으로 구성된다는 관점을 취했다."
            ),
            "keywords": ["발생론적 인식론", "구성주의", "능동적 구성", "도덕교육"],
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """피아제 핵심 키워드 데이터 입력."""
    keywords = [
        {
            "id": "kw-piaget-heteronomous-morality",
            "term": "타율적 도덕성",
            "term_en": "heteronomous morality",
            "definition": (
                "피아제가 도덕발달의 초기 단계로 규정한 도덕성의 형태. "
                "약 5~10세 아동에게 나타나며, 규칙을 성인의 권위에 의해 주어진 절대적·불변적인 것으로 이해한다. "
                "행동의 결과(물질적 피해의 크기)를 기준으로 잘못을 판단하고(객관적 책임), "
                "규칙 위반에 대해 자동적 처벌이 따른다고 믿는다(내재적 정의). "
                "어른에 대한 일방적 존경(unilateral respect)을 특징으로 한다. "
                "도덕적 실재론과 동의어로 사용되기도 한다."
            ),
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "related_terms": ["자율적 도덕성", "도덕적 실재론", "일방적 존경", "내재적 정의", "객관적 책임"]
        },
        {
            "id": "kw-piaget-autonomous-morality",
            "term": "자율적 도덕성",
            "term_en": "autonomous morality",
            "definition": (
                "피아제가 도덕발달의 성숙한 단계로 규정한 도덕성의 형태. "
                "약 10세 이후에 나타나며, 규칙을 상호 합의에 의해 만들어진 것으로 이해하고 "
                "상황에 따라 변경 가능하다고 인식한다. "
                "행동의 의도(intention)를 기준으로 옳고 그름을 판단하며(주관적 책임), "
                "처벌은 위반과 논리적으로 연관되어야 한다고 본다(보상적 처벌). "
                "또래 간 상호적 존경(mutual respect)과 협동을 특징으로 한다. "
                "도덕적 상대주의와 연관된다."
            ),
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "related_terms": ["타율적 도덕성", "상호적 존경", "주관적 책임", "협동", "보상적 처벌"]
        },
        {
            "id": "kw-piaget-moral-realism",
            "term": "도덕적 실재론",
            "term_en": "moral realism",
            "definition": (
                "피아제가 타율적 도덕성 단계 아동의 특징으로 기술한 도덕 인식 태도. "
                "도덕 규칙이 외부의 권위에 의해 주어진 객관적·불변적 실재로서, "
                "인간의 의도나 의식과 독립하여 존재한다고 여긴다. "
                "세 가지 특징: (1) 규칙의 문자적·절대적 준수, (2) 객관적 책임(결과로 판단), "
                "(3) 속죄적 처벌의 정당성. 타율적 도덕성과 거의 동의어로 쓰인다."
            ),
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "related_terms": ["타율적 도덕성", "객관적 책임", "속죄적 처벌", "도덕적 상대주의"]
        },
        {
            "id": "kw-piaget-immanent-justice",
            "term": "내재적 정의",
            "term_en": "immanent justice",
            "definition": (
                "타율적 도덕성 단계 아동의 믿음으로, 규칙 위반 행위는 자동적으로 "
                "세계 자체(자연)로부터 처벌을 받는다는 신념. "
                "나쁜 일을 한 아이가 우연히 나쁜 일을 겪으면 그것이 그의 잘못에 대한 처벌이라고 믿는다. "
                "우주가 도덕적으로 질서 지어져 있다는 아니미즘적 세계관과 연결된다. "
                "자율적 도덕성이 발달하면서 이 믿음은 사라진다."
            ),
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "related_terms": ["타율적 도덕성", "속죄적 처벌", "아니미즘", "자율적 도덕성"]
        },
        {
            "id": "kw-piaget-unilateral-respect",
            "term": "일방적 존경",
            "term_en": "unilateral respect",
            "definition": (
                "힘과 권위의 차이에서 비롯되는 일방적인 복종·외경심. "
                "어른-아이 관계처럼 불평등한 관계에서 아이가 어른에게 가지는 존경. "
                "이 관계는 타율적 도덕성의 사회적 기반이 된다: "
                "어른의 명령이 곧 도덕적 의무가 되는 구조. "
                "상호적 존경(mutual respect)과 대립된다."
            ),
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "related_terms": ["상호적 존경", "타율적 도덕성", "권위", "협동"]
        },
        {
            "id": "kw-piaget-mutual-respect",
            "term": "상호적 존경",
            "term_en": "mutual respect",
            "definition": (
                "평등한 관계에서 발생하는 쌍방향적 존경. "
                "또래 관계에서 나타나며, 호혜성(reciprocity)과 협동의 경험에서 비롯된다. "
                "자율적 도덕성의 사회적 기반: 규칙은 상호 합의에 의해 만들어지며 "
                "상호 존중의 원리에 따라 지켜진다. "
                "진정한 도덕성의 발달을 위해서는 일방적 존경이 상호적 존경으로 대체되어야 한다."
            ),
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "related_terms": ["일방적 존경", "자율적 도덕성", "호혜성", "협동"]
        },
        {
            "id": "kw-piaget-egocentrism",
            "term": "자기중심성",
            "term_en": "egocentrism",
            "definition": (
                "피아제가 기술한 전조작기 아동의 인지적 특성으로, "
                "자신의 관점과 타인의 관점을 구별하지 못하는 상태. "
                "이기심(selfishness)과 다르며, 타인이 다른 관점을 가질 수 있다는 것을 "
                "인지적으로 이해하지 못하는 상태이다. "
                "자기중심성은 도덕 발달을 제약한다: 타인의 의도를 파악하지 못하므로 "
                "의도에 따른 도덕 판단이 불가능하다. "
                "탈중심화(decentration)를 통해 극복된다."
            ),
            "thinker_id": "piaget",
            "work_id": "piaget-psychology-of-intelligence",
            "related_terms": ["탈중심화", "조망 수용", "전조작기", "도덕 발달"]
        },
        {
            "id": "kw-piaget-decentration",
            "term": "탈중심화",
            "term_en": "decentration",
            "definition": (
                "자기중심성(egocentrism)을 극복하고 동시에 여러 관점이나 차원을 고려하는 능력의 발달. "
                "구체적 조작기에 나타나며, 이를 통해 타인의 관점을 이해하고(조망 수용), "
                "보존 개념을 이해하며, 의도에 따른 도덕 판단이 가능해진다. "
                "도덕 발달에서 탈중심화는 타율적 도덕성에서 자율적 도덕성으로의 이행을 가능하게 하는 "
                "핵심 인지적 전환이다."
            ),
            "thinker_id": "piaget",
            "work_id": "piaget-psychology-of-intelligence",
            "related_terms": ["자기중심성", "조망 수용", "구체적 조작기", "자율적 도덕성"]
        },
        {
            "id": "kw-piaget-assimilation-accommodation",
            "term": "동화와 조절",
            "term_en": "assimilation and accommodation",
            "definition": (
                "피아제의 인지 발달 메커니즘. "
                "동화(assimilation): 새로운 경험을 기존 도식(schema)에 통합하는 과정. "
                "조절(accommodation): 새로운 경험에 맞게 기존 도식을 수정·확장하는 과정. "
                "평형화(equilibration): 동화와 조절의 균형을 회복하는 자기 조절 과정으로, "
                "인지 발달(따라서 도덕 발달)의 내적 동인이다. "
                "이 메커니즘은 아동이 능동적으로 지식을 구성하는 구성주의적 발달 과정을 설명한다."
            ),
            "thinker_id": "piaget",
            "work_id": "piaget-origins-of-intelligence",
            "related_terms": ["도식", "평형화", "구성주의", "인지 발달"]
        },
        {
            "id": "kw-piaget-expiatory-punishment",
            "term": "속죄적 처벌",
            "term_en": "expiatory punishment",
            "definition": (
                "타율적 도덕성 단계 아동이 선호하는 처벌의 유형. "
                "규칙 위반에 대해 고통이나 강제로 보상받아야 한다는 관념. "
                "처벌의 내용이 위반 행위와 논리적으로 연관될 필요가 없으며, "
                "단지 충분히 엄격하고 권위자에 의해 부과되면 된다고 여긴다. "
                "자율적 도덕성 발달과 함께 보상적 처벌(reciprocal punishment)로 대체된다."
            ),
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "related_terms": ["보상적 처벌", "자연적 결과", "타율적 도덕성", "내재적 정의"]
        },
        {
            "id": "kw-piaget-reciprocal-punishment",
            "term": "보상적 처벌",
            "term_en": "reciprocal punishment",
            "definition": (
                "자율적 도덕성 단계에서 선호하는 처벌의 유형. "
                "위반 행위와 논리적으로 연관된 처벌 — 자연적 결과, 배상, 관계 회복 등 — 이 "
                "속죄적 처벌보다 더 적절하고 교육적이라는 관념. "
                "예: 물건을 망가뜨린 경우 배상, 거짓말을 한 경우 신뢰를 잃는 것. "
                "회복적 정의(restorative justice) 운동과 이론적으로 연결된다."
            ),
            "thinker_id": "piaget",
            "work_id": "piaget-moral-judgment",
            "related_terms": ["속죄적 처벌", "자연적 결과", "자율적 도덕성", "호혜성"]
        },
        {
            "id": "kw-piaget-genetic-epistemology",
            "term": "발생론적 인식론",
            "term_en": "genetic epistemology",
            "definition": (
                "피아제가 창시한 학문 분야로, 지식이 어떻게 발생하고 발달하는지를 탐구한다. "
                "'genetic'은 '유전적'이 아니라 '발생적·발달적'을 의미한다. "
                "지식은 선험적(아 프리오리)으로 주어지거나 경험에서 직접 추출되는 것이 아니라, "
                "주체와 환경의 능동적 상호작용을 통해 단계적으로 구성된다고 주장한다. "
                "도덕적 지식도 마찬가지로 발달 단계에 따라 능동적으로 구성된다."
            ),
            "thinker_id": "piaget",
            "work_id": "piaget-psychology-of-intelligence",
            "related_terms": ["구성주의", "인지 발달", "동화와 조절", "도덕 발달"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """피아제 관계 데이터 입력."""
    relations = [
        {
            "from_thinker": "piaget",
            "to_thinker": "kohlberg",
            "type": "influenced",
            "description": (
                "피아제의 도덕발달 두 단계론(타율→자율)이 콜버그 도덕발달 6단계론의 직접적 선구가 되었다. "
                "콜버그는 피아제의 연구를 확장하여 도덕 발달을 전인습, 인습, 후인습 3수준 6단계로 정교화했다. "
                "또한 피아제의 인지발달-도덕발달 연계 주장을 경험적으로 검증했다."
            ),
            "evidence": "Kohlberg, 'The Development of Children's Orientations toward a Moral Order' (1963)"
        },
        {
            "from_thinker": "dewey",
            "to_thinker": "piaget",
            "type": "influenced_by",
            "description": (
                "듀이의 진보주의 교육론과 경험 중심 학습 이론이 피아제의 교육관에 영향을 미쳤다. "
                "듀이의 '행함으로써 배우기(learning by doing)', 아동의 능동적 참여, "
                "민주적 교육 환경의 중요성은 피아제의 구성주의 교육론과 맥을 같이한다."
            ),
            "evidence": "피아제의 교육론(Science of Education, 1969)에서 듀이의 영향이 명확히 드러남"
        },
        {
            "from_thinker": "gilligan",
            "to_thinker": "piaget",
            "type": "criticized",
            "description": (
                "길리건은 피아제(및 콜버그)의 도덕발달론이 주로 남아를 연구 대상으로 하여 "
                "정의(justice) 중심의 도덕 발달만을 기술했다고 비판했다. "
                "여아와 여성의 도덕 발달은 정의보다 배려(care)와 관계(relationship)를 중심으로 이루어지며, "
                "이는 열등한 것이 아니라 다른 도덕 발달의 경로임을 주장했다."
            ),
            "evidence": "Gilligan, 'In a Different Voice' (1982)"
        },
        {
            "from_thinker": "vygotsky",
            "to_thinker": "piaget",
            "type": "criticized",
            "description": (
                "비고츠키는 피아제의 인지 발달 이론이 사회적 상호작용과 언어의 역할을 과소평가한다고 비판했다. "
                "피아제가 발달이 학습에 선행한다고 본 반면, 비고츠키는 사회적 학습이 발달을 이끈다고 주장했다(ZPD). "
                "또한 자기중심적 언어 해석에서도 의견이 달랐다."
            ),
            "evidence": "Vygotsky, 'Thought and Language' (1934); 'Mind in Society' (1978)"
        }
    ]

    for rel in relations:
        rel_id = f"{rel['from_thinker']}-{rel['type']}-{rel['to_thinker']}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id}: {result['result']}")

    return len(relations)


def main():
    """메인 실행 함수."""
    print("=== 피아제(Piaget) 데이터 ES 입력 시작 ===\n")
    client = get_client()

    try:
        print("1. 분야(field) 확인/추가")
        ensure_field(client)
        print()

        print("2. 사상가(thinker) 입력")
        insert_thinker(client)
        print()

        print("3. 저서(works) 입력")
        work_count = insert_works(client)
        print(f"   → {work_count}개 저서 입력 완료\n")

        print("4. 주장(claims) 입력")
        claim_count = insert_claims(client)
        print(f"   → {claim_count}개 주장 입력 완료\n")

        print("5. 키워드(keywords) 입력")
        kw_count = insert_keywords(client)
        print(f"   → {kw_count}개 키워드 입력 완료\n")

        print("6. 관계(relations) 입력")
        rel_count = insert_relations(client)
        print(f"   → {rel_count}개 관계 입력 완료\n")

        print("=== 입력 요약 ===")
        print(f"  사상가: 1명 (piaget)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n✓ 피아제 데이터 입력 완료!")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}")
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
