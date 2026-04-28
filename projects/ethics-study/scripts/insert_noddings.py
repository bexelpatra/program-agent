"""넬 나딩스(Nel Noddings) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS, INDEX_FIELDS
)


def ensure_field(client):
    """도덕발달 분야가 ethics-fields 인덱스에 없으면 추가."""
    try:
        client.get(index=INDEX_FIELDS, id="moral_development")
        print("[field] moral_development: 이미 존재")
    except Exception:
        doc = {
            "id": "moral_development",
            "name": "도덕발달론",
            "description": (
                "아동 및 인간의 도덕 판단과 도덕 행동이 어떻게 발달하는지를 탐구하는 분야. "
                "피아제의 인지발달 기반 도덕발달 이론, 콜버그의 도덕발달 단계론, "
                "길리건의 배려윤리, 나딩스의 배려교육론 등을 포함한다. "
                "도덕심리학, 도덕교육론과 밀접하게 연관되며 임용시험 핵심 영역이다."
            ),
            "order": 4
        }
        result = client.index(index=INDEX_FIELDS, id="moral_development", document=doc)
        print(f"[field] moral_development: {result['result']}")


def insert_thinker(client):
    """나딩스 사상가 데이터 입력."""
    doc = {
        "id": "noddings",
        "name": "넬 나딩스",
        "name_en": "Nel Noddings",
        "field": "moral_development",
        "era": "현대",
        "birth_year": 1929,
        "death_year": 2022,
        "background": (
            "넬 나딩스는 미국 뉴저지 주 이링턴에서 태어났다. "
            "수학 교사로서 공립학교 현장에서 오랜 기간 근무한 경험을 바탕으로, "
            "교육철학과 도덕교육 이론을 발전시켰다. "
            "스탠퍼드 대학교 교육학과 교수로 재직하며 배려윤리(ethics of care)를 체계화했다. "
            "이후 컬럼비아 대학교 Teachers College 등에서도 강의하며 국제적 영향력을 넓혔다. "
            "1984년 출간한 '배려(Caring)'는 캐럴 길리건의 배려윤리 논의를 교육학적으로 심화·체계화한 저작으로, "
            "도덕교육론 분야의 고전이 되었다. "
            "나딩스는 철학적 윤리학과 교육학의 경계를 넘나들며, "
            "실천적 교육 현장 경험을 이론적 성찰과 결합한 독특한 학문적 입장을 견지했다."
        ),
        "core_philosophy": (
            "나딩스 사상의 핵심은 배려(caring)를 도덕의 근본으로 삼는 것이다. "
            "그녀는 칸트식의 보편적 원리나 정의(justice) 중심의 도덕철학을 비판하고, "
            "배려자(one-caring)와 피배려자(cared-for) 사이의 구체적이고 관계적인 도덕 경험을 강조한다. "
            "배려에는 두 가지 핵심 요소가 있다: "
            "전념(engrossment)은 배려자가 피배려자의 실제적 관심과 필요에 완전히 몰입하는 것이며, "
            "동기전환(motivational displacement)은 배려자 자신의 동기가 피배려자의 동기로 이동하는 것이다. "
            "자연적 배려(natural caring)는 자연스럽고 자발적인 배려이며, "
            "윤리적 배려(ethical caring)는 의식적 노력으로 배려를 실천하는 것이다. "
            "교육에서는 교과 중심이 아닌 배려 주제 중심의 전인교육(whole person education)을 주장하며, "
            "모델링, 대화, 실천, 확인의 네 가지 방법을 제안한다."
        ),
        "philosophical_journey": (
            "초기(교육현장 경험기, ~1970년대): 수학 교사로서의 현장 경험이 나딩스 철학의 원천이 되었다. "
            "규칙과 원리 중심의 전통적 도덕교육이 실제 교육 현장과 괴리됨을 절감하였다. "
            "중기(배려 이론 체계화, 1980~1990년대): 1984년 '배려: 윤리와 도덕교육에 대한 여성적 접근'을 출간하여 "
            "배려윤리의 철학적 기초를 정립했다. "
            "길리건의 심리학적 배려윤리를 교육철학으로 심화·확장했으며, "
            "마틴 부버(Martin Buber)의 대화철학과 만남의 개념에서도 영향을 받았다. "
            "1992년 '학교에서 배려에 대한 도전'으로 교육과정 개혁 논의를 선도했다. "
            "후기(행복과 교육, 2000년대 이후): 2003년 '행복과 교육'을 통해 "
            "교육의 궁극적 목적을 행복(happiness)으로 설정하고, "
            "배려 관계 속에서의 전인적 성장을 강조하는 방향으로 사상을 확장했다."
        ),
        "keywords": [
            "배려윤리",
            "전념",
            "동기전환",
            "배려자",
            "피배려자",
            "자연적 배려",
            "윤리적 배려",
            "모델링",
            "대화",
            "실천",
            "확인",
            "전인교육",
            "윤리적 이상",
            "관계적 존재론"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="noddings", document=doc)
    print(f"[thinker] noddings: {result['result']}")
    return result


def insert_works(client):
    """나딩스 저서 데이터 입력."""
    works = [
        {
            "id": "noddings-caring",
            "thinker_id": "noddings",
            "title": "배려: 윤리와 도덕교육에 대한 여성적 접근",
            "title_original": "Caring: A Feminine Approach to Ethics and Moral Education",
            "year": 1984,
            "significance": (
                "나딩스 배려윤리의 핵심 저작으로, 배려 관계를 도덕의 토대로 정립했다. "
                "전념(engrossment)과 동기전환(motivational displacement)이라는 배려의 두 핵심 요소를 제시하고, "
                "자연적 배려와 윤리적 배려를 구분했다. "
                "칸트적 원리·규칙 중심 도덕철학을 비판하고, "
                "구체적 관계와 맥락에서 출발하는 배려윤리의 철학적 기초를 마련했다. "
                "도덕교육에서 모델링, 대화, 실천, 확인의 네 가지 방법을 제안했다."
            ),
            "key_concepts": [
                "배려(caring)", "전념(engrossment)", "동기전환(motivational displacement)",
                "자연적 배려", "윤리적 배려", "배려자", "피배려자", "윤리적 이상",
                "모델링", "대화", "실천", "확인"
            ]
        },
        {
            "id": "noddings-challenge-to-care",
            "thinker_id": "noddings",
            "title": "배려에의 도전: 학교에서 배려윤리",
            "title_original": "The Challenge to Care in Schools: An Alternative Approach to Education",
            "year": 1992,
            "significance": (
                "나딩스가 배려윤리를 학교 교육과정에 적용한 저작. "
                "교과 중심 교육과정을 비판하고, 배려의 주제 중심으로 교육과정을 재편할 것을 제안했다. "
                "자기 자신 배려, 가까운 타인 배려, 먼 타인 배려, 동식물 배려, 인공물 배려, 관념 배려 등 "
                "배려의 영역을 다층적으로 구분했다. "
                "전인교육(whole person education)을 위한 구체적 교육과정 모델을 제시했다."
            ),
            "key_concepts": [
                "전인교육", "배려 주제 중심 교육과정", "배려의 영역", "학교 개혁"
            ]
        },
        {
            "id": "noddings-philosophy-of-education",
            "thinker_id": "noddings",
            "title": "교육철학",
            "title_original": "Philosophy of Education",
            "year": 1995,
            "significance": (
                "나딩스의 교육철학 입문서로, 배려윤리를 비롯한 다양한 교육철학적 논의를 체계적으로 정리했다. "
                "전통적·진보적 교육철학의 쟁점들을 검토하면서, "
                "배려 관계를 중심으로 한 나딩스의 교육철학적 입장을 종합했다. "
                "교사-학생 관계, 교육의 목적, 교육과정 설계 등에서 배려윤리의 함의를 논의했다."
            ),
            "key_concepts": [
                "교육철학", "교사-학생 관계", "배려 관계", "교육의 목적"
            ]
        },
        {
            "id": "noddings-happiness-and-education",
            "thinker_id": "noddings",
            "title": "행복과 교육",
            "title_original": "Happiness and Education",
            "year": 2003,
            "significance": (
                "나딩스가 교육의 궁극적 목적을 행복(happiness)으로 정립한 저작. "
                "아리스토텔레스의 에우다이모니아(eudaimonia)와 현대적 행복론을 검토하면서, "
                "배려 관계 속에서 실현되는 진정한 행복과 전인적 성장을 논의했다. "
                "가정의 배려 경험이 학교 교육과 행복에 미치는 영향을 강조했다."
            ),
            "key_concepts": [
                "행복(happiness)", "에우다이모니아", "전인적 성장", "배려와 행복"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """나딩스 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 배려의 두 핵심 요소 — 전념과 동기전환
        {
            "id": "noddings-claim-001",
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "source_detail": "Caring, Chapter 2: A Feminine Approach to Ethics",
            "claim": (
                "배려(caring)는 두 가지 핵심 요소로 이루어진다: "
                "전념(engrossment)과 동기전환(motivational displacement). "
                "전념은 배려자가 피배려자의 실재와 관심에 완전히 몰입하는 것이며, "
                "동기전환은 배려자 자신의 동기가 피배려자의 동기와 필요로 이동하여 "
                "피배려자를 위해 행동하게 되는 것이다."
            ),
            "explanation": (
                "나딩스는 배려를 단순한 감정이나 태도가 아니라, 구체적인 관계 속에서 실현되는 것으로 본다. "
                "전념(engrossment): 배려자는 피배려자를 진정으로 이해하기 위해 "
                "자신의 선입관·편견·가치관을 잠시 내려놓고 피배려자의 현실과 감정을 있는 그대로 받아들인다. "
                "이는 감정이입(empathy)과 유사하지만, 피배려자를 자신의 내면에 투사하는 것이 아니라 "
                "피배려자 자체로 받아들이는 것이다. "
                "동기전환(motivational displacement): 배려자의 에너지와 동기가 자신의 목적에서 "
                "피배려자의 필요와 목적으로 이동한다. "
                "배려자는 '내가 무엇을 원하는가'가 아니라 '이 사람에게 무엇이 필요한가'를 중심으로 행동한다."
            ),
            "argument": (
                "나딩스는 실제 배려 관계(어머니-자녀, 교사-학생)의 현상학적 분석으로 이 두 요소를 도출한다. "
                "배려 관계에서 배려자는 피배려자의 현실에 수용적·공감적으로 열려 있으며(전념), "
                "피배려자의 필요를 충족시키기 위해 자신의 에너지를 기꺼이 전환한다(동기전환). "
                "이 두 요소가 없으면 진정한 배려가 아니라 '배려하는 척'에 불과하다."
            ),
            "counterpoint": (
                "일부 비판자들은 전념과 동기전환의 개념이 지나치게 자기희생을 요구하여 "
                "배려자(특히 여성)의 소진(burnout)과 착취로 이어질 수 있다고 지적한다. "
                "나딩스는 이에 대해 배려자 자신도 배려받아야 하며, "
                "윤리적 자아(ethical self)의 유지가 지속적 배려를 가능하게 한다고 응답한다."
            ),
            "context": (
                "나딩스는 칸트식 의무론이나 공리주의가 추상적 원리를 앞세워 "
                "구체적 인간 관계의 도덕적 경험을 간과한다고 보았다. "
                "배려의 두 요소는 그러한 추상성에 맞서 관계적·구체적 도덕의 핵심을 포착하기 위한 개념이다."
            ),
            "keywords": ["전념", "동기전환", "배려", "배려자", "피배려자"],
            "verified": False
        },
        # CLAIM-002: 배려자(one-caring)와 피배려자(cared-for) 관계
        {
            "id": "noddings-claim-002",
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "source_detail": "Caring, Chapter 2",
            "claim": (
                "배려 관계는 배려자(one-caring)와 피배려자(cared-for)로 구성되며, "
                "이 관계는 상호적이지만 대칭적이지 않다. "
                "배려자는 전념과 동기전환을 통해 피배려자를 배려하며, "
                "피배려자는 그 배려를 수용·인정(reception)함으로써 배려 관계를 완성한다."
            ),
            "explanation": (
                "나딩스는 배려를 일방적 행위가 아닌 관계적 사건(relational event)으로 본다. "
                "배려자(one-caring)는 전념과 동기전환을 통해 피배려자를 위해 행동한다. "
                "피배려자(cared-for)는 배려를 받아 인정하고, 그 인정(acknowledgment)을 배려자에게 보냄으로써 "
                "배려 관계가 완성된다. "
                "이 관계는 상호적(reciprocal)이지만, 역할과 책임의 무게가 배려자에게 더 크게 놓인다는 점에서 "
                "비대칭적(asymmetric)이다. "
                "교사-학생 관계에서 교사는 배려자, 학생은 피배려자의 역할을 하며, "
                "학생의 수용과 반응이 교사의 배려를 완성시킨다."
            ),
            "argument": (
                "나딩스는 배려가 혼자서는 실현될 수 없으며, "
                "반드시 피배려자의 수용과 반응 속에서만 성립한다고 주장한다. "
                "교사가 아무리 학생을 배려해도 학생이 그것을 받아들이지 않으면 배려 관계는 성립하지 않는다. "
                "따라서 피배려자 역시 배려 관계에서 도덕적 역할을 담당한다."
            ),
            "counterpoint": (
                "비판자들은 피배려자의 수용을 배려의 완성 조건으로 삼는 것이 "
                "피배려자가 배려를 거부하거나 수용할 능력이 없는 경우를 설명하기 어렵다고 지적한다. "
                "또한 관계의 비대칭성이 배려자의 과도한 부담으로 이어질 수 있다."
            ),
            "context": (
                "나딩스는 도덕의 출발점을 고립된 개인의 이성이 아니라 "
                "관계 속에서 찾는다. 배려자와 피배려자의 관계 구조가 바로 그 출발점이다."
            ),
            "keywords": ["배려자", "피배려자", "배려 관계", "수용", "상호성"],
            "verified": False
        },
        # CLAIM-003: 자연적 배려와 윤리적 배려
        {
            "id": "noddings-claim-003",
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "source_detail": "Caring, Chapter 3: Ethical Caring",
            "claim": (
                "배려에는 자연적 배려(natural caring)와 윤리적 배려(ethical caring)의 두 종류가 있다. "
                "자연적 배려는 자발적·본능적으로 이루어지는 배려이며, "
                "윤리적 배려는 자연적 배려가 어려운 상황에서 '최선의 자아(best self)'와 "
                "'윤리적 이상(ethical ideal)'에 의지하여 의식적 노력으로 배려를 실천하는 것이다."
            ),
            "explanation": (
                "자연적 배려(natural caring): 자녀를 향한 어머니의 배려처럼 "
                "자발적이고 자연스럽게 흘러나오는 배려. 의지적 노력 없이도 이루어진다. "
                "윤리적 배려(ethical caring): 좋아하지 않거나 낯선 사람, 어렵고 힘든 상황에서도 "
                "배려해야 한다는 당위를 느낄 때 작동하는 배려. "
                "'나는 배려해야 한다(I ought)'는 감각과 '나는 배려하고 싶다(I want to care)'라는 "
                "기억된 자연적 배려의 경험이 결합하여 윤리적 배려가 실현된다. "
                "윤리적 배려는 자연적 배려의 기억과 이상적 배려자로서의 자기 이미지(ethical ideal)에 의해 동기부여된다."
            ),
            "argument": (
                "나딩스는 도덕적 당위('해야 한다')가 외부의 원리나 법칙에서 오는 것이 아니라, "
                "자연적 배려의 경험에서 기원한다고 주장한다. "
                "우리는 자연적 배려를 통해 배려하는 것이 무엇인지 알며, "
                "그 경험을 통해 배려가 어려운 상황에서도 배려하려는 윤리적 동기를 얻는다."
            ),
            "counterpoint": (
                "칸트적 윤리학자들은 자연적 감정에서 도덕적 당위를 도출하는 것은 "
                "'자연주의적 오류(naturalistic fallacy)'라고 비판할 수 있다. "
                "또한 자연적 배려가 편애(favoritism)를 조장하여 정의(justice)를 훼손할 수 있다는 비판도 있다."
            ),
            "context": (
                "나딩스는 칸트의 '의무에서 행해진 행위만이 도덕적 가치를 가진다'는 주장에 반대하며, "
                "자연적 배려를 도덕의 출발점으로 삼는다."
            ),
            "keywords": ["자연적 배려", "윤리적 배려", "윤리적 이상", "최선의 자아"],
            "verified": False
        },
        # CLAIM-004: 윤리적 이상(ethical ideal)
        {
            "id": "noddings-claim-004",
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "source_detail": "Caring, Chapter 3",
            "claim": (
                "배려윤리의 목표는 윤리적 이상(ethical ideal)을 유지하고 강화하는 것이다. "
                "윤리적 이상은 '내가 최선의 배려자(best one-caring)였을 때'의 기억과 이미지로 구성되며, "
                "윤리적 배려의 동기가 된다. 도덕교육은 이 윤리적 이상을 풍요롭게 하는 과정이어야 한다."
            ),
            "explanation": (
                "나딩스는 추상적인 도덕 원리(예: 선의지, 최대 행복) 대신, "
                "각자의 삶에서 형성된 '최선의 배려자 자아(best caring self)'의 이미지를 도덕의 준거로 삼는다. "
                "윤리적 이상은 고정된 것이 아니라 살아있는 경험과 관계 속에서 계속 변화하고 성장한다. "
                "도덕교육은 학생들이 풍부한 배려 경험을 쌓고, "
                "더 나은 배려자가 되고 싶다는 바람(윤리적 이상)을 키우도록 도와야 한다."
            ),
            "argument": (
                "나딩스는 도덕적 행동의 동기가 '규칙을 따라야 한다'는 의무감보다 "
                "'나는 배려하는 사람이 되고 싶다'는 욕구와 이상에 있다고 주장한다. "
                "윤리적 이상이 강할수록 어려운 상황에서도 배려를 실천할 가능성이 높아진다."
            ),
            "counterpoint": (
                "윤리적 이상이 개인의 경험과 기억에 의존하기 때문에, "
                "보편적 도덕 기준을 제시하지 못한다는 비판이 있다. "
                "또한 배려 경험이 부족한 사람은 윤리적 이상 자체가 빈약할 수 있다."
            ),
            "context": (
                "나딩스는 공리주의나 의무론적 윤리학이 제시하는 추상적 도덕 원리에 반대하며, "
                "구체적 관계 경험에서 형성되는 윤리적 이상을 도덕의 준거로 삼는다."
            ),
            "keywords": ["윤리적 이상", "최선의 자아", "도덕 동기", "배려 경험"],
            "verified": False
        },
        # CLAIM-005: 정의윤리 비판 — 원리·규칙 중심 도덕의 한계
        {
            "id": "noddings-claim-005",
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "source_detail": "Caring, Chapter 2",
            "claim": (
                "원리·규칙 중심의 정의윤리(ethics of justice)는 구체적 인간 관계의 도덕 경험을 간과한다. "
                "도덕적 결정은 보편적 원리의 적용이 아니라 구체적 상황과 관계 속에서 이루어지며, "
                "배려의 관계적 맥락이 도덕적 판단의 진정한 출발점이 되어야 한다."
            ),
            "explanation": (
                "나딩스는 칸트의 정언명령과 공리주의적 최대행복 원리처럼 "
                "추상적이고 보편적인 도덕 원리를 비판한다. "
                "이러한 원리들은 구체적인 관계에서 느껴지는 배려의 경험을 담아내지 못하며, "
                "도덕적 판단에서 감정과 관계의 역할을 부당하게 축소한다. "
                "나딩스는 도덕적 문제는 '원리 X를 이 상황에 적용하면 어떤 결론이 나오는가'가 아니라 "
                "'이 관계에서 나는 어떻게 배려할 수 있는가'라는 방식으로 접근해야 한다고 주장한다."
            ),
            "argument": (
                "나딩스는 콜버그의 '하인즈 딜레마'에서 제이크(Jake)와 에이미(Amy)의 응답을 예로 든다. "
                "콜버그는 원리 중심으로 답한 제이크를 더 높은 도덕 수준으로 평가했으나, "
                "나딩스(와 길리건)는 에이미의 관계·배려 중심 응답도 동등하게 도덕적임을 주장한다. "
                "정의윤리는 추상성·보편성을 미덕으로 삼지만, 실제 도덕 경험의 구체성과 특수성을 잃는다."
            ),
            "counterpoint": (
                "비판자들은 배려윤리가 보편적 정의 원칙을 포기함으로써 "
                "불공정과 차별을 정당화할 수 있다고 우려한다. "
                "나딩스는 배려윤리가 정의를 부정하는 것이 아니라 보완한다고 응답하지만, "
                "대규모 사회적 문제(예: 분배 정의)를 다루는 데 한계가 있다는 비판은 남아 있다."
            ),
            "context": (
                "나딩스는 콜버그의 정의 중심 도덕발달론과 길리건의 비판에 영향을 받아, "
                "도덕교육에서 배려를 정의보다 우선시하거나 적어도 동등하게 다루어야 한다고 주장했다."
            ),
            "keywords": ["정의윤리 비판", "원리 중심 도덕", "배려윤리", "관계적 맥락"],
            "verified": False
        },
        # CLAIM-006: 배려의 4가지 교육 방법
        {
            "id": "noddings-claim-006",
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "source_detail": "Caring, Chapter 9: An Ethic of Caring in Education",
            "claim": (
                "배려윤리를 교육적으로 실현하기 위해 네 가지 방법이 필요하다: "
                "모델링(modeling), 대화(dialogue), 실천(practice), 확인(confirmation). "
                "이 네 가지는 배려하는 사람을 길러내기 위한 핵심 교육적 방법이다."
            ),
            "explanation": (
                "모델링(modeling): 교사가 배려하는 태도와 행동을 직접 보여준다. "
                "학생은 배려 관계를 관찰하고 그 안에서 배려가 무엇인지 배운다. "
                "대화(dialogue): 개방적이고 진지한 대화를 통해 학생과 교사가 서로를 이해한다. "
                "이 대화는 일방적 교훈이 아닌 쌍방향의 탐색이다. "
                "실천(practice): 배려를 실제로 경험하고 실천할 기회를 제공한다. "
                "봉사 학습, 협동 프로젝트, 공동체 참여 등이 이에 해당한다. "
                "확인(confirmation): 교사는 학생에게서 최선의 자아(best self)를 발견하고, "
                "그 잠재력을 긍정하고 격려한다. 학생이 더 나은 배려자가 될 수 있다는 믿음을 전달한다."
            ),
            "argument": (
                "나딩스는 배려는 가르칠 수 있는 것이 아니라 경험되고 실천되어야 하는 것이라고 주장한다. "
                "도덕교육에서 추상적 원리나 교훈을 주입하는 방식은 실패하며, "
                "실제 배려 관계를 경험하고 그 안에서 성장하는 것이 진정한 도덕교육이다. "
                "네 가지 방법은 이 경험적·실천적 도덕교육을 실현하기 위한 구체적 방법론이다."
            ),
            "counterpoint": (
                "이 네 가지 방법이 교실 현장에서 어떻게 체계적으로 실현될 수 있는지 "
                "구체적 교육과정이나 평가 방식에 대한 논의가 부족하다는 비판이 있다. "
                "또한 교사의 배려 역량에 전적으로 의존하는 방식이 교사 소진을 유발할 수 있다."
            ),
            "context": (
                "나딩스는 지식 전달 중심의 전통 교육을 비판하고, "
                "배려 관계를 교육의 핵심에 놓는 새로운 교육 패러다임을 제시하고자 했다."
            ),
            "keywords": ["모델링", "대화", "실천", "확인", "도덕교육 방법"],
            "verified": False
        },
        # CLAIM-007: 전인교육 — 배려 주제 중심 교육과정
        {
            "id": "noddings-claim-007",
            "thinker_id": "noddings",
            "work_id": "noddings-challenge-to-care",
            "source_detail": "The Challenge to Care in Schools, Chapter 1",
            "claim": (
                "학교 교육과정은 교과 중심이 아닌 배려의 주제(themes of care) 중심으로 재편되어야 한다. "
                "전인교육(whole person education)은 학업적 성취뿐 아니라 "
                "자기 자신, 타인, 동식물, 인공물, 관념에 대한 배려 능력의 발달을 목적으로 해야 한다."
            ),
            "explanation": (
                "나딩스는 학교가 과도하게 학업 성취와 대학 입학에 초점을 맞추어 "
                "학생들의 전인적 발달을 소홀히 한다고 비판한다. "
                "배려 주제 중심 교육과정은 다음 영역의 배려를 포괄한다: "
                "(1) 자기 자신에 대한 배려(자아 이해, 건강, 영성 등), "
                "(2) 친밀한 타인에 대한 배려(가족, 친구 관계), "
                "(3) 먼 타인에 대한 배려(시민 의식, 세계 시민), "
                "(4) 동식물과 자연에 대한 배려(환경 감수성), "
                "(5) 인공물에 대한 배려(물건의 의미와 책임), "
                "(6) 관념에 대한 배려(지적 호기심, 학문적 열정). "
                "각 교과는 이 배려 주제와 연결될 때 생명력을 갖는다."
            ),
            "argument": (
                "나딩스는 현행 교과 중심 교육과정이 특정 유형의 학생(학문적 성향)에게만 유리하며, "
                "다양한 관심과 재능을 가진 학생들을 소외시킨다고 주장한다. "
                "배려 주제 중심으로 교육과정을 재편하면 모든 학생이 의미 있는 교육 경험을 할 수 있다."
            ),
            "counterpoint": (
                "전통주의자들은 배려 주제 중심 교육과정이 학문적 엄격성을 희생시킬 수 있다고 우려한다. "
                "또한 이 접근법이 실제 교육 시스템(시험, 대입 등)과 어떻게 양립할 수 있는지에 대한 "
                "구체적 방안이 부족하다는 비판도 있다."
            ),
            "context": (
                "나딩스는 학교 개혁 논쟁이 한창이던 1990년대 미국 교육계에서 "
                "학업 성취 위주의 교육 개혁에 반대하며 전인교육의 대안을 제시했다."
            ),
            "keywords": ["전인교육", "배려 주제 중심", "교육과정 개혁", "학교 개혁"],
            "verified": False
        },
        # CLAIM-008: 관계적 존재론
        {
            "id": "noddings-claim-008",
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "source_detail": "Caring, Chapter 2",
            "claim": (
                "인간은 본질적으로 관계 속의 존재이다(relational ontology). "
                "도덕성은 고립된 자아의 이성에서 출발하는 것이 아니라, "
                "타인과의 구체적인 관계 속에서 형성되고 표현된다. "
                "배려는 이 관계적 존재로서의 인간에 가장 적합한 도덕 형태이다."
            ),
            "explanation": (
                "나딩스는 서양의 도덕철학이 독립적이고 자율적인 개인(autonomous individual)을 "
                "도덕의 출발점으로 삼는 것을 비판한다. "
                "인간은 태어날 때부터 어머니와의 관계 속에 있으며, "
                "성장하면서도 수많은 관계 속에서 자아를 형성한다. "
                "따라서 도덕의 출발점은 고립된 이성이 아니라 관계 속에서의 배려 경험이어야 한다."
            ),
            "argument": (
                "나딩스는 실제 도덕 생활을 돌아보면, "
                "우리가 도덕적으로 행동하는 것은 추상적 원리를 따르기 때문이 아니라 "
                "구체적인 관계 속에서 타인의 필요를 느끼기 때문임을 주장한다. "
                "관계적 존재론은 이 도덕 경험의 실제를 더 잘 포착한다."
            ),
            "counterpoint": (
                "관계적 존재론이 가까운 관계에만 편향된 배려를 정당화하고, "
                "낯선 타인이나 미래 세대에 대한 도덕적 책임을 약화시킬 수 있다는 비판이 있다."
            ),
            "context": (
                "나딩스는 마틴 부버의 '나-너(I-Thou)' 관계 철학에서 영향을 받아, "
                "관계를 도덕의 근본 조건으로 삼는 존재론적 기반을 마련했다."
            ),
            "keywords": ["관계적 존재론", "배려", "관계", "자아"],
            "verified": False
        },
        # CLAIM-009: 가정에서의 배려 경험과 도덕성의 기초
        {
            "id": "noddings-claim-009",
            "thinker_id": "noddings",
            "work_id": "noddings-happiness-and-education",
            "source_detail": "Happiness and Education, Chapter 8",
            "claim": (
                "가정(home)에서의 배려 경험은 도덕성과 행복의 기초이다. "
                "어머니와 자녀 간의 자연적 배려 관계가 도덕 발달의 원초적 모델이며, "
                "학교는 이 가정적 배려의 정신을 이어받아야 한다."
            ),
            "explanation": (
                "나딩스는 가정에서의 어머니-자녀 관계를 배려의 원형(paradigm)으로 삼는다. "
                "어머니는 아이의 필요에 전념하고(engrossment), "
                "자신의 동기를 아이의 동기로 전환함으로써(motivational displacement) 자연적 배려를 실현한다. "
                "이 초기 가정 배려 경험이 아이에게 '배려받음'과 '배려함'의 감각을 심어주며, "
                "이후 도덕 발달의 토대가 된다. "
                "학교는 이 가정의 배려 정신을 이어받아 학생들이 배려받는 경험을 제공해야 한다."
            ),
            "argument": (
                "나딩스는 도덕 발달의 첫 번째 교사는 학교가 아니라 가정이며, "
                "가정에서 배려받지 못한 아이는 도덕 발달에 어려움을 겪는다고 주장한다. "
                "따라서 교육 정책은 가정의 배려 기능을 지원해야 하며, "
                "학교 교육도 가정의 배려를 보완하고 확장하는 역할을 해야 한다."
            ),
            "counterpoint": (
                "어머니의 배려를 도덕의 원형으로 삼는 것이 성별 역할을 고정화하고 "
                "여성에게 배려의 의무를 부과하는 결과를 낳을 수 있다는 페미니즘적 비판이 있다. "
                "나딩스는 후기 저작에서 이 비판을 수용하여 배려의 성 중립성을 강조했다."
            ),
            "context": (
                "나딩스는 '행복과 교육'에서 교육의 목적을 행복으로 설정하면서, "
                "가정과 학교에서의 배려 관계가 행복의 핵심 조건임을 주장했다."
            ),
            "keywords": ["가정 배려", "도덕성의 기초", "어머니-자녀 관계", "학교-가정 연계"],
            "verified": False
        },
        # CLAIM-010: 교사-학생 관계에서의 배려
        {
            "id": "noddings-claim-010",
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "source_detail": "Caring, Chapter 9",
            "claim": (
                "교사-학생 관계는 배려 관계의 핵심 형태이며, "
                "교사는 학생에게 전념(engrossment)하고 동기를 전환(motivational displacement)함으로써 "
                "학생의 필요와 성장에 응답해야 한다. "
                "이 배려 관계 속에서 학생은 최선의 자아로 성장할 수 있다."
            ),
            "explanation": (
                "나딩스는 교사-학생 관계를 이상적 배려 관계의 모델로 제시한다. "
                "배려하는 교사(one-caring teacher)는: "
                "(1) 학생의 현실적 관심사와 필요에 전념하며, "
                "(2) 자신의 교육 목표보다 학생의 필요와 성장을 우선시하며, "
                "(3) 학생의 최선의 자아를 발견하고 긍정한다(확인, confirmation). "
                "이러한 배려 관계는 지식 전달 이상의 것, 즉 학생의 도덕적·인격적 성장을 가능하게 한다."
            ),
            "argument": (
                "나딩스는 교육의 질은 교육과정이나 시험보다 교사와 학생의 관계의 질에 달려 있다고 주장한다. "
                "배려하는 교사와의 관계 속에서 학생은 단순히 지식을 습득하는 것이 아니라 "
                "배려하는 법을 배우고, 자신이 가치 있는 존재임을 경험한다."
            ),
            "counterpoint": (
                "배려 중심 교육관이 교사의 개인적 역량과 감정에 지나치게 의존하여 "
                "교사 소진(burnout)을 심화시킬 수 있다. "
                "또한 배려를 측정·평가하기 어렵기 때문에 교육 책무성과 충돌한다는 비판이 있다."
            ),
            "context": (
                "나딩스는 학교 현장에서 관료적·도구적 교육관이 지배하는 것에 반발하며, "
                "교사-학생 관계의 도덕적·인격적 차원을 회복할 것을 촉구했다."
            ),
            "keywords": ["교사-학생 관계", "배려 교육", "확인", "학생 성장"],
            "verified": False
        },
        # CLAIM-011: 배려의 상호성과 비대칭성
        {
            "id": "noddings-claim-011",
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "source_detail": "Caring, Chapter 4",
            "claim": (
                "배려 관계는 상호적이지만 대칭적이지 않다. "
                "배려자(one-caring)와 피배려자(cared-for)의 역할과 책임은 다르며, "
                "배려자는 더 큰 도덕적 책임을 진다. "
                "그러나 이 비대칭성은 착취가 아니라 관계적 성장의 조건이다."
            ),
            "explanation": (
                "나딩스는 배려 관계에서 배려자가 피배려자보다 더 많은 것을 주는 것처럼 보이지만, "
                "이것이 착취나 희생이 아님을 강조한다. "
                "배려자는 피배려자를 배려함으로써 자신의 윤리적 이상을 실현하고 성장한다. "
                "피배려자는 배려를 받음으로써 성장하고, 나중에 배려자가 될 역량을 키운다. "
                "장기적으로 이 관계는 상호 성장을 가능하게 한다."
            ),
            "argument": (
                "나딩스는 어머니-자녀 관계, 교사-학생 관계를 예로 들어 "
                "비대칭적 배려 관계가 어떻게 양쪽 모두의 성장을 가능하게 하는지 보여준다. "
                "어머니는 아이를 배려함으로써 자신도 성장하고, "
                "아이는 배려받음으로써 나중에 타인을 배려할 수 있는 존재가 된다."
            ),
            "counterpoint": (
                "비대칭적 배려 관계가 배려자의 자기희생과 소진을 정당화하는 데 남용될 수 있다는 비판이 있다. "
                "특히 여성이 배려자 역할을 도맡는 사회적 현실에서 이 이론이 성 불평등을 강화할 수 있다."
            ),
            "context": (
                "나딩스는 배려 관계의 비대칭성을 인정하면서도, "
                "이것이 착취나 억압이 아닌 관계적 성장의 조건임을 밝히려 했다."
            ),
            "keywords": ["배려의 상호성", "배려의 비대칭성", "관계적 성장"],
            "verified": False
        },
        # CLAIM-012: 행복과 교육의 목적
        {
            "id": "noddings-claim-012",
            "thinker_id": "noddings",
            "work_id": "noddings-happiness-and-education",
            "source_detail": "Happiness and Education, Introduction and Chapter 1",
            "claim": (
                "교육의 궁극적 목적은 학업 성취나 경제적 생산성이 아니라 행복(happiness)이다. "
                "진정한 행복은 배려 관계와 의미 있는 활동 속에서 실현되며, "
                "학교는 이 행복을 지향하는 교육 환경을 만들어야 한다."
            ),
            "explanation": (
                "나딩스는 현대 교육이 표준화된 시험, 대학 입학, 경제적 생산성을 목표로 삼아 "
                "학생들의 행복과 전인적 발달을 소홀히 한다고 비판한다. "
                "나딩스가 말하는 행복은 쾌락적 행복(hedonic happiness)이 아니라 "
                "아리스토텔레스의 에우다이모니아에 가까운 '번성하는 삶(flourishing life)'이다. "
                "이 행복은 타인과의 배려 관계, 자신이 좋아하는 활동에의 몰입, "
                "공동체와의 연결 속에서 실현된다."
            ),
            "argument": (
                "나딩스는 학생들이 행복하지 않으면서 좋은 시험 성적을 낸다고 해서 "
                "교육이 성공했다고 볼 수 없다고 주장한다. "
                "진정한 교육적 성공은 학생이 자기 자신을 이해하고, "
                "타인과 의미 있는 관계를 맺으며, 자신의 삶에 만족하는 것이다."
            ),
            "counterpoint": (
                "교육의 목적을 행복으로 설정하면 교육과정과 평가 체계를 어떻게 구성해야 하는지 "
                "구체적 방향을 제시하기 어렵다는 비판이 있다. "
                "또한 행복의 정의가 문화마다 다르기 때문에 보편적 교육 목표로 삼기 어렵다는 지적도 있다."
            ),
            "context": (
                "나딩스는 '행복과 교육'에서 신보수주의적 교육 개혁의 성취 중심 담론에 반대하며, "
                "교육의 본질적 목적을 행복으로 재설정하려 했다."
            ),
            "keywords": ["행복", "교육의 목적", "전인교육", "번성하는 삶"],
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """나딩스 키워드 데이터 입력."""
    keywords = [
        {
            "id": "noddings-kw-caring",
            "term": "배려",
            "term_en": "caring",
            "definition": (
                "나딩스 윤리학의 핵심 개념. 배려자(one-caring)가 피배려자(cared-for)를 향해 "
                "전념(engrossment)과 동기전환(motivational displacement)을 통해 맺는 관계적 도덕 경험. "
                "자연적 배려(natural caring)와 윤리적 배려(ethical caring)로 구분된다."
            ),
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "related_terms": ["전념", "동기전환", "배려자", "피배려자", "자연적 배려", "윤리적 배려"]
        },
        {
            "id": "noddings-kw-engrossment",
            "term": "전념",
            "term_en": "engrossment",
            "definition": (
                "배려의 첫 번째 핵심 요소. 배려자가 피배려자의 실재와 관심에 완전히 몰입하여 "
                "자신의 선입관을 내려놓고 피배려자의 현실을 있는 그대로 받아들이는 것. "
                "감정이입(empathy)과 유사하지만 피배려자 자체로 받아들이는 점이 다르다."
            ),
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "related_terms": ["배려", "동기전환", "배려자"]
        },
        {
            "id": "noddings-kw-motivational-displacement",
            "term": "동기전환",
            "term_en": "motivational displacement",
            "definition": (
                "배려의 두 번째 핵심 요소. 배려자의 에너지와 동기가 자신의 목적에서 "
                "피배려자의 필요와 목적으로 이동하는 것. "
                "배려자는 '내가 무엇을 원하는가'가 아니라 '이 사람에게 무엇이 필요한가'를 중심으로 행동한다."
            ),
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "related_terms": ["배려", "전념", "배려자"]
        },
        {
            "id": "noddings-kw-one-caring",
            "term": "배려자",
            "term_en": "one-caring",
            "definition": (
                "배려 관계에서 배려를 제공하는 쪽. 전념과 동기전환을 통해 피배려자를 배려하며, "
                "더 큰 도덕적 책임을 진다. 교사, 어머니 등이 대표적 사례."
            ),
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "related_terms": ["피배려자", "전념", "동기전환", "배려"]
        },
        {
            "id": "noddings-kw-cared-for",
            "term": "피배려자",
            "term_en": "cared-for",
            "definition": (
                "배려 관계에서 배려를 받는 쪽. 배려를 수용하고 인정함으로써 배려 관계를 완성시킨다. "
                "학생, 자녀 등이 대표적 사례. 피배려자의 수용이 없으면 배려 관계는 성립하지 않는다."
            ),
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "related_terms": ["배려자", "배려 관계", "수용"]
        },
        {
            "id": "noddings-kw-natural-caring",
            "term": "자연적 배려",
            "term_en": "natural caring",
            "definition": (
                "자발적·본능적으로 이루어지는 배려. 어머니가 자녀를 배려하는 것처럼 "
                "의지적 노력 없이도 자연스럽게 흘러나오는 배려. "
                "윤리적 배려의 동기와 기반이 된다."
            ),
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "related_terms": ["윤리적 배려", "배려", "윤리적 이상"]
        },
        {
            "id": "noddings-kw-ethical-caring",
            "term": "윤리적 배려",
            "term_en": "ethical caring",
            "definition": (
                "자연적 배려가 어려운 상황에서 '최선의 자아(best self)'와 '윤리적 이상(ethical ideal)'에 "
                "의지하여 의식적 노력으로 배려를 실천하는 것. "
                "'나는 배려해야 한다(I ought)'는 감각이 윤리적 배려를 작동시킨다."
            ),
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "related_terms": ["자연적 배려", "윤리적 이상", "최선의 자아"]
        },
        {
            "id": "noddings-kw-ethical-ideal",
            "term": "윤리적 이상",
            "term_en": "ethical ideal",
            "definition": (
                "'내가 최선의 배려자(best one-caring)였을 때'의 기억과 이미지로 구성되는 도덕적 준거. "
                "윤리적 배려의 동기가 되며, 도덕교육은 이 윤리적 이상을 풍요롭게 하는 과정이어야 한다."
            ),
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "related_terms": ["윤리적 배려", "자연적 배려", "최선의 자아"]
        },
        {
            "id": "noddings-kw-modeling",
            "term": "모델링",
            "term_en": "modeling",
            "definition": (
                "배려 교육의 첫 번째 방법. 교사가 배려하는 태도와 행동을 직접 보여줌으로써 "
                "학생이 배려 관계를 관찰하고 배울 수 있게 한다."
            ),
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "related_terms": ["대화", "실천", "확인", "배려 교육"]
        },
        {
            "id": "noddings-kw-dialogue",
            "term": "대화",
            "term_en": "dialogue",
            "definition": (
                "배려 교육의 두 번째 방법. 교사와 학생 간의 개방적이고 쌍방향적인 대화를 통해 "
                "서로를 이해하고 배려 관계를 심화한다. 일방적 교훈이 아닌 상호적 탐색의 대화."
            ),
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "related_terms": ["모델링", "실천", "확인", "배려 교육"]
        },
        {
            "id": "noddings-kw-practice",
            "term": "실천",
            "term_en": "practice",
            "definition": (
                "배려 교육의 세 번째 방법. 배려를 실제로 경험하고 실천할 기회를 제공한다. "
                "봉사 학습, 협동 프로젝트, 공동체 참여 등이 이에 해당한다."
            ),
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "related_terms": ["모델링", "대화", "확인", "배려 교육"]
        },
        {
            "id": "noddings-kw-confirmation",
            "term": "확인",
            "term_en": "confirmation",
            "definition": (
                "배려 교육의 네 번째 방법. 교사가 학생에게서 최선의 자아(best self)를 발견하고 "
                "그 잠재력을 긍정하고 격려한다. 학생이 더 나은 배려자가 될 수 있다는 믿음을 전달한다."
            ),
            "thinker_id": "noddings",
            "work_id": "noddings-caring",
            "related_terms": ["모델링", "대화", "실천", "윤리적 이상"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """나딩스 관련 사상 관계 데이터 입력."""
    relations = [
        {
            "from_thinker": "gilligan",
            "to_thinker": "noddings",
            "type": "influenced",
            "description": (
                "캐럴 길리건의 배려윤리는 나딩스에게 결정적 영향을 미쳤다. "
                "길리건은 '다른 목소리로(In a Different Voice, 1982)'에서 "
                "콜버그의 정의 중심 도덕발달론이 여성의 배려 중심 도덕 경험을 간과한다고 비판했다. "
                "나딩스는 이 통찰을 수용하여 배려윤리를 철학적으로 체계화하고 교육학에 적용했다."
            ),
            "evidence": "Noddings, Caring (1984), Preface and Introduction"
        },
        {
            "from_thinker": "kohlberg",
            "to_thinker": "noddings",
            "type": "criticized",
            "description": (
                "나딩스는 콜버그의 정의 중심 도덕발달론을 비판적으로 계승했다. "
                "콜버그의 도덕발달 단계론이 추상적 원리와 정의를 최고 수준의 도덕으로 설정함으로써 "
                "배려와 관계 중심의 도덕 경험을 저평가한다고 비판했다. "
                "나딩스는 정의윤리와 배려윤리가 상보적 관계에 있어야 한다고 주장했다."
            ),
            "evidence": "Noddings, Caring (1984), Chapter 2; The Challenge to Care in Schools (1992)"
        },
        {
            "from_thinker": "buber",
            "to_thinker": "noddings",
            "type": "influenced",
            "description": (
                "마틴 부버의 대화철학과 '나-너(I-Thou)' 관계 개념이 나딩스의 관계적 존재론과 "
                "배려 관계 이론에 영향을 미쳤다. "
                "부버는 인간의 근본적 존재 방식을 '나-너' 관계 속에서 찾았으며, "
                "나딩스는 이를 배려 관계의 철학적 기반으로 활용했다."
            ),
            "evidence": "Noddings, Caring (1984), Chapter 2 — Buber 직접 인용"
        },
        {
            "from_thinker": "noddings",
            "to_thinker": "gilligan",
            "type": "developed",
            "description": (
                "나딩스는 길리건의 심리학적 배려윤리를 철학적·교육학적으로 심화·발전시켰다. "
                "길리건이 도덕 심리학 연구를 통해 배려윤리의 심리적 기반을 제시했다면, "
                "나딩스는 이를 철학적 윤리 체계와 교육 이론으로 발전시켰다."
            ),
            "evidence": "Noddings, Caring (1984)"
        },
        {
            "from_thinker": "piaget",
            "to_thinker": "noddings",
            "type": "influenced",
            "description": (
                "피아제의 인지발달 이론과 도덕발달론은 나딩스의 배려교육론에 간접적 영향을 미쳤다. "
                "피아제의 협동과 상호 존중 중심 도덕교육 관점은 "
                "나딩스의 배려 관계 중심 교육론과 맥을 같이한다."
            ),
            "evidence": "나딩스 도덕교육론의 이론적 맥락"
        }
    ]

    for i, rel in enumerate(relations):
        rel_id = f"noddings-rel-{i+1:03d}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id} ({rel['from_thinker']} → {rel['to_thinker']}): {result['result']}")

    return len(relations)


def main():
    client = get_client()
    try:
        print("=== 나딩스(Nel Noddings) 데이터 입력 시작 ===\n")

        # 1. 분야 확인
        print("--- 분야(field) 확인 ---")
        ensure_field(client)
        print()

        # 2. 사상가
        print("--- 사상가(thinker) 입력 ---")
        insert_thinker(client)
        print()

        # 3. 저서
        print("--- 저서(works) 입력 ---")
        n_works = insert_works(client)
        print(f"총 {n_works}개 저서 입력 완료\n")

        # 4. 주장
        print("--- 주장(claims) 입력 ---")
        n_claims = insert_claims(client)
        print(f"총 {n_claims}개 주장 입력 완료\n")

        # 5. 키워드
        print("--- 키워드(keywords) 입력 ---")
        n_keywords = insert_keywords(client)
        print(f"총 {n_keywords}개 키워드 입력 완료\n")

        # 6. 관계
        print("--- 관계(relations) 입력 ---")
        n_relations = insert_relations(client)
        print(f"총 {n_relations}개 관계 입력 완료\n")

        print("=== 나딩스 데이터 입력 완료 ===")
        print(f"요약: 사상가 1명, 저서 {n_works}개, 주장 {n_claims}개, 키워드 {n_keywords}개, 관계 {n_relations}개")

    finally:
        close_client(client)


if __name__ == "__main__":
    main()
