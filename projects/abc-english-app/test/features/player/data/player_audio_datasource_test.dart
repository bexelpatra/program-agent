import 'dart:async';

import 'package:abc_english_app/core/audio/audio_service.dart';
import 'package:abc_english_app/core/config/app_config.dart';
import 'package:abc_english_app/core/domain/entities/episode.dart';
import 'package:abc_english_app/features/episode_detail/domain/entities/episode_detail.dart';
import 'package:abc_english_app/features/player/data/datasources/player_audio_datasource.dart';
import 'package:abc_english_app/features/player/domain/entities/playback_source.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:just_audio/just_audio.dart';
import 'package:just_audio_background/just_audio_background.dart';

/// Hand-written spy AudioService. mocktail's `captureAny(named: ...)` for a
/// method with multiple named args conflates captures order, so we capture
/// directly via `setSource(...)` override. Only the methods PlayerAudio-
/// DataSource actually calls need real behaviour.
class _SpyAudio implements AudioService {
  _SpyAudio({
    this.stateStreamValue = const Stream<PlayerState>.empty(),
    this.positionStreamValue = const Stream<Duration>.empty(),
    this.setSourceError,
  });

  // Captured setSource call.
  String? capturedUrl;
  String? capturedLocalPath;
  MediaItem? capturedMetadata;
  Map<String, String>? capturedHeaders;
  int setSourceCalls = 0;
  final Object? setSourceError;

  int playCalls = 0;
  int pauseCalls = 0;
  int disposeCalls = 0;
  Duration? lastSeek;
  int seekCalls = 0;

  final Stream<PlayerState> stateStreamValue;
  final Stream<Duration> positionStreamValue;

  @override
  Stream<PlayerState> get stateStream => stateStreamValue;

  @override
  Stream<Duration> get positionStream => positionStreamValue;

  @override
  Future<void> setSource({
    required String? url,
    String? localPath,
    required MediaItem metadata,
    Map<String, String>? headers,
  }) async {
    setSourceCalls++;
    capturedUrl = url;
    capturedLocalPath = localPath;
    capturedMetadata = metadata;
    capturedHeaders = headers;
    if (setSourceError != null) {
      throw setSourceError!;
    }
  }

  @override
  Future<void> play() async {
    playCalls++;
  }

  @override
  Future<void> pause() async {
    pauseCalls++;
  }

  @override
  Future<void> seek(Duration position) async {
    seekCalls++;
    lastSeek = position;
  }

  @override
  Future<void> dispose() async {
    disposeCalls++;
  }
}

EpisodeDetail _detail({
  String id = 'ep-1',
  bool isDownloaded = false,
  String? audioLocalPath,
  int durationMs = 60_000,
  String title = 'Morning News',
}) {
  final now = DateTime.utc(2026, 4, 5);
  return EpisodeDetail(
    episode: Episode(
      id: id,
      title: title,
      publishedDate: now,
      durationMs: durationMs,
      lastModified: now,
      isDownloaded: isDownloaded,
      audioLocalPath: audioLocalPath,
    ),
    sentences: const <Sentence>[],
  );
}

AppConfig _config({
  String baseUrl = 'http://10.0.0.5:8000',
  String token = 'tkn-xyz',
}) {
  return AppConfig(apiBaseUrl: baseUrl, apiToken: token, env: AppEnv.dev);
}

void main() {
  PlayerAudioDataSource makeDs(_SpyAudio audio, {AppConfig? cfg}) {
    return PlayerAudioDataSource(
      audioService: audio,
      config: cfg ?? _config(),
    );
  }

  group('resolveSource', () {
    test(
        'downloaded with non-empty audioLocalPath → PlaybackSource.local(path)',
        () {
      final audio = _SpyAudio();
      final detail = _detail(
          isDownloaded: true, audioLocalPath: '/var/data/eps/ep-1.mp3');
      final result = makeDs(audio).resolveSource(detail);
      expect(
        result,
        isA<LocalSource>().having(
            (e) => e.path, 'path', '/var/data/eps/ep-1.mp3'),
      );
    });

    test(
        'isDownloaded=true but audioLocalPath is empty → falls back to streaming',
        () {
      final audio = _SpyAudio();
      final detail = _detail(isDownloaded: true, audioLocalPath: '');
      final result = makeDs(audio).resolveSource(detail);
      expect(result, isA<StreamingSource>());
    });

    test('isDownloaded=false → streaming URL with /api/v1/episodes/{id}/audio',
        () {
      final audio = _SpyAudio();
      final detail = _detail(isDownloaded: false, id: 'ep-42');
      final result = makeDs(audio,
              cfg: _config(baseUrl: 'https://api.example.com'))
          .resolveSource(detail);
      expect(
        result,
        isA<StreamingSource>().having(
          (e) => e.url,
          'url',
          'https://api.example.com/api/v1/episodes/ep-42/audio',
        ),
      );
    });
  });

  group('loadEpisode', () {
    test('local source → setSource(url: null, localPath: ..., headers: null)',
        () async {
      final audio = _SpyAudio();
      final detail = _detail(
          isDownloaded: true, audioLocalPath: '/var/data/eps/ep-1.mp3');

      await makeDs(audio).loadEpisode(detail);

      expect(audio.setSourceCalls, 1);
      expect(audio.capturedUrl, isNull,
          reason: 'local branch must pass url=null');
      expect(audio.capturedLocalPath, '/var/data/eps/ep-1.mp3');
      expect(audio.capturedMetadata, isA<MediaItem>());
      expect(audio.capturedHeaders, isNull,
          reason: 'local branch must not pass headers');
    });

    test(
        'streaming source → setSource(url, headers: Authorization: Bearer <token>)',
        () async {
      final audio = _SpyAudio();
      final cfg = _config(baseUrl: 'https://api.example.com', token: 'T-1');
      final detail = _detail(isDownloaded: false, id: 'ep-99');

      await makeDs(audio, cfg: cfg).loadEpisode(detail);

      expect(audio.setSourceCalls, 1);
      expect(audio.capturedUrl,
          'https://api.example.com/api/v1/episodes/ep-99/audio');
      expect(audio.capturedLocalPath, isNull,
          reason: 'streaming branch must not pass localPath');
      expect(audio.capturedMetadata, isA<MediaItem>());
      expect(
        audio.capturedHeaders,
        {'Authorization': 'Bearer T-1'},
        reason: 'Bearer header required for authenticated streaming endpoint',
      );
    });

    test('metadata has correct id / title / album for lock-screen MediaItem',
        () async {
      final audio = _SpyAudio();
      final detail = _detail(id: 'ep-7', title: 'Daily Brief');
      await makeDs(audio).loadEpisode(detail);

      final md = audio.capturedMetadata!;
      expect(md.id, 'ep-7');
      expect(md.title, 'Daily Brief');
      expect(md.album, 'ABC News Daily');
      expect(md.duration, const Duration(milliseconds: 60_000));
    });

    test('durationMs == 0 → MediaItem.duration is null', () async {
      final audio = _SpyAudio();
      final detail = _detail(durationMs: 0);
      await makeDs(audio).loadEpisode(detail);

      expect(audio.capturedMetadata!.duration, isNull);
    });

    test('AudioService error is propagated raw (no wrapping at core boundary)',
        () async {
      final audio = _SpyAudio(setSourceError: PlayerException(403, 'forbidden'));

      await expectLater(
        makeDs(audio).loadEpisode(_detail()),
        throwsA(isA<PlayerException>()),
        reason:
            'data layer surfaces raw just_audio exceptions; repository does the AppException wrapping',
      );
    });
  });

  group('transport delegation', () {
    test('play/pause/seek/dispose delegate to AudioService', () async {
      final audio = _SpyAudio();
      final ds = makeDs(audio);

      await ds.play();
      await ds.pause();
      await ds.seek(const Duration(milliseconds: 42));
      await ds.dispose();

      expect(audio.playCalls, 1);
      expect(audio.pauseCalls, 1);
      expect(audio.seekCalls, 1);
      expect(audio.lastSeek, const Duration(milliseconds: 42));
      expect(audio.disposeCalls, 1);
    });
  });

  group('stream forwarding', () {
    test('playerStateStream + positionStream forward AudioService streams',
        () async {
      final positionCtrl = StreamController<Duration>.broadcast();
      final stateCtrl = StreamController<PlayerState>.broadcast();
      addTearDown(() async {
        await positionCtrl.close();
        await stateCtrl.close();
      });

      final audio = _SpyAudio(
        positionStreamValue: positionCtrl.stream,
        stateStreamValue: stateCtrl.stream,
      );

      final ds = makeDs(audio);

      final positions = <Duration>[];
      final states = <PlayerState>[];
      final psSub = ds.positionStream.listen(positions.add);
      final ssSub = ds.playerStateStream.listen(states.add);
      addTearDown(() async {
        await psSub.cancel();
        await ssSub.cancel();
      });

      positionCtrl.add(const Duration(milliseconds: 100));
      stateCtrl.add(PlayerState(true, ProcessingState.ready));

      // Let the microtask queue drain so listeners fire.
      await Future<void>.delayed(Duration.zero);

      expect(positions, [const Duration(milliseconds: 100)]);
      expect(states.single.playing, isTrue);
      expect(states.single.processingState, ProcessingState.ready);
    });
  });
}
