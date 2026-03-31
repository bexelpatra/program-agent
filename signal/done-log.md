# Done Log

(완료된 태스크가 시간순으로 누적된다. Manager가 태스크를 DONE 처리할 때마다 아래에 추가한다.)

### TASK-001 (DONE) - 2026-03-25T12:05
- title: config.py 작성 (설정 및 상수 정의)
- assignee: coder
- summary: 프로젝트 설정 파일 작성. DB 경로, 크롤링 URL, User-Agent, 타임아웃, 대상 환율/지수 목록 포함.
- files: src/config.py

### TASK-002 (DONE) - 2026-03-25T12:08
- title: database.py 작성 (DB 초기화 및 저장)
- assignee: coder
- summary: aiosqlite 기반 DB 모듈 구현. init_db(), save_exchange_rates(), save_market_indices() 3개 async 함수. architecture.md 스키마 반영.
- files: src/database.py

### TASK-003 (DONE) - 2026-03-25T12:12
- title: scraper.py 작성 (네이버증권 크롤링)
- assignee: coder
- summary: aiohttp+BS4+lxml 비동기 크롤링 구현. 환율(HTML파싱), 세계지수(JS JSON추출), 코스닥(별도페이지). 라이브 테스트 환율4건 지수8건 정상 확인.
- files: src/scraper.py

### TASK-004 (DONE) - 2026-03-25T12:15
- title: main.py 작성 (메인 실행 스크립트)
- assignee: coder
- summary: asyncio.gather로 환율+지수 동시 크롤링, collected_at 추가, DB 저장, 결과 로깅. 라이브 실행 0.27초에 환율4건+지수8건 정상 수집 및 저장 확인.
- files: src/main.py

### TASK-006 (DONE) - 2026-03-25T12:18
- title: cron 설정 (09:30, 15:30)
- assignee: coder
- summary: run_crawler.sh 셸 스크립트 작성. 날짜별 로그 저장, 실행 권한 부여. crontab 등록 명령 안내 포함 (사용자 확인 대기).
- files: src/run_crawler.sh

### TASK-005 (DONE) - 2026-03-25T12:20
- title: 전체 테스트 작성 및 실행
- assignee: tester
- summary: 15개 테스트 전부 통과 (1.48초). DB 테스트 6개(임시DB사용), 스크래퍼 라이브 테스트 9개. 첫 시도 성공.
- files: tests/test_database.py, tests/test_scraper.py
