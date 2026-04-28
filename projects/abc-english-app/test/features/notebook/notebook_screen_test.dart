import 'package:abc_english_app/core/errors/result.dart';
import 'package:abc_english_app/features/notebook/data/repositories/notebook_repository_impl.dart';
import 'package:abc_english_app/features/notebook/domain/entities/notebook_entry.dart';
import 'package:abc_english_app/features/notebook/domain/entities/sync_status.dart';
import 'package:abc_english_app/features/notebook/domain/repositories/notebook_repository.dart';
import 'package:abc_english_app/features/notebook/presentation/notebook_screen.dart';
import 'package:abc_english_app/features/notebook/presentation/widgets/notebook_add_dialog.dart';
import 'package:abc_english_app/features/notebook/presentation/widgets/notebook_entry_tile.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

/// In-memory repository driven by the widget tests.
class _FakeRepo implements NotebookRepository {
  _FakeRepo(this._initial);
  final List<NotebookEntry> _initial;

  @override
  Future<Result<List<NotebookEntry>>> list({DateTime? sinceModified}) async {
    return Success(List.unmodifiable(_initial));
  }

  @override
  Future<Result<NotebookEntry>> add({
    required String word,
    required String context,
    String? episodeId,
    int? sentenceIndex,
    String? meaning,
    String? note,
  }) async {
    final now = DateTime.utc(2026, 4, 5);
    final entry = NotebookEntry(
      id: 'added-${_initial.length}',
      word: word,
      context: context,
      createdAt: now,
      lastModified: now,
      syncStatus: SyncStatus.synced,
      meaning: meaning,
      note: note,
    );
    _initial.add(entry);
    return Success(entry);
  }

  @override
  Future<Result<NotebookEntry>> update({
    required String id,
    String? word,
    String? context,
    String? episodeId,
    int? sentenceIndex,
    String? meaning,
    String? note,
  }) async {
    throw UnimplementedError();
  }

  @override
  Future<Result<void>> remove(String id) async => const Success(null);
}

NotebookEntry _entry({
  String id = 'nb-1',
  String word = 'albeit',
  String? meaning,
}) {
  final now = DateTime.utc(2026, 4, 5);
  return NotebookEntry(
    id: id,
    word: word,
    context: 'c',
    createdAt: now,
    lastModified: now,
    syncStatus: SyncStatus.synced,
    meaning: meaning,
  );
}

Widget _host(ProviderContainer c) {
  return UncontrolledProviderScope(
    container: c,
    child: const MaterialApp(home: NotebookScreen()),
  );
}

ProviderContainer _container(_FakeRepo repo) {
  return ProviderContainer(
    overrides: [
      notebookRepositoryProvider.overrideWith((ref) async => repo),
    ],
  );
}

void main() {
  testWidgets('renders the entries list + FAB', (tester) async {
    final repo = _FakeRepo([
      _entry(id: 'nb-1', word: 'albeit', meaning: '비록'),
      _entry(id: 'nb-2', word: 'serendipity', meaning: '행운의 발견'),
    ]);
    final c = _container(repo);
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();

    expect(find.byType(NotebookEntryTile), findsNWidgets(2));
    expect(find.text('albeit'), findsOneWidget);
    expect(find.text('serendipity'), findsOneWidget);
    expect(find.byKey(const Key('notebook-add-fab')), findsOneWidget);
  });

  testWidgets('FAB tap opens the add dialog', (tester) async {
    final repo = _FakeRepo(<NotebookEntry>[]);
    final c = _container(repo);
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();

    await tester.tap(find.byKey(const Key('notebook-add-fab')));
    await tester.pumpAndSettle();
    expect(find.byType(NotebookAddDialog), findsOneWidget);
    expect(find.byKey(const Key('notebook-add-word')), findsOneWidget);
  });

  testWidgets('empty list shows the empty-state copy', (tester) async {
    final repo = _FakeRepo(<NotebookEntry>[]);
    final c = _container(repo);
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();
    expect(find.text('아직 저장한 단어가 없습니다'), findsOneWidget);
  });
}
