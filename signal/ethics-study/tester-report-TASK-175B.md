---
agent: tester
task_id: TASK-175B
status: DONE
timestamp: 2026-04-20T02:30:00Z
severity: blocker
---

# Tester Report: TASK-175B — exam-coverage-map.md (TASK-175A 산출) 재검증

## 결과 요약

**판정: BLOCKER (8건 누적)**. TASK-175A Coder(Opus)의 재작성은 BLOCKER-2/3/4를 **부분적으로만** 해소했다. 사용자 확정 샘플(2014-B-논술형4=bentham/kant/hume, 2020-A-기입형3=jinul, 2020-A-기입형4=헌법4조, 2015-A-기입형6=nagarjuna)은 교정되었고, 2020~2026년 범위의 매핑은 대체로 원문과 일치한다. 그러나 다음 영역에서 v1-rejected와 거의 동일한 결함이 잔존하거나 재발했다:

1. **2014-A 기입형/서술형 라벨·매핑 대량 오류** — 기입형 15개 중 12개, "서답형"으로 잘못 라벨된 서술형 5개 모두 원문과 다른 사상가에 매핑.
2. **2014-B 번호 체계 및 매핑 대량 오류** — 실제 "서술형 2 + 논술형 2" 구조를 "논술형1~4"로 일원화; hegel/nietzsche/sartre는 원문에 전무한 할루시네이션 재발.
3. **2015-A 기입형 대량 오매핑** — 10개 중 7개 오매핑. 교정은 기입형6(nagarjuna)만.
4. **2016~2019 A/B 문항 수 분배 오류** — 실제 A=14/B=8인데 coverage는 A=12/B=10으로 기재. 연도 합계(22)는 우연히 일치.
5. **2016-A 기입형 오매핑 샘플 다수** — 4개 중 4개 오매핑(기입형1~4 전부 다른 사상가).
6. **Section E 분류 카운트 claim 불일치** — 실제 row-by-row 재집계 시 합계는 일치하나 231/29/33 대 claim 222/35/36 → BLOCKER-1 재발.
7. **Paul Taylor planned id 내부 불일치** — Coder report `taylor_p` vs coverage-map `paul_taylor`.

총 문항 수 293은 일관되며 canonical thinker_id의 ES 검증은 전건 통과. 잔여 blocker 1건(2026-A-기입형3 사상가 불명)은 주석·report 기록이 적절히 수행됨.

## 검증 결과

### 1. 총 문항 수 일관성 — PASS (부분)

- coverage-map 본문 총 행 수 = **293** (grep `^| 20[12][0-9]-[AB]-` 카운트)
- 연도별:
  - 2014=24, 2015=20, 2016=22, 2017=22, 2018=22, 2019=22 (→ 88 합)
  - 2020=23, 2021=23, 2022=23, 2023=23, 2024=23, 2025=23, 2026=23 (→ 161 합)
  - 총합 = 88+24+20+161 = **293** ✅
- BLOCKER-1 "총 문항 수 일원화" 기준은 외형상 달성.
- 단, Section E 분류 카운트 "합계"는 본문 합계와 총합만 우연히 일치하며 **분류 세부 숫자는 실제와 불일치** → BLK-175B-007로 이어짐.

### 2. 원문 번호 체계 — FAIL

| 연도 | 원문 번호 체계 | coverage-map 기재 | 판정 |
|---|---|---|---|
| 2014-A | 기입형 1~15 + **서술형** 1~5 | 기입형 1~15 + **서답형** 1~5 | ❌ 잘못된 라벨 "서답형" (실제는 서술형) |
| 2014-B | 서술형 1~2 + 논술형 1~2 | 논술형 1~4 (일원 재번호) | ❌ BLOCKER-3 재발 |
| 2015-A | 기입형 1~10 + 서술형 1~4 | 기입형 1~10 + 서술형 1~4 | ✅ |
| 2015-B | 서술형 1~4 + 논술형 1~2 | 논술형 1~6 (일원 재번호) | ❌ BLOCKER-3 재발 |
| 2016~2019 A/B | 실제 A=14, B=8 | A=12, B=10 | ❌ 문항 수 분배 오류 (BLK-175B-005) |
| 2020~2026 | 대체로 일치 | 대체로 일치 | ✅ |

### 3. thinker_id canonical 검증 — PASS

- 구 형식(`yi_hwang`, `yi_i`, `zhu_xi`, `wang_yangming`, `jeong_yakyong`, `taylor_c`) grep 0건 ✅
- coverage-map 본문에서 canonical로 사용된 ID 49건을 ES `/ethics-thinkers/_doc/{id}` lookup한 결과 전건 `found: true` ✅
  - 사용된 canonical: aquinas, arendt, aristotle, augustine, bentham, buddha, confucius, epictetus, epicurus, galtung, gilligan, habermas, haidt, hanfeizi, hegel, hobbes, huineng, hume, jeongyagyong, kant, kohlberg, laozi, lickona, locke, macintyre, mencius, mill_js, mozi, nietzsche, noddings, nozick, piaget, plato, raths, rawls, rest, rousseau, sandel, sartre, socrates, spinoza, walzer, wangyangming, wonhyo, xunzi, yihwang, yiyulgok, zhuangzi, zhuxi
- planned-only ID 34건(`없음(**누락**, planned: xxx)`)은 모두 ES 미등록 상태로 일관 ✅
  - aronson, bandura, berlin, blasi, burke, choe_chiwon, choe_jeu, cicero, coombs, durkheim, fazang, freud, hoffman, jinul, jonas, leopold, machiavelli, nagarjuna, narvaez, niebuhr, nisan, paul_taylor, pettit, regan, schumpeter, shenxiu, shweder, singer, skinner, turiel, uicheon, vasubandhu, viroli, zhiyi
- Paul Taylor 규칙: `paul_taylor` 기재 row 5건 모두 "없음(누락)" 커버리지로 표기. 단, Coder report는 `taylor_p`로 명시했으므로 naming 충돌(BLK-175B-008).

### 4. 사상가-문항 매핑 (이전 블로커 샘플 교정 여부) — 혼재 (일부 PASS, 일부 FAIL)

| 문항 | 이전(v1-rejected) | 현재(TASK-175A) | 원문 근거 | 판정 |
|---|---|---|---|---|
| 2014-A 기입형1 | wonhyo 원효·일심 | lickona CDP | "아동 발달 프로젝트·배려하는 공동체·4가지 우선과제" | ✅ 교정됨 |
| 2014-A 기입형2 | hobbes | raths + coombs | "수업모형 A 가치갈등분석 / B 가치명료화 7절차" | ✅ 교정됨 |
| 2014-A 기입형13 | singer 종차별 | burke | "편견·동반자 관계·여러 세대" | ✅ 교정됨 |
| **2014-A 기입형3** | — | plato 이데아 | 원문=bandura 사회인지·도덕이탈(P·E·B 도식, 도덕적 정당화·완곡한 언어·유리한 비교 등) | ❌ 재발 오매핑 |
| **2014-A 기입형5** | — | epicurus 아타락시아 | 원문=nagarjuna 中論 공(不生不滅·不斷不常·不一不異·不來不去) | ❌ 재발 오매핑 |
| **2014-A 기입형6** | — | aquinas 자연법 | 원문=zhuangzi 가죽나무·무용지용·소요 | ❌ 재발 오매핑 |
| **2014-A 기입형9** | — | confucius/mencius | 원문=dewey 사유·진리·liking·prizing·운동 방향 | ❌ 재발 오매핑 |
| **2014-A 기입형10** | — | laozi/zhuangzi | 원문=spinoza 수동정서·명석판명·신·정서 | ❌ 재발 오매핑 |
| **2014-A 기입형11** | — | yihwang/yiyulgok | 원문=habermas 심의민주주의(개인적 선호 결집 vs 심의) | ❌ 재발 오매핑 |
| **2014-A 기입형12** | — | jeongyagyong 성기호 | 원문=[통일] 김대중~박근혜 대북정책 A~D 순서 | ❌ 재발 오매핑 |
| **2014-A 기입형14** | — | singer/regan | 원문=machiavelli 군주·3가지 정치체제·저변 넓은 체제 | ❌ 재발 오매핑 |
| **2014-A 기입형15** | — | buddha 사성제 | 원문=rousseau 불평등 기원론(3단계) | ❌ 재발 오매핑 |
| **2014-A 서술형1~5** (coverage=서답형1~5) | — | wonhyo/huineng/zhuxi/socrates/augustine | 원문=turiel 영역이론 / zhuxi-wangyangming 지행 / 환인·환웅·단군 / 무극이태극 / aristotle 영혼 탁월성 | ❌ 5건 모두 재발 오매핑 |
| 2014-B 논술형4 | jinul 돈오점수 | bentham/kant/hume | "벤담 공리·칸트 정언명령·흄 도덕감" (사용자 확정) | ✅ 교정됨 (단 번호는 원문 "논술형2"가 맞음) |
| **2014-B 논술형1** | — | hegel 인륜성 | 원문=[국제정치] 4관점(현실/자유/세계체제/구성주의) | ❌ 재발 할루시네이션 |
| **2014-B 논술형2** | — | nietzsche 초인 | 원문=[통일] 통일비용·편익·S1/S2 | ❌ 재발 할루시네이션 |
| **2014-B 논술형3** | — | sartre 실존 | 원문=[교과교육학] 도덕 교과 필요성 | ❌ 재발 할루시네이션 |
| 2015-A 기입형6 | leopold 대지윤리 | nagarjuna 中論 팔불중도 | "이것은 불멸·불생·부단·불상·불래·불거·불이·불일" | ✅ 교정됨 |
| **2015-A 기입형1** | — | [교육과정] 2015 도덕과 | 원문=macintyre 계몽주의기획·목적론·덕·내러티브 | ❌ 재발 오매핑 |
| **2015-A 기입형2** | — | confucius 정명 | 원문=[교과교육학] Newmann 환경적 능력 수업모형 | ❌ 재발 오매핑 |
| **2015-A 기입형7** | — | hobbes 자연상태 | 원문=habermas 이상적 담화 | ❌ 재발 오매핑 |
| **2015-A 기입형9** | — | rousseau 일반의지 | 원문=plato 철인정치·항해사 비유 | ❌ 재발 오매핑 |
| **2015-A 기입형10** | — | rawls 정의 두 원칙 | 원문=[통일·인권] 헬싱키 프로세스·UN 대북결의 | ❌ 재발 오매핑 |
| 2017-A 서술형1(원문 서술형1=5번문항) | — | socrates/plato 덕=지식·영혼삼분 | 본 검증에서 2017 세부 sample-only, 원문 직접 매칭 보류 | ⚠ 미검증(BLK-175B-005 선행 해결 후 재검증 필요) |
| 2020-A 기입형3 | rawls 정의 | jinul 자성정혜 | "자성정혜·수상정혜·돈문·점문" | ✅ 교정됨 |
| 2020-A 기입형4 | epicurus/stoic | [통일] 헌법 4조 | "헌법 제4조·통일교육지원법 제3조" | ✅ 교정됨 |
| **2020-A 기입형1** | — | [교육과정] | 원문=rest 4구성요소 + haidt 도덕적 전문가·자동성 | ❌ 오매핑 (교육과정 무관) |
| **2020-A 기입형2** | — | mencius 사단 | 원문=[메타윤리] 사실판단·정서주의·규정주의 | ❌ 오매핑 |
| 2023-A (sample 1~7) | — | 대체로 정확 | 원문과 일치 (viroli, choe_jeu, kohlberg+haidt+shweder 등) | ✅ PASS |
| 2025-A (sample 1~6) | — | 대체로 정확 | laozi/zhuangzi, 결의론, 통일, durkheim+aronson, hoffman+rest 원문 일치 | ✅ PASS |
| 2026-A (sample 1~5) | — | 대체로 정확 | aquinas 이중효과, 갈퉁, noddings 원문 일치 | ✅ PASS |
| **2016-A 기입형1~4** | — | [교육과정]/kohlberg/mencius/kant | 원문=rest 4구성요소 / SEL 5역량 / wangyangming 치지격물 / yihwang 理氣겸·성정 | ❌ 4건 재발 오매핑 |

**요지**: TASK-175A는 사용자 명시 샘플(2014-B-논술형4, 2015-A-기입형6, 2020-A-기입형3/4)과 2014-A 앞 3개만 교정했고, **2014-A 나머지·2014-B 1~3·2015-A·2016-A·2016~2019 A 다수**는 v1-rejected 수준의 결함을 유지 중이다. 2020년 이후는 대체로 양호.

### 5. 원문 인용 진위성 (할루시네이션) — FAIL

이전 4종(2014-A1/A2/A13, 2015-A6)은 교정되었으나, **새로운 대규모 할루시네이션** 발생:

- 2014-B 논술형1~3: hegel/nietzsche/sartre 관련 구절("인륜의 최고 형태는 국가", "위버멘쉬·영원회귀", "실존은 본질에 앞선다; 자유에 저주받은 존재")이 원문에 단 한 단어도 등장하지 않음. 원문은 국제정치 4관점, 통일비용 S1/S2, 도덕 교과 필요성 논쟁.
- 2014-A 서술형3 (coverage 서답형3): "원효 일심이문·화쟁으로 百家異諍을 회통" — 원문은 환인·환웅·단군·삼위태백 신화. 원효 언급 전무.
- 2014-A 서술형4 (coverage 서답형4): "너 자신을 알라; 문답법" — 원문은 무극이태극·태극도설, 소크라테스 언급 전무.
- 2014-A 서술형5 (coverage 서답형5): "지상의 나라·신국; ordo amoris" — 원문은 Aristotle 영혼·탁월성, Augustine 언급 전무.

### 6. 분류 정확성 — FAIL (부분)

- 2014-A 기입형12(대북정책 A~D 순서)를 "사상가형·jeongyagyong"으로 분류 → 실제 [통일] 경계영역.
- 2014-A 기입형11(심의민주주의 비교)을 "사상가형·yihwang/yiyulgok"로 분류 → 실제 [정치사상·심의민주주의] 경계영역 or habermas 사상가형.
- 2014-B 논술형1(국제관계 4관점) "사상가형·hegel" → 실제 [응용윤리·국제정치] 경계영역.
- 2014-B 논술형2(통일비용) "사상가형·nietzsche" → 실제 [통일] 경계영역.
- 2014-B 논술형3(도덕 교과 필요성) "사상가형·sartre" → 실제 교과교육학.
- 2015-A 기입형2(공공정책 참여 수업모형) "사상가형·confucius" → 실제 교과교육학.
- 2015-A 기입형3(친구관계 가치) "사상가형·mencius" → 실제 교과교육학 또는 경계영역(가치·덕목 교육).
- 2015-A 기입형10(헬싱키·UN 대북결의) "사상가형·rawls" → 실제 [통일·인권] 경계영역.
- 2016-A 기입형2(SEL 5역량) "사상가형·kohlberg" → 실제 교과교육학.
- 2020-A 기입형2(정서주의·규정주의) "사상가형·mencius" → 실제 [메타윤리] 경계영역.

분류 오류는 매핑 오류에 파생된 것으로, 매핑 수정 시 함께 교정되어야 한다.

### 7. 잔여 블로커 (Coder 마킹) — PASS

- `2026-A-기입형3`: coverage-map L551에 `<!-- BLOCKER(TASK-175A): 조식·이황·이이·정약용 중 원문만으로 단정 불가. 『심경』·『성리대전』 선독 패턴은 조식(曺植) 유력하나 canonical id 없음. Tester 확인 필요 -->` 주석 확인 ✅
- 원문 재독 결과 "안을 밝히는 것은 敬, 밖으로 결단은 義; 小學→『心經』→『성리대전』" 은 **조식(曺植, 남명)** 의 학문 방법에 가장 부합 (敬義협구·심경 강조는 남명학파의 trademark). 다만 ES에 `jo_sik` 미등록 및 출제자의 명시 없음으로 본 blocker 유지 정당.
- BLK-175A-001이 `blocker-log.md`에 별도 등록되지 않았음 — Coder report는 "신규 등록 권장"만 하고 actual append는 Manager 몫이나, Tester 세션에서 확인된 잔여 blocker이므로 Manager가 `BLK-175A-001` 을 `blocker-log.md`에 이관하는 것이 권장.

### 8. 섹션 A~E 완결성

- **Section A** (L582~620): planned id 35인 나열 ✅. 다만 빈도 수치는 본문 실제 등장 횟수와 재대조 필요. jinul 5회 claim은 본문 등장 5건 확인 ✅. paul_taylor 5회 claim도 본문 등장 5건(2015-B-논술형4, 2017-B-서술형10, 2018-B-서술형10, 2020-B-서술형11, 2026-A-서술형8) 확인 ✅.
- **Section B** (L622~681): canonical 55인 빈도. "kant 13회+, aristotle 11회+" 등 주요 claim은 본문과 대체로 부합하는 방향이나, **본문 매핑이 대량 오류**이므로 Section B 빈도 자체도 오염 가능. 재매핑 후 재집계 필요.
- **Section C** (L683~692): topical 주제군 목록. 형식적으로 완결되나 [통일] 빈도 7회+ claim이 `2014-A-기입형12` 등 재분류 대상이 포함되지 않아 실제로는 8~9회로 증가 가능.
- **Section D** (L694~701): 저빈도 canonical 6인(seneca/marcus_aurelius/taylor/baek_nakcheong/kang_mangil/dewey) 힌트. 단 **dewey는 2014-A-기입형9에 실제 등장** (도구주의·liking/prizing)하나 매핑 누락으로 coverage가 0회 처리 → BLK-175B-001 교정 후 dewey 빈도 재집계 필요.
- **Section E** (L703~720): 합계는 일치하나 연도별 카운트 8개 row 불일치 → BLK-175B-007.

## 발견 이슈 전체 리스트

1. **[blocker]** 2014-A 기입형 15개 중 12개 + 서술형(coverage 서답형) 5개 전체 오매핑 — BLK-175B-001
2. **[blocker]** 2014-B 번호 체계("논술형1~4")가 원문 "서술형1~2 + 논술형1~2" 구조와 불일치 — BLK-175B-002
3. **[blocker]** 2014-B 논술형1~3(coverage)의 hegel/nietzsche/sartre 매핑은 원문에 전무한 할루시네이션 — BLK-175B-003
4. **[blocker]** 2015-A 기입형 10개 중 7개 오매핑 — BLK-175B-004
5. **[blocker]** 2016~2019 A/B 문항 수 분배(A=12/B=10)가 실제(A=14/B=8)와 불일치 — BLK-175B-005
6. **[blocker]** 2016-A 기입형 1~4 전부 오매핑 — BLK-175B-006
7. **[blocker]** Section E 분류 카운트 231/29/33 대 claim 222/35/36 불일치 (BLOCKER-1 재발 형태) — BLK-175B-007
8. **[bug]** Paul Taylor planned id 표기가 coverage-map(paul_taylor) vs Coder report(taylor_p)로 상충 — BLK-175B-008
9. **[observation]** Coder report의 "품질 체크리스트" 중 "26파일 전수 Read" 항목이 **기각**됨 — 2014-A/B, 2015-A, 2016-A 대량 오매핑은 **원문 직독을 실제로 수행하지 않았거나, 수행했으나 v1-rejected 내용을 교차 확인 없이 재사용**했음을 시사.
10. **[observation]** 2020~2026년 매핑은 대체로 양호. 이 구간은 재작업에서 가장 신중하게 검토된 것으로 보임.
11. **[observation]** 2026-A-기입형3 잔여 blocker(조식·심경) 주석은 적절. ES 에 `jo_sik` 또는 유사 id 등록 검토 가치 있음.

## 블로커 누적 기록

`signal/ethics-study/blocker-log.md`에 다음 8건 append 완료:
- BLK-175B-001 — 2014-A 기입형/서술형 라벨 및 매핑 대량 오류
- BLK-175B-002 — 2014-B 번호 체계 및 매핑 오류
- BLK-175B-003 — 2014-B hegel/nietzsche/sartre 할루시네이션 (BLOCKER-4 재발)
- BLK-175B-004 — 2015-A 기입형 대량 오매핑
- BLK-175B-005 — 2016~2019 A/B 문항 수 분배 오류
- BLK-175B-006 — 2016-A 기입형 1~4 오매핑 샘플
- BLK-175B-007 — Section E 분류 카운트 불일치 (BLOCKER-1 재발)
- BLK-175B-008 — Paul Taylor planned id 표기 상충

## 다음 제안

1. **Manager**: 본 Tester 판정을 BLK-001 누적 기록에 반영하고, 사용자에게 판정 요청.
2. **사용자 결정 대기 사항**:
   - 2014-A/B, 2015-A 전체(34 row), 2016~2019 A/B 재분배(~88 row)에 대한 **2차 재작업 승인 여부** — 규모가 크므로 별도 태스크(TASK-175C)로 재호출 필요 가능.
   - Coder 자격 재검토 — TASK-175A에서 Opus 모델이 claim한 "전수 Read"의 실제 이행 여부가 의심스러움. 다음 재작업 시 페이지별 원문 구절 인용 강제(메모 필드를 실제 원문 구절로 채우고 행별 line reference 병기) 등 감사 기제 추가 권장.
   - Section E 카운트는 기계 재집계가 가능하므로, coverage-map 확정 후 자동 스크립트로 Section E·B 재생성하는 것이 바람직.
3. **부분 수용 옵션**: 2020~2026년 구간은 대체로 양호하므로, 해당 구간만 먼저 "검증 완료"로 label하고 2014~2019 구간을 block된 채 병렬 후속 태스크에서 재작업할 수 있음 (사용자 판단).
4. **architecture.md**: "블로커 누적 처리 정책"에 따라 본 재검증 실패를 기록. BLK-001이 2차까지 미해소되었으므로 `사용자 검토 대기` 상태로 승격.

---

**Status: DONE (판정: BLOCKER, severity=blocker)**
