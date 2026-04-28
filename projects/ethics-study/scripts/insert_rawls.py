"""존 롤스(John Rawls) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS, INDEX_FIELDS
)


def ensure_field(client):
    """정치철학 분야가 ethics-fields 인덱스에 없으면 추가."""
    try:
        client.get(index=INDEX_FIELDS, id="political_philosophy")
        print("[field] political_philosophy: 이미 존재")
    except Exception:
        doc = {
            "id": "political_philosophy",
            "name": "정치철학",
            "description": (
                "국가, 권력, 정의, 자유, 권리, 사회계약 등 정치적 삶의 근본 원리를 탐구하는 철학 분야. "
                "홉스, 로크, 루소의 사회계약론, 롤스의 정의론, 공동체주의 등을 포함한다."
            ),
            "order": 3
        }
        result = client.index(index=INDEX_FIELDS, id="political_philosophy", document=doc)
        print(f"[field] political_philosophy: {result['result']}")


def insert_thinker(client):
    """롤스 사상가 데이터 입력."""
    doc = {
        "id": "rawls",
        "name": "존 롤스",
        "name_en": "John Rawls",
        "field": "political_philosophy",
        "era": "현대",
        "birth_year": 1921,
        "death_year": 2002,
        "background": (
            "미국 메릴랜드 주 볼티모어에서 태어났다. 프린스턴 대학교에서 학사 및 박사 학위를 취득했다. "
            "2차 세계대전 중 미 육군에 입대하여 태평양 전선에서 복무했으며, "
            "히로시마 원폭 투하 후 일본에서 복무한 경험이 전쟁과 정의에 대한 깊은 성찰로 이어졌다. "
            "코넬 대학교, MIT를 거쳐 1962년부터 하버드 대학교 철학과 교수로 재직하며 "
            "정치철학의 부활을 이끌었다. 1971년 출간한 '정의론(A Theory of Justice)'은 "
            "20세기 정치철학에서 가장 영향력 있는 저작으로 평가받으며, "
            "공리주의와 직관주의에 대한 체계적 대안을 제시했다. "
            "만년에는 뇌졸중으로 건강이 악화된 가운데서도 '만민법', '공정으로서의 정의: 재서술' 등을 집필했다."
        ),
        "core_philosophy": (
            "롤스의 핵심 사상은 '공정으로서의 정의(justice as fairness)'이다. "
            "원초적 입장(original position)이라는 가상적 상황에서 무지의 베일(veil of ignorance) 뒤에 놓인 "
            "합리적 당사자들이 사회의 기본 구조를 규율할 정의 원칙에 합의한다는 사고실험이다. "
            "이로부터 도출되는 정의의 두 원칙은: (1) 평등한 기본적 자유의 원칙, "
            "(2a) 공정한 기회균등의 원칙과 (2b) 차등원칙(최소수혜자에게 최대 이익)이다. "
            "제1원칙은 제2원칙에 사전적으로(lexically) 우선한다. "
            "후기 저작에서는 합당한 다원주의의 사실을 인정하고, "
            "중첩적 합의(overlapping consensus)와 공적 이성(public reason)에 기초한 "
            "정치적 자유주의(political liberalism)로 발전시켰다."
        ),
        "philosophical_journey": (
            "초기(~1950년대): 프린스턴 박사논문에서 도덕 판단의 성격을 탐구했다. "
            "2차 세계대전 참전 경험이 정의와 불의에 대한 근본적 물음을 촉발했다. "
            "중기(1958~1971): '공정으로서의 정의(1958)', '정의감(1963)', '분배적 정의(1967)' 등 "
            "일련의 논문을 통해 정의론의 핵심 논증을 점진적으로 발전시켰다. "
            "1971년 대작 '정의론'을 출간하여 공리주의에 대한 칸트적 대안을 체계적으로 제시했다. "
            "후기(1980~2002): 샌델, 왈저, 매킨타이어 등 공동체주의자들의 비판에 대응하여 "
            "'정치적 자유주의(1993)'에서 포괄적 자유주의에서 정치적 자유주의로 전환했다. "
            "'만민법(1999)'에서 국제정의론을, '공정으로서의 정의: 재서술(2001)'에서 "
            "정의론의 최종 정리를 시도했다."
        ),
        "keywords": [
            "공정으로서의 정의",
            "원초적 입장",
            "무지의 베일",
            "차등원칙",
            "평등한 자유의 원칙",
            "사전적 순서",
            "반성적 균형",
            "중첩적 합의",
            "공적 이성",
            "기본 구조",
            "최소극대화",
            "합당한 다원주의"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="rawls", document=doc)
    print(f"[thinker] rawls: {result['result']}")
    return result


def insert_works(client):
    """롤스 저서 데이터 입력."""
    works = [
        {
            "id": "rawls-theory-of-justice",
            "thinker_id": "rawls",
            "title": "정의론",
            "title_original": "A Theory of Justice",
            "year": 1971,
            "significance": (
                "20세기 정치철학에서 가장 영향력 있는 저작. "
                "공리주의와 직관주의에 대한 체계적 대안으로서 '공정으로서의 정의'를 제시했다. "
                "3부로 구성: 제1부 '이론(Theory)' — 원초적 입장, 무지의 베일, 정의의 두 원칙, "
                "제2부 '제도(Institutions)' — 정의 원칙의 제도적 적용, "
                "제3부 '목적(Ends)' — 정의로운 사회에서의 선과 안정성. "
                "사회계약론의 전통을 가장 추상적인 수준으로 끌어올려, "
                "칸트적 구성주의에 기초한 정의론을 전개했다. "
                "1999년 개정판에서 일부 논증을 수정했다."
            ),
            "key_concepts": [
                "공정으로서의 정의", "원초적 입장", "무지의 베일", "정의의 두 원칙",
                "차등원칙", "기본 구조", "반성적 균형", "최소극대화"
            ]
        },
        {
            "id": "rawls-political-liberalism",
            "thinker_id": "rawls",
            "title": "정치적 자유주의",
            "title_original": "Political Liberalism",
            "year": 1993,
            "significance": (
                "정의론 이후 롤스 사상의 가장 중요한 발전을 담은 저작. "
                "합당한 다원주의의 사실을 정면으로 수용하여, "
                "정의론의 공정으로서의 정의가 포괄적 교설(comprehensive doctrine)이 아니라 "
                "정치적 정의관(political conception of justice)임을 명확히 했다. "
                "중첩적 합의(overlapping consensus), 공적 이성(public reason), "
                "입헌 민주주의의 정당성 원리 등 핵심 개념을 제시했다. "
                "공동체주의 비판에 대한 롤스의 체계적 응답이다."
            ),
            "key_concepts": [
                "정치적 자유주의", "합당한 다원주의", "중첩적 합의",
                "공적 이성", "정치적 정의관", "입헌 민주주의"
            ]
        },
        {
            "id": "rawls-law-of-peoples",
            "thinker_id": "rawls",
            "title": "만민법",
            "title_original": "The Law of Peoples",
            "year": 1999,
            "significance": (
                "롤스의 국제정의론을 체계적으로 전개한 저작. "
                "자유주의적 인민(liberal peoples)과 적정 수준의 인민(decent peoples) 사이의 "
                "만민법(Law of Peoples)의 원칙을 도출한다. "
                "국내 정의론의 원초적 입장을 국제적 수준으로 확장하되, "
                "세계시민주의(cosmopolitanism)가 아니라 인민 중심의 접근을 취했다. "
                "무법 국가, 고통받는 사회, 이상적 이론과 비이상적 이론의 관계를 논한다."
            ),
            "key_concepts": [
                "만민법", "자유주의적 인민", "적정 수준의 인민",
                "인권", "정의로운 전쟁", "원조 의무"
            ]
        },
        {
            "id": "rawls-justice-as-fairness-restatement",
            "thinker_id": "rawls",
            "title": "공정으로서의 정의: 재서술",
            "title_original": "Justice as Fairness: A Restatement",
            "year": 2001,
            "significance": (
                "롤스가 생애 마지막으로 정리한 정의론의 최종 버전. "
                "정의론과 정치적 자유주의의 핵심 논증을 통합적으로 재서술하며, "
                "재산소유 민주주의(property-owning democracy)와 자유주의적 사회주의를 "
                "정의의 두 원칙을 실현할 수 있는 체제로 제시했다. "
                "복지국가 자본주의(welfare-state capitalism)는 차등원칙을 충족하지 못한다고 비판했다."
            ),
            "key_concepts": [
                "재산소유 민주주의", "자유주의적 사회주의",
                "기본 구조", "배경적 정의", "호혜성"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """롤스 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 공정으로서의 정의
        {
            "id": "rawls-claim-001",
            "thinker_id": "rawls",
            "work_id": "rawls-theory-of-justice",
            "source_detail": "A Theory of Justice, §1-4",
            "claim": (
                "정의는 사회 제도의 제1덕목(first virtue)이다. "
                "정의의 핵심 관념은 '공정으로서의 정의(justice as fairness)'로, "
                "정의 원칙은 자유롭고 평등한 사람들이 공정한 조건 아래에서 합의할 원칙이다. "
                "이는 공리주의의 최대다수 최대행복 원칙과 직관주의의 자명한 원칙 목록에 대한 체계적 대안이다."
            ),
            "original_text": (
                "Justice is the first virtue of social institutions, as truth is of systems of thought. "
                "A theory however elegant and economical must be rejected or revised if it is untrue; "
                "likewise laws and institutions no matter how efficient and well-arranged must be reformed or abolished if they are unjust."
            ),
            "original_text_ko": (
                "진리가 사고 체계의 제1덕목이듯, 정의는 사회 제도의 제1덕목이다. "
                "아무리 우아하고 경제적인 이론이라도 참이 아니면 거부되거나 수정되어야 한다. "
                "마찬가지로 아무리 효율적이고 잘 정비된 법과 제도라도 정의롭지 못하면 개혁되거나 폐지되어야 한다."
            ),
            "explanation": (
                "롤스는 정의를 사회 제도의 가장 중요한 가치로 놓음으로써, "
                "효율성이나 사회적 총합 복지보다 정의가 우선함을 선언한다. "
                "공정으로서의 정의는 사회계약론의 전통(로크, 루소, 칸트)을 가장 추상적인 수준으로 "
                "끌어올린 것으로, 합리적이고 자유로운 사람들이 평등한 초기 상황에서 "
                "사회의 기본 조건(terms of association)을 규정할 원칙에 합의한다는 구상이다."
            ),
            "argument": (
                "(1) 정의는 사회 제도의 제1덕목이다. 효율성이나 안정성보다 정의가 우선한다. "
                "(2) 각 개인은 정의에 기초한 불가침성을 가지며, 사회 전체의 복지라는 이유로도 유린될 수 없다. "
                "(3) 공리주의는 개인의 불가침성을 보장하지 못한다(소수의 희생을 정당화할 수 있다). "
                "(4) 직관주의는 원칙들 사이의 우선순위를 제공하지 못한다. "
                "(5) 공정으로서의 정의는 사회계약론을 일반화하여, 공정한 초기 상황에서의 합의로 정의 원칙을 도출한다. "
                "(6) 이 접근은 개인의 불가침성을 보장하면서도 원칙 간 우선순위를 명확히 한다."
            ),
            "counterpoint": (
                "공리주의자 존 C. 하사니(John C. Harsanyi)는 'Can the Maximin Principle Serve as a Basis for Morality?'(1975)에서 "
                "원초적 입장의 합리적 당사자들은 최소극대화가 아니라 기대효용 극대화를 선택할 것이며, "
                "이는 공리주의로 귀결된다고 반박했다. "
                "로버트 노직(Robert Nozick)은 '아나키, 국가, 유토피아'(Anarchy, State, and Utopia, 1974)에서 "
                "정의는 분배 패턴이 아니라 개인의 자격(entitlement)과 정당한 이전 과정에 의해 결정된다고 비판했다."
            ),
            "context": (
                "1950~60년대 영미 정치철학은 메타윤리학과 언어분석에 치중하여 "
                "규범적 정치이론이 쇠퇴한 상태였다. 롤스의 정의론은 이 흐름을 역전시켜 "
                "규범적 정치철학의 부활을 이끌었다."
            ),
            "keywords": ["공정으로서의 정의", "제1덕목", "개인의 불가침성"],
            "verified": False
        },
        # CLAIM-002: 원초적 입장
        {
            "id": "rawls-claim-002",
            "thinker_id": "rawls",
            "work_id": "rawls-theory-of-justice",
            "source_detail": "A Theory of Justice, §4, §20-25",
            "claim": (
                "원초적 입장(original position)은 정의 원칙 선택을 위한 공정한 초기 상황이다. "
                "이 가상적 상황에서 합리적 당사자들이 사회의 기본 구조를 규율할 정의 원칙을 선택한다. "
                "원초적 입장은 전통적 사회계약론의 자연 상태에 대응하되, "
                "역사적 사실이 아니라 순수한 가설적 장치(hypothetical device)이다."
            ),
            "original_text": (
                "The original position is not, of course, thought of as an actual historical state of affairs, "
                "much less as a primitive condition of culture. It is understood as a purely hypothetical situation "
                "characterized so as to lead to a certain conception of justice."
            ),
            "original_text_ko": (
                "원초적 입장은 물론 실제 역사적 사태로 생각되지 않으며, "
                "원시적 문화 상태는 더더욱 아니다. 그것은 특정한 정의관으로 이끌도록 "
                "특성화된 순수하게 가설적인 상황으로 이해된다."
            ),
            "explanation": (
                "원초적 입장은 롤스 정의론의 핵심적 방법론적 장치이다. "
                "홉스, 로크, 루소의 자연 상태가 (비록 가설적이지만) 역사적 상태를 암시하는 데 반해, "
                "롤스의 원초적 입장은 순수한 사고실험이다. "
                "이 장치의 목적은 정의 원칙의 선택에서 도덕적으로 자의적인(morally arbitrary) 요소를 "
                "배제하고, 공정한 조건에서의 합의를 도출하는 것이다."
            ),
            "argument": (
                "(1) 정의 원칙은 공정한 조건에서의 합의에 의해 정당화되어야 한다. "
                "(2) 현실의 협상은 권력, 재능, 사회적 지위 등의 차이로 불공정하다. "
                "(3) 이러한 도덕적으로 자의적인 요소를 배제하는 가설적 상황이 필요하다. "
                "(4) 원초적 입장은 당사자들이 합리적이고 상호 무관심(mutually disinterested)하며, "
                "무지의 베일 뒤에 놓인 상황을 설정한다. "
                "(5) 이 상황에서의 합의가 공정하다면, 그 결과인 정의 원칙도 공정하다. "
                "(6) 이것이 '공정으로서의 정의'라는 이름의 의미이다: 정의 원칙이 공정한 절차에서 선택된다."
            ),
            "counterpoint": (
                "마이클 샌델(Michael Sandel)은 '자유주의와 정의의 한계'(Liberalism and the Limits of Justice, 1982)에서 "
                "원초적 입장의 자아관이 지나치게 추상적이라고 비판했다. "
                "샌델에 따르면, 무지의 베일 뒤의 자아는 공동체적 유대, 문화적 정체성, "
                "구성적 목적(constitutive ends)을 박탈당한 '비연고적 자아(unencumbered self)'이며, "
                "이러한 자아에 의한 선택은 실제 인간의 도덕 경험을 반영하지 못한다."
            ),
            "context": (
                "원초적 입장은 칸트의 정언명령의 절차적 해석이다. "
                "칸트의 보편화 가능성 검사를 사회적 차원으로 확장한 것으로, "
                "롤스 자신이 이를 '칸트적 구성주의(Kantian constructivism)'라 불렀다."
            ),
            "keywords": ["원초적 입장", "가설적 장치", "사회계약", "공정한 조건"],
            "verified": False
        },
        # CLAIM-003: 무지의 베일
        {
            "id": "rawls-claim-003",
            "thinker_id": "rawls",
            "work_id": "rawls-theory-of-justice",
            "source_detail": "A Theory of Justice, §24",
            "claim": (
                "무지의 베일(veil of ignorance)은 원초적 입장에서 당사자들에게 부과되는 정보 제한이다. "
                "당사자들은 자신의 사회적 지위, 계급, 자연적 재능, 지능, 체력, "
                "선관(conception of the good), 인생 계획, 심리적 성향, "
                "세대, 사회의 경제 수준과 문명 단계를 알지 못한다. "
                "이를 통해 정의 원칙의 선택에서 모든 도덕적으로 자의적인 요소가 배제된다."
            ),
            "original_text": (
                "Among the essential features of this situation is that no one knows his place in society, "
                "his class position or social status, nor does any one know his fortune in the distribution "
                "of natural assets and abilities, his intelligence, strength, and the like."
            ),
            "original_text_ko": (
                "이 상황의 본질적 특징 중 하나는, 어느 누구도 사회에서 자기 자리, "
                "자기의 계급적 지위나 사회적 신분을 모른다는 것이며, "
                "자연적 자산과 능력의 배분에서 자기의 운, 지능, 체력 등도 모른다는 것이다."
            ),
            "explanation": (
                "무지의 베일은 원초적 입장을 공정하게 만드는 핵심 장치이다. "
                "당사자들이 자신의 특수한 조건을 모르기 때문에, "
                "특정 계층이나 집단에 유리한 원칙을 선택할 수 없다. "
                "이 무지는 정의 원칙의 보편성과 공정성을 보장하는 구조적 장치이다. "
                "무지의 베일은 도덕적으로 자의적인 요소(자연적 재능, 사회적 출발점)가 "
                "정의 원칙에 영향을 미치는 것을 방지한다."
            ),
            "argument": (
                "(1) 자연적 재능과 사회적 지위의 분배는 도덕적 관점에서 자의적(arbitrary)이다. "
                "(2) 도덕적으로 자의적인 요소가 정의 원칙의 선택에 영향을 미쳐서는 안 된다. "
                "(3) 이를 보장하는 방법은 당사자들이 이러한 정보를 갖지 못하게 하는 것이다. "
                "(4) 무지의 베일은 자연적 재능, 사회적 지위, 선관, 세대 등의 정보를 차단한다. "
                "(5) 그러나 당사자들은 사회의 일반적 사실(정치학, 경제학, 인간 심리 등)은 알고 있다. "
                "(6) 이 조건에서 합리적 당사자들은 자신이 어떤 위치에 놓이더라도 수용할 수 있는 원칙을 선택한다."
            ),
            "counterpoint": (
                "로널드 드워킨(Ronald Dworkin)은 'The Original Position'(1975)에서 "
                "무지의 베일이 일종의 대리적 장치에 불과하며, 진정한 정당화 근거는 "
                "평등한 관심과 존중(equal concern and respect)이라는 더 근본적인 원칙이라고 주장했다. "
                "데이비드 고티에(David Gauthier)는 '합의에 의한 도덕'(Morals by Agreement, 1986)에서 "
                "무지의 베일이 도덕적 직관을 장치에 투입한 것이므로 진정한 계약론이 아니라고 비판했다."
            ),
            "context": (
                "무지의 베일의 아이디어는 존 하사니(John Harsanyi)의 '공평한 관찰자(impartial observer)' 논증과 "
                "유사하지만, 하사니는 이로부터 공리주의를, 롤스는 차등원칙을 도출한다는 점에서 다르다."
            ),
            "keywords": ["무지의 베일", "정보 제한", "도덕적 자의성", "공정한 선택"],
            "verified": False
        },
        # CLAIM-004: 정의의 제1원칙 — 평등한 자유의 원칙
        {
            "id": "rawls-claim-004",
            "thinker_id": "rawls",
            "work_id": "rawls-theory-of-justice",
            "source_detail": "A Theory of Justice, §11, §13; Justice as Fairness: A Restatement, §13",
            "claim": (
                "정의의 제1원칙(평등한 자유의 원칙): "
                "각 개인은 모든 사람에게 적용되는 동일한 자유 체계와 양립 가능한 "
                "평등한 기본적 자유(equal basic liberties)의 완전히 적절한 체계에 대해 "
                "동등한 권리를 가진다. "
                "이 원칙은 제2원칙(기회균등과 차등원칙)에 사전적으로 우선한다."
            ),
            "original_text": (
                "Each person has an equal claim to a fully adequate scheme of equal basic rights and liberties, "
                "which scheme is compatible with the same scheme for all; and in this scheme the equal political "
                "liberties, and only those liberties, are to be guaranteed their fair value."
            ),
            "original_text_ko": (
                "각 개인은 평등한 기본적 권리와 자유의 완전히 적절한 체계에 대해 "
                "동등한 권리를 가지며, 이 체계는 모든 사람에게 동일한 체계와 양립 가능해야 한다. "
                "그리고 이 체계에서 평등한 정치적 자유, 오직 그 자유만이 "
                "그 공정한 가치를 보장받아야 한다."
            ),
            "explanation": (
                "제1원칙은 기본적 자유의 평등한 보장을 요구한다. "
                "기본적 자유에는 양심의 자유, 사상의 자유, 정치적 자유(투표권, 공직 취임권), "
                "집회와 결사의 자유, 신체의 자유와 온전성, 법의 지배에 의해 보장되는 권리 등이 포함된다. "
                "이 원칙이 제2원칙에 우선하므로, 경제적 이익을 위해 기본적 자유를 제한할 수 없다."
            ),
            "argument": (
                "(1) 원초적 입장의 당사자들은 자신의 선관(conception of the good)을 모른다. "
                "(2) 그러나 어떤 선관을 가지든 그것을 추구하기 위해 기본적 자유가 필요하다. "
                "(3) 기본적 자유는 모든 합리적 인생 계획에 필수적인 '기본적 선(primary goods)'이다. "
                "(4) 합리적 당사자들은 자유의 평등한 보장을 최우선으로 선택한다. "
                "(5) 이 원칙은 경제적 이익과의 교환이 불가능하다(사전적 우선성). "
                "(6) 이로써 공리주의와 달리 소수의 자유가 다수의 이익을 위해 희생되는 것을 방지한다."
            ),
            "counterpoint": (
                "아마르티아 센(Amartya Sen)은 '자유, 합리성과 사회적 선택'(Rationality and Freedom, 2002) 등에서 "
                "자유의 절대적 우선성에 의문을 제기하며, 극심한 빈곤 상태에서는 "
                "물질적 필요가 일부 자유에 우선할 수 있다고 주장했다. "
                "H.L.A. 하트(H.L.A. Hart)는 'Rawls on Liberty and Its Priority'(1973)에서 "
                "기본적 자유의 목록 선정과 자유 간의 충돌 해결 기준이 불충분하다고 비판했다."
            ),
            "context": (
                "롤스의 제1원칙은 자유주의 전통(로크, 밀)의 핵심을 계승하면서도, "
                "자유의 공정한 가치(fair value)를 강조함으로써 형식적 자유와 실질적 자유의 간극을 줄이려 했다."
            ),
            "keywords": ["평등한 자유의 원칙", "기본적 자유", "제1원칙", "사전적 우선성"],
            "verified": False
        },
        # CLAIM-005: 정의의 제2원칙a — 공정한 기회균등의 원칙
        {
            "id": "rawls-claim-005",
            "thinker_id": "rawls",
            "work_id": "rawls-theory-of-justice",
            "source_detail": "A Theory of Justice, §12, §14; Justice as Fairness: A Restatement, §13-14",
            "claim": (
                "공정한 기회균등의 원칙(fair equality of opportunity): "
                "사회적·경제적 불평등은 공정한 기회균등의 조건 아래 모든 사람에게 "
                "개방된 직위와 직책에 결부되어야 한다. "
                "이는 형식적 기회균등(careers open to talents)을 넘어, "
                "유사한 재능과 동기를 가진 사람들이 유사한 성공 전망을 가져야 한다는 것이다."
            ),
            "original_text": (
                "Social and economic inequalities are to be arranged so that they are "
                "attached to offices and positions open to all under conditions of fair equality of opportunity."
            ),
            "original_text_ko": (
                "사회적·경제적 불평등은 공정한 기회균등의 조건 아래 "
                "모든 사람에게 개방된 직위와 직책에 결부되도록 편성되어야 한다."
            ),
            "explanation": (
                "공정한 기회균등은 형식적 기회균등(법적 차별 금지)보다 강한 요구이다. "
                "사회적 출신 배경에 관계없이 동등한 재능과 의지를 가진 사람들은 "
                "동등한 성공 전망을 가져야 한다. "
                "이를 위해 교육 기회의 실질적 평등, 사회적 배경에 의한 차별 시정 등이 요구된다. "
                "공정한 기회균등의 원칙은 차등원칙에 우선한다."
            ),
            "argument": (
                "(1) 형식적 기회균등(법적 차별 금지)만으로는 사회적 출신의 영향을 제거할 수 없다. "
                "(2) 부유한 가정의 자녀와 빈곤한 가정의 자녀는 같은 재능이 있어도 전혀 다른 기회를 가진다. "
                "(3) 이러한 사회적 우연성은 도덕적으로 자의적이다. "
                "(4) 따라서 공정한 기회균등은 유사한 재능과 동기를 가진 사람들에게 "
                "사회적 배경과 무관하게 유사한 성공 전망을 보장할 것을 요구한다. "
                "(5) 이를 위해 교육, 의료, 사회적 지원의 실질적 평등이 필요하다."
            ),
            "counterpoint": (
                "로버트 노직(Robert Nozick)은 '아나키, 국가, 유토피아'(Anarchy, State, and Utopia, 1974)에서 "
                "기회균등을 위한 국가 개입은 개인의 자유와 재산권을 침해하며, "
                "사람들이 자발적으로 자녀에게 투자하는 것을 제한할 수 없다고 비판했다. "
                "리처드 아네슨(Richard Arneson)은 'Equality and Equal Opportunity for Welfare'(1989)에서 "
                "기회가 아니라 복지의 평등이 더 근본적인 평등 원리라고 주장했다."
            ),
            "context": (
                "공정한 기회균등 원칙은 능력주의(meritocracy)의 이상을 실질화하려는 시도이지만, "
                "롤스 자신도 자연적 재능의 분배가 자의적이라는 점에서 "
                "능력주의만으로는 불충분하다고 보았으며, 이것이 차등원칙의 필요성으로 이어진다."
            ),
            "keywords": ["공정한 기회균등", "형식적 기회균등", "사회적 우연성"],
            "verified": False
        },
        # CLAIM-006: 정의의 제2원칙b — 차등원칙
        {
            "id": "rawls-claim-006",
            "thinker_id": "rawls",
            "work_id": "rawls-theory-of-justice",
            "source_detail": "A Theory of Justice, §13, §17; Justice as Fairness: A Restatement, §18",
            "claim": (
                "차등원칙(difference principle): "
                "사회적·경제적 불평등은 사회의 최소수혜자(least advantaged members)에게 "
                "최대의 이익이 되도록 편성되어야 한다. "
                "불평등은 그것이 모든 사람, 특히 가장 불리한 위치에 있는 사람들에게 "
                "이익이 될 때에만 정당화된다."
            ),
            "original_text": (
                "Social and economic inequalities are to be arranged so that they are "
                "to the greatest benefit of the least-advantaged members of society."
            ),
            "original_text_ko": (
                "사회적·경제적 불평등은 사회의 최소수혜자에게 "
                "최대의 이익이 되도록 편성되어야 한다."
            ),
            "explanation": (
                "차등원칙은 롤스 정의론의 가장 독특하고 논쟁적인 원칙이다. "
                "완전한 평등보다 불평등이 허용되지만, 오직 그 불평등이 "
                "최소수혜자의 상황을 개선하는 경우에만 정당화된다. "
                "예를 들어, 의사에게 높은 보수를 지급하는 것은 그것이 "
                "의료 서비스의 질과 접근성을 높여 최소수혜자에게 이익이 되는 한에서 정당하다."
            ),
            "argument": (
                "(1) 자연적 재능의 분배는 도덕적으로 자의적이다 — 노력이나 도덕적 공로의 결과가 아니다. "
                "(2) 사회적 출신의 영향도 도덕적으로 자의적이다. "
                "(3) 따라서 재능과 사회적 출신에 기초한 불평등은 자체로는 정당하지 않다. "
                "(4) 그러나 불평등이 모든 사람에게 이익이 된다면, 특히 최소수혜자에게 이익이 된다면 허용될 수 있다. "
                "(5) 무지의 베일 뒤에서 합리적 당사자들은 최악의 경우를 대비하여(maximin) "
                "최소수혜자에게 최대 이익이 되는 원칙을 선택한다. "
                "(6) 차등원칙은 호혜성(reciprocity)의 원리를 표현한다: "
                "재능 있는 자의 이익은 덜 재능 있는 자에게도 이익이 되어야 한다."
            ),
            "counterpoint": (
                "로버트 노직(Robert Nozick)은 '아나키, 국가, 유토피아'(Anarchy, State, and Utopia, 1974)에서 "
                "차등원칙은 재능 있는 자의 자연적 자산을 공동 자산으로 취급하여 "
                "자기 소유권(self-ownership)을 침해한다고 비판했다. "
                "프리드리히 하이에크(Friedrich Hayek)는 '법, 입법, 자유'(Law, Legislation and Liberty, 1976)에서 "
                "'사회적 정의'라는 개념 자체가 자생적 질서(spontaneous order)에 적용될 수 없는 "
                "무의미한 개념이라고 비판했다."
            ),
            "context": (
                "차등원칙은 자유주의와 평등주의의 결합을 시도한다. "
                "전통적 자유주의의 시장 중심적 관점과 사회주의의 평등 중심적 관점 사이에서 "
                "불평등을 허용하되 그 수혜가 최소수혜자에게 돌아가도록 하는 '제3의 길'을 제시한다."
            ),
            "keywords": ["차등원칙", "최소수혜자", "호혜성", "분배 정의"],
            "verified": False
        },
        # CLAIM-007: 사전적 순서
        {
            "id": "rawls-claim-007",
            "thinker_id": "rawls",
            "work_id": "rawls-theory-of-justice",
            "source_detail": "A Theory of Justice, §8, §46",
            "claim": (
                "정의의 두 원칙 사이에는 사전적 순서(lexical order, serial order)가 존재한다. "
                "제1원칙(평등한 자유)이 제2원칙(기회균등+차등원칙)에 절대적으로 우선하고, "
                "제2원칙 내에서는 기회균등의 원칙이 차등원칙에 우선한다. "
                "이 순서에 따라 자유를 경제적 이익과 교환할 수 없으며, "
                "기회균등을 효율성과 교환할 수 없다."
            ),
            "original_text": (
                "These principles are to be arranged in a serial order with the first principle prior to the second. "
                "This ordering means that a departure from the institutions of equal liberty required by the first principle "
                "cannot be justified by, or compensated for, by greater social and economic advantages."
            ),
            "original_text_ko": (
                "이 원칙들은 제1원칙이 제2원칙에 우선하는 순차적 순서로 배열되어야 한다. "
                "이 순서는 제1원칙이 요구하는 평등한 자유의 제도로부터의 이탈이 "
                "더 큰 사회적·경제적 이점에 의해 정당화되거나 보상될 수 없음을 의미한다."
            ),
            "explanation": (
                "사전적 순서는 직관주의에 대한 롤스의 핵심적 대안이다. "
                "직관주의는 복수의 원칙을 인정하지만 그 사이의 우선순위를 제공하지 못한다. "
                "롤스는 명확한 우선순위를 설정함으로써 이 문제를 해결한다. "
                "'사전적'이라는 용어는 사전에서 단어를 배열하는 방식에서 비롯된다: "
                "첫 글자가 같을 때만 둘째 글자를 비교하듯, "
                "제1원칙이 충족된 후에만 제2원칙이 적용된다."
            ),
            "argument": (
                "(1) 직관주의는 복수의 원칙 사이의 우선순위를 제공하지 못한다(결정불능 문제). "
                "(2) 정의론은 원칙들 사이의 명확한 우선순위를 제공해야 한다. "
                "(3) 기본적 자유는 경제적 이익과 질적으로 다른 가치를 가진다. "
                "(4) 원초적 입장의 당사자들은 자유를 경제적 이익과 교환하지 않을 것이다. "
                "(5) 따라서 제1원칙은 제2원칙에 절대적으로 우선한다. "
                "(6) 마찬가지로 기회균등은 효율성이나 소득 극대화보다 우선한다."
            ),
            "counterpoint": (
                "아마르티아 센(Amartya Sen)은 'Equality of What?'(1979)에서 "
                "사전적 순서가 지나치게 경직적이라고 비판하며, "
                "역량(capabilities) 접근을 통해 자유와 복지의 관계를 더 유연하게 파악할 것을 제안했다. "
                "브라이언 배리(Brian Barry)는 'The Liberal Theory of Justice'(1973)에서 "
                "경제 발전의 초기 단계에서는 자유의 절대적 우선성이 비현실적일 수 있다고 지적했다."
            ),
            "context": (
                "롤스도 사전적 순서의 적용에는 일정한 물질적 조건이 충족되어야 함을 인정했다. "
                "극심한 빈곤 상태에서는 자유의 우선성이 온전히 적용되기 어렵다."
            ),
            "keywords": ["사전적 순서", "우선성 규칙", "직관주의 비판"],
            "verified": False
        },
        # CLAIM-008: 반성적 균형
        {
            "id": "rawls-claim-008",
            "thinker_id": "rawls",
            "work_id": "rawls-theory-of-justice",
            "source_detail": "A Theory of Justice, §4, §9",
            "claim": (
                "반성적 균형(reflective equilibrium)은 도덕적 정당화의 방법이다. "
                "우리의 숙고된 도덕 판단(considered moral judgments)과 "
                "도덕 원칙 사이를 왕복하며 양자를 조정하여 "
                "정합적 균형(coherent balance)에 도달하는 과정이다. "
                "원칙이 판단을 수정하기도 하고, 판단이 원칙을 수정하기도 한다."
            ),
            "original_text": (
                "By going back and forth, sometimes altering the conditions of the contractual circumstances, "
                "at others withdrawing our judgments and conforming them to principle, I assume that eventually "
                "we shall find a description of the initial situation that both expresses reasonable conditions "
                "and yields principles which match our considered judgments duly pruned and adjusted. "
                "This state of affairs I refer to as reflective equilibrium."
            ),
            "original_text_ko": (
                "계약 상황의 조건을 변경하기도 하고, 판단을 철회하여 원칙에 맞추기도 하면서 "
                "이리저리 왕복함으로써, 결국 합리적인 조건을 표현하면서 동시에 "
                "적절히 가지치기되고 조정된 우리의 숙고된 판단에 부합하는 원칙을 산출하는 "
                "초기 상황의 기술에 도달할 것이라고 가정한다. "
                "이 상태를 나는 반성적 균형이라 부른다."
            ),
            "explanation": (
                "반성적 균형은 롤스의 도덕 인식론이자 방법론이다. "
                "도덕 이론은 위로부터(원칙에서 판단으로)만 정당화되는 것도 아니고, "
                "아래로부터(판단에서 원칙으로)만 정당화되는 것도 아니다. "
                "양방향의 조정을 통해 원칙과 판단이 상호 지지하는 상태가 반성적 균형이다. "
                "넓은 반성적 균형(wide reflective equilibrium)은 모든 관련 이론과 배경 이론도 고려한다."
            ),
            "argument": (
                "(1) 우리에게는 특정한 도덕 판단에 대한 확신(숙고된 판단)이 있다. 예: 노예제는 부정의하다. "
                "(2) 그러나 개별 판단만으로는 체계적 도덕 이론이 되지 않는다. "
                "(3) 도덕 원칙은 이러한 판단들을 체계화하고 설명해야 한다. "
                "(4) 그러나 원칙이 일부 숙고된 판단과 충돌할 수 있다. "
                "(5) 이 경우 원칙을 수정하거나, 판단을 수정하거나, 양쪽 모두를 조정한다. "
                "(6) 이 왕복 과정을 통해 원칙과 판단이 상호 정합적인 균형에 도달한다. "
                "(7) 이 균형이 도덕적 정당화의 최선의 형태이다."
            ),
            "counterpoint": (
                "피터 싱어(Peter Singer)는 'Sidgwick and Reflective Equilibrium'(1974)에서 "
                "반성적 균형이 기존의 도덕적 편견을 정당화하는 보수적 방법론이 될 수 있다고 비판했다. "
                "숙고된 판단 자체가 사회적 편견을 반영할 수 있기 때문이다. "
                "R.M. 헤어(R.M. Hare)는 'Rawls' Theory of Justice'(1973)에서 "
                "반성적 균형은 주관적 직관의 집합에 불과하며 객관적 도덕 진리에 도달하지 못한다고 비판했다."
            ),
            "context": (
                "반성적 균형의 방법은 넬슨 굿맨(Nelson Goodman)의 귀납 논리학에서의 "
                "정합적 정당화 방법에서 영감을 받은 것이다. "
                "이 방법론은 이후 윤리학 전반에서 널리 채택되었다."
            ),
            "keywords": ["반성적 균형", "숙고된 판단", "도덕적 정당화", "정합론"],
            "verified": False
        },
        # CLAIM-009: 기본적 자유 목록
        {
            "id": "rawls-claim-009",
            "thinker_id": "rawls",
            "work_id": "rawls-theory-of-justice",
            "source_detail": "A Theory of Justice, §11; Political Liberalism, Lecture VIII",
            "claim": (
                "기본적 자유(basic liberties)는 제1원칙에 의해 보장되는 자유의 구체적 목록이다. "
                "양심의 자유와 사상의 자유, 결사의 자유, "
                "인신의 자유와 온전성(liberty and integrity of the person), "
                "정치적 자유(투표권과 공직 취임권), "
                "법의 지배(rule of law)에 의해 보장되는 권리와 자유를 포함한다."
            ),
            "original_text": (
                "The basic liberties are, roughly speaking, political liberty (the right to vote and to be eligible for public office) "
                "together with freedom of speech and assembly; liberty of conscience and freedom of thought; "
                "freedom of the person along with the right to hold (personal) property; "
                "and freedom from arbitrary arrest and seizure as defined by the concept of the rule of law."
            ),
            "original_text_ko": (
                "기본적 자유는 대략적으로 말해, 정치적 자유(투표권과 공직 취임 자격)와 "
                "언론 및 집회의 자유, 양심의 자유와 사상의 자유, "
                "신체의 자유 및 (개인적) 재산을 보유할 권리, "
                "법의 지배 개념에 의해 정의되는 자의적 체포와 압류로부터의 자유를 포함한다."
            ),
            "explanation": (
                "롤스의 기본적 자유 목록은 자유주의 전통의 핵심 자유를 체계화한 것이다. "
                "이 자유들은 두 가지 도덕적 능력(moral powers)의 발달과 행사를 위해 필수적이다: "
                "(1) 정의감의 능력(capacity for a sense of justice), "
                "(2) 선관의 능력(capacity for a conception of the good). "
                "주의할 점은 계약의 자유와 생산수단의 사적 소유권은 기본적 자유에 포함되지 않는다."
            ),
            "argument": (
                "(1) 기본적 자유의 목록은 두 가지 도덕적 능력의 발달과 행사에 필수적인 자유로 구성된다. "
                "(2) 정의감의 능력을 위해 정치적 자유, 사상의 자유, 집회의 자유가 필요하다. "
                "(3) 선관의 능력을 위해 양심의 자유, 결사의 자유, 신체의 자유가 필요하다. "
                "(4) 법의 지배는 이 모든 자유의 제도적 보장이다. "
                "(5) 생산수단의 사적 소유권은 기본적 자유에 포함되지 않는다 — "
                "이는 재산소유 민주주의와 자유주의적 사회주의 모두와 양립 가능하게 하기 위함이다."
            ),
            "counterpoint": (
                "H.L.A. 하트(H.L.A. Hart)는 'Rawls on Liberty and Its Priority'(1973)에서 "
                "기본적 자유 목록의 선정 기준이 불분명하며, "
                "서로 다른 기본적 자유들이 충돌할 때의 해결 기준이 불충분하다고 비판했다. "
                "롤스는 '정치적 자유주의'(1993)에서 이 비판을 수용하여 "
                "기본적 자유의 근거를 두 가지 도덕적 능력에 체계적으로 연결시켰다."
            ),
            "context": (
                "기본적 자유 목록에서 생산수단의 사적 소유권이 제외된 것은 "
                "롤스의 정의론이 자본주의와 사회주의 모두와 양립 가능함을 보여주는 핵심적 특징이다."
            ),
            "keywords": ["기본적 자유", "도덕적 능력", "정의감", "선관"],
            "verified": False
        },
        # CLAIM-010: 기본 구조
        {
            "id": "rawls-claim-010",
            "thinker_id": "rawls",
            "work_id": "rawls-theory-of-justice",
            "source_detail": "A Theory of Justice, §2; Political Liberalism, Lecture VII",
            "claim": (
                "정의의 제1주제(primary subject)는 사회의 기본 구조(basic structure)이다. "
                "기본 구조란 주요 사회 제도들이 기본적 권리와 의무를 배분하고 "
                "사회적 협동의 이익의 분배를 결정하는 방식이다. "
                "헌법, 경제 체제, 재산 제도, 가족 제도 등이 이에 해당한다."
            ),
            "original_text": (
                "For us the primary subject of justice is the basic structure of society, "
                "or more exactly, the way in which the major social institutions distribute fundamental rights "
                "and duties and determine the division of advantages from social cooperation."
            ),
            "original_text_ko": (
                "우리에게 정의의 제1주제는 사회의 기본 구조이며, "
                "더 정확히 말하면 주요 사회 제도들이 기본적 권리와 의무를 배분하고 "
                "사회적 협동의 이점의 분배를 결정하는 방식이다."
            ),
            "explanation": (
                "롤스가 정의의 주제를 기본 구조로 한정한 것은 중요한 이론적 선택이다. "
                "개인의 행위나 개별 거래가 아니라, 그러한 행위와 거래가 이루어지는 "
                "제도적 틀(institutional framework)이 정의의 대상이다. "
                "기본 구조가 중요한 이유는 그것이 사람들의 삶의 전망에 "
                "깊고 처음부터(from the start) 영향을 미치기 때문이다."
            ),
            "argument": (
                "(1) 사회의 기본 구조는 개인의 삶의 전망에 깊이 영향을 미친다. "
                "(2) 어떤 사회에 태어나느냐, 어떤 제도 아래에서 자라느냐에 따라 기회가 결정된다. "
                "(3) 이러한 영향은 '처음부터(from the start)' 작용하여 누적적이다. "
                "(4) 개별 거래의 공정성은 배경적 제도(background institutions)의 공정성을 전제한다. "
                "(5) 따라서 정의의 제1주제는 개별 거래가 아니라 기본 구조이다. "
                "(6) 기본 구조에 적용되는 원칙은 개인 행위에 적용되는 원칙과 다를 수 있다."
            ),
            "counterpoint": (
                "G.A. 코헨(G.A. Cohen)은 'If You're an Egalitarian, How Come You're So Rich?'(2000)와 "
                "'Rescuing Justice and Equality'(2008)에서 정의 원칙은 기본 구조뿐 아니라 "
                "개인의 행위와 선택에도 적용되어야 한다고 비판했다. "
                "코헨에 따르면, 정의로운 사회는 정의로운 제도뿐 아니라 "
                "정의로운 에토스(ethos)를 가진 시민들을 필요로 한다. "
                "노직은 기본 구조 개념 자체가 불분명하다고 비판했다."
            ),
            "context": (
                "기본 구조에 대한 초점은 롤스의 정의론이 이상적 이론(ideal theory)임을 보여준다. "
                "완전히 정의로운 기본 구조가 어떤 것인지를 먼저 규명하고, "
                "그로부터 비이상적 상황에 대한 지침을 도출하는 접근이다."
            ),
            "keywords": ["기본 구조", "주요 사회 제도", "배경적 정의"],
            "verified": False
        },
        # CLAIM-011: 순수 절차적 정의
        {
            "id": "rawls-claim-011",
            "thinker_id": "rawls",
            "work_id": "rawls-theory-of-justice",
            "source_detail": "A Theory of Justice, §14",
            "claim": (
                "차등원칙은 순수 절차적 정의(pure procedural justice)의 사례이다. "
                "분배의 정의로움을 판단하는 결과 독립적 기준(independent criterion)이 없으며, "
                "공정한 절차를 따르면 그 결과가 무엇이든 정의롭다. "
                "이는 완전한 절차적 정의(케이크 자르기)나 불완전한 절차적 정의(재판)와 구별된다."
            ),
            "original_text": (
                "The idea of pure procedural justice is best understood by a comparison with perfect and "
                "imperfect procedural justice. ... In pure procedural justice there is no independent criterion "
                "for the right result: instead there is a correct or fair procedure such that the outcome is "
                "likewise correct or fair, whatever it is, provided that the procedure has been properly followed."
            ),
            "original_text_ko": (
                "순수 절차적 정의의 관념은 완전한 절차적 정의 및 불완전한 절차적 정의와의 비교를 통해 "
                "가장 잘 이해된다. ... 순수 절차적 정의에서는 올바른 결과에 대한 독립적 기준이 없다. "
                "대신 올바른 또는 공정한 절차가 있어서, 그 절차가 적절히 따라진다면 "
                "결과가 무엇이든 그것 역시 올바르거나 공정하다."
            ),
            "explanation": (
                "순수 절차적 정의는 분배 정의에 대한 롤스의 방법론적 핵심이다. "
                "분배의 결과를 사전에 특정하는 것이 아니라, "
                "정의로운 기본 구조라는 절차가 보장되면 그로부터 나오는 분배는 정의롭다. "
                "이는 도박의 비유로 설명된다: 공정한 규칙 아래의 도박 결과는 그 자체로 공정하다."
            ),
            "argument": (
                "(1) 분배적 정의에는 세 유형이 있다: 완전한, 불완전한, 순수 절차적 정의. "
                "(2) 완전한 절차적 정의(예: 케이크 나누기)는 독립적 기준과 이를 실현하는 절차가 있다. "
                "(3) 불완전한 절차적 정의(예: 재판)는 독립적 기준은 있으나 이를 보장하는 절차는 없다. "
                "(4) 순수 절차적 정의는 독립적 기준 없이, 공정한 절차의 결과가 곧 정의롭다. "
                "(5) 사회적 분배에서는 사전에 '올바른 분배'를 특정할 수 없다. "
                "(6) 따라서 정의로운 기본 구조(공정한 절차)를 수립하고, "
                "그 결과로 나오는 분배를 정의로운 것으로 받아들인다."
            ),
            "counterpoint": (
                "로버트 노직(Robert Nozick)은 '아나키, 국가, 유토피아'(1974)에서 "
                "자신의 자격이론(entitlement theory)이야말로 진정한 절차적 정의라고 주장하며, "
                "롤스의 차등원칙은 결국 분배 패턴을 특정하는 결과주의적(patterned) 원칙이라고 비판했다. "
                "코헨(G.A. Cohen)은 순수 절차적 정의가 결과의 불의를 은폐할 수 있다고 우려했다."
            ),
            "context": (
                "순수 절차적 정의 개념은 법학, 정치학, 경제학에서 "
                "제도 설계(institutional design)의 중요성을 강조하는 데 널리 영향을 미쳤다."
            ),
            "keywords": ["순수 절차적 정의", "공정한 절차", "결과 독립적"],
            "verified": False
        },
        # CLAIM-012: 중첩적 합의
        {
            "id": "rawls-claim-012",
            "thinker_id": "rawls",
            "work_id": "rawls-political-liberalism",
            "source_detail": "Political Liberalism, Lecture IV",
            "claim": (
                "중첩적 합의(overlapping consensus)는 서로 다른 포괄적 교설(comprehensive doctrines)을 가진 "
                "시민들이 각자의 교설 내부의 이유로 동일한 정치적 정의관에 동의하는 상태이다. "
                "이는 단순한 타협(modus vivendi)이 아니라, "
                "각 교설의 도덕적 이유에 기초한 진정한 도덕적 합의이다."
            ),
            "original_text": (
                "In such a consensus, the reasonable doctrines endorse the political conception, each from its own point of view. "
                "Social unity is based on a consensus on the political conception; and stability is possible "
                "when the doctrines making up the consensus are affirmed by society's politically active citizens."
            ),
            "original_text_ko": (
                "그러한 합의에서 합당한 교설들은 각자의 관점에서 정치적 정의관을 지지한다. "
                "사회적 통일성은 정치적 정의관에 대한 합의에 기초하며, "
                "합의를 구성하는 교설들이 사회의 정치적으로 활동적인 시민들에 의해 "
                "긍정될 때 안정성이 가능하다."
            ),
            "explanation": (
                "중첩적 합의는 정치적 자유주의의 핵심 개념이다. "
                "근대 민주 사회에서는 합당한 다원주의의 사실(fact of reasonable pluralism)로 인해 "
                "모든 시민이 하나의 포괄적 교설에 동의하는 것은 불가능하다. "
                "그러나 서로 다른 종교적, 철학적, 도덕적 교설을 가진 시민들이 "
                "각자의 교설 내부의 이유로 동일한 정치적 정의관을 지지할 수 있다면, "
                "안정적이고 정당한 정치 질서가 가능하다."
            ),
            "argument": (
                "(1) 합당한 다원주의: 근대 민주 사회에서 합당한 시민들은 서로 다른 포괄적 교설을 가진다. "
                "(2) 하나의 포괄적 교설을 강제하는 것은 부당하고 불가능하다(억압의 사실). "
                "(3) 그러나 정치적 안정과 정당성을 위해 정의에 대한 공유된 기반이 필요하다. "
                "(4) 정치적 정의관은 포괄적 교설에서 독립적인(freestanding) 것이어야 한다. "
                "(5) 서로 다른 합당한 교설들이 각자의 내부적 이유로 이 정치적 정의관을 지지할 수 있다. "
                "(6) 이러한 중첩적 합의는 단순한 이해관계의 타협(modus vivendi)이 아니라 도덕적 합의이다. "
                "(7) 따라서 정치적 자유주의는 합당한 다원주의와 양립 가능한 안정적 정의 체계를 제공한다."
            ),
            "counterpoint": (
                "위르겐 하버마스(Jürgen Habermas)는 'Reconciliation through the Public Use of Reason'(1995)에서 "
                "중첩적 합의가 진정한 합리적 합의가 아니라 전략적 타협에 가까우며, "
                "담론 윤리학(discourse ethics)에 의한 합리적 합의가 더 근본적이라고 비판했다. "
                "조지프 라즈(Joseph Raz)는 'Facing Diversity'(1990)에서 "
                "정치적 자유주의의 중립성이 자기모순적이며, 자유주의도 하나의 포괄적 교설이라고 주장했다."
            ),
            "context": (
                "중첩적 합의 개념은 롤스가 1985년 논문 'Justice as Fairness: Political not Metaphysical'에서 "
                "처음 체계적으로 전개하였으며, '정치적 자유주의'(1993)에서 완성되었다."
            ),
            "keywords": ["중첩적 합의", "포괄적 교설", "정치적 정의관", "안정성"],
            "verified": False
        },
        # CLAIM-013: 공적 이성
        {
            "id": "rawls-claim-013",
            "thinker_id": "rawls",
            "work_id": "rawls-political-liberalism",
            "source_detail": "Political Liberalism, Lecture VI; 'The Idea of Public Reason Revisited' (1997)",
            "claim": (
                "공적 이성(public reason)은 시민들이 근본적인 정치 문제에 대해 "
                "공적으로 논의할 때 사용해야 하는 이성의 형태이다. "
                "시민들은 자신의 포괄적 교설(종교적, 철학적 확신)이 아니라, "
                "모든 합당한 시민이 수용할 수 있는 정치적 가치와 원칙에 호소해야 한다."
            ),
            "original_text": (
                "The idea of public reason specifies at the deepest level the basic moral and political values "
                "that are to determine a constitutional democratic government's relation to its citizens "
                "and their relation to one another."
            ),
            "original_text_ko": (
                "공적 이성의 관념은 가장 깊은 수준에서, "
                "입헌 민주 정부와 시민 사이의 관계 및 시민 상호 간의 관계를 결정할 "
                "기본적인 도덕적·정치적 가치를 규정한다."
            ),
            "explanation": (
                "공적 이성은 정치적 자유주의의 규범적 핵심이다. "
                "다원주의 사회에서 근본적 정치 문제(헌법적 본질, 기본적 정의의 문제)를 논의할 때, "
                "시민들은 모든 합당한 시민이 받아들일 수 있는 이유를 제시해야 한다는 시민적 의무이다. "
                "이는 사적 영역에서의 종교적 논의나 시민사회의 자유로운 토론을 제한하는 것이 아니라, "
                "공적 정치 포럼에서의 정당화 방식에 관한 것이다."
            ),
            "argument": (
                "(1) 합당한 다원주의 사회에서 시민들은 서로 다른 포괄적 교설을 가진다. "
                "(2) 근본적 정치 문제에서 특정 포괄적 교설에 기반한 논증은 "
                "다른 교설을 가진 시민들에게 정당한 이유가 되지 못한다. "
                "(3) 정치권력의 행사는 모든 시민에게 정당화될 수 있어야 한다(자유주의적 정당성 원리). "
                "(4) 따라서 근본적 정치 문제에서 시민들은 정치적 가치에 호소해야 한다. "
                "(5) 이것이 시민성의 의무(duty of civility)이다. "
                "(6) 공적 이성의 내용은 정치적 정의관의 가치와 탐구의 지침으로 구성된다."
            ),
            "counterpoint": (
                "니콜라스 월터스토프(Nicholas Wolterstorff)는 'The Role of Religion in Decision and Discussion of Political Issues'(1997)에서 "
                "공적 이성의 요구가 종교적 시민들에게 부당한 부담을 지운다고 비판했다. "
                "종교적 확신은 많은 시민의 도덕적 추론의 핵심이며, "
                "이를 공적 영역에서 배제하는 것은 불공정하다는 것이다. "
                "하버마스(Jürgen Habermas)는 'Religion in the Public Sphere'(2006)에서 "
                "종교적 이유를 공적 이성으로 '번역'할 것을 제안하며 절충적 입장을 취했다."
            ),
            "context": (
                "공적 이성 논쟁은 낙태, 안락사, 동성 결혼 등 "
                "종교적 확신이 정치적 입장에 영향을 미치는 현대의 주요 논쟁과 직결된다."
            ),
            "keywords": ["공적 이성", "시민성의 의무", "정당성 원리", "포괄적 교설"],
            "verified": False
        },
        # CLAIM-014: 합당한 다원주의의 사실
        {
            "id": "rawls-claim-014",
            "thinker_id": "rawls",
            "work_id": "rawls-political-liberalism",
            "source_detail": "Political Liberalism, Lecture I, §6; Lecture II",
            "claim": (
                "합당한 다원주의의 사실(fact of reasonable pluralism)이란, "
                "자유로운 제도 아래에서 합당한(reasonable) 시민들이 "
                "서로 양립 불가능한(incompatible) 포괄적 교설을 가지게 되는 것은 "
                "자유로운 이성의 정상적 행사의 결과라는 것이다. "
                "이는 무지나 비합리성의 결과가 아니라, '판단의 짐(burdens of judgment)'에서 비롯된다."
            ),
            "original_text": (
                "The diversity of reasonable comprehensive religious, philosophical, and moral doctrines found in modern "
                "democratic societies is not a mere historical condition that may soon pass away; it is a permanent feature "
                "of the public culture of democracy."
            ),
            "original_text_ko": (
                "현대 민주 사회에서 발견되는 합당한 포괄적 종교, 철학, 도덕 교설의 다양성은 "
                "곧 사라질 수 있는 단순한 역사적 조건이 아니다. "
                "그것은 민주주의의 공적 문화의 영구적 특징이다."
            ),
            "explanation": (
                "합당한 다원주의의 사실은 정치적 자유주의로의 전환의 출발점이다. "
                "정의론에서 롤스는 질서정연한 사회의 모든 시민이 "
                "정의론을 포괄적 교설로서 받아들일 것을 가정했다. "
                "그러나 이것은 비현실적이다. 자유로운 제도 아래에서 합당한 사람들이 "
                "서로 다른 종교, 철학, 도덕 교설을 가지는 것은 불가피하다. "
                "이 불가피성은 '판단의 짐' — 증거의 복잡성, 가중치의 차이, "
                "개념의 모호성, 경험의 다양성 등 — 에서 비롯된다."
            ),
            "argument": (
                "(1) 자유로운 제도 아래에서 시민들은 이성을 자유롭게 행사한다. "
                "(2) 이성의 자유로운 행사는 불가피하게 서로 다른 결론을 산출한다(판단의 짐). "
                "(3) 이 다양성은 무지나 비합리성의 결과가 아니라 합당한 불일치(reasonable disagreement)이다. "
                "(4) 따라서 합당한 다원주의는 민주주의의 영구적 특징이다. "
                "(5) 정치 이론은 이 사실을 출발점으로 삼아야 한다. "
                "(6) 하나의 포괄적 교설에 기초한 정치 질서는 억압을 필요로 하며 정당하지 않다. "
                "(7) 따라서 정치적 정의관은 포괄적 교설로부터 독립적(freestanding)이어야 한다."
            ),
            "counterpoint": (
                "조지프 라즈(Joseph Raz)는 'The Morality of Freedom'(1986)에서 "
                "자유주의 자체가 좋은 삶에 대한 실질적 관점(자율성의 가치)을 전제하며, "
                "이러한 완전주의적(perfectionist) 자유주의가 정치적 자유주의보다 "
                "더 정직하고 효과적이라고 주장했다. "
                "라즈에 따르면 합당한 다원주의를 인정하면서도 "
                "자율성(autonomy)의 가치를 국가가 촉진할 수 있다."
            ),
            "context": (
                "합당한 다원주의의 사실 인정은 롤스 사상의 '정치적 전환(political turn)'의 핵심이며, "
                "정의론(1971)과 정치적 자유주의(1993) 사이의 가장 중요한 변화를 설명한다."
            ),
            "keywords": ["합당한 다원주의", "판단의 짐", "합당한 불일치", "포괄적 교설"],
            "verified": False
        },
        # CLAIM-015: 최소극대화 규칙
        {
            "id": "rawls-claim-015",
            "thinker_id": "rawls",
            "work_id": "rawls-theory-of-justice",
            "source_detail": "A Theory of Justice, §26",
            "claim": (
                "최소극대화 규칙(maximin rule)은 불확실성 아래의 합리적 선택 규칙으로, "
                "각 선택지의 최악의 결과를 비교하여 최악이 가장 나은 선택지를 택하는 것이다. "
                "원초적 입장의 당사자들은 무지의 베일 아래에서 이 규칙을 따라 "
                "차등원칙(최소수혜자에게 최대 이익)을 선택한다."
            ),
            "original_text": (
                "The maximin rule tells us to rank alternatives by their worst possible outcomes: "
                "we are to adopt the alternative the worst outcome of which is superior to the worst outcomes "
                "of the others."
            ),
            "original_text_ko": (
                "최소극대화 규칙은 선택지들을 그 최악의 가능한 결과에 의해 서열화하라고 말한다. "
                "우리는 최악의 결과가 다른 선택지들의 최악의 결과보다 우월한 선택지를 채택해야 한다."
            ),
            "explanation": (
                "최소극대화는 원초적 입장에서 차등원칙을 선택하는 논증의 핵심이다. "
                "무지의 베일 뒤에서 당사자들은 자신이 사회의 어떤 위치에 놓일지 모른다. "
                "이 상황에서 합리적 선택은 최악의 경우를 대비하는 것이다. "
                "공리주의의 기대효용 극대화와 대비되며, "
                "롤스는 세 가지 조건 아래에서 최소극대화가 합리적이라고 주장한다: "
                "(1) 확률 추정의 근거가 없을 때, (2) 최소한의 수용 가능한 수준이 보장되어야 할 때, "
                "(3) 최악의 결과가 심각하게 나쁠 때."
            ),
            "argument": (
                "(1) 원초적 입장의 당사자들은 확률 분포를 알지 못한다(무지의 베일). "
                "(2) 기대효용 극대화(평균 공리주의)는 확률 추정을 필요로 하므로 적용 불가능하다. "
                "(3) 정의 원칙의 선택은 되돌릴 수 없는(irrevocable) 선택이다. "
                "(4) 공리주의를 선택하면 최악의 경우 기본적 자유를 잃을 수 있다. "
                "(5) 이 세 조건(확률 정보 부재, 최소 수용 수준의 중요성, 최악의 결과의 심각성) 아래에서 "
                "합리적 당사자들은 최소극대화 전략을 택한다. "
                "(6) 최소극대화에 따라 차등원칙이 선택된다: 최소수혜자의 상황이 최대화된다."
            ),
            "counterpoint": (
                "존 C. 하사니(John C. Harsanyi)는 'Can the Maximin Principle Serve as a Basis for Morality?'(1975)에서 "
                "원초적 입장의 합리적 당사자들은 최소극대화가 아니라 기대효용 극대화를 선택할 것이며, "
                "이는 평균 공리주의로 귀결된다고 반박했다. "
                "하사니에 따르면, 최소극대화는 극단적으로 위험회피적인 비합리적 전략이며, "
                "불확실성 아래에서도 동등 확률의 원칙(principle of equal probability)에 따라 "
                "기대효용을 계산할 수 있다."
            ),
            "context": (
                "최소극대화 논증은 롤스 정의론에서 가장 논쟁적인 부분 중 하나이다. "
                "후기 저작에서 롤스는 최소극대화에 대한 의존을 줄이고, "
                "정의 원칙의 정당화에서 호혜성(reciprocity)과 시민적 우정(civic friendship)을 더 강조했다."
            ),
            "keywords": ["최소극대화", "불확실성", "합리적 선택", "위험 회피"],
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """롤스 키워드 데이터 입력."""
    keywords = [
        {
            "id": "rawls-kw-001",
            "thinker_id": "rawls",
            "term": "공정으로서의 정의 (Justice as Fairness)",
            "term_original": "justice as fairness",
            "definition": (
                "롤스 정의론의 핵심 관념. 정의 원칙은 자유롭고 평등한 사람들이 "
                "공정한 조건(원초적 입장) 아래에서 합의할 원칙이라는 구상이다. "
                "사회계약론의 전통을 가장 추상적인 수준으로 끌어올린 것으로, "
                "공리주의와 직관주의에 대한 체계적 대안이다."
            ),
            "related_claims": ["rawls-claim-001", "rawls-claim-002"],
            "source": "A Theory of Justice, §1-4"
        },
        {
            "id": "rawls-kw-002",
            "thinker_id": "rawls",
            "term": "원초적 입장 (Original Position)",
            "term_original": "original position",
            "definition": (
                "정의 원칙 선택을 위한 가상적 초기 상황. "
                "전통적 사회계약론의 자연 상태에 대응하되, 순수한 가설적 장치이다. "
                "합리적이고 상호 무관심한 당사자들이 무지의 베일 뒤에서 "
                "사회의 기본 구조를 규율할 원칙을 선택한다."
            ),
            "related_claims": ["rawls-claim-002", "rawls-claim-003"],
            "source": "A Theory of Justice, §4, §20-25"
        },
        {
            "id": "rawls-kw-003",
            "thinker_id": "rawls",
            "term": "무지의 베일 (Veil of Ignorance)",
            "term_original": "veil of ignorance",
            "definition": (
                "원초적 입장에서 당사자들에게 부과되는 정보 제한. "
                "사회적 지위, 자연적 재능, 선관, 세대 등의 정보를 차단하여 "
                "정의 원칙의 선택에서 도덕적으로 자의적인 요소를 배제한다. "
                "공정한 선택의 조건을 구조적으로 보장하는 핵심 장치이다."
            ),
            "related_claims": ["rawls-claim-003"],
            "source": "A Theory of Justice, §24"
        },
        {
            "id": "rawls-kw-004",
            "thinker_id": "rawls",
            "term": "차등원칙 (Difference Principle)",
            "term_original": "difference principle",
            "definition": (
                "정의의 제2원칙의 일부로, 사회적·경제적 불평등은 "
                "사회의 최소수혜자에게 최대의 이익이 되도록 편성되어야 한다는 원칙. "
                "호혜성(reciprocity)의 원리를 표현하며, "
                "완전한 평등보다 불평등이 모든 이에게 이익이 되는 경우만 허용한다."
            ),
            "related_claims": ["rawls-claim-006", "rawls-claim-015"],
            "source": "A Theory of Justice, §13, §17"
        },
        {
            "id": "rawls-kw-005",
            "thinker_id": "rawls",
            "term": "기본적 자유 (Basic Liberties)",
            "term_original": "basic liberties",
            "definition": (
                "제1원칙에 의해 보장되는 자유의 목록. "
                "양심의 자유, 사상의 자유, 정치적 자유(투표권, 공직 취임권), "
                "결사의 자유, 신체의 자유와 온전성, 법의 지배에 의한 보장을 포함한다. "
                "두 가지 도덕적 능력(정의감, 선관)의 발달과 행사에 필수적이다."
            ),
            "related_claims": ["rawls-claim-004", "rawls-claim-009"],
            "source": "A Theory of Justice, §11; Political Liberalism, Lecture VIII"
        },
        {
            "id": "rawls-kw-006",
            "thinker_id": "rawls",
            "term": "사전적 순서 (Lexical Order)",
            "term_original": "lexical order / serial order",
            "definition": (
                "정의 원칙들 사이의 절대적 우선순위 체계. "
                "제1원칙(평등한 자유)이 제2원칙에 절대적으로 우선하고, "
                "제2원칙 내에서는 기회균등이 차등원칙에 우선한다. "
                "자유를 경제적 이익과 교환할 수 없다는 것이 핵심이다."
            ),
            "related_claims": ["rawls-claim-007"],
            "source": "A Theory of Justice, §8, §46"
        },
        {
            "id": "rawls-kw-007",
            "thinker_id": "rawls",
            "term": "반성적 균형 (Reflective Equilibrium)",
            "term_original": "reflective equilibrium",
            "definition": (
                "도덕적 정당화의 방법론. 숙고된 도덕 판단과 도덕 원칙 사이를 왕복하며 "
                "양자를 조정하여 정합적 균형에 도달하는 과정이다. "
                "넬슨 굿맨의 귀납 논리학에서 영감을 받았으며, "
                "이후 윤리학 전반에서 널리 채택된 방법론이다."
            ),
            "related_claims": ["rawls-claim-008"],
            "source": "A Theory of Justice, §4, §9"
        },
        {
            "id": "rawls-kw-008",
            "thinker_id": "rawls",
            "term": "중첩적 합의 (Overlapping Consensus)",
            "term_original": "overlapping consensus",
            "definition": (
                "서로 다른 포괄적 교설을 가진 시민들이 각자의 교설 내부의 이유로 "
                "동일한 정치적 정의관에 동의하는 상태. "
                "단순한 타협(modus vivendi)이 아니라 진정한 도덕적 합의이며, "
                "정치적 자유주의의 핵심 개념이다."
            ),
            "related_claims": ["rawls-claim-012"],
            "source": "Political Liberalism, Lecture IV"
        },
        {
            "id": "rawls-kw-009",
            "thinker_id": "rawls",
            "term": "공적 이성 (Public Reason)",
            "term_original": "public reason",
            "definition": (
                "근본적 정치 문제에 대해 시민들이 공적으로 논의할 때 사용해야 하는 이성의 형태. "
                "포괄적 교설이 아니라 모든 합당한 시민이 수용할 수 있는 "
                "정치적 가치와 원칙에 호소해야 한다는 시민성의 의무를 표현한다."
            ),
            "related_claims": ["rawls-claim-013"],
            "source": "Political Liberalism, Lecture VI; 'The Idea of Public Reason Revisited' (1997)"
        },
        {
            "id": "rawls-kw-010",
            "thinker_id": "rawls",
            "term": "기본 구조 (Basic Structure)",
            "term_original": "basic structure",
            "definition": (
                "정의의 제1주제. 주요 사회 제도들이 기본적 권리와 의무를 배분하고 "
                "사회적 협동의 이익의 분배를 결정하는 방식이다. "
                "헌법, 경제 체제, 재산 제도, 가족 제도 등이 해당한다. "
                "개별 거래가 아니라 제도적 틀이 정의의 대상이다."
            ),
            "related_claims": ["rawls-claim-010"],
            "source": "A Theory of Justice, §2; Political Liberalism, Lecture VII"
        },
        {
            "id": "rawls-kw-011",
            "thinker_id": "rawls",
            "term": "최소극대화 (Maximin Rule)",
            "term_original": "maximin rule",
            "definition": (
                "불확실성 아래의 합리적 선택 규칙. 각 선택지의 최악의 결과를 비교하여 "
                "최악이 가장 나은 선택지를 택한다. "
                "원초적 입장에서 차등원칙을 선택하는 논증의 핵심이며, "
                "기대효용 극대화(공리주의)에 대한 대안이다."
            ),
            "related_claims": ["rawls-claim-015"],
            "source": "A Theory of Justice, §26"
        },
        {
            "id": "rawls-kw-012",
            "thinker_id": "rawls",
            "term": "합당한 다원주의 (Reasonable Pluralism)",
            "term_original": "reasonable pluralism / fact of reasonable pluralism",
            "definition": (
                "자유로운 제도 아래에서 합당한 시민들이 서로 양립 불가능한 "
                "포괄적 교설을 가지게 되는 것은 자유로운 이성의 정상적 행사의 결과라는 사실. "
                "무지나 비합리성의 결과가 아니라 '판단의 짐(burdens of judgment)'에서 비롯된다. "
                "정치적 자유주의의 출발점이다."
            ),
            "related_claims": ["rawls-claim-014"],
            "source": "Political Liberalism, Lecture I, §6; Lecture II"
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """롤스 관계 데이터 입력."""
    # 먼저 기존 관계 확인
    existing_relations = set()
    try:
        result = client.search(
            index=INDEX_RELATIONS,
            query={"bool": {"should": [
                {"term": {"from_thinker": "rawls"}},
                {"term": {"to_thinker": "rawls"}}
            ]}},
            _source=["id"],
            size=20
        )
        for hit in result['hits']['hits']:
            existing_relations.add(hit['_source']['id'])
        print(f"[relations] 기존 rawls 관련 관계: {existing_relations}")
    except Exception:
        pass

    relations = [
        {
            "id": "relation-kant-rawls",
            "from_thinker": "kant",
            "to_thinker": "rawls",
            "type": "influenced",
            "description": (
                "칸트(Immanuel Kant, 1724~1804)의 도덕철학은 롤스에게 가장 근본적인 영향을 미쳤다. "
                "롤스는 자신의 정의론을 '칸트적 구성주의(Kantian constructivism)'라 불렀다. "
                "원초적 입장은 칸트의 정언명령의 절차적 해석이며, "
                "자유롭고 평등한 도덕적 인격(moral person)이라는 관념은 "
                "칸트의 이성적 존재자(rational being) 개념에서 비롯된다. "
                "정의 원칙의 보편성과 자율성(autonomy)에 대한 강조 역시 칸트적이다."
            ),
            "strength": "강함",
            "period": "20세기"
        },
        # relation-hobbes-rawls는 이미 존재하므로 제외
        {
            "id": "relation-rawls-nozick",
            "from_thinker": "rawls",
            "to_thinker": "nozick",
            "type": "influenced",
            "description": (
                "로버트 노직(Robert Nozick, 1938~2002)은 '아나키, 국가, 유토피아'(Anarchy, State, and Utopia, 1974)에서 "
                "롤스의 정의론에 대한 가장 강력한 자유지상주의적(libertarian) 비판을 전개했다. "
                "노직은 차등원칙이 재능 있는 자의 자기 소유권(self-ownership)을 침해하며, "
                "정의는 분배 패턴이 아니라 자격(entitlement)과 정당한 이전 과정에 의해 결정된다고 주장했다. "
                "롤스와 노직의 논쟁은 20세기 정치철학의 가장 중요한 논쟁 중 하나이다."
            ),
            "strength": "강함",
            "period": "20세기"
        },
        {
            "id": "relation-rawls-sandel",
            "from_thinker": "rawls",
            "to_thinker": "sandel",
            "type": "influenced",
            "description": (
                "마이클 샌델(Michael Sandel, 1953~)은 '자유주의와 정의의 한계'(Liberalism and the Limits of Justice, 1982)에서 "
                "롤스의 자아관이 '비연고적 자아(unencumbered self)'에 기초한다고 비판했다. "
                "샌델에 따르면, 무지의 베일 뒤의 자아는 공동체적 유대와 구성적 목적을 박탈당한 "
                "추상적 존재이며, 이러한 자아관은 인간의 도덕 경험을 왜곡한다. "
                "이 비판은 공동체주의(communitarianism) 대 자유주의 논쟁의 출발점이 되었다."
            ),
            "strength": "강함",
            "period": "20세기"
        },
        {
            "id": "relation-rawls-habermas",
            "from_thinker": "rawls",
            "to_thinker": "habermas",
            "type": "influenced",
            "description": (
                "위르겐 하버마스(Jürgen Habermas, 1929~)는 롤스와 정치적 자유주의의 핵심 문제에 대해 "
                "생산적인 논쟁을 전개했다. 하버마스는 'Reconciliation through the Public Use of Reason'(1995)에서 "
                "롤스의 중첩적 합의가 진정한 합리적 합의가 아니라 전략적 타협에 가깝다고 비판하며, "
                "담론 윤리학(discourse ethics)에 기초한 합리적 합의를 대안으로 제시했다. "
                "롤스는 'Reply to Habermas'(1995)에서 이에 응답하며, "
                "두 사상가는 자유주의적 민주주의의 정당화에 대한 심층적 대화를 나누었다."
            ),
            "strength": "보통",
            "period": "20세기"
        },
        {
            "id": "relation-rousseau-rawls",
            "from_thinker": "rousseau",
            "to_thinker": "rawls",
            "type": "influenced",
            "description": (
                "루소(Jean-Jacques Rousseau, 1712~1778)의 사회계약론은 롤스에게 중요한 영향을 미쳤다. "
                "루소의 일반의지(volonté générale) 개념, 즉 공동선을 지향하는 시민의 의지라는 관념은 "
                "롤스의 원초적 입장에서의 합의와 유사한 구조를 가진다. "
                "롤스는 루소의 사회계약론을 홉스·로크와 함께 자신의 직접적 선행자로 인정했으며, "
                "특히 평등에 대한 루소의 강조가 차등원칙의 발상에 기여했다."
            ),
            "strength": "보통",
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
    r = client.get(index=INDEX_THINKERS, id="rawls")
    print(f"[thinker] rawls: name={r['_source']['name_en']}, era={r['_source']['era']}, field={r['_source']['field']}")

    # field 확인
    try:
        f = client.get(index=INDEX_FIELDS, id="political_philosophy")
        print(f"[field] political_philosophy: name={f['_source']['name']}")
    except Exception:
        print("[field] political_philosophy: NOT FOUND")

    # works 확인
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "rawls"}})
    print(f"[works] rawls 저서 수: {works_count['count']}")
    works_result = client.search(
        index=INDEX_WORKS,
        query={"term": {"thinker_id": "rawls"}},
        _source=["id", "title_original", "year"],
        size=10
    )
    for hit in works_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['title_original']} ({s['year']})")

    # claims 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "rawls"}})
    print(f"[claims] rawls 주장 수: {claims_count['count']}")
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "rawls"}},
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
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "rawls"}})
    print(f"[keywords] rawls 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_count = client.count(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "rawls"}},
            {"term": {"to_thinker": "rawls"}}
        ]}}
    )
    print(f"[relations] rawls 관련 관계 수: {rel_count['count']}")
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "rawls"}},
            {"term": {"to_thinker": "rawls"}}
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
        print("=== 존 롤스(John Rawls) 데이터 입력 시작 ===\n")

        print("0. 분야(정치철학) 확인/추가")
        ensure_field(client)

        print("\n1. 사상가 입력")
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
        print(f"field: 1건 | thinker: 1건 | works: {stats['works']}건 | claims: {stats['claims']}건 | "
              f"keywords: {stats['keywords']}건 | relations: {stats['relations']}건")

        return stats

    finally:
        close_client(client)


if __name__ == "__main__":
    main()
