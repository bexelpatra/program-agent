"""요한 갈퉁(Johan Galtung) 데이터를 ES에 직접 입력하는 스크립트.

평화학(peace studies) 분야의 창시자. 적극적 평화, 구조적/문화적 폭력,
평화의 삼각형, 평화연구방법론(진단-예후-치료) 등 핵심 개념을 포함한다.
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
    """평화학 분야가 ethics-fields 인덱스에 없으면 추가."""
    try:
        client.get(index=INDEX_FIELDS, id="peace_studies")
        print("[field] peace_studies: 이미 존재")
    except Exception:
        doc = {
            "id": "peace_studies",
            "name": "평화학",
            "description": (
                "전쟁의 부재(소극적 평화)를 넘어 구조적·문화적 폭력의 제거(적극적 평화)를 "
                "추구하는 학제적 분야. 갈퉁을 창시자로 하며 분쟁 전환(conflict transformation), "
                "평화교육, 비폭력 연구 등을 포함한다. 통일교육·시민윤리 영역에서 임용시험 빈출."
            ),
            "order": 5
        }
        result = client.index(index=INDEX_FIELDS, id="peace_studies", document=doc)
        print(f"[field] peace_studies: {result['result']}")


def insert_thinker(client):
    """갈퉁 사상가 데이터 입력."""
    doc = {
        "id": "galtung",
        "name": "요한 갈퉁",
        "name_en": "Johan Galtung",
        "field": "peace_studies",
        "era": "현대",
        "birth_year": 1930,
        "death_year": 2024,
        "background": (
            "노르웨이 오슬로 출신 사회학자·수학자로, 현대 평화학(peace studies)의 창시자로 평가된다. "
            "오슬로 대학교에서 수학(1956)과 사회학(1957) 박사학위를 받았다. "
            "1959년 오슬로 국제평화연구소(PRIO, Peace Research Institute Oslo)를 창설하고, "
            "1964년 학술지 Journal of Peace Research를 창간하여 평화연구를 독립된 학문 분과로 정립했다. "
            "간디의 비폭력 사상과 마르크스의 구조 분석, 체계이론을 종합하여 "
            "'소극적 평화(전쟁의 부재)' 대 '적극적 평화(구조적·문화적 폭력의 부재)' 개념을 정식화했다. "
            "평생 150권 이상의 저서와 1,700편 이상의 논문을 남겼으며, "
            "TRANSCEND International을 설립해 세계 각지의 분쟁 조정에 실천적으로 참여했다. "
            "한국 분단 문제에도 관심을 가져 한반도 평화에 관한 제언을 여러 차례 남겼다."
        ),
        "core_philosophy": (
            "갈퉁 평화학의 핵심은 폭력 개념의 확장과 평화의 이중 정의에 있다. "
            "전통적 평화 개념은 '전쟁·직접 폭력의 부재'(소극적 평화, negative peace)에 머물렀으나, "
            "갈퉁은 구조적 폭력(structural violence)과 문화적 폭력(cultural violence) 개념을 도입하여 "
            "'구조적·문화적 폭력까지 제거된 상태'(적극적 평화, positive peace)를 진정한 평화로 규정한다. "
            "폭력을 직접적-구조적-문화적 세 차원으로 분석하는 '폭력의 삼각형(violence triangle)'과 "
            "이에 대응하는 '평화의 삼각형(peace triangle: 직접 평화-구조적 평화-문화적 평화)'을 제시했다. "
            "분쟁 분석에서는 태도(Attitude)-행동(Behavior)-모순(Contradiction)의 ABC 삼각형을 사용하고, "
            "의학 모델에서 차용한 '진단(diagnosis)-예후(prognosis)-치료(therapy)'의 평화연구 방법론을 정립했다. "
            "해결책으로는 TRANSCEND 접근(초월적 중재)과 비폭력(간디 계승)을 제시한다."
        ),
        "philosophical_journey": (
            "초기(1950~60년대): 수학·사회학 훈련 배경에서 평화를 과학적으로 연구하려는 기획. "
            "1959년 PRIO 창설, 1964년 Journal of Peace Research 창간으로 학문 기반을 구축. "
            "중기(1969): 'Violence, Peace, and Peace Research' 논문으로 구조적 폭력 개념 도입. "
            "소극적/적극적 평화의 이분법을 정식화하며 평화연구의 패러다임을 전환. "
            "후기(1990): 'Cultural Violence' 논문으로 세 번째 폭력 범주인 문화적 폭력을 추가하여 "
            "폭력의 삼각형 이론을 완성. 종교·이데올로기·언어·예술이 직접·구조적 폭력을 정당화하는 방식을 분석. "
            "실천기(1990년대~): TRANSCEND International 설립, 전 세계 150여 개 분쟁에 대한 중재 자문. "
            "분쟁 전환(conflict transformation) 방법론을 교육하며 평화학을 실천 학문으로 확장."
        ),
        "keywords": [
            "적극적 평화",
            "소극적 평화",
            "구조적 폭력",
            "문화적 폭력",
            "직접적 폭력",
            "평화의 삼각형",
            "폭력의 삼각형",
            "TRANSCEND",
            "분쟁 전환",
            "ABC 삼각형",
            "진단-예후-치료",
            "평화연구"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="galtung", document=doc)
    print(f"[thinker] galtung: {result['result']}")
    return result


def insert_works(client):
    """갈퉁 저서/주요 논문 데이터 입력."""
    works = [
        {
            "id": "galtung-violence-peace-research",
            "thinker_id": "galtung",
            "title": "폭력, 평화, 그리고 평화연구",
            "title_original": "Violence, Peace, and Peace Research",
            "year": 1969,
            "significance": (
                "Journal of Peace Research에 발표된 갈퉁의 가장 영향력 있는 논문. "
                "구조적 폭력(structural violence) 개념을 도입하여 폭력 연구의 범위를 "
                "직접 폭력에서 사회구조가 야기하는 잠재적 피해로 확장했다. "
                "소극적 평화(전쟁 부재)와 적극적 평화(구조적 폭력 부재)의 구분을 정식화하여 "
                "평화학의 기본 개념틀을 제공했다."
            ),
            "key_concepts": [
                "구조적 폭력", "직접적 폭력", "소극적 평화", "적극적 평화",
                "잠재적 실현가능성", "평화연구"
            ]
        },
        {
            "id": "galtung-cultural-violence",
            "thinker_id": "galtung",
            "title": "문화적 폭력",
            "title_original": "Cultural Violence",
            "year": 1990,
            "significance": (
                "Journal of Peace Research에 발표된 논문으로, 1969년의 폭력 이론을 확장해 "
                "세 번째 폭력 범주인 '문화적 폭력'을 도입했다. "
                "종교, 이데올로기, 언어, 예술, 과학 등이 직접적·구조적 폭력을 "
                "'정상'이거나 '정당'한 것으로 보이게 만드는 기능을 한다고 분석했다. "
                "폭력의 삼각형(직접-구조-문화) 이론을 완성한 저작이다."
            ),
            "key_concepts": ["문화적 폭력", "폭력의 삼각형", "폭력의 정당화", "이데올로기"]
        },
        {
            "id": "galtung-peace-by-peaceful-means",
            "thinker_id": "galtung",
            "title": "평화적 수단에 의한 평화",
            "title_original": "Peace by Peaceful Means: Peace and Conflict, Development and Civilization",
            "year": 1996,
            "significance": (
                "갈퉁 평화학의 집대성. 평화·분쟁·발전·문명 네 축으로 구성되어 "
                "평화이론, 분쟁이론, 발전이론, 문명이론을 체계적으로 제시한다. "
                "TRANSCEND 방법론의 이론적 토대를 제공하며, "
                "평화를 '평화적 수단으로만 달성해야 한다'는 간디적 원칙을 학문적으로 정식화했다."
            ),
            "key_concepts": [
                "TRANSCEND 방법", "분쟁 전환", "ABC 삼각형",
                "진단-예후-치료", "문명 비교"
            ]
        },
        {
            "id": "galtung-transcend-transform",
            "thinker_id": "galtung",
            "title": "분쟁 전환의 수단: TRANSCEND 방법",
            "title_original": "Transcend and Transform: An Introduction to Conflict Work",
            "year": 2004,
            "significance": (
                "실천적 분쟁 조정 매뉴얼로, TRANSCEND 방법을 평화교육·현장실무자 관점에서 설명한다. "
                "분쟁 당사자들의 양립 불가능해 보이는 목표를 '초월(transcend)'하여 "
                "창의적 대안을 도출하는 중재 접근을 제시한다."
            ),
            "key_concepts": ["TRANSCEND", "분쟁 전환", "창의적 중재", "평화교육"]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """갈퉁 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 소극적 평화 vs 적극적 평화
        {
            "id": "galtung-claim-001",
            "thinker_id": "galtung",
            "work_id": "galtung-violence-peace-research",
            "source_detail": "Violence, Peace, and Peace Research (1969), Section 1",
            "claim": (
                "평화는 단순히 전쟁이나 직접적 폭력이 없는 상태(소극적 평화, negative peace)에 머물러서는 안 되며, "
                "구조적 폭력까지 제거된 상태(적극적 평화, positive peace)로 확장되어야 한다. "
                "적극적 평화는 사회 정의의 실현과 같으며, 인간의 잠재력이 구조적 제약 없이 "
                "온전히 발현될 수 있는 상태이다."
            ),
            "original_text": (
                "We shall refer to the absence of personal violence as negative peace, "
                "and to the absence of structural violence as positive peace. "
                "...peace research...should be concerned with both."
            ),
            "explanation": (
                "갈퉁 이전의 평화 개념은 주로 전쟁의 부재, 즉 소극적 평화에 국한되었다. "
                "갈퉁은 전쟁이 없어도 기아·빈곤·차별 등으로 인해 인간의 실현 가능한 잠재력과 "
                "실제 실현된 것 사이에 간격이 있다면 폭력이 존재한다고 본다. "
                "따라서 평화를 '구조적 폭력까지 제거된 상태'(적극적 평화)로 재정의함으로써 "
                "평화연구의 과제를 사회 정의의 실현으로 확장한다."
            ),
            "argument": (
                "(1) 인간 잠재력 실현 관점: 현실적 가능성과 실제 실현 간의 격차가 폭력이므로, "
                "이를 구조적으로 만드는 사회제도 역시 폭력에 해당한다. "
                "(2) 평화연구의 학문적 독립성: 평화를 '전쟁 없음'으로만 규정하면 "
                "국제정치학의 하위 분과로 축소된다. 적극적 평화 개념은 평화학을 "
                "사회 정의·발전이론과 연결하는 독자적 학제로 만든다. "
                "(3) 도덕적 요구: 전쟁 없음이 곧 평화라면 불평등한 억압 체제도 '평화'로 불릴 수 있는데, "
                "이는 도덕적으로 받아들이기 어렵다."
            ),
            "counterpoint": (
                "현실주의 국제정치학(케네스 월츠 등)은 '전쟁 부재'를 구체적 성과로 보는 반면 "
                "구조적 폭력 개념은 너무 광범위해 모든 사회 문제를 '폭력'으로 포괄한다고 비판한다. "
                "보울딩(Kenneth Boulding)은 갈퉁의 구조적 폭력 개념이 '폭력'이라는 말의 분석력을 "
                "희석시킨다고 지적했다."
            ),
            "context": (
                "1969년 논문 'Violence, Peace, and Peace Research'에서 처음 정식화. "
                "1960년대 베트남전쟁·탈식민화·남북 격차 문제의 인식 속에서, "
                "'전쟁 부재만으로는 평화가 아니다'라는 제3세계 지식인들의 문제의식과 공명했다."
            ),
            "keywords": ["소극적 평화", "적극적 평화", "구조적 폭력", "사회 정의", "평화의 정의"],
            "verified": False
        },
        # CLAIM-002: 구조적 폭력
        {
            "id": "galtung-claim-002",
            "thinker_id": "galtung",
            "work_id": "galtung-violence-peace-research",
            "source_detail": "Violence, Peace, and Peace Research (1969), Section 3",
            "claim": (
                "구조적 폭력(structural violence)은 특정한 가해자 없이 사회구조 자체에 의해 "
                "인간의 기본 욕구 실현이 저지되는 상태이다. "
                "빈곤, 기아, 차별, 착취, 교육 기회 박탈 등이 대표적 예이며, "
                "직접적 폭력보다 훨씬 광범위한 피해를 초래하지만 가시성이 낮아 정당화되기 쉽다."
            ),
            "original_text": (
                "Violence is present when human beings are being influenced so that their actual "
                "somatic and mental realizations are below their potential realizations. "
                "...violence without this subject-action-object relation...we shall refer to as "
                "structural violence."
            ),
            "explanation": (
                "갈퉁은 폭력을 '잠재적 실현가능성(potential)과 실제 실현(actual) 사이의 격차'로 정의한다. "
                "직접적 폭력은 '주체-행위-대상'이 명시적인 반면, "
                "구조적 폭력은 가해 주체가 특정되지 않고 사회제도·국제질서에 내장되어 있다. "
                "예: 의료 기술이 발달해 치료 가능한 질병으로 사람이 죽는다면 이는 구조적 폭력이다. "
                "평균수명 격차, 문맹률, 영아사망률 등이 구조적 폭력의 지표로 사용될 수 있다."
            ),
            "argument": (
                "(1) 잠재-실제 격차 정의: 실현 가능함에도 실현되지 않으면 어떤 힘이 저지한 것이며, "
                "그 힘이 인적 가해자 없이 작동하면 구조에 내재된 폭력이다. "
                "(2) 피해 규모 비교: 20세기 전쟁 사망자보다 빈곤·영양실조로 인한 사망자가 훨씬 많다. "
                "(3) 국제 불평등: 남북 간 경제격차·자원배분 불균형은 제국주의·종속구조라는 "
                "국제적 구조적 폭력의 결과이다."
            ),
            "counterpoint": (
                "개념의 과잉확장 비판: '폭력'이라는 용어를 구조·제도까지 확대하면 "
                "특수한 의도적 가해 행위의 도덕적 무게가 희석된다(코디 등 분석철학자의 비판). "
                "인과 귀속의 어려움: 구조적 폭력의 '가해자'가 불특정하면 책임 주체를 "
                "지목해 개선할 실천 지점이 불분명해진다."
            ),
            "context": (
                "1960년대 남북 격차 문제, 신식민주의 논쟁, 라틴아메리카 종속이론의 맥락에서 "
                "갈퉁은 구조적 폭력 개념으로 국제불평등을 평화연구의 핵심 의제로 끌어들였다."
            ),
            "keywords": ["구조적 폭력", "잠재-실제 격차", "불평등", "빈곤", "제도적 폭력"],
            "verified": False
        },
        # CLAIM-003: 문화적 폭력
        {
            "id": "galtung-claim-003",
            "thinker_id": "galtung",
            "work_id": "galtung-cultural-violence",
            "source_detail": "Cultural Violence (1990), Introduction & Section 1",
            "claim": (
                "문화적 폭력(cultural violence)은 종교, 이데올로기, 언어, 예술, 과학 등 "
                "문화의 상징 영역에서 작동하며, 직접적 폭력과 구조적 폭력을 "
                "'정당한 것' 또는 '자연스러운 것'으로 보이게 만드는 기능을 한다. "
                "예: 우월 민족 이데올로기, 정당전쟁론, 가부장적 종교 해석, "
                "'필요악'이라는 언어 사용 등이 이에 해당한다."
            ),
            "original_text": (
                "By 'cultural violence' we mean those aspects of culture, the symbolic sphere of our existence "
                "—exemplified by religion and ideology, language and art, empirical science and formal science "
                "(logic, mathematics)— that can be used to justify or legitimize direct or structural violence."
            ),
            "explanation": (
                "문화적 폭력은 직접 피해를 입히지는 않지만, 다른 형태의 폭력을 정당화하여 "
                "가해자의 양심을 마비시키고 피해자의 저항 의지를 꺾는다. "
                "갈퉁은 문화적 폭력이 직접·구조적 폭력을 '붉은색(잘못)'에서 "
                "'노란색(용인 가능)' 또는 '녹색(정당)'으로 탈바꿈시킨다고 표현한다. "
                "여섯 개 문화 영역(종교, 법과 이데올로기, 언어, 예술, 경험과학, 형식과학)이 분석 대상이 된다."
            ),
            "argument": (
                "(1) 폭력 정당화 기제: 종교적 '선택된 민족' 관념, 애국주의 서사, "
                "인종·성별 우열 이론은 모두 폭력을 도덕적으로 수용 가능하게 만든다. "
                "(2) 내면화 효과: 문화적 폭력은 사회화 과정에서 내면화되어 "
                "피해자조차 현재 질서를 당연한 것으로 여기게 만든다(헤게모니). "
                "(3) 지속성: 직접·구조적 폭력을 뒷받침하는 상징체계가 존속하는 한, "
                "제도 개혁만으로는 평화가 달성되지 않는다."
            ),
            "counterpoint": (
                "문화 환원주의 비판: 모든 문화 현상을 폭력 정당화 기능으로 환원하면 "
                "문화의 자율적 영역과 해방적 가능성이 간과된다. "
                "상대주의 문제: '어떤 문화는 폭력적'이라는 판단 자체가 "
                "또 다른 문화적 우월주의로 이어질 수 있다."
            ),
            "context": (
                "1990년 논문 'Cultural Violence'에서 처음 체계화. "
                "1969년의 직접·구조 폭력 이론을 20년에 걸쳐 보완하여 "
                "폭력의 삼각형(직접-구조-문화)을 완성했다."
            ),
            "keywords": ["문화적 폭력", "폭력 정당화", "이데올로기", "헤게모니", "상징 폭력"],
            "verified": False
        },
        # CLAIM-004: 폭력의 삼각형 / 평화의 삼각형
        {
            "id": "galtung-claim-004",
            "thinker_id": "galtung",
            "work_id": "galtung-cultural-violence",
            "source_detail": "Cultural Violence (1990) & Peace by Peaceful Means (1996), Part I",
            "claim": (
                "폭력은 직접적 폭력(direct)-구조적 폭력(structural)-문화적 폭력(cultural)의 "
                "세 꼭짓점으로 이루어진 삼각형을 이룬다. 이에 상응하는 평화 역시 "
                "직접 평화-구조적 평화-문화적 평화의 삼각형으로 구성된다. "
                "세 차원이 상호 강화하며, 한 꼭짓점만의 개혁으로는 진정한 평화가 달성되지 않는다."
            ),
            "explanation": (
                "폭력의 삼각형: ① 직접적 폭력은 가시적·사건적(전쟁·살인·폭행). "
                "② 구조적 폭력은 제도·시스템에 내장(빈곤·차별·억압). "
                "③ 문화적 폭력은 상징·규범에서 앞의 두 가지를 정당화. "
                "평화의 삼각형: ① 직접 평화(비폭력 문화, 휴전, 군축), "
                "② 구조적 평화(정의로운 제도, 평등한 경제구조, 민주적 참여), "
                "③ 문화적 평화(평화교육, 평화문화, 상호 이해의 내러티브). "
                "세 영역은 순환 고리를 이루며 한 영역의 변화가 다른 영역에 영향을 미친다."
            ),
            "argument": (
                "(1) 상호 강화 관계: 문화적 폭력이 구조적 폭력을 정당화하고, "
                "구조적 폭력이 직접적 폭력(반란·폭동 포함)을 유발한다. "
                "역방향으로 직접 폭력의 반복은 구조를 경직시키고 문화 속 폭력 서사를 강화한다. "
                "(2) 통합적 접근의 필요성: 평화협정(직접 평화)만으로는 구조적 불평등이 유지되고, "
                "재발 위험이 크다. 진정한 평화는 세 차원 동시 접근을 요구한다. "
                "(3) 임상적 유비: 증상 치료(직접)-병인 제거(구조)-생활습관 개선(문화)의 "
                "세 차원을 함께 다뤄야 건강이 회복되는 것과 같다."
            ),
            "counterpoint": (
                "삼분류의 인위성: 실제 폭력은 세 차원이 뒤엉켜 있어 엄격한 구분이 어렵다. "
                "실천 우선순위 문제: 세 영역 모두를 동시에 다루는 것은 현실에서 자원 배분 "
                "문제를 낳으며, 급박한 직접 폭력 상황에서 문화 개혁을 논하는 것은 "
                "비현실적이라는 비판이 있다."
            ),
            "context": (
                "1990년 Cultural Violence 논문에서 폭력 삼각형이 완성되고, "
                "1996년 'Peace by Peaceful Means'에서 평화 삼각형으로 확장되어 "
                "갈퉁 평화이론의 기본 틀로 정착했다."
            ),
            "keywords": ["폭력의 삼각형", "평화의 삼각형", "직접 평화", "구조적 평화", "문화적 평화"],
            "verified": False
        },
        # CLAIM-005: ABC 삼각형 — 분쟁 분석
        {
            "id": "galtung-claim-005",
            "thinker_id": "galtung",
            "work_id": "galtung-peace-by-peaceful-means",
            "source_detail": "Peace by Peaceful Means (1996), Part II: Conflict Theory",
            "claim": (
                "모든 분쟁(conflict)은 태도(Attitude)-행동(Behavior)-모순(Contradiction)의 "
                "ABC 삼각형으로 분석할 수 있다. A(태도)는 당사자의 적대적 감정·인식, "
                "B(행동)는 표출된 공격·폭력, C(모순)는 양립 불가능해 보이는 목표의 충돌이다. "
                "C가 분쟁의 뿌리이며 A·B는 드러난 증상이다."
            ),
            "explanation": (
                "A(Attitude): 증오·편견·불신 등 내적·심리적 차원. 비가시적. "
                "B(Behavior): 협박·폭력·보이콧 등 외적·행동 차원. 가시적. "
                "C(Contradiction): 당사자들이 추구하는 목표 간의 양립불가능 구조. 근본 원인. "
                "평화적 분쟁 전환은 B(행동)의 즉각적 완화뿐 아니라 "
                "A(태도)의 변화와 C(구조적 모순)의 재구성을 함께 요구한다. "
                "특히 C를 방치한 채 B만 억누르면 분쟁은 잠복할 뿐이다."
            ),
            "argument": (
                "(1) 체계적 분석 도구: ABC 삼각형은 분쟁을 다층적으로 진단하여 "
                "단순 행동 수준의 개입을 넘어 근본 원인에 접근하게 한다. "
                "(2) TRANSCEND 방법의 기초: C(모순)를 초월하는 창의적 대안 도출이 "
                "갈퉁 중재법의 핵심이며, 이는 ABC 모델 위에서만 가능하다. "
                "(3) 임상 적용성: PRIO·TRANSCEND International의 수많은 실제 분쟁 조정 사례에서 "
                "ABC 프레임이 유효한 진단 도구로 사용되었다."
            ),
            "counterpoint": (
                "단순화 비판: 실제 분쟁에는 다수의 행위자·이슈·역사적 맥락이 중첩되어 "
                "ABC 삼각형으로 환원하기 어렵다. 권력 비대칭을 명시적으로 다루지 않는다는 "
                "비판(페미니스트 평화학·비판 평화학)도 있다."
            ),
            "context": (
                "갈퉁이 분쟁을 체계이론적으로 모형화하는 과정에서 발전. "
                "간디의 사티아그라하(진리 고수) 전통과 사회심리학의 태도-행동 모형을 "
                "종합한 틀로, 1990년대 이후 평화학 교과서의 표준 분석도구가 되었다."
            ),
            "keywords": ["ABC 삼각형", "분쟁 분석", "태도", "행동", "모순", "분쟁 전환"],
            "verified": False
        },
        # CLAIM-006: 진단-예후-치료 방법론
        {
            "id": "galtung-claim-006",
            "thinker_id": "galtung",
            "work_id": "galtung-peace-by-peaceful-means",
            "source_detail": "Peace by Peaceful Means (1996), Methodology chapter",
            "claim": (
                "평화연구는 의학을 모델로 '진단(diagnosis)-예후(prognosis)-치료(therapy)'의 "
                "3단계 방법론을 따라야 한다. 분쟁의 증상·원인을 진단하고, "
                "개입 없이 전개될 경로를 예후로 예측한 뒤, 평화적 수단에 의한 치료를 설계한다. "
                "사실 기술에 그치지 않고 규범적 처방까지 포함하는 실천적 학문이 되어야 한다."
            ),
            "explanation": (
                "진단(Diagnosis): 분쟁의 ABC 요소, 폭력 삼각형 상의 위치, 역사적 배경 기술. "
                "예후(Prognosis): 개입하지 않을 경우 사태가 어떻게 전개될지 예측 — "
                "에스컬레이션·새 균형·외부 개입 등 시나리오 분석. "
                "치료(Therapy): TRANSCEND 방법을 포함한 평화적 개입 처방. "
                "이 방법론은 평화학을 단순 기술과학(descriptive)이 아닌 "
                "규범적·실천적 학문(prescriptive)으로 정초하려는 시도이다."
            ),
            "argument": (
                "(1) 실천지향성: 평화연구는 분쟁 피해자에게 실제적 도움이 되어야 하므로 "
                "기술을 넘어 처방이 필요하다. "
                "(2) 간학제적 정합성: 의학·공학 등 처방적 학문 모델은 이론-실천 연계를 "
                "제도화하는 데 성공했다. 평화학도 같은 구조를 채택할 수 있다. "
                "(3) 비교평가 가능성: 진단-예후-치료의 명시적 절차는 개입 효과를 "
                "사후 평가하고 학습을 축적할 수 있게 한다."
            ),
            "counterpoint": (
                "의학 유비의 한계: 사회 현상은 생체처럼 통제된 '치료' 대상이 아니며, "
                "'의사로서의 평화연구자' 모델은 전문가주의·개입주의 위험이 있다는 비판. "
                "규범적 편향 우려: 처방을 내리는 순간 연구자의 가치가 개입되므로 "
                "객관성 문제가 제기될 수 있다."
            ),
            "context": (
                "갈퉁이 PRIO와 오슬로대에서 평화학을 제도화하는 과정에서 "
                "학문적 정체성 문제에 답하기 위해 제시한 방법론. "
                "1996년 'Peace by Peaceful Means'에서 명시적으로 체계화되었다."
            ),
            "keywords": ["평화연구 방법론", "진단-예후-치료", "처방적 학문", "실천적 평화학"],
            "verified": False
        },
        # CLAIM-007: TRANSCEND 방법
        {
            "id": "galtung-claim-007",
            "thinker_id": "galtung",
            "work_id": "galtung-transcend-transform",
            "source_detail": "Transcend and Transform (2004), Chapters 1-3",
            "claim": (
                "분쟁 당사자들의 양립 불가능해 보이는 목표는 '초월(transcend)'을 통해 "
                "새로운 차원에서 공존 가능한 창의적 대안으로 재구성될 수 있다. "
                "TRANSCEND 방법은 어느 쪽도 포기하지 않으면서 양쪽 목표를 함께 충족할 수 있는 "
                "제3의 해결책을 공동 창출하는 중재 접근이다. "
                "승자-패자 게임을 공동 창조(co-creation) 게임으로 전환한다."
            ),
            "explanation": (
                "일반적 분쟁 해결은 네 가지 결과 중 하나로 귀결된다: "
                "① A 승리, ② B 승리, ③ 타협(양자 일부 양보), ④ 교착(연기). "
                "TRANSCEND는 다섯 번째 길, 즉 '양립 불가능한 목표를 초월하여 "
                "원래 목표를 더 높은 차원에서 재정의'하는 접근을 추구한다. "
                "예: 영토 분쟁에서 '주권 공유+공동 개발구' 같은 새로운 제도적 상상. "
                "중재자는 당사자와 별도 대화를 통해 각자의 '정당한 목표(legitimate goals)'를 식별하고, "
                "이를 모두 실현할 수 있는 시나리오를 제안하여 당사자의 창의성을 자극한다."
            ),
            "argument": (
                "(1) 제로섬 탈피: 분쟁을 제로섬으로 전제하는 한 지속가능한 해결은 없다. "
                "초월은 파이 자체를 키워 모두의 정당한 요구를 수용할 공간을 만든다. "
                "(2) 공동 창조의 힘: 당사자들이 제3자의 타협안을 받아들이는 것보다 "
                "스스로 공동 창출한 해결책을 훨씬 강하게 지지·이행한다. "
                "(3) 실증: 에콰도르-페루 국경분쟁, 한반도, 스리랑카 등 "
                "갈퉁이 관여한 여러 사례에서 창의적 대안 도출의 단서가 확인된다."
            ),
            "counterpoint": (
                "권력 비대칭 앞에서의 한계: 당사자 간 힘의 격차가 극심할 때 "
                "'상호 창의적 합의'는 약자의 양보를 포장하는 수사로 변질될 수 있다. "
                "문화적 전제: TRANSCEND는 합리적 대화가 가능한 당사자를 전제하지만, "
                "극단적 이데올로기 집단에는 적용 어려울 수 있다."
            ),
            "context": (
                "1990년대 TRANSCEND International을 통한 현장 중재 경험을 이론화. "
                "간디의 사티아그라하(진리가 승리하되 상대를 적으로 삼지 않음) 전통과 "
                "수학적 게임이론의 확장판으로 볼 수 있다."
            ),
            "keywords": ["TRANSCEND", "분쟁 전환", "초월", "공동 창조", "창의적 중재"],
            "verified": False
        },
        # CLAIM-008: 평화교육 — 평화적 수단에 의한 평화
        {
            "id": "galtung-claim-008",
            "thinker_id": "galtung",
            "work_id": "galtung-peace-by-peaceful-means",
            "source_detail": "Peace by Peaceful Means (1996), Part IV & Transcend and Transform (2004)",
            "claim": (
                "평화는 반드시 '평화적 수단'으로만 달성되어야 한다. "
                "폭력적 수단으로 달성된 평화는 새로운 폭력의 씨앗이 되며, "
                "목표와 수단의 일치가 평화학의 근본 원칙이다. "
                "평화교육은 학생이 직접·구조·문화적 폭력을 식별하고 "
                "비폭력적 분쟁 전환 역량을 갖추도록 훈련시키는 과정이다."
            ),
            "explanation": (
                "'평화적 수단에 의한 평화(Peace by Peaceful Means)'는 "
                "간디의 '수단과 목적의 동일성' 원칙을 평화학에 편입한 것이다. "
                "폭력을 통한 평화 달성은 자기모순이며, 단기적 안정이 장기적 폭력의 원인이 된다. "
                "평화교육의 내용: ① 폭력의 삼각형 인식 훈련, "
                "② ABC 분석·TRANSCEND 기법 실습, "
                "③ 비폭력 의사소통·공감 역량, "
                "④ 세계시민의식·문화 간 이해. "
                "대한민국 임용시험에서도 평화교육의 원칙·방법으로 빈번히 출제된다."
            ),
            "argument": (
                "(1) 수단-목적 일치: 억압으로 달성된 '질서'는 피억압자의 원한을 축적해 "
                "다음 분쟁의 에너지가 된다(역사적 관찰). "
                "(2) 교육의 재생산 기능: 문화적 평화는 교육을 통해서만 세대 간 전승되므로, "
                "평화문화 구축은 평화교육 없이 불가능하다. "
                "(3) 간디 실증: 비폭력 저항(사티아그라하)이 "
                "인도 독립 등 대규모 정치 변혁을 이뤄낸 역사적 사례."
            ),
            "counterpoint": (
                "긴급 상황 대응 한계: 즉각적 대량학살·침략 앞에서 '평화적 수단만' 고집은 "
                "피해자 보호 의무와 충돌할 수 있다(인도적 개입 논쟁). "
                "현실주의 비판: 국제정치에서 '평화적 수단'이 언제나 가능하지는 않으며, "
                "최소한의 억제력(deterrence)이 필요하다는 반론이 있다."
            ),
            "context": (
                "1996년 저서의 제목 자체가 핵심 원칙이다. "
                "유네스코의 평화문화(Culture of Peace) 개념과 궤를 같이하며, "
                "21세기 평화교육 커리큘럼의 이론적 기반이 되었다. "
                "한국 도덕과·사회과 교육과정의 통일·평화교육 단원에도 반영되어 있다."
            ),
            "keywords": ["평화교육", "평화적 수단", "수단-목적 일치", "비폭력", "평화문화"],
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """갈퉁 핵심 키워드 데이터 입력."""
    keywords = [
        {
            "id": "kw-positive-peace",
            "term": "적극적 평화",
            "term_en": "Positive Peace",
            "definition": (
                "갈퉁이 도입한 개념으로, 전쟁이나 직접적 폭력의 부재를 넘어 "
                "구조적 폭력과 문화적 폭력까지 제거된 상태를 의미한다. "
                "사회 정의의 실현, 인간 잠재력의 온전한 발현이 가능한 조건이다. "
                "소극적 평화(negative peace)와 대비된다."
            ),
            "thinker_id": "galtung",
            "work_id": "galtung-violence-peace-research",
            "related_terms": ["소극적 평화", "구조적 폭력", "문화적 폭력", "사회 정의", "평화의 삼각형"]
        },
        {
            "id": "kw-negative-peace",
            "term": "소극적 평화",
            "term_en": "Negative Peace",
            "definition": (
                "전쟁·무력 충돌·직접적 폭력이 없는 상태. "
                "전통적 평화 개념에 해당하며, 갈퉁은 이것만으로는 진정한 평화라 할 수 없다고 본다. "
                "구조적·문화적 폭력이 존속하는 '조용한 억압'의 상태일 수 있기 때문이다."
            ),
            "thinker_id": "galtung",
            "work_id": "galtung-violence-peace-research",
            "related_terms": ["적극적 평화", "직접적 폭력", "휴전", "평화협정"]
        },
        {
            "id": "kw-structural-violence",
            "term": "구조적 폭력",
            "term_en": "Structural Violence",
            "definition": (
                "특정 가해자 없이 사회구조·제도·국제질서에 내장되어 "
                "인간의 기본 욕구 실현을 체계적으로 저지하는 폭력. "
                "빈곤·차별·착취·교육 기회 박탈·의료 접근 불평등 등이 대표 사례다. "
                "잠재적 실현가능성과 실제 실현 사이의 격차로 측정할 수 있다."
            ),
            "thinker_id": "galtung",
            "work_id": "galtung-violence-peace-research",
            "related_terms": ["직접적 폭력", "문화적 폭력", "불평등", "제도적 폭력", "적극적 평화"]
        },
        {
            "id": "kw-cultural-violence",
            "term": "문화적 폭력",
            "term_en": "Cultural Violence",
            "definition": (
                "종교·이데올로기·언어·예술·과학 등 문화의 상징 영역에서 작동하며, "
                "직접적·구조적 폭력을 정당화하거나 정상화하는 기능을 수행하는 폭력. "
                "예: 선민사상, 정당전쟁론, 우월 민족 이데올로기, 차별적 언어 사용. "
                "갈퉁이 1990년 논문에서 도입하여 폭력의 삼각형을 완성했다."
            ),
            "thinker_id": "galtung",
            "work_id": "galtung-cultural-violence",
            "related_terms": ["폭력의 삼각형", "이데올로기", "헤게모니", "상징 폭력", "평화문화"]
        },
        {
            "id": "kw-violence-triangle",
            "term": "폭력의 삼각형",
            "term_en": "Violence Triangle",
            "definition": (
                "갈퉁이 제안한 폭력 분석 모형으로, 직접적 폭력(Direct)-구조적 폭력(Structural)-"
                "문화적 폭력(Cultural)의 세 꼭짓점으로 구성된다. "
                "세 폭력은 상호 강화하며 한 영역만의 개혁으로는 근절되지 않는다. "
                "이에 대응하는 '평화의 삼각형(직접·구조·문화)'이 평화 구축의 틀이 된다."
            ),
            "thinker_id": "galtung",
            "work_id": "galtung-cultural-violence",
            "related_terms": ["직접적 폭력", "구조적 폭력", "문화적 폭력", "평화의 삼각형"]
        },
        {
            "id": "kw-peace-triangle",
            "term": "평화의 삼각형",
            "term_en": "Peace Triangle",
            "definition": (
                "폭력의 삼각형에 대응되는 개념. "
                "직접 평화(비폭력·휴전·군축), 구조적 평화(정의로운 제도·평등한 경제구조), "
                "문화적 평화(평화교육·평화문화·상호 이해 내러티브)의 세 차원으로 구성된다. "
                "세 영역의 통합적 접근이 적극적 평화 달성의 조건이다."
            ),
            "thinker_id": "galtung",
            "work_id": "galtung-peace-by-peaceful-means",
            "related_terms": ["적극적 평화", "폭력의 삼각형", "평화교육", "평화문화"]
        },
        {
            "id": "kw-abc-triangle",
            "term": "ABC 삼각형",
            "term_en": "ABC Conflict Triangle",
            "definition": (
                "갈퉁의 분쟁 분석 모형으로 태도(Attitude)-행동(Behavior)-모순(Contradiction)의 "
                "세 요소로 분쟁을 진단한다. A는 내적 감정·인식, B는 표출된 공격·폭력, "
                "C는 당사자 목표의 양립불가능 구조이다. C가 분쟁의 뿌리이다."
            ),
            "thinker_id": "galtung",
            "work_id": "galtung-peace-by-peaceful-means",
            "related_terms": ["분쟁 전환", "TRANSCEND", "태도", "행동", "모순"]
        },
        {
            "id": "kw-transcend-method",
            "term": "TRANSCEND",
            "term_en": "TRANSCEND Method",
            "definition": (
                "갈퉁이 창안한 분쟁 전환 방법론. 당사자들의 양립 불가능해 보이는 목표를 "
                "'초월'하여 양측의 정당한 요구를 모두 충족할 수 있는 "
                "창의적 제3의 대안을 공동 창출하는 접근이다. "
                "승패·타협·교착을 넘어선 '다섯 번째 길'을 추구한다."
            ),
            "thinker_id": "galtung",
            "work_id": "galtung-transcend-transform",
            "related_terms": ["분쟁 전환", "ABC 삼각형", "공동 창조", "중재", "비폭력"]
        },
        {
            "id": "kw-peace-research-methodology",
            "term": "진단-예후-치료",
            "term_en": "Diagnosis-Prognosis-Therapy",
            "definition": (
                "갈퉁이 의학에서 차용한 평화연구 방법론의 3단계. "
                "분쟁의 현 상태 진단, 개입 없을 때의 전개 예측, "
                "평화적 수단에 의한 처방적 치료로 구성된다. "
                "평화학을 기술적 학문을 넘어 처방적·실천적 학문으로 정초하려는 시도이다."
            ),
            "thinker_id": "galtung",
            "work_id": "galtung-peace-by-peaceful-means",
            "related_terms": ["평화연구 방법론", "TRANSCEND", "처방적 학문"]
        },
        {
            "id": "kw-peace-by-peaceful-means",
            "term": "평화적 수단에 의한 평화",
            "term_en": "Peace by Peaceful Means",
            "definition": (
                "목표(평화)와 수단(방법)은 일치해야 한다는 갈퉁 평화학의 근본 원칙. "
                "폭력적 수단으로 달성된 평화는 새로운 폭력의 원인이 된다. "
                "간디의 수단-목적 동일성 사상을 계승하며, "
                "평화교육·비폭력 실천의 핵심 슬로건이다."
            ),
            "thinker_id": "galtung",
            "work_id": "galtung-peace-by-peaceful-means",
            "related_terms": ["비폭력", "간디", "평화교육", "사티아그라하", "수단-목적 일치"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """갈퉁과 관련 사상가 간 관계 데이터 입력."""
    relations = [
        {
            "from_thinker": "kant",
            "to_thinker": "galtung",
            "type": "influenced",
            "description": (
                "칸트의 '영구평화론(Zum ewigen Frieden, 1795)'이 갈퉁 평화학의 선구적 이론으로 작용했다. "
                "칸트가 제시한 공화제·국제연방·세계시민법의 평화 조건은 "
                "갈퉁의 '구조적 평화(정의로운 제도 + 민주적 참여 + 세계시민의식)' 개념에 이론적 유산을 제공했다. "
                "특히 '항구적 평화는 제도적 구조의 재편을 요구한다'는 칸트 명제가 "
                "갈퉁의 구조적 폭력/구조적 평화 구분의 철학적 토대가 된다."
            ),
            "evidence": "영구평화론(1795) → Peace by Peaceful Means(1996) 구조적 평화 논의"
        },
        {
            "from_thinker": "habermas",
            "to_thinker": "galtung",
            "type": "influenced",
            "description": (
                "하버마스의 의사소통 행위이론과 담론윤리가 갈퉁의 TRANSCEND 중재법에 영향을 주었다. "
                "강제 없는 대화를 통한 상호이해 가능성 주장은, "
                "갈퉁이 당사자 간 공동 창조적 대안 탐색을 설계하는 이론적 기반이 되었다. "
                "문화적 폭력 분석에서도 하버마스의 '체계에 의한 생활세계의 식민화' 개념이 "
                "상징 영역에서의 정당화 기제 분석에 연결된다."
            ),
            "evidence": "Peace by Peaceful Means(1996) 의사소통·담론 관련 서술"
        },
        {
            "from_thinker": "galtung",
            "to_thinker": "rawls",
            "type": "criticized",
            "description": (
                "갈퉁은 롤스의 정의론이 국가 내부 분배 정의에 국한되어 "
                "국제적 구조적 폭력(남북 격차·제국주의적 경제구조)을 충분히 다루지 못한다고 비판적으로 보았다. "
                "갈퉁의 구조적 폭력 개념은 롤스적 정의론의 범위를 국제질서로 확장해야 한다는 "
                "문제의식을 제기하며, 적극적 평화=세계 정의라는 더 넓은 정의관을 요구한다."
            ),
            "evidence": "Peace by Peaceful Means(1996) 제3부 발전·세계체제 분석"
        }
    ]

    for rel in relations:
        rel_id = f"{rel['from_thinker']}-{rel['type']}-{rel['to_thinker']}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id}: {result['result']}")

    return len(relations)


def main():
    """메인 실행 함수."""
    print("=== 요한 갈퉁(Johan Galtung) 데이터 ES 입력 시작 ===\n")

    client = get_client()

    try:
        print("[1/6] 분야 확인 및 생성...")
        ensure_field(client)
        print()

        print("[2/6] 사상가 데이터 입력...")
        insert_thinker(client)
        print()

        print("[3/6] 저서 데이터 입력...")
        works_count = insert_works(client)
        print(f"     -> {works_count}개 저서 입력 완료\n")

        print("[4/6] 주장 데이터 입력...")
        claims_count = insert_claims(client)
        print(f"     -> {claims_count}개 주장 입력 완료\n")

        print("[5/6] 키워드 데이터 입력...")
        kw_count = insert_keywords(client)
        print(f"     -> {kw_count}개 키워드 입력 완료\n")

        print("[6/6] 관계 데이터 입력...")
        rel_count = insert_relations(client)
        print(f"     -> {rel_count}개 관계 입력 완료\n")

        print("=== 입력 완료 요약 ===")
        print(f"  - 사상가: 1명 (galtung)")
        print(f"  - 저서: {works_count}개")
        print(f"  - 주장: {claims_count}개")
        print(f"  - 키워드: {kw_count}개")
        print(f"  - 관계: {rel_count}개")
        print("\n요한 갈퉁 데이터 ES 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
