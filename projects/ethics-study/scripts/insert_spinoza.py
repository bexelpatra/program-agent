"""바뤼흐 스피노자(Baruch Spinoza) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS
)


def insert_thinker(client):
    """스피노자 사상가 데이터 입력."""
    doc = {
        "id": "spinoza",
        "name": "바뤼흐 스피노자",
        "name_en": "Baruch Spinoza",
        "field": "western_ethics",
        "era": "근대 합리론",
        "birth_year": 1632,
        "death_year": 1677,
        "background": (
            "암스테르담의 포르투갈계 유대인 가정에서 태어났다. "
            "유대교 공동체에서 전통 교육을 받았으나, 신에 대한 비정통적 견해로 "
            "1656년 24세의 나이에 유대교 회당에서 파문(cherem)당했다. "
            "이후 렌즈 깎는 기술자로 생계를 유지하며 철학 연구에 전념했다. "
            "데카르트 철학을 깊이 연구하되 이를 근본적으로 변형하여 독자적 체계를 구축했다. "
            "생전에 본명으로 출판한 저서는 '데카르트 철학의 원리'(1663) 한 권뿐이며, "
            "주저 '에티카'는 사후(1677)에 출판되었다. "
            "45세에 폐결핵으로 사망했으며, 사후에도 오랫동안 무신론자로 비난받았으나 "
            "18세기 이후 독일 관념론과 낭만주의에 지대한 영향을 미쳤다."
        ),
        "core_philosophy": (
            "스피노자 철학의 핵심은 실체 일원론과 '신즉자연(Deus sive Natura)' 테제다. "
            "자기원인(causa sui)인 유일한 실체가 곧 신이자 자연이며, "
            "모든 개별 사물은 이 실체의 양태(modus)에 불과하다. "
            "인간의 정신과 신체는 하나의 실체를 서로 다른 속성(사유와 연장)으로 표현한 것이다. "
            "윤리학에서는 감정(affectus)을 기하학적 방법으로 분석하고, "
            "적합한 인식(adequate knowledge)을 통해 수동적 감정(passio)을 극복하여 "
            "능동적 감정(actio)으로 전환하는 것이 자유와 행복의 길이라 주장한다. "
            "최고의 인식인 직관지(scientia intuitiva)로 신을 이해할 때 "
            "'신에 대한 지적 사랑(amor Dei intellectualis)'이 실현된다."
        ),
        "philosophical_journey": (
            "초기(~1660): 유대교 전통에서 벗어나며 데카르트 철학을 연구하고, "
            "합리론적 방법론을 독자적으로 발전시키기 시작했다. '지성개선론' 집필을 시작했으나 미완성. "
            "중기(1660~1670): 라인스뷔르흐(Rijnsburg)와 포르뷔르흐(Voorburg)에 거주하며 "
            "'에티카'의 초고를 작성하고, '신학정치론'(1670)을 익명으로 출판했다. "
            "신학정치론은 성서 비평과 사상의 자유를 옹호하여 큰 논쟁을 일으켰다. "
            "말기(1670~1677): 헤이그에 거주하며 '에티카'를 완성하고 '정치론'을 집필했으나, "
            "1677년 폐결핵으로 사망하여 정치론은 미완성으로 남았다. "
            "사후: 유고집(Opera Posthuma)으로 '에티카', '정치론', '지성개선론' 등이 출판되었다."
        ),
        "keywords": [
            "신즉자연(Deus sive Natura)",
            "실체 일원론",
            "코나투스(conatus)",
            "감정의 기하학",
            "직관지(scientia intuitiva)",
            "신에 대한 지적 사랑"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="spinoza", document=doc)
    print(f"[thinker] spinoza: {result['result']}")
    return result


def insert_works(client):
    """스피노자 저서 데이터 입력."""
    works = [
        {
            "id": "spinoza-ethica",
            "thinker_id": "spinoza",
            "title": "에티카",
            "title_original": "Ethica Ordine Geometrico Demonstrata",
            "year": 1677,
            "significance": (
                "스피노자의 주저. 기하학적 방법(정의-공리-정리-증명-주석)으로 서술된 "
                "형이상학·인식론·감정론·윤리학의 총체적 체계. "
                "5부로 구성되어 있다: 1부 '신에 대하여'(실체 일원론, 신즉자연), "
                "2부 '정신의 본성과 기원에 대하여'(심신평행론, 인식론), "
                "3부 '감정의 기원과 본성에 대하여'(코나투스, 감정의 기하학), "
                "4부 '인간의 예속에 대하여'(수동적 감정의 지배), "
                "5부 '지성의 능력 또는 인간의 자유에 대하여'(직관지, 신에 대한 지적 사랑). "
                "사후 유고집(Opera Posthuma, 1677)으로 출판되었다."
            ),
            "key_concepts": [
                "실체 일원론", "신즉자연", "속성과 양태", "심신평행론",
                "코나투스", "감정의 기하학", "직관지", "신에 대한 지적 사랑"
            ]
        },
        {
            "id": "spinoza-tractatus-theologico-politicus",
            "thinker_id": "spinoza",
            "title": "신학정치론",
            "title_original": "Tractatus Theologico-Politicus",
            "year": 1670,
            "significance": (
                "성서 비평과 사상의 자유를 체계적으로 논증한 저작. "
                "성서를 초자연적 계시가 아니라 역사적·문헌적으로 분석하여 "
                "근대 성서 비평학의 선구가 되었다. "
                "사상과 표현의 자유가 국가의 안정과 경건에 해를 끼치지 않으며 "
                "오히려 필수적임을 논증했다. "
                "1670년 익명으로 출판되었으나 곧 스피노자의 저작임이 알려져 "
                "격렬한 비난을 받았고, 1674년 네덜란드에서 금서로 지정되었다."
            ),
            "key_concepts": [
                "성서 비평", "사상의 자유", "예언의 본성",
                "국가와 종교의 관계", "자연권"
            ]
        },
        {
            "id": "spinoza-tractatus-de-intellectus-emendatione",
            "thinker_id": "spinoza",
            "title": "지성개선론",
            "title_original": "Tractatus de Intellectus Emendatione",
            "year": 1677,
            "significance": (
                "스피노자 인식론의 방법론적 서론에 해당하는 미완성 저작. "
                "참된 행복에 이르는 길을 탐구하며, 지성을 개선하는 방법을 제시한다. "
                "인식의 네 단계(전문·경험·추론·직관)를 구분하고, "
                "참된 관념에서 출발하여 체계적으로 인식을 확장하는 방법을 논한다. "
                "사후 유고집(Opera Posthuma, 1677)으로 출판되었다. "
                "에티카의 인식론적 기초를 이해하는 데 중요한 문헌이다."
            ),
            "key_concepts": [
                "지성의 개선", "인식의 네 단계", "참된 관념",
                "최고선의 탐구", "방법론"
            ]
        },
        {
            "id": "spinoza-tractatus-politicus",
            "thinker_id": "spinoza",
            "title": "정치론",
            "title_original": "Tractatus Politicus",
            "year": 1677,
            "significance": (
                "스피노자의 마지막 저작으로, 미완성 상태로 사후 출판되었다. "
                "신학정치론의 정치 이론을 더 체계적으로 발전시킨 저작으로, "
                "군주제·귀족제·민주제의 세 정체를 분석한다. "
                "인간을 있는 그대로(ut sunt) 분석하며, "
                "감정에 의해 움직이는 인간 본성에 기초한 현실적 정치 이론을 추구했다. "
                "민주제 부분에서 집필이 중단되었다."
            ),
            "key_concepts": [
                "자연권", "국가의 권리", "정체론",
                "감정에 기초한 정치학", "민주제"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """스피노자 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 신즉자연 (Deus sive Natura)
        {
            "id": "spinoza-claim-001",
            "thinker_id": "spinoza",
            "work_id": "spinoza-ethica",
            "source_detail": "Ethica I, Propositio 14-15; IV, Praefatio",
            "claim": (
                "신과 자연은 동일하다(Deus sive Natura). "
                "신은 초월적 인격신이 아니라, 무한한 속성을 지닌 유일한 실체로서 "
                "자연 전체와 동일하다. 신 외에는 어떤 실체도 존재하지 않으며, "
                "모든 것은 신 안에 있고 신 없이는 존재할 수도 사유될 수도 없다."
            ),
            "original_text": (
                "Praeter Deum nulla dari neque concipi potest substantia. "
                "(Besides God, no substance can be or be conceived. "
                "Ethica I, Prop. 14) "
                "Quicquid est, in Deo est, et nihil sine Deo esse neque concipi potest. "
                "(Whatever is, is in God, and nothing can be or be conceived without God. "
                "Ethica I, Prop. 15)"
            ),
            "original_text_ko": (
                "신 외에는 어떤 실체도 존재하거나 사유될 수 없다. (에티카 1부 정리 14) "
                "존재하는 모든 것은 신 안에 있으며, 신 없이는 어떤 것도 존재하거나 사유될 수 없다. "
                "(에티카 1부 정리 15)"
            ),
            "explanation": (
                "스피노자는 데카르트의 실체 개념을 급진적으로 밀고 나가 "
                "자기원인(causa sui)인 실체는 오직 하나뿐이며 그것이 곧 신이자 자연이라고 논증한다. "
                "신은 세계 밖에서 세계를 창조한 초월적 존재가 아니라 "
                "자연 전체의 내재적 원인(causa immanens)이다. "
                "이 입장은 전통 유신론(유대교·기독교)의 인격신 개념을 근본적으로 부정한다."
            ),
            "argument": (
                "(1) 실체는 자기원인(causa sui), 즉 그 본질이 존재를 포함하는 것이다. "
                "(2) 두 개 이상의 실체가 있다면 서로 속성이 같거나 다르다. 같다면 구별 불가, 다르면 서로 관계 불가. "
                "(3) 따라서 실체는 오직 하나이며, 이것이 무한히 많은 속성을 지닌 신이다. "
                "(4) 모든 개별 사물은 이 유일 실체의 양태(modus)이므로, 신 안에 있다. "
                "(5) 신은 능산적 자연(natura naturans)이자 소산적 자연(natura naturata)이다."
            ),
            "counterpoint": (
                "데카르트는 '성찰'(Meditationes de Prima Philosophia, 1641)에서 "
                "사유 실체(res cogitans)와 연장 실체(res extensa)를 분리하고, "
                "신을 이 둘과 구별되는 무한 실체로 설정하여 삼원론적 존재론을 주장했다. "
                "라이프니츠는 '모나돌로지'(Monadologie, 1714)에서 "
                "실체가 무한히 많다(모나드)고 주장하여 스피노자의 일원론을 정면으로 반박했다. "
                "또한 전통 유신론(토마스 아퀴나스 등)은 신과 피조물의 존재론적 구별을 핵심으로 하므로, "
                "스피노자의 신즉자연은 범신론 또는 무신론으로 비판받았다."
            ),
            "context": (
                "스피노자의 신 개념은 당대에 무신론으로 간주되어 격렬한 비난을 받았으나, "
                "18세기 '범신론 논쟁(Pantheismusstreit)'을 거쳐 "
                "독일 관념론(셸링, 헤겔)에 지대한 영향을 미쳤다. "
                "노발리스는 스피노자를 '신에 취한 사람(ein Gottbetrunkener Mensch)'이라 불렀다."
            ),
            "category": "형이상학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-002: 실체 일원론
        {
            "id": "spinoza-claim-002",
            "thinker_id": "spinoza",
            "work_id": "spinoza-ethica",
            "source_detail": "Ethica I, Definitio 3, 6; Propositio 5, 8, 14",
            "claim": (
                "존재하는 실체는 오직 하나이며, 그것은 무한히 많은 속성(attributum)을 지닌다. "
                "우리 인간이 인식할 수 있는 속성은 사유(cogitatio)와 연장(extensio) 두 가지뿐이다. "
                "모든 개별 사물은 이 유일 실체의 양태(modus)이다."
            ),
            "original_text": (
                "Per substantiam intelligo id quod in se est et per se concipitur. "
                "(By substance I understand what is in itself and is conceived through itself. "
                "Ethica I, Def. 3) "
                "Duae substantiae, quae diversa attributa habent, nihil inter se commune habent. "
                "(Two substances having different attributes have nothing in common. "
                "Ethica I, Prop. 2)"
            ),
            "original_text_ko": (
                "실체란 자기 안에 있으며 자기에 의해 사유되는 것이다. (에티카 1부 정의 3) "
                "서로 다른 속성을 가진 두 실체는 서로 공통점이 없다. (에티카 1부 정리 2)"
            ),
            "explanation": (
                "스피노자의 실체 일원론은 데카르트의 이원론(심신 이원)을 극복하려는 시도다. "
                "데카르트가 사유 실체와 연장 실체를 분리한 결과 심신 상호작용의 문제가 발생했는데, "
                "스피노자는 사유와 연장을 하나의 동일한 실체가 지닌 두 속성으로 봄으로써 "
                "이 문제를 원천적으로 해소한다. 개별 사물(인간 포함)은 실체가 아니라 양태이므로 "
                "독립적 존재가 아니라 실체(=신=자연)의 표현이다."
            ),
            "argument": (
                "(1) 실체는 '자기 안에 있고 자기에 의해 사유되는 것'이다(정의 3). "
                "(2) 같은 속성을 공유하는 두 실체는 구별 불가하므로 존재하지 않는다(정리 5). "
                "(3) 실체의 본성에는 존재가 속하므로 실체는 필연적으로 존재한다(정리 7). "
                "(4) 모든 실체는 무한하다(정리 8). "
                "(5) 따라서 무한히 많은 속성을 가진 실체(=신)는 유일하며, "
                "모든 유한한 것은 이 실체의 양태이다(정리 14-15)."
            ),
            "counterpoint": (
                "데카르트는 '철학의 원리'(Principia Philosophiae, 1644)에서 "
                "사유하는 실체(정신)와 연장을 가진 실체(물체)가 본성상 전혀 다른 별개의 실체라고 주장했다. "
                "이 이원론은 심신 상호작용의 난제(송과선 가설)를 남겼지만, "
                "정신의 자유와 도덕적 책임을 확보하는 이점이 있었다. "
                "라이프니츠는 실체를 무한히 많은 모나드로 보아 스피노자의 일원론과 데카르트의 이원론 "
                "모두를 거부하는 다원론(pluralism)을 제시했다."
            ),
            "context": (
                "17세기 합리론 철학에서 실체의 수와 본성은 핵심 논쟁 주제였다. "
                "데카르트(이원론), 스피노자(일원론), 라이프니츠(다원론)는 "
                "각각 다른 방식으로 실체 개념을 해석하며 근대 형이상학의 지형을 형성했다."
            ),
            "category": "형이상학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-003: 코나투스 (conatus)
        {
            "id": "spinoza-claim-003",
            "thinker_id": "spinoza",
            "work_id": "spinoza-ethica",
            "source_detail": "Ethica III, Propositio 6-7, 9; Scholium ad Prop. 9",
            "claim": (
                "각 사물은 자신의 존재를 유지하려는 노력(conatus)을 본질로 한다. "
                "이 코나투스가 정신에만 관계되면 의지(voluntas), "
                "정신과 신체에 함께 관계되면 욕망(appetitus 또는 cupiditas)이라 불린다. "
                "욕망은 인간 본질 그 자체이며, 모든 감정의 기초다."
            ),
            "original_text": (
                "Unaquaeque res, quantum in se est, in suo esse perseverare conatur. "
                "(Each thing, insofar as it is in itself, strives to persevere in its being. "
                "Ethica III, Prop. 6) "
                "Cupiditas est ipsa hominis essentia. "
                "(Desire is the very essence of man. Ethica III, Affect. Def. 1)"
            ),
            "original_text_ko": (
                "각 사물은 자기 안에 있는 한에서 자신의 존재를 유지하려고 노력한다. "
                "(에티카 3부 정리 6) "
                "욕망은 인간의 본질 그 자체이다. (에티카 3부 감정의 정의 1)"
            ),
            "explanation": (
                "코나투스는 스피노자 윤리학의 핵심 개념으로, "
                "존재 보존의 노력이 모든 사물의 가장 근본적인 활동임을 의미한다. "
                "이것은 외부에서 주어진 목적이 아니라 각 사물의 내재적 본성이다. "
                "인간의 경우 코나투스는 의식적 욕망(cupiditas)으로 나타나며, "
                "기쁨(laetitia)과 슬픔(tristitia)은 코나투스가 증가하거나 감소할 때 느끼는 감정이다. "
                "모든 감정은 궁극적으로 욕망·기쁨·슬픔의 세 기본 감정에서 파생된다."
            ),
            "argument": (
                "(1) 어떤 사물도 자기 스스로를 파괴하는 것을 포함하지 않는다(정리 4). "
                "(2) 각 사물은 다른 사물과 대립하는 한에서만 파괴될 수 있다(정리 5). "
                "(3) 따라서 각 사물은 자신의 존재를 유지하려는 노력(conatus)을 지닌다(정리 6). "
                "(4) 이 노력은 사물의 현행적 본질 그 자체이다(정리 7). "
                "(5) 코나투스가 증가하는 상태가 기쁨(laetitia), 감소하는 상태가 슬픔(tristitia)이며, "
                "이 두 감정과 욕망(cupiditas)이 모든 감정의 기초다."
            ),
            "counterpoint": (
                "홉스(Thomas Hobbes)는 '리바이어던'(Leviathan, 1651) 6장에서 "
                "유사한 자기 보존 충동(endeavour) 개념을 제시했으나, "
                "이를 사회계약의 동기로 활용하여 정치철학에 적용한 반면, "
                "스피노자는 코나투스를 존재론적·윤리학적 원리로 발전시켰다. "
                "칸트는 '순수이성비판'(Kritik der reinen Vernunft, 1781)에서 "
                "도덕의 원리를 자연적 충동이 아니라 순수 이성의 자율에서 찾아야 한다고 주장하여, "
                "코나투스와 같은 자연적 경향성에 기초한 윤리학을 비판했다."
            ),
            "context": (
                "코나투스 개념은 당대 역학(갈릴레오, 데카르트, 홉스)의 관성 법칙과 "
                "관련되지만, 스피노자는 이를 물리학을 넘어 형이상학과 윤리학의 핵심 원리로 확장했다. "
                "현대에는 들뢰즈(Gilles Deleuze)가 스피노자의 코나투스를 "
                "'역량(puissance)' 개념으로 재해석하며 주목받았다."
            ),
            "category": "윤리학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-004: 감정의 기하학
        {
            "id": "spinoza-claim-004",
            "thinker_id": "spinoza",
            "work_id": "spinoza-ethica",
            "source_detail": "Ethica III, Praefatio; Propositio 11, 56-59; Affect. Def.",
            "claim": (
                "감정(affectus)은 자연의 법칙에 따르는 현상이며, "
                "기하학적 방법으로 인식할 수 있다. "
                "감정은 결함이나 죄가 아니라 자연의 필연적 표현이므로, "
                "비난이나 조롱이 아니라 이해의 대상이다. "
                "기본 감정은 욕망(cupiditas), 기쁨(laetitia), 슬픔(tristitia) 세 가지이며, "
                "나머지 모든 감정은 이 셋의 조합이다."
            ),
            "original_text": (
                "Sedulo curavi humanas actiones non ridere, non lugere, neque detestari, "
                "sed intelligere. "
                "(I have taken great care not to laugh at human actions, not to weep at them, "
                "nor to detest them, but to understand them. "
                "Tractatus Politicus I.4; cf. Ethica III, Praefatio)"
            ),
            "original_text_ko": (
                "나는 인간의 행동을 비웃지도, 슬퍼하지도, 혐오하지도 않고 "
                "이해하려고 노력했다. (정치론 1.4; 에티카 3부 서문 참조)"
            ),
            "explanation": (
                "스피노자는 감정을 도덕적 판단 이전에 자연 현상으로 다룬다. "
                "데카르트가 '정념론'(Les Passions de l'Ame, 1649)에서 감정을 "
                "의지로 제어해야 할 대상으로 본 반면, "
                "스피노자는 감정을 자연의 필연적 법칙에 따르는 것으로 보고 "
                "기하학적 질서(정의-공리-정리)로 체계화한다. "
                "코나투스를 증가시키는 것은 기쁨(laetitia), 감소시키는 것은 슬픔(tristitia)이며, "
                "이 기본 감정의 조합으로 사랑·미움·희망·공포·질투 등 48가지 감정을 도출한다."
            ),
            "argument": (
                "(1) 자연에는 우연이 없으며 모든 것은 필연적으로 결정되어 있다. "
                "(2) 감정도 자연의 일부이므로 필연적 원인과 속성을 지닌다. "
                "(3) 따라서 감정은 기하학적 방법으로 탐구할 수 있다. "
                "(4) 기본 감정(욕망·기쁨·슬픔)에서 모든 복합 감정이 파생된다. "
                "(5) 감정의 원인을 이해하면 감정에 대한 수동적 예속에서 벗어날 수 있다."
            ),
            "counterpoint": (
                "데카르트는 '정념론'(Les Passions de l'Ame, 1649)에서 "
                "감정(정념)은 영혼과 신체의 결합에서 발생하며, "
                "의지의 노력으로 제어할 수 있다고 주장했다. "
                "스피노자는 이를 비판하며, 의지는 독립적 능력이 아니라 "
                "개별 의욕(volitio)의 총체에 불과하므로 감정을 의지로 직접 억제하는 것은 불가능하다고 보았다. "
                "흄(David Hume)은 '인간 본성에 관한 논고'(A Treatise of Human Nature, 1739-40)에서 "
                "이성은 정념의 노예이며 노예여야 한다고 주장하여, "
                "감정에 대한 이성의 우위를 더 급진적으로 부정했다."
            ),
            "context": (
                "17세기 합리론에서 감정은 대체로 이성에 의해 극복되어야 할 것으로 간주되었다. "
                "스피노자는 감정을 자연과학적으로 다루려 한 점에서 혁신적이며, "
                "이 접근은 현대 감정 이론(안토니오 다마지오 등)에서 재평가받고 있다."
            ),
            "category": "윤리학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-005: 자유와 필연
        {
            "id": "spinoza-claim-005",
            "thinker_id": "spinoza",
            "work_id": "spinoza-ethica",
            "source_detail": "Ethica I, Def. 7; I, Prop. 32; II, Prop. 48; V, Prop. 3-10",
            "claim": (
                "자유의지(liberum arbitrium)는 환상이다. "
                "모든 것은 신의 본성의 필연성에서 결정된다. "
                "그러나 자유(libertas)는 필연성과 양립 가능하다: "
                "자유란 외적 원인이 아니라 자기 본성의 필연성에 의해 행동하는 것이다. "
                "인간은 적합한 인식을 통해 수동적 감정의 예속에서 벗어나 "
                "자기 본성에 따라 행동할 수 있으며, 이것이 진정한 자유다."
            ),
            "original_text": (
                "Ea res libera dicitur, quae ex sola suae naturae necessitate existit "
                "et a se sola ad agendum determinatur. "
                "(That thing is said to be free which exists solely from the necessity "
                "of its own nature and is determined to action by itself alone. "
                "Ethica I, Def. 7)"
            ),
            "original_text_ko": (
                "오직 자기 본성의 필연성에 의해서만 존재하고 "
                "자기에 의해서만 행동하도록 결정되는 것이 자유롭다고 불린다. "
                "(에티카 1부 정의 7)"
            ),
            "explanation": (
                "스피노자는 통상적 의미의 자유의지—아무런 원인 없이 달리 행동할 수 있었다는 의미—를 부정한다. "
                "인간이 자유의지를 가졌다고 믿는 것은 자신의 욕구는 의식하면서 "
                "그 욕구의 원인은 모르기 때문이다(에티카 1부 부록). "
                "그러나 스피노자는 양립론적(compatibilist) 자유 개념을 제시한다: "
                "외적 원인에 의해 수동적으로 끌려가는 것이 예속이고, "
                "자기 본성의 필연성에 따라 행동하는 것이 자유다. "
                "적합한 인식을 통해 감정의 원인을 이해하면 수동적 감정이 능동적 감정으로 전환된다."
            ),
            "argument": (
                "(1) 자연에는 우연이 없으며 모든 것은 필연적 원인에 의해 결정된다(정리 I.29). "
                "(2) 의지(voluntas)는 보편적 능력이 아니라 개별 의욕의 총체이다(정리 II.48). "
                "(3) 인간이 자유의지를 믿는 것은 자기 욕구의 원인을 무지하기 때문이다(부록 I). "
                "(4) 그러나 자유는 필연성과 양립한다: 자기 본성에서 행동하는 것이 자유다(정의 I.7). "
                "(5) 적합한 인식(adequate knowledge)으로 감정의 원인을 이해하면 "
                "수동적 감정(passio)이 능동적 감정(actio)으로 전환된다(정리 V.3). "
                "(6) 이 전환이 예속에서 자유로의 이행이다."
            ),
            "counterpoint": (
                "데카르트는 '성찰'(Meditationes, 1641) 4성찰에서 "
                "자유의지를 인간이 가진 가장 완전한 능력으로 보았으며, "
                "이것이 신의 형상(imago Dei)을 반영한다고 주장했다. "
                "칸트는 '실천이성비판'(Kritik der praktischen Vernunft, 1788)에서 "
                "도덕적 자유를 현상계의 인과 결정론과 별도의 예지계에 위치시켜, "
                "자유와 필연의 양립을 스피노자와 전혀 다른 방식(초월적 자유)으로 해결했다. "
                "스피노자의 결정론적 자유는 자유의지를 부정한다는 점에서 "
                "도덕적 책임의 근거를 약화시킨다는 비판을 받았다."
            ),
            "context": (
                "자유의지 문제는 17세기 철학의 핵심 쟁점이었다. "
                "스피노자의 양립론적 자유 개념은 현대 양립론(compatibilism) 논의의 선구로 평가된다."
            ),
            "category": "윤리학/형이상학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-006: 직관지 (scientia intuitiva)와 신에 대한 지적 사랑
        {
            "id": "spinoza-claim-006",
            "thinker_id": "spinoza",
            "work_id": "spinoza-ethica",
            "source_detail": "Ethica II, Prop. 40, Schol. 2; V, Prop. 25-36",
            "claim": (
                "인식에는 세 종류가 있다: "
                "1종 인식(상상, imaginatio)—감각과 기호에 의한 혼란한 인식, "
                "2종 인식(이성, ratio)—공통 개념과 적합한 관념에 의한 인식, "
                "3종 인식(직관지, scientia intuitiva)—신의 속성의 적합한 관념에서 "
                "개별 사물의 본질에 대한 인식으로 나아가는 최고 인식. "
                "직관지에서 '신에 대한 지적 사랑(amor Dei intellectualis)'이 발생하며, "
                "이것이 최고의 행복(beatitudo)이다."
            ),
            "original_text": (
                "Mentis summa virtus est Deum cognoscere, sive res tertio cognitionis genere "
                "intelligere. "
                "(The greatest virtue of the mind is to know God, or to understand things "
                "by the third kind of knowledge. Ethica V, Prop. 25) "
                "Ex tertio cognitionis genere oritur necessario Amor intellectualis Dei. "
                "(From the third kind of knowledge there necessarily arises "
                "the intellectual love of God. Ethica V, Prop. 32, Corollary)"
            ),
            "original_text_ko": (
                "정신의 최고 덕은 신을 인식하는 것, 즉 제3종 인식으로 사물을 이해하는 것이다. "
                "(에티카 5부 정리 25) "
                "제3종 인식에서 필연적으로 신에 대한 지적 사랑이 발생한다. "
                "(에티카 5부 정리 32 따름정리)"
            ),
            "explanation": (
                "스피노자의 인식론은 윤리학과 직결된다. "
                "1종 인식(상상)은 감각에 의존하여 부적합하고 오류의 원천이며, "
                "2종 인식(이성)은 보편적 법칙을 파악하지만 개별 사물의 본질에 도달하지 못한다. "
                "3종 인식(직관지)은 신의 본성에서 출발하여 개별 사물을 영원의 상 아래(sub specie aeternitatis) "
                "직관적으로 파악한다. 이 인식에서 최고의 기쁨인 '신에 대한 지적 사랑'이 발생하며, "
                "이것이 곧 인간이 도달할 수 있는 최고의 행복(beatitudo)이다."
            ),
            "argument": (
                "(1) 인식이 적합할수록(adequate) 감정도 능동적이 된다. "
                "(2) 2종 인식(이성)은 사물의 보편적 속성을 파악하지만, "
                "3종 인식(직관지)은 개별 사물의 본질을 신의 속성에서 직접 파악한다. "
                "(3) 직관지로 사물을 인식할 때 가장 큰 기쁨이 발생한다(정리 V.27). "
                "(4) 이 기쁨에 원인으로서 신의 관념이 수반되므로, 이것이 '신에 대한 지적 사랑'이다(정리 V.32). "
                "(5) 이 사랑은 영원하며 파괴될 수 없다(정리 V.37). "
                "(6) 이것이 인간의 행복(beatitudo)이자 자유이며, 덕 그 자체다."
            ),
            "counterpoint": (
                "칸트는 '순수이성비판'(Kritik der reinen Vernunft, 1781)에서 "
                "지적 직관(intellektuelle Anschauung)은 인간에게 가능하지 않다고 주장했다. "
                "인간의 인식은 감성적 직관에 의존하며, 사물 자체(Ding an sich)를 "
                "직접 파악하는 것은 불가능하다. "
                "따라서 스피노자의 직관지 개념은 인간 인식의 한계를 넘어서는 "
                "독단적 형이상학이라는 비판을 받을 수 있다. "
                "키르케고르(Søren Kierkegaard)는 스피노자의 '영원의 상' 아래에서의 인식이 "
                "개별적 실존의 구체성과 결단의 의미를 간과한다고 비판했다."
            ),
            "context": (
                "'신에 대한 지적 사랑'은 에티카 5부의 결론이자 스피노자 윤리학의 최종 목표다. "
                "이것은 전통적 종교의 신 사랑(amor Dei)과 형태적으로 유사하지만, "
                "내용적으로는 이성적 인식에 기반한 철학적 사랑이다."
            ),
            "category": "인식론/윤리학",
            "difficulty": "심화",
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """스피노자 키워드 데이터 입력."""
    keywords = [
        {
            "id": "spinoza-kw-001",
            "thinker_id": "spinoza",
            "term": "신즉자연 (Deus sive Natura)",
            "term_original": "Deus sive Natura",
            "definition": (
                "신과 자연은 동일하다는 스피노자의 핵심 테제. "
                "신은 초월적 인격신이 아니라 무한한 속성을 지닌 유일한 실체이자 "
                "자연 전체의 내재적 원인이다. "
                "능산적 자연(natura naturans, 산출하는 자연 = 신의 속성)과 "
                "소산적 자연(natura naturata, 산출된 자연 = 양태의 총체)의 구별은 "
                "관점의 차이일 뿐 존재론적 분리가 아니다."
            ),
            "related_claims": ["spinoza-claim-001", "spinoza-claim-002"],
            "source": "Ethica I, Prop. 14-15, 29 Schol."
        },
        {
            "id": "spinoza-kw-002",
            "thinker_id": "spinoza",
            "term": "코나투스 (Conatus)",
            "term_original": "conatus",
            "definition": (
                "각 사물이 자신의 존재를 유지하려는 근본적 노력 또는 충동. "
                "스피노자 윤리학의 핵심 원리로, 인간에게서 이것은 의식적 욕망(cupiditas)으로 나타난다. "
                "코나투스의 증가가 기쁨(laetitia), 감소가 슬픔(tristitia)이며, "
                "이 세 감정(욕망·기쁨·슬픔)이 모든 감정의 기초이다."
            ),
            "related_claims": ["spinoza-claim-003", "spinoza-claim-004"],
            "source": "Ethica III, Prop. 6-9"
        },
        {
            "id": "spinoza-kw-003",
            "thinker_id": "spinoza",
            "term": "직관지 (Scientia Intuitiva)",
            "term_original": "scientia intuitiva",
            "definition": (
                "스피노자 인식론의 제3종 인식. 신의 속성의 적합한 관념에서 출발하여 "
                "개별 사물의 본질을 직관적으로 파악하는 최고의 인식 방식. "
                "이 인식에서 '신에 대한 지적 사랑(amor Dei intellectualis)'이 발생하며, "
                "이것이 인간이 도달할 수 있는 최고의 행복(beatitudo)이다."
            ),
            "related_claims": ["spinoza-claim-006"],
            "source": "Ethica II, Prop. 40 Schol. 2; V, Prop. 25-36"
        },
        {
            "id": "spinoza-kw-004",
            "thinker_id": "spinoza",
            "term": "양태 (Modus)",
            "term_original": "modus",
            "definition": (
                "실체의 변용(affectio), 즉 실체 안에 있고 실체에 의해 사유되는 것. "
                "스피노자의 일원론에서 모든 개별 사물(인간 포함)은 유일 실체(=신=자연)의 양태이다. "
                "양태는 독립적 존재가 아니라 실체의 표현이며, "
                "무한 양태(운동과 정지, 무한 지성)와 유한 양태(개별 사물)로 구분된다."
            ),
            "related_claims": ["spinoza-claim-001", "spinoza-claim-002"],
            "source": "Ethica I, Def. 5; I, Prop. 15, 25"
        },
        {
            "id": "spinoza-kw-005",
            "thinker_id": "spinoza",
            "term": "심신평행론 (Parallelism)",
            "term_original": "parallelismus (후대 용어)",
            "definition": (
                "정신과 신체는 하나의 동일한 실체를 서로 다른 속성(사유와 연장)으로 "
                "표현한 것이므로, 서로 인과적으로 작용하지 않지만 엄밀하게 대응한다. "
                "관념의 질서와 연결은 사물의 질서와 연결과 동일하다(Ethica II, Prop. 7). "
                "이로써 데카르트 이원론의 심신 상호작용 문제를 해소한다."
            ),
            "related_claims": ["spinoza-claim-002"],
            "source": "Ethica II, Prop. 7; III, Prop. 2 Schol."
        },
        {
            "id": "spinoza-kw-006",
            "thinker_id": "spinoza",
            "term": "영원의 상 (Sub Specie Aeternitatis)",
            "term_original": "sub specie aeternitatis",
            "definition": (
                "'영원의 관점에서' 사물을 보는 것. "
                "시간과 장소에 종속된 상상적 인식이 아니라, "
                "사물을 신의 본성에서 필연적으로 따라 나오는 것으로 이해하는 인식 방식. "
                "직관지(3종 인식)에서 달성되며, 이를 통해 정신의 영원성과 "
                "신에 대한 지적 사랑에 도달한다."
            ),
            "related_claims": ["spinoza-claim-006", "spinoza-claim-005"],
            "source": "Ethica V, Prop. 29-31"
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """스피노자 관계 데이터 입력."""
    relations = [
        {
            "id": "relation-descartes-spinoza",
            "from_thinker": "descartes",
            "to_thinker": "spinoza",
            "type": "influenced",
            "description": (
                "데카르트(René Descartes, 1596~1650)의 합리론적 방법론과 실체 개념은 "
                "스피노자 철학의 직접적 출발점이다. "
                "스피노자는 데카르트의 실체 정의('자기 안에 있고 자기에 의해 사유되는 것')를 "
                "급진적으로 밀고 나가 실체는 오직 하나(=신)뿐이라는 일원론에 도달했다. "
                "데카르트의 이원론(사유 실체와 연장 실체의 분리)과 심신 상호작용 문제를 "
                "속성 이론과 심신평행론으로 해소했다."
            ),
            "strength": "강함",
            "period": "17세기"
        },
        {
            "id": "relation-spinoza-leibniz",
            "from_thinker": "spinoza",
            "to_thinker": "leibniz",
            "type": "influenced",
            "description": (
                "라이프니츠(Gottfried Wilhelm Leibniz, 1646~1716)는 1676년 "
                "스피노자를 직접 방문하여 대화를 나누었고, 에티카 초고를 열람했다. "
                "라이프니츠는 스피노자의 일원론에 깊이 영향받았으나, "
                "이를 비판적으로 극복하여 다원론적 모나드론(Monadologie, 1714)을 발전시켰다. "
                "스피노자의 필연주의를 거부하고 가능세계 이론으로 우연성을 확보하려 했다."
            ),
            "strength": "보통",
            "period": "17세기 말"
        },
        {
            "id": "relation-spinoza-hegel",
            "from_thinker": "spinoza",
            "to_thinker": "hegel",
            "type": "influenced",
            "description": (
                "헤겔(Georg Wilhelm Friedrich Hegel, 1770~1831)은 "
                "'철학사 강의'(Vorlesungen über die Geschichte der Philosophie)에서 "
                "'스피노자주의에 빠지지 않으면 철학을 시작할 수 없다'고 평가했다. "
                "스피노자의 실체 일원론을 출발점으로 삼되, "
                "실체가 주체(Subjekt)이기도 해야 한다는 변증법적 발전을 통해 "
                "스피노자의 '무세계론(Akosmismus)'을 극복하려 했다."
            ),
            "strength": "강함",
            "period": "19세기 초"
        },
        {
            "id": "relation-stoics-spinoza",
            "from_thinker": "stoics",
            "to_thinker": "spinoza",
            "type": "influenced",
            "description": (
                "스토아 학파의 내재적 신 개념(로고스), 필연주의, "
                "감정 극복을 통한 자유의 추구는 스피노자 사상과 구조적 유사성이 있다. "
                "스피노자가 스토아 철학을 직접 계승했다고 단정하기는 어렵지만, "
                "감정을 이해와 인식으로 극복한다는 윤리학적 방향, "
                "신과 자연의 동일시(스토아의 범신론적 로고스), "
                "자유를 필연의 인식으로 보는 관점에서 깊은 친연성이 있다."
            ),
            "strength": "보통",
            "period": "고대~17세기"
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
    r = client.get(index=INDEX_THINKERS, id="spinoza")
    print(f"[thinker] spinoza: name={r['_source']['name_en']}, era={r['_source']['era']}")

    # works 확인
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "spinoza"}})
    print(f"[works] spinoza 저서 수: {works_count['count']}")
    works_result = client.search(
        index=INDEX_WORKS,
        query={"term": {"thinker_id": "spinoza"}},
        _source=["id", "title_original", "year"]
    )
    for hit in works_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['title_original']} ({s['year']})")

    # claims 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "spinoza"}})
    print(f"[claims] spinoza 주장 수: {claims_count['count']}")
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "spinoza"}},
        size=10,
        _source=["id", "claim", "argument", "counterpoint", "original_text", "original_text_ko", "verified"]
    )
    missing_fields = []
    for hit in claims_result['hits']['hits']:
        s = hit['_source']
        has_arg = bool(s.get('argument'))
        has_cp = bool(s.get('counterpoint'))
        has_ot = bool(s.get('original_text'))
        has_otko = bool(s.get('original_text_ko'))
        print(f"  - {s['id']}: argument={has_arg}, counterpoint={has_cp}, "
              f"original_text={has_ot}, original_text_ko={has_otko}, verified={s.get('verified')}")
        if not has_arg or not has_cp or not has_ot or not has_otko:
            missing_fields.append(s['id'])

    if missing_fields:
        print(f"[경고] 필수 필드 누락: {missing_fields}")
    else:
        print("[OK] 모든 claim에 argument+counterpoint+original_text+original_text_ko 존재")

    # keywords 확인
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "spinoza"}})
    print(f"[keywords] spinoza 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_count_from = client.count(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "spinoza"}},
            {"term": {"to_thinker": "spinoza"}}
        ]}}
    )
    print(f"[relations] spinoza 관련 관계 수: {rel_count_from['count']}")
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "spinoza"}},
            {"term": {"to_thinker": "spinoza"}}
        ]}},
        _source=["id", "from_thinker", "to_thinker", "type"]
    )
    for hit in rel_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['from_thinker']} --[{s['type']}]--> {s['to_thinker']}")

    return {
        "works": works_count['count'],
        "claims": claims_count['count'],
        "keywords": kw_count['count'],
        "relations": rel_count_from['count'],
        "missing_fields": missing_fields
    }


def main():
    client = get_client()
    try:
        print("=== 바뤼흐 스피노자(Baruch Spinoza) 데이터 입력 시작 ===\n")

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
