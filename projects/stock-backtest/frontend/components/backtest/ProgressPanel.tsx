"use client";

/**
 * ProgressPanel — TASK-094 (초안) → TASK-218 (인플레이스 결과 표시) 패널.
 *
 * /backtests/new 화면이 폼 모드 ↔ 진행 모드를 토글할 때 표시되는 카드.
 * TASK-218 부터 status='done' 일 때 결과 화면으로 자동/수동 라우팅하지
 * 않는다 — 호출부 (page.tsx) 가 같은 페이지에서 결과 컴포넌트를 in-place
 * 렌더링한다. 이력 화면 (`/backtests/[run_id]`) 으로의 진입은 별도
 * 경로 (앱 메인 이력 카드) 에서만 트리거한다.
 *
 * 분기:
 *   - error (네트워크 등 ApiError): 빨강 카드 + 추적 ID + "다시 시도"
 *   - run==null + loading: "백테스트 생성 중..."
 *   - run==null + !loading: "대기" (이론상 도달하지 않지만 안전망)
 *   - status=='pending' | 'running': 진행률 바 + 취소 버튼
 *   - status=='done': 완료 안내 카드만 (호출부가 결과를 렌더링)
 *   - status=='failed': 빨강 카드 + run.error.{message,stage,trace_id}
 *   - status=='cancelled': 회색 카드 + "새 백테스트"
 *
 * 모든 텍스트는 ko.progress / ko.errorGuide 에서 가져온다 — UI/UX 원칙 3.
 */
import type { BacktestRun } from "@/lib/api/schemas";
import { ko } from "@/lib/i18n/ko";
import { ApiError } from "@/lib/api/client";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

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
  // TASK-218: status='done' 자동 라우팅 제거. 같은 페이지(`/backtests/new`)
  // 에서 호출부가 결과를 in-place 렌더링한다. 결과 화면 라우팅이 필요한
  // 진입점(앱 메인 이력 카드 등) 은 그쪽에서 직접 router.push 한다.

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

  // 3) 완료 — 라우팅 없음. 호출부 (`/backtests/new`) 가 같은 페이지에
  //    결과 패널을 in-place 렌더한다 (TASK-218). "새 백테스트" 버튼만 노출.
  if (status === "done") {
    return (
      <Card className="border-green-200 bg-green-50 p-6">
        <h3 className="font-semibold text-green-900">
          {ko.progress.doneTitle}
        </h3>
        <p className="mt-2 text-sm text-green-800">
          {ko.progress.doneInPlace}
        </p>
        <Button variant="secondary" className="mt-4" onClick={onReset}>
          {ko.progress.newBacktest}
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
