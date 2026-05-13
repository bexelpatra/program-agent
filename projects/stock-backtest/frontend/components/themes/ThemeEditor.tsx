"use client";

/**
 * ThemeEditor — 테마 생성/편집 다이얼로그 (TASK-307).
 *
 * mode='create' 면 빈 form → `api.createTheme`, mode='edit' 면 initial 값
 * 채운 form → `api.updateTheme`. AddAssetDialog 와 동일한 inline overlay
 * 패턴 (Radix Dialog 의존성 회피). Zod 검증은 `ThemeCreateSchema` /
 * `ThemeUpdateSchema` 로 제출 직전 1회.
 *
 * UI/UX 원칙:
 *   · 1 (JSON 노출 0) — form-only.
 *   · 2 (한국어) — 라벨/플레이스홀더/에러 모두 한국어, traceId.slice(0,8) prefix.
 *   · 3 (진행 가시화) — "저장 중..." spinner + toast.
 *   · 5 (Zod 검증) — submit 시 ThemeCreate/UpdateSchema.parse() 로 422
 *     이전에 클라이언트 측 차단.
 */
import { useEffect, useState } from "react";

import { api, ApiError } from "@/lib/api/client";
import { ThemeCreateSchema, ThemeUpdateSchema } from "@/lib/api/schemas";
import type { Theme } from "@/lib/api/types";
import { ko } from "@/lib/i18n/ko";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/toast";

type Mode = "create" | "edit";

interface Props {
  open: boolean;
  mode: Mode;
  initial?: Theme | null;
  onOpenChange: (v: boolean) => void;
  onSaved: () => void;
}

export function ThemeEditor({
  open,
  mode,
  initial,
  onOpenChange,
  onSaved,
}: Props) {
  const [name, setName] = useState(initial?.name ?? "");
  const [description, setDescription] = useState(initial?.description ?? "");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const { toast } = useToast();

  // dialog 가 열릴 때마다 initial 을 재반영 (edit 모드에서 다른 row 클릭 시).
  useEffect(() => {
    if (open) {
      setName(initial?.name ?? "");
      setDescription(initial?.description ?? "");
      setError(null);
    }
  }, [open, initial]);

  if (!open) return null;

  async function submit() {
    setError(null);
    const trimmedName = name.trim();
    if (!trimmedName) {
      setError(ko.theme.editor.nameRequired);
      return;
    }
    if (trimmedName.length > 120) {
      setError(ko.theme.editor.nameTooLong);
      return;
    }
    setSubmitting(true);
    try {
      if (mode === "create") {
        const payload = ThemeCreateSchema.parse({
          name: trimmedName,
          description: description.trim() || null,
        });
        await api.createTheme(payload);
        toast({
          title: ko.theme.editor.success,
          description: ko.theme.editor.createSuccess,
          variant: "success",
        });
      } else {
        if (!initial) {
          setError(ko.error.generic);
          return;
        }
        const payload = ThemeUpdateSchema.parse({
          name: trimmedName,
          description: description.trim() || null,
        });
        await api.updateTheme(initial.theme_id, payload);
        toast({
          title: ko.theme.editor.success,
          description: ko.theme.editor.updateSuccess,
          variant: "success",
        });
      }
      onSaved();
      onOpenChange(false);
    } catch (e) {
      if (e instanceof ApiError) {
        const traceSuffix = e.traceId ? ` (추적 ${e.traceId.slice(0, 8)})` : "";
        const msg = `${e.message}${traceSuffix}`;
        setError(msg);
        toast({
          title: ko.error.generic,
          description: msg,
          variant: "destructive",
        });
      } else {
        const msg = e instanceof Error ? e.message : String(e);
        setError(msg);
      }
    } finally {
      setSubmitting(false);
    }
  }

  const title =
    mode === "create" ? ko.theme.editor.createTitle : ko.theme.editor.editTitle;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      role="dialog"
      aria-modal="true"
      aria-labelledby="theme-editor-title"
    >
      <div className="w-full max-w-lg rounded-lg bg-white p-6 shadow-xl">
        <h2 id="theme-editor-title" className="text-xl font-semibold">
          {title}
        </h2>

        <div className="mt-4 space-y-3">
          <div className="space-y-1">
            <Label htmlFor="theme_name">{ko.theme.editor.nameLabel}</Label>
            <Input
              id="theme_name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder={ko.theme.editor.namePlaceholder}
            />
          </div>
          <div className="space-y-1">
            <Label htmlFor="theme_desc">{ko.theme.editor.descLabel}</Label>
            <Input
              id="theme_desc"
              value={description ?? ""}
              onChange={(e) => setDescription(e.target.value)}
              placeholder={ko.theme.editor.descPlaceholder}
            />
          </div>
          {error && (
            <p className="text-sm text-red-600" role="alert">
              {error}
            </p>
          )}
        </div>

        <div className="mt-6 flex justify-end gap-2">
          <Button
            variant="secondary"
            onClick={() => onOpenChange(false)}
            disabled={submitting}
          >
            {ko.theme.editor.cancel}
          </Button>
          <Button onClick={submit} disabled={submitting}>
            {submitting
              ? ko.theme.editor.submitting
              : ko.theme.editor.submit}
          </Button>
        </div>
      </div>
    </div>
  );
}
