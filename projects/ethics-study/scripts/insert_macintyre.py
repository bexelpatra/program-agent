"""앨러스데어 매킨타이어(Alasdair MacIntyre) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS, INDEX_FIELDS
)


def ensure_field(client):
    """western_ethics 분야가 ethics-fields 인덱스에 없으면 추가."""
    try:
        client.get(index=INDEX_FIELDS, id="western_ethics")
        print("[field] western_ethics: 이미 존재")
    except Exception:
        doc = {
            "id": "western_ethics",
            "name": "서양윤리",
            "description": (
                "고대 그리스 철학에서 현대 분석윤리학까지 서양의 윤리 사상을 다루는 분야. "
                "덕 윤리, 의무론, 공리주의, 자연법 윤리 등을 포함한다."
            ),
            "order": 1
        }
        result = client.index(index=INDEX_FIELDS, id="western_ethics", document=doc)
        print(f"[field] western_ethics: {result['result']}")


def insert_thinker(client):
    """매킨타이어 사상가 데이터 입력."""
    doc = {
        "id": "macintyre",
        "name": "앨러스데어 매킨타이어",
        "name_en": "Alasdair MacIntyre",
        "field": "western_ethics",
        "era": "현대 공동체주의",
        "birth_year": 1929,
        "death_year": None,
        "background": (
            "스코틀랜드 글래스고에서 태어난 영국계 미국 철학자. "
            "맨체스터 대학교, 옥스퍼드 대학교에서 수학한 뒤 미국으로 건너가 "
            "브랜다이스, 보스턴, 밴더빌트 대학교 등에서 가르쳤으며, "
            "현재 노트르담 대학교 명예교수로 재직 중이다. "
            "초기에는 마르크스주의와 기독교 신앙 사이에서 지적 여정을 걷다가, "
            "1981년 '덕의 상실(After Virtue)'을 출간하며 현대 도덕철학에 대한 근본적 비판을 제기했다. "
            "이 저작으로 그는 공동체주의 사상의 선두 주자로 자리매김했다. "
            "아리스토텔레스적 덕 윤리와 가톨릭 자연법 전통을 결합한 독특한 입장을 견지하며, "
            "자유주의 도덕철학과 근대 계몽주의 기획 전체에 대한 비판을 심화시켜 왔다."
        ),
        "core_philosophy": (
            "매킨타이어의 핵심 사상은 현대 도덕 담론의 혼란이 계몽주의의 실패, "
            "특히 덕 윤리의 전통에서 분리된 탈맥락적 도덕 언어에서 비롯된다는 진단이다. "
            "그는 아리스토텔레스의 목적론적 윤리와 덕의 전통 속에서 도덕철학의 갱신 가능성을 찾는다. "
            "인간은 이야기(narrative)를 통해 정체성과 도덕적 방향을 형성하며(서사적 자아), "
            "덕은 실천(practice) 내의 내적 선(internal goods)을 추구함으로써 발전된다. "
            "합리성은 전통 의존적(tradition-dependent)이며, 자유주의의 중립적 합리성 주장은 "
            "사실상 또 다른 전통에 불과하다. 도덕적 덕의 실현에는 공동체가 필수적이다."
        ),
        "philosophical_journey": (
            "초기(1950년대~1960년대): 마르크스주의와 기독교 사이에서 지적 갈등을 겪으며 "
            "영국 분석철학의 언어 분석 방법을 비판적으로 검토했다. "
            "중기(1970년대~1981): 사회과학의 설명 모델과 도덕 언어의 본성을 탐구했다. "
            "1981년 '덕의 상실'로 현대 도덕철학 전체에 대한 체계적 비판을 전개했다. "
            "후기(1988~현재): '누구의 정의? 어떤 합리성?'(1988)에서 합리성의 전통 의존성을, "
            "'도덕 탐구의 세 가지 경쟁 버전'(1990)에서 백과사전적·계보학적·전통적 도덕 탐구를 비교했다. "
            "'의존적 합리적 동물'(1999)에서 덕 윤리의 생물학적·사회적 기반을 심화시켰다. "
            "가톨릭 토마스주의 전통으로 귀의하여 아리스토텔레스-아퀴나스적 덕 전통을 옹호했다."
        ),
        "keywords": [
            "정서주의",
            "서사적 자아",
            "실천(practice)",
            "내적 선",
            "외적 선",
            "전통 의존적 합리성",
            "계몽주의 기획",
            "덕의 상실",
            "공동체주의",
            "아리스토텔레스적 전통"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="macintyre", document=doc)
    print(f"[thinker] macintyre: {result['result']}")
    return result


def insert_works(client):
    """매킨타이어 저서 데이터 입력."""
    works = [
        {
            "id": "macintyre-after-virtue",
            "thinker_id": "macintyre",
            "title": "덕의 상실",
            "title_original": "After Virtue: A Study in Moral Theory",
            "year": 1981,
            "significance": (
                "매킨타이어의 대표작이자 현대 덕 윤리 부흥의 촉발점. "
                "현대 도덕 담론이 '정서주의(emotivism)'로 전락했음을 진단하고, "
                "그 원인을 계몽주의가 도덕의 목적론적·공동체적 맥락을 파괴한 데서 찾는다. "
                "아리스토텔레스의 덕 윤리 전통을 복원함으로써 현대 도덕철학의 위기를 극복할 수 있다고 주장한다. "
                "'실천(practice)'과 '서사적 자아(narrative self)' 개념을 핵심 도구로 도입했다."
            ),
            "key_concepts": [
                "정서주의", "계몽주의 기획의 실패", "덕", "실천(practice)",
                "내적 선", "서사적 자아", "전통"
            ]
        },
        {
            "id": "macintyre-whose-justice",
            "thinker_id": "macintyre",
            "title": "누구의 정의? 어떤 합리성?",
            "title_original": "Whose Justice? Which Rationality?",
            "year": 1988,
            "significance": (
                "합리성이 중립적이고 보편적이라는 자유주의의 가정을 비판하는 저작. "
                "역사적으로 경쟁하는 다양한 정의 전통(아리스토텔레스, 아우구스티누스, 스코틀랜드 계몽주의, 자유주의)을 분석한다. "
                "합리성은 항상 특정 전통 안에서 작동하며, 전통 초월적 합리성은 환상이라고 주장한다. "
                "전통 의존적 합리성(tradition-dependent rationality) 개념을 체계화했다."
            ),
            "key_concepts": [
                "전통 의존적 합리성", "정의 전통", "자유주의적 합리성 비판",
                "인식론적 위기", "전통 내 합리성"
            ]
        },
        {
            "id": "macintyre-three-rival-versions",
            "thinker_id": "macintyre",
            "title": "도덕 탐구의 세 가지 경쟁 버전",
            "title_original": "Three Rival Versions of Moral Enquiry: Encyclopaedia, Genealogy, and Tradition",
            "year": 1990,
            "significance": (
                "도덕 탐구의 세 가지 경쟁 양식인 백과사전식(encyclopaedic), 계보학적(genealogical), "
                "전통적(traditional) 접근을 비교·분석한다. "
                "니체와 푸코류의 계보학 및 근대 백과사전식 도덕철학에 맞서 "
                "아리스토텔레스-토마스주의적 전통이 인식론적으로 우월함을 논증한다. "
                "1988년 에든버러 기포드 강의(Gifford Lectures)를 기반으로 한다."
            ),
            "key_concepts": [
                "백과사전적 도덕 탐구", "계보학적 도덕 탐구", "전통적 도덕 탐구",
                "토마스주의", "니체 비판"
            ]
        },
        {
            "id": "macintyre-dependent-rational-animals",
            "thinker_id": "macintyre",
            "title": "의존적 합리적 동물",
            "title_original": "Dependent Rational Animals: Why Human Beings Need the Virtues",
            "year": 1999,
            "significance": (
                "인간의 동물적 본성과 의존성(dependency)을 인정하는 데서 덕 윤리의 새로운 기초를 모색한다. "
                "우리는 모두 어린 시절, 노년, 질병 등에서 타인에게 의존하는 동물이며, "
                "이 취약성과 상호 의존성이 오히려 덕의 실천과 공동체 윤리의 근거임을 주장한다. "
                "자율적·독립적 개인을 전제하는 자유주의 윤리학을 생물학적·사회학적으로 비판한다."
            ),
            "key_concepts": [
                "의존적 합리성", "취약성", "상호 의존", "덕의 생물학적 기초",
                "인정 덕(acknowledged dependence)"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """매킨타이어 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 덕의 상실 — 계몽주의 도덕철학 비판
        {
            "id": "macintyre-claim-001",
            "thinker_id": "macintyre",
            "work_id": "macintyre-after-virtue",
            "source_detail": "After Virtue, Ch. 1-2",
            "claim": (
                "현대 도덕 담론은 심각한 혼란 상태에 있다. "
                "도덕적 논쟁은 끝날 수 없는(interminable) 성격을 가지며, "
                "상호 공약 불가능한(incommensurable) 전제들 위에서 이루어진다. "
                "이는 계몽주의가 도덕의 목적론적·공동체적 맥락을 파괴하고 "
                "탈맥락화된 도덕 언어의 파편들만 남긴 결과이다."
            ),
            "original_text": (
                "The most striking feature of contemporary moral utterance is that so much of it is used "
                "to express disagreements; and the most striking feature of the debates in which these "
                "disagreements are expressed is their interminable character. I do not mean by this just "
                "that such debates go on and on and on — although they do — but that they apparently "
                "can find no terminus. There seems to be no rational way of securing moral agreement."
            ),
            "original_text_ko": (
                "현대 도덕 발화에서 가장 두드러진 특징은 그 대부분이 불일치를 표현하는 데 사용된다는 점이다. "
                "그리고 이러한 불일치가 표현되는 논쟁들의 가장 두드러진 특징은 그것이 끝날 수 없는 성격이라는 점이다. "
                "나는 이로써 그런 논쟁이 그냥 계속되고 또 계속된다는 것을 의미하는 게 아니라 — 물론 그것도 사실이지만 — "
                "그것이 종결점을 찾지 못하는 것처럼 보인다는 것을 의미한다. "
                "도덕적 합의를 확보할 합리적 방법이 없는 것처럼 보인다."
            ),
            "explanation": (
                "매킨타이어는 현대 도덕 논쟁의 특징으로 세 가지를 제시한다: "
                "①개념적 공약 불가능성(논쟁 당사자들이 서로 다른 전제를 가짐), "
                "②주장들의 비인격적(impersonal) 성격(모두가 객관성을 주장), "
                "③논쟁의 역사적 기원의 불투명성(현대인은 그 개념들이 어디서 왔는지 모름). "
                "이런 혼란은 근대 계몽주의가 목적론적 맥락에서 분리된 도덕 언어의 파편들만 남긴 결과이다."
            ),
            "argument": (
                "(1) 현대 도덕 논쟁은 끝날 수 없는(interminable) 성격을 갖는다 — 낙태, 전쟁, 정의 논쟁 등. "
                "(2) 이 논쟁들은 각각 타당한 논리적 형식을 취하면서도 공약 불가능한 전제를 갖는다. "
                "(3) 이 현상의 원인은 도덕 언어가 본래의 맥락(목적론적·공동체적 전통)에서 분리된 데 있다. "
                "(4) 계몽주의는 신학적·목적론적 도덕의 맥락을 파괴하고 탈맥락화된 언어의 파편들을 남겼다. "
                "(5) 따라서 현대 도덕 담론은 참조 틀 없이 뒤섞인 개념들로 구성된다."
            ),
            "counterpoint": (
                "위르겐 하버마스(Jürgen Habermas)는 '도덕의식과 소통적 행위'(Moral Consciousness and Communicative Action, 1983)에서 "
                "도덕적 논쟁의 끝날 수 없는 성격이 전통의 상실 때문이 아니라 "
                "아직 소통적 합리성(communicative rationality)이 충분히 실현되지 않았기 때문이라고 반박했다. "
                "하버마스에 따르면 매킨타이어의 처방(공동체주의적 전통 복원)은 특정 전통의 패권을 강요할 위험이 있다."
            ),
            "context": (
                "1970년대 말~1980년대 영미 윤리학은 규칙 공리주의와 의무론의 대립, "
                "메타윤리학적 언어 분석에 치중하고 있었다. "
                "매킨타이어는 이런 조류를 역사적·사회적 맥락에서 비판하며 "
                "덕 윤리의 부흥을 촉발했다."
            ),
            "keywords": ["끝날 수 없는 도덕 논쟁", "계몽주의 기획", "도덕 담론의 혼란"],
            "verified": False
        },
        # CLAIM-002: 정서주의 비판
        {
            "id": "macintyre-claim-002",
            "thinker_id": "macintyre",
            "work_id": "macintyre-after-virtue",
            "source_detail": "After Virtue, Ch. 2-3",
            "claim": (
                "현대 도덕 문화는 사실상 정서주의(emotivism)를 내면화하고 있다. "
                "정서주의는 모든 도덕 판단이 개인의 태도와 감정의 표현에 불과하다는 이론으로, "
                "에이어(A.J. Ayer)와 스티븐슨(C.L. Stevenson)이 대표적이다. "
                "매킨타이어에 따르면 정서주의는 단순히 틀린 이론이 아니라, "
                "계몽주의 이후 도덕 문화가 실제로 정서주의적으로 변해버렸음을 잘 반영한다."
            ),
            "original_text": (
                "Emotivism is the doctrine that all evaluative judgments and more specifically all moral "
                "judgments are nothing but expressions of preference, expressions of attitude or feeling, "
                "insofar as they are moral or evaluative in character... "
                "I am going to argue that the theory is not so much mistaken as it is a correct account "
                "of a particular historical and cultural situation."
            ),
            "original_text_ko": (
                "정서주의는 모든 평가 판단, 더 구체적으로는 모든 도덕 판단이 선호의 표현, "
                "태도나 감정의 표현에 불과하다는 교설이다 — 그것들이 도덕적 혹은 평가적 성격을 갖는 한에서... "
                "나는 이 이론이 틀렸다기보다는 특정한 역사적·문화적 상황에 대한 올바른 기술이라고 논증할 것이다."
            ),
            "explanation": (
                "매킨타이어는 정서주의 이론 자체의 진위 문제를 넘어, "
                "현대 도덕 문화가 정서주의적 양식으로 작동하고 있다는 사회학적 진단을 제시한다. "
                "현대의 '관리자(manager)', '치료사(therapist)', '미학적 개인주의자(aesthete)' 등의 인물 유형이 "
                "정서주의 문화를 체현한다고 분석한다. "
                "이는 도덕 언어를 감정 조작의 도구로 사용하는 현대적 관행을 비판한다."
            ),
            "argument": (
                "(1) 정서주의(에이어, 스티븐슨)는 도덕 판단을 감정·태도의 표현으로 환원한다. "
                "(2) 이 이론은 개별 이론으로서 논박 가능하지만, 현대 문화를 진단하는 데는 정확하다. "
                "(3) 현대인들은 도덕 언어를 사용하면서 실제로는 타인의 행동에 영향을 미치려는 정서적 수단으로 사용한다. "
                "(4) '관리자', '치료사', '미학적 개인주의자'라는 현대적 인물 유형이 정서주의를 체현한다. "
                "(5) 정서주의 문화에서 도덕 논쟁은 합리적 설득이 아닌 감정 조작으로 전락한다."
            ),
            "counterpoint": (
                "R.M. 헤어(R.M. Hare)는 '도덕의 언어'(The Language of Morals, 1952)와 "
                "'도덕 사고'(Moral Thinking, 1981)에서 도덕 언어의 보편적 처방성(universal prescriptivity)을 강조하며, "
                "정서주의가 도덕 언어의 합리적 차원을 놓쳤다고 비판했다. "
                "헤어에 따르면 도덕 판단은 단순한 감정 표현이 아니라 보편화 가능한 처방이다."
            ),
            "context": (
                "20세기 중반 영어권 윤리학에서 정서주의(에이어 '언어, 진리, 논리', 1936)와 "
                "처방주의(헤어)가 주류를 이루고 있었다. "
                "매킨타이어는 이를 단순한 메타윤리학적 논쟁으로 보지 않고, "
                "역사적·문화적 현상으로 해석함으로써 새로운 비판적 시각을 제시했다."
            ),
            "keywords": ["정서주의", "감정 조작", "도덕 언어의 위기"],
            "verified": False
        },
        # CLAIM-003: 서사적 자아
        {
            "id": "macintyre-claim-003",
            "thinker_id": "macintyre",
            "work_id": "macintyre-after-virtue",
            "source_detail": "After Virtue, Ch. 15",
            "claim": (
                "인간의 자아(self)와 행위(action)는 서사(narrative)라는 틀 안에서만 이해될 수 있다. "
                "개별 행위는 단독으로는 의미를 가지지 못하며, "
                "더 넓은 이야기(story) 안에서 의도와 맥락을 통해 이해된다. "
                "인간은 '이야기하는 동물(story-telling animal)'이며, "
                "도덕적 정체성은 서사적 통일성(narrative unity) 속에서 형성된다."
            ),
            "original_text": (
                "It is because we all live out narratives in our lives and because we understand our own "
                "lives in terms of the narratives that we live out that the form of narrative is appropriate "
                "for understanding the actions of others. Stories are lived before they are told — "
                "except in the case of fiction. Man is in his actions and practice, as well as in his "
                "fictions, essentially a story-telling animal."
            ),
            "original_text_ko": (
                "우리 모두가 우리의 삶 안에서 서사를 살아내고, 우리가 살아내는 서사의 관점에서 "
                "우리 자신의 삶을 이해하기 때문에, 서사의 형식은 타인의 행위를 이해하는 데 적절하다. "
                "이야기는 — 허구의 경우를 제외하면 — 말해지기 전에 먼저 살아진다. "
                "인간은 자신의 행위와 실천 속에서, 그리고 허구 속에서도, 본질적으로 이야기하는 동물이다."
            ),
            "explanation": (
                "매킨타이어는 인간의 정체성이 원자적·탈맥락적 자아에서 나오지 않고, "
                "자신이 속한 공동체, 역사, 서사 속에서 형성된다고 주장한다. "
                "덕(virtue)은 이런 서사 속에서만 의미를 갖고 실천될 수 있다. "
                "이는 자유주의의 '무연고적 자아(unencumbered self)' 개념에 대한 직접적 비판이다."
            ),
            "argument": (
                "(1) 단일한 행위는 그 자체로 이해될 수 없으며, 더 넓은 서사 안에서 의도·목적이 드러난다. "
                "(2) 인간의 삶은 서사적 구조를 갖는다 — 시작, 중간, 끝이 있고 주제가 있다. "
                "(3) 개인의 정체성은 '나는 어떤 이야기의 일부인가?'라는 질문에 대한 답에서 나온다. "
                "(4) 도덕적 정체성은 공동체, 전통, 역할 속에서의 서사적 통일성이다. "
                "(5) 따라서 자유주의적 원자적 개인주의는 도덕적 자아의 실제 구조를 왜곡한다."
            ),
            "counterpoint": (
                "폴 리쾨르(Paul Ricœur)는 '자아 자신으로서의 타자'(Oneself as Another, 1992)에서 "
                "서사적 정체성 개념을 발전시키면서도, 매킨타이어가 서사적 자아를 지나치게 공동체에 고정시킴으로써 "
                "자아의 반성적 거리두기(distanciation)와 비판적 수정 가능성을 축소시켰다고 지적했다."
            ),
            "context": (
                "1970~80년대 분석철학은 행위 이론(action theory)에서 '의도'와 '원인'을 둘러싼 논쟁을 전개했다. "
                "매킨타이어는 이 논쟁에 역사적·서사적 차원을 도입하여, "
                "행위 이해에는 단순한 인과 분석을 넘어서는 해석학적 틀이 필요함을 주장했다."
            ),
            "keywords": ["서사적 자아", "이야기하는 동물", "서사적 통일성"],
            "verified": False
        },
        # CLAIM-004: 실천과 내적 선
        {
            "id": "macintyre-claim-004",
            "thinker_id": "macintyre",
            "work_id": "macintyre-after-virtue",
            "source_detail": "After Virtue, Ch. 14",
            "claim": (
                "덕(virtue)은 실천(practice)의 개념과 불가분하게 연결된다. "
                "실천이란 내적으로 일관된 협동적 사회 활동으로, "
                "내적 선(internal goods)을 실현하기 위해 탁월성의 기준에 복종하는 것이다. "
                "내적 선은 그 실천에 참여해야만 얻을 수 있으며, "
                "외적 선(external goods, 돈·명예·권력)과 구별된다."
            ),
            "original_text": (
                "A practice involves standards of excellence and obedience to rules as well as the "
                "achievement of goods. To enter into a practice is to accept the authority of those "
                "standards and the inadequacy of my own performance as judged by them. "
                "It is to subject my own attitudes, choices, preferences and tastes to the standards "
                "which currently and partially define the practice."
            ),
            "original_text_ko": (
                "실천은 탁월성의 기준들과 규칙들에 대한 복종, 그리고 선들의 성취를 포함한다. "
                "실천에 진입한다는 것은 그 기준들의 권위와, 그 기준들로 판단했을 때 나 자신의 수행의 "
                "불충분함을 받아들이는 것이다. "
                "그것은 현재 부분적으로 그 실천을 정의하는 기준들에 나 자신의 태도, 선택, 선호, 취향을 복종시키는 것이다."
            ),
            "explanation": (
                "매킨타이어는 체스, 건축, 농업, 의학, 음악 등의 예를 통해 실천을 설명한다. "
                "체스의 내적 선은 특정 종류의 분석적 기술·전략적 상상력·경쟁적 강도이며, "
                "이는 오직 체스를 통해서만, 체스의 탁월성 기준에 복종해야만 얻을 수 있다. "
                "외적 선(보상금, 명성)은 실천 외부에서도 얻을 수 있다. "
                "덕은 실천 안에서 내적 선을 추구하고 탁월성을 발전시키는 성품이다."
            ),
            "argument": (
                "(1) '실천(practice)'은 협동적 사회 활동으로, 내적으로 일관된 탁월성 기준을 갖는다. "
                "(2) 실천에는 내적 선과 외적 선이 있다. 내적 선은 그 실천에 참여해야만 얻을 수 있다. "
                "(3) 덕은 실천 안에서 내적 선의 성취를 가능하게 하는 성품이다. "
                "(4) 외적 선(돈, 권력, 명예)만을 추구하면 실천 자체를 부패시킨다. "
                "(5) 덕의 실천에는 제도(institution)가 필요하지만, 제도는 외적 선에 집착하여 실천을 부패시킬 위험도 있다."
            ),
            "counterpoint": (
                "마사 누스바움(Martha Nussbaum)은 '선의 취약성'(The Fragility of Goodness, 1986)에서 "
                "실천 개념이 전통 의존적이어서 다른 문화권의 사람들이 공유하는 덕의 보편성을 충분히 설명하지 못하며, "
                "아리스토텔레스의 덕 윤리는 능력 접근법(capabilities approach)으로 재구성해야 한다고 주장했다."
            ),
            "context": (
                "매킨타이어는 현대 사회에서 덕이 탈맥락화된 원인을 탐구하면서, "
                "덕이 실현될 수 있는 사회적 조건이 실천과 공동체임을 강조했다. "
                "이는 자유주의 사회의 관료제와 시장 논리가 실천의 내적 선을 위협한다는 사회 비판과 연결된다."
            ),
            "keywords": ["실천(practice)", "내적 선", "외적 선", "탁월성"],
            "verified": False
        },
        # CLAIM-005: 전통 의존적 합리성
        {
            "id": "macintyre-claim-005",
            "thinker_id": "macintyre",
            "work_id": "macintyre-whose-justice",
            "source_detail": "Whose Justice? Which Rationality?, Ch. 1, 18-20",
            "claim": (
                "합리성은 전통 의존적(tradition-dependent)이다. "
                "모든 합리적 탐구는 특정 전통의 맥락 안에서 이루어지며, "
                "전통 초월적이거나 전통 중립적인 합리성은 존재하지 않는다. "
                "자유주의가 주장하는 중립적 합리성은 사실상 자유주의 전통의 합리성에 불과하다."
            ),
            "original_text": (
                "What the Enlightenment made us for the most part blind to and what we now need to "
                "recover is... a conception of rational enquiry as embodied in a tradition, a conception "
                "according to which the standards of rational justification themselves emerge from and are "
                "part of a history in which they are vindicated by the way in which they transcend the "
                "limitations of and provide remedies for the defects of their predecessors within the "
                "forms of human intellectual and practical activity."
            ),
            "original_text_ko": (
                "계몽주의가 우리로 하여금 대부분 보지 못하게 한 것, 그리고 우리가 지금 회복해야 할 것은... "
                "전통 안에 체현된 합리적 탐구의 개념이다. 이 개념에 따르면 합리적 정당화의 기준들 자체가 "
                "하나의 역사에서 출현하고 그 역사의 일부이며, 그 역사 안에서 인간 지적·실천적 활동의 형식 내에서 "
                "선행자들의 한계를 초월하고 결함에 대한 치유책을 제공하는 방식으로 정당화된다."
            ),
            "explanation": (
                "매킨타이어는 아리스토텔레스, 아우구스티누스, 토마스 아퀴나스, 흄 등 네 개의 주요 정의·합리성 전통을 "
                "역사적으로 분석하여, 각 전통이 내부적 기준으로 합리성을 구성한다고 주장한다. "
                "합리성은 전통 내부에서 인식론적 위기를 극복하는 과정을 통해 발전한다. "
                "전통들 사이의 비교는 가능하지만, 그것은 전통 초월적 관점에서가 아니라 "
                "한 전통이 다른 전통의 문제를 더 잘 해결할 수 있음을 보여줌으로써 이루어진다."
            ),
            "argument": (
                "(1) 자유주의는 중립적·보편적 합리성을 표방하지만, 이것은 자유주의 전통의 합리성이다. "
                "(2) 모든 합리적 탐구는 출발점·방법론·목표를 제공하는 전통 안에서 이루어진다. "
                "(3) 전통들 사이의 합리적 비교는 가능하다 — 특정 전통이 다른 전통의 인식론적 위기를 더 잘 해결할 수 있다. "
                "(4) 아리스토텔레스-토마스 전통은 자유주의가 해결하지 못하는 도덕적 문제들을 더 잘 해결한다. "
                "(5) 따라서 전통의 포기가 아니라 전통의 비판적 발전이 합리적 도덕 탐구의 올바른 방식이다."
            ),
            "counterpoint": (
                "위르겐 하버마스(Jürgen Habermas)는 '도덕의식과 소통적 행위'(Moral Consciousness and Communicative Action, 1983)에서 "
                "전통 초월적 합리성은 존재하지 않는다는 매킨타이어의 주장이 상대주의로 귀결될 위험이 있다고 비판했다. "
                "하버마스는 소통적 행위(communicative action)의 이상적 발화 상황(ideal speech situation)이 "
                "전통 초월적 합리성의 기초를 제공한다고 주장했다."
            ),
            "context": (
                "1980년대 자유주의 정치철학(롤스, 드워킨)은 중립성(neutrality)을 핵심 원리로 표방했다. "
                "매킨타이어는 이런 자유주의의 합리성 주장이 자기 기만적이며, "
                "합리성은 항상 역사적·사회적 전통에 의존함을 주장했다."
            ),
            "keywords": ["전통 의존적 합리성", "인식론적 위기", "자유주의적 중립성 비판"],
            "verified": False
        },
        # CLAIM-006: 계몽주의 기획의 실패
        {
            "id": "macintyre-claim-006",
            "thinker_id": "macintyre",
            "work_id": "macintyre-after-virtue",
            "source_detail": "After Virtue, Ch. 4-9",
            "claim": (
                "계몽주의의 도덕 기획(the Enlightenment project)은 실패했다. "
                "계몽주의는 신학적·목적론적 맥락에서 분리된 도덕 원리를 순수한 이성만으로 "
                "정당화하려 했지만, 이 시도는 필연적으로 실패할 수밖에 없었다. "
                "칸트, 흄, 키르케고어 등의 도덕철학은 각각 다른 방식으로 이 실패를 드러낸다."
            ),
            "original_text": (
                "The Enlightenment project of justifying morality had to fail, and had to fail in just the "
                "way that it did fail, as a result of the transformation of human action as such, "
                "that is, of human life as such. The peculiarly modern self, the self that it is the "
                "achievement of the Enlightenment to have invented, finds no limits set to that on "
                "which it may pass judgment for such limits could only derive from rational criteria "
                "for judgment and prior to the application of such criteria the self is limitless."
            ),
            "original_text_ko": (
                "도덕을 정당화하려는 계몽주의 기획은 실패해야 했고, 실제로 그것이 실패한 바로 그 방식으로 "
                "실패해야 했다 — 인간 행위 자체의, 즉 인간 삶 자체의 변환의 결과로서. "
                "독특하게 근대적인 자아, 즉 계몽주의가 발명한 성취물인 자아는 "
                "그것이 판단을 내릴 수 있는 것에 한계가 설정되지 않는 자아를 발견한다. "
                "왜냐하면 그런 한계들은 오직 판단을 위한 합리적 기준들에서만 나올 수 있기 때문이다."
            ),
            "explanation": (
                "매킨타이어는 칸트의 정언명령, 흄의 감정 이론, 공리주의적 행복 이론이 모두 "
                "도덕의 참된 토대를 제공하는 데 실패했다고 분석한다. "
                "이 실패는 우연적인 것이 아니라, 목적론적(teleological) 틀을 제거한 채 "
                "도덕을 재구성하려는 시도 자체의 구조적 한계에서 비롯된다. "
                "목적론을 회복하지 않고는 도덕의 합리적 기초를 마련할 수 없다."
            ),
            "argument": (
                "(1) 아리스토텔레스적 도덕 구조는 '인간 본성 현재 모습', '인간 본성 이상 모습(목적)', "
                "'윤리학(이상 모습으로 나아가는 방법)' 세 요소로 구성된다. "
                "(2) 계몽주의는 목적론적 '인간 본성 이상 모습'을 제거함으로써 이 구조를 파괴했다. "
                "(3) 목적론 없이는 '인간 본성 현재 모습'에서 도덕적 처방을 끌어낼 수 없다. "
                "(4) 칸트는 순수 이성에서 도덕 원리를 도출하려 했으나, 공허한 형식주의에 빠졌다. "
                "(5) 공리주의는 쾌락·행복을 도덕 기준으로 삼았으나, 이 개념들이 너무 이질적이어서 "
                "공약 불가능한 계산 문제를 해결하지 못했다."
            ),
            "counterpoint": (
                "크리스틴 코스가드(Christine Korsgaard)는 '규범성의 근원'(The Sources of Normativity, 1996)에서 "
                "칸트적 구성주의는 목적론 없이도 도덕 규범의 정당성을 '반성적 보증(reflective endorsement)'을 통해 "
                "확보할 수 있다고 반박했다. "
                "매킨타이어의 목적론 회복 요구는 형이상학적 생물학에 의존하므로 현대 과학과 양립하기 어렵다는 비판도 있다."
            ),
            "context": (
                "매킨타이어는 아리스토텔레스 이후의 서양 도덕 사상사를 계몽주의 기획의 실패 과정으로 서술한다. "
                "특히 17세기 이후 도덕철학자들이 공유하는 인간 목적론의 포기가 "
                "현대 도덕 담론의 혼란을 낳은 근본 원인이라고 진단한다."
            ),
            "keywords": ["계몽주의 기획", "목적론", "도덕 정당화의 실패"],
            "verified": False
        },
        # CLAIM-007: 자유주의 비판
        {
            "id": "macintyre-claim-007",
            "thinker_id": "macintyre",
            "work_id": "macintyre-whose-justice",
            "source_detail": "Whose Justice? Which Rationality?, Ch. 17",
            "claim": (
                "자유주의적 개인주의(liberal individualism)는 인간을 공동체와 전통에서 분리된 "
                "원자적 개인으로 잘못 이해한다. "
                "자유주의는 공동체, 역사, 전통이 자아의 정체성 형성에 본질적임을 인정하지 않으며, "
                "그 '중립적 합리성' 주장은 자기기만적이다. "
                "자유주의 국가의 도덕적 중립성은 실제로는 특정 형태의 삶(소비주의적 개인주의)을 지지한다."
            ),
            "original_text": (
                "Liberalism, while appearing to represent a neutral tradition-independent position, "
                "is itself a tradition, embodying its own conceptions of rationality, justice, and the good. "
                "To present it as neutral is therefore deeply misleading, for it disguises the ways in "
                "which liberal theory and practice systematically disadvantage those who are not already "
                "committed to some version of liberal individualism."
            ),
            "original_text_ko": (
                "자유주의는 전통 중립적인 입장을 대표하는 것처럼 보이지만, "
                "그 자체로 합리성, 정의, 선에 대한 자신의 관념들을 체현하는 하나의 전통이다. "
                "그것을 중립적으로 제시하는 것은 따라서 심각하게 오해를 낳는 것이다. "
                "왜냐하면 그것은 자유주의 이론과 실천이 체계적으로 자유주의적 개인주의의 어떤 버전에 이미 "
                "헌신하지 않은 이들을 불리하게 만드는 방식들을 위장하기 때문이다."
            ),
            "explanation": (
                "매킨타이어는 자유주의가 주장하는 '공동선보다 권리 우선'의 원칙이 "
                "사실상 특정 자아관(무연고적 자아)과 특정 합리성 관념을 전제한다고 비판한다. "
                "롤스의 원초적 입장과 무지의 베일은 공동체와 전통적 유대에서 분리된 "
                "비역사적 자아를 전제한다. "
                "자유주의 사회는 실제로 공동체적 덕의 실천에 필요한 사회적 조건을 훼손한다."
            ),
            "argument": (
                "(1) 자유주의는 도덕적 중립성을 표방하지만, 이는 자기기만이다. "
                "(2) 자유주의 자체가 특정 자아관(원자적·무연고적 자아)과 합리성 관념을 갖는 전통이다. "
                "(3) 자유주의는 사람들이 자신의 공동체적 맥락과 역할에서 정체성을 찾는 것을 방해한다. "
                "(4) 자유주의 국가의 중립성 주장은 소비주의적·개인주의적 삶의 양식을 사실상 지지한다. "
                "(5) 공동체주의적 관점에서 사회는 개인들의 목적 추구를 위한 도구가 아니라, "
                "덕의 실현과 인간 번영(flourishing)의 조건이다."
            ),
            "counterpoint": (
                "존 롤스(John Rawls)는 '정치적 자유주의'(Political Liberalism, 1993)에서 "
                "자신의 자유주의는 포괄적 교설(comprehensive doctrine)로서의 자유주의가 아니라 "
                "합당한 다원주의를 전제로 한 정치적 자유주의이므로, "
                "매킨타이어의 비판이 목표를 잘못 삼았다고 응답했다."
            ),
            "context": (
                "1980년대 공동체주의 논쟁은 샌델('자유주의와 정의의 한계', 1982), "
                "테일러('자아의 원천들', 1989), 왈처('정의의 영역들', 1983)와 함께 전개되었다. "
                "매킨타이어는 그 중에서도 가장 급진적으로 자유주의 기획 전체를 역사적·철학적으로 비판했다."
            ),
            "keywords": ["자유주의적 개인주의 비판", "무연고적 자아", "자유주의의 전통성"],
            "verified": False
        },
        # CLAIM-008: 덕윤리의 복원
        {
            "id": "macintyre-claim-008",
            "thinker_id": "macintyre",
            "work_id": "macintyre-after-virtue",
            "source_detail": "After Virtue, Ch. 10-18",
            "claim": (
                "아리스토텔레스의 덕 윤리 전통을 복원함으로써 현대 도덕철학의 위기를 극복할 수 있다. "
                "덕(virtue)이란 실천(practice)에 참여하고, 서사적 삶을 살며, "
                "전통 속에서 인간 번영(flourishing)을 실현하는 데 필요한 성품이다. "
                "매킨타이어는 새로운 성 베네딕트를 기다린다는 말로 책을 마무리하며, "
                "덕의 전통을 보전할 공동체 건설의 중요성을 강조했다."
            ),
            "original_text": (
                "What matters at this stage is the construction of local forms of community within which "
                "civility and the intellectual and moral life can be sustained through the new dark ages "
                "which are already upon us. And if the tradition of the virtues was able to survive the "
                "horrors of the last dark ages, we are not entirely without grounds for hope. "
                "This time however the barbarians are not waiting beyond the frontiers; they have already "
                "been governing us for quite some time. And it is our lack of consciousness of this that "
                "constitutes part of our predicament. We are waiting not for a Godot, but for another "
                "— doubtless very different — St Benedict."
            ),
            "original_text_ko": (
                "이 단계에서 중요한 것은 이미 우리에게 닥친 새로운 암흑시대를 통해 시민적 교양과 "
                "지적·도덕적 삶이 유지될 수 있는 공동체의 지역적 형태들을 구성하는 것이다. "
                "덕의 전통이 지난 암흑시대의 공포들을 견뎌낼 수 있었다면, "
                "우리는 희망의 근거가 전혀 없지는 않다. "
                "그러나 이번에는 야만인들이 국경 너머에서 기다리고 있지 않다. "
                "그들은 이미 꽤 오랫동안 우리를 통치해 왔다. "
                "그리고 이것에 대한 우리의 의식 부재가 우리 곤경의 일부를 이룬다. "
                "우리는 고도를 기다리는 것이 아니라, 또 다른 — 의심할 여지 없이 매우 다른 — "
                "성 베네딕트를 기다리고 있다."
            ),
            "explanation": (
                "매킨타이어는 덕을 세 층위에서 이해한다: "
                "①실천(practice)의 내적 선 추구를 가능하게 하는 덕, "
                "②서사적 삶의 통일성을 유지하게 하는 덕, "
                "③전통의 탐구를 지속시키는 덕. "
                "이 삼층 구조 안에서 정직, 용기, 정의, 절제 등의 덕이 상호 연결된다. "
                "현대 암흑시대를 극복하기 위해서는 새로운 형태의 공동체(수도원 같은)가 필요하다."
            ),
            "argument": (
                "(1) 현대 도덕 담론의 혼란을 치유하려면 탈맥락화된 도덕 이론이 아니라 "
                "실천·서사·전통이라는 맥락 속에서 덕 윤리를 복원해야 한다. "
                "(2) 덕 윤리는 '인간 번영(flourishing/eudaimonia)'이라는 목적론을 전제한다. "
                "(3) 인간 번영은 공동체적 실천 안에서만 가능하며, 탈맥락화된 개인에게는 가능하지 않다. "
                "(4) 따라서 덕의 전통을 보전하는 지역 공동체의 건설이 필요하다. "
                "(5) 이는 단순한 전통 보수주의가 아니라, 역사적으로 발전하는 살아있는 전통의 복원이다."
            ),
            "counterpoint": (
                "그레고리 블랙(Gregory Vlastos)이나 줄리아 앤나스(Julia Annas)같은 고대 철학 연구자들은 "
                "'헬레니스틱 윤리학'(Hellenistic Ethics in Focus, 1994)류의 연구에서 "
                "매킨타이어의 아리스토텔레스 독해가 지나치게 선별적이며, "
                "아리스토텔레스의 목적론을 현대에 복원하는 것은 그 형이상학적·생물학적 전제들 때문에 난관에 봉착한다고 지적했다."
            ),
            "context": (
                "매킨타이어는 '덕의 상실'의 결론부에서 현대 자유민주주의 국가를 '새로운 암흑시대'로 규정하고, "
                "새로운 베네딕트를 기다린다는 선언으로 마무리하여 학계에 큰 파장을 일으켰다."
            ),
            "keywords": ["덕윤리 복원", "인간 번영", "새로운 베네딕트"],
            "verified": False
        },
        # CLAIM-009: 공동체와 덕
        {
            "id": "macintyre-claim-009",
            "thinker_id": "macintyre",
            "work_id": "macintyre-after-virtue",
            "source_detail": "After Virtue, Ch. 14-15; Dependent Rational Animals, Ch. 8-10",
            "claim": (
                "덕의 실현에는 공동체가 필수적이다. "
                "인간은 의존적 합리적 동물(dependent rational animals)로서, "
                "어린 시절·노년·질병 등에서 타인에게 의존하며 상호 돌봄의 관계 속에서 성장한다. "
                "덕은 이 의존적·공동체적 맥락 안에서만 실천되고 발전될 수 있으며, "
                "독립적 개인을 전제하는 자유주의 윤리학은 인간의 실제 조건을 왜곡한다."
            ),
            "original_text": (
                "We are all vulnerable to afflictions of body and mind, we are all dependent on others "
                "for our development as practical reasoners, and we all need the virtues, if we are to "
                "function well in sustaining those relationships of giving and receiving through which our "
                "common goods are achieved. "
                "The exercise of independent practical reasoning is itself one of the tasks of the "
                "virtuous, and it presupposes a type of community within which this practical reasoning "
                "can be developed."
            ),
            "original_text_ko": (
                "우리는 모두 육체와 정신의 고통에 취약하며, "
                "실천적 추론자로서의 우리 발전에서 타인에게 의존한다. "
                "그리고 우리 공동의 선이 성취되는 주고받는 관계들을 유지하는 데 잘 기능하려면 "
                "우리 모두는 덕들이 필요하다. "
                "독립적 실천 추론의 행사는 그 자체로 덕 있는 이들의 과제들 중 하나이며, "
                "이 실천 추론이 발전될 수 있는 공동체의 유형을 전제한다."
            ),
            "explanation": (
                "1999년의 '의존적 합리적 동물'에서 매킨타이어는 '덕의 상실'보다 더 나아가, "
                "인간의 동물적 취약성과 상호 의존성으로부터 덕의 필요성을 논증한다. "
                "인간이 의존하는 공동체 안에서 인정 덕(acknowledged dependence)이 발전하며, "
                "이것이 공동체적 삶의 덕이 개인의 자율성보다 더 근본적임을 보여준다."
            ),
            "argument": (
                "(1) 인간은 어린 시절·노년·질병에서 필연적으로 타인에 의존한다. "
                "(2) 인간 번영은 이런 의존적 관계를 통해 이루어지며, 이 관계가 공동체를 구성한다. "
                "(3) 실천적 추론 능력 자체가 공동체 안에서 발전된다 — 언어, 교육, 제도를 통해. "
                "(4) 따라서 덕의 실천은 공동체 없이는 불가능하다. "
                "(5) 자유주의 윤리학이 전제하는 독립적·자율적 개인은 허구이며, "
                "현실의 의존적 인간 조건을 무시한다."
            ),
            "counterpoint": (
                "윌 킴리카(Will Kymlicka)는 '자유주의 공동체주의와 문화'(Liberalism, Community and Culture, 1989)에서 "
                "자유주의도 공동체의 중요성을 충분히 수용할 수 있으며, "
                "자유주의적 개인주의가 반드시 원자적 개인을 전제하지는 않는다고 반론을 제기했다. "
                "킴리카는 자유주의적 다문화주의가 공동체와 문화의 중요성을 인정한다고 주장했다."
            ),
            "context": (
                "1990년대 이후 공동체주의 논쟁은 자유주의-공동체주의 이분법을 넘어서는 방향으로 전개되었다. "
                "매킨타이어는 '의존적 합리적 동물'에서 공동체의 필요성을 생물학적·인류학적 기반 위에 놓음으로써 "
                "공동체주의 논증을 더욱 강화했다."
            ),
            "keywords": ["공동체와 덕", "의존적 합리적 동물", "상호 의존", "인정 덕"],
            "verified": False
        },
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """매킨타이어 관련 키워드 데이터 입력."""
    keywords = [
        {
            "id": "macintyre-kw-emotivism",
            "term": "정서주의",
            "term_en": "Emotivism",
            "definition": (
                "모든 도덕 판단이 감정·태도의 표현에 불과하다는 메타윤리학적 이론(에이어, 스티븐슨). "
                "매킨타이어는 이 이론 자체의 옳고 그름을 넘어, "
                "현대 도덕 문화가 실제로 정서주의적으로 작동하고 있다고 진단했다."
            ),
            "thinker_id": "macintyre",
            "work_id": "macintyre-after-virtue",
            "related_terms": ["도덕 담론의 혼란", "계몽주의 기획", "도덕 언어"]
        },
        {
            "id": "macintyre-kw-narrative-self",
            "term": "서사적 자아",
            "term_en": "Narrative Self",
            "definition": (
                "인간의 정체성은 원자적·탈맥락적 자아에서 나오지 않고, "
                "자신이 속한 공동체, 역사, 이야기(narrative) 속에서 형성된다는 개념. "
                "인간은 '이야기하는 동물'이며, 도덕적 정체성은 서사적 통일성 속에서 발전한다."
            ),
            "thinker_id": "macintyre",
            "work_id": "macintyre-after-virtue",
            "related_terms": ["서사적 통일성", "공동체주의", "자아 정체성"]
        },
        {
            "id": "macintyre-kw-practice",
            "term": "실천(practice)",
            "term_en": "Practice",
            "definition": (
                "매킨타이어의 핵심 개념. 내적으로 일관된 협동적 사회 활동으로, "
                "내적 선(internal goods)을 실현하기 위해 탁월성의 기준에 복종하는 것. "
                "체스, 건축, 의학, 농업, 음악 등이 예이며, 이 실천 안에서만 덕이 의미를 갖는다."
            ),
            "thinker_id": "macintyre",
            "work_id": "macintyre-after-virtue",
            "related_terms": ["내적 선", "외적 선", "탁월성", "덕"]
        },
        {
            "id": "macintyre-kw-internal-goods",
            "term": "내적 선",
            "term_en": "Internal Goods",
            "definition": (
                "특정 실천(practice)에 참여해야만 획득할 수 있는 선(goods). "
                "예컨대 체스의 내적 선은 분석적 기술·전략적 상상력이며, "
                "이는 오직 체스를 통해서만, 체스의 탁월성 기준에 복종해야만 얻을 수 있다. "
                "외적 선(돈, 명예, 권력)과 달리 공동체적 차원을 가진다."
            ),
            "thinker_id": "macintyre",
            "work_id": "macintyre-after-virtue",
            "related_terms": ["실천(practice)", "외적 선", "덕", "탁월성"]
        },
        {
            "id": "macintyre-kw-tradition-rationality",
            "term": "전통 의존적 합리성",
            "term_en": "Tradition-Dependent Rationality",
            "definition": (
                "합리성은 항상 특정 전통의 맥락 안에서 작동하며, "
                "전통 초월적·전통 중립적 합리성은 존재하지 않는다는 개념. "
                "자유주의의 중립적 합리성 주장은 사실상 자유주의 전통의 합리성에 불과하다. "
                "전통들 사이의 합리적 비교는 한 전통이 다른 전통의 인식론적 위기를 더 잘 해결함을 보임으로써 가능하다."
            ),
            "thinker_id": "macintyre",
            "work_id": "macintyre-whose-justice",
            "related_terms": ["인식론적 위기", "자유주의 비판", "전통"]
        },
        {
            "id": "macintyre-kw-enlightenment-project",
            "term": "계몽주의 기획",
            "term_en": "Enlightenment Project",
            "definition": (
                "신학적·목적론적 맥락에서 분리된 도덕 원리를 순수 이성만으로 정당화하려 한 계몽주의의 기획. "
                "매킨타이어에 따르면 이 기획은 필연적으로 실패했으며, "
                "그 결과가 현대 도덕 담론의 혼란이다. "
                "칸트, 흄, 공리주의가 대표적 실패 사례이다."
            ),
            "thinker_id": "macintyre",
            "work_id": "macintyre-after-virtue",
            "related_terms": ["목적론", "계몽주의 도덕철학 비판", "덕의 상실"]
        },
        {
            "id": "macintyre-kw-after-virtue",
            "term": "덕의 상실",
            "term_en": "After Virtue",
            "definition": (
                "매킨타이어의 1981년 저작이자 개념. "
                "계몽주의가 목적론적·공동체적 맥락에서 도덕을 분리시킨 후, "
                "아리스토텔레스적 덕 전통이 상실되었음을 가리킨다. "
                "현대 도덕 담론은 덕의 상실 이후 파편화된 언어들의 혼합에 불과하다는 진단."
            ),
            "thinker_id": "macintyre",
            "work_id": "macintyre-after-virtue",
            "related_terms": ["계몽주의 기획", "덕윤리", "아리스토텔레스 전통"]
        },
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """매킨타이어 관련 관계 데이터 입력."""
    relations = [
        {
            "id": "aristotle-influenced-macintyre",
            "from_thinker": "aristotle",
            "to_thinker": "macintyre",
            "type": "influenced",
            "description": (
                "아리스토텔레스의 덕 윤리, 목적론, 실천지(phronesis), 에우다이모니아 개념이 "
                "매킨타이어의 덕 윤리 복원 프로그램의 핵심 토대가 되었다. "
                "매킨타이어는 '덕의 상실'에서 아리스토텔레스적 도덕 전통의 복원을 주장했다."
            ),
            "evidence": "After Virtue, Ch. 12 'Aristotle's Account of the Virtues'"
        },
        {
            "id": "macintyre-influenced-sandel",
            "from_thinker": "macintyre",
            "to_thinker": "sandel",
            "type": "influenced",
            "description": (
                "매킨타이어의 공동체주의적 비판(자유주의적 개인주의 비판, 공동체와 전통의 중요성)이 "
                "샌델의 자유주의 비판('자유주의와 정의의 한계', 1982)과 공동선 추구 정치철학에 영향을 주었다. "
                "두 사람은 롤스식 자유주의 비판이라는 공동체주의 운동의 핵심을 공유한다."
            ),
            "evidence": "Sandel, Liberalism and the Limits of Justice (1982), Introduction"
        },
        {
            "id": "macintyre-criticized-rawls",
            "from_thinker": "macintyre",
            "to_thinker": "rawls",
            "type": "criticized",
            "description": (
                "매킨타이어는 롤스의 자유주의적 정의론이 공동체와 전통에서 분리된 '무연고적 자아'를 전제하며, "
                "그 정의 원칙은 전통 중립적 합리성이라는 허구 위에 세워졌다고 비판했다. "
                "또한 롤스의 원초적 입장이 특정 자유주의 전통의 관점을 보편적으로 가장한다고 보았다."
            ),
            "evidence": "After Virtue, Ch. 17; Whose Justice? Which Rationality?, Ch. 17"
        }
    ]

    inserted = 0
    for rel in relations:
        # 중복 확인
        try:
            existing = client.search(
                index=INDEX_RELATIONS,
                query={"bool": {"must": [
                    {"term": {"from_thinker": rel["from_thinker"]}},
                    {"term": {"to_thinker": rel["to_thinker"]}},
                    {"term": {"type": rel["type"]}}
                ]}},
                size=1
            )
            if existing["hits"]["total"]["value"] > 0:
                print(f"[relation] {rel['id']}: 이미 존재 — skip")
                continue
        except Exception as e:
            print(f"[relation] 중복 확인 오류: {e}")

        result = client.index(index=INDEX_RELATIONS, id=rel["id"], document=rel)
        print(f"[relation] {rel['id']}: {result['result']}")
        inserted += 1

    return inserted


def verify_data(client):
    """입력된 데이터 검증."""
    print("\n=== 데이터 검증 ===")

    # thinker 확인
    try:
        thinker = client.get(index=INDEX_THINKERS, id="macintyre")
        print(f"[thinker] macintyre: 존재 ({thinker['_source']['name']})")
    except Exception:
        print("[thinker] macintyre: 없음 (오류)")

    # works 수 확인
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "macintyre"}})
    print(f"[works] macintyre 저서 수: {works_count['count']}")

    # claims 수 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "macintyre"}})
    print(f"[claims] macintyre 주장 수: {claims_count['count']}")

    # claim 필수 필드 확인
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "macintyre"}},
        _source=["id", "argument", "counterpoint", "original_text", "original_text_ko"],
        size=20
    )
    missing_fields = []
    for hit in claims_result["hits"]["hits"]:
        s = hit["_source"]
        cid = s.get("id", hit["_id"])
        for field in ["argument", "counterpoint", "original_text", "original_text_ko"]:
            if not s.get(field):
                missing_fields.append(f"{cid}.{field}")

    if missing_fields:
        print(f"[경고] 필수 필드 누락: {missing_fields}")
    else:
        print("[OK] 모든 claim에 argument+counterpoint+original_text+original_text_ko 존재")

    # keywords 확인
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "macintyre"}})
    print(f"[keywords] macintyre 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_count = client.count(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "macintyre"}},
            {"term": {"to_thinker": "macintyre"}}
        ]}}
    )
    print(f"[relations] macintyre 관련 관계 수: {rel_count['count']}")
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "macintyre"}},
            {"term": {"to_thinker": "macintyre"}}
        ]}},
        _source=["id", "from_thinker", "to_thinker", "type"],
        size=10
    )
    for hit in rel_result["hits"]["hits"]:
        s = hit["_source"]
        print(f"  - {s['id']}: {s['from_thinker']} --[{s['type']}]--> {s['to_thinker']}")

    return {
        "works": works_count["count"],
        "claims": claims_count["count"],
        "keywords": kw_count["count"],
        "relations": rel_count["count"],
        "missing_fields": missing_fields
    }


def main():
    client = get_client()
    try:
        print("=== 앨러스데어 매킨타이어(Alasdair MacIntyre) 데이터 입력 시작 ===\n")

        print("0. 분야(western_ethics) 확인/추가")
        ensure_field(client)

        print("\n1. 사상가 입력")
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
        print(f"field: 1건 | thinker: 1건 | works: {stats['works']}건 | claims: {stats['claims']}건 | "
              f"keywords: {stats['keywords']}건 | relations: {stats['relations']}건")

        return stats

    finally:
        close_client(client)


if __name__ == "__main__":
    main()
