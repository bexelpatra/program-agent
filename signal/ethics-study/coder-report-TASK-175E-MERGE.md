---
agent: coder
task_id: TASK-175E-MERGE
status: DONE
timestamp: 2026-04-22T00:11:18
---

## 결과 요약

Phase 6 MERGE 산출물 완료. `merge_coverage.py` 스크립트를 신규 작성하여 26개
coverage 파일(2014-A~2026-B)을 파싱·집계하고, 통합 커버리지 맵
`exam-coverage-map.md`를 렌더링했다. ES pre-flight(cluster yellow,
ethics-thinkers=55, canonical 55 dump) · blocker-log 교차 검증
(93 issued / 1 withdrawn / **net active 92**) · 배점 검산(2014-A 50점 /
2014-B 30점 / 2015+ 40점 × 24개 → **전 26개 OK**) 모두 통과.

## 변경된 파일

- `projects/ethics-study/scripts/merge_coverage.py` (신규, ~700 lines)
- `projects/ethics-study/exam-solutions/exam-coverage-map.md` (신규, 20996 bytes)
- `signal/ethics-study/coder-report-TASK-175E-MERGE.md` (신규, 이 파일)

v1-rejected / v2-rejected md 파일은 수정 없음 (mtime 미변경):
- `projects/ethics-study/exam-solutions/exam-coverage-map.v1-rejected.md` (2026-04-19 23:32 — 수정 없음)
- `projects/ethics-study/exam-solutions/exam-coverage-map.v2-rejected.md` (2026-04-20 00:26 — 수정 없음)

`src/`, `tests/` 디렉토리 미수정.

## 구현 주요 사항

### 2-path 파서 (구형 17 + 신형 9)
- 구형(2014-A ~ 2022-A): 파일 상단 요약 테이블 1개.
- 신형(2022-B ~ 2026-B): 파일 말미 전체 요약 테이블. 문항별 mini table과
  재출제 연속성 보조 표를 배제하기 위해 `has_q AND has_score` 조건으로
  선별(문항/배점 둘 다 있는 테이블만).

### 동적 헤더 매핑
- `thinker_id` / `배점` / `ES 커버리지`·`ES 상태`·`ES` / `문항`·`Q` / `분류`·`유형`
  키워드로 소문자 lookup. 9종+ 헤더 변형 지원 확인.

### thinker_id 추출
- 주: `` `[a-z][a-z0-9_]*` `` (백틱 감싼 id). architecture.md L491 suffix 규약 준수
  (`taylor` vs `taylor_p` 엄격 분리).
- 보조: 백틱 없는 구형 파일(2014-A/2014-B 등 bare id `confucius`·`spinoza`)용
  bare id regex + canonical 55 ∪ MISS_NAME_MAP 알려진 id 필터.

### 컬럼 오프셋 보정 (데이터 row가 헤더보다 셀 수가 많은 경우)
1. **테이블 전체 shift**: row 셀 수가 `header_len + k` 가 dominant이면
   후보 shift k 중 `thinker_id` 백틱 id 최빈 매칭 위치 선택. 2018-A/2019-A에서
   1칸 shift 검출.
2. **row-level shift**: 현재 thinker 셀이 "—" 단독이고 바로 옆 셀에 백틱 id
   있으면 해당 셀로 이동 (엄격 조건만 적용하여 false shift 방지).
3. **unescaped pipe 깨진 row 구제**: row 셀 수가 header_len보다 3+ 많고
   thinker_id 비어있으면 row 전체에서 백틱 id 스캔 (2020-B Q11, 2021-A Q5,
   2022-A Q10 구제 — 이들은 원문 markdown에서 `|` 미이스케이프로 파싱 깨짐).
4. **escaped pipe** (`\|`): `_PIPE_PLACEHOLDER` 치환 후 split, 복원. 2018-A Q2
   `"창의적 사고 역량 \| (     )"` 등 정상 처리.

### Section 분류 로직 (classify_row)
- **thinker**: 백틱 id 존재 + 분류가 사상가형(복합이어도 사상가형 명시).
- **boundary_with_thinker**: 백틱 id 존재 + 분류가 교과교육학·경계영역·
  일반개념·메타윤리. 사상가 집계와 Section C 양쪽 모두 노출.
- **boundary**: id 없음 + 분류가 교과교육학·경계영역·일반개념·메타윤리.
- **pending**: id 없음 + 위 조건 미충족 (BLOCKER-PENDING 포함).

### ES pre-flight + blocker-log 교차 검증
- Cluster health `yellow` 확인 (green/yellow 중 1).
- `ethics-thinkers` 카운트 55 일치.
- canonical 55 dump (id → 한글명) 취득 후 `_lookup_name`에서 사용.
- `ethics-claims` terms aggregation으로 thinker별 claim 수 산출.
- `blocker-log.md` 파싱: `### BLK-175E-YYYY[AB]-NNN ...` 93 entries issued.
  `철회` 또는 `FALSE-POSITIVE` 마커 1건 (BLK-175E-2025A-003) → net 92 확인.

## 출력 맵 통계

```yaml
generated_at: 2026-04-22 00:11:18
coverage_files: 26
canonical_thinkers: 55
total_question_rows: 293
total_id_mentions: 359
MISS_thinkers_covered: 45   # Section A
HIT_thinkers_covered: 49    # Section B 출제횟수>0
Section_C_rows: 65          # boundary/pending
blockers_issued: 93
blockers_withdrawn: 1
blockers_net_active: 92
es_cluster_status: yellow
score_sum_verification: ALL_OK (26/26 년도 일치)
```

### Section B 상위 canonical 10
`kant`=16, `kohlberg`=15, `mill_js`=14, `rawls`=13, `zhuxi`=12, `aristotle`=10,
`rest`=8, `wangyangming`=8, `zhuangzi`=8, `jeongyagyong`=7.

### Section D TOP10 (TASK-176 우선순위)
1. `jinul` 7회 (최최우선·5회+)
2. `blasi` 5회 (최최우선)
3. `durkheim` 5회 (최최우선)
4. `hoffman` 5회 (최최우선)
5. `bandura` 4회 (최우선·3회+)
6. `pettit` 4회 (최우선)
7. `singer` 4회 (최우선)
8. `turiel` 4회 (최우선)
9. `moore` 3회 (최우선)
10. `narvaez` 3회 (최우선)

### taylor / taylor_p 분리 검증
- `taylor` (찰스 테일러, canonical 55, ES 등록): Section B #45, 2회 출제
  (2016-B, 2021-A). claims 6.
- `taylor_p` (폴 테일러, ES 미등록, 생명중심주의): Section A #17, 2회 출제
  (2021-A, 2026-A). BLK-175E-2021A-003, BLK-175E-2026A-002/003.
- 혼동 없음 (architecture.md L491 규약 준수 확인).

### 배점 검산 (Section E)
- 전 26개 년도 `score_sum == expected` (2014-A 50, 2014-B 30, 2015+ 40 × 24).
- 합계 1040점 (50+30+40×24=50+30+960=1040 일치).

## 이슈/블로커

### observation (태스크화 불필요, 참고용)

1. **원문 coverage 파일의 unescaped `|` 문자**: 2020-B Q11, 2021-A Q5, 2022-A Q10
   3개 row에서 본문 내부에 `|`가 이스케이프 없이 포함되어 있어 cell 분해가 깨짐.
   → row 전체 스캔 fallback으로 thinker_id는 정상 추출(shenxiu/huineng/zhiyi
   등 전부 포함). 단 Section C의 분류·원문 셀 요지 표시가 일부 부정확하게 나옴.
   원본 coverage md를 수정하지 않는다는 태스크 규정에 따라 데이터 품질 이슈로
   남김(스크립트는 robust fallback으로 핵심 집계는 보존).

2. **MISS_NAME_MAP 수동 엔트리**: `shaftel`(샤프텔 역할놀이), `shenxiu`(북종 신수),
   `donghak_choe`(동학), `machiavelli`, `newmann` 5건을 코드 내 매핑에 추가.
   장기적으로는 TASK-176에서 ES 등록 후 ES로부터 실시간 fetch하도록 전환 권장.

3. **Section C 중 2014-A "(없음/누락)" 5건**: 2014-A 원문 coverage의 기입형
   1·3·5·13·14·서술형 1 등 thinker_id가 공백인 row. 이는 2014년 구형 임용
   문항이 사상가 확정되지 않은 순수 개념·교과교육학형이거나 원본 coverage에서
   귀속 미완 상태일 수 있음. 추가 조사는 TASK-175E 스코프 밖.

## 다음 제안

1. **TASK-176 착수**: Section D TOP10 순서(`jinul`→`blasi`→`durkheim`→
   `hoffman`→`bandura`→`pettit`→`singer`→`turiel`→`moore`→`narvaez`)로
   ethics-thinkers 인덱스에 10인 신규 등록.
2. **원문 coverage 파일 품질 개선 (선택)**: 별도 독립 태스크로 2020-B Q11,
   2021-A Q5, 2022-A Q10의 unescaped `|` 3곳을 `\|`로 치환하면 Section C
   표시가 완전해진다. 단 집계에는 영향 없음.
3. **exam-coverage-map.md 자동 갱신 파이프라인 (선택)**: ES claims 추가 시
   merge_coverage.py 재실행으로 HIT/MISS 재집계 가능. 새 coverage md 추가
   시에도 OLD_FORMAT_FILES/NEW_FORMAT_FILES 리스트에 파일명만 추가.
