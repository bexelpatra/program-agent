---
agent: coder
task_id: TASK-214
status: DONE
timestamp: 2026-04-30T00:00:00
---

## 결과 요약

분할/증자/감자 임시처방을 A 방향으로 적용했다.

- **yfinance**: `fetch_ohlcv` 의 `ticker.history(...)` 호출을 `auto_adjust=False` →
  `auto_adjust=True` 로 전환. 이제 close 자체가 split/dividend 소급 보정된 가격을
  반환하므로, 엔진(`close` 만 사용)에서 분할 시 가짜 시그널이 발동하지 않는다.
  `OhlcvBar.adj_close` 는 호환성 유지 — auto_adjust=True 시 'Adj Close' 컬럼이
  'Close' 와 동일 값이거나 누락될 수 있어 누락 시 close 값으로 fallback 추가.
  지시사항대로 `earliest_available()` (TASK-213 산출물) 은 건드리지 않았다.
- **pykrx**: 비조정가 한계를 코드 도크스트링에 명시 (한국 ETF 는 분할이 거의 없어
  실전 영향 적음). 정공법은 BLOCKER-003 → Phase 2 백로그.
- **architecture.md**: "거래 정책" 섹션 (배당 처리 직후, L647 전) 에 "분할/증자/감자
  처리 (V3 MVP 임시처방)" 서브섹션을 추가. yfinance/pykrx 정책과 정공법 (Phase 2)
  방향 명시.
- **blockers.md**: BLOCKER-003 [SOFT] (TASK-214) 등록. corporate_actions SPLIT
  이벤트 엔진 적용 + pykrx 분할 데이터 수집 정공법을 사유/우회 방안과 함께 적재.

호출부 추가 점검:
- `validate_ticker` (L130) 는 `ticker.history(period="1y")` (기본값) — 데이터 존재
  여부만 확인하므로 변경 불필요.
- `fetch_dividends` (L116) 는 `ticker.dividends` attribute — `history()` 의
  `auto_adjust` 와 무관 (별도 actions API).
- `earliest_available` (L171, TASK-213) 은 지시사항대로 변경 금지.

## 변경된 파일

- `projects/stock-backtest/backend/app/data/sources/yfinance_source.py` (수정)
  - L83: `auto_adjust=False` → `auto_adjust=True`
  - L72-85: 클래스 docstring 갱신 (TASK-214 임시처방 명시)
  - L101-108: 'Adj Close' 누락 시 close 값 fallback 추가
- `projects/stock-backtest/backend/app/data/sources/pykrx_source.py` (수정)
  - L100-103: 클래스 docstring 갱신 (BLOCKER-003 Phase 2 명시)
- `signal/stock-backtest/architecture.md` (수정)
  - L647-654: 거래 정책 섹션에 "분할/증자/감자 처리 (V3 MVP 임시처방)" 추가
- `signal/stock-backtest/blockers.md` (수정)
  - BLOCKER-003 [SOFT] (TASK-214) 신규 추가

## 회귀 검증

`/home/jai/pa/stock-backtest/projects/stock-backtest/.venv` (프로젝트 venv) 사용.

```
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/pytest \
    tests/data/test_pipeline.py tests/regression/test_calendar_defense.py
```

- 결과: **29 passed** (기존 yfinance fetch_ohlcv mock 회귀 1건 포함, NaN drop 동작 유지).
- 추가: import smoke (`YfinanceSource`, `PykrxSource`) OK.

가격 데이터 변동에 따른 골든 baseline 갱신은 이 태스크 범위 밖 — TASK-215 에서 통합 처리.

## Public API 변경

없음. `fetch_ohlcv` 의 시그니처/반환 타입 동일. `OhlcvBar.adj_close` 는 동일하게
`float | None` 이지만 의미가 "auto_adjust 적용된 close 사본" 으로 사실상 변화한다
(실전 영향: 호출부는 여전히 `close` 만 사용해야 하며, `adj_close` 는 호환성용).

## 이슈/블로커

- **BLOCKER-003 [SOFT]**: 분할/증자/감자 정공법은 Phase 2 백로그. MVP 임시처방으로
  yfinance 자산은 자동 보정되나, pykrx 자산 (한국 ETF) 은 비조정 한계가 그대로 남는다.
  한국 ETF 분할 발생 시 가짜 시그널 가능성. blockers.md 에 등재.
- **가격 fixture 변동 가능성**: 이미 캐시된 yfinance ohlcv (DB 적재분) 가
  auto_adjust=False 시점 데이터라면, 차후 백필 시 동일 자산의 과거 가격이
  소급 보정된 값으로 갱신된다. 골든 baseline 재생성 (TASK-215) 에서 통합 검증.
- **TASK-211 충돌 위험**: 동시 진행 중. TASK-214 는 data/sources, signal/architecture,
  signal/blockers 만 수정. TASK-211 은 engine.py 수정. 충돌 없음 확인.

## 다음 제안

- **TASK-215 (Tester)**: 골든 baseline 9 케이스 통합 재생성 시 yfinance 자산
  (US/Crypto) 의 과거 close 값이 분할/배당 소급 보정으로 변경됨을 baseline 에
  반영. baseline 변경분이 클 경우 (예: AAPL, NVDA 같은 split 있는 종목) 변경
  사유 commit msg 명시 필요.
- **TASK-216 (사용자 통지)**: BTC ohlcv 재백필 안내. BTC 는 split 이 없으나
  배당도 없으므로 auto_adjust=True 영향 0. 그러나 다른 yfinance 자산
  (SPY/QQQ/AAPL 등) 은 dividend reinvest 형태로 과거 가격이 보정되므로
  재백필 권장 — 사용자 통지 메시지에 추가 검토 권장.
- **Phase 2 정공법**: BLOCKER-003 처리 시 (a) `corporate_actions` 테이블에 SPLIT
  타입 row 적재, (b) pykrx/yfinance 양쪽에서 SPLIT 이벤트 별도 수집 어댑터,
  (c) 엔진 EOD 시점 portfolio.position.qty 동적 조정 로직 (배당 cash 입금과
  유사 패턴), (d) 비조정 close 사용 (yfinance auto_adjust=False 복원) 의 4단계
  태스크로 분해 가능.
