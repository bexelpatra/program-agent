import 'package:dio/dio.dart';

import '../../../../core/errors/app_exception.dart';
import '../models/lookup_result_dto.dart';

/// Remote data source for the `/api/v1/lookup` endpoint.
///
/// Thin pass-through over the shared [Dio] client. The `DioClient` in
/// `lib/core/network/` already wires Bearer auth + retry + error mapping,
/// so this layer mostly concerns itself with URL + query-param shaping and
/// JSON → DTO parsing.
class LookupRemoteDataSource {
  const LookupRemoteDataSource(this._dio);

  final Dio _dio;

  Future<LookupResultDto> lookup({
    required String word,
    String? context,
  }) async {
    try {
      final response = await _dio.get<Map<String, dynamic>>(
        '/api/v1/lookup',
        queryParameters: {
          'word': word,
          if (context != null && context.isNotEmpty) 'context': context,
        },
      );
      final data = response.data;
      if (data == null) {
        throw NetworkException(
          'lookup: empty response',
          statusCode: response.statusCode,
        );
      }
      return LookupResultDto.fromJson(data);
    } on DioException catch (dioError) {
      // The DioClient's errorMappingInterceptor has already converted the
      // underlying cause to an AppException and stashed it on `.error`.
      final mapped = dioError.error;
      if (mapped is AppException) {
        throw mapped;
      }
      throw NetworkException(
        'lookup: ${dioError.message ?? "unknown"}',
        cause: dioError,
        statusCode: dioError.response?.statusCode,
      );
    }
  }
}
