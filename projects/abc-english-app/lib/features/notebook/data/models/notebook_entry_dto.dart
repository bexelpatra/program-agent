// ignore_for_file: invalid_annotation_target

import 'package:freezed_annotation/freezed_annotation.dart';

import '../../domain/entities/notebook_entry.dart';
import '../../domain/entities/sync_status.dart';

part 'notebook_entry_dto.freezed.dart';
part 'notebook_entry_dto.g.dart';

/// Wire-format mirror of a single notebook entry in the v1 API
/// (`projects/abc-english/web/api/v1/notebook.py`).
@freezed
class NotebookEntryDto with _$NotebookEntryDto {
  const NotebookEntryDto._();

  const factory NotebookEntryDto({
    required String id,
    required String word,
    @Default('') String context,
    @JsonKey(name: 'episode_id') String? episodeId,
    @JsonKey(name: 'sentence_index') int? sentenceIndex,
    String? meaning,
    String? note,
    @JsonKey(name: 'created_at') String? createdAt,
    @JsonKey(name: 'last_modified') String? lastModified,
  }) = _NotebookEntryDto;

  factory NotebookEntryDto.fromJson(Map<String, dynamic> json) =>
      _$NotebookEntryDtoFromJson(json);

  /// Map to the domain entity. Entries fresh off the wire are always
  /// [SyncStatus.synced] — the local datasource is the only place that
  /// produces pending statuses.
  NotebookEntry toEntity() {
    final modified = lastModified != null
        ? DateTime.parse(lastModified!)
        : DateTime.now().toUtc();
    final created = createdAt != null
        ? DateTime.parse(createdAt!)
        : modified;
    return NotebookEntry(
      id: id,
      word: word,
      context: context,
      episodeId: (episodeId?.isEmpty ?? true) ? null : episodeId,
      sentenceIndex: sentenceIndex,
      meaning: (meaning?.isEmpty ?? true) ? null : meaning,
      note: (note?.isEmpty ?? true) ? null : note,
      createdAt: created,
      lastModified: modified,
      syncStatus: SyncStatus.synced,
    );
  }
}
