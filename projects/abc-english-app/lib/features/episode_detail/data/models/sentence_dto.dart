// ignore_for_file: invalid_annotation_target

import 'package:freezed_annotation/freezed_annotation.dart';

import '../../../../core/domain/entities/sentence.dart';

part 'sentence_dto.freezed.dart';
part 'sentence_dto.g.dart';

/// Wire-format mirror of a single sentence element inside
/// `/api/v1/episodes/{id}.sentences[*]`.
///
/// The server already emits millisecond timestamps (`start_ms`/`end_ms`) per
/// `projects/abc-english/web/api/v1/episodes.py::_project_sentence`; keeping
/// the DTO in the same units avoids unit conversions on every hop.
@freezed
class SentenceDto with _$SentenceDto {
  const SentenceDto._();

  const factory SentenceDto({
    required int index,
    required String text,
    @JsonKey(name: 'start_ms') int? startMs,
    @JsonKey(name: 'end_ms') int? endMs,
    double? wer,
    String? difficulty,
  }) = _SentenceDto;

  factory SentenceDto.fromJson(Map<String, dynamic> json) =>
      _$SentenceDtoFromJson(json);

  Sentence toEntity() {
    return Sentence(
      index: index,
      text: text,
      startMs: startMs ?? 0,
      endMs: endMs ?? 0,
      wer: wer,
      difficulty: difficulty,
    );
  }
}
