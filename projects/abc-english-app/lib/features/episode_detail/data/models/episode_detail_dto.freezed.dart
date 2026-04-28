// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'episode_detail_dto.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

EpisodeDetailDto _$EpisodeDetailDtoFromJson(Map<String, dynamic> json) {
  return _EpisodeDetailDto.fromJson(json);
}

/// @nodoc
mixin _$EpisodeDetailDto {
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
  List<SentenceDto> get sentences => throw _privateConstructorUsedError;

  /// Serializes this EpisodeDetailDto to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of EpisodeDetailDto
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $EpisodeDetailDtoCopyWith<EpisodeDetailDto> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $EpisodeDetailDtoCopyWith<$Res> {
  factory $EpisodeDetailDtoCopyWith(
    EpisodeDetailDto value,
    $Res Function(EpisodeDetailDto) then,
  ) = _$EpisodeDetailDtoCopyWithImpl<$Res, EpisodeDetailDto>;
  @useResult
  $Res call({
    String id,
    String title,
    @JsonKey(name: 'published_date') String publishedDate,
    @JsonKey(name: 'duration') int? durationSeconds,
    @JsonKey(name: 'avg_wer') double? avgWer,
    @JsonKey(name: 'last_modified') String? lastModified,
    List<SentenceDto> sentences,
  });
}

/// @nodoc
class _$EpisodeDetailDtoCopyWithImpl<$Res, $Val extends EpisodeDetailDto>
    implements $EpisodeDetailDtoCopyWith<$Res> {
  _$EpisodeDetailDtoCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of EpisodeDetailDto
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
    Object? sentences = null,
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
            sentences: null == sentences
                ? _value.sentences
                : sentences // ignore: cast_nullable_to_non_nullable
                      as List<SentenceDto>,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$EpisodeDetailDtoImplCopyWith<$Res>
    implements $EpisodeDetailDtoCopyWith<$Res> {
  factory _$$EpisodeDetailDtoImplCopyWith(
    _$EpisodeDetailDtoImpl value,
    $Res Function(_$EpisodeDetailDtoImpl) then,
  ) = __$$EpisodeDetailDtoImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String id,
    String title,
    @JsonKey(name: 'published_date') String publishedDate,
    @JsonKey(name: 'duration') int? durationSeconds,
    @JsonKey(name: 'avg_wer') double? avgWer,
    @JsonKey(name: 'last_modified') String? lastModified,
    List<SentenceDto> sentences,
  });
}

/// @nodoc
class __$$EpisodeDetailDtoImplCopyWithImpl<$Res>
    extends _$EpisodeDetailDtoCopyWithImpl<$Res, _$EpisodeDetailDtoImpl>
    implements _$$EpisodeDetailDtoImplCopyWith<$Res> {
  __$$EpisodeDetailDtoImplCopyWithImpl(
    _$EpisodeDetailDtoImpl _value,
    $Res Function(_$EpisodeDetailDtoImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of EpisodeDetailDto
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
    Object? sentences = null,
  }) {
    return _then(
      _$EpisodeDetailDtoImpl(
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
        sentences: null == sentences
            ? _value._sentences
            : sentences // ignore: cast_nullable_to_non_nullable
                  as List<SentenceDto>,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$EpisodeDetailDtoImpl extends _EpisodeDetailDto {
  const _$EpisodeDetailDtoImpl({
    required this.id,
    required this.title,
    @JsonKey(name: 'published_date') required this.publishedDate,
    @JsonKey(name: 'duration') this.durationSeconds,
    @JsonKey(name: 'avg_wer') this.avgWer,
    @JsonKey(name: 'last_modified') this.lastModified,
    final List<SentenceDto> sentences = const <SentenceDto>[],
  }) : _sentences = sentences,
       super._();

  factory _$EpisodeDetailDtoImpl.fromJson(Map<String, dynamic> json) =>
      _$$EpisodeDetailDtoImplFromJson(json);

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
  final List<SentenceDto> _sentences;
  @override
  @JsonKey()
  List<SentenceDto> get sentences {
    if (_sentences is EqualUnmodifiableListView) return _sentences;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_sentences);
  }

  @override
  String toString() {
    return 'EpisodeDetailDto(id: $id, title: $title, publishedDate: $publishedDate, durationSeconds: $durationSeconds, avgWer: $avgWer, lastModified: $lastModified, sentences: $sentences)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$EpisodeDetailDtoImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.publishedDate, publishedDate) ||
                other.publishedDate == publishedDate) &&
            (identical(other.durationSeconds, durationSeconds) ||
                other.durationSeconds == durationSeconds) &&
            (identical(other.avgWer, avgWer) || other.avgWer == avgWer) &&
            (identical(other.lastModified, lastModified) ||
                other.lastModified == lastModified) &&
            const DeepCollectionEquality().equals(
              other._sentences,
              _sentences,
            ));
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
    const DeepCollectionEquality().hash(_sentences),
  );

  /// Create a copy of EpisodeDetailDto
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$EpisodeDetailDtoImplCopyWith<_$EpisodeDetailDtoImpl> get copyWith =>
      __$$EpisodeDetailDtoImplCopyWithImpl<_$EpisodeDetailDtoImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$EpisodeDetailDtoImplToJson(this);
  }
}

abstract class _EpisodeDetailDto extends EpisodeDetailDto {
  const factory _EpisodeDetailDto({
    required final String id,
    required final String title,
    @JsonKey(name: 'published_date') required final String publishedDate,
    @JsonKey(name: 'duration') final int? durationSeconds,
    @JsonKey(name: 'avg_wer') final double? avgWer,
    @JsonKey(name: 'last_modified') final String? lastModified,
    final List<SentenceDto> sentences,
  }) = _$EpisodeDetailDtoImpl;
  const _EpisodeDetailDto._() : super._();

  factory _EpisodeDetailDto.fromJson(Map<String, dynamic> json) =
      _$EpisodeDetailDtoImpl.fromJson;

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
  @override
  List<SentenceDto> get sentences;

  /// Create a copy of EpisodeDetailDto
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$EpisodeDetailDtoImplCopyWith<_$EpisodeDetailDtoImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
