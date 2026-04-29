/**
 * Korean (ko-KR) message catalogue.
 *
 * Lightweight dot-path lookup. We deliberately avoid pulling in a full
 * i18n runtime for V3; a simple `t("nav.home")` call is enough for the
 * MVP UI. If we later need plurals / interpolation / locale switching,
 * we can migrate to next-intl (already installed in package.json).
 *
 * 한자(한글) 표기 원칙 — `feedback_hanja_notation.md`:
 *  · 한자 개념어를 쓸 때만 `한자(한글)` 형식. 일반 metric 명칭(Sharpe 등)은
 *    한글 + 영문 약어를 병기한다.
 */

export const ko = {
  app: {
    title: "Quant Lab",
    subtitle: "퀀트 투자 백테스팅 플랫폼",
  },
  nav: {
    home: "홈",
    backtests: "백테스트",
    assets: "자산",
    history: "이력",
  },
  asset: {
    add: "자산 추가",
    addTickerLabel: "ticker 입력",
    addMarketLabel: "시장 선택",
    market: { KR: "한국", US: "미국", CRYPTO: "암호화폐" },
    addSubmit: "추가",
    backfilling: "데이터 백필 중",
    notFound: "찾을 수 없는 자산입니다.",
    duplicate: "이미 등록된 자산입니다.",
  },
  backtest: {
    create: "새 백테스트",
    selectStrategy: "전략 선택",
    selectUniverse: "자산 선택",
    period: "기간",
    baseCurrency: "기축통화",
    initialCash: "초기 자본",
    run: "실행",
    cancel: "취소",
    progress: "진행률",
    pending: "대기 중",
    running: "실행 중",
    done: "완료",
    failed: "실패",
    cancelled: "취소됨",
  },
  metric: {
    cagr: "연복리 수익률 (CAGR)",
    mdd: "최대 낙폭 (MDD)",
    sharpe: "샤프지수 (Sharpe)",
    sortino: "소티노지수 (Sortino)",
    calmar: "칼마지수 (Calmar)",
    winRate: "승률",
  },
  error: {
    generic: "오류가 발생했습니다",
    networkFailure: "서버에 연결할 수 없습니다. 백엔드가 실행 중인지 확인하세요.",
    contactSupport: "추적 ID:",
  },
  // TASK-094: 진행률 폴링 패널 (in-place, /backtests/new) 와
  // 한국어 에러 메시지 액션 가이드. 기존 backtest.* 키와 의도적으로 분리 —
  // backtest.* 는 폼 라벨, progress.* 는 진행률/취소/완료 흐름 전용.
  progress: {
    pending: "대기 중...",
    running: "실행 중",
    progressPct: "진행률",
    cancel: "취소",
    cancelConfirm: "백테스트를 취소하시겠습니까?",
    cancelled: "취소됨",
    failed: "실패",
    failedTitle: "백테스트 실패",
    done: "완료 — 결과 보기",
    doneTitle: "완료",
    doneRedirecting: "결과 화면으로 이동 중...",
    seeResult: "결과 보기 →",
    retry: "다시 시도",
    newBacktest: "새 백테스트",
    creating: "백테스트 생성 중...",
    waiting: "대기",
    errorOccurred: "오류 발생",
    stage: "단계",
    traceId: "추적 ID",
  },
  // 액션 가이드 — "무엇을 어떻게 고칠지" 까지 짧은 한 줄로 안내
  // (UI/UX 원칙 2·3 — 친절하고 실행 가능한 한국어 에러).
  errorGuide: {
    networkFailure:
      "서버에 연결할 수 없습니다. 백엔드가 실행 중인지 확인하고 다시 시도하세요.",
    invalidUniverse:
      "선택한 자산 중 데이터가 없는 자산이 있습니다. 자산 카탈로그에서 백필 상태를 확인하세요.",
    periodTooShort:
      "선택한 기간이 너무 짧습니다. 최소 30일 이상으로 설정하세요.",
    insufficientCash:
      "초기 자본이 너무 적습니다. universe 의 최소 가격을 고려해 늘리세요.",
    notice: "기간이 자동 조정됐습니다",
  },
} as const;

/**
 * Lookup a nested string by dot-path (e.g. `t("nav.home")`).
 *
 * Returns the path itself when the lookup misses or when the resolved
 * value isn't a string (e.g. accessing an object node by mistake). This
 * mirrors next-intl's "missing key" fallback behaviour and keeps the UI
 * from crashing on typos.
 */
export function t(path: string): string {
  const parts = path.split(".");
  let current: unknown = ko;
  for (const p of parts) {
    if (current && typeof current === "object" && p in (current as object)) {
      current = (current as Record<string, unknown>)[p];
    } else {
      return path;
    }
  }
  return typeof current === "string" ? current : path;
}
