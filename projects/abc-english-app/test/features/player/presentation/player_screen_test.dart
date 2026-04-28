import 'dart:async';

import 'package:abc_english_app/core/domain/entities/episode.dart';
import 'package:abc_english_app/core/errors/app_exception.dart';
import 'package:abc_english_app/core/errors/result.dart';
import 'package:abc_english_app/features/episode_detail/data/repositories/episode_detail_repository_impl.dart';
import 'package:abc_english_app/features/episode_detail/domain/entities/episode_detail.dart';
import 'package:abc_english_app/features/episode_detail/domain/repositories/episode_detail_repository.dart';
import 'package:abc_english_app/features/player/data/repositories/player_repository_impl.dart';
import 'package:abc_english_app/features/player/domain/entities/playback_state.dart';
import 'package:abc_english_app/features/player/domain/repositories/player_repository.dart';
import 'package:abc_english_app/features/player/presentation/player_screen.dart';
import 'package:abc_english_app/features/player/presentation/widgets/player_sentence_tile.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

class _FakeEpisodeDetailRepo implements EpisodeDetailRepository {
  _FakeEpisodeDetailRepo(this.result);
  final Result<EpisodeDetail> result;

  @override
  Future<Result<EpisodeDetail>> getDetail(String id) async => result;
}

class _FakePlayerRepo implements PlayerRepository {
  _FakePlayerRepo({Stream<PlaybackState>? stateStream})
      : _controller = StreamController<PlaybackState>.broadcast() {
    if (stateStream != null) {
      _controller.addStream(stateStream);
    }
  }

  final StreamController<PlaybackState> _controller;

  int playCalls = 0;
  int pauseCalls = 0;
  int seekCalls = 0;
  int loadCalls = 0;
  Duration? lastSeek;

  void emit(PlaybackState state) {
    if (!_controller.isClosed) {
      _controller.add(state);
    }
  }

  @override
  Stream<PlaybackState> get stateStream => _controller.stream;

  @override
  Future<Result<void>> loadEpisode(EpisodeDetail detail) async {
    loadCalls++;
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
    seekCalls++;
    lastSeek = position;
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

EpisodeDetail _detail({List<Sentence>? sentences, String id = 'ep-1'}) {
  final now = DateTime.utc(2026, 4, 5);
  return EpisodeDetail(
    episode: Episode(
      id: id,
      title: 'Morning News',
      publishedDate: now,
      durationMs: 60_000,
      lastModified: now,
      isDownloaded: false,
    ),
    sentences: sentences ??
        const [
          Sentence(index: 0, text: 'First sentence.', startMs: 0, endMs: 2000),
          Sentence(
              index: 1, text: 'Second sentence.', startMs: 2000, endMs: 4000),
          Sentence(
              index: 2, text: 'Third sentence.', startMs: 4000, endMs: 6000),
        ],
  );
}

Widget _host(ProviderContainer c) {
  return UncontrolledProviderScope(
    container: c,
    child: const MaterialApp(home: PlayerScreen(episodeId: 'ep-1')),
  );
}

ProviderContainer _container({
  required Result<EpisodeDetail> detail,
  required _FakePlayerRepo playerRepo,
}) {
  return ProviderContainer(
    overrides: [
      episodeDetailRepositoryProvider.overrideWith(
        (ref) async => _FakeEpisodeDetailRepo(detail),
      ),
      playerRepositoryProvider.overrideWithValue(playerRepo),
    ],
  );
}

void main() {
  testWidgets('loading state → CircularProgressIndicator', (tester) async {
    final player = _FakePlayerRepo();
    final c = _container(
      detail: Success(_detail()),
      playerRepo: player,
    );
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    // First frame: FutureProvider is still pending.
    expect(find.byType(CircularProgressIndicator), findsWidgets);

    await tester.pumpAndSettle();
  });

  testWidgets('data state → renders sentence tiles', (tester) async {
    final player = _FakePlayerRepo();
    final c = _container(
      detail: Success(_detail()),
      playerRepo: player,
    );
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();

    expect(find.byType(PlayerSentenceTile), findsWidgets);
    expect(find.text('Morning News'), findsOneWidget);
  });

  testWidgets('error state → error view with retry', (tester) async {
    final player = _FakePlayerRepo();
    final c = _container(
      detail: const Failure<EpisodeDetail>(NotFoundException('gone')),
      playerRepo: player,
    );
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();

    expect(find.text('에피소드를 찾을 수 없습니다.'), findsOneWidget);
    expect(find.text('다시 시도'), findsOneWidget);
  });

  testWidgets('FAB tap calls play() (paused state)', (tester) async {
    final player = _FakePlayerRepo();
    final c = _container(
      detail: Success(_detail()),
      playerRepo: player,
    );
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();

    // Emit a paused state and let the StreamProvider pick it up.
    player.emit(PlaybackState.initial());
    await tester.pumpAndSettle();

    await tester.tap(find.byKey(const Key('player-play-pause')));
    await tester.pumpAndSettle();

    expect(player.playCalls, 1);
    expect(player.pauseCalls, 0);
  });

  testWidgets('FAB tap calls pause() (playing state)', (tester) async {
    final player = _FakePlayerRepo();
    final c = _container(
      detail: Success(_detail()),
      playerRepo: player,
    );
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();

    // Emit a playing state and let the StreamProvider pick it up.
    player.emit(PlaybackState.initial().copyWith(isPlaying: true));
    await tester.pumpAndSettle();

    await tester.tap(find.byKey(const Key('player-play-pause')));
    await tester.pumpAndSettle();

    expect(player.pauseCalls, 1);
    expect(player.playCalls, 0);
  });

  testWidgets('current index highlighted when position is inside sentence 1',
      (tester) async {
    final player = _FakePlayerRepo();
    final c = _container(
      detail: Success(_detail()),
      playerRepo: player,
    );
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();

    // Position inside sentence 1 (2000ms–4000ms).
    player.emit(
      PlaybackState.initial().copyWith(positionMs: 3000, totalDurationMs: 6000),
    );
    await tester.pumpAndSettle();

    // Sentence 1 tile should be highlighted (isCurrent=true).
    // The widget key is on the inner GestureDetector, so find the enclosing
    // PlayerSentenceTile by matching sentence.index in the tile widget.
    final tiles = tester.widgetList<PlayerSentenceTile>(
      find.byType(PlayerSentenceTile),
    );
    final byIndex = {for (final t in tiles) t.sentence.index: t};
    expect(byIndex[1]!.isCurrent, isTrue);
    expect(byIndex[0]!.isCurrent, isFalse);
    expect(byIndex[2]!.isCurrent, isFalse);
  });

  testWidgets('empty sentences → "문장이 없습니다"', (tester) async {
    final player = _FakePlayerRepo();
    final c = _container(
      detail: Success(_detail(sentences: const [])),
      playerRepo: player,
    );
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();

    expect(find.text('문장이 없습니다.'), findsOneWidget);
  });

  testWidgets('error in playback state → banner rendered', (tester) async {
    final player = _FakePlayerRepo();
    final c = _container(
      detail: Success(_detail()),
      playerRepo: player,
    );
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();

    player.emit(
      PlaybackState.initial().copyWith(
        error: const UnauthorizedException('bad token'),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.textContaining('스트리밍 인증 실패'), findsOneWidget);
  });
}
