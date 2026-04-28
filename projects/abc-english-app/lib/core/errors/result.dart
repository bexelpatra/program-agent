import 'app_exception.dart';

/// Sealed `Result<T>` — carries either a [Success] value or a [Failure] with
/// an [AppException]. Used as the return type of every UseCase.
///
/// UseCases never throw; they always return `Result<T>`. Presentation layer
/// uses [when] to render success/failure states.
sealed class Result<T> {
  const Result();

  /// Pattern-match on success/failure.
  R when<R>({
    required R Function(T value) success,
    required R Function(AppException error) failure,
  }) {
    final self = this;
    if (self is Success<T>) {
      return success(self.value);
    }
    return failure((self as Failure<T>).error);
  }

  bool get isSuccess => this is Success<T>;
  bool get isFailure => this is Failure<T>;
}

class Success<T> extends Result<T> {
  const Success(this.value);
  final T value;
}

class Failure<T> extends Result<T> {
  const Failure(this.error);
  final AppException error;
}
