import '../../../../core/errors/result.dart';
import '../repositories/player_repository.dart';

/// UseCase: move the playback head to an absolute [Duration] position.
///
/// Negative positions and positions past `totalDurationMs` are clamped by
/// `just_audio` at the data layer; this usecase stays transport-agnostic.
class SeekTo {
  const SeekTo(this._repository);

  final PlayerRepository _repository;

  Future<Result<void>> call(Duration position) =>
      _repository.seek(position);
}
