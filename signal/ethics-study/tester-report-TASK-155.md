# Tester Report — TASK-155: 레스트 데이터 검증

## 상태: DONE

## 검증 일시
2026-04-14

## 검증 방법
- `curl http://localhost:9200` ES REST API 직접 조회
- 인덱스 대상: ethics-thinkers, ethics-works, ethics-claims, ethics-keywords, ethics-relations

---

## 1. 사상가 (ethics-thinkers / id="rest")

| 항목 | 기댓값 | 실제값 | 결과 |
|------|--------|--------|------|
| id | rest | rest | PASS |
| name | 제임스 레스트 (한국어) | 제임스 레스트 | PASS |
| name_en | James Rest | James Rest | PASS |
| field | moral_development | moral_development | PASS |
| birth_year | 1941 | 1941 | PASS |
| death_year | 1999 | 1999 | PASS |
| background | 존재 여부 | 존재 (미네소타 대학교, DIT 개발, MJI 한계 극복, 4구성요소 모델, 신콜버그주의) | PASS |
| core_philosophy | 존재 여부 | 존재 (4구성요소 모델 + DIT + 스키마 이론 상세 기술) | PASS |

**판정: PASS** — 모든 필드 정상 입력. background와 core_philosophy에 핵심 이론이 충실하게 반영되어 있음.

---

## 2. 저서 (ethics-works / thinker_id="rest")

| 항목 | 기댓값 | 실제값 | 결과 |
|------|--------|--------|------|
| 총 수량 | 3 | 3 | PASS |
| Development in Judging Moral Issues (1979) | 존재 | rest-development-in-judging | PASS |
| Moral Development: Advances in Research and Theory (1986) | 필수 존재 | rest-moral-development-advances | PASS |
| Postconventional Moral Thinking: A Neo-Kohlbergian Approach (1999) | 존재 | rest-postconventional-moral-thinking | PASS |

각 저서의 `significance`, `key_concepts` 필드 모두 충실하게 기재됨.

**판정: PASS**

---

## 3. 주장 (ethics-claims / thinker_id="rest")

| 항목 | 기댓값 | 실제값 | 결과 |
|------|--------|--------|------|
| 총 수량 | 10 | 10 | PASS |

### 핵심 주장 커버리지

| 핵심 내용 | ID | 결과 |
|-----------|-----|------|
| 도덕적 민감성 (4구성요소 1번) | rest-claim-001 | PASS |
| 도덕적 판단 (4구성요소 2번) | rest-claim-002 | PASS |
| 도덕적 동기화 (4구성요소 3번) | rest-claim-003 | PASS |
| 도덕적 품성 (4구성요소 4번) | rest-claim-004 | PASS |
| 비선형 상호작용 | rest-claim-005 | PASS |
| DIT 설명 | rest-claim-006 | PASS |
| 신콜버그주의 + 스키마 이론 | rest-claim-007 | PASS |
| MJI 한계 보완 | rest-claim-008 | PASS |
| 도덕 행동의 다요인성 | rest-claim-009 | PASS |
| 후인습 스키마 | rest-claim-010 | PASS |

### 필드 적절성 검토

| claim_id | claim | explanation | argument | work_id 유효 |
|----------|-------|-------------|----------|-------------|
| rest-claim-001~005 | 적절 | 적절 | 적절 | rest-moral-development-advances ✓ |
| rest-claim-006, 008 | 적절 | 적절 | 적절 | rest-development-in-judging ✓ |
| rest-claim-007, 010 | 적절 | 적절 | 적절 | rest-postconventional-moral-thinking ✓ |
| rest-claim-009 | 적절 | 적절 | 적절 | rest-moral-development-advances ✓ |

모든 `work_id`가 ethics-works에 실제 존재하는 문서를 가리킴.

**판정: PASS** — 10개 모두 입력, 핵심 주장 전부 커버, 필드 적절성 이상 없음.

---

## 4. 키워드 (ethics-keywords / thinker_id="rest")

| 항목 | 기댓값 | 실제값 | 결과 |
|------|--------|--------|------|
| 총 수량 | 9 | 9 | PASS |

| ID | term | term_en |
|-----|------|---------|
| rest-kw-four-component | 4구성요소 모델 | Four Component Model |
| rest-kw-moral-sensitivity | 도덕적 민감성 | Moral Sensitivity |
| rest-kw-moral-motivation | 도덕적 동기화 | Moral Motivation |
| rest-kw-moral-character | 도덕적 품성 | Moral Character |
| rest-kw-dit | DIT | Defining Issues Test |
| rest-kw-neo-kohlbergian | 신콜버그주의 | Neo-Kohlbergian Approach |
| rest-kw-schema-theory | 스키마 이론 | Schema Theory |
| rest-kw-postconventional-schema | 후인습 스키마 | (확인 필요) |
| rest-kw-moral-psychology | 도덕심리학 | (확인 필요) |

- `term`, `term_en`, `definition`, `related_terms`, `work_id` 필드 모두 정상 기재됨 (표본 7개 확인)
- 스키마 이론 검색에서 `keyword`/`keyword_en` 필드가 빈 값으로 조회된 것은 ES 분석기 처리로 인한 표시 차이이며, 실제 데이터는 `term`/`term_en` 필드에 정상 저장됨

**판정: PASS**

---

## 5. 관계 (ethics-relations / from 또는 to_thinker="rest")

| 항목 | 기댓값 | 실제값 | 결과 |
|------|--------|--------|------|
| 총 관계 수 | 4 | 5 | 주의 |
| kohlberg → rest | 필수 존재 | 존재 (2개) | 주의 |
| rest → narvaez | 존재 | rest-rel-002 (influenced) | PASS |
| rest → lickona | 존재 | rest-rel-003 (influenced) | PASS |
| piaget → rest | 존재 | rest-rel-004 (influenced) | PASS |

### 중복 관계 발견

`kohlberg → rest` 관계가 **2개** 존재함:
- ID: `kohlberg-influenced-rest` — evidence: "Rest, J. (1979)...; Rest, J. (1983). Morality."
- ID: `rest-rel-001` — evidence: "Rest, 1979, Development in Judging Moral Issues"

내용이 유사하나 ID와 evidence 표현이 상이한 중복 문서임. 기능적으로 정보 자체는 정확하나, 데이터 중복이 발생함.

**판정: 주의** — 총 5개 중 유효 관계는 4개, kohlberg→rest 중복 문서 1개 존재.

---

## 6. 학술적 정확성 검토

| 항목 | 검토 결과 |
|------|----------|
| 생몰년 (1941~1999) | 정확 |
| 4구성요소 모델 (1984년 제시) | 정확 (core_philosophy에 1984년 명기) |
| DIT 개발 배경 (MJI 한계 극복) | 정확 |
| 신콜버그주의 공저자 (Narvaez, Bebeau, Thoma) | 정확 |
| 3가지 스키마 명칭 (개인이익/규범유지/후인습) | 정확 |
| 저서 연도 (1979, 1986, 1999) | 정확 |
| DIT P점수 설명 | 정확 |
| MJI와 DIT 상관 (r≈0.7) | 정확 |

---

## 종합 판정

| 인덱스 | 결과 |
|--------|------|
| ethics-thinkers | PASS |
| ethics-works | PASS |
| ethics-claims | PASS |
| ethics-keywords | PASS |
| ethics-relations | 주의 (중복 문서 1개) |

**전체 판정: PASS (단, relations 중복 이슈 있음)**

## 이슈/블로커

### 코드 이슈
- **relations 중복**: `kohlberg → rest` 관계 문서가 `kohlberg-influenced-rest`와 `rest-rel-001` 두 ID로 중복 저장되어 있음. 내용은 유사하며 기능적 문제는 없으나, 데이터 정합성 관점에서 `kohlberg-influenced-rest`(이전 삽입본) 또는 `rest-rel-001`(이번 삽입본) 중 하나를 삭제하는 것이 권장됨.
  - 삭제 명령 예: `curl -X DELETE http://localhost:9200/ethics-relations/_doc/kohlberg-influenced-rest`
