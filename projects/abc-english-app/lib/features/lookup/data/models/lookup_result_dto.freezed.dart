// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'lookup_result_dto.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

LookupResultDto _$LookupResultDtoFromJson(Map<String, dynamic> json) {
  return _LookupResultDto.fromJson(json);
}

/// @nodoc
mixin _$LookupResultDto {
  String get term => throw _privateConstructorUsedError;
  @JsonKey(name: 'term_type')
  String? get termType => throw _privateConstructorUsedError;
  @JsonKey(name: 'explanation_en')
  String? get explanationEn => throw _privateConstructorUsedError;
  String? get etymology => throw _privateConstructorUsedError;
  List<String> get examples => throw _privateConstructorUsedError;

  /// Serializes this LookupResultDto to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of LookupResultDto
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $LookupResultDtoCopyWith<LookupResultDto> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $LookupResultDtoCopyWith<$Res> {
  factory $LookupResultDtoCopyWith(
    LookupResultDto value,
    $Res Function(LookupResultDto) then,
  ) = _$LookupResultDtoCopyWithImpl<$Res, LookupResultDto>;
  @useResult
  $Res call({
    String term,
    @JsonKey(name: 'term_type') String? termType,
    @JsonKey(name: 'explanation_en') String? explanationEn,
    String? etymology,
    List<String> examples,
  });
}

/// @nodoc
class _$LookupResultDtoCopyWithImpl<$Res, $Val extends LookupResultDto>
    implements $LookupResultDtoCopyWith<$Res> {
  _$LookupResultDtoCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of LookupResultDto
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? term = null,
    Object? termType = freezed,
    Object? explanationEn = freezed,
    Object? etymology = freezed,
    Object? examples = null,
  }) {
    return _then(
      _value.copyWith(
            term: null == term
                ? _value.term
                : term // ignore: cast_nullable_to_non_nullable
                      as String,
            termType: freezed == termType
                ? _value.termType
                : termType // ignore: cast_nullable_to_non_nullable
                      as String?,
            explanationEn: freezed == explanationEn
                ? _value.explanationEn
                : explanationEn // ignore: cast_nullable_to_non_nullable
                      as String?,
            etymology: freezed == etymology
                ? _value.etymology
                : etymology // ignore: cast_nullable_to_non_nullable
                      as String?,
            examples: null == examples
                ? _value.examples
                : examples // ignore: cast_nullable_to_non_nullable
                      as List<String>,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$LookupResultDtoImplCopyWith<$Res>
    implements $LookupResultDtoCopyWith<$Res> {
  factory _$$LookupResultDtoImplCopyWith(
    _$LookupResultDtoImpl value,
    $Res Function(_$LookupResultDtoImpl) then,
  ) = __$$LookupResultDtoImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String term,
    @JsonKey(name: 'term_type') String? termType,
    @JsonKey(name: 'explanation_en') String? explanationEn,
    String? etymology,
    List<String> examples,
  });
}

/// @nodoc
class __$$LookupResultDtoImplCopyWithImpl<$Res>
    extends _$LookupResultDtoCopyWithImpl<$Res, _$LookupResultDtoImpl>
    implements _$$LookupResultDtoImplCopyWith<$Res> {
  __$$LookupResultDtoImplCopyWithImpl(
    _$LookupResultDtoImpl _value,
    $Res Function(_$LookupResultDtoImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of LookupResultDto
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? term = null,
    Object? termType = freezed,
    Object? explanationEn = freezed,
    Object? etymology = freezed,
    Object? examples = null,
  }) {
    return _then(
      _$LookupResultDtoImpl(
        term: null == term
            ? _value.term
            : term // ignore: cast_nullable_to_non_nullable
                  as String,
        termType: freezed == termType
            ? _value.termType
            : termType // ignore: cast_nullable_to_non_nullable
                  as String?,
        explanationEn: freezed == explanationEn
            ? _value.explanationEn
            : explanationEn // ignore: cast_nullable_to_non_nullable
                  as String?,
        etymology: freezed == etymology
            ? _value.etymology
            : etymology // ignore: cast_nullable_to_non_nullable
                  as String?,
        examples: null == examples
            ? _value._examples
            : examples // ignore: cast_nullable_to_non_nullable
                  as List<String>,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$LookupResultDtoImpl extends _LookupResultDto {
  const _$LookupResultDtoImpl({
    required this.term,
    @JsonKey(name: 'term_type') this.termType,
    @JsonKey(name: 'explanation_en') this.explanationEn,
    this.etymology,
    final List<String> examples = const <String>[],
  }) : _examples = examples,
       super._();

  factory _$LookupResultDtoImpl.fromJson(Map<String, dynamic> json) =>
      _$$LookupResultDtoImplFromJson(json);

  @override
  final String term;
  @override
  @JsonKey(name: 'term_type')
  final String? termType;
  @override
  @JsonKey(name: 'explanation_en')
  final String? explanationEn;
  @override
  final String? etymology;
  final List<String> _examples;
  @override
  @JsonKey()
  List<String> get examples {
    if (_examples is EqualUnmodifiableListView) return _examples;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_examples);
  }

  @override
  String toString() {
    return 'LookupResultDto(term: $term, termType: $termType, explanationEn: $explanationEn, etymology: $etymology, examples: $examples)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$LookupResultDtoImpl &&
            (identical(other.term, term) || other.term == term) &&
            (identical(other.termType, termType) ||
                other.termType == termType) &&
            (identical(other.explanationEn, explanationEn) ||
                other.explanationEn == explanationEn) &&
            (identical(other.etymology, etymology) ||
                other.etymology == etymology) &&
            const DeepCollectionEquality().equals(other._examples, _examples));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    term,
    termType,
    explanationEn,
    etymology,
    const DeepCollectionEquality().hash(_examples),
  );

  /// Create a copy of LookupResultDto
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$LookupResultDtoImplCopyWith<_$LookupResultDtoImpl> get copyWith =>
      __$$LookupResultDtoImplCopyWithImpl<_$LookupResultDtoImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$LookupResultDtoImplToJson(this);
  }
}

abstract class _LookupResultDto extends LookupResultDto {
  const factory _LookupResultDto({
    required final String term,
    @JsonKey(name: 'term_type') final String? termType,
    @JsonKey(name: 'explanation_en') final String? explanationEn,
    final String? etymology,
    final List<String> examples,
  }) = _$LookupResultDtoImpl;
  const _LookupResultDto._() : super._();

  factory _LookupResultDto.fromJson(Map<String, dynamic> json) =
      _$LookupResultDtoImpl.fromJson;

  @override
  String get term;
  @override
  @JsonKey(name: 'term_type')
  String? get termType;
  @override
  @JsonKey(name: 'explanation_en')
  String? get explanationEn;
  @override
  String? get etymology;
  @override
  List<String> get examples;

  /// Create a copy of LookupResultDto
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$LookupResultDtoImplCopyWith<_$LookupResultDtoImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
