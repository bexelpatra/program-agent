"""존 스튜어트 밀(John Stuart Mill) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS
)


def insert_thinker(client):
    """밀 사상가 데이터 입력."""
    doc = {
        "id": "mill_js",
        "name": "존 스튜어트 밀",
        "name_en": "John Stuart Mill",
        "field": "western_ethics",
        "era": "근대 영국",
        "birth_year": 1806,
        "death_year": 1873,
        "background": (
            "런던 펜톤빌(Pentonville)에서 철학자 제임스 밀(James Mill)의 장남으로 태어났다. "
            "아버지의 엄격한 교육 방침 아래 3세에 그리스어, 8세에 라틴어를 배웠으며, "
            "13세에 정치경제학을 체계적으로 공부했다. "
            "학교 교육 없이 아버지와 제러미 벤담의 지도 하에 교육받았으며, "
            "20세에 심각한 정신적 위기(mental crisis)를 겪으면서 순수한 양적 공리주의의 한계를 자각하고 "
            "워즈워스의 시와 낭만주의에서 회복의 실마리를 찾았다. "
            "동인도 회사에서 35년간 근무하며 철학·정치 저술 활동을 병행했고, "
            "1865~68년 하원의원으로 활동하며 여성 참정권을 최초로 의회에서 제안했다. "
            "해리엇 테일러(Harriet Taylor)와의 정신적 교류와 후의 결혼은 그의 사상, "
            "특히 여성 해방론에 깊은 영향을 미쳤다."
        ),
        "core_philosophy": (
            "벤담의 양적 공리주의를 계승하되 쾌락의 질적 차이를 도입하여 '질적 공리주의'를 완성했다. "
            "'배부른 돼지보다 불만족한 소크라테스가 낫다'는 명제로 대표되듯, "
            "정신적·지적 쾌락이 육체적 쾌락보다 질적으로 우월함을 주장했다. "
            "또한 자유론에서 '해악 원리(Harm Principle)'를 제시하여, "
            "타인에게 해를 끼치지 않는 한 개인의 자유는 어떤 이유로도 침해될 수 없다고 주장했다. "
            "공리주의와 자유주의를 결합한 자유지상주의적 공리주의를 체계화했으며, "
            "여성 해방, 대의민주주의, 귀납적 논리학 분야에서도 중요한 업적을 남겼다."
        ),
        "philosophical_journey": (
            "초기(1820s~1830s): 아버지와 벤담의 영향 아래 급진적 공리주의자로 출발했다. "
            "1826년 정신적 위기를 겪으며 순수한 양적 공리주의가 인간 내면의 감정과 문화적 가치를 "
            "충분히 설명하지 못함을 자각했다. "
            "중기(1840s~1860s): 낭만주의, 콜리지, 생시몽 사상과의 만남을 통해 공리주의를 재구성했다. "
            "1843년 논리학 체계로 귀납적 방법론을 확립하고, "
            "1848년 정치경제학 원리로 고전파 경제학을 집대성했다. "
            "1859년 자유론, 1861년 공리주의와 대의정부론을 출판하며 사상의 완성기에 이르렀다. "
            "말년(1860s~1873): 여성의 종속(1869)으로 성평등 논의의 선구가 되었으며, "
            "사후 출판된 자서전에서 자신의 지적 여정을 회고했다."
        ),
        "keywords": [
            "질적 공리주의",
            "해악 원리",
            "최대 다수의 최대 행복",
            "역량 있는 판단자",
            "자유의 세 영역",
            "대의민주주의",
            "귀납법",
            "여성 해방"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="mill_js", document=doc)
    print(f"[thinker] mill_js: {result['result']}")
    return result


def insert_works(client):
    """밀 저서 데이터 입력."""
    works = [
        {
            "id": "mill-utilitarianism",
            "thinker_id": "mill_js",
            "title": "공리주의",
            "title_original": "Utilitarianism",
            "year": 1863,
            "significance": (
                "밀의 공리주의 윤리학을 집대성한 핵심 저작. "
                "벤담의 양적 공리주의를 비판·계승하여 쾌락의 질적 차이를 도입했다. "
                "역량 있는 판단자 기준, 공리주의의 증명, 정의와 공리의 관계를 논한다. "
                "임용시험에서 가장 중요하게 다루어지는 밀의 저서이다."
            ),
            "key_concepts": [
                "질적 공리주의", "역량 있는 판단자", "공리주의의 증명",
                "정의와 공리", "내적 제재", "최대 행복 원리"
            ]
        },
        {
            "id": "mill-on-liberty",
            "thinker_id": "mill_js",
            "title": "자유론",
            "title_original": "On Liberty",
            "year": 1859,
            "significance": (
                "자유주의 정치철학의 고전. 해악 원리(Harm Principle)를 제시하여 "
                "개인 자유와 사회 권위의 한계를 논하는 밀의 대표 저작이다. "
                "자유의 세 영역, 사상과 토론의 자유, 반다수결주의를 다루며, "
                "현대 자유주의 정치철학의 기초를 닦았다."
            ),
            "key_concepts": [
                "해악 원리", "자유의 세 영역", "사상과 토론의 자유",
                "개성의 자유", "반다수결주의", "실험적 삶의 방식"
            ]
        },
        {
            "id": "mill-subjection-of-women",
            "thinker_id": "mill_js",
            "title": "여성의 종속",
            "title_original": "The Subjection of Women",
            "year": 1869,
            "significance": (
                "19세기 페미니즘의 선구적 저작. 여성에 대한 법적·사회적 종속이 "
                "경험적 근거 없이 전통과 편견에만 의존한다고 비판하고, "
                "성 평등이 사회 전체의 공리에 기여함을 논증했다. "
                "여성 참정권 운동의 이론적 토대를 마련했다."
            ),
            "key_concepts": [
                "성평등", "여성 해방", "공리주의적 페미니즘",
                "자의적 차별", "법적 종속", "여성 참정권"
            ]
        },
        {
            "id": "mill-considerations-representative-government",
            "thinker_id": "mill_js",
            "title": "대의정부론",
            "title_original": "Considerations on Representative Government",
            "year": 1861,
            "significance": (
                "밀의 정치철학을 집대성한 저작. 대의민주주의가 이상적 정부 형태임을 논증하고, "
                "비례대표제, 복수 투표제, 비밀투표 반대 등 구체적 제도 설계를 제안했다. "
                "민주주의의 위험으로 다수결의 횡포와 교육받지 못한 대중의 정치 참여를 지적했다."
            ),
            "key_concepts": [
                "대의민주주의", "비례대표제", "복수 투표제",
                "다수결의 횡포", "시민 참여", "정치적 교육"
            ]
        },
        {
            "id": "mill-system-of-logic",
            "thinker_id": "mill_js",
            "title": "논리학 체계",
            "title_original": "A System of Logic",
            "year": 1843,
            "significance": (
                "경험주의 논리학과 귀납법의 방법론을 체계화한 저작. "
                "연역적 삼단논법의 한계를 비판하고, 자연과학의 방법론인 귀납법이 "
                "지식의 진정한 원천임을 논증했다. 밀의 귀납법 다섯 가지 원칙이 소개된다."
            ),
            "key_concepts": [
                "귀납법", "삼단논법 비판", "경험주의", "인과관계",
                "밀의 귀납법 5원칙", "과학적 방법론"
            ]
        },
        {
            "id": "mill-principles-of-political-economy",
            "thinker_id": "mill_js",
            "title": "정치경제학 원리",
            "title_original": "Principles of Political Economy",
            "year": 1848,
            "significance": (
                "고전파 경제학을 집대성한 저작으로, 리카도 경제학을 계승·발전시켰다. "
                "생산과 분배의 법칙을 구분하여 분배는 사회 제도에 의해 변경 가능함을 주장하고, "
                "노동자 협동조합과 토지 개혁을 지지하는 자유주의적 사회주의 노선을 취했다."
            ),
            "key_concepts": [
                "고전파 경제학", "생산과 분배", "노동자 협동조합",
                "자유주의적 사회주의", "토지 개혁", "경제적 자유"
            ]
        },
        {
            "id": "mill-autobiography",
            "thinker_id": "mill_js",
            "title": "자서전",
            "title_original": "Autobiography",
            "year": 1873,
            "significance": (
                "밀의 지적·정신적 성장 과정을 기록한 자서전. 사후 출판되었다. "
                "아버지의 엄격한 교육, 1826년의 정신적 위기, 해리엇 테일러와의 관계, "
                "공리주의에서 자유주의적 공리주의로의 사상적 전환 과정을 상세히 기술한다."
            ),
            "key_concepts": [
                "정신적 위기", "지적 전기", "해리엇 테일러",
                "사상 형성", "교육론", "공리주의 전환"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """밀 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 질적 공리주의 — 쾌락의 질적 차이
        {
            "id": "mill-claim-001",
            "thinker_id": "mill_js",
            "work_id": "mill-utilitarianism",
            "source_detail": "Utilitarianism, Ch.2",
            "claim": "쾌락에는 질적 차이가 있으며, 정신적 쾌락은 육체적 쾌락보다 질적으로 우월하다.",
            "original_text": (
                "It is better to be Socrates dissatisfied than a fool satisfied. "
                "And if the fool, or the pig, are of a different opinion, it is because "
                "they only know their own side of the question."
            ),
            "original_text_ko": (
                "만족한 바보보다 불만족한 소크라테스가 낫다. "
                "그리고 만약 바보나 돼지가 다른 의견을 가진다면, "
                "그것은 그들이 문제의 자기 쪽 면만 알기 때문이다."
            ),
            "explanation": (
                "밀은 벤담의 양적 공리주의를 수정하여 쾌락에 질적 차이가 있음을 주장했다. "
                "모든 쾌락이 양적으로만 다르다고 본 벤담과 달리, 밀은 지적·정신적 쾌락이 "
                "육체적 쾌락보다 질적으로 우월하다고 보았다. "
                "'배부른 돼지보다 불만족한 소크라테스'라는 표현은 이를 가장 잘 나타낸다."
            ),
            "argument": (
                "밀의 논거는 다음과 같다: (1) 두 쾌락을 모두 경험한 사람들, "
                "즉 '역량 있는 판단자(competent judges)'들은 일관되게 정신적 쾌락을 선호한다. "
                "(2) 이 선호는 단순히 양적으로 더 크기 때문이 아니라, "
                "질적으로 더 뛰어나기 때문이다. "
                "(3) 인간 능력 중 고차적인 능력(이성, 감정, 상상)이 있으며, "
                "이 능력의 발휘에서 오는 쾌락이 더 높은 가치를 가진다. "
                "(4) 따라서 '역량 있는 판단자의 판단'이 쾌락의 질적 우열의 기준이 된다."
            ),
            "counterpoint": (
                "헨리 시지윅(Henry Sidgwick)은 '윤리학의 방법들'(The Methods of Ethics, 1874)에서 "
                "밀의 질적 차이 주장이 공리주의 내부의 논리적 일관성을 깨뜨린다고 비판했다. "
                "만약 쾌락의 질이 양과 독립적이라면, 결국 쾌락의 총량 극대화라는 공리주의의 "
                "핵심 계산 원리가 성립할 수 없다는 것이다. "
                "또한 벤담(Jeremy Bentham)은 '도덕과 입법의 원리 서론'(1789)에서 "
                "쾌락의 종류 간 질적 우열을 인정하지 않고 오직 양적 차이만을 주장했으며, "
                "이는 밀의 수정이 공리주의의 원래 정신에서 이탈임을 시사한다."
            ),
            "context": (
                "벤담의 공리주의는 '핀 게임과 시 짓기는 동등하다'는 식으로 "
                "모든 쾌락을 동등하게 취급했다. 밀은 이것이 인간의 고차적 능력을 무시하며, "
                "공리주의가 '돼지의 철학'이라는 비판에 취약하다고 보아 질적 차이를 도입했다."
            ),
            "keywords": ["질적 공리주의", "역량 있는 판단자", "정신적 쾌락", "고차 쾌락"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-002: 역량 있는 판단자
        {
            "id": "mill-claim-002",
            "thinker_id": "mill_js",
            "work_id": "mill-utilitarianism",
            "source_detail": "Utilitarianism, Ch.2",
            "claim": "쾌락의 질적 우열은 두 쾌락을 모두 경험한 역량 있는 판단자의 선호에 의해 결정된다.",
            "original_text": (
                "Of two pleasures, if there be one to which all or almost all who have experience "
                "of both give a decided preference... that is the more desirable pleasure."
            ),
            "original_text_ko": (
                "두 쾌락 중에서, 두 가지 모두를 경험한 사람들의 전부 또는 거의 전부가 "
                "결정적인 선호를 보이는 것이... 더 바람직한 쾌락이다."
            ),
            "explanation": (
                "밀은 쾌락의 질적 우열을 판단하는 기준으로 '역량 있는 판단자'를 제시했다. "
                "역량 있는 판단자란 비교 대상인 두 쾌락을 모두 충분히 경험하여 "
                "그 차이를 알 수 있는 사람을 뜻한다. "
                "이들의 일관된 선호가 어떤 쾌락이 더 가치 있는지를 결정하는 기준이 된다."
            ),
            "argument": (
                "밀의 논거: (1) 쾌락의 질적 우열은 객관적 척도 없이 판단하기 어렵다. "
                "(2) 그러나 두 쾌락을 모두 경험한 사람은 어느 쪽이 더 가치 있는지 판단할 수 있다. "
                "(3) 단 한 쪽 쾌락만 아는 사람은 비교 판단의 자격이 없다 "
                "(돼지나 바보가 자신의 쾌락을 선호하는 이유). "
                "(4) 역량 있는 판단자들의 일관된 선호는 단순히 개인적 취향이 아닌, "
                "인간 능력의 고차적 발휘에 대한 공통 인식을 반영한다."
            ),
            "counterpoint": (
                "제이 그리핀(James Griffin)은 '웰빙'(Well-Being, 1986)에서 "
                "역량 있는 판단자 기준이 순환 논리에 빠진다고 비판했다. "
                "'고차 쾌락을 선호하는 사람'을 역량 있는 판단자로 정의하면, "
                "이 기준으로 고차 쾌락이 더 낫다고 증명하는 것은 순환 논증이 된다는 것이다. "
                "또한 롤스(John Rawls)는 '정의론'(A Theory of Justice, 1971)에서 "
                "선호에 기반한 기준이 역사적으로 형성된 적응적 선호를 반영할 뿐이라고 비판했다."
            ),
            "context": (
                "벤담의 쾌락 계산은 강도·지속성 등 양적 기준만을 사용했다. "
                "밀은 이 기준이 인간 능력의 차이를 반영하지 못한다고 보고, "
                "경험에 기반한 판단자 기준을 도입했다."
            ),
            "keywords": ["역량 있는 판단자", "경험적 기준", "쾌락의 질", "선호"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-003: 공리 원리
        {
            "id": "mill-claim-003",
            "thinker_id": "mill_js",
            "work_id": "mill-utilitarianism",
            "source_detail": "Utilitarianism, Ch.2",
            "claim": "공리의 원리(최대 행복 원리)는 행복을 극대화하는 행위가 도덕적으로 옳다고 규정한다.",
            "original_text": (
                "The creed which accepts as the foundation of morals 'utility' or the 'greatest happiness principle' "
                "holds that actions are right in proportion as they tend to promote happiness; "
                "wrong as they tend to produce the reverse of happiness."
            ),
            "original_text_ko": (
                "'공리' 또는 '최대 행복 원리'를 도덕의 토대로 받아들이는 신조는 "
                "행위가 행복을 증진하는 경향에 비례하여 옳고, "
                "행복의 반대를 산출하는 경향에 비례하여 그르다고 주장한다."
            ),
            "explanation": (
                "밀은 벤담의 최대 행복 원리를 계승하면서도 질적 공리주의로 수정했다. "
                "행복은 쾌락과 고통의 부재로 이루어지며, 이를 극대화하는 것이 도덕의 기준이다. "
                "단 밀의 행복 개념은 벤담의 순수한 쾌락이 아닌, "
                "질적으로 차등화된 쾌락의 총합이다."
            ),
            "argument": (
                "밀의 논거: (1) 모든 인간은 자신의 행복을 추구한다는 경험적 사실. "
                "(2) 각자의 행복이 각자에게 선(good)이라면, 전체의 행복은 전체에게 선이다. "
                "(3) 따라서 '모든 사람의 행복의 총합'이 도덕의 기준이 되어야 한다. "
                "(4) 도덕적 행위는 이 총합을 증가시키는 행위이고, "
                "비도덕적 행위는 감소시키는 행위이다."
            ),
            "counterpoint": (
                "칸트(Immanuel Kant)는 '도덕 형이상학의 기초'(Groundwork, 1785)에서 "
                "결과보다 동기의 순수성이 도덕성의 기준이 되어야 한다고 비판했다. "
                "최대 행복을 목표로 한다면 소수의 희생이 다수의 행복을 위해 정당화될 수 있으며, "
                "이는 인간을 수단으로 취급하는 것이다. "
                "롤스(John Rawls)는 '정의론'(1971)에서 공리주의가 "
                "개인의 권리를 전체 공리에 희생시킬 위험이 있다고 비판했다."
            ),
            "context": (
                "19세기 영국에서 공리주의는 법·사회 개혁의 이론적 토대였다. "
                "밀은 이 원리를 정교화하여 단순한 쾌락 계산이 아닌 인간의 번영(flourishing)을 "
                "포함하는 더 풍부한 행복 개념으로 발전시켰다."
            ),
            "keywords": ["공리의 원리", "최대 행복 원리", "행복 극대화", "쾌락과 고통"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-004: 공리주의의 증명
        {
            "id": "mill-claim-004",
            "thinker_id": "mill_js",
            "work_id": "mill-utilitarianism",
            "source_detail": "Utilitarianism, Ch.4",
            "claim": "행복이 바람직하다는 것은, 모든 사람이 실제로 행복을 욕구한다는 사실로부터 증명된다.",
            "original_text": (
                "The only proof capable of being given that an object is visible is that people actually see it. "
                "The only proof that a sound is audible is that people hear it... "
                "In like manner, I apprehend, the sole evidence it is possible to produce that anything is desirable "
                "is that people do actually desire it."
            ),
            "original_text_ko": (
                "어떤 것이 가시적임을 증명할 수 있는 유일한 증거는 사람들이 실제로 그것을 본다는 것이다. "
                "소리가 들린다는 것을 증명하는 유일한 증거는 사람들이 그것을 듣는다는 것이다... "
                "마찬가지로, 나는 어떤 것이 바람직하다는 것을 증명할 수 있는 유일한 증거는 "
                "사람들이 실제로 그것을 욕구한다는 것이라고 이해한다."
            ),
            "explanation": (
                "밀은 공리주의 원리를 '증명'하려 했다. 그 증명 방식은 유비적이다: "
                "어떤 것이 가시적이라는 증거가 실제로 보인다는 사실이듯, "
                "행복이 바람직하다는 증거는 사람들이 실제로 행복을 욕구한다는 사실이다. "
                "각자가 자신의 행복을 욕구하므로, 집합적으로 전체 행복이 집합적으로 욕구된다."
            ),
            "argument": (
                "밀의 논거: (1) 경험적으로 볼 때, 모든 사람은 자신의 행복을 욕구한다. "
                "(2) 욕구된 것은 욕구하는 자에게 선(good)이다. "
                "(3) 따라서 각자의 행복은 그 사람에게 선이다. "
                "(4) 각 사람의 행복이 그 사람에게 선이라면, "
                "모든 사람의 행복은 모든 사람에게 선 — 즉 도덕적 선 — 이다."
            ),
            "counterpoint": (
                "G.E. 무어(G.E. Moore)는 '윤리학 원리'(Principia Ethica, 1903)에서 "
                "이를 '자연주의적 오류(naturalistic fallacy)'의 전형적 사례로 비판했다. "
                "'욕구됨'(is desired)에서 '바람직함'(is desirable)을 도출하는 것은 "
                "사실(is)에서 가치(ought)를 도출하는 잘못된 추론이라는 것이다. "
                "또한 헨리 시지윅(Henry Sidgwick)은 '윤리학의 방법들'(1874)에서 "
                "각자가 자신의 행복을 욕구함으로부터 전체 행복이 바람직하다는 결론이 "
                "논리적으로 도출되지 않는다고(합성의 오류) 비판했다."
            ),
            "context": (
                "밀은 도덕 원리가 수학적 증명 방식으로는 증명될 수 없지만, "
                "경험적 증거에 의해 뒷받침될 수 있다고 생각했다. "
                "이 장은 공리주의 윤리학의 기초를 정당화하려는 시도이며, "
                "동시에 가장 많은 철학적 비판을 받은 부분이기도 하다."
            ),
            "keywords": ["공리주의의 증명", "자연주의적 오류", "바람직함", "욕구"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-005: 해악 원리
        {
            "id": "mill-claim-005",
            "thinker_id": "mill_js",
            "work_id": "mill-on-liberty",
            "source_detail": "On Liberty, Ch.1",
            "claim": "사회가 개인의 자유를 합법적으로 제한할 수 있는 유일한 근거는 타인에 대한 해악 방지이다(해악 원리).",
            "original_text": (
                "The only purpose for which power can be rightfully exercised over any member "
                "of a civilised community, against his will, is to prevent harm to others. "
                "His own good, either physical or moral, is not a sufficient warrant."
            ),
            "original_text_ko": (
                "문명 사회의 어떤 구성원에 대해 그의 의사에 반하여 권력을 정당하게 행사할 수 있는 "
                "유일한 목적은 타인에 대한 해악을 방지하는 것이다. "
                "그 자신의 신체적 또는 도덕적 선은 충분한 근거가 되지 않는다."
            ),
            "explanation": (
                "자유론의 핵심 원리인 '해악 원리(Harm Principle)'이다. "
                "개인의 자유는 타인에게 해를 끼치지 않는 한 어떤 이유로도 침해될 수 없다. "
                "자신만을 해치는 행위(자해 행위)는 사회가 간섭할 권리가 없으며, "
                "이는 자유주의적 정치의 핵심 원칙이다."
            ),
            "argument": (
                "밀의 논거: (1) 개인은 자기 자신의 주인이다. "
                "자신에게만 영향을 미치는 행위에 대해 사회가 간섭하는 것은 개인 주권 침해이다. "
                "(2) 사상의 자유와 실험적 삶의 방식은 사회 진보를 위해 필수적이다. "
                "다양한 생활 방식이 허용되어야 최선의 방식이 무엇인지 발견할 수 있다. "
                "(3) 공리주의적 관점에서도 장기적으로 자유가 허용된 사회가 더 큰 공리를 달성한다. "
                "(4) 간섭주의(paternalism)는 개인의 행복에 대해 개인 자신보다 사회가 더 잘 안다고 "
                "가정하는데, 이는 대개 틀린 가정이다."
            ),
            "counterpoint": (
                "패트릭 데블린(Patrick Devlin)은 '도덕의 집행'(The Enforcement of Morals, 1965)에서 "
                "사회는 그 도덕적 구조를 지키기 위해 개인의 행동을 규제할 수 있다고 주장하며 "
                "해악 원리를 비판했다. 사회 응집력을 해치는 행위는 '해악'이 될 수 있다는 것이다. "
                "또한 Joel Feinberg는 '해악 원리'(Harm to Others, 1984)에서 "
                "해악의 개념 자체가 모호하며, 간접적 해악의 경우 원리의 적용 범위가 불명확해진다고 비판했다."
            ),
            "context": (
                "19세기 영국에서는 음주, 안식일 준수, 성적 도덕에 대한 법적 규제 논쟁이 활발했다. "
                "밀은 이러한 도덕적 간섭주의에 반대하여 자유의 경계선을 명확히 제시했다."
            ),
            "keywords": ["해악 원리", "개인 자유", "간섭 금지", "자유주의"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-006: 자유의 세 영역
        {
            "id": "mill-claim-006",
            "thinker_id": "mill_js",
            "work_id": "mill-on-liberty",
            "source_detail": "On Liberty, Ch.1",
            "claim": "개인의 자유에는 세 가지 영역이 있다: 내면적 자유, 취향과 추구의 자유, 결사의 자유.",
            "original_text": (
                "This, then, is the appropriate region of human liberty. "
                "It comprises, first, the inward domain of consciousness... "
                "Secondly, the principle requires liberty of tastes and pursuits... "
                "Thirdly, from this liberty of each individual follows the liberty... "
                "of combination among individuals."
            ),
            "original_text_ko": (
                "이것이 바로 인간 자유의 적절한 영역이다. "
                "첫째, 의식의 내면적 영역... "
                "둘째, 이 원리는 취향과 추구의 자유를 요구한다... "
                "셋째, 각 개인의 이러한 자유로부터 개인들 간의 결합의 자유가 따라온다."
            ),
            "explanation": (
                "밀은 해악 원리가 보호하는 자유의 영역을 세 가지로 구분했다. "
                "첫째, 내면적 자유: 의식·사상·감정·의견의 자유, 종교·도덕·정치적 의견에서의 절대적 자유. "
                "둘째, 취향과 추구의 자유: 자신의 삶의 방식을 선택할 자유, "
                "타인의 승인 없이 자신의 계획대로 살 자유. "
                "셋째, 결사의 자유: 타인에게 해를 끼치지 않는 한 어떤 목적으로도 단결할 자유."
            ),
            "argument": (
                "밀의 논거: (1) 내면적 자유는 인간의 사상 발전을 위해 절대적으로 필요하다. "
                "사상의 자유가 없으면 진리가 발견되지 않고, 사회 진보가 멈춘다. "
                "(2) 취향의 자유는 인간 개성(individuality)의 발전을 위해 필수적이다. "
                "개성이 발현될 때 인간은 자신의 능력을 최대로 계발하고, "
                "이것이 결국 사회 전체의 공리에 기여한다. "
                "(3) 결사의 자유는 위 두 자유에서 자연스럽게 도출된다."
            ),
            "counterpoint": (
                "이사야 벌린(Isaiah Berlin)은 '자유의 두 개념'(Two Concepts of Liberty, 1958)에서 "
                "밀의 자유 개념을 '소극적 자유(negative liberty)'로 분류하면서, "
                "이것만으로는 실질적 자유를 보장하기 어렵다고 비판했다. "
                "경제적 불평등으로 인해 선택 능력이 없는 사람에게는 형식적 자유가 무의미하다는 것이다. "
                "찰스 테일러(Charles Taylor)는 '무엇이 잘못되었는가'(What's Wrong with Negative Liberty, 1979)에서 "
                "소극적 자유 개념이 자기실현을 위한 조건을 무시한다고 비판했다."
            ),
            "context": (
                "밀은 자유의 영역을 명확히 함으로써, 국가와 사회가 어디까지 간섭할 수 있고 "
                "어디서부터는 간섭해서는 안 되는지의 경계를 제시하려 했다."
            ),
            "keywords": ["자유의 세 영역", "내면적 자유", "취향의 자유", "결사의 자유"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-007: 사상과 토론의 자유
        {
            "id": "mill-claim-007",
            "thinker_id": "mill_js",
            "work_id": "mill-on-liberty",
            "source_detail": "On Liberty, Ch.2",
            "claim": "사상과 토론의 자유는 절대적으로 보장되어야 한다. 침묵당한 의견이 진리일 수 있으며, 설령 오류라도 진리를 더 명확히 한다.",
            "original_text": (
                "If all mankind minus one were of one opinion, mankind would be no more justified "
                "in silencing that one person than he, if he had the power, would be justified "
                "in silencing mankind."
            ),
            "original_text_ko": (
                "만약 인류에서 한 사람을 제외한 모두가 하나의 의견을 가지고 있다면, "
                "인류가 그 한 사람을 침묵시키는 것은, 그 사람이 권력을 가졌을 때 "
                "인류를 침묵시키는 것보다 더 정당하지 않다."
            ),
            "explanation": (
                "밀은 사상과 토론의 자유를 가장 중요한 자유로 보았다. "
                "어떤 의견을 침묵시키는 것이 잘못인 이유는 네 가지이다: "
                "(1) 침묵당한 의견이 진리일 수 있다. "
                "(2) 설령 오류라도, 진리와 오류의 충돌이 진리를 더 명확히 한다. "
                "(3) 오래된 진리도 도전받지 않으면 살아있는 확신이 아닌 죽은 도그마가 된다. "
                "(4) 진리의 일부는 반대 의견 속에 포함되어 있을 수 있다."
            ),
            "argument": (
                "밀의 논거: (1) 인간은 오류 가능하다. 어떤 권위도 절대적으로 옳다고 단정할 수 없으므로, "
                "이단적 의견을 억압하는 것은 자신의 무오류성을 가정하는 것이다. "
                "(2) 역사적으로 많은 진리가 처음에는 소수 의견이었다 "
                "(소크라테스, 갈릴레이, 종교 개혁자들의 예). "
                "(3) 사상의 자유로운 시장에서 진리는 결국 오류를 이긴다. "
                "(4) 적극적 반론 없이 유지되는 믿음은 그 근거를 이해하지 못하는 죽은 도그마에 불과하다."
            ),
            "counterpoint": (
                "알렉산더 미클존(Alexander Meiklejohn)은 언론의 자유가 "
                "자기통치(self-governance)에 필요한 공적 토론에만 절대적으로 적용되며, "
                "사적 발언에는 제한이 가능하다고 주장하여 밀의 절대적 자유론을 한정했다. "
                "또한 캐스 선스타인(Cass Sunstein)은 '공화국.com'(Republic.com, 2001)에서 "
                "인터넷 시대의 반향실(echo chamber) 효과가 밀이 상정한 "
                "'사상의 자유로운 시장'이 실제로 작동하지 않음을 보여준다고 비판했다."
            ),
            "context": (
                "19세기 영국에서는 신성 모독죄, 선동죄 등으로 언론이 억압받았다. "
                "밀은 이러한 표현 억압이 사회 진보를 방해한다고 보아 "
                "사상과 토론의 절대적 자유를 주장했다."
            ),
            "keywords": ["사상의 자유", "토론의 자유", "소수 의견", "표현의 자유"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-008: 개성과 자유지상주의
        {
            "id": "mill-claim-008",
            "thinker_id": "mill_js",
            "work_id": "mill-on-liberty",
            "source_detail": "On Liberty, Ch.3",
            "claim": "개성(individuality)의 자유로운 발전은 공리를 위해서도 필수적이며, 자유 그 자체가 공리에 기여한다.",
            "original_text": (
                "He who lets the world, or his own portion of it, choose his plan of life for him, "
                "has no need of any other faculty than the ape-like one of imitation... "
                "Among the works of man, which human life is rightly employed in perfecting and beautifying, "
                "the first in importance surely is man himself."
            ),
            "original_text_ko": (
                "세상이, 또는 자신의 세계의 일부가, 자신의 삶의 계획을 선택하도록 내맡기는 사람은 "
                "유인원 같은 모방 능력 외에는 다른 능력이 필요하지 않다... "
                "인간이 완성하고 아름답게 하는 데 정당하게 고용되는 인간의 작품들 중에서, "
                "가장 중요한 것은 분명 인간 자신이다."
            ),
            "explanation": (
                "밀은 개성의 발전을 공리의 중요한 구성 요소로 보았다. "
                "개인이 자신의 능력을 자유롭게 계발하고 자신만의 삶의 방식을 선택할 때, "
                "그것이 단지 개인적 선이 아니라 사회 전체의 진보에 기여한다. "
                "자유를 단순히 수단이 아닌 목적으로 보는 '자유지상주의적 공리주의'의 핵심이다."
            ),
            "argument": (
                "밀의 논거: (1) 각 개인은 자신의 조건과 성격을 가장 잘 이해하는 사람이다. "
                "(2) 개인이 자신의 능력을 발휘할 때 내면의 힘이 강해지고 풍부해진다. "
                "(3) 다양한 생활 방식이 허용될 때 사회는 '실험'을 통해 더 나은 방식을 발견한다. "
                "(4) 탁월한 개성을 가진 천재(genius)는 새로운 사상과 관습을 만들어 "
                "사회를 진보시키므로, 개성의 자유는 사회 전체에게도 유익하다."
            ),
            "counterpoint": (
                "칼 마르크스(Karl Marx)는 '독일 이데올로기'(The German Ideology, 1845)에서 "
                "밀이 주장하는 '개성의 자유'가 실질적으로는 부르주아 계급의 자유이며, "
                "경제적 불평등이 존재하는 한 노동자에게 개성의 자유는 공허한 개념이라고 비판했다. "
                "알래스데어 매킨타이어(Alasdair MacIntyre)는 '덕의 상실'(After Virtue, 1981)에서 "
                "밀의 개인주의가 공동체적 유대와 전통을 약화시킨다고 비판했다."
            ),
            "context": (
                "밀은 '획일적 관습의 횡포'와 '다수의 여론에 의한 압제'를 자유의 가장 큰 위협으로 보았다. "
                "개성의 자유는 이에 맞서는 방어 원리이다."
            ),
            "keywords": ["개성", "자유지상주의적 공리주의", "자기 계발", "실험적 삶"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-009: 공리주의와 정의
        {
            "id": "mill-claim-009",
            "thinker_id": "mill_js",
            "work_id": "mill-utilitarianism",
            "source_detail": "Utilitarianism, Ch.5",
            "claim": "정의는 공리의 특수한 경우로, 가장 중요하고 강렬한 공리적 의무이다.",
            "original_text": (
                "Justice is a name for certain classes of moral rules which concern the essentials of human well-being more nearly, "
                "and are therefore of more absolute obligation, than any other rules for the guidance of life."
            ),
            "original_text_ko": (
                "정의는 인간 복지의 본질에 더 밀접하게 관련되어 다른 어떤 삶의 지침 규칙보다 "
                "더 절대적인 의무를 지니는 특정 종류의 도덕 규칙의 이름이다."
            ),
            "explanation": (
                "밀은 공리주의의 가장 큰 도전인 '공리와 정의의 충돌' 문제를 다루었다. "
                "그는 정의가 공리와 별개의 독립적 원리가 아니라, "
                "공리의 일부 중에서도 가장 중요하고 강렬한 부분이라고 주장했다. "
                "정의 의무는 다른 도덕적 의무보다 강력한 이유는 "
                "그것이 인간 안전과 복지의 핵심을 보호하기 때문이다."
            ),
            "argument": (
                "밀의 논거: (1) 정의 감정의 분석: 정의 감정은 자신이 해를 당했을 때 "
                "분개하는 자연적 감정에서 기원한다. "
                "(2) 이 감정이 도덕적 의무가 되는 것은 사회 전체의 이익(공리)과 결합될 때이다. "
                "(3) 정의는 '완전 의무(perfect obligation)'를 만들어내며, "
                "불의는 항상 특정한 사람이 피해를 당했음을 의미한다. "
                "(4) 이러한 특성이 정의 의무를 다른 도덕 의무보다 더 강렬하고 절대적으로 만든다."
            ),
            "counterpoint": (
                "롤스(John Rawls)는 '정의론'(A Theory of Justice, 1971)에서 "
                "정의를 공리에 종속시키는 밀의 입장에 반대하여, "
                "정의는 공리 이전에 성립하는 독립적 원리라고 주장했다. "
                "정의 원리는 공리 계산과 무관하게 우선적으로 지켜져야 한다는 것이다. "
                "칸트(Immanuel Kant)는 '도덕 형이상학'(Metaphysics of Morals, 1797)에서 "
                "정의는 의무론적 원리이지 공리적 계산의 결과물이 될 수 없다고 주장했다."
            ),
            "context": (
                "공리주의에 대한 주요 반론 중 하나는 '공리를 위해 정의를 희생할 수 있다'는 것이었다. "
                "밀은 정의가 공리의 가장 중요한 부분임을 보임으로써 이 반론에 답하려 했다."
            ),
            "keywords": ["공리주의와 정의", "정의 감정", "완전 의무", "인간 안전"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-010: 내적 제재
        {
            "id": "mill-claim-010",
            "thinker_id": "mill_js",
            "work_id": "mill-utilitarianism",
            "source_detail": "Utilitarianism, Ch.3",
            "claim": "공리주의의 궁극적 제재(sanction)는 양심이라는 내적 제재이며, 의무를 어겼을 때 느끼는 고통이다.",
            "original_text": (
                "The internal sanction of duty, whatever our standard of duty may be, "
                "is one and the same — a feeling in our own mind; "
                "a pain, more or less intense, attendant on violation of duty."
            ),
            "original_text_ko": (
                "우리의 의무 기준이 무엇이든 간에 의무의 내적 제재는 하나이자 동일하다 — "
                "우리 자신의 마음속의 감정; "
                "의무 위반에 수반되는 크고 작은 고통."
            ),
            "explanation": (
                "벤담은 공리주의의 제재를 물리적 제재, 정치적 제재, 도덕적 제재, 종교적 제재 등 "
                "외적 제재로 설명했다. 밀은 이에 더하여 내적 제재인 양심을 강조했다. "
                "의무를 어겼을 때 느끼는 내면의 고통, 즉 양심의 가책이 "
                "공리주의의 가장 강력하고 근본적인 제재라는 것이다."
            ),
            "argument": (
                "밀의 논거: (1) 외적 제재는 처벌이나 사회적 불이익으로 복종을 강제하지만, "
                "진정한 도덕성은 내면적 동기에서 나와야 한다. "
                "(2) 인간은 사회적 동물로서 동료 인간과의 일체감(unity)을 자연스럽게 느끼며, "
                "이 감정이 타인의 행복에 대한 관심으로 발전한다. "
                "(3) 이러한 사회적 감정이 의무감과 결합하여 "
                "양심(conscience)이라는 내적 제재를 형성한다. "
                "(4) 이 내적 제재는 교육과 문화를 통해 강화된다."
            ),
            "counterpoint": (
                "칸트(Immanuel Kant)는 '도덕 형이상학의 기초'(Groundwork, 1785)에서 "
                "감정에 기반한 도덕은 진정한 의무가 아니라고 비판했다. "
                "고통을 느끼기 때문에 의무를 지키는 것은 경향성(inclination)에 따른 것이며, "
                "진정한 도덕적 의무는 순수 이성의 명령에서 나와야 한다는 것이다. "
                "또한 쇼펜하우어(Arthur Schopenhauer)는 공리주의적 제재가 "
                "결국 이기주의와 구별되지 않는다고 비판했다."
            ),
            "context": (
                "공리주의에 대한 비판 중 하나는 '왜 다수의 행복을 위해 행동해야 하는가'이다. "
                "밀은 내적 제재론을 통해 공리주의 의무의 심리적 토대를 설명했다."
            ),
            "keywords": ["내적 제재", "양심", "도덕 감정", "의무감"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-011: 대의민주주의
        {
            "id": "mill-claim-011",
            "thinker_id": "mill_js",
            "work_id": "mill-considerations-representative-government",
            "source_detail": "Considerations on Representative Government, Ch.3",
            "claim": "대의민주주의는 이상적인 정부 형태이다. 그러나 비례대표제를 통해 소수의 의견도 대표되어야 한다.",
            "original_text": (
                "The ideally best form of government is that in which the sovereignty... "
                "is vested in the entire aggregate of the community... "
                "representative government is the nearest approach to the ideal type of government."
            ),
            "original_text_ko": (
                "이상적으로 최선의 정부 형태는 주권이... "
                "공동체 전체의 총체에 귀속되는 것이다... "
                "대의정부는 이상적인 정부 유형에 가장 가까운 것이다."
            ),
            "explanation": (
                "밀은 대의민주주의가 이상적 정부 형태라고 주장했다. "
                "그 이유는 (1) 시민이 자신의 이익을 방어할 수 있고, "
                "(2) 시민의 도덕적·지적 능력을 향상시키며, "
                "(3) 최대 다수의 이익을 반영하기 때문이다. "
                "그러나 단순 다수결은 소수를 억압할 수 있으므로, "
                "비례대표제를 통해 소수 의견도 대표되어야 한다고 주장했다."
            ),
            "argument": (
                "밀의 논거: (1) 직접민주주의는 현대 국가에서 실현 불가능하므로 대의제가 차선이다. "
                "(2) 좋은 정부의 두 기준: 시민의 덕과 지성을 활용 및 향상시키고, "
                "공공 업무를 잘 처리하는 것이다. "
                "(3) 다수결은 지적으로 훈련된 소수의 의견을 무시할 수 있으므로, "
                "헤어(Thomas Hare)의 비례대표제가 필요하다. "
                "(4) 교육 수준이나 납세 여부에 따른 복수 투표제도 정당화될 수 있다."
            ),
            "counterpoint": (
                "루소(Jean-Jacques Rousseau)는 '사회계약론'(The Social Contract, 1762)에서 "
                "대의민주주의는 진정한 민주주의가 아니며, 일반의지(general will)는 "
                "대표될 수 없다고 비판했다. "
                "밀의 복수 투표제에 대해서는 로버트 달(Robert Dahl)이 "
                "'민주주의와 그 비판자들'(Democracy and Its Critics, 1989)에서 "
                "정치적 평등의 원리에 위배된다고 비판했다."
            ),
            "context": (
                "19세기 영국에서 선거권 확대 운동이 활발했다. "
                "밀은 민주주의를 지지하면서도 '다수결의 횡포'와 "
                "'무지한 대중의 정치'를 우려하는 양면적 입장을 취했다."
            ),
            "keywords": ["대의민주주의", "비례대표제", "다수결의 횡포", "복수 투표제"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-012: 여성 해방
        {
            "id": "mill-claim-012",
            "thinker_id": "mill_js",
            "work_id": "mill-subjection-of-women",
            "source_detail": "The Subjection of Women, Ch.1",
            "claim": "여성에 대한 법적·사회적 종속은 경험적 근거가 없는 자의적 차별이며, 성 평등이 사회 전체의 공리에 기여한다.",
            "original_text": (
                "The principle which regulates the existing social relations between the two sexes... "
                "is wrong in itself, and now one of the chief hindrances to human improvement; "
                "and that it ought to be replaced by a principle of perfect equality."
            ),
            "original_text_ko": (
                "양성 사이의 현존 사회적 관계를 규제하는 원리는... "
                "그 자체로 잘못되었으며 이제는 인간 발전의 주요 장애물 중 하나이다; "
                "그리고 그것은 완전한 평등의 원리로 대체되어야 한다."
            ),
            "explanation": (
                "밀은 여성의 법적·사회적 종속이 세 가지 이유에서 잘못되었다고 주장했다. "
                "(1) 자의적이다: 여성의 열등함은 실험(경험)으로 증명된 것이 아닌 "
                "전통과 편견에 근거한다. "
                "(2) 해악이다: 여성의 재능이 낭비되어 사회 전체의 공리가 감소한다. "
                "(3) 불공정하다: 법 앞의 평등이라는 자유주의 원리에 위배된다."
            ),
            "argument": (
                "밀의 논거: (1) 여성의 능력에 대한 우리의 지식은 "
                "강제와 제약 아래서 형성되었으므로 신뢰할 수 없다. "
                "진정한 자유 아래서 여성이 어떤 능력을 발휘할 수 있는지 모른다. "
                "(2) 역사적으로 여성의 사회적 역할이 고정된 것은 힘에 의한 것이지, "
                "자연적 적합성에 의한 것이 아니다. "
                "(3) 공리주의적으로, 인구의 절반인 여성의 재능을 활용할 수 없다면 "
                "사회 전체의 진보가 제한된다."
            ),
            "counterpoint": (
                "장 자크 루소(Jean-Jacques Rousseau)는 '에밀'(Émile, 1762)에서 "
                "여성의 교육은 남성에게 기쁨을 주기 위한 것이어야 한다고 주장하여 "
                "성적 차별을 자연화했다. "
                "그러나 밀의 입장은 반박이 어렵고, 오히려 현대 페미니스트들 일부는 "
                "밀이 가정 내 성별 분업을 완전히 비판하지 않았다고 지적한다 "
                "(Ann Robson, 'The Subjection of Women and the Improvement of Mankind', 1994)."
            ),
            "context": (
                "해리엇 테일러 밀(Harriet Taylor Mill)과의 지적 협력이 이 저작에 결정적 영향을 미쳤다. "
                "밀은 1865년 하원의원으로서 여성 참정권을 최초로 의회에 제안했다."
            ),
            "keywords": ["여성 해방", "성평등", "공리주의적 페미니즘", "자의적 차별"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-013: 귀납법
        {
            "id": "mill-claim-013",
            "thinker_id": "mill_js",
            "work_id": "mill-system-of-logic",
            "source_detail": "A System of Logic, Book II, Ch.3",
            "claim": "귀납법이 경험적 지식의 진정한 원천이며, 연역적 삼단논법은 이미 알려진 것에서 새로운 것을 도출하지 못한다.",
            "original_text": (
                "The individual facts which are the premises of a syllogism were known before the general proposition; "
                "and the conclusion, which purports to be derived from that general proposition, "
                "was virtually included in the premises of the syllogism."
            ),
            "original_text_ko": (
                "삼단논법의 전제인 개별 사실들은 일반 명제 이전에 알려져 있었다; "
                "그리고 그 일반 명제로부터 도출된 것으로 주장되는 결론은 "
                "사실상 삼단논법의 전제 안에 이미 포함되어 있었다."
            ),
            "explanation": (
                "밀은 전통적 삼단논법이 새로운 지식을 생산하지 못한다고 비판했다. "
                "'모든 사람은 죽는다 → 소크라테스는 사람이다 → 소크라테스는 죽는다'에서 "
                "결론은 전제에 이미 포함되어 있다. "
                "진정한 새 지식은 관찰과 실험을 통한 귀납적 추론에서 나온다고 주장했다."
            ),
            "argument": (
                "밀의 논거: (1) 삼단논법의 대전제('모든 사람은 죽는다')는 귀납적 일반화로 얻어진다. "
                "(2) 따라서 삼단논법은 결국 귀납적 추론에 의존한다. "
                "(3) 밀의 귀납법 다섯 원칙(일치법, 차이법, 일치차이법, 잉여법, 공변법)이 "
                "인과관계를 발견하는 체계적 방법을 제공한다. "
                "(4) 자연과학의 성공은 귀납적 방법론에 의존한다."
            ),
            "counterpoint": (
                "칼 포퍼(Karl Popper)는 '과학적 발견의 논리'(The Logic of Scientific Discovery, 1934)에서 "
                "귀납법은 논리적으로 정당화될 수 없다고 비판했다('귀납의 문제'). "
                "아무리 많은 관찰 사례가 있어도 일반 법칙을 논리적으로 확증할 수 없으며, "
                "오히려 반증(falsification)이 과학의 핵심이라고 주장했다. "
                "흄(David Hume)도 '인간 지성에 관한 탐구'(Enquiry Concerning Human Understanding, 1748)에서 "
                "귀납법의 논리적 근거를 부정했다."
            ),
            "context": (
                "19세기 초 영국에서 자연과학이 급속도로 발전하면서 과학적 방법론에 대한 관심이 높았다. "
                "밀은 귀납법을 체계화하여 사회과학에도 적용 가능한 방법론을 제시하려 했다."
            ),
            "keywords": ["귀납법", "삼단논법 비판", "과학적 방법론", "인과관계"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-014: 완성주의와 고차 능력
        {
            "id": "mill-claim-014",
            "thinker_id": "mill_js",
            "work_id": "mill-utilitarianism",
            "source_detail": "Utilitarianism, Ch.2",
            "claim": "인간의 고차적 능력(이성, 감정, 상상력)의 발휘가 행복의 핵심이며, 이것이 고차 쾌락의 근거이다.",
            "original_text": (
                "It is better to be a human being dissatisfied than a pig satisfied; "
                "better to be Socrates dissatisfied than a fool satisfied."
            ),
            "original_text_ko": (
                "만족한 돼지보다 불만족한 인간이 낫다; "
                "만족한 바보보다 불만족한 소크라테스가 낫다."
            ),
            "explanation": (
                "밀은 인간 능력의 위계를 상정했다. 인간의 고차적 능력 — "
                "지적 활동, 감정, 상상력, 도덕적 감수성 — 이 발휘될 때 "
                "발생하는 쾌락이 고차 쾌락이며, 이것이 인간 행복의 핵심이다. "
                "이는 아리스토텔레스의 에우다이모니아(eudaimonia) 개념과 유사하며, "
                "밀의 완성주의적 경향을 보여준다."
            ),
            "argument": (
                "밀의 논거: (1) 인간은 동물과 달리 이성, 상상력, 감정이라는 "
                "고차 능력을 가지고 있다. "
                "(2) 이 능력들을 발휘할 때 경험하는 쾌락은 육체적 쾌락보다 질적으로 우월하다. "
                "(3) 고차 능력을 가진 존재는 일단 그 능력의 쾌락을 맛보면 "
                "그것을 위한 불만족을 감수한다. "
                "(4) 따라서 인간 능력의 충분한 발현(flourishing)이 진정한 행복이다."
            ),
            "counterpoint": (
                "아리스토텔레스(Aristotle)는 '니코마코스 윤리학'(Nicomachean Ethics, 기원전 4세기)에서 "
                "유사하게 인간 특유의 기능(이성)의 탁월한 발휘가 행복이라고 주장했다. "
                "그러나 존 스튜어트 밀의 완성주의는 공리주의 틀 안에 있다는 점에서, "
                "덕 윤리학과 구분된다. "
                "피터 레일턴(Peter Railton)은 '소외, 결과주의, 공리주의의 한계'(1984)에서 "
                "완성주의적 요소를 공리주의에 통합하는 것이 개인의 욕구와 "
                "객관적 선의 간 긴장을 낳는다고 지적했다."
            ),
            "context": (
                "밀의 교육 배경에는 고전 문학, 철학, 수학이 포함되었고, "
                "정신적 위기 이후 워즈워스의 시에서 치유를 경험했다. "
                "이 경험이 감정과 상상력의 가치를 인식하게 했다."
            ),
            "keywords": ["완성주의", "고차 능력", "에우다이모니아", "인간 번영"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-015: 덕과 공리주의
        {
            "id": "mill-claim-015",
            "thinker_id": "mill_js",
            "work_id": "mill-utilitarianism",
            "source_detail": "Utilitarianism, Ch.4",
            "claim": "덕(virtue)은 처음에는 행복의 수단이지만, 인간 심리의 발전을 통해 덕 자체가 행복의 일부가 될 수 있다.",
            "original_text": (
                "Virtue, according to the utilitarian doctrine, is not naturally and originally part of the end, "
                "but it is capable of becoming so; and in those who love it disinterestedly "
                "it has become so, and is desired and cherished, not as a means to happiness, "
                "but as a part of their happiness."
            ),
            "original_text_ko": (
                "공리주의 교리에 따르면, 덕은 자연적으로나 원래부터 목적의 일부가 아니다. "
                "그러나 덕은 목적의 일부가 될 수 있다; 그리고 덕을 사심 없이 사랑하는 사람들에게는 "
                "덕이 그렇게 되었으며, 행복의 수단이 아니라 그들의 행복의 일부로서 욕구되고 소중히 여겨진다."
            ),
            "explanation": (
                "밀은 공리주의가 덕을 단순히 행복의 도구로 취급한다는 비판에 답했다. "
                "덕은 처음에는 행복을 위한 수단으로 계발되지만, "
                "심리적 연상(association)을 통해 덕 자체가 행복의 일부가 될 수 있다. "
                "이는 공리주의가 덕 윤리학의 통찰을 흡수할 수 있음을 보여준다."
            ),
            "argument": (
                "밀의 논거: (1) 인간 심리에서 수단과 목적의 연상이 이루어지면, "
                "수단이 목적의 일부가 될 수 있다. "
                "(돈을 행복의 수단으로 추구하다가 돈 자체를 목적으로 삼게 되듯) "
                "(2) 덕도 마찬가지로, 처음에는 행복을 위해 계발되지만 "
                "결국 행복의 구성 요소가 된다. "
                "(3) 따라서 공리주의는 덕을 단순 도구로 보는 것이 아니라 "
                "행복의 내재적 부분으로 볼 수 있다."
            ),
            "counterpoint": (
                "아리스토텔레스(Aristotle)는 '니코마코스 윤리학'(기원전 4세기)에서 "
                "덕이 행복의 구성 요소임을 주장했지만, "
                "이는 심리적 연상 과정을 통해서가 아니라 인간 본성에 내재된 것이라고 보았다. "
                "로저 크리스프(Roger Crisp)는 '공리주의에의 길'(Reasons and the Good, 2006)에서 "
                "밀의 심리적 연상론이 덕의 도구적 가치와 내재적 가치를 혼동한다고 비판했다."
            ),
            "context": (
                "공리주의가 덕을 경시한다는 비판에 대응하여, "
                "밀은 공리주의가 인간의 도덕적 성장과 덕의 계발을 포함할 수 있음을 논증했다."
            ),
            "keywords": ["덕과 공리주의", "심리적 연상", "내재적 가치", "도덕 성장"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-016: 다수결의 횡포
        {
            "id": "mill-claim-016",
            "thinker_id": "mill_js",
            "work_id": "mill-on-liberty",
            "source_detail": "On Liberty, Ch.1",
            "claim": "민주주의에서도 다수의 여론에 의한 '사회적 횡포'가 개인 자유의 가장 큰 위협이 될 수 있다.",
            "original_text": (
                "The tyranny of prevailing opinion and feeling... "
                "is peculiarly formidable to those who dissent from the reigning authority... "
                "there is a limit to the legitimate interference of collective opinion with individual independence."
            ),
            "original_text_ko": (
                "지배적인 의견과 감정의 횡포는... "
                "지배적 권위에서 벗어나는 사람들에게 특히 무서운 것이다... "
                "집합적 의견이 개인 독립에 정당하게 간섭할 수 있는 한계가 있다."
            ),
            "explanation": (
                "밀은 자유에 대한 위협이 국가 권력만이 아님을 지적했다. "
                "민주주의 사회에서도 다수의 여론과 관습이 소수자의 자유를 억압할 수 있다. "
                "이것이 '사회적 횡포(social tyranny)'이며, 법적 처벌보다 더 깊이 "
                "삶에 침투하여 영혼 자체를 노예화한다고 경고했다."
            ),
            "argument": (
                "밀의 논거: (1) 자유에 대한 위협은 정부뿐 아니라 지배적 사회 여론에서도 온다. "
                "(2) 사회적 압력은 법보다 더 강력하다 — 사람들의 생각과 행동을 직접 규율하기 때문이다. "
                "(3) 토크빌(Alexis de Tocqueville)의 '다수의 횡포' 분석을 발전시켜, "
                "민주주의의 본질적 위험으로 다수주의를 지적했다. "
                "(4) 개인 자유를 보호하는 원리(해악 원리)는 정부뿐 아니라 "
                "사회의 여론 압력에도 적용되어야 한다."
            ),
            "counterpoint": (
                "에밀 뒤르켐(Émile Durkheim)은 '도덕 교육'(Moral Education, 1925)에서 "
                "사회적 규범과 집합 의식이 개인의 도덕 발달에 필수적이라고 주장하여 "
                "밀의 개인주의적 자유론을 비판했다. "
                "공동체주의자(communitarians)인 알래스데어 매킨타이어(Alasdair MacIntyre)는 "
                "'덕의 상실'(After Virtue, 1981)에서 개인의 자율성을 공동체와 전통에서 분리하면 "
                "도덕 판단의 기준을 잃게 된다고 비판했다."
            ),
            "context": (
                "토크빌의 '미국의 민주주의'(1835~40)에 영향을 받아, "
                "밀은 민주주의의 이론적 정당화와 동시에 민주주의의 위험에도 주목했다."
            ),
            "keywords": ["다수결의 횡포", "사회적 횡포", "반다수결주의", "소수자 보호"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-017: 자유의 경계 — 자기 관련 행위
        {
            "id": "mill-claim-017",
            "thinker_id": "mill_js",
            "work_id": "mill-on-liberty",
            "source_detail": "On Liberty, Ch.4",
            "claim": "행위를 '자기 관련 행위'와 '타인 관련 행위'로 구분하여, 자기 관련 행위에는 사회가 간섭할 수 없다.",
            "original_text": (
                "In the part which merely concerns himself, his independence is, of right, absolute. "
                "Over himself, over his own body and mind, the individual is sovereign."
            ),
            "original_text_ko": (
                "오직 자신에게만 관련된 부분에서는, 그의 독립은 권리상 절대적이다. "
                "자기 자신에 대해서, 자신의 몸과 마음에 대해서, 개인은 주권자이다."
            ),
            "explanation": (
                "밀은 해악 원리를 구체화하기 위해 '자기 관련 행위'와 '타인 관련 행위'를 구분했다. "
                "자기 관련 행위(self-regarding actions)란 오직 자신에게만 영향을 미치는 행위이며, "
                "이에 대해서는 사회의 간섭이 정당화되지 않는다. "
                "개인은 자신의 몸과 마음의 절대적 주권자이다."
            ),
            "argument": (
                "밀의 논거: (1) 개인은 자신의 이익에 대해 가장 잘 아는 사람이다. "
                "(2) 개인의 실수에 대한 최선의 교정은 자연적 결과이지, 사회의 처벌이 아니다. "
                "(3) 자기 관련 행위에 대한 간섭은 그 행위가 어떠하든 무조건 잘못이다. "
                "인간은 실수할 권리도 있다. "
                "(4) 사회가 간섭해서 얻는 이익보다 자유 침해로 발생하는 해악이 더 크다."
            ),
            "counterpoint": (
                "조엘 파인버그(Joel Feinberg)는 '해악의 도덕적 한계'(The Moral Limits of the Criminal Law, 1984)에서 "
                "'순수하게 자기 관련적인 행위'는 실제로 존재하기 어렵다고 지적했다. "
                "모든 행위는 어떤 방식으로든 타인에게 영향을 미치기 때문이다. "
                "제랄드 드워킨(Gerald Dworkin)은 '온정주의'(Paternalism, 1972)에서 "
                "자율성을 보호하기 위한 온화한 간섭주의(soft paternalism)는 정당화될 수 있다고 주장했다."
            ),
            "context": (
                "19세기 영국의 주류 도덕관은 음주, 도박, 성적 행위 등에 대해 "
                "법적 규제를 정당화했다. "
                "밀은 이러한 도덕적 간섭주의에 반대하는 이론적 근거를 제시했다."
            ),
            "keywords": ["자기 관련 행위", "개인 주권", "간섭주의 비판", "자유의 경계"],
            "verified": False,
            "verification_log": []
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """밀 핵심 키워드 데이터 입력."""
    keywords = [
        {
            "id": "mill-keyword-001",
            "term": "질적 공리주의",
            "term_en": "Qualitative Utilitarianism",
            "definition": (
                "존 스튜어트 밀이 벤담의 양적 공리주의를 수정하여 제시한 입장. "
                "쾌락에는 양적 차이뿐 아니라 질적 차이도 있으며, "
                "정신적·지적 쾌락(고차 쾌락)이 육체적 쾌락(저차 쾌락)보다 질적으로 우월하다고 주장한다. "
                "쾌락의 질적 우열은 두 쾌락을 모두 경험한 '역량 있는 판단자'의 선호에 의해 결정된다."
            ),
            "thinker_id": "mill_js",
            "work_id": "mill-utilitarianism",
            "related_terms": ["역량 있는 판단자", "고차 쾌락", "저차 쾌락", "벤담의 양적 공리주의"]
        },
        {
            "id": "mill-keyword-002",
            "term": "해악 원리",
            "term_en": "Harm Principle",
            "definition": (
                "밀의 '자유론'에서 제시된 원리. "
                "사회가 개인의 자유를 합법적으로 제한할 수 있는 유일한 근거는 "
                "타인에 대한 해악을 방지하는 것이다. "
                "자신만을 해치는 행위(자기 관련 행위)에 대해서는 사회가 간섭할 수 없다. "
                "자유주의 정치철학의 핵심 원리이다."
            ),
            "thinker_id": "mill_js",
            "work_id": "mill-on-liberty",
            "related_terms": ["자기 관련 행위", "간섭주의", "자유의 세 영역", "개인 자유"]
        },
        {
            "id": "mill-keyword-003",
            "term": "역량 있는 판단자",
            "term_en": "Competent Judge",
            "definition": (
                "밀이 쾌락의 질적 우열을 판단하는 기준으로 제시한 개념. "
                "비교 대상인 두 쾌락을 모두 충분히 경험하여 그 차이를 아는 사람을 가리킨다. "
                "이들의 일관된 선호가 어떤 쾌락이 더 가치 있는지를 결정하는 기준이 된다. "
                "두 쾌락 중 한 쪽만 아는 사람(예: 돼지, 바보)은 판단 자격이 없다."
            ),
            "thinker_id": "mill_js",
            "work_id": "mill-utilitarianism",
            "related_terms": ["질적 공리주의", "고차 쾌락", "경험적 기준", "선호"]
        },
        {
            "id": "mill-keyword-004",
            "term": "고차 쾌락",
            "term_en": "Higher Pleasures",
            "definition": (
                "밀이 구분한 쾌락의 두 종류 중 질적으로 우월한 것. "
                "이성, 감정, 상상력 등 인간의 고차 능력을 발휘할 때 생기는 쾌락이다. "
                "지적 탐구, 예술 감상, 도덕적 성취 등에서 오는 쾌락이 이에 해당한다. "
                "대비 개념은 육체적 감각에서 오는 '저차 쾌락(lower pleasures)'이다."
            ),
            "thinker_id": "mill_js",
            "work_id": "mill-utilitarianism",
            "related_terms": ["질적 공리주의", "역량 있는 판단자", "저차 쾌락", "인간 능력"]
        },
        {
            "id": "mill-keyword-005",
            "term": "내적 제재",
            "term_en": "Internal Sanction",
            "definition": (
                "밀이 공리주의의 도덕적 동기로 제시한 개념. "
                "의무를 어겼을 때 느끼는 내면의 고통, 즉 양심(conscience)이 "
                "공리주의의 궁극적이고 가장 강력한 제재이다. "
                "벤담의 외적 제재(물리적·법적·사회적·종교적)에 더하여, "
                "내적 제재가 도덕의 심리적 토대임을 주장했다."
            ),
            "thinker_id": "mill_js",
            "work_id": "mill-utilitarianism",
            "related_terms": ["제재", "양심", "외적 제재", "도덕 감정", "의무감"]
        },
        {
            "id": "mill-keyword-006",
            "term": "개성",
            "term_en": "Individuality",
            "definition": (
                "밀의 '자유론' 제3장에서 중심 개념. "
                "각 개인이 자신만의 고유한 방식으로 능력을 계발하고 삶을 영위하는 것을 뜻한다. "
                "밀은 개성의 자유로운 발전이 개인의 행복뿐 아니라 "
                "사회 진보를 위해서도 필수적이라고 주장했다. "
                "다양성과 실험적 삶의 방식이 보장될 때 최선의 삶의 방식이 발견된다."
            ),
            "thinker_id": "mill_js",
            "work_id": "mill-on-liberty",
            "related_terms": ["자유지상주의적 공리주의", "다양성", "실험적 삶", "사회 진보"]
        },
        {
            "id": "mill-keyword-007",
            "term": "대의민주주의",
            "term_en": "Representative Democracy",
            "definition": (
                "밀이 '대의정부론'에서 이상적인 정부 형태로 제시한 개념. "
                "주권이 전체 국민에게 있되, 실제 통치는 국민이 선출한 대표자를 통해 이루어진다. "
                "밀은 비례대표제를 통해 소수 의견도 대표되어야 하며, "
                "시민의 지적·도덕적 향상을 위한 기회도 제공해야 한다고 주장했다."
            ),
            "thinker_id": "mill_js",
            "work_id": "mill-considerations-representative-government",
            "related_terms": ["비례대표제", "복수 투표제", "다수결의 횡포", "시민 참여"]
        },
        {
            "id": "mill-keyword-008",
            "term": "자유지상주의적 공리주의",
            "term_en": "Libertarian Utilitarianism",
            "definition": (
                "밀이 공리주의와 자유주의를 결합한 입장. "
                "자유가 단지 행복의 수단이 아니라 그 자체로 공리에 기여하는 내재적 가치를 가진다고 본다. "
                "개인의 자유로운 발전과 다양성이 사회 전체의 장기적 공리를 극대화한다는 주장이다. "
                "벤담의 순수한 쾌락 계산적 공리주의와 구분된다."
            ),
            "thinker_id": "mill_js",
            "work_id": "mill-on-liberty",
            "related_terms": ["해악 원리", "개성", "공리주의", "자유주의"]
        },
        {
            "id": "mill-keyword-009",
            "term": "귀납법의 다섯 원칙",
            "term_en": "Five Methods of Induction",
            "definition": (
                "밀이 '논리학 체계'에서 제시한 귀납적 인과관계 발견의 다섯 가지 방법. "
                "(1) 일치법(Method of Agreement): 여러 경우에서 공통 선행 조건을 원인으로 본다. "
                "(2) 차이법(Method of Difference): 결과가 있는 경우와 없는 경우를 비교한다. "
                "(3) 일치차이법(Joint Method): 일치법과 차이법을 결합한다. "
                "(4) 잉여법(Method of Residues): 이미 알려진 원인의 효과를 빼고 남은 것을 본다. "
                "(5) 공변법(Method of Concomitant Variation): 함께 변화하는 현상의 인과관계를 추론한다."
            ),
            "thinker_id": "mill_js",
            "work_id": "mill-system-of-logic",
            "related_terms": ["귀납법", "인과관계", "과학적 방법론", "경험주의"]
        },
        {
            "id": "mill-keyword-010",
            "term": "공리주의의 증명",
            "term_en": "Proof of Utilitarianism",
            "definition": (
                "밀이 '공리주의' 제4장에서 시도한 공리주의의 정당화. "
                "행복이 바람직하다는 것은, 모든 사람이 실제로 행복을 욕구한다는 경험적 사실로부터 논증된다. "
                "G.E. 무어는 이를 '자연주의적 오류'라고 비판했다 "
                "(사실[is desired]에서 가치[is desirable]를 도출하는 오류)."
            ),
            "thinker_id": "mill_js",
            "work_id": "mill-utilitarianism",
            "related_terms": ["자연주의적 오류", "바람직함", "욕구", "G.E. 무어"]
        },
        {
            "id": "mill-keyword-011",
            "term": "정의와 공리",
            "term_en": "Justice and Utility",
            "definition": (
                "밀이 '공리주의' 제5장에서 다룬 주제. "
                "정의는 공리와 독립적인 원리가 아니라, 공리의 특수한 경우이다. "
                "정의 의무는 인간 복지의 가장 핵심적인 부분을 보호하므로, "
                "다른 도덕 의무보다 더 강력하고 절대적인 성격을 갖는다."
            ),
            "thinker_id": "mill_js",
            "work_id": "mill-utilitarianism",
            "related_terms": ["정의 감정", "완전 의무", "공리주의", "인간 안전"]
        },
        {
            "id": "mill-keyword-012",
            "term": "비례대표제",
            "term_en": "Proportional Representation",
            "definition": (
                "밀이 '대의정부론'에서 지지한 선거 제도. "
                "토마스 헤어(Thomas Hare)가 제안한 단기이양식 비례대표제를 지지했다. "
                "단순 다수결 제도는 소수파를 대의 기관에서 완전히 배제하므로, "
                "비례대표제를 통해 소수 의견도 입법부에 대표되어야 한다고 주장했다."
            ),
            "thinker_id": "mill_js",
            "work_id": "mill-considerations-representative-government",
            "related_terms": ["대의민주주의", "다수결의 횡포", "소수 보호", "토마스 헤어"]
        }
    ]

    for keyword in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=keyword["id"], document=keyword)
        print(f"[keyword] {keyword['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """밀 관련 사상 간 관계 데이터 입력."""
    relations = [
        {
            "from_thinker": "bentham",
            "to_thinker": "mill_js",
            "type": "influenced",
            "description": (
                "제러미 벤담은 밀의 아버지 제임스 밀을 통해 존 스튜어트 밀에게 깊은 영향을 미쳤다. "
                "밀은 벤담의 공리주의를 계승하여 도덕과 정치의 기준으로 삼았으며, "
                "이를 발전시켜 질적 공리주의를 완성했다."
            ),
            "evidence": "Mill, Autobiography (1873), Ch.2: '아버지의 교육과 벤담의 영향' 기술"
        },
        {
            "from_thinker": "mill_js",
            "to_thinker": "bentham",
            "type": "developed",
            "description": (
                "밀은 벤담의 양적 공리주의를 발전시켜 쾌락의 질적 차이를 도입한 "
                "질적 공리주의를 완성했다. 최대 행복 원리를 계승하면서도, "
                "'역량 있는 판단자' 기준과 고차 쾌락 개념을 추가하여 공리주의를 풍부하게 만들었다."
            ),
            "evidence": "Mill, Utilitarianism (1863), Ch.2: 벤담 공리주의 계승 및 수정"
        },
        {
            "from_thinker": "kant_i",
            "to_thinker": "mill_js",
            "type": "criticized",
            "description": (
                "칸트의 의무론적 윤리학은 공리주의 전반에 대한 강력한 반론을 제공하여 "
                "밀의 공리주의 정교화를 자극했다. "
                "밀은 정의 개념의 논의(공리주의 제5장)에서 칸트적 비판에 답하려 했다."
            ),
            "evidence": "Kant, Groundwork (1785): 결과가 아닌 동기의 순수성이 도덕의 기준"
        },
        {
            "from_thinker": "mill_js",
            "to_thinker": "rawls_j",
            "type": "influenced",
            "description": (
                "밀의 자유주의적 공리주의, 특히 개인의 자유와 권리에 대한 강조는 "
                "롤스의 자유주의 정치철학에 영향을 미쳤다. "
                "롤스는 공리주의를 비판하면서도 밀의 자유 원리 일부를 자신의 정의 원칙에 통합했다."
            ),
            "evidence": "Rawls, A Theory of Justice (1971), §6: 공리주의 비판과 자유 원리"
        },
        {
            "from_thinker": "mill_js",
            "to_thinker": "bentham",
            "type": "criticized",
            "description": (
                "밀은 벤담의 순수한 양적 공리주의가 인간의 고차 능력과 정신적 가치를 무시한다고 비판했다. "
                "'공리주의'에서 쾌락의 질적 차이를 인정하지 않는 벤담의 입장을 "
                "'돼지의 철학'으로 묘사되는 위험에 처해 있다고 보고, 이를 수정했다."
            ),
            "evidence": "Mill, Utilitarianism (1863), Ch.2: 쾌락의 질적 차이 도입"
        }
    ]

    # relations는 고유 ID를 생성하여 입력
    for i, relation in enumerate(relations):
        rel_id = f"rel-{relation['from_thinker']}-{relation['to_thinker']}-{relation['type']}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=relation)
        print(f"[relation] {rel_id}: {result['result']}")

    return len(relations)


def main():
    print("=== 존 스튜어트 밀(John Stuart Mill) 데이터 ES 입력 시작 ===\n")

    client = get_client()

    try:
        # 1. 사상가 입력
        print("--- [1/5] 사상가 입력 ---")
        insert_thinker(client)
        print()

        # 2. 저서 입력
        print("--- [2/5] 저서 입력 ---")
        works_count = insert_works(client)
        print(f"총 {works_count}건 입력\n")

        # 3. 주장 입력
        print("--- [3/5] 주장 입력 ---")
        claims_count = insert_claims(client)
        print(f"총 {claims_count}건 입력\n")

        # 4. 키워드 입력
        print("--- [4/5] 키워드 입력 ---")
        keywords_count = insert_keywords(client)
        print(f"총 {keywords_count}건 입력\n")

        # 5. 관계 입력
        print("--- [5/5] 관계 입력 ---")
        relations_count = insert_relations(client)
        print(f"총 {relations_count}건 입력\n")

        print("=== 입력 완료 ===")
        print(f"- thinker: 1건")
        print(f"- works: {works_count}건")
        print(f"- claims: {claims_count}건")
        print(f"- keywords: {keywords_count}건")
        print(f"- relations: {relations_count}건")

    finally:
        close_client(client)


if __name__ == "__main__":
    main()
