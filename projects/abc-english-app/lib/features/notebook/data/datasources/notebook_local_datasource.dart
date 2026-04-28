import 'package:drift/drift.dart';

import '../../../../core/errors/app_exception.dart';
import '../../../../core/storage/app_database.dart';
import '../../domain/entities/notebook_entry.dart';
import '../../domain/entities/sync_status.dart';

/// Drift-side of the notebook feature.
///
/// Sync state is derived from two columns:
///   - `syncedAt IS NULL` + `deletedAt IS NULL` → [SyncStatus.pendingUpsert]
///   - `deletedAt IS NOT NULL`                   → [SyncStatus.pendingDelete]
///   - otherwise                                 → [SyncStatus.synced]
///
/// Offline deletes flip [deletedAt] rather than removing the row so the
/// sync engine can propagate the DELETE to the server; the row is
/// hard-deleted only once the server acknowledges it (via [hardDelete]).
class NotebookLocalDataSource {
  NotebookLocalDataSource(this._db);

  final AppDatabase _db;

  /// List visible entries (tombstones excluded). Used by the UI list.
  Future<List<NotebookEntry>> getAll({DateTime? sinceModified}) async {
    try {
      final query = _db.select(_db.notebookEntries)
        ..where((e) => e.deletedAt.isNull())
        ..orderBy([(e) => OrderingTerm.desc(e.lastModified)]);
      if (sinceModified != null) {
        query.where((e) => e.lastModified.isBiggerOrEqualValue(sinceModified));
      }
      final rows = await query.get();
      return rows.map(_toEntity).toList(growable: false);
    } catch (error) {
      throw StorageException('notebook.local.getAll failed', cause: error);
    }
  }

  Future<NotebookEntry?> getById(String id) async {
    try {
      final row = await (_db.select(_db.notebookEntries)
            ..where((e) => e.id.equals(id)))
          .getSingleOrNull();
      return row == null ? null : _toEntity(row);
    } catch (error) {
      throw StorageException('notebook.local.getById failed', cause: error);
    }
  }

  /// All rows waiting to be pushed to the server: pending upserts AND
  /// pending deletes (tombstones). Order doesn't matter — the sync engine
  /// resolves by id.
  Future<List<NotebookEntry>> getPending() async {
    try {
      final query = _db.select(_db.notebookEntries)
        ..where((e) => e.syncedAt.isNull() | e.deletedAt.isNotNull());
      final rows = await query.get();
      return rows.map(_toEntity).toList(growable: false);
    } catch (error) {
      throw StorageException('notebook.local.getPending failed', cause: error);
    }
  }

  /// Insert or replace an entry. [syncedAt] policy:
  ///   - [SyncStatus.synced]        → stamp with `lastModified` (synced now)
  ///   - [SyncStatus.pendingUpsert] → leave `synced_at = null`
  ///   - [SyncStatus.pendingDelete] → caller should use [markDeleted] / the
  ///     tombstone helpers instead; we still accept it here for code paths
  ///     that want to flip state atomically.
  Future<void> upsert(NotebookEntry entry) async {
    try {
      await _db.into(_db.notebookEntries).insert(
            _toCompanion(entry),
            mode: InsertMode.insertOrReplace,
          );
    } catch (error) {
      throw StorageException('notebook.local.upsert failed', cause: error);
    }
  }

  /// Soft-delete: stamp [deletedAt] so the row is excluded from UI lists
  /// but still visible to the sync engine as a pending DELETE.
  Future<void> markDeleted(String id, DateTime when) async {
    try {
      await (_db.update(_db.notebookEntries)..where((e) => e.id.equals(id)))
          .write(
        NotebookEntriesCompanion(
          deletedAt: Value(when),
          lastModified: Value(when),
          syncedAt: const Value(null),
        ),
      );
    } catch (error) {
      throw StorageException('notebook.local.markDeleted failed', cause: error);
    }
  }

  /// Hard delete — used when the server has acknowledged a DELETE or when
  /// an online delete never needed a tombstone.
  Future<int> hardDelete(String id) async {
    try {
      return await (_db.delete(_db.notebookEntries)
            ..where((e) => e.id.equals(id)))
          .go();
    } catch (error) {
      throw StorageException('notebook.local.hardDelete failed', cause: error);
    }
  }

  /// Back-compat alias — existing callers expect [remove]. Same semantics
  /// as [hardDelete].
  Future<int> remove(String id) => hardDelete(id);

  static NotebookEntry _toEntity(NotebookEntryRow row) {
    return NotebookEntry(
      id: row.id,
      word: row.word,
      context: row.context,
      episodeId: row.episodeId,
      sentenceIndex: row.sentenceIndex,
      meaning: row.meaning,
      note: row.note,
      createdAt: row.createdAt,
      lastModified: row.lastModified,
      syncStatus: _statusFromRow(row),
    );
  }

  static SyncStatus _statusFromRow(NotebookEntryRow row) {
    if (row.deletedAt != null) {
      return SyncStatus.pendingDelete;
    }
    return row.syncedAt == null
        ? SyncStatus.pendingUpsert
        : SyncStatus.synced;
  }

  static NotebookEntriesCompanion _toCompanion(NotebookEntry e) {
    return NotebookEntriesCompanion.insert(
      id: e.id,
      word: e.word,
      context: e.context,
      createdAt: e.createdAt,
      lastModified: e.lastModified,
      episodeId: Value(e.episodeId),
      sentenceIndex: Value(e.sentenceIndex),
      meaning: Value(e.meaning),
      note: Value(e.note),
      syncedAt: Value(
        e.syncStatus == SyncStatus.synced ? e.lastModified : null,
      ),
      deletedAt: Value(
        e.syncStatus == SyncStatus.pendingDelete ? e.lastModified : null,
      ),
    );
  }
}
