"""루이스 래스(Louis Raths) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS, INDEX_FIELDS
)


def ensure_field(client):
    """도덕발달 분야가 ethics-fields 인덱스에 없으면 확인."""
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
                "길리건의 배려윤리, 나딩스의 배려교육론, 래스의 가치명료화 등을 포함한다. "
                "도덕심리학, 도덕교육론과 밀접하게 연관되며 임용시험 핵심 영역이다."
            ),
            "order": 4
        }
        result = client.index(index=INDEX_FIELDS, id="moral_development", document=doc)
        print(f"[field] moral_development: {result['result']}")


def insert_thinker(client):
    """래스 사상가 데이터 입력."""
    doc = {
        "id": "raths",
        "name": "루이스 래스",
        "name_en": "Louis Raths",
        "field": "moral_development",
        "era": "현대",
        "birth_year": 1906,
        "death_year": 1978,
        "background": (
            "루이스 래스는 뉴욕 대학교(New York University) 교수로서, "
            "존 듀이(John Dewey)의 실용주의 교육철학의 영향을 깊이 받은 교육학자이다. "
            "듀이의 민주주의 교육 이념과 경험 중심 교육론을 계승하면서, "
            "가치교육 분야에서 독창적인 이론을 개척했다. "
            "1960년대에 메릴 하민(Merrill Harmin), 시드니 사이먼(Sidney Simon)과 공동 연구를 통해 "
            "가치명료화(values clarification) 이론과 교수법을 체계화하였다. "
            "가치명료화 이론은 1970년대 미국 학교 교육에서 폭넓게 수용되었으며, "
            "콜버그의 도덕발달 단계론과 함께 도덕교육의 양대 흐름을 형성했다. "
            "래스는 교사가 학생에게 특정 가치를 주입하는 전통적 도덕교육을 비판하고, "
            "학생 스스로 자신의 가치를 선택·명료화하도록 돕는 교육 방법을 제안했다."
        ),
        "core_philosophy": (
            "래스의 핵심 철학은 가치명료화(values clarification)이다. "
            "가치명료화란 개인이 자신의 가치를 선택(choosing), 소중히 여김(prizing), "
            "행동(acting)의 세 과정과 7가지 기준을 통해 명료화해가는 과정이다. "
            "7가지 기준은: (1) 자유롭게 선택, (2) 여러 대안들 중에서 선택, "
            "(3) 각 대안의 결과를 충분히 숙고한 후 선택, (4) 선택한 것을 소중히 여김(존중), "
            "(5) 공적으로 확언(affirm), (6) 선택에 따라 행동, (7) 반복적으로 행동이다. "
            "래스는 이 7가지 기준을 모두 충족시키는 것만이 진정한 가치(full value)이며, "
            "그렇지 않은 것은 단지 가치 지표(value indicator)에 불과하다고 보았다. "
            "또한 교사는 학생에게 특정 가치를 교화(indoctrination)해서는 안 되며, "
            "명료화 반응(clarifying response)을 통해 학생이 스스로 가치를 탐색하도록 도와야 한다고 주장했다."
        ),
        "philosophical_journey": (
            "초기(듀이 영향기): 존 듀이의 실용주의 교육철학을 수용하면서 "
            "민주주의적 가치교육, 경험 중심 교육에 관심을 가졌다. "
            "중기(가치명료화 이론 체계화, 1960년대): 하민, 사이먼과 협력하여 "
            "가치명료화 이론의 개념적 기초를 완성했다. "
            "1966년 「가치와 교수(Values and Teaching)」를 출간하여 "
            "가치명료화의 7가지 기준과 교수 전략을 체계화했다. "
            "후기(교육 현장 적용, 1970년대): 가치명료화 접근이 미국 교육 현장에 광범위하게 보급되었다. "
            "1978년 개정판을 통해 이론을 보완하고 다양한 교실 활동 전략을 추가했다. "
            "이 시기 콜버그로부터 가치 상대주의를 조장한다는 비판을 받았으며, "
            "이에 대한 논쟁이 도덕교육 분야의 핵심 쟁점이 되었다."
        ),
        "keywords": [
            "가치명료화",
            "7가지 기준",
            "가치 지표",
            "완전한 가치",
            "교화 반대",
            "명료화 반응",
            "가치 투표",
            "순위 매기기",
            "가치 상대주의",
            "선택·존중·행동"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="raths", document=doc)
    print(f"[thinker] raths: {result['result']}")
    return result


def insert_works(client):
    """래스 저서 데이터 입력."""
    works = [
        {
            "id": "raths-values-and-teaching-1966",
            "thinker_id": "raths",
            "title": "가치와 교수",
            "title_original": "Values and Teaching",
            "year": 1966,
            "significance": (
                "래스, 하민, 사이먼이 공동 저술한 가치명료화 이론의 핵심 원전. "
                "가치명료화의 7가지 기준(선택 3개, 존중 2개, 행동 2개)을 처음으로 체계화하였다. "
                "가치 지표(value indicator)와 완전한 가치(full value)의 구분을 도입하고, "
                "명료화 반응(clarifying response), 가치 투표, 순위 매기기 등 "
                "구체적인 교실 교수 전략을 제시했다. "
                "전통적 도덕교화(moralizing)에 반대하고 학생의 자율적 가치 선택을 지원하는 "
                "교사의 역할을 새롭게 정의한 저작으로, 미국 도덕교육 혁신의 기폭제가 되었다."
            ),
            "key_concepts": [
                "가치명료화", "7가지 기준", "가치 지표", "완전한 가치",
                "명료화 반응", "가치 투표", "교화 반대", "선택·존중·행동"
            ]
        },
        {
            "id": "raths-values-and-teaching-1978",
            "thinker_id": "raths",
            "title": "가치와 교수: 교실에서 가치 다루기 (개정판)",
            "title_original": "Values and Teaching: Working with Values in the Classroom (2nd ed.)",
            "year": 1978,
            "significance": (
                "1966년 초판을 보완·확장한 개정판. "
                "가치명료화의 이론적 기초를 재정리하고, "
                "1970년대 미국 교육 현장에서의 적용 경험을 반영한 교수 전략을 추가했다. "
                "콜버그 등 비판자들의 문제제기에 대한 응답도 포함되어 있으며, "
                "가치명료화 접근의 한계와 보완 방향을 논의했다."
            ),
            "key_concepts": [
                "가치명료화 심화", "교실 활동 전략", "비판에 대한 응답", "교사의 역할"
            ]
        },
        {
            "id": "raths-meeting-needs-of-children",
            "thinker_id": "raths",
            "title": "아동의 요구 충족",
            "title_original": "Meeting the Needs of Children",
            "year": 1948,
            "significance": (
                "래스의 초기 저작으로, 듀이의 영향 아래 아동의 심리적·사회적 요구에 초점을 맞춘 교육을 탐구했다. "
                "가치교육에 앞서 교사가 학생의 기본 요구(need)를 이해하고 충족하는 것이 중요하다는 "
                "래스의 교육 철학의 원형을 보여주는 저작이다."
            ),
            "key_concepts": [
                "아동의 요구", "교육적 민감성", "실용주의 교육", "듀이의 영향"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """래스 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 가치명료화의 7가지 기준
        {
            "id": "raths-claim-001",
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "source_detail": "Values and Teaching (1966), Chapter 2",
            "claim": (
                "진정한 가치(full value)는 선택(choosing), 소중히 여김(prizing), 행동(acting)의 "
                "세 과정과 7가지 기준을 모두 충족해야 한다. "
                "선택의 기준: (1) 자유롭게 선택, (2) 여러 대안들 중에서 선택, "
                "(3) 각 대안의 결과를 충분히 숙고한 후 선택. "
                "존중의 기준: (4) 선택한 것을 소중히 여기고 기뻐함, (5) 공적으로 확언(affirm). "
                "행동의 기준: (6) 그 선택에 따라 행동, (7) 생활 속에서 반복적으로 행동."
            ),
            "original_text": (
                "We define values as those elements that show the following: (1) are freely chosen; "
                "(2) are chosen from alternatives; (3) are chosen after thoughtful consideration "
                "of the consequences of each alternative; (4) are prized and cherished; "
                "(5) are publicly affirmed; (6) are acted upon; and (7) are part of a repeated pattern of life."
            ),
            "explanation": (
                "래스는 가치를 진정한 가치(full value)와 가치 지표(value indicator)로 구분한다. "
                "선택(choosing) 과정은 자유, 대안, 결과 숙고의 세 기준으로 구성된다. "
                "소중히 여김(prizing) 과정은 내적 존중과 공적 확언의 두 기준으로 구성된다. "
                "행동(acting) 과정은 실제 행동과 반복적 행동의 두 기준으로 구성된다. "
                "7가지 기준을 모두 충족해야만 비로소 진정한 가치로 인정된다. "
                "하나라도 충족되지 않으면 태도, 믿음, 관심 등 가치 지표에 불과하다."
            ),
            "argument": (
                "래스는 학생들이 표현하는 많은 것들—태도, 믿음, 열망, 관심—이 "
                "진정한 가치가 아닌 가치 지표임을 지적한다. "
                "진정한 가치는 (1) 강압이나 타인의 시선 없이 스스로 선택되어야 하고, "
                "(2) 여러 선택지를 비교 검토한 결과여야 하며, "
                "(3) 결과를 알면서도 선택한 것이어야 하고, "
                "(4) 실제 삶에서 반복적으로 실현되어야 한다. "
                "이 엄격한 기준을 통해 래스는 가치를 단순한 선호나 충동과 구별하고, "
                "진정한 가치만이 삶에 방향과 의미를 부여한다고 주장했다."
            ),
            "counterpoint": (
                "콜버그는 래스의 7가지 기준이 가치의 '형식'에만 집중하고 "
                "'내용'(어떤 가치가 더 옳은가)에 대한 판단을 회피한다고 비판했다. "
                "예를 들어, 7가지 기준을 모두 충족한 나치의 가치도 진정한 가치로 인정해야 하는가라는 문제가 생긴다. "
                "스트라우만(Straughan) 등도 내용 없는 형식적 기준으로는 "
                "도덕적 발달의 방향성을 제시할 수 없다고 비판했다."
            ),
            "context": (
                "1960년대 미국의 전통적 도덕교육은 교사가 학생에게 '올바른' 가치를 가르치는 "
                "교화(moralizing) 방식이 주류였다. 래스는 이러한 방식이 학생의 자율성을 침해하고, "
                "가치 선택의 과정을 무시한다고 보고 대안적 접근을 제시했다."
            ),
            "keywords": ["7가지 기준", "가치명료화", "선택·존중·행동", "완전한 가치", "가치 지표"],
            "verified": False
        },
        # CLAIM-002: 가치 지표(value indicator)와 완전한 가치(full value)의 구분
        {
            "id": "raths-claim-002",
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "source_detail": "Values and Teaching (1966), Chapter 2-3",
            "claim": (
                "7가지 기준을 모두 충족하지 못하는 것은 '가치 지표(value indicator)'에 불과하며, "
                "태도(attitudes), 믿음(beliefs), 활동(activities), 관심(interests), "
                "느낌(feelings), 열망(aspirations), 걱정(worries), 문제(problems)가 이에 해당한다. "
                "가치 지표는 진정한 가치로 발전할 수 있는 잠재적 소재이다."
            ),
            "explanation": (
                "래스는 학생들이 표현하는 대부분의 것들이 가치 지표임에 주목한다. "
                "예를 들어, '나는 평화를 원한다'고 말하지만 평화를 위해 아무런 행동도 하지 않는다면, "
                "이는 열망(aspiration)이라는 가치 지표에 불과하다. "
                "교사의 역할은 이러한 가치 지표들을 명료화 과정을 통해 "
                "진정한 가치로 발전하도록 도와주는 것이다. "
                "이를 통해 학생은 자신이 실제로 무엇을 가치 있게 여기는지 더 명확히 이해할 수 있다."
            ),
            "argument": (
                "래스는 사람들이 실제로는 일관되게 행동하지 않으면서도 "
                "특정 가치를 가졌다고 믿는 경우가 많다는 점을 지적한다. "
                "진정한 가치는 단순히 마음 속에 있는 것이 아니라, "
                "삶 속에서 반복적으로 실현되어야 한다. "
                "교사는 학생의 가치 지표에 관심을 기울이고, "
                "명료화 질문을 통해 학생이 스스로 진정한 가치를 발견하도록 안내해야 한다."
            ),
            "counterpoint": (
                "비판자들은 가치 지표와 완전한 가치의 구분이 너무 엄격하여 "
                "대부분의 가치관이 가치 지표로 격하될 수 있다고 지적한다. "
                "또한 7가지 기준을 모두 충족하는지 여부를 어떻게 판단할 것인지에 대한 "
                "명확한 기준이 없다는 비판도 있다."
            ),
            "context": (
                "래스는 학생들의 무관심, 무기력, 규칙 위반, 극단적 행동 등의 문제가 "
                "명료화되지 않은 가치로 인한 혼란에서 비롯된다고 보았다. "
                "가치가 명료화될수록 학생들은 삶에 목적의식과 방향성을 갖게 된다."
            ),
            "keywords": ["가치 지표", "완전한 가치", "태도", "믿음", "열망", "가치명료화"],
            "verified": False
        },
        # CLAIM-003: 교화(indoctrination) 반대
        {
            "id": "raths-claim-003",
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "source_detail": "Values and Teaching (1966), Chapter 1",
            "claim": (
                "교사는 학생에게 특정 가치를 주입하거나 교화(indoctrination)해서는 안 된다. "
                "도덕설교(moralizing), 모범 제시(modeling), 규칙 설정(rule setting)을 통한 "
                "직접적 가치 전달 방식은 학생의 자율적 가치 형성을 방해한다."
            ),
            "explanation": (
                "래스는 전통적 도덕교육의 세 가지 방식—교화, 도덕설교, 모범 제시—을 비판한다. "
                "이 방식들은 교사가 '옳다'고 생각하는 가치를 학생에게 일방적으로 전달하려 한다. "
                "그러나 가치는 외부에서 강요될 수 없으며, "
                "개인이 스스로의 경험과 성찰을 통해 선택하고 형성해야 한다. "
                "교화는 학생의 비판적 사고를 억압하고, 진정한 가치 내면화를 방해한다."
            ),
            "argument": (
                "래스의 논증은 두 가지 전제에 기초한다. "
                "첫째, 민주주의 사회에서는 다양한 가치가 공존하므로 어떤 가치가 '옳은'지 단정할 수 없다. "
                "둘째, 진정한 가치는 자유로운 선택의 과정을 통해서만 형성된다. "
                "따라서 교사가 특정 가치를 주입하는 것은 민주주의 원리에 반하며, "
                "진정한 가치 형성의 과정을 왜곡한다."
            ),
            "counterpoint": (
                "콜버그는 래스의 반교화 입장이 지나친 가치 상대주의(value relativism)를 초래한다고 비판했다. "
                "교사가 어떤 가치도 직접 가르치지 않는다면, "
                "학생은 도덕적으로 더 성숙한 가치를 발달시킬 기회를 잃는다. "
                "리코나(Lickona)도 래스의 접근이 도덕적 방향성 없는 교육으로 귀결될 수 있다고 비판했다."
            ),
            "context": (
                "1960년대 미국 사회는 인권운동, 베트남 전쟁 반대 운동 등 가치 충돌이 극심한 시기였다. "
                "래스는 이러한 사회적 맥락에서 어떤 단일한 가치 체계도 "
                "모든 학생에게 강요되어서는 안 된다고 보았다."
            ),
            "keywords": ["교화 반대", "도덕설교", "가치 주입", "자율성", "민주주의 교육"],
            "verified": False
        },
        # CLAIM-004: 명료화 반응(clarifying response)
        {
            "id": "raths-claim-004",
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "source_detail": "Values and Teaching (1966), Chapter 4",
            "claim": (
                "교사는 학생의 가치 관련 발언에 판단 없이 반응하는 '명료화 반응(clarifying response)'을 사용해야 한다. "
                "명료화 반응은 학생이 스스로 자신의 생각을 더 깊이 탐색하도록 돕는 비지시적 개입이다. "
                "교사는 학생의 가치에 동의하거나 반대하지 않고, 개방형 질문으로 성찰을 촉진한다."
            ),
            "explanation": (
                "명료화 반응의 예시: "
                "'당신이 그것을 자유롭게 선택했나요?' "
                "'다른 대안들도 생각해보았나요?' "
                "'그것을 선택하면 어떤 일이 일어날지 생각해보셨나요?' "
                "'이것이 당신에게 정말 중요한가요?' "
                "'그 생각을 다른 사람들에게도 이야기할 의향이 있나요?' "
                "'이 믿음에 따라 실제로 행동하고 있나요?' "
                "교사는 학생의 답에 칭찬하거나 비판하지 않고, 추가 질문으로 탐색을 심화한다."
            ),
            "argument": (
                "명료화 반응이 효과적인 이유: "
                "(1) 학생이 자신의 생각을 언어화하는 과정에서 가치가 명료화된다. "
                "(2) 교사의 판단이 없으므로 학생이 솔직하게 자신의 생각을 표현할 수 있다. "
                "(3) 7가지 기준(선택, 존중, 행동)을 점검하는 질문 형식으로 구성되어 "
                "자연스럽게 가치명료화 과정을 유도한다."
            ),
            "counterpoint": (
                "비판자들은 명료화 반응이 실제 교실에서 적용하기 어렵다고 지적한다. "
                "완전히 중립적인 교사 반응은 비현실적이며, "
                "교사의 침묵이나 중립이 그 자체로 학생에게 메시지를 전달할 수 있다. "
                "또한 명료화 반응만으로는 학생이 도덕적으로 더 성숙한 방향으로 성장하도록 "
                "안내할 수 없다는 비판도 있다."
            ),
            "context": (
                "래스는 교사가 학생의 가치에 대해 즉각적으로 평가하고 교정하려는 경향을 문제로 보았다. "
                "이러한 교사 반응은 학생의 자기탐색을 차단하고, "
                "표면적 순응을 유발할 수 있다고 판단했다."
            ),
            "keywords": ["명료화 반응", "비지시적 개입", "개방형 질문", "가치 탐색", "교사 역할"],
            "verified": False
        },
        # CLAIM-005: 가치 투표(value voting)
        {
            "id": "raths-claim-005",
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "source_detail": "Values and Teaching (1966), Chapter 5",
            "claim": (
                "가치 투표(value voting)는 학생들이 다양한 이슈에 대해 공개적으로 의견을 표명하게 하는 "
                "가치명료화 교수 전략이다. '~하는 사람은 손을 들어보세요'처럼 "
                "공개적 확언(public affirmation)을 통해 학생은 자신의 가치 입장을 명료화한다."
            ),
            "explanation": (
                "가치 투표의 방법: 교사가 '당신은 ~을 믿습니까?', '~을 하겠습니까?' 등의 "
                "질문에 학생들이 손을 들거나, 찬성/반대/미결정으로 응답하게 한다. "
                "이 활동은 7가지 기준 중 '공적으로 확언하기'에 해당한다. "
                "학생은 자신의 입장을 공적으로 표명하면서 "
                "그 가치가 진정으로 자신의 것인지를 성찰하게 된다."
            ),
            "argument": (
                "가치 투표의 교육적 효과: "
                "(1) 자신의 가치를 공개적으로 확언하면서 내면화가 강화된다. "
                "(2) 다른 학생들의 다양한 가치 입장을 인식하고 존중하는 기회가 된다. "
                "(3) 비강압적 방식으로 진행되므로 학생의 자율성을 보장한다. "
                "(4) 빠른 시간 안에 학급 전체가 다양한 주제에 대해 성찰할 수 있다."
            ),
            "counterpoint": (
                "가치 투표는 동조 압력(peer pressure)을 유발할 수 있다는 비판이 있다. "
                "소수 의견을 가진 학생이 집단의 압력으로 자신의 진짜 가치를 표현하지 못할 수 있다. "
                "또한 복잡한 도덕 이슈를 단순한 찬반으로 환원하는 문제도 지적된다."
            ),
            "context": (
                "래스는 학생들이 가치에 대해 추상적으로만 논의하지 않고 "
                "구체적으로 자신의 입장을 표명하고 경험할 기회가 필요하다고 보았다."
            ),
            "keywords": ["가치 투표", "공적 확언", "가치명료화 전략", "교수 전략"],
            "verified": False
        },
        # CLAIM-006: 순위 매기기(ranking) 전략
        {
            "id": "raths-claim-006",
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "source_detail": "Values and Teaching (1966), Chapter 5",
            "claim": (
                "순위 매기기(ranking) 전략은 학생들에게 여러 선택지나 가치들의 우선순위를 정하게 함으로써 "
                "자신이 실제로 무엇을 더 중요하게 여기는지 명료화하는 교수 전략이다. "
                "대안들 중에서 선택하는 과정(7가지 기준의 두 번째)을 실습하게 한다."
            ),
            "explanation": (
                "순위 매기기의 예: '다음 세 가지 삶의 방식 중 당신이 가장 선호하는 순서대로 "
                "1, 2, 3으로 번호를 매겨보세요.' "
                "이 활동을 통해 학생은 단순히 '좋다/나쁘다'가 아니라 "
                "여러 가치들 사이의 상대적 중요성을 탐색하게 된다. "
                "가치 간의 충돌이 드러나면서 학생은 더 깊은 수준의 가치 성찰을 경험한다."
            ),
            "argument": (
                "순위 매기기는 7가지 기준 중 '대안들 중에서 선택'을 구체화한 전략이다. "
                "단일 가치에 대한 찬반보다 복수의 가치를 비교하는 경험이 "
                "더 깊은 가치 명료화를 유도한다. "
                "학생은 자신의 순위 이유를 설명하면서 자신의 가치 체계를 더 명확히 인식하게 된다."
            ),
            "counterpoint": (
                "비판자들은 순위 매기기가 가치를 단순히 개인적 선호의 순서로 환원한다고 지적한다. "
                "일부 가치들은 비교하기보다 독립적으로 평가해야 할 수 있으며, "
                "순위를 매기는 행위 자체가 학생의 실제 가치 체계를 왜곡할 수 있다."
            ),
            "context": (
                "래스는 학생들이 가치들이 충돌할 때 어떻게 선택하는지를 탐색하게 하는 것이 "
                "가치교육의 핵심이라고 보았다."
            ),
            "keywords": ["순위 매기기", "가치명료화 전략", "대안 선택", "교수 전략"],
            "verified": False
        },
        # CLAIM-007: 콜버그와의 논쟁—가치 상대주의 비판에 대한 입장
        {
            "id": "raths-claim-007",
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1978",
            "source_detail": "Values and Teaching (2nd ed., 1978)",
            "claim": (
                "가치명료화는 가치 상대주의를 조장한다는 콜버그의 비판에 대해, "
                "래스는 가치명료화의 목표가 특정 가치의 선택이 아니라 "
                "가치 선택 과정의 질을 높이는 것임을 강조했다. "
                "어떤 가치를 선택할지는 학생의 자율에 달려 있으나, "
                "선택의 과정이 자유롭고 숙고적이어야 한다."
            ),
            "explanation": (
                "콜버그는 가치명료화가 '모든 가치는 동등하다'는 상대주의를 암묵적으로 전제한다고 비판했다. "
                "이에 대해 래스 측은 가치명료화가 특정 가치를 지지하거나 반대하지 않음으로써 "
                "학생의 자율성을 존중하는 것이라고 반론했다. "
                "가치명료화는 '무엇이 옳은가'의 문제보다 "
                "'어떻게 가치를 형성하는가'의 과정에 집중한다."
            ),
            "argument": (
                "래스의 입장: (1) 민주주의 사회에서 교육자는 학생에게 특정 가치를 강요할 권한이 없다. "
                "(2) 가치 선택 과정의 질—자유, 대안 검토, 결과 숙고—을 높이는 것이 교육의 역할이다. "
                "(3) 학생이 충분한 정보와 자유 속에서 선택한 가치는, 교사가 주입한 가치보다 "
                "더 안정적이고 지속적으로 실현된다."
            ),
            "counterpoint": (
                "콜버그의 반론: 가치명료화는 나치즘을 자유롭게 선택한 학생도 "
                "진정한 가치를 가졌다고 인정해야 하는 문제에 봉착한다. "
                "도덕적 발달은 방향이 있어야 하며, "
                "더 성숙한 도덕적 추론을 향한 자극이 필요하다. "
                "리코나 역시 가치명료화가 도덕적 덕목 교육의 역할을 포기했다고 비판했다."
            ),
            "context": (
                "1970년대 미국 도덕교육 학계에서 가치명료화와 콜버그의 도덕발달 단계론은 "
                "두 주요 접근으로 경쟁하면서 활발한 논쟁을 벌였다. "
                "이 논쟁은 도덕교육에서 '과정' 대 '내용', '자율성' 대 '방향성'의 긴장을 반영한다."
            ),
            "keywords": ["가치 상대주의", "콜버그 비판", "가치 선택 과정", "자율성 대 방향성"],
            "verified": False
        },
        # CLAIM-008: 듀이의 영향—경험과 민주주의
        {
            "id": "raths-claim-008",
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "source_detail": "Values and Teaching (1966), Chapter 1",
            "claim": (
                "래스의 가치명료화 이론은 듀이의 실용주의 교육철학, 특히 "
                "'경험으로부터의 학습(learning from experience)'과 민주주의 교육 이념의 영향을 깊이 받았다. "
                "가치는 삶의 경험을 통해 형성·검증되며, "
                "민주주의 교육에서 자율적 가치 형성 능력은 핵심 역량이다."
            ),
            "explanation": (
                "듀이는 교육이 삶의 경험과 분리될 수 없으며, "
                "학생이 능동적으로 경험하고 성찰하는 과정에서 진정한 학습이 이루어진다고 보았다. "
                "래스는 이를 계승하여 가치 역시 경험적 과정—선택, 경험, 성찰, 재선택—을 통해 형성된다고 보았다. "
                "민주주의 사회에서 가치 다원주의를 인정하는 래스의 입장도 듀이에서 비롯된다."
            ),
            "argument": (
                "래스의 논거: (1) 가치는 추상적으로 전달될 수 없으며 구체적 경험 속에서 형성된다(듀이의 경험 교육). "
                "(2) 민주주의 사회는 다양한 가치가 공존하므로, "
                "교육은 자율적 가치 선택 능력을 길러야 한다(듀이의 민주주의 교육). "
                "(3) 반성적 사고(reflective thinking)가 가치 형성의 핵심이다."
            ),
            "counterpoint": (
                "듀이 자신은 가치의 완전한 상대주의를 지지하지는 않았다. "
                "듀이는 민주적 과정에서 공유될 수 있는 가치들이 있다고 보았으며, "
                "래스가 듀이를 지나치게 상대주의적으로 해석했다는 견해도 있다."
            ),
            "context": (
                "래스가 활동하던 뉴욕 대학교는 듀이의 영향이 강한 교육학 연구 환경이었다. "
                "래스는 듀이의 진보주의 교육 전통 안에서 가치교육이라는 새로운 영역을 개척했다."
            ),
            "keywords": ["듀이 영향", "경험으로부터 학습", "민주주의 교육", "실용주의"],
            "verified": False
        },
        # CLAIM-009: 가치 혼란(value confusion)과 학생 행동 문제
        {
            "id": "raths-claim-009",
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "source_detail": "Values and Teaching (1966), Chapter 1",
            "claim": (
                "가치가 명료화되지 않은 학생들은 무관심(apathy), 무기력(flightiness), "
                "지나친 복종(overdissent), 역할 연기(role-playing), "
                "일관성 없음(inconsistency) 등의 행동 문제를 보인다. "
                "가치명료화는 이러한 가치 혼란에서 비롯된 문제를 해결하는 교육적 처방이다."
            ),
            "explanation": (
                "래스는 학생의 많은 행동 문제가 가치 혼란(value confusion)에서 비롯된다고 보았다. "
                "가치가 명료하지 않으면 학생은 삶의 방향을 잡지 못하고 표류한다. "
                "무관심한 학생은 아무것도 중요하게 여기지 못하고, "
                "무기력한 학생은 하나의 것에서 다른 것으로 방황한다. "
                "지나친 복종은 자신의 가치를 형성하지 못하고 타인을 모방하는 것이다."
            ),
            "argument": (
                "래스의 인과 관계 주장: "
                "가치 혼란 → 삶의 방향 부재 → 다양한 행동 문제 발생. "
                "역으로, 가치명료화 → 삶의 방향과 의미 형성 → 행동 문제 감소. "
                "교사가 학생의 가치 혼란을 인식하고 명료화를 도울 때, "
                "학생의 전반적인 성장과 적응이 이루어진다."
            ),
            "counterpoint": (
                "비판자들은 학생의 행동 문제가 가치 혼란만으로 설명될 수 없으며, "
                "사회경제적 요인, 발달 단계, 가정 환경 등 복합적 원인이 있다고 지적한다. "
                "또한 가치명료화만으로 복잡한 행동 문제가 해결된다는 래스의 주장이 "
                "지나치게 단순하다는 비판도 있다."
            ),
            "context": (
                "1960년대 미국 교육에서 학생 무관심, 학교 이탈, 약물 문제 등이 심각한 사회 문제였다. "
                "래스는 이러한 문제들의 근원을 가치 혼란에서 찾고 교육적 해결책을 제시했다."
            ),
            "keywords": ["가치 혼란", "행동 문제", "무관심", "무기력", "가치명료화 효과"],
            "verified": False
        },
        # CLAIM-010: 가치명료화와 교사의 중립성
        {
            "id": "raths-claim-010",
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "source_detail": "Values and Teaching (1966), Chapter 4",
            "claim": (
                "가치명료화 접근에서 교사는 중립적 촉진자(neutral facilitator)의 역할을 해야 한다. "
                "교사는 자신의 가치를 학생에게 강요하지 않고, "
                "학생이 스스로 가치를 탐색하는 과정을 돕는 안내자 역할에 머물러야 한다."
            ),
            "explanation": (
                "교사의 중립성이란 교사가 특정 가치를 옳거나 그르다고 판단하지 않는다는 것이다. "
                "명료화 반응에서 교사는 학생의 답에 대해 칭찬하거나 비판하지 않는다. "
                "교사는 '좋은 답'과 '나쁜 답'을 구분하지 않고, "
                "학생이 더 깊이 탐색하도록 돕는 질문만 던진다."
            ),
            "argument": (
                "교사 중립성의 근거: "
                "(1) 교사는 전문적 권위를 가지므로, 교사의 가치 표현은 학생에게 큰 영향을 미친다. "
                "(2) 학생이 교사에게 인정받으려 '올바른' 답을 말하는 순응 행동을 방지해야 한다. "
                "(3) 가치는 자유롭게 선택되어야 하므로, 교사의 권위적 표현은 이를 방해한다."
            ),
            "counterpoint": (
                "완전한 교사 중립성은 비현실적이다. "
                "교사가 어떤 주제를 선택하고 어떤 질문을 던지는지 자체가 이미 가치 판단을 담고 있다. "
                "또한 인종차별, 폭력 등 명백히 잘못된 가치에 대해서도 "
                "교사가 중립을 지켜야 하는가라는 문제가 생긴다."
            ),
            "context": (
                "래스는 교사가 학생에게 권위적으로 가치를 주입하는 전통적 교육 방식을 "
                "관찰하면서 이에 대한 대안적 교사 역할을 제안했다."
            ),
            "keywords": ["교사 중립성", "촉진자", "교사 역할", "가치명료화", "비지시적"],
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """래스 키워드 데이터 입력."""
    keywords = [
        {
            "id": "kw-values-clarification",
            "term": "가치명료화",
            "term_en": "values clarification",
            "definition": (
                "래스, 하민, 사이먼이 체계화한 도덕교육 접근법. "
                "선택(choosing), 소중히 여김(prizing), 행동(acting)의 세 과정과 "
                "7가지 기준을 통해 개인이 자신의 가치를 스스로 명료화하도록 돕는다. "
                "교사는 특정 가치를 가르치거나 주입하지 않고, "
                "학생의 가치 탐색 과정을 촉진하는 역할을 한다."
            ),
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "related_terms": ["7가지 기준", "가치 지표", "명료화 반응", "교화 반대"]
        },
        {
            "id": "kw-seven-criteria",
            "term": "7가지 기준",
            "term_en": "seven criteria of values",
            "definition": (
                "진정한 가치(full value)를 판별하는 래스의 7가지 기준. "
                "선택(choosing): (1) 자유롭게 선택, (2) 대안들 중에서 선택, (3) 결과 숙고 후 선택. "
                "소중히 여김(prizing): (4) 선택을 소중히 여기고 기뻐함, (5) 공적으로 확언. "
                "행동(acting): (6) 선택에 따라 행동, (7) 반복적으로 행동. "
                "7가지 기준을 모두 충족해야만 진정한 가치이며, 그렇지 않으면 가치 지표이다."
            ),
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "related_terms": ["가치명료화", "완전한 가치", "가치 지표", "선택·존중·행동"]
        },
        {
            "id": "kw-value-indicator",
            "term": "가치 지표",
            "term_en": "value indicator",
            "definition": (
                "7가지 기준을 모두 충족하지 못하는 것으로, "
                "진정한 가치(full value)와 구별되는 개념. "
                "태도(attitudes), 믿음(beliefs), 관심(interests), "
                "느낌(feelings), 열망(aspirations), 걱정(worries) 등이 해당한다. "
                "가치 지표는 진정한 가치로 발전할 수 있는 소재가 된다."
            ),
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "related_terms": ["완전한 가치", "7가지 기준", "가치명료화"]
        },
        {
            "id": "kw-full-value",
            "term": "완전한 가치",
            "term_en": "full value",
            "definition": (
                "7가지 기준을 모두 충족하는 진정한 가치. "
                "자유롭게 선택되고, 대안들 중에서 선택되며, 결과를 숙고한 뒤 선택되고, "
                "소중히 여겨지며, 공적으로 확언되고, 행동으로 실현되며, 반복적으로 나타나는 것. "
                "가치 지표(value indicator)와 대비되는 개념."
            ),
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "related_terms": ["가치 지표", "7가지 기준", "가치명료화"]
        },
        {
            "id": "kw-indoctrination-anti",
            "term": "교화 반대",
            "term_en": "anti-indoctrination",
            "definition": (
                "래스 가치명료화의 핵심 원칙으로, 교사가 학생에게 특정 가치를 주입하거나 강요해서는 안 된다는 입장. "
                "도덕설교(moralizing), 모범 제시, 규칙 설정 등을 통한 직접적 가치 전달을 거부한다. "
                "이 원칙은 콜버그로부터 가치 상대주의를 조장한다는 비판을 받았다."
            ),
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "related_terms": ["가치명료화", "교사 중립성", "가치 상대주의"]
        },
        {
            "id": "kw-clarifying-response",
            "term": "명료화 반응",
            "term_en": "clarifying response",
            "definition": (
                "교사가 학생의 가치 관련 발언에 판단 없이 반응하는 기법. "
                "개방형 질문을 통해 학생이 스스로 자신의 생각을 탐색하도록 돕는다. "
                "예: '다른 대안들도 생각해보았나요?', '그 믿음에 따라 행동하고 있나요?' "
                "교사는 학생의 답에 칭찬하거나 비판하지 않고 추가 탐색을 촉진한다."
            ),
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "related_terms": ["가치명료화", "교사 중립성", "비지시적 개입", "개방형 질문"]
        },
        {
            "id": "kw-value-voting",
            "term": "가치 투표",
            "term_en": "value voting",
            "definition": (
                "학생들이 다양한 이슈에 대해 공개적으로 의견을 표명하게 하는 가치명료화 교수 전략. "
                "'~하는 사람은 손을 들어보세요'처럼 공적 확언(public affirmation)을 통해 "
                "학생이 자신의 가치 입장을 명료화하고 다른 학생들의 다양한 입장을 인식하게 한다. "
                "7가지 기준 중 '공적으로 확언하기'에 해당하는 활동이다."
            ),
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "related_terms": ["가치명료화", "공적 확언", "7가지 기준", "교수 전략"]
        },
        {
            "id": "kw-ranking",
            "term": "순위 매기기",
            "term_en": "ranking",
            "definition": (
                "학생들에게 여러 선택지나 가치들의 우선순위를 정하게 하여 "
                "자신이 실제로 무엇을 더 중요하게 여기는지 명료화하는 가치명료화 교수 전략. "
                "7가지 기준 중 '대안들 중에서 선택하기'를 구체화한 활동이다."
            ),
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "related_terms": ["가치명료화", "대안 선택", "7가지 기준", "교수 전략"]
        },
        {
            "id": "kw-value-confusion",
            "term": "가치 혼란",
            "term_en": "value confusion",
            "definition": (
                "가치가 명료화되지 않은 상태로, 래스에 따르면 학생의 무관심, 무기력, "
                "역할 연기, 일관성 없음 등 다양한 행동 문제의 근원이다. "
                "가치명료화 교육을 통해 가치 혼란이 해소되면 "
                "학생은 삶의 방향과 의미를 찾고 행동 문제가 감소한다."
            ),
            "thinker_id": "raths",
            "work_id": "raths-values-and-teaching-1966",
            "related_terms": ["가치명료화", "무관심", "가치명료화 효과"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """래스 관계 데이터 입력."""
    relations = [
        {
            "from_thinker": "dewey",
            "to_thinker": "raths",
            "type": "influenced",
            "description": (
                "존 듀이의 실용주의 교육철학, 특히 경험 중심 교육론과 민주주의 교육 이념이 "
                "래스의 가치명료화 이론의 철학적 토대가 되었다. "
                "래스는 가치 역시 경험적 과정을 통해 형성된다는 듀이의 관점을 계승하였으며, "
                "교화 반대 입장도 듀이의 민주주의 교육 이념에 기반한다."
            ),
            "evidence": "Values and Teaching (1966), Chapter 1 — 듀이 교육철학 명시적 언급"
        },
        {
            "from_thinker": "kohlberg",
            "to_thinker": "raths",
            "type": "criticized",
            "description": (
                "콜버그는 래스의 가치명료화가 가치 상대주의(value relativism)를 조장한다고 비판했다. "
                "가치명료화는 어떤 가치도 다른 가치보다 도덕적으로 우월하지 않다고 암묵적으로 전제하는데, "
                "이는 도덕적 발달의 방향성을 제거하여 교육이 아닌 중립화에 불과하다는 것이다. "
                "콜버그는 교육은 더 성숙한 도덕 추론 단계로 학생을 이끌어야 한다고 주장했다."
            ),
            "evidence": "Kohlberg, 'The Cognitive-Developmental Approach to Moral Education' (1975)"
        },
        {
            "from_thinker": "raths",
            "to_thinker": "kohlberg",
            "type": "criticized",
            "description": (
                "래스는 콜버그의 도덕발달 단계론이 학생에게 '올바른' 도덕 추론 방식을 "
                "교사가 유도한다는 점에서 일종의 교화라고 비판했다. "
                "콜버그의 접근은 자유로운 가치 선택을 방해하고, "
                "학생을 특정 도덕적 방향으로 이끌려는 시도라는 것이다."
            ),
            "evidence": "Values and Teaching (2nd ed., 1978) — 콜버그 비판 관련 논의"
        },
        {
            "from_thinker": "raths",
            "to_thinker": "simon",
            "type": "developed",
            "description": (
                "래스는 메릴 하민, 시드니 사이먼과 함께 가치명료화 이론을 공동 개발했다. "
                "사이먼은 이후 「가치명료화: 교사와 학생을 위한 실천 지침」(1972)을 통해 "
                "가치명료화를 미국 학교 현장에 더욱 광범위하게 보급했다."
            ),
            "evidence": "Values and Teaching (1966) — Raths, Harmin, Simon 공저"
        }
    ]

    for i, rel in enumerate(relations):
        rel_id = f"raths-relation-{i+1:03d}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id}: {result['result']}")

    return len(relations)


def main():
    print("=== 루이스 래스(Louis Raths) 데이터 입력 시작 ===")
    client = get_client()

    try:
        # 1. 분야 확인
        ensure_field(client)

        # 2. 사상가 입력
        insert_thinker(client)

        # 3. 저서 입력
        n_works = insert_works(client)
        print(f"[완료] 저서 {n_works}개 입력")

        # 4. 주장 입력
        n_claims = insert_claims(client)
        print(f"[완료] 주장 {n_claims}개 입력")

        # 5. 키워드 입력
        n_keywords = insert_keywords(client)
        print(f"[완료] 키워드 {n_keywords}개 입력")

        # 6. 관계 입력
        n_relations = insert_relations(client)
        print(f"[완료] 관계 {n_relations}개 입력")

        print("\n=== 래스 데이터 입력 완료 ===")
        print(f"  사상가: 1명")
        print(f"  저서:   {n_works}개")
        print(f"  주장:   {n_claims}개")
        print(f"  키워드: {n_keywords}개")
        print(f"  관계:   {n_relations}개")

    finally:
        close_client(client)


if __name__ == "__main__":
    main()
