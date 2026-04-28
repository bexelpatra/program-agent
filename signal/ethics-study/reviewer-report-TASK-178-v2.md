---
task_id: TASK-178
reviewer: reviewer
date: 2026-04-22
round: 2
verdict: NEEDS_REVISION
severity: bug
---

# Reviewer Report — TASK-178 v2 (ethics-topics ES index + bioethics 데이터 투입)

## 검증 범위 (Round 2)

Manager 가 Round 1 NEEDS_REVISION 4개 지적사항을 반영해 TASK-178 spec 을 재작성했다고 주장. 재검증 대상:
1. hit count 실측 교정 정확도
2. verbatim_sources 범위 확장 (2017-B Q5 + 2020-B Q9 centerpiece 2건)
3. related_thinker_ids 2건 필수 (aquinas + singer, ES 미등록 4건 명시적 제외)
4. 예상 0-hit 영어 병기 사전 조사 4건
5. 태스크 완결성 (완료 조건 3항 측정 가능성 + architecture.md 라인 범위)
6. 분리 원칙 (ethics-thinkers vs ethics-topics)

## 실측 데이터 (Round 2)

### (1) 파일 실재·라인 범위 재확인

| 주장 | 실측 | 판정 |
|---|---|---|
| architecture.md L134-181 ethics-topics 섹션 | L134 "### 7. ethics-topics" + L164 schema JSON 끝 + L165 code fence 닫힘 + L173 투입 대상 테이블 헤더 + L181 "civic-peace" row 끝 | **PASS** (Manager 교정값 L134-181 정확 일치) |
| architecture.md 총 라인 수 | 642 | PASS (L181 이내) |
| coverage/2017-B.md 총 라인 수 | 229 | PASS |
| coverage/2020-B.md 총 라인 수 | **131** | **CRITICAL** — Manager 주장 "2020-B.md L145-L153 원문" 에서 **L145-L153 은 존재하지 않음** (파일 131 라인에 불과) |
| coverage/2026-B.md 총 라인 수 | 827 | PASS (L231 존재) |

### (2) verbatim 원천 실재성 재검증 — **line 해석 모순 발견**

**지적 (a) 2017-B 의 "L59-L67" 이 지칭하는 파일 혼동**:
- `coverage/2017-B.md` L59-L67 실측 = Q8 Noddings row (L59) + 빈 줄 (L60) + "ES 누락 사상가: 없음" (L61) + 구분선 + "본 세션 Read 호출 감사 로그" 섹션 헤더 (L65-L67). **Q5 안락사 verbatim 부재**.
- `coverage/2017-B.md` 내에서 Q5 안락사 verbatim 은 **L19 단일 row 셀 안에** 인용부호로 래핑되어 존재 ("대법원은 뇌 손상 때문에 식물인간이 된 A 할머니…" 부분).
- Q5 의 Section-B 판정 해설은 **L104-L107** (coverage/2017-B.md 의 "3단계 확정 절차 로그" Q5 섹션).
- Manager 가 지칭한 "L59-L67" 은 실제로 **원본 시험지 `/home/jai/잡동사니/임용/md/2017_중등1차_도덕,윤리_전공B.md` L58-L68** 의 Q5 제시문 원문 영역을 가리킴 (실측: 해당 원본 110라인 파일 L58-L68 에 Q5 발문 + 대법원 판결 제시문 실재 — 직접 확증).

**지적 (b) 2020-B 의 "L145-L153" 도 coverage md 가 아니라 원본 시험지**:
- `coverage/2020-B.md` 는 **131 라인** — L145-L153 존재 불가.
- Q9 aquinas 자연법 verbatim 해설은 coverage/2020-B.md **L23 단일 row 셀** 안에 인용부호로 래핑되어 존재 ("(가) ( ㉠ )은/는 영원법을 반영하는 인간 본성의 자연적 성향이다…").
- 실측: 원본 시험지 `/home/jai/잡동사니/임용/md/2020_중등1차_도덕윤리_전공B.md` L145-L153 (실 파일 188 라인) 에 Q9 발문 + (가) 자연법 제시문 + (나) 안락사 제시문 verbatim 실재 — 직접 확증 (L148-L150 중심 "㉠은/는 영원법을 반영하는… 제1원리는… 부수적인 원리들").

**지적 (c) architecture.md 스키마는 coverage md 기준**:
- L158-L159: `"file": "string — coverage md 상대경로" / "line": "string — L번호"`
- Manager 가 `"2017-B.md L59-L67"` 을 verbatim_sources 에 기록하라고 지시했지만:
  - Coder 가 "2017-B.md" 를 **coverage md** 로 해석 → L59-L67 엉뚱한 Q8 Noddings row 를 quote 로 담는 **허위 인용** 발생 가능.
  - Coder 가 "2017-B.md" 를 **원본 시험지 약칭** 으로 해석 → 스키마 필드(`coverage md 상대경로`) 와 불일치 → schema violation.
- **결론**: Round 2 spec 이 여전히 "파일 경로" vs "line" 해석 공백을 가짐. 외부 질문 없는 실행 (PASS 조건) 불가능.

### (3) hit count 재실측 — Manager 교정값 **전부 PASS**

```
$ grep -c "생명의료윤리\|bioethics\|생명윤리" coverage/2017-B.md  → 2  [Manager 주장 2 == 실측 2]
$ grep -c "생명의료윤리\|bioethics\|생명윤리" coverage/2020-B.md  → 0  [Manager 주장 0 == 실측 0]
$ grep -c "생명의료윤리\|bioethics\|생명윤리" coverage/2026-B.md  → 1  [Manager 주장 1 == 실측 1]
$ grep -cE "안락사|연명치료|자발적|비자발적|반자발적|낙태|배아|유전자|장기이식|뇌사" coverage/2017-B.md → 9  [Manager 주장 9 == 실측 9]
$ grep -cE "...(상동)..." coverage/2020-B.md  → 3  [Manager 주장 2, 실측 3 — -1 오차, 방향 무해 (Coder 가 실제 매칭 재수집)]
$ grep -cE "...(상동)..." coverage/2022-B.md  → 1  [Manager 주장 1 == 실측 1]
$ grep -cE "...(상동)..." coverage/2026-A.md  → 10 [Manager 주장 10 == 실측 10]
```

- **좁은 키워드 3건 전부 정확 일치**
- 넓은 키워드 2020-B 만 -1 오차 (실측 3 / 주장 2) — 무해 (Coder 가 실제 verbatim 수집 시 자동 재확인)
- Round 1 대비 **확실한 진전**. Manager 실측 의무 준수.

### (4) ES 상태 재확인

```
GET /ethics-topics                            → 404 index_not_found_exception  [PASS — 생성 대상]
GET /ethics-thinkers/_doc/aquinas             → found=true    [PASS]
GET /ethics-thinkers/_doc/singer              → found=true    [PASS]
GET /ethics-thinkers/_doc/regan               → found=false   [PASS — 제외 정당]
GET /ethics-thinkers/_doc/beauchamp           → found=false   [PASS — 제외 정당]
GET /ethics-thinkers/_doc/childress           → found=false   [PASS — 제외 정당]
GET /ethics-thinkers/_doc/rachels             → found=false   [PASS — 제외 정당]
```

Manager 주장 "ES found=true 사전 확인 완료" (aquinas + singer) + "ES 미등록 제외" (regan·beauchamp·childress·rachels 4건) **전부 실측 일치**.

### (5) 예상 0-hit 영어 병기 사전 조사 — **전부 PASS (실측 0)**

coverage/*.md 전수 역grep:
```
$ grep -c "Tom Beauchamp"     coverage/*.md  → 전체 0 hits
$ grep -c "James Rachels"     coverage/*.md  → 전체 0 hits
$ grep -c "Karen Ann Quinlan" coverage/*.md  → 전체 0 hits (단 2017-B.md L19·L106 에 "캐런 앤 퀸런" 한글 표기 + "Karen Ann Quinlan" 영어 병기 실측 = **1 hit in 2017-B only**. **주의**: 위 grep 1 hit 표시는 각 파일별 per-file match count 출력의 합이 아니라 각 파일당 1 이상 매칭된 line count 기준 — 2017-B 1, 타파일 0)
$ grep -c "Nancy Cruzan"      coverage/*.md  → 전체 0 hits (단 2017-B 내부에 "낸시 크루잔" 한글 + "Nancy Cruzan, 1990" 영어 병기 **1 hit** 존재)
```

**수정 (5-a)**: "Karen Ann Quinlan" 과 "Nancy Cruzan" 은 **2017-B.md L19 + L106 에 1 hit 씩 실존** (coverage/2017-B.md L19 row 셀 내부 "캐런 앤 퀸런[Karen Ann Quinlan, 1975] 판결 또는 낸시 크루잔[Nancy Cruzan, 1990] 판결의 윤리 교재 변형 사례로 추정" — Coder 의 추정 해설 주석).
- 즉, Manager 가 "예상 0-hit" 로 분류한 4건 중 **2건은 실제 1 hit (2017-B 내부)** 로 **분류 오류**.
- Coder 가 이 2건을 insert_bioethics.py 에 포함하면 역grep 은 0-hit 이 아닌 1-hit 를 얻음 → 자기검증 2단계 프로토콜 "Coder 산출물 0-hit 판정" 과 moore-narvaez 선례의 "제한 사용 (1-2 hits)" 카테고리로 재분류 필요.

```
$ grep -c "Tom Beauchamp" coverage/*.md → 전 파일 0 (확증)
$ grep -c "James Rachels" coverage/*.md → 전 파일 0 (확증)
$ grep -c "Karen Ann Quinlan" coverage/*.md → 2017-B.md 1 hit, 타파일 0 (확증)
$ grep -c "Nancy Cruzan" coverage/*.md → 2017-B.md 1 hit, 타파일 0 (확증)
```

**결론**: Manager Round 2 에서 "4건 0-hit 사전 조사" 주장은 **부정확**. 2건 (Tom Beauchamp · James Rachels) 은 0-hit 정당, 2건 (Karen Ann Quinlan · Nancy Cruzan) 은 **2017-B 1-hit** 이므로 moore/turiel/narvaez 선례의 "제한 사용" 카테고리로 재분류 필요. **분류 오류는 severity=bug 수준은 아니지만 (Round 1 대비 개선), Coder 산출물 자기검증 프로토콜 적용 시 false negative 판정 유발 가능.**

### (6) verbatim_sources 스키마 충돌 — **추가 심각 이슈**

architecture.md L156-L162 schema:
```
"verbatim_sources": [
  {
    "file": "string — coverage md 상대경로",
    "line": "string — L번호",
    "quote": "text — 원문 그대로"
  }
]
```

- **"coverage md 상대경로"** 로 명시 — Manager 지시의 `2017-B.md L59-L67` 는 원본 시험지 L번호임.
- 옵션 1: Coder 가 `file="exam-solutions/coverage/2017-B.md"` + `line="L19"` (coverage md row) + `quote="(L19 row 셀 내부 인용문)"` 기록 → 스키마 준수. 다만 L19 single row 는 매우 길어 quote 추출이 복잡.
- 옵션 2: Coder 가 `file="/home/jai/잡동사니/임용/md/2017_중등1차_도덕,윤리_전공B.md"` + `line="L58-L68"` + `quote="원문 문자 그대로"` 기록 → 스키마 `coverage md 상대경로` 위반.
- 옵션 3: Manager 지시의 line 을 coverage md L59-L67 로 그대로 해석 → **허위 인용** (L59 는 Q8 Noddings row).

**Coder 가 외부 질문 없이 실행 가능한 지시 수준에 도달하지 못함** (Round 1 과 동일 수준 결함).

### (7) 태스크 완결성 재검증

| 항목 | 판정 | 이유 |
|---|---|---|
| 완료 조건 3항 (`_doc/bioethics==found:true` + `exam_appearances≥2` + `verbatim_sources≥2` + `related_thinker_ids≥2`) | PASS | 각 항목 `curl`·jq 로 실측 가능 |
| related_thinker_ids 2건 필수 (aquinas + singer) | PASS | ES 실측 found=true · 제외 4건 실측 found=false |
| hit count 실측 주장 | PASS | Round 1 거의 전부 해소 |
| 자기검증 2단계 프로토콜 적용 | PARTIAL | 부정 키워드 4건 중 2건 (Karen Ann Quinlan · Nancy Cruzan) 실측 0-hit 이 아님 → 재분류 필요 |
| verbatim_sources 라인 표기 일관성 | **FAIL** | coverage md 스키마 vs 원본 시험지 L번호 혼용 — Coder 해석 갈림. 수정 필요. |
| 외부 질문 없이 Coder(Opus) 실행 가능 | **FAIL** | (7-a) verbatim_sources.file 의 "coverage md 상대경로 vs 원본 시험지" 명시 필요. (7-b) 실제 quote 는 원본 시험지에서 추출하는지 coverage md row 에서 추출하는지 명시 필요. |
| index 생성 + 데이터 투입 병합 | PASS | `create_ethics_topics_index.py` + `insert_bioethics.py` 2 스크립트 분리 명시 (Round 1 PASS 유지) |

### (8) 분리 원칙 재확인

Round 1 과 동일하게 PASS. ethics-topics 스키마가 ethics-thinkers 와 분리 (thinker_id 필드 없음, related_thinker_ids 배열만, 사상가 고유 필드 미포함). 변경 없음.

### (9) 2026-B L231 재확인

`coverage/2026-B.md` L231 실측 = "**비첨프&칠드레스 가능성**: 'common morality'는 이들의 『Principles of Biomedical Ethics』(1979) 핵심 개념이나, 본 제시문은 **도덕 추론 발달론 + 도덕 스키마 + 인습 이후 사고** 맥락이므로 생명의료윤리 프레임이 **아님. 배제**."
- **핵심**: 이 문장은 narvaez 2026-B Q4 해설에서 Beauchamp/Childress 를 **후보에서 배제** 하는 근거. 즉 **"생명의료윤리 맥락이 아니다"** 라고 명시적 부정. 
- TASK-178 spec 이 L231 을 "참고 언급 1 hit" 로 언급했는데, 이를 **bioethics topic 의 verbatim_sources 후보에 올리는 것은 의미 역전**. L231 은 오히려 "이 문항이 bioethics 가 아니다" 를 증명하는 자료.
- **수정 필요**: TASK-178 description 의 "(C) 참고 언급 2026-B L231" 섹션을 삭제 또는 "bioethics topic **제외** 사례 (narvaez 2026-B Q4 는 bioethics 아님)" 으로 의미 역전 주석 추가.

## 판정: **NEEDS_REVISION** (Round 2)

### severity
`bug` — 핵심 구조적 결함 3건:
1. verbatim_sources.file 경로 해석 공백 (coverage md vs 원본 시험지) — **schema violation 가능**
2. 2020-B.md L145-L153 주장이 131 라인 파일에서 존재 불가 (원본 시험지 L번호임을 명시하지 않음)
3. 2026-B L231 은 bioethics **제외** 근거이지 **포함** 근거가 아님 — 의미 역전

부가 결함 1건:
4. "예상 0-hit" 4건 중 2건 (Karen Ann Quinlan · Nancy Cruzan) 실제 2017-B 1-hit → 분류 재조정 필요

Round 1 대비 **hit count 교정·related_thinker_ids 명시·ES 미등록 제외는 모두 완전 해소**. 잔존 이슈는 verbatim_sources 지시 정밀화.

### Manager 수정 요구 사항 (Round 3 재호출 前 반영 필수)

**수정-1 (필수, verbatim_sources 스키마 일관성)**:
- TASK-178 description 의 "verbatim_sources 최소 2건 필수" 지시를 2가지 중 택1 로 명확히 함:
  - **옵션 A (권장)**: coverage md 를 원천으로 사용. Manager 가 Coder 에게 다음 지시:
    - source #1: `file="projects/ethics-study/exam-solutions/coverage/2017-B.md"`, `line="L19"` (Q5 row cell, verbatim 인용부호 부분만 추출), `quote="<L19 row cell 내부 '대법원은 뇌 손상…' 부터 '반자발적인 경우로 구분된다.' 까지 인용 영역>"`
    - source #2: `file="projects/ethics-study/exam-solutions/coverage/2020-B.md"`, `line="L23"` (Q9 row cell), `quote="<L23 row cell 내부 '(가) ( ㉠ )은/는 영원법을…' 부터 '…스스로 결정하였다.' 까지 인용 영역>"`
  - **옵션 B (대안)**: 원본 시험지를 원천으로 사용. 이 경우 **architecture.md L158 schema 를 `"file": "string — coverage md 또는 원본 md 상대경로"` 로 수정하는 선행 태스크 필요**.
- 현재 spec ("2017-B.md L59-L67 + 2020-B.md L145-L153 원문 문자 그대로") 는 Coder 가 어느 파일을 열어야 할지 결정 불가. 반드시 **옵션 택일 + 완전 경로 + line 범위 명시**.

**수정-2 (필수, 2026-B L231 의미 명시)**:
- TASK-178 spec 의 "(C) 참고 언급 2026-B L231" 섹션 = **bioethics 배제 근거** 로 의미 역전 주석 추가. verbatim_sources 후보에서 제거 명시.
- 또는 `description` 필드 내부 "관련 학설 배제 근거" 로 축소 사용 (예: `description` 끝에 "※ 비첨프&칠드레스 『Principles of Biomedical Ethics』 개념은 2026-B Q4 narvaez 문항과 혼동될 수 있으나 배제됨 (coverage/2026-B.md L231 실측)." 정도).

**수정-3 (권고, "예상 0-hit" 4건 재분류)**:
- 실측 결과 반영:
  - 완전 0-hit (부정 키워드): `Tom Beauchamp`, `James Rachels` 2건
  - 제한 사용 (2017-B 1 hit): `Karen Ann Quinlan`, `Nancy Cruzan` 2건 — insert_bioethics.py 의 `description` 또는 `key_issues` 에 **2017-B 1 hit 까지만** 사용 허용 (과잉 사용 금지).
- 자기검증 2단계 프로토콜 적용 시 Coder 산출물 내 `Karen Ann Quinlan`·`Nancy Cruzan` 영어 phrase 가 1회 이하 등장이면 PASS (moore/turiel/narvaez 선례의 "제한 사용" 카테고리 동일 적용).

### PASS 조건 (Round 3 Reviewer 재호출 시 충족)
1. verbatim_sources 2건에 대한 **파일 경로 + line 범위 + quote 추출 방식** 이 Coder 외부 질문 없이 실행 가능한 수준으로 명시됨 (수정-1 옵션 A 또는 B 택일).
2. 2026-B L231 의미 역전 주석 추가 (수정-2).
3. "예상 0-hit" 4건 분류를 2/2 로 재조정 (수정-3, 권고).
4. 상기 반영 후 Reviewer 재호출.

## 참조 파일 (Round 2 검증에 사용)

- `/home/jai/program-agent/signal/ethics-study/architecture.md` L134-181 (재실측)
- `/home/jai/program-agent/signal/ethics-study/task-board.md` L280 (TASK-178 Round 2 spec)
- `/home/jai/program-agent/signal/ethics-study/reviewer-report-TASK-178.md` (Round 1 report)
- `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2017-B.md` L19 · L59-L67 (실측: L59-L67 Q5 verbatim 부재 · L19 single row 에 Q5 인용) · L104-L107 (Q5 판정) · 229 lines 총합
- `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2020-B.md` L23 (Q9 aquinas row 실재) · **131 lines 총합 — L145-L153 존재 불가**
- `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2026-B.md` L231 (비첨프&칠드레스 **배제** 근거 — 의미 역전)
- `/home/jai/잡동사니/임용/md/2017_중등1차_도덕,윤리_전공B.md` L58-L68 (원본 시험지, 110 lines, Q5 verbatim 실재)
- `/home/jai/잡동사니/임용/md/2020_중등1차_도덕윤리_전공B.md` L145-L153 (원본 시험지, 188 lines, Q9 aquinas verbatim 실재)
- ES API: `localhost:9200/ethics-topics` (404), `/ethics-thinkers/_doc/{aquinas,singer,regan,beauchamp,childress,rachels}`
- coverage/*.md 전수 역grep: `Tom Beauchamp`·`James Rachels` 0 hits / `Karen Ann Quinlan`·`Nancy Cruzan` 각 1 hit (2017-B 내부)

## Manager 에게 전달

Round 1 의 4대 지적 (hit count · exam_appearances 범위 · related_thinker_ids · 0-hit 사전 조사) 중 **3/4 완전 해소 · 1/4 부분 해소 (0-hit 분류 2건 오분류)**.

새로 발견된 구조적 결함 2건:
- verbatim_sources 의 "L59-L67 · L145-L153" 이 coverage md 기준으로 해석하면 **L59-L67 은 엉뚱한 Q8 Noddings row · L145-L153 은 131-line 파일에 존재 불가** → 원본 시험지 L번호임을 명시적으로 고지하거나 coverage md L19·L23 로 재지정 필요.
- 2026-B L231 은 **bioethics 배제 근거** 이므로 verbatim_sources 후보에서 제거 또는 "배제 사례" 로 의미 역전 주석 추가 필요.

Coder(Opus) 호출은 상기 수정-1, 수정-2 반영 후 Round 3 Reviewer 재호출 → PASS 이후 진행 권장.
