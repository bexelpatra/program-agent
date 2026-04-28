/// Per-entry queue state for offline → online synchronisation.
///
/// The local drift schema stores this implicitly via `synced_at`:
///   - non-null `syncedAt` → [SyncStatus.synced]
///   - null `syncedAt`     → [SyncStatus.pendingUpsert]
///   - a "delete" intent has no dedicated column today — see
///     [SyncStatus.pendingDelete] note below. The sync engine layer
///     materialises this state from a side-table or tombstone when that
///     feature lands (not in scope for this task).
enum SyncStatus {
  /// Server has acknowledged the latest version of this entry.
  synced,

  /// Local create/update waiting to be pushed.
  pendingUpsert,

  /// User deleted the entry offline; awaiting a DELETE push. The current
  /// schema encodes deletes as soft-delete rows elsewhere in the sync
  /// pipeline — kept on the enum so presentation/domain can treat delete
  /// intent symmetrically with upsert intent.
  pendingDelete,
}
