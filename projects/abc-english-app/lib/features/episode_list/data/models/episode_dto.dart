// `JsonKey` on a freezed constructor parameter is the documented pattern
// but analyzer 3.x flags it. See https://github.com/rrousselGit/freezed#custom-json-keys
// ignore_for_file: invalid_annotation_target

import 'package:freezed_annotation/freezed_annotation.dart';

import '../../../../core/domain/entities/episode.dart';

part 'episode_dto.freezed.dart';
part 'episode_dto.g.dart';

/// Wire-format mirror of a single row returned by `/api/v1/episodes`.
///
/// The server emits durations in seconds (`duration` / `duration_seconds`) —
/// the DTO accepts both for resilience and stores a single seconds value,
/// which `toEntity()` converts to the entity's milliseconds.
///
/// DTOs are intentionally separate from [Episode]: the wire shape can drift
/// (new optional fields, renames) without churning domain code.
@freezed
class EpisodeDto with _$EpisodeDto {
  const EpisodeDto._();

  const factory EpisodeDto({
    required String id,
    required String title,
    @JsonKey(name: 'published_date') required String publishedDate,
    @JsonKey(name: 'duration') int? durationSeconds,
    @JsonKey(name: 'avg_wer') double? avgWer,
    @JsonKey(name: 'last_modified') String? lastModified,
  }) = _EpisodeDto;

  factory EpisodeDto.fromJson(Map<String, dynamic> json) =>
      _$EpisodeDtoFromJson(json);

  /// Map to the domain entity.
  ///
  /// - `isDownloaded` / `audioLocalPath` are set from local state, not the
  ///   wire — the repository merges remote + local before returning.
  /// - `lastModified` falls back to `publishedDate` (both are ISO strings
  ///   the server normalises).
  Episode toEntity({
    bool isDownloaded = false,
    String? audioLocalPath,
  }) {
    final published = DateTime.parse(publishedDate);
    final modified = lastModified != null
        ? DateTime.parse(lastModified!)
        : published;
    return Episode(
      id: id,
      title: title,
      publishedDate: published,
      durationMs: (durationSeconds ?? 0) * 1000,
      avgWer: avgWer,
      lastModified: modified,
      isDownloaded: isDownloaded,
      audioLocalPath: audioLocalPath,
    );
  }
}
