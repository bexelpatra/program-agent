import 'package:freezed_annotation/freezed_annotation.dart';

import '../../../../core/errors/app_exception.dart';

part 'playback_state.freezed.dart';

/// Domain-level snapshot of the audio player.
///
/// Mapped from `just_audio`'s `PlayerState` + `positionStream` inside the
/// data layer (`PlayerRepositoryImpl`) — this entity stays pure Dart with no
/// platform imports so the domain/presentation layers can reason about
/// playback without pulling in `just_audio`.
///
/// All durations are carried in milliseconds (same unit as the wire format
/// and `Sentence.startMs`/`endMs`). This keeps index computation against the
/// sentence list unit-safe.
@freezed
class PlaybackState with _$PlaybackState {
  const factory PlaybackState({
    /// Episode currently bound to the player. `null` before the first
    /// [loadEpisode] call completes.
    String? episodeId,

    /// Total track length in milliseconds. 0 until `just_audio` reports a
    /// duration (happens shortly after `setSource`).
    @Default(0) int totalDurationMs,

    /// Current playback head in milliseconds.
    @Default(0) int positionMs,

    /// Whether the player is actively playing (not paused / not stopped).
    /// Orthogonal to [isBuffering] — both can be true while buffering mid-play.
    @Default(false) bool isPlaying,

    /// Whether the player is currently blocked on a buffer fill.
    @Default(false) bool isBuffering,

    /// Whether playback has reached the end of the track.
    @Default(false) bool isCompleted,

    /// Last surfaced error. `null` in the happy path. Presentation layer
    /// decides how to render (SnackBar, inline banner, etc.).
    AppException? error,
  }) = _PlaybackState;

  /// Initial state before any episode is bound.
  factory PlaybackState.initial() => const PlaybackState();
}
