"""앨버트 반두라(Albert Bandura) 데이터를 ES에 직접 입력하는 스크립트.

Task: TASK-176-05
공식 4회 (2020-A, 2024-B, 2025-B, 2026-B) + coverage 본문 참조 2회 (2014-A, 2019-A).
2024-B → 2025-B → 2026-B 3연속 재출제 (임용시험 도덕·윤리 최장 연속 기록).
moral_development 분야. kohlberg·blasi·hoffman·durkheim 선례 답습.
원문 인용 규칙(agents/coder.md §원문/입력 인용 규칙) 엄수:
 - claims.original_text 는 coverage md 실측 원문(verbatim) 또는 빈 문자열("").
 - 모든 한자·영어 trademark 는 coverage md 역grep으로 0건이면 제거.

역grep 자기검증 (coverage 12파일):
 - "Albert Bandura" → 19 hits / 6 files (HIT)
 - "앨버트 반두라" → 7 hits / 4 files (HIT)
 - "앨버트 밴듀라" → 1 hit / 1 file (HIT, 2024-B)
 - "삼원 상호 결정론" / "triadic reciprocal" → 5+4 hits (HIT: 2026-B·2025-B)
 - "self-sanctions" → 4 hits / 1 file (HIT: 2026-B)
 - "자기 제재" → 8 hits / 3 files (HIT: 2026-B·2020-A)
 - "도덕적 이탈" / "moral disengagement" → 35+10 hits (HIT)
 - "자아효능감" → 14 hits / 3 files (HIT: 2025-B·2020-A·2019-A)
 - "self-efficacy" → 5 hits / 4 files (HIT)
 - "대리 강화" / "vicarious reinforcement" → 14+4 hits (HIT: 2019-A·2020-A)
 - "관찰학습" / "observational learning" → 3+2 hits (HIT: 2020-A·2019-A)
 - "보보 인형" → 6 hits / 2 files (HIT: 2019-A·2020-A)
 - "Social Foundations" → 5 hits / 4 files (HIT: 2026-B·2025-B·2024-B·2019-A)
 - "Moral Disengagement" → 8 hits / 3 files (HIT: 2026-B·2024-B·2020-A)
 - "Social Learning Theory" → 2 hits / 2 files (HIT: 2019-A·2020-A)
 - "human agency" → 2 hits / 1 file (HIT: 2026-B)
 - "selective activation" → 3 hits / 2 files (HIT: 2026-B·2024-B)
 - "완곡한 표현" / "완곡한 명칭" / "유리한 비교" / "책임 전가" / "책임 분산" / "비인간화"
   → 모두 HIT (2026-B·2020-A 주력)
 - Stanford / 스탠퍼드 → HIT (2026-B L284·2025-B L150·2024-B L200)
 - "1925-2021" / "1925-" → HIT (2026-B L284·2025-B L150·2024-B L200)
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


THINKER_ID = "bandura"


def ensure_field(client):
    """moral_development 분야 존재 확인 — kohlberg·blasi·hoffman 선례에서 이미 생성."""
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
                "호프만의 공감 각성·공감 발달 이론, "
                "반두라의 사회인지이론·도덕적 이탈 이론 등을 포함한다. "
                "도덕심리학·도덕교육론과 밀접하게 연관되며 임용시험 핵심 영역이다."
            ),
            "order": 4,
        }
        result = client.index(index=INDEX_FIELDS, id="moral_development", document=doc)
        print(f"[field] moral_development: {result['result']}")


def insert_thinker(client):
    """반두라 사상가 데이터 입력."""
    doc = {
        "id": THINKER_ID,
        "name": "앨버트 반두라 (Albert Bandura)",
        "name_en": "Albert Bandura",
        "field": "moral_development",
        "era": "현대",
        "birth_year": 1925,
        "death_year": 2021,
        "background": (
            "캐나다 태생의 미국 심리학자. 스탠퍼드 대학교(Stanford University)에서 오랜 기간 "
            "심리학 교수로 재직했으며, 사회학습이론(social learning theory) 및 "
            "사회인지이론(social cognitive theory)의 정초자로 평가된다. "
            "1961·1963년 수행한 보보 인형 실험(Bobo doll experiment)을 통해 "
            "아동이 모델의 행동을 관찰하는 것만으로도 공격 행동을 학습한다는 사실을 실험적으로 입증하였고, "
            "이는 고전적 행동주의(스키너)의 직접 강화 중심 학습관을 근본적으로 수정하는 근거가 되었다. "
            "1986년 『Social Foundations of Thought and Action: A Social Cognitive Theory』에서 "
            "삼원 상호 결정론(triadic reciprocal determinism)·자기효능감(self-efficacy)·"
            "관찰학습(observational learning)·대리강화(vicarious reinforcement)를 통합한 "
            "사회인지이론을 정립하였으며, 2016년 『Moral Disengagement: How People Do Harm and "
            "Live with Themselves』에서 도덕 심리학 영역의 대표 trademark인 "
            "도덕적 이탈(moral disengagement) 이론을 집대성하였다. "
            "임용 도덕·윤리 시험에서 2014-A·2019-A·2020-A·2024-B·2025-B·2026-B 등 반복 출제되는 "
            "현대 도덕 심리학의 핵심 사상가이며, 특히 2024-B→2025-B→2026-B 3연속 재출제는 "
            "임용 도덕·윤리 최장 연속 기록이다."
        ),
        "core_philosophy": (
            "반두라 사회인지이론의 핵심은 인간 행동이 개인(Person)·행동(Behavior)·"
            "환경(Environment) 세 요인의 상호작용으로 결정된다는 "
            "삼원 상호 결정론(triadic reciprocal determinism)이다. "
            "이는 환경이 일방적으로 개인을 결정한다는 행동주의·환경결정론을 비판하면서도, "
            "인간이 순수한 내적 자율성만으로 행동한다는 인본주의적 관점과도 거리를 둔다. "
            "도덕성에 있어서 반두라는 도덕 기준(moral standards)과 자기 제재(self-sanctions)의 "
            "결합으로 구성된 자기조절 기제(self-regulatory mechanism)를 제시한다. "
            "자기 제재는 도덕 기준을 준수할 때의 자기 승인(self-approval)과 "
            "위반 시의 자기 비난(self-censure)으로 양방향 작동하며, "
            "이 자기 제재가 '선택적으로 활성화'(selective activation)되거나 "
            "'도덕적 이탈'(moral disengagement)이 일어나면 "
            "동일한 도덕 기준을 가진 사람도 상황에 따라 다르게 행동할 수 있다. "
            "반두라는 도덕적 이탈의 심리사회적 기제를 8가지로 체계화하여 "
            "비난받을 만한 행위 측면(도덕적 정당화·유리한 비교·완곡한 표현), "
            "해로운 결과 측면(결과에 대한 축소·무시·왜곡), "
            "피해자 측면(비인간화·비난의 귀인), "
            "행위 주체성 측면(책임 전가·책임 분산)의 4영역 8기제로 정식화하였다. "
            "또한 자기효능감(self-efficacy)은 특정 상황에서 과제를 성공적으로 수행할 수 있다는 "
            "자기 자신의 능력에 대한 신념으로, "
            "① 실천 성취(enactive mastery experience), ② 대리적 경험(vicarious experience), "
            "③ 언어적 설득(verbal persuasion), ④ 생리적·정서적 상태(physiological and "
            "affective states)라는 4원천에서 형성된다."
        ),
        "philosophical_journey": (
            "반두라는 캐나다에서 출생하여 미국으로 건너와 "
            "스탠퍼드 대학교(Stanford University)에 정착하여 60여 년에 걸쳐 연구 활동을 이어갔다. "
            "초기에는 공격성의 사회적 학습 연구(1961·1963 보보 인형 실험)를 통해 "
            "관찰학습과 대리강화의 실험적 증거를 확립하였고, "
            "1977년 『Social Learning Theory』에서 사회학습이론의 골격을 제시하였다. "
            "1986년 『Social Foundations of Thought and Action』에서는 이론적 확장을 통해 "
            "'사회학습이론'을 '사회인지이론'으로 재명명하고, "
            "인간의 인지·자기조절·행위 주체성(human agency)을 중심에 두는 통합 이론을 정립하였다. "
            "이는 스키너(Skinner)의 급진적 행동주의가 인간을 환경 자극의 수동적 반응자로 "
            "환원한 것을 비판하고, 의도적·자기조절적 행위 주체로서의 인간을 복원한 "
            "패러다임 전환이다. 1990년대 이후에는 도덕 심리학으로 연구 영역을 확장하여 "
            "도덕적 이탈 이론을 정교화하였으며, 1999년 「Moral Disengagement in the Perpetration "
            "of Inhumanities」 논문과 2016년 『Moral Disengagement』 저서에서 8기제 4영역 체계를 "
            "집대성하였다. 이는 콜버그의 인지발달적 도덕판단 이론이 '도덕 판단-행동 간극' "
            "문제에 부딪혔던 것과 달리, 왜 동일한 도덕 기준을 지닌 사람들이 "
            "비인도적·반도덕적 행동을 수행할 수 있는지를 자기조절 기제의 선택적 비활성화로 "
            "설명하는 독자적 접근이다. "
            "블라시의 도덕적 정체성 이론과 2024-B 대립 배치(갑=블라시·을=반두라)되었고, "
            "반두라는 '도덕적 균형(moral balance) 계산'을 통해 도덕적 일탈 행동의 선택 가능성을 "
            "설명하는 반면, 블라시는 도덕적 정체성의 자기 일관성에서 일탈이 선택 불가능함을 "
            "주장한다."
        ),
        "keywords": [
            "삼원 상호 결정론",
            "도덕적 이탈",
            "8가지 도덕적 이탈 기제",
            "자기 제재",
            "자기조절",
            "선택적 활성화",
            "행위 주체성",
            "자기효능감",
            "관찰학습",
            "대리 강화",
        ],
    }
    result = client.index(index=INDEX_THINKERS, id=THINKER_ID, document=doc)
    print(f"[thinker] {THINKER_ID}: {result['result']}")
    return result


def insert_works(client):
    """반두라 주요 저서 데이터 입력."""
    works = [
        {
            "id": "bandura-social-foundations-1986",
            "thinker_id": THINKER_ID,
            "title": "사고와 행동의 사회적 기초: 사회인지이론",
            "title_original": "Social Foundations of Thought and Action: A Social Cognitive Theory",
            "year": 1986,
            "significance": (
                "반두라 사회인지이론의 정식 출발점이자 대표 이론서. "
                "기존 '사회학습이론'을 '사회인지이론(social cognitive theory)'으로 재명명하며, "
                "삼원 상호 결정론(triadic reciprocal determinism)을 제1장에서 체계적으로 정식화한다. "
                "개인(Person)·행동(Behavior)·환경(Environment) 세 요인의 양방향 상호작용 모형을 통해 "
                "스키너의 급진적 행동주의·환경결정론을 비판하고, "
                "인간의 인지·자기조절·행위 주체성(human agency)을 이론 중심에 둔 패러다임 전환을 이루었다. "
                "대리강화·관찰학습·자기효능감 개념도 본서에서 통합 제시된다. "
                "임용 도덕·윤리 2020-A Q7·2025-B Q5·2026-B Q5 제시문의 직접 근거 저작."
            ),
            "key_concepts": [
                "삼원 상호 결정론",
                "사회인지이론",
                "행위 주체성",
                "자기효능감",
                "관찰학습",
                "대리강화",
                "자기조절",
            ],
        },
        {
            "id": "bandura-moral-disengagement-2016",
            "thinker_id": THINKER_ID,
            "title": "도덕적 이탈: 사람들은 어떻게 해를 끼치고 그와 더불어 살아가는가",
            "title_original": "Moral Disengagement: How People Do Harm and Live with Themselves",
            "year": 2016,
            "significance": (
                "반두라 도덕 심리학의 평생 연구를 집대성한 대표 저작. "
                "1986년 『Social Foundations』 9장·1991년 「Social cognitive theory of moral "
                "thought and action」·1999년 「Moral Disengagement in the Perpetration of "
                "Inhumanities」로 이어진 도덕적 이탈 이론을 체계화한다. "
                "도덕 기준과 자기 제재(self-sanctions)로 구성된 자기조절 기제가 "
                "'선택적으로 활성화(selective activation)'되어 해로운 행위로부터 이탈되는 "
                "8가지 심리사회적 기제를 4영역(비난받을 만한 행위·해로운 결과·피해자·행위 주체성)으로 분류한다. "
                "임용 도덕·윤리 2020-A Q7·2024-B Q5·2026-B Q5 trademark 직접 출처."
            ),
            "key_concepts": [
                "도덕적 이탈",
                "자기 제재",
                "선택적 활성화",
                "8가지 도덕적 이탈 기제",
                "도덕적 자기조절",
                "도덕적 정당화",
                "비인간화",
                "책임 전가",
            ],
        },
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """반두라 핵심 주장 데이터 입력.

    original_text는 coverage md 실측 verbatim 원문만 기입.
    확증 불가 구절은 빈 문자열("")로 남기고 explanation에 해설만 둔다.
    """
    claims = [
        # CLAIM-001: 삼원 상호 결정론 (2026-B Q5 ㉠ + 2025-B Q5 + 2014-A 기입형3)
        {
            "id": "bandura-claim-001",
            "thinker_id": THINKER_ID,
            "work_id": "bandura-social-foundations-1986",
            "source_detail": (
                "Social Foundations of Thought and Action (1986) 제1장 · "
                "2014학년도 중등1차 전공A 기입형3 · 2020학년도 전공A Q7 · "
                "2025학년도 전공B Q5 · 2026학년도 전공B Q5 ㉠"
            ),
            "claim": (
                "인간의 기능 수행은 개인(Person)·행동(Behavior)·환경(Environment) "
                "세 요인의 상호작용으로 결정된다. "
                "삼원 상호 결정론(triadic reciprocal determinism / reciprocal causation)은 "
                "환경의 일방적 결정을 부정하면서도 인간 행위를 내적 자율성에만 환원하지 않는 "
                "반두라 사회인지이론의 핵심 모형이다."
            ),
            # 2026-B L92 verbatim + 2014-A L16 verbatim + 2025-B L146 verbatim
            "original_text": (
                "인간의 기능 수행은 개인, 행위, ( ㉠ ) 간 상호작용의 결과이다 "
                "— 2026학년도 전공B Q5 제시문 (coverage/2026-B.md L92) / "
                "환경이 개인의 성격이나 행동을 만드는 것이 아니다. 인간의 발달은 아래 그림처럼 "
                "개인, 환경, 행동 모두가 각각 서로 양 방향으로 영향을 미치는 상호작용으로 나타난다 "
                "— 2014학년도 전공A 기입형3 제시문 (coverage/2014-A.md L16) / "
                "자아효능감은 삼원상호결정론(triadic reciprocal causation)의 한 요소로서 "
                "개인(P) · 환경(E) · 행동(B) 세 요인의 상호작용 속에서 형성된다 "
                "— 2025학년도 전공B Q5 제시문 (coverage/2025-B.md L146)"
            ),
            "explanation": (
                "삼원 상호 결정론은 반두라 『Social Foundations(1986)』 제1장에서 정식화된 "
                "사회인지이론의 메타 모형이다. 개인(Person)에는 인지·정서·신념·생리적 특성이 포함되고, "
                "행동(Behavior)은 실제 수행되는 행위이며, 환경(Environment)은 물리적·사회적 맥락이다. "
                "세 요인은 일방향이 아니라 양방향으로 서로 영향을 주고받으며, "
                "인간 행위는 이 세 요인의 역동적 상호작용의 결과로 나타난다. "
                "이는 스키너의 행동주의(환경→행동)·정신분석(개인→행동)의 일방향 결정 모형을 모두 "
                "극복하는 통합 틀이다. 2026-B Q5 ㉠ 정답 = 환경."
            ),
            "argument": (
                "전제1: 환경이 개인·행동을 일방적으로 결정한다면 인간은 환경 자극의 수동적 반응자에 불과하다. "
                "전제2: 그러나 인간은 환경을 변형·창조하는 인지·자기조절 능력을 가진다. "
                "전제3: 동시에 인간은 완전히 환경으로부터 독립되지도 않으며, 행동은 환경과 지속 상호작용한다. "
                "결론: 따라서 인간 기능은 개인·행동·환경 3자의 양방향 상호작용으로 결정된다."
            ),
            "counterpoint": (
                "스키너의 급진적 행동주의(radical behaviorism)는 내적 인지 변인을 과학적 설명에서 배제하고 "
                "환경-행동의 외적 관찰 가능한 관계에만 의존해야 한다고 본다. "
                "이 관점에서 '개인' 변인을 독립 축으로 세우는 삼원 모형은 "
                "관찰 불가능한 내부 심리를 가정한 비과학적 사변이라는 비판이 가능하다."
            ),
            "context": (
                "2026-B Q5 ㉠ 빈칸 정답(환경) 근거 + 2014-A 기입형3·2020-A Q7·2025-B Q5의 공통 이론 기반. "
                "반두라의 사회인지이론을 한 문장으로 집약하는 trademark 개념."
            ),
            "keywords": [
                "삼원 상호 결정론",
                "triadic reciprocal determinism",
                "개인-행동-환경",
                "사회인지이론",
                "행위 주체성",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-002: 도덕 기준 + 자기 제재 = 자기조절 기제 (2026-B Q5 ㉡)
        {
            "id": "bandura-claim-002",
            "thinker_id": THINKER_ID,
            "work_id": "bandura-moral-disengagement-2016",
            "source_detail": (
                "Moral Disengagement (2016) 제1장 Moral Self-Regulation · "
                "2026학년도 전공B Q5 ㉡ · 2014학년도 전공A 기입형3"
            ),
            "claim": (
                "도덕적 자기조절 기제는 도덕 기준(moral standards)과 자기 제재(self-sanctions)의 "
                "결합으로 구성된다. 자기 제재는 도덕 기준 준수 시의 자기 승인(self-approval)·자부심과 "
                "위반 시의 자기 비난(self-censure)·수치로 양방향 작동하며, "
                "도덕적 추론을 실제 도덕 행위로 변환하는 내적 동기 기제이다."
            ),
            # 2026-B L94 verbatim
            "original_text": (
                "인간은 자신에게 만족감과 자존감을 주는 것을 선택하여 실행한다. "
                "반면 이를 침해하는 행동은 꺼리는데, 그 이유는 자기 비난을 초래하기 때문이다. "
                "도덕적 기준 및 ( ㉡ )와/과 결합된 자기조절 기제는 도덕적 추론을 행동으로 변환하여 "
                "결과적으로 도덕적 행위로 나아가게 한다 "
                "— 2026학년도 전공B Q5 제시문 (coverage/2026-B.md L94) / "
                "개인의 (     )이/가 선택적으로 활성화되고 해로운 행위로부터 이탈되는 메카니즘 "
                "— 2014학년도 전공A 기입형3 제시문 (coverage/2014-A.md L16)"
            ),
            "explanation": (
                "반두라 『Moral Disengagement(2016)』 제1장 'Moral Self-Regulation'의 핵심 구조. "
                "개인은 도덕 기준을 내면화하고, 그 기준에 따라 자신의 행동을 평가한다. "
                "기준 준수 시 자기 승인(자부심·만족감)이 보상으로 작동하고, "
                "위반 시 자기 비난(수치·죄책감)이 처벌로 작동한다. "
                "이 자기 제재의 양방향 작동이 '자기조절 기제(self-regulatory mechanism)'이며, "
                "도덕적 추론을 실제 도덕 행위로 변환하는 동기적 매개이다. "
                "2026-B Q5 ㉡ 정답 = 자기 제재(self-sanctions) 또는 자기 비난(self-censure)."
            ),
            "argument": (
                "전제1: 도덕 기준만으로는 행위가 발생하지 않는다(판단-행동 간극). "
                "전제2: 기준 위반 시 자기 비난이 처벌로, 준수 시 자기 승인이 보상으로 내적 작동한다. "
                "전제3: 이 보상-처벌의 자기조절 기제가 도덕 추론을 행위로 변환한다. "
                "결론: 따라서 도덕 기준 + 자기 제재 = 도덕적 자기조절 기제."
            ),
            "counterpoint": (
                "블라시의 도덕적 정체성 이론은 도덕 행위의 원천을 "
                "자기 제재의 보상-처벌 계산이 아니라 "
                "자아의 통합성(integrity) 자체에서 찾는다. "
                "도덕적 정체성이 강한 사람에게 도덕 위반은 자기 비난을 회피하기 위한 선택이 아니라 "
                "'자기이기를 포기하는 것'으로서 애초에 선택지가 되지 못한다."
            ),
            "context": (
                "2026-B Q5 ㉡ 빈칸 정답의 직접 근거. "
                "반두라 도덕 심리학을 관통하는 자기조절 모형의 기본 구조."
            ),
            "keywords": [
                "도덕적 자기조절",
                "자기 제재",
                "self-sanctions",
                "도덕 기준",
                "자기 승인",
                "자기 비난",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-003: 선택적 활성화 + 도덕적 이탈 (2026-B Q5)
        {
            "id": "bandura-claim-003",
            "thinker_id": THINKER_ID,
            "work_id": "bandura-moral-disengagement-2016",
            "source_detail": (
                "Moral Disengagement (2016) · 2020학년도 전공A Q7 · "
                "2024학년도 전공B Q5(을) · 2026학년도 전공B Q5"
            ),
            "claim": (
                "자기 제재가 '선택적으로 활성화'(selective activation)되거나 "
                "'도덕적 이탈'(moral disengagement)이 일어나면, "
                "동일한 도덕 기준을 지닌 사람들도 다양한 방식으로 행동할 수 있다. "
                "도덕적 이탈은 자기 제재의 선택적 비활성화를 통해 반도덕적 행위를 가능하게 하는 "
                "심리사회적 기제이다."
            ),
            # 2026-B L94 verbatim
            "original_text": (
                "( ㉡ )이/가 선택적으로 활성화되거나 도덕적 이탈이 일어나면, "
                "인간은 동일한 도덕적 기준을 지니고 있어도 다양한 방식으로 행동할 수 있다 "
                "— 2026학년도 전공B Q5 제시문 (coverage/2026-B.md L94) / "
                "개인의 (     )이/가 선택적으로 활성화되고 해로운 행위로부터 이탈되는 메카니즘 "
                "— 2014학년도 전공A 기입형3 제시문 (coverage/2014-A.md L16)"
            ),
            "explanation": (
                "반두라의 도덕적 이탈 이론의 출발점. "
                "동일한 도덕 기준을 내면화한 사람이라 하더라도, "
                "상황과 맥락에 따라 자기 제재가 선택적으로 작동하거나 정지할 수 있다. "
                "자기 제재가 비활성화되면 도덕 기준의 위반에도 자기 비난이 발생하지 않으며, "
                "따라서 비인도적·반도덕적 행동이 '자신이 도덕적 사람이라는 자아상을 유지한 채' 수행된다. "
                "이것이 '도덕적 이탈(moral disengagement)'이며, "
                "홀로코스트·제노사이드·전쟁 범죄·학교 폭력 등의 심리학적 설명 틀이 된다."
            ),
            "argument": (
                "전제1: 동일한 도덕 기준을 가진 사람들도 비인도적 행동을 수행할 수 있다. "
                "전제2: 이 현상은 도덕 기준의 부재가 아니라 자기 제재의 선택적 비활성화로 설명 가능하다. "
                "전제3: 자기 제재의 선택적 비활성화 = 도덕적 이탈. "
                "결론: 따라서 도덕적 이탈은 자기조절 기제의 선택적 작동이라는 관점에서 설명된다."
            ),
            "counterpoint": (
                "블라시는 도덕적 정체성이 강한 사람에게 도덕적 일탈은 선택지 자체로 고려되지 않는다고 본다. "
                "그에 따르면 반두라의 '최적 균형 계산' 모형은 도덕 행위의 조건부·계산적 성격을 과장하며, "
                "참된 도덕 정체성이 주는 자기 일관성 요구의 절대성을 간과한다."
            ),
            "context": (
                "2026-B Q5 원문 핵심 구절 · 2024-B Q5(을)의 균형 계산 논리로 연결. "
                "반두라 도덕 이론의 trademark 설명 구조."
            ),
            "keywords": [
                "도덕적 이탈",
                "moral disengagement",
                "선택적 활성화",
                "selective activation",
                "자기 제재 비활성화",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-004: 8가지 도덕적 이탈 기제 4영역 (2026-B Q5 + 2020-A Q7)
        {
            "id": "bandura-claim-004",
            "thinker_id": THINKER_ID,
            "work_id": "bandura-moral-disengagement-2016",
            "source_detail": (
                "Moral Disengagement (2016) · Bandura (1999) Moral Disengagement in the "
                "Perpetration of Inhumanities · 2020학년도 전공A Q7 · 2026학년도 전공B Q5"
            ),
            "claim": (
                "자기 제재가 선택적으로 비활성화되는 심리사회적 기제는 8가지이며, "
                "4영역으로 분류된다: "
                "(a) 비난받을 만한 행위 측면 — 도덕적 정당화·유리한 비교·완곡한 표현, "
                "(b) 해로운 결과 측면 — 결과에 대한 축소·무시·왜곡, "
                "(c) 피해자 측면 — 비인간화·비난의 귀인, "
                "(d) 행위 주체성 측면 — 책임 전가·책임 분산."
            ),
            # 2026-B L96 verbatim + 2020-A L24 verbatim (기제 열거)
            "original_text": (
                "자기조절 과정에서 유해한 행동에 대해 ( ㉡ )이/가 선택적으로 활성화되는 "
                "심리사회적 기제(psychosocial mechanism)는 8가지이다. "
                "비난받을 만한 행위 측면에서는 도덕적 정당화, 유리한 비교, 완곡한 표현이 있고, "
                "해로운 결과 측면에서는 결과에 대한 축소·무시·왜곡이 있다. "
                "그리고 피해자 측면에서는 비인간화와 ㉢ 비난의 귀인(attribution)이 있고, "
                "행위 주체성 측면에서는 ㉣ 책임 전가(displacement)와 책임 분산이 있다 "
                "— 2026학년도 전공B Q5 제시문 (coverage/2026-B.md L96) / "
                "도덕적 정당화, 완곡한 언어의 사용, 유리한 비교, 책임 소재의 이동, 책임감의 분산, "
                "결과의 무시와 왜곡, 비인간화, 비난의 전가 "
                "— 2014학년도 전공A 기입형3 제시문 (coverage/2014-A.md L16)"
            ),
            "explanation": (
                "반두라 도덕 심리학의 대표 trademark. "
                "1991년 「Social cognitive theory of moral thought and action」 Table 1, "
                "1999년 「Moral Disengagement in the Perpetration of Inhumanities」 Figure 1, "
                "2016년 『Moral Disengagement』에서 체계화된 4영역 8기제 공식 도식. "
                "(a) 비난받을 만한 행위 측면: ① 도덕적 정당화(moral justification — 사회적·도덕적 명분 "
                "부여), ② 유리한 비교(advantageous comparison — 더 잔혹한 타자와의 대조로 자기 "
                "행위를 미화), ③ 완곡한 표현(euphemistic labeling — 부수적 피해·구조조정 등 "
                "완곡한 언어로 행위의 도덕적 무게를 감소). "
                "(b) 해로운 결과 측면: ④ 결과에 대한 축소·무시·왜곡(minimizing/ignoring/"
                "misconstruing consequences). "
                "(c) 피해자 측면: ⑤ 비인간화(dehumanization — 피해자를 인간 이하로 규정), "
                "⑥ 비난의 귀인(attribution of blame — 피해자에게 책임 전가). "
                "(d) 행위 주체성 측면: ⑦ 책임 전가(displacement of responsibility — 권위자·상급자의 "
                "지시로 귀속), ⑧ 책임 분산(diffusion of responsibility — 집단 전체로 희석). "
                "2020-A Q7 ㉠=완곡한 명칭 사용, ㉡=유리한 비교, ㉢=비인간화. "
                "2026-B Q5 ㉢=비난의 귀인, ㉣=책임 전가."
            ),
            "argument": (
                "전제1: 도덕적 이탈은 자기 제재의 선택적 비활성화이다. "
                "전제2: 이 비활성화는 무작위가 아니라 체계적인 심리사회적 기제로 일어난다. "
                "전제3: 기제는 행위·결과·피해자·행위 주체성 네 측면에서 작동한다. "
                "결론: 따라서 도덕적 이탈은 4영역 8기제의 체계적 구조로 정식화된다."
            ),
            "counterpoint": (
                "8기제 분류의 경계는 실제 사례에서 중첩될 수 있다는 비판이 있다. "
                "예: '상부의 명령이었다(책임 전가)'와 '모두가 함께 한 일이다(책임 분산)'는 "
                "동시에 작동하는 경우가 많아 경계가 모호하다. "
                "또한 문화·정치적 맥락에 따라 특정 기제의 지배적 작동 패턴이 달라질 수 있다."
            ),
            "context": (
                "2026-B Q5 원문 핵심 구절(4영역 전면) · 2020-A Q7 도표 재현(3x3 구조) · "
                "2014-A 기입형3 8기제 전체 열거. 반두라 도덕 심리학 최빈출 개념."
            ),
            "keywords": [
                "8가지 도덕적 이탈 기제",
                "4영역",
                "도덕적 정당화",
                "유리한 비교",
                "완곡한 표현",
                "비인간화",
                "비난의 귀인",
                "책임 전가",
                "책임 분산",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-005: 행위 주체성 (human agency) — 2026-B Q5
        {
            "id": "bandura-claim-005",
            "thinker_id": THINKER_ID,
            "work_id": "bandura-social-foundations-1986",
            "source_detail": (
                "Social Foundations of Thought and Action (1986) · 2026학년도 전공B Q5"
            ),
            "claim": (
                "인간은 환경 자극의 수동적 반응자가 아니라 "
                "자신의 기능 수행과 행동에 대해 의도적인 영향력을 행사하는 행위 주체이다. "
                "인간의 행위가 전적으로 외적인 힘에 의해 통제된다면 "
                "그 행동에 대해 책임을 지는 것은 적절하지 않다. "
                "도덕적 책임은 행위 주체성(human agency)을 전제로 성립한다."
            ),
            # 2026-B L92 verbatim
            "original_text": (
                "도덕성과 관련하여 행위 주체가 된다는 것은 자신의 기능 수행과 행동에 대해 "
                "의도적인 영향력을 행사한다는 의미이다. "
                "인간의 행위가 전적으로 외적인 힘에 의해 통제된다면, "
                "인간이 그 행동에 대해 책임을 지는 것은 적절하지 않다 "
                "— 2026학년도 전공B Q5 제시문 (coverage/2026-B.md L92)"
            ),
            "explanation": (
                "반두라 사회인지이론의 인간관 선언. "
                "스키너(B.F. Skinner)의 급진적 행동주의가 인간 행위를 환경 자극의 반사적·결정적 결과로 "
                "환원한 것에 대한 직접적 반박이다. "
                "반두라는 인간이 자기 행위를 의도적으로 조직·조절하는 주체(agent)임을 강조하며, "
                "이 행위 주체성(agency)이 도덕적 책임의 가능 조건임을 선언한다. "
                "만약 인간 행위가 완전히 환경에 의해 결정된다면 도덕적 책임 귀속 자체가 불가능하다."
            ),
            "argument": (
                "전제1: 도덕적 책임은 행위 주체의 의도적 통제 가능성을 전제한다. "
                "전제2: 외적 힘의 완전 통제를 가정하면 이 전제는 성립하지 않는다. "
                "전제3: 그러나 인간은 자기 기능·행동에 의도적 영향력을 행사할 수 있다. "
                "결론: 따라서 인간은 도덕적 책임의 귀속 주체로서 행위 주체성을 가진다."
            ),
            "counterpoint": (
                "급진적 행동주의(스키너)는 '행위 주체성' 개념을 관찰 불가능한 내부 원인에 의한 "
                "비과학적 설명으로 간주한다. 또한 신경과학적 결정론은 의지·선택도 뇌 상태의 산물이므로 "
                "엄밀한 의미의 주체성은 착시라고 본다."
            ),
            "context": (
                "2026-B Q5 제시문 첫 문장 trademark · 반두라의 스키너 환경결정론 비판을 함축하는 "
                "철학적 선언. 행위 주체성 개념은 2020-A·2024-B·2025-B·2026-B 전반의 이론적 토대."
            ),
            "keywords": [
                "행위 주체성",
                "human agency",
                "도덕적 책임",
                "의도적 영향력",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-006: 자기효능감 + 4원천 (2025-B Q5)
        {
            "id": "bandura-claim-006",
            "thinker_id": THINKER_ID,
            "work_id": "bandura-social-foundations-1986",
            "source_detail": (
                "Social Foundations of Thought and Action (1986) · "
                "Self-Efficacy: The Exercise of Control (1997) 제3장 · "
                "2019학년도 전공A Q3 · 2025학년도 전공B Q5"
            ),
            "claim": (
                "자기효능감(self-efficacy)은 특정한 상황에서 과제를 성공적으로 수행할 수 있다는 "
                "자기 자신의 능력에 대한 신념이다. 자기효능감의 원천은 "
                "① 실천 성취(enactive mastery experience), ② 대리적 경험(vicarious experience), "
                "③ 언어적 설득(verbal persuasion), ④ 생리적·정서적 상태(physiological and "
                "affective states)의 4가지이다."
            ),
            # 2025-B L146 verbatim
            "original_text": (
                "자아효능감(self-efficacy)은 특정한 상황에서 과제를 성공적으로 수행할 수 있다는 "
                "자기 자신의 능력에 대한 신념이다. … 자아효능감의 원천은 ① 실천 성취"
                "(enactive mastery experience), ② 대리적 경험(vicarious experience), "
                "③ 언어적 설득(verbal persuasion), ④ 생리적·정서적 상태(physiological and "
                "affective states)이다 "
                "— 2025학년도 전공B Q5 제시문 (coverage/2025-B.md L146)"
            ),
            "explanation": (
                "반두라 『Self-Efficacy: The Exercise of Control(1997)』 제3장에서 정식화된 "
                "자기효능감 4원천 체계. ① 실천 성취 — 자신이 실제 과제를 성공적으로 수행한 경험이 "
                "가장 강력한 효능감 원천이다. ② 대리적 경험 — 유사한 타인의 성공을 관찰함으로써 "
                "'나도 할 수 있다'는 효능감을 형성한다. ③ 언어적 설득 — 타인의 격려·설득·피드백이 "
                "효능감에 영향을 준다. ④ 생리적·정서적 상태 — 긴장·피로·불안 같은 신체·정서 신호를 "
                "해석하여 자기 능력을 평가한다. "
                "자기효능감은 사회인지이론 내에서 자기조절·동기·도전 지속성을 매개하는 핵심 변인이다."
            ),
            "argument": (
                "전제1: 인간 행동은 결과 예측만이 아니라 자기 능력 신념에 의해 결정된다. "
                "전제2: 능력 신념(효능감)은 경험·관찰·설득·생리상태의 네 원천에서 형성된다. "
                "전제3: 각 원천의 가중치는 실천 성취 > 대리 경험 > 언어 설득 > 생리 상태 순이다. "
                "결론: 따라서 자기효능감은 4원천의 체계적 조합에서 형성되며, 도덕·학습·동기를 매개한다."
            ),
            "counterpoint": (
                "효능감과 실제 수행의 인과 방향 문제가 제기된다. 높은 효능감이 수행을 향상시키는가, "
                "아니면 과거 성공이 효능감을 높이는가의 순환 해석 위험이 있다. "
                "또한 자기효능감 과대 평가는 오히려 현실 오판·위험 감수를 초래할 수 있다는 비판도 있다."
            ),
            "context": (
                "2025-B Q5 trademark 4중 일치 핵심 + 2019-A Q3(대리 강화)과 개념적 연속성. "
                "자기효능감 4원천은 반두라 평생 연구의 핵심 개념."
            ),
            "keywords": [
                "자기효능감",
                "self-efficacy",
                "4원천",
                "실천 성취",
                "대리적 경험",
                "언어적 설득",
                "생리적 정서적 상태",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-007: 관찰학습 + 대리 강화 (2019-A Q3)
        {
            "id": "bandura-claim-007",
            "thinker_id": THINKER_ID,
            "work_id": "bandura-social-foundations-1986",
            "source_detail": (
                "Social Learning Theory (1977) · Social Foundations of Thought and Action (1986) · "
                "2019학년도 전공A Q3"
            ),
            "claim": (
                "사회학습이론은 모델을 관찰하는 것만으로도 행동이 강화된다고 본다. "
                "대리 강화(vicarious reinforcement)는 관찰자가 다른 사람의 행동이 강화되는 것을 "
                "봄으로써 관찰한 행동을 하려는 경향이 증가되는 현상이다. "
                "단순히 모델의 행동을 보는 것보다 그 모델의 행동이 강화되는 것을 보는 것이 "
                "관찰자의 행동 경향을 증가시키는 데 더 효과적이다."
            ),
            # 2019-A L17 verbatim (Q3 제시문)
            "original_text": (
                "사회학습이론은 모델을 관찰하는 것만으로도 행동이 강화된다고 본다 … "
                "강화의 한 유형인 (     )은/는 관찰자가 다른 사람의 행동이 강화되는 것을 봄으로써 "
                "관찰한 행동을 하려는 경향이 증가되는 것을 말한다 … "
                "단순히 모델의 행동을 보는 것보다는 그 모델의 행동이 강화되는 것을 보는 것이 "
                "관찰자의 행동 경향을 증가시키는 데 더 효과적 … "
                "교사를 도와준 학생이 교사로부터 긍정적 강화를 받을 때, "
                "이를 목격한 학생들은 교사를 돕고자 하는 도덕적 행동 경향이 증가된다 "
                "— 2019학년도 전공A Q3 제시문 (coverage/2019-A.md L17)"
            ),
            "explanation": (
                "반두라 『Social Learning Theory(1977)』의 기본 명제이자 "
                "1961·1963년 보보 인형 실험(Bobo doll experiment)의 이론적 근거. "
                "고전적 행동주의(스키너)는 학습이 직접 강화·처벌에 의해서만 성립한다고 보지만, "
                "반두라는 모델의 행동·결과를 관찰하는 것만으로도 관찰자의 행동 경향이 변화함을 입증했다. "
                "대리 강화(vicarious reinforcement)와 쌍을 이루는 vicarious punishment는 관찰자가 "
                "모델의 결과를 통해 간접적으로 강화·처벌을 받는 현상이며, "
                "이는 도덕교육에서 모범인의 행동과 그 결과를 제시함으로써 아동의 도덕적 행동 경향을 "
                "증가시키는 교육학적 함의를 가진다. "
                "2019-A Q3 빈칸 정답 = 대리 강화."
            ),
            "argument": (
                "전제1: 학습은 직접 강화 없이도 성립할 수 있다. "
                "전제2: 모델의 행동과 그 결과(강화·처벌)를 관찰함으로써 관찰자의 행동 경향이 변한다. "
                "전제3: 결과가 강화되는 모델의 행동은 관찰자에 의해 더 잘 모방된다. "
                "결론: 따라서 관찰학습과 대리 강화가 사회적 학습의 핵심 기제이다."
            ),
            "counterpoint": (
                "스키너의 급진적 행동주의는 관찰학습도 결국 관찰자의 과거 직접 강화 경험으로 환원 "
                "설명된다고 본다. 즉 '관찰만으로 학습'은 보이지 않는 내적 인지 매개를 가정하므로 "
                "조작적 조건화로 재설명 가능하다는 반론이다."
            ),
            "context": (
                "2019-A Q3 제시문 핵심 · 사회학습이론의 공식 정의 + 보보 인형 실험의 이론적 배경. "
                "임용 도덕·윤리의 반두라 초기 출제 trademark."
            ),
            "keywords": [
                "관찰학습",
                "observational learning",
                "대리 강화",
                "vicarious reinforcement",
                "보보 인형 실험",
                "사회학습이론",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-008: 도덕적 균형 계산 + 도덕적 일탈 (2024-B Q5 을)
        {
            "id": "bandura-claim-008",
            "thinker_id": THINKER_ID,
            "work_id": "bandura-moral-disengagement-2016",
            "source_detail": (
                "Moral Disengagement (2016) · 2024학년도 전공B Q5 (을)"
            ),
            "claim": (
                "사람들은 자신을 구성하는 모든 정체성을 최적의 균형(balance) 상태로 이끄는 선택을 한다. "
                "그동안 자신이 행한 도덕적 행동의 역사에 기초하여 현재 자신의 도덕적 균형을 계산하며, "
                "'이렇게 행동해도 내가 원하는 유형의 도덕적인 사람으로 남아있을 수 있다면' "
                "도덕적 일탈 행동을 선택할 수 있다."
            ),
            # 2024-B L196 verbatim
            "original_text": (
                "자신을 구성하는 모든 정체성을 최적의 ( ㉢ ) 상태로 이끄는 선택이 무엇인지 따져보게 된다. "
                "이 때 그 동안 자신이 행한 도덕적 행동의 역사에 기초하여 "
                "현재 자신의 도덕적 ( ㉢ )을/를 계산한다. "
                "이러한 저울질의 결과 '이렇게 행동해도 내가 원하는 유형의 도덕적인 사람으로 "
                "남아있을 수 있다면' 사람들은 ㉣ 도덕적 일탈 행동을 선택할 수 있다 "
                "— 2024학년도 전공B Q5 을 제시문 (coverage/2024-B.md L196)"
            ),
            "explanation": (
                "반두라 도덕적 자기조절 이론의 계산 모형. "
                "도덕 행위자는 과거 도덕적 행동의 역사(누적 '도덕 잔고')를 바탕으로 "
                "현재 전체 정체성의 최적 균형을 계산한다. "
                "누적 도덕 잔고가 충분하면 일시적 도덕 일탈을 허용해도 "
                "'도덕적 사람이라는 자아상'이 유지 가능하다고 판단하여 일탈 행동을 선택할 수 있다. "
                "이 모형은 도덕적 이탈 8기제가 작동하는 배후 동기 구조를 제공한다. "
                "2024-B Q5 ㉢ 정답 = 균형, ㉣ = 도덕적 일탈 행동."
            ),
            "argument": (
                "전제1: 정체성은 도덕적 요소와 비도덕적 요소의 복합으로 구성된다. "
                "전제2: 사람들은 정체성 요소 간 최적 균형을 추구한다. "
                "전제3: 과거 도덕 행동의 누적이 현재 도덕 균형 계산의 기준이 된다. "
                "결론: 따라서 누적 도덕 잔고가 충분하면 일시적 도덕 일탈도 선택 가능한 선택지가 된다."
            ),
            "counterpoint": (
                "블라시(Augusto Blasi)는 이 '균형 계산' 모형을 도덕적 정체성의 경직된 절대성을 "
                "간과한 이상화의 반대편 오류로 비판한다. "
                "블라시에 따르면 진정한 도덕적 정체성을 지닌 사람에게 "
                "중심 가치에 반하는 도덕적 일탈 행동은 선택지 자체로 고려되지 않으며, "
                "자기이기를 포기하는 심리적 불가능성에 속한다."
            ),
            "context": (
                "2024-B Q5 을(반두라) 제시문 핵심 trademark. "
                "갑(블라시)과 대립 배치되어 도덕적 정체성 vs 도덕적 균형 계산의 구도로 출제."
            ),
            "keywords": [
                "도덕적 균형",
                "최적 균형",
                "balance",
                "도덕적 일탈 행동",
                "도덕적 자기조절",
                "정체성 균형 계산",
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
    """반두라 핵심 키워드 데이터 입력. 중복 체크 후 insert."""
    keywords = [
        {
            "id": "kw-bandura-triadic-reciprocal-determinism",
            "term": "삼원 상호 결정론",
            "term_en": "triadic reciprocal determinism",
            "definition": (
                "반두라 『Social Foundations of Thought and Action(1986)』 제1장 trademark. "
                "인간의 기능 수행이 개인(Person)·행동(Behavior)·환경(Environment) "
                "세 요인의 양방향 상호작용으로 결정된다는 사회인지이론의 메타 모형. "
                "일방향 환경결정론(행동주의)·내적결정론(정신분석)을 모두 극복하는 통합 틀이다. "
                "2014-A 기입형3·2020-A Q7·2025-B Q5·2026-B Q5 ㉠에 반복 출제."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "bandura-social-foundations-1986",
            "related_terms": ["사회인지이론", "개인-행동-환경", "행위 주체성", "reciprocal causation"],
        },
        {
            "id": "kw-bandura-moral-disengagement",
            "term": "도덕적 이탈",
            "term_en": "moral disengagement",
            "definition": (
                "반두라 도덕 심리학의 대표 trademark. "
                "자기 제재가 선택적으로 비활성화되어 "
                "'동일한 도덕 기준을 지닌 사람들도 반도덕적 행동을 수행할 수 있게 되는' 심리사회적 현상. "
                "『Moral Disengagement(2016)』에서 8가지 기제 4영역 체계로 집대성. "
                "2020-A Q7·2024-B Q5·2026-B Q5에 반복 출제된 반두라 최빈출 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "bandura-moral-disengagement-2016",
            "related_terms": ["자기 제재", "선택적 활성화", "8가지 기제", "도덕적 자기조절"],
        },
        {
            "id": "kw-bandura-eight-mechanisms",
            "term": "8가지 도덕적 이탈 기제",
            "term_en": "eight mechanisms of moral disengagement",
            "definition": (
                "반두라 도덕적 이탈 이론의 공식 체계(1991·1999·2016). "
                "4영역 분류: "
                "(a) 비난받을 만한 행위 — 도덕적 정당화·유리한 비교·완곡한 표현; "
                "(b) 해로운 결과 — 결과에 대한 축소·무시·왜곡; "
                "(c) 피해자 — 비인간화·비난의 귀인; "
                "(d) 행위 주체성 — 책임 전가·책임 분산. "
                "2020-A Q7 도표(3x3 연결 구조) · 2026-B Q5 원문 4영역 전면 출제."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "bandura-moral-disengagement-2016",
            "related_terms": ["도덕적 이탈", "도덕적 정당화", "비인간화", "책임 전가", "책임 분산"],
        },
        {
            "id": "kw-bandura-self-sanctions",
            "term": "자기 제재",
            "term_en": "self-sanctions",
            "definition": (
                "반두라 『Moral Disengagement(2016)』 제1장 'Moral Self-Regulation' trademark. "
                "도덕 기준 준수 시의 자기 승인(self-approval)·자부심과 "
                "위반 시의 자기 비난(self-censure)·수치로 양방향 작동하는 내적 제재 기제. "
                "도덕 기준 + 자기 제재 = 자기조절 기제(self-regulatory mechanism). "
                "2026-B Q5 ㉡ 빈칸 정답 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "bandura-moral-disengagement-2016",
            "related_terms": ["자기조절", "자기 승인", "자기 비난", "도덕 기준"],
        },
        {
            "id": "kw-bandura-self-efficacy",
            "term": "자기효능감",
            "term_en": "self-efficacy",
            "definition": (
                "특정한 상황에서 과제를 성공적으로 수행할 수 있다는 자기 자신의 능력에 대한 신념. "
                "반두라 평생 연구의 핵심 개념. "
                "『Self-Efficacy: The Exercise of Control(1997)』 제3장에서 4원천으로 정식화: "
                "① 실천 성취(enactive mastery experience), ② 대리적 경험(vicarious experience), "
                "③ 언어적 설득(verbal persuasion), ④ 생리적·정서적 상태. "
                "2014-A·2019-A·2025-B에 반복 출제."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "bandura-social-foundations-1986",
            "related_terms": ["4원천", "실천 성취", "대리적 경험", "언어적 설득"],
        },
        {
            "id": "kw-bandura-observational-learning",
            "term": "관찰학습",
            "term_en": "observational learning",
            "definition": (
                "직접 강화·처벌 없이도 모델의 행동과 그 결과를 관찰함으로써 "
                "관찰자의 행동 경향이 변화하는 학습 형태. "
                "반두라 『Social Learning Theory(1977)』의 기본 명제. "
                "1961·1963년 보보 인형 실험(Bobo doll experiment)에서 실험적으로 입증. "
                "주의·보존·운동 재생·동기의 4단계 인지 과정을 거친다. "
                "2019-A Q3의 이론적 배경."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "bandura-social-foundations-1986",
            "related_terms": ["사회학습이론", "보보 인형 실험", "모델링", "대리 강화"],
        },
        {
            "id": "kw-bandura-vicarious-reinforcement",
            "term": "대리 강화",
            "term_en": "vicarious reinforcement",
            "definition": (
                "강화의 한 유형. "
                "관찰자가 다른 사람(모델)의 행동이 강화되는 것을 봄으로써 "
                "관찰한 행동을 하려는 경향이 증가되는 현상. "
                "단순 관찰보다 모델의 행동이 강화되는 것을 관찰하는 것이 관찰자의 행동 경향을 "
                "더 효과적으로 증가시킨다. vicarious punishment와 쌍개념. "
                "2019-A Q3 빈칸 정답 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "bandura-social-foundations-1986",
            "related_terms": ["관찰학습", "사회학습이론", "vicarious punishment", "모델링"],
        },
        {
            "id": "kw-bandura-human-agency",
            "term": "행위 주체성",
            "term_en": "human agency",
            "definition": (
                "인간이 환경 자극의 수동적 반응자가 아니라 "
                "자신의 기능 수행과 행동에 대해 의도적 영향력을 행사하는 주체(agent)임을 나타내는 "
                "반두라 사회인지이론의 핵심 인간관. "
                "스키너의 급진적 행동주의·환경결정론 비판의 이론적 근거이며, "
                "도덕적 책임 귀속의 가능 조건이다. "
                "2026-B Q5 제시문 첫 trademark."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "bandura-social-foundations-1986",
            "related_terms": ["의도적 영향력", "도덕적 책임", "자기조절", "human agency"],
        },
        {
            "id": "kw-bandura-selective-activation",
            "term": "선택적 활성화",
            "term_en": "selective activation",
            "definition": (
                "자기 제재가 상황·맥락에 따라 선택적으로 작동하거나 비활성화되는 현상. "
                "동일한 도덕 기준을 지닌 사람들이 왜 상황에 따라 다른 도덕적 행동을 하는지 설명하는 "
                "반두라 도덕적 이탈 이론의 핵심 메커니즘. "
                "2026-B Q5 원문 구절 + 2014-A 기입형3 원문 구절에 직접 등장."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "bandura-moral-disengagement-2016",
            "related_terms": ["도덕적 이탈", "자기 제재", "자기조절", "심리사회적 기제"],
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
    """반두라 영향·비교 관계 데이터 입력.

    ES 등록 확인된 thinker_id만 링크 (2026-04-22 insert_*.py 존재 확인):
    - kohlberg : 등록 — 인지발달 도덕판단 vs 사회인지 자기조절 대립
    - blasi    : 등록 — 2024-B Q5 갑(블라시) vs 을(반두라) 대립 출제.
                 도덕적 정체성(자기 일관성) vs 도덕적 균형 계산 대립
    - hoffman  : 등록 — 도덕 심리학 정서 vs 사회인지 자기조절 비교
    """
    relations = [
        {
            "from_thinker": "blasi",
            "to_thinker": THINKER_ID,
            "type": "compared",
            "description": (
                "블라시(Augusto Blasi)의 도덕적 정체성 이론과 "
                "반두라(Albert Bandura)의 사회인지 도덕적 자기조절 이론은 "
                "'도덕적 일탈 행동'의 가능성에 대해 대립적 입장을 가진다. "
                "블라시는 도덕적 정체성이 강한 사람에게 중심 가치에 반하는 행동은 "
                "자기 일관성의 요구에서 선택 불가능한 것(unthinkable)이 된다고 본다. "
                "반면 반두라는 사람들이 도덕 행동의 누적 이력을 바탕으로 "
                "전체 정체성의 '최적 균형(optimal balance)'을 계산하여 "
                "일시적 도덕적 일탈을 선택할 수 있다고 본다. "
                "2024-B Q5는 갑(블라시)과 을(반두라)을 직접 대립 배치하여 "
                "도덕적 정체성 vs 도덕적 균형 계산의 구도를 출제하였다."
            ),
            "evidence": (
                "Blasi (2005) Moral Character: A Psychological Approach; "
                "Bandura (2016) Moral Disengagement; "
                "2024-B 전공B Q5 갑(블라시)·을(반두라) 제시문 대립 배치 "
                "(coverage/2024-B.md L196-L200·L228-L229)"
            ),
        },
        {
            "from_thinker": "kohlberg",
            "to_thinker": THINKER_ID,
            "type": "compared",
            "description": (
                "콜버그(Lawrence Kohlberg)의 인지발달 도덕판단 이론과 "
                "반두라(Albert Bandura)의 사회인지 도덕적 자기조절 이론은 "
                "도덕성의 원천과 판단-행동 간극의 해명 방식에서 대비된다. "
                "콜버그는 도덕 행동의 원천을 도덕 판단의 인지 구조(정의 원리)에서 찾으며, "
                "정서·사회학습을 전도덕적 요인으로 본다. "
                "반두라는 이에 반해 도덕 기준과 자기 제재의 결합으로 구성된 자기조절 기제, "
                "그리고 관찰학습·대리강화 같은 사회적 학습 기제가 "
                "도덕 행동을 실제로 변환·작동시킨다고 주장한다. "
                "2021-A Q6에서 블라시와 콜버그가 대립 배치되며 반두라의 사회학습이론이 "
                "비교 참조점으로 언급된다."
            ),
            "evidence": (
                "Kohlberg (1984) Essays on Moral Development Vol.2; "
                "Bandura (1986) Social Foundations of Thought and Action; "
                "coverage/2021-A.md L20 (콜버그-반두라 대비 언급)"
            ),
        },
        {
            "from_thinker": "hoffman",
            "to_thinker": THINKER_ID,
            "type": "compared",
            "description": (
                "호프만(Martin L. Hoffman)의 공감 기반 도덕 심리학과 "
                "반두라(Albert Bandura)의 사회인지 도덕 심리학은 "
                "도덕 행동의 정서적·인지적 기반에 대해 서로 다른 강조점을 가진다. "
                "호프만은 공감(empathy)과 공감적 고통·공감적 염려를 도덕 동기의 근본으로 삼으며 "
                "귀납적 훈육(inductive discipline)을 통한 내면화를 강조한다. "
                "반두라는 관찰학습·대리강화·자기조절 기제를 통해 도덕 행동을 설명하며, "
                "공감보다 인지·자기 제재·자기효능감의 매개를 핵심으로 삼는다. "
                "두 이론은 도덕 심리학 내에서 정서주의와 사회인지주의의 대표적 두 축을 이룬다."
            ),
            "evidence": (
                "Hoffman (2000) Empathy and Moral Development; "
                "Bandura (1986) Social Foundations of Thought and Action; "
                "Bandura (2016) Moral Disengagement"
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
    print("=== 앨버트 반두라(Bandura) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (bandura)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n[OK] 반두라 데이터 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}", file=sys.stderr)
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
