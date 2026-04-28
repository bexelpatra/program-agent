import 'package:abc_english_app/core/domain/entities/episode.dart';
import 'package:abc_english_app/core/errors/app_exception.dart';
import 'package:abc_english_app/core/errors/result.dart';
import 'package:abc_english_app/features/episode_detail/data/repositories/episode_detail_repository_impl.dart';
import 'package:abc_english_app/features/episode_detail/domain/entities/episode_detail.dart';
import 'package:abc_english_app/features/episode_detail/domain/repositories/episode_detail_repository.dart';
import 'package:abc_english_app/features/episode_detail/presentation/episode_detail_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

class _FakeRepo implements EpisodeDetailRepository {
  _FakeRepo(this.result);
  final Result<EpisodeDetail> result;

  @override
  Future<Result<EpisodeDetail>> getDetail(String id) async => result;
}

EpisodeDetail _detail({List<Sentence>? sentences}) {
  final now = DateTime.utc(2026, 4, 5);
  return EpisodeDetail(
    episode: Episode(
      id: 'ep-1',
      title: 'Morning News',
      publishedDate: now,
      durationMs: 125000,
      lastModified: now,
      isDownloaded: false,
    ),
    sentences: sentences ??
        const [
          Sentence(index: 0, text: 'First sentence.', startMs: 0, endMs: 1000),
          Sentence(
              index: 1, text: 'Second sentence.', startMs: 1000, endMs: 2000),
          Sentence(
              index: 2, text: 'Third sentence.', startMs: 2000, endMs: 3000),
        ],
  );
}

Widget _host(ProviderContainer c) {
  return UncontrolledProviderScope(
    container: c,
    child: const MaterialApp(
      home: EpisodeDetailScreen(episodeId: 'ep-1'),
    ),
  );
}

ProviderContainer _container(Result<EpisodeDetail> result) {
  return ProviderContainer(
    overrides: [
      episodeDetailRepositoryProvider.overrideWith(
        (ref) async => _FakeRepo(result),
      ),
    ],
  );
}

void main() {
  testWidgets('data: renders sentences list + play button', (tester) async {
    final c = _container(Success(_detail()));
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();

    expect(find.text('Morning News'), findsOneWidget);
    expect(find.byKey(const Key('episode-detail-play-button')), findsOneWidget);

    // Sentence text lives inside a RichText TextSpan tree. `find.textContaining`
    // checks the whole TextSpan plainText so it matches the sentence body
    // regardless of the leading index prefix.
    final sentenceFinder = find.byWidgetPredicate(
      (w) =>
          w is RichText &&
          (w.text.toPlainText()).contains('First sentence.'),
    );
    // The sentences render below the viewport fold; scroll until the first
    // one is visible so the test is robust to window height.
    await tester.dragUntilVisible(
      sentenceFinder,
      find.byType(Scrollable).first,
      const Offset(0, -200),
    );
    expect(sentenceFinder, findsOneWidget);
  });

  testWidgets('download button tap shows SnackBar explaining phase 5',
      (tester) async {
    final c = _container(Success(_detail()));
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();

    await tester.tap(find.byKey(const Key('episode-detail-download-button')));
    await tester.pump(); // let SnackBar build
    expect(find.textContaining('다운로드 기능'), findsOneWidget);
  });

  testWidgets('empty sentences → "문장이 없습니다"', (tester) async {
    final c = _container(Success(_detail(sentences: const [])));
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();

    expect(find.text('문장이 없습니다.'), findsOneWidget);
  });

  testWidgets('failure → error view', (tester) async {
    final c = _container(
      const Failure<EpisodeDetail>(NotFoundException('gone')),
    );
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();

    expect(find.text('에피소드를 찾을 수 없습니다.'), findsOneWidget);
    expect(find.text('다시 시도'), findsOneWidget);
  });
}
