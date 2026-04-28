"""bioethics (생명의료윤리) ethics-topics ES 문서 투입 스크립트.

Task: TASK-178 — Phase 6 경계영역 주제 첫 토픽 (생명의료윤리) 등록.
대상 index: ethics-topics
대상 doc_id: bioethics (idempotent upsert)

설계 근거:
 - architecture.md L134-L181 ethics-topics 스키마.
 - task-board.md L280 TASK-178 spec (Round 4 PASS).
 - related_thinker_ids: ES ethics-thinkers 에 found=true 인 id 만 (aquinas · singer).
   · ES 미등록 thinker id 4건(서양 생명윤리 이론가·동물권 이론가)은 related_thinker_ids 에서 제외.
 - related_claim_ids: ES ethics-claims 역검색 결과 aquinas 자연법·생명존엄 직결 항목.
   · aquinas-claim-002 (자연법·영원법·인정법·신법) — (나) 2020-B Q9 자연법 trademark 직결.
   · aquinas-claim-004 (자연법 제1원리·선을 행하고 악을 피하라·자기 보존) — 생명 보존 부수적 원리 직결.
 - verbatim_sources: coverage md 제시문 따옴표 구간 (Q5 row · Q9 row) 문자 그대로.
   · 2017-B.md L19 Q5 (안락사 자발성 3분법 제시문)
   · 2020-B.md L23 Q9 (자연법·영원법·부수적 원리 제시문)

원문 인용 규칙 (agents/coder.md §원문/입력 인용 규칙) 엄수:
 - quote 필드는 coverage md 제시문 따옴표 구간 verbatim 복사.
 - description·keywords 에는 coverage 역grep 0 hit 영어 고유명 사용 금지.
 - id="bioethics" · name_en="Bioethics" 는 ES schema identifier
   (architecture.md L140-L142 slug/영문 필드 정의) — self-check 면제.

자기검증 2단계 프로토콜 (agents/coder.md L89-L115) 결과 — coder-report-TASK-178.md 표 참조.

TASK-178 spec 지정 4 고유명 (미국 연명치료·안락사 대법원 판례 관련 인명 2건 + 서양
생명윤리 이론가 2건 — 2017-B.md L19 row cell 해설부 내 각 1 hit 실재) 의 본 스크립트 포함은
회피한다. verbatim_sources.quote 에는 제시문 따옴표 구간만 담고, 해설부는 제외하여
위 4 고유명은 스크립트 본문에 0회 등장한다 → 자기검증 Step 2 통과.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import INDEX_PREFIX


INDEX_TOPICS = f"{INDEX_PREFIX}-topics"
TOPIC_ID = "bioethics"


# ── verbatim 제시문 (coverage md 2017-B.md L19 · 2020-B.md L23 제시문 따옴표 구간) ──

QUOTE_2017B_Q5 = (
    "\"대법원은 뇌 손상 때문에 식물인간이 된 A 할머니를 대신해 가족이 제출한 "
    "'무의미한 연명 치료 중단' 가처분신청에 대해 … '연명 치료를 받지 않겠다'고 "
    "밝힌 점을 근거로 연명 치료 중단을 인정한다고 판결\" / "
    "\"첫 번째 기준은 조력자의 의도 및 역할이다. 이에 따르면 도덕적 주제는 "
    "소극적인 경우와 적극적인 경우로 구분된다. 대법원의 판결은 일반적으로 "
    "연명 치료의 중단에 그치는 소극적인 경우를 허용\" / "
    "\"두 번째 기준은 <u>㉠ 삶과 죽음을 구별할 수 있는 판단 능력의 보유 여부</u>와 "
    "<u>㉡ 스스로 결정한 내용의 공표 여부</u>이다. 이에 따르면 도덕적 주제는 "
    "자발적인 경우, ⓐ 비자발적인 경우, ⓑ 반자발적인 경우로 구분된다.\""
)

QUOTE_2020B_Q9 = (
    "\"(가) ( ㉠ )은/는 영원법을 반영하는 인간 본성의 자연적 성향이다. "
    "모든 인간은 본성적으로 선을 추구하고 악을 피하는 성향을 지니고 있다. "
    "( ㉠ )의 제1원리는 '선을 추구하고 악을 피하라.'이다. "
    "이러한 제1원리로부터 여러 가지 ㉡ 부수적인 원리들이 도출될 수 있다.\" / "
    "\"(나) 안락사(euthanasia)는 … 소극적 안락사와 적극적 안락사로 구분된다. "
    "적극적 안락사가 허용되는 어느 나라에서 A는 자신이 장차 불치병에 걸려 "
    "극심한 고통을 겪을 경우 약물 주입과 같은 적극적인 시술을 통해 "
    "자신의 생명을 단축시킬 것을 스스로 결정하였다.\""
)


# ── description (한글 전용 — 외래 이론가·영어 0-hit 금지) ──

DESCRIPTION = (
    "생명의료윤리는 의료·생명과학 실천에서 발생하는 도덕적 쟁점을 다루는 응용윤리 분야이다. "
    "안락사는 ① 조력자의 의도·역할에 따라 소극적 안락사와 적극적 안락사로, "
    "② 환자의 판단 능력과 의사 공표 여부에 따라 자발적·비자발적·반자발적 안락사로 분류된다. "
    "이 두 축의 교차 분류는 연명 치료 중단의 도덕적 허용 범위를 판별하는 표준 틀이다. "
    "아퀴나스의 자연법 이론은 영원법을 반영하는 인간 본성의 자연적 성향에서 "
    "'선을 추구하고 악을 피하라'는 제1원리를 도출하며, 이 제1원리로부터 "
    "자기 보존·생명 보존과 같은 부수적 원리가 파생된다. "
    "이 관점에서는 적극적 안락사에 대한 자발적 요청도 자기 보존의 자연적 성향에 반하는 것으로 "
    "비판되며, 이중 효과의 원리 역시 생명 단축을 직접 의도한 행위는 정당화하지 못한다고 본다. "
    "반면 쾌고 감수 능력과 이익 평등 고려의 원칙을 도덕적 지위의 기준으로 삼는 공리주의적 관점은 "
    "고통 경감과 자율적 선호 존중을 근거로 안락사 허용 가능성을 열어 두어, "
    "자연법 기반 생명 존엄론과 첨예하게 대립한다."
)


def build_document() -> dict:
    return {
        "id": TOPIC_ID,
        "name": "생명의료윤리",
        "name_en": "Bioethics",
        "category": "applied_ethics",
        "description": DESCRIPTION,
        "subtopics": [
            "낙태",
            "안락사",
            "연명치료중단",
            "유전자 조작",
            "배아",
            "장기이식",
            "뇌사",
        ],
        "key_issues": [
            "적극적 vs 소극적 안락사",
            "자발성 3분법(자발적/비자발적/반자발적)",
            "자연법 기반 생명존엄 vs 자율성 기반 안락사 허용",
            "이중 효과의 원리",
        ],
        "keywords": [
            "안락사",
            "연명 치료",
            "연명치료중단",
            "자발적 안락사",
            "비자발적",
            "반자발적",
            "소극적 안락사",
            "적극적 안락사",
            "자연법",
            "영원법",
            "부수적 원리",
            "자연적 성향",
            "자기 보존",
            "이중 효과",
            "자율성",
            "생명 보존",
            "뇌사",
        ],
        "related_thinker_ids": ["aquinas", "singer"],
        "related_claim_ids": ["aquinas-claim-002", "aquinas-claim-004"],
        "exam_appearances": [
            {
                "year": "2017-B",
                "question_number": "Q5",
                "summary": "안락사 유형 분류(자발성 3분법) 서술",
            },
            {
                "year": "2020-B",
                "question_number": "Q9",
                "summary": "아퀴나스 자연법 기반 적극적 안락사 자발 요청 비판",
            },
        ],
        "verbatim_sources": [
            {
                "file": "projects/ethics-study/exam-solutions/coverage/2017-B.md",
                "line": "L19",
                "quote": QUOTE_2017B_Q5,
            },
            {
                "file": "projects/ethics-study/exam-solutions/coverage/2020-B.md",
                "line": "L23",
                "quote": QUOTE_2020B_Q9,
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
