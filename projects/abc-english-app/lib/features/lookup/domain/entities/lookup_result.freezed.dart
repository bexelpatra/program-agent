// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'lookup_result.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

/// @nodoc
mixin _$LookupResult {
  String get word => throw _privateConstructorUsedError;
  List<String> get definitions => throw _privateConstructorUsedError;
  List<String> get examples => throw _privateConstructorUsedError;
  String? get phonetic => throw _privateConstructorUsedError;
  String? get termType => throw _privateConstructorUsedError;
  String? get etymology => throw _privateConstructorUsedError;

  /// Create a copy of LookupResult
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $LookupResultCopyWith<LookupResult> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $LookupResultCopyWith<$Res> {
  factory $LookupResultCopyWith(
    LookupResult value,
    $Res Function(LookupResult) then,
  ) = _$LookupResultCopyWithImpl<$Res, LookupResult>;
  @useResult
  $Res call({
    String word,
    List<String> definitions,
    List<String> examples,
    String? phonetic,
    String? termType,
    String? etymology,
  });
}

/// @nodoc
class _$LookupResultCopyWithImpl<$Res, $Val extends LookupResult>
    implements $LookupResultCopyWith<$Res> {
  _$LookupResultCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of LookupResult
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? word = null,
    Object? definitions = null,
    Object? examples = null,
    Object? phonetic = freezed,
    Object? termType = freezed,
    Object? etymology = freezed,
  }) {
    return _then(
      _value.copyWith(
            word: null == word
                ? _value.word
                : word // ignore: cast_nullable_to_non_nullable
                      as String,
            definitions: null == definitions
                ? _value.definitions
                : definitions // ignore: cast_nullable_to_non_nullable
                      as List<String>,
            examples: null == examples
                ? _value.examples
                : examples // ignore: cast_nullable_to_non_nullable
                      as List<String>,
            phonetic: freezed == phonetic
                ? _value.phonetic
                : phonetic // ignore: cast_nullable_to_non_nullable
                      as String?,
            termType: freezed == termType
                ? _value.termType
                : termType // ignore: cast_nullable_to_non_nullable
                      as String?,
            etymology: freezed == etymology
                ? _value.etymology
                : etymology // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$LookupResultImplCopyWith<$Res>
    implements $LookupResultCopyWith<$Res> {
  factory _$$LookupResultImplCopyWith(
    _$LookupResultImpl value,
    $Res Function(_$LookupResultImpl) then,
  ) = __$$LookupResultImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String word,
    List<String> definitions,
    List<String> examples,
    String? phonetic,
    String? termType,
    String? etymology,
  });
}

/// @nodoc
class __$$LookupResultImplCopyWithImpl<$Res>
    extends _$LookupResultCopyWithImpl<$Res, _$LookupResultImpl>
    implements _$$LookupResultImplCopyWith<$Res> {
  __$$LookupResultImplCopyWithImpl(
    _$LookupResultImpl _value,
    $Res Function(_$LookupResultImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of LookupResult
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? word = null,
    Object? definitions = null,
    Object? examples = null,
    Object? phonetic = freezed,
    Object? termType = freezed,
    Object? etymology = freezed,
  }) {
    return _then(
      _$LookupResultImpl(
        word: null == word
            ? _value.word
            : word // ignore: cast_nullable_to_non_nullable
                  as String,
        definitions: null == definitions
            ? _value._definitions
            : definitions // ignore: cast_nullable_to_non_nullable
                  as List<String>,
        examples: null == examples
            ? _value._examples
            : examples // ignore: cast_nullable_to_non_nullable
                  as List<String>,
        phonetic: freezed == phonetic
            ? _value.phonetic
            : phonetic // ignore: cast_nullable_to_non_nullable
                  as String?,
        termType: freezed == termType
            ? _value.termType
            : termType // ignore: cast_nullable_to_non_nullable
                  as String?,
        etymology: freezed == etymology
            ? _value.etymology
            : etymology // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc

class _$LookupResultImpl implements _LookupResult {
  const _$LookupResultImpl({
    required this.word,
    required final List<String> definitions,
    required final List<String> examples,
    this.phonetic,
    this.termType,
    this.etymology,
  }) : _definitions = definitions,
       _examples = examples;

  @override
  final String word;
  final List<String> _definitions;
  @override
  List<String> get definitions {
    if (_definitions is EqualUnmodifiableListView) return _definitions;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_definitions);
  }

  final List<String> _examples;
  @override
  List<String> get examples {
    if (_examples is EqualUnmodifiableListView) return _examples;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_examples);
  }

  @override
  final String? phonetic;
  @override
  final String? termType;
  @override
  final String? etymology;

  @override
  String toString() {
    return 'LookupResult(word: $word, definitions: $definitions, examples: $examples, phonetic: $phonetic, termType: $termType, etymology: $etymology)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$LookupResultImpl &&
            (identical(other.word, word) || other.word == word) &&
            const DeepCollectionEquality().equals(
              other._definitions,
              _definitions,
            ) &&
            const DeepCollectionEquality().equals(other._examples, _examples) &&
            (identical(other.phonetic, phonetic) ||
                other.phonetic == phonetic) &&
            (identical(other.termType, termType) ||
                other.termType == termType) &&
            (identical(other.etymology, etymology) ||
                other.etymology == etymology));
  }

  @override
  int get hashCode => Object.hash(
    runtimeType,
    word,
    const DeepCollectionEquality().hash(_definitions),
    const DeepCollectionEquality().hash(_examples),
    phonetic,
    termType,
    etymology,
  );

  /// Create a copy of LookupResult
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$LookupResultImplCopyWith<_$LookupResultImpl> get copyWith =>
      __$$LookupResultImplCopyWithImpl<_$LookupResultImpl>(this, _$identity);
}

abstract class _LookupResult implements LookupResult {
  const factory _LookupResult({
    required final String word,
    required final List<String> definitions,
    required final List<String> examples,
    final String? phonetic,
    final String? termType,
    final String? etymology,
  }) = _$LookupResultImpl;

  @override
  String get word;
  @override
  List<String> get definitions;
  @override
  List<String> get examples;
  @override
  String? get phonetic;
  @override
  String? get termType;
  @override
  String? get etymology;

  /// Create a copy of LookupResult
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$LookupResultImplCopyWith<_$LookupResultImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
