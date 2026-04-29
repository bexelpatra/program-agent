"use client";

/**
 * Toast — minimal client-side notification system.
 *
 * No external dependency (sonner / Radix toast not in package.json).
 * Pattern:
 *   1. Wrap the app in `<ToastProvider>` (done in `app/layout.tsx`).
 *   2. Anywhere below it, call `useToast()` and `toast({...})`.
 *
 * The Toaster portal is fixed bottom-right, auto-dismisses after a
 * configurable duration. Errors should pass `variant: "destructive"`
 * and include the trace_id from `ApiError.traceId` (UI/UX 원칙 2).
 *
 * If we later need richer behaviour (swipe to dismiss, action buttons,
 * stacking animations), swap the implementation for `sonner`; the
 * `toast()` API surface is intentionally compatible.
 */
import * as React from "react";

import { cn } from "@/lib/utils";

export type ToastVariant = "default" | "success" | "destructive";

export interface ToastInput {
  title: string;
  description?: string;
  variant?: ToastVariant;
  /** Auto-dismiss after N ms. Default 5000. Set to 0 to keep until clicked. */
  durationMs?: number;
}

interface ToastInstance extends ToastInput {
  id: number;
}

interface ToastContextValue {
  toasts: ToastInstance[];
  toast: (t: ToastInput) => void;
  dismiss: (id: number) => void;
}

const ToastContext = React.createContext<ToastContextValue | null>(null);

let nextId = 1;

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<ToastInstance[]>([]);

  const dismiss = React.useCallback((id: number) => {
    setToasts((cur) => cur.filter((t) => t.id !== id));
  }, []);

  const toast = React.useCallback(
    (t: ToastInput) => {
      const id = nextId++;
      const instance: ToastInstance = { id, ...t };
      setToasts((cur) => [...cur, instance]);
      const duration = t.durationMs ?? 5000;
      if (duration > 0) {
        setTimeout(() => dismiss(id), duration);
      }
    },
    [dismiss],
  );

  const value = React.useMemo(
    () => ({ toasts, toast, dismiss }),
    [toasts, toast, dismiss],
  );

  return (
    <ToastContext.Provider value={value}>
      {children}
      <Toaster />
    </ToastContext.Provider>
  );
}

export function useToast(): ToastContextValue {
  const ctx = React.useContext(ToastContext);
  if (!ctx) {
    throw new Error("useToast must be used inside <ToastProvider>");
  }
  return ctx;
}

const VARIANT_CLASSES: Record<ToastVariant, string> = {
  default: "border-gray-200 bg-white text-gray-900",
  success: "border-green-200 bg-green-50 text-green-900",
  destructive: "border-red-200 bg-red-50 text-red-900",
};

function Toaster() {
  const ctx = React.useContext(ToastContext);
  if (!ctx) return null;
  return (
    <div className="pointer-events-none fixed inset-x-0 bottom-0 z-50 flex flex-col items-end gap-2 p-4 sm:right-0 sm:top-auto sm:max-w-sm">
      {ctx.toasts.map((t) => (
        <div
          key={t.id}
          role="status"
          className={cn(
            "pointer-events-auto w-full rounded-md border p-4 shadow-md",
            VARIANT_CLASSES[t.variant ?? "default"],
          )}
          onClick={() => ctx.dismiss(t.id)}
        >
          <div className="text-sm font-semibold">{t.title}</div>
          {t.description ? (
            <div className="mt-1 text-xs opacity-80">{t.description}</div>
          ) : null}
        </div>
      ))}
    </div>
  );
}
