"""순자(荀子, Xunzi) 데이터를 ES에 직접 입력하는 스크립트.

동양윤리 Phase 2의 세 번째 사상가.
출제비중: 핵심 → 표준 규모 (claims 10~12건)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import (
    INDEX_THINKERS, INDEX_WORKS, INDEX_CLAIMS,
    INDEX_KEYWORDS, INDEX_RELATIONS, INDEX_FIELDS
)


def ensure_eastern_ethics_field(client):
    """동양윤리 분야가 ethics-fields 인덱스에 없으면 추가한다."""
    try:
        client.get(index=INDEX_FIELDS, id="eastern_ethics")
        print("[field] eastern_ethics: already exists")
    except Exception:
        doc = {
            "id": "eastern_ethics",
            "name": "동양윤리",
            "description": (
                "동양의 윤리 사상을 다루는 분야. "
                "유교(선진유학, 성리학, 양명학, 한국유학), 도가, 불교, 제자백가 등을 포함한다. "
                "한국 윤리 임용시험에서 서양윤리와 함께 핵심 출제 영역이다."
            ),
            "order": 2
        }
        result = client.index(index=INDEX_FIELDS, id="eastern_ethics", document=doc)
        print(f"[field] eastern_ethics: {result['result']}")


def insert_thinker(client):
    """순자 사상가 데이터 입력."""
    doc = {
        "id": "xunzi",
        "name": "순자",
        "name_en": "Xunzi (Hsün Tzu)",
        "field": "eastern_ethics",
        "era": "전국시대",
        "birth_year": -313,
        "death_year": -238,
        "nationality": "중국 (조나라)",
        "background": (
            "조(趙)나라 출신으로, 이름은 순황(荀況), 존칭은 순경(荀卿) 또는 손경(孫卿). "
            "제(齊)나라 직하학궁(稷下學宮)에서 학문을 닦았으며, "
            "세 번이나 제주(祭酒, 학궁의 수장)를 역임하여 당대 최고의 학자로 인정받았다. "
            "이후 초(楚)나라 춘신군(春申君)의 초빙으로 란릉령(蘭陵令)을 지냈다. "
            "법가(法家)의 대표적 사상가인 한비자(韓非子)와 이사(李斯)가 그의 문하생이다. "
            "유가의 전통을 계승하면서도 성악설(性惡說)이라는 독자적 인성론을 제시하여 "
            "맹자(孟子)의 성선설과 유가 내부에서 가장 근본적인 대립을 형성했다."
        ),
        "core_philosophy": (
            "순자 사상의 핵심은 성악설(性惡說)과 화성기위(化性起僞)이다. "
            "인간의 본성(性)은 이익을 좋아하고 질투하며 욕망을 따르는 것이므로 악(惡)하다. "
            "그러나 인위적 노력(僞)인 예(禮)와 의(義)를 통해 본성을 변화시킬 수 있다. "
            "성인(聖人)이 예의(禮義)를 제정한 것은 인간의 악한 본성을 교화하기 위함이다. "
            "천론(天論)에서는 하늘(天)을 도덕적 주재자가 아닌 자연 법칙으로 보고, "
            "인간은 자연을 통제하고 이용할 수 있다(制天命而用之)고 주장했다. "
            "학문과 교육을 통한 점진적 축적(積)을 강조하며, "
            "예와 법을 병용(禮法竝用)하여 사회 질서를 확립해야 한다고 보았다."
        ),
        "philosophical_journey": (
            "초기(~기원전 280경): 조나라에서 태어나 유가의 전통을 학습했다. "
            "제나라 직하학궁에 유학하여 다양한 학파(유가·도가·묵가·명가·법가)의 사상을 접하며 "
            "폭넓은 학문적 기반을 형성했다. "
            "중기(기원전 280~250경): 직하학궁에서 세 번 제주(祭酒)를 역임하며 "
            "당대 최고의 학자로 명성을 얻었다. 이 시기에 맹자의 성선설을 비판하고 "
            "성악설을 체계화했으며, 예론(禮論)·천론(天論)·정명론(正名論) 등 "
            "핵심 사상을 정립했다. "
            "말기(기원전 250~238경): 초나라 춘신군의 초빙으로 란릉령을 지냈다. "
            "한비자(韓非子)와 이사(李斯)를 제자로 가르쳤으며, "
            "이들이 법가 사상을 발전시키는 데 결정적 영향을 미쳤다. "
            "춘신군 사후에도 란릉에 머물며 저술 활동을 하다 생을 마감했다."
        ),
        "keywords": [
            "성악설(性惡說)",
            "화성기위(化性起僞)",
            "예(禮)",
            "위(僞)",
            "천인지분(天人之分)",
            "제천명이용지(制天命而用之)",
            "적(積)",
            "대청명(大清明)",
            "허일이정(虛壹而靜)",
            "약정속성(約定俗成)"
        ]
    }
    result = client.index(index=INDEX_THINKERS, id="xunzi", document=doc)
    print(f"[thinker] xunzi: {result['result']}")
    return result


def insert_works(client):
    """순자 관련 저서 데이터 입력."""
    works = [
        {
            "id": "xunzi-xunzi",
            "thinker_id": "xunzi",
            "title": "순자",
            "title_original": "荀子 (Xunzi)",
            "year": -250,
            "significance": (
                "순자와 그 제자들이 편찬한 저서로, 총 32편으로 구성되어 있다. "
                "성악편·예론편·천론편·정명편·권학편·해폐편 등이 핵심 편목이다. "
                "선진유학의 주요 경전 중 하나로, 인성론·정치론·인식론·자연관 등 "
                "순자 사상의 전모를 담고 있다. "
                "유가의 예(禮) 사상을 체계화하고, 성악설에 기반한 교화론을 전개하며, "
                "자연주의적 천론(天論)을 제시한 점에서 선진유학의 집대성으로 평가된다."
            ),
            "key_concepts": [
                "성악설(性惡說)", "화성기위(化性起僞)", "예(禮)",
                "천론(天論)", "정명(正名)", "권학(勸學)", "해폐(解蔽)"
            ]
        },
        {
            "id": "xunzi-xingebian",
            "thinker_id": "xunzi",
            "title": "성악편",
            "title_original": "性惡篇 (Xing E Pian)",
            "year": -250,
            "significance": (
                "순자 32편 중 성악설(性惡說)의 핵심 논변이 담긴 편이다. "
                "'인간의 본성은 악하니, 그 선한 것은 인위(僞)이다"
                "(人之性惡 其善者僞也)'라는 명제를 제시하고, "
                "맹자의 성선설을 정면으로 반박한다. "
                "본성(性)과 인위(僞)의 엄격한 구분, "
                "성인(聖人)이 예의(禮義)를 제정한 이유, "
                "교화를 통한 본성의 변화 가능성을 체계적으로 논증한다."
            ),
            "key_concepts": [
                "성악설(性惡說)", "성(性)과 위(僞)", "화성기위(化性起僞)",
                "예의(禮義)", "성선설 비판"
            ]
        },
        {
            "id": "xunzi-lilun",
            "thinker_id": "xunzi",
            "title": "예론편",
            "title_original": "禮論篇 (Li Lun Pian)",
            "year": -250,
            "significance": (
                "예(禮)의 기원, 기능, 사회적 의미를 체계적으로 논한 편이다. "
                "예는 성인이 인간의 욕망을 조절하고 사회 질서를 확립하기 위해 제정한 것이며, "
                "분(分, 사회적 구별)을 통해 각자의 역할과 위치를 정하는 기능을 한다. "
                "'예란 어디서 일어나는가? 사람은 나면서부터 욕망이 있으니"
                "(禮起於何也 曰 人生而有欲)'라는 문답으로 시작하여 "
                "예의 필요성과 기원을 논증한다."
            ),
            "key_concepts": [
                "예(禮)", "분(分)", "양욕(養欲)", "사회질서",
                "상례(喪禮)", "제례(祭禮)"
            ]
        },
        {
            "id": "xunzi-tianlun",
            "thinker_id": "xunzi",
            "title": "천론편",
            "title_original": "天論篇 (Tian Lun Pian)",
            "year": -250,
            "significance": (
                "하늘(天)에 대한 순자의 자연주의적 관점을 전개한 편이다. "
                "하늘은 도덕적 주재자가 아니라 일정한 법칙(常)을 가진 자연이며, "
                "인간 사회의 치란(治亂)은 하늘이 아니라 인간의 행위에 달려 있다. "
                "'하늘의 운행에는 일정함이 있으니(天行有常)', "
                "'자연을 따르기만 하며 찬양하기보다 통제하여 이용하라"
                "(大天而思之 孰與物畜而制之)'는 명제로 "
                "동아시아 사상사에서 가장 이른 자연주의적·합리주의적 천론을 제시했다."
            ),
            "key_concepts": [
                "천행유상(天行有常)", "천인지분(天人之分)",
                "제천명이용지(制天命而用之)", "자연법칙"
            ]
        }
    ]
    for w in works:
        result = client.index(index=INDEX_WORKS, id=w["id"], document=w)
        print(f"[work] {w['id']}: {result['result']}")
    return len(works)


def insert_claims(client):
    """순자 핵심 주장 데이터 입력."""
    claims = [
        {
            "id": "xunzi-claim-001",
            "thinker_id": "xunzi",
            "work_id": "xunzi-xingebian",
            "source_detail": "순자 성악편(性惡篇)",
            "claim": (
                "성악설(性惡說): 인간의 본성(性)은 악하다. "
                "인간이 선한 것은 인위적 노력(僞)의 결과이다."
            ),
            "original_text": "人之性惡 其善者僞也",
            "original_text_ko": "사람의 본성은 악하니, 그 선한 것은 인위(僞)이다.",
            "explanation": (
                "순자 성악설의 핵심 명제이다. 인간은 태어나면서 이익을 좋아하고(好利), "
                "질투하며(疾惡), 이목의 욕망을 따르는 본성을 가지고 있다. "
                "이를 그대로 따르면 다툼과 혼란이 생긴다. "
                "선(善)은 본래의 성(性)이 아니라 후천적 인위(僞, 사람의 의식적 노력)로 이루어진다."
            ),
            "argument": (
                "순자는 성(性)을 '하늘이 부여한 자연적 성질(天之就也)'로 정의한다. "
                "배우거나 노력하지 않아도 저절로 그러한 것이 본성이다. "
                "인간은 나면서부터 이익을 좋아하니(今人之性 生而有好利焉) 이를 따르면 쟁탈이 일어나고, "
                "질투심이 있으니(生而有疾惡焉) 이를 따르면 잔해(殘賊)가 생기며, "
                "감각적 욕망이 있으니(生而有耳目之欲) 이를 따르면 음란(淫亂)이 생긴다. "
                "따라서 인간의 본성을 그대로 놓아두면 반드시 악(惡)에 이르므로 본성은 악하다."
            ),
            "counterpoint": (
                "맹자(孟子)는 성선설을 주장하며, 인간에게 선천적인 도덕적 감정(사단, 四端)이 있다고 보았다. "
                "맹자 공손추 상편에서 '측은지심이 없으면 사람이 아니다"
                "(無惻隱之心 非人也)'라 했다. "
                "순자는 이에 대해 '맹자가 성(性)과 위(僞)를 구분하지 못했다"
                "(孟子曰人之性善 是不及知人之性 而不察乎人之性僞之分者也)'고 반박했다. "
                "주희(朱熹)는 후대에 맹자의 입장을 정통으로 채택하여, "
                "순자의 성악설은 유학 정통에서 이단으로 배척되는 경향이 있었다."
            ),
            "context": (
                "전국시대 말기, 인간 본성에 대한 다양한 논의(성선·성악·성무선악)가 활발하던 시기. "
                "순자는 맹자의 성선설이 인간의 현실을 직시하지 못한다고 보고 "
                "성악설을 통해 예와 교화의 필요성을 논증하고자 했다."
            ),
            "keywords": ["성악설(性惡說)", "성(性)", "위(僞)", "인성론"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "xunzi-claim-002",
            "thinker_id": "xunzi",
            "work_id": "xunzi-xingebian",
            "source_detail": "순자 성악편(性惡篇)",
            "claim": (
                "화성기위(化性起僞): 본성(性)을 변화시켜 인위(僞)를 일으킨다. "
                "교화와 학습을 통해 악한 본성을 선하게 바꿀 수 있다."
            ),
            "original_text": "故聖人化性而起僞 僞起而生禮義 禮義生而制法度",
            "original_text_ko": (
                "그러므로 성인은 본성을 변화시켜 인위를 일으키고, "
                "인위가 일어나 예의가 생기며, 예의가 생겨 법도를 제정한다."
            ),
            "explanation": (
                "화성기위는 순자 교화론의 핵심 개념이다. "
                "성(性)은 변화시킬 수 있으며, 그 수단이 바로 인위(僞)이다. "
                "위(僞)는 '거짓'이 아니라 '사람이 의식적으로 행하는 것(人爲)'을 의미한다. "
                "성인(聖人)이 예의(禮義)를 제정하고 법도를 세운 것은 "
                "바로 악한 본성을 교화하기 위한 인위적 노력의 결과이다."
            ),
            "argument": (
                "순자는 '굽은 나무는 반드시 증교(蒸矯, 뜨거운 불로 구부림)한 뒤에야 곧아지고, "
                "무딘 쇠는 반드시 갈고 닦아야 날카로워진다(枸木必將待檃栝烝矯然後直 "
                "鈍金必將待礱厲然後利)'고 비유한다. "
                "마찬가지로 인간의 악한 본성도 스승(師)의 가르침과 예의의 교화를 거쳐야 선해진다. "
                "본성 자체가 악하기에 오히려 교화가 필수적이고 가능하다는 역설적 논리이다."
            ),
            "counterpoint": (
                "맹자는 본성이 이미 선하므로 외부의 교화보다 내면의 확충(擴充)이 중요하다고 보았다. "
                "맹자 고자 상편에서 '인의예지는 밖에서 나를 녹여 넣는 것이 아니라 "
                "내가 본래 가지고 있는 것이다(仁義禮智 非由外鑠我也 我固有之也)'라 했다. "
                "고자(告子)는 '성(性)은 선도 악도 아니다(性無善無不善)'라 주장하여 "
                "성선·성악 모두에 반대하는 제3의 입장을 제시했다."
            ),
            "context": (
                "성악설에서 핵심적인 것은 '교화 가능성'이다. "
                "순자는 본성이 악하다고 진단하되, 인위를 통해 변화시킬 수 있다고 봄으로써 "
                "교육과 예의 제도의 필요성을 논증했다. "
                "이는 법가의 형벌 중심 교화와 구별되는 유가적 교화론이다."
            ),
            "keywords": ["화성기위(化性起僞)", "위(僞)", "교화", "성(性)"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "xunzi-claim-003",
            "thinker_id": "xunzi",
            "work_id": "xunzi-lilun",
            "source_detail": "순자 예론편(禮論篇)",
            "claim": (
                "예(禮)의 기원과 기능: 예는 성인이 인간의 욕망을 조절하고 "
                "사회 질서를 확립하기 위해 제정한 것이다."
            ),
            "original_text": "禮起於何也 曰 人生而有欲 欲而不得則不能無求 求而無度量分界則不能不爭 爭則亂 亂則窮",
            "original_text_ko": (
                "예는 어디서 일어나는가? 사람은 나면서부터 욕망이 있으니, "
                "욕망이 있는데 얻지 못하면 구하지 않을 수 없고, "
                "구하는데 한도와 구분이 없으면 다투지 않을 수 없고, "
                "다투면 어지러워지고, 어지러워지면 곤궁해진다."
            ),
            "explanation": (
                "순자에게 예(禮)는 성인이 인간 사회의 혼란을 방지하기 위해 "
                "의도적으로 제정한 제도이다. "
                "인간은 욕망(欲)을 가지고 태어나므로, 욕망의 무제한적 추구는 "
                "필연적으로 쟁탈과 혼란을 초래한다. "
                "예는 이 욕망에 한도(度量)와 구분(分界)을 부여하여 질서를 확립한다. "
                "순자의 예론은 공자의 예(禮) 사상을 제도적·사회적 차원에서 체계화한 것이다."
            ),
            "argument": (
                "순자는 예의 기능을 '양(養)'과 '분(分)'으로 설명한다. "
                "'양'은 욕망을 적절히 충족시키는 것이고(養人之欲 給人之求), "
                "'분'은 사회적 등급과 구분을 세우는 것이다. "
                "예를 통해 욕망과 물자가 서로 조절되어(欲必不窮乎物 物必不屈於欲) "
                "사회가 안정된다. 선왕(先王)이 예의를 제정한 것은 바로 이 혼란을 막기 위함이다."
            ),
            "counterpoint": (
                "노자(老子)는 도덕경에서 '예(禮)란 충(忠)과 신(信)이 엷어진 것이며 "
                "혼란의 시작이다(夫禮者 忠信之薄 而亂之首)'라 하여 "
                "예를 인위적이고 퇴화의 산물로 비판했다. "
                "묵자(墨子)는 유가의 번잡한 예제(禮制)가 사치와 낭비를 조장한다고 비판하며 "
                "절용(節用)을 주장했다."
            ),
            "context": (
                "전국시대의 사회 혼란 속에서 질서 회복의 방법론으로서 예의 역할이 부각되었다. "
                "순자는 공자가 제시한 예(禮)의 이념을 "
                "사회 제도의 필요성이라는 관점에서 논증적으로 체계화했다."
            ),
            "keywords": ["예(禮)", "분(分)", "욕망", "사회질서"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "xunzi-claim-004",
            "thinker_id": "xunzi",
            "work_id": "xunzi-tianlun",
            "source_detail": "순자 천론편(天論篇)",
            "claim": (
                "천론(天論): 하늘(天)은 도덕적 주재자가 아니라 자연 법칙이다. "
                "천인분리(天人之分)를 명확히 해야 한다."
            ),
            "original_text": "天行有常 不爲堯存 不爲桀亡",
            "original_text_ko": (
                "하늘의 운행에는 일정함이 있으니, "
                "요(堯)임금 때문에 존재하는 것이 아니고 "
                "걸(桀)왕 때문에 없어지는 것도 아니다."
            ),
            "explanation": (
                "순자는 하늘을 의지를 가진 인격적 주재자로 보는 전통적 천관(天觀)을 부정하고, "
                "하늘은 일정한 법칙(常)에 따라 운행하는 자연으로 보았다. "
                "천변(天變, 이상 기후나 재해)은 하늘의 뜻이 아니라 자연 현상일 뿐이며, "
                "사회의 치란(治亂)은 하늘이 아니라 인간의 행위에 달려 있다. "
                "이것이 '천인지분(天人之分)', 즉 하늘과 인간의 역할 구분이다."
            ),
            "argument": (
                "순자는 '하늘의 운행에는 일정함이 있다(天行有常)'는 명제에서 출발한다. "
                "해·달·별의 운행, 사계절의 교체는 요순시대나 걸주시대나 동일하다. "
                "그런데 요순 때는 다스려졌고 걸주 때는 혼란했으니, "
                "이는 하늘의 차이가 아니라 인간의 차이이다. "
                "따라서 하늘을 두려워하며 그저 기도할 것이 아니라, "
                "하늘과 인간의 역할을 분명히 구분(明於天人之分)해야 한다."
            ),
            "counterpoint": (
                "동중서(董仲舒)는 한대(漢代)에 천인감응설(天人感應說)을 주장하여 "
                "하늘이 인간 사회의 선악에 응답한다고 보았다. 이는 순자의 천인분리와 정면으로 대립한다. "
                "맹자도 '하늘이 뜻을 드러낸다(天之暦數在爾躬)'는 전통적 천관을 일부 수용하여 "
                "천명(天命)의 도덕적 의미를 인정했다."
            ),
            "context": (
                "고대 중국에서는 하늘을 인격적 주재자로 보는 천관이 지배적이었다. "
                "순자는 이를 비판하며 합리주의적·자연주의적 천론을 제시했으나, "
                "한대 이후 동중서의 천인감응설이 정통이 되면서 순자의 천론은 오랫동안 주목받지 못했다."
            ),
            "keywords": ["천론(天論)", "천행유상(天行有常)", "천인지분(天人之分)"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "xunzi-claim-005",
            "thinker_id": "xunzi",
            "work_id": "xunzi-tianlun",
            "source_detail": "순자 천론편(天論篇)",
            "claim": (
                "제천이용(制天命而用之): 자연을 숭배하기보다 "
                "통제하고 이용해야 한다."
            ),
            "original_text": "大天而思之 孰與物畜而制之 從天而頌之 孰與制天命而用之",
            "original_text_ko": (
                "하늘을 위대하게 여기고 그리워하기만 하는 것이 "
                "만물을 길러 통제하는 것만 하겠는가? "
                "하늘을 따르며 찬양하기만 하는 것이 "
                "천명을 통제하여 이용하는 것만 하겠는가?"
            ),
            "explanation": (
                "'제천명이용지(制天命而用之)'는 순자 자연관의 결론적 명제이다. "
                "하늘이 자연 법칙에 불과하다면, 인간은 그것을 두려워하거나 숭배할 것이 아니라 "
                "적극적으로 이해하고 통제하여 인간의 이익을 위해 활용해야 한다. "
                "이는 동아시아 사상사에서 가장 이른 시기의 적극적 자연관이며, "
                "인간 주체성을 강조하는 합리주의적 사고이다."
            ),
            "argument": (
                "순자는 하늘의 자연 법칙성(天行有常)을 확인한 후, "
                "그로부터 인간의 실천적 태도를 도출한다. "
                "하늘에 기대어 공짜로 얻으려 하지 말고(錯人而思天 則失萬物之情), "
                "인간의 노력으로 자연을 활용해야 한다. "
                "농사, 축산, 수리(水利) 등 자연을 통제하는 실천적 지혜가 중요하며, "
                "이것이 '성인의 정치'의 일부이다."
            ),
            "counterpoint": (
                "노자(老子)는 '도법자연(道法自然)'을 주장하며 인간이 자연에 순응해야 한다고 보았다. "
                "도덕경 25장에서 '사람은 땅을 본받고, 땅은 하늘을 본받고, "
                "하늘은 도를 본받고, 도는 자연을 본받는다(人法地 地法天 天法道 道法自然)'라 했다. "
                "이는 자연을 통제하려는 순자의 입장과 정면으로 대립한다."
            ),
            "context": (
                "순자의 '제천이용' 사상은 농업 사회에서 자연환경을 관리하고 "
                "활용하는 실천적 지혜와 연결된다. "
                "근대 이후 일부 학자들은 이를 근대적 자연관의 선구로 평가하기도 한다."
            ),
            "keywords": ["제천명이용지(制天命而用之)", "자연관", "인간주체성"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "xunzi-claim-006",
            "thinker_id": "xunzi",
            "work_id": "xunzi-xunzi",
            "source_detail": "순자 왕제편(王制篇), 부국편(富國篇)",
            "claim": (
                "명분론(名分論): 분(分)을 통해 사회적 구별을 세우고, "
                "각자의 역할과 위치를 정해야 사회가 안정된다."
            ),
            "original_text": "人何以能群 曰分 分何以能行 曰義",
            "original_text_ko": (
                "사람이 어떻게 무리를 이룰 수 있는가? 분(分, 구별)이 있기 때문이다. "
                "분은 어떻게 행해질 수 있는가? 의(義)가 있기 때문이다."
            ),
            "explanation": (
                "순자는 인간이 다른 동물과 달리 사회(群)를 이룰 수 있는 것은 "
                "분(分, 사회적 역할의 구분)이 있기 때문이라고 보았다. "
                "분(分)은 예(禮)를 통해 구현되며, 의(義)가 그 실행의 근거이다. "
                "각자의 분수에 맞는 역할을 수행할 때 사회가 안정되고, "
                "분이 없으면 다툼과 혼란이 생긴다."
            ),
            "argument": (
                "인간은 개인적으로는 소보다 힘이 약하고 말보다 빠르지 않지만, "
                "소와 말을 부릴 수 있는 것은 인간이 무리를 이룰 수 있기 때문이다(能群). "
                "무리를 이루려면 분(分)이 필요하다. "
                "분이란 귀천(貴賤)·장유(長幼)·빈부(貧富)의 등급을 구분하여 "
                "각자의 역할과 자원 배분을 정하는 것이다. "
                "이 구분이 없으면 모두가 같은 것을 탐하여 다투게 된다."
            ),
            "counterpoint": (
                "묵자(墨子)는 겸애(兼愛)를 주장하며 사회적 차별 없이 모든 사람을 평등하게 "
                "사랑해야 한다고 보았다. 순자는 묵자의 겸애가 '분(分)을 없앤다(墨子蔽於用而不知文)'고 비판했다. "
                "노자도 '대도가 폐해지니 인의가 생겼다(大道廢 有仁義)'며 "
                "인위적 사회 구분 자체를 부정했다."
            ),
            "context": (
                "전국시대의 사회 혼란 속에서 질서 회복의 원리로서 분(分)의 개념이 중요했다. "
                "순자의 명분론은 후대 유가의 명분(名分)·분수(分數) 개념의 이론적 기초가 되었다."
            ),
            "keywords": ["분(分)", "명분론", "군(群)", "사회질서"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "xunzi-claim-007",
            "thinker_id": "xunzi",
            "work_id": "xunzi-xunzi",
            "source_detail": "순자 권학편(勸學篇)",
            "claim": (
                "교육론: 학문의 축적(積)이 중요하다. "
                "끊임없는 학습과 노력이 사람을 변화시킨다."
            ),
            "original_text": "積土成山 風雨興焉 積水成淵 蛟龍生焉 積善成德 而神明自得 聖心備焉",
            "original_text_ko": (
                "흙을 쌓아 산을 이루면 비바람이 일어나고, "
                "물을 모아 연못을 이루면 교룡이 생기며, "
                "선을 쌓아 덕을 이루면 신명(神明)이 저절로 갖추어지고 성인의 마음이 구비된다."
            ),
            "explanation": (
                "순자는 학문과 교육의 점진적 축적(積)을 강조한다. "
                "본성이 악하더라도 꾸준히 선을 쌓으면(積善) 덕을 이루어 성인에 이를 수 있다. "
                "권학편(勸學篇)은 순자 32편의 첫 편으로, "
                "학문의 시작과 끝, 방법과 자세를 체계적으로 논한다. "
                "'학문은 끝이 없다(學不可以已)'는 선언으로 시작한다."
            ),
            "argument": (
                "'학문은 끝이 없다(學不可以已)'가 권학편의 첫 문장이다. "
                "순자는 '천리 길도 한 걸음부터(不積跬步 無以至千里)'의 비유로 축적의 중요성을 강조한다. "
                "성인과 보통 사람의 차이는 본성의 차이가 아니라 "
                "학문 축적의 차이이다(聖人者 人之所積而致也). "
                "도중에 멈추지 않는 것(鍥而不舍)이 핵심이다."
            ),
            "counterpoint": (
                "맹자는 '사람이 배우지 않고도 할 수 있는 것이 양능(良能)이고, "
                "생각하지 않고도 아는 것이 양지(良知)이다"
                "(人之所不學而能者 其良能也 所不慮而知者 其良知也, 맹자 진심 상편)'라 하여 "
                "선천적 도덕 능력을 강조했다. 순자는 이러한 선천적 앎을 부정하고 "
                "후천적 학습의 절대적 중요성을 주장한다."
            ),
            "context": (
                "권학편은 순자 전체의 서론에 해당하며, "
                "학문을 통한 인간 변화 가능성이라는 순자 사상의 근본 전제를 제시한다."
            ),
            "keywords": ["적(積)", "권학(勸學)", "학문", "교육"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "xunzi-claim-008",
            "thinker_id": "xunzi",
            "work_id": "xunzi-xingebian",
            "source_detail": "순자 성악편(性惡篇), 권학편(勸學篇)",
            "claim": (
                "군자와 소인: 적선(積善)하면 군자가 되고, "
                "적불선(積不善)하면 소인이 된다. 군자와 소인의 차이는 본성이 아니라 축적이다."
            ),
            "original_text": "積善成德 積不善成賊 積靡不審 積微成著",
            "original_text_ko": (
                "선을 쌓으면 덕이 이루어지고, 불선을 쌓으면 해악이 이루어진다. "
                "미세한 것이 쌓이면 점차 분명해진다."
            ),
            "explanation": (
                "순자에게 군자(君子)와 소인(小人)의 구별은 타고난 것이 아니라 "
                "후천적 노력의 축적(積)에 달려 있다. "
                "꾸준히 선(善)을 쌓으면 군자가 되고, 불선(不善)을 쌓으면 소인이 된다. "
                "이는 성악설의 논리적 귀결로, 본성이 같더라도 "
                "인위적 노력의 방향과 정도에 따라 결과가 달라진다."
            ),
            "argument": (
                "'길에서 가는 사람도 우(禹, 성인)가 될 수 있다(塗之人可以爲禹)'라는 순자의 명제는 "
                "만인의 성인 가능성을 선언한다. 본성은 같으나(性同), "
                "노력 여부에 따라 군자·소인으로 나뉜다. "
                "성인(聖人)도 태어날 때는 다른 사람과 본성이 같았으나, "
                "학문과 예의를 축적하여 성인이 된 것이다."
            ),
            "counterpoint": (
                "맹자도 '사람이면 누구나 요순이 될 수 있다(人皆可以爲堯舜, 맹자 고자 하편)'라 했으나, "
                "그 근거가 다르다. 맹자는 선한 본성을 확충하면 되므로 "
                "외부 학습보다 내적 반성(反求諸己)을 강조한 반면, "
                "순자는 악한 본성을 극복해야 하므로 외부의 스승·예법·학문이 필수적이라고 보았다."
            ),
            "context": (
                "군자·소인론은 공자 이래 유가의 핵심 주제이며, "
                "순자는 이를 성악설·축적론과 결합하여 재해석했다."
            ),
            "keywords": ["적선(積善)", "군자(君子)", "소인(小人)", "적(積)"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "xunzi-claim-009",
            "thinker_id": "xunzi",
            "work_id": "xunzi-xunzi",
            "source_detail": "순자 왕제편(王制篇), 성악편(性惡篇)",
            "claim": (
                "법과 예의 관계 — 예법병용(禮法竝用): "
                "예(禮)로 교화하되, 법(法)으로 다스리는 것을 병행해야 한다."
            ),
            "original_text": "治之經 禮與刑 君子以修百姓 庶人以修一己",
            "original_text_ko": (
                "다스림의 경륜은 예와 형벌이다. "
                "군자는 이로써 백성을 다스리고, 서인은 이로써 자신을 다스린다."
            ),
            "explanation": (
                "순자는 예(禮)만으로는 모든 사람을 교화할 수 없으므로, "
                "법(法)과 형벌(刑)을 보조적으로 사용해야 한다고 보았다. "
                "예는 교화의 근본이고, 법은 보조 수단이다. "
                "이는 순자가 유가의 덕치(德治)와 법가의 법치(法治)를 종합한 것으로, "
                "그의 제자 한비자와 이사가 법가로 발전하는 이론적 기반이 되었다."
            ),
            "argument": (
                "순자는 '예의로 이끌고 형벌로 바로잡는다(隆禮義 而殺詩書)'는 원칙을 제시한다. "
                "예로 교화할 수 있는 자는 예로 다스리고, "
                "예로 교화할 수 없는 자는 법으로 제재한다. "
                "예가 없는 법은 폭력이며, 법이 없는 예는 무력하다. "
                "양자의 병용이 올바른 통치의 경륜(經)이다."
            ),
            "counterpoint": (
                "맹자는 '힘으로 인(仁)을 가장하는 것이 패(覇)이고, "
                "덕으로 인을 행하는 것이 왕(王)이다(以力假仁者霸 以德行仁者王, 맹자 공손추 상편)'라 하여 "
                "법과 형벌에 의존하는 통치를 패도(覇道)로 비판했다. "
                "한비자(韓非子)는 반대로 예는 실효성이 없으며 법과 술(術)만이 "
                "효과적 통치 수단이라고 보아 순자보다 더 극단적인 법치론으로 나아갔다."
            ),
            "context": (
                "순자의 예법병용론은 유가와 법가의 접점에 위치한다. "
                "그의 제자인 한비자와 이사가 법가 사상을 발전시킨 것은 "
                "순자의 이러한 현실주의적 통치론과 무관하지 않다."
            ),
            "keywords": ["예법병용(禮法竝用)", "법(法)", "형벌", "통치론"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "xunzi-claim-010",
            "thinker_id": "xunzi",
            "work_id": "xunzi-xunzi",
            "source_detail": "순자 해폐편(解蔽篇)",
            "claim": (
                "심론(心論): 마음의 대청명(大清明) 상태를 "
                "허일이정(虛壹而靜)을 통해 달성해야 한다."
            ),
            "original_text": "人何以知道 曰心 心何以知 曰虛壹而靜",
            "original_text_ko": (
                "사람이 어떻게 도(道)를 아는가? 마음(心)으로 안다. "
                "마음이 어떻게 아는가? 비우고(虛) 하나로 모으고(壹) 고요히 함(靜)으로써 안다."
            ),
            "explanation": (
                "순자는 마음(心)이 도(道)를 인식하는 기관이라고 보았다. "
                "그런데 마음은 편벽(蔽)에 가려지기 쉬우므로, "
                "허(虛, 기존 지식에 얽매이지 않음)·"
                "일(壹, 하나에 집중하여 흩어지지 않음)·"
                "정(靜, 감정에 흔들리지 않고 고요함)의 수양을 통해 "
                "대청명(大清明, 크게 맑고 밝은 인식 상태)에 도달해야 한다."
            ),
            "argument": (
                "해폐편(解蔽篇)에서 순자는 다양한 사상가들이 도의 일부분만 보고 "
                "전체를 안다고 착각하는 '폐(蔽, 가려짐)'의 문제를 분석한다. "
                "묵자는 용(用)에 가려져 문(文)을 모르고, "
                "장자는 천(天)에 가려져 인(人)을 모른다. "
                "이 편벽을 극복하려면 허일이정(虛壹而靜)의 수양이 필요하다. "
                "마음이 대청명(大清明)에 이르면 만물의 이치를 편벽 없이 인식할 수 있다."
            ),
            "counterpoint": (
                "맹자는 마음 자체에 이미 도덕적 능력(양지양능)이 내재해 있으므로 "
                "마음을 보존(存心)하고 키우는 것(養心)이 핵심이라고 보았다. "
                "맹자 진심 상편에서 '그 마음을 다하면 그 본성을 안다(盡其心者 知其性也)'라 했다. "
                "장자(莊子)는 심재(心齋)와 좌망(坐忘)을 통해 마음을 비우는 것을 강조했으나, "
                "이는 도(道)에 대한 직관적 합일을 목적으로 하여 순자의 인식론적 접근과 다르다."
            ),
            "context": (
                "순자의 심론은 인식론적 관점에서 마음의 기능과 수양 방법을 논한 것으로, "
                "맹자의 도덕적 심론과는 접근 방식이 다르다. "
                "허일이정은 후대 주자학의 거경(居敬) 수양론에도 영향을 미쳤다."
            ),
            "keywords": ["심론", "대청명(大清明)", "허일이정(虛壹而靜)", "해폐(解蔽)"],
            "verified": False,
            "verification_log": []
        },
        {
            "id": "xunzi-claim-011",
            "thinker_id": "xunzi",
            "work_id": "xunzi-xunzi",
            "source_detail": "순자 정명편(正名篇)",
            "claim": (
                "정명론(正名論): 이름(名)을 바로잡아야 한다. "
                "명칭은 약정속성(約定俗成), 즉 사회적 약속에 의해 성립한다."
            ),
            "original_text": "名無固宜 約之以命 約定俗成謂之宜 異於約則謂之不宜",
            "original_text_ko": (
                "이름에는 본래 정해진 적합함이 없으니, "
                "약속하여 이름 붙이고, 약속이 정해지고 관습이 이루어지면 적합하다 하고, "
                "약속과 다르면 적합하지 않다고 한다."
            ),
            "explanation": (
                "순자의 정명론은 언어와 명칭에 대한 이론이다. "
                "이름(名)은 실재(實)에 본래부터 대응하는 것이 아니라, "
                "사회적 약속(約)과 관습(俗)에 의해 성립한다(約定俗成). "
                "이름이 바로잡히면 사물의 구분이 명확해지고, "
                "이름이 혼란하면 사회적 소통과 질서가 무너진다. "
                "이는 공자의 정명(正名) 사상을 언어철학적으로 심화한 것이다."
            ),
            "argument": (
                "순자는 이름의 세 가지 유형을 제시한다: "
                "형명(刑名, 형태에 따른 이름), 소명(所名, 실재를 가리키는 이름), "
                "산명(散名, 개별적 이름)과 공명(共名, 보편적 이름). "
                "올바른 이름 사용은 '같은 것은 같다 하고 다른 것은 다르다 하는 것(同則同之 異則異之)'이다. "
                "궤변가(詭辯家)들이 이름을 혼란시키면 시비(是非)가 불분명해지고 "
                "형벌과 법이 제대로 시행되지 않는다(刑名不正 則賞罰不當)."
            ),
            "counterpoint": (
                "공손룡(公孫龍)은 '백마는 말이 아니다(白馬非馬)'라는 논변으로 "
                "이름과 실재의 관계를 역설적으로 탐구했다. "
                "순자는 이러한 명가(名家)의 논변을 '이름으로 이름을 어지럽히는 것(以名亂名)'이라 비판했다. "
                "장자는 '이름은 실재의 그릇(名者 實之賓也, 장자 소요유편)'이라 하여 "
                "이름에 대한 집착 자체를 넘어서야 한다고 보았다."
            ),
            "context": (
                "전국시대에는 명가(名家)의 궤변, 묵가의 논리학, 유가의 정명 등 "
                "언어와 이름에 대한 논의가 활발했다. "
                "순자의 정명론은 이러한 다양한 논의를 종합적으로 정리한 것이다."
            ),
            "keywords": ["정명론(正名論)", "약정속성(約定俗成)", "명(名)", "실(實)"],
            "verified": False,
            "verification_log": []
        }
    ]
    for c in claims:
        result = client.index(index=INDEX_CLAIMS, id=c["id"], document=c)
        print(f"[claim] {c['id']}: {result['result']}")
    return len(claims)


def insert_keywords(client):
    """순자 관련 키워드 데이터 입력."""
    keywords = [
        {
            "id": "kw-xunzi-xingeshuo",
            "term": "성악설(性惡說)",
            "term_en": "Theory of Evil Nature",
            "definition": (
                "순자의 인성론. 인간의 본성(性)은 이익을 좋아하고 질투하며 욕망을 따르는 것이므로 "
                "악(惡)하다. 선(善)은 후천적 인위(僞)의 결과이다. "
                "맹자의 성선설(性善說)과 유가 내부에서 가장 근본적인 대립을 형성한다."
            ),
            "thinker_id": "xunzi",
            "work_id": "xunzi-xingebian",
            "related_terms": ["화성기위(化性起僞)", "위(僞)", "성선설(性善說)"]
        },
        {
            "id": "kw-xunzi-huaxingqiwei",
            "term": "화성기위(化性起僞)",
            "term_en": "Transforming Nature and Establishing the Artificial",
            "definition": (
                "본성(性)을 변화시켜 인위(僞)를 일으킨다는 순자의 교화론의 핵심 개념. "
                "위(僞)는 '거짓'이 아니라 '사람이 의식적으로 행하는 것(人爲)'을 의미한다. "
                "성인이 예의를 제정한 것이 화성기위의 대표적 사례이다."
            ),
            "thinker_id": "xunzi",
            "work_id": "xunzi-xingebian",
            "related_terms": ["성악설(性惡說)", "예(禮)", "위(僞)"]
        },
        {
            "id": "kw-xunzi-li",
            "term": "예(禮)",
            "term_en": "Ritual Propriety (Li)",
            "definition": (
                "순자에게 예(禮)는 성인이 인간의 욕망을 조절하고 사회 질서를 확립하기 위해 "
                "제정한 사회적 제도·규범의 총체이다. "
                "욕망에 한도(度量)와 구분(分界)을 부여하여 쟁탈을 방지하는 기능을 한다. "
                "공자의 예 사상을 제도적·사회적 차원에서 체계화한 것이다."
            ),
            "thinker_id": "xunzi",
            "work_id": "xunzi-lilun",
            "related_terms": ["분(分)", "화성기위(化性起僞)", "예법병용(禮法竝用)"]
        },
        {
            "id": "kw-xunzi-wei",
            "term": "위(僞)",
            "term_en": "Artifice / Conscious Activity (Wei)",
            "definition": (
                "순자 철학의 핵심 개념으로, '사람의 의식적·의도적 행위(人爲)'를 뜻한다. "
                "'거짓'이라는 일상적 의미와 구분해야 한다. "
                "본성(性)이 자연적·선천적인 것이라면, 위(僞)는 인위적·후천적인 것이다. "
                "예의(禮義)·학문·교화 등이 모두 위(僞)에 해당한다."
            ),
            "thinker_id": "xunzi",
            "work_id": "xunzi-xingebian",
            "related_terms": ["성(性)", "화성기위(化性起僞)", "예(禮)"]
        },
        {
            "id": "kw-xunzi-tianrenzhifen",
            "term": "천인지분(天人之分)",
            "term_en": "Separation of Heaven and Humanity",
            "definition": (
                "하늘(天)과 인간(人)의 역할을 분명히 구분해야 한다는 순자의 천론(天論) 핵심 개념. "
                "하늘은 자연 법칙에 따라 운행하며, 인간 사회의 치란(治亂)은 "
                "하늘이 아니라 인간의 행위에 달려 있다. "
                "천인합일(天人合一)을 지향하는 전통적 유가 천관과 구별된다."
            ),
            "thinker_id": "xunzi",
            "work_id": "xunzi-tianlun",
            "related_terms": ["천행유상(天行有常)", "제천명이용지(制天命而用之)"]
        },
        {
            "id": "kw-xunzi-zhitianming",
            "term": "제천명이용지(制天命而用之)",
            "term_en": "Control the Mandate of Heaven and Utilize It",
            "definition": (
                "자연(天命)을 숭배하거나 두려워하지 말고, "
                "통제하고 이용해야 한다는 순자의 적극적 자연관. "
                "동아시아 사상사에서 가장 이른 시기의 인간 주체성 강조이며, "
                "도가의 자연 순응론(道法自然)과 대립한다."
            ),
            "thinker_id": "xunzi",
            "work_id": "xunzi-tianlun",
            "related_terms": ["천인지분(天人之分)", "천행유상(天行有常)"]
        },
        {
            "id": "kw-xunzi-ji",
            "term": "적(積)",
            "term_en": "Accumulation (Ji)",
            "definition": (
                "순자 교육론의 핵심 개념. 학문과 선행의 점진적 축적을 통해 "
                "인간을 변화시킬 수 있다는 사상이다. "
                "'적토성산(積土成山, 흙을 쌓아 산을 이룸)', "
                "'적선성덕(積善成德, 선을 쌓아 덕을 이룸)' 등의 비유로 표현된다. "
                "성인과 범인의 차이는 본성이 아니라 축적의 차이이다."
            ),
            "thinker_id": "xunzi",
            "work_id": "xunzi-xunzi",
            "related_terms": ["화성기위(化性起僞)", "권학(勸學)", "적선(積善)"]
        },
        {
            "id": "kw-xunzi-daqingming",
            "term": "대청명(大清明)",
            "term_en": "Great Clarity and Brightness",
            "definition": (
                "마음(心)이 편벽(蔽)을 벗어나 크게 맑고 밝은 인식 상태에 도달한 것. "
                "허일이정(虛壹而靜)의 수양을 통해 달성되며, "
                "만물의 이치를 편벽 없이 인식할 수 있는 최고의 인식 경지이다."
            ),
            "thinker_id": "xunzi",
            "work_id": "xunzi-xunzi",
            "related_terms": ["허일이정(虛壹而靜)", "해폐(解蔽)", "심(心)"]
        },
        {
            "id": "kw-xunzi-xuyijing",
            "term": "허일이정(虛壹而靜)",
            "term_en": "Empty, Unified, and Still",
            "definition": (
                "순자의 인식론적 수양론. "
                "허(虛)는 기존 지식에 얽매이지 않는 것, "
                "일(壹)은 하나에 집중하여 흩어지지 않는 것, "
                "정(靜)은 감정에 흔들리지 않고 고요한 것이다. "
                "이 세 조건을 충족하면 마음이 대청명(大清明)에 이르러 도(道)를 인식할 수 있다."
            ),
            "thinker_id": "xunzi",
            "work_id": "xunzi-xunzi",
            "related_terms": ["대청명(大清明)", "해폐(解蔽)", "심(心)"]
        },
        {
            "id": "kw-xunzi-yuedingsucheng",
            "term": "약정속성(約定俗成)",
            "term_en": "Established by Convention",
            "definition": (
                "이름(名)은 사물에 본래부터 대응하는 것이 아니라, "
                "사회적 약속(約)과 관습(俗)에 의해 성립한다는 순자의 언어 이론. "
                "순자 정명편(正名篇)의 핵심 개념으로, "
                "현대 언어학의 '기호의 자의성(arbitrariness of sign)' 개념과 유사하다."
            ),
            "thinker_id": "xunzi",
            "work_id": "xunzi-xunzi",
            "related_terms": ["정명론(正名論)", "명(名)", "실(實)"]
        }
    ]
    for kw in keywords:
        result = client.index(index=INDEX_KEYWORDS, id=kw["id"], document=kw)
        print(f"[keyword] {kw['id']}: {result['result']}")
    return len(keywords)


def insert_relations(client):
    """순자 관련 사상적 관계 데이터 입력."""
    # 먼저 기존 relation 확인
    existing_ids = set()
    try:
        res = client.search(
            index=INDEX_RELATIONS,
            query={"bool": {"should": [
                {"term": {"from_thinker": "xunzi"}},
                {"term": {"to_thinker": "xunzi"}}
            ]}},
            _source=["id"],
            size=50
        )
        for hit in res['hits']['hits']:
            existing_ids.add(hit['_id'])
        print(f"[relations] 기존 xunzi 관련 relation: {existing_ids}")
    except Exception as e:
        print(f"[relations] 기존 relation 확인 실패: {e}")

    relations = [
        {
            "id": "relation-confucius-xunzi",
            "from_thinker": "confucius",
            "to_thinker": "xunzi",
            "type": "influenced",
            "description": (
                "순자는 공자의 예(禮) 사상을 계승하면서도, "
                "인간 본성에 대해 성악설(性惡說)이라는 독자적 입장을 제시했다. "
                "공자의 인(仁)을 수용하되 인간의 자연적 본성은 악하므로 "
                "예와 교화(化性起僞)를 통해 선하게 만들어야 한다고 주장했다."
            ),
            "evidence": "순자 전편에서 공자를 최고의 성인으로 언급"
        },
        {
            "id": "relation-mencius-xunzi-debate",
            "from_thinker": "mencius",
            "to_thinker": "xunzi",
            "type": "criticized",
            "description": (
                "순자는 맹자의 성선설을 정면으로 비판하며 성악설을 주장했다. "
                "맹자와 순자의 성선/성악 대립은 유가 내부의 가장 근본적인 인성론 논쟁이다."
            ),
            "evidence": "순자 성악편(性惡篇)"
        },
        {
            "id": "relation-xunzi-hanfeizi",
            "from_thinker": "xunzi",
            "to_thinker": "hanfeizi",
            "type": "influenced",
            "description": (
                "한비자(韓非子)는 순자의 제자로, 순자의 성악설과 예법병용론에서 출발하여 "
                "법가(法家) 사상을 체계화했다. 순자가 예(禮)를 근본으로 하되 법을 보조적으로 사용한 반면, "
                "한비자는 법(法)·술(術)·세(勢)를 중심으로 하는 극단적 법치주의로 나아갔다. "
                "인간 본성에 대한 비관적 시각은 순자로부터 계승한 것이다."
            ),
            "evidence": "사기(史記) 노자한비열전(老子韓非列傳)"
        },
        {
            "id": "relation-xunzi-lisi",
            "from_thinker": "xunzi",
            "to_thinker": "lisi",
            "type": "influenced",
            "description": (
                "이사(李斯)는 순자의 제자로, 진(秦)나라에서 승상(丞相)이 되어 "
                "법가적 통치를 실행했다. 순자에게서 학문을 배운 후 "
                "'제왕의 공업을 이루겠다'며 진나라로 갔으며, "
                "진시황의 천하통일과 법치주의 정책에 핵심적 역할을 했다. "
                "분서갱유(焚書坑儒)를 건의한 것으로도 알려져 있다."
            ),
            "evidence": "사기(史記) 이사열전(李斯列傳)"
        },
        {
            "id": "relation-xunzi-dongzhongshu",
            "from_thinker": "xunzi",
            "to_thinker": "dongzhongshu",
            "type": "influenced",
            "description": (
                "동중서(董仲舒)는 한대(漢代) 유학의 대표적 사상가로, "
                "순자의 예(禮) 중심 사상과 교화론의 영향을 받았다. "
                "그러나 천론(天論)에서는 순자의 천인분리(天人之分)와 정반대인 "
                "천인감응설(天人感應說)을 주장하여 대조를 이룬다."
            ),
            "evidence": "춘추번로(春秋繁露)"
        }
    ]

    inserted = 0
    for rel in relations:
        if rel["id"] in existing_ids:
            print(f"[relation] {rel['id']}: already exists (skip)")
            continue
        result = client.index(index=INDEX_RELATIONS, id=rel["id"], document=rel)
        print(f"[relation] {rel['id']}: {result['result']}")
        inserted += 1
    return inserted


def verify_data(client):
    """입력된 순자 데이터 전수 확인."""
    print("\n=== 데이터 검증 ===")

    # refresh
    client.indices.refresh(index=INDEX_THINKERS)
    client.indices.refresh(index=INDEX_WORKS)
    client.indices.refresh(index=INDEX_CLAIMS)
    client.indices.refresh(index=INDEX_KEYWORDS)
    client.indices.refresh(index=INDEX_RELATIONS)

    # thinker 확인
    try:
        thinker = client.get(index=INDEX_THINKERS, id="xunzi")
        print(f"[thinker] xunzi: {thinker['_source']['name']} ({thinker['_source']['name_en']})")
    except Exception as e:
        print(f"[thinker] xunzi: NOT FOUND - {e}")

    # works 확인
    works_count = client.count(index=INDEX_WORKS, query={"term": {"thinker_id": "xunzi"}})
    print(f"[works] xunzi 저서 수: {works_count['count']}")

    # claims 확인
    claims_count = client.count(index=INDEX_CLAIMS, query={"term": {"thinker_id": "xunzi"}})
    print(f"[claims] xunzi 주장 수: {claims_count['count']}")

    # 필수 필드 확인
    claims_result = client.search(
        index=INDEX_CLAIMS,
        query={"term": {"thinker_id": "xunzi"}},
        _source=["id", "argument", "counterpoint", "original_text", "original_text_ko"],
        size=20
    )
    missing_fields = []
    for hit in claims_result['hits']['hits']:
        s = hit['_source']
        for field in ["argument", "counterpoint", "original_text", "original_text_ko"]:
            if not s.get(field):
                missing_fields.append(f"{s['id']}.{field}")

    if missing_fields:
        print(f"[경고] 필수 필드 누락: {missing_fields}")
    else:
        print("[OK] 모든 claim에 argument+counterpoint+original_text+original_text_ko 존재")

    # keywords 확인
    kw_count = client.count(index=INDEX_KEYWORDS, query={"term": {"thinker_id": "xunzi"}})
    print(f"[keywords] xunzi 키워드 수: {kw_count['count']}")

    # relations 확인
    rel_count = client.count(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "xunzi"}},
            {"term": {"to_thinker": "xunzi"}}
        ]}}
    )
    print(f"[relations] xunzi 관련 관계 수: {rel_count['count']}")
    rel_result = client.search(
        index=INDEX_RELATIONS,
        query={"bool": {"should": [
            {"term": {"from_thinker": "xunzi"}},
            {"term": {"to_thinker": "xunzi"}}
        ]}},
        _source=["id", "from_thinker", "to_thinker", "type"],
        size=20
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
        print("=== 순자(荀子, Xunzi) 데이터 입력 시작 ===\n")

        print("0. 동양윤리 분야 확인/추가")
        ensure_eastern_ethics_field(client)

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
