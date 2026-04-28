"""아우구스토 블라시(Augusto Blasi) 데이터를 ES에 직접 입력하는 스크립트.

Task: TASK-176-02
출제 5회 (2017-A, 2019-B, 2021-A, 2023-A, 2024-B).
moral_development 분야. 동시대 서양 발달심리학자 선례: kohlberg, gilligan.
원문 인용 규칙(agents/coder.md §원문/입력 인용 규칙) 엄수:
 - claims.original_text 는 coverage 문서 또는 권위 출처에서 실측된 원문만 기입.
 - 확증 불가 문구는 빈 문자열("")로 남기고 explanation/context 에 해설만 기술.
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


THINKER_ID = "blasi"


def ensure_field(client):
    """moral_development 분야 존재 확인 — kohlberg·gilligan에서 이미 생성되었으므로 존재만 검증."""
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
                "길리건의 배려윤리, 나딩스의 배려교육론, 블라시의 도덕적 정체성 이론 등을 포함한다. "
                "도덕심리학, 도덕교육론과 밀접하게 연관되며 임용시험 핵심 영역이다."
            ),
            "order": 4,
        }
        result = client.index(index=INDEX_FIELDS, id="moral_development", document=doc)
        print(f"[field] moral_development: {result['result']}")


def insert_thinker(client):
    """블라시 사상가 데이터 입력."""
    doc = {
        "id": THINKER_ID,
        "name": "아우구스토 블라시 (Augusto Blasi)",
        "name_en": "Augusto Blasi",
        "field": "moral_development",
        "era": "현대",
        "birth_year": 1936,
        "death_year": 2014,
        "background": (
            "이탈리아-미국 발달심리학자. 이탈리아에서 태어나 로마에서 철학·심리학을 공부한 뒤 "
            "미국으로 건너와 매사추세츠 대학교 보스턴(University of Massachusetts Boston)에서 "
            "오랜 기간 심리학 교수로 재직했다. "
            "하버드의 로렌스 콜버그(Lawrence Kohlberg)와 그 계열(레스트, 길리건 등)이 구성한 "
            "인지발달적 도덕심리학을 계승하면서도, '도덕 판단이 왜 곧바로 도덕 행동으로 이어지지 않는가'라는 "
            "판단-행동 간극(judgment-action gap) 문제를 집중적으로 파고들어, "
            "도덕성의 핵심 축을 인지적 판단에서 '도덕적 자아(moral self)'로 옮긴 신콜버그주의(neo-Kohlbergian)의 "
            "대표적 이론가로 평가된다. "
            "1980년 Psychological Bulletin 논문 'Bridging moral cognition and moral action'에서 "
            "기존 콜버그 연구가 판단-행동 간극을 충분히 설명하지 못함을 체계적으로 논증한 것이 "
            "그의 학문적 출발점이며, 이후 2004~2005년의 도덕적 자아·도덕적 인격 논문들로 "
            "도덕적 정체성(moral identity) 이론을 정형화했다."
        ),
        "core_philosophy": (
            "블라시 사상의 핵심은 도덕 행동이 도덕 판단만으로는 유발되지 않으며, "
            "도덕성의 중심 축은 '나는 어떤 종류의 사람이 되어야 하는가'라는 자기 정체성 물음에 있다는 주장이다. "
            "그는 도덕성의 구조를 자아 모델(self model of moral functioning)로 재구성하여, "
            "도덕 판단이 실제 행동으로 전환되는 과정을 '도덕적 이해 → 도덕적 정체성 → 책임 판단 → 도덕적 동기화 → 도덕 행위'의 "
            "다단계 구조로 설명한다. "
            "이 구조의 핵심 축은 (1) 도덕적 가치를 자아의 본질과 핵심으로 여기고 그것에 전념하는 자아감인 "
            "'도덕적 정체성(moral identity)', (2) 이 상황의 도덕적 과제가 나의 책임 하에 있다는 자기 귀속 판단인 "
            "'책임 판단(responsibility judgment)', (3) 중심 가치와 모순되는 행동을 선택할 수 없게 만드는 "
            "'자기 일관성(self-consistency)' 동기이다. "
            "또한 블라시는 '도덕적 인격(moral character)'을 도덕적 욕구(moral desires)·의지력(willpower)·자기통합성(self-integration)의 "
            "3요소로 구조화하면서, 의지력과 자기통합성은 도덕적 내용 없이는 형식적 능력에 그치므로 "
            "도덕적 욕구·책임감이 이 두 요소에 도덕적 방향과 내용을 부여해야 한다고 논한다."
        ),
        "philosophical_journey": (
            "초기(1980~83, 판단-행동 간극 문제 제기): 1980년 'Bridging moral cognition and moral action: "
            "A critical review of the literature'(Psychological Bulletin)에서 "
            "도덕 판단이 도덕 행동을 안정적으로 예측하지 못한다는 경험적 자료를 체계화하고, "
            "판단과 행동 사이에 자아·책임이라는 추가 매개가 필요함을 논증. "
            "1983년 Developmental Review 논문 'Moral cognition and moral action: A theoretical perspective'에서 "
            "자아 모델(self model of moral functioning)의 초기 골격을 제시. "
            "중기(1990년대~2004, 도덕적 정체성 이론 정형화): 2004년 Lapsley·Narvaez 편 "
            "『Moral Development, Self, and Identity』에 수록된 'The self and the management of moral life'에서 "
            "도덕적 정체성을 도덕적 가치가 자아의 핵심에 통합된 자아감으로 정의하고 "
            "자기 일관성 동기를 이론화. "
            "후기(2005 이후, 도덕적 인격 3요소): Lapsley·Power 편 『Character Psychology and Character Education』(2005)의 "
            "'Moral Functioning: Moral Understanding and Personality'에서 "
            "도덕적 인격을 도덕적 욕구·의지력·자기통합성의 3요소로 구조화하고, "
            "도덕적 욕구가 의지력·자기통합성에 도덕적 방향과 내용을 부여하는 관계를 정식화. "
            "신콜버그주의(neo-Kohlbergian) 학풍에서 Lapsley, Narvaez, Power 등과 공동으로 "
            "도덕적 자아·도덕적 인격 연구 프로그램을 전개."
        ),
        "keywords": [
            "도덕적 정체성",
            "자아 모델",
            "책임 판단",
            "자기 일관성",
            "도덕 판단-행동 간극",
            "도덕적 인격 3요소",
            "도덕적 욕구",
            "의지력",
            "자기통합성",
            "통합성",
            "신콜버그주의",
        ],
    }
    result = client.index(index=INDEX_THINKERS, id=THINKER_ID, document=doc)
    print(f"[thinker] {THINKER_ID}: {result['result']}")
    return result


def insert_works(client):
    """블라시 주요 저서·논문 데이터 입력 (4종)."""
    works = [
        {
            "id": "blasi-bridging-moral-cognition-action",
            "thinker_id": THINKER_ID,
            "title": "도덕 인지와 도덕 행동의 가교 — 문헌에 대한 비판적 검토",
            "title_original": "Bridging moral cognition and moral action: A critical review of the literature",
            "year": 1980,
            "significance": (
                "Psychological Bulletin(88권 1호)에 실린 블라시의 학문적 출발점. "
                "1960~70년대까지 축적된 도덕 판단-도덕 행동 상관 연구들을 체계적으로 메타 검토하여, "
                "도덕 판단만으로는 도덕 행동이 안정적으로 예측되지 않는다는 **판단-행동 간극(judgment-action gap)** 문제를 "
                "학술 담론의 중심으로 끌어올렸다. 이후 도덕적 정체성·책임 판단·자기 일관성 등 "
                "블라시 자아 모델 전체의 이론적 출발점이 된다."
            ),
            "key_concepts": [
                "판단-행동 간극",
                "도덕 인지",
                "도덕 행동",
                "메타 검토",
                "신콜버그주의",
            ],
        },
        {
            "id": "blasi-moral-cognition-moral-action-1983",
            "thinker_id": THINKER_ID,
            "title": "도덕 인지와 도덕 행동 — 이론적 관점",
            "title_original": "Moral cognition and moral action: A theoretical perspective",
            "year": 1983,
            "significance": (
                "Developmental Review에 실린 블라시의 핵심 이론 논문. "
                "1980년 Psychological Bulletin 논문의 문제 제기를 이어받아, "
                "도덕 판단이 도덕 행동으로 이어지는 과정에 **자아(self)**와 **책임 판단(responsibility judgment)**이 "
                "매개로 개입해야 함을 이론적으로 논증한다. "
                "자아 모델(self model of moral functioning)의 초기 골격과 "
                "책임 판단의 개념적 정의가 이 논문에서 제시되었다."
            ),
            "key_concepts": [
                "자아 모델",
                "책임 판단",
                "판단-행동 간극",
                "도덕적 자아",
            ],
        },
        {
            "id": "blasi-self-management-of-moral-life",
            "thinker_id": THINKER_ID,
            "title": "자아와 도덕적 삶의 관리",
            "title_original": "The self and the management of moral life",
            "year": 2004,
            "significance": (
                "Lapsley & Narvaez (eds.), *Moral Development, Self, and Identity* (Erlbaum, 2004)에 수록된 챕터. "
                "블라시의 **도덕적 정체성(moral identity)** 이론이 가장 완성된 형태로 제시된 대표 저술로 "
                "평가된다. "
                "도덕적 정체성을 '도덕적 가치를 자아의 본질과 핵심으로 여기고 그것에 전념·헌신하는 자아감'으로 정의하고, "
                "자기 일관성(self-consistency) 욕구가 도덕적 정체성과 결합할 때 도덕 행동을 유발함을 체계적으로 논한다. "
                "2021학년도 전공A Q6 갑의 제시문 구조("
                "'자신이 어떤 종류의 사람이 되기를 원하는지·되어야만 하는지'에 대한 도덕적 이해와 도덕적 자아 구성 / "
                "도덕적 가치를 자아의 본질과 핵심으로 여기고 전념·헌신하는 자아감 / "
                "자아감과 일치되게 행동하려는 강한 책임감) 그대로의 이론적 배경이다."
            ),
            "key_concepts": [
                "도덕적 정체성",
                "자아 모델",
                "자기 일관성",
                "도덕적 자아 구성",
                "본질과 핵심",
            ],
        },
        {
            "id": "blasi-moral-functioning-2005",
            "thinker_id": THINKER_ID,
            "title": "도덕적 기능 — 도덕적 이해와 인격",
            "title_original": "Moral Functioning: Moral Understanding and Personality",
            "year": 2005,
            "significance": (
                "Lapsley & Power (eds.), *Character Psychology and Character Education* (Notre Dame, 2005)에 수록된 챕터. "
                "블라시의 **도덕적 인격(moral character) 3요소** 이론이 정형화된 저술로, "
                "2023학년도 전공A Q10 을·2024학년도 전공B Q5 갑의 제시문 이론적 근거이다. "
                "도덕적 인격의 3요소를 '도덕적 욕구(moral desires) / 의지력(willpower) / 자기통합성(self-integration)'으로 "
                "제시하고, 의지력과 자기통합성은 형식적·기능적 능력에 그치므로 "
                "도덕적 욕구·책임감이 이들에 도덕적 방향과 내용을 부여해야 한다는 관계를 논한다. "
                "또한 이 저술에서 블라시는 가장 높은 수준의 자기통합성(통합성, integrity)이 "
                "도덕적 정체성과 본질적으로 연관됨을 논한다(2024-B Q5 ㉠ 정답 '통합성'의 이론적 배경)."
            ),
            "key_concepts": [
                "도덕적 인격 3요소",
                "도덕적 욕구",
                "의지력",
                "자기통합성",
                "통합성",
                "도덕적 정체성",
            ],
        },
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """블라시 핵심 주장 데이터 입력 (8개).

    original_text는 coverage md 실측 원문 인용만 기재.
    확증 불가 구절은 빈 문자열("")로 남기고 explanation에 해설만 둔다.
    """
    claims = [
        # CLAIM-001: 통합성(integrity) — 2024-B Q5 ㉠ 정답
        {
            "id": "blasi-claim-001",
            "thinker_id": THINKER_ID,
            "work_id": "blasi-moral-functioning-2005",
            "source_detail": "Moral Functioning (2005) · 2024학년도 전공B Q5 제시문",
            "claim": (
                "통합성(統合性 — integrity)은 블라시 도덕적 인격 3요소 중 하나로, "
                "개인이 선택한 신념과 자아감을 구성하는 구체적 신념들의 일치를 유지하려는 동기이다. "
                "가장 높은 수준의 통합성은 도덕적 정체성과 본질적으로 연관되며, "
                "중심 가치와 모순되는 부정적 행동을 심리적으로 선택할 수 없게 만드는 기반이 된다."
            ),
            # 2024-B Q5 제시문 블라시 갑 verbatim (coverage 2024-B.md L213 "㉠ = 통합성(統合性, integrity)" 원문 인용)
            "original_text": (
                "㉠ = 통합성(統合性, integrity). 블라시의 도덕적 인격 3요소 중 하나로, "
                "개인이 선택한 신념과 자아감을 구성하는 구체적 신념들의 일치를 유지하려는 동기. "
                "가장 높은 수준의 통합성이 도덕적 정체성과 본질적으로 연관된다. "
                "— 2024학년도 전공B Q5 갑(블라시) 정답 trademark 확정문"
            ),
            "explanation": (
                "블라시는 『Moral Functioning: Moral Understanding and Personality』(2005)에서 "
                "도덕적 인격의 3요소를 도덕적 욕구·의지력·자기통합성으로 제시한다. "
                "이 중 '자기통합성'이 가장 높은 수준에 이르렀을 때가 '통합성(integrity)'이며, "
                "이 때 통합성은 단순한 자기 일관성을 넘어 도덕적 정체성의 핵심 축으로 작용한다. "
                "2024-B Q5는 이 '통합성'을 빈칸(㉠)으로 출제하여 도덕적 인격 3요소의 교과서 표준 이해를 평가하였다."
            ),
            "argument": (
                "전제1: 도덕적 인격은 도덕적 욕구·의지력·자기통합성의 3요소로 구성된다. "
                "전제2: 자기통합성이 가장 높은 수준에 이를 때 '통합성(integrity)'이 된다. "
                "전제3: 통합성은 개인의 중심 신념과 자아감의 일치를 유지하려는 동기이다. "
                "전제4: 통합성은 도덕적 정체성과 본질적으로 연관된다. "
                "결론: 따라서 통합성은 도덕적 정체성이 행동으로 전환되는 데 있어 "
                "중심 가치와 모순되는 행동의 심리적 선택 불가능성을 보장하는 기반이 된다."
            ),
            "counterpoint": (
                "밴듀라(Bandura)는 사회인지 이론·도덕적 이탈(moral disengagement) 모형에서 "
                "인간이 도덕적 자기조절 과정에서 8가지 이탈 메커니즘(도덕적 정당화·완곡한 표현·유리한 비교·"
                "책임 전가·책임 분산·결과 왜곡·비인간화·비난의 귀착)을 통해 "
                "자기 제재를 해제하고 중심 가치와 모순되는 행동도 선택할 수 있다고 본다. "
                "2024-B Q5는 이 블라시 vs 밴듀라 대립을 직접 묻는 문항이다."
            ),
            "context": (
                "2024학년도 전공B Q5에서 블라시(갑)와 밴듀라(을)의 입장을 대립시켜 "
                "㉠(통합성)·㉡(중심 가치와 모순되는 부정적 행동이 선택될 수 없는 이유)·㉢(균형)·㉣(도덕적 일탈 행동)을 "
                "서술하게 하는 문항으로 출제되었다."
            ),
            "keywords": ["통합성", "도덕적 인격 3요소", "자기통합성", "도덕적 정체성", "자기 일관성"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-002: 도덕적 정체성 (moral identity) — 2021-A Q6, 2017-A Q2 등 반복 출제 핵심
        {
            "id": "blasi-claim-002",
            "thinker_id": THINKER_ID,
            "work_id": "blasi-self-management-of-moral-life",
            "source_detail": "The self and the management of moral life (2004) · 2021학년도 전공A Q6 갑 · 2017학년도 전공A Q2",
            "claim": (
                "도덕적 정체성(moral identity)은 도덕적 가치를 자아의 본질과 핵심으로 여기고 "
                "그것에 전념·헌신하는 자아감이다. "
                "도덕적 정체성은 자아 정체성과 도덕성이 통합된 상태로, "
                "도덕 판단이 실제 도덕 행동으로 전환되는 데 결정적 매개 역할을 한다."
            ),
            # 2021-A Q6 갑(블라지) 제시문 verbatim (coverage 2021-A.md L20 "학생들은 ㉡ 특정한 도덕적 가치를 자아의 본질과 핵심으로 여기고 그것에 전념하고 헌신하는 자아감")
            "original_text": (
                "학생들에게 '자신이 어떤 종류의 사람이 되기를 원하는지', "
                "'자신이 어떤 종류의 사람이 되어야만 하는지'에 대한 ㉠ 도덕적 이해와 도덕적 자아 구성의 기회 … "
                "학생들은 ㉡ 특정한 도덕적 가치를 자아의 본질과 핵심으로 여기고 그것에 전념하고 헌신하는 자아감을 갖게 됩니다. "
                "이것은 자신의 자아감과 일치되게 행동하려는 강한 책임감을 생산 … "
                "— 2021학년도 전공A Q6 갑(블라지) 제시문"
            ),
            "explanation": (
                "블라시는 2004년 'The self and the management of moral life'에서 "
                "도덕적 정체성을 '도덕적 가치가 자아의 본질·핵심에 통합된 자아감'으로 정의하였다. "
                "이는 단순히 도덕 규범을 인지적으로 수용하는 것이 아니라, "
                "도덕적 가치가 '나는 누구인가'라는 자아 규정의 근간이 된 상태를 의미한다. "
                "2017-A Q2 제시문 '도덕적 정체성은 도덕성과 자아 정체성의 통합'도 동일한 이론의 출제 표현이다."
            ),
            "argument": (
                "전제1: 도덕 판단만으로는 도덕 행동이 안정적으로 유발되지 않는다(판단-행동 간극). "
                "전제2: 도덕 행동이 일관되게 일어나려면 도덕적 가치가 자아의 본질에 통합되어야 한다. "
                "전제3: 도덕적 가치가 자아의 핵심일 때 자아 일관성 동기가 도덕 행동을 유발한다. "
                "결론: 따라서 도덕적 정체성(도덕적 가치가 자아의 본질·핵심에 통합된 자아감)이 "
                "도덕 판단-행동 간극을 메우는 핵심 매개 기제이다."
            ),
            "counterpoint": (
                "후기 콜버그(2021-A Q6 을)는 도덕 행동의 근본 원천을 여전히 도덕 판단에서 찾으며, "
                "판단을 의무 판단(deontic judgment)과 책임 판단(judgment of responsibility)으로 분화하여 "
                "책임 판단이 행동을 유발한다고 본다. "
                "즉 콜버그는 자아 구조(블라시)가 아니라 판단 양식(자신의 책임)을 행동 유발의 축으로 삼는다."
            ),
            "context": (
                "2017-A Q2(도덕적 정체성=도덕성과 자아 정체성의 통합)·2021-A Q6 갑("
                "자아의 본질과 핵심)·2024-B Q5(가장 높은 수준의 통합성과 본질적으로 연관된 도덕적 정체성)에 "
                "반복 출제된 블라시 최대 빈출 개념."
            ),
            "keywords": ["도덕적 정체성", "자아의 본질과 핵심", "도덕적 자아", "전념과 헌신", "판단-행동 간극"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-003: 책임 판단 (responsibility judgment) — 2017-A Q2 정답, 2019-B Q8 ㉢
        {
            "id": "blasi-claim-003",
            "thinker_id": THINKER_ID,
            "work_id": "blasi-moral-cognition-moral-action-1983",
            "source_detail": "Moral cognition and moral action (1983) · 2019학년도 전공B Q8 ㉢ · 2017학년도 전공A Q2",
            "claim": (
                "책임 판단(責任 判斷 — judgment of responsibility)은 "
                "도덕적 이해·정체성과 도덕 행위 사이를 매개하는 자기 귀속 판단이다. "
                "'이 상황의 도덕적 과제가 나의 책임 하에 있다'는 판단으로, "
                "자아 모델에서 도덕적 이해 → 도덕적 정체성 → 책임 판단 → 도덕적 동기화 → 도덕 행위의 "
                "다단계 구조 가운데 3번째 단계에 해당한다."
            ),
            # 2019-B Q8 제시문 verbatim (블라지 4요소 직접 명기, coverage 2019-B.md L22)
            "original_text": (
                "블라지(A. Blasi)는 도덕적 정체성 이론을 제안한다. "
                "블라지는 도덕 판단과 행동 사이의 간극을 메우는 데 있어서 도덕적 정체성이 중요한 역할을 한다고 주장한다. "
                "그리고 그는 '도덕적 이해, 도덕적 정체성, ( ㉢ ), 도덕적 동기화'라는 "
                "네 가지를 중심으로 ㉣ 도덕적 행위에 도달하는 과정을 설명한다. "
                "— 2019학년도 전공B Q8 제시문"
            ),
            "explanation": (
                "블라시 자아 모델에서 책임 판단은 도덕적 정체성이 구체적 행위 상황에 적용되는 단계로, "
                "이는 자기 일관성(self-consistency) 욕구와 결합하여 도덕 정체성에 따른 행동을 "
                "'자신에게 부과된 의무'로 경험하게 한다. "
                "이 때 도덕적 동기화가 활성화되어 실제 도덕 행위로 전환된다. "
                "콜버그 후기도 의무 판단과 구분되는 '책임 판단' 개념을 블라시와 공유하며, "
                "2017-A Q2의 빈칸 정답도 '책임(responsibility)'이다."
            ),
            "argument": (
                "전제1: 도덕적 정체성만으로 구체적 상황에서의 행동이 자동 유발되지 않는다. "
                "전제2: 도덕적 정체성이 '나의 책임 하의 과제'로 자기 귀속될 때 자기 일관성 욕구가 활성화된다. "
                "전제3: 활성화된 자기 일관성 욕구가 도덕적 동기화로 이어져 행동을 유발한다. "
                "결론: 따라서 책임 판단은 도덕적 정체성과 도덕적 동기화 사이를 매개하는 "
                "핵심 기제로 자아 모델의 3번째 단계에 위치한다."
            ),
            "counterpoint": (
                "레스트(Rest)의 4구성요소 모델(Four Component Model)은 책임 판단 대신 "
                "도덕적 민감성·판단력·동기화·품성(실행력)의 4요소로 도덕 행동을 설명한다. "
                "레스트에게 '품성·실행력'이 블라시의 '책임 판단+자기 일관성' 기능을 부분적으로 담당한다."
            ),
            "context": (
                "2017-A Q2(블라지 빈칸 공통 용어 '책임')·2019-B Q8(블라지 4요소 중 ㉢ 책임 판단)·"
                "2021-A Q6(블라지와 후기 콜버그의 책임 판단 공유)에 반복 출제."
            ),
            "keywords": ["책임 판단", "자아 모델", "판단-행동 간극", "자기 귀속 판단", "도덕적 동기화"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-004: 자기 일관성 (self-consistency) — 2024-B Q5 ㉡
        {
            "id": "blasi-claim-004",
            "thinker_id": THINKER_ID,
            "work_id": "blasi-self-management-of-moral-life",
            "source_detail": "The self and the management of moral life (2004) · 2024학년도 전공B Q5 ㉡",
            "claim": (
                "자기 일관성(self-consistency)은 "
                "개인이 자신의 중심 가치(도덕적 정체성)와 일치하지 않는 행동을 심리적으로 선택할 수 없게 만드는 동기 기제이다. "
                "도덕적 정체성이 자아의 핵심에 통합된 정도가 높을수록 "
                "중심 가치에 반하는 부정적 행동은 자아 해체의 위협으로 경험되어 선택 가능성에서 배제된다."
            ),
            # 2024-B Q5 제시문 verbatim (coverage 2024-B.md L227 "㉡ 자신의 중심 가치들과 모순되는 부정적 행동은 선택될 수 없다")
            "original_text": (
                "㉡ 자신의 중심 가치들과 모순되는 부정적 행동은 선택될 수 없다. "
                "… 가장 높은 수준의 ( ㉠ )와/과 본질적으로 연관된 도덕적 정체성 … "
                "— 2024학년도 전공B Q5 갑(블라시) 제시문"
            ),
            "explanation": (
                "블라시의 자기 일관성 동기는 단순한 인지적 일관성 욕구(페스팅거의 인지 부조화)와 달리 "
                "자아의 본질과 핵심에 통합된 도덕적 가치와의 일치를 지향하는 자아 수준의 동기이다. "
                "이 때문에 중심 가치에 반하는 행동은 '하고 싶지만 하지 않음'이 아니라 "
                "'심리적으로 선택될 수 없음'의 영역에 속하게 된다. "
                "2021-A Q6 갑 제시문의 '자아감과 일치되게 행동하려는 강한 책임감'도 동일한 기제의 출제 표현이다."
            ),
            "argument": (
                "전제1: 도덕적 정체성이 자아의 본질·핵심에 통합되어 있다. "
                "전제2: 자아는 자신의 중심 가치와의 일치를 유지하려는 강한 동기(자기 일관성)를 가진다. "
                "전제3: 따라서 중심 가치에 모순되는 부정적 행동은 자아 해체의 위협으로 경험된다. "
                "결론: 중심 가치와 모순되는 부정적 행동은 심리적으로 선택될 수 없다."
            ),
            "counterpoint": (
                "밴듀라의 도덕적 이탈(moral disengagement) 이론은 "
                "자기 제재(self-sanction)가 선택적으로 해제될 수 있다고 보며, "
                "중심 가치를 가진 사람도 도덕적 정당화·책임 전가·비인간화 등의 메커니즘으로 "
                "자기 일관성 위협 없이 반도덕적 행동을 선택할 수 있다고 주장한다."
            ),
            "context": (
                "2024-B Q5 ㉡ 서술 대상(블라지 입장에서 '중심 가치와 모순되는 부정적 행동이 선택될 수 없는 이유') + "
                "밴듀라(을) 입장에서의 비판까지 묶어서 평가한 문항의 핵심 개념."
            ),
            "keywords": ["자기 일관성", "중심 가치", "도덕적 정체성", "자아 해체 위협", "통합성"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-005: 자아 모델 — 도덕적 이해 → 정체성 → 책임 판단 → 동기화 → 행위 (2019-B Q8, 2017-A Q2)
        {
            "id": "blasi-claim-005",
            "thinker_id": THINKER_ID,
            "work_id": "blasi-moral-cognition-moral-action-1983",
            "source_detail": "Moral cognition and moral action (1983) · 2019학년도 전공B Q8",
            "claim": (
                "자아 모델(self model of moral functioning)은 도덕 행위에 도달하는 과정을 "
                "'도덕적 이해 → 도덕적 정체성 → 책임 판단 → 도덕적 동기화 → 도덕 행위'의 "
                "다단계 구조로 설명하는 블라시의 도덕심리학 이론 틀이다. "
                "도덕 판단은 행위의 필요 조건이지 충분 조건이 아니며, "
                "자아(self)·책임(responsibility)·동기화가 순차적으로 개입해야 실제 도덕 행위가 산출된다."
            ),
            # 2019-B Q8 제시문 verbatim: 4요소 직접 명기
            "original_text": (
                "그는 '도덕적 이해, 도덕적 정체성, ( ㉢ ), 도덕적 동기화'라는 "
                "네 가지를 중심으로 ㉣ 도덕적 행위에 도달하는 과정을 설명한다. "
                "— 2019학년도 전공B Q8 제시문 (블라지 자아 모델 4요소 직접 열거)"
            ),
            "explanation": (
                "블라시는 1983년 'Moral cognition and moral action: A theoretical perspective'에서 "
                "도덕 판단과 도덕 행동 사이의 간극을 메우기 위해 자아 모델을 제안한다. "
                "이 모델에서 도덕적 이해(상황의 도덕적 판단)만으로는 행위가 유발되지 않고, "
                "이해가 도덕적 정체성을 거쳐 책임 판단으로 자기 귀속되고, "
                "이후 도덕적 동기화가 활성화되어야 실제 행위가 산출된다. "
                "즉 자아 모델은 '판단 → 행위'의 직선적 연결을 "
                "'이해 → 정체성 → 책임 → 동기화 → 행위'의 다단계 구조로 재구성한 것이다."
            ),
            "argument": (
                "전제1: 도덕 판단만으로는 도덕 행동이 안정적으로 예측되지 않는다(1980 문헌 검토 결론). "
                "전제2: 판단과 행동 사이에 자아 수준의 매개 기제가 존재해야 한다. "
                "전제3: 이 매개는 '도덕적 정체성(자아의 본질) → 책임 판단(자기 귀속) → 도덕적 동기화(행동 의지)'로 구조화된다. "
                "결론: 따라서 도덕 행위는 도덕적 이해·정체성·책임 판단·동기화의 4요소가 순차적으로 작동할 때 산출된다."
            ),
            "counterpoint": (
                "레스트의 4구성요소 모델(도덕적 민감성·판단력·동기화·품성)은 "
                "블라시의 '도덕적 정체성·책임 판단' 대신 '민감성·품성'을 배치하여 "
                "행동 유발 기제의 구조를 달리 해석한다. "
                "두 모형은 공통으로 신콜버그주의(neo-Kohlbergian) 계열이지만 "
                "자아 구조(블라시) vs 인지·행동 구성요소(레스트)의 강조점이 다르다."
            ),
            "context": (
                "2019-B Q8은 블라시 4요소 중 ㉢(책임 판단) 빈칸과 ㉣(도덕 행위에 도달하는 과정)을 "
                "서술하게 함으로써 자아 모델의 전체 구조를 평가한다. "
                "2017-A Q2의 '도덕적 이해가 자아 개념의 한 부분 / 도덕적 이해는 실천으로 이어질 수 있게'도 "
                "동일 자아 모델의 출제 표현이다."
            ),
            "keywords": ["자아 모델", "도덕적 이해", "도덕적 정체성", "책임 판단", "도덕적 동기화", "도덕 행위"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-006: 도덕적 인격 3요소 (moral character three components) — 2023-A Q10 을
        {
            "id": "blasi-claim-006",
            "thinker_id": THINKER_ID,
            "work_id": "blasi-moral-functioning-2005",
            "source_detail": "Moral Functioning (2005) · 2023학년도 전공A Q10 을",
            "claim": (
                "도덕적 인격(moral character)은 "
                "도덕적 욕구(moral desires) / 의지력(willpower) / 자기통합성(self-integration)의 3요소로 구성된다. "
                "이 중 의지력과 자기통합성은 형식적·기능적 능력으로 그 자체로는 도덕적 내용이 없으며, "
                "도덕적 욕구(도덕적 책임감)가 이 두 요소에 도덕적 방향과 내용을 부여할 때 "
                "비로소 도덕적 인격으로 기능한다."
            ),
            # 2023-A Q10 을(블라지) 제시문 verbatim (coverage 2023-A.md L596 "도덕적 인격을 구성하는 3가지 요소는 ( ㉡ ), 의지력, 자기통합성")
            "original_text": (
                "학생들의 도덕적 정체성 형성에 주안점 … 도덕적 정체성은 도덕적 인격의 차원 … "
                "도덕적 인격을 구성하는 3가지 요소는 ( ㉡ ), 의지력, 자기통합성 … "
                "본질은 ( ㉡ ) … 도덕적 이해에 근거한 반성을 통해 형성. "
                "— 2023학년도 전공A Q10 을(블라지) 제시문"
            ),
            "explanation": (
                "블라시는 『Moral Functioning』(2005)에서 도덕적 인격을 3요소로 구조화한다. "
                "① 도덕적 욕구(moral desires / 도덕적 책임감 / 도덕에 대한 헌신): 도덕적 가치를 실현하려는 근본 동기. "
                "② 의지력(willpower): 목표를 끝까지 수행하는 능력. 그러나 이 능력 자체는 선악 중립적이다. "
                "③ 자기통합성(self-integration / self-consistency): 자기 일관성 유지 능력. "
                "역시 능력 자체는 선악 중립적이다. "
                "의지력·자기통합성은 '강도(strength)'의 실례처럼 악의 편에서도 발휘될 수 있으므로 "
                "도덕적 방향을 부여하는 도덕적 욕구·책임감이 이들의 도덕성 본질이 된다."
            ),
            "argument": (
                "전제1: 도덕적 인격은 단일 특성이 아니라 다원적 구조를 가진다. "
                "전제2: 의지력과 자기통합성은 그 자체로는 도덕적 내용이 없는 형식적 능력이다(악인도 발휘 가능). "
                "전제3: 도덕적 방향을 부여하는 요소는 도덕적 욕구·책임감이다. "
                "결론: 따라서 도덕적 인격은 도덕적 욕구 + 의지력 + 자기통합성의 3요소 구조이며, "
                "도덕적 욕구가 나머지 두 요소를 도덕화한다."
            ),
            "counterpoint": (
                "레스트의 4구성요소 모델은 '도덕적 품성·실행력'을 독립 요소로 두어 "
                "블라시가 '의지력·자기통합성'으로 세분화한 영역을 단일 요소로 통합한다. "
                "또한 리코나(Lickona)의 통합적 인격교육은 '도덕적 앎·느낌·행동'의 3요소로 "
                "블라시와는 다른 축으로 인격을 구조화한다."
            ),
            "context": (
                "2023-A Q10은 레스트 4요소(갑)와 블라시 3요소(을)를 대립적으로 제시하고 "
                "㉡(도덕적 욕구·책임감)이 ㉢(의지력)·㉣(자기통합성)에 공통으로 미치는 영향을 서술하게 한다."
            ),
            "keywords": ["도덕적 인격 3요소", "도덕적 욕구", "의지력", "자기통합성", "도덕적 책임감"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-007: 판단-행동 간극 (judgment-action gap) — 1980년 논문 핵심 문제 제기
        {
            "id": "blasi-claim-007",
            "thinker_id": THINKER_ID,
            "work_id": "blasi-bridging-moral-cognition-action",
            "source_detail": "Bridging moral cognition and moral action (1980, Psychological Bulletin)",
            "claim": (
                "도덕 판단과 도덕 행동 사이에는 인지-행동 간극(judgment-action gap)이 존재한다. "
                "1960~70년대까지의 경험적 연구들은 도덕 판단 단계가 같더라도 실제 도덕 행동은 크게 달라지며, "
                "도덕 판단만으로는 도덕 행동을 안정적으로 예측할 수 없음을 보여준다. "
                "이 간극을 메우기 위해 자아·책임 판단이라는 매개 기제가 이론적으로 요청된다."
            ),
            "original_text": "",  # Psychological Bulletin 원문 verbatim 확증 보류 — 공란 처리
            "explanation": (
                "블라시의 1980년 Psychological Bulletin 논문 'Bridging moral cognition and moral action'은 "
                "당시까지 누적된 도덕 판단-도덕 행동 상관 연구들을 체계적으로 메타 검토하여 "
                "다음을 보인다: 콜버그 척도의 도덕 판단 단계가 높은 사람이 "
                "실제 도덕 행동(부정행위 회피·이타행동 등)에서 일관되게 더 도덕적이지 않다. "
                "이 간극 문제는 이후 블라시의 자아 모델·도덕적 정체성·책임 판단 이론 전체의 출발점이 된다."
            ),
            "argument": (
                "전제1: 도덕 판단 이론(콜버그)은 판단 단계가 행동을 예측한다고 가정한다. "
                "전제2: 그러나 경험적 연구는 판단 단계와 행동 사이의 상관이 일관되지 않음을 보인다. "
                "전제3: 따라서 판단과 행동 사이에 추가 매개 기제가 필요하다. "
                "결론: 자아·책임 판단·동기화 등의 매개 변수를 포함하는 다단계 모델이 이론적으로 요청된다."
            ),
            "counterpoint": (
                "콜버그 계열에서는 이 간극이 판단 측정의 한계(DIT의 한계·인공적 딜레마 상황 등)로 설명 가능하며 "
                "판단 중심 이론의 근본 수정이 아닌 측정 방법론 보완으로 해결된다고 반론한다. "
                "밴듀라는 사회인지 이론에서 자기효능감·결과 기대·자기 제재 해제로 간극을 설명한다."
            ),
            "context": (
                "1980년 Psychological Bulletin 88(1)에 게재된 이 논문은 "
                "신콜버그주의(neo-Kohlbergian) 학풍의 출발점 중 하나로, "
                "2019-B Q8·2021-A Q6·2023-A Q10·2024-B Q5 등 "
                "블라시가 출제된 모든 임용 문항의 이론적 배경이다."
            ),
            "keywords": ["판단-행동 간극", "도덕 인지", "도덕 행동", "메타 검토", "신콜버그주의"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-008: 도덕적 욕구가 의지력·자기통합성에 미치는 영향 (2023-A Q10 작성 방법 핵심)
        {
            "id": "blasi-claim-008",
            "thinker_id": THINKER_ID,
            "work_id": "blasi-moral-functioning-2005",
            "source_detail": "Moral Functioning (2005) · 2023학년도 전공A Q10 <작성 방법>",
            "claim": (
                "도덕적 욕구(도덕적 책임감)는 "
                "의지력과 자기통합성에 도덕적 방향과 내용을 부여하는 역할을 한다. "
                "의지력과 자기통합성은 그 자체로는 형식적·기능적 능력에 그치므로 "
                "도덕적 욕구가 이들을 도덕화할 때에만 도덕적 인격의 구성 요소로 의미를 가진다."
            ),
            # 2023-A Q10 작성 방법 verbatim (coverage 2023-A.md L573 "본질은 ( ㉡ ) … 도덕적 이해에 근거한 반성을 통해 형성")
            "original_text": (
                "의지력과 자기통합성은 … 본질은 될 수 없다 … 도덕적 인격의 핵심적인 요소이자 "
                "본질은 ( ㉡ ) … 도덕적 이해에 근거한 반성을 통해 형성. "
                "— 2023학년도 전공A Q10 을(블라지) 제시문"
            ),
            "explanation": (
                "블라시의 도덕적 인격 3요소에서 의지력은 '목표 수행 능력', "
                "자기통합성은 '자기 일관성 유지 능력'이다. "
                "그러나 악인도 의지력과 자기 일관성을 발휘할 수 있으므로 "
                "이 두 요소만으로는 도덕적 인격이 성립하지 않는다. "
                "도덕적 욕구(도덕적 책임감)가 이 두 요소에 '도덕성'이라는 내용을 부여해야 "
                "의지력은 '도덕적 판단을 관철하는 의지력'이 되고, "
                "자기통합성은 '도덕적 자아와 일관된 통합성'이 된다. "
                "도덕적 욕구는 도덕적 이해에 근거한 반성을 통해 형성된다."
            ),
            "argument": (
                "전제1: 의지력과 자기통합성은 선악 중립적 기능 능력이다. "
                "전제2: 도덕적 인격이 성립하려면 이들 기능에 도덕적 방향이 부여되어야 한다. "
                "전제3: 도덕적 욕구(책임감)는 도덕적 이해에 근거한 반성을 통해 형성된 도덕적 방향성이다. "
                "결론: 도덕적 욕구가 의지력·자기통합성에 도덕적 방향과 내용을 부여함으로써 "
                "이들이 도덕적 인격의 구성 요소로 실질화된다."
            ),
            "counterpoint": (
                "의지력·자기통합성을 '독립적 도덕 덕목'으로 보는 아리스토텔레스적 덕 윤리에서는 "
                "블라시의 '형식적 능력' 규정이 지나치게 환원적이라는 비판이 가능하다. "
                "덕 윤리에서는 의지(prohairesis)가 이미 가치 지향성을 내포하는 품성적 덕이다."
            ),
            "context": (
                "2023-A Q10 <작성 방법>의 핵심 서술 요구 사항: "
                "㉡(도덕적 욕구·책임감)이 ㉢(의지력)·㉣(자기통합성)에 미치는 공통 영향을 서술하라."
            ),
            "keywords": ["도덕적 욕구", "의지력", "자기통합성", "도덕적 방향 부여", "도덕적 이해에 근거한 반성"],
            "verified": False,
            "verification_log": [],
        },
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """블라시 핵심 키워드 데이터 입력. 중복 체크 후 insert."""
    keywords = [
        {
            "id": "kw-blasi-moral-identity",
            "term": "도덕적 정체성",
            "term_en": "moral identity",
            "definition": (
                "블라시가 정의한 개념으로, 도덕적 가치를 자아의 본질과 핵심으로 여기고 "
                "그것에 전념·헌신하는 자아감. 도덕적 가치가 '나는 누구인가'라는 자아 규정의 근간이 된 상태. "
                "도덕성과 자아 정체성의 통합으로 이해되며, 자기 일관성 동기와 결합하여 "
                "도덕 판단-행동 간극을 메우는 핵심 매개 기제 역할을 한다. "
                "2017-A Q2·2021-A Q6·2023-A Q10·2024-B Q5에 반복 출제된 블라시 최대 빈출 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "blasi-self-management-of-moral-life",
            "related_terms": ["자아 모델", "자기 일관성", "책임 판단", "통합성", "도덕적 인격"],
        },
        {
            "id": "kw-blasi-self-model",
            "term": "자아 모델",
            "term_en": "self model of moral functioning",
            "definition": (
                "블라시가 1983년 'Moral cognition and moral action' 논문에서 제시한 도덕심리학 이론 틀. "
                "도덕 행위에 도달하는 과정을 '도덕적 이해 → 도덕적 정체성 → 책임 판단 → 도덕적 동기화 → 도덕 행위'의 "
                "다단계 구조로 설명한다. 도덕 판단은 행위의 필요 조건이지 충분 조건이 아니며, "
                "자아와 책임이 매개되어야 실제 도덕 행위가 산출된다는 핵심 주장. "
                "2019-B Q8·2017-A Q2의 이론적 배경."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "blasi-moral-cognition-moral-action-1983",
            "related_terms": ["도덕적 정체성", "책임 판단", "도덕적 동기화", "판단-행동 간극"],
        },
        {
            "id": "kw-blasi-responsibility-judgment",
            "term": "책임 판단",
            "term_en": "judgment of responsibility",
            "definition": (
                "블라시 자아 모델의 3번째 단계로, '이 상황의 도덕적 과제가 나의 책임 하에 있다'는 자기 귀속 판단. "
                "도덕적 정체성이 구체적 행위 상황에 적용될 때 작동하며, "
                "자기 일관성 욕구와 결합하여 도덕적 동기화를 활성화시킨다. "
                "후기 콜버그도 의무 판단(deontic judgment)과 구분되는 책임 판단 개념을 블라시와 공유한다. "
                "2017-A Q2(빈칸 정답 '책임')·2019-B Q8 ㉢·2021-A Q6에 출제."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "blasi-moral-cognition-moral-action-1983",
            "related_terms": ["자아 모델", "도덕적 정체성", "자기 일관성", "도덕적 동기화", "의무 판단"],
        },
        {
            "id": "kw-blasi-self-consistency",
            "term": "자기 일관성",
            "term_en": "self-consistency",
            "definition": (
                "블라시가 도덕 행동의 유발 기제로 제시한 동기 개념. "
                "개인이 자신의 중심 가치(도덕적 정체성)와 일치하지 않는 행동을 "
                "심리적으로 선택할 수 없게 만드는 자아 수준의 동기이다. "
                "단순한 인지적 일관성(페스팅거의 인지 부조화)이 아니라 자아의 본질·핵심에 통합된 "
                "도덕적 가치와의 일치를 지향하는 동기로, 중심 가치에 반하는 행동을 "
                "자아 해체의 위협으로 경험하게 만든다. "
                "2024-B Q5 ㉡(중심 가치와 모순되는 부정적 행동이 선택될 수 없는 이유)의 핵심 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "blasi-self-management-of-moral-life",
            "related_terms": ["도덕적 정체성", "자기통합성", "통합성", "중심 가치", "판단-행동 간극"],
        },
        {
            "id": "kw-blasi-judgment-action-gap",
            "term": "판단-행동 간극",
            "term_en": "judgment-action gap",
            "definition": (
                "블라시의 1980년 Psychological Bulletin 논문 "
                "'Bridging moral cognition and moral action'에서 체계화된 핵심 문제. "
                "도덕 판단 단계가 동일하더라도 실제 도덕 행동은 크게 달라지며, "
                "도덕 판단만으로는 도덕 행동을 안정적으로 예측할 수 없다는 경험적 관찰. "
                "이 간극을 메우기 위해 블라시는 자아 모델(도덕적 이해 → 정체성 → 책임 판단 → 동기화 → 행위)을 제안하였고, "
                "이는 신콜버그주의(neo-Kohlbergian) 학풍의 출발점이 된다."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "blasi-bridging-moral-cognition-action",
            "related_terms": ["자아 모델", "도덕적 정체성", "책임 판단", "신콜버그주의"],
        },
        {
            "id": "kw-blasi-moral-character-three",
            "term": "도덕적 인격 3요소",
            "term_en": "three components of moral character",
            "definition": (
                "블라시 『Moral Functioning』(2005)에서 제시한 도덕적 인격의 구조. "
                "① 도덕적 욕구(moral desires / 도덕적 책임감) + ② 의지력(willpower) + ③ 자기통합성(self-integration). "
                "의지력과 자기통합성은 그 자체로는 선악 중립적 형식 능력이므로, "
                "도덕적 욕구·책임감이 이들에 도덕적 방향과 내용을 부여해야 "
                "도덕적 인격의 구성 요소로 기능한다. "
                "도덕적 욕구는 도덕적 이해에 근거한 반성을 통해 형성된다. "
                "2023-A Q10 을·2024-B Q5 갑에 직접 출제."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "blasi-moral-functioning-2005",
            "related_terms": ["도덕적 욕구", "의지력", "자기통합성", "통합성", "도덕적 정체성"],
        },
        {
            "id": "kw-blasi-integrity",
            "term": "통합성",
            "term_en": "integrity",
            "definition": (
                "블라시 도덕적 인격 3요소 중 '자기통합성'이 가장 높은 수준에 이르렀을 때의 형태. "
                "개인이 선택한 신념과 자아감을 구성하는 구체적 신념들의 일치를 유지하려는 동기로, "
                "가장 높은 수준의 통합성은 도덕적 정체성과 본질적으로 연관된다. "
                "중심 가치와 모순되는 부정적 행동을 심리적으로 선택할 수 없게 만드는 기반이 되며, "
                "2024학년도 전공B Q5 ㉠ 정답으로 출제되었다."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "blasi-moral-functioning-2005",
            "related_terms": ["자기통합성", "도덕적 정체성", "자기 일관성", "도덕적 인격 3요소"],
        },
        {
            "id": "kw-blasi-moral-desires",
            "term": "도덕적 욕구",
            "term_en": "moral desires",
            "definition": (
                "블라시 도덕적 인격 3요소의 본질 요소. "
                "도덕적 가치를 실현하려는 근본 동기·헌신·책임감으로, 도덕적 책임감(moral responsibility)으로도 불린다. "
                "도덕적 이해에 근거한 반성을 통해 형성되며, "
                "그 자체로 선악 중립적 형식 능력인 의지력과 자기통합성에 도덕적 방향과 내용을 부여함으로써 "
                "이 두 요소를 도덕적 인격의 구성 요소로 실질화한다. "
                "2023학년도 전공A Q10 을 ㉡ 정답 후보."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "blasi-moral-functioning-2005",
            "related_terms": ["도덕적 책임감", "의지력", "자기통합성", "도덕적 이해에 근거한 반성"],
        },
        {
            "id": "kw-blasi-neo-kohlbergian",
            "term": "신콜버그주의",
            "term_en": "neo-Kohlbergian",
            "definition": (
                "콜버그의 인지발달적 도덕심리학을 계승하면서 한계를 보완하는 연구 프로그램. "
                "대표적 학자로 블라시(도덕적 정체성·자아 모델)·레스트(4구성요소 모델·DIT)·Lapsley·Narvaez 등이 있다. "
                "콜버그가 도덕 판단 중심으로 설명한 도덕성을 "
                "자아·정체성·책임·동기·행동 차원까지 확장하여 "
                "판단-행동 간극을 메우려는 공통 문제의식을 가진다."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "blasi-bridging-moral-cognition-action",
            "related_terms": ["콜버그 계승", "레스트 4요소", "판단-행동 간극", "자아 모델", "도덕적 정체성"],
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
    """블라시 영향·비교 관계 데이터 입력.

    ES 등록 확인된 thinker_id만 링크한다 (본 세션 2026-04-22 curl 확인):
    - kohlberg (로렌스 콜버그) : 등록됨 — 인지발달적 도덕심리학 계승 + 후기 책임 판단 공유
    - piaget (장 피아제) : 등록됨 — 인지발달 전통 계승
    - rest (제임스 레스트) : 등록됨 — 신콜버그주의 동료 + 4구성요소 모델 대비
    - gilligan (캐롤 길리건) : 등록됨 — 동시대 도덕발달 이론가, 콜버그 비판 축은 다름
    ※ Lapsley·Narvaez·Power·Hoffman 등은 ES 미등록이므로 관계 생략.
    """
    relations = [
        {
            "from_thinker": "kohlberg",
            "to_thinker": THINKER_ID,
            "type": "influenced",
            "description": (
                "콜버그의 인지발달적 도덕심리학과 도덕 판단 3수준 6단계 이론은 "
                "블라시의 이론적 출발점이다. 블라시는 콜버그의 도덕 판단 이론이 도덕 행동을 충분히 "
                "설명하지 못하는 판단-행동 간극 문제를 확인하며, 자아 모델로 이를 보완하였다. "
                "후기 콜버그는 의무 판단(deontic)과 책임 판단(responsibility)을 구분하며 블라시의 "
                "책임 판단 개념을 수용하였고, 2021학년도 전공A Q6은 이 공유 구조(갑 블라시·을 후기 콜버그)를 출제하였다."
            ),
            "evidence": (
                "Blasi (1980) Psychological Bulletin; "
                "Kohlberg (1984) Essays on Moral Development Vol.2의 책임 판단 논의; "
                "2021학년도 전공A Q6 갑·을 배치"
            ),
        },
        {
            "from_thinker": "piaget",
            "to_thinker": THINKER_ID,
            "type": "influenced",
            "description": (
                "피아제의 인지발달론·자율적 도덕성 이론은 "
                "콜버그를 매개로 블라시의 도덕심리학 전통의 근원을 이룬다. "
                "블라시는 피아제-콜버그의 인지발달 계보에서 인지(판단)뿐 아니라 "
                "자아·정체성·책임 판단의 차원을 추가로 발전시켰다."
            ),
            "evidence": (
                "피아제 『아동의 도덕 판단』(1932) → 콜버그 3수준 6단계 → "
                "블라시 자아 모델·도덕적 정체성으로 이어지는 인지발달-신콜버그주의 계보"
            ),
        },
        {
            "from_thinker": "rest",
            "to_thinker": THINKER_ID,
            "type": "compared",
            "description": (
                "레스트의 4구성요소 모델(도덕적 민감성·판단력·동기화·품성/실행력)과 "
                "블라시의 자아 모델(도덕적 이해·정체성·책임 판단·동기화)은 "
                "공히 신콜버그주의(neo-Kohlbergian) 계열로, "
                "판단-행동 간극을 메우는 다원적 구조를 제시한다는 공통점을 가지나, "
                "강조점이 인지·행동 구성요소(레스트) vs 자아·정체성 구조(블라시)로 갈린다. "
                "2019학년도 전공B Q8·2023학년도 전공A Q10은 두 이론가를 "
                "4요소 대 3요소로 대립적으로 배치하여 출제하였다."
            ),
            "evidence": (
                "Rest (1986) Moral Development; Blasi (2005) Moral Functioning; "
                "2019학년도 전공B Q8 제시문 (레스트·블라지 4요소 병치); "
                "2023학년도 전공A Q10 (갑 레스트 4요소 ㉠ / 을 블라지 3요소 ㉡)"
            ),
        },
        {
            "from_thinker": "kohlberg",
            "to_thinker": THINKER_ID,
            "type": "criticized",
            "description": (
                "블라시는 1980년 Psychological Bulletin 논문에서 "
                "콜버그식 도덕 판단 중심 이론이 판단-행동 간극(judgment-action gap)을 "
                "충분히 설명하지 못함을 메타 검토로 보이며, "
                "자아·정체성·책임이라는 추가 매개 기제의 필요성을 논증하였다. "
                "이 비판은 신콜버그주의(neo-Kohlbergian) 학풍의 출발점이 된다."
            ),
            "evidence": (
                "Blasi, A. (1980). 'Bridging moral cognition and moral action: A critical review of the literature.' "
                "Psychological Bulletin 88(1)"
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
    print("=== 아우구스토 블라시(Blasi) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (blasi)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n[OK] 블라시 데이터 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}", file=sys.stderr)
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
