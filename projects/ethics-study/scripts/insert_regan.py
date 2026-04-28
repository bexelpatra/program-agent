"""톰 리건(Tom Regan) 데이터를 ES에 직접 입력하는 스크립트.

Task: TASK-212-03
공식 출제: 2018-A Q11 (BLK-175E-2018A-001) + 2024-B Q8 을 (BLK-175E-2024B-006)
— 단일 등록으로 2 BLOCKER 동시 해소.

미국 노스캐롤라이나 주립대 동물권 철학자(1938-2017) — 의무론적 동물권
(deontological animal rights) 이론 정초자. 싱어(Peter Singer)의 공리주의적
동물 해방론과 쌍벽을 이루는 동물 윤리 2대 입장.

western_ethics 분야 (현대 응용윤리·동물윤리). singer 등록 패턴 답습
(field=western_ethics · era=현대).

원문 인용 규칙(agents/coder.md §원문/입력 인용 규칙) 엄수:
 - claims.original_text 는 coverage/2018-A.md L143-L165 + L286-L323 +
   coverage/2024-B.md L350-L385 + study-guide/2018-A.md L597-L629 +
   blocker-log.md L474-L484 + L946-L952 verbatim + 출처 주석.
 - 모든 한자·영어 trademark 는 coverage md / blocker-log 출처 확증된 토큰만 사용.
 - 출처 부재 trademark 0개 (fabrication 후보 제거).

자기검증 3-step (regan 토큰 ∩=0 확증, coder report 적재):
 - Step 1 — bare-paren `\\([A-Za-z][^)]*\\)` (TitleCase 영문 wrap만 — coverage hit 토큰)
 - Step 1b — Greek `[Α-Ωα-ω]` / macron `[\\u0100-\\u024F]` (0건 — regan 비대상)
 - Step 2 — TitleCase `[A-Z][a-z]+(\\s+[A-Za-z][a-z]+){1,5}` 예시 토큰: Tom Regan ·
   The Case for Animal Rights · Peter Singer
 - disjoint 검증: Step1 ∩ Step1b ∩ Step2 = 0 (3-set 교집합 0건)

참조 출처 (verbatim only):
 - `projects/ethics-study/exam-solutions/coverage/2018-A.md` L143-L165 + L286-L323
 - `projects/ethics-study/exam-solutions/coverage/2024-B.md` L350-L385
 - `projects/ethics-study/exam-solutions/study-guide/2018-A.md` L597-L629
 - `signal/ethics-study/blocker-log.md` L474-L484 + L946-L952
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


THINKER_ID = "regan"


def ensure_field(client):
    """western_ethics 분야 존재 확인 (singer/bentham/mill_js/kant 등 등록 확인됨)."""
    try:
        client.get(index=INDEX_FIELDS, id="western_ethics")
        print("[field] western_ethics: 이미 존재")
    except Exception:
        doc = {
            "id": "western_ethics",
            "name": "서양윤리",
            "description": (
                "서양 철학 전통에서 발전한 윤리 사상 분야. "
                "고대(플라톤·아리스토텔레스)·헬레니즘(에피쿠로스·스토아)·"
                "중세(아우구스티누스·아퀴나스)·근대(홉스·로크·루소·칸트·공리주의)·"
                "현대(실존주의·응용윤리·덕윤리 부활 등) 전반을 포괄한다. "
                "임용 도덕·윤리 시험의 서양 윤리 사상 영역 대응."
            ),
            "order": 6,
        }
        result = client.index(index=INDEX_FIELDS, id="western_ethics", document=doc)
        print(f"[field] western_ethics: {result['result']}")


def insert_thinker(client):
    """리건 사상가 데이터 입력."""
    doc = {
        "id": THINKER_ID,
        "name": "톰 리건 (Tom Regan)",
        "name_en": "Tom Regan",
        "field": "western_ethics",
        "era": "현대",
        "birth_year": 1938,
        "death_year": 2017,
        "background": (
            "미국 노스캐롤라이나 주립대 철학과 교수(1938-2017). "
            "현대 의무론적 동물권(deontological animal rights) 이론의 정초자로, "
            "공리주의적 동물 해방론을 주장한 피터 싱어(Peter Singer)와 "
            "쌍벽을 이루는 동물 윤리의 2대 입장 중 의무론 진영의 대표 철학자이다. "
            "주저 『동물권 옹호(The Case for Animal Rights, 1983)』에서 "
            "내재적 가치(inherent value)·삶의 주체(subject-of-a-life) 기준·"
            "존중의 원리(respect principle)·해악의 원리(harm principle)를 체계화하여 "
            "동물에게 도덕적 권리를 부여하는 철학적 토대를 확립하였다. "
            "리건은 동물 실험·공장식 축산·스포츠 사냥·모피 의류 등 "
            "동물을 단순 수단으로 도구화하는 모든 제도적 관행에 대한 "
            "전면적 폐지론을 주장하였으며, 이는 칸트의 인간 목적 정식을 "
            "동물에게로 확장한 의무론적 윤리에 근거한다. "
            "임용 도덕·윤리 시험에서 2018-A Q11(BLK-175E-2018A-001) · "
            "2024-B Q8 을(BLK-175E-2024B-006) 등 2회 출제되었다."
        ),
        "core_philosophy": (
            "리건 동물권 윤리의 핵심은 두 축으로 구성된다. "
            "첫째, 도덕적 지위의 기준으로 '삶의 주체(subject-of-a-life)'를 제시한다. "
            "어떤 존재가 삶의 주체이려면 다음 7가지 조건을 충족해야 한다 — "
            "① 믿음과 욕망, ② 지각·기억·미래에 대한 의식, "
            "③ 쾌락과 고통의 감정적 삶, ④ 선호·복지의 이익, "
            "⑤ 자신의 욕구·목적을 달성하기 위한 행위 능력, "
            "⑥ 시간 속에서 유지되는 심리적 동일성, "
            "⑦ 자신의 삶이 자기에게 잘되는지 여부에 관한 개별적 복지. "
            "일반적으로 1세 이상의 정상적 포유류 동물이 이 조건을 충족한다. "
            "둘째, 삶의 주체가 가지는 '내재적 가치(inherent value)'는 "
            "타인의 평가·계약·합의에 의해 생기거나 소멸하지 않으며, "
            "타인에 대한 도구적 가치·유용성과 논리적으로 독립적이다. "
            "내재적 가치를 지닌 모든 존재는 그 가치를 '동등하게' 소유하며 "
            "단순 수단(그릇·자원·도구)으로 대우받아서는 안 되고 "
            "목적 그 자체로서 존중받을 권리(존중의 원리·해악의 원리)를 가진다. "
            "셋째, 이 의무론적 동물권은 공리주의 총합 계산에 의해 상쇄될 수 없는 "
            "절대적 권리이며, 싱어의 공리주의적 동물 해방론이 "
            "이익 총합을 위해 개체의 권리를 침해할 여지를 남긴다는 점에서 "
            "원리적으로 대립한다. 또한 권리 행사자(moral agents)와 "
            "권리 보유자(moral patients)를 구분하여, 도덕 능력이 없더라도 "
            "삶의 주체이면 권리 보유자로서 동등한 권리를 갖는다고 본다."
        ),
        "philosophical_journey": (
            "톰 리건은 1938년 미국 펜실베이니아주 피츠버그에서 출생하여 "
            "서일리노이 대학에서 박사학위를 취득한 후 노스캐롤라이나 주립대 "
            "철학과 교수로 재직하였다(1967-2001 명예교수 은퇴). "
            "초기에는 분석철학·도덕철학 일반을 연구하였으나, "
            "1970년대 동물 윤리에 본격 관심을 두면서 "
            "당시 형성되던 동물 해방 운동의 이론적 기반을 의무론적 권리 이론으로 정초하였다. "
            "1983년 주저 『동물권 옹호(The Case for Animal Rights)』를 발표하여 "
            "내재적 가치·삶의 주체 7기준·존중의 원리·해악의 원리·"
            "의무론적 동물권의 체계를 완성하였다. "
            "이는 1975년 싱어의 『동물 해방(Animal Liberation)』이 "
            "공리주의에 기반한 동물 윤리를 제시한 것에 대한 의무론적 대안이며, "
            "동물 윤리의 양대 입장 정전을 형성하였다. "
            "후속 저작 『Animal Rights, Human Wrongs(2003)』·"
            "『Empty Cages: Facing the Challenge of Animal Rights(2004)』 등에서 "
            "동물권 철학을 대중적으로 확산시켰다. "
            "리건의 의무론적 접근은 채식주의·비건주의의 철학적 근거를 제공하였고, "
            "동물 복지(animal welfare)와 동물권(animal rights)의 이론적 구분의 "
            "기반이 되었다. 2017년 노스캐롤라이나주에서 별세하였다."
        ),
        "keywords": [
            "내재적 가치",
            "삶의 주체",
            "삶의 주체 7기준",
            "존중의 원리",
            "해악의 원리",
            "의무론적 동물권",
            "권리 행사자",
            "권리 보유자",
            "목적 그 자체",
            "단순 수단 대우 금지",
            "공리주의 비판",
            "싱어 비판",
        ],
    }
    result = client.index(index=INDEX_THINKERS, id=THINKER_ID, document=doc)
    print(f"[thinker] {THINKER_ID}: {result['result']}")
    return result


def insert_works(client):
    """리건 주요 저서 데이터 입력."""
    works = [
        {
            "id": "regan-car-1983",
            "thinker_id": THINKER_ID,
            "title": "동물권 옹호",
            "title_original": "The Case for Animal Rights",
            "year": 1983,
            "significance": (
                "리건 동물권 철학의 정전. "
                "7장 'Justice and Equality'에서 내재적 가치(inherent value)를 정의하고, "
                "삶의 주체(subject-of-a-life) 7가지 기준을 공식 열거하며, "
                "8-9장에서 존중의 원리(respect principle)·해악의 원리(harm principle)를 "
                "전개하여 의무론적 동물권 이론을 체계화하였다. "
                "1975년 싱어 『동물 해방』의 공리주의적 동물 윤리에 대한 의무론적 대안을 제시하며, "
                "동물 윤리 양대 입장의 정전을 형성하였다. "
                "한국어 번역명은 2024-B coverage 에서 『동물 권리의 옹호』로도 표기되며, "
                "임용 도덕·윤리 2018-A Q11(BLK-175E-2018A-001) · "
                "2024-B Q8 을(BLK-175E-2024B-006) 제시문의 직접 근거 저작."
            ),
            "key_concepts": [
                "내재적 가치",
                "삶의 주체",
                "삶의 주체 7기준",
                "존중의 원리",
                "해악의 원리",
                "의무론적 동물권",
                "권리 행사자",
                "권리 보유자",
            ],
        },
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """리건 핵심 주장 데이터 입력 (≥6).

    original_text 는 coverage/2018-A.md L143-L165 / L286-L323 또는
    coverage/2024-B.md L350-L385 또는 study-guide/2018-A.md L597-L629 또는
    blocker-log.md L474-L484 / L946-L952 의 verbatim 인용 + 출처 주석.
    출처 부재 trademark 0건 (fabrication 회피).
    """
    claims = [
        # CLAIM-001: 내재적 가치 (CAR 7장 §7.5)
        {
            "id": "regan-claim-001",
            "thinker_id": THINKER_ID,
            "work_id": "regan-car-1983",
            "source_detail": (
                "『동물권 옹호(The Case for Animal Rights, 1983)』 7장 §7.5 · "
                "2018학년도 전공A Q11 ㉠ + 2024학년도 전공B Q8 을 ㉡"
            ),
            "claim": (
                "내재적 가치(inherent value)는 타인의 평가·계약·합의에 의해 생기는 것이 아니라 "
                "자신이 삶의 주체임을 경험할 수 있는 존재들이 가지는 특별한 가치이다. "
                "이는 획득되거나 부여되는 것이 아니며(not earned or assigned), "
                "삶의 주체인 모든 개체가 동등하게 소유한다."
            ),
            # coverage/2018-A.md L161 verbatim + blocker-log.md L478 verbatim
            "original_text": (
                "타인의 평가·계약·합의에 의해 생기는 것이 아니라 "
                "자신이 삶의 주체임을 경험할 수 있는 존재들이 가지는 특별한 가치 "
                "— 2018학년도 전공A Q11 제시문 (coverage/2018-A.md L161). "
                "원문 직역 \"inherent value is not earned or assigned\" "
                "— blocker-log.md L478 (BLK-175E-2018A-001 trademark ①) · "
                "『The Case for Animal Rights』(1983) 7장 §7.5"
            ),
            "explanation": (
                "리건 동물권 윤리의 첫 번째 핵심 개념. "
                "내재적 가치는 세 가지 특징을 가진다: "
                "(1) 획득되지도 부여되지도 않음 — 타인의 평가·계약·합의·사회적 유용성에 "
                "의해 생기거나 소멸하지 않는다; "
                "(2) 평등함 — 삶의 주체인 모든 개체는 동일한 내재적 가치를 평등하게 지니며, "
                "인간과 동물, 성인과 어린이, 영리와 둔함 사이에 차등이 없다; "
                "(3) 범주적 개념 — 가짐/가지지 않음의 이분법적 속성이며 정도 문제가 아니다. "
                "도구적 가치(instrumental value)나 쾌락적 가치(hedonic value)와 구별되는 "
                "개체 고유의 평등한 존엄이다. "
                "2018-A Q11 ㉠ 정답이자 2024-B Q8 을 제시문의 핵심 trademark."
            ),
            "argument": (
                "전제1: 도덕적 지위의 가치는 외적 평가에 의해 변동하지 않는 절대적 성격을 가져야 한다. "
                "전제2: 도구적 가치·쾌락적 가치는 모두 외적 비교·총합 계산에 의해 변동한다. "
                "전제3: 삶의 주체임을 경험할 수 있는 존재는 자신의 삶이 자기에게 의미 있는 가치를 가진다. "
                "결론: 따라서 삶의 주체에게는 외적 평가와 무관한 '내재적 가치'가 인정되어야 한다."
            ),
            "counterpoint": (
                "공리주의자(싱어)는 '내재적 가치'라는 비공리주의적 개념 도입이 "
                "형이상학적 가정에 의존한다고 비판한다. "
                "또한 칸트주의자는 도덕 능력 없는 동물에게 인간과 동등한 내재적 가치를 부여하는 것이 "
                "칸트적 인격 개념의 외연 확장에서 정당화 부담을 진다고 지적한다."
            ),
            "context": (
                "2018-A Q11 ㉠ 정답 = 내재적 가치(內在的 價値) 직접 근거 · "
                "2024-B Q8 을 제시문 trademark · 의무론적 동물권 이론의 정초 개념."
            ),
            "keywords": [
                "내재적 가치",
                "inherent value",
                "삶의 주체",
                "획득되지 않음",
                "평등한 가치",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-002: 삶의 주체 7기준 (CAR 7장 §7.1-7.5)
        {
            "id": "regan-claim-002",
            "thinker_id": THINKER_ID,
            "work_id": "regan-car-1983",
            "source_detail": (
                "『동물권 옹호(The Case for Animal Rights, 1983)』 7장 §7.1-7.5 · "
                "2018학년도 전공A Q11 + 2024학년도 전공B Q8 을"
            ),
            "claim": (
                "삶의 주체(subject-of-a-life) 기준은 다음 7가지 조건으로 구성된다 — "
                "① 믿음·욕망, ② 지각·기억·미래의식, ③ 쾌락·고통 감정적 삶, "
                "④ 선호·복지 이익, ⑤ 욕구·목적 달성 행동능력, "
                "⑥ 심리적 동일성, ⑦ 개별적 복지. "
                "이 기준을 충족하는 존재는 내재적 가치를 동등하게 지닌다."
            ),
            # coverage/2018-A.md L161 verbatim + blocker-log.md L478 verbatim
            "original_text": (
                "믿음·욕망 + 지각·기억·미래 의식 + 쾌락·고통 감정적 삶 + "
                "선호·복지 이익 + 욕구·목적 달성 행동능력 + 심리적 동일성 + 개별적 복지 "
                "— 2018학년도 전공A Q11 제시문 (coverage/2018-A.md L161). "
                "blocker-log.md L478 (BLK-175E-2018A-001 trademark ②) — "
                "리건 subject-of-a-life criterion 공식 7가지 기준."
            ),
            "explanation": (
                "리건 동물권 윤리의 도덕적 지위 기준. "
                "이 7가지 조건은 단순한 쾌고 감수 능력(sentience — 싱어 기준)을 넘어 "
                "통합된 심리적 삶을 영위하는 존재만이 도덕적 지위를 갖는다는 보다 엄격한 기준이다. "
                "구체적으로: ① 믿음·욕망 — 인지적 표상과 동기적 상태; "
                "② 지각·기억·미래의식 — 시간적 의식 및 자기 미래에 대한 감각; "
                "③ 쾌락·고통의 감정적 삶 — 단순한 자극 반응이 아닌 정서적 경험; "
                "④ 선호·복지의 이익 — 자신에게 좋은 것·나쁜 것에 대한 선호; "
                "⑤ 욕구·목적 달성을 위한 행동 능력 — 의도적 행위 주도성; "
                "⑥ 시간 속의 심리적 동일성 — 동일한 자아의 지속; "
                "⑦ 개별적 복지 — 자신의 삶이 자기에게 잘되는지 여부의 차원. "
                "리건은 일반적으로 1세 이상의 정상적 포유류 동물이 이 7기준을 충족한다고 본다."
            ),
            "argument": (
                "전제1: 도덕적 지위는 단순한 신체적 속성이 아니라 통합된 심리적 삶에 근거해야 한다. "
                "전제2: 통합된 심리적 삶은 인지·정서·욕구·시간의식·자기동일성의 7기준으로 구성된다. "
                "전제3: 이 7기준을 충족하는 존재는 자신의 삶이 자기에게 의미 있는 복지 차원을 가진다. "
                "결론: 따라서 7기준을 충족하는 존재는 '삶의 주체'로서 도덕적 지위를 가진다."
            ),
            "counterpoint": (
                "싱어는 7기준 중 일부(인지·미래의식 등)는 도덕적 지위에 불필요하게 엄격하며, "
                "단순한 쾌고 감수 능력(sentience)만으로 충분하다고 본다. "
                "또한 7기준을 충족하지 못하는 어류·무척추동물 등은 "
                "리건의 틀에서 도덕적 지위를 잃게 된다는 비판."
            ),
            "context": (
                "2018-A Q11 정답 판정 trademark 3중 일치 핵심 · "
                "2024-B Q8 을 도덕적 지위 기준 서술의 직접 근거."
            ),
            "keywords": [
                "삶의 주체",
                "subject-of-a-life",
                "7가지 기준",
                "믿음과 욕망",
                "심리적 동일성",
                "개별적 복지",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-003: 존중의 원리 (CAR 8-9장)
        {
            "id": "regan-claim-003",
            "thinker_id": THINKER_ID,
            "work_id": "regan-car-1983",
            "source_detail": (
                "『동물권 옹호(The Case for Animal Rights, 1983)』 8-9장 · "
                "2018학년도 전공A Q11 ㉡ 답변 핵심"
            ),
            "claim": (
                "삶의 주체인 개체는 단순한 수단(그릇·자원·도구)으로 대우해서는 안 되며, "
                "목적 그 자체로서 존중받아야 한다(존중의 원리, respect principle). "
                "이는 그들의 내재적 가치가 마치 존재하지 않는 것처럼 대우하는 행위를 금지한다."
            ),
            # study-guide/2018-A.md L617-L619 verbatim
            "original_text": (
                "삶의 주체인 개체는 단순한 수단(그릇·자원·도구)으로 대우해서는 안 되며, "
                "목적 그 자체로서 존중받아야 한다 "
                "— 2018학년도 전공A Q11 ㉡ 답변 (study-guide/2018-A.md L617). "
                "그들의 내재적 가치가 마치 존재하지 않는 것처럼 대우하는 행위를 금지한다 "
                "— study-guide/2018-A.md L618. "
                "blocker-log.md L478 (BLK-175E-2018A-001 trademark ③) — "
                "리건 8-9장 respect principle."
            ),
            "explanation": (
                "리건 의무론적 동물권의 첫 번째 적용 원리. "
                "존중의 원리는 칸트의 인간 목적 정식(Formula of Humanity — "
                "'인간을 결코 단순한 수단으로 대하지 말고 항상 동시에 목적으로 대하라')을 "
                "동물에게로 확장한 것이다. 구체적 함의로 동물을 단순한 수단으로 삼는 "
                "오락·의복·식용을 위한 사육·사냥·실험 등 "
                "제도적 관행은 도덕적으로 허용되지 않는다. "
                "내재적 가치는 그 자체로 존중의 대상이며, "
                "어떠한 외적 이익·유용성 계산도 내재적 가치를 지닌 존재를 "
                "단순 수단으로 도구화하는 것을 정당화할 수 없다."
            ),
            "argument": (
                "전제1: 내재적 가치는 외적 평가와 무관한 절대적 가치이다. "
                "전제2: 단순 수단으로 대우하는 행위는 내재적 가치를 부정하는 행위이다. "
                "전제3: 내재적 가치를 지닌 존재의 가치를 부정하는 행위는 도덕적으로 금지된다. "
                "결론: 따라서 삶의 주체인 개체는 단순 수단이 아닌 목적 그 자체로 존중받아야 한다."
            ),
            "counterpoint": (
                "공리주의자는 어떤 경우에도 동물을 수단으로 사용해서는 안 된다는 절대적 금지가 "
                "현실적으로 인간 사회의 작동을 불가능하게 만들 수 있다고 지적한다. "
                "또한 의학 연구에서 동물 실험 전면 금지의 실천적 비용이 매우 크다는 비판."
            ),
            "context": (
                "2018-A Q11 ㉡ 답변 핵심 원리 · "
                "칸트 인간 목적 정식의 동물 확장 · 의무론적 동물권의 실천 원칙."
            ),
            "keywords": [
                "존중의 원리",
                "respect principle",
                "목적 그 자체",
                "단순 수단 금지",
                "칸트 목적 정식 확장",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-004: 해악의 원리 (CAR 8-9장)
        {
            "id": "regan-claim-004",
            "thinker_id": THINKER_ID,
            "work_id": "regan-car-1983",
            "source_detail": (
                "『동물권 옹호(The Case for Animal Rights, 1983)』 8-9장 · "
                "2018학년도 전공A Q11 ㉡ 답변 두 번째 원리"
            ),
            "claim": (
                "삶의 주체인 개체에게 해악(harm)을 끼쳐서는 안 된다(해악의 원리, harm principle). "
                "해악이란 개체의 복지를 저해하거나 삶의 기회를 박탈하는 행위이며, "
                "다른 개체의 더 큰 이익·유용성을 위해서라도 해악을 강요하는 것은 금지된다."
            ),
            # study-guide/2018-A.md L620 verbatim
            "original_text": (
                "삶의 주체인 개체에게 해악(harm)을 끼쳐서는 안 된다. "
                "해악이란 개체의 복지를 저해하거나 삶의 기회를 박탈하는 행위이다. "
                "다른 개체의 더 큰 이익·유용성을 위해서라도 한 개체에게 해악을 강요하는 것은 "
                "그 개체의 내재적 가치를 마치 존재하지 않는 것처럼 대우하는 행위로서 금지된다 "
                "— 2018학년도 전공A Q11 ㉡ 답변 (study-guide/2018-A.md L620). "
                "blocker-log.md L478 (BLK-175E-2018A-001 trademark ③) — "
                "리건 8-9장 harm principle."
            ),
            "explanation": (
                "리건 의무론적 동물권의 두 번째 적용 원리. "
                "해악의 원리는 존중의 원리의 부정적 표현으로, "
                "존중의 원리가 '목적으로 대하라'는 적극적 명령이라면 "
                "해악의 원리는 '해악을 끼치지 말라'는 소극적 금지이다. "
                "리건은 해악을 (a) 직접적 고통 부과, (b) 복지 박탈, "
                "(c) 삶의 기회 박탈(예: 사망)로 구분한다. "
                "공리주의가 '전체 이익 총합 극대화'를 위해 일부 개체에 대한 해악을 "
                "허용할 여지를 남기는 것과 달리, "
                "리건의 해악의 원리는 어떠한 총합 계산으로도 상쇄될 수 없는 절대적 금지이다."
            ),
            "argument": (
                "전제1: 내재적 가치를 지닌 존재의 복지·삶의 기회는 절대적으로 보호되어야 한다. "
                "전제2: 해악은 복지·삶의 기회를 침해하는 행위이다. "
                "전제3: 타인의 이익을 위해 한 개체의 절대적 가치를 침해하는 것은 정당화될 수 없다. "
                "결론: 따라서 삶의 주체인 개체에게 해악을 끼쳐서는 안 된다."
            ),
            "counterpoint": (
                "공리주의자는 해악의 원리의 절대적 적용이 자기방어·"
                "정당한 의학 연구 등의 합리적 예외를 배제한다고 비판한다. "
                "리건은 이에 대해 무고한 자에 대한 해악만이 절대적으로 금지되며 "
                "예외적 조정 원리(미니맥스 원칙·악화 원리 등)를 통해 응답한다."
            ),
            "context": (
                "2018-A Q11 ㉡ 답변의 두 번째 핵심 원리 · "
                "공리주의 총합 계산에 대한 의무론적 제약."
            ),
            "keywords": [
                "해악의 원리",
                "harm principle",
                "복지 박탈 금지",
                "삶의 기회 박탈 금지",
                "절대적 금지",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-005: 의무론적 동물권 — 싱어 공리주의 비판
        {
            "id": "regan-claim-005",
            "thinker_id": THINKER_ID,
            "work_id": "regan-car-1983",
            "source_detail": (
                "『동물권 옹호(The Case for Animal Rights, 1983)』 전체 · "
                "2024학년도 전공B Q8 을의 갑(싱어) 비판 핵심"
            ),
            "claim": (
                "의무론적 동물권은 공리주의적 총합 계산으로 상쇄될 수 없는 절대적 권리이다. "
                "싱어의 이익 평등 고려 공리주의는 전체 이익 총합 극대화를 추구하므로 "
                "개별 동물의 도덕적 지위가 다른 존재들의 유용성 계산에 좌우될 수 있고, "
                "동물을 수단으로 도구화할 가능성을 원리적으로 배제하지 못한다."
            ),
            # coverage/2024-B.md L371-L372 verbatim
            "original_text": (
                "공리주의는 전체 이익의 총합 극대화를 추구하므로, "
                "결국 개별 동물의 도덕적 지위가 다른 존재들의 이익·유용성 계산에 좌우될 수 있다 "
                "— 2024학년도 전공B Q8 을의 갑 비판 (coverage/2024-B.md L371-L372). "
                "리건에게 내재적 가치를 가진 삶의 주체는 "
                "유용성과 무관하게 동등한 존중의 권리를 가지는 존재이며, "
                "어떤 존재도 타인의 이익을 위한 단순 수단으로 이용될 수 없다 "
                "— coverage/2024-B.md L372 + blocker-log.md L950 "
                "(BLK-175E-2024B-006 trademark ②: independence of utility)."
            ),
            "explanation": (
                "리건 동물 윤리의 공리주의 비판 핵심. "
                "싱어의 공리주의 틀에서는 어떤 동물에게 고통을 가하는 것이 "
                "전체 이익의 합을 증대시킨다면(예: 동물실험이 인간 복지에 기여하면) "
                "원칙적으로 허용될 여지가 남는다. "
                "동물이 다른 존재에게 가지는 유용성이 도덕 판단의 일부가 되기 때문이다. "
                "이는 싱어의 이익 평등 고려 원칙이 동물의 이익을 인간 이익과 동등한 무게로 "
                "고려하더라도, 결국 총합의 도구화를 막지 못한다는 한계를 드러낸다. "
                "리건은 이에 대해 의무론적·권리 기반 접근만이 동물을 그 자체로서 "
                "존중할 수 있다고 본다 — 권리는 총합 계산의 대상이 아니라 "
                "어떠한 이익 계산도 침해할 수 없는 절대적 보호 영역이기 때문이다. "
                "이는 동물 윤리 양대 입장(공리주의 vs 의무론)의 정전 대립 구도를 형성한다."
            ),
            "argument": (
                "전제1: 공리주의는 전체 이익 총합 극대화를 추구한다. "
                "전제2: 총합 극대화 원리는 일부 개체의 이익이 더 큰 총합 이익을 위해 희생되는 것을 허용한다. "
                "전제3: 따라서 공리주의는 개별 동물을 수단으로 도구화할 여지를 원리적으로 배제하지 못한다. "
                "결론: 의무론적·권리 기반 접근만이 동물을 그 자체로 존중할 수 있다."
            ),
            "counterpoint": (
                "싱어는 자신의 이익 평등 고려 원칙이 단순 총합 극대화가 아니라 "
                "각 개체의 이익에 동등한 비중을 부여하는 평등 원칙임을 강조하며 "
                "리건의 비판이 공리주의를 단순화한다고 응답한다. "
                "또한 리건의 절대적 권리 입장이 권리 충돌 시 해결 원리를 갖지 못한다는 비판."
            ),
            "context": (
                "2024-B Q8 을 ㉢ 유용성 사용 비판 서술의 직접 근거 · "
                "동물 윤리 양대 입장 정전 대립."
            ),
            "keywords": [
                "의무론적 동물권",
                "deontological animal rights",
                "공리주의 비판",
                "싱어 비판",
                "유용성 독립성",
                "총합 계산 거부",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-006: 권리 행사자 vs 권리 보유자 구분
        {
            "id": "regan-claim-006",
            "thinker_id": THINKER_ID,
            "work_id": "regan-car-1983",
            "source_detail": (
                "『동물권 옹호(The Case for Animal Rights, 1983)』 5-6장 · "
                "blocker-log.md L479 (BLK-175E-2018A-001 후속 조치 trademark)"
            ),
            "claim": (
                "권리 행사자(moral agents)와 권리 보유자(moral patients)는 구분되며, "
                "도덕 능력이 없는 권리 보유자도 삶의 주체이면 권리 행사자와 "
                "동등한 권리를 보유한다. 이는 도덕 주체와 도덕 환자의 권리 평등 원칙이다."
            ),
            # blocker-log.md L479 verbatim
            "original_text": (
                "권리 행사자(moral agents)/권리 보유자(moral patients) 구분 "
                "— blocker-log.md L479 (BLK-175E-2018A-001 후속 조치 trademark)"
            ),
            "explanation": (
                "리건 동물권 이론의 도덕적 주체·환자 구분론. "
                "도덕 행위자(moral agent)는 도덕적 의무를 인식하고 행위에 책임을 지는 존재로 "
                "정상적 성인이 이에 해당한다. "
                "도덕 환자(moral patient)는 도덕적 의무를 행할 수 없으나 "
                "타인의 도덕적 행위 대상이 될 수 있는 존재이며, "
                "유아·중증 인지 장애인·삶의 주체인 동물 등이 이에 해당한다. "
                "리건의 핵심 주장은 도덕 능력의 차이에도 불구하고 "
                "두 범주 모두가 삶의 주체이면 동등한 내재적 가치와 권리를 보유한다는 것이다. "
                "이는 도덕 능력만을 권리의 근거로 삼는 칸트적 전통(도덕 능력 없는 동물에 대한 "
                "직접 의무 부정)을 비판하는 핵심 논거이다 — "
                "유아도 도덕 능력은 없으나 인간으로서 권리를 인정하면서, "
                "동일하게 도덕 능력 없는 동물에게 권리를 거부하는 것은 "
                "일관성 없는 종차별주의(singer 용어)·자의적 차별이다."
            ),
            "argument": (
                "전제1: 권리는 삶의 주체임에 근거하며 도덕 행위 능력에 근거하지 않는다. "
                "전제2: 유아·중증 인지 장애인은 도덕 행위 능력이 없으나 권리를 보유한다. "
                "전제3: 동물도 동일하게 도덕 행위 능력이 없으나 삶의 주체이다. "
                "결론: 따라서 동물도 권리 보유자로서 권리 행사자와 동등한 권리를 가진다."
            ),
            "counterpoint": (
                "칸트주의자는 도덕 능력이 권리의 본질적 근거라고 주장하며, "
                "유아·인지 장애인의 권리는 잠재적 도덕 능력 또는 인간 종 소속에 근거한다고 본다. "
                "리건은 이에 대해 인간 종 소속을 권리 근거로 삼는 것이야말로 종차별주의라고 응답한다."
            ),
            "context": (
                "리건 동물권 이론의 칸트 비판 핵심 논거 · "
                "도덕 능력 없는 권리 보유자에 대한 의무 정초."
            ),
            "keywords": [
                "권리 행사자",
                "moral agents",
                "권리 보유자",
                "moral patients",
                "도덕 주체",
                "도덕 환자",
                "권리 평등성",
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
    """리건 핵심 키워드 데이터 입력. 중복 체크 후 insert."""
    keywords = [
        {
            "id": "kw-regan-inherent-value",
            "term": "내재적 가치",
            "term_en": "inherent value",
            "definition": (
                "리건 『동물권 옹호(The Case for Animal Rights, 1983)』 7장 §7.5 trademark. "
                "타인의 평가·계약·합의에 의해 생기는 것이 아니라 "
                "자신이 삶의 주체임을 경험할 수 있는 존재들이 가지는 특별한 가치. "
                "원문: \"inherent value is not earned or assigned\". "
                "획득되지도 부여되지도 않으며, 삶의 주체인 모든 개체가 동등하게 소유하는 "
                "범주적·이분법적 가치. 도구적 가치·쾌락적 가치와 구별되는 개체 고유의 평등한 존엄. "
                "2018-A Q11 ㉠ 정답 + 2024-B Q8 을 trademark."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "regan-car-1983",
            "related_terms": [
                "삶의 주체",
                "존중의 원리",
                "해악의 원리",
                "의무론적 동물권",
                "목적 그 자체",
            ],
        },
        {
            "id": "kw-regan-subject-of-a-life",
            "term": "삶의 주체",
            "term_en": "subject-of-a-life",
            "definition": (
                "리건 『The Case for Animal Rights(1983)』 7장 §7.1-7.5 trademark. "
                "도덕적 지위의 기준으로서 7가지 조건을 충족하는 존재. "
                "① 믿음·욕망, ② 지각·기억·미래의식, ③ 쾌락·고통 감정적 삶, "
                "④ 선호·복지 이익, ⑤ 욕구·목적 달성 행동능력, "
                "⑥ 심리적 동일성, ⑦ 개별적 복지. "
                "통합된 심리적 삶을 영위하는 존재만이 도덕적 지위를 갖는다는 기준이며, "
                "일반적으로 1세 이상의 정상적 포유류 동물이 이 조건을 충족한다."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "regan-car-1983",
            "related_terms": [
                "내재적 가치",
                "7가지 기준",
                "심리적 동일성",
                "개별적 복지",
                "쾌고 감수 능력",
            ],
        },
        {
            "id": "kw-regan-respect-principle",
            "term": "존중의 원리",
            "term_en": "respect principle",
            "definition": (
                "리건 『CAR』 8-9장 trademark. "
                "삶의 주체인 개체는 단순한 수단(그릇·자원·도구)으로 대우해서는 안 되며, "
                "목적 그 자체로서 존중받아야 한다는 원리. "
                "그들의 내재적 가치가 마치 존재하지 않는 것처럼 대우하는 행위를 금지한다. "
                "칸트의 인간 목적 정식(Formula of Humanity)을 동물에게로 확장한 것으로, "
                "오락·의복·식용을 위한 사육·사냥·실험 등 동물을 단순 수단으로 삼는 "
                "제도적 관행을 도덕적으로 금지한다."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "regan-car-1983",
            "related_terms": [
                "내재적 가치",
                "단순 수단 금지",
                "목적 그 자체",
                "칸트 목적 정식 확장",
                "해악의 원리",
            ],
        },
        {
            "id": "kw-regan-harm-principle",
            "term": "해악의 원리",
            "term_en": "harm principle",
            "definition": (
                "리건 『CAR』 8-9장 trademark. "
                "삶의 주체인 개체에게 해악(harm)을 끼쳐서는 안 된다는 원리. "
                "해악이란 개체의 복지를 저해하거나 삶의 기회를 박탈하는 행위이다. "
                "다른 개체의 더 큰 이익·유용성을 위해서라도 한 개체에게 해악을 강요하는 것은 "
                "그 개체의 내재적 가치를 마치 존재하지 않는 것처럼 대우하는 행위로서 금지된다. "
                "공리주의가 전체 이익 총합 극대화를 위해 일부 개체에 대한 해악을 "
                "허용할 여지를 남기는 것과 달리, 어떠한 총합 계산으로도 상쇄될 수 없는 절대적 금지이다."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "regan-car-1983",
            "related_terms": [
                "존중의 원리",
                "복지 박탈 금지",
                "삶의 기회 박탈 금지",
                "공리주의 비판",
                "절대적 금지",
            ],
        },
        {
            "id": "kw-regan-deontological-animal-rights",
            "term": "의무론적 동물권",
            "term_en": "deontological animal rights",
            "definition": (
                "리건 『CAR』 trademark. "
                "공리주의적 총합 계산으로 상쇄될 수 없는 절대적 권리로서의 동물권. "
                "싱어의 이익 평등 고려 공리주의가 전체 이익 총합 극대화를 추구하므로 "
                "개별 동물의 도덕적 지위가 다른 존재들의 유용성 계산에 좌우될 수 있는 것과 달리, "
                "리건의 의무론적 권리는 어떠한 외적 이익 계산도 침해할 수 없는 절대적 보호 영역. "
                "동물 윤리 양대 입장(공리주의 vs 의무론)의 정전 대립 형성. "
                "2024-B Q8 을의 갑(싱어) 비판 핵심 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "regan-car-1983",
            "related_terms": [
                "공리주의 비판",
                "싱어 비판",
                "유용성 독립성",
                "총합 계산 거부",
                "절대적 권리",
            ],
        },
        {
            "id": "kw-regan-moral-agents-patients",
            "term": "권리 행사자 / 권리 보유자",
            "term_en": "moral agents / moral patients",
            "definition": (
                "리건 『CAR』 5-6장 trademark. "
                "도덕 행위자(moral agent)는 도덕적 의무를 인식하고 행위에 책임을 지는 존재(정상적 성인). "
                "도덕 환자(moral patient)는 도덕적 의무를 행할 수 없으나 "
                "타인의 도덕적 행위 대상이 될 수 있는 존재(유아·중증 인지 장애인·삶의 주체인 동물). "
                "리건의 핵심 주장은 도덕 능력의 차이에도 불구하고 두 범주 모두가 삶의 주체이면 "
                "동등한 내재적 가치와 권리를 보유한다는 것 — 이는 도덕 능력만을 권리 근거로 삼는 "
                "칸트적 전통을 비판하는 논거. "
                "단일 출처: blocker-log.md L479 (BLK-175E-2018A-001 후속 조치 trademark)."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "regan-car-1983",
            "related_terms": [
                "도덕 주체",
                "도덕 환자",
                "권리 평등성",
                "칸트 비판",
                "삶의 주체",
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
    """리건 영향·비교 관계 데이터 입력.

    ES 등록 확인된 thinker_id 만 링크 (2026-04-28 curl 확인):
    - singer  : 등록 (era=현대, 1946-) — 동물 윤리 양대 입장 정전 대립
                (공리주의 vs 의무론 — 2024-B Q8 갑·을 직접 출제)
    - kant    : 등록 — 인간 목적 정식의 동물 확장 (존중의 원리)
    """
    relations = [
        {
            "from_thinker": THINKER_ID,
            "to_thinker": "singer",
            "type": "criticized",
            "description": (
                "리건(1938-2017)과 싱어(1946~)의 동물 윤리관 대립은 "
                "현대 동물 윤리 양대 입장의 정전 구도이다. "
                "싱어의 공리주의적 동물 해방론은 이익 평등 고려의 원칙에 기반하여 "
                "쾌고 감수 능력(sentience)을 가진 모든 존재의 이익을 동등하게 고려해야 한다고 본다. "
                "리건은 이를 비판하며 의무론적 동물권을 제시한다 — "
                "공리주의는 전체 이익 총합 극대화를 추구하므로 개별 동물의 도덕적 지위가 "
                "다른 존재들의 유용성 계산에 좌우될 수 있고, "
                "동물을 수단으로 도구화할 가능성을 원리적으로 배제하지 못한다는 것. "
                "리건에게 내재적 가치를 가진 삶의 주체는 유용성과 무관하게 "
                "동등한 존중의 권리를 가지는 존재이며, "
                "어떤 존재도 타인의 이익을 위한 단순 수단으로 이용될 수 없다. "
                "2024-B Q8 (갑 싱어 vs 을 리건)은 이 정전 대립의 직접 출제."
            ),
            "evidence": (
                "coverage/2024-B.md L354 — "
                "'갑 = 피터 싱어(Peter Singer, 1946~) — 이익 평등 고려의 원칙 + 종차별주의 비판; "
                "을 = 톰 리건(Tom Regan, 1938-2017) — 내재적 가치 + 삶의 주체 + 의무론적 동물권'; "
                "coverage/2024-B.md L371-L372 — "
                "'을(리건) 입장에서 갑(싱어) 한계 — 공리주의는 전체 이익 총합 극대화를 추구하므로 "
                "개별 동물의 도덕적 지위가 다른 존재들의 이익·유용성 계산에 좌우될 수 있다'; "
                "blocker-log.md L950 (BLK-175E-2024B-006 trademark ②) — "
                "'리건 유용성 독립성: 내재적 가치는 타인에 대한 도구적 가치·유용성과 논리적으로 독립적'"
            ),
        },
        {
            "from_thinker": THINKER_ID,
            "to_thinker": "kant",
            "type": "extended",
            "description": (
                "리건(1938-2017)의 존중의 원리는 칸트(1724-1804)의 인간 목적 정식 "
                "(Formula of Humanity — '인간을 결코 단순한 수단으로 대하지 말고 "
                "항상 동시에 목적으로 대하라')을 동물에게로 확장한 것이다. "
                "칸트는 도덕 능력(이성·자율성)을 가진 인격(person)에게만 "
                "직접적 의무를 부여하고, 동물에 대해서는 간접적 의무 "
                "(동물 학대는 인간의 도덕적 감수성을 훼손하므로 금지)만을 인정하였다. "
                "리건은 이러한 간접 의무 이론을 비판하며, "
                "도덕 능력이 없는 권리 보유자(moral patients — 유아·동물)도 "
                "삶의 주체이면 도덕 행위자(moral agents)와 동등한 권리를 가진다고 주장한다. "
                "리건의 의무론적 동물권 이론은 칸트 의무론의 형식("
                "단순 수단 대우 금지·목적 그 자체 존중)을 보존하면서 "
                "그 적용 범위를 인격에서 삶의 주체로 확장한 것이다."
            ),
            "evidence": (
                "study-guide/2018-A.md L617 — "
                "'존중의 원리(respect principle): 삶의 주체인 개체는 단순한 수단으로 대우해서는 안 되며, "
                "목적 그 자체로서 존중받아야 한다. 이는 칸트의 인간 목적 정식을 동물로 확장한 것이다'; "
                "blocker-log.md L951 — "
                "'리건 칸트 목적 자체 원칙의 동물 확장: 동물을 단순 수단으로 사용하는 것 자체가 금지됨'; "
                "blocker-log.md L951 — "
                "'간접 의무 이론(indirect duty theories, 칸트·데카르트) 비판 — 동물에 대한 의무는 직접적'"
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
    print("=== 톰 리건(Tom Regan) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (regan)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n[OK] 톰 리건 데이터 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}", file=sys.stderr)
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
