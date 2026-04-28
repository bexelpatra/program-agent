import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../episode_detail/data/repositories/episode_detail_repository_impl.dart';
import '../../../episode_detail/domain/entities/episode_detail.dart';
import '../../../episode_detail/domain/usecases/get_episode_detail.dart';
import '../../data/repositories/player_repository_impl.dart';
import '../../domain/entities/playback_state.dart';
import '../../domain/usecases/jump_to_sentence.dart';
import '../../domain/usecases/load_episode.dart';
import '../../domain/usecases/play_pause.dart';
import '../../domain/usecases/seek_to.dart';

/// Provider wiring for the player presentation layer.
///
/// Kept separate from the screen file so widget tests can override these
/// without pulling in a full `MaterialApp.router` stack.

/// Loads the [EpisodeDetail] for the current player screen and then binds
/// the shared [PlayerRepository] to that episode via [LoadEpisode].
///
/// Family on `episodeId` so navigating back to a different episode clears
/// the bound state naturally via `autoDispose`.
final playerEpisodeProvider =
    FutureProvider.autoDispose.family<EpisodeDetail, String>(
  (ref, id) async {
    final repo = await ref.watch(episodeDetailRepositoryProvider.future);
    final useCase = GetEpisodeDetail(repo);
    final result = await useCase(id);
    return result.when(
      success: (detail) async {
        // Bind the player to the resolved episode. Failure here (missing
        // audio file / 401 on streaming URL) is surfaced via the player's
        // own [PlaybackState.error] stream, so the widget layer has two
        // distinct error channels:
        //   1. detail fetch fails → this future throws
        //   2. playback bind fails → stateStream emits `error != null`
        final playerRepo = ref.read(playerRepositoryProvider);
        final loadRes = await LoadEpisode(playerRepo)(detail);
        loadRes.when(
          success: (_) {},
          failure: (error) {
            // Don't rethrow — the UI treats a load failure as a non-fatal
            // banner so the user can still scroll the transcript.
          },
        );
        return detail;
      },
      failure: (error) => throw error,
    );
  },
);

/// Broadcast stream of the latest [PlaybackState]. Widgets subscribe via
/// `ref.watch(playbackStateProvider)` and get `AsyncValue<PlaybackState>`.
///
/// Emits the repository's current state stream directly. We don't seed it
/// with `PlaybackState.initial()` here because the player repo already
/// pushes a fresh state on every load/seek/tick.
final playbackStateProvider =
    StreamProvider.autoDispose<PlaybackState>((ref) {
  final repo = ref.watch(playerRepositoryProvider);
  return repo.stateStream;
});

// --- UseCase convenience providers --------------------------------------

final playPauseUseCaseProvider = Provider<PlayPause>((ref) {
  return PlayPause(ref.watch(playerRepositoryProvider));
});

final seekToUseCaseProvider = Provider<SeekTo>((ref) {
  return SeekTo(ref.watch(playerRepositoryProvider));
});

final jumpToSentenceUseCaseProvider = Provider<JumpToSentence>((ref) {
  return JumpToSentence(ref.watch(playerRepositoryProvider));
});
