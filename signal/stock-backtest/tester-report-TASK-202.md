---
agent: tester
task_id: TASK-202
status: DONE
severity: observation
timestamp: 2026-04-29T20:25:00
---

## 결과 요약

비개발자 첫 사용 시나리오를 e2e 페르소나 harness 로 자동화 + 2026-04-29 사고
(weights 에 ticker symbol 직접 입력 → 422) 를 회귀 테스트로 영구 박제했다.
헤드리스 브라우저 없이 HTTP + HTML grep + JSON API 로 검증하므로 systemd 영속화된
quant-lab-{backend(8001),frontend(3001)} 위에서 1.16~2.73s 안에 9개 케이스 전부 통과.

향후 동일 사고 (frontend 가 raw 입력을 backend 로 흘리거나 backend 의 symbol→id
fallback 이 깨지거나 catalog 시드가 빠지는 경우) 가 재발하면 즉시 실패 → 사용자
보고 전 발견된다.

## 검증 대상

- `backend/app/api/health.py` GET /api/health
- `backend/app/api/assets.py` GET /api/assets (q, market, limit)
- `backend/app/api/strategies.py` GET /api/strategies (allocator 3 + filter 2 + JSON Schema)
- `backend/app/api/backtests.py` POST /api/backtests + GET /api/backtests/{run_id}
- `backend/app/services/backtest_runner.py` `_resolve_symbol_keys_to_asset_ids` (TASK-201)
- `frontend/app/assets/page.tsx` 한국어 키워드
- `frontend/app/backtests/new/page.tsx` AssetWeightMap + FilterConfigBuilder (TASK-200)

## 변경된 파일

- `projects/stock-backtest/backend/tests/e2e/__init__.py` (신규)
- `projects/stock-backtest/backend/tests/e2e/conftest.py` (신규)
- `projects/stock-backtest/backend/tests/e2e/test_persona_first_use.py` (신규, 6 테스트)
- `projects/stock-backtest/backend/tests/e2e/test_failure_replay.py` (신규, 3 테스트)

frontend / signal / backend/app / 기존 테스트 디렉토리(api,golden,regression)
및 `backend/tests/conftest.py` 는 일절 수정하지 않음 (병렬 안전성 준수).

## 테스트 결과

실행 명령 (backend venv: `/home/jai/pa/stock-backtest/projects/stock-backtest/.venv/bin/python`):

```bash
cd projects/stock-backtest/backend
.venv/bin/python -m pytest tests/e2e/ -v
```

결과: **9 passed, 0 failed, 0 skipped — 1.16s** (2회차 캐시 적용)

| # | 테스트 | 검증 내용 |
|---|--------|-----------|
| 1 | `test_step1_assets_page_renders` | /assets 한국어 키워드 (자산 카탈로그 / 심볼 또는 한글명 검색 / 자산 추가) |
| 2 | `test_step2_assets_api_lists_seed_catalog` | 시드 4종: SPY / 069500 (KODEX 200) / BTC-USD / ETH-USD |
| 3 | `test_step3_strategies_api_exposes_allocator3_filter2` | allocator={fixed_weight, all_weather, equal_weight}, filter={moving_average, momentum} + JSON Schema |
| 4 | `test_step4_backtest_create_with_asset_id_keys` | POST /api/backtests with str(asset_id) 키 → 200/201 + run_id |
| 5 | `test_step5_backtest_status_pollable` | terminal status (done/failed/cancelled) 도달 (~15s 폴링) |
| 6 | `test_step6_frontend_backtests_new_renders_widgets` | /backtests/new 한국어 키워드 6종 (새 백테스트 / 전략 선택 / 자산 선택 / 기축통화 / 필터 추가 / 필터 없음) |
| 7 | `test_replay_symbol_keys_in_weights_now_resolved` | weights {"SPY":0.6,"BTC-USD":0.4} → backend fallback 매핑 → 200/201 |
| 8 | `test_replay_unknown_symbol_returns_friendly_error` | weights {"NONEXISTENT_TICKER_ZZZ":1.0} → status=failed + 한국어 메시지 (또는 즉시 422+친절 detail) |
| 9 | `test_replay_no_json_textarea_in_frontend_build` | `.next/static` grep `JSON.parse.*params \| <textarea.*JSON \| textarea.*weights` → match 0 (또는 dev 모드 SKIP) |

### 회귀 영향 검증

기존 테스트도 함께 돌렸음:

```bash
.venv/bin/python -m pytest tests/regression/ tests/golden/ tests/api/
```

결과: `5 failed, 72 passed, 6 skipped` — 그러나 TASK-200/201 적용 전 baseline 도
`6 failed, 11 passed, 4 skipped` 로 `tests/api/test_api_contract.py` 의 동일 패턴
fail (`GET /api/assets/{asset_id}`, `GET /api/assets/{asset_id}/ohlcv`,
`GET /api/backtests/{run_id}`, `DELETE /api/backtests/{run_id}`,
`GET /api/backtests/{run_id}/result`) 가 이미 존재. **TASK-200/201 으로 인한 신규
회귀 0** (오히려 `POST /api/assets` fail 1건이 PASS 로 전환되어 개선).

baseline fail 5건은 TASK-202 와 무관한 기존 schemathesis 계약 결함이므로 별도 분석
태스크 후보 (severity=observation, TASK-202 본 작업과 분리).

## 회귀 박제 항목 (영구)

이 e2e 가 잡아내는 사고/회귀:

1. **TASK-200 우회 회귀**: 누가 `<textarea>` 로 JSON 입력을 다시 끼워넣으면 #9 가
   빌드물 grep 으로 즉시 탐지 (UI/UX 원칙 1 강제).
2. **TASK-201 fallback 깨짐**: `_resolve_symbol_keys_to_asset_ids` 가 사라지거나
   동작이 변하면 #7 이 422 로 떨어짐.
3. **시드 카탈로그 누락**: SPY / 069500 / BTC-USD / ETH-USD 중 1건이라도 빠지면 #2
   가 fail. (UI/UX 원칙 2 의 비개발자 즉시-사용 보장.)
4. **MVP 프리셋 5종 set drift**: allocator 3 + filter 2 외 추가/삭제가 발생하면 #3
   set 비교에서 fail (Quant Lab CLAUDE.md L26 절대 원칙).
5. **/api/strategies JSON Schema 누락**: frontend 가 폼 자동 생성에 의존하므로
   `params_schema` 가 빠지면 #3 에서 fail.
6. **터미널 status 미도달**: worker 가 영원히 pending 으로 남는 회귀를 #5 가 30회
   폴링으로 탐지.
7. **한국어 키워드 누락**: frontend i18n 키 변경/누락 시 #1, #6 이 즉시 fail
   (UI/UX 원칙 2).

## 이슈/블로커

- **블로커 없음.**
- **observation 1 (TASK-202 외부)**: `tests/api/test_api_contract.py` 의
  schemathesis 계약 fuzz fail 5건이 baseline 부터 존재. e2e 와 무관하므로 본 태스크는
  PASS 처리하되, 별도 태스크로 분리 권고 (아래 "다음 제안" 참조).
- **observation 2**: `test_replay_no_json_textarea_in_frontend_build` 는
  `.next/static` 빌드 디렉토리 부재 시 SOFT skip. systemd 가 `next dev` 로 운영
  중이라 현재 빌드물이 있어 PASS — 향후 `next build` 산출물로 운영 전환되어도 동작.
- **observation 3**: `test_replay_unknown_symbol_returns_friendly_error` 는
  현재 backend 가 POST 200 (pending) → worker 단계에서 처리하는 경로를 따름.
  미존재 ticker 가 fallback 에서 어떻게 식별되어 friendly error 로 전달되는지는
  실제 사용자 트리거 시 추가 확인 권장 (코드 결함은 발견되지 않음).

## 다음 제안

1. **schemathesis 계약 fuzz fail 5건 별도 태스크화** (TASK-203/204 슬롯 후보):
   - `tests/api/test_api_contract.py` baseline 5 fail 의 root cause 분석
   - severity 를 본 작업과 구분해서 등록 (코드 결함 가능성)
2. **CI 진입 시 e2e 분리 마커 권장**: `pytest -m e2e` 로 분리하면 systemd 영속화가
   없는 CI 노드에서 자동 skip 가능. 현재는 fixture SOFT skip 으로 충분.
3. **사용자 첫 사용 시나리오 확장**: 백테스트 결과 차트 렌더링 (/backtests/{id}/result
   페이지) 까지 페르소나 흐름 확장 시, step7~ 로 추가 가능. 현재 step1~6 으로 "백테스트
   1회 등록 + 폴링" 까지가 MVP.
4. **Failure replay 카탈로그 패턴화**: 향후 비개발자 사고가 재발할 때마다
   `test_failure_replay.py` 에 케이스를 누적 추가하는 운영 룰 권장. 매 사고당 회귀 1건
   영구 박제 → 같은 사고 재발 0 보장.
