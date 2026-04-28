import 'package:freezed_annotation/freezed_annotation.dart';

part 'episode.freezed.dart';

/// Promoted to `core/domain` so both `episode_list` and `episode_detail`
/// features can consume the same type without cross-feature imports (see
/// architecture.md §앱 아키텍처 — features 간 직접 의존 금지).
///
/// Pure Dart — no HTTP, no DB, no widget types. DTOs in the data layer map
/// on/off this shape via `toEntity()` / `fromEntity()`.
@freezed
class Episode with _$Episode {
  const factory Episode({
    required String id,
    required String title,
    required DateTime publishedDate,
    required int durationMs,
    required DateTime lastModified,
    required bool isDownloaded,
    double? avgWer,
    String? audioLocalPath,
  }) = _Episode;
}
