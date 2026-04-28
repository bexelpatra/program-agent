// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'lookup_result_dto.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$LookupResultDtoImpl _$$LookupResultDtoImplFromJson(
  Map<String, dynamic> json,
) => _$LookupResultDtoImpl(
  term: json['term'] as String,
  termType: json['term_type'] as String?,
  explanationEn: json['explanation_en'] as String?,
  etymology: json['etymology'] as String?,
  examples:
      (json['examples'] as List<dynamic>?)?.map((e) => e as String).toList() ??
      const <String>[],
);

Map<String, dynamic> _$$LookupResultDtoImplToJson(
  _$LookupResultDtoImpl instance,
) => <String, dynamic>{
  'term': instance.term,
  'term_type': instance.termType,
  'explanation_en': instance.explanationEn,
  'etymology': instance.etymology,
  'examples': instance.examples,
};
