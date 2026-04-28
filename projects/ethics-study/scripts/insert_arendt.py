"""한나 아렌트(Hannah Arendt) 데이터를 ES에 직접 입력하는 스크립트.

field: civic_edu (민주시민교육 — 공적 영역·복수성·악의 평범성 등)
era:   20세기 서양
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import (
    INDEX_CLAIMS,
    INDEX_KEYWORDS,
    INDEX_RELATIONS,
    INDEX_THINKERS,
    INDEX_WORKS,
)
from src.es_client import close_client, get_client


# ---------------------------------------------------------------------------
# 1. thinker
# ---------------------------------------------------------------------------

def insert_thinker(client):
    """아렌트 사상가 데이터 입력."""
    doc = {
        "id": "arendt",
        "name": "한나 아렌트",
        "name_en": "Hannah Arendt",
        "field": "civic_edu",
        "era": "20세기 서양",
        "birth_year": 1906,
        "death_year": 1975,
        "background": (
            "한나 아렌트는 독일 하노버 근교에서 유대인 가정에서 태어나 "
            "마르부르크·프라이부르크·하이델베르크 대학교에서 마르틴 하이데거, "
            "에드문트 후설, 칼 야스퍼스에게 사사했다. "
            "1933년 나치 집권 후 프랑스로 망명해 유대인 난민 구호 활동을 했고, "
            "1941년 미국으로 다시 망명하여 뉴욕을 거점으로 학문 활동을 전개했다. "
            "The New School for Social Research, 프린스턴, 시카고 대학 등에서 가르쳤으며, "
            "전체주의·혁명·공적 영역·판단력 등 20세기 정치사상의 핵심 주제를 개척했다. "
            "'정치철학자'라는 호칭을 거부하고 스스로를 '정치이론가(political theorist)'라 불렀다."
        ),
        "core_philosophy": (
            "아렌트 사상의 핵심은 '정치적인 것(the political)'의 고유성을 회복하는 데 있다. "
            "그녀는 인간 활동을 노동(labor) · 작업(work) · 행위(action)로 삼분하고, "
            "이 가운데 행위만이 타자와 함께 말과 행동으로 새로움을 시작하는 "
            "진정한 의미의 정치적 활동이라고 보았다. "
            "행위는 '공적 영역(public realm)' 속에서, 서로 다른 인간들이 함께 존재한다는 "
            "'복수성(plurality)'의 조건과, 각자가 세상에 새로움을 가져올 수 있다는 "
            "'탄생성(natality)'의 조건 위에서 성립한다. "
            "전체주의는 바로 이 복수성·공적 영역·행위 역량을 파괴하는 체제이며, "
            "대규모 관료제·고독·무사유(thoughtlessness)는 "
            "아이히만에게서 드러난 '악의 평범성(banality of evil)'을 가능케 한다. "
            "따라서 권력(power)은 폭력(violence)과 구분되며, "
            "시민들이 함께 말하고 행위하는 곳에서만 권력이 태어난다."
        ),
        "philosophical_journey": (
            "초기(학위·망명, 1920~30년대): 하이데거·야스퍼스 아래서 아우구스티누스의 사랑 개념으로 박사학위를 받았고, "
            "유대인 문제와 전체주의의 징후를 망명 경험 속에서 체감했다. "
            "중기(전체주의 분석, 1950년대): 1951년 '전체주의의 기원'으로 반유대주의·제국주의·전체주의를 계보적으로 분석했다. "
            "1958년 '인간의 조건'에서 노동-작업-행위의 삼분법과 공적 영역 개념을 제시했다. "
            "후기(판단력·악의 평범성, 1960~70년대): 1963년 아이히만 재판 보고서 '예루살렘의 아이히만'에서 "
            "'악의 평범성' 테제를 제기하여 큰 논쟁을 일으켰다. "
            "1960년대 후반부터 칸트의 '판단력 비판'을 정치적 판단 이론으로 재해석하는 작업에 몰두했으며, "
            "유고집 '정신의 삶(The Life of the Mind)'에서 사유·의지·판단의 세 능력을 탐구했다."
        ),
        "keywords": [
            "활동적 삶",
            "관조적 삶",
            "노동",
            "작업",
            "행위",
            "공적 영역",
            "사적 영역",
            "복수성",
            "탄생성",
            "전체주의",
            "악의 평범성",
            "무사유",
            "판단력",
            "권력",
            "폭력",
            "시민적 자유"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="arendt", document=doc)
    print(f"[thinker] arendt: {result['result']}")
    return result


# ---------------------------------------------------------------------------
# 2. works
# ---------------------------------------------------------------------------

def insert_works(client):
    """아렌트 저서 데이터 입력."""
    works = [
        {
            "id": "arendt-origins-of-totalitarianism",
            "thinker_id": "arendt",
            "title": "전체주의의 기원",
            "title_original": "The Origins of Totalitarianism",
            "year": 1951,
            "significance": (
                "아렌트의 첫 대작으로, 반유대주의·제국주의·전체주의를 3부 구조로 계보적으로 분석했다. "
                "전체주의를 '새로운 종류의 정부 형태'로 규정하고, "
                "이데올로기와 테러, 계급사회의 해체와 대중사회의 등장, "
                "강제수용소를 통한 '인간의 불필요성(superfluousness)' 체험을 "
                "전체주의의 본질적 구성요소로 제시했다. "
                "20세기 정치 병리에 대한 고전적 진단서로 자리잡았다."
            ),
            "key_concepts": [
                "전체주의", "반유대주의", "제국주의", "이데올로기", "테러",
                "대중사회", "원자화", "강제수용소", "인간의 불필요성"
            ]
        },
        {
            "id": "arendt-human-condition",
            "thinker_id": "arendt",
            "title": "인간의 조건",
            "title_original": "The Human Condition",
            "year": 1958,
            "significance": (
                "아렌트 정치철학의 체계적 저작. '활동적 삶(vita activa)'을 노동·작업·행위로 삼분하고, "
                "각 활동이 대응하는 인간 조건(생명·세계성·복수성)을 규명했다. "
                "고대 그리스 폴리스의 공적 영역 경험에서 출발하여, "
                "근대 이후 노동의 영광화와 공적 영역의 쇠퇴가 가져온 귀결을 비판적으로 진단했다. "
                "탄생성(natality)을 정치와 교육의 핵심 범주로 도입한 저작이기도 하다."
            ),
            "key_concepts": [
                "활동적 삶(vita activa)", "노동(labor)", "작업(work)", "행위(action)",
                "공적 영역", "사적 영역", "사회적 영역", "복수성", "탄생성",
                "세계성(worldliness)"
            ]
        },
        {
            "id": "arendt-eichmann-in-jerusalem",
            "thinker_id": "arendt",
            "title": "예루살렘의 아이히만: 악의 평범성에 대한 보고서",
            "title_original": "Eichmann in Jerusalem: A Report on the Banality of Evil",
            "year": 1963,
            "significance": (
                "아이히만 재판을 직접 참관하고 작성한 보고서. "
                "아이히만이 '괴물'이 아니라 '평범한 관료'였음을 관찰하면서 "
                "'악의 평범성(banality of evil)'이라는 개념을 제기하여 큰 논쟁을 불러일으켰다. "
                "사유(thinking)의 부재, 상투어에 의존하는 언어, "
                "관료제적 복종이 대규모 악행을 가능하게 한다는 통찰을 제시했다. "
                "이후 '정신의 삶'에서 사유·의지·판단 탐구로 이어지는 사상의 전환점이 되었다."
            ),
            "key_concepts": [
                "악의 평범성", "무사유(thoughtlessness)", "상투어", "관료제적 악",
                "판단의 거부", "책임"
            ]
        },
        {
            "id": "arendt-on-revolution",
            "thinker_id": "arendt",
            "title": "혁명론",
            "title_original": "On Revolution",
            "year": 1963,
            "significance": (
                "미국 혁명과 프랑스 혁명을 비교 분석한 정치사상서. "
                "미국 혁명을 '자유의 구성'이라는 정치적 혁명으로, "
                "프랑스 혁명을 '사회적 문제(빈곤)'에 의해 변질된 혁명으로 대비시킨다. "
                "혁명의 본질을 '새로운 시작(new beginning)' — 곧 탄생성의 정치적 발현 — 으로 파악하며, "
                "평의회(council) 체제를 시민적 참여의 이상적 정치 형식으로 제시했다."
            ),
            "key_concepts": [
                "혁명", "자유의 구성", "새로운 시작", "사회적 문제", "평의회 체제",
                "공적 행복"
            ]
        },
        {
            "id": "arendt-on-violence",
            "thinker_id": "arendt",
            "title": "폭력론",
            "title_original": "On Violence",
            "year": 1970,
            "significance": (
                "1960년대 학생운동과 베트남 전쟁의 맥락에서 "
                "권력(power)과 폭력(violence)을 개념적으로 구분한 짧지만 영향력 있는 저작. "
                "권력은 사람들이 함께 행위할 때 생기는 집합적 능력이고, "
                "폭력은 도구적·수단적 강제력이다. "
                "폭력은 권력이 상실될 때 등장하며, 권력을 대체할 수 없다고 주장한다."
            ),
            "key_concepts": [
                "권력", "폭력", "강제력", "정당성", "수단-목적 합리성"
            ]
        },
        {
            "id": "arendt-life-of-the-mind",
            "thinker_id": "arendt",
            "title": "정신의 삶",
            "title_original": "The Life of the Mind",
            "year": 1978,
            "significance": (
                "아렌트의 유고 저작. '활동적 삶'에 대응하는 '관조적 삶(vita contemplativa)'을 "
                "사유(thinking)·의지(willing)·판단(judging) 세 능력으로 나누어 분석한다. "
                "판단(judging) 부분은 완성되지 못한 채 남았으며, "
                "칸트 '판단력 비판'의 반성적 판단 개념을 정치적 판단의 모델로 재해석하려는 시도가 담겨 있다."
            ),
            "key_concepts": [
                "관조적 삶", "사유", "의지", "판단", "반성적 판단",
                "대표적 사고(representative thinking)"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


# ---------------------------------------------------------------------------
# 3. claims
# ---------------------------------------------------------------------------

def insert_claims(client):
    """아렌트 핵심 주장 입력 (9개)."""
    claims = [
        # CLAIM-001: vita activa 삼분 — 노동·작업·행위
        {
            "id": "arendt-claim-001",
            "thinker_id": "arendt",
            "work_id": "arendt-human-condition",
            "source_detail": "The Human Condition, Ch. 1 §1, Ch. 3~5",
            "claim": (
                "인간의 활동적 삶(vita activa)은 노동(labor)·작업(work)·행위(action)의 세 가지로 나뉜다. "
                "노동은 생명 유지를 위한 순환적 활동, "
                "작업은 인간이 살아갈 '세계'를 만드는 제작 활동, "
                "행위는 타자와 함께 말과 행동으로 새로움을 시작하는 정치적 활동이다. "
                "이 삼분은 각각 '생명', '세계성', '복수성'이라는 인간 조건에 대응한다."
            ),
            "original_text": (
                "With the term vita activa, I propose to designate three fundamental human activities: "
                "labor, work, and action. They are fundamental because each corresponds to one of the "
                "basic conditions under which life on earth has been given to man."
            ),
            "original_text_ko": (
                "나는 '활동적 삶(vita activa)'이라는 용어로 세 가지 근본적 인간 활동 — "
                "노동, 작업, 행위 — 을 지칭하려 한다. 이 셋이 근본적인 이유는 "
                "각각이 지상에서 인간에게 주어진 삶의 기본 조건 하나씩에 대응하기 때문이다."
            ),
            "explanation": (
                "노동(labor): 동물로서 인간이 생명을 유지하기 위해 자연과 신진대사적으로 주고받는 순환 활동. "
                "그 산물은 소비되어 지속되지 않는다. "
                "작업(work): 호모 파베르(homo faber)가 도구를 사용해 지속적인 사물·건축물·예술품을 만들고, "
                "이로써 인간이 거주할 수 있는 '세계(world)'를 구축하는 활동. "
                "행위(action): 말(speech)과 행동을 통해 타자와 함께 새로움을 시작하는 활동. "
                "예측 불가능하고 환원 불가능하며, 바로 이 점에서 정치의 본래 영역을 이룬다."
            ),
            "argument": (
                "아렌트는 고대 그리스 폴리스 경험과 서양 정치사상사를 재독해하면서 "
                "근대 이후 이 삼분이 붕괴되어 왔음을 지적한다. "
                "마르크스 이후 노동이 최고의 인간 활동으로 격상되면서, "
                "작업이 만든 '세계'와 행위가 열어 놓는 '정치'가 모두 노동의 논리(생산성·필연성)에 흡수되었다. "
                "삼분을 회복해야만 각 활동의 고유한 의미와 정치의 자리가 복원된다."
            ),
            "counterpoint": (
                "마르크스주의자들은 노동을 하위 활동으로 분류하는 것이 "
                "노동계급의 해방적 의미를 축소한다고 비판한다. "
                "하버마스는 '작업/행위' 구분이 도구적 합리성과 의사소통적 합리성의 구분과 "
                "겹치면서도 완전히 일치하지 않는다고 지적한다."
            ),
            "context": (
                "전체주의 경험 이후 '정치란 무엇인가'를 되묻는 작업이 '인간의 조건'이며, "
                "노동·작업·행위의 삼분은 그 이론적 출발점이다."
            ),
            "keywords": ["활동적 삶", "노동", "작업", "행위", "인간 조건"],
            "verified": False
        },
        # CLAIM-002: 활동적 삶 vs 관조적 삶
        {
            "id": "arendt-claim-002",
            "thinker_id": "arendt",
            "work_id": "arendt-human-condition",
            "source_detail": "The Human Condition, Prologue; The Life of the Mind, Introduction",
            "claim": (
                "서양 사상은 플라톤 이래 관조적 삶(vita contemplativa)을 활동적 삶(vita activa) 위에 두어 왔다. "
                "그러나 아렌트는 관조가 활동을 판단하는 상위 기준이 되어서는 안 되며, "
                "활동적 삶 고유의 존엄과 의미 — 특히 행위의 정치적 의미 — 를 회복해야 한다고 주장한다. "
                "후기에는 관조적 삶을 사유·의지·판단의 '정신의 삶'으로 재정의한다."
            ),
            "original_text": (
                "The term vita activa is loaded and overloaded with tradition. "
                "It is as old as (but not older than) our tradition of political thought. "
                "And this tradition, far from comprehending and conceptualizing all the political "
                "experiences of Western mankind, grew out of a specific historical constellation."
            ),
            "original_text_ko": (
                "'활동적 삶'이라는 용어는 전통으로 인해 겹겹이 짐을 지고 있다. "
                "이 용어는 우리 정치사상 전통과 같은 연령을 가지며, "
                "이 전통은 서구 인류의 모든 정치 경험을 포괄·개념화하기는커녕 "
                "특정한 역사적 성좌에서 자라난 것이다."
            ),
            "explanation": (
                "플라톤은 이데아의 관조(theoria)를 정치적 삶보다 높이 평가했고, "
                "이 위계는 기독교 전통에서 vita contemplativa의 우위로 이어졌다. "
                "아렌트는 이 위계가 정치의 자율성과 행위의 의미를 체계적으로 평가절하했다고 본다. "
                "유고작 '정신의 삶'에서는 관조적 삶을 단일한 '진리 응시'가 아니라 "
                "사유·의지·판단이라는 세 능력의 활동으로 재구성함으로써, "
                "활동적 삶과 관조적 삶 사이의 위계를 해체한다."
            ),
            "argument": (
                "아렌트의 논증: (1) 플라톤 이래 관조 우위는 폴리스 쇠퇴 후 철학자의 "
                "'정치로부터의 후퇴'를 정당화하는 장치였다. "
                "(2) 이 위계 속에서 행위는 '불확실하고 낮은 것'으로 격하되었다. "
                "(3) 전체주의 경험은 오히려 '사유하지 않음(무사유)'이 악의 조건임을 보여 주었다 → "
                "사유와 행위 어느 한쪽의 우위가 아니라 양자의 관계를 재사고해야 한다."
            ),
            "counterpoint": (
                "플라톤-아리스토텔레스주의자와 일부 기독교 사상가들은 "
                "관조적 삶의 우위가 정치의 우연성을 보편적 선(善)에 정박시키는 데 필요하다고 반박한다. "
                "아렌트의 재해석이 '진리' 차원을 약화시킨다는 비판도 있다."
            ),
            "context": (
                "'인간의 조건' 서문에서 아렌트는 자신의 기획을 "
                "'근대가 망각해 온 vita activa의 의미를 다시 묻는 것'이라고 밝힌다."
            ),
            "keywords": ["활동적 삶", "관조적 삶", "정신의 삶", "플라톤 비판"],
            "verified": False
        },
        # CLAIM-003: 공적 영역과 사적 영역
        {
            "id": "arendt-claim-003",
            "thinker_id": "arendt",
            "work_id": "arendt-human-condition",
            "source_detail": "The Human Condition, Ch. 2 §§4~7",
            "claim": (
                "인간의 삶은 공적 영역(public realm)과 사적 영역(private realm)으로 구분된다. "
                "공적 영역은 서로 다른 복수의 인간들이 말과 행위로 출현하는 '나타남의 공간(space of appearance)'이며, "
                "사적 영역은 생명 유지와 친밀성을 위한 은폐의 영역이다. "
                "근대에 등장한 '사회적 영역(the social)'은 양자의 경계를 침식해 공적인 것의 고유성을 훼손한다."
            ),
            "original_text": (
                "The term 'public' signifies the world itself, in so far as it is common to all of us "
                "and distinguished from our privately owned place in it. "
                "To live together in the world means essentially that a world of things is between "
                "those who have it in common."
            ),
            "original_text_ko": (
                "'공적'이라는 말은 우리 모두에게 공통된, "
                "그리고 우리가 사적으로 소유한 자리와 구별되는 '세계' 자체를 의미한다. "
                "이 세계 안에서 함께 산다는 것은 본질적으로, "
                "공유된 사물들의 세계가 그것을 공통으로 갖는 사람들 사이에 자리한다는 뜻이다."
            ),
            "explanation": (
                "공적 영역의 두 가지 특성: "
                "(1) '나타남의 공간' — 서로 보고 들리는 속에서만 실재성이 확증된다. "
                "(2) '공통세계(common world)' — 세대를 가로질러 지속되는 제도·법·기억의 공간. "
                "사적 영역은 가정(오이코스)에 속하며 생명 유지·친밀성·은폐의 자리다. "
                "근대의 '사회적 영역'은 가정경제가 거대화되면서 등장한 행정·경제·관리의 공간으로, "
                "공적 영역의 행위적 성격과 사적 영역의 친밀성 모두를 잠식한다."
            ),
            "argument": (
                "아렌트는 공적 영역 없이는 개인의 행위가 '실재성'을 얻지 못한다고 논증한다. "
                "타자에게 나타나지 않는 행위는 '세계 속에 있음'의 지위를 갖지 못하기 때문이다. "
                "또한 공통세계가 사라지면 인간은 자기 시각에 갇혀 복수성을 상실한다. "
                "전체주의는 바로 이 공적 영역의 파괴를 통해 가능했다."
            ),
            "counterpoint": (
                "페미니즘 이론가(특히 한나 피트킨, 세일라 벤하비브)들은 "
                "'사회적 영역'에 대한 아렌트의 폄하가 노동·가사·돌봄 등 "
                "여성적·경제적 문제들을 정치의 바깥으로 밀어낸다고 비판한다. "
                "또한 공/사 구분이 젠더적 위계를 재생산할 위험이 있다고 지적한다."
            ),
            "context": (
                "고대 그리스 폴리스의 'oikos-polis' 구분이 이론적 준거가 되지만, "
                "아렌트는 이를 현대 대중사회 비판의 범주로 재전유한다."
            ),
            "keywords": ["공적 영역", "사적 영역", "사회적 영역", "나타남의 공간", "공통세계"],
            "verified": False
        },
        # CLAIM-004: 복수성(plurality)
        {
            "id": "arendt-claim-004",
            "thinker_id": "arendt",
            "work_id": "arendt-human-condition",
            "source_detail": "The Human Condition, Prologue; Ch. 1 §1; Ch. 5",
            "claim": (
                "행위와 정치의 근본 조건은 '복수성(plurality)'이다. "
                "복수성이란 '인간들(men, in the plural)이 지구에 살고 세계에 거주한다'는 사실, "
                "곧 평등성과 구별성이 동시에 성립하는 조건을 말한다. "
                "모두가 같지 않고(구별성), 그러나 서로를 이해할 수 있을 만큼 같다(평등성)."
            ),
            "original_text": (
                "Plurality is the condition of human action because we are all the same, that is, "
                "human, in such a way that nobody is ever the same as anyone else who ever lived, "
                "lives, or will live."
            ),
            "original_text_ko": (
                "복수성은 인간 행위의 조건이다. 우리 모두가 '인간'이라는 점에서 같지만, "
                "어느 누구도 일찍이 살았거나 지금 살고 있거나 앞으로 살 다른 누구와도 결코 같지 않다는 의미에서 그러하다."
            ),
            "explanation": (
                "복수성은 단순한 '다수성(multiplicity)'이 아니다. "
                "(1) 평등성(equality): 없으면 서로 이해·소통할 수 없고, "
                "(2) 구별성(distinction): 없으면 말과 행위로 자기를 드러낼 이유가 없다. "
                "두 계기가 동시에 성립해야만 정치가 가능하다. "
                "이 복수성은 '인간(man)'의 본성이 아니라 '인간들(men)'의 조건이며, "
                "따라서 정치 철학의 오랜 '인간 본질' 언어를 대체하는 아렌트적 범주이다."
            ),
            "argument": (
                "아렌트는 플라톤 이래의 정치철학이 '인간(man)'의 본질에서 정치를 연역했기 때문에 "
                "복수성을 놓쳤다고 주장한다. "
                "전체주의는 '한 사람(One Man)처럼 움직이는 인류'를 만들려는 시도로서 "
                "복수성의 파괴를 본질로 한다. "
                "따라서 복수성의 인정·보호가 자유와 정치의 전제조건이다."
            ),
            "counterpoint": (
                "보편주의 정치이론가들은 복수성 강조가 공통 규범의 근거를 약화시킨다고 비판한다. "
                "하버마스의 담론윤리는 복수성 위에 합의의 조건을 다시 세워야 한다고 본다."
            ),
            "context": (
                "복수성은 아렌트 정치사상 전체를 관통하는 중심 범주로, "
                "공적 영역·행위·권력·판단 개념의 토대가 된다."
            ),
            "keywords": ["복수성", "평등성", "구별성", "행위의 조건", "정치"],
            "verified": False
        },
        # CLAIM-005: 탄생성(natality)
        {
            "id": "arendt-claim-005",
            "thinker_id": "arendt",
            "work_id": "arendt-human-condition",
            "source_detail": "The Human Condition, Prologue; Ch. 5 §24",
            "claim": (
                "탄생성(natality)은 '새로운 인간이 세계에 태어남으로써 새로움을 시작할 수 있다'는 조건이며, "
                "하이데거의 '죽음을 향한 존재(being-toward-death)'와 달리 "
                "아렌트가 정치·교육의 중심 범주로 내세운 개념이다. "
                "행위는 탄생성의 정치적 실현이다."
            ),
            "original_text": (
                "The new beginning inherent in birth can make itself felt in the world only because "
                "the newcomer possesses the capacity of beginning something anew, that is, of acting."
            ),
            "original_text_ko": (
                "출생에 내재된 새로운 시작은, 새로 오는 자가 무엇인가를 새롭게 시작할 능력 — "
                "곧 행위할 능력 — 을 갖기 때문에 비로소 세계 안에서 자기를 느끼게 한다."
            ),
            "explanation": (
                "탄생성에는 세 층위가 있다: "
                "(1) 생물학적 출생(first birth) — 생명으로의 등장, "
                "(2) 세계로의 진입(second birth) — 말과 행위로 타자에게 자기를 드러내는 일, "
                "(3) 정치적 시작(beginning) — 기존 질서에 새로운 계기를 도입함. "
                "혁명·교육·행위는 모두 탄생성의 정치적 실현이다."
            ),
            "argument": (
                "아렌트의 논증: 인간은 죽는 존재이지만 '새로 태어나는 자'이기도 하다. "
                "이 출생의 사실이 '예측 불가능한 새로움'을 세계에 도입할 수 있는 근거가 된다. "
                "전체주의와 필연성의 이데올로기는 바로 이 '시작할 수 있음'을 부정하는데, "
                "탄생성을 긍정하는 정치만이 자유를 보존할 수 있다."
            ),
            "counterpoint": (
                "하이데거주의자들은 탄생성 개념이 '죽음을 향한 존재'의 실존적 진지함을 약화시킨다고 비판한다. "
                "탄생성이 행위의 '새로움'을 과장해 제도·전통의 안정성을 과소평가한다는 지적도 있다."
            ),
            "context": (
                "교육학자들(특히 거트 비에스타)은 탄생성을 민주시민교육의 이론적 기반으로 활용한다 — "
                "학생은 '새로 오는 자'로서 세계에 새로운 것을 가져올 존재다."
            ),
            "keywords": ["탄생성", "새로운 시작", "행위", "교육", "하이데거 비판"],
            "verified": False
        },
        # CLAIM-006: 전체주의의 본질
        {
            "id": "arendt-claim-006",
            "thinker_id": "arendt",
            "work_id": "arendt-origins-of-totalitarianism",
            "source_detail": "The Origins of Totalitarianism, Part 3, Ch. 12~13",
            "claim": (
                "전체주의는 단순한 독재가 아니라 '이데올로기(ideology)'와 '테러(terror)'의 결합으로 작동하는 "
                "새로운 종류의 정부 형태이다. "
                "그 본질은 법(law)의 자리에 운동(movement)의 필연성을 세우고, "
                "인간 복수성과 개성을 해체하여 '불필요한 존재(superfluous human beings)'로 만드는 데 있다."
            ),
            "original_text": (
                "Terror is the essence of totalitarian domination. "
                "Ideology and terror: these two phenomena are inextricable."
            ),
            "original_text_ko": (
                "테러는 전체주의적 지배의 본질이다. "
                "이데올로기와 테러 — 이 두 현상은 떼어낼 수 없이 결합되어 있다."
            ),
            "explanation": (
                "(1) 이데올로기: '자연의 법칙' 또는 '역사의 법칙'이라는 유사-법칙으로 "
                "모든 사건을 연역 가능하게 만들어, 경험과 복수성을 무시한다. "
                "(2) 테러: 법을 대체해 '운동'의 필연성이 스스로 관철되도록 하는 수단. "
                "(3) 강제수용소는 전체주의의 '실험실'로서, 인간을 "
                "자발성과 개성이 제거된 '꼭두각시' 또는 '불필요한 존재'로 만드는 장치였다. "
                "이는 나치즘(반유대주의·인종주의)과 스탈린주의(계급주의) 모두에서 공통적으로 나타난 구조이다."
            ),
            "argument": (
                "아렌트는 기존의 독재/폭정 개념으로는 전체주의를 설명할 수 없다고 주장한다. "
                "전통적 폭군은 자신의 권력을 위해 법을 어기지만, "
                "전체주의는 법을 초월한 '초법적 필연성'을 관철하려 한다. "
                "또한 기존 국가가 '적의 제거'에서 멈춘다면, 전체주의는 '객관적 적'을 끝없이 생산한다."
            ),
            "counterpoint": (
                "냉전기 전체주의론은 나치와 스탈린주의를 지나치게 동일시한다는 비판을 받았다. "
                "일부 역사가들은 아렌트의 분석이 이데올로기 요인을 과대평가하고 "
                "사회·경제적 조건을 과소평가한다고 지적한다."
            ),
            "context": (
                "1951년 초판 이후 스탈린 사후의 변화, 수정주의 역사학, "
                "냉전의 종결을 거치며 전체주의론은 여러 차례 재평가되어 왔다."
            ),
            "keywords": ["전체주의", "이데올로기", "테러", "강제수용소", "인간의 불필요성"],
            "verified": False
        },
        # CLAIM-007: 악의 평범성과 무사유
        {
            "id": "arendt-claim-007",
            "thinker_id": "arendt",
            "work_id": "arendt-eichmann-in-jerusalem",
            "source_detail": "Eichmann in Jerusalem, Postscript; The Life of the Mind, Introduction",
            "claim": (
                "홀로코스트의 실행자 아이히만에게서 드러난 악은 "
                "'뿌리 깊은 악마성'이 아니라 '평범성(banality)'이었다. "
                "이 악의 원인은 사악한 의도가 아니라 '사유하지 않음(thoughtlessness)' — "
                "타자의 관점에서 생각하는 능력의 결여 — 에 있다."
            ),
            "original_text": (
                "The trouble with Eichmann was precisely that so many were like him, "
                "and that the many were neither perverted nor sadistic, that they were, and still are, "
                "terribly and terrifyingly normal. "
                "... the lesson of the fearsome, word-and-thought-defying banality of evil."
            ),
            "original_text_ko": (
                "아이히만의 문제는 바로 그와 같은 사람이 너무 많다는 것, "
                "그리고 그들 다수가 비뚤어진 자나 사디스트가 아니라 "
                "끔찍하고 섬뜩할 정도로 '정상적'이었고 지금도 정상적이라는 데 있다. "
                "... 이것이 바로 말과 사유를 거부하는 저 무서운 '악의 평범성'의 교훈이다."
            ),
            "explanation": (
                "아렌트가 관찰한 아이히만의 특징: "
                "(1) 상투어(clichés)와 관료적 어법에 사로잡혀 자기 말을 갖지 못함, "
                "(2) 타인의 관점에서 사태를 보는 상상력의 부재, "
                "(3) 도덕적 선악이 아니라 '출세와 의무 수행'의 문법 속에서만 사고함. "
                "이 결함은 '어리석음'과 다르며 — 아이히만은 지능적으로 부족하지 않았다 — "
                "오히려 '사유하기'라는 정신 활동의 부재 자체이다. "
                "'정신의 삶' 서문에서 아렌트는 이 관찰을 사유·의지·판단 분석의 출발점으로 삼는다."
            ),
            "argument": (
                "근거: (1) 재판 기록에서 아이히만은 자신의 행위를 '법과 의무'의 언어로만 설명하고 "
                "피해자들의 경험을 상상할 수 없었다. "
                "(2) 그의 도덕적 혼란은 나치 법 체계 안에서 '정상성'이 얼마나 "
                "규범적 사유를 대체했는지 보여 준다. "
                "(3) 따라서 20세기적 악은 '야수적 의지'보다 '무사유의 관료성'으로 이해되어야 한다."
            ),
            "counterpoint": (
                "역사가 데이비드 세자라니·베티나 스탕네트 등은 이후 연구에서 "
                "아이히만이 단순한 '서류 처리자'가 아니라 확고한 반유대주의 이데올로그였음을 논증하며 "
                "아렌트의 인물상이 부정확하다고 비판한다. "
                "또한 '평범성' 테제가 가해자의 책임을 경감시킨다는 오독도 제기되었다 — "
                "아렌트 자신은 이를 반박한다."
            ),
            "context": (
                "1961년 예루살렘에서 열린 아돌프 아이히만 재판을 The New Yorker에 연재한 보고서가 "
                "1963년 단행본 '예루살렘의 아이히만'으로 출간되었다."
            ),
            "keywords": ["악의 평범성", "무사유", "아이히만", "관료제적 악", "사유"],
            "verified": False
        },
        # CLAIM-008: 권력 ≠ 폭력
        {
            "id": "arendt-claim-008",
            "thinker_id": "arendt",
            "work_id": "arendt-on-violence",
            "source_detail": "On Violence, §§II~III",
            "claim": (
                "권력(power)과 폭력(violence)은 개념적으로 구분된다. "
                "권력은 사람들이 '함께 행위할 때(acting in concert)' 생겨나는 집합적 능력이고, "
                "폭력은 도구(총·제도)에 의존하는 강제력이다. "
                "권력이 상실될 때 폭력이 나타나며, 폭력은 권력을 파괴할 수는 있어도 생산할 수는 없다."
            ),
            "original_text": (
                "Power corresponds to the human ability not just to act but to act in concert. "
                "Power is never the property of an individual; it belongs to a group "
                "and remains in existence only so long as the group keeps together."
            ),
            "original_text_ko": (
                "권력은 단순히 행위하는 능력이 아니라 '함께 행위하는' 능력에 대응한다. "
                "권력은 결코 개인의 소유가 아니며 집단에 속하고, "
                "집단이 뭉쳐 있는 동안만 존재한다."
            ),
            "explanation": (
                "(1) 권력(power): 사람들이 말과 행위로 함께함 속에서 생성되는 '집합적 역량'. "
                "개인의 소유가 아니고, 도구로 환원되지 않으며, 집단이 흩어지면 소멸한다. "
                "(2) 힘(strength)·무력(force)·권위(authority)·폭력(violence): 각기 다른 현상. "
                "폭력은 특히 도구적이고 수단-목적 합리성에 종속된다. "
                "(3) 둘의 관계: 권력은 정당성을 필요로 하고, 폭력은 정당화(justification)를 필요로 한다. "
                "권력이 붕괴할수록 폭력이 등장하는 것은 권력의 '결여'를 메우기 위해서다."
            ),
            "argument": (
                "근거: (1) 역사적 사례 — 간디·미국 민권운동은 폭력 없이 권력을 생성했다. "
                "(2) 전체주의·독재에서 폭력의 극대화는 오히려 정당성의 붕괴를 반영한다. "
                "(3) 베트남 전쟁·68혁명의 맥락에서 '폭력=권력'이라는 통념(사르트르, 마오)을 반박."
            ),
            "counterpoint": (
                "막스 베버의 권력 정의('자기 의지를 관철할 확률')나 마르크스주의 전통은 "
                "권력/폭력의 개념적 구별이 너무 규범적이고 경험적 강제력을 설명하지 못한다고 비판한다. "
                "미셸 푸코의 규율권력 분석은 권력이 훨씬 편재적·미시적임을 보여 준다."
            ),
            "context": (
                "1970년 출간된 '폭력론'은 학생운동과 반전운동의 폭력 논쟁에 대한 개입이다."
            ),
            "keywords": ["권력", "폭력", "함께 행위하기", "정당성", "도구성"],
            "verified": False
        },
        # CLAIM-009: 판단력 — 정치적 판단의 모델
        {
            "id": "arendt-claim-009",
            "thinker_id": "arendt",
            "work_id": "arendt-life-of-the-mind",
            "source_detail": "The Life of the Mind, Vol. 1 Thinking, Introduction; Lectures on Kant's Political Philosophy",
            "claim": (
                "정치적 판단(political judgment)의 모델은 칸트 '판단력 비판'의 반성적 판단, "
                "특히 미적 판단에서 찾아야 한다. "
                "판단은 보편 규칙의 기계적 적용(규정적 판단)이 아니라, "
                "특수한 것에서 출발해 타자의 입장을 고려하는 '대표적 사고(representative thinking)'로서의 "
                "반성적 판단이다."
            ),
            "original_text": (
                "I form an opinion by considering a given issue from different viewpoints, "
                "by making present to my mind the standpoints of those who are absent; "
                "that is, I represent them. This process of representation does not blindly adopt "
                "the actual views of those who stand somewhere else... "
                "The more people's standpoints I have present in my mind while I am pondering a given issue, "
                "and the better I can imagine how I would feel and think if I were in their place, "
                "the stronger will be my capacity for representative thinking and the more valid my final conclusions, my opinion."
            ),
            "original_text_ko": (
                "나는 어떤 사안을 서로 다른 관점에서 고찰하고, "
                "자리에 없는 사람들의 입장을 내 마음속에 현전시킴으로써 의견을 형성한다 — "
                "곧 나는 그들을 '대표(represent)'한다. "
                "이 대표의 과정은 다른 자리에 서 있는 사람들의 실제 견해를 맹목적으로 받아들이는 것이 아니다. "
                "어떤 사안을 숙고할 때 내 마음에 더 많은 사람들의 관점을 현전시킬 수 있을수록, "
                "그리고 그들의 자리에 있을 때 내가 어떻게 느끼고 사유할지를 더 잘 상상할 수 있을수록, "
                "내 '대표적 사고'의 역량은 더 강해지고 내 최종 결론, 곧 의견은 더 타당해진다."
            ),
            "explanation": (
                "아렌트는 칸트 제3비판서에서 두 자원을 끌어온다: "
                "(1) 공통감(sensus communis) — 타인과 소통 가능한 '공동체 감각', "
                "(2) 확장된 심성(enlarged mentality) — 타자의 입장을 상상으로 대표하는 능력. "
                "정치적 판단은 '이 특수한 사건을 어떻게 볼 것인가'라는 반성적 판단이며, "
                "따라서 단순한 선호도 보편 원리의 연역도 아니다. "
                "이 관점은 사유(thinking) 능력과 결합되어 '무사유'에 대한 저항 능력을 이룬다."
            ),
            "argument": (
                "근거: (1) 도덕 규칙의 기계적 적용은 아이히만적 관료성에서 도덕적 재난을 낳았다. "
                "(2) 정치적 행위는 언제나 '이 특수한 상황'과 관련되며, "
                "규정적 판단으로는 새로움·복수성을 포착할 수 없다. "
                "(3) 칸트 미학의 '보편적 동의의 요구' 구조는 "
                "사적 선호를 넘어 공적 타당성을 확보하는 정치적 판단의 모델이 된다."
            ),
            "counterpoint": (
                "하버마스는 아렌트의 판단 개념이 결국 '담론적 정당화' 없이 타당성을 확보할 수 없다고 본다. "
                "리오타르 등은 역으로 아렌트가 여전히 칸트적 보편주의에 의존한다고 비판한다. "
                "또한 판단 저술이 미완으로 남았기 때문에 해석의 여지가 크다."
            ),
            "context": (
                "1970년대 '칸트 정치철학 강의'에서 본격 전개된 후, '정신의 삶' 3부 'Judging'으로 기획되었으나 "
                "아렌트의 급작스런 사망(1975)으로 미완 유고로 남았다."
            ),
            "keywords": ["판단력", "반성적 판단", "대표적 사고", "공통감", "확장된 심성"],
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


# ---------------------------------------------------------------------------
# 4. keywords
# ---------------------------------------------------------------------------

def insert_keywords(client):
    """아렌트 키워드 사전 입력."""
    keywords = [
        {
            "id": "arendt-kw-vita-activa",
            "term": "활동적 삶",
            "term_en": "vita activa",
            "definition": (
                "인간의 활동을 노동·작업·행위로 삼분하는 아렌트의 상위 범주. "
                "전통적으로 관조적 삶(vita contemplativa)에 종속되어 왔으나, "
                "아렌트는 그 고유한 의미 — 특히 행위의 정치적 의미 — 를 복원하고자 한다."
            ),
            "thinker_id": "arendt",
            "work_id": "arendt-human-condition",
            "related_terms": ["노동", "작업", "행위", "관조적 삶"]
        },
        {
            "id": "arendt-kw-labor",
            "term": "노동",
            "term_en": "labor",
            "definition": (
                "생명 유지를 위해 자연과 신진대사적으로 이루어지는 순환 활동. "
                "그 산물은 소비되어 지속되지 않으며, 인간 조건 '생명(life)'에 대응한다."
            ),
            "thinker_id": "arendt",
            "work_id": "arendt-human-condition",
            "related_terms": ["작업", "행위", "소비", "생명"]
        },
        {
            "id": "arendt-kw-work",
            "term": "작업",
            "term_en": "work",
            "definition": (
                "호모 파베르가 도구를 사용해 지속적인 사물·제도·예술품을 제작하는 활동. "
                "인간이 거주하는 '세계(world)'를 구축하며, 인간 조건 '세계성'에 대응한다."
            ),
            "thinker_id": "arendt",
            "work_id": "arendt-human-condition",
            "related_terms": ["노동", "행위", "세계", "호모 파베르"]
        },
        {
            "id": "arendt-kw-action",
            "term": "행위",
            "term_en": "action",
            "definition": (
                "말과 행동을 통해 타자와 함께 새로움을 시작하는 활동. "
                "복수성·탄생성의 조건 위에서 성립하며, 정치의 본래 영역을 이룬다. "
                "예측 불가능하고 되돌릴 수 없다는 특성을 갖는다."
            ),
            "thinker_id": "arendt",
            "work_id": "arendt-human-condition",
            "related_terms": ["복수성", "탄생성", "공적 영역", "권력"]
        },
        {
            "id": "arendt-kw-public-realm",
            "term": "공적 영역",
            "term_en": "public realm",
            "definition": (
                "복수의 인간들이 서로 보고 들리는 '나타남의 공간'이자, "
                "세대를 가로질러 지속되는 '공통세계'. "
                "행위와 말이 실재성을 얻는 정치의 자리."
            ),
            "thinker_id": "arendt",
            "work_id": "arendt-human-condition",
            "related_terms": ["사적 영역", "사회적 영역", "행위", "공통세계"]
        },
        {
            "id": "arendt-kw-private-realm",
            "term": "사적 영역",
            "term_en": "private realm",
            "definition": (
                "가정(오이코스)에 속하는 생명 유지·친밀성·은폐의 영역. "
                "공적 영역과 구분되지만, 양자 모두 인간 실존에 필수적이다."
            ),
            "thinker_id": "arendt",
            "work_id": "arendt-human-condition",
            "related_terms": ["공적 영역", "사회적 영역", "친밀성"]
        },
        {
            "id": "arendt-kw-plurality",
            "term": "복수성",
            "term_en": "plurality",
            "definition": (
                "'인간들'이 지구에 함께 살고 세계에 거주한다는 사실로서, "
                "평등성과 구별성이 동시에 성립하는 조건. "
                "행위와 정치의 근본 조건이다."
            ),
            "thinker_id": "arendt",
            "work_id": "arendt-human-condition",
            "related_terms": ["행위", "공적 영역", "평등성", "구별성"]
        },
        {
            "id": "arendt-kw-natality",
            "term": "탄생성",
            "term_en": "natality",
            "definition": (
                "'새로운 인간이 태어남으로써 새로움을 시작할 수 있다'는 조건. "
                "하이데거의 '죽음을 향한 존재'에 대응되는 아렌트의 대안 범주이며, "
                "행위·혁명·교육의 가능 근거가 된다."
            ),
            "thinker_id": "arendt",
            "work_id": "arendt-human-condition",
            "related_terms": ["행위", "새로운 시작", "교육", "혁명"]
        },
        {
            "id": "arendt-kw-totalitarianism",
            "term": "전체주의",
            "term_en": "totalitarianism",
            "definition": (
                "이데올로기와 테러의 결합으로 작동하는 새로운 정부 형태. "
                "법의 자리에 '운동의 필연성'을 세우고 인간 복수성을 해체한다. "
                "강제수용소에서 인간을 '불필요한 존재'로 만드는 실험이 이루어진다."
            ),
            "thinker_id": "arendt",
            "work_id": "arendt-origins-of-totalitarianism",
            "related_terms": ["이데올로기", "테러", "강제수용소", "대중사회"]
        },
        {
            "id": "arendt-kw-banality-of-evil",
            "term": "악의 평범성",
            "term_en": "banality of evil",
            "definition": (
                "아이히만 재판 관찰에서 도출된 개념. "
                "대규모 악이 악마적 의도가 아니라 '사유하지 않음(무사유)' — "
                "타자의 관점에서 사고하지 못하는 관료적 평범성 — 에서 비롯됨을 가리킨다."
            ),
            "thinker_id": "arendt",
            "work_id": "arendt-eichmann-in-jerusalem",
            "related_terms": ["무사유", "아이히만", "관료제적 악", "사유"]
        },
        {
            "id": "arendt-kw-thoughtlessness",
            "term": "무사유",
            "term_en": "thoughtlessness",
            "definition": (
                "상투어에 갇혀 자기 말을 갖지 못하고, 타인의 관점에서 사태를 볼 수 없는 상태. "
                "아렌트가 악의 평범성의 핵심 원인으로 지목한 정신 활동의 부재."
            ),
            "thinker_id": "arendt",
            "work_id": "arendt-life-of-the-mind",
            "related_terms": ["악의 평범성", "사유", "판단력"]
        },
        {
            "id": "arendt-kw-judgment",
            "term": "판단력",
            "term_en": "judgment",
            "definition": (
                "보편 규칙을 기계적으로 적용하는 대신, 특수한 것에서 출발해 "
                "타자의 입장을 상상으로 대표하는 반성적 능력. "
                "칸트 '판단력 비판'의 미적 판단 모델을 아렌트가 정치적 판단으로 재해석한 것."
            ),
            "thinker_id": "arendt",
            "work_id": "arendt-life-of-the-mind",
            "related_terms": ["대표적 사고", "공통감", "확장된 심성", "무사유"]
        },
        {
            "id": "arendt-kw-power-violence",
            "term": "권력/폭력 구분",
            "term_en": "power vs. violence",
            "definition": (
                "권력은 사람들이 '함께 행위함'에서 생성되는 집합적 능력이고, "
                "폭력은 도구에 의존하는 강제력이다. "
                "폭력은 권력을 파괴할 수 있으나 생산할 수 없으며, "
                "권력이 쇠퇴할 때 폭력이 등장한다."
            ),
            "thinker_id": "arendt",
            "work_id": "arendt-on-violence",
            "related_terms": ["권력", "폭력", "정당성", "함께 행위하기"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


# ---------------------------------------------------------------------------
# 5. relations
# ---------------------------------------------------------------------------

def insert_relations(client):
    """아렌트 관련 사상 관계 데이터 입력."""
    relations = [
        {
            "from_thinker": "heidegger",
            "to_thinker": "arendt",
            "type": "influenced",
            "description": (
                "마르부르크에서 하이데거에게 사사한 아렌트는 "
                "현상학적 방법·실존분석·세계 개념에서 깊은 영향을 받았다. "
                "다만 아렌트는 하이데거의 '죽음을 향한 존재'에 맞서 '탄생성'을 내세우며, "
                "하이데거의 나치 가담과 정치적 무책임을 비판했다."
            ),
            "evidence": "The Human Condition (1958); 'Martin Heidegger at Eighty' (1971)"
        },
        {
            "from_thinker": "jaspers",
            "to_thinker": "arendt",
            "type": "influenced",
            "description": (
                "칼 야스퍼스는 아렌트의 박사논문 지도교수이자 평생의 스승·친구였다. "
                "'소통'·'한계상황'·'공동체적 이성' 개념이 아렌트의 공적 영역·복수성 사유에 영향을 주었으며, "
                "야스퍼스의 '죄의 문제(Die Schuldfrage)'는 아렌트 책임론의 준거 중 하나이다."
            ),
            "evidence": "Arendt-Jaspers Correspondence; The Origins of Totalitarianism dedication"
        },
        {
            "from_thinker": "aristotle",
            "to_thinker": "arendt",
            "type": "influenced",
            "description": (
                "아리스토텔레스의 '폴리스', '프락시스(praxis)/포이에시스(poiesis)' 구분, "
                "인간은 '정치적 동물(zōon politikon)'이라는 규정은 "
                "아렌트의 행위·공적 영역 이론의 고전적 준거이다."
            ),
            "evidence": "The Human Condition Ch. 2 §4"
        },
        {
            "from_thinker": "kant",
            "to_thinker": "arendt",
            "type": "influenced",
            "description": (
                "칸트 '판단력 비판'의 반성적 판단·공통감·확장된 심성 개념이 "
                "아렌트의 정치적 판단 이론의 직접적 기반이 되었다. "
                "아렌트는 '칸트 정치철학 강의'에서 칸트 미학을 정치철학의 미완 저작으로 재해석한다."
            ),
            "evidence": "Lectures on Kant's Political Philosophy (1982 유고); The Life of the Mind"
        },
        {
            "from_thinker": "arendt",
            "to_thinker": "habermas",
            "type": "influenced",
            "description": (
                "아렌트의 '함께 행위함'으로서의 권력 개념과 공적 영역 이론은 "
                "하버마스의 '공론장(Öffentlichkeit)'과 '의사소통권력' 개념 형성에 결정적 영향을 미쳤다."
            ),
            "evidence": "Habermas, 'Hannah Arendt's Communications Concept of Power' (1977)"
        },
        {
            "from_thinker": "arendt",
            "to_thinker": "benhabib",
            "type": "influenced",
            "description": (
                "세일라 벤하비브는 아렌트의 공/사 구분·판단 개념을 "
                "페미니즘과 담론윤리의 관점에서 비판적으로 계승·확장했다."
            ),
            "evidence": "Benhabib, The Reluctant Modernism of Hannah Arendt (1996)"
        },
        {
            "from_thinker": "arendt",
            "to_thinker": "agamben",
            "type": "influenced",
            "description": (
                "조르조 아감벤의 '벌거벗은 생명(bare life)'과 '예외상태' 이론은 "
                "아렌트의 전체주의 분석·강제수용소 논의·'인간 권리의 몰락' 장에서 "
                "직접적 영감을 받았다."
            ),
            "evidence": "Agamben, Homo Sacer (1995)"
        },
        {
            "from_thinker": "arendt",
            "to_thinker": "biesta",
            "type": "influenced",
            "description": (
                "교육학자 거트 비에스타는 아렌트의 '탄생성'·'공적 영역' 개념을 "
                "민주시민교육과 '주체화(subjectification)' 이론의 기초로 삼는다. "
                "학습자는 '새로 오는 자'로서 세계에 새로움을 가져올 수 있는 존재로 재정의된다."
            ),
            "evidence": "Biesta, The Beautiful Risk of Education (2014)"
        }
    ]

    for i, rel in enumerate(relations):
        rel_id = f"arendt-rel-{i+1:03d}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id} ({rel['from_thinker']} → {rel['to_thinker']}): {result['result']}")

    return len(relations)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def verify(client):
    """간단한 확인 쿼리."""
    client.indices.refresh(
        index=[INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS, INDEX_KEYWORDS, INDEX_RELATIONS]
    )

    thinker = client.get(index=INDEX_THINKERS, id="arendt")["_source"]
    print(f"[verify/thinker] id={thinker['id']}, name={thinker['name']}, "
          f"field={thinker['field']}, era={thinker['era']}")

    n_works = client.count(
        index=INDEX_WORKS,
        query={"term": {"thinker_id": "arendt"}}
    )["count"]
    n_claims = client.count(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "arendt"}}
    )["count"]
    n_kws = client.count(
        index=INDEX_KEYWORDS,
        query={"term": {"thinker_id": "arendt"}}
    )["count"]
    n_rels_from = client.count(
        index=INDEX_RELATIONS,
        query={"term": {"from_thinker": "arendt"}}
    )["count"]
    n_rels_to = client.count(
        index=INDEX_RELATIONS,
        query={"term": {"to_thinker": "arendt"}}
    )["count"]

    print(f"[verify/counts] works={n_works}, claims={n_claims}, "
          f"keywords={n_kws}, relations(from=arendt)={n_rels_from}, relations(to=arendt)={n_rels_to}")


def main():
    client = get_client()
    try:
        print("=== 한나 아렌트(Hannah Arendt) 데이터 입력 시작 ===\n")

        print("--- 사상가(thinker) 입력 ---")
        insert_thinker(client)
        print()

        print("--- 저서(works) 입력 ---")
        n_works = insert_works(client)
        print(f"총 {n_works}개 저서 입력 완료\n")

        print("--- 주장(claims) 입력 ---")
        n_claims = insert_claims(client)
        print(f"총 {n_claims}개 주장 입력 완료\n")

        print("--- 키워드(keywords) 입력 ---")
        n_keywords = insert_keywords(client)
        print(f"총 {n_keywords}개 키워드 입력 완료\n")

        print("--- 관계(relations) 입력 ---")
        n_relations = insert_relations(client)
        print(f"총 {n_relations}개 관계 입력 완료\n")

        print("--- 검증 ---")
        verify(client)
        print()

        print("=== 아렌트 데이터 입력 완료 ===")
        print(
            f"요약: 사상가 1명, 저서 {n_works}개, 주장 {n_claims}개, "
            f"키워드 {n_keywords}개, 관계 {n_relations}개"
        )

    finally:
        close_client(client)


if __name__ == "__main__":
    main()
