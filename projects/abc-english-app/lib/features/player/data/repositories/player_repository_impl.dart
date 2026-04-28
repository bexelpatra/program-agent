import 'dart:async';

import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:just_audio/just_audio.dart';

import '../../../../core/audio/audio_service.dart';
import '../../../../core/config/app_config.dart';
import '../../../../core/errors/app_exception.dart';
import '../../../../core/errors/result.dart';
import '../../../episode_detail/domain/entities/episode_detail.dart';
import '../../domain/entities/playback_state.dart';
import '../../domain/repositories/player_repository.dart';
import '../datasources/player_audio_datasource.dart';

/// Adapts just_audio-flavoured streams and exceptions to the domain
/// [PlayerRepository] contract.
///
/// State assembly: just_audio exposes [PlayerState] (playing + processing)
/// and [Duration] position on *separate* streams. The domain wants a single
/// [PlaybackState] snapshot. We keep the latest of each internally and emit
/// a fresh merged snapshot on every source-stream tick, plus on every
/// public mutation (loadEpisode/error/etc.) that changes fields neither raw
/// stream covers (episodeId, totalDurationMs, surfaced AppException).
class PlayerRepositoryImpl implements PlayerRepository {
  PlayerRepositoryImpl({
    required PlayerAudioDataSource datasource,
  }) : _datasource = datasource {
    _wireUpstream();
  }

  final PlayerAudioDataSource _datasource;

  /// Broadcast so multiple widgets (scrubber, script highlight, play button)
  /// can subscribe without fighting over a single-subscription stream.
  final StreamController<PlaybackState> _stateController =
      StreamController<PlaybackState>.broadcast();

  StreamSubscription<PlayerState>? _playerStateSub;
  StreamSubscription<Duration>? _positionSub;

  PlaybackState _current = PlaybackState.initial();

  bool _disposed = false;

  @override
  Stream<PlaybackState> get stateStream => _stateController.stream;

  @override
  Future<Result<void>> loadEpisode(EpisodeDetail detail) async {
    if (_disposed) {
      return Failure(
        StorageException('player.loadEpisode after dispose'),
      );
    }
    try {
      // Reset domain state to the new binding *before* kicking off the
      // async load so subscribers don't briefly see the prior episode's
      // position while the new source buffers.
      _current = PlaybackState.initial().copyWith(
        episodeId: detail.episode.id,
        totalDurationMs: detail.episode.durationMs,
      );
      _stateController.add(_current);

      await _datasource.loadEpisode(detail);
      return const Success(null);
    } on AppException catch (error) {
      return _emitFailure(error);
    } on ArgumentError catch (error) {
      return _emitFailure(
        UnknownException('player.loadEpisode: ${error.message}',
            cause: error),
      );
    } on PlayerException catch (error) {
      return _emitFailure(
        NetworkException(
          'player.loadEpisode: ${error.message ?? "just_audio error"}',
          cause: error,
          statusCode: error.code,
        ),
      );
    } on PlatformException catch (error) {
      return _emitFailure(
        UnknownException(
          'player.loadEpisode: ${error.message ?? error.code}',
          cause: error,
        ),
      );
    } catch (error) {
      return _emitFailure(
        UnknownException('player.loadEpisode failed', cause: error),
      );
    }
  }

  @override
  Future<Result<void>> play() => _runMutation('play', _datasource.play);

  @override
  Future<Result<void>> pause() => _runMutation('pause', _datasource.pause);

  @override
  Future<Result<void>> seek(Duration position) =>
      _runMutation('seek', () => _datasource.seek(position));

  @override
  Future<Result<void>> dispose() async {
    if (_disposed) return const Success(null);
    _disposed = true;
    await _playerStateSub?.cancel();
    await _positionSub?.cancel();
    _playerStateSub = null;
    _positionSub = null;
    // `_audioService.dispose()` is idempotent on just_audio's side, but we
    // intentionally do *not* call it here: the AudioService provider in
    // core/audio/audio_service.dart already wires `ref.onDispose` to tear
    // down the underlying AudioPlayer. Calling it twice disposes a
    // singleton used across the app.
    await _stateController.close();
    return const Success(null);
  }

  // ---------------------------------------------------------------------------
  // Internals
  // ---------------------------------------------------------------------------

  void _wireUpstream() {
    _playerStateSub = _datasource.playerStateStream.listen(
      _onPlayerState,
      onError: _onStreamError,
    );
    _positionSub = _datasource.positionStream.listen(
      _onPosition,
      onError: _onStreamError,
    );
  }

  void _onPlayerState(PlayerState raw) {
    if (_disposed) return;
    _current = _current.copyWith(
      isPlaying: raw.playing,
      isBuffering: raw.processingState == ProcessingState.buffering ||
          raw.processingState == ProcessingState.loading,
      isCompleted: raw.processingState == ProcessingState.completed,
    );
    _stateController.add(_current);
  }

  void _onPosition(Duration position) {
    if (_disposed) return;
    _current = _current.copyWith(positionMs: position.inMilliseconds);
    _stateController.add(_current);
  }

  void _onStreamError(Object error, StackTrace stack) {
    if (_disposed) return;
    final mapped = _mapStreamError(error);
    _current = _current.copyWith(error: mapped);
    _stateController.add(_current);
  }

  Future<Result<void>> _runMutation(
    String op,
    Future<void> Function() action,
  ) async {
    if (_disposed) {
      return Failure(StorageException('player.$op after dispose'));
    }
    try {
      await action();
      return const Success(null);
    } on AppException catch (error) {
      return _emitFailure(error);
    } on PlayerException catch (error) {
      return _emitFailure(
        NetworkException(
          'player.$op: ${error.message ?? "just_audio error"}',
          cause: error,
          statusCode: error.code,
        ),
      );
    } on PlatformException catch (error) {
      return _emitFailure(
        UnknownException(
          'player.$op: ${error.message ?? error.code}',
          cause: error,
        ),
      );
    } catch (error) {
      return _emitFailure(
        UnknownException('player.$op failed', cause: error),
      );
    }
  }

  Failure<void> _emitFailure(AppException error) {
    _current = _current.copyWith(error: error);
    if (!_stateController.isClosed) {
      _stateController.add(_current);
    }
    return Failure(error);
  }

  AppException _mapStreamError(Object error) {
    if (error is AppException) return error;
    if (error is PlayerException) {
      return NetworkException(
        'player stream: ${error.message ?? "just_audio error"}',
        cause: error,
        statusCode: error.code,
      );
    }
    if (error is PlatformException) {
      return UnknownException(
        'player stream: ${error.message ?? error.code}',
        cause: error,
      );
    }
    return UnknownException('player stream error', cause: error);
  }
}

// ---------------------------------------------------------------------------
// Riverpod wiring
// ---------------------------------------------------------------------------

/// DI entry point consumed by presentation. Keep-alive is inherited from
/// `audioServiceProvider` (the platform resource it wraps).
final playerRepositoryProvider = Provider<PlayerRepository>((ref) {
  final audio = ref.watch(audioServiceProvider);
  final config = ref.watch(appConfigProvider);
  final datasource = PlayerAudioDataSource(
    audioService: audio,
    config: config,
  );
  final repo = PlayerRepositoryImpl(datasource: datasource);
  ref.onDispose(() {
    repo.dispose();
  });
  return repo;
});
