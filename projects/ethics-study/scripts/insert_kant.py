"""임마누엘 칸트 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client, search_documents
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS
)


def insert_thinker(client):
    """임마누엘 칸트 사상가 데이터 입력."""
    doc = {
        "id": "kant",
        "name": "임마누엘 칸트",
        "name_en": "Immanuel Kant",
        "field": "western_ethics",
        "era": "근대",
        "birth_year": 1724,
        "death_year": 1804,
        "background": (
            "프로이센 쾨니히스베르크(현 러시아 칼리닌그라드)에서 마구 제조공의 아들로 태어났다. "
            "경건주의 신앙 환경에서 성장했으며, 쾨니히스베르크 대학에서 수학·물리학·철학을 공부했다. "
            "졸업 후 약 9년간 가정교사로 생활하다가 1755년 대학 강사(Privatdozent)가 되었고, "
            "1770년 쾨니히스베르크 대학 논리학·형이상학 정교수로 임용되었다. "
            "평생 쾨니히스베르크를 거의 떠나지 않았으나, 뉴턴 과학과 루소의 사상을 접하며 사상적 전환을 이루었다. "
            "'독사에게 물린 듯' 루소의 『에밀』을 읽고 산책을 포기했다는 일화가 유명하다. "
            "흄의 인과율 비판이 자신을 '독단적 선잠'에서 깨웠다고 고백했다. "
            "1781년 『순수이성비판』 출간으로 서양 철학사의 코페르니쿠스적 전회를 이루었으며, "
            "이후 비판 3부작과 도덕철학 저서들로 근대 철학의 정점을 이루었다."
        ),
        "core_philosophy": (
            "비판 철학(Kritische Philosophie)의 창시자. "
            "인식론에서 '코페르니쿠스적 전회'를 수행하여, 인식이 대상을 따르는 것이 아니라 대상이 인식 형식을 따른다고 주장했다. "
            "현상(Erscheinung)과 물자체(Ding an sich)의 구분, 순수이성의 이율배반 폭로를 통해 이성의 한계를 설정했다. "
            "도덕철학에서는 도덕성의 근거를 경험·감정·행복이 아닌 이성의 자율성(Autonomie)에서 찾았다. "
            "선의지(guter Wille)만이 무조건적으로 선하며, 도덕법칙은 정언명법(kategorischer Imperativ)으로 표현된다. "
            "세 가지 정식: (1) 보편법칙 정식, (2) 인간성 정식(목적 자체), (3) 자율성/목적의 왕국 정식. "
            "자유·신·영혼불사를 실천이성의 요청(Postulat)으로 정당화하여, 도덕과 종교의 관계를 새롭게 정립했다."
        ),
        "philosophical_journey": (
            "전비판기(1746~1769): 뉴턴 물리학에 기반한 자연과학적 저술, 라이프니츠-볼프 형이상학 수용. "
            "『일반 자연사와 천체론』(1755), 『신의 존재 증명의 유일 가능한 증거』(1763) 등. "
            "루소 수용(1760년대): 루소의 『에밀』과 『사회계약론』을 통해 자유·도덕·계몽의 문제로 관심 전환. "
            "침묵기(1770~1780): 『감성계와 지성계의 형식과 원리에 관하여』(1770) 이후 10년의 숙고. "
            "비판기(1781~1790): 『순수이성비판』(1781/1787), 『도덕형이상학 기초놓기』(1785), "
            "『실천이성비판』(1788), 『판단력비판』(1790)으로 비판 3부작 완성. "
            "후기(1793~1804): 『이성의 한계 안에서의 종교』(1793), 『도덕형이상학』(1797), "
            "『영구평화론』(1795), 미완성 『오푸스 포스투뭄』 등."
        ),
        "keywords": [
            "정언명법",
            "선의지",
            "자율성",
            "코페르니쿠스적 전회",
            "물자체",
            "실천이성",
            "목적의 왕국",
            "이성의 요청"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="kant", document=doc)
    print(f"[thinker] kant: {result['result']}")
    return result


def insert_works(client):
    """임마누엘 칸트 저서 데이터 입력."""
    works = [
        {
            "id": "kant-groundwork",
            "thinker_id": "kant",
            "title": "도덕형이상학 기초놓기",
            "title_original": "Grundlegung zur Metaphysik der Sitten",
            "year": 1785,
            "significance": (
                "칸트 도덕철학의 입문서이자 핵심 저작. "
                "도덕의 최고 원리를 탐구하여 정언명법(kategorischer Imperativ)을 세 가지 정식으로 제시한다. "
                "선의지, 의무, 도덕법칙, 자율성, 인간의 존엄성 등 칸트 윤리학의 핵심 개념이 집약되어 있다. "
                "윤리 임용시험에서 가장 빈출되는 칸트 저작. "
                "아카데미판 기준 4:387~463."
            ),
            "key_concepts": [
                "선의지", "정언명법", "보편법칙 정식", "인간성 정식",
                "목적의 왕국", "자율성", "의무", "도덕적 가치"
            ]
        },
        {
            "id": "kant-critique-pure-reason",
            "thinker_id": "kant",
            "title": "순수이성비판",
            "title_original": "Kritik der reinen Vernunft",
            "year": 1781,
            "significance": (
                "서양 철학사의 코페르니쿠스적 전회를 이룬 칸트의 주저. "
                "인식의 선험적 구조를 분석하고, 이성의 한계를 설정한다. "
                "현상과 물자체의 구분, 범주론, 순수이성의 이율배반이 핵심 내용이다. "
                "도덕적 자유의 가능성을 확보하기 위한 이론적 토대를 제공한다. "
                "초판(1781, A판)과 재판(1787, B판)이 있으며, 아카데미판 기준 B판 기준 인용."
            ),
            "key_concepts": [
                "코페르니쿠스적 전회", "물자체", "현상", "선험적 종합판단",
                "이율배반", "범주", "감성·오성·이성", "초월론적 관념론"
            ]
        },
        {
            "id": "kant-critique-practical-reason",
            "thinker_id": "kant",
            "title": "실천이성비판",
            "title_original": "Kritik der praktischen Vernunft",
            "year": 1788,
            "significance": (
                "칸트 도덕철학의 체계적 서술. "
                "도덕법칙의 선험적 성격, 자유의지, 최고선(summum bonum), "
                "실천이성의 요청(자유·신·영혼불사)을 체계적으로 논증한다. "
                "'이성의 사실(Faktum der Vernunft)'로서의 도덕법칙 개념을 제시하며, "
                "도덕적 감정으로서의 경외(Achtung)를 분석한다. "
                "아카데미판 기준 5:1~163."
            ),
            "key_concepts": [
                "도덕법칙", "자유의지", "최고선", "실천이성의 요청",
                "이성의 사실", "경외(Achtung)", "덕과 행복", "요청"
            ]
        },
        {
            "id": "kant-critique-judgment",
            "thinker_id": "kant",
            "title": "판단력비판",
            "title_original": "Kritik der Urteilskraft",
            "year": 1790,
            "significance": (
                "비판 3부작의 완결편. 미적 판단과 목적론적 판단을 분석한다. "
                "미적 판단의 보편적 타당성 주장, 숭고(das Erhabene)의 분석, "
                "자연의 합목적성 개념이 핵심이다. "
                "이론이성(자연)과 실천이성(자유) 사이의 가교 역할. "
                "아카데미판 기준 5:165~485."
            ),
            "key_concepts": [
                "미적 판단", "숭고", "합목적성", "반성적 판단력",
                "취미판단", "자연미", "도덕적 상징"
            ]
        },
        {
            "id": "kant-metaphysics-morals",
            "thinker_id": "kant",
            "title": "도덕형이상학",
            "title_original": "Metaphysik der Sitten",
            "year": 1797,
            "significance": (
                "칸트의 법 이론(법론)과 덕 이론(덕론)을 체계적으로 전개한 후기 실천철학의 정점. "
                "법론(Rechtslehre): 외적 자유의 원리로서 권리와 법의 체계. "
                "덕론(Tugendlehre): 의무론적 관점에서의 덕 개념, 자기 자신에 대한 의무, 타인에 대한 의무. "
                "아카데미판 기준 6:203~493."
            ),
            "key_concepts": [
                "법론", "덕론", "권리", "의무", "자기완성", "타인의 행복",
                "불완전한 의무", "완전한 의무"
            ]
        },
        {
            "id": "kant-perpetual-peace",
            "thinker_id": "kant",
            "title": "영구평화론",
            "title_original": "Zum ewigen Frieden",
            "year": 1795,
            "significance": (
                "국제 관계의 도덕적 기초를 논한 칸트의 정치철학 소론. "
                "공화국 체제, 국제 연맹, 세계시민법의 3가지 확정 조항을 통해 영구평화의 조건을 제시한다. "
                "현대 국제법과 국제연합(UN) 구상의 철학적 원형으로 평가된다. "
                "아카데미판 기준 8:341~386."
            ),
            "key_concepts": [
                "공화제", "국제 연맹", "세계시민법", "영구평화",
                "전쟁 금지", "주권 존중", "보편적 환대"
            ]
        },
        {
            "id": "kant-what-is-enlightenment",
            "thinker_id": "kant",
            "title": "계몽이란 무엇인가",
            "title_original": "Beantwortung der Frage: Was ist Aufklärung?",
            "year": 1784,
            "significance": (
                "계몽주의의 정수를 담은 짧은 에세이. "
                "'Sapere aude!(감히 알려고 하라!)' — 자신의 이성을 사용할 용기를 가지라는 계몽의 정신을 선언한다. "
                "미성년 상태(Unmündigkeit)에서 벗어나 스스로 생각하는 자율적 이성 사용을 강조한다. "
                "아카데미판 기준 8:33~42."
            ),
            "key_concepts": [
                "계몽", "Sapere aude", "미성년 상태", "이성의 공적 사용",
                "자율적 사유", "자유", "후견인"
            ]
        },
        {
            "id": "kant-religion-within-reason",
            "thinker_id": "kant",
            "title": "이성의 한계 안에서의 종교",
            "title_original": "Die Religion innerhalb der Grenzen der bloßen Vernunft",
            "year": 1793,
            "significance": (
                "칸트의 종교철학 주저. 도덕과 종교의 관계를 비판적으로 재구성한다. "
                "인간 본성의 근본악(das radikal Böse), 악에의 성향, 은혜와 자유의 관계를 분석한다. "
                "종교는 도덕의 명령을 신의 명령으로 이해하는 것이라는 도덕 신학적 입장을 제시한다. "
                "아카데미판 기준 6:1~202."
            ),
            "key_concepts": [
                "근본악", "악에의 성향", "도덕적 회심", "은혜",
                "교회 신앙 vs 이성 신앙", "도덕 신학"
            ]
        },
        {
            "id": "kant-lectures-ethics",
            "thinker_id": "kant",
            "title": "윤리학강의",
            "title_original": "Vorlesungen über Ethik (Collins, Kaehler, Vigilantius 등)",
            "year": 1780,
            "significance": (
                "칸트가 쾨니히스베르크 대학에서 행한 윤리학 강의 노트를 학생들이 필기한 것을 편집한 자료. "
                "비판기 이전 및 비판기 칸트의 윤리 사상 발전 과정을 보여준다. "
                "『도덕형이상학 기초놓기』와 함께 칸트 도덕철학의 상세한 내용을 담고 있다. "
                "아카데미판 기준 27권."
            ),
            "key_concepts": [
                "의무", "덕", "자기 자신에 대한 의무", "거짓말 금지",
                "자살 금지", "행복론 비판"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """임마누엘 칸트 핵심 주장 데이터 입력."""
    claims = [
        # ── CLAIM 001: 선의지 ──────────────────────────────────────
        {
            "id": "kant-claim-001",
            "thinker_id": "kant",
            "work_id": "kant-groundwork",
            "source_detail": "GMS 4:393 (도덕형이상학 기초놓기 제1장 첫 문장)",
            "claim": "선의지(guter Wille)만이 무조건적으로 선하다. 재능·기질·행운의 선물은 선의지 없이는 극도로 악할 수도 있다.",
            "original_text": (
                "Es ist überall nichts in der Welt, ja überhaupt auch außer derselben zu denken möglich, "
                "was ohne Einschränkung für gut könnte gehalten werden, als allein ein guter Wille."
            ),
            "explanation": (
                "칸트는 도덕적 가치의 유일한 원천으로 선의지를 제시한다. "
                "지성·용기·결단력·행복조차도 선의지가 없으면 오히려 악에 봉사할 수 있다. "
                "선의지는 결과나 성취가 아니라, 오직 의지 그 자체로서의 선함—즉 도덕법칙을 따르려는 의지—에서 성립한다. "
                "선의지의 가치는 어떤 목적의 달성에도 의존하지 않는다."
            ),
            "argument": (
                "경험적으로 선한 것들(재능, 행복 등)은 조건적으로만 선하다 — 잘못 사용되면 악이 된다. "
                "무조건적으로 선한 것은 어떤 조건 아래서도 선한 것이어야 한다. "
                "오직 도덕법칙에 따르려는 의지 — 선의지 — 만이 그 자체로, 어떤 결과와 무관하게 선하다. "
                "따라서 도덕적 가치의 유일한 원천은 결과나 경향성이 아니라 의지의 원리에 있다."
            ),
            "counterpoint": (
                "밀은 『공리주의(Utilitarianism)』 제2장에서 행위의 도덕적 가치는 행위자의 의도가 아니라 "
                "결과적으로 산출하는 행복의 양에 달려 있다고 주장하며, 의도만으로 도덕성을 평가하는 칸트식 접근을 비판했다. "
                "헤겔은 『법철학(Grundlinien der Philosophie des Rechts)』 §135~140에서 칸트의 선의지 개념이 "
                "공허한 형식주의에 그친다고 비판했다 — 구체적 사회적 맥락 없이 의지만으로는 도덕적 내용을 채울 수 없다는 것이다."
            ),
            "context": (
                "경험적 행복론(공리주의, 행복주의)을 비판하고, 도덕성의 근거를 순수 이성에서 찾기 위한 논의의 출발점이다."
            ),
            "keywords": ["선의지", "무조건적 선", "도덕적 가치", "경향성", "의무"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 002: 의무로부터의 행위 ─────────────────────────────
        {
            "id": "kant-claim-002",
            "thinker_id": "kant",
            "work_id": "kant-groundwork",
            "source_detail": "GMS 4:397~399 (도덕형이상학 기초놓기 제1장)",
            "claim": "도덕적 가치를 갖는 행위는 의무에 맞는 행위(pflichtmäßig)가 아니라 의무로부터 행해진 행위(aus Pflicht)이다.",
            "original_text": (
                "Eine Handlung aus Pflicht hat ihren moralischen Wert nicht in der Absicht, "
                "welche dadurch erreicht werden soll, sondern in der Maxime, nach der sie beschlossen wird."
            ),
            "explanation": (
                "칸트는 행위의 도덕적 가치를 결과나 동기의 종류(경향성)에서 찾지 않고, 행위의 준칙(Maxime)에서 찾는다. "
                "의무에 맞는 행위(pflichtmäßig): 의무가 요구하는 것과 일치하지만, 경향성이나 이기심에서 나온 행위. "
                "의무로부터의 행위(aus Pflicht): 오직 의무이기 때문에 행하는 행위 — 경향성이 아닌 도덕법칙 존중에서. "
                "상인이 정직하게 거스름돈을 주는 것은 장사에 유리해서이면 pflichtmäßig, "
                "고객을 속여서는 안 된다는 의무에서이면 aus Pflicht이다."
            ),
            "argument": (
                "경향성(욕구·감정·이익)에서 나온 행위는 상황에 따라 가변적이므로 보편적 도덕 원리의 근거가 될 수 없다. "
                "도덕법칙은 경험적 조건과 무관하게 타당해야 한다. "
                "따라서 도덕적 가치는 행위를 낳은 동기 — 오직 의무 의식(법칙에 대한 존경) — 에만 있을 수 있다. "
                "결과가 좋아도 잘못된 동기에서 나온 행위는 도덕적 가치를 갖지 않는다."
            ),
            "counterpoint": (
                "흄은 『도덕 원리 탐구(Enquiry Concerning the Principles of Morals)』 §1에서 "
                "이성만으로는 행위를 동기화할 수 없으며, 도덕의 최종 근거는 감정(공감·인류애)에 있다고 주장했다. "
                "공리주의는 동기보다 결과를 도덕 평가의 기준으로 삼아야 한다고 반박한다. "
                "아리스토텔레스는 『니코마코스 윤리학』 제2권에서 덕스러운 행위는 즐겁게, 적절한 감정과 함께 수행되어야 한다고 주장하며, "
                "의무 의식만을 강조하는 접근을 비판할 소지가 있다."
            ),
            "context": (
                "도덕성의 근거를 감정·경향성에서 찾는 영국 도덕 감각론(허치슨, 흄)과 행복론을 비판하고, "
                "순수 이성에 기반한 의무론 윤리학의 토대를 수립하기 위한 논의이다."
            ),
            "keywords": ["의무로부터의 행위", "pflichtmäßig", "aus Pflicht", "경향성", "준칙", "도덕적 동기"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 003: 정언명법 제1정식 (보편법칙) ────────────────────
        {
            "id": "kant-claim-003",
            "thinker_id": "kant",
            "work_id": "kant-groundwork",
            "source_detail": "GMS 4:421 (도덕형이상학 기초놓기 제2장)",
            "claim": "정언명법 제1정식(보편법칙 정식): 오직 네가 동시에 그것이 보편적 법칙이 되기를 원할 수 있는 준칙에 따라서만 행위하라.",
            "original_text": (
                "Handle nur nach derjenigen Maxime, durch die du zugleich wollen kannst, "
                "daß sie ein allgemeines Gesetz werde."
            ),
            "explanation": (
                "정언명법(kategorischer Imperativ)은 조건 없이, 무조건적으로 명령하는 도덕 명령이다. "
                "가언명법(hypothetischer Imperativ)이 '만약 X를 원한다면, Y를 하라'는 형식이라면, "
                "정언명법은 결과와 무관하게 '하라(혹은 하지 말라)'고 명령한다. "
                "보편법칙 정식은 자신의 행위 준칙(Maxime — 내가 따르는 주관적 원칙)을 보편화 가능 여부로 검증한다. "
                "거짓 약속의 준칙: '나는 필요할 때 지킬 의도 없이 약속하겠다'를 보편화하면 "
                "약속 제도 자체가 붕괴하므로, 이 준칙은 보편법칙이 될 수 없다."
            ),
            "argument": (
                "도덕법칙은 모든 이성적 존재에게 동일하게 타당해야 한다. "
                "나의 행위 원칙(준칙)이 모든 이성적 존재에게 보편적으로 적용될 수 있다면, 그 원칙은 도덕법칙과 일치한다. "
                "자기모순 검증: 보편화했을 때 자기모순이 발생하거나(완전한 의무), "
                "보편화를 원할 수 없는 준칙(불완전한 의무)은 도덕적으로 허용될 수 없다. "
                "이 검증은 순수 이성만으로 수행되므로 경험에 의존하지 않는다."
            ),
            "counterpoint": (
                "헤겔은 『법철학』 §135에서 보편화 가능성 검증만으로는 실질적 도덕 내용이 도출되지 않는다고 비판했다 — "
                "사유재산 없는 사회도 모순 없이 보편화될 수 있기 때문이다. "
                "밀은 『공리주의』 제1장에서 칸트가 결국 '결과를 고려하지 않을 수 없다'고 지적하며, "
                "보편화 가능성 기준이 암묵적으로 결과주의를 전제한다고 비판했다. "
                "W. D. Ross는 『옳음과 선(The Right and the Good)』(1930)에서 단일 원칙으로는 "
                "도덕적 의무들의 충돌을 해결할 수 없다며 '조건부 의무(prima facie duties)' 개념을 제시했다."
            ),
            "context": (
                "도덕법칙의 형식을 이성적으로 도출하기 위한 논의로, "
                "가언명법과 정언명법의 구분, 의무의 분류(완전/불완전 의무) 논의와 연결된다."
            ),
            "keywords": ["정언명법", "보편법칙 정식", "준칙", "가언명법", "완전한 의무", "불완전한 의무"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 004: 정언명법 제2정식 (인간성) ──────────────────────
        {
            "id": "kant-claim-004",
            "thinker_id": "kant",
            "work_id": "kant-groundwork",
            "source_detail": "GMS 4:429 (도덕형이상학 기초놓기 제2장)",
            "claim": "정언명법 제2정식(인간성 정식): 너의 인격과 다른 모든 사람의 인격에 있는 인간성을 항상 동시에 목적으로, 결코 단순히 수단으로만 사용하지 않도록 행위하라.",
            "original_text": (
                "Handle so, daß du die Menschheit sowohl in deiner Person, als in der Person eines jeden andern, "
                "jederzeit zugleich als Zweck, niemals bloß als Mittel brauchest."
            ),
            "explanation": (
                "이성적 존재(인간)는 그 자체로 절대적 가치(존엄성, Würde)를 지닌다. "
                "물건(Sache)은 가격(Preis)을 가지며 대체 가능하지만, 인격(Person)은 존엄성을 가지며 대체 불가능하다. "
                "'단순히 수단으로만'이 핵심: 인간을 수단으로 이용하는 것이 완전히 금지되는 것은 아니다(협력·서비스 등). "
                "금지되는 것은 인격을 '단순히(bloß)' 수단으로만, 즉 그 자신의 목적과 이성적 자율성을 무시한 채 이용하는 것이다."
            ),
            "argument": (
                "이성적 존재는 자신의 목적을 스스로 설정할 수 있는 자율적 존재이다. "
                "자율성(자기 입법 능력)이 바로 존엄성의 근거이다. "
                "이성적 존재를 단순한 도구로 취급하는 것은 그의 이성적 자율성을 무시하는 것이다. "
                "따라서 이성적 존재를 항상 목적으로 대우해야 한다는 요청은 이성의 자율성 개념에서 직접 도출된다."
            ),
            "counterpoint": (
                "피터 싱어는 『실천 윤리학(Practical Ethics)』(1979) 제3장에서 "
                "인간성 정식이 인간 이외의 이성적 존재(고등 동물)를 충분히 포괄하지 못하며, "
                "이익 평등 배려의 원칙이 더 포괄적인 도덕 기준이라고 비판했다. "
                "로버트 노직은 『아나키, 국가, 유토피아(Anarchy, State, and Utopia)』(1974)에서 "
                "인간성 정식을 지지하면서도 칸트적 의무론이 개인 권리의 절대성을 충분히 정초하지 못한다고 주장했다."
            ),
            "context": (
                "인간의 존엄성과 권리의 철학적 근거를 제공하는 논의로, "
                "인권 사상, 생명윤리, 사회정의 논의의 철학적 토대이다."
            ),
            "keywords": ["인간성 정식", "목적 자체", "수단", "존엄성", "인격", "인권"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 005: 정언명법 제3정식 (자율성/목적의 왕국) ─────────────
        {
            "id": "kant-claim-005",
            "thinker_id": "kant",
            "work_id": "kant-groundwork",
            "source_detail": "GMS 4:431~432, 438~439 (도덕형이상학 기초놓기 제2장)",
            "claim": "자율성(Autonomie)은 도덕법칙의 최고 원리이다. 이성적 존재들은 목적의 왕국(Reich der Zwecke)의 입법자이자 구성원이다.",
            "original_text": (
                "Autonomie des Willens ist die Beschaffenheit des Willens, dadurch derselbe ihm selbst "
                "(unabhängig von aller Beschaffenheit der Gegenstände des Wollens) ein Gesetz ist."
            ),
            "explanation": (
                "자율성(Autonomie): 의지가 외부의 강제나 경향성이 아닌, 자기 자신이 입법한 법칙에 따르는 것. "
                "타율성(Heteronomie): 의지가 외부 목적(행복, 신의 명령, 감정 등)에 의해 규정되는 것. "
                "타율적 도덕은 조건부 도덕(가언명법)에 불과하다. "
                "목적의 왕국(Reich der Zwecke): 모든 이성적 존재가 서로를 목적으로 대우하고 "
                "공동으로 도덕법칙을 입법하는 이상적 공동체의 이념."
            ),
            "argument": (
                "도덕법칙이 무조건적 구속력을 갖기 위해서는 외부 권위(신·국가·감정)에 의존할 수 없다. "
                "외부 권위에 의존하면, 그 권위가 없어지면 도덕도 사라지게 된다. "
                "이성적 존재는 자기 자신에게 도덕법칙을 부여(자기 입법)할 수 있는 유일한 존재이다. "
                "자율적으로 입법한 법칙에 따르는 것이야말로 진정한 자유이며 도덕의 근거이다."
            ),
            "counterpoint": (
                "밀은 『공리주의』에서 순수한 형식적 자율성만으로는 도덕 행위의 실질적 내용이 채워지지 않는다고 비판했다. "
                "니체는 『도덕의 계보학(Zur Genealogie der Moral)』(1887)에서 칸트의 자율성 개념이 "
                "금욕주의적 이상의 변형이자 스스로를 기만하는 자유 개념이라고 비판했다. "
                "크리스틴 코스가드(Christine Korsgaard)는 『규범성의 원천(The Sources of Normativity)』(1996)에서 "
                "칸트의 자율성 개념을 현대적으로 재구성하여 반성적 자기-구성 이론으로 발전시켰다."
            ),
            "context": (
                "자율성 개념은 타율적 도덕(쾌락주의, 신명론, 도덕 감각론)에 대한 비판을 담고 있으며, "
                "칸트 윤리학의 핵심 원리로서 세 가지 정식을 통합하는 개념이다."
            ),
            "keywords": ["자율성", "타율성", "목적의 왕국", "자기 입법", "이성적 존재", "도덕적 자유"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 006: 가언명법 vs 정언명법 ──────────────────────────
        {
            "id": "kant-claim-006",
            "thinker_id": "kant",
            "work_id": "kant-groundwork",
            "source_detail": "GMS 4:414~420 (도덕형이상학 기초놓기 제2장)",
            "claim": "명법에는 조건부 목적에 의존하는 가언명법과 무조건적으로 명령하는 정언명법이 있다. 도덕의 명법은 오직 정언명법이다.",
            "original_text": (
                "Alle Imperativen gebieten entweder hypothetisch oder kategorisch. "
                "Jene stellen die praktische Notwendigkeit einer möglichen Handlung als Mittel zu etwas anderm, "
                "was man will (oder doch möglich ist, daß man es wolle), vor. "
                "Der kategorische Imperativ würde der sein, der eine Handlung als für sich selbst, "
                "ohne Beziehung auf einen andern Zweck, als objektiv-notwendig vorstellte."
            ),
            "explanation": (
                "가언명법(hypothetischer Imperativ): '만약 X를 원한다면, Y를 하라'는 조건부 명령. "
                "숙련성의 규칙(특정 목적을 위한 기술적 조언)과 영리함의 충고(행복을 위한 실용적 조언)가 이에 해당한다. "
                "정언명법(kategorischer Imperativ): '(무조건) Y를 하라'는 무조건적 명령. "
                "도덕의 명법은 행복이나 이익과 무관하게 모든 이성적 존재에게 타당하므로 정언명법이어야 한다."
            ),
            "argument": (
                "가언명법은 목적에 조건부이므로, 그 목적을 원하지 않으면 구속력이 없다. "
                "도덕적 의무는 어떤 조건 아래서도 — 심지어 행복을 희생하더라도 — 타당해야 한다. "
                "따라서 도덕의 명법은 가언명법일 수 없고 정언명법이어야 한다."
            ),
            "counterpoint": (
                "공리주의는 도덕을 '최대 다수의 최대 행복'이라는 목적에 종속시키므로, "
                "칸트 관점에서는 고급 가언명법에 불과하다. "
                "아리스토텔레스의 덕 윤리학도 행복(에우다이모니아)을 궁극 목적으로 설정하므로 "
                "칸트적 의미에서는 타율적이다."
            ),
            "context": (
                "도덕 명령의 형식적 구분으로, 칸트 의무론의 출발점이 되는 분석이다."
            ),
            "keywords": ["가언명법", "정언명법", "의무", "조건부 명령", "숙련성", "영리함", "도덕성"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 007: 도덕법칙의 선험성 ────────────────────────────
        {
            "id": "kant-claim-007",
            "thinker_id": "kant",
            "work_id": "kant-groundwork",
            "source_detail": "GMS 4:389~392 (도덕형이상학 기초놓기 머리말)",
            "claim": "도덕형이상학은 경험적 원리를 일체 포함해서는 안 된다. 도덕법칙은 모든 이성적 존재에 타당하므로 경험에서 도출될 수 없다.",
            "original_text": (
                "Eine Metaphysik der Sitten... muß rein sein, "
                "d.i. von aller empirischen Kenntnis völlig gesäubert."
            ),
            "explanation": (
                "도덕법칙이 경험에서 도출된다면, 그것은 '지금까지 관찰된 인간의 행동 양식'에 불과하게 된다. "
                "경험적 도덕은 보편적 필연성을 가질 수 없다 — 예외가 있을 수 있기 때문이다. "
                "도덕법칙은 모든 이성적 존재(인간뿐 아니라 이성적 외계인이 있다면 그들에게도)에게 타당해야 한다. "
                "따라서 도덕법칙은 경험으로부터 독립된 선험적(a priori) 원리이어야 한다."
            ),
            "argument": (
                "경험은 개연적이고 상대적인 것만 보여준다. "
                "도덕적 당위('~해야 한다')는 사실('~이다')과 다르다 — 흄의 is-ought 문제와 관련. "
                "보편적·필연적 도덕법칙은 경험을 초월한 이성의 순수한 산물이어야 한다. "
                "인류학·심리학은 도덕철학의 도구적 자료일 수 있지만, 도덕의 원리를 제공하지는 않는다."
            ),
            "counterpoint": (
                "흄은 『인간 본성론(A Treatise of Human Nature)』 3권에서 "
                "도덕의 근거는 이성이 아닌 감정(도덕 감각)이라고 주장했다. "
                "존 롤스는 『정의론(A Theory of Justice)』(1971) §9에서 칸트의 형이상학적 전제 없이도 "
                "'도덕의 선험성'을 절차적으로 재구성할 수 있다고 보았다."
            ),
            "context": (
                "당시 독일에서 유행한 경험주의적 도덕 인류학(행복론)과 영국 도덕 감각론에 대한 비판이다."
            ),
            "keywords": ["도덕법칙의 선험성", "경험 독립성", "보편적 도덕", "a priori", "도덕형이상학"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 008: 도덕적 감정 — 경외(Achtung) ───────────────────
        {
            "id": "kant-claim-008",
            "thinker_id": "kant",
            "work_id": "kant-critique-practical-reason",
            "source_detail": "KpV 5:71~89 (실천이성비판 제1부 제3장 순수실천이성의 동기론)",
            "claim": "도덕적 감정으로서의 경외(Achtung, 존경/경외감)는 도덕법칙 자체에 의해 이성이 직접 산출한 감정이다. 이것만이 도덕의 유일한 동기이다.",
            "original_text": (
                "Achtung fürs moralische Gesetz ist also die einzige und zugleich unbezweifelte moralische Triebfeder, "
                "so wie dieses Gefühl auch auf kein Objekt, als lediglich aus diesem Grunde gerichtet wird."
            ),
            "explanation": (
                "칸트는 도덕에서 감정을 원칙적으로 배제하지 않는다 — 다만 경향성에서 나온 감정은 도덕의 근거가 될 수 없다. "
                "경외(Achtung)는 경향성이나 외부 대상에 의해 촉발되는 감정이 아니라, "
                "도덕법칙의 위대함을 이성이 인식할 때 자연히 발생하는 감정이다. "
                "이 경외감은 자아(경향성적 자아)를 굴복시키는 부정적 측면과 "
                "도덕법칙에 대한 숭고한 존중이라는 긍정적 측면을 동시에 갖는다."
            ),
            "argument": (
                "경향성(쾌락, 이익, 동정 등)에서 나온 동기는 도덕의 충분한 근거가 될 수 없다 — 가변적이고 조건부이기 때문이다. "
                "그러나 이성적 존재인 인간은 자신이 도덕법칙의 요구를 인식할 때, "
                "자신의 경향적 자아를 억제하는 고통과 동시에 도덕법칙에 대한 경외를 느낀다. "
                "이 경외는 이성의 자율성에서 비롯되므로 선험적 도덕 감정이며, 유일한 도덕적 동기이다."
            ),
            "counterpoint": (
                "아리스토텔레스는 『니코마코스 윤리학』 제2권 제3장에서 "
                "덕스러운 행위는 고통 없이, 기꺼이 즐겁게 수행되어야 한다고 주장했다. "
                "칸트에서 도덕적 행위가 항상 경향성과의 투쟁을 전제하는 것처럼 보이는 점을 비판했다. "
                "쉴러(Friedrich Schiller)는 『우아함과 품위에 관하여(Über Anmut und Würde)』(1793)에서 "
                "의무와 경향성이 일치하는 '아름다운 영혼(schöne Seele)'의 이상을 제시하며, "
                "의무와 경향성의 갈등을 과장하는 칸트 윤리학을 비판했다."
            ),
            "context": (
                "도덕 감각론(허치슨, 흄)의 감정 윤리학을 비판하면서도, "
                "순수 이성에서 도출된 특수한 도덕 감정으로서 경외를 인정하는 균형 잡힌 논의이다."
            ),
            "keywords": ["경외", "Achtung", "도덕적 감정", "도덕적 동기", "경향성과 의무", "존경"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 009: 이성의 사실 (Faktum der Vernunft) ─────────────
        {
            "id": "kant-claim-009",
            "thinker_id": "kant",
            "work_id": "kant-critique-practical-reason",
            "source_detail": "KpV 5:31~32, 42~43 (실천이성비판 제1부 제1편 제1장)",
            "claim": "도덕법칙은 순수 실천이성의 사실(Faktum der reinen praktischen Vernunft)이다. 이것은 연역될 수 없으며, 이성적 존재라면 누구나 직접 의식한다.",
            "original_text": (
                "Das Bewußtsein dieses Grundgesetzes kann man ein Faktum der Vernunft nennen, "
                "weil man es nicht aus vorhergehenden Daten der Vernunft, z.B. dem Bewußtsein der Freiheit, "
                "herausvernünfteln kann, sondern weil es sich für sich selbst uns aufdringt."
            ),
            "explanation": (
                "『도덕형이상학 기초놓기』에서 칸트는 도덕법칙을 자유 개념에서 연역하려 했지만, "
                "『실천이성비판』에서는 도덕법칙이 이성 그 자체의 직접적 사실임을 주장한다. "
                "이성의 사실은 선험적 종합판단처럼 논리적으로 증명될 수 없지만, "
                "이성적 존재라면 누구나 자신에게 도덕법칙이 부과됨을 의식한다. "
                "이 도덕법칙 의식으로부터 역으로 자유의 실재성이 확보된다."
            ),
            "argument": (
                "도덕법칙의 구속력은 논리적 증명이나 경험적 근거에서 나오는 것이 아니다. "
                "우리는 자신이 어떤 행위를 해야 한다는 당위를 직접 의식한다 — 이것이 이성의 사실이다. "
                "이 사실은 연역될 수 없지만 부정될 수도 없다. "
                "도덕법칙의 의식이 가능하기 위해서는 의지의 자유가 있어야 하므로, 자유의 실재성이 실천적으로 확보된다."
            ),
            "counterpoint": (
                "J. G. 피히테는 『전체 지식론의 기초(Grundlage der gesamten Wissenschaftslehre)』(1794)에서 "
                "'이성의 사실' 개념이 충분히 설명되지 않았다고 비판하며, "
                "자아(Ich)의 자기 정립에서 도덕법칙을 연역하려 했다. "
                "현대의 헤르만 코헨(Hermann Cohen)은 칸트의 이성의 사실이 '사실(Tatsache)' 대신 "
                "'행위-사실(Tathandlung)'로 이해되어야 한다고 재해석했다."
            ),
            "context": (
                "도덕법칙의 정당화 문제를 다루는 핵심 개념으로, "
                "『도덕형이상학 기초놓기』에서 『실천이성비판』으로의 칸트 사상 발전을 보여준다."
            ),
            "keywords": ["이성의 사실", "Faktum der Vernunft", "도덕법칙의 의식", "자유의 연역", "실천이성"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 010: 자유와 도덕법칙 ─────────────────────────────
        {
            "id": "kant-claim-010",
            "thinker_id": "kant",
            "work_id": "kant-critique-practical-reason",
            "source_detail": "KpV 5:4, 29~30 (실천이성비판 머리말·제1부 제1장)",
            "claim": "자유(Freiheit)는 도덕법칙의 존재 근거(ratio essendi)이며, 도덕법칙은 자유의 인식 근거(ratio cognoscendi)이다. 자유와 도덕법칙은 상호 함축한다.",
            "original_text": (
                "Freiheit und unbedingte praktische Gesetz weisen also wechselseitig aufeinander zurück. "
                "...das moralische Gesetz ist der Erkenntnisgrund der Freiheit."
            ),
            "explanation": (
                "순수이성비판에서 자유는 이론적으로 증명될 수 없고 단지 이율배반(제3이율배반)의 맥락에서 '가능성'으로 남겨졌다. "
                "실천이성비판에서 도덕법칙(이성의 사실)이 주어지면, "
                "그 도덕법칙에 따를 수 있으려면 자유가 있어야 한다는 논증으로 자유의 실재성이 확보된다. "
                "자유(선험적 자유)는 자연 인과의 사슬을 벗어나 도덕법칙에 따라 행위를 시작할 수 있는 능력이다."
            ),
            "argument": (
                "우리는 도덕법칙(이성의 사실)을 의식한다. "
                "도덕법칙은 '~해야 한다(Sollen)'는 당위를 부과한다. "
                "당위는 '할 수 있음(Können)'을 함축한다 — 자유가 없다면 당위는 의미가 없다. "
                "따라서 도덕법칙 의식에서 자유의 실재성이 실천적으로 확보된다. "
                "역으로, 자유가 실재하기 때문에 도덕법칙이 존재할 수 있다."
            ),
            "counterpoint": (
                "스피노자는 『윤리학(Ethica)』(1677) 제1부에서 모든 것은 필연적 인과 법칙에 따르며 "
                "자유의지는 무지의 결과라고 주장했다. "
                "현대 신경과학(리벳 실험 등)은 의지 결정이 의식적 결정보다 선행한다는 증거를 제시하며 "
                "자유의지의 실재성에 도전한다."
            ),
            "context": (
                "이론이성(자연 인과)과 실천이성(자유) 사이의 긴장을 해소하는 논의로, "
                "칸트 철학 전체의 핵심 구조를 이해하는 데 필수적이다."
            ),
            "keywords": ["자유", "도덕법칙", "ratio essendi", "ratio cognoscendi", "선험적 자유", "자연인과"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 011: 최고선과 실천이성의 요청 ──────────────────────
        {
            "id": "kant-claim-011",
            "thinker_id": "kant",
            "work_id": "kant-critique-practical-reason",
            "source_detail": "KpV 5:107~134 (실천이성비판 제2부 변증론)",
            "claim": "최고선(das höchste Gut)은 덕(Tugend)과 그에 비례하는 행복(Glückseligkeit)의 결합이다. 최고선의 실현 가능성을 위해 영혼불사와 신의 존재가 실천이성의 요청으로 필요하다.",
            "original_text": (
                "Das höchste Gut in einer Welt ist möglich, ist das erste Postulat der reinen praktischen Vernunft. "
                "...Gott und die Unsterblichkeit der Seele sind Postulate der reinen praktischen Vernunft."
            ),
            "explanation": (
                "칸트는 도덕의 동기가 행복이어서는 안 된다고 주장하면서도, "
                "덕스러운 자가 행복하게 되는 상태(최고선)가 실현 가능해야 한다고 본다. "
                "그러나 현세에서 덕과 행복의 필연적 연결은 보장되지 않는다. "
                "따라서 최고선의 실현을 위해 실천이성은 세 가지를 요청(Postulat)한다: "
                "(1) 영혼불사: 완전한 덕성(신성성)을 향한 무한한 진보를 위해 필요. "
                "(2) 신의 존재: 덕에 비례한 행복을 보장할 수 있는 도덕적 세계 창시자. "
                "(3) 자유: 이미 앞에서 확보됨."
            ),
            "argument": (
                "이성은 최고선을 추구하도록 우리에게 명한다. "
                "최고선이 실현 가능하지 않다면 도덕법칙의 명령 자체가 불합리해진다. "
                "현세에서 최고선의 완전한 실현은 불가능하므로, 무한한 시간(영혼불사)과 "
                "자연과 자유를 연결하는 도덕적 주재자(신)가 필요하다. "
                "이것들은 이론적 인식이 아니라 실천적 필요에 의한 요청이다."
            ),
            "counterpoint": (
                "헤겔은 『정신현상학(Phänomenologie des Geistes)』(1807) '도덕성' 장에서 "
                "칸트의 최고선 논증이 '도덕적 세계관'의 내부 모순을 드러낸다고 비판했다 — "
                "도덕법칙과 행복의 화해는 단순한 '요청'이 아니라 역사적 정신의 자기 실현을 통해 이루어진다. "
                "밀은 도덕의 목적이 행복이어야 하므로, 덕이 행복에 봉사할 때 의미가 있다고 주장하며 "
                "덕과 행복의 긴장을 칸트식으로 처리하는 것에 반대했다."
            ),
            "context": (
                "칸트의 도덕 신학과 종교철학의 토대이며, "
                "도덕이 신앙의 근거가 되는 구조('도덕에서 신으로')를 설명한다."
            ),
            "keywords": ["최고선", "실천이성의 요청", "영혼불사", "신의 존재", "덕과 행복", "요청"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 012: 코페르니쿠스적 전회 ─────────────────────────
        {
            "id": "kant-claim-012",
            "thinker_id": "kant",
            "work_id": "kant-critique-pure-reason",
            "source_detail": "KrV B xvi (순수이성비판 재판 서문)",
            "claim": "인식이 대상을 따르는 것이 아니라 대상이 인식 주체의 선험적 형식을 따른다 — 이것이 코페르니쿠스적 전회이다.",
            "original_text": (
                "Man versuche es daher einmal, ob wir nicht in den Aufgaben der Metaphysik damit besser fortkommen, "
                "daß wir annehmen, die Gegenstände müssen sich nach unserem Erkenntnis richten."
            ),
            "explanation": (
                "전통 인식론: 인식은 대상을 있는 그대로 파악하는 것(인식이 대상에 맞춰짐). "
                "칸트의 전회: 우리가 경험하는 대상은 이미 인식 주체의 선험적 형식(시간·공간이라는 직관 형식, "
                "오성의 범주들)에 의해 구성된다. "
                "물자체(Ding an sich): 우리의 인식 형식과 무관하게 존재하는 것이지만, "
                "우리는 그것을 직접 인식할 수 없고 오직 현상(Erscheinung)만을 인식한다. "
                "이 전회는 형이상학의 전통적 주장들(신·자유·영혼불사의 이론적 인식)을 불가능하게 만들면서도, "
                "도덕적 자유의 가능성을 현상계 너머에 확보한다."
            ),
            "argument": (
                "전통 형이상학은 경험을 넘어선 영역(물자체)에 대한 인식을 주장하다가 이율배반에 빠진다. "
                "인식 대상이 인식 형식에 따른다고 전제하면, 선험적 종합판단(수학·자연과학)의 가능성이 설명된다. "
                "이 전제는 이성의 한계도 설정한다 — 인식 형식을 벗어난 영역(물자체)은 인식 불가능하다."
            ),
            "counterpoint": (
                "헤겔은 『정신현상학』 서문에서 칸트가 인식의 도구(범주)를 사용하기 전에 그 도구를 검사하려는 것은 "
                "헤엄치기 전에 헤엄치는 법을 배우려는 것과 같다고 비판했다. "
                "물자체 개념에 대해서는 야코비(Friedrich Heinrich Jacobi)가 "
                "'물자체 없이는 칸트 철학에 들어갈 수 없고, 물자체와 함께는 머물 수 없다'고 비판했다."
            ),
            "context": (
                "근대 인식론 논쟁(합리론 vs 경험론)의 종합이며, "
                "형이상학을 새롭게 정립하고 도덕적 자유의 영역을 확보하기 위한 이론적 토대이다."
            ),
            "keywords": ["코페르니쿠스적 전회", "물자체", "현상", "선험적 형식", "초월론적 관념론", "인식론"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 013: 근본악 ──────────────────────────────────────
        {
            "id": "kant-claim-013",
            "thinker_id": "kant",
            "work_id": "kant-religion-within-reason",
            "source_detail": "Rel. 6:29~44 (이성의 한계 안에서의 종교 제1편)",
            "claim": "인간 본성에는 도덕법칙보다 자기 사랑(경향성)을 우선시하는 근본악(das radikal Böse)의 성향이 있다. 이것은 선천적이지만 자유로운 행위에 귀속된다.",
            "original_text": (
                "Der Mensch ist böse, d.i. er nimmt das Bewußtsein des moralischen Gesetzes... "
                "doch in seine Maxime auf, aber er hat auch eine Neigung, Ausnahmen davon zu machen. "
                "...Diese Gebrechlichkeit der menschlichen Natur heißt das radikal Böse."
            ),
            "explanation": (
                "칸트는 인간이 단순히 '자연적으로 악하다'고 말하는 것이 아니다. "
                "인간은 도덕법칙을 알면서도 이를 경향성(자기 사랑)에 종속시키는 성향을 갖는다. "
                "악의 세 단계: (1) 연약함(Gebrechlichkeit): 옳은 것을 알지만 실천이 약하다. "
                "(2) 불순함(Unlauterkeit): 의무에서 행동하지만 감춰진 동기가 섞여 있다. "
                "(3) 사악함(Bösartigkeit/Verderbtheit): 법칙보다 경향성을 의식적으로 우선시한다. "
                "'근본(radikal)'은 자유로운 행위의 가장 깊은 근거에 있다는 뜻."
            ),
            "argument": (
                "인간에게 선에의 소질(Anlage zum Guten)이 있음에도 악한 행위가 보편적으로 관찰된다. "
                "이 악은 단순한 동물성(본능)에서 오는 것이 아니라, 자유로운 의지의 잘못된 선택에서 온다. "
                "따라서 악은 도덕적 책임이 귀속될 수 있다(자연적 필연성이 아니므로). "
                "이 악을 극복하기 위해서는 도덕적 혁명(심성의 전환)이 필요하며, 이것은 이성의 자율성으로 가능하다."
            ),
            "counterpoint": (
                "루소는 『에밀(Émile)』(1762) 제1권에서 인간은 본래 선하게 태어났으나 사회가 인간을 타락시킨다고 주장했다. "
                "칸트의 근본악론은 루소의 낙관적 인간 본성론에 대한 비판적 수정이라 볼 수 있다. "
                "아우구스티누스는 『신국론(De Civitate Dei)』에서 원죄(peccatum originale)로 인한 인간의 악을 주장했는데, "
                "칸트는 이를 신학적 원죄가 아닌 도덕철학적 용어로 재해석한다."
            ),
            "context": (
                "도덕적 회심(Gesinnungsänderung)과 도덕 교육의 필요성을 논하기 위한 맥락이며, "
                "칸트의 종교철학과 도덕 교육론의 출발점이다."
            ),
            "keywords": ["근본악", "악에의 성향", "연약함", "불순함", "사악함", "도덕적 회심", "자유와 악"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 014: 영구평화론 ────────────────────────────────
        {
            "id": "kant-claim-014",
            "thinker_id": "kant",
            "work_id": "kant-perpetual-peace",
            "source_detail": "ZeF 8:349~360 (영구평화론 확정 조항들)",
            "claim": "영구평화를 위한 세 가지 확정 조항: (1) 모든 국가의 시민적 체제는 공화제여야 한다. (2) 국제법은 자유로운 국가들의 연맹에 기초해야 한다. (3) 세계시민법은 보편적 우호(환대) 조건에 한정되어야 한다.",
            "original_text": (
                "1. Die bürgerliche Verfassung in jedem Staat soll republikanisch sein. "
                "2. Das Völkerrecht soll auf einen Föderalism freier Staaten gegründet sein. "
                "3. Das Weltbürgerrecht soll auf Bedingungen der allgemeinen Hospitalität eingeschränkt sein."
            ),
            "explanation": (
                "칸트는 영구평화가 이상에 불과하지 않고 실현 가능한 목표임을 주장한다. "
                "공화제: 입법·집행이 분리되고 법의 지배가 이루어지는 체제 — 전쟁 결정이 시민 동의를 필요로 하므로 신중. "
                "자유 국가들의 연맹(Völkerbund): 국가들이 자신의 주권을 포기하지 않고도 평화를 위해 협력. "
                "세계시민적 환대(hospitality): 외국인이 타국 영토에서 적대적으로 취급받지 않을 권리 — "
                "이민·망명의 권리가 아닌, 교류의 기초 조건."
            ),
            "argument": (
                "전쟁은 자연 상태의 연장이며, 이성은 평화 상태를 의무로 부과한다. "
                "공화제 국가는 전쟁 결정에 시민의 동의를 요하므로 전쟁을 자제하게 된다. "
                "국가들의 연맹은 강압적 세계 국가 없이도 국제적 법치를 가능하게 한다. "
                "세계시민적 교류는 인류가 하나의 도덕적 공동체로 발전하는 기반이다."
            ),
            "counterpoint": (
                "헤겔은 『법철학』 §333~340에서 칸트의 국가 연맹이 실질적 강제력 없이는 공허한 이상에 불과하다고 비판했다. "
                "현실 국제관계에서 전쟁은 세계정신이 역사를 통해 자신을 실현하는 방식이기도 하다고 보았다. "
                "슈미트(Carl Schmitt)는 『정치적인 것의 개념(Der Begriff des Politischen)』(1932)에서 "
                "칸트식 세계시민적 평화론이 정치의 고유한 적-동지 구별을 무시한다고 비판했다."
            ),
            "context": (
                "프랑스 혁명 이후 유럽 전쟁이 격화되던 시기(1795년)에 쓰인 정치철학 소론으로, "
                "현대 국제법·UN·EU 구상의 철학적 선구로 평가된다."
            ),
            "keywords": ["영구평화", "공화제", "국가 연맹", "세계시민법", "환대", "국제 윤리"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 015: 계몽 ───────────────────────────────────────
        {
            "id": "kant-claim-015",
            "thinker_id": "kant",
            "work_id": "kant-what-is-enlightenment",
            "source_detail": "WA 8:35 (계몽이란 무엇인가 첫 문단)",
            "claim": "계몽(Aufklärung)은 인간이 스스로 초래한 미성년 상태(Unmündigkeit)에서 벗어나는 것이다. '감히 알려고 하라(Sapere aude)!' — 이것이 계몽의 표어이다.",
            "original_text": (
                "Aufklärung ist der Ausgang des Menschen aus seiner selbst verschuldeten Unmündigkeit. "
                "Unmündigkeit ist das Unvermögen, sich seines Verstandes ohne Leitung eines anderen zu bedienen. "
                "Selbstverschuldet ist diese Unmündigkeit, wenn die Ursache derselben nicht am Mangel des Verstandes, "
                "sondern der Entschließung und des Mutes liegt, sich seiner ohne Leitung eines andern zu bedienen. "
                "Sapere aude! Habe Mut, dich deines eigenen Verstandes zu bedienen! "
                "ist also der Wahlspruch der Aufklärung."
            ),
            "explanation": (
                "미성년 상태(Unmündigkeit): 타인의 안내 없이 자신의 이성을 사용하지 못하는 상태. "
                "'스스로 초래한(selbstverschuldet)': 이성이 부족한 것이 아니라, 결단과 용기가 없기 때문. "
                "이성의 공적 사용(öffentlicher Gebrauch der Vernunft): 학자로서 공개 강연·저술에서 이성을 자유롭게 사용. "
                "이성의 사적 사용(privater Gebrauch der Vernunft): 특정 직위·역할에서의 복종 — 군인·공무원 등. "
                "칸트는 공적 사용의 자유를 보장하는 계몽된 전제군주(프리드리히 대왕)를 지지했다."
            ),
            "argument": (
                "인간은 이성을 갖고 있지만, 편의·두려움·게으름으로 타인(후견인)에게 의존한다. "
                "이 미성년 상태는 타고난 것이 아니라 선택의 결과이므로 극복 가능하다. "
                "자유로운 이성의 공적 사용이 허용된다면, 사회 전체가 점진적으로 계몽된다. "
                "계몽은 단순한 지식 증가가 아니라 자율적 사유 능력의 실현이다."
            ),
            "counterpoint": (
                "푸코는 『계몽이란 무엇인가(What is Enlightenment?)』(1984)에서 칸트의 계몽 개념을 "
                "비판적으로 계승하면서도, 계몽이 권력-지식 체계와 결부되어 새로운 형태의 통제를 낳을 수 있음을 지적했다. "
                "아도르노와 호르크하이머는 『계몽의 변증법(Dialektik der Aufklärung)』(1947)에서 "
                "계몽이성이 도구적 이성으로 전락하여 지배와 통제의 수단이 되었다고 비판했다."
            ),
            "context": (
                "1784년 베를린 월간지의 '계몽이란 무엇인가?' 논쟁에 답하는 형식으로 쓰인 글로, "
                "칸트의 정치철학·교육철학의 핵심을 담고 있다."
            ),
            "keywords": ["계몽", "Sapere aude", "미성년 상태", "이성의 공적 사용", "자율성", "자유"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 016: 인간의 존엄성과 가격 없는 존엄 ──────────────────
        {
            "id": "kant-claim-016",
            "thinker_id": "kant",
            "work_id": "kant-groundwork",
            "source_detail": "GMS 4:434~436 (도덕형이상학 기초놓기 제2장)",
            "claim": "도덕법칙을 따를 수 있는 이성적 존재는 가격(Preis)이 아닌 존엄성(Würde)을 지닌다. 존엄성은 어떤 등가물로도 대체될 수 없는 무조건적 가치이다.",
            "original_text": (
                "Was einen Preis hat, an dessen Stelle kann auch etwas anderes als Äquivalent gesetzt werden; "
                "was dagegen über allen Preis erhaben ist, mithin kein Äquivalent verstattet, das hat eine Würde."
            ),
            "explanation": (
                "가격(Preis): 등가 교환이 가능한 상대적 가치. "
                "시장 가격(Marktpreis): 필요와 공급에 의해 결정되는 가치. "
                "감동 가격(Affektionspreis): 감정적 취향에 의해 결정되는 가치. "
                "존엄성(Würde): 어떤 것과도 비교·교환될 수 없는 절대적 가치. "
                "자율적 이성 존재만이 도덕법칙을 스스로 입법할 수 있으므로, "
                "그 자율성이 존엄성의 근거이다."
            ),
            "argument": (
                "덕과 도덕법칙에 대한 적합성은 어떤 경향성의 충족보다도 높이 평가되어야 한다. "
                "이 탁월성(덕의 탁월성)은 어떤 가격과도 비교될 수 없다. "
                "이성적 존재는 자연의 목적(본능, 욕구)에 종속되지 않고 자신의 목적을 설정할 수 있다. "
                "이 자율적 목적 설정 능력 자체가 존엄성의 원천이다."
            ),
            "counterpoint": (
                "싱어는 『실천 윤리학』에서 칸트의 존엄성 개념이 인간에게만 무조건적 가치를 부여하는 종차별주의(speciesism)라고 비판했다. "
                "감각 능력이 있는 동물도 이익 평등 배려의 대상이 되어야 한다고 주장했다. "
                "마르크스는 『자본론(Das Kapital)』(1867)에서 자본주의 체제가 모든 가치를 교환 가치로 환원시켜 "
                "인간 노동과 인격을 상품화한다고 비판했다 — 칸트의 존엄성 개념과 대화 가능한 맥락."
            ),
            "context": (
                "인간 권리, 노예제 비판, 생명윤리(인간 대상 실험 등)의 철학적 근거로서, "
                "현대 인권 사상의 가장 중요한 철학적 원천 중 하나이다."
            ),
            "keywords": ["존엄성", "Würde", "가격", "이성적 존재", "대체 불가능성", "인권의 근거"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 017: 거짓말 금지 절대성 ──────────────────────────
        {
            "id": "kant-claim-017",
            "thinker_id": "kant",
            "work_id": "kant-metaphysics-morals",
            "source_detail": "MS 6:429~431 (도덕형이상학 덕론 제9절); 『진실을 말할 의무에 관하여』(1797) 8:425~430",
            "claim": "거짓말은 어떤 경우에도 허용되지 않는다. 살인자가 피해자의 위치를 물어볼 때조차 진실을 말해야 한다.",
            "original_text": (
                "Die Lüge ist Wegwerfung und gleichsam Vernichtung seiner Menschenwürde. "
                "Wahrhaftigkeit in Aussagen, die man nicht umgehen kann, ist formale Pflicht des Menschen gegen jeden."
            ),
            "explanation": (
                "거짓말의 준칙은 보편화될 수 없다 — '모든 사람이 거짓말을 한다'면 진술의 의미 자체가 붕괴한다. "
                "거짓말은 타인의 이성적 자율성을 침해하고 언어·소통의 기반인 신뢰를 파괴한다. "
                "또한 거짓말은 자기 인간성(Menschenwürde)의 자기 부정이다. "
                "칸트는 살인자에게도 진실을 말해야 한다고 주장하여 많은 비판을 받았지만, "
                "이 입장은 도덕법칙의 절대성에 대한 그의 일관된 견해를 보여준다."
            ),
            "argument": (
                "거짓말의 준칙: '나는 필요할 때 거짓말을 하겠다'를 보편화하면 진술의 신뢰성이 붕괴한다. "
                "거짓말을 하면 상대방의 이성적 자율성을 침해한다 — 상대방이 잘못된 믿음 아래 결정하게 된다. "
                "결과가 좋더라도(살인자를 속여 피해자를 구함) 거짓말 자체의 도덕적 잘못은 사라지지 않는다."
            ),
            "counterpoint": (
                "벤자맹 콩스탕(Benjamin Constant)은 『정치적 반동에 관하여』(1797)에서 "
                "진실을 들을 권리는 그것을 들을 자격이 있는 사람에게만 있으므로, "
                "살인자에게 진실을 말할 의무는 없다고 비판했다. "
                "W. D. Ross는 『옳음과 선』에서 진실을 말할 의무와 생명을 구할 의무가 충돌할 때 "
                "후자가 더 강한 조건부 의무(prima facie duty)일 수 있다고 주장했다."
            ),
            "context": (
                "콩스탕의 비판에 대한 직접 답변으로 쓰인 글이며, "
                "칸트 의무론의 절대주의적 성격과 도덕적 딜레마 문제를 선명하게 드러내는 사례이다."
            ),
            "keywords": ["거짓말 금지", "절대적 의무", "진실성", "완전한 의무", "도덕적 딜레마", "보편법칙"],
            "verified": False,
            "verification_log": []
        },
        # ── CLAIM 018: 행복은 도덕의 동기가 될 수 없다 ──────────────────
        {
            "id": "kant-claim-018",
            "thinker_id": "kant",
            "work_id": "kant-critique-practical-reason",
            "source_detail": "KpV 5:21~26, 59~65 (실천이성비판 제1부 제1편 제3장)",
            "claim": "행복 원리를 도덕의 기초로 삼는 것은 도덕성을 파괴한다. 행복은 도덕의 동기가 아니라 최고선에서 덕에 비례하는 결과로서만 정당화된다.",
            "original_text": (
                "Das Prinzip der eigenen Glückseligkeit ist das verderblichste nicht bloß darum, "
                "weil es falsch ist und die Erfahrung seiner Widerlegung die Behauptung widerspricht... "
                "sondern weil es Moralität untergräbt."
            ),
            "explanation": (
                "행복주의 비판: 행복(쾌락, 이익)을 도덕의 기초로 삼으면 도덕법칙은 가언명법이 된다. "
                "'행복해지길 원한다면 X를 하라'는 조건부 명령은 진정한 도덕이 아니다. "
                "또한 행복은 경험적 개념으로, 사람마다 다르게 정의되므로 보편적 도덕의 근거가 될 수 없다. "
                "칸트는 행복 자체를 부정하는 것이 아니라, 행복을 도덕의 근거로 삼는 것을 비판한다. "
                "최고선에서 행복은 덕에 비례하는 결과로 허용된다."
            ),
            "argument": (
                "행복은 개인마다, 문화마다, 시대마다 다르게 이해된다 — 보편적 도덕의 근거가 될 수 없다. "
                "행복 추구는 자기 사랑(경향성)의 표현이며, 경향성은 조건적 가치만을 갖는다. "
                "도덕적으로 나쁜 일을 통해서도 행복을 얻을 수 있으므로, 행복이 도덕의 기준일 수 없다. "
                "도덕법칙은 행복 여부와 무관하게 타당해야 한다."
            ),
            "counterpoint": (
                "밀은 『공리주의』 제4장에서 행복(쾌락)이 유일하게 그 자체로 바람직한 목적이라고 주장하며, "
                "행복 원리를 거부하는 칸트식 도덕이 실질적 도덕 내용을 제공하지 못한다고 비판했다. "
                "아리스토텔레스는 에우다이모니아(행복·번영)가 인간 행위의 궁극 목적임을 주장하며, "
                "행복과 덕은 분리될 수 없다고 보았다."
            ),
            "context": (
                "에피쿠로스주의(쾌락), 공리주의(공리), 행복론 전반에 대한 비판이며, "
                "칸트 의무론 윤리학의 핵심 특징인 '도덕과 행복의 분리'를 보여준다."
            ),
            "keywords": ["행복 비판", "행복주의", "도덕의 동기", "최고선", "덕과 행복 분리", "경향성"],
            "verified": False,
            "verification_log": []
        },
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """임마누엘 칸트 키워드 데이터 입력."""
    keywords = [
        {
            "id": "kant-kw-categorical-imperative",
            "term": "정언명법",
            "term_en": "Categorical Imperative (Kategorischer Imperativ)",
            "definition": (
                "칸트 윤리학의 핵심 원리. 어떤 조건이나 목적과 무관하게 무조건적으로 부과되는 도덕 명령. "
                "세 가지 정식으로 표현된다: "
                "(1) 보편법칙 정식(GMS 4:421): '네 준칙이 보편법칙이 될 수 있도록 행위하라.' "
                "(2) 인간성 정식(GMS 4:429): '인간성을 항상 목적으로, 결코 단순히 수단으로만 대우하라.' "
                "(3) 자율성/목적의 왕국 정식(GMS 4:432): '모든 이성적 존재가 보편적 입법자인 목적의 왕국의 구성원처럼 행위하라.' "
                "가언명법(조건부 명령)과 대비된다."
            ),
            "thinker_id": "kant",
            "work_id": "kant-groundwork",
            "related_terms": ["선의지", "자율성", "의무", "보편법칙", "인간성 정식", "목적의 왕국"]
        },
        {
            "id": "kant-kw-good-will",
            "term": "선의지",
            "term_en": "Good Will (Guter Wille)",
            "definition": (
                "칸트 윤리학의 출발점. 무조건적으로, 어떤 상황에서도 선한 유일한 것. "
                "선의지는 도덕법칙에 따르려는 의지, 즉 의무 의식에서 행동하는 의지이다. "
                "결과, 재능, 행복, 지성 등 다른 모든 가치들은 선의지 없이는 악에 봉사할 수 있다. "
                "선의지의 가치는 그것이 성취하거나 산출하는 것에 의존하지 않는다 — 의지 그 자체의 선함. "
                "(GMS 4:393 첫 문장)"
            ),
            "thinker_id": "kant",
            "work_id": "kant-groundwork",
            "related_terms": ["의무", "경향성", "도덕적 가치", "aus Pflicht", "도덕법칙"]
        },
        {
            "id": "kant-kw-autonomy",
            "term": "자율성",
            "term_en": "Autonomy (Autonomie des Willens)",
            "definition": (
                "의지가 외부 규정 없이 스스로에게 도덕법칙을 부여하는 성질. "
                "타율성(Heteronomie) — 외부 권위(신, 국가, 감정, 행복)에 의해 의지가 규정됨 — 의 반대. "
                "자율성이 도덕법칙의 최고 원리(GMS 4:440)이며, 자율성이 곧 자유의 실질적 내용이다. "
                "자율적 의지만이 도덕적으로 선한 행위의 원천이 될 수 있다. "
                "자율성 = 자기 입법(Selbstgesetzgebung) = 진정한 자유."
            ),
            "thinker_id": "kant",
            "work_id": "kant-groundwork",
            "related_terms": ["타율성", "자유", "선의지", "목적의 왕국", "도덕법칙", "정언명법"]
        },
        {
            "id": "kant-kw-ding-an-sich",
            "term": "물자체",
            "term_en": "Thing-in-Itself (Ding an sich)",
            "definition": (
                "우리의 인식 형식과 무관하게 그 자체로 존재하는 것. "
                "우리는 현상(Erscheinung) — 인식 형식(공간·시간·범주)에 의해 구성된 것 — 만 인식 가능하다. "
                "물자체는 원칙적으로 인식 불가능하다(이론이성의 한계). "
                "도덕철학적 의의: 자유·신·영혼불사는 현상계 너머 물자체의 영역에 속하므로, "
                "이론적으로 부정될 수 없고 실천적으로 요청된다. "
                "(KrV B xxvi-xxvii)"
            ),
            "thinker_id": "kant",
            "work_id": "kant-critique-pure-reason",
            "related_terms": ["현상", "코페르니쿠스적 전회", "이율배반", "초월론적 관념론", "자유"]
        },
        {
            "id": "kant-kw-kingdom-of-ends",
            "term": "목적의 왕국",
            "term_en": "Kingdom of Ends (Reich der Zwecke)",
            "definition": (
                "모든 이성적 존재가 서로를 목적으로 대우하고 공동으로 도덕법칙을 입법하는 이상적 도덕 공동체. "
                "각 구성원은 보편적 입법자(주권자)이면서 동시에 법칙에 복종하는 구성원이다. "
                "이 왕국은 도덕적 이상으로서, 모든 이성적 존재가 자율적으로 공유하는 도덕 질서의 표현. "
                "정언명법 제3정식의 내용: '목적의 왕국의 보편적 입법자인 것처럼 행위하라.' "
                "(GMS 4:433~436)"
            ),
            "thinker_id": "kant",
            "work_id": "kant-groundwork",
            "related_terms": ["자율성", "인간성 정식", "존엄성", "이성적 존재", "정언명법 제3정식"]
        },
        {
            "id": "kant-kw-postulates",
            "term": "실천이성의 요청",
            "term_en": "Postulates of Practical Reason (Postulate der reinen praktischen Vernunft)",
            "definition": (
                "최고선의 실현 가능성을 위해 실천이성이 요청(상정)해야 하는 세 가지 이념. "
                "(1) 자유(Freiheit): 이미 도덕법칙 의식에서 확보됨. "
                "(2) 영혼불사(Unsterblichkeit der Seele): 완전한 덕성(신성성)을 향한 무한 진보를 위해 무한한 시간이 필요. "
                "(3) 신의 존재(Dasein Gottes): 덕에 비례하는 행복을 보장하는 도덕적 세계 창시자. "
                "요청은 이론적 인식이 아니라 실천적 신앙(moralischer Glaube)이다. "
                "(KpV 5:122~134)"
            ),
            "thinker_id": "kant",
            "work_id": "kant-critique-practical-reason",
            "related_terms": ["최고선", "영혼불사", "신의 존재", "자유", "도덕 신학", "실천적 신앙"]
        },
        {
            "id": "kant-kw-radical-evil",
            "term": "근본악",
            "term_en": "Radical Evil (Das radikal Böse)",
            "definition": (
                "칸트의 종교철학 개념. 인간 본성 깊은 곳에 있는 도덕법칙보다 경향성을 우선시하는 성향. "
                "'근본(radikal)'은 '뿌리(radix)'에서 유래 — 자유로운 행위의 가장 깊은 근거에 있음. "
                "세 단계: 연약함(Gebrechlichkeit) → 불순함(Unlauterkeit) → 사악함(Bösartigkeit). "
                "이 악은 자연적 필연성이 아니라 자유로운 선택의 결과이므로 도덕적 책임이 귀속된다. "
                "극복 방법: 도덕적 혁명(Gesinnung의 전환) — 이성의 자율성으로 가능. "
                "(Rel. 6:29~44)"
            ),
            "thinker_id": "kant",
            "work_id": "kant-religion-within-reason",
            "related_terms": ["악에의 성향", "도덕적 회심", "자유의지", "원죄 비교", "이성의 한계 안에서의 종교"]
        },
        {
            "id": "kant-kw-sapere-aude",
            "term": "Sapere aude (감히 알려고 하라)",
            "term_en": "Sapere aude (Dare to Know / Have Courage to Use Your Own Understanding)",
            "definition": (
                "칸트 계몽론의 표어. 호라티우스의 라틴어 구절에서 차용. "
                "'감히 알려고 하라! 네 자신의 이성을 사용할 용기를 가져라!' "
                "계몽의 핵심: 타인의 권위에 의존하는 미성년 상태에서 벗어나 스스로 생각하는 것. "
                "이성의 자율적 사용 = 계몽 = 도덕적 자율성의 인식론적 표현. "
                "(WA 8:35)"
            ),
            "thinker_id": "kant",
            "work_id": "kant-what-is-enlightenment",
            "related_terms": ["계몽", "미성년 상태", "자율성", "이성의 공적 사용", "자유"]
        },
        {
            "id": "kant-kw-dignity",
            "term": "존엄성",
            "term_en": "Dignity (Würde)",
            "definition": (
                "칸트 인간학의 핵심 개념. 이성적 존재가 갖는 절대적 내적 가치. "
                "가격(Preis)과 대비: 가격은 등가 교환 가능하지만, 존엄성은 어떤 것과도 교환될 수 없다. "
                "존엄성의 근거: 이성적 자율성 — 자신에게 도덕법칙을 부여할 수 있는 능력. "
                "인간성 정식의 토대: 인간의 존엄성은 인간을 단순히 수단으로 취급하는 것을 금한다. "
                "현대 인권 사상의 철학적 원천. (GMS 4:434~436)"
            ),
            "thinker_id": "kant",
            "work_id": "kant-groundwork",
            "related_terms": ["인간성 정식", "자율성", "목적 자체", "이성적 존재", "인권"]
        },
        {
            "id": "kant-kw-highest-good",
            "term": "최고선",
            "term_en": "Highest Good (Das höchste Gut / Summum Bonum)",
            "definition": (
                "덕(Tugend)과 그에 비례하는 행복(Glückseligkeit)의 완전한 결합. "
                "도덕의 목적이 행복이어서는 안 되지만, 덕과 행복의 조화는 이성이 지향하는 궁극적 목적. "
                "현세에서 완전한 최고선 실현은 불가능하므로 실천이성의 요청(영혼불사, 신의 존재)이 필요. "
                "칸트 도덕 신학의 핵심: '도덕이 종교로 이어지는' 구조. "
                "(KpV 5:107~119)"
            ),
            "thinker_id": "kant",
            "work_id": "kant-critique-practical-reason",
            "related_terms": ["덕", "행복", "실천이성의 요청", "도덕 신학", "영혼불사", "신의 존재"]
        },
        {
            "id": "kant-kw-maxim",
            "term": "준칙",
            "term_en": "Maxim (Maxime)",
            "definition": (
                "행위자가 자신의 행동 원칙으로 채택하는 주관적 원리. "
                "도덕법칙(객관적·보편적 원리)과 대비: 준칙은 개인의 주관적 행위 원칙이다. "
                "보편법칙 정식의 검증 대상: '내 준칙이 보편법칙이 될 수 있는가?' "
                "예시: '나는 돈이 필요할 때 거짓 약속을 하겠다' — 보편화하면 약속 제도가 붕괴하므로 도덕적으로 불허. "
                "(GMS 4:400 각주)"
            ),
            "thinker_id": "kant",
            "work_id": "kant-groundwork",
            "related_terms": ["보편법칙 정식", "정언명법", "도덕법칙", "의지", "행위 원칙"]
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """임마누엘 칸트 관련 관계 데이터 입력."""
    relations = [
        {
            "id": "kant-rel-001",
            "from_thinker": "kant",
            "to_thinker": "hume",
            "type": "criticized",
            "description": (
                "칸트는 흄의 인과율 회의주의가 자신을 '독단적 선잠'에서 깨웠다고 인정하면서도, "
                "흄의 결론(인과율은 습관적 연상)을 거부했다. "
                "칸트는 인과율을 오성의 선험적 범주로 정초함으로써 흄의 회의주의를 극복하고자 했다. "
                "또한 흄의 도덕 감각론(도덕의 근거는 감정)에 대해, "
                "도덕의 근거는 감정이 아닌 이성의 자율성에 있다고 비판했다."
            ),
            "evidence": "칸트, 순수이성비판 B 재판 서문; 실천이성비판 5:41; 도덕형이상학 기초놓기 4:408~411"
        },
        {
            "id": "kant-rel-002",
            "from_thinker": "kant",
            "to_thinker": "rousseau",
            "type": "synthesized",
            "description": (
                "칸트는 루소의 자유·평등·자율성 개념을 도덕철학의 핵심으로 수용하여 발전시켰다. "
                "루소의 '일반의지(volonté générale)'와 자기 부과 법칙 개념은 칸트의 자율성 윤리학에 직접적 영감을 주었다. "
                "칸트는 루소를 '도덕의 뉴턴'이라고 불렀다. "
                "그러나 칸트는 루소의 경험적 인간 본성론을 넘어서 순수 이성에 기반한 도덕 형이상학을 구축했다."
            ),
            "evidence": "칸트 단편 노트 『미와 숭고의 감정에 관한 고찰』; 『도덕형이상학 기초놓기』 서문"
        },
        {
            "id": "kant-rel-003",
            "from_thinker": "kant",
            "to_thinker": "mill",
            "type": "influenced",
            "description": (
                "칸트의 의무론 윤리학은 밀의 공리주의와 긴장 관계에 있으면서도 영향을 미쳤다. "
                "밀은 『공리주의』에서 칸트의 보편법칙 정식을 비판하면서도, 보편화 가능성의 기준이 암묵적으로 결과주의를 전제한다는 논점을 통해 "
                "결과주의 윤리학의 정당화에 활용했다. "
                "칸트의 인간 존엄성·자유 개념은 밀의 자유주의 사상(『자유론(On Liberty)』)에도 간접적으로 영향을 주었다."
            ),
            "evidence": "밀, 공리주의 제1장; 자유론 제1장"
        },
        {
            "id": "kant-rel-004",
            "from_thinker": "kant",
            "to_thinker": "aquinas",
            "type": "criticized",
            "description": (
                "칸트는 아퀴나스류의 자연법 윤리학과 신의 존재 증명을 비판했다. "
                "『순수이성비판』 B620~630에서 우주론적·목적론적 신 존재 증명이 현상계 너머의 영역에 인과율을 부당하게 적용한다고 비판했다. "
                "또한 자연의 목적론적 질서에서 도덕 원리를 도출하는 자연법 윤리학은 타율적 도덕(자연의 타율)에 해당한다고 비판했다."
            ),
            "evidence": "칸트, 순수이성비판 B620~630; 실천이성비판 5:40~41; 도덕형이상학 기초놓기 4:441~444"
        },
        {
            "id": "kant-rel-005",
            "from_thinker": "kant",
            "to_thinker": "aristotle",
            "type": "criticized",
            "description": (
                "칸트는 아리스토텔레스의 덕 윤리학과 행복론(에우다이모니아)을 비판했다. "
                "에우다이모니아(행복)를 도덕의 궁극 목적으로 삼는 것은 타율적 도덕이다 — "
                "행복이라는 외적 목적이 도덕의 근거가 되기 때문이다. "
                "덕(아레테)은 결과나 목적이 아니라 의무 자체에 근거해야 한다. "
                "그러나 칸트 자신도 『도덕형이상학』에서 덕 개념을 활용했으며, "
                "현대의 덕 윤리학 부흥은 칸트 의무론에 대한 대안 모색의 결과이기도 하다."
            ),
            "evidence": "칸트, 실천이성비판 5:64~65; 도덕형이상학 기초놓기 4:393~394"
        },
        {
            "id": "kant-rel-006",
            "from_thinker": "kant",
            "to_thinker": "socrates",
            "type": "synthesized",
            "description": (
                "칸트는 소크라테스의 '덕은 지식이다' 테제와 영혼의 돌봄 전통을 비판적으로 계승했다. "
                "소크라테스의 지적 덕 개념이 너무 지성주의적이라고 보면서도, "
                "도덕의 근거를 이성에서 찾는 합리주의적 윤리학 전통을 공유했다. "
                "소크라테스의 양심(다이모니온) 개념은 칸트의 도덕적 양심(moralisches Gewissen) 논의와 대화 가능하다."
            ),
            "evidence": "칸트, 도덕형이상학 6:437~440 (양심론); 윤리학 강의 27:352"
        }
    ]

    for rel in relations:
        result = client.index(index=INDEX_RELATIONS, id=rel["id"], document=rel)
        print(f"[relation] {rel['id']}: {result['result']}")

    return len(relations)


def verify_insertion(client):
    """입력된 데이터를 간단히 검증한다."""
    print("\n=== 검증 ===")

    # thinker 확인
    thinker = client.get(index=INDEX_THINKERS, id="kant")
    print(f"[OK] thinker: {thinker['_source']['name']} ({thinker['_source']['name_en']})")

    # works 건수 확인
    works = search_documents(client, INDEX_WORKS, {"term": {"thinker_id": "kant"}}, size=20)
    print(f"[OK] works: {works['hits']['total']['value']}건")

    # claims 건수 확인
    claims = search_documents(client, INDEX_CLAIMS, {"term": {"thinker_id": "kant"}}, size=30)
    print(f"[OK] claims: {claims['hits']['total']['value']}건")

    # keywords 건수 확인
    keywords = search_documents(client, INDEX_KEYWORDS, {"term": {"thinker_id": "kant"}}, size=20)
    print(f"[OK] keywords: {keywords['hits']['total']['value']}건")

    # relations 건수 확인
    relations = search_documents(
        client, INDEX_RELATIONS,
        {"bool": {"should": [
            {"term": {"from_thinker": "kant"}},
            {"term": {"to_thinker": "kant"}}
        ], "minimum_should_match": 1}},
        size=20
    )
    print(f"[OK] relations (kant 관련): {relations['hits']['total']['value']}건")


def main():
    """메인 실행 함수."""
    print("=== 임마누엘 칸트 데이터 입력 시작 ===\n")

    client = get_client()

    try:
        # 1. thinker 입력
        print("--- thinker 입력 ---")
        insert_thinker(client)

        # 2. works 입력
        print("\n--- works 입력 ---")
        n_works = insert_works(client)
        print(f"  총 {n_works}건 입력")

        # 3. claims 입력
        print("\n--- claims 입력 ---")
        n_claims = insert_claims(client)
        print(f"  총 {n_claims}건 입력")

        # 4. keywords 입력
        print("\n--- keywords 입력 ---")
        n_keywords = insert_keywords(client)
        print(f"  총 {n_keywords}건 입력")

        # 5. relations 입력
        print("\n--- relations 입력 ---")
        n_relations = insert_relations(client)
        print(f"  총 {n_relations}건 입력")

        # 6. 검증
        verify_insertion(client)

        print("\n=== 완료 ===")
        print(f"  thinker: 1건")
        print(f"  works: {n_works}건")
        print(f"  claims: {n_claims}건")
        print(f"  keywords: {n_keywords}건")
        print(f"  relations: {n_relations}건")

    finally:
        close_client(client)


if __name__ == "__main__":
    main()
