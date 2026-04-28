"""장 폴 사르트르(Jean-Paul Sartre) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS
)


def insert_thinker(client):
    """사르트르 사상가 데이터 입력."""
    doc = {
        "id": "sartre",
        "name": "장 폴 사르트르",
        "name_en": "Jean-Paul Sartre",
        "field": "western_ethics",
        "era": "현대 실존주의",
        "birth_year": 1905,
        "death_year": 1980,
        "background": (
            "파리에서 태어났으며 생후 15개월에 아버지를 잃고 외조부 슐바이처(Albert Schweitzer의 사촌) "
            "가정에서 성장했다. 에콜 노르말 쉬페리외르(École normale supérieure)에서 철학을 공부했으며, "
            "시몬 드 보부아르(Simone de Beauvoir)를 만나 평생 지적 동반자 관계를 맺었다. "
            "1933~1934년 베를린에 유학하여 후설(Edmund Husserl)의 현상학과 "
            "하이데거(Martin Heidegger)의 존재론을 깊이 연구했다. "
            "제2차 세계대전 중 독일 포로수용소에서 9개월을 보내며 자유와 책임에 관한 사유를 심화했고, "
            "레지스탕스 활동에 참여했다. 전후 실존주의의 대표 사상가로 명성을 얻었으며, "
            "1964년 노벨 문학상을 거부했다. 알제리 전쟁, 베트남 전쟁 등 정치적 사안에 "
            "앙가주망(engagement)을 실천하며 공개적으로 발언했다."
        ),
        "core_philosophy": (
            "사르트르 철학의 핵심은 '실존은 본질에 앞선다(L'existence précède l'essence)'는 "
            "테제이다. 신이 없는 세계에서 인간은 미리 규정된 본질 없이 세계에 내던져지며(délaissement), "
            "스스로 자신의 본질을 만들어가야 한다. 이 근본적 자유는 동시에 전적인 책임을 수반한다. "
            "현상학적 존재론에서 즉자존재(en-soi)와 대자존재(pour-soi)의 구분은 "
            "의식의 존재 방식을 해명한다. 대자존재인 인간은 '무(néant)'로서 끊임없이 자신을 초월하며, "
            "이 과정에서 자기기만(mauvaise foi)의 유혹과 실존적 불안(angoisse)에 직면한다. "
            "후기에는 개인 실존에서 집단적 실천으로 관심을 확장하여 "
            "마르크스주의와의 대화를 통해 변증법적 이성비판(Critique de la raison dialectique)을 전개했다."
        ),
        "philosophical_journey": (
            "초기(1930년대~1943): 현상학적 연구 시기. 후설과 하이데거의 영향 아래 "
            "'상상력'(1936), '자아의 초월'(1936), '감정론 소묘'(1939), '상상계'(1940)를 저술했다. "
            "'구토'(La Nausée, 1938)는 실존적 통찰을 소설 형식으로 담아낸 첫 번째 주요 문학 작품이다. "
            "중기(1943~1960): 실존주의 체계 구축 시기. '존재와 무'(L'Être et le Néant, 1943)에서 "
            "현상학적 존재론의 체계를 완성했다. '실존주의는 휴머니즘이다'(1946) 강연으로 "
            "실존주의를 대중에게 소개했다. 희곡 '닫힌 방'(Huis clos, 1944)에서 "
            "'지옥은 타인이다'를 형상화했다. "
            "후기(1960~1980): 마르크스주의와의 대화 및 집단 실천론 시기. "
            "'변증법적 이성비판'(1960)에서 개인 자유와 사회구조의 관계를 분석했다. "
            "자서전 '말'(Les Mots, 1964)을 발표했다."
        ),
        "keywords": [
            "실존주의",
            "앙가주망(engagement)",
            "즉자존재/대자존재(en-soi/pour-soi)",
            "자기기만(mauvaise foi)",
            "실존적 불안(angoisse)",
            "자유와 책임"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="sartre", document=doc)
    print(f"[thinker] sartre: {result['result']}")
    return result


def insert_works(client):
    """사르트르 저서 데이터 입력."""
    works = [
        {
            "id": "sartre-etre-neant",
            "thinker_id": "sartre",
            "title": "존재와 무",
            "title_original": "L'Être et le Néant",
            "year": 1943,
            "significance": (
                "사르트르 현상학적 존재론의 주저. 부제 '현상학적 존재론 소론(Essai d'ontologie "
                "phénoménologique)'이 시사하듯, 후설의 현상학과 하이데거의 존재론을 비판적으로 계승하여 "
                "독자적 존재론을 구축한다. 즉자존재(en-soi)와 대자존재(pour-soi)의 구분을 핵심 축으로 삼아 "
                "의식, 자유, 자기기만, 타자, 신체, 시간성을 체계적으로 분석한다. "
                "700페이지가 넘는 방대한 저작으로, 전쟁 중 집필되어 점령 하 파리에서 출판되었다. "
                "실존주의 철학의 이론적 토대를 제공한 20세기 철학의 기념비적 저작이다."
            ),
            "key_concepts": [
                "즉자존재(en-soi)", "대자존재(pour-soi)", "자기기만(mauvaise foi)",
                "무(néant)", "타자의 시선", "상황(situation)", "초월(transcendance)"
            ]
        },
        {
            "id": "sartre-existentialisme-humanisme",
            "thinker_id": "sartre",
            "title": "실존주의는 휴머니즘이다",
            "title_original": "L'existentialisme est un humanisme",
            "year": 1946,
            "significance": (
                "1945년 10월 클뤼브 맹트낭(Club Maintenant)에서 행한 강연을 정리한 소책자. "
                "가톨릭 신학자, 마르크스주의자 등의 비판에 답하는 형식으로 실존주의의 핵심 테제를 "
                "명료하게 제시한다. '실존은 본질에 앞선다', '인간은 자유로 선고받았다', "
                "앙가주망 등 사르트르 사상의 핵심 개념이 대중적 언어로 설명된다. "
                "사르트르 본인은 이후 이 강연이 사상을 지나치게 단순화했다고 여겼지만, "
                "실존주의를 세계에 알린 가장 영향력 있는 텍스트로 남아 있다."
            ),
            "key_concepts": [
                "실존은 본질에 앞선다", "앙가주망", "자유와 책임",
                "절망(désespoir)", "고독(solitude)", "실존적 휴머니즘"
            ]
        },
        {
            "id": "sartre-critique-raison-dialectique",
            "thinker_id": "sartre",
            "title": "변증법적 이성비판",
            "title_original": "Critique de la raison dialectique",
            "year": 1960,
            "significance": (
                "사르트르의 후기 주저. 개인 실존의 자유에서 출발했던 전기 철학을 사회적·역사적 차원으로 확장한다. "
                "마르크스주의와의 대화를 통해 실천(praxis), 집렬체(série), 융합집단(groupe en fusion), "
                "희소성(rareté) 등의 개념을 도입한다. "
                "제1권(1960)에서 개인 실천과 집단 형성 이론을 전개하고, "
                "사후 출판된 제2권(1985)에서 역사의 지성가능성 문제를 다룬다. "
                "'실존주의는 마르크스주의의 자투리 학문'이라는 도발적 테제와 함께 "
                "개인 자유와 사회구조 사이의 변증법적 관계를 탐구한다."
            ),
            "key_concepts": [
                "실천(praxis)", "집렬체(série)", "융합집단(groupe en fusion)",
                "희소성(rareté)", "소외(aliénation)", "역사의 지성가능성"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """사르트르 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 실존은 본질에 앞선다
        {
            "id": "sartre-claim-001",
            "thinker_id": "sartre",
            "work_id": "sartre-existentialisme-humanisme",
            "source_detail": "L'existentialisme est un humanisme (1946), pp. 26-29",
            "claim": (
                "실존은 본질에 앞선다(L'existence précède l'essence). "
                "인간은 먼저 세계에 내던져진 뒤 스스로 자신의 본질을 만들어간다. "
                "미리 규정된 인간 본성이란 없으며, 인간은 자신이 만드는 것 그 자체이다."
            ),
            "original_text": (
                "Qu'est-ce que signifie ici que l'existence précède l'essence? "
                "Cela signifie que l'homme existe d'abord, se rencontre, surgit dans le monde, "
                "et qu'il se définit après. "
                "L'homme, tel que le conçoit l'existentialiste, s'il n'est pas définissable, "
                "c'est qu'il n'est d'abord rien. "
                "Il ne sera qu'ensuite, et il sera tel qu'il se sera fait. "
                "(L'existentialisme est un humanisme, 1946)"
            ),
            "original_text_ko": (
                "여기서 실존이 본질에 앞선다는 것은 무엇을 의미하는가? "
                "그것은 인간이 먼저 존재하고, 세계 안에서 자신을 만나고, 세계 속에 솟아오르며, "
                "그 이후에 자신을 정의한다는 것을 의미한다. "
                "실존주의자들이 생각하는 인간은, 만약 정의될 수 없다면, "
                "그것은 그가 처음에는 아무것도 아니기 때문이다. "
                "그는 그 후에야 비로소 무엇이 될 것이며, 그가 만들어놓은 것이 될 것이다. "
                "(실존주의는 휴머니즘이다, 1946)"
            ),
            "explanation": (
                "사르트르는 칼날의 제작자가 칼의 목적과 형태(본질)를 먼저 구상한 뒤 칼을 만드는 것처럼, "
                "신이 인간의 본질을 먼저 구상하고 인간을 창조했다는 전통적 유신론 모델을 거부한다. "
                "무신론적 실존주의에서는 먼저 실존(existence)이 있고, 그 이후에 인간이 자신의 행위를 통해 "
                "자신의 본질을 만들어간다. 이는 전통 철학의 본질주의(essentialisme)를 전복한다."
            ),
            "argument": (
                "(1) 신은 존재하지 않으므로 인간 본성의 선험적 설계자도 없다. "
                "(2) 따라서 '인간 본성'이라는 미리 규정된 본질도 존재하지 않는다. "
                "(3) 인간은 먼저 아무것도 없는 상태로 세계에 내던져진다(délaissement). "
                "(4) 인간은 자신의 선택과 행위를 통해 비로소 자신의 본질을 구성한다. "
                "(5) 따라서 인간은 자기 자신의 유일한 창조자이며, 자신에 대해 전적으로 책임을 진다."
            ),
            "counterpoint": (
                "클로드 레비-스트로스(Claude Lévi-Strauss)는 '야생의 사고'(La Pensée sauvage, 1962)에서 "
                "사르트르의 역사적 이성 우위론과 실존 주체 중심주의를 구조주의적 관점에서 비판했다. "
                "레비-스트로스에 따르면 인간의 사유는 개인적 자유로운 실존에서 비롯되는 것이 아니라 "
                "언어·신화·친족 구조 등 무의식적 구조에 의해 규정된다. "
                "사르트르의 '실존'은 구조의 산물을 자유로 오인한 것이다."
            ),
            "context": (
                "데카르트 이후 서양 철학의 코기토(cogito) 전통, 칸트의 초월적 자아, "
                "키르케고르의 실존 개념, 하이데거의 현존재(Dasein) 분석에 대한 사르트르의 비판적 응답."
            ),
            "keywords": ["실존", "본질", "실존주의", "내던져짐", "본질주의 비판"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-002: 자유와 책임 — 인간은 자유로 선고받았다
        {
            "id": "sartre-claim-002",
            "thinker_id": "sartre",
            "work_id": "sartre-etre-neant",
            "source_detail": "L'Être et le Néant (1943), Part IV, ch. 1",
            "claim": (
                "인간은 자유로 선고받았다(L'homme est condamné à être libre). "
                "자유는 인간이 선택할 수 있는 속성이 아니라 인간 존재의 존재 구조 자체이다. "
                "자유롭지 않기로 선택하는 것조차 자유의 행사이므로, 인간은 자유로부터 도피할 수 없다."
            ),
            "original_text": (
                "Je suis condamné à être libre. Cela signifie qu'on ne saurait trouver à ma liberté "
                "d'autres limites qu'elle-même, ou, si l'on préfère, que nous ne sommes pas libres "
                "de cesser d'être libres. "
                "(L'Être et le Néant, 1943, Part IV, ch. 1)"
            ),
            "original_text_ko": (
                "나는 자유로 선고받았다. 이것은 내 자유에 대해 자유 자체 이외의 다른 한계를 찾을 수 없다는 것을, "
                "혹은 선호한다면, 우리가 자유롭기를 그칠 자유가 없다는 것을 의미한다. "
                "(존재와 무, 1943, 4부 1장)"
            ),
            "explanation": (
                "사르트르에게 자유는 인간 존재의 존재론적 구조이다. 대자존재(pour-soi)는 자신의 존재에 대해 "
                "끊임없이 '아니오'라고 말할 수 있는 능력, 즉 부정(négation)의 능력을 가진다. "
                "이 부정 능력이 곧 자유이며, 이는 인간이 어떤 상황에서도 그 상황에 대해 태도를 취할 수 있음을 뜻한다. "
                "심지어 상황에 굴복하는 것조차 '굴복하기로 선택'하는 자유의 행사이다."
            ),
            "argument": (
                "(1) 대자존재(pour-soi, 의식)는 즉자존재(en-soi, 사물)와 달리 자신의 존재를 문제 삼는다. "
                "(2) 의식은 자신의 과거·상황·본성으로부터 물러서서 그것에 대해 부정(néantisation)을 수행할 수 있다. "
                "(3) 이 부정 능력이 인간의 자유의 존재론적 근거이다. "
                "(4) 자유는 외부 조건 부재가 아니라, 어떤 조건 아래서도 의미(signification)를 선택하는 능력이다. "
                "(5) 자유롭지 않음을 선택하는 것 자체가 자유의 행사이므로, 자유로부터의 완전한 도피는 불가능하다."
            ),
            "counterpoint": (
                "모리스 메를로-퐁티(Maurice Merleau-Ponty)는 '지각의 현상학'(Phénoménologie de la "
                "perception, 1945)에서 사르트르의 절대적 자유 개념을 비판했다. "
                "메를로-퐁티에 따르면 신체-주체는 세계와 선(先)반성적으로 얽혀 있으며(motricité), "
                "사르트르의 의식 중심주의는 몸의 습관(habitude)과 상황의 두께를 무시한다. "
                "상황의 실질적 저항 없이 모든 것이 동등하게 선택 가능하다는 사르트르의 자유는 "
                "추상적이고 공허하다."
            ),
            "context": (
                "전쟁과 점령 상황에서의 인간 행동에 대한 성찰. "
                "레지스탕스 활동과 부역 사이의 선택 문제. "
                "스피노자의 결정론과 칸트의 자율 개념에 대한 비판적 응답."
            ),
            "keywords": ["자유", "책임", "대자존재", "부정", "선택"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-003: 앙가주망(engagement)
        {
            "id": "sartre-claim-003",
            "thinker_id": "sartre",
            "work_id": "sartre-existentialisme-humanisme",
            "source_detail": "L'existentialisme est un humanisme (1946), pp. 48-57",
            "claim": (
                "자유는 사회적 실천을 요구한다. 실존주의는 주관주의적 도피가 아니라 "
                "앙가주망(engagement, 참여·투신)을 통해 타인과 세계에 대한 책임을 수행하는 것이다. "
                "내가 선택할 때 나는 모든 인간을 위해 선택하는 것이다."
            ),
            "original_text": (
                "Quand nous disons que l'homme se choisit, nous entendons que chacun d'entre nous "
                "se choisit, mais par là nous voulons dire aussi qu'en se choisissant il choisit "
                "tous les hommes. "
                "En effet, il n'est pas un de nos actes qui, en créant l'homme que nous voulons être, "
                "ne crée en même temps une image de l'homme tel que nous estimons qu'il doit être. "
                "(L'existentialisme est un humanisme, 1946)"
            ),
            "original_text_ko": (
                "우리가 인간은 자기 자신을 선택한다고 말할 때, 우리는 우리들 각자가 자기 자신을 선택한다는 것을 "
                "의미하지만, 그렇게 함으로써 우리는 또한 자기 자신을 선택하면서 모든 인간을 선택한다는 것을 "
                "의미하고 싶다. "
                "사실상, 우리가 되고자 하는 인간을 창조하는 우리의 행위들 중에, 동시에 우리가 그렇게 되어야 한다고 "
                "여기는 인간의 이미지를 창조하지 않는 것은 하나도 없다. "
                "(실존주의는 휴머니즘이다, 1946)"
            ),
            "explanation": (
                "사르트르의 앙가주망은 지식인의 사회적 책임을 강조하는 실천 개념이다. "
                "자유는 고독한 개인의 내면에 머무를 수 없으며, 선택은 항상 타인과의 관계 속에서 이루어진다. "
                "내가 특정 방식의 삶을 선택한다는 것은 그 삶이 좋다고 인정하는 것이며, "
                "이는 모든 인간에게 해당하는 규범을 암묵적으로 설정하는 것이다. "
                "따라서 개인의 선택은 보편적 의미를 지니며, 앙가주망을 회피하는 것도 일종의 선택이다."
            ),
            "argument": (
                "(1) 인간의 자유는 타인의 자유와 무관하게 작동하지 않는다. "
                "(2) 내가 선택하는 것은 그것이 좋다는 판단을 포함하며, 이는 암묵적으로 보편적 규범을 설정한다. "
                "(3) '나는 자유를 원한다'는 선택은 논리적으로 타인의 자유도 원한다는 것을 함축한다. "
                "(4) 따라서 자유의 진정한 실현은 개인적 차원을 넘어 타인의 자유와 사회적 조건 변혁을 추구하는 "
                "   앙가주망을 요구한다. "
                "(5) 정치·사회적 사안에서 중립을 표방하는 것도 기존 체제를 용인하는 하나의 선택이다."
            ),
            "counterpoint": (
                "알베르 카뮈(Albert Camus)는 '반항하는 인간'(L'Homme révolté, 1951)에서 "
                "사르트르의 앙가주망이 역사와 혁명을 절대화할 위험이 있다고 비판했다. "
                "카뮈에 따르면 어떤 정치적 대의에 완전히 투신(engagement)하는 것은 "
                "그 대의 이름으로 행해지는 폭력을 정당화할 수 있으며, "
                "이는 단순한 반항(révolte)의 한계를 넘어 허무주의적 테러리즘으로 전락할 수 있다."
            ),
            "context": (
                "전후 프랑스 지식인들의 사회적 역할 논쟁, 공산당과의 관계 문제, "
                "알제리 독립 운동에 대한 입장. '현대'(Les Temps modernes) 잡지 창간(1945)."
            ),
            "keywords": ["앙가주망", "참여", "사회적 책임", "자유의 보편성", "지식인"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-004: 즉자존재/대자존재 (en-soi / pour-soi)
        {
            "id": "sartre-claim-004",
            "thinker_id": "sartre",
            "work_id": "sartre-etre-neant",
            "source_detail": "L'Être et le Néant (1943), Introduction §§5-6, Part II ch. 1",
            "claim": (
                "존재는 즉자존재(en-soi, 사물의 존재)와 대자존재(pour-soi, 의식의 존재)로 구분된다. "
                "즉자존재는 그 자체로 꽉 차 있는 불투명한 존재이며, "
                "대자존재는 자신의 존재 안에 '무(néant)'를 품고 있는 의식으로서 "
                "끊임없이 자신을 초월한다."
            ),
            "original_text": (
                "L'être est. L'être est en soi. L'être est ce qu'il est. "
                "... La conscience est un être pour lequel il est dans son être question de son être "
                "en tant que cet être implique un être autre que lui. "
                "(L'Être et le Néant, 1943, Introduction §5 & Part II ch. 1)"
            ),
            "original_text_ko": (
                "존재는 있다. 존재는 즉자적이다. 존재는 자신이 있는 것 그대로이다. "
                "... 의식은 자신의 존재 안에서 자신의 존재가 문제가 되는, "
                "그리고 이 존재가 자신 이외의 다른 존재를 함축하는 그런 존재이다. "
                "(존재와 무, 1943, 서론 §5 및 2부 1장)"
            ),
            "explanation": (
                "즉자존재(en-soi)는 돌·책상·동물 등 사물의 존재 방식으로, "
                "자신이 무엇인지 문제 삼지 않고 그냥 있다. 자기 동일성(identité)을 유지하며 변화하지 않는다. "
                "대자존재(pour-soi)는 인간 의식의 존재 방식으로, 자신이 무엇인지 끊임없이 문제 삼는다. "
                "의식은 항상 자신이 아닌 것을 향해 있으며(지향성, intentionnalité), "
                "자신을 부정함으로써 자신을 초월한다. "
                "인간이 '되어가는' 존재인 것은 바로 이 대자적 구조 때문이다."
            ),
            "argument": (
                "(1) 현상학적 분석에 따르면 의식은 항상 '무언가에 대한 의식'이다(후설의 지향성). "
                "(2) 의식이 대상을 의식하기 위해서는 대상과 의식 사이에 거리, 즉 '무(néant)'가 있어야 한다. "
                "(3) 이 무가 의식의 존재론적 구조를 규정한다: 의식은 자신의 존재 안에 무를 품고 있다. "
                "(4) 의식이 자신의 과거·상황·본성을 부정(néantiser)할 수 있는 것은 이 구조 때문이다. "
                "(5) 반면 즉자존재는 자기 동일적이며 무를 포함하지 않으므로 자유도 없고 변화도 없다."
            ),
            "counterpoint": (
                "마르틴 하이데거(Martin Heidegger)는 '존재와 시간'(Sein und Zeit, 1927)에서 "
                "의식-사물의 이분법을 극복하는 '현존재(Dasein)'의 세계-내-존재(In-der-Welt-sein) 구조를 "
                "제시했다. 하이데거 측에서 보면, 사르트르의 즉자/대자 이분법은 여전히 "
                "데카르트적 주관-객관 이원론의 잔재이며, '세계'를 의식과 사물의 단순 병렬로 환원시킨다는 "
                "비판이 가능하다. 하이데거는 사르트르가 자신의 존재 분석을 휴머니즘적으로 왜곡했다고 "
                "'휴머니즘에 관한 편지'(Brief über den Humanismus, 1947)에서 지적했다."
            ),
            "context": (
                "후설(Edmund Husserl)의 지향성 이론과 현상학적 환원, "
                "하이데거의 존재 분석, 헤겔의 정신현상학(즉자-대자-즉자대자 변증법)에 대한 응답."
            ),
            "keywords": ["즉자존재", "대자존재", "en-soi", "pour-soi", "무(néant)", "지향성"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-005: 자기기만(mauvaise foi)
        {
            "id": "sartre-claim-005",
            "thinker_id": "sartre",
            "work_id": "sartre-etre-neant",
            "source_detail": "L'Être et le Néant (1943), Part I, ch. 2",
            "claim": (
                "자기기만(mauvaise foi, 나쁜 믿음)은 인간이 자신의 자유와 책임을 부정하고 "
                "마치 자신이 즉자존재(사물)처럼 규정된 본성을 가진 것처럼 행동하는 태도이다. "
                "자기기만은 타인의 강요가 아니라 자기 자신을 속이는 의식의 자기 기만이다."
            ),
            "original_text": (
                "La mauvaise foi n'est pas de dehors, elle n'est pas un mensonge: "
                "c'est une mensonge à soi-même. "
                "... Le garçon de café joue à être garçon de café. "
                "Il réalise sa condition d'homme en la niant. "
                "(L'Être et le Néant, 1943, Part I, ch. 2)"
            ),
            "original_text_ko": (
                "자기기만은 외부에서 오는 것이 아니며 거짓말도 아니다: "
                "그것은 자기 자신에 대한 거짓말이다. "
                "... 카페 웨이터는 카페 웨이터이기를 연기한다. "
                "그는 자신의 인간 조건을 부정함으로써 그것을 실현한다. "
                "(존재와 무, 1943, 1부 2장)"
            ),
            "explanation": (
                "사르트르는 '카페 웨이터' 예를 통해 자기기만을 설명한다. "
                "카페 웨이터가 자신의 모든 동작을 지나치게 정확하게 수행하며 "
                "마치 기계처럼 행동한다면, 그는 '웨이터'라는 역할이 자신의 전부인 것처럼, "
                "즉 자신이 변할 수 없는 즉자존재인 것처럼 스스로를 속이는 것이다. "
                "이는 자유에서 비롯되는 불안(angoisse)을 회피하기 위한 전략이다. "
                "자기기만의 반대는 진정성(authenticité): 자신의 자유와 책임을 있는 그대로 인정하는 태도이다."
            ),
            "argument": (
                "(1) 대자존재인 인간은 자신의 과거·역할·상황에 의해 완전히 규정될 수 없다(초월성). "
                "(2) 그러나 인간은 이 초월성에서 비롯되는 불안(angoisse)을 피하려 한다. "
                "(3) 자기기만은 자신을 마치 즉자존재처럼 파악함으로써 이 불안을 회피하는 전략이다. "
                "(4) 이는 의식이 자기 자신에게 거짓말을 하는 것으로, 외부의 강요 없이 스스로 수행한다. "
                "(5) 자기기만이 가능한 것은 역설적으로 인간이 자유롭기 때문이다: "
                "   자유가 없다면 자유를 부정하는 자기기만도 불가능하다."
            ),
            "counterpoint": (
                "헤르베르트 마르쿠제(Herbert Marcuse)는 '일차원적 인간'(One-Dimensional Man, 1964)에서 "
                "개인의 자기기만을 단순히 의식의 문제로 환원하는 것은 불충분하다고 비판했다. "
                "마르쿠제에 따르면 현대 자본주의 사회는 '행복한 의식(happy consciousness)'을 "
                "구조적으로 생산하여 개인이 지배 이데올로기를 자발적으로 내면화하게 만든다. "
                "이 경우 자기기만은 개인적 선택이 아니라 사회적·구조적 강제의 산물이다."
            ),
            "context": (
                "프로이트의 무의식 이론(사르트르는 무의식을 거부하고 자기기만 개념으로 대체), "
                "키르케고르의 '절망(despair)' 개념, 하이데거의 '빠져있음(Verfallenheit)'과의 비교."
            ),
            "keywords": ["자기기만", "mauvaise foi", "진정성", "불안", "역할"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-006: 타자와 시선 — 지옥은 타인이다
        {
            "id": "sartre-claim-006",
            "thinker_id": "sartre",
            "work_id": "sartre-etre-neant",
            "source_detail": (
                "L'Être et le Néant (1943), Part III; "
                "Huis clos (1944) — 희곡"
            ),
            "claim": (
                "타인의 시선(le regard)은 나를 대상화(objectivation)한다. "
                "타인이 나를 바라볼 때 나는 즉자존재로 응고되며, "
                "나의 자유와 초월성이 박탈되는 것처럼 느낀다. "
                "'지옥은 타인이다(L'enfer, c'est les autres).'"
            ),
            "original_text": (
                "L'enfer, c'est les Autres. "
                "(Huis clos, 1944, scène 5) "
                "— et: "
                "Autrui est d'abord pour moi l'être par qui je suis regardé. "
                "(L'Être et le Néant, 1943, Part III, §3)"
            ),
            "original_text_ko": (
                "지옥은 타인들이다. "
                "(닫힌 방, 1944, 5장) "
                "— 그리고: "
                "타인은 우선 나에게 나를 바라보는 자로서의 존재이다. "
                "(존재와 무, 1943, 3부 §3)"
            ),
            "explanation": (
                "사르트르는 희곡 '닫힌 방(Huis clos)'에서 세 명의 죽은 영혼이 지옥의 방 안에 갇혀 "
                "서로를 영원히 바라보는 상황을 설정한다. '지옥은 타인이다'는 이 상황에서 나온 말로, "
                "인간 관계의 근본적 갈등 구조를 드러낸다. "
                "타인의 시선은 나를 고정된 대상으로 만들며, 나는 타인의 눈에 비친 나의 이미지를 "
                "통제할 수 없다. 이것이 수치심(honte)의 근원이다. "
                "사르트르에게 타자 관계는 근본적으로 갈등적이다: 나의 자유는 타인을 대상화함으로써만 확보되고, "
                "타인의 자유는 나를 대상화한다."
            ),
            "argument": (
                "(1) 타인은 단순히 나의 의식에 나타나는 대상이 아니라, 나를 바라보는 자유로운 주체이다. "
                "(2) 타인이 나를 바라볼 때 나는 타인의 시선 안에서 규정되고 응고된다(객체화). "
                "(3) 나는 타인이 나를 어떻게 보는지를 통제할 수 없으며, 이로 인해 수치심이 발생한다. "
                "(4) 이 수치심은 나의 자유가 타인의 시선에 의해 위협받는다는 사실에서 비롯된다. "
                "(5) 나와 타인의 관계는 근본적으로 '보는 자-보이는 자'의 갈등 관계이며, "
                "   이 갈등은 어느 일방이 완전히 극복할 수 없다."
            ),
            "counterpoint": (
                "에마뉘엘 레비나스(Emmanuel Lévinas)는 '전체성과 무한'(Totalité et Infini, 1961)에서 "
                "사르트르의 타자 이론이 타자를 결국 '나의 자유에 대한 위협'으로 환원시킨다고 비판했다. "
                "레비나스에게 타자의 얼굴(visage)은 나를 윤리적으로 요청하는 무한성이며, "
                "타자 관계는 갈등(conflit)이 아니라 환대(hospitalité)와 책임을 요구하는 만남이다. "
                "사르트르의 타자론은 타자를 나의 주관성의 적으로 파악함으로써 "
                "타자의 진정한 타자성(altérité)을 존중하지 못한다."
            ),
            "context": (
                "헤겔의 '주인-노예 변증법'(정신현상학, 1807), "
                "후설의 타자 경험론(상호주관성), 하이데거의 공동현존재(Mitdasein) 개념과의 비교."
            ),
            "keywords": ["타자", "시선(regard)", "대상화", "수치심", "지옥은 타인이다"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-007: 실존적 불안과 구토
        {
            "id": "sartre-claim-007",
            "thinker_id": "sartre",
            "work_id": "sartre-etre-neant",
            "source_detail": (
                "L'Être et le Néant (1943), Introduction §4; "
                "La Nausée (1938) — 소설"
            ),
            "claim": (
                "실존적 불안(angoisse)은 인간이 자신의 절대적 자유를 직면할 때 느끼는 현기증이다. "
                "구토(nausée)는 즉자적 사물들의 잉여적 존재(existence de trop)와 직면할 때 "
                "대자존재가 느끼는 존재론적 메스꺼움이다."
            ),
            "original_text": (
                "L'angoisse est précisément ma conscience d'être ma propre avenir sur le mode "
                "du n'être-pas. "
                "(L'Être et le Néant, 1943, Introduction §4) "
                "— et: "
                "L'existence, c'est là. Doux, doux, si doux... Et moi — mou, faible, obscène, "
                "digérant, ballottant de mornes pensées — moi aussi j'étais de trop. "
                "(La Nausée, 1938)"
            ),
            "original_text_ko": (
                "불안은 정확히 내가 나의 미래를 '있지 않는-것'의 방식으로 의식하는 것이다. "
                "(존재와 무, 1943, 서론 §4) "
                "— 그리고: "
                "실존, 그것이 거기 있다. 부드럽고, 부드럽고, 너무나 부드럽다... 그리고 나 — 유약하고, "
                "나약하고, 외설스럽고, 소화하고, 음울한 생각들에 흔들리는 — 나 역시 잉여였다. "
                "(구토, 1938)"
            ),
            "explanation": (
                "불안(angoisse)은 단순한 공포가 아니다. 공포는 특정 대상(뱀, 높이 등)에 대한 것이지만, "
                "불안은 자기 자신의 자유에 대한 것이다. '나는 다음 순간 무엇이든 될 수 있다'는 자유는 "
                "동시에 '나는 아무런 근거도 없이 선택해야 한다'는 공허감을 수반한다. "
                "구토(nausée)는 소설 '구토'의 주인공 로캉탱이 밤나무 뿌리를 바라보며 경험하는 것으로, "
                "사물들이 단순히 '있다'는 사실의 불투명한 잉여성, 즉 어떤 이유도 목적도 없이 존재한다는 "
                "사실에 대한 존재론적 반응이다."
            ),
            "argument": (
                "(1) 대자존재는 자신의 가능성들을 향해 열려 있으며, 이 가능성들은 아직 확정되지 않았다. "
                "(2) 이 열린 가능성은 자유이지만, 동시에 어떤 행동도 미리 보장되지 않는다는 불안정성이다. "
                "(3) 불안은 이 자유의 현기증(vertige)이다: 나는 자신이 무엇을 할 것인지 미리 알 수 없다. "
                "(4) 구토는 즉자적 존재들의 잉여성과 대면할 때 발생한다: 사물들은 아무런 이유 없이 '있다'. "
                "(5) 이 우연성(contingence)의 직면이 인간에게 존재론적 메스꺼움을 야기한다."
            ),
            "counterpoint": (
                "마르틴 하이데거(Martin Heidegger)는 '형이상학이란 무엇인가'(Was ist Metaphysik?, 1929)에서 "
                "불안(Angst)을 존재 전체가 미끄러지는 현상(das Weggleiten des Seienden im Ganzen)으로 "
                "분석했다. 하이데거의 불안은 사르트르처럼 자유의 현기증이라기보다, "
                "현존재를 '무(das Nichts)' 앞에 세우고 존재 물음을 촉발하는 근본 기분(Grundstimmung)이다. "
                "사르트르의 불안은 하이데거의 것보다 더 주관주의적이며, "
                "존재 물음보다 자유와 책임의 문제로 방향이 전환되어 있다는 비판이 가능하다."
            ),
            "context": (
                "키르케고르의 '불안의 개념'(Begrebet Angest, 1844), "
                "하이데거의 불안(Angst) 분석, 파스칼의 인간 조건에 대한 불안."
            ),
            "keywords": ["불안(angoisse)", "구토(nausée)", "우연성", "잉여 존재", "자유의 현기증"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-008: 자유의 상황성(situation) — 상황 속의 자유
        {
            "id": "sartre-claim-008",
            "thinker_id": "sartre",
            "work_id": "sartre-etre-neant",
            "source_detail": "L'Être et le Néant (1943), Part IV, ch. 1, §2 (La liberté et la facticité: la situation)",
            "claim": (
                "자유는 절대적이지만 상황 속에서만 실현된다. "
                "인간은 계급·성별·국적·시대 등 주어진 사실성(facticité) 안에서 태어나며, "
                "이 사실성을 어떻게 의미화하는가가 자유의 내용이 된다. "
                "상황 없는 자유도, 자유 없는 상황도 없다."
            ),
            "original_text": (
                "Il n'y a de liberté qu'en situation et il n'y a de situation que par la liberté. "
                "La réalité-humaine rencontre partout des résistances et des obstacles qu'elle n'a "
                "pas créés; mais ces résistances et ces obstacles n'ont de sens que dans et par "
                "le libre choix que la réalité-humaine est. "
                "(L'Être et le Néant, 1943, Part IV, ch. 1)"
            ),
            "original_text_ko": (
                "상황 속에서만 자유가 있고, 자유를 통해서만 상황이 있다. "
                "인간-실재는 도처에서 자신이 만들지 않은 저항과 장애들을 만난다; "
                "그러나 이 저항과 장애들은 인간-실재가 수행하는 자유로운 선택 안에서, "
                "그리고 그것을 통해서만 의미를 갖는다. "
                "(존재와 무, 1943, 4부 1장)"
            ),
            "explanation": (
                "사르트르는 자유가 '진공 속의 자유'가 아님을 인정한다. "
                "인간은 특정 계급·젠더·국적·신체 조건 안에서 태어나며(사실성, facticité), "
                "이 상황은 저항과 장애물을 제공한다. 그러나 이 상황이 어떤 의미를 갖는지는 "
                "결국 인간의 자유로운 선택에 달려 있다. "
                "가난은 사람을 자동으로 혁명가로 만들지 않는다. 가난이 혁명의 동기가 되는 것은 "
                "혁명을 선택하는 프로젝트(projet) 안에서이다. "
                "이로써 사르트르의 자유는 메를로-퐁티의 비판에 일정 부분 응답한다."
            ),
            "argument": (
                "(1) 자유는 항상 구체적 상황 속에서 행사된다(상황성, situationnalité). "
                "(2) 상황의 요소들(계급·역할·역사·신체 등)은 저항과 장애를 제공하지만, "
                "   그것들의 의미는 인간의 근본 기투(projet fondamental)에 의해 결정된다. "
                "(3) 따라서 동일한 상황도 사람마다 다르게 경험된다: 자유가 상황을 의미화하기 때문이다. "
                "(4) 그러나 인간은 자신의 사실성(출생·신체·계급·역사)을 선택할 수 없으므로, "
                "   자유는 상황에 의해 '제약'되는 것이 아니라 상황과 '변증법적'으로 관계한다. "
                "(5) 결국 자유와 상황은 분리 불가능하다: 상황 없는 자유는 공허하고, "
                "   자유 없는 상황은 의미 없다."
            ),
            "counterpoint": (
                "루이 알튀세르(Louis Althusser)는 '이데올로기와 이데올로기적 국가장치'(Idéologie et "
                "appareils idéologiques d'État, 1970)에서 사르트르의 자유 개념이 이데올로기에 의한 "
                "주체 구성을 간과한다고 비판했다. "
                "알튀세르에 따르면 개인은 이데올로기에 의해 '호명(interpellation)'되어 주체로 구성되므로, "
                "사르트르가 전제하는 자유로운 선택의 주체는 이미 이데올로기적 산물이다. "
                "상황을 의미화하는 자유로운 주체란 이데올로기의 효과일 뿐이다."
            ),
            "context": (
                "메를로-퐁티의 체화된 자유 비판에 대한 사르트르의 응답, "
                "마르크스주의의 계급 결정론과의 긴장, 후기 '변증법적 이성비판'에서의 상황성 심화."
            ),
            "keywords": ["상황(situation)", "사실성(facticité)", "근본기투", "자유의 구체성", "상황성"],
            "verified": False,
            "verification_log": []
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """사르트르 키워드 데이터 입력."""
    keywords = [
        {
            "id": "sartre-kw-001",
            "thinker_id": "sartre",
            "term": "실존주의 (Existentialisme)",
            "term_en": "Existentialism",
            "definition": (
                "인간의 실존(existence)을 본질(essence)에 앞서는 것으로 파악하는 20세기 철학 사조. "
                "사르트르는 무신론적 실존주의의 대표자로, 신의 부재 속에서 인간이 스스로 자신의 본질을 "
                "만들어가야 한다는 급진적 자유와 책임의 철학을 전개했다. "
                "키르케고르(유신론적 실존주의)와 하이데거(실존 분석론)의 영향을 받았으나, "
                "사르트르는 이를 명시적 인본주의(humanisme)로 발전시켰다."
            ),
            "thinker_id": "sartre",
            "work_id": "sartre-existentialisme-humanisme",
            "related_terms": ["실존", "본질", "자유", "책임", "앙가주망"]
        },
        {
            "id": "sartre-kw-002",
            "thinker_id": "sartre",
            "term": "앙가주망 (Engagement)",
            "term_en": "Engagement / Commitment",
            "definition": (
                "자유를 지닌 인간이 정치적·사회적 현실에 적극적으로 참여·투신하는 것. "
                "사르트르에게 중립은 없다: 참여하지 않는 것도 하나의 선택이며, "
                "그 선택은 현상 유지를 지지하는 효과를 갖는다. "
                "특히 지식인은 자신의 지식과 영향력을 사회 변혁에 사용해야 할 책임이 있다. "
                "사르트르 자신의 알제리 독립 운동 지지, 소련 비판, 마오이즘 지지 등이 "
                "앙가주망의 실천 예이다."
            ),
            "thinker_id": "sartre",
            "work_id": "sartre-existentialisme-humanisme",
            "related_terms": ["자유", "책임", "지식인", "실존주의"]
        },
        {
            "id": "sartre-kw-003",
            "thinker_id": "sartre",
            "term": "즉자존재 (En-soi)",
            "term_en": "Being-in-itself",
            "definition": (
                "사물·물체의 존재 방식. 자기 자신과 일치하며(A=A), 자신의 존재에 대해 문제 삼지 않고 "
                "그냥 있는 존재. 변화하지 않으며 내면에 부정(néant)을 품지 않는다. "
                "돌, 나무, 도구 등이 즉자존재이다. "
                "인간도 타인의 시선에 의해 객체화될 때 즉자존재처럼 응고된다."
            ),
            "thinker_id": "sartre",
            "work_id": "sartre-etre-neant",
            "related_terms": ["대자존재", "pour-soi", "존재와 무", "객체화"]
        },
        {
            "id": "sartre-kw-004",
            "thinker_id": "sartre",
            "term": "대자존재 (Pour-soi)",
            "term_en": "Being-for-itself",
            "definition": (
                "의식·인간의 존재 방식. 자신의 존재 안에 '무(néant)'를 품고 있어 "
                "자신이 무엇인지 끊임없이 문제 삼으며 자신을 초월하는 존재. "
                "과거에 의해 완전히 규정되지 않으며 항상 가능성으로 열려 있다. "
                "이 구조가 인간의 자유의 존재론적 근거이다."
            ),
            "thinker_id": "sartre",
            "work_id": "sartre-etre-neant",
            "related_terms": ["즉자존재", "en-soi", "자유", "무(néant)", "초월"]
        },
        {
            "id": "sartre-kw-005",
            "thinker_id": "sartre",
            "term": "자기기만 (Mauvaise foi)",
            "term_en": "Bad faith",
            "definition": (
                "인간이 자신의 자유와 책임을 부정하고 마치 규정된 본성을 가진 사물처럼 행동하는 태도. "
                "자기 자신에 대한 거짓말로, 외부 강제 없이 자발적으로 수행된다. "
                "불안(angoisse)에서 도피하기 위해 역할·습관·본성에 의해 완전히 규정된 척한다. "
                "반대 개념은 진정성(authenticité): 자신의 자유와 책임을 직면하는 태도."
            ),
            "thinker_id": "sartre",
            "work_id": "sartre-etre-neant",
            "related_terms": ["진정성", "불안", "자유", "책임", "역할"]
        },
        {
            "id": "sartre-kw-006",
            "thinker_id": "sartre",
            "term": "실존적 불안 (Angoisse)",
            "term_en": "Anguish / Anxiety",
            "definition": (
                "자신의 절대적 자유와 무근거성(groundlessness)을 직면할 때 느끼는 현기증. "
                "키르케고르의 불안(Angest) 개념을 계승하여 사르트르적으로 재해석했다. "
                "공포(peur)가 외부 위험에 대한 반응인 것과 달리, 불안은 자기 자신의 자유에 대한 반응이다. "
                "자기기만은 이 불안을 회피하려는 시도이다."
            ),
            "thinker_id": "sartre",
            "work_id": "sartre-etre-neant",
            "related_terms": ["자기기만", "자유", "책임", "구토", "진정성"]
        },
        {
            "id": "sartre-kw-007",
            "thinker_id": "sartre",
            "term": "자유와 책임 (Liberté et responsabilité)",
            "term_en": "Freedom and responsibility",
            "definition": (
                "사르트르 윤리학의 핵심 쌍. 인간의 절대적 자유는 절대적 책임을 수반한다. "
                "자신의 행동을 외부 환경·유전·심리·신·운명 등으로 돌리는 것은 자기기만이다. "
                "인간은 자신에게 일어나는 모든 일에 대해, 심지어 전쟁에 참여하는 것조차도, "
                "'그렇게 되도록 선택한' 자로서 책임을 진다. "
                "'나는 자유로 선고받았다(Je suis condamné à être libre).'"
            ),
            "thinker_id": "sartre",
            "work_id": "sartre-existentialisme-humanisme",
            "related_terms": ["앙가주망", "자기기만", "불안", "진정성", "실존주의"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """사르트르 관계 데이터 입력 (중복 확인 후 입력)."""
    relations_to_insert = [
        # kierkegaard → sartre (influenced): 실존 사상 계승
        {
            "id": "relation-kierkegaard-sartre",
            "from_thinker": "kierkegaard",
            "to_thinker": "sartre",
            "type": "influenced",
            "description": (
                "쇠렌 키르케고르(Søren Kierkegaard, 1813~1855)는 사르트르 실존주의의 선구자이다. "
                "키르케고르의 '실존(eksistens)' 개념, 즉 단독자(den Enkelte)로서 신 앞에 서는 "
                "개인의 구체적 실존을 강조한 것은 사르트르의 실존 중심 철학에 직접적 영감을 주었다. "
                "키르케고르가 '불안의 개념'(Begrebet Angest, 1844)에서 분석한 불안(Angest)은 "
                "사르트르의 불안(angoisse) 개념으로 이어진다. "
                "다만 키르케고르는 유신론적 실존주의를 전개한 반면, "
                "사르트르는 무신론적 실존주의를 전개하여 방향이 다르다."
            ),
            "strength": "보통",
            "period": "20세기 전반"
        },
        # heidegger → sartre (influenced): 현존재 분석의 영향
        {
            "id": "relation-heidegger-sartre",
            "from_thinker": "heidegger",
            "to_thinker": "sartre",
            "type": "influenced",
            "description": (
                "마르틴 하이데거(Martin Heidegger, 1889~1976)의 '존재와 시간'(Sein und Zeit, 1927)은 "
                "사르트르 현상학적 존재론의 직접적 토대이다. "
                "사르트르는 1933~1934년 베를린 유학 시절 하이데거의 존재론을 집중적으로 연구했으며, "
                "현존재(Dasein) 분석, 내던져있음(Geworfenheit), 기투(Entwurf), "
                "세계-내-존재(In-der-Welt-sein) 등의 개념을 사르트르식으로 변용했다. "
                "그러나 하이데거는 '휴머니즘에 관한 편지'(Brief über den Humanismus, 1947)에서 "
                "사르트르가 자신의 존재 분석을 주관주의적으로 왜곡했다고 비판했다."
            ),
            "strength": "강함",
            "period": "20세기 전반"
        },
        # sartre → beauvoir (influenced): 보부아르에게 영향
        {
            "id": "relation-sartre-beauvoir",
            "from_thinker": "sartre",
            "to_thinker": "beauvoir",
            "type": "influenced",
            "description": (
                "시몬 드 보부아르(Simone de Beauvoir, 1908~1986)는 사르트르의 지적 동반자로, "
                "사르트르의 실존주의를 페미니즘과 결합하여 '제2의 성'(Le Deuxième Sexe, 1949)을 저술했다. "
                "보부아르는 '여자로 태어나는 것이 아니라 여자가 되는 것이다(On ne naît pas femme: "
                "on le devient)'라는 명제를 통해 사르트르의 '실존은 본질에 앞선다'를 "
                "젠더 문제에 적용했다. "
                "두 사람의 관계는 상호 영향의 관계이기도 하나, "
                "사르트르의 실존주의적 틀이 보부아르 사상의 출발점이었다."
            ),
            "strength": "강함",
            "period": "20세기 중반"
        }
    ]

    inserted_count = 0
    for rel in relations_to_insert:
        # 중복 확인
        try:
            existing = client.get(index=INDEX_RELATIONS, id=rel["id"])
            print(f"[relation] {rel['id']}: SKIP (already exists)")
        except Exception:
            result = client.index(index=INDEX_RELATIONS, id=rel["id"], document=rel)
            print(f"[relation] {rel['id']}: {result['result']}")
            inserted_count += 1

    # nietzsche → sartre relation 확인 (이미 존재)
    try:
        existing = client.get(index=INDEX_RELATIONS, id="relation-nietzsche-sartre")
        print(f"[relation] relation-nietzsche-sartre: SKIP (already exists)")
    except Exception:
        rel = {
            "id": "relation-nietzsche-sartre",
            "from_thinker": "nietzsche",
            "to_thinker": "sartre",
            "type": "influenced",
            "description": (
                "프리드리히 니체(Friedrich Nietzsche, 1844~1900)의 '신의 죽음' 선언은 "
                "사르트르 실존주의의 핵심 전제이다. "
                "사르트르의 '실존은 본질에 앞선다'는 테제와 "
                "'인간은 자유를 선고받았다'는 명제는 "
                "신의 죽음 이후 인간이 스스로 가치를 창조해야 한다는 "
                "니체적 문제의식의 실존주의적 전개이다."
            ),
            "strength": "보통",
            "period": "20세기 중반"
        }
        result = client.index(index=INDEX_RELATIONS, id=rel["id"], document=rel)
        print(f"[relation] relation-nietzsche-sartre: {result['result']}")
        inserted_count += 1

    return inserted_count


def verify_data(client):
    """입력된 데이터를 전수 확인."""
    print("\n=== 전수 확인 ===")

    # refresh
    for idx in [INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS, INDEX_KEYWORDS, INDEX_RELATIONS]:
        client.indices.refresh(index=idx)

    # thinker 확인
    r = client.get(index=INDEX_THINKERS, id="sartre")
    print(f"[thinker] sartre: name={r['_source']['name_en']}, era={r['_source']['era']}")

    # works 확인
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "sartre"}})
    print(f"[works] sartre 저서 수: {works_count['count']}")
    works_result = client.search(
        index=INDEX_WORKS,
        query={"term": {"thinker_id": "sartre"}},
        _source=["id", "title_original", "year"]
    )
    for hit in works_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['title_original']} ({s['year']})")

    # claims 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "sartre"}})
    print(f"[claims] sartre 주장 수: {claims_count['count']}")
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "sartre"}},
        size=10,
        _source=["id", "claim", "argument", "counterpoint", "original_text", "original_text_ko", "verified"]
    )
    missing_fields = []
    for hit in claims_result['hits']['hits']:
        s = hit['_source']
        has_arg = bool(s.get('argument'))
        has_cp = bool(s.get('counterpoint'))
        has_ot = bool(s.get('original_text'))
        has_otko = bool(s.get('original_text_ko'))
        print(f"  - {s['id']}: argument={has_arg}, counterpoint={has_cp}, "
              f"original_text={has_ot}, original_text_ko={has_otko}, verified={s.get('verified')}")
        if not has_arg or not has_cp or not has_ot or not has_otko:
            missing_fields.append(s['id'])

    if missing_fields:
        print(f"[경고] 필수 필드 누락: {missing_fields}")
    else:
        print("[OK] 모든 claim에 argument+counterpoint+original_text+original_text_ko 존재")

    # keywords 확인
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "sartre"}})
    print(f"[keywords] sartre 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "sartre"}},
            {"term": {"to_thinker": "sartre"}}
        ]}},
        _source=["id", "from_thinker", "to_thinker", "type"]
    )
    rel_count = rel_result['hits']['total']['value']
    print(f"[relations] sartre 관련 관계 수: {rel_count}")
    for hit in rel_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['from_thinker']} --[{s['type']}]--> {s['to_thinker']}")

    return {
        "works": works_count['count'],
        "claims": claims_count['count'],
        "keywords": kw_count['count'],
        "relations": rel_count,
        "missing_fields": missing_fields
    }


def main():
    client = get_client()
    try:
        print("=== 장 폴 사르트르(Jean-Paul Sartre) 데이터 입력 시작 ===\n")

        print("1. 사상가 입력")
        insert_thinker(client)

        print("\n2. 저서 입력")
        works_n = insert_works(client)
        print(f"   총 {works_n}건 입력")

        print("\n3. 핵심 주장 입력")
        claims_n = insert_claims(client)
        print(f"   총 {claims_n}건 입력")

        print("\n4. 키워드 입력")
        kw_n = insert_keywords(client)
        print(f"   총 {kw_n}건 입력")

        print("\n5. 관계 입력")
        rel_n = insert_relations(client)
        print(f"   총 {rel_n}건 입력 (중복 제외)")

        stats = verify_data(client)
        print("\n=== 입력 완료 ===")
        print(f"works: {stats['works']}, claims: {stats['claims']}, "
              f"keywords: {stats['keywords']}, relations: {stats['relations']}")
        if stats['missing_fields']:
            print(f"[경고] 필수 필드 누락 claim: {stats['missing_fields']}")
        else:
            print("[OK] 모든 필수 필드 충족")

    finally:
        close_client(client)


if __name__ == "__main__":
    main()
