"""environmental-ethics (환경윤리) ethics-topics ES 문서 투입 스크립트.

Task: TASK-181 — Phase 6 경계영역 주제 Track A 마무리 (환경윤리) 등록.
대상 index: ethics-topics
대상 doc_id: environmental-ethics (hyphen — architecture.md L140/L177 예시 전부 hyphen)

설계 근거:
 - architecture.md L134-L181 ethics-topics 스키마.
 - task-board.md L292 TASK-181 spec (Round 2 PASS).
 - related_thinker_ids: ES ethics-thinkers 에 found=true 인 id 3건 (leopold · taylor_p · singer).
   · ES 미등록 thinker id 4건(심층생태학·전체론 이론가 — 네스·regan·롤스턴·캘리콧 slug) 제외.
 - related_claim_ids: ES ethics-claims 역검색 결과 환경윤리 직결 항목 7건.
   · leopold-claim-001 (대지윤리·3단계 윤리 확장)
   · leopold-claim-002 (호모 사피엔스 역할 전환 — 정복자에서 평범한 구성원·시민)
   · leopold-claim-003 (생명 공동체 통합성·안정성·아름다움 표어)
   · taylor_p-claim-001 (목적론적 삶의 중심 · 고유한 선)
   · taylor_p-claim-002 (고유한 선 claim)
   · taylor_p-claim-003 (내재적 가치 claim)
   · taylor_p-claim-004 (고유한 선 vs 내재적 가치 구분 — 사실/당위)
 - verbatim_sources: coverage md 제시문 따옴표 구간 (Q9 row · Q12 을 blockquote) 문자 그대로.
   · 2021-A.md L23 Q9 row cell (taylor_p 생명중심주의 제시문)
   · 2026-A.md L604 Q12 을 blockquote (leopold 대지윤리 제시문)

원문 인용 규칙 (agents/coder.md §원문/입력 인용 규칙) 엄수:
 - quote 필드는 coverage md 제시문 따옴표 구간 verbatim 복사.
 - 괄호 영문 (inherent worth) 식 괄호 안 영어·markdown 강조 `**...**`·HTML `<u>`
   태그 등은 byte-level 보존 (TASK-178-FIX 선례 엄수).
 - description·keywords 에는 coverage 역grep 0 hit 영어 고유명 사용 금지.
 - id="environmental-ethics" · name_en="Environmental Ethics" · category="applied_ethics"
   는 ES schema identifier (architecture.md L140-L143) — self-check 면제.

자기검증 2단계 프로토콜 (agents/coder.md L89-L115) 결과 — coder-report-TASK-181.md 표 참조.

TASK-181 spec 부정 키워드 0-hit (서양 심층생태학·전체론 이론가 4인 — coverage md
전수 역grep 0 hit) 는 본 스크립트 본문에 0회 등장 확인 — 자기검증 Step 2 통과.
제한 사용 (coverage hit≥1 실재) 사상가 고유명 3인은 related_thinker_ids 에만 slug
(leopold · taylor_p · singer) 로 등장하며, TitleCase 영어 고유명은 본문 미등장.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import INDEX_PREFIX


INDEX_TOPICS = f"{INDEX_PREFIX}-topics"
TOPIC_ID = "environmental-ethics"


# ── verbatim 제시문 ──
# 원천: 2021-A.md L23 Q9 row cell (taylor_p) · 2026-A.md L604 Q12 을 blockquote (leopold).
# markdown 강조 `**...**` · 괄호 영문 `(inherent worth)` 식 byte-level 보존.

QUOTE_2021A_Q9_TAYLOR = (
    "\"◦ 생명체는 자신의 보존에 힘쓰고, 자기의 선을 실현하는 고유 방식을 지닌 "
    "( ㉠ )이다. 생명체가 ( ㉠ )(이)라는 것은 그 내적 작동뿐 아니라 외적 활동 "
    "모두 목표 지향적이라는 것이다. 생명체는 시간을 넘어 자신의 존재를 유지하고, "
    "자기 종을 재생산하며 나아가 변화무쌍한 환경에서 사건 및 상황 등에 계속 "
    "적응한다. 곧 생명체는 재생산과 적응의 생물학적 과정을 잘 수행하게 하는 "
    "경향성을 지닌다. / ◦ 우리에게는 인간에 대한 도덕적 의무와 더불어 야생 "
    "생명체 자체에 대한 의무도 있다. 야생 생명체에 대한 의무는 인간에 대한 "
    "도덕적 의무에 예속되거나 의존하지 않는다. 물론 야생 생명체는 우선적 "
    "의미에서의 도덕적 권리를 지니지 않는다. 그럼에도 인간을 존중해야 하는 "
    "것과 마찬가지로 ㉡ 야생 생명체도 존중해야 한다.\""
)

QUOTE_2026A_Q12_LEOPOLD = (
    "> 을: \"**최초의 윤리는 개인 간의 관계를 다루었다. 뒤에 개인과 사회의 "
    "관계가 덧붙여졌다. 그러나 아직까지 인간과 ( ㉡ ) 및 그 위에서 살아가는 "
    "동식물과의 관계를 다루는 윤리는 없다. ( ㉡ ) 윤리는 호모 사피엔스의 "
    "역할을 ( ㉡ ) 공동체의 정복자에서 그것의 평범한 구성원이자 시민으로 "
    "변화시킨다**. …(중략)… **바람직한 ( ㉡ ) 이용을 오직 경제적 문제로만 "
    "생각하지 말라. 무엇이 경제적으로 이익인지 뿐만 아니라 윤리적, 심미적으로 "
    "무엇이 옳은지의 측면에서도 각각의 질문을 검토하라**. **어떤 것이 생명 "
    "공동체의 통합성, 안정성, 아름다움의 보전에 이바지하는 경향이 있다면, "
    "그것은 옳다. 그렇지 않다면 그르다**.\""
)


# ── description (한글 전용 — 외래 이론가·영어 0-hit 금지) ──

DESCRIPTION = (
    "환경윤리는 인간 외 자연(동식물·생태계·대지)의 도덕적 지위와 인간의 환경적 책임을 "
    "다루는 응용윤리 분야이다. 도덕적 고려 범위를 어디까지 확장할 것인지를 기준으로 "
    "① 인간중심주의, ② 동물중심주의, ③ 생명중심주의, ④ 생태계중심주의(전체론)로 분류된다. "
    "생명중심주의는 모든 유기체가 자기 보존·자기 선 실현·재생산·환경 적응을 목표 지향적으로 "
    "수행하는 '목적론적 삶의 중심'으로서 고유한 선을 지니며, 도덕 행위자가 자연 존중의 "
    "태도를 받아들일 때 그 고유한 선이 내재적 가치로 인정된다고 본다(개체주의적 환경윤리). "
    "생태계중심주의는 도덕적 고려 단위를 개체가 아닌 생명 공동체·생태계·대지 등 전체에 "
    "두며, 대지윤리의 표어 '어떤 것이 생명 공동체의 통합성·안정성·아름다움의 보전에 "
    "이바지하는 경향이 있다면 옳고, 그렇지 않다면 그르다'가 전체론적 규범의 원형이다. "
    "대지윤리는 윤리의 3단계 확장(개인 간 관계 → 개인과 사회 관계 → 인간과 대지 관계)을 "
    "제시하고, 호모 사피엔스의 역할을 대지 공동체의 정복자에서 평범한 구성원이자 시민으로 "
    "전환할 것을 요구한다. 심층생태학은 인간을 자연 전체와 분리 불가능한 관계망의 일부로 "
    "보는 전체론적 관점을 심화한다. 개체주의(생명중심주의)와 전체론(생태계중심주의)은 "
    "멸종위기 종 보존을 위한 과잉번식 개체 솎아내기와 같은 딜레마에서 대립한다."
)


def build_document() -> dict:
    return {
        "id": TOPIC_ID,
        "name": "환경윤리",
        "name_en": "Environmental Ethics",
        "category": "applied_ethics",
        "description": DESCRIPTION,
        "subtopics": [
            "인간중심주의",
            "동물중심주의",
            "생명중심주의",
            "생태계중심주의",
            "심층생태학",
            "대지윤리",
            "환경정의",
            "미래세대 책임",
        ],
        "key_issues": [
            "개체주의(생명중심주의) vs 전체론(생태계중심주의)",
            "도덕적 고려 범위의 확장",
            "인간 vs 비인간 자연의 도덕적 지위",
            "대지윤리 표어 — 생명 공동체 통합성·안정성·아름다움",
        ],
        "keywords": [
            "환경윤리",
            "생명중심주의",
            "생태계 중심주의",
            "대지윤리",
            "심층생태학",
            "인간중심주의",
            "목적론적 삶의 중심",
            "고유한 선",
            "내재적 가치",
            "본래적 가치",
            "자연 존중",
            "야생 생명체",
            "유기체",
            "생명 공동체",
            "통합성",
            "안정성",
            "아름다움",
            "호모 사피엔스",
            "정복자",
            "평범한 구성원",
        ],
        "related_thinker_ids": ["leopold", "taylor_p", "singer"],
        "related_claim_ids": [
            "leopold-claim-001",
            "leopold-claim-002",
            "leopold-claim-003",
            "taylor_p-claim-001",
            "taylor_p-claim-002",
            "taylor_p-claim-003",
            "taylor_p-claim-004",
        ],
        "exam_appearances": [
            {
                "year": "2021-A",
                "question_number": "Q9",
                "summary": (
                    "taylor_p 생명중심주의·목적론적 삶의 중심 centerpiece "
                    "(레오폴드·네스 ecocentrism 비교)"
                ),
            },
            {
                "year": "2026-A",
                "question_number": "Q12",
                "summary": (
                    "taylor_p(갑) vs leopold(을) 직접 대비 — 생명중심주의 vs 대지윤리"
                ),
            },
        ],
        "verbatim_sources": [
            {
                "file": "projects/ethics-study/exam-solutions/coverage/2021-A.md",
                "line": "L23",
                "quote": QUOTE_2021A_Q9_TAYLOR,
            },
            {
                "file": "projects/ethics-study/exam-solutions/coverage/2026-A.md",
                "line": "L604",
                "quote": QUOTE_2026A_Q12_LEOPOLD,
            },
        ],
    }


def upsert_topic(client) -> None:
    doc = build_document()
    result = client.index(index=INDEX_TOPICS, id=TOPIC_ID, document=doc)
    print(f"[topic] {TOPIC_ID}: {result['result']}")


def main() -> None:
    client = get_client()
    try:
        upsert_topic(client)
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
