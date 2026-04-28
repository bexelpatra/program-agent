---
agent: tester
task_id: TASK-070
status: DONE
timestamp: 2026-04-22T13:10:00
severity: observation
---

## 결과 요약

TASK-070 요구사항에 따라 ABC English 앱의 end-to-end 통합 테스트를 작성하고 headless 실행을 확인했다. `integration_test/app_e2e_test.dart`에 2개 시나리오(에피소드 목록 렌더 smoke + 전체 E2E 흐름)를 구현했고 외부 의존(Dio/drift/just_audio/connectivity_plus)은 repository/service provider 수준의 Riverpod override로 스텁했다. 통합 2건 + 기존 unit/widget 170건 모두 PASS (172/172). `lib/` 수정 없음.

## 변경된 파일

- `projects/abc-english-app/integration_test/app_e2e_test.dart` (신규) — E2E 시나리오 2건, fake repository 5종(`_FakeEpisodeRepo`, `_FakeEpisodeDetailRepo`, `_FakeLookupRepo`, `_FakeNotebookRepo`, `_FakePlayerRepo`) + `_FakeConnectivityService`/`_StubConnectivity`, `PlayerSentenceTile`의 `RichText`에 걸린 `LongPressGestureRecognizer`를 직접 발화하는 `_longPressWordInSentence` 헬퍼 포함.
- `projects/abc-english-app/pubspec.yaml` (수정) — `dev_dependencies`에 `integration_test: sdk: flutter` 추가. (`flutter pub get` 성공, 기존 170개 테스트 실행에 영향 없음을 확인.)

`lib/` 하위 코드는 일절 수정하지 않았다.

## 테스트 결과

- 통과: 172 (unit/widget 170 + integration 2)
- 실패: 0
- 실행 커맨드 및 결과:
  - 통합: `flutter test -d flutter-tester integration_test/app_e2e_test.dart --no-pub --dart-define=ABC_API_BASE_URL=http://localhost:65535 --dart-define=ABC_API_TOKEN=stub-token` → `00:07 +2: All tests passed!`
  - 기존 suite: `flutter test --no-pub --dart-define=ABC_API_BASE_URL=http://localhost:65535 --dart-define=ABC_API_TOKEN=stub-token` → `00:08 +170: All tests passed!`

### 시나리오 커버리지 (E2E 2번째 테스트, 첫 번째는 smoke)

1. ProviderScope + `AbcApp` 부팅 시 Episodes 탭이 3개의 `EpisodeCard`를 렌더 (1번째 smoke 테스트에서 단언).
2. `Morning News Rundown` 탭 → `/episodes/ep-001` 라우팅, `Transcript` 헤더 + `episode-detail-play-button` 노출.
3. 재생 버튼 탭 → `/player/ep-001` 라우팅, fake `PlayerRepository.loadEpisode` 1회 호출 단언 (`loadCalls == 1`).
4. 3번째 문장 tile(`player-sentence-2`) 탭 → fake의 `seekCalls`에 `Duration(milliseconds: 5000)`(문장 start) 기록.
5. 1번째 문장(`player-sentence-1`) 안의 `test_word` 토큰 long-press → `Key('lookup-add-to-notebook')` 버튼이 보이는 lookup bottom sheet 노출. 전용 헬퍼로 해당 `TextSpan`의 `LongPressGestureRecognizer.onLongPress`를 직접 호출해 `flutter_test`에서도 재현 가능하게 처리.
6. `단어장에 추가` 탭 → fake `NotebookRepository.add` 호출 검증 (word=`test_word`, episodeId=`ep-001`, sentenceIndex=`1`). `단어장에 추가되었습니다` SnackBar 확인.
7. Notebook 탭 진입 → `NotebookEntryTile` 1개 렌더, `test_word` 가시.

### 의존성 스텁 전략

`connectivityServiceProvider`, `episodeRepositoryProvider`(FutureProvider), `episodeDetailRepositoryProvider`(FutureProvider), `lookupRepositoryProvider`, `notebookRepositoryProvider`(FutureProvider), `playerRepositoryProvider`를 `ProviderScope.overrides`로 치환. FutureProvider는 `overrideWith((ref) async => ...)`, Plain Provider는 `overrideWithValue(...)` 규칙을 준수. DioAdapter/in-memory drift를 쓰지 않는 repository-level DI 방식이 기존 170개 테스트가 이미 사용하던 훅이므로 스타일 일관성도 유지.

## 이슈/블로커

없음 (블로커 없음). 아래는 observation-level 관찰 사항:

- **(observation) 통합 테스트 실행 커맨드 문서화 필요**: 셸 환경에서 `flutter test integration_test/*.dart`는 디바이스 탐색 때문에 바로 실행되지 않고, `-d flutter-tester` 플래그 + `--dart-define=ABC_API_BASE_URL=...` 조합이 필요하다. `projects/abc-english-app/README.md`나 향후 CI 설정에 고정해 두면 재현성이 좋아진다.
- **(observation) auto_sync 경고 로그 노이즈**: `notebookAutoSyncTriggerProvider`가 scope mount 시점에 구독을 시작해 초기 online 전환 1회분 sync를 시도한다. 본 E2E는 `notebookRepositoryProvider`만 override했고 `notebookSyncServiceProvider`/`notebookRemoteDataSourceProvider`는 그대로 둬서 `notebook.sync.failed {reason: StorageException}` 로그가 찍힌다. 코드상 try/catch로 완전 swallow 되어 테스트 결과에는 영향이 없다. 노이즈가 거슬리면 별도 태스크로 `notebookAutoSyncTriggerProvider.overrideWith`(no-op trigger) 혹은 구독 지연(lazy) 옵션을 추가할 수 있음.
- **(observation) E2E 실행 시간**: 2개 시나리오가 약 7초 소요. 시나리오가 더 늘어나면 `flutter_tester` 부팅 오버헤드가 누적되므로, 필요 시 group 단위 `setUpAll`/`tearDownAll` 도입 또는 셸 단위 테스트로 일부 이동하는 것을 고려할 수 있음.

## 다음 제안

1. Manager: 본 태스크를 DONE 처리하고 done-log에 반영. `integration_test` 실행 커맨드(`-d flutter-tester` + `--dart-define=ABC_API_BASE_URL=...`)를 README/CI에 고정하는 태스크는 priority LOW observation 기반이므로 Manager 판단으로 태스크화 또는 retrospective 이월.
2. auto_sync 로그 노이즈는 observation이므로 Manager 판단에 따라 태스크화/retrospective 이월.
3. `lib/` 수정이 전혀 없어 clean architecture/레이어링에 영향 없음. Coder 후속 수정 없이 다음 feature 태스크로 진행 가능.
