import 'package:dio/dio.dart';

import '../../../../core/errors/app_exception.dart';
import '../../../../core/network/dio_client.dart';
import '../models/episode_detail_dto.dart';

/// HTTP-side of the episode detail feature. Wraps
/// `GET /api/v1/episodes/{id}`.
class EpisodeDetailRemoteDataSource {
  EpisodeDetailRemoteDataSource(this._client);

  final DioClient _client;

  Future<EpisodeDetailDto> fetchDetail(String id) async {
    try {
      final response = await _client.raw.get<Map<String, dynamic>>(
        '/api/v1/episodes/$id',
      );
      final data = response.data;
      if (data == null) {
        throw NotFoundException('episode $id: empty body');
      }
      return EpisodeDetailDto.fromJson(data);
    } on DioException catch (error) {
      throw _unwrapDioException(error);
    }
  }

  AppException _unwrapDioException(DioException error) {
    final mapped = error.error;
    if (mapped is AppException) {
      return mapped;
    }
    return UnknownException(error.message ?? 'HTTP error', cause: error);
  }
}
