---
agent: tester
task_id: TASK-078
status: DONE
timestamp: 2026-04-13T15:30:00
---

## 결과 요약

이황(퇴계) 데이터 전수 검증 완료.
- thinker 1건, works 4건, claims 12건, keywords 11건, relations 4건 조회 확인
- 이슈: 심각 1건, 보통 2건, 경미 2건

## 1. ethics-thinkers 검증

**yihwang** — 이황 (李滉, 퇴계)

| 항목 | 검증 결과 |
|------|-----------|
| name | 이황 (李滉, 퇴계) — 정확 |
| name_en | Yi Hwang (Toegye) — 정확 |
| field | eastern_ethics — 정확 |
| era | 조선 — 정확 |
| birth_year | 1501 — 정확 |
| death_year | 1570 — 정확 |
| background | 예안 출신, 34세 문과 급제, 도산서당 1561년, 성학십도 1568년 진상, 영남학파 종조 — 모두 정확 |
| core_philosophy | 이기호발설, 주리론, 이선기후, 경 수양론, 미발함양·이발성찰 — 정확하게 요약됨 |
| philosophical_journey | 초기·중기·말기 3단계 구분 적절. 사서집주·근사록 탐구, 천명도 수정(1553경), 사단칠정 논쟁(1559~1566), 도산서당(1561), 성학십도 진상(1568) — 정확 |
| keywords | 12개 키워드 적절 |

**판정**: 정확

## 2. ethics-works 검증

### yihwang-seonghak-sipdo (성학십도, 1568)
- title_original: 聖學十圖 (Ten Diagrams on Sage Learning) — 정확
- year: 1568 — 정확 (선조 원년)
- significance: 선조에게 진상, 10개 도설 나열 — 정확
- 10개 도설 순서: 태극도→서명도→소학도→대학도→백록동규도→심통성정도→인설도→심학도→경재잠도→숙흥야매잠도 — **정확** (표준 순서와 일치)
- key_concepts: 적절

### yihwang-toegye-jeonse (퇴계전서)
- title_original: 退溪全書 — 정확
- year: null — 적절 (사후 편찬 문집)
- significance: 기대승과의 서한 수록 언급 — 정확
- key_concepts: 적절

### yihwang-jaseongnok (자성록)
- title_original: 自省錄 — 정확
- significance: 수양 실천 기록, 거경(居敬) — 정확
- key_concepts: 적절

### yihwang-cheonmyeongdosol (천명도설/천명신도, 1553)
- title_original: 天命圖說 / 天命新圖 — 정확
- year: 1553 — 정확 (학계 통설과 부합)
- significance: 정지운 천명구도 → 천명신도 수정 — 정확
- key_concepts: 적절

**판정**: 정확

## 3. ethics-claims 검증

### claim-001: 이기호발설 (理氣互發說)
- **원문**: "四端之發 純理故無不善 七情之發 兼氣故有善惡 … 理發而氣隨之 氣發而理乘之" — **정확**. 퇴계전서 사단칠정서의 핵심 구절.
- **한국어 번역**: 정확
- **논증 구조**: (1)이기불상잡 → (2)사단=본연지성 발현 → (3)칠정=형기 감촉 발현 → (4)발원처 구분 — 논리적으로 적절
- **counterpoint**: 이이의 기발이승일도설(氣發理乘一途說) — 정확. 출처 "성학집요·답성호원" 적절.
- **context**: 기대승과의 논쟁 1559~1566 — 정확
- work_id: yihwang-toegye-jeonse — 적절 (사단칠정서가 퇴계전서에 수록)

### claim-002: 사단순선·칠정선악
- 원문: "四端 理之發 七情 氣之發 四端無不善 七情有善惡" — 정확
- claim-001과 내용이 겹치지만 강조점(도덕적 자각 근거)이 다름 — 허용 범위
- counterpoint: 이이 + 기대승 언급 — 적절

### claim-003: 이(理)의 능동성
- 원문: "理有動靜 故氣有動靜 若理無動靜 氣何自而有動靜乎" — **정확**. 퇴계의 이동정(理動靜) 논의의 핵심 구절.
- counterpoint: 이이의 이무위(理無爲) — 정확

### claim-004: 경(敬) 중심 수양론
- 원문: "敬者 聖學之所以成始成終者也 … 主一無適之謂敬" — **정확**. 주일무적은 정이(程頤)의 경 정의로 이황이 계승한 것.
- 미발함양·이발성찰 구조 — 정확
- work_id: yihwang-seonghak-sipdo — 적절 (제9도 경재잠도)
- counterpoint: 왕양명의 치양지 — 적절

### claim-005: 성학십도 체계
- 10개 도설 순서 — **정확** (위 works 검증과 일치)
- 전반부(1~5도) 우주론·존재론, 후반부(6~10도) 심성론·수양론 구분 — 적절
- "6도(심통성정도)는 이황이 독자적으로 작성한 도설" — **정확**
- counterpoint: 왕양명 — 적절

### claim-006: 이선기후(理先氣後)
- 원문: "有是理然後有是氣 理先氣後 非謂時間之先後也" — **정확**
- counterpoint: 이이의 이기무선후(理氣無先後) — 정확

### claim-007: 이기불상잡(理氣不相雜)
- 원문: "理氣不相雜 亦不相離 不相雜者 理自理 氣自氣 各有其分也" — **정확**
- 이황=불상잡 강조 vs 이이=불상리 강조 대비 — 정확
- counterpoint: 이이의 답성호원 — 적절

### claim-008: 심통성정(心統性情)
- 원문: "心統性情 性是心之體 情是心之用" — 정확
- "장재(張載)가 제시하고 주희가 계승" — **정확**
- "세 개의 심통성정도(천명도·성정도·체용도)" — **보통 이슈**. 성학십도 제6도의 3개 하위 도설의 명칭이 "천명도·성정도·체용도"로 표기되어 있으나, 학계에서 일반적으로 사용하는 명칭은 "중도(中圖)를 중심으로 한 3개 도설" 혹은 단순히 "심통성정도의 세 그림"이다. 다만 이황 자신이 이 세 도설에 구체적 이름을 부여한 문헌 근거가 명확하지 않아, "천명도·성정도·체용도"라는 명칭의 출처가 불분명하다. 내용 자체(3개 도설로 구성)는 맞으나 개별 도설 명칭은 부정확할 수 있다.

### claim-009: 천명도 개정
- 정지운 천명구도 → 천명신도 수정 — **정확**
- "사단을 이(理)에, 칠정을 기(氣)에 각각 연결하는 수정" — 정확
- 1553년경 — 정확
- counterpoint: 기대승의 비판 — 적절

### claim-010: 주리론(主理論)
- 영남학파의 핵심 입장 — 정확
- counterpoint: 이이의 주기론(주기론), 기호학파 — 정확

### claim-011: 본연지성·기질지성과 변화기질
- "주희의 성론을 계승" — 정확
- 변화기질(變化氣質)을 통한 본연지성 회복 — 정확
- counterpoint: 왕양명의 심즉리, 양지 직접 발현 — 적절

### claim-012: 군주 성학론
- 성학십도 서문(진성학십도차) 내용 — 정확
- "心正則萬化出 心邪則萬化亦邪" — 유교적 정치론의 표준 표현
- counterpoint: 한비자의 법·술·세 — 적절하지만 다소 거리가 있는 대비. 이이의 성학집요가 더 직접적인 대비가 될 수 있으나 이이는 계승 관계이므로 한비자와의 대비도 허용 범위.

**판정**: 학술적으로 정확. claim-008의 심통성정도 하위 명칭에 경미한 이슈 있음.

## 4. ethics-keywords 검증

### 스키마 이슈 (보통)
기존 사상가(소크라테스 등)의 keywords는 architecture.md 스키마대로 `term_en`, `work_id`, `related_terms` 필드를 사용한다. 그러나 이황의 keywords는 이 필드들 대신 `term_original`, `related_claims`, `source` 필드를 사용하고 있다.

| 스키마 필드 | 기존 사상가 | 이황 | 비고 |
|-------------|-------------|------|------|
| term_en | 있음 | **없음** | term_original로 대체 |
| work_id | 있음 | **없음** | source로 대체 |
| related_terms | 있음 | **없음** | related_claims로 대체 |
| term_original | 없음 | 있음 | 비표준 필드 |
| related_claims | 없음 | 있음 | 비표준 필드 |
| source | 없음 | 있음 | 비표준 필드 |

이 불일치는 검색 및 CLI 기능에 영향을 줄 수 있다.

### 내용 검증

| ID | term | 내용 정확성 |
|----|------|------------|
| kw-001 | 이기호발설 | 정확. 이이의 기발이승일도설과의 대비 정확. |
| kw-002 | 사단칠정 | 정확. 사단 4가지(측은·수오·사양·시비), 칠정 7가지(희·노·애·구·애·오·욕) 정확. |
| kw-003 | 경(敬) | 정확. 주일무적, 거경함양, 미발/이발 구분 정확. |
| kw-004 | 성학십도 | 정확. 10도 순서 정확. |
| kw-005 | 이선기후 | 정확. 所以然之故(존재 근거) 설명 적절. |
| kw-006 | 이기불상잡 | 정확. 이이의 불상리 강조와 대비 정확. |
| kw-007 | 심통성정 | 정확. 장재 → 주희 → 이황 계승 정확. |
| kw-008 | 주리론 | 정확. 기호학파 주기론과의 대립 정확. |
| kw-009 | 미발함양 이발성찰 | 정확. |
| kw-010 | 영남학파 | 정확. 대표 학자 유성룡·김성일·정구 정확. |
| kw-011 | 본연지성·기질지성 | 정확. |

**판정**: 내용은 정확하나 스키마 불일치(보통 이슈) 있음.

## 5. ethics-relations 검증

### relation-zhuxi-yihwang
- from: zhuxi → to: yihwang, type: influenced
- 의미: "주희가 이황에게 영향을 주었다" — **정확**
- description: 주희 성리학 계승, 이기호발설 전개, 주자서절요 편찬 — 정확

### relation-wangyangming-yihwang (**심각 이슈**)
- from: wangyangming → to: yihwang, type: criticized
- 의미: "왕양명이 이황을 비판했다" — **부정확**. 실제로는 이황이 왕양명을 비판한 것이다.
- 데이터 자체의 note 필드에도 방향 오류를 인정하는 내용이 있음: "방향: wangyangming criticized yihwang은 정확히는 이황이 왕양명을 비판한 것. 관계 방향 재확인 필요"
- **별도로 relation-yihwang-wangyangming (from: yihwang → to: wangyangming, type: criticized)이 존재**하므로 정확한 방향의 관계는 이미 있음.
- **결론**: relation-wangyangming-yihwang은 방향이 틀렸고, relation-yihwang-wangyangming과 중복이다. 삭제해야 한다. (왕양명은 이황보다 먼저 사망했고 이황을 알지 못했으므로 왕양명→이황 방향의 criticized 관계는 역사적으로 성립 불가)

### relation-yihwang-wangyangming
- from: yihwang → to: wangyangming, type: criticized
- 의미: "이황이 왕양명을 비판했다" — **정확**
- description: 심즉리 비판, 지행합일 비판, 선지후행 강조 — 정확

### relation-yihwang-yiyulgok-debate
- from: yihwang → to: yiyulgok, type: influenced
- 의미: "이황이 이이(율곡)에게 영향을 주었다" — **부분적으로 정확**
- description: 이이가 이황의 이기호발설을 비판하여 기발이승일도설을 정립, 영남학파 vs 기호학파 형성 — 정확
- type이 "influenced"인데 description은 비판적 계승(debate) 성격이 강함. 그러나 이이가 이황의 사상에 대한 비판적 응답으로 자기 사상을 형성했으므로 "influenced"도 허용 범위. 이황→이이 방향으로 사상적 영향을 준 것은 사실이다.
- **경미 이슈**: ID가 "relation-yihwang-yiyulgok-debate"로 debate를 표시하고 있으나 type은 influenced. 의미상 혼동 가능하나 실질적으로 "이황의 사상이 이이의 사상 형성에 결정적 영향을 미쳤다"는 점에서 influenced는 맞음.

**판정**: relation-wangyangming-yihwang 방향 오류(심각). 삭제 필요.

## 이슈 목록

### 심각 (1건)

**ISSUE-078-01**: relation-wangyangming-yihwang 방향 오류 및 중복
- 위치: ethics-relations / relation-wangyangming-yihwang
- 문제: from: wangyangming → to: yihwang, type: criticized는 "왕양명이 이황을 비판했다"는 뜻이나, 실제로는 이황이 왕양명을 비판한 것이다. 왕양명(1472~1529)은 이황(1501~1570)보다 먼저 세상을 떠났으며 이황의 존재를 알지 못했다.
- 또한 정확한 방향의 relation-yihwang-wangyangming이 이미 존재하므로 중복이다.
- 수정: relation-wangyangming-yihwang 삭제

### 보통 (2건)

**ISSUE-078-02**: keywords 스키마 불일치
- 위치: ethics-keywords / yihwang-kw-001 ~ kw-011 (전체 11건)
- 문제: architecture.md에 정의된 스키마(term_en, work_id, related_terms)를 사용하지 않고, 비표준 필드(term_original, related_claims, source)를 사용
- 기존 사상가(소크라테스, 플라톤 등)의 keywords와 필드 구조가 다름
- 영향: CLI 검색 기능에서 term_en, work_id, related_terms 기반 쿼리가 이황 키워드에 적용되지 않을 수 있음
- 수정: 11건 모두 스키마에 맞게 필드 변환 필요 (term_original → term_en으로 매핑, source → work_id로 매핑, related_claims → related_terms로 매핑)

**ISSUE-078-03**: claim-008 심통성정도 하위 도설 명칭
- 위치: ethics-claims / yihwang-claim-008 explanation
- 문제: "세 개의 심통성정도(천명도·성정도·체용도)"로 표기되어 있으나, 이 개별 명칭은 학계 표준 명칭이 아님. 일반적으로 "3개 도설" 또는 주희의 원도를 기반으로 한 상도/중도/하도 등으로 지칭됨.
- 수정: "세 개의 심통성정도"로만 서술하거나, 학계에서 사용되는 명칭을 확인하여 수정

### 경미 (2건)

**ISSUE-078-04**: claim-001과 claim-002의 내용 중복
- 위치: ethics-claims / yihwang-claim-001, yihwang-claim-002
- 문제: claim-001(이기호발설)과 claim-002(사단순선·칠정선악)는 내용이 상당 부분 겹친다. 두 claim 모두 "사단=이발=순선, 칠정=기발=선악"을 설명한다.
- 수정: 허용 범위이나, claim-002의 강조점(도덕적 자각의 근거)을 더 차별화하면 좋겠음

**ISSUE-078-05**: relation-yihwang-yiyulgok-debate의 ID와 type 불일치
- 위치: ethics-relations / relation-yihwang-yiyulgok-debate
- 문제: ID에 "debate"가 포함되어 있으나 type은 "influenced". 실질적으로 influenced가 맞으나 ID 명명이 혼동을 줄 수 있음.
- 수정: 경미. 필요 시 ID를 relation-yihwang-yiyulgok로 변경하거나 현행 유지 가능.

## 종합 판정

이황(퇴계) 데이터의 **학술적 정확성은 전반적으로 우수**하다.

- 이기호발설의 핵심 원문("理發而氣隨之, 氣發而理乘之")이 정확하게 입력됨
- 사단칠정 논쟁에서 기대승·이이와의 대비가 정확하게 기술됨
- 성학십도 10개 도설의 순서와 구성이 정확함
- 경(敬) 수양론의 미발함양·이발성찰 체계가 정확함
- 주희 성리학 계승 관계가 정확함
- 천명도 개정(천명구도 → 천명신도)이 정확함
- counterpoint(반론)에서 이이·왕양명의 저서가 구체적으로 적시됨

**수정 필요 사항**: 심각 이슈 1건(relation 방향 오류 삭제), 보통 이슈 2건(keywords 스키마 통일, claim-008 명칭 수정)
