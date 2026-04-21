---
agent: coder
task_id: TASK-175E-2022-B
status: DONE
timestamp: 2026-04-21T15:30:00+09:00
---

## 결과 요약
- **문항**: 11문항 40점 (기입형 Q1·Q2 [2점]×2 = 4점 + 서술형 Q3~Q11 [4점]×9 = 36점). 원문 L7 "11문항 40점" 일치. 검산: 2×2 + 4×9 = 40 ✓
- **등장 사상가**: 총 13명(복수 출제 없음). `popper`(Q1) · [교과교육학](Q2) · `durkheim`+`piaget`(Q3) · `mill_js`(Q4) · `xunzi`(Q5) · `mozi`+`hanfeizi`(Q6) · `james`+`dewey`(Q7) · `hoffman`+`noddings`(Q8) · `singer`+`rawls`(Q9) · `zhuxi`+`yihwang`(Q10) · `haidt`(Q11).
- **ES 조회 집계**:
  - **HIT (11건)**: `piaget` · `mill_js` · `xunzi` · `mozi` · `hanfeizi` · `dewey` · `noddings` · `rawls` · `zhuxi` · `yihwang` · `haidt`.
  - **MISS (5건)**: `popper` · `durkheim` · `james` · `hoffman` · `singer` → 신규 BLK-175E-2022B-001~005 등록.
  - **N/A (1건)**: Q2는 교과교육학(통일교육원 『평화·통일교육: 방향과 관점』) — 사상가 지명이 아닌 공식 자료 기반 문항.
- **신규 블로커**: 5건 (BLK-175E-2022B-001 ~ BLK-175E-2022B-005).
- **재출제 블로커**: 3건 (durkheim 2연속·singer 2연속·hoffman **4연속** — 2016-A·2019-B·2021-B·2022-B).

## 변경된 파일
- `projects/ethics-study/exam-solutions/coverage/2022-B.md` **(신규 생성)** — 11문항 전수 원문 직독 + 3단계 확정 + row-by-row + ES 조회 + 한자 병기(230+ 건).
- `signal/ethics-study/blocker-log.md` **(append)**: BLK-175E-2022B-001 ~ BLK-175E-2022B-005 (5개 블로커, 기존 72건 → 77건).

## thinker_id 목록 및 ES 상태

| Q | 인물 (한글 / 영문 / thinker_id) | ES 상태 | 비고 |
|---|--------------------------------|---------|------|
| Q1 | 칼 포퍼 / Karl Popper / `popper` | **MISS** | BLK-175E-2022B-001 (신규) |
| Q2 | — [교과교육학: 평화·통일교육원 『방향과 관점』] | N/A | 사상가 지명 아님 |
| Q3 갑 | 에밀 뒤르켐 / Émile Durkheim / `durkheim` | **MISS** | BLK-175E-2022B-002 (재발 — 2021-B→2022-B 2연속) |
| Q3 을 | 장 피아제 / Jean Piaget / `piaget` | HIT | — |
| Q4 | 존 스튜어트 밀 / John Stuart Mill / `mill_js` | HIT | 이니셜 suffix 규약 준수 |
| Q5 | 순자 / Xunzi, 荀子 / `xunzi` | HIT | — |
| Q6 갑 | 묵자 / Mozi, 墨子 / `mozi` | HIT | — |
| Q6 을 | 한비자 / Han Feizi, 韓非子 / `hanfeizi` | HIT | — |
| Q7 갑 | 윌리엄 제임스 / William James / `james` | **MISS** | BLK-175E-2022B-003 (신규, `rest`=James Rest와 혼동 주의) |
| Q7 을 | 존 듀이 / John Dewey / `dewey` | HIT | — |
| Q8 갑 | 마틴 호프만 / Martin L. Hoffman / `hoffman` | **MISS** | BLK-175E-2022B-004 (**4연속 재발** — 2016-A·2019-B·2021-B·2022-B) |
| Q8 을 | 넬 나딩스 / Nel Noddings / `noddings` | HIT | — |
| Q9 갑 | 피터 싱어 / Peter Singer / `singer` | **MISS** | BLK-175E-2022B-005 (재발 — 2019-B→2022-B 2연속) |
| Q9 을 | 존 롤즈 / John Rawls / `rawls` | HIT | — |
| Q10 갑 | 주희·주자 / Zhu Xi, 朱熹 / `zhuxi` | HIT | `zhuxi == zhu_xi` 동일인 (architecture L485-486) |
| Q10 을 | 퇴계 이황 / Yi Hwang, 李滉 / `yihwang` | HIT | `yihwang == yi_hwang` 동일인; 인용부는 주돈이 원문이나 발문 "한국 윤리 사상가"로 을=이황 확정 |
| Q11 | 조너선 하이트 / Jonathan Haidt / `haidt` | HIT | — |

## 재출제 사상가 결과 (누적 경계 대상 3연속 확인)

**태스크 지시 "3연속 재출제 (최최우선 ES 재검증)" 대상**:
- **`jinul`** (2020-A/2021-B/2022-A 3연속): **2022-B 등장 여부 = 未등장 (0회)**. 2022-B 한국 윤리 사상 문항은 Q10 을 이황 단독으로 지눌 미출제. → **3연속에서 그침 (4연속 아님)**.
- **`turiel`** (2018-B/2021-B/2022-A 3연속): **2022-B 등장 여부 = 未등장 (0회)**. 2022-B 도덕심리학/도덕교육 문항(Q3 을 피아제·Q8 갑 호프만·Q11 하이트)에 튜리엘 미출제. → **3연속에서 그침 (4연속 아님)**.

**태스크 지시 "2연속 재출제" 대상**:
- **`pettit`** (2020-A/2022-A): 2022-B 未등장. 2022-B 서양 사회·정치철학은 Q1 포퍼·Q9 싱어·Q9 롤즈 — 페팃 미출제.
- **`blasi`** (2019-B/2021-A): 2022-B 未등장.
- **`hoffman`** (2019-B/2021-B): **2022-B Q8 갑 등장 확증 → 4연속 달성** (2016-A 포함하면 2016-A·2019-B·2021-B·2022-B). **최최우선 등록 대상** — BLK-175E-2022B-004.

**2022-B 신규 확인 2연속 재출제**:
- **`durkheim`** (2021-B→2022-B): Q3 갑. 도덕 교육 3요소·규율 정신·벌의 사회적 기능.
- **`singer`** (2019-B→2022-B): Q9 갑. 이익평등고려 원칙·해외 원조 의무(2019-B는 동물 해방).

## 이슈/블로커 (본 태스크 신규 등록 5건)

| BLK ID | 인물 (id) | 출제 위치 | 우선순위 | 재출제 선례 |
|--------|-----------|-----------|---------|-------------|
| BLK-175E-2022B-001 | 칼 포퍼 (`popper`) | Q1 유일 사상가 | 최우선 | 신규 |
| BLK-175E-2022B-002 | 에밀 뒤르켐 (`durkheim`) | Q3 갑 | **최우선** | **2021-B→2022-B 2연속** (BLK-175E-2021B-004 후속) |
| BLK-175E-2022B-003 | 윌리엄 제임스 (`james`) | Q7 갑 | 최우선 | 신규 (ES `rest`=James Rest와 이름 혼동 주의) |
| BLK-175E-2022B-004 | 마틴 호프만 (`hoffman`) | Q8 갑 | **최최우선** | **2016-A→2019-B→2021-B→2022-B 4연속** (BLK-175E-2016A-005·2019B-002·2021B-005 후속) |
| BLK-175E-2022B-005 | 피터 싱어 (`singer`) | Q9 갑 | **최우선** | **2019-B→2022-B 2연속** (BLK-175E-2019B-001 후속) |

## Phase 6 규칙 준수 확인 (architecture.md L523-L588)

1. **원문 직독**: 현 세션 내 `/home/jai/잡동사니/임용/md/2022_중등1차_도덕윤리_전공B.md` 전체 185 lines Read 완료.
2. **문제→제시문→사상가 3단계 확정**: 11문항 각 ①발문 독해 → ②제시문 trademark 추출(한자·원어·저서명·고유 용어) → ③사상가·분류 판정 + 근거 2~3구절 원문 복사 수행.
3. **한자+한글 병기**: 2022-B.md 내 한자-한글 병기 약 230+ 건. 한자 단독 노출 0건(원문 인용구 내부 한자는 원문 보존).
4. **불확실 처리**: Q10 을 인용부 주돈이(Zhou Dunyi) 원문 관련 HTML NOTE 주석 삽입 — 발문 "한국 윤리 사상가"에 의해 을=이황으로 확정하되 주돈이 ES 미등록 참고 기록.
5. **배치 크기**: 1회 호출 = 2022-B 단일 시험지 11문항 (규약 준수).
6. **thinker_id suffix 규약** (architecture L490-L492): `mill_js`(이니셜 suffix 유지) · `zhuxi == zhu_xi` · `yihwang == yi_hwang` 동일인 규약 준수. 동명이인 suffix 위반 0건(Paul Taylor·Charles Taylor·T.H. Green 등 미등장).

## 다음 제안
1. **Tester 검증**: row-by-row 전수 대조 + 원문 grep 검증 + ES curl 재검증 + 한자 병기 누락 검사. 특히 Q1(포퍼)·Q7(제임스)·Q8(호프만)의 trademark 3중 일치 재검증 권장.
2. **TASK-176 ES 등록 태스크 우선순위 재조정**:
   - **최최우선 (4연속 재출제)**: `hoffman` — 공감 각성 5양식 + 공감 발달 5단계 claim 구성 필수.
   - **최우선 (2연속 재출제)**: `durkheim` · `singer`. `popper` · `james`도 최우선(거장, 단골 출제).
3. **2022-A 누적 블로커 현황 재검토**: 2022-A(7건: jinul·pettit·green_th·turiel·shenxiu·zhiyi·beccaria) + 2022-B(5건: popper·durkheim·james·hoffman·singer) = **2022 연도 단독 12명 ES 미등록**. Phase 6 Coder 단계에서의 필연적 누적이며, Phase 7(ES 보강 + claim 작성)에서 일괄 해소 대상.
4. **3연속·4연속 경계 리스트 업데이트**:
   - 3연속 유지: `jinul`(2020-A·2021-B·2022-A) · `turiel`(2018-B·2021-B·2022-A).
   - **4연속 달성**: `hoffman`(2016-A·2019-B·2021-B·2022-B). ES 등록 최우선.
5. **다음 연도 진행**: 2023-A·2023-B로 Phase 6 연도별 coverage 계속 진행. 현 세션 기준 2014~2022 완료, 2023~2026 남음.
