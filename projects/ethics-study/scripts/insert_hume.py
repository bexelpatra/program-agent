"""데이비드 흄(David Hume) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS
)


def insert_thinker(client):
    """흄 사상가 데이터 입력."""
    doc = {
        "id": "hume",
        "name": "데이비드 흄",
        "name_en": "David Hume",
        "field": "western_ethics",
        "era": "근대 영국·스코틀랜드",
        "birth_year": 1711,
        "death_year": 1776,
        "background": (
            "스코틀랜드 에든버러에서 태어나 에든버러 대학교에서 수학하고, "
            "법학을 공부했으나 철학에 전념하게 되었다. "
            "프랑스 앙주(La Flèche)에 3년 체류하며(1734~1737) 데카르트·말브랑슈 등 합리론 전통을 직접 접하고, "
            "이에 대한 비판으로서 경험론적 인식론을 정립하는 계기로 삼았다. "
            "28세에 출판한 '인간 본성에 관한 논고'(Treatise of Human Nature, 1739~1740)는 "
            "당시 거의 주목받지 못했지만 이후 근대 철학의 전환점이 된 저작이다. "
            "에든버러 대학 도덕철학 교수직 지원에 두 차례 실패하였는데, 무신론 혐의가 주된 이유였다. "
            "외교관 보좌역, 영국 대사관 서기 등 실무 직책을 거쳤으며, "
            "아담 스미스(Adam Smith)와 깊은 우정을 나눈 것으로 유명하다. "
            "생전에 발표를 보류한 '자연종교에 관한 대화'(Dialogues Concerning Natural Religion)는 "
            "사후 1779년에 출판되었다."
        ),
        "core_philosophy": (
            "영국 경험론(Locke·Berkeley)을 극한까지 밀고 나가 '온건한 회의주의(mitigated scepticism)'에 도달했다. "
            "모든 관념은 선행하는 인상(impression)에서 파생된다는 원리를 출발점으로 삼아, "
            "인과관계·자아·외부 세계·신의 존재에 관한 형이상학적 주장을 해체했다. "
            "인과관계는 사건들 사이의 필연적 연결이 아니라 항상 선행(constant conjunction)에서 "
            "형성된 '심리적 기대(custom/habit)'일 뿐임을 논증했으며(인과관계 비판), "
            "이는 과학적 귀납 추론의 정당성 문제(귀납 문제)로 이어졌다. "
            "윤리학에서는 이성이 단독으로 도덕적 의무를 낳을 수 없고 "
            "감정(sentiment·passion)만이 행위를 동기화할 수 있다는 도덕 감정주의를 주장했으며, "
            "'사실'에서 '당위'를 논리적으로 도출할 수 없다는 '흄의 단두대(Hume's Guillotine)'는 "
            "현대 메타윤리학의 출발점이 되었다."
        ),
        "philosophical_journey": (
            "초기(1730s): 합리론을 극복하고 경험론을 급진적으로 체계화한 '인간 본성에 관한 논고'(1739~1740)를 "
            "출판했지만 '사산아처럼 출판되었다'고 회고할 만큼 무반응이었다. "
            "중기(1740s~1750s): '도덕 원리 탐구'(1751)와 '인간 이해력 탐구'(1748)로 "
            "자신의 핵심 주장을 더 접근하기 쉽게 재서술했다. "
            "흄 스스로 '도덕 원리 탐구'를 자신의 저작 중 최고로 평가했다. "
            "'정치론 소론'(1741~42)을 통해 정치경제학과 역사 서술에도 기여했다. "
            "말년(1754~1776): 6권짜리 '영국의 역사'(History of England, 1754~1761)로 당대에 "
            "베스트셀러 작가가 되어 생전의 명성을 얻었다. "
            "사후 출판된 '자연종교에 관한 대화'(1779)에서 신의 존재 증명과 종교적 기적을 정면으로 비판했다."
        ),
        "keywords": [
            "인상과 관념",
            "인과관계 비판",
            "귀납 문제",
            "도덕 감정주의",
            "사실-당위 논리 간극",
            "자아 번들 이론",
            "온건한 회의주의",
            "자연적 덕과 인위적 덕"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="hume", document=doc)
    print(f"[thinker] hume: {result['result']}")
    return result


def insert_works(client):
    """흄 저서 데이터 입력."""
    works = [
        {
            "id": "hume-treatise",
            "thinker_id": "hume",
            "title": "인간 본성에 관한 논고",
            "title_original": "A Treatise of Human Nature",
            "year": 1739,
            "significance": (
                "흄의 철학 체계 전체를 담은 주저(主著). "
                "인식론(Book I: Of the Understanding), 감정론(Book II: Of the Passions), "
                "도덕론(Book III: Of Morals)으로 구성된다. "
                "인상·관념 구분, 인과관계 비판, 귀납 문제, 자아 번들 이론, 도덕 감정주의, "
                "사실-당위 논리 간극 등 흄 철학의 핵심 테제가 모두 여기에 최초로 제시된다. "
                "출판 당시에는 주목받지 못했으나, 이후 칸트의 비판 철학을 촉발한 결정적 저작이다."
            ),
            "key_concepts": [
                "인상과 관념", "인과관계 비판", "귀납 문제", "자아 번들 이론",
                "도덕 감정주의", "사실-당위 논리 간극", "자연적·인위적 덕"
            ]
        },
        {
            "id": "hume-enquiry-understanding",
            "thinker_id": "hume",
            "title": "인간 이해력 탐구",
            "title_original": "An Enquiry Concerning Human Understanding",
            "year": 1748,
            "significance": (
                "'인간 본성에 관한 논고' Book I의 핵심 논증을 더 명확하고 접근하기 쉽게 재서술한 저작. "
                "인과관계·필연적 연결·귀납 문제(Section 4~7), 기적 비판(Section 10), "
                "섭리와 미래 삶에 대한 회의적 논증(Section 11)을 포함한다. "
                "Section 12에서 '온건한 회의주의(mitigated scepticism)'를 제시한다. "
                "임용시험에서 흄의 인식론적 주장을 확인하는 주요 출처이다."
            ),
            "key_concepts": [
                "인과관계", "필연적 연결", "귀납 문제", "기적 비판",
                "온건한 회의주의", "관계 of ideas vs matters of fact"
            ]
        },
        {
            "id": "hume-enquiry-morals",
            "thinker_id": "hume",
            "title": "도덕 원리 탐구",
            "title_original": "An Enquiry Concerning the Principles of Morals",
            "year": 1751,
            "significance": (
                "흄 스스로 자신의 저작 중 '비교할 수 없이 최고'라고 평가한 도덕철학 저작. "
                "'인간 본성에 관한 논고' Book III의 도덕론을 더 완숙하게 재서술했다. "
                "공감(sympathy)·유용성(utility)·자연적 덕을 중심으로 도덕 감정주의를 전개하며, "
                "인위적 덕(정의)을 사회적 약속과 유용성에서 도출한다. "
                "공리주의(벤담)에 영향을 준 저작으로도 중요하다."
            ),
            "key_concepts": [
                "도덕 감정주의", "공감", "유용성", "자연적 덕", "인위적 덕",
                "정의", "덕 윤리"
            ]
        },
        {
            "id": "hume-dialogues-natural-religion",
            "thinker_id": "hume",
            "title": "자연종교에 관한 대화",
            "title_original": "Dialogues Concerning Natural Religion",
            "year": 1779,
            "significance": (
                "흄이 생전에 출판을 보류하고 사후에 출판된 종교철학 저작. "
                "필로(Philo), 클레안테스(Cleanthes), 데메아(Demea) 세 인물 간의 대화 형식으로, "
                "신의 존재에 대한 설계 논증(design argument)을 정면으로 비판한다. "
                "기적의 불가능성과 악의 문제(problem of evil)를 논하며, "
                "종교적 믿음의 합리적 근거를 해체한다. "
                "서양 무신론·불가지론 전통에서 가장 중요한 저작 중 하나이다."
            ),
            "key_concepts": [
                "설계 논증 비판", "악의 문제", "기적 비판", "종교 회의주의",
                "자연종교", "불가지론"
            ]
        },
        {
            "id": "hume-essays-moral-political",
            "thinker_id": "hume",
            "title": "도덕·정치·문예 소론집",
            "title_original": "Essays, Moral, Political, and Literary",
            "year": 1741,
            "significance": (
                "흄이 일반 독자를 위해 쓴 소론 모음집(1741~1742 초판, 이후 수정 증보). "
                "정치, 경제, 미학, 역사에 관한 다양한 주제를 다루며, "
                "흄을 당대에 유명 저술가로 만든 저작이다. "
                "상업 사회 옹호, 무역 균형론 비판, 국가 부채 문제, 취향의 기준 등을 논한다. "
                "흄의 정치경제학적 사유와 아담 스미스에 대한 영향을 이해하는 데 중요하다."
            ),
            "key_concepts": [
                "상업 사회", "취향의 기준", "정치 평론", "경제론",
                "역사 서술", "공화주의"
            ]
        },
        {
            "id": "hume-history-of-england",
            "thinker_id": "hume",
            "title": "영국의 역사",
            "title_original": "The History of England",
            "year": 1754,
            "significance": (
                "흄이 6권으로 완성한 영국사 저작(1754~1761). "
                "당대 최고의 베스트셀러로 흄에게 생전에 경제적 독립과 명성을 안겨주었다. "
                "휘그(Whig)당 중심의 편향된 역사 서술 전통을 비판하고 "
                "스튜어트 왕조에 상대적으로 균형 잡힌 시각을 취해 논란이 되었다. "
                "경험주의적 역사 방법론을 적용한 사례이자, "
                "흄의 인과론적 사유가 역사 서술에 반영된 저작이다."
            ),
            "key_concepts": [
                "역사 서술", "경험주의적 방법론", "정치사", "영국사",
                "역사적 인과관계", "균형잡힌 역사관"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """흄 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 인상과 관념 구분
        {
            "id": "hume-claim-001",
            "thinker_id": "hume",
            "work_id": "hume-treatise",
            "source_detail": "A Treatise of Human Nature, Book I, Part I, Section 1",
            "claim": (
                "모든 지각(perceptions)은 인상(impressions)과 관념(ideas)으로 나뉘며, "
                "관념은 반드시 선행하는 인상에서 파생된다. 인상 없는 관념은 무의미하다."
            ),
            "original_text": (
                "All the perceptions of the human mind resolve themselves into two distinct kinds, "
                "which I shall call IMPRESSIONS and IDEAS. The difference betwixt these consists "
                "in the degrees of force and liveliness, with which they strike upon the mind."
            ),
            "explanation": (
                "흄은 로크의 '관념(idea)' 개념을 인상과 관념으로 세분하여 경험론의 기초를 정밀화했다. "
                "'인상'은 우리가 직접 느끼는 강렬하고 생생한 지각(감각, 감정 등)이고, "
                "'관념'은 인상이 사라진 후 기억이나 상상 속에 남는 희미한 복사본이다. "
                "이 구분으로부터 흄은 '의미 기준(meaning criterion)'을 도출한다: "
                "어떤 개념이 진정한 내용을 가지려면 그에 대응하는 인상이 존재해야 한다. "
                "인과관계·자아·신의 존재처럼 직접 인상으로 추적할 수 없는 형이상학적 개념은 "
                "이 기준에 의해 해체된다."
            ),
            "argument": (
                "(1) 우리의 모든 심적 내용은 인상 또는 관념이다. "
                "(2) 관념은 인상을 약화시킨 복사본이며, 반드시 선행하는 인상이 있어야 한다. "
                "(예외: 복합 관념은 단순 관념들의 조합이지만, 그 단순 관념 각각은 인상에서 유래한다.) "
                "(3) 어떤 철학적 개념의 의미를 검증하려면 그에 대응하는 인상을 찾아야 한다. "
                "(4) 인상으로 추적할 수 없는 개념은 내용 없는 언어적 소음에 불과하다. "
                "(5) 따라서 합리론자들의 '본유관념(innate ideas)'은 존재하지 않는다."
            ),
            "counterpoint": (
                "칸트는 '순수이성비판'(Kritik der reinen Vernunft, 1781)에서 흄의 인상-관념 이론이 "
                "경험의 가능 조건 자체를 설명하지 못한다고 비판했다. "
                "경험이 가능하려면 이미 시간·공간 같은 선험적 직관 형식과 인과율 같은 선험적 범주가 "
                "전제되어야 하므로, 모든 인식이 인상에서 시작한다는 흄의 주장은 "
                "경험 자체의 구성 조건을 설명하지 못한다는 것이다. "
                "또한 버클리(George Berkeley)는 '인간 지식의 원리론'(A Treatise Concerning the "
                "Principles of Human Knowledge, 1710)에서 물질 실체에 대한 관념의 불가능성을 "
                "흄과 유사하게 논증했지만, 신의 관념은 가능하다고 보아 흄의 무신론적 함의를 거부했다."
            ),
            "context": (
                "로크의 경험론은 관념의 기원을 감각과 반성으로 설명했지만, "
                "관념과 직접 경험 사이의 경계를 명확히 하지 않았다. "
                "흄은 인상과 관념의 엄밀한 구분으로 경험론을 급진화하고, "
                "합리론의 본유관념 및 형이상학적 실체 개념을 무력화하는 도구로 사용했다."
            ),
            "keywords": ["인상", "관념", "의미 기준", "경험론", "본유관념 비판"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-002: 인과관계 비판 — 필연적 연결 없음
        {
            "id": "hume-claim-002",
            "thinker_id": "hume",
            "work_id": "hume-treatise",
            "source_detail": "A Treatise of Human Nature, Book I, Part III, Section 6; Enquiry Concerning Human Understanding, Section 7",
            "claim": (
                "인과관계는 사건들 사이의 객관적·필연적 연결이 아니라, "
                "항상 선행(constant conjunction)에서 형성된 심리적 기대(custom/habit)이다. "
                "우리는 원인이 결과를 '만들어낸다'는 힘(power)을 결코 인상으로 경험할 수 없다."
            ),
            "original_text": (
                "We have no other notion of cause and effect, but that of certain objects, "
                "which have been always conjoin'd together, and which in all past instances "
                "have been found inseparable. We cannot penetrate into the reason of the conjunction."
            ),
            "explanation": (
                "흄은 인과 관계를 분석하여 세 가지 요소를 찾는다: "
                "①선행성(priority in time) — 원인은 결과보다 먼저 온다, "
                "②인접성(contiguity) — 원인과 결과는 시공간적으로 가깝다, "
                "③항상적 결합(constant conjunction) — A 다음에 B가 항상 따라왔다. "
                "그러나 세 번째 요소가 아무리 반복되어도 '필연적 연결(necessary connection)'을 "
                "지각(인상)으로 직접 경험할 수 없다. "
                "우리가 인과관계를 느끼는 것은 반복된 관찰로 형성된 심리적 습관(custom)이 "
                "마음에 전이(transition)되어 미래를 기대하게 만들기 때문이다."
            ),
            "argument": (
                "(1) 인과관계 개념이 의미를 가지려면 '인과적 힘'에 대응하는 인상이 있어야 한다. "
                "(2) 그러나 당구공 충돌 예처럼, 우리는 A 다음에 B가 따라오는 것만 볼 뿐, "
                "A가 B를 '만들어낸다'는 힘을 직접 인상으로 경험하지 못한다. "
                "(3) 물체 간 충돌에서도 자기 마음속 반성에서도 '힘'의 인상은 찾을 수 없다. "
                "(4) 따라서 인과적 필연성은 세계에 존재하는 객관적 사실이 아니라, "
                "반복 경험으로 마음이 형성한 '기대 습관(expectation/habit)'이다. "
                "(5) 이 습관이 미래에도 같은 패턴이 이어질 것이라는 믿음을 낳는다."
            ),
            "counterpoint": (
                "칸트는 '순수이성비판'(1781)에서 인과율은 흄처럼 귀납적으로 습득된 것이 아니라, "
                "경험을 가능하게 하는 선험적(a priori) 오성 범주(pure concept of the understanding)임을 "
                "논증했다. 인과율이 단순히 심리적 습관이라면 자연과학의 보편적·필연적 법칙은 "
                "성립할 수 없기 때문이다. "
                "또한 버트런드 러셀(Bertrand Russell)은 '철학의 문제들'(The Problems of Philosophy, 1912)에서 "
                "흄의 인과관계 비판이 과학적 추론의 토대를 위협한다는 점을 인정하면서도, "
                "인과관계가 없다는 결론보다 귀납의 원리를 공리(postulate)로 받아들이는 것이 "
                "더 합리적임을 제안했다."
            ),
            "context": (
                "합리론과 스콜라 철학은 인과관계를 필연적·형이상학적 연결로 보았다. "
                "흄의 인과관계 비판은 이 전제를 경험론적으로 해체하고, "
                "자연과학의 귀납적 방법론에 새로운 문제(귀납 문제)를 제기하는 출발점이 되었다."
            ),
            "keywords": ["인과관계", "필연적 연결", "항상적 결합", "습관", "경험론"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-003: 귀납 문제
        {
            "id": "hume-claim-003",
            "thinker_id": "hume",
            "work_id": "hume-enquiry-understanding",
            "source_detail": "An Enquiry Concerning Human Understanding, Section 4",
            "claim": (
                "과거의 경험은 미래에 같은 패턴이 반복될 것임을 논리적으로 보장하지 못한다. "
                "귀납 추론의 정당화는 순환 논리에 빠진다(귀납 문제)."
            ),
            "original_text": (
                "It is impossible, therefore, that any arguments from experience can prove "
                "this resemblance of the past to the future; since all these arguments are founded "
                "on the supposition of that resemblance."
            ),
            "explanation": (
                "흄은 귀납 추론을 두 가지 방식으로 정당화하려는 시도가 모두 실패함을 보인다. "
                "(1) 논리적(연역적) 정당화: '태양이 내일도 뜰 것이다'는 명제는 "
                "논리적으로 필연적이지 않다. 태양이 내일 뜨지 않는 것은 모순이 아니다. "
                "따라서 귀납은 연역으로 정당화될 수 없다. "
                "(2) 경험적 정당화: '과거에 귀납이 잘 맞았으니 미래에도 맞을 것이다'는 주장은 "
                "귀납으로 귀납을 정당화하는 순환 논리이다. "
                "결론: 귀납 추론의 합리적 정당화는 불가능하며, 우리가 귀납을 사용하는 것은 "
                "이성이 아닌 심리적 습관(custom) 때문이다."
            ),
            "argument": (
                "(1) 모든 사실적 추론(matters of fact)은 원인과 결과의 연결에 기반한다. "
                "(2) 원인-결과 연결에 대한 지식은 오직 경험에서만 나온다(관찰·귀납). "
                "(3) 경험은 과거의 관찰이고, 귀납은 '과거가 미래에도 반복될 것이다'는 가정에 의존한다. "
                "(4) 이 가정(자연의 제일성, uniformity of nature)은 논리적으로 증명할 수 없고, "
                "경험으로 증명하려 하면 순환 논리가 된다. "
                "(5) 따라서 귀납의 합리적 정당화는 불가능하다. "
                "우리는 이성이 아닌 심리적 습관(custom/habit)에 의해 귀납을 따른다."
            ),
            "counterpoint": (
                "칼 포퍼(Karl Popper)는 '과학적 발견의 논리'(The Logic of Scientific Discovery, 1934)에서 "
                "귀납 문제를 해결하는 대신 '반증 가능성(falsifiability)'을 과학의 기준으로 제시했다. "
                "과학은 귀납이 아닌 연역적 반증에 의해 진행되므로 귀납 정당화가 필요 없다는 것이다. "
                "반면 한스 라이헨바흐(Hans Reichenbach)는 '귀납의 이론'(The Theory of Probability, 1949)에서 "
                "귀납이 반드시 성공하지는 않아도 성공할 수 있다면 귀납이 최선의 베팅임을 "
                "실용적 정당화(pragmatic justification)로 논증했다."
            ),
            "context": (
                "인과관계 비판의 자연스러운 귀결로서 제시되었다. "
                "인과관계가 심리적 습관에 불과하다면, "
                "과거 경험으로부터 미래를 예측하는 귀납의 합리적 근거도 없어진다. "
                "이는 뉴턴 과학의 귀납적 방법론에 대한 철학적 도전으로 이해되었다."
            ),
            "keywords": ["귀납 문제", "귀납 추론", "자연의 제일성", "순환 논리", "습관"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-004: 도덕 감정주의 — 이성은 도덕의 기초가 될 수 없다
        {
            "id": "hume-claim-004",
            "thinker_id": "hume",
            "work_id": "hume-treatise",
            "source_detail": "A Treatise of Human Nature, Book III, Part I, Section 1; Enquiry Concerning the Principles of Morals, Appendix 1",
            "claim": (
                "이성(reason)만으로는 도덕적 판단을 내릴 수 없다. "
                "도덕은 이성이 아닌 감정(sentiment/passion)에 기초하며, "
                "이성은 도덕적 행위를 유발할 수 없다."
            ),
            "original_text": (
                "Reason is, and ought only to be the slave of the passions, "
                "and can never pretend to any other office than to serve and obey them."
            ),
            "explanation": (
                "흄의 도덕 감정주의는 두 가지 핵심 논증으로 구성된다. "
                "(1) 이성의 행위 동기화 불가능성: 이성은 참·거짓을 판단하는 능력이다. "
                "그러나 도덕 판단은 행위를 동기화해야 한다. "
                "이성만으로는 욕구나 감정을 일으킬 수 없으므로 행위를 동기화할 수 없다. "
                "도덕적 행위를 일으키는 것은 항상 감정(passion)이다. "
                "(2) 도덕적 선악은 인상(감정)으로 경험된다: "
                "덕(virtue)을 볼 때 우리는 승인(approbation)의 감정을, "
                "악(vice)을 볼 때 불승인(disapprobation)의 감정을 느낀다. "
                "이 감정 자체가 도덕 판단이다."
            ),
            "argument": (
                "(1) 이성은 관념들의 관계(demonstration) 또는 사실 문제(matters of fact)를 다룬다. "
                "(2) 도덕적 판단은 행위를 유발해야 하는데, 이성의 판단은 그 자체로 욕구를 낳지 못한다. "
                "(3) 행위를 유발하는 것은 항상 욕구·감정·감성(passions)이며, 이성은 이를 보조할 뿐이다. "
                "(예: '이것이 도둑질이다'는 이성적 판단이지만, 도둑질을 하지 않게 하는 것은 "
                "공정성에 대한 감정적 반응이다.) "
                "(4) 도덕적 선악은 이성으로 파악되는 사실이나 관계가 아니라, "
                "공감(sympathy)을 통해 느끼는 승인·불승인의 감정이다. "
                "(5) 따라서 '이성은 감정의 노예'이고, 도덕의 기초는 이성이 아닌 감정이다."
            ),
            "counterpoint": (
                "칸트는 '도덕형이상학 기초'(Groundwork for the Metaphysics of Morals, 1785)에서 "
                "흄의 도덕 감정주의는 보편성·필연성을 확보할 수 없다고 비판했다. "
                "감정은 사람마다, 문화마다 다르므로 감정에 기반한 도덕은 상대주의에 빠진다는 것이다. "
                "칸트는 도덕 법칙이 순수 이성에서만 도출될 수 있으며, "
                "정언명령(categorical imperative)이 보편적 도덕 원리의 근거임을 주장했다. "
                "또한 헤어(R.M. Hare)는 '도덕의 언어'(The Language of Morals, 1952)에서 "
                "흄식의 도덕 감정주의는 도덕 판단을 단순한 감정 표현으로 환원하여 "
                "도덕적 논증과 합리적 설득의 가능성을 훼손한다고 비판했다."
            ),
            "context": (
                "17~18세기 합리론적 도덕론(쿠드워스, 클라크, 울러스턴 등)은 "
                "도덕적 선악이 이성으로 파악되는 객관적 관계라고 보았다. "
                "샤프츠버리와 허치슨은 감정(도덕 감각)을 도덕의 기초로 보았는데, "
                "흄은 이 전통을 계승하면서 이성의 도덕적 역할을 보다 철저히 제한했다."
            ),
            "keywords": ["도덕 감정주의", "이성의 한계", "감정", "공감", "승인·불승인"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-005: 사실-당위 논리 간극 (흄의 단두대)
        {
            "id": "hume-claim-005",
            "thinker_id": "hume",
            "work_id": "hume-treatise",
            "source_detail": "A Treatise of Human Nature, Book III, Part I, Section 1",
            "claim": (
                "'이다(is)' 명제에서 '해야 한다(ought)' 명제를 논리적으로 도출할 수 없다. "
                "사실 진술로부터 규범 진술을 끌어내는 것은 논리적 비약이다(사실-당위 논리 간극)."
            ),
            "original_text": (
                "In every system of morality, which I have hitherto met with, I have always remark'd, "
                "that the author proceeds for some time in the ordinary way of reasoning, and establishes "
                "the being of a God, or makes observations concerning human affairs; when of a sudden I "
                "am surpriz'd to find, that instead of the usual copulations of propositions, is, and is not, "
                "I meet with no proposition that is not connected with an ought, or an ought not."
            ),
            "explanation": (
                "흄은 모든 도덕 이론이 사실 명제들을 나열하다가 갑자기 '해야 한다'는 규범 명제로 "
                "전환한다는 점을 발견하고, 이 전환에 대한 정당화가 제시되지 않는다고 지적했다. "
                "'신이 존재한다' → '신이 인간을 사랑한다' → '인간은 이웃을 사랑해야 한다'처럼, "
                "순수한 사실 명제들로부터 당위 명제를 도출하는 것은 새로운 서술 방식을 도입하는 것이다. "
                "이 간극을 '자연주의적 오류(naturalistic fallacy)'라 부르기도 한다(무어의 명명). "
                "현대 메타윤리학의 사실-가치 이분법의 출발점이 된 관찰이다."
            ),
            "argument": (
                "(1) 논리적으로 타당한 추론에서 결론에 포함되는 내용은 전제에 이미 있어야 한다. "
                "(2) '이다' 명제들은 현상에 대한 기술이고, '해야 한다' 명제는 행위에 대한 처방이다. "
                "(3) 두 종류의 명제는 서로 다른 논리적 지위를 가지므로, "
                "전자만으로 후자를 논리적으로 도출할 수 없다. "
                "(4) 따라서 기존 도덕 이론들이 사실에서 당위를 도출하려 할 때 "
                "반드시 숨겨진 가치 전제가 있거나 논리적 비약이 있다."
            ),
            "counterpoint": (
                "G.E. 무어(G.E. Moore)는 '윤리학 원리'(Principia Ethica, 1903)에서 "
                "자연적 속성에서 선(good)을 도출하려는 시도를 '자연주의적 오류(naturalistic fallacy)'라 명명하고 "
                "흄의 논점을 확장했다. "
                "반면 존 서얼(John Searle)은 '말과 행동'(Speech Acts, 1969)에서 "
                "제도적 사실(institutional facts, 예: 약속)은 사실이면서 동시에 당위를 함의한다는 "
                "'약속 사례'를 제시하여 흄의 간극이 절대적이지 않음을 논증하려 했다. "
                "또한 퍼트남(Hilary Putnam)은 '사실과 가치의 붕괴'(The Collapse of the "
                "Fact/Value Dichotomy, 2002)에서 사실과 가치는 언어적으로 뒤얽혀 있어 "
                "흄식의 이분법이 성립하지 않는다고 비판했다."
            ),
            "context": (
                "도덕 이론을 신학적·자연주의적 근거에서 도출하려는 당시 도덕 이론가들의 경향에 대한 "
                "비판으로 제시되었다. 이 짧은 각주 성격의 논평이 20세기 메타윤리학의 핵심 문제를 "
                "선취한 것으로 평가받는다."
            ),
            "keywords": ["사실-당위 논리 간극", "흄의 단두대", "자연주의적 오류", "메타윤리학", "규범 추론"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-006: 자아 번들 이론
        {
            "id": "hume-claim-006",
            "thinker_id": "hume",
            "work_id": "hume-treatise",
            "source_detail": "A Treatise of Human Nature, Book I, Part IV, Section 6",
            "claim": (
                "자아(self)는 인상들과 관념들의 묶음(bundle)일 뿐이며, "
                "지속적·동일한 자아 실체는 경험으로 확인할 수 없다."
            ),
            "original_text": (
                "For my part, when I enter most intimately into what I call myself, "
                "I always stumble on some particular perception or other, of heat or cold, "
                "light or shade, love or hatred, pain or pleasure. I never can catch myself "
                "at any time without a perception, and can never observe any thing but the perception."
            ),
            "explanation": (
                "흄은 자아를 인상들의 '번들(bundle)'로 규정한다. "
                "우리가 내면을 들여다볼 때 발견하는 것은 항상 특정한 지각들(감각, 감정, 기억 등)이지, "
                "이 지각들을 통일하는 지속적 자아 실체는 발견되지 않는다. "
                "자아의 동일성(personal identity)은 기억과 상상이 지각들을 연결하여 만들어낸 "
                "허구(fiction)이다. "
                "이는 데카르트의 '나는 생각한다, 고로 나는 존재한다'에서 전제되는 지속적 자아 실체를 해체한다."
            ),
            "argument": (
                "(1) 인상·관념의 의미 기준에 따르면, '자아(self)'에 대응하는 단순 인상이 있어야 한다. "
                "(2) 그러나 내면 성찰에서 발견되는 것은 항상 구체적인 개별 지각들이지, "
                "'자아 자체'라는 별도의 인상은 없다. "
                "(3) 따라서 데카르트가 가정한 것처럼 사유의 주체로서 지속하는 자아 실체는 "
                "경험적으로 확인할 수 없다. "
                "(4) '나는 어제도 오늘도 나다'라는 동일성 감각은, "
                "기억이 서로 다른 시점의 지각들 사이에 유사성과 인과관계를 연결해 만들어낸 허구다. "
                "(5) 자아는 '지각들의 묶음(bundle of perceptions)'이다."
            ),
            "counterpoint": (
                "칸트는 '순수이성비판'(1781)에서 흄처럼 자아를 지각들의 총합으로만 보면 "
                "경험의 통일성이 불가능해진다고 비판했다. "
                "경험이 가능하려면 모든 지각들을 하나로 묶는 '통각의 통일(unity of apperception)'이 "
                "선험적으로 전제되어야 한다는 것이다. "
                "또한 데릭 파핏(Derek Parfit)은 '이성과 인격'(Reasons and Persons, 1984)에서 "
                "흄의 번들 이론을 받아들이면서도, 이것이 실천 윤리에서 "
                "이기주의를 약화시키고 중립적 관심(impersonal concern)을 강화한다는 함의를 이끌어냈다."
            ),
            "context": (
                "합리론은 데카르트의 '코기토(cogito)'처럼 지속적·동일한 자아 실체를 전제했고, "
                "로크도 의식의 연속성으로 인격 동일성을 설명했다. "
                "흄은 이 두 전통에서 가정한 실체적 자아를 경험론적으로 해체했다."
            ),
            "keywords": ["번들 이론", "자아", "인격 동일성", "지각의 묶음", "자아 허구"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-007: 자연적 덕과 인위적 덕
        {
            "id": "hume-claim-007",
            "thinker_id": "hume",
            "work_id": "hume-treatise",
            "source_detail": "A Treatise of Human Nature, Book III, Part II, Section 1; Part III, Section 1",
            "claim": (
                "덕(virtue)은 자연적 덕(natural virtues)과 인위적 덕(artificial virtues)으로 나뉜다. "
                "자연적 덕(자비, 용기 등)은 공감을 통해 즉각 승인되며, "
                "인위적 덕(정의, 약속 준수 등)은 사회적 약속과 공익 계산에서 나온다."
            ),
            "original_text": (
                "I have already observ'd, that justice takes its rise from human conventions; "
                "and that these are intended as a remedy to some inconveniences, "
                "which proceed from the concurrence of certain qualities of the human mind "
                "with the situation of external objects."
            ),
            "explanation": (
                "자연적 덕은 인위적 약속이 없어도 인간 본성의 공감(sympathy) 능력 때문에 "
                "즉각 승인·실천되는 덕이다. 예: 자비(benevolence), 용기, 겸손 등. "
                "인위적 덕은 그 자체로 자연스럽게 승인되지는 않으나, "
                "사회적 필요와 약속·제도적 맥락 안에서 형성되어 전체 체계로서 유용성을 인정받는 덕이다. "
                "예: 정의(justice), 약속 준수(fidelity), 정절 등. "
                "정의가 인위적인 이유는, 재산이 없는 자연 상태에서 '정의'는 의미가 없기 때문이다. "
                "재산 제도·약속 제도가 성립한 이후에야 '남의 것을 돌려주어야 한다'는 정의 개념이 생긴다."
            ),
            "argument": (
                "(1) 인간 본성에는 공감(sympathy) 능력이 있어, 타인의 고통이나 기쁨을 느낄 수 있다. "
                "(2) 자연적 덕(자비 등)은 이 공감 능력이 직접 발동하여 승인되는 덕이다. "
                "(3) 정의와 약속 준수는 개별 행위만으로는 항상 최선이 아닐 수 있으나, "
                "전체 규칙 체계가 사회 유지에 유용하기 때문에 승인된다. "
                "(4) 정의는 자연적 상태에서 발생하지 않고, 소유 제도가 생긴 인위적 사회에서 "
                "사회적 약속으로 등장한 것이다. "
                "(5) 따라서 정의는 인위적 덕이지만, 사회 유지에 필수불가결하므로 진정한 덕이다."
            ),
            "counterpoint": (
                "애덤 스미스(Adam Smith)는 '도덕감정론'(The Theory of Moral Sentiments, 1759)에서 "
                "흄의 공감(sympathy) 개념을 수용하면서도, 공감이 타인의 감정을 그대로 느끼는 것이 아니라 "
                "관찰자가 상상으로 재구성하는 것임을 강조하여 흄의 논의를 발전시켰다. "
                "또한 존 롤스(John Rawls)는 '정의론'(A Theory of Justice, 1971)에서 "
                "흄의 정의론이 기존 사회 약속에서 정의를 도출하여 기존 불평등을 정당화할 위험이 있다고 비판하고, "
                "공정으로서의 정의(justice as fairness)를 대안으로 제시했다."
            ),
            "context": (
                "자연법론(그로티우스, 푸펜도르프 등)은 정의를 자연적이고 보편적인 규범으로 보았다. "
                "흄은 정의가 인위적 사회 제도에서 파생됨을 주장하여 "
                "자연법론적 정의론을 경험론적으로 해체했다."
            ),
            "keywords": ["자연적 덕", "인위적 덕", "정의", "공감", "사회적 약속"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-008: 기적 비판
        {
            "id": "hume-claim-008",
            "thinker_id": "hume",
            "work_id": "hume-enquiry-understanding",
            "source_detail": "An Enquiry Concerning Human Understanding, Section 10",
            "claim": (
                "기적(miracle)은 자연 법칙의 위반인데, 기적의 증언에 대한 증거는 "
                "자연 법칙의 불변성에 대한 경험적 증거보다 항상 약하다. "
                "따라서 기적을 믿는 것은 합리적이지 않다."
            ),
            "original_text": (
                "A miracle is a violation of the laws of nature; and as a firm and unalterable "
                "experience has established these laws, the proof against a miracle, from the very "
                "nature of the fact, is as entire as any argument from experience can possibly be imagined."
            ),
            "explanation": (
                "흄은 기적 주장을 평가하는 방법으로 '증거의 증거에 대한 저울질'을 제시한다. "
                "기적이 일어났다는 증거(증인의 증언)와 기적이 일어나지 않는다는 증거(자연 법칙의 일관성)를 "
                "비교하면, 자연 법칙에 대한 인류의 보편적·반복적 경험이 항상 기적 증언보다 무겁다. "
                "따라서 이성적 인간은 기적 주장을 거부해야 한다. "
                "이 논증은 기적에 기반한 종교적 주장 전반에 대한 비판으로 확장된다."
            ),
            "argument": (
                "(1) 모든 경험적 판단은 증거의 무게에 비례해야 한다. "
                "(2) 자연 법칙은 수백만 번의 관찰로 확립된 것으로, 그에 반하는 증거는 극히 강해야 한다. "
                "(3) 기적 주장은 소수의 증인 증언에 의존하는데, "
                "증인은 착각·기만·자기기만에 취약하다. "
                "(4) 기적 증언의 강도(소수 증인)는 자연 법칙의 불변성에 대한 증거(보편 경험)보다 항상 약하다. "
                "(5) 따라서 이성적 인간은 기적 주장을 기각하고 "
                "증언의 오류 가능성을 받아들이는 것이 더 합리적이다."
            ),
            "counterpoint": (
                "C.S. 루이스(C.S. Lewis)는 '기적'(Miracles, 1947)에서 흄의 논증이 "
                "자연 법칙이 절대적이라는 것을 전제하는 순환 논리라고 비판했다. "
                "자연주의(naturalism)가 참이라고 미리 가정하면 기적은 불가능하지만, "
                "신이 존재하고 자연에 개입할 수 있다면 자연 법칙은 통상적 패턴일 뿐이라는 것이다. "
                "또한 존 얼만(John Earman)은 '흄의 기적적 실패'(Hume's Abject Failure, 2000)에서 "
                "베이즈 통계 분석을 이용하여 충분히 독립적인 증인들의 증언은 "
                "기적의 사전 확률이 낮더라도 사후 확률을 높일 수 있음을 수학적으로 논증하며 "
                "흄의 논증이 지나치게 단순하다고 비판했다."
            ),
            "context": (
                "17~18세기에 기적은 종교의 진리성을 입증하는 근거로 널리 인용되었다. "
                "흄은 종교의 기적 주장을 경험론적 증거 이론으로 비판하여, "
                "자연종교(natural religion)에 대한 회의주의적 관점을 체계화했다."
            ),
            "keywords": ["기적 비판", "자연 법칙", "증거의 무게", "종교 회의주의", "증언"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-009: 관계 of ideas vs matters of fact (흄의 포크)
        {
            "id": "hume-claim-009",
            "thinker_id": "hume",
            "work_id": "hume-enquiry-understanding",
            "source_detail": "An Enquiry Concerning Human Understanding, Section 4, Part 1",
            "claim": (
                "모든 인간의 인식은 '관념들의 관계(relations of ideas)'와 '사실 문제(matters of fact)' "
                "두 종류로 나뉜다. 이 두 가지 외의 것(형이상학)은 모두 불태워야 한다('흄의 포크')."
            ),
            "original_text": (
                "All the objects of human reason or enquiry may naturally be divided into two kinds, "
                "to wit, Relations of Ideas, and Matters of Fact. Of the first kind are the sciences "
                "of Geometry, Algebra, and Arithmetic... Matters of fact, which are the second objects "
                "of human reason, are not ascertained in the same manner."
            ),
            "explanation": (
                "'관념들의 관계'는 논리학·수학처럼 관념들 간의 논리적 관계에 의해 참·거짓이 결정되는 명제로, "
                "부정하면 모순이 생긴다(분석적 판단). 경험 없이 선험적으로 알 수 있다. "
                "'사실 문제'는 경험과 관찰에 의해서만 확인되는 명제로, "
                "부정해도 모순이 생기지 않는다(종합적 판단). "
                "흄은 이 이분법을 적용하면 기존 형이상학적 주장들이 "
                "어느 범주에도 속하지 않는 무의미한 소리임을 보여준다. "
                "'신이 존재한다'는 명제는 분석적이지도 경험으로 검증 가능하지도 않으므로, "
                "흄에 따르면 불태워야 할 헛소리이다."
            ),
            "argument": (
                "(1) 진정한 인식은 관념들의 관계(논리·수학) 또는 사실 문제(경험 과학) 두 종류뿐이다. "
                "(2) 형이상학, 신학, 자연법론의 많은 주장들은 분석적 진리도 아니고 경험으로 검증 가능하지도 않다. "
                "(3) 따라서 이러한 주장들은 인식적 내용이 없는 '궤변과 허상(sophistry and illusion)'이다. "
                "(4) 도서관에 있는 책 중 위 두 종류에 해당하지 않는 것은 '불에 태워야 한다'."
            ),
            "counterpoint": (
                "칸트는 '순수이성비판'(1781) 서문에서 흄의 이분법을 정면으로 문제 삼았다. "
                "흄은 '분석적 a priori'와 '종합적 a posteriori'만을 인정했지만, "
                "칸트는 '종합적 a priori'(수학·자연과학의 선험적 종합 판단)가 가능함을 논증하여 "
                "흄의 이분법이 불완전함을 주장했다. "
                "또한 논리실증주의자(비엔나 학파)들은 흄의 이분법을 계승하여 "
                "'검증 가능성 원리(verificationism)'를 제시했지만, "
                "포퍼와 콰인(W.V.O. Quine)에 의해 이 원리 자체도 검증 불가능하다는 비판을 받았다."
            ),
            "context": (
                "'흄의 포크(Hume's Fork)'라 불리는 이 이분법은 '인간 이해력 탐구' 마지막 단락에서 "
                "극적인 방식으로 제시된다. "
                "형이상학과 신학에 대한 경험론적 비판의 정점으로, "
                "20세기 논리실증주의에 직접적 영향을 주었다."
            ),
            "keywords": ["흄의 포크", "관념들의 관계", "사실 문제", "분석-종합 구분", "형이상학 비판"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-010: 공감(sympathy)과 도덕 평가
        {
            "id": "hume-claim-010",
            "thinker_id": "hume",
            "work_id": "hume-enquiry-morals",
            "source_detail": "An Enquiry Concerning the Principles of Morals, Section 5; Treatise Book III, Part III, Section 1",
            "claim": (
                "공감(sympathy)은 도덕 평가의 핵심 메커니즘으로, "
                "우리가 타인의 쾌고(苦楽)에 공명하는 능력이 덕과 악덕을 식별하는 기초이다. "
                "공감은 또한 사회 통합과 도덕적 연대의 토대이다."
            ),
            "original_text": (
                "It is sufficient, that there is some particle of the dove, kneaded into our frame, "
                "along with the elements of the wolf and the serpent. Let these generous sentiments "
                "be ever so weak; let them be insufficient to move even a hand or finger of our body, "
                "they must still direct the determinations of our mind."
            ),
            "explanation": (
                "흄의 공감(sympathy) 개념은 단순한 동정심이 아니라, "
                "타인의 감정과 처지를 자신의 것처럼 느끼는 심리적 메커니즘이다. "
                "우리는 타인의 행복을 보면 승인의 쾌감을, 타인의 고통을 보면 불승인의 불쾌감을 느낀다. "
                "이 공감 반응이 덕(유용하거나 즐거운 성품)과 악덕(해롭거나 불쾌한 성품)을 구분하는 기준이다. "
                "공감 능력이 없다면 도덕 판단 자체가 불가능하다는 것이 흄의 주장이다."
            ),
            "argument": (
                "(1) 인간에게는 타인의 정서 상태를 자신에게 전이(transmit)하는 공감 능력이 있다. "
                "(2) 덕스러운 성품(용감함, 관대함 등)은 당사자와 주변인에게 유용하거나 즐거운 것이므로, "
                "공감을 통해 우리는 이를 승인하게 된다. "
                "(3) 악덕스러운 성품은 해롭거나 불쾌한 것이므로, 공감을 통해 불승인하게 된다. "
                "(4) 이 공감 기반 승인·불승인이 도덕 판단의 실질적 내용이다. "
                "(5) 공감 범위는 가까운 사람에서 점차 넓혀지며, 사회 전체로의 확장이 '일반적 관점'을 낳는다."
            ),
            "counterpoint": (
                "애덤 스미스(Adam Smith)는 '도덕감정론'(The Theory of Moral Sentiments, 1759)에서 "
                "흄의 공감 개념이 타인의 감정을 직접 '전염'처럼 받아들이는 것으로 오해될 수 있다고 보고, "
                "공감이란 상상력을 통해 관찰자가 행위자의 처지에 자신을 놓아보는 '공감적 상상'임을 강조했다. "
                "또한 블레이크(Michael Slote)는 '감정주의의 도덕'(Morals from Motives, 2001)에서 "
                "흄의 공감론이 공감의 불균등 분포(가까운 사람에게 더 강한 공감)를 해결하지 못해 "
                "도덕의 공평성 요구를 충족하기 어렵다고 비판했다."
            ),
            "context": (
                "이성주의 도덕론이 도덕 감정을 보조적 역할로만 보았던 것에 비해, "
                "흄은 공감을 도덕 판단의 핵심 메커니즘으로 격상시켰다. "
                "이는 허치슨의 '도덕 감각(moral sense)' 이론을 계승하면서도, "
                "타고난 능력이 아닌 공감의 심리적 메커니즘으로 재구성한 것이다."
            ),
            "keywords": ["공감", "도덕 감정주의", "승인·불승인", "덕과 악덕", "사회 통합"],
            "verified": False,
            "verification_log": []
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """흄 핵심 키워드 데이터 입력."""
    keywords = [
        {
            "id": "kw-hume-impressions-ideas",
            "term": "인상과 관념",
            "term_en": "Impressions and Ideas",
            "definition": (
                "흄 인식론의 기초 구분. 인상(impressions)은 감각·감정·욕구 등 직접적이고 생생한 지각이며, "
                "관념(ideas)은 인상이 사라진 후 기억·상상에 남는 희미한 복사본이다. "
                "모든 관념은 선행하는 인상에서 파생되어야 하며, 이는 형이상학적 개념 비판의 도구이다. "
                "출처: Treatise Book I, Part I, Section 1; Enquiry Section 2."
            ),
            "thinker_id": "hume",
            "work_id": "hume-treatise",
            "related_terms": ["경험론", "의미 기준", "인과관계 비판", "자아 번들 이론"]
        },
        {
            "id": "kw-hume-causation",
            "term": "인과관계 비판",
            "term_en": "Critique of Causation / Necessary Connection",
            "definition": (
                "흄은 인과관계에서 '필연적 연결(necessary connection)'이 인상으로 확인되지 않음을 논증했다. "
                "우리가 인과관계라고 믿는 것은 항상적 결합(constant conjunction)의 반복이 "
                "심리적 습관(custom/habit)을 낳아 미래 기대를 형성한 것이다. "
                "A 다음 B가 항상 따라온다고 해서 A가 B를 '만들어낸다'는 힘이 있는 것은 아니다. "
                "출처: Treatise Book I, Part III, Section 6; Enquiry Section 7."
            ),
            "thinker_id": "hume",
            "work_id": "hume-treatise",
            "related_terms": ["귀납 문제", "항상적 결합", "습관", "경험론"]
        },
        {
            "id": "kw-hume-induction-problem",
            "term": "귀납 문제",
            "term_en": "Problem of Induction",
            "definition": (
                "흄이 제기한 귀납 추론의 정당화 불가능성 문제. "
                "과거 경험이 미래에도 반복될 것이라는 가정(자연의 제일성, uniformity of nature)은 "
                "연역적으로 증명할 수 없고, 경험적으로 정당화하면 순환 논리에 빠진다. "
                "과학적 귀납 추론의 합리적 토대에 대한 근본적 의문 제기. "
                "출처: Enquiry Section 4."
            ),
            "thinker_id": "hume",
            "work_id": "hume-enquiry-understanding",
            "related_terms": ["인과관계 비판", "자연의 제일성", "경험론", "반증주의"]
        },
        {
            "id": "kw-hume-moral-sentimentalism",
            "term": "도덕 감정주의",
            "term_en": "Moral Sentimentalism",
            "definition": (
                "이성이 아닌 감정(sentiment/passion)이 도덕 판단과 행위 동기의 원천이라는 흄의 도덕론. "
                "'이성은 감정의 노예'라는 명제로 대표된다. "
                "도덕적 선악은 이성으로 파악되는 관계가 아니라, "
                "공감을 통해 느끼는 승인·불승인의 감정이다. "
                "출처: Treatise Book III, Part I, Section 1; Enquiry Appendix 1."
            ),
            "thinker_id": "hume",
            "work_id": "hume-treatise",
            "related_terms": ["공감", "사실-당위 논리 간극", "이성의 한계", "허치슨"]
        },
        {
            "id": "kw-hume-is-ought",
            "term": "사실-당위 논리 간극",
            "term_en": "Is-Ought Gap / Hume's Guillotine",
            "definition": (
                "사실 명제('이다/이지 않다')에서 규범 명제('해야 한다/하지 않아야 한다')를 "
                "논리적으로 도출할 수 없다는 흄의 메타윤리학적 관찰. "
                "'흄의 단두대(Hume's Guillotine)' 또는 '사실-가치 이분법'으로도 불린다. "
                "현대 메타윤리학의 출발점으로, 자연주의적 오류(naturalistic fallacy) 논의의 선구. "
                "출처: Treatise Book III, Part I, Section 1."
            ),
            "thinker_id": "hume",
            "work_id": "hume-treatise",
            "related_terms": ["도덕 감정주의", "자연주의적 오류", "메타윤리학", "사실-가치 이분법"]
        },
        {
            "id": "kw-hume-bundle-theory",
            "term": "자아 번들 이론",
            "term_en": "Bundle Theory of Self",
            "definition": (
                "자아(self)는 지각들(perceptions)의 묶음(bundle)이며, "
                "이 지각들의 배후에 있는 지속적·동일한 자아 실체는 경험으로 확인할 수 없다는 흄의 주장. "
                "내면 성찰에서 발견되는 것은 항상 특정한 지각들이지 자아 자체가 아니다. "
                "인격 동일성(personal identity)은 기억이 지각들을 연결하여 만들어낸 허구이다. "
                "출처: Treatise Book I, Part IV, Section 6."
            ),
            "thinker_id": "hume",
            "work_id": "hume-treatise",
            "related_terms": ["인상과 관념", "인격 동일성", "자아 실체 부정", "데카르트 비판"]
        },
        {
            "id": "kw-hume-sympathy",
            "term": "공감",
            "term_en": "Sympathy",
            "definition": (
                "흄 도덕론의 핵심 심리적 메커니즘. 타인의 감정과 처지에 공명(共鳴)하여 "
                "자신도 유사한 감정을 느끼는 능력. "
                "덕(유용하거나 즐거운 성품)은 공감을 통해 승인되고, "
                "악덕(해롭거나 불쾌한 성품)은 불승인된다. "
                "단순 동정심과 달리, 흄의 공감은 관찰자가 행위자의 처지로 전이하는 심리적 과정이다. "
                "출처: Treatise Book III, Part III; Enquiry Section 5."
            ),
            "thinker_id": "hume",
            "work_id": "hume-enquiry-morals",
            "related_terms": ["도덕 감정주의", "승인·불승인", "자연적 덕", "아담 스미스"]
        },
        {
            "id": "kw-hume-artificial-virtues",
            "term": "인위적 덕",
            "term_en": "Artificial Virtues",
            "definition": (
                "흄이 구분한 덕의 한 종류. 자연적 공감만으로는 즉각 승인되지 않지만, "
                "사회적 약속·제도 안에서 전체 체계의 유용성이 인정되어 승인되는 덕. "
                "정의(justice), 약속 준수(fidelity), 정절 등이 대표 사례. "
                "정의는 소유 제도가 생긴 인위적 사회에서 등장한 것으로, "
                "자연적 덕(benevolence 등)과 달리 사회적 맥락이 필요하다. "
                "출처: Treatise Book III, Part II, Section 1."
            ),
            "thinker_id": "hume",
            "work_id": "hume-treatise",
            "related_terms": ["자연적 덕", "정의", "사회 계약", "공감"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """흄 관련 사상 관계 데이터 입력."""
    relations = [
        # 흄 → 칸트: 가장 중요한 관계 — 독단적 잠에서 깨어나게 함
        {
            "id": "relation-hume-kant",
            "from_thinker": "hume",
            "to_thinker": "kant",
            "type": "influenced",
            "description": (
                "칸트는 '프롤레고메나'(Prolegomena, 1783)에서 흄이 자신을 '독단적 잠에서 깨어나게 했다'고 고백했다. "
                "흄의 인과관계 비판은 칸트로 하여금 순수 이성의 가능 조건을 비판적으로 검토하게 하여, "
                "'순수이성비판'(1781)의 선험적 분석론을 낳았다. "
                "칸트는 인과율을 흄처럼 귀납적 습관이 아닌 선험적 오성 범주로 격상시켜 흄의 회의주의에 답했다. "
                "이 영향 관계는 서양 근대 철학 전체에서 가장 중요한 지적 전환 중 하나로 평가된다."
            ),
            "evidence": (
                "Kant, Prolegomena to Any Future Metaphysics (1783), Preface: "
                "'It was the recollection of David Hume which, many years ago, first interrupted my dogmatic slumber.'"
            )
        },
        # 흄 → 벤담: 공리주의에 대한 영향
        {
            "id": "relation-hume-bentham",
            "from_thinker": "hume",
            "to_thinker": "bentham",
            "type": "influenced",
            "description": (
                "벤담은 흄의 '도덕 원리 탐구'(Enquiry Concerning the Principles of Morals, 1751)를 읽고 "
                "'공리(utility)'라는 핵심 개념의 단서를 발견했다고 회고했다. "
                "흄의 경험론적 방법론, 자연적 덕의 '유용성' 강조, 감정 기반 도덕론은 "
                "벤담이 공리주의 윤리학을 체계화하는 데 중요한 영감을 주었다. "
                "그러나 흄이 감정과 공감을 도덕의 기초로 본 반면, 벤담은 공리 계산이라는 "
                "이성적 절차를 전면에 내세웠다는 점에서 차이가 있다."
            ),
            "evidence": (
                "Bentham, An Introduction to the Principles of Morals and Legislation (1789), "
                "footnote to Chapter 1; Hume, Enquiry Concerning the Principles of Morals (1751), Section 5"
            )
        },
        # 흄 → 아담 스미스: 우정과 상호 영향
        {
            "id": "relation-hume-smith",
            "from_thinker": "hume",
            "to_thinker": "smith",
            "type": "influenced",
            "description": (
                "흄과 아담 스미스는 에든버러를 중심으로 한 스코틀랜드 계몽주의의 대표 지식인으로, "
                "깊은 우정과 지적 교류를 나눴다. "
                "흄의 공감(sympathy) 개념과 인위적 덕(정의) 이론은 "
                "스미스의 '도덕감정론'(The Theory of Moral Sentiments, 1759)에서 "
                "공감의 심리적 메커니즘으로 발전·정교화되었다. "
                "흄의 경험론적 방법론과 정치경제학 소론(Essays)은 '국부론'(Wealth of Nations, 1776)에도 영향을 주었다."
            ),
            "evidence": (
                "Smith, A., The Theory of Moral Sentiments (1759), Part I, Section 1; "
                "Hume–Smith 서신 교환 (Letters of David Hume)"
            )
        },
        # 아리스토텔레스 → 흄: 덕 윤리와 감정론 영향
        {
            "id": "relation-aristotle-hume",
            "from_thinker": "aristotle",
            "to_thinker": "hume",
            "type": "influenced_by",
            "description": (
                "흄의 덕 윤리(자연적 덕·인위적 덕 구분)와 감정(passion)의 역할 강조는 "
                "아리스토텔레스의 덕 윤리학 전통과 연결된다. "
                "아리스토텔레스가 감정(pathos)을 도덕 교육과 덕의 형성에서 핵심 요소로 보았듯, "
                "흄도 감정이 도덕 판단과 행위 동기의 원천임을 주장했다. "
                "그러나 흄은 아리스토텔레스의 목적론적 자연관과 형이상학을 거부하고, "
                "경험론적 심리학으로 대체했다는 점에서 결정적으로 다르다."
            ),
            "evidence": (
                "Hume, A Treatise of Human Nature (1739), Book III, Part I; "
                "Aristotle, Nicomachean Ethics, Books II~IV (덕과 감정론)"
            )
        },
        # 흄 → 현대 메타윤리학: 사실-당위 간극의 영향
        {
            "id": "relation-hume-moore",
            "from_thinker": "hume",
            "to_thinker": "moore",
            "type": "influenced",
            "description": (
                "흄의 사실-당위 논리 간극(is-ought gap)은 G.E. 무어의 '자연주의적 오류(naturalistic fallacy)' "
                "논의에 직접적 영향을 주었다. "
                "무어는 '윤리학 원리'(Principia Ethica, 1903)에서 자연적 속성에서 선(good)을 "
                "도출하려는 모든 시도가 오류임을 논증했으며, 이는 흄의 통찰을 메타윤리학적으로 발전시킨 것이다. "
                "흄-무어 라인은 20세기 분석철학 메타윤리학 논의의 출발점이 되었다."
            ),
            "evidence": (
                "Moore, G.E., Principia Ethica (1903), Chapter 1; "
                "Hume, Treatise Book III, Part I, Section 1 (is-ought passage)"
            )
        }
    ]

    for rel in relations:
        result = client.index(index=INDEX_RELATIONS, id=rel["id"], document=rel)
        print(f"[relation] {rel['id']}: {result['result']}")

    return len(relations)


def main():
    """메인 실행 함수."""
    print("=== 흄(David Hume) 데이터 ES 입력 시작 ===\n")

    client = get_client()

    try:
        # 1. 사상가
        print("--- 사상가 입력 ---")
        insert_thinker(client)

        # 2. 저서
        print("\n--- 저서 입력 ---")
        works_count = insert_works(client)
        print(f"저서 {works_count}건 입력 완료")

        # 3. 핵심 주장
        print("\n--- 핵심 주장 입력 ---")
        claims_count = insert_claims(client)
        print(f"주장 {claims_count}건 입력 완료")

        # 4. 키워드
        print("\n--- 키워드 입력 ---")
        keywords_count = insert_keywords(client)
        print(f"키워드 {keywords_count}건 입력 완료")

        # 5. 관계
        print("\n--- 사상 관계 입력 ---")
        relations_count = insert_relations(client)
        print(f"관계 {relations_count}건 입력 완료")

        print("\n=== 흄 데이터 입력 완료 ===")
        print(f"총계: 사상가 1, 저서 {works_count}, 주장 {claims_count}, 키워드 {keywords_count}, 관계 {relations_count}")

    except Exception as e:
        print(f"[ERROR] {e}")
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
