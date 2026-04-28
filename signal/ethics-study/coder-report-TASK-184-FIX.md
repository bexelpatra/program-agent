---
agent: coder
task_id: TASK-184-FIX
status: DONE
timestamp: 2026-04-22T00:00:00
---

## 결과 요약

`projects/ethics-study/exam-solutions/study-guide/2015-A.md` 에서 Coder 자체 보강으로 주입되었던 Greek 알파벳 토큰 4종(`γενναῖον`, `ψεῦδος`, `μετὰ`, `λόγος`) 및 손상형 단편(`με λόγου`)을 전수 제거했다. 3개 edit 으로 완료했으며, 각 토큰이 포함된 괄호를 제거하되 주변 한글 설명(`고귀한 거짓말`, `덕은 로고스를 동반하는 것`, `로고스 그 자체`, `로고스와 함께 있는 것`, `로고스 자체`)이 이미 문맥을 담고 있어 의미 손실 없이 문법적으로 성립한다. 다른 문항·섹션의 본문은 변경하지 않았다.

## 변경된 파일

- projects/ethics-study/exam-solutions/study-guide/2015-A.md (수정, 3 edits)

## 변경 Diff (Before/After 스니펫)

### Edit 1 — L352 기입형 9 (플라톤, 국가 이익 거짓말)

**Before**
```
  4. "국가 이익을 위한 거짓말 허용" → "고귀한 거짓말(noble lie, γενναῖον ψεῦδος)".
```

**After**
```
  4. "국가 이익을 위한 거짓말 허용" → "고귀한 거짓말(noble lie)".
```

제거 토큰: `γενναῖον`, `ψεῦδος`. `noble lie` 한글 의역은 이미 문장에 존재하며 coverage/2015-A.md L23 에도 `noble lie` hit=1.

### Edit 2 — L452 서술형 1 (아리스토텔레스, 잘못된 점)

**Before**
```
아리스토텔레스는 "덕은 로고스를 동반하는 것(μετὰ λόγου)"이지 "로고스 그 자체(λόγος)"가 아니라고 수정한다.
```

**After**
```
아리스토텔레스는 "덕은 로고스를 동반하는 것"이지 "로고스 그 자체"가 아니라고 수정한다.
```

제거 토큰: `μετὰ`, `λόγου`(μετὰ λόγου 전체), `λόγος`. `로고스` 한글 표기가 동일 문장 내에 존재하여 의미 보존.

### Edit 3 — L463 서술형 1 채점 기준

**Before**
```
- (2점) ㉠ 소크라테스의 옳은 점·잘못된 점 — (옳은 점) 덕이 이성(로고스)과 분리 불가 / (잘못된 점) 주지주의 환원, 덕을 앎(에피스테메)으로만 축소하여 욕구·습관·품성의 차원을 간과. "로고스와 함께 있는 것(με λόγου)"과 "로고스 자체(λόγος)"의 구분.
```

**After**
```
- (2점) ㉠ 소크라테스의 옳은 점·잘못된 점 — (옳은 점) 덕이 이성(로고스)과 분리 불가 / (잘못된 점) 주지주의 환원, 덕을 앎(에피스테메)으로만 축소하여 욕구·습관·품성의 차원을 간과. "로고스와 함께 있는 것"과 "로고스 자체"의 구분.
```

제거 토큰: `με λόγου` (원래 `μετὰ λόγου` 의 손상형으로 보이며 의미 불명), `λόγος`. `로고스` 한글 표기가 인접 구절에 존재.

## 완료 조건 검증

### 1. Greek 토큰 0건 재확증

```bash
$ grep -c 'γενναῖον\|ψεῦδος\|μετὰ\|λόγος' projects/ethics-study/exam-solutions/study-guide/2015-A.md
0
```

완료 조건 2 충족.

### 2. edits 수 ≤ 3

3 edits. 완료 조건 3 충족.

### 3. 자기검증 2단계 Step 1 재실행 — 괄호 안 Latin 토큰 전수 추출 후 coverage 역grep

편집 후 `grep -oE '\([A-Za-z][^)]*\)' study-guide/2015-A.md | sort -u` 결과는 총 76 개 유니크 토큰. 이 중 원문 인용·thinker 식별자·standard trademark 외에 Coder 보강 성격 토큰 샘플 및 coverage/2015-A.md 역grep hit:

| 토큰 | coverage hit (case-sensitive) | 판정 |
| --- | --- | --- |
| `(noble lie)` | 1 (L23) | OK |
| `(deinotés)` | 2 | OK |
| `(episteme — 앎)` (episteme) | 1 | OK |
| `(phronēsis)` | 1 | OK |
| `(logos)` | 1 | OK |
| `(idea)` | 1 | OK |
| `(Politeia)` | 1 | OK |
| `(Plato)` | 2 | OK |
| `(Aristotle)` | 2 | OK |
| `(Nicomachean Ethics)` | 1 | OK |

모든 샘플 hit ≥ 1. Greek 알파벳으로 시작하는 괄호 토큰은 정규식 `\([A-Za-z]` 에 매칭되지 않아 추출되지 않으며, 편집 후 Greek 토큰 자체가 0건이므로 자기검증 경계 조건 문제도 해소됐다. 완료 조건 4 충족.

### 4. 범위 외 변경 없음

Edit 3건 모두 Greek 토큰이 포함된 정확한 구절만 치환했다. `git status` 상 해당 파일이 untracked 이므로 diff 비교 불가(신규 파일)여서 Before/After 스니펫으로 증빙한다. 완료 조건 5 충족.

## 이슈/블로커

없음.

## 다음 제안

1. agents/coder.md L89-L115 자기검증 2단계 프로토콜의 Step 1 정규식 `\([A-Za-z][^)]*\)` 은 **Latin 알파벳만** 탐지한다. Greek 알파벳(`\p{Greek}`)·Cyrillic 등 비-Latin 문자로 시작하는 괄호 토큰은 경계 밖으로 빠져나간다. 본 태스크의 `γενναῖον ψεῦδος`, `μετὰ λόγου`, `λόγος` 3건이 정확히 이 경계 조건에 해당한다.
   - 제안: Step 1 정규식을 `\([^\x00-\x7F]*[A-Za-z\p{Greek}][^)]*\)` 혹은 2-pass (Latin + non-ASCII 별도) 로 확장. 또는 Step 2 에 "괄호 안 non-ASCII 알파벳 토큰 추출" 3번째 추출 명령을 추가.
   - 구체 예: `grep -oE '\([^)]*[α-ωΑ-Ω][^)]*\)' {file}` 로 Greek 포함 괄호를 별도 추출.
2. 본 태스크는 FIX 전용으로 범위를 준수했으나, 2015-A.md 외 다른 study-guide 파일(2014-A·2016-A 등)에도 동일 패턴의 Greek 보강이 존재할 가능성이 있음. Manager 판단으로 batch audit 태스크(`grep -lE '[α-ωΑ-Ω]' projects/ethics-study/exam-solutions/study-guide/*.md`) 를 고려할 수 있다.
