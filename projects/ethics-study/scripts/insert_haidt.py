"""조너선 하이트(Jonathan Haidt) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS, INDEX_FIELDS
)


def ensure_field(client):
    """도덕발달 분야가 ethics-fields 인덱스에 없으면 추가."""
    try:
        client.get(index=INDEX_FIELDS, id="moral_development")
        print("[field] moral_development: 이미 존재")
    except Exception:
        doc = {
            "id": "moral_development",
            "name": "도덕발달론",
            "description": (
                "아동 및 인간의 도덕 판단과 도덕 행동이 어떻게 발달하는지를 탐구하는 분야. "
                "피아제의 인지발달 기반 도덕발달 이론, 콜버그의 도덕발달 단계론, "
                "길리건의 배려윤리, 나딩스의 배려교육론 등을 포함한다. "
                "도덕심리학, 도덕교육론과 밀접하게 연관되며 임용시험 핵심 영역이다."
            ),
            "order": 4
        }
        result = client.index(index=INDEX_FIELDS, id="moral_development", document=doc)
        print(f"[field] moral_development: {result['result']}")


def insert_thinker(client):
    """하이트 사상가 데이터 입력."""
    doc = {
        "id": "haidt",
        "name": "조너선 하이트",
        "name_en": "Jonathan Haidt",
        "field": "moral_development",
        "era": "현대",
        "birth_year": 1963,
        "background": (
            "뉴욕 출신으로 예일 대학교에서 철학을 전공하고 펜실베이니아 대학교에서 심리학 박사학위(1992)를 받았다. "
            "버지니아 대학교 심리학과에서 16년간 재직하며 도덕심리학의 새 패러다임을 정립하였고, "
            "2011년부터 뉴욕대학교(NYU) 스턴 경영대학원 교수로 재직 중이다. "
            "초기 연구에서는 혐오(disgust)와 도덕 감정의 연계성을 탐구하였고, "
            "2001년 '사회적 직관주의 모델(Social Intuitionist Model)'을 발표하여 "
            "도덕 판단에서 직관이 추론보다 앞선다는 혁신적 주장을 제시했다. "
            "이후 리처드 쇼더(Richard Shweder)의 문화심리학과 앨런 피스크(Alan Fiske)의 관계 이론에 영향을 받아 "
            "도덕기반이론(Moral Foundations Theory)을 발전시켰다. "
            "정치 성향과 도덕 심리의 관계를 연구하여 진보와 보수가 다른 도덕 기반을 강조함을 밝혔다."
        ),
        "core_philosophy": (
            "하이트 도덕심리학의 핵심은 도덕적 직관주의(moral intuitionism)와 도덕기반이론(Moral Foundations Theory)이다. "
            "사회적 직관주의 모델에 따르면 도덕 판단은 빠르고 자동적인 직관적 반응에서 시작되며, "
            "추론은 사후에 그 판단을 정당화하는 역할을 한다. "
            "'코끼리와 기수' 비유에서 직관(코끼리)이 방향을 결정하고 추론(기수)은 따라가며 합리화할 뿐이다. "
            "도덕기반이론은 인간의 도덕성이 진화적으로 준비된 6가지 기초 위에 세워진다고 본다: "
            "배려/피해(Care/Harm), 공정/속임(Fairness/Cheating), 충성/배신(Loyalty/Betrayal), "
            "권위/전복(Authority/Subversion), 신성/타락(Sanctity/Degradation), 자유/억압(Liberty/Oppression). "
            "콜버그와 피아제의 합리주의적 도덕발달론을 비판하며, "
            "도덕성은 추론 능력의 발달이 아니라 진화적으로 준비된 정서·직관의 산물이라고 주장했다."
        ),
        "philosophical_journey": (
            "초기(1990년대): 혐오(disgust)와 도덕 감정의 연계성 연구. 브라질, 인도, 미국 비교 문화 연구를 통해 "
            "도덕적 판단이 문화마다 다양하며 추론만으로 설명되지 않음을 확인했다. "
            "중기(2001~2010): 2001년 '감정적 강아지와 이성적 꼬리(The Emotional Dog and Its Rational Tail)'로 "
            "사회적 직관주의 모델을 제안. 2004년 쇼더, 피스크와 함께 도덕기반이론의 초기 틀을 제시. "
            "후기(2010년대~): 2012년 '바른 마음(The Righteous Mind)'으로 도덕기반이론을 대중화하고 "
            "정치심리학에 적용. 진보와 보수의 도덕 기반 차이를 분석하여 정치적 분극화를 설명. "
            "그렉 루키아노프와 함께 '과보호하는 미국의 정신(2018)'으로 대학 캠퍼스 문화와 인지 왜곡을 비판했다."
        ),
        "keywords": [
            "사회적 직관주의",
            "도덕기반이론",
            "코끼리와 기수",
            "배려/피해",
            "공정/속임",
            "충성/배신",
            "권위/전복",
            "신성/타락",
            "자유/억압",
            "WEIRD",
            "도덕적 직관주의",
            "nativism"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="haidt", document=doc)
    print(f"[thinker] haidt: {result['result']}")
    return result


def insert_works(client):
    """하이트 저서 데이터 입력."""
    works = [
        {
            "id": "haidt-righteous-mind",
            "thinker_id": "haidt",
            "title": "바른 마음: 나의 옳음과 그들의 옳음은 왜 다른가",
            "title_original": "The Righteous Mind: Why Good People Are Divided by Politics and Religion",
            "year": 2012,
            "significance": (
                "하이트의 대표작으로, 도덕기반이론(Moral Foundations Theory)을 종합적으로 제시한 저작이다. "
                "왜 선한 사람들이 도덕적으로 대립하는지를 직관-추론의 비대칭 구조와 "
                "6가지 도덕 기반으로 설명한다. "
                "진보(배려·공정 강조)와 보수(6개 기반 균형 강조)의 도덕 심리 차이를 분석하여 "
                "정치적 분극화의 심리적 뿌리를 해명했다. "
                "사회적 직관주의 모델, 코끼리와 기수 비유, WEIRD 편향 비판이 체계적으로 제시되어 있다."
            ),
            "key_concepts": [
                "도덕기반이론", "사회적 직관주의", "코끼리와 기수",
                "배려/피해", "공정/속임", "충성/배신",
                "권위/전복", "신성/타락", "자유/억압",
                "WEIRD", "nativism"
            ]
        },
        {
            "id": "haidt-happiness-hypothesis",
            "thinker_id": "haidt",
            "title": "행복의 가설",
            "title_original": "The Happiness Hypothesis: Finding Modern Truth in Ancient Wisdom",
            "year": 2006,
            "significance": (
                "하이트가 고대 철학과 현대 심리학을 종합하여 행복의 조건을 탐구한 저작이다. "
                "'코끼리와 기수' 비유가 처음 등장하는 책으로, "
                "감정(코끼리)과 이성(기수)의 관계, 자동적 처리와 통제적 처리의 비대칭을 설명했다. "
                "스토아, 불교, 기독교 등의 지혜와 현대 긍정심리학을 연결하여 "
                "인간의 도덕 감정과 행복 추구를 심리학적으로 탐구했다."
            ),
            "key_concepts": [
                "코끼리와 기수", "행복", "긍정심리학", "자동적 처리", "이중처리 이론"
            ]
        },
        {
            "id": "haidt-coddling-of-american-mind",
            "thinker_id": "haidt",
            "title": "과보호하는 미국의 정신",
            "title_original": "The Coddling of the American Mind: How Good Intentions and Bad Ideas Are Setting Up a Generation for Failure",
            "year": 2018,
            "significance": (
                "그렉 루키아노프(Greg Lukianoff)와 공저한 저작으로, "
                "미국 대학 캠퍼스에서 나타나는 안전주의(safetyism) 문화를 인지행동치료(CBT)의 "
                "인지 왜곡 개념으로 비판했다. "
                "세 가지 나쁜 관념(진실은 내 감정이다/선의와 악의의 이분법/우리는 취약하다)이 "
                "학생들의 심리적 회복력을 약화시킨다고 주장했다. "
                "도덕심리학의 관점에서 도덕적 의존성과 제도적 보호 요구가 도덕 발달을 저해한다고 비판했다."
            ),
            "key_concepts": [
                "안전주의", "인지 왜곡", "심리적 취약성", "도덕 의존성", "회복력"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """하이트 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 사회적 직관주의 모델 — 직관 우선, 추론은 사후 정당화
        {
            "id": "haidt-claim-001",
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "source_detail": "The Righteous Mind, Part 1: Chapter 2 — The Emotional Dog and Its Rational Tail",
            "claim": (
                "도덕 판단은 빠르고 자동적인 직관에서 먼저 발생하고, "
                "추론은 나중에 그 직관적 판단을 정당화하는 역할을 한다(사회적 직관주의 모델). "
                "이성은 도덕 판단의 원인이 아니라 결론이 먼저 내려진 후에 작동하는 사후적 정당화 도구이다."
            ),
            "original_text": (
                "The social intuitionist model says that moral reasoning is usually a post hoc construction, "
                "generated after a judgment has been reached. "
                "The dog wags its tail, and most of what goes on is automatic, effortless, and inaccessible."
            ),
            "explanation": (
                "하이트는 콜버그의 합리주의 모델(도덕 판단은 추론의 산물)을 뒤집는다. "
                "사회적 직관주의 모델(SIM)에 따르면 도덕 판단은 6단계를 거친다: "
                "① 직관적 판단 → ② 도덕적 추론(사후 정당화) → ③ 사회적 설득 → "
                "④ 타인의 추론에 의한 영향 → ⑤ 직관에 의한 직접 설득 → ⑥ 반성적 추론에 의한 판단 변경. "
                "실험에서 사람들은 도덕적으로 불쾌하지만 피해자 없는 행위(예: 국기로 화장실 청소)를 "
                "왜 나쁜지 설명하지 못하면서도('도덕적 무성어화(moral dumbfounding)') 나쁘다고 판단했다. "
                "이는 판단이 추론이 아닌 직관에서 나옴을 보여준다."
            ),
            "argument": (
                "(1) 도덕적 무성어화(moral dumbfounding) 실험: 피해자 없는 도덕적 불쾌 시나리오에서 "
                "사람들은 왜 나쁜지 설명하지 못하면서도 나쁘다는 판단을 유지했다. "
                "(2) 이중처리 이론(dual process theory): 시스템 1(빠른 직관)이 먼저 반응하고, "
                "시스템 2(느린 추론)는 주로 정당화에 사용된다. "
                "(3) 신경과학적 증거: 도덕 판단 시 감정 처리 영역이 먼저 활성화되고, "
                "추론 영역은 나중에 활성화된다."
            ),
            "counterpoint": (
                "그린(Joshua Greene)은 이중처리 이론을 지지하면서도 "
                "추론이 직관을 극복할 수 있다는 점(공리주의적 판단)을 강조했다. "
                "스캔런(T.M. Scanlon)은 도덕 판단에서 추론의 독립적 역할을 옹호했다. "
                "피아제와 콜버그의 합리주의 전통에서는 도덕 추론의 발달이 도덕 행동 개선과 "
                "연결된다고 반론한다."
            ),
            "context": (
                "1990년대 혐오 감정과 도덕 판단 연구에서 출발하여, "
                "2001년 Psychological Review에 '감정적 강아지와 이성적 꼬리(The Emotional Dog and Its Rational Tail)'로 발표. "
                "플라톤 이래의 이성 중심 도덕철학과 콜버그 도덕발달론에 대한 도전이다."
            ),
            "keywords": ["사회적 직관주의", "도덕 판단", "직관", "사후 정당화", "도덕적 무성어화"],
            "verified": False
        },
        # CLAIM-002: 코끼리와 기수 비유
        {
            "id": "haidt-claim-002",
            "thinker_id": "haidt",
            "work_id": "haidt-happiness-hypothesis",
            "source_detail": "The Happiness Hypothesis, Chapter 1 — The Divided Self",
            "claim": (
                "인간의 마음은 '코끼리(elephant)'와 '기수(rider)'로 나눌 수 있다. "
                "코끼리는 감정, 직관, 자동적 처리를 상징하고, "
                "기수는 이성적 추론, 의식적 사고를 상징한다. "
                "기수는 코끼리를 통제하는 것처럼 보이지만, 실제로는 코끼리가 방향을 결정하고 "
                "기수는 이를 정당화하거나 따라갈 뿐이다."
            ),
            "original_text": (
                "The rider is conscious verbal thinking. The elephant is everything else. "
                "The rider can do several useful things: It can see further into the future, "
                "help the elephant make better choices, and learn new skills. "
                "But the elephant is much bigger and stronger, and when the two conflict, "
                "the elephant usually wins."
            ),
            "explanation": (
                "하이트의 코끼리-기수 비유는 이중처리 이론을 직관적으로 표현한다. "
                "코끼리(감정·직관·습관·자동 처리): 크고 강하며, 즉각적이고 강력하다. 도덕적 반응의 주된 원천. "
                "기수(이성·추론·계획): 코끼리를 안내하거나 설명할 수 있지만, "
                "코끼리가 방향을 정하면 기수는 따라가며 합리화한다. "
                "도덕교육에 대한 함의: 단순히 이성적 추론을 가르치는 것만으로는 부족하며, "
                "직관과 감정을 올바르게 형성하는 것이 중요하다."
            ),
            "argument": (
                "(1) 신경과학: 변연계(감정)는 전두엽(추론)보다 진화적으로 오래되었고 더 빠르게 반응한다. "
                "(2) 의지력 연구(Roy Baumeister): 자기통제는 한정된 자원이며 쉽게 고갈된다. "
                "(3) 도덕적 무성어화 실험: 사람들은 이성적 설명 없이도 도덕 판단을 확신한다."
            ),
            "counterpoint": (
                "일부 철학자들은 이 비유가 이성의 역할을 과소평가한다고 비판한다. "
                "칸트적 전통에서는 도덕적 자율성이 이성적 자기규제에 달려 있다고 본다. "
                "그린은 공리주의적 추론이 직관적 반응을 극복하는 사례가 있다고 반론했다."
            ),
            "context": (
                "2006년 '행복의 가설'에서 처음 체계적으로 제시되고, "
                "2012년 '바른 마음'에서 도덕 판단과 정치 심리 분석에 핵심 틀로 활용되었다."
            ),
            "keywords": ["코끼리와 기수", "이중처리 이론", "직관", "이성", "자동 처리"],
            "verified": False
        },
        # CLAIM-003: 도덕기반이론 — 6가지 도덕 기반
        {
            "id": "haidt-claim-003",
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "source_detail": "The Righteous Mind, Part 2: Chapter 6 — Taste Buds of the Righteous Mind",
            "claim": (
                "인간의 도덕성은 진화적으로 준비된 6가지 기초(moral foundations) 위에 세워진다: "
                "① 배려/피해(Care/Harm), ② 공정/속임(Fairness/Cheating), "
                "③ 충성/배신(Loyalty/Betrayal), ④ 권위/전복(Authority/Subversion), "
                "⑤ 신성/타락(Sanctity/Degradation), ⑥ 자유/억압(Liberty/Oppression). "
                "각 기초는 진화 과정에서 특정 적응 문제를 해결하기 위해 형성된 직관 모듈이며, "
                "문화는 이 기초 위에 다양한 도덕 체계를 구축한다."
            ),
            "explanation": (
                "도덕기반이론(MFT)은 도덕성의 보편적 심리적 기반을 제안한다. "
                "① 배려/피해: 아이와 취약자를 돌보는 것에서 진화. 공감, 연민 관련. "
                "② 공정/속임: 협력과 상호 이익에서 진화. 정의, 권리, 자율성 관련. "
                "③ 충성/배신: 연합 집단 형성에서 진화. 집단 충성, 자기희생 관련. "
                "④ 권위/전복: 위계적 사회 구조에서 진화. 존경, 전통, 리더십 관련. "
                "⑤ 신성/타락: 병원체 회피에서 진화. 혐오, 순수, 신성함 관련. "
                "⑥ 자유/억압: 지배에 대한 저항에서 진화. 자유, 자율성 관련. "
                "진보주의자는 주로 ①②를, 보수주의자는 여섯 기반 모두를 균형 있게 사용한다."
            ),
            "argument": (
                "(1) 쇼더(Shweder)의 세 가지 윤리(자율성, 공동체, 신성) + 피스크(Fiske)의 관계 이론에서 출발. "
                "(2) 비교 문화 연구: 서양·비서양 사회 모두에서 6가지 기반이 나타나지만 강조 비율이 다름. "
                "(3) YourMorals.org 대규모 설문: 정치 성향과 도덕 기반 프로파일의 일관된 상관관계 확인."
            ),
            "counterpoint": (
                "그레이(Kurt Gray)는 도덕성이 배려/피해 하나의 기반으로 환원 가능하다고 주장했다. "
                "오트만(Ohtman)은 이론의 경험적 기반(설문)이 문화 편향적이라고 비판했다. "
                "일부는 '신성' 기반이 종교·문화 특수적이라 보편적 도덕 기반으로 보기 어렵다고 주장한다."
            ),
            "context": (
                "2004년 쇼더·피스크와 공저 논문에서 초기 3기반 이론을 제시하고, "
                "2007년 이후 조셉·해넘(Joseph & Haidt)을 통해 5기반으로 확장, "
                "2011년 Graham et al.에서 자유/억압을 6번째 기반으로 추가했다."
            ),
            "keywords": ["도덕기반이론", "배려/피해", "공정/속임", "충성/배신", "권위/전복", "신성/타락", "자유/억압"],
            "verified": False
        },
        # CLAIM-004: 배려/피해 기반
        {
            "id": "haidt-claim-004",
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "source_detail": "The Righteous Mind, Part 2: Chapter 7",
            "claim": (
                "배려/피해(Care/Harm) 기반은 취약한 존재를 보호하고 고통을 피하려는 진화적 직관이다. "
                "공감과 연민의 감정에 뿌리를 두며, 아이나 취약자가 상처 받는 것에 대한 강력한 반응을 유발한다. "
                "진보주의 도덕 체계에서 가장 중심적인 기반이다."
            ),
            "explanation": (
                "배려/피해 기반은 자녀 양육과 취약자 보호에서 진화했다. "
                "촉발자(trigger): 고통, 상처, 슬픔, 취약성의 단서. "
                "특징적 감정: 공감, 연민, 분노(피해자 대신). "
                "도덕적 덕목: 친절, 돌봄, 자비, 비폭력. "
                "진보주의자들은 이 기반을 도덕의 핵심으로 보는 경향이 강하다."
            ),
            "argument": (
                "(1) 진화적 기원: 영장류에서도 유사한 행동이 관찰된다. "
                "(2) 보편성: 모든 문화에서 아동 학대와 취약자 해침을 도덕적으로 잘못으로 여긴다. "
                "(3) 실험: 귀여운 얼굴(아기 모습)을 보면 즉각적 돌봄 반응이 유발된다."
            ),
            "counterpoint": (
                "그레이(Gray)는 배려/피해가 모든 도덕을 통합하는 단일 기반이라 주장하며 "
                "다기반 이론에 반론한다. "
                "배려 기반 과잉 강조는 '피해자 문화(victimhood culture)' 조장을 낳을 수 있다는 비판도 있다."
            ),
            "context": (
                "YourMorals.org 연구에서 진보주의자들은 보수주의자보다 배려 기반 점수가 높게 나타났다."
            ),
            "keywords": ["배려/피해", "공감", "연민", "취약성", "진보 도덕"],
            "verified": False
        },
        # CLAIM-005: 콜버그·피아제 합리주의 비판
        {
            "id": "haidt-claim-005",
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "source_detail": "The Righteous Mind, Part 1: Chapter 3 — Elephant and Rider",
            "claim": (
                "콜버그와 피아제의 합리주의적 도덕발달론은 도덕 판단을 추론 능력의 발달로 설명하지만, "
                "이는 실제 도덕 심리를 오해한 것이다. "
                "도덕성은 합리적 추론의 산물이 아니라, "
                "진화적으로 준비된 직관·감정 반응의 산물이며, 추론은 이를 사후에 정당화할 뿐이다."
            ),
            "explanation": (
                "피아제는 인지 발달이 도덕 발달을 이끈다고 보았고, "
                "콜버그는 추론 능력이 향상될수록 더 높은 도덕 단계에 도달한다고 주장했다. "
                "하이트는 이들이 철학자의 오류(합리주의 편향)를 범한다고 비판한다. "
                "도덕적 무성어화 실험: 사람들은 왜 그것이 나쁜지 설명하지 못하면서도 "
                "강하게 나쁘다는 판단을 유지했다. 이는 판단이 추론이 아닌 직관에서 비롯됨을 보여준다. "
                "또한 콜버그는 도덕을 정의(justice)와 권리 중심으로 좁게 정의하여 "
                "충성, 권위, 신성 같은 다른 도덕 기반을 무시했다."
            ),
            "argument": (
                "(1) 도덕적 무성어화 실험에서 피험자들은 추론 없이도 강한 도덕 판단을 내렸다. "
                "(2) 실제 사회에서 도덕적으로 높은 수준의 추론자가 도덕적으로 더 행동하지 않는다. "
                "(3) 비교 문화 연구: 비서양 사회에서는 공정·권리 외에 충성·권위·신성 기반 도덕이 강하게 나타난다. "
                "(4) 콜버그 연구 대상 편향: 주로 WEIRD(서양, 교육받은, 부유한) 남성들."
            ),
            "counterpoint": (
                "콜버그와 피아제는 도덕 발달의 방향성과 교육적 개입 가능성을 제시한 점에서 여전히 가치가 있다. "
                "일부 연구자는 하이트가 추론의 역할을 지나치게 평가절하한다고 비판한다. "
                "추론이 도덕 판단을 사후에만 지지하는 것이 아니라 변경할 수도 있다는 증거가 있다."
            ),
            "context": (
                "하이트는 2001년 논문에서 콜버그의 도덕발달 모델이 지나치게 추론 중심이라고 명시적으로 비판했다. "
                "이는 도덕심리학 내 합리주의 vs 직관주의 논쟁의 핵심이다."
            ),
            "keywords": ["합리주의 비판", "콜버그", "피아제", "도덕 추론", "직관"],
            "verified": False
        },
        # CLAIM-006: 도덕성의 선천적 기초 (Nativism)
        {
            "id": "haidt-claim-006",
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "source_detail": "The Righteous Mind, Part 2: Chapter 5 — Beyond WEIRD Morality",
            "claim": (
                "도덕적 기반은 선천적으로 준비(innately prepared)되어 있다. "
                "인간은 특정 자극(예: 아이의 고통, 집단 배신)에 반응하도록 진화적으로 준비된 "
                "'첫 번째 초안(first draft)'을 가지고 태어나며, "
                "문화와 경험이 이 초안을 수정하고 정교화한다."
            ),
            "explanation": (
                "하이트의 nativism은 강한 nativism(도덕 규칙이 선천적으로 내재)이 아닌 "
                "약한 nativism(도덕 반응에 대한 진화적 준비성)을 의미한다. "
                "마코비(Cosmides)와 투비(Tooby)의 진화심리학에 영향받아, "
                "인간의 마음은 특정 적응 문제에 반응하는 모듈로 이루어져 있다고 본다. "
                "도덕 기반은 인류 진화 환경에서 반복되었던 문제들(배신자 탐지, 연합 유지 등)에 "
                "대한 적응적 반응으로 형성되었다."
            ),
            "argument": (
                "(1) 영아 연구: 생후 수개월의 아기도 공정성과 친절함에 대한 선호를 보인다(Hamlin et al., 2007). "
                "(2) 비교문화: 피해, 공정, 충성 관련 도덕 직관이 문화 전반에서 나타난다. "
                "(3) 진화적 설명: 각 도덕 기반은 반복적 사회 문제에 대한 진화적 해결책으로 설명 가능하다."
            ),
            "counterpoint": (
                "사회구성주의자들은 도덕이 문화적 학습의 산물이며 선천성 주장을 과장이라 비판한다. "
                "진화심리학 자체에 대한 방법론적 비판(적응주의의 '그냥 그런 이야기')이 있다."
            ),
            "context": (
                "쇼더의 문화심리학과 마코비·투비의 진화심리학을 통합하여 "
                "도덕의 선천성과 문화적 다양성을 동시에 설명하려는 시도이다."
            ),
            "keywords": ["nativism", "선천적 도덕", "진화심리학", "도덕 모듈", "첫 번째 초안"],
            "verified": False
        },
        # CLAIM-007: WEIRD 편향 비판
        {
            "id": "haidt-claim-007",
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "source_detail": "The Righteous Mind, Part 2: Chapter 5 — Beyond WEIRD Morality",
            "claim": (
                "서양 도덕철학과 콜버그 도덕심리학은 WEIRD(Western, Educated, Industrialized, Rich, Democratic) "
                "사회의 특수한 도덕 감각을 보편적인 것으로 오해하는 편향이 있다. "
                "WEIRD 사회는 자율성, 개인 권리, 공정성을 도덕의 핵심으로 보지만, "
                "전 세계 대부분의 문화는 공동체, 권위, 신성함을 포함한 더 넓은 도덕 영역을 가진다."
            ),
            "explanation": (
                "하이트는 헨리크(Henrich), 하이네(Heine), 노렌자이안(Norenzayan)의 "
                "'WEIRD 문제' 논문(2010)에서 아이디어를 얻어 도덕심리학에 적용했다. "
                "WEIRD 사회의 특징: 개인주의, 분석적 사고, 독립적 자아관. "
                "비WEIRD 사회: 집단주의, 전체론적 사고, 상호의존적 자아관. "
                "콜버그 도덕발달론은 WEIRD 도덕(자율성과 공정)을 최고 단계로 상정하여 "
                "비WEIRD 도덕(공동체, 권위, 신성)을 낮은 단계로 폄하한다."
            ),
            "argument": (
                "(1) 쇼더의 비교 문화 연구: 인도인들은 배려·공정 외에 공동체·신성에서도 "
                "강한 도덕 판단을 내린다. "
                "(2) YourMorals.org 데이터: 정치 성향과 도덕 기반 사용의 문화 간 차이. "
                "(3) 심리학 실험의 대부분이 북미·유럽 학부생을 대상으로 하여 보편성 주장에 한계가 있다."
            ),
            "counterpoint": (
                "WEIRD 내에서도 내부 다양성이 크다. "
                "일부 보편 도덕(살인 금지, 아동 보호)은 WEIRD/비WEIRD 구분을 초월한다. "
                "WEIRD 편향 비판이 문화상대주의로 흐를 경우 도덕적 진보의 기준을 잃는다는 우려가 있다."
            ),
            "context": (
                "서양 도덕철학과 심리학이 지나치게 좁은 표본과 문화적 가정에 기반하고 있음을 비판하는 맥락. "
                "도덕심리학의 비교 문화적 확장을 촉구한다."
            ),
            "keywords": ["WEIRD", "문화 편향", "보편 도덕", "개인주의", "공동체주의"],
            "verified": False
        },
        # CLAIM-008: 진보와 보수의 도덕 기반 차이
        {
            "id": "haidt-claim-008",
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "source_detail": "The Righteous Mind, Part 3: Chapter 12 — Can't We All Disagree More Constructively?",
            "claim": (
                "진보주의자(liberals)는 주로 배려/피해와 자유/억압 기반에 집중하여 도덕 판단을 내리는 반면, "
                "보수주의자(conservatives)는 여섯 가지 도덕 기반 모두를 상대적으로 균형 있게 활용한다. "
                "정치적 갈등의 근원은 이성적 판단의 차이가 아니라 "
                "근본적으로 다른 도덕 직관 프로파일에 있다."
            ),
            "explanation": (
                "YourMorals.org 대규모 설문 데이터 분석 결과: "
                "진보주의자: 배려(+), 공정(+), 충성(-), 권위(-), 신성(-), 자유(+) 강조. "
                "보수주의자: 모든 기반을 비교적 균등하게 강조, 특히 충성·권위·신성 기반 상대적 고점. "
                "이에 따라 진보주의자는 보수주의자의 도덕을 이해하기 어렵고, "
                "보수주의자는 진보주의자에게 빠진 도덕 언어가 있다고 느낀다. "
                "도덕 행렬(moral matrix)이 다르기 때문에 정치적 대화가 어렵다."
            ),
            "argument": (
                "(1) YourMorals.org의 수만 명 데이터: 일관되게 진보·보수 간 도덕 기반 프로파일 차이가 확인됨. "
                "(2) 진화적 기원: 진보는 집단 외부를 향한 개방성(openness to experience)과 상관, "
                "보수는 위계와 전통을 통한 질서 유지와 상관. "
                "(3) 도덕 언어 분석: 진보 정치인과 보수 정치인의 연설에서 사용하는 도덕 어휘 차이."
            ),
            "counterpoint": (
                "도덕 기반 설문이 자기보고에 의존하므로 실제 행동을 예측하지 못할 수 있다. "
                "진보·보수 이분법이 지나치게 단순하며 내부 다양성을 무시한다는 비판. "
                "나딩스(Noddings)는 배려윤리가 진보·보수를 초월하는 보편적 가치라고 반론한다."
            ),
            "context": (
                "미국 정치 양극화가 심화되는 맥락에서, "
                "하이트는 상대 진영을 이해하기 위해서는 그들의 도덕 직관을 이해해야 한다고 주장한다. "
                "이를 위해 '도덕 매트릭스(moral matrix)' 개념을 사용한다."
            ),
            "keywords": ["진보 도덕", "보수 도덕", "정치 심리", "도덕 행렬", "정치적 분극화"],
            "verified": False
        },
        # CLAIM-009: 도덕은 집단 결속을 위해 진화했다 (Hive Hypothesis)
        {
            "id": "haidt-claim-009",
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "source_detail": "The Righteous Mind, Part 3: Chapter 10 — The Hive Switch",
            "claim": (
                "인간은 개인의 이익을 추구하는 동시에 집단의 일부로 녹아드는 '군집성(hivishness)'을 가진다. "
                "도덕 감정과 종교적 경험은 개인을 넘어 집단에 헌신하게 만드는 '군집 스위치(hive switch)'를 작동시키며, "
                "이는 집단 수준의 선택(group selection)이 인간 도덕의 진화에 기여했음을 시사한다."
            ),
            "explanation": (
                "하이트는 인간이 90%는 침팬지(개인 이기성)이지만 10%는 꿀벌(집단 헌신)이라고 비유한다. "
                "군집 스위치가 켜지는 조건: 군악대 행진, 종교 의식, 스포츠 응원, 집단 위기 등. "
                "이때 개인의 경계가 흐려지고 집단 정체성이 강화된다. "
                "이는 인간이 초사회적 동물로 진화했음을 보여주며, "
                "도덕 체계가 개인 행동 규제뿐 아니라 집단 결속 기능을 한다는 것을 의미한다."
            ),
            "argument": (
                "(1) 집단 선택론: 윌슨(D.S. Wilson)의 다수준 선택 이론에 기반하여 "
                "집단 수준에서 이타적 집단이 이기적 집단을 이길 수 있다고 주장. "
                "(2) 플로우(flow) 경험: 칙센트미하이(Csikszentmihalyi)의 집단 몰입 연구. "
                "(3) 종교·의례의 사회적 기능: 집단 결속을 강화하는 도구로서의 종교."
            ),
            "counterpoint": (
                "집단 선택론은 진화생물학에서 논쟁적이다(도킨스, 피크(Pinker)의 반론). "
                "군집 본능이 집단 간 갈등과 전쟁의 심리적 기반이 된다는 비판. "
                "종교의 적응적 기능 강조가 종교의 인식론적 주장을 회피한다는 비판."
            ),
            "context": (
                "'바른 마음' 3부에서 도덕이 단순히 개인 행동 규제가 아니라 "
                "집단 결속 메커니즘이라는 진화적 관점을 제시하는 맥락이다."
            ),
            "keywords": ["군집 스위치", "집단 결속", "집단 선택", "초사회성", "종교와 도덕"],
            "verified": False
        },
        # CLAIM-010: 도덕은 미뢰(taste bud)와 같다 — 도덕 심리의 보편성과 다양성
        {
            "id": "haidt-claim-010",
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "source_detail": "The Righteous Mind, Part 2: Chapter 6 — Taste Buds of the Righteous Mind",
            "claim": (
                "도덕 기반은 음식의 맛을 감지하는 미뢰(taste buds)와 같다. "
                "미뢰가 단맛, 짠맛, 쓴맛 등 다양한 맛에 반응하듯, "
                "인간의 도덕 심리는 여러 도덕 기반에 반응할 수 있도록 준비되어 있다. "
                "도덕 체계들은 이 기반들 중 어떤 것을 강조하느냐에 따라 다양한 '맛'을 낸다."
            ),
            "explanation": (
                "미뢰 비유는 도덕의 보편성(모든 인간이 같은 도덕 기반을 가짐)과 "
                "다양성(문화마다 강조하는 기반이 다름)을 동시에 설명한다. "
                "단맛만 좋아하는 사람이 쓴맛을 이해 못하듯, "
                "일부 기반만 발달시킨 사람(문화)은 다른 기반에 반응하는 사람을 이해하지 못한다. "
                "도덕교육 함의: 다양한 도덕 기반을 경험하고 발달시키는 것이 중요하다."
            ),
            "argument": (
                "(1) 미각의 진화적 기원과 다양성은 도덕 기반의 진화적 기원과 문화적 다양성의 좋은 유비이다. "
                "(2) 문화 비교: 모든 문화에서 기반은 존재하지만 강조 비율이 다르다."
            ),
            "counterpoint": (
                "미뢰 비유는 도덕을 주관적 취향으로 환원시킬 위험이 있다는 비판. "
                "도덕적 진보(노예제 폐지 등)를 미뢰 변화로 설명하기 어렵다."
            ),
            "context": (
                "'바른 마음' 2부의 핵심 비유로, 도덕기반이론을 직관적으로 설명하기 위해 사용된다."
            ),
            "keywords": ["미뢰 비유", "도덕기반이론", "보편성", "다양성", "도덕 직관"],
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """하이트 핵심 키워드 데이터 입력."""
    keywords = [
        {
            "id": "kw-social-intuitionist-model",
            "term": "사회적 직관주의 모델",
            "term_en": "Social Intuitionist Model (SIM)",
            "definition": (
                "하이트가 2001년 제안한 도덕 판단 모델. "
                "도덕 판단은 빠르고 자동적인 직관에서 먼저 발생하며, "
                "추론은 나중에 그 판단을 정당화하는 사후적 역할을 한다고 본다. "
                "콜버그의 합리주의 모델과 대립되는 직관주의적 입장이다."
            ),
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "related_terms": ["도덕 판단", "직관", "사후 정당화", "이중처리 이론", "코끼리와 기수"]
        },
        {
            "id": "kw-moral-foundations-theory",
            "term": "도덕기반이론",
            "term_en": "Moral Foundations Theory (MFT)",
            "definition": (
                "하이트와 동료들이 제안한 이론으로, 인간의 도덕성이 진화적으로 준비된 "
                "여섯 가지 기초(배려/피해, 공정/속임, 충성/배신, 권위/전복, 신성/타락, 자유/억압) 위에 세워진다고 본다. "
                "진보주의자와 보수주의자의 도덕 차이를 이 기반들의 강조 비율 차이로 설명한다."
            ),
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "related_terms": ["배려/피해", "공정/속임", "충성/배신", "권위/전복", "신성/타락", "자유/억압", "nativism"]
        },
        {
            "id": "kw-elephant-and-rider",
            "term": "코끼리와 기수",
            "term_en": "Elephant and Rider",
            "definition": (
                "하이트가 인간 심리의 이중 구조를 설명하는 비유. "
                "코끼리는 감정, 직관, 자동적 처리를, 기수는 이성적 추론을 상징한다. "
                "코끼리(직관)가 방향을 결정하면 기수(이성)는 이를 따르며 합리화한다. "
                "도덕 판단에서 직관의 주도적 역할을 강조한다."
            ),
            "thinker_id": "haidt",
            "work_id": "haidt-happiness-hypothesis",
            "related_terms": ["사회적 직관주의", "이중처리 이론", "직관", "자동 처리"]
        },
        {
            "id": "kw-moral-dumbfounding",
            "term": "도덕적 무성어화",
            "term_en": "Moral Dumbfounding",
            "definition": (
                "하이트가 명명한 현상으로, 사람들이 왜 특정 행위가 도덕적으로 잘못인지 "
                "설명하지 못하면서도 그 판단을 강하게 유지하는 것을 말한다. "
                "예: 피해자 없는 근친상간 시나리오. 도덕 판단이 추론이 아닌 직관에 기반함을 보여준다."
            ),
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "related_terms": ["사회적 직관주의", "직관", "도덕 판단"]
        },
        {
            "id": "kw-weird-bias",
            "term": "WEIRD 편향",
            "term_en": "WEIRD Bias (Western, Educated, Industrialized, Rich, Democratic)",
            "definition": (
                "서양, 교육받은, 산업화된, 부유한, 민주적 사회의 도덕 감각을 보편적인 것으로 오해하는 편향. "
                "하이트는 콜버그의 도덕발달론과 서양 도덕철학이 WEIRD 편향에 빠져 있다고 비판한다. "
                "비서양 문화의 공동체·권위·신성 기반 도덕을 열등하게 취급한다."
            ),
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "related_terms": ["도덕기반이론", "문화 편향", "콜버그 비판", "보편 도덕"]
        },
        {
            "id": "kw-care-harm",
            "term": "배려/피해",
            "term_en": "Care/Harm",
            "definition": (
                "도덕기반이론의 첫 번째 기반. 취약한 존재를 보호하고 고통을 피하려는 "
                "진화적 직관. 공감과 연민의 감정과 연결되며, 진보주의 도덕 체계에서 핵심적이다."
            ),
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "related_terms": ["도덕기반이론", "공감", "연민", "진보 도덕"]
        },
        {
            "id": "kw-fairness-cheating",
            "term": "공정/속임",
            "term_en": "Fairness/Cheating",
            "definition": (
                "도덕기반이론의 두 번째 기반. 협력과 상호 이익에서 진화한 도덕 기반으로, "
                "정의, 권리, 자율성과 연결된다. 배신자 탐지와 상호호혜성에 민감한 직관이다."
            ),
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "related_terms": ["도덕기반이론", "정의", "권리", "상호호혜"]
        },
        {
            "id": "kw-loyalty-betrayal",
            "term": "충성/배신",
            "term_en": "Loyalty/Betrayal",
            "definition": (
                "도덕기반이론의 세 번째 기반. 연합 집단 형성에서 진화한 도덕 기반으로, "
                "집단 충성심, 자기희생, 배신자에 대한 혐오와 연결된다. "
                "보수주의 도덕 체계에서 강하게 강조된다."
            ),
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "related_terms": ["도덕기반이론", "집단 결속", "보수 도덕"]
        },
        {
            "id": "kw-authority-subversion",
            "term": "권위/전복",
            "term_en": "Authority/Subversion",
            "definition": (
                "도덕기반이론의 네 번째 기반. 위계적 사회 구조에서 진화한 도덕 기반으로, "
                "존경, 전통, 리더십 복종과 연결된다. "
                "보수주의 도덕에서 강하게 강조되며, 권위에 대한 도전을 도덕적 위반으로 본다."
            ),
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "related_terms": ["도덕기반이론", "전통", "위계", "보수 도덕"]
        },
        {
            "id": "kw-sanctity-degradation",
            "term": "신성/타락",
            "term_en": "Sanctity/Degradation",
            "definition": (
                "도덕기반이론의 다섯 번째 기반. 병원체 회피에서 진화한 도덕 기반으로, "
                "혐오(disgust) 감정, 순수함, 신성함과 연결된다. "
                "종교적 도덕과 보수주의 도덕에서 강하게 나타난다."
            ),
            "thinker_id": "haidt",
            "work_id": "haidt-righteous-mind",
            "related_terms": ["도덕기반이론", "혐오", "신성", "종교 도덕", "보수 도덕"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """하이트 관련 사상가 관계 데이터 입력."""
    relations = [
        {
            "from_thinker": "kohlberg",
            "to_thinker": "haidt",
            "type": "criticized",
            "description": (
                "하이트는 콜버그의 합리주의적 도덕발달론을 비판적으로 계승했다. "
                "콜버그의 도덕 발달 단계론에서 출발하면서도, "
                "도덕 판단이 추론이 아닌 직관에서 비롯된다는 점을 강조하며 콜버그 모델의 근본 가정을 뒤집었다. "
                "또한 콜버그가 도덕을 정의·공정 중심으로 좁게 정의하여 다른 도덕 기반을 무시했다고 비판했다."
            ),
            "evidence": "The Righteous Mind, Part 1 — 콜버그 모델 비판 전반"
        },
        {
            "from_thinker": "hume",
            "to_thinker": "haidt",
            "type": "influenced",
            "description": (
                "흄의 감정주의 도덕론이 하이트의 직관주의에 직접적 영향을 주었다. "
                "흄은 '이성은 열정의 노예'라고 주장하여 도덕 판단에서 감정의 우선성을 강조했다. "
                "하이트는 이를 계승하여 직관(감정)이 추론보다 앞선다는 사회적 직관주의 모델을 발전시켰다."
            ),
            "evidence": "The Righteous Mind, Part 1: Chapter 2 — 흄 인용 및 계승"
        },
        {
            "from_thinker": "piaget",
            "to_thinker": "haidt",
            "type": "criticized",
            "description": (
                "하이트는 피아제의 인지발달 중심 도덕발달론을 비판했다. "
                "피아제는 도덕 발달을 인지 발달(자기중심성 극복, 추론 능력 향상)의 결과로 보았으나, "
                "하이트는 도덕성이 주로 직관·감정에 기반하며 추론은 사후적 역할을 한다고 반론했다. "
                "또한 피아제의 연구가 WEIRD 편향을 담고 있다고 비판했다."
            ),
            "evidence": "The Righteous Mind, Part 1 — 피아제 모델 비판"
        },
        {
            "from_thinker": "haidt",
            "to_thinker": "kohlberg",
            "type": "criticized",
            "description": (
                "하이트가 콜버그의 도덕발달론을 직접 비판했다. "
                "콜버그가 도덕을 정의/공정 기반으로 좁게 정의했으며, "
                "합리주의적 가정(도덕 판단은 추론의 산물)이 실제 도덕 심리와 다르다고 주장했다. "
                "콜버그의 연구가 WEIRD 표본에 편향되어 보편성을 주장할 수 없다고 비판했다."
            ),
            "evidence": "The Righteous Mind, Chapter 3, Part 2: WEIRD 비판"
        }
    ]

    for rel in relations:
        rel_id = f"{rel['from_thinker']}-{rel['type']}-{rel['to_thinker']}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id}: {result['result']}")

    return len(relations)


def main():
    """메인 실행 함수."""
    print("=== 조너선 하이트(Jonathan Haidt) 데이터 ES 입력 시작 ===\n")

    client = get_client()

    try:
        # 1. 분야 확인
        print("[1/6] 분야 확인 및 생성...")
        ensure_field(client)
        print()

        # 2. 사상가 입력
        print("[2/6] 사상가 데이터 입력...")
        insert_thinker(client)
        print()

        # 3. 저서 입력
        print("[3/6] 저서 데이터 입력...")
        works_count = insert_works(client)
        print(f"     → {works_count}개 저서 입력 완료\n")

        # 4. 주장 입력
        print("[4/6] 주장 데이터 입력...")
        claims_count = insert_claims(client)
        print(f"     → {claims_count}개 주장 입력 완료\n")

        # 5. 키워드 입력
        print("[5/6] 키워드 데이터 입력...")
        kw_count = insert_keywords(client)
        print(f"     → {kw_count}개 키워드 입력 완료\n")

        # 6. 관계 입력
        print("[6/6] 관계 데이터 입력...")
        rel_count = insert_relations(client)
        print(f"     → {rel_count}개 관계 입력 완료\n")

        print("=== 입력 완료 요약 ===")
        print(f"  - 사상가: 1명 (haidt)")
        print(f"  - 저서: {works_count}개")
        print(f"  - 주장: {claims_count}개")
        print(f"  - 키워드: {kw_count}개")
        print(f"  - 관계: {rel_count}개")
        print("\n✓ 조너선 하이트 데이터 ES 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
