import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Runtime environment classification.
///
/// Populated from the `ABC_ENV` compile-time constant.
enum AppEnv {
  dev,
  staging,
  prod;

  static AppEnv parse(String raw) {
    switch (raw) {
      case 'dev':
        return AppEnv.dev;
      case 'staging':
        return AppEnv.staging;
      case 'prod':
        return AppEnv.prod;
      default:
        throw ArgumentError('Unknown ABC_ENV value: "$raw"');
    }
  }
}

/// Immutable application configuration loaded from `--dart-define`.
///
/// Values must be injected at build/run time. See `scripts/run_dev.sh`.
/// Missing values trigger an assert failure in debug, and an explicit
/// [ArgumentError] in release to prevent silent mis-configuration.
class AppConfig {
  AppConfig({
    required this.apiBaseUrl,
    required this.apiToken,
    required this.env,
  }) {
    if (apiBaseUrl.isEmpty) {
      throw ArgumentError(
        'ABC_API_BASE_URL is required. Pass with --dart-define=ABC_API_BASE_URL=...',
      );
    }
    if (apiToken.isEmpty) {
      throw ArgumentError(
        'ABC_API_TOKEN is required. Pass with --dart-define=ABC_API_TOKEN=...',
      );
    }
  }

  final String apiBaseUrl;
  final String apiToken;
  final AppEnv env;

  /// Load config from compile-time constants.
  factory AppConfig.fromEnvironment() {
    const rawEnv = String.fromEnvironment('ABC_ENV', defaultValue: 'dev');
    return AppConfig(
      apiBaseUrl: const String.fromEnvironment('ABC_API_BASE_URL'),
      apiToken: const String.fromEnvironment('ABC_API_TOKEN'),
      env: AppEnv.parse(rawEnv),
    );
  }

  bool get isRelease => env == AppEnv.prod;
  bool get isDev => env == AppEnv.dev;
}

/// Riverpod provider for the singleton [AppConfig].
///
/// Override at `ProviderScope` level for testing with a fake config.
final appConfigProvider = Provider<AppConfig>((ref) {
  return AppConfig.fromEnvironment();
});
