// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'episode_detail_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$EpisodeDetailDtoImpl _$$EpisodeDetailDtoImplFromJson(
  Map<String, dynamic> json,
) => _$EpisodeDetailDtoImpl(
  id: json['id'] as String,
  title: json['title'] as String,
  publishedDate: json['published_date'] as String,
  durationSeconds: (json['duration'] as num?)?.toInt(),
  avgWer: (json['avg_wer'] as num?)?.toDouble(),
  lastModified: json['last_modified'] as String?,
  sentences:
      (json['sentences'] as List<dynamic>?)
          ?.map((e) => SentenceDto.fromJson(e as Map<String, dynamic>))
          .toList() ??
      const <SentenceDto>[],
);

Map<String, dynamic> _$$EpisodeDetailDtoImplToJson(
  _$EpisodeDetailDtoImpl instance,
) => <String, dynamic>{
  'id': instance.id,
  'title': instance.title,
  'published_date': instance.publishedDate,
  'duration': instance.durationSeconds,
  'avg_wer': instance.avgWer,
  'last_modified': instance.lastModified,
  'sentences': instance.sentences,
};
