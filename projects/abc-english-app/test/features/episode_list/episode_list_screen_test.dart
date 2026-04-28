import 'package:abc_english_app/core/domain/entities/episode.dart';
import 'package:abc_english_app/core/errors/app_exception.dart';
import 'package:abc_english_app/core/errors/result.dart';
import 'package:abc_english_app/features/episode_list/data/repositories/episode_repository_impl.dart';
import 'package:abc_english_app/features/episode_list/domain/repositories/episode_repository.dart';
import 'package:abc_english_app/features/episode_list/presentation/episode_list_screen.dart';
import 'package:abc_english_app/features/episode_list/presentation/widgets/episode_card.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

/// Toy repository the controller can drive. Returns canned values per
/// instance — online stream override means no real connectivity plugin call.
class _FakeRepo implements EpisodeRepository {
  _FakeRepo(this.plan);

  /// Ordered list of page-1 responses. Subsequent calls repeat the last one.
  final List<Result<List<Episode>>> plan;
  int _calls = 0;

  @override
  Future<Result<List<Episode>>> listEpisodes({
    int page = 1,
    int size = 20,
    DateTime? sinceModified,
  }) async {
    final idx = _calls < plan.length ? _calls : plan.length - 1;
    _calls++;
    return plan[idx];
  }

  @override
  Future<Result<Episode>> getById(String id) async =>
      const Failure(NotFoundException('not used'));
}

Episode _ep(String id) {
  final now = DateTime.utc(2026, 4, 5);
  return Episode(
    id: id,
    title: 'T-$id',
    publishedDate: now,
    durationMs: 60000,
    lastModified: now,
    isDownloaded: false,
  );
}

Widget _host(ProviderContainer container) {
  return UncontrolledProviderScope(
    container: container,
    child: const MaterialApp(home: EpisodeListScreen()),
  );
}

ProviderContainer _container({
  required EpisodeRepository repo,
  Stream<bool>? online,
}) {
  return ProviderContainer(
    overrides: [
      episodeRepositoryProvider.overrideWith((ref) async => repo),
      // Keep the online banner deterministic — always online by default.
      onlineStreamProvider.overrideWith((ref) =>
          online ?? Stream<bool>.fromIterable([true])),
    ],
  );
}

void main() {
  testWidgets('loading → data: renders EpisodeCard for each entry',
      (tester) async {
    final repo = _FakeRepo([
      Success([_ep('a'), _ep('b')]),
    ]);
    final c = _container(repo: repo);
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    // Initial build: loading.
    expect(find.byType(CircularProgressIndicator), findsWidgets);

    await tester.pumpAndSettle();
    expect(find.byType(EpisodeCard), findsNWidgets(2));
  });

  testWidgets('empty list shows the empty-state copy', (tester) async {
    final repo = _FakeRepo([const Success<List<Episode>>([])]);
    final c = _container(repo: repo);
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();
    expect(find.text('에피소드가 아직 없습니다'), findsOneWidget);
    expect(find.byType(EpisodeCard), findsNothing);
  });

  testWidgets('failure → error view with retry button', (tester) async {
    final repo = _FakeRepo([
      const Failure<List<Episode>>(NetworkException('offline sample')),
    ]);
    final c = _container(repo: repo);
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();

    expect(find.byIcon(Icons.error_outline), findsOneWidget);
    expect(find.text('다시 시도'), findsOneWidget);
  });

  testWidgets('offline stream shows banner', (tester) async {
    final repo = _FakeRepo([const Success<List<Episode>>([])]);
    final c = _container(
      repo: repo,
      online: Stream<bool>.fromIterable([false]),
    );
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(c));
    await tester.pumpAndSettle();
    expect(find.textContaining('오프라인'), findsOneWidget);
  });
}
