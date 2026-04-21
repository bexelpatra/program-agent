"""토마스 리코나(Thomas Lickona) 데이터를 ES에 직접 입력하는 스크립트."""

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
    """리코나 사상가 데이터 입력."""
    doc = {
        "id": "lickona",
        "name": "토마스 리코나",
        "name_en": "Thomas Lickona",
        "field": "moral_development",
        "era": "현대",
        "birth_year": 1943,
        "background": (
            "토마스 리코나는 1943년 미국에서 태어나 뉴욕주립대학교 코틀랜드 캠퍼스(SUNY Cortland)에서 "
            "발달심리학 및 교육학 교수로 오랫동안 재직했다. "
            "콜비 칼리지(Colby College) 및 보스턴 대학교에서 교육받았고, "
            "피아제와 콜버그의 인지발달적 도덕발달 연구를 계승하면서도 그 한계를 넘어서는 "
            "통합적 인격교육론을 체계화했다. "
            "1991년 출간한 『인격교육(Educating for Character)』은 미국 내 인격교육 운동의 핵심 텍스트로 "
            "자리 잡았으며, 이 책으로 리코나는 현대 인격교육 운동의 가장 중요한 이론가 중 한 명이 되었다. "
            "그는 '인격교육 파트너십(Character Education Partnership)'의 창립 멤버로 활동했고, "
            "미국 전역의 학교 인격교육 프로그램 개발에 직접 참여했다. "
            "리코나는 도덕교육을 단순한 가치 전달이나 도덕적 추론 훈련으로 환원하지 않고, "
            "인지·정서·행동을 아우르는 통합적 접근을 강조한다는 점에서 독특한 위치를 차지한다."
        ),
        "core_philosophy": (
            "리코나 인격교육론의 핵심은 도덕성을 세 가지 상호 연관된 구성 요소로 파악하는 것이다: "
            "도덕적 앎(moral knowing), 도덕적 느낌(moral feeling), 도덕적 행동(moral action). "
            "도덕적 앎은 도덕적 인식, 가치 인식, 관점 채택, 도덕적 추론, 의사결정, 자기 인식의 여섯 가지를 포함한다. "
            "도덕적 느낌은 양심, 자존감, 감정이입, 선의 사랑, 자기 통제, 겸손의 여섯 가지를 포함한다. "
            "도덕적 행동은 능력, 의지, 습관의 세 가지를 포함한다. "
            "리코나는 완전한 인격(good character)이란 이 세 요소 모두를 갖춘 상태라고 주장한다. "
            "이는 콜버그의 인지 중심 도덕발달론의 한계를 극복하면서도, "
            "단순한 덕목 목록 주입이라는 비판을 피하는 통합적 접근이다. "
            "핵심 덕목으로는 존중(respect)과 책임(responsibility)을 강조하며, "
            "이를 학교 전체의 문화적 변화(whole-school approach)를 통해 체계적으로 가르쳐야 한다고 주장한다."
        ),
        "philosophical_journey": (
            "초기(1970년대): 피아제와 콜버그의 인지발달적 도덕발달 연구를 수학하고 발달심리학자로 출발했다. "
            "이 시기에는 도덕적 추론 능력의 발달에 초점을 맞추었다. "
            "중기(1980년대): 콜버그 접근의 한계 — 인지적 추론 능력이 반드시 도덕적 행동으로 이어지지 않는다는 문제 — 를 "
            "인식하면서 도덕적 감정과 인격(character)의 역할에 주목하기 시작했다. "
            "아리스토텔레스의 덕윤리(virtue ethics)에서 이론적 자원을 발견하고, "
            "인격교육의 틀을 체계화했다. "
            "후기(1990년대 이후): 1991년 『인격교육』 출간으로 이론을 완성했으며, "
            "2004년 『인격의 문제(Character Matters)』에서 학교 문화 변화와 "
            "교사의 역할을 더욱 강조하는 방향으로 이론을 발전시켰다. "
            "미국 인격교육 운동의 이론적·실천적 선도자로 활동하며 "
            "전국적인 학교 개혁 프로그램의 기초를 제공했다."
        ),
        "keywords": [
            "인격교육",
            "도덕적 앎",
            "도덕적 느낌",
            "도덕적 행동",
            "핵심 덕목",
            "존중",
            "책임",
            "학교 전체 접근",
            "인격",
            "덕윤리"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="lickona", document=doc)
    print(f"[thinker] lickona: {result['result']}")
    return result


def insert_works(client):
    """리코나 저서 데이터 입력."""
    works = [
        {
            "id": "lickona-educating-for-character",
            "thinker_id": "lickona",
            "title": "인격교육",
            "title_original": "Educating for Character: How Our Schools Can Teach Respect and Responsibility",
            "year": 1991,
            "significance": (
                "리코나 인격교육론의 핵심 저작이자 현대 미국 인격교육 운동의 가장 중요한 이론서. "
                "도덕성을 도덕적 앎·도덕적 느낌·도덕적 행동의 세 요소로 구성된 것으로 체계화하고, "
                "학교에서 이 세 요소를 통합적으로 발달시킬 수 있는 구체적인 인격교육 방법론을 제시했다. "
                "핵심 덕목으로 존중과 책임을 강조하며, 이를 학교 전체 문화의 변화를 통해 "
                "실현하는 전략을 상세히 기술했다. "
                "출판 후 미국 전역의 학교 인격교육 프로그램에 지대한 영향을 미쳤다."
            ),
            "key_concepts": [
                "도덕적 앎", "도덕적 느낌", "도덕적 행동",
                "존중", "책임", "핵심 덕목",
                "학교 전체 접근", "인격교육", "교사의 역할"
            ]
        },
        {
            "id": "lickona-character-matters",
            "thinker_id": "lickona",
            "title": "인격의 문제",
            "title_original": "Character Matters: How to Help Our Children Develop Good Judgment, Integrity, and Other Essential Virtues",
            "year": 2004,
            "significance": (
                "『인격교육』의 후속작으로, 인격교육의 실천적 전략을 가정과 학교 양 측면에서 더욱 심화했다. "
                "10가지 핵심 덕목(지혜, 공정성, 용기, 자기통제, 사랑, 긍정적 태도, 근면, 성실성, 감사, "
                "겸손)을 제시하고 각각의 발달 방법을 구체적으로 안내했다. "
                "학교 문화 전반의 변화와 교사의 도덕적 모델 역할을 더욱 강조했다."
            ),
            "key_concepts": [
                "10가지 핵심 덕목", "학교 문화", "가정교육", "교사 모델",
                "인격교육 실천", "자기통제", "성실성"
            ]
        },
        {
            "id": "lickona-raising-good-children",
            "thinker_id": "lickona",
            "title": "좋은 아이 기르기",
            "title_original": "Raising Good Children: From Birth through the Teenage Years",
            "year": 1983,
            "significance": (
                "리코나의 초기 저작으로, 발달심리학과 도덕발달론을 바탕으로 "
                "부모가 자녀의 도덕 발달을 어떻게 도울 수 있는지를 단계적으로 안내한 책. "
                "콜버그의 도덕발달 단계론을 실제 양육 장면에 적용하면서도, "
                "이후 인격교육론으로 이어지는 통합적 접근의 맹아를 보여준다."
            ),
            "key_concepts": [
                "도덕발달 단계", "양육", "가정 도덕교육", "가치 내면화"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """리코나 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 도덕성의 세 요소 — 도덕적 앎·느낌·행동
        {
            "id": "lickona-claim-001",
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "source_detail": "Educating for Character, Chapter 3: The Components of Good Character",
            "claim": (
                "완전한 인격(good character)은 도덕적 앎(moral knowing), "
                "도덕적 느낌(moral feeling), 도덕적 행동(moral action)의 세 가지 요소로 구성되며, "
                "효과적인 도덕교육은 이 세 요소를 모두 발달시켜야 한다. "
                "도덕적으로 아는 것만으로는 부족하고, 도덕적으로 느끼고 행동하는 것까지 통합되어야 "
                "진정한 인격이 형성된다."
            ),
            "original_text": (
                "Good character consists of knowing the good, desiring the good, and doing the good — "
                "habits of the mind, habits of the heart, and habits of action. "
                "All three are necessary for leading a moral life; all three must be the object of good character education."
            ),
            "explanation": (
                "리코나는 도덕성을 세 상호 연관된 요소로 분석한다. "
                "도덕적 앎(moral knowing): 도덕적 인식, 가치 인식, 관점 채택, 도덕적 추론, 의사결정, 자기 인식의 여섯 하위 요소. "
                "도덕적 느낌(moral feeling): 양심, 자존감, 감정이입, 선의 사랑, 자기 통제, 겸손의 여섯 하위 요소. "
                "도덕적 행동(moral action): 능력, 의지, 습관의 세 하위 요소. "
                "세 요소는 서로 영향을 주고받으며, 어느 하나라도 결여되면 완전한 인격이 형성될 수 없다. "
                "예: 도덕적 앎만 있고 느낌이 없으면 냉담한 도덕주의자, 느낌만 있고 행동이 없으면 공허한 선의에 그친다."
            ),
            "argument": (
                "(1) 콜버그 등의 인지 중심 접근은 도덕적 추론 능력의 발달을 목표로 삼았으나, "
                "도덕적 추론이 뛰어난 사람도 도덕적으로 행동하지 않는 사례가 많다. "
                "(2) 아리스토텔레스의 덕윤리는 덕(virtue)이 앎·욕구·행동의 통합이라고 주장하는데, "
                "리코나는 이를 현대 도덕교육 맥락에서 재해석한다. "
                "(3) 따라서 도덕교육은 세 요소 모두를 체계적으로 발달시키는 통합적 접근이어야 한다."
            ),
            "counterpoint": (
                "콜버그 지지자들은 리코나의 접근이 덕목의 내용을 미리 결정하고 주입한다는 점에서 "
                "아동의 자율적 도덕 추론을 저해할 수 있다고 비판했다. "
                "핵심 덕목의 선택 자체가 특정 문화적 가치를 반영한다는 상대주의적 비판도 있다."
            ),
            "context": (
                "리코나는 1980년대 미국의 도덕적 위기(청소년 범죄, 학교 폭력, 가치관 혼란)에 대응하여 "
                "인격교육의 필요성을 제기했다. 인지 중심 접근의 한계를 극복하는 대안으로 "
                "통합적 인격교육을 제시한 것이다."
            ),
            "keywords": ["도덕적 앎", "도덕적 느낌", "도덕적 행동", "인격", "통합적 도덕교육"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-002: 도덕적 앎(moral knowing)의 여섯 구성 요소
        {
            "id": "lickona-claim-002",
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "source_detail": "Educating for Character, Chapter 3",
            "claim": (
                "도덕적 앎(moral knowing)은 여섯 가지 하위 요소로 구성된다: "
                "(1) 도덕적 인식(moral awareness) — 도덕적 문제 상황을 인식하는 능력, "
                "(2) 가치 인식(knowing moral values) — 핵심 도덕 가치를 이해하는 능력, "
                "(3) 관점 채택(perspective-taking) — 타인의 관점에서 이해하는 능력, "
                "(4) 도덕적 추론(moral reasoning) — 도덕적 판단을 추론하는 능력, "
                "(5) 의사결정(decision-making) — 도덕적 상황에서 좋은 결정을 내리는 능력, "
                "(6) 자기 인식(self-knowledge) — 자신의 도덕적 강점과 약점을 아는 능력."
            ),
            "original_text": None,
            "explanation": (
                "도덕적 앎은 단순한 지식 암기가 아니라 도덕적 상황에서 인지적으로 잘 기능하는 능력의 총체이다. "
                "도덕적 인식: '이 상황이 도덕적 문제를 포함하고 있는가'를 파악하는 능력. "
                "가치 인식: 존중, 책임, 정직 등 핵심 가치가 무엇인지, 왜 중요한지를 이해하는 것. "
                "관점 채택: 콜버그가 강조한 역할 교환 능력 — 타인이 어떻게 느끼고 생각하는지를 이해. "
                "도덕적 추론: 도덕적 딜레마에서 어떤 행동이 옳은지를 추론하는 능력. "
                "의사결정: 이해충돌 상황에서 모든 선택지와 결과를 고려하는 능력. "
                "자기 인식: 자신의 행동이 타인에게 미치는 영향, 자신의 편견과 약점을 아는 것."
            ),
            "argument": (
                "(1) 도덕교육이 단순히 규칙을 외우거나 딜레마 토론에만 집중하면 "
                "이 여섯 요소의 통합적 발달이 어렵다. "
                "(2) 관점 채택(perspective-taking)은 콜버그 이후 도덕발달론에서 핵심으로 인정받은 능력인데, "
                "이것이 도덕적 앎의 한 요소임을 명시함으로써 인지적 접근의 성과를 통합한다. "
                "(3) 자기 인식은 도덕적 자기조절의 토대로, 소크라테스의 '너 자신을 알라'에서 연원하는 덕이다."
            ),
            "counterpoint": (
                "이 여섯 요소의 발달을 어떻게 평가하고 측정할 것인지의 문제가 남는다. "
                "또한 요소들 간의 위계나 우선순위가 불분명하다는 비판이 있다."
            ),
            "context": (
                "리코나는 도덕교육을 단순화하거나 환원하지 않고, "
                "도덕성의 풍부하고 복잡한 구조를 드러내려 했다. "
                "도덕적 앎의 세분화는 도덕교육 프로그램 설계에 구체적 지침을 제공한다."
            ),
            "keywords": ["도덕적 앎", "도덕적 인식", "관점 채택", "도덕적 추론", "의사결정"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-003: 도덕적 느낌(moral feeling)의 여섯 구성 요소
        {
            "id": "lickona-claim-003",
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "source_detail": "Educating for Character, Chapter 3",
            "claim": (
                "도덕적 느낌(moral feeling)은 여섯 가지 하위 요소로 구성된다: "
                "(1) 양심(conscience) — 옳고 그름에 대한 내면의 감각, "
                "(2) 자존감(self-esteem) — 자신의 가치에 대한 건강한 인식, "
                "(3) 감정이입(empathy) — 타인의 감정과 상황을 공감하는 능력, "
                "(4) 선의 사랑(loving the good) — 좋은 것을 사랑하고 도덕적 행위에서 기쁨을 찾는 성향, "
                "(5) 자기 통제(self-control) — 충동과 욕망을 통제하는 능력, "
                "(6) 겸손(humility) — 자신의 한계를 인식하고 진리와 선에 열려 있는 태도."
            ),
            "original_text": None,
            "explanation": (
                "도덕적 느낌은 도덕적 앎을 실제 행동으로 연결하는 정서적 동기의 기반이다. "
                "양심: 단순한 죄책감이 아니라, 옳은 일을 하도록 이끄는 내면의 지침. "
                "자존감: 건강한 자존감은 자신을 도덕적 존재로 여기게 하고, "
                "나쁜 행동을 자신의 정체성과 불일치하게 느끼도록 한다. "
                "감정이입: 타인의 고통을 공감하고 돕고자 하는 동기의 핵심. "
                "선의 사랑: 도덕적 행동을 외적 강제가 아닌 내적 욕구로 하게 하는 것. "
                "자기 통제: 충동적 행동을 억제하는 의지력. "
                "겸손: 편견과 오만을 넘어서 도덕적 성장을 가능하게 하는 태도."
            ),
            "argument": (
                "(1) 감정이 도덕적 행동의 핵심 동기임을 강조함으로써, "
                "순수 이성 중심의 칸트 윤리학이나 콜버그식 접근의 한계를 보완한다. "
                "(2) 흄의 도덕 감정론 전통에서 도덕적 느낌의 중요성이 인정받아 왔으며, "
                "리코나는 이를 교육론적으로 체계화한다. "
                "(3) 특히 감정이입은 길리건의 배려윤리와도 연결되는 핵심 도덕 감정이다."
            ),
            "counterpoint": (
                "감정이 도덕교육의 대상이 될 수 있는지에 대한 의문이 있다. "
                "감정은 직접적으로 가르치기 어렵고, "
                "문화적 맥락에 따라 '올바른' 감정의 기준이 다를 수 있다는 비판도 있다."
            ),
            "context": (
                "리코나는 1980~90년대 미국 학교에서 도덕적 추론 훈련(콜버그 방식)이 "
                "실제 도덕적 행동 변화로 이어지지 않는다는 문제의식에서 "
                "도덕적 느낌의 발달을 강조했다."
            ),
            "keywords": ["도덕적 느낌", "양심", "감정이입", "자기 통제", "겸손", "선의 사랑"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-004: 도덕적 행동(moral action)의 세 구성 요소
        {
            "id": "lickona-claim-004",
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "source_detail": "Educating for Character, Chapter 3",
            "claim": (
                "도덕적 행동(moral action)은 세 가지 하위 요소로 구성된다: "
                "(1) 능력(competence) — 도덕적 판단을 실제 행동으로 옮길 수 있는 기술과 능력, "
                "(2) 의지(will) — 옳은 행동을 하겠다는 강한 결의와 결단력, "
                "(3) 습관(habit) — 반복된 실천을 통해 형성된 도덕적 행동 패턴. "
                "아리스토텔레스가 강조했듯, 덕은 반복적 실천을 통해 습관화될 때 비로소 진정한 덕이 된다."
            ),
            "original_text": None,
            "explanation": (
                "도덕적 행동은 앎과 느낌이 실제 행동으로 실현되는 차원이다. "
                "능력(competence): 경청, 갈등 해결, 협력, 의사소통 등 도덕적 판단을 행동으로 옮기는 데 필요한 기술. "
                "의지(will): 단기적 유혹이나 압박을 이기고 옳은 행동을 선택하는 의지력. "
                "  도덕적 용기(moral courage)는 의지의 핵심 요소. "
                "습관(habit): 아리스토텔레스의 에토스(ethos) 개념 — 덕스러운 행동을 반복하면 덕이 제2의 본성이 된다. "
                "  좋은 습관은 도덕적 노력 없이도 자동적으로 좋은 행동을 하게 만든다."
            ),
            "argument": (
                "(1) 좋은 의도만으로는 부족하다 — 실제로 행동할 능력과 반복 실천이 필요하다. "
                "(2) 아리스토텔레스: '우리는 용감한 행동을 함으로써 용감해진다(We become brave by doing brave acts).' "
                "  리코나는 이 습관화 논리를 도덕교육의 핵심 원리로 받아들인다. "
                "(3) 학교에서 봉사학습, 협동 프로젝트 등 실천 기회를 제공하는 것이 "
                "  도덕적 행동 습관 형성에 결정적이다."
            ),
            "counterpoint": (
                "습관화 강조는 맹목적 복종이나 외적 강제에 의한 행동 형성으로 이어질 위험이 있다. "
                "칸트는 덕이 의무에서 비롯된 자율적 결의여야 한다고 강조했는데, "
                "습관화된 행동이 진정한 도덕적 행위인지에 대한 의문이 제기될 수 있다."
            ),
            "context": (
                "리코나는 도덕교육이 교실 토론에 그쳐서는 안 되고, "
                "학생이 직접 도덕적 행동을 실천하는 경험을 제공해야 한다고 일관되게 강조한다."
            ),
            "keywords": ["도덕적 행동", "습관", "의지", "능력", "덕의 습관화", "도덕적 용기"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-005: 핵심 덕목과 보편적 가치
        {
            "id": "lickona-claim-005",
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "source_detail": "Educating for Character, Chapter 2: What Is Good Character?",
            "claim": (
                "존중(respect)과 책임(responsibility)은 학교 인격교육의 핵심 덕목이며, "
                "이 두 덕목은 문화와 종교의 차이를 넘어 인정될 수 있는 보편적 가치이다. "
                "존중은 자신과 타인, 모든 생명의 내재적 가치를 인정하는 것이고, "
                "책임은 자신의 행동에 대한 의무를 이행하는 것이다."
            ),
            "original_text": (
                "The two great moral values — values that virtually everyone agrees on across cultures — "
                "are respect and responsibility."
            ),
            "explanation": (
                "리코나는 도덕 상대주의를 거부하고, 보편적 핵심 덕목이 존재한다고 주장한다. "
                "존중(respect): 황금률('네가 대접받고자 하는 대로 남을 대접하라')에 근거. "
                "  자기 존중, 타인 존중, 모든 생명과 환경에 대한 존중을 포함. "
                "책임(responsibility): 자신의 행동 결과에 대한 책임, 사회적 의무, 공동선에 대한 기여. "
                "이 두 덕목은 이후 『인격의 문제』에서 10가지 덕목으로 확장된다. "
                "(정직, 공정성, 관용, 분별력, 자기 규율, 도움 주기, 연민, 협력, 용기, 민주적 가치 등)"
            ),
            "argument": (
                "(1) 비록 문화마다 덕목의 표현 방식은 다르지만, "
                "  존중과 책임은 거의 모든 문화 전통에서 핵심 가치로 인정된다. "
                "(2) 존중과 책임은 서로를 전제한다 — 타인을 존중하는 사람은 자신의 행동에 책임을 진다. "
                "(3) 이 두 덕목을 중심으로 하는 인격교육은 특정 종교나 이데올로기에 편향되지 않고 "
                "  공립학교에서 시행 가능하다."
            ),
            "counterpoint": (
                "어떤 덕목이 '보편적'인지를 누가 결정하는가의 문제가 있다. "
                "핵심 덕목 선택 자체가 특정 문화적·계층적 가치를 반영한다는 비판(맥파이크 등)이 있다. "
                "또한 덕목 목록을 제시하는 것이 덕목의 피상적 이해나 기계적 암기로 이어질 위험이 있다."
            ),
            "context": (
                "리코나는 1980년대 미국 공립학교에서 가치 중립 교육(values clarification, 래스 등)이 "
                "도덕 상대주의를 조장한다고 비판하면서, 보편적 가치에 기반한 인격교육을 주장했다."
            ),
            "keywords": ["핵심 덕목", "존중", "책임", "보편적 가치", "인격교육"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-006: 학교 전체 접근법(whole-school approach)
        {
            "id": "lickona-claim-006",
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "source_detail": "Educating for Character, Part III: Creating a Moral School Community",
            "claim": (
                "인격교육은 개별 수업이나 특정 프로그램으로 충분하지 않으며, "
                "학교 전체의 도덕 공동체(moral community)를 형성하는 '학교 전체 접근법(whole-school approach)'을 통해 "
                "이루어져야 한다. 교실, 복도, 운동장, 급식실 등 학교 생활 전반이 "
                "인격 발달의 장이 되어야 한다."
            ),
            "original_text": None,
            "explanation": (
                "리코나는 인격교육을 교실 안 수업에 국한하지 않고, "
                "학교 문화 전체의 변화를 요구하는 것으로 본다. "
                "교실 차원: 민주적 학급 운영, 협동학습, 학급 회의, 학급 규칙의 민주적 수립. "
                "학교 차원: 학교 분위기(school ethos), 학교 규칙과 규범, 전교적 봉사 프로그램. "
                "가정·지역사회 차원: 학부모 참여, 지역사회 봉사, 가정과의 협력. "
                "이 접근은 '잠재적 교육과정(hidden curriculum)'이 인격 형성에 미치는 영향을 중시한다."
            ),
            "argument": (
                "(1) 아동은 명시적 교육(explicit curriculum)보다 학교 생활 전반의 경험에서 더 많이 배운다. "
                "(2) 교사가 존중과 공정성을 가르치면서도 권위적으로 행동하면, "
                "  학생은 말보다 행동에서 배운다. "
                "(3) 학교 문화 전체가 인격교육의 원리를 구현해야 교실 수업의 효과가 극대화된다."
            ),
            "counterpoint": (
                "학교 전체 접근법은 모든 교사와 직원의 일관된 참여를 요구하는데, "
                "이를 실천하기가 어렵고 행정적 부담이 크다는 현실적 한계가 있다. "
                "또한 '학교 문화' 형성 자체가 특정 가치를 강제하는 동조 압력이 될 수 있다는 비판도 있다."
            ),
            "context": (
                "리코나는 인격교육을 교과목 한 시간의 문제가 아니라 "
                "학교 공동체 전체의 삶의 방식으로 보았다. "
                "이는 듀이의 민주적 학교 공동체론, 콜버그의 '공정한 공동체 학교'에서 영향을 받은 것이다."
            ),
            "keywords": ["학교 전체 접근", "도덕 공동체", "학교 문화", "잠재적 교육과정", "인격교육"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-007: 교사의 도덕적 멘토 역할
        {
            "id": "lickona-claim-007",
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "source_detail": "Educating for Character, Chapter 4: The Teacher as Caregiver, Model, and Mentor",
            "claim": (
                "교사는 단순한 지식 전달자가 아니라 "
                "돌봄 제공자(caregiver), 도덕적 모델(model), 도덕적 멘토(mentor)의 세 가지 역할을 해야 한다. "
                "교사 자신이 학생에게 인격의 살아있는 모범이 되어야 하며, "
                "이것이 인격교육의 가장 강력한 수단이다."
            ),
            "original_text": (
                "Teachers must be caregivers who foster students' self-worth and sense of belonging, "
                "models who show by personal example the meaning of good character, "
                "and mentors who guide and challenge students to develop their moral potential."
            ),
            "explanation": (
                "돌봄 제공자(caregiver): 학생 개개인의 복지와 성장에 진심으로 관심을 가지는 교사. "
                "  학생이 교사에게 존중받는다고 느낄 때 교사의 도덕적 권위가 형성된다. "
                "도덕적 모델(model): 교사의 모든 행동이 도덕 교육의 자료가 된다. "
                "  교사가 어떻게 갈등을 다루는지, 어떻게 공정하게 행동하는지가 학생에게 깊은 인상을 남긴다. "
                "도덕적 멘토(mentor): 학생의 도덕적 추론과 판단을 안내하고, "
                "  직접 가르치고(direct moral instruction), 도덕적 반성을 촉진하며, "
                "  도덕적으로 어렵지 않은 일에도 가치를 부여한다."
            ),
            "argument": (
                "(1) '모델링(modeling)'은 반두라(Bandura)의 사회학습 이론이 검증한 강력한 학습 메커니즘이다. "
                "(2) 교사와 학생의 관계의 질이 인격 형성에 결정적 영향을 미친다. "
                "(3) 교사가 모범을 보이지 않으면서 덕목을 가르치는 것은 역효과를 낸다."
            ),
            "counterpoint": (
                "교사에게 도덕적 완벽성을 요구하는 것은 비현실적이며, "
                "교사도 불완전한 도덕적 행위자임을 인정해야 한다는 비판이 있다. "
                "또한 교사의 가치관을 학생에게 강요하는 것이 될 수 있다는 자유주의적 우려도 있다."
            ),
            "context": (
                "리코나는 교사의 역할을 도덕교육의 핵심으로 보며, "
                "교사 양성 교육에서 인격교육 역량을 개발해야 한다고 주장한다."
            ),
            "keywords": ["교사의 역할", "도덕적 모델", "멘토", "돌봄", "인격교육"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-008: 콜버그 인지 중심 접근의 한계 — 감정과 행동 통합의 필요성
        {
            "id": "lickona-claim-008",
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "source_detail": "Educating for Character, Chapter 2",
            "claim": (
                "콜버그의 인지발달적 도덕교육 접근은 도덕적 추론 능력의 발달을 도덕교육의 목표로 삼았으나, "
                "이는 불완전하다. 도덕적으로 추론할 줄 아는 사람이 반드시 도덕적으로 행동하는 것은 아니며, "
                "도덕적 감정(느낌)과 도덕적 행동(습관)이 도덕적 앎과 함께 발달해야 진정한 인격이 형성된다."
            ),
            "original_text": None,
            "explanation": (
                "리코나는 콜버그 접근의 세 가지 한계를 지적한다. "
                "(1) 인지-행동 괴리: 높은 단계의 도덕적 추론이 반드시 도덕적 행동으로 이어지지 않는다. "
                "  워터게이트 사건 관련자들도 높은 수준의 도덕적 추론이 가능했다. "
                "(2) 감정 무시: 도덕적 감정(공감, 양심, 죄책감 등)이 행동 동기로서 중요한데, "
                "  콜버그는 이를 충분히 다루지 않았다. "
                "(3) 덕과 인격 무시: 반복적 실천을 통해 형성되는 덕목과 인격이 "
                "  도덕적 삶의 핵심인데, 인지 접근은 이를 경시한다."
            ),
            "argument": (
                "(1) 심리학 연구는 도덕 판단과 도덕 행동 사이의 간극을 일관되게 보여준다. "
                "(2) 아리스토텔레스의 덕윤리는 덕(virtue)이 앎·욕구·행동의 통합임을 이미 통찰했다. "
                "(3) 따라서 효과적인 도덕교육은 세 요소를 모두 포괄하는 접근이어야 한다."
            ),
            "counterpoint": (
                "콜버그 지지자들은 리코나의 비판이 콜버그 이론을 단순화한 것이라고 반론한다. "
                "콜버그도 학교를 도덕 공동체로 만드는 '공정한 공동체 학교(just community school)' 접근을 발전시켰다. "
                "또한 리코나 자신도 콜버그의 인지 발달 성과를 '도덕적 앎'에 통합한다."
            ),
            "context": (
                "리코나는 콜버그의 제자 격으로, 비판적 계승의 입장에서 인격교육론을 발전시켰다. "
                "이 주장은 인격교육 운동과 인지적 도덕발달론 사이의 핵심 논쟁점이다."
            ),
            "keywords": ["콜버그 비판", "인지 중심 접근의 한계", "도덕적 감정", "인격교육", "도덕발달"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-009: 덕목 가방(bag of virtues) 비판에 대한 재반론
        {
            "id": "lickona-claim-009",
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "source_detail": "Educating for Character, Chapter 2",
            "claim": (
                "콜버그는 인격교육을 '덕목 가방(bag of virtues)' 접근이라고 비판했는데, "
                "이는 덕목의 목록을 자의적으로 선택하여 아동에게 주입하는 교화(indoctrination)라는 것이다. "
                "그러나 리코나는 핵심 덕목을 가르치는 것이 교화가 아니며, "
                "오히려 아동의 도덕적 자율성 발달에 기여하는 방식으로 가르칠 수 있다고 반론한다."
            ),
            "original_text": None,
            "explanation": (
                "콜버그의 비판: 특정 덕목을 '핵심'으로 규정하고 가르치는 것은 "
                "(1) 덕목 선택의 자의성 문제, (2) 아동의 자율적 도덕 발달 저해, "
                "(3) 문화적 상대주의를 무시하는 가치 주입이라는 문제를 안고 있다. "
                "리코나의 재반론: "
                "(1) 보편적으로 인정될 수 있는 핵심 덕목(존중, 책임 등)이 존재한다. "
                "(2) 덕목은 주입이 아니라 이해, 경험, 실천을 통해 내면화될 수 있다. "
                "(3) 덕목을 가르치는 방식이 중요 — 이유를 함께 가르치고, 토론하고, 실천하게 하면 "
                "  교화가 아닌 자율적 내면화가 가능하다."
            ),
            "argument": (
                "(1) 덕목 교육을 거부하면 가치 중립 교육으로 귀결되는데, "
                "  이는 오히려 도덕 상대주의를 조장하는 결과를 낳는다. "
                "(2) 부모가 자녀에게 정직과 친절을 가르치는 것을 '교화'라고 부르지 않는 것처럼, "
                "  학교에서 존중과 책임을 가르치는 것도 교화가 아니다. "
                "(3) 리코나는 단순 암기나 주입이 아닌, 이해와 실천을 통한 내면화를 강조한다."
            ),
            "counterpoint": (
                "그럼에도 '보편적 핵심 덕목'의 경계는 결국 사회적 합의의 산물이며, "
                "누가 그 합의를 주도하는가의 권력 문제가 남는다. "
                "포스트모던 교육학자들은 어떤 덕목 교육도 지배 문화의 재생산 기능을 한다고 비판한다."
            ),
            "context": (
                "이 논쟁은 인격교육 vs. 인지발달적 도덕교육 간의 가장 중요한 이론적 대립점이며, "
                "1980~90년대 미국 도덕교육 논쟁의 핵심이었다."
            ),
            "keywords": ["덕목 가방 비판", "교화", "인격교육", "콜버그 비판", "보편적 덕목"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-010: 도덕교육에서 직접 교수와 간접 교수의 통합
        {
            "id": "lickona-claim-010",
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "source_detail": "Educating for Character, Part II: Teaching Character in the Classroom",
            "claim": (
                "효과적인 인격교육은 직접 교수(direct instruction)와 간접 교수(indirect instruction)를 통합해야 한다. "
                "직접 교수는 덕목의 의미와 중요성을 명시적으로 가르치는 것이고, "
                "간접 교수는 문학, 역사, 예술 등 교과 내용과 학교생활 전반을 통해 덕목을 자연스럽게 체득하게 하는 것이다."
            ),
            "original_text": None,
            "explanation": (
                "직접 교수 방법: 덕목에 대한 명시적 토론, 도덕적 딜레마 토론(콜버그 방식 수용), "
                "  덕목의 정의와 예시, 학급 회의, 봉사학습 반성 활동. "
                "간접 교수 방법: 좋은 문학작품을 통한 도덕적 공감 형성, "
                "  역사 속 도덕적 인물과 사건 탐구, 교사의 모델링, "
                "  학교 문화와 분위기를 통한 암묵적 교육. "
                "두 방법의 통합: 직접 교수는 도덕적 앎을 발달시키고, "
                "  간접 교수는 도덕적 느낌과 습관을 형성한다."
            ),
            "argument": (
                "(1) 순수한 직접 교수(설교, 훈계)는 학생의 반발을 살 수 있으며 피상적 암기에 그칠 수 있다. "
                "(2) 순수한 간접 교수만으로는 도덕적 앎의 체계적 발달이 부족하다. "
                "(3) 두 방법의 통합이 도덕적 앎·느낌·행동 세 요소를 균형 있게 발달시킨다."
            ),
            "counterpoint": (
                "두 방법을 통합하는 구체적 방법론이 교사마다 다르게 적용될 수 있으며, "
                "실제 수업에서 두 방법의 균형을 유지하기 어렵다는 현실적 한계가 있다."
            ),
            "context": (
                "리코나는 도덕교육이 별도의 '도덕 시간'에만 국한되어서는 안 되고, "
                "모든 교과 학습에 통합되어야 한다는 교육과정 통합론을 주장한다."
            ),
            "keywords": ["직접 교수", "간접 교수", "인격교육", "도덕 수업", "봉사학습"],
            "verified": False,
            "verification_log": []
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """리코나 핵심 키워드 데이터 입력."""
    keywords = [
        {
            "id": "kw-lickona-character-education",
            "term": "인격교육",
            "term_en": "character education",
            "definition": (
                "도덕성의 세 요소(도덕적 앎·느낌·행동)를 통합적으로 발달시키는 것을 목표로 하는 교육 접근. "
                "리코나가 체계화한 현대 인격교육론은 핵심 덕목(특히 존중과 책임)을 중심으로 "
                "학교 전체의 도덕 공동체를 형성하는 것을 강조한다. "
                "단순한 가치 암기나 도덕적 추론 훈련을 넘어서, "
                "덕스러운 인격을 갖춘 사람을 형성하는 것이 목표이다. "
                "1990년대 미국에서 급성장한 교육 운동으로, "
                "가치명료화 접근과 콜버그식 인지 접근 모두를 넘어서는 대안으로 제시되었다."
            ),
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "related_terms": ["도덕적 앎", "도덕적 느낌", "도덕적 행동", "핵심 덕목", "학교 전체 접근"]
        },
        {
            "id": "kw-lickona-moral-knowing",
            "term": "도덕적 앎",
            "term_en": "moral knowing",
            "definition": (
                "리코나의 인격교육론에서 도덕성의 첫 번째 구성 요소. "
                "도덕적 인식(moral awareness), 가치 인식, 관점 채택(perspective-taking), "
                "도덕적 추론, 의사결정, 자기 인식의 여섯 하위 요소로 구성된다. "
                "단순한 도덕 규칙의 암기가 아니라, 도덕적 상황을 인식하고, "
                "가치를 이해하며, 타인의 관점을 채택하고, 옳은 판단을 내리는 능력의 총체이다."
            ),
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "related_terms": ["도덕적 느낌", "도덕적 행동", "관점 채택", "도덕적 추론", "인격교육"]
        },
        {
            "id": "kw-lickona-moral-feeling",
            "term": "도덕적 느낌",
            "term_en": "moral feeling",
            "definition": (
                "리코나의 인격교육론에서 도덕성의 두 번째 구성 요소. "
                "양심(conscience), 자존감(self-esteem), 감정이입(empathy), "
                "선의 사랑(loving the good), 자기 통제(self-control), 겸손(humility)의 "
                "여섯 하위 요소로 구성된다. "
                "도덕적 앎을 실제 행동으로 연결하는 정서적 동기의 기반으로, "
                "콜버그식 인지 중심 접근이 경시한 도덕의 정서적 차원이다."
            ),
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "related_terms": ["도덕적 앎", "도덕적 행동", "양심", "감정이입", "자기 통제", "겸손"]
        },
        {
            "id": "kw-lickona-moral-action",
            "term": "도덕적 행동",
            "term_en": "moral action",
            "definition": (
                "리코나의 인격교육론에서 도덕성의 세 번째 구성 요소. "
                "능력(competence), 의지(will), 습관(habit)의 세 하위 요소로 구성된다. "
                "도덕적 앎과 느낌이 실제 행동으로 실현되는 차원으로, "
                "아리스토텔레스의 덕 습관화 이론('우리는 덕스러운 행동을 함으로써 덕스러워진다')에 근거한다. "
                "특히 습관(habit)의 형성이 중요한데, 좋은 행동을 반복함으로써 덕이 제2의 본성이 된다."
            ),
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "related_terms": ["도덕적 앎", "도덕적 느낌", "습관", "의지", "능력", "덕의 습관화"]
        },
        {
            "id": "kw-lickona-core-virtues",
            "term": "핵심 덕목",
            "term_en": "core virtues",
            "definition": (
                "리코나가 인격교육의 중심으로 삼는, 문화와 종교를 초월하여 보편적으로 인정될 수 있는 덕목들. "
                "대표적 핵심 덕목은 존중(respect)과 책임(responsibility)이며, "
                "이후 정직, 공정성, 관용, 자기 규율, 친절, 협력, 용기, 민주적 가치 등으로 확장된다. "
                "콜버그가 비판한 '덕목 가방(bag of virtues)' 접근과 달리, "
                "리코나는 이 덕목들이 이유와 함께 이해·경험·실천을 통해 내면화되어야 한다고 강조한다."
            ),
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "related_terms": ["존중", "책임", "인격교육", "덕목 가방 비판", "보편적 가치"]
        },
        {
            "id": "kw-lickona-respect",
            "term": "존중",
            "term_en": "respect",
            "definition": (
                "리코나의 핵심 덕목 중 하나. 자신과 타인, 모든 생명의 내재적 가치를 인정하고 "
                "그에 합당하게 대우하는 것. "
                "황금률('네가 대접받고자 하는 대로 남을 대접하라')에 근거하며, "
                "자기 존중, 타인 존중, 권위에 대한 적절한 존중, "
                "재산과 환경에 대한 존중을 포함한다. "
                "존중은 책임(responsibility)과 함께 모든 도덕 공동체의 기반이 되는 덕목이다."
            ),
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "related_terms": ["책임", "핵심 덕목", "황금률", "인격교육"]
        },
        {
            "id": "kw-lickona-responsibility",
            "term": "책임",
            "term_en": "responsibility",
            "definition": (
                "리코나의 핵심 덕목 중 하나. 자신의 행동과 그 결과에 대한 도덕적 의무를 인식하고 이행하는 것. "
                "개인적 차원의 책임(자신의 행동에 책임지기)과 사회적 차원의 책임(공동선에 기여하기)을 포함한다. "
                "책임감은 자기 통제(self-control), 근면함, 사회적 의무 이행과 연결된다. "
                "존중(respect)과 함께 모든 인격교육 프로그램의 핵심 덕목으로 강조된다."
            ),
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "related_terms": ["존중", "핵심 덕목", "자기 통제", "인격교육"]
        },
        {
            "id": "kw-lickona-whole-school-approach",
            "term": "학교 전체 접근",
            "term_en": "whole-school approach",
            "definition": (
                "리코나가 강조하는 인격교육의 실천 전략으로, "
                "인격교육을 특정 수업이나 프로그램에 한정하지 않고 "
                "학교 생활 전반에 걸쳐 통합적으로 실시하는 접근. "
                "교실(민주적 학급 운영, 협동학습), 학교 차원(학교 분위기, 전교 프로그램), "
                "가정·지역사회(학부모 참여, 봉사활동)를 모두 인격 발달의 장으로 만드는 것을 목표로 한다. "
                "잠재적 교육과정(hidden curriculum)이 명시적 교육과정만큼 인격 형성에 중요하다는 인식에 기반한다."
            ),
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "related_terms": ["인격교육", "도덕 공동체", "잠재적 교육과정", "학교 문화"]
        },
        {
            "id": "kw-lickona-empathy",
            "term": "감정이입",
            "term_en": "empathy",
            "definition": (
                "타인의 감정과 상황을 공감하는 능력. "
                "리코나의 인격교육론에서 도덕적 느낌(moral feeling)의 핵심 요소 중 하나. "
                "인지적 차원(타인의 관점 이해)과 정서적 차원(타인의 감정 공감)을 모두 포함한다. "
                "감정이입은 이타적 행동과 도움 행동의 핵심 동기가 되며, "
                "배려윤리(길리건, 나딩스)와도 연결되는 도덕적 능력이다. "
                "도덕교육에서 문학, 역할극, 봉사학습 등을 통해 발달시킬 수 있다."
            ),
            "thinker_id": "lickona",
            "work_id": "lickona-educating-for-character",
            "related_terms": ["도덕적 느낌", "배려", "관점 채택", "이타성"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """리코나 관계 데이터 입력."""
    relations = [
        {
            "from_thinker": "kohlberg",
            "to_thinker": "lickona",
            "type": "influenced",
            "description": (
                "콜버그의 인지발달적 도덕발달 이론이 리코나에게 출발점이 되었다. "
                "리코나는 콜버그의 도덕 발달 단계론, 역할 채택(role-taking) 능력, "
                "도덕적 추론 발달의 중요성을 수용하여 '도덕적 앎(moral knowing)'의 핵심 요소로 통합했다. "
                "그러나 동시에 리코나는 콜버그의 인지 중심 접근이 도덕적 감정과 행동을 충분히 다루지 못한다는 점에서 "
                "비판적으로 계승했다."
            ),
            "evidence": (
                "Lickona, Educating for Character (1991), Chapter 2: "
                "Kohlberg's approach as one component of the three-part model"
            )
        },
        {
            "from_thinker": "aristotle",
            "to_thinker": "lickona",
            "type": "influenced",
            "description": (
                "아리스토텔레스의 덕윤리(virtue ethics)가 리코나 인격교육론의 핵심 철학적 토대이다. "
                "아리스토텔레스의 '덕은 반복 실천을 통해 습관화된다(we become just by doing just acts)'는 주장이 "
                "리코나의 '도덕적 행동(moral action)' 개념, 특히 습관(habit)의 강조로 이어졌다. "
                "또한 덕을 앎·욕구·행동의 통합으로 본 아리스토텔레스의 통찰이 "
                "리코나의 도덕적 앎·느낌·행동의 세 요소 분석의 기원이 된다."
            ),
            "evidence": (
                "Lickona, Educating for Character (1991), Chapter 3: "
                "Aristotle's concept of virtue as habituated action"
            )
        },
        {
            "from_thinker": "lickona",
            "to_thinker": "kohlberg",
            "type": "criticized",
            "description": (
                "리코나는 콜버그의 인지발달적 도덕교육 접근이 도덕성의 인지적 측면만 강조하고 "
                "도덕적 감정(느낌)과 도덕적 행동(습관)을 충분히 다루지 않는다고 비판했다. "
                "또한 도덕적 추론 능력이 실제 도덕적 행동으로 이어지지 않는 '인지-행동 괴리'를 "
                "콜버그 접근의 근본적 한계로 지적했다."
            ),
            "evidence": (
                "Lickona, Educating for Character (1991), Chapter 2: "
                "Critique of cognitive-developmental approach"
            )
        },
        {
            "from_thinker": "piaget",
            "to_thinker": "lickona",
            "type": "influenced",
            "description": (
                "피아제의 도덕발달 이론과 인지발달론이 리코나의 도덕교육론에 간접적 영향을 미쳤다. "
                "피아제의 자율적 도덕성 개념과 협동을 통한 도덕 발달 강조가 "
                "리코나의 학교 민주 공동체론 및 협동학습 강조와 연결된다. "
                "리코나는 피아제-콜버그 전통의 발달심리학적 성과를 자신의 인격교육론에 통합했다."
            ),
            "evidence": "Lickona의 발달심리학적 배경; Raising Good Children (1983)에서 피아제·콜버그 단계 활용"
        }
    ]

    for i, rel in enumerate(relations):
        rel_id = f"rel-{rel['from_thinker']}-{rel['to_thinker']}-lickona-{i+1}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id}: {result['result']}")

    return len(relations)


def main():
    """메인 실행 함수."""
    print("=== 리코나(Lickona) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (lickona)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n✓ 리코나 데이터 입력 완료!")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}")
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
