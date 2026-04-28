import '../../../../core/errors/result.dart';
import '../entities/notebook_entry.dart';
import '../repositories/notebook_repository.dart';

/// UseCase: add a new notebook entry.
class AddNotebookEntry {
  const AddNotebookEntry(this._repository);

  final NotebookRepository _repository;

  Future<Result<NotebookEntry>> call({
    required String word,
    required String context,
    String? episodeId,
    int? sentenceIndex,
    String? meaning,
    String? note,
  }) {
    return _repository.add(
      word: word,
      context: context,
      episodeId: episodeId,
      sentenceIndex: sentenceIndex,
      meaning: meaning,
      note: note,
    );
  }
}
