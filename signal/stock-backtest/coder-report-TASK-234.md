---
agent: coder
task_id: TASK-234
status: DONE
timestamp: 2026-04-30T13:35:00
---

## 결과 요약

PaginatedResponse.total 이 limit 분만 카운트하던 부정확성을 수정했다.

- `SqlAssetRepository` 에 `count(...)` 메서드 추가 — `search(...)` 와 동일 필터(`q`, `market`, `asset_type`) 적용한 전체 row 수 반환.
- `BacktestRepository` 에 `count_runs()` 메서드 추가 — `list_runs(...)` 와 동일 모집단의 row 수 반환.
- 두 라우터(`/api/assets`, `/api/backtests`) 가 `len(items)` → 별도 count 호출로 전환.
- 신규 단위 테스트 `tests/api/test_pagination.py` 4 케이스 (DB 가용 시) — items=limit 일 때 total > limit 보장.

## 변경된 파일

- `projects/stock-backtest/backend/app/data/asset_repository.py` (수정)
- `projects/stock-backtest/backend/app/data/repositories/backtest_repository.py` (수정)
- `projects/stock-backtest/backend/app/api/assets.py` (수정)
- `projects/stock-backtest/backend/app/api/backtests.py` (수정)
- `projects/stock-backtest/backend/tests/api/test_pagination.py` (신규)

### 추가된 public 메서드 시그니처 (Repository / 공개 API 변경 보고)

- `SqlAssetRepository.count(q: str | None = None, market: Market | None = None, asset_type: str | None = None) -> int`
- `BacktestRepository.count_runs() -> int`

추후 `list_runs` 가 status 등 필터를 받게 되면 `count_runs` 도 동일 시그니처로 확장할 것 (코드 주석으로 명시).

## 검증 결과

- ruff: PASS (touched 파일 5개 모두 통과). `app/api/backtests.py` 에 pre-existing 미사용 import (`datetime`, `timezone`) 가 있으나 본 태스크 범위 외 — 수정하지 않음.
- black: PASS (touched 파일 모두 통과). `app/api/assets.py` 는 pre-existing 포맷 차이(섹션 주석 후 빈 줄, `Query(...)` 줄바꿈) 가 있으나 본 태스크 범위 외 — 손대지 않음.
- pytest `tests/api/test_pagination.py`: 4/4 PASS.
- pytest `tests/api/test_api_contract.py`: 5 fuzz failure 는 **pre-existing** — 404 응답이 OpenAPI spec 에 미documented (의 baseline 결함). stash/restore 로 검증 완료. pagination 변경과 무관.

## 이슈/블로커

없음.

## 다음 제안

- `app/api/backtests.py:19` 의 미사용 `datetime`, `timezone` import 정리 (pre-existing) — 별도 cleanup 태스크로 분리 권장.
- `/api/assets/{asset_id}` 등 5개 엔드포인트의 OpenAPI `responses` 에 `404` 명시 누락 (test_api_contract_fuzz baseline 실패) — 별도 태스크로 분리 권장.
- `BacktestRepository.list_runs` 가 향후 status 등 필터를 받게 되면 `count_runs` 시그니처도 같이 확장해야 동치성이 유지됨 (architecture.md 의 "Repository API" 섹션 누적 반영 권장).
