import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart' show ScrollDirection;
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/errors/app_exception.dart';
import '../../../shared/presentation/widgets/lookup_bottom_sheet.dart';
import '../../episode_detail/domain/entities/episode_detail.dart';
import '../../notebook/data/repositories/notebook_repository_impl.dart';
import '../../notebook/domain/usecases/add_notebook_entry.dart';
import '../domain/entities/playback_state.dart';
import '../domain/utils/compute_current_sentence_index.dart';
import 'providers/player_providers.dart';
import 'widgets/player_control_bar.dart';
import 'widgets/player_seek_bar.dart';
import 'widgets/player_sentence_tile.dart';

/// Full-screen player with synced transcript.
///
/// Architecture:
///  - [EpisodeDetail] is fetched via [playerEpisodeProvider] (which also
///    calls [LoadEpisode] as a side effect so `stateStream` starts emitting).
///  - [PlaybackState] is subscribed via [playbackStateProvider].
///  - The transcript is a [ListView.builder]. When the current sentence
///    index changes we animate-scroll to centre that tile, unless the
///    user is actively dragging — a 5s timeout after the last manual
///    scroll gesture re-enables auto-scroll (mirrors the web UI's
///    `study.js` hands-off behaviour during seek scrubbing).
class PlayerScreen extends ConsumerStatefulWidget {
  const PlayerScreen({super.key, required this.episodeId});

  final String episodeId;

  @override
  ConsumerState<PlayerScreen> createState() => _PlayerScreenState();
}

class _PlayerScreenState extends ConsumerState<PlayerScreen> {
  final ScrollController _scrollController = ScrollController();
  final Map<int, GlobalKey> _itemKeys = {};
  int _lastScrolledIndex = -1;
  bool _userIsScrolling = false;
  Timer? _autoScrollResumeTimer;

  /// Approximate rendered height of a single [PlayerSentenceTile], used as a
  /// fallback when the target tile isn't yet mounted (long jump out of the
  /// `cacheExtent`). For the typical playback case the next sentence is
  /// already mounted, so we prefer the precise [Scrollable.ensureVisible]
  /// path below.
  static const double _approxItemHeight = 96;

  GlobalKey _keyFor(int index) =>
      _itemKeys.putIfAbsent(index, () => GlobalKey());

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_handleScroll);
  }

  @override
  void dispose() {
    _scrollController.removeListener(_handleScroll);
    _scrollController.dispose();
    _autoScrollResumeTimer?.cancel();
    super.dispose();
  }

  void _handleScroll() {
    // If the user hasn't touched the list (programmatic scroll), don't
    // flip into "user is scrolling". ScrollPosition doesn't expose that
    // reliably — approximate: treat only gesture-originated scrolls as
    // manual by checking `userScrollDirection`.
    final dir = _scrollController.position.userScrollDirection;
    if (dir == ScrollDirection.idle) return;
    _pauseAutoScroll();
  }

  void _pauseAutoScroll() {
    _userIsScrolling = true;
    _autoScrollResumeTimer?.cancel();
    _autoScrollResumeTimer = Timer(const Duration(seconds: 5), () {
      if (mounted) {
        setState(() => _userIsScrolling = false);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final detailAsync = ref.watch(playerEpisodeProvider(widget.episodeId));
    final playbackAsync = ref.watch(playbackStateProvider);

    return Scaffold(
      appBar: AppBar(
        title: detailAsync.when(
          loading: () => const Text('Loading...'),
          error: (_, _) => const Text('Player'),
          data: (detail) => Text(
            detail.episode.title,
            overflow: TextOverflow.ellipsis,
          ),
        ),
      ),
      body: detailAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, _) => _ErrorView(
          message: _friendlyMessage(error),
          onRetry: () =>
              ref.invalidate(playerEpisodeProvider(widget.episodeId)),
        ),
        data: (detail) {
          final playback = playbackAsync.value ?? PlaybackState.initial();
          final currentIndex = computeCurrentSentenceIndex(
            playback.positionMs,
            detail.sentences,
          );

          // Kick an auto-scroll when the current index changes and the
          // user isn't currently dragging the list.
          if (currentIndex != _lastScrolledIndex &&
              currentIndex >= 0 &&
              !_userIsScrolling) {
            _lastScrolledIndex = currentIndex;
            WidgetsBinding.instance.addPostFrameCallback((_) {
              _autoScrollTo(currentIndex);
            });
          }

          return _PlayerBody(
            detail: detail,
            playback: playback,
            currentIndex: currentIndex,
            scrollController: _scrollController,
            tileKeyFor: _keyFor,
            onPlayPause: () => _handlePlayPause(playback),
            onSkipBack: () => _handleSkip(playback, -15),
            onSkipForward: () => _handleSkip(playback, 15),
            onSeek: _handleSeek,
            onSentenceTap: (index) => _handleSentenceTap(
              index,
              detail.sentences,
            ),
            onWordLongPress: (word, sentenceIndex, sentenceText) =>
                _handleWordLongPress(
              word: word,
              sentenceIndex: sentenceIndex,
              sentenceText: sentenceText,
              episodeId: detail.episode.id,
            ),
          );
        },
      ),
    );
  }

  // ---------------------------------------------------------------------------
  // Actions
  // ---------------------------------------------------------------------------

  Future<void> _handlePlayPause(PlaybackState playback) async {
    final useCase = ref.read(playPauseUseCaseProvider);
    final result = await useCase(playback);
    if (!mounted) return;
    result.when(
      success: (_) {},
      failure: (error) => _toastError(error),
    );
  }

  Future<void> _handleSkip(PlaybackState playback, int seconds) async {
    final newMs = (playback.positionMs + seconds * 1000).clamp(
      0,
      playback.totalDurationMs > 0
          ? playback.totalDurationMs
          : playback.positionMs + seconds * 1000,
    );
    await _handleSeek(Duration(milliseconds: newMs));
  }

  Future<void> _handleSeek(Duration position) async {
    final useCase = ref.read(seekToUseCaseProvider);
    final result = await useCase(position);
    if (!mounted) return;
    result.when(
      success: (_) {},
      failure: (error) => _toastError(error),
    );
  }

  Future<void> _handleSentenceTap(int index, List<Sentence> sentences) async {
    // A tap on the tile seeks AND (if paused) resumes playback, matching
    // the web study page's tap-to-jump behaviour in `study.js::sentence-time`.
    final useCase = ref.read(jumpToSentenceUseCaseProvider);
    final result = await useCase(index, sentences);
    if (!mounted) return;
    result.when(
      success: (_) {
        // Re-enable auto-scroll: the user just told us where to look,
        // so further position changes should keep the viewport in sync.
        _userIsScrolling = false;
        _autoScrollResumeTimer?.cancel();
      },
      failure: (error) => _toastError(error),
    );
  }

  Future<void> _handleWordLongPress({
    required String word,
    required int sentenceIndex,
    required String sentenceText,
    required String episodeId,
  }) {
    return LookupBottomSheet.show(
      context,
      word: word,
      context: sentenceText,
      episodeId: episodeId,
      sentenceIndex: sentenceIndex,
      onAddToNotebook: _addLookupWordToNotebook,
    );
  }

  /// Bridges the shared [LookupBottomSheet] to the notebook feature.
  ///
  /// The sheet itself lives in `shared/` and must not import `features/
  /// notebook/`; the host (this screen) injects this callback so the
  /// dependency direction is: player (host) -> notebook repository.
  Future<bool> _addLookupWordToNotebook({
    required String word,
    required String context,
    String? episodeId,
    int? sentenceIndex,
    String? meaning,
    String? note,
  }) async {
    final repo = await ref.read(notebookRepositoryProvider.future);
    final useCase = AddNotebookEntry(repo);
    final result = await useCase(
      word: word,
      context: context,
      episodeId: episodeId,
      sentenceIndex: sentenceIndex,
      meaning: meaning,
      note: note,
    );
    return result.isSuccess;
  }

  // ---------------------------------------------------------------------------
  // Scroll
  // ---------------------------------------------------------------------------

  void _autoScrollTo(int index) {
    if (!_scrollController.hasClients) return;

    // Preferred path: if the target tile is mounted (visible or within the
    // cacheExtent), align its top edge with the viewport top so the new
    // dialogue line is the first line the reader's eye lands on.
    final ctx = _itemKeys[index]?.currentContext;
    if (ctx != null) {
      Scrollable.ensureVisible(
        ctx,
        alignment: 0.0,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
      return;
    }

    // Fallback: jump roughly to the index using the height estimate, then
    // re-attempt precise alignment after the next layout pass once the tile
    // is mounted.
    final pos = _scrollController.position;
    final target =
        (index * _approxItemHeight).clamp(0, pos.maxScrollExtent).toDouble();
    _scrollController.animateTo(
      target,
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeOut,
    );
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!mounted) return;
      final retryCtx = _itemKeys[index]?.currentContext;
      if (retryCtx == null) return;
      Scrollable.ensureVisible(
        retryCtx,
        alignment: 0.0,
        duration: const Duration(milliseconds: 200),
        curve: Curves.easeOut,
      );
    });
  }

  // ---------------------------------------------------------------------------
  // Utilities
  // ---------------------------------------------------------------------------

  void _toastError(AppException error) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(_friendlyMessage(error)),
        duration: const Duration(seconds: 3),
      ),
    );
  }

  static String _friendlyMessage(Object error) {
    if (error is UnauthorizedException) {
      return '인증이 필요합니다. 오디오 스트리밍이 차단되었습니다.';
    }
    if (error is NotFoundException) {
      return '에피소드를 찾을 수 없습니다.';
    }
    if (error is NetworkException) {
      return '네트워크 오류: ${error.message}';
    }
    if (error is AppException) {
      return error.message;
    }
    return '재생 중 오류가 발생했습니다.';
  }
}

// ---------------------------------------------------------------------------
// Body
// ---------------------------------------------------------------------------

class _PlayerBody extends StatelessWidget {
  const _PlayerBody({
    required this.detail,
    required this.playback,
    required this.currentIndex,
    required this.scrollController,
    required this.tileKeyFor,
    required this.onPlayPause,
    required this.onSkipBack,
    required this.onSkipForward,
    required this.onSeek,
    required this.onSentenceTap,
    required this.onWordLongPress,
  });

  final EpisodeDetail detail;
  final PlaybackState playback;
  final int currentIndex;
  final ScrollController scrollController;
  final GlobalKey Function(int index) tileKeyFor;
  final VoidCallback onPlayPause;
  final VoidCallback onSkipBack;
  final VoidCallback onSkipForward;
  final ValueChanged<Duration> onSeek;
  final ValueChanged<int> onSentenceTap;
  final void Function(String word, int sentenceIndex, String sentenceText)
      onWordLongPress;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        if (playback.error != null)
          _PlaybackErrorBanner(error: playback.error!),
        PlayerSeekBar(
          positionMs: playback.positionMs,
          totalDurationMs: playback.totalDurationMs > 0
              ? playback.totalDurationMs
              : detail.episode.durationMs,
          onSeek: onSeek,
        ),
        const SizedBox(height: 4),
        PlayerControlBar(
          isPlaying: playback.isPlaying,
          isBuffering: playback.isBuffering,
          onPlayPause: onPlayPause,
          onSkipBack: onSkipBack,
          onSkipForward: onSkipForward,
        ),
        const Divider(height: 16),
        Expanded(
          child: detail.sentences.isEmpty
              ? const Center(child: Text('문장이 없습니다.'))
              : ListView.builder(
                  controller: scrollController,
                  padding: const EdgeInsets.symmetric(vertical: 8),
                  itemCount: detail.sentences.length,
                  itemBuilder: (context, index) {
                    final sentence = detail.sentences[index];
                    return PlayerSentenceTile(
                      key: tileKeyFor(index),
                      sentence: sentence,
                      isCurrent: index == currentIndex,
                      onTap: () => onSentenceTap(index),
                      onWordLongPress: (word, context) => onWordLongPress(
                        word,
                        index,
                        context,
                      ),
                    );
                  },
                ),
        ),
      ],
    );
  }
}

class _PlaybackErrorBanner extends StatelessWidget {
  const _PlaybackErrorBanner({required this.error});

  final AppException error;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final isAuth = error is UnauthorizedException;
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      color: scheme.errorContainer,
      child: Row(
        children: [
          Icon(Icons.error_outline, color: scheme.onErrorContainer),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              isAuth
                  ? '스트리밍 인증 실패 — 토큰을 확인해주세요.'
                  : '재생 오류: ${error.message}',
              style: TextStyle(color: scheme.onErrorContainer),
            ),
          ),
        ],
      ),
    );
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
