// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'sentence_dto.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

SentenceDto _$SentenceDtoFromJson(Map<String, dynamic> json) {
  return _SentenceDto.fromJson(json);
}

/// @nodoc
mixin _$SentenceDto {
  int get index => throw _privateConstructorUsedError;
  String get text => throw _privateConstructorUsedError;
  @JsonKey(name: 'start_ms')
  int? get startMs => throw _privateConstructorUsedError;
  @JsonKey(name: 'end_ms')
  int? get endMs => throw _privateConstructorUsedError;
  double? get wer => throw _privateConstructorUsedError;
  String? get difficulty => throw _privateConstructorUsedError;

  /// Serializes this SentenceDto to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of SentenceDto
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $SentenceDtoCopyWith<SentenceDto> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SentenceDtoCopyWith<$Res> {
  factory $SentenceDtoCopyWith(
    SentenceDto value,
    $Res Function(SentenceDto) then,
  ) = _$SentenceDtoCopyWithImpl<$Res, SentenceDto>;
  @useResult
  $Res call({
    int index,
    String text,
    @JsonKey(name: 'start_ms') int? startMs,
    @JsonKey(name: 'end_ms') int? endMs,
    double? wer,
    String? difficulty,
  });
}

/// @nodoc
class _$SentenceDtoCopyWithImpl<$Res, $Val extends SentenceDto>
    implements $SentenceDtoCopyWith<$Res> {
  _$SentenceDtoCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of SentenceDto
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? index = null,
    Object? text = null,
    Object? startMs = freezed,
    Object? endMs = freezed,
    Object? wer = freezed,
    Object? difficulty = freezed,
  }) {
    return _then(
      _value.copyWith(
            index: null == index
                ? _value.index
                : index // ignore: cast_nullable_to_non_nullable
                      as int,
            text: null == text
                ? _value.text
                : text // ignore: cast_nullable_to_non_nullable
                      as String,
            startMs: freezed == startMs
                ? _value.startMs
                : startMs // ignore: cast_nullable_to_non_nullable
                      as int?,
            endMs: freezed == endMs
                ? _value.endMs
                : endMs // ignore: cast_nullable_to_non_nullable
                      as int?,
            wer: freezed == wer
                ? _value.wer
                : wer // ignore: cast_nullable_to_non_nullable
                      as double?,
            difficulty: freezed == difficulty
                ? _value.difficulty
                : difficulty // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$SentenceDtoImplCopyWith<$Res>
    implements $SentenceDtoCopyWith<$Res> {
  factory _$$SentenceDtoImplCopyWith(
    _$SentenceDtoImpl value,
    $Res Function(_$SentenceDtoImpl) then,
  ) = __$$SentenceDtoImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int index,
    String text,
    @JsonKey(name: 'start_ms') int? startMs,
    @JsonKey(name: 'end_ms') int? endMs,
    double? wer,
    String? difficulty,
  });
}

/// @nodoc
class __$$SentenceDtoImplCopyWithImpl<$Res>
    extends _$SentenceDtoCopyWithImpl<$Res, _$SentenceDtoImpl>
    implements _$$SentenceDtoImplCopyWith<$Res> {
  __$$SentenceDtoImplCopyWithImpl(
    _$SentenceDtoImpl _value,
    $Res Function(_$SentenceDtoImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of SentenceDto
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? index = null,
    Object? text = null,
    Object? startMs = freezed,
    Object? endMs = freezed,
    Object? wer = freezed,
    Object? difficulty = freezed,
  }) {
    return _then(
      _$SentenceDtoImpl(
        index: null == index
            ? _value.index
            : index // ignore: cast_nullable_to_non_nullable
                  as int,
        text: null == text
            ? _value.text
            : text // ignore: cast_nullable_to_non_nullable
                  as String,
        startMs: freezed == startMs
            ? _value.startMs
            : startMs // ignore: cast_nullable_to_non_nullable
                  as int?,
        endMs: freezed == endMs
            ? _value.endMs
            : endMs // ignore: cast_nullable_to_non_nullable
                  as int?,
        wer: freezed == wer
            ? _value.wer
            : wer // ignore: cast_nullable_to_non_nullable
                  as double?,
        difficulty: freezed == difficulty
            ? _value.difficulty
            : difficulty // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$SentenceDtoImpl extends _SentenceDto {
  const _$SentenceDtoImpl({
    required this.index,
    required this.text,
    @JsonKey(name: 'start_ms') this.startMs,
    @JsonKey(name: 'end_ms') this.endMs,
    this.wer,
    this.difficulty,
  }) : super._();

  factory _$SentenceDtoImpl.fromJson(Map<String, dynamic> json) =>
      _$$SentenceDtoImplFromJson(json);

  @override
  final int index;
  @override
  final String text;
  @override
  @JsonKey(name: 'start_ms')
  final int? startMs;
  @override
  @JsonKey(name: 'end_ms')
  final int? endMs;
  @override
  final double? wer;
  @override
  final String? difficulty;

  @override
  String toString() {
    return 'SentenceDto(index: $index, text: $text, startMs: $startMs, endMs: $endMs, wer: $wer, difficulty: $difficulty)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SentenceDtoImpl &&
            (identical(other.index, index) || other.index == index) &&
            (identical(other.text, text) || other.text == text) &&
            (identical(other.startMs, startMs) || other.startMs == startMs) &&
            (identical(other.endMs, endMs) || other.endMs == endMs) &&
            (identical(other.wer, wer) || other.wer == wer) &&
            (identical(other.difficulty, difficulty) ||
                other.difficulty == difficulty));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode =>
      Object.hash(runtimeType, index, text, startMs, endMs, wer, difficulty);

  /// Create a copy of SentenceDto
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$SentenceDtoImplCopyWith<_$SentenceDtoImpl> get copyWith =>
      __$$SentenceDtoImplCopyWithImpl<_$SentenceDtoImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SentenceDtoImplToJson(this);
  }
}

abstract class _SentenceDto extends SentenceDto {
  const factory _SentenceDto({
    required final int index,
    required final String text,
    @JsonKey(name: 'start_ms') final int? startMs,
    @JsonKey(name: 'end_ms') final int? endMs,
    final double? wer,
    final String? difficulty,
  }) = _$SentenceDtoImpl;
  const _SentenceDto._() : super._();

  factory _SentenceDto.fromJson(Map<String, dynamic> json) =
      _$SentenceDtoImpl.fromJson;

  @override
  int get index;
  @override
  String get text;
  @override
  @JsonKey(name: 'start_ms')
  int? get startMs;
  @override
  @JsonKey(name: 'end_ms')
  int? get endMs;
  @override
  double? get wer;
  @override
  String? get difficulty;

  /// Create a copy of SentenceDto
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$SentenceDtoImplCopyWith<_$SentenceDtoImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
