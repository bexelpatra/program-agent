import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/domain/entities/episode.dart';
import '../../../core/errors/app_exception.dart';
import '../data/repositories/episode_detail_repository_impl.dart';
import '../domain/entities/episode_detail.dart';
import '../domain/usecases/get_episode_detail.dart';

/// Episode detail screen (`/episodes/:id`).
///
/// Shows the episode header (title + meta), a large primary play button
/// that routes into the player, a placeholder download button (wired in
/// Phase 5+), and the aligned sentence list.
class EpisodeDetailScreen extends ConsumerWidget {
  const EpisodeDetailScreen({super.key, required this.episodeId});

  final String episodeId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final async = ref.watch(episodeDetailControllerProvider(episodeId));
    return Scaffold(
      appBar: AppBar(
        title: const Text('Episode'),
      ),
      body: async.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, _) => _ErrorView(
          message: _friendlyMessage(error),
          onRetry: () => ref.invalidate(
            episodeDetailControllerProvider(episodeId),
          ),
        ),
        data: (detail) => _DetailView(detail: detail),
      ),
    );
  }

  static String _friendlyMessage(Object error) {
    if (error is NotFoundException) {
      return '에피소드를 찾을 수 없습니다.';
    }
    if (error is NetworkException) {
      return '네트워크 오류: ${error.message}';
    }
    if (error is UnauthorizedException) {
      return '인증이 필요합니다. 앱 토큰을 확인해주세요.';
    }
    if (error is AppException) {
      return error.message;
    }
    return '에피소드를 불러오지 못했습니다.';
  }
}

class _DetailView extends StatelessWidget {
  const _DetailView({required this.detail});

  final EpisodeDetail detail;

  @override
  Widget build(BuildContext context) {
    return CustomScrollView(
      slivers: [
        SliverToBoxAdapter(
          child: _Header(episode: detail.episode),
        ),
        SliverToBoxAdapter(
          child: _ActionBar(episode: detail.episode),
        ),
        const SliverToBoxAdapter(
          child: Padding(
            padding: EdgeInsets.fromLTRB(16, 16, 16, 8),
            child: Text(
              'Transcript',
              style: TextStyle(fontWeight: FontWeight.w600, fontSize: 16),
            ),
          ),
        ),
        if (detail.sentences.isEmpty)
          const SliverToBoxAdapter(
            child: Padding(
              padding: EdgeInsets.all(16),
              child: Text('문장이 없습니다.'),
            ),
          )
        else
          SliverList.builder(
            itemCount: detail.sentences.length,
            itemBuilder: (context, index) {
              return _SentenceTile(sentence: detail.sentences[index]);
            },
          ),
        const SliverToBoxAdapter(child: SizedBox(height: 24)),
      ],
    );
  }
}

class _Header extends StatelessWidget {
  const _Header({required this.episode});

  final Episode episode;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final textTheme = Theme.of(context).textTheme;
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            episode.title,
            style: textTheme.headlineSmall?.copyWith(
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: 8),
          DefaultTextStyle.merge(
            style: textTheme.bodySmall?.copyWith(
              color: scheme.onSurfaceVariant,
            ),
            child: Wrap(
              spacing: 10,
              runSpacing: 4,
              crossAxisAlignment: WrapCrossAlignment.center,
              children: [
                Text(_formatDate(episode.publishedDate)),
                const Text('·'),
                Text(_formatDurationMs(episode.durationMs)),
                if (episode.avgWer != null) ...[
                  const Text('·'),
                  Text('WER ${(episode.avgWer! * 100).toStringAsFixed(0)}%'),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }

  static String _formatDate(DateTime d) {
    final y = d.year.toString().padLeft(4, '0');
    final m = d.month.toString().padLeft(2, '0');
    final day = d.day.toString().padLeft(2, '0');
    return '$y-$m-$day';
  }

  static String _formatDurationMs(int ms) {
    if (ms <= 0) return '--:--';
    final totalSec = ms ~/ 1000;
    final minutes = (totalSec ~/ 60).toString().padLeft(2, '0');
    final seconds = (totalSec % 60).toString().padLeft(2, '0');
    return '$minutes:$seconds';
  }
}

class _ActionBar extends StatelessWidget {
  const _ActionBar({required this.episode});

  final Episode episode;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Row(
        children: [
          Expanded(
            child: FilledButton.icon(
              key: const Key('episode-detail-play-button'),
              onPressed: () => context.push('/player/${episode.id}'),
              icon: const Icon(Icons.play_arrow_rounded, size: 28),
              label: const Padding(
                padding: EdgeInsets.symmetric(vertical: 8),
                child: Text('재생',
                    style: TextStyle(
                        fontSize: 16, fontWeight: FontWeight.w600)),
              ),
            ),
          ),
          const SizedBox(width: 12),
          _DownloadButton(isDownloaded: episode.isDownloaded),
        ],
      ),
    );
  }
}

class _DownloadButton extends StatelessWidget {
  const _DownloadButton({required this.isDownloaded});

  final bool isDownloaded;

  @override
  Widget build(BuildContext context) {
    // Download execution logic lands in Phase 5+ (offline downloader). For
    // now we expose the UI affordance and explain that via SnackBar so the
    // user can still see the future capability on the detail screen.
    return OutlinedButton.icon(
      key: const Key('episode-detail-download-button'),
      onPressed: () {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('다운로드 기능은 Phase 5 이후 연결 예정'),
            duration: Duration(seconds: 2),
          ),
        );
      },
      icon: Icon(
        isDownloaded
            ? Icons.download_done_rounded
            : Icons.download_rounded,
        size: 20,
      ),
      label: Text(isDownloaded ? '다운로드됨' : '다운로드'),
      style: OutlinedButton.styleFrom(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 16),
      ),
    );
  }
}

class _SentenceTile extends StatelessWidget {
  const _SentenceTile({required this.sentence});

  final Sentence sentence;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final textTheme = Theme.of(context).textTheme;

    final timeLabel =
        '(${_fmt(sentence.startMs)}–${_fmt(sentence.endMs)})';
    final extras = <String>[];
    if (sentence.wer != null) {
      extras.add('WER ${(sentence.wer! * 100).toStringAsFixed(0)}%');
    }
    if (sentence.difficulty != null && sentence.difficulty!.isNotEmpty) {
      extras.add(sentence.difficulty!);
    }

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          RichText(
            text: TextSpan(
              style: textTheme.bodyLarge,
              children: [
                TextSpan(
                  text: '${sentence.index + 1}. ',
                  style: textTheme.bodyMedium?.copyWith(
                    color: scheme.onSurfaceVariant,
                    fontFeatures: const [FontFeature.tabularFigures()],
                  ),
                ),
                TextSpan(text: sentence.text),
              ],
            ),
          ),
          const SizedBox(height: 2),
          Text(
            [timeLabel, ...extras].join('  '),
            style: textTheme.bodySmall?.copyWith(
              color: scheme.onSurfaceVariant,
              fontFeatures: const [FontFeature.tabularFigures()],
            ),
          ),
        ],
      ),
    );
  }

  static String _fmt(int ms) {
    if (ms < 0) return '--:--';
    final totalSec = ms ~/ 1000;
    final minutes = (totalSec ~/ 60).toString().padLeft(2, '0');
    final seconds = (totalSec % 60).toString().padLeft(2, '0');
    return '$minutes:$seconds';
  }
}

class _ErrorView extends StatelessWidget {
  const _ErrorView({required this.message, required this.onRetry});

  final String message;
  final VoidCallback onRetry;

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
// Providers
// ---------------------------------------------------------------------------

/// Use-case provider. Resolves the async repository dependency.
final getEpisodeDetailUseCaseProvider =
    FutureProvider<GetEpisodeDetail>((ref) async {
  final repo = await ref.watch(episodeDetailRepositoryProvider.future);
  return GetEpisodeDetail(repo);
});

/// Per-episode controller. Keyed by the episode id so separate detail
/// screens don't share state.
final episodeDetailControllerProvider = FutureProvider.autoDispose
    .family<EpisodeDetail, String>((ref, id) async {
  final useCase = await ref.watch(getEpisodeDetailUseCaseProvider.future);
  final result = await useCase(id);
  return result.when(
    success: (detail) => detail,
    failure: (error) => throw error,
  );
});
