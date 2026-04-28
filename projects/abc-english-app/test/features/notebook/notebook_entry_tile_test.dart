import 'package:abc_english_app/features/notebook/domain/entities/notebook_entry.dart';
import 'package:abc_english_app/features/notebook/domain/entities/sync_status.dart';
import 'package:abc_english_app/features/notebook/presentation/widgets/notebook_entry_tile.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

NotebookEntry _entry({
  String id = 'nb-1',
  String word = 'albeit',
  SyncStatus status = SyncStatus.synced,
  String? meaning,
  String? note,
  String? episodeId,
  int? sentenceIndex,
}) {
  final now = DateTime.utc(2026, 4, 5);
  return NotebookEntry(
    id: id,
    word: word,
    context: 'c',
    createdAt: now,
    lastModified: now,
    syncStatus: status,
    meaning: meaning,
    note: note,
    episodeId: episodeId,
    sentenceIndex: sentenceIndex,
  );
}

Widget _wrap(Widget w) => MaterialApp(home: Scaffold(body: ListView(children: [w])));

void main() {
  testWidgets('renders word + meaning when provided', (tester) async {
    await tester.pumpWidget(_wrap(NotebookEntryTile(
      entry: _entry(meaning: '비록 ~일지라도'),
      onTap: () {},
      onDelete: () async {},
    )));
    expect(find.text('albeit'), findsOneWidget);
    expect(find.text('비록 ~일지라도'), findsOneWidget);
  });

  testWidgets('shows placeholder when meaning is null', (tester) async {
    await tester.pumpWidget(_wrap(NotebookEntryTile(
      entry: _entry(),
      onTap: () {},
      onDelete: () async {},
    )));
    expect(find.text('뜻 미입력'), findsOneWidget);
  });

  testWidgets('sync indicator appears only for pending statuses',
      (tester) async {
    await tester.pumpWidget(_wrap(NotebookEntryTile(
      entry: _entry(status: SyncStatus.pendingUpsert),
      onTap: () {},
      onDelete: () async {},
    )));
    expect(find.byIcon(Icons.schedule_rounded), findsOneWidget);
  });

  testWidgets('sync indicator hidden when synced', (tester) async {
    await tester.pumpWidget(_wrap(NotebookEntryTile(
      entry: _entry(status: SyncStatus.synced),
      onTap: () {},
      onDelete: () async {},
    )));
    expect(find.byIcon(Icons.schedule_rounded), findsNothing);
  });

  testWidgets('episode source label renders with sentence index', (tester) async {
    await tester.pumpWidget(_wrap(NotebookEntryTile(
      entry: _entry(episodeId: 'ep-1', sentenceIndex: 4),
      onTap: () {},
      onDelete: () async {},
    )));
    // sentenceIndex is rendered as (index + 1).
    expect(find.textContaining('출처: ep-1 · 문장 5'), findsOneWidget);
  });

  testWidgets('tap invokes onTap', (tester) async {
    var taps = 0;
    await tester.pumpWidget(_wrap(NotebookEntryTile(
      entry: _entry(),
      onTap: () => taps++,
      onDelete: () async {},
    )));
    await tester.tap(find.byType(ListTile));
    await tester.pumpAndSettle();
    expect(taps, 1);
  });
}
