"""프리드리히 니체(Friedrich Nietzsche) 데이터를 ES에 직접 입력하는 스크립트."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS
)


def insert_thinker(client):
    """니체 사상가 데이터 입력."""
    doc = {
        "id": "nietzsche",
        "name": "프리드리히 니체",
        "name_en": "Friedrich Nietzsche",
        "field": "western_ethics",
        "era": "근대/현대 전환기",
        "birth_year": 1844,
        "death_year": 1900,
        "background": (
            "프로이센 뢰켄(Röcken)에서 루터교 목사의 아들로 태어났다. "
            "아버지가 5세 때 사망한 뒤 어머니와 여동생 아래에서 성장했다. "
            "본(Bonn)과 라이프치히(Leipzig) 대학에서 고전문헌학을 공부했으며, "
            "24세의 나이로 바젤(Basel) 대학 고전문헌학 교수로 임명되었다. "
            "작곡가 리하르트 바그너(Richard Wagner)와 깊은 우정을 맺었으나 "
            "이후 결별했다. 루 살로메(Lou Salomé)와의 관계가 좌절된 뒤 "
            "고독한 방랑 생활을 이어갔다. 만성적 건강 악화에 시달리며 "
            "1879년 교수직을 사임한 뒤 이탈리아·스위스·프랑스를 떠돌며 집필했다. "
            "1889년 토리노에서 정신 붕괴를 겪었고, 이후 11년간 정신착란 상태에서 "
            "1900년 바이마르에서 사망했다."
        ),
        "core_philosophy": (
            "니체 철학의 핵심은 기존 서양 형이상학과 기독교 도덕에 대한 근본적 전복이다. "
            "'신은 죽었다(Gott ist tot)'는 선언을 통해 전통적 가치 체계의 붕괴를 진단하고, "
            "위버멘쉬(Übermensch)를 새로운 가치 창조의 이상으로 제시한다. "
            "영원회귀(Ewige Wiederkehr)는 삶의 무조건적 긍정을 요구하는 최고의 시험이며, "
            "힘에의 의지(Wille zur Macht)는 삶의 근본 원리로서 모든 존재의 자기 초극 충동이다. "
            "도덕의 계보학적 분석을 통해 주인도덕(Herrenmoral)과 노예도덕(Sklavenmoral)의 "
            "이중 기원을 폭로하고, '가치의 전도(Umwertung aller Werte)'를 통해 "
            "삶을 부정하는 금욕주의적 이상을 극복하고 디오니소스적 삶의 긍정을 추구한다."
        ),
        "philosophical_journey": (
            "초기(1869~1876): 바젤 교수 시기. 쇼펜하우어의 의지 형이상학과 바그너 예술에 열광하며 "
            "'비극의 탄생'(1872)에서 디오니소스적-아폴론적 이원론을 제시했다. "
            "중기(1876~1882): 바그너와 결별하고 '자유정신' 시기로 전환. "
            "'인간적인 너무나 인간적인'(1878)에서 형이상학적 사유에서 벗어나 "
            "심리학적·과학적 방법으로 도덕과 문화를 분석했다. "
            "'즐거운 학문'(1882)에서 '신의 죽음'을 처음 선언했다. "
            "후기(1883~1888): 사상적 절정기. '차라투스트라'(1883~1885)에서 위버멘쉬와 영원회귀를, "
            "'선악의 저편'(1886)과 '도덕의 계보'(1887)에서 도덕의 계보학적 해체를 수행했다. "
            "'우상의 황혼', '안티크리스트', 'Ecce Homo'(모두 1888)에서 "
            "가치의 전도 프로젝트를 완성하려 했으나 1889년 정신 붕괴로 중단되었다."
        ),
        "keywords": [
            "위버멘쉬(Übermensch)",
            "영원회귀(Ewige Wiederkehr)",
            "힘에의 의지(Wille zur Macht)",
            "주인도덕/노예도덕(Herren-/Sklavenmoral)",
            "가치의 전도(Umwertung aller Werte)",
            "르상티망(Ressentiment)"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="nietzsche", document=doc)
    print(f"[thinker] nietzsche: {result['result']}")
    return result


def insert_works(client):
    """니체 저서 데이터 입력."""
    works = [
        {
            "id": "nietzsche-zarathustra",
            "thinker_id": "nietzsche",
            "title": "차라투스트라는 이렇게 말했다",
            "title_original": "Also sprach Zarathustra",
            "year": 1885,
            "significance": (
                "니체 철학의 정수를 문학적 형식으로 담아낸 대표작. "
                "예언자 차라투스트라의 입을 빌려 위버멘쉬(Übermensch), "
                "영원회귀(Ewige Wiederkehr des Gleichen), 힘에의 의지(Wille zur Macht)라는 "
                "핵심 사상을 제시한다. 4부로 구성되어 1883~1885년에 걸쳐 출간되었다. "
                "차라투스트라가 10년간의 고독한 은둔 끝에 산에서 내려와 "
                "인간에게 위버멘쉬를 가르치는 이야기로 시작한다. "
                "'신은 죽었다'는 진단 위에서 새로운 가치 창조의 길을 제시하는 '만인을 위한, "
                "그러나 누구를 위한 것도 아닌 책(Ein Buch für Alle und Keinen)'이다."
            ),
            "key_concepts": [
                "위버멘쉬", "영원회귀", "힘에의 의지",
                "낙타-사자-어린아이의 세 변화", "마지막 인간", "정오"
            ]
        },
        {
            "id": "nietzsche-jenseits",
            "thinker_id": "nietzsche",
            "title": "선악의 저편",
            "title_original": "Jenseits von Gut und Böse",
            "year": 1886,
            "significance": (
                "차라투스트라의 시적 형식을 산문적·논증적 형식으로 전환한 저작. "
                "부제 '미래 철학의 서곡(Vorspiel einer Philosophie der Zukunft)'이 시사하듯, "
                "기존 철학적 편견들을 해체하고 새로운 철학의 방향을 제시한다. "
                "진리에의 의지, 자유정신, '좋은 것과 나쁜 것' 대 '선과 악'의 구별, "
                "민족과 조국, 고귀함의 의미 등 9장으로 구성된다. "
                "주인도덕과 노예도덕의 대비를 본격적으로 전개한 저작이다."
            ),
            "key_concepts": [
                "주인도덕과 노예도덕", "자유정신", "진리에의 의지",
                "관점주의", "고귀함", "미래의 철학자"
            ]
        },
        {
            "id": "nietzsche-genealogie",
            "thinker_id": "nietzsche",
            "title": "도덕의 계보",
            "title_original": "Zur Genealogie der Moral",
            "year": 1887,
            "significance": (
                "'선악의 저편'의 보론이자 니체 도덕 비판의 가장 체계적인 저작. "
                "세 편의 논문으로 구성된다: (1) '선과 악', '좋음과 나쁨'의 기원, "
                "(2) 양심의 가책과 그에 관련된 것들, (3) 금욕주의적 이상의 의미. "
                "도덕적 가치 판단의 역사적·심리적 기원을 추적하는 '계보학(Genealogie)' 방법을 "
                "확립했다. 르상티망(Ressentiment)에서 노예도덕이 탄생하는 과정, "
                "양심의 가책이 인간의 본능적 공격성의 내면화에서 비롯됨을 분석한다."
            ),
            "key_concepts": [
                "계보학", "르상티망", "양심의 가책", "금욕주의적 이상",
                "주인도덕/노예도덕", "약속할 수 있는 동물"
            ]
        },
        {
            "id": "nietzsche-froehliche-wissenschaft",
            "thinker_id": "nietzsche",
            "title": "즐거운 학문",
            "title_original": "Die fröhliche Wissenschaft",
            "year": 1882,
            "significance": (
                "니체 중기에서 후기로의 전환을 보여주는 핵심 저작. "
                "'신은 죽었다(Gott ist tot)'라는 유명한 선언이 처음 등장하는 책(§125, 광인)이다. "
                "영원회귀 사상도 이 책의 마지막 아포리즘(§341)에서 처음 제시되었다. "
                "부제 'la gaya scienza'는 프로방스 음유시인들의 즐거운 기예를 가리키며, "
                "학문적 엄숙함을 넘어 춤추는 정신, 웃는 지혜를 추구한다. "
                "1882년 초판은 4권이었으나, 1887년 제5권과 서문을 추가한 제2판이 출간되었다."
            ),
            "key_concepts": [
                "신의 죽음", "영원회귀", "la gaya scienza",
                "그림자의 발견", "위대한 건강", "자유정신"
            ]
        }
    ]

    for work in works:
        result = client.index(index=INDEX_WORKS, id=work["id"], document=work)
        print(f"[work] {work['id']}: {result['result']}")

    return len(works)


def insert_claims(client):
    """니체 핵심 주장 데이터 입력."""
    claims = [
        # CLAIM-001: 신의 죽음 (Der Tod Gottes)
        {
            "id": "nietzsche-claim-001",
            "thinker_id": "nietzsche",
            "work_id": "nietzsche-froehliche-wissenschaft",
            "source_detail": "Die fröhliche Wissenschaft, §125 (Der tolle Mensch)",
            "claim": (
                "신은 죽었다. 그리고 우리가 신을 죽인 것이다. "
                "전통적 형이상학과 기독교 도덕의 최고 가치가 더 이상 구속력을 갖지 못하게 되었으며, "
                "이로써 서양 문명의 가치 체계 전체가 근본적 위기에 처했다."
            ),
            "original_text": (
                "Gott ist todt! Gott bleibt todt! Und wir haben ihn getödtet! "
                "Wie trösten wir uns, die Mörder aller Mörder? "
                "Das Heiligste und Mächtigste, was die Welt bisher besaß, "
                "es ist unter unsern Messern verblutet. "
                "(Die fröhliche Wissenschaft, §125)"
            ),
            "original_text_ko": (
                "신은 죽었다! 신은 죽은 채로 있다! 그리고 우리가 그를 죽인 것이다! "
                "모든 살인자 중의 살인자인 우리는 어떻게 스스로를 위로할 것인가? "
                "세계가 지금까지 소유했던 가장 신성하고 강력한 것이 "
                "우리의 칼 아래서 피를 흘렸다. (즐거운 학문, §125)"
            ),
            "explanation": (
                "'신의 죽음'은 단순한 무신론적 주장이 아니라 서양 형이상학 전체의 붕괴를 진단하는 "
                "문명사적 사건이다. 플라톤의 이데아, 기독교의 신, 계몽의 이성 등 "
                "초감성적 세계(übersinnliche Welt)가 더 이상 삶의 의미와 방향을 제공하지 못하게 된 상황, "
                "즉 니힐리즘(Nihilismus)의 도래를 의미한다. "
                "니체에게 이 사건은 두려움과 해방의 이중적 의미를 갖는다."
            ),
            "argument": (
                "(1) 서양 문명은 2천 년간 초감성적 세계(이데아, 신, 이성)를 최고 가치로 삼아왔다. "
                "(2) 근대 과학과 비판 정신의 발전으로 이 초감성적 세계의 실재성이 의심받게 되었다. "
                "(3) 최고 가치가 탈가치화(Entwertung)되면서 '왜?'에 대한 답이 사라졌다(니힐리즘). "
                "(4) 이는 단순한 신앙의 상실이 아니라 진리·도덕·목적 등 서양적 가치 체계 전체의 위기이다. "
                "(5) 그러나 이 위기는 동시에 새로운 가치 창조의 기회이다."
            ),
            "counterpoint": (
                "카를 야스퍼스(Karl Jaspers, 1883~1969)는 '니체: 그의 철학에 대한 입문'(Nietzsche: "
                "Einführung in das Verständnis seines Philosophierens, 1936)에서 "
                "니체의 '신의 죽음' 선언이 실존적 한계상황에 대한 진지한 대면이지만, "
                "초월자(Transzendenz)를 완전히 부정할 수는 없다고 주장했다. "
                "야스퍼스에 따르면, 실존은 초월자와의 관계 속에서만 본래적이 될 수 있으며, "
                "니체 자신의 영원회귀 사상도 일종의 초월적 긍정으로 읽을 수 있다."
            ),
            "context": (
                "헤겔 좌파, 포이어바흐의 종교 비판, 다윈의 진화론 등 "
                "19세기 유럽의 세속화 과정 속에서 형성된 사상이다."
            ),
            "keywords": ["신의 죽음", "니힐리즘", "Gott ist tot", "탈가치화"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-002: 위버멘쉬 (Übermensch)
        {
            "id": "nietzsche-claim-002",
            "thinker_id": "nietzsche",
            "work_id": "nietzsche-zarathustra",
            "source_detail": "Also sprach Zarathustra, Zarathustras Vorrede §3-4",
            "claim": (
                "위버멘쉬(Übermensch)는 인간이 극복해야 할 목표이다. "
                "인간은 짐승과 위버멘쉬 사이에 걸쳐진 밧줄이며, "
                "자기 자신을 넘어서 새로운 가치를 창조할 수 있는 존재이다."
            ),
            "original_text": (
                "Ich lehre euch den Übermenschen. Der Mensch ist Etwas, "
                "das überwunden werden soll. Was habt ihr gethan, ihn zu überwinden? "
                "Alle Wesen bisher schufen Etwas über sich hinaus: "
                "und ihr wollt die Ebbe dieser grossen Fluth sein "
                "und lieber noch zum Thiere zurückgehn, als den Menschen überwinden? "
                "(Also sprach Zarathustra, Vorrede §3)"
            ),
            "original_text_ko": (
                "나는 너희에게 위버멘쉬를 가르친다. 인간은 극복되어야 할 그 무엇이다. "
                "너희는 인간을 극복하기 위해 무엇을 했는가? "
                "지금까지 모든 존재는 자기 자신을 넘어서는 무언가를 창조해왔다: "
                "그런데 너희는 이 위대한 밀물의 썰물이 되고 싶으며, "
                "인간을 극복하기보다 차라리 짐승으로 되돌아가고 싶은가? "
                "(차라투스트라는 이렇게 말했다, 서문 §3)"
            ),
            "explanation": (
                "위버멘쉬는 나치즘이 왜곡한 '초인(Superman)' 개념과 근본적으로 다르다. "
                "이는 인종적 우월성이 아니라, 자기 극복과 새로운 가치 창조의 이상을 의미한다. "
                "신의 죽음 이후 의미의 공백을 채울 수 있는 존재, "
                "삶 자체를 있는 그대로 긍정하며 자신만의 가치를 창조하는 존재이다. "
                "'마지막 인간(der letzte Mensch)'은 위버멘쉬의 대립항으로, "
                "안락과 편안함만을 추구하며 자기 극복을 포기한 인간 유형이다."
            ),
            "argument": (
                "(1) 신의 죽음으로 인간에게 주어졌던 초월적 의미가 사라졌다. "
                "(2) 인간은 동물과 위버멘쉬 사이의 '다리(Brücke)'이지 목적이 아니다. "
                "(3) 정신의 세 변화(낙타→사자→어린아이)를 통해 인간은 기존 가치의 짐을 지고(낙타), "
                "   '너는 해야 한다(Du sollst)'에 맞서 '나는 원한다(Ich will)'를 외치며(사자), "
                "   마침내 망각과 새 시작의 놀이를 통해 새로운 가치를 창조한다(어린아이). "
                "(4) 위버멘쉬는 도달할 수 없는 이상이 아니라 자기 극복의 끊임없는 과정이다."
            ),
            "counterpoint": (
                "마르틴 하이데거(Martin Heidegger, 1889~1976)는 '니체'(Nietzsche, 1961, "
                "1936~1946년 강의록)에서 위버멘쉬 개념을 형이상학의 완성이자 동시에 한계로 해석했다. "
                "하이데거에 따르면 니체의 위버멘쉬는 힘에의 의지의 주체로서 "
                "존재자 전체에 대한 무조건적 지배를 추구하는 근대 주체성의 극단이며, "
                "이는 존재 자체의 의미에 대한 물음을 오히려 은폐한다."
            ),
            "context": (
                "다윈의 진화론적 영향(인간은 고정된 존재가 아닌 발전하는 존재), "
                "쇼펜하우어의 의지 형이상학, 에머슨의 '자기 신뢰(Self-Reliance)' 사상의 영향."
            ),
            "keywords": ["위버멘쉬", "Übermensch", "자기 극복", "마지막 인간", "세 변화"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-003: 영원회귀 (Ewige Wiederkehr)
        {
            "id": "nietzsche-claim-003",
            "thinker_id": "nietzsche",
            "work_id": "nietzsche-froehliche-wissenschaft",
            "source_detail": "Die fröhliche Wissenschaft, §341; Also sprach Zarathustra, III. Teil",
            "claim": (
                "영원회귀(Ewige Wiederkehr des Gleichen)는 동일한 삶이 무한히 반복된다는 사상이다. "
                "이것은 우주론적 가설이라기보다 삶에 대한 최고의 긍정을 시험하는 "
                "실존적 사유실험이다."
            ),
            "original_text": (
                "Was, wenn dir eines Tages oder Nachts, ein Dämon in deine einsamste "
                "Einsamkeit nachschliche und dir sagte: 'Dieses Leben, wie du es jetzt "
                "lebst und gelebt hast, wirst du noch einmal und noch unzählige Male leben "
                "müssen; und es wird nichts Neues daran sein, sondern jeder Schmerz und "
                "jede Lust und jeder Gedanke und Seufzer... muß dir wiederkommen...' "
                "(Die fröhliche Wissenschaft, §341)"
            ),
            "original_text_ko": (
                "만약 어느 날 혹은 어느 밤, 한 악마가 네 가장 외로운 고독 속으로 "
                "몰래 스며들어 이렇게 말한다면: '너는 지금 살고 있고 살아온 이 삶을 "
                "다시 한 번, 그리고 무수히 반복하여 살아야 할 것이다; "
                "거기에는 새로운 것이라곤 아무것도 없을 것이며, "
                "모든 고통과 기쁨, 모든 생각과 탄식이... 너에게 되돌아와야 한다...' "
                "(즐거운 학문, §341)"
            ),
            "explanation": (
                "영원회귀는 니체 사상에서 가장 심원하고 논쟁적인 개념이다. "
                "이것이 물리적 우주론(동일한 것의 실제적 반복)인지, "
                "순수한 윤리적 사유실험(삶을 긍정하는가의 시금석)인지에 대해 "
                "학자들 사이에 논쟁이 있다. 니체는 과학적 근거를 제시하려 했으나 "
                "(유고에서 물리학적 논증 시도) 완성하지 못했다. "
                "중요한 것은 이 사상이 삶에 대한 태도의 시험이라는 점이다: "
                "영원회귀를 기꺼이 원할 수 있는가?"
            ),
            "argument": (
                "(1) 만약 이 삶이 영원히 동일하게 반복된다면, 그것을 원할 수 있는가? "
                "(2) 이 질문에 '예!'라고 답할 수 있다면, 그것이 삶에 대한 최고의 긍정이다. "
                "(3) 영원회귀는 저편 세계(내세, 천국)에 의미를 투사하는 태도를 근본적으로 차단한다. "
                "(4) 모든 순간이 영원한 의미를 가지므로, '지금 여기'의 삶을 온전히 긍정해야 한다. "
                "(5) 차라투스트라의 '정오(der große Mittag)'는 영원회귀를 깨달아 삶을 전적으로 긍정하는 순간이다."
            ),
            "counterpoint": (
                "게오르그 짐멜(Georg Simmel, 1858~1918)은 '쇼펜하우어와 니체'(Schopenhauer und "
                "Nietzsche, 1907)에서 영원회귀의 우주론적 논증이 논리적으로 타당하지 않다고 비판했다. "
                "유한한 힘의 무한한 시간에 걸친 재조합이 반드시 동일한 배열의 반복을 보장하지 않으며, "
                "설사 반복이 실재한다 해도 의식이 없는 반복은 윤리적 의미를 갖지 못한다고 지적했다."
            ),
            "context": (
                "고대 스토아학파의 우주적 순환론, 피타고라스학파의 영원회귀 관념, "
                "보스코비치(Boscovich)의 역학적 세계관의 영향."
            ),
            "keywords": ["영원회귀", "Ewige Wiederkehr", "삶의 긍정", "amor fati"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-004: 힘에의 의지 (Wille zur Macht)
        {
            "id": "nietzsche-claim-004",
            "thinker_id": "nietzsche",
            "work_id": "nietzsche-jenseits",
            "source_detail": "Jenseits von Gut und Böse, §36; Also sprach Zarathustra, II. Teil 'Von der Selbst-Ueberwindung'",
            "claim": (
                "힘에의 의지(Wille zur Macht)는 삶의 근본 원리이다. "
                "모든 살아있는 것은 자기 보존이 아니라 자기 초극, 힘의 증대를 추구한다. "
                "이것은 물리적 폭력이 아니라 자기 극복, 창조, 성장의 충동이다."
            ),
            "original_text": (
                "Wo ich Lebendiges fand, da fand ich Willen zur Macht; "
                "und noch im Willen des Dienenden fand ich den Willen, Herr zu sein. "
                "(Also sprach Zarathustra, II. Teil, Von der Selbst-Ueberwindung)"
            ),
            "original_text_ko": (
                "내가 살아있는 것을 발견한 곳에서, 나는 힘에의 의지를 발견했다; "
                "그리고 섬기는 자의 의지 속에서도 나는 주인이 되려는 의지를 발견했다. "
                "(차라투스트라는 이렇게 말했다, 제2부, 자기 극복에 대하여)"
            ),
            "explanation": (
                "힘에의 의지는 쇼펜하우어의 '삶에의 의지(Wille zum Leben)'를 비판적으로 계승한 것이다. "
                "쇼펜하우어가 의지를 맹목적 충동으로 보고 부정을 권했다면, "
                "니체는 의지를 자기 초극의 창조적 힘으로 긍정한다. "
                "다윈의 생존 본능(자기 보존)도 니체가 보기에 불충분하다: "
                "생명은 단순히 살아남으려 하는 것이 아니라 자신을 넘어서려 한다. "
                "이 개념은 니체 사후 여동생 엘리자베트가 편집한 '힘에의 의지' 유고 편집본으로 인해 "
                "왜곡되었으나, 니체 자신의 저작에서는 자기 극복의 원리로 제시된다."
            ),
            "argument": (
                "(1) 쇼펜하우어의 '삶에의 의지'는 맹목적 자기 보존이지만, 생명의 실상을 관찰하면 "
                "   보존보다 성장과 확장을 추구하는 경향이 발견된다. "
                "(2) 모든 유기적 기능은 힘의 증대를 목표로 하며, 자기 보존은 그 부수적 결과에 불과하다. "
                "(3) 인식조차도 힘에의 의지의 한 형태이다: 세계를 파악한다는 것은 세계를 자기 것으로 "
                "   만든다는 것이다(관점주의). "
                "(4) 도덕적 가치도 힘에의 의지의 표현이다: 주인도덕은 힘의 풍요에서, "
                "   노예도덕은 힘의 결핍에서 나온다."
            ),
            "counterpoint": (
                "위르겐 하버마스(Jürgen Habermas, 1929~)는 '근대의 철학적 담론'(Der philosophische "
                "Diskurs der Moderne, 1985)에서 니체의 힘에의 의지를 비판적으로 분석했다. "
                "하버마스에 따르면, 니체가 이성 비판을 수행하면서 이성의 자리에 힘에의 의지를 놓는 것은 "
                "수행적 모순(performativer Widerspruch)에 빠지며, "
                "권력의 자의적 행사를 정당화할 위험이 있다."
            ),
            "context": (
                "쇼펜하우어의 의지 형이상학에 대한 비판적 전환, "
                "다윈주의 생물학에 대한 비판적 수용(생존이 아닌 성장이 생명의 본질)."
            ),
            "keywords": ["힘에의 의지", "Wille zur Macht", "자기 극복", "관점주의"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-005: 주인도덕과 노예도덕 (Herren- und Sklavenmoral)
        {
            "id": "nietzsche-claim-005",
            "thinker_id": "nietzsche",
            "work_id": "nietzsche-genealogie",
            "source_detail": "Zur Genealogie der Moral, Erste Abhandlung; Jenseits von Gut und Böse, §260",
            "claim": (
                "도덕에는 두 가지 근본적으로 다른 유형이 있다. "
                "주인도덕(Herrenmoral)은 힘의 풍요에서 '좋음(gut)'과 '나쁨(schlecht)'을 구별하고, "
                "노예도덕(Sklavenmoral)은 르상티망에서 '선(gut)'과 '악(böse)'을 구별한다."
            ),
            "original_text": (
                "Der Sklavenaufstand in der Moral beginnt damit, "
                "daß das Ressentiment selbst schöpferisch wird und Werthe gebiert: "
                "das Ressentiment solcher Wesen, denen die eigentliche Reaktion, "
                "die der That, versagt ist, die sich nur durch eine imaginäre Rache "
                "schadlos halten. "
                "(Zur Genealogie der Moral, Erste Abhandlung, §10)"
            ),
            "original_text_ko": (
                "도덕에서의 노예 반란은 르상티망 자체가 창조적으로 되어 "
                "가치를 낳는 것으로 시작된다: "
                "본래적 반응인 행동이 거부된 존재들, "
                "상상적 복수를 통해서만 자신의 손해를 만회하는 "
                "그러한 존재들의 르상티망. "
                "(도덕의 계보, 제1논문, §10)"
            ),
            "explanation": (
                "니체는 도덕의 계보학적 분석을 통해 도덕적 가치 판단의 이중 기원을 폭로한다. "
                "주인도덕은 강자가 자기 자신의 풍요로운 삶을 '좋은 것'으로, "
                "그렇지 못한 것을 단지 '나쁜 것'으로 평가한다(자기 긍정). "
                "노예도덕은 약자가 자신을 억압하는 강자를 '악'으로 규정하고, "
                "그에 대한 반동으로 자신의 약함을 '선'으로 재해석한다(타자 부정). "
                "기독교 도덕은 전형적인 노예도덕의 승리로, 겸손·동정·금욕 등의 덕이 "
                "실은 약자의 르상티망에서 비롯되었다는 것이 니체의 분석이다."
            ),
            "argument": (
                "(1) 역사적으로 '좋은(gut)'이라는 말은 원래 '고귀한, 귀족적인'을 뜻했고, "
                "   '나쁜(schlecht)'은 '비천한, 평민적인'을 뜻했다(어원학적 분석). "
                "(2) 강자(귀족)는 자기 자신의 삶을 긍정하고 '좋음'을 먼저 설정한다(능동적 가치 정립). "
                "(3) 약자(노예)는 행동할 힘이 없으므로 르상티망(Ressentiment)을 품는다. "
                "(4) 르상티망은 먼저 강자를 '악(böse)'으로 규정한 뒤, "
                "   그 반동으로 자신의 약함을 '선(gut)'으로 재해석한다(반동적 가치 정립). "
                "(5) 유대교의 성직자적 가치 전도가 이 노예 반란의 기원이며, "
                "   기독교가 그 승리를 완성했다."
            ),
            "counterpoint": (
                "막스 셸러(Max Scheler, 1874~1928)는 '윤리학에서의 르상티망'(Das Ressentiment "
                "im Aufbau der Moralen, 1912)에서 니체의 분석을 부분적으로 수용하면서도, "
                "기독교의 사랑(Agape)이 르상티망에서 비롯된 것이 아니라 "
                "힘의 풍요에서 나오는 진정한 가치 감정이라고 반박했다. "
                "셸러에 따르면, 니체는 부르주아적 인도주의(Humanitarismus)의 동정을 "
                "기독교적 사랑과 혼동한 것이다."
            ),
            "context": (
                "고대 로마의 귀족 윤리, 초기 기독교의 로마 제국 내 가치 전도, "
                "파울 레(Paul Rée)의 '도덕 감정의 기원'(1877)에 대한 비판적 발전."
            ),
            "keywords": ["주인도덕", "노예도덕", "르상티망", "Ressentiment", "가치 전도"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-006: 가치의 전도 (Umwertung aller Werte)
        {
            "id": "nietzsche-claim-006",
            "thinker_id": "nietzsche",
            "work_id": "nietzsche-jenseits",
            "source_detail": "Jenseits von Gut und Böse, Vorrede; Zur Genealogie der Moral, Vorrede §6",
            "claim": (
                "가치의 전도(Umwertung aller Werte)는 기존의 모든 가치 체계를 "
                "근본적으로 재평가하고 전복하는 과제이다. "
                "플라톤적-기독교적 도덕이 삶을 부정하는 가치 체계임을 폭로하고, "
                "삶을 긍정하는 새로운 가치를 정립해야 한다."
            ),
            "original_text": (
                "Man darf wohl vor Allem über die Plumpheit und Bäuerlichkeit der Moral "
                "erstaunen, die damit in Europa zur Herrschaft kam, "
                "insofern fast jede höhere, feinere, kühnere Moral als ihr Widerpart "
                "verfemt und der Oeffentlichkeit als böse verschrieen wurde. "
                "(Jenseits von Gut und Böse, §199)"
            ),
            "original_text_ko": (
                "무엇보다 유럽에서 지배권을 잡은 도덕의 투박함과 촌스러움에 "
                "놀라지 않을 수 없다. 거의 모든 더 고귀하고, 섬세하고, 대담한 도덕은 "
                "그에 대한 반대물로 낙인찍히고, 대중 앞에서 악으로 비난받았으니 말이다. "
                "(선악의 저편, §199)"
            ),
            "explanation": (
                "'가치의 전도'는 니체 후기 철학의 최종 과제이자 미완의 프로젝트이다. "
                "니체는 원래 '힘에의 의지: 모든 가치의 전도 시도(Versuch einer Umwertung "
                "aller Werthe)'라는 주저를 계획했으나 완성하지 못했다. "
                "이 과제의 핵심은 (1) 기존 가치 체계의 계보학적 해체와 "
                "(2) 새로운 가치의 창조이다. 플라톤 이래 서양 형이상학이 "
                "'참된 세계(wahre Welt)'를 설정하고 현실 세계를 '가상(Schein)'으로 "
                "폄하해온 것을 뒤집어야 한다."
            ),
            "argument": (
                "(1) 서양 형이상학은 '참된 세계'(이데아, 신의 나라, 물자체)를 상정하고 "
                "   감각적 현실을 '가상'으로 폄하해왔다. "
                "(2) 이 이원론적 구도는 삶 자체를 부정하는 것이다: 현실의 삶은 열등하고 "
                "   '저편'의 세계만이 진정한 가치를 갖는다는 금욕주의적 이상. "
                "(3) '참된 세계'는 허구임이 드러났으므로(신의 죽음) 가상 세계도 폐기된다: "
                "   남는 것은 '이' 세계뿐이다. "
                "(4) 따라서 삶을 부정하는 가치 체계를 전도하고, "
                "   삶을 긍정하는 가치를 새로 창조해야 한다(디오니소스적 긍정)."
            ),
            "counterpoint": (
                "레오 슈트라우스(Leo Strauss, 1899~1973)는 '근대성의 세 물결'(Three Waves of "
                "Modernity, 1975)에서 니체의 가치의 전도가 역사주의와 상대주의를 극단으로 밀고 간 "
                "'제3의 물결'이라고 비판했다. 슈트라우스에 따르면, 모든 가치의 전도는 "
                "자연적 정의(natural right)의 가능성을 파괴하며, "
                "이는 결국 정치적 허무주의로 귀결될 수밖에 없다."
            ),
            "context": (
                "플라톤 이데아론에서 칸트 물자체론에 이르는 서양 이원론적 형이상학, "
                "기독교 금욕주의적 이상, 근대 계몽의 진보 신앙에 대한 총체적 비판."
            ),
            "keywords": ["가치의 전도", "Umwertung aller Werte", "금욕주의적 이상", "이원론 비판"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-007: 디오니소스적 긍정
        {
            "id": "nietzsche-claim-007",
            "thinker_id": "nietzsche",
            "work_id": "nietzsche-zarathustra",
            "source_detail": "Die Geburt der Tragödie; Ecce Homo; Götzen-Dämmerung",
            "claim": (
                "디오니소스적 긍정은 삶의 고통과 모순을 회피하지 않고 "
                "전적으로 긍정하는 태도이다. 삶의 비극적 측면까지 포함한 "
                "무조건적 긍정이 니체 철학의 최종 목표이다."
            ),
            "original_text": (
                "Meine Formel für die Größe am Menschen ist amor fati: "
                "daß man Nichts anders haben will, vorwärts nicht, rückwärts nicht, "
                "in alle Ewigkeit nicht. Das Nothwendige nicht bloß ertragen, "
                "noch weniger verhehlen... sondern es lieben... "
                "(Ecce Homo, Warum ich so klug bin, §10)"
            ),
            "original_text_ko": (
                "인간의 위대함에 대한 나의 공식은 운명애(amor fati)이다: "
                "앞으로도, 뒤로도, 온 영원에 걸쳐서도 달리 되기를 원하지 않는 것. "
                "필연적인 것을 단지 견디는 것이 아니라, "
                "더구나 그것을 숨기는 것은 더더욱 아니라... 그것을 사랑하는 것... "
                "(이 사람을 보라, 나는 왜 이렇게 영리한지, §10)"
            ),
            "explanation": (
                "디오니소스는 니체 철학의 출발점이자 귀결점이다. 초기 저작 '비극의 탄생'(1872)에서 "
                "디오니소스적인 것(Rausch, 도취, 근원적 일자와의 합일)과 "
                "아폴론적인 것(Traum, 꿈, 개체화의 형식)의 대립으로 시작하여, "
                "후기에는 디오니소스가 삶의 무조건적 긍정 전체를 상징하게 된다. "
                "'운명애(amor fati)'는 삶의 고통·모순·비극을 회피하거나 다른 세계로 도피하지 않고 "
                "'이것이 삶이었던가? 좋다! 다시 한번!(War das das Leben? Wohlan! Noch Ein Mal!)'이라고 "
                "말할 수 있는 태도이다."
            ),
            "argument": (
                "(1) 서양 형이상학과 기독교는 삶의 고통에서 벗어나기 위해 '참된 세계'를 설정했다(현실 도피). "
                "(2) 쇼펜하우어도 의지의 맹목적 고통에서 벗어나기 위해 의지의 부정을 권했다(삶의 부정). "
                "(3) 니체는 삶의 고통·모순·비극을 인정하면서도 그것을 전적으로 긍정할 것을 요구한다. "
                "(4) 디오니소스적 긍정은 영원회귀와 결합된다: 이 삶이 영원히 반복된다 해도 "
                "   '다시 한번!'이라고 외칠 수 있는가? "
                "(5) amor fati(운명애)는 단순한 체념이 아니라 필연에 대한 적극적 사랑이다."
            ),
            "counterpoint": (
                "테오도르 아도르노(Theodor W. Adorno, 1903~1969)는 '도덕 철학의 문제들'(Probleme "
                "der Moralphilosophie, 1963 강의)에서 니체의 삶의 무조건적 긍정이 "
                "현존하는 고통과 불의에 대한 비판적 거리를 상실할 위험이 있다고 지적했다. "
                "아우슈비츠 이후의 세계에서 모든 것을 있는 그대로 긍정하는 것은 "
                "폭력과 고통에 대한 묵인이 될 수 있다."
            ),
            "context": (
                "그리스 디오니소스 제의, 그리스 비극(아이스킬로스, 소포클레스), "
                "쇼펜하우어의 비관주의(Pessimismus)에 대한 극복."
            ),
            "keywords": ["디오니소스", "amor fati", "운명애", "삶의 긍정", "비극적 긍정"],
            "verified": False,
            "verification_log": []
        },
        # CLAIM-008: 원한 (Ressentiment)
        {
            "id": "nietzsche-claim-008",
            "thinker_id": "nietzsche",
            "work_id": "nietzsche-genealogie",
            "source_detail": "Zur Genealogie der Moral, Erste Abhandlung, §10-14",
            "claim": (
                "르상티망(Ressentiment)은 노예도덕의 심리적 기제이다. "
                "행동할 힘이 없는 자들이 강자에 대한 원한을 품고, "
                "이 원한이 가치 창조의 동력이 되어 기존 가치 체계를 전도한다."
            ),
            "original_text": (
                "Während alle vornehme Moral aus einem triumphierenden Ja-sagen "
                "zu sich selber herauswächst, sagt die Sklaven-Moral von vornherein "
                "Nein zu einem 'Außerhalb', zu einem 'Anders', zu einem 'Nicht-selbst': "
                "und dies Nein ist ihre schöpferische That. "
                "(Zur Genealogie der Moral, Erste Abhandlung, §10)"
            ),
            "original_text_ko": (
                "모든 고귀한 도덕이 자기 자신에 대한 승리의 긍정에서 자라나는 반면, "
                "노예 도덕은 처음부터 '바깥', '다른 것', '자기가 아닌 것'에 대해 "
                "부정을 말한다: 그리고 이 부정이 그들의 창조적 행위이다. "
                "(도덕의 계보, 제1논문, §10)"
            ),
            "explanation": (
                "르상티망은 단순한 분노나 질투가 아니라, 행동으로 발산되지 못한 복수심이 "
                "내면화되어 가치 판단의 형태로 변형된 것이다. "
                "강자는 자기 자신의 삶을 먼저 긍정하고 '좋음(gut)'을 설정하지만, "
                "약자는 먼저 강자를 '악(böse)'으로 규정한 뒤 그에 대한 반동으로 "
                "자신을 '선(gut)'으로 재해석한다. "
                "이것이 '도덕에서의 노예 반란(Sklavenaufstand in der Moral)'이다. "
                "기독교적 겸손·동정·금욕 등은 이 르상티망의 산물이다."
            ),
            "argument": (
                "(1) 능동적(aktiv) 인간은 즉각적으로 행동하고 반응하므로 원한이 축적되지 않는다. "
                "(2) 반동적(reaktiv) 인간은 행동할 힘이 없으므로 복수심을 내면에 축적한다. "
                "(3) 이 축적된 복수심이 '상상적 복수(imaginäre Rache)'의 형태로 가치를 창조한다. "
                "(4) '너는 악하다, 따라서 나는 선하다'라는 추론이 노예도덕의 기본 구조이다. "
                "(5) 금욕주의적 성직자(asketischer Priester)가 이 르상티망을 조직하고 "
                "   방향을 부여하여 양심의 가책으로 전환시킨다(제2논문)."
            ),
            "counterpoint": (
                "막스 셸러(Max Scheler, 1874~1928)는 '윤리학에서의 르상티망'(Das Ressentiment "
                "im Aufbau der Moralen, 1912)에서 니체의 르상티망 분석을 현상학적으로 정교화하면서도, "
                "기독교적 사랑은 르상티망의 산물이 아니라 가치 서열에 대한 직접적 감정이라고 반박했다. "
                "셸러에 따르면 니체가 비판하는 '동정(Mitleid)'은 부르주아적 인도주의이지 "
                "기독교적 아가페(Agape)가 아니다."
            ),
            "context": (
                "프랑스 모랄리스트(라 로슈푸코 등)의 자기기만 분석, "
                "도스토예프스키의 '지하실의 수기'에 나타난 원한의 심리학."
            ),
            "keywords": ["르상티망", "Ressentiment", "노예 반란", "반동적 가치 정립"],
            "verified": False,
            "verification_log": []
        }
    ]

    for claim in claims:
        result = client.index(index=INDEX_CLAIMS, id=claim["id"], document=claim)
        print(f"[claim] {claim['id']}: {result['result']}")

    return len(claims)


def insert_keywords(client):
    """니체 키워드 데이터 입력."""
    keywords = [
        {
            "id": "nietzsche-kw-001",
            "thinker_id": "nietzsche",
            "term": "위버멘쉬 (Übermensch)",
            "term_original": "Übermensch",
            "definition": (
                "인간이 자기 극복을 통해 도달해야 할 이상. "
                "신의 죽음 이후 의미의 공백을 채울 수 있는 새로운 가치 창조자. "
                "인간은 동물과 위버멘쉬 사이에 걸쳐진 밧줄이며, "
                "정신의 세 변화(낙타→사자→어린아이)를 통해 기존 가치의 짐을 지고, "
                "기존 가치에 저항하며, 마침내 새로운 가치를 창조하는 과정을 거친다. "
                "나치즘이 왜곡한 인종적 '초인' 개념과는 근본적으로 다르다."
            ),
            "related_claims": ["nietzsche-claim-002", "nietzsche-claim-001"],
            "source": "Also sprach Zarathustra, Vorrede §3-4"
        },
        {
            "id": "nietzsche-kw-002",
            "thinker_id": "nietzsche",
            "term": "영원회귀 (Ewige Wiederkehr)",
            "term_original": "Ewige Wiederkehr des Gleichen",
            "definition": (
                "동일한 삶이 무한히 반복된다는 사상. "
                "우주론적 가설이라기보다 삶에 대한 최고의 긍정을 시험하는 실존적 사유실험. "
                "이 삶을 영원히 다시 살아야 한다면 그것을 원할 수 있는가라는 물음은 "
                "삶에 대한 태도의 궁극적 시금석이다. "
                "영원회귀를 기꺼이 원할 수 있는 자가 위버멘쉬에 가까운 존재이다."
            ),
            "related_claims": ["nietzsche-claim-003", "nietzsche-claim-007"],
            "source": "Die fröhliche Wissenschaft, §341; Also sprach Zarathustra, III. Teil"
        },
        {
            "id": "nietzsche-kw-003",
            "thinker_id": "nietzsche",
            "term": "힘에의 의지 (Wille zur Macht)",
            "term_original": "Wille zur Macht",
            "definition": (
                "삶의 근본 원리로서 모든 존재의 자기 초극 충동. "
                "쇼펜하우어의 '삶에의 의지(Wille zum Leben)'를 비판적으로 계승한 개념으로, "
                "단순한 자기 보존이 아니라 힘의 증대, 성장, 자기 극복을 추구하는 충동이다. "
                "물리적 폭력이 아닌 창조·인식·예술 등 모든 생명 활동의 근본 동력. "
                "니체 사후 여동생의 편집으로 왜곡되었으나, 원래는 자기 극복의 원리이다."
            ),
            "related_claims": ["nietzsche-claim-004", "nietzsche-claim-005"],
            "source": "Jenseits von Gut und Böse, §36; Also sprach Zarathustra, II. Teil"
        },
        {
            "id": "nietzsche-kw-004",
            "thinker_id": "nietzsche",
            "term": "주인도덕/노예도덕 (Herren-/Sklavenmoral)",
            "term_original": "Herrenmoral / Sklavenmoral",
            "definition": (
                "도덕의 두 가지 근본 유형. "
                "주인도덕은 강자가 자기 자신의 풍요로운 삶을 '좋은 것(gut)'으로 긍정하고 "
                "그렇지 못한 것을 '나쁜 것(schlecht)'으로 평가하는 능동적 가치 정립. "
                "노예도덕은 약자가 르상티망에서 강자를 '악(böse)'으로 규정하고 "
                "자신의 약함을 '선(gut)'으로 재해석하는 반동적 가치 정립. "
                "기독교 도덕은 노예도덕의 역사적 승리이다."
            ),
            "related_claims": ["nietzsche-claim-005", "nietzsche-claim-008"],
            "source": "Zur Genealogie der Moral, Erste Abhandlung; Jenseits von Gut und Böse, §260"
        },
        {
            "id": "nietzsche-kw-005",
            "thinker_id": "nietzsche",
            "term": "가치의 전도 (Umwertung aller Werte)",
            "term_original": "Umwertung aller Werte",
            "definition": (
                "기존의 플라톤적-기독교적 가치 체계를 근본적으로 재평가하고 전복하는 과제. "
                "'참된 세계'와 '가상 세계'의 이원론을 해체하고, "
                "삶을 부정하는 금욕주의적 이상을 극복하며, "
                "삶을 긍정하는 새로운 가치를 창조하는 것이 목표이다. "
                "니체 후기 철학의 최종 프로젝트이나 미완으로 남았다."
            ),
            "related_claims": ["nietzsche-claim-006", "nietzsche-claim-001"],
            "source": "Jenseits von Gut und Böse, Vorrede; Zur Genealogie der Moral"
        },
        {
            "id": "nietzsche-kw-006",
            "thinker_id": "nietzsche",
            "term": "르상티망 (Ressentiment)",
            "term_original": "Ressentiment",
            "definition": (
                "행동으로 발산되지 못한 복수심이 내면화되어 가치 판단의 형태로 변형된 심리적 기제. "
                "노예도덕의 창조적 원천으로, 강자에 대한 원한이 "
                "'상상적 복수(imaginäre Rache)'를 통해 가치 전도를 산출한다. "
                "능동적 인간은 즉각적으로 반응하므로 르상티망이 축적되지 않지만, "
                "반동적 인간은 행동할 힘이 없어 원한을 내면에 쌓고 "
                "이를 도덕적 판단으로 승화시킨다."
            ),
            "related_claims": ["nietzsche-claim-008", "nietzsche-claim-005"],
            "source": "Zur Genealogie der Moral, Erste Abhandlung, §10-14"
        }
    ]

    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")

    return len(keywords)


def insert_relations(client):
    """니체 관계 데이터 입력."""
    relations = [
        {
            "id": "relation-schopenhauer-nietzsche",
            "from_thinker": "schopenhauer",
            "to_thinker": "nietzsche",
            "type": "influenced",
            "description": (
                "아르투어 쇼펜하우어(Arthur Schopenhauer, 1788~1860)는 니체의 철학적 출발점이다. "
                "니체는 라이프치히 대학 시절 '의지와 표상으로서의 세계'를 읽고 깊은 감명을 받았다. "
                "쇼펜하우어의 의지 형이상학, 예술을 통한 의지의 부정, 비관주의(Pessimismus)는 "
                "니체 초기 사상('비극의 탄생')의 기반이 되었다. "
                "그러나 니체는 점차 쇼펜하우어의 삶의 부정(의지의 부정)을 거부하고, "
                "'삶에의 의지'를 '힘에의 의지'로 전환하며, 비관주의를 디오니소스적 긍정으로 극복했다."
            ),
            "strength": "강함",
            "period": "19세기 중반~후반"
        },
        {
            "id": "relation-nietzsche-heidegger",
            "from_thinker": "nietzsche",
            "to_thinker": "heidegger",
            "type": "influenced",
            "description": (
                "마르틴 하이데거(Martin Heidegger, 1889~1976)는 1936~1946년의 강의에서 "
                "니체를 서양 형이상학의 완성자로 해석했다. "
                "하이데거에 따르면, 니체의 힘에의 의지와 영원회귀는 "
                "플라톤에서 시작된 서양 형이상학(존재자 전체를 존재자성으로 파악하는 사유)의 "
                "극단이자 완성이며, 존재 망각(Seinsvergessenheit)의 최종 형태이다. "
                "니체 해석은 하이데거 후기 사유의 핵심 계기가 되었다."
            ),
            "strength": "강함",
            "period": "20세기 전반"
        },
        {
            "id": "relation-nietzsche-sartre",
            "from_thinker": "nietzsche",
            "to_thinker": "sartre",
            "type": "influenced",
            "description": (
                "장폴 사르트르(Jean-Paul Sartre, 1905~1980)의 실존주의는 "
                "니체의 '신의 죽음' 선언에서 핵심적 영감을 받았다. "
                "사르트르의 '실존은 본질에 앞선다'는 테제와 "
                "'인간은 자유를 선고받았다'는 명제는 "
                "신의 죽음 이후 인간이 스스로 가치를 창조해야 한다는 "
                "니체적 문제의식의 실존주의적 전개이다. "
                "다만 사르트르는 니체의 귀족주의적 요소를 거부하고 "
                "자유와 책임의 보편성을 강조했다."
            ),
            "strength": "보통",
            "period": "20세기 중반"
        },
        {
            "id": "relation-nietzsche-foucault",
            "from_thinker": "nietzsche",
            "to_thinker": "foucault",
            "type": "influenced",
            "description": (
                "미셸 푸코(Michel Foucault, 1926~1984)는 니체의 계보학(Genealogie) 방법을 "
                "직접적으로 계승하여 '지식의 고고학'과 '권력의 계보학'을 발전시켰다. "
                "푸코의 '니체, 계보학, 역사'(Nietzsche, la généalogie, l'histoire, 1971)는 "
                "니체의 방법론을 체계적으로 재해석한 핵심 텍스트이다. "
                "도덕·이성·진리 등의 '기원(Ursprung)'이 아닌 '출현(Entstehung)'과 "
                "'유래(Herkunft)'를 추적하는 계보학적 방법은 "
                "푸코의 감옥·광기·성(性) 연구의 방법론적 토대가 되었다."
            ),
            "strength": "강함",
            "period": "20세기 후반"
        }
    ]

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
    r = client.get(index=INDEX_THINKERS, id="nietzsche")
    print(f"[thinker] nietzsche: name={r['_source']['name_en']}, era={r['_source']['era']}")

    # works 확인
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "nietzsche"}})
    print(f"[works] nietzsche 저서 수: {works_count['count']}")
    works_result = client.search(
        index=INDEX_WORKS,
        query={"term": {"thinker_id": "nietzsche"}},
        _source=["id", "title_original", "year"]
    )
    for hit in works_result['hits']['hits']:
        s = hit['_source']
        print(f"  - {s['id']}: {s['title_original']} ({s['year']})")

    # claims 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "nietzsche"}})
    print(f"[claims] nietzsche 주장 수: {claims_count['count']}")
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "nietzsche"}},
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
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "nietzsche"}})
    print(f"[keywords] nietzsche 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_count_from = client.count(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "nietzsche"}},
            {"term": {"to_thinker": "nietzsche"}}
        ]}}
    )
    print(f"[relations] nietzsche 관련 관계 수: {rel_count_from['count']}")
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "nietzsche"}},
            {"term": {"to_thinker": "nietzsche"}}
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
        print("=== 프리드리히 니체(Friedrich Nietzsche) 데이터 입력 시작 ===\n")

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
