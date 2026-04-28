// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'playback_source.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

/// @nodoc
mixin _$PlaybackSource {
  @optionalTypeArgs
  TResult when<TResult extends Object?>({
    required TResult Function(String path) local,
    required TResult Function(String url) streaming,
    required TResult Function() none,
  }) => throw _privateConstructorUsedError;
  @optionalTypeArgs
  TResult? whenOrNull<TResult extends Object?>({
    TResult? Function(String path)? local,
    TResult? Function(String url)? streaming,
    TResult? Function()? none,
  }) => throw _privateConstructorUsedError;
  @optionalTypeArgs
  TResult maybeWhen<TResult extends Object?>({
    TResult Function(String path)? local,
    TResult Function(String url)? streaming,
    TResult Function()? none,
    required TResult orElse(),
  }) => throw _privateConstructorUsedError;
  @optionalTypeArgs
  TResult map<TResult extends Object?>({
    required TResult Function(LocalSource value) local,
    required TResult Function(StreamingSource value) streaming,
    required TResult Function(NoSource value) none,
  }) => throw _privateConstructorUsedError;
  @optionalTypeArgs
  TResult? mapOrNull<TResult extends Object?>({
    TResult? Function(LocalSource value)? local,
    TResult? Function(StreamingSource value)? streaming,
    TResult? Function(NoSource value)? none,
  }) => throw _privateConstructorUsedError;
  @optionalTypeArgs
  TResult maybeMap<TResult extends Object?>({
    TResult Function(LocalSource value)? local,
    TResult Function(StreamingSource value)? streaming,
    TResult Function(NoSource value)? none,
    required TResult orElse(),
  }) => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PlaybackSourceCopyWith<$Res> {
  factory $PlaybackSourceCopyWith(
    PlaybackSource value,
    $Res Function(PlaybackSource) then,
  ) = _$PlaybackSourceCopyWithImpl<$Res, PlaybackSource>;
}

/// @nodoc
class _$PlaybackSourceCopyWithImpl<$Res, $Val extends PlaybackSource>
    implements $PlaybackSourceCopyWith<$Res> {
  _$PlaybackSourceCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of PlaybackSource
  /// with the given fields replaced by the non-null parameter values.
}

/// @nodoc
abstract class _$$LocalSourceImplCopyWith<$Res> {
  factory _$$LocalSourceImplCopyWith(
    _$LocalSourceImpl value,
    $Res Function(_$LocalSourceImpl) then,
  ) = __$$LocalSourceImplCopyWithImpl<$Res>;
  @useResult
  $Res call({String path});
}

/// @nodoc
class __$$LocalSourceImplCopyWithImpl<$Res>
    extends _$PlaybackSourceCopyWithImpl<$Res, _$LocalSourceImpl>
    implements _$$LocalSourceImplCopyWith<$Res> {
  __$$LocalSourceImplCopyWithImpl(
    _$LocalSourceImpl _value,
    $Res Function(_$LocalSourceImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of PlaybackSource
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({Object? path = null}) {
    return _then(
      _$LocalSourceImpl(
        path: null == path
            ? _value.path
            : path // ignore: cast_nullable_to_non_nullable
                  as String,
      ),
    );
  }
}

/// @nodoc

class _$LocalSourceImpl implements LocalSource {
  const _$LocalSourceImpl({required this.path});

  @override
  final String path;

  @override
  String toString() {
    return 'PlaybackSource.local(path: $path)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$LocalSourceImpl &&
            (identical(other.path, path) || other.path == path));
  }

  @override
  int get hashCode => Object.hash(runtimeType, path);

  /// Create a copy of PlaybackSource
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$LocalSourceImplCopyWith<_$LocalSourceImpl> get copyWith =>
      __$$LocalSourceImplCopyWithImpl<_$LocalSourceImpl>(this, _$identity);

  @override
  @optionalTypeArgs
  TResult when<TResult extends Object?>({
    required TResult Function(String path) local,
    required TResult Function(String url) streaming,
    required TResult Function() none,
  }) {
    return local(path);
  }

  @override
  @optionalTypeArgs
  TResult? whenOrNull<TResult extends Object?>({
    TResult? Function(String path)? local,
    TResult? Function(String url)? streaming,
    TResult? Function()? none,
  }) {
    return local?.call(path);
  }

  @override
  @optionalTypeArgs
  TResult maybeWhen<TResult extends Object?>({
    TResult Function(String path)? local,
    TResult Function(String url)? streaming,
    TResult Function()? none,
    required TResult orElse(),
  }) {
    if (local != null) {
      return local(path);
    }
    return orElse();
  }

  @override
  @optionalTypeArgs
  TResult map<TResult extends Object?>({
    required TResult Function(LocalSource value) local,
    required TResult Function(StreamingSource value) streaming,
    required TResult Function(NoSource value) none,
  }) {
    return local(this);
  }

  @override
  @optionalTypeArgs
  TResult? mapOrNull<TResult extends Object?>({
    TResult? Function(LocalSource value)? local,
    TResult? Function(StreamingSource value)? streaming,
    TResult? Function(NoSource value)? none,
  }) {
    return local?.call(this);
  }

  @override
  @optionalTypeArgs
  TResult maybeMap<TResult extends Object?>({
    TResult Function(LocalSource value)? local,
    TResult Function(StreamingSource value)? streaming,
    TResult Function(NoSource value)? none,
    required TResult orElse(),
  }) {
    if (local != null) {
      return local(this);
    }
    return orElse();
  }
}

abstract class LocalSource implements PlaybackSource {
  const factory LocalSource({required final String path}) = _$LocalSourceImpl;

  String get path;

  /// Create a copy of PlaybackSource
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$LocalSourceImplCopyWith<_$LocalSourceImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class _$$StreamingSourceImplCopyWith<$Res> {
  factory _$$StreamingSourceImplCopyWith(
    _$StreamingSourceImpl value,
    $Res Function(_$StreamingSourceImpl) then,
  ) = __$$StreamingSourceImplCopyWithImpl<$Res>;
  @useResult
  $Res call({String url});
}

/// @nodoc
class __$$StreamingSourceImplCopyWithImpl<$Res>
    extends _$PlaybackSourceCopyWithImpl<$Res, _$StreamingSourceImpl>
    implements _$$StreamingSourceImplCopyWith<$Res> {
  __$$StreamingSourceImplCopyWithImpl(
    _$StreamingSourceImpl _value,
    $Res Function(_$StreamingSourceImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of PlaybackSource
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({Object? url = null}) {
    return _then(
      _$StreamingSourceImpl(
        url: null == url
            ? _value.url
            : url // ignore: cast_nullable_to_non_nullable
                  as String,
      ),
    );
  }
}

/// @nodoc

class _$StreamingSourceImpl implements StreamingSource {
  const _$StreamingSourceImpl({required this.url});

  @override
  final String url;

  @override
  String toString() {
    return 'PlaybackSource.streaming(url: $url)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$StreamingSourceImpl &&
            (identical(other.url, url) || other.url == url));
  }

  @override
  int get hashCode => Object.hash(runtimeType, url);

  /// Create a copy of PlaybackSource
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$StreamingSourceImplCopyWith<_$StreamingSourceImpl> get copyWith =>
      __$$StreamingSourceImplCopyWithImpl<_$StreamingSourceImpl>(
        this,
        _$identity,
      );

  @override
  @optionalTypeArgs
  TResult when<TResult extends Object?>({
    required TResult Function(String path) local,
    required TResult Function(String url) streaming,
    required TResult Function() none,
  }) {
    return streaming(url);
  }

  @override
  @optionalTypeArgs
  TResult? whenOrNull<TResult extends Object?>({
    TResult? Function(String path)? local,
    TResult? Function(String url)? streaming,
    TResult? Function()? none,
  }) {
    return streaming?.call(url);
  }

  @override
  @optionalTypeArgs
  TResult maybeWhen<TResult extends Object?>({
    TResult Function(String path)? local,
    TResult Function(String url)? streaming,
    TResult Function()? none,
    required TResult orElse(),
  }) {
    if (streaming != null) {
      return streaming(url);
    }
    return orElse();
  }

  @override
  @optionalTypeArgs
  TResult map<TResult extends Object?>({
    required TResult Function(LocalSource value) local,
    required TResult Function(StreamingSource value) streaming,
    required TResult Function(NoSource value) none,
  }) {
    return streaming(this);
  }

  @override
  @optionalTypeArgs
  TResult? mapOrNull<TResult extends Object?>({
    TResult? Function(LocalSource value)? local,
    TResult? Function(StreamingSource value)? streaming,
    TResult? Function(NoSource value)? none,
  }) {
    return streaming?.call(this);
  }

  @override
  @optionalTypeArgs
  TResult maybeMap<TResult extends Object?>({
    TResult Function(LocalSource value)? local,
    TResult Function(StreamingSource value)? streaming,
    TResult Function(NoSource value)? none,
    required TResult orElse(),
  }) {
    if (streaming != null) {
      return streaming(this);
    }
    return orElse();
  }
}

abstract class StreamingSource implements PlaybackSource {
  const factory StreamingSource({required final String url}) =
      _$StreamingSourceImpl;

  String get url;

  /// Create a copy of PlaybackSource
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$StreamingSourceImplCopyWith<_$StreamingSourceImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class _$$NoSourceImplCopyWith<$Res> {
  factory _$$NoSourceImplCopyWith(
    _$NoSourceImpl value,
    $Res Function(_$NoSourceImpl) then,
  ) = __$$NoSourceImplCopyWithImpl<$Res>;
}

/// @nodoc
class __$$NoSourceImplCopyWithImpl<$Res>
    extends _$PlaybackSourceCopyWithImpl<$Res, _$NoSourceImpl>
    implements _$$NoSourceImplCopyWith<$Res> {
  __$$NoSourceImplCopyWithImpl(
    _$NoSourceImpl _value,
    $Res Function(_$NoSourceImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of PlaybackSource
  /// with the given fields replaced by the non-null parameter values.
}

/// @nodoc

class _$NoSourceImpl implements NoSource {
  const _$NoSourceImpl();

  @override
  String toString() {
    return 'PlaybackSource.none()';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType && other is _$NoSourceImpl);
  }

  @override
  int get hashCode => runtimeType.hashCode;

  @override
  @optionalTypeArgs
  TResult when<TResult extends Object?>({
    required TResult Function(String path) local,
    required TResult Function(String url) streaming,
    required TResult Function() none,
  }) {
    return none();
  }

  @override
  @optionalTypeArgs
  TResult? whenOrNull<TResult extends Object?>({
    TResult? Function(String path)? local,
    TResult? Function(String url)? streaming,
    TResult? Function()? none,
  }) {
    return none?.call();
  }

  @override
  @optionalTypeArgs
  TResult maybeWhen<TResult extends Object?>({
    TResult Function(String path)? local,
    TResult Function(String url)? streaming,
    TResult Function()? none,
    required TResult orElse(),
  }) {
    if (none != null) {
      return none();
    }
    return orElse();
  }

  @override
  @optionalTypeArgs
  TResult map<TResult extends Object?>({
    required TResult Function(LocalSource value) local,
    required TResult Function(StreamingSource value) streaming,
    required TResult Function(NoSource value) none,
  }) {
    return none(this);
  }

  @override
  @optionalTypeArgs
  TResult? mapOrNull<TResult extends Object?>({
    TResult? Function(LocalSource value)? local,
    TResult? Function(StreamingSource value)? streaming,
    TResult? Function(NoSource value)? none,
  }) {
    return none?.call(this);
  }

  @override
  @optionalTypeArgs
  TResult maybeMap<TResult extends Object?>({
    TResult Function(LocalSource value)? local,
    TResult Function(StreamingSource value)? streaming,
    TResult Function(NoSource value)? none,
    required TResult orElse(),
  }) {
    if (none != null) {
      return none(this);
    }
    return orElse();
  }
}

abstract class NoSource implements PlaybackSource {
  const factory NoSource() = _$NoSourceImpl;
}
