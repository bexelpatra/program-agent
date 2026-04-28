"""에픽테토스(Epictetus) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS
)


def insert_thinker(client):
    """에픽테토스 사상가 데이터 입력."""
    doc = {
        "id": "epictetus",
        "name": "에픽테토스",
        "name_en": "Epictetus",
        "field": "western_ethics",
        "era": "고대 로마·후기 스토아",
        "birth_year": 50,
        "death_year": 135,
        "background": (
            "프리기아(Phrygia, 현 터키)의 히에라폴리스에서 노예로 태어났다. "
            "로마에서 네로 황제의 비서관 에파프로디토스(Epaphroditus)의 노예였으며, "
            "주인의 허락을 받아 스토아 철학자 무소니우스 루푸스(Musonius Rufus)에게 사사했다. "
            "해방 후 로마에서 철학을 가르쳤으나, 89년 도미티아누스 황제의 철학자 추방령으로 "
            "그리스 북서부 니코폴리스(Nicopolis)로 이주하여 학교를 열었다. "
            "에픽테토스는 글을 쓰지 않았으며, 그의 가르침은 제자 아리아노스(Flavius Arrianus)가 "
            "기록한 '담론집(Discourses, Διατριβαί)'과 이를 요약한 '엥케이리디온(Enchiridion, 편람)'으로 전한다. "
            "다리가 불편했다고 전해지며(노예 시절 부상 또는 질병), "
            "신체적 장애에도 불구하고 내면의 자유를 강조한 삶 자체가 그의 철학을 체현했다."
        ),
        "core_philosophy": (
            "에픽테토스 철학의 핵심은 '우리에게 달려 있는 것(ἐφ᾽ ἡμῖν, eph' hemin)'과 "
            "'우리에게 달려 있지 않은 것(οὐκ ἐφ᾽ ἡμῖν)'의 구분이다. "
            "우리에게 달려 있는 것은 판단, 욕구, 충동, 혐오 등 내면의 태도뿐이며, "
            "신체, 재산, 평판, 관직 등은 우리에게 달려 있지 않다. "
            "불행은 우리에게 달려 있지 않은 것을 통제하려는 헛된 시도에서 비롯된다. "
            "행복(εὐδαιμονία)은 외부 사건 자체가 아니라 그에 대한 우리의 판단과 태도를 바로잡는 데 있다. "
            "이성(λόγος)에 따라 자연(φύσις)과 조화롭게 살며, 신이 부여한 역할(πρόσωπον)을 "
            "성실히 수행하는 것이 스토아적 덕의 실천이다."
        ),
        "philosophical_journey": (
            "초기(노예 시절~해방): 무소니우스 루푸스에게 스토아 철학을 배우며 "
            "내면의 자유와 외적 조건의 무관함을 체득했다. "
            "노예 신분에서 겪은 고통이 '통제할 수 없는 것에 대한 집착 포기'라는 핵심 통찰의 바탕이 되었다. "
            "중기(로마 시절, 해방~89년): 해방 후 로마에서 철학 강의를 시작했다. "
            "실천적이고 직설적인 교육 방식으로 명성을 얻었으나, "
            "도미티아누스의 철학자 추방령(89년)으로 로마를 떠나야 했다. "
            "후기(니코폴리스 시절, 89~135년): 니코폴리스에 학교를 열고 "
            "수많은 제자를 양성했다. 아리아노스가 이 시기 강의를 기록하여 "
            "'담론집' 8권 중 4권과 '엥케이리디온'이 전해진다. "
            "마르쿠스 아우렐리우스는 직접 만나지 않았으나 에픽테토스의 저작을 통해 깊은 영향을 받았다."
        ),
        "keywords": [
            "우리에게 달려 있는 것(eph' hemin)",
            "프로하이레시스(도덕적 선택)",
            "표상의 사용",
            "역할(프로소폰)",
            "아파테이아(부동심)",
            "자연에 따른 삶",
            "내면의 자유"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="epictetus", document=doc)
    print(f"[thinker] epictetus: {result['result']}")
    return result


def insert_works(client):
    """에픽테토스 저서 데이터 입력."""
    works = [
        {
            "id": "epictetus-discourses",
            "thinker_id": "epictetus",
            "title": "담론집",
            "title_original": "Discourses (Διατριβαί, Diatribai)",
            "year": 108,
            "significance": (
                "에픽테토스의 제자 아리아노스(Arrianus)가 스승의 강의를 기록한 것으로, "
                "원래 8권이었으나 현재 4권만 전한다. "
                "에픽테토스 철학의 가장 상세한 원천으로, 구체적 상황에 대한 윤리적 분석, "
                "학생들과의 대화, 실천적 훈련 방법 등을 담고 있다. "
                "스토아 윤리학의 일상 적용을 보여주는 핵심 문헌이다."
            ),
            "key_concepts": [
                "eph' hemin(우리에게 달려 있는 것)",
                "프로하이레시스", "표상의 사용", "세 가지 토포스(훈련 영역)",
                "역할과 의무", "자유와 노예"
            ]
        },
        {
            "id": "epictetus-enchiridion",
            "thinker_id": "epictetus",
            "title": "엥케이리디온 (편람)",
            "title_original": "Enchiridion (Ἐγχειρίδιον)",
            "year": 125,
            "significance": (
                "아리아노스가 에픽테토스의 '담론집'에서 핵심 가르침을 추려 53개 항목으로 정리한 요약본. "
                "'엥케이리디온'은 '손 안에 드는 것(handbook)'이라는 뜻으로, "
                "일상에서 즉시 참조할 수 있는 실천 지침서다. "
                "첫 구절 '우리에게 달려 있는 것과 달려 있지 않은 것을 구분하라'는 "
                "스토아 윤리학 전체의 출발점으로 유명하다. "
                "후대 기독교 수도원에서도 수양서로 사용되어 "
                "스토아 철학이 서양 정신사에 지속적으로 영향을 미치는 데 기여했다."
            ),
            "key_concepts": [
                "이분법(dichotomy of control)", "표상의 올바른 사용",
                "욕구와 혐오의 훈련", "역할 수행", "부동심(아파테이아)"
            ]
        },
        {
            "id": "epictetus-fragments",
            "thinker_id": "epictetus",
            "title": "단편집",
            "title_original": "Fragments (Ἀποσπάσματα)",
            "year": 120,
            "significance": (
                "담론집의 소실된 4권과 기타 출처에서 전해지는 에픽테토스의 단편적 발언 모음. "
                "스토바이오스(Stobaeus)의 '발췌선집(Anthology)'과 "
                "아울루스 겔리우스(Aulus Gellius)의 '아티카의 밤(Noctes Atticae)' 등에 보존되어 있다. "
                "담론집과 엥케이리디온에서 다루지 않는 주제들을 보완한다."
            ),
            "key_concepts": [
                "스토아 윤리학 보완 자료", "일상적 덕의 실천", "철학적 훈련"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """에픽테토스 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 이분법 — 우리에게 달려 있는 것과 그렇지 않은 것
        {
            "id": "epictetus-claim-001",
            "thinker_id": "epictetus",
            "work_id": "epictetus-enchiridion",
            "source_detail": "Enchiridion 1; Discourses I.1",
            "claim": (
                "존재하는 것들 가운데 어떤 것은 우리에게 달려 있고(ἐφ᾽ ἡμῖν), "
                "어떤 것은 우리에게 달려 있지 않다(οὐκ ἐφ᾽ ἡμῖν). "
                "우리에게 달려 있는 것은 판단, 충동, 욕구, 혐오이며, "
                "달려 있지 않은 것은 신체, 재산, 평판, 관직이다. "
                "행복과 자유는 이 구분을 깨닫고 우리에게 달려 있는 것에만 집중할 때 얻어진다."
            ),
            "original_text": (
                "Τῶν ὄντων τὰ μέν ἐστιν ἐφ᾽ ἡμῖν, τὰ δὲ οὐκ ἐφ᾽ ἡμῖν. "
                "ἐφ᾽ ἡμῖν μὲν ὑπόληψις, ὁρμή, ὄρεξις, ἔκκλισις, "
                "καὶ ἑνὶ λόγῳ ὅσα ἡμέτερα ἔργα· "
                "οὐκ ἐφ᾽ ἡμῖν δὲ τὸ σῶμα, ἡ κτῆσις, δόξαι, ἀρχαί, "
                "καὶ ἑνὶ λόγῳ ὅσα οὐχ ἡμέτερα ἔργα. "
                "(Of things some are in our power, and others are not.)"
            ),
            "original_text_ko": (
                "존재하는 것들 가운데 어떤 것은 우리에게 달려 있고, 어떤 것은 우리에게 달려 있지 않다. "
                "우리에게 달려 있는 것은 판단, 충동, 욕구, 혐오, 한마디로 우리 자신의 행위이다. "
                "우리에게 달려 있지 않은 것은 신체, 재산, 평판, 관직, 한마디로 우리 자신의 행위가 아닌 것이다."
            ),
            "explanation": (
                "에픽테토스 철학의 가장 근본적인 원리. "
                "외부 사건(질병, 빈곤, 타인의 행동)은 통제할 수 없지만, "
                "그에 대한 우리의 판단과 반응은 전적으로 우리에게 달려 있다. "
                "사람들이 불행한 이유는 외부 사건 자체가 아니라, "
                "통제할 수 없는 것을 통제하려 하거나 통제할 수 있는 것을 방치하기 때문이다. "
                "이 이분법을 체득하면 어떤 상황에서도 내면의 자유와 평정을 유지할 수 있다."
            ),
            "argument": (
                "(1) 세상의 모든 것은 '우리 힘으로 바꿀 수 있는 것'과 '바꿀 수 없는 것'으로 나뉜다. "
                "(2) 판단, 욕구, 충동, 혐오는 우리 내면의 작용이므로 우리가 통제할 수 있다. "
                "(3) 신체, 재산, 평판, 관직은 외부 요인에 의해 좌우되므로 우리가 궁극적으로 통제할 수 없다. "
                "(4) 통제 불가능한 것에 기대를 걸면 좌절과 고통이 필연적으로 따른다. "
                "(5) 통제 가능한 내면에 집중하면 외부 사건에 흔들리지 않는 자유(ἐλευθερία)를 얻는다. "
                "(6) 따라서 행복의 조건은 외적 환경이 아니라 내면의 태도에 있다."
            ),
            "counterpoint": (
                "아리스토텔레스는 '니코마코스 윤리학'(1099a-1099b)에서 "
                "행복(에우다이모니아)에는 덕뿐 아니라 일정한 외적 재화(건강, 부, 친구, 좋은 가문)도 필요하다고 주장했다. "
                "극단적 불행 속에서도 행복할 수 있다는 스토아적 입장은 비현실적이라는 것이다. "
                "에피쿠로스는 쾌락과 고통의 감각 경험이 행복의 기준이라 보아, "
                "에픽테토스처럼 외적 고통을 단순히 '판단의 문제'로 환원하는 것에 동의하지 않았다."
            ),
            "context": (
                "에픽테토스가 노예 출신이라는 사실이 이 가르침에 특별한 무게를 부여한다. "
                "그는 자신의 삶으로 이 원리를 체현했다—신체적 자유가 없어도 "
                "내면의 자유는 가능하다는 것을 직접 보여주었다. "
                "이 이분법은 스토아 철학의 핵심이지만, 에픽테토스가 가장 명확하고 실천적으로 정식화했다."
            ),
            "category": "윤리학",
            "difficulty": "기본",
            "verified": False
        },
        # CLAIM-002: 표상의 올바른 사용
        {
            "id": "epictetus-claim-002",
            "thinker_id": "epictetus",
            "work_id": "epictetus-discourses",
            "source_detail": "Discourses I.1.7; II.18.24; Enchiridion 5",
            "claim": (
                "우리를 괴롭히는 것은 사물 자체가 아니라 사물에 대한 우리의 판단(δόγματα)이다. "
                "표상(φαντασία)이 떠오를 때 즉시 동의하지 말고 검토해야 한다. "
                "올바른 표상 사용은 스토아적 자유의 핵심 실천이다."
            ),
            "original_text": (
                "Ταράσσει τοὺς ἀνθρώπους οὐ τὰ πράγματα, ἀλλὰ τὰ περὶ τῶν πραγμάτων δόγματα. "
                "(It is not things that disturb us, but our judgments about things. Enchiridion 5)"
            ),
            "original_text_ko": (
                "사람들을 괴롭히는 것은 사물이 아니라 사물에 대한 판단이다."
            ),
            "explanation": (
                "에픽테토스에 따르면 외부 사건은 그 자체로 좋거나 나쁘지 않다. "
                "사건이 우리에게 영향을 미치는 것은 우리가 그것에 부여하는 판단을 통해서다. "
                "예를 들어 죽음 자체는 두려운 것이 아니지만, '죽음은 두렵다'는 판단이 공포를 낳는다. "
                "따라서 철학적 훈련의 핵심은 자동적으로 떠오르는 표상(인상)에 "
                "즉시 동의하지 않고 이성으로 검토하여 올바른 판단을 내리는 것이다. "
                "이것이 에픽테토스가 말하는 '표상의 올바른 사용(χρῆσις φαντασιῶν)'이다."
            ),
            "argument": (
                "(1) 같은 사건을 겪어도 사람마다 반응이 다르다—이는 사건이 아니라 판단이 반응을 결정함을 보여준다. "
                "(2) 판단은 우리에게 달려 있으므로(이분법), 우리가 바꿀 수 있다. "
                "(3) 잘못된 판단(예: '재산 손실은 재앙이다')은 불필요한 고통을 낳는다. "
                "(4) 올바른 판단(예: '재산은 내 힘 밖의 것이므로 집착할 대상이 아니다')은 평정을 준다. "
                "(5) 철학적 훈련은 표상이 떠올 때 '잠깐, 이것은 나에게 달려 있는가?'라고 묻는 습관을 기르는 것이다. "
                "(6) 이 훈련을 통해 외부 사건에 대한 자동적 감정 반응을 이성적 판단으로 대체할 수 있다."
            ),
            "counterpoint": (
                "에피쿠로스는 감각 경험(쾌락과 고통)이 실재적이며, "
                "고통을 단순히 판단의 문제로 환원할 수 없다고 보았다. "
                "아리스토텔레스도 감정(πάθος)은 적절한 상황에서 적절한 정도로 느끼는 것이 덕이라 하여(중용론), "
                "감정 자체를 판단의 오류로 보는 스토아적 접근과 달랐다. "
                "현대 인지행동치료(CBT)는 에픽테토스의 이 통찰에 직접 영향을 받았으나, "
                "감정의 신체적·무의식적 차원을 추가적으로 고려한다."
            ),
            "context": (
                "이 원리는 초기 스토아(크리시포스)의 인식론에 뿌리를 두지만, "
                "에픽테토스가 실천적 심리학의 수준으로 끌어올렸다. "
                "알베르 엘리스(Albert Ellis)의 합리적 정서행동치료(REBT)와 "
                "아론 벡(Aaron Beck)의 인지치료(CT)가 에픽테토스의 이 통찰에서 직접 영감을 받았다."
            ),
            "category": "윤리학·인식론",
            "difficulty": "기본",
            "verified": False
        },
        # CLAIM-003: 프로하이레시스 (도덕적 선택 능력)
        {
            "id": "epictetus-claim-003",
            "thinker_id": "epictetus",
            "work_id": "epictetus-discourses",
            "source_detail": "Discourses I.17.21; II.10.1; III.3.4-5",
            "claim": (
                "프로하이레시스(προαίρεσις, 도덕적 선택 능력)는 인간의 본질이며, "
                "어떤 외부 힘도 이를 강제할 수 없다. "
                "사람의 진정한 정체성은 신체나 재산이 아니라 프로하이레시스에 있다. "
                "프로하이레시스를 올바르게 사용하는 것이 곧 덕이고 자유다."
            ),
            "original_text": (
                "Σὲ δὲ τίς δύναται ἀναγκάσαι εἰς ὃ μὴ δοκεῖ συγκαταθέσθαι; τίς εἰς ὃ μὴ θέλεις ὁρμῆσαι; "
                "(Who can compel you to assent to what seems false? Who can compel you to pursue what you do not want? "
                "Discourses I.17.21)"
            ),
            "original_text_ko": (
                "누가 당신에게 거짓으로 보이는 것에 동의하도록 강제할 수 있는가? "
                "누가 당신이 원하지 않는 것을 추구하도록 강제할 수 있는가?"
            ),
            "explanation": (
                "프로하이레시스는 에픽테토스 철학의 핵심 개념으로, "
                "이성적 존재로서 인간이 가진 선택·판단·결단의 능력을 가리킨다. "
                "아리스토텔레스도 이 용어를 사용했지만 주로 '숙고된 선택'의 의미였고, "
                "에픽테토스는 이를 인간 존재의 본질, 즉 '진정한 자아'로 격상시켰다. "
                "폭군이 신체를 구속하거나 재산을 빼앗을 수 있지만, "
                "프로하이레시스—판단하고 선택하는 내면의 능력—은 침범할 수 없다. "
                "이것이 스토아적 자유의 궁극적 근거다."
            ),
            "argument": (
                "(1) 인간의 고유한 능력은 이성적 선택(프로하이레시스)이다. "
                "(2) 외부 강제력(폭군, 질병, 빈곤)은 신체와 재산에는 작용할 수 있지만 "
                "판단과 동의에는 작용할 수 없다. "
                "(3) 누구도 나에게 거짓을 참으로 믿도록 강제할 수 없고, "
                "내가 원하지 않는 것을 추구하도록 강제할 수 없다. "
                "(4) 따라서 프로하이레시스는 외부 힘에 의해 침범될 수 없는 영역이다. "
                "(5) 인간의 진정한 정체성과 자유는 이 침범 불가능한 내면의 선택 능력에 있다. "
                "(6) 프로하이레시스를 이성(로고스)에 따라 올바르게 행사하는 것이 곧 덕이다."
            ),
            "counterpoint": (
                "마르크스주의 철학은 인간의 의식(판단, 선택)이 물질적·사회적 조건에 의해 구조적으로 규정된다고 보아, "
                "프로하이레시스의 절대적 자유를 관념론적 환상이라 비판할 수 있다. "
                "한나 아렌트는 '인간의 조건'(1958)에서 자유는 내면의 사유가 아니라 "
                "공적 공간에서의 행위(action)를 통해 실현된다고 하여 에픽테토스의 내면주의와 대비된다. "
                "현대 신경과학은 의식적 선택에 앞서 뇌의 무의식적 과정이 이미 진행된다는 실험 결과를 제시하여 "
                "프로하이레시스의 절대적 자율성에 도전한다."
            ),
            "context": (
                "에픽테토스가 노예 출신이라는 점에서 프로하이레시스 개념은 특별한 의미를 가진다. "
                "신체적으로 타인의 소유물이었던 자가 '진정한 자아는 아무도 소유할 수 없다'고 선언한 것이다. "
                "이 개념은 후대 기독교의 영혼 불가침성, 칸트의 인격 존엄성 개념에도 영향을 주었다."
            ),
            "category": "윤리학·자유론",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-004: 세 가지 토포스 (수련 영역)
        {
            "id": "epictetus-claim-004",
            "thinker_id": "epictetus",
            "work_id": "epictetus-discourses",
            "source_detail": "Discourses III.2.1-5; III.12.1-8",
            "claim": (
                "철학적 수련에는 세 가지 토포스(τόποι, 영역)가 있다: "
                "(1) 욕구와 혐오의 영역(ὄρεξις/ἔκκλισις) — 스토아 자연학(physics)에 해당, "
                "(2) 충동과 행위의 영역(ὁρμή) — 스토아 윤리학(ethics)에 해당, "
                "(3) 동의와 판단의 영역(συγκατάθεσις) — 스토아 논리학(logic)에 해당. "
                "이 순서대로 수련해야 하며, 첫 번째가 가장 급하고 중요하다."
            ),
            "original_text": (
                "Τρεῖς εἰσι τόποι, ἐν οἷς ἀσκηθῆναι δεῖ τὸν ἐσόμενον καλὸν καὶ ἀγαθόν· "
                "(There are three areas in which one who would be good and noble must be trained. "
                "Discourses III.2.1)"
            ),
            "original_text_ko": (
                "훌륭하고 선한 사람이 되려는 자가 수련해야 할 세 가지 영역이 있다."
            ),
            "explanation": (
                "에픽테토스는 스토아 철학의 세 분야(자연학·윤리학·논리학)를 "
                "실천적 수련 프로그램으로 재구성했다. "
                "첫 번째 토포스(욕구/혐오)는 우리가 무엇을 바라고 피하는지를 바로잡는 것으로, "
                "오직 덕만을 욕구하고 악덕만을 혐오하도록 훈련한다. "
                "두 번째 토포스(충동/행위)는 사회적 역할과 의무를 올바르게 수행하는 것이다. "
                "세 번째 토포스(동의/판단)는 표상에 대해 정확하게 판단하는 논리적 능력을 기르는 것이다. "
                "에픽테토스는 대부분의 학생이 첫 번째 토포스도 제대로 수련하지 않으면서 "
                "세 번째(논리학)로 뛰어가려 한다고 비판했다."
            ),
            "argument": (
                "(1) 철학은 단순한 지식이 아니라 삶의 기술(τέχνη τοῦ βίου)이므로 체계적 훈련이 필요하다. "
                "(2) 가장 시급한 것은 욕구와 혐오를 바로잡는 것이다—잘못된 욕구가 모든 고통의 원천이므로. "
                "(3) 욕구가 바로잡힌 후에야 사회적 역할(아버지, 시민, 친구)을 올바르게 수행할 수 있다. "
                "(4) 역할 수행이 확립된 후에야 판단의 정밀성(논리학)이 의미를 가진다. "
                "(5) 이 순서를 무시하고 논리학적 세련됨만 추구하는 것은 "
                "삶을 바로잡지 못하는 공허한 철학이다."
            ),
            "counterpoint": (
                "아리스토텔레스는 '니코마코스 윤리학' 2권에서 덕은 습관(ἔθος)을 통해 형성되며, "
                "실천적 지혜(φρόνησις)가 중심이라 보아 에픽테토스의 체계적 토포스 구분과 다르다. "
                "소크라테스는 덕은 앎(지행합일)이라 하여 지적 이해가 곧 실천으로 이어진다고 보았으나, "
                "에픽테토스는 앎과 실천 사이에 반복적 훈련(ἄσκησις)이 필요하다고 강조하여 "
                "소크라테스의 지행합일론을 사실상 수정했다."
            ),
            "context": (
                "세 가지 토포스는 에픽테토스 고유의 체계로, 초기 스토아에서 직접적인 선행 형태를 찾기 어렵다. "
                "이것은 에픽테토스가 스토아 철학을 단순히 전달한 것이 아니라 "
                "자신만의 실천적 교육 체계로 재구성했음을 보여준다."
            ),
            "category": "윤리학·교육",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-005: 역할(프로소폰)과 의무
        {
            "id": "epictetus-claim-005",
            "thinker_id": "epictetus",
            "work_id": "epictetus-discourses",
            "source_detail": "Discourses II.10; Enchiridion 30; Discourses I.2.12-18",
            "claim": (
                "모든 인간에게는 여러 역할(πρόσωπον)이 있다: "
                "이성적 존재로서의 보편적 역할, 그리고 구체적 관계에서의 역할(아들, 아버지, 시민, 친구). "
                "각 역할이 부과하는 의무(καθῆκον)를 성실히 수행하는 것이 덕이다. "
                "역할은 선택한 것이든 주어진 것이든 모두 수행해야 한다."
            ),
            "original_text": (
                "Σκέψαι τίς εἶ. πρῶτον μὲν ἄνθρωπος... εἶτα πολίτης... "
                "(Consider who you are. First, a human being... then a citizen... "
                "Discourses II.10.1)"
            ),
            "original_text_ko": (
                "네가 누구인지 살펴보라. 먼저 인간이고... 그다음 시민이고..."
            ),
            "explanation": (
                "에픽테토스는 스토아 윤리학의 의무론(카테콘 이론)을 역할 개념으로 구체화했다. "
                "모든 인간은 (1) 이성적 존재로서의 보편적 역할(인류 전체에 대한 의무), "
                "(2) 구체적 관계에서의 역할(특정한 관계적 의무)을 가진다. "
                "배우가 주어진 역할을 최선을 다해 연기하듯, "
                "우리도 삶에서 주어진 역할을 성실히 수행해야 한다. "
                "역할 자체를 선택할 수는 없지만(아들로 태어나는 것은 선택이 아니지만), "
                "그 역할을 어떻게 수행할지는 우리에게 달려 있다."
            ),
            "argument": (
                "(1) 인간은 사회적 존재이며 다양한 관계 속에 놓여 있다. "
                "(2) 각 관계는 특정한 의무를 수반한다—아버지는 아버지로서, 시민은 시민으로서의 의무가 있다. "
                "(3) 이 의무를 수행하는 것이 자연에 따른 삶(κατὰ φύσιν)이다. "
                "(4) 역할은 우리가 선택한 것(직업, 관계)과 주어진 것(성별, 국적)이 있지만, "
                "둘 다 성실히 수행해야 한다. "
                "(5) 역할 수행은 이분법(eph' hemin)과 모순되지 않는다—"
                "결과는 통제할 수 없지만 역할을 성실히 수행하려는 노력은 우리에게 달려 있다."
            ),
            "counterpoint": (
                "실존주의 철학자 사르트르는 '존재와 무'(1943)에서 "
                "인간에게 주어진 역할이란 없으며, 실존이 본질에 앞선다고 주장했다. "
                "사회적 역할에 자기를 동일시하는 것은 '자기기만(mauvaise foi)'이다. "
                "이는 에픽테토스의 역할 윤리학과 정면으로 대립한다. "
                "한편 유교의 오륜(五倫)은 역할 윤리라는 점에서 에픽테토스와 구조적 유사성이 있으나, "
                "개인의 내면적 자유보다 관계적 조화를 강조한다."
            ),
            "context": (
                "역할(프로소폰) 개념은 중기 스토아의 파나이티오스(Panaetius)가 이미 발전시켰으며, "
                "키케로의 '의무론(De Officiis)'에도 반영되어 있다. "
                "에픽테토스는 이를 일상적 실천의 수준에서 더 구체화했다."
            ),
            "category": "윤리학",
            "difficulty": "보통",
            "verified": False
        },
        # CLAIM-006: 신의 섭리와 우주적 질서에 대한 동의
        {
            "id": "epictetus-claim-006",
            "thinker_id": "epictetus",
            "work_id": "epictetus-discourses",
            "source_detail": "Discourses I.6; I.16; Enchiridion 53",
            "claim": (
                "우주는 신(제우스/로고스)의 섭리에 의해 합리적으로 질서 지어져 있다. "
                "인간에게 일어나는 모든 일은 우주적 계획의 일부이며, "
                "철학자의 과제는 이 질서에 자발적으로 동의하고 자신의 역할을 기꺼이 수행하는 것이다. "
                "불평은 우주적 질서에 대한 무지에서 비롯된다."
            ),
            "original_text": (
                "ἄγου δέ μ᾽, ὦ Ζεῦ, καὶ σύ γ᾽ ἡ Πεπρωμένη, "
                "ὅποι ποθ᾽ ὑμῖν εἰμι διατεταγμένος· "
                "ὡς ἕψομαί γ᾽ ἄοκνος· ἢν δέ γε μὴ θέλω, "
                "κακὸς γενόμενος, οὐδὲν ἧττον ἕψομαι. "
                "(Lead me, O Zeus, and thou, O Destiny, "
                "whither I am appointed to go. "
                "I will follow willingly; but if I am not willing, "
                "I will follow nonetheless, though a wretch. — Cleanthes' Hymn, cited in Enchiridion 53)"
            ),
            "original_text_ko": (
                "이끌어 주소서, 오 제우스여, 그리고 그대, 운명의 여신이여, "
                "당신들이 나를 배치한 곳으로. "
                "나는 기꺼이 따르겠나이다. 만약 내가 원하지 않더라도, "
                "비천한 자가 되어 어차피 따르게 될 것입니다."
            ),
            "explanation": (
                "에픽테토스는 스토아 물리학의 섭리론(프로노이아)을 윤리학적 실천으로 연결한다. "
                "우주는 이성(로고스)에 의해 지배되며, 모든 사건은 이 이성적 질서의 일부다. "
                "인간의 이성은 우주적 이성의 일부이므로, 자연에 따라 사는 것은 "
                "우주적 질서에 자발적으로 동의하는 것이다. "
                "저항해도 운명은 바뀌지 않지만, 자발적 동의는 내면의 평화를 준다. "
                "이는 운명론이 아니라 '자발적 수용'의 윤리학이다."
            ),
            "argument": (
                "(1) 우주는 이성(로고스)에 의해 합리적으로 질서 지어져 있다(스토아 물리학 전제). "
                "(2) 인간의 이성은 우주적 이성의 일부(분유)이다. "
                "(3) 자연에 따라 사는 것은 우주적 이성과 조화롭게 사는 것이다. "
                "(4) 우주적 질서에 저항하면 고통이 따르지만 결과는 바뀌지 않는다. "
                "(5) 우주적 질서에 자발적으로 동의하면 평정과 기쁨이 가능하다. "
                "(6) 따라서 지혜로운 자는 운명을 기꺼이 받아들이며, 이것이 진정한 자유다."
            ),
            "counterpoint": (
                "에피쿠로스는 우주에 목적이나 섭리가 없으며 원자들의 무작위적 결합이라 주장하여 "
                "스토아의 섭리론을 정면으로 부정했다. "
                "근대 실존주의(카뮈, '시시포스의 신화' 1942)는 우주에 의미가 없다는 부조리를 직시하면서도 "
                "그 속에서 반항하는 것이 인간의 존엄이라 하여, "
                "에픽테토스의 '자발적 동의'와 대조된다. "
                "또한 악의 문제(theodicy)—섭리가 있다면 왜 무고한 고통이 있는가—는 "
                "스토아 섭리론의 오랜 난제다."
            ),
            "context": (
                "클레안테스의 찬가(Hymn to Zeus)는 초기 스토아의 섭리론을 시적으로 표현한 것으로, "
                "에픽테토스가 '엥케이리디온'의 마지막 항목에 인용할 만큼 중시했다. "
                "이 섭리론은 기독교와의 접점에서 중요하며, "
                "초기 기독교 교부들이 스토아 사상을 수용하는 통로가 되었다."
            ),
            "category": "형이상학·윤리학",
            "difficulty": "심화",
            "verified": False
        },
        # CLAIM-007: 자유와 노예의 참된 의미
        {
            "id": "epictetus-claim-007",
            "thinker_id": "epictetus",
            "work_id": "epictetus-discourses",
            "source_detail": "Discourses IV.1 (On Freedom)",
            "claim": (
                "진정한 자유는 정치적·법적 지위가 아니라 내면의 상태다. "
                "외적으로 자유로운 사람도 욕구와 공포에 종속되어 있으면 노예이며, "
                "법적 노예라도 프로하이레시스를 올바르게 행사하면 자유롭다. "
                "자유로운 자는 오직 자기에게 달려 있는 것만을 욕구하고, "
                "자기에게 달려 있지 않은 것에는 집착하지 않는 자다."
            ),
            "original_text": (
                "Ἐλεύθερός ἐστιν ὁ ζῶν ὡς βούλεται... "
                "ὃν οὔτ᾽ ἀναγκάσαι τις δύναται οὔτε κωλῦσαι οὔτε βιάσασθαι. "
                "(Free is the one who lives as he wishes... "
                "whom no one can compel, hinder, or force. Discourses IV.1.1)"
            ),
            "original_text_ko": (
                "자유로운 자는 자기가 원하는 대로 사는 자이며, "
                "아무도 그를 강제하거나 방해하거나 폭력으로 굴복시킬 수 없는 자다."
            ),
            "explanation": (
                "'담론집' 4권 1장은 에픽테토스의 가장 긴 담론으로 자유를 주제로 한다. "
                "에픽테토스는 자유를 외적 조건(법적 신분, 정치적 권리)이 아니라 "
                "내면적 상태(욕구와 혐오의 올바른 방향)로 재정의한다. "
                "부유하고 권력 있는 자도 재산 손실이나 권력 상실을 두려워하면 노예이며, "
                "가난하고 법적 노예인 자도 오직 자신에게 달려 있는 것만을 욕구하면 자유롭다. "
                "이것은 에픽테토스 자신의 노예 경험에서 우러나온 통찰이다."
            ),
            "argument": (
                "(1) 자유란 원하는 대로 살고, 아무도 강제·방해·폭력으로 굴복시킬 수 없는 상태다. "
                "(2) 외적 재화(재산, 건강, 명예)를 욕구하는 자는 이를 빼앗을 수 있는 자의 힘에 종속된다. "
                "(3) 종속된 자는 아무리 법적으로 자유로워도 실질적으로 노예다. "
                "(4) 오직 자기에게 달려 있는 것(판단, 선택)만을 욕구하는 자는 "
                "아무도 빼앗을 수 없는 것을 가지므로 진정으로 자유롭다. "
                "(5) 따라서 진정한 자유는 외적 해방이 아니라 내면의 해방에 있다."
            ),
            "counterpoint": (
                "마르크스는 내면적 자유에 대한 강조가 실제적 억압(노예제, 착취)을 정당화할 수 있다고 비판할 것이다. "
                "구조적 불평등을 '내면의 태도'로 해결할 수 없으며, 해방은 물질적·사회적 조건의 변혁을 통해서만 가능하다. "
                "한나 아렌트는 '혁명론'(1963)에서 "
                "자유는 내면적 경험이 아니라 공적 공간에서의 행위를 통해 실현된다고 주장하여 "
                "에픽테토스의 내면주의를 비판적으로 넘어선다."
            ),
            "context": (
                "에픽테토스가 노예 출신으로서 '자유'를 재정의한 것은 철학사에서 독특한 위치를 차지한다. "
                "이 담론은 미국 독립전쟁과 인권 운동에서도 인용되었으며, "
                "빅토르 프랑클(Viktor Frankl)의 '로고테라피'에도 영향을 주었다. "
                "프랑클은 아우슈비츠 수용소 경험을 에픽테토스적 프레임으로 해석했다."
            ),
            "category": "윤리학·자유론",
            "difficulty": "심화",
            "verified": False
        },
        # CLAIM-008: 아파테이아 — 격정으로부터의 자유
        {
            "id": "epictetus-claim-008",
            "thinker_id": "epictetus",
            "work_id": "epictetus-enchiridion",
            "source_detail": "Enchiridion 2-4; Discourses III.24.84-88",
            "claim": (
                "현자는 격정(πάθος)에 휘둘리지 않는 상태인 아파테이아(ἀπάθεια)에 도달해야 한다. "
                "이는 감정의 부재가 아니라 잘못된 판단에서 비롯되는 파괴적 격정—공포, 탐욕, 분노, 슬픔—으로부터의 "
                "자유를 의미한다. 올바른 판단은 올바른 감정(εὐπάθεια, 좋은 감정)을 낳는다."
            ),
            "original_text": (
                "Μέμνησο ὅτι οὐχ ὁ λοιδορῶν ἢ ὁ τύπτων ὑβρίζει, "
                "ἀλλὰ τὸ δόγμα τὸ περὶ τούτων ὡς ὑβριζόντων. "
                "(Remember that it is not the one who insults or strikes you who wrongs you, "
                "but the judgment that they are wronging you. Enchiridion 20)"
            ),
            "original_text_ko": (
                "모욕하거나 때리는 자가 당신을 해치는 것이 아니라, "
                "그들이 당신을 해치고 있다는 판단이 당신을 해친다는 것을 기억하라."
            ),
            "explanation": (
                "스토아 철학에서 아파테이아는 격정(파토스)의 부재 또는 격정으로부터의 자유를 뜻한다. "
                "스토아가 말하는 격정은 잘못된 판단에 근거한 과도하고 비이성적인 감정 반응이다. "
                "에픽테토스에 따르면 '모욕당했다'는 판단이 분노를 낳고, "
                "'재산을 잃었다'는 판단이 슬픔을 낳는다. "
                "판단을 바로잡으면 이런 파괴적 격정은 사라진다. "
                "대신 이성에 부합하는 좋은 감정(에우파테이아)—기쁨(χαρά), 소망(βούλησις), "
                "조심(εὐλάβεια)—은 현자에게도 있다."
            ),
            "argument": (
                "(1) 격정(공포, 탐욕, 분노, 슬픔)은 외부 사건의 직접적 결과가 아니라 잘못된 판단의 결과다. "
                "(2) 잘못된 판단이란 '이것은 나에게 좋다/나쁘다'는 판단 중 "
                "우리에게 달려 있지 않은 것에 대한 것이다. "
                "(3) 판단을 바로잡으면—'이것은 나에게 달려 있지 않으므로 좋지도 나쁘지도 않다'—격정은 사라진다. "
                "(4) 격정이 사라진 상태(아파테이아)에서도 이성적 감정(에우파테이아)은 남는다. "
                "(5) 따라서 아파테이아는 감정 없는 무감각이 아니라 이성에 부합하는 감정 상태다."
            ),
            "counterpoint": (
                "아리스토텔레스는 '니코마코스 윤리학' 2권에서 "
                "덕은 감정의 제거가 아니라 적절한 때에 적절한 정도로 느끼는 중용(μεσότης)이라 주장했다. "
                "분노도 정당한 상황에서 적절한 정도로 느끼면 덕이 될 수 있다(예: 부정의에 대한 분노). "
                "에픽테토스의 아파테이아는 이 관점에서 보면 지나치게 감정을 억압하는 것일 수 있다. "
                "흄(Hume)은 '인간 본성에 관한 논고'(1739-40)에서 "
                "이성은 감정의 노예이며 감정 없이 도덕 판단은 불가능하다고 하여 "
                "스토아의 이성 중심주의에 정면 도전했다."
            ),
            "context": (
                "'아파테이아'는 후대에 '무감각(apathy)'으로 오해되어 스토아 철학에 대한 편견의 원인이 되었다. "
                "그러나 에픽테토스가 말하는 아파테이아는 감정 자체의 부재가 아니라 "
                "잘못된 판단에 기반한 파괴적 격정으로부터의 해방이다. "
                "에우파테이아(좋은 감정) 개념이 이를 보완한다."
            ),
            "category": "윤리학·심리학",
            "difficulty": "보통",
            "verified": False
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """에픽테토스 키워드 데이터 입력."""
    keywords = [
        {
            "id": "epictetus-kw-001",
            "thinker_id": "epictetus",
            "term": "에프 헤민 (Eph' hemin)",
            "term_original": "ἐφ᾽ ἡμῖν",
            "definition": (
                "'우리에게 달려 있는 것'. 에픽테토스 철학의 가장 근본적인 개념. "
                "판단, 충동, 욕구, 혐오 등 내면의 태도만이 우리에게 달려 있으며, "
                "신체, 재산, 평판, 관직 등은 우리에게 달려 있지 않다. "
                "이 구분을 깨닫고 실천하는 것이 스토아적 자유와 행복의 출발점이다."
            ),
            "related_claims": ["epictetus-claim-001", "epictetus-claim-002"],
            "source": "Enchiridion 1; Discourses I.1"
        },
        {
            "id": "epictetus-kw-002",
            "thinker_id": "epictetus",
            "term": "프로하이레시스 (Prohairesis)",
            "term_original": "προαίρεσις",
            "definition": (
                "도덕적 선택 능력 또는 의지. 에픽테토스에게 인간의 본질이자 진정한 자아. "
                "외부 힘이 침범할 수 없는 내면의 선택·판단·결단 능력으로, "
                "이를 이성에 따라 올바르게 행사하는 것이 덕이며 자유다. "
                "아리스토텔레스도 사용한 용어이나, 에픽테토스가 '인간 존재의 본질'로 격상시켰다."
            ),
            "related_claims": ["epictetus-claim-003", "epictetus-claim-007"],
            "source": "Discourses I.17.21; II.10.1"
        },
        {
            "id": "epictetus-kw-003",
            "thinker_id": "epictetus",
            "term": "판타시아 (Phantasia)",
            "term_original": "φαντασία",
            "definition": (
                "표상 또는 인상. 외부 사물이나 사건이 마음에 떠올리는 심적 이미지. "
                "에픽테토스에 따르면 표상 자체는 자동적으로 생기지만, "
                "그에 동의할지 여부는 우리에게 달려 있다. "
                "표상의 올바른 사용(χρῆσις φαντασιῶν)은 스토아적 자유의 핵심 실천이다."
            ),
            "related_claims": ["epictetus-claim-002"],
            "source": "Discourses I.1.7; Enchiridion 5"
        },
        {
            "id": "epictetus-kw-004",
            "thinker_id": "epictetus",
            "term": "아파테이아 (Apatheia)",
            "term_original": "ἀπάθεια",
            "definition": (
                "격정(πάθος)으로부터의 자유 또는 부동심. "
                "감정의 완전한 부재가 아니라 잘못된 판단에 기반한 파괴적 격정(공포, 탐욕, 분노, 슬픔)에서 "
                "벗어난 상태. 이성에 부합하는 좋은 감정(에우파테이아: 기쁨, 소망, 조심)은 유지된다. "
                "후대에 '무감각(apathy)'으로 오해되어 스토아 철학에 대한 편견의 원인이 되었다."
            ),
            "related_claims": ["epictetus-claim-008"],
            "source": "Enchiridion 2-4; Discourses III.24"
        },
        {
            "id": "epictetus-kw-005",
            "thinker_id": "epictetus",
            "term": "프로소폰 (Prosopon)",
            "term_original": "πρόσωπον",
            "definition": (
                "역할 또는 인격(persona). 연극의 가면에서 유래한 용어로, "
                "에픽테토스에게 인간이 삶에서 수행해야 할 사회적 역할을 의미한다. "
                "이성적 존재로서의 보편적 역할과 구체적 관계(아들, 시민, 친구)에서의 역할이 있으며, "
                "각 역할이 부과하는 의무(카테콘)를 성실히 수행하는 것이 덕이다."
            ),
            "related_claims": ["epictetus-claim-005"],
            "source": "Discourses II.10; Enchiridion 30"
        },
        {
            "id": "epictetus-kw-006",
            "thinker_id": "epictetus",
            "term": "토포스 (Topos)",
            "term_original": "τόπος (pl. τόποι)",
            "definition": (
                "수련 영역 또는 훈련 분야. 에픽테토스가 철학적 수련을 체계화한 세 영역: "
                "(1) 욕구와 혐오의 영역(자연학 대응), "
                "(2) 충동과 행위의 영역(윤리학 대응), "
                "(3) 동의와 판단의 영역(논리학 대응). "
                "이 순서대로 수련해야 하며, 에픽테토스 고유의 교육 체계다."
            ),
            "related_claims": ["epictetus-claim-004"],
            "source": "Discourses III.2.1-5; III.12.1-8"
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """에픽테토스 관계 데이터 입력."""
    relations = [
        {
            "id": "relation-musonius-epictetus",
            "from_thinker": "musonius_rufus",
            "to_thinker": "epictetus",
            "type": "influenced",
            "description": (
                "무소니우스 루푸스(Musonius Rufus, 기원후 20~101경)는 에픽테토스의 직접적인 스승이다. "
                "에픽테토스는 노예 시절 주인의 허락을 받아 무소니우스의 강의를 들었으며, "
                "실천 중심의 스토아 윤리학, 여성 교육 옹호 등에서 스승의 영향을 받았다. "
                "무소니우스의 저작도 제자 루키우스에 의해 기록되었다는 점에서 "
                "에픽테토스-아리아노스의 관계와 유사하다."
            ),
            "strength": "강함",
            "period": "1세기"
        },
        {
            "id": "relation-epictetus-marcus",
            "from_thinker": "epictetus",
            "to_thinker": "marcus_aurelius",
            "type": "influenced",
            "description": (
                "마르쿠스 아우렐리우스(Marcus Aurelius, 121~180)는 에픽테토스를 직접 만나지 않았으나, "
                "스승 유니우스 루스티쿠스(Junius Rusticus)로부터 에픽테토스의 '담론집'을 소개받아 "
                "깊은 영향을 받았다. '명상록'에서 에픽테토스를 여러 번 언급하며, "
                "이분법, 표상의 사용, 역할 윤리 등 에픽테토스의 핵심 개념을 자신의 사유에 통합했다."
            ),
            "strength": "강함",
            "period": "2세기"
        },
        {
            "id": "relation-chrysippus-epictetus",
            "from_thinker": "chrysippus",
            "to_thinker": "epictetus",
            "type": "influenced",
            "description": (
                "크리시포스(Chrysippus, 기원전 279~206)는 초기 스토아 학파의 체계를 완성한 철학자로, "
                "스토아 논리학, 인식론, 윤리학의 기본 틀을 제공했다. "
                "에픽테토스의 표상론(판타시아), 동의론(쉥카타테시스), 격정론(파토스)은 "
                "크리시포스의 이론적 기반 위에 서 있다. "
                "에픽테토스는 크리시포스를 존경하면서도 지나친 이론적 세련됨보다 실천을 강조했다."
            ),
            "strength": "보통",
            "period": "기원전 3세기 → 기원후 1~2세기"
        },
        {
            "id": "relation-epictetus-cbt",
            "from_thinker": "epictetus",
            "to_thinker": "cognitive_behavioral_therapy",
            "type": "influenced",
            "description": (
                "에픽테토스의 '사물이 아니라 판단이 괴롭힌다'는 원리는 "
                "현대 인지행동치료(CBT)의 직접적 선구다. "
                "알베르 엘리스(Albert Ellis)는 합리적 정서행동치료(REBT)를 개발할 때 "
                "에픽테토스를 명시적으로 인용했으며, "
                "아론 벡(Aaron Beck)의 인지치료(CT)도 동일한 통찰에 기반한다. "
                "에픽테토스는 고대 철학자 중 현대 심리치료에 가장 직접적 영향을 미친 인물이다."
            ),
            "strength": "강함",
            "period": "1~2세기 → 20세기"
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
    r = client.get(index=INDEX_THINKERS, id="epictetus")
    print(f"[thinker] epictetus: name={r['_source']['name_en']}, era={r['_source']['era']}")

    # works 확인
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "epictetus"}})
    print(f"[works] epictetus 저서 수: {works_count['count']}")
    works_result = client.search(
        index=INDEX_WORKS,
        query={"term": {"thinker_id": "epictetus"}},
        _source=["id", "title_original", "year"]
    )
    for hit in works_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['title_original']} ({s['year']})")

    # claims 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "epictetus"}})
    print(f"[claims] epictetus 주장 수: {claims_count['count']}")
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "epictetus"}},
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
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "epictetus"}})
    print(f"[keywords] epictetus 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_count = client.count(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "epictetus"}},
            {"term": {"to_thinker": "epictetus"}}
        ]}}
    )
    print(f"[relations] epictetus 관련 관계 수: {rel_count['count']}")
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "epictetus"}},
            {"term": {"to_thinker": "epictetus"}}
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
        print("=== 에픽테토스(Epictetus) 데이터 입력 시작 ===\n")

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
