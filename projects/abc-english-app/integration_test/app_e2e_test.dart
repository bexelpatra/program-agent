// End-to-end smoke integration test for the ABC English Flutter app.
//
// Scenario (TASK-070):
//   1. Boot ProviderScope + AbcApp with all external dependencies faked
//      via Riverpod overrides (no real Dio / drift / just_audio).
//   2. Episodes tab renders the fixture list (3 episodes).
//   3. Tapping an episode routes to `/episodes/:id` and shows the
//      transcript + play button.
//   4. Tapping "재생" routes to `/player/:id` and renders the player
//      shell. The fake PlayerRepository stands in for just_audio.
//   5. Tapping a transcript tile invokes jumpToSentence — verified by
//      inspecting the fake repository's recorded `seek` calls.
//   6. Long-press on a word opens the lookup bottom sheet with a canned
//      LookupResult for `test_word`.
//   7. "단어장에 추가" tap pushes the entry through NotebookRepository.add
//      and dismisses the sheet (SnackBar confirmation asserted).
//   8. Navigating back to the Notebook tab lists the freshly added entry.
//
// Runs headless via `flutter test integration_test/app_e2e_test.dart`.
// External integrations (Dio, drift, just_audio, connectivity_plus) are
// stubbed at the repository provider layer — the same injection seam the
// 170 unit/widget tests already use. This keeps the test hermetic and
// avoids platform plugins that the flutter_test harness cannot provide.

import 'dart:async';

import 'package:abc_english_app/app.dart';
import 'package:abc_english_app/core/connectivity/connectivity_service.dart';
import 'package:abc_english_app/core/domain/entities/episode.dart';
import 'package:abc_english_app/core/errors/app_exception.dart';
import 'package:abc_english_app/core/errors/result.dart';
import 'package:abc_english_app/features/episode_detail/data/repositories/episode_detail_repository_impl.dart';
import 'package:abc_english_app/features/episode_detail/domain/entities/episode_detail.dart';
import 'package:abc_english_app/features/episode_detail/domain/repositories/episode_detail_repository.dart';
import 'package:abc_english_app/features/episode_list/data/repositories/episode_repository_impl.dart';
import 'package:abc_english_app/features/episode_list/domain/repositories/episode_repository.dart';
import 'package:abc_english_app/features/episode_list/presentation/episode_list_screen.dart';
import 'package:abc_english_app/features/episode_list/presentation/widgets/episode_card.dart';
import 'package:abc_english_app/features/lookup/data/repositories/lookup_repository_impl.dart';
import 'package:abc_english_app/features/lookup/domain/entities/lookup_result.dart';
import 'package:abc_english_app/features/lookup/domain/repositories/lookup_repository.dart';
import 'package:abc_english_app/features/notebook/data/repositories/notebook_repository_impl.dart';
import 'package:abc_english_app/features/notebook/data/sync/notebook_auto_sync_trigger.dart';
import 'package:abc_english_app/features/notebook/domain/entities/notebook_entry.dart';
import 'package:abc_english_app/features/notebook/domain/entities/sync_status.dart';
import 'package:abc_english_app/features/notebook/domain/repositories/notebook_repository.dart';
import 'package:abc_english_app/features/notebook/presentation/widgets/notebook_entry_tile.dart';
import 'package:abc_english_app/features/player/data/repositories/player_repository_impl.dart';
import 'package:abc_english_app/features/player/domain/entities/playback_state.dart';
import 'package:abc_english_app/features/player/domain/repositories/player_repository.dart';
import 'package:abc_english_app/features/player/presentation/widgets/player_sentence_tile.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

// ---------------------------------------------------------------------------
// Fixtures
// ---------------------------------------------------------------------------

DateTime _fixedNow() => DateTime.utc(2026, 4, 22, 10);

/// Three-episode fixture list for the Episodes tab.
List<Episode> _fixtureEpisodes() {
  final now = _fixedNow();
  return [
    Episode(
      id: 'ep-001',
      title: 'Morning News Rundown',
      publishedDate: now,
      durationMs: 180_000,
      lastModified: now,
      isDownloaded: false,
    ),
    Episode(
      id: 'ep-002',
      title: 'Midday Markets Update',
      publishedDate: now.subtract(const Duration(days: 1)),
      durationMs: 240_000,
      lastModified: now,
      isDownloaded: false,
    ),
    Episode(
      id: 'ep-003',
      title: 'Evening Feature Story',
      publishedDate: now.subtract(const Duration(days: 2)),
      durationMs: 300_000,
      lastModified: now,
      isDownloaded: false,
    ),
  ];
}

/// Five-sentence transcript for ep-001. Includes the literal token
/// `test_word` so we can long-press it and assert the lookup sheet picks
/// it up via the tile's word tokenizer.
EpisodeDetail _fixtureDetail(String id) {
  final episodes = _fixtureEpisodes();
  final ep = episodes.firstWhere((e) => e.id == id, orElse: () => episodes[0]);
  return EpisodeDetail(
    episode: ep,
    sentences: const [
      Sentence(
          index: 0, text: 'Welcome to the show.', startMs: 0, endMs: 2000),
      Sentence(
          index: 1,
          text: 'Today we explore one test_word up close.',
          startMs: 2000,
          endMs: 5000),
      Sentence(
          index: 2, text: 'Three key points to cover.', startMs: 5000, endMs: 8000),
      Sentence(
          index: 3,
          text: 'Four speakers join the panel.',
          startMs: 8000,
          endMs: 11000),
      Sentence(
          index: 4, text: 'Thanks for listening today.', startMs: 11000, endMs: 14000),
    ],
  );
}

LookupResult _fixtureLookup() {
  return const LookupResult(
    word: 'test_word',
    definitions: ['test definition for the integration e2e run'],
    examples: ['An example using test_word here.'],
    termType: 'word',
  );
}

// ---------------------------------------------------------------------------
// Fakes
// ---------------------------------------------------------------------------

class _FakeEpisodeRepo implements EpisodeRepository {
  _FakeEpisodeRepo(this._episodes);
  final List<Episode> _episodes;

  @override
  Future<Result<List<Episode>>> listEpisodes({
    int page = 1,
    int size = 20,
    DateTime? sinceModified,
  }) async {
    // Only page 1 carries content; page>=2 returns empty so `hasMore` flips
    // to false and the list controller stops requesting.
    if (page == 1) {
      return Success(List<Episode>.unmodifiable(_episodes));
    }
    return const Success(<Episode>[]);
  }

  @override
  Future<Result<Episode>> getById(String id) async {
    final ep = _episodes.where((e) => e.id == id).toList();
    if (ep.isEmpty) {
      return Failure<Episode>(NotFoundException('no such episode'));
    }
    return Success(ep.first);
  }
}

class _FakeEpisodeDetailRepo implements EpisodeDetailRepository {
  _FakeEpisodeDetailRepo(this._detailBuilder);
  final EpisodeDetail Function(String id) _detailBuilder;

  @override
  Future<Result<EpisodeDetail>> getDetail(String id) async {
    return Success(_detailBuilder(id));
  }
}

class _FakeLookupRepo implements LookupRepository {
  _FakeLookupRepo(this._result);
  final LookupResult _result;

  @override
  Future<Result<LookupResult>> lookup({
    required String word,
    String? context,
  }) async {
    return Success(_result);
  }
}

class _FakeNotebookRepo implements NotebookRepository {
  _FakeNotebookRepo();

  final List<NotebookEntry> _entries = <NotebookEntry>[];
  int _idSeq = 0;

  List<NotebookEntry> get allEntries => List<NotebookEntry>.unmodifiable(_entries);

  @override
  Future<Result<List<NotebookEntry>>> list({DateTime? sinceModified}) async {
    return Success(List<NotebookEntry>.unmodifiable(_entries));
  }

  @override
  Future<Result<NotebookEntry>> add({
    required String word,
    required String context,
    String? episodeId,
    int? sentenceIndex,
    String? meaning,
    String? note,
  }) async {
    final now = DateTime.utc(2026, 4, 22, 10, 30);
    final entry = NotebookEntry(
      id: 'nb-${++_idSeq}',
      word: word,
      context: context,
      createdAt: now,
      lastModified: now,
      syncStatus: SyncStatus.synced,
      episodeId: episodeId,
      sentenceIndex: sentenceIndex,
      meaning: meaning,
      note: note,
    );
    _entries.add(entry);
    return Success(entry);
  }

  @override
  Future<Result<NotebookEntry>> update({
    required String id,
    String? word,
    String? context,
    String? episodeId,
    int? sentenceIndex,
    String? meaning,
    String? note,
  }) async {
    throw UnimplementedError('notebook.update not exercised by this e2e');
  }

  @override
  Future<Result<void>> remove(String id) async {
    _entries.removeWhere((e) => e.id == id);
    return const Success(null);
  }
}

class _FakePlayerRepo implements PlayerRepository {
  _FakePlayerRepo() : _controller = StreamController<PlaybackState>.broadcast();

  final StreamController<PlaybackState> _controller;

  int loadCalls = 0;
  int playCalls = 0;
  int pauseCalls = 0;
  final List<Duration> seekCalls = [];

  @override
  Stream<PlaybackState> get stateStream => _controller.stream;

  @override
  Future<Result<void>> loadEpisode(EpisodeDetail detail) async {
    loadCalls++;
    // Emit an initial state so the stream-provider sees something.
    _controller.add(
      PlaybackState.initial().copyWith(
        episodeId: detail.episode.id,
        totalDurationMs: detail.episode.durationMs,
      ),
    );
    return const Success(null);
  }

  @override
  Future<Result<void>> play() async {
    playCalls++;
    return const Success(null);
  }

  @override
  Future<Result<void>> pause() async {
    pauseCalls++;
    return const Success(null);
  }

  @override
  Future<Result<void>> seek(Duration position) async {
    seekCalls.add(position);
    return const Success(null);
  }

  @override
  Future<Result<void>> dispose() async {
    if (!_controller.isClosed) {
      await _controller.close();
    }
    return const Success(null);
  }
}

/// Always-online connectivity fake. Implements the same public surface as
/// [ConnectivityService] by subclassing and forcing both answers.
class _FakeConnectivityService extends ConnectivityService {
  _FakeConnectivityService() : super(connectivity: _StubConnectivity());

  @override
  Future<bool> isOnline() async => true;

  @override
  Stream<bool> get onlineStream async* {
    yield true;
    // Never emit a transition — keeps NotebookAutoSyncTrigger quiescent.
  }
}

class _StubConnectivity implements Connectivity {
  @override
  Future<List<ConnectivityResult>> checkConnectivity() async {
    return const [ConnectivityResult.wifi];
  }

  @override
  Stream<List<ConnectivityResult>> get onConnectivityChanged =>
      const Stream<List<ConnectivityResult>>.empty();
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/// Build the set of provider overrides used by every scenario. Returning a
/// record lets the individual tests also reach into the fakes to assert
/// call counts or inspect stored state.
class _Overrides {
  _Overrides({
    required this.episode,
    required this.detail,
    required this.lookup,
    required this.notebook,
    required this.player,
  });

  final _FakeEpisodeRepo episode;
  final _FakeEpisodeDetailRepo detail;
  final _FakeLookupRepo lookup;
  final _FakeNotebookRepo notebook;
  final _FakePlayerRepo player;

  List<Override> build() {
    return [
      // Block the real connectivity_plus plugin: the auto-sync trigger
      // subscribes to onlineStream at scope creation.
      connectivityServiceProvider.overrideWithValue(_FakeConnectivityService()),
      episodeRepositoryProvider.overrideWith((ref) async => episode),
      episodeDetailRepositoryProvider.overrideWith((ref) async => detail),
      lookupRepositoryProvider.overrideWithValue(lookup),
      notebookRepositoryProvider.overrideWith((ref) async => notebook),
      playerRepositoryProvider.overrideWithValue(player),
    ];
  }
}

_Overrides _buildOverrides() {
  return _Overrides(
    episode: _FakeEpisodeRepo(_fixtureEpisodes()),
    detail: _FakeEpisodeDetailRepo(_fixtureDetail),
    lookup: _FakeLookupRepo(_fixtureLookup()),
    notebook: _FakeNotebookRepo(),
    player: _FakePlayerRepo(),
  );
}

Future<void> _pumpApp(WidgetTester tester, _Overrides overrides) async {
  await tester.pumpWidget(
    ProviderScope(
      overrides: overrides.build(),
      child: const AbcApp(),
    ),
  );
  await tester.pumpAndSettle();
}

/// Scroll until [finder] resolves to a hit-testable widget inside the
/// first [Scrollable] descendant of [within]. Reuses Flutter's
/// dragUntilVisible so we don't depend on viewport size.
Future<void> _scrollUntilVisible(
  WidgetTester tester, {
  required Finder finder,
  required Finder within,
  Offset delta = const Offset(0, -200),
}) async {
  final scrollable = find.descendant(
    of: within,
    matching: find.byType(Scrollable),
  );
  await tester.dragUntilVisible(
    finder,
    scrollable.first,
    delta,
  );
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

void main() {
  // Installs the IntegrationTestWidgetsFlutterBinding; on headless runs
  // this behaves like the regular test binding but exposes the extra
  // hooks (screenshot / reportData) that `flutter drive` uses on-device.
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Episodes tab renders the fixture list', (tester) async {
    final overrides = _buildOverrides();
    await _pumpApp(tester, overrides);

    expect(find.byType(EpisodeListScreen), findsOneWidget);
    expect(find.byType(EpisodeCard), findsNWidgets(3));
    expect(find.text('Morning News Rundown'), findsOneWidget);
    expect(find.text('Midday Markets Update'), findsOneWidget);
    expect(find.text('Evening Feature Story'), findsOneWidget);
  });

  testWidgets('end-to-end: list → detail → player → word add → notebook',
      (tester) async {
    // A roomier viewport so the transcript list, player controls, and
    // notebook tile all fit without needing to scroll every single step.
    await tester.binding.setSurfaceSize(const Size(500, 1600));
    addTearDown(() => tester.binding.setSurfaceSize(null));

    final overrides = _buildOverrides();
    await _pumpApp(tester, overrides);

    // --- Step 1: Tap into the first episode (ep-001). ---
    await tester.tap(find.text('Morning News Rundown'));
    await tester.pumpAndSettle();

    // We are now on `/episodes/ep-001`. The AppBar title is the generic
    // "Episode" copy (the title lives in the body header), and the
    // transcript "Transcript" label is visible.
    expect(find.text('Transcript'), findsOneWidget);
    expect(find.byKey(const Key('episode-detail-play-button')), findsOneWidget);

    // --- Step 2: Play button → player screen. ---
    await tester.tap(find.byKey(const Key('episode-detail-play-button')));
    await tester.pumpAndSettle();

    // Player screen mounted: its AppBar shows the episode title and the
    // fake PlayerRepository.loadEpisode has been invoked.
    expect(overrides.player.loadCalls, 1,
        reason: 'PlayerRepository.loadEpisode must fire on screen mount');
    expect(find.byType(PlayerSentenceTile), findsWidgets);

    // --- Step 3: Tap a sentence tile → jumpToSentence hits the repo. ---
    // Use the third sentence (index 2) so the fake records a non-zero seek.
    await tester.tap(find.byKey(const Key('player-sentence-2')));
    await tester.pumpAndSettle();

    expect(overrides.player.seekCalls, isNotEmpty,
        reason: 'sentence tap should call PlayerRepository.seek via jumpToSentence');
    // jumpToSentence seeks to the sentence start — 5000ms per fixture.
    expect(overrides.player.seekCalls.last, const Duration(milliseconds: 5000));

    // --- Step 4: Long-press a word → lookup sheet opens. ---
    // `PlayerSentenceTile` tokenizes each word into its own TextSpan with
    // a LongPressGestureRecognizer. To trigger that recognizer reliably
    // under `flutter_test`, we emulate the gesture on the tile itself and
    // rely on sentence-index 1 containing the literal `test_word` token.
    await _longPressWordInSentence(
      tester,
      sentenceKey: 'player-sentence-1',
      wordToken: 'test_word',
    );
    await tester.pumpAndSettle();

    // Lookup sheet content is on-screen.
    expect(find.byKey(const Key('lookup-add-to-notebook')), findsOneWidget);
    expect(find.text('test_word'), findsWidgets);

    // --- Step 5: Tap "단어장에 추가" → NotebookRepository.add called. ---
    await tester.tap(find.byKey(const Key('lookup-add-to-notebook')));
    // First pump builds the SnackBar, second lets its animation start.
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 16));

    expect(overrides.notebook.allEntries, hasLength(1),
        reason: 'add-to-notebook CTA must call NotebookRepository.add exactly once');
    final added = overrides.notebook.allEntries.single;
    expect(added.word, 'test_word');
    expect(added.episodeId, 'ep-001');
    expect(added.sentenceIndex, 1);

    // SnackBar confirmation visible.
    expect(find.text('단어장에 추가되었습니다'), findsOneWidget);

    // Close the bottom sheet cleanly before navigating tabs. Waiting for
    // the SnackBar timeout avoids lingering Timer<Null> on tearDown.
    await tester.pumpAndSettle(const Duration(seconds: 3));
    // Return from the player screen so we're back in the shell nav.
    final playerNavigator = Navigator.of(
      tester.element(find.byType(PlayerSentenceTile).first),
    );
    playerNavigator.pop();
    // Pop the bottom sheet if it's still up.
    if (find.byKey(const Key('lookup-add-to-notebook')).evaluate().isNotEmpty) {
      playerNavigator.pop();
    }
    await tester.pumpAndSettle();

    // --- Step 6: Navigate to Notebook tab, verify entry listed. ---
    await tester.tap(find.byIcon(Icons.book_outlined));
    await tester.pumpAndSettle();

    expect(find.byType(NotebookEntryTile), findsOneWidget);
    expect(find.text('test_word'), findsWidgets);
  }, timeout: const Timeout(Duration(seconds: 60)));
}

// ---------------------------------------------------------------------------
// Internals
// ---------------------------------------------------------------------------

/// Triggers a long-press on a specific word token inside a
/// [PlayerSentenceTile].
///
/// Walks the tile's `RichText` to find the child `TextSpan` whose text
/// matches [wordToken] (case-insensitive, punctuation stripped the same
/// way the tile does) and fires its [LongPressGestureRecognizer]
/// directly. This is the documented pattern for driving per-span gesture
/// recognizers from the test harness — the higher-level
/// `tester.longPress(find.text(word))` does not work because the
/// recognizer is installed on a `TextSpan`, not on a `Text` widget.
Future<void> _longPressWordInSentence(
  WidgetTester tester, {
  required String sentenceKey,
  required String wordToken,
}) async {
  // The tile contains two RichTexts — the transcript line (which carries
  // per-word LongPressGestureRecognizers) and a compact timestamp row. We
  // walk every RichText under the tile and pick the first one whose span
  // tree actually contains our target token. That avoids relying on
  // document order / finds-one semantics.
  final richTextFinder = find.descendant(
    of: find.byKey(Key(sentenceKey)),
    matching: find.byType(RichText),
  );
  expect(richTextFinder, findsWidgets,
      reason: 'tile with key=$sentenceKey must contain at least one RichText');

  TextSpan? target;
  for (final element in richTextFinder.evaluate()) {
    final widget = element.widget as RichText;
    target = _findSpanForToken(widget.text, wordToken);
    if (target != null) break;
  }
  expect(target, isNotNull,
      reason:
          'expected a RichText under $sentenceKey to contain a TextSpan for "$wordToken"');

  final recognizer = target!.recognizer;
  expect(recognizer, isA<LongPressGestureRecognizer>(),
      reason: 'matching TextSpan must carry a LongPressGestureRecognizer');

  (recognizer! as LongPressGestureRecognizer).onLongPress?.call();
  await tester.pump();
}

TextSpan? _findSpanForToken(InlineSpan root, String token) {
  TextSpan? hit;
  final cleanedTarget = _cleanWord(token);
  root.visitChildren((span) {
    if (span is TextSpan) {
      final text = span.text;
      if (text != null && _cleanWord(text).toLowerCase() == cleanedTarget) {
        hit ??= span;
      }
    }
    return hit == null; // keep walking until we find a match
  });
  return hit;
}

String _cleanWord(String raw) {
  // Mirrors `PlayerSentenceTile._punctuation` trimming so we match
  // whatever the widget actually registered for long-press.
  final re = RegExp(r"^[^\p{L}\p{N}'\-]+|[^\p{L}\p{N}'\-]+$", unicode: true);
  return raw.replaceAll(re, '').toLowerCase();
}
