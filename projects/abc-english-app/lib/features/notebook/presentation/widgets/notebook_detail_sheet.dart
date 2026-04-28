import 'package:flutter/material.dart';

import '../../domain/entities/notebook_entry.dart';

/// Bottom sheet for viewing/editing a notebook entry.
///
/// Users can edit `meaning` and `note`. The word itself is shown read-only
/// to discourage accidental renames — deleting and re-adding is the
/// intentional flow for that. Save dispatches an upsert via [onSave] and
/// pops when the upsert resolves.
class NotebookDetailSheet extends StatefulWidget {
  const NotebookDetailSheet({
    super.key,
    required this.entry,
    required this.onSave,
  });

  final NotebookEntry entry;
  final Future<void> Function({
    required String id,
    String? meaning,
    String? note,
  }) onSave;

  @override
  State<NotebookDetailSheet> createState() => _NotebookDetailSheetState();
}

class _NotebookDetailSheetState extends State<NotebookDetailSheet> {
  late final TextEditingController _meaning;
  late final TextEditingController _note;
  bool _saving = false;

  @override
  void initState() {
    super.initState();
    _meaning = TextEditingController(text: widget.entry.meaning ?? '');
    _note = TextEditingController(text: widget.entry.note ?? '');
  }

  @override
  void dispose() {
    _meaning.dispose();
    _note.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    setState(() => _saving = true);
    try {
      await widget.onSave(
        id: widget.entry.id,
        meaning: _meaning.text.trim().isEmpty ? null : _meaning.text.trim(),
        note: _note.text.trim().isEmpty ? null : _note.text.trim(),
      );
      if (mounted) Navigator.of(context).pop();
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final textTheme = Theme.of(context).textTheme;
    final insets = MediaQuery.of(context).viewInsets;
    return Padding(
      padding: EdgeInsets.fromLTRB(16, 12, 16, 16 + insets.bottom),
      child: SafeArea(
        top: false,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Center(
              child: Container(
                width: 36,
                height: 4,
                margin: const EdgeInsets.only(bottom: 12),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.outlineVariant,
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
            ),
            Text(widget.entry.word,
                style: textTheme.titleLarge
                    ?.copyWith(fontWeight: FontWeight.w700)),
            if (widget.entry.context.isNotEmpty) ...[
              const SizedBox(height: 4),
              Text(
                widget.entry.context,
                style: textTheme.bodySmall?.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                  fontStyle: FontStyle.italic,
                ),
              ),
            ],
            const SizedBox(height: 16),
            TextField(
              key: const Key('notebook-detail-meaning'),
              controller: _meaning,
              decoration: const InputDecoration(
                labelText: '뜻',
                border: OutlineInputBorder(),
              ),
              minLines: 1,
              maxLines: 3,
            ),
            const SizedBox(height: 12),
            TextField(
              key: const Key('notebook-detail-note'),
              controller: _note,
              decoration: const InputDecoration(
                labelText: '메모',
                border: OutlineInputBorder(),
              ),
              minLines: 2,
              maxLines: 5,
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                TextButton(
                  onPressed: _saving ? null : () => Navigator.pop(context),
                  child: const Text('취소'),
                ),
                const SizedBox(width: 8),
                FilledButton(
                  key: const Key('notebook-detail-save'),
                  onPressed: _saving ? null : _save,
                  child: _saving
                      ? const SizedBox(
                          width: 16,
                          height: 16,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('저장'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
