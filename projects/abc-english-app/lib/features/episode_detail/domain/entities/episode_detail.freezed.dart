// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'episode_detail.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

/// @nodoc
mixin _$EpisodeDetail {
  Episode get episode => throw _privateConstructorUsedError;
  List<Sentence> get sentences => throw _privateConstructorUsedError;

  /// Create a copy of EpisodeDetail
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $EpisodeDetailCopyWith<EpisodeDetail> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $EpisodeDetailCopyWith<$Res> {
  factory $EpisodeDetailCopyWith(
    EpisodeDetail value,
    $Res Function(EpisodeDetail) then,
  ) = _$EpisodeDetailCopyWithImpl<$Res, EpisodeDetail>;
  @useResult
  $Res call({Episode episode, List<Sentence> sentences});

  $EpisodeCopyWith<$Res> get episode;
}

/// @nodoc
class _$EpisodeDetailCopyWithImpl<$Res, $Val extends EpisodeDetail>
    implements $EpisodeDetailCopyWith<$Res> {
  _$EpisodeDetailCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of EpisodeDetail
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({Object? episode = null, Object? sentences = null}) {
    return _then(
      _value.copyWith(
            episode: null == episode
                ? _value.episode
                : episode // ignore: cast_nullable_to_non_nullable
                      as Episode,
            sentences: null == sentences
                ? _value.sentences
                : sentences // ignore: cast_nullable_to_non_nullable
                      as List<Sentence>,
          )
          as $Val,
    );
  }

  /// Create a copy of EpisodeDetail
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $EpisodeCopyWith<$Res> get episode {
    return $EpisodeCopyWith<$Res>(_value.episode, (value) {
      return _then(_value.copyWith(episode: value) as $Val);
    });
  }
}

/// @nodoc
abstract class _$$EpisodeDetailImplCopyWith<$Res>
    implements $EpisodeDetailCopyWith<$Res> {
  factory _$$EpisodeDetailImplCopyWith(
    _$EpisodeDetailImpl value,
    $Res Function(_$EpisodeDetailImpl) then,
  ) = __$$EpisodeDetailImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({Episode episode, List<Sentence> sentences});

  @override
  $EpisodeCopyWith<$Res> get episode;
}

/// @nodoc
class __$$EpisodeDetailImplCopyWithImpl<$Res>
    extends _$EpisodeDetailCopyWithImpl<$Res, _$EpisodeDetailImpl>
    implements _$$EpisodeDetailImplCopyWith<$Res> {
  __$$EpisodeDetailImplCopyWithImpl(
    _$EpisodeDetailImpl _value,
    $Res Function(_$EpisodeDetailImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of EpisodeDetail
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({Object? episode = null, Object? sentences = null}) {
    return _then(
      _$EpisodeDetailImpl(
        episode: null == episode
            ? _value.episode
            : episode // ignore: cast_nullable_to_non_nullable
                  as Episode,
        sentences: null == sentences
            ? _value._sentences
            : sentences // ignore: cast_nullable_to_non_nullable
                  as List<Sentence>,
      ),
    );
  }
}

/// @nodoc

class _$EpisodeDetailImpl implements _EpisodeDetail {
  const _$EpisodeDetailImpl({
    required this.episode,
    required final List<Sentence> sentences,
  }) : _sentences = sentences;

  @override
  final Episode episode;
  final List<Sentence> _sentences;
  @override
  List<Sentence> get sentences {
    if (_sentences is EqualUnmodifiableListView) return _sentences;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_sentences);
  }

  @override
  String toString() {
    return 'EpisodeDetail(episode: $episode, sentences: $sentences)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$EpisodeDetailImpl &&
            (identical(other.episode, episode) || other.episode == episode) &&
            const DeepCollectionEquality().equals(
              other._sentences,
              _sentences,
            ));
  }

  @override
  int get hashCode => Object.hash(
    runtimeType,
    episode,
    const DeepCollectionEquality().hash(_sentences),
  );

  /// Create a copy of EpisodeDetail
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$EpisodeDetailImplCopyWith<_$EpisodeDetailImpl> get copyWith =>
      __$$EpisodeDetailImplCopyWithImpl<_$EpisodeDetailImpl>(this, _$identity);
}

abstract class _EpisodeDetail implements EpisodeDetail {
  const factory _EpisodeDetail({
    required final Episode episode,
    required final List<Sentence> sentences,
  }) = _$EpisodeDetailImpl;

  @override
  Episode get episode;
  @override
  List<Sentence> get sentences;

  /// Create a copy of EpisodeDetail
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$EpisodeDetailImplCopyWith<_$EpisodeDetailImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
