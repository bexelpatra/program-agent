import 'package:flutter/material.dart';

import '../../../../core/domain/entities/episode.dart';
import 'download_badge.dart';

/// Single-episode card used by the episode list screen.
///
/// Mirrors the web `.episode-card` pattern (title on top, meta row underneath
/// with date / duration / optional WER badge) but styled with Material 3
/// primitives so it sits well alongside other native widgets (BottomNav,
/// Snackbars, ripples).
class EpisodeCard extends StatelessWidget {
  const EpisodeCard({
    super.key,
    required this.episode,
    required this.onTap,
  });

  final Episode episode;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final textTheme = Theme.of(context).textTheme;

    return Card(
      key: Key('episode-card-${episode.id}'),
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                episode.title,
                style: textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.w600,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 8),
              _MetaRow(
                date: episode.publishedDate,
                durationMs: episode.durationMs,
                avgWer: episode.avgWer,
                isDownloaded: episode.isDownloaded,
                mutedStyle: textTheme.bodySmall?.copyWith(
                  color: scheme.onSurfaceVariant,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _MetaRow extends StatelessWidget {
  const _MetaRow({
    required this.date,
    required this.durationMs,
    required this.avgWer,
    required this.isDownloaded,
    required this.mutedStyle,
  });

  final DateTime date;
  final int durationMs;
  final double? avgWer;
  final bool isDownloaded;
  final TextStyle? mutedStyle;

  @override
  Widget build(BuildContext context) {
    return Wrap(
      spacing: 10,
      runSpacing: 6,
      crossAxisAlignment: WrapCrossAlignment.center,
      children: [
        Text(_formatDate(date), style: mutedStyle),
        Text('·', style: mutedStyle),
        Text(_formatDurationMs(durationMs), style: mutedStyle),
        if (avgWer != null) _WerBadge(value: avgWer!),
        DownloadBadge(isDownloaded: isDownloaded),
      ],
    );
  }

  static String _formatDate(DateTime d) {
    final y = d.year.toString().padLeft(4, '0');
    final m = d.month.toString().padLeft(2, '0');
    final day = d.day.toString().padLeft(2, '0');
    return '$y-$m-$day';
  }

  static String _formatDurationMs(int ms) {
    if (ms <= 0) return '--:--';
    final totalSec = ms ~/ 1000;
    final minutes = (totalSec ~/ 60).toString().padLeft(2, '0');
    final seconds = (totalSec % 60).toString().padLeft(2, '0');
    return '$minutes:$seconds';
  }
}

class _WerBadge extends StatelessWidget {
  const _WerBadge({required this.value});

  final double value;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    // Lower WER => transcript quality is better. Colour is informational
    // only; the numeric value carries the meaning.
    final label = 'WER ${(value * 100).toStringAsFixed(0)}%';
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      decoration: BoxDecoration(
        color: scheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: scheme.outlineVariant),
      ),
      child: Text(
        label,
        style: Theme.of(context).textTheme.labelSmall?.copyWith(
              color: scheme.onSurface,
              fontWeight: FontWeight.w500,
            ),
      ),
    );
  }
}
