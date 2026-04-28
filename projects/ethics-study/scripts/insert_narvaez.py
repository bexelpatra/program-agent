"""다르시아 나바에즈(Darcia Narvaez, 1952~) 데이터를 ES 에 직접 입력하는 스크립트.

Task: TASK-176-10 — TOP10 MISS 최종 10번째 등록.
공식 3회 출제 — 2016-A Q9 / 2024-A Q6 (나) / 2026-B Q4 (을).
BLK: BLK-175E-2016A-004 · BLK-175E-2024A-002 (2026-B Q4 갱신 포함 — 완전 해소 대상).
moral_development 분야(kohlberg · turiel · hoffman · haidt 동일 field 선등록 확인).

원문 인용 규칙(agents/coder.md §원문/입력 인용 규칙) 엄수:
 - claims.original_text 는 coverage md 실측 원문(verbatim) + 출처 주석.
 - 영어 병기 괄호 (Xxx) 는 coverage/*.md 역grep 1+ hit 확인된 것만 사용.
 - 스크립트 본문에 부정 키워드 5건 grep -c == 0 확증.

역grep 자기검증 (coverage 26파일, 저장 직전 실측):
 - "Darcia Narvaez"               →  9 hits / 3 files (HIT)
 - "Narvaez"                       → 다수 hits (2016-A · 2024-A · 2026-B 등)
 - "나바에즈"                      → 2016-A · 2024-A 다수 (canonical name 표기)
 - "나르바에즈"                    → 2026-B 다수 (대안 표기, 동일 인물)
 - "Triune Ethics"                 →  7 hits / 2 files (HIT — 삼원 윤리 이론)
 - "삼원 윤리 이론"                →  coverage 에서 반복 등장 (안전 키워드)
 - "안전 윤리"                     →  6 hits (2024-A L107 verbatim)
 - "관여 윤리"                     →  6 hits (2024-A L107 verbatim)
 - "상상 윤리"                     →  6 hits (2024-A L107 verbatim)
 - "통합적 윤리 교육"              →  5 hits (2016-A L122 verbatim, IEE)
 - "IEE"                           →  coverage 에 등장 (Integrative Ethical Education 약자)
 - "Integrative Ethical Education" →  coverage 에 등장
 - "윤리적 전문가"                 →  5 hits (2016-A L120 verbatim)
 - "ethical expert"                →  2016-A L23 + 해설 등 제한 사용
 - "4과정"                         →  12 hits (Four Process Model)
 - "Four Process Model"            →  coverage 에 등장
 - "7가지 윤리적 기술"             →  5 hits (2016-A L122 verbatim)
 - "4구성 요소"                    →  coverage 에 등장 (레스트)
 - "도덕 스키마"                   →  9 hits (2026-B L225 verbatim)
 - "moral schema"                  →  coverage 에 등장
 - "공동의 도덕성"                 → 10 hits (2026-B L226 verbatim)
 - "common morality"               →  coverage 에 등장 (2026-B L226 괄호 병기)
 - "신콜버그"                      → 23 hits (매우 안전)
 - "Neo-Kohlbergian"               →  coverage 에 등장
 - "이중 과정"                     →  5 hits (dual-process)
 - "dual-process"                  →  coverage 에 등장
 - (관여 궁박 영어 표기 제거됨 — coverage 0 hit 확인)
 - "관여 궁박"                     →  5 hits
 - "공감적 고통"                   → 19 hits
 - "노터데임"                      →  2 hits (2024-A, 다수파 표기)
 - "노트르담"                      →  1 hit  (2026-B, 소수 표기 — 동일 인물 소속)
 - "Neurobiology and the Development" →  2 hits (저서 제목)
 - "Postconventional Moral Thinking"   →  2 hits (저서 제목 · 1999 공저)
 - "Embodied Morality"             →  1 hit  (저서 제목 · 2016)
 - "삼원뇌"                        →  3 hits (Paul MacLean 삼원뇌)
 - "MacLean"                       →  2 hits
 - "파충류뇌"                      →  1 hit  (제한 사용)
 - "Paul MacLean"                  →  coverage 에 등장
 - "인습 이후"                     →  coverage 에 반복 등장
 - "postconventional"              →  coverage 에 반복 등장

부정 키워드 (TASK 지정 5+2 건 — 본문 grep -c == 0 판정 기준):
 [본 docstring 에 해당 문자열을 기재하지 않는다 — grep -c == 0 통과 목적으로 의도 생략]
 [규약: TASK 프롬프트 본문에 나열된 7건 (영어 4 + 한글 3) 는 본 파일 어디에도 등장 불가]

제한 사용 (1-3 hits — 본문 최소 사용):
 - "노터데임" 2, "노트르담" 1    → 각 1-2회만 (한글 표기 우선)
 - "Embodied Morality" 1         → 저서 목록에서 1회
 - "Postconventional Moral Thinking" 2 → 저서 목록·설명 2-3회
 - "Neurobiology and the Development of Human Morality" 2 → 저서 제목·설명 2-3회
 - "파충류뇌" 1                  → 삼원뇌 설명에서 1회
 - "MacLean"/"Paul MacLean" 2    → 삼원뇌 배경 설명에서 1-2회
 - "나르바에즈" (대안 표기)       → 2026-B 주표기이나 canonical name 은 "나바에즈" (한글 과반수)
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


THINKER_ID = "narvaez"


def ensure_field(client):
    """moral_development 분야 존재 확인.

    kohlberg · turiel · hoffman · haidt · blasi · gilligan 등이 동일 field 를 사용 중.
    이미 존재하는 경우 "이미 존재" 반환.
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
                "호프만의 공감 발달, 하이트 사회적 직관주의, "
                "그리고 나바에즈의 삼원 윤리 이론·통합적 윤리 교육 모델 등 "
                "현대 도덕 심리학 전반."
            ),
            "order": 10,
        }
        result = client.index(
            index=INDEX_FIELDS, id="moral_development", document=doc
        )
        print(f"[field] moral_development: {result['result']}")


def insert_thinker(client):
    """나바에즈 사상가 데이터 입력."""
    doc = {
        "id": THINKER_ID,
        "name": "나바에즈 (Darcia Narvaez)",
        "name_en": "Darcia Narvaez",
        "field": "moral_development",
        "era": "현대",
        "birth_year": 1952,
        "death_year": None,
        "background": (
            "1952년 출생의 미국 도덕 심리학자. "
            "미국 노터데임대(노트르담대) 심리학과 교수로 재직하며, "
            "레스트(James Rest)의 제자이자 신콜버그주의(Neo-Kohlbergian) 학파의 "
            "대표적 계승자·확장자로 자리한다. "
            "콜버그(Lawrence Kohlberg)의 인지발달 중심 도덕 판단 연구와 "
            "레스트의 4구성 요소 모델(Four Component Model)을 수용하면서도, "
            "도덕성의 기저에 자동적·직관적 인지 과정과 체화된 신경생리학적 기반이 "
            "놓여 있음을 강조한다. "
            "대표 저작 『Neurobiology and the Development of Human Morality(2014)』 에서 "
            "폴 맥린(Paul MacLean)의 삼원뇌(triune brain) 이론을 도덕 정향으로 확장하여 "
            "삼원 윤리 이론(Triune Ethics Theory)을 정립하였으며, "
            "『Postconventional Moral Thinking: A Neo-Kohlbergian Approach(1999, 레스트 공저)』 와 "
            "『Embodied Morality(2016)』 등을 통해 신콜버그주의의 이론적 지평을 넓혔다. "
            "도덕교육론 측면에서는 통합적 윤리 교육 모델(Integrative Ethical Education, IEE)을 제안하여, "
            "아동·학생을 윤리적 초보자에서 윤리적 전문가로 발달시키는 도덕 교육 목표와 "
            "4과정 모형·7가지 윤리적 기술로 구성된 교수 체계를 제시하였다. "
            "임용 도덕·윤리 시험에서 2016-A Q9·2024-A Q6 (나)·2026-B Q4 (을) "
            "3회 출제된 현대 도덕 심리학의 핵심 사상가이다."
        ),
        "core_philosophy": (
            "나바에즈 윤리학의 핵심은 도덕성이 의식적 추론만이 아니라 "
            "직관적·자동적 과정과 신경생리학적 기반 위에서 작동하는 "
            "통합적 체계라는 입장이다. "
            "삼원 윤리 이론(Triune Ethics Theory)에 따르면 도덕성의 근저에는 "
            "안전 윤리 · 관여 윤리 · 상상 윤리(ethic of imagination) 라는 "
            "세 가지 정향이 놓인다. "
            "안전 윤리는 자기 보존과 자기 이익에 초점을 둔 방어적 정향으로, "
            "삼원뇌 이론의 파충류뇌 단계에 대응한다. "
            "관여 윤리는 공감을 기초로 타인과 친밀한 관계를 형성하는 정향이며, "
            "두 양태로 나타난다 — 자기조절체계가 작동할 때는 사랑·배려·애착의 "
            "'매 순간을 사는 존재' 로 드러나고, 자기규제 시스템이 약할 때는 "
            "관여 궁박 (공감적 고통) 으로 전이된다. "
            "상상 윤리는 숙고적 이성 능력을 활용하여 안전 윤리의 충동과 관여 윤리의 직관에 "
            "반응하여 그것들을 조정하는 가장 모범적·성숙한 도덕 정향이다. "
            "또한 나바에즈는 레스트의 4구성 요소 모델을 4과정 모형(Four Process Model) 으로 재구성하고, "
            "각 과정마다 7가지 윤리적 기술을 제시하여 "
            "통합적 윤리 교육 모델(IEE) 의 교수·학습 체계를 정초하였다. "
            "인식론적으로는 도덕적 추론과 도덕적 직관의 이중 과정 이론(dual-process theory)을 수용하며, "
            "도덕 스키마(moral schema) 가 언어적 추론만이 아니라 직관적 인식을 통해서도 "
            "드러난다고 보아, 인습 이후 사고 수준에서 작동하는 도덕 스키마가 "
            "공동의 도덕성(common morality) 에 반영된다고 주장한다."
        ),
        "philosophical_journey": (
            "나바에즈는 레스트 문하에서 신콜버그주의 도덕 심리학의 계보를 이어받아 "
            "4구성 요소 모델의 이론적 확장을 수행하였다. "
            "초기 작업은 레스트와의 공저 『Postconventional Moral Thinking: A Neo-Kohlbergian Approach』(1999) 에서 "
            "콜버그 6단계를 도덕 스키마(개인 이익 · 규범 유지 · 인습 이후) 로 재구성하는 데 집중되었다. "
            "2000년대에 접어들면서 폴 맥린의 삼원뇌 이론을 도덕 영역으로 확장하는 시도로 "
            "삼원 윤리 이론(Triune Ethics Theory)을 정립하였으며, "
            "이는 2014년 『Neurobiology and the Development of Human Morality』 에서 "
            "신경생리학적 근거와 함께 체계화되었다. "
            "2016년 『Embodied Morality』 에서는 체화된 인지 관점을 도덕 발달론에 통합하였다. "
            "도덕교육론 측면에서는 통합적 윤리 교육 모델(IEE)을 제안하여 "
            "초보자-전문가 구도와 4과정 모형 · 7가지 윤리적 기술을 중심으로 "
            "교사의 교수·학습 과정과 학습 환경 조성의 과제를 정식화하였다. "
            "이 궤적을 통해 나바에즈는 콜버그·레스트가 남긴 인지 발달 중심의 도덕 판단 연구를 "
            "직관·자동적 처리·신경생리학·체화 인지·공동체 맥락으로 확장한 현대 신콜버그주의의 "
            "대표 계승자로 자리매김하였다."
        ),
        "keywords": [
            "삼원 윤리 이론",
            "안전 윤리",
            "관여 윤리",
            "상상 윤리",
            "통합적 윤리 교육 모델",
            "윤리적 전문가",
            "윤리적 초보자",
            "4과정 모형",
            "7가지 윤리적 기술",
            "도덕 스키마",
            "공동의 도덕성",
            "신콜버그주의",
            "이중 과정 이론",
            "관여 궁박",
        ],
    }
    result = client.index(index=INDEX_THINKERS, id=THINKER_ID, document=doc)
    print(f"[thinker] {THINKER_ID}: {result['result']}")
    return result


def insert_works(client):
    """나바에즈 주요 저서 데이터 입력."""
    works = [
        {
            "id": "narvaez-neurobiology-morality-2014",
            "thinker_id": THINKER_ID,
            "title": "인간 도덕성의 신경생리학과 발달",
            "title_original": "Neurobiology and the Development of Human Morality",
            "year": 2014,
            "significance": (
                "나바에즈가 삼원 윤리 이론(Triune Ethics Theory)을 "
                "신경생리학적 근거와 발달 심리학적 토대 위에서 체계화한 대표 저작. "
                "폴 맥린(Paul MacLean)의 삼원뇌(triune brain) 이론 "
                "— 파충류뇌(생존) · 포유류뇌(감정·관계) · 신피질(숙고) — "
                "을 도덕 정향으로 확장하여, "
                "안전 윤리 · 관여 윤리 · 상상 윤리 의 세 가지 도덕 정향을 "
                "근원적 인지·정서 체계와 연결 짓는다. "
                "임용 도덕·윤리 2024-A Q6 (나) 제시문의 직접 근거 저작이며, "
                "2026-B Q4 (을)의 '직관적·자동적 과정·도덕 스키마' 논의의 이론적 배경으로 참조된다."
            ),
            "key_concepts": [
                "삼원 윤리 이론",
                "안전 윤리",
                "관여 윤리",
                "상상 윤리",
                "삼원뇌",
                "신경생리학적 도덕성",
                "관여 궁박",
            ],
        },
        {
            "id": "narvaez-postconventional-moral-thinking-1999",
            "thinker_id": THINKER_ID,
            "title": "인습 이후 도덕 사고: 신콜버그적 접근",
            "title_original": "Postconventional Moral Thinking: A Neo-Kohlbergian Approach",
            "year": 1999,
            "significance": (
                "레스트(James Rest) 와의 공저. "
                "콜버그의 3수준 6단계 이론을 "
                "도덕 스키마(moral schema) 3 유형 — 개인 이익 · 규범 유지 · 인습 이후 — 으로 재구성하여 "
                "신콜버그주의(Neo-Kohlbergian) 학파의 이론적 토대를 마련한 저작. "
                "DIT(Defining Issues Test) 측정 도구의 이론적 배경을 제공하며, "
                "후속 연구에서 나바에즈가 도덕 스키마에 직관적·체화된 차원을 덧붙여 "
                "삼원 윤리 이론과 통합적 윤리 교육 모델로 확장하는 출발점이 된다. "
                "임용 도덕·윤리 2026-B Q4 (을) 제시문의 '인습 이후 사고 수준에서 작동하는 도덕 스키마 · "
                "공동의 도덕성' 논의의 직접 이론적 근거."
            ),
            "key_concepts": [
                "신콜버그주의",
                "도덕 스키마",
                "인습 이후 사고",
                "4구성 요소",
                "DIT",
            ],
        },
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """나바에즈 핵심 주장 데이터 입력.

    original_text 는 coverage md 실측 verbatim 원문 + 출처 주석.
    """
    claims = [
        # CLAIM-001: 삼원 윤리 이론 — 2024-A Q6 (나)
        {
            "id": "narvaez-claim-001",
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "source_detail": (
                "Neurobiology and the Development of Human Morality (2014) · "
                "2024학년도 전공A Q6 (나)"
            ),
            "claim": (
                "도덕성의 근저에 자리하는 세 가지 정향은 "
                "안전 윤리 · 관여 윤리 · 상상 윤리이다. "
                "삼원 윤리 이론(Triune Ethics Theory)은 "
                "삼원뇌 이론의 세 층위(파충류뇌 · 포유류뇌 · 신피질)에 대응하는 "
                "세 도덕 정향이 인간의 도덕적 행위를 근원적으로 구조화한다고 본다."
            ),
            # 2024-A.md L107 verbatim (L290 에서 재인용)
            "original_text": (
                "도덕성의 근저에 자리하는 세 가지 정향은 안전, 관여, 상상의 윤리 "
                "— 2024학년도 전공A Q6 (나) 제시문 (coverage/2024-A.md L107). "
                "해설 L290: '나바에즈 삼원 윤리 이론 trademark. "
                "Paul MacLean 의 삼원뇌 이론(파충류뇌=생존 / 포유류뇌=감정·관계 / 신피질=숙고)을 "
                "도덕 정향으로 확장'."
            ),
            "explanation": (
                "나바에즈 『Neurobiology and the Development of Human Morality(2014)』 의 trademark 명제. "
                "삼원 윤리 이론은 폴 맥린의 삼원뇌 이론을 도덕 영역으로 확장한 틀로, "
                "도덕성이 단일한 인지 체계가 아니라 "
                "세 층위의 신경생리학적·진화적 체계에 대응하는 "
                "세 가지 도덕 정향(안전 · 관여 · 상상)으로 구성된다고 본다. "
                "2024-A Q6 (나) ㉣ 정답 = 상상의 윤리(가장 모범적 도덕 정향)의 "
                "직접 이론 배경."
            ),
            "argument": (
                "전제1: 인간 뇌는 진화적으로 구분되는 세 층위(파충류뇌 · 포유류뇌 · 신피질)로 구성된다. "
                "전제2: 각 층위는 고유한 인지·정서 기능에 대응한다 — "
                "생존/반사 · 감정/관계 · 숙고/상상. "
                "전제3: 도덕성 또한 이 세 층위의 작동과 결합된 세 정향으로 분화된다. "
                "결론: 안전 · 관여 · 상상의 세 윤리 정향이 도덕적 행위의 근저에 있다."
            ),
            "counterpoint": (
                "콜버그·레스트 계열의 인지 발달·추론 중심 도덕심리학은 "
                "도덕 판단을 주로 의식적 추론 단계로 분석하며, "
                "신경생리학적 삼원 구도로 도덕성을 환원하는 데 거리를 둔다. "
                "또한 하이트의 도덕 기반 이론은 다섯 또는 여섯 기반을 제시하여 "
                "삼원 구조보다 더 다원적인 체계를 주장한다."
            ),
            "context": (
                "2024-A Q6 (나) 제시문의 첫 명제 · "
                "삼원 윤리 이론 trademark."
            ),
            "keywords": [
                "삼원 윤리 이론",
                "안전 윤리",
                "관여 윤리",
                "상상 윤리",
                "삼원뇌",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-002: 안전 윤리 — 2024-A Q6 (나) ㉠
        {
            "id": "narvaez-claim-002",
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "source_detail": (
                "Neurobiology and the Development of Human Morality (2014) · "
                "2024학년도 전공A Q6 (나) ㉠"
            ),
            "claim": (
                "안전 윤리는 자기 보존·자기 생존과 자기의 이익에 "
                "많은 초점을 두는 방어적 도덕 정향이다. "
                "삼원뇌 이론의 파충류뇌 단계에 대응하며, "
                "위협·위험·불확실성에 대한 반응성이 중심이 된다."
            ),
            # 2024-A.md L107 verbatim
            "original_text": (
                "안전 윤리는 ( ㉠ )와/과 자기의 이익에 많은 초점 "
                "— 2024학년도 전공A Q6 (나) 제시문 (coverage/2024-A.md L107). "
                "해설 L291: '㉠ = 자기(self) / 자기 자신. "
                "안전 윤리는 자기 보존 / 자기 생존과 자기 이익 추구 지향'."
            ),
            "explanation": (
                "나바에즈 삼원 윤리 이론의 첫 정향. "
                "안전 윤리는 생존과 자기 이익 보호에 초점을 두며, "
                "위협·위험에 대한 방어·도피·공격 반응을 도덕적 행위의 근저에서 조직한다. "
                "삼원뇌 중 가장 오래된 층위(파충류뇌)에 대응하며, "
                "불안·공포 등의 정서가 강하게 작동할 때 우세해진다. "
                "2024-A Q6 (나) ㉠ 정답 = 자기 (가 · 나 공통 변수)."
            ),
            "argument": (
                "전제1: 인간 행동의 근저에는 생존을 우선시하는 진화적 체계가 있다. "
                "전제2: 이 체계는 도덕적 상황에서 자기 보존·자기 이익을 기준으로 판단하게 한다. "
                "전제3: 따라서 도덕 정향의 하나로 자기 중심의 안전 지향이 분화된다. "
                "결론: 안전 윤리는 자기와 자기 이익에 초점을 맞춘 도덕 정향이다."
            ),
            "counterpoint": (
                "관여 윤리·상상 윤리 관점에서는 안전 윤리만이 지배할 때 "
                "타인에 대한 공감·배려와 미래 지향적 숙고가 제약된다고 본다. "
                "상상 윤리가 안전 윤리의 충동을 조정하는 것이 성숙한 도덕성의 과제."
            ),
            "context": (
                "2024-A Q6 (나) ㉠ 빈칸 정답의 직접 근거 · "
                "안전 윤리 규정 trademark."
            ),
            "keywords": [
                "안전 윤리",
                "자기 보존",
                "자기 이익",
                "파충류뇌",
                "방어적 정향",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-003: 관여 윤리·관여 궁박 — 2024-A Q6 (나) ㉢
        {
            "id": "narvaez-claim-003",
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "source_detail": (
                "Neurobiology and the Development of Human Morality (2014) · "
                "2024학년도 전공A Q6 (나) ㉢"
            ),
            "claim": (
                "관여 윤리는 공감을 기초로 타인과의 강력하고 "
                "친밀한 관계를 형성하는 도덕 정향이다. "
                "자기조절체계가 균형을 유지할 때는 사랑·배려·애착으로 드러나며, "
                "공감이 강하지만 자기조절 시스템이 약할 때는 "
                "관여 궁박 (공감적 고통)으로 전이된다."
            ),
            # 2024-A.md L107 verbatim
            "original_text": (
                "관여 윤리는 … 공감을 기초로 타인과의 강력하고 친밀한 관계 "
                "… 자기조절체계에 의해 두 가지 상태 … 하나는 … 사랑, 배려, 애착 … "
                "'매 순간을 사는 존재' 에 초점 "
                "… 다른 하나는 공감이 강하지만 자기 규제적 시스템이 약할 때 "
                "… 타인에 대한 넘치는 애착 혹은 배려로 인해 마음이 불편한 상태 "
                "— 2024학년도 전공A Q6 (나) 제시문 (coverage/2024-A.md L107). "
                "해설 L292-L294: '㉢ = 관여 궁박 / 관여 불편 / 공감적 고통 / 공감적 번민'."
            ),
            "explanation": (
                "나바에즈 삼원 윤리 이론의 두 번째 정향. "
                "관여 윤리는 공감을 기반으로 타인과 친밀한 관계를 형성하는 포유류뇌 층위의 정향이며, "
                "두 양태로 나타난다. "
                "(1) 자기조절체계가 작동하는 균형 상태에서는 사랑·배려·애착의 현재적 충실성으로 드러나고, "
                "(2) 자기규제 시스템이 약화된 상태에서는 타인에 대한 지나친 정서적 몰입이 "
                "자신의 고통으로 전이되는 관여 궁박 상태로 나타난다. "
                "2024-A Q6 (나) ㉢ 정답 = 관여 궁박 / 공감적 고통."
            ),
            "argument": (
                "전제1: 인간은 포유류뇌 층위의 정서·관계 체계를 통해 타인과 결속한다. "
                "전제2: 공감은 이 체계의 핵심 작동 양식으로 타인의 정서·복지에 대한 민감성을 형성한다. "
                "전제3: 그러나 자기조절이 약해지면 공감이 자신의 고통으로 과잉 전이될 수 있다. "
                "결론: 관여 윤리는 배려의 균형 상태와 관여 궁박의 비균형 상태라는 두 양태를 지닌다."
            ),
            "counterpoint": (
                "호프만(Martin Hoffman)의 공감 발달 이론은 공감적 고통을 발달 단계의 한 축으로 놓고 "
                "유도·귀납 훈육을 통한 공감의 조절·확장 경로를 제시한다. "
                "나바에즈는 이를 자기규제 시스템 약화 상황으로 재개념화한다."
            ),
            "context": (
                "2024-A Q6 (나) ㉢ 빈칸 정답의 직접 근거 · "
                "관여 윤리 이중 양태 trademark."
            ),
            "keywords": [
                "관여 윤리",
                "공감",
                "관여 궁박",
                "공감적 고통",
                "자기조절체계",
                "포유류뇌",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-004: 상상 윤리 — 2024-A Q6 (나) ㉣
        {
            "id": "narvaez-claim-004",
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "source_detail": (
                "Neurobiology and the Development of Human Morality (2014) · "
                "2024학년도 전공A Q6 (나) ㉣"
            ),
            "claim": (
                "상상 윤리(ethic of imagination)는 숙고적 이성 능력을 활용하여 "
                "안전 윤리의 충동과 관여 윤리의 직관에 반응하여 그것들을 조정하는 정향이다. "
                "삼원뇌의 신피질 층위에 대응하며, 세 정향 가운데 가장 성숙한 도덕 정향으로 평가된다."
            ),
            # 2024-A.md L107 verbatim
            "original_text": (
                "상상 윤리는 숙고적 이성 능력을 활용하여 안전 윤리의 충동과 관여 윤리의 직관에 "
                "반응하여 그것들을 조정 … 가장 모범적인 도덕적 정향은 ( ㉣ ) "
                "— 2024학년도 전공A Q6 (나) 제시문 (coverage/2024-A.md L107). "
                "해설 L295: '㉣ = 상상의 윤리 / 상상 윤리'."
            ),
            "explanation": (
                "나바에즈 삼원 윤리 이론의 세 번째 정향이자 가장 성숙한 도덕 정향. "
                "상상 윤리는 신피질 기반의 숙고적 이성으로 "
                "안전 윤리의 충동(생존·방어 반응)과 관여 윤리의 직관(공감·관계)에 반응하여 "
                "양자를 조정·통합한다. "
                "과거·현재·미래를 포괄하는 상상력과 타자·공동체 지향을 결합하여 "
                "도덕적 판단을 확장된 지평에서 수행하는 능력. "
                "2024-A Q6 (나) ㉣ 정답 = 상상의 윤리."
            ),
            "argument": (
                "전제1: 안전 윤리는 충동적 · 자기 중심적, 관여 윤리는 직관적 · 관계 중심적이다. "
                "전제2: 성숙한 도덕성은 두 정향을 균형 있게 조정하고 확장할 수 있어야 한다. "
                "전제3: 숙고적 이성 능력은 신피질 층위에서 상상·미래 지향·타자 지향으로 작동한다. "
                "결론: 상상 윤리가 안전·관여 정향을 조정하는 가장 모범적 도덕 정향이다."
            ),
            "counterpoint": (
                "이성주의적 단계 이론(콜버그)은 추론 능력 자체의 발달을 성숙의 핵심으로 보아 "
                "'상상' 이라는 개념으로 도덕의 최고 정향을 규정하는 데 거리를 둔다."
            ),
            "context": (
                "2024-A Q6 (나) ㉣ 서술형 답안의 직접 근거 · "
                "상상 윤리 trademark."
            ),
            "keywords": [
                "상상 윤리",
                "숙고적 이성",
                "신피질",
                "정향 조정",
                "성숙한 도덕성",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-005: 통합적 윤리 교육 모델 · 윤리적 전문가 — 2016-A Q9
        {
            "id": "narvaez-claim-005",
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "source_detail": (
                "Integrative Ethical Education(IEE) 도덕교육 모델 · "
                "2016학년도 전공A Q9"
            ),
            "claim": (
                "통합적 윤리 교육 모델(Integrative Ethical Education, IEE)은 "
                "학생을 윤리적 초보자에서 윤리적 전문가(ethical expert)로 발달시키는 "
                "도덕 교육 틀이다. "
                "교사는 먼저 자신이 윤리적 전문가가 된 뒤 학생들을 전문가로 양성하기 위해 "
                "교수·학습 과정에서 학습 내용과 학습 환경 등 여러 축에 걸친 중점 사항을 "
                "체계적으로 설계해야 한다."
            ),
            # 2016-A.md L120 · L122 verbatim
            "original_text": (
                "이제 도덕교육에서도 도덕적 추론과 도덕적 직관 모두에 관심을 기울여야 합니다. "
                "… 우리가 먼저 초보자가 아닌 (윤리적 전문가)이/가 되고, "
                "여기에 기초하여 학생들을 (윤리적 전문가)(으)로 양성하기 위해 노력해야 합니다 "
                "— 2016학년도 전공A Q9 제시문 (coverage/2016-A.md L120). "
                "'통합적 윤리 교육 모델' 을 강조한 나바에즈(D. Narvaez)는 "
                "학생들을 (윤리적 전문가)(으)로 양성하기 위해 교사가 교수·학습 과정에서 "
                "중점을 두어야 하는 몇 가지 사항에 대해서 언급했습니다 "
                "(coverage/2016-A.md L122)."
            ),
            "explanation": (
                "나바에즈 통합적 윤리 교육 모델(IEE) trademark. "
                "IEE 는 도덕성 발달을 윤리 기술의 점진적 숙달로 파악하며, "
                "교사의 과제는 풍부한 보살핌의 분위기 조성(학습 환경 축)과 "
                "윤리 기술에 직접 초점을 맞춘 교수(학습 내용 축) 등을 통해 "
                "학생이 윤리적 초보자에서 윤리적 전문가로 발달하도록 돕는 것이다. "
                "2016-A Q9 정답 = 윤리적 전문가 · "
                "학습 내용 및 환경 관련 중점 사항 2가지 서술."
            ),
            "argument": (
                "전제1: 도덕성 발달은 도덕적 추론뿐 아니라 도덕적 직관까지 포함하는 "
                "기술의 숙달 과정으로 이해되어야 한다. "
                "전제2: 숙달은 초보자 단계에서 전문가 단계로의 점진적 이행을 거친다. "
                "전제3: 교사가 전문가 상태에 도달하지 못하면 학생을 전문가로 양성하기 어렵다. "
                "결론: 도덕 교육의 목표는 교사·학생 모두를 윤리적 전문가로 기르는 "
                "통합적 윤리 교육 체계의 구축이다."
            ),
            "counterpoint": (
                "가치 명료화 계열은 학생 개인의 가치 선택 과정을 중시하여 "
                "'전문가 발달 모델' 의 외재적 목표 설정에 거리를 두고, "
                "콜버그 정의공동체 접근은 공동체 규범·분위기 조성을 중심에 둔다."
            ),
            "context": (
                "2016-A Q9 빈칸 정답(윤리적 전문가) 의 직접 근거 · "
                "통합적 윤리 교육 모델 trademark."
            ),
            "keywords": [
                "통합적 윤리 교육 모델",
                "IEE",
                "윤리적 전문가",
                "윤리적 초보자",
                "도덕 교육",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-006: 4과정 모형·7가지 윤리적 기술 — 2016-A Q9
        {
            "id": "narvaez-claim-006",
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "source_detail": (
                "Integrative Ethical Education(IEE) 도덕교육 모델 · "
                "2016학년도 전공A Q9"
            ),
            "claim": (
                "좋은 인격을 갖춘 사람의 특징을 4과정 모형(Four Process Model)으로 제안하고, "
                "각 과정마다 7가지 윤리적 기술을 제시한다. "
                "4과정은 레스트(James Rest) 의 4구성 요소 모델 "
                "— 윤리적 민감성 · 윤리적 판단 · 윤리적 초점(동기) · 윤리적 행동 — 을 계승·재구성한 것이다."
            ),
            # 2016-A.md L122 verbatim
            "original_text": (
                "좋은 인격을 갖춘 사람의 특징과 관련해 4과정 모형을 제안하고, "
                "각 과정마다 7가지 윤리적 기술들을 제시하였습니다 "
                "— 2016학년도 전공A Q9 제시문 (coverage/2016-A.md L122). "
                "해설: '나바에즈의 4×7=28 ethical skills 체계' (coverage/2016-A.md L23)."
            ),
            "explanation": (
                "나바에즈 IEE 의 교수 체계 trademark. "
                "4과정 모형(Four Process Model)은 레스트의 4구성 요소 모델 "
                "(윤리적 민감성 · 판단 · 초점 · 행동) 을 계승·재구성한 것으로, "
                "각 과정마다 7가지 윤리적 기술을 제시하여 "
                "총 4×7 = 28 개의 윤리 기술 체계를 구성한다. "
                "학생들은 학년·발달 단계에 맞추어 각 기술을 반복 연습함으로써 "
                "윤리적 전문가로 발달한다. "
                "2016-A Q9 제시문의 직접 근거 구절."
            ),
            "argument": (
                "전제1: 도덕적 행위는 민감성·판단·초점·행동이라는 별개의 심리적 과정을 요구한다 (레스트 모델 계승). "
                "전제2: 각 과정은 고유한 윤리적 기술들의 집합으로 구성된다. "
                "전제3: 구체적 기술은 학년·발달 단계에 맞춘 반복 연습으로 숙달된다. "
                "결론: 4과정 모형과 각 7가지 윤리 기술의 체계적 교수가 도덕 교육의 구체 방법이다."
            ),
            "counterpoint": (
                "인지발달 단계론(콜버그)은 단계 자체의 발달을 핵심에 두어 "
                "'기술 목록' 중심 접근을 행동주의적이라고 비판할 수 있다. "
                "나바에즈는 자동화된 숙달이 이중 과정 이론에 정합적이라고 응수한다."
            ),
            "context": (
                "2016-A Q9 제시문의 직접 구절 · "
                "4과정 모형 · 7기술 체계 trademark."
            ),
            "keywords": [
                "4과정 모형",
                "7가지 윤리적 기술",
                "4구성 요소",
                "윤리 기술 체계",
                "레스트 계승",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-007: 도덕 스키마 · 직관적·자동적 과정 — 2026-B Q4 (을)
        {
            "id": "narvaez-claim-007",
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-postconventional-moral-thinking-1999",
            "source_detail": (
                "Postconventional Moral Thinking: A Neo-Kohlbergian Approach (1999, 레스트 공저) · "
                "2026학년도 전공B Q4 (을) ㉢"
            ),
            "claim": (
                "도덕 스키마(moral schema)는 형식뿐만 아니라 내용도 포함하고 있으며, "
                "언어를 통한 명료한 표현보다는 직관적 인식을 통해 드러나는 경향이 있다. "
                "이중 과정 이론(dual-process theory)에 따르면 "
                "도덕적 인지의 상당 부분은 직관적·자동적 과정을 거친다."
            ),
            # 2026-B.md L225 verbatim
            "original_text": (
                "우리 인지 활동의 상당 부분이 이와 같지 않으며 "
                "오히려 ( ㉢ )이고 자동적인 과정을 거친다는 데 있다. "
                "단계를 통한 발달은 추론의 형식만을 고려하고 있다. "
                "그러나 도덕 스키마는 형식뿐만 아니라 내용도 포함하고 있으며, "
                "언어를 통한 명료한 표현보다는 ( ㉢ ) 인식을 통해 드러나는 경향이 있다 "
                "— 2026학년도 전공B Q4 (을) 제시문 (coverage/2026-B.md L225). "
                "해설 L224: '나르바에즈 직관·자동적 처리(intuitive, automatic processing) trademark'."
            ),
            "explanation": (
                "나바에즈 신콜버그주의 확장의 핵심 명제. "
                "콜버그·레스트가 중시한 명시적 도덕 추론(현상주의 가정)만으로는 "
                "도덕적 인지의 상당 부분을 설명할 수 없으며, "
                "도덕 스키마는 추론의 형식에 그치지 않고 내용까지 포함하면서 "
                "직관적·자동적 과정을 통해 드러난다. "
                "2026-B Q4 (을) ㉢ 정답 = 직관(直觀 — intuitive) · "
                "하이트의 사회직관주의와는 다른 신콜버그주의 내부의 이중 과정 수용."
            ),
            "argument": (
                "전제1: 콜버그 단계론의 현상주의 가정은 '의식적이고 명시적이며 특별한 노력이 요구되는 인지' 만 고려한다. "
                "전제2: 그러나 일상적 도덕 인지의 상당 부분은 자동적·직관적으로 이뤄진다. "
                "전제3: 도덕 스키마는 추론 형식뿐 아니라 내용까지 포함하며 직관 인식을 통해 드러난다. "
                "결론: 신콜버그주의는 추론과 직관을 모두 포함하는 이중 과정 틀로 확장되어야 한다."
            ),
            "counterpoint": (
                "콜버그 원형(현상주의 가정)에 충실한 입장은 의식적 추론의 단계적 구조가 "
                "도덕 발달의 핵심이며, 자동적·직관적 과정은 도덕성이라기보다 "
                "정서적 반응에 가깝다고 본다."
            ),
            "context": (
                "2026-B Q4 (을) ㉢ 정답(직관) 의 직접 근거 · "
                "도덕 스키마 + 이중 과정 이론 trademark."
            ),
            "keywords": [
                "도덕 스키마",
                "직관",
                "자동적 과정",
                "이중 과정 이론",
                "신콜버그주의",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-008: 공동의 도덕성 · 공동체 맥락 — 2026-B Q4 (을) ㉣
        {
            "id": "narvaez-claim-008",
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-postconventional-moral-thinking-1999",
            "source_detail": (
                "Postconventional Moral Thinking: A Neo-Kohlbergian Approach (1999) · "
                "2026학년도 전공B Q4 (을) ㉣"
            ),
            "claim": (
                "인습 이후 사고 수준에서 작동하는 도덕 스키마는 공유된 이상에 기반하며, "
                "이것은 공동의 도덕성(common morality)에 반영되어 있다. "
                "형식과 내용 모두를 포함하는 공동의 도덕성은 "
                "도덕적 논의와 열린 토론을 통해 형성되며, "
                "공동체의 맥락과 집단적 숙고가 온전히 스며 있는 상태이다."
            ),
            # 2026-B.md L226 verbatim
            "original_text": (
                "인습 이후 사고 수준에서 작동하는 도덕 스키마는 공유된 이상에 기반하며, "
                "이것은 ㉣ 공동의 도덕성(common morality) 에 반영되어 있다. "
                "형식과 내용 모두를 포함하고 있는 공동의 도덕성은 "
                "도덕적 논의와 열린 토론을 통해 형성되며, "
                "공동체의 맥락과 집단적 숙고가 온전히 스며 있는 상태이다 "
                "— 2026학년도 전공B Q4 (을) 제시문 (coverage/2026-B.md L226)."
            ),
            "explanation": (
                "나바에즈 신콜버그주의의 공동체주의적·맥락주의적 확장. "
                "인습 이후(postconventional) 사고 수준의 도덕 스키마는 "
                "고립된 개인의 명시적 추론이 아니라 "
                "공유된 도덕적 이상을 기반으로 하며, "
                "이 공유된 이상은 공동의 도덕성으로 귀결된다. "
                "공동의 도덕성은 도덕적 논의 · 열린 토론 · 공동체 맥락 · 집단적 숙고가 "
                "복합적으로 작동한 결과로 형성되며, "
                "콜버그의 '개인의 보편화 가능한 도덕 원리' 와 구별되는 "
                "사회적·맥락적 차원을 지닌다. "
                "2026-B Q4 (을) ㉣ 서술의 비교 축 — "
                "콜버그 ㉡(추론으로 도달) ↔ 나바에즈 ㉣(직관·토론·공동체로 형성)."
            ),
            "argument": (
                "전제1: 인습 이후 수준의 도덕 스키마는 공유된 이상을 기반으로 한다. "
                "전제2: 공유된 이상은 개인 추론이 아니라 공동체의 논의·토론·숙고에서 형성된다. "
                "전제3: 이 공동체적 형성 과정에 직관적·체화된 인식이 함께 작동한다. "
                "결론: 공동의 도덕성은 형식과 내용을 모두 포함하며 공동체 맥락에 의해 구성된다."
            ),
            "counterpoint": (
                "콜버그 정의공동체 접근은 "
                "공동체 맥락의 중요성을 인정하면서도 "
                "궁극적으로 개인의 후인습 단계 추론 능력이 도덕 발달의 종착점임을 고수한다. "
                "또한 하버마스의 담론윤리는 '이상적 담화 상황' 의 형식적 조건을 "
                "도덕적 정당성의 근거로 삼는 점에서 공동체의 실질적 맥락에 덜 의존한다."
            ),
            "context": (
                "2026-B Q4 (을) ㉣ 공동의 도덕성 서술의 직접 근거 · "
                "나바에즈 공동체 맥락 확장 trademark."
            ),
            "keywords": [
                "공동의 도덕성",
                "인습 이후 사고",
                "열린 토론",
                "집단적 숙고",
                "공동체 맥락",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-009: 신콜버그주의 — 전반 맥락
        {
            "id": "narvaez-claim-009",
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-postconventional-moral-thinking-1999",
            "source_detail": (
                "Postconventional Moral Thinking: A Neo-Kohlbergian Approach (1999) · "
                "2024학년도 전공A · 2026학년도 전공B Q4 전반"
            ),
            "claim": (
                "나바에즈는 신콜버그주의(Neo-Kohlbergian) 학파의 대표 계승자로, "
                "콜버그 3수준 6단계를 도덕 스키마 3 유형 "
                "— 개인 이익 · 규범 유지 · 인습 이후 — 로 재구성하고, "
                "여기에 직관·자동적 처리·체화 인지·신경생리학적 기반을 덧붙여 "
                "현대 도덕 심리학의 이론적 지평을 확장한다."
            ),
            # 2026-B.md L223 · L230 verbatim
            "original_text": (
                "나르바에즈(Darcia Narvaez, 1955-, 미국 노트르담대 도덕심리학자, 레스트 제자, "
                "『Postconventional Moral Thinking: A Neo-Kohlbergian Approach(1999, 공저)』 … "
                "신콜버그주의 도덕 스키마·직관·삼원윤리이론 정초) "
                "— 2026학년도 전공B Q4 (을) 해설 (coverage/2026-B.md L223). "
                "'레스트는 1999년 타계 후 신콜버그주의를 이어가는 후계자가 "
                "나르바에즈·베브와(Bebeau)·투마(Thoma)이며, "
                "도덕 스키마를 ‘형식+내용 + 직관적 차원’ 으로 확장한 것은 "
                "나르바에즈의 특색' (coverage/2026-B.md L230)."
            ),
            "explanation": (
                "나바에즈의 이론적 자리매김. "
                "콜버그 원형은 3수준 6단계의 추론 발달이었으나, "
                "레스트는 이를 도덕 스키마 3 유형으로 재편하여 DIT 측정 도구와 결합하였고, "
                "나바에즈는 레스트를 계승하면서 도덕 스키마에 "
                "직관·자동적 처리·체화 인지·신경생리학 기반(삼원 윤리 이론)을 덧붙여 "
                "신콜버그주의를 확장하였다. "
                "2024-A·2026-B 두 해 출제에서 나바에즈의 이론적 위치가 모두 이 계보로 제시된다."
            ),
            "argument": (
                "전제1: 콜버그 6단계 이론은 인습 이후 수준의 보편 도덕 원리 추론을 정점으로 둔다. "
                "전제2: 레스트는 이를 도덕 스키마 3 유형으로 재구성하여 측정 가능하게 하였다. "
                "전제3: 나바에즈는 이 3 유형에 직관·체화·공동체 맥락·신경생리학적 기반을 덧붙였다. "
                "결론: 나바에즈는 신콜버그주의의 대표 계승자로서 도덕 심리학의 다차원적 확장을 이끈다."
            ),
            "counterpoint": (
                "하이트의 사회직관주의는 콜버그·신콜버그 계보 전체와 단절을 선언하며 "
                "도덕 판단의 기원을 도덕 기반(moral foundations) 의 자동적 활성화로 설명한다. "
                "나바에즈는 양 진영의 핵심 통찰을 수용하되 신콜버그 계보 안에서 통합을 도모한다."
            ),
            "context": (
                "2024-A Q6 (나) · 2026-B Q4 (을) 두 해 출제의 공통 배경 · "
                "신콜버그주의 계보 trademark."
            ),
            "keywords": [
                "신콜버그주의",
                "레스트 계승",
                "도덕 스키마",
                "DIT",
                "체화 인지",
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
    """나바에즈 핵심 키워드 데이터 입력. 중복 체크 후 insert."""
    keywords = [
        {
            "id": "kw-narvaez-triune-ethics-theory",
            "term": "삼원 윤리 이론",
            "term_en": "Triune Ethics Theory",
            "definition": (
                "나바에즈 『Neurobiology and the Development of Human Morality(2014)』 trademark. "
                "폴 맥린(Paul MacLean)의 삼원뇌(triune brain) 이론 "
                "— 파충류뇌 · 포유류뇌 · 신피질 — 을 도덕 정향으로 확장하여 "
                "안전 윤리 · 관여 윤리 · 상상 윤리 라는 세 도덕 정향을 제시하는 이론. "
                "2024학년도 전공A Q6 (나) 제시문의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "related_terms": [
                "안전 윤리",
                "관여 윤리",
                "상상 윤리",
                "삼원뇌",
                "신경생리학적 도덕성",
            ],
        },
        {
            "id": "kw-narvaez-safety-ethic",
            "term": "안전 윤리",
            "term_en": "",
            "definition": (
                "나바에즈 삼원 윤리 이론의 첫 정향. "
                "자기 보존 · 자기 생존과 자기 이익에 많은 초점을 두는 방어적 도덕 정향이며, "
                "삼원뇌의 파충류뇌 층위에 대응한다. "
                "위협·위험·불확실성에 대한 반응성이 중심이 되는 정향. "
                "2024-A Q6 (나) ㉠ 정답(자기) 의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "related_terms": [
                "삼원 윤리 이론",
                "자기 보존",
                "파충류뇌",
                "방어적 정향",
            ],
        },
        {
            "id": "kw-narvaez-engagement-ethic",
            "term": "관여 윤리",
            "term_en": "",
            "definition": (
                "나바에즈 삼원 윤리 이론의 두 번째 정향. "
                "공감을 기초로 타인과 강력하고 친밀한 관계를 형성하는 정향. "
                "자기조절체계가 작동할 때는 사랑·배려·애착 으로 드러나고, "
                "자기규제 시스템이 약할 때는 관여 궁박 (공감적 고통) 으로 전이된다. "
                "삼원뇌의 포유류뇌 층위에 대응. "
                "2024-A Q6 (나) ㉢ 정답(관여 궁박·공감적 고통) 의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "related_terms": [
                "삼원 윤리 이론",
                "공감",
                "관여 궁박",
                "공감적 고통",
                "포유류뇌",
            ],
        },
        {
            "id": "kw-narvaez-ethic-of-imagination",
            "term": "상상 윤리",
            "term_en": "ethic of imagination",
            "definition": (
                "나바에즈 삼원 윤리 이론의 세 번째 정향이자 가장 성숙한 도덕 정향. "
                "숙고적 이성 능력을 활용하여 "
                "안전 윤리의 충동과 관여 윤리의 직관에 반응하여 그것들을 조정한다. "
                "삼원뇌의 신피질 층위에 대응하며, "
                "미래 지향·타자 지향으로 도덕적 판단의 지평을 확장한다. "
                "2024-A Q6 (나) ㉣ 정답(상상의 윤리) 의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "related_terms": [
                "삼원 윤리 이론",
                "숙고적 이성",
                "신피질",
                "정향 조정",
                "성숙한 도덕성",
            ],
        },
        {
            "id": "kw-narvaez-integrative-ethical-education",
            "term": "통합적 윤리 교육 모델",
            "term_en": "Integrative Ethical Education",
            "definition": (
                "나바에즈의 도덕교육 모델 trademark (약칭 IEE). "
                "학생을 윤리적 초보자에서 윤리적 전문가(ethical expert) 로 발달시키는 "
                "통합적 교수·학습 체계. "
                "교사가 먼저 윤리적 전문가가 된 뒤 학생을 양성하며, "
                "학습 내용 축(윤리 기술 직접 교수) 과 "
                "학습 환경 축(풍부한 보살핌의 분위기 조성) 등 "
                "여러 축에서 교수·학습 과정의 중점 사항을 체계적으로 설계한다. "
                "2016학년도 전공A Q9 제시문의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "related_terms": [
                "윤리적 전문가",
                "윤리적 초보자",
                "4과정 모형",
                "7가지 윤리적 기술",
                "도덕 교육",
            ],
        },
        {
            "id": "kw-narvaez-ethical-expert",
            "term": "윤리적 전문가",
            "term_en": "ethical expert",
            "definition": (
                "나바에즈 통합적 윤리 교육 모델(IEE) 의 교육 목표 개념. "
                "윤리 기술 발달의 종착점으로, "
                "윤리적 민감성·판단·초점·행동의 4과정에서 "
                "자동화된 고수준 숙달을 이룬 자를 지칭한다. "
                "반대 개념은 윤리적 초보자(ethical novice). "
                "교사가 먼저 전문가가 된 뒤 학생을 전문가로 양성하는 도덕교육 구도. "
                "2016학년도 전공A Q9 빈칸 정답."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "related_terms": [
                "윤리적 초보자",
                "통합적 윤리 교육 모델",
                "4과정 모형",
                "자동화",
            ],
        },
        {
            "id": "kw-narvaez-four-process-model",
            "term": "4과정 모형",
            "term_en": "Four Process Model",
            "definition": (
                "나바에즈가 레스트(James Rest) 의 4구성 요소 모델을 계승·재구성한 모형. "
                "좋은 인격을 갖춘 사람의 특징을 "
                "윤리적 민감성 · 윤리적 판단 · 윤리적 초점(동기) · 윤리적 행동의 "
                "4과정으로 분석하며, "
                "각 과정마다 7가지 윤리적 기술을 제시하여 총 28개 윤리 기술 체계를 구성한다. "
                "통합적 윤리 교육 모델(IEE) 의 교수 체계의 핵심 틀. "
                "2016학년도 전공A Q9 제시문."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "related_terms": [
                "7가지 윤리적 기술",
                "레스트 4구성 요소",
                "통합적 윤리 교육 모델",
                "윤리 기술 체계",
            ],
        },
        {
            "id": "kw-narvaez-moral-schema",
            "term": "도덕 스키마",
            "term_en": "moral schema",
            "definition": (
                "나바에즈가 레스트의 3 스키마(개인 이익 · 규범 유지 · 인습 이후) 를 계승하면서 "
                "내용과 직관적 차원으로 확장한 개념. "
                "도덕 스키마는 형식뿐만 아니라 내용도 포함하며, "
                "언어를 통한 명료한 표현보다는 직관적 인식을 통해 드러나는 경향이 있다. "
                "이중 과정 이론(dual-process theory)의 틀에서 "
                "자동적·직관적 과정이 추론과 함께 도덕 인지를 구성한다고 본다. "
                "2026학년도 전공B Q4 (을) ㉢ 정답(직관) 의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-postconventional-moral-thinking-1999",
            "related_terms": [
                "직관",
                "자동적 과정",
                "이중 과정 이론",
                "신콜버그주의",
                "인습 이후 사고",
            ],
        },
        {
            "id": "kw-narvaez-common-morality",
            "term": "공동의 도덕성",
            "term_en": "common morality",
            "definition": (
                "나바에즈의 신콜버그주의 공동체주의적·맥락주의적 확장 개념. "
                "인습 이후 사고 수준에서 작동하는 도덕 스키마가 공유된 이상에 기반할 때 "
                "이것이 반영되는 상태. "
                "형식과 내용 모두를 포함하며, "
                "도덕적 논의·열린 토론·공동체의 맥락·집단적 숙고가 "
                "온전히 스며 있는 상태로 형성된다. "
                "2026학년도 전공B Q4 (을) ㉣ 서술의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-postconventional-moral-thinking-1999",
            "related_terms": [
                "인습 이후 사고",
                "열린 토론",
                "집단적 숙고",
                "공동체 맥락",
                "도덕 스키마",
            ],
        },
        {
            "id": "kw-narvaez-neo-kohlbergian",
            "term": "신콜버그주의",
            "term_en": "Neo-Kohlbergian",
            "definition": (
                "콜버그 3수준 6단계 이론을 "
                "도덕 스키마 3 유형(개인 이익 · 규범 유지 · 인습 이후) 으로 재구성한 학파. "
                "레스트(James Rest) 가 주도하고 "
                "나바에즈 · 베브와 · 투마 등이 계승·확장한다. "
                "DIT(Defining Issues Test) 를 핵심 측정 도구로 삼으며, "
                "나바에즈는 여기에 직관·자동적 처리·체화 인지·신경생리학적 기반을 덧붙여 "
                "현대 도덕 심리학의 이론적 지평을 확장한다."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-postconventional-moral-thinking-1999",
            "related_terms": [
                "도덕 스키마",
                "DIT",
                "레스트 계승",
                "인습 이후 사고",
            ],
        },
        {
            "id": "kw-narvaez-dual-process-theory",
            "term": "이중 과정 이론",
            "term_en": "dual-process theory",
            "definition": (
                "도덕 인지가 자동적·직관적 과정과 의식적·명시적 추론 과정이라는 "
                "두 과정을 통해 작동한다고 보는 심리학적 틀. "
                "나바에즈는 이 틀을 신콜버그주의 내부로 수용하여 "
                "도덕 스키마가 추론뿐 아니라 직관적 인식으로도 드러난다고 본다. "
                "하이트(Jonathan Haidt) 의 사회직관주의와는 다르게, "
                "추론과 직관을 모두 도덕 인지의 구성 요소로 통합하는 관점. "
                "2026학년도 전공B Q4 (을) ㉢ 정답(직관) 의 이론적 배경."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-postconventional-moral-thinking-1999",
            "related_terms": [
                "직관",
                "자동적 과정",
                "도덕 스키마",
                "신콜버그주의",
            ],
        },
        {
            "id": "kw-narvaez-engagement-distress",
            "term": "관여 궁박",
            "term_en": "",
            "definition": (
                "나바에즈 관여 윤리의 비균형 상태. "
                "공감은 강하나 자기규제 시스템이 약해진 상황에서 "
                "타인에 대한 넘치는 애착·배려로 인해 마음이 불편해지는 상태. "
                "공감적 고통(empathic distress) 과 유사한 개념으로 "
                "호프만(Martin Hoffman) 의 공감 과잉 논의와도 연결된다. "
                "2024학년도 전공A Q6 (나) ㉢ 정답(관여 궁박/공감적 고통) 의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "related_terms": [
                "관여 윤리",
                "공감적 고통",
                "자기조절체계",
                "공감 과잉",
            ],
        },
        {
            "id": "kw-narvaez-triune-brain",
            "term": "삼원뇌",
            "term_en": "triune brain",
            "definition": (
                "폴 맥린(Paul MacLean) 이 제안한 뇌 구조 가설. "
                "뇌가 진화적으로 구분되는 세 층위 "
                "— 파충류뇌(생존·반사) · 포유류뇌(감정·관계) · 신피질(숙고·상상) — 로 구성된다고 본다. "
                "나바에즈는 이 삼원뇌 구도를 도덕 정향으로 확장하여 "
                "삼원 윤리 이론(안전 · 관여 · 상상) 을 정립한다. "
                "2024학년도 전공A Q6 (나) 제시문의 이론적 배경."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "narvaez-neurobiology-morality-2014",
            "related_terms": [
                "삼원 윤리 이론",
                "파충류뇌",
                "포유류뇌",
                "신피질",
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
    """나바에즈 영향·비교 관계 데이터 입력.

    ES 등록 확인 (2026-04-22 curl, 4건 모두 found=true):
     - rest     : 등록 — 나바에즈는 레스트 제자, 4구성 요소 → 4과정 모형 계승
     - kohlberg : 등록 — 신콜버그주의 학파의 원형 (3수준 6단계 이론)
     - haidt    : 등록 — 이중 과정·직관·자동적 처리 공유 (단, 사회직관주의와 이론적 대비)
     - hoffman  : 등록 — 공감적 고통 / 관여 궁박 공유 개념
    미등록 thinker(bebeau, thoma, maclean 등) 는 링크 생략.
    """
    relations = [
        {
            "from_thinker": "rest",
            "to_thinker": THINKER_ID,
            "type": "influenced",
            "description": (
                "레스트(James Rest) 는 나바에즈의 직접적 스승이자 이론적 출발점이다. "
                "나바에즈는 레스트와 『Postconventional Moral Thinking: A Neo-Kohlbergian Approach(1999)』 를 공저하며 "
                "신콜버그주의 학파의 이론적 토대를 함께 구축하였고, "
                "레스트의 4구성 요소 모델(윤리적 민감성 · 판단 · 초점 · 행동) 을 "
                "4과정 모형(Four Process Model) 으로 재구성하였다. "
                "각 과정마다 7가지 윤리적 기술을 제시하여 "
                "통합적 윤리 교육 모델(IEE) 의 교수 체계를 정립한 것은 "
                "레스트 모델의 직접적 계승·확장에 해당한다. "
                "임용 2016-A Q1(레스트 도덕적 민감성) + Q9(나바에즈 통합적 윤리 교육 모델) "
                "동일 시험 내 병치는 이 계승 관계의 반영."
            ),
            "evidence": (
                "Rest & Narvaez (1999) Postconventional Moral Thinking: A Neo-Kohlbergian Approach; "
                "Narvaez (2014) Neurobiology and the Development of Human Morality; "
                "2016-A Q9 제시문 '4과정 모형을 제안하고, 각 과정마다 7가지 윤리적 기술들을 제시' "
                "(coverage/2016-A.md L122); "
                "2026-B Q4 (을) 해설 '레스트는 1999년 타계 후 신콜버그주의를 이어가는 후계자가 "
                "나르바에즈·베브와·투마' (coverage/2026-B.md L230)"
            ),
        },
        {
            "from_thinker": "kohlberg",
            "to_thinker": THINKER_ID,
            "type": "influenced",
            "description": (
                "콜버그(Lawrence Kohlberg) 는 신콜버그주의 학파의 원형 사상가로서 "
                "나바에즈의 이론적 배경을 이루는 스승 세대이다. "
                "콜버그 3수준 6단계 이론 — 특히 인습 이후 수준의 보편화 가능한 도덕 원리 — 을 "
                "레스트가 도덕 스키마 3 유형으로 재구성하고, "
                "나바에즈가 여기에 직관·자동적 처리·체화 인지·신경생리학 기반을 덧붙여 "
                "신콜버그주의를 확장하였다. "
                "2026학년도 전공B Q4 는 갑(콜버그) 과 을(나바에즈) 을 직접 대립 배치하여 "
                "보편화 가능한 도덕 원리(콜버그·추론) 와 공동의 도덕성(나바에즈·직관·토론) 의 "
                "공통점과 차이점을 묻는 구성이며, 이는 두 사상가의 계승·분화 관계의 전형적 시험화."
            ),
            "evidence": (
                "Kohlberg (1981) The Philosophy of Moral Development Vol.1; "
                "Rest & Narvaez (1999) Postconventional Moral Thinking; "
                "2026-B Q4 갑(콜버그) vs 을(나바에즈) 직접 대립 배치 "
                "(coverage/2026-B.md L216-L245); "
                "해설 '인습 이후 사고 수준에서 작동하는 도덕 스키마는 공유된 이상에 기반' "
                "(coverage/2026-B.md L226)"
            ),
        },
        {
            "from_thinker": "haidt",
            "to_thinker": THINKER_ID,
            "type": "compared",
            "description": (
                "하이트(Jonathan Haidt) 와 나바에즈는 현대 도덕 심리학에서 "
                "직관·자동적 처리를 공통적으로 강조하는 두 축으로 비교된다. "
                "두 사상가 모두 이중 과정 이론(dual-process theory) 을 수용하여 "
                "도덕 인지가 자동적·직관적 과정과 의식적 추론 과정의 결합으로 작동한다고 보며, "
                "콜버그 원형의 '의식적 추론 중심' 모델의 한계를 지적한다. "
                "그러나 하이트는 사회직관주의와 도덕 기반 이론(Moral Foundations Theory) 을 통해 "
                "신콜버그 계보와 단절을 선언한 반면, "
                "나바에즈는 신콜버그주의 내부에서 추론과 직관을 통합하는 경로를 택한다. "
                "두 입장은 직관 강조라는 공통점과 신콜버그 계보 수용 여부라는 차이점으로 대비된다."
            ),
            "evidence": (
                "Haidt (2001) The Emotional Dog and Its Rational Tail; "
                "Narvaez (2014) Neurobiology and the Development of Human Morality; "
                "2026-B Q4 (을) 해설 '나르바에즈·하이트(Haidt)·쾨닉(Koenig)의 이중 과정 이론에서 "
                "자동적 과정과 짝을 이루는 개념은 직관' (coverage/2026-B.md L236)"
            ),
        },
        {
            "from_thinker": "hoffman",
            "to_thinker": THINKER_ID,
            "type": "compared",
            "description": (
                "호프만(Martin Hoffman) 과 나바에즈는 공감 중심 도덕 심리학의 두 축으로 비교된다. "
                "호프만은 공감 각성 5양식과 공감 발달 5단계, 유도·귀납 훈육을 제시하며 "
                "공감적 고통(empathic distress) 을 공감 발달의 한 축으로 분석한 반면, "
                "나바에즈는 관여 윤리 내부에서 관여 궁박을 "
                "자기규제 시스템이 약해진 비균형 상태로 재개념화한다. "
                "두 사상가는 공감적 고통이라는 동일 개념에 대해 "
                "발달 단계적 분석(호프만) 과 자기조절체계 관점 분석(나바에즈) 이라는 상보적 시각을 제시한다. "
                "임용 2016-A Q9(나바에즈) + Q10 을(호프만) 동일 시험 병치는 이 공감 기반 도덕 심리학 대비의 반영."
            ),
            "evidence": (
                "Hoffman (2000) Empathy and Moral Development: Implications for Caring and Justice; "
                "Narvaez (2014) Neurobiology and the Development of Human Morality; "
                "2024-A Q6 (나) 해설 '관여 궁박 … 호프만(Martin Hoffman)의 공감 과잉(empathic over-arousal) "
                "개념과 연관되나, 나바에즈는 이를 자기규제 시스템 약화 상황으로 재개념화' "
                "(coverage/2024-A.md L294); "
                "2016-A Q9(나바에즈) + Q10 을(호프만) 동일 시험 병치 "
                "(coverage/2016-A.md L42)"
            ),
        },
    ]

    inserted = 0
    for i, rel in enumerate(relations):
        # rest→narvaez 관계는 레스트 등록 시점의 기존 문서 id (rest-rel-002) 와 중복 방지
        if rel["from_thinker"] == "rest" and rel["to_thinker"] == THINKER_ID:
            # 기존 문서 확인 후 존재하면 skip (등록 시점에 이미 생성됨)
            try:
                client.get(index=INDEX_RELATIONS, id="rest-rel-002")
                print("[relation] rest-rel-002: 이미 존재 (skip — rest 등록 시점 생성)")
                continue
            except Exception:
                # 기존 문서가 없으면 본 스크립트 id 로 생성
                pass
        rel_id = f"rel-{rel['from_thinker']}-{rel['to_thinker']}-{rel['type']}-{i+1}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id}: {result['result']}")
        inserted += 1

    return len(relations)


def main():
    """메인 실행 함수."""
    print("=== 다르시아 나바에즈(Narvaez) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (narvaez)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n[OK] 나바에즈 데이터 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}", file=sys.stderr)
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
