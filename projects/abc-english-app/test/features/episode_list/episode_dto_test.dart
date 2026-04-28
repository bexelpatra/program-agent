import 'package:abc_english_app/features/episode_list/data/models/episode_dto.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('EpisodeDto.fromJson', () {
    test('parses the v1 wire shape', () {
      final dto = EpisodeDto.fromJson(const <String, dynamic>{
        'id': 'ep-1',
        'title': 'Morning News',
        'published_date': '2026-04-01',
        'duration': 360,
        'avg_wer': 0.12,
        'last_modified': '2026-04-02T10:00:00Z',
      });
      expect(dto.id, 'ep-1');
      expect(dto.title, 'Morning News');
      expect(dto.publishedDate, '2026-04-01');
      expect(dto.durationSeconds, 360);
      expect(dto.avgWer, closeTo(0.12, 1e-9));
      expect(dto.lastModified, '2026-04-02T10:00:00Z');
    });

    test('tolerates missing optional fields', () {
      final dto = EpisodeDto.fromJson(const <String, dynamic>{
        'id': 'ep-2',
        'title': 'Bare',
        'published_date': '2026-04-03',
      });
      expect(dto.durationSeconds, isNull);
      expect(dto.avgWer, isNull);
      expect(dto.lastModified, isNull);
    });
  });

  group('EpisodeDto.toEntity', () {
    test('converts seconds to ms and falls back lastModified → publishedDate',
        () {
      final dto = EpisodeDto.fromJson(const <String, dynamic>{
        'id': 'ep-3',
        'title': 'No LM',
        'published_date': '2026-04-04',
        'duration': 42,
      });
      final ep = dto.toEntity();
      expect(ep.durationMs, 42 * 1000);
      expect(ep.lastModified, ep.publishedDate,
          reason: 'fallback when last_modified absent');
      expect(ep.isDownloaded, isFalse);
      expect(ep.audioLocalPath, isNull);
    });

    test('merges in local download state', () {
      final dto = EpisodeDto.fromJson(const <String, dynamic>{
        'id': 'ep-4',
        'title': 'Mergeable',
        'published_date': '2026-04-05',
        'duration': 60,
      });
      final ep = dto.toEntity(
        isDownloaded: true,
        audioLocalPath: '/tmp/ep-4.mp3',
      );
      expect(ep.isDownloaded, isTrue);
      expect(ep.audioLocalPath, '/tmp/ep-4.mp3');
    });

    test('duration defaults to 0 when missing', () {
      final dto = EpisodeDto.fromJson(const <String, dynamic>{
        'id': 'ep-5',
        'title': 'NoDur',
        'published_date': '2026-04-06',
      });
      expect(dto.toEntity().durationMs, 0);
    });
  });
}
