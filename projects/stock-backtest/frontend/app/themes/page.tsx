"use client";

/**
 * /themes — 테마 카탈로그 화면 (Phase 2 화면 4 — TASK-307).
 *
 * 책임:
 *   1. `api.listThemes()` 호출 → ThemeList 렌더 (멤버 카운트 포함).
 *   2. "새 테마" 버튼 → ThemeEditor (mode='create') 다이얼로그.
 *   3. 카드 편집 → ThemeEditor (mode='edit') 다이얼로그.
 *   4. 카드 삭제 → window.confirm + `api.deleteTheme` (204) → 토스트.
 *   5. 카드 본문 클릭 → `/themes/{theme_id}` 라우팅 (Next Link — ThemeList
 *      내부 처리, 화면 5 = TASK-308 의 상세 페이지).
 *
 * 자산 카탈로그 (`/assets`) 와 동일한 layout 골격 (헤더 + Card 컨테이너 +
 * grid). UI/UX 원칙 1·2·3·5 강제. ApiError 는 traceId.slice(0,8) 으로
 * support trace 노출.
 */
import { useCallback, useEffect, useState } from "react";

import { api, ApiError } from "@/lib/api/client";
import { ko } from "@/lib/i18n/ko";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/toast";
import { ThemeEditor } from "@/components/themes/ThemeEditor";
import { ThemeList } from "@/components/themes/ThemeList";
import type { Theme } from "@/lib/api/types";

export default function ThemesPage() {
  const [items, setItems] = useState<Theme[]>([]);
  const [loading, setLoading] = useState(false);
  const [editorOpen, setEditorOpen] = useState(false);
  const [editorMode, setEditorMode] = useState<"create" | "edit">("create");
  const [editing, setEditing] = useState<Theme | null>(null);
  const [deleting, setDeleting] = useState<number | null>(null);
  const { toast } = useToast();

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.listThemes(undefined, 100, 0);
      setItems(res.items);
    } catch (e) {
      const err = e as ApiError;
      const traceSuffix = err.traceId
        ? ` (${ko.error.contactSupport} ${err.traceId.slice(0, 8)})`
        : "";
      toast({
        title: ko.error.generic,
        description: `${err.message}${traceSuffix}`,
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => {
    void load();
  }, [load]);

  function openCreate() {
    setEditorMode("create");
    setEditing(null);
    setEditorOpen(true);
  }

  function openEdit(theme: Theme) {
    setEditorMode("edit");
    setEditing(theme);
    setEditorOpen(true);
  }

  async function handleDelete(theme: Theme) {
    // 토스트 시스템이 confirm UI 를 직접 제공하지 않으므로 표준
    // window.confirm 으로 의도 확인 (UI/UX 원칙 2 — 한국어 prompt).
    if (typeof window !== "undefined") {
      const ok = window.confirm(ko.theme.delete.confirm);
      if (!ok) return;
    }
    setDeleting(theme.theme_id);
    try {
      await api.deleteTheme(theme.theme_id);
      toast({
        title: ko.theme.delete.success,
        description: theme.name,
        variant: "success",
      });
      await load();
    } catch (e) {
      const err = e as ApiError;
      const traceSuffix = err.traceId
        ? ` (추적 ${err.traceId.slice(0, 8)})`
        : "";
      toast({
        title: ko.error.generic,
        description: `${err.message}${traceSuffix}`,
        variant: "destructive",
      });
    } finally {
      setDeleting(null);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="mx-auto max-w-7xl space-y-6">
        <header className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">{ko.theme.list.title}</h1>
          <Button onClick={openCreate}>{ko.theme.list.create}</Button>
        </header>

        {loading ? (
          <div className="rounded-lg border border-gray-200 bg-white p-12 text-center text-gray-600">
            {ko.theme.list.loading}
          </div>
        ) : (
          <ThemeList
            items={items}
            onEdit={openEdit}
            onDelete={handleDelete}
          />
        )}

        {deleting !== null && (
          <p
            className="text-xs text-gray-500"
            role="status"
            aria-live="polite"
          >
            {ko.theme.delete.submitting}
          </p>
        )}
      </div>

      <ThemeEditor
        open={editorOpen}
        mode={editorMode}
        initial={editing}
        onOpenChange={setEditorOpen}
        onSaved={load}
      />
    </main>
  );
}
