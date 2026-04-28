"""장자크 루소(Jean-Jacques Rousseau) 데이터를 ES에 직접 입력하는 스크립트."""

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
    """루소 사상가 데이터 입력."""
    doc = {
        "id": "rousseau",
        "name": "장자크 루소",
        "name_en": "Jean-Jacques Rousseau",
        "field": "political_philosophy",
        "era": "계몽주의",
        "birth_year": 1712,
        "death_year": 1778,
        "background": (
            "제네바 공화국에서 시계공의 아들로 태어났다. 어머니는 출산 직후 사망했고, "
            "아버지는 루소가 10세 때 제네바를 떠나 사실상 고아로 자랐다. "
            "정규 교육을 거의 받지 못한 독학인으로, 방랑 생활을 하며 다양한 직업을 전전했다. "
            "바렌 부인(Madame de Warens)의 보호 아래 지적 성장을 이루었고, "
            "파리에서 디드로(Diderot), 달랑베르(d'Alembert) 등 백과전서파와 교류했으나 "
            "이후 결별했다. 테레즈 르바쇠르(Thérèse Levasseur)와 평생을 함께했으며, "
            "다섯 자녀를 모두 고아원에 보낸 것은 후일 큰 도덕적 비난의 대상이 되었다. "
            "말년에는 피해망상에 시달렸고, '고백록'과 '고독한 산책자의 몽상' 등 자전적 작품을 남겼다. "
            "1778년 에르므농빌(Ermenonville)에서 사망했으며, 프랑스 혁명 후 팡테옹에 안장되었다."
        ),
        "core_philosophy": (
            "루소의 핵심 사상은 자연 상태의 선량함과 문명에 의한 타락이라는 대립 구도에 기초한다. "
            "인간은 본성적으로 선하며(bon sauvage), 자기애(amour de soi)와 연민(pitié)이라는 "
            "두 가지 자연적 감정을 가지고 있다. 그러나 사유재산의 발생과 사회의 발전은 "
            "자존심(amour-propre)을 낳아 불평등, 예속, 도덕적 타락을 초래했다. "
            "이 타락에서 벗어나기 위해 루소는 사회계약을 통한 정치 공동체를 구상한다. "
            "일반의지(volonté générale)에 의해 통치되는 공동체에서 개인은 모든 권리를 "
            "공동체 전체에 양도하되, 동시에 자유와 평등을 보장받는다. "
            "'인간은 자유롭게 태어났으나, 어디에서나 쇠사슬에 묶여 있다'는 선언에서 "
            "자유의 상실과 회복이라는 루소 정치철학의 핵심 문제가 드러난다."
        ),
        "philosophical_journey": (
            "초기(~1749): 방랑과 독학의 시기. 바렌 부인 밑에서 음악, 문학, 철학을 공부하며 "
            "지적 기반을 형성했다. 파리로 이주하여 백과전서파와 교류했다. "
            "전환기(1749~1755): 디종 아카데미의 현상 논문 공모에 응모한 '학문예술론'(1750)에서 "
            "학문과 예술이 풍속을 타락시켰다는 역설적 주장으로 명성을 얻었다. "
            "'인간 불평등 기원론'(1755)에서 자연 상태론과 불평등 비판을 체계화했다. "
            "성숙기(1755~1762): '신엘로이즈'(1761)로 감성적 소설의 대표작을 남겼고, "
            "'사회계약론'(1762)에서 일반의지와 인민주권론을 전개했으며, "
            "'에밀'(1762)에서 자연에 따른 교육론을 제시했다. "
            "두 책 모두 파리 고등법원에 의해 금서 처분되어 스위스와 영국으로 망명해야 했다. "
            "후기(1762~1778): 망명과 고독의 시기. '고백록'(사후 1782 출판), "
            "'고독한 산책자의 몽상'(사후 1782 출판) 등 자전적 작품을 집필했다. "
            "피해망상이 심해졌으나, 내면 성찰의 깊이는 오히려 더해졌다."
        ),
        "keywords": [
            "자연 상태",
            "일반의지(volonté générale)",
            "사회계약",
            "자기애(amour de soi)",
            "자존심(amour-propre)",
            "인민주권",
            "소극적 교육",
            "불평등",
            "시민종교",
            "자유"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="rousseau", document=doc)
    print(f"[thinker] rousseau: {result['result']}")
    return result


def insert_works(client):
    """루소 저서 데이터 입력."""
    works = [
        {
            "id": "rousseau-social-contract",
            "thinker_id": "rousseau",
            "title": "사회계약론",
            "title_original": "Du Contrat social ou Principes du droit politique",
            "year": 1762,
            "significance": (
                "루소 정치철학의 대표작이자 근대 민주주의 사상의 초석. "
                "'인간은 자유롭게 태어났으나, 어디에서나 쇠사슬에 묶여 있다'는 유명한 첫 문장으로 시작한다. "
                "일반의지(volonté générale)에 기초한 정치 공동체의 원리를 전개하며, "
                "주권은 양도·분할 불가능하고 인민 전체에 귀속된다고 주장한다. "
                "4권으로 구성: 제1권 — 사회계약의 원리, 제2권 — 주권과 일반의지, "
                "제3권 — 정부의 형태, 제4권 — 투표·시민종교·독재관 등. "
                "프랑스 혁명에 지대한 영향을 미쳤으며, 파리 고등법원에 의해 금서 처분되었다."
            ),
            "key_concepts": [
                "일반의지", "사회계약", "주권", "인민주권", "시민종교",
                "자유와 복종의 양립", "입법자", "직접민주주의"
            ]
        },
        {
            "id": "rousseau-inequality",
            "thinker_id": "rousseau",
            "title": "인간 불평등 기원론",
            "title_original": "Discours sur l'origine et les fondements de l'inégalité parmi les hommes",
            "year": 1755,
            "significance": (
                "디종 아카데미의 현상 논문('인간 사이의 불평등의 기원은 무엇이며 자연법에 의해 허용되는가?')에 "
                "응모한 저작. 자연 상태의 인간(자연인)과 사회 상태의 인간(시민)을 대비하여, "
                "불평등이 자연적인 것이 아니라 사유재산과 사회 발전의 산물임을 논증한다. "
                "두 부분으로 구성: 제1부 — 자연 상태의 인간(자기애와 연민), "
                "제2부 — 불평등의 발생과 심화(사유재산, 정치적 불평등). "
                "마르크스의 소외론과 사유재산 비판의 선구적 저작으로 평가된다."
            ),
            "key_concepts": [
                "자연 상태", "자연인(homme naturel)", "자기애(amour de soi)",
                "자존심(amour-propre)", "연민(pitié)", "사유재산", "불평등"
            ]
        },
        {
            "id": "rousseau-emile",
            "thinker_id": "rousseau",
            "title": "에밀",
            "title_original": "Émile, ou De l'éducation",
            "year": 1762,
            "significance": (
                "루소의 교육론 대표작으로, 가상의 아이 에밀의 성장 과정을 통해 "
                "자연에 따른 교육(éducation selon la nature)의 원리를 전개한다. "
                "5권으로 구성: 제1~2권 — 유아기~소년기(감각 교육), "
                "제3권 — 소년기(실용적 학습), 제4권 — 청년기(도덕·종교 교육, '사부아 보좌신부의 신앙고백' 포함), "
                "제5권 — 소피(Sophie)와의 관계를 통한 시민 교육. "
                "소극적 교육(éducation négative): 자연의 발달 과정을 방해하지 않는 것이 교육의 핵심. "
                "'사부아 보좌신부의 신앙고백'이 가톨릭교회와 갈뱅파 모두의 분노를 사 금서 처분되었다."
            ),
            "key_concepts": [
                "소극적 교육", "자연에 따른 교육", "사부아 보좌신부의 신앙고백",
                "자연인과 시민의 긴장", "감각 교육", "자기애의 발전"
            ]
        },
        {
            "id": "rousseau-first-discourse",
            "thinker_id": "rousseau",
            "title": "학문예술론",
            "title_original": "Discours sur les sciences et les arts",
            "year": 1750,
            "significance": (
                "디종 아카데미의 현상 논문('학문과 예술의 부흥이 풍속을 순화하는 데 기여했는가?')에 "
                "응모하여 수상한 저작. '아니오'라는 역설적 답변으로 루소의 이름을 알렸다. "
                "학문과 예술의 발전이 덕(vertu)의 쇠퇴와 풍속의 타락을 가져왔다고 주장한다. "
                "스파르타의 소박한 덕과 아테네·로마의 문화적 화려함 속 도덕적 퇴폐를 대비시킨다. "
                "루소 사상의 출발점으로, 문명 비판과 자연 회귀라는 핵심 주제가 처음 등장한다."
            ),
            "key_concepts": [
                "문명 비판", "덕(vertu)의 쇠퇴", "학문과 도덕의 관계",
                "스파르타 대 아테네", "자연적 소박함"
            ]
        },
        {
            "id": "rousseau-confessions",
            "thinker_id": "rousseau",
            "title": "고백록",
            "title_original": "Les Confessions",
            "year": 1782,
            "significance": (
                "루소의 자서전으로, 사후에 출판되었다(제1~6권 1782, 제7~12권 1789). "
                "아우구스티누스의 '고백록'을 의식하면서도, 신 앞의 고백이 아닌 "
                "독자 앞의 솔직한 자기 폭로를 시도한다. "
                "'나는 있는 그대로의 나 자신을 보여주는 기획을 구상했다'는 선언으로 시작하며, "
                "어린 시절의 체벌 경험에서 성적 취향, 자녀 유기에 이르기까지 "
                "당시로서는 파격적인 자기 고백을 담고 있다. "
                "근대적 자서전 문학의 선구이자, 주관성과 감성을 중시하는 낭만주의의 출발점으로 평가된다."
            ),
            "key_concepts": [
                "자기 고백", "투명성(transparence)", "진정성(authenticité)",
                "내면 성찰", "감성(sensibilité)"
            ]
        },
        {
            "id": "rousseau-julie",
            "thinker_id": "rousseau",
            "title": "신엘로이즈",
            "title_original": "Julie, ou la nouvelle Héloïse",
            "year": 1761,
            "significance": (
                "서간체 소설로, 18세기 유럽에서 가장 많이 팔린 소설 중 하나. "
                "귀족 여성 줄리(Julie)와 평민 가정교사 생프뢰(Saint-Preux)의 사랑을 다룬다. "
                "신분 차이에 의한 비극적 사랑, 덕(vertu)과 정념(passion)의 갈등, "
                "자연 속의 이상적 공동체(클라랑, Clarens) 등을 그린다. "
                "루소의 감성주의와 자연 회귀 사상이 문학적으로 형상화된 작품이며, "
                "낭만주의 소설의 선구로 평가된다."
            ),
            "key_concepts": [
                "감성(sensibilité)", "덕과 정념의 갈등", "자연 회귀",
                "이상적 공동체(클라랑)", "서간체 소설"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """루소 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 자연 상태 — 자유롭고 선량한 미개인
        {
            "id": "rousseau-claim-001",
            "thinker_id": "rousseau",
            "work_id": "rousseau-inequality",
            "source_detail": "Discours sur l'inégalité, Première partie",
            "claim": (
                "자연 상태의 인간(l'homme naturel)은 자유롭고 선량한 존재(bon sauvage)이다. "
                "자연인은 자기보존 본능인 자기애(amour de soi)와 타인의 고통에 대한 "
                "자연적 감정인 연민(pitié)만을 가지며, 도덕적으로 선하지도 악하지도 않은 "
                "전-도덕적(pré-moral) 상태에 있다."
            ),
            "original_text": (
                "L'homme naissant n'a point été méchant, parce qu'il n'a point connu ce que c'est "
                "qu'être bon ou méchant... les sauvages ne sont pas méchants précisément parce qu'ils "
                "ne savent pas ce que c'est qu'être bons."
            ),
            "original_text_ko": (
                "태어나는 인간은 악하지 않았다. 왜냐하면 그는 선하다는 것이나 악하다는 것이 "
                "무엇인지 알지 못했기 때문이다... 미개인들이 악하지 않은 것은 정확히 "
                "선하다는 것이 무엇인지 모르기 때문이다."
            ),
            "explanation": (
                "루소의 자연 상태론은 홉스의 그것과 근본적으로 다르다. "
                "홉스가 자연 상태를 만인에 대한 만인의 투쟁으로 묘사한 반면, "
                "루소는 자연인을 고립되어 살며 타인과 갈등할 이유가 없는 평화로운 존재로 그린다. "
                "자연인은 이성이 아직 발달하지 않았으므로 욕망도 단순하며, "
                "자기보존에 필요한 것 이상을 원하지 않는다. "
                "연민은 이성보다 앞선 자연적 감정으로, 타인의 고통을 보면 불쾌감을 느끼게 한다."
            ),
            "argument": (
                "(1) 홉스는 자연 상태의 인간에게 문명인의 욕망(허영, 경쟁, 소유욕)을 잘못 투사했다. "
                "(2) 자연인은 고립적으로 살며 타인과 지속적 관계를 맺지 않으므로 갈등의 원인이 없다. "
                "(3) 자연인의 욕구는 자기보존에 한정되며, 이는 자연이 충분히 충족시켜준다. "
                "(4) 연민(pitié)은 이성보다 앞선 자연적 감정으로, 타인에 대한 공격성을 억제한다. "
                "(5) 따라서 자연 상태는 전쟁이 아니라 평화의 상태이다."
            ),
            "counterpoint": (
                "토머스 홉스(Thomas Hobbes)는 '리바이어던'(Leviathan, 1651) 제13장에서 "
                "자연 상태를 만인에 대한 만인의 투쟁으로 묘사하며, 인간의 자연적 평등이 "
                "오히려 상호 불신과 선제공격의 합리성을 낳는다고 주장했다. "
                "또한 볼테르(Voltaire)는 루소의 자연인 이상화를 풍자하며, "
                "'당신의 책을 읽으면 네 발로 걷고 싶어진다'고 비꼬았다. "
                "현대 인류학은 수렵-채집 사회에서도 집단 간 폭력이 존재했음을 보여주어 "
                "루소의 평화로운 자연 상태론에 의문을 제기한다."
            ),
            "context": (
                "디종 아카데미의 현상 공모 '인간 사이 불평등의 기원'에 대한 응답으로 집필되었다. "
                "루소는 '학문예술론'(1750)에서 제기한 문명 비판을 심화시켜, "
                "불평등의 기원을 자연이 아닌 사회에서 찾고자 했다."
            ),
            "keywords": ["자연 상태", "자연인", "자기애(amour de soi)", "연민(pitié)", "bon sauvage"],
            "verified": False
        },
        # CLAIM-002: 사회적 불평등의 기원 — 사유재산
        {
            "id": "rousseau-claim-002",
            "thinker_id": "rousseau",
            "work_id": "rousseau-inequality",
            "source_detail": "Discours sur l'inégalité, Seconde partie",
            "claim": (
                "사회적 불평등은 사유재산의 발생에서 비롯되었다. "
                "'최초로 한 토지에 울타리를 치고 이것은 내 것이라고 말할 생각을 한 사람'이 "
                "시민사회의 진정한 창시자이며, 이로부터 모든 불평등과 예속이 시작되었다."
            ),
            "original_text": (
                "Le premier qui, ayant enclos un terrain, s'avisa de dire : Ceci est à moi, "
                "et trouva des gens assez simples pour le croire, fut le vrai fondateur de la société civile. "
                "Que de crimes, de guerres, de meurtres, que de misères et d'horreurs n'eût point épargnés "
                "au genre humain celui qui, arrachant les pieux ou comblant le fossé, eût crié à ses "
                "semblables : Gardez-vous d'écouter cet imposteur."
            ),
            "original_text_ko": (
                "한 토지에 울타리를 치고서 '이것은 내 것이다'라고 말할 생각을 처음으로 한 사람, "
                "그리고 그것을 믿을 만큼 순진한 사람들을 발견한 사람이 시민사회의 진정한 창시자였다. "
                "말뚝을 뽑아버리거나 도랑을 메우면서 동료들에게 '이 사기꾼의 말을 듣지 마시오'라고 "
                "외쳤다면, 얼마나 많은 범죄, 전쟁, 살인, 비참과 공포를 인류에게 면하게 해주었을 것인가."
            ),
            "explanation": (
                "루소에 따르면 불평등에는 두 종류가 있다: 자연적(신체적) 불평등과 도덕적(정치적) 불평등. "
                "자연적 불평등은 나이, 건강, 체력 등의 차이이며, "
                "도덕적 불평등은 부, 권력, 지위의 차이로 사회적으로 만들어진 것이다. "
                "사유재산의 등장은 인간을 상호 의존적으로 만들었고, "
                "부자는 자신의 재산을 보호하기 위해 법과 국가를 만들어 "
                "불평등을 제도화하고 정당화했다."
            ),
            "argument": (
                "(1) 자연 상태에서는 사유재산이 없었고, 각자 필요한 만큼만 취했다. "
                "(2) 야금술과 농업의 발전이 토지의 경작과 분배를 가져왔다. "
                "(3) 사유재산은 부와 빈곤의 분화를 낳았다. "
                "(4) 부자들은 자신의 재산을 보호하기 위해 법과 정치 사회의 수립을 제안했다. "
                "(5) 이는 겉으로는 모두의 이익을 위한 것처럼 보이지만, "
                "실제로는 기존 불평등을 고정화하고 정당화하는 기만적 계약이었다. "
                "(6) 이로써 자연적 자유가 상실되고 예속이 영구화되었다."
            ),
            "counterpoint": (
                "존 로크(John Locke)는 '통치론 제2론'(Two Treatises of Government, Second Treatise, 1689) "
                "제5장에서 사유재산을 자연권으로 정당화했다. 노동을 통해 자연물에 자신의 것을 섞으면 "
                "그것은 정당한 소유가 된다는 노동 혼합 이론(labor-mixing theory)을 제시했다. "
                "로크에게 사유재산은 불평등의 원인이 아니라 자유의 조건이다. "
                "또한 데이비드 흄(David Hume)은 사유재산이 사회적 편의(convention)에 의해 "
                "발생한 것이며, 사회의 안정과 번영을 위해 필수적이라고 보았다."
            ),
            "context": (
                "18세기 유럽의 경제적 불평등 심화와 농업 사회에서 상업 사회로의 전환이 배경이다. "
                "루소는 로크의 소유권 이론과 자연법 전통에 대한 급진적 비판을 시도했다."
            ),
            "keywords": ["사유재산", "불평등", "시민사회", "도덕적 불평등", "자연적 불평등"],
            "verified": False
        },
        # CLAIM-003: 일반의지(volonté générale)
        {
            "id": "rousseau-claim-003",
            "thinker_id": "rousseau",
            "work_id": "rousseau-social-contract",
            "source_detail": "Du Contrat social, Livre II, Chapitres 1-3",
            "claim": (
                "일반의지(volonté générale)는 공동체 전체의 공동선(bien commun)을 지향하는 의지이며, "
                "전체의지(volonté de tous)와 구별된다. 전체의지는 개별 의지의 단순 합산이지만, "
                "일반의지는 개별 의지에서 서로 상쇄되는 과부족을 제거한 후 남는 것이다."
            ),
            "original_text": (
                "Il y a souvent bien de la différence entre la volonté de tous et la volonté générale ; "
                "celle-ci ne regarde qu'à l'intérêt commun, l'autre regarde à l'intérêt privé, "
                "et n'est qu'une somme de volontés particulières : mais ôtez de ces mêmes volontés "
                "les plus et les moins qui s'entredétruisent, reste pour somme des différences la volonté générale."
            ),
            "original_text_ko": (
                "전체의지와 일반의지 사이에는 흔히 큰 차이가 있다. "
                "일반의지는 오직 공동의 이익만을 고려하고, 전체의지는 사적 이익을 고려하며 "
                "개별 의지의 합에 불과하다. 그러나 이 개별 의지들에서 서로 상쇄되는 "
                "과부족을 제거하면, 차이의 합으로 일반의지가 남는다."
            ),
            "explanation": (
                "일반의지는 루소 정치철학의 핵심 개념이다. "
                "전체의지가 개인들의 사적 이익의 합이라면, 일반의지는 공동체 구성원으로서의 "
                "각 개인이 공동선을 향해 갖는 의지이다. "
                "일반의지는 항상 옳고(toujours droite) 공공의 유용을 지향하지만, "
                "인민의 심의(délibération)가 항상 일반의지를 올바르게 표현하는 것은 아니다. "
                "일반의지는 투표의 다수결로 근사적으로 파악할 수 있으나, "
                "파벌이나 부분적 결사가 존재하면 왜곡될 수 있다."
            ),
            "argument": (
                "(1) 사회계약에 의해 각 개인은 공동체의 일원이 된다. "
                "(2) 공동체 일원으로서 개인은 사적 이익(volonté particulière)뿐 아니라 "
                "공동선에 대한 의지(volonté générale)를 가진다. "
                "(3) 전체의지는 사적 이익의 합이므로 공동선과 일치하지 않을 수 있다. "
                "(4) 그러나 개별 의지들 사이의 차이(과부족)를 제거하면 공동선을 향한 의지가 남는다. "
                "(5) 일반의지는 주권의 행사이며, 법의 근거이다. "
                "(6) 따라서 일반의지에 따르는 것이 곧 자유이다."
            ),
            "counterpoint": (
                "벤자민 콩스탕(Benjamin Constant)은 '근대인의 자유와 고대인의 자유의 비교'(1819)에서 "
                "루소의 일반의지 개념이 개인의 자유를 집단의 의지에 종속시킬 위험이 있다고 비판했다. "
                "이사야 벌린(Isaiah Berlin)은 '자유의 두 개념'(Two Concepts of Liberty, 1958)에서 "
                "루소의 적극적 자유 개념이 전체주의로 귀결될 수 있다고 경고했다. "
                "또한 슘페터(Joseph Schumpeter)는 일반의지라는 개념 자체가 경험적으로 확인 불가능한 "
                "형이상학적 허구라고 비판했다."
            ),
            "context": (
                "루소는 제네바 공화국의 직접민주주의 전통과 고대 로마 공화정의 시민적 덕을 "
                "이상으로 삼았다. 일반의지 개념은 몽테스키외의 '법의 정신'(1748)과 "
                "디드로의 '백과전서'에서 영향을 받으면서도 독자적으로 발전시킨 것이다."
            ),
            "keywords": ["일반의지", "전체의지", "공동선", "주권", "시민적 자유"],
            "verified": False
        },
        # CLAIM-004: 사회계약 — 자유의 양도가 아닌 자유의 보장
        {
            "id": "rousseau-claim-004",
            "thinker_id": "rousseau",
            "work_id": "rousseau-social-contract",
            "source_detail": "Du Contrat social, Livre I, Chapitres 6-8",
            "claim": (
                "사회계약은 각 구성원이 자신의 모든 권리를 공동체 전체에 양도하는 것이지만, "
                "이 양도는 자유의 상실이 아니라 자유의 보장이다. "
                "자연적 자유(liberté naturelle)를 잃는 대신 시민적 자유(liberté civile)와 "
                "도덕적 자유(liberté morale)를 얻는다."
            ),
            "original_text": (
                "Trouver une forme d'association qui défende et protège de toute la force commune "
                "la personne et les biens de chaque associé, et par laquelle chacun s'unissant à tous "
                "n'obéisse pourtant qu'à lui-même et reste aussi libre qu'auparavant."
            ),
            "original_text_ko": (
                "각 구성원의 인격과 재산을 공동의 힘 전체로 방어하고 보호하며, "
                "각자가 모두와 결합하면서도 오직 자기 자신에게만 복종하고 "
                "이전과 마찬가지로 자유로운 결합의 형태를 찾는 것."
            ),
            "explanation": (
                "루소의 사회계약은 홉스나 로크의 사회계약과 근본적으로 다르다. "
                "홉스에서 사회계약은 자연권을 주권자에게 양도하는 것이고, "
                "로크에서는 자연권의 일부를 정부에 위탁하는 것이다. "
                "루소에서는 각 개인이 자신의 모든 권리를 공동체 전체(일반의지)에 양도하되, "
                "모두가 동등하게 양도하므로 누구도 타인에게 종속되지 않는다. "
                "이 양도를 통해 자연적 자유(무제한적이나 불안정한)를 잃지만, "
                "시민적 자유(법에 의해 보장되는)와 도덕적 자유(자기가 부과한 법에 복종하는)를 얻는다."
            ),
            "argument": (
                "(1) 자연 상태에서의 자유는 무제한적이나, 물리적 힘에 의해 언제든 침해될 수 있다. "
                "(2) 사회계약의 근본 문제: 자유를 보장하면서 결합할 형태를 찾는 것. "
                "(3) 해법: 각 개인이 모든 권리를 공동체 전체에 양도한다. "
                "(4) 양도가 전면적이므로 조건이 모두에게 동등하고, 누구도 타인에게 종속되지 않는다. "
                "(5) 자연적 자유를 잃지만 시민적 자유(소유권을 포함)를 얻는다. "
                "(6) 또한 도덕적 자유—자기가 부과한 법에 복종하는 것—를 얻으며, "
                "이것만이 인간을 진정으로 자기 자신의 주인으로 만든다."
            ),
            "counterpoint": (
                "토머스 홉스(Thomas Hobbes)는 '리바이어던'(Leviathan, 1651) 제17장에서 "
                "사회계약은 자연권을 하나의 주권자에게 양도하는 것이며, 주권자는 계약 당사자가 아니라고 보았다. "
                "홉스에게 계약의 목적은 자유의 보장이 아니라 안전(자기보존)의 확보이다. "
                "벤자민 콩스탕(Benjamin Constant)은 루소의 전면적 양도가 "
                "개인의 독립적 영역을 말살할 수 있다고 비판하며, "
                "국가 권력에 대한 개인적 자유의 한계를 설정할 필요가 있다고 주장했다."
            ),
            "context": (
                "루소는 당시 절대왕정과 봉건적 예속에 맞서 "
                "자유와 평등에 기초한 정치 공동체의 가능성을 모색했다. "
                "동시에 홉스의 절대주권론과 로크의 제한적 정부론 모두를 비판적으로 극복하고자 했다."
            ),
            "keywords": ["사회계약", "자연적 자유", "시민적 자유", "도덕적 자유", "양도"],
            "verified": False
        },
        # CLAIM-005: "인간은 자유롭게 태어났으나, 어디에서나 쇠사슬에 묶여 있다"
        {
            "id": "rousseau-claim-005",
            "thinker_id": "rousseau",
            "work_id": "rousseau-social-contract",
            "source_detail": "Du Contrat social, Livre I, Chapitre 1",
            "claim": (
                "인간은 자유롭게 태어났으나, 어디에서나 쇠사슬에 묶여 있다. "
                "이 쇠사슬을 정당화할 수 있는 것은 오직 사회계약뿐이며, "
                "힘이나 전통은 정당한 근거가 될 수 없다."
            ),
            "original_text": (
                "L'homme est né libre, et partout il est dans les fers. "
                "Tel se croit le maître des autres, qui ne laisse pas d'être plus esclave qu'eux. "
                "Comment ce changement s'est-il fait ? Je l'ignore. "
                "Qu'est-ce qui peut le rendre légitime ? Je crois pouvoir résoudre cette question."
            ),
            "original_text_ko": (
                "인간은 자유롭게 태어났으나, 어디에서나 쇠사슬에 묶여 있다. "
                "자기가 다른 사람들의 주인이라고 믿는 자도 그들보다 더 노예인 것은 마찬가지다. "
                "이 변화는 어떻게 일어났는가? 나는 모른다. "
                "무엇이 그것을 정당화할 수 있는가? 나는 이 문제를 풀 수 있다고 믿는다."
            ),
            "explanation": (
                "사회계약론의 유명한 첫 문장으로, 루소 정치철학의 핵심 문제를 집약한다. "
                "인간은 본성상 자유로운 존재이지만, 현실의 모든 사회에서 예속 상태에 놓여 있다. "
                "루소의 과제는 이 예속의 역사적 기원을 설명하는 것이 아니라, "
                "그것을 정당화할 수 있는 원리—즉 사회계약—를 제시하는 것이다. "
                "주인이 노예보다 더 노예라는 역설은 지배자도 지배 관계에 종속되어 있음을 뜻한다."
            ),
            "argument": (
                "(1) 인간은 본성적으로 자유롭게 태어난다(자연적 자유). "
                "(2) 그러나 현실의 모든 사회에서 인간은 다양한 형태의 예속 상태에 있다. "
                "(3) 힘에 의한 지배는 권리를 만들지 않는다(le plus fort n'est jamais assez fort). "
                "(4) 자유의 양도(포기)는 인간의 자격 자체의 포기이므로 불가능하다. "
                "(5) 따라서 정당한 사회질서는 오직 합의(convention), 즉 사회계약에 의해서만 가능하다."
            ),
            "counterpoint": (
                "로버트 필머(Robert Filmer)는 '가부장론'(Patriarcha, 1680)에서 "
                "왕권은 아담으로부터 내려온 자연적 권위이며, 사회계약은 허구라고 주장했다. "
                "존 로크(John Locke)도 '통치론 제1론'에서 필머를 반박했지만, "
                "루소와 달리 자유의 제한적 양도만을 인정했다. "
                "데이비드 흄(David Hume)은 '원초적 계약에 관하여'(Of the Original Contract, 1748)에서 "
                "역사적으로 실제 사회계약이 체결된 적이 없으며, "
                "정치적 복종의 근거는 계약이 아니라 관습과 편의라고 비판했다."
            ),
            "context": (
                "사회계약론의 서두로, 루소가 정치적 정당성의 문제를 제기하는 출발점이다. "
                "그로티우스, 홉스, 로크 등 선행 사회계약론자들의 이론을 비판적으로 검토하며, "
                "자신의 독자적 사회계약론을 전개할 토대를 놓는다."
            ),
            "keywords": ["자유", "쇠사슬", "정당성", "사회계약", "힘과 권리"],
            "verified": False
        },
        # CLAIM-006: 자유와 복종의 양립 — "자기 자신에게만 복종하는 것이 자유"
        {
            "id": "rousseau-claim-006",
            "thinker_id": "rousseau",
            "work_id": "rousseau-social-contract",
            "source_detail": "Du Contrat social, Livre I, Chapitre 8",
            "claim": (
                "도덕적 자유(liberté morale)란 자기 자신이 부과한 법에 복종하는 것이다. "
                "일반의지에 따르는 것은 타율이 아니라 자율이며, "
                "이것만이 인간을 진정으로 자기 자신의 주인으로 만든다."
            ),
            "original_text": (
                "On pourrait sur ce qui précède ajouter à l'acquis de l'état civil la liberté morale, "
                "qui seule rend l'homme vraiment maître de lui ; car l'impulsion du seul appétit est esclavage, "
                "et l'obéissance à la loi qu'on s'est prescrite est liberté."
            ),
            "original_text_ko": (
                "앞에서 말한 것에 더하여 시민 상태의 획득물에 도덕적 자유를 보탤 수 있는데, "
                "이것만이 인간을 진정으로 자기 자신의 주인으로 만든다. "
                "왜냐하면 단순한 욕구의 충동은 노예 상태이고, "
                "자기가 스스로에게 부과한 법에 복종하는 것이 자유이기 때문이다."
            ),
            "explanation": (
                "루소는 세 종류의 자유를 구별한다: 자연적 자유(자연 상태에서의 무제한적 자유), "
                "시민적 자유(법에 의해 보장되는 자유), 도덕적 자유(자기 입법에 의한 자유). "
                "도덕적 자유는 루소 정치철학에서 가장 높은 형태의 자유이다. "
                "단순한 욕구에 따르는 것은 자유가 아니라 노예 상태이며, "
                "이성과 양심에 따라 자기가 부과한 법에 복종하는 것이 진정한 자유이다. "
                "이 개념은 칸트의 자율성(Autonomie) 개념에 직접적 영감을 주었다."
            ),
            "argument": (
                "(1) 자연적 자유는 물리적 힘에 의해서만 제한되며 불안정하다. "
                "(2) 시민적 자유는 일반의지(법)에 의해 제한되지만 안정적이다. "
                "(3) 도덕적 자유는 자기가 스스로에게 부과한 법에 복종하는 것이다. "
                "(4) 단순한 욕구(appétit)에 끌려다니는 것은 자유가 아니라 예속이다. "
                "(5) 이성과 양심에 따라 행위하는 것, 즉 자기 입법(auto-législation)만이 진정한 자유이다. "
                "(6) 일반의지에 따르는 것은 곧 자기 자신의 의지에 따르는 것이므로 자유이다."
            ),
            "counterpoint": (
                "이사야 벌린(Isaiah Berlin)은 '자유의 두 개념'(Two Concepts of Liberty, 1958)에서 "
                "루소의 도덕적 자유 개념을 '적극적 자유(positive liberty)'의 전형으로 분류하고, "
                "이것이 개인을 '진정한 자아'의 이름으로 강제할 수 있는 위험을 내포한다고 경고했다. "
                "'자유롭도록 강제된다(forcé d'être libre)'는 루소 자신의 표현(사회계약론 I, 7)이 "
                "이 위험을 단적으로 보여준다. 콩스탕 역시 루소의 자유가 고대적 집단적 자유이며, "
                "근대적 개인적 자유와 양립하기 어렵다고 비판했다."
            ),
            "context": (
                "사회계약론 제1권 제8장 '시민 상태에 관하여'에서 자연 상태에서 시민 상태로의 "
                "이행이 인간에게 가져다주는 변화를 서술하는 맥락이다. "
                "루소는 이 이행이 단순한 계약적 교환이 아니라 인간의 도덕적 변형(transformation morale)이라고 본다."
            ),
            "keywords": ["도덕적 자유", "자율", "자기 입법", "시민적 자유", "자연적 자유"],
            "verified": False
        },
        # CLAIM-007: 주권론 — 주권은 양도·분할 불가, 인민주권
        {
            "id": "rousseau-claim-007",
            "thinker_id": "rousseau",
            "work_id": "rousseau-social-contract",
            "source_detail": "Du Contrat social, Livre II, Chapitres 1-2",
            "claim": (
                "주권(souveraineté)은 일반의지의 행사이며, 양도될 수도 분할될 수도 없다. "
                "주권은 인민 전체에 귀속되며, 대표(représentation)될 수 없다."
            ),
            "original_text": (
                "Je dis donc que la souveraineté n'étant que l'exercice de la volonté générale "
                "ne peut jamais s'aliéner, et que le souverain, qui n'est qu'un être collectif, "
                "ne peut être représenté que par lui-même."
            ),
            "original_text_ko": (
                "따라서 나는 주권이란 일반의지의 행사에 불과하므로 결코 양도될 수 없으며, "
                "주권자는 집합적 존재에 불과하므로 오직 자기 자신에 의해서만 대표될 수 있다고 말한다."
            ),
            "explanation": (
                "루소에게 주권자(souverain)는 사회계약에 의해 결합된 인민 전체이다. "
                "주권은 일반의지의 행사이므로, 의지를 양도할 수 없는 것처럼 주권도 양도할 수 없다. "
                "주권의 분할(예: 입법·사법·행정의 분리)은 주권의 파괴이다. "
                "루소는 몽테스키외의 권력분립론을 암묵적으로 비판하며, "
                "주권의 단일성과 불가분성을 강조한다. "
                "정부(gouvernement)는 주권자와 구별되는 집행 기관에 불과하며, "
                "인민의 위임을 받은 관리(magistrats)이지 대표(représentants)가 아니다."
            ),
            "argument": (
                "(1) 주권은 일반의지의 행사이다. "
                "(2) 의지는 양도될 수 없다: 누군가의 의지가 나의 의지를 대신할 수는 없다. "
                "(3) 따라서 주권도 양도될 수 없으며, 인민 전체에만 귀속된다. "
                "(4) 주권은 분할될 수 없다: 일반의지는 전체적이거나 아무것도 아니다. "
                "(5) 정부는 주권자(인민)와 신민(sujet) 사이의 중개 기관일 뿐이다. "
                "(6) 대의(représentation)는 주권의 포기이며, 대표자가 스스로의 이익을 추구하면 "
                "일반의지는 왜곡된다."
            ),
            "counterpoint": (
                "몽테스키외(Montesquieu)는 '법의 정신'(De l'esprit des lois, 1748)에서 "
                "권력분립(séparation des pouvoirs)을 자유의 조건으로 제시했는데, "
                "이는 루소의 주권 불가분론과 정면으로 충돌한다. "
                "존 로크(John Locke)도 '통치론 제2론'에서 입법권과 집행권의 분리를 주장했다. "
                "매디슨(James Madison)은 '연방주의자 논문'(Federalist Papers, No. 10, 1787)에서 "
                "대의제가 직접민주주의보다 파벌의 위험을 더 잘 통제할 수 있다고 반박했다."
            ),
            "context": (
                "루소는 제네바 공화국의 소규모 직접민주주의를 이상으로 삼았다. "
                "당시 유럽의 대부분의 국가가 절대왕정이거나 귀족제였으며, "
                "영국의 의회제도 실질적으로는 소수 유산계급의 과두제에 가까웠다."
            ),
            "keywords": ["주권", "인민주권", "양도 불가", "분할 불가", "일반의지"],
            "verified": False
        },
        # CLAIM-008: 교육론 — 소극적 교육(éducation négative)
        {
            "id": "rousseau-claim-008",
            "thinker_id": "rousseau",
            "work_id": "rousseau-emile",
            "source_detail": "Émile, Livre II",
            "claim": (
                "최선의 교육은 소극적 교육(éducation négative)이다. "
                "아이에게 지식이나 덕을 직접 가르치는 것이 아니라, "
                "마음이 악덕으로부터, 정신이 오류로부터 보호되도록 하는 것이 교육의 핵심이다. "
                "자연의 발달 과정을 존중하고 방해하지 않아야 한다."
            ),
            "original_text": (
                "La première éducation doit donc être purement négative. Elle consiste, "
                "non point à enseigner la vertu ni la vérité, mais à garantir le cœur du vice "
                "et l'esprit de l'erreur."
            ),
            "original_text_ko": (
                "따라서 최초의 교육은 순전히 소극적이어야 한다. "
                "그것은 덕이나 진리를 가르치는 것이 아니라, "
                "마음을 악덕으로부터, 정신을 오류로부터 보호하는 것이다."
            ),
            "explanation": (
                "루소의 소극적 교육은 당시의 주입식·권위적 교육에 대한 급진적 대안이다. "
                "아이는 자연적으로 선하므로, 교육자의 역할은 지식을 주입하는 것이 아니라 "
                "사회의 악한 영향으로부터 아이를 보호하고, 자연의 발달 단계에 따라 "
                "적절한 경험을 제공하는 것이다. 각 발달 단계에 맞는 교육이 필요하며, "
                "성급하게 이성적 교육을 시도하면 오히려 해가 된다. "
                "아이는 감각과 경험을 통해 스스로 배우도록 해야 한다."
            ),
            "argument": (
                "(1) 자연에서 나오는 모든 것은 선하지만, 인간의 손에서 타락한다. "
                "(2) 따라서 교육의 과제는 자연의 선함을 보존하는 것이다. "
                "(3) 아이에게 이른 시기에 관습, 권위, 편견을 주입하면 자연적 발달을 왜곡한다. "
                "(4) 소극적 교육은 시간을 잃는 것이 아니라 시간을 얻는 것이다. "
                "(5) 아이는 감각과 직접 경험을 통해 자연스럽게 판단력을 발달시킨다. "
                "(6) 이성 교육은 12세 이후, 즉 이성이 자연적으로 발달한 후에 시작해야 한다."
            ),
            "counterpoint": (
                "존 로크(John Locke)는 '교육에 관한 몇 가지 생각'(Some Thoughts Concerning Education, 1693)에서 "
                "아이의 마음을 백지(tabula rasa)로 보고, 조기에 습관과 이성을 형성해야 한다고 주장했다. "
                "로크는 어린 시기의 습관 형성과 이성적 훈련을 강조한 반면, "
                "루소는 자연의 발달 단계를 존중하여 성급한 교육을 경계했다. "
                "에밀 뒤르켐(Émile Durkheim)은 '도덕교육론'(L'Éducation morale, 1925)에서 "
                "루소의 개인주의적 교육이 사회화의 필요성을 간과한다고 비판했다."
            ),
            "context": (
                "18세기 유럽의 교육은 종교적·권위적 성격이 강했으며, "
                "아이를 '작은 어른'으로 취급하는 경향이 있었다. "
                "루소는 아동기의 고유한 가치를 인정하고, 아이의 발달 단계에 맞는 교육을 최초로 체계화했다."
            ),
            "keywords": ["소극적 교육", "자연에 따른 교육", "에밀", "감각 교육", "발달 단계"],
            "verified": False
        },
        # CLAIM-009: 시민종교(religion civile)
        {
            "id": "rousseau-claim-009",
            "thinker_id": "rousseau",
            "work_id": "rousseau-social-contract",
            "source_detail": "Du Contrat social, Livre IV, Chapitre 8",
            "claim": (
                "국가는 시민종교(religion civile)를 제정할 수 있으며, "
                "이는 사회적 유대를 위한 최소한의 종교적 교의이다. "
                "시민종교의 교의는 신의 존재, 내세, 선인의 행복과 악인의 벌, "
                "사회계약과 법의 신성함, 그리고 불관용의 배제이다."
            ),
            "original_text": (
                "Les dogmes de la religion civile doivent être simples, en petit nombre, "
                "énoncés avec précision, sans explications ni commentaires. "
                "L'existence de la Divinité puissante, intelligente, bienfaisante, prévoyante et pourvoyante, "
                "la vie à venir, le bonheur des justes, le châtiment des méchants, "
                "la sainteté du contrat social et des lois : voilà les dogmes positifs."
            ),
            "original_text_ko": (
                "시민종교의 교의는 단순하고, 소수여야 하며, 해설이나 주석 없이 정확하게 진술되어야 한다. "
                "강력하고, 지성적이고, 자비롭고, 선견지명이 있으며 섭리하는 신의 존재, "
                "내세, 의로운 자의 행복, 악한 자의 처벌, "
                "사회계약과 법의 신성함: 이것이 적극적 교의이다."
            ),
            "explanation": (
                "루소는 종교를 세 종류로 구분한다: 인간의 종교(자연종교/복음서의 종교), "
                "시민의 종교(고대 도시국가의 종교), 사제의 종교(가톨릭 등 제도종교). "
                "사제의 종교는 시민의 충성을 분열시키므로 해롭고, "
                "인간의 종교는 너무 보편적이어서 시민적 유대를 형성하지 못한다. "
                "시민종교는 공동체의 결속을 위한 최소한의 종교적 신조로, "
                "이를 거부하는 자는 추방될 수 있다."
            ),
            "argument": (
                "(1) 국가는 시민들의 사회적 유대를 필요로 한다. "
                "(2) 종교적 감정은 이 유대에 기여할 수 있다. "
                "(3) 그러나 제도종교(가톨릭 등)는 국가와 교회 사이의 충성 분열을 야기한다. "
                "(4) 순수한 자연종교는 너무 개인적이어 사회적 유대를 형성하지 못한다. "
                "(5) 따라서 국가는 최소한의 시민종교적 교의를 제정할 수 있다. "
                "(6) 시민종교의 유일한 부정적 교의는 불관용의 배제이다."
            ),
            "counterpoint": (
                "존 로크(John Locke)는 '관용에 관한 편지'(A Letter Concerning Toleration, 1689)에서 "
                "국가와 종교의 분리를 주장하며, 국가가 종교적 교의를 제정하는 것에 반대했다. "
                "볼테르(Voltaire)는 루소의 시민종교가 새로운 형태의 종교적 강제라고 비판했다. "
                "현대 자유주의의 관점에서 시민종교는 양심의 자유를 침해할 수 있으며, "
                "존 롤스(John Rawls)의 '정치적 자유주의'(Political Liberalism, 1993)는 "
                "포괄적 교설(comprehensive doctrine)을 국가가 부과하는 것을 거부한다."
            ),
            "context": (
                "루소는 제네바의 칼뱅파 전통 속에서 자랐으나, '에밀'의 '사부아 보좌신부의 신앙고백'에서 "
                "이신론적 자연종교를 옹호하여 가톨릭과 칼뱅파 모두의 분노를 샀다. "
                "시민종교론은 고대 로마의 종교적 관행과 마키아벨리의 종교론에서 영향을 받았다."
            ),
            "keywords": ["시민종교", "사회적 유대", "관용", "자연종교", "불관용의 배제"],
            "verified": False
        },
        # CLAIM-010: 자기애(amour de soi) vs 자존심(amour-propre)
        {
            "id": "rousseau-claim-010",
            "thinker_id": "rousseau",
            "work_id": "rousseau-inequality",
            "source_detail": "Discours sur l'inégalité, Note XV",
            "claim": (
                "자기애(amour de soi)와 자존심(amour-propre)은 근본적으로 다른 감정이다. "
                "자기애는 자연적이고 선한 감정으로 자기보존을 지향하지만, "
                "자존심은 사회에서 발생한 인위적 감정으로 타인과의 비교에서 우월함을 추구하며, "
                "시기, 질투, 허영 등 모든 악덕의 원천이다."
            ),
            "original_text": (
                "L'amour de soi-même est un sentiment naturel qui porte tout animal à veiller à sa propre "
                "conservation... L'amour-propre n'est qu'un sentiment relatif, factice, et né dans la société, "
                "qui porte chaque individu à faire plus de cas de soi que de tout autre, "
                "qui inspire aux hommes tous les maux qu'ils se font mutuellement."
            ),
            "original_text_ko": (
                "자기애는 모든 동물로 하여금 자기 보존에 주의를 기울이게 하는 자연적 감정이다... "
                "자존심은 상대적이고 인위적이며 사회에서 태어난 감정에 불과하며, "
                "각 개인으로 하여금 자신을 다른 누구보다도 중요하게 여기게 만들고, "
                "인간들이 서로에게 가하는 모든 해악의 원천이 되는 감정이다."
            ),
            "explanation": (
                "이 구별은 루소 인간학의 핵심이자 타락의 메커니즘을 설명하는 열쇠이다. "
                "자기애(amour de soi)는 모든 동물이 가진 자기보존 본능으로, "
                "연민(pitié)과 결합하여 자연 상태에서의 평화를 가능하게 한다. "
                "자존심(amour-propre)은 사회적 비교에서 발생하는 감정으로, "
                "타인보다 우월하다고 인정받고 싶은 욕구이다. "
                "자존심이 발생하면 인간은 타인의 시선에 종속되고, "
                "시기, 질투, 허영, 경멸 등의 악덕이 생겨난다."
            ),
            "argument": (
                "(1) 자기애(amour de soi)는 모든 동물에게 있는 자연적 감정이다. "
                "(2) 자기애는 자기보존만을 지향하며, 타인에 대한 비교나 적대를 포함하지 않는다. "
                "(3) 자존심(amour-propre)은 사회적 상호작용에서, 특히 타인의 시선에 대한 의식에서 발생한다. "
                "(4) 자존심은 타인보다 우월하기를 원하고 타인의 인정을 갈구한다. "
                "(5) 이 비교와 경쟁의 감정에서 시기, 질투, 허영, 경멸 등 모든 사회적 악덕이 생겨난다. "
                "(6) 따라서 인간의 도덕적 타락은 자연이 아니라 사회의 산물이다."
            ),
            "counterpoint": (
                "토머스 홉스(Thomas Hobbes)는 '리바이어던'(Leviathan, 1651)에서 "
                "영광(glory)에 대한 욕구를 인간의 자연적 본성으로 보았으나, "
                "루소는 이를 사회에 의해 만들어진 인위적 감정(자존심)이라고 반박했다. "
                "애덤 스미스(Adam Smith)는 '도덕감정론'(The Theory of Moral Sentiments, 1759)에서 "
                "타인의 시선에 대한 관심(desire to be approved)을 긍정적으로 평가하며, "
                "이것이 사회적 덕의 원천이 될 수 있다고 보았다."
            ),
            "context": (
                "'인간 불평등 기원론'의 주석 XV에서 체계적으로 구분되지만, "
                "본문 전체에 걸쳐 이 구별이 루소의 논증을 관통한다. "
                "에밀'에서도 소년기에서 청년기로의 전환에서 자존심의 발생과 통제가 핵심 교육 과제로 다루어진다."
            ),
            "keywords": ["자기애(amour de soi)", "자존심(amour-propre)", "타락의 메커니즘", "사회적 비교", "연민(pitié)"],
            "verified": False
        },
        # CLAIM-011: 입법자(législateur)
        {
            "id": "rousseau-claim-011",
            "thinker_id": "rousseau",
            "work_id": "rousseau-social-contract",
            "source_detail": "Du Contrat social, Livre II, Chapitre 7",
            "claim": (
                "입법자(législateur)는 일반의지를 구체적인 법으로 표현할 수 있는 예외적 존재이다. "
                "인민은 항상 선을 원하지만 항상 선이 무엇인지 아는 것은 아니므로, "
                "입법자가 인민을 계도하여 일반의지를 법의 형태로 구체화해야 한다."
            ),
            "original_text": (
                "Pour découvrir les meilleures règles de société qui conviennent aux nations, "
                "il faudrait une intelligence supérieure qui vît toutes les passions des hommes "
                "et qui n'en éprouvât aucune... Il faudrait des dieux pour donner des lois aux hommes."
            ),
            "original_text_ko": (
                "국민들에게 적합한 최선의 사회 규칙을 발견하려면, "
                "인간의 모든 정념을 꿰뚫어 보면서도 그 어떤 정념도 느끼지 않는 "
                "탁월한 지성이 필요할 것이다... 인간에게 법을 주려면 신들이 필요할 것이다."
            ),
            "explanation": (
                "입법자는 주권자(인민)를 대체하는 것이 아니라 보조하는 존재이다. "
                "인민은 일반의지의 주체이지만, 일반의지를 구체적 법으로 표현하는 능력은 부족할 수 있다. "
                "입법자는 모세, 리쿠르고스, 솔론 같은 역사적 입법자를 모델로 하며, "
                "법을 제정한 후 물러나야 한다(법 제정 후 통치 권력을 갖지 않는다). "
                "입법자는 설득과 권위로 인민을 이끌되, 강제력은 사용하지 않는다."
            ),
            "argument": (
                "(1) 일반의지는 항상 올바르지만, 인민의 판단이 항상 올바른 것은 아니다. "
                "(2) 인민은 자신의 진정한 이익을 모를 수 있고, 파벌에 속을 수 있다. "
                "(3) 따라서 인민을 계도하여 일반의지를 법으로 표현할 수 있는 인물이 필요하다. "
                "(4) 이 입법자는 인간의 본성을 변화시킬 수 있을 만큼 탁월해야 한다. "
                "(5) 입법자는 법을 제정하되 집행 권력을 갖지 않으므로 폭군이 되지 않는다. "
                "(6) 역사적으로 모세, 리쿠르고스, 솔론, 누마 등이 이러한 입법자의 사례이다."
            ),
            "counterpoint": (
                "칼 포퍼(Karl Popper)는 '열린 사회와 그 적들'(The Open Society and Its Enemies, 1945)에서 "
                "플라톤의 철인왕과 유사한 이러한 구상이 전체주의적 함의를 갖는다고 비판했다. "
                "입법자가 인민의 '진정한 의지'를 알고 있다는 전제는 "
                "독재자가 인민의 이름으로 통치하는 것을 정당화할 수 있다. "
                "매디슨(James Madison)은 '연방주의자 논문'에서 "
                "제도적 견제와 균형이 탁월한 개인에 의존하는 것보다 더 안정적인 해법이라고 보았다."
            ),
            "context": (
                "루소는 제네바, 스파르타, 로마 등 소규모 공화정의 역사에서 영감을 받았다. "
                "특히 고대 입법자들(리쿠르고스, 솔론 등)이 국가의 기초를 놓은 사례를 "
                "자신의 이론적 틀에 통합하고자 했다."
            ),
            "keywords": ["입법자", "일반의지", "법", "인민 계도", "리쿠르고스"],
            "verified": False
        },
        # CLAIM-012: 직접민주주의 — 대의제 비판
        {
            "id": "rousseau-claim-012",
            "thinker_id": "rousseau",
            "work_id": "rousseau-social-contract",
            "source_detail": "Du Contrat social, Livre III, Chapitre 15",
            "claim": (
                "주권은 대표될 수 없으며, 대의제는 자유의 포기이다. "
                "영국 인민은 자기가 자유롭다고 생각하지만, 그것은 큰 착각이다. "
                "그들이 자유로운 것은 의회 의원을 선출하는 동안뿐이며, "
                "선출 후에는 다시 노예가 된다."
            ),
            "original_text": (
                "Le peuple anglais pense être libre ; il se trompe fort, il ne l'est que durant l'élection "
                "des membres du parlement ; sitôt qu'ils sont élus, il est esclave, il n'est rien. "
                "Dans les courts moments de sa liberté, l'usage qu'il en fait mérite bien qu'il la perde."
            ),
            "original_text_ko": (
                "영국 인민은 자기가 자유롭다고 생각한다. 그것은 크게 잘못된 것이다. "
                "그들이 자유로운 것은 의회 의원을 선출하는 동안뿐이며, "
                "의원들이 선출되자마자 그들은 노예가 되고 아무것도 아니게 된다. "
                "그 짧은 자유의 순간에 그들이 자유를 사용하는 방식을 보면, "
                "자유를 잃는 것은 당연하다."
            ),
            "explanation": (
                "루소는 고대 그리스·로마의 직접민주주의를 이상으로 삼으며, "
                "근대 대의제를 강하게 비판한다. 의지는 대표될 수 없으므로, "
                "대의원은 인민의 대표(représentants)가 아니라 위임자(commissaires)일 뿐이다. "
                "인민이 직접 법을 만들지 않으면 그것은 인민의 법이 아니다. "
                "루소는 대의제가 봉건제에서 유래한 것이며, "
                "고대인들은 대의제를 알지 못했다고 지적한다."
            ),
            "argument": (
                "(1) 주권은 일반의지의 행사이며, 의지는 대표될 수 없다. "
                "(2) 대의원이 인민의 의지를 '대표'한다고 해도, 그것은 대의원 자신의 의지에 불과하다. "
                "(3) 인민이 직접 입법에 참여하지 않으면, 그들은 주권자가 아니라 신민일 뿐이다. "
                "(4) 영국의 의회제는 선거 때만 자유롭고 나머지는 예속 상태이다. "
                "(5) 대의제는 봉건제의 유산이며, 고대의 자유로운 인민들은 대의제를 알지 못했다. "
                "(6) 진정한 자유는 인민의 직접 참여(직접민주주의)에서만 가능하다."
            ),
            "counterpoint": (
                "에드먼드 버크(Edmund Burke)는 '브리스톨 연설'(Speech to the Electors of Bristol, 1774)에서 "
                "대의원은 유권자의 지시에 따르는 대리인이 아니라 독립적 판단을 행사하는 대표자라고 주장했다. "
                "매디슨(James Madison)은 '연방주의자 논문' 제10호에서 "
                "대의제가 파벌의 해악을 통제하고 공공선을 증진하는 데 직접민주주의보다 우월하다고 반론했다. "
                "현대 민주주의 이론에서 대의제는 대규모 사회에서 불가피한 제도적 선택으로 받아들여진다."
            ),
            "context": (
                "18세기 영국의 의회제도가 당시 유럽에서 가장 자유로운 정치 체제로 칭송받던 시기에, "
                "루소는 이에 대한 근본적 비판을 제기했다. "
                "루소의 직접민주주의론은 소규모 도시국가(제네바, 스파르타, 로마)를 모델로 하며, "
                "대규모 국가에의 적용 가능성은 루소 자신도 인정한 한계이다."
            ),
            "keywords": ["직접민주주의", "대의제 비판", "영국 의회", "주권", "인민 참여"],
            "verified": False
        },
        # CLAIM-013: 자연인과 시민의 긴장 — 에밀의 교육적 딜레마
        {
            "id": "rousseau-claim-013",
            "thinker_id": "rousseau",
            "work_id": "rousseau-emile",
            "source_detail": "Émile, Livre I",
            "claim": (
                "자연인(homme naturel)과 시민(citoyen)은 양립하기 어렵다. "
                "자연인을 만들고자 하면 시민이 될 수 없고, 시민을 만들고자 하면 자연인이 파괴된다. "
                "자연적 교육(에밀)과 시민적 교육(사회계약론) 사이에는 근본적 긴장이 있다."
            ),
            "original_text": (
                "Forcé de combattre la nature ou les institutions sociales, il faut opter entre faire "
                "un homme ou un citoyen ; car on ne peut faire à la fois l'un et l'autre."
            ),
            "original_text_ko": (
                "자연과 사회제도 사이에서 싸워야 하는 상황에서, "
                "인간을 만들 것인지 시민을 만들 것인지 선택해야 한다. "
                "왜냐하면 둘 다 동시에 만들 수는 없기 때문이다."
            ),
            "explanation": (
                "이 긴장은 루소 사상의 핵심적 딜레마이다. "
                "'인간 불평등 기원론'과 '에밀'에서 루소는 자연인의 자족성과 독립성을 이상으로 그리지만, "
                "'사회계약론'에서는 시민으로서의 참여와 일반의지에의 복종을 요구한다. "
                "자연인은 오직 자기 자신에게만 의존하는 존재이지만, "
                "시민은 공동체 전체에 자신을 양도한 존재이다. "
                "에밀의 교육은 자연인을 만드는 것을 목표로 하지만, "
                "에밀이 결국 사회 속에서 살아야 한다는 점에서 이 딜레마는 완전히 해소되지 않는다."
            ),
            "argument": (
                "(1) 자연인은 자기 자신에게만 의존하며 전체적 통일성을 가진다. "
                "(2) 시민은 공동체의 일부이며 공동체에 의해 규정된다. "
                "(3) 이 두 이상은 서로 다른 방향을 가리킨다: 독립 vs 헌신. "
                "(4) 반쪽짜리 교육(자연적이지도 시민적이지도 않은)은 양쪽 모두에 실패한 인간을 만든다. "
                "(5) 에밀의 교육은 자연인을 만드는 쪽을 택하되, "
                "이 자연인이 사회 속에서도 자기를 잃지 않도록 준비시킨다."
            ),
            "counterpoint": (
                "에른스트 카시러(Ernst Cassirer)는 '루소 문제'(The Question of Jean-Jacques Rousseau, 1932)에서 "
                "이 긴장이 루소 사상의 모순이 아니라 통일적 체계의 다른 측면이라고 해석했다. "
                "카시러에 따르면 자연인과 시민 모두 자율성(autonomie)이라는 공통 원리에 기초하며, "
                "에밀은 사회 속에서도 자율적인 인간을 기르는 프로젝트이다. "
                "그러나 주디스 슈클라(Judith Shklar)는 '인간과 시민'(Men and Citizens, 1969)에서 "
                "이 긴장이 루소 사상에서 결코 해소되지 않는 근본적 이율배반이라고 주장했다."
            ),
            "context": (
                "에밀 제1권 서두에서 제기되는 이 딜레마는 루소 사상 전체를 관통한다. "
                "에밀의 교육이 자연인을 목표로 하면서도 마지막(제5권)에서 "
                "에밀이 시민적 의무를 배우는 것으로 끝나는 것은 이 긴장의 표현이다."
            ),
            "keywords": ["자연인", "시민", "교육적 딜레마", "자율성", "에밀"],
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """루소 키워드 데이터 입력."""
    keywords = [
        {
            "id": "rousseau-kw-001",
            "thinker_id": "rousseau",
            "term": "일반의지 (Volonté Générale)",
            "term_original": "volonté générale",
            "definition": (
                "공동체 전체의 공동선(bien commun)을 지향하는 의지. "
                "전체의지(volonté de tous)가 개별 의지의 단순 합산인 반면, "
                "일반의지는 개별 의지에서 서로 상쇄되는 과부족을 제거한 후 남는 것이다. "
                "주권의 행사이며 법의 근거로, 항상 올바르고 공공의 유용을 지향한다."
            ),
            "related_claims": ["rousseau-claim-003", "rousseau-claim-007"],
            "source": "Du Contrat social, Livre II, Chapitres 1-3"
        },
        {
            "id": "rousseau-kw-002",
            "thinker_id": "rousseau",
            "term": "사회계약 (Contrat Social)",
            "term_original": "contrat social / pacte social",
            "definition": (
                "각 구성원이 자신의 모든 권리를 공동체 전체에 양도하는 합의. "
                "자연적 자유를 잃는 대신 시민적 자유와 도덕적 자유를 얻는다. "
                "루소의 사회계약은 홉스(주권자에게 양도)나 로크(정부에 위탁)와 달리 "
                "공동체 전체(일반의지)에 양도하는 것이 특징이다."
            ),
            "related_claims": ["rousseau-claim-004", "rousseau-claim-005"],
            "source": "Du Contrat social, Livre I, Chapitres 6-8"
        },
        {
            "id": "rousseau-kw-003",
            "thinker_id": "rousseau",
            "term": "자연 상태 (État de Nature)",
            "term_original": "état de nature",
            "definition": (
                "사회 이전의 인간의 상태. 루소에 따르면 자연인은 자유롭고 선량하며, "
                "자기애(amour de soi)와 연민(pitié)만을 가진 고립된 존재이다. "
                "홉스의 전쟁 상태와 대비되며, 루소는 홉스가 문명인의 악덕을 "
                "자연인에게 잘못 투사했다고 비판한다."
            ),
            "related_claims": ["rousseau-claim-001"],
            "source": "Discours sur l'inégalité, Première partie"
        },
        {
            "id": "rousseau-kw-004",
            "thinker_id": "rousseau",
            "term": "자기애 / 자존심 (Amour de Soi / Amour-Propre)",
            "term_original": "amour de soi / amour-propre",
            "definition": (
                "자기애(amour de soi)는 자기보존을 지향하는 자연적·절대적 감정이고, "
                "자존심(amour-propre)은 타인과의 비교에서 우월함을 추구하는 사회적·상대적 감정이다. "
                "자기애는 선하지만, 자존심은 시기·질투·허영 등 모든 사회적 악덕의 원천이다. "
                "이 구별은 루소 인간학의 핵심이자 타락의 메커니즘을 설명하는 열쇠이다."
            ),
            "related_claims": ["rousseau-claim-001", "rousseau-claim-010"],
            "source": "Discours sur l'inégalité, Note XV; Émile, Livre IV"
        },
        {
            "id": "rousseau-kw-005",
            "thinker_id": "rousseau",
            "term": "소극적 교육 (Éducation Négative)",
            "term_original": "éducation négative",
            "definition": (
                "덕이나 진리를 직접 가르치는 것이 아니라, 마음을 악덕으로부터 "
                "정신을 오류로부터 보호하는 교육. 자연의 발달 단계를 존중하여 "
                "성급한 주입식 교육을 배제하고, 감각과 경험을 통한 자연스러운 학습을 중시한다. "
                "아동기의 고유한 가치를 인정하는 근대 교육학의 출발점이다."
            ),
            "related_claims": ["rousseau-claim-008"],
            "source": "Émile, Livre II"
        },
        {
            "id": "rousseau-kw-006",
            "thinker_id": "rousseau",
            "term": "인민주권 (Souveraineté du Peuple)",
            "term_original": "souveraineté du peuple",
            "definition": (
                "주권은 인민 전체에 귀속되며, 양도·분할·대표될 수 없다. "
                "주권은 일반의지의 행사이므로, 인민이 직접 입법에 참여해야 한다. "
                "정부는 주권자(인민)의 집행 기관에 불과하며, "
                "대의원은 인민의 대표가 아니라 위임자일 뿐이다."
            ),
            "related_claims": ["rousseau-claim-007", "rousseau-claim-012"],
            "source": "Du Contrat social, Livre II, Chapitres 1-2; Livre III, Chapitre 15"
        },
        {
            "id": "rousseau-kw-007",
            "thinker_id": "rousseau",
            "term": "시민종교 (Religion Civile)",
            "term_original": "religion civile",
            "definition": (
                "사회적 유대를 위한 최소한의 종교적 교의. "
                "신의 존재, 내세, 사회계약과 법의 신성함 등을 포함하며, "
                "유일한 부정적 교의는 불관용의 배제이다. "
                "제도종교(가톨릭 등)의 충성 분열을 방지하면서도 "
                "공동체의 도덕적 유대를 유지하기 위한 루소의 해법이다."
            ),
            "related_claims": ["rousseau-claim-009"],
            "source": "Du Contrat social, Livre IV, Chapitre 8"
        },
        {
            "id": "rousseau-kw-008",
            "thinker_id": "rousseau",
            "term": "입법자 (Législateur)",
            "term_original": "législateur",
            "definition": (
                "일반의지를 구체적인 법으로 표현할 수 있는 예외적 존재. "
                "인민은 항상 선을 원하지만 항상 선이 무엇인지 아는 것은 아니므로, "
                "입법자가 인민을 계도한다. 모세, 리쿠르고스, 솔론 등이 역사적 모델이며, "
                "법 제정 후에는 집행 권력을 갖지 않고 물러나야 한다."
            ),
            "related_claims": ["rousseau-claim-011"],
            "source": "Du Contrat social, Livre II, Chapitre 7"
        },
        {
            "id": "rousseau-kw-009",
            "thinker_id": "rousseau",
            "term": "불평등 (Inégalité)",
            "term_original": "inégalité",
            "definition": (
                "루소는 자연적 불평등(신체적 차이)과 도덕적·정치적 불평등(부, 권력, 지위의 차이)을 구별한다. "
                "도덕적 불평등은 자연적인 것이 아니라 사유재산과 사회의 산물이다. "
                "최초로 토지를 울타리 친 사람이 시민사회와 불평등의 창시자이며, "
                "법과 국가는 이 불평등을 고정화하고 정당화하는 기제이다."
            ),
            "related_claims": ["rousseau-claim-002"],
            "source": "Discours sur l'inégalité, Seconde partie"
        },
        {
            "id": "rousseau-kw-010",
            "thinker_id": "rousseau",
            "term": "자유 (Liberté)",
            "term_original": "liberté",
            "definition": (
                "루소는 세 종류의 자유를 구별한다: "
                "(1) 자연적 자유(liberté naturelle) — 자연 상태에서 물리적 힘에 의해서만 제한되는 무제한적 자유, "
                "(2) 시민적 자유(liberté civile) — 일반의지(법)에 의해 보장되고 제한되는 자유, "
                "(3) 도덕적 자유(liberté morale) — 자기 자신이 부과한 법에 복종하는 자유. "
                "도덕적 자유가 가장 높은 형태이며, '자기가 스스로에게 부과한 법에 복종하는 것이 자유'이다."
            ),
            "related_claims": ["rousseau-claim-004", "rousseau-claim-005", "rousseau-claim-006"],
            "source": "Du Contrat social, Livre I, Chapitres 1, 6-8"
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """루소 관계 데이터 입력 (중복 확인 후)."""
    # 먼저 이미 존재하는 루소 관련 relation을 확인
    existing = set()
    try:
        res = client.search(
            index=INDEX_RELATIONS,
            query={"bool": {"should": [
                {"term": {"from_thinker": "rousseau"}},
                {"term": {"to_thinker": "rousseau"}}
            ]}},
            size=50,
            _source=["id"]
        )
        for hit in res['hits']['hits']:
            existing.add(hit['_id'])
        print(f"[relations] 기존 루소 관련 관계: {existing}")
    except Exception:
        pass

    relations = [
        {
            "id": "relation-rousseau-kant",
            "from_thinker": "rousseau",
            "to_thinker": "kant",
            "type": "influenced",
            "description": (
                "루소는 칸트(Immanuel Kant, 1724~1804)에게 결정적 영향을 미쳤다. "
                "칸트는 루소를 '도덕의 뉴턴'이라 불렀으며, 루소의 자유·평등·자율성 개념이 "
                "칸트 도덕철학의 핵심 개념인 자율성(Autonomie)과 정언명령(kategorischer Imperativ)에 "
                "직접적 영감을 주었다. '에밀'을 읽고 산책을 잊을 정도로 몰두했다는 일화가 유명하며, "
                "'인간 불평등 기원론'은 칸트에게 인간 본성에 대한 깊은 통찰을 제공했다. "
                "루소의 '자기 자신이 부과한 법에 복종하는 것이 자유'라는 명제는 "
                "칸트의 도덕적 자율성 개념의 직접적 원천이다."
            ),
            "strength": "강함",
            "period": "18세기"
        },
        {
            "id": "relation-rousseau-french-revolution",
            "from_thinker": "rousseau",
            "to_thinker": "french-revolution",
            "type": "influenced",
            "description": (
                "루소의 인민주권론, 일반의지 개념, 자유와 평등의 이념은 "
                "프랑스 혁명(1789)에 지대한 사상적 영향을 미쳤다. "
                "'인간과 시민의 권리선언'(1789)의 기본 원리 — 인민주권, 자유, 평등 — 는 "
                "루소의 사회계약론에 직접적으로 기초한다. "
                "로베스피에르(Robespierre)는 루소의 열렬한 추종자로, "
                "일반의지와 시민종교 개념을 혁명 정치에 적용하려 했다. "
                "그러나 공포정치(Terreur)와의 연관성은 루소 사상의 전체주의적 함의에 대한 "
                "비판의 근거가 되기도 했다."
            ),
            "strength": "강함",
            "period": "18세기 말"
        },
        {
            "id": "relation-rousseau-marx",
            "from_thinker": "rousseau",
            "to_thinker": "marx",
            "type": "influenced",
            "description": (
                "루소의 사유재산 비판과 불평등 분석은 마르크스(Karl Marx, 1818~1883)에게 "
                "간접적이나 중요한 영향을 미쳤다. '인간 불평등 기원론'에서 사유재산을 "
                "불평등과 예속의 원천으로 지목한 것은 마르크스의 사유재산 철폐론과 "
                "소외(Entfremdung) 개념의 선구로 평가된다. "
                "그러나 마르크스는 루소의 자연 상태 회귀를 낭만적이라 보았으며, "
                "변증법적 유물론에 기초한 역사적 분석을 루소의 사변적 접근과 대비시켰다. "
                "엥겔스는 '반뒤링론'에서 루소의 불평등론을 높이 평가했다."
            ),
            "strength": "보통",
            "period": "18~19세기"
        },
        {
            "id": "relation-montesquieu-rousseau",
            "from_thinker": "montesquieu",
            "to_thinker": "rousseau",
            "type": "influenced",
            "description": (
                "몽테스키외(Montesquieu, 1689~1755)의 '법의 정신'(De l'esprit des lois, 1748)은 "
                "루소에게 중요한 영향을 미쳤다. 루소는 법과 정치 체제에 대한 몽테스키외의 "
                "비교 분석적 접근, 공화정의 덕(vertu) 개념, 기후와 풍토의 영향론 등을 수용했다. "
                "그러나 루소는 몽테스키외의 권력분립론을 주권의 분할로 비판했으며, "
                "몽테스키외의 영국 정체 칭송에 대해서도 대의제 비판으로 맞섰다."
            ),
            "strength": "보통",
            "period": "18세기"
        }
    ]

    inserted = 0
    for rel in relations:
        if rel["id"] in existing:
            print(f"[relation] {rel['id']}: 이미 존재 (스킵)")
            continue
        result = client.index(index=INDEX_RELATIONS, id=rel["id"], document=rel)
        print(f"[relation] {rel['id']}: {result['result']}")
        inserted += 1

    # 기존에 존재하는 관계도 보고
    skipped_existing = [
        "relation-hobbes-rousseau (hobbes → rousseau, influenced)",
        "relation-locke-rousseau (locke → rousseau, influenced)",
        "kant-rel-002 (kant → rousseau, synthesized)",
        "relation-bentham-rousseau (bentham → rousseau, criticized)"
    ]
    print(f"\n[기존 관계 (이미 존재)] {len(skipped_existing)}건:")
    for s in skipped_existing:
        print(f"  - {s}")

    return inserted


def verify_data(client):
    """입력된 데이터를 전수 확인."""
    print("\n=== 전수 확인 ===")

    # refresh
    client.indices.refresh(index=INDEX_THINKERS)
    client.indices.refresh(index=INDEX_WORKS)
    client.indices.refresh(index=INDEX_CLAIMS)
    client.indices.refresh(index=INDEX_KEYWORDS)
    client.indices.refresh(index=INDEX_RELATIONS)

    # thinker 확인
    r = client.get(index=INDEX_THINKERS, id="rousseau")
    print(f"[thinker] rousseau: name={r['_source']['name_en']}, era={r['_source']['era']}, field={r['_source']['field']}")

    # field 확인
    try:
        f = client.get(index=INDEX_FIELDS, id="political_philosophy")
        print(f"[field] political_philosophy: name={f['_source']['name']}")
    except Exception:
        print("[field] political_philosophy: NOT FOUND")

    # works 확인
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "rousseau"}})
    print(f"[works] rousseau 저서 수: {works_count['count']}")
    works_result = client.search(
        index=INDEX_WORKS,
        query={"term": {"thinker_id": "rousseau"}},
        _source=["id", "title_original", "year"],
        size=10
    )
    for hit in works_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['title_original']} ({s['year']})")

    # claims 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "rousseau"}})
    print(f"[claims] rousseau 주장 수: {claims_count['count']}")
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "rousseau"}},
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
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "rousseau"}})
    print(f"[keywords] rousseau 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_count = client.count(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "rousseau"}},
            {"term": {"to_thinker": "rousseau"}}
        ]}}
    )
    print(f"[relations] rousseau 관련 관계 수: {rel_count['count']}")
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "rousseau"}},
            {"term": {"to_thinker": "rousseau"}}
        ]}},
        _source=["id", "from_thinker", "to_thinker", "type"],
        size=20
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
        print("=== 장자크 루소(Jean-Jacques Rousseau) 데이터 입력 시작 ===\n")

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
        print(f"   총 {rel_n}건 신규 입력")

        stats = verify_data(client)
        print("\n=== 입력 완료 ===")
        print(f"field: 1건 | thinker: 1건 | works: {stats['works']}건 | claims: {stats['claims']}건 | "
              f"keywords: {stats['keywords']}건 | relations: {stats['relations']}건 (전체, 기존 포함)")

        if stats['missing_fields']:
            print(f"[경고] 필수 필드 누락 claim: {stats['missing_fields']}")
        else:
            print("[OK] 모든 데이터 정상 입력 완료")

        return stats

    finally:
        close_client(client)


if __name__ == "__main__":
    main()
