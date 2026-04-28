# agents/coder.md 수정 제안 — 자기검증 2단계 규약

- 작성: 2026-04-22 (TASK-176-10-FIX DONE 직후)
- 원인 태스크: TASK-176-10 (narvaez ES 등록) · TASK-176-10-T (3 bug 발견) · TASK-176-10-FIX (Manager inline 수정)
- 대상 파일: `agents/coder.md` (원문/입력 인용 규칙 섹션, L83-87)
- **상태**: 사용자 승인 대기 (CLAUDE.md Step 6 규정 — 사용자 승인 없이 프레임워크 파일 수정 금지)

---

## 현행 규정 원문 (agents/coder.md L83-87)

```markdown
### 원문/입력 인용 규칙 (문서·해설·분석 성격 태스크 공통)
- 사용자 제시 원문·입력 파일을 근거로 해설/요약/분류/매핑을 작성할 때, **원문에 grep 0건인 고유명·trademark·개념어·한자어·인용문을 절대 추가하지 않는다.** "이 사상가라면 이 용어를 쓸 것" 같은 자동 보강은 금지.
- 원문 인용은 문자 그대로(verbatim) 복사하고, 해설·추론은 인용과 구분되는 별도 블록에 둔다.
- 불확실하면 보강하지 말고 "확증 보류" 처리 후 blocker/observation으로 남긴다.
- 작성 후 자기검증: 새로 쓴 고유명·한자·trademark를 원문 파일에 역grep해 0건이면 제거·대체한다.
```

---

## 문제 상황 — narvaez 3 bug 재발

### 개선 궤적 중단
- pettit(bug 3) → singer(bug 1) → turiel(bug 0) → moore(bug 0) → **narvaez(bug 3)** — 2연속 clean run 직후 재발

### Tester 발견 3 bug (모두 coverage 0-hit 영어 phrase)
| ID | 토큰 | 위치 (insert_narvaez.py) | coverage case-sensitive hit | 근본 원인 |
|----|------|--------------------------|----:|----------|
| bug-1 | `safety ethic` | L152 (본문 괄호 병기) · L350 (claim 본문) · L852 (keyword `term_en`) | 0 | 한글 "안전 윤리" 8 hits 풍부하지만 영어 phrase 자체 부재. Coder 창작·보강 |
| bug-2 | `engagement ethic` | L152 · L405 · L872 (keyword `term_en`) | 0 | coverage 는 `engagement care` 1 hit / `engagement distress` 3 hits 만. `engagement ethic` 0 |
| bug-3 | `moral foundations theory` (소문자) | L1198 | 0 (case-sensitive) | coverage 는 TitleCase `Moral Foundations Theory` 5 hits 만. case-sensitive 표준 미준수 |

### 근본 원인 — Coder(Opus) 자기검증 regex 한계

현행 Coder 자기검증 루프 (narvaez coder-report L37-51 인용):
```
grep -oE '\([A-Za-z][^)]*\)' insert_narvaez.py | sort -u
```

이 regex 는 **괄호 안 영어 토큰만** 캐치. 놓친 패턴:

1. **JSON 필드 값** — keyword 정의의 `"term_en": "safety ethic"` 형태 (L852·L872). 괄호 구문 아니므로 regex 미매칭.
2. **본문 괄호 밖 영어 phrase** — 혹은 괄호 병기했더라도 coverage 역grep 결과를 **script 본문**이 아닌 **coverage md 파일**에 수행했어야 함. Coder report L51 의 `engagement ethic=3` 같은 hit count 는 script 자신의 grep 결과일 가능성 (중복 계산).
3. **대소문자 변이** — `moral foundations theory` (L1198 소문자) vs coverage `Moral Foundations Theory` (TitleCase 5 hits). case-sensitive 엄수 없으면 탐지 실패.

### Manager inline FIX 결과 (TASK-176-10-FIX)
- L152·L350·L405 영어 병기 `(safety ethic)`·`(engagement ethic)` 6건 삭제
- L852·L872 `term_en` 2건 → `""` 공란 처리 (kw-narvaez-dual-process-nonconscious L1074 선례 준수)
- L1198 `moral foundations theory` → `Moral Foundations Theory` TitleCase 교체
- 검증: `grep -c "safety ethic\|engagement ethic" insert_narvaez.py == 0`, `grep -c "moral foundations theory" == 0`, `grep -c "Moral Foundations Theory" == 1`
- ES 재실행: `kw-narvaez-safety-ethic` · `kw-narvaez-engagement-ethic` 삭제 후 재생성 (term_en='' 반영), claim-002/003/009 updated

---

## 제안 diff

### 추가 위치
`agents/coder.md` 의 "원문/입력 인용 규칙" 섹션 마지막 불릿 (L87) 뒤에 **2단계 자기검증 프로토콜** 을 추가.

### 추가 제안 문구 (markdown 그대로)

```markdown
### 자기검증 2단계 프로토콜 (원문 인용 태스크 필수)

원문-grep 실증이 요구되는 태스크(해설 요약·ES 등록·매핑 집계 등)에서는 아래 2단계를 **저장 전 반드시 실행**한다. Step 1 만으로는 JSON 필드·본문 괄호 밖 영어 phrase·대소문자 변이를 포착할 수 없어 재발 사례(TASK-176-10 narvaez 3 bug)가 있다.

**Step 1 — 괄호 안 영어 토큰**
```bash
grep -oE '\([A-Za-z][^)]*\)' {script_or_output} | sort -u
```

**Step 2 — 괄호 밖 / JSON 필드 / TitleCase 전수 추출 (신규)**
- JSON 필드 값 (term_en, name_en, source_detail 등):
  ```bash
  grep -oE '"(term_en|name_en)"\s*:\s*"[^"]*"' {script_or_output}
  ```
- 괄호 밖 TitleCase 영어 phrase (2~6 단어):
  ```bash
  grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}' {script_or_output}
  ```

**검증 실행 규칙**
- 각 추출 토큰을 **coverage 입력 md 전수**(자기 산출물이 아닌 원문 파일)에 `grep -F --case-sensitive` 로 역검색.
- 0-hit 토큰은 **제거 / 한글 단독 전환 / TitleCase 등 coverage 존재 표기 대체** 중 택1.
- Coder report 의 "유지된 토큰 표" hit count 는 반드시 **coverage md 를 대상으로 한 case-sensitive 실측값**이어야 한다. script 본문 자신에 grep 한 값은 기재 금지.

**면제 조건**
- 태스크 스펙에 "명시적 창작 허용" (예: architecture.md 설계 결정) 이 기재된 경우.
- 실행 결과를 report 의 "자기검증 루프 결과" 에 표 형식으로 정확히 적재.
```

---

## 적용 시 영향 분석

### 긍정 영향
- narvaez 3 bug 같은 재발 패턴 저장 전 포착 가능 (특히 JSON 필드 값 누락 · case-sensitive 변이).
- Coder self-verification 신뢰도 상승 → Tester 가 "bug 발견자" 가 아닌 "최종 확증자" 로 역할 집중.
- Manager inline FIX 빈도 감소 (TOP10 에서는 3회 발생, 모두 영어 trademark 0-hit 원인).

### 부정 영향 / 비용
- Coder 자기검증 시간 +15~25% 추정 (narvaez 스펙 기준, Step 2 regex 2개 + case-sensitive 대조 작업 증가).
- 스크립트 길이가 큰 태스크에서 false positive 증가 가능 (예: `Charles Taylor` 같은 ES 실재 TitleCase 도 Step 2 regex 에 매칭 → 하지만 coverage 역grep 결과 ≥1 hit 이면 PASS).

### 소급 적용 여부
- **소급 불필요**: 기존 등록 10인 (jinul·blasi·durkheim·hoffman·bandura·pettit·singer·turiel·moore·narvaez) 중 bug 발생 3인 모두 Manager inline FIX 로 이미 반영 완료.
- 향후 신규 사상가 등록 태스크 (Phase 7 이후 녹색당(green_th)·비롤리(viroli) 등) 부터 적용.

---

## 사용자 승인 필요 사항

다음 변경은 **프레임워크 파일 수정**에 해당하므로 CLAUDE.md 규정상 사용자 승인 필수:

1. [ ] `agents/coder.md` L87 뒤에 "자기검증 2단계 프로토콜" 섹션 추가 (위 제안 문구)
2. [ ] (선택) 관련 보조 제안: Manager 대필 프로토콜 명문화 (retrospective 제안 8)
3. [ ] (선택) 관련 보조 제안: Coder report "유지된 토큰 표" 대상 명시 (retrospective 제안 9)

승인 시 Manager 가 단독 세션에서 적용하고, 다른 세션에 재시작 유도 (CLAUDE.md "프레임워크 파일 수정 시" 규정 준수).

---

## 참조

- `signal/ethics-study/done-log.md` TASK-176-10 · TASK-176-10-T · TASK-176-10-FIX
- `signal/ethics-study/coder-report.md` (narvaez Coder 자기검증 루프 Step A~D)
- `signal/ethics-study/tester-report.md` (narvaez 9-체크 + 3 bug)
- `signal/ethics-study/retrospective.md` "Phase 6 TASK-176 TOP10 MISS 회고" 섹션
- `signal/ethics-study/data-quality-log.md` TASK-DQ-005
- `projects/ethics-study/scripts/insert_narvaez.py` L152·L350·L405·L852·L872·L1198 (FIX 6 위치)
