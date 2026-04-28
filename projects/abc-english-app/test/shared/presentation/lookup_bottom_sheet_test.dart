import 'package:abc_english_app/core/errors/app_exception.dart';
import 'package:abc_english_app/core/errors/result.dart';
import 'package:abc_english_app/features/lookup/data/repositories/lookup_repository_impl.dart';
import 'package:abc_english_app/features/lookup/domain/entities/lookup_result.dart';
import 'package:abc_english_app/features/lookup/domain/repositories/lookup_repository.dart';
import 'package:abc_english_app/shared/presentation/widgets/lookup_bottom_sheet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

/// Fake lookup repository. Returns a canned Result (or throws a delayed
/// Result) so tests can exercise loading → result and loading → error.
class _FakeLookupRepo implements LookupRepository {
  _FakeLookupRepo({
    required this.result,
    this.delay = Duration.zero,
  });

  final Result<LookupResult> result;
  final Duration delay;

  @override
  Future<Result<LookupResult>> lookup({
    required String word,
    String? context,
  }) async {
    if (delay > Duration.zero) {
      await Future<void>.delayed(delay);
    }
    return result;
  }
}

/// Records invocations of the onAddToNotebook callback so tests can
/// assert the widget forwards the expected provenance fields.
class _RecordingAdder {
  _RecordingAdder();

  final List<Map<String, Object?>> calls = [];

  Future<bool> call({
    required String word,
    required String context,
    String? episodeId,
    int? sentenceIndex,
    String? meaning,
    String? note,
  }) async {
    calls.add({
      'word': word,
      'context': context,
      'episodeId': episodeId,
      'sentenceIndex': sentenceIndex,
      'meaning': meaning,
      'note': note,
    });
    return true;
  }
}

LookupResult _ok({
  String word = 'albeit',
  List<String> definitions = const ['비록 …일지라도'],
  List<String> examples = const ['Albeit late, he arrived.'],
}) {
  return LookupResult(
    word: word,
    definitions: definitions,
    examples: examples,
  );
}

Widget _host({
  required ProviderContainer container,
  required String word,
  required String sentenceContext,
  required OnAddToNotebook onAdd,
}) {
  return UncontrolledProviderScope(
    container: container,
    child: MaterialApp(
      home: Scaffold(
        body: Builder(
          builder: (ctx) => Center(
            child: ElevatedButton(
              onPressed: () => LookupBottomSheet.show(
                ctx,
                word: word,
                context: sentenceContext,
                episodeId: 'ep-1',
                sentenceIndex: 3,
                onAddToNotebook: onAdd,
              ),
              child: const Text('open'),
            ),
          ),
        ),
      ),
    ),
  );
}

ProviderContainer _container({
  required _FakeLookupRepo lookup,
}) {
  return ProviderContainer(
    overrides: [
      lookupRepositoryProvider.overrideWithValue(lookup),
    ],
  );
}

void main() {
  testWidgets('opening the sheet shows loading then result', (tester) async {
    final lookup = _FakeLookupRepo(
      result: Success(_ok()),
      delay: const Duration(milliseconds: 80),
    );
    final adder = _RecordingAdder();
    final c = _container(lookup: lookup);
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(
      container: c,
      word: 'albeit',
      sentenceContext: 'Albeit late, he arrived.',
      onAdd: adder.call,
    ));
    await tester.pumpAndSettle();

    await tester.tap(find.text('open'));
    await tester.pump(); // open sheet
    await tester.pump(const Duration(milliseconds: 10));

    // While the lookup future hasn't completed, loading copy is visible.
    expect(find.text('조회 중...'), findsOneWidget);

    await tester.pump(const Duration(milliseconds: 100));
    await tester.pumpAndSettle();

    // Result block appears.
    expect(find.text('비록 …일지라도'), findsOneWidget);
    expect(find.byKey(const Key('lookup-add-to-notebook')), findsOneWidget);
  });

  testWidgets('"단어장에 추가" tap → onAddToNotebook called with provenance',
      (tester) async {
    final lookup = _FakeLookupRepo(result: Success(_ok()));
    final adder = _RecordingAdder();
    final c = _container(lookup: lookup);
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(
      container: c,
      word: 'albeit',
      sentenceContext: 'Albeit late, he arrived.',
      onAdd: adder.call,
    ));
    await tester.pumpAndSettle();

    await tester.tap(find.text('open'));
    await tester.pumpAndSettle();

    await tester.tap(find.byKey(const Key('lookup-add-to-notebook')));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 10));

    expect(adder.calls, hasLength(1));
    final call = adder.calls.single;
    expect(call['word'], 'albeit');
    expect(call['context'], 'Albeit late, he arrived.');
    expect(call['episodeId'], 'ep-1');
    expect(call['sentenceIndex'], 3);
    // meaning is `definitions.join('\n')` from the widget.
    expect(call['meaning'], '비록 …일지라도');
  });

  testWidgets('lookup failure → error copy visible, no notebook add button',
      (tester) async {
    final lookup = _FakeLookupRepo(
      result: const Failure<LookupResult>(NetworkException('no net')),
    );
    final adder = _RecordingAdder();
    final c = _container(lookup: lookup);
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(
      container: c,
      word: 'albeit',
      sentenceContext: 'ctx',
      onAdd: adder.call,
    ));
    await tester.pumpAndSettle();

    await tester.tap(find.text('open'));
    await tester.pumpAndSettle();

    expect(find.textContaining('네트워크 오류'), findsOneWidget);
    expect(find.text('다시 시도'), findsOneWidget);
    expect(find.byKey(const Key('lookup-add-to-notebook')), findsNothing);
  });

  testWidgets('lookup UnauthorizedException → 인증 안내 copy', (tester) async {
    final lookup = _FakeLookupRepo(
      result: const Failure<LookupResult>(UnauthorizedException('bad token')),
    );
    final adder = _RecordingAdder();
    final c = _container(lookup: lookup);
    addTearDown(c.dispose);

    await tester.pumpWidget(_host(
      container: c,
      word: 'x',
      sentenceContext: 'c',
      onAdd: adder.call,
    ));
    await tester.pumpAndSettle();

    await tester.tap(find.text('open'));
    await tester.pumpAndSettle();

    expect(find.textContaining('인증이 필요합니다'), findsOneWidget);
  });
}
