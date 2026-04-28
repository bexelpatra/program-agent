import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

import '../../../../core/domain/entities/sentence.dart';

/// One sentence in the player's transcript list.
///
/// The sentence itself is split on whitespace and rendered as a
/// `RichText` where each non-whitespace token is its own [TextSpan] with a
/// dedicated [LongPressGestureRecognizer]. This is the Flutter-native
/// equivalent of the web UI's `<span class="word">` spans — see
/// `projects/abc-english/web/static/js/study.js::tokenizeSentence`.
///
/// - Tap on the tile (not a word) → [onTap] (seek to sentence).
/// - Long-press on a word → [onWordLongPress] (opens lookup sheet).
///
/// [isCurrent] controls highlight + bold so the parent widget can cheaply
/// swap a single tile's style when the playback head crosses sentence
/// boundaries without rebuilding the whole list.
class PlayerSentenceTile extends StatefulWidget {
  const PlayerSentenceTile({
    super.key,
    required this.sentence,
    required this.isCurrent,
    required this.onTap,
    required this.onWordLongPress,
  });

  final Sentence sentence;
  final bool isCurrent;
  final VoidCallback onTap;

  /// Called with `(word, sentenceText)` — the parent uses this pair to
  /// seed the lookup bottom sheet and build the `context` param for the
  /// `/api/v1/lookup` call.
  final void Function(String word, String sentenceContext) onWordLongPress;

  @override
  State<PlayerSentenceTile> createState() => _PlayerSentenceTileState();
}

class _PlayerSentenceTileState extends State<PlayerSentenceTile> {
  final List<LongPressGestureRecognizer> _recognizers = [];

  @override
  void dispose() {
    for (final r in _recognizers) {
      r.dispose();
    }
    _recognizers.clear();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final textTheme = Theme.of(context).textTheme;

    // Re-create recognizers for every build — cheap, and it keeps each
    // span's callback bound to the right token when the underlying
    // sentence text changes (e.g. transcript reload).
    for (final r in _recognizers) {
      r.dispose();
    }
    _recognizers.clear();

    final spans = _buildSpans(
      text: widget.sentence.text,
      baseStyle: textTheme.bodyLarge?.copyWith(
            fontWeight: widget.isCurrent
                ? FontWeight.w600
                : FontWeight.w400,
            color: widget.isCurrent
                ? scheme.onPrimaryContainer
                : scheme.onSurface,
          ) ??
          const TextStyle(),
      onWordLongPress: (word) =>
          widget.onWordLongPress(word, widget.sentence.text),
    );

    final indexSpan = TextSpan(
      text: '${widget.sentence.index + 1}. ',
      style: textTheme.bodyMedium?.copyWith(
        color: scheme.onSurfaceVariant,
        fontFeatures: const [FontFeature.tabularFigures()],
      ),
    );

    return GestureDetector(
      key: Key('player-sentence-${widget.sentence.index}'),
      behavior: HitTestBehavior.opaque,
      onTap: widget.onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 160),
        curve: Curves.easeOut,
        margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
        decoration: BoxDecoration(
          color: widget.isCurrent
              ? scheme.primaryContainer
              : Colors.transparent,
          borderRadius: BorderRadius.circular(10),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            RichText(
              text: TextSpan(children: [indexSpan, ...spans]),
            ),
            const SizedBox(height: 4),
            Text(
              _formatTimeRange(widget.sentence.startMs, widget.sentence.endMs),
              style: textTheme.labelSmall?.copyWith(
                color: scheme.onSurfaceVariant,
                fontFeatures: const [FontFeature.tabularFigures()],
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ---------------------------------------------------------------------------
  // Span building
  // ---------------------------------------------------------------------------

  static final RegExp _punctuation =
      RegExp(r"^[^\p{L}\p{N}'\-]+|[^\p{L}\p{N}'\-]+$", unicode: true);

  List<InlineSpan> _buildSpans({
    required String text,
    required TextStyle baseStyle,
    required void Function(String word) onWordLongPress,
  }) {
    if (text.isEmpty) return const [];
    final spans = <InlineSpan>[];
    final parts = text.split(RegExp(r'(\s+)'));
    for (final part in parts) {
      if (part.isEmpty) continue;
      if (RegExp(r'^\s+$').hasMatch(part)) {
        spans.add(TextSpan(text: part, style: baseStyle));
        continue;
      }
      final cleaned = part.replaceAll(_punctuation, '');
      if (cleaned.isEmpty) {
        spans.add(TextSpan(text: part, style: baseStyle));
        continue;
      }
      final recognizer = LongPressGestureRecognizer()
        ..onLongPress = () => onWordLongPress(cleaned.toLowerCase());
      _recognizers.add(recognizer);
      spans.add(TextSpan(
        text: part,
        style: baseStyle,
        recognizer: recognizer,
      ));
    }
    return spans;
  }

  static String _formatTimeRange(int startMs, int endMs) {
    return '(${_fmt(startMs)}–${_fmt(endMs)})';
  }

  static String _fmt(int ms) {
    if (ms < 0) return '--:--';
    final totalSec = ms ~/ 1000;
    final minutes = (totalSec ~/ 60).toString().padLeft(2, '0');
    final seconds = (totalSec % 60).toString().padLeft(2, '0');
    return '$minutes:$seconds';
  }
}
