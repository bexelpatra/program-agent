import 'package:abc_english_app/core/connectivity/connectivity_service.dart';
import 'package:abc_english_app/core/domain/entities/episode.dart';
import 'package:abc_english_app/core/errors/app_exception.dart';
import 'package:abc_english_app/core/errors/result.dart';
import 'package:abc_english_app/features/episode_list/data/datasources/episode_local_datasource.dart';
import 'package:abc_english_app/features/episode_list/data/datasources/episode_remote_datasource.dart';
import 'package:abc_english_app/features/episode_list/data/models/episode_dto.dart';
import 'package:abc_english_app/features/episode_list/data/repositories/episode_repository_impl.dart';
import 'package:abc_english_app/features/episode_list/domain/usecases/list_episodes.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class _MockRemote extends Mock implements EpisodeRemoteDataSource {}

class _MockLocal extends Mock implements EpisodeLocalDataSource {}

class _MockConn extends Mock implements ConnectivityService {}

class _EpisodeFake extends Fake implements Episode {}

EpisodeDto _dto({
  String id = 'ep-1',
  String title = 'Title',
  String date = '2026-04-01',
  int? dur = 60,
}) {
  return EpisodeDto(
    id: id,
    title: title,
    publishedDate: date,
    durationSeconds: dur,
    avgWer: null,
    lastModified: null,
  );
}

Episode _entity({
  String id = 'ep-1',
  bool isDownloaded = false,
  String? audioLocalPath,
}) {
  final now = DateTime.utc(2026, 4, 1);
  return Episode(
    id: id,
    title: 't',
    publishedDate: now,
    durationMs: 60000,
    lastModified: now,
    isDownloaded: isDownloaded,
    audioLocalPath: audioLocalPath,
  );
}

void main() {
  setUpAll(() {
    registerFallbackValue(_EpisodeFake());
    registerFallbackValue(<Episode>[]);
  });

  late _MockRemote remote;
  late _MockLocal local;
  late _MockConn conn;
  late EpisodeRepositoryImpl repo;

  setUp(() {
    remote = _MockRemote();
    local = _MockLocal();
    conn = _MockConn();
    repo = EpisodeRepositoryImpl(
      remote: remote,
      local: local,
      connectivity: conn,
    );
  });

  group('listEpisodes', () {
    test('online: remote fetch → upsertMany → Success with merged entities',
        () async {
      when(() => conn.isOnline()).thenAnswer((_) async => true);
      when(() => remote.fetchEpisodes(
            page: any(named: 'page'),
            size: any(named: 'size'),
            sinceModified: any(named: 'sinceModified'),
          )).thenAnswer((_) async => [
            _dto(id: 'ep-1'),
            _dto(id: 'ep-2'),
          ]);
      // Local mirror holds ep-1 marked as downloaded.
      when(() => local.getAll()).thenAnswer((_) async => [
            _entity(id: 'ep-1', isDownloaded: true, audioLocalPath: '/a.mp3'),
          ]);
      when(() => local.upsertMany(any())).thenAnswer((_) async {});

      final result = await repo.listEpisodes();

      expect(result, isA<Success<List<Episode>>>());
      final list = (result as Success<List<Episode>>).value;
      expect(list, hasLength(2));
      expect(list.firstWhere((e) => e.id == 'ep-1').isDownloaded, isTrue,
          reason: 'local download flag merged in');
      expect(list.firstWhere((e) => e.id == 'ep-1').audioLocalPath, '/a.mp3');
      expect(list.firstWhere((e) => e.id == 'ep-2').isDownloaded, isFalse);

      verify(() => remote.fetchEpisodes(
            page: 1,
            size: 20,
            sinceModified: null,
          )).called(1);
      verify(() => local.upsertMany(any())).called(1);
    });

    test('offline: returns local.getAll() without touching remote', () async {
      when(() => conn.isOnline()).thenAnswer((_) async => false);
      when(() => local.getAll()).thenAnswer((_) async => [
            _entity(id: 'ep-local'),
          ]);

      final result = await repo.listEpisodes();
      expect(result, isA<Success<List<Episode>>>());
      expect((result as Success<List<Episode>>).value.single.id, 'ep-local');
      verifyNever(() => remote.fetchEpisodes(
            page: any(named: 'page'),
            size: any(named: 'size'),
            sinceModified: any(named: 'sinceModified'),
          ));
    });

    test('online + remote throws AppException → Failure(AppException)',
        () async {
      when(() => conn.isOnline()).thenAnswer((_) async => true);
      when(() => remote.fetchEpisodes(
            page: any(named: 'page'),
            size: any(named: 'size'),
            sinceModified: any(named: 'sinceModified'),
          )).thenThrow(const NetworkException('boom'));
      when(() => local.getAll()).thenAnswer((_) async => <Episode>[]);

      final result = await repo.listEpisodes();
      expect(result, isA<Failure<List<Episode>>>());
      expect((result as Failure<List<Episode>>).error, isA<NetworkException>());
    });

    test('online + remote throws non-AppException → Failure(UnknownException)',
        () async {
      when(() => conn.isOnline()).thenAnswer((_) async => true);
      when(() => remote.fetchEpisodes(
            page: any(named: 'page'),
            size: any(named: 'size'),
            sinceModified: any(named: 'sinceModified'),
          )).thenThrow(Exception('raw'));
      when(() => local.getAll()).thenAnswer((_) async => <Episode>[]);

      final result = await repo.listEpisodes();
      expect(result, isA<Failure<List<Episode>>>());
      expect(
          (result as Failure<List<Episode>>).error, isA<UnknownException>());
    });
  });

  group('getById', () {
    test('local hit → Success without touching remote', () async {
      when(() => local.getById('ep-1'))
          .thenAnswer((_) async => _entity(id: 'ep-1'));

      final result = await repo.getById('ep-1');
      expect(result, isA<Success<Episode>>());
      verifyNever(() => remote.fetchById(any()));
      verifyNever(() => conn.isOnline());
    });

    test('local miss + offline → Failure(NotFoundException)', () async {
      when(() => local.getById(any())).thenAnswer((_) async => null);
      when(() => conn.isOnline()).thenAnswer((_) async => false);

      final result = await repo.getById('ep-missing');
      expect(result, isA<Failure<Episode>>());
      expect((result as Failure<Episode>).error, isA<NotFoundException>());
    });

    test('local miss + online → remote fetch + upsert + Success', () async {
      when(() => local.getById(any())).thenAnswer((_) async => null);
      when(() => conn.isOnline()).thenAnswer((_) async => true);
      when(() => remote.fetchById('ep-x'))
          .thenAnswer((_) async => _dto(id: 'ep-x'));
      when(() => local.upsert(any())).thenAnswer((_) async {});

      final result = await repo.getById('ep-x');
      expect(result, isA<Success<Episode>>());
      verify(() => local.upsert(any())).called(1);
    });
  });

  group('ListEpisodes UseCase delegation', () {
    test('calls repository.listEpisodes with forwarded args', () async {
      when(() => conn.isOnline()).thenAnswer((_) async => false);
      when(() => local.getAll()).thenAnswer((_) async => <Episode>[]);

      final useCase = ListEpisodes(repo);
      await useCase(
        page: 3,
        size: 15,
        sinceModified: DateTime.utc(2026, 4, 1),
      );
      // Offline path reached local — confirms call propagated through repo.
      verify(() => local.getAll()).called(1);
    });
  });
}
