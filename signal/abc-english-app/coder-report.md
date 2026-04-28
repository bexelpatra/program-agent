---
agent: coder
task_id: TASK-054-FIX
status: DONE
timestamp: 2026-04-22T13:05:00
---

## 결과 요약

`lookup_bottom_sheet.dart` 를 `features/player/presentation/widgets/` 에서 `shared/presentation/widgets/` 로 이동하고, `features/notebook/` 직접 import 를 콜백 주입으로 대체했다. player → lookup / lookup → notebook 의 feature 간 cross-import 가 모두 제거되었다. `flutter analyze` clean, `flutter test` 170/170 PASS 유지.

### 변경 골자
1. 신규 위치: `lib/shared/presentation/widgets/lookup_bottom_sheet.dart`. import 는 `core/errors/app_exception.dart` + `features/lookup/data/repositories/lookup_repository_impl.dart` (provider) + `features/lookup/domain/entities/lookup_result.dart` + `features/lookup/domain/usecases/lookup_word.dart` 4개. `features/notebook/` import 0건 (grep 확인).
2. Widget API 에 `typedef OnAddToNotebook = Future<bool> Function({...})` 추가 + 필수 `onAddToNotebook` 매개변수 신설. 기존 `AddNotebookEntry`/`notebookRepositoryProvider` 직접 참조 삭제. 성공/실패는 `bool` 로 받아 시트 내부에서 SnackBar + saved state 갱신.
3. `PlayerScreen` 에서 신규 `_addLookupWordToNotebook` 메서드가 notebook repository provider + `AddNotebookEntry` usecase 를 실행, 결과를 `Result.isSuccess` 로 환원해 시트에 `bool` 반환. 호출부는 `LookupBottomSheet.show(..., onAddToNotebook: _addLookupWordToNotebook)`.
4. 테스트 파일 이동: `test/features/player/presentation/lookup_bottom_sheet_test.dart` → `test/shared/presentation/lookup_bottom_sheet_test.dart`. 의존성에서 `notebookRepositoryProvider.overrideWith(...)` 제거, 대신 `_RecordingAdder` 가 콜백으로 인자를 캡처. 기존 4개 testWidgets assertion 을 동일하게 유지 (provenance/failure/unauthorized/loading→result).

## 변경된 파일

### 신규
- `projects/abc-english-app/lib/shared/presentation/widgets/lookup_bottom_sheet.dart`
- `projects/abc-english-app/test/shared/presentation/lookup_bottom_sheet_test.dart`

### 삭제
- `projects/abc-english-app/lib/features/player/presentation/widgets/lookup_bottom_sheet.dart`
- `projects/abc-english-app/test/features/player/presentation/lookup_bottom_sheet_test.dart`

### 수정
- `projects/abc-english-app/lib/features/player/presentation/player_screen.dart`
  - import 교체: `widgets/lookup_bottom_sheet.dart` → `../../../shared/presentation/widgets/lookup_bottom_sheet.dart`
  - notebook 브릿지용 import 추가: `features/notebook/data/repositories/notebook_repository_impl.dart`, `features/notebook/domain/usecases/add_notebook_entry.dart`
  - `_handleWordLongPress` 가 `onAddToNotebook: _addLookupWordToNotebook` 전달
  - 신규 메서드 `_addLookupWordToNotebook({required word, required context, episodeId, sentenceIndex, meaning, note}) → Future<bool>`

## 공개 API 변경

### `LookupBottomSheet` (shared/presentation/widgets)
- 생성자 매개변수 변경: `required OnAddToNotebook onAddToNotebook` 추가.
- 정적 `LookupBottomSheet.show(...)` 의 매개변수에도 `required OnAddToNotebook onAddToNotebook` 추가.
- 신규 typedef `OnAddToNotebook = Future<bool> Function({required String word, required String context, String? episodeId, int? sentenceIndex, String? meaning, String? note})`.

## 검증

- `flutter analyze` → `No issues found! (ran in 1.0s)`.
- `flutter test` → `00:08 +170: All tests passed!`.
- `grep -r "features/notebook" lib/shared/presentation/widgets/lookup_bottom_sheet.dart` → 0건.
- `grep -rn "lookup_bottom_sheet" lib/` → 호출부는 `player_screen.dart` 1곳만, 임포트 경로는 `shared/presentation/widgets/lookup_bottom_sheet.dart`.

## 이슈/블로커

### 설계 예외 (architecture 반영 제안)
**`features/player/presentation/player_screen.dart` 가 `features/notebook/data|domain` 을 직접 import 한다.** 이는 architecture.md L157 "features 간 직접 의존 금지" 와 충돌한다.

- 현재 상태: player_screen 이 `notebookRepositoryProvider` + `AddNotebookEntry` usecase 를 직접 호출 (L9, L10, L230-L244).
- 이유: 태스크 범위에서 `lookup_bottom_sheet` 의 cross-import 만 제거하는 것이 목표였고, notebook 추가 진입점을 `core/` 수준의 port 로 추상화하려면 (a) 새 abstract class, (b) app root DI 주입 지점 수정, (c) settings/notebook_screen 등 다른 호출자 조사 가 필요해 코드 복잡성이 급증한다.
- 제안 A (권장): architecture.md "레이어 규칙" 단락에 예외 명시 —
  > "player 는 재생 중 단어장 추가 진입점을 제공하므로 notebook 의 repository provider + AddNotebookEntry usecase 를 직접 참조할 수 있다. 이는 host feature 가 sibling feature 의 도메인을 소비하는 유일한 승인 경로이며, 다른 feature 간 직접 의존은 금지된다."
- 제안 B: 후속 태스크에서 `core/shared/notebook_entry_point.dart` (또는 유사) 에 추상 port 정의 → `main.dart` 에서 구체 구현 주입. player/settings 등 복수 호출자가 생기면 이때 전환.
- 우선은 A(예외 명시)로 진행하고, 추가 호출자가 3곳 이상이 될 때 B(port 승격)로 리팩터링 권장. 이 내용은 retrospective 로 이월 필요.

### 기타
- `lookup_bottom_sheet` 가 `shared/presentation/` 에 위치하지만 `lookupRepositoryProvider` 를 읽는다 (lookup 도메인 UseCase 직접 실행). 이는 shared 위젯이 lookup feature 의 **domain + provider** 만 사용한다는 점에서 규칙 내 — features 간 의존이 아니라 "공용 위젯 → 단일 feature 의 domain entry". 단 향후 lookup 외 다른 feature 에서도 이 패턴이 생기면 shared 위젯의 feature 종속을 재검토 필요.

## 다음 제안

1. **architecture.md 예외 명시**: Manager 가 위 "설계 예외" 문구를 architecture.md 레이어 규칙 섹션에 추가. retrospective 에도 "host feature 의 sibling 도메인 소비" 토픽 기록.
2. **Tester 재회귀**: 동일 태스크에 대해 Tester 가 `grep "features/notebook" lib/shared/presentation/widgets/` → 0건, `flutter test` 170/170 을 재확인하는 태스크가 있으면 닫음.
3. **후속 (backlog)**: `core/ports/notebook_entry_point.dart` 도입 검토. player + settings + 향후 quick-add floating action 등 notebook add 호출자가 2개 이상 되면 port 승격.
