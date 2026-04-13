"""세네카(Seneca) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS
)


def insert_thinker(client):
    """세네카 사상가 데이터 입력."""
    doc = {
        "id": "seneca",
        "name": "세네카",
        "name_en": "Seneca (Lucius Annaeus Seneca)",
        "field": "western_ethics",
        "era": "고대 로마·후기 스토아",
        "birth_year": -4,
        "death_year": 65,
        "background": (
            "히스파니아 코르두바(현 스페인 코르도바)에서 부유한 기사 계층 가문에 태어났다. "
            "로마에서 수사학과 철학을 교육받았으며, "
            "특히 스토아 철학자 아탈로스(Attalus)와 소티온(Sotion)에게 사사했다. "
            "원로원 의원으로 정치에 참여했으나, 칼리굴라 치세에서는 죽을 뻔했고, "
            "클라우디우스 치세(41~49년)에는 코르시카 섬에 8년간 유배되었다. "
            "유배에서 복귀 후 아그리피나의 요청으로 어린 네로의 가정교사이자 조언자가 되었다. "
            "네로 즉위 초기(54~62년)에는 사실상 제국 운영을 주도하며 '네로의 5년(Quinquennium Neronis)'이라 "
            "불리는 선정의 시기를 이끌었다. "
            "그러나 점차 네로와 갈등하여 은퇴했고, "
            "65년 피소의 음모(Pisonian conspiracy)에 연루되었다는 혐의로 네로에게 자결을 명받아 "
            "스토아적 평정 속에 자결했다. "
            "세네카는 고대 세계에서 가장 부유한 인물 중 하나였으며, "
            "부와 권력 한가운데서 검소와 덕을 설파한 것이 위선이라는 비판을 받기도 했다."
        ),
        "core_philosophy": (
            "세네카 철학의 핵심은 철학의 치료적 기능이다. "
            "철학은 영혼의 질병(격정, 분노, 두려움, 슬픔)을 치료하는 의술이며, "
            "이론적 탐구보다 실천적 적용이 중요하다. "
            "덕(virtus)만이 유일한 선이며, 덕은 이성에 따른 삶에서 실현된다. "
            "시간의 유한성을 인식하고 매 순간을 의미 있게 사는 것이 지혜이며, "
            "죽음에 대한 명상(meditatio mortis)은 삶을 더 잘 살게 하는 수련이다. "
            "분노는 가장 위험한 격정이며, 이성적 판단으로 극복해야 한다. "
            "세네카는 스토아 원칙을 고수하면서도 에피쿠로스 등 다른 학파의 통찰을 유연하게 수용하여 "
            "절충적·실천적 스토아주의를 발전시켰다."
        ),
        "philosophical_journey": (
            "초기(~41년): 로마에서 스토아 철학자 아탈로스, 소티온, 파피리우스 파비아누스에게 사사. "
            "초기 저작에서 이미 실천적 윤리학에 관심을 보였다. "
            "유배기(41~49년): 코르시카 유배 중 '위안의 글'(Consolationes)을 집필하며 "
            "스토아적 위로 문학의 전통을 발전시켰다. 유배의 고통 속에서 "
            "운명에 대한 스토아적 수용과 내면의 자유를 실천적으로 시험했다. "
            "정치 참여기(49~62년): 네로의 가정교사·조언자로서 "
            "'관용에 대하여(De Clementia)' 등을 통해 스토아 정치철학을 실천에 옮겼다. "
            "이 시기 '분노에 대하여(De Ira)', '행복한 삶에 대하여(De Vita Beata)' 등 "
            "주요 도덕 에세이를 집필했다. "
            "은퇴기(62~65년): 네로와의 갈등 후 공적 생활에서 물러나 "
            "'루킬리우스에게 보내는 도덕 서한집(Epistulae Morales)'과 "
            "'자연 탐구(Naturales Quaestiones)'를 집필하며 "
            "가장 성숙한 철학적 성찰을 남겼다. "
            "65년 스토아적 평정 속에 자결하여, 소크라테스의 죽음과 비교되는 철학자의 죽음을 보여주었다."
        ),
        "keywords": [
            "철학의 치료적 기능",
            "시간의 유한성",
            "죽음의 명상(meditatio mortis)",
            "분노 극복",
            "덕(virtus)",
            "도덕 서한",
            "운명에 대한 동의(amor fati)"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="seneca", document=doc)
    print(f"[thinker] seneca: {result['result']}")
    return result


def insert_works(client):
    """세네카 저서 데이터 입력."""
    works = [
        {
            "id": "seneca-epistulae-morales",
            "thinker_id": "seneca",
            "title": "도덕 서한집 (루킬리우스에게 보내는 편지)",
            "title_original": "Epistulae Morales ad Lucilium (Moral Letters to Lucilius)",
            "year": 64,
            "significance": (
                "세네카의 가장 중요한 철학 저작. 친구 루킬리우스에게 보내는 편지 형식으로, "
                "총 124통이 전하며 20권으로 구성된다. "
                "스토아 윤리학의 핵심 주제들—덕, 시간, 죽음, 우정, 분노, 부, 빈곤—을 "
                "일상적이고 접근 가능한 언어로 다룬다. "
                "편지 형식 덕분에 추상적 원칙이 구체적 상황에 적용되어 "
                "스토아 철학의 실천적 가이드로 평가된다. "
                "에피쿠로스를 비롯한 다른 학파의 격언도 자유롭게 인용하는 절충적 성격이 특징이다."
            ),
            "key_concepts": [
                "덕의 실천", "시간의 올바른 사용", "죽음에 대한 명상",
                "우정의 가치", "부와 빈곤", "분노 극복", "내면의 평정"
            ]
        },
        {
            "id": "seneca-de-ira",
            "thinker_id": "seneca",
            "title": "분노에 대하여",
            "title_original": "De Ira (On Anger)",
            "year": 41,
            "significance": (
                "세네카의 가장 방대한 도덕 에세이 중 하나로, 3권으로 구성된다. "
                "분노의 본성, 원인, 치료법을 체계적으로 다룬 최초의 서양 철학 문헌 중 하나다. "
                "분노는 '짧은 광기(brevis furor)'이며, 이성에 반하는 격정이므로 "
                "어떤 상황에서도 정당화될 수 없다고 주장한다. "
                "칼리굴라의 폭정을 목격한 후 집필된 것으로 추정되며, "
                "권력자의 분노가 얼마나 파괴적인지에 대한 정치적 함의도 담고 있다."
            ),
            "key_concepts": [
                "분노의 메커니즘", "인지적 분노 이론", "분노의 치료법",
                "관용(clementia)", "사전 명상(praemeditatio)"
            ]
        },
        {
            "id": "seneca-de-brevitate-vitae",
            "thinker_id": "seneca",
            "title": "인생의 짧음에 대하여",
            "title_original": "De Brevitate Vitae (On the Shortness of Life)",
            "year": 49,
            "significance": (
                "장인 파울리누스(Paulinus)에게 헌정된 에세이로, "
                "인생이 짧은 것이 아니라 우리가 시간을 낭비하기 때문에 짧다고 느낀다는 핵심 논증을 전개한다. "
                "시간의 올바른 사용이 행복의 핵심이라는 세네카 윤리학의 특징적 주제를 집약적으로 담고 있다. "
                "세네카의 가장 많이 읽히는 저작 중 하나이며, "
                "시간 관리와 삶의 의미에 대한 고전으로 현대에도 널리 인용된다."
            ),
            "key_concepts": [
                "시간의 유한성", "시간 낭비 비판", "진정한 여가(otium)",
                "철학적 삶", "현재에 집중"
            ]
        },
        {
            "id": "seneca-de-clementia",
            "thinker_id": "seneca",
            "title": "관용에 대하여",
            "title_original": "De Clementia (On Clemency)",
            "year": 56,
            "significance": (
                "젊은 황제 네로에게 헌정된 정치철학 저작으로, "
                "스토아적 이상 군주론을 제시한다. "
                "관용(clementia)은 단순한 관대함이 아니라 "
                "이성적 판단에 기반한 형벌의 절제이며, 현명한 통치의 핵심 덕이라 주장한다. "
                "잔인한 처벌은 통치자 자신에게도 해롭고 국가를 불안정하게 만든다. "
                "세네카의 정치 참여 시기를 대표하는 저작으로, "
                "스토아 철학의 정치적 적용을 보여준다."
            ),
            "key_concepts": [
                "관용(clementia)", "스토아적 군주론", "형벌의 절제",
                "통치자의 덕", "이성적 통치"
            ]
        },
        {
            "id": "seneca-de-vita-beata",
            "thinker_id": "seneca",
            "title": "행복한 삶에 대하여",
            "title_original": "De Vita Beata (On the Happy Life)",
            "year": 58,
            "significance": (
                "형 갈리오(Gallio)에게 헌정된 에세이로, "
                "행복은 오직 덕(virtus)에 의해서만 달성되며 쾌락이 아니라고 주장한다. "
                "에피쿠로스의 쾌락주의를 비판하면서도, "
                "부가 그 자체로 악이 아니며 현명하게 사용하면 덕에 봉사할 수 있다고 변호한다. "
                "세네카 자신의 막대한 부에 대한 비판에 대응하는 자기변호적 성격도 있다."
            ),
            "key_concepts": [
                "행복과 덕의 관계", "쾌락주의 비판", "부의 올바른 사용",
                "자연에 따른 삶", "철학자의 일관성"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """세네카 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 인생은 짧지 않다 — 시간의 올바른 사용
        {
            "id": "seneca-claim-001",
            "thinker_id": "seneca",
            "work_id": "seneca-de-brevitate-vitae",
            "source_detail": "De Brevitate Vitae I.1-3; II.1",
            "claim": (
                "인생은 짧은 것이 아니라, 우리가 인생의 대부분을 낭비하기 때문에 짧다고 느끼는 것이다. "
                "충분히 긴 인생을 받았지만, 우리는 그것을 사소한 일, 게으름, 야망, 사교 등에 허비한다. "
                "시간은 우리가 가진 유일한 진정한 재산이며, 이를 올바르게 사용하는 자만이 행복하다."
            ),
            "original_text": (
                "Non accepimus brevem vitam, sed fecimus; "
                "nec inopes eius sed prodigi sumus. "
                "(We have not been given a short life, but we have made it short; "
                "we are not poorly supplied but wasteful of it. "
                "De Brevitate Vitae I.3)"
            ),
            "original_text_ko": (
                "우리는 짧은 인생을 받은 것이 아니라, 인생을 짧게 만든 것이다. "
                "우리에게 인생이 부족한 것이 아니라, 우리가 인생을 낭비하는 것이다."
            ),
            "explanation": (
                "세네카는 인생의 짧음에 대한 일반적 불만을 뒤집는다. "
                "문제는 시간의 양이 아니라 사용 방식이다. "
                "대부분의 사람들은 바쁜 활동(occupatio)에 몰두하지만 "
                "정작 자기 자신에게 시간을 쓰지 않는다. "
                "정치적 야망, 사교, 음주, 쾌락 추구에 시간을 빼앗기고, "
                "죽음이 다가올 때야 비로소 살아보지 못했다고 후회한다. "
                "오직 철학에 몰두하는 자만이 진정으로 살아 있으며(vivere), "
                "나머지는 단지 존재할 뿐(esse)이다."
            ),
            "argument": (
                "(1) 자연은 인간에게 충분한 수명을 부여했다. "
                "(2) 그러나 대부분의 사람은 시간을 사소한 활동에 낭비한다. "
                "(3) 시간은 되돌릴 수 없는 유일한 자원이며, 돈이나 재산보다 귀중하다. "
                "(4) 사람들은 돈은 아끼면서 시간은 아끼지 않는 모순적 행동을 한다. "
                "(5) 오직 철학적 삶(자기 성찰, 덕의 추구)에 시간을 쓰는 자만이 진정으로 산다. "
                "(6) 따라서 인생이 짧다고 불평하기 전에 시간 사용 방식을 검토해야 한다."
            ),
            "counterpoint": (
                "에피쿠로스는 '메노이케우스에게 보내는 편지'에서 "
                "긴 삶보다 즐거운 삶이 중요하다고 하여, 시간의 양보다 질을 강조하는 점에서는 "
                "세네카와 유사하지만, 그 '질'을 쾌락(아타락시아)에서 찾는다. "
                "아리스토텔레스는 '니코마코스 윤리학'에서 행복에 '완전한 생애(bios teleios)'가 필요하다고 보아, "
                "삶의 길이도 중요하다고 간주했다. "
                "현대 실존주의(하이데거)는 죽음을 향한 존재(Sein-zum-Tode)로서 "
                "유한성의 인식이 진정한 실존의 조건이라 보아, 세네카와 구조적으로 유사하다."
            ),
            "context": (
                "'인생의 짧음에 대하여'는 세네카의 가장 대중적인 저작으로, "
                "현대 자기계발 서적에서도 빈번히 인용된다. "
                "세네카 자신이 바쁜 정치 생활에서 시간에 쫓기던 경험이 반영되어 있다."
            ),
            "category": "윤리학",
            "difficulty": "기본",
            "verified": False
        },
        # CLAIM-002: 분노는 짧은 광기다
        {
            "id": "seneca-claim-002",
            "thinker_id": "seneca",
            "work_id": "seneca-de-ira",
            "source_detail": "De Ira I.1.1-2; I.2.3; II.3-4",
            "claim": (
                "분노는 '짧은 광기(brevis furor)'이며, 이성에 완전히 반하는 격정이다. "
                "분노는 어떤 상황에서도 정당화될 수 없으며, "
                "정의를 위해 분노가 필요하다는 주장은 잘못이다. "
                "분노는 시작되면 통제할 수 없으므로, 시작 자체를 막아야 한다."
            ),
            "original_text": (
                "Ira, inquit Theophrastus, brevem insaniam esse. "
                "(...) Nihil ergo magis e re publica est quam iram exstingui. "
                "(Anger, says Theophrastus, is a brief madness. "
                "(...) Nothing is more in the public interest than the extinction of anger. "
                "De Ira I.1.2; I.2.1)"
            ),
            "original_text_ko": (
                "테오프라스토스가 말하길, 분노는 짧은 광기라고 했다. "
                "(...) 분노를 소멸시키는 것보다 공익에 더 부합하는 것은 없다."
            ),
            "explanation": (
                "세네카는 아리스토텔레스의 '적절한 분노는 덕이다'라는 입장에 정면으로 반대한다. "
                "분노가 시작되면 이성의 통제를 벗어나 파괴적이 되기 때문에, "
                "'적절한 분노'란 존재하지 않는다. "
                "분노는 단계적으로 진행된다: (1) 전-감정(involuntary initial reaction)은 "
                "통제 불가능하지만 격정은 아니다. (2) 이성이 이 전-감정에 동의하면 분노가 시작된다. "
                "(3) 분노가 시작되면 이성을 압도한다. "
                "따라서 2단계에서 동의를 거부하는 것이 핵심이다."
            ),
            "argument": (
                "(1) 분노는 이성의 통제를 벗어나는 격정(affectus)이다. "
                "(2) 분노가 시작되면 정도를 조절하는 것이 불가능하다—마치 절벽에서 뛰어내리면 "
                "중간에 멈출 수 없는 것과 같다. "
                "(3) 따라서 '적절한 분노'란 형용모순이다. "
                "(4) 정의를 집행하는 데 분노가 필요하다는 주장은 틀렸다—"
                "판사는 분노 없이 냉정하게 판결할 때 더 정의롭다. "
                "(5) 전-감정(involuntary first movement)은 자연적이며 통제할 수 없지만, "
                "이에 이성적 동의를 부여하는 것은 우리에게 달려 있다. "
                "(6) 동의를 거부함으로써 분노의 시작 자체를 방지해야 한다."
            ),
            "counterpoint": (
                "아리스토텔레스는 '니코마코스 윤리학' 4권에서 "
                "'적절한 시기에 적절한 대상에 대해 적절한 정도로 분노하는 것은 덕(πραΰτης, 온화함)이며, "
                "부정의에 대해 분노하지 않는 것은 비겁함이다'고 주장했다. "
                "이 관점에서 세네카의 '분노 완전 제거론'은 비현실적이고 "
                "부정의에 대한 적절한 반응을 불가능하게 한다. "
                "흄은 감정이 도덕 판단의 근거라 하여, "
                "이성만으로 도덕적 행위가 가능하다는 스토아적 전제에 도전했다."
            ),
            "context": (
                "세네카가 칼리굴라의 광적인 분노와 폭정을 직접 목격한 경험이 이 저작의 배경이다. "
                "권력자의 통제되지 않는 분노가 얼마나 파괴적인지를 체험적으로 알았던 것이다. "
                "세네카의 분노론은 현대 분노 관리(anger management)와 "
                "인지행동치료(CBT)의 철학적 선구로 평가된다."
            ),
            "category": "윤리학·심리학",
            "difficulty": "기본",
            "verified": False
        },
        # CLAIM-003: 죽음의 명상 (meditatio mortis)
        {
            "id": "seneca-claim-003",
            "thinker_id": "seneca",
            "work_id": "seneca-epistulae-morales",
            "source_detail": "Epistulae Morales 4.5; 12; 26; 77; De Brevitate Vitae 7",
            "claim": (
                "매일 죽음을 명상하라(meditatio mortis). "
                "죽음을 두려워하는 자는 제대로 살지 못하며, "
                "죽음을 받아들인 자만이 진정으로 자유롭다. "
                "죽음은 잃는 것이 아니라 돌려주는 것이며, "
                "잘 살았다면 충분히 살았다."
            ),
            "original_text": (
                "Quotidie morimur; quotidie enim demitur aliqua pars vitae. "
                "(We die every day; for every day a part of our life is taken from us. "
                "Epistulae Morales 24.20)"
            ),
            "original_text_ko": (
                "우리는 매일 죽는다. 매일 우리 삶의 일부가 빼앗기기 때문이다."
            ),
            "explanation": (
                "세네카에게 죽음 명상(meditatio mortis)은 단순한 비관이 아니라 "
                "삶을 더 잘 살게 하는 능동적 수련이다. "
                "죽음을 끊임없이 상기하면: (1) 시간의 가치를 깨달아 낭비를 줄이고, "
                "(2) 사소한 것에 대한 집착이 줄어들며, "
                "(3) 미래에 대한 두려움 대신 현재에 집중하게 되고, "
                "(4) 운명에 대한 수용력이 커진다. "
                "세네카는 '매일 죽는다'고 말한다—매일 삶의 일부가 사라지므로 "
                "죽음은 먼 미래의 사건이 아니라 지금 진행 중인 과정이다."
            ),
            "argument": (
                "(1) 죽음은 확실하지만 그 시점은 불확실하다. "
                "(2) 죽음을 모르는 체하면 시간을 낭비하고 사소한 것에 집착하게 된다. "
                "(3) 죽음을 매일 명상하면 삶의 유한성을 인식하여 시간의 가치를 깨닫는다. "
                "(4) 유한성의 인식은 불필요한 두려움과 집착을 줄여준다. "
                "(5) 죽음에 준비된 자는 운명의 어떤 변화에도 흔들리지 않는다. "
                "(6) 따라서 죽음 명상은 삶의 질을 높이는 가장 강력한 철학적 수련이다."
            ),
            "counterpoint": (
                "에피쿠로스는 '죽음은 우리에게 아무것도 아니다'라며 "
                "죽음에 대해 생각하지 않는 것이 해법이라 한 반면, "
                "세네카는 오히려 적극적으로 죽음을 명상해야 한다고 주장한다. "
                "현대 실존주의(하이데거)는 '죽음을 향한 존재(Sein-zum-Tode)'로서 "
                "유한성의 인식이 진정한 실존의 조건이라 하여 세네카와 구조적으로 유사하다. "
                "그러나 세네카의 죽음 명상이 '삶의 의미'보다 '마음의 평정'에 초점을 두는 점에서 "
                "실존주의와 차이가 있다."
            ),
            "context": (
                "세네카 자신이 65년 네로에게 자결을 명받아 스토아적 평정 속에 죽음을 맞이했다. "
                "평생에 걸친 죽음 명상이 실제 죽음의 순간에 체현된 것이다. "
                "타키투스의 '연대기(Annales)' 15.62-64에 세네카의 죽음 장면이 상세히 기록되어 있으며, "
                "소크라테스의 죽음과 의식적으로 비교된다."
            ),
            "category": "윤리학",
            "difficulty": "기본",
            "verified": False
        },
        # CLAIM-004: 사전 명상 (praemeditatio malorum)
        {
            "id": "seneca-claim-004",
            "thinker_id": "seneca",
            "work_id": "seneca-epistulae-morales",
            "source_detail": "Epistulae Morales 76.33-34; 91; De Tranquillitate Animi 11.6-8",
            "claim": (
                "닥칠 수 있는 불행을 미리 상상하여 마음의 준비를 해두어야 한다(praemeditatio malorum). "
                "미리 예상한 일은 충격이 줄어들고, 예상하지 못한 일은 충격이 배가된다. "
                "유배, 빈곤, 질병, 죽음 등을 미리 명상하면 "
                "실제로 닥쳤을 때 평정을 유지할 수 있다."
            ),
            "original_text": (
                "Praemeditatio futurorum malorum levat eorum adventum. "
                "(Premeditating future evils lightens their arrival. "
                "Paraphrase of Epistulae Morales 76.34)"
            ),
            "original_text_ko": (
                "미래의 불행에 대한 사전 명상은 그것이 실제로 닥쳤을 때의 충격을 줄여준다."
            ),
            "explanation": (
                "프라에메디타티오 말로룸(praemeditatio malorum)은 세네카가 발전시킨 "
                "스토아적 정신 수련법이다. "
                "매일 아침 '오늘 무엇이 잘못될 수 있는가?'를 상상하고 "
                "그에 대한 스토아적 대응을 미리 연습한다. "
                "이것은 비관주의가 아니라 심리적 면역(psychological inoculation)이다. "
                "예상하지 못한 불행은 충격이 크지만, 미리 준비한 불행은 "
                "'이미 예상했다'는 인식이 완충제가 된다. "
                "세네카는 이를 병사의 훈련에 비유한다—실전 전에 훈련하는 것이 "
                "전투에서 더 잘 대처하게 해주는 것처럼."
            ),
            "argument": (
                "(1) 예상하지 못한 일은 충격이 크고, 예상한 일은 충격이 줄어든다. "
                "(2) 나쁜 일(유배, 질병, 빈곤, 죽음)은 누구에게나 닥칠 수 있다. "
                "(3) 이것들을 미리 상상하고 스토아적 대응을 연습하면 "
                "실제 사건 시 평정을 유지할 수 있다. "
                "(4) 이것은 비관주의가 아니라 현실주의적 준비(realistic preparation)다. "
                "(5) 미리 명상하면 '이것은 일어날 수 있다고 이미 알고 있었다'는 인식이 "
                "감정적 충격을 완화한다. "
                "(6) 따라서 사전 명상은 운명의 변화에 대한 가장 효과적인 심리적 방어 수단이다."
            ),
            "counterpoint": (
                "에피쿠로스는 미래의 나쁜 일을 미리 걱정하는 것은 "
                "현재의 아타락시아를 해치는 불필요한 고통이라 비판했다. "
                "쾌락주의적 관점에서 고통을 미리 경험하는 것은 고통을 두 배로 늘리는 것이다. "
                "현대 심리학에서는 프라에메디타티오가 '디센시타이제이션(체계적 둔감화)'과 유사하다고 보며 "
                "그 효과를 인정하지만, 과도한 사전 걱정이 불안장애를 악화시킬 수 있다는 점도 지적한다."
            ),
            "context": (
                "세네카 자신이 코르시카 유배(41~49년)를 경험했고, "
                "이후에도 네로 치하에서 언제든 몰락할 수 있었다. "
                "사전 명상은 세네카에게 추상적 수련이 아니라 "
                "실제 위험에 대비하는 생존 기술이었다."
            ),
            "category": "윤리학·심리학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-005: 덕만이 유일한 선이다
        {
            "id": "seneca-claim-005",
            "thinker_id": "seneca",
            "work_id": "seneca-de-vita-beata",
            "source_detail": "De Vita Beata 3-4; 16; Epistulae Morales 74.12-16",
            "claim": (
                "행복한 삶(vita beata)은 오직 덕(virtus)에 의해서만 달성된다. "
                "덕은 그 자체로 충분하며 외적 재화를 필요로 하지 않는다. "
                "부, 건강, 명성은 덕에 방해되지 않을 때 선호할 수 있지만, "
                "이것들 없이도 완전한 행복이 가능하다."
            ),
            "original_text": (
                "Beata est ergo vita conveniens naturae suae. "
                "(The happy life, therefore, is one that is in agreement with its own nature. "
                "De Vita Beata 3.3)"
            ),
            "original_text_ko": (
                "행복한 삶이란 자기 자신의 본성에 일치하는 삶이다."
            ),
            "explanation": (
                "세네카는 스토아의 핵심 테제—덕만이 유일한 선—를 견지하면서도 "
                "부와 물질적 안락에 대해 미묘한 입장을 취한다. "
                "부 자체는 악이 아니며 현명하게 사용하면 덕에 봉사할 수 있다. "
                "그러나 부는 행복의 조건이 아니며, 부 없이도 완전한 행복이 가능하다. "
                "세네카는 자신의 막대한 부에 대한 비판에 대해 "
                "'현자는 부를 선호하지만 의존하지 않는다'고 변호한다. "
                "부를 가진 현자와 빈곤한 현자는 둘 다 행복하지만, "
                "부를 가진 현자는 관대함의 덕을 실천할 더 많은 기회를 가진다."
            ),
            "argument": (
                "(1) 인간의 본성은 이성이며, 이성에 따른 삶이 자연에 따른 삶이다. "
                "(2) 자연에 따른 삶의 완성이 덕(virtus)이며, 덕이 행복의 충분조건이다. "
                "(3) 외적 재화(부, 건강, 명성)는 운에 좌우되며 우리에게 달려 있지 않다. "
                "(4) 행복의 조건을 운에 좌우되는 것에 두면 행복도 불안정해진다. "
                "(5) 따라서 덕만이 안정적이고 자족적인 행복의 기초다. "
                "(6) 외적 재화는 선호할 수 있지만(preferred indifferents) 행복에 필수적이지는 않다."
            ),
            "counterpoint": (
                "세네카의 비판자들은 로마 최고의 부자 중 하나가 "
                "'부는 필요 없다'고 설파하는 것이 위선이라 지적했다. "
                "아리스토텔레스는 행복에 외적 재화가 필요하다고 보아 스토아적 자족론에 반대했다. "
                "에피쿠로스는 행복에 최소한의 물질적 조건(자연적이고 필요한 욕구의 충족)이 "
                "필수적이라 주장했다."
            ),
            "context": (
                "'행복한 삶에 대하여'가 집필된 시기(58년경) 세네카는 네로의 조언자로서 "
                "엄청난 부와 권력을 누리고 있었다. "
                "부에 대한 비판은 당시부터 존재했으며, 세네카 자신도 이를 의식하고 있었다."
            ),
            "category": "윤리학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-006: 운명에 대한 동의 — 운명을 기꺼이 따르라
        {
            "id": "seneca-claim-006",
            "thinker_id": "seneca",
            "work_id": "seneca-epistulae-morales",
            "source_detail": "Epistulae Morales 107.11; De Providentia 5.4-8",
            "claim": (
                "운명이 이끄는 자는 따라가고, 거부하는 자는 끌려간다. "
                "신(섭리)은 선한 사람에게 고난을 보내는 것이 아니라 시련을 통해 강하게 만든다. "
                "고난은 덕을 시험하고 강화하는 기회이며, "
                "운명에 자발적으로 동의하는 것(amor fati)이 스토아적 지혜의 정수다."
            ),
            "original_text": (
                "Ducunt volentem fata, nolentem trahunt. "
                "(Fate leads the willing and drags the unwilling. "
                "Epistulae Morales 107.11, quoting Cleanthes)"
            ),
            "original_text_ko": (
                "운명은 순응하는 자를 이끌고, 거부하는 자를 끌어간다."
            ),
            "explanation": (
                "세네카는 클레안테스의 유명한 격언을 인용하며 스토아적 운명론을 전개한다. "
                "우주는 섭리(프로노이아)에 의해 합리적으로 질서 지어져 있으며, "
                "우리에게 일어나는 모든 일은 이 질서의 일부다. "
                "고난은 벌이 아니라 훈련이다—역도 선수가 무거운 역기를 드는 것은 "
                "벌이 아니라 더 강해지기 위한 훈련인 것처럼. "
                "운명에 저항하면 고통만 가중될 뿐 결과는 바뀌지 않지만, "
                "자발적으로 수용하면 고통은 줄고 내면의 평정을 유지할 수 있다."
            ),
            "argument": (
                "(1) 우주는 이성적 섭리에 의해 지배된다(스토아 물리학 전제). "
                "(2) 우리에게 일어나는 일은 이 섭리의 일부이며, 합리적 이유가 있다. "
                "(3) 고난은 덕을 시험하고 강화하는 기회다—쉬운 삶은 덕을 연마할 기회를 주지 않는다. "
                "(4) 운명에 저항하면 결과는 바뀌지 않고 고통만 가중된다. "
                "(5) 운명에 자발적으로 동의하면 평정과 덕의 실현이 가능하다. "
                "(6) 따라서 '기꺼이 따르는 것'이 지혜이고, '끌려가는 것'은 어리석음이다."
            ),
            "counterpoint": (
                "에피쿠로스는 우주에 섭리가 없으며 원자들의 무작위적 결합이라 주장하여 "
                "운명에 대한 동의 자체가 무의미하다고 보았다. "
                "니체의 '운명에 대한 사랑(amor fati)' 개념은 세네카와 유사하지만, "
                "스토아의 섭리론 없이 삶의 모든 순간을 있는 그대로 긍정하는 것이다. "
                "카뮈는 '시시포스의 신화'(1942)에서 부조리한 운명에 대해 "
                "동의가 아니라 반항이 인간의 존엄이라 주장했다."
            ),
            "context": (
                "세네카가 코르시카 유배(41~49년)에서 이 원칙을 실천적으로 시험했고, "
                "최종적으로 네로의 사형 명령에 대해 스토아적 수용으로 응한 것이 "
                "이 가르침의 체현이다."
            ),
            "category": "형이상학·윤리학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-007: 관용은 통치자의 최고 덕이다
        {
            "id": "seneca-claim-007",
            "thinker_id": "seneca",
            "work_id": "seneca-de-clementia",
            "source_detail": "De Clementia I.1-5; I.11; II.3-7",
            "claim": (
                "관용(clementia)은 통치자의 가장 중요한 덕이며, "
                "단순한 관대함이 아니라 이성적 판단에 기반한 형벌의 절제다. "
                "잔인함은 약함의 표시이며, 관용은 강함의 표시다. "
                "관용은 통치자를 신에 가깝게 만드는 덕이다."
            ),
            "original_text": (
                "Nullum tamen clementia ex omnibus magis quam regem aut principem decet. "
                "(No one is better suited to clemency than a king or prince. "
                "De Clementia I.5.2)"
            ),
            "original_text_ko": (
                "모든 사람 중에서 관용이 가장 잘 어울리는 자는 왕이나 군주다."
            ),
            "explanation": (
                "세네카는 관용을 세 가지 관련 개념과 구분한다: "
                "(1) 관용(clementia)은 형벌을 가할 권한이 있는 자가 이성적으로 절제하는 것. "
                "(2) 연민(misericordia)은 타인의 고통에 대한 감정적 반응으로, 격정(pathos)이므로 덕이 아님. "
                "(3) 용서(venia)는 마땅한 처벌을 면제하는 것으로, 관용과 다름. "
                "관용은 감정이 아니라 이성적 판단이며, 처벌이 필요할 때는 집행하되 "
                "과도하지 않도록 절제하는 것이다. 잔인한 통치는 공포를 낳고 공포는 반란을 낳아 "
                "결국 통치자 자신을 위험에 빠뜨린다."
            ),
            "argument": (
                "(1) 통치자는 시민의 생사여탈권을 가지므로 가장 큰 책임을 진다. "
                "(2) 잔인한 형벌은 공포를 낳고, 공포는 반란과 음모를 촉진한다. "
                "(3) 관용은 신민의 충성과 사랑을 얻어 안정적 통치를 가능하게 한다. "
                "(4) 관용은 감정적 연민이 아니라 이성적 판단이므로 약함이 아니다. "
                "(5) 신들은 인간의 잘못에도 세계를 파괴하지 않으므로, "
                "신을 닮고자 하는 통치자도 관용을 실천해야 한다. "
                "(6) 따라서 관용은 통치자를 신에 가장 가깝게 만드는 최고의 덕이다."
            ),
            "counterpoint": (
                "마키아벨리는 '군주론'(1532) 17장에서 "
                "군주는 사랑받는 것보다 두려움의 대상이 되는 것이 안전하다고 주장했다. "
                "관용은 나약함으로 오해되어 통치를 위험에 빠뜨릴 수 있다. "
                "한비자는 법가(法家) 사상에서 상벌의 엄격한 집행이 "
                "통치의 핵심이라 하여 관용을 경계했다. "
                "역사적으로 네로가 세네카의 가르침에도 불구하고 폭군이 된 것은 "
                "관용의 교육이 제도적 견제 없이는 한계가 있음을 보여준다."
            ),
            "context": (
                "'관용에 대하여'는 네로 즉위 초기(56년경)에 집필되어 "
                "젊은 황제에게 이상적 통치의 모델을 제시하려 했다. "
                "네로의 초기 통치(quinquennium Neronis)가 실제로 관대했던 것은 "
                "세네카의 영향으로 해석된다. 이후 네로가 폭정으로 전환한 것은 "
                "스토아 정치철학의 비극적 한계를 보여준다."
            ),
            "category": "정치철학·윤리학",
            "difficulty": "심화",
            "verified": False
        },
        # CLAIM-008: 자기 자신에게 매일 회계하라
        {
            "id": "seneca-claim-008",
            "thinker_id": "seneca",
            "work_id": "seneca-epistulae-morales",
            "source_detail": "Epistulae Morales 83.2; De Ira III.36",
            "claim": (
                "매일 저녁 하루를 되돌아보며 자기 자신에게 회계해야 한다. "
                "오늘 어떤 나쁜 습관을 치료했는가? 어떤 유혹에 저항했는가? "
                "어떤 점에서 나아졌는가? 이 매일의 자기 검토(examen conscientiae)가 "
                "점진적 도덕 진보의 핵심이다."
            ),
            "original_text": (
                "Facio autem quod Sextii fecerunt: quum consummatus est dies et in cubile me recepi, "
                "totum diem meum scrutor facta ac dicta mea reverbero. "
                "(I do what the Sextii did: when the day is over and I have retired to bed, "
                "I examine my whole day and review my deeds and words. "
                "De Ira III.36.1)"
            ),
            "original_text_ko": (
                "나는 섹스티이가 했던 것을 한다: 하루가 끝나고 잠자리에 들면, "
                "나의 하루 전체를 검토하고 나의 행위와 말을 되짚어본다."
            ),
            "explanation": (
                "세네카는 피타고라스학파와 섹스티우스(Sextius)의 전통에서 가져온 "
                "매일의 자기 검토(examen conscientiae)를 스토아적 수련으로 발전시켰다. "
                "매일 저녁 하루의 행동, 말, 생각을 되돌아보며 "
                "스토아적 원칙에 비추어 평가한다. "
                "이때 자기 자신에게 관대하되 솔직해야 한다—목적은 자기 처벌이 아니라 개선이다. "
                "'오늘 나는 분노를 억제했는가?', '시간을 낭비하지는 않았는가?', "
                "'남에게 정의롭게 대했는가?' 등을 검토한다. "
                "이 실천은 이냐시오 드 로욜라의 '양심 성찰(examen)'에 직접 영향을 주었다."
            ),
            "argument": (
                "(1) 도덕적 진보는 갑작스러운 도약이 아니라 매일의 점진적 개선을 통해 이루어진다. "
                "(2) 매일의 자기 검토 없이는 자신의 결점을 인식하지 못한다. "
                "(3) 결점을 인식하지 못하면 개선도 불가능하다. "
                "(4) 매일 저녁 하루를 되돌아보면 반복되는 패턴(분노, 시간 낭비 등)을 발견할 수 있다. "
                "(5) 패턴을 발견하면 다음 날 의식적으로 교정할 수 있다. "
                "(6) 따라서 매일의 자기 검토는 도덕적 진보의 가장 효과적인 방법이다."
            ),
            "counterpoint": (
                "에피쿠로스는 행복이 욕구의 절제를 통해 비교적 쉽게 달성 가능하다고 보아, "
                "매일의 엄격한 자기 검토가 오히려 불안을 가중시킬 수 있다고 볼 것이다. "
                "니체는 '도덕의 계보학'(1887)에서 양심의 가책(bad conscience)이 "
                "건강한 본능을 억압하는 도구가 될 수 있다고 경고했다. "
                "그러나 세네카는 자기 검토를 '자기 처벌'이 아니라 '개선의 수단'으로 제시하며, "
                "이 점에서 니체의 비판 대상인 기독교적 죄의식과 구별된다."
            ),
            "context": (
                "세네카의 자기 검토 실천은 이냐시오 드 로욜라(Ignatius of Loyola)의 "
                "'영신수련(Spiritual Exercises)'에서의 양심 성찰(examen)에 직접 영향을 주었다. "
                "또한 현대 인지행동치료(CBT)의 '사고 기록지(thought record)'나 "
                "일기 치료(journaling therapy)의 선구로 평가된다."
            ),
            "category": "윤리학·실천",
            "difficulty": "보통",
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """세네카 키워드 데이터 입력."""
    keywords = [
        {
            "id": "seneca-kw-001",
            "thinker_id": "seneca",
            "term": "메디타티오 모르티스 (Meditatio Mortis)",
            "term_original": "meditatio mortis",
            "definition": (
                "죽음의 명상. 세네카가 강조한 스토아적 정신 수련으로, "
                "죽음의 필연성을 매일 상기하여 삶의 유한성을 인식하고 "
                "현재를 더 의미 있게 사는 것을 목표로 한다. "
                "'우리는 매일 죽는다(quotidie morimur)'는 세네카의 유명한 명제가 이를 요약한다."
            ),
            "related_claims": ["seneca-claim-003", "seneca-claim-001"],
            "source": "Epistulae Morales 4.5; 12; 26"
        },
        {
            "id": "seneca-kw-002",
            "thinker_id": "seneca",
            "term": "프라에메디타티오 말로룸 (Praemeditatio Malorum)",
            "term_original": "praemeditatio malorum",
            "definition": (
                "불행의 사전 명상. 닥칠 수 있는 불행(유배, 빈곤, 질병, 죽음)을 "
                "미리 상상하여 심리적 준비를 하는 스토아적 수련법. "
                "미리 예상한 일은 충격이 줄어들고, 예상하지 못한 일은 충격이 배가된다는 원리. "
                "현대 심리학의 '체계적 둔감화(systematic desensitization)'와 구조적으로 유사하다."
            ),
            "related_claims": ["seneca-claim-004"],
            "source": "Epistulae Morales 76.33-34; 91"
        },
        {
            "id": "seneca-kw-003",
            "thinker_id": "seneca",
            "term": "클레멘티아 (Clementia)",
            "term_original": "clementia",
            "definition": (
                "관용 또는 인자. 형벌을 가할 권한이 있는 자가 이성적 판단에 기반하여 "
                "형벌을 절제하는 덕. 감정적 연민(misericordia)이나 면제(venia)와 구별된다. "
                "세네카는 이를 통치자의 최고 덕으로 제시했으며, "
                "네로에게 헌정한 '관용에 대하여(De Clementia)'에서 상세히 논했다."
            ),
            "related_claims": ["seneca-claim-007"],
            "source": "De Clementia I-II"
        },
        {
            "id": "seneca-kw-004",
            "thinker_id": "seneca",
            "term": "브레비스 푸로르 (Brevis Furor)",
            "term_original": "brevis furor",
            "definition": (
                "'짧은 광기'. 세네카가 분노를 정의하기 위해 사용한 표현(테오프라스토스에서 인용). "
                "분노는 이성을 완전히 마비시키는 격정(affectus)이며, "
                "시작되면 통제할 수 없으므로 시작 자체를 막아야 한다. "
                "분노는 어떤 상황에서도 정당화될 수 없다는 세네카의 핵심 주장을 상징한다."
            ),
            "related_claims": ["seneca-claim-002"],
            "source": "De Ira I.1.2"
        },
        {
            "id": "seneca-kw-005",
            "thinker_id": "seneca",
            "term": "엑사멘 콘스키엔티아에 (Examen Conscientiae)",
            "term_original": "examen conscientiae",
            "definition": (
                "양심 검토 또는 자기 회계. 매일 저녁 하루의 행동, 말, 생각을 "
                "되돌아보며 스토아적 원칙에 비추어 평가하는 실천. "
                "피타고라스학파와 섹스티우스의 전통에서 가져와 세네카가 스토아적으로 발전시켰다. "
                "이냐시오 드 로욜라의 영신수련에 직접 영향을 주었으며, "
                "현대 CBT의 사고 기록지(thought record)의 선구로 평가된다."
            ),
            "related_claims": ["seneca-claim-008"],
            "source": "De Ira III.36; Epistulae Morales 83.2"
        },
        {
            "id": "seneca-kw-006",
            "thinker_id": "seneca",
            "term": "비르투스 (Virtus)",
            "term_original": "virtus",
            "definition": (
                "덕 또는 탁월함. 라틴어 vir(남자)에서 파생된 말로 용기의 뉘앙스를 담지만, "
                "스토아 철학에서는 사주덕(지혜, 정의, 용기, 절제)을 포괄하는 총합적 개념. "
                "세네카에게 비르투스만이 유일한 선이며, 행복(vita beata)의 충분조건이다. "
                "그리스어 아레테(ἀρετή)의 라틴어 번역어."
            ),
            "related_claims": ["seneca-claim-005", "seneca-claim-006"],
            "source": "De Vita Beata 3-4; Epistulae Morales 74"
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """세네카 관계 데이터 입력."""
    relations = [
        {
            "id": "relation-chrysippus-seneca",
            "from_thinker": "chrysippus",
            "to_thinker": "seneca",
            "type": "influenced",
            "description": (
                "크리시포스(Chrysippus, 기원전 279~206)는 초기 스토아 학파의 체계를 완성한 철학자다. "
                "세네카의 윤리학, 격정론(passiones), 운명론은 크리시포스의 이론적 기초 위에 서 있다. "
                "세네카는 크리시포스를 존경하면서도 그의 지나친 논리적 세밀함을 비판하고 "
                "실천적 적용을 중시했다."
            ),
            "strength": "보통",
            "period": "기원전 3세기 → 기원후 1세기"
        },
        {
            "id": "relation-seneca-montaigne",
            "from_thinker": "seneca",
            "to_thinker": "montaigne",
            "type": "influenced",
            "description": (
                "몽테뉴(Michel de Montaigne, 1533~1592)는 세네카의 열렬한 독자였으며, "
                "'수상록(Essais)'에서 세네카를 빈번히 인용했다. "
                "몽테뉴의 에세이 형식, 죽음에 대한 성찰, 자기 검토의 전통은 "
                "세네카의 '도덕 서한집'에 직접적으로 영향을 받았다. "
                "몽테뉴는 세네카와 플루타르코스를 자신의 '두 기둥'이라 불렀다."
            ),
            "strength": "강함",
            "period": "1세기 → 16세기"
        },
        {
            "id": "relation-seneca-ignatius",
            "from_thinker": "seneca",
            "to_thinker": "ignatius_loyola",
            "type": "influenced",
            "description": (
                "세네카의 자기 검토(examen conscientiae) 실천은 "
                "이냐시오 드 로욜라(Ignatius of Loyola, 1491~1556)의 "
                "'영신수련(Spiritual Exercises)'에서의 양심 성찰에 직접 영향을 주었다. "
                "초기 기독교 교부들이 세네카를 '거의 기독교인'으로 평가했으며, "
                "세네카와 사도 바울 사이의 위조 서한도 이 전통에서 나왔다."
            ),
            "strength": "보통",
            "period": "1세기 → 16세기"
        },
        {
            "id": "relation-epicurus-seneca",
            "from_thinker": "epicurus",
            "to_thinker": "seneca",
            "type": "influenced",
            "description": (
                "세네카는 스토아 철학자이지만 에피쿠로스의 격언과 통찰을 자주 인용했다. "
                "'도덕 서한집' 초기 편지들에서 에피쿠로스의 격언을 매번 인용하며, "
                "'진리는 어떤 학파의 소유도 아니다'라는 절충적 태도를 보였다. "
                "특히 우정, 단순한 삶, 쾌락의 절제 등에서 에피쿠로스와 공통점을 인정했다."
            ),
            "strength": "보통",
            "period": "기원전 3세기 → 기원후 1세기"
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
    r = client.get(index=INDEX_THINKERS, id="seneca")
    print(f"[thinker] seneca: name={r['_source']['name_en']}, era={r['_source']['era']}")

    # works 확인
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "seneca"}})
    print(f"[works] seneca 저서 수: {works_count['count']}")
    works_result = client.search(
        index=INDEX_WORKS,
        query={"term": {"thinker_id": "seneca"}},
        _source=["id", "title_original", "year"]
    )
    for hit in works_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['title_original']} ({s['year']})")

    # claims 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "seneca"}})
    print(f"[claims] seneca 주장 수: {claims_count['count']}")
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "seneca"}},
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
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "seneca"}})
    print(f"[keywords] seneca 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_count = client.count(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "seneca"}},
            {"term": {"to_thinker": "seneca"}}
        ]}}
    )
    print(f"[relations] seneca 관련 관계 수: {rel_count['count']}")
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "seneca"}},
            {"term": {"to_thinker": "seneca"}}
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
        print("=== 세네카(Seneca) 데이터 입력 시작 ===\n")

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
