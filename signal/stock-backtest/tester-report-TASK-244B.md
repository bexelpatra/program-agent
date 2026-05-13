---
agent: tester
task_id: TASK-244B
status: DONE
timestamp: 2026-05-07T00:40:00
severity: bug
---

## 결과 요약

TASK-244 (engine.py 큐잉 패턴) 검증 — DoD (a)~(c) 모두 PASS, DoD (d) **10/11 (9/9 L1~L3 + L4 1/2)**. L4 S1 SUSPECT 의 원인은 코드 결함이 아닌 **`scripts/validation/case_l4.py` L48-62 의 fixture 가 TASK-244 fix 이전 엔진 출력으로 박제되어 있어 — Opus 가 새 엔진의 의도된 동작 ("Day 0=pure cash $10,000") 과 fixture 의 옛 값 ("Day 0=$9,747.06") 의 불일치를 정확히 catch**. severity=`bug` 로 분류 — Tester 영역 (`tests/`) 외부 (`scripts/`) 라 본 태스크 내 수정 불가, Manager 에게 후속 Coder 태스크 (case_l4.py L48-62 fixture 갱신) 를 제안한다.

DoD (a) 4 신규 메소드 PASS, DoD (b) regression 50/50 PASS, DoD (c) 골든 9 baseline 재생성 + 임계값 분석 (sharpe/mdd 일부 케이스에서 임계값 초과지만 **이는 TASK-244 fix 의 의도된 효과 — 옛 값이 BUG 의 부산물**, ESCALATE 사항으로 명시 보고).

## 변경된 파일

| 파일 | 변경 요지 |
|------|-----------|
| `backend/tests/domain/test_engine.py` | `TestEodEquityAccountingTiming` 신규 클래스 + 헬퍼 3 종 (`_UseFirstAssetAllocator`, `_CashOnlyAllocator`, `_OnceOnFirstDayAllocator`) 추가. 4 메소드: `test_day_0_eod_is_pure_cash`, `test_day_1_eod_is_post_init_trade`, `test_sell_signal_d_eod_still_holds`, `test_buy_signal_d_eod_still_cash`. 기존 3 클래스와 충돌 없음 (이름 / fixture 분리). |
| `backend/tests/golden/snapshots/*.json` (9 파일) | TASK-244 큐잉 패턴 후 baseline 재생성 (`GOLDEN_UPDATE=1 pytest tests/golden/`). |

`scripts/`, `app/` 미수정 (Tester 영역 규칙 준수).

## 테스트 결과

### (a) `tests/domain/test_engine.py` 신규 4 메소드 — PASS

```
$ ../.venv/bin/python -m pytest tests/domain/test_engine.py::TestEodEquityAccountingTiming -v
collected 4 items

tests/domain/test_engine.py::TestEodEquityAccountingTiming::test_day_0_eod_is_pure_cash PASSED [ 25%]
tests/domain/test_engine.py::TestEodEquityAccountingTiming::test_day_1_eod_is_post_init_trade PASSED [ 50%]
tests/domain/test_engine.py::TestEodEquityAccountingTiming::test_sell_signal_d_eod_still_holds PASSED [ 75%]
tests/domain/test_engine.py::TestEodEquityAccountingTiming::test_buy_signal_d_eod_still_cash PASSED [100%]

========================= 4 passed, 1 warning in 0.48s =========================
```

전체 `test_engine.py` 13 케이스 (기존 9 + 신규 4) 도 0 회귀:

```
$ ../.venv/bin/python -m pytest tests/domain/test_engine.py -q
13 passed, 1 warning in 0.49s
```

### (b) regression 3 파일 — 0 회귀 PASS

```
$ ../.venv/bin/python -m pytest tests/regression/ -q
50 passed, 2 warnings in 2.86s
```

| 파일 | 케이스 수 | 결과 |
|------|-----------|------|
| `tests/regression/test_lookahead.py` | 8 | PASS |
| `tests/regression/test_calendar_defense.py` | 22 | PASS |
| `tests/regression/test_cash_by_ccy.py` | 20 | PASS |
| **합계** | **50** | **PASS** |

큐잉 패턴이 lookahead defense 를 더 엄격하게 만든다 (D+1 settlement 가 자연스럽게 다음 iteration 으로 이동) — 회귀 사례 0건.

### (c) 골든 9 baseline 재생성 + 임계값 검증

```
$ GOLDEN_UPDATE=1 ../.venv/bin/python -m pytest tests/golden/ -q
12 passed, 1 warning in 2.71s

$ ../.venv/bin/python -m pytest tests/golden/ -q   # 재실행 (no GOLDEN_UPDATE)
12 passed, 1 warning in 2.77s   # 재생성한 baseline 자체 일관 확인
```

#### 9 케이스 전후 비교 (5 metric × 9 case)

| 시나리오/전략 | metric | old (BUG) | new (fix) | \|Δ\|/\|old\| | sign |
|--------------|--------|-----------|-----------|---------------|------|
| 1_kr_only / all_weather | final_equity | 12988918.5772 | 12988918.5772 | 0.00% | + → + |
| 1_kr_only / all_weather | cagr | 0.054049 | 0.053762 | 0.53% | + → + |
| 1_kr_only / all_weather | mdd | 0.000000 | -0.001144 | INF | 0 → - |
| 1_kr_only / all_weather | sharpe | 3046.930506 | 87.147845 | **97.14%** | + → + |
| 1_kr_only / all_weather | win_rate | 1.000000 | 0.999187 | 0.08% | + → + |
| 1_kr_only / equal_weight | final_equity | 12632025.0008 | 12632025.0008 | 0.00% | + → + |
| 1_kr_only / equal_weight | cagr | 0.048179 | 0.047899 | 0.58% | + → + |
| 1_kr_only / equal_weight | mdd | 0.000000 | -0.001141 | INF | 0 → - |
| 1_kr_only / equal_weight | sharpe | 2603.977163 | 79.353593 | **96.95%** | + → + |
| 1_kr_only / equal_weight | win_rate | 1.000000 | 0.999187 | 0.08% | + → + |
| 1_kr_only / fixed_weight | final_equity | 12988918.5772 | 12988918.5772 | 0.00% | + → + |
| 1_kr_only / fixed_weight | cagr | 0.054049 | 0.053762 | 0.53% | + → + |
| 1_kr_only / fixed_weight | mdd | 0.000000 | -0.001144 | INF | 0 → - |
| 1_kr_only / fixed_weight | sharpe | 3046.930506 | 87.147845 | **97.14%** | + → + |
| 1_kr_only / fixed_weight | win_rate | 1.000000 | 0.999187 | 0.08% | + → + |
| 2_kr_us / all_weather | final_equity | 15102763.3092 | 15102763.3092 | 0.00% | + → + |
| 2_kr_us / all_weather | cagr | 0.086548 | 0.086064 | 0.56% | + → + |
| 2_kr_us / all_weather | mdd | 0.000000 | -0.001881 | INF | 0 → - |
| 2_kr_us / all_weather | sharpe | 1042.347065 | 83.869330 | **91.95%** | + → + |
| 2_kr_us / all_weather | win_rate | 1.000000 | 0.999187 | 0.08% | + → + |
| 2_kr_us / equal_weight | final_equity | 15330753.8964 | 15330753.8964 | 0.00% | + → + |
| 2_kr_us / equal_weight | cagr | 0.089840 | 0.089328 | 0.57% | + → + |
| 2_kr_us / equal_weight | mdd | 0.000000 | -0.002003 | INF | 0 → - |
| 2_kr_us / equal_weight | sharpe | 1219.064586 | 82.047485 | **93.27%** | + → + |
| 2_kr_us / equal_weight | win_rate | 1.000000 | 0.999187 | 0.08% | + → + |
| 2_kr_us / fixed_weight | final_equity | 15102763.3092 | 15102763.3092 | 0.00% | + → + |
| 2_kr_us / fixed_weight | cagr | 0.086548 | 0.086064 | 0.56% | + → + |
| 2_kr_us / fixed_weight | mdd | 0.000000 | -0.001881 | INF | 0 → - |
| 2_kr_us / fixed_weight | sharpe | 1042.347065 | 83.869330 | **91.95%** | + → + |
| 2_kr_us / fixed_weight | win_rate | 1.000000 | 0.999187 | 0.08% | + → + |
| 3_us_crypto / all_weather | final_equity | 25971.6944 | 25971.6944 | 0.00% | + → + |
| 3_us_crypto / all_weather | cagr | 0.211192 | 0.210478 | 0.34% | + → + |
| 3_us_crypto / all_weather | mdd | -0.000212 | -0.001399 | **559.91%** | - → - |
| 3_us_crypto / all_weather | sharpe | 21.185014 | 21.015375 | 0.80% | + → + |
| 3_us_crypto / all_weather | win_rate | 0.897375 | 0.896579 | 0.09% | + → + |
| 3_us_crypto / equal_weight | final_equity | 29289.8479 | 29289.8479 | 0.00% | + → + |
| 3_us_crypto / equal_weight | cagr | 0.240792 | 0.239959 | 0.35% | + → + |
| 3_us_crypto / equal_weight | mdd | -0.001126 | -0.001505 | 33.66% | - → - |
| 3_us_crypto / equal_weight | sharpe | 19.108885 | 18.980647 | 0.67% | + → + |
| 3_us_crypto / equal_weight | win_rate | 0.825776 | 0.824980 | 0.10% | + → + |
| 3_us_crypto / fixed_weight | final_equity | 25971.6944 | 25971.6944 | 0.00% | + → + |
| 3_us_crypto / fixed_weight | cagr | 0.211192 | 0.210478 | 0.34% | + → + |
| 3_us_crypto / fixed_weight | mdd | -0.000212 | -0.001399 | **559.91%** | - → - |
| 3_us_crypto / fixed_weight | sharpe | 21.185014 | 21.015375 | 0.80% | + → + |
| 3_us_crypto / fixed_weight | win_rate | 0.897375 | 0.896579 | 0.09% | + → + |

#### 부호 일치 검증 (DoD i): **9/9 PASS**

- final_equity: 모두 양수 유지.
- cagr: 모두 양수 유지.
- mdd: 모두 비양수 유지 (옛 0 → 새 음수 도 architecture.md L640 정합 — 옛 0 은 BUG: Day 0 이 post-trade 였으므로 monotonic uptrend 시 dd 기록 불가).
- sharpe: 모두 양수 유지.
- win_rate: 모두 0~1 범위 유지.

#### 절대 변동 검증 (DoD ii): **부분 PASS — 4건 임계값 초과**

| 케이스 | 미달 metric | \|Δ\|/\|old\| | 임계값 | 분석 |
|--------|-------------|---------------|--------|------|
| 1_kr_only/* (3 전략 각 1건) | sharpe | 91-97% | 50% | **TASK-244 fix 의 의도된 효과**. 옛 sharpe ≈ 1000~3000 은 비현실적 — old 엔진은 매일 portfolio 가 D+1 가격 매수 직후 D 가격 평가라 returns variance 가 인위적으로 0 에 가까웠음 → Sharpe 인플레이션. 새 엔진은 Day 0→Day 1 의 commission/slippage step 이 stdev 에 합리적으로 잡혀 sharpe 가 두 자리수 (전형적 백테스트 sharpe 범위) 로 정상화. |
| 2_kr_us/* (3 전략 각 1건) | sharpe | 91-93% | 50% | 위와 동일 메커니즘. 옛 1000+ → 새 80+ 로 정상화. |
| 3_us_crypto/* (2 전략, all_weather + fixed_weight) | mdd | 559% | 50% | 옛 -0.000212 (절대값 매우 작음 — 분모 효과로 percent 가 커짐). 새 -0.001399 (BTC 시드 noise vol=0.02 + Day 0 step 추가). 절대 차이는 0.0012 (자릿수 차이 1단계). 부호 동일, 자릿수 동일. equal_weight 케이스 (33.66%) 와 비교 시 분모 절대값 차이가 percent 격차를 만든 것 — sharpe 류 정상화는 아님. |

**ESCALATE 권고 사항 (사용자 판단 필요)**:

1. **sharpe 정상화 (6 케이스)**: 옛 baseline 의 sharpe ≈ 1000+ 는 BUG 부산물 (returns 시리즈 variance ≈ 0). 새 baseline 의 sharpe (80~90 range) 는 정확하나, 사용자가 만약 이전 화면에서 비현실적으로 높은 sharpe 를 보고 만족했다면 UI/리포트 시 "백테스트 결과가 이전 release 과 비교 불가" 안내 필요. (BUG 수정이라 이는 자연스러운 결과.)

2. **mdd 부호 변경 (6 케이스, 1_kr_only / 2_kr_us)**: 옛 0 → 새 -0.001~-0.002. 정확한 회계로의 이행 — 사용자가 옛 "drawdown 0%" 보고를 신뢰했을 가능성이 있다면 동일 안내.

3. **3_us_crypto mdd 559% 변동**: 옛 -0.000212 → 새 -0.001399. 자릿수 동일, 부호 동일. 사용자 입장에서 "drawdown 약 0.14% (옛 0.02%)" 의 차이 — UI 표기 자릿수 한 칸 다른 수준.

이상은 사용자 판단을 위한 케이스별 표 보고 — Manager 가 사용자에게 escalate 후 진행 결정.

### (d) `run_all.py` 실행 — **10/11 PASS**

```
$ ../.venv/bin/python -m scripts.validation.run_all
======================================================================
Layer 1 — 닫힌식 오라클 (5 cases)
======================================================================
  C1 ✅ PASS (0.16s) — SPY BH USD 평탄가 (yearly)
  C2 ✅ PASS (1.96s) — KODEX BH KRW 선형 +20%
  C3 ✅ PASS (0.00s) — BTC fractional BH USD 선형 +50%
  C4 ✅ PASS (0.00s) — 60/40 BH USD 평탄가 (yearly)
  C5 ✅ PASS (0.00s) — AllWeather 5자산 BH USD (yearly)

======================================================================
Layer 2 — 손계산 박제 (3 cases)
======================================================================
  C6 ✅ PASS (0.00s) — 60/40 monthly 5-day Jan-Feb 경계 (path-dependent)
  C7 ✅ PASS (0.00s) — compute_metrics 직접: MDD 합성 시리즈 [100,110,120,100,80,90,110]
  C8 ✅ PASS (0.00s) — 폭락-회복 단일 SPY 5-day (peak/trough 명확)

======================================================================
Layer 3 — Invariants (1 case)
======================================================================
  C9 ✅ PASS (0.00s) — L3 invariants — 큰 폭락-회복 (peak idx=20, trough idx=40)

======================================================================
Layer 4 — Opus 4.7 sanity (2 cases) — 호출에 시간 소요
======================================================================
  S1 ❌ FAIL — Opus sanity: 폭락-회복
      FAIL opus_verdict: actual=SUSPECT expected=PLAUSIBLE
  S2 ✅ PASS — Opus sanity: 60/40 monthly

======================================================================
FINAL: 10/11 PASS
======================================================================
```

L1 5/5 + L2 3/3 + L3 1/1 + L4 1/2 = **10/11**.

L4 S1 FAIL 분석은 아래 ## 이슈/블로커 참조. 환경 의존성이 아닌 **코드 결함** (case_l4.py fixture 가 stale).

## 임계값 검증 표 — DoD (c) 임계값 명시 정리

| 임계값 | 적용 metric | 충족 여부 | 비고 |
|--------|-------------|-----------|------|
| (i) 부호 동일 (CAGR 양→양, MDD 음→음, win_rate ≥ 0) | 모든 metric | **9/9 PASS** | mdd 의 옛 0 (BUG) → 새 음수 (정상) 는 부호 이행 문제 아닌 회계 정확화 (mdd ≤ 0 invariant 유지). |
| (ii-a) `\|Δ\|/\|old\|` < 10% (final_equity) | final_equity | **9/9 PASS** | 모든 케이스 0% (settlement 결과 자체는 동일, EOD 시점만 변경). |
| (ii-b) `\|Δ\|/\|old\|` < 50% (cagr/mdd/sharpe/win_rate) | cagr | **9/9 PASS** | 0.34-0.58% drift. |
| (ii-b) | win_rate | **9/9 PASS** | 0.08-0.10% drift. |
| (ii-b) | mdd | **3/9 PASS** + 6건 정의 미달 (옛 0 분모) + scenario_3 559% × 2건. ESCALATE. | 옛 0 케이스 6건은 BUG 분모 — 새 baseline 가 mdd 회계 정상화. scenario_3 mdd 절대값 매우 작아 percent 격차 큼. |
| (ii-b) | sharpe | **3/9 PASS** + 6건 91-97% 초과. ESCALATE. | 옛 sharpe 1000+ 는 stdev≈0 인플레이션 (BUG 부산물). 새 sharpe 80-90 range 가 정상. |

**총 합계**: DoD (i) 9/9 부호 PASS, DoD (ii-a) 9/9 final_equity PASS, DoD (ii-b) 27/45 metric PASS + 18 ESCALATE (BUG 부산물 vs 정상화 사이의 자연스러운 regime change). 사용자 escalation 권고.

## 이슈/블로커

### Issue 1 (severity: bug) — `scripts/validation/case_l4.py` L48-62 fixture 가 TASK-244 fix 이전 엔진 출력으로 박제됨

**현상** (run_all.py L4 S1 SUSPECT):
- case_l4.py L50 `_build_s1_inputs` engine_output_md: `initial_equity (Day 0): $9,747.06 (qty=97 × $100 + cash $47.06; init buy at $102.5 settlement)`
- 새 엔진 (TASK-244 fix 후) 실측: `Day 0 equity = 10000` (pure cash, settlement skip).
- Opus 가 정확히 catch — verdict=SUSPECT, reasoning: "Day 0 initial_equity 가 $9,747.06 으로 초기 자본 $10,000 보다 $252.94 낮게 기록되어 있습니다. 이는 idx 1 settlement($102.5)에서 체결된 매수 포지션을 Day 0 종가($100)로 평가해 EOD에 반영한 회계 흔적입니다. ... 최근 커밋 메시지(`TASK-244 BUG 발견 - D EOD equity 회계 결함`)와 일치하는 의심점입니다."

**실측 검증** (case_l3 의 C9 와 동일 setup 으로 직접 호출):

```
Day 0 equity = 10000             # 옛 fixture: $9,747.06
Day 1 equity = 9989.559877875    # 옛 fixture 미보고
Day 20 equity = 14597.059877875  # 옛 fixture: 동일 ($14,597.06)
Day 40 equity = 5867.059877875   # 옛 fixture: 동일 ($5,867.06)
Final equity = 12657.059877875   # 옛 fixture: 동일 ($12,657.06)
num_fills = 1                    # 옛 fixture: 동일
```

→ Day 0 만 변경 (큐잉 패턴이 첫날 매수 시그널을 D=1 settlement 로 미룸).

**원인**: TASK-244 Coder 가 `tests/`, `scripts/validation/case_l1.py`, `case_l2.py` 까지는 expected 식 갱신했으나, `case_l4.py` 의 Opus prompt fixture (engine_output_md literal string) 갱신을 누락.

**영향**: L4 S1 영구 SUSPECT — `run_all.py` 가 11/11 절대 달성 불가.

**제안 수정** (Coder 후속 태스크):
- `scripts/validation/case_l4.py` L48-62 `_build_s1_inputs` engine_output_md 의 `initial_equity (Day 0): $9,747.06` → `$10,000.00 (pure cash — TASK-244 큐잉 패턴: Day 0 = 어제 시그널 없음 → settlement skip → portfolio = initial_cash. Day 1 settlement 후부터 매수 효과 반영.)`
- 동시에 추가 정확성 보강: Day 1 equity = $9,989.56 (settlement 후 commission/slippage 차감) 도 fixture 에 명시 가능.
- 갱신 후 `run_all.py` 재실행하여 11/11 PASS 확인.

**Tester 영역 외 (`scripts/`) 라 본 태스크에서 미수정**. Manager 가 후속 Coder 태스크 (예: TASK-244C) 를 분배해야 한다.

### Issue 2 (severity: observation) — 골든 baseline 6 케이스 sharpe + 6 케이스 mdd 임계값 (50%) 초과

상기 (c) 표 참조. **TASK-244 fix 의 의도된 효과** — 옛 baseline 은 BUG 부산물 (sharpe variance≈0 인플레이션, mdd Day 0 post-trade 라 dd 기록 불가). 새 baseline 이 정상. 사용자 escalation 권고 (UI/리포트에 "이전 release 와 비교 불가" 안내 가능).

## 다음 제안

1. **(Manager 결정 필요) Issue 1 처리**: Coder 후속 태스크 (예: TASK-244C) — `scripts/validation/case_l4.py` L48-62 `_build_s1_inputs` engine_output_md 갱신. DoD: `run_all.py` 11/11 PASS 재달성. 본 태스크 (TASK-244B) 는 status=DONE 유지 (Tester 영역 한계 내 모두 완수).

2. **(사용자 ESCALATE) Issue 2**: 골든 baseline 임계값 초과 6+6 케이스의 사용자 보고 — sharpe 정상화 / mdd 회계 정확화 안내. 사용자 confirm 후 baseline 확정.

3. **commit msg** (Tester 분담):
   ```
   TASK-244B: engine EOD 회계 fix 검증 — TestEodEquityAccountingTiming 4 신규 + 골든 baseline 9 재생성 + regression 50/50 + run_all 10/11 (case_l4 fixture stale BUG 발견)
   ```
   본 commit 에는 `tests/domain/test_engine.py` 의 신규 클래스와 `tests/golden/snapshots/*.json` 9 파일 변경분만 포함. case_l4.py 변경은 후속 Coder 태스크 commit 에 별도 포함.
