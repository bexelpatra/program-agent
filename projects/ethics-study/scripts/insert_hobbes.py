"""토머스 홉스(Thomas Hobbes) 데이터를 ES에 직접 입력하는 스크립트."""

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
    """홉스 사상가 데이터 입력."""
    doc = {
        "id": "hobbes",
        "name": "토머스 홉스",
        "name_en": "Thomas Hobbes",
        "field": "political_philosophy",
        "era": "근대 초기",
        "birth_year": 1588,
        "death_year": 1679,
        "background": (
            "영국 웨스트포트(Westport, Malmesbury)에서 성직자의 아들로 태어났다. "
            "옥스퍼드 대학교 모들린 홀(Magdalen Hall)에서 스콜라 철학을 배웠으나 "
            "이에 만족하지 못하고, 캐번디시(Cavendish) 가문의 가정교사로 활동하며 "
            "유럽 대륙 여행(Grand Tour)을 통해 갈릴레오, 가상디(Gassendi), 메르센(Mersenne) 등 "
            "당대 최고의 과학자·철학자들과 교류했다. "
            "영국 내전(English Civil War, 1642~1651)의 경험이 그의 정치철학에 결정적 영향을 미쳤으며, "
            "전쟁과 무질서의 공포가 강력한 주권 국가의 필요성에 대한 확신으로 이어졌다. "
            "1640년 파리로 망명하여 약 11년간 체류하며 '리바이어던'을 집필했고, "
            "1651년 귀국 후 크롬웰 정권과 왕정복고 모두에서 살아남아 91세까지 장수했다."
        ),
        "core_philosophy": (
            "홉스의 핵심 사상은 기하학적 방법(geometrical method)에 기초한 정치학의 과학적 정초이다. "
            "인간은 본성상 자기보존(self-preservation)을 추구하는 존재이며, "
            "자연 상태(state of nature)에서는 공통의 권력이 없어 '만인에 대한 만인의 투쟁(bellum omnium contra omnes)'이 "
            "벌어진다. 이 상태에서 삶은 '고독하고, 가난하고, 험악하고, 잔인하고, 짧다(solitary, poor, nasty, brutish, and short).' "
            "이성은 자연법(laws of nature)을 발견하게 하며, 그 첫째는 평화를 추구하라는 것이다. "
            "자연법의 실현을 위해 개인들은 사회계약을 통해 자신의 자연권을 하나의 주권자(sovereign)에게 양도하고, "
            "이로써 커먼웰스(Commonwealth, 국가)가 탄생한다. 주권자는 절대적 권위를 가지며, "
            "이 권위의 분할은 곧 자연 상태로의 회귀를 의미한다."
        ),
        "philosophical_journey": (
            "초기(~1630년대): 투키디데스의 '펠로폰네소스 전쟁사' 번역(1629)을 통해 정치적 관심을 키웠다. "
            "유클리드 기하학에 매료되어 기하학적 방법을 철학에 적용하려는 야심을 품었다. "
            "중기(1640~1651): 영국 내전의 혼란 속에서 파리로 망명하여 정치철학 체계를 완성했다. "
            "'법의 원리'(The Elements of Law, 1640, 필사본 유통), "
            "'시민론'(De Cive, 1642)을 거쳐 대작 '리바이어던'(Leviathan, 1651)을 출간했다. "
            "후기(1651~1679): 귀국 후 '물체론'(De Corpore, 1655), '인간론'(De Homine, 1658)을 출간하여 "
            "물체·인간·시민(De Corpore-De Homine-De Cive)으로 이루어진 철학 체계를 완성했다. "
            "말년에는 수학 논쟁(원의 구적법)에 몰두하고, 호메로스 번역을 하며 91세까지 활동했다."
        ),
        "keywords": [
            "자연 상태",
            "만인에 대한 만인의 투쟁",
            "사회계약",
            "주권자(sovereign)",
            "리바이어던",
            "자연법",
            "자연권",
            "자기보존",
            "커먼웰스",
            "절대주권"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="hobbes", document=doc)
    print(f"[thinker] hobbes: {result['result']}")
    return result


def insert_works(client):
    """홉스 저서 데이터 입력."""
    works = [
        {
            "id": "hobbes-leviathan",
            "thinker_id": "hobbes",
            "title": "리바이어던",
            "title_original": "Leviathan, or The Matter, Forme and Power of a Commonwealth Ecclesiasticall and Civil",
            "year": 1651,
            "significance": (
                "홉스 정치철학의 대표작이자 서양 정치사상사에서 가장 중요한 저작 중 하나. "
                "자연 상태, 자연법, 사회계약, 주권자론, 커먼웰스의 구조를 체계적으로 전개한다. "
                "4부로 구성: 제1부 '인간에 관하여(Of Man)' — 인간 본성과 자연 상태, "
                "제2부 '커먼웰스에 관하여(Of Commonwealth)' — 주권과 국가 구조, "
                "제3부 '기독교 커먼웰스에 관하여' — 종교와 국가의 관계, "
                "제4부 '어둠의 왕국에 관하여' — 교회 권력 비판. "
                "표지의 거대한 인공 인간(리바이어던) 이미지는 주권자가 인민의 신체로 구성됨을 상징한다."
            ),
            "key_concepts": [
                "자연 상태", "만인에 대한 만인의 투쟁", "자연법", "사회계약",
                "주권자", "커먼웰스", "대리(authorization)", "자기보존"
            ]
        },
        {
            "id": "hobbes-de-cive",
            "thinker_id": "hobbes",
            "title": "시민론",
            "title_original": "De Cive (Philosophical Rudiments Concerning Government and Society)",
            "year": 1642,
            "significance": (
                "홉스 정치철학 체계(De Corpore-De Homine-De Cive 삼부작)의 세 번째이자 "
                "가장 먼저 출간된 저작. 리바이어던의 핵심 논증이 더 간결하게 전개되어 있다. "
                "3부 구성: 제1부 '자유(Liberty)' — 자연 상태와 자연법, "
                "제2부 '통치(Dominion)' — 주권의 근거와 구조, "
                "제3부 '종교(Religion)' — 종교와 국가 권력의 관계. "
                "라틴어로 먼저 출간(1642)된 후 영어판(1651)이 나왔다."
            ),
            "key_concepts": [
                "자연 상태", "자연법", "주권", "신민의 의무", "종교와 국가"
            ]
        },
        {
            "id": "hobbes-de-corpore",
            "thinker_id": "hobbes",
            "title": "물체론",
            "title_original": "De Corpore (Concerning Body)",
            "year": 1655,
            "significance": (
                "홉스 철학 체계 삼부작의 제1부로, 형이상학·자연철학의 토대를 다룬다. "
                "기하학적 방법을 철학 전체에 적용하려는 홉스의 야심이 담긴 저작이다. "
                "물체(body)와 운동(motion)을 존재의 근본 원리로 삼는 유물론적 형이상학을 전개하며, "
                "감각, 상상, 추론의 메커니즘을 물질적 운동으로 설명한다. "
                "이 유물론이 홉스 정치철학의 자연주의적 인간관의 토대가 된다."
            ),
            "key_concepts": [
                "유물론", "기하학적 방법", "물체와 운동", "감각 이론", "인과론"
            ]
        },
        {
            "id": "hobbes-de-homine",
            "thinker_id": "hobbes",
            "title": "인간론",
            "title_original": "De Homine (Concerning Man)",
            "year": 1658,
            "significance": (
                "홉스 철학 체계 삼부작의 제2부로, 인간의 본성을 다룬다. "
                "광학(optics)과 감각 이론에 상당 부분을 할애하며, "
                "인간의 정념(passions), 언어, 이성, 종교적 본성 등을 논한다. "
                "리바이어던 제1부의 인간론과 유사하지만, "
                "더 체계적인 자연철학적 맥락에서 전개된다. "
                "삼부작 중 가장 덜 알려져 있으나, 홉스의 인간 본성론의 자연주의적 기초를 보여준다."
            ),
            "key_concepts": [
                "감각과 광학", "정념(passions)", "인간 본성", "언어와 이성"
            ]
        },
        {
            "id": "hobbes-elements-of-law",
            "thinker_id": "hobbes",
            "title": "법의 원리",
            "title_original": "The Elements of Law, Natural and Politic",
            "year": 1640,
            "significance": (
                "홉스 정치철학의 최초 체계적 저술로, 필사본으로 유통되었다(출판은 1650년). "
                "자연 상태, 자연법, 사회계약의 기본 논증이 처음으로 전개된다. "
                "두 부분으로 구성: 제1부 '인간 본성(Human Nature)' — 감각, 정념, 이성, "
                "제2부 '정치체(De Corpore Politico)' — 국가의 기원과 권력. "
                "영국 내전 직전(1640년 장기의회 소집)에 왕당파 입장을 담아 작성되었으며, "
                "이로 인해 홉스는 신변 위협을 느끼고 프랑스로 망명했다."
            ),
            "key_concepts": [
                "인간 본성", "자연 상태", "자연법", "사회계약", "주권"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """홉스 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 자연 상태 — 만인에 대한 만인의 투쟁
        {
            "id": "hobbes-claim-001",
            "thinker_id": "hobbes",
            "work_id": "hobbes-leviathan",
            "source_detail": "Leviathan, Part I, Chapter 13",
            "claim": (
                "공통의 권력(common power)이 없는 자연 상태(state of nature)에서 인간은 "
                "'만인에 대한 만인의 투쟁(war of every man against every man)' 상태에 놓인다. "
                "이 상태에서 삶은 '고독하고, 가난하고, 험악하고, 잔인하고, 짧다"
                "(solitary, poor, nasty, brutish, and short).'"
            ),
            "original_text": (
                "Whatsoever therefore is consequent to a time of war, where every man is enemy to every man, "
                "the same consequent to the time wherein men live without other security than what their own "
                "strength and their own invention shall furnish them withal. In such condition there is no place "
                "for industry... and the life of man, solitary, poor, nasty, brutish, and short."
            ),
            "original_text_ko": (
                "그러므로 모든 사람이 모든 사람의 적인 전쟁 상태에 수반되는 것은, "
                "자신의 힘과 발명 이외에는 어떤 안전보장도 없이 사는 시대에도 동일하게 수반된다. "
                "이런 상태에서는 산업을 위한 자리가 없으며... 인간의 삶은 고독하고, 가난하고, "
                "험악하고, 잔인하고, 짧다."
            ),
            "explanation": (
                "홉스의 자연 상태는 역사적 사실이라기보다 논리적 가설이다. "
                "공통 권력이 부재할 때 인간 본성—경쟁(competition), 불신(diffidence), 영광(glory)—이 "
                "어떤 결과를 낳는지를 보여주는 사고실험이다. "
                "인간은 자연적으로 대략 평등하여(신체적·정신적 능력에서), "
                "누구도 타인을 완전히 지배할 수 없고, 가장 약한 자도 연합이나 계략으로 "
                "가장 강한 자를 죽일 수 있다. 이 평등이 상호 불신을 낳고, "
                "불신이 선제공격의 합리성을 만들어 전쟁 상태로 귀결된다."
            ),
            "argument": (
                "(1) 인간은 신체적·정신적 능력에서 대략적으로 평등하다(natural equality). "
                "(2) 능력의 평등에서 희망의 평등이 나온다: 누구나 원하는 것을 얻을 수 있다고 기대한다. "
                "(3) 같은 것을 원하는 둘이 있을 때 서로 적이 된다(경쟁, competition). "
                "(4) 적의 존재는 상호 불신(diffidence)을 낳고, 선제공격이 합리적이 된다. "
                "(5) 일부는 정복 자체에서 즐거움을 느낀다(영광, glory). "
                "(6) 이 세 원인—경쟁, 불신, 영광—으로 인해 공통 권력이 없으면 전쟁 상태가 필연적이다. "
                "(7) 전쟁 상태에서는 산업, 문화, 지식, 사회가 불가능하며 삶은 비참하다."
            ),
            "counterpoint": (
                "존 로크(John Locke)는 '통치론 제2론'(Two Treatises of Government, Second Treatise, 1689) "
                "제2장에서 자연 상태는 전쟁 상태가 아니라 자연법이 지배하는 자유와 평등의 상태라고 반박했다. "
                "로크에 따르면 자연 상태에서도 이성(자연법)이 작동하여 생명, 자유, 재산의 상호 존중이 가능하며, "
                "홉스는 자연 상태와 전쟁 상태를 잘못 혼동했다. "
                "루소(Jean-Jacques Rousseau)는 '인간 불평등 기원론'(Discours sur l'origine de l'inégalité, 1755)에서 "
                "홉스가 문명화된 인간의 욕망(경쟁, 허영)을 자연인에게 잘못 투사했다고 비판했다. "
                "루소에 따르면 자연인은 자기보존과 동정심(pitié)만을 가진 고립된 존재이며, "
                "만인의 투쟁은 자연 상태가 아니라 부패한 사회의 모습이다."
            ),
            "context": (
                "영국 내전(1642~1651)의 경험이 홉스의 자연 상태론에 결정적 영향을 미쳤다. "
                "왕과 의회 사이의 권력 분쟁, 종교 갈등, 내전의 참상은 "
                "공통 권력이 붕괴하면 어떤 일이 벌어지는지를 생생하게 보여주었다. "
                "홉스에게 내전은 자연 상태의 현실적 사례였다."
            ),
            "keywords": ["자연 상태", "만인에 대한 만인의 투쟁", "경쟁", "불신", "영광"],
            "verified": False
        },
        # CLAIM-002: 자연권 — 자기보존의 권리
        {
            "id": "hobbes-claim-002",
            "thinker_id": "hobbes",
            "work_id": "hobbes-leviathan",
            "source_detail": "Leviathan, Part I, Chapter 14",
            "claim": (
                "자연권(right of nature, jus naturale)은 모든 사람이 자신의 생명을 보존하기 위해 "
                "자신의 힘을 자기가 원하는 대로 사용할 수 있는 자유이다. "
                "이 권리는 자연 상태에서 모든 것에 대한 권리(right to all things)를 포함한다."
            ),
            "original_text": (
                "The right of nature, which writers commonly call jus naturale, is the liberty each man hath "
                "to use his own power as he will himself for the preservation of his own nature; that is to say, "
                "of his own life; and consequently, of doing anything which, in his own judgement and reason, "
                "he shall conceive to be the aptest means thereunto."
            ),
            "original_text_ko": (
                "저술가들이 흔히 자연권(jus naturale)이라 부르는 자연의 권리란, "
                "각 사람이 자기 자신의 본성, 즉 자신의 생명을 보존하기 위해 "
                "자신의 힘을 자기가 원하는 대로 사용할 수 있는 자유이다. "
                "따라서 자신의 판단과 이성에서 그에 가장 적합한 수단이라고 생각되는 것은 "
                "무엇이든 할 수 있는 자유이다."
            ),
            "explanation": (
                "홉스에게 자연권은 자연법(law of nature)과 구별된다. "
                "자연권은 '자유(liberty)'이고, 자연법은 '의무(obligation)'이다. "
                "자연 상태에서 모든 사람은 자기보존을 위해 무엇이든 할 수 있는 권리를 가지는데, "
                "이것은 타인의 신체에 대한 권리까지 포함한다. "
                "이 무제한적 권리가 바로 만인에 대한 만인의 투쟁을 낳는 원인이기도 하다. "
                "평화를 위해서는 이 무제한적 자연권을 자발적으로 포기(renounce)하거나 "
                "양도(transfer)해야 한다."
            ),
            "argument": (
                "(1) 자연은 모든 사람에게 모든 것에 대한 권리를 부여했다. "
                "(2) 이 권리는 자기보존이라는 자연적 경향성(natural inclination)에 근거한다. "
                "(3) 자기보존을 위해 필요하다고 판단하는 것은 무엇이든 할 수 있는 자유가 자연권이다. "
                "(4) 그러나 모든 사람이 모든 것에 대한 권리를 가지면, "
                "아무도 안전하지 못하다(자연 상태의 비참함). "
                "(5) 따라서 이성(자연법)은 평화를 위해 이 권리의 일부를 포기할 것을 명한다."
            ),
            "counterpoint": (
                "로크는 '통치론 제2론'(1689) 제2장에서 자연권을 홉스와 다르게 규정했다. "
                "로크에게 자연권은 '모든 것에 대한 권리'가 아니라 "
                "생명(life), 자유(liberty), 재산(property)에 대한 제한된 권리이며, "
                "자연법에 의해 처음부터 제약된다. 자연법은 타인의 생명·자유·재산을 침해하지 말라고 명하므로, "
                "홉스처럼 자연권이 무제한적이라는 전제 자체가 잘못이다. "
                "루소는 '사회계약론'(Du Contrat Social, 1762) 제1권에서 "
                "진정한 자유는 자연적 자유(홉스의 자연권)가 아니라 "
                "시민적 자유(civil liberty)와 도덕적 자유(moral liberty)에 있다고 주장했다."
            ),
            "context": (
                "자연권 개념은 중세 자연법 전통(아퀴나스 등)에서 이어지지만, "
                "홉스는 이를 근본적으로 재해석했다. 아퀴나스에게 자연법은 "
                "영원법(eternal law)의 인간 이성에의 참여이지만, "
                "홉스에게 자연법은 자기보존이라는 세속적 목적에 봉사하는 이성의 명령이다."
            ),
            "keywords": ["자연권", "자기보존", "자유", "모든 것에 대한 권리"],
            "verified": False
        },
        # CLAIM-003: 자연법 — 이성의 명령
        {
            "id": "hobbes-claim-003",
            "thinker_id": "hobbes",
            "work_id": "hobbes-leviathan",
            "source_detail": "Leviathan, Part I, Chapters 14-15",
            "claim": (
                "자연법(law of nature, lex naturalis)은 이성에 의해 발견된 일반 규칙으로, "
                "자신의 생명에 파괴적인 것을 하지 말고, 생명 보존에 가장 좋다고 판단되는 수단을 "
                "포기하지 말라고 명한다. 제1자연법은 '평화를 추구하고 따르라'이며, "
                "제2자연법은 '평화를 위해 자연권을 상호 포기하라'이다."
            ),
            "original_text": (
                "A law of nature, lex naturalis, is a precept, or general rule, found out by reason, "
                "by which a man is forbidden to do that which is destructive of his life, or taketh away "
                "the means of preserving the same, and to omit that by which he thinketh it may be best preserved."
            ),
            "original_text_ko": (
                "자연법(lex naturalis)은 이성에 의해 발견된 계율 또는 일반 규칙으로, "
                "그것에 의해 인간은 자신의 생명에 파괴적인 것을 하거나 "
                "생명을 보존하는 수단을 빼앗는 것이 금지되고, "
                "생명을 가장 잘 보존할 수 있다고 생각되는 것을 게을리하는 것이 금지된다."
            ),
            "explanation": (
                "홉스는 자연법을 총 19개 열거하지만, 핵심은 처음 세 개이다. "
                "제1자연법: 평화를 추구하라(seek peace and follow it). "
                "제2자연법: 타인도 동의한다면 자연권을 상호 포기하라(mutual laying down of rights). "
                "제3자연법: 맺은 약속(covenant)을 이행하라 — 이것이 정의(justice)의 기초이다. "
                "자연법은 이성의 명령이지만, 이를 강제할 권력이 없으면 실효성이 없다. "
                "따라서 자연법은 그 자체로는 도덕적 의무(in foro interno)에 불과하며, "
                "주권자가 있어야 실질적 의무(in foro externo)가 된다."
            ),
            "argument": (
                "(1) 자연 상태(만인의 투쟁)는 모두에게 해롭다. "
                "(2) 이성은 자기보존에 유리한 것을 추구하라고 명한다. "
                "(3) 평화가 자기보존에 가장 유리하므로, 이성은 평화를 추구하라고 명한다(제1자연법). "
                "(4) 평화는 각자가 무제한적 자연권을 보유하면 불가능하므로, "
                "타인도 동의한다면 자연권을 상호 포기해야 한다(제2자연법). "
                "(5) 상호 포기의 약속(covenant)은 지켜져야 한다(제3자연법 = 정의). "
                "(6) 그러나 약속 이행을 강제할 권력 없이는 약속은 '빈말(words)'에 불과하다. "
                "(7) 따라서 자연법 실현에는 절대적 주권자가 필요하다."
            ),
            "counterpoint": (
                "토마스 아퀴나스(Thomas Aquinas)는 '신학대전'(Summa Theologiae, 1265~1274) I-II, q.91, a.2에서 "
                "자연법을 영원법(lex aeterna)에 대한 이성적 피조물의 참여로 정의하여, "
                "자연법의 근거를 신의 이성에 두었다. 홉스는 이를 세속화하여 "
                "자연법을 자기보존이라는 인간적 목적에 봉사하는 이성의 명령으로 재정의함으로써 "
                "자연법 전통을 근본적으로 변형시켰다는 비판을 받는다. "
                "로크는 '통치론 제2론'(1689)에서 자연법이 주권자 없이도 이성적 인간에 의해 "
                "자연 상태에서 인식·준수될 수 있다고 보아, "
                "홉스의 '주권자 없으면 자연법은 무력하다'는 주장에 반대했다."
            ),
            "context": (
                "자연법 전통은 아리스토텔레스, 스토아 학파, 키케로, 아퀴나스로 이어지는 오래된 전통이다. "
                "홉스는 이 전통을 이어받으면서도, 신적 근거를 제거하고 "
                "자기보존이라는 세속적 원리로 대체함으로써 근대적 자연법론을 수립했다."
            ),
            "keywords": ["자연법", "이성의 명령", "평화", "약속 이행", "정의"],
            "verified": False
        },
        # CLAIM-004: 사회계약 — 자연권의 상호 양도
        {
            "id": "hobbes-claim-004",
            "thinker_id": "hobbes",
            "work_id": "hobbes-leviathan",
            "source_detail": "Leviathan, Part II, Chapter 17",
            "claim": (
                "사회계약(social contract)은 자연 상태의 비참함에서 벗어나기 위해 "
                "모든 사람이 자신의 자연권을 하나의 인격(person) 또는 합의체에 양도하는 것이다. "
                "이 양도는 '나는 이 사람 또는 이 합의체에게 나를 다스릴 권리를 위임하고, "
                "그의 모든 행위를 나의 행위로 인정한다(authorize)'는 형식이다."
            ),
            "original_text": (
                "I authorise and give up my right of governing myself to this man, or to this assembly of men, "
                "on this condition; that thou give up thy right to him, and authorise all his actions "
                "in like manner."
            ),
            "original_text_ko": (
                "나는 나 자신을 다스릴 나의 권리를 이 사람, 또는 이 합의체에게 위임하고 양도한다. "
                "단, 너도 마찬가지로 네 권리를 그에게 양도하고, 그의 모든 행위를 네 것으로 인정한다는 조건 하에."
            ),
            "explanation": (
                "홉스의 사회계약은 로크나 루소의 것과 결정적으로 다르다. "
                "첫째, 계약은 개인들 사이에서 이루어지며 주권자는 계약의 당사자가 아니다. "
                "따라서 주권자는 계약을 위반할 수 없다(계약 당사자가 아니므로). "
                "둘째, 양도되는 것은 자연권이며, 양도는 사실상 돌이킬 수 없다. "
                "셋째, 핵심 개념은 '대리(authorization)'이다: 신민들은 주권자의 모든 행위를 "
                "자신의 행위로 인정한다. 따라서 주권자의 행위에 불만을 품는 것은 "
                "사실상 자기 자신의 행위에 불만을 품는 것이 된다."
            ),
            "argument": (
                "(1) 자연 상태는 만인의 투쟁이므로 모두에게 해롭다. "
                "(2) 평화를 위해서는 공통 권력(common power)이 필요하다. "
                "(3) 공통 권력은 자발적 합의에 의해서만 정당하게 수립될 수 있다. "
                "(4) 합의의 내용: 각 개인이 자기를 다스릴 권리를 하나의 인격에게 양도하고, "
                "그의 행위를 자기 행위로 인정(authorize)한다. "
                "(5) 이로써 다수가 하나의 인격으로 통합되며(united in one person), "
                "이것이 커먼웰스(Commonwealth), 즉 리바이어던이다. "
                "(6) 이 인격을 담지하는 자가 주권자(sovereign)이며, "
                "나머지 모든 사람은 신민(subjects)이다."
            ),
            "counterpoint": (
                "로크는 '통치론 제2론'(1689) 제8~9장에서 사회계약을 홉스와 다르게 구성한다. "
                "로크에게 계약은 두 단계이다: 먼저 개인들이 정치 사회를 형성하는 계약(social compact), "
                "다음으로 이 사회가 정부에 권력을 '신탁(trust)'하는 것이다. "
                "로크에서 정부(주권자)는 신탁받은 권력의 수탁자이므로, "
                "신탁을 위반하면 인민이 저항할 수 있다. "
                "루소는 '사회계약론'(1762) 제1권에서 각 개인이 자신의 모든 권리를 "
                "공동체 전체(일반의지)에 양도하되, 공동체의 구성원으로서 그 권리를 다시 받는다고 하여, "
                "홉스의 일방적 양도와 달리 양도와 회복이 동시에 일어나는 계약을 제안했다."
            ),
            "context": (
                "사회계약 개념은 에피쿠로스의 계약적 정의론에서 선구를 찾을 수 있으나, "
                "근대적 사회계약론의 체계적 정초는 홉스에서 시작된다. "
                "홉스의 계약론은 로크, 루소를 거쳐 롤스에 이르는 "
                "사회계약 전통의 출발점이다."
            ),
            "keywords": ["사회계약", "대리(authorization)", "권리 양도", "커먼웰스"],
            "verified": False
        },
        # CLAIM-005: 주권자론 — 절대주권
        {
            "id": "hobbes-claim-005",
            "thinker_id": "hobbes",
            "work_id": "hobbes-leviathan",
            "source_detail": "Leviathan, Part II, Chapter 18",
            "claim": (
                "주권자(sovereign)의 권력은 절대적이며 분할될 수 없다. "
                "주권의 분할은 곧 커먼웰스의 해체이자 자연 상태로의 회귀를 의미한다. "
                "주권자는 입법, 사법, 행정, 전쟁과 평화, 검열, 보상과 처벌의 모든 권한을 가진다."
            ),
            "original_text": (
                "For what is it to divide the power of a Commonwealth, but to dissolve it; "
                "for powers divided mutually destroy each other."
            ),
            "original_text_ko": (
                "커먼웰스의 권력을 분할하는 것은 곧 그것을 해체하는 것이 아니고 무엇이겠는가? "
                "분할된 권력들은 서로를 파괴하기 때문이다."
            ),
            "explanation": (
                "홉스에게 주권의 절대성은 논리적 필연이다. "
                "사회계약의 목적은 자연 상태의 비참함에서 벗어나는 것이므로, "
                "주권이 제한되거나 분할되면 갈등 해결의 최종 심급이 사라져 "
                "자연 상태가 복귀한다. 주권자의 12가지 권리에는 다음이 포함된다: "
                "법률 제정과 폐지, 전쟁과 평화의 결정, 재판, "
                "관리 임명, 보상과 처벌, 칭호·명예 부여 등. "
                "그러나 홉스는 주권자가 신민의 자기보존 권리를 완전히 빼앗을 수는 없다고 본다. "
                "신민은 자기 생명을 직접 위협받을 때 저항할 수 있는 최소한의 자유를 보유한다."
            ),
            "argument": (
                "(1) 사회계약의 목적은 자기보존과 안전(security)이다. "
                "(2) 안전은 분쟁을 최종적으로 결정하는 권력이 있어야 보장된다. "
                "(3) 최종 결정 권력이 둘 이상이면 그들 사이에 분쟁이 생기고, "
                "이를 결정할 상위 권력이 필요해진다(무한퇴행). "
                "(4) 따라서 주권은 반드시 하나(단일)이고 절대적(최고)이어야 한다. "
                "(5) 주권 분할(예: 입법권과 집행권의 분리)은 갈등의 씨앗이며, "
                "영국 내전이 바로 왕과 의회의 주권 분쟁에서 비롯되었다."
            ),
            "counterpoint": (
                "로크는 '통치론 제2론'(1689) 제12~14장에서 입법권과 집행권의 분리를 옹호하며, "
                "주권의 분할이 오히려 전제(tyranny)를 방지한다고 주장했다. "
                "몽테스키외(Montesquieu)는 '법의 정신'(De l'esprit des lois, 1748) 제11권에서 "
                "입법, 행정, 사법의 삼권분립을 체계화하여, "
                "홉스의 절대주권론에 정면으로 대립하는 권력 분립론을 확립했다. "
                "이후 매디슨(James Madison)은 '연방주의자 논집'(The Federalist Papers, 1788) 제51편에서 "
                "견제와 균형(checks and balances)이 자유의 보루라고 하여 홉스 절대주권론을 거부했다."
            ),
            "context": (
                "영국 내전에서 왕(집행권)과 의회(입법권)의 갈등이 전쟁으로 비화한 경험이 "
                "홉스의 주권 분할 불가론의 직접적 배경이다. "
                "홉스에게 내전은 주권 분할의 필연적 귀결이었다."
            ),
            "keywords": ["절대주권", "주권 불가분", "권력 분할 비판"],
            "verified": False
        },
        # CLAIM-006: 대리(Authorization) 개념
        {
            "id": "hobbes-claim-006",
            "thinker_id": "hobbes",
            "work_id": "hobbes-leviathan",
            "source_detail": "Leviathan, Part I, Chapter 16; Part II, Chapter 17",
            "claim": (
                "커먼웰스의 핵심은 대리(authorization)이다. 신민들은 주권자를 자신의 대리인(author)으로 "
                "임명하여, 주권자의 행위를 자기 자신의 행위로 인정한다. "
                "따라서 주권자가 행하는 모든 것은 신민 자신의 행위이며, "
                "주권자에게 불의(injustice)를 행했다고 불평하는 것은 자기 자신에게 불의를 행했다고 "
                "불평하는 것과 같다."
            ),
            "original_text": (
                "A multitude of men are made one person when they are by one man, or one person, "
                "represented; so that it be done with the consent of every one of that multitude in particular. "
                "For it is the unity of the representer, not the unity of the represented, "
                "that maketh the person one."
            ),
            "original_text_ko": (
                "다수의 인간은 한 사람 또는 한 인격에 의해 대표될 때 하나의 인격이 된다. "
                "단, 이것이 그 다수의 모든 개인의 동의를 얻어 이루어져야 한다. "
                "인격을 하나로 만드는 것은 대표되는 자들의 통일이 아니라 "
                "대표하는 자의 통일이기 때문이다."
            ),
            "explanation": (
                "홉스의 대리(authorization) 개념은 리바이어던에서 가장 혁신적인 요소 중 하나이다. "
                "개인들은 계약을 통해 주권자를 자신의 '작자(author)'의 '행위자(actor)'로 만든다. "
                "즉 주권자는 개인들의 이름으로 행위하는 대리인이다. "
                "이 구조에서 주권자의 행위는 논리적으로 개인들 자신의 행위가 되므로, "
                "주권자를 비난하는 것은 자기모순이 된다. "
                "이것은 현대 대의민주주의(representative democracy)의 개념적 선구이면서도, "
                "동시에 주권자의 절대적 권위를 정당화하는 논증이기도 하다."
            ),
            "argument": (
                "(1) 인격(person)에는 자연적 인격(natural person)과 인위적 인격(artificial person)이 있다. "
                "(2) 인위적 인격은 타인의 말과 행위를 대표(represent)하는 자이다. "
                "(3) 대표되는 자가 작자(author)이고, 대표하는 자가 행위자(actor)이다. "
                "(4) 사회계약에서 모든 개인은 주권자를 자신의 행위자로 임명(authorize)한다. "
                "(5) 따라서 주권자의 모든 행위는 개인들 자신의 행위와 같다. "
                "(6) 결론: 주권자에게 부정의를 범했다고 불평할 수 없다—자기 행위에 대해 "
                "자기에게 불의를 범하는 것은 불가능하므로."
            ),
            "counterpoint": (
                "루소는 '사회계약론'(1762) 제2권에서 주권은 양도될 수 없고(inalienable) "
                "대표될 수 없다(irrepresentable)고 주장했다. "
                "루소에게 일반의지(volonté générale)는 대리될 수 없으며, "
                "대표자를 세우는 순간 인민은 자유를 잃는다. "
                "'영국인들은 자기가 자유롭다고 생각하지만, 의회 선거 때만 자유롭고 "
                "선거가 끝나면 노예가 된다'는 루소의 유명한 비판은 "
                "홉스적 대리(authorization) 개념에 대한 직접적 공격이다."
            ),
            "context": (
                "대리(authorization) 개념은 영국 의회 전통에서 '대표(representation)'의 법적 개념을 "
                "정치철학에 도입한 것이다. 이 개념은 이후 버크(Edmund Burke)의 "
                "'가상적 대표(virtual representation)' 논의와 현대 민주주의 이론에 영향을 미쳤다."
            ),
            "keywords": ["대리(authorization)", "인위적 인격", "대표", "작자와 행위자"],
            "verified": False
        },
        # CLAIM-007: 자기보존의 양도 불가능성
        {
            "id": "hobbes-claim-007",
            "thinker_id": "hobbes",
            "work_id": "hobbes-leviathan",
            "source_detail": "Leviathan, Part I, Chapter 14; Part II, Chapter 21",
            "claim": (
                "자기보존(self-preservation)의 권리는 양도할 수 없다. "
                "사회계약의 목적 자체가 자기보존이므로, 자기 생명을 포기하겠다는 계약은 "
                "자기모순이며 무효이다. 신민은 주권자가 자신을 직접 죽이려 할 때 저항할 수 있다."
            ),
            "original_text": (
                "A man cannot lay down the right of resisting them that assault him by force to take away "
                "his life, because he cannot be understood to aim thereby at any good to himself."
            ),
            "original_text_ko": (
                "인간은 자신의 생명을 빼앗기 위해 폭력으로 자신을 공격하는 자에게 "
                "저항하는 권리를 포기할 수 없다. 왜냐하면 그것이 자신에게 어떤 좋은 것을 "
                "목표로 한다고 이해될 수 없기 때문이다."
            ),
            "explanation": (
                "이것은 홉스 절대주권론의 내적 한계이자 안전장치이다. "
                "홉스는 모든 권리 양도의 동기는 자기보존이라고 본다. "
                "따라서 자기보존 자체를 포기하는 계약은 양도의 동기에 모순되므로 무효이다. "
                "이 논리에 의해 신민은 사형 선고를 받았을 때 도주하거나, "
                "자신을 죽이려는 주권자의 명령에 저항할 수 있다. "
                "다만 이것은 주권자의 정당성 자체를 부정하는 것은 아니다. "
                "주권자는 사형을 선고할 권리가 있고, 신민은 도주할 권리가 있다."
            ),
            "argument": (
                "(1) 모든 자발적 행위(voluntary act)의 목적은 행위자 자신에게 좋은 것이다. "
                "(2) 권리를 양도하는 행위도 자발적 행위이므로, 양도자에게 좋은 것을 목적으로 해야 한다. "
                "(3) 자기 생명을 보존하는 것은 모든 좋은 것의 전제이다. "
                "(4) 자기 생명을 포기하겠다는 약속은 양도자에게 어떤 좋은 것도 가져다주지 않는다. "
                "(5) 따라서 자기보존의 권리를 양도하겠다는 계약은 자기모순이며 구속력이 없다. "
                "(6) 결론: 신민의 생명이 직접 위협받을 때 저항은 정당하다."
            ),
            "counterpoint": (
                "로크는 '통치론 제2론'(1689) 제19장에서 이 논리를 확대하여, "
                "주권자(정부)가 인민의 생명·자유·재산을 체계적으로 침해하면 "
                "인민 전체의 저항권(right of revolution)이 발생한다고 주장했다. "
                "홉스에서 자기보존 저항은 개인적이고 극단적인 경우로 제한되지만, "
                "로크에서는 집단적·정치적 저항권으로 발전한다. "
                "한편, 절대주의 옹호자 필머(Robert Filmer)는 '가부장론'(Patriarcha, 1680)에서 "
                "주권자에 대한 저항은 어떤 경우에도 불허된다고 하여 홉스보다 더 강한 절대주의를 주장했다."
            ),
            "context": (
                "자기보존의 양도 불가능성은 홉스 사상의 개인주의적 측면을 보여준다. "
                "홉스의 체계에서 국가(커먼웰스)의 목적은 궁극적으로 개인의 자기보존이며, "
                "이 목적이 달성되지 않으면 복종의 의무도 약해진다."
            ),
            "keywords": ["자기보존", "양도 불가능한 권리", "저항의 자유"],
            "verified": False
        },
        # CLAIM-008: 커먼웰스 — 인공 인간
        {
            "id": "hobbes-claim-008",
            "thinker_id": "hobbes",
            "work_id": "hobbes-leviathan",
            "source_detail": "Leviathan, Introduction; Part II, Chapter 17",
            "claim": (
                "커먼웰스(Commonwealth)는 인공 인간(artificial man)이다. "
                "주권자는 이 인공 인간의 영혼이고, 관리는 관절, 보상과 처벌은 신경, "
                "재산과 부는 힘이며, 국민의 안전(salus populi)이 그의 사업(business)이다. "
                "이 인공 인간이 리바이어던(Leviathan), 즉 '가사적 신(mortal god)'이다."
            ),
            "original_text": (
                "For by art is created that great Leviathan called a Commonwealth, or State, "
                "which is but an artificial man, though of greater stature and strength than the natural, "
                "for whose protection and defence it was intended."
            ),
            "original_text_ko": (
                "기예(art)에 의해 커먼웰스 또는 국가라 불리는 저 위대한 리바이어던이 창조되었는데, "
                "이것은 인공 인간에 불과하지만, 그것의 보호와 방어를 위해 만들어진 "
                "자연 인간보다 더 큰 체격과 힘을 가지고 있다."
            ),
            "explanation": (
                "홉스는 국가를 인공물(artifact)로 본다. 자연이 아니라 인간의 기예(art)에 의해 "
                "만들어진 것이다. 리바이어던은 구약성서 욥기에 나오는 바다 괴물로, "
                "홉스는 이를 국가의 엄청난 힘과 위엄을 상징하는 이름으로 사용한다. "
                "'가사적 신(mortal god)'이라는 표현은 주권자가 불멸의 신 아래에서 "
                "지상의 평화와 안전을 보장하는 최고 권위임을 의미한다. "
                "이 기계론적·인공론적 국가관은 아리스토텔레스의 "
                "'인간은 본성상 정치적 동물(zoon politikon)'이라는 자연주의적 국가관과 대조된다."
            ),
            "argument": (
                "(1) 자연은 인간을 만들었고, 인간은 기예(art)로 자연을 모방한다. "
                "(2) 자연의 가장 위대한 작품은 인간이므로, 기예의 가장 위대한 작품은 인공 인간(국가)이다. "
                "(3) 국가의 각 부분은 자연 인간의 신체에 비유된다: "
                "주권자=영혼, 관리=관절, 법=이성과 의지, 내전=질병, 내전에 의한 국가해체=죽음. "
                "(4) 이 인공 인간은 개인들의 계약에 의해 생성되었으므로 자연적이 아니라 인위적이다. "
                "(5) 이 인공 인간의 목적은 자연 인간의 보호와 방어(salus populi)이다."
            ),
            "counterpoint": (
                "아리스토텔레스는 '정치학'(Politika, 기원전 350경) 제1권에서 "
                "국가(polis)는 자연에 의해 존재하며 인간보다 선행한다고 주장했다. "
                "인간은 본성상 정치적 동물(zoon politikon)이므로 국가는 인공물이 아니라 자연물이다. "
                "헤겔(G.W.F. Hegel)은 '법철학'(Grundlinien der Philosophie des Rechts, 1821)에서 "
                "국가를 계약의 산물이 아니라 이성의 현실태(Wirklichkeit der sittlichen Idee)로 보아, "
                "홉스의 기계론적·계약론적 국가관을 거부했다."
            ),
            "context": (
                "17세기 기계론적 세계관(갈릴레오, 데카르트)의 영향 아래, "
                "홉스는 자연도 인간도 국가도 모두 물질과 운동의 기계론으로 설명하려 했다. "
                "이 관점에서 국가는 시계처럼 부품(개인들)이 결합하여 작동하는 기계이다."
            ),
            "keywords": ["커먼웰스", "인공 인간", "리바이어던", "가사적 신"],
            "verified": False
        },
        # CLAIM-009: 유물론적 인간관
        {
            "id": "hobbes-claim-009",
            "thinker_id": "hobbes",
            "work_id": "hobbes-leviathan",
            "source_detail": "Leviathan, Part I, Chapters 1-6; De Corpore, Part IV",
            "claim": (
                "인간의 모든 정신 활동—감각, 상상, 기억, 추론, 정념—은 물질적 운동(motion)으로 환원된다. "
                "감각은 외부 대상에서 발생한 운동이 감각 기관을 통해 뇌와 심장에 전달되는 것이고, "
                "사고(thought)는 감각의 잔여 운동이다. 비물질적 실체(incorporeal substance)는 모순이다."
            ),
            "original_text": (
                "All which qualities, called 'sensible', are, in the object that causeth them, "
                "but so many several motions of the matter, by which it presseth our organs diversely. "
                "Neither in us that are pressed are they anything else but diverse motions; "
                "for motion produceth nothing but motion."
            ),
            "original_text_ko": (
                "'감각적'이라 불리는 이 모든 성질은, 그것을 야기하는 대상에서는 "
                "우리의 감각 기관을 다양하게 압박하는 물질의 여러 운동에 불과하다. "
                "압박받는 우리 안에서도 그것은 다양한 운동 이외의 다른 것이 아니다. "
                "왜냐하면 운동은 운동 이외의 것을 산출하지 않기 때문이다."
            ),
            "explanation": (
                "홉스의 유물론(materialism)은 그의 정치철학의 철학적 토대이다. "
                "정신 활동이 물질적 운동이라면, 인간 행위는 욕구(appetite)와 혐오(aversion)라는 "
                "물리적 경향성으로 설명된다. 좋은 것(good)은 욕구의 대상이고, "
                "나쁜 것(evil)은 혐오의 대상이다. "
                "이 유물론적 인간관에서 자기보존이라는 가장 기본적인 욕구가 "
                "정치 체계 전체의 동기적 토대가 된다. "
                "비물질적 영혼, 자유의지의 비물질적 근거, 신의 비물질적 실체 등은 "
                "홉스에게 '말의 모순(contradiction in terms)'이다."
            ),
            "argument": (
                "(1) 존재하는 것(that which exists)은 반드시 공간을 차지하는 물체(body)이다. "
                "(2) 비물질적 실체(incorporeal substance)는 '공간을 차지하지 않는 공간 차지자'와 같은 모순이다. "
                "(3) 감각은 외부 물체의 운동이 감각 기관을 통해 전달되는 것이다. "
                "(4) 상상과 기억은 감각이 멈춘 후 잔여하는 감쇠된 운동이다. "
                "(5) 추론은 이름(names)의 결합과 분리, 즉 언어적 계산(computation)이다. "
                "(6) 정념(passions)은 자기보존에 유리하거나 불리한 것에 대한 운동적 반응(appetite/aversion)이다. "
                "(7) 따라서 인간의 모든 활동은 운동으로 설명 가능하며, 비물질적 설명은 불필요하다."
            ),
            "counterpoint": (
                "데카르트(René Descartes)는 '성찰'(Meditationes de Prima Philosophia, 1641) 제6성찰에서 "
                "정신(res cogitans)과 물체(res extensa)는 근본적으로 다른 실체라는 이원론(dualism)을 주장했다. "
                "데카르트에게 사고는 비연장적(non-extended) 실체의 활동이며, "
                "물질적 운동으로 환원될 수 없다. "
                "홉스는 데카르트의 '성찰'에 대한 반론(Third Set of Objections, 1641)에서 "
                "사고가 물질의 운동일 수 있다고 주장했고, 데카르트는 이를 거부했다. "
                "칸트는 '순수이성비판'(Kritik der reinen Vernunft, 1781) 변증론에서 "
                "유물론도 관념론도 이론적으로 증명될 수 없다고 보았다."
            ),
            "context": (
                "17세기 기계론적 자연철학(갈릴레오, 데카르트)의 맥락에서 "
                "홉스는 가장 급진적인 유물론을 전개했다. "
                "데카르트가 정신과 물질의 이원론을 유지한 반면, "
                "홉스는 모든 것을 물질과 운동으로 환원하는 일원론적 유물론을 주장했다."
            ),
            "keywords": ["유물론", "운동", "감각 이론", "정념", "욕구와 혐오"],
            "verified": False
        },
        # CLAIM-010: 정의 — 약속 이행
        {
            "id": "hobbes-claim-010",
            "thinker_id": "hobbes",
            "work_id": "hobbes-leviathan",
            "source_detail": "Leviathan, Part I, Chapter 15",
            "claim": (
                "정의(justice)란 맺은 약속(covenant)을 이행하는 것이다. "
                "약속이 없는 곳에는 정의도 부정의도 없다. "
                "그리고 약속 이행을 강제하는 권력(주권자)이 없는 곳에서도 "
                "정의는 실효적으로 존재하지 않는다."
            ),
            "original_text": (
                "The definition of injustice is no other than the not performance of covenant. "
                "And whatsoever is not unjust is just."
            ),
            "original_text_ko": (
                "부정의의 정의(定義)는 약속의 불이행 이외의 다른 것이 아니다. "
                "그리고 부정의하지 않은 것은 정의롭다."
            ),
            "explanation": (
                "홉스의 정의론은 제3자연법에서 도출된다. "
                "정의는 자연적 덕이나 이데아적 형상이 아니라, "
                "상호 합의한 약속(covenant)을 이행하는 것이다. "
                "이 정의 개념은 약속의 존재를 전제하므로, 약속이 없는 자연 상태에서는 정의가 없다. "
                "또한 약속 이행을 강제할 권력이 없으면 약속은 '빈말(words)'이므로, "
                "정의가 실효적으로 존재하려면 주권자의 강제력이 필요하다. "
                "이 견해는 법실증주의(legal positivism)의 선구로 평가된다."
            ),
            "argument": (
                "(1) 제3자연법: 맺은 약속을 이행하라. 이것이 정의의 샘(fountain)이자 기원이다. "
                "(2) 약속이 없으면 양도된 권리가 없고, 모든 사람이 모든 것에 대한 권리를 가지므로, "
                "어떤 행위도 부정의할 수 없다. "
                "(3) 따라서 정의와 부정의는 약속의 존재를 전제한다. "
                "(4) 그러나 약속 이행을 강제할 권력 없이는 '먼저 이행하는 자'가 불리하므로, "
                "약속은 구속력을 잃는다. "
                "(5) 따라서 커먼웰스(주권자)가 수립된 후에야 정의가 실효적으로 존재한다."
            ),
            "counterpoint": (
                "플라톤은 '국가'(Politeia, 기원전 380경) 제4권에서 정의를 "
                "영혼의 세 부분(이성, 기개, 욕구)이 각각 제 역할을 다하는 조화로 정의했다. "
                "정의는 약속이나 계약 이전에 영혼의 자연적 질서로 존재한다. "
                "아리스토텔레스는 '니코마코스 윤리학'(기원전 350경) 제5권에서 "
                "정의를 분배적 정의(distributive justice)와 교정적 정의(corrective justice)로 구분하며, "
                "정의는 덕(virtue)의 일종으로 공동체의 자연적 목적에 봉사한다고 보았다. "
                "두 입장 모두 정의를 약속 이행으로 환원하는 홉스와 대조된다."
            ),
            "context": (
                "홉스의 정의론은 에피쿠로스의 계약적 정의론의 근대적 발전이며, "
                "이후 흄의 관습적 정의론, 벤담의 법실증주의, "
                "하트(H.L.A. Hart)의 법실증주의로 이어지는 전통의 출발점이다."
            ),
            "keywords": ["정의", "약속 이행", "강제력", "법실증주의"],
            "verified": False
        },
        # CLAIM-011: 신민의 자유 — 법의 침묵이 있는 곳
        {
            "id": "hobbes-claim-011",
            "thinker_id": "hobbes",
            "work_id": "hobbes-leviathan",
            "source_detail": "Leviathan, Part II, Chapter 21",
            "claim": (
                "신민의 자유(liberty of subjects)는 주권자가 법으로 규제하지 않은 영역에서만 존재한다. "
                "'법이 침묵하는 곳(where the law is silent)'에서 신민은 자유롭다. "
                "사고파는 자유, 거주지 선택, 직업 선택, 자녀 교육 등은 "
                "주권자가 명시적으로 규제하지 않는 한 신민의 자유에 속한다."
            ),
            "original_text": (
                "The liberty of a subject lieth therefore only in those things which, in regulating their actions, "
                "the sovereign hath praetermitted; such as is the liberty to buy and sell, and otherwise contract "
                "with one another; to choose their own abode, their own diet, their own trade of life, "
                "and institute their children as they themselves think fit; and the like."
            ),
            "original_text_ko": (
                "신민의 자유는 오직 주권자가 그들의 행위를 규제하면서 빠뜨린 것들에서만 존재한다. "
                "예를 들어 사고파는 자유, 서로 계약하는 자유, 자기 거주지를 선택하는 자유, "
                "식단, 직업, 자녀 교육을 자기가 적합하다고 생각하는 대로 하는 자유 등이다."
            ),
            "explanation": (
                "홉스에게 자유(liberty)는 운동에 대한 외적 방해의 부재(absence of external impediments)이다. "
                "이 물리적 자유 개념에 따라, 법이 금지하지 않은 것은 자유롭다. "
                "그러나 주권자는 원칙적으로 어떤 것이든 법으로 규제할 수 있으므로, "
                "신민의 자유는 주권자의 의지에 의존한다. "
                "이것은 자유를 자연적 권리로 보는 로크적 전통과 대조된다. "
                "다만 실제로 주권자가 모든 것을 규제하는 것은 불가능하고 바람직하지도 않으므로, "
                "상당한 영역에서 사실상의 자유가 보장된다."
            ),
            "argument": (
                "(1) 자유란 운동에 대한 외적 방해의 부재이다(물리적 자유 개념). "
                "(2) 법은 신민의 행위에 대한 외적 규제(방해)이다. "
                "(3) 법이 규제하지 않은 영역에서는 외적 방해가 없으므로 신민은 자유롭다. "
                "(4) 주권자는 평화와 안전에 필요한 모든 것을 법으로 규제할 수 있다. "
                "(5) 그러나 주권자가 규제하지 않기로 한 영역(법의 침묵)에서 신민의 자유가 존재한다. "
                "(6) 자기보존의 경우처럼 양도 불가능한 자연권은 법으로도 빼앗을 수 없다."
            ),
            "counterpoint": (
                "로크는 '통치론 제2론'(1689) 제4장에서 자유를 '법 아래의 자유(freedom under law)'로 정의했다. "
                "로크에게 법은 자유를 제한하는 것이 아니라 보호하고 확대하는 것이다. "
                "'법이 없는 곳에 자유도 없다(where there is no law, there is no freedom).' "
                "이는 홉스의 '법이 침묵하는 곳에서 자유'와 정반대의 견해이다. "
                "밀(J.S. Mill)은 '자유론'(On Liberty, 1859)에서 "
                "개인의 자유를 주권자의 침묵이 아니라 '위해 원칙(harm principle)'에 의해 보호해야 한다고 주장하여, "
                "자유의 근거를 주권자의 재량에서 원칙적 한계로 옮겼다."
            ),
            "context": (
                "홉스의 소극적 자유(negative liberty) 개념은 이후 "
                "이사야 벌린(Isaiah Berlin)의 '자유의 두 개념'(Two Concepts of Liberty, 1958)에서 "
                "소극적 자유(liberty from) 전통의 선구로 자리매김된다."
            ),
            "keywords": ["신민의 자유", "법의 침묵", "소극적 자유"],
            "verified": False
        },
        # CLAIM-012: 자연적 평등
        {
            "id": "hobbes-claim-012",
            "thinker_id": "hobbes",
            "work_id": "hobbes-leviathan",
            "source_detail": "Leviathan, Part I, Chapter 13",
            "claim": (
                "자연은 인간을 신체적·정신적 능력에서 대략적으로 평등하게 만들었다. "
                "가장 약한 자도 비밀스러운 계략이나 다른 약자들과의 연합으로 "
                "가장 강한 자를 죽일 수 있다. 이 자연적 평등이 전쟁 상태의 근본 원인이다."
            ),
            "original_text": (
                "Nature hath made men so equal in the faculties of body and mind as that, "
                "though there be found one man sometimes manifestly stronger in body or of quicker mind than another, "
                "yet when all is reckoned together the difference between man and man is not so considerable "
                "as that one man can thereupon claim to himself any benefit to which another may not pretend as well as he."
            ),
            "original_text_ko": (
                "자연은 인간을 신체와 정신의 능력에서 매우 평등하게 만들었으므로, "
                "때때로 한 사람이 다른 사람보다 신체가 분명히 강하거나 정신이 빠른 경우가 있더라도, "
                "모든 것을 함께 고려하면 인간과 인간의 차이는 "
                "한 사람이 다른 사람이 자기만큼 요구할 수 없는 어떤 이익을 "
                "자기만 주장할 수 있을 정도로 크지 않다."
            ),
            "explanation": (
                "홉스의 자연적 평등론은 아리스토텔레스의 자연적 불평등론(자연 노예론)에 대한 반박이다. "
                "아리스토텔레스는 일부 인간은 본성상 지배자이고 일부는 본성상 노예라고 보았지만, "
                "홉스는 인간 사이의 자연적 차이가 정치적 지배를 정당화할 만큼 크지 않다고 본다. "
                "신체적으로 가장 약한 자도 무기나 연합으로 가장 강한 자를 제압할 수 있고, "
                "정신적으로는 경험을 통해 누구나 비슷한 수준의 지혜를 얻을 수 있다. "
                "이 평등은 사회계약의 전제이다: 평등하기에 아무도 자연적으로 타인을 지배할 수 없고, "
                "따라서 지배는 합의에 의해서만 정당하다."
            ),
            "argument": (
                "(1) 신체적 능력에서 개인 차이가 있지만, 가장 약한 자도 "
                "계략이나 연합으로 가장 강한 자를 제거할 수 있다. "
                "(2) 정신적 능력에서의 차이는 경험과 교육에 의한 것이며 자연적이지 않다. "
                "(3) 더구나 모든 사람은 자신이 타인보다 현명하다고 생각하는데, "
                "이 보편적 자부심 자체가 지혜의 평등한 분배의 증거이다. "
                "(4) 능력의 평등에서 희망의 평등이 나온다: 누구나 원하는 것을 얻을 수 있다고 기대한다. "
                "(5) 이 평등이 경쟁, 불신, 전쟁의 원인이 된다."
            ),
            "counterpoint": (
                "아리스토텔레스는 '정치학'(Politika, 기원전 350경) 제1권에서 "
                "자연적 불평등을 주장했다: 일부 인간은 본성상 자유인이고 일부는 본성상 노예이며, "
                "이 자연적 위계가 정치적 지배를 정당화한다. "
                "니체(Friedrich Nietzsche)는 '선악의 저편'(Jenseits von Gut und Böse, 1886) 제9장에서 "
                "인간의 자연적 평등은 허구이며, 인간 사이에는 서열과 차이(Rangordnung)가 있다고 주장하여, "
                "홉스의 평등 전제를 거부했다."
            ),
            "context": (
                "홉스의 자연적 평등론은 근대 민주주의의 평등 이념과 연결된다. "
                "비록 홉스 자신은 민주주의보다 군주정을 선호했지만, "
                "자연적 평등에서 출발하는 그의 논증 구조는 "
                "이후 로크, 루소, 제퍼슨 등의 평등주의적 정치이론의 논리적 토대를 제공했다."
            ),
            "keywords": ["자연적 평등", "능력의 평등", "전쟁의 원인"],
            "verified": False
        },
        # CLAIM-013: 주권자의 세 가지 형태
        {
            "id": "hobbes-claim-013",
            "thinker_id": "hobbes",
            "work_id": "hobbes-leviathan",
            "source_detail": "Leviathan, Part II, Chapter 19",
            "claim": (
                "커먼웰스는 주권이 부여되는 방식에 따라 세 가지 형태가 있다: "
                "군주정(monarchy, 한 사람), 귀족정(aristocracy, 합의체의 일부), "
                "민주정(democracy, 전체 합의체). "
                "홉스는 군주정이 가장 효율적이고 안정적인 정체라고 주장하지만, "
                "어떤 형태든 주권은 절대적이어야 한다."
            ),
            "original_text": (
                "The difference of Commonwealths consisteth in the difference of the sovereign, "
                "or the person representative of all and every one of the multitude. "
                "And because the sovereignty is either in one man, or in an assembly of more than one... "
                "when the representative is one man, then is the Commonwealth a monarchy; "
                "when an assembly of all that will come together, then it is a democracy, or popular Commonwealth; "
                "when an assembly of a part only, then it is called an aristocracy."
            ),
            "original_text_ko": (
                "커먼웰스의 차이는 주권자, 즉 다수의 모든 개인의 대표 인격의 차이에 있다. "
                "주권이 한 사람에게 있으면 군주정이고, "
                "모두가 참여하는 합의체에 있으면 민주정 또는 인민 커먼웰스이고, "
                "일부의 합의체에만 있으면 귀족정이라 불린다."
            ),
            "explanation": (
                "홉스는 아리스토텔레스 이래의 정체 분류(군주정, 귀족정, 민주정)를 유지하면서도, "
                "그 변형 형태(폭군정, 과두정, 무정부)를 별도의 정체로 인정하지 않는다. "
                "폭군정은 군주정을 싫어하는 자들의 이름이고, 과두정은 귀족정을 싫어하는 자들의 이름이며, "
                "무정부는 민주정을 싫어하는 자들의 이름일 뿐이다. "
                "홉스는 군주정을 선호하는데, 그 이유는 결정의 신속성, 일관성, "
                "사적 이익과 공적 이익의 일치(군주의 부와 안전이 인민의 부와 안전에 달려 있으므로), "
                "파벌과 내전의 위험 감소 등이다."
            ),
            "argument": (
                "(1) 주권의 본질은 형태에 관계없이 동일하다: 절대적이고 불가분이어야 한다. "
                "(2) 그러나 실천적으로 군주정이 우월하다: "
                "(2a) 군주는 언제든 자문을 구할 수 있지만, 합의체는 정해진 때에만 모인다. "
                "(2b) 군주의 사적 이익은 공적 이익과 일치하는 경향이 있다(인민이 부유해야 군주도 부유). "
                "(2c) 합의체에서는 파벌이 생기고, 파벌 갈등이 내전으로 비화할 수 있다. "
                "(3) 합의체 정부(민주정, 귀족정)에서 주권이 사실상 분할되면 자연 상태로 회귀한다."
            ),
            "counterpoint": (
                "아리스토텔레스는 '정치학'(기원전 350경) 제3~4권에서 정체를 "
                "공익을 위한 올바른 정체(군주정, 귀족정, 혼합정)와 "
                "사익을 위한 타락한 정체(폭군정, 과두정, 중우정)로 구분했다. "
                "홉스가 이 구분을 거부한 것은 모든 주권은 절대적이어야 한다는 전제에서 비롯된다. "
                "몽테스키외는 '법의 정신'(1748)에서 공화정(민주정+귀족정), 군주정, 전제정을 구분하고, "
                "각 정체에 적합한 원리(덕, 명예, 공포)가 있다고 보아, "
                "홉스의 군주정 우월론을 거부했다."
            ),
            "context": (
                "홉스가 군주정을 선호한 것은 영국 내전의 경험에서 비롯된다. "
                "의회(합의체)와 왕(군주)의 갈등이 내전으로 비화한 경험은, "
                "합의체 정부의 불안정성에 대한 홉스의 확신을 강화했다."
            ),
            "keywords": ["군주정", "귀족정", "민주정", "정체론"],
            "verified": False
        },
        # CLAIM-014: 공포와 복종의 정당성
        {
            "id": "hobbes-claim-014",
            "thinker_id": "hobbes",
            "work_id": "hobbes-leviathan",
            "source_detail": "Leviathan, Part I, Chapter 14; Part II, Chapter 20",
            "claim": (
                "공포(fear)에 의해 맺은 약속도 유효하다. "
                "공포에 의한 동의도 자발적 동의이며, 따라서 구속력이 있다. "
                "정복에 의한 커먼웰스(Commonwealth by acquisition)도 "
                "제도에 의한 커먼웰스(Commonwealth by institution)와 동일한 정당성을 가진다."
            ),
            "original_text": (
                "Covenants entered into by fear, in the condition of mere nature, are obligatory. "
                "For example, if I covenant to pay a ransom, or service, for my life, to an enemy, "
                "I am bound by it."
            ),
            "original_text_ko": (
                "순수한 자연 상태에서 공포에 의해 맺은 약속은 구속력이 있다. "
                "예를 들어, 적에게 내 생명을 위해 몸값이나 봉사를 지불하겠다고 약속하면, "
                "나는 그것에 구속된다."
            ),
            "explanation": (
                "홉스는 두 가지 방식의 커먼웰스 수립을 인정한다. "
                "제도에 의한 커먼웰스(by institution): 개인들이 자발적으로 모여 주권자를 세우는 것. "
                "정복에 의한 커먼웰스(by acquisition): 정복자에 대한 공포로 복종하는 것. "
                "홉스에게 두 경우 모두 정당한데, 핵심은 '동의'의 존재이다. "
                "공포에 의한 동의도 동의이다. 자연 상태에서의 모든 합의는 "
                "어느 정도 공포의 맥락에서 이루어지기 때문이다. "
                "이 논증은 사실상의 권력을 정당화하는 데 사용될 수 있어 논쟁적이다."
            ),
            "argument": (
                "(1) 자발적 행위(voluntary act)는 행위자의 의지에서 비롯된 행위이다. "
                "(2) 공포에 의해 행위한 사람도 '공포의 결과를 피하고 싶다'는 의지에서 행위하므로, "
                "그 행위는 자발적이다. "
                "(3) 자발적 행위에서 맺은 약속은 구속력이 있다. "
                "(4) 따라서 공포에 의한 약속도 구속력이 있다. "
                "(5) 정복에 의한 커먼웰스에서 신민은 정복자에 대한 공포로 복종을 약속하는데, "
                "이것도 자발적 약속이므로 정당하다. "
                "(6) 결론: 주권의 정당성은 수립 방식(합의/정복)이 아니라 동의의 존재 여부에 달려 있다."
            ),
            "counterpoint": (
                "로크는 '통치론 제2론'(1689) 제16장에서 정복에 의한 지배는 "
                "진정한 동의가 아니라 강압(force)에 불과하므로 정당한 정부를 수립하지 못한다고 주장했다. "
                "로크에게 정당한 정부는 오직 자유롭고 강압 없는 동의(free consent)에만 기초한다. "
                "공포에 의한 동의는 진정한 동의가 아니며, 강도에게 맺은 약속이 구속력이 없듯이 "
                "정복자에게 맺은 약속도 구속력이 없다."
            ),
            "context": (
                "이 논증은 홉스가 크롬웰 정권(정복에 의한 권력)의 정당성을 인정하는 데 "
                "사용될 수 있었다. 실제로 홉스는 리바이어던 출간(1651) 직후 "
                "파리에서 런던으로 귀국하여 크롬웰 정권 하에서 살았다."
            ),
            "keywords": ["공포에 의한 동의", "정복에 의한 커먼웰스", "자발적 행위"],
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """홉스 키워드 데이터 입력."""
    keywords = [
        {
            "id": "hobbes-kw-001",
            "thinker_id": "hobbes",
            "term": "자연 상태 (State of Nature)",
            "term_original": "state of nature / status naturalis",
            "definition": (
                "공통의 권력(common power)이 존재하지 않는 인간의 상태. "
                "홉스에 따르면 이 상태에서 인간은 만인에 대한 만인의 투쟁 상태에 놓이며, "
                "삶은 '고독하고, 가난하고, 험악하고, 잔인하고, 짧다.' "
                "역사적 사실이라기보다 논리적 가설로, 공통 권력 부재 시 인간 본성이 "
                "어떤 결과를 낳는지를 보여주는 사고실험이다."
            ),
            "related_claims": ["hobbes-claim-001", "hobbes-claim-012"],
            "source": "Leviathan, Part I, Chapter 13"
        },
        {
            "id": "hobbes-kw-002",
            "thinker_id": "hobbes",
            "term": "사회계약 (Social Contract)",
            "term_original": "covenant / social contract",
            "definition": (
                "자연 상태의 비참함에서 벗어나기 위해 모든 사람이 자신의 자연권을 "
                "하나의 인격(주권자)에게 양도하는 상호 합의. "
                "홉스의 사회계약은 개인들 사이에서 이루어지며 주권자는 계약 당사자가 아니다. "
                "핵심은 대리(authorization): 신민은 주권자의 행위를 자기 행위로 인정한다."
            ),
            "related_claims": ["hobbes-claim-004", "hobbes-claim-006"],
            "source": "Leviathan, Part II, Chapter 17"
        },
        {
            "id": "hobbes-kw-003",
            "thinker_id": "hobbes",
            "term": "주권자 (Sovereign)",
            "term_original": "sovereign",
            "definition": (
                "사회계약에 의해 절대적 권력을 부여받은 인격(한 사람 또는 합의체). "
                "주권자는 계약 당사자가 아니므로 계약을 위반할 수 없고, "
                "입법, 사법, 전쟁과 평화, 관리 임명 등 모든 공적 권한을 가진다. "
                "주권의 분할은 곧 커먼웰스의 해체를 의미한다."
            ),
            "related_claims": ["hobbes-claim-005", "hobbes-claim-013"],
            "source": "Leviathan, Part II, Chapters 17-19"
        },
        {
            "id": "hobbes-kw-004",
            "thinker_id": "hobbes",
            "term": "자연법 (Law of Nature)",
            "term_original": "lex naturalis / law of nature",
            "definition": (
                "이성에 의해 발견된 일반 규칙으로, 자기 생명에 파괴적인 것을 하지 말라고 명한다. "
                "제1자연법: 평화를 추구하라. 제2자연법: 평화를 위해 자연권을 상호 포기하라. "
                "제3자연법: 맺은 약속을 이행하라(=정의). "
                "자연법은 주권자의 강제력이 있어야 실효적이다."
            ),
            "related_claims": ["hobbes-claim-003", "hobbes-claim-010"],
            "source": "Leviathan, Part I, Chapters 14-15"
        },
        {
            "id": "hobbes-kw-005",
            "thinker_id": "hobbes",
            "term": "자연권 (Right of Nature)",
            "term_original": "jus naturale / right of nature",
            "definition": (
                "자기보존을 위해 자신의 힘을 원하는 대로 사용할 수 있는 자유. "
                "자연 상태에서는 모든 것에 대한 권리(right to all things)를 포함한다. "
                "자연법(의무)과 구별되는 개념으로, 자연권은 자유(liberty)이고 자연법은 의무(obligation)이다."
            ),
            "related_claims": ["hobbes-claim-002", "hobbes-claim-007"],
            "source": "Leviathan, Part I, Chapter 14"
        },
        {
            "id": "hobbes-kw-006",
            "thinker_id": "hobbes",
            "term": "리바이어던 (Leviathan)",
            "term_original": "Leviathan",
            "definition": (
                "구약성서 욥기에 나오는 바다 괴물의 이름으로, 홉스가 국가(커먼웰스)를 상징하는 데 사용했다. "
                "인공 인간(artificial man)이자 '가사적 신(mortal god)'으로, "
                "개인들의 사회계약에 의해 창조되며 그들을 보호하고 평화를 유지하는 역할을 한다. "
                "리바이어던의 표지에 그려진 거대한 인간 형상은 무수한 개인들의 신체로 구성되어 있다."
            ),
            "related_claims": ["hobbes-claim-008"],
            "source": "Leviathan, Introduction"
        },
        {
            "id": "hobbes-kw-007",
            "thinker_id": "hobbes",
            "term": "대리 (Authorization)",
            "term_original": "authorization",
            "definition": (
                "사회계약에서 핵심적인 행위로, 신민이 주권자를 자신의 대리인(actor)으로 임명하여 "
                "주권자의 모든 행위를 자기 자신의 행위로 인정하는 것. "
                "대리에 의해 다수의 개인이 하나의 인격(커먼웰스)으로 통합된다. "
                "현대 대의민주주의(representative democracy)의 개념적 선구."
            ),
            "related_claims": ["hobbes-claim-004", "hobbes-claim-006"],
            "source": "Leviathan, Part I, Chapter 16; Part II, Chapter 17"
        },
        {
            "id": "hobbes-kw-008",
            "thinker_id": "hobbes",
            "term": "커먼웰스 (Commonwealth)",
            "term_original": "Commonwealth / Civitas",
            "definition": (
                "사회계약에 의해 수립된 정치 공동체(국가). "
                "인공 인간(artificial man)으로 비유되며, 주권자가 그 영혼이다. "
                "제도에 의한 커먼웰스(by institution)와 정복에 의한 커먼웰스(by acquisition)가 있으며, "
                "두 경우 모두 동의(consent)에 기초하므로 정당하다."
            ),
            "related_claims": ["hobbes-claim-004", "hobbes-claim-008", "hobbes-claim-014"],
            "source": "Leviathan, Part II, Chapters 17-20"
        },
        {
            "id": "hobbes-kw-009",
            "thinker_id": "hobbes",
            "term": "만인에 대한 만인의 투쟁 (Bellum Omnium Contra Omnes)",
            "term_original": "bellum omnium contra omnes / war of every man against every man",
            "definition": (
                "자연 상태에서의 인간 조건을 기술하는 홉스의 핵심 개념. "
                "실제의 전투(fighting)뿐 아니라 전투 의지가 알려진 상태(known disposition to fight)도 "
                "전쟁에 해당한다. 이 상태에서는 정의·불의, 소유권, 산업, 문화 등이 존재하지 않는다. "
                "사회계약과 주권자 수립의 필요성을 논증하는 출발점이다."
            ),
            "related_claims": ["hobbes-claim-001"],
            "source": "Leviathan, Part I, Chapter 13; De Cive, Chapter 1"
        },
        {
            "id": "hobbes-kw-010",
            "thinker_id": "hobbes",
            "term": "자기보존 (Self-Preservation)",
            "term_original": "self-preservation",
            "definition": (
                "인간의 가장 근본적인 자연적 경향성이자 자연권의 핵심. "
                "홉스 정치철학 전체의 동기적 토대로, 자연법, 사회계약, 주권자론 모두가 "
                "궁극적으로 자기보존이라는 목적에 봉사한다. "
                "자기보존의 권리는 양도 불가능하며, 주권자가 직접 생명을 위협할 때 "
                "신민은 저항할 수 있다."
            ),
            "related_claims": ["hobbes-claim-002", "hobbes-claim-007"],
            "source": "Leviathan, Part I, Chapter 14; Part II, Chapter 21"
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """홉스 관계 데이터 입력."""
    relations = [
        {
            "id": "relation-hobbes-locke",
            "from_thinker": "hobbes",
            "to_thinker": "locke",
            "type": "influenced",
            "description": (
                "홉스의 자연 상태론과 사회계약론은 로크(John Locke, 1632~1704)에게 직접적 영향을 미쳤다. "
                "로크는 '통치론 제2론'(Two Treatises of Government, 1689)에서 "
                "홉스의 문제 설정(자연 상태에서 정치 사회로의 이행)을 수용하면서도, "
                "자연 상태를 전쟁 상태가 아니라 자연법이 지배하는 상태로, "
                "주권자를 절대적 존재가 아니라 인민의 신탁(trust)을 받은 존재로 재해석했다. "
                "홉스의 절대주권론에 대한 비판적 계승이다."
            ),
            "strength": "강함",
            "period": "17세기"
        },
        {
            "id": "relation-hobbes-rousseau",
            "from_thinker": "hobbes",
            "to_thinker": "rousseau",
            "type": "influenced",
            "description": (
                "루소(Jean-Jacques Rousseau, 1712~1778)는 홉스의 사회계약론을 비판적으로 계승했다. "
                "'인간 불평등 기원론'(1755)에서 루소는 홉스가 문명화된 인간의 악덕을 "
                "자연 상태의 인간에게 잘못 투사했다고 비판했다. "
                "'사회계약론'(1762)에서는 홉스와 달리 주권을 인민 전체(일반의지)에 두고, "
                "주권의 양도와 대표를 거부했다. "
                "홉스의 문제(자유와 질서의 양립)를 공유하되 해법을 근본적으로 달리한다."
            ),
            "strength": "강함",
            "period": "18세기"
        },
        {
            "id": "relation-hobbes-rawls",
            "from_thinker": "hobbes",
            "to_thinker": "rawls",
            "type": "influenced",
            "description": (
                "롤스(John Rawls, 1921~2002)는 '정의론'(A Theory of Justice, 1971)에서 "
                "홉스의 사회계약론 전통을 더 추상적인 수준에서 계승했다. "
                "원초적 입장(original position)은 홉스의 자연 상태에 대응하며, "
                "정의 원칙에 대한 합의는 사회계약에 대응한다. "
                "그러나 롤스는 홉스와 달리 합리적 자기이익(rational self-interest)만이 아니라 "
                "합리성과 공정성(fairness)의 결합에 기초한 계약을 구상했다."
            ),
            "strength": "보통",
            "period": "20세기"
        },
        {
            "id": "relation-machiavelli-hobbes",
            "from_thinker": "machiavelli",
            "to_thinker": "hobbes",
            "type": "influenced",
            "description": (
                "마키아벨리(Niccolò Machiavelli, 1469~1527)의 현실주의적 정치론은 "
                "홉스에게 간접적 영향을 미쳤다. "
                "마키아벨리의 '군주론'(Il Principe, 1532)에서 나타나는 "
                "정치를 도덕·종교로부터 독립된 자율적 영역으로 보는 관점, "
                "권력의 현실적 작동에 대한 관심, 인간 본성에 대한 비관적 시각은 "
                "홉스의 정치적 현실주의에 선행한다. "
                "다만 홉스는 마키아벨리와 달리 정치학의 과학적(기하학적) 정초를 시도했다."
            ),
            "strength": "보통",
            "period": "16~17세기"
        },
        {
            "id": "relation-hobbes-spinoza",
            "from_thinker": "hobbes",
            "to_thinker": "spinoza",
            "type": "influenced",
            "description": (
                "스피노자(Baruch Spinoza, 1632~1677)는 홉스의 자연권론과 사회계약론에서 "
                "직접적 영향을 받았다. '신학정치론'(Tractatus Theologico-Politicus, 1670)에서 "
                "스피노자는 홉스와 유사하게 자연권을 힘(potentia)과 동일시하고, "
                "사회계약에 의한 국가 수립을 논한다. "
                "그러나 스피노자는 홉스와 달리 사상의 자유와 표현의 자유를 "
                "국가의 목적으로 강조했다."
            ),
            "strength": "강함",
            "period": "17세기"
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
    r = client.get(index=INDEX_THINKERS, id="hobbes")
    print(f"[thinker] hobbes: name={r['_source']['name_en']}, era={r['_source']['era']}, field={r['_source']['field']}")

    # field 확인
    try:
        f = client.get(index=INDEX_FIELDS, id="political_philosophy")
        print(f"[field] political_philosophy: name={f['_source']['name']}")
    except Exception:
        print("[field] political_philosophy: NOT FOUND")

    # works 확인
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "hobbes"}})
    print(f"[works] hobbes 저서 수: {works_count['count']}")
    works_result = client.search(
        index=INDEX_WORKS,
        query={"term": {"thinker_id": "hobbes"}},
        _source=["id", "title_original", "year"],
        size=10
    )
    for hit in works_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['title_original']} ({s['year']})")

    # claims 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "hobbes"}})
    print(f"[claims] hobbes 주장 수: {claims_count['count']}")
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "hobbes"}},
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
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "hobbes"}})
    print(f"[keywords] hobbes 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_count = client.count(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "hobbes"}},
            {"term": {"to_thinker": "hobbes"}}
        ]}}
    )
    print(f"[relations] hobbes 관련 관계 수: {rel_count['count']}")
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "hobbes"}},
            {"term": {"to_thinker": "hobbes"}}
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
        print("=== 토머스 홉스(Thomas Hobbes) 데이터 입력 시작 ===\n")

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
