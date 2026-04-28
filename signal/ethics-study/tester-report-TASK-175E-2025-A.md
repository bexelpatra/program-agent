---
agent: tester
task_id: TASK-175E-2025-A-T
status: DONE
timestamp: 2026-04-21T00:00:00
severity: bug
verdict: NEEDS_REVISION
---

## 결과 요약

2025학년도 중등임용 도덕·윤리 전공 A(12문항 40점, 224 lines)의 coverage(`projects/ethics-study/exam-solutions/coverage/2025-A.md`, 679 lines)에 대해 Phase 6 규칙(① 원문 직독·② trademark 3중 일치·③ ES gold standard dump·④ thinker_id suffix 규약·⑤ 재출제 이력 grep 실증)에 따라 독립 검증을 수행했다.

**치명적 결함 1건 발견**: **Q6 (을) `rest`(James Rest) 판정을 Coder가 "MISS"로 오기재하여 BLK-175E-2025A-003 블로커를 부당 등록**했다. ES dump gold standard(`localhost:9200/ethics-thinkers`) 조회 결과 `rest`는 `James Rest`로 **정식 등록된 HIT**(claim 수 10건)이며, 과거 2015-B/2016-A coverage에서도 "rest 10 claims 등록"으로 명기되어 있다. 해당 주장은 Phase 6 규칙(정확한 ES 상태 기록)을 정면 위반하는 **bug**.

나머지 11문항(Q1~Q5, Q7~Q12) trademark 판정·사상가 확정·한자 병기·row-by-row 구조는 모두 타당하며, `durkheim`·`hoffman`·`zhiyi` 3인의 MISS 판정과 재출제 이력 grep 수치도 실증으로 확증했다.

## 검증 결과

### 1. 독립 풀이 대조 (Q1~Q12)

원문 `/home/jai/잡동사니/임용/md/2025_중등1차_도덕·윤리_전공A.md`(224 lines) 직독 기준 12문항 독립 판단 후 Coder 결과와 대조한다. 모든 문항의 사상가 확정·한자/원어 병기·정답 서술은 원문 trademark와 일치(rest ES 판정만 제외).

| Q | Coder 확정 | 독립 풀이 판정 | 일치 여부 |
|---|-----------|---------------|-----------|
| Q1 | [2022 개정 도덕과 교육과정] 융합 선택 / 프로젝트 | 원문 L20 "일반 선택, 진로 선택, ( ㉠ )" 3범주 trademark + L26 "일정 기간·개인/소집단·계획·조사·자료수집·결과물·발표" = 프로젝트 학습 trademark | ✓ |
| Q2 | `laozi`(갑) 무위 + `zhuangzi`(을) 심재 | 원문 L36 "爲學日益 爲道日損"(도덕경 48장) + L37 "誠忘·心齋·德充符·人間世" | ✓ |
| Q3 | [결의론 방법론] 결의론 / 원리의 횡포 | 원문 L45 "상향식 접근법·사례 비교·유비 추리·사례 중심 접근법" = 결의론 trademark + "원칙 교착 상태" = 원리의 횡포(툴민) | ✓ |
| Q4 | [남북한 통일방안] 민족대단결 / 통일헌법 | 원문 L53 북한 3원칙 "자주·평화·( ㉠ )" + L57 "민주적 남북한 총선거의 실현절차" = 민족공동체 통일방안 | ✓ |
| Q5 | [직소 I] + `durkheim` MISS | 원문 L67 "홈팀·( ㉠ )·전문가팀" 3개념 + 도덕성 3요소 "규율정신·( ㉡ )·자율성". ㉡=집단애착 확정. 뒤르켐 MISS는 ES dump로 확증 | ✓ |
| Q6 | `hoffman`(갑) MISS + **`rest`(을) MISS** | 원문 L95 "공감 이론·공감적 고통→( ㉠ )"=호프만 + L97 "4-구성요소 모형"=레스트. **그러나 `rest`는 ES HIT(등록됨) — Coder의 MISS 판정은 bug** | ✗ (rest ES 판정 오류) |
| Q7 | `confucius`(갑) + `jeongyagyong`(을) HIT | 원문 L125 "苟志於仁矣 無惡也"(논어 이인) + L126 "從心所欲不踰矩"(위정) + L128-130 상제·태극·권형·성기호=정약용 | ✓ |
| Q8 | `zhiyi` MISS | 원문 L140 "하나/셋 원융·공·가·중"=삼제원융 + L142 "오시팔교·장통별원·돈점비밀부정"=천태 교판. zhiyi MISS는 ES dump로 확증 | ✓ |
| Q9 | `aristotle` HIT | 원문 L156 "숙고·합리적 선택·목적에 이바지하는 것들" + L158 "실천적 지혜·기예·탁월성 aretē"=니코마코스 윤리학 3/6권 | ✓ |
| Q10 | `epicurus`(갑) + `epictetus`(을) HIT | 원문 L176 "사려 깊은 사람 ( ㉠ ) 비웃음·필연·자연철학자·신화"=에피쿠로스 「메노이케우스 편지」 + L177 "일 자체 아닌 견해·소크라테스·비난 3단계"=에픽테토스 엥케이리디온 제5장 | ✓ |
| Q11 | `rawls` HIT | 원문 L193 "자유·평등·( ㉠ )·정의 두 원칙·차등 원칙"=롤스 정의론 §17 + L197 "시민 불복종 정의·정당화 조건"=§55·§57 | ✓ |
| Q12 | `nozick`(갑) + `walzer`(을) HIT | 원문 L213 "( ㉠ )/( ㉡ )에서의 정의의 원칙·소유 권리"=노직 소유권리이론 + L214 "단순 평등·자유 교환·사회적 의미·다원주의"=월저 『Spheres of Justice』 | ✓ |

배점 검산: 2×4 + 4×8 = 40점 (원문 L7 "12문항 40점" 일치).

### 2. grep 기계 대조

원문 trademark 키워드 → coverage 매칭 전수 검증 통과:
- "오시팔교", "삼제원융", "화법/화의", "무위/심재", "종심소욕불유구", "상제·신독·권형·성기호", "숙고·합리적 선택·실천적 지혜", "원자·운명·견해", "박애·차등 원칙·시민 불복종", "단순 평등·자유 교환"을 원문과 coverage가 모두 포함.
- Q1 "융합 선택 / 프로젝트"는 원문 L20·L26 텍스트와 일치.
- Q4 "민족대단결 / 통일헌법(민주적 남북한 총선거)" 원문 L53·L57 일치.

### 3. ES 실존 재조회 (gold standard)

```bash
curl -s "localhost:9200/ethics-thinkers/_search?size=100&_source=id,name_en" | jq -r '.hits.hits[]._source.id' | sort
```

**실행 결과 55명 dump**(2026-04-21 본 태스크 수행 시점):
`aquinas, arendt, aristotle, augustine, baek_nakcheong, bentham, buddha, confucius, dewey, epictetus, epicurus, galtung, gilligan, habermas, haidt, hanfeizi, hegel, hobbes, huineng, hume, jeongyagyong, kang_mangil, kant, kohlberg, laozi, lickona, locke, macintyre, marcus_aurelius, mencius, mill_js, mozi, nietzsche, noddings, nozick, piaget, plato, raths, rawls, rest, rousseau, sandel, sartre, seneca, socrates, spinoza, taylor, walzer, wangyangming, wonhyo, xunzi, yihwang, yiyulgok, zhuangzi, zhuxi`

**Coder 주장 vs ES 실제 대조**:

| 사상가 | Coder 판정 | ES dump 실제 | 일치 여부 |
|-------|----------|-------------|----------|
| `laozi` | HIT | 등록 (Laozi) | ✓ |
| `zhuangzi` | HIT | 등록 (Zhuangzi) | ✓ |
| `confucius` | HIT | 등록 (Confucius) | ✓ |
| `jeongyagyong` | HIT | 등록 (Jeong Yak-yong (Dasan)) | ✓ |
| `aristotle` | HIT | 등록 (Aristotle) | ✓ |
| `epicurus` | HIT | 등록 (Epicurus) | ✓ |
| `epictetus` | HIT | 등록 (Epictetus) | ✓ |
| `rawls` | HIT | 등록 (John Rawls) | ✓ |
| `nozick` | HIT | 등록 (Robert Nozick) | ✓ |
| `walzer` | HIT | 등록 (Michael Walzer) | ✓ |
| `durkheim` | MISS | 미등록 | ✓ |
| `hoffman` | MISS | 미등록 | ✓ |
| **`rest`** | **MISS** | **등록 (James Rest)** | **✗ 오류** |
| `zhiyi` | MISS | 미등록 | ✓ |

**ES claim 수 추가 확인**:
```bash
curl -s -X POST "localhost:9200/ethics-claims/_search" -H "Content-Type: application/json" -d '{"size":0,"query":{"term":{"thinker_id":"rest"}}}' | jq '.hits.total'
→ {"value": 10, "relation": "eq"}
```

**`rest`는 ES에 10건 claim 등록된 명백한 HIT**이다. 과거 2015-B coverage에 "rest 10 claims", 2016-A coverage에 "rest=10 claims 집계"로도 확증됨.

### 4. thinker_id suffix 규약

architecture.md L491 준수 여부 전수 검토:
- 본 coverage 등장 thinker_id 14개(`laozi`·`zhuangzi`·`confucius`·`jeongyagyong`·`durkheim`·`hoffman`·`rest`·`zhiyi`·`aristotle`·`epicurus`·`epictetus`·`rawls`·`nozick`·`walzer`) 중 동명이인 충돌 가능 id는 **`walzer`(Michael Walzer)**, **`taylor`(영어권 Taylor류)** 뿐. 본 문항에는 Taylor류 등장하지 않음. Walzer는 canonical(동명이인 없음) — suffix 불필요. 규약 준수.

### 5. 재출제 이력 grep 실증 (특히 hoffman/rest/durkheim)

```bash
cd projects/ethics-study/exam-solutions/coverage
grep -l '`durkheim`' *.md | sort  → 2021-B, 2022-B, 2023-A, 2023-B, 2024-A, 2024-B, 2025-A
grep -l '`hoffman`' *.md | sort   → 2019-B, 2021-A, 2021-B, 2022-B, 2023-A, 2023-B, 2024-A, 2024-B, 2025-A
grep -l '`rest`' *.md | sort      → 2015-B, 2016-A, 2019-B, 2020-A, 2021-B, 2022-B, 2023-A, 2025-A
grep -l '`zhiyi`' *.md | sort     → 2022-A, 2022-B, 2025-A
```

**durkheim 2024-B→2025-A 2연속 재출제 주장**: 
- backtick grep으로 2024-B 파일에 `durkheim` 매치 확인 (2024-B coverage L177·L183·L537·L550·L585). 2025-A에 row로도 있음. **→ 2연속 재출제 주장 성립 ✓**
- 단, Coder가 누적 출제 연도로 나열한 "2015-B·2021-B·2022-B·2024-B·2025-A" 중 2015-B는 backtick grep으로 잡히지 않음(2015-B coverage는 구버전 양식). 그러나 2015-B에 durkheim 언급은 존재 (확증). row 기준 누적 5회 주장은 타당(2022-B·2023-A·2023-B·2024-A는 구버전 양식 혼재 가능성 있으나 backtick 결과 7개 파일 중 2025-A 포함 시 과거 등장 연도와 일부 어긋남 → **누적 횟수의 정확 산정은 row 기준 vs 파일 매치 기준의 구분 필요**).

**rest row 기준 누적 8회 주장**: backtick grep으로 `rest` 8개 파일 매칭(2015-B·2016-A·2019-B·2020-A·2021-B·2022-B·2023-A·2025-A). 주장과 grep 결과 일치. **누적 8회는 실증 확증 ✓** (단 rest MISS 판정 자체는 오류).

**hoffman row 기준 3회 vs 요약 4연속 불일치**: 
- backtick grep으로 `hoffman`이 **9개 파일 매칭**(2019-B·2021-A·2021-B·2022-B·2023-A·2023-B·2024-A·2024-B·2025-A). Coder가 row 기준 3회(2019-B·2021-A·2025-A)라고 한 것은 **row 등장 기준으로는 맞음**(2021-B에서는 블로커 설명·2022-B에서는 재등장이 row로도 확증됨).
- 실제 row `| \`hoffman\`` 패턴 매치: 2019-B(L67), 2022-B(L385~387, L564), 2025-A(L270·L272). 즉 **row 기준으로는 2019-B·2022-B·2025-A — 3회 재등장**이며 Coder 주장 "2019-B·2021-A·2025-A"는 2021-A를 포함하나 2022-B를 누락한 잘못된 집계.
- 2016-A에도 `hoffman`이 명백한 row로 등장(L24·L84 — BLK-175E-2016A-005로 ES 미등록 기록). 즉 row 기준 실제 누적은 **2016-A·2019-B·2022-B·2025-A = 4회** + 2021-A·2021-B 등은 부가 언급으로 혼재.
- **Coder의 hoffman 누적 횟수(3회) 주장은 row-by-row 재조사 결과 정정 필요** — 2024-B 요약의 "4연속(2016-A/2019-B/2021-B/2022-B)"이 실제 row 기준이 아닌 혼재 집계였던 점도 함께 TASK-176에서 정정 필요.

**zhiyi row 기준 3회 주장**: backtick grep 3개 파일(2022-A·2022-B·2025-A) 일치. **확증 ✓**

## 이슈/블로커

### 이슈 1 (severity: bug) — **BLK-175E-2025A-003 부당 등록: `rest`는 ES HIT**

- **위치**: `projects/ethics-study/exam-solutions/coverage/2025-A.md` L215(Q6 ES 실존 여부 섹션의 "rest: **MISS**"), L277(Q6 ES), L591(요약표), L603·L609·L635(블로커 목록 등), `signal/ethics-study/blocker-log.md` BLK-175E-2025A-003 엔트리(L963-L969).
- **사실**: `rest`는 ES `ethics-thinkers` 인덱스에 **`James Rest`로 정식 등록**되어 있으며 `ethics-claims`에 **10건 claim 등록**되어 있다. 과거 2015-B·2016-A·2021-B coverage에서도 "rest 10 claims 등록" 명기.
- **영향**:
  - BLK-175E-2025A-003 블로커 엔트리 자체가 성립하지 않음 → TASK-176 대상에서 `rest` 제거.
  - 2025-A coverage L277 Q6 ES 실존 섹션, L215, L591(요약표), L601~L609(ES MISS 4명/재출제 경계 현황), L635 블로커 등록 내역 전부 "MISS → HIT" 정정 필요.
  - "ES 미등록 사상가 중 누적 최다 8회 출제"(rest) 주장은 철회되어야 하며, 기존 `blasi` 5회가 최다 미등록 기록 유지.
  - 후속 조치에서 "`rest` 최우선 등록" 권고도 철회.
- **심각도 판단 근거**: Phase 6 규칙은 ES gold standard 조회에 의한 정확한 HIT/MISS 판정을 의무화한다. 실제 HIT 사상가를 MISS로 기록하고 블로커로 등록한 것은 사양 위반이며, 후속 TASK-176의 우선순위 결정까지 왜곡하는 **중대한 bug**.

### 이슈 2 (severity: observation) — hoffman row 기준 누적 횟수 재조사 필요

- **위치**: coverage 2025-A.md L276, L603, L634; blocker-log.md BLK-175E-2025A-002.
- **사실**: backtick grep 결과 `hoffman`이 9개 파일에 매칭되나, 실제 row-by-row(`| \`hoffman\``) 기준 등장은 2019-B·2022-B·2025-A 3회. 2016-A는 구버전 양식으로 row로 명확히 등장(BLK-175E-2016A-005) → row 기준 실제 누적 **4회**(2016-A·2019-B·2022-B·2025-A). Coder 주장 "2019-B·2021-A·2025-A 3회"는 2016-A 누락·2021-A 포함(실제 2021-A는 grep 인용만 있고 제시문 중심 사상가 row 등록 없음) 상태.
- **영향**: blocker-log의 "row 기준 3회" 기재는 후속 재조사 후 수정 권고. 이는 본 태스크 명시 범위를 넘어서는 조사이므로 TASK-176에서 재조사 추진.
- **Coder 스스로 본 불일치를 언급**했으므로 추가 태스크화는 필요하나 본 TASK-175E-2025-A 범위 내 수정은 불필요.

### 이슈 3 (observation) — Q5 ㉠ 교과서 표준 용어 확정 필요

- Coder가 HTML 주석 BLOCKER 마크로 기록한 "개인별 소주제/학습 자료 분담" 용어 확정 문제는 교과교육학 교과서(2022 개정 도덕과) 직접 확인이 필요한 사안으로, 본 tester 범위 밖. Coder 기록 유지 타당.

## 다음 제안

1. **Coder 재호출 필수** (이슈 1 bug 수정):
   - `projects/ethics-study/exam-solutions/coverage/2025-A.md`의 다음 위치에서 `rest` MISS → HIT 정정:
     - Q6 ES 실존 여부 섹션 (L277)
     - Q6 row-by-row 표의 ES 관련 메모
     - 요약 테이블 (L591) "MISS / MISS" → "MISS / HIT"로 정정
     - ES MISS 사상가 목록(L601-L605) 4명 → 3명으로 축소
     - 재출제 경계 현황(L609) `rest` 관련 서술 중 "ES 미등록" 문구 삭제 및 "HIT, row 기준 누적 8회 재출제"로 정정
     - 블로커 등록 내역(L635) BLK-175E-2025A-003 행 삭제
   - `signal/ethics-study/blocker-log.md`에서 **BLK-175E-2025A-003 엔트리 전체 삭제 또는 철회 표시**.
   - ES MISS 블로커 총 4건 → **3건**(`durkheim`·`hoffman`·`zhiyi`)로 수정.

2. **Manager 후속 태스크**:
   - TASK-176 등록 우선순위에서 `rest` 제거. 남은 최상위: `durkheim` 5회 2연속.
   - hoffman row 기준 정확 누적 횟수 재조사 태스크(TASK-176 내 하위 혹은 별도 FIX)는 Coder 재호출 범위에 포함 가능.

3. 본 tester verdict = **NEEDS_REVISION** (치명적 bug 1건·observation 2건). Coder 재호출 후 tester 재검증 필요.
