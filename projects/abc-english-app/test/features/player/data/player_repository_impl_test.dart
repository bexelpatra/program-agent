import 'dart:async';

import 'package:abc_english_app/core/domain/entities/episode.dart';
import 'package:abc_english_app/core/errors/app_exception.dart';
import 'package:abc_english_app/core/errors/result.dart';
import 'package:abc_english_app/features/episode_detail/domain/entities/episode_detail.dart';
import 'package:abc_english_app/features/player/data/datasources/player_audio_datasource.dart';
import 'package:abc_english_app/features/player/data/repositories/player_repository_impl.dart';
import 'package:abc_english_app/features/player/domain/entities/playback_source.dart';
import 'package:abc_english_app/features/player/domain/entities/playback_state.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:just_audio/just_audio.dart';

/// Hand-written stub. Subclassing [PlayerAudioDataSource] directly would
/// require a full AudioService; implementing its public API manually keeps
/// the repository test hermetic.
class _SpyDs implements PlayerAudioDataSource {
  _SpyDs({
    StreamController<PlayerState>? stateCtrl,
    StreamController<Duration>? positionCtrl,
  })  : _stateCtrl = stateCtrl ?? StreamController<PlayerState>.broadcast(),
        _positionCtrl =
            positionCtrl ?? StreamController<Duration>.broadcast();

  final StreamController<PlayerState> _stateCtrl;
  final StreamController<Duration> _positionCtrl;

  int loadCalls = 0;
  int playCalls = 0;
  int pauseCalls = 0;
  int seekCalls = 0;
  int disposeCalls = 0;
  Duration? lastSeek;

  Object? loadError;
  Object? playError;
  Object? pauseError;
  Object? seekError;

  void emitState(PlayerState state) {
    if (!_stateCtrl.isClosed) _stateCtrl.add(state);
  }

  void emitPosition(Duration d) {
    if (!_positionCtrl.isClosed) _positionCtrl.add(d);
  }

  void emitStateError(Object e) {
    if (!_stateCtrl.isClosed) _stateCtrl.addError(e);
  }

  Future<void> close() async {
    if (!_stateCtrl.isClosed) await _stateCtrl.close();
    if (!_positionCtrl.isClosed) await _positionCtrl.close();
  }

  @override
  Stream<PlayerState> get playerStateStream => _stateCtrl.stream;

  @override
  Stream<Duration> get positionStream => _positionCtrl.stream;

  @override
  Future<void> loadEpisode(EpisodeDetail detail) async {
    loadCalls++;
    if (loadError != null) throw loadError!;
  }

  @override
  Future<void> play() async {
    playCalls++;
    if (playError != null) throw playError!;
  }

  @override
  Future<void> pause() async {
    pauseCalls++;
    if (pauseError != null) throw pauseError!;
  }

  @override
  Future<void> seek(Duration position) async {
    seekCalls++;
    lastSeek = position;
    if (seekError != null) throw seekError!;
  }

  @override
  Future<void> dispose() async {
    disposeCalls++;
  }

  // Unused by repository, but required by the abstract interface.
  @override
  PlaybackSource resolveSource(EpisodeDetail detail) =>
      const PlaybackSource.none();
}

EpisodeDetail _detail({
  String id = 'ep-1',
  int durationMs = 123_000,
}) {
  final now = DateTime.utc(2026, 4, 5);
  return EpisodeDetail(
    episode: Episode(
      id: id,
      title: 't',
      publishedDate: now,
      durationMs: durationMs,
      lastModified: now,
      isDownloaded: false,
    ),
    sentences: const <Sentence>[],
  );
}

void main() {
  late _SpyDs ds;

  setUp(() {
    ds = _SpyDs();
  });

  tearDown(() async {
    await ds.close();
  });

  group('loadEpisode', () {
    test('success → Success(null), emits initial state for new episode',
        () async {
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });

      final emitted = <PlaybackState>[];
      final sub = repo.stateStream.listen(emitted.add);
      addTearDown(() async {
        await sub.cancel();
      });

      final r = await repo.loadEpisode(_detail(id: 'x', durationMs: 9000));
      expect(r, isA<Success<void>>());
      expect(ds.loadCalls, 1);
      await Future<void>.delayed(Duration.zero);

      // First emit: new episode binding.
      expect(emitted.isNotEmpty, isTrue);
      final first = emitted.first;
      expect(first.episodeId, 'x');
      expect(first.totalDurationMs, 9000);
      expect(first.error, isNull);
    });

    test('datasource throws AppException → Failure, state carries error',
        () async {
      ds.loadError = const NetworkException('no net');

      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });

      final emitted = <PlaybackState>[];
      final sub = repo.stateStream.listen(emitted.add);
      addTearDown(() async {
        await sub.cancel();
      });

      final r = await repo.loadEpisode(_detail());
      expect(r, isA<Failure<void>>());
      expect((r as Failure<void>).error, isA<NetworkException>());

      await Future<void>.delayed(Duration.zero);
      // Last emit should include the error.
      expect(emitted.last.error, isA<NetworkException>());
    });

    test('datasource throws ArgumentError → Failure(UnknownException)',
        () async {
      ds.loadError = ArgumentError('bad source');
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });
      final r = await repo.loadEpisode(_detail());
      expect(r, isA<Failure<void>>());
      expect((r as Failure<void>).error, isA<UnknownException>());
    });

    test('datasource throws PlayerException → Failure(NetworkException)',
        () async {
      ds.loadError = PlayerException(500, 'server oops');
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });
      final r = await repo.loadEpisode(_detail());
      expect(r, isA<Failure<void>>());
      final error = (r as Failure<void>).error;
      expect(error, isA<NetworkException>());
      expect((error as NetworkException).statusCode, 500);
    });

    test('datasource throws PlatformException → Failure(UnknownException)',
        () async {
      ds.loadError = PlatformException(code: 'BAD', message: 'fubar');
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });
      final r = await repo.loadEpisode(_detail());
      expect(r, isA<Failure<void>>());
      expect((r as Failure<void>).error, isA<UnknownException>());
    });

    test('loadEpisode after dispose → Failure(StorageException)', () async {
      final repo = PlayerRepositoryImpl(datasource: ds);
      await repo.dispose();
      final r = await repo.loadEpisode(_detail());
      expect(r, isA<Failure<void>>());
      expect((r as Failure<void>).error, isA<StorageException>());
    });
  });

  group('play/pause/seek delegation', () {
    test('play success → Success(null) and ds.play called', () async {
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });
      final r = await repo.play();
      expect(r, isA<Success<void>>());
      expect(ds.playCalls, 1);
    });

    test('pause → Success and ds.pause called', () async {
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });
      final r = await repo.pause();
      expect(r, isA<Success<void>>());
      expect(ds.pauseCalls, 1);
    });

    test('seek → Success and ds.seek called with position', () async {
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });
      final r = await repo.seek(const Duration(milliseconds: 555));
      expect(r, isA<Success<void>>());
      expect(ds.seekCalls, 1);
      expect(ds.lastSeek, const Duration(milliseconds: 555));
    });

    test('play after dispose → Failure(StorageException)', () async {
      final repo = PlayerRepositoryImpl(datasource: ds);
      await repo.dispose();
      final r = await repo.play();
      expect(r, isA<Failure<void>>());
      expect((r as Failure<void>).error, isA<StorageException>());
    });

    test('play throws AppException → Failure', () async {
      ds.playError = const NetworkException('down');
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });
      final r = await repo.play();
      expect(r, isA<Failure<void>>());
      expect((r as Failure<void>).error, isA<NetworkException>());
    });
  });

  group('stateStream mapping', () {
    test('PlayerState(playing=true, ready) → isPlaying=true, isBuffering=false',
        () async {
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });

      final emitted = <PlaybackState>[];
      final sub = repo.stateStream.listen(emitted.add);
      addTearDown(() async {
        await sub.cancel();
      });

      ds.emitState(PlayerState(true, ProcessingState.ready));
      await Future<void>.delayed(Duration.zero);

      expect(emitted.last.isPlaying, isTrue);
      expect(emitted.last.isBuffering, isFalse);
      expect(emitted.last.isCompleted, isFalse);
    });

    test('processingState=buffering → isBuffering=true', () async {
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });

      final emitted = <PlaybackState>[];
      final sub = repo.stateStream.listen(emitted.add);
      addTearDown(() async {
        await sub.cancel();
      });

      ds.emitState(PlayerState(true, ProcessingState.buffering));
      await Future<void>.delayed(Duration.zero);

      expect(emitted.last.isBuffering, isTrue);
    });

    test('processingState=loading → isBuffering=true', () async {
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });

      final emitted = <PlaybackState>[];
      final sub = repo.stateStream.listen(emitted.add);
      addTearDown(() async {
        await sub.cancel();
      });

      ds.emitState(PlayerState(false, ProcessingState.loading));
      await Future<void>.delayed(Duration.zero);

      expect(emitted.last.isBuffering, isTrue);
    });

    test('processingState=completed → isCompleted=true', () async {
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });

      final emitted = <PlaybackState>[];
      final sub = repo.stateStream.listen(emitted.add);
      addTearDown(() async {
        await sub.cancel();
      });

      ds.emitState(PlayerState(false, ProcessingState.completed));
      await Future<void>.delayed(Duration.zero);

      expect(emitted.last.isCompleted, isTrue);
    });

    test('positionStream tick → PlaybackState.positionMs updates', () async {
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });

      final emitted = <PlaybackState>[];
      final sub = repo.stateStream.listen(emitted.add);
      addTearDown(() async {
        await sub.cancel();
      });

      ds.emitPosition(const Duration(milliseconds: 4242));
      await Future<void>.delayed(Duration.zero);

      expect(emitted.last.positionMs, 4242);
    });

    test('totalDurationMs preserved across position ticks after loadEpisode',
        () async {
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });

      final emitted = <PlaybackState>[];
      final sub = repo.stateStream.listen(emitted.add);
      addTearDown(() async {
        await sub.cancel();
      });

      await repo.loadEpisode(_detail(durationMs: 75_000));
      ds.emitPosition(const Duration(milliseconds: 10_000));
      await Future<void>.delayed(Duration.zero);

      expect(emitted.last.totalDurationMs, 75_000);
      expect(emitted.last.positionMs, 10_000);
    });

    test('upstream stream error → error field populated with NetworkException',
        () async {
      final repo = PlayerRepositoryImpl(datasource: ds);
      addTearDown(() async {
        await repo.dispose();
      });

      final emitted = <PlaybackState>[];
      final sub = repo.stateStream.listen(emitted.add);
      addTearDown(() async {
        await sub.cancel();
      });

      ds.emitStateError(PlayerException(503, 'boom'));
      await Future<void>.delayed(Duration.zero);

      expect(emitted.last.error, isA<NetworkException>());
    });
  });

  group('dispose', () {
    test('dispose is idempotent', () async {
      final repo = PlayerRepositoryImpl(datasource: ds);
      final r1 = await repo.dispose();
      final r2 = await repo.dispose();
      expect(r1, isA<Success<void>>());
      expect(r2, isA<Success<void>>());
    });
  });
}
