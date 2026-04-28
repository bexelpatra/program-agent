import 'package:abc_english_app/features/player/presentation/widgets/player_seek_bar.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

/// PlayerSeekBar is a stateless (in terms of DI) widget: positionMs /
/// totalDurationMs / onSeek are plain params, so there's no Riverpod wiring
/// to override here.
void main() {
  Widget host({
    required int positionMs,
    required int totalDurationMs,
    required ValueChanged<Duration> onSeek,
  }) {
    return MaterialApp(
      home: Scaffold(
        body: PlayerSeekBar(
          positionMs: positionMs,
          totalDurationMs: totalDurationMs,
          onSeek: onSeek,
        ),
      ),
    );
  }

  testWidgets('renders position and duration labels', (tester) async {
    await tester.pumpWidget(host(
      positionMs: 45_000, // 0:45
      totalDurationMs: 125_000, // 2:05
      onSeek: (_) {},
    ));

    expect(find.text('0:45'), findsOneWidget);
    expect(find.text('2:05'), findsOneWidget);
  });

  testWidgets('drag-end calls onSeek with the final value', (tester) async {
    Duration? seeked;
    await tester.pumpWidget(host(
      positionMs: 0,
      totalDurationMs: 120_000,
      onSeek: (d) => seeked = d,
    ));

    final slider = find.byKey(const Key('player-seek-bar'));
    expect(slider, findsOneWidget);

    // Simulate a drag on the slider thumb. A horizontal drag across the
    // slider track should push the value past 0; the exact destination ms
    // depends on the track width so we only assert that:
    //   a) onSeek fired at the gesture end; and
    //   b) the seeked Duration is non-zero (the drag moved the thumb).
    await tester.drag(slider, const Offset(200, 0));
    await tester.pumpAndSettle();

    expect(seeked, isNotNull,
        reason: 'onSeek must fire at drag-end with the final value');
    expect(seeked!.inMilliseconds > 0, isTrue);
  });

  testWidgets('zero total duration → slider is disabled (no onSeek fires)',
      (tester) async {
    Duration? seeked;
    await tester.pumpWidget(host(
      positionMs: 0,
      totalDurationMs: 0,
      onSeek: (d) => seeked = d,
    ));

    final slider = find.byKey(const Key('player-seek-bar'));
    await tester.drag(slider, const Offset(200, 0));
    await tester.pumpAndSettle();

    expect(seeked, isNull,
        reason:
            'With total duration unknown (=0) the slider should be disabled and onSeek must not fire');
  });

  testWidgets('short position → 0:05', (tester) async {
    await tester.pumpWidget(host(
      positionMs: 5_000,
      totalDurationMs: 60_000,
      onSeek: (_) {},
    ));
    expect(find.text('0:05'), findsOneWidget);
    expect(find.text('1:00'), findsOneWidget);
  });
}
