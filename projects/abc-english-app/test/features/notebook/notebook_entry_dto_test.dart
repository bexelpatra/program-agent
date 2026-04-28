import 'package:abc_english_app/features/notebook/data/models/notebook_entry_dto.dart';
import 'package:abc_english_app/features/notebook/domain/entities/sync_status.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('NotebookEntryDto.fromJson', () {
    test('parses the v1 wire shape, snake_case → camelCase', () {
      final dto = NotebookEntryDto.fromJson(const <String, dynamic>{
        'id': 'nb-1',
        'word': 'albeit',
        'context': 'Albeit briefly',
        'episode_id': 'ep-1',
        'sentence_index': 3,
        'meaning': '비록 ~일지라도',
        'note': 'connector',
        'created_at': '2026-04-05T10:00:00Z',
        'last_modified': '2026-04-05T12:00:00Z',
      });
      expect(dto.id, 'nb-1');
      expect(dto.episodeId, 'ep-1');
      expect(dto.sentenceIndex, 3);
      expect(dto.lastModified, '2026-04-05T12:00:00Z');
    });

    test('defaults context to empty string', () {
      final dto = NotebookEntryDto.fromJson(const <String, dynamic>{
        'id': 'nb-2',
        'word': 'x',
      });
      expect(dto.context, '');
    });
  });

  group('NotebookEntryDto.toEntity', () {
    test('marks fresh wire entries as synced', () {
      final dto = NotebookEntryDto.fromJson(const <String, dynamic>{
        'id': 'nb-3',
        'word': 'w',
        'context': 'c',
        'created_at': '2026-04-05T10:00:00Z',
        'last_modified': '2026-04-05T12:00:00Z',
      });
      final e = dto.toEntity();
      expect(e.syncStatus, SyncStatus.synced);
      expect(e.id, 'nb-3');
    });

    test('empty strings in optional fields collapse to null', () {
      final dto = NotebookEntryDto.fromJson(const <String, dynamic>{
        'id': 'nb-4',
        'word': 'w',
        'episode_id': '',
        'meaning': '',
        'note': '',
      });
      final e = dto.toEntity();
      expect(e.episodeId, isNull);
      expect(e.meaning, isNull);
      expect(e.note, isNull);
    });

    test('missing timestamps fall back to current UTC', () {
      final dto = NotebookEntryDto.fromJson(const <String, dynamic>{
        'id': 'nb-5',
        'word': 'w',
      });
      final before = DateTime.now().toUtc().subtract(const Duration(seconds: 2));
      final e = dto.toEntity();
      final after = DateTime.now().toUtc().add(const Duration(seconds: 2));
      expect(e.lastModified.isAfter(before), isTrue);
      expect(e.lastModified.isBefore(after), isTrue);
      expect(e.createdAt, e.lastModified);
    });
  });
}
