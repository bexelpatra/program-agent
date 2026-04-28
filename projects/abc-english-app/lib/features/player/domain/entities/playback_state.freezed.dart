// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'playback_state.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

/// @nodoc
mixin _$PlaybackState {
  /// Episode currently bound to the player. `null` before the first
  /// [loadEpisode] call completes.
  String? get episodeId => throw _privateConstructorUsedError;

  /// Total track length in milliseconds. 0 until `just_audio` reports a
  /// duration (happens shortly after `setSource`).
  int get totalDurationMs => throw _privateConstructorUsedError;

  /// Current playback head in milliseconds.
  int get positionMs => throw _privateConstructorUsedError;

  /// Whether the player is actively playing (not paused / not stopped).
  /// Orthogonal to [isBuffering] — both can be true while buffering mid-play.
  bool get isPlaying => throw _privateConstructorUsedError;

  /// Whether the player is currently blocked on a buffer fill.
  bool get isBuffering => throw _privateConstructorUsedError;

  /// Whether playback has reached the end of the track.
  bool get isCompleted => throw _privateConstructorUsedError;

  /// Last surfaced error. `null` in the happy path. Presentation layer
  /// decides how to render (SnackBar, inline banner, etc.).
  AppException? get error => throw _privateConstructorUsedError;

  /// Create a copy of PlaybackState
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $PlaybackStateCopyWith<PlaybackState> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PlaybackStateCopyWith<$Res> {
  factory $PlaybackStateCopyWith(
    PlaybackState value,
    $Res Function(PlaybackState) then,
  ) = _$PlaybackStateCopyWithImpl<$Res, PlaybackState>;
  @useResult
  $Res call({
    String? episodeId,
    int totalDurationMs,
    int positionMs,
    bool isPlaying,
    bool isBuffering,
    bool isCompleted,
    AppException? error,
  });
}

/// @nodoc
class _$PlaybackStateCopyWithImpl<$Res, $Val extends PlaybackState>
    implements $PlaybackStateCopyWith<$Res> {
  _$PlaybackStateCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of PlaybackState
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? episodeId = freezed,
    Object? totalDurationMs = null,
    Object? positionMs = null,
    Object? isPlaying = null,
    Object? isBuffering = null,
    Object? isCompleted = null,
    Object? error = freezed,
  }) {
    return _then(
      _value.copyWith(
            episodeId: freezed == episodeId
                ? _value.episodeId
                : episodeId // ignore: cast_nullable_to_non_nullable
                      as String?,
            totalDurationMs: null == totalDurationMs
                ? _value.totalDurationMs
                : totalDurationMs // ignore: cast_nullable_to_non_nullable
                      as int,
            positionMs: null == positionMs
                ? _value.positionMs
                : positionMs // ignore: cast_nullable_to_non_nullable
                      as int,
            isPlaying: null == isPlaying
                ? _value.isPlaying
                : isPlaying // ignore: cast_nullable_to_non_nullable
                      as bool,
            isBuffering: null == isBuffering
                ? _value.isBuffering
                : isBuffering // ignore: cast_nullable_to_non_nullable
                      as bool,
            isCompleted: null == isCompleted
                ? _value.isCompleted
                : isCompleted // ignore: cast_nullable_to_non_nullable
                      as bool,
            error: freezed == error
                ? _value.error
                : error // ignore: cast_nullable_to_non_nullable
                      as AppException?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$PlaybackStateImplCopyWith<$Res>
    implements $PlaybackStateCopyWith<$Res> {
  factory _$$PlaybackStateImplCopyWith(
    _$PlaybackStateImpl value,
    $Res Function(_$PlaybackStateImpl) then,
  ) = __$$PlaybackStateImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String? episodeId,
    int totalDurationMs,
    int positionMs,
    bool isPlaying,
    bool isBuffering,
    bool isCompleted,
    AppException? error,
  });
}

/// @nodoc
class __$$PlaybackStateImplCopyWithImpl<$Res>
    extends _$PlaybackStateCopyWithImpl<$Res, _$PlaybackStateImpl>
    implements _$$PlaybackStateImplCopyWith<$Res> {
  __$$PlaybackStateImplCopyWithImpl(
    _$PlaybackStateImpl _value,
    $Res Function(_$PlaybackStateImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of PlaybackState
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? episodeId = freezed,
    Object? totalDurationMs = null,
    Object? positionMs = null,
    Object? isPlaying = null,
    Object? isBuffering = null,
    Object? isCompleted = null,
    Object? error = freezed,
  }) {
    return _then(
      _$PlaybackStateImpl(
        episodeId: freezed == episodeId
            ? _value.episodeId
            : episodeId // ignore: cast_nullable_to_non_nullable
                  as String?,
        totalDurationMs: null == totalDurationMs
            ? _value.totalDurationMs
            : totalDurationMs // ignore: cast_nullable_to_non_nullable
                  as int,
        positionMs: null == positionMs
            ? _value.positionMs
            : positionMs // ignore: cast_nullable_to_non_nullable
                  as int,
        isPlaying: null == isPlaying
            ? _value.isPlaying
            : isPlaying // ignore: cast_nullable_to_non_nullable
                  as bool,
        isBuffering: null == isBuffering
            ? _value.isBuffering
            : isBuffering // ignore: cast_nullable_to_non_nullable
                  as bool,
        isCompleted: null == isCompleted
            ? _value.isCompleted
            : isCompleted // ignore: cast_nullable_to_non_nullable
                  as bool,
        error: freezed == error
            ? _value.error
            : error // ignore: cast_nullable_to_non_nullable
                  as AppException?,
      ),
    );
  }
}

/// @nodoc

class _$PlaybackStateImpl implements _PlaybackState {
  const _$PlaybackStateImpl({
    this.episodeId,
    this.totalDurationMs = 0,
    this.positionMs = 0,
    this.isPlaying = false,
    this.isBuffering = false,
    this.isCompleted = false,
    this.error,
  });

  /// Episode currently bound to the player. `null` before the first
  /// [loadEpisode] call completes.
  @override
  final String? episodeId;

  /// Total track length in milliseconds. 0 until `just_audio` reports a
  /// duration (happens shortly after `setSource`).
  @override
  @JsonKey()
  final int totalDurationMs;

  /// Current playback head in milliseconds.
  @override
  @JsonKey()
  final int positionMs;

  /// Whether the player is actively playing (not paused / not stopped).
  /// Orthogonal to [isBuffering] — both can be true while buffering mid-play.
  @override
  @JsonKey()
  final bool isPlaying;

  /// Whether the player is currently blocked on a buffer fill.
  @override
  @JsonKey()
  final bool isBuffering;

  /// Whether playback has reached the end of the track.
  @override
  @JsonKey()
  final bool isCompleted;

  /// Last surfaced error. `null` in the happy path. Presentation layer
  /// decides how to render (SnackBar, inline banner, etc.).
  @override
  final AppException? error;

  @override
  String toString() {
    return 'PlaybackState(episodeId: $episodeId, totalDurationMs: $totalDurationMs, positionMs: $positionMs, isPlaying: $isPlaying, isBuffering: $isBuffering, isCompleted: $isCompleted, error: $error)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PlaybackStateImpl &&
            (identical(other.episodeId, episodeId) ||
                other.episodeId == episodeId) &&
            (identical(other.totalDurationMs, totalDurationMs) ||
                other.totalDurationMs == totalDurationMs) &&
            (identical(other.positionMs, positionMs) ||
                other.positionMs == positionMs) &&
            (identical(other.isPlaying, isPlaying) ||
                other.isPlaying == isPlaying) &&
            (identical(other.isBuffering, isBuffering) ||
                other.isBuffering == isBuffering) &&
            (identical(other.isCompleted, isCompleted) ||
                other.isCompleted == isCompleted) &&
            (identical(other.error, error) || other.error == error));
  }

  @override
  int get hashCode => Object.hash(
    runtimeType,
    episodeId,
    totalDurationMs,
    positionMs,
    isPlaying,
    isBuffering,
    isCompleted,
    error,
  );

  /// Create a copy of PlaybackState
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$PlaybackStateImplCopyWith<_$PlaybackStateImpl> get copyWith =>
      __$$PlaybackStateImplCopyWithImpl<_$PlaybackStateImpl>(this, _$identity);
}

abstract class _PlaybackState implements PlaybackState {
  const factory _PlaybackState({
    final String? episodeId,
    final int totalDurationMs,
    final int positionMs,
    final bool isPlaying,
    final bool isBuffering,
    final bool isCompleted,
    final AppException? error,
  }) = _$PlaybackStateImpl;

  /// Episode currently bound to the player. `null` before the first
  /// [loadEpisode] call completes.
  @override
  String? get episodeId;

  /// Total track length in milliseconds. 0 until `just_audio` reports a
  /// duration (happens shortly after `setSource`).
  @override
  int get totalDurationMs;

  /// Current playback head in milliseconds.
  @override
  int get positionMs;

  /// Whether the player is actively playing (not paused / not stopped).
  /// Orthogonal to [isBuffering] — both can be true while buffering mid-play.
  @override
  bool get isPlaying;

  /// Whether the player is currently blocked on a buffer fill.
  @override
  bool get isBuffering;

  /// Whether playback has reached the end of the track.
  @override
  bool get isCompleted;

  /// Last surfaced error. `null` in the happy path. Presentation layer
  /// decides how to render (SnackBar, inline banner, etc.).
  @override
  AppException? get error;

  /// Create a copy of PlaybackState
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$PlaybackStateImplCopyWith<_$PlaybackStateImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
