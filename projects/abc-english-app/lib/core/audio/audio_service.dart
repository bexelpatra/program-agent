import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:just_audio/just_audio.dart';
import 'package:just_audio_background/just_audio_background.dart';

/// Thin wrapper over [AudioPlayer] + `just_audio_background`.
///
/// Keeps core boundary clean: exposes a minimal API (setSource/play/pause/
/// seek/dispose + position/state streams) and lets the caller pick between
/// a downloaded file or a streaming URL.
///
/// Raw [PlayerException] / [PlatformException] are *not* wrapped into
/// [AppException] here — feature layer decides on UX mapping. The core
/// boundary for error conversion is the feature's repository/usecase layer.
class AudioService {
  AudioService({AudioPlayer? player}) : _player = player ?? AudioPlayer();

  final AudioPlayer _player;

  Stream<Duration> get positionStream => _player.positionStream;

  Stream<PlayerState> get stateStream => _player.playerStateStream;

  /// Load a source. Prefers [localPath] when present (offline playback),
  /// otherwise streams from [url]. Both null → [ArgumentError].
  ///
  /// [metadata] is shown on the Android lock screen / notification via
  /// `just_audio_background`. `artUri` is optional.
  ///
  /// [headers] apply **only** to streaming from [url] (they are forwarded to
  /// `just_audio`'s `AudioSource.uri(headers:)`). When playing from
  /// [localPath] the headers are ignored — local files don't speak HTTP.
  /// Pass `{'Authorization': 'Bearer <token>'}` here for authenticated
  /// streaming endpoints.
  Future<void> setSource({
    required String? url,
    String? localPath,
    required MediaItem metadata,
    Map<String, String>? headers,
  }) async {
    if (localPath == null && url == null) {
      throw ArgumentError(
        'setSource requires either localPath or url (both were null).',
      );
    }

    final source = localPath != null
        ? AudioSource.file(localPath, tag: metadata)
        : AudioSource.uri(
            Uri.parse(url!),
            tag: metadata,
            headers: headers,
          );
    await _player.setAudioSource(source);
  }

  Future<void> play() => _player.play();

  Future<void> pause() => _player.pause();

  Future<void> seek(Duration position) => _player.seek(position);

  Future<void> dispose() => _player.dispose();
}

/// Riverpod provider. `keepAlive` because the player is a heavy, long-lived
/// platform resource — we don't want it torn down when the last listener
/// temporarily drops.
final audioServiceProvider = Provider<AudioService>((ref) {
  final service = AudioService();
  ref.onDispose(() {
    service.dispose();
  });
  return service;
});
