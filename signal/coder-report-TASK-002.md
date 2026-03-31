# Coder Report — TASK-002

## Status: DONE

## Task
데이터 수집기(collector) 구현

## 작업 내용

`src/collector.py` 생성 완료. 구현 내용:

### 함수 구성
1. **`_normalize_dataframe(df, symbol)`** — yfinance 반환 DataFrame을 DB 스키마(symbol, date, open, high, low, close, adj_close, volume)에 맞게 정규화. MultiIndex 컬럼 처리, 컬럼명 소문자 변환, adj_close 미존재 시 close 대체, NaN 행 제거 포함.

2. **`collect_symbol(db, symbol)`** — 단일 심볼 수집. `db.get_last_date()`로 백필/증분 자동 판단:
   - last_date가 None → `yf.download(period="max")` 백필
   - last_date가 있음 → last_date+1일 ~ 오늘까지 증분 수집
   - 이미 최신이면 0 반환

3. **`collect_all(db=None)`** — `TICKER_SYMBOLS` 전체 순회. 개별 티커 실패 시 `logger.exception()`으로 기록 후 건너뛰기. 결과 딕셔너리 반환 및 요약 로깅.

### 완료 조건 충족 확인
- [x] 백필/증분 자동 판단 로직 포함
- [x] 모든 티커 순회 수집
- [x] database.py의 insert_prices() 사용
- [x] 에러 처리 (개별 티커 실패 시 계속 진행)
- [x] Import 에러 없이 구문 올바름 (ast.parse 및 실제 import 검증 완료)

## 생성된 파일
- `src/collector.py`
