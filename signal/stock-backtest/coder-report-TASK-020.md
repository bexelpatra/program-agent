---
agent: coder
task_id: TASK-020
status: DONE
timestamp: 2026-04-29T08:21:17+09:00
---

## 결과 요약

DataSource / FxSource 추상 Protocol 과 yfinance 어댑터 구현체를 추가했다.
US 주식 / Crypto OHLCV + 배당은 `YfinanceSource`, 환율은 `YfinanceFxSource`.
수집 레이어 방어 정책(close=0/null/NaN 거부 + WARNING 로깅), V1 결정 9 의 rate
limit (초당 ~2 req, 0.5s 간격) 을 어댑터에 내장했다.

## 변경된 파일

- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/data/sources/__init__.py` (신규)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/data/sources/base.py` (신규 — Protocol)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/data/sources/yfinance_source.py` (신규)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/data/__init__.py` (수정 — 8 심볼 re-export 추가)

### 공개 API (신규)

`app.data` (re-export):
- `DataSource` (Protocol): `fetch_ohlcv(symbol, start, end) -> list[OhlcvBar]`, `fetch_dividends(symbol, start, end) -> list[DividendEvent]`, `validate_ticker(symbol) -> TickerValidation`
- `FxSource` (Protocol): `fetch_fx(base_ccy, quote_ccy, start, end) -> list[FxBar]`, `validate_pair(base_ccy, quote_ccy) -> bool`
- `OhlcvBar`, `FxBar`, `DividendEvent`, `TickerValidation` (frozen dataclass)
- `YfinanceSource`, `YfinanceFxSource` (구현체)

## DoD 검증 결과

| # | 검증 | 결과 |
|---|------|------|
| 1 | `python -c "from app.data import DataSource, FxSource, OhlcvBar, FxBar, DividendEvent, TickerValidation, YfinanceSource, YfinanceFxSource; print('ok')"` | `ok` (PASS) |
| 2 | `YfinanceSource().validate_ticker('SPY')` | `exists=True, has_min_history=True, earliest=2025-04-29, latest=2026-04-28` (PASS) |
| 3 | `YfinanceSource().validate_ticker('XYZNOTEXIST123')` | `exists=False, has_min_history=False, note='데이터 없음'` (PASS) |
| 4 | `YfinanceSource().fetch_ohlcv('SPY', today-10d, today)` | bar 7건, 첫 bar `time=2026-04-20 EDT, close=708.72, volume=43,546,800` (PASS) |
| 5 | close=0/null 거부 단위 테스트 | 코드 리뷰만 — `_is_invalid_close()` 가 None/NaN/0 모두 차단. 단위 테스트는 TASK-081 |
| 6 | `YfinanceFxSource().validate_pair('USD', 'KRW')` | `True` (PASS) |

> venv 활성화 필요: `source projects/stock-backtest/.venv/bin/activate`

## 클린 코드 / 클린 아키텍처 자체 점검

- **계층 의존**: `data/sources/*` 는 외부 라이브러리(yfinance) 와 stdlib 만 import. domain/presentation 역방향 의존 없음.
- **DataSource vs FxSource 분리**: 통화 페어(FX) 와 ticker(주식/암호화폐) 는 도메인이 다르므로 별도 Protocol.
- **dataclass(frozen=True)**: `OhlcvBar`, `FxBar`, `DividendEvent`, `TickerValidation` 모두 불변 — 부주의한 mutation 방지.
- **단일 책임**: `_rate_limit`, `_is_nan`, `_safe_float`, `_is_invalid_close`, `_fx_symbol` 모두 한 가지 일.
- **이름**: `_is_invalid_close` (질문형), `_fx_symbol` (의도 드러냄), `note` (한글 가능 — UI/UX 원칙).
- **주석 = Why**: `_RATE_LIMIT_SLEEP_SEC` 옆에 V1 결정 9 근거, `_is_nan` 에 NaN 자기-비교 트릭 이유 명시.
- **확장 포인트**: `pykrx` (TASK-021) / `pyupbit` 등도 동일 base.py Protocol 을 구현하면 plug-in 가능.

## 이슈/블로커

없음. 네트워크 검증 4건 모두 PASS.

## 다음 제안

1. **TASK-081 (단위 테스트)**: `_is_invalid_close` (None/NaN/0 모두 거부), `_fx_symbol` (USD base vs others), `_safe_float` 의 분기를 mock pandas Row 로 검증. 네트워크 없이 가능.
2. **rate limit token bucket 화**: 현재 모듈 글로벌 lock + sleep 은 단일 프로세스 한정. 멀티 프로세스 (스케줄러 + API 동시 fetch) 환경에서는 burst 보호가 약하다. APScheduler 통합 시점(TASK-070+)에서 재검토 권고.
3. **pykrx 어댑터**: KR 주식은 yfinance 로도 가능하나 KOSPI/KOSDAQ 정합성·배당락 보정은 pykrx 가 정확. base.py 그대로 구현체만 추가하면 된다 — TASK-021 분리 권장.
4. **timezone 정규화 책임 명시**: 어댑터는 yfinance 가 주는 timezone-aware datetime 그대로 반환. 저장 레이어(SqlOhlcvRepository, TASK-040 추정) 에서 UTC 정규화 + 시장 캘린더 정렬 필요. architecture.md 의 "데이터 정규화" 섹션에 책임 분담을 명시하면 후속 confusion 방지.
