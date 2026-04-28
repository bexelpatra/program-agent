import 'package:abc_english_app/core/connectivity/connectivity_service.dart';
import 'package:abc_english_app/core/domain/entities/episode.dart';
import 'package:abc_english_app/core/errors/app_exception.dart';
import 'package:abc_english_app/core/errors/result.dart';
import 'package:abc_english_app/features/episode_detail/data/datasources/episode_detail_local_datasource.dart';
import 'package:abc_english_app/features/episode_detail/data/datasources/episode_detail_remote_datasource.dart';
import 'package:abc_english_app/features/episode_detail/data/models/episode_detail_dto.dart';
import 'package:abc_english_app/features/episode_detail/data/models/sentence_dto.dart';
import 'package:abc_english_app/features/episode_detail/data/repositories/episode_detail_repository_impl.dart';
import 'package:abc_english_app/features/episode_detail/domain/entities/episode_detail.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class _MockRemote extends Mock implements EpisodeDetailRemoteDataSource {}

class _MockLocal extends Mock implements EpisodeDetailLocalDataSource {}

class _MockConn extends Mock implements ConnectivityService {}

class _EpisodeFake extends Fake implements Episode {}

Episode _ep({bool isDownloaded = false, String? audio}) {
  final now = DateTime.utc(2026, 4, 5);
  return Episode(
    id: 'ep-1',
    title: 't',
    publishedDate: now,
    durationMs: 60000,
    lastModified: now,
    isDownloaded: isDownloaded,
    audioLocalPath: audio,
  );
}

EpisodeDetail _detail({bool isDownloaded = false, List<Sentence>? sentences}) {
  return EpisodeDetail(
    episode: _ep(isDownloaded: isDownloaded, audio: isDownloaded ? '/a.mp3' : null),
    sentences: sentences ??
        const [
          Sentence(index: 0, text: 'hi', startMs: 0, endMs: 500),
        ],
  );
}

EpisodeDetailDto _remoteDto() {
  return EpisodeDetailDto(
    id: 'ep-1',
    title: 'T',
    publishedDate: '2026-04-05',
    durationSeconds: 60,
    sentences: const [
      SentenceDto(
        index: 0,
        text: 'remote sent',
        startMs: 0,
        endMs: 500,
      ),
    ],
  );
}

void main() {
  setUpAll(() {
    registerFallbackValue(_EpisodeFake());
    registerFallbackValue(<Sentence>[]);
  });

  late _MockRemote remote;
  late _MockLocal local;
  late _MockConn conn;
  late EpisodeDetailRepositoryImpl repo;

  setUp(() {
    remote = _MockRemote();
    local = _MockLocal();
    conn = _MockConn();
    repo = EpisodeDetailRepositoryImpl(
      remote: remote,
      local: local,
      connectivity: conn,
    );
    when(() => local.upsertEpisode(any())).thenAnswer((_) async {});
    when(() => local.upsertSentences(any(), any())).thenAnswer((_) async {});
  });

  group('getDetail', () {
    test('downloaded + sentences → serves local without touching remote',
        () async {
      when(() => local.getDetail('ep-1'))
          .thenAnswer((_) async => _detail(isDownloaded: true));

      final result = await repo.getDetail('ep-1');
      expect(result, isA<Success<EpisodeDetail>>());
      verifyNever(() => remote.fetchDetail(any()));
      verifyNever(() => conn.isOnline());
    });

    test('not downloaded + online → remote, upsert, return fresh', () async {
      when(() => local.getDetail('ep-1')).thenAnswer((_) async => null);
      when(() => conn.isOnline()).thenAnswer((_) async => true);
      when(() => remote.fetchDetail('ep-1'))
          .thenAnswer((_) async => _remoteDto());

      final result = await repo.getDetail('ep-1');
      expect(result, isA<Success<EpisodeDetail>>());
      final detail = (result as Success<EpisodeDetail>).value;
      expect(detail.sentences.single.text, 'remote sent');
      verify(() => local.upsertEpisode(any())).called(1);
      verify(() => local.upsertSentences('ep-1', any())).called(1);
    });

    test('not downloaded + offline + local cache → serve cache', () async {
      when(() => local.getDetail('ep-1'))
          .thenAnswer((_) async => _detail(isDownloaded: false));
      when(() => conn.isOnline()).thenAnswer((_) async => false);

      final result = await repo.getDetail('ep-1');
      expect(result, isA<Success<EpisodeDetail>>());
      verifyNever(() => remote.fetchDetail(any()));
    });

    test('offline + no cache → Failure(NotFoundException)', () async {
      when(() => local.getDetail(any())).thenAnswer((_) async => null);
      when(() => conn.isOnline()).thenAnswer((_) async => false);

      final result = await repo.getDetail('ep-1');
      expect(result, isA<Failure<EpisodeDetail>>());
      expect((result as Failure<EpisodeDetail>).error,
          isA<NotFoundException>());
    });

    test('online + remote throws AppException → Failure', () async {
      when(() => local.getDetail(any())).thenAnswer((_) async => null);
      when(() => conn.isOnline()).thenAnswer((_) async => true);
      when(() => remote.fetchDetail(any()))
          .thenThrow(const NetworkException('down'));

      final result = await repo.getDetail('ep-1');
      expect(result, isA<Failure<EpisodeDetail>>());
      expect((result as Failure<EpisodeDetail>).error,
          isA<NetworkException>());
    });

    test('cached-not-downloaded + online still refetches remote', () async {
      // Downloaded=false and cached — repository should NOT short-circuit here,
      // it should fetch remote and upsert.
      when(() => local.getDetail('ep-1'))
          .thenAnswer((_) async => _detail(isDownloaded: false));
      when(() => conn.isOnline()).thenAnswer((_) async => true);
      when(() => remote.fetchDetail('ep-1'))
          .thenAnswer((_) async => _remoteDto());

      final result = await repo.getDetail('ep-1');
      expect(result, isA<Success<EpisodeDetail>>());
      verify(() => remote.fetchDetail('ep-1')).called(1);
    });
  });
}
