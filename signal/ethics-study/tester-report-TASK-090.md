# Tester Report — TASK-090

## 상태: DONE

## 검증 요약

원효(wonhyo)와 혜능(huineng) 데이터를 ES에서 조회하여 검증 완료. 전체적으로 양호하나 **이슈 2건** 발견.

---

## 1. ethics-thinkers 검증

### 원효 (wonhyo)
| 항목 | 값 | 판정 |
|------|----|----|
| name | 원효 (元曉) | OK |
| birth_year | 617 | OK |
| death_year | 686 | OK |
| era | 삼국시대/통일신라 | OK |
| field | eastern_ethics | OK |
| background | 해골 바가지 일화, 의상 동행, 요석공주, 설총 등 | OK — 정확 |
| core_philosophy | 화쟁·일심·무애 | OK |
| philosophical_journey | 출가→유학 시도→해골물 깨달음→저술→무애행→입적(686) | OK |
| keywords | 화쟁, 일심, 무애, 대승기신론소, 판비량론, 회통, 해골물 깨달음 | OK |

- **참고**: name에 "元曉"로 표기되었는데, 원효의 한자 이름은 "元曉"가 맞다.

### 혜능 (huineng)
| 항목 | 값 | 판정 |
|------|----|----|
| name | 혜능 (慧能) | OK |
| birth_year | 638 | OK |
| death_year | 713 | OK |
| era | 당(唐) | OK |
| field | eastern_ethics | OK |
| background | 광동 출생, 나무꾼, 금강경 청문, 오조 홍인, 신수 게송 대결 | OK — 정확 |
| core_philosophy | 돈오·자성청정·견성성불·무념·무주·무상 | OK |
| philosophical_journey | 출생→금강경 청문→홍인 문하→육조→법성사 깃발 문답→조계산 포교→입적 | OK |
| keywords | 돈오, 견성성불, 무념, 자성, 육조단경, 자성청정, 남종선 | OK |

---

## 2. ethics-works 검증

### 원효 저서 (3건)

| ID | 저서명 | 저술연도 | 판정 |
|----|--------|---------|------|
| wonhyo-daesunggisinnonso | 대승기신론소 (大乘起信論疏) | 668 | OK — 마명의 대승기신론 주석서. 연도는 추정치이나 학술적으로 합리적 범위 |
| wonhyo-geumgangsaemaerongnon | 금강삼매경론 (金剛三昧經論) | 685 | OK — 원효 만년의 대표 저술. 화쟁 사상의 체계적 전개 |
| wonhyo-panbilyangnon | 판비량론 (判比量論) | 671 | OK — 현장 제자 규기의 논리 비판서. 연도 671년은 통설에 부합 |

### 혜능 저서 (1건)

| ID | 저서명 | 연도 | 판정 |
|----|--------|------|------|
| huineng-platform-sutra | 육조단경 (六祖壇經) | 713 | OK — 제자 법해 등이 편찬한 어록집. 입적 연도와 편찬 연도를 동일시한 것은 합리적 |

---

## 3. ethics-claims 검증

### 원효 claims (3건)

#### wonhyo-claim-001: 화쟁(和諍)
- claim: 불교 교리 대립을 일심으로 수렴시켜 조화 — **정확**
- original_text: "一心을 체(體)로 삼아 萬法을 회통한다" (대승기신론소) — **정확**, 원효 사상의 핵심 문구
- work_id: wonhyo-geumgangsaemaerongnon — **주의**: 화쟁 사상은 금강삼매경론에서 체계적으로 전개되었으나, 십문화쟁론(十門和諍論)이 화쟁의 대표 저술. 금강삼매경론을 연결한 것은 부분적으로 타당
- source_detail: "금강삼매경론, 서문 및 본론; 십문화쟁론" — 십문화쟁론 언급 포함하여 적절
- 판정: **OK**

#### wonhyo-claim-002: 일심(一心)
- claim: 일심은 진여문과 생멸문의 공통 근거 — **정확**
- original_text: "是心攝一切世間法出世間法" (마명, 대승기신론, 원효가 주석) — **정확**, 대승기신론 원문
- work_id: wonhyo-daesunggisinnonso — **정확**
- argument: 본각·불각·시각 개념을 통한 논증 — **정확**, 대승기신론소의 핵심 구조
- 판정: **OK**

#### wonhyo-claim-003: 무애행(無礙行)
- claim: 승려 격식에 얽매이지 않고 민중 교화 — **정확**
- original_text: "일체 무애인(一切無礙人), 일도출생사(一道出生死)" (무애가 구절, 삼국유사 인용) — **정확**, 삼국유사 권4에 기록된 유명한 구절
- work_id: wonhyo-geumgangsaemaerongnon — **부적합하지만 이해 가능**: 무애행은 저서라기보다 실천이므로 특정 저서 연결이 어려움. 금강삼매경론을 연결한 것은 편의상 선택
- source_detail: "무애가 실천, 원효전 (삼국유사 권4)" — **정확**
- 판정: **OK**

### 혜능 claims (3건)

#### huineng-claim-001: 돈오(頓悟)
- claim: 점수 없이 단번에 자성 깨달음 — **정확**
- original_text: "本來無一物，何處惹塵埃" — **정확**, 육조단경 행유품의 혜능 게송
- 신수 게송 비교: "身是菩提樹，心如明鏡臺，時時勤拂拭，莫使惹塵埃" — explanation에 정확히 기술
- 판정: **OK**

#### huineng-claim-002: 견성성불(見性成佛)
- claim: 자성을 직접 봄으로써 곧 부처 — **정확**
- original_text: "自性若悟，眾生是佛；自性若迷，佛是眾生。" — **정확**, 육조단경 원문
- source_detail: "육조단경, 반야품 제2; 선정혜 품(定慧品) 제4" — **정확**
- 판정: **OK**

#### huineng-claim-003: 무념(無念)
- claim: 경계에 물들지 않는 마음, 생각 자체를 없애는 것이 아님 — **정확**, 중요한 구분
- original_text: "於諸境上心不染曰無念。" — **정확**, 육조단경 정혜품 원문
- 무주·무상과 함께 수행 3원리 — **정확**
- 판정: **OK**

---

## 4. ethics-keywords 검증 (6건)

| ID | term | 한자 | 판정 |
|----|------|------|------|
| wonhyo-kw-hwajae | 화쟁 | 和諍 | OK |
| wonhyo-kw-ilsim | 일심 | 一心 | OK |
| wonhyo-kw-muae | 무애 | 無礙 | OK |
| huineng-kw-dono | 돈오 | 頓悟 | OK |
| huineng-kw-gyeonseong-seongbul | 견성성불 | 見性成佛 | OK |
| huineng-kw-munyeom | 무념 | 無念 | OK |

- 모든 definition이 정확하고 충분한 설명을 포함함.
- related_terms 연결도 적절함.

---

## 5. ethics-relations 검증

### huineng-rel-001: buddha → huineng (influenced)
- 의미: "붓다가 혜능에게 영향을 주었다"
- evidence: 금강경 청문 후 깨달음
- 판정: **OK** — 방향 정확, 내용 정확

### wonhyo-rel-001: wonhyo → uisang (influenced)
- 의미: "원효가 의상에게 영향을 주었다"
- evidence: 삼국유사 원효전·의상전, 대승기신론소와 화엄 사상 연관
- 판정: **OK** — 방향 정확. 두 사람은 상호 영향 관계이나 원효→의상 방향도 타당

### buddha-rel-002: buddha → wonhyo (influenced)
- 의미: "붓다가 원효에게 영향을 주었다"
- 판정: **OK** — 기존 데이터, 정확

### huineng-rel-002: huineng → wonhyo (influenced) — **이슈**
- 의미: "혜능이 원효에게 영향을 주었다"
- **문제**: 원효(617~686)는 혜능(638~713)보다 먼저 태어나고 먼저 사망했다. 혜능이 육조로 인가받은 것은 원효 생존 후반기이지만, 혜능의 사상이 널리 알려진 것은 원효 사후이다. 따라서 "혜능이 원효에게 영향을 주었다"는 역사적으로 **성립하기 어렵다**.
- description에는 "직접적 교류의 역사적 기록은 없다"고 명시하면서도 influenced 관계를 설정한 것이 모순적이다.
- **권고**: 이 관계를 삭제하거나, 방향을 뒤집어 wonhyo → huineng 으로 변경하되 type을 "parallel" 또는 description을 "동시대 동아시아 불교의 병렬적 사상 흐름"으로 수정하는 것이 적절하다. 혹은, 후대 연구에서 비교 연구가 이루어졌다는 맥락이므로 아예 삭제하는 것이 가장 깔끔하다.
- **심각도**: 중 — 학술적 사실 관계 오류

---

## 6. 스키마 준수 검증

| 항목 | 판정 |
|------|------|
| 모든 claims에 verified: false | OK |
| 모든 claims에 verification_log: [] | OK |
| claims 필수 필드 (claim, original_text, explanation, argument, counterpoint, context, keywords) | OK — 모두 포함 |
| thinkers에 philosophical_journey 포함 | OK |
| relations 방향 규칙 "from [type] to" | OK (huineng-rel-002 제외) |

---

## 이슈 목록

### 이슈 1 (중): huineng-rel-002 방향/타당성 오류
- **문서**: ethics-relations, ID: huineng-rel-002
- **내용**: huineng → wonhyo (influenced)는 시간적으로 성립 불가. 원효가 혜능보다 먼저 활동·사망했으므로 혜능이 원효에게 영향을 줄 수 없다.
- **권고**: 해당 relation 삭제 권고. 두 사상가의 사상적 유사성은 별도의 비교 연구 영역이지 influenced 관계가 아님.

### 이슈 2 (하): 원효 이름 한자 표기
- **문서**: ethics-thinkers, ID: wonhyo
- **내용**: name 필드에 "원효 (元曉)"로 표기되어 있다. 원효의 한자 이름으로 "元曉"가 널리 쓰이지만, 정확한 표기는 법명(法名)이 "元曉"이다. 다만 일부 자료에서 "元曉"는 시호이며 법명은 다르다는 주장도 있으나, 통설상 "元曉"는 수용 가능하다.
- **판정**: 현행 유지 가능 (참고 사항)

---

## 종합 판정

- **thinkers**: 2/2 OK
- **works**: 4/4 OK
- **claims**: 6/6 OK (내용 정확, 원문 정합)
- **keywords**: 6/6 OK
- **relations**: 3/4 OK, 1건 이슈 (huineng-rel-002)
- **스키마 준수**: OK

**전체 판정: PASS (이슈 1건 수정 권고)**

핵심 검증 포인트인 원효-화쟁·일심·무애행, 혜능-돈오·견성성불·무념은 모두 정확하게 입력되어 있다. 한문 원문도 정확하다. 생몰년도 정확하다. relations에서 huineng-rel-002만 수정/삭제가 필요하다.
