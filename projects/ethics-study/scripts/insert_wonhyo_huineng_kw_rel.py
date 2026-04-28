#!/usr/bin/env python3
"""Insert Wonhyo and Huineng keywords and relations into Elasticsearch."""

from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

# ============================================================
# WONHYO KEYWORDS
# ============================================================
wonhyo_keywords = [
    {
        "id": "wonhyo-kw-hwajae",
        "term": "화쟁",
        "term_en": "Hwajae (Harmonizing Disputes, 和諍)",
        "definition": "원효(元曉)의 핵심 사상. 불교 각 종파의 교리적 대립을 일심(一心)을 공통 근거로 삼아 조화·통합하는 방법론. '다툼을 화해시킨다'는 뜻으로, 공(空)·유(有), 대승·소승 등 대립하는 교설들이 모두 일심의 다양한 표현임을 밝혀 회통(會通)한다.",
        "thinker_id": "wonhyo",
        "work_id": "wonhyo-geumgangsaemaerongnon",
        "related_terms": ["일심", "회통", "방편", "교리 통합"],
    },
    {
        "id": "wonhyo-kw-ilsim",
        "term": "일심",
        "term_en": "Ilsim (One Mind, 一心)",
        "definition": "원효가 대승기신론소(大乘起信論疏)에서 전개한 핵심 개념. 모든 세간법과 출세간법을 포섭하는 근본 바탕. 진여문(眞如門, 변하지 않는 참된 모습)과 생멸문(生滅門, 인연에 따라 변하는 현상)이라는 두 측면을 포함하는 하나의 마음. 중생과 부처가 모두 이 일심을 공유한다.",
        "thinker_id": "wonhyo",
        "work_id": "wonhyo-daesunggisinnonso",
        "related_terms": ["화쟁", "진여문", "생멸문", "본각", "회통"],
    },
    {
        "id": "wonhyo-kw-muae",
        "term": "무애",
        "term_en": "Muae (No Hindrance, 無礙)",
        "definition": "원효가 실천한 수행·교화 원리. '어떠한 것에도 걸림이 없다'는 뜻. 형식적 계율이나 승려의 격식에 얽매이지 않고 민중 속에 들어가 노래·춤·대화로 불법을 전하는 실천 방식. 일심에 통달한 자가 자연스럽게 드러내는 자유로운 교화 행위.",
        "thinker_id": "wonhyo",
        "work_id": "wonhyo-geumgangsaemaerongnon",
        "related_terms": ["무애행", "중생교화", "일심", "소성거사"],
    },
]

# ============================================================
# HUINENG KEYWORDS
# ============================================================
huineng_keywords = [
    {
        "id": "huineng-kw-dono",
        "term": "돈오",
        "term_en": "Dono (Sudden Enlightenment, 頓悟)",
        "definition": "혜능(慧能)이 확립한 남종선(南宗禪)의 핵심 개념. 점진적 수행(漸修) 없이 단번에 자기 본성(自性)을 깨닫는 것. '본래 한 물건도 없거늘 어디에 먼지가 앉으리오(本來無一物，何處惹塵埃)'라는 혜능의 게송이 돈오의 의미를 상징적으로 표현한다. 신수(神秀)의 점오(漸悟)와 대비된다.",
        "thinker_id": "huineng",
        "work_id": "huineng-platform-sutra",
        "related_terms": ["견성성불", "자성청정", "남종선", "점수"],
    },
    {
        "id": "huineng-kw-gyeonseong-seongbul",
        "term": "견성성불",
        "term_en": "Gyeonseong Seongbul (Seeing One's Nature and Becoming Buddha, 見性成佛)",
        "definition": "자기의 본성(自性)을 직접 봄(見性)으로써 곧 부처가 되는 것(成佛). 혜능 선종의 핵심 명제. 부처는 외부에서 구하는 것이 아니라 자성(自性) 안에 이미 완전하게 갖추어져 있으므로, 자성을 직접 깨달으면 즉각 성불이 이루어진다.",
        "thinker_id": "huineng",
        "work_id": "huineng-platform-sutra",
        "related_terms": ["돈오", "자성", "자성구족", "직지인심"],
    },
    {
        "id": "huineng-kw-munyeom",
        "term": "무념",
        "term_en": "Munyeom (No-Thought, 無念)",
        "definition": "혜능이 제시한 선(禪) 수행의 세 가지 원리 중 하나. '경계(境界)에 마음이 물들지 않는 것'이 무념이다. 생각 자체를 없애는 것이 아니라, 생각이 일어날 때 그것에 집착하거나 물들지 않는 마음의 상태. 무주(無住, 어떤 경계에도 머물지 않음), 무상(無相, 외형에 집착하지 않음)과 함께 남종선의 수행 원리를 이룬다.",
        "thinker_id": "huineng",
        "work_id": "huineng-platform-sutra",
        "related_terms": ["무주", "무상", "자성청정", "돈오"],
    },
]

# ============================================================
# RELATIONS
# ============================================================
relations = [
    {
        "id": "huineng-rel-001",
        "from_thinker": "buddha",
        "to_thinker": "huineng",
        "type": "influenced",
        "description": "혜능(慧能, 638~713)은 붓다의 가르침, 특히 금강경(金剛經)과 반야(般若) 사상에 깊이 영향을 받았다. 혜능이 깨달음을 얻은 계기는 금강경 구절을 들은 것이었으며, 육조단경에는 붓다의 가르침에 대한 독창적 재해석이 담겨 있다. 돈오(頓悟)·무념(無念)은 붓다의 직관적 깨달음 전통을 계승·발전시킨 것이다.",
        "evidence": "혜능, 육조단경 행유품(行由品): '응무소주 이생기심(應無所住 而生其心)' 금강경 구절 청문 후 깨달음",
    },
    {
        "id": "wonhyo-rel-001",
        "from_thinker": "wonhyo",
        "to_thinker": "uisang",
        "type": "influenced",
        "description": "원효(元曉, 617~686)와 의상(義湘, 625~702)은 함께 당나라 유학을 시도한 동행이었다. 의상은 유학을 완수하여 화엄종(華嚴宗)을 전래하였고, 원효는 귀국 후 독자적 사상(화쟁·일심)을 전개하였다. 두 사람은 신라 불교의 가장 중요한 사상가로서 서로 영향을 주고받았으며, 한국 화엄 사상 형성에 원효의 대승기신론소가 중요한 역할을 하였다.",
        "evidence": "삼국유사 권4, 원효전·의상전; 원효 대승기신론소와 의상 화엄일승법계도의 사상적 연관",
    },
    {
        "id": "huineng-rel-002",
        "from_thinker": "huineng",
        "to_thinker": "wonhyo",
        "type": "influenced",
        "description": "혜능(638~713)과 원효(617~686)는 동시대 인물로, 직접적 교류의 역사적 기록은 없다. 그러나 양자 모두 직관적 깨달음·일심(一心)·무애(無礙)·자성(自性)을 강조하는 점에서 동아시아 불교의 같은 지적 흐름을 공유한다. 남종선의 돈오 전통이 이후 한국 불교(지눌 등)를 통해 원효 사상과 교차 연구된다.",
        "evidence": "비교 불교 연구: 가마타 시게오(鎌田茂雄), 한국불교사 — 원효와 선종 사상 비교",
    },
]

# Insert wonhyo keywords
print("=== Inserting Wonhyo keywords ===")
for kw in wonhyo_keywords:
    resp = es.index(index="ethics-keywords", id=kw["id"], document=kw)
    print(f"  {kw['id']}: {resp['result']}")

# Insert huineng keywords
print("\n=== Inserting Huineng keywords ===")
for kw in huineng_keywords:
    resp = es.index(index="ethics-keywords", id=kw["id"], document=kw)
    print(f"  {kw['id']}: {resp['result']}")

# Insert relations
print("\n=== Inserting relations ===")
for rel in relations:
    resp = es.index(index="ethics-relations", id=rel["id"], document=rel)
    print(f"  {rel['id']} ({rel['from_thinker']} → {rel['to_thinker']}): {resp['result']}")

print("\nAll done.")
