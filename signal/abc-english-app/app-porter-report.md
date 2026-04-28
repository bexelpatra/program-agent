---
agent: app-porter
task_id: TASK-052, TASK-053, TASK-054
status: DONE
timestamp: 2026-04-22T14:30
---

## 결과 요약

Phase 5 Player presentation 레이어 3 태스크 완료.

- **TASK-052** (screen 골격): `PlayerScreen` + 컨트롤바 + 시크바 작성. `playerRepositoryProvider.stateStream` 을 `StreamProvider` 로 구독 (`playbackStateProvider`). 에피소드 상세는 `playerEpisodeProvider` (FutureProvider.family) 가 `EpisodeDetail` 을 로드하면서 부작용으로 `LoadEpisode` UseCase 까지 호출 — stateStream 이 즉시 emit 하기 시작하도록 연결.
- **TASK-053** (스크립트 동기화/토글/탭점프): `ListView.builder` + `PlayerSentenceTile` + `computeCurrentSentenceIndex` (이미 domain 에 존재) 로 현재 문장 하이라이트. `ScrollController.animateTo` 기반 auto-scroll. 사용자가 직접 스크롤하면 `userScrollDirection != idle` 감지 → 5초 타이머로 auto-scroll 일시 중지. 탭 = `JumpToSentence` UseCase → seek.
- **TASK-054** (단어 롱프레스 → 사전 조회 + 단어장 추가): `PlayerSentenceTile` 의 RichText 가 단어 단위 `TextSpan` + `LongPressGestureRecognizer` 로 구성. 롱프레스 → `LookupBottomSheet` → `/api/v1/lookup` 호출. 결과에서 "단어장에 추가" 버튼 → `AddNotebookEntry` UseCase.

`lookup` feature 는 이 태스크 한정 예외로 **domain + data 최소 골격**을 작성 (Manager 지시에 따름). `LookupResult` entity, `LookupRepository` interface, `LookupRepositoryImpl` (dio 기반), `LookupResultDto` 포함.

## 변경된 파일

### 신규 — Player presentation

- `projects/abc-english-app/lib/features/player/presentation/player_screen.dart` (신규)
- `projects/abc-english-app/lib/features/player/presentation/providers/player_providers.dart` (신규)
- `projects/abc-english-app/lib/features/player/presentation/widgets/player_control_bar.dart` (신규)
- `projects/abc-english-app/lib/features/player/presentation/widgets/player_seek_bar.dart` (신규)
- `projects/abc-english-app/lib/features/player/presentation/widgets/player_sentence_tile.dart` (신규)
- `projects/abc-english-app/lib/features/player/presentation/widgets/lookup_bottom_sheet.dart` (신규)

### 신규 — Lookup feature (예외 허용 범위)

- `projects/abc-english-app/lib/features/lookup/domain/entities/lookup_result.dart` (신규)
- `projects/abc-english-app/lib/features/lookup/domain/entities/lookup_result.freezed.dart` (build_runner 생성)
- `projects/abc-english-app/lib/features/lookup/domain/repositories/lookup_repository.dart` (신규)
- `projects/abc-english-app/lib/features/lookup/domain/usecases/lookup_word.dart` (신규)
- `projects/abc-english-app/lib/features/lookup/data/models/lookup_result_dto.dart` (신규)
- `projects/abc-english-app/lib/features/lookup/data/models/lookup_result_dto.freezed.dart` (build_runner 생성)
- `projects/abc-english-app/lib/features/lookup/data/models/lookup_result_dto.g.dart` (build_runner 생성)
- `projects/abc-english-app/lib/features/lookup/data/datasources/lookup_remote_datasource.dart` (신규)
- `projects/abc-english-app/lib/features/lookup/data/repositories/lookup_repository_impl.dart` (신규)

### 수정

- `projects/abc-english-app/lib/core/routing/app_router.dart` — `PlayerPlaceholder` import 를 `PlayerScreen` 으로 교체, `/player/:id` 빌더 교체.

### 삭제

- `projects/abc-english-app/lib/features/player/presentation/player_placeholder.dart` — `PlayerScreen` 이 대체.

## 웹→모바일 매핑 결정

| 웹 요소 (레퍼런스) | 모바일 매핑 | 근거 |
|-------------------|-------------|------|
| `<audio>` + custom `#btn-play`·`#seek` (study.html L32–42) | `PlayerControlBar` + `PlayerSeekBar` 분리. `FloatingActionButton.large` 72dp 로 엄지 접근성 확보 | 웹은 마우스 정밀 클릭, 모바일은 엄지 탭 → 대형 타겟 필요 |
| `-3s`/`+3s` 스킵 (study.html L56–60, 사용자가 1~30초 변경 가능) | 고정 ±15s 스킵 (TASK 지시) | MVP 는 설정 토글 스킵. localStorage 상당 기능은 Settings 으로 이월 |
| 배속 `<select>` (study.html L46–54) | **생략** (TASK 범위 외) | Manager 지시에 없으므로 다음 제안으로 이월. AudioService 에 setSpeed 이미 존재 |
| `<p class="sentence">` 리스트 + `data-idx` (study.html L83–86 · study.js L148–162) | `ListView.builder` + `PlayerSentenceTile` (Stateful — `LongPressGestureRecognizer` 관리) | 웹은 DOM 직접 querySelector, Flutter 는 builder 패턴 |
| `.sentence.active` 하이라이트 + `scrollIntoView({block:"center"})` (study.js L202–213) | `AnimatedContainer` 배경색 + `ScrollController.animateTo` (tile 높이 추정치 84dp 사용) | Flutter 의 ensureVisible 은 ListView.builder 에서 key 접근이 번거로워 offset 계산 선택 |
| 사용자 수동 스크롤 중 auto-scroll 억제 — 웹은 없음 (별도 UI 가이드 없음) | `userScrollDirection != idle` 감지 후 5초 타이머 (TASK 지시) | 모바일 터치 스크롤 충돌 방지 — 웹보다 중요 |
| `.sentence-time` 버튼 탭 → seek (study.js L280–289) | 전체 타일 `GestureDetector.onTap` → JumpToSentence UseCase | 타일 전체가 탭 타겟 (별도 ▶ 버튼 없이 Fitts's law 충족) |
| `.word` span 클릭 → lookup modal (study.js L512–520) | `TextSpan` + `LongPressGestureRecognizer` 로 **롱프레스** | 모바일에서 탭 = seek 과 충돌하므로 롱프레스로 이동 (TASK 지시) |
| drag-selection (1~6단어) → lookup bubble (study.js L522–549) | **생략** | Flutter SelectableText 선택 이벤트 훅이 복잡 — observation 으로 이월 |
| 우측 드로어 lookup modal (study.html L88–100, study.js L400–498) | `showModalBottomSheet` + `LookupBottomSheet` | 모바일은 사이드 드로어보다 바텀시트가 엄지 접근 유리 |
| 모달 헤더 "loading..." badge + spinner (study.js L408–422) | `FutureBuilder` 가 자동 로딩/에러 상태 분기 + `_LoadingView`/`_ErrorView` | Flutter 관례적 패턴 |
| 키보드 단축키 (space/←/→/↑/↓) (study.js L291–369) | **전부 생략** (터치 환경) | app-porter.md 매핑 표 원칙 "키보드 단축키 → 제거" |
| 백그라운드 재생 인디케이터 (웹에는 없음 — 탭 열려 있어야 재생) | 별도 UI 없음 (just_audio_background 알림창이 OS 레벨 제공) | Coder TASK-023 에서 처리, presentation 범위 외 |
| 401 오류 표시 (웹은 전역 toast) | `_PlaybackErrorBanner` 화면 상단 ErrorContainer + `_ErrorView` 전체 화면 (episode detail 로드 실패 시) | TASK 지시 "401 발생 시의 오류 화면도 표시" |

## 구현 세부 사항

### Riverpod 구조

```
playerEpisodeProvider (FutureProvider.autoDispose.family<EpisodeDetail, String>)
  ├─ episodeDetailRepositoryProvider (기존) 에서 EpisodeDetail 로드
  └─ 부작용: LoadEpisode(playerRepo)(detail) 호출 — stateStream 기동

playbackStateProvider (StreamProvider.autoDispose<PlaybackState>)
  └─ playerRepositoryProvider.stateStream 직접 구독

playPauseUseCaseProvider / seekToUseCaseProvider / jumpToSentenceUseCaseProvider
  └─ 각 UseCase 를 repository 주입하여 생성
```

`playerEpisodeProvider` 의 부작용(LoadEpisode)은 실패 시 rethrow 하지 않는다 — 사용자가 스크립트를 스크롤할 수 있도록 비치명적으로 처리하고, 실제 오류는 `PlaybackState.error` 스트림이 `_PlaybackErrorBanner` 로 표시한다. 즉 "데이터 로드 실패" 와 "재생 바인딩 실패" 는 독립적인 에러 채널.

### Auto-scroll 알고리즘

- `_lastScrolledIndex` 로 현재 index 변경 여부 추적.
- `addPostFrameCallback` 안에서 `ScrollController.animateTo(target)` 호출 (layout 완료 후 실행 보장).
- `target = (index * _approxItemHeight).clamp(0, maxScrollExtent)`.
- `_approxItemHeight = 84` — `PlayerSentenceTile` 패딩+텍스트 2줄+시간 범위 표시의 관측치 근사. 실제 텍스트 길이에 따라 변동하지만 ListView.builder 가 viewport 근처 tile 만 ensure 해주면 상단 정렬은 아님 — 최소 가시성은 보장.
- 사용자 수동 스크롤 감지 → 5초 timeout 후 auto-scroll 재개.
- 문장 tap → timeout 즉시 취소 (tap 자체가 사용자의 "여기로 가 달라" 신호이므로).

### 단어 토큰화

`web/static/js/study.js::tokenizeSentence` 로직을 Dart 로 이식:
- `RegExp(r'(\s+)')` 로 split.
- 비공백 토큰은 앞뒤 구두점(`^[^\p{L}\p{N}'\-]+|[^\p{L}\p{N}'\-]+$`) 제거.
- 정리된 소문자 `word` 가 롱프레스 콜백으로 전달됨.
- 공백/구두점만 있는 토큰은 리코그나이저 없이 표시 → 불필요한 제스처 인식기 생성 방지.

### LookupResult DTO → Entity 매핑 결정

태스크는 `LookupResult(word, phonetic?, definitions, examples)` 를 요구했지만, 백엔드 실제 응답 (`projects/abc-english/web/api/v1/lookup.py` → `src/ollama_client.py::LookupResult`) 은 `{term, term_type, explanation_en, etymology?, examples[]}`. 정합 방식:
- `term → word`
- `explanation_en → definitions: [explanation_en]` (단일 항목 리스트)
- `examples → examples` (1:1)
- `phonetic` 은 entity 에 `null` 로 유지 (백엔드 미지원) — 향후 LLM 프롬프트 확장 시 채움
- `term_type`, `etymology` 는 entity 에 보존 (modal 에서 표시)

## 실행 검증

- `flutter pub get`: OK.
- `dart run build_runner build --delete-conflicting-outputs`: 41 outputs written. lookup_result.freezed.dart, lookup_result_dto.freezed.dart, lookup_result_dto.g.dart 생성 확인.
- `flutter analyze lib/`: **No issues found!** (ran in 0.7s)
- `flutter analyze` 전체: 4 건의 pre-existing 경고 (tests 파일의 unnecessary_import / unused_element / no_leading_underscores) — 이번 작업과 무관. app-porter 금지 규정상 tests/ 수정 불가.

## 이슈/블로커

1. **TASK-050-FIX 미완 영향**: Coder 병렬 태스크가 완료되기 전까지 스트리밍 재생은 401 로 실패. 이 태스크는 UI 로직 구현에 집중했고 `_PlaybackErrorBanner` 가 401 을 사용자에게 안내. 실기기 스모크(TASK-055)는 TASK-050-FIX 완료 후 가능.
2. **API invariant 간 skew**: `LookupResult` entity 형태 (`definitions`, `phonetic`) 가 태스크 사양과 백엔드 응답 사이에서 타협했음 — Report "LookupResult DTO → Entity 매핑 결정" 섹션 참고. 백엔드를 변경할지 entity 를 좁힐지는 Manager 판단.
3. **lookup 레이어 완성도**: TASK 지시("data 레이어 skeleton 만, 복잡한 상황 분기는 스킵")에 따라 로컬 캐시/오프라인 큐잉 없음. 온라인에서만 동작. 오프라인 동안은 bottom sheet 의 `_ErrorView` 가 표시됨. TASK-063 (notebook "나중에 채움") 과 유사한 패턴을 lookup 에도 적용할지 Manager 결정 필요.

## 관찰 (observation)

- **lookup feature 는 domain+data 최소 골격만 완성**. presentation 진입이 lookup_bottom_sheet.dart 한 곳에 집중되어 있어서 향후 다른 화면(notebook 편집, 에피소드 상세)에서도 재사용 가능. Tester 가 lookup_repository_impl 단위 테스트를 작성할 때 `Dio` mock 또는 `DioAdapter` 패턴 사용 권장 (기존 `dio_client_test.dart` 참고).
- **auto-scroll `_approxItemHeight = 84`** 는 근사치. Tester 가 위젯 테스트에서 실제 렌더 높이를 관측해 상수를 조정할 여지 있음. 또는 `ListView.builder` 대신 `ScrollablePositionedList` 패키지 도입 검토 (향후).
- **재생 속도 (0.75x / 1.0x / 1.25x / 1.5x)** UI 미구현. architecture.md §player 요구사항에는 있으나 TASK-052/053/054 에는 명시 없음. Settings 탭 또는 player 하단 작은 chip 그룹으로 향후 추가 권장.
- **드래그-선택 기반 multi-word 조회** (웹의 1~6 단어 선택) 미구현. Flutter `SelectableText` + `onSelectionChanged` 로 구현 가능하지만 현재 `RichText` 기반 단어 롱프레스와 충돌 가능성 있음 — 설계 결정 필요.
- **API invariant**: `playerEpisodeProvider` 가 `LoadEpisode` 까지 호출하는 "loader 기반" 패턴을 사용 중. 제공자가 side-effectful인 점이 불편하다면 향후 `PlayerController` (`AsyncNotifier`) 로 리팩터 가능.

## 다음 제안

1. **TASK-056 (Tester)**: `PlayerControlBar` / `PlayerSeekBar` / `PlayerSentenceTile` 위젯 테스트, `LookupBottomSheet` FutureBuilder 상태 테스트(loading/error/success + add-to-notebook 콜백), `computeCurrentSentenceIndex` 는 이미 domain 에서 검증 가능. `lookup_repository_impl` 단위 테스트 (Dio mock) 도 Coder 또는 Tester 중 하나가 커버해야 함.
2. **TASK-050-FIX (Coder)**: 완료 후 TASK-055 (user 실기기 스모크) 실행 → 실제 스트리밍 + 락스크린 컨트롤 확인.
3. **향후 TASK**: 재생 속도 토글, drag-selection 기반 lookup, lookup 결과 로컬 캐시, auto-scroll 높이 정확도 개선 — 모두 별도 태스크로 분리 권장.
4. **Lookup feature 테스트**: `lookup_result_dto_test.dart` 로 fromJson 매핑 (term_type 모든 variant, etymology null, examples empty) 검증 필요.
