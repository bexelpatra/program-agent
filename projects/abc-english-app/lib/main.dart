import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:just_audio_background/just_audio_background.dart';

import 'app.dart';
import 'core/logging/app_logger.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Background audio plumbing — must be initialised before any audio player
  // is constructed. See https://pub.dev/packages/just_audio_background
  await JustAudioBackground.init(
    androidNotificationChannelId: 'com.abcenglish.audio',
    androidNotificationChannelName: 'ABC English playback',
    androidNotificationOngoing: true,
  );

  // Global uncaught error boundary. Routes framework errors through the
  // structured logger so we get consistent release-build reporting.
  FlutterError.onError = (details) {
    FlutterError.presentError(details);
    AppLogger.instance.error(
      'flutter.framework_error',
      context: {'library': details.library ?? 'unknown'},
      error: details.exception,
      stackTrace: details.stack,
    );
  };

  // Errors outside the Flutter framework (async, isolate).
  PlatformDispatcher.instance.onError = (error, stack) {
    AppLogger.instance.error(
      'platform.uncaught',
      error: error,
      stackTrace: stack,
    );
    return true;
  };

  runApp(
    const ProviderScope(child: AbcApp()),
  );
}
