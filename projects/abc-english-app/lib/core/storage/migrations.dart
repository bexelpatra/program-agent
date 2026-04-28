import 'package:drift/drift.dart';

import 'app_database.dart';

/// Centralised migration policy.
///
/// Bump [schemaVersion] for each new shipping schema. Add an `if (from < N)`
/// block inside [onUpgrade] to describe the v(N-1) → vN transition.
/// Keeping the logic here (rather than inline in [AppDatabase]) lets us grow
/// the migration tree without bloating the schema file.
class AppMigrations {
  const AppMigrations._();

  /// Current shipping schema version. Increment monotonically.
  static const int schemaVersion = 2;

  static MigrationStrategy strategy(GeneratedDatabase db) {
    return MigrationStrategy(
      onCreate: (m) async {
        await m.createAll();
      },
      onUpgrade: (m, from, to) async {
        // v1 → v2: notebook offline-delete tombstone column. Existing rows
        // stay non-deleted (NULL), matching the `not yet deleted` sentinel
        // used throughout the sync pipeline.
        if (from < 2) {
          final db0 = db as AppDatabase;
          await m.addColumn(db0.notebookEntries, db0.notebookEntries.deletedAt);
        }
        // Future migrations go here, e.g.:
        //
        // if (from < 3) {
        //   // 여기에 추가
        // }
      },
    );
  }
}
