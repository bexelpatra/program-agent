import 'dart:ffi';
import 'dart:io' show File, Platform;

import 'package:abc_english_app/core/storage/app_database.dart';
import 'package:abc_english_app/core/storage/migrations.dart';
import 'package:drift/drift.dart' hide isNull;
import 'package:drift/native.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:sqlite3/open.dart';

/// Test-only loader. Desktop Linux CI images ship `libsqlite3.so.0` but
/// not the unversioned `libsqlite3.so` that `package:sqlite3` looks for,
/// so we point it at the versioned file explicitly. Harmless on macOS /
/// Windows — the override is only applied on Linux.
void _installLinuxSqliteLoader() {
  if (!Platform.isLinux) return;
  const candidates = [
    '/lib/x86_64-linux-gnu/libsqlite3.so.0',
    '/usr/lib/x86_64-linux-gnu/libsqlite3.so.0',
    '/lib/aarch64-linux-gnu/libsqlite3.so.0',
    '/usr/lib/aarch64-linux-gnu/libsqlite3.so.0',
  ];
  for (final path in candidates) {
    if (File(path).existsSync()) {
      open.overrideFor(OperatingSystem.linux, () => DynamicLibrary.open(path));
      return;
    }
  }
  // Otherwise fall back to default resolver — will error with a clearer
  // message than our override.
}

AppDatabase _memoryDb() {
  return AppDatabase(NativeDatabase.memory());
}

void main() {
  setUpAll(_installLinuxSqliteLoader);

  group('AppMigrations', () {
    test('schemaVersion == 2 (v2 added notebook deletedAt tombstone)', () {
      expect(AppMigrations.schemaVersion, 2);
    });

    test('AppDatabase exposes the same schemaVersion', () async {
      final db = _memoryDb();
      try {
        expect(db.schemaVersion, 2);
      } finally {
        await db.close();
      }
    });

    test('onCreate builds every shipped table', () async {
      final db = _memoryDb();
      try {
        // Touching any generated dao triggers onCreate via createAll().
        await db.customSelect('SELECT 1').get();

        final tables = await db
            .customSelect(
              "SELECT name FROM sqlite_master "
              "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' "
              "ORDER BY name",
            )
            .map((r) => r.read<String>('name'))
            .get();

        expect(
          tables,
          containsAll(['episodes', 'notebook_entries', 'sentences']),
        );
      } finally {
        await db.close();
      }
    });
  });

  group('Episodes round-trip', () {
    late AppDatabase db;

    setUp(() {
      db = _memoryDb();
    });

    tearDown(() async {
      await db.close();
    });

    test('insert + select a row', () async {
      final publishedAt = DateTime.utc(2026, 4, 1, 12);
      final lastModified = DateTime.utc(2026, 4, 2, 12);

      await db.into(db.episodes).insert(
            EpisodesCompanion.insert(
              id: 'ep-1',
              title: 'Morning News',
              publishedDate: publishedAt,
              durationMs: 360000,
              lastModified: lastModified,
              avgWer: const Value(0.12),
            ),
          );

      final rows = await db.select(db.episodes).get();
      expect(rows, hasLength(1));
      expect(rows.single.id, 'ep-1');
      expect(rows.single.title, 'Morning News');
      expect(rows.single.durationMs, 360000);
      expect(rows.single.avgWer, closeTo(0.12, 1e-9));
    });
  });

  group('Sentences round-trip', () {
    late AppDatabase db;

    setUp(() {
      db = _memoryDb();
    });

    tearDown(() async {
      await db.close();
    });

    test('Dart getters (sentenceIndex/body) work via companion', () async {
      // Parent episode (FK).
      await db.into(db.episodes).insert(
            EpisodesCompanion.insert(
              id: 'ep-1',
              title: 't',
              publishedDate: DateTime.utc(2026, 1, 1),
              durationMs: 10000,
              lastModified: DateTime.utc(2026, 1, 1),
            ),
          );

      await db.into(db.sentences).insert(
            SentencesCompanion.insert(
              episodeId: 'ep-1',
              sentenceIndex: 0,
              body: 'Good morning.',
              startMs: 0,
              endMs: 1500,
            ),
          );

      final rows = await db.select(db.sentences).get();
      expect(rows, hasLength(1));
      expect(rows.single.episodeId, 'ep-1');
      expect(rows.single.sentenceIndex, 0);
      expect(rows.single.body, 'Good morning.');
      expect(rows.single.startMs, 0);
      expect(rows.single.endMs, 1500);
    });

    test(
      'on-disk column names are `index` and `text` (not sentenceIndex/body)',
      () async {
        // Seed parent + child.
        await db.into(db.episodes).insert(
              EpisodesCompanion.insert(
                id: 'ep-1',
                title: 't',
                publishedDate: DateTime.utc(2026, 1, 1),
                durationMs: 10000,
                lastModified: DateTime.utc(2026, 1, 1),
              ),
            );
        await db.into(db.sentences).insert(
              SentencesCompanion.insert(
                episodeId: 'ep-1',
                sentenceIndex: 7,
                body: 'hello world',
                startMs: 0,
                endMs: 1000,
              ),
            );

        // Raw query using the on-disk column names.
        final raw = await db
            .customSelect(
              'SELECT episode_id, "index", "text" FROM sentences '
              'WHERE episode_id = ?1',
              variables: [Variable<String>('ep-1')],
            )
            .get();

        expect(raw, hasLength(1));
        expect(raw.single.read<String>('episode_id'), 'ep-1');
        expect(raw.single.read<int>('index'), 7);
        expect(raw.single.read<String>('text'), 'hello world');

        // And a column named `body` must *not* exist.
        final badColumn = db.customSelect(
          'SELECT body FROM sentences',
        );
        await expectLater(badColumn.get(), throwsA(anything));
      },
    );
  });

  group('NotebookEntries round-trip', () {
    late AppDatabase db;

    setUp(() {
      db = _memoryDb();
    });

    tearDown(() async {
      await db.close();
    });

    test('insert + select with nullables preserved', () async {
      final now = DateTime.utc(2026, 4, 5);
      await db.into(db.notebookEntries).insert(
            NotebookEntriesCompanion.insert(
              id: 'nb-1',
              word: 'serendipity',
              context: 'happy accident',
              createdAt: now,
              lastModified: now,
            ),
          );

      final rows = await db.select(db.notebookEntries).get();
      expect(rows, hasLength(1));
      expect(rows.single.id, 'nb-1');
      expect(rows.single.word, 'serendipity');
      expect(rows.single.meaning, isNull);
      expect(rows.single.syncedAt, isNull);
    });
  });
}
