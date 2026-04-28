import '../../../../core/errors/result.dart';
import '../entities/episode_detail.dart';
import '../repositories/episode_detail_repository.dart';

/// UseCase: load a single episode's detail (metadata + sentence list).
class GetEpisodeDetail {
  const GetEpisodeDetail(this._repository);

  final EpisodeDetailRepository _repository;

  Future<Result<EpisodeDetail>> call(String id) => _repository.getDetail(id);
}
