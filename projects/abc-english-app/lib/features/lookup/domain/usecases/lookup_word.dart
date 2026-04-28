import '../../../../core/errors/result.dart';
import '../entities/lookup_result.dart';
import '../repositories/lookup_repository.dart';

/// UseCase: look up the meaning of a word (optionally with its surrounding
/// sentence so the LLM can disambiguate senses).
class LookupWord {
  const LookupWord(this._repository);

  final LookupRepository _repository;

  Future<Result<LookupResult>> call({
    required String word,
    String? context,
  }) =>
      _repository.lookup(word: word, context: context);
}
