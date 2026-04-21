"""존 듀이(John Dewey) 데이터를 ES에 직접 입력하는 스크립트.

field: civic_edu (민주시민교육)
era: 근현대 서양
규모: 표준 (claims 8~10)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS, INDEX_FIELDS
)


def ensure_field(client):
    """civic_edu 분야 존재 확인 (Phase 5 사전 생성)."""
    try:
        client.get(index=INDEX_FIELDS, id="civic_edu")
        print("[field] civic_edu: 이미 존재")
    except Exception:
        doc = {
            "id": "civic_edu",
            "name": "민주시민교육",
            "description": "민주주의와 교육·공적 영역 등 시민성 형성 담론",
            "order": 7
        }
        client.index(index=INDEX_FIELDS, id="civic_edu", document=doc)
        print("[field] civic_edu: created")


def insert_thinker(client):
    """듀이 사상가 데이터 입력."""
    doc = {
        "id": "dewey",
        "name": "존 듀이",
        "name_en": "John Dewey",
        "field": "civic_edu",
        "era": "근현대 서양",
        "birth_year": 1859,
        "death_year": 1952,
        "background": (
            "미국 버몬트주 벌링턴에서 태어난 듀이는 버몬트 대학교에서 철학을 공부한 뒤 "
            "존스홉킨스 대학교에서 헤겔 관념론과 새로 태동하던 실험심리학을 접하고 박사학위를 받았다(1884). "
            "미시간 대학교, 시카고 대학교를 거쳐 컬럼비아 대학교에서 오랫동안 재직했으며(1904~1930), "
            "시카고 시절에는 부속 실험학교(Laboratory School)를 설립하여 자신의 교육 이론을 실제로 검증했다. "
            "제임스(William James), 퍼스(C. S. Peirce)와 함께 미국 프래그머티즘(pragmatism)을 대표하는 사상가이며, "
            "그의 사유는 철학·교육·심리·정치·미학에 걸쳐 광범위하게 전개되었다. "
            "20세기 전반 미국의 진보주의 교육 운동과 민주주의 담론에 결정적 영향을 미쳤으며, "
            "사회 개혁 활동(NAACP 공동 설립, 뉴욕 교사조합 지원, 트로츠키 재판 위원회 위원장 등)에도 적극 참여했다. "
            "한국에서는 '민주시민교육'과 '도덕과 교육' 영역에서 경험 중심·탐구 중심 교육철학의 근거로 빈번히 인용된다."
        ),
        "core_philosophy": (
            "듀이 사상의 핵심은 '경험(experience)'과 '탐구(inquiry)'를 통해 민주주의와 교육이 상호 구성된다는 관점이다. "
            "그에게 경험은 유기체와 환경의 능동적 상호작용이며, 지식은 이 경험 속에서 문제를 해결하기 위한 "
            "도구(instrument)로 구성된다. 따라서 진리는 고정된 대상이 아니라 탐구 공동체의 검증 가능한 '보증된 주장 가능성(warranted assertibility)'이다. "
            "교육은 단순한 지식 전달이 아니라 경험의 재구성(reconstruction of experience)이며, "
            "학습자가 반성적 사고(reflective thinking)를 통해 문제를 해결하면서 성장(growth)하는 과정이다. "
            "민주주의는 정치 제도가 아니라 '함께 살아가는 방식(associated living)'이며, "
            "교육은 민주주의를 실현하는 가장 핵심적인 공적 과정이다. "
            "따라서 학교는 민주적 공동체의 축소판이어야 하고, 학습자의 능동적 참여와 협동이 보장되어야 한다."
        ),
        "philosophical_journey": (
            "초기(1880~1890년대): 헤겔 관념론의 영향 아래 정신과 자연의 통일을 모색했다. "
            "이후 제임스의 기능주의 심리학과 다윈의 진화론을 수용하면서 관념론에서 프래그머티즘으로 전환했다. "
            "시카고 시기(1894~1904): 시카고 대학 실험학교를 운영하며 '나의 교육 신조(My Pedagogic Creed, 1897)', "
            "'학교와 사회(The School and Society, 1899)', '아동과 교육과정(The Child and the Curriculum, 1902)'을 저술하여 "
            "아동 중심·경험 중심 교육론을 체계화했다. "
            "컬럼비아 시기(1904~1930): '민주주의와 교육(Democracy and Education, 1916)'으로 교육철학의 고전을 남겼고, "
            "'인간 본성과 행위(1922)', '경험과 자연(1925)', '확실성의 탐구(1929)' 등으로 프래그머티즘을 철학 전반에 확장했다. "
            "후기(1930~1952): '공공성과 그 문제들(The Public and Its Problems, 1927)', '자유주의와 사회적 행동(1935)', "
            "'경험과 교육(Experience and Education, 1938)', '탐구의 논리(Logic: The Theory of Inquiry, 1938)'를 통해 "
            "참여적 민주주의와 탐구 논리를 정교화했다. "
            "피아제·비고츠키의 구성주의, 프레이리의 비판교육학, 하버마스의 담론윤리, 롤스의 공적 이성 개념 등에 "
            "직·간접적 영향을 미쳤다."
        ),
        "keywords": [
            "경험",
            "탐구",
            "반성적 사고",
            "성장으로서의 교육",
            "경험의 연속성",
            "상호작용",
            "민주주의",
            "참여적 민주주의",
            "도구주의",
            "프래그머티즘",
            "경험의 재구성",
            "함께 살아가는 방식",
            "공공성",
            "문제 해결 학습"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="dewey", document=doc)
    print(f"[thinker] dewey: {result['result']}")
    return result


def insert_works(client):
    """듀이 저서 데이터 입력."""
    works = [
        {
            "id": "dewey-democracy-and-education",
            "thinker_id": "dewey",
            "title": "민주주의와 교육",
            "title_original": "Democracy and Education: An Introduction to the Philosophy of Education",
            "year": 1916,
            "significance": (
                "듀이 교육철학을 집대성한 대표작이자 20세기 교육철학의 고전. "
                "교육을 '경험의 재구성을 통한 성장'으로 규정하고, "
                "민주주의를 '공동 경험을 공유하는 연합적 삶의 방식(mode of associated living)'으로 정의했다. "
                "교육은 민주주의의 실현 조건이며 동시에 민주주의는 교육의 이상적 환경임을 체계적으로 논증했다. "
                "'교육은 삶을 위한 준비가 아니라 삶 그 자체'라는 명제와 함께 "
                "경험 중심 교육과정, 반성적 사고, 직업과 교양의 통합 등 현대 교육학의 핵심 주제를 선도했다. "
                "한국 도덕과·사회과 민주시민교육 담론의 고전적 근거로 빈번히 인용된다."
            ),
            "key_concepts": [
                "성장으로서의 교육", "경험의 재구성", "연합적 삶의 방식",
                "민주주의", "직업교육과 교양교육의 통합", "교육의 사회적 기능"
            ]
        },
        {
            "id": "dewey-experience-and-education",
            "thinker_id": "dewey",
            "title": "경험과 교육",
            "title_original": "Experience and Education",
            "year": 1938,
            "significance": (
                "진보주의 교육 운동 내부의 왜곡(아동 방임, 전통 교과 전면 부정)을 비판하며 "
                "듀이 자신이 자신의 교육철학을 재정리한 후기 저작. "
                "'경험의 연속성(continuity of experience)'과 '상호작용(interaction)'을 "
                "교육적 경험의 두 준거로 제시하여 아무 경험이나 교육적인 것은 아니라는 점을 분명히 했다. "
                "교사의 역할을 '경험 설계자이자 민주적 공동체의 안내자'로 재정의하고, "
                "전통교육과 진보교육의 이분법을 넘어서는 경험 중심 교육의 원리를 제시했다."
            ),
            "key_concepts": [
                "경험의 연속성", "상호작용", "교육적 경험",
                "진보주의 교육의 자기비판", "교사의 안내자 역할"
            ]
        },
        {
            "id": "dewey-how-we-think",
            "thinker_id": "dewey",
            "title": "사고하는 방법",
            "title_original": "How We Think",
            "year": 1910,
            "significance": (
                "반성적 사고(reflective thinking)의 개념과 단계를 체계화한 저작. "
                "1933년 개정판에서 반성적 사고의 5단계 — (1) 문제의 인식, (2) 문제의 명료화, "
                "(3) 가설의 설정, (4) 추론을 통한 검토, (5) 행위에 의한 검증 — 을 제시했다. "
                "이 모델은 이후 '문제 해결 학습(problem-solving method)'의 이론적 기초가 되었으며, "
                "도덕교육에서 가치탐구·도덕적 추론 수업 설계에 광범위하게 활용되었다."
            ),
            "key_concepts": [
                "반성적 사고", "탐구의 5단계", "문제 해결 학습", "과학적 사고"
            ]
        },
        {
            "id": "dewey-quest-for-certainty",
            "thinker_id": "dewey",
            "title": "확실성의 탐구",
            "title_original": "The Quest for Certainty: A Study of the Relation of Knowledge and Action",
            "year": 1929,
            "significance": (
                "서양 철학사가 지식(theoria)을 행위(praxis)보다 우위에 두고 "
                "고정불변의 확실성을 추구해온 전통을 비판한 후기 대표작. "
                "'방관자 이론(spectator theory of knowledge)'을 비판하고, "
                "지식은 세계에 개입하는 실험적 탐구를 통해 구성된다는 도구주의(instrumentalism)를 정교화했다. "
                "가치 판단 역시 지식과 동일한 탐구 절차로 검증 가능한 영역임을 주장하여 "
                "사실·가치 이원론을 해체했다."
            ),
            "key_concepts": [
                "도구주의", "방관자 이론 비판", "사실과 가치의 연속성",
                "실험적 탐구", "지식과 행위의 통합"
            ]
        },
        {
            "id": "dewey-public-and-its-problems",
            "thinker_id": "dewey",
            "title": "공공성과 그 문제들",
            "title_original": "The Public and Its Problems",
            "year": 1927,
            "significance": (
                "월터 리프먼(Walter Lippmann)의 엘리트주의 민주주의관에 대한 듀이의 응답. "
                "'공중(the public)'을 '행위의 간접적 결과에 영향을 받아 그것을 통제하려는 사람들'로 재정의하고, "
                "대중 사회에서 '공중의 식별(identification)과 소통'이 민주주의의 핵심 과제임을 주장했다. "
                "직접민주주의의 이상을 유지하면서도 대중사회의 조건에서 이를 실현하기 위해 "
                "대면적 공동체(face-to-face community)와 자유롭고 체계적인 의사소통의 부활을 강조했다. "
                "참여적 민주주의(participatory democracy) 이론의 고전적 원천이다."
            ),
            "key_concepts": [
                "공중", "참여적 민주주의", "대면적 공동체",
                "공적 소통", "간접적 결과의 통제"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """듀이 핵심 주장 데이터 입력."""
    claims = [
        {
            "id": "dewey-claim-001",
            "thinker_id": "dewey",
            "work_id": "dewey-democracy-and-education",
            "source_detail": "Democracy and Education, Chapter 7 'The Democratic Conception in Education'",
            "claim": (
                "민주주의는 단순한 정치 제도가 아니라 '함께 살아가는 방식이자 공동의 경험을 소통하는 양식'이며, "
                "교육은 이러한 민주주의를 실현하고 재생산하는 핵심 과정이다."
            ),
            "original_text": (
                "A democracy is more than a form of government; it is primarily a mode of associated living, "
                "of conjoint communicated experience."
            ),
            "original_text_ko": (
                "민주주의는 정부 형태 이상의 것이다. 그것은 일차적으로 연합적 삶의 방식이며, "
                "공동으로 소통되는 경험의 양식이다."
            ),
            "explanation": (
                "듀이는 민주주의를 투표·대의제 같은 정치 제도로 환원하지 않는다. "
                "그에게 민주주의는 성원들이 공통의 관심사를 공유하고 상호 작용하면서 "
                "각자의 행위가 타인에게 미치는 결과를 고려하는 삶의 양식이다. "
                "따라서 민주주의는 학교·가정·직장·지역사회 모든 곳에서 실현되어야 하며, "
                "교육은 이 민주적 삶의 방식을 익히게 하는 가장 체계적 제도이다."
            ),
            "argument": (
                "① 집단 성원의 자각적 관심의 수와 다양성이 크고, ② 타 집단과의 자유롭고 충분한 상호작용이 있을수록 "
                "그 사회는 민주적이다. ③ 이러한 상호작용과 공동 관심은 훈련된 습관과 지성(intelligence) 없이 유지될 수 없다. "
                "④ 따라서 민주주의 사회는 모든 구성원에게 지적·도덕적 성장을 보장하는 교육을 요청한다."
            ),
            "counterpoint": (
                "리프먼은 대중 사회에서 시민이 공적 사안에 대한 충분한 판단 능력을 갖기 어렵다며 "
                "전문가 중심 민주주의를 주장했다. "
                "엘리트주의자들은 듀이의 이상이 규모가 큰 현대 사회에서 비현실적이라고 비판한다."
            ),
            "context": (
                "제1차 세계대전 직후, 대중 사회와 관료제의 확대 속에서 민주주의의 실질적 의미가 약화되던 시기. "
                "듀이는 형식적 민주주의(제도로서의 민주주의)와 실질적 민주주의(삶의 방식으로서의 민주주의)를 구분하여 "
                "후자를 교육의 궁극 목적으로 제시했다."
            ),
            "keywords": ["민주주의", "함께 살아가는 방식", "교육", "공적 소통"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "dewey-claim-002",
            "thinker_id": "dewey",
            "work_id": "dewey-democracy-and-education",
            "source_detail": "Democracy and Education, Chapter 4 'Education as Growth'",
            "claim": (
                "교육의 목적은 교육 그 자체, 즉 '성장(growth)'이며 더 많은 성장을 가능하게 하는 성장이다. "
                "따라서 교육은 '삶을 위한 준비'가 아니라 현재 경험을 재구성함으로써 이루어지는 성장 과정 그 자체이다."
            ),
            "original_text": (
                "Since in reality there is nothing to which growth is relative save more growth, "
                "there is nothing to which education is subordinate save more education."
            ),
            "original_text_ko": (
                "실제로 성장은 더 많은 성장 이외의 어떤 것에도 종속되지 않으며, "
                "마찬가지로 교육은 더 많은 교육 이외의 어떤 것에도 종속되지 않는다."
            ),
            "explanation": (
                "듀이는 교육의 목적을 외부에 고정된 이상(완성된 인격, 직업인 등)에 두는 관점을 비판한다. "
                "성장은 새로운 경험을 통해 더 풍부한 경험을 할 능력을 획득하는 과정이며, "
                "이러한 성장 자체가 교육의 내재적 목적이다. 교육은 특정 단계에 끝나는 준비 기간이 아니라 "
                "평생 지속되는 경험 재구성의 과정이다."
            ),
            "argument": (
                "① 삶의 본질은 자기갱신(self-renewing) 과정이다. "
                "② 미성숙(immaturity)은 결함이 아니라 '성장할 수 있는 능력(ability to grow)'이라는 적극적 힘이다. "
                "③ 따라서 교육은 외부 목적을 위한 수단이 아니라 성장 능력을 지속적으로 확대하는 내재적 과정이다."
            ),
            "counterpoint": (
                "전통주의자들은 '성장'이 기준 없는 공허한 개념이며, 어떤 방향으로의 성장인지를 답하지 못한다고 비판한다. "
                "듀이는 '더 많은 성장을 가능하게 하는 성장'을 기준으로 제시하지만 "
                "악한 성향의 성장도 용인되는가라는 반론이 제기된다."
            ),
            "context": (
                "19세기 미국 교육은 '삶을 위한 준비'를 구호로 삼아 성인 사회의 요구를 아동에게 일방적으로 부과하는 경향이 강했다. "
                "듀이는 이러한 준비설(preparation theory)을 교육의 현재 가치를 부정하는 관점이라고 비판했다."
            ),
            "keywords": ["성장으로서의 교육", "경험의 재구성", "미성숙", "자기갱신"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "dewey-claim-003",
            "thinker_id": "dewey",
            "work_id": "dewey-experience-and-education",
            "source_detail": "Experience and Education, Chapter 3 'Criteria of Experience'",
            "claim": (
                "모든 경험이 교육적인 것은 아니며, 교육적 경험은 '경험의 연속성(continuity)'과 "
                "'상호작용(interaction)'이라는 두 원리를 동시에 충족해야 한다."
            ),
            "original_text": (
                "The principle of continuity of experience means that every experience both takes up something "
                "from those which have gone before and modifies in some way the quality of those which come after."
            ),
            "original_text_ko": (
                "경험의 연속성 원리란 모든 경험이 이전 경험에서 무언가를 이어받고, "
                "동시에 이후 경험의 질을 어떤 방식으로든 변화시킨다는 것을 의미한다."
            ),
            "explanation": (
                "연속성은 시간적 차원(이전-현재-이후 경험의 유기적 연결)을, "
                "상호작용은 공간적 차원(학습자의 내적 조건과 환경적 조건의 교호)을 나타낸다. "
                "두 원리의 종합이 '교육적 경험'을 판별하는 준거이며, "
                "이를 충족하지 못하는 경험은 '비교육적(mis-educative) 경험'이 되어 성장을 오히려 저해할 수 있다."
            ),
            "argument": (
                "① 경험은 단순한 외적 사건이 아니라 주체와 환경의 상호작용이다. "
                "② 어떤 경험이 이후 경험의 질을 높이는 방향으로 연결될 때에만 성장이 발생한다. "
                "③ 따라서 교사는 경험의 연속성과 상호작용이 바람직한 방향으로 작동하도록 환경을 설계해야 한다."
            ),
            "counterpoint": (
                "진보주의 내부 비판자들은 '바람직한 방향'을 판단할 객관 기준이 모호하다고 지적했다. "
                "보수주의자들은 두 원리가 전통 교과의 체계적 학습을 정당화하기 어렵다고 비판한다."
            ),
            "context": (
                "1930년대 미국 진보주의 교육운동은 '아동 중심' 구호 아래 교과 내용과 교사 역할을 지나치게 약화시키는 경향을 보였다. "
                "듀이는 이러한 왜곡을 바로잡기 위해 '경험과 교육'을 저술하여 교육적 경험의 준거를 명시했다."
            ),
            "keywords": ["경험의 연속성", "상호작용", "교육적 경험", "비교육적 경험"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "dewey-claim-004",
            "thinker_id": "dewey",
            "work_id": "dewey-how-we-think",
            "source_detail": "How We Think (1933 rev.), Chapter 7 'Analysis of Reflective Thinking'",
            "claim": (
                "반성적 사고(reflective thinking)는 (1) 문제 상황의 인식, (2) 문제의 명료화, "
                "(3) 가설 설정, (4) 추론을 통한 가설 검토, (5) 행위에 의한 가설 검증의 5단계로 이루어지며, "
                "교육의 핵심 목표는 학습자가 이러한 사고를 습관화하도록 돕는 것이다."
            ),
            "explanation": (
                "반성적 사고는 단순한 의견 나열이나 인상 표현과 달리, "
                "'문제 해결을 위한 증거 기반의 탐구'이다. "
                "듀이는 과학적 탐구의 논리를 교실로 가져와 학습자가 실제 문제 상황에서 "
                "가설을 세우고 검증하는 과정에서 지식을 능동적으로 구성하게 해야 한다고 보았다. "
                "도덕 문제 해결에도 동일한 탐구 구조가 적용될 수 있다."
            ),
            "argument": (
                "① 사고는 문제 상황(indeterminate situation)에서 발생한다. "
                "② 반성적 사고는 임의적 연상과 달리 증거에 의해 통제된다. "
                "③ 따라서 교사는 학습자가 실제 문제와 대면하도록 교육 환경을 설계하고, "
                "탐구 단계를 거쳐 스스로 해결에 이르도록 안내해야 한다."
            ),
            "counterpoint": (
                "비판자들은 5단계가 기계적으로 적용되면 학습이 오히려 형식화된다고 우려했다. "
                "듀이 자신도 단계는 고정된 순서가 아니라 탐구의 논리적 국면임을 명시했으나, "
                "많은 수업 설계에서 단계가 절차적 템플릿으로 경직화되는 경향이 나타났다."
            ),
            "context": (
                "19세기 말~20세기 초 미국 교육은 암기와 낭독 중심이었다. "
                "듀이는 과학적 탐구의 논리를 일반 교육 방법으로 확장하여 '문제 해결 학습'의 이론적 기초를 제공했다."
            ),
            "keywords": ["반성적 사고", "문제 해결 학습", "탐구의 5단계", "가설 검증"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "dewey-claim-005",
            "thinker_id": "dewey",
            "work_id": "dewey-quest-for-certainty",
            "source_detail": "The Quest for Certainty, Chapter 1",
            "claim": (
                "서양 철학은 지식을 관조(theoria) 대상으로 보는 '방관자 이론(spectator theory of knowledge)'에 사로잡혀 "
                "고정된 확실성을 추구해왔으나, 지식은 본래 세계에 개입하는 실험적 탐구를 통해 구성되는 '도구(instrument)'이다."
            ),
            "explanation": (
                "듀이는 플라톤 이래 서양 철학이 이론과 실천, 지식과 행위를 위계적으로 분리하고 "
                "전자에 확실성을 귀속시켜온 전통을 비판한다. "
                "그의 도구주의(instrumentalism)는 관념이나 이론을 그것이 문제 상황을 해결하는 데 얼마나 유효한가로 평가한다. "
                "지식은 세계에 대한 거울이 아니라 세계를 변화시키는 도구이며, 이에 따라 절대적 확실성 대신 "
                "'보증된 주장 가능성(warranted assertibility)'을 지식의 기준으로 삼는다."
            ),
            "argument": (
                "① 고대 철학은 변화하는 세계의 불안 앞에서 영원불변한 진리에 안식을 구했다. "
                "② 그러나 근대 과학은 지식이 실험과 조작을 통해 얻어짐을 보여준다. "
                "③ 따라서 철학도 관조적 확실성 추구를 포기하고, 경험 세계의 문제를 해결하는 실험적 탐구로 재정위되어야 한다."
            ),
            "counterpoint": (
                "실재론자들은 듀이의 도구주의가 진리 개념을 '유용성'으로 환원하여 "
                "과학적 실재론이 요구하는 객관성을 훼손한다고 비판한다. "
                "러셀(B. Russell) 등은 '보증된 주장 가능성'만으로는 진리의 대응적 측면을 설명할 수 없다고 지적했다."
            ),
            "context": (
                "기포드 강연(Gifford Lectures, 1929)을 토대로 한 저작. "
                "실증주의와 관념론이 각축하던 20세기 초 철학 지형에서 프래그머티즘의 입장을 체계적으로 제시했다."
            ),
            "keywords": ["도구주의", "방관자 이론", "프래그머티즘", "보증된 주장 가능성"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "dewey-claim-006",
            "thinker_id": "dewey",
            "work_id": "dewey-public-and-its-problems",
            "source_detail": "The Public and Its Problems, Chapter 5",
            "claim": (
                "민주주의는 대표자 선출과 다수결 절차로 환원되지 않는다. "
                "진정한 민주주의는 공중(the public)이 자신에게 영향을 미치는 간접적 결과를 인식하고 "
                "대면적 공동체와 자유로운 소통을 통해 스스로를 조직해가는 '참여적 민주주의(participatory democracy)'이다."
            ),
            "original_text": (
                "Democracy must begin at home, and its home is the neighborly community."
            ),
            "original_text_ko": (
                "민주주의는 반드시 가정에서 시작되어야 하며, 그 가정은 이웃하는 공동체이다."
            ),
            "explanation": (
                "듀이는 '공중'을 '행위의 간접적 결과에 영향을 받아 그것을 통제하려 조직된 사람들'로 정의한다. "
                "산업사회에서 행위의 결과가 광범위하고 복잡해지면서 공중 스스로도 자신을 식별하기 어려워졌는데, "
                "이를 해결하려면 대면적 공동체와 자유로운 탐구·소통을 통해 공적 쟁점을 함께 탐구할 수 있어야 한다. "
                "엘리트 전문가에게 민주주의를 위임하는 리프먼의 제안과 명확히 대조된다."
            ),
            "argument": (
                "① 공중은 본질적으로 간접적 결과를 인식·통제하려는 사람들의 집합이다. "
                "② 산업사회에서는 결과가 광범위해져 공중이 스스로를 식별하기 어렵다(공중의 '상실'). "
                "③ 그러므로 공중의 회복은 대면적 공동체의 활성화와 자유로운 소통에 달려 있으며, 이는 교육의 과제이다."
            ),
            "counterpoint": (
                "월터 리프먼은 『환상의 공중(The Phantom Public)』에서 대중이 공적 사안을 판단할 인지 자원이 부족하다며 "
                "전문가 주도의 민주주의를 제안했다. "
                "현실주의자들은 듀이의 참여적 민주주의를 낭만주의로 간주한다."
            ),
            "context": (
                "1920년대 미국은 대규모 산업화와 매스미디어의 팽창으로 지역 공동체가 약화되고 있었다. "
                "듀이는 리프먼과의 공개 논쟁에 응답하여 이 저서를 썼다."
            ),
            "keywords": ["참여적 민주주의", "공중", "대면적 공동체", "공공성"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "dewey-claim-007",
            "thinker_id": "dewey",
            "work_id": "dewey-democracy-and-education",
            "source_detail": "Democracy and Education, Chapter 26 'Theories of Morals'",
            "claim": (
                "도덕은 고정된 규칙의 체계가 아니라 '성장하는 경험' 속에서 지적으로 탐구되는 실천이다. "
                "선과 악은 선험적으로 주어진 본질이 아니라 구체적 상황에서의 결과와 성장 가능성을 기준으로 "
                "반성적으로 판단된다."
            ),
            "explanation": (
                "듀이 윤리학은 의무론과 공리주의 양자 모두를 비판적으로 수용한다. "
                "도덕은 원리 적용이나 쾌고 계산으로 환원되지 않고, 구체적 문제 상황에서 "
                "대안적 행위 방식을 상상·검토·검증하는 실험적 탐구이다. "
                "따라서 도덕 교육은 규칙 주입이나 덕목 암기가 아니라 "
                "학습자가 도덕적 문제 상황에서 반성적으로 판단하고 책임 있게 행위하도록 돕는 과정이다."
            ),
            "argument": (
                "① 도덕적 상황은 본질적으로 대안들 사이의 갈등 상황이다. "
                "② 이 상황에서 옳은 행위는 사전에 주어진 규칙의 연역이 아니라 결과를 고려한 실험적 판단을 통해 결정된다. "
                "③ 따라서 도덕교육은 반성적 사고의 훈련이며, 덕목 교화(indoctrination)와 구별된다."
            ),
            "counterpoint": (
                "덕윤리학자들은 듀이의 접근이 도덕적 성품의 안정성과 덕목의 지속적 함양을 소홀히 한다고 비판한다. "
                "칸트주의자들은 결과에 의존하는 판단이 도덕 법칙의 보편성을 훼손한다고 본다."
            ),
            "context": (
                "20세기 초 미국에서 전통적 덕목 교육과 새로운 진보주의 도덕교육이 충돌하고 있었다. "
                "듀이는 도덕을 삶의 모든 경험에 내재한 탐구 과정으로 재정의하여 "
                "도덕교육을 교과에서 분리하지 않고 전체 교육 과정에 통합해야 한다고 주장했다."
            ),
            "keywords": ["프래그머티즘 윤리", "도덕적 탐구", "반성적 도덕판단", "도덕교육"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "dewey-claim-008",
            "thinker_id": "dewey",
            "work_id": "dewey-democracy-and-education",
            "source_detail": "Democracy and Education, Chapter 23 'Vocational Aspects of Education'",
            "claim": (
                "직업교육과 교양교육의 이분법은 극복되어야 한다. "
                "진정한 교육은 직업적 활동 속에서 지적·도덕적 의미를 발견하고, "
                "교양을 삶의 모든 활동을 풍부히 하는 기반으로 통합한다."
            ),
            "explanation": (
                "듀이는 고대 그리스 이래 자유민의 교양교육(liberal education)과 노예·장인의 직업교육(vocational training)을 "
                "위계적으로 분리해온 전통을 비판한다. "
                "산업민주주의 사회에서 모든 시민은 노동자이자 시민이므로, "
                "직업적 활동이 사회적 의미와 지적 탐구로 연결되는 교육이 필요하다. "
                "이는 직업교육의 협소한 기능주의(단순 기술 훈련)와 교양교육의 유한계급적 엘리트주의 양자를 모두 넘어선다."
            ),
            "argument": (
                "① 모든 직업은 사회적 관계망 안에서 의미를 가지며, 단순 기술로 환원될 수 없다. "
                "② 교양은 특정 계급의 전유물이 아니라 모든 직업적 활동에 지적 의미를 부여하는 기반이다. "
                "③ 따라서 교육은 직업과 교양을 통합하여 학습자가 자신의 활동의 사회적·도덕적 의미를 이해하도록 해야 한다."
            ),
            "counterpoint": (
                "전통주의자들은 이 통합이 교양교육의 고유한 지적 엄밀성을 희석한다고 비판한다. "
                "마르크스주의 교육학자들은 듀이의 통합이 자본주의적 분업 구조 자체를 문제 삼지 않는다고 지적한다."
            ),
            "context": (
                "20세기 초 미국은 산업화와 이민 증가로 인해 실용 교육과 전통 교양교육 사이에서 "
                "교육과정 논쟁이 격렬했다. 듀이는 이분법 자체를 해체하는 제3의 길을 제시했다."
            ),
            "keywords": ["직업교육", "교양교육", "교육의 통합", "산업민주주의"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "dewey-claim-009",
            "thinker_id": "dewey",
            "work_id": "dewey-experience-and-education",
            "source_detail": "Experience and Education, Chapter 4",
            "claim": (
                "학교는 민주적 공동체의 축소판이어야 하며, 교사의 역할은 지식의 일방적 전달자가 아니라 "
                "학습자의 경험을 설계하고 민주적 탐구 공동체를 안내하는 '조직자'이다."
            ),
            "explanation": (
                "진보주의 교육의 일부 실천가들이 '아동의 자유'를 오해하여 교사의 적극적 역할을 회피하는 경향을 보이자, "
                "듀이는 교사가 아동의 경험을 방임하는 것이 아니라 "
                "교육적 경험이 일어나도록 환경을 설계하고 공동체를 이끄는 '전문적 안내자'여야 함을 강조했다. "
                "교실의 민주적 상호작용은 학교 밖 민주주의 실천의 준비이자 그 자체로 민주주의의 실현이다."
            ),
            "argument": (
                "① 아동의 경험은 스스로 교육적이 되지 않으며 환경 설계가 필요하다. "
                "② 교사는 집단 전체의 성장을 염두에 두고 활동을 조직할 지적·도덕적 책임이 있다. "
                "③ 권위주의와 방임의 이분법을 넘어 민주적 안내자로서 교사 역할을 재정의해야 한다."
            ),
            "counterpoint": (
                "급진적 진보주의자들은 교사의 '안내자' 역할조차 은폐된 권위라고 비판한다. "
                "반대로 전통주의자들은 교사의 지식 권위를 명시적으로 복권해야 한다고 주장한다."
            ),
            "context": (
                "1930년대 진보주의 교육 운동 내부의 혼란을 정리하기 위한 후기 저작의 핵심 논지. "
                "한국의 시민교육·도덕과 교육에서 '교사의 안내자 역할'을 논의할 때 자주 인용된다."
            ),
            "keywords": ["민주적 학교", "교사의 안내자 역할", "탐구 공동체", "경험 설계"],
            "verified": False,
            "verification_log": []
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """듀이 키워드 데이터 입력."""
    keywords = [
        {
            "id": "kw-dewey-experience",
            "term": "경험",
            "term_en": "experience",
            "definition": (
                "듀이 철학의 중심 개념으로, 유기체와 환경의 능동적 상호작용을 가리킨다. "
                "경험은 감각 인상의 수동적 수용이 아니라 '행함(doing)'과 '겪음(undergoing)'의 연속적 교호이다. "
                "교육·도덕·탐구 모두 경험 안에서 이루어지며, 경험은 '연속성'과 '상호작용'이라는 "
                "두 원리에 의해 교육적 질이 판정된다."
            ),
            "thinker_id": "dewey",
            "work_id": "dewey-experience-and-education",
            "related_terms": ["경험의 연속성", "상호작용", "경험의 재구성", "성장"]
        },
        {
            "id": "kw-dewey-inquiry",
            "term": "탐구",
            "term_en": "inquiry",
            "definition": (
                "'탐구의 논리(Logic, 1938)'에서 체계화된 듀이의 핵심 개념. "
                "불확정적 상황(indeterminate situation)을 확정적 상황(determinate situation)으로 변환하는 "
                "통제된 과정을 가리킨다. 과학적 탐구·도덕적 판단·일상적 문제 해결이 모두 동일한 탐구 구조를 공유한다. "
                "탐구의 결과는 절대적 진리가 아니라 '보증된 주장 가능성(warranted assertibility)'이다."
            ),
            "thinker_id": "dewey",
            "work_id": "dewey-quest-for-certainty",
            "related_terms": ["반성적 사고", "도구주의", "보증된 주장 가능성", "프래그머티즘"]
        },
        {
            "id": "kw-dewey-reflective-thinking",
            "term": "반성적 사고",
            "term_en": "reflective thinking",
            "definition": (
                "'사고하는 방법(How We Think)'에서 제시된 개념. "
                "문제 상황에 대해 증거 기반으로 대안을 검토하고 검증하는 사고 양식. "
                "(1) 문제 인식, (2) 문제 명료화, (3) 가설 설정, (4) 추론적 검토, (5) 행위에 의한 검증의 5단계로 분석된다. "
                "문제 해결 학습(problem-solving method)과 도덕적 판단 교육의 이론적 토대가 되었다."
            ),
            "thinker_id": "dewey",
            "work_id": "dewey-how-we-think",
            "related_terms": ["탐구", "문제 해결 학습", "가설 검증", "도덕적 판단"]
        },
        {
            "id": "kw-dewey-growth",
            "term": "성장으로서의 교육",
            "term_en": "education as growth",
            "definition": (
                "교육을 외부 목적(성인 사회 적응, 직업 준비 등)의 수단이 아니라 "
                "경험의 재구성을 통한 지속적 성장 자체로 보는 듀이의 교육관. "
                "성장은 '더 많은 성장을 가능하게 하는 성장'을 기준으로 평가되며, "
                "미성숙(immaturity)은 결함이 아니라 성장 능력이다."
            ),
            "thinker_id": "dewey",
            "work_id": "dewey-democracy-and-education",
            "related_terms": ["경험의 재구성", "미성숙", "교육의 목적", "자기갱신"]
        },
        {
            "id": "kw-dewey-continuity-interaction",
            "term": "경험의 연속성과 상호작용",
            "term_en": "continuity and interaction of experience",
            "definition": (
                "'경험과 교육(1938)'에서 제시된 교육적 경험의 두 준거. "
                "연속성(continuity): 모든 경험은 이전 경험을 이어받고 이후 경험의 질을 변화시킨다. "
                "상호작용(interaction): 경험은 학습자의 내적 조건과 환경적 조건의 교호 속에서 형성된다. "
                "두 원리의 종합이 교육적 경험과 비교육적(mis-educative) 경험을 구별하는 기준이다."
            ),
            "thinker_id": "dewey",
            "work_id": "dewey-experience-and-education",
            "related_terms": ["교육적 경험", "비교육적 경험", "경험", "환경"]
        },
        {
            "id": "kw-dewey-democracy",
            "term": "함께 살아가는 방식으로서의 민주주의",
            "term_en": "democracy as mode of associated living",
            "definition": (
                "민주주의를 정부 형태나 다수결 절차가 아니라 '연합적 삶의 방식이자 공동으로 소통되는 경험의 양식'으로 "
                "규정하는 듀이의 민주주의관. 민주주의는 가정·학교·직장·지역사회 등 모든 영역에서 "
                "실현되어야 하며, 교육은 이를 실현하는 핵심 과정이다."
            ),
            "thinker_id": "dewey",
            "work_id": "dewey-democracy-and-education",
            "related_terms": ["참여적 민주주의", "공중", "공적 소통", "민주시민교육"]
        },
        {
            "id": "kw-dewey-participatory-democracy",
            "term": "참여적 민주주의",
            "term_en": "participatory democracy",
            "definition": (
                "'공공성과 그 문제들(1927)'에서 정교화된 개념. "
                "공중(the public)이 자신에게 영향을 미치는 간접적 결과를 인식하고 "
                "대면적 공동체와 자유로운 소통을 통해 스스로를 조직·통제하는 민주주의. "
                "엘리트 전문가 주도의 대의민주주의(리프먼)와 대조된다."
            ),
            "thinker_id": "dewey",
            "work_id": "dewey-public-and-its-problems",
            "related_terms": ["공중", "대면적 공동체", "공공성", "민주주의"]
        },
        {
            "id": "kw-dewey-instrumentalism",
            "term": "도구주의",
            "term_en": "instrumentalism",
            "definition": (
                "관념·이론·지식을 문제 해결의 도구(instrument)로 평가하는 듀이의 프래그머티즘 인식론. "
                "지식은 세계를 거울처럼 반영하는 것이 아니라 경험 속 문제를 해결하기 위해 구성되는 도구이며, "
                "진리는 '보증된 주장 가능성'으로 재정의된다. '방관자 이론(spectator theory)'을 비판한다."
            ),
            "thinker_id": "dewey",
            "work_id": "dewey-quest-for-certainty",
            "related_terms": ["프래그머티즘", "방관자 이론", "탐구", "보증된 주장 가능성"]
        },
        {
            "id": "kw-dewey-reconstruction-of-experience",
            "term": "경험의 재구성",
            "term_en": "reconstruction of experience",
            "definition": (
                "교육을 '경험의 의미를 더 풍부하게 하고 이후 경험의 방향을 지도할 능력을 증진하는 경험의 재구성'으로 "
                "규정하는 듀이의 교육 정의. 단순한 경험의 누적이 아니라 이전 경험과 이후 경험을 "
                "지적으로 연결하고 갱신하는 과정이다."
            ),
            "thinker_id": "dewey",
            "work_id": "dewey-democracy-and-education",
            "related_terms": ["성장으로서의 교육", "경험의 연속성", "반성적 사고", "교육적 경험"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """듀이 관계 데이터 입력."""
    relations = [
        {
            "from_thinker": "dewey",
            "to_thinker": "piaget",
            "type": "influenced",
            "description": (
                "듀이의 프래그머티즘 교육철학, 특히 아동의 능동적 경험과 반성적 사고를 통한 학습 개념이 "
                "피아제의 구성주의 인지발달 이론 및 교육론 형성에 영향을 주었다. "
                "피아제는 자신의 교육 저작에서 듀이의 '행함으로써 배우기' 정신을 수용했다."
            ),
            "evidence": "Piaget, Science of Education and the Psychology of the Child (1969) — 듀이 교육철학 계승 언급"
        },
        {
            "from_thinker": "dewey",
            "to_thinker": "kohlberg",
            "type": "influenced",
            "description": (
                "듀이의 도덕적 탐구 개념과 민주적 교육 이념이 콜버그 도덕교육론의 철학적 배경이 되었다. "
                "콜버그는 학교를 '정의로운 공동체(just community)'로 재구성하자는 제안에서 "
                "듀이의 '학교 = 민주적 공동체의 축소판' 테제를 직접 계승했다."
            ),
            "evidence": "Kohlberg, 'The Moral Atmosphere of the School' (1970); 정의공동체 학교 프로그램"
        },
        {
            "from_thinker": "dewey",
            "to_thinker": "habermas",
            "type": "influenced",
            "description": (
                "듀이의 민주적 공적 탐구 개념(공중, 자유로운 소통, 참여적 민주주의)은 "
                "하버마스의 공론장(public sphere) 이론과 담론윤리(discourse ethics)의 미국 프래그머티즘적 원천으로 평가된다. "
                "하버마스는 후기 저작에서 자신의 담론이론이 듀이의 탐구 공동체 개념과 친화성이 있음을 명시했다."
            ),
            "evidence": "Habermas, 'Between Facts and Norms' (1992) — 듀이 프래그머티즘과의 친연성 언급"
        },
        {
            "from_thinker": "dewey",
            "to_thinker": "rawls",
            "type": "influenced",
            "description": (
                "듀이의 공적 탐구와 민주적 합당성(reasonableness) 개념이 롤스의 '공적 이성(public reason)' 이념의 "
                "미국적 사상사 배경 중 하나로 평가된다. 롤스는 1980년대 이후 저작에서 듀이 전통의 정치적 자유주의 요소를 흡수한다."
            ),
            "evidence": "Rawls, 'Political Liberalism' (1993); Dewey Lectures (1980)"
        }
    ]

    for rel in relations:
        rel_id = f"{rel['from_thinker']}-{rel['type']}-{rel['to_thinker']}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id}: {result['result']}")

    return len(relations)


def main():
    """메인 실행 함수."""
    print("=== 듀이(Dewey) 데이터 ES 입력 시작 ===\n")
    client = get_client()

    try:
        print("1. 분야(field) 확인/추가")
        ensure_field(client)
        print()

        print("2. 사상가(thinker) 입력")
        insert_thinker(client)
        print()

        print("3. 저서(works) 입력")
        work_count = insert_works(client)
        print(f"   → {work_count}개 저서 입력 완료\n")

        print("4. 주장(claims) 입력")
        claim_count = insert_claims(client)
        print(f"   → {claim_count}개 주장 입력 완료\n")

        print("5. 키워드(keywords) 입력")
        kw_count = insert_keywords(client)
        print(f"   → {kw_count}개 키워드 입력 완료\n")

        print("6. 관계(relations) 입력")
        rel_count = insert_relations(client)
        print(f"   → {rel_count}개 관계 입력 완료\n")

        print("=== 입력 요약 ===")
        print(f"  사상가: 1명 (dewey)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n듀이 데이터 입력 완료.")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}")
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
