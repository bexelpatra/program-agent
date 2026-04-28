import '../../../../core/errors/result.dart';
import '../../../episode_detail/domain/entities/episode_detail.dart';
import '../entities/playback_state.dart';

/// Port the player feature uses to drive audio playback.
///
/// Implementations live in `data/repositories/player_repository_impl.dart`.
/// The abstraction exists so UseCases / presentation never import
/// `just_audio` directly.
///
/// Lifecycle:
///  1. [loadEpisode] — binds a specific episode. Resolves source (local vs
///     streaming), preloads metadata, resets position to 0. May only be
///     called once at a time; calling again replaces the prior binding.
///  2. [play] / [pause] / [seek] — act on the currently bound episode.
///     No-op if nothing is loaded.
///  3. [dispose] — release platform resources. Safe to call multiple times.
///
/// All mutating methods return `Result<void>` so presentation can handle
/// failures (missing local file, 401 on streaming URL, etc.) uniformly.
/// [stateStream] is a broadcast stream — presentation will subscribe via
/// `StreamProvider`.
abstract class PlayerRepository {
  Future<Result<void>> loadEpisode(EpisodeDetail detail);

  Future<Result<void>> play();

  Future<Result<void>> pause();

  Future<Result<void>> seek(Duration position);

  Stream<PlaybackState> get stateStream;

  Future<Result<void>> dispose();
}
