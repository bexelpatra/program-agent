import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/connectivity/connectivity_service.dart';
import '../../../core/domain/entities/episode.dart';
import '../../../core/errors/app_exception.dart';
import '../data/repositories/episode_repository_impl.dart';
import '../domain/usecases/list_episodes.dart';
import 'widgets/episode_card.dart';

/// Episode list (Episodes tab root).
///
/// Responsibilities:
/// - Pull paginated results via [ListEpisodes] (page=1, size=20).
/// - Load further pages when the user nears the bottom of the list.
/// - Pull-to-refresh reloads from page=1.
/// - Show an offline banner when the device loses connectivity (still
///   serves local mirror data — repository handles that transparently).
class EpisodeListScreen extends ConsumerStatefulWidget {
  const EpisodeListScreen({super.key});

  @override
  ConsumerState<EpisodeListScreen> createState() => _EpisodeListScreenState();
}

class _EpisodeListScreenState extends ConsumerState<EpisodeListScreen> {
  late final ScrollController _scrollController;

  @override
  void initState() {
    super.initState();
    _scrollController = ScrollController()..addListener(_onScroll);
  }

  @override
  void dispose() {
    _scrollController.removeListener(_onScroll);
    _scrollController.dispose();
    super.dispose();
  }

  void _onScroll() {
    // Trigger next-page load when ~400px from the bottom — small enough to
    // feel proactive, large enough to avoid firing on every overscroll.
    if (!_scrollController.hasClients) return;
    final pos = _scrollController.position;
    if (pos.pixels >= pos.maxScrollExtent - 400) {
      ref.read(episodeListControllerProvider.notifier).loadMore();
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(episodeListControllerProvider);
    final online = ref.watch(onlineStreamProvider).valueOrNull ?? true;

    return Scaffold(
      appBar: AppBar(title: const Text('Episodes')),
      body: Column(
        children: [
          if (!online) const _OfflineBanner(),
          Expanded(child: _buildBody(state)),
        ],
      ),
    );
  }

  Widget _buildBody(AsyncValue<EpisodeListState> state) {
    return state.when(
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (error, _) => _ErrorView(
        message: _friendlyMessage(error),
        onRetry: () =>
            ref.read(episodeListControllerProvider.notifier).refresh(),
      ),
      data: (data) => _EpisodeListBody(
        data: data,
        scrollController: _scrollController,
        onRefresh: () =>
            ref.read(episodeListControllerProvider.notifier).refresh(),
        onEpisodeTap: (id) => context.push('/episodes/$id'),
      ),
    );
  }

  static String _friendlyMessage(Object error) {
    if (error is NetworkException) {
      return '네트워크 오류: ${error.message}';
    }
    if (error is UnauthorizedException) {
      return '인증이 필요합니다. 앱 토큰을 확인해주세요.';
    }
    if (error is AppException) {
      return error.message;
    }
    return '목록을 불러오지 못했습니다.';
  }
}

class _OfflineBanner extends StatelessWidget {
  const _OfflineBanner();

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Container(
      width: double.infinity,
      color: scheme.errorContainer,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: [
          Icon(Icons.cloud_off_rounded,
              size: 18, color: scheme.onErrorContainer),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              '오프라인 모드 — 로컬 에피소드 표시',
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: scheme.onErrorContainer,
                  ),
            ),
          ),
        ],
      ),
    );
  }
}

class _EpisodeListBody extends StatelessWidget {
  const _EpisodeListBody({
    required this.data,
    required this.scrollController,
    required this.onRefresh,
    required this.onEpisodeTap,
  });

  final EpisodeListState data;
  final ScrollController scrollController;
  final Future<void> Function() onRefresh;
  final void Function(String episodeId) onEpisodeTap;

  @override
  Widget build(BuildContext context) {
    if (data.episodes.isEmpty) {
      return RefreshIndicator(
        onRefresh: onRefresh,
        child: ListView(
          controller: scrollController,
          physics: const AlwaysScrollableScrollPhysics(),
          children: const [
            SizedBox(height: 120),
            _EmptyStateView(),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: onRefresh,
      child: ListView.builder(
        controller: scrollController,
        physics: const AlwaysScrollableScrollPhysics(),
        itemCount: data.episodes.length + (data.isLoadingMore ? 1 : 0),
        itemBuilder: (context, index) {
          if (index >= data.episodes.length) {
            return const Padding(
              padding: EdgeInsets.symmetric(vertical: 16),
              child: Center(child: CircularProgressIndicator()),
            );
          }
          final ep = data.episodes[index];
          return EpisodeCard(
            episode: ep,
            onTap: () => onEpisodeTap(ep.id),
          );
        },
      ),
    );
  }
}

class _EmptyStateView extends StatelessWidget {
  const _EmptyStateView();

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.podcasts_rounded,
                size: 56, color: scheme.onSurfaceVariant),
            const SizedBox(height: 12),
            Text(
              '에피소드가 아직 없습니다',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 4),
            Text(
              '아래로 당겨 새로고침해보세요.',
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: scheme.onSurfaceVariant,
                  ),
            ),
          ],
        ),
      ),
    );
  }
}

class _ErrorView extends StatelessWidget {
  const _ErrorView({required this.message, required this.onRetry});

  final String message;
  final Future<void> Function() onRetry;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.error_outline, size: 48),
            const SizedBox(height: 12),
            Text(
              message,
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 16),
            FilledButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh_rounded),
              label: const Text('다시 시도'),
            ),
          ],
        ),
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// State + controller
// ---------------------------------------------------------------------------

/// View-layer state for the paginated episode list.
class EpisodeListState {
  const EpisodeListState({
    required this.episodes,
    required this.page,
    required this.hasMore,
    required this.isLoadingMore,
  });

  const EpisodeListState.initial()
      : episodes = const [],
        page = 0,
        hasMore = true,
        isLoadingMore = false;

  final List<Episode> episodes;
  final int page;
  final bool hasMore;
  final bool isLoadingMore;

  EpisodeListState copyWith({
    List<Episode>? episodes,
    int? page,
    bool? hasMore,
    bool? isLoadingMore,
  }) {
    return EpisodeListState(
      episodes: episodes ?? this.episodes,
      page: page ?? this.page,
      hasMore: hasMore ?? this.hasMore,
      isLoadingMore: isLoadingMore ?? this.isLoadingMore,
    );
  }
}

/// Provider for the `ListEpisodes` use case. Depends on the async
/// repository provider wired in the data layer.
final listEpisodesUseCaseProvider =
    FutureProvider<ListEpisodes>((ref) async {
  final repo = await ref.watch(episodeRepositoryProvider.future);
  return ListEpisodes(repo);
});

/// Stream provider exposing online/offline transitions. Used by the screen
/// to show an offline banner. Kept here (presentation) so the connectivity
/// service doesn't need to know about UI state.
final onlineStreamProvider = StreamProvider<bool>((ref) {
  return ref.watch(connectivityServiceProvider).onlineStream;
});

/// Async controller for the paginated list. Exposes refresh / loadMore
/// imperatives that the screen invokes in response to user input.
class EpisodeListController
    extends AutoDisposeAsyncNotifier<EpisodeListState> {
  static const int _pageSize = 20;

  @override
  Future<EpisodeListState> build() async {
    return _load(const EpisodeListState.initial(), page: 1);
  }

  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(
        () => _load(const EpisodeListState.initial(), page: 1));
  }

  Future<void> loadMore() async {
    final current = state.valueOrNull;
    if (current == null) return;
    if (!current.hasMore || current.isLoadingMore) return;
    state = AsyncValue.data(current.copyWith(isLoadingMore: true));
    try {
      final next = await _load(current, page: current.page + 1);
      state = AsyncValue.data(next);
    } catch (error, stack) {
      // Preserve existing list — errors during pagination just stop further
      // loads rather than blowing away what the user already sees.
      state = AsyncValue.data(current.copyWith(isLoadingMore: false));
      // Rethrow via AsyncValue.error if callers want visibility; for MVP
      // we just log through the framework.
      Zone.current.handleUncaughtError(error, stack);
    }
  }

  Future<EpisodeListState> _load(
    EpisodeListState current, {
    required int page,
  }) async {
    final useCase = await ref.read(listEpisodesUseCaseProvider.future);
    final result = await useCase(page: page, size: _pageSize);
    return result.when(
      success: (fresh) {
        final merged = page == 1
            ? fresh
            : [...current.episodes, ...fresh];
        return EpisodeListState(
          episodes: merged,
          page: page,
          hasMore: fresh.length >= _pageSize,
          isLoadingMore: false,
        );
      },
      failure: (error) => throw error,
    );
  }
}

final episodeListControllerProvider = AutoDisposeAsyncNotifierProvider<
    EpisodeListController, EpisodeListState>(
  EpisodeListController.new,
);
