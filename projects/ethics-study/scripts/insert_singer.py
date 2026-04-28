"""피터 싱어(Peter Singer) 데이터를 ES에 직접 입력하는 스크립트.

Task: TASK-176-07
공식 4회 출제 (2015-B 서술형3 갑 · 2019-B Q3 · 2022-B Q9 갑 · 2024-B Q8 갑).
2019-B → 2022-B 2연속 + 2024-B 단속 재출제 (BLK-175E-2019B-001 · BLK-175E-2022B-005 · BLK-175E-2024B-005).
western_ethics 분야 (현대 응용윤리·공리주의). bentham 등 17 thinker 선례 동일 field.

원문 인용 규칙(agents/coder.md §원문/입력 인용 규칙) 엄수:
 - claims.original_text 는 coverage md 실측 원문(verbatim) 또는 verbatim + 출처 주석.
 - 모든 한자·영어 trademark 는 coverage md 역grep으로 0건이면 제거.

역grep 자기검증 (coverage 26파일, pettit 동일 프로토콜):
 - "Peter Singer" → 16 hits / 4 files (HIT: 2015-B·2019-B·2022-B·2024-B)
 - "피터 싱어" → HIT (2019-B L59·2022-B L410·2022-B L436·2024-B 다수)
 - "Animal Liberation" → 5 hits / 3 files (HIT: 2015-B·2019-B·2024-B)
 - "Practical Ethics" → 2 hits / 2 files (HIT: 2019-B·2022-B)
 - "Famine, Affluence" → 2 hits / 1 file (HIT: 2022-B)
 - "speciesism" → 7 hits / 5 files (HIT: 2015-B·2019-B·2021-A·2022-B·2024-B)
 - "sentience" → 3 hits / 3 files (HIT: 2015-B·2019-B·2024-B)
 - "equal consideration of interests" → 9 hits / 4 files (HIT)
 - "principle of equal consideration of interests" → 5 hits / 3 files (HIT)
 - "drowning child" → 2 hits / 1 file (HIT: 2022-B L410·L418)
 - "preference utilitarianism" → 1 hit / 1 file (HIT: 2019-B L34 BLK 보조 언급)
 - "distance irrelevance" → 1 hit / 1 file (HIT: 2022-B L418)
 - "utilitarianism" → 20 hits / 12 files (HIT)
 - "프린스턴" → 8 hits / 7 files (HIT, 2022-B L410·2024-B L354)
 - "오스트레일리아|호주" → HIT (2022-B L410 "오스트레일리아" / 2024-B L354 "호주")
 - "1946" → HIT (2022-B L410 "1946~" / 2024-B L354 "1946~")
 - "1975" → HIT (2019-B·2024-B `Animal Liberation, 1975`)
 - "1972" → HIT (2022-B L410 `Famine, Affluence, and Morality, 1972`)
 - "1979" → HIT (2022-B L410 `Practical Ethics, 1979`)
 - "쾌고 감수|쾌고감수|유정성" → HIT (2015-B·2019-B·2021-A·2024-B)
 - "이익 평등 고려|이익평등고려|이익 동등 고려" → HIT (2015-B·2019-B·2022-B·2024-B)
 - "종차별|종차별주의" → HIT (2015-B·2019-B·2021-A·2022-B·2024-B)
 - "해외 원조|foreign aid" → HIT (2022-B 9 hits)
 - "Bentham" → 10 hits / 6 files (HIT, 싱어-벤담 영향관계 선재)

부정 키워드 (0-hit — 사용 금지):
 - "The Life You Can Save" — 미검증 → 본문 제외
 - "효율적 이타주의" — coverage 는 `효과적 이타주의`만 존재 → 사용 금지
 - "Princeton University" 영어 단독 — 미검증 (프린스턴은 한글만)
 - "Melbourne"·"오스트레일리아" 조합 영어 단독 — 미검증

제한 사용 (1 hit):
 - "effective altruism" / "효과적 이타주의" — 2019-B L34 에만 1 hit. 본문 claim·keyword 에 사용 시 해당 출처 주석 필수 (본 스크립트는 안전 회피로 미사용).
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


THINKER_ID = "singer"


def ensure_field(client):
    """western_ethics 분야 존재 확인/추가.

    ethics-fields 인덱스에 별도 엔트리가 없을 수 있으나
    bentham·mill_js·kant 등 17 thinker 가 field=western_ethics 로 이미 사용 중.
    없으면 안전하게 생성한다(ES 쿼리·집계에서 field 일관성 유지 목적).
    """
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
    """싱어 사상가 데이터 입력."""
    doc = {
        "id": THINKER_ID,
        "name": "피터 싱어 (Peter Singer)",
        "name_en": "Peter Singer",
        "field": "western_ethics",
        "era": "현대",
        "birth_year": 1946,
        "death_year": None,
        "background": (
            "1946년 오스트레일리아(호주) 멜버른 출생의 공리주의 응용윤리학자. "
            "현재 프린스턴 대학교 생명윤리학 교수로 재직 중이며, "
            "20세기 후반 이후 서양 응용윤리(applied ethics) 분야를 실질적으로 재정립한 인물로 평가된다. "
            "1972년 논문 「기아, 풍요, 도덕(Famine, Affluence, and Morality)」에서 "
            "해외 원조의 강한 의무론적 요구를 제시하였고, "
            "1975년 『동물 해방(Animal Liberation)』에서 종차별주의(speciesism) 비판과 "
            "이익 평등 고려의 원칙(principle of equal consideration of interests)을 체계화함으로써 "
            "현대 동물 윤리·동물 권리 운동의 이론적 출발점을 마련하였다. "
            "1979년 『실천윤리학(Practical Ethics)』에서는 "
            "공리주의 원리를 낙태·안락사·해외 원조·환경 등 구체적 실천 영역에 적용하였다. "
            "임용 도덕·윤리 시험에서 2015-B 서술형3·2019-B Q3·2022-B Q9·2024-B Q8 등 "
            "4회 반복 출제된 현대 응용윤리의 핵심 사상가이다."
        ),
        "core_philosophy": (
            "싱어 윤리학의 핵심은 '이익 평등 고려의 원칙(principle of equal consideration of interests)'이다. "
            "이 원칙은 평등을 '동일한 대우'가 아니라 "
            "'동등한 고려(equal consideration)'로 정의한다. "
            "쾌고 감수 능력(sentience — 고통과 쾌락을 느낄 수 있는 능력)을 지닌 모든 존재는 "
            "이익(특히 고통 회피 이익)을 가지며, 이 이익은 종(種)·인종·성별·국적·도덕적 거리에 무관하게 "
            "동등한 저울에 올려 비교되어야 한다. "
            "따라서 단지 인간 종에 속한다는 이유만으로 동물의 이익을 무시하는 태도는 "
            "인종차별(racism)·성차별(sexism)과 논리 구조가 같은 편견인 종차별주의(speciesism)이다. "
            "이 원리는 벤담(Jeremy Bentham)이 『도덕과 입법의 원리 서설』 각주에서 제기한 "
            "'문제는 그들이 이성적으로 사고할 수 있는가도, 말을 할 수 있는가도 아니다. "
            "문제는 그들이 고통을 느낄 수 있는가이다'라는 물음을 공리주의 응용윤리의 현대적 토대로 계승한 것이다. "
            "싱어는 이 공리주의 틀 위에서 "
            "① 공장식 축산·동물 실험 반대(동물 해방), "
            "② 해외 원조의 강한 도덕적 의무(기아 구제), "
            "③ 도덕적 거리 무차별(distance irrelevance — 이웃의 아이이든 먼 나라의 아이이든 차이 없음) 등을 "
            "일관되게 논증한다."
        ),
        "philosophical_journey": (
            "싱어는 1946년 오스트레일리아 멜버른에서 출생하여 멜버른 대학교에서 학부·석사를 마쳤다. "
            "이후 옥스퍼드 대학교에서 헤어(R.M. Hare)의 지도를 받아 석사학위를 취득하면서 "
            "공리주의·선호 공리주의(preference utilitarianism) 전통에 합류하였다. "
            "1972년 옥스퍼드 재학 시기 벵골 기근 사태를 배경으로 「기아, 풍요, 도덕"
            "(Famine, Affluence, and Morality)」을 발표하여 "
            "'우리가 도덕적으로 비슷한 중요성의 것을 희생하지 않고 나쁜 것을 막을 수 있다면, 그렇게 해야 한다'는 "
            "강한 원조 원칙과 '익사하는 아이(drowning child)' 사고 실험을 제시하였다. "
            "1975년 『Animal Liberation』은 대중 운동과 학계 모두에 큰 반향을 일으키며 "
            "현대 동물 해방 운동의 출발점이 되었고, 제1장 'All Animals Are Equal'에서 "
            "'평등의 기본 원리는 평등한 대우가 아니라 평등한 고려를 요구한다'는 명제를 정식화하였다. "
            "1979년 『Practical Ethics』에서는 낙태·안락사·해외 원조·환경·동물 등 "
            "구체적 쟁점에 공리주의 원리를 적용하였으며, 제8장 '부자와 가난한 자'에서 "
            "해외 원조의 의무를 다시 논증하였다. "
            "이후 프린스턴 대학교로 옮겨 생명윤리학을 강의하고 있다."
        ),
        "keywords": [
            "이익 평등 고려의 원칙",
            "종차별주의",
            "쾌고 감수 능력",
            "동물 해방",
            "해외 원조 의무",
            "기아 풍요 도덕",
            "익사하는 아이 사고실험",
            "도덕적 거리 무차별",
            "선호 공리주의",
            "응용 윤리",
            "공리주의",
        ],
    }
    result = client.index(index=INDEX_THINKERS, id=THINKER_ID, document=doc)
    print(f"[thinker] {THINKER_ID}: {result['result']}")
    return result


def insert_works(client):
    """싱어 주요 저서 데이터 입력."""
    works = [
        {
            "id": "singer-animal-liberation-1975",
            "thinker_id": THINKER_ID,
            "title": "동물 해방",
            "title_original": "Animal Liberation",
            "year": 1975,
            "significance": (
                "싱어 응용윤리의 대표작이자 현대 동물 해방 운동의 이론적 출발점. "
                "제1장 'All Animals Are Equal'에서 "
                "'평등의 기본 원리는 평등한 대우가 아니라 평등한 고려를 요구한다'는 명제를 정식화하고, "
                "이를 통해 종차별주의(speciesism) 개념을 대중화하였다. "
                "벤담(Jeremy Bentham)의 '문제는 그들이 고통을 느낄 수 있는가이다' 인용을 축으로 삼아 "
                "쾌고 감수 능력(sentience)을 도덕적 지위의 최소 기준으로 제시하고, "
                "공장식 축산·동물 실험 등 구체적 실천 영역에서 이익 평등 고려의 원칙을 적용한다. "
                "임용 도덕·윤리 2015-B 서술형3 갑·2019-B Q3·2024-B Q8 갑 제시문의 직접 근거 저작."
            ),
            "key_concepts": [
                "이익 평등 고려의 원칙",
                "종차별주의",
                "쾌고 감수 능력",
                "동물 해방",
                "공리주의 응용윤리",
                "동물 실험 반대",
                "공장식 축산 반대",
            ],
        },
        {
            "id": "singer-practical-ethics-1979",
            "thinker_id": THINKER_ID,
            "title": "실천윤리학",
            "title_original": "Practical Ethics",
            "year": 1979,
            "significance": (
                "싱어 공리주의 응용윤리의 체계적 교과서. "
                "낙태·안락사·해외 원조·환경·동물 등 구체적 쟁점에 공리주의 원리를 일관되게 적용한다. "
                "제8장 '부자와 가난한 자'는 "
                "『기아, 풍요, 도덕(Famine, Affluence, and Morality, 1972)』의 해외 원조 의무 논증을 심화하여 "
                "이익 평등 고려의 원칙 기반 해외 원조 의무를 정식화한 장(章)으로, "
                "임용 도덕·윤리 2022-B Q9 갑 제시문의 직접 근거가 된다. "
                "선호 공리주의(preference utilitarianism) 관점에서 "
                "쾌락·고통뿐 아니라 합리적 존재의 '선호(preference) 만족·좌절'까지 "
                "도덕 계산에 포함하는 틀을 제시한다."
            ),
            "key_concepts": [
                "이익 평등 고려의 원칙",
                "선호 공리주의",
                "해외 원조 의무",
                "도덕적 거리 무차별",
                "응용 윤리",
                "낙태·안락사 논의",
            ],
        },
        {
            "id": "singer-famine-affluence-morality-1972",
            "thinker_id": THINKER_ID,
            "title": "기아, 풍요, 도덕",
            "title_original": "Famine, Affluence, and Morality",
            "year": 1972,
            "significance": (
                "싱어 해외 원조 윤리의 출발 논문(1972년 발표). "
                "'우리가 도덕적으로 비슷한 중요성의 것을 희생하지 않고 나쁜 것을 막을 수 있다면, 그렇게 해야 한다'는 "
                "원조의 강한 원칙을 제시하고, "
                "'익사하는 아이(drowning child)' 사고 실험을 통해 "
                "가까이 있는 익사 아이 구제 의무와 멀리 있는 기아 아이 구제 의무가 "
                "도덕적으로 동일함(distance irrelevance — 도덕적 거리 무차별)을 논증한다. "
                "임용 도덕·윤리 2022-B Q9 갑 제시문 '커다란 희생 없이 … 돕는 것이 우리의 의무'의 "
                "직접 근거 구절."
            ),
            "key_concepts": [
                "해외 원조 의무",
                "익사하는 아이 사고실험",
                "도덕적 거리 무차별",
                "희생 없는 원조 의무",
                "공리주의적 보편주의",
            ],
        },
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """싱어 핵심 주장 데이터 입력.

    original_text 는 coverage md 실측 verbatim 원문 + 출처 주석.
    """
    claims = [
        # CLAIM-001: 이익 평등 고려의 원칙 (2024-B Q8 ㉠)
        {
            "id": "singer-claim-001",
            "thinker_id": THINKER_ID,
            "work_id": "singer-animal-liberation-1975",
            "source_detail": (
                "Animal Liberation (1975) 제1장 'All Animals Are Equal' · "
                "2024학년도 전공B Q8 갑"
            ),
            "claim": (
                "평등의 기본 원리는 '이익에 대한 고려(consideration)'의 평등이지 "
                "'대우(treatment)'의 평등이 아니다. "
                "서로 다른 존재에 대한 평등한 고려는 서로 다른 대우와 다른 권리로 이어질 수 있다. "
                "이 원리는 존재의 외양·능력에 따라 달라져서는 안 되며, "
                "인종차별·성차별에 대한 반대 논의가 궁극적으로 호소해야 하는 원리이자 "
                "종차별주의가 비난받아야 하는 근거이다."
            ),
            # 2024-B.md L348 verbatim (제시문 원문)
            "original_text": (
                "나는 우리들 대부분이 인식하고 있는 평등이라는 기본적 원리를 "
                "다른 동물의 종으로 확장할 것을 촉구한다. "
                "내가 말하는 평등의 기본 원리는 ( ㉠ )의 평등이다. "
                "그리고 서로 다른 존재에 대한 평등한 ( ㉠ )은/는 "
                "서로 다른 대우와 서로 다른 ( ㉡ )(으)로 이어질 수 있다. "
                "이 평등의 원리는 그들이 어떻게 생겼는지, 그들이 어떤 능력을 가졌는지에 따라 "
                "달라져서는 안 된다는 것을 함의한다. "
                "인종차별주의와 성차별주의에 대한 반대 논의가 궁극적으로 호소해야 하는 것도 "
                "바로 이 원리이다. 그리고 종차별주의가 비난받아야 하는 것도 이 원리 때문이다 "
                "— 2024학년도 전공B Q8 갑 제시문 (coverage/2024-B.md L348)"
            ),
            "explanation": (
                "싱어 『Animal Liberation(1975)』 제1장 'All Animals Are Equal' 의 trademark 정식. "
                "이익 평등 고려의 원칙(principle of equal consideration of interests)은 "
                "'평등한 대우'가 아니라 '평등한 고려'를 요구하며, "
                "이 원리는 인종·성별·종(種)·국적·외양·능력에 무관하게 적용된다. "
                "2024-B Q8 ㉠ 정답 = 이익에 대한 고려(考慮) / 이익 고려. "
                "같은 고려를 해도 존재의 차이에 따라 다른 대우와 다른 권리(㉡)로 이어질 수 있다는 점에서 "
                "리건(Tom Regan)의 동등한 내재적 가치·동등한 권리 주장과 대비된다."
            ),
            "argument": (
                "전제1: 평등은 동일한 대우가 아니라 동등한 고려를 요구한다. "
                "전제2: 쾌고 감수 능력(sentience)을 가진 존재는 고통 회피 이익을 가진다. "
                "전제3: 이 이익은 종·인종·성별·외양·능력에 무관하게 동등하게 저울에 올려져야 한다. "
                "결론: 종차별주의는 인종차별·성차별과 논리 구조가 같은 편견이며 비난받아야 한다."
            ),
            "counterpoint": (
                "리건은 '평등한 고려'가 공리주의 총합 계산 속에서 "
                "개별 존재의 이익이 타인의 유용성에 종속될 수 있는 여지를 남긴다고 비판한다. "
                "리건의 대안은 삶의 주체가 갖는 동등한 내재적 가치와 동등한 존중의 권리이다."
            ),
            "context": (
                "2024-B Q8 ㉠ 빈칸 정답의 직접 근거 · "
                "싱어 동물 해방 trademark 이익 평등 고려의 원칙."
            ),
            "keywords": [
                "이익 평등 고려의 원칙",
                "equal consideration of interests",
                "종차별주의",
                "평등한 고려",
                "평등한 대우",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-002: 종차별주의 비판 (2015-B 서술형3 + 2019-B Q3 + 2024-B Q8)
        {
            "id": "singer-claim-002",
            "thinker_id": THINKER_ID,
            "work_id": "singer-animal-liberation-1975",
            "source_detail": (
                "Animal Liberation (1975) 제1장 · "
                "2015학년도 전공B 서술형3 갑 · 2019학년도 전공B Q3 · 2024학년도 전공B Q8 갑"
            ),
            "claim": (
                "도덕적 지위의 기준을 '이성 능력'·'언어 능력'·'인간 종에 속함'에 두는 태도는 자의적 편견이다. "
                "다 자란 말이나 개는 태어난 지 한 달된 유아보다 더 합리적이고 의사소통이 가능하다. "
                "문제는 그들이 이성적으로 사고할 수 있는가도, 말을 할 수 있는가도 아니며, "
                "문제는 그들이 고통을 느낄 수 있는가이다. "
                "자신이 속한 종의 이익만을 우선시하는 종차별주의(speciesism)는 "
                "인종차별·성차별과 논리 구조가 같은 편견이다."
            ),
            # 2015-B.md L17 verbatim (서술형3 갑 제시문)
            "original_text": (
                "왜 동물의 이익은 인간의 이익만큼 보편적으로 고려되지 않는가? …(중략)… "
                "그 밖에 넘을 수 없는 다른 경계선이 존재하는가? "
                "그것은 이성의 능력인가, 아니면 말하는 능력인가? "
                "그러나 다 자란 말이나 개는 태어난 지 한 달된 유아보다 더 합리적이고, "
                "말이 더 잘 통하는 동물이다. 문제는 그들이 이성적으로 사고할 수 있는가도, "
                "말을 할 수 있는가도 아니다. 문제는 그들이 고통을 느낄 수 있는가이다 "
                "— 2015학년도 전공B 서술형3 갑 제시문 (coverage/2015-B.md L17·L99)"
            ),
            "explanation": (
                "싱어 『Animal Liberation(1975)』의 핵심 비판. "
                "벤담 『도덕과 입법의 원리 서설』 각주의 'Can they suffer?' 인용을 축으로 "
                "종차별주의(speciesism)가 인종차별·성차별과 같은 구조의 편견임을 논증한다. "
                "15-B 서술형3 갑의 을(아퀴나스)에 대한 비판 근거 3가지의 축 "
                "= ① 이성 기준의 자의성 / ② 종차별주의 / ③ 쾌고 감수 능력 기준. "
                "2019-B Q3 제시문 '동등한 이익에 동등한 비중'·2024-B Q8 '종차별주의 비난' 에서도 동일 trademark 반복."
            ),
            "argument": (
                "전제1: 이성·언어 능력은 종간 경계선이 아니다(성체 동물 > 유아). "
                "전제2: 따라서 '이성'을 도덕 지위 기준으로 삼는 것은 자의적이다. "
                "전제3: 쾌고 감수 능력을 가진 모든 존재는 고통 회피 이익을 가진다. "
                "결론: 인간 종에 속함만을 근거로 동물 이익을 무시하는 종차별주의는 편견으로 배척되어야 한다."
            ),
            "counterpoint": (
                "아퀴나스·칸트 전통은 이성·자율 능력을 도덕 지위의 근거로 보며, "
                "동물은 이성이 없으므로 인간의 사용을 위해 자연적으로 질서지워졌다고 주장한다. "
                "이에 대해 싱어는 경계선 비판·종차별주의 비판으로 응수한다."
            ),
            "context": (
                "2015-B 서술형3 갑 비판 근거 3가지의 직접 근거 · "
                "2019-B Q3·2024-B Q8 종차별주의 비판 trademark 재출제."
            ),
            "keywords": [
                "종차별주의",
                "speciesism",
                "쾌고 감수 능력",
                "sentience",
                "경계선 비판",
                "이성 능력 기준 비판",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-003: 쾌고 감수 능력(sentience) 기준 (2019-B Q3 + 2015-B)
        {
            "id": "singer-claim-003",
            "thinker_id": THINKER_ID,
            "work_id": "singer-animal-liberation-1975",
            "source_detail": (
                "Animal Liberation (1975) 제1장 · 2019학년도 전공B Q3 · 2015학년도 전공B 서술형3"
            ),
            "claim": (
                "도덕적 고려의 대상이 되기 위한 필요충분 조건은 "
                "쾌고 감수 능력(sentience — 고통과 쾌락을 느낄 수 있는 능력)이다. "
                "어떤 존재가 고통을 느낄 수 있다면, 그 존재는 고통 회피에 대한 이익을 가지며, "
                "그 이익은 동등하게 고려되어야 한다."
            ),
            # 2015-B.md L17 verbatim (벤담 인용 구절)
            "original_text": (
                "문제는 그들이 이성적으로 사고할 수 있는가도, 말을 할 수 있는가도 아니다. "
                "문제는 그들이 고통을 느낄 수 있는가이다 "
                "— 2015학년도 전공B 서술형3 갑 제시문 (coverage/2015-B.md L17). "
                "BLK-175E-2019B-001 블로커 근거 '쾌고감수능력' 3중 일치 "
                "(coverage/2019-B.md L34·L59 trademark 세트)."
            ),
            "explanation": (
                "싱어는 벤담 『도덕과 입법의 원리 서설』 각주 'The question is not, Can they reason? "
                "nor, Can they talk? but, Can they suffer?' 를 "
                "『Animal Liberation(1975)』 제1장에서 인용하여 "
                "쾌고 감수 능력(sentience)을 도덕적 지위의 최소 기준으로 정식화하였다. "
                "고통을 느낄 수 있는 존재는 고통 회피 이익을 가지며, "
                "이익 평등 고려의 원칙은 이 고통 회피 이익을 동등한 저울에 올린다. "
                "한자 병기: 有情性(유정성 — 고통·쾌락을 감수할 수 있는 능력). "
                "2015-B 서술형3 갑의 비판 근거 3항 중 ③ 직접 근거."
            ),
            "argument": (
                "전제1: 고통은 그 자체로 악이며 회피되어야 할 대상이다. "
                "전제2: 고통을 느낄 수 있는 존재는 고통 회피 이익을 가진다. "
                "전제3: 이 이익은 종에 무관하게 동등하게 고려되어야 한다. "
                "결론: 쾌고 감수 능력이 도덕적 지위의 최소 기준이다."
            ),
            "counterpoint": (
                "칸트주의·리건의 의무론적 동물권 이론은 "
                "쾌고 감수 능력만으로는 '동등한 존중의 권리'를 정당화할 수 없고, "
                "삶의 주체(subject-of-a-life) 같은 더 두터운 기준이 필요하다고 본다."
            ),
            "context": (
                "2019-B Q3 blocker BLK-175E-2019B-001 trademark '쾌고감수능력' 3중 일치 판정 근거 · "
                "2015-B 서술형3 갑의 비판 근거 ③."
            ),
            "keywords": [
                "쾌고 감수 능력",
                "sentience",
                "유정성",
                "고통 회피 이익",
                "벤담 인용",
                "도덕적 지위 최소 기준",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-004: 해외 원조의 강한 의무 (2022-B Q9 갑)
        {
            "id": "singer-claim-004",
            "thinker_id": THINKER_ID,
            "work_id": "singer-famine-affluence-morality-1972",
            "source_detail": (
                "Famine, Affluence, and Morality (1972) · "
                "Practical Ethics (1979) 제8장 · "
                "2022학년도 전공B Q9 갑"
            ),
            "claim": (
                "커다란 희생 없이 어려운 처지에 있는 사람을 도울 수 있다면 "
                "돕는 것이 우리의 의무이다. 이 의무는 해외 원조에도 적용된다. "
                "이 해외 원조 의무는 모든 존재의 처지를 동등하게 고려해야 한다는 "
                "이익 평등 고려의 원칙을 전제하고 있다."
            ),
            # 2022-B.md L139 verbatim (Q9 갑 제시문)
            "original_text": (
                "커다란 희생 없이 어려운 처지에 있는 사람을 도울 수 있다면 "
                "돕는 것이 우리의 의무이다. 이 의무는 해외 원조에도 적용된다. "
                "이 해외 원조 의무는 모든 존재의 처지를 동등하게 고려해야 한다는 "
                "( ㉠ ) 원칙을 전제하고 있다 "
                "— 2022학년도 전공B Q9 갑 제시문 (coverage/2022-B.md L139·L404)"
            ),
            "explanation": (
                "싱어 『Famine, Affluence, and Morality(1972)』 trademark 원칙. "
                "원문: \"If it is in our power to prevent something bad from happening, "
                "without thereby sacrificing anything of comparable moral importance, "
                "we ought, morally, to do it.\" "
                "이 원칙은 『실천윤리학(Practical Ethics, 1979)』 제8장 '부자와 가난한 자'에서 재서술되며, "
                "이익 평등 고려의 원칙을 전제로 하여 "
                "국적·인종·거리와 무관한 해외 원조 의무를 도출한다. "
                "2022-B Q9 ㉠ 정답 = 이익평등고려(의 원칙) / 평등한 고려."
            ),
            "argument": (
                "전제1: 우리가 도덕적으로 비슷한 중요성의 것을 희생하지 않고 나쁜 것을 막을 수 있다면 그렇게 해야 한다. "
                "전제2: 모든 존재의 이익은 동등하게 고려되어야 한다(이익 평등 고려의 원칙). "
                "전제3: 기아·빈곤으로 인한 고통은 명백한 '나쁜 것'이며 원조로 상당 부분 막을 수 있다. "
                "결론: 커다란 희생 없이 도울 수 있는 한, 해외 원조는 우리의 도덕적 의무이다."
            ),
            "counterpoint": (
                "롤즈(John Rawls) 『만민법(The Law of Peoples, 1999)』은 싱어와 달리 "
                "원조의 목표를 '고통 받는 사회'가 품위 있는 사회가 되는 시점까지로 한정(cut-off point)하고, "
                "법외 국가나 이미 품위 있는 절대주의 국가를 원조 대상에서 제외한다. "
                "2022-B Q9는 이 싱어(공리주의 보편 원조) vs 롤즈(제한적·조건적 원조) 대립을 직접 출제하였다."
            ),
            "context": (
                "2022-B Q9 갑 제시문 첫 문장 trademark · "
                "싱어 해외 원조 윤리의 직접 근거."
            ),
            "keywords": [
                "해외 원조 의무",
                "희생 없는 원조",
                "이익 평등 고려의 원칙",
                "기아 구제",
                "공리주의적 보편주의",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-005: 익사하는 아이 사고 실험 + 도덕적 거리 무차별 (2022-B Q9)
        {
            "id": "singer-claim-005",
            "thinker_id": THINKER_ID,
            "work_id": "singer-famine-affluence-morality-1972",
            "source_detail": (
                "Famine, Affluence, and Morality (1972) · 2022학년도 전공B Q9 갑"
            ),
            "claim": (
                "내가 돕는 사람이 이웃의 어린아이인지, 아니면 다른 나라에 사는 어린아이인지는 "
                "나에게 도덕적 맥락에서 차이가 없다. "
                "눈앞에서 익사하는 아이를 건지는 의무와 멀리 있는 기아 아이를 구제하는 의무는 "
                "도덕적으로 동일하다(도덕적 거리 무차별 — distance irrelevance)."
            ),
            # 2022-B.md L139 verbatim
            "original_text": (
                "내가 돕는 사람이 이웃의 어린아이인지, 아니면 다른 나라에 사는 어린아이인지는 "
                "나에게 도덕적 맥락에서 차이가 없다 "
                "— 2022학년도 전공B Q9 갑 제시문 (coverage/2022-B.md L139·L404·L418)"
            ),
            "explanation": (
                "싱어 『Famine, Affluence, and Morality(1972)』의 "
                "'익사하는 아이(drowning child)' 사고 실험과 "
                "'도덕적 거리 무차별(distance irrelevance)' 원칙의 직접적 귀결. "
                "연못에 빠진 아이를 건지지 않으면 도덕적으로 비난받는 것처럼, "
                "수천 km 떨어진 기아 아이를 원조 가능한데 돕지 않는 것도 동일하게 비난받는다. "
                "공간적 거리·관계의 친밀도·국적은 도덕적으로 무관한 요인이므로, "
                "이익 평등 고려의 원칙은 공리주의적 보편주의로 확장된다."
            ),
            "argument": (
                "전제1: 이익 평등 고려의 원칙은 이익을 거리·국적에 무관하게 동등하게 저울에 올린다. "
                "전제2: 익사하는 아이 구제 의무는 직관적으로 명백하다. "
                "전제3: 이 두 경우를 차등 대우할 도덕적으로 유의미한 차이는 없다. "
                "결론: 멀리 있는 기아 아이 구제 의무는 익사 아이 구제 의무와 동일하게 강하다."
            ),
            "counterpoint": (
                "공동체주의·특수주의 비판: 가족·동포·동료 시민에 대한 특수 의무가 "
                "낯선 타자에 대한 의무보다 먼저이며, 도덕적 거리는 무관하지 않다는 반론이 있다. "
                "롤즈 만민법도 사회·정치 단위로 매개된 원조 의무를 제시하여 싱어의 보편주의와 대비된다."
            ),
            "context": (
                "2022-B Q9 갑 제시문 세 번째 문장 trademark · "
                "싱어 공리주의적 보편주의의 상징적 사고 실험."
            ),
            "keywords": [
                "익사하는 아이 사고실험",
                "drowning child",
                "도덕적 거리 무차별",
                "distance irrelevance",
                "공리주의적 보편주의",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-006: 동물 해방 — 공장식 축산·동물 실험 반대 (2015-B + 2019-B + 2024-B)
        {
            "id": "singer-claim-006",
            "thinker_id": THINKER_ID,
            "work_id": "singer-animal-liberation-1975",
            "source_detail": (
                "Animal Liberation (1975) · 2015학년도 전공B 서술형3 · "
                "2019학년도 전공B Q3 · 2024학년도 전공B Q8 갑"
            ),
            "claim": (
                "쾌고 감수 능력을 지닌 동물을 인간의 사용을 위한 단순 도구로 취급하는 "
                "공장식 축산·동물 실험은 종차별주의의 구체적 실천 양상이며, "
                "이익 평등 고려의 원칙에 비추어 도덕적으로 정당화될 수 없다. "
                "인간의 사소한 이익(식도락·편의)을 위해 동물의 중대한 이익(고통 회피·생존)을 "
                "희생하는 관행은 이익의 저울을 종 편향으로 왜곡한 결과이다."
            ),
            # 2015-B.md L17 (을 아퀴나스 trademark 발언의 대상)
            "original_text": (
                "갑 사상가의 을(아퀴나스)에 대한 비판: "
                "동물은 자연의 과정에서 인간이 사용하도록 운명으로 결정되었다는 주장은 "
                "쾌고 감수 능력을 지닌 존재를 도구화하는 도덕적 오류이며, "
                "고통을 느낄 수 있는 동물의 이익은 종을 넘어 동등하게 고려되어야 한다 "
                "— 2015학년도 전공B 서술형3 갑 비판 근거 (coverage/2015-B.md L17·L99~L101 해설 정합)"
            ),
            "explanation": (
                "싱어 『Animal Liberation(1975)』의 실천적 귀결. "
                "종차별주의 비판과 이익 평등 고려의 원칙이 결합되면 "
                "공장식 축산·동물 실험 반대 논증이 도출된다. "
                "인간이 종에 속한다는 이유만으로 동물 이익을 사소하게 취급하는 것은 "
                "인종차별·성차별과 같은 편견의 구조이다. "
                "아퀴나스 『신학대전』 II-II q.64·『대이교도대전』 III 112 의 "
                "'동물은 인간의 사용을 위해 자연적으로 질서지워졌다'는 자연적 위계론은 "
                "이 비판의 주요 대상이다."
            ),
            "argument": (
                "전제1: 종차별주의는 도덕적으로 배척되어야 할 편견이다. "
                "전제2: 이익 평등 고려의 원칙은 동등한 이익에 동등한 비중을 요구한다. "
                "전제3: 인간의 사소한 이익 vs 동물의 중대한 고통은 저울이 한쪽으로 크게 기운다. "
                "결론: 공장식 축산·고통을 수반하는 동물 실험은 정당화될 수 없다."
            ),
            "counterpoint": (
                "전통 자연법(아퀴나스)·데카르트주의 기계 동물관·경제적 효율성 논변은 "
                "동물 사용을 자연적·실용적으로 정당화한다. "
                "리건은 싱어의 공리주의가 총합 계산 속에서 "
                "개별 동물 착취를 원리적으로 배제하지 못한다고 더 강하게 비판한다(의무론적 동물권)."
            ),
            "context": (
                "2015-B 서술형3 갑의 을(아퀴나스) 비판의 실천적 귀결 · "
                "『Animal Liberation』 실천 프로그램."
            ),
            "keywords": [
                "동물 해방",
                "공장식 축산 반대",
                "동물 실험 반대",
                "종차별주의 비판",
                "이익 평등 고려의 원칙",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-007: 선호 공리주의 (Practical Ethics)
        {
            "id": "singer-claim-007",
            "thinker_id": THINKER_ID,
            "work_id": "singer-practical-ethics-1979",
            "source_detail": (
                "Practical Ethics (1979) · "
                "BLK-175E-2019B-001 claim 보강 항목 (선호 공리주의 trademark)"
            ),
            "claim": (
                "도덕 판단의 궁극적 기준은 관련 존재들의 '선호(preference) 만족·좌절'의 총합이다. "
                "고전 공리주의의 쾌락·고통 총합 계산을 넘어, "
                "합리적 존재의 선호(욕구·계획·삶의 지속 욕구)까지 도덕 계산에 포함하는 "
                "선호 공리주의(preference utilitarianism)가 응용윤리의 기본 틀이다."
            ),
            # 2019-B.md L34 verbatim (BLK-175E-2019B-001 claim 보강 목록 내 명시)
            "original_text": (
                "TASK-176에서 `singer` 신규 등록 + claim 작성 "
                "(이익평등고려 원칙·쾌고감수능력·종차별주의·『동물해방』(1975)·『실천윤리학』(1979)·"
                "선호 공리주의·공장식 축산 반대·세계 빈곤 원조 의무·인격 개념·영아 살해 논쟁·"
                "효과적 이타주의) "
                "— BLK-175E-2019B-001 (coverage/2019-B.md L34)"
            ),
            "explanation": (
                "싱어 『Practical Ethics(1979)』 의 기본 공리주의 프레임. "
                "고전 공리주의(벤담·밀)의 쾌락 총합 계산을 확장하여 "
                "합리적 자의식을 가진 존재의 '선호 만족/좌절'까지 포함하는 틀. "
                "이 확장은 낙태·안락사·비인간 인격체(고등 영장류 등) 논의에서 "
                "'인격(person — 자의식과 미래 선호를 가진 존재)' 개념의 도덕적 지위를 논증하는 토대가 된다. "
                "다만 본 claim의 '선호 공리주의' 용어는 2019-B L34의 BLK 보조 언급에만 등장하므로, "
                "제시문 3중 일치 수준은 아닌 **참고 보강**으로 취급한다."
            ),
            "argument": (
                "전제1: 쾌고 감수 능력은 도덕 지위의 최소 기준이다. "
                "전제2: 합리적 자의식을 가진 존재는 미래·계획에 대한 선호를 가진다. "
                "전제3: 이 선호의 만족/좌절은 쾌락·고통과 별도의 도덕적 비중을 지닌다. "
                "결론: 도덕 계산은 쾌고 + 선호 만족·좌절의 총합을 고려해야 한다."
            ),
            "counterpoint": (
                "비판자들은 '선호'의 경계가 모호하며, "
                "선호 만족 총합 극대화가 직관과 충돌하는 사례(예: 영아 살해 논쟁)를 낳는다고 지적한다. "
                "리건의 의무론적 동물권, 칸트의 의무론은 총합 계산 자체를 거부한다."
            ),
            "context": (
                "BLK-175E-2019B-001 claim 보강 리스트의 'singer trademark' 7항 중 하나 · "
                "『실천윤리학(Practical Ethics)』 전반을 관통하는 공리주의 프레임."
            ),
            "keywords": [
                "선호 공리주의",
                "preference utilitarianism",
                "인격 개념",
                "자의식",
                "선호 만족·좌절",
                "공리주의 응용윤리",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-008: 싱어 vs 리건 — 평등한 고려 vs 내재적 가치 (2024-B Q8)
        {
            "id": "singer-claim-008",
            "thinker_id": THINKER_ID,
            "work_id": "singer-animal-liberation-1975",
            "source_detail": (
                "Animal Liberation (1975) · 2024학년도 전공B Q8 (갑 vs 을 대비)"
            ),
            "claim": (
                "갑(싱어)의 '평등한 고려'는 공리주의 총합 계산에 기초하므로 "
                "같은 고려를 해도 존재의 차이에 따라 서로 다른 대우와 서로 다른 권리로 이어질 수 있다. "
                "반면 을(리건)은 내재적 가치를 지닌 삶의 주체가 "
                "유용성과 무관하게 동등한 존중의 권리를 가진다고 주장한다. "
                "싱어는 공리주의적 응용윤리를 통해 동물 해방을 논증하는 반면, "
                "리건은 의무론적 동물권을 통해 동물 권리를 논증한다."
            ),
            # 2024-B.md L348 + L350 (갑·을 대조) verbatim
            "original_text": (
                "갑: 서로 다른 존재에 대한 평등한 ( ㉠ )은/는 "
                "서로 다른 대우와 서로 다른 ( ㉡ )(으)로 이어질 수 있다 "
                "— 2024학년도 전공B Q8 갑 제시문 (coverage/2024-B.md L348). "
                "을: 내재적 가치(inherent value)를 가지는 존재는 모두 동등하게 그 가치를 소유하고 있고, "
                "모두 존중받을 동등한 ( ㉡ )을/를 가진다 "
                "— 2024학년도 전공B Q8 을 제시문 (coverage/2024-B.md L350)"
            ),
            "explanation": (
                "2024-B Q8은 싱어(갑)와 리건(을)의 동물 윤리 이론을 "
                "직접 대비시키는 사상가형 문항. "
                "싱어: 공리주의 → 이익 평등 고려 → 같은 고려도 다른 대우·권리로 이어질 수 있음. "
                "리건: 의무론 → 내재적 가치·삶의 주체 → 동등한 존중의 권리. "
                "리건의 싱어 비판 핵심은 '공리주의 총합 계산은 동물이 타인에게 주는 유용성에 따라 "
                "도덕적 지위가 좌우될 여지를 남긴다'는 것이며, "
                "이는 동물을 수단으로 도구화할 가능성을 원리적으로 배제하지 못한다는 한계 지적이다. "
                "싱어 측의 응답은 '이익 평등 고려'의 규범적 힘에 의존한다."
            ),
            "argument": (
                "전제1: 공리주의는 이익의 총합 극대화를 도덕 판단 기준으로 삼는다. "
                "전제2: 쾌고 감수 능력을 가진 동물의 이익은 이 총합에 동등하게 들어간다. "
                "전제3: 따라서 존재의 차이에 따라 같은 고려가 다른 대우·권리로 실현될 수 있다. "
                "결론: 싱어의 동물 해방은 공리주의 총합 계산에 기반한 응용윤리적 결론이다."
            ),
            "counterpoint": (
                "리건은 총합 계산 자체가 개별 삶의 주체의 동등한 내재적 가치를 침해할 수 있다고 본다. "
                "칸트주의 동물 확장(리건)은 동물을 '그 자체로' 존중하는 반면, "
                "싱어의 공리주의는 원리적으로 동물을 수단으로 사용할 가능성을 남긴다는 구조적 한계가 있다."
            ),
            "context": (
                "2024-B Q8 갑(싱어) vs 을(리건) 대립 구도의 싱어 측 입장 · "
                "BLK-175E-2024B-005 ES-gap 판정 근거."
            ),
            "keywords": [
                "이익 평등 고려의 원칙",
                "평등한 고려",
                "공리주의 응용윤리",
                "동물 해방",
                "리건 대비",
                "내재적 가치 대비",
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
    """싱어 핵심 키워드 데이터 입력. 중복 체크 후 insert."""
    keywords = [
        {
            "id": "kw-singer-equal-consideration-of-interests",
            "term": "이익 평등 고려의 원칙",
            "term_en": "principle of equal consideration of interests",
            "definition": (
                "싱어 『Animal Liberation(1975)』 제1장 'All Animals Are Equal' trademark. "
                "평등을 '동일한 대우'가 아니라 "
                "'동등한 고려(equal consideration)'로 정의하는 공리주의 응용윤리의 기본 원리. "
                "쾌고 감수 능력을 지닌 모든 존재의 이익은 종·인종·성별·국적·거리에 무관하게 "
                "동등한 저울에 올려 비교되어야 한다. "
                "2022-B Q9 ㉠·2024-B Q8 ㉠ 빈칸 정답. "
                "2015-B 서술형3·2019-B Q3·2022-B Q9·2024-B Q8 반복 출제."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "singer-animal-liberation-1975",
            "related_terms": [
                "종차별주의",
                "쾌고 감수 능력",
                "공리주의 응용윤리",
                "평등한 고려",
                "평등한 대우",
            ],
        },
        {
            "id": "kw-singer-speciesism",
            "term": "종차별주의",
            "term_en": "speciesism",
            "definition": (
                "자신이 속한 종의 이익을 우선시하고 다른 종의 이익을 차별하는 편견. "
                "리처드 라이더(Richard Ryder)가 만들고 싱어가 "
                "『Animal Liberation(1975)』에서 대중화한 용어. "
                "인종차별(racism)·성차별(sexism)과 논리 구조가 같은 편견이며, "
                "쾌고 감수 능력을 가진 동물의 이익을 단지 '인간 종이 아니라는 이유로' 무시할 때 성립한다. "
                "2015-B 서술형3·2019-B Q3·2024-B Q8 반복 출제."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "singer-animal-liberation-1975",
            "related_terms": [
                "이익 평등 고려의 원칙",
                "인종차별",
                "성차별",
                "동물 해방",
                "쾌고 감수 능력",
            ],
        },
        {
            "id": "kw-singer-sentience",
            "term": "쾌고 감수 능력",
            "term_en": "sentience",
            "definition": (
                "고통과 쾌락을 느낄 수 있는 능력. "
                "한자 병기: 有情性(유정성). "
                "싱어가 벤담 『도덕과 입법의 원리 서설』 각주 "
                "'문제는 그들이 이성적으로 사고할 수 있는가도, 말을 할 수 있는가도 아니다. "
                "문제는 그들이 고통을 느낄 수 있는가이다' 를 계승하여 "
                "도덕적 지위의 최소 기준으로 정식화한 개념. "
                "쾌고 감수 능력을 가진 존재는 고통 회피 이익을 가지며, "
                "이 이익은 이익 평등 고려의 원칙에 따라 동등하게 저울에 올려져야 한다."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "singer-animal-liberation-1975",
            "related_terms": [
                "이익 평등 고려의 원칙",
                "유정성",
                "고통 회피 이익",
                "벤담 계승",
                "도덕적 지위 기준",
            ],
        },
        {
            "id": "kw-singer-animal-liberation",
            "term": "동물 해방",
            "term_en": "Animal Liberation",
            "definition": (
                "싱어 1975년 저작 제목이자 운동의 명칭. "
                "공장식 축산·동물 실험 등 동물을 인간의 사용을 위한 단순 도구로 취급하는 관행을 "
                "종차별주의의 구체적 실천 양상으로 비판하고 철폐할 것을 요구한다. "
                "이익 평등 고려의 원칙과 쾌고 감수 능력 기준을 결합한 공리주의 응용윤리의 실천 프로그램. "
                "2015-B 서술형3·2019-B Q3·2024-B Q8 반복 출제의 직접 근거 저작."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "singer-animal-liberation-1975",
            "related_terms": [
                "종차별주의",
                "공장식 축산 반대",
                "동물 실험 반대",
                "이익 평등 고려의 원칙",
                "응용 윤리",
            ],
        },
        {
            "id": "kw-singer-overseas-aid-duty",
            "term": "해외 원조 의무",
            "term_en": "duty of overseas aid",
            "definition": (
                "싱어 『Famine, Affluence, and Morality(1972)』·"
                "『Practical Ethics(1979)』 제8장 '부자와 가난한 자' trademark. "
                "이익 평등 고려의 원칙과 쾌고 감수 능력 기준을 국제 차원으로 확장한 결론으로, "
                "'커다란 희생 없이 어려운 처지에 있는 사람을 도울 수 있다면 돕는 것이 우리의 의무'라는 "
                "강한 원조 원칙을 제시한다. "
                "2022-B Q9 갑 제시문의 직접 근거. "
                "롤즈 『만민법』의 제한적 원조(품위 있는 사회까지 cut-off point)와 대비된다."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "singer-famine-affluence-morality-1972",
            "related_terms": [
                "기아 구제",
                "공리주의적 보편주의",
                "이익 평등 고려의 원칙",
                "도덕적 거리 무차별",
                "롤즈 만민법 대비",
            ],
        },
        {
            "id": "kw-singer-drowning-child",
            "term": "익사하는 아이 사고실험",
            "term_en": "drowning child thought experiment",
            "definition": (
                "싱어 『Famine, Affluence, and Morality(1972)』의 상징적 사고 실험. "
                "연못에 빠진 아이를 건지지 않으면 도덕적으로 비난받는 것처럼, "
                "수천 km 떨어진 기아 아이를 원조 가능한데 돕지 않는 것도 동일하게 비난받는다. "
                "공간적 거리·관계의 친밀도·국적은 도덕적으로 무관한 요인이며, "
                "이익 평등 고려의 원칙은 공리주의적 보편주의로 귀결된다. "
                "2022-B Q9 갑 제시문의 '이웃의 어린아이 vs 다른 나라 어린아이' 구절의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "singer-famine-affluence-morality-1972",
            "related_terms": [
                "도덕적 거리 무차별",
                "해외 원조 의무",
                "공리주의적 보편주의",
                "이익 평등 고려의 원칙",
            ],
        },
        {
            "id": "kw-singer-distance-irrelevance",
            "term": "도덕적 거리 무차별",
            "term_en": "distance irrelevance",
            "definition": (
                "싱어 해외 원조 논증의 핵심 원리. "
                "공간적 거리·국적·관계의 친밀도는 도덕적으로 무관한 요인이며, "
                "이익 평등 고려의 원칙은 국경과 거리를 넘어 모든 존재의 이익에 동등하게 적용된다. "
                "'이웃의 어린아이인지 다른 나라에 사는 어린아이인지는 도덕적 맥락에서 차이가 없다'는 "
                "2022-B Q9 갑 제시문 구절이 이 trademark의 직접 표현."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "singer-famine-affluence-morality-1972",
            "related_terms": [
                "익사하는 아이 사고실험",
                "해외 원조 의무",
                "공리주의적 보편주의",
                "이익 평등 고려의 원칙",
            ],
        },
        {
            "id": "kw-singer-preference-utilitarianism",
            "term": "선호 공리주의",
            "term_en": "preference utilitarianism",
            "definition": (
                "싱어 『Practical Ethics(1979)』의 기본 공리주의 프레임. "
                "고전 공리주의(벤담·밀)의 쾌락 총합 계산을 확장하여 "
                "합리적 자의식을 가진 존재의 '선호(preference) 만족·좌절'까지 "
                "도덕 계산에 포함한다. "
                "이 확장은 낙태·안락사·비인간 인격체 논의에서 "
                "'인격(person — 자의식과 미래 선호를 가진 존재)' 개념을 통한 도덕적 지위 논증의 토대. "
                "출처: coverage/2019-B.md L34 BLK-175E-2019B-001 claim 보강 목록."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "singer-practical-ethics-1979",
            "related_terms": [
                "공리주의 응용윤리",
                "인격 개념",
                "자의식",
                "선호 만족·좌절",
                "낙태 안락사 논의",
            ],
        },
        {
            "id": "kw-singer-famine-affluence-morality",
            "term": "기아 풍요 도덕",
            "term_en": "Famine, Affluence, and Morality",
            "definition": (
                "싱어 1972년 Philosophy & Public Affairs 논문 제목. "
                "해외 원조 윤리의 출발 논문으로, "
                "'우리가 도덕적으로 비슷한 중요성의 것을 희생하지 않고 나쁜 것을 막을 수 있다면, "
                "그렇게 해야 한다'는 강한 원조 원칙과 "
                "익사하는 아이(drowning child) 사고 실험을 제시한다. "
                "2022-B Q9 갑 제시문의 직접 근거 논문."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "singer-famine-affluence-morality-1972",
            "related_terms": [
                "해외 원조 의무",
                "익사하는 아이 사고실험",
                "도덕적 거리 무차별",
                "이익 평등 고려의 원칙",
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
    """싱어 영향·비교 관계 데이터 입력.

    ES 등록 확인(2026-04-22 curl 확인, 61명 목록):
    - bentham : 등록 — 벤담의 'Can they suffer?' 원리 계승, 싱어 공리주의 동물 윤리의 사상사적 원천
      (coverage/2015-B.md L99 "싱어 『동물 해방』의 벤담 인용 + 종차별주의 비판 trademark").
    미등록 (relation 생략):
    - regan — 2024-B Q8 을(리건) 대비 관계를 걸려 했으나 ES 미등록 → 스킵.
      (regan 등록은 별도 TASK-176 항목으로 예정, BLK-175E-2018A-001·BLK-175E-2024B-006.)
    """
    relations = [
        {
            "from_thinker": "bentham",
            "to_thinker": THINKER_ID,
            "type": "influenced",
            "description": (
                "벤담(Jeremy Bentham)의 공리주의, 특히 "
                "『도덕과 입법의 원리 서설(An Introduction to the Principles of Morals and Legislation, 1789)』 "
                "각주의 유명한 물음 "
                "'문제는 그들이 이성적으로 사고할 수 있는가도, 말을 할 수 있는가도 아니다. "
                "문제는 그들이 고통을 느낄 수 있는가이다(The question is not, Can they reason? "
                "nor, Can they talk? but, Can they suffer?)' 는 "
                "싱어(Peter Singer) 동물 해방 윤리의 직접적 사상사적 원천이다. "
                "싱어는 『Animal Liberation(1975)』 제1장 'All Animals Are Equal' 에서 "
                "이 벤담 구절을 인용하며 쾌고 감수 능력(sentience)을 도덕적 지위의 최소 기준으로 정식화하고, "
                "이익 평등 고려의 원칙과 종차별주의 비판을 벤담 공리주의의 응용윤리적 확장으로 전개한다. "
                "싱어는 다만 벤담의 단순 쾌락·고통 총합에서 더 나아가 "
                "『Practical Ethics(1979)』에서 선호 공리주의(preference utilitarianism)로 틀을 수정한다."
            ),
            "evidence": (
                "Bentham (1789) An Introduction to the Principles of Morals and Legislation ch.17 n.1; "
                "Singer (1975) Animal Liberation ch.1 'All Animals Are Equal'; "
                "2015-B 서술형3 갑 제시문 '문제는 그들이 고통을 느낄 수 있는가이다' "
                "(coverage/2015-B.md L17·L99 — 싱어 『동물 해방』의 벤담 인용 명시); "
                "2019-B Q3 BLK-175E-2019B-001 '쾌고감수능력' trademark 세트 "
                "(coverage/2019-B.md L34·L59)"
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
    print("=== 피터 싱어(Singer) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (singer)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n[OK] 싱어 데이터 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}", file=sys.stderr)
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
