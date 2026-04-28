import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/errors/app_exception.dart';
import '../../../features/lookup/data/repositories/lookup_repository_impl.dart';
import '../../../features/lookup/domain/entities/lookup_result.dart';
import '../../../features/lookup/domain/usecases/lookup_word.dart';

/// Signature for the "add to notebook" callback.
///
/// The callback is invoked when the user taps "단어장에 추가" inside the
/// bottom sheet. Implementations decide how the add is performed (usually
/// by calling a notebook repository/use-case in the host feature) and must
/// return a [Future] that resolves to `true` on success and `false` on
/// failure — the sheet uses that to render the saved/failed state.
///
/// Keeping this as a callback (rather than letting the sheet reach into a
/// notebook provider directly) is what keeps this widget in `shared/`
/// while the notebook feature stays encapsulated in its own slice:
/// the sheet depends only on `features/lookup/domain` + core errors.
typedef OnAddToNotebook = Future<bool> Function({
  required String word,
  required String context,
  String? episodeId,
  int? sentenceIndex,
  String? meaning,
  String? note,
});

/// Bottom sheet presented on long-press of a word in the transcript.
///
/// - Fetches the lookup result asynchronously via [LookupWord].
/// - Renders word → definitions → examples.
/// - "단어장에 추가" CTA invokes [onAddToNotebook] with episode provenance;
///   the host wires that to its notebook repository/use-case.
class LookupBottomSheet extends ConsumerStatefulWidget {
  const LookupBottomSheet({
    super.key,
    required this.word,
    required this.context,
    required this.episodeId,
    required this.sentenceIndex,
    required this.onAddToNotebook,
  });

  final String word;
  final String context;
  final String episodeId;
  final int sentenceIndex;
  final OnAddToNotebook onAddToNotebook;

  /// Convenience: open the sheet as a modal bottom sheet.
  static Future<void> show(
    BuildContext ctx, {
    required String word,
    required String context,
    required String episodeId,
    required int sentenceIndex,
    required OnAddToNotebook onAddToNotebook,
  }) {
    return showModalBottomSheet<void>(
      context: ctx,
      isScrollControlled: true,
      useSafeArea: true,
      showDragHandle: true,
      builder: (_) => LookupBottomSheet(
        word: word,
        context: context,
        episodeId: episodeId,
        sentenceIndex: sentenceIndex,
        onAddToNotebook: onAddToNotebook,
      ),
    );
  }

  @override
  ConsumerState<LookupBottomSheet> createState() => _LookupBottomSheetState();
}

class _LookupBottomSheetState extends ConsumerState<LookupBottomSheet> {
  late Future<LookupResult> _future;
  bool _saving = false;
  bool _saved = false;

  @override
  void initState() {
    super.initState();
    _future = _runLookup();
  }

  Future<LookupResult> _runLookup() async {
    final repo = ref.read(lookupRepositoryProvider);
    final useCase = LookupWord(repo);
    final result = await useCase(
      word: widget.word,
      context: widget.context,
    );
    return result.when(
      success: (value) => value,
      failure: (error) => throw error,
    );
  }

  Future<void> _addToNotebook(LookupResult result) async {
    setState(() => _saving = true);
    try {
      final meaning = result.definitions.isEmpty
          ? null
          : result.definitions.join('\n');
      final ok = await widget.onAddToNotebook(
        word: widget.word,
        context: widget.context,
        episodeId: widget.episodeId,
        sentenceIndex: widget.sentenceIndex,
        meaning: meaning,
      );
      if (!mounted) return;
      setState(() {
        _saving = false;
        _saved = ok;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(ok ? '단어장에 추가되었습니다' : '추가에 실패했습니다'),
          duration: const Duration(seconds: 2),
        ),
      );
    } catch (_) {
      if (!mounted) return;
      setState(() => _saving = false);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('추가에 실패했습니다')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: ConstrainedBox(
        constraints: BoxConstraints(
          maxHeight: MediaQuery.of(context).size.height * 0.75,
        ),
        child: Padding(
          padding: EdgeInsets.only(
            left: 20,
            right: 20,
            top: 8,
            bottom: 16 + MediaQuery.of(context).viewInsets.bottom,
          ),
          child: FutureBuilder<LookupResult>(
            future: _future,
            builder: (context, snapshot) {
              if (snapshot.connectionState != ConnectionState.done) {
                return _LoadingView(word: widget.word);
              }
              if (snapshot.hasError) {
                return _ErrorView(
                  word: widget.word,
                  error: snapshot.error,
                  onRetry: () {
                    setState(() {
                      _future = _runLookup();
                    });
                  },
                );
              }
              final result = snapshot.data!;
              return _ResultView(
                result: result,
                saving: _saving,
                saved: _saved,
                onAdd: () => _addToNotebook(result),
              );
            },
          ),
        ),
      ),
    );
  }
}

class _LoadingView extends StatelessWidget {
  const _LoadingView({required this.word});

  final String word;

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          word,
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.w700,
              ),
        ),
        const SizedBox(height: 16),
        const Row(
          children: [
            SizedBox(
              width: 18,
              height: 18,
              child: CircularProgressIndicator(strokeWidth: 2),
            ),
            SizedBox(width: 10),
            Text('조회 중...'),
          ],
        ),
        const SizedBox(height: 16),
      ],
    );
  }
}

class _ErrorView extends StatelessWidget {
  const _ErrorView({
    required this.word,
    required this.error,
    required this.onRetry,
  });

  final String word;
  final Object? error;
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          word,
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.w700,
              ),
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Icon(Icons.error_outline, color: scheme.error),
            const SizedBox(width: 8),
            Expanded(child: Text(_friendlyMessage(error))),
          ],
        ),
        const SizedBox(height: 16),
        Row(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            TextButton(
              onPressed: () => Navigator.of(context).maybePop(),
              child: const Text('닫기'),
            ),
            FilledButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh_rounded),
              label: const Text('다시 시도'),
            ),
          ],
        ),
      ],
    );
  }

  static String _friendlyMessage(Object? error) {
    if (error is UnauthorizedException) {
      return '인증이 필요합니다. 앱 토큰을 확인해주세요.';
    }
    if (error is NetworkException) {
      return '네트워크 오류: ${error.message}';
    }
    if (error is AppException) {
      return error.message;
    }
    return '단어를 조회하지 못했습니다.';
  }
}

class _ResultView extends StatelessWidget {
  const _ResultView({
    required this.result,
    required this.saving,
    required this.saved,
    required this.onAdd,
  });

  final LookupResult result;
  final bool saving;
  final bool saved;
  final VoidCallback onAdd;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final textTheme = Theme.of(context).textTheme;
    return SingleChildScrollView(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: [
              Flexible(
                child: Text(
                  result.word,
                  style: textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
              if (result.phonetic != null) ...[
                const SizedBox(width: 10),
                Text(
                  '/${result.phonetic}/',
                  style: textTheme.bodyMedium?.copyWith(
                    color: scheme.onSurfaceVariant,
                  ),
                ),
              ],
              if (result.termType != null) ...[
                const SizedBox(width: 10),
                Container(
                  padding: const EdgeInsets.symmetric(
                      horizontal: 8, vertical: 2),
                  decoration: BoxDecoration(
                    color: scheme.secondaryContainer,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    result.termType!,
                    style: textTheme.labelSmall?.copyWith(
                      color: scheme.onSecondaryContainer,
                    ),
                  ),
                ),
              ],
            ],
          ),
          const SizedBox(height: 12),
          if (result.definitions.isEmpty)
            Text(
              '뜻 정보가 없습니다.',
              style: textTheme.bodyMedium?.copyWith(
                color: scheme.onSurfaceVariant,
                fontStyle: FontStyle.italic,
              ),
            )
          else
            _SectionBlock(
              title: '뜻',
              items: result.definitions,
            ),
          if (result.etymology != null) ...[
            const SizedBox(height: 12),
            _SectionBlock(title: '어원', items: [result.etymology!]),
          ],
          if (result.examples.isNotEmpty) ...[
            const SizedBox(height: 12),
            _SectionBlock(title: '예문', items: result.examples),
          ],
          const SizedBox(height: 20),
          SizedBox(
            width: double.infinity,
            child: FilledButton.icon(
              key: const Key('lookup-add-to-notebook'),
              onPressed: (saving || saved) ? null : onAdd,
              icon: Icon(
                saved
                    ? Icons.check_circle_rounded
                    : Icons.bookmark_add_rounded,
              ),
              label: Text(
                saving
                    ? '추가 중...'
                    : saved
                        ? '단어장에 추가됨'
                        : '단어장에 추가',
              ),
            ),
          ),
          const SizedBox(height: 8),
        ],
      ),
    );
  }
}

class _SectionBlock extends StatelessWidget {
  const _SectionBlock({required this.title, required this.items});

  final String title;
  final List<String> items;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final textTheme = Theme.of(context).textTheme;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: textTheme.labelLarge?.copyWith(
            color: scheme.onSurfaceVariant,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 4),
        ...items.map(
          (it) => Padding(
            padding: const EdgeInsets.only(top: 4),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Padding(
                  padding: EdgeInsets.only(top: 6, right: 8),
                  child: Icon(Icons.circle, size: 5),
                ),
                Expanded(
                  child: Text(
                    it,
                    style: textTheme.bodyMedium,
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
