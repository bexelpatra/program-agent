"""남명 조식(南冥 曺植, Cho Sik) 데이터를 ES에 직접 입력하는 스크립트.

Task: TASK-212-01
공식 출제: 2026-A Q3 (BLK-175E-2026A-001 · row 기준 최초 등장).
조선 중기 영남학파 대표 성리학자 (1501-1572) · 퇴계 이황(yihwang, 1501-1570) 동시대인.

eastern_ethics 분야. yihwang/yiyulgok 등 한국 성리학자 동일 field 등록 패턴 답습.
era=`조선` (yihwang·yiyulgok ES 실측 동일 표기 — jeongyagyong 은 `조선 후기`).

원문 인용 규칙(agents/coder.md §원문/입력 인용 규칙) 엄수:
 - claims.original_text 는 coverage md 실측 원문(verbatim) + 출처 주석.
 - 모든 한자·영어 trademark 는 coverage md / blocker-log 출처 확증된 토큰만 사용.
 - 출처 부재 trademark 0개 (사단칠정논쟁 거리두기 등 fabrication 후보 제거).

자기검증 3-step (cho_sik 토큰 ∩=0 확증, coder report 적재):
 - Step 1 — bare-paren `\([A-Za-z][^)]*\)` (TitleCase 한자 래퍼만 — 0-hit 위반 토큰 없음)
 - Step 1b — Greek `[Α-Ωα-ω]` / macron `[\u0100-\u024F]` (0건 — 한국 성리학 비대상)
 - Step 2 — TitleCase `[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}` (Cho Sik / South Korea 등)
 - disjoint 검증: Step1 ∩ Step1b ∩ Step2 = 0

참조 출처 (verbatim only):
 - `projects/ethics-study/exam-solutions/coverage/2026-A.md` L100-L141
 - `projects/ethics-study/exam-solutions/study-guide/2026-A.md` L155-L177
 - `signal/ethics-study/blocker-log.md` L1074-L1080
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


THINKER_ID = "cho_sik"


def ensure_field(client):
    """eastern_ethics 분야 존재 확인 (yihwang/yiyulgok 등 기존 한국 성리학자 등록 확인됨)."""
    try:
        client.get(index=INDEX_FIELDS, id="eastern_ethics")
        print("[field] eastern_ethics: 이미 존재")
    except Exception:
        doc = {
            "id": "eastern_ethics",
            "name": "동양윤리",
            "description": (
                "동양 철학 전통에서 발전한 윤리 사상 분야. "
                "유가·도가·묵가·법가 등 중국 제자백가, "
                "한국 성리학(퇴계·율곡·남명 등), 신유학, "
                "한국·중국·일본 불교(천태·화엄·선종 등)를 포괄한다. "
                "임용 도덕·윤리 시험의 동양 윤리 사상 영역 대응."
            ),
            "order": 1,
        }
        result = client.index(index=INDEX_FIELDS, id="eastern_ethics", document=doc)
        print(f"[field] eastern_ethics: {result['result']}")


def insert_thinker(client):
    """남명 조식 사상가 데이터 입력."""
    doc = {
        "id": THINKER_ID,
        "name": "남명 조식 (南冥 曺植)",
        "name_en": "Cho Sik",
        "field": "eastern_ethics",
        "era": "조선",
        "birth_year": 1501,
        "death_year": 1572,
        "background": (
            "조선 중기 성리학자(1501-1572). 호 남명(南冥), 자 건중(楗仲). "
            "경상우도 합천 출신으로, 퇴계 이황(1501-1570)과 동시대를 살며 "
            "조선 중기 영남 사림(嶺南士林)의 양대 산맥을 이루었다. "
            "여러 차례 관직(전생서 주부·단성현감·상서원 판관·종친부 전첨 등)을 사양하고 "
            "재야에서 학문과 수양에 전념한 산림처사(山林處士)의 표상이다. "
            "수양처로 산천재(山天齋, 지리산 자락)·뇌룡정을 두고 "
            "경(敬)과 의(義)를 두 글자로 삼아 평생의 좌우명으로 새겼으며, "
            "패검(佩劍)에 '내명자경 외단자의(內明者敬 外斷者義)' 16자를 새겨 일상 실천 원리로 삼았다. "
            "임진왜란 시 곽재우·정인홍·김면 등 의병장 다수가 남명 문하에서 배출되어 "
            "남명 학문의 실천 지향성이 역사적 결실로 입증되었다. "
            "임용 도덕·윤리 시험에서 2026-A Q3에 row 기준 최초 출제 (BLK-175E-2026A-001 해소 대상)."
        ),
        "core_philosophy": (
            "남명 조식 학문의 핵심은 '경의(敬義) 병립(竝立)'이다. "
            "경(敬)은 안을 밝히는 내면 수양(主敬)으로 마음을 한 곳에 집중하여 또렷이 깨어 있게 하고, "
            "의(義)는 밖으로 결단하는 외면 실천(行義)으로 시비(是非)·선악(善惡)을 가려 옳음을 택하는 실천력이다. "
            "남명은 이 두 글자를 '하늘의 해와 달'에 비유하여 분리될 수 없는 수양의 양륜(兩輪)으로 규정하였다. "
            "패검명(佩劍銘) '내명자경 외단자의(內明者敬 外斷者義 — 안을 밝히는 것은 경이고 밖으로 결단하는 것은 의이다)'는 "
            "『주역(周易)』 곤괘(坤卦) 문언전 '경이직내 의이방외(敬以直內 義以方外)'를 받아 "
            "자기 수양의 안팎 이원 구조를 압축한 남명 trademark이다. "
            "퇴계 이황의 거경궁리(居敬窮理 — 경에 머무르며 이치를 궁구함) 체계가 "
            "경(敬)과 궁리(窮理)의 짝으로 정좌·궁구를 강조한 데 비해, "
            "남명의 경의 병립은 경과 의의 짝으로 일상 실천·외향 결단을 강조한다. "
            "이 점에서 남명은 퇴계와 출처관(出處觀)에서도 대비된다 — "
            "퇴계가 출사(出仕)를 신중히 수용한 데 반해 남명은 처사(處士)로 재야를 철저히 견지하였다. "
            "학문 단계로는 소학(小學)에 근거한 실천을 먼저 익히고, "
            "이후 근사록(近思錄)을 보고 곁에 성리대전(性理大全)을 두고 1~2년 탐구하라고 가르쳤다."
        ),
        "philosophical_journey": (
            "남명은 1501년 경남 합천에서 태어나 어려서 부친을 여의고 외가에서 자랐다. "
            "초년에는 과거 시험을 준비하다가 30세 무렵 위기지학(爲己之學)으로 방향을 전환하여 "
            "성리학 본령에 매진하였다. 여러 차례 관직 천거를 받았으나 모두 사양하고, "
            "지리산 자락 산천재(山天齋)·뇌룡정에 은거하여 강학과 수양을 이어갔다. "
            "1555년(명종 10) 단성현감(丹城縣監) 사직소(辭職疏)에서 명종의 모친 문정왕후를 "
            "'한 과부(寡婦)'로 지칭하는 파격적 직언을 올린 일은 조선 유학사 상소문의 정점으로 평가된다. "
            "남명은 일상에서 성성자(惺惺子, 방울)를 허리에 차고 다니며 방울 소리로 마음의 흐트러짐을 각성시켰고, "
            "패검(佩劍)에 새긴 '내명자경 외단자의' 8자를 평생의 좌우명으로 삼았다. "
            "저서로 『남명집(南冥集)』과 『학기유편(學記類編)』을 남겼다. "
            "『남명집』은 시문·서간·잡저를 집성한 문집이고, "
            "『학기유편』은 경·의 수양론을 체계적으로 정리한 학문 기록이다. "
            "사후 그의 문하에서 곽재우·정인홍·김면 등이 임진왜란기 의병장으로 활약하여 "
            "남명 학문의 실천성을 역사적으로 입증하였다. "
            "남명은 퇴계 이황(영남좌도)·율곡 이이(기호)와 더불어 조선 성리학 3대 축의 한 자리를 차지한다."
        ),
        "keywords": [
            "경의 병립",
            "경의 쌍수",
            "내명자경 외단자의",
            "패검명",
            "산림처사",
            "출처관 대비",
            "거경궁리 대조",
            "학문 단계론",
            "산천재",
            "뇌룡정",
            "남명집",
            "학기유편",
        ],
    }
    result = client.index(index=INDEX_THINKERS, id=THINKER_ID, document=doc)
    print(f"[thinker] {THINKER_ID}: {result['result']}")
    return result


def insert_works(client):
    """남명 조식 주요 저서 데이터 입력."""
    works = [
        {
            "id": "cho_sik-nammyeongjip",
            "thinker_id": THINKER_ID,
            "title": "남명집",
            "title_original": "南冥集",
            "year": None,
            "significance": (
                "남명 조식의 시문·서간·잡저를 집성한 문집. "
                "「좌우명(座右銘)」·「패검명(佩劍銘)」 등 "
                "경의(敬義) 병립 수양론을 압축한 명문(銘文)들과, "
                "단성현감 사직소(丹城縣監 辭職疏, 1555) 등 "
                "조선 유학사 상소문의 정점으로 평가되는 직언 글을 포함한다. "
                "임용 도덕·윤리 2026-A Q3 제시문 '경(敬)과 의(義) 두 글자가 해와 달과 같다'· "
                "'안을 밝히는 것은 경이고 밖으로 결단하는 것은 의이다'· "
                "'소학에 근거한 실천 이후에는 근사록을 보아야 한다' 구절의 직접 근거 저작."
            ),
            "key_concepts": [
                "경의 병립",
                "내명자경 외단자의",
                "좌우명",
                "패검명",
                "단성현감 사직소",
                "산림처사",
            ],
        },
        {
            "id": "cho_sik-hakgiyupyeon",
            "thinker_id": THINKER_ID,
            "title": "학기유편",
            "title_original": "學記類編",
            "year": None,
            "significance": (
                "남명 조식이 경(敬)·의(義) 수양론을 체계적으로 정리한 학문 기록. "
                "성리학 핵심 개념을 항목별로 정선·편집한 학습용 저작으로, "
                "남명의 학문 단계론(소학→근사록→성리대전)과 경의 병립 수양론을 "
                "체계화한 핵심 저서이다. "
                "blocker-log L1078 명시 — '학기유편(學記類編) — 경·의 수양론의 체계적 정리'."
            ),
            "key_concepts": [
                "경의 수양론 체계화",
                "학문 단계론",
                "성리학 항목 정선",
                "남명 학문의 강령",
            ],
        },
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """남명 조식 핵심 주장 데이터 입력.

    original_text 는 coverage/2026-A.md L100-L141 또는 study-guide/2026-A.md L155-L177
    또는 blocker-log.md L1074-L1080 의 verbatim 인용 + 출처 주석.
    출처 부재 trademark 0건 (fabrication 회피).
    """
    claims = [
        # CLAIM-001: 경의(敬義) 병립 — 경과 의가 해와 달
        {
            "id": "cho_sik-claim-001",
            "thinker_id": THINKER_ID,
            "work_id": "cho_sik-nammyeongjip",
            "source_detail": (
                "『남명집(南冥集)』 「좌우명(座右銘)」 · "
                "2026학년도 전공A Q3 제시문 첫 단락"
            ),
            "claim": (
                "경(敬)과 의(義)를 같이 가지면 그것을 아무리 쓰더라도 다함이 없다. "
                "이 두 글자가 집안에 있는 것은 마치 하늘에 해와 달이 있는 것과 같아서 "
                "만고에 걸쳐 바뀌지 않을 것이다. "
                "성현의 천 가지 만 가지 말씀도 그 요체와 귀착이 이 뜻에서 벗어나지 않는다."
            ),
            # coverage/2026-A.md L106 verbatim (Q3 제시문 L48 인용)
            "original_text": (
                "경(敬)과 ( ㉠ )을/를 같이 가지면, 그것을 아무리 쓰더라도 다함이 없다. "
                "나의 집에 이 두 글자가 있는 것은 마치 하늘에 해와 달이 있는 것과 같아서 "
                "만고에 걸쳐 바뀌지 않을 것이다. 성현의 천 가지 만 가지 말씀도 "
                "그 요체와 귀착이 이 뜻에서 벗어나지 않는다 "
                "— 2026학년도 전공A Q3 제시문 (coverage/2026-A.md L106 · "
                "study-guide/2026-A.md L148)"
            ),
            "explanation": (
                "남명 조식 학문의 trademark인 '경의(敬義) 병립(竝立)' 정식. "
                "경(敬)은 안을 밝히는 내면 수양(主敬), 의(義)는 밖으로 결단하는 외면 실천(行義)으로, "
                "남명은 이 두 글자를 '하늘의 해와 달'에 비유하여 "
                "분리될 수 없는 수양의 양륜(兩輪)으로 규정하였다. "
                "수양처(산천재·뇌룡정)의 벽에 두 글자를 걸어두고 평생의 좌우명으로 삼은 일화가 "
                "조식 『남명집』 「좌우명」 및 제자 오건·정인홍·김우옹 등이 전한 trademark. "
                "2026-A Q3 ㉠ 정답 = 의(義 — righteousness)."
            ),
            "argument": (
                "전제1: 자기 수양은 안의 명료함과 밖의 결단을 모두 요구한다. "
                "전제2: 경(敬)은 안의 명료함을, 의(義)는 밖의 결단을 담당한다. "
                "전제3: 두 가지가 짝을 이루어야 수양이 다함이 없다. "
                "결론: 따라서 경과 의는 해와 달처럼 분리될 수 없는 수양의 양륜이다."
            ),
            "counterpoint": (
                "퇴계 이황의 거경궁리(居敬窮理) 체계는 경(敬)과 궁리(窮理)의 짝으로 "
                "정좌(靜坐)·이치 탐구를 강조하는데, 남명의 경의 병립과는 짝의 구성이 다르다. "
                "퇴계 측에서는 의(義) 자체보다 이(理)를 궁구하는 인식적 측면을 더 중시한다고 볼 수 있다."
            ),
            "context": (
                "2026-A Q3 ㉠ 빈칸 정답의 직접 근거 · "
                "남명 학문의 trademark 정식 (경의 병립)."
            ),
            "keywords": [
                "경의 병립",
                "경",
                "의",
                "해와 달 비유",
                "좌우명",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-002: 패검명(佩劍銘) "內明者敬 外斷者義"
        {
            "id": "cho_sik-claim-002",
            "thinker_id": THINKER_ID,
            "work_id": "cho_sik-nammyeongjip",
            "source_detail": (
                "『남명집(南冥集)』 「패검명(佩劍銘)」 · "
                "2026학년도 전공A Q3 제시문 둘째 단락"
            ),
            "claim": (
                "안을 밝히는 것은 경(敬)이고, 밖으로 결단하는 것은 의(義)이다. "
                "이 8자(內明者敬 外斷者義)를 패검(佩劍)에 새겨 평생 차고 다니며 "
                "일상의 실천 원리로 삼았다."
            ),
            # coverage/2026-A.md L107 verbatim (Q3 제시문 L50)
            "original_text": (
                "안을 밝히는 것은 경이고, 밖으로 결단하는 것은 ( ㉠ )(이)다 "
                "— 2026학년도 전공A Q3 제시문 (coverage/2026-A.md L107 · "
                "study-guide/2026-A.md L150). "
                "패검명 원문 \"內明者敬 外斷者義\" "
                "— blocker-log.md L1078 (BLK-175E-2026A-001 trademark 3중 일치)"
            ),
            "explanation": (
                "남명 조식이 평생 차고 다닌 패검(佩劍)에 새긴 16자 명문(銘文) 중 핵심 8자. "
                "원출전은 『주역(周易)』 곤괘(坤卦) 문언전의 "
                "'군자경이직내 의이방외(君子敬以直內 義以方外 — 군자는 경으로 안을 곧게 하고 의로 밖을 반듯하게 한다)' 구절이며, "
                "남명은 이를 자기 수양의 안팎 이원 구조(內明者敬·外斷者義)로 확정하고 "
                "패검 명문으로 새겨 일생의 실천 원리로 삼은 것이 trademark. "
                "퇴계·율곡 등 다른 조선 성리학자들도 경(敬)은 중시했으나, "
                "경과 의를 한 쌍으로 묶어 패검 명문에 새겨 내외 이분으로 수양을 정식화한 것은 "
                "조식의 고유 체계."
            ),
            "argument": (
                "전제1: 수양은 추상 원리만으로는 일상에 정착하지 않는다. "
                "전제2: 일상의 도구(검·방울)에 좌우명을 새기면 매 순간 수양이 환기된다. "
                "전제3: 패검에 '내명자경 외단자의'를 새기는 것은 "
                "안의 경·밖의 의를 한 몸에 결합하는 실천 장치이다. "
                "결론: 따라서 패검명은 경의 병립을 일상화하는 남명 수양론의 trademark이다."
            ),
            "counterpoint": (
                "주자학 전통은 일반적으로 정좌(靜坐)·궁리(窮理) 등 "
                "내면 수양과 이치 탐구를 통해 수양을 추구하므로, "
                "패검·방울 같은 외적 상징물에 의존하는 수양은 "
                "주자학 정통과 다소 거리가 있다는 평가도 있다."
            ),
            "context": (
                "2026-A Q3 ㉠ 빈칸 정답 의(義) 의 직접 근거 · "
                "남명 패검명 trademark."
            ),
            "keywords": [
                "패검명",
                "내명자경 외단자의",
                "경이직내 의이방외",
                "주역 곤괘 문언전",
                "패검",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-003: 학문 단계론 (소학→근사록→성리대전)
        {
            "id": "cho_sik-claim-003",
            "thinker_id": THINKER_ID,
            "work_id": "cho_sik-hakgiyupyeon",
            "source_detail": (
                "『학기유편(學記類編)』·『남명집』 서간·행장 · "
                "2026학년도 전공A Q3 제시문 셋째 단락"
            ),
            "claim": (
                "물 뿌리고 청소하고 응대하는 예는 어렸을 때부터 익혀서 익숙한 일이며, "
                "이 단계에서 이미 60%(육분, 六分)의 길에 도달하였다. "
                "소학(小學)에 근거한 실천 이후에는 근사록(近思錄)을 보아야 하고, "
                "곁에 성리대전(性理大全)을 두고 1~2년 탐구를 해야 한다. "
                "성현이 되는 것은 모두 이 책(근사록)을 벗어나지 않는다."
            ),
            # coverage/2026-A.md L108 verbatim (Q3 제시문 L52)
            "original_text": (
                "물 뿌리고 청소하고 응대하는 예는 어렸을 때부터 익혀서 익숙한 일이다. "
                "이미 육분(六分, 60%)의 길에 도달하였다. 소학에 근거한 실천 이후에는, "
                "( ㉡ )을/를 보아야 하고, 곁에 성리대전을 두고 1~2년 탐구를 해야 한다. "
                "…(중략)… 성현이 되는 것은 모두 이 ( ㉡ )을/를 벗어나지 않는다 "
                "— 2026학년도 전공A Q3 제시문 (coverage/2026-A.md L108 · "
                "study-guide/2026-A.md L152)"
            ),
            "explanation": (
                "남명 조식의 학문 단계론(소학 → 근사록 → 성리대전) trademark. "
                "조식은 제자들에게 먼저 『소학(小學)』으로 실천의 기본 예절을 익히고, "
                "그 다음 주희(朱熹)·여조겸(呂祖謙)이 공편한 『근사록(近思錄, 1175)』을 통해 "
                "성리학 핵심 개념의 강령을 세운 뒤, "
                "마지막으로 명나라 호광(胡廣) 주편의 『성리대전(性理大全)』으로 심화 탐구하라고 가르쳤다. "
                "'성현이 되는 것은 이 책을 벗어나지 않는다'는 극찬은 조식의 학문 단계 지정 trademark. "
                "2026-A Q3 ㉡ 정답 = 『근사록(近思錄)』 (또는 『대학(大學)』 차순위 후보)."
            ),
            "argument": (
                "전제1: 학문은 일상 예절(쇄소응대)부터 시작한다. "
                "전제2: 실천의 기초가 잡힌 후에는 강령서(근사록)로 성리학 핵심을 정립한다. "
                "전제3: 강령이 잡힌 후에는 집대성서(성리대전)로 심화 탐구한다. "
                "결론: 소학 → 근사록 → 성리대전 순서가 성현이 되는 학문의 길이다."
            ),
            "counterpoint": (
                "조선 성리학 다른 학통(예: 율곡 『성학집요(聖學輯要)』)은 "
                "소학·대학을 중심에 두는 단계론을 제시한다. "
                "남명 학통 내에서도 『대학』을 강조한 흐름이 병존하므로 "
                "㉡ 후보로 『대학』을 들 수도 있으나, 본 문항 맥락(성리대전 병독)에서는 "
                "『근사록』이 더 정합적이다."
            ),
            "context": (
                "2026-A Q3 ㉡ 빈칸 정답 『근사록』 의 직접 근거 · "
                "남명 학문 단계론 trademark."
            ),
            "keywords": [
                "학문 단계론",
                "소학",
                "근사록",
                "성리대전",
                "쇄소응대",
                "육분",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-004: 출처관(出處觀) 대비 — 거경궁리와 대조되는 경의 병립
        {
            "id": "cho_sik-claim-004",
            "thinker_id": THINKER_ID,
            "work_id": "cho_sik-nammyeongjip",
            "source_detail": (
                "『남명집(南冥集)』 서간·행장 · "
                "blocker-log.md L1078 (BLK-175E-2026A-001 후속 조치) · "
                "coverage/2026-A.md L120 (후보 배제 논증)"
            ),
            "claim": (
                "남명 조식의 경의 병립은 퇴계 이황의 거경궁리(居敬窮理) 체계와 대조된다. "
                "퇴계가 경(敬)과 궁리(窮理)의 짝으로 정좌(靜坐)·이치 탐구를 강조한 데 비해, "
                "남명은 경(敬)과 의(義)의 짝으로 일상 실천·외향 결단을 강조하였다. "
                "이 차이는 출처관(出處觀)에서도 나타난다 — "
                "퇴계가 출사(出仕)를 신중히 수용한 데 반해 남명은 처사(處士)로 재야를 철저히 견지하였다."
            ),
            # coverage/2026-A.md L120 verbatim + blocker-log L1078 verbatim
            "original_text": (
                "퇴계 이황(`yihwang`, HIT): 경(敬) 중심 수양론을 체계화한 대표자이나, "
                "\"경과 의를 해와 달로 병립\"하고 \"패검에 敬義 각자\"를 한 수양론적 trademark은 조식 고유. "
                "퇴계는 \"거경궁리(居敬窮理)\" 체계(경 + 궁리)로 의와의 병립 구조가 아님 "
                "— coverage/2026-A.md L120 (후보 배제 논증). "
                "퇴계와의 출처관(出處觀) 대비 — 퇴계 출사(出仕)의 신중한 수용 vs 남명 처사(處士)의 철저한 재야 견지 "
                "— blocker-log.md L1078 (BLK-175E-2026A-001 후속 조치)"
            ),
            "explanation": (
                "남명과 퇴계는 동시대 영남 사림의 양대 산맥으로, "
                "경(敬) 수양은 공유하지만 짝을 이루는 개념이 다르다. "
                "퇴계: 경 + 궁리(窮理 — 이치 탐구) → 정좌·인식 중심. "
                "남명: 경 + 의(義 — 외향 결단) → 일상 실천 중심. "
                "이 짝의 차이는 학문 성격과 사환(仕宦) 태도 모두에 반영된다. "
                "퇴계가 여러 차례 사양 끝에 출사를 수용한 반면, "
                "남명은 단성현감 사직소(1555)에서 보이듯 출사를 끝까지 거부하고 산림처사로 일관하였다. "
                "조선 성리학 영남좌도(퇴계)·영남우도(남명)의 분기점이자 "
                "한국 유학사 출처관 논의의 정전(正典) 사례."
            ),
            "argument": (
                "전제1: 경(敬)을 어떤 개념과 짝지우느냐가 수양의 방향을 결정한다. "
                "전제2: 퇴계는 경+궁리로 인식·정좌 방향을 택했다. "
                "전제3: 남명은 경+의로 일상 실천·외향 결단 방향을 택했다. "
                "결론: 따라서 두 학자의 학문은 같은 성리학 안에서 짝의 구성에 따라 갈라진다."
            ),
            "counterpoint": (
                "퇴계 측 입장에서는 궁리(窮理) 안에 이미 의(義)에 대한 인식이 포함되며, "
                "정좌 수양이 곧 일상 실천의 토대를 마련한다고 본다. "
                "남명의 외향 강조가 자칫 인식적 깊이를 소홀히 할 위험이 있다는 비판도 가능하다."
            ),
            "context": (
                "조선 성리학 영남학파 양대 산맥의 분기점 · "
                "출처관(出處觀) 논의의 정전 사례."
            ),
            "keywords": [
                "출처관 대비",
                "거경궁리 대조",
                "퇴계 이황 대비",
                "산림처사",
                "처사",
                "출사",
            ],
            "verified": False,
            "verification_log": [],
        },
        # CLAIM-005: 산림처사 정신 — 실천·외향 강조
        {
            "id": "cho_sik-claim-005",
            "thinker_id": THINKER_ID,
            "work_id": "cho_sik-nammyeongjip",
            "source_detail": (
                "『남명집(南冥集)』 단성현감 사직소(丹城縣監 辭職疏, 1555) · "
                "blocker-log.md L1078 (BLK-175E-2026A-001 후속 조치)"
            ),
            "claim": (
                "남명은 여러 차례 관직 천거(전생서 주부·단성현감·상서원 판관·종친부 전첨 등)를 사양하고 "
                "재야에서 학문과 수양에 전념하는 산림처사(山林處士) 정신을 견지하였다. "
                "산천재(山天齋)·뇌룡정에서 강학하며 일상 실천의 의(義)를 가르쳤고, "
                "임진왜란 시 곽재우·정인홍·김면 등 의병장 다수가 남명 문하에서 배출되어 "
                "남명 학문의 실천 지향성이 역사적 결실로 입증되었다."
            ),
            # blocker-log.md L1078 verbatim
            "original_text": (
                "산림처사(山林處士) — 여러 차례 관직(전생서 주부·단성현감·상서원 판관·종친부 전첨) 사양, "
                "재야에서 학문과 수양에 전념. "
                "단성현감 사직소(丹城縣監 辭職疏, 1555) — 명종 모친 문정왕후를 \"한 과부(寡婦)\"로 지칭하는 "
                "파격적 직언으로 조선 유학사 상소문의 정점. "
                "의병장 문인 배출 — 임진왜란 시 곽재우·정인홍·김면 등 남명 문하에서 의병장 다수 배출, "
                "실천 지향성이 역사적 결실로 입증 "
                "— blocker-log.md L1078 (BLK-175E-2026A-001 후속 조치 trademark 정리)"
            ),
            "explanation": (
                "남명 조식이 자기 학문의 실천성을 일생의 행적으로 증언한 trademark. "
                "산림처사(山林處士) — 산림(재야)에 머무르는 처사(處士) — 정신은 "
                "성리학 출처관(出處觀)의 한 극단으로, "
                "관직에 나아가지 않고도 학문과 수양으로 사회에 기여하는 사대부의 길이다. "
                "수양처 산천재(山天齋, 지리산 자락)·뇌룡정에서 제자들과 강학하며 "
                "일상 실천의 의(義)를 강조한 결과, "
                "임진왜란 시 곽재우·정인홍·김면 등 의병장 다수가 남명 문하에서 배출되었다. "
                "이는 남명 경의(敬義) 병립의 외향·실천 차원이 "
                "역사적 위기에 결단·행동으로 결실을 맺은 사례로 평가된다."
            ),
            "argument": (
                "전제1: 학문은 강학·저술로만 평가되지 않고 그 실천 결실로도 평가된다. "
                "전제2: 남명은 산림처사로서 일상 실천의 의(義)를 가르쳤다. "
                "전제3: 그 문하에서 임진왜란 의병장이 다수 배출되었다. "
                "결론: 따라서 남명 학문의 실천 지향성은 역사적 결실로 입증되었다."
            ),
            "counterpoint": (
                "출사를 거부한 산림처사 노선은 사대부의 정치적 책임을 회피한다는 비판이 가능하다. "
                "또한 의병장 배출이 곧 학문의 우월성을 입증한다는 추론은 "
                "역사적 우연성과 학문 내적 가치를 혼동할 위험이 있다."
            ),
            "context": (
                "남명 학문의 실천 지향성을 역사적으로 입증한 사례 · "
                "조선 성리학 출처관(出處觀) 한 극단의 정전."
            ),
            "keywords": [
                "산림처사",
                "단성현감 사직소",
                "산천재",
                "뇌룡정",
                "의병장 문인",
                "곽재우",
                "정인홍",
                "실천 지향성",
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
    """남명 조식 핵심 키워드 데이터 입력. 중복 체크 후 insert."""
    keywords = [
        {
            "id": "kw-cho_sik-gyeongui-byeongnip",
            "term": "경의 병립",
            "term_en": "parallel cultivation of reverence and righteousness",
            "definition": (
                "남명 조식 학문의 trademark. "
                "경(敬 — 안을 밝히는 내면 수양, 主敬)과 "
                "의(義 — 밖으로 결단하는 외면 실천, 行義)을 "
                "분리될 수 없는 수양의 양륜(兩輪)으로 함께 세우는 정식. "
                "남명은 두 글자를 '하늘의 해와 달'에 비유하여 "
                "'성현의 천 가지 만 가지 말씀이 이 뜻에서 벗어나지 않는다'고 평가하였다. "
                "퇴계 이황의 거경궁리(경+궁리) 체계와 대비되는 영남우도 수양론의 정점. "
                "2026-A Q3 ㉠ 빈칸 정답 = 의(義)."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "cho_sik-nammyeongjip",
            "related_terms": [
                "경",
                "의",
                "내명자경 외단자의",
                "거경궁리 대조",
                "주경 행의",
            ],
        },
        {
            "id": "kw-cho_sik-naemyeongjagyeong",
            "term": "내명자경 외단자의",
            "term_en": "inner illumination through reverence, outer decision through righteousness",
            "definition": (
                "남명 조식이 평생 차고 다닌 패검(佩劍)에 새긴 16자 명문(銘文) 중 핵심 8자. "
                "한자: 內明者敬 外斷者義 — 안을 밝히는 것은 경이고, 밖으로 결단하는 것은 의이다. "
                "원출전 『주역(周易)』 곤괘(坤卦) 문언전 '경이직내 의이방외(敬以直內 義以方外)'를 "
                "남명이 자기 수양의 안팎 이원 구조로 압축·각인한 trademark. "
                "2026-A Q3 제시문 둘째 단락 직접 근거. "
                "출처: blocker-log.md L1078 (BLK-175E-2026A-001 trademark 3중 일치)."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "cho_sik-nammyeongjip",
            "related_terms": [
                "패검명",
                "경의 병립",
                "주역 곤괘 문언전",
                "경이직내 의이방외",
            ],
        },
        {
            "id": "kw-cho_sik-paegeommyeong",
            "term": "패검명",
            "term_en": "inscription on the sword-handle",
            "definition": (
                "남명 조식이 평생 차고 다닌 패검(佩劍)에 새긴 명문(銘文). "
                "한자: 佩劍銘. 16자 중 핵심 8자가 '내명자경 외단자의(內明者敬 外斷者義)'이며, "
                "이는 남명 경의 병립 수양론의 일상 실천 도구. "
                "허리에 차고 다닌 성성자(惺惺子, 방울)와 함께 남명 수양론의 물리적 상징."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "cho_sik-nammyeongjip",
            "related_terms": [
                "내명자경 외단자의",
                "성성자",
                "경의 병립",
                "수양 도구",
            ],
        },
        {
            "id": "kw-cho_sik-hakmun-dangye",
            "term": "학문 단계론",
            "term_en": "study stage theory",
            "definition": (
                "남명 조식의 성리학 학습 단계 trademark. "
                "공식: 소학(小學) → 근사록(近思錄) → 성리대전(性理大全). "
                "① 소학 — 쇄소응대(灑掃應對) 등 실천의 기본 예절 (이미 60% 도달). "
                "② 근사록(주희·여조겸 공편, 1175) — 성리학 핵심 개념의 강령. "
                "③ 성리대전(명 호광 주편) — 송대 성리학 집대성서 1~2년 심화 탐구. "
                "남명은 '성현이 되는 것은 이 책(근사록)을 벗어나지 않는다'고 극찬하였다. "
                "2026-A Q3 ㉡ 빈칸 정답 = 『근사록』."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "cho_sik-hakgiyupyeon",
            "related_terms": [
                "소학",
                "근사록",
                "성리대전",
                "쇄소응대",
                "육분",
            ],
        },
        {
            "id": "kw-cho_sik-sanrim-cheosa",
            "term": "산림처사",
            "term_en": "scholar-recluse in the mountains and forests",
            "definition": (
                "남명 조식이 일생 견지한 출처관(出處觀)의 trademark. "
                "한자: 山林處士 — 산림(재야)에 머무르는 처사(處士). "
                "여러 차례 관직 천거(전생서 주부·단성현감·상서원 판관·종친부 전첨 등)를 사양하고 "
                "재야에서 학문과 수양에 전념하는 사대부의 길. "
                "수양처 산천재(山天齋)·뇌룡정에서 강학. "
                "퇴계 이황이 출사(出仕)를 신중히 수용한 데 비해 남명은 처사로 재야를 철저히 견지. "
                "1555년 단성현감 사직소(辭職疏)에서 명종 모친 문정왕후를 '한 과부(寡婦)'로 지칭한 "
                "파격적 직언은 조선 유학사 상소문의 정점."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "cho_sik-nammyeongjip",
            "related_terms": [
                "출처관 대비",
                "단성현감 사직소",
                "산천재",
                "뇌룡정",
                "퇴계 출사 대비",
            ],
        },
        {
            "id": "kw-cho_sik-sancheonjae",
            "term": "산천재",
            "term_en": "Sancheonjae study hall",
            "definition": (
                "남명 조식의 수양처. 한자: 山天齋. "
                "지리산 자락에 위치한 강학·은거지로, "
                "남명이 만년에 제자들과 강학하며 경의(敬義) 병립 수양론을 가르친 장소. "
                "뇌룡정과 함께 남명 학문의 물리적 거점."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "cho_sik-nammyeongjip",
            "related_terms": [
                "뇌룡정",
                "산림처사",
                "수양처",
                "지리산",
            ],
        },
        {
            "id": "kw-cho_sik-geogyeong-gungri-daejo",
            "term": "거경궁리 대조",
            "term_en": "contrast with reverence-abiding and principle-investigating",
            "definition": (
                "남명 조식의 경의 병립이 퇴계 이황의 거경궁리(居敬窮理) 체계와 대비되는 trademark. "
                "퇴계: 경(敬) + 궁리(窮理 — 이치 탐구) → 정좌·인식 중심. "
                "남명: 경(敬) + 의(義 — 외향 결단) → 일상 실천 중심. "
                "조선 성리학 영남좌도(퇴계)·영남우도(남명) 분기점. "
                "출처: coverage/2026-A.md L120 후보 배제 논증 — "
                "'퇴계는 거경궁리(居敬窮理) 체계(경 + 궁리)로 의와의 병립 구조가 아님. 배제'."
            ),
            "thinker_id": THINKER_ID,
            "work_id": "cho_sik-nammyeongjip",
            "related_terms": [
                "경의 병립",
                "출처관 대비",
                "퇴계 이황 대비",
                "영남좌도",
                "영남우도",
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
    """남명 조식 영향·비교 관계 데이터 입력.

    ES 등록 확인된 thinker_id 만 링크 (2026-04-28 curl 확인):
    - yihwang  : 등록 (era=조선, 1501-1570) — 동시대 영남 사림 양대 산맥, 거경궁리 vs 경의 병립 대비
    - yiyulgok : 등록 (era=조선, 1536-1584) — 후대 기호학파 vs 영남우도 대비
    """
    relations = [
        {
            "from_thinker": THINKER_ID,
            "to_thinker": "yihwang",
            "type": "compared",
            "description": (
                "남명 조식(1501-1572)과 퇴계 이황(1501-1570)은 동시대 영남 사림의 양대 산맥이다. "
                "두 학자 모두 경(敬)을 수양의 핵심으로 삼았으나 짝을 이루는 개념이 다르다. "
                "퇴계는 거경궁리(居敬窮理) 체계 — 경(敬)과 궁리(窮理 — 이치 탐구)의 짝으로 "
                "정좌(靜坐)·인식 중심 수양을 강조하였다. "
                "남명은 경의(敬義) 병립 — 경(敬)과 의(義 — 외향 결단)의 짝으로 "
                "일상 실천·외향 결단을 강조하였다. "
                "이 짝의 차이는 출처관(出處觀)에서도 나타난다 — "
                "퇴계가 출사(出仕)를 신중히 수용한 데 반해 남명은 처사(處士)로 재야를 철저히 견지하였다. "
                "조선 성리학 영남좌도(퇴계)·영남우도(남명) 분기점."
            ),
            "evidence": (
                "coverage/2026-A.md L120 (Q3 후보 배제 논증) — "
                "'퇴계는 거경궁리(居敬窮理) 체계(경 + 궁리)로 의와의 병립 구조가 아님. 배제'; "
                "blocker-log.md L1078 (BLK-175E-2026A-001 후속 조치) — "
                "'퇴계와의 출처관(出處觀) 대비 — 퇴계 출사(出仕)의 신중한 수용 vs "
                "남명 처사(處士)의 철저한 재야 견지'"
            ),
        },
        {
            "from_thinker": THINKER_ID,
            "to_thinker": "yiyulgok",
            "type": "compared",
            "description": (
                "남명 조식(1501-1572)과 율곡 이이(1536-1584)는 조선 성리학 3대 축의 두 자리이다. "
                "남명은 영남우도 산림처사 노선으로 일상 실천의 의(義)를 강조하였고, "
                "율곡은 기호학파 출사 노선으로 『성학집요(聖學輯要)』 등을 통해 "
                "교수학습 체계와 경세(經世) 사상을 정립하였다. "
                "학문 단계론에서 율곡이 소학·대학 중심을 표준화한 데 비해, "
                "남명은 소학 → 근사록 → 성리대전 순서를 강조하였다. "
                "두 학자는 영남(嶺南)·기호(畿湖) 두 학맥의 정점으로, "
                "퇴계와 함께 조선 중기 성리학 3대 축을 이룬다."
            ),
            "evidence": (
                "coverage/2026-A.md L121 (Q3 후보 배제 논증) — "
                "'율곡 이이(`yiyulgok`, HIT): 『성학집요(聖學輯要)』의 단계론은 소학-대학의 "
                "교수학습 체계로 표준이나, \"경의 두 글자 해와 달 비유\"는 율곡 텍스트에 부재. 배제'; "
                "blocker-log.md L1078 — "
                "'조선 성리학 기호(畿湖)·영남(嶺南) 양대 학맥 중 영남우도의 정점 — "
                "퇴계(영남좌도)·율곡(기호)과 함께 조선 성리학 3대 축'"
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
    print("=== 남명 조식(Cho Sik) 데이터 ES 입력 시작 ===\n")
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
        print(f"  사상가: 1명 (cho_sik)")
        print(f"  저서: {work_count}개")
        print(f"  주장: {claim_count}개")
        print(f"  키워드: {kw_count}개")
        print(f"  관계: {rel_count}개")
        print("\n[OK] 남명 조식 데이터 입력 완료")

    except Exception as e:
        print(f"\n[ERROR] 데이터 입력 중 오류 발생: {e}", file=sys.stderr)
        raise
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
