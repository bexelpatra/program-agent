import '../../../../core/domain/entities/sentence.dart';
import '../../../../core/errors/app_exception.dart';
import '../../../../core/errors/result.dart';
import '../repositories/player_repository.dart';

/// UseCase: seek to the start of a specific sentence by its index in the
/// episode's sentence list.
///
/// Triggered when the user taps a `SentenceTile` in the script view. The
/// index→timestamp lookup stays in domain (pure list indexing), the actual
/// seek is delegated to [PlayerRepository].
class JumpToSentence {
  const JumpToSentence(this._repository);

  final PlayerRepository _repository;

  Future<Result<void>> call(
    int sentenceIndex,
    List<Sentence> sentences,
  ) {
    if (sentenceIndex < 0 || sentenceIndex >= sentences.length) {
      return Future.value(
        Failure(NotFoundException(
          'sentenceIndex $sentenceIndex out of range (0..${sentences.length - 1})',
        )),
      );
    }
    final target = Duration(milliseconds: sentences[sentenceIndex].startMs);
    return _repository.seek(target);
  }
}
