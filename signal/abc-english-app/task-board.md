# Task Board

| ID | Title | Assignee | Execution | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|-----------|--------|----------|------------|---------|---------|
| --- | **Phase 0: 프로젝트 기반** | --- | --- | --- | --- | --- | --- | --- |
| TASK-001 | Flutter 프로젝트 스캐폴딩 (flutter create, pubspec.yaml 의존성 정의) | coder | agent | TODO | HIGH | - | 2026-04-22 | 2026-04-22 |
| TASK-002 | Android manifest 설정 (INTERNET, FOREGROUND_SERVICE, MediaSession) | coder | agent | TODO | HIGH | TASK-001 | 2026-04-22 | 2026-04-22 |
| TASK-003 | core/config/app_config.dart (--dart-define 환경변수 읽기) | coder | agent | TODO | HIGH | TASK-001 | 2026-04-22 | 2026-04-22 |
| TASK-004 | core/errors/app_exception.dart + core/result.dart (sealed Result 타입) | coder | agent | TODO | HIGH | TASK-001 | 2026-04-22 | 2026-04-22 |
| TASK-005 | core/logging/app_logger.dart (logger 라이브러리 래퍼, 릴리스 레벨 분기) | coder | agent | TODO | MEDIUM | TASK-001 | 2026-04-22 | 2026-04-22 |
| TASK-006 | core/theme/app_theme.dart (Material 3 라이트·다크 테마, BreakPoints) | app-porter | agent | TODO | MEDIUM | TASK-001 | 2026-04-22 | 2026-04-22 |
| TASK-007 | main.dart + app.dart (Riverpod ProviderScope, MaterialApp.router, 전역 에러 바운더리) | coder | agent | TODO | HIGH | TASK-003,TASK-006 | 2026-04-22 | 2026-04-22 |
| TASK-008 | go_router 라우팅 설정 (tab shell + detail 라우트 placeholder) | coder | agent | TODO | HIGH | TASK-007 | 2026-04-22 | 2026-04-22 |
| TASK-009 | scripts/run_dev.sh 실행 편의 스크립트 | coder | agent | TODO | LOW | TASK-003 | 2026-04-22 | 2026-04-22 |
| --- | **Phase 1: 백엔드 /api/v1/ 신설 (abc-english 측)** | --- | --- | --- | --- | --- | --- | --- |
| TASK-010 | abc-english/web/api/v1/__init__.py + deps.py (Bearer 의존성) + settings에 ABC_API_TOKEN 추가 | coder | agent | TODO | HIGH | - | 2026-04-22 | 2026-04-22 |
| TASK-011 | /api/v1/episodes GET (목록, page/size/since_modified) | coder | agent | TODO | HIGH | TASK-010 | 2026-04-22 | 2026-04-22 |
| TASK-012 | /api/v1/episodes/{id} GET (상세+문장 리스트+타임스탬프) | coder | agent | TODO | HIGH | TASK-010 | 2026-04-22 | 2026-04-22 |
| TASK-013 | /api/v1/episodes/{id}/audio GET (기존 audio.py 재사용 래퍼) | coder | agent | TODO | HIGH | TASK-010 | 2026-04-22 | 2026-04-22 |
| TASK-014 | /api/v1/episodes/{id}/manifest GET (파일 목록 + ETag) | coder | agent | TODO | MEDIUM | TASK-010 | 2026-04-22 | 2026-04-22 |
| TASK-015 | /api/v1/lookup GET (단어 조회, 기존 lookup.py 위임) | coder | agent | TODO | MEDIUM | TASK-010 | 2026-04-22 | 2026-04-22 |
| TASK-016 | /api/v1/notebook CRUD (GET/POST/PATCH/DELETE + last_modified) | coder | agent | TODO | MEDIUM | TASK-010 | 2026-04-22 | 2026-04-22 |
| TASK-017 | /api/v1/notebook/sync POST (오프라인 변경 배치 업로드) | coder | agent | TODO | MEDIUM | TASK-016 | 2026-04-22 | 2026-04-22 |
| TASK-018 | /api/v1/ 통합 단위테스트 (Bearer 검증, 각 엔드포인트 계약) | tester | agent | TODO | HIGH | TASK-011,TASK-012,TASK-013,TASK-014,TASK-015,TASK-016,TASK-017 | 2026-04-22 | 2026-04-22 |
| --- | **Phase 2: Core 레이어** | --- | --- | --- | --- | --- | --- | --- |
| TASK-020 | core/network/dio_client.dart (Bearer 인터셉터, 재시도, 타임아웃) | coder | agent | TODO | HIGH | TASK-003,TASK-004 | 2026-04-22 | 2026-04-22 |
| TASK-021 | core/storage/app_database.dart (drift 정의, episodes/sentences/notebook 테이블) | coder | agent | TODO | HIGH | TASK-001 | 2026-04-22 | 2026-04-22 |
| TASK-022 | core/storage/migrations.dart (drift 마이그레이션 스켈레톤) | coder | agent | TODO | MEDIUM | TASK-021 | 2026-04-22 | 2026-04-22 |
| TASK-023 | core/audio/audio_service.dart (just_audio + just_audio_background 래퍼) | coder | agent | TODO | HIGH | TASK-001 | 2026-04-22 | 2026-04-22 |
| TASK-024 | core/connectivity/connectivity_service.dart (connectivity_plus 래퍼) | coder | agent | TODO | MEDIUM | TASK-001 | 2026-04-22 | 2026-04-22 |
| TASK-025 | core/sync/sync_engine.dart (LWW 동기화 스켈레톤) | coder | agent | TODO | MEDIUM | TASK-020,TASK-021,TASK-024 | 2026-04-22 | 2026-04-22 |
| TASK-026 | core/ 단위테스트 (dio 인터셉터·drift 쿼리·sync 엔진 mock) | tester | agent | TODO | HIGH | TASK-020,TASK-021,TASK-025 | 2026-04-22 | 2026-04-22 |
| --- | **Phase 3: Feature - Episode List** | --- | --- | --- | --- | --- | --- | --- |
| TASK-030 | features/episode_list/domain (Entity, Repository 인터페이스, UseCase) | coder | agent | TODO | HIGH | TASK-004 | 2026-04-22 | 2026-04-22 |
| TASK-031 | features/episode_list/data (Repository 구현, remote/local DataSource) | coder | agent | TODO | HIGH | TASK-020,TASK-021,TASK-030 | 2026-04-22 | 2026-04-22 |
| TASK-032 | features/episode_list/presentation (Screen, EpisodeCard, Download badge) | app-porter | agent | TODO | HIGH | TASK-006,TASK-030 | 2026-04-22 | 2026-04-22 |
| TASK-033 | episode_list 단위·위젯 테스트 | tester | agent | TODO | HIGH | TASK-031,TASK-032 | 2026-04-22 | 2026-04-22 |
| --- | **Phase 4: Feature - Episode Detail** | --- | --- | --- | --- | --- | --- | --- |
| TASK-040 | features/episode_detail/domain (Entity+문장 리스트, UseCase) | coder | agent | TODO | HIGH | TASK-030 | 2026-04-22 | 2026-04-22 |
| TASK-041 | features/episode_detail/data (Repository 구현) | coder | agent | TODO | HIGH | TASK-040,TASK-031 | 2026-04-22 | 2026-04-22 |
| TASK-042 | features/episode_detail/presentation (Screen, 다운로드 버튼, 재생 진입) | app-porter | agent | TODO | HIGH | TASK-006,TASK-040 | 2026-04-22 | 2026-04-22 |
| TASK-043 | episode_detail 테스트 | tester | agent | TODO | HIGH | TASK-041,TASK-042 | 2026-04-22 | 2026-04-22 |
| --- | **Phase 5: Feature - Player (핵심)** | --- | --- | --- | --- | --- | --- | --- |
| TASK-050 | features/player/domain (PlaybackState Entity, UseCase) | coder | agent | TODO | HIGH | TASK-040 | 2026-04-22 | 2026-04-22 |
| TASK-051 | features/player/data (audio_service 연동, 스트리밍/로컬 소스 분기) | coder | agent | TODO | HIGH | TASK-023,TASK-050 | 2026-04-22 | 2026-04-22 |
| TASK-052 | features/player/presentation Screen 골격 (컨트롤바, 시크바, AppBar) | app-porter | agent | TODO | HIGH | TASK-006,TASK-050 | 2026-04-22 | 2026-04-22 |
| TASK-053 | features/player/presentation 스크립트 동기화·토글·탭점프 (positionStream 구독, binary search, auto scroll) | app-porter | agent | TODO | HIGH | TASK-052 | 2026-04-22 | 2026-04-22 |
| TASK-054 | 단어 롱프레스 → 사전 조회 + 단어장 추가 모달 (SentenceTile 확장) | app-porter | agent | TODO | MEDIUM | TASK-053,TASK-060 | 2026-04-22 | 2026-04-22 |
| TASK-055 | 백그라운드 재생 스모크 (실기기 락스크린 컨트롤 확인) | user | user | TODO | HIGH | TASK-051,TASK-053 | 2026-04-22 | 2026-04-22 |
| TASK-056 | player 테스트 (상태 전이, 스크립트 index 계산, 위젯) | tester | agent | TODO | HIGH | TASK-053 | 2026-04-22 | 2026-04-22 |
| --- | **Phase 6: Feature - Notebook** | --- | --- | --- | --- | --- | --- | --- |
| TASK-060 | features/notebook/domain (Entity, UseCase, PendingSync) | coder | agent | TODO | HIGH | TASK-004 | 2026-04-22 | 2026-04-22 |
| TASK-061 | features/notebook/data (Repository, 오프라인 큐잉) | coder | agent | TODO | HIGH | TASK-020,TASK-021,TASK-060 | 2026-04-22 | 2026-04-22 |
| TASK-062 | features/notebook/presentation (목록, 상세, 추가 모달, 편집) | app-porter | agent | TODO | HIGH | TASK-006,TASK-060 | 2026-04-22 | 2026-04-22 |
| TASK-063 | 오프라인 "나중에 채움" 배치 조회 (온라인 복귀 시 null 뜻 보충) | coder | agent | TODO | MEDIUM | TASK-025,TASK-061 | 2026-04-22 | 2026-04-22 |
| TASK-064 | notebook 테스트 (CRUD, sync, 오프라인 큐) | tester | agent | TODO | HIGH | TASK-061,TASK-063 | 2026-04-22 | 2026-04-22 |
| --- | **Phase 7: 빌드·통합 스모크** | --- | --- | --- | --- | --- | --- | --- |
| TASK-070 | 통합 테스트 (integration_test/): 에피소드 목록 → 상세 → 재생 → 단어 추가 시나리오 | tester | agent | TODO | HIGH | TASK-053,TASK-062 | 2026-04-22 | 2026-04-22 |
| TASK-071 | Android APK 빌드 (debug keystore) | user | user | TODO | HIGH | TASK-070 | 2026-04-22 | 2026-04-22 |
| TASK-072 | 실기기 스모크 (목록·재생·오프라인 다운로드·단어장 종단 확인) | user | user | TODO | HIGH | TASK-071 | 2026-04-22 | 2026-04-22 |
