"""로버트 노직(Robert Nozick) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS, INDEX_FIELDS
)


def insert_thinker(client):
    """노직 사상가 데이터 입력."""
    doc = {
        "id": "nozick",
        "name": "로버트 노직",
        "name_en": "Robert Nozick",
        "field": "political_philosophy",
        "era": "현대",
        "birth_year": 1938,
        "death_year": 2002,
        "background": (
            "미국 뉴욕 브루클린에서 유대계 가정에 태어났다. "
            "컬럼비아 대학교에서 학사 학위를, 프린스턴 대학교에서 박사 학위를 취득했다. "
            "하버드 대학교 철학과 교수로 재직하며 존 롤스의 동료이자 가장 강력한 비판자로 활동했다. "
            "1974년 출간한 '아나키에서 유토피아로(Anarchy, State, and Utopia)'는 "
            "롤스의 '정의론'에 대한 자유지상주의적 대안으로, 20세기 정치철학의 핵심 저작이 되었다. "
            "철학적 관심이 넓어 인식론, 합리성, 형이상학 등 다양한 분야에서도 독창적인 저작을 남겼다."
        ),
        "core_philosophy": (
            "노직의 핵심 사상은 자유지상주의(libertarianism)와 소유권적 정의론(entitlement theory)이다. "
            "정의는 분배의 결과 패턴이 아니라 취득과 이전의 과정이 정당한지에 의해 결정된다. "
            "정의의 세 원칙은: (1) 취득에서의 정의(justice in acquisition) — 로크적 단서 하에서의 최초 취득, "
            "(2) 이전에서의 정의(justice in transfer) — 자발적 교환과 증여, "
            "(3) 교정에서의 정의(justice in rectification) — 과거 부정의의 시정이다. "
            "이로부터 최소국가(minimal state), 즉 폭력·절도·사기 방지와 계약 이행에만 국한된 "
            "야경국가만이 도덕적으로 정당화될 수 있다고 주장했다. "
            "자기소유권(self-ownership)을 근본 원리로 삼아, "
            "재분배를 위한 과세는 강제노동과 동등하다고 논증했다."
        ),
        "keywords": [
            "소유권적 정의론",
            "최소국가",
            "자기소유권",
            "로크적 단서",
            "윌트 체임벌린 논변",
            "패턴화된 정의 비판",
            "야경국가",
            "자유지상주의"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="nozick", document=doc)
    print(f"[thinker] nozick: {result['result']}")
    return result


def insert_works(client):
    """노직 저서 데이터 입력."""
    works = [
        {
            "id": "nozick-anarchy-state-utopia",
            "thinker_id": "nozick",
            "title": "아나키에서 유토피아로",
            "title_original": "Anarchy, State, and Utopia",
            "year": 1974,
            "significance": (
                "20세기 정치철학의 가장 중요한 저작 중 하나. "
                "롤스의 '정의론'(1971)에 대한 자유지상주의적 대안을 체계적으로 제시했다. "
                "3부로 구성: 제1부 — 자연 상태에서 최소국가의 정당화(보이지 않는 손 설명), "
                "제2부 — 최소국가를 넘어서는 확장국가 비판(소유권적 정의론, 윌트 체임벌린 논변), "
                "제3부 — 유토피아 프레임워크(다양한 공동체의 자발적 선택). "
                "1975년 전미도서상(National Book Award) 수상. "
                "자유지상주의 정치철학의 고전이 되었으며, "
                "분배 정의에 대한 논의의 지형을 근본적으로 변화시켰다."
            ),
            "key_concepts": [
                "최소국가", "소유권적 정의론", "자기소유권", "윌트 체임벌린 논변",
                "보이지 않는 손 설명", "패턴화된 정의 비판", "로크적 단서", "유토피아 프레임워크"
            ]
        },
        {
            "id": "nozick-philosophical-explanations",
            "thinker_id": "nozick",
            "title": "철학적 설명",
            "title_original": "Philosophical Explanations",
            "year": 1981,
            "significance": (
                "노직이 정치철학 이후 인식론, 형이상학, 가치론으로 관심을 확장한 저작. "
                "지식의 조건으로 '추적(tracking)' 이론을 제시하여 게티어 문제에 대한 독창적 해법을 제안했다. "
                "인과적 조건부(counterfactual) 분석을 통해, "
                "참인 믿음이 지식이 되려면 진리를 '추적'해야 한다고 주장했다. "
                "자유의지, 개인의 정체성, 삶의 의미 등 광범위한 철학적 문제를 다루었다."
            ),
            "key_concepts": [
                "추적 이론", "반사실적 조건", "지식의 조건",
                "자유의지", "개인 정체성"
            ]
        },
        {
            "id": "nozick-examined-life",
            "thinker_id": "nozick",
            "title": "검토된 삶",
            "title_original": "The Examined Life",
            "year": 1989,
            "significance": (
                "일반 독자를 대상으로 한 철학적 에세이 모음. "
                "죽음, 부모와 자녀, 성(sexuality), 행복, 창조성 등 삶의 근본 문제를 성찰했다. "
                "이전의 엄격한 자유지상주의적 입장에서 일정 부분 후퇴하여, "
                "비자발적 협동 문제와 상징적 효과(symbolic meaning)를 인정하는 등 "
                "보다 유연한 정치적 입장을 시사했다."
            ),
            "key_concepts": [
                "삶의 의미", "행복", "자아의 본질",
                "창조성", "소크라테스적 삶"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """노직 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 소유권적 정의론
        {
            "id": "nozick-claim-001",
            "thinker_id": "nozick",
            "work_id": "nozick-anarchy-state-utopia",
            "source_detail": "Anarchy, State, and Utopia, Ch. 7 'Distributive Justice'",
            "claim": (
                "정의는 분배의 최종 상태(end-state)나 구조적 패턴이 아니라, "
                "소유물이 어떤 과정을 거쳐 취득되고 이전되었는지에 의해 결정된다. "
                "소유권적 정의론(entitlement theory)의 세 원칙은: "
                "(1) 취득에서의 정의 — 무주물의 최초 취득이 로크적 단서를 충족하면 정당하다. "
                "(2) 이전에서의 정의 — 정당하게 소유한 것의 자발적 이전은 정당하다. "
                "(3) 교정에서의 정의 — 부당한 취득이나 이전은 시정되어야 한다."
            ),
            "original_text": (
                "If the world were wholly just, the following inductive definition would exhaustively "
                "cover the subject of justice in holdings: "
                "1. A person who acquires a holding in accordance with the principle of justice in acquisition, "
                "is entitled to that holding. "
                "2. A person who acquires a holding in accordance with the principle of justice in transfer, "
                "from someone else entitled to the holding, is entitled to the holding. "
                "3. No one is entitled to a holding except by (repeated) applications of 1 and 2."
            ),
            "original_text_ko": (
                "만약 세계가 완전히 정의롭다면, 다음의 귀납적 정의가 소유에서의 정의 문제를 "
                "빠짐없이 다룰 것이다: "
                "1. 취득에서의 정의 원칙에 따라 소유물을 획득한 사람은 그 소유물에 대한 자격이 있다. "
                "2. 이전에서의 정의 원칙에 따라, 그 소유물에 대한 자격이 있는 다른 사람으로부터 "
                "소유물을 획득한 사람은 그 소유물에 대한 자격이 있다. "
                "3. 1과 2의 (반복된) 적용에 의하지 않고서는 누구도 소유물에 대한 자격이 없다."
            ),
            "explanation": (
                "소유권적 정의론은 노직 정치철학의 핵심이다. "
                "역사적(historical) 정의론으로서, 현재의 분배 상태가 정의로운지는 "
                "그 상태에 이르게 된 과정의 정당성에 달려 있다. "
                "이는 결과 상태의 패턴(예: 평등, 공리 극대화)을 기준으로 하는 "
                "롤스의 차등원칙 같은 패턴화된(patterned) 정의론과 근본적으로 대립한다."
            ),
            "argument": (
                "(1) 정의는 소유물(holdings)이 어떻게 발생했는지에 관한 것이다. "
                "(2) 정당한 취득과 정당한 이전의 연쇄가 현재의 소유를 정당화한다. "
                "(3) 결과 상태의 패턴은 정의의 기준이 될 수 없다 — 자유로운 거래가 어떤 패턴이든 깨뜨리기 때문이다. "
                "(4) 따라서 정의의 원칙은 역사적(historical)이고 비패턴화된(unpatterned) 것이어야 한다. "
                "(5) 과거의 부정의(강탈, 사기 등)가 있었다면 교정의 원칙으로 시정해야 한다. "
                "(6) 이 세 원칙을 충족하는 분배는, 결과가 어떤 패턴이든, 정의롭다."
            ),
            "counterpoint": (
                "존 롤스(John Rawls)는 '정의론'(A Theory of Justice, 1971)에서 "
                "순수한 절차적 정의만으로는 사회의 기본 구조가 만들어내는 누적적 불평등을 "
                "통제할 수 없다고 비판할 수 있다. 롤스에 따르면, 배경적 정의(background justice)가 "
                "보장되지 않으면 개별 거래가 공정하더라도 전체 분배가 정의롭다고 할 수 없다. "
                "G. A. 코헨(G. A. Cohen)은 'Self-Ownership, Freedom, and Equality'(1995)에서 "
                "자기소유권 테제가 자연적 재능의 도덕적 자의성을 무시한다고 비판했다."
            ),
            "context": (
                "노직의 소유권적 정의론은 로크의 자연권 전통에 뿌리를 두고 있으며, "
                "롤스의 분배적 정의론에 대한 가장 체계적인 자유지상주의적 대안이다."
            ),
            "keywords": ["소유권적 정의론", "취득의 정의", "이전의 정의", "교정의 정의"],
            "verified": False
        },
        # CLAIM-002: 최소국가론
        {
            "id": "nozick-claim-002",
            "thinker_id": "nozick",
            "work_id": "nozick-anarchy-state-utopia",
            "source_detail": "Anarchy, State, and Utopia, Part I, Ch. 2-5",
            "claim": (
                "최소국가(minimal state)만이 도덕적으로 정당화될 수 있다. "
                "최소국가는 폭력, 절도, 사기로부터의 보호와 계약 이행의 강제에만 국한된다. "
                "이보다 확장된 국가(재분배, 복지, 교육 등을 제공하는)는 "
                "개인의 권리를 침해하며 도덕적으로 정당화될 수 없다."
            ),
            "original_text": (
                "Our main conclusions about the state are that a minimal state, limited to the narrow functions "
                "of protection against force, theft, fraud, enforcement of contracts, and so on, is justified; "
                "that any more extensive state will violate persons' rights not to be forced to do certain things, "
                "and is unjustified."
            ),
            "original_text_ko": (
                "국가에 대한 우리의 주요 결론은 다음과 같다: 폭력, 절도, 사기로부터의 보호, "
                "계약의 집행 등 좁은 기능에 국한된 최소국가는 정당화되며, "
                "이보다 확장된 국가는 특정한 일을 하도록 강제받지 않을 개인의 권리를 침해하므로 "
                "정당화될 수 없다."
            ),
            "explanation": (
                "노직은 로크적 자연 상태에서 출발하여, 보이지 않는 손 과정을 통해 "
                "최소국가가 자연스럽게 발생할 수 있음을 보이고, "
                "이 최소국가가 무정부주의자의 우려와 달리 개인의 권리를 침해하지 않음을 논증한다. "
                "그러나 최소국가를 넘어서는 어떤 확장도 — 재분배, 가부장적 간섭, 도덕적 입법 등 — "
                "개인의 자유와 소유권을 침해한다."
            ),
            "argument": (
                "(1) 개인은 생명, 자유, 재산에 대한 자연적 권리를 가진다(로크). "
                "(2) 자연 상태의 보호 결사체들이 경쟁과 통합을 거쳐 지배적 보호 기관(dominant protective agency)이 된다. "
                "(3) 이 과정은 보이지 않는 손에 의해 발생하며, 누구의 권리도 침해하지 않는다. "
                "(4) 지배적 보호 기관은 자연스럽게 최소국가로 전환된다. "
                "(5) 이 최소국가는 정당하지만, 재분배 등 추가 기능을 수행하는 확장국가는 "
                "개인의 권리를 침해하므로 부당하다."
            ),
            "counterpoint": (
                "존 롤스(John Rawls)는 '정의론'(A Theory of Justice, 1971)에서 "
                "사회는 상호 이익을 위한 협동 체계이며, 이 협동의 이익을 공정하게 분배하는 것이 "
                "정의의 핵심 과제라고 주장했다. 롤스에 따르면 자연적 재능의 분배는 "
                "도덕적으로 자의적이므로, 재분배는 권리 침해가 아니라 공정성의 요구이다. "
                "사뮤엘 프리먼(Samuel Freeman)은 'Illiberal Libertarians'(2001)에서 "
                "노직의 최소국가가 사회적 협동의 호혜적 성격을 무시한다고 비판했다."
            ),
            "context": (
                "노직의 최소국가론은 자유지상주의의 핵심 정치 이론이며, "
                "야경국가(night-watchman state) 전통을 20세기 분석철학의 방법으로 정교화한 것이다."
            ),
            "keywords": ["최소국가", "야경국가", "보호 기관", "확장국가 비판"],
            "verified": False
        },
        # CLAIM-003: 자기소유권
        {
            "id": "nozick-claim-003",
            "thinker_id": "nozick",
            "work_id": "nozick-anarchy-state-utopia",
            "source_detail": "Anarchy, State, and Utopia, Ch. 3, Ch. 7",
            "claim": (
                "자기소유권(self-ownership)은 각 개인이 자기 자신의 몸, 재능, 노동에 대해 "
                "절대적인 권리를 가진다는 원리이다. "
                "타인이나 국가가 개인의 재능이나 노동의 산물에 대해 강제적으로 요구할 수 있는 "
                "정당한 근거는 없다. 자기소유권은 노직 정치철학의 근본 전제이다."
            ),
            "original_text": (
                "Seizing the results of someone's labor is equivalent to seizing hours from him "
                "and directing him to carry on various activities. If people force you to do certain work, "
                "or unrewarded work, for a certain period of time, they decide what you are to do "
                "and what purposes your work is to serve apart from your decisions. "
                "This process whereby they take this decision from you makes them a part-owner of you; "
                "it gives them a property right in you."
            ),
            "original_text_ko": (
                "누군가의 노동 결과를 빼앗는 것은 그에게서 시간을 빼앗고 "
                "그에게 여러 활동을 하도록 지시하는 것과 같다. "
                "만약 사람들이 당신에게 일정 기간 동안 특정 일이나 보상 없는 일을 강제한다면, "
                "그들은 당신이 무엇을 해야 하는지, 당신의 노동이 당신의 결정과 무관하게 "
                "어떤 목적에 봉사해야 하는지를 결정하는 것이다. "
                "이 결정을 당신에게서 빼앗는 과정은 그들을 당신의 부분적 소유자로 만든다; "
                "그것은 그들에게 당신에 대한 재산권을 준다."
            ),
            "explanation": (
                "자기소유권은 노직의 자유지상주의 체계의 근본 토대이다. "
                "각 개인은 자기 자신에 대한 완전한 소유권을 가지며, "
                "이는 타인의 신체를 도구로 사용하거나 노동의 산물을 강제로 빼앗는 것을 "
                "도덕적으로 금지한다. 이 원리로부터 과세를 통한 재분배에 대한 비판이 도출된다."
            ),
            "argument": (
                "(1) 각 개인은 자기 자신(몸, 재능, 노동)에 대한 절대적 소유권을 가진다. "
                "(2) 자기 노동의 결과물에 대한 권리는 자기소유권의 확장이다. "
                "(3) 타인의 노동 산물을 강제로 빼앗는 것은 그 사람의 일부를 소유하는 것과 같다. "
                "(4) 따라서 재분배를 위한 강제적 과세는 강제노동(forced labor)과 도덕적으로 동등하다. "
                "(5) 자기소유권을 침해하는 어떤 정책도 도덕적으로 정당화될 수 없다."
            ),
            "counterpoint": (
                "G. A. 코헨(G. A. Cohen)은 'Self-Ownership, Freedom, and Equality'(1995)에서 "
                "자기소유권 테제가 형식적 자유만을 보장하며 실질적 자유를 훼손한다고 비판했다. "
                "코헨에 따르면, 자기소유권과 외부 자원의 사적 소유를 결합하면 "
                "무소유자가 유소유자에게 종속되는 결과가 발생하며, "
                "이는 자유지상주의가 표방하는 자유의 이상과 모순된다."
            ),
            "context": (
                "자기소유권 개념은 로크의 '통치론'에 뿌리를 두고 있으며, "
                "노직이 이를 현대적으로 정교화하여 분배 정의 비판의 토대로 삼았다."
            ),
            "keywords": ["자기소유권", "강제노동", "노동의 산물", "개인의 권리"],
            "verified": False
        },
        # CLAIM-004: 로크적 단서
        {
            "id": "nozick-claim-004",
            "thinker_id": "nozick",
            "work_id": "nozick-anarchy-state-utopia",
            "source_detail": "Anarchy, State, and Utopia, Ch. 7, pp. 175-182",
            "claim": (
                "로크적 단서(Lockean Proviso)는 최초 취득의 정당성 조건이다. "
                "무주물의 취득은 타인의 상황을 악화시키지 않는 한에서만 정당하다. "
                "노직은 로크의 '충분히 좋은 것이 다른 이들을 위해 남아 있어야 한다'는 조건을 "
                "약한 형태로 재해석하여, 타인이 더 이상 그 자원을 자유롭게 사용할 수 없게 되더라도 "
                "전반적으로 타인의 상황이 악화되지 않으면 취득은 정당하다고 주장했다."
            ),
            "original_text": (
                "A process normally giving rise to a permanent bequeathable property right in a previously "
                "unowned thing will not do so if the position of others no longer at liberty to use the thing "
                "is thereby worsened."
            ),
            "original_text_ko": (
                "이전에 무주물이었던 것에 대해 영구적이고 상속 가능한 재산권을 발생시키는 과정은, "
                "그것을 더 이상 자유롭게 사용할 수 없게 된 타인의 상황이 "
                "그로 인해 악화되는 경우에는 그러한 권리를 발생시키지 않는다."
            ),
            "explanation": (
                "로크적 단서는 소유권적 정의론에서 취득의 정의 원칙을 제한하는 조건이다. "
                "무한한 자원이 있다면 취득에 제한이 필요 없겠지만, "
                "현실에서는 한 사람의 취득이 타인의 기회를 제한할 수 있다. "
                "노직은 로크의 '충분하고 좋은 것'이 남아야 한다는 강한 조건 대신, "
                "타인의 전반적 상황을 악화시키지 않으면 된다는 약한 조건을 채택했다."
            ),
            "argument": (
                "(1) 최초 취득이 정당하려면 일정한 제한 조건을 충족해야 한다. "
                "(2) 로크는 '다른 이들을 위해 충분하고 좋은 것이 남아야 한다'고 주장했다(강한 단서). "
                "(3) 강한 단서는 지나치게 제약적이어서, 결국 어떤 취득도 정당화하지 못할 수 있다. "
                "(4) 약한 단서: 취득이 타인의 전반적 상황을 악화시키지 않으면 정당하다. "
                "(5) 자본주의적 취득과 교환은 대체로 모든 이의 상황을 개선하므로, "
                "약한 로크적 단서를 충족한다."
            ),
            "counterpoint": (
                "제러미 월드론(Jeremy Waldron)은 'The Right to Private Property'(1988)에서 "
                "노직의 약한 로크적 단서가 지나치게 관대하여, "
                "극단적 불평등과 무소유자의 발생을 허용한다고 비판했다. "
                "월드론에 따르면, 취득 이전의 자유로운 사용 가능성이 박탈되는 것 자체가 "
                "상당한 손실이며, 노직의 '전반적 악화 없음' 기준은 이를 적절히 포착하지 못한다."
            ),
            "context": (
                "로크적 단서는 노직의 소유권적 정의론에서 최초 취득의 정당성을 "
                "제한하는 유일한 조건으로, 자유지상주의 체계 내의 자체적 제약이다."
            ),
            "keywords": ["로크적 단서", "최초 취득", "약한 단서", "정당한 취득"],
            "verified": False
        },
        # CLAIM-005: 패턴화된 정의론 비판
        {
            "id": "nozick-claim-005",
            "thinker_id": "nozick",
            "work_id": "nozick-anarchy-state-utopia",
            "source_detail": "Anarchy, State, and Utopia, Ch. 7, pp. 153-164",
            "claim": (
                "패턴화된 정의론(patterned theories of justice)은 자유와 양립할 수 없다. "
                "패턴화된 원칙은 분배가 특정 자연적 차원(노력, 도덕적 공로, 필요 등)에 따라 "
                "이루어져야 한다고 주장하는데, 자유로운 거래는 필연적으로 어떤 패턴이든 깨뜨린다. "
                "패턴을 유지하려면 지속적인 자유 침해(과세, 금지)가 불가피하다."
            ),
            "original_text": (
                "No end-state principle or distributional patterned principle of justice can be continuously "
                "realized without continuous interference with people's lives. Any favored pattern would be "
                "transformed into one unfavored by the principle, by people choosing to act in various ways; "
                "for example, by people exchanging goods and services with other people."
            ),
            "original_text_ko": (
                "어떤 최종 상태 원칙이나 분배 패턴화된 정의 원칙도 사람들의 삶에 대한 "
                "지속적인 간섭 없이는 지속적으로 실현될 수 없다. "
                "어떤 선호되는 패턴이든, 사람들이 다양한 방식으로 행동하기로 선택함으로써 — "
                "예를 들어 다른 사람들과 재화와 서비스를 교환함으로써 — "
                "그 원칙에 의해 선호되지 않는 패턴으로 변형될 것이다."
            ),
            "explanation": (
                "이 논변은 롤스의 차등원칙, 공리주의의 효용 극대화, 평등주의 등 "
                "모든 패턴화된 분배 원칙에 대한 일반적 비판이다. "
                "사람들이 자유롭게 거래하면 어떤 패턴이든 깨어지므로, "
                "패턴을 유지하려면 자유를 지속적으로 제한해야 한다. "
                "이는 패턴화된 정의와 자유 사이에 근본적 긴장이 있음을 보여준다."
            ),
            "argument": (
                "(1) 패턴화된 정의론은 분배가 특정 패턴(평등, 공로, 필요 등)을 따라야 한다고 주장한다. "
                "(2) 그러나 자유로운 사람들의 자발적 거래는 어떤 패턴이든 깨뜨린다. "
                "(3) 패턴을 복원하려면 거래의 자유를 제한하거나 결과를 재분배해야 한다. "
                "(4) 이는 지속적인 자유 침해를 요구한다. "
                "(5) 따라서 패턴화된 정의는 자유와 양립 불가능하다. "
                "(6) 정의론은 비패턴화된(unpatterned), 역사적(historical) 원칙이어야 한다."
            ),
            "counterpoint": (
                "존 롤스(John Rawls)는 '정의론'(A Theory of Justice, 1971)에서 "
                "정의의 원칙은 개별 거래가 아니라 사회의 기본 구조(basic structure)에 적용된다고 주장했다. "
                "따라서 제도적 수준에서의 규칙(과세, 상속법 등)은 개인의 자유로운 거래와 양립 가능하며, "
                "배경적 정의를 유지하면서도 자유를 존중할 수 있다. "
                "롤스에 따르면 노직은 기본 구조와 개별 거래의 구별을 간과한 것이다."
            ),
            "context": (
                "이 비판은 윌트 체임벌린 논변과 밀접하게 연결되며, "
                "분배 정의에 대한 자유지상주의적 접근의 핵심 논증이다."
            ),
            "keywords": ["패턴화된 정의", "최종 상태 원칙", "자유와 분배", "비패턴화된 원칙"],
            "verified": False
        },
        # CLAIM-006: 윌트 체임벌린 논변
        {
            "id": "nozick-claim-006",
            "thinker_id": "nozick",
            "work_id": "nozick-anarchy-state-utopia",
            "source_detail": "Anarchy, State, and Utopia, Ch. 7, pp. 160-164",
            "claim": (
                "윌트 체임벌린 논변(Wilt Chamberlain argument)은 패턴화된 정의론에 대한 "
                "구체적 반례이다. 어떤 정의로운 분배 D1에서 출발하더라도, "
                "사람들이 자유롭게 윌트 체임벌린의 경기를 보기 위해 입장료를 지불하면, "
                "새로운 분배 D2가 발생하며 이는 원래의 패턴을 깨뜨린다. "
                "D1이 정의롭고 각 이전이 자발적이라면, D2도 정의롭다."
            ),
            "original_text": (
                "It is not clear how those holding alternative conceptions of distributive justice "
                "can reject the claim that D2 is just. For it arises from D1 by a process in which "
                "each person has a right to dispose of his legitimately held resources as he wishes."
            ),
            "original_text_ko": (
                "분배 정의에 대한 대안적 관념을 가진 이들이 D2가 정의롭다는 주장을 "
                "어떻게 거부할 수 있는지 분명하지 않다. "
                "왜냐하면 D2는 D1에서, 각 사람이 자신이 정당하게 소유한 자원을 "
                "원하는 대로 처분할 권리를 가지는 과정을 통해 발생하기 때문이다."
            ),
            "explanation": (
                "윌트 체임벌린 논변은 패턴화된 정의론 비판의 가장 유명한 사고실험이다. "
                "어떤 패턴화된 분배(D1)든 사람들의 자유로운 선택에 의해 깨어진다. "
                "각 이전이 자발적이었으므로 새로운 분배(D2)도 정의롭다. "
                "원래 패턴을 복원하려면 사람들의 자유로운 거래를 금지해야 한다."
            ),
            "argument": (
                "(1) 어떤 정의론이든 선호하는 분배 D1이 있다고 가정한다. "
                "(2) 농구 스타 윌트 체임벌린이 팬들에게 입장료 25센트를 받겠다고 한다. "
                "(3) 100만 명이 자발적으로 25센트를 지불한다. "
                "(4) 체임벌린은 25만 달러를 벌며, 새로운 분배 D2가 발생한다. "
                "(5) D1이 정의롭고, 각 이전이 자발적이었으므로, D2도 정의롭다. "
                "(6) 그러나 D2는 D1의 패턴과 다르다. "
                "(7) 따라서 패턴을 유지하려면 자발적 이전을 금지해야 하며, 이는 자유의 침해이다."
            ),
            "counterpoint": (
                "존 롤스(John Rawls)는 정의 원칙이 개별 거래가 아니라 기본 구조에 적용된다고 응답할 수 있다. "
                "제도적 틀(과세 제도 등) 안에서 사람들은 자유롭게 거래하며, "
                "기본 구조가 배경적 정의를 유지한다. "
                "제럴드 도킨(Gerald Dworkin)은 개인의 자발적 동의만으로는 "
                "결과의 정의를 보장하지 못하며, 거래의 구조적 맥락이 중요하다고 반박했다."
            ),
            "context": (
                "윌트 체임벌린(실제 NBA 선수, 1936~1999)의 이름을 딴 이 논변은 "
                "정치철학에서 가장 많이 인용되고 논의되는 사고실험 중 하나이다."
            ),
            "keywords": ["윌트 체임벌린 논변", "자발적 이전", "패턴의 붕괴", "D1에서 D2로"],
            "verified": False
        },
        # CLAIM-007: 보이지 않는 손 설명
        {
            "id": "nozick-claim-007",
            "thinker_id": "nozick",
            "work_id": "nozick-anarchy-state-utopia",
            "source_detail": "Anarchy, State, and Utopia, Part I, Ch. 2",
            "claim": (
                "최소국가는 보이지 않는 손 과정(invisible hand process)을 통해 "
                "자연 상태에서 자연스럽게 발생한다. "
                "누구도 국가를 의도적으로 설계하지 않지만, "
                "보호 결사체들의 자유로운 경쟁과 통합을 통해 "
                "지배적 보호 기관이 등장하고, 이것이 최소국가로 전환된다. "
                "이 과정은 누구의 권리도 침해하지 않는다."
            ),
            "original_text": (
                "An invisible-hand explanation explains what looks as if it were produced by someone's "
                "intentional design, as not being brought about by anyone's intentions."
            ),
            "original_text_ko": (
                "보이지 않는 손 설명은, 누군가의 의도적 설계에 의해 만들어진 것처럼 보이는 것을, "
                "누구의 의도에 의해서도 초래되지 않은 것으로 설명한다."
            ),
            "explanation": (
                "노직은 애덤 스미스의 '보이지 않는 손' 개념을 정치 이론에 적용한다. "
                "자연 상태에서 사람들은 자기 보호를 위해 보호 결사체를 형성한다. "
                "이 결사체들이 경쟁하고 통합되면서 특정 영토에서 지배적 보호 기관이 등장한다. "
                "이 기관이 독립인(independents)에게도 보호를 제공하게 되면 최소국가가 된다."
            ),
            "argument": (
                "(1) 자연 상태에서 사람들은 자기 보호를 위해 상호 보호 결사체를 형성한다. "
                "(2) 결사체들 사이에 경쟁이 발생하고, 더 효과적인 결사체가 우세해진다. "
                "(3) 특정 영토에서 하나의 지배적 보호 기관(dominant protective agency)이 등장한다. "
                "(4) 이 기관은 비회원(독립인)의 위험한 자력 구제를 금지하되, "
                "이들에게 보상으로 보호 서비스를 제공한다. "
                "(5) 이로써 최소국가와 기능적으로 동일한 울트라최소국가(ultra-minimal state)가 탄생한다. "
                "(6) 이 전체 과정은 보이지 않는 손에 의한 것으로, 누구의 권리도 침해하지 않는다."
            ),
            "counterpoint": (
                "머레이 로스바드(Murray Rothbard)는 'Robert Nozick and the Immaculate Conception of the State'(1977)에서 "
                "노직의 보이지 않는 손 논변이 실제로는 지배적 보호 기관이 독립인의 자력 구제 권리를 "
                "침해한다고 비판했다. 로스바드에 따르면, 독립인에게 보상을 제공하더라도 "
                "그의 동의 없이 자력 구제를 금지하는 것은 권리 침해이며, "
                "따라서 최소국가조차 도덕적으로 정당화되지 않는다(무정부자본주의 입장)."
            ),
            "context": (
                "보이지 않는 손 설명은 노직의 방법론적 개인주의를 보여주며, "
                "사회계약론의 합의 모델과 달리 자연적 과정으로 국가를 설명한다."
            ),
            "keywords": ["보이지 않는 손", "보호 결사체", "지배적 보호 기관", "자연적 발생"],
            "verified": False
        },
        # CLAIM-008: 유토피아 프레임워크
        {
            "id": "nozick-claim-008",
            "thinker_id": "nozick",
            "work_id": "nozick-anarchy-state-utopia",
            "source_detail": "Anarchy, State, and Utopia, Part III, Ch. 10",
            "claim": (
                "유토피아 프레임워크(framework for utopia)는 최소국가를 '메타유토피아'로 재해석한다. "
                "최소국가는 그 안에서 사람들이 자발적으로 다양한 공동체를 형성하고 "
                "각자의 이상에 따라 살 수 있는 틀을 제공한다. "
                "단일한 유토피아는 인간의 다양성을 수용할 수 없으며, "
                "최소국가만이 다양한 유토피아적 실험들이 공존할 수 있는 프레임워크이다."
            ),
            "original_text": (
                "The framework is libertarian and laissez-faire. The state may not use its coercive apparatus "
                "for the purpose of getting some citizens to aid others, or in order to prohibit activities "
                "to people for their own good or protection."
            ),
            "original_text_ko": (
                "이 프레임워크는 자유지상주의적이고 자유방임적이다. "
                "국가는 일부 시민이 다른 시민을 돕도록 하기 위해, "
                "또는 사람들 자신의 이익이나 보호를 위해 활동을 금지하기 위해 "
                "강제 장치를 사용할 수 없다."
            ),
            "explanation": (
                "유토피아 프레임워크는 '아나키에서 유토피아로'의 마지막 부분으로, "
                "최소국가를 단순한 야경국가가 아니라 다양한 삶의 방식이 공존하는 "
                "고차원적 틀로 재해석한다. 사람들은 자유롭게 사회주의 공동체, "
                "종교 공동체, 자유주의 공동체 등을 형성할 수 있으며, "
                "최소국가는 이들의 공존을 보장한다."
            ),
            "argument": (
                "(1) 사람들은 서로 다른 이상적 삶의 방식을 가진다. "
                "(2) 단일한 유토피아(사회주의, 종교적, 자유주의적 등)는 "
                "이러한 다양성을 수용할 수 없다. "
                "(3) 따라서 유토피아는 단일한 공동체가 아니라, "
                "다양한 공동체가 자유롭게 형성되고 개인이 자유롭게 선택할 수 있는 '프레임워크'여야 한다. "
                "(4) 최소국가는 바로 이러한 프레임워크를 제공한다. "
                "(5) 최소국가 = 메타유토피아: 유토피아를 위한 유토피아이다."
            ),
            "counterpoint": (
                "존 롤스(John Rawls)는 '정치적 자유주의'(Political Liberalism, 1993)에서 "
                "합당한 다원주의를 인정하면서도, 정의의 원칙은 모든 공동체를 포괄하는 "
                "기본 구조에 적용되어야 한다고 주장했다. 롤스에 따르면 노직의 프레임워크는 "
                "공동체 간 불평등과 취약한 구성원에 대한 보호를 간과한다. "
                "윌 킴리카(Will Kymlicka)는 'Contemporary Political Philosophy'(2002)에서 "
                "자발적 선택이라는 전제가 현실의 권력 불균형과 정보 비대칭을 무시한다고 비판했다."
            ),
            "context": (
                "유토피아 프레임워크는 노직의 자유지상주의에 적극적·긍정적 비전을 부여하며, "
                "단순한 국가 비판을 넘어 다원적 사회에 대한 구상으로 나아간다."
            ),
            "keywords": ["유토피아 프레임워크", "메타유토피아", "자발적 공동체", "다양한 삶의 방식"],
            "verified": False
        },
        # CLAIM-009: 과세 = 강제노동 논변
        {
            "id": "nozick-claim-009",
            "thinker_id": "nozick",
            "work_id": "nozick-anarchy-state-utopia",
            "source_detail": "Anarchy, State, and Utopia, Ch. 7, pp. 169-172",
            "claim": (
                "재분배를 위한 소득세는 강제노동(forced labor)과 도덕적으로 동등하다. "
                "노동 소득에 대한 과세는 사람의 노동 시간의 일부를 강제로 빼앗는 것이며, "
                "이는 그 사람에 대한 부분적 소유권을 행사하는 것과 같다. "
                "이는 자기소유권 원칙에 대한 직접적 침해이다."
            ),
            "original_text": (
                "Taxation of earnings from labor is on a par with forced labor. "
                "Some persons find this claim obviously true: taking the earnings of n hours labor "
                "is like taking n hours from the person; it is like forcing the person "
                "to work n hours for another's purpose."
            ),
            "original_text_ko": (
                "노동 소득에 대한 과세는 강제노동과 동등하다. "
                "어떤 사람들은 이 주장이 명백히 참이라고 생각한다: "
                "n시간 노동의 소득을 빼앗는 것은 그 사람에게서 n시간을 빼앗는 것과 같다; "
                "그것은 그 사람에게 다른 사람의 목적을 위해 n시간 동안 일하도록 강제하는 것과 같다."
            ),
            "explanation": (
                "이 논변은 자기소유권으로부터 재분배적 과세의 부정당성을 도출하는 핵심 논증이다. "
                "내 노동은 나의 것이며, 그 산물도 나의 것이다. "
                "국가가 내 노동 소득의 일부를 과세한다면, 그것은 내 노동 시간의 일부를 "
                "타인의 목적에 강제로 사용하는 것이며, 이는 강제노동의 한 형태이다."
            ),
            "argument": (
                "(1) 자기소유권: 각 개인은 자기 자신과 자기 노동에 대한 완전한 소유권을 가진다. "
                "(2) 노동의 산물에 대한 권리는 자기소유권의 확장이다. "
                "(3) 소득세는 노동 산물의 일부를 강제로 빼앗는 것이다. "
                "(4) 이는 그만큼의 노동 시간을 타인을 위해 강제로 일하게 하는 것과 동일하다. "
                "(5) 강제노동은 자기소유권의 침해이며 도덕적으로 부당하다. "
                "(6) 따라서 재분배를 위한 소득세도 도덕적으로 부당하다."
            ),
            "counterpoint": (
                "리엄 머피(Liam Murphy)와 토마스 네이글(Thomas Nagel)은 "
                "'The Myth of Ownership'(2002)에서 세전 소득(pre-tax income)이 "
                "'자연적' 소유라는 전제 자체가 허구라고 비판했다. "
                "이들에 따르면, 소유권은 법적·제도적 체계의 산물이며, "
                "세전 소득은 과세 체계를 포함한 전체 법체계에 의해 규정된 것이다. "
                "따라서 과세를 '빼앗김'으로 보는 것은 제도 이전의 자연적 소유권을 전제하는 오류이다."
            ),
            "context": (
                "이 논변은 자유지상주의 조세 비판의 가장 유명한 표현이며, "
                "복지국가에 대한 근본적 도전으로 널리 논의되고 있다."
            ),
            "keywords": ["과세와 강제노동", "소득세 비판", "자기소유권 침해", "재분배 비판"],
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """노직 키워드 데이터 입력."""
    keywords = [
        {
            "id": "nozick-kw-001",
            "thinker_id": "nozick",
            "term": "소유권적 정의론 (Entitlement Theory)",
            "term_original": "entitlement theory",
            "definition": (
                "정의는 분배의 최종 상태나 패턴이 아니라 소유물의 취득과 이전 과정의 정당성에 의해 결정된다는 이론. "
                "세 원칙으로 구성: (1) 취득에서의 정의, (2) 이전에서의 정의, (3) 교정에서의 정의. "
                "역사적(historical)이고 비패턴화된(unpatterned) 정의론이다."
            ),
            "related_claims": ["nozick-claim-001"],
            "source": "Anarchy, State, and Utopia, Ch. 7"
        },
        {
            "id": "nozick-kw-002",
            "thinker_id": "nozick",
            "term": "최소국가 (Minimal State)",
            "term_original": "minimal state",
            "definition": (
                "폭력, 절도, 사기로부터의 보호와 계약 이행의 강제에만 국한된 국가. "
                "야경국가(night-watchman state)와 동의어. "
                "이보다 확장된 국가는 개인의 권리를 침해하므로 도덕적으로 정당화될 수 없다. "
                "보이지 않는 손 과정을 통해 자연 상태에서 정당하게 발생한다."
            ),
            "related_claims": ["nozick-claim-002", "nozick-claim-007"],
            "source": "Anarchy, State, and Utopia, Part I"
        },
        {
            "id": "nozick-kw-003",
            "thinker_id": "nozick",
            "term": "자기소유권 (Self-Ownership)",
            "term_original": "self-ownership",
            "definition": (
                "각 개인이 자기 자신의 몸, 재능, 노동에 대해 절대적인 소유권을 가진다는 원리. "
                "타인이나 국가가 개인의 재능이나 노동의 산물에 대해 "
                "강제적으로 요구할 정당한 근거는 없다. "
                "노직 자유지상주의의 근본 전제이며, 과세=강제노동 논변의 기초이다."
            ),
            "related_claims": ["nozick-claim-003", "nozick-claim-009"],
            "source": "Anarchy, State, and Utopia, Ch. 3, Ch. 7"
        },
        {
            "id": "nozick-kw-004",
            "thinker_id": "nozick",
            "term": "로크적 단서 (Lockean Proviso)",
            "term_original": "Lockean proviso",
            "definition": (
                "최초 취득의 정당성을 제한하는 조건. "
                "무주물의 취득은 타인의 전반적 상황을 악화시키지 않는 한에서만 정당하다. "
                "로크의 '충분하고 좋은 것이 남아야 한다'는 강한 조건을 "
                "노직이 약한 형태로 재해석한 것이다."
            ),
            "related_claims": ["nozick-claim-004"],
            "source": "Anarchy, State, and Utopia, Ch. 7, pp. 175-182"
        },
        {
            "id": "nozick-kw-005",
            "thinker_id": "nozick",
            "term": "윌트 체임벌린 논변 (Wilt Chamberlain Argument)",
            "term_original": "Wilt Chamberlain argument",
            "definition": (
                "패턴화된 정의론에 대한 사고실험적 반례. "
                "어떤 정의로운 분배(D1)에서 출발하더라도, 자유로운 거래를 통해 "
                "원래 패턴과 다른 분배(D2)가 발생한다. "
                "D1이 정의롭고 각 이전이 자발적이라면 D2도 정의로우므로, "
                "패턴 유지를 위해서는 자유를 침해해야 한다는 것을 보여준다."
            ),
            "related_claims": ["nozick-claim-006"],
            "source": "Anarchy, State, and Utopia, Ch. 7, pp. 160-164"
        },
        {
            "id": "nozick-kw-006",
            "thinker_id": "nozick",
            "term": "패턴화된 정의 (Patterned Justice)",
            "term_original": "patterned principle of justice",
            "definition": (
                "분배가 특정 자연적 차원(도덕적 공로, 필요, 노력, 한계생산 등)에 따라 "
                "이루어져야 한다고 주장하는 정의 원칙. "
                "롤스의 차등원칙, 공리주의, 평등주의 등이 해당한다. "
                "노직은 모든 패턴화된 원칙이 자유와 양립 불가능하다고 비판했다."
            ),
            "related_claims": ["nozick-claim-005", "nozick-claim-006"],
            "source": "Anarchy, State, and Utopia, Ch. 7"
        },
        {
            "id": "nozick-kw-007",
            "thinker_id": "nozick",
            "term": "야경국가 (Night-Watchman State)",
            "term_original": "night-watchman state",
            "definition": (
                "최소국가의 별칭으로, 국방, 치안, 사법에만 국한된 국가를 가리킨다. "
                "19세기 자유주의 전통에서 유래한 용어이며, "
                "노직은 이를 도덕적으로 정당화할 수 있는 유일한 국가 형태로 제시했다."
            ),
            "related_claims": ["nozick-claim-002"],
            "source": "Anarchy, State, and Utopia, Part I"
        },
        {
            "id": "nozick-kw-008",
            "thinker_id": "nozick",
            "term": "자유지상주의 (Libertarianism)",
            "term_original": "libertarianism",
            "definition": (
                "개인의 자유와 소유권을 정치 도덕의 핵심으로 삼는 사상. "
                "국가의 역할을 최소한으로 제한하고, 자발적 교환과 계약의 자유를 최대화한다. "
                "노직은 분석철학적 방법으로 자유지상주의를 체계적으로 정당화한 대표적 사상가이다."
            ),
            "related_claims": ["nozick-claim-001", "nozick-claim-002", "nozick-claim-003"],
            "source": "Anarchy, State, and Utopia 전반"
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """노직 관계 데이터 입력."""
    # 먼저 기존 관계 확인
    existing_relations = set()
    try:
        result = client.search(
            index=INDEX_RELATIONS,
            query={"bool": {"should": [
                {"term": {"from_thinker": "nozick"}},
                {"term": {"to_thinker": "nozick"}}
            ]}},
            _source=["id"],
            size=20
        )
        for hit in result['hits']['hits']:
            existing_relations.add(hit['_source']['id'])
        print(f"[relations] 기존 nozick 관련 관계: {existing_relations}")
    except Exception:
        pass

    relations = [
        {
            "id": "relation-locke-nozick",
            "from_thinker": "locke",
            "to_thinker": "nozick",
            "type": "influenced",
            "description": (
                "존 로크(John Locke, 1632~1704)의 자연권 이론과 소유권 이론은 "
                "노직의 자유지상주의에 가장 근본적인 영향을 미쳤다. "
                "로크의 '통치론(Two Treatises of Government, 1689)'에서 제시된 "
                "자연 상태, 자연적 권리(생명, 자유, 재산), 노동에 의한 소유권 취득 이론은 "
                "노직의 소유권적 정의론의 직접적 토대이다. "
                "'로크적 단서(Lockean proviso)'라는 명칭 자체가 이 지적 계보를 드러낸다. "
                "노직은 로크의 자연 상태를 현대적으로 재구성하여 최소국가의 정당화 논변을 전개했다."
            ),
            "strength": "강함",
            "period": "20세기"
        },
        {
            "id": "relation-nozick-libertarianism",
            "from_thinker": "nozick",
            "to_thinker": "nozick",
            "type": "founded",
            "description": (
                "노직은 '아나키에서 유토피아로'(1974)를 통해 "
                "학술적 자유지상주의(academic libertarianism)의 토대를 놓았다. "
                "분석철학적 엄밀성으로 자유지상주의를 정당화한 최초의 체계적 시도로, "
                "이후 자유지상주의 정치철학의 모든 논의가 이 저작을 기준점으로 삼게 되었다. "
                "좌파 자유지상주의(left-libertarianism)와 우파 자유지상주의의 구분도 "
                "노직의 논변에 대한 반응으로 발전했다."
            ),
            "strength": "강함",
            "period": "20세기"
        }
    ]

    inserted = 0
    for rel in relations:
        if rel["id"] in existing_relations:
            print(f"[relation] {rel['id']}: 이미 존재 (건너뜀)")
            continue
        result = client.index(index=INDEX_RELATIONS, id=rel["id"], document=rel)
        print(f"[relation] {rel['id']}: {result['result']}")
        inserted += 1

    return inserted


def verify_data(client):
    """입력된 데이터를 전수 확인."""
    print("\n=== 전수 확인 ===")

    # refresh
    client.indices.refresh(index="_all")

    # thinker 확인
    r = client.get(index=INDEX_THINKERS, id="nozick")
    print(f"[thinker] nozick: name={r['_source']['name_en']}, era={r['_source']['era']}, field={r['_source']['field']}")

    # works 확인
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "nozick"}})
    print(f"[works] nozick 저서 수: {works_count['count']}")
    works_result = client.search(
        index=INDEX_WORKS,
        query={"term": {"thinker_id": "nozick"}},
        _source=["id", "title_original", "year"],
        size=10
    )
    for hit in works_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['title_original']} ({s['year']})")

    # claims 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "nozick"}})
    print(f"[claims] nozick 주장 수: {claims_count['count']}")
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "nozick"}},
        size=20,
        _source=["id", "claim", "argument", "counterpoint", "original_text", "original_text_ko", "verified"]
    )
    missing_fields = []
    for hit in claims_result['hits']['hits']:
        s = hit['_source']
        has_arg = bool(s.get('argument'))
        has_cp = bool(s.get('counterpoint'))
        has_ot = bool(s.get('original_text'))
        has_otk = bool(s.get('original_text_ko'))
        print(f"  - {s['id']}: argument={has_arg}, counterpoint={has_cp}, original_text={has_ot}, original_text_ko={has_otk}, verified={s.get('verified')}")
        if not has_arg or not has_cp or not has_ot or not has_otk:
            missing_fields.append(s['id'])

    if missing_fields:
        print(f"[경고] 필수 필드 누락: {missing_fields}")
    else:
        print("[OK] 모든 claim에 argument+counterpoint+original_text+original_text_ko 존재")

    # keywords 확인
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "nozick"}})
    print(f"[keywords] nozick 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_count = client.count(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "nozick"}},
            {"term": {"to_thinker": "nozick"}}
        ]}}
    )
    print(f"[relations] nozick 관련 관계 수: {rel_count['count']}")
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "nozick"}},
            {"term": {"to_thinker": "nozick"}}
        ]}},
        _source=["id", "from_thinker", "to_thinker", "type"],
        size=10
    )
    for hit in rel_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['from_thinker']} --[{s['type']}]--> {s['to_thinker']}")

    return {
        "works": works_count['count'],
        "claims": claims_count['count'],
        "keywords": kw_count['count'],
        "relations": rel_count['count'],
        "missing_fields": missing_fields
    }


def main():
    client = get_client()
    try:
        print("=== 로버트 노직(Robert Nozick) 데이터 입력 시작 ===\n")

        print("1. 사상가 입력")
        insert_thinker(client)

        print("\n2. 저서 입력")
        works_n = insert_works(client)
        print(f"   총 {works_n}건 입력")

        print("\n3. 핵심 주장 입력")
        claims_n = insert_claims(client)
        print(f"   총 {claims_n}건 입력")

        print("\n4. 키워드 입력")
        kw_n = insert_keywords(client)
        print(f"   총 {kw_n}건 입력")

        print("\n5. 관계 입력")
        rel_n = insert_relations(client)
        print(f"   총 {rel_n}건 입력")

        stats = verify_data(client)
        print("\n=== 입력 완료 ===")
        print(f"thinker: 1건 | works: {stats['works']}건 | claims: {stats['claims']}건 | "
              f"keywords: {stats['keywords']}건 | relations: {stats['relations']}건")

        return stats

    finally:
        close_client(client)


if __name__ == "__main__":
    main()
