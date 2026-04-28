---
agent: tester
task_id: TASK-161
status: DONE
timestamp: 2026-04-15T00:00:00
severity: observation
---

## 결과 요약

백낙청(baek_nakcheong) ES 데이터(thinker 1 / works 3 / claims 7 / keywords 7 / relations 0)에 대해
ES 쿼리 검증 및 웹 교차검증을 수행했다. 핵심 학술 사실(분단체제론·변혁적 중도주의·87년체제·민족문학론·
창작과비평·한반도식 통일)은 대체로 정확하다. 저서 3건의 연도·제목·의의는 창비 공식/언론 자료와 일치한다.
다만 몇몇 **부수 정보의 부정확**과 **스키마 필드명 불일치**가 관찰되어 observation 으로 보고한다.
핵심 주장 내용과 DB 가치를 저해하는 블로커·버그는 없다.

## 변경된 파일

없음 (검증 전용 태스크, src/·scripts/ 수정 없음)

## 테스트 결과

### 1. ES 적재 건수 (실측)
- `ethics-thinkers/_doc/baek_nakcheong` : 존재 (field=unification_edu, birth_year=1938, keywords 10개)
- `ethics-works` (thinker_id=baek_nakcheong) : 3건 — 공부길(1994), 흔들리는(1998), 한반도식(2006)
- `ethics-claims` (thinker_id=baek_nakcheong) : 7건 — 전 건 argument/counterpoint/keywords 존재,
  `original_text_ko` 포함은 3건(claim-001/002/004) — 태스크 요구 ≥3 충족
- `ethics-keywords` (thinker_id=baek_nakcheong) : 7건 — 분단체제론/변혁적 중도주의/87년체제/민족문학론/
  흔들리는 분단체제/한반도식 통일/창작과비평
- `ethics-relations` (thinker_id=baek_nakcheong) : 0건 (스크립트 의도대로)

Coder report의 "thinker keywords 10개" / "keywords 7건" 서술과 실 ES 값 일치.

### 2. 저서 연도·출판사 정확성 (웹 교차검증)

| 저서 | DB year | 실제 초판 | 출판사 | 판정 |
|------|---------|-----------|--------|------|
| 분단체제 변혁의 공부길 | 1994 | 1994 (창작과비평사) | 창비 | 일치 |
| 흔들리는 분단체제 | 1998 | 1998-06-20 (창비) | 창비 | 일치 |
| 한반도식 통일, 현재진행형 | 2006 | 2006-05-01 (창비) | 창비 | 일치 |

- 교보문고·창비 공식·알라딘 상품 페이지 및 "한반도식 통일…서 담론 제시"(경향 2006) 등 언론 보도로 확인.
- 스키마상 `publisher` 필드는 없으므로 저장 값 영향 없음.

### 3. 핵심 개념 정확성

#### 3.1 분단체제론 (claim-001, kw-bundan-chejeron)
- 최초 본격 논의는 「분단체제의 인식을 위하여」(『창작과비평』 1992년 겨울호/통권 78호).
- 『분단체제 변혁의 공부길』(1994)은 이 글을 포함·보론 추가한 첫 단행본.
- claim-001의 source_detail("『분단체제 변혁의 공부길』, 「분단체제의 인식을 위하여」")과 context
  ("1992년 논문 … 기점으로 본격화")는 학술적 사실과 일치.
- 월러스틴 세계체제론·그람시 헤게모니론 영향 언급도 다수 2차 문헌(paiknakchung.net, changbi 매거진)에서 확인됨.

#### 3.2 변혁적 중도주의 (claim-002, kw-byeonhyeok-jungdo)
- 『변혁적 중도론』(창비, 2016) 단행본으로도 집약된 개념. 실제 텍스트 초기 용례는 2000년대 중반 이후 평론.
- claim-002가 `work_id=baek-hanbando-tongil`로 한반도식 통일(2006)에 귀속된 것은 광의로 허용 가능(동시기 논의).
  단, 보다 정확한 주저는 『변혁적 중도론』이지만 해당 저서는 DB에 없어 차선의 귀속으로 판단. **허용**.

#### 3.3 87년체제론 (claim-003, kw-87nyeon-cheje)
- 2005~2007년 『창작과비평』 지면 87년체제 논쟁, 김종엽·조희연 공동 논의 등 서술은
  한국민족문화대백과사전의 87년체제 항목과 정합.
- `2013년체제`는 『2013년체제 만들기』(창비, 2012)로 정리됨 — Coder의 philosophical_journey 서술과 일치.

#### 3.4 민족문학론 (claim-004, kw-minjok-munhakron)
- 「민족문학 개념의 정립을 위해」는 1974년에 발표되었고 1978년 평론집 『민족문학과 세계문학 I』(창작과비평사)에 수록.
- claim-004 source_detail 기재 형식("(1974) 및 후속 평론") 정확.

#### 3.5 흔들리는 분단체제 (claim-005, kw-heundeulineun-bundan)
- 탈냉전(1989~91), 한·중 수교(1992), 남북기본합의서(1991) 등 argument의 역사적 근거 모두 사실관계 정확.

#### 3.6 한반도식 통일 (claim-006, kw-hanbandosik-tongil)
- 6·15공동선언 제2항 "남측의 연합제안과 북측의 낮은 단계의 연방제안의 공통성" 인용은 원문과 일치.
- "완전한 통일·1회성 사건이 아닌 과정으로서의 통일" 논지는 교재(경향·프레시안 리뷰)에서 확인됨.

#### 3.7 창작과비평 (claim-007, kw-changjak-bipyeong)
- 창간(1966), 강제 폐간(1980, 전두환 정권), 복간(1988) 연도 모두 사실관계 정확.

### 4. Thinker 정보 검증 (배경·경력)

웹 교차검증 결과 몇 가지 **부정확·오차**가 발견됨:

1. **서울대 재직 기간**: coder = "서울대학교 영문학과 교수(1972~2003)"
   - 실제: **1962년부터** 서울대 영문과 재직 시작(전임강사 → 조교수 단계), 1972년 하버드 박사 취득, 1974년 유신 반대 성명으로 해직(→1980 복직), 2003년 정년퇴임.
   - 즉 "1972~2003"은 박사학위 이후 재직 기간으로 해석할 여지는 있으나, 일반적으로 백낙청 약력은 "1962년 서울대 영문과 부임 / 2003년 정년퇴임"으로 기재한다.
   - background 서술이 학문적 공백(1974~1980 해직 기간)을 누락.
   - **severity: observation** — DB 유용성에 치명적이지 않으나 장기적으로 수정 권장.

2. **대구 출생 표현**: background = "대구 출생"
   - 실제: "외가(대구)에서 태어나 성장" — 본적·출신 가문은 수원 백씨. 간략화는 허용 가능.
   - **severity: observation**.

3. **회갑 후반부 사회활동**: 6·15공동선언실천 남측위 상임대표, 한반도평화포럼 공동이사장 — 실제 직함 확인됨. 일치.

### 5. 필드명 일관성 문제 (Coder report에서도 이슈로 지적)

- architecture.md §3 ethics-claims 스키마는 `original_text` 로 정의.
- 본 스크립트는 모든 claim에 `original_text_ko` 필드를 사용 → **스키마 불일치**.
- 다른 인서트 스크립트(예: insert_mozi/kohlberg 등) 다수는 `original_text` 를 사용하는 것으로 확인 필요.
- ES 매핑이 dynamic이라 입력 자체는 성공하였으나, 향후 **검색/export 시 필드 이름 분기**가 발생할 위험.
- **severity: observation** (검색 파이프라인에 통합되는 시점에 필드 통일 후속 태스크 필요).

### 6. argument / counterpoint 정합성

7개 claim 모두:
- argument: 해당 주장을 뒷받침하는 **논리 구조**(역사적 사실 + 이론적 전제) 제시, 근거 인용 정확.
- counterpoint: 보수·자유주의·탈민족주의·진보 좌파 등 **실제 존재하는 학술·정치 비판**을 기재. 가공이나 허위 비판은 관찰되지 않음.
  - 예: 문지 그룹(김현 등)의 민족문학론 비판, 최장집과의 평화체제 논쟁, 진보 좌파의 "중도주의=타협" 비판 — 모두 실제 문헌 근거 있음.

### 7. keywords 정의

7개 keyword 모두 `term / term_en / definition / thinker_id / work_id / related_terms` 필드 완비.
term_en 번역(Division System Theory, Transformative Centrism 등)은 영문 학술계에서 실제 사용되는 번역과 일치.

## 이슈/블로커

- **BUG 없음** — claim 본문·저서 연도·키워드 정의·창간/폐간 사실 등 핵심 사실 모두 정확.
- **OBSERVATION (후속 태스크 권장)**
  1. claim 전 건의 `original_text_ko` 필드를 스키마 정의인 `original_text` 로 맞추는 일괄 수정(타 사상가 데이터와의 일관성 확보). Manager 결정 사항.
  2. thinker `background` 의 서울대 재직 기간 표기(1972~2003 → 1962~2003, 1974 해직/1980 복직 각주 추가) 미세 보정.

두 항 모두 현 단계 학습 자료로서의 활용성에 영향을 주는 결함이 아니므로 `severity: observation` 으로 분류.

## 다음 제안

1. 본 태스크는 DONE 처리 가능.
2. Manager는 `original_text` vs `original_text_ko` 정책을 공식 결정하고, 필요 시 전 사상가 대상 스키마 정합 태스크를 생성(권장).
3. Phase 5 잔여 인물(갈퉁·강만길·듀이·아렌트) 입력 태스크로 진행.
4. 영향원(월러스틴·그람시) 관계는 해당 사상가가 DB에 등록되는 시점에 relation 태스크로 다시 검토.
