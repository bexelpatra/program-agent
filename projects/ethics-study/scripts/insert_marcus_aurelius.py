"""마르쿠스 아우렐리우스(Marcus Aurelius) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS
)


def insert_thinker(client):
    """마르쿠스 아우렐리우스 사상가 데이터 입력."""
    doc = {
        "id": "marcus_aurelius",
        "name": "마르쿠스 아우렐리우스",
        "name_en": "Marcus Aurelius",
        "field": "western_ethics",
        "era": "고대 로마·후기 스토아",
        "birth_year": 121,
        "death_year": 180,
        "background": (
            "로마 황제(재위 161~180)이자 스토아 철학자. "
            "로마 제국의 '오현제(Five Good Emperors)' 중 마지막 황제다. "
            "선대 황제 안토니누스 피우스의 양자로 입적되어 최고의 교육을 받았으며, "
            "어린 시절부터 철학에 이끌려 스토아 철학자 유니우스 루스티쿠스(Junius Rusticus)에게 사사했다. "
            "루스티쿠스를 통해 에픽테토스의 '담론집'을 접하고 깊은 영향을 받았다. "
            "재위 기간 대부분을 게르만족과의 전쟁(마르코만니 전쟁, 166~180)과 "
            "안토니누스 역병(165~180, 천연두 추정)의 위기 속에서 보냈다. "
            "이 극한 상황에서 군영의 천막 안에서 스토아적 성찰을 기록한 것이 '명상록(Τὰ εἰς ἑαυτόν)'이다. "
            "명상록은 출판을 의도하지 않은 개인적 성찰 일기로, "
            "스토아 철학의 가장 감동적이고 인간적인 문헌으로 평가된다."
        ),
        "core_philosophy": (
            "마르쿠스의 스토아 철학은 세 기둥에 의지한다: "
            "(1) 우주적 이성(λόγος)에 대한 믿음—모든 것은 로고스에 의해 질서 지어져 있으며, "
            "우리에게 일어나는 일은 이 질서의 일부다. "
            "(2) 덕(ἀρετή)의 자족성—외적 재화(건강, 재산, 권력)는 '선호되는 무관한 것(preferred indifferents)'이며, "
            "오직 덕(지혜, 정의, 용기, 절제)만이 진정한 선이다. "
            "(3) 사회적 존재로서의 의무—인간은 이성을 공유하는 공동체의 일원이며, "
            "타인에 대한 정의롭고 자비로운 행위가 자연에 따른 삶의 핵심이다. "
            "마르쿠스는 황제로서 엄청난 권력과 책임을 가졌기에, "
            "스토아 윤리학의 사회적·정치적 차원을 가장 잘 체현한 인물이다."
        ),
        "philosophical_journey": (
            "초기(121~161, 즉위 전): 소년 시절부터 철학에 이끌려 "
            "스토아 철학자 유니우스 루스티쿠스, 아폴로니오스, 섹스투스에게 사사했다. "
            "'명상록' 1권에서 각 스승에게 배운 것을 감사하며 열거한다. "
            "루스티쿠스가 에픽테토스의 '담론집'을 소개해준 것이 결정적 전환점이었다. "
            "중기(161~170, 즉위 초): 공동 황제 루키우스 베루스와 함께 통치하면서 "
            "파르티아 전쟁, 안토니누스 역병 등 위기에 직면했다. "
            "철학적 수양이 통치의 실질적 지침이 되었다. "
            "후기(170~180, 다뉴브 전선): 게르만족과의 전쟁에서 전선을 직접 지휘하며 "
            "군영 천막에서 '명상록'을 기록했다. "
            "전쟁, 역병, 배신 속에서도 스토아적 평정을 유지하려 애쓴 기록이 명상록의 핵심을 이룬다. "
            "180년 빈도보나(현 빈) 근처에서 병으로 사망했다."
        ),
        "keywords": [
            "명상록",
            "우주적 이성(로고스)",
            "자연에 따른 삶",
            "사회적 존재",
            "덕의 자족성",
            "무상(無常)",
            "내면의 성채"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="marcus_aurelius", document=doc)
    print(f"[thinker] marcus_aurelius: {result['result']}")
    return result


def insert_works(client):
    """마르쿠스 아우렐리우스 저서 데이터 입력."""
    works = [
        {
            "id": "marcus-meditations",
            "thinker_id": "marcus_aurelius",
            "title": "명상록",
            "title_original": "Meditations (Τὰ εἰς ἑαυτόν, Ta eis heauton, 'To Himself')",
            "year": 175,
            "significance": (
                "마르쿠스 아우렐리우스가 자기 자신에게 보내는 개인적 성찰 일기로, "
                "출판을 의도하지 않았다. 12권으로 구성되며, "
                "1권은 스승들에 대한 감사, 2~12권은 다뉴브 전선 등에서의 일상적 성찰이다. "
                "스토아 윤리학의 핵심 원리를 로마 황제의 개인적 고뇌와 결합시킨 독특한 문헌으로, "
                "스토아 철학 문헌 중 가장 널리 읽히며, "
                "권력의 정점에서 겸손과 덕을 추구한 기록으로 인류 문학의 고전이다. "
                "코이네 그리스어(Koine Greek)로 작성되었다."
            ),
            "key_concepts": [
                "자연에 따른 삶", "덕의 자족성", "무상(transience)",
                "우주적 관점", "사회적 의무", "내면의 성채(citadel)",
                "표상의 분석", "죽음에 대한 명상"
            ]
        },
        {
            "id": "marcus-letters-fronto",
            "thinker_id": "marcus_aurelius",
            "title": "프론토에게 보낸 서한집",
            "title_original": "Letters to Fronto (Epistulae ad M. Caesarem et invicem)",
            "year": 145,
            "significance": (
                "수사학 스승 프론토(Marcus Cornelius Fronto)와 주고받은 서한. "
                "1815년 안젤로 마이(Angelo Mai)가 바티칸과 밀라노 필사본에서 발견했다. "
                "마르쿠스의 청년기 사유를 보여주며, 수사학에서 철학으로 관심이 옮겨가는 과정, "
                "즉위 전 개인적 성격과 가치관을 엿볼 수 있는 자료다. "
                "철학적 내용보다는 전기적·역사적 가치가 크다."
            ),
            "key_concepts": [
                "수사학에서 철학으로의 전환", "스승 관계", "로마 황제의 교육"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """마르쿠스 아우렐리우스 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 모든 것은 변한다 — 무상(無常)의 명상
        {
            "id": "marcus-claim-001",
            "thinker_id": "marcus_aurelius",
            "work_id": "marcus-meditations",
            "source_detail": "Meditations II.14; IV.3.4; VI.15",
            "claim": (
                "모든 것은 변화하며 사라진다. 인간의 삶, 명성, 제국, 심지어 기억 자체도 무상하다. "
                "이 무상함을 깊이 인식하는 것은 절망이 아니라 해방이다—"
                "덧없는 것에 집착하지 않고 현재의 덕에 집중하게 해준다."
            ),
            "original_text": (
                "Πάντα ὅσα ὁρᾷς τάχιστα φθαρήσεται, "
                "καὶ οἱ φθειρόμενα αὐτὰ ἐποπτεύσαντες τάχιστα καὶ αὐτοὶ φθαρήσονται. "
                "(All that you see will soon perish, and those who watch them perishing "
                "will soon perish themselves. Meditations IX.33)"
            ),
            "original_text_ko": (
                "네가 보는 모든 것은 곧 소멸할 것이며, "
                "그것이 소멸하는 것을 지켜보는 자들도 곧 소멸할 것이다."
            ),
            "explanation": (
                "마르쿠스는 명상록 전체에 걸쳐 무상의 주제를 반복한다. "
                "위대한 황제들(아우구스투스, 하드리아누스)도 사라졌고, "
                "그들을 기억하는 자들도 사라졌으며, 기억 자체도 사라질 것이다. "
                "이 인식은 허무주의가 아니라 스토아적 치료제다: "
                "덧없는 것(명성, 쾌락, 권력)에 집착하는 것이 부질없음을 깨닫고, "
                "유일하게 영속적 가치를 가진 것—현재 순간의 덕의 실천—에 집중하게 해준다. "
                "또한 죽음에 대한 공포를 줄여주는 효과도 있다."
            ),
            "argument": (
                "(1) 자연은 끊임없이 변화한다—생성과 소멸이 자연의 본성이다(스토아 자연학). "
                "(2) 인간의 삶, 명성, 제국도 자연의 일부이므로 변화와 소멸을 피할 수 없다. "
                "(3) 과거의 위대한 인물들도 모두 사라졌으며, 그들에 대한 기억도 사라지고 있다. "
                "(4) 따라서 명성이나 사후 평판에 집착하는 것은 비합리적이다. "
                "(5) 영속적 가치를 가진 것은 오직 현재 순간의 덕의 실천뿐이다. "
                "(6) 무상에 대한 명상은 이 진실을 상기시켜 불필요한 집착에서 해방시킨다."
            ),
            "counterpoint": (
                "아리스토텔레스는 행복(에우다이모니아)에 외적 재화와 완전한 생애가 필요하다고 보아, "
                "마르쿠스처럼 덧없음에서 위안을 찾는 접근과 다르다. "
                "니체는 '영원회귀(Ewige Wiederkehr)' 사상에서 "
                "삶의 모든 순간이 영원히 반복된다면 그것을 긍정할 수 있는가를 물으며, "
                "무상에서 해방이 아니라 삶에 대한 최고의 긍정을 추구했다. "
                "불교의 무상(anicca)과 구조적으로 유사하지만, "
                "불교는 집착의 소멸(열반)을 목표로 하고 마르쿠스는 덕의 실천을 목표로 한다."
            ),
            "context": (
                "마르쿠스가 이 성찰을 기록한 시기는 안토니누스 역병(천연두)으로 "
                "제국 인구의 상당 부분이 사망하고 게르만족의 침입이 이어지던 때다. "
                "무상에 대한 명상은 추상적 철학이 아니라 "
                "대량 죽음을 매일 목격하는 황제의 실존적 대응이었다."
            ),
            "category": "형이상학·윤리학",
            "difficulty": "기본",
            "verified": False
        },
        # CLAIM-002: 내면의 성채 — 퇴각하여 자신을 회복하라
        {
            "id": "marcus-claim-002",
            "thinker_id": "marcus_aurelius",
            "work_id": "marcus-meditations",
            "source_detail": "Meditations IV.3; VII.28; VIII.48",
            "claim": (
                "인간은 자기 자신의 내면으로 퇴각할 수 있으며, "
                "이보다 더 조용하고 평화로운 피난처는 없다. "
                "외부 세계가 아무리 혼란스러워도 내면의 성채(ἡγεμονικόν)는 침범될 수 없다. "
                "자주 내면으로 퇴각하여 핵심 원칙을 상기시키는 것이 정신 건강의 비결이다."
            ),
            "original_text": (
                "Οὐδαμοῦ γὰρ οὔτε ἡσυχιώτερον οὔτε ἀπραγμονέστερον ἄνθρωπος ἀναχωρεῖ "
                "ἢ εἰς τὴν ἑαυτοῦ ψυχήν. "
                "(Nowhere can a person retreat more peacefully or quietly "
                "than into their own soul. Meditations IV.3)"
            ),
            "original_text_ko": (
                "인간이 자기 자신의 영혼보다 더 평화롭고 고요하게 퇴각할 수 있는 곳은 어디에도 없다."
            ),
            "explanation": (
                "마르쿠스는 시골 별장이나 해변으로의 은퇴를 꿈꾸는 것이 무의미하다고 지적한다. "
                "진정한 휴식은 외적 장소가 아니라 자기 내면에 있다. "
                "내면의 성채(헤게모니콘)에는 스토아적 핵심 원칙들이 있으며, "
                "이 원칙들을 상기하면 어떤 혼란 속에서도 평정을 회복할 수 있다. "
                "이것은 에픽테토스의 이분법(eph' hemin)의 실천적 적용이다. "
                "전선에서 전쟁을 지휘하면서 시골 별장으로 갈 수 없는 황제가 "
                "내면에서 평화를 찾는 실천적 기법이기도 했다."
            ),
            "argument": (
                "(1) 외적 환경(장소, 상황)은 우리에게 달려 있지 않으며 항상 변한다. "
                "(2) 외적 환경에서 평화를 찾으려는 것은 불안정한 것에 의존하는 것이다. "
                "(3) 내면(판단, 원칙)은 우리에게 달려 있으며 항상 접근 가능하다. "
                "(4) 스토아적 핵심 원칙(이분법, 덕의 자족성, 자연에 따른 삶)을 상기하면 "
                "마음의 혼란이 가라앉는다. "
                "(5) 따라서 자주 내면으로 퇴각하여 원칙을 상기하는 것이 "
                "가장 효과적이고 신뢰할 수 있는 정신 회복 방법이다."
            ),
            "counterpoint": (
                "마르크스주의 관점에서는 '내면의 성채'가 현실의 모순과 억압을 은폐하는 "
                "관념적 도피일 수 있다. 구조적 문제는 내면의 태도가 아니라 사회적 변혁으로 해결해야 한다. "
                "한나 아렌트는 '인간의 조건'(1958)에서 "
                "'내면으로의 퇴각'이 공적 공간에서의 행위를 포기하는 것이 될 수 있다고 경고했다. "
                "다만 마르쿠스는 내면으로 퇴각한 후 다시 사회적 의무로 돌아가는 것을 강조하므로, "
                "영구적 은둔과는 다르다."
            ),
            "context": (
                "마르쿠스가 전쟁터에서 이 성찰을 기록했다는 맥락이 중요하다. "
                "실제로 시골 별장으로 갈 수 없는 극한 상황에서 "
                "내면의 피난처를 찾는 실천적 필요에서 나온 통찰이다. "
                "현대 마인드풀니스(mindfulness)와 구조적 유사성이 있으며, "
                "라이언 홀리데이(Ryan Holiday) 등 현대 스토아주의 대중화에서 핵심 개념이다."
            ),
            "category": "윤리학·심리학",
            "difficulty": "기본",
            "verified": False
        },
        # CLAIM-003: 사회적 존재 — 인간은 서로를 위해 태어났다
        {
            "id": "marcus-claim-003",
            "thinker_id": "marcus_aurelius",
            "work_id": "marcus-meditations",
            "source_detail": "Meditations II.1; VI.44; VIII.59; IX.23",
            "claim": (
                "인간은 본성상 사회적 존재(κοινωνικὸν ζῷον)이며, "
                "이성을 공유하는 공동체의 일원이다. "
                "타인에게 해를 끼치는 것은 자기 자신에게 해를 끼치는 것이며, "
                "타인을 위해 일하는 것이 자연에 따른 삶이다. "
                "불쾌한 사람을 만나더라도 그들도 같은 이성을 공유하는 동료임을 기억해야 한다."
            ),
            "original_text": (
                "ἀλλήλων ἕνεκεν γεγόναμεν. "
                "(We were born for each other. Meditations IX.23)"
            ),
            "original_text_ko": (
                "우리는 서로를 위해 태어났다."
            ),
            "explanation": (
                "마르쿠스는 아침마다 '오늘 나는 참견하는 자, 배은망덕한 자, 거만한 자, "
                "사기꾼을 만날 것이다'라고 자신에게 말한다(II.1). "
                "그러나 이들도 이성을 공유하는 동료이며, 그들의 악행은 무지에서 비롯된다. "
                "스토아 철학에서 모든 이성적 존재는 우주적 이성(로고스)을 분유하며, "
                "따라서 하나의 공동체(코스모폴리스)를 이룬다. "
                "이 공동체에 대한 봉사가 자연에 따른 삶이며, "
                "타인을 해치는 것은 공동체를 해치는 것이고 결국 자기를 해치는 것이다."
            ),
            "argument": (
                "(1) 이성(로고스)은 인간에게 공통적이며, 모든 인간은 하나의 이성적 공동체를 이룬다. "
                "(2) 사회적 존재인 인간의 자연적 기능은 타인과 협력하고 공동선에 기여하는 것이다. "
                "(3) 타인에게 해를 끼치는 것은 공동체를 해치는 것이며, 자연에 반하는 행위다. "
                "(4) 타인의 악행은 이 진실에 대한 무지에서 비롯되므로 분노보다 연민이 적절하다. "
                "(5) 따라서 불쾌한 사람을 만나더라도 그가 이성을 공유하는 동료임을 기억하고, "
                "정의롭고 관대하게 대해야 한다."
            ),
            "counterpoint": (
                "에피쿠로스는 '숨어 살라(λάθε βιώσας, lathe biosas)'라는 격언으로 "
                "정치적·사회적 활동에서 물러나 사적 우정의 공동체에서 행복을 찾을 것을 권했다. "
                "이는 사회적 존재로서의 의무를 강조하는 마르쿠스의 입장과 정면으로 대립한다. "
                "홉스는 '리바이어던'(1651)에서 인간의 자연 상태는 '만인의 만인에 대한 전쟁'이라 하여 "
                "마르쿠스의 낙관적 사회관과 대조된다."
            ),
            "context": (
                "마르쿠스가 이 원칙을 실천한 맥락은 주목할 만하다. "
                "역병과 전쟁 속에서 로마 제국을 통치하며, "
                "카시우스(Avidius Cassius)의 반란까지 겪으면서도 "
                "관용과 정의를 실천하려 했다는 기록이 남아 있다. "
                "카시우스 반란 후 관련자들을 대대적으로 처벌하지 않은 것은 이 원칙의 실천으로 해석된다."
            ),
            "category": "윤리학·정치철학",
            "difficulty": "기본",
            "verified": False
        },
        # CLAIM-004: 덕만이 유일한 선이다
        {
            "id": "marcus-claim-004",
            "thinker_id": "marcus_aurelius",
            "work_id": "marcus-meditations",
            "source_detail": "Meditations III.6; V.12; VIII.1",
            "claim": (
                "오직 덕(ἀρετή)만이 진정한 선이고, 악덕만이 진정한 악이다. "
                "건강, 부, 명성, 쾌락은 '선호되는 무관한 것(preferred indifferents)'이며, "
                "질병, 빈곤, 고통은 '비선호 무관한 것'이다. "
                "이것들은 행복에 기여하거나 방해하지 않으며, "
                "행복은 오직 덕(지혜, 정의, 용기, 절제)의 실천에 달려 있다."
            ),
            "original_text": (
                "Αἰδεῖσθαι ἑαυτὸν μάλιστα. Δικαιοπραγεῖν. Ἀληθεύειν. "
                "(Respect yourself above all. Act justly. Speak the truth. Meditations VII.54, paraphrased)"
            ),
            "original_text_ko": (
                "무엇보다 자기 자신을 존중하라. 정의롭게 행하라. 진실을 말하라."
            ),
            "explanation": (
                "스토아 윤리학의 핵심 테제—덕만이 유일한 선(μόνον τὸ καλὸν ἀγαθόν)—을 "
                "마르쿠스는 황제로서의 일상에 적용한다. "
                "권력, 부, 명성의 정점에 있는 그가 이것들을 '무관한 것'으로 선언하는 것은 "
                "이론적 진술이 아니라 실존적 고백이다. "
                "사주덕(四主德: 지혜, 정의, 용기, 절제)을 매 순간 실천하는 것이 행복의 유일한 조건이며, "
                "외적 재화의 상실은 진정한 해악이 아니다."
            ),
            "argument": (
                "(1) 외적 재화(건강, 부, 명성)는 우리에게 달려 있지 않으며 운에 좌우된다. "
                "(2) 운에 좌우되는 것에 행복을 의존시키면 행복도 운에 좌우된다. "
                "(3) 진정한 행복은 안정적이어야 하므로, 운에 좌우되지 않는 것에 기초해야 한다. "
                "(4) 덕은 우리의 판단과 선택에 달려 있으므로 운에 좌우되지 않는다. "
                "(5) 따라서 오직 덕만이 행복의 안정적 기초를 제공할 수 있다. "
                "(6) 외적 재화는 있으면 좋지만 없어도 행복에 영향을 미치지 않는 '무관한 것'이다."
            ),
            "counterpoint": (
                "아리스토텔레스는 '니코마코스 윤리학' 1권에서 "
                "행복에는 덕뿐 아니라 외적 재화(건강, 부, 좋은 가문)도 필요하다고 보았다. "
                "'프리아모스의 운명처럼 극단적 불행 속에서 행복하다고 말할 수 없다'(1100a5-9). "
                "에피쿠로스는 쾌락의 부재가 곧 고통이므로, "
                "건강과 기본적 안락이 행복에 필수적이라 주장했다. "
                "현대 긍정심리학도 물질적 조건이 일정 수준 이하이면 행복에 유의미한 영향을 미친다고 본다."
            ),
            "context": (
                "마르쿠스가 제국의 부와 권력 한가운데서 이것들을 '무관한 것'으로 선언한 것은 "
                "스토아 철학의 진정성을 가장 극적으로 보여준다. "
                "빈곤한 노예(에픽테토스)와 세계 최고 권력자(마르쿠스)가 "
                "같은 결론에 도달한 것은 스토아 윤리학의 보편성을 증명한다."
            ),
            "category": "윤리학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-005: 우주적 관점 — 위에서 내려다보기
        {
            "id": "marcus-claim-005",
            "thinker_id": "marcus_aurelius",
            "work_id": "marcus-meditations",
            "source_detail": "Meditations VII.48; IX.30; XII.24",
            "claim": (
                "인간사를 우주적 관점에서 바라보면 모든 것이 작고 덧없다. "
                "우리의 삶은 무한한 시간과 공간 속에서 한 점에 불과하다. "
                "이 '위에서 내려다보기(view from above)'는 사소한 것에 대한 집착을 줄이고 "
                "진정으로 중요한 것(덕, 이성, 공동체)에 집중하게 해준다."
            ),
            "original_text": (
                "ὅσον τοι τὸ τῆς γῆς σημεῖον· καὶ τούτου πόστον γωνίδιον ἡ κατοίκησις αὕτη· "
                "(How small a portion of the earth is your dwelling! "
                "And how tiny a corner of it is this! Meditations VI.36)"
            ),
            "original_text_ko": (
                "땅 전체 중에서 네가 사는 곳이 얼마나 작은 점인지! "
                "그리고 이 작은 점 안에서 네 거주지가 얼마나 작은 구석인지!"
            ),
            "explanation": (
                "마르쿠스는 반복적으로 '위에서 내려다보기'라는 관상적 기법을 사용한다. "
                "상상으로 높이 올라가 인간사를 바라보면, "
                "전쟁, 축제, 장례, 결혼이 개미집처럼 작게 보인다. "
                "시간의 관점에서도 마찬가지다—과거의 모든 위대한 인물이 사라졌고, "
                "우리도 곧 사라질 것이다. "
                "이 우주적 관점은 사소한 욕망과 분노를 상대화하고, "
                "현재 순간의 이성적 행위에 집중하게 해주는 치료적 기법이다."
            ),
            "argument": (
                "(1) 지구는 우주에서 한 점이며, 우리의 삶은 영원한 시간에서 한 순간이다. "
                "(2) 이 사실을 깊이 인식하면 세속적 욕망(명성, 부, 권력)의 덧없음이 드러난다. "
                "(3) 덧없음을 인식하면 이런 욕망에 대한 집착이 자연스럽게 줄어든다. "
                "(4) 집착이 줄어들면 판단이 더 이성적이 되고, 진정으로 중요한 것에 집중할 수 있다. "
                "(5) 진정으로 중요한 것—현재 순간의 덕의 실천—은 시공간의 규모와 무관하게 가치 있다."
            ),
            "counterpoint": (
                "파스칼은 '팡세'(1670)에서 무한한 우주 앞에서 인간의 미소함이 "
                "공포와 불안을 낳을 수 있다고 보았다('무한한 공간의 영원한 침묵이 나를 두렵게 한다'). "
                "마르쿠스와 달리 파스칼은 이 경험에서 신앙의 필요성을 도출한다. "
                "실존주의(카뮈, '이방인' 1942)는 우주적 관점이 삶의 부조리를 드러내지만, "
                "거기서 위안이 아니라 반항적 긍정을 이끌어낸다."
            ),
            "context": (
                "'위에서 내려다보기'는 고대 철학에서 널리 사용된 정신 수련이다. "
                "키케로의 '스키피오의 꿈'(Somnium Scipionis)에서 스키피오가 하늘에서 지구를 내려다보며 "
                "로마의 영광이 얼마나 작은지 깨닫는 장면이 선행 형태다. "
                "마르쿠스는 이를 일상적 자기 수양의 도구로 체계화했다."
            ),
            "category": "형이상학·윤리학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-006: 현재에 집중하라 — 과거와 미래에 대한 걱정은 무의미하다
        {
            "id": "marcus-claim-006",
            "thinker_id": "marcus_aurelius",
            "work_id": "marcus-meditations",
            "source_detail": "Meditations II.14; III.10; VIII.36; XII.3",
            "claim": (
                "과거에 대한 후회와 미래에 대한 불안은 현재의 고통을 불필요하게 가중시킨다. "
                "우리가 실제로 살 수 있는 것은 오직 현재 순간뿐이며, "
                "현재 순간은 모든 사람에게 동등하게 주어진다. "
                "긴 삶을 사는 자나 짧은 삶을 사는 자나 잃는 것은 동일하게 '현재'뿐이다."
            ),
            "original_text": (
                "ὁ γὰρ μακρότατος βίος καὶ ὁ βραχύτατος εἰς ταὐτὸν καθίστανται. "
                "τὸ γὰρ παρὸν πᾶσιν ἴσον. "
                "(The longest and shortest lives amount to the same thing. "
                "The present is equal for all. Meditations II.14)"
            ),
            "original_text_ko": (
                "가장 긴 삶과 가장 짧은 삶은 같은 것에 이른다. "
                "현재는 모든 사람에게 동일하기 때문이다."
            ),
            "explanation": (
                "마르쿠스에 따르면 과거는 이미 지나갔고 미래는 아직 오지 않았다. "
                "우리가 실제로 경험하고 행위하는 것은 오직 현재 순간뿐이다. "
                "100년을 산 자도 20년을 산 자도 잃는 것은 동일하게 '현재 순간'뿐이다—"
                "과거는 이미 소유하고 있지 않고, 미래는 아직 소유하고 있지 않으므로. "
                "이 통찰은 미래에 대한 불안과 과거에 대한 후회를 불식시키고, "
                "현재 순간의 덕의 실천에 전적으로 집중하게 해준다."
            ),
            "argument": (
                "(1) 과거는 이미 지나가 돌이킬 수 없고, 미래는 아직 오지 않아 알 수 없다. "
                "(2) 우리가 실제로 행위하고 영향을 미칠 수 있는 것은 오직 현재 순간뿐이다. "
                "(3) 과거에 대한 후회나 미래에 대한 불안은 현재의 고통을 불필요하게 가중시킨다. "
                "(4) 모든 사람이 소유하고 잃는 것은 동등하게 '현재 순간'이다. "
                "(5) 따라서 긴 삶이 짧은 삶보다 더 많은 것을 가진 것이 아니다. "
                "(6) 현재 순간에 덕을 실천하는 것이 삶의 질을 결정하며, 이는 삶의 길이와 무관하다."
            ),
            "counterpoint": (
                "아리스토텔레스는 '니코마코스 윤리학' 1권에서 "
                "행복은 완전한 생애(bios teleios)에 걸쳐 평가되어야 한다고 주장했다. "
                "'한 마리의 제비가 봄을 만들지 않듯, 하루나 짧은 시간이 행복을 만들지 않는다'(1098a18-20). "
                "이는 마르쿠스처럼 현재 순간에 행복을 환원하는 것에 반대한다. "
                "하이데거는 '존재와 시간'(1927)에서 진정한 실존은 "
                "죽음을 향한 존재(Sein-zum-Tode)로서 미래를 직시하는 것이라 하여, "
                "과거·미래를 무시하는 접근과 다르다."
            ),
            "context": (
                "이 통찰은 현대 마인드풀니스(mindfulness) 수련과 구조적으로 유사하며, "
                "존 카밧진(Jon Kabat-Zinn)의 마음챙김 명상 프로그램에서도 인용된다. "
                "마르쿠스가 전선에서 언제 죽을지 모르는 상황에서 기록한 것임을 고려하면, "
                "현재에 대한 집중은 추상적 철학이 아니라 생존을 위한 실천이었다."
            ),
            "category": "윤리학",
            "difficulty": "기본",
            "verified": False
        },
        # CLAIM-007: 죽음은 자연의 작용이다
        {
            "id": "marcus-claim-007",
            "thinker_id": "marcus_aurelius",
            "work_id": "marcus-meditations",
            "source_detail": "Meditations II.4; IV.3.4; VI.15; IX.3",
            "claim": (
                "죽음은 자연의 작용이며, 자연의 작용을 두려워하는 것은 아이와 같다. "
                "죽음은 원소들이 흩어져 우주로 돌아가는 과정일 뿐이며, "
                "아우구스투스의 궁정도, 알렉산드로스의 제국도 모두 사라졌다. "
                "죽음에 대한 명상은 현재를 더 잘 살게 해준다."
            ),
            "original_text": (
                "Ὕλη ἦσθα, γέγονας ἄνθρωπος. Ἀπελεύσῃ εἰς τὸ σπέρμα. "
                "(You were matter; you became a human being. You will return to the seed. "
                "Meditations IV.14, paraphrased)"
            ),
            "original_text_ko": (
                "너는 물질이었다가 인간이 되었다. 다시 씨앗으로 돌아갈 것이다."
            ),
            "explanation": (
                "마르쿠스는 에피쿠로스와 다른 방식으로 죽음 공포를 극복한다. "
                "에피쿠로스가 '죽으면 감각이 없으므로 두려워할 것이 없다'고 한 반면, "
                "마르쿠스는 죽음을 자연의 순환으로 파악한다. "
                "스토아 물리학에 따르면 우주는 주기적으로 생성과 소멸을 반복(에크피로시스)하며, "
                "개체의 죽음은 원소들이 우주로 돌아가 새로운 형태를 취하는 자연스러운 과정이다. "
                "자연의 작용을 두려워하는 것은 비합리적이다."
            ),
            "argument": (
                "(1) 인간은 자연의 일부이며, 자연의 법칙에 따라 생겨나고 소멸한다. "
                "(2) 자연의 법칙은 합리적(이성적)이며 우주적 로고스의 표현이다. "
                "(3) 죽음은 이 자연 법칙의 일부로, 구성 원소들이 우주로 돌아가는 과정이다. "
                "(4) 자연적 과정을 두려워하는 것은 비합리적이며, 이성에 반한다. "
                "(5) 과거의 모든 위대한 인물(아우구스투스, 알렉산드로스)도 죽었으며, "
                "그들의 죽음이 우주에 아무런 해를 끼치지 않았다. "
                "(6) 따라서 죽음을 자연스럽게 받아들이고, 주어진 시간을 덕으로 채우는 것이 합리적이다."
            ),
            "counterpoint": (
                "에피쿠로스는 '죽음은 감각의 소멸이므로 우리에게 아무것도 아니다'라는 "
                "유물론적 논증으로 죽음 공포를 극복하려 했다. "
                "마르쿠스의 접근은 이와 다르다—죽음이 '아무것도 아닌 것'이 아니라 "
                "'자연의 합리적 작용'이라는 적극적 의미를 부여한다. "
                "플라톤은 '파이돈'에서 영혼의 불멸을 근거로 죽음을 영혼의 해방으로 보았지만, "
                "마르쿠스는 영혼의 불멸에 대해 확신하지 못했으며 "
                "('영혼이 소멸하든 흩어지든', Meditations IV.21) 이 불확실성 자체를 수용했다."
            ),
            "context": (
                "안토니누스 역병(165~180)으로 제국 인구의 상당 부분이 사망하는 상황에서 "
                "마르쿠스는 매일 죽음을 목격했다. "
                "명상록의 죽음에 대한 성찰은 추상적 사변이 아니라 "
                "대량 죽음의 한가운데에서의 실존적 대응이었다."
            ),
            "category": "형이상학·윤리학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-008: 타인의 악행에 분노하지 말라
        {
            "id": "marcus-claim-008",
            "thinker_id": "marcus_aurelius",
            "work_id": "marcus-meditations",
            "source_detail": "Meditations II.1; VI.27; IX.42; XI.18.9",
            "claim": (
                "타인의 악행에 분노하는 것은 비합리적이다. "
                "악행은 무지에서 비롯되며, 무지한 자를 탓하는 것은 눈먼 자를 탓하는 것과 같다. "
                "분노 자체가 덕에 반하는 격정(πάθος)이므로, "
                "악행을 하는 자보다 분노하는 내가 더 큰 해를 자신에게 끼친다."
            ),
            "original_text": (
                "Τὸ μὲν ἁμαρτάνειν ἀκούσιον· ψεῦδος γὰρ οὐδεὶς ἑκών. "
                "(Wrongdoing is involuntary; for no one willingly embraces falsehood. "
                "Based on Meditations XI.18.9, echoing Socrates)"
            ),
            "original_text_ko": (
                "잘못된 행위는 비자발적이다. 아무도 자발적으로 거짓을 받아들이지 않기 때문이다."
            ),
            "explanation": (
                "마르쿠스는 소크라테스의 '악행은 무지의 소산'이라는 통찰을 계승한다. "
                "사람이 잘못을 저지르는 것은 무엇이 진정으로 선한지 모르기 때문이다. "
                "만약 그들이 진정한 선(덕)을 알았다면 악을 행하지 않았을 것이다. "
                "따라서 악행에 대한 적절한 반응은 분노가 아니라 교정하려는 노력, "
                "그것이 불가능하면 관용과 연민이다. "
                "더구나 분노 자체가 나의 이성을 흐리고 덕에서 멀어지게 하므로, "
                "타인의 악행보다 나 자신의 분노가 더 큰 해악이다."
            ),
            "argument": (
                "(1) 모든 이성적 존재는 자신이 선이라고 판단하는 것을 추구한다(소크라테스 전통). "
                "(2) 악행을 하는 자는 진정한 선이 무엇인지에 대해 잘못된 판단을 가지고 있다. "
                "(3) 잘못된 판단은 무지에서 비롯되며, 무지는 자발적이지 않다. "
                "(4) 비자발적 무지에 대해 분노하는 것은 눈먼 자가 보지 못하는 것에 분노하는 것처럼 비합리적이다. "
                "(5) 분노 자체가 나의 이성적 상태를 해치는 격정이므로, 분노는 타인보다 나에게 더 해롭다. "
                "(6) 따라서 적절한 반응은 교정 시도 또는 관용이지, 분노가 아니다."
            ),
            "counterpoint": (
                "아리스토텔레스는 '니코마코스 윤리학' 4권에서 "
                "적절한 상황에서 적절한 정도의 분노는 덕(용기와 정의의 표현)이라 보았다. "
                "부정의에 대해 분노하지 않는 것은 오히려 비겁함이나 무감각이 될 수 있다. "
                "마르크스주의는 구조적 억압에 대한 분노가 사회 변혁의 동력이라 보아, "
                "분노를 억제하는 것이 기존 체제를 정당화할 수 있다고 비판한다."
            ),
            "context": (
                "마르쿠스는 카시우스(Avidius Cassius)의 반란(175년)을 겪었고, "
                "궁정 내 음모와 배신도 경험했다. "
                "이런 맥락에서 '분노하지 말라'는 가르침은 추상적 원칙이 아니라 "
                "실제 배신자들에 대한 태도를 자기에게 훈계하는 것이었다."
            ),
            "category": "윤리학",
            "difficulty": "보통",
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """마르쿠스 아우렐리우스 키워드 데이터 입력."""
    keywords = [
        {
            "id": "marcus-kw-001",
            "thinker_id": "marcus_aurelius",
            "term": "헤게모니콘 (Hegemonikon)",
            "term_original": "ἡγεμονικόν",
            "definition": (
                "지배적 이성 또는 영혼의 지도 원리. 스토아 심리학에서 영혼의 중심부로, "
                "인상(표상)을 수용하고 판단하며 충동을 발생시키는 이성적 기능. "
                "마르쿠스에게 '내면의 성채(inner citadel)'이며, "
                "외부 사건이 침범할 수 없는 자유의 공간이다. "
                "헤게모니콘을 올바르게 유지하는 것이 스토아적 덕의 핵심이다."
            ),
            "related_claims": ["marcus-claim-002", "marcus-claim-004"],
            "source": "Meditations IV.3; VII.28"
        },
        {
            "id": "marcus-kw-002",
            "thinker_id": "marcus_aurelius",
            "term": "코스모폴리스 (Cosmopolis)",
            "term_original": "κοσμόπολις",
            "definition": (
                "세계 도시 또는 우주적 공동체. 스토아 철학에서 모든 이성적 존재가 "
                "우주적 이성(로고스)을 공유하며 이루는 보편적 공동체. "
                "마르쿠스에게 로마 시민이기 이전에 코스모폴리스의 시민인 것이 더 근본적이며, "
                "이 보편적 공동체에 대한 의무(정의, 자비, 협력)가 가장 중요하다."
            ),
            "related_claims": ["marcus-claim-003"],
            "source": "Meditations IV.4; VI.44"
        },
        {
            "id": "marcus-kw-003",
            "thinker_id": "marcus_aurelius",
            "term": "아디아포라 (Adiaphora)",
            "term_original": "ἀδιάφορα",
            "definition": (
                "'무관한 것들' 또는 도덕적으로 중립적인 것들. "
                "스토아 윤리학에서 덕과 악덕 이외의 모든 것—건강, 부, 명성, 쾌락, 고통 등. "
                "이것들은 '선호되는 무관한 것(preferred indifferents)'과 "
                "'비선호 무관한 것(dispreferred indifferents)'으로 나뉘지만, "
                "어느 쪽이든 진정한 선도 악도 아니다. "
                "마르쿠스는 황제의 권력과 부조차 아디아포라로 간주했다."
            ),
            "related_claims": ["marcus-claim-004"],
            "source": "Meditations V.12; VIII.1"
        },
        {
            "id": "marcus-kw-004",
            "thinker_id": "marcus_aurelius",
            "term": "위에서 내려다보기 (View from Above)",
            "term_original": "θέα ἄνωθεν (thea anothen)",
            "definition": (
                "상상으로 높이 올라가 인간사를 우주적 관점에서 바라보는 스토아적 관상 기법. "
                "인간의 삶, 전쟁, 축제가 거시적 시공간에서 얼마나 작고 덧없는지 인식하여 "
                "사소한 집착을 상대화하고 진정으로 중요한 것(덕, 이성)에 집중하게 하는 정신 수련. "
                "키케로의 '스키피오의 꿈'에 선행 형태가 있으며, 마르쿠스가 체계적으로 활용했다."
            ),
            "related_claims": ["marcus-claim-005", "marcus-claim-001"],
            "source": "Meditations VII.48; IX.30"
        },
        {
            "id": "marcus-kw-005",
            "thinker_id": "marcus_aurelius",
            "term": "카타 퓌신 (Kata Physin)",
            "term_original": "κατὰ φύσιν",
            "definition": (
                "'자연에 따라' 또는 '본성에 따라'. 스토아 윤리학의 최고 원칙. "
                "인간의 자연(본성)은 이성이므로, 자연에 따른 삶은 이성에 따른 삶이다. "
                "동시에 인간은 우주적 자연(우주적 이성)의 일부이므로, "
                "우주적 질서에 조화롭게 사는 것도 자연에 따른 삶이다. "
                "마르쿠스에게 이것은 덕의 실천과 사회적 의무 이행을 의미한다."
            ),
            "related_claims": ["marcus-claim-003", "marcus-claim-004", "marcus-claim-007"],
            "source": "Meditations II.14; V.3; VII.55"
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """마르쿠스 아우렐리우스 관계 데이터 입력."""
    relations = [
        {
            "id": "relation-epictetus-marcus",
            "from_thinker": "epictetus",
            "to_thinker": "marcus_aurelius",
            "type": "influenced",
            "description": (
                "마르쿠스 아우렐리우스는 에픽테토스를 직접 만나지 않았으나, "
                "스승 유니우스 루스티쿠스로부터 에픽테토스의 '담론집'을 소개받아 "
                "깊은 영향을 받았다. 명상록에서 에픽테토스를 여러 번 언급하며, "
                "이분법, 표상의 사용, 역할 윤리 등 에픽테토스의 핵심 개념을 자신의 사유에 통합했다."
            ),
            "strength": "강함",
            "period": "2세기"
        },
        {
            "id": "relation-marcus-stoic-revival",
            "from_thinker": "marcus_aurelius",
            "to_thinker": "modern_stoicism",
            "type": "influenced",
            "description": (
                "마르쿠스의 '명상록'은 현대 스토아주의(Modern Stoicism) 부흥의 핵심 텍스트다. "
                "라이언 홀리데이(Ryan Holiday), 마시모 피글리우치(Massimo Pigliucci) 등이 "
                "명상록을 현대인의 자기계발과 정신건강에 적용하고 있다. "
                "또한 인지행동치료(CBT)의 철학적 원천으로 인정받고 있다."
            ),
            "strength": "강함",
            "period": "2세기 → 21세기"
        },
        {
            "id": "relation-socrates-marcus",
            "from_thinker": "socrates",
            "to_thinker": "marcus_aurelius",
            "type": "influenced",
            "description": (
                "소크라테스의 '덕은 앎이다', '악행은 무지의 소산', '영혼 돌봄'의 사상이 "
                "스토아 전통을 통해 마르쿠스에게 전해졌다. "
                "명상록에서 마르쿠스는 소크라테스를 여러 번 언급하며, "
                "특히 '악행은 비자발적(무지에서 비롯됨)'이라는 소크라테스적 원칙을 수용한다."
            ),
            "strength": "보통",
            "period": "기원전 5세기 → 기원후 2세기"
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
    r = client.get(index=INDEX_THINKERS, id="marcus_aurelius")
    print(f"[thinker] marcus_aurelius: name={r['_source']['name_en']}, era={r['_source']['era']}")

    # works 확인
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "marcus_aurelius"}})
    print(f"[works] marcus_aurelius 저서 수: {works_count['count']}")
    works_result = client.search(
        index=INDEX_WORKS,
        query={"term": {"thinker_id": "marcus_aurelius"}},
        _source=["id", "title_original", "year"]
    )
    for hit in works_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['title_original']} ({s['year']})")

    # claims 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "marcus_aurelius"}})
    print(f"[claims] marcus_aurelius 주장 수: {claims_count['count']}")
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "marcus_aurelius"}},
        size=10,
        _source=["id", "claim", "argument", "counterpoint", "original_text", "original_text_ko", "verified"]
    )
    missing_fields = []
    for hit in claims_result['hits']['hits']:
        s = hit['_source']
        has_arg = bool(s.get('argument'))
        has_cp = bool(s.get('counterpoint'))
        has_orig = bool(s.get('original_text'))
        has_orig_ko = bool(s.get('original_text_ko'))
        print(f"  - {s['id']}: argument={has_arg}, counterpoint={has_cp}, original_text={has_orig}, original_text_ko={has_orig_ko}, verified={s.get('verified')}")
        if not has_arg or not has_cp:
            missing_fields.append(s['id'])

    if missing_fields:
        print(f"[경고] argument/counterpoint 누락: {missing_fields}")
    else:
        print("[OK] 모든 claim에 argument+counterpoint 존재")

    # keywords 확인
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "marcus_aurelius"}})
    print(f"[keywords] marcus_aurelius 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_count = client.count(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "marcus_aurelius"}},
            {"term": {"to_thinker": "marcus_aurelius"}}
        ]}}
    )
    print(f"[relations] marcus_aurelius 관련 관계 수: {rel_count['count']}")
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "marcus_aurelius"}},
            {"term": {"to_thinker": "marcus_aurelius"}}
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
        "relations": rel_count['count'],
        "missing_fields": missing_fields
    }


def main():
    client = get_client()
    try:
        print("=== 마르쿠스 아우렐리우스(Marcus Aurelius) 데이터 입력 시작 ===\n")

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
