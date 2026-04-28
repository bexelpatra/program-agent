import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';

import 'package:abc_english_app/core/config/app_config.dart';
import 'package:abc_english_app/core/errors/app_exception.dart';
import 'package:abc_english_app/core/network/dio_client.dart';
import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';

/// A scripted [HttpClientAdapter] — each call to [fetch] pops the next
/// planned response. Captures every observed [RequestOptions] so the test
/// can assert on headers / attempt counts.
class _ScriptedAdapter implements HttpClientAdapter {
  _ScriptedAdapter(this._plan);

  final List<_Planned> _plan;
  final List<RequestOptions> requests = <RequestOptions>[];
  int _idx = 0;

  int get callCount => requests.length;

  @override
  Future<ResponseBody> fetch(
    RequestOptions options,
    Stream<Uint8List>? requestStream,
    Future<dynamic>? cancelFuture,
  ) async {
    requests.add(options);
    if (_idx >= _plan.length) {
      throw StateError(
        'Scripted adapter exhausted after ${_plan.length} responses '
        '(request #${_idx + 1})',
      );
    }
    final step = _plan[_idx++];
    if (step is _PlannedThrowFromOptions) {
      step._observedOptions = options;
    }
    return step.execute();
  }

  @override
  void close({bool force = false}) {}
}

sealed class _Planned {
  Future<ResponseBody> execute();
}

class _PlannedStatus extends _Planned {
  _PlannedStatus(this.status, {this.body = const <String, dynamic>{}});
  final int status;
  final Map<String, dynamic> body;

  @override
  Future<ResponseBody> execute() async {
    final bytes = utf8.encode(jsonEncode(body));
    return ResponseBody.fromBytes(
      bytes,
      status,
      headers: const {
        'content-type': ['application/json'],
      },
    );
  }
}

class _PlannedThrowFromOptions extends _Planned {
  _PlannedThrowFromOptions(this.buildError);
  final DioException Function(RequestOptions) buildError;

  RequestOptions? _observedOptions;

  @override
  Future<ResponseBody> execute() async {
    final opts = _observedOptions!;
    throw buildError(opts);
  }
}

AppConfig _fakeConfig() {
  return AppConfig(
    apiBaseUrl: 'https://example.test',
    apiToken: 'test-token-xyz',
    env: AppEnv.dev,
  );
}

/// Convenience wrapper so the test can read the inner AppException out of the
/// outer DioException thrown by the mapping interceptor.
Object _unwrap(DioException e) => e.error ?? e;

void main() {
  group('DioClient — auth interceptor', () {
    test('adds Authorization: Bearer <token> to every request', () async {
      final adapter = _ScriptedAdapter([_PlannedStatus(200)]);
      final client = DioClient(_fakeConfig());
      client.raw.httpClientAdapter = adapter;

      await client.raw.get<dynamic>('/episodes');

      expect(adapter.callCount, 1);
      expect(
        adapter.requests.single.headers['Authorization'],
        'Bearer test-token-xyz',
      );
    });
  });

  group('DioClient — error mapping', () {
    test('401 → UnauthorizedException', () async {
      final adapter = _ScriptedAdapter([_PlannedStatus(401)]);
      final client = DioClient(_fakeConfig());
      client.raw.httpClientAdapter = adapter;

      try {
        await client.raw.get<dynamic>('/episodes');
        fail('expected DioException');
      } on DioException catch (e) {
        expect(_unwrap(e), isA<UnauthorizedException>());
      }
      expect(adapter.callCount, 1, reason: '4xx → no retry');
    });

    test('403 → UnauthorizedException', () async {
      final adapter = _ScriptedAdapter([_PlannedStatus(403)]);
      final client = DioClient(_fakeConfig());
      client.raw.httpClientAdapter = adapter;

      try {
        await client.raw.get<dynamic>('/episodes');
        fail('expected DioException');
      } on DioException catch (e) {
        expect(_unwrap(e), isA<UnauthorizedException>());
      }
    });

    test('404 → NotFoundException', () async {
      final adapter = _ScriptedAdapter([_PlannedStatus(404)]);
      final client = DioClient(_fakeConfig());
      client.raw.httpClientAdapter = adapter;

      try {
        await client.raw.get<dynamic>('/missing');
        fail('expected DioException');
      } on DioException catch (e) {
        expect(_unwrap(e), isA<NotFoundException>());
      }
      expect(adapter.callCount, 1, reason: '4xx → no retry');
    });

    test('400 → immediate failure, no retry', () async {
      final adapter = _ScriptedAdapter([_PlannedStatus(400)]);
      final client = DioClient(_fakeConfig());
      client.raw.httpClientAdapter = adapter;

      try {
        await client.raw.get<dynamic>('/bad');
        fail('expected DioException');
      } on DioException catch (_) {
        // mapped to UnknownException by current impl — what we care about
        // here is the lack of retries.
      }
      expect(adapter.callCount, 1, reason: '4xx → no retry');
    });

    test('422 → immediate failure, no retry', () async {
      final adapter = _ScriptedAdapter([_PlannedStatus(422)]);
      final client = DioClient(_fakeConfig());
      client.raw.httpClientAdapter = adapter;

      try {
        await client.raw.post<dynamic>('/notebook');
        fail('expected DioException');
      } on DioException catch (_) {}
      expect(adapter.callCount, 1);
    });
  });

  group('DioClient — retry policy', () {
    test('5xx retries 3 times then fails with NetworkException', () async {
      // 1 original + 3 retries = 4 total calls, all 500.
      final adapter = _ScriptedAdapter([
        _PlannedStatus(500),
        _PlannedStatus(500),
        _PlannedStatus(500),
        _PlannedStatus(500),
      ]);
      final client = DioClient(_fakeConfig());
      client.raw.httpClientAdapter = adapter;

      try {
        await client.raw.get<dynamic>('/flaky');
        fail('expected DioException');
      } on DioException catch (e) {
        final inner = _unwrap(e);
        expect(inner, isA<NetworkException>());
        expect((inner as NetworkException).statusCode, 500);
      }
      expect(
        adapter.callCount,
        4,
        reason: '1 original + 3 retries = 4 total HTTP calls',
      );
    }, timeout: const Timeout(Duration(seconds: 30)));

    test('connectionTimeout is retried (all attempts consumed)', () async {
      // Note: when the adapter throws a DioException and the retry interceptor
      // re-issues via `_dio.fetch()`, nested pipeline reprocessing collapses
      // the original type to `unknown` by the time the outer caller sees it.
      // The `5xx → NetworkException` test already exercises the
      // retry→NetworkException mapping end-to-end; here we only verify the
      // retry policy itself: a timeout is retryable (4 calls = 1 + 3 retries)
      // and it ultimately surfaces as an AppException.
      //
      // Must reuse the actual RequestOptions passed to `fetch`, otherwise the
      // `_retryAttempt` counter (stored in options.extra) is lost on every
      // rebuild and the retry loop never terminates.
      DioException mkTimeout(RequestOptions opts) =>
          DioException.connectionTimeout(
            timeout: const Duration(seconds: 5),
            requestOptions: opts,
            error: 'simulated connect timeout',
          );
      final adapter = _ScriptedAdapter([
        _PlannedThrowFromOptions(mkTimeout),
        _PlannedThrowFromOptions(mkTimeout),
        _PlannedThrowFromOptions(mkTimeout),
        _PlannedThrowFromOptions(mkTimeout),
      ]);
      final client = DioClient(_fakeConfig());
      client.raw.httpClientAdapter = adapter;

      try {
        await client.raw.get<dynamic>('/slow');
        fail('expected DioException');
      } on DioException catch (e) {
        expect(_unwrap(e), isA<AppException>());
      }
      expect(adapter.callCount, 4, reason: 'timeout is retryable → 4 attempts');
    }, timeout: const Timeout(Duration(seconds: 30)));

    test('5xx then 200 on retry succeeds', () async {
      final adapter = _ScriptedAdapter([
        _PlannedStatus(500),
        _PlannedStatus(200, body: {'ok': true}),
      ]);
      final client = DioClient(_fakeConfig());
      client.raw.httpClientAdapter = adapter;

      final res = await client.raw.get<dynamic>('/recovers');
      expect(res.statusCode, 200);
      expect(adapter.callCount, 2,
          reason: 'original 500 + 1 retry that succeeds');
    });
  });
}
