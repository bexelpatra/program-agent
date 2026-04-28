import '../../../../core/errors/result.dart';
import '../repositories/notebook_repository.dart';

/// UseCase: delete a notebook entry.
class DeleteNotebookEntry {
  const DeleteNotebookEntry(this._repository);

  final NotebookRepository _repository;

  Future<Result<void>> call(String id) => _repository.remove(id);
}
