"""벤담(Jeremy Bentham) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS
)


def insert_thinker(client):
    """벤담 사상가 데이터 입력."""
    doc = {
        "id": "bentham",
        "name": "제러미 벤담",
        "name_en": "Jeremy Bentham",
        "field": "western_ethics",
        "era": "근대 영국",
        "birth_year": 1748,
        "death_year": 1832,
        "background": (
            "런던 스피탈필즈(Spitalfields)에서 부유한 법조인 가문에서 태어났다. "
            "신동으로 알려져 12세에 옥스퍼드 퀸스 칼리지에 입학하고, 15세에 졸업한 뒤 법률을 공부했다. "
            "그러나 실제 법 실무보다 법철학과 사회 개혁에 관심을 가져, 법조인으로 일하지 않고 저술과 개혁 활동에 전념했다. "
            "프리스틀리의 '최대 다수의 최대 행복' 원리와 흄의 경험주의, 에피쿠로스의 쾌락주의에 영향을 받았다. "
            "프랑스 명예시민권을 받았고, 미국 독립혁명과 프랑스 혁명에 지적 공감을 표했다. "
            "사망 후 시신을 '오토 아이콘(auto-icon)'으로 만들어 유니버시티 칼리지 런던(UCL)에 보존해 달라는 유언을 남겼으며, "
            "현재도 UCL에 전시되어 있다."
        ),
        "core_philosophy": (
            "공리주의(Utilitarianism)의 창시자. 모든 인간의 행동은 쾌락을 추구하고 고통을 피하려는 동기에 의해 지배되며(심리적 이기주의), "
            "따라서 도덕과 입법의 목적은 '최대 다수의 최대 행복'을 달성하는 것이어야 한다고 주장했다. "
            "쾌락과 고통은 강도·지속성·확실성·근접성·생산성·순수성·범위 등 7가지 기준으로 양적으로 계산 가능하다고 보았으며(쾌락 계산, felicific calculus), "
            "쾌락의 질적 차이를 인정하지 않는 행위 공리주의를 주장했다. "
            "사회 제도와 법률은 공리의 원리에 따라 개혁되어야 한다고 보아, "
            "감옥 개혁(판옵티콘), 민주주의 확대, 동물 복지, 고리대금 철폐 등 다방면의 사회 개혁론을 전개했다."
        ),
        "philosophical_journey": (
            "청년기(1760s~1780s): 흄, 헬베티우스, 프리스틀리의 저작에서 공리 원리의 기초를 발견하고 체계화하기 시작했다. "
            "'도덕과 입법의 원리 서론'(1789) 출판으로 공리주의 윤리학의 기초를 정립했다. "
            "중기(1780s~1810s): 판옵티콘 감옥 설계와 사회 개혁 운동에 몰두하면서, "
            "공리 원리를 법률·정치 제도에 적용하는 실천적 작업을 수행했다. "
            "말년(1810s~1832): 민주주의와 보통선거권, 언론 자유, 동성애 비범죄화 등 급진적 자유주의 개혁을 주장했다. "
            "제자 제임스 밀, 존 스튜어트 밀을 통해 공리주의 전통을 이어갔다."
        ),
        "keywords": [
            "공리의 원리",
            "최대 다수의 최대 행복",
            "쾌락 계산",
            "행위 공리주의",
            "제재",
            "판옵티콘",
            "심리적 이기주의"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="bentham", document=doc)
    print(f"[thinker] bentham: {result['result']}")
    return result


def insert_works(client):
    """벤담 저서 데이터 입력."""
    works = [
        {
            "id": "bentham-introduction-principles",
            "thinker_id": "bentham",
            "title": "도덕과 입법의 원리 서론",
            "title_original": "An Introduction to the Principles of Morals and Legislation",
            "year": 1789,
            "significance": (
                "벤담 공리주의 윤리학의 핵심 저작이자 서양 공리주의 전통의 출발점. "
                "공리의 원리, 쾌락과 고통의 목록, 쾌락 계산의 7가지 기준, "
                "제재(sanction) 이론, 범죄와 처벌의 원리를 체계적으로 논한다. "
                "임용시험 윤리 과목에서 가장 중요하게 다루어지는 벤담의 저서이다."
            ),
            "key_concepts": [
                "공리의 원리", "쾌락 계산", "제재", "최대 행복 원리",
                "쾌락과 고통", "행위 공리주의", "입법 원리"
            ]
        },
        {
            "id": "bentham-panopticon",
            "thinker_id": "bentham",
            "title": "판옵티콘 글들",
            "title_original": "The Panopticon Writings",
            "year": 1787,
            "significance": (
                "원형 감시 건물(판옵티콘) 설계를 통해 공리주의적 형벌과 감시 원리를 구현하려 한 저작. "
                "감시자는 보이지 않지만 수감자는 항상 관찰당할 수 있다는 구조를 통해 "
                "최소 비용으로 최대의 규율 효과를 달성하고자 했다. "
                "미셸 푸코는 '감시와 처벌'에서 이를 근대 권력의 상징으로 분석했다."
            ),
            "key_concepts": [
                "판옵티콘", "감시", "처벌", "개혁", "규율"
            ]
        },
        {
            "id": "bentham-fragment-on-government",
            "thinker_id": "bentham",
            "title": "정부론 단편",
            "title_original": "A Fragment on Government",
            "year": 1776,
            "significance": (
                "벤담의 첫 번째 주요 출판 저작으로, 블랙스톤의 '영국법 주석'에서 나타난 "
                "사회계약론과 자연법론을 공리주의 관점에서 비판한 저작. "
                "'최대 다수의 최대 행복'이라는 공리 원리를 명시적으로 제시하면서 "
                "기존 법 이론의 허구성을 비판했다."
            ),
            "key_concepts": [
                "최대 다수의 최대 행복", "사회계약 비판", "공리 원리", "법 개혁"
            ]
        },
        {
            "id": "bentham-deontology",
            "thinker_id": "bentham",
            "title": "의무론",
            "title_original": "Deontology",
            "year": 1834,
            "significance": (
                "벤담 사후 보우링(John Bowring)에 의해 출판된 저작. "
                "개인 윤리와 관련하여 공리주의 원리를 적용한 도덕철학을 전개하며, "
                "사적 영역에서의 공리 극대화 원리를 논한다. "
                "칸트적 의무론과의 대비에서 벤담의 공리주의적 의무 개념을 이해하는 데 중요하다."
            ),
            "key_concepts": [
                "사적 윤리", "공리주의 도덕", "의무", "행복"
            ]
        },
        {
            "id": "bentham-constitutional-code",
            "thinker_id": "bentham",
            "title": "헌법전",
            "title_original": "Constitutional Code",
            "year": 1830,
            "significance": (
                "벤담이 민주주의적 공화제 정부의 이상적 헌법 설계를 제시한 저작. "
                "보통선거권, 비밀투표, 언론 자유, 삼권분립, 관료제 개혁 등을 체계적으로 논한다. "
                "공리주의를 정치 제도 설계에 적용한 대표적 저작이다."
            ),
            "key_concepts": [
                "민주주의", "보통선거권", "입법원리", "관료제", "공리주의 정치"
            ]
        },
        {
            "id": "bentham-rationale-of-punishment",
            "thinker_id": "bentham",
            "title": "처벌의 근거",
            "title_original": "The Rationale of Punishment",
            "year": 1830,
            "significance": (
                "공리주의 형벌론을 체계화한 저작. "
                "처벌은 그 자체로는 악(고통)이지만, 더 큰 악(범죄)을 방지함으로써 "
                "공리를 증대시키는 경우에만 정당화된다고 논한다. "
                "처벌의 목적을 응보가 아닌 위하(deterrence)와 개혁(reform)에 두었다."
            ),
            "key_concepts": [
                "형벌론", "위하", "개혁", "공리주의 처벌", "비례 원칙"
            ]
        },
        {
            "id": "bentham-anarchical-fallacies",
            "thinker_id": "bentham",
            "title": "무정부적 오류들",
            "title_original": "Anarchical Fallacies",
            "year": 1843,
            "significance": (
                "프랑스 혁명의 '인간과 시민의 권리 선언'(1789)을 비판한 저작(벤담 사후 출판). "
                "'자연권'이나 '양도 불가능한 권리' 같은 개념을 '횃불 위의 넌센스(nonsense upon stilts)'라고 규정하며, "
                "권리는 실정법에 의해서만 성립한다고 주장했다."
            ),
            "key_concepts": [
                "자연권 비판", "실정법", "법 실증주의", "인권 비판"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """벤담 핵심 주장 데이터 입력."""
    claims = [
        {
            "id": "bentham-claim-001",
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "source_detail": "An Introduction to the Principles of Morals and Legislation, Chapter 1, §1",
            "claim": "자연은 인류를 쾌락과 고통이라는 두 주권자 아래 두었다. 우리가 무엇을 해야 하는지, 무엇을 할 것인지를 결정하는 것은 오직 이 두 가지이다.",
            "original_text": "Nature has placed mankind under the governance of two sovereign masters, pain and pleasure. It is for them alone to point out what we ought to do, as well as to determine what we shall do.",
            "original_text_ko": "자연은 인류를 쾌락과 고통이라는 두 주권자의 지배 아래 두었다. 우리가 무엇을 해야 하는지를 가리키고 우리가 무엇을 할 것인지를 결정하는 것은 오직 이 두 가지뿐이다.",
            "explanation": (
                "벤담은 인간의 행동이 쾌락을 추구하고 고통을 피하려는 심리적 동기에 의해 지배된다는 "
                "'심리적 이기주의(psychological egoism)'를 출발점으로 삼는다. "
                "이는 단순한 기술적 사실 진술(인간은 실제로 이렇게 행동한다)이자 규범적 원리의 토대이다. "
                "이 전제로부터 도덕과 입법의 목적은 쾌락을 극대화하고 고통을 최소화하는 것이어야 한다는 결론이 도출된다."
            ),
            "argument": (
                "전제1: 인간 행동의 실제 동기는 항상 쾌락을 극대화하고 고통을 최소화하는 것이다(심리적 이기주의). "
                "전제2: 무엇을 해야 하는가의 문제(규범)는 무엇이 인간을 움직이는가의 문제(사실)와 연결되어야 한다. "
                "전제3: 쾌락과 고통만이 우리를 실제로 움직이는 것이므로, 이것들이 도덕적 판단의 기준이 되어야 한다. "
                "결론: 따라서 공리의 원리(쾌락 증가, 고통 감소)가 도덕과 입법의 유일한 타당한 기준이다."
            ),
            "counterpoint": (
                "칸트는 '도덕형이상학 기초'에서 쾌락과 고통 같은 경험적 욕구에 기반한 도덕은 "
                "보편성과 필연성을 가질 수 없다고 비판했다. 도덕 법칙은 경향성(inclination)이 아니라 "
                "순수 이성으로부터 도출되어야 하며, 의무는 결과(쾌락)가 아닌 원리(준칙)에 따라야 한다고 주장했다. "
                "밀은 '공리주의'에서 벤담의 심리적 이기주의를 수정하여 쾌락의 질적 차이를 인정하고, "
                "타인의 행복을 위한 행동도 공리주의와 양립 가능함을 보이려 했다."
            ),
            "context": "공리주의 도덕 이론의 첫 번째 장으로, 이후 모든 공리주의 원리의 심리학적 토대를 확립하는 맥락에서 제시되었다.",
            "keywords": ["심리적 이기주의", "쾌락", "고통", "공리의 원리"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "bentham-claim-002",
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "source_detail": "An Introduction to the Principles of Morals and Legislation, Chapter 1, §2",
            "claim": "공리의 원리(Principle of Utility)란 어떤 행동이든 관련 당사자의 행복을 증가시키거나 감소시키는 경향에 따라 그 행동을 시인하거나 부인하는 원리이다.",
            "original_text": "By the principle of utility is meant that principle which approves or disapproves of every action whatsoever, according to the tendency which it appears to have to augment or diminish the happiness of the party whose interest is in question.",
            "original_text_ko": "공리의 원리란 어떤 행동이든 그것이 관련 당사자의 행복을 증가시키거나 감소시키는 경향에 따라 그 행동을 시인하거나 부인하는 원리를 의미한다.",
            "explanation": (
                "공리(utility)란 이득·편익·쾌락·선·행복을 산출하거나 해악·고통·악·불행을 방지하는 "
                "어떤 대상의 속성이다. 벤담은 '행복'을 '쾌락의 합계에서 고통의 합계를 뺀 것'으로 정의한다. "
                "이 원리는 개인의 행위뿐 아니라 정부의 모든 조치에도 적용된다. "
                "나중에 벤담은 이를 '최대 행복 원리(Greatest Happiness Principle)'라고도 불렀다."
            ),
            "argument": (
                "전제1: 도덕 판단의 기준은 행위 자체의 속성(의도, 동기, 형식)이 아니라 그 결과여야 한다. "
                "전제2: 결과 중 도덕적으로 가장 중요한 것은 쾌락(행복)의 증가와 고통(불행)의 감소이다. "
                "전제3: 따라서 어떤 행위의 도덕성은 그것이 산출하는 쾌락과 고통의 총량에 의해 판단된다. "
                "결론: 공리의 원리, 즉 행복을 최대화하고 불행을 최소화하는 원리가 도덕과 입법의 기준이다."
            ),
            "counterpoint": (
                "로스(W.D. Ross)는 '옳음과 선'에서 공리 원리는 직관적으로 자명한 다수의 의무들(약속 준수, 정직, "
                "감사 등)을 설명하지 못한다고 비판했다. "
                "롤스는 '정의론'에서 공리주의는 개인의 권리와 평등한 자유를 침해해서라도 전체 효용을 "
                "극대화하는 것을 허용할 수 있어 정의의 요구와 충돌한다고 비판했다."
            ),
            "context": "공리의 원리를 명시적으로 정의하고, 이를 도덕과 입법의 기본 원리로 확립하는 맥락이다.",
            "keywords": ["공리의 원리", "최대 행복 원리", "행복", "공리주의"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "bentham-claim-003",
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "source_detail": "An Introduction to the Principles of Morals and Legislation, Chapter 4",
            "claim": "쾌락과 고통의 가치(행복 계산, Felicific Calculus)는 강도(intensity), 지속성(duration), 확실성(certainty), 근접성(propinquity), 생산성(fecundity), 순수성(purity), 범위(extent)의 7가지 기준으로 측정할 수 있다.",
            "original_text": "To a person considered by himself, the value of a pleasure or pain considered by itself, will be greater or less, according to the four following circumstances: 1. Its intensity. 2. Its duration. 3. Its certainty or uncertainty. 4. Its propinquity or remoteness. ...Two other circumstances are to be taken into the account: 5. Its fecundity... 6. Its purity... 7. Its extent.",
            "original_text_ko": "개인에게 고려될 때, 쾌락이나 고통의 가치는 다음 네 가지 상황에 따라 크거나 작을 것이다: 1. 강도, 2. 지속성, 3. 확실성 또는 불확실성, 4. 근접성 또는 원격성. ...두 가지 추가 상황도 고려되어야 한다: 5. 생산성, 6. 순수성, 7. 범위.",
            "explanation": (
                "강도(intensity): 쾌락 또는 고통이 얼마나 강한가. "
                "지속성(duration): 쾌락 또는 고통이 얼마나 오래 지속되는가. "
                "확실성(certainty): 쾌락 또는 고통이 실제로 발생할 가능성이 얼마나 높은가. "
                "근접성(propinquity): 쾌락 또는 고통이 얼마나 가까운 미래에 발생하는가. "
                "생산성(fecundity): 쾌락이 더 많은 쾌락을 낳을 가능성, 또는 고통이 더 많은 고통을 낳을 가능성. "
                "순수성(purity): 쾌락이 반대로 고통을 낳지 않을 가능성, 또는 고통이 반대로 쾌락을 낳지 않을 가능성. "
                "범위(extent): 영향을 받는 사람의 수. 개인적 행위 판단 시 앞의 6가지, 공동체 수준에서는 7번째도 더한다."
            ),
            "argument": (
                "전제1: 도덕적 판단이 객관적이고 과학적이 되려면 쾌락과 고통을 측정 가능해야 한다. "
                "전제2: 쾌락과 고통은 강도·지속성 등 구체적 기준으로 측정 가능하다(양적 쾌락주의). "
                "전제3: 이 기준들을 적용하면 어떤 행위가 더 많은 행복을 산출하는지 계산할 수 있다. "
                "결론: 쾌락 계산(Felicific Calculus)을 통해 도덕적 판단을 객관적으로 수행할 수 있다."
            ),
            "counterpoint": (
                "밀은 '공리주의'에서 벤담의 양적 쾌락 계산을 비판하며 쾌락에는 질적 차이가 있다고 주장했다. "
                "'만족한 돼지보다 불만족한 소크라테스가 낫다'는 명제로, "
                "지적·도덕적 쾌락은 단순 쾌락보다 질적으로 우월하다고 보았다. "
                "무어(G.E. Moore)는 '윤리학 원리'에서 쾌락만이 가치 있는 것이 아니라 지식, 우정, 미적 경험 등 "
                "쾌락 없이도 내재적 가치를 갖는 것들이 있다고 비판했다."
            ),
            "context": "쾌락과 고통의 가치를 측정하는 구체적 방법을 제시함으로써 공리 계산을 실천적으로 수행하는 방법을 논하는 맥락이다.",
            "keywords": ["쾌락 계산", "펠리피직 계산법", "7가지 기준", "양적 공리주의"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "bentham-claim-004",
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "source_detail": "An Introduction to the Principles of Morals and Legislation, Chapter 3",
            "claim": "인간의 행위를 통제하고 도덕을 강제하는 제재(Sanction)는 물리적 제재, 정치적(법적) 제재, 도덕적(사회적) 제재, 종교적 제재의 네 가지이다.",
            "original_text": "Of these several sanctions the names of four may be given... the physical sanction; the political sanction; the moral or popular sanction; the religious sanction.",
            "original_text_ko": "이 여러 제재들의 이름은 다음과 같이 부여될 수 있다... 물리적 제재, 정치적 제재, 도덕적 또는 대중적 제재, 종교적 제재.",
            "explanation": (
                "물리적 제재(physical sanction): 자연적 결과로 인한 쾌락과 고통. 예) 과식하면 배탈이 남. "
                "정치적(법적) 제재(political sanction): 법과 정부에 의한 상벌. 예) 범죄 행위에 대한 법적 처벌. "
                "도덕적(사회적) 제재(moral sanction): 공동체 구성원들의 시인과 부인, 명성과 불명예. 예) 사회적 비난. "
                "종교적 제재(religious sanction): 신의 상벌에 대한 기대. 예) 신의 심판에 대한 두려움. "
                "벤담은 이 네 가지 제재가 서로 보완적으로 작용하여 인간 행동을 공리에 맞게 유도한다고 보았다."
            ),
            "argument": (
                "전제1: 인간은 쾌락을 추구하고 고통을 피하는 존재이므로, 제재는 특정 행동에 쾌락이나 고통을 연결시켜 행동을 통제한다. "
                "전제2: 법만으로는 모든 비공리적 행동을 통제할 수 없으며, 다양한 제재가 필요하다. "
                "전제3: 물리적·정치적·도덕적·종교적 네 가지 제재가 각기 다른 상황에서 작동한다. "
                "결론: 입법자는 이 네 가지 제재를 이해하고 활용하여 공리를 극대화하는 사회 환경을 설계해야 한다."
            ),
            "counterpoint": (
                "칸트는 '도덕형이상학 기초'에서 제재(외부적 강제)에 의한 도덕은 진정한 도덕이 아니라고 비판했다. "
                "진정한 도덕적 행위는 외부 제재에 대한 두려움이나 기대가 아니라, "
                "순수한 의무감(도덕 법칙에 대한 존경심)에서 비롯되어야 한다고 주장했다. "
                "롤스는 '정의론'에서 정의로운 사회 제도는 단순한 제재 체계가 아니라 "
                "구성원들이 자발적으로 동의할 수 있는 공정한 원칙들에 의해 규율되어야 한다고 논했다."
            ),
            "context": "공리주의적 입장에서 인간 행동을 도덕적으로 통제하는 메커니즘을 분석하고, 입법자가 활용할 수 있는 수단을 체계화하는 맥락이다.",
            "keywords": ["제재", "4가지 제재", "물리적 제재", "법적 제재", "도덕적 제재", "종교적 제재"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "bentham-claim-005",
            "thinker_id": "bentham",
            "work_id": "bentham-fragment-on-government",
            "source_detail": "A Fragment on Government, Preface",
            "claim": "어떤 정부 형태가 좋은지 나쁜지를 판단하는 유일한 기준은 최대 다수의 최대 행복(the greatest happiness of the greatest number)이다.",
            "original_text": "it is the greatest happiness of the greatest number that is the measure of right and wrong.",
            "original_text_ko": "최대 다수의 최대 행복이 옳고 그름의 척도이다.",
            "explanation": (
                "벤담은 이 원리를 사회계약론(로크, 루소)이나 자연권론(블랙스톤)에 대한 대안으로 제시했다. "
                "정부의 정당성은 자연권이나 계약에서 오는 것이 아니라, "
                "그것이 실제로 구성원들의 행복을 얼마나 증진하는가에 달려 있다. "
                "'최대 다수'와 '최대 행복'이라는 두 요소는 때로 긴장 관계에 있을 수 있다는 점이 후대에 비판을 받았다."
            ),
            "argument": (
                "전제1: 어떤 법·제도·정책이 옳은지는 그것이 산출하는 결과(행복과 불행)에 의해 판단되어야 한다. "
                "전제2: 사회는 개인들의 집합이므로, 사회적 행복은 구성원들의 개인적 행복의 총합이다. "
                "전제3: 모든 사람의 이익은 동등하게 계산되어야 한다('각자는 하나, 아무도 하나 이상이 아니다'). "
                "결론: 따라서 최대 다수의 최대 행복이 정치 제도와 법률의 목적이자 평가 기준이다."
            ),
            "counterpoint": (
                "롤스는 '정의론'에서 최대 다수의 최대 행복 원리는 소수의 권리를 다수의 이익을 위해 희생시키는 것을 "
                "허용할 수 있어 정의의 요구와 충돌한다고 비판했다. "
                "노직은 '아나키·국가·유토피아'에서 공리 극대화를 위해 개인의 권리를 침해하는 것은 "
                "개인을 목적이 아닌 수단으로 취급하는 것이라고 비판했다. "
                "또한 '최대 다수'와 '최대 행복' 사이의 내적 충돌 문제도 있다—"
                "행복의 양을 최대화하면 숫자는 줄 수도 있고, 숫자를 최대화하면 1인당 행복이 줄 수도 있다."
            ),
            "context": "기존의 자연법·사회계약론적 정치 이론을 비판하고 공리주의적 정치 이론의 토대를 마련하는 맥락이다.",
            "keywords": ["최대 다수의 최대 행복", "공리주의 정치", "행복 원리"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "bentham-claim-006",
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "source_detail": "An Introduction to the Principles of Morals and Legislation, Chapter 1, §4",
            "claim": "공리의 원리에 반대하는 두 가지 원리는 금욕주의의 원리(Principle of Asceticism)와 공감·반감의 원리(Principle of Sympathy and Antipathy)이며, 이 둘은 모두 잘못된 도덕 원리이다.",
            "original_text": "",
            "explanation": (
                "금욕주의 원리: 고통을 산출하는 경향이 있는 행위를 시인하고 쾌락을 산출하는 경향이 있는 행위를 부인한다. "
                "이는 공리 원리와 정반대이다. 벤담은 일부 종교적·철학적 금욕주의가 이 원리를 따른다고 비판한다. "
                "공감·반감의 원리: 어떤 행위가 자신에게 감정적으로 좋은 느낌을 주면 옳고, 나쁜 느낌을 주면 그르다고 판단한다. "
                "이는 사실상 주관적 감정을 도덕의 기준으로 삼는 것으로, 객관적 기준이 없다. "
                "벤담은 도덕 판단에서 유일하게 객관적이고 일관된 기준은 공리 원리뿐이라고 주장한다."
            ),
            "argument": (
                "전제1: 올바른 도덕 원리는 일관성이 있어야 하고 실제 인간 행동의 동기와 연결되어야 한다. "
                "전제2: 금욕주의 원리는 쾌락을 나쁜 것으로 보지만, 실제로 아무도 모든 쾌락을 거부하며 살지 않는다(비일관성). "
                "전제3: 공감·반감의 원리는 개인의 감정적 반응에 불과하여 객관적이고 보편적인 도덕 기준을 제공하지 못한다. "
                "결론: 따라서 공리 원리만이 도덕의 일관되고 객관적인 기준이다."
            ),
            "counterpoint": (
                "흄은 '도덕 원리 탐구'에서 도덕 판단은 이성이 아닌 감정(sentiment)에 근거하며, "
                "이는 공감(sympathy)을 통해 확장된다고 주장했다. 벤담이 비판하는 '공감·반감의 원리'는 "
                "흄의 도덕 감정론과 유사한데, 흄의 관점에서는 공감이 개인적 편견이 아닌 "
                "인류 공통의 도덕적 반응의 토대라고 답할 것이다. "
                "칸트는 도덕 원리는 감정도 결과도 아닌 순수 이성에서 도출되어야 한다고 주장하며, "
                "공리 원리 자체도 경험적 원리이므로 진정한 도덕 법칙이 될 수 없다고 비판했다."
            ),
            "context": "공리의 원리가 다른 잘못된 도덕 원리들에 비해 우월함을 보이기 위해 반대 원리들을 체계적으로 비판하는 맥락이다.",
            "keywords": ["금욕주의의 원리", "공감·반감의 원리", "공리의 원리", "도덕 원리"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "bentham-claim-007",
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "source_detail": "An Introduction to the Principles of Morals and Legislation, Chapter 17, §4",
            "claim": "동물도 고통을 느낄 수 있는 존재이므로, 그들의 고통은 도덕적으로 고려되어야 한다. 문제는 동물이 생각할 수 있는가, 말할 수 있는가가 아니라, 고통을 느낄 수 있는가(Can they suffer?)이다.",
            "original_text": "The question is not, Can they reason? nor, Can they talk? but, Can they suffer?",
            "original_text_ko": "문제는 그들이 이성을 가졌는가도 아니고, 그들이 말할 수 있는가도 아니다. 문제는 그들이 고통을 느낄 수 있는가이다.",
            "explanation": (
                "벤담은 고통과 쾌락을 경험할 수 있는 능력(sentience)이 도덕적 고려의 기준이라고 보았다. "
                "이성이나 언어 능력이 아닌 고통 감수 능력이 기준이 되어야 하며, "
                "동물도 고통을 느낄 수 있으므로 그들의 이익도 도덕적 계산에 포함되어야 한다. "
                "이는 당시로서 매우 혁신적인 주장이었으며, 현대 동물 윤리학의 선구가 되었다."
            ),
            "argument": (
                "전제1: 공리주의에서 도덕적 고려의 대상은 쾌락과 고통을 경험할 수 있는 모든 존재이다. "
                "전제2: 동물은 고통과 쾌락을 경험할 수 있다. "
                "전제3: 이성이나 언어 능력은 도덕적 고려의 기준이 아니다(이 기준을 적용하면 일부 인간도 제외될 수 있다). "
                "결론: 따라서 동물의 고통도 도덕적 계산에 포함되어야 한다."
            ),
            "counterpoint": (
                "칸트는 '도덕형이상학'에서 도덕 공동체의 구성원이 되려면 이성적 행위자(rational agent)여야 한다고 주장했다. "
                "동물은 이성적 행위자가 아니므로 도덕적 의무의 직접적 대상이 아니며, "
                "다만 동물 학대는 인간의 도덕적 감수성을 무디게 만들기 때문에 간접적으로 금지된다고 보았다. "
                "피터 싱어는 '동물 해방'에서 벤담의 이 주장을 계승하여 종차별주의(speciesism)를 비판하고 "
                "동물의 이익도 동등하게 고려되어야 한다는 현대적 동물 권리론을 전개했다."
            ),
            "context": "노예 해방 논의의 맥락에서, 피부색이나 종(species)과 같은 특성이 아닌 고통 감수 능력을 도덕적 고려의 기준으로 제시한 각주에서 나온 주장이다.",
            "keywords": ["동물 윤리", "고통 감수 능력", "공리주의 도덕적 지위", "종차별주의"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "bentham-claim-008",
            "thinker_id": "bentham",
            "work_id": "bentham-panopticon",
            "source_detail": "The Panopticon Writings, Letter I",
            "claim": "판옵티콘(Panopticon)은 중앙 감시탑에서 간수 한 명이 모든 수감자를 볼 수 있지만, 수감자는 감시당하고 있는지 알 수 없는 원형 감옥이다. 이 구조는 최소 비용으로 최대의 감시 효과와 교화를 달성한다.",
            "original_text": "the more constantly the persons to be inspected are under the eyes of the persons who inspect them, the more perfectly will the purpose of the establishment have been attained.",
            "original_text_ko": "감시를 받는 사람들이 감시하는 사람들의 눈 아래 더 지속적으로 놓여 있을수록, 그 시설의 목적은 더 완전하게 달성될 것이다.",
            "explanation": (
                "판옵티콘의 핵심 원리: 피감시자는 항상 감시될 수 있다고 의식하게 되어 스스로 행동을 교정한다(자기 감시). "
                "간수가 항상 볼 필요는 없으며, 볼 수 있다는 가능성만으로도 충분하다. "
                "이는 처벌의 확실성이 엄격성보다 더 중요하다는 공리주의적 형벌론과 연결된다. "
                "벤담은 이를 감옥뿐 아니라 학교, 공장, 병원 등 다양한 감시·관리 시설에 적용할 수 있다고 보았다."
            ),
            "argument": (
                "전제1: 효율적인 교화는 최소 비용으로 최대 효과를 달성해야 한다(공리 원리). "
                "전제2: 범죄 억제는 엄격한 처벌보다 지속적 감시와 처벌의 확실성에서 온다. "
                "전제3: 원형 구조와 역광 조명으로 중앙 감시탑의 감시자는 모든 수감자를 볼 수 있지만, 수감자는 감시자를 볼 수 없다. "
                "전제4: 이 구조로 수감자는 항상 관찰될 수 있다는 인식 아래 스스로 행동을 규율한다. "
                "결론: 판옵티콘은 공리주의적 원리에 따라 최소 비용으로 최대의 교화 효과를 달성하는 이상적 시설 설계이다."
            ),
            "counterpoint": (
                "미셸 푸코는 '감시와 처벌'에서 판옵티콘을 근대 권력의 작동 방식의 상징으로 분석했다. "
                "판옵티콘은 단순한 감옥 설계가 아니라, 권력이 개인의 몸과 정신에 침투하여 스스로 자신을 감시하게 만드는 "
                "'훈육 권력(disciplinary power)'의 원형이라고 주장했다. "
                "이는 벤담이 의도한 공리주의적 효율성보다 더 심층적인 지배와 통제의 메커니즘을 내포한다는 비판이다."
            ),
            "context": "1787년 러시아 방문 중 형의 시설 관리 방법을 관찰하며 영감을 받아 설계한 것으로, 영국 정부에 건축을 제안했지만 결국 실현되지 못했다.",
            "keywords": ["판옵티콘", "감시", "자기 감시", "교화", "훈육 권력"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "bentham-claim-009",
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "source_detail": "An Introduction to the Principles of Morals and Legislation, Chapter 13",
            "claim": "처벌은 그 자체로 고통이므로 악(evil)이지만, 그것이 더 큰 악(범죄)을 방지함으로써 공리를 증가시키는 경우에만 정당화된다. 처벌의 목적은 응보가 아니라 미래 범죄의 억제이다.",
            "original_text": "But all punishment in itself is evil. Upon the principle of utility, if it ought at all to be admitted, it ought only to be admitted in as far as it promises to exclude some greater evil.",
            "original_text_ko": "모든 처벌은 그 자체로 악이다. 공리의 원리에 의하면, 처벌이 허용되어야 한다면, 그것은 오직 그것이 더 큰 악을 배제할 것을 약속하는 한에서만 허용되어야 한다.",
            "explanation": (
                "공리주의적 처벌론의 핵심: 처벌은 과거 잘못에 대한 보복(응보)이 아니라 미래 범죄를 방지하는 도구이다. "
                "처벌이 정당화되려면: (1) 범죄 억제 효과가 있어야 하고, (2) 그 고통이 방지되는 범죄의 고통보다 작아야 하고, "
                "(3) 처벌 외의 방법으로 동일한 목적을 달성할 수 없어야 한다. "
                "처벌의 양은 범죄에서 얻는 이익보다 약간만 더 클 정도로 비례 원칙을 따라야 한다."
            ),
            "argument": (
                "전제1: 처벌은 고통이므로 그 자체로는 공리를 감소시키는 악이다. "
                "전제2: 그러나 처벌이 미래 범죄(더 큰 악)를 방지함으로써 전체적으로 공리를 증가시킬 수 있다. "
                "전제3: 따라서 처벌은 그것이 방지하는 범죄의 해악보다 적은 해악을 가져오는 경우에만 정당화된다. "
                "결론: 처벌의 유일한 정당화 근거는 미래 피해 방지(위하, deterrence)이며, 응보는 정당한 근거가 아니다."
            ),
            "counterpoint": (
                "칸트는 '도덕형이상학'에서 처벌은 오직 범죄자가 그것을 받을 만하기 때문에(응보), "
                "즉 정의의 요구로서 부과되어야 한다고 주장했다. "
                "'사회의 시민 공동체가 해산되더라도 감옥에 있는 마지막 살인자는 처형되어야 한다'는 유명한 언명으로, "
                "처벌의 근거는 미래 이익(억제)이 아닌 과거 행위에 대한 정의의 실현이라고 보았다. "
                "롤스는 처벌의 목적에서 응보와 억제 사이의 긴장을 인정하면서도, "
                "공정한 절차와 원칙에 의해 설계된 처벌 제도가 필요하다고 보았다."
            ),
            "context": "형법과 처벌의 원리를 공리주의적으로 재정립하고, 당시의 가혹하고 비효율적인 영국 형사 제도를 개혁하려는 맥락에서 제시되었다.",
            "keywords": ["공리주의 형벌론", "억제", "응보 부정", "비례 원칙"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "bentham-claim-010",
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "source_detail": "An Introduction to the Principles of Morals and Legislation, Chapter 2",
            "claim": "공동체는 구성원 개인들의 집합체이며, 공동체의 이익은 그 구성원 개인들의 이익의 합계이다. 따라서 사회적 공리란 곧 개인적 공리들의 총합이다.",
            "original_text": "The interest of the community then is, what?—the sum of the interests of the several members who compose it.",
            "original_text_ko": "그렇다면 공동체의 이익이란 무엇인가?—공동체를 구성하는 여러 구성원들의 이익의 합계이다.",
            "explanation": (
                "벤담의 사회 개념은 원자론적(atomistic)이다: 사회는 개인들의 집합에 불과하며, "
                "사회 그 자체는 개인들과 독립된 별도의 이익을 갖지 않는다. "
                "이 원자론적 개인주의로부터 '각자는 하나로 계산되고 아무도 하나 이상으로 계산되지 않는다'는 "
                "평등주의적 원칙이 도출된다. "
                "공리 계산 시 모든 개인의 쾌락과 고통은 동등한 비중으로 고려되어야 한다."
            ),
            "argument": (
                "전제1: '공동체'라는 허구적 몸(fictitious body)의 이익을 이야기하려면, 먼저 개인의 이익이 무엇인지 알아야 한다. "
                "전제2: 공동체는 그것을 구성하는 개인들의 집합이므로, 공동체 전체의 이익은 개인 이익들의 합이다. "
                "전제3: 따라서 공동체의 이익을 증진한다는 것은 그 구성원들의 이익의 총합을 증진하는 것이다. "
                "결론: 입법자는 개인의 이익들을 집계하여 최대 다수의 최대 행복을 달성하도록 정책을 설계해야 한다."
            ),
            "counterpoint": (
                "헤겔은 '법철학'에서 국가(Sittlichkeit)는 개인들의 단순한 집합이 아니라, "
                "개인이 그 안에서만 진정한 자유와 도덕성을 실현할 수 있는 인륜적 공동체라고 비판했다. "
                "공동체는 개인들의 이익의 산술적 합계로 환원될 수 없으며, 공동체 자체가 개인과 구별되는 고유한 가치를 갖는다고 주장했다. "
                "마르크스주의는 개인주의적 공리주의가 자본주의적 이익 관계를 자연화한다고 비판했다."
            ),
            "context": "공리의 원리를 사회 차원으로 확장할 때 사회적 공리가 개인 공리의 합산임을 명확히 하는 맥락이다.",
            "keywords": ["사회적 공리", "원자론적 개인주의", "이익의 합계", "평등주의"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "bentham-claim-011",
            "thinker_id": "bentham",
            "work_id": "bentham-anarchical-fallacies",
            "source_detail": "Anarchical Fallacies, Article II",
            "claim": "자연권(natural rights)은 '횃불 위의 넌센스(nonsense upon stilts)'이다. 권리는 법(실정법)이 존재할 때만 성립하며, 법 이전의 자연 상태에서는 어떤 권리도 존재하지 않는다.",
            "original_text": "Natural rights is simple nonsense: natural and imprescriptible rights, rhetorical nonsense—nonsense upon stilts.",
            "original_text_ko": "자연권은 단순한 넌센스이다. 자연적이고 양도 불가능한 권리는 수사학적 넌센스—횃불 위의 넌센스이다.",
            "explanation": (
                "벤담은 법실증주의(legal positivism)의 입장에서 자연권 개념을 비판한다. "
                "권리는 법적으로 정의된 것이며, 법 없이는 권리도 없다. "
                "프랑스 혁명의 '인간과 시민의 권리 선언'에서 선언된 '자연적·양도 불가능한 권리'는 "
                "실정법의 뒷받침 없이는 공허한 수사에 불과하다. "
                "권리를 창출하고 보장하는 것은 법과 국가이며, '자연 상태'에서는 권리가 아닌 욕망과 힘만이 있다."
            ),
            "argument": (
                "전제1: 권리는 의무에 대응하며, 의무는 법에 의해 강제 가능할 때만 실질적으로 존재한다. "
                "전제2: '자연법'은 실제로 존재하는 법이 아니라 사람들이 자신의 감정이나 견해를 표현하기 위해 사용하는 허구이다. "
                "전제3: 법 없이 권리가 존재한다고 주장하는 것은 아무것도 만들어내지 않으면서 "
                "마치 무언가가 존재하는 것처럼 주장하는 넌센스이다. "
                "결론: 권리는 실정법에 의해 창출되며, 자연권 개념은 법철학적으로 무의미하다."
            ),
            "counterpoint": (
                "로크는 '통치론'에서 자연권(생명·자유·재산)은 신이 부여한 것으로 정부 성립 이전에 존재하며, "
                "이를 보호하기 위해 정부가 구성된다고 주장했다. "
                "롤스는 '정의론'에서 원초적 입장(veil of ignorance)의 사고실험을 통해 "
                "실정법에 선행하는 정의의 원칙들을 도출함으로써, "
                "자연권과 유사한 기본적 자유가 도덕적으로 정당화될 수 있음을 보였다."
            ),
            "context": "프랑스 혁명의 인권 선언을 영국 공리주의 관점에서 비판하는 맥락이다. 벤담은 혁명의 목적(개혁)에는 공감하면서도 그 방법론(자연권 선언)을 비판했다.",
            "keywords": ["자연권 비판", "법실증주의", "실정법", "횃불 위의 넌센스"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "bentham-claim-012",
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "source_detail": "An Introduction to the Principles of Morals and Legislation, Chapter 1, §1-3; Chapter 3",
            "claim": "입법의 목적은 공리의 원리에 따라 공동체 전체의 행복을 증진하는 것이며, 입법자는 쾌락과 고통의 제재를 활용하여 개인의 이익과 공동체 이익이 일치하도록 법 제도를 설계해야 한다.",
            "original_text": "",
            "explanation": (
                "벤담의 입법론: 입법자의 역할은 개인들의 이기적 동기(쾌락 추구, 고통 회피)를 활용하여 "
                "공동체 전체의 공리가 극대화되도록 유인 구조를 설계하는 것이다. "
                "자연 상태에서 개인 이익과 공동체 이익은 충돌할 수 있으므로, "
                "법과 처벌을 통해 이 두 이익이 일치하도록 만들어야 한다. "
                "이는 '인공적 조화(artificial identification of interests)'의 원리이다."
            ),
            "argument": (
                "전제1: 인간은 쾌락을 추구하고 고통을 피하는 이기적 존재이다. "
                "전제2: 개인이 자신의 이익만을 추구하면 타인과 공동체에 해를 끼칠 수 있다. "
                "전제3: 입법은 처벌(법적 제재)을 통해 반사회적 행동에 고통을 부과하고, "
                "친사회적 행동에 쾌락(보상)을 부과함으로써 개인 이익과 공동체 이익을 일치시킬 수 있다. "
                "결론: 입법의 목적은 공리 원리에 따라 개인과 공동체 이익의 인공적 조화를 달성하는 것이다."
            ),
            "counterpoint": (
                "루소는 '사회계약론'에서 입법의 목적이 일반의지(volonté générale)를 실현하는 것이라고 보았다. "
                "이는 단순한 개인 이익의 합산(전체 의지, volonté de tous)이 아닌 진정한 공동선이다. "
                "루소의 관점에서 벤담의 접근은 공동체를 단순한 개인들의 집합으로 보는 원자론적 오류를 범한다. "
                "아담 스미스는 '국부론'에서 시장의 '보이지 않는 손'이 개인 이익 추구를 공동 이익으로 자연스럽게 "
                "전환시키므로, 인위적 입법 조정은 오히려 비효율적일 수 있다고 보았다."
            ),
            "context": "공리주의를 법과 정치 제도에 적용하여 사회 개혁론의 이론적 토대를 마련하는 맥락이다.",
            "keywords": ["입법 원리", "인공적 조화", "법적 제재", "공리주의 정치"],
            "verified": False,
            "verification_log": []
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """벤담 관련 키워드 사전 입력."""
    keywords = [
        {
            "id": "bentham-keyword-001",
            "term": "공리의 원리",
            "term_en": "Principle of Utility",
            "definition": (
                "벤담이 도덕과 입법의 기본 원리로 제시한 것으로, 어떤 행위든 관련 당사자의 행복을 "
                "증가시키거나 감소시키는 경향에 따라 시인하거나 부인하는 원리이다. "
                "나중에 '최대 행복 원리(Greatest Happiness Principle)'라고도 불렸다. "
                "도덕적 판단의 기준은 행위의 결과, 즉 산출되는 쾌락(행복)과 고통(불행)의 총량이다."
            ),
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "related_terms": ["최대 행복 원리", "공리주의", "최대 다수의 최대 행복"]
        },
        {
            "id": "bentham-keyword-002",
            "term": "쾌락 계산",
            "term_en": "Felicific Calculus",
            "definition": (
                "벤담이 제시한 쾌락과 고통의 가치를 측정하는 방법. "
                "강도(intensity), 지속성(duration), 확실성(certainty), 근접성(propinquity), "
                "생산성(fecundity), 순수성(purity), 범위(extent)의 7가지 기준으로 "
                "쾌락과 고통을 양적으로 계산할 수 있다고 보았다. "
                "이를 통해 도덕적 판단을 객관적이고 과학적으로 수행할 수 있다고 주장했다."
            ),
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "related_terms": ["공리의 원리", "양적 공리주의", "행위 공리주의"]
        },
        {
            "id": "bentham-keyword-003",
            "term": "최대 다수의 최대 행복",
            "term_en": "The Greatest Happiness of the Greatest Number",
            "definition": (
                "벤담이 정부와 입법의 목적으로 제시한 원리. 도덕적으로 올바른 행위와 정책은 "
                "가장 많은 사람들에게 가장 큰 행복을 가져다주는 것이어야 한다. "
                "벤담 이전에 프리스틀리(Priestley)가 이 표현을 처음 사용했으나, "
                "벤담이 공리주의 체계의 핵심 원리로 발전시켰다."
            ),
            "thinker_id": "bentham",
            "work_id": "bentham-fragment-on-government",
            "related_terms": ["공리의 원리", "최대 행복 원리", "공리주의"]
        },
        {
            "id": "bentham-keyword-004",
            "term": "행위 공리주의",
            "term_en": "Act Utilitarianism",
            "definition": (
                "개별 행위의 도덕성을 그 행위가 직접 산출하는 쾌락과 고통의 총량으로 판단하는 공리주의 형태. "
                "벤담의 공리주의가 행위 공리주의의 전형으로 분류된다. "
                "규칙 공리주의(rule utilitarianism)와 대비되는 개념으로, "
                "후자는 최대 행복을 산출하는 규칙들을 따를 때 행위가 옳다고 본다. "
                "밀은 벤담의 행위 공리주의를 수정하여 쾌락의 질적 차이와 규칙의 역할을 인정했다."
            ),
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "related_terms": ["규칙 공리주의", "공리주의", "쾌락 계산"]
        },
        {
            "id": "bentham-keyword-005",
            "term": "제재",
            "term_en": "Sanction",
            "definition": (
                "벤담이 인간의 행동을 통제하는 메커니즘으로 제시한 4가지 유형의 상벌 체계. "
                "물리적 제재(자연적 결과), 정치적/법적 제재(법과 정부), "
                "도덕적/사회적 제재(공동체의 시인과 부인), 종교적 제재(신의 상벌)가 있다. "
                "이 네 가지 제재는 서로 보완적으로 작용하여 개인이 공리에 맞는 행동을 하도록 유도한다."
            ),
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "related_terms": ["4가지 제재", "공리의 원리", "입법 원리"]
        },
        {
            "id": "bentham-keyword-006",
            "term": "판옵티콘",
            "term_en": "Panopticon",
            "definition": (
                "벤담이 설계한 원형 감시 시설. 중앙의 감시탑에서 모든 수감자를 볼 수 있지만, "
                "수감자는 감시탑 내부를 볼 수 없어 항상 감시당할 수 있다는 것을 의식하게 된다. "
                "이 '가시성의 권력'을 통해 수감자들이 스스로를 감시하도록 만드는 자기 규율 효과를 낳는다. "
                "미셸 푸코는 이를 근대 권력의 상징으로 분석했다."
            ),
            "thinker_id": "bentham",
            "work_id": "bentham-panopticon",
            "related_terms": ["감시", "자기 규율", "훈육 권력", "공리주의 형벌론"]
        },
        {
            "id": "bentham-keyword-007",
            "term": "심리적 이기주의",
            "term_en": "Psychological Egoism",
            "definition": (
                "모든 인간의 행동은 결국 자신의 쾌락을 극대화하고 고통을 최소화하려는 동기에서 비롯된다는 "
                "기술적(descriptive) 명제. 벤담은 이를 공리주의의 심리학적 토대로 삼았다. "
                "이 명제는 도덕적 규범을 도출하기 위한 사실적 전제로서, "
                "인간이 실제로 이렇게 행동한다는 주장이다(규범적 이기주의와 구별)."
            ),
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "related_terms": ["공리의 원리", "쾌락", "고통", "행위 동기"]
        },
        {
            "id": "bentham-keyword-008",
            "term": "양적 공리주의",
            "term_en": "Quantitative Utilitarianism",
            "definition": (
                "벤담이 주장한 공리주의의 형태로, 쾌락에는 질적 차이가 없고 오직 양적 차이만 있다는 입장. "
                "'시 짓기(pushpin)와 음악은 동등하다'는 벤담의 언명이 이를 잘 보여준다. "
                "쾌락은 오직 강도·지속성 등의 기준으로 측정되어야 하며, 어떤 쾌락이 질적으로 우월하다는 "
                "주장은 기준이 없다고 보았다. 밀은 이에 맞서 질적 공리주의를 제시했다."
            ),
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "related_terms": ["쾌락 계산", "행위 공리주의", "질적 공리주의"]
        },
        {
            "id": "bentham-keyword-009",
            "term": "인공적 이익 조화",
            "term_en": "Artificial Identification of Interests",
            "definition": (
                "벤담의 입법론에서 핵심 개념. 자연 상태에서 개인 이익과 공동체 이익은 충돌할 수 있으나, "
                "법과 제도를 통해 이 두 이익이 일치하도록 인위적으로 조화시킬 수 있다는 원리. "
                "입법자는 쾌락·고통의 제재(특히 법적 제재)를 설계하여 개인이 공동체 이익에 부합하게 행동할 때 "
                "개인 이익도 증가하도록 유인 구조를 만들어야 한다."
            ),
            "thinker_id": "bentham",
            "work_id": "bentham-introduction-principles",
            "related_terms": ["입법 원리", "제재", "공리주의 정치"]
        },
        {
            "id": "bentham-keyword-010",
            "term": "법실증주의",
            "term_en": "Legal Positivism",
            "definition": (
                "법의 타당성은 도덕적·자연법적 기준이 아니라 제정 절차와 형식적 요건에 따라 결정된다는 입장. "
                "벤담은 자연법과 자연권 개념을 거부하고, 실정법(positive law)만이 진정한 법이라고 주장했다. "
                "자연권은 '횃불 위의 넌센스'라고 규정하여, 권리는 오직 국가가 법으로 창출하고 보장할 때만 존재한다고 보았다. "
                "이 입장은 훗날 오스틴(John Austin)과 하트(H.L.A. Hart)의 법실증주의로 계승되었다."
            ),
            "thinker_id": "bentham",
            "work_id": "bentham-anarchical-fallacies",
            "related_terms": ["자연권 비판", "실정법", "자연법", "오스틴"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """벤담 관련 사상 관계 데이터 입력."""
    relations = [
        {
            "id": "relation-epicurus-bentham",
            "from_thinker": "epicurus",
            "to_thinker": "bentham",
            "type": "influenced_by",
            "description": (
                "에피쿠로스의 쾌락주의(hedonism)는 벤담 공리주의의 심리학적 토대에 영향을 주었다. "
                "에피쿠로스가 쾌락을 최고선으로 보고 고통을 악으로 본 것은, "
                "벤담이 쾌락과 고통을 인간 행동의 주권자로 설정한 것과 연결된다. "
                "그러나 에피쿠로스가 사적·정신적 쾌락을 강조한 반면, 벤담은 쾌락을 사회적·양적으로 계산하여 입법에 적용했다는 점에서 다르다."
            ),
            "evidence": "Bentham, An Introduction to the Principles of Morals and Legislation, Ch.1"
        },
        {
            "id": "relation-hume-bentham",
            "from_thinker": "hume",
            "to_thinker": "bentham",
            "type": "influenced_by",
            "description": (
                "흄의 경험주의와 공리 개념이 벤담에게 직접적 영향을 주었다. "
                "벤담은 흄의 '도덕 원리 탐구'를 읽고 공리주의 원리의 단서를 발견했다고 회고했다. "
                "흄의 경험주의적 방법론과 감정에 기반한 도덕론은 벤담이 경험적·과학적 도덕론을 구성하는 데 영향을 주었다. "
                "그러나 흄이 이성의 역할을 제한하고 감정을 도덕의 원천으로 본 반면, "
                "벤담은 공리 계산이라는 이성적 절차를 도덕의 기준으로 삼았다는 점에서 차이가 있다."
            ),
            "evidence": "Bentham, Introduction to the Principles of Morals and Legislation, footnote to Chapter 1"
        },
        {
            "id": "relation-bentham-mill-js",
            "from_thinker": "bentham",
            "to_thinker": "mill_js",
            "type": "influenced",
            "description": (
                "존 스튜어트 밀은 벤담의 제자 제임스 밀의 아들로, 벤담 공리주의의 직접적 계승자이다. "
                "밀은 '공리주의'(1863)에서 벤담의 양적 공리주의를 계승하면서도, "
                "쾌락의 질적 차이를 인정하고('만족한 돼지보다 불만족한 소크라테스가 낫다'), "
                "내적 제재(양심의 가책)를 강조하고, 규칙 공리주의적 요소를 도입하여 공리주의를 더 세련되게 발전시켰다."
            ),
            "evidence": "Mill, J.S., Utilitarianism (1863), Chapter 2"
        },
        {
            "id": "relation-bentham-kant",
            "from_thinker": "bentham",
            "to_thinker": "kant",
            "type": "criticized",
            "description": (
                "벤담의 공리주의와 칸트의 의무론은 서로 대립하는 윤리 체계이다. "
                "벤담은 칸트 방식의 의무론이 행위의 결과를 무시하고 추상적 원리에 집착한다는 점을 비판했으며, "
                "자연권과 같은 형이상학적 개념을 '넌센스'로 규정했다. "
                "반대로 칸트는 쾌락·결과 중심의 도덕론이 보편적 도덕 법칙의 근거를 제공할 수 없다고 비판했다. "
                "두 사상가의 대립은 결과론 대 의무론의 핵심 쟁점을 대표한다."
            ),
            "evidence": "Bentham, An Introduction to the Principles of Morals and Legislation, Ch.1; Kant, Groundwork for the Metaphysics of Morals"
        },
        {
            "id": "relation-bentham-rousseau",
            "from_thinker": "bentham",
            "to_thinker": "rousseau",
            "type": "criticized",
            "description": (
                "벤담은 루소의 사회계약론과 일반의지 개념을 허구적이고 위험한 것으로 비판했다. "
                "특히 프랑스 혁명에서 루소의 사상이 자연권 선언과 결합하여 '무정부적 오류'를 낳았다고 보았다. "
                "사회를 원자론적 개인들의 집합으로 본 벤담과 달리, 루소는 개인을 초월하는 일반의지가 존재한다고 주장했다. "
                "벤담은 일반의지와 같은 허구적 집합 개념 대신 개인 이익의 실증적 집계를 기반으로 한 정치론을 주장했다."
            ),
            "evidence": "Bentham, Anarchical Fallacies; Bentham, Fragment on Government"
        }
    ]

    for rel in relations:
        result = client.index(index=INDEX_RELATIONS, id=rel["id"], document=rel)
        print(f"[relation] {rel['id']}: {result['result']}")

    return len(relations)


def main():
    """메인 실행 함수."""
    print("=== 벤담(Jeremy Bentham) 데이터 ES 입력 시작 ===\n")

    client = get_client()

    try:
        # 1. 사상가
        print("--- 사상가 입력 ---")
        insert_thinker(client)

        # 2. 저서
        print("\n--- 저서 입력 ---")
        works_count = insert_works(client)
        print(f"저서 {works_count}건 입력 완료")

        # 3. 핵심 주장
        print("\n--- 핵심 주장 입력 ---")
        claims_count = insert_claims(client)
        print(f"주장 {claims_count}건 입력 완료")

        # 4. 키워드
        print("\n--- 키워드 입력 ---")
        keywords_count = insert_keywords(client)
        print(f"키워드 {keywords_count}건 입력 완료")

        # 5. 관계
        print("\n--- 사상 관계 입력 ---")
        relations_count = insert_relations(client)
        print(f"관계 {relations_count}건 입력 완료")

        print("\n=== 벤담 데이터 입력 완료 ===")
        print(f"총계: 사상가 1, 저서 {works_count}, 주장 {claims_count}, 키워드 {keywords_count}, 관계 {relations_count}")

    except Exception as e:
        print(f"[ERROR] {e}")
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
