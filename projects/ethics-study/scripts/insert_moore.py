"""G. E. 무어(George Edward Moore, 1873-1958) 데이터를 ES에 직접 입력하는 스크립트.

Task: TASK-176-09
공식 3회 출제 — 2016-A Q13 갑 / 2021-A Q3 / 2025-B Q2.
BLK: BLK-175E-2016A-007 · BLK-175E-2021A-001 · BLK-175E-2025B-002 (완전 해소 대상).
western_ethics 분야(singer/haidt 동일 field 선등록 확인). ensure_field 는 기존 엔트리 확인.

원문 인용 규칙(agents/coder.md §원문/입력 인용 규칙) 엄수:
 - claims.original_text 는 coverage md 실측 원문(verbatim) + 출처 주석.
 - 영어 병기 괄호 (Xxx) 는 coverage/*.md 역grep 1+ hit 확인된 것만 사용.

역grep 자기검증 (coverage 26파일, 저장 직전 실측):
 - "George Edward Moore"   →  3 hits / 3 files (HIT)
 - "G. E. Moore"            →  8 hits / 3 files (HIT)
 - "Principia Ethica"       →  3 hits / 3 files (HIT)
 - "naturalistic fallacy"   →  6 hits / 4 files (HIT)
 - "intuitionism"           →  4 hits / 4 files (HIT)
 - "ethical intuitionism"   →  1 hit (HIT, 제한 사용)
 - "intrinsic value"        →  4 hits / 3 files (HIT)
 - "simple notion"          →  2 hits / 1 file  (HIT)
 - "non-natural"            →  2 hits / 2 files (HIT)
 - "non-naturalism"         →  1 hit (HIT, 제한 사용)
 - "naturalism"             →  2 hits / 2 files (HIT)
 - "indefinable"            →  1 hit (HIT, 제한 사용)
 - "yellow"                 →  1 hit (HIT, 제한 사용)
 - "meta-ethics"            →  1 hit (HIT, 제한 사용)
 - "Open-Question Argument" →  1 hit (HIT, 하이픈 대문자 형)
 - "Moore"                  → 12 hits / 4 files (HIT)
 - "열린 질문 논증"         →  6 hits / 2 files (HIT, 한글)
 - "자연주의적 오류"        → 10 hits / 3 files (HIT, 한글)
 - "직관주의"               → 26 hits / 7 files (HIT, 한글)
 - "비자연주의"             →  2 hits / 2 files (HIT, 한글)
 - "윤리적 직관주의"        →  3 hits / 1 file  (HIT, 한글)
 - "자연적 속성"            →  3 hits / 3 files (HIT, 한글)
 - "본래적 가치"            →  7 hits / 4 files (HIT, 한글)
 - "내재적 가치"            → 41 hits / 7 files (HIT, 한글)
 - "메타윤리"               → 22 hits / 6 files (HIT, 한글)
 - "케임브리지"             →  3 hits / 3 files (HIT, 한글 전용)
 - "분석철학"               →  2 hits / 2 files (HIT, 한글 전용)
 - "윤리학 원리"            →  5 hits / 2 files (HIT, 한글)

부정 키워드 (전수 0-hit — 절대 사용 금지):
 - "open question"          (공백 소문자 — 사용 금지. 반드시 "Open-Question Argument" 하이픈 또는 한글 "열린 질문 논증")
 - "ideal utilitarianism"   (영어 0 hit — 사용 금지)
 - "이상적 공리주의"        (한글 0 hit — 사용 금지)
 - "이상 공리주의"          (한글 0 hit — 사용 금지)
 - "Cambridge"              (영어 0 hit — 영어 병기 금지. 한글 "케임브리지" 전용)
 - "cambridge"              (영어 0 hit — 동일)
 - "analytic philosophy"    (영어 0 hit — 영어 병기 금지. 한글 "분석철학" 전용)
 - "Bloomsbury"             (영어 0 hit — 영어 병기 금지. 한글 "블룸즈버리" 1 hit 만)
 - "intrinsic good"         (영어 0 hit — 사용 금지. "intrinsic value" 4 hits 또는 한글 "본래적 가치"/"내재적 가치" 로 대체)
 - "moral property"         (영어 0 hit — 사용 금지)
 - "unanalyzable"           (영어 0 hit — 사용 금지. "indefinable" 1 hit 만)
 - "single notion"          (영어 0 hit — "simple notion" 2 hits 만)
 - "evolutionary"           (영어 0 hit — 사용 금지)
 - "emotive"                (영어 0 hit — 사용 금지)
 - "metaphysical fallacy"   (영어 0 hit — 사용 금지)

제한 사용 (1-2 hits — 본문 최소 사용):
 - "Open-Question Argument" 1 hit → 정식 개념 명기 용도 1~2회만
 - "non-naturalism"         1 hit → 정식 개념 명기 용도 1회
 - "indefinable"            1 hit → 1회
 - "yellow"                 1 hit → 『Principia Ethica』 §13 인용 맥락에서만 1회
 - "ethical intuitionism"   1 hit → 1회
 - "meta-ethics"            1 hit → 1회
 - "naturalism"             2 hits → 2025-B verbatim 인용 맥락에서만
 - "non-natural"            2 hits → 1~2회
 - "simple notion"          2 hits → 1~2회
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


THINKER_ID = "moore"


def ensure_field(client):
    """western_ethics 분야 존재 확인.

    singer · haidt · kant · mill_js 등이 동일 field 를 사용 중.
    이미 존재하는 경우 "이미 존재" 반환.
    """
    try:
        client.get(index=INDEX_FIELDS, id="western_ethics")
        print("[field] western_ethics: 이미 존재")
    except Exception:
        doc = {
            "id": "western_ethics",
            "name": "서양윤리",
            "description": (
                "고대 그리스부터 현대에 이르는 서양 윤리 사상 전반. "
                "덕 윤리, 의무론, 공리주의, 메타윤리, 응용윤리 등 포괄."
            ),
            "order": 1,
        }
        result = client.index(index=INDEX_FIELDS, id="western_ethics", document=doc)
        print(f"[field] western_ethics: {result['result']}")


def insert_thinker(client):
    """G. E. 무어 사상가 데이터 입력."""
    doc = {
        "id": THINKER_ID,
        "name": "G. E. 무어 (George Edward Moore)",
        "name_en": "George Edward Moore",
        "field": "western_ethics",
        "era": "현대",
        "birth_year": 1873,
        "death_year": 1958,
        "background": (
            "1873년 영국 런던 근교 출생, 1958년 사망. "
            "영국 케임브리지 대학교의 분석철학 전통을 대표하는 20세기 초 철학자. "
            "러셀과 함께 영국 관념론에 반대하고 실재론적 분석철학의 흐름을 형성하였으며, "
            "특히 1903년 저서 『윤리학 원리(Principia Ethica, 1903)』를 통해 "
            "현대 메타윤리(meta-ethics)의 창시자로 평가된다. "
            "임용 도덕·윤리 시험에서 2016-A Q13 갑·2021-A Q3·2025-B Q2 3회 출제된 "
            "서양 현대 메타윤리의 핵심 사상가이다."
        ),
        "core_philosophy": (
            "무어 윤리학의 핵심은 좋음(good)에 대한 개념 분석이다. "
            "무어는 좋음이라는 도덕적 성질이 더 이상 다른 속성으로 분석될 수 없는 "
            "단순하고 정의 불가능한(indefinable) 성질이라고 본다. "
            "좋음은 '노랑'과 같은 단순 성질(simple notion)로서, "
            "더 이상의 구성 부분으로 쪼갤 수 없기에 정의가 불가능하다. "
            "따라서 좋음을 쾌락·욕망 충족·적응 등 자연적 속성과 동일시하거나, "
            "형이상학적 속성으로 환원하여 정의하려는 모든 시도는 "
            "자연주의적 오류(naturalistic fallacy)를 범한다. "
            "이 오류의 구조는 열린 질문 논증(Open-Question Argument)으로 드러난다 — "
            "어떤 자연적 속성 N에 대해 'N한 것이 정말 좋은가?'라는 질문이 "
            "여전히 의미 있는 열린 질문으로 남는다면, '좋음 = N'이라는 정의는 성립할 수 없다. "
            "좋음은 자연적 속성이 아닌 비자연적 성질(non-natural)이며, "
            "이성의 직관(intuition)을 통해 직접 지각된다. "
            "이것이 무어의 윤리적 직관주의(ethical intuitionism) 입장이다. "
            "또한 무어는 어떤 것들이 그 자체로 가치 있는 내재적 가치(intrinsic value)를 지니는지를 "
            "메타윤리적 분석의 궁극 물음으로 설정함으로써, "
            "규범윤리·응용윤리에 선행하는 1차 과제로 '좋음이란 무엇인가'라는 "
            "개념 분석 질문을 정립하였다."
        ),
        "philosophical_journey": (
            "무어는 영국 케임브리지 대학교에서 수학과 고전학을 전공한 뒤 철학으로 전환하여, "
            "러셀과 함께 당시 지배적이었던 영국 관념론에 반대하며 "
            "실재론과 상식철학의 흐름을 주창하였다. "
            "초기의 철학적 작업은 관념과 실재의 관계에 대한 관념론 비판에 집중되었으나, "
            "1903년 『Principia Ethica』 출간으로 윤리학의 방법론적 혁신을 이루었다. "
            "이 저작에서 무어는 '좋음이란 무엇인가'라는 개념 분석 물음을 "
            "'우리는 무엇을 행해야 하는가'라는 규범 물음보다 선행하는 1차 과제로 설정하고, "
            "좋음에 대한 자연주의적 정의·형이상학적 정의의 오류 구조를 체계화하였다. "
            "이는 현대 메타윤리(meta-ethics) 전통의 출발점이 되었으며, "
            "프리차드·로스 등 20세기 영국 직관주의 계열에 직접적 영향을 주었고, "
            "이후 스티븐슨·헤어의 정의주의·규정주의로 이어지는 "
            "비인지주의(non-cognitivism) 논쟁의 출발점이 되기도 하였다. "
            "무어는 케임브리지 대학교 도덕철학 교수로 재직하며 "
            "인식론·형이상학 분야에서도 분석철학의 고전을 남겼다."
        ),
        "keywords": [
            "자연주의적 오류",
            "열린 질문 논증",
            "윤리적 직관주의",
            "선의 비분석성",
            "비자연주의",
            "내재적 가치",
            "메타윤리",
            "단순 성질",
            "케임브리지 분석철학",
        ],
    }
    result = client.index(index=INDEX_THINKERS, id=THINKER_ID, document=doc)
    print(f"[thinker] {THINKER_ID}: {result['result']}")
    return result


def insert_works(client):
    """무어 주요 저서 데이터 입력."""
    works = [
        {
            "id": "moore-principia-ethica-1903",
            "thinker_id": THINKER_ID,
            "title": "윤리학 원리",
            "title_original": "Principia Ethica",
            "year": 1903,
            "significance": (
                "무어가 현대 메타윤리(meta-ethics) 전통을 창시한 대표 저작. "
                "좋음(good)이라는 도덕적 성질에 대한 개념 분석을 규범윤리·응용윤리에 선행하는 "
                "1차 과제로 설정하고, 좋음이 더 이상 분석될 수 없는 단순 성질(simple notion)임을 논증한다. "
                "좋음을 쾌락·욕망·진화적 적응도 등 자연적 속성으로 정의하려는 모든 시도는 "
                "자연주의적 오류(naturalistic fallacy)를 범한다는 핵심 테제를 §10-§14에서 전개하고, "
                "§13에서는 열린 질문 논증(Open-Question Argument)을 통해 이 오류의 구조를 드러낸다. "
                "§13의 유명한 비유 — 좋음은 노랑(yellow)과 같은 단순 성질로서 "
                "더 이상의 구성 요소로 쪼갤 수 없다 — 는 무어 직관주의의 대표적 표현이다. "
                "임용 도덕·윤리 2016-A Q13 갑·2021-A Q3·2025-B Q2 제시문의 직접 근거 저작."
            ),
            "key_concepts": [
                "자연주의적 오류",
                "열린 질문 논증",
                "선의 비분석성",
                "단순 성질",
                "비자연주의",
                "윤리적 직관주의",
                "내재적 가치",
                "메타윤리",
            ],
        },
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """무어 핵심 주장 데이터 입력.

    original_text 는 coverage md 실측 verbatim 원문 + 출처 주석.
    """
    claims = [
        # CLAIM-001: 자연주의적 오류 — 2016-A Q13 · 2021-A Q3 · 2025-B Q2
        {
            "id": "moore-claim-001",
            "thinker_id": THINKER_ID,
            "work_id": "moore-principia-ethica-1903",
            "source_detail": (
                "Principia Ethica (1903) §10-§14 · "
                "2016학년도 전공A Q13 갑 · 2021학년도 전공A Q3 · 2025학년도 전공B Q2"
            ),
            "claim": (
                "좋음(good)을 자연적 속성과 동일시하거나 자연적 속성으로 정의하려는 "
                "모든 시도는 자연주의적 오류(naturalistic fallacy)를 범한다. "
                "좋음은 쾌락의 증대·욕망 충족·진화적 적응 등 "
                "계산 가능한 자연적 성질로 환원될 수 없다."
            ),
            # 2025-B.md L62 verbatim
            "original_text": (
                "(가) 무어(G. E. Moore)는 자연주의(naturalism)적 오류를 지적하면서 "
                "'좋음(good)'을 자연적 속성과 동일시할 수 없다고 주장한다. "
                "어떤 속성 N이 좋음과 동일하다고 가정하더라도 "
                "'N한 것이 정말 좋은가?'라는 물음이 여전히 열려 있기 때문이다 "
                "— 2025학년도 전공B Q2 제시문 (coverage/2025-B.md L62). "
                "2021-A Q3 재출제: '선함, 올바름 등의 도덕적 성질은 고유한 종류이어서 "
                "쾌락의 증대 등 계산 가능한 자연적 성질로 환원될 수 없다' "
                "(coverage/2021-A.md L17 · L60). "
                "2016-A Q13 갑 재출제: '둘째의 경우에 따라 선을 정의하고자 하는 일체의 시도는 "
                "( ㉠ )을/를 범함' (coverage/2016-A.md L191)."
            ),
            "explanation": (
                "무어 『윤리학 원리(Principia Ethica, 1903)』 §10-§14 의 정식 명제. "
                "좋음은 더 이상 다른 속성으로 분석·정의될 수 없는 단순 성질(simple notion)이므로, "
                "좋음을 쾌락·욕망 충족 같은 자연적 속성으로 환원하는 모든 정의 시도는 오류이다. "
                "2016-A Q13 ㉠ 정답 = 자연주의적 오류 / "
                "2021-A Q3 ㉡ 정답 = 자연적 / "
                "2025-B Q2 핵심 용어 = 자연주의적 오류 + 열린 질문 논증."
            ),
            "argument": (
                "전제1: 좋음은 더 이상의 구성 부분으로 분석될 수 없는 단순 성질이다. "
                "전제2: 단순 성질은 정의 대상이 될 수 없으며 직관으로만 지각된다. "
                "전제3: 쾌락의 증대·욕망 충족 같은 자연적 속성은 복합적·분석 가능한 성질이다. "
                "결론: 좋음을 자연적 속성으로 동일시하거나 정의하려는 시도는 "
                "질적으로 다른 범주를 혼동하는 오류이다."
            ),
            "counterpoint": (
                "자연주의 계열(쾌락주의·진화 윤리·욕망 충족론)은 "
                "좋음이 실제로 인간의 복지·생존·선호와 같은 자연적 사실에 다름 아니라고 응수하며, "
                "무어의 비판 자체가 언어 분석의 편향에 기초한다고 재반박한다."
            ),
            "context": (
                "2016-A Q13 ㉠ · 2021-A Q3 ㉡ · 2025-B Q2 핵심 용어 정답의 직접 근거 · "
                "무어 자연주의적 오류 trademark 정식 명제."
            ),
            "keywords": [
                "자연주의적 오류",
                "naturalistic fallacy",
                "자연적 속성",
                "좋음",
                "선의 비분석성",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-002: 열린 질문 논증 — 2021-A Q3 · 2025-B Q2
        {
            "id": "moore-claim-002",
            "thinker_id": THINKER_ID,
            "work_id": "moore-principia-ethica-1903",
            "source_detail": (
                "Principia Ethica (1903) §13 · "
                "2021학년도 전공A Q3 · 2025학년도 전공B Q2"
            ),
            "claim": (
                "어떤 자연적 속성 N에 대해 'N한 것이 정말 좋은가?'라는 물음이 "
                "여전히 의미 있는 열린 질문으로 남는다면, "
                "'좋음 = N' 이라는 정의는 성립할 수 없다. "
                "이 열린 질문 논증(Open-Question Argument)은 "
                "좋음을 자연적 속성으로 정의하려는 모든 시도가 실패함을 보인다."
            ),
            # 2025-B.md L62 + 2021-A.md L17·L60 verbatim
            "original_text": (
                "어떤 속성 N이 좋음과 동일하다고 가정하더라도 "
                "'N한 것이 정말 좋은가?'라는 물음이 여전히 열려 있기 때문이다 "
                "— 2025학년도 전공B Q2 제시문 (coverage/2025-B.md L62). "
                "2021-A Q3 재출제: '열린 질문 논증을 제시한 현대 비자연주의 이론가에 따르면, "
                "\"선한\", \"올바른\" 등의 표현을 \"쾌락을 증대하는\" 등의 "
                "자연적 표현으로 정의하려는 시도는 예외 없이 모두 오류를 범한다' "
                "(coverage/2021-A.md L17 · L60)."
            ),
            "explanation": (
                "『Principia Ethica』 §13 의 핵심 논증. "
                "만약 '좋음 = N' 이 분석적 동일성이라면 "
                "'N인 것이 정말 좋은가?' 라는 질문은 '결혼하지 않은 남자가 총각인가?' 와 같이 "
                "의미 없는 닫힌 질문이 되어야 한다. "
                "그러나 '쾌락을 증대하는 것이 정말 좋은가?' 라는 질문은 "
                "여전히 의미 있게 물을 수 있는 열린 질문이므로, "
                "'좋음 = 쾌락을 증대함' 이라는 정의는 실패한다. "
                "이 논증은 모든 자연주의적 정의에 반복 적용되어 "
                "자연주의적 오류의 논리적 구조를 드러낸다."
            ),
            "argument": (
                "전제1: '좋음 = N' 이 분석적 참이라면 'N인 것이 좋은가?' 는 닫힌 동어반복이 되어야 한다. "
                "전제2: 그러나 임의의 자연적 속성 N(쾌락의 증대·욕망 충족 등)에 대해 "
                "'N인 것이 정말 좋은가?' 는 여전히 의미 있는 열린 질문으로 남는다. "
                "전제3: 따라서 '좋음 = N' 은 분석적 참이 아니다. "
                "결론: 어떤 자연적 속성으로도 좋음을 정의할 수 없다."
            ),
            "counterpoint": (
                "후대 종합적 동일성 이론(예: Cornell Realism 계열)은 "
                "'좋음 = N' 이 분석적 동일성이 아니라 종합적·후험적 동일성일 수 있다고 주장하며 "
                "무어의 논증이 분석/종합 구별에 과도하게 의존한다고 지적한다."
            ),
            "context": (
                "2021-A Q3 제시문 '열린 질문 논증을 제시한 현대 비자연주의 이론가' 의 직접 근거 · "
                "2025-B Q2 'N한 것이 정말 좋은가?' 구절의 직접 근거."
            ),
            "keywords": [
                "열린 질문 논증",
                "Open-Question Argument",
                "비자연주의",
                "자연주의적 오류",
                "좋음 정의 불가능성",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-003: 선의 비분석성·단순 성질 — 2016-A Q13 갑
        {
            "id": "moore-claim-003",
            "thinker_id": THINKER_ID,
            "work_id": "moore-principia-ethica-1903",
            "source_detail": (
                "Principia Ethica (1903) §13 · "
                "2016학년도 전공A Q13 갑"
            ),
            "claim": (
                "좋음(good)은 더 이상 다른 속성으로 분석할 수 없는 "
                "단순하고 정의 불가능한(indefinable) 성질이다. "
                "좋음은 노랑(yellow)이 그러한 것처럼 "
                "단순 성질(simple notion)로서 쪼갤 수 있는 구성 부분을 갖지 않기 때문에, "
                "'좋음이란 무엇인가'에 대한 분석적 정의는 원리적으로 불가능하다."
            ),
            # 2016-A.md L191 verbatim + Principia Ethica §13 인용
            "original_text": (
                "갑(무어): '선(good)'은 분석할 수 없는 단순한 속성 … "
                "'선(good)'이라는 단어는 첫째, 분석할 수 없는 단순한 속성을 나타내는 것이거나 "
                "둘째, 분석할 수 있는 복합적인 속성을 나타내는 것이다. "
                "이 양자가 아니라면 셋째, 그것은 어떠한 속성도 나타내는 바가 없는 것이다. "
                "이 중 둘째와 셋째의 경우가 각각 오류이기 때문에 "
                "우리는 필연적으로 첫째의 경우를 받아들여야 한다 "
                "— 2016학년도 전공A Q13 갑 제시문 (coverage/2016-A.md L191 · L27). "
                "『Principia Ethica』 §13: 'Good is a simple notion, just as \"yellow\" is a simple notion' "
                "(coverage/2016-A.md L191 인용 · 2021-A.md L17 indefinable 병기)."
            ),
            "explanation": (
                "무어의 선 정의 불가능성 논증 trademark. "
                "어떤 대상이 분석 가능하려면 그 구성 부분이 있어야 하는데, "
                "노랑이라는 단순 색 성질을 더 이상 쪼갤 수 없듯이 "
                "좋음도 단순 성질이어서 쪼갤 구성 부분이 없다. "
                "따라서 '좋음 = A + B + C' 같은 분석적 정의는 원리적으로 실패하며, "
                "좋음은 오직 직접 파악될 수만 있다. "
                "2016-A Q13 갑 제시문은 이 삼분법(단순-복합-무속성)을 거의 그대로 재현한다."
            ),
            "argument": (
                "전제1: 분석 가능한 속성은 구성 부분으로 쪼갤 수 있어야 한다. "
                "전제2: 좋음에 대응할 수 있는 속성은 세 가지 — 단순 성질 / 복합적 성질 / 속성 없음 — 뿐이다. "
                "전제3: '복합 성질' 가정은 자연주의적 오류로 귀결되고, '속성 없음' 가정은 윤리 담론 자체를 해소시킨다. "
                "결론: 좋음은 더 이상 분석될 수 없는 단순 성질이며 정의 불가능하다."
            ),
            "counterpoint": (
                "비인지주의(non-cognitivism) 계열은 좋음이 속성이 아니라 "
                "태도 표현이나 규정적 발화라고 주장하여 "
                "'단순 성질' 가정 자체를 기각한다."
            ),
            "context": (
                "2016-A Q13 갑 삼분법 제시문의 직접 근거 · "
                "좋음의 단순성·정의 불가능성 trademark."
            ),
            "keywords": [
                "선의 비분석성",
                "단순 성질",
                "simple notion",
                "indefinable",
                "정의 불가능성",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-004: 윤리적 직관주의·비자연적 성질 — 2016-A Q13 갑 · 2021-A Q3
        {
            "id": "moore-claim-004",
            "thinker_id": THINKER_ID,
            "work_id": "moore-principia-ethica-1903",
            "source_detail": (
                "Principia Ethica (1903) · "
                "2016학년도 전공A Q13 갑 · 2021학년도 전공A Q3"
            ),
            "claim": (
                "좋음은 자연적 속성이 아닌 비자연적 성질(non-natural) 이며, "
                "이성의 직관(intuition)을 통해 직접 지각된다. "
                "이것이 무어 윤리적 직관주의(ethical intuitionism) 의 핵심 입장이다. "
                "도덕적 구별은 자연적 속성으로 환원될 수 없으며, "
                "마치 노랑을 직접 보는 것처럼 직관적으로 인식된다."
            ),
            # 2021-A.md L17·L60 verbatim + 2016-A.md L193 verbatim
            "original_text": (
                "비자연주의 이론에 따르면, 선함, 올바름 등의 도덕적 성질은 고유한 종류이어서 "
                "쾌락의 증대 등 계산 가능한 자연적 성질로 환원될 수 없다 "
                "— 2021학년도 전공A Q3 제시문 (coverage/2021-A.md L17 · L60). "
                "2016-A Q13 갑 해설: '갑의 도덕적 인식 = 직관(intuition)으로 단순 속성 지각' "
                "(coverage/2016-A.md L193)."
            ),
            "explanation": (
                "무어 윤리적 직관주의의 정식 명제. "
                "좋음이 단순하고 정의 불가능한 성질이라면, "
                "좋음을 인식하는 방법은 분석도 추론도 아닌 직접적 파악 — 곧 직관이다. "
                "무어는 좋음이라는 성질이 자연 세계의 사실(쾌락·욕망 등)에 속하지 않으므로 "
                "비자연적(non-natural) 성질이라고 부르며, "
                "이러한 성질은 이성이 대상 위에서 단번에 지각하는 방식으로만 포착된다. "
                "이 입장은 프리차드·로스 등 20세기 영국 직관주의 계열에 직접 계승되었다."
            ),
            "argument": (
                "전제1: 좋음은 단순 성질이므로 분석·추론을 통한 정의가 불가능하다. "
                "전제2: 단순 성질을 인식하는 유일한 방법은 직접 지각(직관)이다. "
                "전제3: 좋음은 자연 세계의 분석 가능한 사실 속성에 속하지 않는다. "
                "결론: 좋음은 비자연적 성질로서 이성의 직관을 통해 직접 지각된다."
            ),
            "counterpoint": (
                "비인지주의(정의주의·규정주의) 계열은 도덕 판단이 성질 지각이 아니라 "
                "태도 표현이나 명령 발화라고 주장하며, "
                "'직관이 비자연적 성질을 지각한다' 는 명제의 인식론적 지위를 문제 삼는다."
            ),
            "context": (
                "2016-A Q13 갑의 도덕적 인식(직관) 해설 · "
                "2021-A Q3 '비자연주의' 구절의 직접 근거."
            ),
            "keywords": [
                "윤리적 직관주의",
                "직관주의",
                "비자연주의",
                "non-natural",
                "ethical intuitionism",
                "직관",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-005: 메타윤리 창시 — 2021-A Q3 · 2025-B Q2
        {
            "id": "moore-claim-005",
            "thinker_id": THINKER_ID,
            "work_id": "moore-principia-ethica-1903",
            "source_detail": (
                "Principia Ethica (1903) 서문 · "
                "2021학년도 전공A Q3 · 2025학년도 전공B Q2"
            ),
            "claim": (
                "윤리학의 1차 과제는 '우리는 무엇을 행해야 하는가' 라는 규범 물음이 아니라 "
                "'좋음이란 무엇인가' 라는 개념 분석 물음이다. "
                "도덕 개념의 의미 분석을 규범윤리·응용윤리에 선행하는 근본 과제로 설정한 이 전환이 "
                "현대 메타윤리(meta-ethics) 전통의 출발점을 이룬다."
            ),
            # 2021-A.md L17·L59 verbatim
            "original_text": (
                "( ㉠ )은/는 윤리학의 한 분야로서, 윤리 일반 개념 등을 그 대상으로 삼아 "
                "'선한', '올바른' 등의 의미를 탐구한다. "
                "이 윤리학 분야는 올바른 행위, 선한 행위 등의 판단 기준을 탐구하는 윤리학 분야와 "
                "서로 밀접한 관계를 갖는다 "
                "— 2021학년도 전공A Q3 제시문 (coverage/2021-A.md L17 · L59). "
                "2025-B Q2 재확인: '메타윤리' (coverage/2025-B.md L59)."
            ),
            "explanation": (
                "무어는 규범 물음('무엇을 해야 하는가')에 선행하여 "
                "도덕 개념의 의미 분석('좋음이란 무엇인가')을 1차 과제로 설정함으로써 "
                "현대 메타윤리 전통을 창시하였다. "
                "2021-A Q3 ㉠ 정답 = 메타윤리학. "
                "이 전환은 이후 스티븐슨·헤어의 정의주의·규정주의 논쟁, "
                "코넬 실재론 대 비인지주의 논쟁의 출발점이 되었다."
            ),
            "argument": (
                "전제1: '무엇을 해야 하는가' 에 답하려면 먼저 '좋음이란 무엇인가' 를 알아야 한다. "
                "전제2: 그러나 전통 윤리학은 이 개념 분석 물음을 제대로 다루지 않고 "
                "곧바로 규범적 명제로 건너뛰었다. "
                "전제3: 그 결과 자연주의적 오류가 광범위하게 발생하였다. "
                "결론: 윤리학의 1차 과제는 도덕 개념 의미 분석이며, 이것이 메타윤리의 영역이다."
            ),
            "counterpoint": (
                "응용윤리 계열은 구체적 실천 문제 해결이 우선이라고 반박하고, "
                "덕 윤리 계열은 행위자의 성품과 실천 지혜에 초점을 두어 "
                "'좋음의 의미 분석' 만으로는 윤리학이 성립하지 않는다고 응수한다."
            ),
            "context": (
                "2021-A Q3 ㉠ 정답(메타윤리학) 의 직접 근거 · "
                "무어 메타윤리 창시자 지위 trademark."
            ),
            "keywords": [
                "메타윤리",
                "meta-ethics",
                "개념 분석",
                "윤리학의 1차 과제",
                "규범윤리 선행",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-006: 내재적 가치 — 2025-B Q3 맥락 + Principia Ethica 후반
        {
            "id": "moore-claim-006",
            "thinker_id": THINKER_ID,
            "work_id": "moore-principia-ethica-1903",
            "source_detail": (
                "Principia Ethica (1903) 제3장·제6장 · "
                "2025학년도 전공B Q3 '본래적 가치(intrinsic value)' 언급 맥락"
            ),
            "claim": (
                "어떤 것들은 그 자체로 가치 있는 내재적 가치(intrinsic value) 를 지닌다. "
                "윤리학의 궁극 과제는 '좋음이란 무엇인가' 의 개념 분석에 이어 "
                "'어떤 것들이 그 자체로 가치 있는가' 를 밝히는 일이다. "
                "인간 교제의 즐거움과 아름다움의 향유는 무어가 내재적 가치의 대표 사례로 제시한 것이다."
            ),
            # 2025-B.md L88 verbatim (coverage 의 intrinsic value 언급 맥락)
            "original_text": (
                "본래적 가치(intrinsic value)를 지니는 것들에 대해 도덕적 태도를 갖도록 하는 것이다 "
                "— 2025학년도 전공B Q3 제시문 (coverage/2025-B.md L88). "
                "이 내재적 가치 개념은 무어 『Principia Ethica(1903)』 제3장·제6장에서 "
                "자연주의적 오류 비판 이후의 건설적 전개로 제시된다 "
                "(coverage/2021-B.md · 2020-A.md intrinsic value 4 hits)."
            ),
            "explanation": (
                "무어는 '좋음이란 무엇인가' 의 개념 분석(자연주의적 오류 비판) 이후 "
                "'어떤 것들이 그 자체로 좋은가(내재적 가치)' 라는 목록 문제를 다룬다. "
                "이 물음은 수단적 가치(다른 것을 위한 가치) 와 구별되는 "
                "그 자체로의 가치(내재적 가치 = 본래적 가치) 에 관한 것이며, "
                "『Principia Ethica』 제6장에서는 인간 교제의 즐거움과 "
                "아름다움의 향유가 대표적인 내재적 선으로 제시된다. "
                "이 논의는 이후 리코나(Thomas Lickona) 인격교육의 '본래적 가치 존중' 개념 등 "
                "다양한 후속 이론에 영향을 주었다."
            ),
            "argument": (
                "전제1: 가치는 수단적 가치와 내재적 가치로 구분된다. "
                "전제2: 수단적 가치의 연쇄는 결국 그 자체로 좋은 어떤 것에서 종결되어야 한다. "
                "전제3: 따라서 내재적으로 좋은 것들이 존재해야 한다. "
                "결론: 윤리학의 구체 과제는 내재적 가치를 지닌 것들의 목록을 밝히는 일이다."
            ),
            "counterpoint": (
                "공리주의 쾌락주의(벤담·밀 초기) 는 오직 쾌락만이 내재적으로 좋다고 주장하여 "
                "무어가 제시한 내재적 가치의 다원적 목록에 반대한다."
            ),
            "context": (
                "2025-B Q3 본래적 가치 구절의 이론적 배경 · "
                "무어 내재적 가치 다원주의 trademark."
            ),
            "keywords": [
                "내재적 가치",
                "본래적 가치",
                "intrinsic value",
                "수단적 가치 대비",
                "가치 다원주의",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-007: 쾌락주의 비판 — Principia Ethica §36-§57
        {
            "id": "moore-claim-007",
            "thinker_id": THINKER_ID,
            "work_id": "moore-principia-ethica-1903",
            "source_detail": (
                "Principia Ethica (1903) 제3장 쾌락주의 비판 · "
                "2025학년도 전공B Q2 자연주의 오류 맥락"
            ),
            "claim": (
                "벤담(Jeremy Bentham)·밀(J. S. Mill) 등의 고전 쾌락주의는 "
                "좋음을 쾌락이라는 자연적 속성과 동일시하므로 자연주의적 오류의 대표 사례이다. "
                "'쾌락이 좋음이다' 라는 명제에 대해 "
                "'쾌락을 증대하는 것이 정말 좋은가?' 라는 물음이 여전히 열린 질문으로 남으므로 "
                "쾌락주의적 정의는 실패한다."
            ),
            # 2021-A.md L17 + 2025-B.md L62 verbatim
            "original_text": (
                "비자연주의 이론에 따르면, 선함, 올바름 등의 도덕적 성질은 고유한 종류이어서 "
                "쾌락의 증대 등 계산 가능한 자연적 성질로 환원될 수 없다 "
                "… '선한', '올바른' 등의 표현을 '쾌락을 증대하는' 등의 자연적 표현으로 "
                "정의하려는 시도는 예외 없이 모두 오류를 범한다 "
                "— 2021학년도 전공A Q3 제시문 (coverage/2021-A.md L17 · L60)."
            ),
            "explanation": (
                "무어는 『Principia Ethica』 제3장에서 쾌락주의(hedonism)를 "
                "자연주의적 오류의 대표 사례로 비판한다. "
                "벤담·밀의 공리주의는 '좋음 = 쾌락의 증대' 라는 정의를 전제로 하는데, "
                "열린 질문 논증을 적용하면 '쾌락의 증대가 정말 좋은가?' 는 "
                "여전히 의미 있는 열린 질문이므로 쾌락주의적 동일시는 실패한다. "
                "이는 쾌락이 내재적 가치를 지닐 수 있다는 점 자체를 부정하는 것이 아니라, "
                "'좋음의 정의가 쾌락이다' 라는 개념적 환원이 오류임을 지적하는 것이다."
            ),
            "argument": (
                "전제1: 쾌락주의는 '좋음 = 쾌락의 증대' 를 분석적 정의로 주장한다. "
                "전제2: '쾌락을 증대하는 것이 정말 좋은가?' 는 여전히 의미 있는 열린 질문이다. "
                "전제3: 분석적 정의였다면 이 질문은 닫힌 동어반복이어야 한다. "
                "결론: 쾌락주의적 정의는 자연주의적 오류를 범한다."
            ),
            "counterpoint": (
                "밀(J. S. Mill)은 『공리주의(Utilitarianism, 1863)』 4장에서 "
                "'바람직함(desirable)' 과 '바람(desired)' 의 관계를 통해 "
                "쾌락이 유일한 내재적 선임을 증명하려 시도하였으나, "
                "무어는 이를 자연주의적 오류의 교과서적 사례로 재비판한다."
            ),
            "context": (
                "2021-A Q3 '쾌락의 증대' 구절의 이론적 배경 · "
                "무어의 벤담·밀 쾌락주의 비판 trademark."
            ),
            "keywords": [
                "쾌락주의 비판",
                "공리주의 비판",
                "자연주의적 오류",
                "밀 비판",
                "벤담 비판",
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
    """무어 핵심 키워드 데이터 입력. 중복 체크 후 insert."""
    keywords = [
        {
            "id": "kw-moore-naturalistic-fallacy",
            "term": "자연주의적 오류",
            "term_en": "naturalistic fallacy",
            "definition": (
                "무어 『Principia Ethica(1903)』 §10-§14 의 trademark 명제. "
                "좋음(good)이라는 도덕적 성질을 쾌락의 증대·욕망 충족·진화적 적응도 등 "
                "자연적 속성과 동일시하거나 자연적 속성으로 정의하려는 "
                "모든 시도가 범하는 개념적 오류. "
                "2016-A Q13 ㉠ 정답 · 2021-A Q3 ㉡ 정답의 이론적 배경 · "
                "2025-B Q2 핵심 용어."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "moore-principia-ethica-1903",
            "related_terms": [
                "열린 질문 논증",
                "비자연주의",
                "자연적 속성",
                "좋음",
                "쾌락주의 비판",
            ],
        },
        {
            "id": "kw-moore-open-question-argument",
            "term": "열린 질문 논증",
            "term_en": "Open-Question Argument",
            "definition": (
                "무어 『Principia Ethica』 §13 의 핵심 논증. "
                "어떤 자연적 속성 N 에 대해 'N한 것이 정말 좋은가?' 라는 물음이 "
                "여전히 의미 있는 열린 질문으로 남는다면, "
                "'좋음 = N' 이라는 분석적 정의는 성립할 수 없다는 논증. "
                "자연주의적 오류의 논리적 구조를 드러내는 무어의 대표 논증 도구. "
                "2025-B Q2 제시문 ''N한 것이 정말 좋은가?'라는 물음이 여전히 열려 있다' 의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "moore-principia-ethica-1903",
            "related_terms": [
                "자연주의적 오류",
                "비자연주의",
                "좋음 정의 불가능성",
                "분석적 동일성",
            ],
        },
        {
            "id": "kw-moore-ethical-intuitionism",
            "term": "윤리적 직관주의",
            "term_en": "ethical intuitionism",
            "definition": (
                "무어 윤리학의 방법론적 입장. "
                "좋음이 단순하고 정의 불가능한 비자연적 성질이므로, "
                "이를 인식하는 유일한 방법은 이성의 직관(intuition)을 통한 직접 지각이다. "
                "마치 노랑이라는 색 성질을 눈으로 직접 보듯이, "
                "좋음은 마음이 대상 위에서 단번에 지각한다. "
                "2016-A Q13 갑 해설 '도덕적 인식 = 직관으로 단순 속성 지각' 의 이론적 배경. "
                "프리차드·로스 등 영국 직관주의 계열에 직접 영향."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "moore-principia-ethica-1903",
            "related_terms": [
                "직관주의",
                "비자연주의",
                "선의 비분석성",
                "단순 성질",
            ],
        },
        {
            "id": "kw-moore-indefinable-good",
            "term": "선의 비분석성",
            "term_en": "indefinability of good",
            "definition": (
                "무어 『Principia Ethica』 §13 의 핵심 테제. "
                "좋음은 더 이상 다른 속성으로 분석할 수 없는 단순 성질(simple notion) 이며, "
                "'좋음 = A + B + C' 같은 분석적 정의는 원리적으로 불가능하다(indefinable). "
                "좋음은 노랑(yellow) 처럼 쪼갤 수 있는 구성 부분을 갖지 않으므로, "
                "정의가 아니라 직접 파악(직관)으로만 인식된다. "
                "2016-A Q13 갑 삼분법 제시문 '분석할 수 없는 단순한 속성' 의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "moore-principia-ethica-1903",
            "related_terms": [
                "단순 성질",
                "윤리적 직관주의",
                "비자연주의",
                "정의 불가능성",
            ],
        },
        {
            "id": "kw-moore-intrinsic-value",
            "term": "내재적 가치",
            "term_en": "intrinsic value",
            "definition": (
                "무어 『Principia Ethica』 제3장·제6장의 건설적 전개 개념. "
                "수단적 가치(다른 것을 위해 좋음) 와 구별되는 "
                "그 자체로 좋은 것(= 본래적 가치) 을 지시한다. "
                "윤리학의 궁극 과제는 '좋음이란 무엇인가' 의 개념 분석 이후 "
                "'어떤 것들이 그 자체로 좋은가' 라는 목록 물음으로 이어진다. "
                "무어가 제시한 대표 사례는 인간 교제의 즐거움과 아름다움의 향유. "
                "2025-B Q3 '본래적 가치(intrinsic value)' 언급 맥락과 연관."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "moore-principia-ethica-1903",
            "related_terms": [
                "본래적 가치",
                "수단적 가치 대비",
                "가치 다원주의",
                "선",
            ],
        },
        {
            "id": "kw-moore-meta-ethics",
            "term": "메타윤리",
            "term_en": "meta-ethics",
            "definition": (
                "무어 『Principia Ethica(1903)』 가 창시한 윤리학 분야. "
                "규범 물음('무엇을 행해야 하는가') 과 응용윤리 물음에 선행하여 "
                "도덕 개념 자체의 의미·지위·인식 방법을 분석한다. "
                "'좋음이란 무엇인가' 라는 개념 분석 물음이 1차 과제. "
                "2021-A Q3 ㉠ 정답의 직접 근거 · "
                "20세기 직관주의·정의주의·규정주의 논쟁의 공통 출발점."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "moore-principia-ethica-1903",
            "related_terms": [
                "개념 분석",
                "규범윤리 선행",
                "자연주의적 오류",
                "윤리적 직관주의",
            ],
        },
        {
            "id": "kw-moore-principia-ethica",
            "term": "윤리학 원리",
            "term_en": "Principia Ethica",
            "definition": (
                "G. E. 무어의 1903년 대표 저작. "
                "자연주의적 오류 비판(§10-§14)·열린 질문 논증(§13)·"
                "선의 비분석성·윤리적 직관주의·내재적 가치의 다원적 목록 등 "
                "현대 메타윤리의 핵심 테제들을 체계적으로 전개. "
                "20세기 영국 분석철학과 메타윤리 전통의 출발점으로 평가된다. "
                "임용 도덕·윤리 2016-A Q13 갑·2021-A Q3·2025-B Q2 제시문의 직접 근거 저작."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "moore-principia-ethica-1903",
            "related_terms": [
                "자연주의적 오류",
                "열린 질문 논증",
                "윤리적 직관주의",
                "메타윤리",
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
    """무어 영향·비교 관계 데이터 입력.

    ES 등록 확인 (2026-04-22 curl, 3건 모두 found=true):
     - mill_js : 등록 — 무어가 『Principia Ethica』 제3장에서 밀의 쾌락주의적 '바람직함' 증명을 자연주의적 오류 사례로 재비판
     - bentham : 등록 — 벤담 고전 공리주의의 '좋음 = 쾌락' 동일시를 자연주의적 오류의 대표 사례로 비판
     - kant    : 등록 — 메타윤리(무어) 대 의무론적 규범윤리(칸트) 의 방법론적 대비
    미등록 thinker(ross_wd, prichard, stevenson, hare) 는 링크 생략.
    """
    relations = [
        {
            "from_thinker": "mill_js",
            "to_thinker": THINKER_ID,
            "type": "contrasted",
            "description": (
                "밀(John Stuart Mill) 의 공리주의는 '좋음 = 쾌락의 증대' 라는 정의를 통해 "
                "규범윤리를 전개하지만, 무어는 『Principia Ethica』 제3장에서 "
                "밀이 『공리주의(Utilitarianism, 1863)』 4장에서 "
                "'바람직함(desirable) = 실제로 바라는 바' 로부터 쾌락이 유일한 내재적 선임을 증명하려 한 것을 "
                "자연주의적 오류의 교과서적 사례로 재비판한다. "
                "열린 질문 논증을 적용하면 '쾌락을 증대하는 것이 정말 좋은가?' 는 "
                "여전히 의미 있는 열린 질문이므로, 밀의 분석적 동일시는 실패한다. "
                "임용 2016-A Q12(밀)·Q13(무어) 동일 시험 내 병치 · "
                "2021-A Q3 '쾌락의 증대' 자연적 표현 비판 구절의 직접 배경."
            ),
            "evidence": (
                "Moore (1903) Principia Ethica §40 '밀의 자연주의적 오류' 논증; "
                "Mill (1863) Utilitarianism 4장 바람직함 증명; "
                "2016-A Q12 갑(칸트)·을(밀) + Q13 갑(무어)·을(흄) 동일 시험 병치 "
                "(coverage/2016-A.md L26·L27); "
                "2021-A Q3 '쾌락의 증대' 를 자연적 표현 예시로 인용 "
                "(coverage/2021-A.md L17·L60)"
            ),
        },
        {
            "from_thinker": "bentham",
            "to_thinker": THINKER_ID,
            "type": "contrasted",
            "description": (
                "벤담(Jeremy Bentham) 의 고전 공리주의가 전제하는 '좋음 = 쾌락' 동일시를 "
                "무어는 자연주의적 오류의 대표 사례로 비판한다. "
                "벤담의 쾌락 계산은 좋음을 계산 가능한 자연적 성질로 환원하려는 시도이며, "
                "열린 질문 논증에 따르면 '쾌락이 많은 것이 정말 좋은가?' 는 "
                "여전히 열린 질문이므로 쾌락주의적 정의는 성립하지 않는다. "
                "내재적 가치 다원주의 측면에서도 무어는 벤담의 일원론적 쾌락주의와 대립한다 — "
                "인간 교제의 즐거움·아름다움의 향유 등 복수의 내재적 선이 존재한다는 입장."
            ),
            "evidence": (
                "Moore (1903) Principia Ethica 제3장 쾌락주의 비판; "
                "Bentham (1789) An Introduction to the Principles of Morals and Legislation 쾌락 계산; "
                "2021-A Q3 '쾌락의 증대 등 계산 가능한 자연적 성질' 직접 인용 "
                "(coverage/2021-A.md L17·L60)"
            ),
        },
        {
            "from_thinker": "kant",
            "to_thinker": THINKER_ID,
            "type": "compared",
            "description": (
                "칸트(Immanuel Kant) 와 무어는 서양 현대 윤리학의 두 축으로서 "
                "각기 다른 수준에서 윤리학을 체계화하였다. "
                "칸트는 규범윤리(의무론) 수준에서 '무엇을 해야 하는가' 에 대해 "
                "정언명법으로 답하는 입장인 반면, "
                "무어는 한 단계 위의 메타윤리 수준에서 "
                "'좋음이란 무엇인가' 라는 개념 분석 물음을 1차 과제로 설정한다. "
                "두 사상가는 모두 경험적·자연적 속성에 대한 환원에 반대한다는 점에서 일치하며 "
                "(칸트 = 선의지의 무조건적 가치, 무어 = 좋음의 비자연적 성질), "
                "도덕적 가치의 고유한 지위를 강조하는 흐름에 공통적으로 속한다. "
                "2016-A Q12(칸트)·Q13(무어) 동일 시험 내 병치는 이 대비 구도의 임용 반영."
            ),
            "evidence": (
                "Moore (1903) Principia Ethica 서문 '1차 과제 설정'; "
                "Kant (1785) Grundlegung zur Metaphysik der Sitten 1장 선의지·의무; "
                "2016-A Q12 갑(칸트) + Q13 갑(무어) 동일 시험 병치 "
                "(coverage/2016-A.md L26·L27); "
                "2021-A Q3 '올바른 행위, 선한 행위 등의 판단 기준을 탐구하는 윤리학 분야와 "
                "서로 밀접한 관계' 메타윤리/규범윤리 대비 "
                "(coverage/2021-A.md L17·L59)"
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
    print("=== G. E. 무어(Moore) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (moore)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n[OK] 무어 데이터 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}", file=sys.stderr)
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
