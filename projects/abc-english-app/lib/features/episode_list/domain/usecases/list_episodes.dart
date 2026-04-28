import '../../../../core/domain/entities/episode.dart';
import '../../../../core/errors/result.dart';
import '../repositories/episode_repository.dart';

/// UseCase: paginated episode list.
///
/// Thin delegator — page/size defaults live at the repository so every
/// call-site (screen, provider, tests) picks them up consistently.
class ListEpisodes {
  const ListEpisodes(this._repository);

  final EpisodeRepository _repository;

  Future<Result<List<Episode>>> call({
    int page = 1,
    int size = 20,
    DateTime? sinceModified,
  }) {
    return _repository.listEpisodes(
      page: page,
      size: size,
      sinceModified: sinceModified,
    );
  }
}
