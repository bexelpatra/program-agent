import 'package:abc_english_app/features/episode_detail/data/models/episode_detail_dto.dart';
import 'package:abc_english_app/features/episode_detail/data/models/sentence_dto.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('SentenceDto.fromJson / toEntity', () {
    test('parses `start_ms`/`end_ms` (snake_case) into the entity', () {
      final dto = SentenceDto.fromJson(const <String, dynamic>{
        'index': 3,
        'text': 'Hello world',
        'start_ms': 1500,
        'end_ms': 2500,
        'wer': 0.05,
        'difficulty': 'B1',
      });
      expect(dto.startMs, 1500);
      expect(dto.endMs, 2500);
      final e = dto.toEntity();
      expect(e.index, 3);
      expect(e.text, 'Hello world');
      expect(e.startMs, 1500);
      expect(e.endMs, 2500);
      expect(e.wer, closeTo(0.05, 1e-9));
      expect(e.difficulty, 'B1');
    });

    test('missing start_ms/end_ms → 0 (documented default)', () {
      final dto = SentenceDto.fromJson(const <String, dynamic>{
        'index': 0,
        'text': 'x',
      });
      final e = dto.toEntity();
      expect(e.startMs, 0);
      expect(e.endMs, 0);
    });
  });

  group('EpisodeDetailDto.fromJson', () {
    test('parses the full shape including sentences', () {
      final dto = EpisodeDetailDto.fromJson(const <String, dynamic>{
        'id': 'ep-1',
        'title': 'Detail',
        'published_date': '2026-04-05',
        'duration': 300,
        'last_modified': '2026-04-06T12:00:00Z',
        'sentences': [
          {
            'index': 0,
            'text': 'One',
            'start_ms': 0,
            'end_ms': 1000,
          },
          {
            'index': 1,
            'text': 'Two',
            'start_ms': 1000,
            'end_ms': 2000,
          },
        ],
      });
      expect(dto.id, 'ep-1');
      expect(dto.sentences, hasLength(2));
    });

    test('sentences defaults to empty list when absent', () {
      final dto = EpisodeDetailDto.fromJson(const <String, dynamic>{
        'id': 'ep-2',
        'title': 'No sents',
        'published_date': '2026-04-05',
      });
      expect(dto.sentences, isEmpty);
    });
  });

  group('EpisodeDetailDto.toEntity', () {
    test('converts seconds → ms, merges local download state, maps sentences',
        () {
      final dto = EpisodeDetailDto.fromJson(const <String, dynamic>{
        'id': 'ep-3',
        'title': 'Merge',
        'published_date': '2026-04-07',
        'duration': 180,
        'sentences': [
          {
            'index': 0,
            'text': 'hi',
            'start_ms': 0,
            'end_ms': 500,
          },
        ],
      });
      final detail = dto.toEntity(
        isDownloaded: true,
        audioLocalPath: '/x.mp3',
      );
      expect(detail.episode.durationMs, 180 * 1000);
      expect(detail.episode.isDownloaded, isTrue);
      expect(detail.episode.audioLocalPath, '/x.mp3');
      expect(detail.sentences, hasLength(1));
      expect(detail.sentences.single.text, 'hi');
    });

    test('missing last_modified falls back to publishedDate', () {
      final dto = EpisodeDetailDto.fromJson(const <String, dynamic>{
        'id': 'ep-4',
        'title': 'No LM',
        'published_date': '2026-04-08',
      });
      final d = dto.toEntity();
      expect(d.episode.lastModified, d.episode.publishedDate);
    });
  });
}
