import 'package:freezed_annotation/freezed_annotation.dart';

part 'sentence.freezed.dart';

/// One aligned sentence within an episode's transcript.
///
/// Millisecond timestamps match the wire format
/// (`start_ms` / `end_ms` produced by `/api/v1/episodes/{id}` — see
/// `projects/abc-english/web/api/v1/episodes.py::_project_sentence`).
///
/// Promoted to `core/domain` so both `episode_detail` and `player` features
/// can consume the same type without cross-feature imports (see
/// architecture.md §앱 아키텍처 — features 간 직접 의존 금지).
///
/// Pure Dart — no HTTP, no DB, no widget types. DTOs in the data layer map
/// on/off this shape via `toEntity()`.
@freezed
class Sentence with _$Sentence {
  const factory Sentence({
    required int index,
    required String text,
    required int startMs,
    required int endMs,
    double? wer,
    String? difficulty,
  }) = _Sentence;
}
