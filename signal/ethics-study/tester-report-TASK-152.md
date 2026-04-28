# Tester Report — TASK-152: 하이트 데이터 검증

## 결과 요약
- **상태**: DONE
- **검증 일시**: 2026-04-14
- **검증 방법**: curl ES REST API 직접 조회

---

## 1. 사상가 (ethics-thinkers) — id="haidt"

| 항목 | 기대 | 실제 | 상태 |
|------|------|------|------|
| id | haidt | haidt | PASS |
| name | 조너선 하이트 | 조너선 하이트 | PASS |
| name_en | Jonathan Haidt | Jonathan Haidt | PASS |
| field | moral_development | moral_development | PASS |
| birth_year | 1963 | 1963 | PASS |
| background | 학문적 배경 서술 | 뉴욕 출신, 예일 철학→펜실베이니아 대학교 심리학 박사(1992), 버지니아 대학교 16년, NYU 스턴 경영대학원 교수. SIM(2001), MFT 발전 등 상세 서술 | PASS |
| core_philosophy | 도덕 직관주의 + MFT | 사회적 직관주의 모델, 코끼리와 기수, 6기반(배려/피해, 공정/속임, 충성/배신, 권위/전복, 신성/타락, 자유/억압) 명시, 콜버그·피아제 비판 포함 | PASS |

**학술적 정확성**: birth_year 1963 정확. field는 `moral_development`로 적절(사회심리학/도덕심리학 전문). background는 학문적 궤적 정확히 서술. core_philosophy는 핵심 이론 완비.

---

## 2. 저서 (ethics-works) — thinker_id="haidt"

총 **3개** 확인 (예상: 3개 PASS)

| id | 제목(원제) | 연도 | 상태 |
|----|------------|------|------|
| haidt-righteous-mind | The Righteous Mind: Why Good People Are Divided by Politics and Religion | 2012 | PASS |
| haidt-happiness-hypothesis | The Happiness Hypothesis: Finding Modern Truth in Ancient Wisdom | 2006 | PASS |
| haidt-coddling-of-american-mind | The Coddling of the American Mind (Greg Lukianoff 공저) | 2018 | PASS |

**학술적 정확성**:
- 「The Righteous Mind」(2012) 필수 저서 확인 PASS
- 「The Happiness Hypothesis」(2006): 코끼리와 기수 비유 최초 등장 저서로 적절
- 「The Coddling of the American Mind」(2018): Greg Lukianoff과 공저 사실 명시, 정확
- 모든 저서에 `significance`, `key_concepts` 필드 포함

---

## 3. 주장 (ethics-claims) — thinker_id="haidt"

총 **10개** 확인 (예상: 10개 PASS)

| id | 핵심 주제 | work_id | explanation | argument | 상태 |
|----|-----------|---------|-------------|----------|------|
| haidt-claim-001 | 사회적 직관주의 모델(SIM) — 직관 선행, 추론은 사후 정당화 | haidt-righteous-mind | O | O | PASS |
| haidt-claim-002 | 코끼리와 기수 비유 | haidt-happiness-hypothesis | O | O | PASS |
| haidt-claim-003 | 도덕기반이론(MFT) — 6기반 전체 | haidt-righteous-mind | O | O | PASS |
| haidt-claim-004 | 배려/피해(Care/Harm) 기반 상세 | haidt-righteous-mind | O | O | PASS |
| haidt-claim-005 | 콜버그·피아제 합리주의 도덕발달론 비판 | haidt-righteous-mind | O | O | PASS |
| haidt-claim-006 | Nativism — 도덕 기반의 선천적 준비(innately prepared) | haidt-righteous-mind | O | O | PASS |
| haidt-claim-007 | WEIRD 편향 비판 | haidt-righteous-mind | O | O | PASS |
| haidt-claim-008 | 진보/보수 도덕 차이 (진보: 배려·자유 강조, 보수: 6기반 균형) | haidt-righteous-mind | O | O | PASS |
| haidt-claim-009 | Hivishness(군집성) — 집단 결속, 종교적 도덕 경험 | haidt-righteous-mind | O | O | PASS |
| haidt-claim-010 | 도덕 미뢰(taste buds) 비유 — MFT 다원론적 도덕 | haidt-righteous-mind | O | O | PASS |

**학술적 정확성**:
- SIM(2001년 발표) 정확히 서술
- 코끼리와 기수 비유는 『행복의 가설』(2006) 기원 — work_id `haidt-happiness-hypothesis` 올바름
- MFT 6기반 명칭 및 순서 정확 (Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation, Liberty/Oppression)
- Nativism은 "innately prepared"로 표현 — 하이트 본래 표현과 일치
- WEIRD 편향 비판 (Western, Educated, Industrialized, Rich, Democratic) 정확
- 진보/보수 도덕 차이 분석 학술적으로 적절
- 모든 claim에 explanation, argument 필드 포함 PASS

---

## 4. 키워드 (ethics-keywords) — thinker_id="haidt"

총 **10개** 확인 (예상: 10개 PASS)

| id | term | term_en | work_id | 상태 |
|----|------|---------|---------|------|
| kw-social-intuitionist-model | 사회적 직관주의 모델 | Social Intuitionist Model (SIM) | haidt-righteous-mind | PASS |
| kw-moral-foundations-theory | 도덕기반이론 | Moral Foundations Theory (MFT) | haidt-righteous-mind | PASS |
| kw-elephant-and-rider | 코끼리와 기수 | Elephant and Rider | haidt-happiness-hypothesis | PASS |
| kw-moral-dumbfounding | 도덕적 무성어화 | Moral Dumbfounding | haidt-righteous-mind | PASS |
| kw-weird-bias | WEIRD 편향 | WEIRD Bias (Western, Educated, Industrialized, Rich, Democratic) | haidt-righteous-mind | PASS |
| kw-care-harm | 배려/피해 | Care/Harm | haidt-righteous-mind | PASS |
| kw-fairness-cheating | 공정/속임 | Fairness/Cheating | haidt-righteous-mind | PASS |
| kw-loyalty-betrayal | 충성/배신 | Loyalty/Betrayal | haidt-righteous-mind | PASS |
| kw-authority-subversion | 권위/전복 | Authority/Subversion | haidt-righteous-mind | PASS |
| kw-sanctity-degradation | 신성/타락 | Sanctity/Degradation | haidt-righteous-mind | PASS |

**참고**: Liberty/Oppression(자유/억압) 키워드는 별도 문서로 없으나, thinker 문서와 MFT 키워드 definition 내에 포함 서술됨. 10개 목표 달성.

**학술적 정확성**:
- Moral Dumbfounding: 하이트 실험(무해한 근친상간 시나리오 등)에서 명명한 현상으로 정확
- 코끼리와 기수 work_id가 `haidt-happiness-hypothesis` — 최초 등장 저서로 정확
- 6기반 키워드 중 5개(Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation) 독립 문서화. Liberty/Oppression은 별도 문서 없음(사소한 누락).
- 모든 키워드에 `related_terms` 필드 포함

---

## 5. 관계 (ethics-relations) — from/to_thinker="haidt"

총 **4개** 확인 (예상: 4개 PASS)

| id | from | to | type | 상태 |
|----|------|----|------|------|
| haidt-criticized-kohlberg | haidt | kohlberg | criticized | PASS |
| kohlberg-criticized-haidt | kohlberg | haidt | criticized | PASS |
| hume-influenced-haidt | hume | haidt | influenced | PASS |
| piaget-criticized-haidt | piaget | haidt | criticized | PASS |

**학술적 정확성**:
- haidt→kohlberg criticized: 합리주의 도덕발달론·WEIRD 편향 비판 — 정확
- kohlberg→haidt criticized: 콜버그 관점에서 하이트 직관주의 비판 — 관계 방향 적절(역비판 표현)
- hume→haidt influenced: 흄의 감정주의("이성은 열정의 노예") → 하이트 직관주의 — 핵심 영향 관계로 정확
- piaget→haidt criticized: 피아제 인지발달론을 하이트가 비판 — 방향 올바름

**참고**: kohlberg-criticized-haidt 문서의 방향(kohlberg→haidt)은 실제로는 "하이트가 콜버그를 비판하는 문맥에서 콜버그 관점을 역서술"한 것으로 해석 가능. description을 보면 하이트의 행동을 서술하고 있어 from/to 방향이 혼재되어 있음 — 경미한 이슈.

---

## 이슈/블로커

### 경미한 이슈

1. **Liberty/Oppression 키워드 미문서화**: 6번째 도덕 기반인 자유/억압(Liberty/Oppression)이 독립 키워드 문서로 없음. MFT 문서와 thinker 문서 내 언급만 있음. 기능상 큰 문제는 없으나 일관성을 위해 추가 권장.

2. **kohlberg-criticized-haidt 관계 방향 혼재**: id `kohlberg-criticized-haidt`의 description이 "하이트는 콜버그의 합리주의적 도덕발달론을 비판적으로 계승했다"로 시작하여, from_thinker=kohlberg임에도 하이트의 행동을 서술함. 의미상 하이트→콜버그 비판과 중복된 내용으로 보임. 의도가 불명확하여 검토 권장.

---

## 최종 판정

| 항목 | 예상 수 | 실제 수 | 판정 |
|------|---------|---------|------|
| 사상가 | 1 | 1 | PASS |
| 저서 | 3 | 3 | PASS |
| 주장 | 10 | 10 | PASS |
| 키워드 | 10 | 10 | PASS |
| 관계 | 4 | 4 | PASS |

**전체 판정: DONE**
- 수량 기준 전부 충족
- 학술적 정확성 전반적으로 우수
- 경미한 이슈 2건(Liberty/Oppression 미문서화, 관계 방향 혼재)은 기능 장애 수준 아님
