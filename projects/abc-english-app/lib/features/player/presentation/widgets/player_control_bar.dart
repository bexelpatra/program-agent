import 'package:flutter/material.dart';

/// Primary transport controls: skip-back 15s, big play/pause FAB,
/// skip-forward 15s.
///
/// Intentionally stateless — the parent decides whether the player is
/// playing and passes the correct icon. Keeping it stateless means the
/// button reflects the *actual* `PlaybackState` rather than an optimistic
/// local toggle that can drift from reality (e.g. the user's earlier
/// play() is still buffering when a second tap comes in).
class PlayerControlBar extends StatelessWidget {
  const PlayerControlBar({
    super.key,
    required this.isPlaying,
    required this.isBuffering,
    required this.onPlayPause,
    required this.onSkipBack,
    required this.onSkipForward,
  });

  final bool isPlaying;
  final bool isBuffering;
  final VoidCallback onPlayPause;
  final VoidCallback onSkipBack;
  final VoidCallback onSkipForward;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          _SkipButton(
            key: const Key('player-skip-back'),
            label: '-15s',
            icon: Icons.replay_rounded,
            onPressed: onSkipBack,
          ),
          Semantics(
            label: isPlaying ? '일시정지' : '재생',
            button: true,
            child: SizedBox(
              width: 72,
              height: 72,
              child: FloatingActionButton.large(
                key: const Key('player-play-pause'),
                heroTag: 'player-play-pause',
                onPressed: onPlayPause,
                backgroundColor: scheme.primary,
                foregroundColor: scheme.onPrimary,
                // Crossfade between play / pause / spinner so the icon
                // doesn't visibly snap when just_audio briefly transitions
                // through `loading`/`buffering` between tap and steady state.
                child: AnimatedSwitcher(
                  duration: const Duration(milliseconds: 180),
                  switchInCurve: Curves.easeOut,
                  switchOutCurve: Curves.easeIn,
                  transitionBuilder: (child, anim) =>
                      FadeTransition(opacity: anim, child: child),
                  child: isBuffering && !isPlaying
                      ? const SizedBox(
                          key: ValueKey('buffering'),
                          width: 28,
                          height: 28,
                          child: CircularProgressIndicator(
                            strokeWidth: 3,
                            color: Colors.white,
                          ),
                        )
                      : Icon(
                          isPlaying
                              ? Icons.pause_rounded
                              : Icons.play_arrow_rounded,
                          key: ValueKey(isPlaying ? 'pause' : 'play'),
                          size: 48,
                        ),
                ),
              ),
            ),
          ),
          _SkipButton(
            key: const Key('player-skip-forward'),
            label: '+15s',
            icon: Icons.forward_10_rounded,
            onPressed: onSkipForward,
          ),
        ],
      ),
    );
  }
}

class _SkipButton extends StatelessWidget {
  const _SkipButton({
    super.key,
    required this.label,
    required this.icon,
    required this.onPressed,
  });

  final String label;
  final IconData icon;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    // Minimum 48×48 dp touch target per Material accessibility guidance.
    return SizedBox(
      width: 64,
      height: 64,
      child: Semantics(
        label: '$label 건너뛰기',
        button: true,
        child: IconButton(
          iconSize: 32,
          onPressed: onPressed,
          icon: Icon(icon),
          tooltip: label,
        ),
      ),
    );
  }
}
