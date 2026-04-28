import 'package:abc_english_app/core/domain/entities/episode.dart';
import 'package:abc_english_app/features/episode_list/presentation/widgets/download_badge.dart';
import 'package:abc_english_app/features/episode_list/presentation/widgets/episode_card.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

Widget _harness(Widget child) => MaterialApp(home: Scaffold(body: child));

Episode _ep({
  String title = 'Morning News',
  DateTime? publishedDate,
  int durationMs = 125000,
  bool isDownloaded = false,
  double? avgWer,
}) {
  return Episode(
    id: 'ep-1',
    title: title,
    publishedDate: publishedDate ?? DateTime.utc(2026, 4, 5),
    durationMs: durationMs,
    lastModified: publishedDate ?? DateTime.utc(2026, 4, 5),
    isDownloaded: isDownloaded,
    avgWer: avgWer,
  );
}

void main() {
  testWidgets('renders title and formatted date/duration', (tester) async {
    await tester.pumpWidget(_harness(
      EpisodeCard(episode: _ep(), onTap: () {}),
    ));
    expect(find.text('Morning News'), findsOneWidget);
    expect(find.text('2026-04-05'), findsOneWidget);
    expect(find.text('02:05'), findsOneWidget,
        reason: '125000 ms → 02:05');
  });

  testWidgets('download badge hidden when not downloaded', (tester) async {
    await tester.pumpWidget(_harness(
      EpisodeCard(episode: _ep(isDownloaded: false), onTap: () {}),
    ));
    final badge = tester.widget<DownloadBadge>(find.byType(DownloadBadge));
    expect(badge.isDownloaded, isFalse);
    expect(find.text('오프라인'), findsNothing);
  });

  testWidgets('download badge visible when downloaded', (tester) async {
    await tester.pumpWidget(_harness(
      EpisodeCard(episode: _ep(isDownloaded: true), onTap: () {}),
    ));
    expect(find.text('오프라인'), findsOneWidget);
    expect(find.byIcon(Icons.download_done_rounded), findsOneWidget);
  });

  testWidgets('WER badge only shown when avgWer != null', (tester) async {
    await tester.pumpWidget(_harness(
      EpisodeCard(episode: _ep(avgWer: 0.07), onTap: () {}),
    ));
    expect(find.text('WER 7%'), findsOneWidget);
  });

  testWidgets('tap invokes onTap', (tester) async {
    var taps = 0;
    await tester.pumpWidget(_harness(
      EpisodeCard(episode: _ep(), onTap: () => taps++),
    ));
    await tester.tap(find.byType(EpisodeCard));
    await tester.pumpAndSettle();
    expect(taps, 1);
  });
}
