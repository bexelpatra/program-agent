import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../features/episode_detail/presentation/episode_detail_screen.dart';
import '../../features/episode_list/presentation/episode_list_screen.dart';
import '../../features/notebook/presentation/notebook_screen.dart';
import '../../features/player/presentation/player_screen.dart';
import '../../features/settings/presentation/settings_placeholder.dart';

/// Named route paths. Using constants keeps navigator call-sites compile
/// checked and avoids raw string leakage.
class AppRoutes {
  const AppRoutes._();

  static const String episodes = '/';
  static const String episodeDetail = '/episodes/:id';
  static const String player = '/player/:id';
  static const String notebook = '/notebook';
  static const String settings = '/settings';
}

final _rootNavKey = GlobalKey<NavigatorState>(debugLabel: 'root');
final _episodesTabKey = GlobalKey<NavigatorState>(debugLabel: 'episodes-tab');
final _notebookTabKey = GlobalKey<NavigatorState>(debugLabel: 'notebook-tab');
final _settingsTabKey = GlobalKey<NavigatorState>(debugLabel: 'settings-tab');

/// Top-level app router.
///
/// Uses [StatefulShellRoute] so each bottom-nav tab keeps its own
/// navigation stack. The player screen is routed via the root navigator
/// (pushed above the shell) so it can be presented full-screen.
final GoRouter appRouter = GoRouter(
  navigatorKey: _rootNavKey,
  initialLocation: AppRoutes.episodes,
  routes: [
    StatefulShellRoute.indexedStack(
      builder: (context, state, navigationShell) {
        return _ShellScaffold(navigationShell: navigationShell);
      },
      branches: [
        StatefulShellBranch(
          navigatorKey: _episodesTabKey,
          routes: [
            GoRoute(
              path: AppRoutes.episodes,
              builder: (context, state) => const EpisodeListScreen(),
              routes: [
                GoRoute(
                  path: 'episodes/:id',
                  builder: (context, state) => EpisodeDetailScreen(
                    episodeId: state.pathParameters['id'] ?? '',
                  ),
                ),
              ],
            ),
          ],
        ),
        StatefulShellBranch(
          navigatorKey: _notebookTabKey,
          routes: [
            GoRoute(
              path: AppRoutes.notebook,
              builder: (context, state) => const NotebookScreen(),
            ),
          ],
        ),
        StatefulShellBranch(
          navigatorKey: _settingsTabKey,
          routes: [
            GoRoute(
              path: AppRoutes.settings,
              builder: (context, state) => const SettingsPlaceholder(),
            ),
          ],
        ),
      ],
    ),
    GoRoute(
      parentNavigatorKey: _rootNavKey,
      path: AppRoutes.player,
      builder: (context, state) => PlayerScreen(
        episodeId: state.pathParameters['id'] ?? '',
      ),
    ),
  ],
);

class _ShellScaffold extends StatelessWidget {
  const _ShellScaffold({required this.navigationShell});

  final StatefulNavigationShell navigationShell;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: navigationShell,
      bottomNavigationBar: NavigationBar(
        selectedIndex: navigationShell.currentIndex,
        onDestinationSelected: (index) => navigationShell.goBranch(
          index,
          initialLocation: index == navigationShell.currentIndex,
        ),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.library_music_outlined),
            selectedIcon: Icon(Icons.library_music),
            label: 'Episodes',
          ),
          NavigationDestination(
            icon: Icon(Icons.book_outlined),
            selectedIcon: Icon(Icons.book),
            label: 'Notebook',
          ),
          NavigationDestination(
            icon: Icon(Icons.settings_outlined),
            selectedIcon: Icon(Icons.settings),
            label: 'Settings',
          ),
        ],
      ),
    );
  }
}
