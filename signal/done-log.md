# Done Log

(완료된 태스크가 시간순으로 누적된다. Manager가 태스크를 DONE 처리할 때마다 아래에 추가한다.)

### TASK-001 (DONE) - 2026-03-25T16:50
- title: 프로젝트 초기화 및 config/database 모듈 구현
- assignee: coder
- summary: requirements.txt, src/__init__.py, src/config.py, src/database.py 작성. ClickHouse ReplacingMergeTree 스키마, MV, 일간수익률 쿼리, 증분수집용 마지막날짜 조회 구현 완료.
- files: requirements.txt, src/__init__.py, src/config.py, src/database.py, logs/

### TASK-002 (DONE) - 2026-03-25T16:55
- title: 데이터 수집기(collector) 구현
- assignee: coder
- summary: src/collector.py 구현. 백필/증분 자동 판단, yfinance DataFrame 정규화, 개별 티커 에러 시 건너뛰기, 전체 수집 요약 로깅.
- files: src/collector.py

### TASK-003 (DONE) - 2026-03-25T16:55
- title: 분석 프레임워크 및 전략 플러그인 구현
- assignee: coder
- summary: analyzer 플러그인 구조 구현. BaseStrategy/Signal/SignalType 정의, StrategyRegistry, STL 계절성 분해, 이동평균 크로스오버(BUY/SELL 시그널), 상관관계 분석 전략 3종.
- files: src/analyzer/__init__.py, src/analyzer/base.py, src/analyzer/seasonality.py, src/analyzer/moving_average.py, src/analyzer/correlation.py

### TASK-004 (DONE) - 2026-03-25T17:00
- title: 백테스팅 엔진 구현
- assignee: coder
- summary: src/backtester.py 구현. Signal weight 반영 포지션 크기, 수수료/슬리피지 적용, 성과 지표 7종(total_return, CAGR, MDD, Sharpe, 승률, P/L비율, 거래횟수), Buy&Hold 벤치마크 비교, 텍스트 리포트.
- files: src/backtester.py

### TASK-005 (DONE) - 2026-03-25T17:10
- title: 엔트리포인트 및 cron 스크립트 구현
- assignee: coder
- summary: src/run_collector.py (cron용), src/run_analyzer.py (CLI: analyze/backtest/list 서브커맨드), run_collector.sh (셸 스크립트) 구현 완료.
- files: src/run_collector.py, src/run_analyzer.py, run_collector.sh

### TASK-006 (DONE) - 2026-03-25T17:10
- title: database + collector 테스트
- assignee: tester
- summary: test_database.py 23개, test_collector.py 15개 = 38개 테스트 전체 통과. _normalize_dataframe 방어적 코딩 개선 제안 있음.
- files: tests/__init__.py, tests/test_database.py, tests/test_collector.py

### TASK-007 (DONE) - 2026-03-25T17:10
- title: 분석 전략 + 백테스터 테스트
- assignee: tester
- summary: test_strategies.py 23개, test_backtester.py 24개 = 47개 테스트 전체 통과. 상관관계 테스트 fixture 데이터 조정으로 해결.
- files: tests/test_strategies.py, tests/test_backtester.py
