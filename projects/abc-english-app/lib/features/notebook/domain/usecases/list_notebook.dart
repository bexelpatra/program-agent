import '../../../../core/errors/result.dart';
import '../entities/notebook_entry.dart';
import '../repositories/notebook_repository.dart';

/// UseCase: list notebook entries (local-first).
class ListNotebook {
  const ListNotebook(this._repository);

  final NotebookRepository _repository;

  Future<Result<List<NotebookEntry>>> call({DateTime? sinceModified}) {
    return _repository.list(sinceModified: sinceModified);
  }
}
