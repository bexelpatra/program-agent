"""에피쿠로스(Epicurus) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS
)


def insert_thinker(client):
    """에피쿠로스 사상가 데이터 입력."""
    doc = {
        "id": "epicurus",
        "name": "에피쿠로스",
        "name_en": "Epicurus",
        "field": "western_ethics",
        "era": "고대 그리스·헬레니즘",
        "birth_year": -341,
        "death_year": -270,
        "background": (
            "사모스(Samos) 섬에서 태어나 어린 시절 아테네에서 교육을 받았으며, "
            "이후 레스보스, 미틸레네, 람프사코스 등을 거쳐 기원전 307년경 아테네로 귀환했다. "
            "아테네 외곽에 '정원(The Garden, κῆπος)'을 구입하여 학교를 세웠는데, "
            "이 공동체는 플라톤의 아카데미아, 아리스토텔레스의 뤼케이온과 달리 "
            "여성, 노예, 이방인도 받아들인 포용적 공동체였다. "
            "에피쿠로스는 생전에 약 300편의 저작을 남겼다고 전해지나 "
            "대부분 소실되었으며, 오늘날 완전히 전하는 것은 디오게네스 라에르티오스가 "
            "'철학자 열전'(Lives and Opinions of Eminent Philosophers)에 수록한 세 편의 편지와 "
            "'주요 학설(Principal Doctrines, Kyriai Doxai)' 40개 명제뿐이다. "
            "루크레티우스의 '사물의 본성에 관하여(De Rerum Natura)'는 에피쿠로스 철학을 "
            "가장 상세히 전하는 라틴어 저작으로 사상 재구성에 필수적이다."
        ),
        "core_philosophy": (
            "에피쿠로스 윤리학의 핵심은 쾌락주의(hedonism)이되, 통속적 쾌락주의와 다르다. "
            "최고선은 쾌락(ἡδονή, hedone)이며, 쾌락의 최고 형태는 격렬한 흥분(kinetic pleasure)이 아니라 "
            "마음의 평정(ἀταραξία, ataraxia)과 육체적 고통의 부재(ἀπονία, aponia)다. "
            "이를 위해 세 가지 공포—신들의 징벌, 죽음, 고통—를 철학적으로 극복해야 한다. "
            "신들은 인간사에 개입하지 않으므로 두려움의 대상이 아니고, "
            "죽음은 감각의 소멸이므로 경험될 수 없어 두려워할 이유가 없으며, "
            "고통은 쾌락의 부재이므로 욕구를 최소화함으로써 줄일 수 있다. "
            "자연학에서는 데모크리토스의 원자론을 계승하되, 클리나멘(clinamen)이라는 "
            "원자의 무작위 이탈로 결정론을 벗어나 자유의지의 여지를 확보했다."
        ),
        "philosophical_journey": (
            "초기(~기원전 307): 람프사코스에서 공동체를 이끌며 원자론과 윤리학을 결합한 "
            "에피쿠로스주의 체계의 기초를 닦았다. "
            "중기(기원전 307~280경): 아테네 '정원' 공동체를 중심으로 제자들과 함께 생활하며 "
            "다수의 저작과 편지를 남겼다. 메노이케우스에게 보내는 편지, 헤로도토스에게 보내는 편지 등 "
            "핵심 문헌이 이 시기에 작성된 것으로 추정된다. "
            "말기(기원전 280~270): 신결석으로 큰 고통을 겪으면서도 정신적 평정을 유지했다고 전해진다. "
            "죽음을 앞두고 친구 이도메네우스에게 보낸 편지에서 "
            "'오늘 육체의 고통이 극심하지만 마음의 기쁨이 이를 능가한다'고 기록했다. "
            "사후(기원전 270 이후): 에피쿠로스주의는 로마 세계로 전파되어 루크레티우스, 필로데모스, "
            "키케로(비판적으로)를 통해 전승되었고, 근대 쾌락주의와 공리주의에 영향을 미쳤다."
        ),
        "keywords": [
            "쾌락주의",
            "아타락시아(마음의 평정)",
            "아포니아(고통 부재)",
            "죽음 공포 극복",
            "욕구 구분",
            "우정의 철학",
            "원자론",
            "정원 공동체"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="epicurus", document=doc)
    print(f"[thinker] epicurus: {result['result']}")
    return result


def insert_works(client):
    """에피쿠로스 저서 데이터 입력."""
    works = [
        {
            "id": "epicurus-letter-menoeceus",
            "thinker_id": "epicurus",
            "title": "메노이케우스에게 보내는 편지",
            "title_original": "Letter to Menoeceus (Ἐπιστολὴ πρὸς Μενοικέα)",
            "year": -300,
            "significance": (
                "에피쿠로스 윤리학의 가장 완결된 요약을 담은 핵심 문헌. "
                "쾌락주의의 의미, 신들에 대한 올바른 이해, 죽음 공포 극복, "
                "운명론과 자유의지, 욕구 구분(자연적·필요한/자연적·불필요한/헛된) 등 "
                "에피쿠로스 윤리학의 핵심 테제를 모두 담고 있다. "
                "'죽음은 우리에게 아무것도 아니다(death is nothing to us)'라는 유명한 명제가 여기에 나온다. "
                "디오게네스 라에르티오스의 '철학자 열전' 10권에 원문 전체가 보존되어 있다."
            ),
            "key_concepts": [
                "쾌락주의", "아타락시아", "아포니아", "죽음 공포 극복",
                "욕구 구분", "신들에 대한 올바른 이해", "자유의지"
            ]
        },
        {
            "id": "epicurus-letter-herodotus",
            "thinker_id": "epicurus",
            "title": "헤로도토스에게 보내는 편지",
            "title_original": "Letter to Herodotus (Ἐπιστολὴ πρὸς Ἡρόδοτον)",
            "year": -300,
            "significance": (
                "에피쿠로스 자연철학(원자론)을 요약한 문헌. "
                "원자와 허공(void)으로 구성된 우주론, 감각 지각 이론, "
                "영혼의 물질성, 세계의 다수성(multiple worlds) 등을 다룬다. "
                "데모크리토스의 원자론을 계승하되 윤리학적 목적—자연에 대한 이해로 공포를 극복—에 종속시킨다. "
                "디오게네스 라에르티오스의 '철학자 열전' 10권에 수록되어 있다."
            ),
            "key_concepts": [
                "원자론", "허공(void)", "감각 이론", "영혼의 물질성",
                "세계의 다수성", "자연철학"
            ]
        },
        {
            "id": "epicurus-principal-doctrines",
            "thinker_id": "epicurus",
            "title": "주요 학설",
            "title_original": "Principal Doctrines (Κύριαι Δόξαι, Kyriai Doxai)",
            "year": -290,
            "significance": (
                "에피쿠로스 철학의 핵심 명제 40개를 짧게 요약한 문헌. "
                "신, 죽음, 쾌락, 욕구, 우정, 정의 등 주요 주제를 간결하게 제시한다. "
                "특히 KD 31~38은 정의(justice)를 상호 불해(mutual non-harm)를 위한 계약으로 규정하며 "
                "사회계약론의 선구로 평가된다. "
                "KD 27은 우정을 행복한 삶에서 가장 중요한 수단으로 기술한다. "
                "디오게네스 라에르티오스의 '철학자 열전' 10권에 수록되어 있다."
            ),
            "key_concepts": [
                "쾌락과 최고선", "죽음 공포 극복", "정의의 계약적 기초",
                "우정의 가치", "자연적 욕구", "신들에 대한 태도"
            ]
        },
        {
            "id": "epicurus-vatican-sayings",
            "thinker_id": "epicurus",
            "title": "바티칸 격언집",
            "title_original": "Vatican Sayings (Gnomologium Vaticanum Epicureum)",
            "year": -280,
            "significance": (
                "1888년 바티칸 도서관에서 발견된 에피쿠로스 및 에피쿠로스 학파의 단편 모음(81개 격언). "
                "주요 학설에는 없는 더 개인적이고 실천적인 가르침을 담고 있다. "
                "우정, 단순한 삶의 기쁨, 욕구 절제, 죽음에 대한 태도 등을 다루며 "
                "에피쿠로스의 삶의 태도를 생생하게 보여준다. "
                "VS 52는 '우정은 춤을 추며 온 세상을 돌아다니며 우리를 불러 행복해지라고 한다'는 명구를 담는다."
            ),
            "key_concepts": [
                "우정", "단순한 삶", "자족", "쾌락의 실천", "삶의 태도"
            ]
        },
        {
            "id": "lucretius-de-rerum-natura",
            "thinker_id": "epicurus",
            "title": "사물의 본성에 관하여",
            "title_original": "De Rerum Natura",
            "year": -55,
            "significance": (
                "로마 시인 루크레티우스(Titus Lucretius Carus)가 에피쿠로스 철학을 "
                "6권의 장시(長詩)로 서술한 작품. 에피쿠로스 본인의 저작이 대부분 소실된 상황에서 "
                "에피쿠로스 자연철학과 윤리학을 가장 상세히 전하는 문헌이다. "
                "원자의 클리나멘(clinamen, 무작위 이탈)을 통한 자유의지 해명, "
                "죽음에 대한 공포 극복, 종교적 미신 비판 등을 담는다. "
                "에피쿠로스 사상의 2차 자료이지만 내용상 에피쿠로스 항목으로 분류한다."
            ),
            "key_concepts": [
                "클리나멘(clinamen)", "원자론", "자유의지", "죽음 공포 극복",
                "종교 비판", "자연철학"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """에피쿠로스 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 쾌락주의 — 최고선은 쾌락
        {
            "id": "epicurus-claim-001",
            "thinker_id": "epicurus",
            "work_id": "epicurus-letter-menoeceus",
            "source_detail": "Letter to Menoeceus, 128-129",
            "claim": (
                "쾌락(ἡδονή, hedone)은 행복한 삶의 시작이자 끝이다. "
                "쾌락이야말로 최고선이며, 고통의 부재(아포니아)와 마음의 평정(아타락시아)이 "
                "쾌락의 가장 완전한 형태다."
            ),
            "original_text": (
                "ἡδονὴν ἀρχὴν καὶ τέλος λέγομεν εἶναι τοῦ μακαρίως ζῆν. "
                "(We say that pleasure is the beginning and end of living blessedly.)"
            ),
            "explanation": (
                "에피쿠로스는 쾌락을 최고선으로 선언하되, 이를 방종이나 방탕과 혼동해서는 안 된다고 강조한다. "
                "그가 말하는 최고 쾌락은 격렬한 육체적 흥분이 아니라 "
                "고통도 공포도 없는 조용하고 안정된 상태(아타락시아+아포니아)이다. "
                "철학의 역할은 이 상태에 도달하도록 이성으로 욕구를 분별하고 불필요한 욕구를 제거하는 것이다."
            ),
            "argument": (
                "(1) 살아있는 모든 존재는 태어나는 순간부터 쾌락을 추구하고 고통을 피한다. "
                "(2) 이 자연적 경향성은 선과 악의 기준이 쾌락과 고통에 있음을 보여준다. "
                "(3) 그러나 모든 쾌락이 선택할 가치가 있는 것은 아니다—더 큰 고통을 낳는 쾌락은 거부해야 한다. "
                "(4) 최고의 쾌락 상태는 고통이 완전히 제거된 아포니아와 정신적 혼란이 없는 아타락시아다. "
                "(5) 따라서 철학은 욕구를 분별하여 이 최고 쾌락 상태를 실현하는 실천적 기술이다."
            ),
            "counterpoint": (
                "아리스토텔레스는 '니코마코스 윤리학'(Nikomacheia Ethika, 기원전 350경) 10권에서 "
                "최고선은 에우다이모니아(eudaimonia, 번영하는 삶)이며 단순한 쾌락의 추구와 구별된다고 주장했다. "
                "쾌락은 훌륭한 활동에 수반되는 것이지 목적 자체가 아니며, "
                "쾌락을 최고선으로 보는 것은 노예나 짐승의 삶을 선택하는 것과 같다고 비판했다(1095b19-20). "
                "또한 밀(J.S. Mill)은 '공리주의'(Utilitarianism, 1863) 2장에서 에피쿠로스의 쾌락주의를 "
                "옹호하면서도 쾌락의 질적 차이(higher vs lower pleasures)를 추가하여 단순 양적 쾌락주의를 수정했다."
            ),
            "context": (
                "플라톤의 '필레보스'(Philebus)와 아리스토텔레스의 '니코마코스 윤리학'이 쾌락의 지위를 "
                "이성·덕 아래에 두는 전통에 맞서, 에피쿠로스는 쾌락을 최고선으로 명시적으로 선언했다. "
                "이 입장은 당시에도 논쟁적이었으며 스토아 학파의 강한 비판을 받았다."
            ),
            "category": "윤리학",
            "difficulty": "기본",
            "verified": False
        },
        # CLAIM-002: 정적 쾌락 vs 동적 쾌락 구분
        {
            "id": "epicurus-claim-002",
            "thinker_id": "epicurus",
            "work_id": "epicurus-letter-menoeceus",
            "source_detail": "Letter to Menoeceus, 131-132; Principal Doctrines KD 3",
            "claim": (
                "쾌락에는 두 종류가 있다: 고통 부재의 정적 쾌락(katastematic pleasure)과 "
                "감각적 자극에서 오는 동적 쾌락(kinetic pleasure). "
                "최고 쾌락은 정적 쾌락, 즉 아타락시아와 아포니아다."
            ),
            "original_text": (
                "When we say that pleasure is the goal, we do not mean the pleasures of the "
                "profligate or the pleasures of consumption... but rather the absence of pain in "
                "the body and disturbance in the soul. (Letter to Menoeceus, 131)"
            ),
            "explanation": (
                "에피쿠로스는 쾌락을 동적 쾌락(욕구 충족 과정의 자극적 쾌감, 예: 먹고 마시는 즐거움)과 "
                "정적 쾌락(욕구가 완전히 충족되어 고통도 결핍도 없는 안정 상태)으로 구분한다. "
                "동적 쾌락은 욕구가 있어야 발생하므로 그 이전에 고통(결핍)을 전제한다. "
                "반면 정적 쾌락은 어떤 결핍도 없는 완전한 상태이므로 더 높은 쾌락이다. "
                "따라서 에피쿠로스의 이상적 삶은 자극적 쾌락보다 단순하고 절제된 삶에서의 평정에 있다."
            ),
            "argument": (
                "(1) 동적 쾌락은 욕구 충족 과정에서 발생하지만, 욕구는 고통(결핍)을 의미한다. "
                "(2) 욕구가 충족되면 동적 쾌락은 사라지고, 새 욕구가 생기면 다시 고통이 시작된다. "
                "(3) 따라서 동적 쾌락의 추구는 쾌락과 고통의 순환을 낳아 진정한 행복을 주지 못한다. "
                "(4) 정적 쾌락은 욕구가 완전히 충족된 '이미 고통이 없는' 상태이므로 더 안정적이고 완전하다. "
                "(5) 철학은 불필요한 욕구를 제거하여 가능한 한 빨리 정적 쾌락 상태(아타락시아)에 도달하도록 돕는다."
            ),
            "counterpoint": (
                "벤담(Jeremy Bentham)은 '도덕 및 입법의 원리 서론'(An Introduction to the Principles "
                "of Morals and Legislation, 1789)에서 쾌락의 질적 구분 없이 양(강도, 지속성, 확실성 등)으로 "
                "쾌락을 측정하는 '쾌락 계산법(felicific calculus)'을 제시했다. "
                "벤담은 정적·동적 구분보다 결과적으로 더 많은 쾌락을 낳는 선택이 도덕적으로 옳다고 보아, "
                "에피쿠로스의 정적 쾌락 우월성 주장을 받아들이지 않았다."
            ),
            "context": (
                "이 구분은 에피쿠로스주의가 방탕한 쾌락주의라는 오해를 반박하는 핵심 논거다. "
                "키레네 학파(Cyrenaics)는 동적 쾌락(즉각적 감각 자극)을 최고선으로 보았지만, "
                "에피쿠로스는 이를 명시적으로 거부하고 정적 쾌락을 더 높게 평가했다."
            ),
            "category": "윤리학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-003: 욕구의 세 가지 구분
        {
            "id": "epicurus-claim-003",
            "thinker_id": "epicurus",
            "work_id": "epicurus-letter-menoeceus",
            "source_detail": "Letter to Menoeceus, 127-128",
            "claim": (
                "욕구는 세 가지로 구분된다: "
                "(1) 자연적이고 필요한 욕구(음식, 피신처, 우정 등), "
                "(2) 자연적이지만 불필요한 욕구(호화로운 음식, 성적 쾌락 등), "
                "(3) 자연적이지도 필요하지도 않은 헛된 욕구(명예, 부, 권력에 대한 욕망). "
                "행복한 삶은 첫 번째 욕구만 충족시키면 충분하다."
            ),
            "original_text": (
                "Of desires, some are natural and necessary, others natural but not necessary, "
                "and others neither natural nor necessary but arising from groundless opinion. "
                "(Letter to Menoeceus, 127)"
            ),
            "explanation": (
                "에피쿠로스는 욕구를 분류하여 행복에 실제로 필요한 욕구와 불필요하게 고통을 유발하는 욕구를 구별한다. "
                "자연적이고 필요한 욕구(물, 단순한 음식, 기본적 피난처)는 쉽게 충족 가능하고 충족되지 않으면 고통을 낳는다. "
                "자연적이지만 불필요한 욕구(더 좋은 음식, 성적 쾌락)는 충족되지 않아도 고통을 낳지 않는다. "
                "헛된 욕구(명예, 불멸의 명성, 막대한 부)는 자연적 필요에서 비롯되지 않고 끝없는 추구를 낳는다. "
                "에피쿠로스 공동체의 절제된 생활 방식은 이 분류에 직접 근거한다."
            ),
            "argument": (
                "(1) 자연적이고 필요한 욕구는 충족되지 않으면 고통(아포니아의 결여)을 낳으므로 반드시 충족해야 한다. "
                "(2) 이 욕구들은 자연이 정해준 한계가 있으며 쉽게 충족 가능하다. "
                "(3) 헛된 욕구는 사회적 관습과 그릇된 의견에서 비롯되며, "
                "충족해도 새 욕구를 낳는 무한한 결핍 상태를 야기한다. "
                "(4) 따라서 철학자는 필요한 욕구만 충족시키고 헛된 욕구를 제거함으로써 "
                "아타락시아에 도달한다. "
                "(5) 단순하고 절제된 삶이 사실상 가장 풍요로운 삶이다."
            ),
            "counterpoint": (
                "아리스토텔레스는 '정치학'(Politika, 기원전 350경) 1권에서 "
                "인간은 본성상 폴리스 안에서 사회적·정치적으로 활동하는 존재(ζῷον πολιτικόν)이므로, "
                "에피쿠로스처럼 정치적 삶을 피하고 공동체에서 물러나 단순한 욕구 충족에 만족하는 것은 "
                "인간의 자연적 본성에 반한다고 비판했다. "
                "스토아 학파의 마르쿠스 아우렐리우스는 '명상록'(Meditations, 2세기경)에서 "
                "자연에 따른 삶은 덕(aretē)을 실현하는 사회적 의무 이행에 있다고 보아, "
                "욕구 절제만으로 충분하다는 에피쿠로스 관점에 암묵적으로 반대했다."
            ),
            "context": (
                "소크라테스 전통은 덕(aretē)이 행복의 충분조건이라 주장했지만, "
                "에피쿠로스는 욕구의 분류와 절제를 통해 실천 가능한 행복론을 제시했다. "
                "이 분류는 이후 스토아 학파의 '선호되는 것(preferred indifferents)' 개념과 "
                "비교되는 중요한 헬레니즘 윤리학 개념이다."
            ),
            "category": "윤리학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-004: 죽음 공포 극복
        {
            "id": "epicurus-claim-004",
            "thinker_id": "epicurus",
            "work_id": "epicurus-letter-menoeceus",
            "source_detail": "Letter to Menoeceus, 124-125",
            "claim": (
                "죽음은 우리에게 아무것도 아니다. "
                "우리가 존재할 때 죽음은 없고, 죽음이 있을 때 우리는 없다. "
                "죽음은 감각의 완전한 소멸이므로 두려워할 대상이 될 수 없다."
            ),
            "original_text": (
                "ὁ θάνατος οὐδὲν πρὸς ἡμᾶς· τὸ γὰρ διαλυθὲν ἀναισθητεῖ, "
                "τὸ δ' ἀναισθητοῦν οὐδὲν πρὸς ἡμᾶς. "
                "(Death is nothing to us; for that which has been dissolved has no sensation, "
                "and that which has no sensation is nothing to us.)"
            ),
            "explanation": (
                "에피쿠로스는 죽음 공포가 행복의 가장 큰 장애물 중 하나라고 진단하고, "
                "원자론적 자연학에 근거하여 이를 논리적으로 해소하려 한다. "
                "원자론에 따르면 죽음은 영혼 원자들의 흩어짐이며, 그 이후에는 감각이 없다. "
                "쾌락과 고통은 오직 감각을 통해서만 경험되므로, 감각이 없는 죽음 후 상태는 "
                "좋지도 나쁘지도 않다. 따라서 죽음을 두려워하는 것은 합리적이지 않다. "
                "이는 플라톤처럼 불사 영혼의 내세 보상을 근거로 삼지 않고 "
                "순수히 논리적으로 죽음 공포를 극복하는 유물론적 위로의 논증이다."
            ),
            "argument": (
                "(1) 영혼은 물질(원자)로 이루어져 있으며 죽으면 흩어진다(원자론 전제). "
                "(2) 감각은 영혼 원자들이 결합되어 있을 때만 가능하다. "
                "(3) 쾌락과 고통은 감각을 통해서만 경험될 수 있다. "
                "(4) 따라서 죽음 이후에는 어떤 감각도 없으므로 쾌락도 고통도 없다. "
                "(5) 쾌락이나 고통이 없는 상태는 우리에게 좋지도 나쁘지도 않다. "
                "(6) 결론: 죽음은 나쁜 것이 아니므로 두려움의 대상이 아니다. "
                "(보완) 죽음 이전의 공포 자체가 고통이므로, 철학적으로 공포를 제거하는 것이 핵심이다."
            ),
            "counterpoint": (
                "에픽테토스(Epictetus)와 스토아 학파는 '엥케이리디온'(Enchiridion, 2세기경)에서 "
                "죽음 공포 극복에 동의하지만, 그 근거를 에피쿠로스와 달리 제시한다. "
                "스토아 학파는 죽음 자체보다 죽음에 대한 '표상(impression)'과 판단을 바꾸는 것이 중요하다고 보며, "
                "의무와 덕을 다하며 사는 것이 죽음을 두려워하지 않는 진정한 근거라고 주장한다. "
                "플라톤은 '파이돈'(Phaidon, 기원전 385경)에서 철학자는 영혼의 불멸을 믿기에 죽음을 두려워하지 않으며, "
                "철학 자체가 '죽음의 연습(μελέτη θανάτου)'이라고 하여 전혀 다른 근거를 제시했다."
            ),
            "context": (
                "당시 그리스인들은 하데스(Hades)에서의 징벌, 운명의 여신들의 심판 등 "
                "죽음 이후의 공포를 종교적으로 경험했다. "
                "에피쿠로스는 이를 유물론적 논증으로 해소하려 했으며, "
                "루크레티우스는 '사물의 본성에 관하여' 3권에서 이 논증을 더 상세히 전개했다."
            ),
            "category": "윤리학",
            "difficulty": "기본",
            "verified": False
        },
        # CLAIM-005: 신들에 대한 무두려움
        {
            "id": "epicurus-claim-005",
            "thinker_id": "epicurus",
            "work_id": "epicurus-letter-menoeceus",
            "source_detail": "Letter to Menoeceus, 123-124; Principal Doctrines KD 1",
            "claim": (
                "신들은 완전히 복된 존재로서 인간사에 관여하지 않는다. "
                "신들로부터의 상이나 벌을 두려워하는 것은 신들의 본성에 대한 잘못된 이해에서 비롯된다. "
                "진정한 경건은 신들의 복된 본성을 올바로 아는 것이다."
            ),
            "original_text": (
                "τὸ μακάριον καὶ ἄφθαρτον οὔτε αὐτὸ πράγματα ἔχει οὔτε ἄλλῳ παρέχει, "
                "ὥστε οὔτε ὀργαῖς οὔτε χάρισι συνέχεται· ἐν ἀσθενεῖ γὰρ πᾶν τὸ τοιοῦτον. "
                "(That which is blessed and indestructible has no troubles itself, "
                "nor does it cause trouble for others; so it is not constrained by anger or "
                "favoritism. Principal Doctrines, KD 1)"
            ),
            "explanation": (
                "에피쿠로스는 신들의 존재 자체를 부정하지 않는다. "
                "그는 신들이 실재하지만 원자들 사이의 '간세계(interworld, metakosmos)'에 거주하며 "
                "인간사에 전혀 관여하지 않는 완전히 복된 존재라고 주장한다. "
                "완전히 복된 존재는 분노, 질투, 편애 같은 감정을 가질 수 없다—이런 감정은 불완전함의 표시이기 때문이다. "
                "따라서 신들의 징벌이나 심판을 두려워하는 종교적 공포는 신들의 본성을 잘못 이해한 데서 비롯된다. "
                "이 주장은 고대 종교적 세계관을 철학적으로 해체하는 급진적 입장이었다."
            ),
            "argument": (
                "(1) 복된 존재(신)는 정의상 결핍이나 좌절이 없어야 한다. "
                "(2) 분노, 편애, 처벌의 욕구는 결핍이나 방해에서 비롯되므로 완전히 복된 존재에게 있을 수 없다. "
                "(3) 신들이 인간사에 개입한다면 인간의 행위에 영향을 받는 것이므로, 완전한 복됨과 양립할 수 없다. "
                "(4) 따라서 신들은 인간사에 관여하지 않으며, 상이나 벌을 내리지 않는다. "
                "(5) 신들에 대한 공포는 잘못된 믿음에서 비롯된 것이므로 철학적 이해로 제거할 수 있다."
            ),
            "counterpoint": (
                "스토아 학파의 크리시포스(Chrysippus)는 (기원전 3~2세기 저작, 키케로 '신들의 본성에 관하여' "
                "De Natura Deorum를 통해 전해짐) 신들이 세계 이성(logos)으로서 우주의 섭리를 통해 "
                "인간의 삶에 의미를 부여한다고 주장했다. "
                "스토아 신학에서 신과 세계는 분리되지 않으며 신은 세계의 합리적 질서 자체다. "
                "플라톤은 '티마이오스'(Timaios, 기원전 360경)에서 데미우르고스(demiurge)가 "
                "세계를 선하게 만들기 위해 이데아를 모방하여 창조했다고 하여, "
                "신의 세계 관여를 긍정적으로 묘사했다."
            ),
            "context": (
                "호메로스의 신화적 전통에서 올림포스 신들은 인간의 운명에 직접 개입하고 "
                "희생제의를 통해 달랠 수 있는 존재로 묘사되었다. "
                "에피쿠로스는 이런 종교적 공포가 아타락시아의 핵심 장애물이라고 보고, "
                "신학을 철학적으로 재구성하여 종교적 불안을 해소하려 했다."
            ),
            "category": "종교철학·신학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-006: 우정의 중요성
        {
            "id": "epicurus-claim-006",
            "thinker_id": "epicurus",
            "work_id": "epicurus-principal-doctrines",
            "source_detail": "Principal Doctrines KD 27; Vatican Sayings VS 52",
            "claim": (
                "현명한 삶이 낳는 모든 것 중에서 우정(φιλία, philia)이 행복에 가장 크게 기여한다. "
                "우정은 행복한 삶을 위해 철학 다음으로 중요한, 또는 철학과 동등한 수단이다."
            ),
            "original_text": (
                "ὧν ἡ σοφία παρασκευάζεται εἰς τὴν τοῦ ὅλου βίου μακαριότητα, "
                "πολὺ μέγιστόν ἐστιν ἡ τῆς φιλίας κτῆσις. "
                "(Of all the things which wisdom provides for the blessedness of the whole life, "
                "by far the greatest is friendship. Principal Doctrines KD 27)"
            ),
            "explanation": (
                "에피쿠로스는 고통과 공포를 제거하는 데 철학과 우정 모두 필수적이라고 본다. "
                "우정은 고립된 개인이 위험·고통에 직면할 때 안전망이 되고, "
                "공유된 기쁨은 쾌락을 증대시키며, 친구의 존재 자체가 마음에 안도감을 준다. "
                "에피쿠로스의 '정원(Garden)' 공동체는 이 철학의 실천이었다. "
                "흥미롭게도 에피쿠로스는 우정이 처음에는 필요에서 시작하지만 "
                "시간이 지나면 그 자체로 사랑하게 된다고 보았다(Vatican Sayings VS 23)."
            ),
            "argument": (
                "(1) 인간은 위험과 고통으로부터 혼자 완전히 안전할 수 없다. "
                "(2) 신뢰할 수 있는 친구들로 이루어진 공동체는 외부 위험으로부터 보호를 제공한다. "
                "(3) 친구의 기쁨을 공유할 때 쾌락이 배가되고, 친구의 슬픔을 나눌 때 고통이 반감된다. "
                "(4) 믿을 수 있는 우정은 미래에 대한 안전감을 주어 아타락시아를 지속가능하게 한다. "
                "(5) 따라서 우정은 단순한 즐거움이 아니라 행복한 삶의 구조적 조건이다."
            ),
            "counterpoint": (
                "칸트는 '도덕형이상학'(Die Metaphysik der Sitten, 1797) 우정 론에서 "
                "진정한 우정은 도덕적 의무와 상호 존중을 기반으로 해야 하며, "
                "쾌락이나 이익을 근거로 한 우정은 불완전하다고 주장했다. "
                "에피쿠로스의 우정이 궁극적으로 쾌락·안전이라는 자기이익에 근거한다면 "
                "칸트적 의미의 진정한 우정이 될 수 없다는 비판이 가능하다. "
                "아리스토텔레스는 '니코마코스 윤리학'(기원전 350경) 8~9권에서 우정을 덕에 기반한 완전한 우정, "
                "쾌락에 기반한 우정, 유익함에 기반한 우정으로 구분하고, "
                "에피쿠로스의 우정 개념은 쾌락·유익함 범주에 그칠 위험이 있다고 간접적으로 시사했다."
            ),
            "context": (
                "에피쿠로스주의는 흔히 개인적·은둔적 삶을 권장한다고 오해되지만, "
                "에피쿠로스 자신은 '정원' 공동체를 직접 이끌며 깊은 우정 관계를 맺었다. "
                "'조용히 살아라(lathe biōsas)'는 격언은 정치적 삶을 피하라는 것이지 "
                "사회적 고립을 권장하는 것이 아니다."
            ),
            "category": "윤리학",
            "difficulty": "기본",
            "verified": False
        },
        # CLAIM-007: 정의의 계약론적 기초
        {
            "id": "epicurus-claim-007",
            "thinker_id": "epicurus",
            "work_id": "epicurus-principal-doctrines",
            "source_detail": "Principal Doctrines KD 31-33",
            "claim": (
                "정의(δικαιοσύνη, dikaiosynē)는 자연적으로 주어진 덕이 아니라 "
                "상호 불해(mutual non-harm)를 위해 사람들 사이에 맺어진 계약이다. "
                "정의는 계약을 체결한 사람들 사이에서만 성립하며, "
                "계약이 없는 곳에는 정의도 부정의도 없다."
            ),
            "original_text": (
                "Ἡ δικαιοσύνη οὐκ ἦν τι καθ' ἑαυτό, ἀλλ' ἐν ταῖς μετ' ἀλλήλων συστροφαῖς "
                "καθ' ὁποίους δήποτε ἀεὶ τόπους συνθήκη τις ὑπὲρ τοῦ μὴ βλάπτειν ἢ βλάπτεσθαι. "
                "(Justice was never anything in itself, but in dealings of people with each other "
                "in any place whatever and at any time, it is a kind of compact not to harm or be harmed. "
                "Principal Doctrines KD 33)"
            ),
            "explanation": (
                "에피쿠로스의 정의론은 플라톤·아리스토텔레스의 자연적 정의론과 대조된다. "
                "플라톤에게 정의는 영혼의 조화라는 자연적 덕이고, 아리스토텔레스에게는 폴리스의 자연적 목적에 따른 덕이다. "
                "그러나 에피쿠로스에게 정의는 순전히 도구적이다: "
                "사람들이 서로 해치지 않기 위해 합의한 계약이며, 이 계약을 지키는 것이 개인의 아타락시아에 유리하기 때문에 정의롭게 행동한다. "
                "이 견해는 근대 사회계약론(홉스, 루소)의 선구이자 "
                "롤스의 공정으로서의 정의(justice as fairness) 개념과 연결된다."
            ),
            "argument": (
                "(1) 정의는 자연에 내재한 어떤 특성이 아니라 인간들 사이의 합의에서 생겨난다. "
                "(2) 이 합의의 내용은 '서로 해치지도 해를 입지도 않겠다'는 상호 불해 원칙이다. "
                "(3) 합의에 참여하지 않은 존재(동물, 합의 없는 먼 나라 사람 등)와는 정의 관계가 성립하지 않는다. "
                "(4) 정의로운 행동을 하는 이유는 의무나 자연적 덕 때문이 아니라, "
                "계약을 어기면 처벌·불안·보복의 공포를 낳아 아타락시아를 해치기 때문이다. "
                "(5) 따라서 정의의 근거는 사회적 효용과 개인의 장기적 쾌락에 있다."
            ),
            "counterpoint": (
                "플라톤은 '국가'(Politeia, 기원전 380경) 2권에서 글라우콘의 정의 계약론(트라시마코스 변형)을 "
                "제시한 후 소크라테스를 통해 이를 반박했다: 정의는 단순한 협약이 아니라 "
                "영혼 안의 각 부분이 제 역할을 다하는 조화의 상태이며, 정의로운 삶은 그 자체로 행복하다. "
                "칸트는 '도덕형이상학 정초'(Grundlegung zur Metaphysik der Sitten, 1785)에서 "
                "도덕은 결과나 계약이 아닌 의무(Pflicht)와 정언명령에 근거해야 하므로, "
                "에피쿠로스의 공리적 정의론은 도덕의 진정한 근거가 될 수 없다고 비판했다."
            ),
            "context": (
                "에피쿠로스의 계약적 정의론은 근대 홉스의 '리바이어던'(Leviathan, 1651)에서 "
                "자연 상태와 사회계약 개념으로 발전하며, "
                "롤스의 '정의론'(A Theory of Justice, 1971)에서 '공정으로서의 정의'로 이어지는 "
                "사회계약론 전통의 중요한 원형이다."
            ),
            "category": "사회철학·정의론",
            "difficulty": "심화",
            "verified": False
        },
        # CLAIM-008: 클리나멘과 자유의지 (선택적 주제)
        {
            "id": "epicurus-claim-008",
            "thinker_id": "epicurus",
            "work_id": "lucretius-de-rerum-natura",
            "source_detail": "De Rerum Natura, Book II, 216-293 (Lucretius)",
            "claim": (
                "원자들은 허공을 낙하할 때 예측 불가능하게 약간씩 경로에서 이탈한다(클리나멘, clinamen). "
                "이 이탈이 결정론적 운명을 깨뜨리고 인간의 자유의지 및 행위 주체성을 가능하게 한다."
            ),
            "original_text": (
                "Quod nisi declinare solerent, omnia deorsum, "
                "imbris uti guttae, caderent per inane profundum, "
                "nec foret offensus natus nec plaga creata principiis: "
                "ita nihil umquam natura creasset. "
                "(Unless the atoms were in the habit of swerving, everything would fall downwards "
                "through the deep void like raindrops, no collision between primary particles would be "
                "born and no blow would be created: thus nature would never have created anything. "
                "De Rerum Natura II, 221-225)"
            ),
            "explanation": (
                "데모크리토스의 원자론은 엄격한 결정론을 함의했다: 모든 것이 원자의 운동 법칙에 따라 정해진다면 "
                "자유의지는 환상이다. 에피쿠로스는 이 문제를 해결하기 위해 클리나멘(clinamen, 빗나감)을 도입했다. "
                "원자는 예측할 수 없는 미세한 이탈을 하는데, 이것이 결정론적 인과사슬을 끊고 "
                "새로운 조합을 가능하게 한다. "
                "이 개념은 루크레티우스에 의해 전해지며, 에피쿠로스 본인의 저작에 직접 나오지는 않는다. "
                "현대 물리학의 양자 불확정성과 유사한 직관을 담고 있어 주목받는다."
            ),
            "argument": (
                "(1) 원자론에 따르면 모든 것은 원자의 운동으로 결정된다(데모크리토스의 결정론). "
                "(2) 그러나 결정론이 참이라면 인간의 자유의지와 도덕적 책임은 불가능하다. "
                "(3) 실제로 우리는 선택을 경험하며, 이 경험은 무시할 수 없다. "
                "(4) 원자들이 완전히 예측 가능한 경로를 따른다면 세계는 완전한 결정론적 체계다. "
                "(5) 원자의 클리나멘(미세한 무작위 이탈)은 이 결정론적 사슬을 깨뜨린다. "
                "(6) 따라서 클리나멘은 결정론에서 벗어나 자유의지의 물리적 기초를 제공한다."
            ),
            "counterpoint": (
                "스토아 학파의 크리시포스(Chrysippus)는 (키케로 '운명에 관하여' De Fato를 통해 전해짐) "
                "자유의지와 결정론은 양립 가능하다(compatibilism)고 주장했다. "
                "우리의 행위는 인과적으로 결정되어 있지만, 그 인과적 원인이 우리 '자신의 성품'에서 비롯된다면 "
                "그 행위는 자유롭다. 무작위적 이탈(클리나멘)은 자유의지의 근거가 아니라 "
                "단순한 무질서일 뿐이라고 비판했다. "
                "칸트는 '순수이성비판'(1781) 3번째 이율배반에서 자유와 자연인과율의 갈등을 다루며, "
                "자유는 경험적 세계의 인과율을 깨는 것이 아니라 예지계(intelligible world)에서의 "
                "이성의 자율성이라고 하여 에피쿠로스의 물리적 해법과 완전히 다른 접근을 취했다."
            ),
            "context": (
                "클리나멘 개념이 에피쿠로스 원전에 명시적으로 나타나지 않는다는 점이 학자들의 논쟁거리다. "
                "루크레티우스가 창작했거나 구술 전통을 기록한 것일 수 있다. "
                "그러나 에피쿠로스가 결정론을 거부하고 자유의지를 옹호했다는 점은 "
                "그의 윤리학(도덕적 책임 전제)에서 분명히 나타난다."
            ),
            "category": "형이상학·자유의지",
            "difficulty": "심화",
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """에피쿠로스 키워드 데이터 입력."""
    keywords = [
        {
            "id": "epicurus-kw-001",
            "thinker_id": "epicurus",
            "term": "아타락시아 (Ataraxia)",
            "term_original": "ἀταραξία",
            "definition": (
                "마음의 평정 또는 동요 없는 상태. 에피쿠로스 윤리학에서 최고 쾌락의 정신적 차원. "
                "공포, 불안, 욕망의 혼란이 없는 고요한 마음 상태로, "
                "올바른 철학적 이해(신에 대한 공포 제거, 죽음 공포 극복, 욕구 절제)를 통해 달성된다."
            ),
            "related_claims": ["epicurus-claim-001", "epicurus-claim-002"],
            "source": "Letter to Menoeceus; Principal Doctrines"
        },
        {
            "id": "epicurus-kw-002",
            "thinker_id": "epicurus",
            "term": "아포니아 (Aponia)",
            "term_original": "ἀπονία",
            "definition": (
                "육체적 고통의 부재. 에피쿠로스 윤리학에서 최고 쾌락의 신체적 차원. "
                "아타락시아(정신적 평정)와 함께 에피쿠로스가 목표로 한 완전한 쾌락 상태를 구성한다. "
                "이 두 상태가 함께 실현될 때 에피쿠로스가 말하는 진정한 행복(εὐδαιμονία)이 달성된다."
            ),
            "related_claims": ["epicurus-claim-001", "epicurus-claim-002"],
            "source": "Letter to Menoeceus"
        },
        {
            "id": "epicurus-kw-003",
            "thinker_id": "epicurus",
            "term": "헤도네 (Hedone)",
            "term_original": "ἡδονή",
            "definition": (
                "쾌락. 에피쿠로스 윤리학에서 최고선(τέλος, telos)이자 삶의 시작과 끝. "
                "에피쿠로스는 쾌락을 정적 쾌락(katastematic: 아타락시아+아포니아)과 "
                "동적 쾌락(kinetic: 감각적 자극)으로 구분하며, 정적 쾌락을 더 높게 평가한다."
            ),
            "related_claims": ["epicurus-claim-001", "epicurus-claim-002"],
            "source": "Letter to Menoeceus, 128-129"
        },
        {
            "id": "epicurus-kw-004",
            "thinker_id": "epicurus",
            "term": "클리나멘 (Clinamen)",
            "term_original": "clinamen (라틴어); παρέγκλισις (그리스어 파렝클리시스)",
            "definition": (
                "원자의 무작위적 이탈 또는 빗나감. "
                "에피쿠로스 자연철학에서 결정론을 깨는 기제로, 루크레티우스의 '사물의 본성에 관하여'에서 전해진다. "
                "원자들이 허공 낙하 중 예측 불가능하게 경로에서 약간 벗어나는 현상으로, "
                "이것이 원자들의 충돌과 조합을 가능하게 하고 인간의 자유의지를 설명한다."
            ),
            "related_claims": ["epicurus-claim-008"],
            "source": "De Rerum Natura, Book II (Lucretius)"
        },
        {
            "id": "epicurus-kw-005",
            "thinker_id": "epicurus",
            "term": "정원 (The Garden)",
            "term_original": "κῆπος (Kepos)",
            "definition": (
                "기원전 307년경 에피쿠로스가 아테네에 세운 철학 공동체. "
                "플라톤의 아카데미아나 아리스토텔레스의 뤼케이온과 달리 "
                "여성, 노예, 이방인을 포함하는 포용적 공동체였다. "
                "에피쿠로스 철학의 실천 장소로, 우정과 공동체 생활을 통한 아타락시아 실현의 모델이다."
            ),
            "related_claims": ["epicurus-claim-006"],
            "source": "Diogenes Laertius, Lives of Eminent Philosophers X"
        },
        {
            "id": "epicurus-kw-006",
            "thinker_id": "epicurus",
            "term": "주요 학설 (Kyriai Doxai)",
            "term_original": "Κύριαι Δόξαι",
            "definition": (
                "에피쿠로스 철학의 핵심 명제 40개를 요약한 문헌. "
                "신, 죽음, 쾌락, 욕구, 우정, 정의를 간결하게 정의하는 명제들로 구성된다. "
                "에피쿠로스주의 교육과 암기의 핵심 텍스트로 사용되었으며, "
                "KD 1(신들의 복됨), KD 3(쾌락의 한계), KD 27(우정), KD 31~38(정의)이 특히 중요하다."
            ),
            "related_claims": ["epicurus-claim-005", "epicurus-claim-006", "epicurus-claim-007"],
            "source": "Principal Doctrines (Kyriai Doxai)"
        },
        {
            "id": "epicurus-kw-007",
            "thinker_id": "epicurus",
            "term": "상호 불해 (Mutual Non-harm)",
            "term_original": "τὸ μὴ βλάπτειν ἢ βλάπτεσθαι",
            "definition": (
                "에피쿠로스 정의론의 핵심 개념. 정의는 자연적 덕이 아니라 "
                "서로 해치지 않고 해침을 받지 않겠다는 약속·계약(συνθήκη)이다. "
                "이 계약은 시간과 장소에 따라 내용이 달라질 수 있으며, "
                "계약 당사자들 사이에서만 정의 관계가 성립한다. "
                "근대 사회계약론의 선구적 개념이다."
            ),
            "related_claims": ["epicurus-claim-007"],
            "source": "Principal Doctrines KD 31-38"
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """에피쿠로스 관계 데이터 입력."""
    relations = [
        {
            "id": "relation-democritus-epicurus",
            "from_thinker": "democritus",
            "to_thinker": "epicurus",
            "type": "influenced",
            "description": (
                "데모크리토스(Democritus, 기원전 460~370경)의 원자론은 에피쿠로스 자연철학의 직접적 기반이다. "
                "에피쿠로스는 원자와 허공(void)으로 구성된 우주론을 계승하되, "
                "데모크리토스의 엄격한 결정론을 클리나멘 개념으로 수정하고, "
                "원자론을 윤리학적 목적(공포 극복, 행복 추구)에 종속시켰다. "
                "에피쿠로스는 데모크리토스를 존경했으나 직접 사사하지는 않았다."
            ),
            "strength": "강함",
            "period": "기원전 4~3세기"
        },
        {
            "id": "relation-epicurus-lucretius",
            "from_thinker": "epicurus",
            "to_thinker": "lucretius",
            "type": "influenced",
            "description": (
                "루크레티우스(Titus Lucretius Carus, 기원전 99~55경)는 에피쿠로스주의의 가장 충실한 로마 전달자다. "
                "'사물의 본성에 관하여(De Rerum Natura)'는 에피쿠로스 자연철학과 윤리학을 "
                "6권의 장시로 상세히 서술하며, 에피쿠로스 본인의 저작이 대부분 소실된 상황에서 "
                "에피쿠로스주의 재구성의 핵심 자료다. "
                "클리나멘 개념도 루크레티우스를 통해 전해진다."
            ),
            "strength": "강함",
            "period": "기원전 1세기"
        },
        {
            "id": "relation-epicurus-mill",
            "from_thinker": "epicurus",
            "to_thinker": "mill",
            "type": "influenced",
            "description": (
                "에피쿠로스의 쾌락주의는 근대 공리주의, 특히 밀(J.S. Mill)에게 중요한 영향을 미쳤다. "
                "밀은 '공리주의'(Utilitarianism, 1863) 2장에서 에피쿠로스를 명시적으로 언급하며 "
                "쾌락주의 공리주의의 선구자로 평가했다. "
                "그러나 밀은 에피쿠로스가 쾌락의 질적 차이(정신적 쾌락 > 육체적 쾌락)를 인정했음에도 "
                "이를 충분히 이론화하지 않았다고 보고, '고급 쾌락'과 '저급 쾌락'의 구분을 추가했다."
            ),
            "strength": "보통",
            "period": "19세기"
        },
        {
            "id": "relation-epicurus-bentham",
            "from_thinker": "epicurus",
            "to_thinker": "bentham",
            "type": "influenced",
            "description": (
                "에피쿠로스의 쾌락주의는 벤담(Jeremy Bentham)의 공리주의에도 영향을 주었다. "
                "벤담은 '도덕 및 입법의 원리 서론'(1789)에서 쾌락과 고통이 인간 행위의 지배자라는 "
                "쾌락주의적 심리학을 출발점으로 삼는데, 이는 에피쿠로스 전통과 연속선상에 있다. "
                "다만 벤담은 에피쿠로스와 달리 쾌락의 양적 계산(felicific calculus)을 중시하고 "
                "사회적·정치적 차원에서 쾌락 극대화를 추구한다."
            ),
            "strength": "보통",
            "period": "18~19세기"
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
    r = client.get(index=INDEX_THINKERS, id="epicurus")
    print(f"[thinker] epicurus: name={r['_source']['name_en']}, era={r['_source']['era']}")

    # works 확인
    from elasticsearch import helpers
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "epicurus"}})
    print(f"[works] epicurus 저서 수: {works_count['count']}")
    works_result = client.search(
        index=INDEX_WORKS,
        query={"term": {"thinker_id": "epicurus"}},
        _source=["id", "title_original", "year"]
    )
    for hit in works_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['title_original']} ({s['year']})")

    # claims 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "epicurus"}})
    print(f"[claims] epicurus 주장 수: {claims_count['count']}")
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "epicurus"}},
        size=10,
        _source=["id", "claim", "argument", "counterpoint", "verified"]
    )
    missing_fields = []
    for hit in claims_result['hits']['hits']:
        s = hit['_source']
        has_arg = bool(s.get('argument'))
        has_cp = bool(s.get('counterpoint'))
        print(f"  - {s['id']}: argument={has_arg}, counterpoint={has_cp}, verified={s.get('verified')}")
        if not has_arg or not has_cp:
            missing_fields.append(s['id'])

    if missing_fields:
        print(f"[경고] argument/counterpoint 누락: {missing_fields}")
    else:
        print("[OK] 모든 claim에 argument+counterpoint 존재")

    # keywords 확인
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "epicurus"}})
    print(f"[keywords] epicurus 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_count_from = client.count(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "epicurus"}},
            {"term": {"to_thinker": "epicurus"}}
        ]}}
    )
    print(f"[relations] epicurus 관련 관계 수: {rel_count_from['count']}")
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "epicurus"}},
            {"term": {"to_thinker": "epicurus"}}
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
        print("=== 에피쿠로스(Epicurus) 데이터 입력 시작 ===\n")

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
