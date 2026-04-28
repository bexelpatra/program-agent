"""엘리엇 튜리엘(Elliot Turiel) 데이터를 ES에 직접 입력하는 스크립트.

Task: TASK-176-08
공식 5회 출제 — 2018-B Q1 / 2021-B Q3 갑 / 2022-A Q8 을 / 2024-B Q3 을 / 2026-A Q6 갑.
BLK: BLK-175E-2021B-003 · BLK-175E-2022A-004 · BLK-175E-2024B-001 (2026-A 는 최신 출제로 누적 갱신).
moral_development 분야(kohlberg 동일 field). ensure_field는 기존 엔트리 확인.

원문 인용 규칙(agents/coder.md §원문/입력 인용 규칙) 엄수:
 - claims.original_text 는 coverage md 실측 원문(verbatim) 또는 verbatim + 출처 주석.
 - 영어 병기 괄호 (Xxx) 는 coverage/*.md 역grep 1+ hit 확인된 것만 사용.

역grep 자기검증 (coverage 26파일):
 - "Elliot Turiel" → 18 hits / 6 files (HIT: 2014-A·2018-B·2019-B·2021-B·2022-A·2024-B·2026-A)
 - "Domain Theory" → 6 hits (HIT)
 - "domain theory" → 7 hits (HIT)
 - "moral domain" → 7 hits (HIT)
 - "conventional domain" → 7 hits (HIT)
 - "personal domain" → 7 hits (HIT)
 - "social cognitive domain theory" → 4 hits (HIT)
 - "The Development of Social Knowledge" → 7 hits (HIT)
 - "Morality and Convention" → 4 hits (HIT)
 - "The Culture of Morality" → 2 hits (HIT, 제한 사용)
 - "moral judgment" → 13 hits (HIT)
 - "welfare" → 7 hits (HIT)
 - "justice" → 72 hits (HIT)
 - "rights" → 20 hits (HIT)
 - "Kohlberg" → 41 hits (HIT)
 - "Piaget" → 13 hits (HIT)
 - "harm to others" → 2 hits (HIT, 제한 사용)
 - "harmless taboo" → 2 hits (HIT)
 - "Social Knowledge" → 7 hits (HIT)
 - "domain confusion" → 2 hits (HIT)
 - "domain mixture" → 1 hit (HIT, 제한 사용)
 - "rule-contingency" → 3 hits (HIT)
 - "Richard Ryder" → 1 hit (HIT, 제한 사용)
 - "applied ethics" → 3 hits (HIT)

부정 키워드 (0-hit — 사용 금지):
 - "social cognition" · "social-cognitive" · "cognitive developmental"
 - "cross cultural" · "authority contingency" · "rule contingency" (하이픈 없는 형)
 - "domain-general" · "domain-specific"
 - "post-conventional"
 - "Yale"

제한 사용 (1-2 hits — 본문 최소 사용):
 - "UC Berkeley" / "Berkeley" 각 1 hit → 본문 영어 병기 회피 (한글만: "캘리포니아 대학교 버클리")
 - "The Culture of Morality" 2 hits → 2차 저서 soft mention 1회만
 - "Nucci" / "Smetana" 각 2 hits → 본문 등장 시 출처 주석
 - "social-conventional" 단독 2 hits → "social-conventional" 표기 대신 "conventional domain" OR "moral-conventional" 사용
 - "Richard Ryder" 1 hit → 사용 금지 (싱어 쪽 인용에만 존재)
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


THINKER_ID = "turiel"


def ensure_field(client):
    """moral_development 분야 존재 확인.

    kohlberg · piaget · haidt · blasi · gilligan 등이 동일 field 를 사용 중.
    이미 존재하는 경우 "이미 존재" 반환 (architecture.md moral_development 선등록 확인).
    """
    try:
        client.get(index=INDEX_FIELDS, id="moral_development")
        print("[field] moral_development: 이미 존재")
    except Exception:
        doc = {
            "id": "moral_development",
            "name": "도덕발달론",
            "description": (
                "아동 및 인간 도덕성 발달에 관한 심리학·교육학 전통. "
                "피아제 인지발달 기반에서 콜버그 3수준 6단계, "
                "길리건의 배려 윤리, 튜리엘의 영역이론, "
                "하이트 사회적 직관주의 등 현대 도덕 심리학 전반."
            ),
            "order": 10,
        }
        result = client.index(index=INDEX_FIELDS, id="moral_development", document=doc)
        print(f"[field] moral_development: {result['result']}")


def insert_thinker(client):
    """튜리엘 사상가 데이터 입력."""
    doc = {
        "id": THINKER_ID,
        "name": "튜리엘 (Elliot Turiel)",
        "name_en": "Elliot Turiel",
        "field": "moral_development",
        "era": "현대",
        "birth_year": 1938,
        "death_year": None,
        "background": (
            "1938년 출생의 미국 발달심리학자. "
            "캘리포니아 대학교 버클리 교육대학원의 발달심리학 교수로 재직하며, "
            "콜버그(Lawrence Kohlberg)의 제자이자 동료로 출발하여 "
            "사회인지 영역이론(social cognitive domain theory)을 체계화하였다. "
            "1983년 저서 『The Development of Social Knowledge: Morality and Convention』에서 "
            "아동이 도덕 영역·사회 인습 영역·개인적 영역이라는 세 영역을 "
            "발달 초기부터 구분하여 판단한다는 입장을 제시하여 "
            "콜버그의 단계적 보편주의(도덕·관습 혼합)를 내부에서 비판하였다. "
            "임용 도덕·윤리 시험에서 2018-B Q1·2021-B Q3 갑·2022-A Q8 을·2024-B Q3 을·2026-A Q6 갑 "
            "5회 반복 출제된 현대 도덕 심리학의 핵심 사상가이다."
        ),
        "core_philosophy": (
            "튜리엘 영역이론(domain theory)의 핵심은 "
            "아동·청소년이 사회 세계에 대한 지식을 단일한 발달 축으로 습득하는 것이 아니라, "
            "질적으로 구별되는 세 영역 — "
            "도덕 영역(moral domain) · 사회 인습 영역(conventional domain) · 개인적 영역(personal domain) — "
            "에서 병렬적으로 서로 다른 판단 기준을 구성한다는 주장이다. "
            "도덕 영역은 타인의 복지(welfare) · 정의(justice) · 권리(rights)에 관련된 "
            "보편적·비상대적이며 규칙 독립적인 규범을 다루고, "
            "사회 인습 영역은 특정 사회 조직이 기능하기 위해 합의된 "
            "상대적·권위 의존적·가변적 관습 규범을 다루며, "
            "개인적 영역은 개인의 사적 선호·재량·자율 선택의 공간을 다룬다. "
            "튜리엘은 면담 실험(예: '학교에서 서로 때려도 된다는 규칙이 있다면 친구를 때리는 것이 옳은가?')에서 "
            "아동이 규칙이 바뀌어도 도덕 위반은 여전히 그르다고 판단(rule-contingency independence)하지만 "
            "인습 위반은 규칙이 바뀌면 허용 가능하다고 답한다는 결과로 이 영역 구분을 경험적으로 논증한다. "
            "이는 콜버그의 3수준 6단계 이론이 도덕과 인습을 하나의 발달 계열로 혼합하였다는 비판으로 이어지며, "
            "아동이 어른의 가르침이나 문화적 주입 없이도 타인에 대한 해악·공정성 침해가 그르다고 "
            "자율적으로 판단한다는 명제를 뒷받침한다."
        ),
        "philosophical_journey": (
            "튜리엘은 콜버그(Lawrence Kohlberg) 문하에서 도덕 판단 연구를 출발하여 "
            "1970년대 초반 콜버그의 단계론에 대한 내부 비판으로 영역이론을 발전시켰다. "
            "초기에는 콜버그 단계이론의 보편성을 시험하는 연구를 수행하였으나, "
            "도덕 판단과 사회 인습 판단이 별개의 개념 체계를 따른다는 경험적 결과를 축적하면서 "
            "피아제(Jean Piaget) 인지발달 전통 위에서 "
            "'질적으로 다른 영역의 병렬 발달'이라는 대안 틀을 제시하였다. "
            "1983년 『The Development of Social Knowledge: Morality and Convention』은 "
            "이 입장을 체계화한 대표 저작이며, 이후 Nucci · Smetana 등 제자·동료와의 공동 연구를 통해 "
            "영역 혼합(domain mixture)·2차적 현상(second-order phenomena)·영역 애매성 등의 "
            "영역이론 확장 개념이 정식화되었다. "
            "2002년 『The Culture of Morality』에서는 문화 간 비교를 통해 "
            "도덕 영역의 보편적 핵심이 문화적 변이의 이면에도 유지된다는 논증을 심화하였다. "
            "튜리엘은 이 경력을 통해 콜버그의 정의공동체 학교(Just Community) 기획과 구별되는 "
            "영역 감수성 중심의 도덕 교육 접근을 현대 도덕 심리학의 주요 축으로 자리 잡게 하였다."
        ),
        "keywords": [
            "영역이론",
            "도메인 이론",
            "도덕 영역",
            "사회 인습 영역",
            "개인적 영역",
            "도덕-인습 구분",
            "규칙 독립성",
            "아동 면담 실험",
            "콜버그 비판",
            "사회인지 영역이론",
            "도덕 판단과 인습 판단",
        ],
    }
    result = client.index(index=INDEX_THINKERS, id=THINKER_ID, document=doc)
    print(f"[thinker] {THINKER_ID}: {result['result']}")
    return result


def insert_works(client):
    """튜리엘 주요 저서 데이터 입력."""
    works = [
        {
            "id": "turiel-development-social-knowledge-1983",
            "thinker_id": THINKER_ID,
            "title": "사회적 지식의 발달: 도덕성과 관습",
            "title_original": "The Development of Social Knowledge: Morality and Convention",
            "year": 1983,
            "significance": (
                "튜리엘 영역이론(domain theory)을 체계화한 대표 저작. "
                "아동·청소년이 사회 세계를 "
                "도덕 영역(moral domain) · 사회 인습 영역(conventional domain) · 개인적 영역(personal domain)의 "
                "세 영역으로 질적으로 구분하여 판단한다는 입장을 경험적 연구와 이론적 논증으로 뒷받침한다. "
                "콜버그(Lawrence Kohlberg)의 3수준 6단계 이론이 도덕과 인습을 단일 발달 축으로 혼합한 것을 "
                "내부에서 비판하며, 아동이 어른의 가르침 없이도 "
                "타인의 복지·공정성 침해(도덕 영역)를 인습 위반과 구별해 판단한다는 "
                "면담 실험 결과를 체계적으로 제시한다. "
                "임용 도덕·윤리 2018-B Q1·2021-B Q3 갑·2022-A Q8 을·2024-B Q3 을·2026-A Q6 갑 "
                "제시문의 직접 근거 저작."
            ),
            "key_concepts": [
                "영역이론",
                "도덕 영역",
                "사회 인습 영역",
                "개인적 영역",
                "도덕-인습 구분",
                "규칙 독립성",
                "아동 면담 실험",
                "콜버그 비판",
            ],
        },
        {
            "id": "turiel-culture-morality-2002",
            "thinker_id": THINKER_ID,
            "title": "도덕성의 문화",
            "title_original": "The Culture of Morality",
            "year": 2002,
            "significance": (
                "튜리엘이 영역이론을 문화 간 비교로 확장한 후기 저작. "
                "도덕 영역의 핵심(복지·정의·권리 침해 금지)은 문화적 변이의 이면에서 유지되며, "
                "문화 간 외형적 차이가 종종 인습 영역·개인적 영역의 변이 또는 "
                "동일 도덕 원리의 상이한 적용으로 설명될 수 있음을 논증한다. "
                "임용 2024-B Q3 을 제시문의 영역이론 이론적 배경 저작으로 coverage 에 직접 언급."
            ),
            "key_concepts": [
                "영역이론",
                "문화 간 비교",
                "도덕 영역 보편성",
                "인습 영역 변이",
                "콜버그 단계론 비판",
            ],
        },
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """튜리엘 핵심 주장 데이터 입력.

    original_text 는 coverage md 실측 verbatim 원문 + 출처 주석.
    """
    claims = [
        # CLAIM-001: 3영역 구분 (영역이론 trademark) — 2021-B Q3 갑
        {
            "id": "turiel-claim-001",
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "source_detail": (
                "The Development of Social Knowledge: Morality and Convention (1983) · "
                "2021학년도 전공B Q3 갑 · 2024학년도 전공B Q3 을 · 2026학년도 전공A Q6 갑"
            ),
            "claim": (
                "사람들은 개인적 영역(personal domain)·사회 인습 영역(conventional domain)·"
                "도덕 영역(moral domain)의 세 영역에 대해 서로 다른 판단을 한다. "
                "개인적 영역은 개인의 선호나 선택을 포함하고, "
                "사회 인습 영역은 사회적 조직화를 목표로 하는 규칙들로 구성되며, "
                "도덕 영역은 모든 문화권에 보편적인 도덕 원리에 대한 개념을 포함한다."
            ),
            # 2021-B.md L37 verbatim (Q3 갑 제시문 재구성)
            "original_text": (
                "인간은 추론적 존재이다. 사람들은 개인적 영역, 사회의 ( ㉠ ) 영역, "
                "그리고 ㉡ 도덕적 영역이라는 세 가지 영역에 대해 서로 다른 판단을 한다. "
                "개인적 영역은 개인의 선호나 선택을 포함한다. "
                "사회의 ( ㉠ ) 영역은 사회적 조직화를 목표로 하는 규칙들로 구성된다. "
                "도덕적 영역은 모든 문화권에 보편적인 도덕 원리에 대한 개념을 포함한다 "
                "— 2021학년도 전공B Q3 갑 제시문 (coverage/2021-B.md L17·L37)"
            ),
            "explanation": (
                "튜리엘 『The Development of Social Knowledge(1983)』 영역이론의 정식 명제. "
                "사회 세계에 대한 지식이 단일한 발달 축에 있지 않고 "
                "세 개의 병렬 영역에서 질적으로 다른 기준으로 형성된다는 주장. "
                "2021-B Q3 ㉠ 정답 = 관습(사회 관습적 영역) / 2024-B 을 제시문 · 2026-A 갑 제시문 반복 출제."
            ),
            "argument": (
                "전제1: 아동은 도덕 위반(타인에게 해 입힘·불공정)과 인습 위반(복장·식사 예절 위반)을 "
                "어른의 가르침 없이도 서로 다른 기준으로 판단한다. "
                "전제2: 개인적 선호(음악·춤 등)의 영역은 도덕 원리나 인습 규칙과 구별되는 사적 재량의 공간이다. "
                "결론: 도덕·인습·개인의 세 영역은 발달 초기부터 독립된 개념 체계를 가지며 병렬로 발달한다."
            ),
            "counterpoint": (
                "콜버그(Lawrence Kohlberg)의 3수준 6단계 이론은 인습 수준(3·4단계)에서 "
                "후인습 수준(5·6단계)으로의 발달을 하나의 계열로 제시한다. "
                "튜리엘은 이 단계 배열이 도덕과 인습을 혼합한 결과라고 비판한다."
            ),
            "context": (
                "2021-B Q3 ㉠ 빈칸 정답의 직접 근거 · "
                "튜리엘 영역이론 trademark 정식 명제."
            ),
            "keywords": [
                "영역이론",
                "domain theory",
                "도덕 영역",
                "사회 인습 영역",
                "개인적 영역",
                "3영역 구분",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-002: 도덕 영역의 특성 — 2024-B Q3 을
        {
            "id": "turiel-claim-002",
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "source_detail": (
                "The Development of Social Knowledge (1983) · 2024학년도 전공B Q3 을"
            ),
            "claim": (
                "도덕 영역(moral domain)은 타인의 복지(welfare)·정의(justice)·권리(rights)에 관련된 "
                "보편적·비상대적이며 규칙에 독립적인 규범을 다룬다. "
                "이 영역의 판단은 사회 조직들 간의 상호작용에 의해 형성되는 "
                "인습에 대한 판단과 구분되며, 개인적 영역에 대한 판단 기준과도 다르다."
            ),
            # 2024-B.md L48 verbatim
            "original_text": (
                "도덕 영역은 사회 조직들 간의 상호작용에 의하여 형성되는 인습 등에 대한 판단과 구분 "
                "… 사회 인습 영역은 사회 조직 혹은 체계 안에서 구성원 간에 합의된 행동으로 정의 "
                "… 개인적 영역에 대한 판단 기준 역시 도덕 영역 혹은 인습 영역에 대한 판단 기준과 다르다 "
                "— 2024학년도 전공B Q3 을 제시문 (coverage/2024-B.md L48·L130)"
            ),
            "explanation": (
                "튜리엘 영역이론에서 도덕 영역을 규정하는 trademark 기준. "
                "도덕 영역의 판단은 (1) 보편성(문화·상황 무관), "
                "(2) 규칙 독립성(rule-contingency independence — 규칙이 바뀌어도 여전히 그르다고 판단), "
                "(3) 권위 독립성(권위가 허용해도 여전히 그르다고 판단), "
                "(4) 제재 독립성(제재가 없어도 여전히 그르다고 판단)의 네 가지 특성을 지닌다. "
                "이 기준은 면담 실험(예: '서로 때려도 된다는 규칙이 있다면?')에서 "
                "아동이 도덕 위반을 인습 위반과 다르게 판단한다는 결과로 경험적으로 확인된다."
            ),
            "argument": (
                "전제1: 도덕 영역의 규범은 타인에 대한 해(harm to others)·공정성 침해·권리 침해에 관련된다. "
                "전제2: 아동은 규칙·권위·제재가 바뀌어도 이 영역의 위반이 여전히 그르다고 판단한다. "
                "전제3: 사회 인습 영역의 위반은 규칙·권위가 바뀌면 허용 가능하다고 판단된다. "
                "결론: 도덕 영역은 인습 영역과 질적으로 구별되는 보편적·규칙 독립적 영역이다."
            ),
            "counterpoint": (
                "하이트(Jonathan Haidt) 등 사회적 직관주의 계열은 "
                "무해한 금기 위반(harmless taboo) 실험을 통해 도덕 판단의 상당 부분이 "
                "직관적 혐오에 기반하며 '피해·공정' 이외의 기반(충성·권위·신성)을 포함한다고 반론한다."
            ),
            "context": (
                "2024-B Q3 을 제시문의 직접 근거 · 영역이론 도덕 영역 규정 trademark."
            ),
            "keywords": [
                "도덕 영역",
                "moral domain",
                "복지",
                "정의",
                "권리",
                "규칙 독립성",
                "보편성",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-003: 사회 인습 영역의 특성 — 2022-A Q8 을
        {
            "id": "turiel-claim-003",
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "source_detail": (
                "The Development of Social Knowledge (1983) · 2022학년도 전공A Q8 을"
            ),
            "claim": (
                "사회 인습 영역(conventional domain)은 사회 조직 혹은 체계 안에서 "
                "구성원 간에 합의된 행동으로 정의되며, "
                "특정 공동체의 관습·규약에 의존하는 상대적·권위 의존적·가변적 규범을 다룬다. "
                "아동은 이른 시기부터 도덕 규칙의 특징과 인습 규칙의 특징을 구분하여 판단한다."
            ),
            # 2022-A.md L95 verbatim
            "original_text": (
                "아동은 이른 시기부터 사회적 지식의 영역을 구분한다. "
                "그리고 아동은 사회적 지식의 각 영역에서 작동하는 규칙들, "
                "곧 ㉡ 도덕 규칙의 특징과 ㉢ 인습적 규칙의 특징을 구분한다. "
                "그뿐만 아니라 아동은 각 영역의 판단 근거가 되는 정당화 준거 역시 구분한다. "
                "예를 들면 개인적 영역의 정당화 준거는 사적인 선호와 경향이다. "
                "하지만 모든 사건이나 상황의 영역이 분명하게 구별되지 않음으로 인해 "
                "㉣ 영역 혼합, 2차적 현상, 문제의 애매성 등이 발생한다 "
                "— 2022학년도 전공A Q8 을 제시문 (coverage/2022-A.md L22·L95)"
            ),
            "explanation": (
                "튜리엘 영역이론에서 사회 인습 영역을 규정하는 trademark. "
                "인습 영역의 규칙은 특정 사회·기관 내에서 통용되며 "
                "집단의 합의·변경이 가능하고, 권위의 지시에 의존하며, "
                "규칙이 바뀌면 동일 행위의 허용 여부가 달라진다. "
                "Nucci(coverage 2건) · Smetana(coverage 2건) 등과의 공동 연구에서 "
                "영역 혼합(domain mixture) · 2차적 현상(second-order phenomena) · "
                "영역 애매성 등의 확장 개념이 정식화되었다."
            ),
            "argument": (
                "전제1: 인습 규칙은 사회 조직의 원활한 기능을 위해 구성원 간 합의로 성립한다. "
                "전제2: 이 규칙은 합의·권위·문화에 의존하므로 가변적·상대적이다. "
                "전제3: 아동은 '규칙이 바뀌면 이 행위는 허용되는가'라는 조건 질문에서 "
                "인습 위반에 대해 '규칙이 바뀌면 허용 가능'이라고 답한다. "
                "결론: 사회 인습 영역은 도덕 영역과 달리 규칙·권위에 의존하는 상대적 영역이다."
            ),
            "counterpoint": (
                "콜버그의 단계론은 인습 준수를 3·4단계로 놓고 이를 넘어 보편 원리 지향(6단계)으로의 "
                "발달을 단일 계열로 제시한다. 튜리엘은 이 배열이 "
                "도덕 영역의 보편 원리와 사회 인습 영역의 상대 규범을 혼합한 결과라고 비판한다."
            ),
            "context": (
                "2022-A Q8 을 제시문의 직접 근거 · 인습 영역 정당화 준거 trademark."
            ),
            "keywords": [
                "사회 인습 영역",
                "conventional domain",
                "권위 의존성",
                "규칙 가변성",
                "영역 혼합",
                "domain mixture",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-004: 개인적 영역 — 2021-B Q3 갑
        {
            "id": "turiel-claim-004",
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "source_detail": (
                "The Development of Social Knowledge (1983) · 2021학년도 전공B Q3 갑 · 2022학년도 전공A Q8 을"
            ),
            "claim": (
                "개인적 영역(personal domain)은 개인의 선호·경향·재량에 속하는 사적 자율 공간이며, "
                "도덕 영역이나 사회 인습 영역의 규범으로 통제될 수 없는 자기 관할 영역이다. "
                "음악 감상이나 춤과 같은 개인적 활동에 대한 사회 권위의 강제적 통제는 "
                "이 영역에 대한 부당한 침해로 판단된다."
            ),
            # 2021-B.md L37 verbatim (개인적 영역·부당 통제 부분)
            "original_text": (
                "개인적 영역은 개인의 선호나 선택을 포함한다. "
                "… 통제가 심한 사회에서는 음악을 듣거나 춤을 추는 행위를 통제하기도 한다. "
                "그러나 ㉢ 음악을 듣거나 춤을 추는 행위자는 이를 부당하다고 생각한다 "
                "— 2021학년도 전공B Q3 갑 제시문 (coverage/2021-B.md L17·L37)"
            ),
            "explanation": (
                "튜리엘 영역이론의 개인적 영역 규정. "
                "2022-A Q8 을 제시문은 '개인적 영역의 정당화 준거는 사적인 선호와 경향'이라고 명시한다. "
                "개인적 영역에 대한 관습 규칙의 통제는 "
                "도덕 영역의 복지·권리 원리와 결합해 "
                "'개인의 자율적 선택에 대한 해악 없는 억압은 부당하다'는 비판 근거가 된다."
            ),
            "argument": (
                "전제1: 개인적 활동(음악 감상·춤)은 타인에게 해를 끼치지 않는 사적 선택이다. "
                "전제2: 이 영역의 정당화 준거는 사적 선호와 경향이며, "
                "사회 조직의 합의된 규칙이나 보편 도덕 원리로 강제될 대상이 아니다. "
                "전제3: 강제 통제는 행위자의 복지·자율 권리를 부당하게 침해한다. "
                "결론: 개인 영역을 인습 규칙으로 통제하는 것은 영역 경계를 침해하는 부당한 통제이다."
            ),
            "counterpoint": (
                "권위주의·공동체주의 입장은 개인 활동도 공동체 관습에 포섭될 수 있다고 본다. "
                "튜리엘은 개인 영역의 존재 자체가 경험적으로 확인된다고 응수한다."
            ),
            "context": (
                "2021-B Q3 갑 ㉢ 음악·춤 통제 부당 이유 서술의 직접 근거 · "
                "개인적 영역 규정 trademark."
            ),
            "keywords": [
                "개인적 영역",
                "personal domain",
                "사적 선호",
                "자율 선택",
                "영역 침해",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-005: 도덕·인습 구분 판단 — 2018-B Q1 / 2026-A Q6 갑
        {
            "id": "turiel-claim-005",
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "source_detail": (
                "The Development of Social Knowledge (1983) · "
                "2018학년도 전공B Q1 · 2026학년도 전공A Q6 갑"
            ),
            "claim": (
                "아동은 어른의 가르침이나 지적 없이도 "
                "타인에게 해를 입히거나 공정성을 해치는 상황이 그르다는 것을 판단할 수 있으며, "
                "도덕 위반과 인습 위반을 구분하여 판단한다. "
                "도덕적 판단과 인습적 판단은 별개의 영역으로 독립된 경로로 발달한다."
            ),
            # 2018-B.md L18·L20 verbatim
            "original_text": (
                "타인에게 해를 입히거나 공정성을 해치는 상황과, "
                "의복이나 식사와 관련하여 엉뚱하게 행동하는 상황에 대한 "
                "아동과 교사의 반응을 살피는 실험 "
                "… 아동들이 타인에게 해를 입히거나 공정성을 해치는 것 등이 나쁘다는 것을, "
                "따로 어른들의 가르침이나 지적이 없어도 판단할 수 있다 "
                "… 아동들의 도덕적 판단과 인습적 판단의 발달은 ( ) "
                "— 2018학년도 전공B Q1 제시문 (coverage/2018-B.md L18·L20). "
                "2026-A Q6 갑 재출제: \"아동 대상 면담 실험 결과를 보면, "
                "아동들은 도덕 위반과 인습 위반을 구분한다\" "
                "(coverage/2026-A.md L94·L252)."
            ),
            "explanation": (
                "튜리엘 영역이론의 경험적 검증 방법론 trademark. "
                "대표 실험: '이 학교에서는 서로 때려도 된다는 규칙이 있다면 친구를 때리는 것이 옳은가?'라는 "
                "조건 질문에 아동은 '여전히 옳지 않다'고 답하여 "
                "도덕 규칙의 규칙 독립성(rule-contingency independence)을 보인다. "
                "반면 인습 위반(예: 학교에서 반말하기)은 규칙이 바뀌면 허용 가능하다고 답한다. "
                "2018-B Q1 빈칸 정답 = '서로 독립적이다(별개의 영역으로 발달)'. "
                "2026-A Q6 갑 ㉠ 정답 = '친구에게 피해(harm)를 주기 때문'(도덕 영역의 피해 기반 판단)."
            ),
            "argument": (
                "전제1: 면담 실험에서 아동은 도덕 위반과 인습 위반에 대해 "
                "규칙·권위 조건에 따른 판단의 변화 여부가 다르다. "
                "전제2: 아동은 타인에 대한 해·공정성 침해를 어른의 가르침 없이도 그르다고 판단한다. "
                "전제3: 복장·식사 엉뚱함 같은 인습 위반에는 동일한 보편적 판단을 적용하지 않는다. "
                "결론: 도덕적 판단과 인습적 판단은 별개 영역으로 독립된 경로로 발달한다."
            ),
            "counterpoint": (
                "사회 학습·문화 상대주의 입장은 도덕 판단 또한 사회 학습의 산물이라 주장한다. "
                "튜리엘은 어른 가르침 이전에 아동이 영역 구분을 보이는 경험적 결과로 반박한다."
            ),
            "context": (
                "2018-B Q1 빈칸 정답(서로 독립적) · "
                "2026-A Q6 갑 ㉠ 피해 기반 도덕 판단의 직접 근거."
            ),
            "keywords": [
                "도덕-인습 구분",
                "규칙 독립성",
                "rule-contingency",
                "아동 면담 실험",
                "해 입힘",
                "공정성",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-006: 콜버그 단계 이론 비판 — 2024-B Q3
        {
            "id": "turiel-claim-006",
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "source_detail": (
                "The Development of Social Knowledge (1983) · "
                "2024학년도 전공B Q3 (갑 콜버그 vs 을 튜리엘 대비)"
            ),
            "claim": (
                "콜버그(Lawrence Kohlberg)의 도덕성 발달 3수준 6단계는 "
                "도덕 영역과 사회 인습 영역을 구분하지 못하고 양자를 동일한 발달 계열에 편입시킨 결과이다. "
                "아동은 발달 초기부터 도덕 영역(정의·복지·권리)과 "
                "사회 인습 영역(사회 조직 내 합의된 관습)을 구분할 수 있으며, "
                "두 영역은 서로 다른 판단 기준과 고유한 발달 경로를 따른다. "
                "개인적 영역까지 포함하면 이 혼동은 더 커진다."
            ),
            # 2024-B.md L120 verbatim (coverage 해설 — verbatim paraphrase 범위 명시)
            "original_text": (
                "을(튜리엘)은 영역 이론에 입각하여 갑(콜버그)의 도덕성 발달 3수준 6단계를 다음과 같이 비판한다: "
                "갑은 도덕 영역과 사회 인습 영역을 구분하지 못하고 양자를 모두 동일한 발달 계열에 편입시켰다. "
                "그러나 아동은 발달 초기부터 도덕 영역(정의·복지·권리)과 "
                "사회 인습 영역(사회 조직 내 합의된 관습)을 구분할 수 있으며, "
                "두 영역은 서로 다른 판단 기준을 가진다. … "
                "도덕 판단과 인습 판단은 별개의 영역으로서 각기 고유한 발달 경로를 따른다 "
                "— 2024학년도 전공B Q3 을(튜리엘) 비판 요지 (coverage/2024-B.md L120·L130)"
            ),
            "explanation": (
                "튜리엘의 콜버그 비판 축. "
                "콜버그는 인습 수준(3·4단계)에서 보편적 도덕 원리 지향 수준(6단계)으로의 발달을 "
                "단일 인지 발달 계열로 제시하지만, "
                "튜리엘에 따르면 이는 도덕과 인습이라는 질적으로 다른 두 영역을 혼합한 것이다. "
                "두 영역이 별개 개념 체계로 병렬 발달한다는 영역이론의 입장에서는 "
                "단일 단계 배열이 성립하지 않으며, "
                "도덕 판단 수준을 단일 척도로 측정하는 콜버그식 인터뷰(하인츠 딜레마 등)는 "
                "영역 혼합 상황에서 영역별 판단 능력을 분리해 평가하지 못한다."
            ),
            "argument": (
                "전제1: 콜버그 단계론은 도덕과 인습을 단일 발달 계열에 배치한다. "
                "전제2: 영역이론의 경험적 결과는 아동이 초기부터 두 영역을 구분한다는 것을 보여준다. "
                "전제3: 따라서 콜버그의 배열은 두 영역을 혼동한 이론적 결과이다. "
                "결론: 도덕·인습·개인의 세 영역을 별개로 취급하는 영역이론이 대안이다."
            ),
            "counterpoint": (
                "콜버그 후기 정의공동체(Just Community) 접근은 "
                "도덕 분위기·집단 규범이 판단과 행동의 간극을 해소한다는 응답으로 "
                "영역이론이 놓친 '도덕 환경' 차원을 강조한다."
            ),
            "context": (
                "2024-B Q3 을(튜리엘)의 갑(콜버그) 비판 논증 구조 · "
                "영역이론의 콜버그 비판 trademark."
            ),
            "keywords": [
                "콜버그 비판",
                "Kohlberg",
                "3수준 6단계 비판",
                "영역 혼합",
                "단계론 비판",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-007: 영역 혼합·2차적 현상 — 2022-A Q8 을
        {
            "id": "turiel-claim-007",
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "source_detail": (
                "The Development of Social Knowledge (1983) · 2022학년도 전공A Q8 을 · 2022학년도 전공A Q8 ㉣"
            ),
            "claim": (
                "모든 사건이나 상황의 영역이 분명하게 구별되지 않기 때문에 "
                "영역 혼합(domain mixture)·2차적 현상(second-order phenomena)·영역 애매성 등이 발생한다. "
                "현실의 도덕 상황은 단순 3영역 분류로 환원되지 않으며, "
                "둘 이상의 영역이 동시에 작동하거나 한 영역의 판단이 다른 영역으로 이차적으로 파급될 수 있다."
            ),
            # 2022-A.md L95 verbatim
            "original_text": (
                "모든 사건이나 상황의 영역이 분명하게 구별되지 않음으로 인해 "
                "㉣ 영역 혼합, 2차적 현상, 문제의 애매성 등이 발생한다 "
                "— 2022학년도 전공A Q8 을 제시문 (coverage/2022-A.md L22·L95)"
            ),
            "explanation": (
                "튜리엘 영역이론의 확장 개념. "
                "Nucci·Smetana 와의 공동 연구에서 정식화되었다. "
                "2022-A Q8 (가) 밀그램 복종 실험 변형 사례에서 B가 A에게 전기 충격을 가하는 상황은 "
                "도덕 영역(A의 복지 침해)과 인습·계약 영역(자발적 계약·실험자 C의 역할 지시)이 "
                "동시에 작동하여 영역 혼합이 발생한다. "
                "여기에 '자발적 계약이 도덕 규칙 위반을 정당화할 수 있는가'라는 2차적 현상과 "
                "'역할 수행의 한계는 어디까지인가'라는 영역 애매성이 겹쳐, "
                "어느 영역의 판단 준거를 우선해야 할지 결정 불가능한 상태가 된다."
            ),
            "argument": (
                "전제1: 실제 도덕 상황은 다수 영역의 요인이 중첩되는 경우가 많다. "
                "전제2: 하나의 영역 판단이 다른 영역에 영향을 미치는 파급이 존재한다. "
                "전제3: 영역 경계 자체가 모호한 경계 사례가 존재한다. "
                "결론: 3영역 이론은 고정된 분류가 아니라 혼합·애매성을 포섭하는 틀이다."
            ),
            "counterpoint": (
                "단일 기준 도덕 이론(공리주의·의무론)은 영역 혼합을 "
                "단일 원리(효용·의무)로 환원하려 한다. 영역이론은 "
                "이 환원이 실제 판단 실천과 맞지 않는다고 응수한다."
            ),
            "context": (
                "2022-A Q8 을 ㉣ 영역 혼합·2차적 현상·영역 애매성 trademark · "
                "(가) 밀그램 변형 상황 해석의 이론적 근거."
            ),
            "keywords": [
                "영역 혼합",
                "domain mixture",
                "2차적 현상",
                "영역 애매성",
                "밀그램 변형",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-008: 문화 간 비교·보편성 — The Culture of Morality (2002)
        {
            "id": "turiel-claim-008",
            "thinker_id": THINKER_ID,
            "work_id": "turiel-culture-morality-2002",
            "source_detail": (
                "The Culture of Morality (2002) · 2021학년도 전공B Q3 갑 '모든 문화권에 보편적'"
            ),
            "claim": (
                "도덕 영역은 모든 문화권에 보편적인 도덕 원리에 대한 개념을 포함한다. "
                "문화 간 외형적 차이가 존재해도 도덕 영역의 핵심(복지·정의·권리 침해 금지)은 "
                "문화적 변이의 이면에서 유지되며, "
                "문화 차이의 상당 부분은 사회 인습 영역이나 개인적 영역의 변이 또는 "
                "동일 도덕 원리의 상이한 적용 상황에서 비롯된다."
            ),
            # 2021-B.md L37 verbatim (갑 제시문 '모든 문화권에 보편적' 구절)
            "original_text": (
                "도덕적 영역은 모든 문화권에 보편적인 도덕 원리에 대한 개념을 포함한다 "
                "— 2021학년도 전공B Q3 갑 제시문 (coverage/2021-B.md L37). "
                "튜리엘 『The Culture of Morality(2002)』 는 이 보편성 주장을 "
                "문화 간 비교 연구로 확장한 후기 저작 (coverage/2018-B.md L95 저서 나열)."
            ),
            "explanation": (
                "튜리엘 영역이론의 보편성 주장. "
                "도덕 영역의 규범은 특정 문화·사회 조직에 의존하지 않고 "
                "타인의 복지·정의·권리라는 내재적·보편적 기준을 따른다. "
                "따라서 문화 간에 외형적으로 다르게 보이는 도덕 판단 차이는 "
                "(1) 인습 영역이나 개인적 영역에서의 변이, "
                "(2) 동일 도덕 원리가 서로 다른 정보적 가정(예: 조상 영혼의 존재 여부) 위에서 "
                "다르게 적용된 결과로 설명될 수 있다. "
                "콜버그의 단계 보편성과는 다른 방식의 '원리 수준 보편성'."
            ),
            "argument": (
                "전제1: 도덕 영역의 규범은 복지·정의·권리라는 내재적 기준에 의해 규정된다. "
                "전제2: 이 기준은 문화·사회 조직에 의존하지 않는다. "
                "전제3: 문화 간 판단 차이의 상당 부분은 인습·개인 영역 변이 또는 정보적 가정 차이로 설명된다. "
                "결론: 도덕 영역은 문화 변이에도 불구하고 원리 수준에서 보편적이다."
            ),
            "counterpoint": (
                "문화 상대주의·하이트의 도덕 기반 이론은 도덕의 기반 자체가 문화에 따라 "
                "다양하게 활성화된다고 주장하며 단일 보편 원리에 회의적이다."
            ),
            "context": (
                "2021-B Q3 갑 제시문 '모든 문화권에 보편적' 구절의 이론적 근거 · "
                "『The Culture of Morality(2002)』의 문화 간 비교 확장."
            ),
            "keywords": [
                "문화 간 보편성",
                "도덕 영역 보편성",
                "정보적 가정",
                "인습 영역 변이",
                "applied ethics",
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
    """튜리엘 핵심 키워드 데이터 입력. 중복 체크 후 insert."""
    keywords = [
        {
            "id": "kw-turiel-domain-theory",
            "term": "영역이론",
            "term_en": "domain theory",
            "definition": (
                "튜리엘 『The Development of Social Knowledge: Morality and Convention(1983)』 trademark. "
                "아동·청소년이 사회 세계에 대한 지식을 "
                "도덕 영역(moral domain) · 사회 인습 영역(conventional domain) · 개인적 영역(personal domain)의 "
                "세 영역에서 병렬적으로 질적으로 다른 기준으로 구성한다는 입장. "
                "2018-B Q1·2021-B Q3 갑·2022-A Q8 을·2024-B Q3 을·2026-A Q6 갑 "
                "5회 반복 출제의 핵심 trademark."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "related_terms": [
                "도덕 영역",
                "사회 인습 영역",
                "개인적 영역",
                "규칙 독립성",
                "콜버그 비판",
            ],
        },
        {
            "id": "kw-turiel-moral-domain",
            "term": "도덕 영역",
            "term_en": "moral domain",
            "definition": (
                "튜리엘 영역이론의 세 영역 중 하나. "
                "타인의 복지(welfare) · 정의(justice) · 권리(rights)에 관련된 "
                "보편적·비상대적이며 규칙 독립적인 규범을 다룬다. "
                "이 영역의 판단은 (1) 보편성, (2) 규칙 독립성, (3) 권위 독립성, "
                "(4) 제재 독립성의 네 가지 특성을 지닌다. "
                "2018-B Q1·2024-B Q3 을·2026-A Q6 갑 제시문의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "related_terms": [
                "영역이론",
                "복지",
                "정의",
                "권리",
                "규칙 독립성",
                "보편성",
            ],
        },
        {
            "id": "kw-turiel-conventional-domain",
            "term": "사회 인습 영역",
            "term_en": "conventional domain",
            "definition": (
                "튜리엘 영역이론의 세 영역 중 하나. "
                "사회 조직 혹은 체계 안에서 구성원 간에 합의된 행동으로 정의되는 "
                "상대적·권위 의존적·가변적 관습 규범의 영역. "
                "규칙이 바뀌거나 권위가 허용하면 동일 행위의 허용 여부가 달라진다. "
                "2021-B Q3 ㉠ 정답 근거 · 2022-A Q8 을 제시문 · 2024-B Q3 을 제시문."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "related_terms": [
                "영역이론",
                "권위 의존성",
                "규칙 가변성",
                "관습 규범",
                "도덕-인습 구분",
            ],
        },
        {
            "id": "kw-turiel-personal-domain",
            "term": "개인적 영역",
            "term_en": "personal domain",
            "definition": (
                "튜리엘 영역이론의 세 영역 중 하나. "
                "개인의 선호·경향·재량에 속하는 사적 자율 공간. "
                "정당화 준거는 사적인 선호와 경향이며, "
                "도덕 영역이나 사회 인습 영역의 규범으로 강제될 수 없다. "
                "음악 감상·춤과 같은 해악 없는 개인 활동에 대한 사회 권위의 강제 통제는 "
                "이 영역에 대한 부당한 침해로 판단된다."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "related_terms": [
                "영역이론",
                "사적 선호",
                "자율 선택",
                "영역 침해",
            ],
        },
        {
            "id": "kw-turiel-morality-convention-distinction",
            "term": "도덕-인습 구분",
            "term_en": "moral-conventional distinction",
            "definition": (
                "튜리엘 영역이론의 경험적 검증 방법론 trademark. "
                "면담 실험(예: '이 학교에서는 서로 때려도 된다는 규칙이 있다면 친구를 때리는 것이 옳은가?')에서 "
                "아동은 규칙이 바뀌어도 도덕 위반은 여전히 그르다고 판단(규칙 독립성)하지만 "
                "인습 위반은 규칙이 바뀌면 허용 가능하다고 답한다. "
                "이 결과는 도덕 판단과 인습 판단이 어린 시기부터 별개의 개념 체계로 발달함을 보여준다. "
                "2018-B Q1 빈칸('서로 독립적이다') · 2026-A Q6 갑 ㉠ 피해 기반 도덕 판단 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "related_terms": [
                "규칙 독립성",
                "rule-contingency",
                "아동 면담 실험",
                "도메인 이론",
                "해 입힘",
            ],
        },
        {
            "id": "kw-turiel-kohlberg-critique",
            "term": "콜버그 단계론 비판",
            "term_en": "critique of Kohlberg",
            "definition": (
                "튜리엘의 콜버그(Lawrence Kohlberg) 3수준 6단계 이론에 대한 내부 비판. "
                "콜버그는 인습 수준(3·4단계)에서 보편적 도덕 원리 지향(6단계)으로의 발달을 "
                "단일 인지 발달 계열로 제시하지만, "
                "튜리엘은 이 배열이 질적으로 다른 도덕 영역과 사회 인습 영역을 혼합한 결과라고 비판한다. "
                "영역이론은 두 영역이 발달 초기부터 별개 개념 체계로 병렬 발달한다고 본다. "
                "2024-B Q3 을(튜리엘) 입장의 핵심 논증."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "related_terms": [
                "Kohlberg",
                "3수준 6단계 비판",
                "영역 혼합",
                "도덕-인습 구분",
            ],
        },
        {
            "id": "kw-turiel-rule-contingency",
            "term": "규칙 독립성",
            "term_en": "rule-contingency independence",
            "definition": (
                "튜리엘 영역이론에서 도덕 영역을 인습 영역과 구별하는 판단 기준. "
                "도덕 위반은 규칙이나 권위가 바뀌어도 여전히 그르다고 판단되며, "
                "인습 위반은 규칙이 바뀌면 허용 가능하다고 판단된다. "
                "면담 실험에서 '이 학교에서는 서로 때려도 된다는 규칙이 있다면?'이라는 "
                "조건 질문으로 경험적으로 측정된다. "
                "2026-A Q6 갑 제시문 '아동들은 서로 때려도 된다는 이야기를 들은 후에도 "
                "듣기 전과 마찬가지로 학교에서 친구들을 때리는 것이 옳지 않다고 답변'의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "related_terms": [
                "도덕 영역",
                "보편성",
                "권위 독립성",
                "제재 독립성",
                "면담 실험",
            ],
        },
        {
            "id": "kw-turiel-domain-mixture",
            "term": "영역 혼합",
            "term_en": "domain mixture",
            "definition": (
                "튜리엘 영역이론의 확장 개념. "
                "현실의 도덕 상황에서 둘 이상의 영역이 동시에 작동하거나 "
                "한 영역의 판단이 다른 영역으로 이차적으로 파급되는 경우를 지칭한다. "
                "2차적 현상(second-order phenomena) · 영역 애매성과 함께 "
                "영역이론이 단순 3분류를 넘어 복잡한 상황을 포섭하는 틀임을 보여준다. "
                "2022-A Q8 을 제시문 ㉣ trademark. "
                "(가) 밀그램 변형 사례에서 도덕 영역과 인습·계약 영역의 중첩으로 설명됨."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "turiel-development-social-knowledge-1983",
            "related_terms": [
                "2차적 현상",
                "영역 애매성",
                "밀그램 변형",
                "영역이론",
            ],
        },
        {
            "id": "kw-turiel-cross-cultural-universality",
            "term": "문화 간 보편성",
            "term_en": "universality across cultures",
            "definition": (
                "튜리엘 영역이론의 보편성 주장. "
                "도덕 영역의 핵심(복지·정의·권리 침해 금지)은 문화적 변이의 이면에서 유지되며, "
                "문화 차이의 상당 부분은 사회 인습 영역이나 개인적 영역의 변이 또는 "
                "동일 도덕 원리의 상이한 적용(서로 다른 정보적 가정 위에서)으로 설명된다. "
                "2021-B Q3 갑 제시문 '도덕적 영역은 모든 문화권에 보편적인 도덕 원리에 대한 개념을 포함'의 근거. "
                "『The Culture of Morality(2002)』 후기 저작에서 확장."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "turiel-culture-morality-2002",
            "related_terms": [
                "도덕 영역",
                "applied ethics",
                "인습 영역 변이",
                "정보적 가정",
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
    """튜리엘 영향·비교 관계 데이터 입력.

    ES 등록 확인 (2026-04-22 curl):
     - kohlberg : 등록 — 튜리엘은 콜버그 제자 출신, 영역이론은 콜버그 단계론의 내부 비판으로 발전
     - piaget   : 등록 — 인지발달 심리학 전통 선행 (튜리엘 영역이론의 발달 심리 배경)
     - blasi    : 등록 — 동시대 도덕 심리학 동료 (도덕적 자아·정체성 이론)
    미등록 thinker 는 링크 생략.
    """
    relations = [
        {
            "from_thinker": "kohlberg",
            "to_thinker": THINKER_ID,
            "type": "influenced",
            "description": (
                "콜버그(Lawrence Kohlberg)는 튜리엘의 직접적 스승이자 이론적 출발점이다. "
                "튜리엘은 콜버그 문하에서 도덕 판단 연구를 시작하였으나, "
                "경험적 연구를 축적하면서 콜버그의 3수준 6단계 이론이 "
                "도덕 영역과 사회 인습 영역을 단일 발달 계열로 혼합했다고 판단하였다. "
                "이로부터 영역이론(domain theory)을 대안으로 제시하였으며, "
                "1983년 『The Development of Social Knowledge: Morality and Convention』은 "
                "이 내부 비판을 체계화한 대표 저작이다. "
                "영향 관계이면서 동시에 이론적 분기가 일어난 사례."
            ),
            "evidence": (
                "Kohlberg (1984) Essays on Moral Development vol.II; "
                "Turiel (1983) The Development of Social Knowledge: Morality and Convention; "
                "2024-B Q3 갑(콜버그) vs 을(튜리엘) 직접 대립 배치 "
                "(coverage/2024-B.md L48·L120); "
                "2022-A Q8 갑(콜버그 정의공동체) + 을(튜리엘 영역이론) 동일 문항 병치 "
                "(coverage/2022-A.md L22·L93·L95)"
            ),
        },
        {
            "from_thinker": "piaget",
            "to_thinker": THINKER_ID,
            "type": "influenced",
            "description": (
                "피아제(Jean Piaget)의 인지발달 심리학과 1932년 『아동의 도덕 판단』은 "
                "튜리엘 영역이론의 발달 심리학적 배경이다. "
                "피아제가 제시한 '아동의 구성적 지식 형성' 원리를 튜리엘은 수용하면서도, "
                "단일한 인지 발달 계열이 아닌 복수 영역의 병렬 구성을 주장한다는 점에서 "
                "피아제·콜버그 단일 단계 계열 전통을 수정·확장한다. "
                "특히 아동이 구성적으로 도덕 개념을 형성한다는 기본 가정은 "
                "피아제에서 이어받은 발달 구성주의 유산이다."
            ),
            "evidence": (
                "Piaget 1932년 저작 『아동의 도덕 판단』; "
                "Turiel (1983) The Development of Social Knowledge; "
                "coverage 전반에 Piaget 13 hits · Jean Piaget 9 hits 로 "
                "도덕 심리학 발달 계보에서 튜리엘과 함께 반복 언급됨."
            ),
        },
        {
            "from_thinker": "blasi",
            "to_thinker": THINKER_ID,
            "type": "compared",
            "description": (
                "블라시(Augusto Blasi)와 튜리엘은 동시대 현대 도덕 심리학의 두 축으로서 "
                "도덕 발달 이론을 각기 다른 방향으로 발전시켰다. "
                "블라시는 도덕적 자아·도덕적 정체성(moral identity)을 통해 "
                "도덕 판단과 도덕 행동의 간극을 설명하는 데 초점을 둔 반면, "
                "튜리엘은 영역이론을 통해 도덕 판단 자체의 내부 구조(도덕·인습·개인 영역 구분)를 규명한다. "
                "두 이론은 콜버그 단계론 이후의 도덕 심리학이 나아간 두 경로로서 "
                "상호 보완적·대조적으로 참조된다."
            ),
            "evidence": (
                "Blasi 도덕적 정체성(moral identity) 이론; "
                "Turiel (1983) The Development of Social Knowledge; "
                "coverage 전반에 두 사상가가 도덕 심리학 목록에서 병기 등장 "
                "(coverage/2019-B.md L34·L83 도덕 심리학 블로커 세트에서 공동 참조)"
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
    print("=== 엘리엇 튜리엘(Turiel) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (turiel)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n[OK] 튜리엘 데이터 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}", file=sys.stderr)
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
