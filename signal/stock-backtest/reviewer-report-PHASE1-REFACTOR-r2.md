---
task_ids: TASK-231, TASK-233, TASK-234, TASK-237, TASK-238
verdict: PASS
round: 2
---

# Reviewer Report: Phase 1 Refactor R2 (정정 검증)

검증 일자: 2026-04-30
검증 방식: task-board.md L159-208 정독 + 4개 spot-check (asset_repository.py 경로, new/page.tsx:96 라인, UniverseSelector.tsx:27-29, all_weather.py:60-79).

## 정정 반영 확인

| 지적 | 반영 여부 | 근거 |
|------|--------|------|
| 1. TASK-231 allow_empty 옵션 | PASS | task-board L168 — "fixed_weight / ma_signal 4단계 + all_weather 3단계 (empty 검사 생략, 별도 `_validate_categories` (L74-79) 가 처리)" 명시 + 시그니처 `validate_weight_dict(v, *, name, total_tolerance=0.05, allow_empty=False)` + "all_weather 호출 시 `allow_empty=True`" 명시. 단위 테스트에 "allow_empty=True 통과" 분기 추가됨. all_weather.py:60-79 실측 (3단계 + `_validate_categories` 별도) 과 일치. |
| 2. TASK-233 None 반환 명시 | PASS | task-board L170 — "**unknown market 일 때 `None` 반환 — raise 금지**, pipeline.py L67 의 `.get()` graceful fallback 의도 보존. 기존 `_resolve_calendar_name` (L31-34) 은 ValueError raise — 동작이 다르므로 그것의 단순 public 승격 금지. 새 함수는 별도 정의" 강조 표시 + raise 금지 사유 + 단위 테스트 "unknown market 입력 시 None 반환" 명시. 회귀 시나리오까지 적시. |
| 3. TASK-234 경로 정정 | PASS | task-board L171 — "**`backend/app/data/asset_repository.py`** (실측 위치 — `repositories/` 하위 아님, `app/data/` 직속)" 강조 + `backtest_repository.py` 는 `repositories/` 하위로 명확히 구분. 실측: `ls` 결과 `app/data/asset_repository.py` (5121 bytes) + `app/data/repositories/backtest_repository.py` (8453 bytes) 둘 다 존재. |
| 4. TASK-238 listAssets/as 캐스트 정정 | PASS | task-board L180 — (a) "`UniverseSelector.tsx:27-29` 의 트릭은 `Awaited<ReturnType<typeof api.listAssets>>["items"][number]` — `listAssets` 트릭 (다른 API)" 강조. 실측 일치 (UniverseSelector.tsx:27-29 가 `UniverseAsset = Awaited<ReturnType<typeof api.listAssets>>["items"][number]` export). (b) "`StrategyParamsForm.tsx` 에 `as` 캐스트 0건 ... 실제 캐스트는 `frontend/app/backtests/new/page.tsx:96`" 강조 + 정확한 캐스트 텍스트 인용. 실측 일치 (sed L94-98 확인 — `(descriptor.params_schema?.properties ?? {}) as Record<string, { type?: string }>`). 수정 ④ 에 `Asset` 타입 export + `UniverseSelector.tsx:27-29` 가 `Asset` import 항목 추가됨. |
| 5. TASK-237 ↔ 238 순차 (Depends On) | PASS | task-board L179 — TASK-237 `Depends On` 컬럼이 `TASK-238` 로 갱신 + description 본문 "**선행 의존**: TASK-238 (BacktestResult 타입이 `lib/api/types.ts` 로 이동된 후 import). 두 태스크가 같은 page.tsx 의 import 블록을 만져 git merge conflict 위험 있어 순차 진행" 명시. |

## 의존성 그래프 일관성

L187-208 의 새 의존성 그래프는 다음과 같이 정합:

- **Phase 1 (동시 7개)**: TASK-230, 231, 232, 233, 234, 236, 238 — 의존성 컬럼 모두 빈값 또는 사전 task 없음. 파일 영역 비겹침 (sources/, allocators/, services/, data/pipeline.py, api/assets.py + api/backtests.py + 2 repositories, registration.py, frontend schemas/types). **검증: 정합**.
- **Phase 2 (동시 2개)**: TASK-235 (`Depends On`: TASK-230, TASK-234) + TASK-237 (`Depends On`: TASK-238). TASK-235 는 backend (api/assets.py + cron_jobs.py), TASK-237 는 frontend (page.tsx + components/backtest/) — 영역 분리 → 병렬 안전. **검증: 정합**.
- **Phase 3 (단독)**: TASK-239 (`Depends On`: TASK-237). 동일 page.tsx 를 분해하므로 단독 진행 합리. **검증: 정합**.
- **Phase 4 (순차)**: TASK-240/241/242/243 모두 `Depends On`: TASK-239. page.tsx 와 다수 컴포넌트 변경 — 순차 권장 합리. **검증: 정합**.

이전 라운드 PASS 였던 태스크 (TASK-230, 232, 236) 의 인용·라인번호는 정정 과정에서 변경 없음. 회귀 없음.

## 추가 spot-check 결과

| 항목 | 실측 결과 | 일치 여부 |
|------|---------|---------|
| `backend/app/data/asset_repository.py` 존재 | 5121 bytes | PASS |
| `backend/app/data/repositories/backtest_repository.py` 존재 | 8453 bytes | PASS |
| `new/page.tsx:96` 의 `as Record<string, { type?: string }>` | L96 `(descriptor.params_schema?.properties ?? {}) as Record<` | PASS |
| `UniverseSelector.tsx:27-29` `listAssets` 트릭 | L27-29 `UniverseAsset = Awaited<ReturnType<typeof api.listAssets>>["items"][number]` | PASS |
| `all_weather.py:60-79` 3단계 + `_validate_categories` | L62-72 = 3단계 (non-negative / total>0 / abs(total-1.0)≤0.05) + L74-79 `_validate_categories` (asset_categories empty 검사 별도) | PASS |

## 종합 판정

**PASS**

5건 지적 사항이 모두 task-board.md description 본문 + Depends On 컬럼 + 의존성 그래프 절에 일관되게 반영되었다. 추가 spot-check 4건도 모두 실측과 일치. Phase 1 7개 태스크 (TASK-230/231/232/233/234/236/238) 동시 Coder 호출에 진입할 수 있다.
