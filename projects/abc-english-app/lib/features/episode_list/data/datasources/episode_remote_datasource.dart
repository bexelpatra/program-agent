import 'package:dio/dio.dart';

import '../../../../core/errors/app_exception.dart';
import '../../../../core/network/dio_client.dart';
import '../models/episode_dto.dart';

/// HTTP-side of the episode list feature.
///
/// Wraps `GET /api/v1/episodes` and `GET /api/v1/episodes/{id}` and converts
/// raw [DioException]s at the boundary into the project's [AppException]
/// hierarchy. The repository above consumes only DTOs or typed exceptions —
/// never raw Dio types.
class EpisodeRemoteDataSource {
  EpisodeRemoteDataSource(this._client);

  final DioClient _client;

  /// Paginated list. Returns DTOs ordered as received from the server.
  Future<List<EpisodeDto>> fetchEpisodes({
    required int page,
    required int size,
    DateTime? sinceModified,
  }) async {
    final query = <String, dynamic>{
      'page': page,
      'size': size,
      if (sinceModified != null)
        'since_modified': sinceModified.toUtc().toIso8601String(),
    };

    try {
      final response = await _client.raw.get<Map<String, dynamic>>(
        '/api/v1/episodes',
        queryParameters: query,
      );
      final data = response.data ?? const <String, dynamic>{};
      final rawList = (data['episodes'] as List?) ?? const [];
      return rawList
          .whereType<Map<String, dynamic>>()
          .map(EpisodeDto.fromJson)
          .toList(growable: false);
    } on DioException catch (error) {
      throw _unwrapDioException(error);
    }
  }

  /// Single-row fetch. 404 → [NotFoundException].
  Future<EpisodeDto> fetchById(String id) async {
    try {
      final response = await _client.raw.get<Map<String, dynamic>>(
        '/api/v1/episodes/$id',
      );
      final data = response.data;
      if (data == null) {
        throw NotFoundException('episode $id: empty body');
      }
      return EpisodeDto.fromJson(data);
    } on DioException catch (error) {
      throw _unwrapDioException(error);
    }
  }

  /// [DioClient._errorMappingInterceptor] wraps the real [AppException] in
  /// [DioException.error]; unwrap it here for clean propagation.
  AppException _unwrapDioException(DioException error) {
    final mapped = error.error;
    if (mapped is AppException) {
      return mapped;
    }
    return UnknownException(error.message ?? 'HTTP error', cause: error);
  }
}
