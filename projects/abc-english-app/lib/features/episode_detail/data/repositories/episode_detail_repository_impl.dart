import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/connectivity/connectivity_service.dart';
import '../../../../core/errors/app_exception.dart';
import '../../../../core/errors/result.dart';
import '../../../../core/network/dio_client.dart';
import '../../../../core/storage/app_database.dart';
import '../../domain/entities/episode_detail.dart';
import '../../domain/repositories/episode_detail_repository.dart';
import '../datasources/episode_detail_local_datasource.dart';
import '../datasources/episode_detail_remote_datasource.dart';

/// Online-first with local fallback.
///
/// - If the episode has been downloaded (local row exists with a non-empty
///   sentence set), we always serve the local copy — downloading commits
///   the user to the offline snapshot, so remote churn shouldn't surprise
///   them mid-session.
/// - Otherwise: try remote when online, upsert the fresh copy locally, and
///   return it. If offline, fall back to whatever local rows exist.
class EpisodeDetailRepositoryImpl implements EpisodeDetailRepository {
  EpisodeDetailRepositoryImpl({
    required EpisodeDetailRemoteDataSource remote,
    required EpisodeDetailLocalDataSource local,
    required ConnectivityService connectivity,
  })  : _remote = remote,
        _local = local,
        _connectivity = connectivity;

  final EpisodeDetailRemoteDataSource _remote;
  final EpisodeDetailLocalDataSource _local;
  final ConnectivityService _connectivity;

  @override
  Future<Result<EpisodeDetail>> getDetail(String id) async {
    try {
      final cached = await _local.getDetail(id);

      final servedFromLocal = cached != null &&
          cached.episode.isDownloaded &&
          cached.sentences.isNotEmpty;
      if (servedFromLocal) {
        return Success(cached);
      }

      if (!await _connectivity.isOnline()) {
        if (cached != null) {
          return Success(cached);
        }
        return Failure(NotFoundException(
          'episode $id not available offline',
        ));
      }

      final dto = await _remote.fetchDetail(id);
      final fresh = dto.toEntity(
        isDownloaded: cached?.episode.isDownloaded ?? false,
        audioLocalPath: cached?.episode.audioLocalPath,
      );
      await _local.upsertEpisode(fresh.episode);
      await _local.upsertSentences(id, fresh.sentences);
      return Success(fresh);
    } on AppException catch (error) {
      return Failure(error);
    } catch (error) {
      return Failure(UnknownException(
        'episode_detail.repository.getDetail failed',
        cause: error,
      ));
    }
  }
}

// ---------------------------------------------------------------------------
// Riverpod wiring
// ---------------------------------------------------------------------------

final episodeDetailRemoteDataSourceProvider =
    Provider<EpisodeDetailRemoteDataSource>((ref) {
  return EpisodeDetailRemoteDataSource(ref.watch(dioClientProvider));
});

final episodeDetailLocalDataSourceProvider =
    FutureProvider<EpisodeDetailLocalDataSource>((ref) async {
  final db = await ref.watch(appDatabaseProvider.future);
  return EpisodeDetailLocalDataSource(db);
});

final episodeDetailRepositoryProvider =
    FutureProvider<EpisodeDetailRepository>((ref) async {
  final local = await ref.watch(episodeDetailLocalDataSourceProvider.future);
  return EpisodeDetailRepositoryImpl(
    remote: ref.watch(episodeDetailRemoteDataSourceProvider),
    local: local,
    connectivity: ref.watch(connectivityServiceProvider),
  );
});
