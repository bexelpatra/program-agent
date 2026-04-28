---
agent: tester
task_id: TASK-185-T
status: DONE
timestamp: 2026-04-22T20:05:00
verdict: FAIL
severity: bug
---

## 결과 요약

`projects/ethics-study/exam-solutions/study-guide/2015-B.md`(Coder 산출물, 실측 **516 lines** · 62914 byte — Manager 공지 "529 lines" 와 lines count 불일치, byte 일치)에 대해 8항 체크 전수 수행. **8개 항목 중 7개 PASS / 1개 FAIL**.

**FAIL 항목**: 항목 8 — 자기검증 Step 1 영어 괄호 토큰 역grep 에서 **bare-id-style 0-hit 토큰 2건** 발견(`(moral motivation)`, `(moral character / implementation)`). 두 English 문구는 coverage L15 에 "도덕적 동기(道德的 動機 — moral motivation)" 형태로 존재하나, Coder 산출물은 한자+em-dash 래퍼를 제거하고 bare-id 형태로 축약 재포장했다. agents/tester.md "원문-grep 0건 자동 severity=bug" 규칙(+ TASK-184-FIX 선례) 엄수에 따라 **severity=bug**.

**Greek/Cyrillic 확장 정규식 실측 결과**: 0건 (2015-B.md 에는 Greek/Cyrillic 문자 포함 괄호 토큰 부재 — 이번 회차에는 발동 없음, 규약 연속성 유지 확인). TASK-184-FIX 의 Greek 확장 패턴이 후속 회차에서 실제 0-hit 로 유지되는 것이 최초로 검증되어 규약 연속성 재현성 확보.

## 변경된 파일

없음(테스트 전용, 소스 미수정).

## 8항 체크 결과 표

| # | 체크 항목 | 실측 근거 | 결과 |
|---|----------|-----------|------|
| 1 | 문항 수 6 | `grep -c '^## 문항' study-guide/2015-B.md` == **6** (L43/L99/L154/L213/L273/L384) | ✅ PASS |
| 2 | 섹션 헤더 `원문 line L{m}-L{n}` 6건 | grep 실측: `L14-L31` (L43) · `L35-L41` (L99) · `L45-L51` (L154) · `L55-L67` (L213) · `L75-L81` (L273) · `L89-L91` (L384) — Manager 기대치 6/6 전수 일치 | ✅ PASS |
| 3 | verbatim byte-level 샘플 8건 전수 coverage hit≥1 | 표 A 참조 (8/8 hit≥1) | ✅ PASS |
| 4 | thinker_id 11건 ES 재조회 전수 `found=true` | 표 B 참조 (11/11 found=True) | ✅ PASS |
| 5 | 본문 내 claim_id 전수 ES `found=true` | grep 으로 추출한 claim_id 2건(singer-claim-001 L191, durkheim-claim-001 L347) 전수 `found=True` | ✅ PASS |
| 6 | DQ-007 override — singer/durkheim ✅ES 등록 + ⚠️ES 미등록 태그 실 thinker 부착 0건 | L18/L28/L31/L190/L346 에 singer·durkheim "✅ES 등록 · found=true · TASK-DQ-007 override" 명시; `⚠️ES 미등록` 문자열 2건 등장(L19/L514)은 모두 **"⚠️ES 미등록 0건"** 식 메타 부재 선언(실 thinker 부착 0건) | ✅ PASS |
| 7 | NOTE-BLOCKER-1 주석 5지점 실재 | L37(상단 공지) · L386(논술형 2 경고 블록) · L404(갑 판정 bullet) · L470(풀이 1단계) · L508(부록) · L514(회차 회고) — Coder 주장 5지점 전수 실재(+1 bonus L508) | ✅ PASS |
| 8 | 자기검증 Step 1 영어 bare-paren 역grep + Greek/Cyrillic 확장 + Step 2 TitleCase + `### 채점 기준` 6건 | `### 채점 기준` 6건 OK, Step 2 TitleCase 11 phrase 전수 coverage hit≥1, Greek/Cyrillic 0건, **Step 1 bare-paren 0-hit 2건**(표 C) | ❌ **FAIL (bug)** |

## 표 A — verbatim byte-level 샘플 (항목 3 근거)

coverage/2015-B.md 역grep (`LC_ALL=C.UTF-8 grep -Fc`):

| 문항 | 샘플 문장 | coverage hit | study-guide hit | 판정 |
|------|----------|-------------|-----------------|------|
| 서1 | `4가지 요소가 '4구성 요소 모델'을 이룹니다` | 1 | 1 | ✅ |
| 서2 | `의(義)와 도(道)가 배합된 것이다` | 1 | 1 | ✅ |
| 서2 | `기(氣)는 텅 비어서 무엇이든 받아들이려 기다린다` | 2 | 2 | ✅ |
| 서3 | `문제는 그들이 고통을 느낄 수 있는가이다` | 2 | 3 | ✅ |
| 서3 | `자연의 과정에서 인간이 사용하도록 운명으로 결정되었기 때문이다` | 1 | 1 | ✅ |
| 서4 | `통설의 의미가 퇴색되어 사람들에게 영향을 미치지 못하게 될 것이기 때문이다` | 1 | 1 | ✅ |
| 논1 | `비사회적인 존재를 사회적인 존재로 만드는 과정이다` | 1 | 1 | ✅ |
| 논2 | `어찌 이발(理發)과 기발(氣發)의 구분이 있겠는가` | 2 | 1 | ✅ |

**HTML `<u>...</u>` 태그 보존 (4쌍)**: study-guide 에 raw `<u>` 4건 / `</u>` 4건 실재 (L221/L285/L394/L396). coverage 는 raw `<u>` 2쌍 (L18 ㉠원리 bold 변이, L20 인심/도심) — 나머지 2개(L17 나누자형 ㉠원리, L19 논술형 1 말미 내가 보기에)는 coverage row cell 에서 `<u>` 무포장 인용. 밑줄 *내용* 자체는 coverage 에 전수 실재 (`㉠원리`=2, `내가 보기에 4단계의 관점` hit=1). **HTML `<u>` 태그 보존 판정 PASS**(원문 체계를 지키고 있으며 coverage row cell 포매팅 차이에 기인한 `<u>` 래퍼 차이는 본문 의미 왜곡 아님).

한자 병기 보존: `(義)`·`(道)`·`(氣)`·`(理發)`·`(氣發)`·`(人心)`·`(道心)`·`(人欲)`·`(末流)`·`(形氣)`·`(物欲)`·`(情)`·`(道義)`·`(口體)`·`(理氣)`·`(性命)`·`(變稱)` 등 전수 보존. ㉠·㉡·㉢ 특수 기호 전수 보존.

## 표 B — thinker_id 전수 ES 재조회 (항목 4 근거)

`curl -s http://localhost:9200/ethics-thinkers/_doc/{id}` 본 세션 실측:

| thinker_id | found |
|------------|-------|
| rest | True |
| mencius | True |
| zhuangzi | True |
| singer | True |
| aquinas | True |
| mill_js | True |
| durkheim | True |
| piaget | True |
| kohlberg | True |
| yihwang | True |
| yiyulgok | True |

11/11 전수 `found=True`. TASK-DQ-007 override 이후 singer·durkheim 등록 상태 재확인.

## 표 C — Step 1 bare-paren 역grep (항목 8 FAIL 근거)

`LC_ALL=C.UTF-8 grep -oE '\([A-Za-z][^)]*\)' study-guide/2015-B.md | sort -u` 추출 → 유의미 토큰(메타 레이블·줄번호·TASK ID·id 단독 제외) 21종. coverage 역grep 결과:

| bare-paren 토큰 | coverage hit | 판정 |
|-----------------|-------------|------|
| `(Animal Liberation, 1975)` | 1 | ✅ |
| `(J. Rest)` | 1 | ✅ |
| `(Jean Piaget)` | 1 | ✅ |
| `(John Stuart Mill)` | 1 | ✅ |
| `(L'Éducation morale, 1902-03)` | 1 | ✅ |
| `(Lawrence Kohlberg)` | 1 | ✅ |
| `(Le Jugement moral chez l'enfant, 1932)` | 1 | ✅ |
| `(On Liberty, 1859)` | 1 | ✅ |
| `(Peter Singer)` | 1 | ✅ |
| `(Summa Theologiae)` | 1 | ✅ |
| `(Summa contra Gentiles)` | 1 | ✅ |
| `(The Philosophy of Moral Development, 1981)` | 1 | ✅ |
| `(Thomas Aquinas)` | 1 | ✅ |
| `(dead dogma)` | 1 | ✅ |
| `(harm principle)` | 1 | ✅ |
| `(living truth)` | 1 | ✅ |
| `(other-regarding)` | 1 | ✅ |
| `(self-regarding)` | 1 | ✅ |
| `(speciesism)` | 1 | ✅ |
| `(Émile Durkheim)` | 1 | ✅ |
| **`(moral character / implementation)`** | **0** | ❌ **bug** |
| **`(moral motivation)`** | **0** | ❌ **bug** |

**원인 분석**: coverage L15 에는 `도덕적 동기(道德的 動機 — moral motivation)` · `도덕적 실행력(道德的 實行力 — moral character / implementation)` 형태로 **한자+em-dash 래퍼 뒤 English** 가 존재하나, Coder 는 study-guide L92/L94 에서 `도덕적 동기(moral motivation)` · `도덕적 실행력(moral character / implementation)` 와 같이 **한자 래퍼를 제거하고 English 만 bare-paren 으로 축약 재포장**했다. English 용어 자체는 coverage 에 실재하나(`grep -Fc "moral motivation"` = 1, `grep -Fc "moral character / implementation"` = 1), bare-paren 토큰 byte-level 일치는 실패.

**TASK-184-FIX 선례 (동일 bracket-style 누수 bug 판정)와 동급 — severity=bug**.

## Greek/Cyrillic 확장 실측 (Task spec 별도 확증 요구)

```bash
LANG=ko_KR.UTF-8 LC_ALL=ko_KR.UTF-8 grep -oE '\([^)]*[α-ωΑ-Ωа-яА-Я][^)]*\)' study-guide/2015-B.md
```

결과: **0건** ✅

2015-B 는 서양 4인(Rest · Singer · Aquinas · Mill) + 동양 4인(Mencius · Zhuangzi · Yihwang · Yiyulgok) + 도덕교육 이론가 3인(Durkheim · Piaget · Kohlberg) 조합으로 Greek/Cyrillic 출현 여지 자체가 없는 회차. TASK-184-FIX 에서 도입된 Greek/Cyrillic 확장 정규식이 후속 회차에서도 **자동 0-hit 로 안정적 미발동** 하는 것이 최초로 확증되어 규약 연속성 확보. 향후 회차(예: 2016-A 등)에 sociology·psychology thinker(베버·프로이드 등) 추가 시 발동 가능성 있음.

## Step 2 TitleCase phrase 전수 역grep (항목 8 일부)

`LC_ALL=C.UTF-8 grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}' study-guide/2015-B.md | sort -u` → 11 phrase. coverage hit 전수:

| phrase | coverage hit |
|--------|-------------|
| `Animal Liberation` | 1 |
| `Jean Piaget` | 2 |
| `John Stuart Mill` | 2 |
| `Lawrence Kohlberg` | 2 |
| `Le Jugement moral chez` | 1 |
| `On Liberty` | 1 |
| `Peter Singer` | 4 |
| `Summa Theologiae` | 1 |
| `Summa contra Gentiles` | 1 |
| `The Philosophy of Moral Development` | 1 |
| `Thomas Aquinas` | 2 |

11/11 전수 coverage 실재 ✅

## 채점 기준 서브섹션 6건 확증 (항목 8 일부)

`grep -c '^### 채점 기준' study-guide/2015-B.md` == **6** ✅ (서술형 1~4 + 논술형 1~2)

## 이슈/블로커

### bug #1 — bare-paren 재포장으로 인한 원문-grep 0-hit 2건

**대상 파일**: `projects/ethics-study/exam-solutions/study-guide/2015-B.md`

**위치**:
- L92 (서술형 1 풀이 과정 2단계): `도덕적 동기(moral motivation)는 ...`
- L94 (서술형 1 풀이 과정 4단계): `도덕적 실행력(moral character / implementation)의 훈련 영역 ...`

**원인**: coverage/2015-B.md L15 의 "도덕적 동기(道德的 動機 — moral motivation)" / "도덕적 실행력(道德的 實行力 — moral character / implementation)" 에서 한자+em-dash 래퍼를 제거하고 bare-paren English 만 남긴 재포장. 축약의 의도는 선해하나, agents/tester.md "문서·해설 성격 산출물 검증 — 원문-grep 대조 표준" 및 coder.md 자기검증 2단계 프로토콜은 bare-paren 토큰의 coverage byte-level 일치를 요구한다.

**재현 grep 명령**:
```bash
grep -Fc '(moral motivation)' coverage/2015-B.md          # 기대 ≥1, 실측 0
grep -Fc '(moral character / implementation)' coverage/2015-B.md  # 기대 ≥1, 실측 0
```

**예상 교정안** (Coder FIX 태스크 권장):

- 옵션 A(coverage 완전 일치 복원): study-guide L92/L94 를 각각
  - `도덕적 동기(道德的 動機 — moral motivation)는 ...`
  - `도덕적 실행력(道德的 實行力 — moral character / implementation)의 훈련 영역 ...`
- 옵션 B(bare-paren 유지 + 한글 병기 강화): `도덕적 동기(도덕적 동기)`처럼 중복 한글화는 무의미하므로, bare-paren 을 한자 래퍼로 복원하는 옵션 A 가 유일하게 합리적.

**TASK-184-FIX 선례 정합성**: 동일 성격(English 재포장으로 bare-paren 누수)으로 FIX 승격되었음. 본 건도 동등 처리 권장.

### observation #1 — Manager spec vs 실측 line count 불일치

Manager task spec: "529 lines". `wc -l` 실측: **516 lines**. byte 일치 (62914). Line count 불일치는 Coder self-report 의 `(신규, 62914 byte, 529 lines)` 주장이 wc -l 기준이 아닌 내부 카운트(?) 에 근거한 것으로 추정. 실측 라인 수가 소폭 적은 것이므로 내용 누락 risk 는 없으나, Manager 가 spec 에 기재한 수치와 실측 차이는 execution-log 감사 가치. severity=observation.

## 다음 제안

1. **Manager**: severity=bug 규정에 따라 bare-paren 2건 FIX 태스크 1건을 `task-board.md` 에 자동 등록. TASK-185-FIX-1 등 prefix 권장. 파일 1개·편집 2곳이므로 소형 태스크.
2. **Coder (FIX 진행 시)**: 옵션 A(한자+em-dash 래퍼 복원) 적용 후 Step 1 bare-paren 0-hit 0건 재grep 확증 + 본 tester-report 의 8항 표 동일 수치 재확인.
3. **Reviewer (FIX Reviewer Round)**: bare-paren FIX 와 Greek/Cyrillic 확장 0건 유지(회귀 없음) 두 가지만 집중 확인.
4. **관찰 사항 — Greek/Cyrillic 확장 규약 연속성**: TASK-184-FIX 도입 후 첫 후속 회차(2015-B)에서 0-hit 자동 유지. 규약은 정상 작동하나, sociology/psychology 사상가(Weber · Freud 등) 등장 회차에서는 발동할 것이므로 향후 관찰 지속 권장.
