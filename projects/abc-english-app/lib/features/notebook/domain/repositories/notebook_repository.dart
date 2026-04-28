import '../../../../core/errors/result.dart';
import '../entities/notebook_entry.dart';

/// Port for notebook CRUD.
///
/// Writes go to local storage first and then, if online, push to the
/// server. The repository returns the entry as it was persisted locally —
/// callers should inspect `syncStatus` to know whether the write is live
/// on the server yet.
abstract class NotebookRepository {
  /// Lists local entries. Offline-first by design; any server reconciliation
  /// happens via a separate sync engine (not this repository).
  Future<Result<List<NotebookEntry>>> list({DateTime? sinceModified});

  Future<Result<NotebookEntry>> add({
    required String word,
    required String context,
    String? episodeId,
    int? sentenceIndex,
    String? meaning,
    String? note,
  });

  Future<Result<NotebookEntry>> update({
    required String id,
    String? word,
    String? context,
    String? episodeId,
    int? sentenceIndex,
    String? meaning,
    String? note,
  });

  Future<Result<void>> remove(String id);
}
