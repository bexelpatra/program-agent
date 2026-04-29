---
agent: coder
task_id: TASK-021
status: DONE
timestamp: 2026-04-29T09:05:00+09:00
---

## 결과 요약

KR 주식 / ETF 데이터 어댑터 `PykrxSource` (DataSource Protocol 구현체) 를 추가했다.
TASK-020 의 `base.py` Protocol 시그니처를 그대로 따르고, yfinance_source 와 동일한
방어 정책 (close=0/null/NaN 거부 + WARNING 로깅) 과 모듈 단위 rate limit lock 패턴을
재사용했다. V1 결정 9 의 pykrx 100ms sleep 을 어댑터 내부에 내장했다.

배당 (분배금) 은 pykrx 가 종합 API 를 제공하지 않아 빈 리스트를 반환하며,
**BLOCKER-002 [SOFT]** 로 등록했다 (한국 ETF 백테스트 시 배당 수익 누락 — UI 고지 필요).

## 변경된 파일

- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/data/sources/pykrx_source.py` (신규)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/data/sources/__init__.py` (수정 — `PykrxSource` re-export 추가)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/data/__init__.py` (수정 — `PykrxSource` re-export 추가)
- `/home/jai/pa/stock-backtest/signal/stock-backtest/blockers.md` (수정 — BLOCKER-002 [SOFT] 신설)

### 공개 API (신규)

`app.data` (re-export):
- `PykrxSource` (DataSource 구현체)
  - `fetch_ohlcv(symbol, start, end) -> list[OhlcvBar]` — KST timezone-aware
  - `fetch_dividends(symbol, start, end) -> list[DividendEvent]` — **MVP 빈 구현**
  - `validate_ticker(symbol) -> TickerValidation` — 한국어 note

ticker 형식: 한국거래소 6자리 종목코드 (예: `'069500'` = KODEX 200). yfinance 의
`069500.KS` 와 다르게 접미사 없음.

## DoD 검증 결과

| # | 검증 | 결과 |
|---|------|------|
| 1 | `python -c "from app.data.sources import PykrxSource; print('ok')"` | `ok` (PASS) |
| 2 | `PykrxSource().validate_ticker('069500')` (KODEX 200) | `exists=True, has_min_history=True, earliest=2025-04-29, latest=2026-04-28, note=None` (PASS) |
| 3 | `PykrxSource().validate_ticker('999999')` | `exists=False, has_min_history=False, note='한국거래소 종목코드가 아니거나 데이터 없음'` (PASS) |
| 4 | `PykrxSource().fetch_ohlcv('069500', today-10d, today)` | bar 7건, 첫 bar `time=2026-04-20 00:00 +09:00, open=94485.0, high=95435.0, low=93755.0, close=94500.0, adj_close=94500.0, volume=14275549.0` (PASS) |
| 5 | `PykrxSource().fetch_dividends('069500', today-365d, today)` | `[]` (PASS — MVP 빈 구현, BLOCKER-002 SOFT) |

> 모든 검증은 venv `/home/jai/pa/stock-backtest/projects/stock-backtest/.venv` 의 pykrx 1.2.7 로 실측 (네트워크/KRX 가용 환경 확인).
> "KRX 로그인 실패: KRX_ID 또는 KRX_PW 환경 변수가 설정되지 않았습니다." 는 pykrx import 시 늘 출력되는 정보 메시지이며, 공개 시세 조회에는 영향 없음 (실측 OHLCV 정상 반환).

## BLOCKER 등록

`signal/stock-backtest/blockers.md` 에 신설:

```
## BLOCKER-002 [SOFT] (TASK-021)
- 발견 시점: 2026-04-29T09:00
- 차단 영역: 데이터 수집 / 한국 ETF 배당 (분배금)
- 사유: pykrx 1.2.7 이 ETF 분배금 / 주식 배당을 종합 API 로 제공하지 않아
  PykrxSource.fetch_dividends 가 빈 리스트를 반환한다 (실측 확인: 069500 1년 구간 []).
  한국 ETF 백테스트 결과에서 배당 수익이 누락된다.
- 우회 방안: MVP 는 빈 구현으로 진행. 향후 KRX 정보시스템 분배금 API 또는 별도
  데이터 소스(예: FinanceDataReader, KRX OpenAPI) 도입 필요. UI 에 "KR 자산은 배당
  미반영" 명시 (UI/UX 원칙 2).
- 처리 결과: TODO
```

## 클린 코드 / 클린 아키텍처 자체 점검

- **인터페이스 일치**: `PykrxSource` 는 `base.DataSource` Protocol 시그니처와 정확히 일치 — `fetch_ohlcv`, `fetch_dividends`, `validate_ticker` 셋 모두 동일 매개변수/반환형. `YfinanceSource` 와 교체 가능.
- **계층 의존**: `data/sources/pykrx_source.py` 는 외부 라이브러리 (`pykrx`) 와 stdlib 만 import. domain/presentation 역방향 의존 없음.
- **수집 레이어 방어**: yfinance_source 와 동일한 `_is_invalid_close` 정책 적용 — close=0/null/NaN 모두 차단 + WARNING 로깅. close=0 은 비거래일/거래정지 신호이므로 어댑터에서 미리 거른다.
- **timezone 처리**: pykrx 가 naive datetime 을 반환하므로 `_to_kst()` 헬퍼로 KST(`+09:00`) timezone 강제 부여. 저장 레이어 UTC 정규화는 호출자 책임 (TASK-040).
- **rate limit**: 모듈 글로벌 lock + 100ms sleep — yfinance 보다 5배 관대 (V1 결정 9). yfinance_source 와 별도 lock 사용 — pykrx ↔ yfinance 호출이 서로의 budget 을 잠식하지 않는다.
- **단일 책임 헬퍼**: `_rate_limit`, `_is_nan`, `_safe_float`, `_is_invalid_close`, `_to_kst` 각각 한 가지 일.
- **이름**: `_to_kst` (의도 드러냄), `_is_invalid_close` (질문형), `note` 한국어 메시지 (UI/UX 원칙 2 — 사용자 직접 노출).
- **주석 = Why**: 100ms 옆에 "yfinance 0.5s 보다 관대" 비교, KST 옆에 "pykrx naive datetime" 변환 이유, `adj_close=close_f` 옆에 "MVP 비조정가 사용" 명시 — 향후 split/dividend 보정 시 어디를 손볼지 즉시 알 수 있음.
- **배당 미구현 명시**: 침묵 회피 — `fetch_dividends` 본문에 docstring + INFO 로깅으로 BLOCKER-002 SOFT 사유 명시. 향후 누가 와도 "왜 빈 리스트인가" 를 5초 안에 파악 가능.

## 이슈/블로커

- **BLOCKER-002 [SOFT]**: pykrx 가 ETF 분배금 종합 API 미제공 — 빈 구현으로 진행 (위 등록 완료).
- **수정주가 (adj_close)**: pykrx 의 기본 `get_market_ohlcv` 는 비조정가. MVP 는 close 와 동일 값으로 처리 (split/dividend 보정 미반영). 향후 `adjusted=True` 옵션 또는 `get_market_cap_by_date` 등 별도 호출로 보강 필요. 별도 BLOCKER 등록은 보류 — KR 주식은 split 빈도가 미국보다 낮아 MVP 영향 작다고 판단. 필요 시 retrospective 에서 재논의.

## 다음 제안

1. **TASK-022 (가칭, pyupbit 어댑터)**: 동일 base.py Protocol 을 구현하면 KR/암호화폐 자산 자유 추가 (TASK-031) 가 자연스럽게 확장된다. ticker 형식: `'KRW-BTC'` 등.
2. **자산 메타 매퍼 (TASK-031 직전)**: 자산 추가 UI 가 ticker 만 받으면 어떤 어댑터를 쓸지 모른다. `'069500'` (6자리 숫자) → PykrxSource, `'BTC-USD'` → YfinanceSource, `'KRW-BTC'` → PyupbitSource 같은 라우팅 함수가 필요. domain/data 경계에 두는 것을 권장.
3. **단위 테스트 (TASK-081 확장)**: `_to_kst` 의 naive↔aware 분기, `_is_invalid_close` 한국어 close=0 (휴장일 모킹), `_safe_float` NaN/None 분기를 mock 으로 검증. 네트워크 없이 가능.
4. **수정주가 보강 검토**: KOSPI 우량주 분할 사례가 백테스트에 들어오는 시점에 split-aware adj_close 보강 (별도 미니 태스크). 우선순위는 SAA/DAA MVP 가속을 위해 후순위.
5. **UI 안내 문구 태스크**: BLOCKER-002 의 "KR 자산은 배당 미반영" 안내를 자산 추가 UI 와 백테스트 결과 화면에 표기. 프론트 작업 시작 시점 (TASK-100+) 에서 동시 처리.
