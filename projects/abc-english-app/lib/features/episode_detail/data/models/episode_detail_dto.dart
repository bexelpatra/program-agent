// ignore_for_file: invalid_annotation_target

import 'package:freezed_annotation/freezed_annotation.dart';

import '../../../../core/domain/entities/episode.dart';
import '../../domain/entities/episode_detail.dart';
import 'sentence_dto.dart';

part 'episode_detail_dto.freezed.dart';
part 'episode_detail_dto.g.dart';

/// Wire-format mirror of the `/api/v1/episodes/{id}` response.
///
/// Base episode fields are duplicated from [episode_list]'s `EpisodeDto`
/// rather than imported cross-feature — the domain-level [Episode] entity
/// is shared via `core/domain`, but data-layer DTOs stay feature-local to
/// keep the wire contract evolvable per feature (see architecture.md
/// §앱 아키텍처 — features 간 직접 의존 금지).
@freezed
class EpisodeDetailDto with _$EpisodeDetailDto {
  const EpisodeDetailDto._();

  const factory EpisodeDetailDto({
    required String id,
    required String title,
    @JsonKey(name: 'published_date') required String publishedDate,
    @JsonKey(name: 'duration') int? durationSeconds,
    @JsonKey(name: 'avg_wer') double? avgWer,
    @JsonKey(name: 'last_modified') String? lastModified,
    @Default(<SentenceDto>[]) List<SentenceDto> sentences,
  }) = _EpisodeDetailDto;

  factory EpisodeDetailDto.fromJson(Map<String, dynamic> json) =>
      _$EpisodeDetailDtoFromJson(json);

  EpisodeDetail toEntity({
    bool isDownloaded = false,
    String? audioLocalPath,
  }) {
    return EpisodeDetail(
      episode: _baseEntity(
        isDownloaded: isDownloaded,
        audioLocalPath: audioLocalPath,
      ),
      sentences: sentences
          .map((s) => s.toEntity())
          .toList(growable: false),
    );
  }

  Episode _baseEntity({
    required bool isDownloaded,
    required String? audioLocalPath,
  }) {
    final published = DateTime.parse(publishedDate);
    final modified =
        lastModified != null ? DateTime.parse(lastModified!) : published;
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
