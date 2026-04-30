---
agent: coder
task_id: TASK-219
status: DONE
timestamp: 2026-04-30T17:25:00
---

## 결과 요약

MA 시그널 allocator (`ma_signal`) 를 신규 구현했다. signal_filters 와 분리된
allocator 단위 시그널로, 자산별 가격이 MA(window) 위면 입력 비중 적용, 아래면 0
(cash 처리). 자산 단위 fallback (window 부족 자산은 skip) 로 멀티 자산 universe
에서 데이터 길이 차이를 안전하게 흡수한다.

backend 등록 매핑 2 곳 (+ 1 패키지 init) 모두 갱신:
- `app/services/backtest_runner.py:53-58` `_ALLOCATORS` dict
- `app/api/strategies.py:14-23 import + L60-67 list_strategies allocators 리스트`
- `app/domain/allocators/__init__.py` re-export + `__all__`

frontend 변경 0 — `lib/api/schemas.ts:182` allocator_name 이 free string 이고
StrategyParamsForm 의 complexFieldRenderer (`page.tsx:91-102`) 가 dict 타입을
AssetWeightMap 으로 자동 매핑하므로 ma_signal `assets: dict[int, float]` 도
자동 동작 (수동 검증은 Manager 가 브라우저로).

## 변경된 파일

신규:
- `projects/stock-backtest/backend/app/domain/allocators/ma_signal.py` (123 lines)
  - `MaSignalParams(BaseModel)` { window: int (default 120, ge=2, le=500), assets: dict[int, float] }
  - `class MaSignal(AllocatorBase[MaSignalParams])` { name="ma_signal", required_universe → params.assets keys }
  - generate_weights: 자산 단위 fallback (universe ∩ assets → window 부족 skip → MA 위면 비중 / 아래면 0 → normalize_weights(allow_cash_slot=True))
- `projects/stock-backtest/backend/tests/domain/test_ma_signal_allocator.py` (149 lines, 8 케이스)
  - 4 generate_weights 케이스 (a~d, task-board ④ 명세) + 4 Params 검증 회귀

수정:
- `projects/stock-backtest/backend/app/domain/allocators/__init__.py` — `from .ma_signal import MaSignal, MaSignalParams` + `__all__ += ["MaSignal", "MaSignalParams"]`
- `projects/stock-backtest/backend/app/services/backtest_runner.py:29-38, 53-58` — import 추가 + `_ALLOCATORS["ma_signal"] = (MaSignal, MaSignalParams)`
- `projects/stock-backtest/backend/app/api/strategies.py:14-23, 60-67` — import 추가 + StrategyDescriptor (한국어 설명: "이동평균 시그널 — 자산별 가격이 MA 위면 매수, 아래면 청산 (cash 처리)")
- `signal/stock-backtest/architecture.md:670` — allocators 행을 4종 + TASK-219 로 갱신 (task-board ⑥ 지시)

## 추가/변경된 public API 시그니처

- `app.domain.allocators.MaSignal(params: MaSignalParams)` — `name="ma_signal"` ClassVar
- `app.domain.allocators.MaSignal.required_universe() -> list[int]` (params.assets 키 반환)
- `app.domain.allocators.MaSignal.generate_weights(universe_asset_ids, prices_until_d, signal_date) -> dict[int, Decimal]`
- `app.services.backtest_runner._ALLOCATORS` 항목 +1 ("ma_signal")
- `GET /api/strategies` 응답 `allocators` 리스트 +1 (4 항목)

## DoD 검증 결과

| DoD | 명세 | 결과 | 증거 |
|-----|------|------|------|
| (a) | 단위 테스트 4 케이스 통과 (BTC/ETH 실측) | **PASS 8/8** (4 generate_weights + 4 Params 검증) | `pytest tests/domain/test_ma_signal_allocator.py -v` → `8 passed` |
| (b) | e2e BTC 100% + ma_signal w=120 + quarterly + 2017-2026 → 분기마다 BUY/SELL | **수동 검증으로 위임** (Reviewer 체크리스트 4 권고) — 아래 "수동 검증 명세" 참조 | manual |
| (c) | 기존 9 골든 회귀 0 | **PASS 12/12** (9 골든 + 3 보조) | `pytest tests/golden/test_golden_scenarios.py -v` → `12 passed` |
| (d) | GET /api/strategies 응답에 ma_signal 등장 | **PASS** — allocators=['fixed_weight','all_weather','equal_weight','ma_signal'] (4개) | TestClient 응답 `name=ma_signal, type=allocator, params_schema={window, assets}` 확인 |

## 수동 검증 명세 (DoD-b 위임)

Manager 또는 사용자가 다음을 직접 실행:

```bash
# 1. backend 기동 (이미 docker-compose up 가정)
# 2. 브라우저 /backtests/new
# 3. 전략 = ma_signal, window=120, assets={"BTC-USD": 1.0}
#    universe = [BTC-USD], rebalance_schedule=quarterly,
#    period=2017-01-01~2026-04-29, base_currency=USD, initial_cash={USD: 100000}
# 4. 실행 → 진행률 100% → 결과 확인
# 기대:
#   - trades 가 분기별 BUY/SELL 발생 (run_id=96 의 1건만 ≠)
#   - MA 깨진 분기는 청산, 회복 분기는 재매수
#   - equity 곡선이 cash-only 구간 + 보유 구간 교차
```

수동 검증 결과를 manager 가 done-log 에 기록.

## 이슈/블로커

### `tests/api/test_api_contract.py::test_strategies_endpoint_returns_mvp_presets` 회귀

- **현상**: 기존 `assert len(body["allocators"]) == 3` 하드코딩이 ma_signal 추가로 4 가 되어 `4 == 3` 단언 실패.
- **분류**: **의도된 회귀** (task-board ③ 가 list_strategies 응답에 ma_signal 추가를 명시했고 GET /api/strategies 응답이 4 항목으로 늘어난 것이 본 태스크의 핵심 산출).
- **조치 필요**: Tester 가 `tests/api/test_api_contract.py:83` 의 `== 3` 을 `== 4` (또는 `>= 3` + name 포함 검증) 로 갱신해야 함.
- **본 태스크에서 수정 안 한 이유**: coder.md L188 "tests/ 디렉토리 파일 수정 금지 (Tester 전용)". task-board 가 신규 단위 테스트 파일 작성은 명시했지만 기존 baseline 갱신은 명시 안 했음.

### 사전에 존재하던 fuzz 실패 (본 태스크와 무관)

`test_api_contract_fuzz[*]` 6 건 실패. ma_signal 추가 전에도 동일 실패 (fuzz 비결정성/DB 연결 의존). 본 태스크 영향 0 — 별건으로 분리 처리 권고.

## 다음 제안

1. **Tester 후속 태스크 등록**: `tests/api/test_api_contract.py::test_strategies_endpoint_returns_mvp_presets` 의 `len == 3` 을 `len == 4` (allocator 카운트) + `len == 2` (filter 카운트) 로 갱신 + name 포함 단언 추가 (`{"fixed_weight","all_weather","equal_weight","ma_signal"} ⊆ names`). hard-coded count 회귀를 막으려면 set-based 단언이 더 안전.

2. **frontend 수동 검증 체크리스트** (본 태스크 DoD-d 보강): Manager 가 브라우저에서 `/backtests/new` → 전략 드롭다운 → "ma_signal" 표시 + 선택 시 AssetWeightMap (assets dict) + window 숫자 입력 자동 렌더 확인. 불일치 시 별도 frontend 수정 태스크 분리.

3. **Phase 2 검토 후보**: ma_signal 사용 빈도가 누적되어 영구 프리셋 격이 되면 architecture.md L499 "Allocator 3종" 표기를 4종으로 격상. Reviewer 가 "L499 는 V3 *원칙* 선언, L670 는 *구현 파일 목록*" 으로 분리 결정한 정책의 재평가 시점.

4. **(관찰)** AllocatorBase 패턴이 4 번째 구현체에서도 매끄럽게 적용됨 — 추후 Momentum allocator, Volatility allocator 등 추가 시도 동일 패턴 반복 가능 (FixedWeight 의 weights 검증 로직이 MaSignalParams.assets 에서도 거의 그대로 쓰임 — 2회 중복. 3회째에 utils 추출 검토).
