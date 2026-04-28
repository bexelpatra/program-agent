"""알도 레오폴드(Aldo Leopold) 데이터를 ES에 직접 입력하는 스크립트.

Task: TASK-180 (Track A 2번째)
공식 출제 — 2026-A Q12 을 centerpiece (row 기준 최초 등장, 1회).
BLK: BLK-175E-2026A-003 (leopold 최초 등장, blocker-log.md L1091 실재) 해소 대상.
field=`western_ethics` (environmental_ethics 미등록, singer·taylor_p 선례 동일).

동명이인 주의 없음 — `leopold` 단일 id 로 고유.

원문 인용 규칙(agents/coder.md §원문/입력 인용 규칙) 엄수:
 - claims.original_text 는 coverage 실측 verbatim 원문 + 출처 주석.
 - 영어 병기 괄호 (Xxx) / 대문자 영어 phrase 는
   coverage/*.md 역grep 1+ hit 확인된 것만 사용.

자기검증 2단계 프로토콜 (Step 1 · Step 2) 사전 실측 — 2026-04-22:

안전 키워드 (≥2 hits, 인용 안전):
 - "Aldo Leopold"                          → 3 hits (HIT)
 - "Leopold"                               → 4 hits (HIT)
 - "레오폴드"                              → 12 hits (HIT)
 - "알도 레오폴드"                         → 4 hits (HIT)
 - "A Sand County Almanac"                 → 2 hits (HIT)
 - "A Sand County Almanac, 1949"           → 2 hits (HIT)
 - "Sand County"                           → 2 hits (HIT)
 - "Almanac"                               → 3 hits (HIT)
 - "모래 군"                               → 2 hits (HIT)
 - "열두 달"                               → 2 hits (HIT)
 - "대지윤리"                              → 13 hits (HIT)
 - "land ethic"                            → 5 hits (HIT)
 - "land ethic maxim"                      → 2 hits (HIT)
 - "biotic community"                      → 3 hits (HIT)
 - "biotic"                                → 3 hits (HIT)
 - "biocentrism"                           → 3 hits (HIT)
 - "ecocentrism"                           → 5 hits (HIT)
 - "holism"                                → 3 hits (HIT)
 - "integrity"                             → 9 hits (HIT)
 - "stability"                             → 6 hits (HIT)
 - "beauty"                                → 2 hits (HIT)
 - "conqueror"                             → 2 hits (HIT)
 - "plain member"                          → 2 hits (HIT)
 - "plain member and citizen"              → 1 hit (HIT)
 - "citizen"                               → 9 hits (HIT)
 - "land"                                  → 9 hits (HIT)
 - "생명 공동체"                           → 6 hits (HIT)
 - "생명공동체"                            → 2 hits (HIT)
 - "대지 공동체"                           → 1 hit (HIT)
 - "대지"                                  → 17 hits (HIT)
 - "호모 사피엔스"                         → 4 hits (HIT)
 - "정복자"                                → 5 hits (HIT)
 - "평범한 구성원"                         → 5 hits (HIT)
 - "통합성"                                → 28 hits (HIT)
 - "안정성"                                → 10 hits (HIT)
 - "아름다움"                              → 9 hits (HIT)
 - "전체론"                                → 4 hits (HIT)
 - "생태계 중심주의"                       → 3 hits (HIT)
 - "생태계"                                → 8 hits (HIT)
 - "유기체"                                → 9 hits (HIT)
 - "3단계 윤리 확장"                       → 2 hits (HIT)
 - "Paul W. Taylor"                        → 8 hits (HIT — relation 대상)
 - "Peter Singer"                          → 16 hits (HIT — relation 대상)
 - "Respect for Nature"                    → 4 hits (HIT)
 - "teleological center of life"           → 3 hits (HIT)
 - "good of its own"                       → 4 hits (HIT)
 - "inherent worth"                        → 6 hits (HIT)
 - "is-ought"                              → 5 hits (HIT)
 - "1949"                                  → 2 hits (HIT)
 - "1948"                                  → 1 hit (HIT, 제한 사용)

제한 사용 (1 hit — 본문 1회 최대):
 - "The Land Ethic"                        → 1 hit (2026-A L616)
 - "Land Ethic"                            → 1 hit
 - "environmental ethics"                  → 1 hit
 - "대지윤리(land ethic)"                   → 1 hit

부정 키워드 (자기검증 0-hit 확증 — 본 스크립트 본문 사용 금지):
  각 토큰은 case-sensitive `grep -F` 로 coverage/*.md 역검색 시 0-hit 이 확인되어
  본 스크립트 본문(docstring·data·주석) 어디에도 포함시키지 않는다.
  (정책상 여기 docstring 리스트는 토큰을 분해·치환 형태로만 언급한다 —
   그대로 적으면 Step 2 정규식 역grep 이 false-positive 로 잡히기 때문.)

 - U-n-i-v-e-r-s-i-t-y o-f W-i-s-c-o-n-s-i-n / W-i-s-c-o-n-s-i-n-M-a-d-i-s-o-n / W-i-s-c-o-n-s-i-n  → 0-hit
 - f-o-r-e-s-t-e-r / w-i-l-d-l-i-f-e m-a-n-a-g-e-m-e-n-t                                      → 0-hit
 - B-a-i-r-d C-a-l-l-i-c-o-t-t / C-a-l-l-i-c-o-t-t                                            → 0-hit
 - l-a-n-d c-o-m-m-u-n-i-t-y                                                                  → 0-hit
 - "대지(공백)윤리" 공백형                                                                    → 0-hit
 - 1887 문자열 형                                                                              → 0-hit (birth_year 정수 필드만)

Step 2 주의 (괄호 밖 대문자 시작 영어 구절 의심):
 - 본 스크립트는 괄호 밖 대문자 시작 영어 구절을 원칙적으로 쓰지 않고,
   모든 영어 표기는 `(foo bar)` 괄호 안 또는 JSON 필드 값에만 넣는다.
 - JSON 필드 값은 coverage md 에 ≥1 hit 확인된 구절만 사용.

ES 등록 확인 (2026-04-22 curl 사전 확증):
 - leopold : found=false (본 스크립트 타깃)
 - taylor_p: found=true (relation 대상)
 - singer  : found=true (relation 대상)
 - western_ethics: found=true (field)
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


THINKER_ID = "leopold"


def ensure_field(client):
    """western_ethics 분야 존재 확인.

    singer · taylor_p · haidt · kant · mill_js · moore 등 동일 field 사용 중.
    이미 존재(확증): 별도 insert 안 함.
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
    """알도 레오폴드 사상가 데이터 입력."""
    doc = {
        "id": THINKER_ID,
        "name": "알도 레오폴드 (Aldo Leopold)",
        "name_en": "Aldo Leopold",
        "field": "western_ethics",
        "era": "현대",
        "birth_year": 1887,
        "death_year": 1948,
        "background": (
            "미국의 생태학자·환경윤리 정초자. "
            "유고 저작 『모래 군(郡)의 열두 달"
            "(A Sand County Almanac, 1949)』에 수록된 논문 「대지윤리(The Land Ethic)」를 통해 "
            "도덕적 고려의 범위를 토양·물·식물·동물을 포함하는 "
            "생명 공동체(biotic community) 전체로 확장한 "
            "생태계 중심주의(ecocentrism) 환경윤리의 대표 이론가이다. "
            "레오폴드는 인류의 윤리를 3단계 윤리 확장으로 파악하고, "
            "제3단계 = 인간과 대지(land) 의 관계를 다루는 대지윤리를 정초하였다. "
            "한국 임용 도덕·윤리 2026-A Q12 을 centerpiece 제시문으로 최초 출제되었다."
        ),
        "core_philosophy": (
            "레오폴드 환경윤리의 핵심은 대지윤리(land ethic) 이다. "
            "대지윤리는 토양·물·식물·동물을 포함하는 생명 공동체(biotic community) "
            "전체를 도덕적 고려의 1차 단위로 삼는 전체론(holism) 입장이다. "
            "레오폴드는 윤리의 역사를 3단계로 본다 — "
            "제1단계는 개인 간 관계의 윤리, 제2단계는 개인과 사회 관계의 윤리, "
            "제3단계는 인간과 대지 및 그 위에서 살아가는 동식물과의 관계 윤리이다. "
            "대지윤리는 호모 사피엔스의 역할을 "
            "대지 공동체의 정복자(conqueror) 에서 "
            "그 공동체의 평범한 구성원이자 시민(plain member and citizen) 으로 변화시킨다. "
            "바람직한 대지 이용은 오직 경제적 문제로만 판단되어서는 안 되며, "
            "윤리적·심미적 판단이 함께 작동해야 한다. "
            "대지윤리의 판단 표어(land ethic maxim) 는 다음과 같다 — "
            "어떤 것이 생명 공동체의 통합성(integrity)·안정성(stability)·아름다움(beauty) 의 "
            "보전에 이바지하는 경향이 있다면 그것은 옳고, 그렇지 않다면 그르다. "
            "이 생태계 중심주의·전체론 입장은 "
            "개별 유기체를 1차 도덕 단위로 삼는 "
            "테일러(Paul W. Taylor) 의 개체주의적 생명중심주의(biocentrism) 와 "
            "도덕적 고려의 단위(unit) 에서 대립한다."
        ),
        "philosophical_journey": (
            "레오폴드는 미국의 생태학자·산림 실천가로서 "
            "야생 보전·토지 이용의 현장 경험을 이론화하는 과정을 거쳐 "
            "20세기 환경윤리의 한 축을 정초하였다. "
            "유고로 1949년 출간된 『모래 군(郡)의 열두 달"
            "(A Sand County Almanac, 1949)』에 수록된 논문 「대지윤리(The Land Ethic)」 는 "
            "생명 공동체(biotic community) 개념과 3단계 윤리 확장 도식, "
            "그리고 통합성·안정성·아름다움을 기준으로 하는 "
            "대지윤리 표어(land ethic maxim) 를 제시하여 "
            "생태계 중심주의(ecocentrism) 환경윤리의 원형 문헌으로 자리잡았다. "
            "테일러(Paul W. Taylor) 의 개체주의적 생명중심주의(biocentrism) 가 "
            "개별 유기체 각각의 고유한 선(good of its own) 을 도덕 단위로 삼는 데 비해, "
            "레오폴드 대지윤리는 생명 공동체 전체를 도덕 단위로 삼는 전체론(holism) 으로 "
            "환경윤리의 개체주의-전체론 대립 구도를 형성하였다. "
            "한국 임용 도덕·윤리 시험에서는 2026-A Q12 을 제시문으로 "
            "row 기준 최초 출제되었다."
        ),
        "keywords": [
            "대지윤리",
            "생명 공동체",
            "3단계 윤리 확장",
            "생태계 중심주의",
            "전체론",
            "통합성",
            "안정성",
            "아름다움",
            "호모 사피엔스",
            "평범한 구성원",
            "정복자",
            "대지",
        ],
    }
    result = client.index(index=INDEX_THINKERS, id=THINKER_ID, document=doc)
    print(f"[thinker] {THINKER_ID}: {result['result']}")
    return result


def insert_works(client):
    """레오폴드 주요 저서 데이터 입력."""
    works = [
        {
            "id": "leopold-work-001",
            "thinker_id": THINKER_ID,
            "title": "모래 군(郡)의 열두 달",
            "title_original": "A Sand County Almanac",
            "year": 1949,
            "significance": (
                "레오폴드의 유고 저작. 수록 논문 「대지윤리(The Land Ethic)」 를 통해 "
                "대지윤리(land ethic) · 생명 공동체(biotic community) · "
                "3단계 윤리 확장 · 대지윤리 표어(land ethic maxim) 등 "
                "생태계 중심주의(ecocentrism) · 전체론(holism) 환경윤리의 핵심 테제를 제시. "
                "호모 사피엔스의 역할을 대지 공동체의 정복자(conqueror) 에서 "
                "평범한 구성원이자 시민(plain member and citizen) 으로 전환시키는 "
                "규범적 비전을 담는다. "
                "임용 도덕·윤리 2026-A Q12 을 centerpiece 제시문의 직접 근거 저작."
            ),
            "key_concepts": [
                "대지윤리",
                "생명 공동체",
                "3단계 윤리 확장",
                "생태계 중심주의",
                "전체론",
                "통합성",
                "안정성",
                "아름다움",
                "평범한 구성원",
                "정복자",
            ],
        },
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """레오폴드 핵심 주장 데이터 입력.

    original_text 는 coverage/2026-A.md L604 블록쿼트 실측 verbatim + 출처 주석.
    """
    claims = [
        # CLAIM-001: 3단계 윤리 확장 — 2026-A Q12 을 centerpiece
        {
            "id": "leopold-claim-001",
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "source_detail": (
                "A Sand County Almanac (1949) 수록 「The Land Ethic」 서두 · "
                "2026-A Q12 을"
            ),
            "claim": (
                "인류 윤리는 3단계로 확장되어 왔다 — "
                "제1단계는 개인 간의 관계를 다루는 윤리(십계명), "
                "제2단계는 개인과 사회의 관계를 다루는 윤리(황금률), "
                "제3단계는 인간과 대지(land) 및 그 위에서 살아가는 "
                "동식물과의 관계를 다루는 대지윤리(land ethic) 이다. "
                "지금까지 제3단계 윤리가 결여되어 있으므로 "
                "대지윤리의 정립이 요청된다."
            ),
            # 2026-A.md L604 verbatim (`> 을: "..."` 블록쿼트)
            "original_text": (
                "최초의 윤리는 개인 간의 관계를 다루었다. "
                "뒤에 개인과 사회의 관계가 덧붙여졌다. "
                "그러나 아직까지 인간과 ( ㉡ ) 및 그 위에서 살아가는 동식물과의 관계를 "
                "다루는 윤리는 없다 "
                "— 2026-A Q12 을 제시문 (coverage/2026-A.md L604 블록쿼트)."
            ),
            "explanation": (
                "레오폴드 「대지윤리(The Land Ethic)」 서두의 trademark 논증. "
                "윤리의 역사를 점진적 확장의 역사로 파악하고, "
                "아직 존재하지 않는 제3단계 — 인간-대지 관계의 윤리 — 를 "
                "대지윤리(land ethic) 로 명명·정초한다. "
                "( ㉡ ) = 대지(land). "
                "2026-A Q12 작성 방법의 ㉡ 용어 기입 문항 핵심."
            ),
            "argument": (
                "전제1: 윤리는 역사적으로 관계의 범위를 점진적으로 확장해 왔다. "
                "전제2: 제1단계(개인-개인)·제2단계(개인-사회) 는 이미 정착되었다. "
                "전제3: 인간과 대지·동식물의 관계를 다루는 윤리(제3단계) 는 "
                "아직 정립되어 있지 않다. "
                "결론: 대지윤리의 정립이 규범적으로 요청된다."
            ),
            "counterpoint": (
                "인간 중심주의는 제3단계 윤리의 필요성 자체를 부인하고, "
                "환경·동식물에 대한 의무를 인간 상호 관계 윤리(제2단계) 의 "
                "간접 적용으로 환원하려 한다."
            ),
            "context": (
                "2026-A Q12 을 centerpiece 의 직접 근거 · "
                "2026-A Q12 작성 방법 ㉡ = 대지 기입 문항의 이론적 배경."
            ),
            "keywords": [
                "3단계 윤리 확장",
                "대지윤리",
                "대지",
                "land ethic",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-002: 호모 사피엔스 역할 전환 — 2026-A Q12 을
        {
            "id": "leopold-claim-002",
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "source_detail": (
                "A Sand County Almanac (1949) 수록 「The Land Ethic」 · "
                "2026-A Q12 을"
            ),
            "claim": (
                "대지윤리(land ethic) 는 호모 사피엔스의 역할을 "
                "대지 공동체의 정복자(conqueror) 에서 "
                "그 공동체의 평범한 구성원이자 시민(plain member and citizen) 으로 "
                "변화시킨다. "
                "인간은 대지를 지배·착취하는 외부 행위자가 아니라 "
                "생명 공동체의 한 구성원으로서 "
                "다른 동식물·토양·물과 함께 상호 의존하는 존재이다."
            ),
            # 2026-A.md L604 verbatim (블록쿼트)
            "original_text": (
                "( ㉡ ) 윤리는 호모 사피엔스의 역할을 "
                "( ㉡ ) 공동체의 정복자에서 그것의 평범한 구성원이자 시민으로 변화시킨다 "
                "— 2026-A Q12 을 제시문 (coverage/2026-A.md L604 블록쿼트)."
            ),
            "explanation": (
                "레오폴드 「대지윤리」의 trademark 구절. "
                "인간의 자기 이해 자체를 대지 공동체의 "
                "평범한 구성원이자 시민으로 재정위시키는 규범적 비전이다. "
                "정복자(conqueror) → 평범한 구성원이자 시민(plain member and citizen) 의 "
                "역할 전환은 전체론(holism) · 생태계 중심주의(ecocentrism) 의 "
                "인간관을 단적으로 집약한다."
            ),
            "argument": (
                "전제1: 인간은 역사적으로 대지를 지배·활용할 외부 행위자로 자기 이해해 왔다. "
                "전제2: 생태학적 사실 — 인간은 생명 공동체의 한 구성원이며 "
                "다른 구성원과 상호 의존한다 — 은 이러한 자기 이해를 반박한다. "
                "전제3: 대지윤리는 이 생태학적 사실에 근거한 새로운 자기 이해를 제안한다. "
                "결론: 인간은 정복자가 아니라 "
                "대지 공동체의 평범한 구성원이자 시민이다."
            ),
            "counterpoint": (
                "인간 중심주의는 이성·언어·도덕적 지위의 질적 고유성을 근거로 "
                "인간의 비대칭적 우위를 유지하려 하며, "
                "'평범한 구성원' 명제를 과도한 평등주의로 간주한다."
            ),
            "context": (
                "2026-A Q12 을 '호모 사피엔스의 역할을 ( ㉡ ) 공동체의 정복자에서 "
                "그것의 평범한 구성원이자 시민으로 변화시킨다' 의 직접 근거."
            ),
            "keywords": [
                "호모 사피엔스",
                "정복자",
                "평범한 구성원",
                "대지윤리",
                "생명 공동체",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-003: 대지윤리 표어 — 2026-A Q12 을
        {
            "id": "leopold-claim-003",
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "source_detail": (
                "A Sand County Almanac (1949) 수록 「The Land Ethic」 · "
                "2026-A Q12 을"
            ),
            "claim": (
                "어떤 것이 생명 공동체의 통합성(integrity)·안정성(stability)·"
                "아름다움(beauty) 의 보전에 이바지하는 경향이 있다면 그것은 옳고, "
                "그렇지 않다면 그르다. "
                "이 표어(land ethic maxim) 는 도덕적 판단의 기준을 "
                "생명 공동체 전체의 보전 여부에 둔다."
            ),
            # 2026-A.md L604 verbatim (블록쿼트)
            "original_text": (
                "어떤 것이 생명 공동체의 통합성, 안정성, 아름다움의 보전에 "
                "이바지하는 경향이 있다면, 그것은 옳다. 그렇지 않다면 그르다 "
                "— 2026-A Q12 을 제시문 (coverage/2026-A.md L604 블록쿼트)."
            ),
            "explanation": (
                "레오폴드 「대지윤리」 의 가장 유명한 trademark 명제. "
                "생명 공동체(biotic community) 전체를 도덕적 판단의 1차 단위로 삼고, "
                "통합성·안정성·아름다움이라는 세 가치의 보전을 "
                "옳고 그름의 기준으로 제시한다. "
                "이 명제는 전체론(holism) · 생태계 중심주의(ecocentrism) 의 "
                "원형 규범이며, "
                "개체주의적 생명중심주의(biocentrism) 를 대표하는 "
                "테일러(Paul W. Taylor) 입장과의 대비점으로 "
                "2026-A Q12 에서 반복 소환된다."
            ),
            "argument": (
                "전제1: 생명 공동체는 토양·물·식물·동물을 포함하는 상호 의존 체계이다. "
                "전제2: 이 체계의 통합성·안정성·아름다움은 "
                "체계 자체의 지속 가능성을 집약하는 핵심 가치이다. "
                "전제3: 어떤 행위가 이 세 가치의 보전에 이바지할 때만 "
                "그것은 공동체의 지속 가능성에 기여한다. "
                "결론: 행위의 옳고 그름은 "
                "생명 공동체의 통합성·안정성·아름다움의 보전 여부로 판정된다."
            ),
            "counterpoint": (
                "개체주의적 생명중심주의(테일러) 는 '생태계 전체' 기준만으로 "
                "도덕 판단을 내리면 개별 유기체의 고유한 선(good of its own) 과 "
                "내재적 가치(inherent worth) 가 희생될 수 있다고 비판한다. "
                "예: 생태계 보전을 위해 특정 종 개체 조정을 찬성할 때, "
                "개체 각각의 내재적 가치를 훼손하는 결과."
            ),
            "context": (
                "2026-A Q12 을 centerpiece 의 trademark 명제 · "
                "2026-A Q12 작성 방법 '갑(테일러) 이 을(레오폴드) 을 비판' 의 "
                "핵심 쟁점 이론 근거."
            ),
            "keywords": [
                "대지윤리",
                "생명 공동체",
                "통합성",
                "안정성",
                "아름다움",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-004: 생태계 중심주의·전체론 — 전체론적 도덕 단위
        {
            "id": "leopold-claim-004",
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "source_detail": (
                "A Sand County Almanac (1949) 수록 「The Land Ethic」 전체 · "
                "2026-A Q12 을 (taylor_p 대비)"
            ),
            "claim": (
                "도덕적 고려의 1차 단위는 개별 유기체가 아니라 "
                "생명 공동체(biotic community) 전체이다. "
                "생명 공동체의 통합성·안정성·아름다움이라는 전체적 가치가 "
                "개별 구성원의 이익·권리보다 규범적 우선성을 가질 수 있다. "
                "이 전체론(holism) · 생태계 중심주의(ecocentrism) 입장은 "
                "테일러의 개체주의적 생명중심주의(biocentrism) 와 "
                "도덕 단위 수준에서 대립한다."
            ),
            # 2026-A.md L604 verbatim + coverage L618 해설 기반
            "original_text": (
                "어떤 것이 생명 공동체의 통합성, 안정성, 아름다움의 보전에 "
                "이바지하는 경향이 있다면, 그것은 옳다. 그렇지 않다면 그르다 "
                "— 2026-A Q12 을 제시문 (coverage/2026-A.md L604 블록쿼트). "
                "이 명제는 생태계 중심주의(ecocentrism) · 전체론(holism) 의 원형 명제이다."
            ),
            "explanation": (
                "레오폴드 대지윤리의 도덕 단위(unit) 선택. "
                "개별 유기체 각각을 1차 도덕 단위로 삼는 "
                "테일러(Paul W. Taylor) 의 개체주의적 생명중심주의(biocentrism) 와 달리, "
                "레오폴드는 생명 공동체·대지 전체를 1차 단위로 삼는다. "
                "이 대립은 임용 2026-A Q12 갑·을 대비 구도의 핵심이며, "
                "작성 방법은 갑(테일러) 이 을(레오폴드) 을 비판할 때 "
                "'생태계·유기체' 를 사용하라고 지시한다."
            ),
            "argument": (
                "전제1: 도덕적 고려 단위는 (a) 개별 유기체 또는 (b) 생명 공동체 전체이다. "
                "전제2: 통합성·안정성·아름다움은 공동체 수준에서만 성립하는 "
                "관계적·체계적 속성이다. "
                "전제3: 개별 유기체의 고유한 선만을 도덕 단위로 삼으면 "
                "공동체 체계의 보전 요구를 놓친다. "
                "결론: 도덕적 고려의 1차 단위는 생명 공동체 전체이다."
            ),
            "counterpoint": (
                "테일러의 개체주의적 생명중심주의(biocentrism) 는 "
                "각 유기체가 자기 보존·자기 선 실현을 향하는 "
                "목적론적 삶의 중심(teleological center of life) 이고, "
                "각자가 고유한 선(good of its own) 과 내재적 가치(inherent worth) 를 지닌다고 본다. "
                "따라서 생태계 보전을 명분으로 개체 유기체의 내재적 가치를 "
                "희생시키는 판단은 비판의 대상이 된다."
            ),
            "context": (
                "2026-A Q12 작성 방법 '갑(테일러) 이 을(레오폴드) 을 비판할 때 "
                "생태계·유기체 사용' 문항의 핵심 쟁점 · "
                "환경윤리 개체주의-전체론 대립 구도의 trademark."
            ),
            "keywords": [
                "생태계 중심주의",
                "전체론",
                "생명 공동체",
                "대지윤리",
                "유기체",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-005: 대지 이용의 경제-윤리-심미 통합 판단 — 2026-A Q12 을
        {
            "id": "leopold-claim-005",
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "source_detail": (
                "A Sand County Almanac (1949) 수록 「The Land Ethic」 · "
                "2026-A Q12 을"
            ),
            "claim": (
                "바람직한 대지(land) 이용은 오직 경제적 문제로만 판단되어서는 안 된다. "
                "경제적 이익뿐 아니라 윤리적·심미적 측면에서 "
                "무엇이 옳은지를 함께 검토해야 한다. "
                "대지윤리는 도구적·경제적 가치를 넘어 "
                "윤리적·심미적 가치의 독립적 비중을 인정한다."
            ),
            # 2026-A.md L604 verbatim (블록쿼트)
            "original_text": (
                "바람직한 ( ㉡ ) 이용을 오직 경제적 문제로만 생각하지 말라. "
                "무엇이 경제적으로 이익인지 뿐만 아니라 "
                "윤리적, 심미적으로 무엇이 옳은지의 측면에서도 "
                "각각의 질문을 검토하라 "
                "— 2026-A Q12 을 제시문 (coverage/2026-A.md L604 블록쿼트)."
            ),
            "explanation": (
                "레오폴드 대지윤리의 가치 다원주의 측면. "
                "대지 이용을 경제 논리로만 축약하는 "
                "순수 도구주의·인간중심 효용주의 관점을 거부하고, "
                "윤리적·심미적 판단을 독립적 판단 축으로 도입한다. "
                "이 점에서 대지윤리는 전체론(holism) 이면서도 "
                "규범적 판단 기준의 다원성을 인정하는 입장이다."
            ),
            "argument": (
                "전제1: 대지 이용은 경제적 이익·윤리적 옳음·심미적 가치의 "
                "복수 차원에서 평가될 수 있다. "
                "전제2: 경제적 이익만을 기준으로 삼으면 "
                "윤리적·심미적 가치가 체계적으로 배제된다. "
                "전제3: 대지윤리는 생명 공동체 전체의 보전을 규범 목표로 삼는다. "
                "결론: 바람직한 대지 이용은 경제·윤리·심미의 3차원을 "
                "통합적으로 검토해야 한다."
            ),
            "counterpoint": (
                "순수 경제주의·인간중심 효용주의는 "
                "윤리·심미 가치도 결국 인간의 선호 만족으로 환원할 수 있다고 주장하며, "
                "독립적 윤리·심미 차원의 도입을 불필요한 복잡화로 본다."
            ),
            "context": (
                "2026-A Q12 을 '바람직한 ( ㉡ ) 이용을 오직 경제적 문제로만 "
                "생각하지 말라' 구절의 직접 근거."
            ),
            "keywords": [
                "대지",
                "대지윤리",
                "생명 공동체",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-006: 생명 공동체 범위 확장 — 토양·물·식물·동물 포함
        {
            "id": "leopold-claim-006",
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "source_detail": (
                "A Sand County Almanac (1949) 수록 「The Land Ethic」 · "
                "2026-A Q12 을 (해설 L617)"
            ),
            "claim": (
                "대지윤리(land ethic) 는 공동체 개념의 경계를 확장하여 "
                "토양·물·식물·동물을 모두 포함하는 생명 공동체(biotic community) 를 "
                "도덕적 단위로 삼는다. "
                "대지(land) 는 단순한 토양이 아니라 "
                "토양·물·식물·동물을 통합한 생태적 전체이다."
            ),
            # 2026-A.md L604 근거 + L617 해설 통합
            "original_text": (
                "( ㉡ ) 윤리는 호모 사피엔스의 역할을 "
                "( ㉡ ) 공동체의 정복자에서 그것의 평범한 구성원이자 시민으로 변화시킨다 "
                "— 2026-A Q12 을 제시문 (coverage/2026-A.md L604 블록쿼트). "
                "( ㉡ ) = 대지(land) 이며, 대지 공동체 개념은 "
                "토양·물·식물·동물을 포함하는 생명 공동체(biotic community) 로 확장된다 "
                "(coverage/2026-A.md L617 해설)."
            ),
            "explanation": (
                "레오폴드 대지윤리의 존재론적 기초. "
                "공동체 개념의 경계를 인간 사회 수준에서 "
                "토양·물·식물·동물을 포함하는 생태적 전체로 확장함으로써 "
                "윤리의 관계망을 재정의한다. "
                "이 생명 공동체 개념은 대지윤리 표어(land ethic maxim) 의 "
                "'생명 공동체의 통합성·안정성·아름다움' 에서 규범적 대상으로 작동한다."
            ),
            "argument": (
                "전제1: 공동체는 상호 의존하는 구성원들의 관계망이다. "
                "전제2: 토양·물·식물·동물은 인간과 상호 의존하는 생태적 관계망을 이룬다. "
                "전제3: 따라서 이들은 공동체의 구성원으로 포함되어야 한다. "
                "결론: 대지윤리의 도덕적 공동체는 "
                "토양·물·식물·동물을 포함하는 생명 공동체이다."
            ),
            "counterpoint": (
                "인간 중심주의는 공동체 개념을 이성·언어를 공유하는 "
                "인간 상호 관계로 제한하고, "
                "비-인간 자연에 대한 공동체 소속 부여를 범주 오류로 본다."
            ),
            "context": (
                "2026-A Q12 을 ㉡ = 대지 · 생명 공동체 범위 확장의 이론적 배경 · "
                "대지윤리 표어의 규범적 대상 '생명 공동체' 의 정의."
            ),
            "keywords": [
                "생명 공동체",
                "대지",
                "대지윤리",
                "생태계 중심주의",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-007: 환경윤리의 세 축 — 통합성·안정성·아름다움
        {
            "id": "leopold-claim-007",
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "source_detail": (
                "A Sand County Almanac (1949) 수록 「The Land Ethic」 · "
                "2026-A Q12 을"
            ),
            "claim": (
                "대지윤리의 규범적 판단 기준은 "
                "생명 공동체의 통합성(integrity)·안정성(stability)·"
                "아름다움(beauty) 이라는 세 가치이다. "
                "이 세 가치는 각각 생태계 체계의 구조적 온전성, "
                "변화 속에서의 지속 가능성, "
                "심미적 질을 포착하며, "
                "상호 독립적이면서도 종합적으로 도덕 판단을 구성한다."
            ),
            # 2026-A.md L604 verbatim (블록쿼트)
            "original_text": (
                "어떤 것이 생명 공동체의 통합성, 안정성, 아름다움의 보전에 "
                "이바지하는 경향이 있다면, 그것은 옳다. 그렇지 않다면 그르다 "
                "— 2026-A Q12 을 제시문 (coverage/2026-A.md L604 블록쿼트)."
            ),
            "explanation": (
                "대지윤리 표어(land ethic maxim) 의 세 판단 축. "
                "통합성은 생명 공동체 체계의 구조적 온전성, "
                "안정성은 변화·외부 교란 속에서의 체계 지속 가능성, "
                "아름다움은 심미적 질을 가리킨다. "
                "이 세 축을 '생명 공동체' 단위에서 판단하는 점이 "
                "레오폴드 환경윤리를 전체론(holism) · 생태계 중심주의(ecocentrism) 로 "
                "규정짓는 특징이다."
            ),
            "argument": (
                "전제1: 생명 공동체의 규범적 상태는 "
                "구조·지속·심미의 세 측면에서 평가된다. "
                "전제2: 이 세 측면은 각각 통합성·안정성·아름다움으로 개념화된다. "
                "전제3: 행위가 세 가치의 보전에 이바지할 때 "
                "공동체의 전체적 건강이 유지된다. "
                "결론: 옳고 그름은 통합성·안정성·아름다움의 보전 여부로 판정된다."
            ),
            "counterpoint": (
                "공리주의 환경윤리는 쾌락·선호 총량 계산으로 환경 판단을 환원하려 하고, "
                "'아름다움' 같은 심미 가치가 객관적 판단 기준이 될 수 없다고 비판한다."
            ),
            "context": (
                "2026-A Q12 을 centerpiece 의 trademark 세 가치 · "
                "대지윤리 표어의 세 판단 축."
            ),
            "keywords": [
                "통합성",
                "안정성",
                "아름다움",
                "생명 공동체",
                "대지윤리",
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
    """레오폴드 핵심 키워드 데이터 입력. 중복 체크 후 insert."""
    keywords = [
        {
            "id": "leopold-keyword-001",
            "term": "대지윤리",
            "term_en": "land ethic",
            "definition": (
                "레오폴드 『모래 군(郡)의 열두 달"
                "(A Sand County Almanac, 1949)』 수록 논문 "
                "「대지윤리(The Land Ethic)」 의 trademark 이론. "
                "인간과 대지(land) 및 그 위에서 살아가는 동식물과의 관계를 다루는 "
                "제3단계 윤리로서, "
                "토양·물·식물·동물을 포함하는 생명 공동체(biotic community) 전체를 "
                "도덕적 고려의 1차 단위로 삼는 생태계 중심주의(ecocentrism) · "
                "전체론(holism) 환경윤리의 원형. "
                "2026-A Q12 을 centerpiece 제시문의 이론 축."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "related_terms": [
                "생명 공동체",
                "3단계 윤리 확장",
                "생태계 중심주의",
                "전체론",
                "통합성",
            ],
        },
        {
            "id": "leopold-keyword-002",
            "term": "생명 공동체",
            "term_en": "biotic community",
            "definition": (
                "레오폴드 대지윤리의 도덕적 공동체 개념. "
                "토양·물·식물·동물을 포함하는 상호 의존적 생태적 전체로서, "
                "대지(land) 는 단순한 토양이 아니라 이들을 통합한 생명 공동체이다. "
                "대지윤리 표어(land ethic maxim) 는 이 공동체의 "
                "통합성·안정성·아름다움 의 보전을 "
                "도덕적 판단의 기준으로 삼는다. "
                "2026-A Q12 을 제시문 '생명 공동체의 통합성, 안정성, 아름다움' 의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "related_terms": [
                "대지윤리",
                "대지",
                "생태계 중심주의",
                "통합성",
            ],
        },
        {
            "id": "leopold-keyword-003",
            "term": "3단계 윤리 확장",
            "term_en": "",
            "definition": (
                "레오폴드 「대지윤리」 서두 trademark 도식. "
                "제1단계는 개인 간의 관계 윤리(십계명), "
                "제2단계는 개인과 사회 관계 윤리(황금률), "
                "제3단계는 인간과 대지 및 동식물과의 관계 윤리(대지윤리) 이다. "
                "레오폴드는 제3단계가 아직 정립되지 않았으므로 "
                "대지윤리의 정초가 규범적으로 요청된다고 본다. "
                "2026-A Q12 을 제시문 '최초의 윤리는 개인 간의 관계 …' 의 직접 근거."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "related_terms": [
                "대지윤리",
                "대지",
                "호모 사피엔스",
            ],
        },
        {
            "id": "leopold-keyword-004",
            "term": "호모 사피엔스의 역할 전환",
            "term_en": "",
            "definition": (
                "레오폴드 대지윤리의 인간관 전환 명제. "
                "대지윤리는 호모 사피엔스의 역할을 "
                "대지 공동체의 정복자(conqueror) 에서 "
                "그 공동체의 평범한 구성원이자 시민"
                "(plain member and citizen) 으로 변화시킨다. "
                "이 전환은 전체론(holism) · 생태계 중심주의(ecocentrism) 의 "
                "인간관을 집약하며, 2026-A Q12 을 제시문 trademark."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "related_terms": [
                "호모 사피엔스",
                "정복자",
                "평범한 구성원",
                "대지윤리",
            ],
        },
        {
            "id": "leopold-keyword-005",
            "term": "생태계 중심주의",
            "term_en": "ecocentrism",
            "definition": (
                "도덕적 고려의 1차 단위를 생태계·생명 공동체 전체에 두는 "
                "환경윤리 입장. 레오폴드의 대지윤리(land ethic) 가 대표 이론이다. "
                "개별 유기체 각각을 1차 단위로 삼는 "
                "테일러(Paul W. Taylor) 의 개체주의적 생명중심주의(biocentrism) 와 대비된다. "
                "2026-A Q12 갑·을 대비 구도의 을(레오폴드) 축."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "related_terms": [
                "전체론",
                "대지윤리",
                "생명 공동체",
            ],
        },
        {
            "id": "leopold-keyword-006",
            "term": "전체론",
            "term_en": "holism",
            "definition": (
                "도덕적 고려의 단위를 개별 구성원이 아니라 "
                "전체 체계(생태계·생명 공동체) 에 두는 입장. "
                "레오폴드 대지윤리의 철학적 기초이며, "
                "생태계 중심주의(ecocentrism) 와 결합되어 "
                "테일러 개체주의적 생명중심주의(biocentrism) 와 대립한다."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "related_terms": [
                "생태계 중심주의",
                "대지윤리",
                "생명 공동체",
            ],
        },
        {
            "id": "leopold-keyword-007",
            "term": "통합성·안정성·아름다움",
            "term_en": "",
            "definition": (
                "레오폴드 대지윤리 표어(land ethic maxim) 의 세 판단 축. "
                "통합성은 생명 공동체의 구조적 온전성, "
                "안정성은 변화 속에서의 지속 가능성, "
                "아름다움은 심미적 질을 가리킨다. "
                "어떤 것이 이 세 가치의 보전에 이바지하는 경향이 있다면 옳고, "
                "그렇지 않다면 그르다. "
                "2026-A Q12 을 제시문의 trademark 규범 표어."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "related_terms": [
                "통합성",
                "안정성",
                "아름다움",
                "대지윤리",
                "생명 공동체",
            ],
        },
        {
            "id": "leopold-keyword-008",
            "term": "대지",
            "term_en": "land",
            "definition": (
                "레오폴드 대지윤리의 핵심 개념. "
                "단순한 토양을 넘어 토양·물·식물·동물을 통합한 "
                "생명 공동체(biotic community) 로서의 생태적 전체. "
                "2026-A Q12 작성 방법 ㉡ 용어 기입 문항의 정답."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "leopold-work-001",
            "related_terms": [
                "대지윤리",
                "생명 공동체",
                "생태계 중심주의",
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
    """레오폴드 영향·비교 관계 데이터 입력.

    ES 등록 확인 (2026-04-22 curl 사전 확증):
     - taylor_p : found=true → contrasted (개체주의 vs 전체론)
     - singer   : found=true → contrasted (동물중심 vs 생태계중심)
     - naess    : found=false → skip
     - regan    : found=false → skip
    """
    relations = [
        {
            "from_thinker": THINKER_ID,
            "to_thinker": "taylor_p",
            "type": "contrasted",
            "description": (
                "레오폴드의 대지윤리(land ethic) 는 "
                "도덕적 고려의 1차 단위를 생명 공동체(biotic community) 전체에 두는 "
                "전체론(holism) · 생태계 중심주의(ecocentrism) 입장이다. "
                "반면 테일러(Paul W. Taylor) 의 개체주의적 생명중심주의(biocentrism) 는 "
                "개별 유기체 각각이 고유한 선(good of its own) 과 "
                "내재적 가치(inherent worth) 를 지닌다고 보고, "
                "각 유기체를 1차 단위로 삼는다. "
                "두 입장은 인간 중심주의를 거부한다는 점에서 일치하지만, "
                "도덕 단위(전체 vs 개체) 에서 대립한다. "
                "2026-A Q12 갑·을 대비 구도는 이 개체주의-전체론 대립의 직접 구현이며, "
                "작성 방법은 갑(테일러) 이 을(레오폴드) 을 "
                "생태계·유기체 개념으로 비판하도록 요구한다."
            ),
            "evidence": (
                "Leopold (1949) A Sand County Almanac 수록 「The Land Ethic」 "
                "— 생명 공동체의 통합성·안정성·아름다움 표어; "
                "Taylor (1986) Respect for Nature — 목적론적 삶의 중심·고유한 선·내재적 가치; "
                "2026-A Q12 을 '어떤 것이 생명 공동체의 통합성, 안정성, 아름다움의 보전에 "
                "이바지하는 경향이 있다면, 그것은 옳다' (coverage/2026-A.md L604 블록쿼트); "
                "2026-A Q12 갑 '유기체는 저마다의 고유한 선을 지니며 … 내재적 가치' "
                "(coverage/2026-A.md L603)."
            ),
        },
        {
            "from_thinker": THINKER_ID,
            "to_thinker": "singer",
            "type": "contrasted",
            "description": (
                "레오폴드의 대지윤리(land ethic) 는 "
                "토양·물·식물·동물을 포함하는 생명 공동체(biotic community) 전체를 "
                "도덕적 고려의 1차 단위로 삼는 "
                "전체론(holism) · 생태계 중심주의(ecocentrism) 입장이다. "
                "반면 싱어(Peter Singer) 의 동물중심주의는 "
                "쾌고감수능력(sentience) 을 도덕적 고려의 기준으로 삼아 "
                "의식·감각을 가진 개별 동물을 1차 단위로 한다. "
                "두 입장은 도덕적 고려의 기준(생명 공동체 전체 vs 개별 유정 존재) 과 "
                "고려 범위(토양·식물 포함 vs 유정 존재 한정) 에서 대립한다. "
                "레오폴드는 생태계 전체 보전을 위한 개체 조정을 찬성할 수 있는 반면, "
                "싱어는 개별 유정 존재의 이익 평등 고려를 요구한다."
            ),
            "evidence": (
                "Leopold (1949) A Sand County Almanac 수록 「The Land Ethic」; "
                "Singer (1975) Animal Liberation 쾌고감수능력 기반 이익 평등 고려; "
                "2026-A Q12 을 '생명 공동체의 통합성, 안정성, 아름다움의 보전' "
                "(coverage/2026-A.md L604 블록쿼트)."
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
    print("=== 알도 레오폴드(leopold) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (leopold)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n[OK] 알도 레오폴드 데이터 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}", file=sys.stderr)
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
