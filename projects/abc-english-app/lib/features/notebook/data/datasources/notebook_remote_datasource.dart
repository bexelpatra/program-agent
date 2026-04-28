import 'package:dio/dio.dart';

import '../../../../core/errors/app_exception.dart';
import '../../../../core/network/dio_client.dart';
import '../models/notebook_entry_dto.dart';

/// HTTP-side of the notebook feature. Wraps `/api/v1/notebook` CRUD plus
/// `/api/v1/notebook/sync`.
///
/// The sync endpoint is exposed on this datasource for future use by a
/// dedicated sync engine; the repository in this task only uses the CRUD
/// calls.
class NotebookRemoteDataSource {
  NotebookRemoteDataSource(this._client);

  final DioClient _client;

  Future<List<NotebookEntryDto>> list({
    int page = 1,
    int size = 100,
    DateTime? sinceModified,
  }) async {
    try {
      final response = await _client.raw.get<Map<String, dynamic>>(
        '/api/v1/notebook',
        queryParameters: <String, dynamic>{
          'page': page,
          'size': size,
          if (sinceModified != null)
            'since_modified': sinceModified.toUtc().toIso8601String(),
        },
      );
      final data = response.data ?? const <String, dynamic>{};
      final raw = (data['entries'] as List?) ?? const [];
      return raw
          .whereType<Map<String, dynamic>>()
          .map(NotebookEntryDto.fromJson)
          .toList(growable: false);
    } on DioException catch (error) {
      throw _unwrapDioException(error);
    }
  }

  Future<NotebookEntryDto> create({
    required String word,
    required String context,
    String? episodeId,
    int? sentenceIndex,
    String? meaning,
    String? note,
  }) async {
    try {
      final response = await _client.raw.post<Map<String, dynamic>>(
        '/api/v1/notebook',
        data: <String, dynamic>{
          'word': word,
          'context': context,
          'episode_id': ?episodeId,
          'sentence_index': ?sentenceIndex,
          'meaning': ?meaning,
          'note': ?note,
        },
      );
      final body = response.data;
      if (body == null) {
        throw const UnknownException('notebook create: empty body');
      }
      return NotebookEntryDto.fromJson(body);
    } on DioException catch (error) {
      throw _unwrapDioException(error);
    }
  }

  Future<NotebookEntryDto> patch({
    required String id,
    String? word,
    String? context,
    String? episodeId,
    int? sentenceIndex,
    String? meaning,
    String? note,
  }) async {
    final payload = <String, dynamic>{
      'word': ?word,
      'context': ?context,
      'episode_id': ?episodeId,
      'sentence_index': ?sentenceIndex,
      'meaning': ?meaning,
      'note': ?note,
    };
    try {
      final response = await _client.raw.patch<Map<String, dynamic>>(
        '/api/v1/notebook/$id',
        data: payload,
      );
      final body = response.data;
      if (body == null) {
        throw NotFoundException('notebook patch $id: empty body');
      }
      return NotebookEntryDto.fromJson(body);
    } on DioException catch (error) {
      throw _unwrapDioException(error);
    }
  }

  Future<void> delete(String id) async {
    try {
      await _client.raw.delete<void>('/api/v1/notebook/$id');
    } on DioException catch (error) {
      throw _unwrapDioException(error);
    }
  }

  /// Batch upload offline changes. Each [NotebookSyncChange] is either an
  /// upsert (payload required) or a delete (id required). The server
  /// returns one [NotebookSyncResult] per change with the LWW outcome.
  Future<List<NotebookSyncResult>> syncBatch(
    List<NotebookSyncChange> changes,
  ) async {
    if (changes.isEmpty) {
      return const <NotebookSyncResult>[];
    }
    try {
      final response = await _client.raw.post<Map<String, dynamic>>(
        '/api/v1/notebook/sync',
        data: <String, dynamic>{
          'changes': changes.map((c) => c.toJson()).toList(growable: false),
        },
      );
      final data = response.data ?? const <String, dynamic>{};
      final raw = (data['results'] as List?) ?? const [];
      return raw
          .whereType<Map<String, dynamic>>()
          .map(NotebookSyncResult.fromJson)
          .toList(growable: false);
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

/// One intent in a batch `/sync` request — upsert or delete.
class NotebookSyncChange {
  const NotebookSyncChange.upsert({
    required this.id,
    required NotebookEntryDto payload,
    required DateTime clientLastModified,
  })  : op = 'upsert',
        _payload = payload,
        _clientLastModified = clientLastModified;

  const NotebookSyncChange.delete({
    required this.id,
    required DateTime clientLastModified,
  })  : op = 'delete',
        _payload = null,
        _clientLastModified = clientLastModified;

  final String id;
  final String op;
  final NotebookEntryDto? _payload;
  final DateTime _clientLastModified;

  Map<String, dynamic> toJson() {
    return <String, dynamic>{
      'id': id,
      'op': op,
      if (_payload != null) 'payload': _payload.toJson(),
      'client_last_modified': _clientLastModified.toUtc().toIso8601String(),
    };
  }
}

/// Per-change result from `/api/v1/notebook/sync`. Mirrors the server's
/// `SyncResult` model.
class NotebookSyncResult {
  const NotebookSyncResult({
    required this.id,
    required this.status,
    this.serverLastModified,
    this.detail,
  });

  final String? id;
  final NotebookSyncStatus status;
  final DateTime? serverLastModified;
  final String? detail;

  static NotebookSyncResult fromJson(Map<String, dynamic> json) {
    final rawStatus = json['status'] as String?;
    final rawModified = json['server_last_modified'] as String?;
    return NotebookSyncResult(
      id: json['id'] as String?,
      status: _parseStatus(rawStatus),
      serverLastModified:
          rawModified == null || rawModified.isEmpty
              ? null
              : DateTime.parse(rawModified),
      detail: json['detail'] as String?,
    );
  }

  static NotebookSyncStatus _parseStatus(String? raw) {
    switch (raw) {
      case 'applied':
        return NotebookSyncStatus.applied;
      case 'server_wins':
        return NotebookSyncStatus.serverWins;
      case 'not_found':
        return NotebookSyncStatus.notFound;
      case 'error':
        return NotebookSyncStatus.error;
      default:
        return NotebookSyncStatus.error;
    }
  }
}

/// Outcome values the server returns per sync change.
enum NotebookSyncStatus { applied, serverWins, notFound, error }
