"""캐롤 길리건(Carol Gilligan) 데이터를 ES에 직접 입력하는 스크립트."""

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
    """길리건 사상가 데이터 입력."""
    doc = {
        "id": "gilligan",
        "name": "캐롤 길리건",
        "name_en": "Carol Gilligan",
        "field": "moral_development",
        "era": "현대",
        "birth_year": 1936,
        "background": (
            "캐롤 길리건은 1936년 뉴욕에서 태어났다. 스워스모어 칼리지에서 문학을 전공하고 "
            "래드클리프 칼리지에서 임상심리학으로 석사를, 하버드 대학교에서 사회심리학으로 박사학위를 받았다. "
            "하버드에서 에릭 에릭슨(Erik Erikson)의 강의를 들었고, 이후 로렌스 콜버그(Lawrence Kohlberg)와 "
            "함께 도덕발달을 연구했다. 콜버그의 연구에서 여성 피험자가 남성보다 낮은 도덕발달 단계를 보이는 경향을 "
            "관찰하면서, 이 결과가 여성의 도덕적 열등함이 아니라 연구의 남성 편향에서 비롯된 것임을 깨달았다. "
            "콜버그의 연구 대상이 주로 남아(소년)였으며, 그의 이론이 남성적 도덕 목소리(정의 중심)만을 "
            "규범으로 설정했다는 비판이 그의 문제의식의 핵심이었다. "
            "1982년 「다른 목소리로(In a Different Voice)」를 출간하여 페미니스트 심리학과 "
            "배려윤리학의 창시자로 부상했다. 하버드 교육대학원 교수를 역임하고, "
            "뉴욕 대학교에서 교수로 재직했다."
        ),
        "core_philosophy": (
            "길리건 사상의 핵심은 도덕적 경험에 두 가지 서로 다른 목소리(voice)가 있다는 것이다. "
            "하나는 정의의 윤리(ethics of justice)로, 권리·공정성·보편적 원칙을 중심으로 하며 "
            "주로 남성의 도덕적 경험에서 두드러진다. "
            "다른 하나는 배려의 윤리(ethics of care)로, 관계·책임·맥락적 판단·타인에 대한 배려를 중심으로 하며 "
            "주로 여성의 도덕적 경험에서 두드러진다. "
            "길리건은 배려의 윤리가 정의의 윤리보다 열등하거나 덜 발달한 것이 아니라, "
            "콜버그의 이론이 포착하지 못한 '다른 도덕적 목소리'임을 주장했다. "
            "자아를 관계 속에서 이해하는 관계적 자아(relational self) 개념도 핵심이다. "
            "배려윤리는 추상적 원칙보다 구체적 관계와 맥락에서의 책임을 강조한다."
        ),
        "philosophical_journey": (
            "초기(1960~70년대, 콜버그와의 협업): 하버드에서 콜버그와 함께 도덕발달을 연구하면서 "
            "콜버그 이론의 남성 편향을 발견했다. 여성이 콜버그 척도에서 낮은 점수를 받는 것은 "
            "도덕적 열등함이 아니라 여성의 도덕적 지향이 다름을 보여주는 것이라고 해석하기 시작했다. "
            "중기(1982년, 다른 목소리 출간): 「다른 목소리로」를 출간하여 배려의 윤리를 체계화했다. "
            "임신 중절 결정 연구, 하인츠 딜레마에서의 에이미 분석 등을 통해 "
            "여성의 도덕 경험을 새롭게 조명했다. "
            "후기(1990년대 이후, 관계 이론): 나이나 브라운(Lyn Mikel Brown)과 공동 연구를 통해 "
            "사춘기 소녀의 도덕 발달을 탐구했다(「만남의 지점」, 1992). "
            "관계적 자아와 연결(connection)의 심리학을 발전시켰다. "
            "배려윤리가 개인의 도덕뿐 아니라 정치, 사회, 교육 전반에 적용될 수 있음을 강조했다."
        ),
        "keywords": [
            "배려윤리",
            "다른 목소리",
            "정의 vs 배려",
            "관계적 자아",
            "비폭력의 도덕성",
            "맥락 의존적 판단",
            "배려의 도덕 발달",
            "콜버그 비판",
            "페미니스트 윤리",
            "책임의 윤리",
            "하인츠 딜레마",
            "자기희생적 선"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="gilligan", document=doc)
    print(f"[thinker] gilligan: {result['result']}")
    return result


def insert_works(client):
    """길리건 저서 데이터 입력."""
    works = [
        {
            "id": "gilligan-in-a-different-voice",
            "thinker_id": "gilligan",
            "title": "다른 목소리로",
            "title_original": "In a Different Voice: Psychological Theory and Women's Development",
            "year": 1982,
            "significance": (
                "길리건의 핵심 저서이자 배려윤리학의 출발점. "
                "콜버그의 도덕발달 단계론이 남성의 도덕 경험만을 규범으로 삼아 "
                "여성의 도덕적 목소리를 열등하거나 덜 발달한 것으로 오해했음을 비판했다. "
                "임신 중절 결정에 관한 여성 면접 연구, 하인츠 딜레마에서 에이미의 응답 분석을 통해 "
                "배려의 윤리를 체계화했다. "
                "정의 중심의 도덕 이론에 대한 대안으로 배려와 관계 중심의 도덕성을 제시하였으며, "
                "페미니스트 윤리학과 도덕심리학에 혁명적 영향을 미쳤다."
            ),
            "key_concepts": [
                "배려의 윤리", "정의의 윤리", "다른 목소리",
                "관계적 자아", "배려의 도덕 발달 3단계",
                "콜버그 비판", "하인츠 딜레마", "에이미의 응답"
            ]
        },
        {
            "id": "gilligan-meeting-at-crossroads",
            "thinker_id": "gilligan",
            "title": "만남의 지점",
            "title_original": "Meeting at the Crossroads: Women's Psychology and Girls' Development",
            "year": 1992,
            "significance": (
                "린 미켈 브라운(Lyn Mikel Brown)과의 공동 저서로, "
                "사춘기 소녀들의 심리적 발달과 도덕 발달을 탐구했다. "
                "소녀들이 사춘기에 자신의 목소리와 지식을 잃어버리는 '침묵의 위기'를 포착했다. "
                "여성의 심리적 발달이 관계와 연결의 유지라는 관점에서 이루어짐을 보여주었다."
            ),
            "key_concepts": [
                "침묵의 위기", "소녀의 도덕 발달", "관계와 연결", "여성 심리학"
            ]
        },
        {
            "id": "gilligan-mapping-moral-domain",
            "thinker_id": "gilligan",
            "title": "도덕 영역의 지도 그리기",
            "title_original": "Mapping the Moral Domain",
            "year": 1988,
            "significance": (
                "길리건이 공동 편집한 논문집으로, 배려윤리의 이론적 토대를 다양한 관점에서 확장했다. "
                "배려와 정의의 두 도덕적 지향이 성별 차이를 넘어 "
                "일반적인 도덕 심리학의 두 축임을 보다 명확히 논증했다."
            ),
            "key_concepts": [
                "도덕적 지향", "배려와 정의", "도덕 심리학", "성별 차이"
            ]
        },
        {
            "id": "gilligan-birth-of-pleasure",
            "thinker_id": "gilligan",
            "title": "기쁨의 탄생",
            "title_original": "The Birth of Pleasure",
            "year": 2002,
            "significance": (
                "심리학과 문학, 신화를 결합하여 인간의 관계와 사랑, 상실을 탐구한 저서. "
                "가부장제가 어떻게 남녀 모두의 감정적 연결을 억압하는지 분석했다. "
                "배려와 연결의 윤리가 개인의 심리적 건강과 연결됨을 보여주었다."
            ),
            "key_concepts": [
                "관계와 사랑", "가부장제 비판", "심리적 연결", "배려윤리의 확장"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """길리건 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 콜버그 도덕발달론의 남성 편향 비판
        {
            "id": "gilligan-claim-001",
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "source_detail": "In a Different Voice, Chapter 1: Woman's Place in Man's Life Cycle",
            "claim": (
                "콜버그의 도덕발달 단계론은 남성을 연구 대상으로 구성되었기 때문에 "
                "구조적으로 남성 편향을 가지며, 여성의 도덕적 경험을 적절히 포착하지 못한다. "
                "콜버그의 척도에서 여성이 낮은 단계(3단계)에 머무는 것은 "
                "여성의 도덕적 열등함이 아니라, 여성의 도덕적 목소리가 다르기 때문이다."
            ),
            "original_text": (
                "The repeated finding of these studies is that the girls are deficient in moral development "
                "in comparison to the boys... Kohlberg's six stages are not stages of development "
                "but rather stages in a particular conception of moral development."
            ),
            "explanation": (
                "콜버그는 하버드 대학 남학생 84명을 추적 연구하여 도덕발달 6단계론을 구성했다. "
                "여성은 이 연구에서 제외되었거나 소수에 불과했다. "
                "콜버그의 척도를 여성에게 적용하면 여성은 주로 3단계(대인관계 조화 지향)에 머무는 경향을 보이는데, "
                "콜버그 이론에서 3단계는 인습적 수준으로 비교적 낮은 단계이다. "
                "길리건은 이것이 여성이 인간관계와 배려를 중시하는 도덕 지향을 가지기 때문이며, "
                "이를 낮은 발달로 판단하는 것은 연구의 남성 편향 때문이라고 주장한다."
            ),
            "argument": (
                "(1) 콜버그의 연구 대상이 남성 위주였으므로 이론 자체가 남성적 도덕 경험을 반영한다. "
                "(2) 정의·권리·보편 원칙 중심의 도덕 발달 모델은 여성이 중시하는 "
                "관계·배려·맥락 중심의 도덕 경험을 과소평가한다. "
                "(3) 따라서 여성이 콜버그 척도에서 낮은 점수를 받는 것은 발달의 실패가 아니라 "
                "다른 도덕적 지향의 표현이다."
            ),
            "counterpoint": (
                "콜버그와 그의 동료들은 후속 연구에서 성별 차이가 일관되게 나타나지 않으며, "
                "교육 수준과 사회경제적 요인이 더 중요한 변수라고 반론했다. "
                "워커(Walker, 1984) 등의 메타분석 연구는 성별에 따른 도덕발달 차이가 통계적으로 "
                "유의미하지 않을 수 있음을 보였다. "
                "일부 페미니스트 철학자들은 길리건의 접근이 여성과 배려를 연결함으로써 "
                "오히려 성별 고정관념을 강화할 수 있다고 비판했다."
            ),
            "context": (
                "길리건은 1970년대 콜버그의 연구조교로 일하면서 여성의 도덕 발달에 관한 "
                "독립적 연구를 시작했다. 임신 중절 결정 연구에서 여성들이 보이는 "
                "도덕적 추론 방식이 콜버그의 틀로는 포착되지 않음을 발견했다."
            ),
            "keywords": ["콜버그 비판", "남성 편향", "배려의 윤리", "도덕발달론"],
            "verified": False
        },
        # CLAIM-002: 정의의 윤리 vs 배려의 윤리
        {
            "id": "gilligan-claim-002",
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "source_detail": "In a Different Voice, Chapter 2: Images of Relationship",
            "claim": (
                "도덕에는 두 가지 서로 다른 목소리(voice)가 있다. "
                "하나는 정의의 윤리(ethics of justice)로, 권리·공정성·보편적 원칙·자율성을 강조한다. "
                "다른 하나는 배려의 윤리(ethics of care)로, 관계·책임·맥락적 판단·타인에 대한 배려를 강조한다. "
                "이 두 목소리는 도덕을 바라보는 서로 다른 관점이며, "
                "어느 하나가 다른 하나보다 우월하거나 더 발달한 것이 아니다."
            ),
            "original_text": (
                "The moral imperative that emerges repeatedly in interviews with women is an injunction "
                "to care, a responsibility to discern and alleviate the 'real and recognizable trouble' "
                "of this world. For men, the moral imperative appears rather as an injunction to respect "
                "the rights of others and thus to protect from interference the rights to life and "
                "self-fulfillment."
            ),
            "explanation": (
                "정의의 윤리: 도덕을 권리와 원칙의 문제로 본다. 자율적·독립적 개인이 공정한 원칙에 따라 "
                "서로의 권리를 존중해야 한다고 강조한다. 콜버그의 도덕발달론이 대표적이다. "
                "배려의 윤리: 도덕을 관계와 책임의 문제로 본다. 구체적 관계 속에서 "
                "타인의 필요와 고통에 응답할 책임을 강조한다. 맥락에 따른 판단을 중시한다. "
                "길리건은 두 윤리가 상호 보완적이라고 보며, 성숙한 도덕 발달은 "
                "두 관점 모두를 통합하는 것이라고 주장한다."
            ),
            "argument": (
                "(1) 여성 면접 연구에서 여성들은 도덕적 문제를 권리 충돌로 보기보다는 "
                "관계와 책임의 관점에서 이해하는 경향을 보였다. "
                "(2) 남성 면접 연구에서 남성들은 도덕 문제를 주로 권리와 공정성의 관점에서 접근했다. "
                "(3) 두 집단의 차이는 발달 수준의 차이가 아니라 도덕적 지향의 차이이다."
            ),
            "counterpoint": (
                "길리건 자신도 후기 저작에서 두 윤리가 젠더의 차이가 아니라 "
                "모든 사람에게 존재하는 두 가지 도덕 지향임을 명확히 했다. "
                "나딩스(Noddings)는 배려윤리를 교육 이론으로 더욱 정교화했다. "
                "일부 비판자들은 두 윤리의 구분이 지나치게 단순화되었다고 지적한다."
            ),
            "context": (
                "길리건은 '다른 목소리'가 반드시 여성의 목소리가 아님을 강조했다. "
                "그것은 도덕적 경험의 다양성을 포착하는 개념이며, "
                "두 윤리는 젠더 차이가 아니라 도덕적 지향의 차이를 나타낸다."
            ),
            "keywords": ["정의 vs 배려", "다른 목소리", "배려의 윤리", "관계 중심 도덕성"],
            "verified": False
        },
        # CLAIM-003: 배려의 도덕 발달 3단계 — 자기 생존
        {
            "id": "gilligan-claim-003",
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "source_detail": "In a Different Voice, Chapter 3: Concepts of Self and Morality",
            "claim": (
                "배려의 도덕 발달 1단계는 '자기 생존(survival)' 지향으로, "
                "오직 자신의 필요와 생존에만 초점을 맞춘다. "
                "이 단계에서 자아는 고립되어 있으며, 타인에 대한 고려가 결여되어 있다. "
                "이기적이고 자기중심적인 도덕 판단이 특징이다."
            ),
            "original_text": None,
            "explanation": (
                "길리건은 임신 중절 결정을 고민하는 여성들과의 면접 연구를 통해 "
                "배려윤리의 도덕 발달 3단계를 도출했다. "
                "1단계(자기 생존): 자신의 필요를 최우선으로 삼는다. 도덕적으로 가장 미성숙한 단계. "
                "타인은 자신의 생존을 위한 수단으로만 여겨질 수 있다. "
                "첫 번째 전환: 자기중심성에서 타인에 대한 책임으로의 이동."
            ),
            "argument": (
                "(1) 임신 중절을 고민하는 여성들의 초기 응답에서 많은 여성들이 "
                "자신의 상황과 필요에서만 문제를 바라보는 경향을 보였다. "
                "(2) 이는 콜버그의 1단계(처벌과 복종 지향)와 유사하지만, "
                "자기 생존의 관점에서 이해된다는 점이 다르다."
            ),
            "counterpoint": (
                "길리건의 배려 도덕 발달 단계론은 임신 중절이라는 특수한 상황을 연구 맥락으로 삼았기 때문에 "
                "일반화 가능성에 한계가 있다는 비판이 있다. "
                "남성의 배려 발달을 포착하지 못한다는 지적도 있다."
            ),
            "context": (
                "길리건은 임신 중절 결정을 앞두고 상담 기관을 방문한 29명의 여성과 면접하고, "
                "이후 결정을 내린 21명과 추적 면접을 실시했다. "
                "이 연구가 배려 도덕 발달 3단계론의 경험적 기반이 되었다."
            ),
            "keywords": ["배려의 도덕 발달", "자기 생존", "도덕 발달 단계", "배려윤리"],
            "verified": False
        },
        # CLAIM-004: 배려의 도덕 발달 3단계 — 자기희생적 선
        {
            "id": "gilligan-claim-004",
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "source_detail": "In a Different Voice, Chapter 3: Concepts of Self and Morality",
            "claim": (
                "배려의 도덕 발달 2단계는 '자기희생적 선(goodness as self-sacrifice)' 단계로, "
                "자신의 필요보다 타인의 필요를 우선시하며, 자기희생을 도덕적 선으로 간주한다. "
                "이 단계에서 도덕적 선함은 다른 사람을 돌보는 것이며, "
                "자신의 필요를 주장하는 것은 이기적이라고 여긴다."
            ),
            "original_text": None,
            "explanation": (
                "2단계(자기희생적 선): 첫 번째 전환 이후 나타나는 단계. "
                "타인에 대한 책임과 배려가 도덕의 중심이 되지만, "
                "이는 자아의 포기를 수반한다. "
                "이 단계의 여성은 타인을 위해 자신의 욕구와 필요를 억압하는 것을 '선함'으로 이해한다. "
                "자신을 위한 주장은 이기심으로 여겨져 죄책감을 유발한다. "
                "두 번째 전환: 자기희생에서 자신과 타인 모두를 고려하는 배려로의 이동."
            ),
            "argument": (
                "(1) 면접 여성들 중 많은 이들이 '좋은 여자'란 희생적이고 양보하는 존재라는 "
                "사회적 기대를 내면화한 상태였다. "
                "(2) 이 단계는 '타인 배려'가 심화된 것처럼 보이지만, "
                "실제로는 자신을 지우는 방식으로 관계를 유지하는 것이다. "
                "(3) 이 단계는 여성에게 강요된 사회적 역할(돌봄 제공자)과 연결된다."
            ),
            "counterpoint": (
                "사회학자들은 자기희생이 개인의 도덕 발달 단계가 아니라 "
                "여성에게 부과된 사회적 압력의 결과일 수 있다고 지적한다. "
                "이 단계는 가부장제적 여성 역할 기대의 내면화를 반영한다."
            ),
            "context": (
                "면접 연구에서 많은 여성들이 임신 중절 결정에서 자신보다 "
                "파트너, 가족, 태아의 필요를 먼저 생각했다. "
                "이는 자기희생적 선의 전형적 표현이다."
            ),
            "keywords": ["배려의 도덕 발달", "자기희생적 선", "타인 배려", "도덕 발달 단계"],
            "verified": False
        },
        # CLAIM-005: 배려의 도덕 발달 3단계 — 비폭력의 도덕성
        {
            "id": "gilligan-claim-005",
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "source_detail": "In a Different Voice, Chapter 3: Concepts of Self and Morality",
            "claim": (
                "배려의 도덕 발달 최고 단계인 3단계는 '비폭력의 도덕성(morality of nonviolence)' 단계로, "
                "자신과 타인 모두에 대한 배려를 통합한다. "
                "이 단계에서는 자기 자신도 배려의 대상에 포함되며, "
                "자신을 희생하는 것이 아니라 자신과 타인 모두의 필요를 균형 있게 고려한다. "
                "도덕은 해를 끼치지 않음(nonviolence)과 보편적 배려의 원칙으로 이해된다."
            ),
            "original_text": (
                "The third perspective focuses on the dynamics of relationships and dissolves "
                "the tension between selfishness and responsibility through a new understanding "
                "of the interconnection between other and self... care becomes the self-chosen "
                "principle of a judgment that remains psychological in its concern with relationships "
                "and response but becomes universal in its condemnation of exploitation and hurt."
            ),
            "explanation": (
                "3단계(비폭력의 도덕성): 두 번째 전환 이후 나타나는 성숙한 배려 도덕성. "
                "자신과 타인 모두를 배려해야 한다는 원칙에 도달한다. "
                "자신의 필요를 억압하지 않으면서도 타인에 대한 책임을 다하는 균형을 추구한다. "
                "해를 끼치지 않는 것(nonviolence)이 보편적 도덕 원칙으로 작용한다. "
                "이 단계에서는 '좋은 여자' 역할이 아닌 자신의 선택으로서 배려를 실천한다."
            ),
            "argument": (
                "(1) 도덕적으로 성숙한 여성들은 임신 중절 결정에서 자신의 필요와 타인의 필요를 "
                "동등하게 고려하는 방식으로 사고했다. "
                "(2) '배려'가 사회적 압력이 아닌 자아의 자율적 선택이 된다. "
                "(3) 이 단계의 도덕적 원칙은 '어떤 존재도 해쳐서는 안 된다'는 비폭력의 원리이다."
            ),
            "counterpoint": (
                "비폭력의 도덕성이 구체적 상황에서 어떻게 적용되는지 명확하지 않다는 비판이 있다. "
                "자신과 타인의 필요가 충돌할 때의 해결책이 충분히 제시되지 않는다는 지적도 있다."
            ),
            "context": (
                "이 3단계는 도덕 발달의 선형적 단계이기도 하지만, "
                "성숙한 도덕 판단의 이상적 형태를 나타내기도 한다. "
                "길리건은 콜버그의 단계론과 달리 이 단계를 보편적 원칙의 적용이 아닌 "
                "관계와 배려의 심화로 이해한다."
            ),
            "keywords": ["비폭력의 도덕성", "배려의 도덕 발달", "자기와 타인 배려", "보편적 배려"],
            "verified": False
        },
        # CLAIM-006: 관계적 자아
        {
            "id": "gilligan-claim-006",
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "source_detail": "In a Different Voice, Chapter 1, 2",
            "claim": (
                "서구 윤리학의 전통은 자아를 독립적·자율적·분리된 개인으로 이해하지만, "
                "이는 인간 존재의 한 면만을 포착한다. "
                "길리건은 자아가 관계 속에서 형성되고 유지되는 '관계적 자아(relational self)'임을 강조한다. "
                "인간은 분리(separation)보다 연결(connection)을 통해 정체성을 발달시키며, "
                "관계와 상호 의존이 자아의 핵심이다."
            ),
            "original_text": (
                "The moral problem arises from conflicting responsibilities rather than from "
                "competing rights and requires for its resolution a mode of thinking that is "
                "contextual and narrative rather than formal and abstract."
            ),
            "explanation": (
                "관계적 자아(relational self): 자아는 타인과의 관계에서 구성된다. "
                "관계의 유지와 발전이 자아 발달의 핵심이다. "
                "이는 자유주의 전통의 독립적 자아 개념과 대립된다. "
                "길리건의 관점에서 도덕 문제는 '권리 충돌'이 아니라 '책임 충돌'로 이해되며, "
                "도덕적 해결은 추상적 원칙보다 맥락과 서사적 이해를 통해 이루어진다."
            ),
            "argument": (
                "(1) 여성 심리학 연구에서 여성은 정체성을 관계 속에서 규정하는 경향이 있다. "
                "(2) 남성의 심리적 발달 모델(분리와 독립)은 보편적 발달 모델이 아니라 "
                "남성적 발달 모델이다. "
                "(3) 관계와 연결이 자아의 핵심이라면, "
                "타인에 대한 배려는 자아의 포기가 아니라 자아의 실현이다."
            ),
            "counterpoint": (
                "관계적 자아 개념이 여성 정체성을 관계에만 묶어둘 수 있다는 비판이 있다. "
                "자율성과 독립성도 중요한 인간적 가치임을 간과할 수 있다는 지적도 있다. "
                "자아를 관계로만 정의하면 억압적 관계에서도 그 관계를 유지하도록 압박할 수 있다."
            ),
            "context": (
                "에릭슨, 피아제, 콜버그 등 서구 발달심리학의 전통은 "
                "분리와 독립(자율성)을 심리적 발달의 이상으로 제시했다. "
                "길리건은 이 전통이 남성의 발달 경험을 보편으로 오해하고 있다고 비판했다."
            ),
            "keywords": ["관계적 자아", "연결", "분리 vs 연결", "자율성 비판"],
            "verified": False
        },
        # CLAIM-007: 하인츠 딜레마에서 에이미의 응답 분석
        {
            "id": "gilligan-claim-007",
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "source_detail": "In a Different Voice, Chapter 2: Images of Relationship",
            "claim": (
                "콜버그의 하인츠 딜레마에서 에이미(Amy)의 응답은 제이크(Jake)의 응답보다 "
                "도덕적으로 낮은 수준이 아니라, 다른 도덕적 관점(배려의 윤리)을 표현한다. "
                "에이미는 문제를 권리 충돌이 아니라 관계와 소통의 문제로 이해하며, "
                "약사와 하인츠가 대화와 협력으로 해결책을 찾아야 한다고 제안한다."
            ),
            "original_text": (
                "Amy... sees a world composed of relationships rather than of people standing alone, "
                "a world that coheres through human connection rather than through systems of rules. "
                "She finds the puzzle in the dilemma to lie in the failure of the druggist to respond "
                "to the wife's need, and in the threat that Heinz's thieving might have on the "
                "relationship between them."
            ),
            "explanation": (
                "하인츠 딜레마: 아내를 구하기 위해 약을 훔쳐야 하는가? "
                "제이크(11세 소년): 생명권이 재산권보다 중요하므로 훔쳐야 한다. 권리와 원칙 중심의 답변. "
                "에이미(11세 소녀): 훔치면 약사가 화가 나서 결국 상황이 더 나빠질 수 있다. "
                "약사와 대화로 해결책을 찾아야 한다. 관계와 소통 중심의 답변. "
                "콜버그 기준으로는 에이미가 낮은 단계로 평가되지만, "
                "길리건은 에이미의 응답이 더 성숙한 배려의 도덕성을 보여준다고 주장한다."
            ),
            "argument": (
                "(1) 제이크는 딜레마를 추상적 권리의 충돌로 보고 논리적으로 해결하려 한다. "
                "(2) 에이미는 딜레마를 관계의 위기로 보고 소통과 협력으로 해결하려 한다. "
                "(3) 에이미의 접근은 '실패한 논리'가 아니라 '다른 도덕적 목소리'이며, "
                "관계와 배려의 윤리를 표현한다."
            ),
            "counterpoint": (
                "에이미의 응답이 비현실적(약사가 대화에 응할지 불확실)이라는 비판이 있다. "
                "콜버그 지지자들은 에이미의 응답이 딜레마 자체에 직접 답하지 않는 "
                "회피적 사고를 보인다고 반론했다."
            ),
            "context": (
                "이 분석은 「다른 목소리로」의 핵심 사례 연구로, "
                "길리건이 콜버그의 도덕발달 이론을 비판하는 가장 구체적이고 설득력 있는 사례이다."
            ),
            "keywords": ["하인츠 딜레마", "에이미의 응답", "배려의 윤리", "관계 중심 도덕성"],
            "verified": False
        },
        # CLAIM-008: 책임과 관계의 도덕성
        {
            "id": "gilligan-claim-008",
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "source_detail": "In a Different Voice, Chapter 3, 4",
            "claim": (
                "배려의 윤리는 도덕을 권리(rights)가 아니라 책임(responsibility)과 응답성(responsiveness)의 "
                "관점에서 이해한다. "
                "도덕적 선함은 추상적 원칙에 따른 행위가 아니라, "
                "구체적 관계 속에서 타인의 필요와 고통에 응답하는 것이다. "
                "책임은 관계 속에서 발생하며, 분리된 자아에게 부과되는 외적 의무가 아니다."
            ),
            "original_text": None,
            "explanation": (
                "권리의 윤리(정의의 윤리): 독립적 개인들이 서로의 권리를 침해하지 않아야 한다는 의무론적 도덕. "
                "책임의 윤리(배려의 윤리): 구체적 관계 속에서 타인의 필요에 응답해야 한다는 관계적 도덕. "
                "책임(responsibility)의 어원은 '응답하다(respond)'와 관련이 있다. "
                "길리건에게 도덕적 책임은 관계 속에서 타인에게 응답하는 것이다."
            ),
            "argument": (
                "(1) 여성들의 도덕적 서술에서 '책임'과 '관계'는 핵심 키워드였다. "
                "(2) 여성들은 도덕 문제를 '누구의 권리가 더 중요한가'보다 "
                "'이 관계에서 나의 책임은 무엇인가'로 이해했다. "
                "(3) 이는 칸트적 의무론이나 공리주의와 다른 도덕 이해이다."
            ),
            "counterpoint": (
                "책임 중심 윤리가 책임의 범위와 한계를 명확히 하지 못한다는 비판이 있다. "
                "누구에게, 어디까지 책임이 있는지가 불분명하다. "
                "보편적 원칙 없이 관계 중심으로만 판단하면 '내 집단'의 이익을 위해 "
                "'외부인'을 배제하는 윤리적 편협함이 생길 수 있다."
            ),
            "context": (
                "길리건의 책임 윤리는 레비나스(Emmanuel Levinas)의 타자 철학, "
                "나딩스의 배려교육론과 공명하며, 페미니스트 정치철학에서도 중요하게 다루어진다."
            ),
            "keywords": ["책임의 윤리", "응답성", "관계 중심 도덕성", "배려의 윤리"],
            "verified": False
        },
        # CLAIM-009: 맥락 의존적 도덕 판단
        {
            "id": "gilligan-claim-009",
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "source_detail": "In a Different Voice, Chapter 2, 3",
            "claim": (
                "도덕적 판단은 보편적·추상적 원칙의 적용이 아니라 "
                "구체적 맥락(context), 관계, 서사(narrative)를 고려하는 방식으로 이루어져야 한다. "
                "도덕 문제는 추상적 딜레마가 아니라 실제 삶의 맥락 속에서 이해되어야 하며, "
                "맥락에 따라 동일한 행위의 도덕적 의미가 달라질 수 있다."
            ),
            "original_text": (
                "The moral problem arises from conflicting responsibilities rather than from competing rights "
                "and requires for its resolution a mode of thinking that is contextual and narrative "
                "rather than formal and abstract."
            ),
            "explanation": (
                "맥락 의존적 판단: 도덕적 상황은 추상적 원칙을 기계적으로 적용할 수 없는 "
                "복잡한 관계와 역사를 가진 구체적 상황이다. "
                "서사적 이해: 도덕 문제를 이해하기 위해서는 관련된 사람들의 관계, 역사, "
                "맥락을 서사적으로 파악해야 한다. "
                "이는 원칙 중심의 '포말 윤리(formal ethics)'에 대한 비판이다."
            ),
            "argument": (
                "(1) 임신 중절 결정 연구에서 여성들은 자신의 구체적 상황과 관계를 "
                "상세히 고려하여 판단을 내렸다. "
                "(2) 동일한 상황에서도 관계의 맥락에 따라 도덕적으로 적합한 행위가 달라진다. "
                "(3) 콜버그 방식의 가상적 딜레마는 실제 삶의 복잡성을 단순화한다."
            ),
            "counterpoint": (
                "맥락 의존적 판단이 도덕적 상대주의로 흐를 수 있다는 비판이 있다. "
                "맥락을 지나치게 강조하면 보편적 도덕 기준을 잃어버릴 수 있다. "
                "길리건은 비폭력이라는 보편적 원칙으로 이 한계를 보완하려 했다."
            ),
            "context": (
                "길리건의 맥락주의는 아리스토텔레스의 실천적 지혜(phronesis)와 연결되며, "
                "현대 덕 윤리학과 공명한다. "
                "나딩스의 배려 윤리도 관계의 구체성과 맥락성을 강조한다."
            ),
            "keywords": ["맥락 의존적 판단", "서사적 이해", "구체적 맥락", "배려의 윤리"],
            "verified": False
        },
        # CLAIM-010: 여성의 도덕 경험 재평가
        {
            "id": "gilligan-claim-010",
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "source_detail": "In a Different Voice, Introduction and Chapter 1",
            "claim": (
                "서구 심리학과 윤리학은 여성의 도덕적 경험과 목소리를 일관되게 주변화하거나 "
                "열등한 것으로 평가해 왔다. "
                "길리건은 여성의 도덕적 경험을 남성의 기준으로 판단하는 것을 거부하고, "
                "여성의 도덕적 목소리가 지닌 독자적 가치와 의미를 재평가할 것을 주장한다."
            ),
            "original_text": (
                "The disparity between women's experience and the representation of human development, "
                "noted throughout the psychological literature, has generally been seen to signify "
                "a problem in women's development. Instead, I begin with women's experience "
                "as a starting point for a new theory of moral development."
            ),
            "explanation": (
                "심리학 역사에서 여성의 도덕 발달은 남성을 기준으로 평가되어 왔다. "
                "프로이트는 여성이 '초자아(superego)'가 약하다고 했고, "
                "콜버그는 여성이 도덕발달에서 낮은 단계에 머문다고 했다. "
                "길리건은 이런 판단이 여성의 열등함이 아니라 연구의 남성 중심성을 반영한다고 주장한다. "
                "여성의 도덕 경험을 출발점으로 삼으면 배려윤리라는 새로운 도덕 이론이 출현한다."
            ),
            "argument": (
                "(1) 심리학 역사에서 여성은 연구 대상에서 배제되거나 "
                "남성 규범에서 벗어난 '비정상'으로 다루어졌다. "
                "(2) 여성의 도덕 발달 특성(관계·배려 중심)은 약점이 아니라 "
                "다른 도덕적 지향의 표현이다. "
                "(3) 여성의 도덕 경험을 진지하게 연구하면 도덕심리학의 이론적 지평이 확장된다."
            ),
            "counterpoint": (
                "길리건이 여성을 배려와 연결하고 남성을 정의와 연결함으로써 "
                "오히려 성별 이분법을 강화한다는 비판이 있다. "
                "오늘날 많은 연구자들은 배려와 정의 모두 젠더와 무관하게 인간 보편의 도덕 지향이라고 본다."
            ),
            "context": (
                "1980년대 페미니즘 제2물결이 학문의 남성 중심성을 비판하던 시기에 "
                "길리건의 연구는 페미니스트 심리학과 윤리학에 결정적 기여를 했다."
            ),
            "keywords": ["여성의 도덕 경험", "페미니스트 윤리", "콜버그 비판", "배려의 윤리"],
            "verified": False
        },
        # CLAIM-011: 배려윤리와 도덕교육
        {
            "id": "gilligan-claim-011",
            "thinker_id": "gilligan",
            "work_id": "gilligan-mapping-moral-domain",
            "source_detail": "Mapping the Moral Domain",
            "claim": (
                "도덕교육은 정의의 원칙을 가르치는 것뿐 아니라 배려의 능력을 길러야 한다. "
                "배려 능력은 타인의 필요를 감지하고, 감정이입하며, 관계 속에서 책임감 있게 "
                "행동하는 능력이다. "
                "학교 교육은 정의 중심의 도덕 추론 교육에 치우쳐 배려의 도덕성을 경시하는 경향이 있다."
            ),
            "original_text": None,
            "explanation": (
                "길리건의 배려윤리는 도덕교육 분야에 중요한 함의를 갖는다. "
                "전통적 도덕교육은 도덕 추론(moral reasoning)이나 도덕 원칙의 교육에 초점을 맞췄다. "
                "배려윤리적 도덕교육은 공감, 관계적 감수성, 책임감의 발달을 강조한다. "
                "나딩스(Nel Noddings)는 길리건의 이론을 발전시켜 배려 중심의 도덕교육론을 체계화했다."
            ),
            "argument": (
                "(1) 도덕적 삶은 원칙 적용만이 아니라 구체적 관계에서의 배려 실천을 포함한다. "
                "(2) 배려 능력은 가르칠 수 있고, 학교 환경이 배려 능력 발달에 중요한 역할을 한다. "
                "(3) 학교가 배려 관계를 모델링하고 배려 실천의 장이 되어야 한다."
            ),
            "counterpoint": (
                "배려 능력 교육의 구체적 방법론이 충분히 발전되지 않았다는 비판이 있다. "
                "나딩스가 이 영역을 더욱 구체적으로 발전시켰다."
            ),
            "context": (
                "배려윤리의 도덕교육론은 임용시험에서 길리건과 나딩스를 함께 다루는 이유이기도 하다. "
                "두 이론가는 배려윤리의 이론적 측면(길리건)과 교육적 적용(나딩스)으로 나뉜다."
            ),
            "keywords": ["배려 능력", "도덕교육", "배려의 윤리", "관계적 감수성"],
            "verified": False
        },
        # CLAIM-012: 두 도덕적 지향의 통합
        {
            "id": "gilligan-claim-012",
            "thinker_id": "gilligan",
            "work_id": "gilligan-mapping-moral-domain",
            "source_detail": "Mapping the Moral Domain",
            "claim": (
                "정의의 윤리와 배려의 윤리는 서로 배타적이 아니라 상호 보완적이다. "
                "성숙한 도덕 발달은 두 관점을 통합하는 능력을 포함한다. "
                "정의는 공정성과 평등의 관점에서 배려를 교정하고, "
                "배려는 추상적 정의에 인간적 관계의 온기를 더한다."
            ),
            "original_text": None,
            "explanation": (
                "길리건은 후기 저작에서 배려와 정의의 대립보다 통합을 강조했다. "
                "두 관점은 도덕의 서로 다른 측면을 포착한다. "
                "정의의 윤리: 공정성, 보편성, 권리의 관점. "
                "배려의 윤리: 관계, 맥락, 책임의 관점. "
                "성숙한 도덕 판단은 두 관점을 상황에 따라 적절히 활용한다."
            ),
            "argument": (
                "(1) 현실의 도덕 문제는 권리와 배려 모두를 고려해야 할 경우가 많다. "
                "(2) 정의만 강조하면 관계의 맥락을 무시하는 차가운 도덕이 된다. "
                "(3) 배려만 강조하면 보편적 기준 없이 편향적 배려(내 집단 중심)가 될 수 있다."
            ),
            "counterpoint": (
                "두 윤리의 통합이 어떻게 이루어지는지 구체적 방법론이 충분하지 않다는 지적이 있다. "
                "어떤 상황에서 정의가 우선하고 어떤 상황에서 배려가 우선하는지 불명확하다."
            ),
            "context": (
                "길리건의 후기 입장은 초기의 이분법적 성별 차이 강조에서 벗어나 "
                "두 도덕 지향이 모든 인간에게 존재하는 보편적 도덕 역량임을 강조하는 방향으로 발전했다."
            ),
            "keywords": ["정의와 배려의 통합", "도덕 발달", "상호 보완", "성숙한 도덕성"],
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """길리건 핵심 키워드 데이터 입력."""
    keywords = [
        {
            "id": "kw-gilligan-ethics-of-care",
            "term": "배려윤리",
            "term_en": "ethics of care",
            "definition": (
                "캐롤 길리건이 제창한 도덕 이론으로, 추상적 원칙과 권리 중심의 윤리와 달리 "
                "구체적 관계, 맥락, 타인에 대한 배려와 책임을 도덕의 중심에 놓는 윤리 이론. "
                "콜버그의 정의 중심 도덕발달론에 대한 비판과 대안으로 제시되었다. "
                "인간은 상호 의존적 관계 속에서 살며, 도덕은 이 관계에서의 배려와 응답성을 "
                "핵심으로 한다고 주장한다. "
                "나딩스가 이를 교육론으로 발전시켰다."
            ),
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "related_terms": ["다른 목소리", "정의의 윤리", "관계적 자아", "책임의 윤리", "나딩스"]
        },
        {
            "id": "kw-gilligan-different-voice",
            "term": "다른 목소리",
            "term_en": "different voice",
            "definition": (
                "길리건이 제시한 개념으로, 주류 도덕심리학(콜버그)이 포착하지 못한 "
                "관계·배려·맥락 중심의 도덕적 목소리를 가리킨다. "
                "이 목소리는 여성에게만 특유한 것이 아니라, 도덕 경험의 두 지향 중 하나로 "
                "성별과 무관하게 모든 인간에게서 발견될 수 있다. "
                "서구 도덕철학이 정의의 목소리만을 도덕의 규범으로 삼은 것을 비판하는 개념이다."
            ),
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "related_terms": ["배려윤리", "정의의 윤리", "콜버그 비판", "도덕적 목소리"]
        },
        {
            "id": "kw-gilligan-justice-vs-care",
            "term": "정의 vs 배려",
            "term_en": "justice vs care",
            "definition": (
                "길리건이 제시한 두 가지 도덕적 지향. "
                "정의의 윤리(ethics of justice): 공정성, 권리, 보편적 원칙, 자율성 중심. 추상적·형식적 도덕 추론. "
                "배려의 윤리(ethics of care): 관계, 책임, 맥락적 판단, 응답성 중심. 구체적·서사적 도덕 이해. "
                "두 지향은 어느 하나가 우월한 것이 아니라 상호 보완적인 도덕의 두 관점이다."
            ),
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "related_terms": ["배려윤리", "다른 목소리", "도덕적 지향", "맥락 의존적 판단"]
        },
        {
            "id": "kw-gilligan-relational-self",
            "term": "관계적 자아",
            "term_en": "relational self",
            "definition": (
                "길리건이 강조하는 자아 개념으로, 자아는 고립된 독립 개체가 아니라 "
                "타인과의 관계 속에서 형성되고 유지된다는 관점. "
                "서구 자유주의 전통의 독립적·자율적 자아 개념에 대한 대안. "
                "관계와 연결(connection)이 분리(separation)보다 자아 발달의 핵심이라고 본다. "
                "이 개념에서 도덕적 책임은 외부에서 부과되는 것이 아니라 관계 속에서 발생한다."
            ),
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "related_terms": ["배려윤리", "연결", "분리 vs 연결", "책임의 윤리"]
        },
        {
            "id": "kw-gilligan-nonviolence-morality",
            "term": "비폭력의 도덕성",
            "term_en": "morality of nonviolence",
            "definition": (
                "길리건이 제시한 배려 도덕 발달의 최고 단계. "
                "자신과 타인 모두에 대한 배려를 통합하는 성숙한 도덕성의 형태. "
                "어떤 존재도 해쳐서는 안 된다는 비폭력의 원칙이 배려윤리의 보편적 토대가 된다. "
                "이 단계에서는 배려가 사회적 압력이 아닌 자아의 자유로운 선택이 된다."
            ),
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "related_terms": ["배려의 도덕 발달", "자기와 타인 배려", "보편적 배려", "배려윤리"]
        },
        {
            "id": "kw-gilligan-contextual-judgment",
            "term": "맥락 의존적 판단",
            "term_en": "contextual and narrative judgment",
            "definition": (
                "길리건 배려윤리의 핵심 특성으로, 도덕 판단이 추상적 원칙의 기계적 적용이 아니라 "
                "구체적 상황, 관계의 역사, 맥락을 고려하여 이루어져야 한다는 입장. "
                "도덕 문제는 서사적(narrative)으로 이해되어야 하며, "
                "맥락에 따라 동일한 행위의 도덕적 의미가 달라질 수 있다. "
                "이는 공리주의의 결과 계산이나 칸트의 원칙 적용과 대비된다."
            ),
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "related_terms": ["배려의 윤리", "서사적 이해", "관계 중심 도덕성", "맥락주의"]
        },
        {
            "id": "kw-gilligan-care-development-stages",
            "term": "배려의 도덕 발달 3단계",
            "term_en": "three levels of care moral development",
            "definition": (
                "길리건이 제시한 배려 중심 도덕 발달의 세 단계. "
                "1단계(자기 생존): 자신의 필요만 중심에 두는 단계. "
                "전환 1: 자기중심성에서 책임으로 이동. "
                "2단계(자기희생적 선): 타인 배려를 위해 자신을 희생하는 단계. "
                "전환 2: 자기희생에서 자신과 타인 모두 배려로 이동. "
                "3단계(비폭력의 도덕성): 자신과 타인 모두를 배려하는 성숙한 단계. "
                "콜버그의 6단계와 대응하는 배려윤리적 도덕 발달 모델이다."
            ),
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "related_terms": ["비폭력의 도덕성", "자기희생적 선", "배려윤리", "콜버그 비판"]
        },
        {
            "id": "kw-gilligan-responsibility-ethics",
            "term": "책임의 윤리",
            "term_en": "ethics of responsibility",
            "definition": (
                "배려윤리의 핵심 요소로, 도덕을 권리의 준수가 아니라 관계 속에서 "
                "타인의 필요에 응답하는 책임으로 이해하는 윤리 관점. "
                "책임(responsibility)은 응답하다(respond)와 어원이 같으며, "
                "구체적 관계 속에서 타인에게 응답하는 것이 도덕적 책임의 핵심이다. "
                "이 책임은 외부에서 부과되는 것이 아니라 관계 속에서 발생한다."
            ),
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "related_terms": ["배려윤리", "관계적 자아", "응답성", "배려의 윤리"]
        },
        {
            "id": "kw-gilligan-heinz-dilemma-amy",
            "term": "에이미의 응답",
            "term_en": "Amy's response to Heinz dilemma",
            "definition": (
                "콜버그의 하인츠 딜레마에서 11세 소녀 에이미의 응답. "
                "제이크(소년)가 생명권 > 재산권의 논리로 답한 것과 달리, "
                "에이미는 약사와의 대화와 관계 회복을 통한 해결을 제안했다. "
                "콜버그 기준으로는 낮은 단계로 평가되지만, "
                "길리건은 이를 배려의 윤리를 표현하는 '다른 도덕적 목소리'로 재평가했다. "
                "이 사례는 배려윤리와 정의윤리의 차이를 보여주는 대표적 사례이다."
            ),
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "related_terms": ["하인츠 딜레마", "다른 목소리", "배려의 윤리", "콜버그 비판"]
        },
        {
            "id": "kw-gilligan-feminist-ethics",
            "term": "페미니스트 윤리",
            "term_en": "feminist ethics",
            "definition": (
                "여성의 도덕 경험을 출발점으로 삼아 주류 윤리학의 남성 편향을 비판하고 "
                "대안을 모색하는 윤리 이론의 총칭. "
                "길리건의 배려윤리는 페미니스트 윤리의 대표적 이론이다. "
                "여성이 주변화되거나 열등한 것으로 다루어진 도덕 경험을 재평가하고, "
                "관계·배려·맥락을 도덕의 중심에 놓는다."
            ),
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "related_terms": ["배려윤리", "다른 목소리", "콜버그 비판", "여성의 도덕 경험"]
        },
        {
            "id": "kw-gilligan-self-sacrifice",
            "term": "자기희생적 선",
            "term_en": "goodness as self-sacrifice",
            "definition": (
                "길리건이 배려 도덕 발달 2단계로 제시한 개념. "
                "타인에 대한 배려를 위해 자신의 필요와 욕구를 억압하는 것을 도덕적 선으로 간주하는 태도. "
                "여성에게 사회가 기대하는 역할(희생적 어머니, 헌신적 아내)과 연결되며, "
                "길리건은 이것이 진정한 도덕적 성숙이 아니라 사회적 압력의 내면화일 수 있다고 본다. "
                "3단계(비폭력의 도덕성)에서는 자신도 배려의 대상에 포함된다."
            ),
            "thinker_id": "gilligan",
            "work_id": "gilligan-in-a-different-voice",
            "related_terms": ["배려의 도덕 발달", "비폭력의 도덕성", "관계적 자아", "배려윤리"]
        },
        {
            "id": "kw-gilligan-connection",
            "term": "연결",
            "term_en": "connection",
            "definition": (
                "길리건이 강조하는 심리적·도덕적 핵심 개념으로, "
                "타인과의 관계적 연결이 자아 발달과 도덕적 삶의 근간임을 가리킨다. "
                "서구 심리학이 강조하는 '분리(separation)'와 대비된다. "
                "연결의 상실이나 위협이 도덕적 문제의 핵심이 되는 경우가 많으며, "
                "도덕적 성숙은 연결을 유지하면서도 자아를 실현하는 방식을 찾는 과정이다."
            ),
            "thinker_id": "gilligan",
            "work_id": "gilligan-meeting-at-crossroads",
            "related_terms": ["관계적 자아", "분리 vs 연결", "배려윤리", "책임의 윤리"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """길리건 관계 데이터 입력."""
    relations = [
        {
            "from_thinker": "gilligan",
            "to_thinker": "kohlberg",
            "type": "criticized",
            "description": (
                "길리건은 콜버그의 도덕발달 단계론이 남성을 연구 대상으로 구성되어 "
                "구조적으로 남성 편향을 가지며, 여성의 도덕적 경험을 열등한 것으로 오해하게 만든다고 비판했다. "
                "특히 콜버그의 하인츠 딜레마 분석에서 에이미의 응답이 낮은 단계로 평가된 것을 반박하며, "
                "배려와 관계 중심의 도덕적 목소리가 정의 중심의 도덕과 동등한 가치를 가진다고 주장했다."
            ),
            "evidence": "Gilligan, 'In a Different Voice' (1982)"
        },
        {
            "from_thinker": "kohlberg",
            "to_thinker": "gilligan",
            "type": "influenced",
            "description": (
                "콜버그의 도덕발달 단계론과 하인츠 딜레마는 길리건의 이론 발전에 결정적 계기가 되었다. "
                "길리건은 콜버그와 함께 연구하면서 그의 이론이 포착하지 못하는 여성의 도덕 경험을 발견했고, "
                "이를 비판하고 대안을 제시하는 과정에서 배려윤리가 탄생했다."
            ),
            "evidence": "Gilligan, 'In a Different Voice' (1982) — 서론에서 콜버그 연구와의 관계 설명"
        },
        {
            "from_thinker": "gilligan",
            "to_thinker": "noddings",
            "type": "influenced",
            "description": (
                "길리건의 배려윤리는 넬 나딩스(Nel Noddings)의 배려교육론에 직접적 영향을 주었다. "
                "나딩스는 길리건의 이론을 교육 맥락에 적용하여 배려 관계를 중심으로 하는 "
                "도덕교육론을 발전시켰다. 배려자(one-caring)와 피배려자(cared-for)의 관계론, "
                "배려의 교육과 실천이 나딩스의 핵심 이론이다."
            ),
            "evidence": "Noddings, 'Caring: A Feminine Approach to Ethics and Moral Education' (1984)"
        },
        {
            "from_thinker": "gilligan",
            "to_thinker": "piaget",
            "type": "criticized",
            "description": (
                "길리건은 피아제(및 콜버그)의 도덕발달론이 주로 소년을 연구 대상으로 하여 "
                "정의(justice) 중심의 도덕 발달만을 기술했다고 비판했다. "
                "여아와 여성의 도덕 발달은 정의보다 배려(care)와 관계(relationship)를 중심으로 이루어지며, "
                "이는 열등한 것이 아니라 다른 도덕 발달의 경로임을 주장했다."
            ),
            "evidence": "Gilligan, 'In a Different Voice' (1982), Chapter 1"
        },
        {
            "from_thinker": "gilligan",
            "to_thinker": "noddings",
            "type": "synthesized",
            "description": (
                "길리건과 나딩스는 배려윤리의 공동 창시자로 자주 언급된다. "
                "길리건이 심리학적·철학적 토대를 제공했다면, 나딩스는 이를 교육론으로 정교화했다. "
                "두 이론은 상호 보완적 관계를 형성하며 배려윤리 전체를 구성한다."
            ),
            "evidence": "배려윤리 문헌 전반 — 두 이론가는 항상 함께 다루어진다"
        }
    ]

    for rel in relations:
        rel_id = f"{rel['from_thinker']}-{rel['type']}-{rel['to_thinker']}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id}: {result['result']}")

    return len(relations)


def main():
    """메인 실행 함수."""
    print("=== 길리건(Gilligan) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (gilligan)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n길리건 데이터 입력 완료!")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}")
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
