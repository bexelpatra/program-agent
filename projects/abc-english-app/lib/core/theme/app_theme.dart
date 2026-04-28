import 'package:flutter/material.dart';

/// Material 3 theme factory for the app.
///
/// Seed colour is sourced from the web UI palette
/// (`projects/abc-english/web/static/css/app.css` — light-mode
/// `--accent: #1f6feb`). The dark-mode web accent is a lighter
/// `#5aa9ff`, but Material 3's `ColorScheme.fromSeed(..., Brightness.dark)`
/// already derives the dark variant from the same seed, so we only
/// track the light seed here.
class AppTheme {
  const AppTheme._();

  /// Matches `--accent` in the web stylesheet (light mode).
  static const Color _seedColor = Color(0xFF1F6FEB);

  static ThemeData light() {
    final scheme = ColorScheme.fromSeed(
      seedColor: _seedColor,
      brightness: Brightness.light,
    );
    return _build(scheme);
  }

  static ThemeData dark() {
    final scheme = ColorScheme.fromSeed(
      seedColor: _seedColor,
      brightness: Brightness.dark,
    );
    return _build(scheme);
  }

  static ThemeData _build(ColorScheme scheme) {
    return ThemeData(
      colorScheme: scheme,
      useMaterial3: true,
      appBarTheme: AppBarTheme(
        backgroundColor: scheme.surface,
        foregroundColor: scheme.onSurface,
        elevation: 0,
        centerTitle: false,
      ),
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: scheme.surface,
        indicatorColor: scheme.secondaryContainer,
      ),
    );
  }
}
