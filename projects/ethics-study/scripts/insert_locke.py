"""존 로크(John Locke) 데이터를 ES에 직접 입력하는 스크립트."""

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
    """로크 사상가 데이터 입력."""
    doc = {
        "id": "locke",
        "name": "존 로크",
        "name_en": "John Locke",
        "field": "political_philosophy",
        "era": "근대 초기",
        "birth_year": 1632,
        "death_year": 1704,
        "background": (
            "영국 서머셋(Somerset) 링턴(Wrington)에서 청교도 변호사의 아들로 태어났다. "
            "웨스트민스터 학교(Westminster School)를 거쳐 옥스퍼드 크라이스트처치(Christ Church)에서 "
            "스콜라 철학, 의학, 자연과학을 공부했다. 로버트 보일(Robert Boyle)의 영향으로 "
            "경험주의적 방법론에 깊이 공감했으며, 의사로서의 활동이 경험적 관찰의 중요성에 대한 "
            "확신을 강화했다. 1667년부터 초대 새프츠베리 백작(Earl of Shaftesbury)의 자문으로 "
            "활동하며 정치에 본격적으로 관여했다. 새프츠베리의 몰락과 함께 1683년 네덜란드로 "
            "망명하여 약 6년간 체류했고, 이 시기에 주요 저작들을 완성했다. "
            "1688년 명예혁명(Glorious Revolution) 이후 귀국하여 윌리엄 3세 치하에서 "
            "정치적 영향력을 행사했다. 로크의 사상은 명예혁명의 철학적 정당화로 기능했다."
        ),
        "core_philosophy": (
            "로크의 핵심 사상은 자연법에 기초한 자유주의적 정치철학이다. "
            "인간은 자연 상태에서 자유롭고 평등하며, 이성(자연법)에 의해 생명(life), "
            "자유(liberty), 재산(property)의 자연권을 가진다. "
            "정치 사회는 이 자연권을 더 효과적으로 보호하기 위해 자발적 동의(consent)에 의해 수립된다. "
            "정부의 권력은 인민의 신탁(trust)에 기초하며, 신탁을 위반하는 정부에 대해 "
            "인민은 저항권(right of resistance)을 가진다. "
            "인식론에서는 타불라 라사(tabula rasa, 백지 상태)를 주장하여 "
            "본유관념(innate ideas)을 거부하고, 모든 지식은 경험에서 비롯된다고 보았다. "
            "소유권의 노동이론(labor theory of property)을 통해 개인의 재산권을 자연법적으로 정당화했다."
        ),
        "philosophical_journey": (
            "초기(~1666): 옥스퍼드에서 스콜라 철학과 의학을 배우며 경험주의적 방법론에 눈을 뜨다. "
            "로버트 보일의 실험적 자연철학에 영향을 받아 경험적 관찰의 중요성을 깨달았다. "
            "중기(1667~1683): 새프츠베리 백작의 자문으로 정치에 관여하며 관용, 자연권, "
            "제한적 정부에 대한 사상을 형성했다. '인간오성론'의 초고를 작성하기 시작했다. "
            "망명기(1683~1689): 네덜란드에서 '인간오성론', '통치론', '관용에 관한 서한'을 완성했다. "
            "네덜란드의 종교적 관용과 상업적 번영이 그의 사상에 영향을 미쳤다. "
            "후기(1689~1704): 명예혁명 이후 귀국하여 주요 저작을 출판하고, "
            "교육론(1693), 기독교의 합리성(1695) 등을 집필했다. "
            "오츠(Oates)의 매셤(Masham) 가문에서 말년을 보내며 72세에 사망했다."
        ),
        "keywords": [
            "자연권(생명·자유·재산)",
            "사회계약(동의·신탁)",
            "저항권",
            "타불라 라사",
            "소유권 노동이론",
            "관용",
            "제한적 정부",
            "권력 분립",
            "동의에 의한 정부",
            "자연 상태(평화·이성)"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="locke", document=doc)
    print(f"[thinker] locke: {result['result']}")
    return result


def insert_works(client):
    """로크 저서 데이터 입력."""
    works = [
        {
            "id": "locke-two-treatises",
            "thinker_id": "locke",
            "title": "통치론",
            "title_original": "Two Treatises of Government",
            "year": 1689,
            "significance": (
                "로크 정치철학의 대표작이자 근대 자유주의의 가장 중요한 텍스트 중 하나. "
                "제1론(First Treatise)은 로버트 필머(Robert Filmer)의 왕권신수설(divine right of kings)을 "
                "논박하고, 제2론(Second Treatise)은 자연 상태, 자연법, 소유권, 사회계약, "
                "정부의 목적과 한계, 권력 분립, 저항권을 체계적으로 전개한다. "
                "1688년 명예혁명의 철학적 정당화로 읽히지만, 실제로는 혁명 이전(1679~1681경)에 "
                "대부분 집필되었다. 미국 독립선언서(1776)와 프랑스 인권선언(1789)에 "
                "직접적 영향을 미쳤다."
            ),
            "key_concepts": [
                "자연 상태", "자연법", "자연권(생명·자유·재산)", "소유권 노동이론",
                "사회계약(동의)", "신탁(trust)", "권력 분립", "저항권"
            ]
        },
        {
            "id": "locke-essay",
            "thinker_id": "locke",
            "title": "인간오성론",
            "title_original": "An Essay Concerning Human Understanding",
            "year": 1689,
            "significance": (
                "근대 경험주의 인식론의 기초를 놓은 대작. 4권으로 구성된다. "
                "제1권: 본유관념(innate ideas) 비판 — 데카르트주의 반박. "
                "제2권: 관념의 기원 — 감각(sensation)과 반성(reflection)을 통해 모든 관념이 형성됨. "
                "제3권: 언어와 관념의 관계. "
                "제4권: 지식의 범위와 한계. "
                "타불라 라사(tabula rasa, 백지 상태) 개념으로 유명하며, "
                "이는 로크 정치철학의 평등주의적 토대가 된다: "
                "본유적 신분이나 특권이 없다면, 모든 인간은 동등한 출발점에서 시작한다."
            ),
            "key_concepts": [
                "타불라 라사", "본유관념 비판", "감각과 반성", "단순관념과 복합관념",
                "제1성질과 제2성질", "인격적 동일성(personal identity)"
            ]
        },
        {
            "id": "locke-toleration",
            "thinker_id": "locke",
            "title": "관용에 관한 서한",
            "title_original": "A Letter Concerning Toleration",
            "year": 1689,
            "significance": (
                "종교적 관용의 원리를 체계적으로 옹호한 저작. "
                "교회와 국가의 분리를 주장하며, 시민 정부의 관할은 시민적 이익(civil interests)에 한정되고 "
                "영혼의 구원은 정부의 권한 밖이라고 논증한다. "
                "양심의 자유(liberty of conscience)를 옹호하되, "
                "관용의 한계도 명시한다: 무신론자(사회적 신뢰의 기반인 맹세를 할 수 없으므로)와 "
                "외국 군주(교황)에 충성하는 자는 관용의 대상에서 제외했다. "
                "네덜란드 망명 시기에 집필되었으며, 필립 반 림보르흐(Philip van Limborch)에게 보낸 서한 형식이다."
            ),
            "key_concepts": [
                "종교적 관용", "교회와 국가의 분리", "양심의 자유",
                "시민적 이익", "관용의 한계"
            ]
        },
        {
            "id": "locke-education",
            "thinker_id": "locke",
            "title": "교육론",
            "title_original": "Some Thoughts Concerning Education",
            "year": 1693,
            "significance": (
                "교육의 목적과 방법에 관한 저작으로, 에드워드 클라크(Edward Clarke)에게 보낸 "
                "서한들을 정리한 것이다. 신사(gentleman) 교육을 주제로 하며, "
                "덕(virtue), 지혜(wisdom), 예의(breeding), 학문(learning)의 네 가지 교육 목표를 제시한다. "
                "타불라 라사에 기초하여 교육의 결정적 역할을 강조하며, "
                "'나는 만나는 사람들의 10분의 9는 교육에 의해 선하든 악하든, "
                "유용하든 무용하든 만들어진다고 생각한다'고 선언했다. "
                "루소의 '에밀'(1762)에 직접적 영향을 미쳤다."
            ),
            "key_concepts": [
                "신사 교육", "덕·지혜·예의·학문", "타불라 라사와 교육",
                "습관 형성", "경험적 학습"
            ]
        },
        {
            "id": "locke-second-treatise",
            "thinker_id": "locke",
            "title": "시민정부론(통치론 제2론)",
            "title_original": "Second Treatise of Civil Government",
            "year": 1689,
            "significance": (
                "통치론(Two Treatises) 중 제2론으로, 로크 정치철학의 핵심이 담겨 있다. "
                "제1론이 필머의 왕권신수설을 논박하는 데 할애된 반면, "
                "제2론은 정치 권력의 참된 기원, 범위, 목적을 긍정적으로 전개한다. "
                "19개 장으로 구성되어 자연 상태(2장), 전쟁 상태(3장), 소유권(5장), "
                "정치 사회의 시작(8장), 정부의 목적(9장), 입법권(11장), "
                "권력 분립(12~14장), 정복·찬탈·폭정(15~18장), 정부의 해체와 저항권(19장)을 다룬다. "
                "독립적으로 'Second Treatise' 또는 '시민정부론'으로 자주 인용된다."
            ),
            "key_concepts": [
                "자연 상태", "전쟁 상태", "소유권", "동의에 의한 정부",
                "입법권의 우위", "대권(prerogative)", "저항권", "정부의 해체"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """로크 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 자연 상태 — 자유와 평등, 자연법의 지배
        {
            "id": "locke-claim-001",
            "thinker_id": "locke",
            "work_id": "locke-second-treatise",
            "source_detail": "Second Treatise, Chapter 2, §4-15",
            "claim": (
                "자연 상태(state of nature)는 완전한 자유(perfect freedom)와 평등(equality)의 상태이며, "
                "자연법(law of nature)이 지배한다. 자연법은 곧 이성(reason)이며, "
                "이성은 모든 인간에게 타인의 생명, 건강, 자유, 재산을 침해하지 말 것을 가르친다."
            ),
            "original_text": (
                "To understand political power right, and derive it from its original, we must consider, "
                "what state all men are naturally in, and that is, a state of perfect freedom to order their "
                "actions, and dispose of their possessions and persons, as they think fit, within the bounds "
                "of the law of nature, without asking leave, or depending upon the will of any other man. "
                "A state also of equality, wherein all the power and jurisdiction is reciprocal."
            ),
            "original_text_ko": (
                "정치 권력을 올바로 이해하고 그 기원에서 도출하기 위해서는, "
                "모든 인간이 자연적으로 어떤 상태에 있는지를 고려해야 한다. "
                "그것은 자연법의 범위 안에서 타인의 허락을 구하거나 타인의 의지에 의존하지 않고 "
                "자신의 행동을 정하고, 자신의 소유물과 인신을 적합하다고 생각되는 대로 처분할 수 있는 "
                "완전한 자유의 상태이다. 또한 모든 권력과 관할이 상호적인 평등의 상태이다."
            ),
            "explanation": (
                "로크의 자연 상태는 홉스와 결정적으로 다르다. "
                "홉스에게 자연 상태가 만인에 대한 만인의 투쟁인 반면, "
                "로크에게 자연 상태는 자연법(이성)이 지배하는 질서 있는 상태이다. "
                "자연 상태에서 각 인간은 자연법의 집행자로서 자연법 위반자를 처벌할 권리를 가진다. "
                "자연 상태가 전쟁 상태(state of war)와 구별되는 것은 로크 정치철학의 핵심 축이다: "
                "전쟁 상태는 자연법을 위반하여 타인의 생명을 위협하는 상태이며, "
                "자연 상태의 불편함(inconvenience)은 전쟁 상태와 다르다."
            ),
            "argument": (
                "(1) 인간은 같은 종(species)의 존재로서 자연적으로 평등하다(리처드 후커 인용). "
                "(2) 자연법(이성)은 모든 인간에게 자신을 보존하고, "
                "가능한 한 나머지 인류도 보존할 것을 명한다. "
                "(3) 자연법의 범위 안에서 인간은 자유롭다: 자신의 행동과 재산을 처분할 자유. "
                "(4) 자연 상태에서 각 인간은 자연법의 위반자를 처벌할 집행 권한(executive power)을 가진다. "
                "(5) 이 처벌권은 비례적(proportionate)이어야 하며, 위반의 억제와 보상을 목적으로 한다. "
                "(6) 따라서 자연 상태는 무질서가 아니라 자연법이 지배하는 질서 있는 상태이다."
            ),
            "counterpoint": (
                "홉스는 '리바이어던'(1651) 제13장에서 공통 권력이 없는 자연 상태는 "
                "필연적으로 만인에 대한 만인의 투쟁 상태라고 주장했다. "
                "홉스에 따르면 자연법은 존재하지만 이를 강제할 공통 권력이 없으면 실효성이 없다. "
                "로크의 자연 상태가 너무 낙관적이며, 자연법의 자발적 준수를 과신한다는 비판이다. "
                "데이비드 흄(David Hume)은 '인성론'(A Treatise of Human Nature, 1739) 제3권에서 "
                "사회계약 이전의 자연 상태라는 개념 자체가 역사적 허구이며, "
                "정의와 소유권은 사회적 관습(convention)에 의해 발생한다고 비판했다."
            ),
            "context": (
                "로크는 홉스의 자연 상태론을 직접적으로 비판하면서 자신의 자연 상태론을 전개한다. "
                "자연 상태와 전쟁 상태의 구별은 제한적 정부론의 토대이다: "
                "자연 상태가 이미 어느 정도 질서 있는 상태라면, "
                "정부는 그 질서를 완전히 대체하는 것이 아니라 보완하는 역할을 한다."
            ),
            "keywords": ["자연 상태", "자유", "평등", "자연법", "이성"],
            "verified": False
        },
        # CLAIM-002: 자연권 — 생명, 자유, 재산
        {
            "id": "locke-claim-002",
            "thinker_id": "locke",
            "work_id": "locke-second-treatise",
            "source_detail": "Second Treatise, Chapter 2, §6; Chapter 9, §123",
            "claim": (
                "모든 인간은 자연법에 의해 생명(life), 자유(liberty), 재산(property)에 대한 "
                "양도할 수 없는 자연권(natural rights)을 가진다. "
                "이 세 가지를 포괄하여 로크는 '재산(property)'이라는 넓은 의미의 용어를 사용하며, "
                "정부의 존재 이유는 이 자연권의 보호에 있다."
            ),
            "original_text": (
                "The state of nature has a law of nature to govern it, which obliges every one: "
                "and reason, which is that law, teaches all mankind, who will but consult it, "
                "that being all equal and independent, no one ought to harm another in his life, "
                "health, liberty, or possessions."
            ),
            "original_text_ko": (
                "자연 상태에는 그것을 지배하는 자연법이 있으며, 이는 모든 사람을 구속한다. "
                "그리고 그 법인 이성은 그것에 상의하고자 하는 모든 인류에게, "
                "모두가 평등하고 독립적이므로, 누구도 타인의 생명, 건강, 자유, 또는 소유물을 "
                "해쳐서는 안 된다고 가르친다."
            ),
            "explanation": (
                "로크의 자연권은 홉스의 자연권과 근본적으로 다르다. "
                "홉스에게 자연권은 '모든 것에 대한 무제한적 권리'인 반면, "
                "로크에게 자연권은 자연법에 의해 처음부터 제한된 권리이다. "
                "로크는 'property'를 두 가지 의미로 사용한다: "
                "넓은 의미에서는 생명·자유·재산을 포괄하는 것이고, "
                "좁은 의미에서는 물질적 소유(estate)를 뜻한다. "
                "이 자연권 개념은 미국 독립선언서의 '생명, 자유, 행복의 추구(life, liberty, "
                "and the pursuit of happiness)'에 직접적 영향을 미쳤다."
            ),
            "argument": (
                "(1) 인간은 신(God)의 작품이며, 신의 소유이다(창조주 논증). "
                "(2) 신은 인간에게 자기보존의 의무를 부여했고, 이를 위해 이성(자연법)을 주었다. "
                "(3) 자연법은 타인의 생명, 자유, 재산을 침해하지 말라고 명한다. "
                "(4) 이 금지에 대응하여 각 개인은 생명, 자유, 재산에 대한 권리를 가진다. "
                "(5) 이 권리는 인간이 만든 것이 아니라 자연법(신의 법)에서 비롯되므로 양도 불가능하다. "
                "(6) 정부의 목적은 이 자연권의 보호이며, 이 목적을 배반하는 정부는 정당성을 잃는다."
            ),
            "counterpoint": (
                "제러미 벤담(Jeremy Bentham)은 '정부에 관한 단편'(A Fragment on Government, 1776)과 "
                "'무정부적 오류'(Anarchical Fallacies, 1796)에서 자연권이란 "
                "'말뚝 위의 넌센스(nonsense upon stilts)'라고 일축했다. "
                "벤담에 따르면 권리는 법률에 의해 창설되는 것이며, "
                "법률 이전의 자연권이란 존재하지 않는다. "
                "에드먼드 버크(Edmund Burke)도 '프랑스 혁명에 관한 성찰'(Reflections on the Revolution in France, 1790)에서 "
                "추상적 자연권보다 역사적으로 형성된 구체적 권리(prescriptive rights)가 더 실질적이라고 비판했다."
            ),
            "context": (
                "로크의 자연권 개념은 중세 자연법 전통(아퀴나스)과 그로티우스(Hugo Grotius)의 "
                "자연법론을 계승하되, 개인의 권리를 전면에 내세운 점에서 근대적 전환을 보여준다. "
                "이후 미국 건국의 아버지들과 프랑스 혁명 사상가들에게 결정적 영향을 미쳤다."
            ),
            "keywords": ["자연권", "생명", "자유", "재산", "양도불가능한 권리"],
            "verified": False
        },
        # CLAIM-003: 사회계약 — 동의(consent)와 신탁(trust)
        {
            "id": "locke-claim-003",
            "thinker_id": "locke",
            "work_id": "locke-second-treatise",
            "source_detail": "Second Treatise, Chapter 8, §95-99; Chapter 9, §123-131",
            "claim": (
                "정치 사회는 자유로운 개인들의 자발적 동의(consent)에 의해서만 정당하게 수립된다. "
                "개인들은 자연 상태의 불편함을 해소하기 위해 자연법 집행권을 공동체에 양도하며, "
                "공동체는 이 권력을 정부에 신탁(trust)한다. 정부는 인민의 수탁자(trustee)이다."
            ),
            "original_text": (
                "Men being, as has been said, by nature, all free, equal, and independent, "
                "no one can be put out of this estate, and subjected to the political power of another, "
                "without his own consent. The only way whereby any one divests himself of his natural liberty, "
                "and puts on the bonds of civil society, is by agreeing with other men to join and unite "
                "into a community for their comfortable, safe, and peaceable living one amongst another, "
                "in a secure enjoyment of their properties, and a greater security against any, "
                "that are not of it."
            ),
            "original_text_ko": (
                "인간은 이미 말한 대로 자연적으로 모두 자유롭고, 평등하고, 독립적이므로, "
                "누구도 자신의 동의 없이 이 상태에서 벗어나 타인의 정치 권력에 복종하게 될 수 없다. "
                "자연적 자유를 벗고 시민 사회의 구속을 입는 유일한 방법은, "
                "다른 사람들과 합의하여 공동체로 결합하고 통합하는 것이며, "
                "이는 서로 간의 편안하고 안전하며 평화로운 생활과 "
                "재산의 안전한 향유, 그리고 외부인에 대한 더 큰 안전을 위한 것이다."
            ),
            "explanation": (
                "로크의 사회계약은 홉스와 두 가지 결정적 차이가 있다. "
                "첫째, 양도의 범위: 홉스에서 개인은 자연권 전체를 양도하지만, "
                "로크에서 개인은 자연법 집행권(executive power of the law of nature)만 양도한다. "
                "생명·자유·재산의 자연권 자체는 양도되지 않는다. "
                "둘째, 정부의 지위: 홉스에서 주권자는 계약 당사자가 아니므로 의무가 없지만, "
                "로크에서 정부는 인민의 신탁을 받은 수탁자이므로 신탁 조건(자연권 보호)을 이행할 의무가 있다. "
                "로크는 또한 동의를 명시적 동의(express consent)와 묵시적 동의(tacit consent)로 구분한다."
            ),
            "argument": (
                "(1) 인간은 자연적으로 자유, 평등, 독립적이다. "
                "(2) 자발적 동의 없이는 누구도 타인의 정치 권력에 복종할 수 없다. "
                "(3) 자연 상태에는 세 가지 불편함(inconvenience)이 있다: "
                "확립된 법률의 부재, 공인된 재판관의 부재, 판결을 집행할 권력의 부재. "
                "(4) 이 불편함을 해소하기 위해 개인들은 자연법 집행권을 공동체에 양도한다. "
                "(5) 공동체는 다수결(majority rule)로 운영되며, "
                "입법·집행 권력을 정부에 신탁(trust)한다. "
                "(6) 정부는 수탁자로서 자연권 보호라는 신탁 목적에 구속된다."
            ),
            "counterpoint": (
                "홉스는 '리바이어던'(1651) 제17장에서 사회계약이 개인들 사이에서 이루어지며 "
                "주권자는 계약 당사자가 아니라고 주장했다. 따라서 주권자는 계약을 위반할 수 없다. "
                "로크의 신탁(trust) 개념은 정부를 계약적 의무 하에 두는 것으로, "
                "홉스의 절대주권론과 정면 대립한다. "
                "흄은 '원초적 계약에 관하여'(Of the Original Contract, 1748)에서 "
                "역사상 대부분의 정부는 동의가 아니라 정복이나 관습에 의해 수립되었으므로 "
                "동의 이론은 역사적 허구라고 비판했다. "
                "묵시적 동의(tacit consent) 개념의 모호성도 지속적 비판 대상이다."
            ),
            "context": (
                "로크의 동의 이론은 영국 왕권과 의회의 갈등이라는 맥락에서 형성되었다. "
                "필머의 왕권신수설에 맞서 정치 권력의 정당성을 인민의 동의에 두려는 시도이다. "
                "명예혁명(1688)은 로크의 동의 이론과 저항권 이론의 현실적 실현으로 읽혔다."
            ),
            "keywords": ["사회계약", "동의", "신탁(trust)", "묵시적 동의", "다수결"],
            "verified": False
        },
        # CLAIM-004: 저항권 — 정부 해체와 혁명의 정당성
        {
            "id": "locke-claim-004",
            "thinker_id": "locke",
            "work_id": "locke-second-treatise",
            "source_detail": "Second Treatise, Chapter 19, §220-243",
            "claim": (
                "정부가 인민의 신탁을 위반하여 자연권을 침해하면, "
                "인민은 정부를 해체하고 새로운 정부를 수립할 권리(저항권, right of resistance)를 가진다. "
                "폭정(tyranny)에 대한 저항은 반란(rebellion)이 아니다. "
                "오히려 신탁을 위반한 통치자야말로 진정한 반란자이다."
            ),
            "original_text": (
                "Whensoever therefore the legislative shall transgress this fundamental rule of society; "
                "and either by ambition, fear, folly or corruption, endeavour to grasp themselves, "
                "or put into the hands of any other, an absolute power over the lives, liberties, "
                "and estates of the people; by this breach of trust they forfeit the power the people "
                "had put into their hands for quite contrary ends, and it devolves to the people, "
                "who have a right to resume their original liberty."
            ),
            "original_text_ko": (
                "따라서 입법부가 사회의 이 근본적 규칙을 위반하고, "
                "야심, 두려움, 어리석음 또는 부패로 인해 인민의 생명, 자유, 재산에 대한 "
                "절대적 권력을 스스로 쥐거나 타인의 손에 넘기려 할 때, "
                "이 신탁의 위반으로 그들은 인민이 정반대의 목적을 위해 그들의 손에 맡겼던 "
                "권력을 상실하며, 그 권력은 본래의 자유를 회복할 권리를 가진 인민에게 귀속된다."
            ),
            "explanation": (
                "저항권은 로크 정치철학의 가장 혁명적인 요소이다. "
                "홉스에게 주권자에 대한 저항은 자연 상태로의 회귀를 의미하므로 사실상 금지되지만, "
                "로크에게 정부는 인민의 신탁을 받은 수탁자에 불과하며, "
                "신탁을 위반하면 권력은 인민에게 되돌아온다(devolution of power). "
                "로크는 이것이 무정부를 초래한다는 반론에 대해, "
                "인민은 쉽게 혁명을 일으키지 않으며, 오히려 저항권의 존재가 "
                "통치자의 전제를 억제하는 예방적 기능을 한다고 답한다."
            ),
            "argument": (
                "(1) 정부의 권력은 인민의 신탁에 기초한다. "
                "(2) 신탁의 목적은 자연권(생명, 자유, 재산)의 보호이다. "
                "(3) 정부가 이 목적을 위반하면(폭정), 신탁은 파기된다. "
                "(4) 신탁 파기 시 권력은 인민에게 귀속된다(devolution). "
                "(5) 인민은 새로운 입법부를 수립할 수 있다. "
                "(6) 이 과정은 반란이 아니다: 진정한 반란자(rebels)는 "
                "인민에 대한 전쟁 상태를 개시한 통치자이다. "
                "(7) 이 교리는 무정부를 조장하지 않는다: 인민은 소소한 잘못에는 참으며, "
                "오직 체계적이고 장기적인 폭정에만 저항한다."
            ),
            "counterpoint": (
                "홉스는 '리바이어던'(1651) 제18장에서 주권자에 대한 저항은 "
                "사회계약의 위반이자 자연 상태로의 회귀이므로 정당화될 수 없다고 주장했다. "
                "주권자는 계약 당사자가 아니므로 계약을 위반할 수 없고, "
                "따라서 신민이 주권자를 처벌하거나 교체할 근거가 없다. "
                "보수주의 전통(버크 등)은 혁명이 기존 질서의 파괴와 "
                "예측할 수 없는 혼란을 초래한다고 비판했다. "
                "버크는 '프랑스 혁명에 관한 성찰'(1790)에서 프랑스 혁명의 참상을 예로 들어 "
                "추상적 권리에 기초한 혁명의 위험성을 경고했다."
            ),
            "context": (
                "로크의 저항권 이론은 1688년 명예혁명의 철학적 정당화로 읽혔다. "
                "제임스 2세의 전제에 맞서 의회와 인민이 윌리엄 3세를 초빙한 것은 "
                "로크의 저항권 이론의 현실적 실현으로 해석되었다. "
                "이후 미국 독립혁명(1776)과 프랑스 혁명(1789)에도 "
                "로크의 저항권 개념이 직접적 영향을 미쳤다."
            ),
            "keywords": ["저항권", "신탁 위반", "정부의 해체", "혁명", "폭정"],
            "verified": False
        },
        # CLAIM-005: 권력 분립 — 입법권의 우위
        {
            "id": "locke-claim-005",
            "thinker_id": "locke",
            "work_id": "locke-second-treatise",
            "source_detail": "Second Treatise, Chapters 11-14, §134-168",
            "claim": (
                "정부의 권력은 입법권(legislative power), 집행권(executive power), "
                "동맹권/연합권(federative power)으로 분립되어야 한다. "
                "입법권이 최고 권력(supreme power)이지만, 인민의 신탁에 의해 제약되며, "
                "입법권조차도 자연법을 넘어설 수 없다."
            ),
            "original_text": (
                "The legislative... being only a fiduciary power to act for certain ends, "
                "there remains still in the people a supreme power to remove or alter the legislative, "
                "when they find the legislative act contrary to the trust reposed in them."
            ),
            "original_text_ko": (
                "입법부는... 특정 목적을 위해 행위하도록 위임된 수탁적 권력에 불과하므로, "
                "입법부가 자신에게 부여된 신탁에 반하여 행위한다고 판단될 때 "
                "입법부를 제거하거나 변경할 최고 권력이 여전히 인민에게 남아 있다."
            ),
            "explanation": (
                "로크의 권력 분립론은 몽테스키외의 삼권분립론의 선구이다. "
                "입법권은 법률 제정, 집행권은 법률 시행, 동맹권은 외교·전쟁 등 대외 관계를 담당한다. "
                "로크는 사법권을 별도로 분리하지 않았으며(이는 몽테스키외의 기여), "
                "집행권과 동맹권은 실제로 같은 수중(보통 군주)에 있는 것이 편리하다고 보았다. "
                "핵심은 입법권의 우위(supremacy of the legislative)이다: "
                "입법권이 최고 권력이지만, 인민의 신탁에 의해 제약되므로 절대적이지 않다. "
                "로크는 또한 대권(prerogative)을 인정했다: 집행부가 공공선을 위해 "
                "법률의 규정 없이 또는 법률에 반하여 행위하는 재량권이다."
            ),
            "argument": (
                "(1) 인간은 자연 상태에서 두 가지 권력을 가진다: "
                "자기보존을 위해 자연법의 범위 안에서 행동하는 권력, "
                "자연법 위반자를 처벌하는 집행 권력. "
                "(2) 정치 사회에 들어가면서 첫 번째는 입법권으로, "
                "두 번째는 집행권으로 공동체에 양도된다. "
                "(3) 입법권이 최고 권력인 이유: 사회에 법을 부여할 수 있는 자가 그 사회에서 최고이다. "
                "(4) 그러나 입법권도 제한된다: "
                "(4a) 자의적이어서는 안 된다(자연법에 구속). "
                "(4b) 즉석에서 만든 법(arbitrary decrees)이 아니라 확립된 법률에 의해 통치해야 한다. "
                "(4c) 동의 없이 재산을 빼앗을 수 없다. "
                "(4d) 입법권을 타인에게 위임할 수 없다."
            ),
            "counterpoint": (
                "홉스는 '리바이어던'(1651) 제29장에서 주권의 분할은 커먼웰스의 해체를 의미한다고 주장했다. "
                "홉스에게 입법, 사법, 집행의 분리는 갈등의 씨앗이다. "
                "반면 몽테스키외는 '법의 정신'(1748) 제11권에서 로크의 권력 분립론을 더 발전시켜 "
                "입법, 행정, 사법의 삼권분립을 체계화하고, "
                "'권력을 가진 자는 누구나 그것을 남용하는 경향이 있다'며 "
                "권력의 상호 견제 필요성을 역설했다."
            ),
            "context": (
                "로크의 권력 분립론은 영국 헌정(constitutional) 실천의 이론적 정당화이다. "
                "명예혁명 이후 의회(입법)와 국왕(집행)의 관계를 규정하는 데 기여했으며, "
                "이후 미국 헌법의 삼권분립 구조에 간접적 영향을 미쳤다."
            ),
            "keywords": ["권력 분립", "입법권", "집행권", "동맹권", "대권(prerogative)"],
            "verified": False
        },
        # CLAIM-006: 소유권 노동이론
        {
            "id": "locke-claim-006",
            "thinker_id": "locke",
            "work_id": "locke-second-treatise",
            "source_detail": "Second Treatise, Chapter 5, §25-51",
            "claim": (
                "소유권(property)은 노동(labour)에 의해 발생한다. "
                "신이 세계를 인류 공동으로 주었지만, 각 인간은 자기 자신의 인신(person)에 대한 "
                "소유권을 가지며, 자연에 자신의 노동을 섞은(mixed) 것은 자신의 소유가 된다."
            ),
            "original_text": (
                "Though the earth, and all inferior creatures, be common to all men, "
                "yet every man has a property in his own person: this no body has any right to but himself. "
                "The labour of his body, and the work of his hands, we may say, are properly his. "
                "Whatsoever then he removes out of the state that nature hath provided, and left it in, "
                "he hath mixed his labour with, and joined to it something that is his own, "
                "and thereby makes it his property."
            ),
            "original_text_ko": (
                "비록 대지와 모든 하등 피조물이 모든 인간에게 공동이지만, "
                "모든 사람은 자기 자신의 인신(person)에 대한 소유권을 가진다. "
                "이것에 대해서는 본인 외에 아무도 권리를 갖지 않는다. "
                "그의 신체의 노동과 그의 손의 작업은, 우리가 말할 수 있듯이, 본래 그의 것이다. "
                "그러므로 자연이 마련하고 남겨둔 상태에서 그가 제거한 것은 무엇이든, "
                "자신의 노동을 섞고 자기 자신의 것을 결합한 것이며, "
                "이로써 그것을 자기의 소유로 만든다."
            ),
            "explanation": (
                "로크의 소유권 노동이론은 근대 재산권의 철학적 토대이다. "
                "핵심 논증 구조: (a) 각 개인은 자기 자신(인신)에 대한 소유권을 가진다. "
                "(b) 자기 몸의 노동은 자기의 것이다. (c) 자연물에 노동을 섞으면 소유가 된다. "
                "로크는 두 가지 제한(proviso)을 둔다: "
                "(1) 충분한 양과 질이 다른 사람에게도 남아 있어야 한다(enough and as good). "
                "(2) 부패하기 전에 사용할 수 있는 만큼만 소유할 수 있다(spoilage proviso). "
                "그러나 화폐의 발명이 이 제한을 사실상 극복하게 한다고 로크는 논증한다."
            ),
            "argument": (
                "(1) 신은 세계를 인류 공동(common)으로 주었다. "
                "(2) 그러나 각 개인은 자기 자신의 인신(person)에 대한 소유권을 가진다. "
                "(3) 자기 몸의 노동은 의심할 여지없이 자기의 것이다. "
                "(4) 자연물에 자신의 노동을 섞으면, 그것은 공동 상태에서 제거되어 자기 소유가 된다. "
                "(5) 이 전유(appropriation)에는 타인의 동의가 필요 없다. "
                "(6) 제한: 다른 사람에게도 충분히 남아 있어야 하고(enough-and-as-good), "
                "부패하기 전에 사용할 수 있는 만큼만(spoilage proviso). "
                "(7) 화폐의 발명은 축적의 제한을 극복하게 한다: "
                "금·은은 부패하지 않으므로 무한 축적이 가능해진다."
            ),
            "counterpoint": (
                "카를 마르크스(Karl Marx)는 '자본론'(Das Kapital, 1867) 제1권 제24장에서 "
                "로크의 노동이론이 자본주의적 사유재산을 정당화하는 이데올로기라고 비판했다. "
                "마르크스에 따르면 자본주의에서 노동자의 노동은 자본가에 의해 전유되며(잉여가치), "
                "노동과 소유의 연결은 자본주의적 착취에 의해 단절된다. "
                "로버트 노직(Robert Nozick)은 '무정부, 국가, 유토피아'(Anarchy, State, and Utopia, 1974)에서 "
                "로크의 노동혼합 논증을 비판하며, '토마토 주스를 바다에 부으면 바다를 소유하는가?'라고 "
                "반문하여 노동혼합 개념의 불명확성을 지적했다."
            ),
            "context": (
                "로크의 소유권 이론은 17세기 영국의 토지 인클로저(enclosure) 운동, "
                "아메리카 식민지의 토지 점유, 상업 자본주의의 발전이라는 맥락에서 형성되었다. "
                "아메리카 원주민의 토지에 대해 '경작하지 않으면 소유가 아니다'라는 논리로 "
                "식민지 확장을 정당화하는 데 사용되기도 했다."
            ),
            "keywords": ["소유권", "노동이론", "전유", "노동혼합", "충분조건(proviso)"],
            "verified": False
        },
        # CLAIM-007: 동의에 의한 정부 — 명시적/묵시적 동의
        {
            "id": "locke-claim-007",
            "thinker_id": "locke",
            "work_id": "locke-second-treatise",
            "source_detail": "Second Treatise, Chapter 8, §116-122",
            "claim": (
                "정당한 정부는 오직 피치자의 동의(consent of the governed)에만 기초한다. "
                "동의는 명시적 동의(express consent)와 묵시적 동의(tacit consent)로 나뉜다. "
                "한 국가의 영토 내에서 재산을 소유하거나 거주하는 것만으로도 "
                "그 국가의 법률에 대한 묵시적 동의가 성립한다."
            ),
            "original_text": (
                "Every man, that hath any possessions, or enjoyment, of any part of the dominions "
                "of any government, doth thereby give his tacit consent, and is as far forth obliged "
                "to obedience to the laws of that government, during such enjoyment, "
                "as any one under it."
            ),
            "original_text_ko": (
                "어떤 정부의 영토의 일부에서 소유나 향유를 하는 모든 사람은, "
                "그것에 의해 묵시적 동의를 표하는 것이며, "
                "그 향유가 지속되는 동안 그 정부의 법률에 대해 "
                "그 아래 있는 누구 못지않게 복종할 의무를 진다."
            ),
            "explanation": (
                "명시적 동의(express consent)는 국적 취득, 시민 선서 등 명확한 행위로 표현되며, "
                "이를 통해 그 사회의 영구적 구성원이 된다. "
                "묵시적 동의(tacit consent)는 토지 소유, 거주, 도로 이용 등으로 추정되며, "
                "더 약한 구속력을 가진다: 묵시적 동의를 한 자는 떠날 자유가 있다. "
                "묵시적 동의 개념은 로크 정치철학에서 가장 논쟁적인 부분 중 하나이다. "
                "비판자들은 '거주'나 '도로 이용'을 동의로 보는 것이 "
                "동의 개념을 의미 없이 확장한다고 지적한다."
            ),
            "argument": (
                "(1) 정부의 정당성은 동의에 기초한다. "
                "(2) 모든 시민에게 명시적 동의를 요구하는 것은 비현실적이다. "
                "(3) 그러나 한 국가의 영토에서 재산을 소유하거나 거주하는 것은 "
                "그 국가의 법률의 보호를 받는 것이므로, 법률 준수에 대한 묵시적 동의를 의미한다. "
                "(4) 명시적 동의는 영구적 귀속을 낳지만, 묵시적 동의는 "
                "그 영토를 떠나면 해소될 수 있다. "
                "(5) 이로써 동의 이론의 현실적 적용 가능성을 확보한다."
            ),
            "counterpoint": (
                "흄은 '원초적 계약에 관하여'(Of the Original Contract, 1748)에서 "
                "묵시적 동의 개념을 신랄하게 비판했다. 흄에 따르면 가난한 농부가 "
                "국가를 떠날 현실적 자유가 없는데, 그의 '거주'를 동의로 간주하는 것은 "
                "가난한 자를 배에 실어 대양 한가운데 데려간 뒤 "
                "'배에 남아 있으므로 선장에 자발적으로 복종한 것'이라고 말하는 것과 같다. "
                "A. 존 시먼스(A. John Simmons)는 'Moral Principles and Political Obligations'(1979)에서 "
                "묵시적 동의가 실질적 의무를 창출하기에는 불충분하다고 분석했다."
            ),
            "context": (
                "동의 이론은 17세기 영국에서 왕권의 정당성 근거를 둘러싼 논쟁에서 형성되었다. "
                "필머의 왕권신수설(정당성의 근거 = 신의 수여)에 맞서, "
                "로크는 인민의 동의를 정당성의 유일한 근거로 주장했다."
            ),
            "keywords": ["동의에 의한 정부", "명시적 동의", "묵시적 동의", "정당성"],
            "verified": False
        },
        # CLAIM-008: 제한적 정부 — 정부 권력의 한계
        {
            "id": "locke-claim-008",
            "thinker_id": "locke",
            "work_id": "locke-second-treatise",
            "source_detail": "Second Treatise, Chapter 11, §134-142",
            "claim": (
                "정부의 권력은 자연법에 의해 제한된다. "
                "입법부조차도 (1) 자의적 권력을 행사할 수 없고, (2) 즉석 법령이 아닌 확립된 법률로 통치해야 하며, "
                "(3) 동의 없이 재산을 빼앗을 수 없고, (4) 입법권을 타인에게 위임할 수 없다."
            ),
            "original_text": (
                "These are the bounds which the trust, that is put in them by the society, "
                "and the law of God and nature, have set to the legislative power of every commonwealth, "
                "in all forms of government."
            ),
            "original_text_ko": (
                "이것들이 사회에 의해 그들에게 부여된 신탁과 신의 법과 자연법이 "
                "모든 형태의 정부에서 모든 커먼웰스의 입법권에 설정한 한계이다."
            ),
            "explanation": (
                "로크의 제한적 정부론은 홉스의 절대주권론에 정면 대립한다. "
                "홉스에게 주권자의 권력은 절대적이고 분할 불가능하지만, "
                "로크에게 정부의 권력은 자연법과 인민의 신탁에 의해 본질적으로 제한된다. "
                "네 가지 제한은 근대 입헌주의(constitutionalism)의 핵심 원리를 선취한다: "
                "(1) 자의적 권력 금지 → 법치주의(rule of law), "
                "(2) 확립된 법률 → 법적 안정성, "
                "(3) 동의 없는 과세 금지 → 'no taxation without representation', "
                "(4) 입법권 위임 금지 → 위임 금지 원칙."
            ),
            "argument": (
                "(1) 자연 상태에서 인간은 자의적 권력(arbitrary power)을 가지지 않는다. "
                "(2) 자연법은 자기보존에 필요한 범위에서만 행위하라고 명한다. "
                "(3) 사회계약에서 양도할 수 없는 것: 자기가 가지지 않은 권력은 양도할 수 없다. "
                "(4) 따라서 정부도 자의적 권력을 가질 수 없다. "
                "(5) 마찬가지로 재산에 대한 권리는 자연법에 의한 것이므로, "
                "정부가 동의 없이 빼앗을 수 없다. "
                "(6) 인민이 입법권을 맡긴 것이지, 입법권을 다시 남에게 맡기라고 한 것이 아니다."
            ),
            "counterpoint": (
                "홉스는 '리바이어던'(1651) 제18장에서 주권자의 권력에 대한 어떤 제한도 "
                "자연 상태로의 회귀를 초래한다고 주장했다. "
                "주권자의 권력이 제한되면 그 제한을 판단하는 상위 권력이 필요하고, "
                "이는 무한퇴행 또는 주권의 분열을 낳는다. "
                "장 보댕(Jean Bodin)도 '국가론'(Les Six Livres de la République, 1576)에서 "
                "주권은 절대적이고 영속적인 권력이라 정의하여 "
                "제한적 주권이라는 개념 자체를 모순으로 보았다."
            ),
            "context": (
                "로크의 제한적 정부론은 영국의 매그나 카르타(Magna Carta, 1215) 이래의 "
                "왕권 제한 전통, 특히 1628년 권리청원(Petition of Right)과 "
                "1689년 권리장전(Bill of Rights)의 이론적 토대가 되었다."
            ),
            "keywords": ["제한적 정부", "법치주의", "입헌주의", "동의 없는 과세 금지"],
            "verified": False
        },
        # CLAIM-009: 관용 — 종교적 관용과 교회-국가 분리
        {
            "id": "locke-claim-009",
            "thinker_id": "locke",
            "work_id": "locke-toleration",
            "source_detail": "A Letter Concerning Toleration, pp. 5-20 (ed. Tully)",
            "claim": (
                "시민 정부의 관할은 시민적 이익(civil interests: 생명, 자유, 건강, 재산)에 한정되며, "
                "영혼의 구원(salvation of souls)은 정부의 권한 밖이다. "
                "교회는 자발적 결사체(voluntary society)이며, "
                "신앙의 문제에 강제력을 사용하는 것은 부당하고 비효과적이다."
            ),
            "original_text": (
                "The commonwealth seems to me to be a society of men constituted only for the procuring, "
                "preserving, and advancing of their own civil interests. "
                "Civil interests I call life, liberty, health, and indolency of body; "
                "and the possession of outward things, such as money, lands, houses, furniture, and the like."
            ),
            "original_text_ko": (
                "커먼웰스는 내가 보기에 오직 시민적 이익의 획득, 보존, 증진만을 위해 "
                "구성된 인간들의 사회인 것 같다. "
                "시민적 이익이란 내가 생명, 자유, 건강, 신체의 안녕, "
                "그리고 화폐, 토지, 집, 가구 등과 같은 외적 소유물을 말한다."
            ),
            "explanation": (
                "로크의 관용론은 세 가지 논증에 기초한다. "
                "첫째, 관할권 논증: 정부의 관할은 시민적 이익에 한정되며 영혼의 구원은 관할 밖이다. "
                "둘째, 비효과성 논증: 강제력은 외적 행동은 통제할 수 있지만, "
                "내적 신앙(inward persuasion)은 바꿀 수 없다. 구원에 필요한 것은 진정한 신앙이다. "
                "셋째, 교회의 본질 논증: 교회는 자발적 결사체이므로 "
                "강제력이 아니라 설득과 권고만을 사용해야 한다. "
                "그러나 로크는 무신론자와 교황에 충성하는 가톨릭교도에 대해서는 관용을 거부했다."
            ),
            "argument": (
                "(1) 정부는 시민적 이익(생명, 자유, 건강, 재산)을 보호하기 위해 수립되었다. "
                "(2) 영혼의 구원은 시민적 이익에 포함되지 않는다. "
                "(3) 따라서 정부는 종교적 문제에 관할이 없다(관할권 논증). "
                "(4) 설사 정부가 관할이 있더라도, 강제력은 진정한 신앙을 만들 수 없다(비효과성 논증). "
                "(5) 교회는 자발적으로 결합한 사람들의 모임이며, "
                "탈퇴의 자유가 보장되어야 한다(교회의 본질 논증). "
                "(6) 그러나 관용의 한계: 무신론자는 맹세의 기반인 신을 부정하므로 사회적 신뢰를 훼손하고, "
                "외국 군주에 충성하는 자는 이중 충성의 위험이 있다."
            ),
            "counterpoint": (
                "토마스 홉스는 '리바이어던'(1651) 제3~4부에서 주권자가 종교적 문제에도 "
                "최종 결정권을 가져야 한다고 주장했다. 종교적 갈등이 내전의 주요 원인이었으므로, "
                "종교를 주권자의 통제 하에 두어야 평화가 유지된다. "
                "피에르 벨(Pierre Bayle)은 '역사적·비판적 사전'(Dictionnaire historique et critique, 1697)에서 "
                "로크보다 더 급진적으로 무신론자에 대한 관용까지 옹호하여, "
                "로크 관용론의 한계(무신론 배제)를 넘어섰다."
            ),
            "context": (
                "17세기 유럽의 종교전쟁(30년전쟁, 1618~1648), 영국의 청교도 혁명과 "
                "가톨릭-프로테스탄트 갈등이 로크 관용론의 직접적 배경이다. "
                "네덜란드 망명 시기(1683~1689)에 경험한 네덜란드의 종교적 관용이 "
                "이 저작의 집필에 영향을 미쳤다."
            ),
            "keywords": ["관용", "교회와 국가의 분리", "시민적 이익", "양심의 자유"],
            "verified": False
        },
        # CLAIM-010: 타불라 라사 — 본유관념 비판
        {
            "id": "locke-claim-010",
            "thinker_id": "locke",
            "work_id": "locke-essay",
            "source_detail": "An Essay Concerning Human Understanding, Book I, Chapters 2-4; Book II, Chapter 1",
            "claim": (
                "인간의 마음은 태어날 때 백지(tabula rasa, white paper)와 같으며, "
                "본유관념(innate ideas)은 존재하지 않는다. "
                "모든 관념은 감각(sensation)과 반성(reflection)이라는 두 가지 경험에서 비롯된다."
            ),
            "original_text": (
                "Let us then suppose the mind to be, as we say, white paper, void of all characters, "
                "without any ideas: — How comes it to be furnished? Whence comes it by that vast store "
                "which the busy and boundless fancy of man has painted on it with an almost endless variety? "
                "Whence has it all the materials of reason and knowledge? "
                "To this I answer, in one word, from EXPERIENCE."
            ),
            "original_text_ko": (
                "그러면 마음이, 우리가 말하듯이, 모든 문자가 없고, 어떤 관념도 없는 "
                "백지(white paper)라고 가정하자. 어떻게 마음은 채워지는가? "
                "인간의 바쁘고 한계 없는 상상력이 거의 끝없는 다양함으로 "
                "거기에 그린 그 방대한 저장은 어디서 오는가? "
                "이성과 지식의 모든 재료는 어디서 오는가? "
                "이에 대해 나는 한 단어로 답한다: 경험(EXPERIENCE)으로부터."
            ),
            "explanation": (
                "타불라 라사 개념은 로크 인식론의 출발점이자 그의 정치철학의 인간학적 토대이다. "
                "본유관념 비판의 정치적 함의: 모든 인간이 동일한 백지에서 출발한다면, "
                "선천적 신분이나 특권은 정당화될 수 없다. 이는 로크의 평등주의와 직결된다. "
                "로크는 데카르트(Descartes), 허버트 오브 체르베리(Herbert of Cherbury) 등의 "
                "본유관념론을 세 가지 유형으로 분류하여 반박한다: "
                "(1) 보편적 동의(universal consent) 논증 비판: 사실상 보편적 동의가 존재하지 않는다. "
                "(2) 어린이와 백치도 가지고 있다는 주장 비판: 그들은 해당 관념을 알지 못한다. "
                "(3) 실천적(도덕적) 본유관념 비판: 도덕 원칙도 문화마다 다르다."
            ),
            "argument": (
                "(1) 본유관념론자들은 '어떤 원리는 보편적으로 동의된다'고 주장한다. "
                "(2) 그러나 보편적 동의는 존재하지 않는다: 어린이, 백치, 문맹자는 "
                "'존재하는 것은 무엇이든 존재한다(whatever is, is)' 같은 원리도 알지 못한다. "
                "(3) '잠재적으로 가지고 있다(potential innate)'고 하면, "
                "결국 경험을 통해 발견한다는 것이므로 본유관념론이 아니다. "
                "(4) 실천적(도덕적) 원리도 문화마다 다르므로 보편적 본유가 아니다. "
                "(5) 따라서 마음은 경험 이전에 비어 있으며(tabula rasa), "
                "모든 관념은 감각(외적 경험)과 반성(내적 경험)에서 비롯된다."
            ),
            "counterpoint": (
                "르네 데카르트(René Descartes)는 '성찰'(Meditationes de Prima Philosophia, 1641) "
                "제3성찰에서 신(God)의 관념은 본유적(innate)이라고 주장했다. "
                "신의 관념은 경험에서 도출될 수 없을 만큼 완전하므로, "
                "신이 인간의 마음에 각인한 것이라는 것이다. "
                "라이프니츠(G.W. Leibniz)는 '인간오성신론'(Nouveaux Essais sur l'entendement humain, 1704/1765)에서 "
                "로크의 백지설을 직접 반박하며, 마음은 '무늬 있는 대리석(veined marble)'과 같아서 "
                "경험 이전에 이미 구조(성향, 경향성)가 있다고 주장했다. "
                "노엄 촘스키(Noam Chomsky)는 현대에 '보편 문법(Universal Grammar)'을 제시하여 "
                "언어 능력이 본유적이라는 합리론적 입장을 부활시켰다."
            ),
            "context": (
                "로크의 본유관념 비판은 17세기 합리론(데카르트, 라이프니츠)과 "
                "경험론(베이컨, 홉스, 로크) 사이의 인식론 논쟁의 맥락에 있다. "
                "또한 종교적 권위주의에 대한 비판이기도 하다: "
                "본유관념이 없다면, 어떤 종교적·정치적 원리도 '자명한 진리'로서 "
                "강요될 수 없다."
            ),
            "keywords": ["타불라 라사", "본유관념 비판", "경험론", "감각", "반성"],
            "verified": False
        },
        # CLAIM-011: 입법권의 우위 — 정부 내 최고 권력
        {
            "id": "locke-claim-011",
            "thinker_id": "locke",
            "work_id": "locke-second-treatise",
            "source_detail": "Second Treatise, Chapter 11, §134; Chapter 13, §149-152",
            "claim": (
                "입법권(legislative power)은 커먼웰스에서 최고 권력(supreme power)이다. "
                "법을 만드는 자가 사회에서 최고이기 때문이다. "
                "그러나 입법권도 인민의 신탁(trust)에 의해 제약되며, "
                "인민의 최고 권력(supreme power of the people)은 입법권 위에 있다."
            ),
            "original_text": (
                "There can be but one supreme power, which is the legislative, "
                "to which all the rest are and must be subordinate; yet the legislative being only "
                "a fiduciary power to act for certain ends, there remains still in the people "
                "a supreme power to remove or alter the legislative."
            ),
            "original_text_ko": (
                "최고 권력은 하나만 있을 수 있으며, 그것은 입법권이다. "
                "나머지 모든 것은 이에 종속되어야 한다. "
                "그러나 입법부가 특정 목적을 위해 행위하도록 위임된 수탁적 권력에 불과하므로, "
                "입법부를 제거하거나 변경할 최고 권력이 여전히 인민에게 남아 있다."
            ),
            "explanation": (
                "로크의 '입법권의 우위' 원칙은 두 층위로 작동한다. "
                "첫째, 정부 기관들 사이에서 입법권이 집행권보다 우위에 있다. "
                "법을 만드는 자가 법을 집행하는 자보다 상위이다. "
                "둘째, 그러나 입법권 자체도 인민의 신탁에 의해 제약된다. "
                "인민의 최고 권력은 입법권 위에 있으며, "
                "입법부가 신탁을 위반하면 인민이 입법부를 교체할 수 있다. "
                "이것이 로크의 인민주권론이며, 저항권의 이론적 근거이다."
            ),
            "argument": (
                "(1) 사회에 법을 줄 수 있는 자가 그 사회에서 최고이다. "
                "(2) 입법권은 법을 만드는 권력이므로 최고 권력이다. "
                "(3) 집행권은 법률을 시행하는 것이므로 입법권에 종속된다. "
                "(4) 그러나 입법권도 수탁적 권력(fiduciary power)에 불과하다. "
                "(5) 신탁의 설정자(인민)가 수탁자(입법부)보다 궁극적으로 우위에 있다. "
                "(6) 따라서 '인민의 최고 권력 > 입법권 > 집행권'의 위계가 성립한다."
            ),
            "counterpoint": (
                "홉스는 '리바이어던'(1651) 제18장에서 주권자(입법자)의 권력은 절대적이며 "
                "인민에 의해 제거될 수 없다고 주장했다. 신민은 주권자의 행위를 "
                "자기 자신의 행위로 인정(authorize)했으므로, "
                "주권자를 처벌하는 것은 자기 자신을 처벌하는 것이다. "
                "오스틴(John Austin)은 '법학의 범위 결정'(The Province of Jurisprudence Determined, 1832)에서 "
                "주권자를 '습관적으로 복종받는 우월자'로 정의하여, "
                "주권자에 대한 법적 제한이라는 관념 자체를 거부했다."
            ),
            "context": (
                "영국 의회가 국왕의 권력을 제한해온 역사적 전통(매그나 카르타, 권리청원, 명예혁명)이 "
                "로크의 입법권 우위론의 배경이다. "
                "명예혁명 이후 의회 주권(parliamentary sovereignty)의 원칙이 확립되었으며, "
                "로크의 이론은 이 원칙의 철학적 토대로 기능했다."
            ),
            "keywords": ["입법권의 우위", "인민주권", "수탁적 권력", "최고 권력"],
            "verified": False
        },
        # CLAIM-012: 재산권의 불가침 — 동의 없는 과세 금지
        {
            "id": "locke-claim-012",
            "thinker_id": "locke",
            "work_id": "locke-second-treatise",
            "source_detail": "Second Treatise, Chapter 11, §138-140",
            "claim": (
                "정부는 인민 또는 그 대표자의 동의 없이 재산(property)에 대해 과세할 수 없다. "
                "재산권은 자연법에 의한 것이며, 정부의 목적이 재산 보호인 이상 "
                "정부가 동의 없이 재산을 빼앗는 것은 자기 모순이다."
            ),
            "original_text": (
                "'Tis true, governments cannot be supported without great charge, "
                "and it is fit every one who enjoys his share of the protection, "
                "should pay out of his estate his proportion for the maintenance of it. "
                "But still it must be with his own consent, i.e. the consent of the majority, "
                "giving it either by themselves, or their representatives chosen by them."
            ),
            "original_text_ko": (
                "정부는 큰 비용 없이 유지될 수 없다는 것은 사실이며, "
                "보호의 몫을 향유하는 모든 사람이 그것의 유지를 위해 "
                "자신의 재산에서 비례분을 지불해야 하는 것이 적절하다. "
                "그러나 여전히 그것은 자신의 동의, 즉 다수의 동의에 의해서여야 하며, "
                "그것은 그들 스스로 또는 그들이 선출한 대표자를 통해 이루어져야 한다."
            ),
            "explanation": (
                "이 원칙은 '대표 없이 과세 없다(no taxation without representation)'의 "
                "직접적 철학적 근거이다. 로크에게 재산권은 정부 이전에 자연법에 의해 존재하며, "
                "정부의 목적 자체가 재산 보호이다. 따라서 정부가 동의 없이 재산을 빼앗는 것은 "
                "정부 존립 목적에 모순된다. "
                "이 원칙은 영국 의회의 과세 동의권의 이론적 토대이며, "
                "이후 미국 독립혁명의 핵심 슬로건으로 이어졌다."
            ),
            "argument": (
                "(1) 재산권은 자연법에 의해 정부 이전에 존재한다. "
                "(2) 인간이 정치 사회에 들어간 목적은 재산의 보호이다. "
                "(3) 정부가 동의 없이 재산을 빼앗는 것은 그 목적에 모순된다. "
                "(4) 과세는 재산의 일부를 가져가는 것이므로, "
                "반드시 인민 또는 그 대표자의 동의를 요한다. "
                "(5) 이 동의는 다수결에 의해 표현될 수 있으며, "
                "인민이 직접 또는 선출된 대표자를 통해 행사한다."
            ),
            "counterpoint": (
                "홉스는 '리바이어던'(1651) 제18장에서 주권자는 과세를 포함한 모든 공적 권한을 "
                "개별 동의 없이 행사할 수 있다고 주장했다. 사회계약에서 신민은 이미 "
                "주권자의 모든 행위를 자기 행위로 인정(authorize)했기 때문이다. "
                "현대적 관점에서는 국방, 복지 등 공공재의 제공을 위해 "
                "과세가 불가피하며, 개인의 동의를 일일이 구하는 것이 비현실적이라는 "
                "실용주의적 비판이 있다."
            ),
            "context": (
                "1628년 권리청원(Petition of Right)에서 확인된 '의회 동의 없는 과세 금지' 원칙이 "
                "로크의 논증에 역사적 근거를 제공한다. "
                "이후 1765년 인지세법(Stamp Act)에 대한 미국 식민지인들의 반발은 "
                "로크의 이 원칙에 직접 호소했다."
            ),
            "keywords": ["재산권 불가침", "동의 없는 과세 금지", "대표 없이 과세 없다"],
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """로크 키워드 데이터 입력."""
    keywords = [
        {
            "id": "locke-kw-001",
            "thinker_id": "locke",
            "term": "자연 상태 (State of Nature)",
            "term_original": "state of nature",
            "definition": (
                "로크에게 자연 상태는 자연법(이성)이 지배하는 자유와 평등의 상태이다. "
                "홉스의 '만인에 대한 만인의 투쟁'과 달리, 로크의 자연 상태에서 인간은 "
                "이성의 인도를 받아 타인의 생명, 자유, 재산을 존중할 수 있다. "
                "자연 상태의 불편함(확립된 법률, 공인된 재판관, 집행 권력의 부재)이 "
                "정치 사회로의 이행 동기가 된다."
            ),
            "related_claims": ["locke-claim-001"],
            "source": "Second Treatise, Chapter 2"
        },
        {
            "id": "locke-kw-002",
            "thinker_id": "locke",
            "term": "자연권 (Natural Rights)",
            "term_original": "natural rights (life, liberty, property)",
            "definition": (
                "자연법에 의해 모든 인간에게 부여된 양도 불가능한 권리: "
                "생명(life), 자유(liberty), 재산(property). "
                "로크는 이 세 가지를 넓은 의미의 'property'로 포괄하기도 한다. "
                "정부의 존재 이유는 이 자연권의 보호이며, "
                "홉스의 '모든 것에 대한 무제한적 권리'와 달리 자연법에 의해 처음부터 제한된다."
            ),
            "related_claims": ["locke-claim-002", "locke-claim-012"],
            "source": "Second Treatise, Chapters 2, 5, 9"
        },
        {
            "id": "locke-kw-003",
            "thinker_id": "locke",
            "term": "사회계약 / 동의 (Social Contract / Consent)",
            "term_original": "social compact / consent",
            "definition": (
                "자유로운 개인들이 자발적 동의에 의해 정치 사회를 형성하는 합의. "
                "홉스와 달리 개인은 자연권 전체가 아니라 자연법 집행권만 양도한다. "
                "정부는 인민의 신탁(trust)을 받은 수탁자의 지위에 있다. "
                "동의는 명시적 동의와 묵시적 동의로 구분된다."
            ),
            "related_claims": ["locke-claim-003", "locke-claim-007"],
            "source": "Second Treatise, Chapters 8-9"
        },
        {
            "id": "locke-kw-004",
            "thinker_id": "locke",
            "term": "신탁 (Trust)",
            "term_original": "trust / fiduciary power",
            "definition": (
                "로크 사회계약론의 핵심 개념으로, 정부의 권력이 인민으로부터 "
                "특정 목적(자연권 보호)을 위해 위임된 것임을 나타낸다. "
                "정부는 수탁자(trustee)이며, 인민은 신탁 설정자(settlor)이다. "
                "신탁 위반 시 권력은 인민에게 귀속되며, 이것이 저항권의 근거이다."
            ),
            "related_claims": ["locke-claim-003", "locke-claim-004", "locke-claim-011"],
            "source": "Second Treatise, Chapters 13, 19"
        },
        {
            "id": "locke-kw-005",
            "thinker_id": "locke",
            "term": "저항권 (Right of Resistance)",
            "term_original": "right of resistance / right of revolution",
            "definition": (
                "정부가 인민의 신탁을 위반하여 자연권을 침해할 때, "
                "인민이 정부를 해체하고 새로운 정부를 수립할 수 있는 권리. "
                "로크에 따르면 폭정에 대한 저항은 반란이 아니라, "
                "오히려 신탁을 위반한 통치자가 진정한 반란자이다."
            ),
            "related_claims": ["locke-claim-004"],
            "source": "Second Treatise, Chapter 19"
        },
        {
            "id": "locke-kw-006",
            "thinker_id": "locke",
            "term": "타불라 라사 (Tabula Rasa)",
            "term_original": "tabula rasa / white paper",
            "definition": (
                "인간의 마음이 태어날 때 백지 상태라는 인식론적 개념. "
                "본유관념(innate ideas)을 부정하고, 모든 지식이 경험에서 비롯된다고 주장한다. "
                "감각(sensation)과 반성(reflection)이 관념의 두 원천이다. "
                "정치적 함의: 선천적 신분이나 특권의 정당화 근거를 제거하고 "
                "교육의 결정적 역할을 강조한다."
            ),
            "related_claims": ["locke-claim-010"],
            "source": "An Essay Concerning Human Understanding, Book II, Chapter 1"
        },
        {
            "id": "locke-kw-007",
            "thinker_id": "locke",
            "term": "소유권 노동이론 (Labor Theory of Property)",
            "term_original": "labor theory of property",
            "definition": (
                "자연물에 자신의 노동을 섞으면(mix labour) 소유가 된다는 로크의 소유권 정당화 이론. "
                "각 개인의 자기 인신(person)에 대한 소유권에서 출발하여, "
                "노동을 통한 전유(appropriation)를 정당화한다. "
                "두 가지 제한: 충분조건(enough and as good)과 부패조건(spoilage proviso). "
                "화폐의 발명이 축적의 제한을 극복하게 한다."
            ),
            "related_claims": ["locke-claim-006"],
            "source": "Second Treatise, Chapter 5"
        },
        {
            "id": "locke-kw-008",
            "thinker_id": "locke",
            "term": "관용 (Toleration)",
            "term_original": "toleration",
            "definition": (
                "국가가 종교적 신앙과 예배에 강제력을 행사해서는 안 된다는 원칙. "
                "정부의 관할은 시민적 이익에 한정되며, 영혼의 구원은 정부의 권한 밖이다. "
                "교회는 자발적 결사체로서 강제력이 아닌 설득만을 사용해야 한다. "
                "로크는 무신론자와 외국 군주에 충성하는 자에 대해서는 관용을 거부했다."
            ),
            "related_claims": ["locke-claim-009"],
            "source": "A Letter Concerning Toleration"
        },
        {
            "id": "locke-kw-009",
            "thinker_id": "locke",
            "term": "제한적 정부 (Limited Government)",
            "term_original": "limited government / constitutionalism",
            "definition": (
                "정부의 권력이 자연법과 인민의 신탁에 의해 본질적으로 제한된다는 원칙. "
                "입법부조차도 자의적 권력 행사 금지, 확립된 법률에 의한 통치, "
                "동의 없는 과세 금지, 입법권 위임 금지 등에 구속된다. "
                "홉스의 절대주권론에 대립하며, 근대 입헌주의(constitutionalism)의 토대가 된다."
            ),
            "related_claims": ["locke-claim-005", "locke-claim-008", "locke-claim-012"],
            "source": "Second Treatise, Chapters 11-14"
        },
        {
            "id": "locke-kw-010",
            "thinker_id": "locke",
            "term": "동의에 의한 정부 (Government by Consent)",
            "term_original": "government by consent",
            "definition": (
                "정치 권력의 정당성은 오직 피치자의 자발적 동의에만 기초한다는 원칙. "
                "필머(Filmer)의 왕권신수설에 반대하여, 어떤 정부도 인민의 동의 없이는 "
                "정당하게 수립될 수 없다고 주장한다. "
                "명시적 동의(express consent)와 묵시적 동의(tacit consent)로 구분되며, "
                "현대 민주주의의 '피치자의 동의(consent of the governed)' 원칙의 원류이다."
            ),
            "related_claims": ["locke-claim-003", "locke-claim-007"],
            "source": "Second Treatise, Chapter 8"
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """로크 관계 데이터 입력."""
    relations = [
        {
            "id": "relation-hobbes-locke",
            "from_thinker": "hobbes",
            "to_thinker": "locke",
            "type": "influenced",
            "description": (
                "홉스의 자연 상태론과 사회계약론은 로크에게 직접적 영향을 미쳤다. "
                "로크는 홉스의 문제 설정(자연 상태에서 정치 사회로의 이행)을 수용하면서도, "
                "자연 상태를 전쟁 상태가 아니라 자연법이 지배하는 상태로, "
                "주권자를 절대적 존재가 아니라 인민의 신탁을 받은 존재로 재해석했다. "
                "홉스의 절대주권론에 대한 비판적 계승이다."
            ),
            "strength": "강함",
            "period": "17세기"
        },
        {
            "id": "relation-locke-rousseau",
            "from_thinker": "locke",
            "to_thinker": "rousseau",
            "type": "influenced",
            "description": (
                "루소는 로크의 사회계약론과 자연 상태론에서 직접적 영향을 받았다. "
                "그러나 루소는 로크의 소유권 중심 정치학을 비판하며, "
                "'인간 불평등 기원론'(1755)에서 사유재산이 불평등의 원천이라고 주장했다. "
                "'사회계약론'(1762)에서는 로크의 대의제 대신 직접 민주주의와 "
                "일반의지(volonté générale)에 기초한 주권론을 전개했다."
            ),
            "strength": "강함",
            "period": "18세기"
        },
        {
            "id": "relation-locke-montesquieu",
            "from_thinker": "locke",
            "to_thinker": "montesquieu",
            "type": "influenced",
            "description": (
                "몽테스키외는 '법의 정신'(1748) 제11권에서 로크의 권력 분립론을 발전시켜 "
                "입법, 행정, 사법의 삼권분립을 체계화했다. "
                "로크가 입법권과 집행권의 분리를 논한 반면, "
                "몽테스키외는 사법권을 독립된 권력으로 분리하고 "
                "권력 간의 상호 견제(checks and balances)를 강조했다."
            ),
            "strength": "강함",
            "period": "18세기"
        },
        {
            "id": "relation-locke-american-founders",
            "from_thinker": "locke",
            "to_thinker": "jefferson",
            "type": "influenced",
            "description": (
                "로크의 자연권론, 동의 이론, 저항권은 미국 독립선언서(1776)에 직접적 영향을 미쳤다. "
                "토마스 제퍼슨(Thomas Jefferson)은 독립선언서에서 '생명, 자유, 행복의 추구'라는 "
                "양도 불가능한 권리와, 정부가 이 권리를 침해할 때 인민이 정부를 변경할 권리를 선언했는데, "
                "이는 로크의 자연권 개념과 저항권 이론의 거의 직접적 차용이다."
            ),
            "strength": "강함",
            "period": "18세기"
        },
        {
            "id": "relation-locke-kant",
            "from_thinker": "locke",
            "to_thinker": "kant",
            "type": "influenced",
            "description": (
                "칸트는 로크의 경험주의 인식론에 영향을 받아 '순수이성비판'(1781)에서 "
                "'경험 없이는 지식이 없다'는 명제를 수용하되, "
                "경험 이전의 선험적(a priori) 인식 형식을 주장하여 "
                "로크의 백지설과 데카르트의 본유관념론을 종합했다. "
                "정치적으로도 칸트는 로크의 동의 이론과 공화주의적 정부관에서 영향을 받았다."
            ),
            "strength": "보통",
            "period": "18세기"
        }
    ]

    for rel in relations:
        result = client.index(index=INDEX_RELATIONS, id=rel["id"], document=rel)
        print(f"[relation] {rel['id']}: {result['result']}")

    return len(relations)


def verify_data(client):
    """입력된 데이터를 전수 확인."""
    print("\n=== 전수 확인 ===")

    # thinker 확인
    r = client.get(index=INDEX_THINKERS, id="locke")
    print(f"[thinker] locke: name={r['_source']['name_en']}, era={r['_source']['era']}, field={r['_source']['field']}")

    # field 확인
    try:
        f = client.get(index=INDEX_FIELDS, id="political_philosophy")
        print(f"[field] political_philosophy: name={f['_source']['name']}")
    except Exception:
        print("[field] political_philosophy: NOT FOUND")

    # works 확인
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "locke"}})
    print(f"[works] locke 저서 수: {works_count['count']}")
    works_result = client.search(
        index=INDEX_WORKS,
        query={"term": {"thinker_id": "locke"}},
        _source=["id", "title_original", "year"],
        size=10
    )
    for hit in works_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['title_original']} ({s['year']})")

    # claims 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "locke"}})
    print(f"[claims] locke 주장 수: {claims_count['count']}")
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "locke"}},
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
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "locke"}})
    print(f"[keywords] locke 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_count = client.count(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "locke"}},
            {"term": {"to_thinker": "locke"}}
        ]}}
    )
    print(f"[relations] locke 관련 관계 수: {rel_count['count']}")
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "locke"}},
            {"term": {"to_thinker": "locke"}}
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
        print("=== 존 로크(John Locke) 데이터 입력 시작 ===\n")

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
