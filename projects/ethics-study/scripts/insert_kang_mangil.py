"""강만길(姜萬吉) 데이터를 ES에 직접 입력하는 스크립트.

field: unification_edu (통일교육)
- 분단시대 사학, 통일지향 역사학, 민중적 민족주의, 내재적 발전론, 평화통일론 중심.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS, INDEX_FIELDS
)


def ensure_field(client):
    """unification_edu 분야가 이미 있는지 확인 (있어야 정상)."""
    try:
        client.get(index=INDEX_FIELDS, id="unification_edu")
        print("[field] unification_edu: 이미 존재")
    except Exception:
        doc = {
            "id": "unification_edu",
            "name": "통일교육",
            "description": "분단체제론·통일지향 역사학 등 한국 통일 담론",
            "order": 6
        }
        client.index(index=INDEX_FIELDS, id="unification_edu", document=doc)
        print("[field] unification_edu: created")


def insert_thinker(client):
    """강만길 사상가 데이터 입력."""
    doc = {
        "id": "kang_mangil",
        "name": "강만길 (姜萬吉)",
        "name_en": "Kang Man-gil",
        "field": "unification_edu",
        "era": "현대",
        "birth_year": 1933,
        "death_year": 2023,
        "background": (
            "강만길은 경상남도 마산에서 태어난 한국 현대의 대표적 역사학자이다. "
            "고려대학교 사학과를 졸업하고 같은 대학에서 박사학위를 받았으며, "
            "고려대학교 사학과 교수로 재직하며 한국근현대사 연구를 주도했다. "
            "1980년 광주민주화운동 이후 해직교수로 고초를 겪었으며, "
            "1984년 복직 후에는 '분단시대'라는 개념을 통해 "
            "분단 극복과 통일을 지향하는 역사학의 새로운 패러다임을 제시했다. "
            "친일반민족행위진상규명위원회 위원장, 민족문제연구소 이사장 등을 역임하며 "
            "역사 연구와 실천을 결합한 지식인의 모범을 보였다. "
            "『분단시대의 역사인식』(1978), 『한국민족운동사론』(1985), "
            "『고쳐 쓴 한국현대사』(1994) 등 한국 근현대사학의 흐름을 바꾼 저작들을 남겼다."
        ),
        "core_philosophy": (
            "강만길 사학의 핵심은 '분단시대'라는 시대규정과 "
            "'통일지향 역사학(통일사학)'의 정립이다. "
            "그는 해방 이후의 한국사를 '분단시대'로 규정함으로써, "
            "분단체제가 단순한 정치적 상태가 아니라 "
            "한국인의 역사 인식과 학문 전체를 구속해 온 역사적 조건임을 드러냈다. "
            "따라서 역사학은 분단을 당연시하거나 한쪽의 정통성만을 옹호하는 '분단 사학'을 넘어, "
            "민족 구성원 전체의 삶과 통일을 지향하는 관점에서 "
            "근현대사를 다시 서술해야 한다고 주장한다. "
            "이 관점은 민중을 역사의 주체로 삼는 '민중적 민족주의', "
            "조선후기 이래의 자생적 근대 맹아를 강조하는 '내재적 발전론', "
            "그리고 흡수통일이 아닌 평화·대등통일을 지향하는 '평화통일론'으로 구체화된다."
        ),
        "philosophical_journey": (
            "초기(조선후기 상공업사 연구, 1960~1970년대 전반): 조선후기 상업자본의 발달과 "
            "수공업·광업사를 실증적으로 연구하며 내재적 발전론의 경험적 토대를 다졌다. "
            "식민사관의 정체성론을 비판하고 조선후기 사회의 내적 발전 동력을 밝히는 데 집중했다. "
            "중기(분단시대론 정립, 1970년대 후반~1980년대): 1978년 『분단시대의 역사인식』을 출간하여 "
            "해방 이후를 '분단시대'로 규정하고 통일지향 역사학의 틀을 제시했다. "
            "1980년대 해직·복직의 시련을 겪으며 역사학의 실천적 성격을 더욱 강조했고, "
            "민중을 민족운동의 주체로 재평가하는 민중적 민족주의 사관을 발전시켰다. "
            "후기(평화통일과 역사 청산, 1990년대 이후): 냉전 해체와 남북 화해 국면에서 "
            "흡수통일이 아닌 평화·대등통일의 역사적 정당성을 논증하고, "
            "친일반민족행위 진상규명 등 과거사 청산 작업에 참여하며 "
            "역사학이 현재의 공동체 과제와 어떻게 결합해야 하는지를 실천적으로 보여주었다."
        ),
        "keywords": [
            "분단시대",
            "통일지향 역사학",
            "통일사학",
            "분단 사학",
            "민중적 민족주의",
            "내재적 발전론",
            "식민사관 비판",
            "자본주의 맹아론",
            "평화통일론",
            "대등통일",
            "민족해방운동사",
            "친일 청산",
            "역사학의 실천성"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="kang_mangil", document=doc)
    print(f"[thinker] kang_mangil: {result['result']}")
    return result


def insert_works(client):
    """강만길 저서 데이터 입력."""
    works = [
        {
            "id": "kang-mangil-bundan-sidae",
            "thinker_id": "kang_mangil",
            "title": "분단시대의 역사인식",
            "title_original": "分斷時代의 歷史認識",
            "year": 1978,
            "significance": (
                "강만길 사학의 출발점이자 한국 근현대사학의 전환점이 된 저작. "
                "해방 이후의 한국사를 '분단시대'로 규정하고, "
                "기존의 '해방 후 사학'이 사실상 남·북 어느 한쪽의 정통성을 옹호하는 "
                "'분단 사학'으로 기능해 왔음을 비판했다. "
                "통일을 지향하는 관점에서 근현대사를 재서술해야 한다는 "
                "'통일지향 역사학'의 선언적 저작으로 읽힌다."
            ),
            "key_concepts": [
                "분단시대", "분단 사학", "통일지향 역사학",
                "민족주의 사학", "역사학의 현재성"
            ]
        },
        {
            "id": "kang-mangil-minjok-undongsa",
            "thinker_id": "kang_mangil",
            "title": "한국민족운동사론",
            "title_original": "韓國民族運動史論",
            "year": 1985,
            "significance": (
                "한국 근현대 민족운동을 '민중'을 주체로 재구성한 논문집. "
                "항일 독립운동, 해방 전후의 좌우 민족운동, 통일운동을 "
                "지배 엘리트의 운동이 아니라 민중적 민족주의의 계보로 재평가했다. "
                "이 저작을 통해 민족운동사 연구의 시각이 "
                "국가·엘리트 중심에서 민중·통일 지향으로 이동하는 계기가 마련되었다."
            ),
            "key_concepts": [
                "민중적 민족주의", "민족운동사", "좌우합작",
                "통일전선", "민족해방운동"
            ]
        },
        {
            "id": "kang-mangil-gochyeo-hyeondaesa",
            "thinker_id": "kang_mangil",
            "title": "고쳐 쓴 한국현대사",
            "title_original": "고쳐 쓴 韓國現代史",
            "year": 1994,
            "significance": (
                "해방 이후 한국현대사를 분단시대론의 관점에서 다시 쓴 개설서. "
                "냉전 해체와 남북 관계 변화라는 새로운 조건 속에서 "
                "기존 현대사 서술의 분단 편향을 교정하고, "
                "남·북을 대등한 역사 주체로 다루는 통일지향 현대사 서술의 모델을 제시했다."
            ),
            "key_concepts": [
                "한국현대사", "분단시대 서술", "남북 대등",
                "통일지향 서술", "현대사 개설"
            ]
        },
        {
            "id": "kang-mangil-20segi-uri-yeoksa",
            "thinker_id": "kang_mangil",
            "title": "20세기 우리 역사",
            "title_original": "20世紀 우리 歷史",
            "year": 1999,
            "significance": (
                "일반 독자를 대상으로 한 20세기 한국사 강의록. "
                "식민지 지배 — 해방 — 분단 — 전쟁 — 독재 — 민주화 — 통일 전망으로 이어지는 "
                "20세기 한국사를 민중과 민족의 시각에서 서술했다. "
                "대중을 위한 역사학의 실천이라는 강만길 사학의 공공성 지향을 잘 보여준다."
            ),
            "key_concepts": [
                "20세기 한국사", "대중 역사학", "민중의 시각",
                "통일 전망", "역사 대중화"
            ]
        },
        {
            "id": "kang-mangil-tongil-undongsa",
            "thinker_id": "kang_mangil",
            "title": "통일운동사",
            "title_original": "統一運動史",
            "year": 2003,
            "significance": (
                "해방 이후 한국 통일운동의 흐름을 체계적으로 정리한 저작. "
                "좌우합작운동, 남북협상, 4·19 이후의 통일운동, 7·4 공동성명, 6·15 공동선언 등 "
                "주요 국면을 '평화·대등통일'의 계보로 재구성했다. "
                "흡수통일론에 맞서 평화통일론의 역사적 정당성을 논증한 대표 저작."
            ),
            "key_concepts": [
                "통일운동사", "평화통일론", "대등통일",
                "좌우합작", "6·15 공동선언"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """강만길 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 분단시대론 — 해방 이후는 '분단시대'이다
        {
            "id": "kang-mangil-claim-001",
            "thinker_id": "kang_mangil",
            "work_id": "kang-mangil-bundan-sidae",
            "source_detail": "분단시대의 역사인식, 서문 및 1부",
            "claim": (
                "해방 이후의 한국사는 단순한 '해방 후'가 아니라 '분단시대'로 규정되어야 한다. "
                "분단은 끝난 역사적 사건이 아니라 지금도 남·북 민족 구성원 전체의 삶과 사고를 "
                "구속하고 있는 역사적 조건이며, 이를 시대 규정으로 삼아야 그 극복도 역사학의 과제로 설정된다."
            ),
            "explanation": (
                "강만길은 '해방 후 사학'이라는 기존의 시대 구분이 "
                "분단의 지속성과 극복 과제를 시야에서 놓친다고 본다. "
                "반면 '분단시대'라는 규정은 첫째, 분단이 1945년에 끝난 일회적 사건이 아니라 "
                "이후 수십 년간 한국 사회 전체를 규정해 온 구조임을 드러내고, "
                "둘째, 이 구조를 극복하는 통일이 역사학의 현재적 과제임을 분명히 한다. "
                "따라서 분단시대론은 시대 구분론이자 동시에 역사학의 실천 강령이다."
            ),
            "argument": (
                "강만길은 남·북 각각의 역사 서술이 "
                "상대방을 부정하거나 왜곡하는 '분단 사학'의 형태로 전개되어 왔음을 지적한다. "
                "이는 학문 내적으로는 사실의 왜곡을, 실천적으로는 분단의 재생산을 낳는다. "
                "분단시대라는 시대 규정은 이 분단 사학을 자각하고 넘어서기 위한 "
                "메타적 인식의 틀로 제시된다."
            ),
            "counterpoint": (
                "일부 연구자는 '분단시대'라는 규정이 "
                "모든 현상을 분단이라는 단일 틀로 환원할 위험이 있고, "
                "남·북 각각의 내부 모순(권위주의, 인권 문제 등)을 과소평가할 수 있다고 비판한다. "
                "또한 냉전 해체 이후에는 '분단시대' 규정의 설명력이 약화되었다는 지적도 있다."
            ),
            "context": (
                "1970년대 후반은 유신체제 말기이자 남북 대화가 잠시 시도된 시점으로, "
                "분단의 지속성과 극복 가능성이 지식인들 사이에서 새롭게 문제화된 시기였다. "
                "강만길은 이 문제의식을 역사학의 시대구분론으로 끌어올렸다."
            ),
            "keywords": ["분단시대", "분단 사학", "시대구분", "해방 후 사학 비판"],
            "verified": False
        },
        # CLAIM-002: 통일지향 역사학(통일사학)
        {
            "id": "kang-mangil-claim-002",
            "thinker_id": "kang_mangil",
            "work_id": "kang-mangil-bundan-sidae",
            "source_detail": "분단시대의 역사인식, 2부",
            "claim": (
                "역사학은 남·북 어느 한쪽의 정통성을 옹호하는 '분단 사학'을 넘어, "
                "민족 구성원 전체의 삶과 통일을 지향하는 '통일지향 역사학(통일사학)'으로 재편되어야 한다. "
                "통일사학은 분단 이전의 민족사와 분단 이후 남북 양쪽의 역사를 "
                "통일이라는 미래 지평에서 재구성하는 역사학이다."
            ),
            "explanation": (
                "통일지향 역사학은 세 가지 과제를 가진다. "
                "첫째, 남·북 각각의 역사 서술이 품고 있는 분단 편향을 비판적으로 검토한다. "
                "둘째, 분단 이전의 근대사(특히 민족해방운동사)를 "
                "좌우 어느 한쪽의 전유물이 아니라 민족 전체의 자산으로 재평가한다. "
                "셋째, 해방 이후의 남·북 역사를 대등한 두 역사 주체로 다루며, "
                "미래의 통일을 지향하는 서술 틀을 모색한다."
            ),
            "argument": (
                "강만길은 역사학이 단순한 과거 복원이 아니라 "
                "현재 공동체의 과제와 결합될 때에만 학문적 생명력을 갖는다고 본다. "
                "분단이 지속되는 한 한국 역사학의 최대 현재적 과제는 통일이며, "
                "따라서 역사학은 통일지향성을 자신의 방법적 원리로 삼아야 한다고 주장한다."
            ),
            "counterpoint": (
                "통일지향성을 학문의 원리로 내세우는 것이 "
                "가치 개입을 과도하게 허용하여 실증성을 훼손할 수 있다는 비판이 있다. "
                "또한 '통일'이라는 목표 자체가 정치적으로 논쟁적이므로 "
                "이를 역사학의 전제로 삼는 것이 부적절하다는 지적도 있다."
            ),
            "context": (
                "강만길의 통일사학 주장은 1970~80년대 민족사학 논쟁, "
                "특히 민중사학·민족주의 사학의 흐름과 공명하며 발전했다."
            ),
            "keywords": ["통일지향 역사학", "통일사학", "분단 사학", "민족사"],
            "verified": False
        },
        # CLAIM-003: 민중적 민족주의
        {
            "id": "kang-mangil-claim-003",
            "thinker_id": "kang_mangil",
            "work_id": "kang-mangil-minjok-undongsa",
            "source_detail": "한국민족운동사론, 서론 및 1부",
            "claim": (
                "한국 근현대 민족운동의 진정한 주체는 지배 엘리트나 특정 정치 세력이 아니라 "
                "역사 속에서 고난을 겪고 싸워 온 '민중'이다. "
                "민족주의는 지배층의 국가주의가 아니라 민중의 해방과 통일 요구를 담는 "
                "'민중적 민족주의'로 재정의되어야 한다."
            ),
            "explanation": (
                "강만길은 민족운동사 서술이 흔히 몇몇 엘리트 지도자나 정통 계보 중심으로 "
                "서술되는 것을 비판한다. "
                "실제 항일운동, 해방 전후의 민족운동, 통일운동의 실질적 동력은 "
                "농민·노동자·학생 등 민중이었으며, "
                "이들의 운동은 국가 건설보다는 생존·자유·평등·통일을 지향했다. "
                "따라서 민족주의는 국가주의적 민족주의가 아니라 "
                "민중의 이러한 요구를 담는 민중적 민족주의로 재구성되어야 한다."
            ),
            "argument": (
                "강만길은 1920~30년대 항일 농민·노동 운동, 해방 직후의 좌우합작 운동, "
                "4·19 이후의 민주·통일 운동 등 다양한 사례를 통해 "
                "민중이 민족운동의 주체로 지속적으로 등장해 왔음을 실증한다. "
                "이를 통해 민족주의를 지배층의 이념이 아니라 민중의 해방 이념으로 재전유한다."
            ),
            "counterpoint": (
                "'민중'이라는 범주가 지나치게 포괄적이고 이상화되어 "
                "실제 사회적 분화와 갈등을 단순화한다는 비판이 있다. "
                "또한 민족주의 자체의 배타성 문제를 민중 개념만으로 해결할 수 없다는 지적도 있다."
            ),
            "context": (
                "1980년대 민주화 운동기에는 민중 개념이 사회과학·역사학 전반에서 "
                "분석 범주로 자리잡았고, 강만길은 이를 민족운동사 서술에 적용했다."
            ),
            "keywords": ["민중적 민족주의", "민중", "민족운동사", "민족주의 재정의"],
            "verified": False
        },
        # CLAIM-004: 내재적 발전론과 식민사관 비판
        {
            "id": "kang-mangil-claim-004",
            "thinker_id": "kang_mangil",
            "work_id": "kang-mangil-bundan-sidae",
            "source_detail": "분단시대의 역사인식, 내재적 발전론 관련 장",
            "claim": (
                "조선후기 이래 한국 사회는 내부로부터 근대적 발전의 맹아를 키워 왔으며, "
                "식민지 지배가 이를 왜곡·중단시켰다. "
                "식민사관의 '정체성론'과 '타율성론'은 식민 지배를 정당화하기 위한 이데올로기이며, "
                "한국사는 내재적 발전의 관점에서 재서술되어야 한다."
            ),
            "explanation": (
                "강만길의 초기 연구 주제였던 조선후기 상공업사, 광업사 연구는 "
                "내재적 발전론의 경험적 토대가 되었다. "
                "그는 조선후기에 상업자본, 수공업, 광업, 신분제 동요 등에서 "
                "자생적 근대 맹아가 성장하고 있었음을 실증하고, "
                "이를 기반으로 식민사관이 주장한 한국사의 '정체성'과 '타율성'을 반박한다. "
                "한국 근대의 좌절은 내재적 발전 동력의 부재가 아니라 식민 지배라는 외적 요인 때문이다."
            ),
            "argument": (
                "강만길은 식민사관의 한국사 해석이 식민 지배를 "
                "'외부에서 주어진 근대화'로 미화하는 기능을 한다고 본다. "
                "내재적 발전론은 이 기능을 해체하고 한국사의 주체성을 회복하는 역사학적 작업이다. "
                "이는 단순한 민족주의적 감정이 아니라 실증적 연구에 기반을 둔 재해석이다."
            ),
            "counterpoint": (
                "1990년대 이후에는 내재적 발전론의 '맹아' 개념이 과대평가되었고, "
                "조선후기의 상공업 발전을 자본주의 이행으로 곧바로 연결하기 어렵다는 비판이 제기되었다. "
                "탈민족주의 사학은 내재적 발전론이 또 다른 목적론적 서술이 될 위험을 지적한다."
            ),
            "context": (
                "내재적 발전론은 1960~70년대 김용섭·강만길 등 한국 근대사학자들이 "
                "식민사관을 극복하기 위해 공동으로 발전시킨 패러다임이다."
            ),
            "keywords": ["내재적 발전론", "식민사관 비판", "자본주의 맹아론", "주체적 근대화"],
            "verified": False
        },
        # CLAIM-005: 평화통일론·대등통일론
        {
            "id": "kang-mangil-claim-005",
            "thinker_id": "kang_mangil",
            "work_id": "kang-mangil-tongil-undongsa",
            "source_detail": "통일운동사, 결론부",
            "claim": (
                "한반도의 통일은 어느 한쪽이 다른 한쪽을 흡수하는 흡수통일이 아니라, "
                "남·북이 대등한 역사적·정치적 주체로 참여하는 평화통일이어야 한다. "
                "이는 단순한 현실적 선택이 아니라 분단시대 민족사의 귀결로서 역사적 정당성을 갖는다."
            ),
            "explanation": (
                "강만길은 통일운동사를 흡수통일 계열과 평화·대등통일 계열로 구분하고, "
                "해방 이후 좌우합작운동, 남북협상, 7·4 공동성명, 6·15 공동선언 등이 "
                "평화·대등통일의 계보를 이루어 왔음을 보인다. "
                "그는 흡수통일이 승자의 논리를 정당화하면서 패자의 역사적 경험을 지워 버리는 반면, "
                "평화통일은 남·북 모두의 역사와 주민의 삶을 온전히 껴안는 방식임을 강조한다."
            ),
            "argument": (
                "강만길은 역사적 정당성과 현실적 합리성 양면에서 평화통일이 요구된다고 본다. "
                "역사적으로 민중적 민족운동의 주류는 좌우합작과 평화통일을 지향해 왔고, "
                "현실적으로도 흡수통일은 막대한 사회적 비용과 폭력을 동반한다. "
                "따라서 평화·대등통일은 역사학이 도출하는 통일 전략이다."
            ),
            "counterpoint": (
                "평화·대등통일론은 북한 체제의 인권·정치 문제를 "
                "대등성의 이름으로 눈감아 준다는 비판을 받기도 한다. "
                "또한 남북 간 경제·사회적 격차가 커질수록 '대등' 전제가 현실성을 잃는다는 지적도 있다."
            ),
            "context": (
                "강만길의 평화통일론은 1990년대 이후의 남북 화해 국면, "
                "특히 2000년 6·15 공동선언 전후에 학술적·실천적으로 활발히 제기되었다."
            ),
            "keywords": ["평화통일론", "대등통일", "흡수통일 비판", "6·15 공동선언", "통일운동사"],
            "verified": False
        },
        # CLAIM-006: 역사학의 실천성과 현재성
        {
            "id": "kang-mangil-claim-006",
            "thinker_id": "kang_mangil",
            "work_id": "kang-mangil-bundan-sidae",
            "source_detail": "분단시대의 역사인식, 서문",
            "claim": (
                "역사학은 과거의 객관적 복원에 머물지 않고, "
                "현재 공동체의 과제와 결합되어 '현재성'과 '실천성'을 가져야 한다. "
                "분단시대 한국 역사학의 현재적 과제는 분단 극복과 통일이며, "
                "역사 연구는 이 과제에 응답하는 방식으로 수행되어야 한다."
            ),
            "explanation": (
                "강만길은 실증주의 사학이 주장하는 '가치중립적 역사학'을 비판적으로 재검토한다. "
                "모든 역사 서술은 특정한 현재적 문제의식 속에서 선택되고 조직된 해석이며, "
                "가치중립의 외피 뒤에 숨은 보수적 현상유지의 입장을 드러내는 것이 먼저 필요하다. "
                "그 위에서 역사학자는 자신의 현재적 문제의식(분단 극복, 민주화, 인권 등)을 "
                "자각적으로 드러내고 연구에 반영해야 한다."
            ),
            "argument": (
                "강만길 자신의 경력 — 해직교수로서의 경험, "
                "친일반민족행위진상규명위원회 활동, 통일운동 참여 — 은 "
                "이러한 실천적 역사학의 모범 사례로 제시된다. "
                "역사학은 서재 속 학문이 아니라 현재 공동체의 집단적 자기이해와 결합되어야 한다."
            ),
            "counterpoint": (
                "역사학의 실천성을 과도하게 강조하면 "
                "특정한 정치적 입장에 학문이 도구화될 위험이 있다는 비판이 있다. "
                "실증성과 실천성 사이의 긴장을 어떻게 유지할지가 지속적 과제로 남는다."
            ),
            "context": (
                "강만길의 실천적 역사학 구상은 "
                "1980년대 해직·복직 경험과 민주화 운동기의 지식인 담론에서 정교화되었다."
            ),
            "keywords": ["역사학의 실천성", "역사의 현재성", "실증주의 비판", "지식인의 역할"],
            "verified": False
        },
        # CLAIM-007: 친일 청산과 과거사 정리
        {
            "id": "kang-mangil-claim-007",
            "thinker_id": "kang_mangil",
            "work_id": "kang-mangil-gochyeo-hyeondaesa",
            "source_detail": "고쳐 쓴 한국현대사, 해방 직후 장",
            "claim": (
                "해방 직후 이루어지지 못한 친일반민족행위 청산은 "
                "분단체제의 형성과 현대사의 왜곡을 낳은 근본 원인 중 하나이다. "
                "따라서 늦었지만 지금이라도 친일 청산을 포함한 과거사 정리는 "
                "통일지향 역사학의 핵심 과제이다."
            ),
            "explanation": (
                "강만길은 반민특위 해체와 친일 세력의 국가기구 재편입이 "
                "해방 공간에서 민족·민주 세력의 약화와 분단 고착화를 가속했다고 분석한다. "
                "이 왜곡이 이후 현대사의 여러 파행 — 분단의 고착, 독재의 장기화, "
                "민족정기의 훼손 — 으로 이어졌다. "
                "과거사 정리는 단순한 과거 보복이 아니라 "
                "공동체의 역사적 정체성을 재정립하고 통일 기반을 만드는 작업이다."
            ),
            "argument": (
                "강만길은 친일반민족행위진상규명위원회 위원장 활동을 통해 "
                "이 주장을 실천으로 옮겼다. "
                "역사학이 과거사 정리 법제와 절차에 이론적·실증적 근거를 제공함으로써 "
                "공동체의 도덕적 재건에 기여할 수 있음을 보였다."
            ),
            "counterpoint": (
                "과거사 정리가 정치적으로 이용되어 "
                "현재의 정치적 반대파를 공격하는 도구가 된다는 비판이 있다. "
                "또한 세대가 바뀐 시점에서의 소급적 청산이 "
                "법적·윤리적으로 정당한지에 대한 논쟁이 존재한다."
            ),
            "context": (
                "2000년대 참여정부기의 과거사 정리 법제화 국면에서 "
                "강만길의 주장은 제도적 뒷받침을 얻었다."
            ),
            "keywords": ["친일 청산", "과거사 정리", "반민특위", "역사 정의"],
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """강만길 키워드 데이터 입력."""
    keywords = [
        {
            "id": "kang-mangil-kw-bundan-sidae",
            "term": "분단시대",
            "term_en": "Age of Division",
            "definition": (
                "강만길이 해방 이후의 한국사를 규정하기 위해 제시한 개념. "
                "분단은 1945년의 일회적 사건이 아니라 "
                "이후 남·북 민족 구성원 전체의 삶과 사고를 구속해 온 역사적 조건이며, "
                "이를 시대 규정으로 삼아야 극복 과제도 역사학의 과제로 설정된다는 인식을 담는다."
            ),
            "thinker_id": "kang_mangil",
            "work_id": "kang-mangil-bundan-sidae",
            "related_terms": ["통일지향 역사학", "분단 사학", "통일사학"]
        },
        {
            "id": "kang-mangil-kw-tongil-sahak",
            "term": "통일지향 역사학",
            "term_en": "Reunification-oriented Historiography",
            "definition": (
                "분단 사학을 극복하고 민족 구성원 전체의 삶과 통일을 지향하는 관점에서 "
                "한국 근현대사를 재서술하려는 역사학. 강만길 사학의 방법적 원리."
            ),
            "thinker_id": "kang_mangil",
            "work_id": "kang-mangil-bundan-sidae",
            "related_terms": ["분단시대", "분단 사학", "평화통일론", "통일사학"]
        },
        {
            "id": "kang-mangil-kw-bundan-sahak",
            "term": "분단 사학",
            "term_en": "Divisionist Historiography",
            "definition": (
                "남·북 어느 한쪽의 정통성만을 옹호하고 상대방을 부정·왜곡하는 방식으로 "
                "전개되는 역사학. 강만길이 통일지향 역사학을 대비시키기 위해 "
                "비판적으로 명명한 개념."
            ),
            "thinker_id": "kang_mangil",
            "work_id": "kang-mangil-bundan-sidae",
            "related_terms": ["분단시대", "통일지향 역사학"]
        },
        {
            "id": "kang-mangil-kw-minjung-minjokjueui",
            "term": "민중적 민족주의",
            "term_en": "People-centered Nationalism",
            "definition": (
                "민족운동의 주체를 지배 엘리트가 아닌 '민중'으로 설정하고, "
                "민족주의를 국가주의가 아니라 민중의 해방·통일 요구로 재정의하는 입장. "
                "강만길의 민족운동사 서술의 핵심 관점."
            ),
            "thinker_id": "kang_mangil",
            "work_id": "kang-mangil-minjok-undongsa",
            "related_terms": ["민중", "민족운동사", "통일지향 역사학"]
        },
        {
            "id": "kang-mangil-kw-naejae-baljeon",
            "term": "내재적 발전론",
            "term_en": "Theory of Internal Development",
            "definition": (
                "조선후기 이래 한국 사회 내부에 근대적 발전의 맹아가 성장하고 있었으며, "
                "식민 지배가 이를 왜곡·중단시켰다고 보는 역사 해석. "
                "강만길·김용섭 등이 식민사관의 정체성론·타율성론을 극복하기 위해 발전시켰다."
            ),
            "thinker_id": "kang_mangil",
            "work_id": "kang-mangil-bundan-sidae",
            "related_terms": ["식민사관 비판", "자본주의 맹아론", "주체적 근대화"]
        },
        {
            "id": "kang-mangil-kw-pyeonghwa-tongil",
            "term": "평화통일론",
            "term_en": "Peaceful Reunification Theory",
            "definition": (
                "흡수통일이 아니라 남·북이 대등한 주체로 참여하는 평화적 통일을 지향하는 입장. "
                "강만길은 좌우합작운동·남북협상·6·15 공동선언 등을 "
                "평화·대등통일의 역사적 계보로 재구성했다."
            ),
            "thinker_id": "kang_mangil",
            "work_id": "kang-mangil-tongil-undongsa",
            "related_terms": ["대등통일", "흡수통일 비판", "6·15 공동선언", "통일운동사"]
        },
        {
            "id": "kang-mangil-kw-silcheonsung",
            "term": "역사학의 실천성",
            "term_en": "Praxis-orientation of Historiography",
            "definition": (
                "역사학은 과거의 객관적 복원에만 머물지 않고 "
                "현재 공동체의 과제(분단 극복·민주화·과거사 청산 등)와 결합되어야 한다는 입장. "
                "강만길 사학의 방법론적·윤리적 원리."
            ),
            "thinker_id": "kang_mangil",
            "work_id": "kang-mangil-bundan-sidae",
            "related_terms": ["역사의 현재성", "통일지향 역사학", "지식인의 역할"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """강만길 관련 관계 데이터 입력."""
    relations = [
        {
            "from_thinker": "baek_nakcheong",
            "to_thinker": "kang_mangil",
            "type": "related",
            "description": (
                "백낙청의 '분단체제론'과 강만길의 '분단시대론'은 "
                "분단을 일회적 사건이 아닌 지속적 역사 조건으로 파악한다는 점에서 "
                "상호 공명하는 담론이다. "
                "백낙청이 문학·사회이론 쪽에서 분단체제론을 정립했다면, "
                "강만길은 역사학 쪽에서 분단시대론과 통일지향 역사학을 정립했다. "
                "양자는 1980~90년대 통일 담론의 양대 지성적 기둥으로 평가된다."
            ),
            "evidence": "강만길, 『분단시대의 역사인식』(1978); 백낙청, 『분단체제 변혁의 공부길』(1994)"
        },
        {
            "from_thinker": "kang_mangil",
            "to_thinker": "baek_nakcheong",
            "type": "related",
            "description": (
                "강만길의 분단시대론은 백낙청의 분단체제론 형성에 역사학적 토대를 제공했다. "
                "백낙청은 강만길의 분단시대 규정을 자주 인용하며, "
                "문학·사회이론의 분단체제론을 역사학의 통일지향 서술과 결합시켰다."
            ),
            "evidence": "백낙청의 분단체제론 논의에서 강만길 분단시대론 인용 맥락"
        },
        {
            "from_thinker": "kang_mangil",
            "to_thinker": "kim_yongseop",
            "type": "related",
            "description": (
                "강만길과 김용섭은 1960~70년대 한국 근대사학계에서 "
                "내재적 발전론을 공동으로 발전시킨 대표 연구자이다. "
                "김용섭이 조선후기 농업사를 중심으로 내재적 발전의 경험적 근거를 구축했다면, "
                "강만길은 상공업사·광업사 연구로 이를 보완했다."
            ),
            "evidence": "강만길·김용섭의 1960~70년대 조선후기사 연구 일군"
        },
        {
            "from_thinker": "shin_chaeho",
            "to_thinker": "kang_mangil",
            "type": "influenced",
            "description": (
                "신채호의 민족주의 사학, 특히 민중 중심의 민족운동 서술은 "
                "강만길의 민중적 민족주의 사관에 간접적 영향을 주었다. "
                "강만길은 신채호의 '낭가사상'이나 영웅 중심 서술을 그대로 수용하지는 않지만, "
                "민족사의 주체 문제를 민중 쪽으로 재설정하는 흐름 속에 자리한다."
            ),
            "evidence": "강만길의 민족운동사 서술에서 민족주의 사학 전통에 대한 평가"
        }
    ]

    for i, rel in enumerate(relations):
        rel_id = f"kang-mangil-rel-{i+1:03d}"
        rel["id"] = rel_id
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(
            f"[relation] {rel_id} ({rel['from_thinker']} → {rel['to_thinker']}): "
            f"{result['result']}"
        )

    return len(relations)


def main():
    client = get_client()
    try:
        print("=== 강만길(姜萬吉) 데이터 입력 시작 ===\n")

        print("--- 분야(field) 확인 ---")
        ensure_field(client)
        print()

        print("--- 사상가(thinker) 입력 ---")
        insert_thinker(client)
        print()

        print("--- 저서(works) 입력 ---")
        n_works = insert_works(client)
        print(f"총 {n_works}개 저서 입력 완료\n")

        print("--- 주장(claims) 입력 ---")
        n_claims = insert_claims(client)
        print(f"총 {n_claims}개 주장 입력 완료\n")

        print("--- 키워드(keywords) 입력 ---")
        n_keywords = insert_keywords(client)
        print(f"총 {n_keywords}개 키워드 입력 완료\n")

        print("--- 관계(relations) 입력 ---")
        n_relations = insert_relations(client)
        print(f"총 {n_relations}개 관계 입력 완료\n")

        print("=== 강만길 데이터 입력 완료 ===")
        print(
            f"요약: 사상가 1명, 저서 {n_works}개, 주장 {n_claims}개, "
            f"키워드 {n_keywords}개, 관계 {n_relations}개"
        )

    finally:
        close_client(client)


if __name__ == "__main__":
    main()
