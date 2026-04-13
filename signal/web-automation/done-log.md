# Done Log

### TASK-001 (DONE) - 2026-04-13T20:35
- title: 프로젝트 초기화 (requirements.txt, 디렉토리 구조, config 템플릿)
- assignee: coder
- summary: 12개 파일 생성. requirements.txt, config YAML 3개(settings/tistory/yanolja), 전체 디렉토리 구조 + __init__.py 완료.
- files: requirements.txt, config/settings.yaml, config/tistory.yaml, config/yanolja.yaml, src/__init__.py 외 7개 __init__.py

### TASK-003 (DONE) - 2026-04-13T20:40
- title: Core - config.py (YAML 설정 로더)
- assignee: coder
- summary: Config 클래스 구현. YAML 로드, 사이트별 병합, 점 표기법 접근, 환경변수 오버라이드(WA_ 접두사), 자동 타입 캐스팅 지원.
- files: src/core/config.py

### TASK-002 (DONE) - 2026-04-13T20:50
- title: Core - browser.py (Playwright 브라우저 엔진)
- assignee: coder
- summary: BrowserManager 클래스 구현. async context manager, start/stop/goto/wait_for/click/fill/screenshot/get_page. Config에서 브라우저 설정 로드.
- files: src/core/browser.py

### TASK-004 (DONE) - 2026-04-13T20:50
- title: Core - telegram.py (텔레그램 봇 알림)
- assignee: coder
- summary: TelegramNotifier 클래스 구현. send_message/send_photo/send_alert. enabled=false 시 no-op, 실패 시 예외 없이 로깅만.
- files: src/core/telegram.py

### TASK-005 (DONE) - 2026-04-13T20:50
- title: Core - logger.py (로깅 + 단계별 스크린샷)
- assignee: coder
- summary: setup_logger/get_logger 구현. 파일+콘솔 핸들러, 디렉토리 자동 생성, 포맷: [날짜] [레벨] [모듈] 메시지.
- files: src/core/logger.py

### TASK-006 (DONE) - 2026-04-13T20:50
- title: Core - retry.py (재시도 데코레이터)
- assignee: coder
- summary: retry/async_retry 데코레이터 구현. 지수 백오프, 예외 타입 필터, Config에서 기본값 로드.
- files: src/core/retry.py
