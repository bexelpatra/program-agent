"""게오르크 빌헬름 프리드리히 헤겔(G.W.F. Hegel) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS
)


def insert_thinker(client):
    """헤겔 사상가 데이터 입력."""
    doc = {
        "id": "hegel",
        "name": "게오르크 빌헬름 프리드리히 헤겔",
        "name_en": "Georg Wilhelm Friedrich Hegel",
        "field": "western_ethics",
        "era": "독일 관념론",
        "birth_year": 1770,
        "death_year": 1831,
        "background": (
            "슈투트가르트에서 관료 가문의 장남으로 태어났다. "
            "튀빙엔 신학교(Tübinger Stift)에서 셸링, 횔덜린과 함께 수학하며 "
            "프랑스 혁명의 이상에 열광했다. 졸업 후 베른과 프랑크푸르트에서 가정교사로 일하며 "
            "신학적·정치적 저작을 집필했다. 1801년 예나 대학에서 교수 자격을 얻었고, "
            "1806년 나폴레옹의 예나 점령 직전에 '정신현상학'을 완성했다. "
            "밤베르크 신문 편집자(1807~1808), 뉘른베르크 김나지움 교장(1808~1816)을 거쳐 "
            "하이델베르크 대학(1816~1818), 베를린 대학(1818~1831) 교수를 역임했다. "
            "베를린 시기에 독일 학계의 최고 권위자로 군림했으며, "
            "1831년 콜레라로 급사했다."
        ),
        "core_philosophy": (
            "헤겔 철학의 핵심은 변증법적 관념론이다. 절대자(das Absolute)는 고정된 실체가 아니라 "
            "자기 전개의 과정 속에서 스스로를 인식하는 주체(Subjekt)이다. "
            "정신(Geist)은 자기 소외(Entäußerung)와 지양(Aufhebung)의 변증법적 운동을 통해 "
            "즉자(an sich) → 대자(für sich) → 즉자대자(an und für sich)로 발전한다. "
            "윤리학에서는 추상적 권리(abstraktes Recht) → 도덕(Moralität) → 인륜(Sittlichkeit)의 "
            "변증법적 발전을 통해 개인의 주관적 도덕이 가족·시민사회·국가라는 "
            "객관적 인륜 공동체 속에서 구체적으로 실현된다고 주장한다. "
            "역사는 자유 의식의 진보이며, 세계정신(Weltgeist)이 자유를 실현해 가는 합리적 과정이다."
        ),
        "philosophical_journey": (
            "초기(~1800): 튀빙엔 시기에 칸트와 피히테의 도덕철학, 그리스 폴리스의 인륜적 생활에 "
            "감명받았다. 베른·프랑크푸르트 시기에 기독교의 '실정성(Positivität)'을 비판하고 "
            "사랑과 생명의 통일을 추구하는 신학적 단편들을 남겼다. "
            "예나 시기(1801~1807): 셸링과 공동으로 '철학비판잡지'를 발간하며 동일철학에서 출발했으나 "
            "점차 셸링의 직관적 방법과 결별하고 독자적 변증법 체계를 수립했다. "
            "'정신현상학'(1807)으로 자신의 철학적 입장을 선언했다. "
            "뉘른베르크·하이델베르크 시기(1808~1818): '논리학'(1812~1816)과 "
            "'엔치클로페디'(1817) 초판을 출간하여 체계를 완성했다. "
            "베를린 시기(1818~1831): '법철학'(1820)을 출간하고 미학·종교철학·역사철학·"
            "철학사 강의를 통해 체계를 구체화했다."
        ),
        "keywords": [
            "변증법(Dialektik)",
            "인륜성(Sittlichkeit)",
            "절대정신(absoluter Geist)",
            "지양(Aufhebung)",
            "시민사회(bürgerliche Gesellschaft)",
            "세계정신(Weltgeist)"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="hegel", document=doc)
    print(f"[thinker] hegel: {result['result']}")
    return result


def insert_works(client):
    """헤겔 저서 데이터 입력."""
    works = [
        {
            "id": "hegel-phaenomenologie",
            "thinker_id": "hegel",
            "title": "정신현상학",
            "title_original": "Phänomenologie des Geistes",
            "year": 1807,
            "significance": (
                "헤겔 철학의 서론이자 독자적 체계의 출발점. "
                "의식이 감각적 확신에서 출발하여 지각, 오성, 자기의식, 이성, 정신, 종교를 거쳐 "
                "절대지(absolutes Wissen)에 도달하는 경험의 학(Wissenschaft der Erfahrung)을 서술한다. "
                "'주인과 노예의 변증법', '불행한 의식' 등 유명한 장면을 포함하며, "
                "의식의 자기 형성 과정을 통해 실체가 곧 주체임을 논증한다. "
                "1806년 예나 전투 직전에 탈고되어 1807년 출판되었다."
            ),
            "key_concepts": [
                "감각적 확신", "주인과 노예의 변증법", "불행한 의식",
                "이성", "정신", "절대지", "경험의 학"
            ]
        },
        {
            "id": "hegel-rechtsphilosophie",
            "thinker_id": "hegel",
            "title": "법철학",
            "title_original": "Grundlinien der Philosophie des Rechts",
            "year": 1820,
            "significance": (
                "헤겔 실천철학의 핵심 저작. 객관적 정신의 체계를 "
                "추상적 권리(소유, 계약, 불법) → 도덕(의도, 복지, 양심) → "
                "인륜(가족, 시민사회, 국가)의 삼단 구조로 전개한다. "
                "칸트의 추상적 도덕법칙을 비판하고, 자유가 구체적 사회제도 속에서 "
                "실현되어야 함을 논증한다. 서문의 '이성적인 것은 현실적이고, "
                "현실적인 것은 이성적이다(Was vernünftig ist, das ist wirklich; "
                "und was wirklich ist, das ist vernünftig)'는 헤겔 철학의 상징적 명제이다. "
                "1820년 출판(표지에는 1821년으로 표기)."
            ),
            "key_concepts": [
                "추상적 권리", "도덕", "인륜", "가족",
                "시민사회", "국가", "이성적 현실"
            ]
        },
        {
            "id": "hegel-wissenschaft-der-logik",
            "thinker_id": "hegel",
            "title": "논리학 (대논리학)",
            "title_original": "Wissenschaft der Logik",
            "year": 1812,
            "significance": (
                "헤겔 체계의 토대를 이루는 저작. 존재론(Sein) → 본질론(Wesen) → "
                "개념론(Begriff)의 삼단 구조로 순수 사유의 범주를 변증법적으로 전개한다. "
                "존재(Sein)와 무(Nichts)의 통일로서의 생성(Werden)에서 시작하여, "
                "질·양·한도, 현존재, 본질과 현상, 근거와 실존, 개념과 이념에 이르는 "
                "범주의 자기 전개를 서술한다. "
                "1812년 제1권(존재론), 1813년 제2권(본질론), 1816년 제3권(개념론) 출간. "
                "칸트의 선험 논리학을 비판적으로 계승하면서도 존재론과 논리학의 통일을 추구한다."
            ),
            "key_concepts": [
                "존재와 무", "생성", "질량한도", "본질과 현상",
                "개념", "이념", "변증법적 범주 전개"
            ]
        },
        {
            "id": "hegel-enzyklopaedie",
            "thinker_id": "hegel",
            "title": "엔치클로페디",
            "title_original": "Enzyklopädie der philosophischen Wissenschaften",
            "year": 1817,
            "significance": (
                "헤겔 철학 체계의 전체 개요를 제시하는 백과사전적 저작. "
                "논리학(Logik) → 자연철학(Naturphilosophie) → 정신철학(Philosophie des Geistes)의 "
                "삼분 체계로 구성된다. 정신철학은 다시 주관적 정신 → 객관적 정신 → 절대적 정신으로 "
                "나뉘며, 객관적 정신 부분이 법철학에 해당한다. "
                "초판(1817), 제2판(1827), 제3판(1830)으로 개정되었으며, "
                "각 판에서 체계가 점차 정교해졌다. "
                "강의에서 사용된 교재로, 학생과 동료를 위한 체계적 입문서 역할을 했다."
            ),
            "key_concepts": [
                "논리학", "자연철학", "정신철학", "주관적 정신",
                "객관적 정신", "절대적 정신", "체계"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """헤겔 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 변증법 (정-반-합, Aufhebung)
        {
            "id": "hegel-claim-001",
            "thinker_id": "hegel",
            "work_id": "hegel-wissenschaft-der-logik",
            "source_detail": "Wissenschaft der Logik, Einleitung; Enzyklopädie §79-82",
            "claim": (
                "모든 사유와 존재는 변증법적으로 전개된다. "
                "추상적 지성(Verstand)의 규정은 자기 안에 모순을 포함하며, "
                "이 모순을 통해 부정되고(부정적 이성), "
                "다시 더 높은 통일로 지양된다(긍정적 이성, 사변적 사유). "
                "지양(Aufhebung)은 부정·보존·고양의 세 의미를 동시에 함축한다."
            ),
            "original_text": (
                "Das Aufheben hat in der Sprache den gedoppelten Sinn, "
                "daß es soviel als aufbewahren, erhalten bedeutet und zugleich soviel als "
                "aufhören lassen, ein Ende machen. "
                "(Wissenschaft der Logik I, Das Sein, Anmerkung 1)"
            ),
            "original_text_ko": (
                "지양(Aufheben)이라는 말은 언어 속에 이중적 의미를 지닌다. "
                "그것은 보존하고 간직한다는 뜻과 동시에 중단시키고 끝낸다는 뜻을 함께 갖는다. "
                "(논리학 I, 존재론, 주석 1)"
            ),
            "explanation": (
                "헤겔의 변증법은 통속적으로 '정-반-합(These-Antithese-Synthese)'으로 알려져 있으나, "
                "헤겔 자신은 이 용어를 거의 사용하지 않았다. "
                "변증법의 핵심은 지양(Aufhebung) 개념으로, 부정을 통해 이전 단계를 폐기하면서도 "
                "그 본질적 내용을 보존하고 더 높은 차원으로 고양시키는 운동이다. "
                "이는 단순한 형식논리가 아니라 사유와 존재의 실질적 전개 과정을 서술한다."
            ),
            "argument": (
                "(1) 지성적 사유는 규정을 고정하지만, 모든 유한한 규정은 자기 안에 자신의 부정을 포함한다. "
                "(2) 이 내재적 모순이 드러나면 규정은 자기 자신의 타자로 이행한다(부정적 변증법). "
                "(3) 그러나 이 이행은 단순한 파괴가 아니라, 양자를 포괄하는 구체적 통일이 산출된다(사변적 이성). "
                "(4) 논리학의 출발점인 '존재(Sein)'는 아무런 규정도 없으므로 '무(Nichts)'와 동일하며, "
                "양자의 통일이 '생성(Werden)'이다. 이것이 변증법적 운동의 원형이다."
            ),
            "counterpoint": (
                "키르케고르(Søren Kierkegaard, 1813~1855)는 '비학문적 후서'(Afsluttende uvidenskabelig "
                "Efterskrift, 1846)에서 헤겔의 변증법적 매개(Vermittlung)를 비판했다. "
                "실존적 결단의 '이것이냐 저것이냐(Enten-Eller)'의 양자택일은 "
                "변증법적 종합으로 해소될 수 없으며, "
                "헤겔은 개인의 실존적 도약을 체계적 사변으로 해소함으로써 "
                "실존의 고유한 의미를 말살했다고 주장했다."
            ),
            "context": (
                "피히테의 정립-반정립-종합, 셸링의 동일철학을 비판적으로 계승하면서도 "
                "사유의 내재적 운동으로서의 변증법을 체계화했다."
            ),
            "keywords": ["변증법", "지양", "Aufhebung", "존재와 무", "생성"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-002: 인륜성 (Sittlichkeit) — 가족/시민사회/국가
        {
            "id": "hegel-claim-002",
            "thinker_id": "hegel",
            "work_id": "hegel-rechtsphilosophie",
            "source_detail": "Grundlinien der Philosophie des Rechts, §142-157, §182-256, §257-360",
            "claim": (
                "인륜(Sittlichkeit)은 자유의 이념이 살아있는 선(das lebendige Gute)으로서, "
                "추상적 권리와 주관적 도덕의 변증법적 통일이다. "
                "인륜은 가족(직접적 인륜) → 시민사회(인륜의 분열) → 국가(인륜적 이념의 현실태)로 "
                "변증법적으로 전개된다. 개인의 자유는 고립된 원자적 개인이 아니라 "
                "이러한 인륜적 공동체 속에서만 구체적으로 실현된다."
            ),
            "original_text": (
                "Die Sittlichkeit ist die Idee der Freiheit, als das lebendige Gute, "
                "das in dem Selbstbewußtsein sein Wissen, Wollen, "
                "und durch dessen Handeln seine Wirklichkeit, "
                "so wie dieses an dem sittlichen Sein seine an und für sich seiende "
                "Grundlage und bewegenden Zweck hat. "
                "(Grundlinien der Philosophie des Rechts, §142)"
            ),
            "original_text_ko": (
                "인륜은 자유의 이념으로서 살아있는 선이다. "
                "이 선은 자기의식 속에서 자신의 지(知)와 의지를 가지며, "
                "자기의식의 행위를 통해 자신의 현실성을 갖는다. "
                "마찬가지로 자기의식은 인륜적 존재 속에서 자신의 즉자대자적 기초와 "
                "운동하는 목적을 갖는다. (법철학 §142)"
            ),
            "explanation": (
                "헤겔은 칸트의 형식적 도덕법칙이 내용 없는 공허한 형식주의에 빠진다고 비판하고, "
                "도덕이 구체적 사회제도(가족, 시민사회, 국가) 속에서 실현되어야 한다고 주장한다. "
                "인륜은 단순히 개인의 내면적 의무감이 아니라, "
                "현실적인 제도와 관습, 법률 속에 체현된 객관적 자유이다."
            ),
            "argument": (
                "(1) 추상적 권리(소유, 계약)는 인격의 외적 자유를 인정하지만 내면의 도덕적 의지를 결여한다. "
                "(2) 도덕(의도, 양심)은 주관적 확신에 머물러 객관적 타당성을 확보하지 못한다. "
                "(3) 인륜은 양자의 통일로서, 주관적 의지가 객관적 제도 속에서 자기를 실현하는 '구체적 자유'이다. "
                "(4) 가족은 사랑에 의한 직접적 통일, 시민사회는 개인의 특수 이익이 분화하는 영역, "
                "국가는 특수와 보편의 변증법적 통일이다."
            ),
            "counterpoint": (
                "칼 마르크스(Karl Marx, 1818~1883)는 '헤겔 법철학 비판'(Kritik des Hegelschen "
                "Staatsrechts, 1843)에서 헤겔이 시민사회와 국가의 관계를 전도시켰다고 비판했다. "
                "헤겔은 국가를 시민사회의 모순을 해결하는 이성적 전체로 보았지만, "
                "마르크스에 따르면 국가는 시민사회의 물질적 관계(계급 이익)에 의해 규정되는 것이지 "
                "그 반대가 아니다."
            ),
            "context": (
                "칸트의 도덕법칙의 형식주의, 피히테의 자아 철학의 주관주의를 극복하고 "
                "그리스 폴리스의 실질적 인륜을 근대적으로 재구성하려는 시도이다."
            ),
            "keywords": ["인륜", "Sittlichkeit", "가족", "시민사회", "국가"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-003: 주인과 노예의 변증법
        {
            "id": "hegel-claim-003",
            "thinker_id": "hegel",
            "work_id": "hegel-phaenomenologie",
            "source_detail": "Phänomenologie des Geistes, IV.A. Selbständigkeit und Unselbständigkeit des Selbstbewußtseins",
            "claim": (
                "자기의식은 타자의 인정(Anerkennung)을 통해서만 자기를 확인할 수 있다. "
                "두 자기의식이 만나 생사를 건 투쟁을 벌이고, 죽음을 두려워한 쪽이 노예가 되고 "
                "죽음을 무릅쓴 쪽이 주인이 된다. "
                "그러나 노예는 노동(Arbeit)을 통해 자연을 형성하면서 자립적 의식을 획득하고, "
                "주인은 노예에게 의존하게 되어 오히려 비자립적이 된다. "
                "이로써 지배와 예속의 관계가 변증법적으로 역전된다."
            ),
            "original_text": (
                "Das Selbstbewußtsein ist an und für sich, indem und dadurch, "
                "daß es für ein Anderes an und für sich ist; "
                "d.h. es ist nur als ein Anerkanntes. "
                "(Phänomenologie des Geistes, IV.A)"
            ),
            "original_text_ko": (
                "자기의식은 즉자대자적으로 존재하되, 그것이 다른 자기의식에 대해 "
                "즉자대자적으로 존재함으로써 그러하다. "
                "즉 자기의식은 오직 인정된 것으로서만 존재한다. "
                "(정신현상학 IV.A)"
            ),
            "explanation": (
                "주인과 노예의 변증법은 인간의 자기의식이 상호 인정을 통해 형성됨을 보여주는 "
                "헤겔 철학의 가장 유명한 서사이다. "
                "노예가 노동을 통해 자기 형성(Bildung)을 이루는 반면, "
                "주인은 향유에 머물러 발전하지 못한다는 역전은 "
                "후대 마르크스의 노동 개념과 프랑크푸르트 학파의 비판이론에 지대한 영향을 미쳤다."
            ),
            "argument": (
                "(1) 자기의식은 단독으로는 자기를 확인할 수 없고, 타자의 인정이 필요하다. "
                "(2) 두 자기의식은 서로를 인정받기 위해 생사를 건 투쟁에 돌입한다. "
                "(3) 죽음을 두려워한 자는 항복하여 노예가 되고, 승자는 주인이 된다. "
                "(4) 주인은 노예를 통해 자연을 향유하지만, 자기 형성의 계기를 잃는다. "
                "(5) 노예는 주인에 대한 두려움(공포)과 사물에 대한 노동(형성)을 통해 "
                "독자적 의식을 발전시킨다. 관계가 변증법적으로 역전된다."
            ),
            "counterpoint": (
                "알렉상드르 코제브(Alexandre Kojève, 1902~1968)는 "
                "'헤겔 읽기'(Introduction à la lecture de Hegel, 1947)에서 "
                "주인과 노예의 변증법을 역사의 동력으로 해석하며 "
                "인정투쟁이 역사의 종말(보편적 상호인정)로 귀결된다고 주장했다. "
                "이에 대해 주디스 버틀러(Judith Butler)는 주인-노예 관계가 "
                "완전한 역전이 아니라 권력의 양가성(ambivalence)을 보여주며, "
                "예속 속에서 주체가 형성되는 역설적 구조를 강조했다."
            ),
            "context": (
                "정신현상학의 자기의식 장에서 서술되며, "
                "의식이 단순한 대상 인식에서 자기의식과 상호인정의 차원으로 넘어가는 결정적 전환점이다."
            ),
            "keywords": ["주인과 노예", "인정", "Anerkennung", "노동", "자기의식"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-004: 역사의 목적론 (세계정신, 자유의 실현)
        {
            "id": "hegel-claim-004",
            "thinker_id": "hegel",
            "work_id": "hegel-rechtsphilosophie",
            "source_detail": "Vorlesungen über die Philosophie der Geschichte, Einleitung; Rechtsphilosophie §341-360",
            "claim": (
                "세계사는 자유 의식의 진보이다. 세계정신(Weltgeist)은 특정 시대의 "
                "민족정신(Volksgeist)을 통해 자유를 실현해 간다. "
                "동양 세계에서는 한 사람만이 자유로웠고, 그리스-로마 세계에서는 일부가 자유로웠으며, "
                "게르만 세계(근대)에 이르러 모든 사람이 자유롭다는 것이 인식된다. "
                "역사에서의 이성의 교활(List der Vernunft)은 개인의 열정과 이해관계를 통해 "
                "보편적 목적을 실현한다."
            ),
            "original_text": (
                "Die Weltgeschichte ist der Fortschritt im Bewußtsein der Freiheit — "
                "ein Fortschritt, den wir in seiner Nothwendigkeit zu erkennen haben. "
                "(Vorlesungen über die Philosophie der Geschichte, Einleitung)"
            ),
            "original_text_ko": (
                "세계사는 자유 의식의 진보이다 — "
                "우리는 이 진보를 그 필연성에서 인식해야 한다. "
                "(역사철학 강의, 서론)"
            ),
            "explanation": (
                "헤겔에게 역사는 우연적 사건의 나열이 아니라 "
                "절대정신이 자유를 실현해 가는 합리적·필연적 과정이다. "
                "'이성의 교활'이란 세계정신이 나폴레옹 같은 '세계사적 개인'의 "
                "주관적 열정을 도구로 삼아 보편적 목적(자유의 실현)을 이루는 것을 뜻한다."
            ),
            "argument": (
                "(1) 정신의 본질은 자유이며, 정신은 자기 본질을 의식하고자 한다. "
                "(2) 역사는 정신이 자유를 의식하고 실현해 가는 과정이다. "
                "(3) 각 시대는 세계정신의 특정 원리를 체현하는 민족정신에 의해 대표된다. "
                "(4) 세계사적 개인(알렉산드로스, 카이사르, 나폴레옹)은 자신도 모르는 사이에 "
                "세계정신의 의지를 실행하며, 이것이 '이성의 교활'이다. "
                "(5) 최종적으로 자유가 모든 인간의 본질로 인식되는 데 이른다."
            ),
            "counterpoint": (
                "칼 포퍼(Karl Popper, 1902~1994)는 '열린 사회와 그 적들'(The Open Society "
                "and Its Enemies, 1945) 제2권에서 헤겔의 역사철학을 '역사주의(historicism)'로 비판했다. "
                "역사에 필연적 법칙이나 목적이 있다는 주장은 과학적으로 검증 불가능하며, "
                "전체주의적 정치를 정당화하는 데 악용될 수 있다고 경고했다. "
                "또한 헤겔의 국가 신격화가 프로이센 권위주의를 옹호하는 것이라고 비난했다."
            ),
            "context": (
                "베를린 시기의 역사철학 강의(사후 출판)에서 체계적으로 전개되었으며, "
                "법철학의 세계사 장(§341~360)과 연결된다."
            ),
            "keywords": ["세계사", "세계정신", "자유 의식의 진보", "이성의 교활", "민족정신"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-005: 추상적 권리 → 도덕 → 인륜의 발전
        {
            "id": "hegel-claim-005",
            "thinker_id": "hegel",
            "work_id": "hegel-rechtsphilosophie",
            "source_detail": "Grundlinien der Philosophie des Rechts, §34-104 (추상적 권리), §105-141 (도덕), §142-360 (인륜)",
            "claim": (
                "객관적 정신의 전개는 추상적 권리(abstraktes Recht) → 도덕(Moralität) → "
                "인륜(Sittlichkeit)의 삼단계를 거친다. "
                "추상적 권리는 인격의 외면적 자유(소유, 계약)를 다루지만 내면의 의지를 결여하고, "
                "도덕은 주관적 의지의 내면적 자유(의도, 양심)를 다루지만 객관적 제도를 결여한다. "
                "인륜은 양자의 통일로서, 주관적 의지와 객관적 제도가 합치하는 구체적 자유이다."
            ),
            "original_text": (
                "Das Recht ist zuerst das unmittelbare Dasein, "
                "welches sich die Freiheit auf unmittelbare Weise gibt. "
                "(Grundlinien der Philosophie des Rechts, §40) "
                "Der moralische Standpunkt ist der Standpunkt des Willens, "
                "insofern er nicht bloß an sich, sondern für sich unendlich ist. "
                "(§105)"
            ),
            "original_text_ko": (
                "권리는 우선 자유가 직접적 방식으로 자기에게 부여하는 "
                "직접적 현존재이다. (법철학 §40) "
                "도덕적 입장은 의지가 단지 즉자적으로만이 아니라 "
                "대자적으로도 무한한 한에서의 의지의 입장이다. (§105)"
            ),
            "explanation": (
                "법철학의 전체 구조는 자유가 점진적으로 구체화되는 과정을 보여준다. "
                "추상적 권리에서 자유는 외면적 소유에 머물고, 도덕에서 자유는 내면의 양심에 머문다. "
                "인륜에서야 비로소 자유가 현실적 제도(가족, 시민사회, 국가) 속에서 구체적으로 실현된다. "
                "이 삼단계는 자유의 추상에서 구체로의 변증법적 전개이다."
            ),
            "argument": (
                "(1) 추상적 권리: 자유로운 의지가 외적 사물에 대한 소유를 통해 자기를 실현한다. "
                "그러나 소유·계약은 인격의 외면적 관계에 그치며 의지의 내면적 측면을 포괄하지 못한다. "
                "(2) 도덕: 의지가 자기의 내면(의도, 복지, 양심)으로 반성한다. "
                "그러나 순수한 주관적 확신은 '아름다운 영혼(schöne Seele)'의 공허함이나 "
                "위선(Heuchelei)에 빠질 위험이 있다. "
                "(3) 인륜: 추상적 권리와 도덕의 통일. 주관적 의지가 현실적 제도 속에서 "
                "자기를 객관적으로 실현하며, 이것이 '구체적 자유'이다."
            ),
            "counterpoint": (
                "칸트주의자들은 헤겔이 도덕의 보편적 형식성을 포기하고 "
                "특정 공동체의 관습과 제도에 도덕을 종속시킴으로써 "
                "도덕적 보편주의를 훼손했다고 비판한다. "
                "위르겐 하버마스(Jürgen Habermas)는 '사실성과 타당성'(Faktizität und Geltung, 1992)에서 "
                "헤겔의 인륜 개념이 근대의 탈전통적 도덕 의식을 충분히 반영하지 못하며, "
                "의사소통적 합리성에 기초한 담론윤리로 보완되어야 한다고 주장했다."
            ),
            "context": (
                "법철학은 엔치클로페디 체계에서 '객관적 정신'에 해당하며, "
                "칸트의 도덕 형이상학과 피히테의 자연법 이론을 비판적으로 계승한다."
            ),
            "keywords": ["추상적 권리", "도덕", "인륜", "구체적 자유", "법철학"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-006: 국가론 (국가 = 인륜적 이념의 현실)
        {
            "id": "hegel-claim-006",
            "thinker_id": "hegel",
            "work_id": "hegel-rechtsphilosophie",
            "source_detail": "Grundlinien der Philosophie des Rechts, §257-271",
            "claim": (
                "국가는 인륜적 이념의 현실태(Wirklichkeit)이며, 자유의 구체적 실현이다. "
                "국가는 개인의 자유를 억압하는 외적 강제가 아니라, "
                "개인의 자유가 보편적 자유와 합치하는 최고의 인륜적 공동체이다. "
                "국가에서 개인의 특수한 이익과 보편적 이익이 통일되며, "
                "이것이 '구체적 자유'의 실현이다."
            ),
            "original_text": (
                "Der Staat ist die Wirklichkeit der sittlichen Idee — "
                "der sittliche Geist, als der offenbare, sich selbst deutliche, "
                "substantielle Wille, der sich denkt und weiß "
                "und das, was er weiß und insofern er es weiß, vollführt. "
                "(Grundlinien der Philosophie des Rechts, §257)"
            ),
            "original_text_ko": (
                "국가는 인륜적 이념의 현실태이다 — "
                "인륜적 정신으로서, 자기를 명시하며 자기에게 분명한, "
                "자기를 사유하고 아는 실체적 의지이다. "
                "국가는 자기가 아는 것을, 그리고 아는 한에서 수행한다. "
                "(법철학 §257)"
            ),
            "explanation": (
                "헤겔의 국가론은 사회계약론적 국가관(홉스, 로크, 루소)과 근본적으로 다르다. "
                "사회계약론에서 국가는 개인들의 합의에 의해 구성된 인위적 산물이지만, "
                "헤겔에게 국가는 인륜적 생활의 유기적 전체로서 개인에 논리적으로 선행한다. "
                "국가의 목적은 자유의 실현이며, 시민사회의 특수 이익들의 갈등을 "
                "보편적 이익으로 통합하는 역할을 한다."
            ),
            "argument": (
                "(1) 가족은 사랑에 기초한 직접적 통일이지만, 자녀의 성장과 함께 해체되어 "
                "시민사회의 독립적 개인들로 분화한다. "
                "(2) 시민사회는 '욕구의 체계(System der Bedürfnisse)'로서 개인들이 "
                "자기 이익을 추구하는 영역이나, 빈곤과 사치의 양극화 등 자체적 모순을 산출한다. "
                "(3) 국가는 시민사회의 분열을 지양하여 특수와 보편을 통일하는 최고의 인륜적 공동체이다. "
                "(4) 국가에서 개인은 의무를 이행함으로써 동시에 자기 자유를 실현한다."
            ),
            "counterpoint": (
                "칼 마르크스는 헤겔의 국가론이 현실의 계급 모순을 은폐하는 관념적 정당화라고 비판했다. "
                "국가는 '인륜적 이념의 현실태'가 아니라 지배계급의 이익을 관철하는 도구이며, "
                "진정한 인간 해방은 국가의 폐지를 통해서만 가능하다고 주장했다. "
                "또한 칼 포퍼는 헤겔의 국가 우위론이 개인의 권리를 국가에 종속시키는 "
                "전체주의의 이론적 기초를 제공했다고 비판했다."
            ),
            "context": (
                "법철학 인륜 장의 최종 단계로, 가족과 시민사회의 변증법적 통일이다. "
                "프로이센 입헌군주제를 이성적 국가의 모델로 제시했다는 논쟁이 있다."
            ),
            "keywords": ["국가", "인륜적 이념", "구체적 자유", "보편과 특수의 통일"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-007: 시민사회론 (욕구의 체계)
        {
            "id": "hegel-claim-007",
            "thinker_id": "hegel",
            "work_id": "hegel-rechtsphilosophie",
            "source_detail": "Grundlinien der Philosophie des Rechts, §182-256",
            "claim": (
                "시민사회(bürgerliche Gesellschaft)는 가족과 국가 사이의 중간 영역으로, "
                "개인들이 자기 이익을 추구하는 '욕구의 체계(System der Bedürfnisse)'이다. "
                "시민사회에서 각자는 자기 목적이지만, 타인 없이는 목적을 달성할 수 없으므로 "
                "상호 의존의 체계가 형성된다. "
                "그러나 시민사회는 자체적으로 빈곤(Armut)과 사치의 양극화, "
                "'천민(Pöbel)'의 등장이라는 해결 불가능한 모순을 산출한다."
            ),
            "original_text": (
                "Die bürgerliche Gesellschaft ist die Differenz, "
                "welche zwischen die Familie und den Staat tritt. "
                "(Grundlinien der Philosophie des Rechts, §182 Zusatz) "
                "In der bürgerlichen Gesellschaft ist jeder sich Zweck, "
                "alles andere ist ihm nichts. "
                "(§182 Zusatz)"
            ),
            "original_text_ko": (
                "시민사회는 가족과 국가 사이에 들어서는 차이(분화)이다. "
                "(법철학 §182 보충) "
                "시민사회에서 각자는 자기 자신이 목적이며, "
                "나머지 모든 것은 그에게 아무것도 아니다. "
                "(§182 보충)"
            ),
            "explanation": (
                "헤겔은 '시민사회'를 국가로부터 개념적으로 분리한 최초의 사상가 중 하나이다. "
                "시민사회는 아담 스미스적 시장 경제(욕구의 체계), 사법 행정(사법권), "
                "경찰과 직업단체(복지 행정)를 포함한다. "
                "시민사회는 개인의 특수 이익을 실현하는 영역이지만, "
                "자체적으로는 빈곤 문제를 해결할 수 없어 국가로의 이행이 필연적이다."
            ),
            "argument": (
                "(1) 가족이 해체되면 개인들은 독립적 인격으로서 시민사회에 진입한다. "
                "(2) 시민사회에서 각자는 자기 이익을 추구하지만, "
                "분업과 교환을 통해 타인의 노동에 의존하는 보편적 상호 의존이 형성된다. "
                "(3) 그러나 시장의 자유로운 작동은 부의 불평등한 축적과 빈곤을 산출한다. "
                "(4) 빈곤은 단순한 경제적 결핍이 아니라 인정의 박탈이며, "
                "이는 시민사회 내부에서는 해결 불가능한 구조적 모순이다. "
                "(5) 따라서 시민사회는 자체적으로 국가(보편적 이익의 영역)를 필요로 한다."
            ),
            "counterpoint": (
                "마르크스는 '경제학-철학 수고'(Ökonomisch-philosophische Manuskripte, 1844)에서 "
                "헤겔이 시민사회의 모순을 정확히 포착했지만, "
                "그 해결을 관념적 국가에서 찾은 것은 전도(顚倒)라고 비판했다. "
                "시민사회(자본주의 경제)의 모순은 국가에 의해 지양되는 것이 아니라, "
                "생산관계의 혁명적 변혁을 통해서만 극복될 수 있다고 주장했다."
            ),
            "context": (
                "법철학 인륜 장의 두 번째 단계로, "
                "근대 시장 경제와 시민사회의 독자적 영역을 최초로 이론화한 것으로 평가된다."
            ),
            "keywords": ["시민사회", "욕구의 체계", "빈곤", "직업단체", "상호 의존"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-008: 자유 개념 (즉자적 → 대자적 → 즉자대자적)
        {
            "id": "hegel-claim-008",
            "thinker_id": "hegel",
            "work_id": "hegel-enzyklopaedie",
            "source_detail": "Enzyklopädie §382-386; Rechtsphilosophie §21-28",
            "claim": (
                "자유는 정신의 본질이며, 정신이 자기 자신에게 있는 것(Bei-sich-selbst-Sein)이다. "
                "자유는 즉자적(an sich, 잠재적) → 대자적(für sich, 의식적) → "
                "즉자대자적(an und für sich, 완전히 실현된) 자유로 발전한다. "
                "즉자적 자유는 아직 실현되지 않은 가능성이고, "
                "대자적 자유는 의식적이지만 추상적이며, "
                "즉자대자적 자유는 인륜적 공동체 속에서 구체적으로 실현된 자유이다."
            ),
            "original_text": (
                "Die Substanz des Geistes ist die Freiheit, "
                "d.i. das Nicht-abhängig-sein von einem Anderen, "
                "und das Sich-auf-sich-selbst-beziehen. "
                "(Vorlesungen über die Philosophie der Geschichte, Einleitung) "
                "Der freie Wille ist der Wille, der sich selbst zum Gegenstand hat. "
                "(Rechtsphilosophie §21 Zusatz)"
            ),
            "original_text_ko": (
                "정신의 실체는 자유이다. "
                "즉 타자에 의존하지 않으며 자기 자신에게 관계하는 것이다. "
                "(역사철학 강의, 서론) "
                "자유로운 의지는 자기 자신을 대상으로 갖는 의지이다. "
                "(법철학 §21 보충)"
            ),
            "explanation": (
                "헤겔에게 자유는 외적 구속의 부재(소극적 자유)가 아니라, "
                "정신이 자기를 규정하고 자기 자신에게 있는 적극적 자유이다. "
                "자유의 세 단계는 씨앗에서 꽃으로, 꽃에서 열매로의 유기적 발전에 비유할 수 있다. "
                "자유의 완전한 실현은 인륜적 국가 속에서 개인의 의지와 보편적 의지가 합치할 때 달성된다."
            ),
            "argument": (
                "(1) 자유의 본질은 자기 규정(Selbstbestimmung)이다. 타자에 의해 규정되는 것은 부자유이다. "
                "(2) 즉자적 자유: 정신은 본질적으로 자유이지만 아직 이를 의식하지 못한다(아이, 미개인). "
                "(3) 대자적 자유: 정신이 자유를 의식하지만 추상적 형태에 머문다 "
                "(스토아적 내면의 자유, 칸트의 형식적 자율성). "
                "(4) 즉자대자적 자유: 자유가 현실적 제도 속에서 구체적으로 실현된다. "
                "개인의 의무가 동시에 자기 실현이 되는 인륜적 상태이다."
            ),
            "counterpoint": (
                "이사야 벌린(Isaiah Berlin, 1909~1997)은 '자유의 두 개념'(Two Concepts of Liberty, 1958)에서 "
                "헤겔식 적극적 자유(positive liberty) 개념이 '진정한 자아'나 '높은 자아'의 이름으로 "
                "개인의 실제적 선택을 억압하는 데 악용될 수 있다고 경고했다. "
                "'자유를 위한 강제(forcing to be free)'라는 역설은 "
                "전체주의적 자유 개념으로 전락할 위험이 있다고 비판했다."
            ),
            "context": (
                "엔치클로페디의 정신철학 서론과 법철학 서론에서 전개되며, "
                "자유 개념의 세 단계는 헤겔 실천철학 전체의 구조적 원리를 이룬다."
            ),
            "keywords": ["자유", "즉자적", "대자적", "즉자대자적", "자기규정"],
            "verified": False,
            "verification_log": []
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """헤겔 키워드 데이터 입력."""
    keywords = [
        {
            "id": "hegel-kw-001",
            "thinker_id": "hegel",
            "term": "변증법 (Dialektik)",
            "term_original": "Dialektik",
            "definition": (
                "사유와 존재의 자기 전개 운동. 추상적 규정(지성)이 자기 안의 모순을 통해 부정되고, "
                "더 높은 구체적 통일로 지양(Aufheben)되는 과정. "
                "통속적으로 '정-반-합(These-Antithese-Synthese)'으로 알려져 있으나, "
                "헤겔 자신은 이 용어를 거의 사용하지 않았다. "
                "변증법은 형식논리학의 외적 방법이 아니라 사태 자체의 내재적 운동이다."
            ),
            "related_claims": ["hegel-claim-001", "hegel-claim-005"],
            "source": "Wissenschaft der Logik, Einleitung; Enzyklopädie §79-82"
        },
        {
            "id": "hegel-kw-002",
            "thinker_id": "hegel",
            "term": "인륜성 (Sittlichkeit)",
            "term_original": "Sittlichkeit",
            "definition": (
                "자유의 이념이 살아있는 선으로 실현된 것. "
                "추상적 권리(외면적 자유)와 도덕(내면적 자유)의 변증법적 통일로서, "
                "가족·시민사회·국가라는 구체적 공동체 속에 체현된 객관적 자유. "
                "칸트의 형식적 '도덕(Moralität)'과 대비되는 헤겔 특유의 개념으로, "
                "그리스 폴리스의 실질적 인륜을 근대적으로 재구성한 것이다."
            ),
            "related_claims": ["hegel-claim-002", "hegel-claim-005", "hegel-claim-006"],
            "source": "Grundlinien der Philosophie des Rechts, §142-360"
        },
        {
            "id": "hegel-kw-003",
            "thinker_id": "hegel",
            "term": "절대정신 (absoluter Geist)",
            "term_original": "absoluter Geist",
            "definition": (
                "정신이 자기 자신을 완전히 인식하는 최고 단계. "
                "주관적 정신(개인의 심리)과 객관적 정신(사회·국가·역사)을 거쳐 "
                "예술·종교·철학이라는 절대적 정신의 형태에서 정신은 자기의 본질을 "
                "감성적(예술), 표상적(종교), 개념적(철학)으로 파악한다. "
                "철학에서 정신은 자기를 순수 개념으로 인식하며, 이것이 절대지(absolutes Wissen)이다."
            ),
            "related_claims": ["hegel-claim-001", "hegel-claim-004"],
            "source": "Enzyklopädie §553-577"
        },
        {
            "id": "hegel-kw-004",
            "thinker_id": "hegel",
            "term": "지양 (Aufhebung)",
            "term_original": "Aufhebung",
            "definition": (
                "헤겔 변증법의 핵심 개념. 독일어 aufheben의 세 가지 의미를 동시에 함축한다: "
                "(1) 부정하다·폐기하다(tollere), (2) 보존하다·간직하다(conservare), "
                "(3) 높이 올리다·고양하다(elevare). "
                "변증법적 운동에서 이전 단계는 단순히 파괴되는 것이 아니라, "
                "그 본질적 내용이 보존되면서 더 높은 차원으로 고양된다."
            ),
            "related_claims": ["hegel-claim-001"],
            "source": "Wissenschaft der Logik I, Das Sein, Anmerkung 1"
        },
        {
            "id": "hegel-kw-005",
            "thinker_id": "hegel",
            "term": "시민사회 (bürgerliche Gesellschaft)",
            "term_original": "bürgerliche Gesellschaft",
            "definition": (
                "가족과 국가 사이에 위치하는 인륜의 중간 영역. "
                "개인들이 자기 이익을 추구하는 '욕구의 체계', 권리를 보장하는 '사법 행정', "
                "복지를 담당하는 '경찰과 직업단체'로 구성된다. "
                "헤겔은 시민사회를 국가와 개념적으로 분리한 최초의 사상가 중 하나이다. "
                "시민사회는 자유 시장의 역동성과 함께 빈곤·불평등이라는 자체적 모순을 산출한다."
            ),
            "related_claims": ["hegel-claim-007", "hegel-claim-002"],
            "source": "Grundlinien der Philosophie des Rechts, §182-256"
        },
        {
            "id": "hegel-kw-006",
            "thinker_id": "hegel",
            "term": "세계정신 (Weltgeist)",
            "term_original": "Weltgeist",
            "definition": (
                "세계사를 관통하며 자유를 실현해 가는 보편적 정신. "
                "세계정신은 특정 시대의 민족정신(Volksgeist)을 통해 자기를 표현하며, "
                "세계사적 개인(나폴레옹 등)의 열정을 도구로 삼아 보편적 목적을 실현한다(이성의 교활). "
                "세계사는 동양 → 그리스-로마 → 게르만 세계로 진보하며, "
                "이는 자유 의식의 점진적 확대 과정이다."
            ),
            "related_claims": ["hegel-claim-004"],
            "source": "Vorlesungen über die Philosophie der Geschichte, Einleitung"
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """헤겔 관계 데이터 입력."""
    relations = [
        {
            "id": "relation-kant-hegel",
            "from_thinker": "kant",
            "to_thinker": "hegel",
            "type": "influenced",
            "description": (
                "칸트(Immanuel Kant, 1724~1804)의 선험 철학과 도덕법칙은 "
                "헤겔 철학의 가장 중요한 출발점이다. "
                "헤겔은 칸트의 이성 비판을 높이 평가하면서도, "
                "물자체(Ding an sich)와 현상의 이원론, 도덕법칙의 형식주의, "
                "이론이성과 실천이성의 분리를 극복하고자 했다. "
                "법철학에서 칸트의 추상적 도덕(Moralität)을 "
                "구체적 인륜(Sittlichkeit)으로 지양하는 것이 헤겔 실천철학의 핵심 과제였다."
            ),
            "strength": "강함",
            "period": "18세기 말~19세기 초"
        },
        {
            "id": "relation-fichte-hegel",
            "from_thinker": "fichte",
            "to_thinker": "hegel",
            "type": "influenced",
            "description": (
                "피히테(Johann Gottlieb Fichte, 1762~1814)의 자아 철학과 "
                "정립-반정립-종합의 삼단 구조는 헤겔 변증법의 직접적 선행 형태이다. "
                "헤겔은 피히테가 자아의 자기 정립에서 출발하여 비아(非我)를 대립시키고 "
                "종합으로 나아가는 방법을 계승했으나, "
                "피히테의 주관적 관념론(자아 = 절대적 원리)이 "
                "객관적 자연과 역사를 충분히 포괄하지 못한다고 비판했다."
            ),
            "strength": "강함",
            "period": "19세기 초"
        },
        {
            "id": "relation-hegel-marx",
            "from_thinker": "hegel",
            "to_thinker": "marx",
            "type": "influenced",
            "description": (
                "마르크스(Karl Marx, 1818~1883)는 헤겔의 변증법을 계승하되 "
                "'머리로 서 있는 것을 발로 세웠다'고 자임했다. "
                "헤겔의 관념적 변증법을 유물론적으로 전환하여 역사적 유물론을 수립했다. "
                "헤겔의 시민사회론, 주인과 노예의 변증법, 소외 개념을 비판적으로 수용하여 "
                "자본주의 분석과 프롤레타리아 혁명론의 기초를 놓았다."
            ),
            "strength": "강함",
            "period": "19세기 중반"
        },
        {
            "id": "relation-hegel-kierkegaard",
            "from_thinker": "hegel",
            "to_thinker": "kierkegaard",
            "type": "influenced",
            "description": (
                "키르케고르(Søren Kierkegaard, 1813~1855)는 헤겔 체계를 가장 통렬하게 비판한 사상가이다. "
                "헤겔의 변증법적 매개(Vermittlung)가 실존적 결단의 '이것이냐 저것이냐'를 "
                "사변적 종합으로 해소함으로써 개인의 실존을 말살했다고 비판했다. "
                "그러나 키르케고르의 실존 개념 자체가 헤겔 철학에 대한 반동으로 형성되었으며, "
                "불안·절망·도약 등의 개념은 헤겔의 '불행한 의식'에서 영향받았다."
            ),
            "strength": "강함",
            "period": "19세기 중반"
        }
    ]

    # 기존에 spinoza → hegel 관계가 있는지 확인
    try:
        existing = client.get(index=INDEX_RELATIONS, id="relation-spinoza-hegel")
        print(f"[relation] relation-spinoza-hegel: 이미 존재 (skip)")
    except Exception:
        # 존재하지 않으면 삽입하지 않음 (spinoza 스크립트에서 이미 입력되어 있을 수 있음)
        print("[relation] relation-spinoza-hegel: 미존재 (spinoza 스크립트에서 입력 필요)")

    for rel in relations:
        result = client.index(index=INDEX_RELATIONS, id=rel["id"], document=rel)
        print(f"[relation] {rel['id']}: {result['result']}")

    return len(relations)


def verify_data(client):
    """입력된 데이터를 전수 확인."""
    print("\n=== 전수 확인 ===")

    # refresh
    client.indices.refresh(index=INDEX_THINKERS)
    client.indices.refresh(index=INDEX_WORKS)
    client.indices.refresh(index=INDEX_CLAIMS)
    client.indices.refresh(index=INDEX_KEYWORDS)
    client.indices.refresh(index=INDEX_RELATIONS)

    # thinker 확인
    r = client.get(index=INDEX_THINKERS, id="hegel")
    print(f"[thinker] hegel: name={r['_source']['name_en']}, era={r['_source']['era']}")

    # works 확인
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "hegel"}})
    print(f"[works] hegel 저서 수: {works_count['count']}")
    works_result = client.search(
        index=INDEX_WORKS,
        query={"term": {"thinker_id": "hegel"}},
        _source=["id", "title_original", "year"]
    )
    for hit in works_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['title_original']} ({s['year']})")

    # claims 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "hegel"}})
    print(f"[claims] hegel 주장 수: {claims_count['count']}")
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "hegel"}},
        size=10,
        _source=["id", "claim", "argument", "counterpoint", "original_text", "original_text_ko", "verified"]
    )
    missing_fields = []
    for hit in claims_result['hits']['hits']:
        s = hit['_source']
        has_arg = bool(s.get('argument'))
        has_cp = bool(s.get('counterpoint'))
        has_ot = bool(s.get('original_text'))
        has_otko = bool(s.get('original_text_ko'))
        print(f"  - {s['id']}: argument={has_arg}, counterpoint={has_cp}, "
              f"original_text={has_ot}, original_text_ko={has_otko}, verified={s.get('verified')}")
        if not has_arg or not has_cp or not has_ot or not has_otko:
            missing_fields.append(s['id'])

    if missing_fields:
        print(f"[경고] 필수 필드 누락: {missing_fields}")
    else:
        print("[OK] 모든 claim에 argument+counterpoint+original_text+original_text_ko 존재")

    # keywords 확인
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "hegel"}})
    print(f"[keywords] hegel 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_count_from = client.count(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "hegel"}},
            {"term": {"to_thinker": "hegel"}}
        ]}}
    )
    print(f"[relations] hegel 관련 관계 수: {rel_count_from['count']}")
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "hegel"}},
            {"term": {"to_thinker": "hegel"}}
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
        "relations": rel_count_from['count'],
        "missing_fields": missing_fields
    }


def main():
    client = get_client()
    try:
        print("=== 게오르크 빌헬름 프리드리히 헤겔(G.W.F. Hegel) 데이터 입력 시작 ===\n")

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
