---
agent: tester
task_id: TASK-176-01
status: DONE
timestamp: 2026-04-22T09:15:00
severity: observation
---

## 결과 요약

Coder의 TASK-176-01(`jinul` 보조국사 지눌 ES 등록) 주장을 7개 체크리스트로 전수 검증했다. 7/7 모두 PASS. 카운트·메타 필드·원문 grep 대조·관계 링크 실재·핵심 개념 커버·keyword 유일성·회귀(coverage 미수정) 모두 일치.

`original_text` verbatim 4건(claim-001·003·004·008)은 Coder가 근거로 댄 coverage 파일(2020-A.md·2021-B.md·2022-A.md)에서 **모두 grep 매칭 확인**(0건 없음). original_text 공란(`""`) 5건은 창작 위험이 자동 제거된 상태.

## 변경된 파일

없음 (검증 전용).

## 테스트 결과

### 체크 1: ES 실측 존재 — PASS

```
curl -s localhost:9200/ethics-thinkers/_doc/jinul | jq .found → true
```

메타 필드 완비:
- id=`jinul`, name=`보조국사 지눌 (知訥)`, name_en=`Jinul (Bojo)`
- field=`eastern_ethics`, era=`고려`, birth_year=1158, death_year=1210
- background 443자, core_philosophy 474자, philosophical_journey 377자
- keywords 9개: 돈오점수/정혜쌍수/자성정혜/수상정혜/공적영지/정혜결사/조계종/수심결/간화선

### 체크 2: 카운트 일치 — PASS

| 인덱스 | Coder 주장 | 실측 | 결과 |
|--------|------|------|------|
| ethics-works (thinker_id=jinul) | 5 | 5 | PASS |
| ethics-claims (thinker_id=jinul) | 9 | 9 | PASS |
| ethics-keywords (thinker_id=jinul) | 9 | 9 | PASS |
| ethics-relations (jinul 관련) | 2 | 2 | PASS |

**주의**: ethics-relations 스키마는 `from`/`to`가 아니라 `from_thinker`/`to_thinker` 필드를 사용한다(plato-rel-001 샘플로 확인). 초기 `term.from=jinul` 쿼리가 0건이었던 것은 필드 오해였고, `query_string: "jinul"` 및 `from_thinker`/`to_thinker` 기준으로는 `rel-huineng-jinul-1`, `rel-wonhyo-jinul-2` 2건 정상 존재.

### 체크 3: 원문-grep 대조 표준 — PASS

**claim.original_text 4건 (verbatim quoted) grep 결과:**

| claim_id | 근거 원문 파편 | coverage 파일 | grep 카운트 |
|----------|----------------|---------------|------------|
| jinul-claim-001 | "심성(心性)이 본래 깨끗하고…" | 2020-A.md | 1 ✓ |
| jinul-claim-001 | "점문(漸門)의 오염된 수행…" | 2020-A.md | 1 ✓ |
| jinul-claim-003 | "번뇌가 엷고 몸과 마음이 가볍고…" | 2020-A.md | 1 ✓ |
| jinul-claim-003 | "자성정혜" | 2020-A.md | 5 ✓ |
| jinul-claim-003 | "수상정혜" | 2020-A.md | 5 ✓ |
| jinul-claim-003 | "여덟 가지 번뇌[八風]" | 2020-A.md | 1 ✓ |
| jinul-claim-003 | "天眞/천진" | 2020-A.md | 3 ✓ |
| jinul-claim-004 | "諸入理之門" (한자 verbatim) | 2022-A.md | 1 ✓ |
| jinul-claim-004 | "定是體 慧是用也" | 2022-A.md | 1 ✓ |
| jinul-claim-004 | "공적영지" | 2022-A.md | 1 ✓ |
| jinul-claim-008 | "관(觀)을 배우지 않고 경전만을 공부하면" | 2021-B.md | 1 ✓ |
| jinul-claim-008 | "경전을 공부하지 않을 수 없는" | 2021-B.md | 1 ✓ |
| jinul-claim-008 | "윤회와 해탈의 인과" | 2021-B.md | 1 ✓ |
| jinul-claim-008 | "진리를 통찰하는 명상법" | 2021-B.md | 1 ✓ |

**verbatim 인용 14 파편 중 grep 0건 없음** → Coder 창작/자동보강 의심 없음.

**original_text 공란(`""`) 5건** (claim-002/005/006/007/009): 자동 PASS (창작 위험 제거).

**관찰 사항 (observation만, bug 아님)**: claim/explanation 필드에는 다음 고유명이 포함되어 있으나 출제 coverage 문서에는 0건이다. 이들은 일반 불교사/권위 출처 기반 배경 서술이며, 출제 trademark 주장(★exam-verbatim)이 아니다. 따라서 grep-0-bug 규칙의 1차 대상(원문 인용문)에는 해당하지 않는다.
- "대혜 종고(大慧 宗杲, 1089~1163)" — claim-007 explanation (간화선 창시자 역사 상식)
- "송광사/거조사/보제사" — claim-006 explanation (정혜결사 이력 연표)
- "구자불성(狗子佛性, 무無)" — claim-007 explanation (간화선 표본 화두)
- "성성적적/묵조" — claim-005/007 explanation (수행법 대조 술어)

### 체크 4: relations 링크 타깃 실재 — PASS

```
curl -s localhost:9200/ethics-thinkers/_doc/huineng | jq .found → true
curl -s localhost:9200/ethics-thinkers/_doc/wonhyo | jq .found → true
```

삽입된 2건 실측:
- `rel-huineng-jinul-1` (from_thinker=huineng → to_thinker=jinul, type=influenced, description 『수심결』의 『육조단경』 인용 근거 제시)
- `rel-wonhyo-jinul-2` (from_thinker=wonhyo → to_thinker=jinul, type=influenced, description 화쟁·회통 → 선교일치 계보)

### 체크 5: 핵심 재출제 개념 커버 — PASS

| 개념 | claim 내 match_phrase | keyword 등록 |
|------|----------------------|-------------|
| 돈오점수 | 1 (claim-001) | 1 ✓ |
| 정혜쌍수 | 1 (claim-002) | 1 ✓ |
| 자성정혜 | 1 (claim-003) | 1 ✓ |
| 수상정혜 | 1 (claim-003) | 1 ✓ |

4개 개념 모두 최소 1개 claim 및 keyword로 커버 (정혜쌍수는 claim-002/005/006에도 keyword 수준으로 재등장).

### 체크 6: keyword 중복 미등록 — PASS

9개 term 모두 고유(term별 count=1):
```
      1 조계종
      1 정혜쌍수
      1 정혜결사
      1 자성정혜
      1 수심결
      1 수상정혜
      1 돈오점수
      1 공적영지
      1 간화선
```

### 체크 7: 원본 coverage 파일 미수정 (회귀) — PASS

jinul 관련 coverage 파일 mtime (2026-04-21, TASK-175E 완료일):
- 2020-A.md: 2026-04-21 11:27
- 2021-B.md: 2026-04-21 13:34
- 2022-A.md: 2026-04-21 14:25

insert_jinul.py mtime: 2026-04-22 08:48 (> coverage mtimes). Coder가 coverage 파일을 수정하지 않고 insert 스크립트만 신규 생성했음을 확인.

## 이슈/블로커

없음. 검증 대상 결함 없음.

## 관찰 사항 (observation, 수정 불요)

1. **explanation 필드의 일반 불교사 고유명 미인용**: "대혜 종고", "송광사·거조사·보제사", "구자불성", "성성적적" 등은 출제 원문이 아니라 배경 서술로 포함되어 grep-0-bug 규칙의 1차 대상(verbatim 인용문)에는 해당하지 않는다. Coder 본문이 "역사 상식"으로 기재한 영역이므로 creation으로 보지 않는다. 장기적으로는 explanation에도 원문 인용 규정을 확장하는 프레임워크 정비가 유익할 수 있으나, 본 태스크 범위에서는 PASS.

2. **ethics-relations 필드명 규약**: 스키마가 `from_thinker`/`to_thinker`이므로 태스크 지시의 "from/to" 표현과 혼동 여지가 있다. 향후 검증 체크리스트 작성 시 필드명을 명시하면 초기 0건 오진을 방지할 수 있다.

3. **core_philosophy/background 실측 길이**: 각각 474자·443자로 충실. wonhyo·huineng 선례 템플릿과 동등 수준.

## 다음 제안

- TASK-176-01 DONE 처리.
- coder-report-TASK-176-01의 "다음 제안" 항목(uicheon 등록, zongmi 등록, taego 등록) 중 `uicheon`은 2021-B BLK-175E-2021B-001 해소와 직결되므로 TASK-176-02로 우선 등록할 것을 권고(본 태스크 범위 밖 관찰).
- 향후 `jinul` 관계 링크 확장 시 `zongmi`(공적영지·돈오점수 직접 계승) 추가가 사상 계보 완전성에 필수.
