import 'package:freezed_annotation/freezed_annotation.dart';

part 'lookup_result.freezed.dart';

/// Domain entity for a dictionary lookup of a single word or phrase.
///
/// Shape chosen to match the backend response emitted by
/// `projects/abc-english/web/api/v1/lookup.py` (delegates to
/// `src/ollama_client.py::LookupResult`):
///   `term`, `term_type`, `explanation_en`, `etymology?`, `examples[]`.
///
/// The task-board asked for `(word, phonetic?, definitions, examples)`. We
/// keep `examples` as-is, fold `explanation_en` into [definitions] as a
/// single-entry list (so the UI works regardless of wire shape), and treat
/// `phonetic` as optional — the current backend does not emit it, so it is
/// always `null` for now but reserved for future enrichment. [termType] and
/// [etymology] are surfaced so the UI can mirror the web modal's "idiom
/// etymology" section without losing information.
@freezed
class LookupResult with _$LookupResult {
  const factory LookupResult({
    required String word,
    required List<String> definitions,
    required List<String> examples,
    String? phonetic,
    String? termType,
    String? etymology,
  }) = _LookupResult;
}
