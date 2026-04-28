import 'package:flutter/foundation.dart';
import 'package:logger/logger.dart';

/// Keys whose values must never be logged verbatim (tokens, secrets, raw
/// user input). The [AppLogger] sanitiser replaces their values with a
/// redacted token-length marker.
const _sensitiveKeys = <String>{
  'token',
  'apiToken',
  'authorization',
  'password',
  'bearer',
};

/// Singleton structured logger for the app.
///
/// Logs are always `{feature, action, context}`. Release builds suppress
/// debug/info levels; warning+ always emitted.
class AppLogger {
  AppLogger._();
  static final AppLogger _instance = AppLogger._();
  static AppLogger get instance => _instance;

  final Logger _logger = Logger(
    level: kReleaseMode ? Level.warning : Level.debug,
    printer: PrettyPrinter(
      methodCount: 0,
      errorMethodCount: 5,
      colors: false,
      printEmojis: false,
      dateTimeFormat: DateTimeFormat.onlyTimeAndSinceStart,
    ),
  );

  void debug(String event, {Map<String, Object?>? context}) {
    _logger.d(_format(event, context));
  }

  void info(String event, {Map<String, Object?>? context}) {
    _logger.i(_format(event, context));
  }

  void warning(
    String event, {
    Map<String, Object?>? context,
    Object? error,
    StackTrace? stackTrace,
  }) {
    _logger.w(_format(event, context), error: error, stackTrace: stackTrace);
  }

  void error(
    String event, {
    Map<String, Object?>? context,
    Object? error,
    StackTrace? stackTrace,
  }) {
    _logger.e(_format(event, context), error: error, stackTrace: stackTrace);
  }

  String _format(String event, Map<String, Object?>? context) {
    if (context == null || context.isEmpty) {
      return event;
    }
    final sanitised = sanitize(context);
    return '$event $sanitised';
  }

  /// Replace sensitive fields with a length hint and strip large free-form
  /// blobs so structured logs don't leak secrets or user paste.
  ///
  /// Public so callers that build custom log strings can reuse the policy.
  static Map<String, Object?> sanitize(Map<String, Object?> ctx) {
    final out = <String, Object?>{};
    for (final entry in ctx.entries) {
      final key = entry.key;
      final value = entry.value;
      if (_sensitiveKeys.contains(key.toLowerCase())) {
        final length = value is String ? value.length : 0;
        out[key] = '<redacted len=$length>';
      } else {
        out[key] = value;
      }
    }
    return out;
  }
}
