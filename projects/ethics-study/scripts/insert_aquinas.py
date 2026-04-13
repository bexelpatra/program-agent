"""토마스 아퀴나스 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client, search_documents
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS
)


def insert_thinker(client):
    """토마스 아퀴나스 사상가 데이터 입력."""
    doc = {
        "id": "aquinas",
        "name": "토마스 아퀴나스",
        "name_en": "Thomas Aquinas",
        "field": "western_ethics",
        "era": "중세",
        "birth_year": 1225,
        "death_year": 1274,
        "background": (
            "이탈리아 나폴리 왕국의 아퀴노 백작 가문에서 태어났다. "
            "어린 시절 몬테카시노 베네딕트 수도원에서 교육받았고, 이후 나폴리 대학에 입학하여 아리스토텔레스 철학을 처음 접했다. "
            "1244년 가문의 반대를 무릅쓰고 도미니코 수도회에 입회하였으며, "
            "쾰른에서 알베르투스 마뉴스(대알베르투스)의 제자가 되어 아리스토텔레스 철학을 본격적으로 수학했다. "
            "파리 대학에서 신학 교수로 재직하며 당시 유럽 지성계를 이끌었고, "
            "이탈리아와 파리를 오가며 방대한 저술 활동을 전개했다. "
            "1273년 말 미사 중 신비적 체험 후 집필을 중단하고 '내가 쓴 모든 것이 지푸라기처럼 보인다'는 말을 남겼다. "
            "1274년 리옹 공의회로 향하는 도중 48세의 나이에 사망했다. "
            "1323년 교황 요한 22세에 의해 시성되었으며, 가톨릭 교회의 대표적 철학자·신학자로 공인되었다."
        ),
        "core_philosophy": (
            "이성과 신앙의 조화를 핵심으로 하는 스콜라 철학의 정점. "
            "아리스토텔레스 철학을 기독교 신학과 창조적으로 종합하여, 이성(철학)과 신앙(신학)이 서로 충돌하지 않고 "
            "각각 다른 방법으로 같은 진리를 탐구한다고 보았다. "
            "존재론에서 신은 순수 현실태(actus purus)로서 존재 자체(ipsum esse subsistens)이며, "
            "피조물은 본질(essentia)과 존재(esse)가 구별되는 존재들이라는 존재·본질 구분론을 제시했다. "
            "윤리학에서는 아리스토텔레스의 자연법 개념을 발전시켜, "
            "자연법은 영원법(lex aeterna)에 이성적 피조물이 참여하는 것으로 정의했다. "
            "신의 존재를 이성적으로 증명하는 '다섯 가지 길(quinque viae)'을 제시했으며, "
            "덕 윤리학과 자연법 윤리학을 결합한 종합적 도덕 체계를 구축했다."
        ),
        "philosophical_journey": (
            "수학기(1239~1252): 나폴리 대학에서 아리스토텔레스 철학 입문, "
            "도미니코 수도회 입회 후 알베르투스 마뉴스 아래 쾰른과 파리에서 아리스토텔레스 전집 연구. "
            "제1차 파리 교수 시기(1252~1259): 명제집 주해 집필, 파리 대학 신학 교수로 활동, "
            "초기 주요 저작들(존재와 본질, 진리론 일부) 저술. "
            "이탈리아 시기(1259~1268): 나폴리·오르비에토·비테르보 등지에서 신학대전 제1부 집필 시작, "
            "대이교도대전 완성, 아리스토텔레스 주석 다수 저술. "
            "제2차 파리 교수 시기(1268~1272): 신학대전 제2부(IaIIae, IIaIIae) 집필, "
            "아베로에스주의(이중진리론)와 아우구스티누스주의 양쪽을 비판하며 자신의 종합적 입장 정립. "
            "나폴리 시기(1272~1273): 신학대전 제3부 집필(미완성으로 남음)."
        ),
        "keywords": [
            "자연법",
            "다섯 가지 길",
            "존재와 본질",
            "이성과 신앙",
            "영원법",
            "신학대전",
            "스콜라 철학"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="aquinas", document=doc)
    print(f"[thinker] aquinas: {result['result']}")
    return result


def insert_works(client):
    """토마스 아퀴나스 저서 데이터 입력."""
    works = [
        {
            "id": "aquinas-summa-theologiae",
            "thinker_id": "aquinas",
            "title": "신학대전",
            "title_original": "Summa Theologiae",
            "year": 1274,
            "significance": (
                "중세 스콜라 철학의 최고 걸작이자 가톨릭 신학의 표준적 종합. "
                "신론(Prima Pars), 도덕론(Secunda Pars: IaIIae + IIaIIae), 그리스도론(Tertia Pars)으로 구성된다. "
                "자연법론, 덕론, 신의 존재 증명, 영혼론 등 윤리 임용시험에 가장 중요한 내용을 담고 있다. "
                "신학을 학문적으로 정초하기 위해 아리스토텔레스의 방법론을 도입하여 objection-reply 형식으로 서술된다. "
                "아퀴나스 자신은 미완성으로 남겼으며, 제자들이 보완본(Supplementum)을 덧붙였다."
            ),
            "key_concepts": [
                "신의 존재 증명", "자연법", "영원법", "인정법", "덕론",
                "신학적 덕", "주요덕", "이성과 신앙", "영혼론"
            ]
        },
        {
            "id": "aquinas-summa-contra-gentiles",
            "thinker_id": "aquinas",
            "title": "대이교도대전",
            "title_original": "Summa contra Gentiles",
            "year": 1265,
            "significance": (
                "이성만을 사용하여 기독교 진리를 비그리스도인(이교도, 유대인, 무슬림)에게 설명하고 변호한 호교론적 저작. "
                "신의 존재와 본성, 창조론, 영혼 불사, 구원론 등을 다룬다. "
                "계시 없이 이성만으로 도달할 수 있는 진리의 영역을 체계적으로 탐구함으로써, "
                "이성과 신앙의 관계에 대한 아퀴나스의 입장을 선명하게 드러낸다."
            ),
            "key_concepts": [
                "이성적 신 인식", "신의 단순성", "창조론", "영혼 불사",
                "이성과 신앙의 구분"
            ]
        },
        {
            "id": "aquinas-de-veritate",
            "thinker_id": "aquinas",
            "title": "진리론",
            "title_original": "De Veritate (Quaestiones Disputatae de Veritate)",
            "year": 1259,
            "significance": (
                "제1차 파리 교수 시기에 집필된 논쟁적 질문 형식의 철학적·신학적 저작. "
                "진리의 본질, 지식론, 신적 섭리, 예지, 자유의지 등을 다룬다. "
                "인식론적으로 지성이 어떻게 진리에 도달하는가를 분석하며, "
                "존재와 진리의 관계, 신과 피조물의 인식 구조를 탐구한다."
            ),
            "key_concepts": [
                "진리의 본질", "지성과 존재의 일치", "신적 예지", "자유의지", "초월 범주"
            ]
        },
        {
            "id": "aquinas-de-malo",
            "thinker_id": "aquinas",
            "title": "악론",
            "title_original": "De Malo (Quaestiones Disputatae de Malo)",
            "year": 1270,
            "significance": (
                "제2차 파리 교수 시기에 집필된 악의 문제에 관한 논쟁 질문집. "
                "악의 본질(선의 결여로서의 악), 원죄, 인간의 죄, 악마의 죄 등을 다룬다. "
                "악이 실체가 아니라 선의 결여(privatio boni)임을 체계적으로 논증하며, "
                "아우구스티누스의 악 이해를 아리스토텔레스적 틀로 정교화했다."
            ),
            "key_concepts": [
                "선의 결여", "악의 본질", "원죄", "자유의지", "도덕적 악"
            ]
        },
        {
            "id": "aquinas-de-ente-et-essentia",
            "thinker_id": "aquinas",
            "title": "존재와 본질",
            "title_original": "De Ente et Essentia",
            "year": 1252,
            "significance": (
                "아퀴나스의 초기 저작으로, 그의 형이상학적 핵심 구분인 존재(esse)와 본질(essentia)의 차이를 체계적으로 분석한다. "
                "신에게는 본질과 존재가 일치하지만(신은 존재 자체), "
                "피조물에게는 본질과 존재가 실재적으로 구별된다는 논제를 전개한다. "
                "아리스토텔레스의 질료형상론을 기독교 창조론과 결합하여, 피조물의 유한성을 형이상학적으로 설명한다."
            ),
            "key_concepts": [
                "존재(esse)", "본질(essentia)", "존재·본질 구분", "순수 현실태", "창조론"
            ]
        },
        {
            "id": "aquinas-sententia-ethicorum",
            "thinker_id": "aquinas",
            "title": "니코마코스 윤리학 주석",
            "title_original": "Sententia Libri Ethicorum",
            "year": 1271,
            "significance": (
                "아리스토텔레스의 니코마코스 윤리학에 대한 아퀴나스의 상세한 주석서. "
                "아리스토텔레스의 덕 윤리학을 기독교적 맥락에서 해석하고, "
                "자연적 덕과 신학적 덕(믿음·희망·사랑)의 관계를 명확히 한다. "
                "아퀴나스가 어떻게 이교도 철학자의 윤리학을 기독교 윤리학과 통합했는지를 보여주는 핵심 자료이다."
            ),
            "key_concepts": [
                "덕 윤리학", "에우다이모니아 해석", "자연적 덕", "신학적 덕", "이성과 신앙의 조화"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """토마스 아퀴나스 핵심 주장 데이터 입력."""
    claims = [
        {
            "id": "aquinas-claim-001",
            "thinker_id": "aquinas",
            "work_id": "aquinas-summa-theologiae",
            "source_detail": "Ia, q.2, a.3 (신학대전 제1부 제2문 제3절)",
            "claim": "신의 존재는 이성적으로 증명될 수 있으며, 다섯 가지 길(quinque viae)—운동, 작용인, 가능태와 필연적 존재, 완전성의 등급, 목적론—을 통해 신에게 도달할 수 있다.",
            "original_text": (
                "Respondeo dicendum quod Deum esse quinque viis probari potest. "
                "Prima autem et manifestior via est, quae sumitur ex parte motus."
            ),
            "explanation": (
                "아퀴나스는 신의 존재를 선험적으로(존재론적 논증처럼) 증명하는 것을 거부하고, "
                "감각 경험에서 출발하는 사후적(a posteriori) 증명을 제시한다. "
                "제1의 길(운동): 모든 운동은 원인을 필요로 하므로, 최초의 부동의 원동자가 있어야 한다. "
                "제2의 길(작용인): 결과는 원인을 필요로 하므로, 자기 원인이 없는 제1 작용인이 있어야 한다. "
                "제3의 길(가능태와 필연성): 우연적 존재들의 연쇄는 필연적 존재를 요구한다. "
                "제4의 길(완전성의 등급): 사물들 사이의 완전성의 차이는 최고 완전 존재를 상정한다. "
                "제5의 길(목적론): 지성 없는 사물들이 목적을 향해 운동함은 지성적 존재의 안내를 전제한다."
            ),
            "argument": (
                "공통 구조: 세계에는 설명이 필요한 현상(운동, 인과 연쇄, 우연성, 완전성의 등급, 자연적 목적 지향성)이 있다. "
                "이 현상들의 연쇄는 무한 소급될 수 없다 — 무한 소급은 현상 자체를 설명하지 못한다. "
                "따라서 연쇄를 종결짓는 궁극적 존재(부동의 원동자, 제1 작용인, 필연적 존재, 최고 완전자, 지성적 안내자)가 있어야 한다. "
                "이 궁극적 존재를 우리는 신(Deus)이라고 부른다. "
                "방법론: 아리스토텔레스의 목적론적 자연 이해와 인과론을 기독교 신학의 신 개념과 결합."
            ),
            "counterpoint": (
                "칸트는 『순수이성비판』 B620-630에서 아퀴나스 류의 우주론적 증명과 목적론적 증명을 비판했다. "
                "인과율은 현상계(경험의 영역) 안에서만 적용되므로, 현상계를 넘어선 신의 존재에 인과 논증을 적용할 수 없다고 주장했다. "
                "또한 '필연적 존재' 개념은 결국 존재론적 논증(개념에서 존재를 도출하는 오류)에 의존한다고 비판했다. "
                "흄은 『인간 오성 탐구』 §11에서 인과 원리를 경험 세계 밖으로 확장할 수 없다고 지적하며, "
                "자연의 목적론적 외양은 설계자를 증명하지 못한다고 비판했다."
            ),
            "context": (
                "신의 존재를 자명한 것으로 가정하는 안셀무스의 존재론적 논증을 비판하고, "
                "감각 경험에서 출발하는 이성적 증명의 가능성을 보여주기 위한 맥락이다."
            ),
            "keywords": ["다섯 가지 길", "신의 존재 증명", "부동의 원동자", "우주론적 증명", "목적론적 증명"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "aquinas-claim-002",
            "thinker_id": "aquinas",
            "work_id": "aquinas-summa-theologiae",
            "source_detail": "IaIIae, q.90, a.4; q.91, a.2 (신학대전 제1-2부 제90문 제4절; 제91문 제2절)",
            "claim": "자연법(lex naturalis)은 영원법(lex aeterna)에 이성적 피조물이 참여하는 것이며, 이성을 통해 인식 가능한 도덕적 원리들의 체계이다.",
            "original_text": (
                "Lex naturalis nihil aliud est quam participatio legis aeternae in rationali creatura."
                " (자연법은 이성적 피조물이 영원법에 참여하는 것 외에 다른 것이 아니다.)"
            ),
            "explanation": (
                "아퀴나스는 법을 네 층위로 구분한다: "
                "영원법(lex aeterna): 신의 이성 안에 있는 우주 통치의 원리. "
                "자연법(lex naturalis): 이성적 존재인 인간이 자신의 이성을 통해 영원법에 참여하는 것. "
                "인정법(lex humana): 자연법으로부터 도출된 인간의 실정법. "
                "신법(lex divina): 계시(성경)를 통해 주어진 법. "
                "자연법의 제1원리는 '선을 행하고 악을 피하라(bonum est faciendum et prosequendum, et malum vitandum)'이다. "
                "자연법은 인간의 자연적 성향(자기 보존, 종족 번식, 이성적 인식 욕구)에 대응하는 원리들로 구체화된다."
            ),
            "argument": (
                "전제1: 신은 피조물을 이성에 따라 통치하며, 이 이성적 원리가 영원법이다. "
                "전제2: 인간은 이성적 존재로서 신의 이성적 통치 원리에 능동적으로 참여할 수 있다. "
                "전제3: 인간 이성이 자연적으로 파악하는 선과 악의 기본 원리들은 영원법의 반영이다. "
                "전제4: 이성적 존재는 자신의 자연적 성향을 통해 자연법의 내용을 인식한다. "
                "결론: 따라서 자연법은 이성을 통해 접근 가능한 보편적 도덕 원리이며, 모든 인정법의 기초이다."
            ),
            "counterpoint": (
                "오컴(William of Ockham)은 『명제집 주해(Ordinatio)』 제1권에서 자연법의 내용이 이성에 자명하게 주어지는 것이 아니라 "
                "신의 자유로운 의지 명령(voluntas Dei)에 달려 있다는 신명론(divine command theory)을 주장했다. "
                "따라서 신이 달리 명령했다면 자연법의 내용도 달라질 수 있다고 보아, "
                "아퀴나스의 이성 기반 자연법과 근본적으로 대립한다. "
                "흄은 『도덕 원리 탐구』 부록 I에서 사실 명제(is)로부터 당위 명제(ought)를 도출하는 자연주의적 오류를 지적하여, "
                "자연적 성향에서 도덕 원리를 이끌어내는 자연법론의 토대를 비판했다."
            ),
            "context": (
                "중세 법철학과 도덕 신학의 맥락에서, 인간의 이성적 도덕 인식이 신적 질서와 어떻게 연결되는지를 설명하기 위한 것이다."
            ),
            "keywords": ["자연법", "영원법", "인정법", "신법", "선을 행하고 악을 피하라"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "aquinas-claim-003",
            "thinker_id": "aquinas",
            "work_id": "aquinas-de-ente-et-essentia",
            "source_detail": "De Ente et Essentia, c.4-5 (존재와 본질 제4-5장)",
            "claim": "피조물에서는 본질(essentia)과 존재(esse)가 실재적으로 구별되지만, 신에게서는 본질과 존재가 완전히 일치한다. 신은 존재 자체(ipsum esse subsistens)이다.",
            "original_text": (
                "In Deo autem non est aliud esse et quod est... "
                "In substantiis vero compositis est aliud forma et materia, et aliud esse et quod est seu essentia."
            ),
            "explanation": (
                "아퀴나스의 형이상학적 핵심 통찰: "
                "피조물(복합적 실체): 본질(무엇인가를 규정하는 것)과 존재(실제로 있음)가 다르다. "
                "예컨대 '불사조'는 본질은 규정할 수 있지만 존재하지 않는다. "
                "피조물은 존재를 자기 본질로 갖지 않으므로, 존재를 신으로부터 받는다(창조 의존성). "
                "신: 본질이 곧 존재이다. 신은 '존재한다'는 것이 본질이므로, 존재를 다른 것으로부터 받을 필요가 없다. "
                "이 구분은 왜 신만이 자존적(se ipsum)이고 피조물은 신에게 존재를 의존하는지를 형이상학적으로 설명한다."
            ),
            "argument": (
                "전제1: 어떤 것의 본질이 그것의 존재와 같다면, 그것은 자신의 존재의 원인이 될 수 없다(자기 원인의 부조리). "
                "전제2: 피조물은 자신의 존재를 설명할 수 없다 — 피조물이 '있다'는 사실은 본질에 포함되지 않는다. "
                "전제3: 따라서 피조물의 본질과 존재는 구별되며, 존재는 외부(신)로부터 주어진다. "
                "전제4: 이 설명의 연쇄는 본질과 존재가 일치하는 존재, 즉 신에서 멈추어야 한다. "
                "전제5: 신은 존재 자체(ipsum esse subsistens)이므로, '신이 왜 존재하는가'는 물음 자체가 성립하지 않는다. "
                "결론: 신과 피조물의 근본적 차이는 존재·본질의 일치 여부에 있다."
            ),
            "counterpoint": (
                "스코투스(Duns Scotus)는 『오르디나티오(Ordinatio)』에서 본질과 존재의 실재적 구분(distinctio realis)이 아니라 "
                "형식적 구분(distinctio formalis)이 적절하다고 주장하며, 아퀴나스의 존재·본질 실재적 구분을 비판했다. "
                "오컴은 『명제집 주해』에서 존재와 본질의 실재적 구분은 불필요한 존재자의 증식(오컴의 면도날)이라고 비판했다. "
                "길송(Étienne Gilson)은 20세기에 이 구분이 아퀴나스 존재론의 핵심이자 기독교 형이상학의 독창적 기여임을 변호했다."
            ),
            "context": (
                "아리스토텔레스의 질료형상론을 수용하면서도 기독교 창조론을 형이상학적으로 뒷받침하기 위한 맥락이다."
            ),
            "keywords": ["존재·본질 구분", "ipsum esse subsistens", "창조론", "본질", "존재"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "aquinas-claim-004",
            "thinker_id": "aquinas",
            "work_id": "aquinas-summa-theologiae",
            "source_detail": "IaIIae, q.94, a.2 (신학대전 제1-2부 제94문 제2절)",
            "claim": "자연법의 제1원리는 '선을 행하고 악을 피하라'이며, 이로부터 자기 보존, 종족 번식, 이성적 진리 탐구와 사회 생활이라는 세 가지 자연적 성향에 대응하는 구체적 원리들이 도출된다.",
            "original_text": (
                "Hoc est ergo primum praeceptum legis, quod bonum est faciendum et prosequendum, "
                "et malum vitandum."
            ),
            "explanation": (
                "자연법의 제1원리(prima principia): '선을 행하고 악을 피하라'. "
                "이는 실천 이성의 자명한 출발점으로, 이론 이성의 '모순율'에 해당한다. "
                "이로부터 세 층위의 구체적 원리들이 도출된다: "
                "(1) 인간이 실체로서 가진 성향: 자기 보존 → 생명을 보존해야 함. "
                "(2) 동물로서의 성향: 종족 번식과 자녀 양육 → 가족 제도의 자연적 기초. "
                "(3) 이성적 동물로서의 성향: 진리(특히 신에 대한 진리) 탐구, 사회 생활 → 교육과 사회 제도의 기초. "
                "이 구조는 인간의 자연적 목적(텔로스)이 도덕 원리의 내용을 규정한다는 아리스토텔레스적 목적론을 신학적 틀에서 재정립한 것이다."
            ),
            "argument": (
                "전제1: 이성은 선을 추구하고 악을 피하는 것을 자명한 원리로 파악한다(실천 이성의 제1원리). "
                "전제2: 선은 목적과 연결된다 — 어떤 것이 자신의 목적(텔로스)을 실현하는 것이 그것의 선이다. "
                "전제3: 인간에게는 존재·동물·이성적 동물이라는 세 층위의 자연적 성향이 있으며, 각각이 추구하는 목적이 있다. "
                "전제4: 이 자연적 성향의 목적들이 자연법의 구체적 내용을 이룬다. "
                "결론: 자연법은 추상적 원리(선을 행하라)로부터 구체적 도덕 원리들을 이성적으로 도출하는 체계이다."
            ),
            "counterpoint": (
                "흄은 『인성론』 제3권에서 자연적 성향(사실)에서 도덕 원리(당위)를 도출하는 것은 논리적 비약이라고 비판했다(is-ought 문제). "
                "자연적 성향은 기술적(descriptive) 사실일 뿐이며, 그 자체로 규범적(normative) 당위를 낳지 못한다는 것이다. "
                "롤스는 『정의론』에서 도덕 원리는 자연적 사실이 아니라 합리적 행위자들이 원초적 입장에서 합의할 원칙들에 의해 정당화된다고 주장하며, "
                "자연법론의 목적론적 토대와 다른 방향을 제시했다."
            ),
            "context": (
                "자연법의 구체적 내용과 그 인식론적 근거를 분석하는 맥락으로, "
                "왜 자연법이 시대와 문화를 초월하는 보편적 도덕 원리인지를 설명하기 위한 것이다."
            ),
            "keywords": ["자연법 제1원리", "선을 행하고 악을 피하라", "자연적 성향", "자기 보존", "이성적 목적"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "aquinas-claim-005",
            "thinker_id": "aquinas",
            "work_id": "aquinas-summa-theologiae",
            "source_detail": "Ia, q.79, a.12-13; IaIIae, q.19, a.5-6 (신학대전 제1부 제79문; 제1-2부 제19문)",
            "claim": "양심(conscientia)은 자연법의 원리들을 구체적 상황에 적용하는 이성의 행위이며, 도덕적 판단의 근거가 된다. 올바른 양심은 자연법에 부합하는 판단을 내린다.",
            "original_text": (
                "Conscientia... est quaedam applicatio scientiae ad actum. "
                "(양심은... 앎을 행위에 적용하는 것이다.)"
            ),
            "explanation": (
                "아퀴나스의 양심 이론: "
                "신데레시스(synderesis): 자연법의 제1원리들('선을 행하라')을 향하는 이성의 타고난 성향. "
                "양심(conscientia): 신데레시스의 원리들을 구체적 상황의 행위에 적용하는 이성의 행위(actus). "
                "이 적용이 올바르면 '올바른 양심', 잘못되면 '잘못된 양심'이다. "
                "양심은 오류 가능하지만, 잘못된 양심이라도 양심에 따라 행동해야 한다는 의무가 있다. "
                "다만 잘못된 양심이 무지에서 비롯되면 그 무지가 극복 가능한 것인지(vincible)에 따라 도덕적 책임이 달라진다."
            ),
            "argument": (
                "전제1: 도덕적 행위는 이성적 판단에 근거해야 한다. "
                "전제2: 이성은 보편 원리(자연법)를 가지고 있으며, 이를 구체 상황에 적용한다. "
                "전제3: 이 적용 과정이 양심이며, 행위자는 자신의 양심에 따라 행동할 의무가 있다. "
                "전제4: 올바른 양심은 자연법 원리를 올바르게 적용하며, 잘못된 양심은 지식의 부족이나 왜곡으로 인해 그렇지 못하다. "
                "결론: 양심은 자연법과 구체적 행위 사이를 매개하는 이성의 도덕적 기능이다."
            ),
            "counterpoint": (
                "루터(Martin Luther)는 『의지의 노예에 관하여(De Servo Arbitrio)』에서 인간의 이성과 양심이 원죄로 인해 근본적으로 손상되었으므로, "
                "양심에 따른 이성적 판단은 신뢰할 수 없으며 오직 성경의 말씀만이 도덕적 권위의 기초라고 주장했다. "
                "버틀러 주교(Bishop Butler)는 『열다섯 편의 설교(Fifteen Sermons)』에서 양심을 아퀴나스와 유사하게 도덕 판단의 최고 권위로 인정하면서도, "
                "그 근거를 신학적 자연법보다는 인간 본성의 구성에서 찾았다."
            ),
            "context": (
                "도덕 행위의 주관적 조건을 분석하는 맥락으로, 양심이 어떻게 도덕적 의무의 구체적 내용을 행위자에게 전달하는지를 설명하기 위한 것이다."
            ),
            "keywords": ["양심", "신데레시스", "conscientia", "이성과 도덕 판단", "올바른 양심"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "aquinas-claim-006",
            "thinker_id": "aquinas",
            "work_id": "aquinas-summa-theologiae",
            "source_detail": "IaIIae, q.62-63; IIaIIae 전반 (신학대전 제1-2부 제62-63문; 제2-2부)",
            "claim": "덕(virtus)에는 자연적 힘으로 획득 가능한 주요덕(사추덕: 지혜·정의·용기·절제)과 신의 은혜로 주어지는 신학적 덕(믿음·희망·사랑)이 있으며, 두 덕은 자연과 은혜의 관계로 연결된다.",
            "original_text": (
                "Virtutes theologicae supra naturam humanam sunt; "
                "virtutes autem morales et intellectuales sunt secundum naturam humanam, "
                "in quantum homo est rationalis."
            ),
            "explanation": (
                "아퀴나스의 덕 이론은 아리스토텔레스의 덕론을 신학적으로 확장한다: "
                "주요덕(사추덕, cardinal virtues): 지혜(prudentia), 정의(iustitia), 용기(fortitudo), 절제(temperantia). "
                "인간의 이성적 능력으로 습관을 통해 획득 가능하다(아리스토텔레스적 요소). "
                "신학적 덕(theological virtues): 믿음(fides), 희망(spes), 사랑(caritas). "
                "인간 본성의 능력을 초월하며 신의 은혜(gratia)로만 주어진다. "
                "이 두 덕은 대립하지 않는다: 은혜는 자연을 파괴하지 않고 완성한다(gratia non tollit naturam sed perficit)."
            ),
            "argument": (
                "전제1: 인간의 궁극적 목적은 두 가지이다: 자연적 목적(이성적 삶의 완성)과 초자연적 목적(신의 직접 관조, beatitudo). "
                "전제2: 자연적 목적을 위해서는 자연적 힘으로 획득할 수 있는 덕들(사추덕)이 필요하다. "
                "전제3: 초자연적 목적을 위해서는 자연을 초월하는 신의 은혜로 주어지는 덕들(신학적 덕)이 필요하다. "
                "전제4: 은혜는 자연의 위에 더해져 자연을 파괴하지 않고 오히려 완성한다. "
                "결론: 완전한 덕의 삶은 사추덕과 신학적 덕이 함께 작용할 때 실현된다."
            ),
            "counterpoint": (
                "루터는 『선행에 관하여(Von den guten Werken)』에서 인간의 자연적 능력으로 덕을 획득할 수 있다는 아퀴나스의 입장을 비판했다. "
                "원죄로 인해 인간 본성은 근본적으로 손상되었으므로, 덕은 인간의 노력이 아닌 오직 신의 은혜(sola gratia)로만 가능하다는 것이다. "
                "맥킨타이어(Alasdair MacIntyre)는 『덕의 상실(After Virtue)』에서 아퀴나스의 덕론이 "
                "아리스토텔레스 덕 윤리학의 가장 탁월한 신학적 통합이라고 평가하면서도, "
                "현대의 세속적 윤리학은 이 신학적 틀 없이 덕론의 온전한 의미를 복원하기 어렵다고 지적했다."
            ),
            "context": (
                "이성과 신앙, 자연과 은혜의 관계에 관한 아퀴나스의 종합적 입장을 윤리학에 적용하는 맥락이다."
            ),
            "keywords": ["사추덕", "신학적 덕", "믿음·희망·사랑", "은혜는 자연을 완성한다", "주요덕"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "aquinas-claim-007",
            "thinker_id": "aquinas",
            "work_id": "aquinas-summa-theologiae",
            "source_detail": "Ia, q.2, a.1 (신학대전 제1부 제2문 제1절); 대이교도대전 SCG I, c.3-4",
            "claim": "이성(철학)과 신앙(신학)은 서로 다른 방법으로 같은 진리에 접근할 수 있으며, 참된 이성은 참된 신앙과 충돌할 수 없다. 단, 신앙의 영역은 이성이 도달하기 어려운 초자연적 진리를 포함한다.",
            "original_text": (
                "Cum igitur duo praedicta veritatis genera non sint contraria, "
                "oportet ea in unum veritatis principium convenire."
                " (두 진리[이성적 진리와 신앙적 진리]는 서로 반대가 아니므로, 하나의 진리 원천으로 수렴해야 한다.)"
            ),
            "explanation": (
                "아퀴나스의 이성-신앙 관계론: "
                "이성의 영역: 자연적 이성만으로 접근 가능한 진리들(신의 존재, 세계의 질서, 도덕 원리 등). "
                "신앙의 영역: 계시를 통해서만 알 수 있는 초자연적 진리들(삼위일체, 성육신, 구원 등). "
                "두 영역은 '겹치기도 하고(신의 존재는 이성과 계시 모두로 알 수 있다) 구별되기도 한다(삼위일체는 오직 계시로만)'. "
                "참된 이성의 결론과 참된 신앙의 내용은 동일한 신적 진리에서 유래하므로, 진정한 충돌은 없다. "
                "이는 아베로에스주의자들의 이중진리론(철학적으로 참이면서 신학적으로도 참일 수 있다)을 거부한 것이다."
            ),
            "argument": (
                "전제1: 진리는 하나이며, 신이 그 원천이다. "
                "전제2: 이성적 진리와 계시적 진리는 모두 같은 신적 진리에서 유래한다. "
                "전제3: 같은 원천에서 나온 두 진리가 서로 모순될 수 없다. "
                "전제4: 이성과 신앙이 충돌하는 것처럼 보이면, 이성이나 신앙의 해석 중 하나가 잘못된 것이다. "
                "결론: 철학(이성)과 신학(신앙)은 적대 관계가 아니라 상호 보완 관계이며, 신학은 이성을 사용할 수 있고 사용해야 한다."
            ),
            "counterpoint": (
                "아베로에스(Ibn Rushd)의 추종자들은 '이중진리론'을 주장하며 철학적 결론과 신학적 결론이 독립적으로 각자의 영역에서 참일 수 있다고 보았다. "
                "테르툴리아누스(Tertullianus)는 『이단자들에 대한 변론(De Praescriptione Haereticorum)』에서 "
                "'아테네와 예루살렘이 무슨 관계인가'라고 반문하며, 이성(철학)은 신앙과 무관하거나 심지어 적대적이라고 주장했다. "
                "키르케고르는 『철학적 단편(Philosophiske Smuler)』에서 신앙은 이성의 한계를 '도약'으로 넘어서는 것이며, "
                "이성으로 신앙을 정초하려는 시도는 신앙의 본질을 훼손한다고 비판했다."
            ),
            "context": (
                "중세 대학에서 아리스토텔레스 철학의 도입으로 인해 발생한 이성-신앙 갈등을 해소하고, "
                "신학이 이성을 도구로 사용할 수 있음을 정당화하기 위한 맥락이다."
            ),
            "keywords": ["이성과 신앙", "철학과 신학", "이중진리론 비판", "자연 신학", "스콜라 철학"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "aquinas-claim-008",
            "thinker_id": "aquinas",
            "work_id": "aquinas-summa-theologiae",
            "source_detail": "IaIIae, q.96, a.4; IaIIae, q.95, a.2 (신학대전 제1-2부 제96문 제4절; 제95문 제2절)",
            "claim": "인정법(lex humana)은 자연법으로부터 도출되어야 하며, 자연법에 반하는 인정법은 진정한 의미의 법이 아니라 법의 타락(corruptio legis)이다. '부당한 법은 법이 아니다(lex iniusta non est lex)'.",
            "original_text": (
                "Lex iniusta non est lex. "
                "Sed lex humana in tantum habet rationem legis, in quantum est secundum regulam rationis."
            ),
            "explanation": (
                "아퀴나스의 법 이론에서 인정법의 정당성 조건: "
                "인정법이 정당하려면: (1) 공동선(bonum commune)을 목적으로 해야 한다. "
                "(2) 입법자의 권위 범위 안에 있어야 한다. "
                "(3) 시민들에게 공정하게 부담을 분배해야 한다. "
                "이 중 하나라도 어기면 부당한 법이다. "
                "부당한 법은 구속력이 없으며, 신법에 반하는 법에는 오히려 복종하지 않아야 한다. "
                "이 원칙은 후대 자연법론과 헌법주의의 기초가 되었다."
            ),
            "argument": (
                "전제1: 법의 본질은 공동선을 향한 이성의 명령이다. "
                "전제2: 인정법의 정당성 근거는 그것이 자연법과 이성의 원리에 부합하는 데 있다. "
                "전제3: 자연법에 반하는 인정법은 법의 본질적 조건(이성에 의한 공동선의 규율)을 충족하지 못한다. "
                "전제4: 법의 본질적 조건을 충족하지 못하면 그것은 법이 아니라 법의 외형을 띤 강제(violentia)이다. "
                "결론: 부당한 법은 도덕적 구속력이 없으며, 신앙인은 신법에 반하는 인정법에 저항할 수 있다."
            ),
            "counterpoint": (
                "법실증주의자 켈젠(Hans Kelsen)은 『순수법학(Reine Rechtslehre)』에서 법의 효력은 도덕이나 자연법이 아닌 "
                "상위의 법적 규범으로부터 도출된다고 주장했다. '법과 도덕의 분리'가 과학적 법학의 기초라는 것이다. "
                "오스틴(John Austin)은 『법의 범위(Province of Jurisprudence Determined)』에서 법은 주권자의 명령이며, "
                "그 내용의 도덕적 옳고 그름과 법으로서의 효력은 별개라고 주장했다."
            ),
            "context": (
                "시민적 복종과 저항권의 문제를 다루는 맥락으로, 국가 권력의 한계와 시민의 도덕적 의무를 규정하기 위한 것이다."
            ),
            "keywords": ["부당한 법은 법이 아니다", "인정법", "자연법과 실정법", "법의 정당성", "시민 불복종"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "aquinas-claim-009",
            "thinker_id": "aquinas",
            "work_id": "aquinas-de-malo",
            "source_detail": "De Malo, q.1, a.1 (악론 제1문 제1절); 신학대전 Ia, q.48",
            "claim": "악(malum)은 독자적 실체가 아니라 선(bonum)의 결여(privatio boni)이다. 신은 악을 창조하지 않으며, 악은 선한 존재의 결함이나 선의 부재로서만 존재한다.",
            "original_text": (
                "Malum non habet causam efficientem, sed deficientem. "
                "(악은 작용인이 없고, 다만 결핍의 원인만 있을 뿐이다.)"
            ),
            "explanation": (
                "아퀴나스는 아우구스티누스의 악의 결여설을 아리스토텔레스적 틀로 정교화한다. "
                "존재론적 악: 어떤 존재가 자신이 마땅히 가져야 할 완전성을 결여한 상태. "
                "예) 맹인은 보는 능력이 없다는 의미에서 악이 있다. "
                "도덕적 악(죄): 의지가 마땅히 따라야 할 이성적 질서를 벗어나는 행위. "
                "악에는 작용인이 없다: 선은 적극적 작용인으로 설명되지만, 악은 작용인의 결여(결함)로 설명된다. "
                "이 이론은 신이 왜 악을 창조하지 않는지를 설명한다: 신은 존재를 창조하며 존재는 선하므로, 악은 창조의 대상이 아니다."
            ),
            "argument": (
                "전제1: 존재하는 모든 것은 그 자체로 선하다(esse = bonum). "
                "전제2: 악이 실체(독립적 존재자)라면, 악도 그 자체로 선해야 한다는 모순이 생긴다. "
                "전제3: 악은 '마땅히 있어야 할 선이 없는 것'으로만 정의될 수 있다(결여, privatio). "
                "전제4: 따라서 악은 선한 존재 안에서만 존재하며, 독립된 실체가 아니다. "
                "전제5: 신은 선한 존재만을 창조하므로, 악은 신에게서 비롯되지 않는다. "
                "결론: 악은 선의 결여이며, 신의 선성(善性)과 세계의 악의 공존을 설명할 수 있다."
            ),
            "counterpoint": (
                "마니교(Manichaeism)는 선의 신과 악의 신이 동등하게 존재한다는 이원론을 주장했으며, "
                "아우구스티누스 자신도 한때 마니교에 심취했다가 이를 극복한 후 악의 결여설을 발전시켰다. "
                "라이프니츠(Leibniz)는 『변신론(Theodicée)』에서 악의 존재가 신의 전능·전지·전선과 모순된다는 악의 문제(problem of evil)를 다루며, "
                "이 세계가 가능한 세계들 중 최선의 세계임을 논증하려 했다. "
                "현대 신정론(theodicy) 논쟁에서 매키(J.L. Mackie)는 『악과 전능(Evil and Omnipotence)』에서 "
                "선하고 전능한 신과 악의 공존은 논리적으로 불가능하다고 주장했다."
            ),
            "context": (
                "신의 선성(善性)과 세계의 악의 공존이라는 신정론의 문제를 해결하고, "
                "선한 신이 창조한 세계에 악이 있는 이유를 설명하기 위한 맥락이다."
            ),
            "keywords": ["악의 결여설", "privatio boni", "신정론", "선과 악", "악의 본질"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "aquinas-claim-010",
            "thinker_id": "aquinas",
            "work_id": "aquinas-summa-theologiae",
            "source_detail": "IaIIae, q.1-5 (신학대전 제1-2부 제1-5문); IaIIae, q.3, a.8",
            "claim": "인간의 궁극적 행복(beatitudo)은 이 세상에서 완전히 실현될 수 없으며, 오직 내세에서 신을 직접 관조(visio beatifica)하는 것을 통해서만 완성된다. 아리스토텔레스의 에우다이모니아는 불완전한 행복이다.",
            "original_text": (
                "Beatitudo perfecta non potest esse in hac vita. "
                "Finis ultimus hominis est beatitudo perfecta, "
                "quae in sola Dei visione consistit."
            ),
            "explanation": (
                "아퀴나스는 아리스토텔레스의 행복론을 수용하면서도 초자연적 차원으로 확장한다. "
                "불완전한 행복(beatitudo imperfecta): 아리스토텔레스적 에우다이모니아. 현세에서 덕스러운 활동으로 실현. "
                "완전한 행복(beatitudo perfecta): 내세에서 신의 본질을 직접 바라보는 것(visio beatifica, 지복직관). "
                "이 완전한 행복은 인간 본성의 능력을 초월하므로, 신의 은혜 없이는 불가능하다. "
                "인간 지성은 모든 것을 알고자 하는 자연적 욕구가 있으며, 이 욕구는 오직 신 자체를 앎으로써만 충족될 수 있다."
            ),
            "argument": (
                "전제1: 인간 지성의 자연적 욕구는 진리 전체를 향해 있다. "
                "전제2: 이 욕구는 어떤 유한한 대상을 앎으로써도 완전히 충족되지 않는다. "
                "전제3: 현세의 행복은 언제나 결핍과 불완전함을 수반한다(질병, 죽음, 무지 등). "
                "전제4: 완전한 행복은 지성이 완전히 충족되는 상태, 즉 무한한 진리이자 선인 신 자체를 앎에서만 가능하다. "
                "전제5: 신을 직접 아는 것(visio beatifica)은 인간 본성을 초월하므로 은혜가 필요하다. "
                "결론: 인간의 궁극적 행복은 초자연적이며, 이 세상에서 완성될 수 없다."
            ),
            "counterpoint": (
                "아리스토텔레스는 『니코마코스 윤리학』 제1권에서 인간의 최고선은 현세에서 이성적 덕의 활동을 통해 실현되는 에우다이모니아라고 주장했다. "
                "아퀴나스가 에우다이모니아를 '불완전한 행복'으로 규정하는 것은 아리스토텔레스의 내재적 목적론을 초월론으로 변형시킨다는 비판이 있다. "
                "파도바의 마르실리우스(Marsilius of Padua)는 『평화의 수호자(Defensor Pacis)』에서 "
                "정치적·시민적 행복은 교회나 신학적 목적에 종속되지 않는 독자적 영역이라고 주장하며, "
                "아퀴나스의 자연적 행복과 초자연적 행복의 위계 구조를 비판했다."
            ),
            "context": (
                "인간의 궁극적 목적을 정의함으로써 도덕신학의 기초를 놓는 맥락으로, "
                "철학적 행복론(에우다이모니아)과 신학적 행복론(beatitudo)의 관계를 규정하기 위한 것이다."
            ),
            "keywords": ["지복직관", "beatitudo perfecta", "에우다이모니아 비교", "초자연적 행복", "신 관조"],
            "verified": False,
            "verification_log": []
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """토마스 아퀴나스 키워드 데이터 입력."""
    keywords = [
        {
            "id": "aquinas-kw-natural-law",
            "term": "자연법",
            "term_en": "Natural Law (Lex Naturalis)",
            "definition": (
                "아퀴나스 윤리학·법철학의 핵심 개념. "
                "영원법(lex aeterna, 신의 이성적 우주 통치 원리)에 이성적 피조물인 인간이 참여하는 것. "
                "자연법의 제1원리는 '선을 행하고 악을 피하라(bonum faciendum, malum vitandum)'. "
                "자연적 성향(자기 보존, 종족 번식, 이성적 진리 탐구)에 대응하는 구체적 도덕 원리들로 구성된다. "
                "인정법(인간의 실정법)의 정당성의 근거이며, 자연법에 반하는 인정법은 법이 아니다."
            ),
            "thinker_id": "aquinas",
            "work_id": "aquinas-summa-theologiae",
            "related_terms": ["영원법", "인정법", "신법", "자연적 성향", "양심"]
        },
        {
            "id": "aquinas-kw-eternal-law",
            "term": "영원법",
            "term_en": "Eternal Law (Lex Aeterna)",
            "definition": (
                "신의 이성(ratio divina) 안에 있는 우주 통치의 원리. "
                "신이 피조물을 창조하고 섭리하는 이성적 계획. "
                "이성적 피조물(인간)은 자신의 이성을 통해 영원법에 참여함으로써 자연법을 인식한다. "
                "비이성적 피조물은 본능적으로 영원법에 따른다. "
                "아퀴나스 법 이론의 최상위 층위."
            ),
            "thinker_id": "aquinas",
            "work_id": "aquinas-summa-theologiae",
            "related_terms": ["자연법", "신법", "인정법", "신의 섭리"]
        },
        {
            "id": "aquinas-kw-five-ways",
            "term": "다섯 가지 길",
            "term_en": "Five Ways (Quinque Viae)",
            "definition": (
                "아퀴나스가 신학대전 Ia, q.2, a.3에서 제시한 신의 존재를 위한 다섯 가지 이성적 논증. "
                "제1의 길: 운동으로부터(부동의 원동자). "
                "제2의 길: 작용인의 연쇄로부터(제1 작용인). "
                "제3의 길: 가능태와 필연성으로부터(필연적 존재). "
                "제4의 길: 완전성의 등급으로부터(최고 완전자). "
                "제5의 길: 자연의 목적 지향성으로부터(지성적 안내자). "
                "모두 경험에서 출발하는 사후 논증(a posteriori)이다."
            ),
            "thinker_id": "aquinas",
            "work_id": "aquinas-summa-theologiae",
            "related_terms": ["신의 존재 증명", "우주론적 논증", "목적론적 논증", "부동의 원동자"]
        },
        {
            "id": "aquinas-kw-esse-essentia",
            "term": "존재와 본질의 구분",
            "term_en": "Distinction of Esse and Essentia",
            "definition": (
                "아퀴나스 형이상학의 핵심 테제. "
                "피조물에서 본질(essentia, 무엇인가를 규정하는 것)과 존재(esse, 실제로 있음)는 실재적으로 구별된다. "
                "신에게서만 본질과 존재가 동일하다 — 신은 존재 자체(ipsum esse subsistens). "
                "이 구분은 피조물의 신에 대한 창조적 의존성을 형이상학적으로 설명한다. "
                "아리스토텔레스의 질료형상론을 넘어서는 아퀴나스의 독자적 형이상학적 통찰이다."
            ),
            "thinker_id": "aquinas",
            "work_id": "aquinas-de-ente-et-essentia",
            "related_terms": ["ipsum esse subsistens", "창조론", "신의 단순성", "피조물의 유한성"]
        },
        {
            "id": "aquinas-kw-synderesis",
            "term": "신데레시스",
            "term_en": "Synderesis",
            "definition": (
                "자연법의 제1원리들을 직접 파악하는 이성의 타고난 성향. "
                "아퀴나스에 따르면, 인간은 태어나면서부터 '선을 행하고 악을 피하라'는 기본 도덕 원리를 향하는 이성적 성향을 가진다. "
                "신데레시스는 오류가 없다(항상 선을 향하도록 지향되어 있다). "
                "양심(conscientia)은 이 신데레시스의 원리를 구체적 행위에 적용하는 이성의 행위이며, 오류 가능하다."
            ),
            "thinker_id": "aquinas",
            "work_id": "aquinas-summa-theologiae",
            "related_terms": ["양심", "자연법", "실천이성", "도덕 판단"]
        },
        {
            "id": "aquinas-kw-grace-nature",
            "term": "은혜는 자연을 완성한다",
            "term_en": "Gratia Perficit Naturam",
            "definition": (
                "아퀴나스 신학의 핵심 원리: '은혜(gratia)는 자연(natura)을 파괴하지 않고 완성한다(perficit).' "
                "이성(자연)과 신앙(은혜), 철학과 신학, 자연적 덕과 신학적 덕은 서로 배타적이지 않다. "
                "신의 은혜는 인간의 자연적 능력 위에 더해져 그것을 초자연적 목적으로 고양시킨다. "
                "이 원리는 아퀴나스의 이성-신앙 조화론, 자연-초자연 관계론의 토대이다."
            ),
            "thinker_id": "aquinas",
            "work_id": "aquinas-summa-theologiae",
            "related_terms": ["이성과 신앙", "자연법", "신학적 덕", "초자연적 행복"]
        },
        {
            "id": "aquinas-kw-beatitudo",
            "term": "지복(至福)",
            "term_en": "Beatitudo (Beatific Vision)",
            "definition": (
                "아퀴나스가 규정하는 인간의 궁극적 완전한 행복. "
                "아리스토텔레스의 에우다이모니아(현세적 행복)를 넘어서는 초자연적 목적. "
                "내세에서 신의 본질을 직접 관조(visio beatifica, 지복직관)함으로써 실현된다. "
                "인간 지성의 자연적 욕구(진리 전체를 알려는 욕구)는 오직 무한한 진리인 신 자체를 직접 앎으로써만 완전히 충족된다. "
                "이 행복은 인간 본성의 능력을 초월하므로 신의 은혜로만 가능하다."
            ),
            "thinker_id": "aquinas",
            "work_id": "aquinas-summa-theologiae",
            "related_terms": ["에우다이모니아", "visio beatifica", "초자연적 목적", "은혜", "신 관조"]
        },
        {
            "id": "aquinas-kw-privatio-boni",
            "term": "선의 결여 (악론)",
            "term_en": "Privatio Boni (Privation of Good)",
            "definition": (
                "악(malum)의 본질에 관한 아퀴나스(아우구스티누스)의 이론. "
                "악은 독립된 실체가 아니라, 어떤 존재가 마땅히 가져야 할 선(완전성)을 결여한 상태이다. "
                "예) 맹인은 시력이라는 선을 결여함. 악인은 이성적 질서를 따르는 덕을 결여함. "
                "이 이론은 신이 선한 존재들만을 창조했음에도 세계에 악이 존재하는 이유를 설명하며, "
                "마니교적 이원론(선·악의 두 신)을 반박한다."
            ),
            "thinker_id": "aquinas",
            "work_id": "aquinas-de-malo",
            "related_terms": ["악의 문제", "신정론", "선", "창조론", "자유의지"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """토마스 아퀴나스 관련 관계 데이터 입력."""
    # 기존 관계: aristotle-rel-002 (aristotle→aquinas, influenced) — 이미 입력됨
    # 새로 추가할 관계들 (아퀴나스 관점에서의 관계들)

    relations = [
        {
            "id": "aquinas-rel-001",
            "from_thinker": "aquinas",
            "to_thinker": "aristotle",
            "type": "synthesized",
            "description": (
                "아퀴나스는 아리스토텔레스 철학을 기독교 신학과 종합한 중세 최대의 철학적 성취를 이루었다. "
                "질료형상론(존재·본질 구분으로 심화), 4원인론(신의 존재 증명에 활용), "
                "목적론(자연법의 근거), 덕 윤리학(사추덕에 신학적 덕 추가) 등 아리스토텔레스의 핵심 개념들을 "
                "기독교적 맥락에서 재해석하고 심화했다. "
                "아퀴나스는 아리스토텔레스를 단순히 '철학자(The Philosopher)'라고 부를 만큼 그의 권위를 인정하면서도, "
                "자연적 질서를 초월하는 은혜와 초자연적 목적의 차원을 추가함으로써 아리스토텔레스 철학을 변형·확장했다."
            ),
            "evidence": "토마스 아퀴나스, 신학대전 Ia, IaIIae; 아리스토텔레스 니코마코스 윤리학 주석 전체"
        },
        {
            "id": "aquinas-rel-002",
            "from_thinker": "aquinas",
            "to_thinker": "augustine",
            "type": "synthesized",
            "description": (
                "아퀴나스는 아우구스티누스의 신학적 유산—은혜론, 원죄론, 악의 결여설, 신의 예지와 자유의지의 관계—을 "
                "아리스토텔레스적 철학 틀 위에서 재정립했다. "
                "아우구스티누스의 플라톤주의적 신학에서 아리스토텔레스주의적 스콜라 신학으로의 전환을 이루면서도, "
                "은혜의 필요성, 원죄의 현실, 신의 선성 등 아우구스티누스의 핵심 신학적 통찰을 유지했다. "
                "특히 악의 결여설(privatio boni)을 아리스토텔레스적 가능태·현실태 이론으로 심화했다."
            ),
            "evidence": "토마스 아퀴나스, 악론(De Malo) q.1; 신학대전 Ia q.48-49; 대이교도대전 SCG III"
        },
        {
            "id": "aquinas-rel-003",
            "from_thinker": "aquinas",
            "to_thinker": "kant",
            "type": "influenced",
            "description": (
                "아퀴나스의 자연법 윤리학은 칸트의 도덕철학에 간접적으로 영향을 미쳤다. "
                "칸트의 정언명법—특히 '보편법칙 정식'—은 자연법의 보편성에 대한 세속적 재정식화로 해석될 수 있다. "
                "그러나 칸트는 도덕의 근거를 이성의 자율성에서 찾고 자연적 성향이나 목적을 도덕의 근거에서 배제함으로써, "
                "아퀴나스의 목적론적 자연법론과 근본적으로 갈라진다. "
                "20세기 자연법 부흥(핀니스, 거리즈 등)은 아퀴나스 자연법론을 칸트적 의무론과의 대화 속에서 재해석했다."
            ),
            "evidence": "칸트, 도덕형이상학 기초(1785); 핀니스, 자연법과 자연권(1980)"
        },
        {
            "id": "aquinas-rel-004",
            "from_thinker": "aquinas",
            "to_thinker": "plato",
            "type": "criticized",
            "description": (
                "아퀴나스는 스콜라 철학의 전통에서 플라톤주의적 요소들을 비판적으로 수용했다. "
                "특히 플라톤의 이데아론(보편자의 선험적·독립적 존재)에 대해 아리스토텔레스와 마찬가지로 비판적이었으며, "
                "형상은 개별 사물 안에 내재한다는 아리스토텔레스적 질료형상론을 택했다. "
                "플라톤의 신플라톤주의적 유출설(emanationism)도 거부하고, 신과 피조물의 관계를 유출이 아닌 '창조(creatio ex nihilo)'로 설명했다. "
                "다만 플라톤의 신플라톤주의가 제공한 '신은 순수 선이자 일자'라는 통찰은 신의 속성 이해에 활용했다."
            ),
            "evidence": "토마스 아퀴나스, 존재와 본질 c.4; 신학대전 Ia q.44-45(창조론); 대이교도대전 SCG II c.15"
        },
        {
            "id": "aquinas-rel-005",
            "from_thinker": "aquinas",
            "to_thinker": "aquinas",
            "type": "influenced",
            "description": (
                "토마스 아퀴나스 사후 그의 철학은 '토미즘(Thomism)'이라는 학파를 형성하여 가톨릭 철학·신학의 주류가 되었다. "
                "1879년 교황 레오 13세의 회칙 '영원한 아버지(Aeterni Patris)'는 아퀴나스 철학을 가톨릭 교육의 표준으로 선포했다. "
                "20세기에는 마리탱(Jacques Maritain), 길송(Étienne Gilson), 핀니스(John Finnis) 등이 "
                "아퀴나스의 자연법론과 형이상학을 현대적으로 재해석하는 신토미즘(Neo-Thomism)을 전개했다."
            ),
            "evidence": "교황 레오 13세, Aeterni Patris(1879); 마리탱, 도덕철학(Moral Philosophy, 1960)"
        }
    ]

    # aquinas-rel-005는 자기 자신에 대한 것이라 의미가 없으므로 제거하고 실제 관계로 교체
    # 실제로는 아퀴나스가 후대에 미친 영향을 relations에 별도로 넣는 것은 맞지 않으므로 수정
    relations = relations[:4]  # 처음 4개만 사용

    for rel in relations:
        result = client.index(index=INDEX_RELATIONS, id=rel["id"], document=rel)
        print(f"[relation] {rel['id']}: {result['result']}")

    return len(relations)


def verify_insertion(client):
    """입력된 데이터를 간단히 검증한다."""
    print("\n=== 검증 ===")

    # thinker 확인
    thinker = client.get(index=INDEX_THINKERS, id="aquinas")
    print(f"[OK] thinker: {thinker['_source']['name']} ({thinker['_source']['name_en']})")

    # works 건수 확인
    works = search_documents(client, INDEX_WORKS, {"term": {"thinker_id": "aquinas"}}, size=20)
    print(f"[OK] works: {works['hits']['total']['value']}건")

    # claims 건수 확인
    claims = search_documents(client, INDEX_CLAIMS, {"term": {"thinker_id": "aquinas"}}, size=20)
    print(f"[OK] claims: {claims['hits']['total']['value']}건")

    # keywords 건수 확인
    keywords = search_documents(client, INDEX_KEYWORDS, {"term": {"thinker_id": "aquinas"}}, size=20)
    print(f"[OK] keywords: {keywords['hits']['total']['value']}건")

    # relations 건수 확인
    relations = search_documents(
        client, INDEX_RELATIONS,
        {"bool": {"should": [
            {"term": {"from_thinker": "aquinas"}},
            {"term": {"to_thinker": "aquinas"}}
        ], "minimum_should_match": 1}},
        size=20
    )
    print(f"[OK] relations (aquinas 관련): {relations['hits']['total']['value']}건")


def main():
    """메인 실행 함수."""
    print("=== 토마스 아퀴나스 데이터 입력 시작 ===\n")

    client = get_client()

    try:
        # 1. thinker 입력
        print("--- thinker 입력 ---")
        insert_thinker(client)

        # 2. works 입력
        print("\n--- works 입력 ---")
        n_works = insert_works(client)
        print(f"  총 {n_works}건 입력")

        # 3. claims 입력
        print("\n--- claims 입력 ---")
        n_claims = insert_claims(client)
        print(f"  총 {n_claims}건 입력")

        # 4. keywords 입력
        print("\n--- keywords 입력 ---")
        n_keywords = insert_keywords(client)
        print(f"  총 {n_keywords}건 입력")

        # 5. relations 입력
        print("\n--- relations 입력 ---")
        n_relations = insert_relations(client)
        print(f"  총 {n_relations}건 입력")

        # 6. 검증
        verify_insertion(client)

        print("\n=== 완료 ===")
        print(f"  thinker: 1건")
        print(f"  works: {n_works}건")
        print(f"  claims: {n_claims}건")
        print(f"  keywords: {n_keywords}건")
        print(f"  relations: {n_relations}건")

    finally:
        close_client(client)


if __name__ == "__main__":
    main()
