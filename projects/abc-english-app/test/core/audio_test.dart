import 'dart:async';

import 'package:abc_english_app/core/audio/audio_service.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:just_audio/just_audio.dart';
import 'package:just_audio_background/just_audio_background.dart';
import 'package:mocktail/mocktail.dart';

/// just_audio opens platform channels (audio_session) the moment an
/// `AudioPlayer` is constructed, which is not available from the pure-Dart
/// test VM. We therefore inject a mock [AudioPlayer] — `AudioService`
/// accepts one via its optional `player` parameter specifically for this
/// reason.
///
/// Scope: this file only exercises the pure-Dart argument-validation path
/// and the API surface. Real playback / lock-screen / streaming behaviour
/// lives in `integration_test/` (see TASK-055 / TASK-070).

class _MockAudioPlayer extends Mock implements AudioPlayer {}

class _FakeAudioSource extends Fake implements AudioSource {}

void main() {
  setUpAll(() {
    registerFallbackValue(_FakeAudioSource());
  });

  late _MockAudioPlayer player;

  setUp(() {
    player = _MockAudioPlayer();
    when(() => player.positionStream)
        .thenAnswer((_) => const Stream<Duration>.empty());
    when(() => player.playerStateStream)
        .thenAnswer((_) => const Stream<PlayerState>.empty());
    when(() => player.dispose()).thenAnswer((_) async {});
  });

  group('AudioService.setSource', () {
    test(
      'throws ArgumentError when both url and localPath are null',
      () async {
        final service = AudioService(player: player);

        await expectLater(
          service.setSource(
            url: null,
            metadata: MediaItem(id: 'x', title: 'x'),
          ),
          throwsA(isA<ArgumentError>()),
        );

        // Must not have touched the platform layer.
        verifyNever(() => player.setAudioSource(any()));
      },
    );
  });

  group('AudioService — public API surface', () {
    test('exposes positionStream and stateStream and dispose', () async {
      final service = AudioService(player: player);

      expect(service.positionStream, isA<Stream<Duration>>());
      expect(service.stateStream, isA<Stream<PlayerState>>());

      await service.dispose();
      verify(() => player.dispose()).called(1);
    });
  });
}
