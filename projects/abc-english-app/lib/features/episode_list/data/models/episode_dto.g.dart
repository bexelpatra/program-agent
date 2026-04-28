// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'episode_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$EpisodeDtoImpl _$$EpisodeDtoImplFromJson(Map<String, dynamic> json) =>
    _$EpisodeDtoImpl(
      id: json['id'] as String,
      title: json['title'] as String,
      publishedDate: json['published_date'] as String,
      durationSeconds: (json['duration'] as num?)?.toInt(),
      avgWer: (json['avg_wer'] as num?)?.toDouble(),
      lastModified: json['last_modified'] as String?,
    );

Map<String, dynamic> _$$EpisodeDtoImplToJson(_$EpisodeDtoImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'title': instance.title,
      'published_date': instance.publishedDate,
      'duration': instance.durationSeconds,
      'avg_wer': instance.avgWer,
      'last_modified': instance.lastModified,
    };
