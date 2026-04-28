# Task Board

| ID | Title | Assignee | Execution | Status | Priority | Depends On | Created | Updated |
|----|-------|----------|-----------|--------|----------|------------|---------|---------|
| --- | **Phase 0: 프로젝트 기반** | --- | --- | --- | --- | --- | --- | --- |
| TASK-001 | Flutter 프로젝트 스캐폴딩 (flutter create, pubspec.yaml 의존성 정의) | coder | agent | DONE | HIGH | - | 2026-04-22 | 2026-04-22T10:32 |
| TASK-002 | Android manifest 설정 (INTERNET, FOREGROUND_SERVICE, MediaSession) | coder | agent | DONE | HIGH | TASK-001 | 2026-04-22 | 2026-04-22T10:32 |
| TASK-003 | core/config/app_config.dart (--dart-define 환경변수 읽기) | coder | agent | DONE | HIGH | TASK-001 | 2026-04-22 | 2026-04-22T10:32 |
| TASK-004 | core/errors/app_exception.dart + core/result.dart (sealed Result 타입) | coder | agent | DONE | HIGH | TASK-001 | 2026-04-22 | 2026-04-22T10:32 |
| TASK-005 | core/logging/app_logger.dart (logger 라이브러리 래퍼, 릴리스 레벨 분기) | coder | agent | DONE | MEDIUM | TASK-001 | 2026-04-22 | 2026-04-22T10:32 |
| TASK-006 | core/theme/app_theme.dart (Material 3 라이트·다크 테마, BreakPoints) | coder | agent | DONE | MEDIUM | TASK-001 | 2026-04-22 | 2026-04-22T10:32 |
| TASK-007 | main.dart + app.dart (Riverpod ProviderScope, MaterialApp.router, 전역 에러 바운더리) | coder | agent | DONE | HIGH | TASK-003,TASK-006 | 2026-04-22 | 2026-04-22T10:32 |
| TASK-008 | go_router 라우팅 설정 (tab shell + detail 라우트 placeholder) | coder | agent | DONE | HIGH | TASK-007 | 2026-04-22 | 2026-04-22T10:32 |
| TASK-009 | scripts/run_dev.sh 실행 편의 스크립트 | coder | agent | DONE | LOW | TASK-003 | 2026-04-22 | 2026-04-22T10:32 |
| --- | **Phase 1: 백엔드 /api/v1/ 지원** — 별도 프로젝트 `abc-english`의 TASK-100~108에서 구현. 이 보드에는 의존성 핸드오프 마커만 유지. | --- | --- | --- | --- | --- | --- | --- |
| TASK-HANDOFF-BACKEND | abc-english 프로젝트 Phase 10 (TASK-100~108) 완료 확인 — 앱 클라이언트가 /api/v1/ 호출 가능해야 함 | manager | agent | TODO | HIGH | - | 2026-04-22 | 2026-04-22 |
| --- | **Phase 2: Core 레이어** | --- | --- | --- | --- | --- | --- | --- |
| TASK-020 | core/network/dio_client.dart (Bearer 인터셉터, 재시도, 타임아웃) | coder | agent | DONE | HIGH | TASK-003,TASK-004 | 2026-04-22 | 2026-04-22T10:50 |
| TASK-021 | core/storage/app_database.dart (drift 정의, episodes/sentences/notebook 테이블) | coder | agent | DONE | HIGH | TASK-001 | 2026-04-22 | 2026-04-22T10:50 |
| TASK-022 | core/storage/migrations.dart (drift 마이그레이션 스켈레톤) | coder | agent | DONE | MEDIUM | TASK-021 | 2026-04-22 | 2026-04-22T10:50 |
| TASK-023 | core/audio/audio_service.dart (just_audio + just_audio_background 래퍼) | coder | agent | DONE | HIGH | TASK-001 | 2026-04-22 | 2026-04-22T10:50 |
| TASK-024 | core/connectivity/connectivity_service.dart (connectivity_plus 래퍼) | coder | agent | DONE | MEDIUM | TASK-001 | 2026-04-22 | 2026-04-22T10:50 |
| TASK-025 | core/sync/sync_engine.dart (LWW 동기화 스켈레톤) | coder | agent | DONE | MEDIUM | TASK-020,TASK-021,TASK-024 | 2026-04-22 | 2026-04-22T10:50 |
| TASK-026 | core/ 단위테스트 (dio 인터셉터·drift 쿼리·sync 엔진 mock) | tester | agent | DONE | HIGH | TASK-020,TASK-021,TASK-025 | 2026-04-22 | 2026-04-22T11:10 |
| TASK-026-OBS | dio_client retry 후 connectionTimeout 이 UnknownException 으로 떨어지는 문제 — retry 와 errorMapping 인터셉터 순서 교체 또는 원본 type 보존 | coder | agent | DONE | MEDIUM | TASK-026 | 2026-04-22 | 2026-04-22T12:35 |
| --- | **Phase 3: Feature - Episode List** | --- | --- | --- | --- | --- | --- | --- |
| TASK-030 | features/episode_list/domain (Entity, Repository 인터페이스, UseCase) | coder | agent | DONE | HIGH | TASK-004 | 2026-04-22 | 2026-04-22T11:30 |
| TASK-031 | features/episode_list/data (Repository 구현, remote/local DataSource) | coder | agent | DONE | HIGH | TASK-020,TASK-021,TASK-030 | 2026-04-22 | 2026-04-22T11:30 |
| TASK-032 | features/episode_list/presentation (Screen, EpisodeCard, Download badge) | app-porter | agent | DONE | HIGH | TASK-006,TASK-030 | 2026-04-22 | 2026-04-22T11:45 |
| TASK-033 | episode_list 단위·위젯 테스트 | tester | agent | DONE | HIGH | TASK-031,TASK-032 | 2026-04-22 | 2026-04-22T12:35 |
| --- | **Phase 4: Feature - Episode Detail** | --- | --- | --- | --- | --- | --- | --- |
| TASK-040 | features/episode_detail/domain (Entity+문장 리스트, UseCase) | coder | agent | DONE | HIGH | TASK-030 | 2026-04-22 | 2026-04-22T11:30 |
| TASK-041 | features/episode_detail/data (Repository 구현) | coder | agent | DONE | HIGH | TASK-040,TASK-031 | 2026-04-22 | 2026-04-22T11:30 |
| TASK-042 | features/episode_detail/presentation (Screen, 다운로드 버튼, 재생 진입) | app-porter | agent | DONE | HIGH | TASK-006,TASK-040 | 2026-04-22 | 2026-04-22T11:45 |
| TASK-043 | episode_detail 테스트 | tester | agent | DONE | HIGH | TASK-041,TASK-042 | 2026-04-22 | 2026-04-22T12:35 |
| --- | **Phase 5: Feature - Player (핵심)** | --- | --- | --- | --- | --- | --- | --- |
| TASK-050 | features/player/domain (PlaybackState Entity, UseCase) | coder | agent | DONE | HIGH | TASK-040 | 2026-04-22 | 2026-04-22T11:45 |
| TASK-051 | features/player/data (audio_service 연동, 스트리밍/로컬 소스 분기) | coder | agent | DONE | HIGH | TASK-023,TASK-050 | 2026-04-22 | 2026-04-22T11:45 |
| TASK-050-FIX | core/audio/audio_service.dart 에 `Map<String,String>? headers` 파라미터 추가 — just_audio AudioSource.uri headers 로 포워딩. player_audio_datasource 에서 Bearer 주입해 스트리밍 401 해결 | coder | agent | DONE | HIGH | TASK-051 | 2026-04-22 | 2026-04-22T12:35 |
| TASK-052 | features/player/presentation Screen 골격 (컨트롤바, 시크바, AppBar) | app-porter | agent | DONE | HIGH | TASK-006,TASK-050 | 2026-04-22 | 2026-04-22T11:45 |
| TASK-053 | features/player/presentation 스크립트 동기화·토글·탭점프 (positionStream 구독, binary search, auto scroll) | app-porter | agent | DONE | HIGH | TASK-052 | 2026-04-22 | 2026-04-22T11:45 |
| TASK-054 | 단어 롱프레스 → 사전 조회 + 단어장 추가 모달 (SentenceTile 확장) | app-porter | agent | DONE | MEDIUM | TASK-053,TASK-060 | 2026-04-22 | 2026-04-22T11:45 |
| TASK-054-FIX | lookup_bottom_sheet.dart 이동 (→ lib/shared/presentation) + notebook 연결 콜백화 — features 간 직접 import 제거 | coder | agent | DONE | MEDIUM | TASK-054 | 2026-04-22 | 2026-04-22T13:30 |
| TASK-055 | 백그라운드 재생 스모크 (실기기 락스크린 컨트롤 확인) | user | user | TODO | HIGH | TASK-051,TASK-053 | 2026-04-22 | 2026-04-22 |
| TASK-056 | player 테스트 (상태 전이, 스크립트 index 계산, 위젯) | tester | agent | DONE | HIGH | TASK-053 | 2026-04-22 | 2026-04-22T13:10 |
| --- | **Phase 6: Feature - Notebook** | --- | --- | --- | --- | --- | --- | --- |
| TASK-060 | features/notebook/domain (Entity, UseCase, PendingSync) | coder | agent | DONE | HIGH | TASK-004 | 2026-04-22 | 2026-04-22T11:30 |
| TASK-061 | features/notebook/data (Repository, 오프라인 큐잉) | coder | agent | DONE | HIGH | TASK-020,TASK-021,TASK-060 | 2026-04-22 | 2026-04-22T11:30 |
| TASK-062 | features/notebook/presentation (목록, 상세, 추가 모달, 편집) | app-porter | agent | DONE | HIGH | TASK-006,TASK-060 | 2026-04-22 | 2026-04-22T11:45 |
| TASK-063 | 오프라인 큐 drain (sync_engine 연결, /api/v1/notebook/sync 배치, deletedAt tombstone v2) | coder | agent | DONE | MEDIUM | TASK-025,TASK-061 | 2026-04-22 | 2026-04-22T13:10 |
| TASK-064 | notebook 테스트 (CRUD, sync, 오프라인 큐) | tester | agent | DONE | HIGH | TASK-061,TASK-063 | 2026-04-22 | 2026-04-22T12:35 |
| --- | **Phase 7: 빌드·통합 스모크** | --- | --- | --- | --- | --- | --- | --- |
| TASK-070 | 통합 테스트 (integration_test/): 에피소드 목록 → 상세 → 재생 → 단어 추가 시나리오 | tester | agent | DONE | HIGH | TASK-053,TASK-062 | 2026-04-22 | 2026-04-22T13:30 |
| TASK-071 | Android APK 빌드 (debug keystore) | manager | agent | DONE | HIGH | TASK-070 | 2026-04-22 | 2026-04-23T08:56 |
| TASK-072 | 실기기 스모크 (목록·재생·오프라인 다운로드·단어장 종단 확인) | user | user | TODO | HIGH | TASK-071 | 2026-04-22 | 2026-04-22 |
