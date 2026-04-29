"use client";

/**
 * ProgressPanel — TASK-094 in-place 진행률 패널.
 *
 * /backtests/new 화면이 폼 모드 ↔ 진행 모드를 토글할 때 표시되는 카드.
 * 별도 라우트 (예: /backtests/[run_id]/progress) 를 만들지 않는 이유:
 *   UI/UX 원칙 6 (점진적 노출, 화면 3개 한도) — 화면은 카탈로그 / new /
 *   결과 [run_id] 3개로 고정. 진행률은 new 화면 안에서 in-place 로
 *   처리하고, terminal 상태가 되면 결과 화면으로 라우팅한다.
 *
 * 분기:
 *   - error (네트워크 등 ApiError): 빨강 카드 + 추적 ID + "다시 시도"
 *   - run==null + loading: "백테스트 생성 중..."
 *   - run==null + !loading: "대기" (이론상 도달하지 않지만 안전망)
 *   - status=='pending' | 'running': 진행률 바 + 취소 버튼
 *   - status=='done': 자동 라우팅 1.5s 후 + "결과 보기" 버튼
 *   - status=='failed': 빨강 카드 + run.error.{message,stage,trace_id}
 *   - status=='cancelled': 회색 카드 + "새 백테스트"
 *
 * 모든 텍스트는 ko.progress / ko.errorGuide 에서 가져온다 — UI/UX 원칙 3.
 */
import { useEffect } from "react";
import { useRouter } from "next/navigation";

import type { BacktestRun } from "@/lib/api/schemas";
import { ko } from "@/lib/i18n/ko";
import { ApiError } from "@/lib/api/client";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

const AUTO_REDIRECT_MS = 1500;
const TRACE_ID_PREFIX_LEN = 16;

export interface ProgressPanelProps {
  run: BacktestRun | null;
  loading: boolean;
  error: ApiError | null;
  onCancel: () => Promise<void>;
  /** 폼 모드로 복귀 (runId state 초기화). */
  onReset: () => void;
}

/**
 * BacktestRun.error 는 backend 의 표준 에러 envelope 와 같은 모양:
 *   { stage, type, message, request_ctx, trace_id }
 * 단 schemas 에선 z.record(z.any()) 로 느슨하게 둠 — 여기서 안전하게 narrow.
 */
interface RunErrorShape {
  message?: string;
  stage?: string;
  trace_id?: string;
}

function readRunError(run: BacktestRun): RunErrorShape {
  const e = run.error;
  if (!e || typeof e !== "object") return {};
  const obj = e as Record<string, unknown>;
  return {
    message: typeof obj.message === "string" ? obj.message : undefined,
    stage: typeof obj.stage === "string" ? obj.stage : undefined,
    trace_id: typeof obj.trace_id === "string" ? obj.trace_id : undefined,
  };
}

function formatPct(progress: number): number {
  // 백엔드는 0~1, UI 는 정수 % — clamp 후 반올림.
  if (!Number.isFinite(progress)) return 0;
  const clamped = Math.max(0, Math.min(1, progress));
  return Math.round(clamped * 100);
}

export function ProgressPanel({
  run,
  loading,
  error,
  onCancel,
  onReset,
}: ProgressPanelProps) {
  const router = useRouter();

  // status='done' 이 되면 1.5초 뒤 결과 화면으로 자동 라우팅.
  // 사용자가 그 사이 "결과 보기" 버튼을 누르면 즉시 이동 (수동 우선).
  useEffect(() => {
    if (run?.status !== "done") return;
    const runId = run.run_id;
    const t = setTimeout(() => {
      router.push(`/backtests/${runId}`);
    }, AUTO_REDIRECT_MS);
    return () => clearTimeout(t);
  }, [run?.status, run?.run_id, router]);

  // 1) 폴링 자체 실패 (네트워크 등)
  if (error) {
    return (
      <Card className="border-red-200 bg-red-50 p-6">
        <h3 className="font-semibold text-red-900">
          {ko.progress.errorOccurred}
        </h3>
        <p className="mt-2 text-sm text-red-800">{error.message}</p>
        {error.traceId ? (
          <p className="mt-1 text-xs text-red-600">
            {ko.progress.traceId}: {error.traceId.slice(0, TRACE_ID_PREFIX_LEN)}
          </p>
        ) : null}
        <Button variant="secondary" className="mt-4" onClick={onReset}>
          {ko.progress.retry}
        </Button>
      </Card>
    );
  }

  // 2) 첫 tick 이전 — loading 표시
  if (!run) {
    return (
      <Card className="p-6 text-center text-gray-500">
        {loading ? ko.progress.creating : ko.progress.waiting}
      </Card>
    );
  }

  const status = run.status;
  const pct = formatPct(run.progress);

  // 3) 완료 — 자동 라우팅 + "결과 보기"
  if (status === "done") {
    return (
      <Card className="border-green-200 bg-green-50 p-6">
        <h3 className="font-semibold text-green-900">
          {ko.progress.doneTitle}
        </h3>
        <p className="mt-2 text-sm text-green-800">
          {ko.progress.doneRedirecting}
        </p>
        <Button
          variant="default"
          className="mt-4"
          onClick={() => router.push(`/backtests/${run.run_id}`)}
        >
          {ko.progress.seeResult}
        </Button>
      </Card>
    );
  }

  // 4) 실패 — backend error envelope 상세 노출
  if (status === "failed") {
    const errInfo = readRunError(run);
    const message = errInfo.message ?? ko.error.generic;
    return (
      <Card className="border-red-200 bg-red-50 p-6">
        <h3 className="font-semibold text-red-900">
          {ko.progress.failedTitle}
        </h3>
        <p className="mt-2 text-sm text-red-800">{message}</p>
        {errInfo.stage ? (
          <p className="mt-1 text-xs text-red-600">
            {ko.progress.stage}: {errInfo.stage}
          </p>
        ) : null}
        {errInfo.trace_id ? (
          <p className="mt-1 text-xs text-red-600">
            {ko.progress.traceId}:{" "}
            {errInfo.trace_id.slice(0, TRACE_ID_PREFIX_LEN)}
          </p>
        ) : null}
        <Button variant="secondary" className="mt-4" onClick={onReset}>
          {ko.progress.retry}
        </Button>
      </Card>
    );
  }

  // 5) 취소됨
  if (status === "cancelled") {
    return (
      <Card className="p-6">
        <h3 className="font-semibold text-gray-800">{ko.progress.cancelled}</h3>
        <Button variant="secondary" className="mt-4" onClick={onReset}>
          {ko.progress.newBacktest}
        </Button>
      </Card>
    );
  }

  // 6) pending / running
  return (
    <Card className="p-6">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="font-semibold">
          {status === "pending" ? ko.progress.pending : ko.progress.running}
        </h3>
        <Badge variant="secondary">{status}</Badge>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span>{ko.progress.progressPct}</span>
          <span className="font-mono">{pct}%</span>
        </div>
        <div
          className="h-3 w-full overflow-hidden rounded-full bg-gray-200"
          role="progressbar"
          aria-valuenow={pct}
          aria-valuemin={0}
          aria-valuemax={100}
        >
          <div
            className="h-full bg-blue-600 transition-all duration-300"
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>

      <div className="mt-4 flex justify-end gap-2">
        <Button
          variant="destructive"
          size="sm"
          onClick={() => {
            // window.confirm 은 SSR 안전하지 않지만 ProgressPanel 은
            // "use client" + useEffect 블록만 실행되는 컴포넌트. 사용자
            // 명시 액션 시점에만 호출되므로 안전.
            if (
              typeof window !== "undefined" &&
              window.confirm(ko.progress.cancelConfirm)
            ) {
              void onCancel();
            }
          }}
        >
          {ko.progress.cancel}
        </Button>
      </div>
    </Card>
  );
}
