---
task_id: TASK-038,TASK-039,TASK-040,TASK-041
verdict: PASS
---

# Reviewer Report v2: TASK-038 ~ TASK-041 (재검증)

## 검증 대상
- `signal/abc-english/task-board.md` 라인 51~54 (Phase 9 보강본)
- 이전 NEEDS_REVISION 보고서: `signal/abc-english/reviewer-report-TASK-038-041.md`

## 이전 지적사항 vs 수정본 대조

| # | 지적 항목 | 수정 반영 | 근거 (task-board.md) |
|---|-----------|-----------|----------------------|
| 1 | TASK-038: mapping/shards/analyze 명령 + 5개 소제목 + Kibana 접속 경로 | 반영 | 라인 51: `GET /{index}/_mapping`, `GET /_cat/shards/abc-*?v`, `POST /{index}/_analyze {...}` / 5개 소제목(역색인 원리 / analyzer 파이프라인 / shard·replica / mapping 타입 / dynamic mapping) / `http://localhost:5601 → Dev Tools` 명시 |
| 2 | TASK-039: 10종 쿼리 인덱스·필드 바인딩 + nested 사전 확인 + 결과 요약 포맷 | 반영 | 라인 52: ①~⑩ 각 쿼리에 `→abc-xxx.필드` 바인딩 완료, nested 항목에 `GET /abc-vocabulary/_mapping`으로 선확인 지시, 결과 포맷 `hits.total.value / took(ms) / 상위 3 hit 3줄` 명시 |
| 3 | TASK-040: mkdir + Kibana 5601 + Data View `abc-*`+time field + Lens 4종 집계 스펙 + 대시보드명 + Export 절차 | 반영 | 라인 53: `mkdir -p projects/abc-english/kibana`, 포트 5601, Data View `abc-*` time field `published_date`, Lens 4종 각각 집계 타입/필드/source 인덱스 명시, 대시보드명 `ABC English Learning Overview`, Export 경로 `Stack Management → Saved Objects → Export (include related) → .../kibana/dashboards.ndjson` |
| 4 | TASK-041: 질문→3~5줄 답변→예제 1개 포맷 + ES vs RDB 3축 비교 | 반영 | 라인 54: "질문 → 3~5줄 답변 → abc-english 인덱스 기반 예제 1개", "ES vs RDB — join/스키마/확장성 3축 필수 비교" 명시 |
| 5 | 전 태스크에 "학습 노트 성격(본인 문장)" 명시 | 반영 | 038/039/040/041 모두 description 말미에 "학습 노트 성격: ... 본인 문장" 포함 |
| 6 | architecture.md kibana/ 디렉토리 각주 | 대체 반영 | TASK-040에 `mkdir -p projects/abc-english/kibana` 명시로 Coder 실행 시 누락 위험 제거. architecture 각주는 불필요. |

## 추가 점검

- **의존성 체인**: TASK-038→039→040→041 선형, 선행 TASK-022 DONE 상태 유지 확인.
- **TASK-028**: DONE + "(분해됨 → TASK-038~041)" 표기 유지.
- **인덱스/필드 명칭 일관성**: 바인딩된 필드(`word.keyword`, `difficulty.keyword`, `avg_wer`, `published_date`, `type.keyword`, `example_sentences`)는 이전 v1 검증에서 `src/models.py` INDEX_MAPPINGS와 일치 확인 완료. 재확인 불필요.
- **완결성**: TASK-040의 "Lens 집계 스펙"이 Coder가 UI 조작 없이도 Kibana 공식 문서와 대조해 실행할 수 있는 수준으로 기재됨.

## 판정
**PASS**

이전 6개 지적사항이 모두 task-board.md 라인 51~54에 반영되었다. Coder 호출 가능.

## Manager에게 전달
- TASK-038부터 순차 실행 가능. Phase 9는 학습 노트 성격이므로 Coder report에 "본인 문장 비율"이 반영되었는지 DONE 마감 시 확인 권장.
- TASK-040은 Kibana 수동 조작이 포함되므로 Coder가 실행 불가(UI 접근 권한 없음)하다고 보고하면 `Execution: user` 태스크로 전환 고려.
