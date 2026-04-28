import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/errors/app_exception.dart';
import '../../../../core/errors/result.dart';
import '../../../../core/network/dio_client.dart';
import '../../domain/entities/lookup_result.dart';
import '../../domain/repositories/lookup_repository.dart';
import '../datasources/lookup_remote_datasource.dart';

/// Online-only lookup: dictionary/LLM results are not useful offline (the
/// actual model runs on the backend). If the request fails, the caller
/// sees a `Failure(NetworkException)` and the UI surfaces a retry affordance.
///
/// We don't locally cache lookup results here yet — the backend keeps its
/// own LLM cache (`src/llm_cache.py`), and adding a second layer would
/// require cache-invalidation glue that's out of scope for this task. A
/// note left in the architecture → next-iteration work.
class LookupRepositoryImpl implements LookupRepository {
  const LookupRepositoryImpl({required LookupRemoteDataSource remote})
      : _remote = remote;

  final LookupRemoteDataSource _remote;

  @override
  Future<Result<LookupResult>> lookup({
    required String word,
    String? context,
  }) async {
    try {
      final dto = await _remote.lookup(word: word, context: context);
      return Success(dto.toEntity());
    } on AppException catch (error) {
      return Failure(error);
    } catch (error) {
      return Failure(UnknownException(
        'lookup.repository failed',
        cause: error,
      ));
    }
  }
}

// ---------------------------------------------------------------------------
// Riverpod wiring
// ---------------------------------------------------------------------------

final lookupRemoteDataSourceProvider =
    Provider<LookupRemoteDataSource>((ref) {
  final dio = ref.watch(dioClientProvider);
  return LookupRemoteDataSource(dio.raw);
});

final lookupRepositoryProvider = Provider<LookupRepository>((ref) {
  return LookupRepositoryImpl(
    remote: ref.watch(lookupRemoteDataSourceProvider),
  );
});
