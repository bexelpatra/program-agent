// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'episode_dto.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

EpisodeDto _$EpisodeDtoFromJson(Map<String, dynamic> json) {
  return _EpisodeDto.fromJson(json);
}

/// @nodoc
mixin _$EpisodeDto {
  String get id => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  @JsonKey(name: 'published_date')
  String get publishedDate => throw _privateConstructorUsedError;
  @JsonKey(name: 'duration')
  int? get durationSeconds => throw _privateConstructorUsedError;
  @JsonKey(name: 'avg_wer')
  double? get avgWer => throw _privateConstructorUsedError;
  @JsonKey(name: 'last_modified')
  String? get lastModified => throw _privateConstructorUsedError;

  /// Serializes this EpisodeDto to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of EpisodeDto
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $EpisodeDtoCopyWith<EpisodeDto> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $EpisodeDtoCopyWith<$Res> {
  factory $EpisodeDtoCopyWith(
    EpisodeDto value,
    $Res Function(EpisodeDto) then,
  ) = _$EpisodeDtoCopyWithImpl<$Res, EpisodeDto>;
  @useResult
  $Res call({
    String id,
    String title,
    @JsonKey(name: 'published_date') String publishedDate,
    @JsonKey(name: 'duration') int? durationSeconds,
    @JsonKey(name: 'avg_wer') double? avgWer,
    @JsonKey(name: 'last_modified') String? lastModified,
  });
}

/// @nodoc
class _$EpisodeDtoCopyWithImpl<$Res, $Val extends EpisodeDto>
    implements $EpisodeDtoCopyWith<$Res> {
  _$EpisodeDtoCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of EpisodeDto
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? title = null,
    Object? publishedDate = null,
    Object? durationSeconds = freezed,
    Object? avgWer = freezed,
    Object? lastModified = freezed,
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
                      as String,
            durationSeconds: freezed == durationSeconds
                ? _value.durationSeconds
                : durationSeconds // ignore: cast_nullable_to_non_nullable
                      as int?,
            avgWer: freezed == avgWer
                ? _value.avgWer
                : avgWer // ignore: cast_nullable_to_non_nullable
                      as double?,
            lastModified: freezed == lastModified
                ? _value.lastModified
                : lastModified // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$EpisodeDtoImplCopyWith<$Res>
    implements $EpisodeDtoCopyWith<$Res> {
  factory _$$EpisodeDtoImplCopyWith(
    _$EpisodeDtoImpl value,
    $Res Function(_$EpisodeDtoImpl) then,
  ) = __$$EpisodeDtoImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String id,
    String title,
    @JsonKey(name: 'published_date') String publishedDate,
    @JsonKey(name: 'duration') int? durationSeconds,
    @JsonKey(name: 'avg_wer') double? avgWer,
    @JsonKey(name: 'last_modified') String? lastModified,
  });
}

/// @nodoc
class __$$EpisodeDtoImplCopyWithImpl<$Res>
    extends _$EpisodeDtoCopyWithImpl<$Res, _$EpisodeDtoImpl>
    implements _$$EpisodeDtoImplCopyWith<$Res> {
  __$$EpisodeDtoImplCopyWithImpl(
    _$EpisodeDtoImpl _value,
    $Res Function(_$EpisodeDtoImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of EpisodeDto
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? title = null,
    Object? publishedDate = null,
    Object? durationSeconds = freezed,
    Object? avgWer = freezed,
    Object? lastModified = freezed,
  }) {
    return _then(
      _$EpisodeDtoImpl(
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
                  as String,
        durationSeconds: freezed == durationSeconds
            ? _value.durationSeconds
            : durationSeconds // ignore: cast_nullable_to_non_nullable
                  as int?,
        avgWer: freezed == avgWer
            ? _value.avgWer
            : avgWer // ignore: cast_nullable_to_non_nullable
                  as double?,
        lastModified: freezed == lastModified
            ? _value.lastModified
            : lastModified // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$EpisodeDtoImpl extends _EpisodeDto {
  const _$EpisodeDtoImpl({
    required this.id,
    required this.title,
    @JsonKey(name: 'published_date') required this.publishedDate,
    @JsonKey(name: 'duration') this.durationSeconds,
    @JsonKey(name: 'avg_wer') this.avgWer,
    @JsonKey(name: 'last_modified') this.lastModified,
  }) : super._();

  factory _$EpisodeDtoImpl.fromJson(Map<String, dynamic> json) =>
      _$$EpisodeDtoImplFromJson(json);

  @override
  final String id;
  @override
  final String title;
  @override
  @JsonKey(name: 'published_date')
  final String publishedDate;
  @override
  @JsonKey(name: 'duration')
  final int? durationSeconds;
  @override
  @JsonKey(name: 'avg_wer')
  final double? avgWer;
  @override
  @JsonKey(name: 'last_modified')
  final String? lastModified;

  @override
  String toString() {
    return 'EpisodeDto(id: $id, title: $title, publishedDate: $publishedDate, durationSeconds: $durationSeconds, avgWer: $avgWer, lastModified: $lastModified)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$EpisodeDtoImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.publishedDate, publishedDate) ||
                other.publishedDate == publishedDate) &&
            (identical(other.durationSeconds, durationSeconds) ||
                other.durationSeconds == durationSeconds) &&
            (identical(other.avgWer, avgWer) || other.avgWer == avgWer) &&
            (identical(other.lastModified, lastModified) ||
                other.lastModified == lastModified));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    title,
    publishedDate,
    durationSeconds,
    avgWer,
    lastModified,
  );

  /// Create a copy of EpisodeDto
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$EpisodeDtoImplCopyWith<_$EpisodeDtoImpl> get copyWith =>
      __$$EpisodeDtoImplCopyWithImpl<_$EpisodeDtoImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$EpisodeDtoImplToJson(this);
  }
}

abstract class _EpisodeDto extends EpisodeDto {
  const factory _EpisodeDto({
    required final String id,
    required final String title,
    @JsonKey(name: 'published_date') required final String publishedDate,
    @JsonKey(name: 'duration') final int? durationSeconds,
    @JsonKey(name: 'avg_wer') final double? avgWer,
    @JsonKey(name: 'last_modified') final String? lastModified,
  }) = _$EpisodeDtoImpl;
  const _EpisodeDto._() : super._();

  factory _EpisodeDto.fromJson(Map<String, dynamic> json) =
      _$EpisodeDtoImpl.fromJson;

  @override
  String get id;
  @override
  String get title;
  @override
  @JsonKey(name: 'published_date')
  String get publishedDate;
  @override
  @JsonKey(name: 'duration')
  int? get durationSeconds;
  @override
  @JsonKey(name: 'avg_wer')
  double? get avgWer;
  @override
  @JsonKey(name: 'last_modified')
  String? get lastModified;

  /// Create a copy of EpisodeDto
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$EpisodeDtoImplCopyWith<_$EpisodeDtoImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
