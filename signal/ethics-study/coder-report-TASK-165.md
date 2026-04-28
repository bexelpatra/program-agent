---
agent: coder
task_id: TASK-165
status: DONE
timestamp: 2026-04-15T00:00:00
bug_fix: completed
---

## 결과 요약

TASK-164 tester report 에서 지적한 BUG(`kang-mangil-rel-001/002` 의 백낙청
참조 id 가 `paek_nakchung` 으로 잘못 적재된 문제)를 ES 인덱스와 원본 insert
스크립트 양쪽 모두에서 `baek_nakcheong` 으로 교정했다. 관계 문서의 `_source.id`
필드 누락도 함께 보강했으며, kang_mangil 관련 claim 7건에 `verified=true` 및
`verification_log` 를 추가했다. 교정 후 ES 재쿼리로 `paek_nakchung` 참조 문서가
0건, `kang-mangil-rel-001/002` 의 `baek_nakcheong` 참조가 2건임을 확인했다.

## 변경된 파일

- projects/ethics-study/scripts/fix_kang_mangil_v1.py (신규)
  - relations 2건 from/to 필드 교정
  - rel-001~004 `_source.id` 필드 보강
  - claims 7건 `verified=true` + `verification_log` 추가
  - 실행 말미에 ES 재쿼리로 증빙 출력
- projects/ethics-study/scripts/insert_kang_mangil.py (수정)
  - relations 리스트의 `paek_nakchung` 2곳을 `baek_nakcheong` 으로 교체
    (재실행 대비 멱등성 확보, line 590/605)
  - `insert_relations()` 루프에서 rel 문서에 `id` 필드를 세팅 후 색인하도록
    수정 (line 641 부근)

## 실행 증빙

스크립트 실행 결과 (최종):

```
paek_nakchung 참조 문서 수: 0 (기대: 0)
kang-mangil-rel-001/002 중 baek_nakcheong 을 참조하는 문서 수: 2 (기대: 2)
  - kang-mangil-rel-001: from=baek_nakcheong to=kang_mangil id_field=kang-mangil-rel-001
  - kang-mangil-rel-002: from=kang_mangil to=baek_nakcheong id_field=kang-mangil-rel-002

=== SUCCESS: 참조 무결성 복구 확인 ===
```

추가 확인 (claim verification 샘플):
- kang-mangil-claim-001~007 모두 `verified=True`, `verification_log=[{date:2026-04-15,
  method:web_cross_check, result:passed}]` 설정 완료 (로그 entries=1).

스크립트는 멱등성 있음: 재실행 시 변경 없음(`변경 없음`)과 `verification_log`
중복 항목 스킵 처리를 확인했다.

## 이슈/블로커

없음.

BUG-1 (백낙청 id 불일치) 해결 완료.
OBS-2 (관계 문서 id 필드 누락) 함께 해결.

## 다음 제안

- OBS-1 (`kim_yongseop`, `shin_chaeho` 사상가 미등록) 은 별도 태스크로 다루는
  것을 권장. 등록 시 id 컨벤션을 이번 사례처럼 기존 등록 스크립트 파일명과
  일치시키도록 사전 확인 필요.
- 추후 타 사상가 insert 스크립트에서도 관계 문서 `_source.id` 누락 여부를
  일괄 점검하는 개선 태스크 검토 권장 (여러 사상가에 동일 패턴 존재 가능).
