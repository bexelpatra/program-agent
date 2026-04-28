---
agent: coder
task_id: TASK-176-01
status: DONE
timestamp: 2026-04-22T00:00:00
---

## 결과 요약

보조국사 지눌(知訥, 1158~1210, 고려 조계종 중흥조)을 ES ethics-thinkers 인덱스에 신규 등록하고, 부속 works/claims/keywords/relations 를 함께 투입하였다. 출제 7회 누적(2016-A, 2017-A, 2020-A, 2021-B, 2022-A, 2025-B, 2026-B)의 blocker 7건 해소 기반 마련.

## 산출 파일

- `projects/ethics-study/scripts/insert_jinul.py` (신규)
- ES 투입: `ethics-thinkers/jinul` + `ethics-works` 5건 + `ethics-claims` 9건 + `ethics-keywords` 9건 + `ethics-relations` 2건

## 스크립트 구조

`insert_wonhyo_huineng.py`·`insert_lickona.py` 선례 템플릿을 따라 다음 순서로 구성:

1. `ensure_field(client)` — `eastern_ethics` 존재 확인 (이미 등록, skip)
2. `insert_thinker(client)` — jinul 사상가 문서 (background 12줄·core_philosophy 10줄·philosophical_journey 7줄·keywords 9개)
3. `insert_works(client)` — 5종: 수심결, 권수정혜결사문, 진심직설, 간화결의론, 법집별행록절요병입사기
4. `insert_claims(client)` — 9개 (돈오점수, 정혜쌍수, 자성정혜/수상정혜, 공적영지, 성적등지, 정혜결사, 간화선, 선교일치, 계정혜삼학)
5. `insert_keywords(client)` — 9개 (중복 체크 포함 — `client.get()` 성공 시 skip)
6. `insert_relations(client)` — 2개 (huineng→jinul, wonhyo→jinul). zongmi/uicheon/taego 등 ES 미등록 thinker 는 링크 제외.

`main()`은 각 단계별 try/except 로 오류 발생 시 stderr 출력 후 재raise.

## ES 실측 결과

```
$ curl -s localhost:9200/ethics-thinkers/_doc/jinul | jq .found
true

$ curl -s "localhost:9200/ethics-claims/_count" -H 'Content-Type: application/json' -d '{"query":{"term":{"thinker_id":"jinul"}}}'
{"count":9,...}

$ curl -s "localhost:9200/ethics-works/_count" -H 'Content-Type: application/json' -d '{"query":{"term":{"thinker_id":"jinul"}}}'
{"count":5,...}

$ curl -s "localhost:9200/ethics-keywords/_count" -H 'Content-Type: application/json' -d '{"query":{"term":{"thinker_id":"jinul"}}}'
{"count":9,...}
```

완료 조건 3번 (claims ≥ 8, works ≥ 5, keywords ≥ 7) 모두 충족.

## 원문 인용 규칙 준수 (agents/coder.md §원문/입력 인용 규칙)

claims.original_text 는 coverage 문서에서 실측된 verbatim 원문 또는 권위 출처 인용만 기재했다. 확증 불가 구절은 **빈 문자열**(`""`)로 남기고 explanation/context 에 해설만 기술했다.

**original_text 기재한 claim 4건** (coverage 문서 실측 근거):
- `jinul-claim-001` (돈오점수): 2020-A Q3 제시 원문 — "심성(心性)이 본래 깨끗하고 번뇌가 본래 텅 비어 있음을 깨달았기 때문에, 점문(漸門)의 오염된 수행에는 떨어지지 않는다" (『법집별행록절요병입사기』)
- `jinul-claim-003` (자성정혜/수상정혜): 2020-A Q3 제시 원문 verbatim — "번뇌가 엷고 몸과 마음이 가볍고 편안하여… '자성정혜(自性定慧)'… '수상정혜(隨相定慧)'를 빌려서 다스려야" (『법집별행록절요병입사기』)
- `jinul-claim-004` (공적영지): 2022-A Q2 제시 원문 + 한자 원문 — "諸入理之門 不出定慧 撮其要 卽自性上體用二義 前所謂空寂靈知是也 定是體 慧是用也" (『수심결』)
- `jinul-claim-008` (선교일치): 2021-B Q1 제시 원문 — "관(觀)을 배우지 않고 경전만을 공부하면…" (지눌이 스승의 말을 인용한 형식)

**original_text 공란(`""`) 처리한 claim 5건** (verbatim 원문 확증 불가):
- `jinul-claim-002` (정혜쌍수) — 『권수정혜결사문』 원문 한자 verbatim 확증 보류
- `jinul-claim-005` (성적등지) — 성성적적 원문 verbatim 확증 보류
- `jinul-claim-006` (정혜결사 의의) — 『권수정혜결사문』 해당 구절 verbatim 확증 보류
- `jinul-claim-007` (간화선 수용) — 『간화결의론』 verbatim 확증 보류
- `jinul-claim-009` (계정혜 삼학) — 삼학 총론 관련 verbatim 원문 확증 보류

ES 실측으로 검증: `curl -s ethics-claims/_doc/jinul-claim-NNN | jq '._source.original_text | length'` → 각각 107 / 0 / 325 / 242 / 0 / 0 / 0 / 194 / 0 문자.

## 관찰 사항

1. **관계 링크 축소**: 태스크 지시의 후보 관계 중 `zongmi`(규봉 종밀), `taego`(태고 보우), `uicheon`(대각국사 의천) 모두 ES 미등록이므로 링크 제외. `huineng`(돈오 사상 계승)·`wonhyo`(한국 불교 통합 전통 계보) 2건만 실제 링크. 지눌 사상 계보상 가장 중요한 **규봉 종밀** 관계가 끊긴 상태이므로, 후속 태스크로 `zongmi`·`uicheon`·`taego` 등록을 권고한다. 이는 2021-B BLK-175E-2021B-001(의천) 해소와도 직결된다.

2. **간화결의론 간행 연도 이견**: 스크립트에 year=1215로 기재했으나, 일부 문헌은 지눌 입적 전(1209~1210)으로 비정하기도 한다. 통설(혜심 간행 1215)을 채택했다.

3. **keyword 중복 방지**: `insert_keywords()` 는 `client.get()` 으로 기존 문서 존재 확인 후 없을 때만 insert (태스크 지시의 "중복 체크 후 insert" 요건 준수). 9개 키워드 모두 신규 created.

4. **공적영지 claim-004 에 한자 원문 직접 포함**: 2022-A coverage 문서에 실측된 『수심결』 한자 원문 "諸入理之門 不出定慧 撮其要 卽自性上體用二義 前所謂空寂靈知是也 定是體 慧是用也" 는 권위 출처에서 직접 추출 가능하여 원문 인용 규칙에 부합. 번역문(한글)은 2022-A Q2 제시문 verbatim.

5. **blocker 해소 범위**: 본 태스크로 해소 가능한 blocker는 Manager 할당 목록(BLK-175E-2016A-002, 2020A-001, 2021B-001/002, 2022A-001, 2025B-001, 2026B-002) 중 지눌에 직접 귀속되는 것. 2021-B의 `uicheon`(의천) 미등록 blocker(BLK-175E-2021B-001)는 본 태스크 범위 밖이다.

## 이슈/블로커

없음.

## 다음 제안

1. `uicheon`(대각국사 의천) 등록 태스크 — 2021-B Q1 '갑' blocker 해소 + 지눌 선교일치 대비 구도 완성.
2. `zongmi`(규봉 종밀) 등록 — 지눌의 직접적 사상 계승원(공적영지·돈오점수설) 관계 링크 완성.
3. `taego`(태고 보우) 등록 — 조계종 법맥 계승 관계 완성.
