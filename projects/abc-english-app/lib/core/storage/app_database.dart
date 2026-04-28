import 'dart:io';

import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';

import 'migrations.dart';

part 'app_database.g.dart';

/// Episodes metadata. One row per podcast episode.
///
/// [id] comes from the upstream ABC feed and is the stable primary key.
/// [audioLocalPath] is non-null only if the MP3 has been downloaded for
/// offline playback.
@DataClassName('EpisodeRow')
class Episodes extends Table {
  TextColumn get id => text()();
  TextColumn get title => text()();
  DateTimeColumn get publishedDate => dateTime()();
  IntColumn get durationMs => integer()();
  RealColumn get avgWer => real().nullable()();
  DateTimeColumn get lastModified => dateTime()();
  DateTimeColumn get downloadedAt => dateTime().nullable()();
  TextColumn get audioLocalPath => text().nullable()();

  @override
  Set<Column> get primaryKey => {id};
}

/// Sentences within an episode. Composite PK `(episodeId, sentenceIndex)`
/// means each episode's sentence set is dense and ordered.
///
/// Dart-side getters use `sentenceIndex` / `body` to avoid colliding with
/// [Table.text] and the reserved `index` identifier; the on-disk column
/// names stay `index` and `text` via `.named(...)`.
@DataClassName('SentenceRow')
class Sentences extends Table {
  TextColumn get episodeId => text().references(Episodes, #id)();
  IntColumn get sentenceIndex => integer().named('index')();
  TextColumn get body => text().named('text')();
  IntColumn get startMs => integer()();
  IntColumn get endMs => integer()();
  RealColumn get wer => real().nullable()();
  TextColumn get difficulty => text().nullable()();

  @override
  Set<Column> get primaryKey => {episodeId, sentenceIndex};
}

/// Notebook entries (user-added vocabulary).
///
/// [episodeId] / [sentenceIndex] record provenance if the word was added
/// from a script tap; both are nullable to allow free-form entries.
/// [meaning] may be null when added offline — filled in on reconnect via
/// the "fill-later" strategy (see architecture.md §오프라인 전략).
/// [syncedAt] is null until the row has been POSTed to the server.
/// [deletedAt] is the offline tombstone: non-null rows are hidden from the
/// UI list and wait for the sync engine to propagate a DELETE to the
/// server, after which they are hard-deleted locally.
@DataClassName('NotebookEntryRow')
class NotebookEntries extends Table {
  TextColumn get id => text()();
  TextColumn get word => text()();
  TextColumn get context => text()();
  TextColumn get episodeId => text().nullable()();
  IntColumn get sentenceIndex => integer().nullable()();
  TextColumn get meaning => text().nullable()();
  TextColumn get note => text().nullable()();
  DateTimeColumn get createdAt => dateTime()();
  DateTimeColumn get lastModified => dateTime()();
  DateTimeColumn get syncedAt => dateTime().nullable()();
  DateTimeColumn get deletedAt => dateTime().nullable()();

  @override
  Set<Column> get primaryKey => {id};
}

/// Root database. DAOs intentionally deferred — feature tasks add them as
/// needed (see architecture.md §앱 아키텍처).
@DriftDatabase(tables: [Episodes, Sentences, NotebookEntries])
class AppDatabase extends _$AppDatabase {
  AppDatabase(super.executor);

  @override
  int get schemaVersion => AppMigrations.schemaVersion;

  @override
  MigrationStrategy get migration => AppMigrations.strategy(this);
}

/// Builds a background-isolate [NativeDatabase] under the app's documents
/// directory. Running drift on a background connection keeps SQL work off
/// the UI isolate.
Future<AppDatabase> _openAppDatabase() async {
  final dir = await getApplicationDocumentsDirectory();
  final file = File(p.join(dir.path, 'abc_english.db'));
  final executor = NativeDatabase.createBackgroundConnection(file);
  return AppDatabase(executor);
}

/// Async Riverpod provider. Consumers `.watch` and receive the DB once the
/// path/executor has been resolved.
///
/// Override in tests with an in-memory `NativeDatabase.memory()` executor.
final appDatabaseProvider = FutureProvider<AppDatabase>((ref) async {
  final db = await _openAppDatabase();
  ref.onDispose(() async {
    await db.close();
  });
  return db;
});
