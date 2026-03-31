---
agent: tester
task_id: TASK-005
status: DONE
timestamp: 2026-03-25T14:00:00
---

## 결과 요약
전체 15개 테스트 작성 및 실행 완료. **15 passed, 0 failed** (소요 시간: 1.48초).

### test_database.py (6개 테스트)
| 테스트 | 결과 | 설명 |
|--------|------|------|
| test_init_db_creates_tables | PASSED | exchange_rates, market_indices 테이블 생성 확인 |
| test_init_db_is_idempotent | PASSED | init_db() 중복 호출 시 에러 없음 확인 |
| test_save_exchange_rates | PASSED | 환율 데이터 2건 저장 및 조회 확인 |
| test_save_exchange_rates_empty | PASSED | 빈 리스트 저장 시 0건 확인 |
| test_save_market_indices | PASSED | 세계지수 데이터 2건 저장 및 조회 확인 |
| test_save_market_indices_empty | PASSED | 빈 리스트 저장 시 0건 확인 |

### test_scraper.py (9개 테스트 - 라이브)
| 테스트 | 결과 | 설명 |
|--------|------|------|
| test_fetch_exchange_rates_returns_list | PASSED | list 타입 반환 확인 |
| test_fetch_exchange_rates_non_empty | PASSED | 비어 있지 않은 리스트 반환 확인 |
| test_fetch_exchange_rates_dict_keys | PASSED | dict 키(currency, rate, change_value, change_percent) 확인 |
| test_fetch_exchange_rates_currency_values | PASSED | 통화 코드가 TARGET_CURRENCIES에 속하는지 확인 |
| test_fetch_exchange_rates_rate_positive | PASSED | 환율 값이 양수인지 확인 |
| test_fetch_market_indices_returns_list | PASSED | list 타입 반환 확인 |
| test_fetch_market_indices_non_empty | PASSED | 비어 있지 않은 리스트 반환 확인 |
| test_fetch_market_indices_dict_keys | PASSED | dict 키(index_name, country, value, change_value, change_percent) 확인 |
| test_fetch_market_indices_value_positive | PASSED | 지수 현재값이 양수인지 확인 |

## 변경된 파일
- tests/test_database.py (신규)
- tests/test_scraper.py (신규)

## 이슈/블로커
없음

## 다음 제안
모든 테스트가 통과했으므로 TASK-005를 DONE 처리할 수 있다.
