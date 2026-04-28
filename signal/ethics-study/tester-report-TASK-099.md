# Tester Report — TASK-099

## 상태: DONE

## 태스크
- **Task ID**: TASK-099
- **Title**: 홉스 데이터 검증

## 검증 요약

| 카테고리 | 건수 | 정확 | 수정필요 | 심각 |
|----------|------|------|----------|------|
| thinker | 1 | 1 | 0 | 0 |
| works | 5 | 4 | 1 | 0 |
| claims | 14 | 11 | 3 | 0 |
| keywords | 10 | 10 | 0 | 0 |
| relations | 5 | 5 | 0 | 0 |
| **합계** | **35** | **31** | **4** | **0** |

---

## 1. Thinker 검증

### hobbes — 정확

- **생몰년**: 1588~1679 — 정확. 홉스는 1588년 4월 5일 Westport(Malmesbury 인근)에서 출생, 1679년 12월 4일 사망. 91세 장수.
- **국적/배경**: 영국, 성직자의 아들 — 정확. 아버지는 Westport의 교구 목사(vicar)였으나 싸움 끝에 도주했고, 홉스는 삼촌에게 양육됨. 배경 서술에서는 "성직자의 아들"로 간략화했는데, 엄밀히는 아버지가 도주 후 홉스를 버렸다는 점이 빠져 있으나, 학술적 오류는 아님.
- **옥스퍼드 모들린 홀(Magdalen Hall)**: 정확. 홉스는 1603년 입학, 1608년 학사 학위.
- **캐번디시 가문 가정교사**: 정확. 데번셔 백작(Earl of Devonshire) 캐번디시 가문.
- **갈릴레오, 가상디, 메르센 교류**: 정확. 1634~1636년경 유럽 여행에서 갈릴레오를 만남(1636년 피렌체). 메르센 서클에 참여.
- **1640년 파리 망명, 약 11년 체류**: 정확. 1640년 말 파리로 떠나 1651년 귀국.
- **core_philosophy**: '고독하고, 가난하고, 험악하고, 잔인하고, 짧다' — "solitary, poor, nasty, brutish, and short" (Leviathan I.13)의 정확한 번역.
- **philosophical_journey**: 투키디데스 번역(1629), Elements of Law(1640), De Cive(1642), Leviathan(1651), De Corpore(1655), De Homine(1658) — 모든 연도 정확. 원의 구적법(squaring the circle) 논쟁, 호메로스 번역도 사실.

**판정: 정확**

---

## 2. Works 검증

### hobbes-leviathan — 정확
- **제목**: Leviathan, or The Matter, Forme and Power of a Commonwealth Ecclesiasticall and Civil — 정확 (원제의 정확한 전문)
- **연도**: 1651 — 정확
- **4부 구성**: Of Man / Of Commonwealth / Of a Christian Commonwealth / Of the Kingdom of Darkness — 정확
- **significance**: 서양 정치사상사 핵심 저작이라는 평가 적절

### hobbes-de-cive — 정확
- **원제**: De Cive (Philosophical Rudiments Concerning Government and Society) — 정확. 라틴어판은 1642년, 영어판(Philosophical Rudiments)은 1651년.
- **연도**: 1642 — 정확 (라틴어 초판 기준)
- **3부 구성**: Liberty, Dominion, Religion — 정확

### hobbes-de-corpore — 정확
- **연도**: 1655 — 정확
- **삼부작 제1부**: 정확 (De Corpore - De Homine - De Cive 순서)

### hobbes-de-homine — 정확
- **연도**: 1658 — 정확
- **광학에 상당 부분 할애**: 정확. 전체 15장 중 상당수가 광학 관련.

### hobbes-elements-of-law — 수정필요 (경미)
- **원제**: The Elements of Law, Natural and Politic — 정확
- **연도**: 1640 — 이 연도는 필사본 유통 시점으로 정확. 출판은 1650년(두 부분으로 분리: Human Nature + De Corpore Politico). significance에서 "출판은 1650년"이라고 명시하고 있어 적절.
- **2부 구성**: Human Nature + De Corpore Politico — 정확
- **이슈**: significance에서 "1640년 장기의회(Long Parliament) 소집"이라고 했는데, 장기의회 소집은 1640년 11월 3일이 맞음. 그러나 홉스가 신변 위협을 느끼고 떠난 것은 장기의회 소집 직후(1640년 11월경)이므로 인과관계 서술은 정확. 다만 Elements of Law가 유통된 것은 1640년 5월(단기의회 시기)로, 장기의회보다 먼저임. "장기의회 소집"이 직접적 원인처럼 보이는 서술은 다소 부정확.

**심각도: 경미** — 시기적 뉘앙스 차이. 더 정확하게는 "1640년 5월 단기의회/11월 장기의회 소집 시기에" 정도로 수정 권장.

---

## 3. Claims 검증

### hobbes-claim-001 (자연 상태) — 정확
- **출처**: Leviathan, Part I, Chapter 13 — 정확
- **original_text**: "Whatsoever therefore is consequent to a time of war..." — Leviathan I.13의 정확한 인용. 원전 대조 결과 일치.
- **original_text_ko**: 한국어 번역 정확
- **counterpoint**: 로크(통치론 제2론 2장), 루소(인간 불평등 기원론 1755) — 정확. 루소의 pitie(동정심) 개념 정확.

### hobbes-claim-002 (자연권) — 정확
- **출처**: Leviathan, Part I, Chapter 14 — 정확
- **original_text**: "The right of nature, which writers commonly call jus naturale..." — I.14 정확 인용
- **original_text_ko**: 번역 정확
- **counterpoint**: 로크의 생명·자유·재산 제한적 권리 vs 홉스의 무제한적 자연권 — 정확한 대비. 루소 사회계약론 1권 인용도 적절.

### hobbes-claim-003 (자연법) — 정확
- **출처**: Leviathan, Part I, Chapters 14-15 — 정확
- **original_text**: "A law of nature, lex naturalis, is a precept..." — I.14 정확 인용
- **제1~3 자연법 서술**: 정확. 제1법(평화 추구), 제2법(상호 권리 포기), 제3법(약속 이행=정의)
- **in foro interno / in foro externo 구분**: 정확 (Leviathan I.15)
- **counterpoint**: 아퀴나스 Summa Theologiae I-II, q.91, a.2 — 정확한 출처. 로크의 반론도 정확.

### hobbes-claim-004 (사회계약) — 정확
- **출처**: Leviathan, Part II, Chapter 17 — 정확
- **original_text**: "I authorise and give up my right of governing myself..." — II.17 정확 인용 (홉스 사회계약 공식)
- **주권자가 계약 당사자가 아니라는 설명**: 정확. 이것이 로크와의 핵심 차이.
- **counterpoint**: 로크(2단계 계약 + trust), 루소(일반의지에의 양도) — 정확

### hobbes-claim-005 (절대주권) — 정확
- **출처**: Leviathan, Part II, Chapter 18 — 정확
- **original_text**: "For what is it to divide the power of a Commonwealth, but to dissolve it..." — II.18에서의 정확한 인용
- **12가지 주권자 권리**: 정확 (Leviathan II.18에 열거)
- **counterpoint**: 로크(입법권/집행권 분리), 몽테스키외(삼권분립), 매디슨(견제와 균형) — 모두 정확

### hobbes-claim-006 (대리/Authorization) — 정확
- **출처**: Leviathan, Part I, Chapter 16; Part II, Chapter 17 — 정확
- **original_text**: "A multitude of men are made one person when they are by one man, or one person, represented..." — I.16 정확 인용
- **author/actor 구분**: 정확 (Leviathan I.16의 핵심 개념)
- **counterpoint**: 루소의 대표 불가능성 비판 + "영국인들은 선거 때만 자유롭다" 인용 — 정확 (사회계약론 III.15)

### hobbes-claim-007 (자기보존 양도 불가) — 정확
- **출처**: Leviathan, Part I, Chapter 14; Part II, Chapter 21 — 정확
- **original_text**: "A man cannot lay down the right of resisting them that assault him by force to take away his life..." — I.14 정확 인용
- **counterpoint**: 로크(저항권 확대), 필머(Patriarcha, 1680) — 정확. 다만 Patriarcha는 1680년 출판이지만 집필은 1630~1640년대. 출판 연도 기준으로는 정확.

### hobbes-claim-008 (커먼웰스=인공 인간) — 수정필요 (경미)
- **출처**: Leviathan, Introduction; Part II, Chapter 17 — 정확
- **original_text**: "For by art is created that great Leviathan called a Commonwealth..." — Introduction 정확 인용
- **이슈**: claim 본문에서 "보상과 처벌은 신경"이라고 했는데, 원문(Introduction)에서는 "Reward and Punishment (by which fastened to the seat of the Sovereignty, every joint and member is moved to perform his duty) are the Nerves"로, 보상과 처벌이 신경(Nerves)이라는 것은 맞음. 그러나 원문에서 "재산과 부(Wealth and Riches)는 힘(Strength)"이라는 비유도 있는데, claim에서 이 부분의 순서가 원문과 약간 다르게 나열됨. 내용 자체는 정확하나, 원문의 전체 비유 체계(Sovereignty=Soul, Magistrates=Joints, Reward and Punishment=Nerves, Wealth and Riches=Strength, Salus Populi=Business, Counsellors=Memory, Equity and Laws=Reason and Will, Concord=Health, Sedition=Sickness, Civil War=Death)를 일부만 발췌한 것이므로 오류라기보다 축약.

**판정: 정확 (축약이지만 오류 아님)**

### hobbes-claim-009 (유물론적 인간관) — 수정필요 (경미)
- **출처**: Leviathan, Part I, Chapters 1-6; De Corpore, Part IV — 정확
- **original_text**: "All which qualities, called 'sensible', are, in the object that causeth them, but so many several motions of the matter..." — I.1 정확 인용
- **이슈**: claim에서 "비물질적 실체(incorporeal substance)는 모순이다"라고 했는데, 이 표현의 정확한 출처는 Leviathan IV.46 ("If this superstitious fear of spirits were taken away... the bodies... also would be much more fitted")보다는 Leviathan III.34에서 "the word body and substance... are the same" 등에서 파생됨. 홉스가 "incorporeal substance"를 "contradiction in terms"이라 한 것은 Leviathan IV.46에 있음: "the Universe... being the aggregate of all bodies, there is no real part thereof that is not also body." 직접적으로 "incorporeal substance is a contradiction" 문구는 Leviathan에 정확히 나오며(IV.46), 주장의 학술적 정확성에 문제 없음.
- **counterpoint**: 데카르트 Meditationes(1641) 6성찰, 홉스의 Third Set of Objections(1641) — 정확. 칸트 순수이성비판 변증론 언급도 적절.

**판정: 정확**

### hobbes-claim-010 (정의=약속이행) — 정확
- **출처**: Leviathan, Part I, Chapter 15 — 정확
- **original_text**: "The definition of injustice is no other than the not performance of covenant." — I.15 정확 인용
- **counterpoint**: 플라톤(국가 4권), 아리스토텔레스(NE 5권) — 정확

### hobbes-claim-011 (신민의 자유) — 정확
- **출처**: Leviathan, Part II, Chapter 21 — 정확
- **original_text**: "The liberty of a subject lieth therefore only in those things which, in regulating their actions, the sovereign hath praetermitted..." — II.21 정확 인용
- **counterpoint**: 로크(법 아래의 자유), 밀(위해 원칙) — 정확. 벌린(Two Concepts of Liberty, 1958) 언급도 적절.

### hobbes-claim-012 (자연적 평등) — 정확
- **출처**: Leviathan, Part I, Chapter 13 — 정확
- **original_text**: "Nature hath made men so equal in the faculties of body and mind..." — I.13 정확 인용
- **counterpoint**: 아리스토텔레스(정치학 1권 자연 노예론), 니체(선악의 저편 1886, 9장 서열) — 정확

### hobbes-claim-013 (세 가지 정체) — 수정필요 (경미)
- **출처**: Leviathan, Part II, Chapter 19 — 정확
- **original_text**: "The difference of Commonwealths consisteth in the difference of the sovereign..." — II.19 정확 인용
- **이슈**: claim 본문에서 "귀족정(aristocracy, 합의체의 일부)"이라 했는데, original_text에서는 "an assembly of a part only"라 하여 일치. 그러나 argument의 (2b)에서 "인민이 부유해야 군주도 부유"라는 논증은 Leviathan II.19의 실제 홉스 논증과 약간 단순화된 것임. 원문에서 홉스는 군주의 사적 이익과 공적 이익의 일치를 말하지만, 단순히 "인민이 부유해야 군주도 부유"보다 더 복잡한 논증을 전개함 (군주의 영광, 힘, 안전이 인민의 부와 힘에 의존). 단순화이지 오류는 아님.
- **counterpoint**: 아리스토텔레스(정치학 3~4권 정체 분류), 몽테스키외(법의 정신 1748) — 정확. 몽테스키외의 세 정체(공화정, 군주정, 전제정)와 원리(덕, 명예, 공포) 서술 정확.

**판정: 정확 (단순화이나 오류 아님)**

### hobbes-claim-014 (공포와 복종) — 수정필요 (보통)
- **출처**: Leviathan, Part I, Chapter 14; Part II, Chapter 20 — 정확
- **original_text**: "Covenants entered into by fear, in the condition of mere nature, are obligatory." — I.14 정확 인용
- **이슈**: claim 본문에서 "정복에 의한 커먼웰스(Commonwealth by acquisition)도 제도에 의한 커먼웰스(Commonwealth by institution)와 동일한 정당성을 가진다"고 했는데, 이는 정확하지만 보다 정밀하게 말하면, Leviathan II.20에서 홉스는 acquisition에 의한 커먼웰스에서 "주권자의 권리와 신민의 의무(rights and consequences)"가 institution에 의한 것과 "the same"이라고 했을 뿐, "정당성(legitimacy)"이라는 표현을 직접 쓰지는 않았음. 현대적 재해석이 가미된 표현.
- **counterpoint**: 로크(통치론 제2론 16장, 정복은 강압이지 동의가 아님) — 정확. 로크의 "강도에게 맺은 약속" 비유는 Second Treatise에 실제로 있음.

**심각도: 보통** — "동일한 정당성"이라는 표현은 홉스 원문의 "same rights and consequences"를 확대해석한 것. 수정 권장: "동일한 권리와 결과를 가진다"로.

---

## 4. Keywords 검증

10건 모두 검증 완료.

| ID | 용어 | 판정 | 비고 |
|----|------|------|------|
| hobbes-kw-001 | 자연 상태 | 정확 | 정의, 출처(I.13), related_claims 매핑 정확 |
| hobbes-kw-002 | 사회계약 | 정확 | covenant/social contract 구분, 주권자 비당사자 설명 정확 |
| hobbes-kw-003 | 주권자 | 정확 | 12가지 권한 요약 정확, related_claims 매핑 정확 |
| hobbes-kw-004 | 자연법 | 정확 | 제1~3 자연법 서술 정확, lex naturalis 원어 정확 |
| hobbes-kw-005 | 자연권 | 정확 | jus naturale 원어, 자연권(자유) vs 자연법(의무) 구분 정확 |
| hobbes-kw-006 | 리바이어던 | 정확 | 욥기 출전, mortal god, 표지 이미지 설명 정확 |
| hobbes-kw-007 | 대리(Authorization) | 정확 | author/actor 구분, 대의민주주의 선구 평가 적절 |
| hobbes-kw-008 | 커먼웰스 | 정확 | by institution / by acquisition 구분 정확 |
| hobbes-kw-009 | 만인에 대한 만인의 투쟁 | 정확 | 라틴어 원문(bellum omnium contra omnes), De Cive 1장 출처도 정확 |
| hobbes-kw-010 | 자기보존 | 정확 | 양도 불가능성, 저항권과의 관계 정확 |

**판정: 전체 정확**

---

## 5. Relations 검증

| ID | 방향 | 판정 | 비고 |
|----|------|------|------|
| relation-machiavelli-hobbes | 마키아벨리 → 홉스 | 정확 | 간접적 영향(strength: 보통)은 적절한 평가. 마키아벨리(1469~1527) 생몰년 정확. 군주론(Il Principe, 1532) 출판년도 정확. 정치의 도덕/종교 독립 영향 서술 정확. |
| relation-hobbes-locke | 홉스 → 로크 | 정확 | 로크(1632~1704) 생몰년 정확. Two Treatises(1689) 정확. 비판적 계승 평가 적절. strength: 강함 — 적절. |
| relation-hobbes-rousseau | 홉스 → 루소 | 정확 | 루소(1712~1778) 생몰년 정확. 인간 불평등 기원론(1755), 사회계약론(1762) 정확. 일반의지(volonte generale)에 주권 위치 설명 정확. |
| relation-hobbes-rawls | 홉스 → 롤스 | 정확 | 롤스(1921~2002) 생몰년 정확. Theory of Justice(1971) 정확. original position과 자연 상태의 대응 설명 적절. strength: 보통 — 적절(간접적 영향). |
| relation-hobbes-spinoza | 홉스 → 스피노자 | 정확 | 스피노자(1632~1677) 생몰년 정확. Tractatus Theologico-Politicus(1670) 정확. 자연권=potentia 동일시, 사상/표현의 자유 강조 차이 정확. strength: 강함 — 적절. |

**방향 규칙**: 모든 관계에서 "from이 to에게 influenced" 규칙 준수 확인.

**판정: 전체 정확**

---

## 이슈 목록

### 이슈 1 (경미): hobbes-elements-of-law significance 시기 표현
- **위치**: works / hobbes-elements-of-law / significance
- **현재**: "영국 내전 직전(1640년 장기의회 소집)에 왕당파 입장을 담아 작성"
- **문제**: Elements of Law는 1640년 5월(단기의회 시기)에 유통 시작. 장기의회는 11월 소집. 홉스의 망명 결정에는 장기의회 소집이 영향을 미쳤으나, 저작 유통 자체는 단기의회 시기.
- **수정 제안**: "1640년 단기의회·장기의회 소집 시기에 왕당파 입장을 담아 작성·유통되었으며"

### 이슈 2 (보통): hobbes-claim-014 "동일한 정당성" 표현
- **위치**: claims / hobbes-claim-014 / claim 본문
- **현재**: "동일한 정당성을 가진다"
- **문제**: 홉스 원문(II.20)은 "same rights and consequences"라 했지 "same legitimacy"라 하지 않음. "정당성"은 현대적 재해석이 가미된 표현.
- **수정 제안**: "동일한 주권자 권리와 신민의 의무를 가진다"

### 이슈 3 (경미): hobbes-claim-013 argument 단순화
- **위치**: claims / hobbes-claim-013 / argument (2b)
- **현재**: "인민이 부유해야 군주도 부유"
- **문제**: 원문은 군주의 부, 힘, 안전이 인민의 그것에 의존한다는 더 넓은 논증
- **수정 제안**: "군주의 부, 힘, 안전이 인민의 그것에 의존하므로 사적 이익과 공적 이익이 일치하는 경향"

### 이슈 4 (경미): thinker background "성직자의 아들" 단순화
- **위치**: thinkers / hobbes / background
- **현재**: "성직자의 아들로 태어났다"
- **문제**: 아버지는 교구 목사(vicar)였으나, 싸움 후 도주하여 홉스를 삼촌(Francis Hobbes)이 양육. 한국 윤리 임용시험 맥락에서는 이 정도 상세 사항이 불필요할 수 있으나, 학술적으로는 보충 가능.
- **수정 제안**: 수정 불필요 (임용시험 맥락에서 과도한 상세). 참고사항으로만 기록.

---

## 원전 인용 교차 검증 결과

14개 claim의 original_text(영어 원문)를 Leviathan 원전과 대조한 결과:

| Claim | 출처 | 원문 일치 | 비고 |
|-------|------|-----------|------|
| 001 | I.13 | 일치 | "solitary, poor, nasty, brutish, and short" 포함 |
| 002 | I.14 | 일치 | jus naturale 정의 |
| 003 | I.14 | 일치 | lex naturalis 정의 |
| 004 | II.17 | 일치 | 사회계약 공식 |
| 005 | II.18 | 일치 | 주권 분할 = 해체 |
| 006 | I.16 | 일치 | 대표의 통일 |
| 007 | I.14 | 일치 | 저항권의 양도 불가 |
| 008 | Intro | 일치 | 인공 인간 |
| 009 | I.1 | 일치 | 운동 = 운동 산출 |
| 010 | I.15 | 일치 | 부정의 = 약속 불이행 |
| 011 | II.21 | 일치 | 법의 침묵에서의 자유 |
| 012 | I.13 | 일치 | 자연적 평등 |
| 013 | II.19 | 일치 | 세 정체 구분 |
| 014 | I.14 | 일치 | 공포에 의한 약속의 구속력 |

**결과: 14건 모두 원전 일치 확인**

---

## 한국어 번역(original_text_ko) 검증

14건의 한국어 번역을 영어 원문과 대조한 결과, 모두 의미적으로 정확한 번역임을 확인. 학술 번역 수준의 충실한 직역으로, 한국 윤리 임용시험용으로 적절함.

---

## 종합 판정

전체 35건 중 심각한 사실 오류(factual error) 0건. 경미한 표현 개선 사항 3건, 보통 수준의 표현 정밀화 필요 1건. 홉스의 정치철학 핵심 개념(자연 상태, 자연권, 자연법, 사회계약, 주권자론, 커먼웰스)이 원전에 충실하게 입력되어 있으며, 14건의 Leviathan 원문 인용이 모두 정확. counterpoint에서 인용되는 사상가(로크, 루소, 아리스토텔레스, 플라톤, 데카르트, 칸트, 니체, 몽테스키외, 롤스, 밀, 벌린, 아퀴나스, 필머, 헤겔, 매디슨)의 저서와 주장도 학술적으로 정확.

한국 윤리 임용시험 맥락에서 정치철학 영역의 홉스 관련 핵심 내용이 충분하고 정확하게 포함되어 있음.
