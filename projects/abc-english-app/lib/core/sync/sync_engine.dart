import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../connectivity/connectivity_service.dart';
import '../errors/app_exception.dart';

/// Contract for any entity synchronised through [SyncEngine]. Entities must
/// expose a stable id and a last-write-wins timestamp.
abstract class SyncableEntity {
  String get id;
  DateTime get lastModified;
}

/// Fetch the remote snapshot (full or since-timestamp — the callback
/// decides). Returned entities represent the server's view.
typedef FetchRemote<T extends SyncableEntity> = Future<List<T>> Function();

/// Return local rows that have unsynced writes queued (e.g. offline edits).
typedef GetLocalPending<T extends SyncableEntity> = Future<List<T>> Function();

/// Push a single local entity to the server. Implementations should update
/// the server and return the server's authoritative copy (with possibly
/// different `lastModified`).
typedef PushLocal<T extends SyncableEntity> = Future<T> Function(T entity);

/// Write an entity (possibly from the remote snapshot, possibly the echoed
/// version from a push) into local storage.
typedef UpsertLocal<T extends SyncableEntity> = Future<void> Function(T entity);

/// Generic Last-Write-Wins synchroniser.
///
/// This is a **skeleton** — it orchestrates the flow and conflict policy,
/// but does not know about HTTP, drift, or any specific feature. Feature
/// layers (e.g. notebook) construct it with four callbacks and a
/// [ConnectivityService].
///
/// Flow for [sync]:
///   1. If offline → return [SyncSkipped].
///   2. Fetch remote snapshot and local pending writes.
///   3. For each local pending row, push to server. Upsert server's echoed
///      row locally.
///   4. For each remote row, resolve against local by `lastModified`
///      (larger wins). Upsert winner locally.
///   5. Return [SyncSuccess] with applied/conflict counts, or [SyncFailed]
///      wrapping an [AppException] raised by any callback.
class SyncEngine<T extends SyncableEntity> {
  SyncEngine({
    required ConnectivityService connectivity,
    required FetchRemote<T> fetchRemote,
    required GetLocalPending<T> getLocalPending,
    required PushLocal<T> pushLocal,
    required UpsertLocal<T> upsertLocal,
  })  : _connectivity = connectivity,
        _fetchRemote = fetchRemote,
        _getLocalPending = getLocalPending,
        _pushLocal = pushLocal,
        _upsertLocal = upsertLocal;

  final ConnectivityService _connectivity;
  final FetchRemote<T> _fetchRemote;
  final GetLocalPending<T> _getLocalPending;
  final PushLocal<T> _pushLocal;
  final UpsertLocal<T> _upsertLocal;

  Future<SyncResult> sync() async {
    if (!await _connectivity.isOnline()) {
      return const SyncSkipped();
    }

    try {
      final pending = await _getLocalPending();
      var applied = 0;
      for (final local in pending) {
        final echoed = await _pushLocal(local);
        await _upsertLocal(echoed);
        applied++;
      }

      final remote = await _fetchRemote();
      final pendingById = <String, T>{for (final e in pending) e.id: e};
      var conflicts = 0;
      for (final remoteEntity in remote) {
        final localPending = pendingById[remoteEntity.id];
        if (localPending == null) {
          await _upsertLocal(remoteEntity);
          applied++;
          continue;
        }
        // Conflict: both sides have modified this row. LWW.
        conflicts++;
        final winner =
            remoteEntity.lastModified.isAfter(localPending.lastModified)
                ? remoteEntity
                : localPending;
        await _upsertLocal(winner);
      }

      return SyncSuccess(applied: applied, conflicts: conflicts);
    } on AppException catch (e) {
      return SyncFailed(e);
    } catch (e) {
      return SyncFailed(
        UnknownException('Sync failed: $e', cause: e),
      );
    }
  }
}

/// Outcome of a single [SyncEngine.sync] invocation.
sealed class SyncResult {
  const SyncResult();
}

class SyncSuccess extends SyncResult {
  const SyncSuccess({required this.applied, required this.conflicts});
  final int applied;
  final int conflicts;
}

class SyncSkipped extends SyncResult {
  const SyncSkipped();
}

class SyncFailed extends SyncResult {
  const SyncFailed(this.error);
  final AppException error;
}

/// Provider family template intentionally omitted — feature layers build
/// their own typed `SyncEngine<NotebookEntry>` provider with repository
/// callbacks. See architecture.md §동기화 방식.
///
/// The plain provider below is a convenience for tests that want to verify
/// the engine in isolation.
final syncEngineConnectivityProvider = Provider<ConnectivityService>((ref) {
  return ref.watch(connectivityServiceProvider);
});
