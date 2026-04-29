---
agent: coder
task_id: TASK-091
status: DONE
timestamp: 2026-04-29T09:25:00
severity: observation
---

## 결과 요약

자산 카탈로그 화면(`/assets`)을 Next.js App Router 페이지로 구현했다. 시장 필터(KR/US/CRYPTO), 심볼·한글명 검색, 인라인 모달 기반 자산 추가 다이얼로그를 포함한다. 모든 상호작용은 `lib/api/client`(api.listAssets, api.createAsset)를 통해 백엔드와 통신하며, 에러는 `ApiError`의 `status` / `traceId`를 한국어 메시지로 변환해 toast로 노출한다.

## 변경된 파일

- `/home/jai/pa/stock-backtest/projects/stock-backtest/frontend/app/assets/page.tsx` (신규)
  - 클라이언트 컴포넌트, 검색·필터·로딩 상태·toast 통합
- `/home/jai/pa/stock-backtest/projects/stock-backtest/frontend/components/asset/AssetTable.tsx` (신규)
  - 순수 presentational 컴포넌트, 빈 상태 안내 문구 포함
  - `AssetRow` 타입을 `Awaited<ReturnType<typeof api.listAssets>>["items"][number]`로 export
- `/home/jai/pa/stock-backtest/projects/stock-backtest/frontend/components/asset/AddAssetDialog.tsx` (신규)
  - 인라인 모달(Radix Dialog 미도입), Zod 클라이언트 검증 + ApiError 분기 처리

`schemas.ts` / `client.ts` / `ko.ts` / 기존 `ui/*.tsx` / `app/page.tsx` / `app/layout.tsx`는 수정하지 않았다.

## DoD 결과

| 검증 | 명령 | 결과 |
|------|------|------|
| TypeScript | `npx tsc --noEmit` | exit 0, 에러 없음 |
| Production build | `npm run build` | 성공. `/assets` 정적 렌더 19.8 kB / 114 kB First Load |
| Dev 서버 응답 | `curl http://localhost:3000/assets` | HTTP 200, 8018 bytes |
| HTML grep "자산 카탈로그" | `grep -c` | 1 |
| HTML grep "심볼 또는 한글명 검색" | `grep -c` | 1 |
| HTML grep "자산 추가" | `grep -c` | 1 |
| HTML grep 시장 옵션 | "전체 시장 / 한국 / 미국 / 암호화폐" | 모두 존재 |
| 빈 상태 메시지 | "등록된 자산이 없습니다" | 존재 (DB 비어있어 초기 표시) |
| 홈 회귀 | `curl /` → "자산 카탈로그 보기" | 200, 1 hit (TASK-090 무손상) |

## UI/UX 원칙 적용

- **원칙 1 (JSON / 코드 노출 금지)**: 자산 추가 다이얼로그는 ticker/시장/종류/통화/이름 폼 입력만 사용. JSON viewer 없음. 응답 결과도 toast 한 줄 한국어 요약(`{symbol} ({name}) 등록됨. 백필 진행 중`).
- **원칙 2 (한국어 우선)**: 모든 라벨/플레이스홀더/버튼/에러/빈 상태 메시지 한국어. ApiError는 status별 매핑 — 422 → `ko.asset.notFound` ("찾을 수 없는 자산입니다."), 409 → `ko.asset.duplicate` ("이미 등록된 자산입니다."), 그 외 → `ko.error.generic` + 추적 ID 8자 단축. 검색 실패 시 `ko.error.contactSupport` ("추적 ID:") + traceId 전체 노출.
- **원칙 3 (진행 상태 가시화)**: 검색 버튼 `로딩 중...` ↔ `검색` 토글, 다이얼로그 제출 버튼 `검증 중...` ↔ `추가` 토글, 등록 성공 시 toast로 `백필 진행 중` 또는 `백필 예약 실패 — cron 대기` 노출(API 응답의 `backfill_enqueued` / `note` 활용). 폴링은 현재 화면에는 미포함 — 백엔드가 매번 listAssets로 새로고침되므로 사용자 측 refresh로 충분(추후 SSE/WebSocket 도입 시 별도 태스크).

## 클린 아키텍처 점검

- presentation → API client → schemas 단방향. 페이지에서 `fetch` 직접 호출 없음.
- `AssetTable`은 props만 받는 순수 컴포넌트, `AddAssetDialog`는 자체 폼 상태만 보유.
- a11y: `<Label htmlFor>` 모두 연결, 다이얼로그에 `role="dialog" aria-modal aria-labelledby` 부여.
- 매직 문자열은 i18n dict(`ko.*`)와 `MARKET_VARIANT` 상수로 분리. 검색 placeholder, 빈 상태 안내 등 1회용 문구는 inline로 둠(추가 dict 항목은 TASK-090 영역).

## 이슈/블로커

### 1. Zod `.default()` 입력/출력 변이로 인한 타입 불일치 (해결됨, 후속 정리 권장)

`AssetSchema.meta = z.record(z.any()).default({})` 때문에 `z.infer<AssetSchema>.meta`는 required(output)지만, `z.array(AssetSchema).parse()`가 반환하는 element의 `meta`는 optional(input)으로 추론된다. 결과적으로 `setItems(res.items)`에서 `Asset[]`(output) ← `(input element)[]` 대입이 TS2345로 막혔다.

해결: `AssetTable`에서 `AssetRow = Awaited<ReturnType<typeof api.listAssets>>["items"][number]`로 row 타입을 client 실제 반환에서 직접 파생. 페이지/테이블 모두 같은 타입 사용. 코드 주석에 사유 명시.

후속 권장: TASK-090 영역(`schemas.ts`)에서 `meta: z.record(z.any()).default({})` → `meta: z.record(z.any()).optional()` 또는 `z.record(z.any())` (기본값 없이 입출력 통일)로 정리하면 `Asset` 타입이 모든 콜사이트에서 그대로 쓰인다. 이 태스크 범위는 아니므로 보고만 하고 미수정.

### 2. shadcn Dialog 미도입

스펙 적기 전 옵션이었던 `frontend/components/ui/dialog.tsx`는 만들지 않고 `AddAssetDialog` 안에 inline overlay로 구현. 이유: Radix Dialog는 `@radix-ui/react-dialog` 의존성 추가가 필요하고 V3 MVP에서 다이얼로그 사용처가 1곳뿐이라 비용이 효익을 초과. ESC 닫기/포커스 트랩이 필요해지면 추후 Radix 도입 후 동일 props로 교체 가능하도록 props 시그니처(`open`, `onOpenChange`, `onCreated`)를 Radix Dialog 호환으로 유지.

## 다음 제안

1. **TASK-092 백테스트 생성 화면**: `/backtests/new`에서 (1) 전략 빌더(allocator + filters + schedule), (2) universe 선택(이 화면에서 등록한 자산 재사용), (3) 기간/초기자본/기축통화 폼, (4) 실행 → run_id 폴링 패널 — 본 화면의 `AddAssetDialog` 패턴(toast + ApiError 분기 + 진행 상태 토글)을 그대로 차용 가능. `api.listAssets({ limit: 1000 })`로 universe 픽커 채우면 됨.
2. **schemas.ts meta 필드 정리** (이슈 #1): TASK-090 영역의 후속 cleanup 태스크로 분리 등록 권장. `meta: z.record(z.any()).default({})` → `optional()` 변경 + 영향받는 콜사이트(현재 0건) 점검.
3. **자산 상세/삭제 동선**: 카탈로그 행 클릭 시 상세(가격 시계열 mini chart, 백필 상태, 삭제 버튼) 모달이 필요해질 가능성. UI/UX 원칙 4(결과 시각화)와 맞물리므로 백테스트 결과 화면(TASK-093 예상)과 패턴 통일 후 도입 권장.
4. **클라이언트 측 재로딩 트리거 정리**: 현재 검색 input은 Enter 키 또는 검색 버튼 클릭 시 fetch. debounce 자동 검색은 백엔드 부담을 고려해 미도입. 향후 자산 수가 많아지면 `q` 변경 시 300ms debounce + AbortController 도입 검토.
