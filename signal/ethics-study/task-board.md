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
| TASK-026 | original_text_ko 필드 스키마 추가 (models.py + architecture.md) | coder | DONE | HIGH | - | 2026-03-30T00:00 | 2026-03-30T00:01 |
| TASK-027 | 칸트 claims 한국어 번역 추가 (ES update) | coder | DONE | HIGH | TASK-026 | 2026-03-30T00:00 | 2026-03-30T00:05 |
| TASK-028 | 칸트 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-025 | 2026-03-30T00:10 | 2026-03-30T00:15 |
| TASK-029 | 벤담 데이터 입력 (ES 직접) | coder | DONE | HIGH | - | 2026-04-10T00:00 | 2026-04-10T00:00 |
| TASK-030 | 벤담 데이터 검증 | tester | DONE | HIGH | TASK-029 | 2026-04-10T00:00 | 2026-04-10T00:00 |
| TASK-031 | 벤담 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-030 | 2026-04-10T00:00 | 2026-04-11T00:00 |
| TASK-032 | 밀 데이터 입력 (ES 직접) | coder | DONE | HIGH | TASK-029 | 2026-04-10T00:00 | 2026-04-11T00:00 |
| TASK-033 | 밀 데이터 검증 | tester | DONE | HIGH | TASK-032 | 2026-04-10T00:00 | 2026-04-11T00:00 |
| TASK-034 | 밀 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-033 | 2026-04-10T00:00 | 2026-04-11T13:00 |
| TASK-035 | 흄 데이터 입력 (ES 직접) | coder | DONE | HIGH | TASK-029 | 2026-04-10T00:00 | 2026-04-12T00:00 |
| TASK-036 | 흄 데이터 검증 | tester | DONE | HIGH | TASK-035 | 2026-04-10T00:00 | 2026-04-12T00:00 |
| TASK-037 | 흄 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-036 | 2026-04-10T00:00 | 2026-04-12T00:00 |
| TASK-038 | 에피쿠로스 데이터 입력 (ES 직접) | coder | DONE | MEDIUM | - | 2026-04-12T00:00 | 2026-04-12T00:00 |
| TASK-039 | 에피쿠로스 데이터 검증 | tester | DONE | MEDIUM | TASK-038 | 2026-04-12T00:00 | 2026-04-12T00:00 |
| TASK-040 | 에피쿠로스 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-039 | 2026-04-12T00:00 | 2026-04-12T00:00 |
| TASK-041 | 스토아학파 데이터 입력 (에픽테토스·마르쿠스 아우렐리우스·세네카, ES 직접) | coder | DONE | MEDIUM | - | 2026-04-12T00:00 | 2026-04-13T16:30 |
| TASK-042 | 스토아학파 데이터 검증 | tester | DONE | MEDIUM | TASK-041 | 2026-04-12T00:00 | 2026-04-13T17:45 |
| TASK-043 | 스토아학파 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-042 | 2026-04-12T00:00 | 2026-04-13T18:30 |
| TASK-044 | 스피노자 데이터 입력 (ES 직접) | coder | DONE | MEDIUM | - | 2026-04-12T00:00 | 2026-04-13T18:15 |
| TASK-045 | 스피노자 데이터 검증 | tester | DONE | MEDIUM | TASK-044 | 2026-04-12T00:00 | 2026-04-13T19:00 |
| TASK-046 | 스피노자 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-045 | 2026-04-12T00:00 | 2026-04-13T19:30 |
| TASK-047 | 헤겔 데이터 입력 (ES 직접) | coder | DONE | MEDIUM | - | 2026-04-12T00:00 | 2026-04-13T20:00 |
| TASK-048 | 헤겔 데이터 검증 | tester | DONE | MEDIUM | TASK-047 | 2026-04-12T00:00 | 2026-04-13T20:30 |
| TASK-049 | 헤겔 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-048 | 2026-04-12T00:00 | 2026-04-13T21:00 |
| TASK-050 | 니체 데이터 입력 (ES 직접) | coder | DONE | MEDIUM | - | 2026-04-12T00:00 | 2026-04-13T22:35 |
| TASK-051 | 니체 데이터 검증 | tester | DONE | MEDIUM | TASK-050 | 2026-04-12T00:00 | 2026-04-13T22:50 |
| TASK-052 | 니체 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-051 | 2026-04-12T00:00 | 2026-04-13T23:05 |
| TASK-053 | 사르트르 데이터 입력 (ES 직접) | coder | DONE | MEDIUM | - | 2026-04-12T00:00 | 2026-04-13T21:00 |
| TASK-054 | 사르트르 데이터 검증 | tester | DONE | MEDIUM | TASK-053 | 2026-04-12T00:00 | 2026-04-13T21:15 |
| TASK-055 | 사르트르 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-054 | 2026-04-12T00:00 | 2026-04-13T21:30 |
| --- | **Phase 2: 동양윤리** | --- | --- | --- | --- | --- | --- |
| TASK-056 | 공자 데이터 입력 (ES 직접) | coder | DONE | HIGH | - | 2026-04-13T14:00 | 2026-04-13T15:30 |
| TASK-057 | 공자 데이터 검증 | tester | DONE | HIGH | TASK-056 | 2026-04-13T14:00 | 2026-04-13T17:30 |
| TASK-058 | 공자 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-057 | 2026-04-13T14:00 | 2026-04-13T18:30 |
| TASK-059 | 맹자 데이터 입력 (ES 직접) | coder | DONE | HIGH | - | 2026-04-13T14:00 | 2026-04-13T19:00 |
| TASK-060 | 맹자 데이터 검증 | tester | DONE | HIGH | TASK-059 | 2026-04-13T14:00 | 2026-04-13T19:45 |
| TASK-061 | 맹자 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-060 | 2026-04-13T14:00 | 2026-04-13T20:15 |
| TASK-062 | 순자 데이터 입력 (ES 직접) | coder | DONE | HIGH | - | 2026-04-13T14:00 | 2026-04-13T20:15 |
| TASK-063 | 순자 데이터 검증 | tester | DONE | HIGH | TASK-062 | 2026-04-13T14:00 | 2026-04-13T20:50 |
| TASK-064 | 순자 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-063 | 2026-04-13T14:00 | 2026-04-13T21:10 |
| TASK-065 | 노자 데이터 입력 (ES 직접) | coder | DONE | HIGH | - | 2026-04-13T14:00 | 2026-04-13T21:20 |
| TASK-066 | 노자 데이터 검증 | tester | DONE | HIGH | TASK-065 | 2026-04-13T14:00 | 2026-04-13T21:45 |
| TASK-067 | 노자 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-066 | 2026-04-13T14:00 | 2026-04-13T22:00 |
| TASK-068 | 장자 데이터 입력 (ES 직접) | coder | DONE | MEDIUM | - | 2026-04-13T14:00 | 2026-04-13T22:10 |
| TASK-069 | 장자 데이터 검증 | tester | DONE | MEDIUM | TASK-068 | 2026-04-13T14:00 | 2026-04-13T22:35 |
| TASK-070 | 장자 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-069 | 2026-04-13T14:00 | 2026-04-13T22:45 |
| TASK-071 | 주희(주자) 데이터 입력 (ES 직접) | coder | DONE | HIGH | - | 2026-04-13T14:00 | 2026-04-13T23:05 |
| TASK-072 | 주희 데이터 검증 | tester | DONE | HIGH | TASK-071 | 2026-04-13T14:00 | 2026-04-13T23:05 |
| TASK-073 | 주희 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-072 | 2026-04-13T14:00 | 2026-04-13T21:00 |
| TASK-074 | 왕양명 데이터 입력 (ES 직접) | coder | DONE | MEDIUM | - | 2026-04-13T14:00 | 2026-04-13T21:00 |
| TASK-075 | 왕양명 데이터 검증 | tester | DONE | MEDIUM | TASK-074 | 2026-04-13T14:00 | 2026-04-13T21:15 |
| TASK-076 | 왕양명 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-075 | 2026-04-13T14:00 | 2026-04-13T21:30 |
| TASK-077 | 이황(퇴계) 데이터 입력 (ES 직접) | coder | DONE | HIGH | - | 2026-04-13T14:00 | 2026-04-13T21:00 |
| TASK-078 | 이황 데이터 검증 | tester | DONE | HIGH | TASK-077 | 2026-04-13T14:00 | 2026-04-13T21:15 |
| TASK-079 | 이황 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-078 | 2026-04-13T14:00 | 2026-04-13T21:30 |
| TASK-080 | 이이(율곡) 데이터 입력 (ES 직접) | coder | DONE | HIGH | - | 2026-04-13T14:00 | 2026-04-13T21:15 |
| TASK-081 | 이이 데이터 검증 | tester | DONE | HIGH | TASK-080 | 2026-04-13T14:00 | 2026-04-13T21:40 |
| TASK-082 | 이이 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-081 | 2026-04-13T14:00 | 2026-04-13T21:50 |
| TASK-083 | 정약용(다산) 데이터 입력 (ES 직접) | coder | DONE | MEDIUM | - | 2026-04-13T14:00 | 2026-04-13T21:30 |
| TASK-084 | 정약용 데이터 검증 | tester | DONE | MEDIUM | TASK-083 | 2026-04-13T14:00 | 2026-04-13T21:40 |
| TASK-085 | 정약용 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-084 | 2026-04-13T14:00 | 2026-04-13T21:50 |
| TASK-086 | 붓다(석가모니) 데이터 입력 (ES 직접) | coder | DONE | MEDIUM | - | 2026-04-13T14:00 | 2026-04-13T21:40 |
| TASK-087 | 붓다 데이터 검증 | tester | DONE | MEDIUM | TASK-086 | 2026-04-13T14:00 | 2026-04-13T14:00 |
| TASK-088 | 붓다 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-087 | 2026-04-13T14:00 | 2026-04-13T14:00 |
| TASK-089 | 원효/혜능 데이터 입력 (ES 직접) | coder | DONE | LOW | - | 2026-04-13T14:00 | 2026-04-13T21:50 |
| TASK-090 | 원효/혜능 데이터 검증 | tester | DONE | LOW | TASK-089 | 2026-04-13T14:00 | 2026-04-13T21:50 |
| TASK-091 | 원효/혜능 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | LOW | TASK-090 | 2026-04-13T14:00 | 2026-04-13T22:00 |
| TASK-092 | 묵자 데이터 입력 (ES 직접) | coder | DONE | LOW | - | 2026-04-13T14:00 | 2026-04-13T21:50 |
| TASK-093 | 묵자 데이터 검증 | tester | DONE | LOW | TASK-092 | 2026-04-13T14:00 | 2026-04-13T14:00 |
| TASK-094 | 묵자 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | LOW | TASK-093 | 2026-04-13T14:00 | 2026-04-13T14:00 |
| TASK-095 | 한비자 데이터 입력 (ES 직접) | coder | DONE | LOW | - | 2026-04-13T14:00 | 2026-04-13T21:50 |
| TASK-096 | 한비자 데이터 검증 | tester | DONE | LOW | TASK-095 | 2026-04-13T14:00 | 2026-04-13T21:50 |
| TASK-097 | 한비자 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | LOW | TASK-096 | 2026-04-13T14:00 | 2026-04-13T22:00 |
| --- | **Phase 3: 정치철학/사회사상** | --- | --- | --- | --- | --- | --- |
| TASK-098 | 홉스 데이터 입력 (ES 직접) | coder | DONE | HIGH | - | 2026-04-13T14:00 | 2026-04-13T16:00 |
| TASK-099 | 홉스 데이터 검증 | tester | DONE | HIGH | TASK-098 | 2026-04-13T14:00 | 2026-04-13T18:00 |
| TASK-100 | 홉스 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-099 | 2026-04-13T14:00 | 2026-04-13T18:15 |
| TASK-101 | 로크 데이터 입력 (ES 직접) | coder | DONE | HIGH | - | 2026-04-13T14:00 | 2026-04-13T18:45 |
| TASK-102 | 로크 데이터 검증 | tester | DONE | HIGH | TASK-101 | 2026-04-13T14:00 | 2026-04-13T19:00 |
| TASK-103 | 로크 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-102 | 2026-04-13T14:00 | 2026-04-13T19:30 |
| TASK-104 | 루소 데이터 입력 (ES 직접) | coder | DONE | HIGH | - | 2026-04-13T14:00 | 2026-04-13T20:45 |
| TASK-105 | 루소 데이터 검증 | tester | DONE | HIGH | TASK-104 | 2026-04-13T14:00 | 2026-04-13T21:30 |
| TASK-106 | 루소 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-105 | 2026-04-13T14:00 | 2026-04-13T21:35 |
| TASK-107 | 롤스 데이터 입력 (ES 직접) | coder | DONE | HIGH | - | 2026-04-13T14:00 | 2026-04-13T21:50 |
| TASK-108 | 롤스 데이터 검증 | tester | DONE | HIGH | TASK-107 | 2026-04-13T14:00 | 2026-04-13T22:20 |
| TASK-109 | 롤스 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-108 | 2026-04-13T14:00 | 2026-04-13T22:30 |
| TASK-110 | 노직 데이터 입력 (ES 직접) | coder | DONE | MEDIUM | - | 2026-04-13T14:00 | 2026-04-13T23:00 |
| TASK-111 | 노직 데이터 검증 | tester | DONE | MEDIUM | TASK-110 | 2026-04-13T14:00 | 2026-04-13T23:00 |
| TASK-112 | 노직 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-111 | 2026-04-13T14:00 | 2026-04-13T21:00 |
| TASK-113 | 매킨타이어 데이터 입력 (ES 직접) | coder | DONE | MEDIUM | - | 2026-04-13T14:00 | 2026-04-13T21:15 |
| TASK-114 | 매킨타이어 데이터 검증 | tester | DONE | MEDIUM | TASK-113 | 2026-04-13T14:00 | 2026-04-13T14:00 |
| TASK-115 | 매킨타이어 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-114 | 2026-04-13T14:00 | 2026-04-13T14:00 |
| TASK-116 | 샌델 데이터 입력 (ES 직접) | coder | DONE | MEDIUM | - | 2026-04-13T14:00 | 2026-04-13T21:30 |
| TASK-117 | 샌델 데이터 검증 | tester | DONE | MEDIUM | TASK-116 | 2026-04-13T14:00 | 2026-04-13T21:40 |
| TASK-118 | 샌델 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-117 | 2026-04-13T14:00 | 2026-04-13T21:50 |
| TASK-119 | 하버마스 데이터 입력 (ES 직접) | coder | DONE | MEDIUM | - | 2026-04-13T14:00 | 2026-04-13T21:40 |
| TASK-120 | 하버마스 데이터 검증 | tester | DONE | MEDIUM | TASK-119 | 2026-04-13T14:00 | 2026-04-13T21:50 |
| TASK-121 | 하버마스 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-120 | 2026-04-13T14:00 | 2026-04-13T22:00 |
| TASK-122 | 왈처 데이터 입력 (ES 직접) | coder | DONE | LOW | - | 2026-04-13T14:00 | 2026-04-13T21:50 |
| TASK-123 | 왈처 데이터 검증 | tester | DONE | LOW | TASK-122 | 2026-04-13T14:00 | 2026-04-13T14:00 |
| TASK-124 | 왈처 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | LOW | TASK-123 | 2026-04-13T14:00 | 2026-04-13T14:00 |
| TASK-125 | 테일러 데이터 입력 (ES 직접) | coder | DONE | LOW | - | 2026-04-13T14:00 | 2026-04-13T21:50 |
| TASK-126 | 테일러 데이터 검증 | tester | DONE | LOW | TASK-125 | 2026-04-13T14:00 | 2026-04-13T14:00 |
| TASK-127 | 테일러 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | LOW | TASK-126 | 2026-04-13T14:00 | 2026-04-13T14:00 |
| --- | **Web UI: 검색/조회 인터페이스** | --- | --- | --- | --- | --- | --- |
| TASK-128 | FastAPI 앱 기본 구조 + 메인 페이지 (사상가 목록, 분야별 탭) | coder | DONE | HIGH | - | 2026-04-13T23:30 | 2026-04-14T00:00 |
| TASK-129 | 사상가 상세 페이지 (저작, 주장, 키워드, 관계) | coder | DONE | HIGH | TASK-128 | 2026-04-13T23:30 | 2026-04-14T00:15 |
| TASK-130 | 통합 검색 기능 (claims + keywords + works 전문 검색) | coder | DONE | HIGH | TASK-128 | 2026-04-13T23:30 | 2026-04-14T00:15 |
| TASK-131 | 웹 UI 통합 테스트 (전 페이지 기능 검증 + 원격 접근) | tester | DONE | HIGH | TASK-129,TASK-130 | 2026-04-13T23:30 | 2026-04-14T00:30 |
| TASK-132 | 웹 UI 이슈 수정 (테스트 결과 반영) | coder | DONE | HIGH | TASK-131 | 2026-04-13T23:30 | 2026-04-14T00:45 |
| --- | **Phase 4: 도덕교육론/도덕심리학** | --- | --- | --- | --- | --- | --- |
| TASK-133 | 피아제 데이터 입력 (ES 직접) — 도덕발달 핵심, claims 12+ | coder | DONE | HIGH | - | 2026-04-14T10:00 | 2026-04-14T14:00 |
| TASK-134 | 피아제 데이터 검증 | tester | DONE | HIGH | TASK-133 | 2026-04-14T10:00 | 2026-04-14T14:30 |
| TASK-135 | 피아제 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-134 | 2026-04-14T10:00 | 2026-04-14T14:35 |
| TASK-136 | 콜버그 데이터 입력 (ES 직접) — 도덕발달 핵심, claims 15+ | coder | DONE | HIGH | - | 2026-04-14T10:00 | 2026-04-14T14:30 |
| TASK-137 | 콜버그 데이터 검증 | tester | DONE | HIGH | TASK-136 | 2026-04-14T10:00 | 2026-04-14T15:00 |
| TASK-138 | 콜버그 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | HIGH | TASK-137 | 2026-04-14T10:00 | 2026-04-14T15:00 |
| TASK-139 | 길리건 데이터 입력 (ES 직접) — 배려윤리, claims 10+ | coder | DONE | MEDIUM | - | 2026-04-14T10:00 | 2026-04-14T15:00 |
| TASK-140 | 길리건 데이터 검증 | tester | DONE | MEDIUM | TASK-139 | 2026-04-14T10:00 | 2026-04-14T15:20 |
| TASK-141 | 길리건 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-140 | 2026-04-14T10:00 | 2026-04-14T15:20 |
| TASK-142 | 나딩스 데이터 입력 (ES 직접) — 배려윤리, claims 10+ | coder | DONE | MEDIUM | - | 2026-04-14T10:00 | 2026-04-14T15:00 |
| TASK-143 | 나딩스 데이터 검증 | tester | DONE | MEDIUM | TASK-142 | 2026-04-14T10:00 | 2026-04-14T15:20 |
| TASK-144 | 나딩스 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-143 | 2026-04-14T10:00 | 2026-04-14T15:20 |
| TASK-145 | 래스 데이터 입력 (ES 직접) — 가치명료화, claims 8+ | coder | DONE | MEDIUM | - | 2026-04-14T10:00 | 2026-04-14T15:20 |
| TASK-146 | 래스 데이터 검증 | tester | DONE | MEDIUM | TASK-145 | 2026-04-14T10:00 | 2026-04-14T15:35 |
| TASK-147 | 래스 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-146 | 2026-04-14T10:00 | 2026-04-14T15:35 |
| TASK-148 | 리코나 데이터 입력 (ES 직접) — 인격교육, claims 8+ | coder | DONE | MEDIUM | - | 2026-04-14T10:00 | 2026-04-14T15:20 |
| TASK-149 | 리코나 데이터 검증 | tester | DONE | MEDIUM | TASK-148 | 2026-04-14T10:00 | 2026-04-14T15:35 |
| TASK-150 | 리코나 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-149 | 2026-04-14T10:00 | 2026-04-14T15:35 |
| TASK-151 | 하이트 데이터 입력 (ES 직접) — 도덕심리학, claims 8+ | coder | DONE | MEDIUM | - | 2026-04-14T10:00 | 2026-04-14T15:35 |
| TASK-152 | 하이트 데이터 검증 | tester | DONE | MEDIUM | TASK-151 | 2026-04-14T10:00 | 2026-04-14T15:45 |
| TASK-153 | 하이트 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-152 | 2026-04-14T10:00 | 2026-04-14T15:45 |
| TASK-154 | 레스트 데이터 입력 (ES 직접) — 도덕심리학, claims 8+ | coder | DONE | MEDIUM | - | 2026-04-14T10:00 | 2026-04-14T15:35 |
| TASK-155 | 레스트 데이터 검증 | tester | DONE | MEDIUM | TASK-154 | 2026-04-14T10:00 | 2026-04-14T15:45 |
| TASK-156 | 레스트 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-155 | 2026-04-14T10:00 | 2026-04-14T15:45 |
| --- | **Phase 5: 통일교육/시민윤리 (C안: 인물 중심)** | --- | --- | --- | --- | --- | --- |
| TASK-157 | 갈퉁 데이터 입력 (ES 직접) — field=peace_studies, claims 6~8 (적극적 평화, 구조적 폭력 등) | coder | DONE | MEDIUM | TASK-172 | 2026-04-15T00:00 | 2026-04-15T15:30 |
| TASK-158 | 갈퉁 데이터 검증 | tester | DONE | MEDIUM | TASK-157 | 2026-04-15T00:00 | 2026-04-15T00:00 |
| TASK-159 | 갈퉁 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-158 | 2026-04-15T00:00 | 2026-04-15T00:00 |
| TASK-160 | 백낙청 데이터 입력 (ES 직접) — field=unification_edu, claims 6~8 (분단체제론, 변혁적 중도주의 등) | coder | DONE | MEDIUM | TASK-172 | 2026-04-15T00:00 | 2026-04-15T15:30 |
| TASK-161 | 백낙청 데이터 검증 | tester | DONE | MEDIUM | TASK-160 | 2026-04-15T00:00 | 2026-04-15T00:00 |
| TASK-162 | 백낙청 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-161 | 2026-04-15T00:00 | 2026-04-15T00:00 |
| TASK-163 | 강만길 데이터 입력 (ES 직접) — field=unification_edu, claims 6~8 (통일지향 역사학, 분단시대 사학 등) | coder | DONE | MEDIUM | TASK-172 | 2026-04-15T00:00 | 2026-04-15T15:30 |
| TASK-164 | 강만길 데이터 검증 | tester | DONE | MEDIUM | TASK-163 | 2026-04-15T00:00 | 2026-04-15T00:00 |
| TASK-165 | 강만길 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-164 | 2026-04-15T00:00 | 2026-04-15T00:00 |
| TASK-166 | 듀이 데이터 입력 (ES 직접) — field=civic_edu, claims 8~10 (민주주의와 교육, 경험·반성·탐구 등) | coder | DONE | MEDIUM | TASK-172 | 2026-04-15T00:00 | 2026-04-15T15:30 |
| TASK-167 | 듀이 데이터 검증 | tester | DONE | MEDIUM | TASK-166 | 2026-04-15T00:00 | 2026-04-15T00:00 |
| TASK-168 | 듀이 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-167 | 2026-04-15T00:00 | 2026-04-15T00:00 |
| TASK-169 | 아렌트 데이터 입력 (ES 직접) — field=civic_edu, claims 8~10 (공적 영역, 활동적 삶, 악의 평범성 등) | coder | DONE | MEDIUM | TASK-172 | 2026-04-15T00:00 | 2026-04-15T15:30 |
| TASK-170 | 아렌트 데이터 검증 | tester | DONE | MEDIUM | TASK-169 | 2026-04-15T00:00 | 2026-04-15T00:00 |
| TASK-171 | 아렌트 데이터 이슈 수정 (검증 결과 반영) | coder | DONE | MEDIUM | TASK-170 | 2026-04-15T00:00 | 2026-04-15T00:00 |
| TASK-172 | Phase 5 신규 field 문서 3개 등록 (peace_studies, unification_edu, civic_edu) | coder | DONE | HIGH | - | 2026-04-15T00:00 | 2026-04-15T15:00 |
| --- | **Phase 6: 기출문제 해설 및 ES 보강 (도덕·윤리 전공 A/B, 2014~2026)** | --- | --- | --- | --- | --- | --- |
| TASK-173 | architecture.md Phase 6 섹션 추가 (파일 구조·템플릿·검증 원칙) | manager | DONE | HIGH | - | 2026-04-18T00:00 | 2026-04-18T00:00 |
| TASK-174 | 기출 md 26파일 전수 스캔 → exam-coverage-map.md 산출. 입력 경로: `~/잡동사니/임용/md/` 하위 파일명에 "도덕" 또는 "윤리"를 포함하는 26개. 산출 경로: `projects/ethics-study/exam-solutions/exam-coverage-map.md` (디렉토리 신규 생성). 매핑 항목: 연도/과목(A/B)/문항번호/배점/주요 사상가/핵심 개념/주요 저서/ES 커버리지(있음·부족·없음)/분류(사상가형·교과교육학·경계영역). 최종 섹션: 누락 사상가 목록(중복제거), 교과교육학 문항 목록(제외 대상), 경계영역 문항 목록(topical/ 대상), 부족 claim 힌트 | coder | BLOCKED(TASK-175A) | HIGH | TASK-173 | 2026-04-18T00:00 | 2026-04-19T00:00 |
| TASK-175A | exam-coverage-map.md 전면 재작성. Coder **Opus 호출 필수**. **입력 소스**: `~/잡동사니/임용/md/` 하위, 파일명에 "도덕" 또는 "윤리"를 포함하는 26개 파일(2014~2026 도덕·윤리 전공 A/B). **원문 번호 체계 보존**: 2014-A 기입형 1~15 + 서답형 1~5, 2014-B 서술형 1~2 + 논술형 1~2, 2015-A 기입형 1~10 + 서술형 1~4, 2015-B 서술형 1~3 + 논술형 1~3, 2016~2019 A 기입형 1~8 + 서술형 1~6 + B 서술형 1~4 + 논술형 1~4, 2020~2026 A 기입형 1~8 + 서술형 1~4 + B 서술형 1~4 + 논술형 1~7 (원문 확인 필수). **총 문항 수 293 고정**: 서술·요약·산식 모든 위치에서 동일 수치 (2014=24, 2015=20, 2016~2019=88, 2020~2026=161). **ES thinker_id canonical 조회 명령**: `curl -s "http://localhost:9200/ethics-thinkers/_search?size=100&_source=id,name,name_en" \| jq '.hits.hits[]._source'` 결과를 기록·참조. thinker_id는 canonical만 사용. **Paul Taylor 구분 규칙**: ES의 `taylor`는 Charles Taylor(공동체주의). 2015-A14 등 Paul Taylor(생명중심주의) 해당 문항은 `taylor_p` 예정 id로 표기하고 "없음(**누락**)" 커버리지로 기록. 동명이인 suffix 규칙은 architecture.md "thinker_id 정규화 규칙" 참조. **원문 인용 필수**: 각 문항 row "메모" 컬럼에 원문 2~3구절을 Read 결과에서 직접 복사 삽입. 원문에 등장하지 않는 사상가·개념어 기록 금지. 불명확 사상가는 "사상가 불명(확인 필요)"로 표기. **산출물 교체**: 기존 `projects/ethics-study/exam-solutions/exam-coverage-map.md`를 전면 대체. 이전 산출은 이미 `exam-coverage-map.v1-rejected.md`로 백업됨(기계 치환 반영된 스냅샷) — 추가 백업 불필요. **블로커 누적 규칙**: 재작성 중 원문 판독 불가·출처 미상 row는 `<!-- BLOCKER(TASK-175A): {사유} -->` 주석 처리 후 계속 진행하고, `blocker-log.md`에 개별 누적. 중단 금지 | coder(opus) | DONE | HIGH | TASK-174 | 2026-04-19T00:00 | 2026-04-20T00:00 |
| TASK-175B | 재작성된 exam-coverage-map.md row-by-row 재검증. 각 row의 사상가·분류·thinker_id가 원문과 일치하는지 확인. thinker_id는 ES `_doc` lookup으로 실존 확인. 분류 카운트 합이 총 문항수(293)와 일치하는지 재계산. 블로커 발견 시 `blocker-log.md`에 누적 기록 | tester | DONE(blocker=8) | HIGH | TASK-175A | 2026-04-19T00:00 | 2026-04-20T00:00 |
| TASK-176+ | Phase 6 후속(연도별 해설 26파일·누락 사상가 보강 3-tuple·topical/ 파일): coverage-map 2014~2019 구간 신뢰 불가로 **사용자 검토(BLK-175B-001~008) 확정 전까지 자동 생성 보류**. 사용자가 공부 중 특정 사상가·개념 요청 시 개별 태스크로 유연 진행 가능 (architecture.md 블로커 누적 정책) | manager | BLOCKED(user-review-pending) | HIGH | TASK-175B | 2026-04-20T00:00 | 2026-04-20T00:00 |
| TASK-175D | exam-coverage-map.md 293 row 전수 재검증 (row-by-row). 원문 26파일 직독, 각 row의 ①발문·②제시문·③사상가·분류를 독립 도출해 coverage-map과 대조. 오매핑·할루시네이션·분류 오류·번호 체계 오류·분배 오류 모두 리스트업. 기존 BLK-175B-001~008과 중복은 제외, 신규 발견은 BLK-175D-XXX로 누적. 산출: `signal/ethics-study/tester-report-TASK-175D.md` + `blocker-log.md` append. 목적: 남은 블로커를 미리 정리해 사용자 일괄 검토 규모 확정 | tester | DONE(blocker=11) | HIGH | TASK-175B | 2026-04-20T00:00 | 2026-04-20T18:00 |
| --- | **TASK-175E: 커버리지 맵 전면 재작성 (1연도×1과목 배치, 순차 처리)** | --- | --- | --- | --- | --- | --- |
| TASK-175E-2014-A | 2014 전공A (기입형 1~15, 서술형 1~5, 20문항) 커버리지 재작성. architecture.md "Phase 6 기출 작업 규칙" 엄격 적용: 원문 직독·3단계 확정·메모 복사 인용·file_path:line_range 병기·canonical thinker_id만. 입력: ~/잡동사니/임용/md/2014중등1차-2교시-도덕윤리-전공A-문제지-최종.md. 산출: projects/ethics-study/exam-solutions/coverage/2014-A.md. PASS 받기 전까지 2014-B 진행 금지 | coder(opus) | DONE | HIGH | TASK-175D | 2026-04-20T18:00 | 2026-04-20T19:00 |
| TASK-175E-2014-A-T | 2014-A coverage 전수 검증 (row-by-row 20문항). Coder 독립 풀이 후 대조. grep 0건 규칙. 결과 PASS/FAIL | tester | DONE(PASS) | HIGH | TASK-175E-2014-A | 2026-04-20T18:00 | 2026-04-20T19:30 |
| TASK-175E-2014-B | 2014 전공B (서술형 1~2, 논술형 1~2, 4문항). 입력: 2014중등1차-3교시-도덕윤리-전공B-문제지-최종.md. 산출: coverage/2014-B.md | coder(opus) | DONE | HIGH | TASK-175E-2014-A-T | 2026-04-20T18:00 | 2026-04-20T20:15 |
| TASK-175E-2014-B-T | 2014-B 전수 검증 (4문항) | tester | DONE(PASS) | HIGH | TASK-175E-2014-B | 2026-04-20T18:00 | 2026-04-20T20:30 |
| TASK-175E-2015-A | 2015 전공A (기입형 1~10, 서술형 1~4, 14문항). 입력: 2015중등1차-도덕윤리_전공A.md. 산출: coverage/2015-A.md. 기입형4는 순자(xunzi) 복수 주제 문항 — (가)/(나) 빈칸 정답은 Coder가 원문 직독 후 독립 확정(사전 힌트 없음). 한자+한글 병기 필수 | coder(opus) | DONE(blocker=2) | HIGH | TASK-175E-2014-B-T | 2026-04-20T18:00 | 2026-04-20T21:15 |
| TASK-175E-2015-A-T | 2015-A 전수 검증 (14문항) | tester | DONE(PASS,observation) | HIGH | TASK-175E-2015-A | 2026-04-20T18:00 | 2026-04-20T21:45 |
| TASK-175E-HANJA-FIX | 2014-A, 2015-A coverage **2파일** 한자+한글 병기 보강 (architecture.md 조항 4 소급 적용). 2014-B는 한자 노출 0건으로 대상 제외(Reviewer 확인). **치환 대상**: 메모 컬럼의 해설 문장·판정 근거·분류 설명·집계 섹션·ES 커버리지 column 내 한글 서술. **예외(보존)**: ① `"..."` 또는 `『...』` 로 감싼 원문 직접 인용구절, ② 백틱 `` `...` `` 로 감싼 코드/식별자/URL, ③ HTML 주석 `<!-- ... -->` 내 grep 키워드·BLOCKER 근거. **치환 형식**: `한자(한글독음 — 간단 의미)`. 예시: `禮` → `禮(예)`, `化性起僞` → `化性起僞(화성기위 — 본성을 교화하여 인위를 일으킴)`, `天人之分` → `天人之分(천인지분 — 하늘과 사람의 직분 구분)`, `理發` → `理發(이발 — 이가 발함)`. **Coder 제출물**: 수정된 2파일 + Coder report 에 row별 before/after diff 샘플 포함 | coder(opus) | DONE(+Manager patch 3건) | HIGH | TASK-175E-2015-A-T | 2026-04-20T22:00 | 2026-04-20T22:55 |
| TASK-175E-HANJA-FIX-T | 한자 병기 보강 2파일 전수 검증: ① 치환 대상 영역의 한자 단독 노출 0건 확인, ② 원문 인용/백틱/HTML 주석 영역 비변경 확인, ③ 기존 row 매핑(사상가·분류·ES 커버리지·집계 카운트) 비변경 확인 | tester | DONE(PASS,observation) | HIGH | TASK-175E-HANJA-FIX | 2026-04-20T22:00 | 2026-04-20T22:55 |
| TASK-175E-2015-B | 2015 전공B (**서술형 1~4, 논술형 1~2, 6문항 40점**; 원문 L14=서술형【1~4】5점×4, L71=논술형【1~2】10점×2 확정). 입력: 2015중등1차-도덕윤리_전공B.md (95 lines). 산출: coverage/2015-B.md. architecture.md Phase 6 규칙 조항 1~6 엄격 적용 — 특히 **조항 4 한자+한글 병기 원칙** 선제 적용 (메모·해설·집계·ES 커버리지 column 에서 한자 노출 시 `한자(한글독음 — 간단 의미)` 형식 필수) | coder(opus) | DONE | HIGH | TASK-175E-HANJA-FIX-T | 2026-04-20T18:00 | 2026-04-20T23:30 |
| TASK-175E-2015-B-T | 2015-B 전수 검증 (6문항) | tester | DONE(PASS) | HIGH | TASK-175E-2015-B | 2026-04-20T18:00 | 2026-04-20T23:45 |
| TASK-175E-2016-A | 2016 전공A (**기입형 Q1~Q8 각 [2점]×8=16점 + 서술형 Q9~Q14 각 [4점]×6=24점, 총 14문항 40점**; 원문 L7 "14문항 40점", 기입형 line: L16/L30/L44/L53/L69/L87/L96/L104, 서술형 line: L112/L126/L140/L152/L162/L177 확정). 입력: 2016중등1차-도덕윤리-전공A.md (185 lines). 산출: coverage/2016-A.md. architecture.md Phase 6 규칙 조항 1~6 엄격 적용 — 특히 **조항 4 한자+한글 병기 원칙** 선제 적용 (Q3/Q4/Q5/Q11/Q13/Q14에 한자 인용 집중 — 메모·해설·집계·ES 커버리지 column 에서 한자 노출 시 `한자(한글독음 — 간단 의미)` 형식 필수) | coder(opus) | DONE(blocker=7 ES-gap) | HIGH | TASK-175E-2015-B-T | 2026-04-20T18:00 | 2026-04-21T00:30 |
| TASK-175E-2016-A-T | 2016-A 전수 검증 (14문항) | tester | DONE(PASS) | HIGH | TASK-175E-2016-A | 2026-04-20T18:00 | 2026-04-21T00:45 |
| TASK-175E-2016-B | 2016 전공B (**서술형 Q1~Q5 [4점]×5=20점 + Q6~Q7 [5점]×2=10점 + Q8 [10점]×1=10점, 총 8문항 40점** — 배점 불균등; 원문 L7 "8문항 40점", 문항 line: L16/L29/L44/L53/L63/L75/L85/L93 확정). 입력: 2016중등1차-도덕윤리-전공B.md (112 lines). 산출: coverage/2016-B.md. architecture.md Phase 6 규칙 조항 1~6 엄격 적용 — 특히 **조항 4 한자+한글 병기 원칙** 선제 적용 (**Q5 한자 집중**: 明/聖人/賢人/德/內外/道/理通/氣局/理一分殊 등, **Q6 한자 집중**: 先王/爲學/爲道/無爲/無不爲/聖人). 메모·해설·집계·ES 커버리지 column 에서 한자 노출 시 `한자(한글독음 — 간단 의미)` 형식 필수 | coder(opus) | DONE(blocker=3 ES-gap) | HIGH | TASK-175E-2016-A-T | 2026-04-20T18:00 | 2026-04-21T01:30 |
| TASK-175E-2016-B-T | 2016-B 전수 검증 (8문항) | tester | DONE(PASS,observation) | HIGH | TASK-175E-2016-B | 2026-04-20T18:00 | 2026-04-21T01:45 |
| TASK-175E-2017-A | 2017 전공A (**기입형 Q1~Q8 [2점]×8=16점 + 서술형 Q9~Q14 [4점]×6=24점, 총 14문항 40점**; 원문 L7 "14문항 40점", 문항 line: L14/L28/L36/L46/L56/L66/L76/L86/L96/L111/L121/L129/L143/L157 확정). 입력: 2017_중등1차_도덕,윤리_전공A.md (175 lines). 산출: coverage/2017-A.md. architecture.md Phase 6 규칙 조항 1~6 엄격 적용 — 특히 **조항 4 한자+한글 병기 원칙** 선제 적용 (**Q4 한국불교/지눌 돈오·점수**, **Q5 정약용 성기호설**, **Q6 한국 근대/동학**, **Q11 아리스토텔레스 아크라시아**, **Q13 성리학 인의예지/경**에 한자 집중). 메모·해설·집계·ES 커버리지 column 한자 노출 시 `한자(한글독음 — 간단 의미)` 형식 필수 | coder(opus) | DONE(blocker=5 ES-gap) | HIGH | TASK-175E-2016-B-T | 2026-04-20T18:00 | 2026-04-21T02:30 |
| TASK-175E-2017-A-T | 2017-A 전수 검증 (14문항) | tester | DONE(PASS,observation) | HIGH | TASK-175E-2017-A | 2026-04-20T18:00 | 2026-04-21T02:45 |
| TASK-175E-2017-B | 2017 전공B (**서술형 Q1~Q5 [4점]×5=20점 + Q6~Q7 [5점]×2=10점 + Q8 [10점]×1=10점, 총 8문항 40점** — 배점 불균등; 원문 L7 "8문항 40점", 문항 line: L14/L26/L36/L46/L59/L71/L81/L93 확정, 실제 파일 110줄). 입력: 2017_중등1차_도덕,윤리_전공B.md. 산출: coverage/2017-B.md. architecture.md Phase 6 규칙 조항 1~6 엄격 적용 — 특히 **조항 4 한자+한글 병기 원칙** 선제 적용 (**Q4 초기불교 연기법**: 法/無明/行/識/法界/等正覺, **Q7 동양 고대/노자·장자·묵자**: 天/聖人 등 한자 집중). 메모·해설·집계·ES 커버리지 column 한자 노출 시 `한자(한글독음 — 간단 의미)` 형식 필수 | coder(opus) | DONE | HIGH | TASK-175E-2017-A-T | 2026-04-20T18:00 | 2026-04-21T13:00 |
| TASK-175E-2017-B-T | 2017-B 전수 검증 (8문항) | tester | DONE(PASS) | HIGH | TASK-175E-2017-B | 2026-04-20T18:00 | 2026-04-21T13:15 |
| TASK-175E-2018-A | 2018 전공A (**기입형 Q1~Q8 [2점]×8=16점 + 서술형 Q9~Q14 [4점]×6=24점, 총 14문항 40점**; 원문 L7 "14문항 40점", 문항 line: L14/L24/L41/L53/L63/L73/L81/L99/L123/L135/L143/L157/L167/L177 확정, 실제 파일 187줄). 입력: 2018_중등1차_도덕윤리_전공A.md. 산출: coverage/2018-A.md. architecture.md Phase 6 규칙 조항 1~6 엄격 적용 — 특히 **조항 4 한자+한글 병기 원칙** (**Q4 한국불교**: 眞如/妄念/境界相/言說, **Q12 중국 성리학**: 性/氣/知/行/先後, **Q14 중국 고대**: 是非/得). 메모·해설·집계·ES 커버리지 column 한자 노출 시 `한자(한글독음 — 간단 의미)` 형식 필수 | coder(opus) | DONE(blocker=1 ES-gap) | HIGH | TASK-175E-2017-B-T | 2026-04-20T18:00 | 2026-04-21T13:45 |
| TASK-175E-2018-A-T | 2018-A 전수 검증 (14문항) | tester | DONE(PASS,observation) | HIGH | TASK-175E-2018-A | 2026-04-20T18:00 | 2026-04-21T14:00 |
| TASK-175E-2018-B | 2018 전공B (**서술형 Q1~Q5 [4점]×5=20점 + Q6~Q7 [5점]×2=10점 + Q8 [10점]×1=10점, 총 8문항 40점**; 원문 L7 "8문항 40점", 문항 line: L14/L28/L38/L48/L58/L71/L81/L102 확정, 실제 파일 127줄). 입력: 2018_중등1차_도덕윤리_전공B.md. 산출: coverage/2018-B.md. architecture.md Phase 6 규칙 조항 1~6 엄격 적용 — 특히 **조항 4 한자+한글 병기 원칙** | coder(opus) | DONE(blocker=1 ES-gap) | HIGH | TASK-175E-2018-A-T | 2026-04-20T18:00 | 2026-04-21T14:45 |
| TASK-175E-2018-B-T | 2018-B 전수 검증 (8문항) | tester | DONE(PASS,observation) | HIGH | TASK-175E-2018-B | 2026-04-20T18:00 | 2026-04-21T15:00 |
| TASK-175E-2019-A | 2019 전공A (**기입형 Q1~Q8 [2점]×8=16점 + 서술형 Q9~Q14 [4점]×6=24점, 총 14문항 40점**; 원문 L7 "14문항 40점", 문항 line: L14/L25/L35/L43/L51/L59/L67/L75/L83/L93/L108/L116/L130/L145 확정, 실제 파일 155줄). 입력: 2019_중등1차_도덕윤리A.md. 산출: coverage/2019-A.md. architecture.md Phase 6 규칙 조항 1~6 엄격 적용 — 특히 **조항 4 한자+한글 병기 원칙** | coder(opus) | DONE(blocker=2 ES-gap, Tester 재분류) | HIGH | TASK-175E-2018-B-T | 2026-04-20T18:00 | 2026-04-21T15:45 |
| TASK-175E-2019-A-T | 2019-A 전수 검증 (14문항) | tester | DONE(PASS,blocker 재분류 2건) | HIGH | TASK-175E-2019-A | 2026-04-20T18:00 | 2026-04-21T16:05 |
| TASK-175E-2019-A-FIX | 2019-A coverage ES-gap blocker 주석·카운트 갱신 (Tester 재분류 반영) | coder | DONE | HIGH | TASK-175E-2019-A-T | 2026-04-21T16:05 | 2026-04-21T16:15 |
| TASK-175E-2019-B | 2019 전공B (**서술형 Q1~Q5 [4점]×5=20점 + Q6~Q7 [5점]×2=10점 + Q8 [10점]×1=10점, 총 8문항 40점**; 원문 L7 "8문항 40점", 문항 line: L14/L29/L43/L51/L59/L72/L94/L110 확정, 실제 파일 128줄). 입력: 2019_중등1차_도덕윤리B.md. 산출: coverage/2019-B.md. architecture.md Phase 6 규칙 조항 1~6 엄격 적용. **ES-gap 정책** (2018-A regan·2018-B turiel·2019-A bandura/pettit·skinner 선례): 제시문 중심 사상가가 ES 미등록이면 blocker 등록 (observation 아님) | coder(opus) | DONE(blocker=2 ES-gap Q3·Q8) | HIGH | TASK-175E-2019-A-FIX | 2026-04-20T18:00 | 2026-04-21T17:15 |
| TASK-175E-2019-B-T | 2019-B 전수 검증 (8문항) | tester | DONE(PASS,observation) | HIGH | TASK-175E-2019-B | 2026-04-20T18:00 | 2026-04-21T17:25 |
| TASK-175E-2020-A | 2020 전공A (**기입형 Q1~Q4 [2점]×4=8점 + 서술형 Q5~Q12 [4점]×8=32점, 총 12문항 40점**; 원문 L7 "12문항 40점", 문항 line: L16/L26/L34/L44/L53/L68/L82/L105/L117/L135/L149/L159 확정, 실제 파일 174줄). 입력: 2020_중등1차_도덕윤리_전공A.md. 산출: coverage/2020-A.md. architecture.md Phase 6 규칙 조항 1~6 엄격 적용. **ES-gap 정책** (선례: BLK-175E-2018A-001/2018B-001/2019A-001/2019A-002/2019B-001/2019B-002): 제시문 중심 사상가가 ES 미등록이면 blocker 등록 (observation 아님) | coder(opus) | DONE(blocker=4 ES-gap Q3·Q7·Q10·Q12) | HIGH | TASK-175E-2019-B-T | 2026-04-20T18:00 | 2026-04-21T17:50 |
| TASK-175E-2020-A-T | 2020-A 전수 검증 (12문항) | tester | DONE(PASS) | HIGH | TASK-175E-2020-A | 2026-04-20T18:00 | 2026-04-21T17:57 |
| TASK-175E-2020-B | 2020 전공B (**기입형 Q1~Q2 [2점]×2=4점 + 서술형 Q3~Q11 [4점]×9=36점, 총 11문항 40점**; 원문 L7 "11문항 40점", 문항 line: L14/L28/L38/L51/L75/L90/L109/L119/L145/L157/L172 확정, 실제 파일 188줄). 입력: 2020_중등1차_도덕윤리_전공B.md. 산출: coverage/2020-B.md. architecture.md Phase 6 규칙 조항 1~6 엄격 적용. **ES-gap 정책** (선례 10건 2018A~2020A): 제시문 중심 사상가가 ES 미등록이면 blocker 등록 (observation 아님) | coder(opus) | DONE(blocker=3 ES-gap Q1·Q6·Q8) | HIGH | TASK-175E-2020-A-T | 2026-04-20T18:00 | 2026-04-21T18:15 |
| TASK-175E-2020-B-T | 2020-B 전수 검증 (11문항) | tester | DONE(PASS) | HIGH | TASK-175E-2020-B | 2026-04-20T18:00 | 2026-04-21T18:22 |
| TASK-175E-2021-A | 2021 전공A (**기입형 Q1~Q4 [2점]×4=8점 + 서술형 Q5~Q12 [4점]×8=32점, 총 12문항 40점**; 원문 L7 "12문항 40점", 문항 line: L14/L41/L55/L64/L74/L95/L111/L125/L138/L152/L174/L186 확정, 실제 파일 206줄). 입력: 2021_중등1차_도덕윤리_전공A.md. 산출: coverage/2021-A.md. architecture.md Phase 6 규칙 조항 1~6 엄격 적용. **ES-gap 정책** (선례 13건 2018A~2020B): 제시문 중심 사상가가 ES 미등록이면 blocker 등록 (observation 아님) | coder(opus) | DONE(blocker=3 ES-gap, id bug FIX 대기) | HIGH | TASK-175E-2020-B-T | 2026-04-20T18:00 | 2026-04-21T18:55 |
| TASK-175E-2021-A-T | 2021-A 전수 검증 (12문항) | tester | DONE(bug: paul_taylor→taylor_p 규약 위반) | HIGH | TASK-175E-2021-A | 2026-04-20T18:00 | 2026-04-21T19:05 |
| TASK-175E-2021-A-FIX | 2021-A coverage/blocker-log Q9 Paul Taylor id `paul_taylor`→`taylor_p` 일괄 치환 (architecture.md:491 동명이인 suffix 규약 준수). 대상 파일: coverage/2021-A.md Q9 row, signal/ethics-study/blocker-log.md BLK-175E-2021A-003 섹션, signal/ethics-study/coder-report-TASK-175E-2021-A.md. 정답·trademark·판정은 비변경 | coder | DONE(16건 치환) | HIGH | TASK-175E-2021-A-T | 2026-04-21T19:05 | 2026-04-21T19:08 |
| TASK-175E-2021-B | 2021 전공B (**기입형 Q1~Q2 [2점]×2=4점 + 서술형 Q3~Q11 [4점]×9=36점, 총 11문항 40점**; 원문 L7 "11문항 40점", 문항 line: L14/L24/L33/L48/L62/L76/L90/L104/L118/L132/L145 확정, 실제 파일 157줄). 입력: 2021_중등1차_도덕윤리_전공B.md. 산출: coverage/2021-B.md. architecture.md Phase 6 규칙 조항 1~6 엄격 적용. **ES-gap 정책** (선례 16건 2018A~2021A): 제시문 중심 사상가가 ES 미등록이면 blocker 등록. **thinker_id 규약** (architecture.md:491): 동명이인은 lastname_suffix (taylor/taylor_p, mill_js 패턴) | coder(opus) | DONE(blocker=7 ES-gap) | HIGH | TASK-175E-2021-A-FIX | 2026-04-20T18:00 | 2026-04-21T19:28 |
| TASK-175E-2021-B-T | 2021-B 전수 검증 (11문항) | tester | DONE(PASS) | HIGH | TASK-175E-2021-B | 2026-04-20T18:00 | 2026-04-21T19:35 |
| TASK-175E-2022-A | 2022 전공A (**기입형 Q1~Q4 [2점]×4=8점 + 서술형 Q5~Q12 [4점]×8=32점, 총 12문항 40점**; 원문 L7 "12문항 40점", 문항 line: L14/L24/L32/L40/L49/L62/L76/L89/L105/L121/L143/L159 확정, 실제 파일 206줄). 입력: 2022_중등1차_도덕윤리_전공A.md. 산출: coverage/2022-A.md. architecture.md Phase 6 규칙 조항 1~6 엄격 적용. **ES-gap 정책** (선례 누적 23건 2018A~2021B): 제시문 중심 사상가가 ES 미등록이면 blocker 등록. **thinker_id 규약** (architecture.md:491): 동명이인은 lastname_suffix (taylor/taylor_p, mill_js 패턴) | coder(opus) | DONE(blocker=7 ES-gap) | HIGH | TASK-175E-2021-B-T | 2026-04-20T18:00 | 2026-04-21T19:56 |
| TASK-175E-2022-A-T | 2022-A 전수 검증 (12문항) | tester | DONE(PASS) | HIGH | TASK-175E-2022-A | 2026-04-20T18:00 | 2026-04-21T20:05 |
| TASK-175E-2022-B | 2022 전공B (11문항 40점; blocker=5 popper/durkheim/james/hoffman/singer; **hoffman 4연속 재출제 확증** 2016-A→2019-B→2021-B→2022-B). 산출: coverage/2022-B.md | coder(opus) | DONE(blocker=5 ES-gap) | HIGH | TASK-175E-2022-A-T | 2026-04-20T18:00 | 2026-04-21T20:35 |
| TASK-175E-2022-B-T | 2022-B 전수 검증 (11문항, verdict=PASS) | tester | DONE(PASS) | HIGH | TASK-175E-2022-B | 2026-04-20T18:00 | 2026-04-21T20:45 |
| TASK-175E-2023-A | 2023 전공A (12문항 40점; blocker=6 tocqueville/viroli/choe_jeu/shweder/choe_chiwon/blasi; **blasi 2연속 재출제 확증** 2020-B→2023-A; mill_js 단일 시험 2회 출제 Q7·Q11). 산출: coverage/2023-A.md | coder(opus) | DONE(blocker=6 ES-gap) | HIGH | TASK-175E-2022-B-T | 2026-04-20T18:00 | 2026-04-21T15:20 |
| TASK-175E-2023-A-T | 2023-A 전수 검증 (12문항, verdict=PASS) | tester | DONE(PASS) | HIGH | TASK-175E-2023-A | 2026-04-20T18:00 | 2026-04-21T15:30 |
| TASK-175E-2023-B | 2023 전공B (11문항 40점; blocker=6 Q1 사상가 특정불능/niebuhr/nagarjuna/vasubandhu/freud/skinner; 모든 사상가 고유명 부재 이례). 산출: coverage/2023-B.md | coder(opus) | DONE(blocker=6) | HIGH | TASK-175E-2023-A-T | 2026-04-20T18:00 | 2026-04-21T16:00 |
| TASK-175E-2023-B-T | 2023-B 전수 검증 (11문항, verdict=PASS) | tester | DONE(PASS) | HIGH | TASK-175E-2023-B | 2026-04-20T18:00 | 2026-04-21T16:10 |
| TASK-175E-2024-A | 2024 전공A (12문항 40점; blocker=5 coombs/narvaez/Q5검사명/Q7갑사상가특정불능/fazang; **narvaez 2회 재출제** 2016-A→2024-A, **hoffman 5연속 확장 실패**, mill_js 2023-A→2024-A 2연속). 산출: coverage/2024-A.md | coder(opus) | DONE(blocker=5) | HIGH | TASK-175E-2023-B-T | 2026-04-20T18:00 | 2026-04-21T17:35 |
| TASK-175E-2024-A-T | 2024-A 전수 검증 (12문항, verdict=PASS) | tester | DONE(PASS) | HIGH | TASK-175E-2024-A | 2026-04-20T18:00 | 2026-04-21T17:50 |
| TASK-175E-2024-B | 2024 전공B (11문항 40점; blocker=6 turiel/durkheim/blasi/bandura/singer/regan; **본문 Coder HIT/MISS 정확하나 재출제 연속성 기록에 bug → FIX 필요**). 산출: coverage/2024-B.md | coder(opus) | DONE(blocker=6, 후속 FIX) | HIGH | TASK-175E-2024-A-T | 2026-04-20T18:00 | 2026-04-21T18:30 |
| TASK-175E-2024-B-T | 2024-B 전수 검증 (11문항, verdict=NEEDS_REVISION severity=bug 재출제 연속성 기록 오류) | tester | DONE(NEEDS_REVISION) | HIGH | TASK-175E-2024-B | 2026-04-20T18:00 | 2026-04-21T18:40 |
| TASK-175E-2024-B-FIX | 2024-B 재출제 연속성 기록 정정 (문서만). 15개 지점 수정. 재출제 이력 grep 실증: turiel 4회(2018B/2021B/2022A/2024B) / bandura 4회(2014A/2019A/2020A/2024B) / regan 2회(2018A/2024B) / durkheim 4회(2015B/2021B/2022B/2024B) / **blasi 5회 최다(2017A/2019B/2021A/2023A/2024B)** / singer 4회(2015B/2019B/2022B/2024B) | coder | DONE | HIGH | TASK-175E-2024-B-T | 2026-04-21T18:42 | 2026-04-21T18:55 |
| TASK-175E-2025-A | 2025 전공A (12문항 40점; blocker=4 durkheim/hoffman/rest(오분류)/zhiyi; durkheim 2024-B→2025-A 2연속 확증). 산출: coverage/2025-A.md | coder(opus) | DONE(blocker=4 후속 FIX) | HIGH | TASK-175E-2024-B-T | 2026-04-20T18:00 | 2026-04-21T19:30 |
| TASK-175E-2025-A-T | 2025-A 전수 검증 (12문항, verdict=NEEDS_REVISION severity=bug rest MISS 오분류) | tester | DONE(NEEDS_REVISION) | HIGH | TASK-175E-2025-A | 2026-04-20T18:00 | 2026-04-21T19:45 |
| TASK-175E-2025-A-FIX | 2025-A rest MISS→HIT 정정 (BUG: `rest`는 ES에 10 claims로 실제 HIT인데 Coder가 MISS 오분류, BLK-175E-2025A-003 false-positive). 대상: coverage/2025-A.md L215/L277/L591/L601-L609/L635 rest MISS→HIT 교정 + blocker-log.md BLK-175E-2025A-003 삭제 + coder-report-TASK-175E-2025-A.md 정정. 추가(OBS): hoffman row-count 불일치(Coder 3회 vs grep 4회) 조사 후 정정. src 수정 금지 | coder | DONE | HIGH | TASK-175E-2025-A-T | 2026-04-21T19:46 | 2026-04-21T20:00 |
| TASK-175E-2025-B | 2025 전공B (11문항 40점; 기입형 Q1~Q2 2점×2 + 서술형 Q3~Q11 4점×9=40점). 입력: `/home/jai/잡동사니/임용/md/2025_중등1차_도덕·윤리_전공B.md` (206 lines). 예상 사상가: Q1 jinul(지눌 돈오돈수·자성정혜) / Q2 moore(무어 메타윤리 자연주의 오류) / Q3 lickona(리코나 인격교육 존중·책임 3형식) / Q4 kohlberg(갑 6단계 정의 원리) + gilligan(을 하인즈 11세 남아/여아 이야기) / Q5 bandura(갑 자아효능감 대리경험·언어적 설득·생리적 상태) / Q6 wang_yangming(갑 심즉리·허령) + zhuxi(을 격물치지·궁리) / Q7 yiyulgok(갑 이기의 집·오상순선·기질) + im_seongju 또는 yiyulgok 변이(을 이기지묘·상지하우; 사상가 grep 실증 필수) / Q8 kant(선의지·정언명령·가언명령·의무) / Q9 bentham(갑 제재 4원천·입법자) + mill(을 연상·자연적 감정 토대) / Q10 viroli 또는 pettit(갑 신로마 공화주의 비지배 자치) + berlin(을 소극적 자유) / Q11 hobbes(리바이어던 2자연법·신의계약). 재출제 경계: **bandura 2024-B→2025-B 2연속 여부 grep 실증 필수** (2024-B Q9 등장). 재출제 경계 기록 시 grep 실증 규칙 엄수(TASK-175E-2024-B-FIX에서 확립). 산출: coverage/2025-B.md | coder(opus) | DONE(blocker=6, 후속 FIX) | HIGH | TASK-175E-2025-A-FIX | 2026-04-20T18:00 | 2026-04-21T20:30 |
| TASK-175E-2025-B-T | 2025-B 전수 검증 (11문항, verdict=NEEDS_REVISION severity=bug 3건: Q1 발문 오독 / grep 0건 trademark 7개 / Q7 갑·을 배치 역전 가능성) | tester | DONE(NEEDS_REVISION) | HIGH | TASK-175E-2025-B | 2026-04-20T18:00 | 2026-04-21T20:45 |
| TASK-175E-2025-B-FIX | 2025-B 재작업 완료 (문서만). BUG-1 Q1 발문 재구성 (㉢돈수→점수·㉣자성정혜→수상정혜). BUG-2 7개 한자 trademark를 원문 한글 구절로 교체. BUG-3 Q7 을=yiyulgok 확정, 갑=사상가 확증 보류 (BLK-006 재정의). 최종 HIT 10 / MISS 6. 배점 40점 PASS | coder | DONE | HIGH | TASK-175E-2025-B-T | 2026-04-21T20:46 | 2026-04-21T21:00 |
| TASK-175E-2026-A | 2026 전공A 커버리지 신규 작성 (12문항 40점; HIT 11 / MISS 4). 산출: coverage/2026-A.md (842 lines) | coder(opus) | DONE(blocker=3) | HIGH | TASK-175E-2025-B-FIX | 2026-04-20T18:00 | 2026-04-21T21:55 |
| TASK-175E-2026-A-T | 2026-A 전수 검증 (12문항, verdict=PASS severity=observation) | tester | DONE(PASS) | HIGH | TASK-175E-2026-A | 2026-04-20T18:00 | 2026-04-21T22:05 |
| TASK-175E-2026-B | 2026 전공B 커버리지 신규 작성 (11문항 40점; HIT 8 / MISS 5, bandura 3연속 최장기록·jinul 2연속). 산출: coverage/2026-B.md (827 lines) | coder(opus) | DONE(blocker=5) | HIGH | TASK-175E-2026-A-T | 2026-04-20T18:00 | 2026-04-21T23:30 |
| TASK-175E-2026-B-T | 2026-B 전수 검증 (11문항, verdict=PASS). Phase 6 종결(26/26 coverage 완성). observation 2건(narvaez/bandura row 표기 미세차). MERGE 자격 PASS | tester | DONE(PASS) | HIGH | TASK-175E-2026-B | 2026-04-20T18:00 | 2026-04-21T23:55 |
| TASK-175E-MERGE | 26개 coverage/*.md → exam-coverage-map.md 병합 + Section A~E 집계. **스크립트 고정**: `projects/ethics-study/scripts/merge_coverage.py` (Python 3). **파서는 2-path**: (a) 구형 17개(2014-A~2022-A) 상단 `\| 문항 \| ... \| thinker_id \| ... \| ES 커버리지 \|` 5종 헤더 배리에이션 / (b) 신형 9개(2022-B~2026-B) 문항별 섹션 + 파일 말미 `\| Q \| ... \| thinker_id \| ES \|` 4종 헤더. Python dict-based 동적 헤더 매핑 필수. **thinker_id 추출 정규식**: 백틱 감싼 소문자 id (예: `` `bandura` ``); 교과교육학·보류(BLOCKER-PENDING)는 별도 분기. **canonical 55 dump**: `curl -s "localhost:9200/ethics-thinkers/_search?size=100&_source=id" \| jq -r '.hits.hits[]._source.id' \| sort` (ES 실시간). **taylor vs taylor_p 분리**: architecture.md L491 기준 Charles Taylor(ES 55 HIT) / Paul Taylor(`taylor_p` MISS) 반드시 구분. **Section 스키마**: A(누락 사상가: id \| name_kr \| 출제횟수 \| 출제연도 \| BLK-ID) / B(canonical 55: id \| 출제횟수 \| 출제연도 리스트 \| claims수) / C(경계영역 교과교육학·사상가 특정 불능 집계) / D(MISS TOP10 TASK-176 우선순위) / E(분류 카운트 + 배점 검산: 2014=50·나머지=40). **blocker-log 실측**: `grep -cE "^### BLK-175E-" blocker-log.md` 총 92건 + 철회 1(2025A-003) = net 92. **산출**: exam-coverage-map.md 신규(v1/v2 rejected 보존). **실행 명령**: `python3 projects/ethics-study/scripts/merge_coverage.py > projects/ethics-study/exam-solutions/exam-coverage-map.md` | coder(opus) | DONE | MEDIUM | TASK-175E-2026-B-T | 2026-04-20T18:00 | 2026-04-22T00:13 |
| TASK-175E-MERGE-T | exam-coverage-map.md 전수 검증 (11 체크, verdict=NEEDS_REVISION severity=bug 1건). 10/11 PASS. 1c FAIL: cell 내 thinker_id 중복 매칭 미중복제거로 `sandel`(2016-B Q3, 5→2), `wonhyo`(2016-A Q5, 5→4), `donghak_choe`(2017-A Q6, 2→1), `total_id_mentions`(359→354) inflate. Section D TOP10 / Section E 영향 없음 | tester | DONE(NEEDS_REVISION) | HIGH | TASK-175E-MERGE | 2026-04-22T00:14 | 2026-04-22T00:35 |
| TASK-176 | Section D TOP10 MISS 사상가 ES 등록 (우선순위 순, exam-coverage-map.md Section D 실측). jinul(7)→blasi(5)→durkheim(5)→hoffman(5)→bandura(4)→pettit(4)→singer(4)→turiel(4)→moore(3)→narvaez(3). 사상가 1인당 하위 태스크 2개(insert + 검증). 완료 시 canonical 55 → 65로 확장, Section A에서 10인이 Section B로 이동. **선행 조건**: merge_coverage.py 재실행으로 재집계 가능한지 확인 (MISS_NAME_MAP 수동 엔트리 정리 필요). **실행**: jinul부터 1인씩 순차 완료 후 나머지 9인 배치. architecture.md L490 canonical 55 → 65로 업데이트 | manager | TODO | MEDIUM | TASK-175E-MERGE-FIX | 2026-04-22T01:30 | 2026-04-22T01:30 |
| TASK-176-01 | jinul(보조국사 지눌·知訥) ES 등록. **실측**: exam-coverage-map.md Section A L29 출제 7회(2016-A, 2017-A, 2020-A, 2021-B, 2022-A, 2025-B, 2026-B); coverage 파일 grep jinul 14파일 76건. **사상가 메타**: id=`jinul` / name=`보조국사 지눌 (知訥)` / name_en=`Jinul (Bojo)` / field=`eastern_ethics` (wonhyo 선례) / era=`고려` / birth_year=1158 / death_year=1210. **핵심 저서** (본문 직록 필수): 『수심결(修心訣)』, 『권수정혜결사문(勸修定慧結社文)』, 『진심직설(眞心直說)』, 『간화결의론(看話決疑論)』, 『법집별행록절요병입사기(法集別行錄節要幷入私記)』. **핵심 주장 힌트** (출제 내역 기반, 원문 확증 필수): 돈오점수(頓悟漸修) / 정혜쌍수(定慧雙修) / 자성정혜(自性定慧) vs 수상정혜(隨相定慧) / 공적영지(空寂靈知) / 성적등지(惺寂等持) / 정혜결사 운동 / 조계종 원류. claims 8~10개 권장(7회 출제 → 청구된 주장·개념 충분). **스크립트 패턴**: `projects/ethics-study/scripts/insert_jinul.py` (insert_lickona.py·insert_wonhyo 참조). thinker + works + claims + keywords + relations(wonhyo·huineng 등 영향관계). **원문 인용 규정**: agents/coder.md 신규 규정 준수 — grep 0건 고유명 금지. insert_jinul.py 작성+실행 완료 (works=5, claims=9, keywords=9, relations=2). original_text verbatim 4건, 공란 5건 | coder(opus) | DONE | HIGH | TASK-176 | 2026-04-22T01:30 | 2026-04-22T01:45 |
| TASK-176-02 | blasi(아우구스토 블라시·Augusto Blasi) ES 등록. **실측**: exam-coverage-map.md Section A L30 출제 5회(2017-A, 2019-B, 2021-A, 2023-A, 2024-B); coverage grep 5파일 30건. **사상가 메타**: id=`blasi` / name=`아우구스토 블라시 (Augusto Blasi)` / name_en=`Augusto Blasi` / field=`moral_development` (kohlberg·gilligan 선례) / era=`현대` / birth_year=1936 / death_year=2014 / 이탈리아-미국 발달심리학자. **핵심 주장 힌트** (coverage 실측 개념): 자아 모델(Self Model) / 도덕적 정체성(moral identity) / 책임 판단(responsibility judgment) → 도덕적 행동 / 자기 일관성(self-consistency) / 도덕적 인격 3요소 중 **통합성(integrity·統合性)** (2024-B Q? 정답 "㉠=통합성") / 신콜버그주의 발달심리 계열. **주요 논문·저서**: "Bridging moral cognition and moral action" (1980) / "Moral cognition and moral action: A theoretical perspective" (1983) / "The self and the management of moral life" (2004) / "Moral Functioning" (ed.) 2005. **실행**: `projects/ethics-study/scripts/insert_blasi.py` (insert_kohlberg.py 참조). **원문 인용 규정 엄수**: agents/coder.md 신규 규정 — 확증 불가 original_text는 공란 처리. **재출제 핵심**: 통합성·책임 판단·자아 모델은 필수 claim | coder(opus) | TODO | HIGH | TASK-176-01-T | 2026-04-22T01:57 | 2026-04-22T01:57 |
| TASK-176-02-T | blasi ES 등록 검증. **체크**: (1) ethics-thinkers/blasi found / 메타 완비 / (2) claims ≥ 7(통합성·책임판단·자아모델·도덕적정체성·자기일관성·신콜버그·3요소) / works ≥ 3 / keywords ≥ 6 / (3) original_text verbatim 항목 coverage grep 매칭 (agents/tester.md 신규 표준) / (4) relations 링크 타깃 실재 (kohlberg 계열) / (5) 재출제 핵심 4개념(통합성·책임판단·자아모델·도덕적정체성) 각 ≥1 claim 커버 / (6) keyword 중복 없음 / (7) coverage md mtime 미변경 | tester | TODO | HIGH | TASK-176-02 | 2026-04-22T01:57 | 2026-04-22T01:57 |
| TASK-176-01-T | jinul ES 등록 검증 (7/7 PASS, severity=observation). original_text verbatim 4건 14개 파편 전건 coverage grep 매칭. relations 스키마 `from_thinker`/`to_thinker` 확인. **체크**: (1) `curl -s localhost:9200/ethics-thinkers/_doc/jinul` 존재 + 메타 필드 완비 / (2) works·claims·keywords 카운트 Coder 주장과 일치 / (3) claims.original_text 필드 값에 포함된 한자·고유명을 **저서 실체(또는 권위 있는 출처)와 grep 대조** — 없으면 severity=bug (agents/tester.md 신규 표준) / (4) relations 링크 타깃이 실제 존재(wonhyo 등) / (5) keywords 목록이 ethics-keywords 인덱스에 중복 없이 등록 / (6) 재출제 예상 주요 개념(돈오점수·정혜쌍수·자성정혜·수상정혜) 각각이 최소 1개 claim으로 커버됨 | tester | DONE(PASS) | HIGH | TASK-176-01 | 2026-04-22T01:30 | 2026-04-22T01:55 |
| TASK-175E-MERGE-FIX | `merge_coverage.py` extract_thinker_ids() cell 내 중복제거 패치 + exam-coverage-map.md 재생성. **수정 지점**: `projects/ethics-study/scripts/merge_coverage.py` L323-L343 `extract_thinker_ids()` 함수의 **두 반환 경로 모두**에 order-preserving dedupe 적용: (a) backtick 경로 `THINKER_ID_RE.findall()` 결과 (L330 부근), (b) bare-id 경로 `filtered` 리스트 (L337-L342 부근). 두 경로 모두 `list(dict.fromkeys(ids))` 적용 필수 (Tester 근거상 실제 3개 bug cell은 모두 bare-id 경로). 동일 셀 내 중복 매칭만 제거하고 서로 다른 row/cell 중복은 유지 (Section A/B 출제횟수 집계 의미 보존). **영향 검증**: Section B `sandel` 2회·`wonhyo` 4회, Section A `donghak_choe` 1회로 정정. metadata yaml `total_id_mentions: 354`로 갱신. Section D TOP10 순서 불변·Section E 배점 불변 재확인. **실행**: `python3 projects/ethics-study/scripts/merge_coverage.py > projects/ethics-study/exam-solutions/exam-coverage-map.md`. 산출: 스크립트 patch + map 재생성 + coder-report 정정. Tester 8/8 PASS verdict=DONE observation | coder | DONE | HIGH | TASK-175E-MERGE-T | 2026-04-22T00:36 | 2026-04-22T00:55 |
