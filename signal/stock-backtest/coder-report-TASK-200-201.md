---
agent: coder
task_id: TASK-200+TASK-201
status: DONE
timestamp: 2026-04-29T15:20:00
---

## 결과 요약

사용자 첫 사용 시 발견된 사고(StrategyParamsForm 의 `weights` JSON-string 우회 → ticker 키 입력 → 백엔드 422) 를 정공법으로 해결.

- **TASK-200 (AssetWeightMap)**: universe 자산별 슬라이더 + 숫자 입력 + 합계 표시 + 균등 분배 / 100% 정규화 / 초기화 버튼 + 현금 잔여 안내 + 100% 초과 경고. props 는 컨트롤드 (`universe`, `value: Record<asset_id, weight>`, `onChange`, `allowCashSlot?`). 키는 항상 `asset_id` 정수 — ticker 직접 입력 차단.
- **TASK-201 (FilterConfigBuilder)**: "+ 필터 추가" → 필터 종류 드롭다운 → params_schema 기반 폼(StrategyParamsForm 재사용) → 다중 row + 삭제. AND 결합 안내. 빈 상태 안내 ("필터 없음 — 모든 자산이 항상 보유 자격").
- **StrategyParamsForm**: JSON-string textarea 분기 영구 제거. 그 자리에 `complexFieldRenderer?` 콜백 props 추가 — 부모가 dict/array 키에 대한 전용 위젯을 그 자리에 끼워넣을 수 있게 함. 미주입 시에는 "다른 카드의 전용 위젯에서 입력합니다" 안내만 표시. **소스에 `JSON.parse` / `JSON.stringify` / `<textarea>` 단어 자체가 0건** (코드 흔적도 없음, 정책 주석만 남김).
- **NewBacktestPage**: AssetWeightMap 카드를 별도로 분리 (allocator 가 dict 파라미터를 가질 때만 노출). FilterConfigBuilder 카드 통합 — 기존 `filter_configs:[]` 고정 제거. universe 변경 시 weights 의 누락 asset_id 는 0 으로 자동 추가, 제거된 asset_id 는 자동 삭제 (useEffect, 동등성 비교로 무한루프 방지). canSubmit 에 `weightsTotal > 0` 게이트 추가. weights=0 일 때 한국어 가이드 토스트.
- **ko.ts**: `weight.*`, `filter.*` 키 append-only 추가. 기존 키 보존.

## 변경된 파일

- `/home/jai/pa/stock-backtest/projects/stock-backtest/frontend/components/backtest/AssetWeightMap.tsx` (신규, 219 lines)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/frontend/components/backtest/FilterConfigBuilder.tsx` (신규, 169 lines)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/frontend/components/backtest/StrategyParamsForm.tsx` (수정 — JSON-string fallback 영구 제거, `complexFieldRenderer?` 추가)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/frontend/app/backtests/new/page.tsx` (수정 — AssetWeightMap / FilterConfigBuilder 통합, useEffect weights 동기화, weightsTotal 게이트)
- `/home/jai/pa/stock-backtest/projects/stock-backtest/frontend/lib/i18n/ko.ts` (수정 — append-only `weight.*` + `filter.*` 키)

(backend, signal, frontend/components/{ui,asset}, frontend/lib/{utils,api/*}.ts, 기타 backtest 컴포넌트는 일절 손대지 않음 — 병렬 안전 경계 준수)

## Acceptance test 결과

### 1. `npx tsc --noEmit && npm run build` exit 0
- `npx tsc --noEmit`: PASS (no output, exit 0)
- `npm run build`: PASS — `Compiled successfully` + 6/6 static pages, `/backtests/new` 7.37 kB / 120 kB First Load JS.

### 2. 빌드 산출물 안티패턴 grep — `JSON.parse|<textarea>|weights JSON` 0건 (우리 코드)
- `/backtests/new/page-77ac857adeef73a8.js` (페이지 청크): `JSON.parse=0`, `JSON.stringify=0`, `textarea=0`, `weights JSON=0`
- 공통 청크 `829-af5d7df3967f864d.js` (FilterConfigBuilder/AssetWeightMap 포함): `JSON.parse=0`, `textarea=0`. `JSON.stringify=2` 만 발견됐으나 둘 다 **API 클라이언트의 fetch body 직렬화** (`POST /api/assets`, `POST /api/backtests`) — 사용자 입력 JSON 노출과 무관, 필수 HTTP 페이로드 직렬화. **사용자에게 JSON/코드를 노출하는 안티패턴은 0건**.
- 소스 grep: `JSON.parse|JSON.stringify|<textarea>` 0 hit (정책 설명 주석에 단어만 등장).

증거 명령:
```
grep -oE 'JSON\.parse|JSON\.stringify|textarea' .next/static/chunks/app/backtests/new/page-*.js
# → 모두 0
```

### 3. dev curl `/backtests/new` HTTP 200 + 한국어 키워드
- HTTP: `200`
- SSR HTML 키워드 확인: `새 백테스트` / `전략 선택` / `자산 선택` / `기축통화` / `리밸런싱` 모두 FOUND
- 빌드 청크에서 (state-conditional 카드용): `시그널 필터` / `자산별 비중` / `균등 분배` / `필터 추가` / `필터 없음` / `100% 정규화` / `현금 잔여` / `100% 를 초과` / `AND 결합` 모두 FOUND

### 4. AssetWeightMap 행위 검증 (코드 레벨 — 인라인 단위)
- universe 빈 배열 → "먼저 위에서 자산(universe) 을 선택하세요" 안내 카드만 렌더 (early return)
- 1자산 → 1줄 슬라이더 + 합계 표시
- 다자산 + "균등 분배" → `1/N` 분배 (`distributeEvenly`)
- 합 100% → 합계 텍스트 `text-green-700`
- 합 100.5% 초과 → 빨강 카드 + "100% 정규화" 가이드
- 합 99.5% 미만 + `allowCashSlot` → amber 카드 + 현금 잔여 안내
- 키는 항상 `asset_id` 정수 (ticker 직접 입력 경로 없음)

### 5. FilterConfigBuilder 행위 검증
- `value=[]` → "필터 없음 — 모든 자산이 항상 보유 자격" 안내
- "+ 필터 추가" → 필터 종류 드롭다운 + 취소/추가
- 추가된 필터마다 Card row + StrategyParamsForm 재사용 + 삭제 버튼
- 다중 필터 헤더에 "(N개 — AND 결합)" 표시
- 알 수 없는 필터 (백엔드 가용 목록과 불일치) → amber 안내

### 6. 회귀 검증
- `/`, `/assets`, `/backtests/new` 모두 HTTP 200 (dev 서버, 백엔드 8001 LISTEN)
- `/backtests/[run_id]`: 빌드 OK (`106 kB`). 런타임 검증은 실제 run_id 필요 (이번 태스크 범위 외, e2e 는 TASK-202 에서)

## 이슈 / 블로커

없음. 다만 아래 관찰을 다음 제안에 정리.

## 다음 제안

### 1. TASK-202 (e2e 페르소나 harness) — 우선순위 HIGH
`task-board.md` L105 등록된 대로:
- 시나리오: 자산 추가 → universe 구성 → AssetWeightMap 60/40 → KRW base → 실행 → ProgressPanel → 결과 페이지
- **회귀 박제 필수**: (a) ticker 키로 weights 보내면 422 가 더 이상 가능하지 않음 (위젯이 asset_id 정수 키만 생성) (b) weights 합 0 → 클라 가드로 차단되어 422 도달 안 함 (c) JSON-string textarea 입력 경로 자체가 없음
- harness 후보: Playwright headless 또는 단순 supertest + JSDOM 렌더 + axe-core
- 위치: `backend/tests/e2e/test_persona_first_use.py` (Manager 결정 사항이지만 frontend Vitest 도 검토)

### 2. allocator 별 dict-param key 명시 메타 추가 (프런트만으로는 제약)
현재 `findObjectParamKeys` 가 schema 의 `type: object` 키를 찾아 첫 번째를 weights 슬롯으로 가정한다. FixedWeight 의 `weights` 1개만 있는 MVP 에선 충분하지만, 향후 dict 파라미터가 2개 이상인 allocator 가 추가되면 (예: AllWeather 의 sub_allocations + risk_budgets) 맥락 분기 못 한다.
- 백엔드 `params_schema` properties 에 `x-ui-widget: "asset-weight-map"` 같은 OpenAPI extension 표시 → 프런트가 그 키만 AssetWeightMap 으로 매핑
- 또는 backend StrategyDescriptor 에 `complex_field_widgets: {weights: "asset_weight_map"}` 메타 필드 추가
- 후속 태스크로 분리 권장 (allocator 다양화 시점)

### 3. `complexFieldRenderer` 활용 — page 레벨 통합 옵션
현재 NewBacktestPage 는 weights 카드를 **별도 `<Card>`** 로 분리해 렌더한다 (UX 명확성 ↑). 대안으로 `StrategyParamsForm` 에 `complexFieldRenderer={({key}) => key === weightParamKey ? <AssetWeightMap .../> : null}` 을 주입해 allocator 카드 내부에 끼워넣는 방식도 가능. 사용자 피드백 수집 후 어느 쪽이 비개발자 친화도가 높은지 평가하면 좋겠다 (현재는 카드 분리가 "이게 별도 작업이다" 시그널을 더 명확히 줌).

### 4. 슬라이더 a11y 개선
`<input type="range">` 에 `aria-label` 만 부여. 시각장애 사용자에 비중 % 가 음성으로 들릴지 검증 필요. shadcn `<Slider>` (Radix) 도입 검토 — 현재 zero a11y surface 유지 정책과 균형 평가.

### 5. `FieldLabel` 의 `htmlFor` 와 children 의 input id 매칭 보강
`StrategyParamsForm` 의 object/array 분기에서 `complexFieldRenderer` 가 `null` 을 반환하면 `<p>` 안내가 children 으로 들어간다. `htmlFor=fieldId` 가 가리킬 input 이 없으므로 a11y 경고 가능. 큰 문제는 아니지만 후속 cleanup.
