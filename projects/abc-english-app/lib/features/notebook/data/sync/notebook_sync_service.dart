import '../../../../core/connectivity/connectivity_service.dart';
import '../../../../core/errors/app_exception.dart';
import '../../../../core/logging/app_logger.dart';
import '../../../../core/sync/sync_engine.dart';
import '../../domain/entities/notebook_entry.dart';
import '../../domain/entities/sync_status.dart';
import '../datasources/notebook_local_datasource.dart';
import '../datasources/notebook_remote_datasource.dart';
import '../models/notebook_entry_dto.dart';

/// Drains the offline queue for the notebook feature and reconciles with
/// the server.
///
/// The [SyncEngine] skeleton (see `core/sync/sync_engine.dart`) ships a
/// per-entity push contract. The notebook API, in contrast, exposes a
/// **batch** `/api/v1/notebook/sync` endpoint that applies an array of
/// upsert/delete changes and returns a matching result array. We honour
/// both by:
///
/// 1. Calling the server's batch endpoint once per sync run (fast path for
///    many offline edits).
/// 2. Exposing a `SyncEngine<NotebookEntry>` instance that wraps the same
///    local datasource. The engine's per-entity `pushLocal` delegates to a
///    one-change batch call on the server so callers who want the generic
///    per-entity loop (e.g. eventual reuse for episodes) can still use it.
///
/// The batch `sync()` method is the primary entry point; the engine is
/// exposed via [syncEngine] mostly for tests and future composition.
class NotebookSyncService {
  NotebookSyncService({
    required NotebookLocalDataSource local,
    required NotebookRemoteDataSource remote,
    required ConnectivityService connectivity,
    DateTime Function()? clock,
  })  : _local = local,
        _remote = remote,
        _connectivity = connectivity,
        _clock = clock ?? DateTime.now {
    _engine = SyncEngine<NotebookEntry>(
      connectivity: _connectivity,
      fetchRemote: _fetchRemoteSince,
      getLocalPending: _local.getPending,
      pushLocal: _pushSingle,
      upsertLocal: _local.upsert,
    );
  }

  final NotebookLocalDataSource _local;
  final NotebookRemoteDataSource _remote;
  final ConnectivityService _connectivity;
  final DateTime Function() _clock;
  late final SyncEngine<NotebookEntry> _engine;

  /// Last successful server-side cutoff. We use it as the `since_modified`
  /// filter on the next incremental fetch so we don't pull the whole
  /// notebook every sync. Stored in memory only — a cold restart does a
  /// full resync, which is acceptable for the volumes we expect.
  DateTime? _lastSyncAt;

  SyncEngine<NotebookEntry> get syncEngine => _engine;

  /// Drain pending changes and pull incremental updates. Safe to call
  /// multiple times; no-ops when offline.
  Future<NotebookSyncOutcome> sync() async {
    if (!await _connectivity.isOnline()) {
      AppLogger.instance.debug('notebook.sync.skipped', context: const {
        'reason': 'offline',
      });
      return const NotebookSyncOutcome.skipped();
    }

    try {
      final applied = await _pushPending();
      final pulled = await _pullRemote();
      _lastSyncAt = _clock().toUtc();
      return NotebookSyncOutcome.success(applied: applied, pulled: pulled);
    } on AppException catch (error, stack) {
      AppLogger.instance.warning(
        'notebook.sync.failed',
        context: {'reason': error.runtimeType.toString()},
        error: error,
        stackTrace: stack,
      );
      return NotebookSyncOutcome.failed(error);
    } catch (error, stack) {
      AppLogger.instance.warning(
        'notebook.sync.failed',
        context: const {'reason': 'unknown'},
        error: error,
        stackTrace: stack,
      );
      return NotebookSyncOutcome.failed(
        UnknownException('notebook.sync failed: $error', cause: error),
      );
    }
  }

  // -------------------------------------------------------------------------
  // Push path: batch upload
  // -------------------------------------------------------------------------

  Future<int> _pushPending() async {
    final pending = await _local.getPending();
    if (pending.isEmpty) {
      return 0;
    }

    final changes = pending.map(_toChange).toList(growable: false);
    final results = await _remote.syncBatch(changes);

    // Server is expected to return results in the same order, but we index
    // by id defensively so a single reordered result doesn't misapply.
    final byId = <String, NotebookSyncResult>{};
    for (final r in results) {
      if (r.id != null) byId[r.id!] = r;
    }

    var applied = 0;
    for (final entry in pending) {
      final result = byId[entry.id];
      if (result == null) {
        AppLogger.instance.warning(
          'notebook.sync.result_missing',
          context: {'id': entry.id},
        );
        continue;
      }
      await _applyResult(entry, result);
      if (result.status == NotebookSyncStatus.applied ||
          result.status == NotebookSyncStatus.serverWins ||
          result.status == NotebookSyncStatus.notFound) {
        applied++;
      }
    }
    return applied;
  }

  Future<void> _applyResult(
    NotebookEntry local,
    NotebookSyncResult result,
  ) async {
    switch (result.status) {
      case NotebookSyncStatus.applied:
        if (local.syncStatus == SyncStatus.pendingDelete) {
          await _local.hardDelete(local.id);
          return;
        }
        final modified = result.serverLastModified ?? local.lastModified;
        await _local.upsert(
          local.copyWith(
            lastModified: modified,
            syncStatus: SyncStatus.synced,
          ),
        );
        return;
      case NotebookSyncStatus.serverWins:
        // Server has a newer payload for this id. Pull the authoritative
        // record below (it'll come through _pullRemote). Meanwhile clear
        // local pending state against the server's stamp so we don't loop.
        final modified = result.serverLastModified ?? local.lastModified;
        await _local.upsert(
          local.copyWith(
            lastModified: modified,
            syncStatus: SyncStatus.synced,
          ),
        );
        AppLogger.instance.info(
          'notebook.sync.server_wins',
          context: {'id': local.id},
        );
        return;
      case NotebookSyncStatus.notFound:
        // Delete echo for a row the server already forgot — drop the
        // tombstone locally too.
        if (local.syncStatus == SyncStatus.pendingDelete) {
          await _local.hardDelete(local.id);
        }
        return;
      case NotebookSyncStatus.error:
        // Leave local state alone; surface in logs + retrospective.
        AppLogger.instance.warning(
          'notebook.sync.per_change_error',
          context: {'id': local.id, 'detail': result.detail},
        );
        return;
    }
  }

  NotebookSyncChange _toChange(NotebookEntry entry) {
    if (entry.syncStatus == SyncStatus.pendingDelete) {
      return NotebookSyncChange.delete(
        id: entry.id,
        clientLastModified: entry.lastModified,
      );
    }
    return NotebookSyncChange.upsert(
      id: entry.id,
      payload: _entryToDto(entry),
      clientLastModified: entry.lastModified,
    );
  }

  NotebookEntryDto _entryToDto(NotebookEntry e) {
    return NotebookEntryDto(
      id: e.id,
      word: e.word,
      context: e.context,
      episodeId: e.episodeId,
      sentenceIndex: e.sentenceIndex,
      meaning: e.meaning,
      note: e.note,
      createdAt: e.createdAt.toUtc().toIso8601String(),
      lastModified: e.lastModified.toUtc().toIso8601String(),
    );
  }

  // -------------------------------------------------------------------------
  // Pull path: incremental remote fetch
  // -------------------------------------------------------------------------

  Future<int> _pullRemote() async {
    final since = _lastSyncAt;
    final dtos = await _remote.list(sinceModified: since);
    var pulled = 0;
    for (final dto in dtos) {
      final entity = dto.toEntity();
      // Server-authoritative row → overwrite local (LWW is already
      // encoded server-side via `last_modified` compare).
      await _local.upsert(entity);
      pulled++;
    }
    return pulled;
  }

  // -------------------------------------------------------------------------
  // SyncEngine callback (single-change batch; kept for future per-entity
  // use cases)
  // -------------------------------------------------------------------------

  Future<List<NotebookEntry>> _fetchRemoteSince() async {
    final since = _lastSyncAt;
    final dtos = await _remote.list(sinceModified: since);
    return dtos.map((d) => d.toEntity()).toList(growable: false);
  }

  Future<NotebookEntry> _pushSingle(NotebookEntry entry) async {
    final results = await _remote.syncBatch(<NotebookSyncChange>[
      _toChange(entry),
    ]);
    if (results.isEmpty) {
      throw const NetworkException('notebook.sync: empty result');
    }
    final result = results.first;
    switch (result.status) {
      case NotebookSyncStatus.applied:
      case NotebookSyncStatus.serverWins:
        final modified = result.serverLastModified ?? entry.lastModified;
        return entry.copyWith(
          lastModified: modified,
          syncStatus: SyncStatus.synced,
        );
      case NotebookSyncStatus.notFound:
        // Treat the same as applied — nothing to echo.
        return entry.copyWith(syncStatus: SyncStatus.synced);
      case NotebookSyncStatus.error:
        throw SyncConflictException(
          'notebook.sync: per-change error ${result.detail ?? ''}',
        );
    }
  }
}

/// Outcome wrapper returned by [NotebookSyncService.sync]. Separate from
/// the generic [SyncResult] so consumers can distinguish push vs pull
/// counts.
sealed class NotebookSyncOutcome {
  const NotebookSyncOutcome();

  const factory NotebookSyncOutcome.skipped() = NotebookSyncSkipped;
  const factory NotebookSyncOutcome.success({
    required int applied,
    required int pulled,
  }) = NotebookSyncSuccess;
  const factory NotebookSyncOutcome.failed(AppException error) =
      NotebookSyncFailed;
}

class NotebookSyncSkipped extends NotebookSyncOutcome {
  const NotebookSyncSkipped();
}

class NotebookSyncSuccess extends NotebookSyncOutcome {
  const NotebookSyncSuccess({required this.applied, required this.pulled});
  final int applied;
  final int pulled;
}

class NotebookSyncFailed extends NotebookSyncOutcome {
  const NotebookSyncFailed(this.error);
  final AppException error;
}

// ---------------------------------------------------------------------------
// Riverpod wiring
// ---------------------------------------------------------------------------
//
// The provider for [NotebookSyncService] itself lives in
// `notebook_repository_impl.dart` so the file that already wires the
// datasource providers (local + remote) is the single source of truth for
// the provider graph; adding a second wiring point here would duplicate
// the DataSource instances and break LWW ordering between the repo and
// the sync service.
