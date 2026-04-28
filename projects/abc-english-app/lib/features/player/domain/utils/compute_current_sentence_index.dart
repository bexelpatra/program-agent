import '../../../../core/domain/entities/sentence.dart';

/// Returns the index into [sentences] of the sentence currently being
/// spoken at [positionMs], or `-1` if no sentence applies (empty list, or
/// position sits before the first sentence starts).
///
/// Contract:
/// - [sentences] must be sorted ascending by [Sentence.startMs]. (This is
///   how the server emits them and how Drift orders them on read — see
///   `episode_detail_local_datasource.getDetail`.)
/// - A sentence matches when `startMs <= positionMs < endMs`. If no such
///   sentence exists (gap between sentences), the most recently *started*
///   sentence is returned so the UI doesn't unhighlight during pauses
///   between utterances — the hint the user most likely wants.
/// - `O(log n)` via binary search. The O(n) linear scan alternative was
///   rejected: positionStream emits at ~10Hz and the cost adds up on long
///   episodes, and the binary-search version is only marginally more code.
int computeCurrentSentenceIndex(
  int positionMs,
  List<Sentence> sentences,
) {
  if (sentences.isEmpty) return -1;
  if (positionMs < sentences.first.startMs) return -1;

  // Find the largest index `lo` such that sentences[lo].startMs <= positionMs.
  // Classic upper_bound-then-decrement.
  int lo = 0;
  int hi = sentences.length; // exclusive upper bound

  while (lo < hi) {
    final mid = (lo + hi) >> 1;
    if (sentences[mid].startMs <= positionMs) {
      lo = mid + 1;
    } else {
      hi = mid;
    }
  }

  // `lo` now points just past the last sentence with startMs <= positionMs.
  // Since we handled `positionMs < first.startMs` above, lo >= 1 here.
  return lo - 1;
}
