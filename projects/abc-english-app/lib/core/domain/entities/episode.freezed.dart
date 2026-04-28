// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'episode.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

/// @nodoc
mixin _$Episode {
  String get id => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  DateTime get publishedDate => throw _privateConstructorUsedError;
  int get durationMs => throw _privateConstructorUsedError;
  DateTime get lastModified => throw _privateConstructorUsedError;
  bool get isDownloaded => throw _privateConstructorUsedError;
  double? get avgWer => throw _privateConstructorUsedError;
  String? get audioLocalPath => throw _privateConstructorUsedError;

  /// Create a copy of Episode
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $EpisodeCopyWith<Episode> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $EpisodeCopyWith<$Res> {
  factory $EpisodeCopyWith(Episode value, $Res Function(Episode) then) =
      _$EpisodeCopyWithImpl<$Res, Episode>;
  @useResult
  $Res call({
    String id,
    String title,
    DateTime publishedDate,
    int durationMs,
    DateTime lastModified,
    bool isDownloaded,
    double? avgWer,
    String? audioLocalPath,
  });
}

/// @nodoc
class _$EpisodeCopyWithImpl<$Res, $Val extends Episode>
    implements $EpisodeCopyWith<$Res> {
  _$EpisodeCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Episode
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? title = null,
    Object? publishedDate = null,
    Object? durationMs = null,
    Object? lastModified = null,
    Object? isDownloaded = null,
    Object? avgWer = freezed,
    Object? audioLocalPath = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as String,
            title: null == title
                ? _value.title
                : title // ignore: cast_nullable_to_non_nullable
                      as String,
            publishedDate: null == publishedDate
                ? _value.publishedDate
                : publishedDate // ignore: cast_nullable_to_non_nullable
                      as DateTime,
            durationMs: null == durationMs
                ? _value.durationMs
                : durationMs // ignore: cast_nullable_to_non_nullable
                      as int,
            lastModified: null == lastModified
                ? _value.lastModified
                : lastModified // ignore: cast_nullable_to_non_nullable
                      as DateTime,
            isDownloaded: null == isDownloaded
                ? _value.isDownloaded
                : isDownloaded // ignore: cast_nullable_to_non_nullable
                      as bool,
            avgWer: freezed == avgWer
                ? _value.avgWer
                : avgWer // ignore: cast_nullable_to_non_nullable
                      as double?,
            audioLocalPath: freezed == audioLocalPath
                ? _value.audioLocalPath
                : audioLocalPath // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$EpisodeImplCopyWith<$Res> implements $EpisodeCopyWith<$Res> {
  factory _$$EpisodeImplCopyWith(
    _$EpisodeImpl value,
    $Res Function(_$EpisodeImpl) then,
  ) = __$$EpisodeImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String id,
    String title,
    DateTime publishedDate,
    int durationMs,
    DateTime lastModified,
    bool isDownloaded,
    double? avgWer,
    String? audioLocalPath,
  });
}

/// @nodoc
class __$$EpisodeImplCopyWithImpl<$Res>
    extends _$EpisodeCopyWithImpl<$Res, _$EpisodeImpl>
    implements _$$EpisodeImplCopyWith<$Res> {
  __$$EpisodeImplCopyWithImpl(
    _$EpisodeImpl _value,
    $Res Function(_$EpisodeImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of Episode
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? title = null,
    Object? publishedDate = null,
    Object? durationMs = null,
    Object? lastModified = null,
    Object? isDownloaded = null,
    Object? avgWer = freezed,
    Object? audioLocalPath = freezed,
  }) {
    return _then(
      _$EpisodeImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as String,
        title: null == title
            ? _value.title
            : title // ignore: cast_nullable_to_non_nullable
                  as String,
        publishedDate: null == publishedDate
            ? _value.publishedDate
            : publishedDate // ignore: cast_nullable_to_non_nullable
                  as DateTime,
        durationMs: null == durationMs
            ? _value.durationMs
            : durationMs // ignore: cast_nullable_to_non_nullable
                  as int,
        lastModified: null == lastModified
            ? _value.lastModified
            : lastModified // ignore: cast_nullable_to_non_nullable
                  as DateTime,
        isDownloaded: null == isDownloaded
            ? _value.isDownloaded
            : isDownloaded // ignore: cast_nullable_to_non_nullable
                  as bool,
        avgWer: freezed == avgWer
            ? _value.avgWer
            : avgWer // ignore: cast_nullable_to_non_nullable
                  as double?,
        audioLocalPath: freezed == audioLocalPath
            ? _value.audioLocalPath
            : audioLocalPath // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc

class _$EpisodeImpl implements _Episode {
  const _$EpisodeImpl({
    required this.id,
    required this.title,
    required this.publishedDate,
    required this.durationMs,
    required this.lastModified,
    required this.isDownloaded,
    this.avgWer,
    this.audioLocalPath,
  });

  @override
  final String id;
  @override
  final String title;
  @override
  final DateTime publishedDate;
  @override
  final int durationMs;
  @override
  final DateTime lastModified;
  @override
  final bool isDownloaded;
  @override
  final double? avgWer;
  @override
  final String? audioLocalPath;

  @override
  String toString() {
    return 'Episode(id: $id, title: $title, publishedDate: $publishedDate, durationMs: $durationMs, lastModified: $lastModified, isDownloaded: $isDownloaded, avgWer: $avgWer, audioLocalPath: $audioLocalPath)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$EpisodeImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.publishedDate, publishedDate) ||
                other.publishedDate == publishedDate) &&
            (identical(other.durationMs, durationMs) ||
                other.durationMs == durationMs) &&
            (identical(other.lastModified, lastModified) ||
                other.lastModified == lastModified) &&
            (identical(other.isDownloaded, isDownloaded) ||
                other.isDownloaded == isDownloaded) &&
            (identical(other.avgWer, avgWer) || other.avgWer == avgWer) &&
            (identical(other.audioLocalPath, audioLocalPath) ||
                other.audioLocalPath == audioLocalPath));
  }

  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    title,
    publishedDate,
    durationMs,
    lastModified,
    isDownloaded,
    avgWer,
    audioLocalPath,
  );

  /// Create a copy of Episode
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$EpisodeImplCopyWith<_$EpisodeImpl> get copyWith =>
      __$$EpisodeImplCopyWithImpl<_$EpisodeImpl>(this, _$identity);
}

abstract class _Episode implements Episode {
  const factory _Episode({
    required final String id,
    required final String title,
    required final DateTime publishedDate,
    required final int durationMs,
    required final DateTime lastModified,
    required final bool isDownloaded,
    final double? avgWer,
    final String? audioLocalPath,
  }) = _$EpisodeImpl;

  @override
  String get id;
  @override
  String get title;
  @override
  DateTime get publishedDate;
  @override
  int get durationMs;
  @override
  DateTime get lastModified;
  @override
  bool get isDownloaded;
  @override
  double? get avgWer;
  @override
  String? get audioLocalPath;

  /// Create a copy of Episode
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$EpisodeImplCopyWith<_$EpisodeImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
