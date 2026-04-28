"""에밀 뒤르켐(Émile Durkheim) 데이터를 ES에 직접 입력하는 스크립트.

Task: TASK-176-03
출제 5회 (2015-B 논술1 / 2021-B Q4 / 2022-B Q3 / 2024-B Q4 / 2025-A Q5).
moral_development 분야. kohlberg·gilligan·blasi 선례 답습.
원문 인용 규칙(agents/coder.md §원문/입력 인용 규칙) 엄수:
 - claims.original_text 는 coverage md 실측 원문(verbatim) 또는 빈 문자열("").
 - 모든 프랑스어·한자·trademark는 coverage md 역grep으로 0건이면 제거.
자기검증 (coverage grep 대상 파일: 2015-B·2021-B·2022-B·2024-B·2025-A.md):
 - L'Éducation morale: 2021-B·2022-B·2024-B·2025-A 히트 확인
 - esprit de discipline: 2021-B·2022-B·2024-B 히트 확인
 - attachement aux groupes sociaux: 2021-B·2024-B 히트 확인
 - autonomie de la volonté: 2021-B·2024-B 히트 확인
 - conscience collective: 2021-B·2022-B 히트 확인
 - fait social: 2021-B·2022-B 히트 확인
 - Le Suicide: 2021-B 히트 확인
 - Les Formes élémentaires: 2021-B 히트 확인
 - anomie: 2021-B·2024-B·2025-A 히트 확인
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


THINKER_ID = "durkheim"


def ensure_field(client):
    """moral_development 분야 존재 확인 — kohlberg에서 이미 생성되었으므로 존재만 검증."""
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
                "길리건의 배려윤리, 블라시의 도덕적 정체성 이론, "
                "뒤르켐의 사회학적 도덕교육론(도덕성 3요소) 등을 포함한다. "
                "도덕심리학·도덕교육론·도덕사회학과 밀접하게 연관되며 임용시험 핵심 영역이다."
            ),
            "order": 4,
        }
        result = client.index(index=INDEX_FIELDS, id="moral_development", document=doc)
        print(f"[field] moral_development: {result['result']}")


def insert_thinker(client):
    """뒤르켐 사상가 데이터 입력."""
    doc = {
        "id": THINKER_ID,
        "name": "에밀 뒤르켐 (Émile Durkheim)",
        "name_en": "Émile Durkheim",
        "field": "moral_development",
        "era": "근대",
        "birth_year": 1858,
        "death_year": 1917,
        "background": (
            "프랑스의 사회학자. 프랑스 사회학의 창시자이자 현대 사회학의 정초자 중 한 사람으로 평가된다. "
            "도덕을 개인 이성이나 신적 권위가 아니라 사회적 사실(fait social)로 규정함으로써 "
            "도덕을 사회학적 연구 대상으로 확립하였고, "
            "도덕 교육을 '비사회적 존재를 사회적 존재로 만드는 사회화(socialisation) 과정'으로 정의하여 "
            "근대 도덕 교육론에 결정적 영향을 미쳤다. "
            "1902~03년에 진행한 도덕 교육 강의는 사후(1925)에 "
            "『L'Éducation morale(도덕교육론)』으로 출간되어, "
            "뒤르켐 도덕교육론의 trademark인 '도덕성 3요소'(규율 정신 · 집단에의 애착 · 의지의 자율성)를 전파하였다."
        ),
        "core_philosophy": (
            "뒤르켐 도덕사상의 핵심은 도덕을 사회적 사실(fait social)로 규정하고, "
            "도덕 교육의 목적을 아동을 사회의 도덕 질서에 통합시키는 사회화(socialisation)로 정의하는 데 있다. "
            "그는 신에 의해 부여되는 절대적 도덕과 결별하고, "
            "각각의 사회가 도덕의 기반이 되므로 사회학적 연구를 통해 각 사회가 이상으로 하는 도덕을 찾아내야 한다고 본다. "
            "도덕성은 세 가지 요소로 구성된다: "
            "① 규율 정신(esprit de discipline) — 규칙성에 대한 선호와 권위(authority)에 대한 존중, "
            "② 집단에의 애착(attachement aux groupes sociaux) — 개인이 속한 사회 집단의 이익·가치에 정서적으로 결속, "
            "③ 의지의 자율성(autonomie de la volonté) — 사회의 도덕 규칙이 왜 그러한지에 대한 "
            "과학적·이성적 이해에 기초해 규칙을 자발적으로 수용하는 능력. "
            "뒤르켐의 자율성은 칸트적 순수 이성의 자기 입법이 아니라, "
            "사회 규범의 근거·기능을 합리적으로 통찰하고 자유롭게 자기 것으로 삼는 태도이다."
        ),
        "philosophical_journey": (
            "초기(『사회분업론』, 1893): "
            "도덕적 연대의 두 형태 — 유사성에 기초한 기계적 연대(solidarité mécanique)와 "
            "분업에 기초한 유기적 연대(solidarité organique) — 를 구분하고, "
            "근대 사회에서 도덕 규범이 붕괴되는 아노미(anomie) 문제를 제기. "
            "중기(『자살론(Le Suicide)』, 1897): "
            "사회 통합과 규범이 약화된 상태에서 발생하는 아노미적 자살을 분석하며 "
            "개인 심리를 넘어 사회적 사실(fait social)로서의 도덕·규범을 실증적으로 규명. "
            "1902~03년 도덕 교육 강의: "
            "도덕성 3요소(규율 정신·집단에의 애착·의지의 자율성) 체계를 세우고, "
            "도덕 교육을 '비사회적 존재를 사회적 존재로 만드는 과정'으로 정의. "
            "이 강의는 사후 『L'Éducation morale(도덕교육론)』(1925)으로 출간. "
            "후기(『종교생활의 원초적 형태(Les Formes élémentaires de la vie religieuse)』, 1912): "
            "도덕의 사회학적 기원을 종교·의례에서 형성되는 집합 의식(conscience collective)에서 찾는 연구를 수행."
        ),
        "keywords": [
            "도덕성 3요소",
            "규율 정신",
            "집단에의 애착",
            "의지의 자율성",
            "사회화",
            "사회적 사실",
            "도덕교육론",
            "세속적 도덕",
            "집합 의식",
            "아노미",
        ],
    }
    result = client.index(index=INDEX_THINKERS, id=THINKER_ID, document=doc)
    print(f"[thinker] {THINKER_ID}: {result['result']}")
    return result


def insert_works(client):
    """뒤르켐 주요 저서 데이터 입력 (4종)."""
    works = [
        {
            "id": "durkheim-education-morale",
            "thinker_id": THINKER_ID,
            "title": "도덕교육론",
            "title_original": "L'Éducation morale",
            "year": 1925,
            "significance": (
                "뒤르켐이 1902~03년에 진행한 도덕 교육 강의록을 "
                "1925년 사후에 출간한 유작. "
                "뒤르켐 도덕교육론 전체를 집약한 대표 저작으로, "
                "도덕 교육을 '비사회적 존재를 사회적 존재로 만드는 과정'(사회화)으로 정의하고, "
                "도덕성 3요소(규율 정신·집단에의 애착·의지의 자율성)의 체계를 제시한다. "
                "한국 윤리 임용시험에서 출제된 뒤르켐 trademark "
                "(2015-B 논술1 갑 · 2021-B Q4 갑 · 2022-B Q3 갑 · 2024-B Q4 (가) · 2025-A Q5)의 "
                "이론적 배경이 되는 저작이다."
            ),
            "key_concepts": [
                "도덕성 3요소",
                "규율 정신",
                "집단에의 애착",
                "의지의 자율성",
                "사회화",
                "세속적 도덕",
            ],
        },
        {
            "id": "durkheim-suicide",
            "thinker_id": THINKER_ID,
            "title": "자살론",
            "title_original": "Le Suicide",
            "year": 1897,
            "significance": (
                "뒤르켐이 자살률이라는 명백히 개인적·심리적 현상으로 보이는 사건을 "
                "사회 통합·규범의 정도에 따라 체계적으로 변하는 사회적 사실(fait social)임을 "
                "실증적 자료로 논증한 저작. "
                "이기적 자살·이타적 자살·아노미적 자살·숙명적 자살의 4유형 분류를 통해 "
                "근대 사회의 규범 붕괴(아노미)가 도덕적 통합의 붕괴와 결부됨을 보이며, "
                "개인을 넘어선 사회적 도덕 규범의 실재성을 이론적으로 확립하였다."
            ),
            "key_concepts": [
                "아노미",
                "사회적 사실",
                "사회 통합",
                "집합 의식",
            ],
        },
        {
            "id": "durkheim-division-of-labor",
            "thinker_id": THINKER_ID,
            "title": "사회분업론",
            "title_original": "",
            "year": 1893,
            "significance": (
                "뒤르켐의 박사 학위 논문이자 그의 사회학적 도덕 이론의 출발점. "
                "전통 사회의 도덕적 연대를 유사성에 기초한 기계적 연대(solidarité mécanique)로, "
                "근대 사회의 도덕적 연대를 분업과 상호의존에 기초한 유기적 연대(solidarité organique)로 구분하고, "
                "분업의 병리적 형태로 아노미(anomie)적 분업을 제시하여 "
                "근대 사회에서 도덕 규범이 붕괴되는 문제를 처음 정식화하였다."
            ),
            "key_concepts": [
                "기계적 연대",
                "유기적 연대",
                "아노미",
                "집합 의식",
            ],
        },
        {
            "id": "durkheim-elementary-forms",
            "thinker_id": THINKER_ID,
            "title": "종교생활의 원초적 형태",
            "title_original": "Les Formes élémentaires de la vie religieuse",
            "year": 1912,
            "significance": (
                "뒤르켐 만년의 대표작. "
                "도덕·규범의 사회학적 기원을 종교·의례를 통한 "
                "집합 의식(conscience collective) 형성 과정에서 찾음으로써, "
                "뒤르켐의 '도덕은 사회적 사실(fait social)'이라는 테제를 "
                "종교사회학 영역까지 확장한 저작이다."
            ),
            "key_concepts": [
                "집합 의식",
                "종교사회학",
                "사회적 사실",
            ],
        },
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """뒤르켐 핵심 주장 데이터 입력 (8개).

    original_text는 coverage md 실측 verbatim 원문만 기입.
    확증 불가 구절은 빈 문자열("")로 남기고 explanation에 해설만 둔다.
    """
    claims = [
        # CLAIM-001: 도덕교육 = 사회화 (2015-B 논술1, 2021-B Q4)
        {
            "id": "durkheim-claim-001",
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-education-morale",
            "source_detail": "L'Éducation morale (1925) · 2015학년도 전공B 논술1 갑 · 2021학년도 전공B Q4 갑",
            "claim": (
                "도덕 교육은 비사회적인 존재를 사회적인 존재로 만드는 과정(사회화)이다. "
                "뒤르켐에게 도덕의 기반은 사회이므로, 도덕 교육의 목적은 "
                "아동을 사회의 도덕 질서에 통합시키는 사회화(socialisation)이며, "
                "이 과정은 개인주의 교육관(루소·칸트)이 아닌 사회학적 관점에 선다."
            ),
            # 2015-B L19 verbatim + 2021-B L18 verbatim 병기
            "original_text": (
                "갑: 도덕 교육은 비사회적인 존재를 사회적인 존재로 만드는 과정이다. "
                "… 신에 의해 부여되는 절대적인 도덕과 결별해야 한다. "
                "각각의 사회가 도덕의 기반이 되므로 사회학적 연구를 통해 "
                "각 사회가 이상으로 하는 도덕을 찾아내고, "
                "도덕성의 3가지 요소인 규율 정신, 집단에의 애착, 자율성을 키워 "
                "사회 구성원들의 도덕성이 형성되도록 해야 한다. "
                "— 2015학년도 전공B 논술1 갑(뒤르켐) 제시문 / "
                "갑: 도덕 교육의 목적은 학생들을 도덕적으로 사회화하는 것이다. "
                "— 2021학년도 전공B Q4 갑(뒤르켐) 제시문"
            ),
            "explanation": (
                "뒤르켐은 도덕 교육을 개인 이성의 자기 계발이나 신적 계명의 내면화가 아니라, "
                "아동을 사회의 도덕 질서에 통합시키는 사회화(socialisation)로 정의한다. "
                "이는 도덕을 개인 외부에 실재하는 사회적 사실(fait social)로 규정하는 "
                "뒤르켐 사회학 전체의 기본 전제와 일치한다. "
                "2015-B 논술1과 2021-B Q4는 이 '도덕 교육=사회화' trademark 명제를 "
                "갑 제시문 첫 문장으로 직접 인용한다."
            ),
            "argument": (
                "전제1: 도덕은 개인이 창출하는 것이 아니라 사회가 공유하는 규범 체계이다. "
                "전제2: 아동은 태어날 때 비사회적 존재이며 사회 규범을 갖지 않는다. "
                "전제3: 도덕 교육은 아동에게 사회의 규범을 내면화시키는 과정이어야 한다. "
                "결론: 따라서 도덕 교육은 비사회적 존재를 사회적 존재로 만드는 "
                "사회화(socialisation)의 과정이다."
            ),
            "counterpoint": (
                "피아제는 도덕 교육을 성인 사회 규칙의 일방적 내면화가 아니라 "
                "또래 간 상호 협력·상호 존중을 통한 자율적 도덕성의 구성 과정으로 본다. "
                "2015-B 논술1 을(피아제) 제시문의 "
                "'아동은 성인 사회 규칙보다 아동 상호 간 사회의 규칙을 더 잘 따른다'는 "
                "뒤르켐의 사회화 중심 모델에 대한 직접 비판이다."
            ),
            "context": (
                "2015-B 논술1(10점) 갑과 2021-B Q4 갑 제시문의 핵심 "
                "뒤르켐 trademark 명제. "
                "피아제(을)·콜버그(병)와 대비하여 '사회학적 도덕교육'의 입장을 대변."
            ),
            "keywords": ["도덕교육", "사회화", "비사회적 존재", "사회적 사실", "사회학적 도덕관"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-002: 도덕성 3요소 (2015-B, 2024-B, 2025-A)
        {
            "id": "durkheim-claim-002",
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-education-morale",
            "source_detail": "L'Éducation morale (1925) · 2015학년도 전공B 논술1 갑 · 2024학년도 전공B Q4 (가) · 2025학년도 전공A Q5",
            "claim": (
                "도덕성은 세 가지 요소로 구성된다: "
                "① 규율 정신(esprit de discipline), "
                "② 집단에의 애착(attachement aux groupes sociaux), "
                "③ 의지의 자율성(autonomie de la volonté). "
                "이 세 요소가 함께 갖추어질 때 완전한 도덕성이 형성된다."
            ),
            # 2015-B L19 + 2024-B L157 + 2025-A L193 verbatim
            "original_text": (
                "도덕성의 3가지 요소인 규율 정신, 집단에의 애착, 자율성을 키워 "
                "사회 구성원들의 도덕성이 형성되도록 해야 한다. "
                "— 2015학년도 전공B 논술1 갑(뒤르켐) / "
                "도덕성의 구성요소는 규율정신, 집단에 대한 애착, ㉡ 자율성 "
                "— 2024학년도 전공B Q4 (가) / "
                "도덕성 3요소인 규율 정신, ( ㉡ ), ㉢ 자율성 "
                "— 2025학년도 전공A Q5 (나)"
            ),
            "explanation": (
                "뒤르켐은 『L'Éducation morale(도덕교육론)』에서 "
                "도덕성(moralité)을 세 요소로 분석한다. "
                "① 규율 정신(esprit de discipline): 규칙성에 대한 선호와 권위에 대한 존중. "
                "② 집단에의 애착(attachement aux groupes sociaux): 개인이 속한 사회 집단의 "
                "이익·가치·목적에 정서적으로 결속되는 성향. "
                "③ 의지의 자율성(autonomie de la volonté): 사회의 도덕 규칙의 근거를 "
                "이성적으로 이해하고 자발적으로 수용하는 능력. "
                "앞의 두 요소만으로는 불충분하며 제3요소 자율성이 완성되어야 진정한 도덕성이다 "
                "(2021-B Q4 갑 제시문 '규율을 존중하고 집단에 헌신하는 것만으로는 충분하지 않다')."
            ),
            "argument": (
                "전제1: 도덕은 규칙 준수(규율)·집단 결속(애착)·이성적 승인(자율)의 세 측면을 가진다. "
                "전제2: 규율 정신만 있으면 맹목적 복종, 집단 애착만 있으면 집단주의·맹목적 충성이 된다. "
                "전제3: 자율성이 결여된 규율·애착은 외적 강제에 머물러 진정한 도덕성이 되지 못한다. "
                "결론: 따라서 도덕성은 규율 정신·집단에의 애착·의지의 자율성 세 요소가 "
                "함께 발달할 때 완성된다."
            ),
            "counterpoint": (
                "콜버그는 도덕성의 본질을 사회 규범의 수용이 아니라 보편적 도덕 원리(정의)에 근거한 "
                "자율적 추론 능력으로 본다. 따라서 뒤르켐의 '집단에의 애착'은 "
                "인습 4단계의 '법과 질서 지향'에 머무르는 것으로 비판받는다 "
                "(2015-B 논술1 병의 '4단계 한계' 비판)."
            ),
            "context": (
                "2015-B 논술1 갑 · 2024-B Q4 (가) · 2025-A Q5 (나)에 세 번 모두 "
                "'규율 정신·집단에의 애착·자율성'의 3요소가 동일 구조로 출제된 "
                "뒤르켐 최대 빈출 trademark."
            ),
            "keywords": ["도덕성 3요소", "규율 정신", "집단에의 애착", "의지의 자율성", "도덕교육론"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-003: 규율 정신 — 권위 존중과 규칙성 선호 (2022-B, 2024-B)
        {
            "id": "durkheim-claim-003",
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-education-morale",
            "source_detail": "L'Éducation morale (1925) · 2022학년도 전공B Q3 갑 · 2024학년도 전공B Q4 (가)",
            "claim": (
                "규율 정신(esprit de discipline)은 뒤르켐 도덕성 3요소의 첫 번째 요소로, "
                "도덕 규칙을 일관성 있게 준수하는 행위자의 성향인 규칙성에 대한 선호와 "
                "권위(authority)에 대한 존중이다. "
                "도덕 규칙은 개인에게 외적·선행적·강제적 권위로 작용하며, "
                "이 권위에 대한 존중이 도덕적 주체 형성의 첫 단계이다."
            ),
            # 2024-B L158 verbatim
            "original_text": (
                "규율정신은 도덕 규칙을 일관성 있게 준수하는 행위자의 성향인 "
                "규칙성에 대한 선호와 ( ㉢ )에 대한 존중 "
                "— 2024학년도 전공B Q4 (가) 뒤르켐 제시문"
            ),
            "explanation": (
                "규율 정신은 두 측면을 가진다: "
                "① 규칙성(régularité)에 대한 선호 — 도덕 규칙을 일관되고 반복적으로 준수하려는 성향, "
                "② 권위(autorité)에 대한 존중 — 규칙이 지닌 외적·선행적 권위를 존경하는 태도. "
                "2022-B Q3에서는 이 권위가 빈칸 ㉠으로 출제되었고, "
                "교사는 '규율과 금지의 대변자, 본보기'로서 규칙의 권위를 학생에게 내면화시키는 역할을 한다. "
                "2024-B Q4에서도 같은 '권위'가 빈칸 ㉢으로 재출제되었다."
            ),
            "argument": (
                "전제1: 도덕 규칙은 개인 외부에 존재하는 사회적 사실(fait social)이다. "
                "전제2: 개인은 이 외적 규칙을 권위 있는 명령으로 경험한다. "
                "전제3: 도덕 교육은 규칙 자체가 가진 권위를 학생이 존경하도록 만드는 과정이다. "
                "결론: 규율 정신은 규칙성에 대한 선호 + 권위에 대한 존중의 이중 구조로 정의된다."
            ),
            "counterpoint": (
                "피아제는 도덕 규칙이 외적 권위에서 오는 것이 아니라 "
                "아동 간 상호 협력·합의를 통해 구성되는 것이라고 본다. "
                "2022-B Q3 을(피아제) 제시문의 '부모의 지나친 권위의 부재'가 자율적 도덕성 발달의 조건이라는 "
                "대립적 입장이 바로 이 지점을 겨눈다."
            ),
            "context": (
                "2022-B Q3 갑 제시문의 ㉠(권위)·㉡(벌) 빈칸 핵심 개념. "
                "2024-B Q4 (가)에서도 ㉢(권위)가 빈칸으로 재출제됨."
            ),
            "keywords": ["규율 정신", "권위", "규칙성", "도덕적 사회화", "사회적 사실"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-004: 집단에의 애착 (2025-A Q5 ㉡)
        {
            "id": "durkheim-claim-004",
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-education-morale",
            "source_detail": "L'Éducation morale (1925) · 2025학년도 전공A Q5 (나) ㉡ · 2024학년도 전공B Q4",
            "claim": (
                "집단에의 애착(attachement aux groupes sociaux)은 뒤르켐 도덕성 3요소의 두 번째 요소로, "
                "개인이 속한 사회 집단의 이익·가치·목적에 정서적으로 결속되어 "
                "집단의 관점에서 행동하려는 성향이다. "
                "집단 속에서 자신의 도덕적 존재를 발견·실현하게 된다."
            ),
            # 2025-A L193 + 2024-B L157 verbatim
            "original_text": (
                "도덕성 3요소인 규율 정신, ( ㉡ ), ㉢ 자율성 "
                "— 2025학년도 전공A Q5 (나) / "
                "도덕성의 구성요소는 규율정신, 집단에 대한 애착, ㉡ 자율성 "
                "— 2024학년도 전공B Q4 (가)"
            ),
            "explanation": (
                "뒤르켐은 '집단 애착은 사회 집단의 이익이라는 관점에서 행동'하는 성향으로 규정한다. "
                "이는 이기적 개인주의와 대립되며, 규율 정신이 규칙의 형식적 권위를 존중하는 것이라면 "
                "집단에의 애착은 규칙이 봉사하는 집단의 실질적 가치·이익에 정서적으로 결속하는 것이다. "
                "2025-A Q5의 빈칸 ㉡ 정답이 바로 이 '집단에 대한 애착'이며, "
                "2024-B Q4에서는 역으로 3요소 구조에서 ㉡(자율성)에 대비되는 축으로 명시되었다."
            ),
            "argument": (
                "전제1: 도덕은 개인이 속한 사회 집단의 공유된 가치 체계이다. "
                "전제2: 집단에 대한 형식적 규칙 준수(규율 정신)만으로는 도덕적 헌신이 이루어지지 않는다. "
                "전제3: 집단의 이익·가치에 정서적으로 결속되어야 도덕 규칙이 내적으로 수용된다. "
                "결론: 따라서 집단에의 애착은 도덕성의 두 번째 구성 요소로서 "
                "규율 정신과 자율성 사이의 정서적·헌신적 축을 담당한다."
            ),
            "counterpoint": (
                "콜버그는 집단에의 애착을 인습 3~4단계에 고착된 도덕성으로 진단하고, "
                "보편적 정의 원리(후인습 5~6단계)가 특정 집단의 이익을 초월해야 한다고 본다."
            ),
            "context": (
                "2025-A Q5 (나) 빈칸 ㉡의 정답 및 "
                "2024-B Q4 (가) 3요소 구조 내 중간 요소로 반복 출제."
            ),
            "keywords": ["집단에의 애착", "도덕성 3요소", "집단의 이익", "사회 집단", "정서적 결속"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-005: 의지의 자율성 — 이성적 이해에 기초한 자발적 수용 (2021-B Q4 ㉠, 2025-A)
        {
            "id": "durkheim-claim-005",
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-education-morale",
            "source_detail": "L'Éducation morale (1925) · 2021학년도 전공B Q4 갑 ㉠ · 2025학년도 전공A Q5 (나) ㉢",
            "claim": (
                "의지의 자율성(autonomie de la volonté)은 뒤르켐 도덕성 3요소의 세 번째 요소로, "
                "도덕 규칙을 지적으로 이해하고 그것을 따르기로 동의하고 원함으로써 "
                "행위의 자율성을 확보하는 능력이다. "
                "칸트적 순수 이성의 자기 입법이 아니라, "
                "사회 도덕규범의 근거를 과학적·이성적으로 이해하여 자발적으로 수용하는 태도이다."
            ),
            # 2021-B L18 verbatim
            "original_text": (
                "우리는 도덕 규칙을 지적으로 이해하고 그것을 따르기로 동의하고 원함으로써 "
                "행위의 ( ㉠ )을/를 확보하게 된다. "
                "— 2021학년도 전공B Q4 갑(뒤르켐) 제시문"
            ),
            "explanation": (
                "뒤르켐의 자율성 개념은 칸트의 자율(순수실천이성의 자기 입법)과 구별된다. "
                "칸트적 자율이 사회로부터 독립된 순수 이성의 자기 규제라면, "
                "뒤르켐의 자율은 사회 규칙의 합리성·필연성·기능을 과학적으로 이해한 위에서 "
                "규칙을 자기 것으로 삼는 계몽된 의식이다. "
                "2025-A Q5 작성 방법에서 '㉢ 자율성을 가진 사람이 하는 도덕적 행동의 특징을 "
                "〈사회의 도덕규범〉을 사용하여 서술하라'는 요구는 "
                "자율성이 사회 규범과 대립하는 것이 아니라 사회 규범을 이성적으로 이해·수용하는 "
                "자발적 실천임을 평가한다."
            ),
            "argument": (
                "전제1: 도덕 규칙은 외적 강제로서 부과되면 맹목적 복종에 머문다. "
                "전제2: 개인이 규칙의 사회학적 근거를 이성적으로 이해하면 규칙을 내적으로 승인할 수 있다. "
                "전제3: 이성적 이해에 따른 자발적 수용이 진정한 도덕적 자율이다. "
                "결론: 따라서 의지의 자율성은 사회 규칙과 양립하며, "
                "규율 정신·집단 애착을 완성시키는 3요소의 최종 단계이다."
            ),
            "counterpoint": (
                "칸트주의자는 뒤르켐의 자율성이 결국 사회가 부과하는 규범에 대한 "
                "'계몽된 복종'에 머무르므로, 진정한 자율(순수 이성의 자기 입법)이 아니라 "
                "타율의 변형이라고 비판한다. 피아제 역시 자율성의 기반을 사회 전체의 규범 이해가 아니라 "
                "또래 간 상호성·협력에서 찾는다는 점에서 대립한다."
            ),
            "context": (
                "2021-B Q4 갑 ㉠ 정답(자율성)의 이론적 근거. "
                "2025-A Q5 (나) 작성 방법 ③의 핵심 서술 대상."
            ),
            "keywords": ["의지의 자율성", "이성적 이해", "자발적 수용", "사회의 도덕규범", "계몽된 의식"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-006: 세속적 도덕 — 신과 결별한 사회학적 도덕 (2015-B 논술1)
        {
            "id": "durkheim-claim-006",
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-education-morale",
            "source_detail": "L'Éducation morale (1925) · 2015학년도 전공B 논술1 갑",
            "claim": (
                "도덕은 신에 의해 부여되는 절대적인 도덕과 결별해야 한다. "
                "각각의 사회가 도덕의 기반이 되므로 사회학적 연구를 통해 "
                "각 사회가 이상으로 하는 도덕을 찾아내야 한다. "
                "이것이 뒤르켐이 세운 세속적·사회학적 도덕관이다."
            ),
            # 2015-B L19 verbatim
            "original_text": (
                "신에 의해 부여되는 절대적인 도덕과 결별해야 한다. "
                "각각의 사회가 도덕의 기반이 되므로 사회학적 연구를 통해 "
                "각 사회가 이상으로 하는 도덕을 찾아내고 … "
                "— 2015학년도 전공B 논술1 갑(뒤르켐) 제시문"
            ),
            "explanation": (
                "뒤르켐은 종교가 지배하던 전통 도덕관을 거부하고, "
                "도덕의 기반을 신이 아니라 사회(société)로 재설정한다. "
                "절대적·초월적 도덕 기준은 더 이상 성립하지 않으며, "
                "각 사회가 자신의 조건에 맞는 도덕을 이상으로 삼는다. "
                "따라서 도덕 연구는 신학이 아니라 사회학의 과제가 된다. "
                "이는 뒤르켐 도덕교육론이 근대 세속 교육의 이론적 토대로 평가되는 근거이다."
            ),
            "argument": (
                "전제1: 전통 도덕은 신의 절대적 명령으로 정당화되어 왔다. "
                "전제2: 근대 사회는 과학적 세계관으로 이행하면서 신 중심 도덕관이 설득력을 잃었다. "
                "전제3: 그러나 도덕이 사라진 것이 아니라 도덕의 실제 기반이 사회라는 사실이 드러난다. "
                "결론: 따라서 도덕 연구·도덕 교육은 신학이 아닌 "
                "사회학적 연구를 통해 각 사회의 도덕 이상을 찾아내는 방식으로 수행되어야 한다."
            ),
            "counterpoint": (
                "전통 종교 윤리 및 칸트의 초월적 윤리는 "
                "도덕의 보편성·무조건적 구속력이 신 또는 순수 이성에서만 확보될 수 있다고 반론한다. "
                "뒤르켐의 사회학적 도덕관은 각 사회의 도덕을 상대화하므로 "
                "도덕의 보편적 구속력이 약해진다는 비판을 받는다."
            ),
            "context": (
                "2015-B 논술1 갑(뒤르켐) 제시문 두 번째 문장의 핵심 명제. "
                "'세속적·사회학적 도덕'이라는 뒤르켐의 트레이드마크 입장을 직접 인용."
            ),
            "keywords": ["세속적 도덕", "사회학적 도덕관", "신과의 결별", "사회가 도덕의 기반"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-007: 벌의 사회학적 기능 (2022-B Q3 ㉡)
        {
            "id": "durkheim-claim-007",
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-education-morale",
            "source_detail": "L'Éducation morale (1925) · 2022학년도 전공B Q3 갑 ㉡",
            "claim": (
                "벌은 단순히 위반자에게 고통을 주거나 잘못을 억제하기 위한 수단이 아니라, "
                "위반된 도덕규칙의 권위와 신성성을 재확립하고 "
                "집단의 도덕적 질서·집단 양심(conscience collective)을 회복하는 "
                "상징적·사회적 기능을 수행한다."
            ),
            # 2022-B Q3 제시문에서 "벌을 적절하게 사용" verbatim (L50 보기) - 원문 자체는 짧으므로 인용 + 해설
            "original_text": (
                "도덕교육의 한 방법으로 벌을 적절하게 사용 "
                "— 2022학년도 전공B Q3 갑(뒤르켐) 제시문"
            ),
            "explanation": (
                "뒤르켐은 『L'Éducation morale(도덕교육론)』에서 "
                "벌을 단순 고통 부과가 아닌 '규칙의 신성성 회복 장치'로 해석한다. "
                "벌은 ① 범죄에 대한 사회적 비난의 표현이고, "
                "② 규칙의 권위를 재확립하며, "
                "③ 집단 양심(conscience collective)을 회복시키는 상징적 기능을 갖는다. "
                "이를 통해 학생에게 규칙에 대한 존경심이 내면화된다. "
                "2022-B Q3은 이 '벌의 본래적 역할'을 ㉡ 빈칸·서술 대상으로 출제하였다."
            ),
            "argument": (
                "전제1: 도덕 규칙은 집단의 공유 규범이며 위반은 집단 질서를 해친다. "
                "전제2: 집단 질서가 위반되면 그 규칙의 권위가 손상된다. "
                "전제3: 벌은 위반에 대한 공적 비난을 통해 손상된 권위를 재확인하는 의례이다. "
                "결론: 따라서 벌의 본래적 역할은 고통 부과가 아니라 "
                "규칙의 권위·신성성 회복과 집단 양심의 재건이다."
            ),
            "counterpoint": (
                "피아제는 벌을 타율적 도덕성 단계의 '속죄적 처벌(expiatory punishment)'로 규정하고, "
                "자율적 도덕성 단계에서는 '상호성 있는 처벌(reciprocal punishment)'로 대체되어야 한다고 본다. "
                "즉 피아제에게 벌은 규칙 권위의 회복이 아니라 '상호성 관계의 복원'을 목적으로 한다."
            ),
            "context": (
                "2022-B Q3 ㉡(벌의 본래적 역할) 서술 대상. "
                "뒤르켐 도덕교육의 사회학적 기능론을 대표하는 주장."
            ),
            "keywords": ["벌", "규칙의 권위 재확립", "집단 양심", "신성성 회복", "도덕교육"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-008: 사회적 사실로서의 도덕 (2022-B Q3, 2024-B Q4)
        {
            "id": "durkheim-claim-008",
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-division-of-labor",
            "source_detail": "사회분업론 (1893) · L'Éducation morale (1925) · 2022학년도 전공B Q3 · 2024학년도 전공B Q4",
            "claim": (
                "도덕은 행위를 미리 정한 규칙의 체계로서 사회에 의해 형성된다. "
                "도덕성은 인간의 행위를 미리 결정해 주는 용인된 규칙들의 체계이며, "
                "개인이 만드는 것이 아니라 이미 존재하는 사회적 사실(fait social)이 "
                "개인에게 외재적 구속으로 작용한다."
            ),
            # 2022-B L114 + 2024-B L157 verbatim 병기
            "original_text": (
                "도덕은 행위를 미리 정한 규칙의 체계로서 사회에 의해 형성 "
                "— 2022학년도 전공B Q3 갑(뒤르켐) 제시문 / "
                "( ㉠ )은/는 도덕성의 근원 … 도덕성은 인간의 행위를 미리 결정해 주는 "
                "용인된 규칙들의 체계 "
                "— 2024학년도 전공B Q4 (가) 뒤르켐 제시문"
            ),
            "explanation": (
                "뒤르켐 사회학의 기본 개념인 '사회적 사실(fait social)'은 "
                "개인 외부에 존재하며 개인에게 구속력 있는 사회적 실재를 뜻한다. "
                "도덕은 전형적인 사회적 사실의 사례로서, 개인이 창출하는 것이 아니라 "
                "사회가 이미 마련해 놓은 규칙 체계이며, 개인은 사회화 과정을 통해 이를 내면화한다. "
                "2024-B Q4는 '( ㉠ )은/는 도덕성의 근원'의 ㉠을 '사회'로 확정함으로써 "
                "이 사회적 사실 테제를 정면으로 평가한다."
            ),
            "argument": (
                "전제1: 개인이 태어나기 이전에 이미 사회에는 규범·규칙 체계가 존재한다. "
                "전제2: 이 규범은 개인 외부에서 개인의 행위를 구속·결정한다. "
                "전제3: 따라서 도덕은 개인 심리가 아니라 사회적 사실로서 실재한다. "
                "결론: 도덕은 사회에 의해 형성되는 규칙 체계이며, "
                "도덕 연구는 사회학의 과제이다."
            ),
            "counterpoint": (
                "칸트 윤리학은 도덕의 근원을 사회가 아니라 순수실천이성의 자기 입법에서 찾는다. "
                "피아제 역시 도덕 규칙이 일방적으로 사회로부터 부과되는 것이 아니라 "
                "아동 간 상호작용 속에서 구성된다고 보아 뒤르켐의 외재주의를 비판한다."
            ),
            "context": (
                "2022-B Q3과 2024-B Q4 (가)에서 뒤르켐의 전제 명제로 반복 출제. "
                "뒤르켐 사회학 전체의 기초 개념인 '사회적 사실'이 도덕에 적용된 형태."
            ),
            "keywords": ["사회적 사실", "사회", "규칙의 체계", "외재적 구속", "도덕의 사회학적 근원"],
            "verified": False,
            "verification_log": [],
        },
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """뒤르켐 핵심 키워드 데이터 입력. 중복 체크 후 insert."""
    keywords = [
        {
            "id": "kw-durkheim-three-elements",
            "term": "도덕성 3요소",
            "term_en": "three elements of morality",
            "definition": (
                "뒤르켐이 『L'Éducation morale(도덕교육론)』에서 제시한 도덕성의 구성 체계. "
                "① 규율 정신(esprit de discipline) — 규칙성에 대한 선호와 권위에 대한 존중, "
                "② 집단에의 애착(attachement aux groupes sociaux) — 사회 집단의 이익·가치에 대한 정서적 결속, "
                "③ 의지의 자율성(autonomie de la volonté) — 도덕 규칙의 근거를 이성적으로 이해하고 자발적으로 수용하는 능력. "
                "앞의 두 요소만으로는 불충분하며 자율성이 완성되어야 진정한 도덕성이다. "
                "2015-B 논술1·2024-B Q4·2025-A Q5에 반복 출제된 뒤르켐 최대 빈출 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-education-morale",
            "related_terms": ["규율 정신", "집단에의 애착", "의지의 자율성", "도덕교육론", "사회화"],
        },
        {
            "id": "kw-durkheim-esprit-discipline",
            "term": "규율 정신",
            "term_en": "esprit de discipline",
            "definition": (
                "뒤르켐 도덕성 3요소의 첫 번째. "
                "도덕 규칙을 일관성 있게 준수하는 행위자의 성향인 규칙성에 대한 선호와 "
                "권위(authority)에 대한 존중. "
                "도덕 규칙은 개인에게 외적·선행적·강제적 권위로 작용하며, "
                "교사는 '규율과 금지의 대변자·본보기'로서 이 권위를 학생에게 내면화시킨다. "
                "2022-B Q3 ㉠(권위)·2024-B Q4 ㉢(권위)의 이론적 배경."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-education-morale",
            "related_terms": ["도덕성 3요소", "권위", "규칙성", "사회적 사실"],
        },
        {
            "id": "kw-durkheim-attachement-groupes",
            "term": "집단에의 애착",
            "term_en": "attachement aux groupes sociaux",
            "definition": (
                "뒤르켐 도덕성 3요소의 두 번째. "
                "개인이 속한 사회 집단의 이익·가치·목적에 정서적으로 결속되어 "
                "집단의 관점에서 행동하려는 성향. "
                "집단 속에서 자신의 도덕적 존재를 발견·실현하는 측면을 담당한다. "
                "2025-A Q5 빈칸 ㉡의 정답 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-education-morale",
            "related_terms": ["도덕성 3요소", "사회 집단", "집단의 이익", "집합 의식"],
        },
        {
            "id": "kw-durkheim-autonomie-volonte",
            "term": "의지의 자율성",
            "term_en": "autonomie de la volonté",
            "definition": (
                "뒤르켐 도덕성 3요소의 세 번째. "
                "도덕 규칙을 지적으로 이해하고 그것을 따르기로 동의하고 원함으로써 "
                "행위의 자율성을 확보하는 능력. "
                "칸트의 순수 이성 자기 입법과 달리, 사회 도덕규범의 근거·기능을 "
                "과학적·이성적으로 통찰하여 자발적으로 수용하는 '계몽된 의식'. "
                "2021-B Q4 빈칸 ㉠·2025-A Q5 ㉢의 정답 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-education-morale",
            "related_terms": ["도덕성 3요소", "이성적 이해", "자발적 수용", "사회의 도덕규범"],
        },
        {
            "id": "kw-durkheim-socialisation",
            "term": "사회화",
            "term_en": "socialisation",
            "definition": (
                "뒤르켐이 도덕 교육의 본질로 규정한 개념. "
                "비사회적인 존재로 태어난 아동을 사회적 존재로 만드는 과정으로, "
                "아동을 사회의 도덕 질서·규범에 통합시키는 활동이다. "
                "개인주의 교육관(루소·칸트)과 대립되는 사회학적 도덕 교육의 핵심 원리. "
                "2015-B 논술1 갑·2021-B Q4 갑 제시문의 trademark 명제."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-education-morale",
            "related_terms": ["도덕교육", "비사회적 존재", "사회의 도덕 질서", "사회적 사실"],
        },
        {
            "id": "kw-durkheim-fait-social",
            "term": "사회적 사실",
            "term_en": "fait social",
            "definition": (
                "뒤르켐 사회학의 기본 개념. "
                "개인 외부에 존재하며 개인에게 구속력을 행사하는 사회적 실재. "
                "도덕은 전형적인 사회적 사실로서, 개인이 창출하는 것이 아니라 "
                "사회가 마련해 놓은 규칙 체계이며 개인은 사회화를 통해 이를 내면화한다. "
                "『사회분업론(1893)』·『사회학적 방법의 규칙(1895)』에서 정식화. "
                "2024-B Q4 ㉠(사회) 정답의 이론적 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-division-of-labor",
            "related_terms": ["사회", "외재적 구속", "집합 의식", "도덕의 사회학적 근원"],
        },
        {
            "id": "kw-durkheim-secular-morality",
            "term": "세속적 도덕",
            "term_en": "secular morality",
            "definition": (
                "뒤르켐의 사회학적 도덕교육 원리. "
                "신에 의해 부여되는 절대적인 도덕과 결별하고, "
                "각각의 사회가 도덕의 기반이 되므로 사회학적 연구를 통해 "
                "각 사회가 이상으로 하는 도덕을 찾아내야 한다는 입장. "
                "근대 세속 교육의 이론적 토대. "
                "2015-B 논술1 갑 제시문의 trademark 명제."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-education-morale",
            "related_terms": ["사회학적 도덕관", "신과의 결별", "사회가 도덕의 기반", "도덕의 근대화"],
        },
        {
            "id": "kw-durkheim-conscience-collective",
            "term": "집합 의식",
            "term_en": "conscience collective",
            "definition": (
                "사회 구성원이 공유하는 공통의 신념·감정·가치의 총체. "
                "개인 의식의 단순 합이 아니라 개인을 넘어서는 사회적 실재이며, "
                "도덕 규범·종교·법의 근원이 된다. "
                "『사회분업론(1893)』·『종교생활의 원초적 형태(1912)』의 핵심 개념. "
                "뒤르켐은 벌을 집합 의식이 손상되었을 때 이를 회복시키는 상징적 기능으로 해석한다."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-elementary-forms",
            "related_terms": ["집단 양심", "사회적 사실", "기계적 연대", "종교"],
        },
        {
            "id": "kw-durkheim-anomie",
            "term": "아노미",
            "term_en": "anomie",
            "definition": (
                "사회 규범이 약화되거나 붕괴된 상태. "
                "뒤르켐이 『사회분업론(1893)』에서 병리적 분업의 형태로, "
                "『자살론(1897)』에서 아노미적 자살의 원인으로 정식화한 개념. "
                "급격한 사회 변동·규범 상실·욕구 제한 불가능 상태에서 나타나며, "
                "근대 사회의 도덕적 통합 붕괴 현상을 설명하는 핵심 개념이다."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "durkheim-suicide",
            "related_terms": ["규범 붕괴", "사회 통합", "아노미적 자살", "유기적 연대"],
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
    """뒤르켐 영향·비교 관계 데이터 입력.

    ES 등록 확인된 thinker_id만 링크한다 (2026-04-22 curl 확인):
    - piaget (장 피아제) : 등록됨 — 뒤르켐의 사회화 중심 도덕교육에 대한 심리발달론적 비판
    - kohlberg (로런스 콜버그) : 등록됨 — 2015-B 논술1 병이 갑(뒤르켐) 4단계 한계를 비판
    - rest (제임스 레스트) : 등록됨 — 신콜버그주의 계보에서 도덕성 발달을 다원적으로 확장
    """
    relations = [
        {
            "from_thinker": "piaget",
            "to_thinker": THINKER_ID,
            "type": "criticized",
            "description": (
                "피아제는 뒤르켐의 사회화 중심 도덕교육이 성인 사회 규칙을 "
                "일방적으로 아동에게 내면화시키는 모델에 머무른다고 비판한다. "
                "피아제에 따르면 아동은 오히려 성인 사회 규칙보다 "
                "아동 상호 간 사회의 규칙을 더 잘 따르며, "
                "자율적 도덕성은 또래 간 상호 협력·상호 존중을 통해 구성된다. "
                "또한 피아제는 부모·권위자의 지나친 권위의 부재가 "
                "자율적 도덕성 발달의 조건이라고 보아, "
                "뒤르켐의 '규율 정신(권위 존중)' 중심 구조와 대립한다. "
                "2015-B 논술1·2021-B Q4·2022-B Q3·2024-B Q4는 모두 "
                "뒤르켐(갑/가)과 피아제(을/나)를 대립적으로 병치한다."
            ),
            "evidence": (
                "Piaget (1932) Le Jugement moral chez l'enfant; "
                "2015-B 논술1 을 제시문 '아동은 성인 사회 규칙보다 아동 상호 간 사회의 규칙을 더 잘 따른다'; "
                "2022-B Q3 을 제시문 '부모의 지나친 권위의 부재'"
            ),
        },
        {
            "from_thinker": "kohlberg",
            "to_thinker": THINKER_ID,
            "type": "criticized",
            "description": (
                "콜버그는 뒤르켐의 도덕교육이 결국 인습 4단계(법과 질서 지향)에 머무른다고 비판한다. "
                "뒤르켐의 '집단에의 애착·사회 규범 내면화'는 "
                "기존 질서(사회 체제·법·제도)를 유지하는 것을 도덕의 궁극 목적으로 삼으므로, "
                "기존 질서 자체가 부정의할 때 그 질서를 비판·초월할 보편적 도덕 원리를 갖지 못한다. "
                "콜버그는 후인습 5·6단계의 사회계약·보편적 정의 원리만이 "
                "기존 질서를 넘어서는 도덕적 자율을 가능케 한다고 본다. "
                "2015-B 논술1 병(콜버그)의 '갑(뒤르켐)의 4단계 관점 한계점 2가지'가 이 비판의 직접 출제."
            ),
            "evidence": (
                "Kohlberg (1981) The Philosophy of Moral Development; "
                "2015-B 논술1 병 제시문 '갑은 이러한 도덕성 발달 단계를 이해하지 못함으로써 "
                "4단계를 최고의 단계로 보는 오류를 범하였다'"
            ),
        },
        {
            "from_thinker": "rest",
            "to_thinker": THINKER_ID,
            "type": "compared",
            "description": (
                "레스트의 4구성요소 모형(도덕적 민감성·판단력·동기화·품성)과 "
                "뒤르켐의 도덕성 3요소(규율 정신·집단에의 애착·의지의 자율성)는 "
                "공히 도덕성을 다원적 구조로 파악하지만, "
                "레스트가 개인의 도덕 기능 과정(cognition·affect·action)의 통합에 주목하는 반면 "
                "뒤르켐은 도덕성의 사회학적 구성 요소(규칙 준수·집단 결속·이성적 승인)에 주목한다. "
                "신콜버그주의(레스트)가 콜버그의 판단 중심을 다원화하듯, "
                "뒤르켐은 칸트의 개인 자율을 사회학적으로 다원화한 선례로 비교된다."
            ),
            "evidence": (
                "Rest (1986) Moral Development; "
                "Durkheim (1925) L'Éducation morale; "
                "2025-A Q5 (나)의 3요소 구조 vs 레스트 4구성요소 문항의 병치"
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
    print("=== 에밀 뒤르켐(Durkheim) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (durkheim)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n[OK] 뒤르켐 데이터 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}", file=sys.stderr)
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
