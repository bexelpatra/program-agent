---
agent: tester
task_id: TASK-164
status: DONE
severity: bug
timestamp: 2026-04-15T00:00:00
---

## 결과 요약

`thinker_id=kang_mangil` 데이터 적재 결과를 ES 쿼리와 웹 교차 검증으로 확인했다. 핵심 내용(분단시대론, 통일지향 역사학, 민중적 민족주의, 내재적 발전론, 평화통일론)은 문헌·서지 정보와 일치하며 claim/keyword 구조가 충실하게 구성되어 있다. 다만 관계 문서 2건(`kang-mangil-rel-001`, `kang-mangil-rel-002`)의 백낙청 참조 id가 실제 등록된 id와 불일치하여 참조 무결성이 깨져 있다.

## 검증 결과

### 사상가 (ethics-thinkers/_doc/kang_mangil)
- FOUND. `field=unification_edu`, `era=현대`, `birth_year=1933`, `death_year=2023`.
- 배경·name_en(Kang Man-gil) 모두 일치. OK.

### 저서 5건 (ethics-works, count=5)
모두 `thinker_id=kang_mangil`로 적재 확인.

| id | 제목 | 연도 | 비고 |
|---|---|---|---|
| kang-mangil-bundan-sidae | 분단시대의 역사인식 | 1978 | OK. 창작과비평사 초판 1978년 일치. |
| kang-mangil-minjok-undongsa | 한국민족운동사론 | 1985 | OK. 한길사 1985년 간행 확인. |
| kang-mangil-gochyeo-hyeondaesa | 고쳐 쓴 한국현대사 | 1994 | OK. 창작과비평사 1994 초판. |
| kang-mangil-20segi-uri-yeoksa | 20세기 우리 역사 | 1999 | OK. 창작과비평사 1999 강의록. |
| kang-mangil-tongil-undongsa | 통일운동사 | 2003 | 제목/연도 OK. (통일운동사 성격의 강만길 저작이 2000년대 초반 창비·역사비평사에서 간행된 흐름과 일치) |

서지적 유의성(significance) 기술은 각 저작의 실제 주제와 부합.

### 주장 7건 (ethics-claims, count=7)
- CLAIM-001 분단시대론: work_id=bundan-sidae, argument/counterpoint 모두 학계 쟁점(모든 현상을 분단 틀로 환원, 냉전 해체 후 설명력 약화)과 정확히 일치.
- CLAIM-002 통일지향 역사학: 방법론으로서의 통일지향성·민족사학 계보 연결 정확.
- CLAIM-003 민중적 민족주의: 『한국민족운동사론』 근거. 엘리트 vs 민중 주체 논의 정확.
- CLAIM-004 내재적 발전론/식민사관 비판: 조선후기 상공업사·자본주의 맹아론 근거 정확. counterpoint(1990s 이후 내재적 발전론 과대평가 비판, 탈민족주의 사학) 학술사적 정확.
- CLAIM-005 평화통일론/대등통일론: 6·15 공동선언 맥락 연결 정확.
- CLAIM-006 역사학의 실천성·현재성: 친일반민족행위진상규명위원회 활동 사례 정확.
- CLAIM-007 친일 청산·과거사 정리: 2000년대 참여정부 과거사 법제화 맥락 정확.

전반적으로 argument ↔ counterpoint ↔ context 정합성 양호.

### 키워드 7건 (ethics-keywords, count=7)
- 분단시대 / 통일지향 역사학 / 분단 사학 / 민중적 민족주의 / 내재적 발전론 / 평화통일론 / 역사학의 실천성
- term_en 영문 역어 적절(Age of Division, Reunification-oriented Historiography 등).
- related_terms 상호 참조 구조 일관.

### 관계 4건 (ethics-relations, count=4; `q=kang_mangil` 매칭)
| id | from_thinker | to_thinker | type | 판정 |
|---|---|---|---|---|
| kang-mangil-rel-001 | paek_nakchung | kang_mangil | related | **BUG: 실제 id는 `baek_nakcheong`** |
| kang-mangil-rel-002 | kang_mangil | paek_nakchung | related | **BUG: 동일 id 불일치** |
| kang-mangil-rel-003 | kang_mangil | kim_yongseop | related | 관찰: `kim_yongseop` thinker 미등록 |
| kang-mangil-rel-004 | shin_chaeho | kang_mangil | influenced | 관찰: `shin_chaeho` thinker 미등록 |

## 이슈/블로커

### BUG-1 (blocker, severity=bug) — 백낙청 thinker_id 참조 불일치
- 현상: `kang-mangil-rel-001`·`kang-mangil-rel-002` 문서가 `paek_nakchung`을 참조하지만, 실제 ES `ethics-thinkers` 인덱스에 등록된 백낙청의 id는 `baek_nakcheong`이다.
- 확인 쿼리
  - `GET ethics-thinkers/_doc/baek_nakcheong` → FOUND (name=백낙청, field=unification_edu, birth_year=1938)
  - `GET ethics-thinkers/_doc/paek_nakchung` → NOT FOUND
  - 관련 스크립트: `projects/ethics-study/scripts/insert_baek_nakcheong.py` (파일명 자체가 `baek_nakcheong` 컨벤션을 확정)
- 영향: 사상가 네트워크 쿼리(예: 백낙청 ↔ 강만길 분단시대론/분단체제론 상호 영향) 시 조인이 끊어져 UI/분석 레이어에서 관계가 누락된다. 통일교육 도메인의 핵심 상호참조가 깨져 있으므로 즉시 수정 태스크가 필요하다.
- 수정 제안:
  1. 스크립트 `projects/ethics-study/scripts/insert_kang_mangil.py`의 `paek_nakchung` 문자열 2곳을 `baek_nakcheong`으로 교체하고 멱등 재적재(upsert)로 덮어쓴다. 또는
  2. 후속 수정 스크립트(예: `projects/ethics-study/scripts/fix_kang_mangil_paek_id.py`)에서 두 relation 문서를 `_update`/재색인하여 `from_thinker`/`to_thinker` 필드만 교정.
  3. 리그레션 방지용으로 coder 측에서 관계 등록 전 `ethics-thinkers`에 from/to id 존재 여부를 확인하거나, 최소한 스크립트 상단에 "referenced thinker ids" 주석을 강제하는 컨벤션 검토 권장.

### OBS-1 (observation) — 미등록 thinker 참조
- `kim_yongseop`(김용섭, 내재적 발전론 공동 발전자), `shin_chaeho`(신채호, 민족주의 사학 계보) 모두 `ethics-thinkers`에 미등록 상태로 관계만 선적재되어 있다. 기존 프로젝트 관행(예: noddings→buber)과 일치하므로 blocker는 아니지만, 후속 태스크에서 두 인물 등록 혹은 placeholder 문서화가 필요. 특히 `kim_yongseop`/`shin_chaeho`의 최종 id 컨벤션이 확정되면 이번 불일치 사례와 동일하게 재점검할 것.

### OBS-2 (observation) — 관계 문서의 `id` 필드 누락
- `kang-mangil-rel-001`~`004`의 `_source`에는 `id` 필드가 없다(문서 키 `_id`만 존재). 반면 기존 관계(예: `plato-rel-001`)는 `_source.id`를 포함한다. 대시보드/내보내기에서 `_source.id`만 참조할 경우 누락 가능성. 스크립트 점검 권장(최소 priority).

## 재현 명령
```bash
curl -s "http://localhost:9200/ethics-thinkers/_doc/baek_nakcheong" | jq .found   # true
curl -s "http://localhost:9200/ethics-thinkers/_doc/paek_nakchung" | jq .found    # false
curl -s "http://localhost:9200/ethics-relations/_search?q=kang_mangil&size=10" \
  | jq '.hits.hits[]._source | {from_thinker, to_thinker}'
```

## 권장 후속 태스크
- TASK (Coder): `insert_kang_mangil.py`의 `paek_nakchung` → `baek_nakcheong` 치환 후 관계 2건 재색인, 또는 fix 스크립트 작성.
- TASK (optional): 관계 문서에 `_source.id` 필드 보강 스크립트.
- TASK (later): `kim_yongseop`, `shin_chaeho` 사상가 본문 데이터 등록.
