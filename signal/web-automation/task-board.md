# Task Board

| ID | Title | Assignee | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|--------|----------|------------|---------|---------|
| --- | **Phase 1: Core Toolkit** | --- | --- | --- | --- | --- | --- |
| TASK-001 | 프로젝트 초기화 (requirements.txt, 디렉토리 구조, config 템플릿) | coder | DONE | HIGH | - | 2026-04-13T20:00 | 2026-04-13T20:35 |
| TASK-002 | Core - browser.py (Playwright 브라우저 엔진: 시작/종료/이동/대기/스크린샷) | coder | DONE | HIGH | TASK-001 | 2026-04-13T20:00 | 2026-04-13T20:50 |
| TASK-003 | Core - config.py (YAML 설정 로더) + settings.yaml 템플릿 | coder | DONE | HIGH | TASK-001 | 2026-04-13T20:00 | 2026-04-13T20:40 |
| TASK-004 | Core - telegram.py (텔레그램 봇 알림: token+chat_id 기반) | coder | DONE | HIGH | TASK-001 | 2026-04-13T20:00 | 2026-04-13T20:50 |
| TASK-005 | Core - logger.py (로깅 + 단계별 스크린샷 자동 저장) | coder | DONE | MEDIUM | TASK-001 | 2026-04-13T20:00 | 2026-04-13T20:50 |
| TASK-006 | Core - retry.py (재시도 데코레이터 + 에러 핸들링) | coder | DONE | MEDIUM | TASK-001 | 2026-04-13T20:00 | 2026-04-13T20:50 |
| TASK-007 | Core Toolkit 테스트 (browser, config, telegram, logger, retry) | tester | TODO | HIGH | TASK-002,TASK-003,TASK-004,TASK-005,TASK-006 | 2026-04-13T20:00 | 2026-04-13T20:00 |
| --- | **Phase 2: 인증 + Anti-Bot** | --- | --- | --- | --- | --- | --- |
| TASK-008 | auth/naver_imap.py (Naver IMAP 연결 → 인증번호 자동 추출) + settings.yaml naver 섹션 추가 + tests/test_naver_imap.py (mock 기반 단위 테스트) | coder | IN_PROGRESS | TOP | TASK-001 | 2026-04-13T20:00 | 2026-04-22T00:00 |
| TASK-008-SMOKE | 실계정 연결 스모크 테스트 (WA_NAVER_EMAIL, WA_NAVER_APP_PASSWORD 환경변수로 실제 imap.naver.com:993 연결 → 최근 메일 1건 인증번호 추출 확인) | user | TODO | TOP | TASK-008 | 2026-04-22T00:00 | 2026-04-22T00:00 |
| TASK-009 | antibot/stealth.py (playwright-stealth 설정 적용) | coder | TODO | MEDIUM | TASK-002 | 2026-04-13T20:00 | 2026-04-22T00:00 |
| TASK-010 | ~~antibot/cloudflare.py~~ (제거됨: stealth로 CF 우회 불가 확인, capsolver 유료 API 도입 시점까지 보류) | - | REMOVED | - | - | 2026-04-13T20:00 | 2026-04-22T00:00 |
| TASK-011 | 인증 + stealth 테스트 (naver_imap, stealth) | tester | TODO | HIGH | TASK-008,TASK-009 | 2026-04-13T20:00 | 2026-04-22T00:00 |
| --- | **Phase 3: 티스토리 자동화** | --- | --- | --- | --- | --- | --- |
| TASK-012 | sites/tistory/login.py (카카오 로그인 → 이메일 인증번호 입력) | coder | TODO | HIGH | TASK-002,TASK-008 | 2026-04-13T20:00 | 2026-04-13T20:00 |
| TASK-013 | sites/tistory/writer.py (글 작성 자동화: 제목/본문/카테고리/발행) | coder | TODO | HIGH | TASK-012 | 2026-04-13T20:00 | 2026-04-13T20:00 |
| TASK-014 | tistory.yaml 설정 파일 작성 (URL, 셀렉터, 계정 설정 구조) | coder | TODO | HIGH | TASK-003 | 2026-04-13T20:00 | 2026-04-13T20:00 |
| TASK-015 | 티스토리 통합 테스트 (로그인 → 글 작성 → 발행 확인) | tester | TODO | HIGH | TASK-013,TASK-014 | 2026-04-13T20:00 | 2026-04-13T20:00 |
| --- | **Phase 4: 야놀자 자동화 (BLOCKED - capsolver 도입 대기)** | --- | --- | --- | --- | --- | --- |
| TASK-016 | sites/yanolja/login.py (Cloudflare 통과 → 이메일 로그인) | coder | BLOCKED | LOW | TASK-002,capsolver | 2026-04-13T20:00 | 2026-04-22T00:00 |
| TASK-017 | sites/yanolja/search.py (숙소 검색: 지역/날짜/인원/조건 필터) | coder | BLOCKED | LOW | TASK-016 | 2026-04-13T20:00 | 2026-04-22T00:00 |
| TASK-018 | sites/yanolja/booking.py (예약 버튼 클릭 + 텔레그램 알림) | coder | BLOCKED | LOW | TASK-017,TASK-004 | 2026-04-13T20:00 | 2026-04-22T00:00 |
| TASK-019 | yanolja.yaml 설정 파일 작성 (URL, 셀렉터, 계정 설정 구조) | coder | BLOCKED | LOW | TASK-003 | 2026-04-13T20:00 | 2026-04-22T00:00 |
| TASK-020 | 야놀자 통합 테스트 (CF 통과 → 로그인 → 검색 → 예약 클릭) | tester | BLOCKED | LOW | TASK-018,TASK-019 | 2026-04-13T20:00 | 2026-04-22T00:00 |
| --- | **Phase 5: CLI + 마무리** | --- | --- | --- | --- | --- | --- |
| TASK-021 | cli.py (CLI 진입점: tistory-login, tistory-write, yanolja-search, yanolja-book) | coder | TODO | MEDIUM | TASK-013,TASK-018 | 2026-04-13T20:00 | 2026-04-13T20:00 |
| TASK-022 | sites/base.py (BaseSiteWorkflow 인터페이스 정의) | coder | TODO | LOW | TASK-013,TASK-018 | 2026-04-13T20:00 | 2026-04-13T20:00 |
| TASK-023 | 전체 파이프라인 통합 테스트 | tester | TODO | HIGH | TASK-021 | 2026-04-13T20:00 | 2026-04-13T20:00 |
| --- | **Phase 6: 티스토리 글쓰기 에이전트 (architecture §6 참조)** | --- | --- | --- | --- | --- | --- |
| TASK-024 | 글쓰기 에이전트 상세 태스크 분해 (style/seo/image_placer/agent 등) | manager | TODO | LOW | TASK-013 | 2026-04-22T00:00 | 2026-04-22T00:00 |
