# Done Log

### TASK-001 (DONE) - 2026-04-13T16:01
- title: 알림 동작 검증 스크립트 작성
- assignee: coder
- summary: _test_notify.py 작성. toast/overlay/both 모드별 테스트 가능. memo 필드 포함 샘플 데이터 구성.
- files: projects/starcraft_match_record/_test_notify.py

### TASK-002 (DONE) - 2026-04-13T16:30
- title: player_memos 테이블 추가 (DB 스키마 확장)
- assignee: coder
- summary: db.py에 player_memos 테이블 DDL 추가, 5개 메모 CRUD 메서드(add_memo, get_memos, get_latest_memo, clear_memos, update_memo) 구현.
- files: projects/starcraft_match_record/db.py

### TASK-003 (DONE) - 2026-04-13T16:40
- title: 채팅 메모 명령어 파싱 및 저장 로직 구현
- assignee: coder
- summary: record_manager.py에 _process_chat_memos() 구현. !memo <내용>→저장, !memo clear→삭제. process_replay() 흐름에 통합.
- files: projects/starcraft_match_record/record_manager.py

### TASK-004 (DONE) - 2026-04-13T16:50
- title: 알림에 메모 정보 표시 기능 추가
- assignee: coder
- summary: notifier.py overlay에 메모 행 표시 추가 (노란색, Consolas 8pt). main.py 콜백에서 get_latest_memo() 조회하여 알림에 전달.
- files: projects/starcraft_match_record/notifier.py, projects/starcraft_match_record/main.py

### TASK-005 (DONE) - 2026-04-13T16:50
- title: CLI에 메모 관리 명령어 추가
- assignee: coder
- summary: main.py에 memo 서브커맨드 추가. memo list/add/clear 세 동작 지원. cmd_memo 핸들러 구현.
- files: projects/starcraft_match_record/main.py

### TASK-006 (DONE) - 2026-04-13T17:00
- title: 메모 기능 단위 테스트 작성
- assignee: tester
- summary: 17개 테스트 전체 통과 (DB CRUD 10개 + 채팅 메모 파싱 7개). get_latest_memo 정렬 경미 이슈 발견.
- files: projects/starcraft_match_record/_test_memo.py

### TASK-007 (DONE) - 2026-04-13T17:02
- title: get_latest_memo 정렬 순서 수정
- assignee: coder
- summary: db.py get_latest_memo()의 ORDER BY created_at DESC → ORDER BY id DESC로 변경. 삽입 순서 보장. 테스트 17개 재통과.
- files: projects/starcraft_match_record/db.py

### TASK-008 (DONE) - 2026-04-13T17:20
- title: GUI 설정 화면 구현 (gui.py)
- assignee: coder
- summary: tkinter 기반 GUI 생성. 어두운 테마, 닉네임/경로/알림 설정, 실행/전적 placeholder 버튼, 상태바. config.py API로 저장.
- files: projects/starcraft_match_record/gui.py

### TASK-009 (DONE) - 2026-04-13T17:30
- title: GUI 실행/전적 기능 구현
- assignee: coder
- summary: gui.py에 Launch/Daemon/전적보기/리플레이가져오기 기능 구현. DB/RecordManager 초기화, 스레드 안전 상태바, 버튼 비활성화 처리.
- files: projects/starcraft_match_record/gui.py

### TASK-010 (DONE) - 2026-04-13T17:30
- title: main.py에 gui 서브커맨드 추가
- assignee: coder
- summary: main.py에 gui 서브커맨드 + cmd_gui 핸들러 추가. lazy import로 tkinter 미설치 환경 호환.
- files: projects/starcraft_match_record/main.py
