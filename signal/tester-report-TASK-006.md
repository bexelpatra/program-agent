# Tester Report — TASK-006

## Status: DONE

## 테스트 대상
- `src/database.py` — Database 클래스
- `src/collector.py` — collector 모듈 (_normalize_dataframe, collect_symbol, collect_all)

## 작성된 파일
- `tests/__init__.py` — 패키지 초기화
- `tests/test_database.py` — Database 클래스 테스트 (23개)
- `tests/test_collector.py` — collector 모듈 테스트 (15개)

## 테스트 결과
- **총 38개 테스트 / 38개 통과 (100%)**
- 실행 시간: 0.37초

### test_database.py (23개)
| 클래스 | 테스트 수 | 결과 |
|--------|-----------|------|
| TestInitSchema | 4 | ALL PASS |
| TestInsertPrices | 7 | ALL PASS |
| TestSelectPrices | 3 | ALL PASS |
| TestGetLastDate | 3 | ALL PASS |
| TestGetDailyReturns | 3 | ALL PASS |
| TestClose | 3 | ALL PASS |

### test_collector.py (15개)
| 클래스 | 테스트 수 | 결과 |
|--------|-----------|------|
| TestNormalizeDataframe | 7 | ALL PASS |
| TestCollectSymbol | 4 | ALL PASS |
| TestCollectAll | 4 | ALL PASS |

## Mock 사용
- `clickhouse_connect.get_client` — DB 연결 없이 테스트
- `yfinance.download` — 외부 API 호출 없이 테스트
- `Database` 클래스 — collector 테스트에서 mock 사용

## 비고
- `_normalize_dataframe`에서 close 컬럼 없이 입력 시 adj_close 폴백 로직에서 KeyError 발생 가능 (missing columns 체크보다 앞서 실행됨). 기능상 문제는 아니나, 방어적 코딩 관점에서 개선 가능.
