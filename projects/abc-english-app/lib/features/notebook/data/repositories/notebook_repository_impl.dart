import 'dart:math' as math;

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/connectivity/connectivity_service.dart';
import '../../../../core/errors/app_exception.dart';
import '../../../../core/errors/result.dart';
import '../../../../core/network/dio_client.dart';
import '../../../../core/storage/app_database.dart';
import '../../domain/entities/notebook_entry.dart';
import '../../domain/entities/sync_status.dart';
import '../../domain/repositories/notebook_repository.dart';
import '../datasources/notebook_local_datasource.dart';
import '../datasources/notebook_remote_datasource.dart';
import '../sync/notebook_sync_service.dart';

/// Local-first notebook repository.
///
/// Reads are served from drift (offline-safe). Writes are persisted locally
/// first, then — if online — immediately pushed to the server. Offline
/// writes stay as `pendingUpsert`/`pendingDelete` until a sync engine
/// drains them (outside this task's scope).
///
/// Periodic reconciliation with the server list endpoint is not handled
/// here; a dedicated UseCase / sync engine owns that flow so callers of
/// `list` always get the local snapshot instantly.
class NotebookRepositoryImpl implements NotebookRepository {
  NotebookRepositoryImpl({
    required NotebookRemoteDataSource remote,
    required NotebookLocalDataSource local,
    required ConnectivityService connectivity,
    String Function()? idGenerator,
    DateTime Function()? clock,
  })  : _remote = remote,
        _local = local,
        _connectivity = connectivity,
        _idGenerator = idGenerator ?? _defaultIdGenerator,
        _clock = clock ?? DateTime.now;

  final NotebookRemoteDataSource _remote;
  final NotebookLocalDataSource _local;
  final ConnectivityService _connectivity;
  final String Function() _idGenerator;
  final DateTime Function() _clock;

  @override
  Future<Result<List<NotebookEntry>>> list({DateTime? sinceModified}) async {
    try {
      final entries = await _local.getAll(sinceModified: sinceModified);
      return Success(entries);
    } on AppException catch (error) {
      return Failure(error);
    } catch (error) {
      return Failure(UnknownException(
        'notebook.repository.list failed',
        cause: error,
      ));
    }
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
    try {
      final now = _clock().toUtc();
      final localEntry = NotebookEntry(
        id: _idGenerator(),
        word: word,
        context: context,
        episodeId: episodeId,
        sentenceIndex: sentenceIndex,
        meaning: meaning,
        note: note,
        createdAt: now,
        lastModified: now,
        syncStatus: SyncStatus.pendingUpsert,
      );
      await _local.upsert(localEntry);

      if (!await _connectivity.isOnline()) {
        return Success(localEntry);
      }
      return Success(await _pushCreate(localEntry));
    } on AppException catch (error) {
      return Failure(error);
    } catch (error) {
      return Failure(UnknownException(
        'notebook.repository.add failed',
        cause: error,
      ));
    }
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
    try {
      final existing = await _local.getById(id);
      if (existing == null) {
        return Failure(NotFoundException('notebook entry $id not found'));
      }

      final now = _clock().toUtc();
      final updated = existing.copyWith(
        word: word ?? existing.word,
        context: context ?? existing.context,
        episodeId: episodeId ?? existing.episodeId,
        sentenceIndex: sentenceIndex ?? existing.sentenceIndex,
        meaning: meaning ?? existing.meaning,
        note: note ?? existing.note,
        lastModified: now,
        syncStatus: SyncStatus.pendingUpsert,
      );
      await _local.upsert(updated);

      if (!await _connectivity.isOnline()) {
        return Success(updated);
      }
      return Success(await _pushUpdate(updated));
    } on AppException catch (error) {
      return Failure(error);
    } catch (error) {
      return Failure(UnknownException(
        'notebook.repository.update failed',
        cause: error,
      ));
    }
  }

  @override
  Future<Result<void>> remove(String id) async {
    try {
      if (!await _connectivity.isOnline()) {
        // Offline: keep the row locally with a tombstone so the sync
        // engine can propagate the DELETE on reconnect. Hiding from the
        // UI list is handled by `NotebookLocalDataSource.getAll`.
        final now = _clock().toUtc();
        await _local.markDeleted(id, now);
        return const Success(null);
      }

      // Online: hard-delete locally first (matches previous behaviour for
      // the repository contract), then tell the server. A 404 is benign.
      await _local.remove(id);
      try {
        await _remote.delete(id);
      } on NotFoundException {
        // Server already doesn't know this id — treat as success.
      }
      return const Success(null);
    } on AppException catch (error) {
      return Failure(error);
    } catch (error) {
      return Failure(UnknownException(
        'notebook.repository.remove failed',
        cause: error,
      ));
    }
  }

  Future<NotebookEntry> _pushCreate(NotebookEntry entry) async {
    final dto = await _remote.create(
      word: entry.word,
      context: entry.context,
      episodeId: entry.episodeId,
      sentenceIndex: entry.sentenceIndex,
      meaning: entry.meaning,
      note: entry.note,
    );
    final serverEntry = dto.toEntity();
    // The server allocates its own id — move the local row over to avoid
    // leaving a dangling temp id.
    if (serverEntry.id != entry.id) {
      await _local.remove(entry.id);
    }
    await _local.upsert(serverEntry);
    return serverEntry;
  }

  Future<NotebookEntry> _pushUpdate(NotebookEntry entry) async {
    final dto = await _remote.patch(
      id: entry.id,
      word: entry.word,
      context: entry.context,
      episodeId: entry.episodeId,
      sentenceIndex: entry.sentenceIndex,
      meaning: entry.meaning,
      note: entry.note,
    );
    final serverEntry = dto.toEntity();
    await _local.upsert(serverEntry);
    return serverEntry;
  }
}

// ---------------------------------------------------------------------------
// Default id generator — simple UUIDv4-ish without pulling in a new dep.
// Server assigns canonical ids on create; this only has to be unique within
// the local store until that round-trip returns.
// ---------------------------------------------------------------------------

String _defaultIdGenerator() {
  final random = math.Random.secure();
  final bytes = List<int>.generate(16, (_) => random.nextInt(256));
  // RFC 4122 v4 markers.
  bytes[6] = (bytes[6] & 0x0f) | 0x40;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  String hex2(int b) => b.toRadixString(16).padLeft(2, '0');
  final hex = bytes.map(hex2).join();
  return '${hex.substring(0, 8)}-${hex.substring(8, 12)}-'
      '${hex.substring(12, 16)}-${hex.substring(16, 20)}-${hex.substring(20)}';
}

// ---------------------------------------------------------------------------
// Riverpod wiring
// ---------------------------------------------------------------------------

final notebookRemoteDataSourceProvider =
    Provider<NotebookRemoteDataSource>((ref) {
  return NotebookRemoteDataSource(ref.watch(dioClientProvider));
});

final notebookLocalDataSourceProvider =
    FutureProvider<NotebookLocalDataSource>((ref) async {
  final db = await ref.watch(appDatabaseProvider.future);
  return NotebookLocalDataSource(db);
});

final notebookRepositoryProvider =
    FutureProvider<NotebookRepository>((ref) async {
  final local = await ref.watch(notebookLocalDataSourceProvider.future);
  return NotebookRepositoryImpl(
    remote: ref.watch(notebookRemoteDataSourceProvider),
    local: local,
    connectivity: ref.watch(connectivityServiceProvider),
  );
});

/// Sync service singleton — wraps the same datasource instances the
/// repository uses, so both see one consistent drift view.
final notebookSyncServiceProvider =
    FutureProvider<NotebookSyncService>((ref) async {
  final local = await ref.watch(notebookLocalDataSourceProvider.future);
  return NotebookSyncService(
    local: local,
    remote: ref.watch(notebookRemoteDataSourceProvider),
    connectivity: ref.watch(connectivityServiceProvider),
  );
});
