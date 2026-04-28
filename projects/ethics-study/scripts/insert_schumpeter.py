"""조지프 슘페터(Joseph Alois Schumpeter) 데이터를 ES에 직접 입력하는 스크립트.

Task: TASK-212-02
공식 출제: 2026-B Q6 (나) (BLK-175E-2026B-004 · row 기준 최초 등장).
오스트리아-헝가리 제국 모라비아 출생 미국 하버드대 경제학자·사회학자·정치경제학자
(1883-1950) — 20세기 자본주의·사회주의·민주주의 비교 이론의 정초자.

political_philosophy 분야. rousseau/locke/nozick/rawls/macintyre/sandel/walzer/taylor/
pettit/habermas 등 동일 field 등록 패턴 답습.
era=`현대` (rawls·nozick·sandel·pettit 1900년대 출생 political_philosophy 8건 모두 동일 표기).

원문 인용 규칙(agents/coder.md §원문/입력 인용 규칙) 엄수:
 - claims.original_text 는 coverage/2026-B.md L337-L400 verbatim + 출처 주석.
 - 모든 한자·영어 trademark 는 coverage md / blocker-log 출처 확증된 토큰만 사용.
 - 출처 부재 trademark 0개 (fabrication 후보 제거).

자기검증 3-step (schumpeter 토큰 ∩=0 확증, coder report 적재):
 - Step 1 — bare-paren `\\([A-Za-z][^)]*\\)` (TitleCase 영문 wrap만 — coverage hit 토큰)
 - Step 1b — Greek `[Α-Ωα-ω]` / macron `[\\u0100-\\u024F]` (0건 — 독일어 verbatim 보존)
 - Step 2 — TitleCase `[A-Z][a-z]+(\\s+[A-Za-z][a-z]+){1,5}` 예시 토큰: Joseph Alois Schumpeter ·
   Capitalism Socialism Democracy · Another Theory · Theorie Wirtschaftlichen Entwicklung
 - disjoint 검증: Step1 ∩ Step1b ∩ Step2 = 0 (3-set 교집합 0건)

참조 출처 (verbatim only):
 - `projects/ethics-study/exam-solutions/coverage/2026-B.md` L337-L400
 - `projects/ethics-study/exam-solutions/study-guide/2026-B.md` L351-L400
 - `signal/ethics-study/blocker-log.md` L1123-L1129
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS,
    INDEX_WORKS,
    INDEX_CLAIMS,
    INDEX_KEYWORDS,
    INDEX_RELATIONS,
    INDEX_FIELDS,
)


THINKER_ID = "schumpeter"


def ensure_field(client):
    """political_philosophy 분야 존재 확인 (rousseau/pettit/rawls 등 등록 확인됨)."""
    try:
        client.get(index=INDEX_FIELDS, id="political_philosophy")
        print("[field] political_philosophy: 이미 존재")
    except Exception:
        doc = {
            "id": "political_philosophy",
            "name": "정치철학",
            "description": (
                "정치 공동체의 정당성·자유·정의·권력·권리 등을 탐구하는 철학 분야. "
                "자유주의·공화주의·공동체주의·자유지상주의 등 현대 정치사상 계보를 포함한다."
            ),
            "order": 5,
        }
        result = client.index(index=INDEX_FIELDS, id="political_philosophy", document=doc)
        print(f"[field] political_philosophy: {result['result']}")


def insert_thinker(client):
    """슘페터 사상가 데이터 입력."""
    doc = {
        "id": THINKER_ID,
        "name": "조지프 슘페터 (Joseph Alois Schumpeter)",
        "name_en": "Joseph Alois Schumpeter",
        "field": "political_philosophy",
        "era": "현대",
        "birth_year": 1883,
        "death_year": 1950,
        "background": (
            "오스트리아-헝가리 제국 모라비아(현 체코) 출생의 경제학자·사회학자·정치경제학자(1883-1950). "
            "오스트리아학파(Austrian School) 빈 대학에서 뵘-바베르크(Böhm-Bawerk)·비저(Wieser)에게 사사하였고, "
            "오스트리아 재무장관(1919)·본대학 교수를 거쳐 1932년 미국 하버드대학교로 이주, "
            "1950년 사망 시까지 하버드 경제학과 교수로 재직하였다. "
            "케인즈와 동시대 라이벌로, 거시 수요·재정정책 중심의 케인즈와 달리 "
            "혁신·기업가·창조적 파괴 등 자본주의 동학(動學)을 분석한 사회학적·역사적 경제학 전통을 계승하였다. "
            "주요 저작 『경제 발전의 이론(Theorie der wirtschaftlichen Entwicklung, 1911 / 영역 1934)』 · "
            "『경기순환(Business Cycles, 1939)』 · "
            "『자본주의·사회주의·민주주의(Capitalism, Socialism and Democracy, 1942)』 · "
            "사후 출판 『경제분석의 역사(History of Economic Analysis, 1954)』. "
            "임용 도덕·윤리 시험에서 2026-B Q6 (나) row 기준 최초 출제 (BLK-175E-2026B-004 해소 대상)."
        ),
        "core_philosophy": (
            "슘페터 정치경제학의 핵심은 두 축으로 구성된다. "
            "첫째, 경제 영역에서는 '창조적 파괴(creative destruction)'와 '혁신(innovation)' 이론으로 "
            "자본주의의 동학을 설명한다. 자본주의는 정태적 균형이 아니라 "
            "기업가(entrepreneur)의 혁신을 통해 낡은 구조가 파괴되고 새로운 구조가 창출되는 "
            "끊임없는 변동 과정이며, 혁신은 "
            "신제품·신생산방법·신시장·신원료·신조직의 5유형 '새로운 결합(new combinations)'으로 실현된다. "
            "둘째, 정치 영역에서는 '경쟁적 엘리트 민주주의(competitive elitist democracy)' · "
            "절차적·최소주의적 민주주의를 정식화한다. "
            "민주주의는 인민의 자치(self-government of the people)나 일반의지의 실현이 아니라, "
            "'정치적 결정에 도달하기 위한 제도적 장치(institutional arrangement)' / "
            "'하나의 정치적 방법(political method)'이다. "
            "정치인들이 국민의 표(people's vote)를 얻기 위해 경쟁적으로 투쟁하여 결정 권력을 획득하는 메커니즘이며, "
            "고전적 민주주의 이론의 3전제 — 공동선의 존재, 공동선을 인식하는 합리적 시민, 인민 의지의 존재 — 는 모두 사실에 부합하지 않는다고 비판한다. "
            "셋째, 자본주의의 필연적 쇠퇴를 예측한다 — 합리화·관료화로 기업가 정신이 소멸하고 "
            "지식인 계층의 자본주의 비판이 강화되어 사회주의로의 이행이 불가피하다는 진단이다. "
            "이는 마르크스의 '자본주의 모순으로 인한 붕괴'와는 다른 경로로, "
            "'자본주의의 성공이 그 자신의 토대를 잠식한다'는 역설적 쇠퇴론이다."
        ),
        "philosophical_journey": (
            "슘페터는 1883년 오스트리아-헝가리 제국 모라비아의 트리에슈에서 출생하였다. "
            "빈 대학 법학·경제학 박사(1906)로 카를 멩거 후속 세대 오스트리아학파의 일원으로 출발하였으나, "
            "1911년 『경제 발전의 이론(Theorie der wirtschaftlichen Entwicklung)』에서 "
            "정태적 균형이론을 넘어 동태적 발전 이론을 정립하며 독자적 노선으로 전환하였다. "
            "이 저작에서 '기업가(entrepreneur)'를 새로운 결합을 실현하는 혁신의 담지자로 규정하고, "
            "신용·이자·이윤을 혁신과 결합한 동학적 분석으로 재구성하였다. "
            "1919년 오스트리아 공화국 초대 재무장관으로 짧게 재직한 후 학계로 복귀하여 "
            "본대학 교수(1925-1932)를 거쳐 1932년 미국 하버드대학교로 이주하였다. "
            "1939년 『경기순환(Business Cycles)』에서 콘드라티예프 장기파동·쥐글라르 파동·키친 파동을 "
            "통합한 다중 파동 이론을 제시하였고, "
            "1942년 『자본주의·사회주의·민주주의(Capitalism, Socialism and Democracy)』에서 "
            "5부 구성(마르크스 이론 / 자본주의 / 사회주의 / 사회주의와 민주주의 / 사회주의 정당의 역사)으로 "
            "20세기 정치경제학 정전을 완성하였다. 특히 제22장 '또 다른 민주주의 이론(Another Theory of Democracy)'에서 "
            "고전적 민주주의 이론을 비판하고 경쟁적 엘리트 민주주의를 정식화한 부분은 "
            "달(Robert Dahl) 『민주주의 이론 서론(A Preface to Democratic Theory, 1956)』·『폴리아키(Polyarchy, 1971)』 · "
            "립셋(Lipset) · 헌팅턴(Huntington) 등 후대 민주주의 경험 이론의 원류가 되었다. "
            "1950년 미국 코네티컷주에서 사망하였고, 사후 1954년 미망인 엘리자베스 슘페터의 편집으로 "
            "『경제분석의 역사(History of Economic Analysis, 1954)』가 출판되었다."
        ),
        "keywords": [
            "창조적 파괴",
            "혁신",
            "기업가",
            "새로운 결합",
            "경쟁적 엘리트 민주주의",
            "절차적 민주주의",
            "최소주의 민주주의",
            "고전적 민주주의 비판",
            "정치적 방법",
            "제도적 장치",
            "자본주의 쇠퇴 예측",
            "오스트리아학파",
        ],
    }
    result = client.index(index=INDEX_THINKERS, id=THINKER_ID, document=doc)
    print(f"[thinker] {THINKER_ID}: {result['result']}")
    return result


def insert_works(client):
    """슘페터 주요 저서 데이터 입력."""
    works = [
        {
            "id": "schumpeter-csd-1942",
            "thinker_id": THINKER_ID,
            "title": "자본주의·사회주의·민주주의",
            "title_original": "Capitalism, Socialism and Democracy",
            "year": 1942,
            "significance": (
                "슘페터 후기 정치경제학의 정전이자 20세기 자본주의·사회주의·민주주의 비교 이론의 고전. "
                "5부 구성: 제1부 마르크스 이론 / 제2부 자본주의(창조적 파괴) / "
                "제3부 사회주의(가능성·작동방식) / 제4부 사회주의와 민주주의 / 제5부 사회주의 정당사. "
                "특히 제2부 제7장 '창조적 파괴의 과정'에서 "
                "자본주의 동학의 핵심 개념인 '창조적 파괴(creative destruction)'를 정식화하고, "
                "제4부 제22장 '또 다른 민주주의 이론(Another Theory of Democracy)'에서 "
                "고전적 민주주의 이론(인민자치·일반의지·공동선)을 비판하고 "
                "'경쟁적 엘리트 민주주의(competitive elitist democracy)'를 제시한다. "
                "임용 도덕·윤리 2026-B Q6 (나) 제시문의 직접 근거 저작."
            ),
            "key_concepts": [
                "창조적 파괴",
                "또 다른 민주주의 이론",
                "경쟁적 엘리트 민주주의",
                "정치적 방법",
                "제도적 장치",
                "고전적 민주주의 비판",
                "자본주의 쇠퇴 예측",
            ],
        },
        {
            "id": "schumpeter-twe-1911",
            "thinker_id": THINKER_ID,
            "title": "경제 발전의 이론",
            "title_original": "Theorie der wirtschaftlichen Entwicklung",
            "year": 1911,
            "significance": (
                "슘페터 초기 동학적 경제이론의 정초 저작 (독일어 1911 / 영역 The Theory of Economic Development 1934). "
                "정태적 균형 이론을 넘어 자본주의의 동태적 발전을 분석하며, "
                "'기업가(entrepreneur)'를 새로운 결합(new combinations)을 실현하는 혁신의 담지자로 규정하였다. "
                "혁신의 5유형 — 신제품·신생산방법·신시장·신원료·신조직 — 으로 자본주의 발전을 설명하며, "
                "신용·이자·이윤을 혁신과 결합한 동학적 분석으로 재구성한다. "
                "후기 『자본주의·사회주의·민주주의(1942)』 창조적 파괴 이론의 토대."
            ),
            "key_concepts": [
                "기업가",
                "새로운 결합",
                "혁신 5유형",
                "신제품",
                "신생산방법",
                "신시장",
                "신원료",
                "신조직",
            ],
        },
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """슘페터 핵심 주장 데이터 입력 (≥6).

    original_text 는 coverage/2026-B.md L337-L400 또는 study-guide/2026-B.md L351-L400
    또는 blocker-log.md L1123-L1129 의 verbatim 인용 + 출처 주석.
    출처 부재 trademark 0건 (fabrication 회피).
    """
    claims = [
        # CLAIM-001: 경쟁적 엘리트 민주주의
        {
            "id": "schumpeter-claim-001",
            "thinker_id": THINKER_ID,
            "work_id": "schumpeter-csd-1942",
            "source_detail": (
                "『자본주의·사회주의·민주주의(Capitalism, Socialism and Democracy, 1942)』 "
                "제22장 '또 다른 민주주의 이론(Another Theory of Democracy)' · "
                "2026학년도 전공B Q6 (나) 제시문"
            ),
            "claim": (
                "민주주의에서 정치인들은 국민의 표(people's vote)를 얻기 위해 "
                "경쟁적으로 투쟁함으로써 결정을 내릴 권력을 획득한다. "
                "민주주의는 정치 엘리트들의 경쟁을 통한 결정 메커니즘이며, "
                "이것이 '경쟁적 엘리트 민주주의(competitive elitist democracy)'의 정식이다."
            ),
            # coverage/2026-B.md L354 verbatim (Q6 (나) 제시문 L113 인용)
            "original_text": (
                "정치인들은 국민의 표를 얻기 위한 경쟁적 수단을 통해 정책을 결정하는 권력을 획득한다 "
                "— 2026학년도 전공B Q6 (나) 제시문 (coverage/2026-B.md L345·L354 · "
                "study-guide/2026-B.md L365). "
                "원문 직역 \"The democratic method is that institutional arrangement for "
                "arriving at political decisions in which individuals acquire the power to "
                "decide by means of a competitive struggle for the people's vote\" "
                "— blocker-log.md L1127 (BLK-175E-2026B-004 trademark ②)"
            ),
            "explanation": (
                "슘페터 『자본주의·사회주의·민주주의』 제22장의 trademark 정식. "
                "고전적 민주주의 이론(루소 일반의지·인민주권)에서는 인민 자체가 정책을 결정한다고 보았으나, "
                "슘페터는 실제 민주주의에서 결정 권력은 경쟁 선거를 통해 선출된 정치 엘리트가 획득한다고 본다. "
                "정치인들의 경쟁은 시장에서 기업가의 경쟁과 유비되며, "
                "국민의 표는 시장의 화폐와 같은 '선택 매개체' 기능을 한다. "
                "이는 달(Robert Dahl) 『Polyarchy, 1971』 등 후대 민주주의 경험 이론의 직접적 원류. "
                "2026-B Q6 (나) ㉢ 정답 = 민주주의(democracy) 직접 근거."
            ),
            "argument": (
                "전제1: 고전적 민주주의 이론(인민자치)은 사실에 부합하지 않는다. "
                "전제2: 실제 민주주의에서 정책 결정 권력을 가진 자는 선거에서 표를 얻은 정치인이다. "
                "전제3: 선거는 정치인들 간의 경쟁적 투쟁으로 작동한다. "
                "결론: 따라서 민주주의는 '국민의 표를 얻기 위한 정치인들의 경쟁적 투쟁을 통해 "
                "결정 권력을 획득하는 제도적 장치'이다."
            ),
            "counterpoint": (
                "루소의 직접민주주의·일반의지론에서는 주권은 양도될 수 없으며 대표될 수도 없다. "
                "슘페터의 '대표자 선출 후에는 대표자에게 정치 활동을 위임'한다는 모형은 "
                "루소가 비판한 '대의제에서 인민은 선거 후 다시 노예가 된다'는 명제와 정면 충돌한다."
            ),
            "context": (
                "2026-B Q6 (나) 사상가 확정의 핵심 trademark · "
                "현대 절차적 민주주의 이론 정초."
            ),
            "keywords": [
                "경쟁적 엘리트 민주주의",
                "정치인 경쟁",
                "국민의 표",
                "competitive struggle",
                "competitive elitist democracy",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-002: 절차적·최소주의 민주주의 — 정치적 방법·제도적 장치
        {
            "id": "schumpeter-claim-002",
            "thinker_id": THINKER_ID,
            "work_id": "schumpeter-csd-1942",
            "source_detail": (
                "『자본주의·사회주의·민주주의(1942)』 제22장 · "
                "2026학년도 전공B Q6 (나) 제시문 첫 문장"
            ),
            "claim": (
                "민주주의는 하나의 정치적 방법(political method)일 뿐 그 자체가 목적이 될 수 없으며, "
                "정치적 결정에 도달하기 위한 제도적 장치(institutional arrangement)이다. "
                "이것이 절차적·최소주의적 민주주의 정식이다."
            ),
            # coverage/2026-B.md L353 verbatim + study-guide L365 verbatim
            "original_text": (
                "( ㉢ )은/는 하나의 정치적 방법일 뿐 그것이 특정한 역사적 조건들 아래서 "
                "어떤 결정을 내리든 상관없이 그 자체가 하나의 목적이 될 수는 없다. "
                "( ㉢ )은/는 정치적 결정에 도달하기 위한 제도적 장치이며 "
                "— 2026학년도 전공B Q6 (나) 제시문 (coverage/2026-B.md L345·L353 · "
                "study-guide/2026-B.md L365). "
                "원문 직역 \"democracy is a political method, that is to say, a certain type of "
                "institutional arrangement for arriving at political—legislative and "
                "administrative—decisions\" "
                "— blocker-log.md L1127 (BLK-175E-2026B-004 trademark ①)"
            ),
            "explanation": (
                "슘페터의 절차적·최소주의 민주주의 정의. "
                "민주주의는 그 자체로 도덕적 가치(인민자치·일반의지 실현)나 결과 가치(공동선 실현)를 갖지 않으며, "
                "단지 '정치 지도자를 선출하고 결정에 도달하기 위한 절차적 방법'으로만 정의된다. "
                "어떤 정책이 결정되든 그 정책의 도덕적·실체적 옳고 그름과 무관하게 "
                "절차(경쟁 선거)가 작동했다면 민주주의가 작동한 것이다. "
                "이는 루소·롤스 등의 실체적 민주주의관과 대립하며, "
                "후대 달·립셋·헌팅턴의 경험적·절차적 민주주의 정의의 원형."
            ),
            "argument": (
                "전제1: 정치체제는 '목적' 또는 '방법'으로 정의될 수 있다. "
                "전제2: 민주주의를 '인민자치·공동선 실현'이라는 목적으로 정의하면 사실에 부합하지 않는다. "
                "전제3: 실제 민주주의에서 작동하는 것은 정치 결정에 도달하는 절차이다. "
                "결론: 따라서 민주주의는 '정치적 결정에 도달하기 위한 제도적 장치(political method)'로 정의되어야 한다."
            ),
            "counterpoint": (
                "롤스 등 실체적 민주주의관에서는 절차만으로는 민주주의의 정의(justice)를 보장할 수 없으며, "
                "기본적 자유·공정한 기회 균등 등 실체적 원리가 결합되어야 한다고 본다. "
                "절차적 민주주의는 '다수의 폭정' 위험에 노출된다는 비판."
            ),
            "context": (
                "2026-B Q6 (나) ㉢ 빈칸 정답 민주주의(democracy)의 직접 근거 · "
                "현대 절차적 민주주의 정의의 정전."
            ),
            "keywords": [
                "정치적 방법",
                "제도적 장치",
                "절차적 민주주의",
                "최소주의 민주주의",
                "political method",
                "institutional arrangement",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-003: 고전적 민주주의 비판 — 3전제 부정
        {
            "id": "schumpeter-claim-003",
            "thinker_id": THINKER_ID,
            "work_id": "schumpeter-csd-1942",
            "source_detail": (
                "『자본주의·사회주의·민주주의(1942)』 제21장 '고전적 민주주의 이론' · "
                "blocker-log.md L1127 (BLK-175E-2026B-004 trademark ③)"
            ),
            "claim": (
                "고전적 민주주의 이론은 ① 공동선(common good)의 존재, "
                "② 공동선을 인식하는 합리적 시민의 존재, ③ 인민 의지의 존재라는 3전제 위에 서 있으나 "
                "모두 사실에 부합하지 않는다. "
                "'인민의 자치(self-government of the people)'는 허구이며, "
                "실제 민주주의는 정치 엘리트 선택을 위한 경쟁 메커니즘이다."
            ),
            # blocker-log.md L1127 verbatim
            "original_text": (
                "고전적 관념(classical doctrine)의 '인민의 자치(self-government of the people)' 비판. "
                "고전적 민주주의 이론은 (a) 공동선(common good)의 존재, "
                "(b) 공동선을 인식하는 합리적 시민의 존재, (c) 인민 의지의 존재를 전제하나 모두 사실과 다름 "
                "— 인민의 자치는 허구이며 실제 민주주의는 지도자(엘리트) 선택을 위한 경쟁 메커니즘 "
                "— blocker-log.md L1127 (BLK-175E-2026B-004 trademark ③)"
            ),
            "explanation": (
                "슘페터 『CSD』 제21장의 핵심 명제. "
                "고전적 민주주의 이론(루소·페인·제퍼슨 계열)은 "
                "(a) 모든 사람이 합의할 수 있는 공동선이 존재하며, "
                "(b) 시민이 합리적 숙고로 그 공동선을 인식할 수 있고, "
                "(c) 그 결과 단일한 '인민 의지(volonté générale)'가 형성된다고 가정한다. "
                "슘페터는 (a) 가치 다원주의 시대에 단일 공동선은 존재하지 않으며, "
                "(b) 실제 시민은 정치적 사안에서 합리적 숙고를 행하지 않고 군중심리에 좌우되며, "
                "(c) '인민 의지'는 정치인·언론·이익집단이 형성한 인공물에 불과하다고 비판한다. "
                "이 3전제 비판이 곧 경쟁적 엘리트 민주주의로의 전환 근거. "
                "2026-B Q6 (나) 사상가 확정의 trademark."
            ),
            "argument": (
                "전제1: 고전적 민주주의 이론은 공동선·합리적 시민·인민 의지 3전제 위에 서 있다. "
                "전제2: 가치 다원주의 시대에 단일 공동선은 존재하지 않는다. "
                "전제3: 실제 시민은 정치적 사안에서 합리성을 발휘하지 않으며, 인민 의지는 인공물이다. "
                "결론: 따라서 고전적 민주주의 이론의 3전제는 모두 부정되며, "
                "민주주의는 '인민 자치'가 아니라 '엘리트 선출 절차'로 재정의되어야 한다."
            ),
            "counterpoint": (
                "루소 옹호자들은 슘페터의 '경험적 시민상' 자체가 자본주의가 만들어낸 왜곡된 시민의 모습이며, "
                "교육과 참여 제도를 통해 시민의 합리적 숙고 능력을 회복할 수 있다고 반박한다. "
                "또한 절차적 민주주의는 '다수의 폭정'을 정당화할 위험이 있다."
            ),
            "context": (
                "고전적 vs 현대적 경쟁 엘리트 민주주의 대립 구도의 핵심 · "
                "2026-B Q6 가(루소)·나(슘페터) 대비 출제."
            ),
            "keywords": [
                "고전적 민주주의 비판",
                "공동선",
                "인민 의지",
                "합리적 시민",
                "self-government of the people",
                "classical doctrine",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-004: 창조적 파괴
        {
            "id": "schumpeter-claim-004",
            "thinker_id": THINKER_ID,
            "work_id": "schumpeter-csd-1942",
            "source_detail": (
                "『자본주의·사회주의·민주주의(1942)』 제2부 제7장 '창조적 파괴의 과정' · "
                "blocker-log.md L1127-L1128"
            ),
            "claim": (
                "자본주의의 본질은 정태적 균형이 아니라 동태적 변동이다. "
                "기업가의 혁신을 통해 낡은 경제 구조가 끊임없이 파괴되고 새로운 구조가 창출되는 "
                "'창조적 파괴(creative destruction)'의 과정이 자본주의 동력의 핵심이다."
            ),
            # blocker-log.md L1128 verbatim
            "original_text": (
                "창조적 파괴(creative destruction) — 혁신에 의한 낡은 구조의 파괴와 "
                "새로운 구조의 창출, 자본주의 역동성의 핵심 "
                "— blocker-log.md L1128 (BLK-175E-2026B-004 후속 조치 trademark)"
            ),
            "explanation": (
                "슘페터 『CSD』 제7장의 trademark 개념. "
                "마르크스가 자본주의를 '모순으로 인한 붕괴'로 진단한 것과 달리, "
                "슘페터는 자본주의를 '내재적 혁신을 통한 끊임없는 자기 갱신' 과정으로 본다. "
                "철도가 마차 산업을 파괴하고, 자동차가 철도를 부분 대체하며, 컴퓨터가 타자기를 도태시키듯, "
                "기업가의 혁신은 기존 산업·기업·노동 형태를 '창조적으로 파괴'하면서 새로운 구조를 창출한다. "
                "이는 정태 균형 이론(왈라스·마셜 등)이 포착하지 못하는 자본주의의 동학이며, "
                "현대 경영학·기업가 이론·기술혁신 정책의 고전적 토대가 되었다."
            ),
            "argument": (
                "전제1: 자본주의는 정태적 균형이 아니라 동태적 변동 시스템이다. "
                "전제2: 동태적 변동의 동력은 기업가의 혁신이다. "
                "전제3: 혁신은 기존 구조의 파괴와 새 구조의 창출을 동시에 수반한다. "
                "결론: 따라서 자본주의의 본질은 '창조적 파괴'의 과정이다."
            ),
            "counterpoint": (
                "마르크스주의자들은 창조적 파괴 과정에서 발생하는 노동자 실업·사회적 비용을 "
                "슘페터가 과소평가한다고 비판한다. "
                "또한 거대 기업의 독점화로 혁신 동기가 오히려 약화될 수 있다는 지적."
            ),
            "context": (
                "20세기 경제학·경영학의 고전 개념 · "
                "혁신 이론·기업가 이론의 정전."
            ),
            "keywords": [
                "창조적 파괴",
                "creative destruction",
                "혁신",
                "자본주의 동학",
                "기업가",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-005: 기업가 이론·혁신 5유형
        {
            "id": "schumpeter-claim-005",
            "thinker_id": THINKER_ID,
            "work_id": "schumpeter-twe-1911",
            "source_detail": (
                "『경제 발전의 이론(Theorie der wirtschaftlichen Entwicklung, 1911)』 · "
                "blocker-log.md L1128 (BLK-175E-2026B-004 후속 조치 trademark)"
            ),
            "claim": (
                "기업가(entrepreneur)는 '새로운 결합(new combinations)'을 실현하는 혁신의 담지자이며, "
                "혁신은 ① 신제품, ② 신생산방법, ③ 신시장, ④ 신원료, ⑤ 신조직의 5유형으로 구성된다. "
                "기업가는 단순한 자본가나 경영자가 아니라, 새로운 결합을 시도하는 위험 감수자이다."
            ),
            # blocker-log.md L1128 verbatim
            "original_text": (
                "기업가(entrepreneur) 이론 — 혁신의 담지자, 새로운 결합(new combinations) 실현자. "
                "혁신(innovation) 5유형 — 신제품·신생산방법·신시장·신원료·신조직 "
                "— blocker-log.md L1128 (BLK-175E-2026B-004 후속 조치 trademark)"
            ),
            "explanation": (
                "슘페터 『경제 발전의 이론(1911)』의 핵심 정식. "
                "혁신의 5유형은 다음과 같다: "
                "① 신제품 — 새로운 재화의 도입; "
                "② 신생산방법 — 새로운 생산 방법·기술 도입; "
                "③ 신시장 — 새로운 시장의 개척; "
                "④ 신원료 — 새로운 원료·반제품 공급원의 획득; "
                "⑤ 신조직 — 새로운 산업조직의 실현(예: 독점적 지위 창출 또는 해체). "
                "기업가는 이 5유형의 새로운 결합을 시도하여 경제 균형을 교란하고 "
                "동학적 발전을 추동하는 행위자이며, "
                "단순한 자본 소유자(자본가)나 일상 경영자(매니저)와 구별된다. "
                "20세기 후반 드러커·크리스텐슨 등 경영학자들은 "
                "이 슘페터적 기업가 개념을 현대 혁신 이론의 출발점으로 삼았다."
            ),
            "argument": (
                "전제1: 자본주의 동학의 동력은 혁신이다. "
                "전제2: 혁신은 5유형의 '새로운 결합'으로 분류된다. "
                "전제3: 이 새로운 결합을 실현하는 행위자는 자본가도 매니저도 아닌 별도의 인물이다. "
                "결론: 따라서 자본주의에는 '기업가(entrepreneur)'라는 고유한 경제 행위자가 존재하며, "
                "그는 새로운 결합을 시도하는 혁신의 담지자이다."
            ),
            "counterpoint": (
                "후대 혁신 이론은 슘페터의 '영웅적 개인 기업가' 모형이 "
                "현대 거대 기업의 R&D 부서·집단적 혁신 과정을 설명하지 못한다고 비판한다. "
                "이를 반영하여 슘페터 자신도 후기에 'Mark II 모형'(거대 기업의 일상화된 혁신)으로 수정하였다."
            ),
            "context": (
                "혁신 이론·기업가 정신·창조적 파괴의 메커니즘 분석 · "
                "현대 경영학 혁신 이론의 토대."
            ),
            "keywords": [
                "기업가",
                "entrepreneur",
                "새로운 결합",
                "new combinations",
                "혁신 5유형",
                "신제품",
                "신생산방법",
                "신시장",
                "신원료",
                "신조직",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-006: 자본주의 필연적 쇠퇴 예측
        {
            "id": "schumpeter-claim-006",
            "thinker_id": THINKER_ID,
            "work_id": "schumpeter-csd-1942",
            "source_detail": (
                "『자본주의·사회주의·민주주의(1942)』 제2부 (자본주의는 살아남을 수 있는가?) · "
                "blocker-log.md L1128 (BLK-175E-2026B-004 후속 조치 trademark)"
            ),
            "claim": (
                "자본주의는 그 자신의 성공으로 인해 필연적으로 쇠퇴한다. "
                "합리화·관료화로 기업가 정신이 소멸하고, 지식인 계층의 자본주의 비판이 강화되며, "
                "사회 구조의 변화로 자본주의의 사회적 기반이 잠식되어 사회주의로의 이행이 불가피하다."
            ),
            # blocker-log.md L1128 verbatim
            "original_text": (
                "자본주의의 필연적 쇠퇴 예측 — 합리화·관료화로 기업가 정신 소멸, "
                "지식인 계층의 자본주의 비판, 사회주의로의 이행 "
                "— blocker-log.md L1128 (BLK-175E-2026B-004 후속 조치 trademark)"
            ),
            "explanation": (
                "슘페터 『CSD』 제2부의 역설적 진단. "
                "마르크스가 '자본주의 모순(이윤율 저하·과잉생산·계급투쟁)으로 인한 붕괴'를 예언한 것과 달리, "
                "슘페터는 '자본주의의 성공이 그 자신의 토대를 잠식한다'는 정반대의 논리로 쇠퇴를 예언한다. "
                "구체적 메커니즘: "
                "(a) 거대 기업의 R&D 부서가 혁신을 일상화·관료화하여 "
                "기업가 정신이 소멸한다; "
                "(b) 자본주의 발전이 만들어낸 지식인 계층이 "
                "자본주의 가치를 비판하며 반자본주의 분위기를 형성한다; "
                "(c) 가족 구조 해체·기업 소유 분산 등 사회 구조 변화로 "
                "자본주의의 사회·문화적 기반이 약화된다. "
                "결과로 사회주의로의 이행이 불가피하나, "
                "슘페터는 이를 반드시 환영하지 않으며 사회주의가 민주주의와 양립 가능한지 신중히 검토한다 "
                "(『CSD』 제3부·제4부)."
            ),
            "argument": (
                "전제1: 자본주의 동력의 핵심은 기업가 정신과 사회·문화적 기반이다. "
                "전제2: 자본주의의 성공이 거대 기업·관료화·지식인 비판·가족 해체를 낳는다. "
                "전제3: 이 변화는 기업가 정신과 사회·문화적 기반을 잠식한다. "
                "결론: 따라서 자본주의는 그 자신의 성공으로 인해 필연적으로 쇠퇴하며, "
                "사회주의로의 이행이 불가피하다."
            ),
            "counterpoint": (
                "슘페터의 쇠퇴 예언은 1980년대 신자유주의·1990년대 IT 혁명을 거치며 부분적으로 반박되었다. "
                "거대 기업 내부의 R&D 부서·스타트업 생태계 등 새로운 혁신 메커니즘이 등장하여 "
                "기업가 정신은 다른 형태로 지속되고 있다는 평가."
            ),
            "context": (
                "20세기 자본주의·사회주의 비교 이론의 정전 · "
                "마르크스 모순 붕괴론과 대비되는 '성공 인한 쇠퇴' 명제."
            ),
            "keywords": [
                "자본주의 쇠퇴 예측",
                "기업가 정신 소멸",
                "관료화",
                "지식인 계층",
                "사회주의 이행",
            ],
            "verified": False,
            "verification_log": [],
        },
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """슘페터 핵심 키워드 데이터 입력. 중복 체크 후 insert."""
    keywords = [
        {
            "id": "kw-schumpeter-competitive-elitist-democracy",
            "term": "경쟁적 엘리트 민주주의",
            "term_en": "competitive elitist democracy",
            "definition": (
                "슘페터 『자본주의·사회주의·민주주의(1942)』 제22장 trademark. "
                "민주주의에서 정치인들이 국민의 표(people's vote)를 얻기 위해 "
                "경쟁적으로 투쟁함으로써 정책 결정 권력을 획득하는 절차로 민주주의를 정의. "
                "고전적 민주주의 이론(인민자치·일반의지)을 비판하고, "
                "민주주의를 '엘리트 선출의 경쟁 메커니즘'으로 재정의. "
                "후대 달(Robert Dahl) 『Polyarchy, 1971』 등 경험적 민주주의 이론의 원류. "
                "2026-B Q6 (나) 사상가 확정의 trademark."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "schumpeter-csd-1942",
            "related_terms": [
                "절차적 민주주의",
                "최소주의 민주주의",
                "정치적 방법",
                "제도적 장치",
                "고전적 민주주의 비판",
            ],
        },
        {
            "id": "kw-schumpeter-political-method",
            "term": "정치적 방법 / 제도적 장치",
            "term_en": "political method / institutional arrangement",
            "definition": (
                "슘페터의 절차적·최소주의 민주주의 정의. "
                "원문: \"democracy is a political method, that is to say, a certain type of "
                "institutional arrangement for arriving at political—legislative and "
                "administrative—decisions\". "
                "민주주의는 그 자체로 도덕적·실체적 가치(인민자치·공동선)가 아니라 "
                "단지 '정치적 결정에 도달하기 위한 절차'로 정의된다. "
                "어떤 정책이 결정되든 그 정책의 실체적 옳고 그름과 무관하게 "
                "절차(경쟁 선거)가 작동했다면 민주주의가 작동한 것."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "schumpeter-csd-1942",
            "related_terms": [
                "경쟁적 엘리트 민주주의",
                "절차적 민주주의",
                "최소주의 민주주의",
                "고전적 민주주의 비판",
            ],
        },
        {
            "id": "kw-schumpeter-classical-doctrine-critique",
            "term": "고전적 민주주의 비판",
            "term_en": "critique of the classical doctrine of democracy",
            "definition": (
                "슘페터 『CSD』 제21장의 trademark. "
                "고전적 민주주의 이론(루소·페인·제퍼슨 계열)의 3전제 — "
                "① 공동선(common good)의 존재, "
                "② 공동선을 인식하는 합리적 시민의 존재, "
                "③ 인민 의지(volonté générale)의 존재 — 가 모두 사실에 부합하지 않는다고 비판. "
                "'인민의 자치(self-government of the people)'는 허구이며, "
                "'인민 의지'는 정치인·언론·이익집단이 형성한 인공물이라는 것이 슘페터의 진단."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "schumpeter-csd-1942",
            "related_terms": [
                "공동선",
                "인민 의지",
                "합리적 시민",
                "self-government of the people",
                "경쟁적 엘리트 민주주의",
            ],
        },
        {
            "id": "kw-schumpeter-creative-destruction",
            "term": "창조적 파괴",
            "term_en": "creative destruction",
            "definition": (
                "슘페터 『CSD』 제2부 제7장 trademark. "
                "자본주의의 본질은 정태적 균형이 아니라 동태적 변동이며, "
                "기업가의 혁신을 통해 낡은 경제 구조가 끊임없이 파괴되고 새로운 구조가 창출되는 "
                "과정이 자본주의 동력의 핵심이라는 정식. "
                "마르크스의 '자본주의 모순으로 인한 붕괴'와 달리 "
                "'자본주의의 자기 갱신·자기 파괴를 통한 발전'을 강조. "
                "현대 경영학·기업가 이론·기술혁신 정책의 고전적 토대."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "schumpeter-csd-1942",
            "related_terms": [
                "혁신",
                "기업가",
                "자본주의 동학",
                "새로운 결합",
            ],
        },
        {
            "id": "kw-schumpeter-entrepreneur",
            "term": "기업가 / 새로운 결합",
            "term_en": "entrepreneur / new combinations",
            "definition": (
                "슘페터 『경제 발전의 이론(1911)』 trademark. "
                "기업가(entrepreneur)는 '새로운 결합(new combinations)'을 실현하는 혁신의 담지자. "
                "혁신은 5유형으로 구성된다: ① 신제품, ② 신생산방법, ③ 신시장, ④ 신원료, ⑤ 신조직. "
                "기업가는 단순한 자본가(자본 소유자)나 매니저(일상 경영자)와 구별되며, "
                "새로운 결합을 시도하는 위험 감수자이다."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "schumpeter-twe-1911",
            "related_terms": [
                "혁신",
                "혁신 5유형",
                "창조적 파괴",
                "신제품",
                "신생산방법",
                "신시장",
            ],
        },
        {
            "id": "kw-schumpeter-capitalism-decline",
            "term": "자본주의 쇠퇴 예측",
            "term_en": "prediction of capitalist decline",
            "definition": (
                "슘페터 『CSD』 제2부 trademark. "
                "자본주의는 그 자신의 성공으로 인해 필연적으로 쇠퇴한다는 역설적 진단. "
                "메커니즘: ① 거대 기업의 R&D 부서가 혁신을 관료화하여 기업가 정신 소멸; "
                "② 자본주의가 만들어낸 지식인 계층의 자본주의 비판; "
                "③ 가족 해체·기업 소유 분산 등 사회·문화적 기반 약화. "
                "마르크스의 '모순으로 인한 붕괴'와 달리 '성공으로 인한 쇠퇴'를 예언."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "schumpeter-csd-1942",
            "related_terms": [
                "관료화",
                "기업가 정신 소멸",
                "지식인 계층",
                "사회주의 이행",
            ],
        },
    ]

    inserted = 0
    for kw in keywords:
        try:
            client.get(index=INDEX_KEYWORDS, id=kw["id"])
            print(f"[keyword] {kw['id']}: 이미 존재 (skip)")
        except Exception:
            result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
            print(f"[keyword] {kw['id']}: {result['result']}")
            inserted += 1

    return len(keywords)


def insert_relations(client):
    """슘페터 영향·비교 관계 데이터 입력.

    ES 등록 확인된 thinker_id 만 링크 (2026-04-28 curl 확인):
    - rousseau : 등록 (era=계몽주의, 1712-1778) — 고전 vs 경쟁적 엘리트 민주주의 대비
                 (2026-B Q6 가·나 정전 대립 구도)
    - mill_js  : 등록 (era=현대, 1806-1873) — 자유주의 대표·민주주의 옹호자와의 대조
    """
    relations = [
        {
            "from_thinker": THINKER_ID,
            "to_thinker": "rousseau",
            "type": "compared",
            "description": (
                "슘페터(1883-1950)와 루소(1712-1778)의 민주주의관 대비는 "
                "현대·고전 민주주의 이론 대립의 정전 구도이다. "
                "루소의 고전적 민주주의는 인민자치·일반의지·주권 불가양을 핵심으로 하여 "
                "'민주주의 = 인민이 직접 정책을 결정하는 정치체제'로 정의한다. "
                "슘페터는 이 고전적 정의를 비판하고 "
                "'민주주의 = 정치인이 국민의 표를 얻기 위해 경쟁하는 제도적 장치'로 재정의 "
                "(경쟁적 엘리트 민주주의). "
                "루소의 직접민주주의·대의제 비판('영국 인민은 의회 의원을 선출하는 동안만 자유롭다')과 "
                "슘페터의 대표제 옹호('국민이 일단 대표자를 선출하고 나면 그 이후 정치 활동은 대표자의 일')는 "
                "정반대 극을 이룬다. 2026-B Q6 (가)·(나)는 이 정전 대립 구도의 직접 출제."
            ),
            "evidence": (
                "coverage/2026-B.md L355 — "
                "'국민이 일단 대표자를 선출하고 나면 그 이후의 정치 활동은 대표자의 일이다 "
                "— 슘페터 최소주의적·절차적 민주주의 정식. "
                "이는 루소의 참여 민주주의·대의제 비판과 정반대 구도'; "
                "study-guide/2026-B.md L391 — "
                "'2026-B Q6 가·나 대립 구도는 고전적(루소) vs 현대적 경쟁적 엘리트(슘페터) "
                "민주주의관의 교과서적 대비'"
            ),
        },
        {
            "from_thinker": THINKER_ID,
            "to_thinker": "mill_js",
            "type": "compared",
            "description": (
                "슘페터(1883-1950)와 밀(John Stuart Mill, 1806-1873)의 민주주의관은 "
                "절차적·최소주의 vs 도덕적·발전적 민주주의의 대비를 이룬다. "
                "밀은 『대의정부론』(1861)에서 "
                "민주주의를 '시민의 도덕적·지적 발전을 촉진하는 정치체제'로 정의하고, "
                "정치 참여 자체가 시민을 성장시키는 교육적 가치를 갖는다고 보았다 "
                "(발전적 민주주의관). "
                "슘페터는 이러한 도덕적·실체적 민주주의관을 '고전적 이론'으로 분류하여 비판하고, "
                "민주주의를 '정치적 결정에 도달하기 위한 절차'로만 정의 — "
                "민주주의 자체에 도덕적 가치를 부여하지 않는다."
            ),
            "evidence": (
                "blocker-log.md L1127-L1128 — "
                "'슘페터 민주주의 = 정치적 방법(political method) / 제도적 장치(institutional arrangement) "
                "— 고전적 민주주의 이론(공동선·인민의지·합리적 시민 3전제)을 사실에 맞지 않는다고 비판'; "
                "study-guide/2026-B.md L391 — "
                "'슘페터 절차적 민주주의는 민주주의를 정치적 방법으로만 정의하여 "
                "도덕적·실체적 가치를 박탈 — 밀·롤스 등 도덕적 민주주의관과 대립'"
            ),
        },
    ]

    for i, rel in enumerate(relations):
        rel_id = f"rel-{rel['from_thinker']}-{rel['to_thinker']}-{rel['type']}-{i+1}"
        result = client.index(index=INDEX_RELATIONS, id=rel_id, document=rel)
        print(f"[relation] {rel_id}: {result['result']}")

    return len(relations)


def main():
    """메인 실행 함수."""
    print("=== 조지프 슘페터(Joseph Alois Schumpeter) 데이터 ES 입력 시작 ===\n")
    client = get_client()

    try:
        print("1. 분야(field) 확인/추가")
        try:
            ensure_field(client)
        except Exception as e:
            print(f"[ensure_field] 경고: {e}", file=sys.stderr)
        print()

        print("2. 사상가(thinker) 입력")
        try:
            insert_thinker(client)
        except Exception as e:
            print(f"[insert_thinker] 오류: {e}", file=sys.stderr)
            raise
        print()

        print("3. 저서(works) 입력")
        try:
            work_count = insert_works(client)
            print(f"   -> {work_count}개 저서 입력 완료\n")
        except Exception as e:
            print(f"[insert_works] 오류: {e}", file=sys.stderr)
            raise

        print("4. 주장(claims) 입력")
        try:
            claim_count = insert_claims(client)
            print(f"   -> {claim_count}개 주장 입력 완료\n")
        except Exception as e:
            print(f"[insert_claims] 오류: {e}", file=sys.stderr)
            raise

        print("5. 키워드(keywords) 입력")
        try:
            kw_count = insert_keywords(client)
            print(f"   -> {kw_count}개 키워드 처리 완료\n")
        except Exception as e:
            print(f"[insert_keywords] 오류: {e}", file=sys.stderr)
            raise

        print("6. 관계(relations) 입력")
        try:
            rel_count = insert_relations(client)
            print(f"   -> {rel_count}개 관계 입력 완료\n")
        except Exception as e:
            print(f"[insert_relations] 오류: {e}", file=sys.stderr)
            raise

        print("=== 입력 요약 ===")
        print(f"  사상가: 1명 (schumpeter)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n[OK] 조지프 슘페터 데이터 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}", file=sys.stderr)
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
