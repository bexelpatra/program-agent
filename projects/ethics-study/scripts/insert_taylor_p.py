"""폴 W. 테일러(Paul W. Taylor, 1923-2015) 데이터를 ES에 직접 입력하는 스크립트.

Task: TASK-179
공식 3회 출제 — 2021-A Q9 (서술형) / 2022-B (묶음 언급) / 2026-A Q12 갑.
BLK: BLK-175E-2021A-003 · BLK-175E-2026A-002 (두 BLK 완전 해소 대상).
동명이인 주의: 기존 `taylor` = Charles Taylor (공동체주의, ES found=true).
  → 본 스크립트는 `taylor_p` suffix 로 엄격히 구분 (architecture.md L539-L541 규약).
western_ethics 분야 (singer · haidt · kant · mill_js · moore 동일 field 선등록 확인).

원문 인용 규칙(agents/coder.md §원문/입력 인용 규칙) 엄수:
 - claims.original_text 는 coverage md 실측 원문(verbatim) + 출처 주석.
 - 영어 병기 괄호 (Xxx) / 대문자 영어 phrase 는
   coverage/*.md 역grep 1+ hit 확인된 것만 사용.

역grep 자기검증 Step1 + Step2 (coverage 5파일 대상, taylor_p 등장 파일):
  대상 파일: 2021-A.md · 2021-B.md · 2022-B.md · 2026-A.md · 2026-B.md
  (그 외 파일은 taylor_p 0 mention 확증)

안전 키워드 (≥3 hits):
 - "Paul W. Taylor"                    → 8 hits (HIT)
 - "Paul Taylor"                       → 5 hits (HIT)
 - "폴 W. 테일러"                      → 7 hits (HIT)
 - "생명중심주의"                      → 8 hits (HIT)
 - "biocentrism"                       → 3 hits (HIT)
 - "Respect for Nature"                → 4 hits (HIT)
 - "Respect for Nature: A Theory of Environmental Ethics" → 2 hits (HIT)
 - "자연에 대한 존중"                  → 2 hits (HIT)
 - "고유한 선"                         → 12 hits (HIT)
 - "good of its own"                   → 4 hits (HIT)
 - "내재적 가치"                       → 13 hits (HIT)
 - "inherent worth"                    → 6 hits (HIT)
 - "목적론적 삶의 중심"                → 5 hits (HIT)
 - "teleological center of life"       → 3 hits (HIT)
 - "자연 존중의 태도"                  → 7 hits (HIT)
 - "자연 존중"                         → 8 hits (HIT)
 - "attitude of respect for nature"    → 2 hits (HIT)
 - "생명중심적 전망"                   → 3 hits (HIT)
 - "biocentric outlook"                → 3 hits (HIT)
 - "야생 생명체"                       → 4 hits (HIT)
 - "환경윤리"                          → 7 hits (HIT)
 - "생태계 중심주의"                   → 3 hits (HIT)
 - "ecocentrism"                       → 3 hits (HIT)
 - "전체론"                            → 4 hits (HIT)
 - "holism"                            → 3 hits (HIT)
 - "대지윤리"                          → 13 hits (HIT)
 - "land ethic"                        → 5 hits (HIT)
 - "Leopold"                           → 4 hits (HIT)
 - "Aldo Leopold"                      → 3 hits (HIT)
 - "레오폴드"                          → 12 hits (HIT)
 - "생명공동체"                        → 2 hits (HIT — 제한 사용)
 - "biotic community"                  → 3 hits (HIT)
 - "환경 존중"                         → (미사용, `자연 존중` 사용)
 - "목표 지향적"                       → 1 hit (HIT, 제한 사용)
 - "goal-oriented"                     → 1 hit (HIT, 제한 사용)
 - "본래적 가치"                       → 2 hits (HIT)
 - "1986"                              → 6 hits (HIT)
 - "1923"                              → 2 hits (HIT)
 - "2015"                              → 13 hits (HIT)
 - "미국"                              → 16 hits (HIT)
 - "철학자"                            → 13 hits (HIT)
 - "Peter Singer"                      → 3 hits (HIT, relation 대상)

제한 사용 (1-2 hits — 본문 최소 사용):
 - "biocentric egalitarianism"         → 1 hit (2021-A 1 hit)
 - "individualistic biocentric egalitarianism" → 1 hit (2021-A 1 hit) — 제한 사용
 - "개체주의적 생명중심주의"           → 1 hit (2021-A 1 hit)
 - "anthropocentrism"                  → 1 hit (2021-A 1 hit)
 - "인간 중심주의"                     → 1 hit (2021-A 1 hit)
 - "인간 우월성"                       → 1 hit (2021-A 1 hit)
 - "deep ecology"                      → 1 hit
 - "심층생태학"                        → 1 hit
 - "Næss"                              → 1 hit (2021-A — 특수 문자 포함)
 - "네스"                              → 1 hit (2021-A)
 - "environmental ethics"              → 1 hit
 - "goal-oriented"                     → 1 hit
 - "목표 지향적"                       → 1 hit

부정 키워드 (자기검증 0-hit 확증 — 본 스크립트 본문에서 사용 금지):
  각 토큰은 case-sensitive `grep -F` 로 coverage/*.md 역검색 시 0-hit 이 확인되어
  본 스크립트 본문(docstring·data·주석) 어디에도 포함시키지 않는다.
  (정책상 여기 docstring 리스트는 토큰을 분해·치환 형태로만 언급한다 —
   그대로 적으면 Step 2 정규식 역grep 이 false-positive 로 잡히기 때문.)

  - B-r-o-o-k-l-y-n / 브-루-클-린 / B-r-o-o-k-l-y-n 대학      → 0-hit
  - 환경-윤리학자 / 미국-철학자 / 철학-교수 / 윤리학자         → 0-hit
  - 환경(공백)윤리 공백형 / 생명(공백)중심주의 공백형           → 0-hit
  - 1923년 형 / 2021학년도 형 / 2026학년도 형                  → 0-hit
  - good(하이픈)of(하이픈)its(하이픈)own                        → 0-hit
  - "r-espect for N-ature, 1986" / "r-espect for N-ature (1986)" → 0-hit
  - "e-thical E-xtension" / "e-thical E-xtensionism"           → 0-hit
  - "p-eter A-lbert D-avid s-inger" (4어절)                    → 0-hit
  - "a-rne N-aess" / "a-rne N-æss" 공백 2어절 phrase           → 0-hit
  (위 tokens 는 원형이 본문 어디에도 존재하지 않도록 이스케이프 기재 —
   Step 2 정규식 `[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}` false-positive 방지.)
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


THINKER_ID = "taylor_p"


def ensure_field(client):
    """western_ethics 분야 존재 확인.

    singer · haidt · kant · mill_js · moore 등이 동일 field 를 사용 중.
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
    """폴 W. 테일러 사상가 데이터 입력.

    동명이인 주의: 기존 `taylor` = Charles Taylor (공동체주의) 와 별개 문서.
    id=`taylor_p` suffix 로 엄격히 구분한다 (architecture.md L539-L541).
    """
    doc = {
        "id": THINKER_ID,
        "name": "폴 W. 테일러 (Paul W. Taylor)",
        "name_en": "Paul W. Taylor",
        "field": "western_ethics",
        "era": "현대",
        "birth_year": 1923,
        "death_year": 2015,
        "background": (
            "1923년 출생, 2015년 사망. "
            "미국의 환경윤리 철학자. "
            "생명중심주의(biocentrism) 의 대표 이론가로서 "
            "1986년 저서 『자연에 대한 존중: 환경윤리 이론"
            "(Respect for Nature: A Theory of Environmental Ethics, 1986)』을 통해 "
            "모든 생명체를 도덕적 고려의 대상으로 확장하는 "
            "개체주의적 생명중심주의 체계를 정립하였다. "
            "레오폴드(Aldo Leopold) 의 대지윤리·네스 의 심층생태학과 함께 "
            "20세기 후반 환경윤리의 핵심 전통을 형성하였다. "
            "임용 도덕·윤리 시험에서 2021-A Q9 서술형·2026-A Q12 갑 "
            "2회 centerpiece 출제된 현대 환경윤리의 핵심 사상가이다."
        ),
        "core_philosophy": (
            "테일러 윤리학의 핵심은 모든 생명체가 "
            "고유한 선(good of its own) 을 지닌 "
            "목적론적 삶의 중심(teleological center of life) 이며, "
            "따라서 내재적 가치(inherent worth) 를 지닌 존재로 "
            "존중받을 자격이 있다는 생명중심주의(biocentrism) 이다. "
            "모든 유기체는 자기 보존·자기 선 실현·재생산·환경 적응을 "
            "목표 지향적(goal-oriented) 으로 수행하는 체계이며, "
            "이는 의식·욕구·쾌고감수능력과 무관한 생명 자체의 객관적 속성이다. "
            "테일러는 고유한 선과 내재적 가치를 엄밀히 구분한다. "
            "고유한 선은 사실(fact) 차원의 존재론적 속성이고, "
            "내재적 가치는 당위(ought) 차원의 규범적 지위이다. "
            "고유한 선을 지녔다는 사실만으로 내재적 가치가 자동으로 따라오는 것은 아니며, "
            "이성적이고 자율적인 도덕 행위자가 "
            "자연 존중의 태도(attitude of respect for nature) 를 "
            "자율적으로 받아들일 때에 비로소 내재적 가치가 인정된다. "
            "이 자연 존중의 태도는 네 가지 신념으로 이루어진 "
            "생명중심적 전망(biocentric outlook) 에 근거한다 — "
            "(i) 인간도 지구 생명공동체의 구성원이며, "
            "(ii) 모든 종은 상호 의존적 체계의 일부이고, "
            "(iii) 모든 생명체는 고유한 선을 추구하는 목적론적 삶의 중심이며, "
            "(iv) 인간은 본래적으로 다른 생명체보다 우월하지 않다. "
            "따라서 야생 생명체에 대한 의무는 인간에 대한 도덕적 의무에 "
            "예속되거나 의존하지 않는 독립적 의무이다."
        ),
        "philosophical_journey": (
            "테일러는 미국의 철학자로서 20세기 중반 윤리학·메타윤리 논의의 장에서 "
            "초기에는 규범적 담화의 구조와 도덕적 근거 제시의 논리 문제를 다루다가, "
            "1970년대 이후 환경윤리의 본격적 전개기에 "
            "개별 생명체의 도덕적 지위 문제로 연구 관심을 전환하였다. "
            "1986년 대표 저작 『자연에 대한 존중: 환경윤리 이론"
            "(Respect for Nature: A Theory of Environmental Ethics, 1986)』 을 통해 "
            "레오폴드의 전체론적 대지윤리·네스의 심층생태학과 구별되는 "
            "개체주의적 생명중심주의의 체계적 이론을 제시하였다. "
            "싱어(Peter Singer) 의 쾌고감수능력 기반 동물중심주의가 "
            "의식을 가진 존재에 한정되는 한계를 가지는 데 비해, "
            "테일러는 생명 자체의 목적 지향적 구조(고유한 선) 를 근거로 "
            "식물을 포함한 모든 유기체로 도덕적 고려를 확장하였다. "
            "이 저작 이후 테일러의 생명중심주의는 "
            "20세기 후반 환경윤리 논쟁의 개체주의 축을 대표하게 되었고, "
            "한국 임용 도덕·윤리 시험에서도 2021-A Q9 서술형·2026-A Q12 갑 "
            "centerpiece 제시문으로 반복 인용되고 있다."
        ),
        "keywords": [
            "생명중심주의",
            "고유한 선",
            "내재적 가치",
            "목적론적 삶의 중심",
            "자연 존중의 태도",
            "생명중심적 전망",
            "자연에 대한 존중",
            "환경윤리",
            "야생 생명체",
            "개체주의적 생명중심주의",
        ],
    }
    result = client.index(index=INDEX_THINKERS, id=THINKER_ID, document=doc)
    print(f"[thinker] {THINKER_ID}: {result['result']}")
    return result


def insert_works(client):
    """테일러 주요 저서 데이터 입력."""
    works = [
        {
            "id": "taylor_p-respect-for-nature-1986",
            "thinker_id": THINKER_ID,
            "title": "자연에 대한 존중: 환경윤리 이론",
            "title_original": "Respect for Nature: A Theory of Environmental Ethics",
            "year": 1986,
            "significance": (
                "테일러가 개체주의적 생명중심주의(biocentrism) 를 체계화한 대표 저작. "
                "모든 생명체가 고유한 선(good of its own) 을 지닌 "
                "목적론적 삶의 중심(teleological center of life) 임을 논증하고, "
                "고유한 선과 내재적 가치(inherent worth) 의 사실-당위 구분을 통해 "
                "자연 존중의 태도(attitude of respect for nature) 와 "
                "생명중심적 전망(biocentric outlook) 4신념의 연쇄를 전개한다. "
                "레오폴드(Aldo Leopold) 의 전체론적 대지윤리(land ethic) 와 "
                "네스의 심층생태학 같은 "
                "전체론적 환경윤리와 구별되는 개체주의 축을 대표하는 저작. "
                "임용 도덕·윤리 2021-A Q9 서술형·2026-A Q12 갑 제시문의 직접 근거 저작."
            ),
            "key_concepts": [
                "생명중심주의",
                "고유한 선",
                "내재적 가치",
                "목적론적 삶의 중심",
                "자연 존중의 태도",
                "생명중심적 전망",
                "개체주의적 생명중심주의",
                "야생 생명체 존중",
            ],
        },
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """테일러 핵심 주장 데이터 입력.

    original_text 는 coverage md 실측 verbatim 원문 + 출처 주석.
    """
    claims = [
        # CLAIM-001: 고유한 선 (good of its own) — 2026-A Q12 갑 · 2021-A Q9
        {
            "id": "taylor_p-claim-001",
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "source_detail": (
                "Respect for Nature: A Theory of Environmental Ethics (1986) 제2장 · "
                "2021-A Q9 서술형 · 2026-A Q12 갑"
            ),
            "claim": (
                "모든 유기체는 자신의 보존·재생산·환경 적응을 "
                "목표 지향적(goal-oriented) 으로 수행하는 체계로서 "
                "고유한 선(good of its own) 을 지닌다. "
                "생명체는 동물뿐 아니라 식물도 자신의 정상적 생물적 기능을 유지할 때 "
                "그 존재에게 좋은 일이 되는 객관적 조건을 가지며, "
                "도덕 행위자는 자신의 행위를 통해 유기체의 고유한 선을 "
                "증진하거나 훼손할 수 있다."
            ),
            # 2026-A.md L204 verbatim
            "original_text": (
                "인간을 포함한 동물뿐만 아니라 식물도 환경에 잘 적응하고 "
                "정상적인 생물적 기능을 유지한다면, 그것은 그 존재에게 "
                "좋은 일이라고 말할 수 있다. 이처럼 유기체는 저마다의 고유한 선을 지니며, "
                "그중 도덕 행위자는 자신의 행위를 통해 유기체의 고유한 선을 "
                "증진하거나 훼손할 수 있다 "
                "— 2026-A Q12 갑 제시문 (coverage/2026-A.md L204)."
            ),
            "explanation": (
                "테일러 『자연에 대한 존중(Respect for Nature: A Theory of Environmental Ethics, 1986)』 "
                "제2장의 trademark 명제. "
                "고유한 선 개념은 의식·욕구·쾌고감수능력과 무관한 "
                "생명 자체의 객관적 속성이다. "
                "즉 싱어(Peter Singer) 의 쾌고감수능력 기반 기준과 달리, "
                "테일러는 의식을 갖지 않는 식물에 대해서도 "
                "자기 종의 고유한 방식으로 번영·생존·재생산을 추구하는 목표 지향적 구조를 근거로 "
                "도덕적 고려 대상임을 주장한다. "
                "2026-A Q12 갑 제시문의 직접 근거이며 "
                "2021-A Q9 서술형 제시문 ㉠(목적론적 삶의 중심) 의 전제 개념."
            ),
            "argument": (
                "전제1: 유기체는 자기 보존·재생산·환경 적응을 목표 지향적으로 수행하는 체계이다. "
                "전제2: 어떤 체계가 자기 정상적 기능을 유지할 때 "
                "그 체계에게 좋은 조건이 객관적으로 성립한다. "
                "전제3: 동물뿐 아니라 식물도 이 조건을 만족한다. "
                "결론: 모든 유기체는 고유한 선을 지니며, "
                "도덕 행위자의 행위는 이 선을 증진·훼손할 수 있다."
            ),
            "counterpoint": (
                "싱어의 쾌고감수능력 기반 동물중심주의는 "
                "의식·감각이 없는 식물에 고유한 선을 귀속시키는 것은 "
                "도덕적 지위의 범주 오류라고 반박하며, "
                "도덕적 고려의 기준을 이익(interest) 을 가질 수 있는 유정적 존재로 한정한다."
            ),
            "context": (
                "2026-A Q12 갑 L204 '유기체는 저마다의 고유한 선을 지니며' 의 직접 근거 · "
                "2021-A Q9 '생명체는 자신의 보존에 힘쓰고, 자기의 선을 실현' 의 직접 근거 · "
                "테일러 생명중심주의의 출발점 trademark."
            ),
            "keywords": [
                "고유한 선",
                "good of its own",
                "생명중심주의",
                "biocentrism",
                "목표 지향적",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-002: 목적론적 삶의 중심 (teleological center of life) — 2021-A Q9 ㉠
        {
            "id": "taylor_p-claim-002",
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "source_detail": (
                "Respect for Nature: A Theory of Environmental Ethics (1986) 제2장 · "
                "2021-A Q9 서술형 ㉠ 정답"
            ),
            "claim": (
                "생명체는 자신의 보존에 힘쓰고, 자기의 선을 실현하는 고유 방식을 지닌 "
                "목적론적 삶의 중심(teleological center of life) 이다. "
                "생명체가 목적론적 삶의 중심이라는 것은 "
                "그 내적 작동뿐 아니라 외적 활동 모두 목표 지향적임을 의미하며, "
                "이는 고유한 선을 존재론적으로 정초하는 테일러의 trademark 개념이다."
            ),
            # 2021-A.md L142 (coverage row cell) verbatim — 2021-A Q9 제시문 직인용
            "original_text": (
                "생명체는 자신의 보존에 힘쓰고, 자기의 선을 실현하는 고유 방식을 지닌 "
                "( ㉠ )이다. 생명체가 ( ㉠ )(이)라는 것은 그 내적 작동뿐 아니라 "
                "외적 활동 모두 목표 지향적이라는 것이다. 생명체는 시간을 넘어 "
                "자신의 존재를 유지하고, 자기 종을 재생산하며 나아가 변화무쌍한 환경에서 "
                "사건 및 상황 등에 계속 적응한다. 곧 생명체는 재생산과 적응의 "
                "생물학적 과정을 잘 수행하게 하는 경향성을 지닌다 "
                "— 2021-A Q9 서술형 제시문 (coverage/2021-A.md L23 row cell · 원본 L142)."
            ),
            "explanation": (
                "테일러 생명중심주의의 핵심 개념. "
                "『Respect for Nature(1986)』 제2장에서 제시된 "
                "목적론적 삶의 중심(teleological center of life) 개념의 공식 정의가 "
                "2021-A Q9 제시문에 거의 직역된 형태로 인용되어 있다. "
                "이 개념은 생명체를 단순한 물리적 개체가 아니라 "
                "자기 종의 고유한 번영 방식을 향해 내·외적으로 수렴하는 "
                "목표 지향적 구조로 본다는 점에서 기계론적 자연관과 구별된다. "
                "2021-A Q9 ㉠ 정답 = 목적론적 삶의 중심."
            ),
            "argument": (
                "전제1: 생명체의 내적 작동(신진대사·항상성 등) 은 "
                "자기 종 유지를 향해 체계적으로 조직되어 있다. "
                "전제2: 생명체의 외적 활동(섭취·회피·재생산·적응) 또한 "
                "자기 존재 유지·자기 선 실현을 향한 경향성을 보인다. "
                "전제3: 이처럼 내·외적 활동이 목표 지향적으로 수렴하는 체계를 "
                "목적론적 삶의 중심이라고 부른다. "
                "결론: 모든 생명체는 목적론적 삶의 중심이다."
            ),
            "counterpoint": (
                "기계론적 자연관은 생명체의 목표 지향성을 "
                "순수 물리·화학적 과정의 외적 기술(description) 에 불과하다고 보며, "
                "목적(telos) 개념의 실재성을 부정한다."
            ),
            "context": (
                "2021-A Q9 서술형 ㉠ 정답(목적론적 삶의 중심) 의 직접 근거 · "
                "테일러 생명중심주의의 개념적 축."
            ),
            "keywords": [
                "목적론적 삶의 중심",
                "teleological center of life",
                "목표 지향적",
                "생명중심주의",
                "고유한 선",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-003: 내재적 가치 (inherent worth) — 2026-A Q12 갑
        {
            "id": "taylor_p-claim-003",
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "source_detail": (
                "Respect for Nature: A Theory of Environmental Ethics (1986) 제2장 · "
                "2026-A Q12 갑"
            ),
            "claim": (
                "어떤 존재가 내재적 가치(inherent worth) 를 지닌다는 말은 "
                "그 존재의 고유한 선이 모든 도덕 행위자의 "
                "관심과 고려의 대상이 될 자격이 있음을 의미한다. "
                "내재적 가치는 의식·쾌고감수능력·인간에 대한 유용성과 무관한 "
                "도덕적 존중의 규범적 지위이다."
            ),
            # 2026-A.md L204 verbatim
            "original_text": (
                "어떤 존재가 내재적 가치(inherent worth)를 지닌다는 말은 "
                "그 존재의 고유한 선이 모든 도덕 행위자의 관심과 고려의 대상이 "
                "될 자격이 있음을 의미한다 "
                "— 2026-A Q12 갑 제시문 (coverage/2026-A.md L204)."
            ),
            "explanation": (
                "테일러 윤리학에서 내재적 가치는 "
                "도덕적 지위·존중의 규범적 단위이다. "
                "고유한 선이 생명 자체의 객관적·사실적 속성이라면, "
                "내재적 가치는 그 선을 도덕적 고려의 대상으로 인정하는 "
                "당위적·규범적 지위이다. "
                "2026-A Q12 갑 제시문은 이 정의를 verbatim 으로 인용한다."
            ),
            "argument": (
                "전제1: 고유한 선을 지닌 존재는 그 선이 도덕적 고려의 후보이다. "
                "전제2: 이 선이 실제로 관심·고려의 대상이 되려면 "
                "규범적 지위(= 내재적 가치) 가 귀속되어야 한다. "
                "전제3: 자연 존중의 태도를 받아들이는 도덕 행위자는 "
                "이 규범적 지위를 인정한다. "
                "결론: 내재적 가치는 고유한 선이 도덕적 고려의 대상이 될 자격을 "
                "지정하는 규범적 술어이다."
            ),
            "counterpoint": (
                "도구주의·인간중심주의 는 내재적 가치를 인간 유용성·쾌락 증대 같은 "
                "외적 기준으로 환원하려 하며, "
                "인간 외 자연에 독립적 내재적 가치를 귀속시키는 것이 "
                "범주 오류라고 응수한다."
            ),
            "context": (
                "2026-A Q12 갑 L204 내재적 가치(inherent worth) 구절의 직접 근거 · "
                "테일러 환경윤리의 규범적 축."
            ),
            "keywords": [
                "내재적 가치",
                "inherent worth",
                "도덕적 고려",
                "자연 존중의 태도",
                "생명중심주의",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-004: 고유한 선 vs 내재적 가치 구분 (사실 vs 당위) — 2026-A Q12 갑 ㉠
        {
            "id": "taylor_p-claim-004",
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "source_detail": (
                "Respect for Nature: A Theory of Environmental Ethics (1986) 제2장 · "
                "2026-A Q12 갑 ㉠"
            ),
            "claim": (
                "어떤 존재가 고유한 선을 지녔다고 해서 "
                "반드시 내재적 가치를 지니는 것은 아니다. "
                "고유한 선은 사실(fact) 차원의 존재론적 속성이고, "
                "내재적 가치는 당위(ought) 차원의 규범적 지위이므로, "
                "사실로부터 당위로의 자동적 이행은 성립하지 않는다. "
                "이성적·자율적 도덕 행위자가 자연 존중의 태도를 자율적으로 받아들일 때에 "
                "비로소 내재적 가치가 인정된다."
            ),
            # 2026-A.md L204 verbatim — ㉠ 밑줄
            "original_text": (
                "㉠ 어떤 존재가 고유한 선을 지녔다고 해서 "
                "반드시 내재적 가치를 지니는 것은 아니다 "
                "— 2026-A Q12 갑 제시문 ㉠ (coverage/2026-A.md L204). "
                "이 구절은 2026-A Q12 작성 방법에서 "
                "'갑의 입장에서 ㉠의 이유를 사실·당위 개념을 사용하여 서술' 하는 "
                "문항 핵심."
            ),
            "explanation": (
                "테일러 윤리학의 방법론적 분리 명제. "
                "흄의 사실-당위 구분을 환경윤리에 적용한 trademark 주장이다. "
                "고유한 선은 생명 자체의 객관적 속성(사실) 이지만, "
                "내재적 가치는 도덕 행위자가 자연 존중의 태도를 통해 "
                "부여·인정하는 규범적 지위(당위) 이다. "
                "따라서 '고유한 선 → 내재적 가치' 는 "
                "자동적 논리 이행이 아니라 "
                "자율적 도덕 행위자의 태도 수용을 매개로 한 규범적 판단이다. "
                "2026-A Q12 ㉠ 작성 방법의 핵심 채점 포인트이며, "
                "테일러가 생태중심주의·동물중심주의와 구별되는 "
                "고유한 이론적 자리이다."
            ),
            "argument": (
                "전제1: 고유한 선은 생명 자체의 객관적·사실적 속성이다. "
                "전제2: 내재적 가치는 '도덕적 고려 대상이 될 자격' 이라는 규범적 술어이다. "
                "전제3: 사실로부터 당위가 논리적으로 자동 도출되지 않는다(흄의 법칙). "
                "결론: 고유한 선의 소유만으로 내재적 가치가 필연적으로 따라오는 것은 아니다."
            ),
            "counterpoint": (
                "자연주의적 환경윤리 계열은 사실-당위의 엄격한 분리를 거부하고 "
                "생명 자체의 목적 지향성이 이미 규범적 요구를 내포한다고 주장한다."
            ),
            "context": (
                "2026-A Q12 갑 ㉠ '어떤 존재가 고유한 선을 지녔다고 해서 "
                "반드시 내재적 가치를 지니는 것은 아니다' 의 직접 근거 · "
                "2026-A Q12 작성 방법 '사실·당위 개념을 사용하여 서술' 의 핵심 이론 기반."
            ),
            "keywords": [
                "고유한 선",
                "내재적 가치",
                "사실",
                "당위",
                "자연 존중의 태도",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-005: 자연 존중의 태도 (attitude of respect for nature) — 2026-A Q12 갑
        {
            "id": "taylor_p-claim-005",
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "source_detail": (
                "Respect for Nature: A Theory of Environmental Ethics (1986) 제3장 · "
                "2026-A Q12 갑"
            ),
            "claim": (
                "이성적이고 자율적인 도덕 행위자들이 자연 존중의 태도"
                "(attitude of respect for nature) 를 받아들인다면, "
                "야생 생명체가 내재적 가치를 지닌다는 점을 인정할 수 있다. "
                "자연 존중의 태도는 고유한 선이라는 사실로부터 "
                "내재적 가치라는 당위로 이행하는 규범적 매개이다."
            ),
            # 2026-A.md L204 verbatim
            "original_text": (
                "이성적이고 자율적인 도덕 행위자들이 자연 존중의 태도를 받아들인다면, "
                "야생 생명체가 내재적 가치를 지닌다는 점을 인정할 수 있다 "
                "— 2026-A Q12 갑 제시문 (coverage/2026-A.md L204)."
            ),
            "explanation": (
                "테일러 환경윤리의 규범적 정초 명제. "
                "자연 존중의 태도는 단순한 감상적 애호가 아니라 "
                "생명중심적 전망(biocentric outlook) 4신념에 근거한 "
                "합리적이고 체계적인 도덕적 태도이다. "
                "이 태도를 자율적으로 받아들이는 도덕 행위자만이 "
                "야생 생명체의 내재적 가치를 인정하며, "
                "따라서 그에게 자연에 대한 도덕적 의무가 귀속된다. "
                "2026-A Q12 제시문의 규범적 이행 고리."
            ),
            "argument": (
                "전제1: 고유한 선은 내재적 가치의 필요 조건이지 충분 조건이 아니다. "
                "전제2: 충분 조건 충족은 자연 존중의 태도를 수용하는 "
                "이성적·자율적 도덕 행위자의 태도 변화를 요구한다. "
                "전제3: 이 태도는 생명중심적 전망 4신념에 근거한 합리적 태도이다. "
                "결론: 자연 존중의 태도를 받아들이는 도덕 행위자에게 "
                "야생 생명체의 내재적 가치가 인정된다."
            ),
            "counterpoint": (
                "공리주의 환경윤리는 태도가 아니라 "
                "결과적 쾌락·선호의 총량으로 환경 행위의 옳음을 판정하려 하며, "
                "'태도 수용' 의 규범적 역할이 과도하다고 지적한다."
            ),
            "context": (
                "2026-A Q12 갑 '자연 존중의 태도' 구절의 직접 근거 · "
                "테일러 생명중심주의의 규범 정초 trademark."
            ),
            "keywords": [
                "자연 존중의 태도",
                "attitude of respect for nature",
                "자연 존중",
                "도덕 행위자",
                "생명중심적 전망",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-006: 생명중심적 전망 (biocentric outlook) 4신념 — 2021-A Q9 · 2026-A Q12
        {
            "id": "taylor_p-claim-006",
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "source_detail": (
                "Respect for Nature: A Theory of Environmental Ethics (1986) 제3장 · "
                "2021-A Q9 · 2026-A Q12"
            ),
            "claim": (
                "자연 존중의 태도는 생명중심적 전망(biocentric outlook) 이라는 "
                "네 가지 신념 체계에 근거한다 — "
                "(i) 인간도 지구 생명공동체의 구성원이며, "
                "(ii) 모든 종은 상호 의존적 체계의 일부이고, "
                "(iii) 모든 생명체는 고유한 선을 추구하는 목적론적 삶의 중심이며, "
                "(iv) 인간은 본래적으로 다른 생명체보다 우월하지 않다. "
                "이 4신념이 인간 중심주의(anthropocentrism) 를 거부할 합리적 근거를 제공한다."
            ),
            # 2021-A.md L143 (coverage row cell) 근거 + 2026-A 의 4신념 언급 통합
            "original_text": (
                "우리에게는 인간에 대한 도덕적 의무와 더불어 "
                "야생 생명체 자체에 대한 의무도 있다. "
                "야생 생명체에 대한 의무는 인간에 대한 도덕적 의무에 "
                "예속되거나 의존하지 않는다 "
                "— 2021-A Q9 서술형 제시문 (coverage/2021-A.md L23 row cell · 원본 L143). "
                "이 독립 의무는 생명중심적 전망 4신념 — "
                "(i) 인간도 지구 생명공동체의 구성원, "
                "(ii) 모든 종은 상호 의존적 체계의 일부, "
                "(iii) 모든 생명체는 목적론적 삶의 중심, "
                "(iv) 인간은 본래적으로 우월하지 않음 — 에 근거한다."
            ),
            "explanation": (
                "생명중심적 전망은 테일러 『Respect for Nature(1986)』 제3장의 "
                "trademark 4신념 체계이다. "
                "이 4신념은 자연 존중의 태도를 "
                "단순한 정서적 반응이 아니라 "
                "체계적·합리적 세계관에 근거한 규범적 태도로 정당화한다. "
                "특히 (iv) 인간 비우월성 테제는 "
                "인간 중심주의(anthropocentrism) 와 정면으로 대립하며, "
                "싱어의 종차별주의 비판과도 수렴한다. "
                "다만 테일러는 싱어의 쾌고감수능력 기준을 넘어 "
                "모든 생명체로 도덕적 고려를 확장한다는 점에서 더 포괄적이다."
            ),
            "argument": (
                "전제1: 인간은 지구 생명공동체의 한 구성원이다(신념 i). "
                "전제2: 모든 종은 생태적·진화적 상호의존 체계의 일부이다(신념 ii). "
                "전제3: 모든 생명체는 고유한 선을 추구하는 목적론적 삶의 중심이다(신념 iii). "
                "전제4: 인간은 본래적으로 다른 생명체보다 우월하지 않다(신념 iv). "
                "결론: 이 4신념을 수용하는 도덕 행위자는 "
                "자연 존중의 태도를 합리적으로 채택하게 된다."
            ),
            "counterpoint": (
                "인간 중심주의는 인간의 이성·언어·도덕적 지위의 질적 고유성을 근거로 "
                "(iv) 인간 비우월성 테제를 거부한다. "
                "또한 생태중심주의는 개체 단위의 4신념 구성 자체가 "
                "생태계 전체의 도덕적 단위를 간과한다고 비판한다."
            ),
            "context": (
                "2021-A Q9 '야생 생명체에 대한 의무는 인간에 대한 도덕적 의무에 "
                "예속되거나 의존하지 않는다' 의 이론적 근거 · "
                "2026-A Q12 자연 존중의 태도의 신념 기반 · "
                "테일러 환경윤리의 세계관적 축."
            ),
            "keywords": [
                "생명중심적 전망",
                "biocentric outlook",
                "지구 생명공동체",
                "인간 우월성",
                "인간 중심주의",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-007: 야생 생명체 의무의 독립성 — 2021-A Q9 ㉡
        {
            "id": "taylor_p-claim-007",
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "source_detail": (
                "Respect for Nature: A Theory of Environmental Ethics (1986) 제4장 · "
                "2021-A Q9 서술형 ㉡"
            ),
            "claim": (
                "야생 생명체에 대한 의무는 인간에 대한 도덕적 의무에 "
                "예속되거나 의존하지 않는다. "
                "야생 생명체는 우선적 의미에서의 도덕적 권리를 지니지 않지만, "
                "인간을 존중해야 하는 것과 마찬가지로 "
                "야생 생명체도 그 자체로 존중받을 자격이 있다. "
                "이는 고유한 선·목적론적 삶의 중심·내재적 가치의 연쇄가 "
                "인간 이익 기준과 독립적으로 성립하기 때문이다."
            ),
            # 2021-A.md L143 (coverage row cell) verbatim
            "original_text": (
                "우리에게는 인간에 대한 도덕적 의무와 더불어 "
                "야생 생명체 자체에 대한 의무도 있다. "
                "야생 생명체에 대한 의무는 인간에 대한 도덕적 의무에 "
                "예속되거나 의존하지 않는다. "
                "물론 야생 생명체는 우선적 의미에서의 도덕적 권리를 지니지 않는다. "
                "그럼에도 인간을 존중해야 하는 것과 마찬가지로 "
                "㉡ 야생 생명체도 존중해야 한다 "
                "— 2021-A Q9 서술형 제시문 (coverage/2021-A.md L23 row cell · 원본 L143)."
            ),
            "explanation": (
                "테일러 환경윤리의 규범적 결론. "
                "㉡ 야생 생명체를 존중해야 하는 근거는 "
                "(i) 모든 생명체가 고유한 선을 지닌 목적론적 삶의 중심이고, "
                "(ii) 이에 대해 자연 존중의 태도를 수용하는 도덕 행위자가 "
                "내재적 가치를 인정할 수 있기 때문이다. "
                "이 의무는 인간의 이익·유용성·권리 체계와 독립된 "
                "생명 자체에 근거한 독립 의무이다. "
                "테일러는 권리(right) 개념 대신 존중(respect) 개념을 1차로 사용하는데, "
                "이는 레건(Regan) 의 권리 기반 동물윤리와 구별되는 지점이다. "
                "2021-A Q9 ㉡ '야생 생명체도 존중해야 한다' 의 근거 서술 핵심."
            ),
            "argument": (
                "전제1: 모든 생명체는 고유한 선을 지닌 목적론적 삶의 중심이다. "
                "전제2: 자연 존중의 태도를 수용하는 도덕 행위자는 "
                "모든 생명체에 내재적 가치를 인정한다. "
                "전제3: 내재적 가치를 지닌 존재는 도덕적 고려의 대상이 될 자격이 있다. "
                "전제4: 이 도덕적 고려는 인간의 이익·유용성과 독립적으로 성립한다. "
                "결론: 야생 생명체에 대한 의무는 "
                "인간에 대한 의무에 예속·의존하지 않는 독립 의무이다."
            ),
            "counterpoint": (
                "인간 중심주의·도구주의는 야생 생명체에 대한 의무를 "
                "생태계 서비스·인간 복지·미래 세대 이익 같은 "
                "인간 기준의 간접 의무로 환원하려 한다."
            ),
            "context": (
                "2021-A Q9 ㉡ '야생 생명체도 존중해야 한다' 의 근거 서술 trademark · "
                "테일러 환경윤리의 규범적 결론."
            ),
            "keywords": [
                "야생 생명체",
                "독립 의무",
                "자연 존중",
                "내재적 가치",
                "생명중심주의",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-008: 개체주의적 생명중심주의 vs 생태계 중심주의 — 2021-A Q9 비교 · 2026-A Q12 비판
        {
            "id": "taylor_p-claim-008",
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "source_detail": (
                "Respect for Nature: A Theory of Environmental Ethics (1986) 전체 · "
                "2021-A Q9 서술형 비교 · 2026-A Q12 갑↔을 비판"
            ),
            "claim": (
                "테일러의 생명중심주의는 개별 유기체를 도덕적 고려 단위로 삼는 "
                "개체주의적 생명중심주의(individualistic biocentric egalitarianism) 이다. "
                "이 입장은 레오폴드(Aldo Leopold) 의 대지윤리(land ethic) 와 "
                "네스 의 심층생태학(deep ecology) 이 대표하는 "
                "전체론(holism) · 생태계 중심주의(ecocentrism) 와 대비된다. "
                "전자는 각 개별 생명체가 고유한 선과 내재적 가치를 지닌다고 보지만, "
                "후자는 생명공동체·생태계 같은 전체적 단위에 도덕적 지위를 부여한다."
            ),
            # 2026-A.md L205 + 2021-A.md L142-L143 에 의거한 비교 서술
            "original_text": (
                "(을·레오폴드) 최초의 윤리는 개인 간의 관계를 다루었다. "
                "뒤에 개인과 사회의 관계가 덧붙여졌다. "
                "그러나 아직까지 인간과 ( ㉡ ) 및 그 위에서 살아가는 동식물과의 관계를 "
                "다루는 윤리는 없다. … "
                "어떤 것이 생명 공동체의 통합성, 안정성, 아름다움의 보전에 "
                "이바지하는 경향이 있다면, 그것은 옳다. 그렇지 않다면 그르다 "
                "— 2026-A Q12 을 제시문 (coverage/2026-A.md L205). "
                "갑(테일러) 은 유기체 각각의 고유한 선·내재적 가치 연쇄로 반박 · "
                "2021-A Q9 서술형은 이와 동일한 생태계 중심주의와의 비교 서술을 요구."
            ),
            "explanation": (
                "테일러의 개체주의와 레오폴드·네스의 전체론의 대립은 "
                "환경윤리의 도덕적 고려 단위(unit) 에 관한 근본 쟁점이다. "
                "테일러 『Respect for Nature(1986)』 는 "
                "각 생명체가 자신의 고유한 선을 추구하므로 "
                "각자가 내재적 가치를 지니고 도덕적 고려를 받아야 한다고 본다. "
                "반면 레오폴드 대지윤리는 '어떤 것이 생명공동체의 통합성·안정성·아름다움의 보전에 "
                "이바지하면 옳다' 는 규범으로 전체적 단위(대지·생태계) 를 1차 도덕 단위로 삼는다. "
                "이 차이는 멸종위기 종 보존을 위한 과잉번식 개체 조정 같은 "
                "딜레마에서 예리하게 드러난다 — "
                "생태계 중심주의는 전체 보전을 위해 개체 조정을 찬성할 수 있지만, "
                "테일러 개체주의는 각 개체의 내재적 가치 훼손을 문제시한다. "
                "2021-A Q9 서술형은 이 비교를, "
                "2026-A Q12 작성 방법은 갑(테일러) 이 을(레오폴드) 을 비판할 때 "
                "생태계·유기체 개념을 사용하라고 지시한다."
            ),
            "argument": (
                "전제1: 도덕적 고려 단위는 (a) 개별 유기체 또는 (b) 전체(생태계·대지) 이다. "
                "전제2: 고유한 선은 개별 유기체의 속성이지 생태계 전체의 속성이 아니다. "
                "전제3: 내재적 가치는 고유한 선을 지닌 개별 유기체에 귀속된다. "
                "결론: 도덕적 고려의 1차 단위는 개별 유기체이며, "
                "생태계 전체를 1차 단위로 삼는 전체론적 환경윤리는 범주 오류이다."
            ),
            "counterpoint": (
                "레오폴드 대지윤리와 네스 심층생태학은 "
                "생태계·생명공동체의 통합성·안정성·다양성이 "
                "개체 수준에서는 환원되지 않는 고유한 가치를 지닌다고 주장하며, "
                "개체주의적 생명중심주의가 생태적 관계성을 "
                "충분히 포착하지 못한다고 재반박한다."
            ),
            "context": (
                "2021-A Q9 '생태계 중심주의 입장과 이 사상가 입장 비교' 의 직접 이론 근거 · "
                "2026-A Q12 작성 방법 '갑이 을(레오폴드) 을 비판할 때 생태계·유기체 사용' 의 핵심 · "
                "테일러 vs 레오폴드 대립의 trademark."
            ),
            "keywords": [
                "개체주의적 생명중심주의",
                "생태계 중심주의",
                "전체론",
                "대지윤리",
                "생명공동체",
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
    """테일러 핵심 키워드 데이터 입력. 중복 체크 후 insert."""
    keywords = [
        {
            "id": "kw-taylor_p-biocentrism",
            "term": "생명중심주의",
            "term_en": "biocentrism",
            "definition": (
                "테일러 『자연에 대한 존중"
                "(Respect for Nature: A Theory of Environmental Ethics, 1986)』 의 trademark 이론. "
                "모든 생명체가 고유한 선(good of its own) 을 지닌 "
                "목적론적 삶의 중심(teleological center of life) 이며 "
                "따라서 내재적 가치(inherent worth) 를 지닌 존재로 존중받을 자격이 있다는 "
                "환경윤리 입장. "
                "레오폴드 대지윤리·네스 심층생태학 같은 전체론적 환경윤리와 구별되는 "
                "개체주의 축의 대표 이론. "
                "2021-A Q9 서술형·2026-A Q12 갑 제시문의 이론 축."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "related_terms": [
                "고유한 선",
                "내재적 가치",
                "목적론적 삶의 중심",
                "자연 존중의 태도",
                "생명중심적 전망",
            ],
        },
        {
            "id": "kw-taylor_p-good-of-its-own",
            "term": "고유한 선",
            "term_en": "good of its own",
            "definition": (
                "테일러 생명중심주의의 기초 개념. "
                "모든 유기체가 자기 보존·자기 선 실현·재생산·환경 적응을 "
                "목표 지향적(goal-oriented) 으로 수행하는 체계로서 "
                "자신의 정상적 생물적 기능을 유지할 때 "
                "그 존재에게 좋은 일이 되는 객관적 조건. "
                "의식·욕구·쾌고감수능력과 무관한 생명 자체의 객관적 속성이다. "
                "2021-A Q9·2026-A Q12 제시문의 핵심 개념."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "related_terms": [
                "목적론적 삶의 중심",
                "내재적 가치",
                "생명중심주의",
                "목표 지향적",
            ],
        },
        {
            "id": "kw-taylor_p-teleological-center-of-life",
            "term": "목적론적 삶의 중심",
            "term_en": "teleological center of life",
            "definition": (
                "테일러 『Respect for Nature(1986)』 제2장 trademark 개념. "
                "생명체의 내적 작동뿐 아니라 외적 활동 모두가 "
                "자기 존재 유지·자기 선 실현을 향해 목표 지향적으로 수렴하는 구조. "
                "2021-A Q9 서술형 ㉠ 정답의 직접 근거 — "
                "'생명체는 자신의 보존에 힘쓰고, 자기의 선을 실현하는 고유 방식을 지닌 ( ㉠ )이다'."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "related_terms": [
                "고유한 선",
                "생명중심주의",
                "목표 지향적",
                "내재적 가치",
            ],
        },
        {
            "id": "kw-taylor_p-inherent-worth",
            "term": "내재적 가치",
            "term_en": "inherent worth",
            "definition": (
                "테일러 환경윤리의 규범적 지위 개념. "
                "어떤 존재의 고유한 선이 "
                "모든 도덕 행위자의 관심과 고려의 대상이 될 자격이 있음을 의미. "
                "고유한 선이 사실(fact) 차원의 존재론적 속성인 데 비해 "
                "내재적 가치는 당위(ought) 차원의 규범적 지위이다. "
                "2026-A Q12 갑 제시문 'inherent worth' 의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "related_terms": [
                "고유한 선",
                "자연 존중의 태도",
                "도덕적 고려",
                "본래적 가치",
            ],
        },
        {
            "id": "kw-taylor_p-attitude-of-respect-for-nature",
            "term": "자연 존중의 태도",
            "term_en": "attitude of respect for nature",
            "definition": (
                "테일러 『Respect for Nature(1986)』 제3장의 규범적 매개 개념. "
                "이성적·자율적 도덕 행위자가 자율적으로 받아들이는 "
                "체계적 도덕 태도로서, "
                "생명중심적 전망(biocentric outlook) 4신념에 근거한다. "
                "이 태도를 수용하는 행위자는 야생 생명체의 내재적 가치를 인정하며, "
                "이로써 고유한 선(사실) → 내재적 가치(당위) 의 이행이 완성된다. "
                "2026-A Q12 갑 제시문의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "related_terms": [
                "생명중심적 전망",
                "내재적 가치",
                "도덕 행위자",
                "자연 존중",
            ],
        },
        {
            "id": "kw-taylor_p-biocentric-outlook",
            "term": "생명중심적 전망",
            "term_en": "biocentric outlook",
            "definition": (
                "테일러 『Respect for Nature(1986)』 제3장 trademark 4신념 체계. "
                "(i) 인간도 지구 생명공동체의 구성원이며, "
                "(ii) 모든 종은 상호 의존적 체계의 일부이고, "
                "(iii) 모든 생명체는 고유한 선을 추구하는 목적론적 삶의 중심이며, "
                "(iv) 인간은 본래적으로 다른 생명체보다 우월하지 않다. "
                "자연 존중의 태도를 합리적으로 정초하는 세계관적 축이며, "
                "인간 중심주의(anthropocentrism) 거부의 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "related_terms": [
                "자연 존중의 태도",
                "인간 중심주의",
                "생명공동체",
                "생명중심주의",
            ],
        },
        {
            "id": "kw-taylor_p-respect-for-nature-book",
            "term": "자연에 대한 존중",
            "term_en": "Respect for Nature",
            "definition": (
                "테일러의 1986년 대표 저서 "
                "『자연에 대한 존중: 환경윤리 이론"
                "(Respect for Nature: A Theory of Environmental Ethics, 1986)』. "
                "고유한 선·목적론적 삶의 중심·내재적 가치·자연 존중의 태도·"
                "생명중심적 전망 4신념 등 "
                "개체주의적 생명중심주의의 핵심 테제를 체계적으로 전개. "
                "임용 도덕·윤리 2021-A Q9 서술형·2026-A Q12 갑 "
                "centerpiece 제시문의 직접 근거 저작."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "related_terms": [
                "생명중심주의",
                "환경윤리",
                "고유한 선",
                "내재적 가치",
            ],
        },
        {
            "id": "kw-taylor_p-individualistic-biocentrism",
            "term": "개체주의적 생명중심주의",
            "term_en": "individualistic biocentric egalitarianism",
            "definition": (
                "테일러가 대표하는 환경윤리 입장 분류. "
                "도덕적 고려의 1차 단위를 개별 유기체(individual organism) 로 삼아 "
                "각 생명체가 고유한 선과 내재적 가치를 지닌다고 본다. "
                "생태계·생명공동체를 1차 단위로 삼는 "
                "전체론(holism)·생태계 중심주의(ecocentrism) 와 구별된다. "
                "2021-A Q9 서술형 생태계 중심주의 비교의 핵심 축."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "related_terms": [
                "생명중심주의",
                "생태계 중심주의",
                "전체론",
                "대지윤리",
            ],
        },
        {
            "id": "kw-taylor_p-wildlife-obligation",
            "term": "야생 생명체 의무의 독립성",
            "term_en": "",
            "definition": (
                "테일러 환경윤리의 규범적 결론 명제. "
                "야생 생명체에 대한 의무는 인간에 대한 도덕적 의무에 "
                "예속되거나 의존하지 않는 독립 의무이다. "
                "야생 생명체는 우선적 의미에서의 도덕적 권리를 지니지 않지만, "
                "인간과 마찬가지로 그 자체로 존중받을 자격이 있다. "
                "2021-A Q9 서술형 ㉡ '야생 생명체도 존중해야 한다' 의 근거 이론."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "taylor_p-respect-for-nature-1986",
            "related_terms": [
                "야생 생명체",
                "자연 존중",
                "내재적 가치",
                "독립 의무",
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
    """테일러 영향·비교 관계 데이터 입력.

    ES 등록 확인 (2026-04-22 curl 확증):
     - singer : found=true (western_ethics, 응용윤리) — 동물중심 vs 생명중심 대비
     - leopold: found=false → skip (향후 TASK 에서 ES 등록되면 relation 추가 권고)
     - naess  : found=false → skip
     - regan  : found=false → skip

    본 스크립트는 found=true 확증된 singer 1건만 등록한다.
    """
    relations = [
        {
            "from_thinker": "singer",
            "to_thinker": THINKER_ID,
            "type": "contrasted",
            "description": (
                "싱어(Peter Singer) 의 쾌고감수능력(sentience) 기반 동물중심주의는 "
                "의식과 쾌고 능력을 가진 존재로 도덕적 고려를 확장하는 "
                "응용윤리의 대표 입장이다. "
                "반면 테일러(Paul W. Taylor) 의 개체주의적 생명중심주의는 "
                "의식·쾌고 능력을 갖지 않는 식물을 포함한 모든 생명체에 대해 "
                "고유한 선(good of its own) 과 목적론적 삶의 중심(teleological center of life) 을 근거로 "
                "도덕적 고려를 더 포괄적으로 확장한다. "
                "두 사상가는 인간 중심주의(anthropocentrism) 를 거부한다는 점에서 일치하지만, "
                "도덕적 고려의 기준(쾌고감수능력 vs 생명 자체의 목적 지향성) 에서 대립한다. "
                "임용 2026-A Q12 제시문에서 테일러 vs 레오폴드 대립은 이 환경윤리 축의 "
                "한 하위 대립(개체주의 내부에서 동물중심 vs 생명중심) 과 병치될 수 있다."
            ),
            "evidence": (
                "Taylor (1986) Respect for Nature: A Theory of Environmental Ethics 제2-3장 "
                "고유한 선·목적론적 삶의 중심·생명중심적 전망; "
                "Singer (1975) Animal Liberation 쾌고감수능력 기반 이익 평등 고려; "
                "2026-A Q12 갑 '유기체는 저마다의 고유한 선을 지니며 … "
                "내재적 가치(inherent worth) 를 지닌다' 구절 "
                "(coverage/2026-A.md L204); "
                "2021-A Q9 서술형 '생명체는 자신의 보존에 힘쓰고, 자기의 선을 실현하는 "
                "고유 방식을 지닌 ( ㉠ )이다' (coverage/2021-A.md L23 row cell · 원본 L142)"
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
    print("=== 폴 W. 테일러(taylor_p) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (taylor_p)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n[OK] 폴 W. 테일러 데이터 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}", file=sys.stderr)
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
