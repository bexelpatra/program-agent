import 'dart:async';

import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Wrapper over `connectivity_plus` that exposes a boolean online/offline
/// view. Any connectivity result other than [ConnectivityResult.none] is
/// treated as "online" — downstream code can make its own judgement about
/// reachability once it tries to actually hit the server.
class ConnectivityService {
  ConnectivityService({Connectivity? connectivity})
      : _connectivity = connectivity ?? Connectivity();

  final Connectivity _connectivity;

  /// Current online state (one-shot).
  Future<bool> isOnline() async {
    final results = await _connectivity.checkConnectivity();
    return _isOnlineFromResults(results);
  }

  /// Emits only on *transitions* (online→offline or offline→online). The
  /// caller receives the initial value on subscription and then nothing
  /// until the state actually changes.
  Stream<bool> get onlineStream async* {
    bool? last;
    final initial = await isOnline();
    last = initial;
    yield initial;

    await for (final results in _connectivity.onConnectivityChanged) {
      final current = _isOnlineFromResults(results);
      if (current != last) {
        last = current;
        yield current;
      }
    }
  }

  static bool _isOnlineFromResults(List<ConnectivityResult> results) {
    if (results.isEmpty) {
      return false;
    }
    return results.any((r) => r != ConnectivityResult.none);
  }
}

/// Shared singleton provider.
final connectivityServiceProvider = Provider<ConnectivityService>((ref) {
  return ConnectivityService();
});
