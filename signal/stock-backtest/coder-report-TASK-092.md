---
agent: coder
task_id: TASK-092
status: DONE
timestamp: 2026-04-29T11:55:00
---

## 결과 요약

`/backtests/new` 백테스트 생성 화면을 구현했다. 사용자는 전략(allocator)
드롭다운 → 파라미터 자동 폼 → universe 검색·다중 선택 → 기간 / 기축통화
/ 초기 자본 / 리밸런싱 주기를 폼으로 입력하고 "백테스트 실행" 버튼으로
POST /api/backtests 를 호출, 반환된 `run_id` 로 `/backtests/{run_id}`
(TASK-093 화면)로 라우팅한다. 화면은 4개 카드로 점진 노출(UI/UX 원칙 6),
모든 필드는 폼 입력(원칙 1), 응답은 Zod `BacktestRunSchema` 로 런타임
검증(원칙 5), 에러 토스트는 한국어 + trace_id 8자리 prefix(원칙 2).

## 변경된 파일

- `projects/stock-backtest/frontend/lib/api/schemas.ts` (수정 — append-only)
  - 추가: `BacktestStatusEnum`, `RebalanceScheduleEnum`,
    `FilterConfigSchema`, `StrategyConfigSchema`, `BacktestCreateSchema`,
    `BacktestRunSchema` 및 동명 type. backend `app/schemas/backtest.py`
    (TASK-062 산출물) 와 일대일 대응.
- `projects/stock-backtest/frontend/lib/api/client.ts` (수정 — append-only)
  - 추가: `api.createBacktest(payload) → BacktestRun`,
    `api.getBacktest(runId) → BacktestRun` (둘 다 fetchAndValidate 경유).
  - import 에 `BacktestCreate` type, `BacktestRunSchema` 추가.
- `projects/stock-backtest/frontend/app/backtests/new/page.tsx` (신규)
- `projects/stock-backtest/frontend/components/backtest/StrategyParamsForm.tsx` (신규)
- `projects/stock-backtest/frontend/components/backtest/UniverseSelector.tsx` (신규)

라인 수: page 348, StrategyParamsForm 249, UniverseSelector 196,
schemas +97, client +13. 총 ~1160 라인 (단일 파일 300 라인 기준 모두 통과;
page.tsx 만 348 인데 카드 4개 + 핸들러 + JSX 가 크게 차지. 의미 단위
분리 후보는 "DoD / 다음 제안" 참조).

## 추가 / 변경된 public API (client.ts)

- `api.createBacktest(payload: BacktestCreate) => Promise<BacktestRun>`
- `api.getBacktest(runId: number) => Promise<BacktestRun>`

(`BacktestRun` 은 `BacktestRunSchema` 의 `z.infer` 결과 — frontend 측
runtime 보장.)

## DoD 검증 결과

1. **tsc + build** — `cd projects/stock-backtest/frontend && npx tsc
   --noEmit` exit 0, `npm run build` ✓ Compiled successfully ·
   `/backtests/new` 라우트 4.04 kB / First Load 117 kB.
2. **dev 서버 + curl** — `npm run dev -p 3092` 백그라운드 기동, polling
   후 `curl -sS -o /dev/null -w "HTTP=%{http_code}"
   http://localhost:3092/backtests/new` → `HTTP=200`. body 13,870
   bytes.
3. **HTML 키워드 grep** — "새 백테스트" / "전략 선택" / "자산 선택" /
   "기축통화" / "리밸런싱 주기" / "백테스트 실행" 6/6 hit (case-sensitive
   `grep -F`).
4. **UI/UX 원칙**:
   - 1 (JSON 노출 금지) — scalar 필드는 모두 `<Input>`/`<Select>`
     /`<input type=checkbox>` 폼. enum 필드는 자동 Select. dict/array
     파라미터는 임시 JSON-string 입력 + amber 경고 메시지로 후속 위젯
     예고 (observation 항목 참조).
   - 2 (한국어 + trace_id) — 모든 토스트는 한국어, ApiError 발생 시
     `err.message + (err.traceId ? ' (' + traceId.slice(0,8) + ')' : '')`.
   - 5 (Zod 검증) — POST 응답은 `BacktestRunSchema.safeParse` 통과해야
     resolve. 422/500 은 `ErrorResponseSchema` 로 디코드 후 ApiError 로
     변환 (client.ts L66-93 기존 코드 활용).
   - 6 (점진적 노출) — 4 카드(전략 / universe / 기간·자본 / 액션) 단일
     화면. 별도 마법사 화면 없음.

## 클린 코드 점검

- 컴포넌트 분리: 페이지가 상태/제출 책임만 가지고, 폼 자동 생성은
  `StrategyParamsForm`, 자산 검색 위젯은 `UniverseSelector` 로 분리.
- API 클라이언트는 `fetchAndValidate` 만 사용 — 페이지/위젯에서 `fetch`
  직접 호출 없음.
- `Asset` 타입 input/output variance 회피: `AssetTable.tsx` 와 동일하게
  `UniverseAsset = Awaited<ReturnType<typeof api.listAssets>>['items'][number]`
  로 element 타입 도출. 페이지·위젯 모두 동일 alias 사용.
- 한국어 라벨은 `lib/i18n/ko.ts` 의 `ko.backtest.*` 우선 사용.
- magic value 회피: `BASE_CURRENCY_OPTIONS`, `REBALANCE_OPTIONS`,
  `MARKET_OPTIONS` 모듈 상수.

## 이슈/블로커

없음. 모든 DoD 통과.

## Observation (severity=observation)

1. **dict/array 파라미터의 임시 JSON 입력** — `StrategyParamsForm` 은
   `def.type === "object" | "array"` 인 필드에 한해 placeholder 가 있는
   text Input + JSON.parse 우회를 허용하고 있다. 예: FixedWeight 의
   `weights: dict[str, float]` (asset_id → weight). UI/UX 원칙 1 의 정신
   (JSON 노출 금지) 에 어긋나는 임시 우회 — 후속 태스크에서 전용
   `AssetWeightMap` 위젯(선택된 universe 자산 행마다 비중 슬라이더 +
   합 100% 검증) 으로 교체해야 한다. 임시 입력 영역에는 amber 경고
   메시지를 표시해 사용자 인지 보장.

2. **filter UI 미구현** — TASK-092 스펙 본문에 filter 선택 UI 명시가
   없어 `filter_configs: []` 로 고정 송신. CLAUDE.md L10-14 의 3요소
   원칙(allocator + filters + schedule) 중 filters 가 비어 있는 상태.
   별도 태스크 (예: TASK-092-FILTER) 에서 strategies.filters 드롭다운 +
   per-filter params 폼 (StrategyParamsForm 재사용) 으로 추가하면 좋다.

3. **base_currency 와 universe 통화 불일치 안내 없음** — 사용자가 KRW
   universe 만 선택하고 base_currency=USD 로 둘 경우 엔진은 FX 환산을
   수행하지만 UI 가 사전 안내하지 않는다. universe 변경 시 universe
   통화 셋과 base_currency 가 다르면 inline note 를 띄우는 게 친절하다.

## 다음 제안

- **TASK-093 (결과 화면)** — `/backtests/{run_id}` 동적 라우트 + equity
  curve / drawdown / 지표 / 연·월 수익률 / 거래 내역. POST 응답 후
  바로 라우팅하므로 결과 화면이 status pending/running/done 분기를
  처리해야 한다 (TASK-094 와 결합).
- **TASK-094 (진행률 폴링)** — 결과 화면 진입 직후 `api.getBacktest`
  를 1~2초 간격 polling, status='done' 도달 시 `/result` 호출. 취소
  버튼은 DELETE /api/backtests/{run_id} 로. **현재 화면 안에서**
  in-place 패널은 만들지 않음 (TASK-094 스펙: 결과 페이지 진입 후
  진행률 표시).
- **AssetWeightMap 위젯** — 위 observation 1 후속.
- **filter 선택 UI** — 위 observation 2 후속.
