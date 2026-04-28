# Tester Report — TASK-102

## 상태: DONE

## 태스크
- **Task ID**: TASK-102
- **Title**: 로크 데이터 검증

## 검증 요약

| 카테고리 | 건수 | 정확 | 수정필요 | 심각 |
|----------|------|------|----------|------|
| thinker | 1 | 1 | 0 | 0 |
| works | 5 | 5 | 0 | 0 |
| claims | 12 | 11 | 1 | 0 |
| keywords | 10 | 10 | 0 | 0 |
| relations | 5 | 4 | 1 | 0 |
| **합계** | **33** | **31** | **2** | **0** |

---

## 1. Thinker 검증

### locke — 정확

- **생몰년**: 1632~1704 — 정확. 로크는 1632년 8월 29일 서머셋 링턴(Wrington) 출생, 1704년 10월 28일 에식스 오츠(Oates)에서 사망.
- **국적/배경**: 영국, 청교도 변호사의 아들 — 정확. 아버지 John Locke Sr.는 청교도 성향의 변호사이자 서머셋 지역의 서기관(clerk)으로 의회파(Parliamentarian) 기병대에 복무한 바 있다.
- **웨스트민스터 학교, 옥스퍼드 크라이스트처치**: 정확. 1647년 웨스트민스터 학교 입학, 1652년 크라이스트처치 입학.
- **로버트 보일(Robert Boyle) 영향**: 정확. 1660년대 보일의 실험적 자연철학에 영향을 받아 경험주의적 방법론에 공감.
- **새프츠베리 백작(Earl of Shaftesbury) 자문, 1667년부터**: 정확. 1666년 앤서니 애슐리 쿠퍼(Anthony Ashley Cooper, 이후 초대 새프츠베리 백작)를 만나 1667년부터 그의 가문에 합류.
- **1683년 네덜란드 망명, 약 6년간**: 정확. 새프츠베리 실각 후 1683년 네덜란드로 떠남, 1689년 귀국.
- **1688년 명예혁명(Glorious Revolution) 이후 귀국**: 정확. 메리 공주의 함대와 함께 1689년 2월 귀국.
- **core_philosophy**: 자연법 기초 자유주의, 자연권(생명·자유·재산), 동의, 신탁, 저항권, 타불라 라사, 소유권 노동이론 — 모두 정확한 핵심 요약.
- **philosophical_journey**: 초기/중기/망명기/후기 구분 적절. 교육론(1693), 기독교의 합리성(1695) 연도 정확. 오츠(Oates)의 매셤(Masham) 가문에서 말년 — 정확(Damaris Cudworth Masham).

**판정: 정확**

---

## 2. Works 검증

### locke-two-treatises — 정확
- **원제**: Two Treatises of Government — 정확.
- **연도**: 1689 — 정확 (출판 연도 기준; 실제 집필은 1679~1681경, Peter Laslett의 연구에 의해 확인됨). significance에서도 이 점을 정확히 언급.
- **제1론(필머 반박) / 제2론(긍정적 정치론)**: 정확한 구조 설명.
- **미국 독립선언서(1776), 프랑스 인권선언(1789) 영향**: 정확.

### locke-second-treatise — 정확
- **원제**: Second Treatise of Civil Government — 정확 (더 정확한 전체 제목은 "An Essay Concerning the True Original, Extent, and End of Civil Government"이나, "Second Treatise of Civil Government"는 관용적으로 널리 사용되는 약칭으로 문제 없음).
- **19개 장 구성**: 정확. 언급된 장별 주제(자연 상태 2장, 전쟁 상태 3장, 소유권 5장, 정치 사회의 시작 8장 등) 모두 정확.
- **locke-two-treatises와의 관계**: 별도 work로 등록한 것은 인용 편의상 적절. 대부분의 claim이 Second Treatise를 참조하므로 실용적 판단.

### locke-essay — 정확
- **원제**: An Essay Concerning Human Understanding — 정확.
- **연도**: 1689 — 정확 (정확히는 1689년 12월 출판, 표지에는 1690으로 기재되기도 함. 학술적으로 1689/1690 모두 사용됨).
- **4권 구성**: 제1권(본유관념 비판), 제2권(관념의 기원), 제3권(언어), 제4권(지식) — 정확.
- **인격적 동일성(personal identity)**: key_concepts에 포함 — 정확 (Book II, Chapter 27).

### locke-toleration — 정확
- **원제**: A Letter Concerning Toleration — 정확.
- **연도**: 1689 — 정확 (라틴어판 1689년, Epistola de Tolerantia).
- **필립 반 림보르흐(Philip van Limborch)에게 보낸 서한 형식**: 정확.
- **무신론자·교황 충성자 관용 배제**: 정확.

### locke-education — 정확
- **원제**: Some Thoughts Concerning Education — 정확.
- **연도**: 1693 — 정확.
- **에드워드 클라크(Edward Clarke)에게 보낸 서한**: 정확. Clarke의 아들 교육에 관해 보낸 편지들을 정리한 것.
- **루소의 에밀(1762)에 직접적 영향**: 정확.
- **'10분의 9는 교육에 의해...' 인용**: 정확 (Some Thoughts, §1의 유명한 구절).

**판정: 5건 모두 정확**

---

## 3. Claims 검증

### locke-claim-001 (자연 상태) — 정확
- **source_detail**: Second Treatise, Chapter 2, §4-15 — 정확.
- **original_text**: §4의 정확한 인용. "a state of perfect freedom to order their actions, and dispose of their possessions and persons, as they think fit, within the bounds of the law of nature" — Second Treatise §4 원문과 일치.
- **original_text_ko**: 영문과 대조하여 정확한 번역.
- **홉스 대비 설명**: 홉스의 자연 상태(만인 투쟁) vs 로크의 자연 상태(자연법 지배) 구별 — 정치철학의 기본적 구분으로 정확.
- **counterpoint**: 홉스 리바이어던 제13장, 흄 인성론 제3권 — 출처 정확.

### locke-claim-002 (자연권) — 정확
- **source_detail**: §6, §123 — 정확.
- **original_text**: §6의 정확한 인용. "no one ought to harm another in his life, health, liberty, or possessions."
- **생명, 자유, 재산 — 넓은 의미의 'property'**: 정확. §123에서 로크는 "Lives, Liberties and Estates, which I call by the general Name, Property"라고 명시.
- **counterpoint**: 벤담 'nonsense upon stilts' — 정확 (Anarchical Fallacies, 1796). 버크 프랑스 혁명 성찰 1790 — 정확.

### locke-claim-003 (사회계약) — 정확
- **source_detail**: §95-99, §123-131 — 정확.
- **original_text**: §95의 정확한 인용.
- **홉스와의 차이(양도 범위, 정부 지위)**: 정확한 비교.
- **counterpoint**: 흄 'Of the Original Contract' 1748 — 정확.

### locke-claim-004 (저항권) — 정확
- **source_detail**: Chapter 19, §220-243 — 정확 (Chapter 19는 §211-243).
- **original_text**: §222의 정확한 인용. "Whensoever therefore the legislative shall transgress this fundamental rule of society..."
- **original_text_ko**: "스스로 쥐거나" — 원문 "endeavour to grasp themselves"의 번역으로 적절. 다만 "스스로"가 아닌 "스스로"가 맞춤법상 올바른 표기이나, 실제로 "스스로"로 되어 있어 정확.
- **devolution of power 개념**: 정확.
- **counterpoint**: 홉스 제18장, 버크 — 정확.

### locke-claim-005 (권력 분립) — 정확
- **source_detail**: Chapters 11-14, §134-168 — 정확.
- **original_text**: §149의 발췌. 생략 부호(...)로 표시하여 명확.
- **입법권·집행권·동맹권(federative power) 삼분**: 정확. 로크는 사법권을 별도로 분리하지 않았다는 설명도 정확.
- **대권(prerogative)**: Chapter 14에서 다루는 개념으로, 포함 적절.
- **counterpoint**: 홉스 제29장(주권 분할 = 해체), 몽테스키외 법의 정신 제11권 — 정확.

### locke-claim-006 (소유권 노동이론) — 정확
- **source_detail**: Chapter 5, §25-51 — 정확.
- **original_text**: §27의 유명한 구절 정확 인용. "every man has a property in his own person... The labour of his body, and the work of his hands..."
- **두 제한(enough and as good, spoilage proviso)**: 정확.
- **화폐의 발명이 축적 제한 극복**: §36-50의 정확한 요약.
- **counterpoint**: 마르크스 자본론 1권 24장(본원적 축적) — 정확. 노직의 '토마토 주스' 반례 — Anarchy, State, and Utopia (1974) p.175에서의 유명한 반론, 정확.

### locke-claim-007 (동의에 의한 정부) — 정확
- **source_detail**: Chapter 8, §116-122 — 정확.
- **original_text**: §119의 정확한 인용. 묵시적 동의(tacit consent) 관련 핵심 구절.
- **명시적/묵시적 동의 구분**: 정확.
- **counterpoint**: 흄의 배(ship) 비유 — 정확. 시먼스(Simmons)의 Moral Principles and Political Obligations (1979) — 정확한 학술 참조.

### locke-claim-008 (제한적 정부) — 정확
- **source_detail**: Chapter 11, §134-142 — 정확.
- **네 가지 제한**: (1) 자의적 권력 금지, (2) 확립된 법률, (3) 동의 없는 과세 금지, (4) 입법권 위임 금지 — §135-142의 정확한 요약.
- **counterpoint**: 홉스 제18장, 보댕 국가론(Les Six Livres de la République, 1576) — 정확.

### locke-claim-009 (관용) — 정확
- **source_detail**: A Letter Concerning Toleration, pp. 5-20 (ed. Tully) — Jeremy Waldron/James Tully 편집본 참조, 적절.
- **original_text**: 서한의 도입부 유명한 구절 정확 인용. "a society of men constituted only for the procuring, preserving, and advancing of their own civil interests."
- **세 논증(관할권, 비효과성, 교회의 본질)**: 정확한 분류.
- **관용의 한계(무신론자, 외국 군주 충성자)**: 정확.
- **counterpoint**: 홉스 리바이어던 3~4부(종교와 주권), 피에르 벨(Pierre Bayle) Dictionnaire 1697 — 정확. 벨이 무신론자까지 관용을 확장한 점도 정확.

### locke-claim-010 (타불라 라사) — 정확
- **source_detail**: Book I, Chapters 2-4; Book II, Chapter 1 — 정확.
- **original_text**: Book II, Chapter 1, §2의 유명한 "white paper" 구절 정확 인용.
- **세 유형의 본유관념 반박**: 정확한 요약.
- **counterpoint**: 데카르트 성찰 제3성찰(신의 본유관념), 라이프니츠 인간오성신론(Nouveaux Essais, 1704 집필/1765 출판) — 정확. "무늬 있는 대리석(veined marble)" 비유 — 라이프니츠의 유명한 반례로 정확. 촘스키 보편문법 — 현대적 확장으로 적절.
- **라이프니츠 연도**: "1704/1765" — 정확 (1704년 집필, 로크 사망으로 출판 보류, 1765년 출판).

### locke-claim-011 (입법권의 우위) — 보통 (수정 권장)
- **source_detail**: Chapter 11, §134; Chapter 13, §149-152 — 정확.
- **original_text**: §149의 정확한 인용.
- **내용 자체는 정확**하나, **claim-005와 상당 부분 중복**됨. 두 claim 모두 §149의 동일 구절을 인용하며, "입법권의 우위"와 "인민의 최고 권력"은 claim-005의 권력 분립론에서도 이미 다루고 있다. claim-011은 "인민의 최고 권력 > 입법권 > 집행권"이라는 위계를 더 명시적으로 정리하는 점에서 가치가 있으나, 독립된 claim으로 분리할 필요성은 논쟁적이다.
- **counterpoint**: 홉스 제18장, 오스틴 Province of Jurisprudence Determined (1832) — 정확.

**이슈**: claim-005와 claim-011의 내용 중복. 동일 original_text 인용. 학습 가이드에서 혼동 가능성 있음.
- **심각도**: 경미 (표현개선/구조 정리)
- **권장**: claim-005에서 권력 분립(입법·집행·동맹권의 분리와 상호 관계)에 집중하고, claim-011에서 인민주권론(인민의 최고 권력이 입법권 위에 있음, 저항권과의 연결)에 집중하도록 차별화. 또는 하나로 통합.

### locke-claim-012 (재산권 불가침, 동의 없는 과세 금지) — 정확
- **source_detail**: Chapter 11, §138-140 — 정확.
- **original_text**: §140의 정확한 인용.
- **'대표 없이 과세 없다(no taxation without representation)' 연결**: 정확.
- **인지세법(Stamp Act, 1765)**: 정확한 역사적 맥락.
- **counterpoint**: 홉스 제18장 — 정확.

**Claims 종합: 12건 중 11건 정확, 1건 수정 권장 (경미)**

---

## 4. Keywords 검증

10건 전수 확인.

| ID | 키워드 | 판정 | 비고 |
|----|--------|------|------|
| locke-kw-001 | 자연 상태 (State of Nature) | 정확 | definition에서 홉스와의 차이 정확히 설명. source: Ch.2 정확 |
| locke-kw-002 | 자연권 (Natural Rights) | 정확 | 생명·자유·재산의 넓은 의미 property 설명 정확 |
| locke-kw-003 | 사회계약/동의 (Social Contract/Consent) | 정확 | 자연법 집행권만 양도한다는 설명 정확 |
| locke-kw-004 | 신탁 (Trust) | 정확 | fiduciary power, trustee/settlor 관계 정확 |
| locke-kw-005 | 저항권 (Right of Resistance) | 정확 | 신탁 위반 시 권력 귀속(devolution) 설명 정확 |
| locke-kw-006 | 타불라 라사 (Tabula Rasa) | 정확 | white paper, 감각/반성의 두 원천, 정치적 함의 정확 |
| locke-kw-007 | 소유권 노동이론 (Labor Theory of Property) | 정확 | mix labour, enough-and-as-good, spoilage proviso 정확 |
| locke-kw-008 | 관용 (Toleration) | 정확 | 시민적 이익 한정, 무신론 배제 정확 |
| locke-kw-009 | 제한적 정부 (Limited Government) | 정확 | related_claims에 005, 008, 012 매핑 적절 |
| locke-kw-010 | 동의에 의한 정부 (Government by Consent) | 정확 | 필머 왕권신수설 대립 구도 정확 |

**스키마 참고**: keywords에서 architecture.md 스키마의 `term_en`, `work_id`, `related_terms` 필드 대신 `term_original`, `related_claims`, `source` 필드를 사용하고 있음. 이는 홉스 데이터와 동일한 패턴이므로 로크 고유의 문제가 아니라 프로젝트 전반의 스키마 불일치임. 별도 이슈로 관리 권장.

**판정: 10건 모두 정확**

---

## 5. Relations 검증

| ID | 방향 | 판정 | 비고 |
|----|------|------|------|
| relation-hobbes-locke | hobbes -> locke (influenced) | 정확 | 홉스가 로크에 영향(비판적 계승). 방향 규칙 준수. 자연 상태론/사회계약론 비판적 수용 설명 정확 |
| relation-locke-rousseau | locke -> rousseau (influenced) | 정확 | 루소가 로크의 사회계약론 영향받되 소유권 비판. 인간 불평등 기원론(1755), 사회계약론(1762) 연도 정확 |
| relation-locke-montesquieu | locke -> montesquieu (influenced) | 정확 | 권력 분립론 발전(입법·집행 -> 삼권분립). 법의 정신(1748) 제11권 참조 정확 |
| relation-locke-american-founders | locke -> jefferson (influenced) | 보통 | 내용 정확하나 아래 이슈 참조 |
| relation-locke-kant | locke -> kant (influenced) | 정확 | 경험주의 인식론 + 정치철학 영향. 순수이성비판(1781) 참조 정확. strength "보통"은 적절(칸트는 로크를 비판적으로 종합했으므로) |

### relation-locke-american-founders 이슈

- **심각도**: 경미 (표현개선)
- **내용**: `to_thinker: "jefferson"` — jefferson은 ethics-thinkers 인덱스에 존재하지 않는 사상가 ID. 현재 시스템에서 orphan reference 상태. 이는 현재 프로젝트가 윤리 임용시험 범위의 사상가를 대상으로 하므로 제퍼슨이 아직 입력되지 않은 것이 자연스러우나, 참조 무결성(referential integrity) 측면에서 문제가 될 수 있음.
- **권장**: (1) 향후 제퍼슨 데이터 입력 시 자연 해소, 또는 (2) `to_thinker`를 "american-founders"와 같은 일반적 ID로 변경하여 특정 사상가 의존 제거. 루소(rousseau), 몽테스키외(montesquieu)도 아직 미입력 상태이지만, 이들은 윤리 임용시험 범위 내 사상가로 향후 입력 예정이 예상됨.

### relations 스키마 참고
- architecture.md 스키마에서는 `evidence` 필드를 정의하고 있으나, 실제 로크 relations에는 `strength`, `period` 필드 사용. 홉스 데이터도 동일 패턴. 프로젝트 전반 스키마 불일치이며 로크 고유 문제 아님.

**판정: 5건 중 4건 정확, 1건 경미 이슈**

---

## 6. 특별 검증 항목

### 홉스와의 비교 맥락

| 비교 주제 | claim | 정확성 |
|-----------|-------|--------|
| 자연 상태: 전쟁(홉스) vs 자연법 질서(로크) | 001 | 정확 |
| 자연권: 무제한(홉스) vs 자연법 제한(로크) | 002 | 정확 |
| 사회계약: 전체 양도(홉스) vs 집행권만 양도(로크) | 003 | 정확 |
| 저항권: 불가(홉스) vs 가능(로크) | 004 | 정확 |
| 주권: 절대(홉스) vs 제한적(로크) | 005, 008 | 정확 |
| 종교: 주권자 통제(홉스) vs 교회-국가 분리(로크) | 009 | 정확 |
| 권력 분할: 해체(홉스) vs 분립(로크) | 005, 011 | 정확 |

홉스-로크 비교는 정치철학의 가장 기본적인 대비 구도이며, 모든 claim에서 정확하게 서술되었다.

### Two Treatises의 Second Treatise 인용 정확성

12개 claim 중 10개가 Second Treatise를 참조. 모든 장/절 번호가 정확하며, original_text의 영어 인용이 원전(Peter Laslett 편집 Cambridge Texts 판본 기준)과 일치한다. 특히:
- §4 (자연 상태 정의) — 정확
- §6 (자연법) — 정확
- §27 (노동혼합) — 정확
- §95 (동의) — 정확
- §119 (묵시적 동의) — 정확
- §134, §149 (입법권) — 정확
- §140 (과세 동의) — 정확
- §222 (저항권) — 정확

### 소유권 노동이론의 원전 근거

claim-006은 Chapter 5 (Of Property), §25-51을 참조. 핵심 논증 구조(자기 소유 -> 노동혼합 -> 전유)와 두 제한(enough-and-as-good, spoilage proviso), 화폐를 통한 제한 극복 논증이 모두 원전에 충실하다. counterpoint의 마르크스, 노직 반론도 학술적으로 정확.

---

## 7. 코드 이슈

없음. 데이터 입력 스크립트(`projects/ethics-study/scripts/insert_locke.py`)는 검증 범위 밖이나, ES에 저장된 데이터 자체의 정확성은 확인됨.

---

## 8. 이슈 요약

### 이슈 1: claim-005와 claim-011 내용 중복
- **심각도**: 경미
- **위치**: locke-claim-005, locke-claim-011
- **내용**: 두 claim 모두 입법권의 우위를 다루며 §149의 동일 구절을 인용. claim-005는 권력 분립(입법·집행·동맹권), claim-011은 인민주권론에 초점이 있으나, 상당 부분 중복됨.
- **권장**: 각 claim의 초점을 더 명확히 분리하거나, 하나로 통합.

### 이슈 2: relation-locke-american-founders의 to_thinker 참조
- **심각도**: 경미
- **위치**: relation-locke-american-founders
- **내용**: `to_thinker: "jefferson"` — 해당 ID가 ethics-thinkers에 미존재. orphan reference.
- **권장**: 향후 데이터 확장 시 자연 해소 예상. 당장 수정 불필요하나 인지 필요.

### 참고 (로크 고유 이슈 아님)
- keywords와 relations의 필드 구조가 architecture.md 스키마와 불일치 (홉스 등 기존 데이터도 동일 패턴). 프로젝트 전반 스키마 정비 시 일괄 처리 권장.
