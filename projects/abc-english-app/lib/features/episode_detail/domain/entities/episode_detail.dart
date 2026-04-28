import 'package:freezed_annotation/freezed_annotation.dart';

import '../../../../core/domain/entities/episode.dart';
import '../../../../core/domain/entities/sentence.dart';

// Re-exported so existing call sites (feature presentation, tests, and
// feature-local DTOs) continue to import `Sentence` via `episode_detail.dart`
// while the canonical definition lives in `core/domain/entities/sentence.dart`.
export '../../../../core/domain/entities/sentence.dart' show Sentence;

part 'episode_detail.freezed.dart';

/// Detail view of an episode: base metadata plus its sentence list.
///
/// `Episode` and `Sentence` are reused from `core/domain/entities/` to keep
/// sibling features (`episode_list` / `episode_detail` / `player`) from
/// reaching into each other — see architecture.md §앱 아키텍처
/// (features 간 직접 의존 금지).
@freezed
class EpisodeDetail with _$EpisodeDetail {
  const factory EpisodeDetail({
    required Episode episode,
    required List<Sentence> sentences,
  }) = _EpisodeDetail;
}
