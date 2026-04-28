"""로렌스 콜버그(Lawrence Kohlberg) 데이터를 ES에 직접 입력하는 스크립트."""

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
    """콜버그 사상가 데이터 입력."""
    doc = {
        "id": "kohlberg",
        "name": "로렌스 콜버그",
        "name_en": "Lawrence Kohlberg",
        "field": "moral_development",
        "era": "현대",
        "birth_year": 1927,
        "death_year": 1987,
        "background": (
            "미국 뉴욕 주 브롱스빌에서 태어났다. 제2차 세계대전 후 이스라엘 독립운동에 가담하여 "
            "유럽에서 이스라엘로 유대인 난민을 수송하는 선박의 항해사로 활동했는데, "
            "이 경험이 정의와 도덕 문제에 대한 실존적 관심으로 이어졌다. "
            "1948년 시카고 대학교에 입학하여 1년 만에 학사 학위를 취득했으며, "
            "같은 대학에서 심리학 박사 학위를 받았다(1958). 박사논문 「10세에서 16세 사이 소년들의 "
            "사고방식과 선택의 발달」에서 피아제의 도덕발달 이론을 확장하여 6단계 도덕발달 모델의 원형을 제시했다. "
            "예일 대학교, 시카고 대학교를 거쳐 1968년부터 하버드 대학교 교육대학원(HGSE) 교수로 재직하며 "
            "인간발달 및 교육 센터(Center for Moral Education)를 이끌었다. "
            "1971년 중남미 현지 연구 중 기생충 감염으로 극심한 고통을 겪었으며, "
            "1987년 보스턴 인근 해안에서 익사체로 발견되어 만성 우울증 및 투병 생활로 인한 자살로 추정된다. "
            "피아제의 인지발달론을 도덕 영역으로 확장하는 한편, 롤스의 정의론에서 철학적 기반을 강화했다. "
            "도덕교육에 대한 실천적 관심으로 정의공동체 학교 운동을 직접 실행에 옮겼다."
        ),
        "core_philosophy": (
            "콜버그 이론의 핵심은 도덕발달이 보편적인 3수준 6단계를 거쳐 순차적으로 진행된다는 것이다. "
            "수준 I(전인습적): 1단계(벌과 복종 지향) — 처벌을 피하기 위해 규칙에 복종하며, "
            "권위자의 힘이 옳고 그름의 기준이다. 2단계(도구적 상대주의 지향) — 자신의 이익 충족이 "
            "도덕 판단의 기준이며, 호혜적 교환의 논리('당신이 나를 긁어주면 나도 당신을 긁어줄게')가 작동한다. "
            "수준 II(인습적): 3단계(착한 소년·소녀 지향) — 다른 사람의 기대와 승인을 얻으려 하며, "
            "좋은 의도가 도덕 판단의 기준이다. 4단계(법과 질서 지향) — 사회 제도와 법을 유지하는 것이 "
            "도덕적 의무이며, 권위에 대한 존중과 사회 질서 유지가 핵심이다. "
            "수준 III(후인습적): 5단계(사회계약 지향) — 법은 상호 합의에 의한 사회계약임을 인식하고, "
            "다수의 의견과 기본권의 관계를 고려한다. 6단계(보편적 윤리 원칙 지향) — 스스로 선택한 "
            "보편적 윤리 원칙(정의, 인간 존엄성의 평등)에 따라 행동하며, 법이 이 원칙에 위배될 때 "
            "원칙을 따른다. 콜버그는 도덕 판단의 형식(구조)에 주목하고, 정의(justice)를 핵심 도덕 가치로 보았다. "
            "인지발달주의적 관점에서 도덕발달은 인지 발달에 기반하며, "
            "역할채택(role-taking) 능력의 확장을 통해 이루어진다고 보았다."
        ),
        "philosophical_journey": (
            "초기(1958): 시카고 대학교 박사논문에서 피아제의 2단계 도덕발달론을 확장하여 "
            "6단계 도덕발달 모델을 최초로 제시했다. 중기(1960~1970년대): 예일과 하버드에서 "
            "종단 연구(longitudinal study)를 통해 6단계의 보편성과 순서불변성을 검증했다. "
            "터키, 멕시코, 이스라엘 등 다른 문화권 연구로 단계의 문화 초월적 보편성을 주장했다. "
            "롤스의 「정의론」(1971)에서 철학적 기반을 강화하며, "
            "「도덕 발달의 철학」(1981)과 「도덕 발달의 심리학」(1984) 등 주저를 출간했다. "
            "후기(1970년대 말~1987): 길리건의 배려윤리 비판에 직면하고, "
            "6단계의 경험적 근거 부족 문제를 인정하면서 5단계와 5B 단계(자연법)로 수정을 검토했다. "
            "실천적 전환으로 보스턴 지역 클러스터 학교와 코네티컷 주 니에후스 교도소에서 "
            "정의공동체 접근(Just Community Approach)을 직접 실행했다. "
            "후기 강연에서 7단계(우주적·종교적 관점)의 가능성을 논의했다."
        ),
        "keywords": [
            "3수준 6단계",
            "전인습적 도덕성",
            "인습적 도덕성",
            "후인습적 도덕성",
            "정의공동체",
            "역할채택",
            "하인츠 딜레마",
            "+1 전략",
            "도덕적 분위기",
            "도덕 판단 면접(MJI)",
            "인지발달주의",
            "보편성",
            "도덕교육",
            "정의",
            "사회적 관점 채택"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="kohlberg", document=doc)
    print(f"[thinker] kohlberg: {result['result']}")
    return result


def insert_works(client):
    """콜버그 저서 데이터 입력."""
    works = [
        {
            "id": "kohlberg-dissertation-1958",
            "thinker_id": "kohlberg",
            "title": "10세에서 16세 사이 소년들의 사고방식과 선택의 발달",
            "title_original": "The Development of Modes of Thinking and Choices in Years 10 to 16",
            "year": 1958,
            "significance": (
                "콜버그의 시카고 대학교 박사논문으로, 6단계 도덕발달 모델의 원형을 최초로 제시한 저작. "
                "72명의 10~16세 소년들에게 도덕적 딜레마를 제시하고 면접한 결과를 분석했다. "
                "피아제의 2단계(타율적/자율적 도덕성)를 6단계로 세분화하고, "
                "도덕 판단의 형식적 구조가 연령에 따라 질적으로 변화함을 보였다. "
                "하인츠 딜레마(Heinz Dilemma)를 비롯한 도덕 판단 면접법(Moral Judgment Interview, MJI)의 원형이 여기서 등장한다."
            ),
            "key_concepts": [
                "6단계 도덕발달", "도덕 판단 면접", "하인츠 딜레마",
                "도덕 판단의 형식", "피아제 확장"
            ]
        },
        {
            "id": "kohlberg-philosophy-moral-development-1981",
            "thinker_id": "kohlberg",
            "title": "도덕 발달의 철학 — 도덕 단계와 교육의 이념",
            "title_original": "Essays on Moral Development, Vol. 1: The Philosophy of Moral Development",
            "year": 1981,
            "significance": (
                "콜버그 도덕발달론의 철학적 기초를 체계화한 주저. "
                "소크라테스, 칸트, 롤스의 정의 철학과 콜버그의 도덕발달 단계론의 관계를 논증했다. "
                "「정의로서의 도덕교육(Education for Justice)」, 「덕목가방에 대한 저항(The Bag of Virtues)」 등 "
                "중요 논문을 수록하고, 도덕적 상대주의에 대한 비판과 도덕 단계의 보편성을 옹호했다. "
                "후인습적 도덕성과 메타윤리학의 관계를 탐구하며, 6단계와 롤스 정의론의 연결을 시도했다."
            ),
            "key_concepts": [
                "도덕 단계의 보편성", "정의로서의 도덕교육", "덕목가방 비판",
                "인지발달주의 도덕교육", "메타윤리학", "소크라테스식 방법"
            ]
        },
        {
            "id": "kohlberg-psychology-moral-development-1984",
            "thinker_id": "kohlberg",
            "title": "도덕 발달의 심리학 — 도덕 단계의 본질과 타당성",
            "title_original": "Essays on Moral Development, Vol. 2: The Psychology of Moral Development",
            "year": 1984,
            "significance": (
                "콜버그 도덕발달론의 경험적·심리학적 기초를 집대성한 주저. "
                "도덕 단계의 측정 방법인 표준 쟁점 검사(Standard Issue Scoring)와 "
                "도덕 판단 면접(MJI) 방법론을 상세히 기술했다. "
                "종단 연구 결과를 통해 단계의 순서불변성과 상향 이동을 입증하려 했다. "
                "길리건의 배려윤리 비판과 정의공동체 접근에 대한 논의를 포함하며, "
                "도덕적 분위기(moral atmosphere)와 집단적 도덕 규범의 개념을 제시했다."
            ),
            "key_concepts": [
                "표준 쟁점 검사", "도덕 판단 면접(MJI)", "종단 연구",
                "도덕적 분위기", "정의공동체", "길리건 비판 대응"
            ]
        },
        {
            "id": "kohlberg-meaning-measurement-1981",
            "thinker_id": "kohlberg",
            "title": "도덕 발달의 의미와 측정",
            "title_original": "The Meaning and Measurement of Moral Development",
            "year": 1981,
            "significance": (
                "1979년 하이네만 기념 강연을 바탕으로 출간된 저작. "
                "콜버그 도덕발달 이론의 핵심 개념과 측정 방법을 간결하게 정리하며, "
                "도덕발달 연구의 방법론적 문제를 논의했다. "
                "교육자와 연구자들을 위한 이론의 실용적 적용을 안내한다."
            ),
            "key_concepts": [
                "도덕발달 측정", "단계 채점 방법", "교육적 함의"
            ]
        },
        {
            "id": "kohlberg-just-community-1985",
            "thinker_id": "kohlberg",
            "title": "정의공동체 접근 — 학교 민주주의와 도덕교육",
            "title_original": "The Just Community Approach to Moral Education in Theory and Practice",
            "year": 1985,
            "significance": (
                "콜버그와 동료들이 실천한 정의공동체 학교 접근을 이론적·실천적으로 기술한 저작. "
                "클러스터 학교(Cluster School)와 스컬데이 학교(Scarsdale Alternative High School) 등의 "
                "실제 사례를 통해 민주적 공동체 회의, 도덕적 분위기 형성, 집단 규범 발전 과정을 기술했다. "
                "개인 중심의 인지발달주의 접근에서 공동체·집단 중심의 접근으로 이론을 확장한 저작이다."
            ),
            "key_concepts": [
                "정의공동체 학교", "공동체 회의", "도덕적 분위기",
                "집단 규범", "학교 민주주의", "직접 민주주의"
            ]
        },
        {
            "id": "kohlberg-moral-stages-moralization-1976",
            "thinker_id": "kohlberg",
            "title": "도덕 단계와 도덕화: 인지발달주의 접근",
            "title_original": "Moral Stages and Moralization: The Cognitive-Developmental Approach",
            "year": 1976,
            "significance": (
                "T. 리코나(T. Lickona) 편저 「도덕 발달과 행동」에 수록된 핵심 논문. "
                "인지발달주의 도덕교육론의 개요를 가장 체계적으로 제시한 텍스트로 널리 인용된다. "
                "도덕 단계의 특성, 측정, 교육적 함의를 간결하게 정리하고, "
                "행동주의적 덕교육(character education)과 사회화(socialization) 접근에 대한 비판을 담고 있다. "
                "인지적 불균형(cognitive disequilibrium)을 통한 도덕발달 촉진 원리를 제시했다."
            ),
            "key_concepts": [
                "인지발달주의 도덕교육", "인지적 불균형", "덕교육 비판",
                "단계 특성", "도덕화 과정"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """콜버그 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 도덕발달 3수준 6단계 — 전체 개요
        {
            "id": "kohlberg-claim-001",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-philosophy-moral-development-1981",
            "source_detail": "The Philosophy of Moral Development, Ch. 2",
            "claim": (
                "도덕발달은 보편적인 3수준 6단계를 거쳐 순차적으로 진행된다. "
                "수준 I(전인습적): 1단계(벌과 복종 지향), 2단계(도구적 상대주의 지향). "
                "수준 II(인습적): 3단계(착한 소년·소녀 지향), 4단계(법과 질서 지향). "
                "수준 III(후인습적): 5단계(사회계약 지향), 6단계(보편적 윤리 원칙 지향). "
                "각 단계는 이전 단계의 사고를 포함하면서 더 높은 수준의 도덕적 추론 구조를 형성한다."
            ),
            "explanation": (
                "콜버그는 피아제의 2단계를 6단계로 세분화하였다. 각 단계는 이전 단계와 질적으로 다른 "
                "인지-도덕적 구조를 가지며, 단계 순서는 문화를 초월하여 불변한다. "
                "대부분의 성인은 3~4단계에 머물며, 5~6단계에 도달하는 사람은 소수이다."
            ),
            "argument": (
                "도덕 판단은 단순한 감정이나 학습된 습관이 아니라 인지 구조에 기반하므로, "
                "인지 발달과 마찬가지로 단계적으로 발달한다. "
                "각 단계는 보다 통합적이고 복잡한 사회적 관점을 반영하며, "
                "상위 단계는 하위 단계의 내적 모순을 해결한다."
            ),
            "counterpoint": (
                "길리건(Gilligan)은 이 단계가 남성 중심 편향을 가지며 배려와 관계의 도덕을 과소평가한다고 비판했다. "
                "엠마(Emmet) 등은 6단계가 경험적으로 거의 관찰되지 않는다는 문제를 제기했다. "
                "문화권에 따라 도덕 판단의 내용이 크게 다를 수 있다는 비판도 있다."
            ),
            "context": (
                "콜버그가 1958년 박사논문에서 처음 제시한 이후, 수십 년에 걸친 종단 연구와 "
                "다문화 연구를 통해 이론을 정교화하고 검증했다."
            ),
            "keywords": ["3수준 6단계", "도덕발달", "전인습적", "인습적", "후인습적", "순서불변성"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-002: 1단계 — 벌과 복종 지향
        {
            "id": "kohlberg-claim-002",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-psychology-moral-development-1984",
            "source_detail": "The Psychology of Moral Development, Standard Issue Scoring Manual",
            "claim": (
                "1단계(벌과 복종 지향): 옳은 행동이란 처벌을 피하고 권위에 복종하는 것이다. "
                "행동의 옳고 그름은 그에 따르는 처벌의 유무와 크기로 판단되며, "
                "규칙은 권위자가 부과한 절대적인 것으로 받아들여진다. "
                "사회적 관점: 자기중심적(egocentric) — 타인의 관점을 고려하지 못한다."
            ),
            "explanation": (
                "이 단계는 피아제의 타율적 도덕성과 유사하다. 아동은 규칙의 사회적 맥락이나 "
                "목적을 이해하지 못하고, 단지 권위자의 명령과 그에 따른 처벌을 기준으로 행동한다. "
                "하인츠 딜레마에서 '훔치면 감옥에 가니까 훔치면 안 된다'는 식의 응답이 전형적이다."
            ),
            "argument": (
                "도덕 판단의 첫 번째 구조는 물리적 결과(처벌)에 근거하며, "
                "이는 아동이 아직 타인의 관점을 충분히 채택하지 못하는 인지 발달 수준에 상응한다."
            ),
            "counterpoint": (
                "벌이 도덕교육의 필요 요소라는 주장도 있으나, 콜버그는 처벌 중심 교육이 "
                "도덕발달을 촉진하기보다 1단계에 고착시킬 위험이 있다고 보았다."
            ),
            "context": "3수준 6단계 이론에서 가장 초보적인 도덕적 추론 구조.",
            "keywords": ["1단계", "벌과 복종", "자기중심적 관점", "전인습적"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-003: 2단계 — 도구적 상대주의 지향
        {
            "id": "kohlberg-claim-003",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-psychology-moral-development-1984",
            "source_detail": "The Psychology of Moral Development, Standard Issue Scoring Manual",
            "claim": (
                "2단계(도구적 상대주의 지향): 옳은 행동이란 자신의 필요와 이익을 충족하는 것이며, "
                "때로는 타인의 필요도 충족된다. 호혜적 교환의 논리 — '당신이 나를 긁어주면 나도 당신을 긁어줄게' "
                "— 가 도덕 판단의 기준이다. 공정성은 동등한 교환으로 이해된다. "
                "사회적 관점: 개인주의적(individualistic) — 타인을 자신의 목적 달성을 위한 수단으로 본다."
            ),
            "explanation": (
                "2단계에서 아동은 타인도 자신의 이익을 가진다는 것을 인식하지만, "
                "도덕적 의무는 여전히 자기 이익에 근거한다. 하인츠 딜레마에서 "
                "'아내를 사랑하면 훔칠 수도 있지만, 어차피 감옥 가면 아무 소용없다'는 식의 응답이 전형적이다."
            ),
            "argument": (
                "이 단계에서는 타인의 관점을 부분적으로 인식하기 시작하지만, "
                "도덕성을 상호 이익의 교환으로만 이해하는 단계이다."
            ),
            "counterpoint": "일부 연구자들은 2단계와 3단계 사이의 구분이 실제 도덕 판단에서 명확하지 않다고 지적한다.",
            "context": "전인습적 수준의 두 번째 단계로, 자기중심적 관점에서 상호주의적 관점으로의 이행기.",
            "keywords": ["2단계", "도구적 상대주의", "호혜적 교환", "개인주의적 관점"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-004: 3단계 — 착한 소년·소녀 지향
        {
            "id": "kohlberg-claim-004",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-psychology-moral-development-1984",
            "source_detail": "The Psychology of Moral Development, Standard Issue Scoring Manual",
            "claim": (
                "3단계(착한 소년·소녀 지향, 상호적 대인 관계 도덕성): 옳은 행동이란 "
                "가까운 사람들 — 가족, 친구 — 의 기대와 승인에 부응하는 것이다. "
                "'좋은 사람'이 되는 것이 도덕의 핵심이며, 좋은 동기(의도)가 행동의 도덕성을 결정한다. "
                "황금률(남에게 대접받고자 하는 대로 남을 대접하라)이 적용되기 시작한다. "
                "사회적 관점: 공유된 감정, 합의, 기대를 우선시하는 관계 중심 관점."
            ),
            "explanation": (
                "이 단계에서는 추상적인 사회적 승인과 관계 유지가 도덕 판단의 핵심이 된다. "
                "하인츠 딜레마에서 '좋은 남편이라면 아내를 위해 훔칠 것이다'거나 "
                "'남의 것을 훔치는 것은 나쁜 사람이 하는 짓이다'는 식의 응답이 전형적이다."
            ),
            "argument": (
                "인습적 수준의 첫 단계로, 이제 도덕 판단은 개인의 이해관계를 넘어서 "
                "타인의 기대와 관계 유지라는 사회적 차원을 고려한다."
            ),
            "counterpoint": (
                "길리건은 이 단계에서 나타나는 배려와 관계 중심 사고가 콜버그 체계에서 "
                "4단계보다 '낮은' 단계로 취급된다고 비판했다. 이는 여성적 도덕성에 대한 편향이라고 주장했다."
            ),
            "context": "인습적 수준의 첫 번째 단계로, 대인 관계와 사회적 승인이 도덕 판단의 중심이 되는 시기.",
            "keywords": ["3단계", "착한 소년·소녀", "대인관계 도덕성", "승인 지향", "인습적"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-005: 4단계 — 법과 질서 지향
        {
            "id": "kohlberg-claim-005",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-psychology-moral-development-1984",
            "source_detail": "The Psychology of Moral Development, Standard Issue Scoring Manual",
            "claim": (
                "4단계(법과 질서 지향, 사회체계 도덕성): 옳은 행동이란 의무를 이행하고, "
                "법을 준수하며, 사회 제도와 질서를 유지하는 것이다. "
                "법은 단순한 인간관계의 합의가 아니라 사회 전체를 유지하는 필수적 제도이다. "
                "사회적 관점: 사회 체계 관점 — 개인들의 관계가 아닌 사회 전체의 관점에서 도덕을 판단한다."
            ),
            "explanation": (
                "대부분의 성인이 도달하는 가장 높은 인습적 단계이다. "
                "하인츠 딜레마에서 '법을 어기면 사회 질서가 무너지므로 훔치면 안 된다' 또는 "
                "'아무리 어렵더라도 사유재산권은 보호되어야 한다'는 식의 응답이 전형적이다."
            ),
            "argument": (
                "이 단계에서는 사회 제도와 법이 개인들 간의 합의 이상의 권위를 가진다는 것을 인식한다. "
                "사회가 기능하려면 법과 질서가 유지되어야 하며, 이것이 도덕적 의무의 근거이다."
            ),
            "counterpoint": (
                "4단계에 고착된 사람은 악법에도 복종하는 경향이 있으며, 나치 독일의 '명령에 따른' "
                "범죄자들이 이 단계에 해당한다는 비판이 있다. 콜버그 자신도 이를 '전체주의의 위험'으로 인식했다."
            ),
            "context": "인습적 수준의 최고 단계로, 서구 민주주의 성인 대다수가 이 수준에 머무는 것으로 나타났다.",
            "keywords": ["4단계", "법과 질서", "사회체계 관점", "의무", "인습적"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-006: 5단계 — 사회계약 지향
        {
            "id": "kohlberg-claim-006",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-philosophy-moral-development-1981",
            "source_detail": "The Philosophy of Moral Development, Ch. 5",
            "claim": (
                "5단계(사회계약 지향): 법은 절대적 명령이 아니라 공동의 복지를 위한 사회적 계약임을 인식한다. "
                "법은 민주적 합의에 의해 만들어지고 변경될 수 있으며, "
                "기본적 권리(생명권, 자유권)는 사회계약에 앞서 존재한다. "
                "법이 기본권을 침해할 때 그 법은 정당하지 않다. "
                "사회적 관점: 사회선행적(prior-to-society) 관점 — 사회를 구성하기 전 개인들의 권리와 합의를 고려한다."
            ),
            "explanation": (
                "이 단계는 미국 헌법 및 공리주의적 관점과 유사하다. "
                "하인츠 딜레마에서 '생명권은 재산권보다 중요하므로 훔치는 것이 정당화될 수 있다'는 식의 응답이 전형적이다. "
                "미국 공공 지도자들의 도덕적 논증에서 빈번히 나타난다."
            ),
            "argument": (
                "후인습적 수준의 첫 단계로, 법의 도덕적 기초인 사회계약을 인식함으로써 "
                "법과 도덕을 분리하고, 법을 비판적으로 평가할 수 있게 된다."
            ),
            "counterpoint": (
                "5단계와 6단계의 구분이 지나치게 추상적이며, 실제 연구에서 두 단계를 분리하기 어렵다는 비판이 있다. "
                "콜버그 본인도 후기에 6단계의 경험적 관찰 부족 문제를 인정했다."
            ),
            "context": "후인습적 도덕성의 진입 단계로, 사회 체계 너머 보편적 원칙의 인식으로 나아가는 중간 단계.",
            "keywords": ["5단계", "사회계약", "기본권", "후인습적", "사회선행적 관점"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-007: 6단계 — 보편적 윤리 원칙 지향
        {
            "id": "kohlberg-claim-007",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-philosophy-moral-development-1981",
            "source_detail": "The Philosophy of Moral Development, Ch. 6",
            "claim": (
                "6단계(보편적 윤리 원칙 지향): 옳은 행동이란 스스로 선택한 보편적 윤리 원칙에 따른 것이다. "
                "법이나 사회적 합의가 이 원칙에 어긋날 때는 원칙을 따른다. "
                "보편적 원칙은 모든 인간의 존엄성 평등, 정의, 인격의 목적적 가치에 관한 것이다. "
                "칸트의 정언명령('인간을 수단이 아닌 목적으로 대우하라')과 롤스의 정의 원칙이 이 단계의 철학적 근거이다. "
                "사회적 관점: 도덕적 관점 — 모든 합리적 인간이 동의할 수 있는 관점에서 판단한다."
            ),
            "explanation": (
                "6단계는 소크라테스, 간디, 마틴 루서 킹 Jr.와 같은 도덕적 영웅들에게서 "
                "구현되는 것으로 제시된다. 하인츠 딜레마에서 '생명의 가치는 재산의 가치보다 절대적으로 우선하며, "
                "어떤 합리적 존재도 이에 동의할 것이므로 훔치는 것이 도덕적으로 올바르다'는 식의 응답이 전형적이다."
            ),
            "argument": (
                "도덕발달의 최고 단계는 모든 상황, 모든 문화에서 적용 가능한 보편적 원칙에 도달하는 것이다. "
                "이 단계에서는 개인의 권리와 인간 존엄성의 평등이 모든 실정법과 사회 규범을 초월한다."
            ),
            "counterpoint": (
                "콜버그 자신이 후기에 6단계가 경험적 연구에서 거의 관찰되지 않음을 인정하며 5단계와 통합을 검토했다. "
                "길리건은 6단계가 추상적 정의 원칙만을 강조하고 구체적 관계와 배려를 무시한다고 비판했다."
            ),
            "context": "3수준 6단계 이론의 정점으로, 철학적·이론적 이상을 표현하지만 경험적 타당성 논란이 있다.",
            "keywords": ["6단계", "보편적 윤리 원칙", "정의", "인간 존엄성", "후인습적", "칸트", "롤스"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-008: 도덕발달의 보편성
        {
            "id": "kohlberg-claim-008",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-philosophy-moral-development-1981",
            "source_detail": "The Philosophy of Moral Development, Ch. 3",
            "claim": (
                "도덕발달의 3수준 6단계는 문화를 초월한 보편적 순서로 진행된다. "
                "미국, 터키, 멕시코, 이스라엘, 인도, 태만, 케냐 등 다양한 문화권 연구에서 "
                "동일한 단계 순서가 확인되었다. 단계의 순서는 건너뛰거나 역행하지 않는다. "
                "문화마다 도덕 판단의 내용(무엇이 옳은가)은 다를 수 있지만, "
                "도덕 추론의 형식(어떻게 판단하는가)은 보편적 단계 순서를 따른다."
            ),
            "explanation": (
                "콜버그는 도덕발달이 본성과 환경의 상호작용이지만, 그 구조적 순서는 "
                "인간 인지 발달의 보편적 특성에 의해 결정된다고 주장했다. "
                "이는 문화 상대주의에 대한 강력한 반론이며, 도덕 판단에 절대적 기준이 존재함을 함축한다."
            ),
            "argument": (
                "다양한 문화권의 종단 연구에서 단계 순서의 보편성이 지지되었다. "
                "인지 발달의 보편성(피아제의 발견)이 도덕 발달에도 적용된다. "
                "단계의 논리적 구조는 더 높은 단계가 하위 단계의 내적 모순을 해결하는 방식으로 구성된다."
            ),
            "counterpoint": (
                "슈웨더(Shweder)는 인도 문화에서 다른 도덕적 사고방식이 나타난다며 보편성 주장에 의문을 제기했다. "
                "Snarey(1985)는 문화권에 따라 5~6단계에 도달하는 빈도가 크게 다르다고 보고했다. "
                "단계 판정 과정이 서구적 개인주의 편향을 내포할 수 있다는 비판도 있다."
            ),
            "context": "콜버그가 1960~70년대 다문화 비교 연구를 통해 이론의 보편성을 주장한 핵심 테제.",
            "keywords": ["보편성", "단계 순서", "문화 비교 연구", "순서불변성", "도덕 상대주의 비판"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-009: 역할채택(role-taking)
        {
            "id": "kohlberg-claim-009",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-psychology-moral-development-1984",
            "source_detail": "The Psychology of Moral Development, Ch. 4",
            "claim": (
                "역할채택(role-taking) — 타인의 관점, 생각, 감정을 자신의 것처럼 취하는 능력 — 이 "
                "도덕발달의 핵심 인지적 메커니즘이다. "
                "도덕발달의 각 단계는 더 복잡하고 확장된 역할채택 능력을 반영한다. "
                "1단계: 자기중심적(역할채택 부재) → 2단계: 거울적(mirror) → 3단계: 이자(dyadic) → "
                "4단계: 사회 체계 → 5단계: 사회선행적 → 6단계: 도덕적 관점. "
                "도덕교육에서 타인의 관점을 직접 경험할 기회(역할극, 딜레마 토론)는 발달을 촉진한다."
            ),
            "explanation": (
                "콜버그는 셀만(Selman)의 사회적 관점 채택 이론과 연계하여 "
                "역할채택 능력의 발달이 도덕발달의 필요조건임을 주장했다. "
                "역할채택은 공감과 다르며, 인지적 조망수용(perspective-taking)의 차원이다."
            ),
            "argument": (
                "도덕 판단은 자신과 타인의 이익을 공정하게 고려하는 것을 요구하며, "
                "이는 타인의 관점을 인지적으로 채택하는 능력 없이는 불가능하다. "
                "역할채택 능력은 인지 발달의 탈중심화(decentration)와 함께 성장한다."
            ),
            "counterpoint": (
                "역할채택이 도덕발달의 충분조건은 아니다. 소시오패스는 역할채택 능력이 있지만 "
                "그것을 조작에 활용한다. 블라시(Blasi)는 도덕적 자아 정체성이 더 중요하다고 주장했다."
            ),
            "context": "콜버그가 피아제의 탈중심화 개념을 도덕 영역으로 확장한 핵심 메커니즘.",
            "keywords": ["역할채택", "사회적 관점 채택", "탈중심화", "도덕발달 메커니즘"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-010: 하인츠 딜레마와 도덕 판단 면접(MJI)
        {
            "id": "kohlberg-claim-010",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-dissertation-1958",
            "source_detail": "박사논문 및 MJI 채점 매뉴얼",
            "claim": (
                "도덕 판단의 단계는 '하인츠 딜레마(Heinz Dilemma)'와 같은 가상적 도덕 갈등 상황에서 "
                "이유와 논거를 분석하는 도덕 판단 면접(Moral Judgment Interview, MJI)으로 측정된다. "
                "하인츠 딜레마: 아내가 희귀한 암으로 죽어가고 있는데, 약값이 너무 비싸 살 수 없다면 "
                "하인츠는 약을 훔쳐야 하는가? "
                "중요한 것은 행동 선택(Yes/No)이 아니라 그 이유(reasoning)이며, "
                "이유의 구조가 단계를 결정한다."
            ),
            "explanation": (
                "MJI는 9가지 도덕 딜레마를 포함하며, 각 딜레마에 대한 피험자의 응답을 "
                "표준 쟁점 채점법(Standard Issue Scoring)으로 분석하여 도덕 발달 단계를 산출한다. "
                "판단 내용보다 판단 구조를 평가하는 것이 핵심이다."
            ),
            "argument": (
                "도덕 단계는 행동이 아니라 도덕 추론의 형식적 구조에 나타난다. "
                "행동은 여러 요인에 의해 결정되지만, 도덕 추론의 구조는 발달 단계를 반영한다."
            ),
            "counterpoint": (
                "레스트(Rest)는 MJI의 개방형 면접 방식이 시간이 많이 걸리고 평가자 간 신뢰도 문제가 있다며, "
                "선택형 DIT(Defining Issues Test)를 개발했다. "
                "가상 딜레마 응답이 실제 도덕 행동과 일치하지 않는다는 비판도 있다."
            ),
            "context": "콜버그가 박사논문에서 개발한 이후 수십 년간 도덕발달 연구의 표준 측정 도구.",
            "keywords": ["하인츠 딜레마", "도덕 판단 면접(MJI)", "도덕 추론 구조", "판단 내용 vs 구조"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-011: +1 전략 (Plus-one strategy)
        {
            "id": "kohlberg-claim-011",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-moral-stages-moralization-1976",
            "source_detail": "Moral Stages and Moralization, in T. Lickona (Ed.) Moral Development and Behavior",
            "claim": (
                "+1 전략(Plus-one strategy): 도덕교육에서 교사는 학생의 현재 도덕 발달 단계보다 "
                "정확히 한 단계 높은 수준(+1)의 도덕적 논증을 제시해야 한다. "
                "동일 단계 또는 그보다 낮은 단계의 논증은 인지적 불균형을 일으키지 않으며, "
                "두 단계 이상 높은 논증은 학생이 이해하지 못한다. "
                "인지적 불균형(cognitive disequilibrium) — 현재 사고 구조로 해결할 수 없는 갈등 — "
                "이 발달의 동력이다."
            ),
            "explanation": (
                "피아제의 인지발달 메커니즘을 도덕 영역에 적용한 교육 전략이다. "
                "교사가 학생보다 한 단계 높은 도덕적 관점을 제시하면, "
                "학생은 그 관점을 부분적으로 이해하면서 자신의 현재 사고의 한계를 직면하고 "
                "상위 단계로 이행하도록 자극받는다."
            ),
            "argument": (
                "도덕발달은 강의나 규칙 암기가 아닌, 실제적인 인지 갈등을 통해 이루어진다. "
                "+1 전략은 학생의 현재 수준을 존중하면서도 발달을 촉진하는 최적의 접근이다."
            ),
            "counterpoint": (
                "교사가 학생의 정확한 도덕 발달 단계를 파악하여 +1 수준의 논증을 맞춤 제공하기가 "
                "실제로 매우 어렵다는 실천적 한계가 지적된다. "
                "또한 단계 이론의 타당성에 의문이 제기될 경우 +1 전략의 근거도 약해진다."
            ),
            "context": "콜버그의 인지발달주의 도덕교육론에서 핵심적인 교육 방법론적 원리.",
            "keywords": ["+1 전략", "인지적 불균형", "도덕교육 방법", "피아제적 교육론"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-012: 정의공동체 접근(Just Community Approach)
        {
            "id": "kohlberg-claim-012",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-just-community-1985",
            "source_detail": "The Just Community Approach to Moral Education in Theory and Practice",
            "claim": (
                "정의공동체 접근(Just Community Approach): 도덕교육은 개인의 도덕 추론 발달을 넘어서 "
                "학교나 기관 전체를 민주적 정의공동체로 만드는 것을 목표로 해야 한다. "
                "구성원 모두(학생, 교사)가 동등한 발언권과 의결권을 가진 공동체 회의(community meeting)를 통해 "
                "규칙을 함께 만들고, 갈등을 해결하며, 공동의 가치를 형성한다. "
                "개인의 도덕 단계가 아닌 공동체의 도덕적 분위기(moral atmosphere)가 핵심 변수이다."
            ),
            "explanation": (
                "콜버그는 1974년부터 보스턴 지역 클러스터 학교(Cambridge Cluster School)에서 "
                "정의공동체 접근을 직접 실행했다. 학생과 교사가 동등한 투표권을 가지고 "
                "규칙을 민주적으로 결정하는 방식이 특징이다. "
                "코네티컷 주 니에후스(Niantic) 여자 교도소에서도 같은 원리를 적용했다."
            ),
            "argument": (
                "개인 도덕 추론만 발달시켜서는 도덕적 행동으로 이어지지 않을 수 있다. "
                "집단의 도덕적 분위기와 규범이 구성원의 행동에 결정적 영향을 미치므로, "
                "도덕교육은 공동체 차원에서 이루어져야 한다."
            ),
            "counterpoint": (
                "직접 민주주의 방식은 규모가 큰 학교에서 실행하기 어렵다. "
                "학생과 교사의 실질적 권력 차이로 인해 진정한 민주적 운영이 어렵다는 비판도 있다. "
                "나딩스는 공동체 접근이 여전히 정의 중심이며 배려 관계를 충분히 고려하지 않는다고 비판했다."
            ),
            "context": "1970년대 이후 콜버그가 개인 중심 단계 이론에서 공동체 중심 접근으로 이론을 확장한 실천적 전환.",
            "keywords": ["정의공동체", "공동체 회의", "도덕적 분위기", "학교 민주주의", "직접 민주주의"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-013: 도덕적 분위기(moral atmosphere)
        {
            "id": "kohlberg-claim-013",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-psychology-moral-development-1984",
            "source_detail": "The Psychology of Moral Development, Ch. 6: The Just Community Approach",
            "claim": (
                "도덕적 분위기(moral atmosphere)는 집단이 공유하는 도덕적 규범, 가치, 기대의 총체로, "
                "집단 구성원의 도덕적 행동과 발달에 결정적 영향을 미친다. "
                "개인의 도덕 발달 단계와는 별도로, 집단의 도덕적 분위기 수준이 높을수록 "
                "구성원이 더 도덕적으로 행동하는 경향이 있다. "
                "정의공동체 접근의 목표는 공동체의 도덕적 분위기를 높이는 것이다."
            ),
            "explanation": (
                "콜버그는 초기에 개인의 도덕 추론 발달에 집중했으나, "
                "실천 경험을 통해 집단적·환경적 요인의 중요성을 인식하게 되었다. "
                "도덕적 분위기는 개인의 도덕 단계와 독립적으로 작용하는 집단 수준의 변수이다."
            ),
            "argument": (
                "실제 도덕 행동은 개인의 추론 단계만으로 결정되지 않는다. "
                "도덕적 분위기가 낮은 집단에서는 높은 단계의 추론을 가진 개인도 "
                "비도덕적 행동을 하게 된다. 따라서 도덕교육은 개인과 환경 모두를 변화시켜야 한다."
            ),
            "counterpoint": (
                "도덕적 분위기의 측정이 주관적이며 개인의 도덕 단계보다 측정하기 어렵다는 방법론적 문제가 있다."
            ),
            "context": "정의공동체 접근의 핵심 개념으로, 개인 중심 도덕발달론을 보완하는 집단 수준의 개념.",
            "keywords": ["도덕적 분위기", "집단 규범", "정의공동체", "도덕 행동"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-014: 인지발달주의 관점 — 피아제 계승과 확장
        {
            "id": "kohlberg-claim-014",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-moral-stages-moralization-1976",
            "source_detail": "Moral Stages and Moralization, in T. Lickona (Ed.)",
            "claim": (
                "도덕 교육의 목표는 도덕적 덕목의 습관화(행동주의 접근)나 "
                "문화적 가치의 내면화(사회화 접근)가 아니라, "
                "도덕적 추론 능력의 발달(인지발달주의 접근)이다. "
                "'덕목 가방(bag of virtues)' 접근 — 정직, 친절, 책임 등 덕목 목록을 가르치는 것 — "
                "은 어떤 덕목을 왜 가르쳐야 하는지 정당화하지 못하며, "
                "도덕적 상대주의로 귀결된다. "
                "인지발달주의 접근만이 도덕적 상대주의를 극복하고 보편적 도덕교육을 정당화할 수 있다."
            ),
            "explanation": (
                "콜버그는 행동주의적 덕교육(character education)이 '무엇이 덕인가'에 대한 철학적 답변 없이 "
                "문화적·사회적 규범을 그대로 주입한다고 비판했다. "
                "인지발달주의는 도덕 추론의 보편적 단계 구조를 통해 덕의 내용이 아닌 "
                "판단 형식의 보편성을 옹호한다."
            ),
            "argument": (
                "도덕 발달은 피아제의 인지 발달과 마찬가지로 내적 능동적 구성 과정이다. "
                "교사의 역할은 덕목을 전달하는 것이 아니라 학생이 더 복잡한 도덕 추론을 "
                "스스로 구성하도록 촉진하는 것이다."
            ),
            "counterpoint": (
                "리코나(Lickona)는 덕교육을 옹호하며, 도덕 추론의 발달만으로는 도덕적 행동을 보장하지 못한다고 반론했다. "
                "하이트(Haidt)는 도덕 판단이 추론보다 직관에 더 많이 의존한다는 사회적 직관주의를 제시했다."
            ),
            "context": "콜버그가 인지발달주의 도덕교육론을 행동주의 및 덕교육과 대비하여 정당화한 핵심 논증.",
            "keywords": ["인지발달주의 도덕교육", "덕목 가방 비판", "도덕 추론 발달", "행동주의 비판"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-015: 7단계 — 우주적·종교적 관점 (후기 논의)
        {
            "id": "kohlberg-claim-015",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-philosophy-moral-development-1981",
            "source_detail": "The Philosophy of Moral Development, Ch. 8: Moral Development, Religious Thinking and the Question of a Seventh Stage",
            "claim": (
                "콜버그는 후기에 6단계를 넘어서는 '7단계(soft stage 7)'의 가능성을 탐구했다. "
                "7단계는 도덕성과 우주적·종교적 의미의 관점이 통합되는 경험으로, "
                "정의 원칙을 넘어 존재와 우주 전체에 대한 헌신적 태도를 포함한다. "
                "간디, 마틴 루서 킹 Jr.의 비폭력 저항에서 이 단계의 예를 찾을 수 있다. "
                "7단계는 경험적으로 검증된 단계가 아니라 '부드러운 단계(soft stage)'로서 제시된다."
            ),
            "explanation": (
                "7단계는 도덕발달 단계가 아니라 삶의 의미, 우주에서의 인간의 위치에 대한 "
                "철학적·종교적 물음에 답하는 성숙한 관점으로 이해될 수 있다. "
                "콜버그는 이것이 도덕적 우울증(moral depression) — '왜 도덕적이어야 하는가'라는 물음 — "
                "을 극복하는 방식이라고 보았다."
            ),
            "argument": (
                "6단계의 정의 원칙만으로는 '왜 도덕적이어야 하는가'라는 삶의 의미 물음에 답하기 어렵다. "
                "우주적·종교적 관점에서 정의와 배려를 실천하는 성숙한 도덕성은 "
                "6단계를 넘어서는 차원을 요청한다."
            ),
            "counterpoint": (
                "7단계는 경험적 근거가 없으며 과학적 이론의 범위를 벗어난다는 비판이 있다. "
                "종교적 관점이 반드시 더 높은 도덕성을 의미하지 않는다는 반론도 있다."
            ),
            "context": "콜버그의 후기 사상에서 도덕발달과 삶의 의미, 종교의 관계를 탐구한 논의.",
            "keywords": ["7단계", "우주적 관점", "종교적 도덕성", "삶의 의미", "소프트 스테이지"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-016: 도덕 판단과 도덕 행동의 관계
        {
            "id": "kohlberg-claim-016",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-psychology-moral-development-1984",
            "source_detail": "The Psychology of Moral Development, Ch. 7",
            "claim": (
                "높은 도덕 발달 단계는 더 일관된 도덕적 행동의 경향성과 상관관계를 가지지만, "
                "도덕 판단이 도덕 행동을 자동적으로 결정하지는 않는다. "
                "2차 세계대전 중 유대인을 구조한 이타적 행동자들과 나치 협력자들의 도덕 추론 단계 차이가 "
                "그 상관관계를 보여준다. "
                "행동에는 추론 능력 외에도 의지력, 감정, 상황적 요인 등이 작용한다."
            ),
            "explanation": (
                "콜버그는 도덕 추론과 행동 사이의 '갭' 문제를 인식했다. "
                "레스트는 도덕 행동을 위해 도덕 감수성, 도덕 판단, 도덕 동기, 도덕 품성 등 "
                "4가지 구성 요소가 필요하다는 4구성요소 모델을 발전시켰다."
            ),
            "argument": (
                "도덕 추론의 높은 단계가 도덕적 행동을 보장하지는 않지만, "
                "낮은 단계에 비해 더 높은 확률로 도덕적 행동과 연결된다. "
                "도덕 교육이 추론 발달만으로 충분하지 않을 수 있음을 인정한다."
            ),
            "counterpoint": (
                "블라시(Blasi)는 도덕적 자아 정체성(moral identity)이 판단-행동 일치의 핵심 변수라고 주장했다. "
                "레스트의 4구성요소 모델은 콜버그 이론의 한계를 보완하려는 시도이다."
            ),
            "context": "도덕 추론과 실제 행동 사이의 관계를 다룬 도덕심리학의 핵심 주제.",
            "keywords": ["도덕 판단", "도덕 행동", "판단-행동 간극", "4구성요소", "도덕 정체성"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-017: 도덕발달과 인지발달의 관계
        {
            "id": "kohlberg-claim-017",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-philosophy-moral-development-1981",
            "source_detail": "The Philosophy of Moral Development, Ch. 4",
            "claim": (
                "도덕발달은 인지발달에 근거하며, 인지발달은 도덕발달의 필요조건이지만 충분조건은 아니다. "
                "형식적 조작기(formal operations)에 도달해야 후인습적 도덕 추론이 가능하다. "
                "그러나 형식적 조작기에 도달했다고 해서 자동적으로 후인습적 도덕성이 나타나지는 않는다. "
                "도덕발달은 인지발달과 병행하지만, 도덕적 경험과 사회적 자극이 추가로 필요하다."
            ),
            "explanation": (
                "콜버그는 피아제의 인지발달 단계(감각운동기, 전조작기, 구체적 조작기, 형식적 조작기)와 "
                "도덕발달 단계가 상응함을 주장했다. "
                "구체적 조작기는 인습적 도덕성에, 형식적 조작기는 후인습적 도덕성에 상응한다."
            ),
            "argument": (
                "도덕 추론은 인지 능력의 한 형태이므로, 더 복잡한 도덕적 사고는 "
                "더 발달된 인지 능력을 필요로 한다. "
                "이는 도덕교육이 인지 교육을 전제해야 함을 함축한다."
            ),
            "counterpoint": (
                "하이트는 도덕 판단이 인지적 추론이 아닌 직관적 반응에 더 많이 의존한다고 주장했다. "
                "도덕 추론이 사후 합리화일 수 있다는 비판도 제기된다."
            ),
            "context": "콜버그가 피아제의 인지발달론을 도덕 영역으로 확장한 이론적 기반.",
            "keywords": ["인지발달", "형식적 조작기", "도덕발달 필요조건", "피아제 계승"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-018: 길리건의 배려윤리와의 관계
        {
            "id": "kohlberg-claim-018",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-psychology-moral-development-1984",
            "source_detail": "The Psychology of Moral Development, Appendix: Reply to Gilligan",
            "claim": (
                "콜버그는 길리건의 비판을 부분적으로 수용하면서도 정의 중심 접근의 보편성을 옹호했다. "
                "길리건은 콜버그의 도덕 단계가 남성(하버드 남학생) 중심으로 개발되어 "
                "여성의 배려 지향 도덕성을 과소평가한다고 비판했다. "
                "콜버그는 정의와 배려 모두 도덕의 핵심 지향이지만, "
                "정의가 더 형식적·보편적 원리라고 주장했다. "
                "정의공동체 접근에서는 공동체적 배려와 정의를 통합하려 시도했다."
            ),
            "explanation": (
                "길리건의 「다른 목소리로(In a Different Voice)」(1982)는 콜버그 이론에 대한 "
                "가장 영향력 있는 비판이다. 길리건은 여성이 배려와 관계를 중심으로 "
                "도덕 문제를 접근하며, 이것이 콜버그 체계에서 3단계로 낮게 평가된다고 주장했다."
            ),
            "argument": (
                "정의는 인간의 보편적 도덕 원리로서 배려를 포함할 수 있으며, "
                "배려 역시 공정성과 정의의 원리에 근거해야 한다. "
                "정의공동체에서 공동체적 배려가 구현된다."
            ),
            "counterpoint": (
                "나딩스(Noddings)는 배려가 정의로 환원되지 않는 독립적인 도덕 원리라고 주장했다. "
                "경험적 연구에서 도덕 발달의 성별 차이는 일관되게 나타나지 않는다는 결과도 있다."
            ),
            "context": "1980년대 가장 중요한 도덕발달론 논쟁으로, 정의 대 배려의 도덕 지향 논의.",
            "keywords": ["배려윤리", "정의 대 배려", "길리건 비판", "성별 편향", "정의공동체"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-019: 딜레마 토론을 통한 도덕교육
        {
            "id": "kohlberg-claim-019",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-philosophy-moral-development-1981",
            "source_detail": "The Philosophy of Moral Development, Ch. 1: Education for Justice",
            "claim": (
                "도덕 딜레마 토론(moral dilemma discussion)은 도덕발달을 촉진하는 핵심적 교수법이다. "
                "가상의 또는 실제의 도덕적 갈등 상황을 제시하고 소집단 토론을 통해 "
                "학생들이 서로의 도덕 추론을 공유할 때, 현재 단계의 한계를 인식하고 "
                "더 높은 단계의 관점으로 이행하는 인지적 불균형이 발생한다. "
                "소크라테스적 교육법의 현대적 적용이다."
            ),
            "explanation": (
                "딜레마 토론에서 학생들은 자신과 다른 도덕 추론 수준의 논거를 접하게 된다. "
                "특히 자신보다 한 단계 높은(+1) 논거는 인지적 불균형을 일으켜 발달을 자극한다. "
                "교사의 역할은 딜레마 상황을 설정하고 소크라테스식 질문으로 토론을 촉진하는 것이다."
            ),
            "argument": (
                "도덕발달은 수동적 수업이 아닌 능동적 인지 갈등을 통해 이루어진다. "
                "딜레마 토론은 이 갈등을 안전하게 경험할 기회를 제공한다."
            ),
            "counterpoint": (
                "딜레마 토론이 실제 도덕적 행동 변화로 이어지는지에 대한 경험적 증거가 제한적이라는 비판이 있다. "
                "리코나는 딜레마 토론보다 공동체 생활 속 도덕적 경험이 더 효과적이라고 주장했다."
            ),
            "context": "콜버그의 교육 실천에서 가장 핵심적인 교수법으로, 전 세계 도덕교육에 영향을 미쳤다.",
            "keywords": ["딜레마 토론", "소크라테스 교육법", "인지적 불균형", "도덕교육 방법"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-020: 롤스 정의론과 6단계의 철학적 연결
        {
            "id": "kohlberg-claim-020",
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-philosophy-moral-development-1981",
            "source_detail": "The Philosophy of Moral Development, Ch. 5: From Is to Ought",
            "claim": (
                "도덕발달의 최고 단계(6단계)는 롤스의 정의론에서 철학적으로 정당화된다. "
                "롤스의 원초적 입장(original position)과 무지의 베일(veil of ignorance)은 "
                "이상적 역할채택 — 어떤 사회적 지위에 있을지 모르는 상태에서 공정한 원칙을 선택하는 것 — "
                "의 절차적 표현이다. "
                "따라서 도덕발달의 최고 단계는 경험적 심리학적 사실일 뿐만 아니라 "
                "철학적으로도 정당화된 규범적 이상이다."
            ),
            "explanation": (
                "콜버그는 심리학적 발달 사실(is)에서 도덕적 당위(ought)를 이끌어내는 문제를 인식하고, "
                "롤스의 정의론을 통해 6단계가 철학적으로도 올바른 도덕 판단 방식임을 논증하려 했다. "
                "이는 자연주의적 오류를 피하면서 도덕발달 단계의 규범적 지위를 확보하려는 시도이다."
            ),
            "argument": (
                "도덕발달의 방향성(상위 단계가 더 낫다)을 경험적 사실만으로 정당화하면 '자연주의적 오류'가 된다. "
                "롤스의 정의론이 6단계의 도덕 추론 방식이 철학적으로도 올바름을 보여줌으로써, "
                "콜버그 이론의 규범적 방향성이 정당화된다."
            ),
            "counterpoint": (
                "헤어(Hare) 등 철학자들은 심리학적 발달 사실에서 도덕적 당위를 이끌어내는 것은 "
                "여전히 범주 오류라고 비판했다. 발달의 방향성과 도덕적 우월성은 다른 문제이다."
            ),
            "context": "콜버그가 경험적 도덕발달 이론을 규범적 도덕철학과 연결하려 한 핵심 논증.",
            "keywords": ["롤스 정의론", "원초적 입장", "역할채택", "도덕발달의 규범성", "is-ought 문제"],
            "verified": False,
            "verification_log": []
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """콜버그 관련 키워드 데이터 입력."""
    keywords = [
        {
            "id": "kohlberg-kw-001",
            "term": "3수준 6단계",
            "term_en": "Three Levels and Six Stages",
            "definition": (
                "콜버그의 도덕발달 모델로, 도덕 추론이 전인습적(pre-conventional), "
                "인습적(conventional), 후인습적(post-conventional)의 3수준으로 나뉘고, "
                "각 수준이 2개의 단계로 구성된 총 6단계를 거쳐 발달한다는 이론. "
                "각 단계는 질적으로 다른 도덕적 추론 구조를 가지며 순서는 보편적이다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-philosophy-moral-development-1981",
            "related_terms": ["전인습적 도덕성", "인습적 도덕성", "후인습적 도덕성", "도덕발달"]
        },
        {
            "id": "kohlberg-kw-002",
            "term": "전인습적 도덕성",
            "term_en": "Pre-conventional Morality",
            "definition": (
                "콜버그 도덕발달의 수준 I. 도덕 판단이 개인의 이익(처벌 회피, 욕구 충족)에 근거하는 단계. "
                "1단계(벌과 복종 지향)와 2단계(도구적 상대주의 지향)로 구성된다. "
                "주로 아동기에 나타나며, 사회적 관점 채택 능력이 제한적이다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-psychology-moral-development-1984",
            "related_terms": ["1단계", "2단계", "벌과 복종", "도구적 상대주의"]
        },
        {
            "id": "kohlberg-kw-003",
            "term": "인습적 도덕성",
            "term_en": "Conventional Morality",
            "definition": (
                "콜버그 도덕발달의 수준 II. 도덕 판단이 사회적 기대와 제도적 규칙에 근거하는 단계. "
                "3단계(착한 소년·소녀 지향)와 4단계(법과 질서 지향)로 구성된다. "
                "대부분의 성인이 이 수준에 머문다. '사회의 눈'으로 도덕을 판단한다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-psychology-moral-development-1984",
            "related_terms": ["3단계", "4단계", "착한 소년·소녀", "법과 질서"]
        },
        {
            "id": "kohlberg-kw-004",
            "term": "후인습적 도덕성",
            "term_en": "Post-conventional Morality",
            "definition": (
                "콜버그 도덕발달의 수준 III. 도덕 판단이 사회적 관습과 법을 초월하는 보편적 원칙에 근거하는 단계. "
                "5단계(사회계약 지향)와 6단계(보편적 윤리 원칙 지향)로 구성된다. "
                "소수의 성인만 이 수준에 도달한다. 자율적이고 보편적인 도덕 판단의 단계이다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-philosophy-moral-development-1981",
            "related_terms": ["5단계", "6단계", "사회계약", "보편적 윤리 원칙"]
        },
        {
            "id": "kohlberg-kw-005",
            "term": "정의공동체",
            "term_en": "Just Community",
            "definition": (
                "콜버그가 1970년대부터 실천한 도덕교육 접근. 학교나 기관을 민주적 정의공동체로 만들어 "
                "구성원 모두가 동등한 발언권과 의결권을 가진 공동체 회의를 통해 "
                "규칙을 함께 만들고, 도덕적 분위기를 형성하는 접근. "
                "개인의 도덕 추론 발달을 넘어 집단 차원의 도덕 교육을 목표로 한다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-just-community-1985",
            "related_terms": ["공동체 회의", "도덕적 분위기", "학교 민주주의", "직접 민주주의"]
        },
        {
            "id": "kohlberg-kw-006",
            "term": "역할채택",
            "term_en": "Role-taking",
            "definition": (
                "타인의 관점, 생각, 감정을 자신의 것처럼 인지적으로 취하는 능력. "
                "콜버그 이론에서 도덕발달의 핵심 인지적 메커니즘이다. "
                "각 도덕발달 단계는 더 복잡하고 확장된 역할채택 능력을 반영한다. "
                "피아제의 탈중심화 개념을 도덕 영역으로 확장한 것이다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-psychology-moral-development-1984",
            "related_terms": ["사회적 관점 채택", "탈중심화", "공감", "조망수용"]
        },
        {
            "id": "kohlberg-kw-007",
            "term": "하인츠 딜레마",
            "term_en": "Heinz Dilemma",
            "definition": (
                "콜버그가 도덕 판단 면접(MJI)에서 사용한 가상적 도덕 갈등 상황. "
                "아내의 생명을 구하기 위해 약을 훔쳐야 하는지를 둘러싼 딜레마로, "
                "재산권 vs 생명권, 법 준수 vs 도덕 원칙 등 도덕적 갈등을 제시한다. "
                "행동 선택보다 그 이유와 논거가 도덕발달 단계 측정의 핵심이다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-dissertation-1958",
            "related_terms": ["도덕 판단 면접(MJI)", "도덕 딜레마", "도덕 추론", "단계 측정"]
        },
        {
            "id": "kohlberg-kw-008",
            "term": "+1 전략",
            "term_en": "Plus-one Strategy",
            "definition": (
                "콜버그의 도덕교육 방법론. 교사가 학생의 현재 도덕 발달 단계보다 "
                "정확히 한 단계 높은 수준의 도덕적 논증을 제시함으로써 "
                "인지적 불균형을 유발하고 도덕발달을 촉진하는 교수 전략. "
                "피아제의 인지발달 메커니즘을 도덕 교육에 적용한 것이다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-moral-stages-moralization-1976",
            "related_terms": ["인지적 불균형", "도덕교육 방법", "딜레마 토론", "발달 촉진"]
        },
        {
            "id": "kohlberg-kw-009",
            "term": "도덕적 분위기",
            "term_en": "Moral Atmosphere",
            "definition": (
                "집단이 공유하는 도덕적 규범, 가치, 기대의 총체. "
                "콜버그의 정의공동체 접근에서 핵심 개념으로, "
                "개인의 도덕발달 단계와는 별도로 집단 수준에서 측정되는 변수이다. "
                "도덕적 분위기가 높은 공동체에서 구성원은 더 도덕적으로 행동하는 경향이 있다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-just-community-1985",
            "related_terms": ["정의공동체", "집단 규범", "공동체 회의", "도덕 행동"]
        },
        {
            "id": "kohlberg-kw-010",
            "term": "도덕 판단 면접(MJI)",
            "term_en": "Moral Judgment Interview (MJI)",
            "definition": (
                "콜버그가 개발한 도덕발달 단계 측정 도구. "
                "9가지 가상적 도덕 딜레마를 제시하고 피험자의 응답을 "
                "표준 쟁점 채점법(Standard Issue Scoring)으로 분석하여 "
                "도덕발달 단계를 산출한다. "
                "판단 내용보다 판단의 형식적 구조(추론 방식)가 채점의 기준이다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-dissertation-1958",
            "related_terms": ["하인츠 딜레마", "표준 쟁점 채점법", "단계 측정", "DIT"]
        },
        {
            "id": "kohlberg-kw-011",
            "term": "인지발달주의",
            "term_en": "Cognitive-developmentalism",
            "definition": (
                "도덕발달을 인지발달의 관점에서 이해하는 이론적 접근. "
                "피아제의 인지발달론에 기반하여, 도덕 판단이 인지 구조의 발달과 함께 "
                "단계적으로 변화한다고 보는 관점. "
                "콜버그는 이를 행동주의적 도덕교육(습관화)과 사회화 접근(문화 내면화)에 대한 대안으로 제시했다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-moral-stages-moralization-1976",
            "related_terms": ["피아제", "도덕발달", "구조주의", "능동적 구성"]
        },
        {
            "id": "kohlberg-kw-012",
            "term": "보편성",
            "term_en": "Universality",
            "definition": (
                "콜버그 도덕발달 이론의 핵심 주장 중 하나. "
                "도덕발달의 3수준 6단계는 문화, 국가, 성별을 초월하여 보편적으로 나타나며, "
                "단계의 순서는 어느 문화에서도 동일하다는 주장. "
                "다양한 문화권 비교 연구에 의해 지지되지만, 문화 상대주의자들의 비판을 받고 있다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-philosophy-moral-development-1981",
            "related_terms": ["단계 순서", "문화 초월성", "도덕 상대주의 비판", "순서불변성"]
        },
        {
            "id": "kohlberg-kw-013",
            "term": "공동체 회의",
            "term_en": "Community Meeting",
            "definition": (
                "정의공동체 접근의 핵심 실천 기제. 학교 공동체의 모든 구성원(학생, 교사)이 "
                "주기적으로 모여 공동 규칙, 갈등 해결, 공동체 가치에 대해 토론하고 "
                "동등한 투표권으로 결정을 내리는 민주적 의사결정 과정. "
                "직접 민주주의의 학교 내 적용이자 도덕적 분위기 형성의 장이다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-just-community-1985",
            "related_terms": ["정의공동체", "도덕적 분위기", "직접 민주주의", "학교 민주주의"]
        },
        {
            "id": "kohlberg-kw-014",
            "term": "인지적 불균형",
            "term_en": "Cognitive Disequilibrium",
            "definition": (
                "피아제의 개념을 콜버그가 도덕 교육에 적용한 것. "
                "현재의 도덕적 사고 구조로는 해결할 수 없는 갈등 상황에서 발생하는 인지적 불안정 상태. "
                "이 불균형이 더 높은 도덕발달 단계로 이행하는 동력이 된다. "
                "+1 전략과 딜레마 토론은 이 불균형을 유도하기 위한 교육적 방법이다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-moral-stages-moralization-1976",
            "related_terms": ["+1 전략", "딜레마 토론", "평형화", "발달 촉진"]
        },
        {
            "id": "kohlberg-kw-015",
            "term": "사회적 관점",
            "term_en": "Sociomoral Perspective",
            "definition": (
                "콜버그의 도덕발달 단계 각각에 상응하는 사회적 세계를 이해하는 방식. "
                "1단계(자기중심적) → 2단계(개인주의적) → 3단계(관계 중심) → 4단계(사회 체계) → "
                "5단계(사회선행적) → 6단계(도덕적 관점)의 순서로 확장된다. "
                "도덕발달은 곧 사회적 관점의 확장이며, 역할채택 능력의 발달과 직결된다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-psychology-moral-development-1984",
            "related_terms": ["역할채택", "단계 구조", "조망수용", "도덕발달"]
        },
        {
            "id": "kohlberg-kw-016",
            "term": "순서불변성",
            "term_en": "Invariant Sequence",
            "definition": (
                "콜버그 도덕발달론의 핵심 주장 중 하나. "
                "도덕발달의 단계 순서는 문화와 개인에 관계없이 항상 동일하며, "
                "단계를 건너뛰거나 역행하지 않는다는 원리. "
                "도덕 발달이 단순한 사회화나 학습이 아닌 내적 인지 구조의 발달임을 지지하는 근거이다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-philosophy-moral-development-1981",
            "related_terms": ["보편성", "단계 이론", "피아제 계승", "종단 연구"]
        },
        {
            "id": "kohlberg-kw-017",
            "term": "덕목 가방 비판",
            "term_en": "Bag of Virtues Critique",
            "definition": (
                "콜버그가 전통적 인격교육(character education)을 비판하기 위해 사용한 개념. "
                "정직, 친절, 책임 등 덕목 목록을 가르치는 방식은 어떤 덕목을 왜 가르쳐야 하는지 "
                "철학적으로 정당화하지 못하며, 문화적·사회적 편견을 그대로 주입한다는 비판. "
                "인지발달주의는 덕목 내용이 아닌 도덕 추론의 형식적 보편성을 통해 이 문제를 극복한다고 주장."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-moral-stages-moralization-1976",
            "related_terms": ["인격교육", "덕교육", "인지발달주의 도덕교육", "도덕 상대주의"]
        },
        {
            "id": "kohlberg-kw-018",
            "term": "표준 쟁점 채점법",
            "term_en": "Standard Issue Scoring",
            "definition": (
                "콜버그의 도덕 판단 면접(MJI) 채점 방법. "
                "딜레마에 대한 응답에서 나타나는 도덕적 쟁점(규범, 요소)과 "
                "그것을 다루는 추론 구조(단계)를 분석하여 도덕발달 단계 점수를 산출한다. "
                "1980년대 콜스비(Colby)와 콜버그가 공동 개발하여 이전의 판단 기반 채점을 대체했다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-psychology-moral-development-1984",
            "related_terms": ["도덕 판단 면접(MJI)", "단계 측정", "채점 신뢰도"]
        },
        {
            "id": "kohlberg-kw-019",
            "term": "사회계약",
            "term_en": "Social Contract",
            "definition": (
                "콜버그 도덕발달 5단계의 핵심 개념. "
                "법과 사회 제도를 절대적 명령이 아닌 공동의 복지를 위한 상호 합의로 이해하는 관점. "
                "민주주의적 절차에 의해 만들어지고 변경될 수 있으며, "
                "기본적 인권을 침해하는 법은 정당하지 않다는 인식을 포함한다. "
                "롤스의 사회계약론과 연결되며, 미국 헌법의 정신을 반영한다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-philosophy-moral-development-1981",
            "related_terms": ["5단계", "후인습적 도덕성", "기본권", "롤스", "민주주의"]
        },
        {
            "id": "kohlberg-kw-020",
            "term": "딜레마 토론",
            "term_en": "Dilemma Discussion",
            "definition": (
                "콜버그의 인지발달주의 도덕교육에서 핵심적인 교수법. "
                "가상의 또는 실제의 도덕적 갈등 상황(딜레마)을 소집단 토론을 통해 다루는 방식. "
                "서로 다른 도덕 추론 수준을 가진 학생들이 논증을 공유할 때 "
                "+1 단계의 논거가 인지적 불균형을 일으켜 발달을 촉진한다. "
                "소크라테스적 교육법의 현대적 적용이다."
            ),
            "thinker_id": "kohlberg",
            "work_id": "kohlberg-philosophy-moral-development-1981",
            "related_terms": ["+1 전략", "인지적 불균형", "하인츠 딜레마", "소크라테스 교육법"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """콜버그 관련 관계 데이터 입력."""
    relations = [
        {
            "from_thinker": "piaget",
            "to_thinker": "kohlberg",
            "type": "influenced",
            "description": (
                "피아제의 인지발달론(동화, 조절, 평형화, 탈중심화)과 도덕발달론(타율적/자율적 도덕성)이 "
                "콜버그 이론의 직접적 기반이 되었다. "
                "콜버그는 피아제의 2단계를 6단계로 세분화하고, "
                "구체적 조작기→형식적 조작기의 인지발달과 도덕발달 단계의 상응관계를 논증했다. "
                "도덕 판단 면접(MJI)도 피아제의 임상 면접법을 발전시킨 것이다."
            ),
            "evidence": "Kohlberg, L. (1958). 박사논문; Kohlberg (1981), The Philosophy of Moral Development, Ch. 4"
        },
        {
            "from_thinker": "rawls",
            "to_thinker": "kohlberg",
            "type": "influenced",
            "description": (
                "롤스의 정의론이 콜버그 도덕발달 6단계의 철학적 기반을 강화했다. "
                "콜버그는 롤스의 원초적 입장을 이상적 역할채택의 절차적 표현으로 해석하여, "
                "6단계 후인습적 도덕성의 규범적 정당성을 롤스 정의론으로 뒷받침했다. "
                "콜버그는 도덕발달의 최고 단계가 롤스의 정의 원칙과 상응함을 논증했다."
            ),
            "evidence": "Kohlberg (1981), The Philosophy of Moral Development, Ch. 5: From Is to Ought"
        },
        {
            "from_thinker": "kohlberg",
            "to_thinker": "gilligan",
            "type": "influenced",
            "description": (
                "길리건은 콜버그의 지도학생이자 동료 연구자였으나, "
                "콜버그의 도덕발달 이론이 남성 중심 편향을 가지며 여성의 배려 지향 도덕성을 "
                "과소평가한다고 비판하며 독립적인 배려윤리 이론을 발전시켰다. "
                "길리건의 「다른 목소리로」(1982)는 콜버그 이론에 대한 가장 영향력 있는 도전이었으며, "
                "도덕 이론에서 젠더 관점의 중요성을 부각시켰다."
            ),
            "evidence": "Gilligan, C. (1982). In a Different Voice; Kohlberg (1984), The Psychology of Moral Development, Appendix"
        },
        {
            "from_thinker": "kohlberg",
            "to_thinker": "rest",
            "type": "influenced",
            "description": (
                "제임스 레스트(James Rest)는 콜버그의 제자로서, "
                "콜버그 이론을 비판적으로 계승하여 도덕발달 연구를 발전시켰다. "
                "선택형 DIT(Defining Issues Test)를 개발하여 MJI의 한계를 보완했으며, "
                "도덕 행동을 위한 4구성요소 모델(도덕 감수성, 도덕 판단, 도덕 동기, 도덕 품성)을 제시했다."
            ),
            "evidence": "Rest, J. (1979). Development in Judging Moral Issues; Rest, J. (1983). Morality."
        },
        {
            "from_thinker": "kohlberg",
            "to_thinker": "noddings",
            "type": "criticized",
            "description": (
                "나딩스는 콜버그의 정의 중심 도덕발달론이 추상적 원칙에 치우쳐 "
                "구체적 관계와 배려의 도덕을 무시한다고 비판했다. "
                "나딩스는 배려가 정의로 환원되지 않는 독립적인 도덕 원리이며, "
                "도덕교육의 핵심은 추론 발달이 아닌 배려 관계의 형성임을 주장했다."
            ),
            "evidence": "Noddings, N. (1984). Caring: A Feminine Approach to Ethics and Moral Education"
        },
        {
            "from_thinker": "kohlberg",
            "to_thinker": "habermas",
            "type": "influenced",
            "description": (
                "하버마스는 콜버그의 도덕발달 단계론을 사회이론적으로 재해석했다. "
                "후인습적 도덕성이 담론윤리(discourse ethics)의 이상적 의사소통 상황과 상응하며, "
                "의사소통적 합리성을 통한 도덕 원리의 정당화가 콜버그 6단계의 내용에 해당한다고 보았다. "
                "하버마스는 동시에 콜버그의 개인주의적 접근을 비판하며 담론적 차원을 강조했다."
            ),
            "evidence": "Habermas, J. (1990). Moral Consciousness and Communicative Action"
        }
    ]

    for rel in relations:
        rel_id = f"{rel['from_thinker']}-{rel['type']}-{rel['to_thinker']}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id}: {result['result']}")

    return len(relations)


def main():
    """메인 실행 함수."""
    print("=== 콜버그(Kohlberg) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (kohlberg)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n콜버그 데이터 입력 완료!")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}")
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
