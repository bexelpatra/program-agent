import '../../../../core/domain/entities/episode.dart';
import '../../../../core/errors/result.dart';
import '../repositories/episode_repository.dart';

/// UseCase: fetch a single episode by id.
class GetEpisode {
  const GetEpisode(this._repository);

  final EpisodeRepository _repository;

  Future<Result<Episode>> call(String id) => _repository.getById(id);
}
