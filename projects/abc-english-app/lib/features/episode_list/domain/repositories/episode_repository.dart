import '../../../../core/domain/entities/episode.dart';
import '../../../../core/errors/result.dart';

/// Port between domain (UseCases) and data (remote/local datasources).
///
/// Implementations live in `data/repositories/episode_repository_impl.dart`
/// and translate transport / storage failures into [Result.failure] values
/// carrying an `AppException` — UseCases therefore never see raw HTTP or
/// drift exceptions.
abstract class EpisodeRepository {
  /// Paginated episode list.
  ///
  /// - `page` is 1-indexed and `size` is clamped server-side (1..50).
  /// - `sinceModified`, if provided, asks the server for rows whose
  ///   `lastModified` is greater than or equal to the given timestamp.
  ///   Offline callers get whatever the local mirror holds and should
  ///   treat the result as "best effort".
  Future<Result<List<Episode>>> listEpisodes({
    int page,
    int size,
    DateTime? sinceModified,
  });

  /// Fetch a single episode by id. Local-first; falls back to remote when
  /// online and the local mirror has no row.
  Future<Result<Episode>> getById(String id);
}
