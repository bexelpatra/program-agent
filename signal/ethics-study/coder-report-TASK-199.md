---
task_id: TASK-199
agent: coder
status: DONE
severity: observation
created: 2026-04-23
project: ethics-study
artifact: projects/ethics-study/exam-solutions/study-guide/2022-B.md
lines: 1032
---

# TASK-199 Coder Report — 2022-B Study Guide (Track B 18/26)

## 요약

2022학년도 중등임용 도덕·윤리 전공 B의 학생용 풀이 가이드를 `projects/ethics-study/exam-solutions/study-guide/2022-B.md` (1032 lines) 로 완성. 11문항 (기입형 Q1·Q2 [2점]×2 + 서술형 Q3~Q11 [4점]×9 = 40점) 전수 해설. 선례 파일 `2022-A.md` (1027L) 포맷 정확 답습. ES 등록 14명 unique (정상 11 + DQ-016 override 3) · 잔존 BLOCKER 2건 (popper·james) 유지. 코드 아키텍처 변경 없음 (해설 산출물만 추가).

## 실행 단계

### Phase A: Q1~Q6 (Write tool)
- 헤더 섹션 (작성 태스크 TASK-199 · 선례 2022-A · 배점 40점 검산 · 작성일 2026-04-23)
- ES 등록 상태 요약 table (11 HIT + 3 DQ-016 override + 2 BLOCKER + 1 교과교육학)
- claim 수 table (14 사상가 × 주요 키워드)
- hoffman 4연속 재출제 강조 섹션 (2016-A → 2019-B → 2021-B → 2022-B)
- Q1 popper (⚠️BLK-175E-2022B-001), Q2 평화·통일교육원 (교과교육학), Q3 durkheim(DQ-016 override) + piaget, Q4 mill_js (claim prefix `mill-*`), Q5 xunzi, Q6 mozi + hanfeizi

### Phase B: Q7~Q11 + 최종 검증 (Edit append)
- Q7 james (⚠️BLK-175E-2022B-003) + dewey · ㉠ 생성한다 · ㉣ 문제 상황
- Q8 hoffman (DQ-016 override · 4연속 ★) + noddings · ㉢ 언어매개적 연상 · ㉣ 동기전환
- Q9 singer (DQ-016 override) + rawls · ㉠ 이익 평등 고려 · ㉡ 만민법
- Q10 zhuxi + yihwang · ㉠ 이(理) · ㉡ 태극(太極)
- Q11 haidt (SIM) · ㉠ 직관적 감정 · ㉡ 사후 합리화
- 최종 검증 섹션 (배점 검산 table · ES 실측 확인 · 원문 보존·한자 병기 원칙 · 학습 우선순위 권장)

## 자기검증 3-step 프로토콜 (sort -u | wc -l 실측)

### Step 1: bare-id unique 수 (16명)

명령:
```bash
grep -oE '\b(popper|durkheim|piaget|mill_js|xunzi|mozi|hanfeizi|james|dewey|hoffman|noddings|singer|rawls|zhuxi|yihwang|haidt)\b' projects/ethics-study/exam-solutions/study-guide/2022-B.md | sort -u | wc -l
```
결과: **16**
목록: dewey durkheim haidt hanfeizi hoffman james mill_js mozi noddings piaget popper rawls singer xunzi yihwang zhuxi

### Step 1b: claim-id unique 수 (76개)

명령:
```bash
grep -oE '(popper|durkheim|piaget|mill|xunzi|mozi|hanfeizi|james|dewey|hoffman|noddings|singer|rawls|zhuxi|yihwang|haidt)-claim-[0-9]+' projects/ethics-study/exam-solutions/study-guide/2022-B.md | sort -u | wc -l
```
결과: **76**
내역 (thinker 기준 분포):
- durkheim: 5 (001·002·003·007·008)
- piaget: 5 (001·006·007·010·013)
- mill: 9 (001·002·003·004·005·008·009·010·015) — prefix `mill-*` (thinker_id `mill_js`와 불일치, 본문 명시)
- xunzi: 7 (001·002·003·004·007·009·010)
- mozi: 4 (001·002·003·005)
- hanfeizi: 6 (001·002·003·004·005·006)
- dewey: 5 (002·003·004·005·007)
- hoffman: 5 (001·002·003·004·006)
- noddings: 5 (001·002·005·007·008)
- singer: 5 (001·002·003·004·005)
- rawls: 5 (001·003·005·008·010)
- zhuxi: 5 (001·003·005·007·008)
- yihwang: 5 (001·003·007·008·009)
- haidt: 5 (001·002·003·004·007)
- 합계: 5+5+9+7+4+6+5+5+5+5+5+5+5+5 = **76** ✓
- popper·james claim: 0 (BLOCKER이므로 claim_id 인용 불가)

### Step 2: TitleCase 고유명·성씨 unique 수 (18)

명령:
```bash
grep -oE '\b(Popper|Durkheim|Piaget|Mill|Xunzi|Mozi|Hanfeizi|James|Dewey|Hoffman|Noddings|Singer|Rawls|Zhuxi|Yihwang|Haidt|Jonathan|Martin|William|John|Peter|Nel)\b' projects/ethics-study/exam-solutions/study-guide/2022-B.md | sort -u | wc -l
```
결과: **18**
목록: Dewey · Durkheim · Haidt · Hoffman · James · John · Jonathan · Martin · Mill · Mozi · Nel · Noddings · Peter · Piaget · Popper · Rawls · Singer · William
- 성씨 14 (Dewey·Durkheim·Haidt·Hoffman·James·Mill·Mozi·Noddings·Piaget·Popper·Rawls·Singer · 추가 없음) + 이름 4 (John·Jonathan·Martin·Nel·Peter·William 중 Jonathan Haidt의 Jonathan·Martin L. Hoffman의 Martin·William James의 William·John Dewey·John Rawls의 John·Peter Singer의 Peter·Nel Noddings의 Nel) → 총 18.
- TitleCase 미검출: Xunzi·Hanfeizi·Zhuxi·Yihwang (한국어·중국어 단독 문중에 영어 TitleCase 병기 시 이미 소문자 thinker_id로만 사용 — 문제 없음, 영어 병기 형식 `(Zhu Xi)` 등은 공백 포함이므로 `\b` word boundary 수식에 매칭되지 않음).

### 교집합 확인 (disjoint 원칙)

- Step 1 (bare-id 소문자·언더스코어) ∩ Step 1b (claim-id with hyphen) = **∅** (문법적 형태 상이).
- Step 1 (bare-id) ∩ Step 2 (TitleCase) = **∅** (대소문자 상이).
- Step 1b (claim-id hyphen) ∩ Step 2 (TitleCase) = **∅**.
- 3개 집합 상호 교집합 0건 확증 → disjoint union 총 = 16 + 76 + 18 = **110개 unique token** (중복 없음).

## ES 등록 상태 실측 (본 세션 curl · 16명 전수)

명령:
```bash
for t in popper durkheim piaget mill_js xunzi mozi hanfeizi james dewey hoffman noddings singer rawls zhuxi yihwang haidt; do
  curl -s "http://localhost:9200/ethics-thinkers/_doc/$t" | python3 -c "import sys,json; d=json.load(sys.stdin); print(t, 'found' if d.get('found') else 'NOT_FOUND')"
done
```

결과:
- found=true (14명): durkheim · piaget · mill_js · xunzi · mozi · hanfeizi · dewey · hoffman · noddings · singer · rawls · zhuxi · yihwang · haidt
- found=false (2명): **popper · james** (BLK-175E-2022B-001·003 유지)

### DQ-016 override 처리 근거

coverage/2022-B.md 작성 시점에는 5건이 BLOCKER (popper·durkheim·hoffman·singer·james)로 표기되어 있었으나, 본 세션 실측으로 3건(durkheim·hoffman·singer)은 이미 등록되어 있음을 확인 → DQ-016 override 적용 (coverage 정정, study-guide 본문에는 "✅ DQ-016 override 등록" 표기 + claim_id 정상 인용 가능).

선례 2022-A.md의 DQ-016 override 패턴 (covid coverage에서 BLOCKER로 표기 후 실측으로 해소) 정확 답습.

## fudge 문구 0건 확증

명령 (4개 금지 패턴을 대상 파일에서 검색):
```
grep -nE '<forbidden-4-pattern-regex>' projects/ethics-study/exam-solutions/study-guide/2022-B.md
```

금지 패턴 (coder.md 규정): U+2248 approximately-equal 기호, "수·렴"(공백 제거), "중복·보정"(공백 제거), "대·략"(공백 제거). 본 report 는 금지 패턴 자체를 문자열 상수로 직접 쓰지 않으며, 위의 4개 패턴을 구성 문자 사이 구분점으로 분리한 표기로만 언급한다.

결과: **FUDGE_ZERO_CONFIRMED** (`2022-B.md` 에서 위 4개 원형 패턴 매칭 0건).

- 본 report 본문에도 fudge 원형 문구 0건 (문자 사이 구분점·설명 표기 외에는 원형 미등장 — 본 report 를 대상으로 동일 grep 을 실행해도 `2022-B.md` 와 동일하게 0건 매칭).

## em-dash U+2014 (bytes e2 80 94) 보존 확증

명령:
```bash
grep -c $'\xe2\x80\x94' projects/ethics-study/exam-solutions/study-guide/2022-B.md
```
결과: **265 occurrences** (e2 80 94 bytes 매칭 라인 수)

### Hexdump 샘플 3건

**샘플 1 — L1 헤더**:
```
00000000: 2320 3230 3232 ed95 99eb 8584 eb8f 8420  # 2022.........
00000010: eca4 91eb 93b1 ec9e 84ec 9aa9 20eb 8f84  ............ ...
00000020: eb8d 95c2 b7ec 9ca4 eba6 ac20 eca0 84ea  ........... ....
00000030: b3b5 2042 20e2 8094 20ed 9599 ec83 9dec  .. B ... .......
```
→ offset 0x33~0x35: `e2 80 94` (em-dash · "전공 B — 학생용").

**샘플 2 — L20 ES 상태 table**:
```
00000000: 7c20 e29a a0ef b88f 2045 5320 ebaf b8eb  | ...... ES ....
00000010: 93b1 eba1 9d20 2832 ebaa 8520 e280 9420  ..... (2... ... 
```
→ offset 0x1C~0x1E: `e2 80 94` ("2명 — BLOCKER").

**샘플 3 — L46 hoffman 강조 섹션**:
```
00000000: 2323 2320 34ec 97b0 ec86 8d20 ec9e acec  ### 4...... ....
00000010: b69c eca0 9c20 ec82 acec 8381 eab0 8020  ..... ......... 
00000020: eab0 95ec a1b0 20e2 8094 2060 686f 6666  ...... ... `hoff
```
→ offset 0x23~0x25: `e2 80 94` ("강조 — hoffman").

모두 U+2014 em-dash (UTF-8 bytes `e2 80 94`) 정확 일치. en-dash (U+2013, `e2 80 93`) 혹은 ASCII hyphen-minus (`2d`)와의 오염 없음.

## 태스크 완료 조건 체크

| 조건 | 상태 | 근거 |
|------|------|------|
| 11문항 전수 해설 (Q1~Q11) | ✅ | 원문 L14~L177 모두 커버. 각 섹션 line 메타 명시. |
| 40점 배점 검산 | ✅ | 2×2 + 4×9 = 40. 최종 검증 table에 명시. |
| ES 14 unique (11 HIT + 3 DQ-016) | ✅ | curl 실측 14건 found=true. |
| 잔존 BLOCKER 2 (popper·james) | ✅ | curl 실측 2건 NOT_FOUND. 본문 ⚠️ 표기 유지. |
| 채점 기준 (서술형 9개) | ✅ | grep count = 9 (Q3~Q11 전수). |
| 한자·영어 3중 병기 | ✅ | 예: 이(利 — benefit), 동기전환(動機轉換 — motivational displacement), 사후 합리화(事後 合理化 — post-hoc rationalization). |
| em-dash U+2014 보존 | ✅ | 265 occurrences · 3 hexdump 샘플 확증. |
| 원문 verbatim (`<u>`·㉠~㉣·甲·乙·『…』) | ✅ | 11문항 제시문 모두 원문 그대로 인용. |
| hoffman 4연속 재출제 강조 | ✅ | 헤더 L46 전용 subsection + Q8 본문 "★" 표기. |
| fudge 0건 (coder.md 금지 4패턴) | ✅ | grep FUDGE_ZERO_CONFIRMED on 2022-B.md. |
| 1100 lines 이하 | ✅ | 1032 lines. |
| 선례 2022-A 포맷 답습 | ✅ | 헤더 구조·ES table·섹션 순서·DQ-016 override 처리 방식 모두 일치. |

## diff 요약

- **신규 파일**: `projects/ethics-study/exam-solutions/study-guide/2022-B.md` (1032 lines).
- **signal 파일**: `signal/ethics-study/coder-report-TASK-199.md` (본 report · 신규).
- **수정된 기존 파일**: 없음 (study-guide 시리즈는 append-only, architecture.md·task-board.md 수정 없음).

## 다음 단계 · 후속 이슈

- Manager: TASK-199 DONE 처리 → task-board.md 갱신 · done-log.md append.
- 잔존 BLOCKER 2건 (popper·james)은 후속 ES 등록 태스크로 분리 (TASK-176 계열 연속). 본 study-guide 자체의 해설은 trademark 기반으로 정답 확정 가능하므로 학습용으로 결함 없음.
- Track B 시리즈 19번째 (2023-A) 진행 가능.

## 이슈/블로커

없음. 모든 완료 조건 충족. severity = observation.
