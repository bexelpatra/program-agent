import '../../../../core/errors/result.dart';
import '../entities/episode_detail.dart';

/// Port for fetching an episode's detail (metadata + sentences) regardless
/// of online/offline state. Implementations live in
/// `data/repositories/episode_detail_repository_impl.dart`.
abstract class EpisodeDetailRepository {
  Future<Result<EpisodeDetail>> getDetail(String id);
}
