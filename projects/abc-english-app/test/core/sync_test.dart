import 'package:abc_english_app/core/connectivity/connectivity_service.dart';
import 'package:abc_english_app/core/errors/app_exception.dart';
import 'package:abc_english_app/core/sync/sync_engine.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

/// Tiny fake entity used to exercise the generic engine.
class _FakeEntity implements SyncableEntity {
  _FakeEntity(this.id, this.lastModified, {this.payload = ''});
  @override
  final String id;
  @override
  final DateTime lastModified;
  final String payload;

  @override
  String toString() => 'FakeEntity($id, lm=$lastModified, p=$payload)';
}

class _MockConnectivity extends Mock implements ConnectivityService {}

void main() {
  setUpAll(() {
    registerFallbackValue(_FakeEntity('__fallback__', DateTime(2026)));
  });

  group('SyncEngine', () {
    late _MockConnectivity connectivity;
    late List<_FakeEntity> upserted;
    late List<_FakeEntity> pushed;

    setUp(() {
      connectivity = _MockConnectivity();
      upserted = <_FakeEntity>[];
      pushed = <_FakeEntity>[];
    });

    SyncEngine<_FakeEntity> buildEngine({
      required List<_FakeEntity> pending,
      required List<_FakeEntity> remote,
      Future<_FakeEntity> Function(_FakeEntity)? pushOverride,
    }) {
      return SyncEngine<_FakeEntity>(
        connectivity: connectivity,
        fetchRemote: () async => remote,
        getLocalPending: () async => pending,
        pushLocal: pushOverride ??
            (e) async {
              pushed.add(e);
              return e;
            },
        upsertLocal: (e) async {
          upserted.add(e);
        },
      );
    }

    test('offline → SyncSkipped', () async {
      when(() => connectivity.isOnline()).thenAnswer((_) async => false);

      final engine = buildEngine(pending: [], remote: []);
      final result = await engine.sync();

      expect(result, isA<SyncSkipped>());
      expect(pushed, isEmpty);
      expect(upserted, isEmpty);
    });

    test('online + nothing pending + nothing remote → success(0, 0)',
        () async {
      when(() => connectivity.isOnline()).thenAnswer((_) async => true);

      final engine = buildEngine(pending: [], remote: []);
      final result = await engine.sync();

      expect(result, isA<SyncSuccess>());
      final success = result as SyncSuccess;
      expect(success.applied, 0);
      expect(success.conflicts, 0);
      expect(pushed, isEmpty);
      expect(upserted, isEmpty);
    });

    test('online + 1 local pending, no remote → push, applied=1', () async {
      when(() => connectivity.isOnline()).thenAnswer((_) async => true);

      final localOnly = _FakeEntity('e1', DateTime.utc(2026, 4, 1));
      final engine = buildEngine(pending: [localOnly], remote: []);
      final result = await engine.sync();

      expect(result, isA<SyncSuccess>());
      final success = result as SyncSuccess;
      expect(success.applied, 1);
      expect(success.conflicts, 0);
      expect(pushed, equals([localOnly]));
      expect(upserted, equals([localOnly]));
    });

    test('online + same id both sides, remote newer → conflict, server wins',
        () async {
      when(() => connectivity.isOnline()).thenAnswer((_) async => true);

      final local = _FakeEntity(
        'e1',
        DateTime.utc(2026, 4, 1, 10),
        payload: 'local',
      );
      final remote = _FakeEntity(
        'e1',
        DateTime.utc(2026, 4, 1, 12), // newer
        payload: 'remote',
      );

      final engine = buildEngine(pending: [local], remote: [remote]);
      final result = await engine.sync();

      expect(result, isA<SyncSuccess>());
      final success = result as SyncSuccess;
      expect(success.conflicts, 1);
      expect(success.applied, 1, reason: 'push of local still counts');

      // 1st upsert = echo of push (local), 2nd upsert = remote winner.
      expect(upserted.length, 2);
      expect(upserted.first.payload, 'local');
      expect(upserted.last.payload, 'remote');
      expect(pushed, equals([local]));
    });

    test('online + same id both sides, local newer → push, no conflict bump '
        'for data but server still echoes back (LWW keeps local)', () async {
      when(() => connectivity.isOnline()).thenAnswer((_) async => true);

      final local = _FakeEntity(
        'e1',
        DateTime.utc(2026, 4, 1, 15), // newer
        payload: 'local',
      );
      final remote = _FakeEntity(
        'e1',
        DateTime.utc(2026, 4, 1, 10),
        payload: 'remote',
      );

      final engine = buildEngine(pending: [local], remote: [remote]);
      final result = await engine.sync();

      expect(result, isA<SyncSuccess>());
      final success = result as SyncSuccess;
      // Conflict count increments whenever both sides have this id, but the
      // resolution favours local because local.lastModified > remote.
      expect(success.conflicts, 1);
      expect(pushed, equals([local]));
      // 1st upsert = local echo from push; 2nd upsert = local again as
      // LWW winner.
      expect(upserted.length, 2);
      expect(upserted.map((e) => e.payload), [ 'local', 'local']);
    });

    test('pushLocal throws AppException → SyncFailed', () async {
      when(() => connectivity.isOnline()).thenAnswer((_) async => true);

      final localOnly = _FakeEntity('e1', DateTime.utc(2026, 4, 1));
      final engine = buildEngine(
        pending: [localOnly],
        remote: [],
        pushOverride: (_) async =>
            throw const NetworkException('boom'),
      );

      final result = await engine.sync();

      expect(result, isA<SyncFailed>());
      final failed = result as SyncFailed;
      expect(failed.error, isA<NetworkException>());
      expect(failed.error.message, 'boom');
    });

    test('pushLocal throws non-AppException → wrapped in UnknownException',
        () async {
      when(() => connectivity.isOnline()).thenAnswer((_) async => true);

      final localOnly = _FakeEntity('e1', DateTime.utc(2026, 4, 1));
      final engine = buildEngine(
        pending: [localOnly],
        remote: [],
        pushOverride: (_) async => throw StateError('oops'),
      );

      final result = await engine.sync();

      expect(result, isA<SyncFailed>());
      final failed = result as SyncFailed;
      expect(failed.error, isA<UnknownException>());
    });
  });
}
