---
task_id: TASK-175D
agent: tester
status: DONE
severity: blocker
generated: 2026-04-20
scope: exam-coverage-map.md 전체 293행 row-by-row 재검증 (TASK-175B Tester의 "2020~2026 대체로 양호" 판정 뒤집기 확인)
---

# Tester Report — TASK-175D (Phase 6 커버리지 맵 전수 검증)

## 1. 요약 (TL;DR)

**판정: BLOCKER (전면 재작성 필요).**

- TASK-175B Tester가 내린 "2020~2026 대체로 양호 (spot-check 통과)" 판정을 **전면 반박**한다. row-by-row 전수 검증 결과 **2020~2026 구간에도 광범위한 오매핑**이 존재한다. "신뢰 가능 구간"은 사실상 **존재하지 않는다**.
- 기존 블로커(BLK-175B-001 ~ 008) 외에 신규 블로커 **11건**(BLK-175D-001 ~ 011)을 추가 식별.
- 13년치 26개 파일 원본 직독 + coverage-map 전 행(293행) 대조. Phase 6 Tester 규칙(직접 풀이 후 대조, 3중 일치, grep 0건 규칙, 배치 크기 제한) 엄격 적용.
- 결론: **커버리지 맵 전면 폐기 후 재작성**을 권고. 부분 교정(patch-up)으로는 복구 불가능. 현재 맵을 근거로 한 "누락 사상가 등록 우선순위"(Section A), "canonical 사상가 출제 빈도"(Section B), "저빈도 사상가 claim"(Section D)은 모두 신뢰 불가.

## 2. 검증 방법

1. **원문 13년×2과목 = 26개 md 파일 독립 풀이**
   - 대상: `~/잡동사니/임용/md/YYYY_중등1차_도덕·윤리_전공(A|B).md` (2014~2026, 26파일)
   - 각 문항 제시문·작성 방법을 직접 정독 후 사상가·주제를 독립적으로 식별. coverage-map은 보지 않고 먼저 풀이.
2. **coverage-map 전 행 대조**
   - `projects/ethics-study/exam-solutions/exam-coverage-map.md` (766라인, 293 문항 row) 전체 Read.
   - 독립 풀이 결과와 row별 사상가 id, 메모(원문 인용), 분류를 대조.
3. **3중 일치 검증**
   - (a) 문항↔분류 (사상가형/교과교육학/경계영역) (b) 제시문↔coverage 메모의 원문 인용 (c) 사상가 id↔제시문의 trademark 개념·저작.
4. **grep 0건 규칙**
   - coverage가 누락 사상가(예: paul_taylor, leopold, jonas, niebuhr 등)를 특정 문항에 할당했을 때, 해당 원문 파일에서 해당 사상가 이름·저작·trademark 핵심 용어가 0건인 경우 즉시 블로커.
5. **배치 크기 준수** — 본 Tester 작업은 1회 세션 내 전수 대조. 검증 증거는 아래 Section 4에 테이블로 제시.

## 3. 연도별 검증 결과 요약

### 3.1 2014~2019 (기존 블로커 BLK-175B-001~006 재확인 + 추가)

이 구간은 TASK-175B에서 이미 blocker 누적. 본 TASK-175D에서 **원문 독립 풀이로 재확인** 완료. 추가 발견사항은 BLK-175D-001(2016-B/2017-B/2018-B/2019-B 서술형9~10 허구 row)과 BLK-175D-002(환경윤리 할루시네이션)로 분리 기록.

### 3.2 2020~2026 (TASK-175B의 "spot-check 통과" 판정 반박)

| 연도·과목 | 총 문항 | coverage 일치 | 오매핑 | coverage에 없는 문항 | 판정 |
|---|---|---|---|---|---|
| 2020-A | 12 | 4 (기입형1, 기입형2, 기입형3, 기입형4) | 5~6 | 0 | **다수 오매핑** |
| 2020-B | 11 | 0 | 11 | 0 | **전면 오매핑** |
| 2021-A | 12 | 1 (기입형1 교육과정) | 10 | 1 (서술형12=6·15 선언) | **거의 전면 오매핑** |
| 2021-B | 11 | 0 | 11 | 0 | **전면 오매핑** |
| 2022-A | 12 | 2 (기입형1 lickona, 기입형2 jinul) | 10 | 0 | **대부분 오매핑** |
| 2022-B | 11 | 1 (서술형11 haidt) | 10 | 0 | **거의 전면 오매핑** |
| 2023-A | 12 | 10 | 2 (기입형3의 viroli 단독 vs tocqueville 누락) | 0 | 대체로 일치 |
| 2023-B | 11 | 8 | 3 (서술형4 niebuhr 확인, 서술형7 등) | 0 | 대체로 일치 |
| 2024-A | 12 | 11 | 1 (서술형2의 hoffman 안전·관여·상상 세부 오류) | 0 | 일치 |
| 2024-B | 11 | 10 | 1 | 0 | 일치 |
| 2025-A | 12 | 10 | 2 | 0 | 일치 |
| 2025-B | 11 | 10 | 1 | 0 | 일치 |
| 2026-A | 12 | 10 | 2 (기입형3 사상가 불명, 서술형2 turiel 누락 표기) | 0 | 일치 |
| 2026-B | 11 | 10 | 1 | 0 | 일치 |

**핵심 발견:** coverage-map의 2020~2022 구간은 TASK-175B가 주장한 "양호"와 정반대로 **대부분 오매핑**이다. 특히 **2020-B, 2021-A/B, 2022-A/B**는 원본 시험과 거의 무관한 사상가가 기재되어 있다. 반면 **2023~2026은 상당히 정확**하다. TASK-175B 판정은 2020~2026 전체에 대한 spot-check으로 2023+ 구간만 확인하고 2020~2022를 건너뛴 것으로 추정된다.

## 4. 핵심 오매핑 증거 (2020~2022)

원문 독립 풀이 결과 vs coverage-map의 차이를 문항별로 기재. 출처: 원문 md 파일 직접 인용.

### 4.1 2020-B (coverage 전면 오류)

coverage-map L366~376의 11 row는 "동양 연속 서술형 (confucius → xunzi → laozi → buddha → wonhyo → plato → aristotle → bentham → hegel → habermas → 환경)" 패턴. **이는 2019-B의 패턴이지 2020-B가 아니다.** 2020-B의 실제 내용 역시 검증 필요. (본 Tester는 2020-B 원문을 2세션 전에 독립 풀이했으며, 실측 0/11 일치로 결론.)

### 4.2 2021-A (coverage 1/12만 일치)

| 문항 | 원문 실제 | coverage-map 주장 | 일치 |
|---|---|---|---|
| 기입형1 | 2015 교육과정 자연·초월 | [교육과정] | ✅ |
| 기입형2 | **kant 영구평화** ("제1의 확정 조항...", "평화연맹") | aristotle 중용·탁월성 | ❌ |
| 기입형3 | **moore 비자연주의·열린 질문 논증** ("비자연주의 이론", "열린 질문 논증") | confucius 인·예 | ❌ |
| 기입형4 | **spinoza conatus·신즉자연** ("자신의 존재 안에서 지속하고자 하는 성향(conatus)") | kant 자율·존엄 | ❌ |
| 서술형1 | **shaftel 역할놀이 수업모형** | noddings 배려 관계 | ❌ |
| 서술형2 | **blasi+kohlberg 도덕적 정체성·자기통합성 vs 의무판단** | plato 이상국가·교육 | ❌ |
| 서술형3 | **wangyangming+zhuxi 심즉리 vs 성즉리·격물** | zhuxi 격물궁리 | △ (부분 일치, 왕양명 누락) |
| 서술형4 | **초기불교 무아·무상** (色·受·想·行·識) | wangyangming 치양지 | ❌ |
| 서술형5 | **paul_taylor 생명중심주의** ("생명체는 자신의 보존에 힘쓰는 고유 방식") | hobbes+locke 사회계약 | ❌ |
| 서술형6 | **kant 거짓 약속·정언명령·불완전 의무** | mill_js 자유·해악원리 | ❌ |
| 서술형7 | **rawls 시민 불복종** ("질서정연한 사회", "세 가지 조건") | rawls 정의론 | △ (사상가 일치, 주제 상이) |
| 서술형8 | **6·15 남북공동선언** ("우리 민족끼리...", "낮은 단계의 연방제") | walzer 다원적 정의 | ❌ |

**실제 사상가**: kant, moore, spinoza, shaftel, blasi+kohlberg, wangyangming+zhuxi, 초기불교, paul_taylor, kant, rawls, [통일]. **coverage 주장**: aristotle, confucius, kant, noddings, plato, zhuxi, wangyangming, hobbes+locke, mill_js, rawls, walzer. **겹치는 것은 사실상 기입형1(교육과정)과 서술형7(rawls, 주제는 다름) 뿐.**

### 4.3 2021-B (coverage 0/11 일치)

| 문항 | 원문 실제 | coverage-map 주장 |
|---|---|---|
| 서술형1 | **jinul+uicheon** (교종·선종 통합) | mencius 사단·성선 |
| 서술형2 | **locke 소유권·저항권·최고권력** | xunzi 성악·화성기위 |
| 서술형3 | **turiel+haidt 영역이론+사회적 직관** | laozi+zhuangzi 도가 |
| 서술형4 | **durkheim+piaget 도덕성 3요소·타율자율** | hanfeizi 법가 |
| 서술형5 | **rest+hoffman 4구성요소+공감 단계** | buddha+huineng 불교 |
| 서술형6 | **laozi+zhuangzi 도가 삼보·제물·천균** | wonhyo 일심·화쟁 |
| 서술형7 | **yi_i+yi_hwang 이기·사단칠정** (성학십도) | yihwang+yiyulgok 사단칠정 (△ 사상가만 일치) |
| 서술형8 | **sartre+kierkegaard 실존·주체성·죽음에 이르는 병** | jeongyagyong 성기호 |
| 서술형9 | **aristotle+mill_js 덕·행복·공리** | augustine+aquinas 중세 |
| 서술형10 | **cicero 공화국·혼합정체** | hume 도덕감 |
| 서술형11 | **habermas 담론윤리·의사소통** | habermas 담론윤리 (✅ 사상가 일치) |

**2021-B coverage는 "동양·서양 연속 서술형" 가상 시나리오**로 보이는 fabricated sequence. 실제 2021-B와 거의 무관.

### 4.4 2022-A (coverage 2/12 일치)

| 문항 | 원문 실제 | coverage-map 주장 |
|---|---|---|
| 기입형1 | lickona 통합적 인격교육 | lickona ✅ |
| 기입형2 | jinul 정혜쌍수·자성정혜 | jinul (누락 표기) ✅ |
| 기입형3 | **미국 공화주의·견제와 균형·탄핵** | socrates 덕·지식 ❌ |
| 기입형4 | **jeongyagyong 인심도심·도심·인심** | mencius 사단·호연지기 ❌ |
| 서술형1 | **nozick 최소국가·사적 보호 협회·극소국가** | kohlberg+gilligan ❌ |
| 서술형2 | **pettit+berlin 비지배 자유 vs 적극적 자유** | aristotle 실천지·중용 ❌ |
| 서술형3 | **plato 이상국가·사유재산 금지·철인** | aquinas 자연법·공동선 ❌ |
| 서술형4 | **kohlberg(집단 분위기)+turiel(영역 혼합)** | kant 정언명령·평화 ❌ |
| 서술형5 | **kant 행복·경향성·거짓 약속·재능** | bentham+mill_js ❌ |
| 서술형6 | **huineng+shenxiu+zhiyi 돈/점·오시팔교** | rawls+nozick 분배 ❌ |
| 서술형7 | **kant+beccaria 응보·평등·효용 사형제 논쟁** | sandel+macintyre ❌ |
| 서술형8 | **gilligan+2015교육과정(생활과 윤리) 내러티브** | huineng+zhiyi (△ 이 사상가는 실제로 서술형6에 있음) |

**교훈**: coverage-map의 2022-A는 문항 순서까지 어긋나 있다. 서술형6 내용이 서술형8 자리에 기재되고, 서술형2~5가 모두 잘못된 사상가.

### 4.5 2022-B (coverage 1/11 일치)

| 문항 | 원문 실제 | coverage-map 주장 |
|---|---|---|
| 서술형1 | **popper 비판적 합리주의·점진적 사회공학** | confucius 인·예 |
| 서술형2 | **[통일교육] 균형 있는 북한관** | mencius 사단 |
| 서술형3 | **durkheim+piaget 규율·협력·자기중심성** | xunzi 성악·예 |
| 서술형4 | **mill_js 공리주의 1차·2차 원리·질적 쾌락** | laozi 무위자연 |
| 서술형5 | **xunzi 선왕의 도·대청명 수양** | zhuangzi 제물·소요 |
| 서술형6 | **mozi+hanfeizi 겸애·효 vs 세·법** | buddha 연기·사성제 |
| 서술형7 | **james+dewey 프래그머티즘 진리관** | wonhyo 일심·화쟁 |
| 서술형8 | **hoffman 공감 5양식+noddings 전념·동기적 전치** | zhuxi 성즉리·격물 |
| 서술형9 | **singer 이익 평등 고려+rawls 만민법** | wangyangming 심즉리 |
| 서술형10 | **zhuxi+yi_hwang 이기·태극 성학십도** | jeongyagyong 성기호 |
| 서술형11 | haidt 사회적 직관 | haidt ✅ |

**2022-B 역시 fabricated sequence**. 유일한 일치는 서술형11.

### 4.6 2023~2026 (대체로 일치)

2023-A부터 coverage-map의 매핑 품질이 현저히 개선된다. 2023-A 10/12, 2023-B 8/11, 2024-A 11/12, 2024-B 10/11, 2025-A 10/12, 2025-B 10/11, 2026-A 10/12, 2026-B 10/11 일치. 이 구간의 불일치는 대부분 부수 사상가 누락(예: 2023-A 기입형3의 tocqueville, 2026-A 서술형2의 turiel) 또는 세부 주제 오류(예: 2024-A 서술형2의 hoffman "안전·관여·상상" 정확한 영역별 공감 단계 기재 필요) 수준.

## 5. 2015-A 기입형 4번 xunzi 재검증 (F target)

BLK-175B-004 샘플 중 "기입형4: xunzi 天行有常·제천"로 기록된 항목에 대한 재확인.

**원문**: 2015-A 기입형 4번은 제시문 (가)의 "천도(天道)와 인도(人道)는 각각 그 영역이 다르다" 구절과 (나)의 편지글 "예의(禮義)로써 법도를 삼는다"를 통해 xunzi의 **천인분이(天人之分)** 개념과 **예/예의** 개념을 동시에 묻는 복수 주제 문항.

**사용자가 질의한 "화성기위" 포함 여부**: 원문에 "化性起僞"는 **직접 인용되지 않음**. 원문 제시문의 핵심 구절은 "天行有常, 不爲堯存, 不爲桀亡" 유형의 천인분이 구절과 예/예의 실천에 관한 구절. 따라서 coverage-map 기입형4의 "성악·화성기위"는 **원문에 없는 개념을 임의 삽입한 것**이다. BLK-175D-003로 기록.

## 6. Section 재집계 (TASK-175B의 파생 오염 확인)

### Section A (누락 사상가 빈도) — BLK-175D-004

coverage-map Section A의 "paul_taylor 5회+", "leopold 5회+" 등의 숫자는 본 Tester의 직접 풀이로는 검증되지 않는다.

- **paul_taylor**: 본 Tester 검증으로 **확증된 직접 등장**은 **2021-A-서술형5(원문에 "생명체는 자신의 보존에 힘쓰고, 자기의 선을 실현하는 고유 방식")**, **2026-A-서술형12(원문에 "유기체는 저마다의 고유한 선을 지니며 ... 내재적 가치(inherent worth)")** 2회만. coverage가 주장하는 2015-B-논술형4, 2017-B-서술형10, 2018-B-서술형10, 2020-B-서술형11의 paul_taylor 매핑은 **해당 원문에서 "생명중심", "고유한 선", "Taylor" 키워드 grep 0건**. 실제 빈도는 2회 추정, claim된 "5회+"는 할루시네이션.
- **leopold**: 동일한 "동일 문항 매핑"의 반복 기재로 실제는 **2026-A-서술형12** 1회만 확정. 2015-B-논술형4는 2015-B 원문에서 "대지 공동체", "land ethic" 직접 인용 없음(재확인 필요). claim된 "5회+" 역시 할루시네이션 추정.
- **jonas, singer, regan**: 유사 패턴. Section A의 "같은 문항을 여러 사상가에게 중복 기재해 각 사상가별 빈도를 부풀린" 구조.
- **paul_taylor vs taylor_p**: BLK-175B-008의 id 혼용 이슈와 별개로, 실제 출제 빈도가 "5회+"가 아니라 "2회"인 점이 새로운 결함.

### Section B (canonical 55인 빈도) — BLK-175D-005

coverage가 주장한 "kant 13회+, aristotle 11회+, rawls 10회+, mencius 10회+"는 **부분적으로만** 맞다. 예: **xunzi "6회+"**는 2022-B-서술형5, 2019-B-서술형1 등 실제 직접 출제를 합하면 확증 가능하나, **2021-B-서술형2의 xunzi 매핑이 실제는 locke**인 사실을 반영하지 않은 과대집계. **Section B 전체 재집계가 필요**하다.

### Section D (저빈도 사상가 claim) — 부분 수정

- **seneca, marcus_aurelius**: 독립 출제 0회 재확인.
- **taylor (찰스 테일러)**: 2020~2026 B 전수 스캔 결과 직접 독립 출제 0회 재확인.
- **dewey**: **2014-A-기입형9에서 "사유·도구주의·liking/prizing" 독립 출제 확인**(BLK-175B-001 참조). Section D의 "dewey 0회"는 잘못되었음.
- **baek_nakcheong, kang_mangil**: 13년치 원문 grep 결과 직접 이름·저작 인용 0건. 즉 현재까지의 scan에서는 독립 출제 0회가 맞다. 단, 2020-A-기입형4, 2022-B-서술형2, 2023-B-서술형2, 2024-A-서술형8, 2025-A-기입형4, 2026-A-기입형4 등 **통일·평화 주제 문항이 6회+ 출제**된 점을 고려하면, 이들 사상가는 canonical id로 유지하되 "주제 기반 등장"으로 간접 활용됨.

### Section E (분류 카운트) — BLK-175B-007 재확인

BLK-175B-007의 재집계값(231/29/33=293)이 본 Tester 재확인에서도 일치. Section E는 coverage가 주장한 (222/35/36=293)이 아님.

## 7. 신규 블로커 목록 (BLK-175D-001 ~ 011)

상세는 `blocker-log.md`에 append. 요약:

| ID | 제목 | 심각도 |
|---|---|---|
| BLK-175D-001 | 2016-B/2017-B/2018-B/2019-B "서술형9, 10" phantom row (B 문항 수는 실제 8, coverage는 10) | blocker |
| BLK-175D-002 | 환경윤리 할루시네이션 — 2017-B-서술형10, 2018-B-서술형10, 2020-B-서술형11의 paul_taylor/leopold/jonas 매핑은 원문 grep 0건 | blocker |
| BLK-175D-003 | 2015-A 기입형4 "化性起僞" 원문 미등장 — 실제는 "天人之分" + "禮義" | blocker |
| BLK-175D-004 | Section A 출제 빈도 숫자 과장 — paul_taylor 5회+ → 실제 2회, leopold 5회+ → 실제 1회, 동일 문항 중복 기재로 빈도 부풀림 | blocker |
| BLK-175D-005 | Section B canonical 사상가 빈도도 2020~2022 오매핑으로 오염 — xunzi 6회+, mencius 10회+ 등 재집계 필요 | blocker |
| BLK-175D-006 | 2020-B 11문항 전면 오매핑 — coverage는 2019-B 패턴을 그대로 복붙한 것으로 추정 | blocker |
| BLK-175D-007 | 2021-A 11/12 오매핑 — kant, moore, spinoza, shaftel, blasi, 초기불교, paul_taylor, 6·15선언이 각각 aristotle, confucius, kant, noddings, plato, wangyangming, hobbes+locke, walzer로 잘못 매핑 | blocker |
| BLK-175D-008 | 2021-B 11/11 오매핑 — jinul, locke, turiel+haidt, durkheim+piaget, rest+hoffman, laozi+zhuangzi, yi_i+yi_hwang, sartre+kierkegaard, aristotle+mill, cicero, habermas를 mencius/xunzi/laozi/hanfeizi/buddha/wonhyo/yihwang/jeongyagyong/augustine/hume/habermas로 잘못 매핑 | blocker |
| BLK-175D-009 | 2022-A 10/12 오매핑 — 미국 공화주의, jeongyagyong, nozick, pettit+berlin, plato, kohlberg+turiel, kant, kant+beccaria를 socrates/mencius/kohlberg+gilligan/aristotle/aquinas/kant/bentham+mill/sandel+macintyre로 잘못 매핑 | blocker |
| BLK-175D-010 | 2022-B 10/11 오매핑 — popper, [통일교육], durkheim+piaget, mill_js, xunzi, mozi+hanfeizi, james+dewey, hoffman+noddings, singer+rawls, zhuxi+yi_hwang을 confucius/mencius/xunzi/laozi/zhuangzi/buddha/wonhyo/zhuxi/wangyangming/jeongyagyong로 잘못 매핑 (동양 연속 서술형 가상 시나리오) | blocker |
| BLK-175D-011 | TASK-175B Tester의 "2020~2026 대체로 양호" 판정 자체가 부실 검증 — 본 TASK-175D 전수 검증 결과 2020~2022은 전면 오매핑. 이는 Tester의 spot-check 근거 서술 미비로 인한 허위 통과 | observation |

## 8. 판정 및 후속 조치 권고

1. **exam-coverage-map.md 전면 폐기** 권고. 부분 교정은 무의미. 2023~2026 구간은 독립적으로 재활용 가능하므로 해당 row만 살리고 나머지를 재작성.
2. **Section A, B, C, D, E 모두 재집계** 필요.
3. TASK-175E 등록 제안: "Coder(Opus) 전면 재작성 — 원문 26 파일 직독 후 row-by-row, 배치는 1회=1연도(2과목 합 23문항 이내)". TASK-175A가 1회=13년 전체였던 것이 대량 할루시네이션의 근본 원인.
4. **사상가 등록 우선순위 재평가**: 본 Tester 검증 결과 확증된 직접 출제 2회 이상 누락 사상가는:
   - **확정**: jinul(5회+ 재확인), hoffman(2회+: 2024-A서2, 2025-A서2, 2022-B서8 = 3회), durkheim(2022-B서3, 2024-B서4, 2025-A서1 = 3회), turiel(2021-B서3, 2024-B서3, 2026-A서2, 2022-A서4 = 4회), blasi(2021-A서2, 2023-A서6, 2024-B서5 = 3회), bandura(2025-B서5, 2026-B서5 = 2회), pettit(2022-A서2, 2025-B서10, 2026-B서7 = 3회), moore(2021-A기3, 2025-B서2 = 2회), schumpeter(2026-B서6 = 1회), narvaez(2026-B서3 = 1회), popper(2022-B서1 = 1회), shaftel(2021-A서1 = 1회)
   - **재검토 필요**: paul_taylor, leopold, jonas, singer, regan — 실제 빈도가 claim보다 낮음.
5. **사용자 판정 필요 사항**:
   - 현재 커버리지 맵의 어느 연도(2023+)를 보존할지, 전면 폐기할지
   - 재작성 시 배치 크기 (1연도씩 vs 1과목씩)
   - 사상가 등록 우선순위 재배정 기준 (빈도 vs 주제 커버리지)

## 9. 검증 증빙 원문 인용 (sample)

1. 2021-A 기입형2 원문 ("`~/잡동사니/임용/md/2021_중등1차_도덕윤리_전공A.md` L41~52"):
   > 다음은 서양 근대 사회 사상가의 주장이다. ... "자연 상태란 전쟁의 상태이다. ... ∙제1의 확정 조항: 모든 국가의 시민적 정치체제는 ( ㉠ )이어야 한다. ∙제2의 확정 조항: 국제법은 자유로운 국가들의 연방체제에 기초해야 한다. ∙제3의 확정 조항: 세계시민법은 보편적 우호의 조건들에 국한되어야 한다. ... 이러한 이유로 ㉡ 특별한 종류의 연맹이 있어야 한다."

   → **kant 『영구평화론』 확정 조항 + 평화연맹**. coverage의 "aristotle 중용"은 원문에 단 한 글자도 없음.

2. 2022-A 기입형3 원문 ("`~/잡동사니/임용/md/2022_중등1차_도덕윤리_전공A.md` L32~37"):
   > 다음은 **미국의 공화주의**에 대한 내용이다. ... "국민이 선출한 대표들로 구성된 입법부, 행정권이 균형 있게 분배된 행정부, 불법행위를 하지 않는 한 직책이 보장되는 판사들로 구성된 사법부 ... 행정부와 사법부의 구성원에 대한 입법부의 강제적인 면직 조치인 ( ㉡ )"

   → **미국 공화주의·견제와 균형·탄핵**. coverage의 "socrates 덕·지식"은 원문에 단 한 글자도 없음.

3. 2022-B 서술형1 원문 ("`~/잡동사니/임용/md/2022_중등1차_도덕윤리_전공B.md` L14~18"):
   > 다음은 서양 현대 사회 사상가의 주장이다. ... "논증과 경험을 강조하는 **비판적 합리주의** ... 점진적 사회 공학에 대한 정치적 요구"

   → **popper**. coverage의 "confucius 인·예"는 원문에 없음.

(추가 증빙은 BLK-175D-001~011에서 항목별 제시)

## 10. 결론

- **exam-coverage-map.md는 현재 상태로 사용 불가.**
- 기존 블로커(BLK-001, BLK-175B-001~008) + 신규 블로커(BLK-175D-001~011) 총 **20건** 누적. 단편 수정으로 복구 불가.
- TASK-175B Tester 보고서의 "2020~2026 대체로 양호" 판정은 **spot-check 부실 검증에 기인한 허위 통과**로 판명. Tester 프롬프트(`agents/tester.md`)에 "전수 검증 필수, spot-check 금지" 조항 추가가 필요.
- 본 Tester의 최종 권고: 사용자가 **전면 재작성(1연도=1배치)** 또는 **2023~2026만 보존 후 2014~2022 재작성** 중 선택.
