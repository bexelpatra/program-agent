import 'package:just_audio/just_audio.dart';
import 'package:just_audio_background/just_audio_background.dart';

import '../../../../core/audio/audio_service.dart';
import '../../../../core/config/app_config.dart';
import '../../../episode_detail/domain/entities/episode_detail.dart';
import '../../domain/entities/playback_source.dart';

/// Data-layer wrapper around `AudioService`.
///
/// Responsibilities kept here (and not in the repository) so the repository
/// stays a thin Result-mapping adapter:
///   - Resolving [PlaybackSource] from an [EpisodeDetail]
///     (downloaded → local, else streaming from `/api/v1/episodes/{id}/audio`)
///   - Building the `MediaItem` metadata shown on lock-screen / notification
///   - Attaching the Bearer token via HTTP headers on the streaming path
///     (local files skip auth — they've already been fetched and persisted)
///   - Forwarding play/pause/seek calls
///   - Exposing raw just_audio streams for the repository to adapt to
///     domain [PlaybackState]
class PlayerAudioDataSource {
  PlayerAudioDataSource({
    required AudioService audioService,
    required AppConfig config,
  })  : _audio = audioService,
        _config = config;

  final AudioService _audio;
  final AppConfig _config;

  /// Decide which source to use for [detail]. Downloaded copies always win:
  /// if the local MP3 is present, the user has already committed to the
  /// offline snapshot and we shouldn't bounce them back to streaming on
  /// network glitches.
  PlaybackSource resolveSource(EpisodeDetail detail) {
    final ep = detail.episode;
    final localPath = ep.audioLocalPath;
    if (ep.isDownloaded && localPath != null && localPath.isNotEmpty) {
      return PlaybackSource.local(path: localPath);
    }
    final url = '${_config.apiBaseUrl}/api/v1/episodes/${ep.id}/audio';
    return PlaybackSource.streaming(url: url);
  }

  /// Load [detail] into the player. Does not auto-play — caller must invoke
  /// [play] separately so the UI can opt into pre-roll behaviour.
  ///
  /// Throws whatever `AudioService.setSource` / `just_audio` throws on
  /// failure (PlayerException, PlatformException, ArgumentError). The
  /// repository is responsible for converting these to [AppException].
  Future<void> loadEpisode(EpisodeDetail detail) async {
    final source = resolveSource(detail);
    final metadata = _mediaItem(detail);

    await source.when(
      local: (path) => _audio.setSource(
        url: null,
        localPath: path,
        metadata: metadata,
      ),
      streaming: (url) => _audio.setSource(
        url: url,
        metadata: metadata,
        headers: _streamingAuthHeaders(),
      ),
      none: () =>
          throw ArgumentError('loadEpisode requires a resolvable source'),
    );
  }

  /// Bearer header for the authenticated `/api/v1/episodes/{id}/audio`
  /// endpoint. Kept as an instance method (rather than inlined) so the
  /// header shape is unambiguous and can be overridden in tests via a
  /// subclass if needed.
  Map<String, String> _streamingAuthHeaders() {
    return {'Authorization': 'Bearer ${_config.apiToken}'};
  }

  Future<void> play() => _audio.play();

  Future<void> pause() => _audio.pause();

  Future<void> seek(Duration position) => _audio.seek(position);

  Future<void> dispose() => _audio.dispose();

  /// Low-level `(playing, processingState)` tuple from just_audio. The
  /// repository combines this with [positionStream] to build the domain
  /// [PlaybackState].
  Stream<PlayerState> get playerStateStream => _audio.stateStream;

  /// Current playback head, emitted at roughly 10Hz by just_audio.
  Stream<Duration> get positionStream => _audio.positionStream;

  static MediaItem _mediaItem(EpisodeDetail detail) {
    final ep = detail.episode;
    return MediaItem(
      id: ep.id,
      title: ep.title,
      // `album` used by Android's media session as the "subtitle" line.
      album: 'ABC News Daily',
      duration: ep.durationMs > 0
          ? Duration(milliseconds: ep.durationMs)
          : null,
    );
  }
}
