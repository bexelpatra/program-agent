// `JsonKey` on a freezed constructor parameter is the documented pattern
// but analyzer 3.x flags it. See https://github.com/rrousselGit/freezed#custom-json-keys
// ignore_for_file: invalid_annotation_target

import 'package:freezed_annotation/freezed_annotation.dart';

import '../../domain/entities/lookup_result.dart';

part 'lookup_result_dto.freezed.dart';
part 'lookup_result_dto.g.dart';

/// Wire shape of the `/api/v1/lookup` response.
///
/// Matches `src/ollama_client.py::LookupResult` on the backend:
/// ```json
/// {
///   "term": "...",
///   "term_type": "word|phrasal_verb|idiom|collocation",
///   "explanation_en": "...",
///   "etymology": "..." | null,
///   "examples": ["...", ...]
/// }
/// ```
///
/// The response may also carry a `"source": "cache|ollama"` envelope field —
/// we ignore it here because it doesn't affect the UI.
@freezed
class LookupResultDto with _$LookupResultDto {
  const LookupResultDto._();

  const factory LookupResultDto({
    required String term,
    @JsonKey(name: 'term_type') String? termType,
    @JsonKey(name: 'explanation_en') String? explanationEn,
    String? etymology,
    @Default(<String>[]) List<String> examples,
  }) = _LookupResultDto;

  factory LookupResultDto.fromJson(Map<String, dynamic> json) =>
      _$LookupResultDtoFromJson(json);

  /// Map the DTO into the feature's domain entity.
  ///
  /// We fold `explanation_en` into `definitions` as a single entry so the
  /// UI can render a bullet list uniformly. If the backend later returns a
  /// structured `definitions` array we'll widen this mapping.
  LookupResult toEntity() {
    final defs = <String>[
      if ((explanationEn ?? '').trim().isNotEmpty) explanationEn!.trim(),
    ];
    return LookupResult(
      word: term,
      definitions: defs,
      examples: examples,
      termType: termType,
      etymology: (etymology ?? '').trim().isEmpty ? null : etymology,
    );
  }
}
