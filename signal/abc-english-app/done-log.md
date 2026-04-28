# Done Log

### TASK-071 (DONE) - 2026-04-23T08:56
- title: Android APK 빌드 (debug keystore)
- assignee: manager (user 요청으로 agent 실행)
- summary: `flutter build apk --debug` 성공 → `build/app/outputs/flutter-apk/app-debug.apk` (152 MB). Gradle `assembleDebug` 434.9s, 첫 빌드에서 NDK 28.2.13676358 + Build-Tools 35.0.0 + Platform android-35 자동 설치/라이선스 수락 수행. dart-define 3종은 dev 기본값 사용: `ABC_API_BASE_URL=http://10.0.2.2:8000`, `ABC_API_TOKEN=dev-token`, `ABC_ENV=dev`. Release 빌드나 실 백엔드 연결용 값이 필요하면 재빌드 필요.
- artifact:
  - path: `projects/abc-english-app/build/app/outputs/flutter-apk/app-debug.apk`
  - size: 152 MB
  - sha256: `ae4ea086eb41eaefc72f25aa882d7c43ec5c708466a79d65c7807adeea488fff`
- build_env:
  - flutter: 3.41.7 stable (Dart 3.11.5)
  - android_sdk: `/opt/android-sdk` (platform 35, build-tools 35.0.0, NDK 28.2.13676358)
  - jdk: 17 (setup.sh 설치)
  - host: Ubuntu 22.04.5 LTS
- observations:
  - **(observation) 첫 빌드 시간 7분 소요**: NDK 28.2/Build-Tools 35/Platform 35 온디맨드 설치가 원인. 재빌드는 Gradle 캐시 유효 시 1분 내 예상.
  - **(observation) dart-define 기본값은 실행 불가**: 앱 부팅 시 `AppConfig.fromEnvironment()` 가 `http://10.0.2.2:8000` 으로 dio 초기화 — 실기기(physical device)에서는 Android 에뮬레이터 host-loopback 이 아니므로 네트워크 호출이 즉시 실패. 실기기 테스트는 LAN IP(`http://<host-LAN-IP>:8000`)로 재빌드 필요. `ABC_API_TOKEN` 도 abc-english FastAPI `.env` 의 `API_TOKEN` 과 일치해야 함.
  - **(observation) debug keystore 서명**: Flutter 기본 debug keystore(`~/.android/debug.keystore`) 자동 사용. 배포용 AAB 가 필요하면 별도 release keystore + `android/key.properties` 세팅 후 `flutter build appbundle --release` 사용.

### TASK-070 (DONE) - 2026-04-22T13:30
- title: 통합 테스트 integration_test/ — 에피소드 목록 → 상세 → 재생 → 단어 추가 E2E
- assignee: tester
- summary: `integration_test/app_e2e_test.dart` (594L) 신규 — 2 시나리오(목록 smoke + 전체 흐름 E2E). Repository/Service 레벨 Riverpod override 로 외부 의존(Dio/drift/just_audio/connectivity_plus) 스텁. `flutter test -d flutter-tester integration_test/app_e2e_test.dart` → 2/2 PASS, `flutter test` 전체 170/170 유지 → 합계 172/172. `lib/` 미수정.
- files:
  - projects/abc-english-app/integration_test/app_e2e_test.dart (신규)
  - projects/abc-english-app/pubspec.yaml (dev_dependencies: integration_test)
- scenario_coverage:
  - ProviderScope + AbcApp 부팅 → Episodes 탭 3 EpisodeCard 렌더 (smoke)
  - 목록 탭 → /episodes/ep-001 → Transcript + episode-detail-play-button
  - 재생 버튼 → /player/ep-001, loadEpisode 1회 호출
  - player-sentence-2 탭 → seek(5000ms) (문장 start 타임스탬프)
  - player-sentence-1 안 test_word long-press → lookup bottom sheet → "단어장에 추가" → NotebookRepository.add(word=test_word, episodeId=ep-001, sentenceIndex=1), SnackBar 확인
  - Notebook 탭 진입 → NotebookEntryTile(test_word) 렌더
- manager_notes:
  - (observation) integration_test 실행 커맨드 `-d flutter-tester` + `--dart-define=ABC_API_BASE_URL=...` 필요 — README/CI 고정 대상. retrospective 이월.
  - (observation) `notebookAutoSyncTriggerProvider` 가 scope mount 시점에 구독 시작 → 초기 online 전환에서 `StorageException` swallow 되어 `notebook.sync.failed` 로그 노이즈. 테스트 결과 영향 없음. retrospective 이월 (lazy trigger 옵션).
  - (observation) 2 시나리오 ~7s. 시나리오 증가 시 `flutter_tester` 부팅 오버헤드 고려 필요.
- pending_user_tasks: TASK-055 (백그라운드 재생 스모크), TASK-071 (APK 빌드), TASK-072 (실기기 종단 스모크) — Execution=user

### TASK-054-FIX (DONE) - 2026-04-22T13:30
- title: lookup_bottom_sheet.dart 이동 (→ lib/shared/presentation) + notebook 연결 콜백화 — features 간 직접 import 제거
- assignee: coder
- summary: `lookup_bottom_sheet.dart` 를 `features/player/presentation/widgets/` → `lib/shared/presentation/widgets/` 로 이동. `OnAddToNotebook = Future<bool> Function({required word, required context, episodeId?, sentenceIndex?, meaning?, note?})` typedef 신설, 생성자/`show(...)` 에 `required onAddToNotebook` 추가. `player_screen.dart` 가 `_addLookupWordToNotebook` 브릿지 메서드로 notebook repository + AddNotebookEntry usecase 를 실행해 `bool` 반환. `flutter analyze` clean, `flutter test` 170/170 PASS.
- files:
  - 신규: projects/abc-english-app/lib/shared/presentation/widgets/lookup_bottom_sheet.dart
  - 신규: projects/abc-english-app/test/shared/presentation/lookup_bottom_sheet_test.dart
  - 삭제: projects/abc-english-app/lib/features/player/presentation/widgets/lookup_bottom_sheet.dart
  - 삭제: projects/abc-english-app/test/features/player/presentation/lookup_bottom_sheet_test.dart
  - 수정: projects/abc-english-app/lib/features/player/presentation/player_screen.dart (import 교체 + `_addLookupWordToNotebook` 신규)
- public_signatures:
  - `typedef OnAddToNotebook = Future<bool> Function({required String word, required String context, String? episodeId, int? sentenceIndex, String? meaning, String? note})`
  - `LookupBottomSheet({..., required OnAddToNotebook onAddToNotebook})` + `LookupBottomSheet.show({..., required OnAddToNotebook onAddToNotebook})`
- manager_notes:
  - architecture.md 레이어 규칙 예외 섹션 추가 — "host feature 가 sibling feature 의 domain 을 진입점으로 소비" 경로만 승인, 그 외는 금지. 승격 기준: notebook add 호출자가 player 외 2곳 이상이면 `core/ports/notebook_entry_point.dart` port 로 전환.
  - `lookup_bottom_sheet` 은 shared 에 위치하지만 `lookupRepositoryProvider` 는 직접 read — 단일 feature 의 domain entry 참조로 규칙 내. 복수 feature 패턴 발생 시 재검토.

### TASK-063 (DONE) - 2026-04-22T13:10
- title: notebook 오프라인 큐 drain — sync_engine 연결 + /api/v1/notebook/sync 배치 + deletedAt tombstone 마이그레이션 v2
- assignee: coder
- summary: drift schema v1→v2 `NotebookEntries.deletedAt` tombstone 추가, onUpgrade 에서 컬럼 add. NotebookSyncService 신규 — `/notebook/sync` 배치 upsert/delete + `/notebook?since_modified` 증분 pull, LWW(applied/server_wins/not_found/error) per-change 처리. NotebookAutoSyncTrigger 가 onlineStream 구독해 offline→online 전환 시 자동 drain. NotebookEntry → SyncableEntity implements (freezed 자동 생성 getter). `AbcApp` ConsumerWidget 전환. 57/57 notebook+core PASS.
- files:
  - projects/abc-english-app/lib/core/storage/app_database.dart (v2 migration, deletedAt)
  - projects/abc-english-app/lib/core/storage/migrations.dart (schemaVersion=2, onUpgrade)
  - projects/abc-english-app/lib/features/notebook/data/sync/notebook_sync_service.dart (신규)
  - projects/abc-english-app/lib/features/notebook/data/sync/notebook_auto_sync_trigger.dart (신규)
  - projects/abc-english-app/lib/features/notebook/data/datasources/notebook_local_datasource.dart (+getPending/markDeleted/hardDelete, getAll 에 tombstone 제외)
  - projects/abc-english-app/lib/features/notebook/data/datasources/notebook_remote_datasource.dart (+syncBatch + NotebookSyncChange/Result/Status types)
  - projects/abc-english-app/lib/features/notebook/data/repositories/notebook_repository_impl.dart (offline remove → tombstone)
  - projects/abc-english-app/lib/features/notebook/domain/entities/notebook_entry.dart (implements SyncableEntity)
  - projects/abc-english-app/lib/app.dart (ConsumerWidget + trigger mount)
  - test/core/storage_test.dart, test/features/notebook/notebook_repository_test.dart (minimal adapt: schemaVersion=2, tombstone semantics)
- manager_notes:
  - `_lastSyncAt` 인메모리 only — cold start 시 full resync. persistent storage 는 향후 태스크 대상.
  - AutoSyncTrigger 가 initial connectivity emit 를 online transition 으로 간주 → 앱 시작 시 drain 실행.
  - NotebookSyncService 를 위한 전용 단위테스트는 Tester 후속 태스크 대상.

### TASK-056 (DONE) - 2026-04-22T13:10
- title: Phase 5 player 테스트
- assignee: tester
- summary: 67 신규 테스트. 총 170/170 PASS. domain(9+8), data(10+19), presentation(8+4+5+4) 커버. mocktail 의 `captureAny(named:)` 한계 때문에 hand-written `_SpyAudio`/`_SpyDs` 스파이 클래스 사용. PlayerException→NetworkException(statusCode), PlatformException→UnknownException 매핑 검증. lookup_bottom_sheet 은 mock override 로 통과.
- files:
  - projects/abc-english-app/test/features/player/domain/{compute_current_sentence_index_test.dart, usecases_test.dart} (신규)
  - projects/abc-english-app/test/features/player/data/{player_audio_datasource_test.dart, player_repository_impl_test.dart} (신규)
  - projects/abc-english-app/test/features/player/presentation/{player_screen_test.dart, player_seek_bar_test.dart, player_sentence_tile_test.dart, lookup_bottom_sheet_test.dart} (신규)
- findings:
  - **observation**: `lib/features/player/presentation/widgets/lookup_bottom_sheet.dart:5-9` 이 `features/lookup/` + `features/notebook/` 를 cross-import. architecture.md 의 "features 간 직접 의존 금지" 위반. 이전 App Porter 보고에서도 언급. → retrospective 이월 or 별도 태스크 후보.
  - **observation**: `PlayerAudioDataSource` concrete class — abstract 인터페이스 추출하면 테스트 간편.

### TASK-033, 043, 064, 050-FIX, 026-OBS (DONE) - 2026-04-22T12:35
- title: Phase 3/4/6 feature 테스트 + core FIX batch 검증
- assignee: coder + tester (병렬)
- summary: Coder FIX batch 는 이전 한도 도달 전 이미 디스크에 반영 완료 상태였음(이번 세션이 재확인). AudioService.setSource 새 시그니처: `{required String? url, String? localPath, required MediaItem metadata, Map<String, String>? headers}` → just_audio `AudioSource.uri(headers: ...)` 포워딩, streaming 때 Bearer 자동 주입. dio_client retry 는 `_wrapAsAppException` (L106, max-retry 시 원본 type 보존) + `_preserveOrWrap` (L130, 중첩 AppException 재사용) + `_errorMappingInterceptor` (L141-144, pass-through) 조합. `episode_detail_local_datasource.dart` unnecessary_import 정리됨. Tester 는 3 feature × (repository+DTO+widget) = 72 new tests 추가 → 전체 103/103 PASS, `flutter analyze` clean.
- files:
  - projects/abc-english-app/lib/core/audio/audio_service.dart (시그니처 확장)
  - projects/abc-english-app/lib/core/network/dio_client.dart (retry type 보존)
  - projects/abc-english-app/lib/features/player/data/datasources/player_audio_datasource.dart (Bearer 주입)
  - projects/abc-english-app/test/core/audio_test.dart (new param 대응 adapt)
  - projects/abc-english-app/test/features/episode_list/* (신규 5파일)
  - projects/abc-english-app/test/features/episode_detail/* (신규 2파일)
  - projects/abc-english-app/test/features/notebook/* (신규 1파일 + helper rename)
- public_signatures:
  - `AudioService.setSource({required String? url, String? localPath, required MediaItem metadata, Map<String, String>? headers})`
- manager_notes:
  - Tester observation: presentation 이 Riverpod provider 심볼 때문에 `data/repositories/*_impl.dart` 를 직접 import — 관용적. 후속 리팩터 대상으로 retrospective 이월.
  - 병렬 세션 이슈 1건: notebook_repository_test.dart `_repo`→`makeRepo` 리네임이 두 에이전트 사이에서 발생 — 최종 상태 PASS 이므로 문제 없음. retrospective 에 다중 세션 concurrency 위험 기록 예정.

### TASK-032, 042, 062 (DONE) - 2026-04-22T11:45
- title: Phase 3 / 4 / 6 presentation (episode list / episode detail / notebook)
- assignee: app-porter
- summary: 3 screens + 5 widgets 신규. 3 placeholder 삭제. `app_router.dart` placeholder 교체. Seed color 실측: `projects/abc-english/web/static/css/app.css` L47 `#1F6FEB` (light), L13 `#5AA9FF` (dark). `app_theme.dart` seed `0xFF4A6CF7` → `0xFF1F6FEB`. `flutter analyze` → No issues. build_runner 12 outputs 성공. Riverpod presentation 은 codegen 없이 `Provider` / `AsyncNotifierProvider.autoDispose` 순수 사용.
- files:
  - projects/abc-english-app/lib/features/episode_list/presentation/{screen + 2 widgets} (신규)
  - projects/abc-english-app/lib/features/episode_detail/presentation/{screen + 1 widget} (신규)
  - projects/abc-english-app/lib/features/notebook/presentation/{screen + 3 widgets} (신규)
  - projects/abc-english-app/lib/features/{episode_list,episode_detail,notebook}/presentation/*_placeholder.dart (삭제, 3 파일)
  - projects/abc-english-app/lib/core/theme/app_theme.dart (seed color 교체)
  - projects/abc-english-app/lib/core/routing/app_router.dart (placeholder → screen 교체)
- manager_notes:
  - episode_detail_local_datasource.dart:4 에 `unnecessary_import` 1줄 — TASK-050-FIX 에 끼워 정리 예정.
  - presentation 의 episode 검색은 pagination 와 충돌해 의도적으로 미구현. 전체 search 는 backend page 파라미터 확장 필요 (향후).
  - 태블릿 2열 그리드 MVP 밖.
  - notebook episode 필터는 id 기반 — title lookup 은 feature cross-dep 유발로 보류.

### TASK-050, 051 (DONE) - 2026-04-22T11:45
- title: Phase 5 Player domain + data
- assignee: coder
- summary: 10 신규 Dart + 3 freezed 생성물. PlaybackState/PlaybackSource(freezed union) + `computeCurrentSentenceIndex` pure 이진탐색 + PlayerRepository 인터페이스 + 4 UseCase + AudioService 래핑 datasource + Repository impl + `playerRepositoryProvider`. **Sentence entity 승격**: `lib/features/episode_detail/domain/entities/sentence.dart` → `lib/core/domain/entities/sentence.dart`. 기존 호출부 호환 위해 episode_detail.dart 에서 re-export. `flutter analyze` → No issues.
- files:
  - projects/abc-english-app/lib/features/player/domain/{entities,utils,repositories,usecases}/ (신규)
  - projects/abc-english-app/lib/features/player/data/{datasources,repositories}/ (신규)
  - projects/abc-english-app/lib/core/domain/entities/sentence.dart (이동, 신규 파일)
  - projects/abc-english-app/lib/features/episode_detail/domain/entities/sentence.dart (삭제 + re-export 유지를 위한 episode_detail.dart 경로 조정)
- blocker:
  - **TASK-050-FIX 필요**: streaming URL `/api/v1/episodes/{id}/audio` 는 Bearer 인증. `AudioService.setSource` 에 headers 파라미터 없어 401. 해결안: AudioService 에 `Map<String,String>? headers` 추가 + `AudioSource.uri(headers: ...)` 전달. datasource 에서 Bearer 주입.

### TASK-030, 031, 040, 041, 060, 061 (DONE) - 2026-04-22T11:30
- title: Phase 3 / 4 / 6 — episode_list + episode_detail + notebook domain & data 레이어
- assignee: coder
- summary: 6개 태스크 전부 완료. **Episode entity 는 core/domain 승격** (기존 feature 내 파일 없었으므로 이동이 아닌 신규 생성). feature 간 DTO 교차 import 없음 — episode_detail 은 자기 DTO 에서 base field 중복 매핑 유지. Repository 는 online-first + local fallback (listEpisodes merge, getDetail isDownloaded 우선), notebook 은 local-first + online 즉시 push or pendingUpsert. DioException/drift 예외는 datasource 에서 잡고 AppException 변환 후 Failure 반환. 9 Riverpod providers 완성(3 per feature). `flutter analyze` clean, `build_runner build` 성공 (85 + 32 outputs).
- files:
  - projects/abc-english-app/lib/core/domain/entities/episode.dart (신규)
  - projects/abc-english-app/lib/features/episode_list/domain/{entities,repositories,usecases}/ (신규 3 파일 + freezed 생성물)
  - projects/abc-english-app/lib/features/episode_list/data/{datasources,models,repositories,providers}/ (신규 6 파일 + json_serializable 생성물)
  - projects/abc-english-app/lib/features/episode_detail/domain/ (신규, Sentence entity 포함)
  - projects/abc-english-app/lib/features/episode_detail/data/ (신규)
  - projects/abc-english-app/lib/features/notebook/domain/ (신규, SyncStatus enum 포함)
  - projects/abc-english-app/lib/features/notebook/data/ (신규)
- public_repo_signatures:
  - `EpisodeRepository.listEpisodes({int page, int size, DateTime? sinceModified}) → Future<Result<List<Episode>>>`
  - `EpisodeRepository.getById(String id) → Future<Result<Episode>>`
  - `EpisodeDetailRepository.getDetail(String id) → Future<Result<EpisodeDetail>>`
  - `NotebookRepository.list({DateTime? sinceModified}) → Future<Result<List<NotebookEntry>>>`
  - `NotebookRepository.add(...)`, `update(...)`, `remove(String id)`
- manager_notes:
  - notebook offline pending entries 는 자동 drain 미구현 — Phase 6 후반 TASK-063 에서 sync_engine 연결 예정.
  - isDownloaded/audioLocalPath/downloadedAt 쓰기 경로는 이 태스크 범위 아님. Phase 5 player 또는 별도 download 기능에서 처리.
  - tombstone 컬럼(offline-delete)은 향후 migration 대상.

### TASK-026 (DONE) - 2026-04-22T11:10
- title: core/ 단위테스트
- assignee: tester
- summary: test/core/{network,storage,audio,connectivity,sync}_test.dart 5파일. 31/31 PASS. dio 인터셉터(401/403/404/400/422 매핑, 5xx retry×3, 500→200 recovery), drift in-memory round-trip + 온디스크 `index`/`text` 컬럼명 raw query 확인, connectivity transition emit dedupe, sync LWW(server/local wins + error wrapping). `flutter analyze` clean.
- files:
  - projects/abc-english-app/test/core/network_test.dart (신규)
  - projects/abc-english-app/test/core/storage_test.dart (신규)
  - projects/abc-english-app/test/core/audio_test.dart (신규)
  - projects/abc-english-app/test/core/connectivity_test.dart (신규)
  - projects/abc-english-app/test/core/sync_test.dart (신규)
  - projects/abc-english-app/pubspec.yaml (+sqlite3 ^2.9.4 dev dep — Linux test loader 용)
- findings:
  - **observation**: dio retry 후 connectionTimeout 원본 type 이 `_dio.fetch(options)` 재진입 중 reset 되어 errorMapping 이 UnknownException 으로 떨어뜨림. 5xx 경로는 정상 NetworkException. → TASK-026-OBS 로 등록 (인터셉터 순서 교체 or type 보존).

### TASK-020..TASK-025 (DONE) - 2026-04-22T10:50
- title: Phase 2 — Core 레이어 (dio 네트워크 / drift 스토리지 / audio / connectivity / sync)
- assignee: coder
- summary: 6개 모듈 전부 신규. dio_client 4단계 인터셉터(auth→logging→retry→error-mapping), 재시도는 timeout/connection/5xx 에만 exponential backoff 300ms × 2^(n-1) 최대 3회. drift 3테이블(episodes/sentences/notebook_entries) 정의 + build_runner codegen. sync_engine 제네릭 스켈레톤 (storage/network 직접 의존 없이 4개 콜백 DI, LWW, SyncResult sealed). `flutter analyze` → No issues.
- files:
  - projects/abc-english-app/lib/core/network/dio_client.dart (신규)
  - projects/abc-english-app/lib/core/storage/app_database.dart (신규)
  - projects/abc-english-app/lib/core/storage/app_database.g.dart (drift 생성물)
  - projects/abc-english-app/lib/core/storage/migrations.dart (신규)
  - projects/abc-english-app/lib/core/audio/audio_service.dart (신규)
  - projects/abc-english-app/lib/core/connectivity/connectivity_service.dart (신규)
  - projects/abc-english-app/lib/core/sync/sync_engine.dart (신규)
- manager_notes:
  - drift 컬럼명 충돌 해결: Dart getter `sentenceIndex`/`body` 로 rename, 온디스크 컬럼명은 스펙대로 `index`/`text` 보존. 데이터 계약 영향 없음.
  - audio_service 는 core 경계이므로 예외를 AppException 으로 변환하지 않고 상위 feature 에 raw 전달 — 설계 의도대로.

### TASK-001..TASK-009 (DONE) - 2026-04-22T10:32
- title: Phase 0 — Flutter 프로젝트 뼈대 + core 공통 모듈 + 라우팅 placeholder + 실행 편의 스크립트
- assignee: coder
- summary: `flutter create --org com.abcenglish --project-name abc_english_app --platforms android` 로 Android 전용 스캐폴딩. lib/core/{config,errors,logging,theme,routing} 전부 구현, features/{episode_list,episode_detail,player,notebook,settings}/presentation placeholder 배치. pubspec 22개 의존성 해소 (Riverpod 2.6.1 고정, drift_flutter 없어 drift + sqlite3_flutter_libs ^0.5.24로 대체). Android manifest에 INTERNET/FOREGROUND_SERVICE_MEDIA_PLAYBACK/WAKE_LOCK + com.ryanheise.audioservice.AudioService + MediaButtonReceiver 선언. `flutter pub get` + `flutter analyze` 모두 PASS (No issues found).
- files:
  - projects/abc-english-app/lib/app.dart (신규)
  - projects/abc-english-app/lib/main.dart (재작성)
  - projects/abc-english-app/lib/core/config/app_config.dart (신규)
  - projects/abc-english-app/lib/core/errors/app_exception.dart (신규)
  - projects/abc-english-app/lib/core/errors/result.dart (신규)
  - projects/abc-english-app/lib/core/logging/app_logger.dart (신규)
  - projects/abc-english-app/lib/core/theme/app_theme.dart (신규)
  - projects/abc-english-app/lib/core/theme/break_points.dart (신규)
  - projects/abc-english-app/lib/core/routing/app_router.dart (신규)
  - projects/abc-english-app/lib/features/{episode_list,episode_detail,player,notebook,settings}/presentation/*_placeholder.dart (5개 신규)
  - projects/abc-english-app/scripts/run_dev.sh (신규, 755)
  - projects/abc-english-app/pubspec.yaml (수정)
  - projects/abc-english-app/android/app/src/main/AndroidManifest.xml (수정)
  - projects/abc-english-app/test/widget_test.dart (삭제 — 스캐폴드 기본값, 제거된 MyApp 참조로 analyze/build 실패)
- manager_notes:
  - drift_flutter 대체 승인 (사양 허용 경로).
  - widget_test.dart 삭제 승인 (Coder 규칙의 tests/ 보호는 Tester 산출물 대상이며, flutter create 템플릿은 해당 없음).
  - 테마 seed(0xFF4A6CF7) 임시값 — Phase 3+ app-porter 단계에서 web/static 팔레트 기준 교체.
  - riverpod_generator 포함 승인 (riverpod_annotation 짝).
