import 'package:flutter/material.dart';

/// Data bag returned by [NotebookAddDialog.show] on a successful submit.
class NotebookAddPayload {
  const NotebookAddPayload({
    required this.word,
    required this.context,
    this.meaning,
    this.note,
  });

  final String word;
  final String context;
  final String? meaning;
  final String? note;
}

/// Modal dialog for adding a notebook entry manually (without a source
/// sentence). `word` is required; everything else is optional and trimmed
/// to `null` when blank so we don't spam the DB with empty strings.
class NotebookAddDialog extends StatefulWidget {
  const NotebookAddDialog({super.key});

  static Future<NotebookAddPayload?> show(BuildContext context) {
    return showDialog<NotebookAddPayload>(
      context: context,
      builder: (_) => const NotebookAddDialog(),
    );
  }

  @override
  State<NotebookAddDialog> createState() => _NotebookAddDialogState();
}

class _NotebookAddDialogState extends State<NotebookAddDialog> {
  final _formKey = GlobalKey<FormState>();
  final _word = TextEditingController();
  final _context = TextEditingController();
  final _meaning = TextEditingController();
  final _note = TextEditingController();

  @override
  void dispose() {
    _word.dispose();
    _context.dispose();
    _meaning.dispose();
    _note.dispose();
    super.dispose();
  }

  void _submit() {
    if (!_formKey.currentState!.validate()) return;
    Navigator.of(context).pop(
      NotebookAddPayload(
        word: _word.text.trim(),
        context: _context.text.trim(),
        meaning: _meaning.text.trim().isEmpty ? null : _meaning.text.trim(),
        note: _note.text.trim().isEmpty ? null : _note.text.trim(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('단어 추가'),
      content: SingleChildScrollView(
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextFormField(
                key: const Key('notebook-add-word'),
                controller: _word,
                autofocus: true,
                decoration: const InputDecoration(
                  labelText: '단어 *',
                  hintText: '예: albeit',
                ),
                validator: (v) =>
                    (v == null || v.trim().isEmpty) ? '단어는 필수' : null,
              ),
              const SizedBox(height: 12),
              TextFormField(
                key: const Key('notebook-add-context'),
                controller: _context,
                decoration: const InputDecoration(
                  labelText: '문맥',
                  hintText: '어떤 문장/상황에서 봤는지',
                ),
                maxLines: 2,
              ),
              const SizedBox(height: 12),
              TextFormField(
                key: const Key('notebook-add-meaning'),
                controller: _meaning,
                decoration: const InputDecoration(labelText: '뜻'),
                minLines: 1,
                maxLines: 3,
              ),
              const SizedBox(height: 12),
              TextFormField(
                key: const Key('notebook-add-note'),
                controller: _note,
                decoration: const InputDecoration(labelText: '메모'),
                minLines: 1,
                maxLines: 3,
              ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('취소'),
        ),
        FilledButton(
          key: const Key('notebook-add-submit'),
          onPressed: _submit,
          child: const Text('추가'),
        ),
      ],
    );
  }
}
