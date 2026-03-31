# Task Board

| ID | Title | Assignee | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|--------|----------|------------|---------|---------|
| TASK-001 | 프로젝트 초기화 (docker-compose, requirements, config, ES 클라이언트) | coder | DONE | HIGH | - | 2026-03-25T18:00 | 2026-03-25T18:05 |
| TASK-002 | 데이터 모델 + ES 인덱스 매핑 생성 | coder | DONE | HIGH | TASK-001 | 2026-03-25T18:00 | 2026-03-25T18:10 |
| TASK-003 | YAML 로더 + CLI 기본 커맨드 (load, study, search, relations) | coder | DONE | HIGH | TASK-002 | 2026-03-25T18:00 | 2026-03-25T18:15 |
| TASK-004 | 인프라 테스트 (ES 연결, 인덱스 생성, 로더, 검색) | tester | DONE | HIGH | TASK-003 | 2026-03-25T18:00 | 2026-03-25T18:25 |
| TASK-005 | 서양윤리 데이터 입력 1차 (소크라테스) | coder | DONE | HIGH | TASK-003 | 2026-03-25T18:00 | 2026-03-25T18:25 |
| TASK-006 | 서양윤리 데이터 검증 1차 (소크라테스) | tester | DONE | HIGH | TASK-005 | 2026-03-25T18:00 | 2026-03-26T10:00 |
| TASK-007 | 소크라테스 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-006 | 2026-03-26T10:00 | 2026-03-26T10:05 |
| TASK-008 | exporter.py 구현 (ES → YAML export) | coder | DONE | HIGH | TASK-003 | 2026-03-26T10:10 | 2026-03-26T10:15 |
| TASK-009 | 소크라테스 수정 데이터 ES 적재 + export 검증 | coder | DONE | HIGH | TASK-007,TASK-008 | 2026-03-26T10:10 | 2026-03-26T10:20 |
| TASK-010 | claims 스키마 보강 + 소크라테스 argument/counterpoint 추가 | coder | DONE | HIGH | TASK-009 | 2026-03-26T10:30 | 2026-03-26T10:40 |
| TASK-011 | 소크라테스 argument/counterpoint 품질 개선 | coder | DONE | HIGH | TASK-010 | 2026-03-26T11:00 | 2026-03-26T11:10 |
| TASK-012 | 플라톤 데이터 입력 (ES 직접) | coder | DONE | HIGH | TASK-009 | 2026-03-26T11:30 | 2026-03-26T11:35 |
| TASK-013 | 플라톤 데이터 검증 | tester | DONE | HIGH | TASK-012 | 2026-03-26T11:35 | 2026-03-26T11:45 |
| TASK-014 | 플라톤 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-013 | 2026-03-26T11:45 | 2026-03-26T11:50 |
| TASK-015 | 아리스토텔레스 데이터 입력 (ES 직접) | coder | DONE | HIGH | TASK-009 | 2026-03-26T12:00 | 2026-03-26T12:10 |
| TASK-016 | 아리스토텔레스 데이터 검증 | tester | DONE | HIGH | TASK-015 | 2026-03-26T12:10 | 2026-03-26T12:20 |
| TASK-017 | 아리스토텔레스 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-016 | 2026-03-26T12:20 | 2026-03-26T12:25 |
| TASK-018 | 아우구스티누스 데이터 입력 (ES 직접) | coder | DONE | HIGH | TASK-009 | 2026-03-26T12:30 | 2026-03-26T12:35 |
| TASK-019 | 아우구스티누스 데이터 검증 | tester | DONE | HIGH | TASK-018 | 2026-03-26T12:35 | 2026-03-26T12:40 |
| TASK-020 | 아우구스티누스 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-019 | 2026-03-26T12:40 | 2026-03-26T12:45 |
| TASK-021 | 토마스 아퀴나스 데이터 입력 (ES 직접) | coder | DONE | HIGH | TASK-009 | 2026-03-26T13:00 | 2026-03-26T13:05 |
| TASK-022 | 토마스 아퀴나스 데이터 검증 | tester | DONE | HIGH | TASK-021 | 2026-03-26T13:05 | 2026-03-26T13:10 |
| TASK-023 | 토마스 아퀴나스 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-022 | 2026-03-26T13:10 | 2026-03-26T13:15 |
| TASK-024 | 칸트 데이터 입력 (ES 직접) | coder | DONE | HIGH | TASK-009 | 2026-03-26T13:20 | 2026-03-26T13:40 |
| TASK-025 | 칸트 데이터 검증 | tester | DONE | HIGH | TASK-027 | 2026-03-26T13:40 | 2026-03-30T00:10 |
| TASK-028 | 칸트 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-025 | 2026-03-30T00:10 | 2026-03-30T00:15 |
| TASK-026 | original_text_ko 필드 스키마 추가 (models.py + architecture.md) | coder | DONE | HIGH | - | 2026-03-30T00:00 | 2026-03-30T00:01 |
| TASK-027 | 칸트 claims 한국어 번역 추가 (ES update) | coder | DONE | HIGH | TASK-026 | 2026-03-30T00:00 | 2026-03-30T00:05 |
