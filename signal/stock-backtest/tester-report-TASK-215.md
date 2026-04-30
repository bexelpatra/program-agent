---
agent: tester
task_id: TASK-215
status: DONE
timestamp: 2026-04-30T12:00:00
severity: observation
---

## 결과 요약

골든 baseline 9 케이스 통합 재생성 검토 결과, **신규 baseline 갱신은 불필요**. 다만 작업트리 (uncommitted) 상태에 이미 scenario_3 (BTC 포함) 3 케이스의 갱신된 baseline 이 적재되어 있고, 이 갱신은 **3 선행 태스크 (TASK-211/212/214) 가 아닌 별개의 V3 Q8 fractional 매매 리팩터링** 의 회귀로 확인됨. 9 케이스 모두 현재 코드 상태에서 통과 (`pytest tests/golden/ -v` → 12 passed).

세 선행 태스크의 영향만 보면 골든 baseline 갱신이 필요 없음:
- **TASK-211 (engine 청산 누락)**: 기존 9 케이스는 모두 `signal_filters=tuple()` (빈 필터) 이라 빈 target_weights 발생 path 미진입 → 청산 패턴 무영향. (Coder 보고와 일치)
- **TASK-212 (TradeFill.settlement_date)**: 골든 스냅샷 비교 키는 `final_equity / cagr / mdd / sharpe / win_rate / num_fills / num_equity_points / aborted` 만 — trade time 필드는 비교 안 함. (Coder 보고와 일치)
- **TASK-214 (yfinance auto_adjust=True)**: 골든 fixture 가 **완전 정적** (deterministic 합성 시계열) — yfinance/DB 무관. (아래 §"Fixture 출처 조사" 참조)

## Fixture 출처 조사 (Manager 의사결정 1)

Path: `backend/tests/golden/test_golden_scenarios.py:69-100`

```python
def _make_trending_series(dates, start_price, annual_growth, daily_vol=0.0):
    """우상향 (또는 평탄) 결정적 시계열. vol=0 이면 완전 결정적, 아니면 sin 기반 noise."""
    daily_growth = (1.0 + annual_growth) ** (1.0 / 252.0)
    prices = []
    for i, _d in enumerate(dates):
        noise = math.sin(i * 0.1) * daily_vol if daily_vol > 0 else 0.0
        prices.append(start_price * (daily_growth**i) * (1.0 + noise))
    return prices
```

→ 가격 시계열은 yfinance/pykrx/DB **호출 없이** 순수 수학 함수로 합성됨. `random` 사용 없음 (sin 기반 결정적 noise). FX 도 `_build_fx_rates` 가 `(start_rate, end_rate)` 선형 보간으로 합성.

`backend/tests/conftest.py` 도 확인 — `DATABASE_URL` fallback 만 주입할 뿐 fixture 가격 데이터를 DB 에서 읽지 않음 (golden 테스트는 도메인 직접 호출이라 DB 의존 없음).

→ **TASK-214 (yfinance auto_adjust=True) 영향 0**. 결론: 케이스 A (baseline 갱신 불필요).

## Manager 의사결정 2: 작업트리 baseline 변경 분석

`git status --short tests/golden/` 결과:
```
 M tests/golden/snapshots/scenario_3_us_crypto__all_weather.json
 M tests/golden/snapshots/scenario_3_us_crypto__equal_weight.json
 M tests/golden/snapshots/scenario_3_us_crypto__fixed_weight.json
```

3 파일만 수정됨 (committed: pre-211/212/214). `git diff` line-by-line:

| 키 | 이전 (committed) | 현재 (working) | 변동 |
|----|------------------|-----------------|------|
| scenario_3_us_crypto__fixed_weight.cagr | 0.057082 | 0.211192 | ↑ ~3.7배 |
| scenario_3_us_crypto__fixed_weight.final_equity | 13185.84 | 25971.69 | ↑ ~2배 |
| scenario_3_us_crypto__fixed_weight.num_fills | **4** | **79** | ↑ ~20배 |
| scenario_3_us_crypto__fixed_weight.mdd | 0.0 | -0.000212 | 0 → 음수 (실제 drawdown 발생) |
| scenario_3_us_crypto__fixed_weight.win_rate | 1.0 | 0.897375 | 1.0 → 정상 분포 |
| scenario_3_us_crypto__fixed_weight.sharpe | 962.03 | 21.18 | ↓ (variance 정상화) |

(equal_weight, all_weather 도 동형 패턴 — num_fills 4→80/79, mdd 0→음수, win_rate 1.0→0.82~0.89)

scenario_1 (KR only) / scenario_2 (KR+US) 는 **변경 없음** — `daily_vol=0.0` (완전 결정적 평탄 우상향) 이라 monthly 리밸런싱에 비중 drift 가 거의 없음 → fills 적음, mdd=0, win_rate=1.0 패턴 유지.

scenario_3 만 변경된 이유: BTC (asset_id=4) 의 `daily_vol=0.02` 로 가격 변동성이 있어 비중 drift 가 존재. 그러나 **이전 코드** 는 BTC 가 1주 단위 정수 매매 강제라 $10,000 자본으로 BTC ($8,000 시작) 1개만 살 수 있었고, 1코인 후 추가 매수 불가능 → 리밸런싱이 사실상 동결 (4 fills 만 발생). **현재 코드** 는 V3 Q8 (2026-04-29 결정) 의 코인 한정 fractional 매매로 BTC 를 8자리 소수점까지 매수 가능 → 매월 비중 drift 보정으로 79~80 fills 발생.

### 변경 사유 = TASK-211/212/214 가 아니다

`git diff app/domain/{portfolio,trade,asset/entity}.py` 검토 결과, 작업트리에는 다음 **별개 리팩터링**이 함께 stage 되어 있음:
- `Portfolio.Position.qty: int → Decimal` (8자리 소수점)
- `TradeOrder.qty_target: int → Decimal`
- `TradeFill.qty_filled: int → Decimal` + `settlement_date: date` (TASK-212 의 일부)
- 신규 `app/domain/asset/entity.py`: `FRACTIONAL_MARKETS = frozenset({"CRYPTO"})`, `is_fractional_market(market)` 헬퍼
- `Portfolio.buy/sell` 시그니처에 `fractional: bool = False` 인자 추가
- 신규 alembic migration `0004_fractional_qty.py`

이는 architecture.md L609-615 의 **V3 Q8 재결정 (2026-04-29)** "코인 한정 fractional" 정책의 구현임. CLAUDE.md 의 3 선행 태스크 명세에는 명시되지 않은 영역이다.

→ scenario_3 baseline 변경은 **Q8 fractional 리팩터링의 의도된 회귀** (BTC 백테스트가 평탄선이 되던 run_id=56 사고 해소). TASK-211/212/214 가 아닌, **별개 (이미 작업트리에 진행 중인) Q8 작업의 산출물**.

## 테스트 결과

`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/pytest tests/golden/ -v`

- **12 passed** (9 골든 케이스 + 3 invariant: cancel_check / progress_callback / empty_period ValueError)
  - test_golden_snapshot[fixed_weight-scenario_1_kr_only] PASSED
  - test_golden_snapshot[fixed_weight-scenario_2_kr_us] PASSED
  - test_golden_snapshot[fixed_weight-scenario_3_us_crypto] PASSED
  - test_golden_snapshot[all_weather-scenario_1_kr_only] PASSED
  - test_golden_snapshot[all_weather-scenario_2_kr_us] PASSED
  - test_golden_snapshot[all_weather-scenario_3_us_crypto] PASSED
  - test_golden_snapshot[equal_weight-scenario_1_kr_only] PASSED
  - test_golden_snapshot[equal_weight-scenario_2_kr_us] PASSED
  - test_golden_snapshot[equal_weight-scenario_3_us_crypto] PASSED
  - test_engine_aborts_when_cancel_check_returns_true PASSED
  - test_engine_progress_callback_called PASSED
  - test_engine_raises_on_empty_period PASSED

확장 회귀 (`pytest tests/golden/ tests/regression/ tests/domain/ -v`):
- **72 passed, 0 failed** (1 pykrx DeprecationWarning, 무관)

### 사후 검증: 위 9 케이스 갱신 후 파일 정합

- 1 = 9/9 케이스 baseline 과 현재 코드 일치 (rel_tol=1e-4 통과).
- scenario_1 / scenario_2 baseline 6 파일은 **committed 상태 그대로** — 회귀 0 확인.
- scenario_3 baseline 3 파일은 **working copy 상태** (Q8 fractional 적용 후). 이는 어느 시점에 누군가 (아마 Q8 구현 중 Coder 가) `GOLDEN_UPDATE=1` 로 미리 재생성해둔 것으로 보임. 현재 코드와 정확히 일치하므로 deterministic 재현 가능.

## 변경된 파일

없음 (Tester 가 코드/baseline 직접 수정 안 함). 의사결정 보고만.

## 이슈/블로커

없음. severity: **observation** (코드 결함 아님 — 의도된 회귀, 모든 테스트 통과).

작업트리에 committed 안 된 scenario_3 baseline 변경 3 파일은 합당한 회귀로 판단됨:
- 변경 양상이 Q8 fractional 도입의 직접 결과와 정확히 일치 (BTC fractional 매매로 monthly 리밸런싱 활성화 → fills 증가, drawdown 정상화, win_rate 정상 분포).
- scenario_1 / scenario_2 가 무영향 (vol=0 자산만 포함) → 일관된 인과관계.

## 추가 관찰 (Coder 영역 권장 사항, severity 미해당)

1. **Q8 fractional 리팩터링이 별도 태스크로 명시 분리되지 않음**: TASK-211/212/214 는 명시 태스크지만, 작업트리의 portfolio/trade/asset 의 Decimal 통일·fractional 분기·migration 0004 추가는 어느 태스크의 산출물인지 task-board.md 에서 추적 어려움. Manager 가 별도 TASK 번호 (예: TASK-217 V3 Q8 fractional 매매) 로 회고 단계에서 박제 권장.

2. **commit message 제안 (Manager 가 baseline 변경 commit 시)**:
   ```
   TASK-215 (verify) + V3 Q8 fractional 회귀: scenario_3 baseline 갱신
     - scenario_3 (BTC 포함) num_fills 4 → 79~80, cagr 0.057 → 0.21
     - 사유: V3 Q8 fractional 매매 도입 (CRYPTO Decimal 8자리)
       run_id=56 BTC 평탄선 사고 해소, monthly 리밸런싱 활성화
     - scenario_1 / scenario_2 무영향 (vol=0 결정적 자산만 포함)
     - TASK-211/212/214 자체는 baseline 변경 0 (Tester 검증 완료)
   ```

3. **golden 스냅샷의 trade time 검증 부재 (TASK-212 후속)**: 현재 스냅샷은 `num_fills` 만 비교하고 trade time/settlement_date 정합성은 검증 안 됨. settlement_date 필드 추가의 회귀 보호력이 e2e/test_failure_replay 에 제한. tests/regression/ 에 "fills 의 settlement_date 가 모두 base 캘린더 거래일이며 D+1 형태인지" 검증 추가 권장 (Coder 의 다음 제안과 일치).

## 다음 제안

1. **Manager**: scenario_3 baseline 3 파일을 commit 으로 박제. 위 commit message 제안 사용.
2. **Manager**: V3 Q8 fractional 작업을 task-board.md 에 사후 박제 (TASK-217 V3 Q8 fractional 매매 [DONE] 형식 — 회고 단계에서 일괄).
3. **Manager (TASK-216 후속)**: 사용자에게 BTC ohlcv 재백필 안내 시 scenario_3 baseline 변경도 함께 통지 (사용자가 같은 universe 로 백테스트 재실행 시 결과가 달라질 수 있음).
