import 'package:drift/drift.dart';

import '../../../../core/domain/entities/episode.dart';
import '../../../../core/errors/app_exception.dart';
import '../../../../core/storage/app_database.dart';

/// Drift-side of the episode list feature. Exposes plain [Episode] entities
/// (no DTOs — locally the canonical shape is already the domain model, with
/// the download fields populated from the row).
class EpisodeLocalDataSource {
  EpisodeLocalDataSource(this._db);

  final AppDatabase _db;

  Future<List<Episode>> getAll() async {
    try {
      final rows = await _db.select(_db.episodes).get();
      return rows.map(_toEntity).toList(growable: false);
    } catch (error) {
      throw StorageException('episode.local.getAll failed', cause: error);
    }
  }

  Future<Episode?> getById(String id) async {
    try {
      final query = _db.select(_db.episodes)
        ..where((e) => e.id.equals(id));
      final row = await query.getSingleOrNull();
      return row == null ? null : _toEntity(row);
    } catch (error) {
      throw StorageException('episode.local.getById failed', cause: error);
    }
  }

  Future<void> upsert(Episode episode) async {
    try {
      await _db
          .into(_db.episodes)
          .insert(_toCompanion(episode), mode: InsertMode.insertOrReplace);
    } catch (error) {
      throw StorageException('episode.local.upsert failed', cause: error);
    }
  }

  Future<void> upsertMany(List<Episode> episodes) async {
    if (episodes.isEmpty) return;
    try {
      await _db.batch((batch) {
        batch.insertAll(
          _db.episodes,
          episodes.map(_toCompanion).toList(growable: false),
          mode: InsertMode.insertOrReplace,
        );
      });
    } catch (error) {
      throw StorageException('episode.local.upsertMany failed', cause: error);
    }
  }

  static Episode _toEntity(EpisodeRow row) {
    return Episode(
      id: row.id,
      title: row.title,
      publishedDate: row.publishedDate,
      durationMs: row.durationMs,
      avgWer: row.avgWer,
      lastModified: row.lastModified,
      isDownloaded:
          row.downloadedAt != null && (row.audioLocalPath?.isNotEmpty ?? false),
      audioLocalPath: row.audioLocalPath,
    );
  }

  static EpisodesCompanion _toCompanion(Episode e) {
    return EpisodesCompanion.insert(
      id: e.id,
      title: e.title,
      publishedDate: e.publishedDate,
      durationMs: e.durationMs,
      lastModified: e.lastModified,
      avgWer: Value(e.avgWer),
      // `isDownloaded` is the repository's view; downloadedAt is stamped by
      // the download feature (not in scope here) so we keep whatever is
      // already in the row by leaving the column absent.
      downloadedAt: const Value.absent(),
      audioLocalPath: Value(e.audioLocalPath),
    );
  }
}
