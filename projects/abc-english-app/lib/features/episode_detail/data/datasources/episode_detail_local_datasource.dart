import 'package:drift/drift.dart';

import '../../../../core/domain/entities/episode.dart';
import '../../../../core/errors/app_exception.dart';
import '../../../../core/storage/app_database.dart';
import '../../domain/entities/episode_detail.dart';

/// Drift-side of the episode detail feature.
///
/// Reads from the shared `episodes` + `sentences` tables. This datasource
/// does **not** write the episode row — that is owned by the episode_list
/// datasource. The detail feature only writes its own sentence rows.
class EpisodeDetailLocalDataSource {
  EpisodeDetailLocalDataSource(this._db);

  final AppDatabase _db;

  /// Returns `null` if the episode row is missing locally. Sentence rows
  /// missing for a known episode produce an empty list (still considered a
  /// successful lookup — sentences may simply not yet be downloaded).
  Future<EpisodeDetail?> getDetail(String id) async {
    try {
      final episodeRow = await (_db.select(_db.episodes)
            ..where((e) => e.id.equals(id)))
          .getSingleOrNull();
      if (episodeRow == null) return null;

      final sentenceRows = await (_db.select(_db.sentences)
            ..where((s) => s.episodeId.equals(id))
            ..orderBy([(s) => OrderingTerm.asc(s.sentenceIndex)]))
          .get();

      return EpisodeDetail(
        episode: _toEpisode(episodeRow),
        sentences: sentenceRows.map(_toSentence).toList(growable: false),
      );
    } catch (error) {
      throw StorageException('episode_detail.local.getDetail failed',
          cause: error);
    }
  }

  /// Upsert the base episode row. Kept here (instead of reaching into the
  /// sibling `episode_list` datasource) so the detail feature can persist
  /// its own remote fetch without cross-feature imports. The schema lives
  /// in `core/storage` — both features legitimately share it.
  Future<void> upsertEpisode(Episode episode) async {
    try {
      await _db.into(_db.episodes).insert(
            _toEpisodeCompanion(episode),
            mode: InsertMode.insertOrReplace,
          );
    } catch (error) {
      throw StorageException('episode_detail.local.upsertEpisode failed',
          cause: error);
    }
  }

  Future<void> upsertSentences(String episodeId, List<Sentence> sentences) async {
    if (sentences.isEmpty) {
      // Deliberately no-op — clearing sentences on an empty payload would
      // delete a valid locally-downloaded transcript.
      return;
    }
    try {
      await _db.batch((batch) {
        batch.insertAll(
          _db.sentences,
          sentences
              .map((s) => _toSentenceCompanion(episodeId, s))
              .toList(growable: false),
          mode: InsertMode.insertOrReplace,
        );
      });
    } catch (error) {
      throw StorageException('episode_detail.local.upsertSentences failed',
          cause: error);
    }
  }

  static Episode _toEpisode(EpisodeRow row) {
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

  static Sentence _toSentence(SentenceRow row) {
    return Sentence(
      index: row.sentenceIndex,
      text: row.body,
      startMs: row.startMs,
      endMs: row.endMs,
      wer: row.wer,
      difficulty: row.difficulty,
    );
  }

  static EpisodesCompanion _toEpisodeCompanion(Episode e) {
    return EpisodesCompanion.insert(
      id: e.id,
      title: e.title,
      publishedDate: e.publishedDate,
      durationMs: e.durationMs,
      lastModified: e.lastModified,
      avgWer: Value(e.avgWer),
      downloadedAt: const Value.absent(),
      audioLocalPath: Value(e.audioLocalPath),
    );
  }

  static SentencesCompanion _toSentenceCompanion(
    String episodeId,
    Sentence sentence,
  ) {
    return SentencesCompanion.insert(
      episodeId: episodeId,
      sentenceIndex: sentence.index,
      body: sentence.text,
      startMs: sentence.startMs,
      endMs: sentence.endMs,
      wer: Value(sentence.wer),
      difficulty: Value(sentence.difficulty),
    );
  }
}
