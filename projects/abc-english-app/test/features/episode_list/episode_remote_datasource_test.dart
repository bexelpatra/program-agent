import 'dart:convert';
import 'dart:typed_data';

import 'package:abc_english_app/core/config/app_config.dart';
import 'package:abc_english_app/core/errors/app_exception.dart';
import 'package:abc_english_app/core/network/dio_client.dart';
import 'package:abc_english_app/features/episode_list/data/datasources/episode_remote_datasource.dart';
import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';

/// Minimal scripted adapter — pops the next planned response per request.
class _ScriptedAdapter implements HttpClientAdapter {
  _ScriptedAdapter(this._plan);

  final List<_Planned> _plan;
  final List<RequestOptions> requests = <RequestOptions>[];
  int _idx = 0;

  @override
  Future<ResponseBody> fetch(
    RequestOptions options,
    Stream<Uint8List>? requestStream,
    Future<dynamic>? cancelFuture,
  ) async {
    requests.add(options);
    if (_idx >= _plan.length) {
      throw StateError('adapter exhausted');
    }
    return _plan[_idx++].execute();
  }

  @override
  void close({bool force = false}) {}
}

sealed class _Planned {
  Future<ResponseBody> execute();
}

class _Ok extends _Planned {
  _Ok(this.body, {this.status = 200});
  final Map<String, dynamic> body;
  final int status;
  @override
  Future<ResponseBody> execute() async {
    return ResponseBody.fromBytes(
      utf8.encode(jsonEncode(body)),
      status,
      headers: const {
        'content-type': ['application/json'],
      },
    );
  }
}

AppConfig _cfg() => AppConfig(
      apiBaseUrl: 'https://example.test',
      apiToken: 'tok',
      env: AppEnv.dev,
    );

DioClient _client(_ScriptedAdapter adapter) {
  final c = DioClient(_cfg());
  c.raw.httpClientAdapter = adapter;
  return c;
}

void main() {
  group('EpisodeRemoteDataSource.fetchEpisodes', () {
    test('parses the `episodes` list and sends pagination params', () async {
      final adapter = _ScriptedAdapter([
        _Ok({
          'episodes': [
            {
              'id': 'ep-1',
              'title': 'A',
              'published_date': '2026-04-01',
              'duration': 60,
            },
            {
              'id': 'ep-2',
              'title': 'B',
              'published_date': '2026-04-02',
              'duration': 120,
            },
          ],
        }),
      ]);
      final ds = EpisodeRemoteDataSource(_client(adapter));

      final dtos = await ds.fetchEpisodes(page: 2, size: 10);
      expect(dtos, hasLength(2));
      expect(dtos.first.id, 'ep-1');

      final req = adapter.requests.single;
      expect(req.path, '/api/v1/episodes');
      expect(req.queryParameters['page'], 2);
      expect(req.queryParameters['size'], 10);
    });

    test('forwards since_modified as ISO8601 UTC', () async {
      final adapter = _ScriptedAdapter([
        _Ok(const {'episodes': []}),
      ]);
      final ds = EpisodeRemoteDataSource(_client(adapter));
      await ds.fetchEpisodes(
        page: 1,
        size: 20,
        sinceModified: DateTime.utc(2026, 4, 3, 12),
      );
      final since =
          adapter.requests.single.queryParameters['since_modified'] as String;
      expect(since, startsWith('2026-04-03T12:00:00'));
    });

    test('empty `episodes` → empty list', () async {
      final adapter = _ScriptedAdapter([
        _Ok(const {'episodes': []}),
      ]);
      final ds = EpisodeRemoteDataSource(_client(adapter));
      final dtos = await ds.fetchEpisodes(page: 1, size: 20);
      expect(dtos, isEmpty);
    });

    test('missing body → empty list (defensive)', () async {
      final adapter = _ScriptedAdapter([
        _Ok(const <String, dynamic>{}),
      ]);
      final ds = EpisodeRemoteDataSource(_client(adapter));
      final dtos = await ds.fetchEpisodes(page: 1, size: 20);
      expect(dtos, isEmpty);
    });

    test('404 → NotFoundException (unwrapped from DioException)', () async {
      final adapter = _ScriptedAdapter([
        _Ok(const {'detail': 'missing'}, status: 404),
      ]);
      final ds = EpisodeRemoteDataSource(_client(adapter));
      expect(
        () => ds.fetchEpisodes(page: 1, size: 20),
        throwsA(isA<NotFoundException>()),
      );
    });

    test('401 → UnauthorizedException (unwrapped from DioException)',
        () async {
      final adapter = _ScriptedAdapter([
        _Ok(const {'detail': 'no token'}, status: 401),
      ]);
      final ds = EpisodeRemoteDataSource(_client(adapter));
      expect(
        () => ds.fetchEpisodes(page: 1, size: 20),
        throwsA(isA<UnauthorizedException>()),
      );
    });
  });

  group('EpisodeRemoteDataSource.fetchById', () {
    test('parses the single-row response', () async {
      final adapter = _ScriptedAdapter([
        _Ok({
          'id': 'ep-9',
          'title': 'Solo',
          'published_date': '2026-04-07',
          'duration': 90,
        }),
      ]);
      final ds = EpisodeRemoteDataSource(_client(adapter));
      final dto = await ds.fetchById('ep-9');
      expect(dto.id, 'ep-9');
      expect(adapter.requests.single.path, '/api/v1/episodes/ep-9');
    });

    test('404 → NotFoundException', () async {
      final adapter = _ScriptedAdapter([
        _Ok(const {'detail': 'no'}, status: 404),
      ]);
      final ds = EpisodeRemoteDataSource(_client(adapter));
      expect(() => ds.fetchById('nope'), throwsA(isA<NotFoundException>()));
    });
  });
}
