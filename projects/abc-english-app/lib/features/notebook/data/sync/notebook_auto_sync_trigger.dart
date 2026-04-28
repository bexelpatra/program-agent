import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/connectivity/connectivity_service.dart';
import '../../../../core/logging/app_logger.dart';
import '../repositories/notebook_repository_impl.dart';
import 'notebook_sync_service.dart';

/// Automatically drains the notebook offline queue when connectivity
/// transitions from offline → online. Mounting the
/// [notebookAutoSyncTriggerProvider] subscribes once and keeps the
/// subscription alive for the life of the [ProviderScope] (we call
/// `keepAlive` so the listener isn't torn down when the notebook screen
/// is popped).
///
/// Failures during sync are logged and swallowed — a future transition
/// will try again. This matches the "best-effort" policy in
/// architecture.md §오프라인 전략.
class NotebookAutoSyncTrigger {
  NotebookAutoSyncTrigger({
    required ConnectivityService connectivity,
    required Future<NotebookSyncService> Function() syncServiceResolver,
  })  : _connectivity = connectivity,
        _resolver = syncServiceResolver;

  final ConnectivityService _connectivity;
  final Future<NotebookSyncService> Function() _resolver;

  StreamSubscription<bool>? _sub;
  bool? _lastOnline;

  /// Start listening. Idempotent — a second call is a no-op.
  void start() {
    if (_sub != null) return;
    _sub = _connectivity.onlineStream.listen(_handle);
  }

  /// Release the subscription. Safe to call more than once.
  Future<void> stop() async {
    await _sub?.cancel();
    _sub = null;
    _lastOnline = null;
  }

  Future<void> _handle(bool online) async {
    final previous = _lastOnline;
    _lastOnline = online;

    // Only drain on offline → online transitions. The initial subscription
    // emit (previous == null) counts as an online transition if the app
    // came up connected; otherwise we wait.
    final transitionedOnline =
        online && (previous == false || previous == null);
    if (!transitionedOnline) return;

    try {
      final service = await _resolver();
      final outcome = await service.sync();
      AppLogger.instance.info(
        'notebook.auto_sync.outcome',
        context: {'type': outcome.runtimeType.toString()},
      );
    } catch (error, stack) {
      AppLogger.instance.warning(
        'notebook.auto_sync.error',
        error: error,
        stackTrace: stack,
      );
    }
  }
}

/// Eager singleton so the trigger is mounted as soon as the scope resolves
/// it. Consumers mount it once via `ref.watch(notebookAutoSyncTriggerProvider)`
/// from the app root; the Provider's `keepAlive` semantics (default for
/// non-auto-dispose providers) keep the subscription alive for the scope.
final notebookAutoSyncTriggerProvider =
    Provider<NotebookAutoSyncTrigger>((ref) {
  final trigger = NotebookAutoSyncTrigger(
    connectivity: ref.watch(connectivityServiceProvider),
    syncServiceResolver: () => ref.read(notebookSyncServiceProvider.future),
  );
  trigger.start();
  ref.onDispose(trigger.stop);
  return trigger;
});
