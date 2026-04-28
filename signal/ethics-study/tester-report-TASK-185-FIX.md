---
agent: tester
task_id: TASK-185-T-R2
status: DONE
timestamp: 2026-04-22T00:30:00
verdict: PASS
severity: none
---

## 결과 요약

`projects/ethics-study/exam-solutions/study-guide/2015-B.md` (TASK-185-FIX 적용 후, 실측 **516 lines**) 에 대해 FIX 재검증 5항 전수 수행. **5/5 PASS · item 8 bare-paren 2건 해소 확증 · 회귀 0건**.

- item 1~3 (새 토큰 target/coverage hit): 6/6 hit=1 전수 통과
- item 4 (bare-paren `(moral motivation)` / `(moral character / implementation)` 잔존 0): 2/2 exact-match count=0 전수 통과
- item 5 (Step 1 자기검증 재실행 회귀 체크): R1 유의미 concept 토큰 20종 coverage hit 전수 재통과, 신규 concept-term 0-hit 0건, Greek/Cyrillic 확장 0건 유지
- em-dash U+2014 (`e2 80 94`) byte 검증: L92·L94 두 래퍼 모두 hexdump 로 정확 확증
- 파일 line 수 516 (R1 과 동일) · 구조 header count 6/6 · `### 채점 기준` 6건 유지 — 회귀 없음

R1 FAIL 근거였던 bare-paren 2건이 정확히 교정되었고 주변 구조·샘플 문장에 회귀가 없어 **severity=none · verdict=PASS**.

## 변경된 파일

없음 (검증 전용).

## 재검증 5항 결과 표

| # | 체크 항목 | 명령 | 기대 | 실측 | 판정 |
|---|----------|------|------|------|------|
| 1 | 새 토큰 target hit `(道德的 動機 — moral motivation)` | `LC_ALL=C.UTF-8 grep -Fc '(道德的 動機 — moral motivation)' study-guide/2015-B.md` | ≥1 | **1** (L92) | ✅ |
| 2 | 새 토큰 coverage hit `(道德的 動機 — moral motivation)` | `LC_ALL=C.UTF-8 grep -Fc '(道德的 動機 — moral motivation)' coverage/2015-B.md` | ≥1 | **1** (L15) | ✅ |
| 3a | 새 토큰 target hit `(道德的 實行力 — moral character / implementation)` | `LC_ALL=C.UTF-8 grep -Fc '(道德的 實行力 — moral character / implementation)' study-guide/2015-B.md` | ≥1 | **1** (L94) | ✅ |
| 3b | 새 토큰 coverage hit `(道德的 實行力 — moral character / implementation)` | `LC_ALL=C.UTF-8 grep -Fc '(道德的 實行力 — moral character / implementation)' coverage/2015-B.md` | ≥1 | **1** (L15) | ✅ |
| 4a | bare-paren `(moral motivation)` exact-match 잔존 | `grep -oE '\([A-Za-z][^)]*\)' study-guide/2015-B.md \| grep -Fx '(moral motivation)' \| wc -l` | 0 | **0** | ✅ |
| 4b | bare-paren `(moral character / implementation)` exact-match 잔존 | `grep -oE '\([A-Za-z][^)]*\)' study-guide/2015-B.md \| grep -Fx '(moral character / implementation)' \| wc -l` | 0 | **0** | ✅ |
| 5 | Step 1 자기검증 재실행 회귀 | (아래 표 D 참조) | R1 concept 20종 hit 유지 + 신규 concept 0-hit 0 | 20/20 유지, 신규 0-hit 0 | ✅ |

## 표 D — Step 1 자기검증 재실행 상세 (item 5 근거)

### (1) bare-paren 영어 토큰 전수 추출

`LC_ALL=C.UTF-8 grep -oE '\([A-Za-z][^)]*\)' study-guide/2015-B.md | sort -u` → **unique 40종**.
coverage 역grep 결과:

- **0-hit 토큰 17종** — 전수 구조/메타 레이블 (R1 에서도 "유의미 토큰" 제외 규칙에 해당):
  - 알파벳 라벨 (7): `(A)`, `(A-①)`, `(A-②)`, `(B)`, `(B-①)`, `(B-②)`, `(C)`, `(a)`, `(b)`, `(c)`, `(d)` (실제 11건)
  - 파일/줄번호 참조 (3): `(L1~L206)`, `(coverage/2015-B.md L176~L180 근거)`, `(coverage/2015-B.md L182~L186 + TASK-DQ-007 override 반영)`
  - TASK ID 참조 (2): `(TASK-183 산출물)`, `(TASK-184 산출물)`
  - thinker_id 리스트 (1): `(rest · mencius · zhuangzi · singer · aquinas · mill_js · durkheim · piaget · kohlberg · yihwang · yiyulgok 모두 ✅ ES 등록 확인)`
- **concept 토큰 0-hit**: **0건** (R1 FAIL 2건 모두 해소, 신규 0건) ✅

### (2) R1 유의미 concept 토큰 20종 회귀 재검증

R1 표 C "유의미 토큰 21종" 중 FAIL 2건을 제외한 PASS 20종 전수 재grep:

| concept 토큰 | study-guide hit | coverage hit | 판정 |
|--------------|----------------|--------------|------|
| `(Animal Liberation, 1975)` | 1 | 1 | ✅ |
| `(J. Rest)` | 4 | 1 | ✅ |
| `(Jean Piaget)` | 1 | 1 | ✅ |
| `(John Stuart Mill)` | 1 | 1 | ✅ |
| `(L'Éducation morale, 1902-03)` | 1 | 1 | ✅ |
| `(Lawrence Kohlberg)` | 1 | 1 | ✅ |
| `(Le Jugement moral chez l'enfant, 1932)` | 1 | 1 | ✅ |
| `(On Liberty, 1859)` | 1 | 1 | ✅ |
| `(Peter Singer)` | 1 | 1 | ✅ |
| `(Summa Theologiae)` | 1 | 1 | ✅ |
| `(Summa contra Gentiles)` | 1 | 1 | ✅ |
| `(The Philosophy of Moral Development, 1981)` | 1 | 1 | ✅ |
| `(Thomas Aquinas)` | 1 | 1 | ✅ |
| `(dead dogma)` | 1 | 1 | ✅ |
| `(harm principle)` | 1 | 1 | ✅ |
| `(living truth)` | 1 | 1 | ✅ |
| `(other-regarding)` | 1 | 1 | ✅ |
| `(self-regarding)` | 1 | 1 | ✅ |
| `(speciesism)` | 1 | 1 | ✅ |
| `(Émile Durkheim)` | 1 | 1 | ✅ |

**20/20 전수 유지** ✅ (회귀 없음).

### (3) 신규 concept-term 0-hit

FIX 반영 후 새로 등장한 concept 토큰은 `(道德的 動機 — moral motivation)`, `(道德的 實行力 — moral character / implementation)` 2종이며, 둘 다 coverage hit=1 (item 2·3b). **신규 0-hit 0건** ✅

## em-dash byte 검증 (U+2014 = `E2 80 94`)

### L92 래퍼 hexdump (발췌)

```
00000050  eb 8f 99 ea b8 b0 28 e9  81 93 e5 be b7 e7 9a 84  |......(.........|
00000060  20 e5 8b 95 e6 a9 9f 20  e2 80 94 20 6d 6f 72 61  | ...... ... mora|
00000070  6c 20 6d 6f 74 69 76 61  74 69 6f 6e 29 eb 8a 94  |l motivation)...|
```

`(` 뒤 → `道(e9 81 93) 德(e5 be b7) 的(e7 9a 84) space 動(e5 8b 95) 機(e6 a9 9f) space` **`e2 80 94`**(em-dash) `space moral motivation) …` — **em-dash byte 정확** ✅

### L94 래퍼 hexdump (발췌)

```
00000010  8b a4 ed 96 89 eb a0 a5  28 e9 81 93 e5 be b7 e7  |........(.......|
00000020  9a 84 20 e5 af a6 e8 a1  8c e5 8a 9b 20 e2 80 94  |.. ......... ...|
00000030  20 6d 6f 72 61 6c 20 63  68 61 72 61 63 74 65 72  | moral character|
00000040  20 2f 20 69 6d 70 6c 65  6d 65 6e 74 61 74 69 6f  | / implementatio|
00000050  6e 29 ec 9d 98 20 ed 9b  88 eb a0 a8 20 ec 98 81  |n)... ...... ...|
```

`(` 뒤 → `道(e9 81 93) 德(e5 be b7) 的(e7 9a 84) space 實(e5 af a6) 行(e8 a1 8c) 力(e5 8a 9b) space` **`e2 80 94`**(em-dash) `space moral character / implementation) …` — **em-dash byte 정확** ✅

hyphen-minus `-` (`0x2d`) 아닌 정확한 U+2014 em-dash 사용 확증. coverage L15 원문 byte 복사 재현성 성립.

## 회귀 샘플링 (observation 레벨)

- **파일 line 수**: `wc -l study-guide/2015-B.md` == **516** (R1 과 동일) — Coder 의 2-line in-place edit 완전 일치 ✅
- **verbatim 샘플 spot-check (R1 표 A 중 2건)**:
  - `의(義)와 도(道)가 배합된 것이다` — SG=1, CV=1 (R1 실측 동일) ✅
  - `문제는 그들이 고통을 느낄 수 있는가이다` — SG=3, CV=2 (R1 실측 3/2 동일) ✅
- **구조 헤더 회귀**:
  - `^## 문항` 카운트 = **6** (R1 동일) ✅
  - `^### 채점 기준` 카운트 = **6** (R1 동일) ✅
- **Greek/Cyrillic 확장 정규식 연속성**: `LANG=ko_KR.UTF-8 LC_ALL=ko_KR.UTF-8 grep -cE '\([^)]*[α-ωΑ-Ωа-яА-Я][^)]*\)' study-guide/2015-B.md` == **0** (R1 동일; TASK-184-FIX 도입 규약 연속 stability 2회차 확증) ✅

전수 regression 0건.

## Greek/Cyrillic 확장 규약 연속성 관찰

TASK-184-FIX 에서 도입된 `(` + Greek(α-ωΑ-Ω) / Cyrillic(а-яА-Я) + `)` 패턴 0-hit 확증이 2015-B 에서 R1 에 이어 R2(본 회차)에서도 **자동 0건 유지**. 2015-B 의 사상가 셋(서양 4인 · 동양 4인 · 도덕교육 이론가 3인)은 모두 Greek/Cyrillic 출현 여지 없는 조합. 규약 자체는 발동 없이 연속 stability 유지 중이며, 향후 sociology·psychology 사상가(예: Weber · Freud · Vygotsky) 등장 회차에서 first-activation 이 기대된다. 발동 0건 — observation 없음.

## 이슈/블로커

없음. R1 FAIL 근거(bare-paren 2건)가 정확히 해소되었고 회귀 0건이다.

## 다음 제안

1. **Manager**: TASK-185-FIX 를 DONE 처리, done-log 적재, TASK-185 전체 완료. 2015-B 회차 마감.
2. **후속 회차 적용**: Coder 자기검증 2단계 프로토콜(bare-paren 영어 토큰 전수 coverage 역grep)이 TASK-184-FIX · TASK-185-FIX 에서 2회 연속 bug 근본 차단에 성공. 향후 2015-A · 2016-A 등 미작성 회차에서 동일 프로토콜 표준 적용 권장. Manager task spec 에 "bare-paren 영어 토큰 전수 `grep -oE '\([A-Za-z][^)]*\)'` 후 coverage 역grep 0-hit 0건 확증" 을 명시적 완료 조건으로 기입 가능.
3. **em-dash U+2014 byte 보존**: 2015-B 에서 `(한자 — English)` 래퍼 4건(coverage L15 의 민감성·판단·동기·실행력) 중 study-guide L92/L94 에 동기·실행력 2건 전수 올바르게 복원됨. 향후 민감성·판단 관련 풀이 부분(L88~L91 부근)에 같은 래퍼가 등장할 경우에도 em-dash U+2014 byte 정확 준수 요청. 확인 명령 템플릿: `hexdump -C file.md | grep -A1 'e2 80 94'`.
