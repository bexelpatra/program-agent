import '../../../../core/errors/result.dart';
import '../entities/playback_state.dart';
import '../repositories/player_repository.dart';

/// UseCase: toggle play/pause based on the current [PlaybackState.isPlaying].
///
/// Accepting the snapshot explicitly (instead of reading from the stream
/// inside the usecase) keeps the function pure-ish: same input → same
/// repository call, easy to test without a StreamController fixture.
/// Callers (Riverpod provider / Widget) pass the latest emitted state.
class PlayPause {
  const PlayPause(this._repository);

  final PlayerRepository _repository;

  Future<Result<void>> call(PlaybackState current) {
    if (current.isPlaying) {
      return _repository.pause();
    }
    return _repository.play();
  }
}
