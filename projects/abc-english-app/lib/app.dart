import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/routing/app_router.dart';
import 'core/theme/app_theme.dart';
import 'features/notebook/data/sync/notebook_auto_sync_trigger.dart';

/// Root widget. Hosts `MaterialApp.router`, the global theme, and mounts
/// background services (offline queue drain, etc.) on first frame.
class AbcApp extends ConsumerWidget {
  const AbcApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Mount the auto-sync trigger eagerly. The Provider starts the
    // connectivity subscription as a side effect of first read and keeps
    // itself alive via `ref.onDispose` pairing with the enclosing scope.
    ref.watch(notebookAutoSyncTriggerProvider);

    return MaterialApp.router(
      title: 'ABC English',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light(),
      darkTheme: AppTheme.dark(),
      themeMode: ThemeMode.system,
      routerConfig: appRouter,
    );
  }
}
