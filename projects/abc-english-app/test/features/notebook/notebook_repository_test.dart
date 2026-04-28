import 'package:abc_english_app/core/connectivity/connectivity_service.dart';
import 'package:abc_english_app/core/errors/app_exception.dart';
import 'package:abc_english_app/core/errors/result.dart';
import 'package:abc_english_app/features/notebook/data/datasources/notebook_local_datasource.dart';
import 'package:abc_english_app/features/notebook/data/datasources/notebook_remote_datasource.dart';
import 'package:abc_english_app/features/notebook/data/models/notebook_entry_dto.dart';
import 'package:abc_english_app/features/notebook/data/repositories/notebook_repository_impl.dart';
import 'package:abc_english_app/features/notebook/domain/entities/notebook_entry.dart';
import 'package:abc_english_app/features/notebook/domain/entities/sync_status.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class _MockRemote extends Mock implements NotebookRemoteDataSource {}

class _MockLocal extends Mock implements NotebookLocalDataSource {}

class _MockConn extends Mock implements ConnectivityService {}

class _NotebookEntryFake extends Fake implements NotebookEntry {}

NotebookEntry _entity({
  String id = 'nb-local-1',
  String word = 'w',
  SyncStatus status = SyncStatus.synced,
  DateTime? when,
}) {
  final t = when ?? DateTime.utc(2026, 4, 5);
  return NotebookEntry(
    id: id,
    word: word,
    context: 'c',
    createdAt: t,
    lastModified: t,
    syncStatus: status,
  );
}

NotebookEntryDto _serverDto({String id = 'server-1', String word = 'w'}) {
  return NotebookEntryDto(
    id: id,
    word: word,
    context: 'c',
    createdAt: '2026-04-05T12:00:00Z',
    lastModified: '2026-04-05T12:00:00Z',
  );
}

void main() {
  setUpAll(() {
    registerFallbackValue(_NotebookEntryFake());
  });

  late _MockRemote remote;
  late _MockLocal local;
  late _MockConn conn;

  setUp(() {
    remote = _MockRemote();
    local = _MockLocal();
    conn = _MockConn();
    // Common setup noise — not verified in every test.
    when(() => local.upsert(any())).thenAnswer((_) async {});
    when(() => local.remove(any())).thenAnswer((_) async => 1);
    when(() => local.hardDelete(any())).thenAnswer((_) async => 1);
    when(() => local.markDeleted(any(), any())).thenAnswer((_) async {});
  });

  // Nested inside `main()`; avoid leading-underscore lint.
  NotebookRepositoryImpl makeRepo({
    String Function()? id,
    DateTime Function()? clock,
  }) {
    return NotebookRepositoryImpl(
      remote: remote,
      local: local,
      connectivity: conn,
      idGenerator: id ?? () => 'nb-local-1',
      clock: clock ?? () => DateTime.utc(2026, 4, 5, 12),
    );
  }

  group('list', () {
    test('returns local rows as Success', () async {
      when(() => local.getAll(sinceModified: any(named: 'sinceModified')))
          .thenAnswer((_) async => [_entity(id: 'nb-1')]);

      final repo = makeRepo();
      final r = await repo.list();
      expect(r, isA<Success<List<NotebookEntry>>>());
      expect((r as Success<List<NotebookEntry>>).value.single.id, 'nb-1');
    });

    test('storage exception → Failure', () async {
      when(() => local.getAll(sinceModified: any(named: 'sinceModified')))
          .thenThrow(const StorageException('boom'));

      final r = await makeRepo().list();
      expect(r, isA<Failure<List<NotebookEntry>>>());
      expect((r as Failure<List<NotebookEntry>>).error,
          isA<StorageException>());
    });
  });

  group('add', () {
    test('online: local upsert → remote create → local upsert (server id)',
        () async {
      when(() => conn.isOnline()).thenAnswer((_) async => true);
      when(() => remote.create(
            word: any(named: 'word'),
            context: any(named: 'context'),
            episodeId: any(named: 'episodeId'),
            sentenceIndex: any(named: 'sentenceIndex'),
            meaning: any(named: 'meaning'),
            note: any(named: 'note'),
          )).thenAnswer((_) async => _serverDto(id: 'srv-1', word: 'albeit'));

      final repo = makeRepo();
      final r = await repo.add(word: 'albeit', context: 'x');

      expect(r, isA<Success<NotebookEntry>>());
      final entry = (r as Success<NotebookEntry>).value;
      expect(entry.id, 'srv-1');
      expect(entry.syncStatus, SyncStatus.synced);

      // First upsert = local pending, second = synced server entity.
      verify(() => local.upsert(any())).called(2);
      // Local id differed, so temp row was removed.
      verify(() => local.remove('nb-local-1')).called(1);
    });

    test('offline: local upsert only, returns pendingUpsert', () async {
      when(() => conn.isOnline()).thenAnswer((_) async => false);

      final repo = makeRepo();
      final r = await repo.add(word: 'albeit', context: 'x');

      expect(r, isA<Success<NotebookEntry>>());
      final entry = (r as Success<NotebookEntry>).value;
      expect(entry.id, 'nb-local-1');
      expect(entry.syncStatus, SyncStatus.pendingUpsert);

      verify(() => local.upsert(any())).called(1);
      verifyNever(() => remote.create(
            word: any(named: 'word'),
            context: any(named: 'context'),
            episodeId: any(named: 'episodeId'),
            sentenceIndex: any(named: 'sentenceIndex'),
            meaning: any(named: 'meaning'),
            note: any(named: 'note'),
          ));
    });

    test('online + remote AppException → Failure', () async {
      when(() => conn.isOnline()).thenAnswer((_) async => true);
      when(() => remote.create(
            word: any(named: 'word'),
            context: any(named: 'context'),
            episodeId: any(named: 'episodeId'),
            sentenceIndex: any(named: 'sentenceIndex'),
            meaning: any(named: 'meaning'),
            note: any(named: 'note'),
          )).thenThrow(const NetworkException('no net'));

      final r = await makeRepo().add(word: 'x', context: 'y');
      expect(r, isA<Failure<NotebookEntry>>());
      expect((r as Failure<NotebookEntry>).error, isA<NetworkException>());
    });
  });

  group('update', () {
    test('unknown id → Failure(NotFoundException)', () async {
      when(() => local.getById(any())).thenAnswer((_) async => null);
      final r = await makeRepo().update(id: 'missing', meaning: 'x');
      expect(r, isA<Failure<NotebookEntry>>());
      expect((r as Failure<NotebookEntry>).error, isA<NotFoundException>());
    });

    test('online: local upsert + remote patch + local upsert', () async {
      when(() => local.getById('nb-1'))
          .thenAnswer((_) async => _entity(id: 'nb-1', word: 'old'));
      when(() => conn.isOnline()).thenAnswer((_) async => true);
      when(() => remote.patch(
            id: any(named: 'id'),
            word: any(named: 'word'),
            context: any(named: 'context'),
            episodeId: any(named: 'episodeId'),
            sentenceIndex: any(named: 'sentenceIndex'),
            meaning: any(named: 'meaning'),
            note: any(named: 'note'),
          )).thenAnswer((_) async => _serverDto(id: 'nb-1', word: 'new'));

      final r = await makeRepo().update(id: 'nb-1', word: 'new');
      expect(r, isA<Success<NotebookEntry>>());
      final entry = (r as Success<NotebookEntry>).value;
      expect(entry.word, 'new');
      expect(entry.syncStatus, SyncStatus.synced);
      // First upsert pending, second synced server-returned entity.
      verify(() => local.upsert(any())).called(2);
    });

    test('offline: pendingUpsert with bumped lastModified', () async {
      final old = DateTime.utc(2026, 4, 1);
      when(() => local.getById('nb-1'))
          .thenAnswer((_) async => _entity(id: 'nb-1', when: old));
      when(() => conn.isOnline()).thenAnswer((_) async => false);

      final repo = makeRepo(clock: () => DateTime.utc(2026, 4, 5, 12));
      final r = await repo.update(id: 'nb-1', meaning: 'm');

      expect(r, isA<Success<NotebookEntry>>());
      final entry = (r as Success<NotebookEntry>).value;
      expect(entry.meaning, 'm');
      expect(entry.syncStatus, SyncStatus.pendingUpsert);
      expect(entry.lastModified.isAfter(old), isTrue,
          reason: 'lastModified must advance on write');
      verifyNever(() => remote.patch(
            id: any(named: 'id'),
            word: any(named: 'word'),
            context: any(named: 'context'),
            episodeId: any(named: 'episodeId'),
            sentenceIndex: any(named: 'sentenceIndex'),
            meaning: any(named: 'meaning'),
            note: any(named: 'note'),
          ));
    });
  });

  group('remove', () {
    test('online: local remove + remote delete', () async {
      when(() => conn.isOnline()).thenAnswer((_) async => true);
      when(() => remote.delete('nb-1')).thenAnswer((_) async {});

      final r = await makeRepo().remove('nb-1');
      expect(r, isA<Success<void>>());
      verify(() => local.remove('nb-1')).called(1);
      verify(() => remote.delete('nb-1')).called(1);
    });

    test('offline: markDeleted tombstone, no hard delete, no remote call',
        () async {
      when(() => conn.isOnline()).thenAnswer((_) async => false);

      final r = await makeRepo().remove('nb-1');
      expect(r, isA<Success<void>>());
      // Offline path stamps a tombstone instead of hard-deleting so the
      // sync engine can still see the pending delete.
      verify(() => local.markDeleted('nb-1', any())).called(1);
      verifyNever(() => local.remove(any()));
      verifyNever(() => local.hardDelete(any()));
      verifyNever(() => remote.delete(any()));
    });

    test('online + remote 404 treated as success (server already gone)',
        () async {
      when(() => conn.isOnline()).thenAnswer((_) async => true);
      when(() => remote.delete('nb-1'))
          .thenThrow(const NotFoundException('gone'));

      final r = await makeRepo().remove('nb-1');
      expect(r, isA<Success<void>>());
    });

    test('online + other AppException → Failure', () async {
      when(() => conn.isOnline()).thenAnswer((_) async => true);
      when(() => remote.delete('nb-1'))
          .thenThrow(const NetworkException('down'));

      final r = await makeRepo().remove('nb-1');
      expect(r, isA<Failure<void>>());
      expect((r as Failure<void>).error, isA<NetworkException>());
    });
  });
}
