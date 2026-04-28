import '../../../../core/errors/result.dart';
import '../entities/lookup_result.dart';

/// Port for the dictionary lookup feature.
///
/// Implementations call `/api/v1/lookup?word=&context=` on the abc-english
/// backend. The `context` parameter lets the LLM disambiguate homographs by
/// showing it the sentence the word was tapped in.
abstract class LookupRepository {
  Future<Result<LookupResult>> lookup({
    required String word,
    String? context,
  });
}
