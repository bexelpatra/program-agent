import 'package:abc_english_app/core/domain/entities/episode.dart';
import 'package:abc_english_app/core/errors/app_exception.dart';
import 'package:abc_english_app/core/errors/result.dart';
import 'package:abc_english_app/features/episode_detail/domain/entities/episode_detail.dart';
import 'package:abc_english_app/features/player/domain/entities/playback_state.dart';
import 'package:abc_english_app/features/player/domain/repositories/player_repository.dart';
import 'package:abc_english_app/features/player/domain/usecases/jump_to_sentence.dart';
import 'package:abc_english_app/features/player/domain/usecases/load_episode.dart';
import 'package:abc_english_app/features/player/domain/usecases/play_pause.dart';
import 'package:abc_english_app/features/player/domain/usecases/seek_to.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class _MockRepo extends Mock implements PlayerRepository {}

class _FakeEpisodeDetail extends Fake implements EpisodeDetail {}

Sentence _s(int i, int startMs, int endMs) =>
    Sentence(index: i, text: 'sentence $i', startMs: startMs, endMs: endMs);

EpisodeDetail _detail() {
  final now = DateTime.utc(2026, 4, 22);
  return EpisodeDetail(
    episode: Episode(
      id: 'ep-1',
      title: 'Episode',
      publishedDate: now,
      durationMs: 60000,
      lastModified: now,
      isDownloaded: false,
    ),
    sentences: [_s(0, 0, 1000), _s(1, 1000, 2000)],
  );
}

void main() {
  setUpAll(() {
    registerFallbackValue(_FakeEpisodeDetail());
    registerFallbackValue(Duration.zero);
  });

  late _MockRepo repo;

  setUp(() {
    repo = _MockRepo();
  });

  group('LoadEpisode', () {
    test('delegates to repository.loadEpisode and returns its Result',
        () async {
      when(() => repo.loadEpisode(any()))
          .thenAnswer((_) async => const Success<void>(null));
      final useCase = LoadEpisode(repo);
      final detail = _detail();

      final r = await useCase(detail);
      expect(r, isA<Success<void>>());
      verify(() => repo.loadEpisode(detail)).called(1);
    });

    test('propagates Failure as-is', () async {
      when(() => repo.loadEpisode(any())).thenAnswer(
        (_) async =>
            const Failure<void>(NetworkException('no net')),
      );
      final r = await LoadEpisode(repo)(_detail());
      expect(r, isA<Failure<void>>());
      expect((r as Failure<void>).error, isA<NetworkException>());
    });
  });

  group('PlayPause', () {
    test('currently playing → pauses', () async {
      when(() => repo.pause())
          .thenAnswer((_) async => const Success<void>(null));
      final useCase = PlayPause(repo);

      final r = await useCase(PlaybackState.initial().copyWith(isPlaying: true));
      expect(r, isA<Success<void>>());
      verify(() => repo.pause()).called(1);
      verifyNever(() => repo.play());
    });

    test('currently paused → plays', () async {
      when(() => repo.play())
          .thenAnswer((_) async => const Success<void>(null));
      final useCase = PlayPause(repo);

      final r = await useCase(PlaybackState.initial());
      expect(r, isA<Success<void>>());
      verify(() => repo.play()).called(1);
      verifyNever(() => repo.pause());
    });
  });

  group('SeekTo', () {
    test('delegates to repository.seek', () async {
      when(() => repo.seek(any()))
          .thenAnswer((_) async => const Success<void>(null));
      final useCase = SeekTo(repo);
      const target = Duration(milliseconds: 4200);

      final r = await useCase(target);
      expect(r, isA<Success<void>>());
      verify(() => repo.seek(target)).called(1);
    });
  });

  group('JumpToSentence', () {
    test('valid index → seeks to Duration(sentence.startMs)', () async {
      when(() => repo.seek(any()))
          .thenAnswer((_) async => const Success<void>(null));
      final useCase = JumpToSentence(repo);
      final sentences = [_s(0, 0, 1000), _s(1, 1500, 2500)];

      final r = await useCase(1, sentences);
      expect(r, isA<Success<void>>());
      verify(() =>
              repo.seek(const Duration(milliseconds: 1500)))
          .called(1);
    });

    test('negative index → Failure(NotFoundException) without repo call',
        () async {
      final sentences = [_s(0, 0, 1000)];
      final r = await JumpToSentence(repo)(-1, sentences);
      expect(r, isA<Failure<void>>());
      expect((r as Failure<void>).error, isA<NotFoundException>());
      verifyNever(() => repo.seek(any()));
    });

    test('out-of-range index → Failure(NotFoundException) without repo call',
        () async {
      final sentences = [_s(0, 0, 1000)];
      final r = await JumpToSentence(repo)(5, sentences);
      expect(r, isA<Failure<void>>());
      expect((r as Failure<void>).error, isA<NotFoundException>());
      verifyNever(() => repo.seek(any()));
    });
  });
}
