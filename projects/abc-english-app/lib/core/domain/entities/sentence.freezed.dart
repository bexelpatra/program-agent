// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'sentence.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

/// @nodoc
mixin _$Sentence {
  int get index => throw _privateConstructorUsedError;
  String get text => throw _privateConstructorUsedError;
  int get startMs => throw _privateConstructorUsedError;
  int get endMs => throw _privateConstructorUsedError;
  double? get wer => throw _privateConstructorUsedError;
  String? get difficulty => throw _privateConstructorUsedError;

  /// Create a copy of Sentence
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $SentenceCopyWith<Sentence> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SentenceCopyWith<$Res> {
  factory $SentenceCopyWith(Sentence value, $Res Function(Sentence) then) =
      _$SentenceCopyWithImpl<$Res, Sentence>;
  @useResult
  $Res call({
    int index,
    String text,
    int startMs,
    int endMs,
    double? wer,
    String? difficulty,
  });
}

/// @nodoc
class _$SentenceCopyWithImpl<$Res, $Val extends Sentence>
    implements $SentenceCopyWith<$Res> {
  _$SentenceCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Sentence
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? index = null,
    Object? text = null,
    Object? startMs = null,
    Object? endMs = null,
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
            startMs: null == startMs
                ? _value.startMs
                : startMs // ignore: cast_nullable_to_non_nullable
                      as int,
            endMs: null == endMs
                ? _value.endMs
                : endMs // ignore: cast_nullable_to_non_nullable
                      as int,
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
abstract class _$$SentenceImplCopyWith<$Res>
    implements $SentenceCopyWith<$Res> {
  factory _$$SentenceImplCopyWith(
    _$SentenceImpl value,
    $Res Function(_$SentenceImpl) then,
  ) = __$$SentenceImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int index,
    String text,
    int startMs,
    int endMs,
    double? wer,
    String? difficulty,
  });
}

/// @nodoc
class __$$SentenceImplCopyWithImpl<$Res>
    extends _$SentenceCopyWithImpl<$Res, _$SentenceImpl>
    implements _$$SentenceImplCopyWith<$Res> {
  __$$SentenceImplCopyWithImpl(
    _$SentenceImpl _value,
    $Res Function(_$SentenceImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of Sentence
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? index = null,
    Object? text = null,
    Object? startMs = null,
    Object? endMs = null,
    Object? wer = freezed,
    Object? difficulty = freezed,
  }) {
    return _then(
      _$SentenceImpl(
        index: null == index
            ? _value.index
            : index // ignore: cast_nullable_to_non_nullable
                  as int,
        text: null == text
            ? _value.text
            : text // ignore: cast_nullable_to_non_nullable
                  as String,
        startMs: null == startMs
            ? _value.startMs
            : startMs // ignore: cast_nullable_to_non_nullable
                  as int,
        endMs: null == endMs
            ? _value.endMs
            : endMs // ignore: cast_nullable_to_non_nullable
                  as int,
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

class _$SentenceImpl implements _Sentence {
  const _$SentenceImpl({
    required this.index,
    required this.text,
    required this.startMs,
    required this.endMs,
    this.wer,
    this.difficulty,
  });

  @override
  final int index;
  @override
  final String text;
  @override
  final int startMs;
  @override
  final int endMs;
  @override
  final double? wer;
  @override
  final String? difficulty;

  @override
  String toString() {
    return 'Sentence(index: $index, text: $text, startMs: $startMs, endMs: $endMs, wer: $wer, difficulty: $difficulty)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SentenceImpl &&
            (identical(other.index, index) || other.index == index) &&
            (identical(other.text, text) || other.text == text) &&
            (identical(other.startMs, startMs) || other.startMs == startMs) &&
            (identical(other.endMs, endMs) || other.endMs == endMs) &&
            (identical(other.wer, wer) || other.wer == wer) &&
            (identical(other.difficulty, difficulty) ||
                other.difficulty == difficulty));
  }

  @override
  int get hashCode =>
      Object.hash(runtimeType, index, text, startMs, endMs, wer, difficulty);

  /// Create a copy of Sentence
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$SentenceImplCopyWith<_$SentenceImpl> get copyWith =>
      __$$SentenceImplCopyWithImpl<_$SentenceImpl>(this, _$identity);
}

abstract class _Sentence implements Sentence {
  const factory _Sentence({
    required final int index,
    required final String text,
    required final int startMs,
    required final int endMs,
    final double? wer,
    final String? difficulty,
  }) = _$SentenceImpl;

  @override
  int get index;
  @override
  String get text;
  @override
  int get startMs;
  @override
  int get endMs;
  @override
  double? get wer;
  @override
  String? get difficulty;

  /// Create a copy of Sentence
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$SentenceImplCopyWith<_$SentenceImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
