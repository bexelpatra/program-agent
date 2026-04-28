// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'notebook_entry_dto.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

NotebookEntryDto _$NotebookEntryDtoFromJson(Map<String, dynamic> json) {
  return _NotebookEntryDto.fromJson(json);
}

/// @nodoc
mixin _$NotebookEntryDto {
  String get id => throw _privateConstructorUsedError;
  String get word => throw _privateConstructorUsedError;
  String get context => throw _privateConstructorUsedError;
  @JsonKey(name: 'episode_id')
  String? get episodeId => throw _privateConstructorUsedError;
  @JsonKey(name: 'sentence_index')
  int? get sentenceIndex => throw _privateConstructorUsedError;
  String? get meaning => throw _privateConstructorUsedError;
  String? get note => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at')
  String? get createdAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'last_modified')
  String? get lastModified => throw _privateConstructorUsedError;

  /// Serializes this NotebookEntryDto to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of NotebookEntryDto
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $NotebookEntryDtoCopyWith<NotebookEntryDto> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $NotebookEntryDtoCopyWith<$Res> {
  factory $NotebookEntryDtoCopyWith(
    NotebookEntryDto value,
    $Res Function(NotebookEntryDto) then,
  ) = _$NotebookEntryDtoCopyWithImpl<$Res, NotebookEntryDto>;
  @useResult
  $Res call({
    String id,
    String word,
    String context,
    @JsonKey(name: 'episode_id') String? episodeId,
    @JsonKey(name: 'sentence_index') int? sentenceIndex,
    String? meaning,
    String? note,
    @JsonKey(name: 'created_at') String? createdAt,
    @JsonKey(name: 'last_modified') String? lastModified,
  });
}

/// @nodoc
class _$NotebookEntryDtoCopyWithImpl<$Res, $Val extends NotebookEntryDto>
    implements $NotebookEntryDtoCopyWith<$Res> {
  _$NotebookEntryDtoCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of NotebookEntryDto
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? word = null,
    Object? context = null,
    Object? episodeId = freezed,
    Object? sentenceIndex = freezed,
    Object? meaning = freezed,
    Object? note = freezed,
    Object? createdAt = freezed,
    Object? lastModified = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as String,
            word: null == word
                ? _value.word
                : word // ignore: cast_nullable_to_non_nullable
                      as String,
            context: null == context
                ? _value.context
                : context // ignore: cast_nullable_to_non_nullable
                      as String,
            episodeId: freezed == episodeId
                ? _value.episodeId
                : episodeId // ignore: cast_nullable_to_non_nullable
                      as String?,
            sentenceIndex: freezed == sentenceIndex
                ? _value.sentenceIndex
                : sentenceIndex // ignore: cast_nullable_to_non_nullable
                      as int?,
            meaning: freezed == meaning
                ? _value.meaning
                : meaning // ignore: cast_nullable_to_non_nullable
                      as String?,
            note: freezed == note
                ? _value.note
                : note // ignore: cast_nullable_to_non_nullable
                      as String?,
            createdAt: freezed == createdAt
                ? _value.createdAt
                : createdAt // ignore: cast_nullable_to_non_nullable
                      as String?,
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
abstract class _$$NotebookEntryDtoImplCopyWith<$Res>
    implements $NotebookEntryDtoCopyWith<$Res> {
  factory _$$NotebookEntryDtoImplCopyWith(
    _$NotebookEntryDtoImpl value,
    $Res Function(_$NotebookEntryDtoImpl) then,
  ) = __$$NotebookEntryDtoImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String id,
    String word,
    String context,
    @JsonKey(name: 'episode_id') String? episodeId,
    @JsonKey(name: 'sentence_index') int? sentenceIndex,
    String? meaning,
    String? note,
    @JsonKey(name: 'created_at') String? createdAt,
    @JsonKey(name: 'last_modified') String? lastModified,
  });
}

/// @nodoc
class __$$NotebookEntryDtoImplCopyWithImpl<$Res>
    extends _$NotebookEntryDtoCopyWithImpl<$Res, _$NotebookEntryDtoImpl>
    implements _$$NotebookEntryDtoImplCopyWith<$Res> {
  __$$NotebookEntryDtoImplCopyWithImpl(
    _$NotebookEntryDtoImpl _value,
    $Res Function(_$NotebookEntryDtoImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of NotebookEntryDto
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? word = null,
    Object? context = null,
    Object? episodeId = freezed,
    Object? sentenceIndex = freezed,
    Object? meaning = freezed,
    Object? note = freezed,
    Object? createdAt = freezed,
    Object? lastModified = freezed,
  }) {
    return _then(
      _$NotebookEntryDtoImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as String,
        word: null == word
            ? _value.word
            : word // ignore: cast_nullable_to_non_nullable
                  as String,
        context: null == context
            ? _value.context
            : context // ignore: cast_nullable_to_non_nullable
                  as String,
        episodeId: freezed == episodeId
            ? _value.episodeId
            : episodeId // ignore: cast_nullable_to_non_nullable
                  as String?,
        sentenceIndex: freezed == sentenceIndex
            ? _value.sentenceIndex
            : sentenceIndex // ignore: cast_nullable_to_non_nullable
                  as int?,
        meaning: freezed == meaning
            ? _value.meaning
            : meaning // ignore: cast_nullable_to_non_nullable
                  as String?,
        note: freezed == note
            ? _value.note
            : note // ignore: cast_nullable_to_non_nullable
                  as String?,
        createdAt: freezed == createdAt
            ? _value.createdAt
            : createdAt // ignore: cast_nullable_to_non_nullable
                  as String?,
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
class _$NotebookEntryDtoImpl extends _NotebookEntryDto {
  const _$NotebookEntryDtoImpl({
    required this.id,
    required this.word,
    this.context = '',
    @JsonKey(name: 'episode_id') this.episodeId,
    @JsonKey(name: 'sentence_index') this.sentenceIndex,
    this.meaning,
    this.note,
    @JsonKey(name: 'created_at') this.createdAt,
    @JsonKey(name: 'last_modified') this.lastModified,
  }) : super._();

  factory _$NotebookEntryDtoImpl.fromJson(Map<String, dynamic> json) =>
      _$$NotebookEntryDtoImplFromJson(json);

  @override
  final String id;
  @override
  final String word;
  @override
  @JsonKey()
  final String context;
  @override
  @JsonKey(name: 'episode_id')
  final String? episodeId;
  @override
  @JsonKey(name: 'sentence_index')
  final int? sentenceIndex;
  @override
  final String? meaning;
  @override
  final String? note;
  @override
  @JsonKey(name: 'created_at')
  final String? createdAt;
  @override
  @JsonKey(name: 'last_modified')
  final String? lastModified;

  @override
  String toString() {
    return 'NotebookEntryDto(id: $id, word: $word, context: $context, episodeId: $episodeId, sentenceIndex: $sentenceIndex, meaning: $meaning, note: $note, createdAt: $createdAt, lastModified: $lastModified)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$NotebookEntryDtoImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.word, word) || other.word == word) &&
            (identical(other.context, context) || other.context == context) &&
            (identical(other.episodeId, episodeId) ||
                other.episodeId == episodeId) &&
            (identical(other.sentenceIndex, sentenceIndex) ||
                other.sentenceIndex == sentenceIndex) &&
            (identical(other.meaning, meaning) || other.meaning == meaning) &&
            (identical(other.note, note) || other.note == note) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.lastModified, lastModified) ||
                other.lastModified == lastModified));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    word,
    context,
    episodeId,
    sentenceIndex,
    meaning,
    note,
    createdAt,
    lastModified,
  );

  /// Create a copy of NotebookEntryDto
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$NotebookEntryDtoImplCopyWith<_$NotebookEntryDtoImpl> get copyWith =>
      __$$NotebookEntryDtoImplCopyWithImpl<_$NotebookEntryDtoImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$NotebookEntryDtoImplToJson(this);
  }
}

abstract class _NotebookEntryDto extends NotebookEntryDto {
  const factory _NotebookEntryDto({
    required final String id,
    required final String word,
    final String context,
    @JsonKey(name: 'episode_id') final String? episodeId,
    @JsonKey(name: 'sentence_index') final int? sentenceIndex,
    final String? meaning,
    final String? note,
    @JsonKey(name: 'created_at') final String? createdAt,
    @JsonKey(name: 'last_modified') final String? lastModified,
  }) = _$NotebookEntryDtoImpl;
  const _NotebookEntryDto._() : super._();

  factory _NotebookEntryDto.fromJson(Map<String, dynamic> json) =
      _$NotebookEntryDtoImpl.fromJson;

  @override
  String get id;
  @override
  String get word;
  @override
  String get context;
  @override
  @JsonKey(name: 'episode_id')
  String? get episodeId;
  @override
  @JsonKey(name: 'sentence_index')
  int? get sentenceIndex;
  @override
  String? get meaning;
  @override
  String? get note;
  @override
  @JsonKey(name: 'created_at')
  String? get createdAt;
  @override
  @JsonKey(name: 'last_modified')
  String? get lastModified;

  /// Create a copy of NotebookEntryDto
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$NotebookEntryDtoImplCopyWith<_$NotebookEntryDtoImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
