# Architecture

## 개요
네이버증권에서 주요 금융 지표(환율, 세계 주요 지수)를 크롤링하여 SQLite DB에 저장하는 Python 프로그램.
매일 09:30, 15:30에 cron으로 자동 실행된다.

### 기술 스택
- Python 3.11
- aiohttp + BeautifulSoup4 + lxml (비동기 고성능 크롤링)
- aiosqlite (비동기 DB)
- SQLite3 (경량 로컬 DB)
- cron (스케줄링)

### 크롤링 대상
1. **환율** — `https://finance.naver.com/marketindex/`
   - USD/KRW, EUR/KRW, JPY/KRW, CNY/KRW 등 주요 통화
2. **세계 지수** — `https://finance.naver.com/world/`
   - 코스피, 코스닥, 나스닥, S&P500, 다우존스, 니케이225, 상해종합, 항셍 등

## 구조

```
src/
├── config.py        # 설정 (DB 경로, 크롤링 URL, 대상 목록)
├── database.py      # DB 초기화, 저장 (aiosqlite)
├── scraper.py       # 네이버증권 크롤링 (aiohttp + BS4)
└── main.py          # 메인 진입점 (비동기 실행)
tests/
├── test_scraper.py  # 크롤링 테스트
└── test_database.py # DB 테스트
```

### DB 스키마

**exchange_rates 테이블**
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER PK | 자동증가 |
| currency | TEXT | 통화 코드 (USD, EUR 등) |
| rate | REAL | 환율 |
| change_value | REAL | 변동값 |
| change_percent | REAL | 변동률(%) |
| collected_at | TEXT | 수집 시각 (ISO 8601) |

**market_indices 테이블**
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER PK | 자동증가 |
| index_name | TEXT | 지수명 (KOSPI, NASDAQ 등) |
| country | TEXT | 국가 |
| value | REAL | 현재값 |
| change_value | REAL | 변동값 |
| change_percent | REAL | 변동률(%) |
| collected_at | TEXT | 수집 시각 (ISO 8601) |

## 설계 결정

### 비동기 I/O 사용
- 결정: aiohttp + aiosqlite로 비동기 처리
- 이유: 환율/지수 페이지를 동시에 크롤링하여 속도 극대화
- 대안: requests (동기) — 순차 처리로 느림

### SQLite 사용
- 결정: SQLite를 로컬 DB로 사용
- 이유: 별도 서버 불필요, 파일 기반으로 간단, 일일 2회 수집에 충분
- 대안: PostgreSQL — 이 규모에서는 과도함

### lxml 파서 사용
- 결정: BeautifulSoup에 lxml 파서 적용
- 이유: html.parser 대비 파싱 속도 5-10배 빠름

## 현재 상태
설계 완료 — 태스크 분해 및 구현 단계 진입
