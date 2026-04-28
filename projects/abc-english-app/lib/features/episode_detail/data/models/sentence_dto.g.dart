// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'sentence_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$SentenceDtoImpl _$$SentenceDtoImplFromJson(Map<String, dynamic> json) =>
    _$SentenceDtoImpl(
      index: (json['index'] as num).toInt(),
      text: json['text'] as String,
      startMs: (json['start_ms'] as num?)?.toInt(),
      endMs: (json['end_ms'] as num?)?.toInt(),
      wer: (json['wer'] as num?)?.toDouble(),
      difficulty: json['difficulty'] as String?,
    );

Map<String, dynamic> _$$SentenceDtoImplToJson(_$SentenceDtoImpl instance) =>
    <String, dynamic>{
      'index': instance.index,
      'text': instance.text,
      'start_ms': instance.startMs,
      'end_ms': instance.endMs,
      'wer': instance.wer,
      'difficulty': instance.difficulty,
    };
