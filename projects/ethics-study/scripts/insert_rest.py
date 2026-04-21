"""제임스 레스트(James Rest) 데이터를 ES에 직접 입력하는 스크립트."""

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
    """레스트 사상가 데이터 입력."""
    doc = {
        "id": "rest",
        "name": "제임스 레스트",
        "name_en": "James Rest",
        "field": "moral_development",
        "era": "현대",
        "birth_year": 1941,
        "death_year": 1999,
        "background": (
            "미국 미네소타 대학교 교육심리학과 교수로 재직한 레스트는 로렌스 콜버그의 제자로서 "
            "콜버그의 도덕발달 이론을 계승하고 발전시켰다. "
            "콜버그의 도덕판단면접(MJI: Moral Judgment Interview)이 갖는 방법론적 한계, "
            "즉 임상 면접의 주관성, 대규모 측정의 어려움, 채점의 복잡성을 극복하기 위해 "
            "객관식 형태의 도덕 판단 측정 도구인 DIT(Defining Issues Test)를 개발했다. "
            "평생에 걸쳐 도덕 판단의 발달을 경험적으로 측정하고 검증하는 연구에 헌신하였으며, "
            "도덕 행동이 단일 요인이 아닌 복잡한 심리 과정의 산물임을 강조하는 "
            "4구성요소 모델(Four Component Model)을 체계화했다. "
            "말년에는 제자인 나르바에스(Darcia Narvaez), 비보(Muriel Bebeau), 토마(Stephen Thoma)와 함께 "
            "신콜버그주의(Neo-Kohlbergian) 관점을 발전시켰다."
        ),
        "core_philosophy": (
            "레스트의 핵심 이론은 두 가지로 요약된다. "
            "첫째, 도덕성의 4구성요소 모델(Four Component Model): 도덕적 행동은 "
            "① 도덕적 민감성(moral sensitivity) — 상황에서 도덕적 문제를 인식하고 타인에게 미치는 영향 파악, "
            "② 도덕적 판단(moral judgment) — 어떤 행동이 도덕적으로 옳은지 판단, "
            "③ 도덕적 동기화(moral motivation) — 도덕적 가치를 다른 개인적 가치보다 우선시하는 결정, "
            "④ 도덕적 품성(moral character) — 도덕적 의도를 실행할 수 있는 용기, 인내, 능력의 "
            "네 가지 심리 과정이 복합적으로 작용한 결과다. 각 구성요소는 독립적이며 비선형적으로 상호작용한다. "
            "둘째, DIT(Defining Issues Test): 콜버그의 도덕 딜레마를 활용하되 객관식으로 답하게 하여 "
            "도덕 판단 수준을 대규모로 측정할 수 있게 한 표준화 도구다. "
            "신콜버그주의에서는 콜버그의 단계론을 개인이익 스키마, 규범유지 스키마, 후인습 스키마의 "
            "세 스키마로 재해석하여 도덕 발달을 설명한다."
        ),
        "philosophical_journey": (
            "초기(콜버그 제자, 1960~70년대): 콜버그의 지도 아래 도덕 판단 발달을 연구했다. "
            "콜버그의 MJI 방법론의 한계를 인식하고 대규모 측정이 가능한 도구 개발에 착수하였다. "
            "중기(4구성요소 모델 체계화, 1980년대): 1984년 도덕 행동을 설명하는 4구성요소 모델을 제시했다. "
            "도덕적 판단만으로는 도덕적 행동을 충분히 설명할 수 없음을 강조하고, "
            "민감성, 판단, 동기화, 품성의 네 요소가 모두 필요함을 논증했다. "
            "후기(DIT-2 및 신콜버그주의, 1990년대): 개정판 DIT-2를 개발하고, "
            "나르바에스, 비보, 토마와 함께 신콜버그주의적 접근을 체계화했다. "
            "콜버그의 단계론을 스키마 이론(schema theory)으로 재해석하여 "
            "도덕 발달을 보다 유연하고 심리학적으로 설명하고자 했다."
        ),
        "keywords": [
            "4구성요소 모델",
            "도덕적 민감성",
            "도덕적 판단",
            "도덕적 동기화",
            "도덕적 품성",
            "DIT",
            "신콜버그주의",
            "스키마 이론",
            "후인습 스키마",
            "도덕심리학"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="rest", document=doc)
    print(f"[thinker] rest: {result['result']}")
    return result


def insert_works(client):
    """레스트 저서 데이터 입력."""
    works = [
        {
            "id": "rest-development-in-judging",
            "thinker_id": "rest",
            "title": "도덕 판단의 발달",
            "title_original": "Development in Judging Moral Issues",
            "year": 1979,
            "significance": (
                "레스트가 DIT(Defining Issues Test) 연구를 체계적으로 정리한 초기 주저. "
                "도덕 판단의 발달을 경험적으로 측정하는 방법론을 제시하고, "
                "콜버그의 단계론을 보완·검증하는 방대한 종단 및 횡단 연구 결과를 담았다. "
                "다양한 연령대와 집단(청소년, 성인, 전문직 등)에서 도덕 판단 수준을 측정한 "
                "경험적 자료를 제공하며, DIT의 신뢰도와 타당도를 검증했다."
            ),
            "key_concepts": [
                "DIT", "도덕 판단 발달", "P 점수", "원칙 수준 사고",
                "횡단 연구", "종단 연구", "도덕 발달 측정"
            ]
        },
        {
            "id": "rest-moral-development-advances",
            "thinker_id": "rest",
            "title": "도덕 발달: 연구의 진보",
            "title_original": "Moral Development: Advances in Research and Theory",
            "year": 1986,
            "significance": (
                "레스트의 4구성요소 모델(Four Component Model)을 체계적으로 제시한 핵심 저작. "
                "도덕 행동이 도덕 판단 하나만이 아니라 민감성·판단·동기화·품성의 네 구성요소 간 "
                "복합적 심리 과정에서 비롯된다는 이론적 틀을 확립했다. "
                "기존 콜버그식 도덕발달 연구의 한계를 비판적으로 검토하고, "
                "도덕 행동의 다원적·심리학적 설명을 제공했다."
            ),
            "key_concepts": [
                "4구성요소 모델", "도덕적 민감성", "도덕적 판단",
                "도덕적 동기화", "도덕적 품성", "도덕 행동"
            ]
        },
        {
            "id": "rest-postconventional-moral-thinking",
            "thinker_id": "rest",
            "title": "신콜버그주의적 접근: 후인습적 도덕 사고",
            "title_original": "Postconventional Moral Thinking: A Neo-Kohlbergian Approach",
            "year": 1999,
            "significance": (
                "레스트가 나르바에스(Narvaez), 비보(Bebeau), 토마(Thoma)와 공동 저술한 만년의 역작. "
                "콜버그의 도덕 발달 단계론을 스키마 이론(schema theory)으로 재해석하여 "
                "신콜버그주의(Neo-Kohlbergian) 이론 체계를 완성했다. "
                "개인이익 스키마, 규범유지 스키마, 후인습 스키마의 세 스키마를 통해 "
                "도덕 발달 수준을 설명하고, DIT-2로 이를 측정하는 방법론을 제시했다."
            ),
            "key_concepts": [
                "신콜버그주의", "스키마 이론", "개인이익 스키마",
                "규범유지 스키마", "후인습 스키마", "DIT-2", "후인습적 사고"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """레스트 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 도덕적 민감성
        {
            "id": "rest-claim-001",
            "thinker_id": "rest",
            "work_id": "rest-moral-development-advances",
            "source_detail": "Moral Development: Advances in Research and Theory, Chapter 1",
            "claim": (
                "도덕적 민감성(moral sensitivity)은 4구성요소 모델의 첫 번째 요소로, "
                "특정 상황이 도덕적 문제를 내포하고 있음을 인식하고, "
                "자신의 행동이 타인에게 어떤 영향을 미칠 수 있는지를 파악하는 능력이다. "
                "도덕적 행동의 출발점으로, 도덕적 민감성이 없으면 어떤 상황이 도덕적으로 중요한지 "
                "아예 인식하지 못하게 된다."
            ),
            "explanation": (
                "도덕적 민감성은 상황 속에서 도덕적 의미를 읽어내는 능력이다. "
                "공감(empathy)과 역할 채택(role-taking) 능력이 핵심이다. "
                "예를 들어, 친구가 힘들어한다는 것을 알아차리는 것, "
                "자신의 어떤 말이나 행동이 타인에게 상처를 줄 수 있음을 예측하는 것이 이에 해당한다. "
                "레스트는 이 요소가 다른 요소들과 독립적으로 작동하며, "
                "뛰어난 도덕 판단력을 가져도 도덕적 민감성이 부족하면 도덕적 행동이 일어나지 않을 수 있다고 보았다."
            ),
            "argument": (
                "레스트는 도덕심리학 연구들이 도덕 판단(Kohlberg)이나 도덕적 추론에만 집중해 온 것을 비판했다. "
                "실제 도덕적 행동은 먼저 '이 상황에 도덕적 문제가 있는가'를 인식해야 발생한다. "
                "사회심리학 연구(예: 바이스탠더 효과 연구)에서 방관자들이 도덕적으로 무관심한 것이 아니라 "
                "상황의 도덕적 긴박성을 인식하지 못해서 개입하지 않는 경우가 있음을 근거로 삼았다."
            ),
            "counterpoint": (
                "도덕적 민감성을 단독으로 측정하는 도구의 타당성 문제가 지적되었다. "
                "또한 민감성이 높아도 다른 구성요소(판단, 동기화, 품성)가 부족하면 도덕적 행동이 나타나지 않으므로 "
                "구성요소 간 상호작용 메커니즘에 대한 추가 연구가 필요하다는 비판이 있다."
            ),
            "context": (
                "레스트는 콜버그의 도덕발달 이론이 도덕 판단(Component 2)에만 초점을 맞춘 한계를 극복하기 위해 "
                "도덕 행동에 관여하는 심리 과정 전체를 포괄하는 모델이 필요하다고 보았다."
            ),
            "keywords": ["도덕적 민감성", "4구성요소 모델", "공감", "역할 채택", "도덕 행동"],
            "verified": False
        },
        # CLAIM-002: 도덕적 판단
        {
            "id": "rest-claim-002",
            "thinker_id": "rest",
            "work_id": "rest-moral-development-advances",
            "source_detail": "Moral Development: Advances in Research and Theory, Chapter 1",
            "claim": (
                "도덕적 판단(moral judgment)은 4구성요소 모델의 두 번째 요소로, "
                "인식된 상황에서 어떤 행동 방향이 도덕적으로 옳은지를 판단하는 과정이다. "
                "콜버그의 도덕 발달 단계론이 설명하는 핵심 내용이 바로 이 구성요소이며, "
                "레스트는 이를 DIT(Defining Issues Test)를 통해 측정한다."
            ),
            "explanation": (
                "도덕적 판단은 '무엇이 옳은가'를 결정하는 과정이다. "
                "레스트는 콜버그의 이 관점을 수용하되, 이것만으로는 도덕 행동 전체를 설명할 수 없다고 보았다. "
                "예를 들어, 어떤 사람이 '거짓말은 나쁘다'고 판단하더라도 "
                "실제 상황에서 거짓말을 안 하는 데는 다른 요소들도 필요하다. "
                "DIT는 이 도덕 판단 수준을 P점수(Principled score)로 객관적으로 측정한다."
            ),
            "argument": (
                "레스트는 도덕 판단이 가장 많이 연구된 구성요소임을 인정하면서도, "
                "도덕 판단 수준이 높다고 해서 반드시 도덕적 행동이 따르지 않는다는 경험적 증거를 제시했다. "
                "이는 도덕 판단이 필요하지만 충분하지 않은 조건임을 의미하며, "
                "나머지 세 구성요소의 필요성을 정당화한다."
            ),
            "counterpoint": (
                "일부 연구자들은 레스트의 DIT가 콜버그의 원래 도덕 판단 개념을 충분히 포착하는지에 의문을 제기했다. "
                "객관식 형식이 도덕 추론의 깊이를 제대로 측정할 수 있는가에 대한 비판도 있다."
            ),
            "context": (
                "콜버그의 6단계 도덕 발달론을 중심 축으로 삼되, "
                "이를 도덕 행동 설명의 한 구성요소로 위치지움으로써 보다 포괄적인 모델을 구성하고자 했다."
            ),
            "keywords": ["도덕적 판단", "4구성요소 모델", "DIT", "P점수", "콜버그"],
            "verified": False
        },
        # CLAIM-003: 도덕적 동기화
        {
            "id": "rest-claim-003",
            "thinker_id": "rest",
            "work_id": "rest-moral-development-advances",
            "source_detail": "Moral Development: Advances in Research and Theory, Chapter 1",
            "claim": (
                "도덕적 동기화(moral motivation)는 4구성요소 모델의 세 번째 요소로, "
                "도덕적 가치를 다른 개인적 가치(직업적 성공, 자기 이익 등)보다 우선시하여 "
                "도덕적으로 행동하기로 결정하는 과정이다. "
                "무엇이 옳은지 알더라도 다른 동기가 더 강하면 도덕적으로 행동하지 않을 수 있다."
            ),
            "explanation": (
                "도덕적 동기화는 '옳은 것을 행하고자 하는 의지'와 관련된다. "
                "예를 들어, 부정직한 방법이 더 유리하다는 것을 알면서도 정직을 선택하는 것은 "
                "도덕적 동기화가 작동한 결과다. "
                "반대로, 도덕적 판단은 분명히 하면서도 이기심, 체면, 또래 압력 등에 밀려 "
                "비도덕적으로 행동하는 것은 도덕적 동기화가 실패한 경우다. "
                "레스트는 이 요소가 자아(self)의 도덕적 정체성과 밀접히 연관된다고 보았다."
            ),
            "argument": (
                "도덕 판단과 도덕 행동 간의 갭을 설명하기 위해 이 요소가 필요하다. "
                "연구에 따르면 높은 도덕 판단 수준을 가진 사람도 자기 이익이 걸렸을 때는 "
                "비도덕적으로 행동하는 경우가 있다. 이는 도덕 판단 외에 "
                "'도덕적 가치를 우선시하는 동기'라는 별도의 심리 과정이 필요함을 보여준다."
            ),
            "counterpoint": (
                "도덕적 동기화를 다른 구성요소와 명확히 구분하여 측정하는 것이 방법론적으로 어렵다는 비판이 있다. "
                "또한 동기의 원천(이타성 vs. 도덕적 정체성 vs. 내재화된 규범)에 대한 추가적 이론화가 필요하다."
            ),
            "context": (
                "레스트는 도덕 행동의 실패가 단순히 '옳고 그름을 몰라서'가 아니라 "
                "'알면서도 하지 않는' 경우가 많음에 주목했다. 이 갭을 메우기 위한 요소가 도덕적 동기화다."
            ),
            "keywords": ["도덕적 동기화", "4구성요소 모델", "도덕적 정체성", "가치 우선화"],
            "verified": False
        },
        # CLAIM-004: 도덕적 품성
        {
            "id": "rest-claim-004",
            "thinker_id": "rest",
            "work_id": "rest-moral-development-advances",
            "source_detail": "Moral Development: Advances in Research and Theory, Chapter 1",
            "claim": (
                "도덕적 품성(moral character)은 4구성요소 모델의 네 번째 요소로, "
                "도덕적 의도를 실제 행동으로 옮기는 데 필요한 용기(courage), 인내(persistence), "
                "실행 능력(implementation skills)을 포함한다. "
                "도덕적으로 행동하고자 하는 의도가 있어도 실행 역량이 부족하면 도덕적 행동이 실패한다."
            ),
            "explanation": (
                "도덕적 품성은 덕윤리학(virtue ethics)의 덕(virtue) 개념과 유사하다. "
                "예를 들어, 불의에 맞서야 한다고 판단하고 그러고 싶은 동기도 있지만, "
                "막상 현실에서 용기 없이 침묵하는 것은 도덕적 품성의 부족이다. "
                "또한 도덕적 목표를 방해하는 유혹이나 충동을 통제하는 자기 조절 능력도 포함된다. "
                "레스트는 인격교육(character education)의 중요성이 이 구성요소에서 근거를 찾는다고 보았다."
            ),
            "argument": (
                "심리학 연구에서 자기 통제력(self-control), 의지력(willpower)이 도덕적 행동과 "
                "상관이 있음이 밝혀졌다. 또한 도덕적 실행에는 실제적 계획, 장애물 극복, "
                "끈기 등의 실행 기술이 필요하다는 점에서 품성 요소는 경험적으로 지지된다."
            ),
            "counterpoint": (
                "도덕적 품성과 도덕적 동기화 사이의 경계가 불명확하다는 비판이 있다. "
                "또한 이 요소를 너무 강조하면 구조적·사회적 요인을 도외시하고 "
                "개인의 품성에만 책임을 돌리는 '품성 귀인 오류'로 이어질 수 있다는 우려도 있다."
            ),
            "context": (
                "아리스토텔레스의 덕윤리학에서 '덕'이 행위의 실천 역량을 강조하듯, "
                "레스트도 도덕적 행동이 단순한 의도 이상의 실행 역량을 요구한다고 보았다."
            ),
            "keywords": ["도덕적 품성", "4구성요소 모델", "용기", "자기 조절", "인격교육"],
            "verified": False
        },
        # CLAIM-005: 4구성요소의 비선형적 상호작용
        {
            "id": "rest-claim-005",
            "thinker_id": "rest",
            "work_id": "rest-moral-development-advances",
            "source_detail": "Moral Development: Advances in Research and Theory, Chapter 1",
            "claim": (
                "4구성요소 모델의 각 요소는 독립적이며, 고정된 순서대로 작동하는 것이 아니라 "
                "상황에 따라 비선형적으로 상호작용한다. "
                "각 요소 중 하나라도 충분히 작동하지 않으면 도덕적 행동이 실패할 수 있으며, "
                "각 요소는 각각 별도의 심리 과정으로 설명되고 측정될 수 있다."
            ),
            "explanation": (
                "레스트는 이전 연구들이 도덕적 판단만을 중심 변수로 다뤄왔기 때문에 "
                "도덕 판단과 도덕 행동 간의 상관관계가 생각보다 낮게 나타남을 설명하기 어려웠다고 지적했다. "
                "4구성요소가 모두 갖춰져야 도덕적 행동이 나타나며, "
                "어느 한 요소에서 실패하면 전체 과정이 중단될 수 있다. "
                "예를 들어, 민감성이 뛰어나고 판단력이 높아도 동기화가 실패하면 행동하지 않는다."
            ),
            "argument": (
                "심리학 연구들은 도덕 판단(콜버그 점수)이 실제 친사회적 행동과 "
                "중간 정도의 상관관계만 보임을 반복적으로 보고했다. "
                "레스트는 이 갭을 다른 세 구성요소(민감성, 동기화, 품성)가 매개 변수로 작용하기 때문이라고 설명했다. "
                "따라서 도덕 행동을 이해하려면 4구성요소 모두를 고려해야 한다."
            ),
            "counterpoint": (
                "모델이 기술적(descriptive)이어서 각 구성요소 간의 인과 메커니즘이 충분히 명시화되지 않았다는 비판이 있다. "
                "또한 4구성요소가 완전히 독립적인지, 아니면 어느 정도 공통 심리 기제를 공유하는지에 대한 "
                "추가적 실증 연구가 필요하다."
            ),
            "context": (
                "레스트의 모델은 도덕교육의 다각적 접근을 지지한다. "
                "단순히 도덕 지식이나 추론 능력만 가르치는 것으로는 부족하며, "
                "민감성 훈련, 동기화 강화, 품성 계발을 아우르는 종합적 접근이 필요하다."
            ),
            "keywords": ["4구성요소 모델", "비선형적 상호작용", "도덕 행동", "심리 과정"],
            "verified": False
        },
        # CLAIM-006: DIT(Defining Issues Test)
        {
            "id": "rest-claim-006",
            "thinker_id": "rest",
            "work_id": "rest-development-in-judging",
            "source_detail": "Development in Judging Moral Issues",
            "claim": (
                "DIT(Defining Issues Test, 결정적 문제 검사)는 콜버그의 도덕 딜레마를 활용하되 "
                "객관식 형태로 도덕 판단 수준을 측정하는 표준화 도구다. "
                "응답자는 딜레마 상황에서 자신이 중요하다고 생각하는 고려 사항을 선택·순위화하며, "
                "이를 통해 P점수(후인습 수준 사고의 비율)를 산출한다."
            ),
            "explanation": (
                "DIT는 콜버그의 도덕판단면접(MJI)이 가진 한계, 즉 훈련된 면접자가 필요하고 "
                "채점에 주관성이 개입되며 대규모 측정이 어렵다는 문제를 해결하기 위해 개발되었다. "
                "응답자에게 6개의 도덕 딜레마(예: 하인즈 딜레마)를 제시하고, "
                "각 딜레마에 대해 미리 만들어진 12개의 고려 사항 중 "
                "가장 중요한 것을 선택하고 순위를 매기게 한다. "
                "P점수는 후인습적 수준(Kohlberg 5~6단계에 해당)의 고려 사항이 선택된 비율로, "
                "도덕 판단의 발달 수준을 나타낸다."
            ),
            "argument": (
                "DIT는 높은 신뢰도(검사-재검사 신뢰도 약 0.7 이상)와 타당도(연령에 따른 발달적 증가, "
                "교육 수준과 상관, 친사회적 행동과 상관)를 보여주었다. "
                "MJI보다 훨씬 적은 시간과 비용으로 대규모 집단에 적용 가능하다는 실용적 장점도 있다. "
                "레스트는 DIT로 수십만 명을 대상으로 도덕 판단 발달 연구를 수행했다."
            ),
            "counterpoint": (
                "객관식 형식이 도덕 추론의 질적 깊이를 포착하기 어렵다는 비판이 있다. "
                "응답자가 단순히 '좋게 들리는' 항목을 고를 수 있다는 사회적 바람직성(social desirability) 문제도 지적되었다. "
                "이에 레스트는 후기에 DIT-2를 개발하여 일부 한계를 보완했다."
            ),
            "context": (
                "콜버그의 도덕 발달 이론을 경험 과학적으로 검증하고 확장하려는 노력의 산물이다. "
                "DIT는 도덕교육 연구에서 가장 광범위하게 사용된 도덕 판단 측정 도구가 되었다."
            ),
            "keywords": ["DIT", "도덕 판단 측정", "P점수", "후인습 사고", "표준화 검사"],
            "verified": False
        },
        # CLAIM-007: 신콜버그주의 — 스키마 이론으로 재해석
        {
            "id": "rest-claim-007",
            "thinker_id": "rest",
            "work_id": "rest-postconventional-moral-thinking",
            "source_detail": "Postconventional Moral Thinking: A Neo-Kohlbergian Approach",
            "claim": (
                "신콜버그주의(Neo-Kohlbergian approach)는 콜버그의 도덕 발달 단계론을 "
                "스키마 이론(schema theory)으로 재해석한다. "
                "콜버그의 6단계 대신 개인이익 스키마(Personal Interest Schema), "
                "규범유지 스키마(Maintaining Norms Schema), "
                "후인습 스키마(Postconventional Schema)의 세 스키마를 제안하며, "
                "이를 통해 도덕 발달을 보다 유연하고 심리학적으로 설명한다."
            ),
            "explanation": (
                "스키마(schema)는 인지심리학에서 과거 경험을 통해 형성된 일반화된 지식 구조다. "
                "개인이익 스키마: 도덕 결정을 자신의 이익과 손해로 계산하는 방식. "
                "규범유지 스키마: 기존의 사회적 규범과 법·질서를 유지하는 것이 도덕의 기준이라는 방식. "
                "후인습 스키마: 원칙과 이상에 따라 규범 자체의 타당성을 비판적으로 검토하는 방식. "
                "개인은 이 스키마들을 모두 갖고 있으며, 상황에 따라 활성화되는 스키마가 다를 수 있다."
            ),
            "argument": (
                "콜버그의 단계론은 단계가 불가역적이고 순서가 고정되어야 한다는 엄격한 구조적 가정을 갖는다. "
                "그러나 경험적 연구에서 성인도 낮은 수준의 추론을 하거나 "
                "상황에 따라 추론 수준이 달라지는 것이 관찰된다. "
                "스키마 이론은 이 유연성을 설명하며, '단계'보다 '스키마의 상대적 활성화'로 "
                "도덕 발달 수준을 이해하는 것이 심리학적으로 더 정확하다고 주장한다."
            ),
            "counterpoint": (
                "스키마로의 재해석이 콜버그 이론의 핵심인 '구조적 전체성(structural wholeness)'과 "
                "'발달 불가역성'을 약화시킨다는 비판이 있다. "
                "또한 세 스키마와 콜버그의 6단계 간의 정확한 대응 관계가 불분명하다는 지적도 있다."
            ),
            "context": (
                "1990년대 콜버그 이론에 대한 여러 비판(문화 상대주의, 측정 방법론 문제 등)에 대응하여 "
                "이론을 현대 인지심리학과 접목시킴으로써 콜버그 전통을 쇄신하고자 했다."
            ),
            "keywords": ["신콜버그주의", "스키마 이론", "후인습 스키마", "규범유지 스키마", "개인이익 스키마"],
            "verified": False
        },
        # CLAIM-008: MJI 한계 보완
        {
            "id": "rest-claim-008",
            "thinker_id": "rest",
            "work_id": "rest-development-in-judging",
            "source_detail": "Development in Judging Moral Issues",
            "claim": (
                "콜버그의 도덕판단면접(MJI: Moral Judgment Interview)은 "
                "훈련된 임상가가 직접 면접하고 채점해야 하므로 "
                "시간과 비용이 많이 들고 채점자 간 신뢰도 문제가 있어 대규모 연구에 부적합하다. "
                "레스트의 DIT는 이러한 방법론적 한계를 극복하여 "
                "대규모 표본을 대상으로 경제적·객관적으로 도덕 판단 수준을 측정할 수 있게 했다."
            ),
            "explanation": (
                "MJI는 면접자가 응답자에게 딜레마를 제시하고 심층 면접을 통해 추론 과정을 파악한 뒤 "
                "훈련된 채점 체계로 단계를 결정하는 방식이다. "
                "이 방법은 개인의 추론 구조를 심층적으로 파악할 수 있지만 "
                "1명의 면접에 수 시간이 걸리며, 채점자 간 신뢰도 확보에 어려움이 있다. "
                "DIT는 짧은 시간에 대규모 집단에 적용 가능하며, 컴퓨터 채점이 가능해 객관성을 보장한다."
            ),
            "argument": (
                "레스트는 DIT와 MJI가 같은 구성개념을 측정하는지 비교 연구를 수행했다. "
                "두 검사의 상관이 유의미하게 나타나(r ≈ 0.7), DIT가 콜버그 이론이 측정하려는 것과 "
                "같은 개념을 측정함을 입증했다. "
                "동시에 DIT가 더 빠르고 경제적이며 대규모 연구에 적합함을 보여주었다."
            ),
            "counterpoint": (
                "DIT가 MJI를 완전히 대체할 수 있는지에 대해서는 논란이 있다. "
                "MJI는 응답자가 스스로 이유를 생성(production)하는 반면, "
                "DIT는 제시된 이유 중에서 인식(recognition)하는 것이므로 "
                "측정 방식의 차이가 결과에 영향을 미칠 수 있다."
            ),
            "context": (
                "도덕 발달 연구를 실험 과학으로 발전시키기 위해 신뢰할 수 있고 경제적인 측정 도구의 개발이 필수적이었다. "
                "DIT의 개발은 도덕 발달 연구의 방법론적 혁신이었다."
            ),
            "keywords": ["MJI", "DIT", "도덕 판단 측정", "방법론", "콜버그"],
            "verified": False
        },
        # CLAIM-009: 도덕 행동은 복합 심리 과정의 결과
        {
            "id": "rest-claim-009",
            "thinker_id": "rest",
            "work_id": "rest-moral-development-advances",
            "source_detail": "Moral Development: Advances in Research and Theory, Chapter 1",
            "claim": (
                "도덕적 행동은 단일 심리 요인(예: 도덕 판단 수준)이 아니라 "
                "도덕적 민감성, 도덕적 판단, 도덕적 동기화, 도덕적 품성이라는 "
                "네 가지 복합적 심리 과정이 모두 작동한 결과로 나타난다. "
                "이 중 하나라도 실패하면 도덕적 행동이 발생하지 않을 수 있다."
            ),
            "explanation": (
                "레스트의 이 주장은 기존 도덕심리학 연구들이 왜 도덕 판단 수준과 "
                "실제 도덕 행동 간의 상관이 기대보다 낮은지를 설명해준다. "
                "즉, 도덕 행동이 나타나지 않은 이유가 '도덕 판단이 낮아서'만이 아니라, "
                "'민감성이 부족해서', '다른 가치가 더 강해서(동기화 실패)', '실행 역량이 부족해서(품성 미비)' "
                "등 다양할 수 있다는 것이다."
            ),
            "argument": (
                "심리학의 다수 연구들은 도덕 판단 수준이 실제 부정 행위 억제, "
                "이타적 행동 등과 중간 수준의 상관만 보임을 반복 보고했다. "
                "레스트는 4구성요소 중 어느 하나가 낮으면 행동이 실패할 수 있다는 '약한 고리 효과'를 강조한다. "
                "이는 도덕교육이 한 가지 요소(예: 도덕 추론 교육)에만 집중해서는 안 됨을 시사한다."
            ),
            "counterpoint": (
                "네 구성요소 간의 정확한 상호작용 메커니즘이 충분히 명시화되지 않았다는 비판이 있다. "
                "또한 상황적·사회구조적 요인이 충분히 다루어지지 않았다는 지적도 있다."
            ),
            "context": (
                "레스트는 도덕교육의 실효성을 높이기 위해 도덕 행동의 복합적 심리 과정을 "
                "종합적으로 이해해야 한다는 실천적 동기에서 모델을 구성했다."
            ),
            "keywords": ["도덕 행동", "4구성요소 모델", "복합 심리 과정", "도덕교육"],
            "verified": False
        },
        # CLAIM-010: 후인습 스키마와 도덕 교육
        {
            "id": "rest-claim-010",
            "thinker_id": "rest",
            "work_id": "rest-postconventional-moral-thinking",
            "source_detail": "Postconventional Moral Thinking: A Neo-Kohlbergian Approach",
            "claim": (
                "후인습 스키마(Postconventional Schema)는 사회의 기존 규범이나 법을 그대로 따르는 것이 아니라, "
                "이상적 사회 협력과 공정성의 원칙에 근거하여 규범 자체의 타당성을 비판적으로 검토하고 "
                "정의와 인권을 최우선으로 하는 도덕적 사고 방식이다. "
                "도덕 발달의 최고 수준에 해당하며 교육을 통해 촉진될 수 있다."
            ),
            "explanation": (
                "후인습 스키마는 콜버그의 5~6단계에 해당하는 수준이다. "
                "단순히 법이나 다수의 의견에 따르는 것이 아니라, "
                "'이 법 혹은 규범이 정의로운가'를 스스로 판단하고 "
                "보편적 원칙(인권, 공정성, 인간 존엄성)에 비추어 행동한다. "
                "DIT에서 측정되는 P점수가 높을수록 후인습 스키마 활성화 비율이 높다. "
                "대학 교육, 다양한 윤리적 사고 훈련이 이 스키마 발달을 촉진할 수 있다."
            ),
            "argument": (
                "종단 연구에서 대학 교육이 후인습 스키마 발달과 유의미한 상관을 보였다. "
                "또한 법학자, 의사, 도덕철학 교수 등 전문직 집단에서 후인습 스키마 비율이 높게 나타났다. "
                "이는 고등 교육이 도덕 발달에 긍정적 영향을 미친다는 증거가 된다."
            ),
            "counterpoint": (
                "후인습적 사고가 실제로 더 '나은' 도덕 행동으로 이어지는지에 대한 논란이 있다. "
                "또한 후인습 스키마가 서구 자유주의 도덕 전통에 편향되어 있어 "
                "다른 문화적 도덕 전통을 평가 절하할 수 있다는 비판도 있다."
            ),
            "context": (
                "신콜버그주의에서 후인습 스키마는 도덕 발달의 목표이자 이상이다. "
                "도덕교육의 목표를 이 스키마의 발달로 설정하고, "
                "이를 촉진하는 교육 방법론을 모색하는 것이 신콜버그주의적 도덕교육의 방향이다."
            ),
            "keywords": ["후인습 스키마", "신콜버그주의", "P점수", "도덕 발달", "보편적 원칙"],
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """레스트 키워드 데이터 입력."""
    keywords = [
        {
            "id": "rest-kw-four-component",
            "term": "4구성요소 모델",
            "term_en": "Four Component Model",
            "definition": (
                "레스트가 제안한 도덕 행동 설명 모델. "
                "도덕적 민감성(moral sensitivity), 도덕적 판단(moral judgment), "
                "도덕적 동기화(moral motivation), 도덕적 품성(moral character)의 네 요소가 "
                "복합적·비선형적으로 상호작용하여 도덕 행동을 산출한다고 본다."
            ),
            "thinker_id": "rest",
            "work_id": "rest-moral-development-advances",
            "related_terms": ["도덕적 민감성", "도덕적 판단", "도덕적 동기화", "도덕적 품성", "도덕 행동"]
        },
        {
            "id": "rest-kw-moral-sensitivity",
            "term": "도덕적 민감성",
            "term_en": "Moral Sensitivity",
            "definition": (
                "4구성요소 모델의 첫 번째 요소. "
                "상황 속에 도덕적 문제가 있음을 인식하고 "
                "자신의 행동이 타인에게 미치는 영향을 파악하는 능력. "
                "공감과 역할 채택 능력이 핵심이다."
            ),
            "thinker_id": "rest",
            "work_id": "rest-moral-development-advances",
            "related_terms": ["4구성요소 모델", "공감", "역할 채택"]
        },
        {
            "id": "rest-kw-moral-motivation",
            "term": "도덕적 동기화",
            "term_en": "Moral Motivation",
            "definition": (
                "4구성요소 모델의 세 번째 요소. "
                "도덕적 가치를 다른 개인적 가치보다 우선시하여 "
                "도덕적으로 행동하기로 결정하는 과정. "
                "도덕적 정체성(moral identity)과 밀접히 연관된다."
            ),
            "thinker_id": "rest",
            "work_id": "rest-moral-development-advances",
            "related_terms": ["4구성요소 모델", "도덕적 정체성", "가치 우선화"]
        },
        {
            "id": "rest-kw-moral-character",
            "term": "도덕적 품성",
            "term_en": "Moral Character",
            "definition": (
                "4구성요소 모델의 네 번째 요소. "
                "도덕적 의도를 실제 행동으로 옮기는 데 필요한 용기, 인내, 실행 능력. "
                "덕윤리학의 덕(virtue) 개념과 유사하며, 인격교육의 목표와 연결된다."
            ),
            "thinker_id": "rest",
            "work_id": "rest-moral-development-advances",
            "related_terms": ["4구성요소 모델", "용기", "자기 조절", "인격교육", "덕윤리학"]
        },
        {
            "id": "rest-kw-dit",
            "term": "DIT",
            "term_en": "Defining Issues Test",
            "definition": (
                "레스트가 개발한 도덕 판단 수준 측정 표준화 검사. "
                "콜버그의 도덕 딜레마를 활용하되 객관식으로 답하게 하여 "
                "P점수(후인습 수준 사고 비율)를 산출한다. "
                "콜버그의 MJI에 비해 경제적이고 대규모 측정이 가능하다."
            ),
            "thinker_id": "rest",
            "work_id": "rest-development-in-judging",
            "related_terms": ["도덕 판단 측정", "P점수", "후인습 사고", "MJI", "콜버그"]
        },
        {
            "id": "rest-kw-neo-kohlbergian",
            "term": "신콜버그주의",
            "term_en": "Neo-Kohlbergian Approach",
            "definition": (
                "레스트, 나르바에스, 비보, 토마가 발전시킨 콜버그 이론의 현대적 재해석. "
                "콜버그의 6단계 대신 개인이익 스키마, 규범유지 스키마, 후인습 스키마의 "
                "세 스키마로 도덕 발달을 설명하며, 인지심리학의 스키마 이론을 접목했다."
            ),
            "thinker_id": "rest",
            "work_id": "rest-postconventional-moral-thinking",
            "related_terms": ["스키마 이론", "후인습 스키마", "DIT-2", "콜버그"]
        },
        {
            "id": "rest-kw-schema-theory",
            "term": "스키마 이론",
            "term_en": "Schema Theory",
            "definition": (
                "과거 경험을 통해 형성된 일반화된 지식 구조(스키마)가 "
                "새로운 정보 처리와 판단을 안내한다는 인지심리학 이론. "
                "신콜버그주의에서 도덕 발달을 설명하기 위해 차용되었으며, "
                "개인이익·규범유지·후인습 스키마의 세 수준으로 도덕 발달을 기술한다."
            ),
            "thinker_id": "rest",
            "work_id": "rest-postconventional-moral-thinking",
            "related_terms": ["신콜버그주의", "후인습 스키마", "개인이익 스키마", "규범유지 스키마"]
        },
        {
            "id": "rest-kw-postconventional-schema",
            "term": "후인습 스키마",
            "term_en": "Postconventional Schema",
            "definition": (
                "신콜버그주의의 세 스키마 중 최고 수준. "
                "기존 규범이나 법의 타당성을 비판적으로 검토하고 "
                "이상적 사회 협력과 보편적 원칙(정의, 인권)에 따라 도덕 판단을 내리는 사고 방식. "
                "콜버그의 5~6단계에 해당한다."
            ),
            "thinker_id": "rest",
            "work_id": "rest-postconventional-moral-thinking",
            "related_terms": ["신콜버그주의", "스키마 이론", "DIT", "P점수"]
        },
        {
            "id": "rest-kw-moral-psychology",
            "term": "도덕심리학",
            "term_en": "Moral Psychology",
            "definition": (
                "도덕적 사고, 판단, 감정, 행동의 심리적 기제를 과학적으로 연구하는 학문. "
                "레스트는 도덕심리학의 선구자로서 도덕 판단의 측정과 4구성요소 모델을 통해 "
                "도덕 행동의 복합적 심리 과정을 탐구했다."
            ),
            "thinker_id": "rest",
            "work_id": "rest-moral-development-advances",
            "related_terms": ["4구성요소 모델", "DIT", "도덕 발달"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """레스트 관련 관계 데이터 입력."""
    relations = [
        {
            "from_thinker": "kohlberg",
            "to_thinker": "rest",
            "type": "influenced",
            "description": (
                "콜버그는 도덕 발달 단계론과 도덕판단면접(MJI)으로 레스트에게 결정적 영향을 주었다. "
                "레스트는 콜버그의 직접적 제자로서 콜버그의 이론적 틀을 계승하되, "
                "DIT 개발과 4구성요소 모델로 이를 발전·보완했다."
            ),
            "evidence": "Rest, 1979, Development in Judging Moral Issues"
        },
        {
            "from_thinker": "rest",
            "to_thinker": "narvaez",
            "type": "influenced",
            "description": (
                "레스트는 나르바에스(Darcia Narvaez)와 신콜버그주의 이론을 공동으로 발전시켰다. "
                "나르바에스는 레스트의 신콜버그주의를 계승하면서 도덕 발달의 사회적·문화적 맥락을 "
                "통합한 '통합적 윤리 교육(integrative ethical education)' 이론으로 발전시켰다."
            ),
            "evidence": "Rest & Narvaez et al., 1999, Postconventional Moral Thinking"
        },
        {
            "from_thinker": "rest",
            "to_thinker": "lickona",
            "type": "influenced",
            "description": (
                "레스트의 4구성요소 모델은 리코나(Thomas Lickona)의 인격교육(character education) 이론에 영향을 주었다. "
                "특히 도덕적 품성(moral character)과 도덕적 동기화 구성요소는 "
                "리코나의 도덕적 앎(moral knowing), 도덕적 느낌(moral feeling), "
                "도덕적 행동(moral action)의 삼요소 모델과 개념적으로 연결된다."
            ),
            "evidence": "Lickona, 1991, Educating for Character"
        },
        {
            "from_thinker": "piaget",
            "to_thinker": "rest",
            "type": "influenced",
            "description": (
                "피아제의 인지발달 기반 도덕발달 이론은 콜버그를 거쳐 레스트에게 간접적 영향을 미쳤다. "
                "도덕 발달을 인지 발달과 연동된 단계적 과정으로 보는 관점이 레스트 이론의 토대이다."
            ),
            "evidence": "Piaget, 1932, The Moral Judgment of the Child"
        }
    ]

    for i, rel in enumerate(relations):
        rel_id = f"rest-rel-{i+1:03d}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id} ({rel['from_thinker']} → {rel['to_thinker']}): {result['result']}")

    return len(relations)


def main():
    client = get_client()
    try:
        print("=== 제임스 레스트(James Rest) 데이터 입력 시작 ===\n")

        # 1. 분야 확인
        print("--- 분야 확인 ---")
        ensure_field(client)

        # 2. 사상가
        print("\n--- 사상가 입력 ---")
        insert_thinker(client)

        # 3. 저서
        print("\n--- 저서 입력 ---")
        work_count = insert_works(client)
        print(f"저서 {work_count}개 입력 완료")

        # 4. 주장
        print("\n--- 주장 입력 ---")
        claim_count = insert_claims(client)
        print(f"주장 {claim_count}개 입력 완료")

        # 5. 키워드
        print("\n--- 키워드 입력 ---")
        kw_count = insert_keywords(client)
        print(f"키워드 {kw_count}개 입력 완료")

        # 6. 관계
        print("\n--- 관계 입력 ---")
        rel_count = insert_relations(client)
        print(f"관계 {rel_count}개 입력 완료")

        print("\n=== 데이터 입력 완료 ===")
        print(f"사상가: 1명 (rest)")
        print(f"저서: {work_count}개")
        print(f"주장: {claim_count}개")
        print(f"키워드: {kw_count}개")
        print(f"관계: {rel_count}개")

    finally:
        close_client(client)


if __name__ == "__main__":
    main()
