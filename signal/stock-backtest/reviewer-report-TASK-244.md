---
task_id: TASK-244
verdict: PASS
reviewer: opus-4.7
reviewed_at: 2026-05-06
revision: r2
---

# Reviewer Report — TASK-244 (재검증 r2)

## 검증 대상 (재검증)

- `signal/stock-backtest/task-board.md` L202 (정정된 TASK-244 entry)
- 이전 회차 NEEDS_REVISION 의 R1~R6 항목 반영 여부

## R1~R6 재검증 결과 (grep 실측)

### R1. `run_backtest` 라인 범위 정정 — ✓ 반영

```
$ grep -c "L172-329\|메인 루프 본체 L204-322" task-board.md
1
$ grep -n "L204-329" task-board.md
(매치 없음)
```
정정 후 본문 L202 에 **"`run_backtest` (L172-329, 메인 루프 본체 L204-322) 재구성"** 명시. 이전 잘못된 "L204-329" 단독 표현은 완전히 제거됨. "L204-322 실측" 도 함께 등장 (현재 흐름 묘사 시 메인 루프 구간으로 사용).

### R2. 갱신 대상 파일·함수 정확히 짚기 — ✓ 반영

```
$ grep -c "_helpers.py:319" task-board.md
1
$ grep -c "함수 자체는 변경" task-board.md
1
$ grep -c "L36-78" task-board.md
1
$ grep -c "Jan 30 settlement" task-board.md
1
```

본문에서 모두 확인:
- "**`_helpers.py:319` 의 `closed_form_initial_buy` 함수 자체는 변경 없음** (매수 1회 spec 동일, 시점만 D 0→1 로 이동)"
- "갱신 대상은 **각 case 의 expected_initial_equity / expected_final_equity 산출 식**"
- c1 (L95~) / c2 (L160~, L171) / c3 (L228~) / c4 (L303,310) / c5 (L429~) 모두 라인 번호 명시
- "case_l2.py L36-78 `case_c6_sixty_forty_monthly_mini` docstring **hand-trace 전면 재작성** (Day 0 = pure cash, Jan 29 시그널 → Jan 30 settlement, 5-day equity_curve 자체 재계산)"

→ Coder 가 `_helpers.py` 를 수정하려 들 위험 제거.

### R3. validation harness "11/11" vs "9 케이스" 모호 해소 — ✓ 반영

```
$ grep -c "L1+L2+L3 = 9 케이스" task-board.md
1
$ grep -c "L4 제외" task-board.md
1
$ grep -c "L4 2/2 = 11/11" task-board.md
1
```

본문: "**validation harness 영향 (L1+L2+L3 = 9 케이스 갱신, L4 제외)**" + "L4 (`case_l4.py` S1, S2 Opus 정성 평가) 는 baseline 갱신 대상 **아님** — 정성 spec 변동 없음. 최종 `run_all.py` 출력 = **9/9 PASS (L1~L3) + L4 2/2 = 11/11** 재달성".

→ "9 케이스 갱신" / "11/11 PASS" 가 동시에 등장하던 모호함 해소.

### R4. `architecture.md` DoD (e) 상태 명시 — ✓ 반영

```
$ grep -c "ec5b32d" task-board.md
1
$ grep -c "선반영" task-board.md
1
$ grep -c "Coder 추가 수정 없음" task-board.md
1
```

DoD (e) 가 "**`architecture.md` L635-648 § 'EOD equity 기록 시점 (TASK-244 fix 후 명시)' 는 commit `ec5b32d` 에서 이미 선반영 완료 — Coder 추가 수정 없음.**" 으로 명시. "(필요 시 큐잉 패턴 흐름이 더 정확히 묘사되도록 미세 보강만 가능, 신규 섹션 추가 X.)" 라는 안전 가드도 추가됨.

→ Coder 가 architecture 를 또 수정하려다 충돌·중복 작업할 위험 제거.

### R5. 단위 테스트 4 케이스 위치 명시 — ✓ 반영

```
$ grep -c "TestEodEquityAccountingTiming" task-board.md
1
$ grep -c "test_day_0_eod_is_pure_cash" task-board.md
1
$ grep -c "test_day_1_eod_is_post_init_trade\|test_sell_signal_d_eod_still_holds\|test_buy_signal_d_eod_still_cash" task-board.md
1
```

DoD (a) 에 "`tests/domain/test_engine.py` 에 신규 클래스 **`TestEodEquityAccountingTiming`** 추가 (4 메소드: `test_day_0_eod_is_pure_cash` / `test_day_1_eod_is_post_init_trade` / `test_sell_signal_d_eod_still_holds` / `test_buy_signal_d_eod_still_cash`)" 모두 명시 + 각 메소드의 검증 의미도 짧게 inline 설명.

### R6. DoD (b) / (c) 분리 + 임계값 명시 — ✓ 반영

```
$ grep -c "test_calendar_defense.py.*test_cash_by_ccy.py" task-board.md
1
$ grep -c "0 회귀" task-board.md
6
$ grep -c "10%\|50%" task-board.md
1
$ grep -c "Δ" task-board.md
1
```

본문:
- DoD (b): "기존 회귀 테스트 3 파일 (`tests/regression/test_lookahead.py`, `test_calendar_defense.py`, `test_cash_by_ccy.py`) **0 회귀** (모두 통과; 실패 시 분석 후 보고)" — 3 파일 명시 + 실패 시 절차도 포함.
- DoD (c): "골든 9 baseline 재생성 + **측정 가능한 검증**: (i) 모든 metric 의 부호(sign) 동일 (CAGR 양→양, MDD 음→음 등), (ii) `|Δ| / |old|` 가 `final_equity` / `peak_equity` 에서 < 10%, `mdd` / `sharpe` / `cagr` 에서 < 50% 이내. 초과 시 사용자에게 케이스별 전후 표 보고 후 진행 여부 확인."

→ 측정 가능한 임계값 + 초과 시 escalation 절차까지 명시.

## 이전 PASS 항목 손상 여부 재확인

- **모델 A 의미 보존 (큐잉 패턴)**: ✓ 보존. "pending_rebalance" + "어제 시그널을 오늘 settlement" 패턴 그대로.
- **`tests/golden/snapshots/` 9 파일 정합**: ✓ 보존. "9 파일 (`scenario_{1_kr_only,2_kr_us,3_us_crypto}__{all_weather,equal_weight,fixed_weight}.json`)" 그대로 명시.
- **마지막 iteration 정책 + architecture.md L646 정합**: ✓ 보존. "정책 (a) 채택: timeline 마지막 D 의 시그널은 체결 안 됨 ... architecture.md L646 와 정합" 그대로.
- **`next_trading_day` 호출 1곳 (L249-255 try/except + L251) 제거 + L38 import 제거**: ✓ 보존. 동일 라인 번호 인용.
- **engine.py 흐름 묘사 정합**: ✓ 보존. L211 / L222-227 / L251 / L272-279 / L309-313 등 라인 번호 그대로 인용.

신규 손상 발견 사항 없음.

## 신규 지적 사항

없음. 이전 6 항목 모두 정확히 반영됨.

## 최종 판정

**PASS**

Manager 는 즉시 Coder 를 호출 가능. 호출 시 다음을 명시:
- `agents/coder.md` + 프로젝트 경로 (PROJECT_ID, SIGNAL_DIR, PROJECT_ROOT)
- TASK-244 description (task-board L202)
- 참조: `signal/stock-backtest/architecture.md` L618-648, `validation-report.md`
- report 경로: `signal/stock-backtest/coder-report-TASK-244.md`

도메인 코어 완료 직후 Reviewer 재호출 권장 (CLAUDE.md 마일스톤 재검증 권장 항목): engine.py 큐잉 패턴 재구성 + 골든 baseline 재생성 직후 — 측정 가능한 임계값 (DoD c) 충족 여부를 Coder report 의 자체 주장만으로 신뢰하지 말고 Reviewer 가 git diff + baseline 변동량을 독립 검증하면 좋다.
