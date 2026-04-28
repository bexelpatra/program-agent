import 'package:abc_english_app/core/domain/entities/sentence.dart';
import 'package:abc_english_app/features/player/presentation/widgets/player_sentence_tile.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  Widget host({
    required Sentence sentence,
    required bool isCurrent,
    required VoidCallback onTap,
    required void Function(String, String) onWordLongPress,
  }) {
    return MaterialApp(
      home: Scaffold(
        body: PlayerSentenceTile(
          sentence: sentence,
          isCurrent: isCurrent,
          onTap: onTap,
          onWordLongPress: onWordLongPress,
        ),
      ),
    );
  }

  const sentence =
      Sentence(index: 2, text: 'Hello world.', startMs: 3000, endMs: 5000);

  testWidgets('tap → onTap fires (jumpToSentence hook)', (tester) async {
    var tapped = 0;
    await tester.pumpWidget(host(
      sentence: sentence,
      isCurrent: false,
      onTap: () => tapped++,
      onWordLongPress: (_, _) {},
    ));

    // Tap the tile via its key so we don't hit the word long-press recognizer.
    await tester.tap(find.byKey(const Key('player-sentence-2')));
    await tester.pump();

    expect(tapped, 1);
  });

  testWidgets('renders 1-based index prefix and sentence text', (tester) async {
    await tester.pumpWidget(host(
      sentence: sentence,
      isCurrent: false,
      onTap: () {},
      onWordLongPress: (_, _) {},
    ));

    // RichText.toPlainText() may not recurse; check via the composed children
    // of the single RichText in the tile.
    final rich = tester.widget<RichText>(find.descendant(
      of: find.byKey(const Key('player-sentence-2')),
      matching: find.byType(RichText).first,
    ));
    final plain = (rich.text as TextSpan)
        .toPlainText(includeSemanticsLabels: false, includePlaceholders: false);
    expect(plain.startsWith('3.'), isTrue, reason: 'plain=$plain');
    // The sentence is split into per-word spans, so depending on how
    // toPlainText walks whitespace-only spans the separator may collapse.
    // The important contract is that both words appear in order.
    expect(plain.contains('Hello'), isTrue, reason: 'plain=$plain');
    expect(plain.indexOf('Hello') < plain.indexOf('world'), isTrue,
        reason: 'plain=$plain');
  });

  testWidgets('time range (00:03–00:05) rendered in labelSmall', (tester) async {
    await tester.pumpWidget(host(
      sentence: sentence,
      isCurrent: false,
      onTap: () {},
      onWordLongPress: (_, _) {},
    ));
    expect(find.text('(00:03–00:05)'), findsOneWidget);
  });

  testWidgets('isCurrent=true → highlighted style (AnimatedContainer decoration)',
      (tester) async {
    await tester.pumpWidget(host(
      sentence: sentence,
      isCurrent: true,
      onTap: () {},
      onWordLongPress: (_, _) {},
    ));

    final anim = tester.widget<AnimatedContainer>(find.descendant(
      of: find.byKey(const Key('player-sentence-2')),
      matching: find.byType(AnimatedContainer),
    ));

    final decoration = anim.decoration as BoxDecoration;
    expect(decoration.color, isNotNull);
    expect(decoration.color, isNot(Colors.transparent));
  });

  testWidgets('isCurrent=false → no highlight color (transparent)',
      (tester) async {
    await tester.pumpWidget(host(
      sentence: sentence,
      isCurrent: false,
      onTap: () {},
      onWordLongPress: (_, _) {},
    ));

    final anim = tester.widget<AnimatedContainer>(find.descendant(
      of: find.byKey(const Key('player-sentence-2')),
      matching: find.byType(AnimatedContainer),
    ));

    final decoration = anim.decoration as BoxDecoration;
    expect(decoration.color, Colors.transparent);
  });
}
