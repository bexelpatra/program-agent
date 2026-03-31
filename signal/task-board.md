# Task Board

| ID | Title | Assignee | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|--------|----------|------------|---------|---------|
| TASK-001 | config.py 작성 (설정 및 상수 정의) | coder | DONE | HIGH | - | 2026-03-25T12:00 | 2026-03-25T12:05 |
| TASK-002 | database.py 작성 (DB 초기화 및 저장) | coder | DONE | HIGH | TASK-001 | 2026-03-25T12:00 | 2026-03-25T12:08 |
| TASK-003 | scraper.py 작성 (네이버증권 크롤링) | coder | DONE | HIGH | TASK-001 | 2026-03-25T12:00 | 2026-03-25T12:12 |
| TASK-004 | main.py 작성 (메인 실행 스크립트) | coder | DONE | HIGH | TASK-002, TASK-003 | 2026-03-25T12:00 | 2026-03-25T12:15 |
| TASK-005 | 전체 테스트 작성 및 실행 | tester | DONE | HIGH | TASK-004 | 2026-03-25T12:00 | 2026-03-25T12:20 |
| TASK-006 | cron 설정 (09:30, 15:30) | coder | DONE | MEDIUM | TASK-004 | 2026-03-25T12:00 | 2026-03-25T12:18 |
