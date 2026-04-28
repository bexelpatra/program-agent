import 'package:flutter/material.dart';

/// Small reusable badge indicating whether an episode is available offline.
///
/// Rendered as a pill-shaped chip with a download icon + label when the
/// episode has been downloaded. When not downloaded the widget collapses
/// to `SizedBox.shrink()` so callers can drop it into a row without
/// having to conditionally render themselves.
class DownloadBadge extends StatelessWidget {
  const DownloadBadge({
    super.key,
    required this.isDownloaded,
    this.label = '오프라인',
  });

  final bool isDownloaded;
  final String label;

  @override
  Widget build(BuildContext context) {
    if (!isDownloaded) {
      return const SizedBox.shrink();
    }
    final scheme = Theme.of(context).colorScheme;
    return Semantics(
      label: '다운로드됨',
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
        decoration: BoxDecoration(
          color: scheme.secondaryContainer,
          borderRadius: BorderRadius.circular(999),
          border: Border.all(color: scheme.outlineVariant),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              Icons.download_done_rounded,
              size: 14,
              color: scheme.onSecondaryContainer,
            ),
            const SizedBox(width: 4),
            Text(
              label,
              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                    color: scheme.onSecondaryContainer,
                    fontWeight: FontWeight.w600,
                  ),
            ),
          ],
        ),
      ),
    );
  }
}
