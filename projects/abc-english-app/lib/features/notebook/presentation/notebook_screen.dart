import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/errors/app_exception.dart';
import '../data/repositories/notebook_repository_impl.dart';
import '../domain/entities/notebook_entry.dart';
import '../domain/usecases/add_notebook_entry.dart';
import '../domain/usecases/delete_notebook_entry.dart';
import '../domain/usecases/list_notebook.dart';
import '../domain/usecases/update_notebook_entry.dart';
import 'widgets/notebook_add_dialog.dart';
import 'widgets/notebook_detail_sheet.dart';
import 'widgets/notebook_entry_tile.dart';

/// Notebook tab root. Shows the saved vocabulary list with search and
/// episode filter, plus a FAB for manual additions.
class NotebookScreen extends ConsumerStatefulWidget {
  const NotebookScreen({super.key});

  @override
  ConsumerState<NotebookScreen> createState() => _NotebookScreenState();
}

class _NotebookScreenState extends ConsumerState<NotebookScreen> {
  String _query = '';
  String? _episodeFilter;
  final _searchController = TextEditingController();

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _openAddDialog() async {
    final payload = await NotebookAddDialog.show(context);
    if (payload == null) return;
    final controller = ref.read(notebookControllerProvider.notifier);
    final ok = await controller.add(payload);
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(ok ? '추가했습니다' : '추가에 실패했습니다')),
    );
  }

  Future<void> _openDetail(NotebookEntry entry) async {
    await showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      showDragHandle: false,
      builder: (_) => NotebookDetailSheet(
        entry: entry,
        onSave: ({required id, meaning, note}) async {
          final ok = await ref
              .read(notebookControllerProvider.notifier)
              .updateEntry(id: id, meaning: meaning, note: note);
          if (!mounted) return;
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(ok ? '저장했습니다' : '저장에 실패했습니다')),
          );
        },
      ),
    );
  }

  Future<void> _deleteEntry(NotebookEntry entry) async {
    final ok = await ref
        .read(notebookControllerProvider.notifier)
        .remove(entry.id);
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(ok ? '삭제했습니다' : '삭제에 실패했습니다'),
        action: SnackBarAction(
          label: '새로고침',
          onPressed: () =>
              ref.read(notebookControllerProvider.notifier).refresh(),
        ),
      ),
    );
  }

  List<NotebookEntry> _applyFilters(List<NotebookEntry> input) {
    final q = _query.trim().toLowerCase();
    Iterable<NotebookEntry> out = input;
    if (q.isNotEmpty) {
      out = out.where((e) =>
          e.word.toLowerCase().contains(q) ||
          (e.meaning?.toLowerCase().contains(q) ?? false) ||
          (e.note?.toLowerCase().contains(q) ?? false));
    }
    if (_episodeFilter != null && _episodeFilter!.isNotEmpty) {
      out = out.where((e) => e.episodeId == _episodeFilter);
    }
    return out.toList(growable: false);
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(notebookControllerProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Notebook')),
      floatingActionButton: FloatingActionButton(
        key: const Key('notebook-add-fab'),
        onPressed: _openAddDialog,
        child: const Icon(Icons.add),
      ),
      body: state.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, _) => _ErrorView(
          message: _friendlyMessage(error),
          onRetry: () =>
              ref.read(notebookControllerProvider.notifier).refresh(),
        ),
        data: (entries) {
          final episodeIds = _episodeIdsFrom(entries);
          final filtered = _applyFilters(entries);
          return Column(
            children: [
              _FilterBar(
                controller: _searchController,
                onQueryChanged: (v) => setState(() => _query = v),
                episodeIds: episodeIds,
                selectedEpisode: _episodeFilter,
                onEpisodeChanged: (v) =>
                    setState(() => _episodeFilter = v),
              ),
              Expanded(
                child: filtered.isEmpty
                    ? _EmptyView(hasQuery: _query.isNotEmpty)
                    : RefreshIndicator(
                        onRefresh: () => ref
                            .read(notebookControllerProvider.notifier)
                            .refresh(),
                        child: ListView.separated(
                          physics: const AlwaysScrollableScrollPhysics(),
                          itemCount: filtered.length,
                          separatorBuilder: (_, _) =>
                              const Divider(height: 1),
                          itemBuilder: (context, index) {
                            final e = filtered[index];
                            return NotebookEntryTile(
                              entry: e,
                              onTap: () => _openDetail(e),
                              onDelete: () => _deleteEntry(e),
                            );
                          },
                        ),
                      ),
              ),
            ],
          );
        },
      ),
    );
  }

  static List<String> _episodeIdsFrom(List<NotebookEntry> entries) {
    final set = <String>{};
    for (final e in entries) {
      final id = e.episodeId;
      if (id != null && id.isNotEmpty) set.add(id);
    }
    final list = set.toList()..sort();
    return list;
  }

  static String _friendlyMessage(Object error) {
    if (error is NetworkException) {
      return '네트워크 오류: ${error.message}';
    }
    if (error is AppException) {
      return error.message;
    }
    return '단어장을 불러오지 못했습니다.';
  }
}

class _FilterBar extends StatelessWidget {
  const _FilterBar({
    required this.controller,
    required this.onQueryChanged,
    required this.episodeIds,
    required this.selectedEpisode,
    required this.onEpisodeChanged,
  });

  final TextEditingController controller;
  final ValueChanged<String> onQueryChanged;
  final List<String> episodeIds;
  final String? selectedEpisode;
  final ValueChanged<String?> onEpisodeChanged;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(12, 8, 12, 8),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              key: const Key('notebook-search-field'),
              controller: controller,
              onChanged: onQueryChanged,
              decoration: const InputDecoration(
                prefixIcon: Icon(Icons.search_rounded),
                hintText: '단어·뜻·메모 검색',
                isDense: true,
                border: OutlineInputBorder(),
              ),
            ),
          ),
          const SizedBox(width: 8),
          if (episodeIds.isNotEmpty)
            _EpisodeFilter(
              episodeIds: episodeIds,
              selected: selectedEpisode,
              onChanged: onEpisodeChanged,
            ),
        ],
      ),
    );
  }
}

class _EpisodeFilter extends StatelessWidget {
  const _EpisodeFilter({
    required this.episodeIds,
    required this.selected,
    required this.onChanged,
  });

  final List<String> episodeIds;
  final String? selected;
  final ValueChanged<String?> onChanged;

  @override
  Widget build(BuildContext context) {
    return ConstrainedBox(
      constraints: const BoxConstraints(maxWidth: 140),
      child: DropdownButtonFormField<String?>(
        key: const Key('notebook-episode-filter'),
        initialValue: selected,
        isExpanded: true,
        decoration: const InputDecoration(
          isDense: true,
          border: OutlineInputBorder(),
        ),
        hint: const Text('에피소드'),
        items: [
          const DropdownMenuItem<String?>(
            value: null,
            child: Text('전체'),
          ),
          ...episodeIds.map(
            (id) => DropdownMenuItem<String?>(
              value: id,
              child: Text(id, overflow: TextOverflow.ellipsis),
            ),
          ),
        ],
        onChanged: onChanged,
      ),
    );
  }
}

class _EmptyView extends StatelessWidget {
  const _EmptyView({required this.hasQuery});

  final bool hasQuery;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return ListView(
      physics: const AlwaysScrollableScrollPhysics(),
      children: [
        const SizedBox(height: 100),
        Center(
          child: Column(
            children: [
              Icon(Icons.menu_book_outlined,
                  size: 56, color: scheme.onSurfaceVariant),
              const SizedBox(height: 12),
              Text(
                hasQuery ? '일치하는 단어가 없습니다' : '아직 저장한 단어가 없습니다',
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: 4),
              Text(
                hasQuery ? '다른 검색어를 시도해 보세요' : '우측 하단 + 로 추가해 보세요',
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: scheme.onSurfaceVariant,
                    ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class _ErrorView extends StatelessWidget {
  const _ErrorView({required this.message, required this.onRetry});

  final String message;
  final Future<void> Function() onRetry;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.error_outline, size: 48),
            const SizedBox(height: 12),
            Text(message,
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodyMedium),
            const SizedBox(height: 16),
            FilledButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh_rounded),
              label: const Text('다시 시도'),
            ),
          ],
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Providers + controller
// ---------------------------------------------------------------------------

final listNotebookUseCaseProvider =
    FutureProvider<ListNotebook>((ref) async {
  final repo = await ref.watch(notebookRepositoryProvider.future);
  return ListNotebook(repo);
});

final addNotebookEntryUseCaseProvider =
    FutureProvider<AddNotebookEntry>((ref) async {
  final repo = await ref.watch(notebookRepositoryProvider.future);
  return AddNotebookEntry(repo);
});

final updateNotebookEntryUseCaseProvider =
    FutureProvider<UpdateNotebookEntry>((ref) async {
  final repo = await ref.watch(notebookRepositoryProvider.future);
  return UpdateNotebookEntry(repo);
});

final deleteNotebookEntryUseCaseProvider =
    FutureProvider<DeleteNotebookEntry>((ref) async {
  final repo = await ref.watch(notebookRepositoryProvider.future);
  return DeleteNotebookEntry(repo);
});

class NotebookController
    extends AutoDisposeAsyncNotifier<List<NotebookEntry>> {
  @override
  Future<List<NotebookEntry>> build() async {
    return _fetch();
  }

  Future<List<NotebookEntry>> _fetch() async {
    final useCase = await ref.read(listNotebookUseCaseProvider.future);
    final result = await useCase();
    return result.when(
      success: (entries) => entries,
      failure: (error) => throw error,
    );
  }

  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(_fetch);
  }

  Future<bool> add(NotebookAddPayload payload) async {
    final useCase = await ref.read(addNotebookEntryUseCaseProvider.future);
    final result = await useCase(
      word: payload.word,
      context: payload.context,
      meaning: payload.meaning,
      note: payload.note,
    );
    final ok = result.isSuccess;
    if (ok) {
      state = await AsyncValue.guard(_fetch);
    }
    return ok;
  }

  Future<bool> updateEntry({
    required String id,
    String? meaning,
    String? note,
  }) async {
    final useCase =
        await ref.read(updateNotebookEntryUseCaseProvider.future);
    final result = await useCase(id: id, meaning: meaning, note: note);
    final ok = result.isSuccess;
    if (ok) {
      state = await AsyncValue.guard(_fetch);
    }
    return ok;
  }

  Future<bool> remove(String id) async {
    final useCase =
        await ref.read(deleteNotebookEntryUseCaseProvider.future);
    final result = await useCase(id);
    final ok = result.isSuccess;
    if (ok) {
      state = await AsyncValue.guard(_fetch);
    }
    return ok;
  }
}

final notebookControllerProvider = AutoDisposeAsyncNotifierProvider<
    NotebookController, List<NotebookEntry>>(
  NotebookController.new,
);
