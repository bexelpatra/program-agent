/// Domain-level exception hierarchy used across the `data` and `domain` layers.
///
/// Raw I/O exceptions (DioException, SqliteException, SocketException, ...)
/// are caught at the data-layer boundary and converted into one of the
/// subclasses below. UseCases never see raw exceptions; they wrap these into
/// `Failure<T>` values of `Result<T>`.
sealed class AppException implements Exception {
  const AppException(this.message, {this.cause});

  final String message;
  final Object? cause;

  @override
  String toString() => '$runtimeType: $message';
}

/// Transport-level failure: timeout, DNS, refused connection, 5xx.
class NetworkException extends AppException {
  const NetworkException(super.message, {super.cause, this.statusCode});
  final int? statusCode;
}

/// HTTP 404 or local record missing.
class NotFoundException extends AppException {
  const NotFoundException(super.message, {super.cause});
}

/// HTTP 401/403 — bearer token invalid, expired, or missing.
class UnauthorizedException extends AppException {
  const UnauthorizedException(super.message, {super.cause});
}

/// Local persistence failure: drift/sqlite error, file IO error,
/// unavailable external storage, corruption.
class StorageException extends AppException {
  const StorageException(super.message, {super.cause});
}

/// Server rejected a sync batch (e.g. schema mismatch, version skew).
class SyncConflictException extends AppException {
  const SyncConflictException(super.message, {super.cause});
}

/// Catch-all for truly unexpected failures. Should be rare in production.
class UnknownException extends AppException {
  const UnknownException(super.message, {super.cause});
}
