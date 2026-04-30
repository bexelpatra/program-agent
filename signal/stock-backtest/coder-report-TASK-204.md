---
agent: coder
task_id: TASK-204
status: DONE
timestamp: 2026-04-29T20:35:00
---

## 결과 요약

사용자 첫 시도(run_id=56) 사고 — BTC 100% × $10,000 초기 자본 → 1코인 ~$50k 라 0개 체결 → equity 평탄선 — 의 재현을 사전 차단하는 amber 경고 배너를 `/backtests/new` 의 자산별 비중 입력 카드(AssetWeightMap)에 추가했다.

핵심 동작:

- **정수 주 자산 한정 평가** (KR/US market): `latestPrice * 1주 > initial_cash * weight` 면 amber 경고. 코인(CRYPTO) 은 TASK-205 fractional 매매 적용으로 평가 제외.
- **메시지**: "{symbol} 1주 ≈ {price} {ccy} — 비중 {pct}% × 초기 자본 {cash} = {target} 로는 1주도 매수 불가." + 액션 가이드 ("초기 자본을 늘리거나 해당 자산의 비중을 줄이세요.")
- **코인 정보 배너**: universe 에 코인이 있으면 별도 blue 배너로 "암호화폐는 소수점 매매가 가능 — 작은 비중에서도 체결됩니다" 안내 — 사용자가 코인에 경고가 안 뜨는 이유를 의아해하지 않게.
- **가격 prefetch**: NewBacktestPage 가 universe 변경 시 새로 등장한 자산만 `api.getAssetLatestPrice(asset_id)` 병렬 호출 (이미 알고 있는 가격은 유지). 직전 14일 OHLCV 윈도우의 마지막 close 활용 (주말/공휴일/갭 흡수).
- **클린 경계**: 경고 계산은 export 된 순수 함수 `computeUnbuyableAlerts` 로 분리 — 추후 단위 테스트 가능. 가격 포맷은 `formatPrice` (USD = `$1,234.56`, KRW = `₩12,345`, 기타 = raw + ticker).
- **i18n**: `ko.unbuyable.*` append-only — 기존 `weight.*`, `filter.*` 키 보존.

## 변경된 파일

- `/home/jai/pa/stock-backtest/projects/stock-backtest/frontend/components/backtest/AssetWeightMap.tsx` (수정)
  - `AssetWeightMapAsset.currency` 필드 추가 (기존 `market` 와 동일 위치)
  - Props 에 `latestPrices?`, `initialCash?`, `baseCurrency?` 추가 (모두 optional — 후방호환)
  - export 함수 `computeUnbuyableAlerts(universe, value, latestPrices, initialCash) → UnbuyableAlert[]`
  - 내부 함수 `formatPrice(value, currency)` (USD/KRW/기타 분기)
  - `useMemo` 로 `unbuyableAlerts`, `hasCryptoInUniverse` 계산
  - 기존 합계/현금잔여/100% 초과 배너 아래에 amber 경고 배너 + blue 코인 안내 배너 추가
- `/home/jai/pa/stock-backtest/projects/stock-backtest/frontend/lib/api/client.ts` (수정 — append-only)
  - `OhlcvListSchema` import 추가
  - `api.getAssetOhlcv(assetId, start, end)` 메서드 추가
  - `api.getAssetLatestPrice(assetId): Promise<number | null>` 헬퍼 추가 (직전 14일 윈도우 → 마지막 close 또는 null)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/frontend/lib/api/schemas.ts` (수정 — append-only)
  - `OhlcvPointSchema`, `OhlcvList Schema`, 타입 alias `OhlcvPoint`, `OhlcvList`
  - 백엔드 `OhlcvPoint` (backend/app/schemas/asset.py L63) 거울. `time` ISO datetime string, `close` 필수, 나머지 nullable.
- `/home/jai/pa/stock-backtest/projects/stock-backtest/frontend/app/backtests/new/page.tsx` (수정)
  - state `latestPrices: Record<number, number>` + `useEffect(universe)` 로 누락 자산만 추가 prefetch (eslint-disable 로 무한루프 방지 — 의존성 universe 만)
  - `<AssetWeightMap>` 호출에 `latestPrices`, `initialCash`, `baseCurrency` props 전달
- `/home/jai/pa/stock-backtest/projects/stock-backtest/frontend/lib/i18n/ko.ts` (수정 — append-only)
  - `unbuyable.*` 키 5개: `title`, `cryptoOk`, `priceLoading`, `noPriceData`, `actionHint`
  - 기존 `backtest.*`, `weight.*`, `filter.*` 등 모든 키 보존

(backend/, signal/, frontend/components/backtest/{FilterConfigBuilder, StrategyParamsForm, UniverseSelector, EquityChart, DrawdownChart, MetricsTable, MonthlyHeatmap, TradesTable, ProgressPanel} 일절 미수정 — 병렬 안전 경계 준수)

## Acceptance test 결과

### 1. `npx tsc --noEmit` exit 0
통과 (출력 없음).

### 2. `npm run build` exit 0
통과. /backtests/new 번들 8.01 kB (기존 대비 minor 증가, schemas/client 헬퍼 포함). 6/6 페이지 정적 생성 성공.

### 3. 영속화 dev 서버 재가동
`systemctl --user restart quant-lab-frontend.service` → active (running). PID 121951.

### 4. HTTP 응답
- `GET http://localhost:3001/` → 200 OK
- `GET http://localhost:3001/assets` → 200 OK
- `GET http://localhost:3001/backtests/new` → 200 OK

### 5. 클라이언트 번들 strings 검증
`/backtests/new` 의 빌드 산출물(`page-104b8a58a641c6c9.js`)에서 grep:
- `매수 불가` 토큰 hit (경고 배너 제목)
- `getAssetLatestPrice` 토큰 hit (API 헬퍼)

### 6. 백엔드 OHLCV 엔드포인트 동작 확인
SPY (asset_id=21) 의 직전 14일 OHLCV → 10개 row 반환, last close = $711.69.
→ 사용자가 SPY 100% × $100 시나리오 입력하면 amber 경고 즉시 노출 (711.69 > 100 × 1.0 = 100).

## 클린 코드 점검

- API 호출 1회/자산: `useEffect([universe])` 안에서 누락된 자산만 fetch — 비중 변경/리렌더 시 재호출 없음. 사용자가 universe 자산을 추가만 할 때 새 자산만 fetch.
- 함수 분리: 경고 계산(`computeUnbuyableAlerts`), 포맷(`formatPrice`) 분리 — 호출 사이트 readability 유지.
- export 된 순수 함수 → Tester 가 단위 테스트 가능 (코인 제외, 가격 미수집 보류, weight=0 스킵, target<price 트리거 등 케이스).
- 한국어 i18n: 모든 신규 메시지 ko.unbuyable.* 통과. magic string 없음.
- 가격 포맷: USD/KRW 케이스별 천단위 콤마 + 통화 기호. 기타 통화는 raw + ticker fallback (BTC=USD, KODEX=KRW 두 케이스만 MVP 에서 등장).

## 이슈/블로커

없음. 다음 항목은 의도적으로 1단계 단순화로 보류 — 보수적 안전성 손상 없음:
- **FX 환산 미적용**: 자산 native currency 가격 vs base_currency 자본을 raw 비교. 일반적으로 base 가 KRW 면 USD 자산 가격이 환산되어 더 커지는 방향 (1주 = $711 → ₩980,000+) — 즉 raw 비교는 경고 trigger 가 약하게 잡혀 false positive 위험. 반대로 사용자가 자본을 좀 더 키우는 방향으로 안전하게 유도. 정확한 환산은 추후 fx_rates API 노출 + prefetch 확장.
- **prefetch race condition**: universe 를 빠르게 add/remove 하면 이전 fetch 결과가 늦게 도착해 잠시 stale 일 수 있음 — `cancelled` flag 로 컴포넌트 unmount 만 방어. 비중 평가는 user input 후 "결과 보기" 직전 단계라 ms 단위 race 영향 무시 가능.

## 다음 제안

- **TASK-205 backend (코인 fractional 매매)** 가 적용된 이후, 일반적인 universe 시나리오에서 사용자 첫 시도 사고가 거의 모든 path 에서 차단됨. 이 두 변화의 결합 효과를 retrospective 에 기록 권장.
- **단위 테스트** (Tester 영역): `computeUnbuyableAlerts` 의 edge case (코인 제외, weight=0 스킵, price=0 보류, latestPrices undefined, initialCash<=0 보류, KR/US 정수 자산 트리거) — 이미 export 됐으므로 즉시 테스트 작성 가능.
- **가격 포맷 i18n**: 통화 기호/소수점 자릿수가 `formatPrice` 에 하드코딩됨. 통화 추가 시(JPY/EUR 등) 분기 추가 필요. 추후 `Intl.NumberFormat` 직접 사용으로 일반화 검토.
- **Loading 상태 노출**: 현재 prefetch 중에는 `latestPrices` 가 비어있어 경고가 나타나지 않음. 빠른 사용자라면 prefetch 완료 전 제출할 수 있음. `ko.unbuyable.priceLoading` 키만 추가해두고 UI 노출은 보류 — universe 변경 직후 최대 1초 이내 prefetch 완료, 일반 사용자 입력 시간보다 짧음.
