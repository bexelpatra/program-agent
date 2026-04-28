import 'package:freezed_annotation/freezed_annotation.dart';

part 'playback_source.freezed.dart';

/// Where the player should fetch audio bytes from for a given episode.
///
/// Kept separate from [PlaybackState] because the source is a one-time
/// decision made at `loadEpisode` time (local vs streaming), not a
/// continuously-changing state value. Union type lets the data layer branch
/// cleanly on [map] / [when] without flag-based switching.
@freezed
class PlaybackSource with _$PlaybackSource {
  /// Offline playback from a downloaded MP3 on disk. [path] must be an
  /// absolute filesystem path resolved against `path_provider`.
  const factory PlaybackSource.local({
    required String path,
  }) = LocalSource;

  /// Online playback streamed from a remote URL. The URL targets the
  /// `/api/v1/episodes/{id}/audio` endpoint; Bearer auth is the data layer's
  /// responsibility (see `PlayerAudioDataSource`).
  const factory PlaybackSource.streaming({
    required String url,
  }) = StreamingSource;

  /// Explicit "nothing loaded" marker. Keeps callers from smuggling `null`
  /// around when no episode has been bound yet.
  const factory PlaybackSource.none() = NoSource;
}
