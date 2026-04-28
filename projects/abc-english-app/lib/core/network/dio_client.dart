import 'dart:async';
import 'dart:math' as math;

import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../config/app_config.dart';
import '../errors/app_exception.dart';
import '../logging/app_logger.dart';

/// Max retry attempts for transient failures.
const _maxRetries = 3;

/// Base back-off for exponential delay (doubles each attempt).
const _baseBackoff = Duration(milliseconds: 300);

const _connectTimeout = Duration(seconds: 5);
const _receiveTimeout = Duration(seconds: 10);

/// Thin wrapper around [Dio] for the app-wide HTTP client.
///
/// - Injects `Authorization: Bearer <token>` from [AppConfig].
/// - Retries transient failures (network/5xx) with exponential back-off,
///   but never 4xx (client error is permanent).
/// - Converts [DioException] into the project's [AppException] hierarchy.
/// - Emits structured debug logs (url, method, status, elapsed ms).
class DioClient {
  DioClient(this._config) : _dio = Dio() {
    _dio.options
      ..baseUrl = _config.apiBaseUrl
      ..connectTimeout = _connectTimeout
      ..receiveTimeout = _receiveTimeout
      ..headers['Accept'] = 'application/json';

    _dio.interceptors.add(_authInterceptor());
    _dio.interceptors.add(_loggingInterceptor());
    _dio.interceptors.add(_retryInterceptor());
    _dio.interceptors.add(_errorMappingInterceptor());
  }

  final AppConfig _config;
  final Dio _dio;

  /// Underlying [Dio] instance. Expose for feature layers that need to build
  /// typed repositories; avoid leaking this outside `core/` callers.
  Dio get raw => _dio;

  Interceptor _authInterceptor() {
    return InterceptorsWrapper(
      onRequest: (options, handler) {
        options.headers['Authorization'] = 'Bearer ${_config.apiToken}';
        handler.next(options);
      },
    );
  }

  Interceptor _loggingInterceptor() {
    return InterceptorsWrapper(
      onRequest: (options, handler) {
        options.extra['_startedAt'] = DateTime.now().millisecondsSinceEpoch;
        AppLogger.instance.debug(
          'http.request',
          context: {
            'method': options.method,
            'url': options.uri.toString(),
          },
        );
        handler.next(options);
      },
      onResponse: (response, handler) {
        final startedAt = response.requestOptions.extra['_startedAt'] as int?;
        final elapsedMs = startedAt == null
            ? null
            : DateTime.now().millisecondsSinceEpoch - startedAt;
        AppLogger.instance.debug(
          'http.response',
          context: {
            'method': response.requestOptions.method,
            'url': response.requestOptions.uri.toString(),
            'status': response.statusCode,
            'elapsed_ms': elapsedMs,
          },
        );
        handler.next(response);
      },
    );
  }

  Interceptor _retryInterceptor() {
    return InterceptorsWrapper(
      onError: (error, handler) async {
        if (!_shouldRetry(error)) {
          handler.next(error);
          return;
        }

        final options = error.requestOptions;
        final attempt = (options.extra['_retryAttempt'] as int? ?? 0) + 1;
        if (attempt > _maxRetries) {
          // Exhausted retries on a retryable error. Map and `reject` here
          // so the downstream `_errorMappingInterceptor` does *not* wrap
          // this a second time — nested `_dio.fetch()` already propagated
          // a DioException whose `type` may have been collapsed to
          // `unknown` by dio's interceptor state machine, which would
          // mis-route connectionTimeout → UnknownException in `_mapToAppException`.
          handler.reject(_wrapAsAppException(error));
          return;
        }

        final delay = _baseBackoff * math.pow(2, attempt - 1).toInt();
        AppLogger.instance.debug(
          'http.retry',
          context: {
            'url': options.uri.toString(),
            'attempt': attempt,
            'delay_ms': delay.inMilliseconds,
          },
        );
        await Future<void>.delayed(delay);

        options.extra['_retryAttempt'] = attempt;
        try {
          final response = await _dio.fetch<dynamic>(options);
          handler.resolve(response);
        } on DioException catch (retryError) {
          // The nested fetch already ran through `_errorMappingInterceptor`,
          // so `retryError.error` is the authoritative [AppException].
          // Wrap-only-if-needed preserves the original type and avoids
          // double conversion.
          handler.reject(_preserveOrWrap(retryError, fallback: error));
        }
      },
    );
  }

  Interceptor _errorMappingInterceptor() {
    return InterceptorsWrapper(
      onError: (error, handler) {
        // If an upstream interceptor (retry) already rejected with an
        // AppException payload, pass it through untouched.
        if (error.error is AppException) {
          handler.next(error);
          return;
        }
        handler.reject(_wrapAsAppException(error));
      },
    );
  }

  /// Build a [DioException] whose `error` is the project's [AppException]
  /// while preserving the original `type`/`response`/`stackTrace` for
  /// downstream debugging.
  static DioException _wrapAsAppException(DioException error) {
    return DioException(
      requestOptions: error.requestOptions,
      response: error.response,
      type: error.type,
      error: _mapToAppException(error),
      stackTrace: error.stackTrace,
      message: error.message,
    );
  }

  /// Keep [retryError]'s AppException payload if present; otherwise fall
  /// back to mapping the *original* pre-retry [fallback] whose `type` is
  /// known-good (the nested interceptor chain can reset `type` to `unknown`).
  static DioException _preserveOrWrap(
    DioException retryError, {
    required DioException fallback,
  }) {
    if (retryError.error is AppException) {
      return retryError;
    }
    return _wrapAsAppException(fallback);
  }

  /// Retry policy:
  /// - timeouts / connection errors → yes
  /// - response with status >= 500 → yes
  /// - 4xx → no (client errors are permanent)
  /// - everything else → no
  static bool _shouldRetry(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.receiveTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.connectionError:
        return true;
      case DioExceptionType.badResponse:
        final status = error.response?.statusCode;
        return status != null && status >= 500;
      case DioExceptionType.cancel:
      case DioExceptionType.unknown:
      case DioExceptionType.badCertificate:
        return false;
    }
  }

  static AppException _mapToAppException(DioException error) {
    final status = error.response?.statusCode;
    final message = error.message ?? 'HTTP error';

    if (status == 401 || status == 403) {
      return UnauthorizedException(
        'Unauthorized (status=$status)',
        cause: error,
      );
    }
    if (status == 404) {
      return NotFoundException(
        'Not found: ${error.requestOptions.uri}',
        cause: error,
      );
    }

    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.receiveTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.connectionError:
        return NetworkException(message, cause: error, statusCode: status);
      case DioExceptionType.badResponse:
        if (status != null && status >= 500) {
          return NetworkException(
            'Server error (status=$status)',
            cause: error,
            statusCode: status,
          );
        }
        return UnknownException(message, cause: error);
      case DioExceptionType.cancel:
      case DioExceptionType.unknown:
      case DioExceptionType.badCertificate:
        return UnknownException(message, cause: error);
    }
  }
}

/// Riverpod provider for the shared [DioClient] singleton.
///
/// Override in tests via `ProviderScope(overrides: ...)` with a fake client
/// built on a [Dio] using an [InterceptorsWrapper] that resolves canned
/// responses.
final dioClientProvider = Provider<DioClient>((ref) {
  final config = ref.watch(appConfigProvider);
  return DioClient(config);
});
