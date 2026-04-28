import '../../../../core/errors/result.dart';
import '../entities/notebook_entry.dart';
import '../repositories/notebook_repository.dart';

/// UseCase: update an existing notebook entry.
class UpdateNotebookEntry {
  const UpdateNotebookEntry(this._repository);

  final NotebookRepository _repository;

  Future<Result<NotebookEntry>> call({
    required String id,
    String? word,
    String? context,
    String? episodeId,
    int? sentenceIndex,
    String? meaning,
    String? note,
  }) {
    return _repository.update(
      id: id,
      word: word,
      context: context,
      episodeId: episodeId,
      sentenceIndex: sentenceIndex,
      meaning: meaning,
      note: note,
    );
  }
}
