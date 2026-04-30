---
task_id: TASK-211, TASK-212, TASK-213, TASK-214, TASK-215, TASK-216
verdict: PASS
---

# Reviewer Report: 엔진 결함 수정 6 태스크 재검증 (TASK-211~216)

(2026-04-30 BTC 분기 리밸런싱 시나리오 결함 수정 — 직전 NEEDS_REVISION 6 항목 후속 검증.)

## 검증 대상
- 파일:
  - `/home/jai/pa/stock-backtest/signal/stock-backtest/task-board.md` L99-121 (엔진 결함 수정 섹션 + 실행 순서 권고)
  - 코드 인용 재검증:
    - `backend/app/domain/engine.py` L210-258 (target_weights 분기 + execute_rebalance 호출)
    - `backend/app/domain/trade.py` L79-92 (TradeFill), L171-194 (_classify_orders), L197-230 (_execute_sells), L233-293 (_execute_buys), L296-374 (execute_rebalance + L361/L366 sell/buy_fills 호출)
    - `backend/app/services/backtest_runner.py` L226-251
    - `backend/app/data/pipeline.py`, `backend/app/data/sources/{base,yfinance_source,pykrx_source}.py`
    - `backend/tests/golden/snapshots/` (9 파일)
  - `signal/stock-backtest/blockers.md` (BLOCKER-001/002 존재, 003 추가 예정)
- Manager 주장 요약: 직전 NEEDS_REVISION 6 항목 모두 task-board.md 에 반영 완료.

## 직전 6 수정 요청 반영 검증

### 1. TASK-211 — invariant 명시 + KeyError silent 0 금지 정책

**요구**: 빈 dict entry path 에서 prices/asset_meta 가 보유 자산 cover 한다는 invariant + KeyError 명시 처리.

**반영 확인** (task-board.md L108):
- ③ "**invariant 명시**: 빈 target_weights entry path 에서 `prices` (=settlement_prices) 와 `asset_meta` 가 **현재 보유 자산까지 cover** 한다는 가정을 단위 테스트로 박제. 보유 자산이 universe 부분집합이라는 불변 조건." — 명시.
- ④ "**에러 정책**: 보유 자산이 prices/asset_meta 에 없으면 silent 0 금지 정책에 따라 `MissingPriceError` 명시적 예외 (현 trade.py L210-215 fallback 은 매도용 sell-only 청산이라 OK, 단 asset_meta 부재 시 KeyError 명시 catch)." — 명시.
- 테스트: "boundary '보유 자산이 universe 의 부분집합' invariant 검증" 추가됨.

**판정: 반영 OK**

### 2. TASK-212 — `_execute_sells/_execute_buys` 시그니처 변경 4단계 풀어쓰기

**요구**: ② sells/buys 시그니처에 rebalance_date 인자 추가, ③ execute_rebalance 호출 시 rebalance_date 전달, ④ TradeFill 에 settlement_date=rebalance_date 채움, ⑤ backtest_runner.py:242 datetime.combine 으로 교체.

**반영 확인** (task-board.md L109):
- ① TradeFill 에 settlement_date 추가 — 명시.
- ② `_execute_sells` (L197) / `_execute_buys` (L233) 시그니처에 `rebalance_date: date` 인자 추가 — 명시 (실측 라인 L197/L233 정확).
- ③ `execute_rebalance` (L361 sell_fills 호출, L366 buy_fills 호출) 가 `rebalance_date=rebalance_date` 전달 — 명시 (실측: L361 `sell_fills = _execute_sells(`, L366 `buy_fills = _execute_buys(` 정확).
- ④ TradeFill 생성 시 settlement_date=rebalance_date 채움 (L228, L290 두 위치) — 명시 (실측: L227-229 SELL TradeFill, L290-292 BUY TradeFill, ±2 라인 허용 내).
- ⑤ backtest_runner.py:242 를 `datetime.combine(fill.settlement_date, datetime.min.time(), tzinfo=timezone.utc)` 로 교체 — 명시 (실측 L242 `"time": getattr(fill, "time", now),` 정확).

**판정: 반영 OK** (5 단계 모두 정확한 라인·시그니처로 풀어쓰기 완료)

### 3. TASK-213 — 운영 액션 분리

**요구**: 옵션 A (별도 신규 태스크 TASK-216 분리) 또는 옵션 B (본문 명확화).

**반영 확인** (task-board.md L110, L113):
- TASK-213 description 끝: "**이 태스크는 코드 변경만 담당** — BTC ohlcv 재백필 운영 액션은 TASK-216 (Execution=user) 분리." — 명시.
- TASK-216 신규 등록: "BTC asset_id=56 ohlcv 전체 삭제 + 재백필 수동 트리거", Execution=`user`, Assignee=`manager`, Depends On=TASK-213.

**판정: 반영 OK** (옵션 A 채택, 깔끔한 분리)

### 4. TASK-214 — `auto_adjust=True` 한 가지로 결정 명시

**요구**: Manager 가 결정해서 한 가지로 명시. 권장 = `auto_adjust=True`.

**반영 확인** (task-board.md L111):
- 제목: "분할/증자/감자 처리 — 임시처방 (A 방향: yfinance auto_adjust=True 전환 + pykrx 한계 명시)" — 결정 명시.
- "**결정 명시**: `auto_adjust=True` 채택 (close 자체가 분할/배당 소급 보정. OhlcvBar.close 만 사용하면 끝, 호출부 변경 최소). `OhlcvBar.adj_close` 는 호환성 위해 유지 (auto_adjust=True 시 Adj Close 동일 값)." — 결정 근거 명시.
- ① yfinance_source.py:83 `auto_adjust=False` → `auto_adjust=True` — 단일 변경 명시.
- ③ architecture.md "거래 정책" 섹션 갱신 sub-action 명시.

**판정: 반영 OK** (한 가지로 결정 + 결정 근거까지 박제)

### 5. 실행 순서 권고 + golden baseline 통합 재생성 책임자 (TASK-215) 신설

**요구**: TASK-211/212/214 모두 DONE 후 TASK-215 신설 (단일 책임자) + 실행 순서 명시.

**반영 확인** (task-board.md L112, L115-121):
- TASK-215 신규 등록: "골든 baseline 9 케이스 통합 재생성", Assignee=`tester`, Depends On=`TASK-211, TASK-212, TASK-214`, 9 파일 명시 (`scenario_{1,2,3}__{fixed,all,equal}_weight.json`).
- 실측: `backend/tests/golden/snapshots/` 디렉토리에 9 파일 모두 존재 (scenario_1_kr_only / scenario_2_kr_us / scenario_3_us_crypto × all_weather/equal_weight/fixed_weight). 단, **파일명이 description (`scenario_{1,2,3}__{fixed,all,equal}_weight.json`) 과 일치하지 않음** (실제: `scenario_1_kr_only__fixed_weight.json` 형태). Coder/Tester 가 파일을 실제 디렉토리에서 보고 작업할 가능성이 높아 큰 위험은 아님 — 관찰만 기록 (NEEDS_REVISION 사유는 아님).
- "## 실행 순서 권고" 섹션 (L115-121) 추가:
  1. 순차 1: TASK-212 → TASK-211 (TradeFill 모델 변경 먼저)
  2. 순차 2: TASK-213 → TASK-214 (yfinance/pykrx 동일 파일 충돌 회피)
  3. 병렬: 순차 1 ↔ 순차 2
  4. 마지막: TASK-215 (단일 책임자)
  5. 사용자 액션: TASK-216 (TASK-213 DONE 후)

**판정: 반영 OK** (실행 순서·책임자 모두 명시. 파일명 사소 불일치는 observation)

### 6. golden baseline 갱신 시 git diff/commit message 가이드

**요구**: 각 description 에 git diff 변경 양상 (청산 trade 추가 / time 필드 변경 / 가격 보정 변동) + 회귀 의도 commit message 명시.

**반영 확인**:
- TASK-211 (L108): "**회귀 의도 commit msg**: 'TASK-211: filter fail 시 보유 청산 추가 — 골든 trades 청산 패턴 추가됨'" — 명시.
- TASK-212 (L109): "**회귀 의도 commit msg**: 'TASK-212: TradeFill.settlement_date 추가 — trades 시간 필드가 settlement_d 로 변경'" — 명시.
- TASK-214 (L111): "**회귀 의도 commit msg**: 'TASK-214: yfinance auto_adjust=True — 가격이 split/dividend 소급 보정된 값으로 변경'" — 명시.
- TASK-215 (L112): git diff 변경 양상 검증 명시 ((a) 청산 trade 신규 추가, (b) trade time 필드가 settlement_date 로 변경, (c) 가격 값이 분할 보정 값으로 변경) + commit message "TASK-215: golden baseline 재생성 — TASK-211(청산) + TASK-212(time) + TASK-214(가격보정) 누적 반영" 명시.

**판정: 반영 OK** (4 태스크 모두 일관된 git diff/commit msg 가이드)

## 추가 검증

### TASK-215 Tester 할당 적절성

- TASK-215 의 본질은 "9 케이스 fixture regenerate + git diff line-by-line 검증" — 코드 변경 없이 테스트 baseline 갱신 + 회귀 의도 검증.
- 골든 스냅샷 변경 의도 검증은 Tester 의 본업 (회귀 catch). Coder 가 자기 코드 변경을 정당화하는 것보다 Tester 가 독립 검증이 적합.
- **판정: Tester 할당 적절**

### TASK-216 Execution=user 적절성

- 본질: ① DB 직접 SQL DELETE ② backfill API/scheduler trigger ③ DB SELECT 검증 — 모두 운영 액션 (코드 변경 0).
- DB 직접 조작은 Coder 자율 실행 시 환경 의존성·돌이킬 수 없는 위험 (asset_id=56 데이터 영구 삭제) 존재. 사용자 명시 동의 필요.
- 자산 ID 56 이 실제 BTC 인지 사용자 환경 확인 필요 (다른 환경에서는 다른 ID 일 수 있음).
- **판정: Execution=user 적절**

### 실행 순서 권고와 의존성 일관성

| 권고 순서 | task-board Depends On | 일관성 |
|-----------|----------------------|--------|
| 순차 1: TASK-212 → TASK-211 | TASK-211 Depends On = `TASK-212` | OK |
| 순차 2: TASK-213 → TASK-214 | TASK-214 Depends On = `TASK-213` | OK |
| 마지막: TASK-211/212/214 → TASK-215 | TASK-215 Depends On = `TASK-211, TASK-212, TASK-214` | OK |
| 사용자 액션: TASK-213 → TASK-216 | TASK-216 Depends On = `TASK-213` | OK |
| TASK-212 = 시작점 (선행 없음) | TASK-212 Depends On = `-` | OK |
| TASK-213 = 시작점 (선행 없음) | TASK-213 Depends On = `-` | OK |

**판정: 6/6 모두 일관 — 실행 순서 권고와 Depends On 컬럼 완벽 일치**

## 목적성·클린 아키텍처 (재확인)

- 6 태스크 모두 architecture.md V3 § "거래 정책" + Quant Lab CLAUDE.md "백테스팅 실거래 반영도 70%" + "비거래일 방어" 원칙 부합.
- TASK-211/212 = bug (실거래 반영도 위반). TASK-213/214 = bug + 임시처방 박제. TASK-215 = baseline 회귀 검증. TASK-216 = 운영 액션.
- 클린 아키텍처: domain ↔ data 의존 방향 위반 없음. test 디렉토리는 backend/tests/golden 으로 일관.

## 추후 수정 용이성

- TASK-212 의 `TradeFill.settlement_date` 필드 추가 → 후속 fill 사용처 (Tax/Reporting/UI) 가 그 필드 활용 가능.
- TASK-213 의 `earliest_available` 추상 메서드 → DataSource Protocol 확장이라 향후 어댑터 (Upbit/한국은행) 일관 적용.
- TASK-214 의 임시처방 → BLOCKER-003 으로 정공법 (Phase 2) 박제.
- TASK-215 의 baseline 단일 책임자 → 향후 비슷한 누적 변경 시 동일 패턴 재사용 가능.

## 판정
**PASS**

판정 사유:
- 직전 6 수정 요청 모두 task-board.md 에 정확히 반영 (5/6 완벽 일치, 1/6 = 골든 파일명 표기 사소 불일치는 observation 수준).
- 라인 인용 정확도: TASK-212 의 5 단계 시그니처 변경 명세 (L197/L233/L228/L290/L361/L366/L242) 모두 실측 일치.
- TASK-215/216 신규 추가가 적절한 책임 분리 (Tester baseline / user 운영 액션).
- 실행 순서 권고 ↔ Depends On 컬럼 6/6 일관.
- Manager 가 Coder/Tester 호출 가능 신호.

## 권장 호출 순서 (Manager 행동 가이드)

병렬 가능한 첫 라운드:
1. **Coder TASK-212** (TradeFill 모델 변경) — 시작점, 선행 없음.
2. **Coder TASK-213** (earliest_available 추상 메서드 + yfinance/pykrx 구현) — 시작점, 선행 없음.

위 둘은 서로 다른 파일 (`domain/trade.py + services/backtest_runner.py` vs `data/sources/* + data/pipeline.py`) 이라 병렬 실행 안전. 각각 별도 report 파일 (`coder-report-TASK-212.md`, `coder-report-TASK-213.md`) 사용 권장.

각각 DONE 후:
3. **Coder TASK-211** (engine 청산) — TASK-212 의 TradeFill.settlement_date 가 도입돼 있어야 함.
4. **Coder TASK-214** (yfinance auto_adjust=True + pykrx 코멘트) — TASK-213 의 earliest_available 메서드와 같은 파일이라 순차.

3/4 도 서로 독립이라 병렬 가능 (engine vs sources).

마지막:
5. **Tester TASK-215** (골든 baseline 9 케이스 재생성) — TASK-211/212/214 모두 DONE 후.
6. **사용자 통지 TASK-216** — TASK-213 DONE 후 Manager 가 사용자에게 manual 전달.

## Manager 에게 전달

- PASS 판정 — Coder 호출 진행 가능.
- 첫 라운드: Coder TASK-212 + TASK-213 병렬 호출 권장 (위 권장 호출 순서 1·2).
- 마일스톤 재검증 권장 시점: TASK-211 + TASK-212 + TASK-214 모두 DONE 직후 (TASK-215 진입 전) — 누적 변경의 일관성 독립 검증.
- 작은 관찰 (NEEDS_REVISION 아님): TASK-215 description 의 골든 파일명 표기 (`scenario_{1,2,3}__{fixed,all,equal}_weight.json`) 가 실제 디렉토리의 파일명 패턴 (`scenario_1_kr_only__fixed_weight.json` 등) 과 다름. Tester 가 실제 디렉토리에서 파일을 직접 listing 해서 작업할 것이라 위험은 낮으나, 다음 회차에서 정확 파일명으로 갱신하면 더 명료.
