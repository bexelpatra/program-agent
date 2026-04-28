import 'package:abc_english_app/core/domain/entities/sentence.dart';
import 'package:abc_english_app/features/player/domain/utils/compute_current_sentence_index.dart';
import 'package:flutter_test/flutter_test.dart';

/// Unit tests for the binary-search helper that maps a playback position to
/// the sentence currently being spoken.
///
/// Contract under test (see doc comment on [computeCurrentSentenceIndex]):
///   - empty list → -1
///   - position before first sentence → -1
///   - position past last sentence → last index (most recently started)
///   - boundary: startMs == position → that sentence
///   - boundary: endMs == position → that sentence (still "most recently started")
///   - middle of a sentence → the enclosing sentence
Sentence _s(int i, int start, int end) =>
    Sentence(index: i, text: 'sentence $i', startMs: start, endMs: end);

void main() {
  group('computeCurrentSentenceIndex', () {
    test('empty list → -1', () {
      expect(computeCurrentSentenceIndex(0, const []), -1);
      expect(computeCurrentSentenceIndex(999, const []), -1);
    });

    test('position before first.startMs → -1', () {
      final sentences = [
        _s(0, 1000, 2000),
        _s(1, 2000, 3000),
      ];
      expect(computeCurrentSentenceIndex(0, sentences), -1);
      expect(computeCurrentSentenceIndex(999, sentences), -1);
    });

    test('position exactly at first.startMs → 0', () {
      final sentences = [
        _s(0, 1000, 2000),
        _s(1, 2000, 3000),
      ];
      expect(computeCurrentSentenceIndex(1000, sentences), 0);
    });

    test('position past last.endMs → last index', () {
      final sentences = [
        _s(0, 0, 1000),
        _s(1, 1000, 2000),
        _s(2, 2000, 3000),
      ];
      expect(computeCurrentSentenceIndex(5000, sentences), 2);
      expect(
        computeCurrentSentenceIndex(3000, sentences),
        2,
        reason:
            'endMs == position: sentence 2 is the most recently started one',
      );
    });

    test('position in the middle of sentence → that index', () {
      final sentences = [
        _s(0, 0, 1000),
        _s(1, 1000, 2000),
        _s(2, 2000, 3000),
      ];
      expect(computeCurrentSentenceIndex(500, sentences), 0);
      expect(computeCurrentSentenceIndex(1500, sentences), 1);
      expect(computeCurrentSentenceIndex(2500, sentences), 2);
    });

    test('position exactly on a boundary between sentences → later sentence',
        () {
      // startMs==position wins — `sentences[mid].startMs <= positionMs` puts
      // us onto the sentence that just started.
      final sentences = [
        _s(0, 0, 1000),
        _s(1, 1000, 2000),
        _s(2, 2000, 3000),
      ];
      expect(computeCurrentSentenceIndex(1000, sentences), 1);
      expect(computeCurrentSentenceIndex(2000, sentences), 2);
    });

    test('gap between sentences → most recently started', () {
      final sentences = [
        _s(0, 0, 1000),
        // gap 1000-2000
        _s(1, 2000, 3000),
      ];
      // Position in the gap should return the most recently started sentence.
      expect(computeCurrentSentenceIndex(1500, sentences), 0);
    });

    test('single sentence', () {
      final sentences = [_s(0, 500, 1500)];
      expect(computeCurrentSentenceIndex(0, sentences), -1);
      expect(computeCurrentSentenceIndex(500, sentences), 0);
      expect(computeCurrentSentenceIndex(1000, sentences), 0);
      expect(computeCurrentSentenceIndex(1500, sentences), 0);
      expect(computeCurrentSentenceIndex(5000, sentences), 0);
    });

    test('1000 sentences — binary search correctness at random probes', () {
      // Each sentence is exactly 1000ms long, back-to-back from t=0.
      final sentences = List.generate(
        1000,
        (i) => _s(i, i * 1000, (i + 1) * 1000),
      );
      expect(computeCurrentSentenceIndex(-1, sentences), -1);
      expect(computeCurrentSentenceIndex(0, sentences), 0);
      expect(computeCurrentSentenceIndex(499_500, sentences), 499);
      expect(computeCurrentSentenceIndex(500_000, sentences), 500);
      expect(computeCurrentSentenceIndex(999_999, sentences), 999);
      // Past the end
      expect(computeCurrentSentenceIndex(10_000_000, sentences), 999);
    });
  });
}
