import 'package:flutter/material.dart';

/// Scrubber for the current track.
///
/// Local drag state: while the user is dragging the thumb, we stop
/// reacting to `positionMs` from the repository so the thumb doesn't
/// snap back on each stream tick. On drag-end we call [onSeek] with the
/// final value and let the repository's next tick take over.
class PlayerSeekBar extends StatefulWidget {
  const PlayerSeekBar({
    super.key,
    required this.positionMs,
    required this.totalDurationMs,
    required this.onSeek,
  });

  final int positionMs;
  final int totalDurationMs;
  final ValueChanged<Duration> onSeek;

  @override
  State<PlayerSeekBar> createState() => _PlayerSeekBarState();
}

class _PlayerSeekBarState extends State<PlayerSeekBar> {
  double? _dragValueMs;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final total = widget.totalDurationMs.clamp(0, 1 << 31).toDouble();
    // Avoid a zero-range Slider (throws). Use 1.0 as a harmless placeholder
    // and keep the value locked at 0 until duration resolves.
    final max = total > 0 ? total : 1.0;
    final currentMs = _dragValueMs ??
        widget.positionMs.clamp(0, total > 0 ? total.toInt() : 0).toDouble();

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12),
      child: Column(
        children: [
          SliderTheme(
            data: SliderTheme.of(context).copyWith(
              trackHeight: 3,
              thumbShape:
                  const RoundSliderThumbShape(enabledThumbRadius: 7),
              overlayShape:
                  const RoundSliderOverlayShape(overlayRadius: 18),
            ),
            child: Slider(
              key: const Key('player-seek-bar'),
              min: 0,
              max: max,
              value: currentMs.clamp(0, max).toDouble(),
              onChanged: total > 0
                  ? (v) => setState(() => _dragValueMs = v)
                  : null,
              onChangeEnd: total > 0
                  ? (v) {
                      setState(() => _dragValueMs = null);
                      widget.onSeek(Duration(milliseconds: v.round()));
                    }
                  : null,
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  _fmt(currentMs.round()),
                  style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: scheme.onSurfaceVariant,
                      ),
                ),
                Text(
                  _fmt(widget.totalDurationMs),
                  style: Theme.of(context).textTheme.labelMedium?.copyWith(
                        color: scheme.onSurfaceVariant,
                      ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  static String _fmt(int ms) {
    if (ms <= 0) return '0:00';
    final totalSec = ms ~/ 1000;
    final minutes = (totalSec ~/ 60);
    final seconds = (totalSec % 60).toString().padLeft(2, '0');
    return '$minutes:$seconds';
  }
}
