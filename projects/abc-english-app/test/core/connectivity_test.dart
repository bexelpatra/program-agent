import 'dart:async';

import 'package:abc_english_app/core/connectivity/connectivity_service.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class _MockConnectivity extends Mock implements Connectivity {}

void main() {
  group('ConnectivityService.isOnline', () {
    late _MockConnectivity connectivity;
    late ConnectivityService service;

    setUp(() {
      connectivity = _MockConnectivity();
      service = ConnectivityService(connectivity: connectivity);
    });

    test('wifi → online', () async {
      when(() => connectivity.checkConnectivity()).thenAnswer(
        (_) async => [ConnectivityResult.wifi],
      );
      expect(await service.isOnline(), isTrue);
    });

    test('mobile → online', () async {
      when(() => connectivity.checkConnectivity()).thenAnswer(
        (_) async => [ConnectivityResult.mobile],
      );
      expect(await service.isOnline(), isTrue);
    });

    test('only ConnectivityResult.none → offline', () async {
      when(() => connectivity.checkConnectivity()).thenAnswer(
        (_) async => [ConnectivityResult.none],
      );
      expect(await service.isOnline(), isFalse);
    });

    test('empty list → offline', () async {
      when(() => connectivity.checkConnectivity()).thenAnswer(
        (_) async => <ConnectivityResult>[],
      );
      expect(await service.isOnline(), isFalse);
    });
  });

  group('ConnectivityService.onlineStream', () {
    late _MockConnectivity connectivity;
    late StreamController<List<ConnectivityResult>> events;

    setUp(() {
      connectivity = _MockConnectivity();
      // Use a single-subscription controller (matches the `await for` pattern
      // inside `onlineStream`). The async-generator cancellation of a
      // broadcast subscription deadlocks under `flutter test`.
      events = StreamController<List<ConnectivityResult>>();
      when(() => connectivity.onConnectivityChanged)
          .thenAnswer((_) => events.stream);
    });

    test(
      'emits only on online/offline transitions '
      '(wifi→mobile same online=true dedup; wifi→none→wifi flips)',
      () async {
        // Initial value: wifi → online=true.
        when(() => connectivity.checkConnectivity())
            .thenAnswer((_) async => [ConnectivityResult.wifi]);

        final service = ConnectivityService(connectivity: connectivity);
        final collected = <bool>[];
        final done = Completer<void>();
        final sub = service.onlineStream.listen(
          collected.add,
          onDone: done.complete,
        );

        // Let the initial yield happen.
        await Future<void>.delayed(Duration.zero);

        // wifi → mobile: still online. Must NOT re-emit.
        events.add([ConnectivityResult.mobile]);
        await Future<void>.delayed(Duration.zero);

        // mobile → none: transition to offline. Must emit false.
        events.add([ConnectivityResult.none]);
        await Future<void>.delayed(Duration.zero);

        // none → wifi: transition back to online. Must emit true.
        events.add([ConnectivityResult.wifi]);
        await Future<void>.delayed(Duration.zero);

        // Redundant wifi → wifi: must NOT re-emit.
        events.add([ConnectivityResult.wifi]);
        await Future<void>.delayed(Duration.zero);

        // End the upstream so the async generator drains and completes.
        await events.close();
        await done.future.timeout(const Duration(seconds: 2));
        await sub.cancel();

        expect(
          collected,
          [true, false, true],
          reason: 'only boolean transitions should be emitted',
        );
      },
    );

    test('initial state is emitted as the first value', () async {
      when(() => connectivity.checkConnectivity())
          .thenAnswer((_) async => [ConnectivityResult.none]);

      final service = ConnectivityService(connectivity: connectivity);
      final collected = <bool>[];
      final done = Completer<void>();
      final sub = service.onlineStream.listen(
        collected.add,
        onDone: done.complete,
      );

      await Future<void>.delayed(Duration.zero);
      expect(collected, [false]);

      await events.close();
      await done.future.timeout(const Duration(seconds: 2));
      await sub.cancel();
    });
  });
}
