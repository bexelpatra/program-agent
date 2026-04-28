import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../../core/connectivity/connectivity_service.dart';
import '../../../../core/domain/entities/episode.dart';
import '../../../../core/errors/app_exception.dart';
import '../../../../core/errors/result.dart';
import '../../../../core/network/dio_client.dart';
import '../../../../core/storage/app_database.dart';
import '../../domain/repositories/episode_repository.dart';
import '../datasources/episode_local_datasource.dart';
import '../datasources/episode_remote_datasource.dart';

/// Default repository strategy — online-first with local mirror.
///
/// - listEpisodes: if online, fetch from server, upsert into local, return
///   the server rows enriched with the local download-state; if offline,
///   return whatever the local mirror holds.
/// - getById: check local first (cheapest, offline-safe); if absent and we
///   are online, ask the server, upsert, and return.
///
/// Every outward [AppException] is wrapped in `Result.failure`. Raw
/// exceptions from datasources are caught at the boundary.
class EpisodeRepositoryImpl implements EpisodeRepository {
  EpisodeRepositoryImpl({
    required EpisodeRemoteDataSource remote,
    required EpisodeLocalDataSource local,
    required ConnectivityService connectivity,
  })  : _remote = remote,
        _local = local,
        _connectivity = connectivity;

  final EpisodeRemoteDataSource _remote;
  final EpisodeLocalDataSource _local;
  final ConnectivityService _connectivity;

  @override
  Future<Result<List<Episode>>> listEpisodes({
    int page = 1,
    int size = 20,
    DateTime? sinceModified,
  }) async {
    try {
      final online = await _connectivity.isOnline();
      if (!online) {
        final local = await _local.getAll();
        return Success(local);
      }

      final dtos = await _remote.fetchEpisodes(
        page: page,
        size: size,
        sinceModified: sinceModified,
      );
      final localById = {
        for (final e in await _local.getAll()) e.id: e,
      };
      final merged = dtos.map((dto) {
        final existing = localById[dto.id];
        return dto.toEntity(
          isDownloaded: existing?.isDownloaded ?? false,
          audioLocalPath: existing?.audioLocalPath,
        );
      }).toList(growable: false);

      await _local.upsertMany(merged);
      return Success(merged);
    } on AppException catch (error) {
      return Failure(error);
    } catch (error) {
      return Failure(UnknownException(
        'episode.repository.list failed',
        cause: error,
      ));
    }
  }

  @override
  Future<Result<Episode>> getById(String id) async {
    try {
      final local = await _local.getById(id);
      if (local != null) {
        return Success(local);
      }

      if (!await _connectivity.isOnline()) {
        return Failure(NotFoundException('episode $id not cached offline'));
      }

      final dto = await _remote.fetchById(id);
      final entity = dto.toEntity();
      await _local.upsert(entity);
      return Success(entity);
    } on AppException catch (error) {
      return Failure(error);
    } catch (error) {
      return Failure(UnknownException(
        'episode.repository.getById failed',
        cause: error,
      ));
    }
  }
}

// ---------------------------------------------------------------------------
// Riverpod wiring
// ---------------------------------------------------------------------------

final episodeRemoteDataSourceProvider =
    Provider<EpisodeRemoteDataSource>((ref) {
  return EpisodeRemoteDataSource(ref.watch(dioClientProvider));
});

final episodeLocalDataSourceProvider =
    FutureProvider<EpisodeLocalDataSource>((ref) async {
  final db = await ref.watch(appDatabaseProvider.future);
  return EpisodeLocalDataSource(db);
});

/// DI-complete repository provider. Await to resolve the async DB dependency.
final episodeRepositoryProvider =
    FutureProvider<EpisodeRepository>((ref) async {
  final local = await ref.watch(episodeLocalDataSourceProvider.future);
  return EpisodeRepositoryImpl(
    remote: ref.watch(episodeRemoteDataSourceProvider),
    local: local,
    connectivity: ref.watch(connectivityServiceProvider),
  );
});
