// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'notebook_entry_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$NotebookEntryDtoImpl _$$NotebookEntryDtoImplFromJson(
  Map<String, dynamic> json,
) => _$NotebookEntryDtoImpl(
  id: json['id'] as String,
  word: json['word'] as String,
  context: json['context'] as String? ?? '',
  episodeId: json['episode_id'] as String?,
  sentenceIndex: (json['sentence_index'] as num?)?.toInt(),
  meaning: json['meaning'] as String?,
  note: json['note'] as String?,
  createdAt: json['created_at'] as String?,
  lastModified: json['last_modified'] as String?,
);

Map<String, dynamic> _$$NotebookEntryDtoImplToJson(
  _$NotebookEntryDtoImpl instance,
) => <String, dynamic>{
  'id': instance.id,
  'word': instance.word,
  'context': instance.context,
  'episode_id': instance.episodeId,
  'sentence_index': instance.sentenceIndex,
  'meaning': instance.meaning,
  'note': instance.note,
  'created_at': instance.createdAt,
  'last_modified': instance.lastModified,
};
