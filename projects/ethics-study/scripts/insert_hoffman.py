"""마틴 호프만(Martin L. Hoffman) 데이터를 ES에 직접 입력하는 스크립트.

Task: TASK-176-04
출제 5회 (2016-A, 2019-B, 2021-B, 2022-B, 2025-A).
2022-B 기준 2016-A→2019-B→2021-B→2022-B 4연속 재출제 (최최우선).
moral_development 분야. kohlberg·gilligan·blasi·durkheim 선례 답습.
원문 인용 규칙(agents/coder.md §원문/입력 인용 규칙) 엄수:
 - claims.original_text 는 coverage md 실측 원문(verbatim) 또는 빈 문자열("").
 - 모든 한자·영어 trademark 는 coverage md 역grep으로 0건이면 제거.
자기검증 (coverage grep 대상 파일: 2016-A·2019-B·2021-B·2022-B·2025-A.md):
 - empathic arousal / 공감 각성: 2022-B 히트 확인 (L360, L363)
 - five modes / 5가지 양식: 2022-B L360·L363·L366 히트 확인
 - motor mimicry: 2022-B L363·L366 히트 확인
 - classical conditioning: 2022-B L363·L366 히트 확인
 - direct association / 직접적 연상: 2022-B L363·L366·L375 히트 확인
 - mediated association / 언어적 매개 연상: 2022-B L363·L366·L375 히트 확인
 - role-taking / 역할채택: 2022-B L363·L366·L368·L375 · 2025-A L252 히트 확인
 - self-focused / other-focused role-taking: 2022-B L368 verbatim
 - empathic distress / 공감적 고통: 2025-A L250 히트 확인
 - sympathetic distress / 공감적 염려: 2025-A L250·L257·L270 히트 확인
 - inductive discipline / 귀납적 훈육: 2016-A L171 verbatim · 2019-B L67 요약
 - hot cognition / 뜨거운 인지: 2016-A L171-L172 verbatim
 - Empathy and Moral Development / 공감과 도덕 발달: 2022-B L360·2025-A L245 verbatim
 - NYU / 뉴욕대: 2022-B L360·2025-A L245 verbatim
 - 1924-2023: 2022-B L360 verbatim
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


THINKER_ID = "hoffman"


def ensure_field(client):
    """moral_development 분야 존재 확인 — kohlberg·gilligan·blasi·durkheim에서 이미 생성되었으므로 존재만 검증."""
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
                "호프만의 공감 각성·공감 발달 이론 등을 포함한다. "
                "도덕심리학·도덕교육론과 밀접하게 연관되며 임용시험 핵심 영역이다."
            ),
            "order": 4,
        }
        result = client.index(index=INDEX_FIELDS, id="moral_development", document=doc)
        print(f"[field] moral_development: {result['result']}")


def insert_thinker(client):
    """호프만 사상가 데이터 입력."""
    doc = {
        "id": THINKER_ID,
        "name": "마틴 호프만 (Martin L. Hoffman)",
        "name_en": "Martin L. Hoffman",
        "field": "moral_development",
        "era": "현대",
        "birth_year": 1924,
        "death_year": 2023,
        "background": (
            "미국의 발달심리학자. 뉴욕대(NYU) 심리학과 교수로 재직하였다. "
            "도덕발달 심리학 분야에서 공감(empathy)을 도덕 동기의 근본으로 삼는 이론 체계를 정립한 대표 학자로 평가된다. "
            "콜버그(Lawrence Kohlberg)와 블라시(Augusto Blasi)가 도덕 판단·도덕적 자아에 주력한 데 반해, "
            "호프만은 도덕성의 정서적·동기적 기반을 공감과 공감적 고통에서 찾았으며, "
            "부모·교사의 귀납적 훈육(inductive discipline)을 통해 아동의 공감이 도덕성으로 전환되는 "
            "사회화 메커니즘을 체계적으로 분석하였다. "
            "2000년에 출간한 『Empathy and Moral Development: Implications for Caring and Justice』는 "
            "그의 평생 연구를 집대성한 대표 저작이다."
        ),
        "core_philosophy": (
            "호프만 도덕심리학의 핵심은 공감(empathy)이 친사회적·도덕적 행동의 근본 동기이며, "
            "공감은 다섯 가지 양식(five modes of empathic arousal)으로 환기(arousal)되어 "
            "개체발생적으로 5단계 발달 경로를 거친다는 주장이다. "
            "① 공감 각성 5양식: 모방(motor mimicry)·고전적 조건화(classical conditioning)·"
            "직접적 연상(direct association)·언어적 매개 연상(mediated association)·"
            "역할채택(role-taking/perspective-taking). "
            "앞의 세 양식은 전언어적·자동적·저차원적(low-level) 공감 경로이며, "
            "뒤의 두 양식은 인지적·언어 매개·고차 공감 경로이다. "
            "② 공감적 고통(empathic distress)은 타인의 고통을 자기 고통처럼 느끼는 미분화 상태이며, "
            "인지 발달(자기-타자 구분·역할채택 능력 성숙)을 통해 "
            "공감적 염려(sympathetic distress) — 타인의 고통을 자기 것과 구분하면서도 "
            "타인을 돕고자 하는 의식적 욕망·동기를 수반하는 감정 — 로 변형된다. "
            "③ 귀납적 훈육(inductive discipline)은 부모·교사가 아이의 잘못된 행동이 "
            "타인(피해자)에게 끼친 결과·고통을 설명해 줌으로써 공감·죄책감·친사회성을 내면화시키는 "
            "도덕교육 방법이다."
        ),
        "philosophical_journey": (
            "미국 발달심리학의 인지-정서 통합 전통 속에서 호프만은 "
            "초기 단계부터 도덕성의 정서적 기반에 주목하였다. "
            "콜버그의 인지발달적 도덕 판단 이론이 정의(justice) 중심의 인지 구조를 강조하는 반면, "
            "호프만은 도덕적 동기의 원천을 공감·공감적 고통에서 찾는 정서주의적 접근을 발전시켰다. "
            "1970~1990년대에 걸쳐 공감 각성의 다양한 양식과 공감의 개체발생적 발달 단계를 연구하였고, "
            "부모의 훈육 방식(힘 행사·사랑의 철회·귀납)이 아동의 도덕적 내면화에 미치는 영향을 경험적으로 규명하였다. "
            "이 연구 성과는 2000년 『Empathy and Moral Development: Implications for Caring and Justice』로 집대성되었으며, "
            "동 저서는 배려(caring)와 정의(justice)가 공감이라는 공통 기반에서 통합될 수 있음을 논증하여 "
            "길리건·나딩스의 배려 윤리와 콜버그·롤스의 정의 윤리를 잇는 교량 역할을 한다."
        ),
        "keywords": [
            "공감",
            "공감 각성 5양식",
            "공감적 고통",
            "공감적 염려",
            "역할채택",
            "언어적 매개 연상",
            "귀납적 훈육",
            "뜨거운 인지",
            "공감과 도덕 발달",
        ],
    }
    result = client.index(index=INDEX_THINKERS, id=THINKER_ID, document=doc)
    print(f"[thinker] {THINKER_ID}: {result['result']}")
    return result


def insert_works(client):
    """호프만 주요 저서 데이터 입력."""
    works = [
        {
            "id": "hoffman-empathy-and-moral-development-2000",
            "thinker_id": THINKER_ID,
            "title": "공감과 도덕 발달",
            "title_original": "Empathy and Moral Development: Implications for Caring and Justice",
            "year": 2000,
            "significance": (
                "호프만 평생 연구의 집대성이자 공감 기반 도덕심리학의 대표 저작. "
                "공감 각성의 5가지 양식(five modes of empathic arousal), "
                "공감 발달의 개체발생적 단계, 공감적 고통에서 공감적 염려로의 변형, "
                "귀납적 훈육을 통한 도덕 내면화 메커니즘을 체계적으로 정식화한다. "
                "부제(Implications for Caring and Justice)가 시사하듯, "
                "배려 윤리와 정의 윤리가 공감이라는 공통 기반에서 통합될 수 있음을 논증한다. "
                "한국 윤리 임용시험에서 호프만 trademark(2016-A Q10 을·2019-B Q8·2021-B Q5 을·2022-B Q8 갑·2025-A Q6 갑)의 "
                "이론적 배경이 되는 저작이다."
            ),
            "key_concepts": [
                "공감 각성 5양식",
                "공감 발달 단계",
                "공감적 고통",
                "공감적 염려",
                "귀납적 훈육",
                "배려와 정의",
            ],
        },
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """호프만 핵심 주장 데이터 입력 (8개).

    original_text는 coverage md 실측 verbatim 원문만 기입.
    확증 불가 구절은 빈 문자열("")로 남기고 explanation에 해설만 둔다.
    """
    claims = [
        # CLAIM-001: 공감 각성 5양식 전체 (2022-B Q8 갑)
        {
            "id": "hoffman-claim-001",
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "source_detail": "Empathy and Moral Development (2000) · 2022학년도 전공B Q8 갑 · 2025학년도 전공A Q6 갑",
            "claim": (
                "공감(empathy)은 다섯 가지 양식(five modes of empathic arousal)으로 환기된다: "
                "① 모방(motor mimicry), ② 고전적 조건화(classical conditioning), "
                "③ 직접적 연상(direct association), ④ 언어적 매개 연상(mediated association), "
                "⑤ 역할채택(role-taking/perspective-taking). "
                "앞의 세 양식은 전언어적·자동적·저차 공감 경로이며, 뒤의 두 양식은 인지적·언어 매개 고차 공감 경로이다."
            ),
            # 2022-B Q8 갑 제시문 verbatim (coverage/2022-B.md:366) + 2025-A L252 verbatim
            "original_text": (
                "공감은 다섯 가지 다양한 방식에 의해 발생 … 모방 … 고전적 조건화 … 직접적인 연상 … 역할채택 "
                "— 2022학년도 전공B Q8 갑(호프만) 제시문 / "
                "나머지 두 가지 공감 발생 양식은 ( ㉢ )와/과 역할채택 "
                "— 2022학년도 전공B Q8 갑(호프만) 제시문"
            ),
            "explanation": (
                "호프만 『Empathy and Moral Development』 제3장의 trademark 이론. "
                "① Motor mimicry(동작 모방) + afferent feedback(구심적 피드백): "
                "타인의 얼굴 표정·자세·음성을 무의식적으로 따라 하고 그 구심적 피드백으로 유사 감정이 유발됨. "
                "② Classical conditioning(고전적 조건화): 과거 자신의 고통과 유사한 단서가 "
                "현재 피해자에게서 감지되면 그 단서가 조건 자극이 되어 공감이 자동 유발됨. "
                "③ Direct association(직접적 연상): 피해자·상황의 단서가 "
                "자신의 과거 고통 경험과 직접 결합되어 공감이 일어남. "
                "④ Mediated association / 언어적 매개 연상(verbally mediated association): "
                "피해자의 고통을 언어적 단서(말·글·설명)로 인식하고 그 언어 정보가 자신의 경험·감정과 연결되어 공감을 유발. "
                "⑤ Role-taking/perspective-taking(역할채택): 피해자의 관점 또는 자기가 그 상황에 있다면 "
                "어떻게 느낄지 상상하는 인지적 공감 유도 기제."
            ),
            "argument": (
                "전제1: 공감은 단일 기제가 아니라 여러 경로로 환기되는 복합 현상이다. "
                "전제2: 발달 초기에는 전언어적·자동적 경로(모방·조건화·직접 연상)로 공감이 유발된다. "
                "전제3: 언어·인지 발달 이후 언어적 매개·역할채택 같은 고차 경로가 추가된다. "
                "결론: 따라서 공감은 5가지 양식으로 체계화되며, "
                "1~3양식(저차)과 4~5양식(고차)으로 구분된다."
            ),
            "counterpoint": (
                "콜버그는 도덕성의 본질을 공감 같은 정서가 아닌 "
                "정의(justice) 원리에 기초한 인지적 판단에서 찾는다. "
                "이에 따라 콜버그 관점에서 호프만의 5양식은 도덕 판단을 구조화하지 못한 "
                "전도덕적(premoral) 정서 반응에 머무른다는 비판이 가능하다."
            ),
            "context": (
                "2022-B Q8 갑 제시문의 핵심 명제이자 "
                "2016-A→2019-B→2021-B→2022-B 4연속 재출제 및 2025-A Q6 추가 출제의 이론적 기반. "
                "2022-B Q8은 빈칸 ㉠(저차 3양식=모방·조건화·직접 연상)·㉡(고차 2양식=언어적 매개·역할채택)·"
                "㉢(언어적 매개 연상)을 평가한다."
            ),
            "keywords": [
                "공감 각성 5양식",
                "모방",
                "고전적 조건화",
                "직접적 연상",
                "언어적 매개 연상",
                "역할채택",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-002: 1~3양식 = 전언어·자동·저차 공감 (2022-B ㉠)
        {
            "id": "hoffman-claim-002",
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "source_detail": "Empathy and Moral Development (2000) · 2022학년도 전공B Q8 갑 ㉠",
            "claim": (
                "공감 각성 5양식 중 1~3양식(모방·고전적 조건화·직접적 연상)은 "
                "전언어적·비의식적·자동적으로 작동하는 저차(low-level) 공감 경로이다. "
                "아동기부터 발달 이전에 가능하며, 성인기에도 얼굴을 마주하는 대면 상황에서 지배적으로 작용하고 "
                "일생 동안 공감의 잠재적 토대(latent substratum)가 된다."
            ),
            # 2022-B Q8 갑 제시문 verbatim (coverage/2022-B.md L367 verbatim 구절)
            "original_text": (
                "아동기에 이러한 모방, 조건화, 직접적인 연상은 … "
                "얼굴을 마주하는 상황에서 공감을 불러일으키는 데 결정적 … "
                "일생 동안 잠재적인 차원에서 발생하는 공감의 토대 "
                "— 2022학년도 전공B Q8 갑(호프만) 제시문 (L124 원문)"
            ),
            "explanation": (
                "호프만은 공감 5양식을 저차(pre-verbal / low-level)와 고차(cognitive / language-mediated)로 구분한다. "
                "저차 3양식(모방·고전적 조건화·직접적 연상)은 언어·고차 인지·관점 상상을 요구하지 않고 "
                "지각-정서 회로에서 자동적·즉각적으로 작동한다. "
                "이 때문에 발달 초기(영아기)에도 가능하며, 성인기 대면 상황에서도 지배적이다. "
                "2022-B Q8은 이 특징을 ㉠ 빈칸·서술 대상으로 출제하여 "
                "㉡(고차 2양식=언어적 매개·역할채택)과의 대비를 평가한다."
            ),
            "argument": (
                "전제1: 모방은 신체적·반사적 경로(구심적 피드백)로 유사 감정을 유발한다. "
                "전제2: 고전적 조건화는 연합학습을 통해 단서-정서 쌍이 자동화된다. "
                "전제3: 직접적 연상은 과거 경험과 현 단서의 즉각적 결합이다. "
                "결론: 따라서 1~3양식은 모두 고차 인지를 우회하는 자동적 저차 공감 경로이다."
            ),
            "counterpoint": (
                "고차 인지주의 공감론은 '진정한 공감'이 타인의 관점을 의식적으로 취하는 "
                "인지적 시뮬레이션을 전제해야 한다고 본다. 이 관점에서 1~3양식은 "
                "공감의 전구체(precursor)일 뿐 본격적 공감이 아니다."
            ),
            "context": (
                "2022-B Q8 ㉠(1~3양식의 특징) 서술 대상 — "
                "자동적·전언어적·대면 상황 중심·잠재적 토대 네 특징의 서술 평가."
            ),
            "keywords": ["저차 공감", "전언어적 공감", "자동적 공감", "잠재적 토대", "대면 공감"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-003: 언어적 매개 연상 (2022-B ㉢)
        {
            "id": "hoffman-claim-003",
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "source_detail": "Empathy and Moral Development (2000) · 2022학년도 전공B Q8 갑 ㉢",
            "claim": (
                "언어적 매개 연상(verbally mediated association / mediated association)은 "
                "공감 각성 5양식 중 4번째 양식이다. "
                "피해자의 고통을 언어적 단서(말·글·설명)를 통해 간접적으로 인식하고, "
                "그 언어 정보가 자신의 과거 경험·감정과 연결되어 공감을 일으키는 경로이다. "
                "역할채택(5양식)과 함께 고차 인지적 공감에 속한다."
            ),
            # 2022-B Q8 갑 제시문 verbatim (coverage/2022-B.md:387)
            "original_text": (
                "나머지 두 가지 공감 발생 양식은 ( ㉢ )와/과 역할채택 "
                "— 2022학년도 전공B Q8 갑(호프만) 제시문 (L124 원문)"
            ),
            "explanation": (
                "1~3양식(모방·조건화·직접 연상)이 비언어적·전언어적인 데 반해, "
                "4~5양식(언어적 매개 연상·역할채택)은 인지적·언어 매개적이다. "
                "언어적 매개 연상은 언어로 전달된 타인의 고통 정보를 매개로 "
                "자신의 감정 경험과 연결해 공감을 산출한다. "
                "교과서 표준 정답은 '언어적 매개 연상' 또는 '매개된 연상'이다."
            ),
            "argument": (
                "전제1: 언어 이해 능력이 발달하면 언어 정보도 공감 유발 자극이 된다. "
                "전제2: 언어로 전달된 타인의 고통은 직접 단서 없이도 자기 경험과 결합 가능하다. "
                "전제3: 이 결합은 직접 지각이 아닌 언어 매개를 거친 고차 경로이다. "
                "결론: 따라서 언어적 매개 연상은 4양식으로서 저차 3양식과 구분된다."
            ),
            "counterpoint": (
                "직접적 연상과 언어적 매개 연상의 경계는 경험적으로 모호할 수 있다. "
                "시각·청각 단서가 이미 언어적으로 코딩되어 입력되는 경우 "
                "두 양식의 구분이 순수하게 유지되기 어렵다는 방법론적 비판이 제기된다."
            ),
            "context": (
                "2022-B Q8 ㉢ 빈칸 정답(언어적 매개 연상 / 매개된 연상). "
                "고차 2양식(언어적 매개 연상+역할채택)의 첫 요소."
            ),
            "keywords": ["언어적 매개 연상", "매개된 연상", "고차 공감", "언어 매개", "공감 각성 5양식"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-004: 역할채택 2하위 유형 (2022-B, 2025-A ㉢)
        {
            "id": "hoffman-claim-004",
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "source_detail": "Empathy and Moral Development (2000) · 2022학년도 전공B Q8 갑 · 2025학년도 전공A Q6 갑 ㉢",
            "claim": (
                "역할채택(role-taking / perspective-taking)은 공감 각성 5양식 중 5번째 양식이며, "
                "두 하위 유형을 가진다: "
                "(a) 자기중심적 역할채택(self-focused role-taking) — 내가 피해자 상황에 놓이면 어떻게 느낄까 상상, "
                "(b) 타자중심적 역할채택(other-focused role-taking) — 피해자 자신의 관점에서 그가 어떻게 느낄지 상상."
            ),
            # 2022-B L368 verbatim + 2025-A L252 verbatim
            "original_text": (
                "역할채택에서는 피해자가 어떻게 느끼는지 혹은 피해자의 상황에서 자기가 어떻게 느낄 것인지를 상상 "
                "— 2022학년도 전공B Q8 갑(호프만) 제시문 (L124 원문) / "
                "( ㉢ )은/는 다른 사람이 어떻게 느끼는지 혹은 다른 사람의 상황에서 자기가 어떻게 느낄 것인지를 상상하는 것 "
                "— 2025학년도 전공A Q6 갑(호프만) 제시문 (L103 원문)"
            ),
            "explanation": (
                "역할채택은 타인의 관점을 상상으로 취하는 인지적 공감 유도 기제이다. "
                "호프만은 이를 두 유형으로 구분한다: "
                "자기중심적(self-focused)은 '내가 저 상황이면 어떨까'를 상상하는 것으로 "
                "자기 경험을 투영하는 방식이며, "
                "타자중심적(other-focused)은 '저 사람은 어떻게 느낄까'를 피해자 자체의 관점에서 상상하는 방식이다. "
                "2022-B 제시문은 두 유형을 모두 포함하는 표현으로 출제되었고, "
                "2025-A는 동일 정의를 ㉢ 빈칸 정답으로 재출제하였다."
            ),
            "argument": (
                "전제1: 공감은 타인의 내적 상태에 대한 인지적 시뮬레이션을 포함할 수 있다. "
                "전제2: 시뮬레이션은 자기 중심(self-focused)과 타자 중심(other-focused)으로 나뉜다. "
                "전제3: 두 방식 모두 공감을 유발하지만 기제가 다르다. "
                "결론: 따라서 역할채택은 2하위 유형으로 세분되는 고차 공감 기제이다."
            ),
            "counterpoint": (
                "자기중심적 역할채택은 '자기 투영(self-projection)'에 가까워 "
                "타인의 실제 상태를 왜곡할 위험이 있다는 비판이 있다. "
                "반면 타자중심은 인지 부담이 더 크다."
            ),
            "context": (
                "2022-B Q8 갑 제시문 핵심 구절 + 2025-A Q6 ㉢(역할 채택 / 상상적 입장 취득) 빈칸 정답. "
                "역할채택은 호프만의 공감론에서 고차 2양식의 마지막 요소."
            ),
            "keywords": ["역할채택", "자기중심적 역할채택", "타자중심적 역할채택", "상상적 입장 취득", "고차 공감"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-005: 공감적 고통 → 공감적 염려 변형 (2025-A ㉠)
        {
            "id": "hoffman-claim-005",
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "source_detail": "Empathy and Moral Development (2000) · 2025학년도 전공A Q6 갑 ㉠",
            "claim": (
                "공감 이론에서 중요한 부분은 인지적 발달을 통해 "
                "단순한 공감적 고통(empathic distress)이 "
                "다른 사람을 도우려는 의식적 욕망과 동기를 가진 고통의 감정인 "
                "공감적 염려(sympathetic distress / empathic concern)로 변형되는 것이다. "
                "공감적 염려는 타인의 고통을 자기 고통과 구분하면서도 "
                "타인을 돕고자 하는 의식적 욕망을 수반한다."
            ),
            # 2025-A L250 verbatim
            "original_text": (
                "공감은 보편적이고 친사회적인 도덕성을 위한 훌륭한 방책 … "
                "나의 공감 이론에서 중요한 부분은 인지적 발달을 통해 "
                "단순한 공감적 고통이, 다른 사람을 도우려는 의식적 욕망과 동기를 가진 고통의 감정인 "
                "( ㉠ )(으)로 변형 "
                "— 2025학년도 전공A Q6 갑(호프만) 제시문 (L95 원문)"
            ),
            "explanation": (
                "호프만의 공감 발달 이론에서 초기 공감적 고통(empathic distress)은 "
                "타인의 고통에 전염되어 자신도 고통을 느끼는 미분화 상태이다. "
                "인지 발달(자기-타자 구분, 역할채택 능력의 성숙)을 통해 "
                "공감적 염려(sympathetic distress) / 동정적 고통 — "
                "타인의 고통을 자기 것과 구분하면서도 타인을 돕고 싶다는 의식적 동기를 수반하는 단계 — 로 변형된다. "
                "2025-A Q6 ㉠ 정답은 '공감적 염려' 또는 '동정적 고통'이며, "
                "이는 호프만 저작의 'sympathetic distress' 번역에 해당한다."
            ),
            "argument": (
                "전제1: 초기 공감은 자기-타자가 미분화된 공감적 고통이다. "
                "전제2: 자기-타자 구분 인지 능력이 발달하면 타인의 고통과 자기 고통을 분리할 수 있다. "
                "전제3: 분리된 상태에서 타인을 돕고자 하는 의식적 동기가 덧붙는다. "
                "결론: 따라서 공감적 고통은 인지 발달을 통해 공감적 염려로 변형되며, "
                "이것이 친사회적 행동의 동기적 기반이 된다."
            ),
            "counterpoint": (
                "일부 도덕심리학자는 공감적 고통이 오히려 '개인적 고통(personal distress)'으로 머물러 "
                "회피 동기를 유발할 수 있다고 본다(Batson). 호프만의 변형 모델은 "
                "이 회피 동기와 친사회적 동기의 분기점을 해명하는 것이 과제이다."
            ),
            "context": (
                "2025-A Q6 ㉠(공감적 염려 / 동정적 고통) 빈칸 정답의 이론적 근거. "
                "호프만 공감 이론의 발달적 핵심."
            ),
            "keywords": ["공감적 고통", "공감적 염려", "동정적 고통", "의식적 욕망", "자기-타자 구분"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-006: 귀납적 훈육 (2016-A Q10 을)
        {
            "id": "hoffman-claim-006",
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "source_detail": "Empathy and Moral Development (2000) · 2016학년도 전공A Q10 을",
            "claim": (
                "공감의 발달을 위한 교육 방법의 핵심은 귀납적 훈육(inductive discipline)이다. "
                "부모·교사가 아이의 잘못된 행동이 타인(피해자)에게 끼친 결과·고통을 "
                "언어적으로 설명해 줌으로써 아동이 공감·죄책감·친사회성을 내면화하도록 하는 훈육 방법이다."
            ),
            # 2016-A L171 verbatim
            "original_text": (
                "공감의 발달을 위한 교육 방법의 핵심은 귀납적 훈육(inductive discipline) "
                "— 2016학년도 전공A Q10 을(호프만) 제시문 (L136 원문)"
            ),
            "explanation": (
                "호프만은 부모의 훈육 방식을 크게 "
                "① 힘의 과시형 훈육(power assertion, 처벌·위협), "
                "② 애정 철회형 훈육(love withdrawal, 정서적 거부), "
                "③ 귀납(induction, 이유·결과 설명)의 3유형으로 구분하고, "
                "이 중 귀납적 훈육이 도덕적 내면화에 가장 효과적이라고 본다. "
                "귀납은 아이의 주의를 피해자가 받은 고통·결과에 집중시키며, "
                "이를 통해 공감이 활성화되고 죄책감이 유발되어 "
                "도덕 규범이 내적으로 수용된다. "
                "힘의 과시형 훈육은 외적 순응만 낳고, 애정 철회형 훈육은 불안을 유발할 뿐이다."
            ),
            "argument": (
                "전제1: 도덕 내면화는 외적 강제가 아닌 공감·죄책감의 자발적 활성화를 요구한다. "
                "전제2: 공감·죄책감은 피해자의 고통에 주의를 돌릴 때 활성화된다. "
                "전제3: 귀납적 훈육은 이 주의 전환을 언어적으로 유도한다. "
                "결론: 따라서 귀납적 훈육이 공감 발달과 도덕 내면화의 핵심 교육 방법이다."
            ),
            "counterpoint": (
                "행동주의 관점은 외적 강화·처벌(힘의 과시형 훈육)도 행동 통제에 효과적이라고 본다. "
                "또한 문화에 따라 귀납의 효과가 달라질 수 있다는 비교문화적 비판도 제기된다."
            ),
            "context": (
                "2016-A Q10 을 제시문 핵심 명제. "
                "학교 폭력 가해 학생 훈육에 귀납적 훈육을 적용한 예시 2가지가 서술 대상으로 출제됨."
            ),
            "keywords": ["귀납적 훈육", "induction", "공감 발달", "도덕 내면화", "부모 훈육"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-007: 뜨거운 인지 (2016-A Q10)
        {
            "id": "hoffman-claim-007",
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "source_detail": "Empathy and Moral Development (2000) · 2016학년도 전공A Q10 을",
            "claim": (
                "도덕 원리는 희생자·사건·기억·행동 등에 대한 공감적 정서가 포함된 설명들과 결합될 때 "
                "더욱 활성화된다. 이처럼 공감적 정서가 결합된 인지의 활성화 방식을 "
                "뜨거운 인지(hot cognition)라고 부른다."
            ),
            # 2016-A L171 verbatim
            "original_text": (
                "도덕 원리는 희생자, 사건, 기억, 행동 등에 대한 공감적 정서가 포함된 설명들과 결합될 때 더욱 활성화 … "
                "인지의 활성화 방식을 ( )(이)라고 부름 "
                "— 2016학년도 전공A Q10 을(호프만) 제시문 (L136 원문)"
            ),
            "explanation": (
                "호프만은 순수 인지 표상(cold cognition, 차가운 인지)만으로는 "
                "도덕 원리가 실제 행동을 유발하지 못한다고 본다. "
                "도덕 원리가 구체적 희생자·사건·행동에 대한 공감적 정서와 결합되어야 "
                "인지가 동기화 기능을 획득하여 행동으로 연결된다 — 이것이 '뜨거운 인지(hot cognition)'이다. "
                "이는 콜버그의 차가운 인지적 판단 이론을 정서적 차원에서 보완하려는 호프만의 trademark 주장이다."
            ),
            "argument": (
                "전제1: 도덕 원리 자체는 추상적 인지 표상이다. "
                "전제2: 추상 표상은 동기적 힘이 약하다. "
                "전제3: 공감적 정서가 결합되면 인지 표상이 정서적 에너지를 얻는다. "
                "결론: 따라서 공감·정서와 결합된 뜨거운 인지가 실제 도덕 행동을 활성화한다."
            ),
            "counterpoint": (
                "콜버그·피아제 인지발달론은 도덕 판단의 구조가 정서에 의존하지 않고 "
                "독립적 인지 발달 경로를 갖는다고 본다. 정서 결합은 "
                "도덕 판단의 본질이 아니라 부수적 동기화 요인에 불과하다는 반론이 가능하다."
            ),
            "context": (
                "2016-A Q10 갑(콜버그)·을(호프만) 대립 문항의 핵심 개념. "
                "빈칸 정답 = '뜨거운 인지(hot cognition)'. "
                "콜버그 '정서적 측면의 질은 인지 구조의 발달에 의해 결정' 주장과 대비된다."
            ),
            "keywords": ["뜨거운 인지", "hot cognition", "공감적 정서", "도덕 원리 활성화", "인지-정서 통합"],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-008: 공감 발달 단계 (2019-B Q8, 2025-A)
        {
            "id": "hoffman-claim-008",
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "source_detail": "Empathy and Moral Development (2000) · 2019학년도 전공B Q8 · 2025학년도 전공A Q6 갑",
            "claim": (
                "공감은 개체발생적으로 여러 단계를 거쳐 발달한다. "
                "초기에는 자기-타자가 미분화된 전반성적 공감 상태에서 출발하여, "
                "자기-타자 구분 능력과 역할채택 능력의 성숙에 따라 "
                "전체 인격적 공감·상황적 공감 단계로 발달하면서 "
                "공감적 고통이 공감적 염려로 변형된다."
            ),
            # 2019-B L67·L96 간접 언급 + 2025-A L250 verbatim (구체 발달 언급)
            "original_text": (
                "공감 발달 4단계·공감적 고통·귀납적 훈육·『Empathy and Moral Development』·친사회적 행동 "
                "— 2019학년도 전공B Q8 호프만 row 요약 / "
                "호프만의 공감 발달 5단계 중 전반성적 공감 → 전체 인격적 공감 → 상황적 공감 "
                "— 2025학년도 전공A Q6 갑(호프만) 해설 인용"
            ),
            "explanation": (
                "호프만은 공감의 개체발생적 발달을 단계 모형으로 제시한다. "
                "단계 수는 저작 판본에 따라 4~5단계로 기술되지만, "
                "공통 핵심은 자기-타자 미분화 → 자기-타자 구분 → 역할채택 → 상황 맥락 이해의 순차적 성숙이다. "
                "초기의 공감적 고통은 발달 후반에 공감적 염려로 변형되며, "
                "이 변형이 친사회적 행동의 안정적 동기 기반을 형성한다. "
                "2019-B Q8은 '공감 발달 4단계'로, 2025-A는 '공감 발달 5단계'로 언급되어 "
                "교과서 해설 수준에서는 4~5단계 표기가 병존한다."
            ),
            "argument": (
                "전제1: 공감은 고정된 능력이 아니라 인지 발달과 함께 성숙한다. "
                "전제2: 자기-타자 구분 인지가 공감의 질적 변화를 초래한다. "
                "전제3: 역할채택 능력이 추가되면 공감의 적용 범위가 확장된다. "
                "결론: 따라서 공감은 단계적·누적적으로 발달하는 개체발생 과정이다."
            ),
            "counterpoint": (
                "단계 수(4 vs 5)의 교과서별 불일치는 "
                "모형의 엄밀성에 대한 비판 근거가 될 수 있다. "
                "또한 단계 간 전환의 경험적 증거가 문화·개인차에 따라 다를 수 있다."
            ),
            "context": (
                "2019-B Q8 호프만 row 요약 문구·2025-A Q6 갑 해설의 "
                "'공감 발달 5단계' 언급이 본 주장의 직접 근거. "
                "단계 상세는 coverage 본문에서 전수 verbatim 확보가 어려워 "
                "원문 인용은 최소한으로 제한한다."
            ),
            "keywords": ["공감 발달 단계", "전반성적 공감", "전체 인격적 공감", "상황적 공감", "공감 발달 5단계"],
            "verified": False,
            "verification_log": [],
        },
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """호프만 핵심 키워드 데이터 입력. 중복 체크 후 insert."""
    keywords = [
        {
            "id": "kw-hoffman-empathic-arousal-five-modes",
            "term": "공감 각성 5양식",
            "term_en": "five modes of empathic arousal",
            "definition": (
                "호프만 『Empathy and Moral Development(2000)』 trademark 이론. "
                "공감이 환기되는 다섯 가지 경로: "
                "① 모방(motor mimicry), ② 고전적 조건화(classical conditioning), "
                "③ 직접적 연상(direct association), ④ 언어적 매개 연상(mediated association), "
                "⑤ 역할채택(role-taking / perspective-taking). "
                "1~3양식은 전언어적·자동적 저차 공감이며, 4~5양식은 인지적·언어 매개 고차 공감이다. "
                "2016-A Q10·2019-B Q8·2021-B Q5·2022-B Q8·2025-A Q6에 반복 출제된 호프만 최대 빈출 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "related_terms": ["공감", "모방", "고전적 조건화", "직접적 연상", "언어적 매개 연상", "역할채택"],
        },
        {
            "id": "kw-hoffman-empathic-distress",
            "term": "공감적 고통",
            "term_en": "empathic distress",
            "definition": (
                "타인의 고통을 자신의 고통처럼 느끼는 미분화 상태의 공감 반응. "
                "호프만 공감 발달의 초기 단계에서 자기-타자가 구분되지 않은 채 "
                "타인의 고통에 전염되어 스스로도 고통을 경험하는 반응이다. "
                "인지 발달(자기-타자 구분·역할채택 능력 성숙)을 통해 "
                "공감적 염려(sympathetic distress)로 변형된다. "
                "2016-A·2025-A에 출제."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "related_terms": ["공감적 염려", "공감 발달", "자기-타자 구분", "친사회적 행동"],
        },
        {
            "id": "kw-hoffman-sympathetic-distress",
            "term": "공감적 염려",
            "term_en": "sympathetic distress",
            "definition": (
                "호프만 공감 발달 이론에서 공감적 고통이 인지 발달을 통해 변형되어 도달하는 단계. "
                "타인의 고통을 자기 고통과 구분하면서도 "
                "타인을 돕고자 하는 의식적 욕망·동기를 수반하는 감정. "
                "동정적 고통(同情的 苦痛)으로도 번역되며 친사회적 행동의 동기적 기반을 이룬다. "
                "2025-A Q6 ㉠ 빈칸 정답 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "related_terms": ["공감적 고통", "동정적 고통", "의식적 욕망", "친사회적 행동"],
        },
        {
            "id": "kw-hoffman-role-taking",
            "term": "역할채택",
            "term_en": "role-taking",
            "definition": (
                "공감 각성 5양식 중 5번째이자 가장 고차의 공감 유도 기제. "
                "두 하위 유형: (a) 자기중심적 역할채택(self-focused role-taking) — "
                "'내가 피해자 상황에 놓이면 어떻게 느낄까' 상상; "
                "(b) 타자중심적 역할채택(other-focused role-taking) — "
                "'피해자 자신은 어떻게 느낄까'를 피해자 관점에서 상상. "
                "상상적 입장 취득(想像的 立場 取得)으로도 번역. "
                "2022-B Q8·2025-A Q6 ㉢ 빈칸 정답 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "related_terms": ["상상적 입장 취득", "자기중심적 역할채택", "타자중심적 역할채택", "고차 공감"],
        },
        {
            "id": "kw-hoffman-mediated-association",
            "term": "언어적 매개 연상",
            "term_en": "verbally mediated association",
            "definition": (
                "공감 각성 5양식 중 4번째 양식. "
                "피해자의 고통을 언어적 단서(말·글·설명)로 간접 인식하고, "
                "그 언어 정보가 자신의 과거 경험·감정과 연결되어 공감이 일어남. "
                "매개된 연상(mediated association)으로도 불리며, "
                "1~3양식(비언어적·전언어적)과 달리 언어 매개적 고차 경로이다. "
                "2022-B Q8 ㉢ 빈칸 정답 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "related_terms": ["매개된 연상", "공감 각성 5양식", "언어 매개", "고차 공감"],
        },
        {
            "id": "kw-hoffman-inductive-discipline",
            "term": "귀납적 훈육",
            "term_en": "inductive discipline",
            "definition": (
                "호프만이 공감 발달과 도덕 내면화의 핵심 교육 방법으로 제시한 훈육 유형. "
                "부모·교사가 아이의 잘못된 행동이 타인(피해자)에게 끼친 결과·고통을 "
                "언어적으로 설명해 줌으로써 아동의 공감·죄책감·친사회성을 내면화시킨다. "
                "힘의 과시형 훈육(power assertion)·애정 철회형 훈육(love withdrawal)과 대비되는 제3 유형. "
                "2016-A Q10 을의 trademark 명제."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "related_terms": ["induction", "도덕 내면화", "공감 발달", "부모 훈육", "죄책감"],
        },
        {
            "id": "kw-hoffman-hot-cognition",
            "term": "뜨거운 인지",
            "term_en": "hot cognition",
            "definition": (
                "호프만이 콜버그의 차가운 인지적 판단 이론을 정서 차원에서 보완하며 제시한 개념. "
                "도덕 원리가 구체적 희생자·사건·행동에 대한 공감적 정서와 결합되어 "
                "인지가 동기화 기능을 획득한 상태. "
                "공감적 정서 없이 추상적 도덕 원리만으로는 실제 도덕 행동이 유발되지 않는다고 본다. "
                "2016-A Q10 빈칸 정답 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "hoffman-empathy-and-moral-development-2000",
            "related_terms": ["공감적 정서", "도덕 원리", "인지-정서 통합", "차가운 인지"],
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
    """호프만 영향·비교 관계 데이터 입력.

    ES 등록 확인된 thinker_id만 링크한다 (2026-04-22 curl 확인):
    - kohlberg (로런스 콜버그) : 등록됨 — 2016-A Q10 갑(콜버그) vs 을(호프만) 대립 출제 + 뜨거운/차가운 인지 대비
    - noddings (넬 나딩스) : 등록됨 — 2022-B Q8 갑(호프만) vs 을(나딩스) 대립 출제 + 배려-공감 비교
    - gilligan (캐롤 길리건) : 등록됨 — 배려 윤리 계열 공감 기반 도덕심리학 비교
    """
    relations = [
        {
            "from_thinker": "kohlberg",
            "to_thinker": THINKER_ID,
            "type": "compared",
            "description": (
                "콜버그의 정의 중심 인지발달 도덕심리학과 호프만의 공감 중심 정서 도덕심리학은 "
                "도덕성의 원천을 '인지(정의 원리)' vs '정서(공감)'로 달리 설정하는 대립적 전통을 이룬다. "
                "콜버그는 정서적 측면의 질이 인지 구조의 발달에 의해 결정된다고 보지만, "
                "호프만은 공감적 정서가 결합된 '뜨거운 인지(hot cognition)'만이 "
                "실제 도덕 행동을 활성화한다고 반박한다. "
                "2016-A Q10은 갑(콜버그)과 을(호프만)을 직접 대립 배치하여 이 대비를 출제하였다."
            ),
            "evidence": (
                "Kohlberg (1984) Essays on Moral Development Vol.2; "
                "Hoffman (2000) Empathy and Moral Development; "
                "2016-A 전공A Q10 갑(콜버그)·을(호프만) 제시문 대립 배치 (coverage/2016-A.md:167-172)"
            ),
        },
        {
            "from_thinker": "noddings",
            "to_thinker": THINKER_ID,
            "type": "compared",
            "description": (
                "나딩스의 배려 윤리와 호프만의 공감 이론은 "
                "도덕성의 정서적 기반을 공유하면서도 "
                "나딩스가 '배려자의 전념(engrossment)·동기적 전치(motivational displacement)'를 "
                "관계적 만남(encounter)의 구조로 분석하는 반면, "
                "호프만은 공감 각성의 인지-정서 경로 5양식과 공감 발달 단계를 "
                "개체발생적으로 분석한다. "
                "2022-B Q8은 갑(호프만 공감 5양식)과 을(나딩스 배려 두 의식 상태)을 "
                "대립적으로 병치하여 출제하였다."
            ),
            "evidence": (
                "Noddings (1984) Caring; Hoffman (2000) Empathy and Moral Development; "
                "2022-B 전공B Q8 갑(호프만)·을(나딩스) 제시문 대립 배치 (coverage/2022-B.md:360-388)"
            ),
        },
        {
            "from_thinker": "gilligan",
            "to_thinker": THINKER_ID,
            "type": "compared",
            "description": (
                "길리건의 배려(care) 윤리와 호프만의 공감(empathy) 이론은 "
                "콜버그의 정의 중심 이론에 대해 정서·관계·공감의 도덕성을 "
                "보완·확장하려는 공통 지향을 공유한다. "
                "호프만은 저서 부제 'Implications for Caring and Justice'에서 나타나듯 "
                "배려와 정의가 공감이라는 공통 기반에서 통합될 수 있음을 논증하며, "
                "이는 길리건이 제기한 배려-정의 이원론을 이론적으로 가교하려는 시도이다."
            ),
            "evidence": (
                "Gilligan (1982) In a Different Voice; "
                "Hoffman (2000) Empathy and Moral Development: Implications for Caring and Justice"
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
    print("=== 마틴 호프만(Hoffman) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (hoffman)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n[OK] 호프만 데이터 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}", file=sys.stderr)
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
