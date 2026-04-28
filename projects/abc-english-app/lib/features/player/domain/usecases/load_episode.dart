import '../../../../core/errors/result.dart';
import '../../../episode_detail/domain/entities/episode_detail.dart';
import '../repositories/player_repository.dart';

/// UseCase: bind the player to a specific episode.
///
/// Resolves local vs streaming source internally (see
/// `PlayerAudioDataSource`). After success, the player is paused at position
/// 0 and ready for a [PlayPause] / [SeekTo] call.
class LoadEpisode {
  const LoadEpisode(this._repository);

  final PlayerRepository _repository;

  Future<Result<void>> call(EpisodeDetail detail) =>
      _repository.loadEpisode(detail);
}
