import 'package:flutter/material.dart';

import '../../domain/entities/notebook_entry.dart';
import '../../domain/entities/sync_status.dart';

/// Single-row representation of a notebook entry.
///
/// Swipe-from-end triggers [onDelete] (with confirmation dialog to guard
/// against accidental taps). Tap opens the detail sheet via [onTap].
class NotebookEntryTile extends StatelessWidget {
  const NotebookEntryTile({
    super.key,
    required this.entry,
    required this.onTap,
    required this.onDelete,
  });

  final NotebookEntry entry;
  final VoidCallback onTap;
  final Future<void> Function() onDelete;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final textTheme = Theme.of(context).textTheme;

    return Dismissible(
      key: Key('notebook-tile-${entry.id}'),
      direction: DismissDirection.endToStart,
      background: Container(
        color: scheme.errorContainer,
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.symmetric(horizontal: 20),
        child: Icon(Icons.delete_outline, color: scheme.onErrorContainer),
      ),
      confirmDismiss: (_) async {
        final confirmed = await showDialog<bool>(
          context: context,
          builder: (ctx) => AlertDialog(
            title: const Text('삭제'),
            content: Text('"${entry.word}"을(를) 삭제할까요?'),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(ctx, false),
                child: const Text('취소'),
              ),
              FilledButton(
                onPressed: () => Navigator.pop(ctx, true),
                child: const Text('삭제'),
              ),
            ],
          ),
        );
        return confirmed ?? false;
      },
      onDismissed: (_) async {
        await onDelete();
      },
      child: ListTile(
        onTap: onTap,
        title: Row(
          children: [
            Flexible(
              child: Text(
                entry.word,
                style: textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.w600,
                ),
                overflow: TextOverflow.ellipsis,
              ),
            ),
            const SizedBox(width: 8),
            _SyncIndicator(status: entry.syncStatus),
          ],
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (entry.meaning != null && entry.meaning!.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 2),
                child: Text(
                  entry.meaning!,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: textTheme.bodyMedium,
                ),
              )
            else
              Padding(
                padding: const EdgeInsets.only(top: 2),
                child: Text(
                  '뜻 미입력',
                  style: textTheme.bodySmall?.copyWith(
                    color: scheme.onSurfaceVariant,
                    fontStyle: FontStyle.italic,
                  ),
                ),
              ),
            if (entry.note != null && entry.note!.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 2),
                child: Text(
                  entry.note!,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: textTheme.bodySmall?.copyWith(
                    color: scheme.onSurfaceVariant,
                  ),
                ),
              ),
            if (entry.episodeId != null)
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text(
                  _sourceLabel(entry),
                  style: textTheme.labelSmall?.copyWith(
                    color: scheme.onSurfaceVariant,
                  ),
                ),
              ),
          ],
        ),
        isThreeLine: entry.note != null && entry.note!.isNotEmpty,
      ),
    );
  }

  String _sourceLabel(NotebookEntry e) {
    final idx = e.sentenceIndex;
    if (idx == null) {
      return '출처: ${e.episodeId}';
    }
    return '출처: ${e.episodeId} · 문장 ${idx + 1}';
  }
}

class _SyncIndicator extends StatelessWidget {
  const _SyncIndicator({required this.status});

  final SyncStatus status;

  @override
  Widget build(BuildContext context) {
    if (status == SyncStatus.synced) {
      return const SizedBox.shrink();
    }
    final scheme = Theme.of(context).colorScheme;
    return Tooltip(
      message: '서버 동기화 대기 중',
      child: Icon(
        Icons.schedule_rounded,
        size: 16,
        color: scheme.onSurfaceVariant,
      ),
    );
  }
}
