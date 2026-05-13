---
task_id: TASK-309
status: DONE
severity:
---

# Tester Report: TASK-309 — 백테스트 ↔ 테마 도메인 격리 정적 검증

## 작성한 테스트

- 신규 디렉토리: `projects/stock-backtest/backend/tests/architecture/`
  - `__init__.py` (빈 파일)
  - `test_no_cross_import.py` (3 invariant)

- 헬퍼 `_scan_imports(target_files, banned_modules)`:
  - `pathlib.Path.rglob("*.py")` 로 대상 파일 수집
  - 라인 단위로 정규식 `^\s*from\s+{module}(\.|\s)|^\s*import\s+{module}(\.|\s|$)` 매칭
  - 위반 시 `(path, line_no, banned_module, line_content)` 튜플 누적
- 헬퍼 `_format_violations()`:
  - `app/...py:LINE  [banned=MODULE]  matching_line` 형식 출력 (디버깅 용이)

3 invariant 는 각각 독립 test 함수로 분리 → 한 invariant 실패가 다른 invariant 실행을 막지 않음.

## 검증 결과 (3 invariant)

명령: `cd projects/stock-backtest/backend && ../.venv/bin/python -m pytest tests/architecture/ -q`
결과: `3 passed, 1 warning in 0.07s`

- invariant ① **PASS** — `app/domain/themes/**/*.py` 안에 `app.domain.{engine,strategy,allocators,filters,trade,portfolio}` import 0 hit
- invariant ② **PASS** — `app/domain/{engine,strategy,trade,portfolio}.py` + `app/domain/{allocators,filters}/**/*.py` 안에 `app.domain.themes` import 0 hit
- invariant ③ **PASS** — `app/services/**/*.py` (`backtest_runner.py`, `data_loader.py`, `__init__.py`) 안에 `app.domain.themes` / `app.data.theme_repository` import 0 hit

## 위반 시 출력 형식 검증 (임시 위반 → 원복)

`app/domain/themes/__init__.py` L1 에 임시로 `from app.domain.engine import dummy  # TEMP-TASK-309-VIOLATION-PROBE` 1줄 삽입 후 invariant ① 단독 실행:

```
E   AssertionError: domain/themes 는 백테스트 도메인을 import 하면 안 된다 (Phase 2 격리 위반):
E       app/domain/themes/__init__.py:1  [banned=app.domain.engine]  from app.domain.engine import dummy  # TEMP-TASK-309-VIOLATION-PROBE
```

출력 형식 확인 후 즉시 원복. `git diff app/domain/themes/__init__.py` → 변경 없음 (exit 0, 빈 diff).

## 코드베이스 현재 상태 (실측 grep)

```bash
$ grep -rn "from app\.domain\.engine\|from app\.domain\.strategy\|from app\.domain\.allocators\|from app\.domain\.filters\|from app\.domain\.trade\|from app\.domain\.portfolio" app/domain/themes/
# (no output)

$ grep -rn "from app\.domain\.themes" app/domain/engine.py app/domain/strategy.py app/domain/allocators/ app/domain/filters/ app/domain/trade.py app/domain/portfolio.py
# (no output)

$ grep -rn "from app\.domain\.themes\|from app\.data\.theme_repository" app/services/
# (no output)
```

3 invariant 전부 0 hit 로 격리 무결성 확인.

## 회귀 검증 (DoD c)

`../.venv/bin/python -m pytest tests/ -q --ignore=tests/architecture` 결과: `7 failed, 162 passed, 4 skipped` (130.95s).

7개 실패는 모두 **사전 존재 회귀** — TASK-309 변경(아키텍처 테스트 디렉토리/파일 신규 1건만 추가, 기존 코드 0 수정) 무관함을 stash 검증으로 입증:

- `git stash --include-untracked` 후 동일 테스트 실행 → 동일하게 7개 실패
- 실패 목록:
  - `tests/api/test_api_contract.py::test_api_contract_fuzz[POST /api/assets]`
  - `tests/api/test_api_contract.py::test_api_contract_fuzz[GET /api/assets/{asset_id}]`
  - `tests/api/test_api_contract.py::test_api_contract_fuzz[GET /api/assets/{asset_id}/ohlcv]`
  - `tests/api/test_api_contract.py::test_api_contract_fuzz[GET /api/backtests/{run_id}]`
  - `tests/api/test_api_contract.py::test_api_contract_fuzz[DELETE /api/backtests/{run_id}]`
  - `tests/api/test_api_contract.py::test_api_contract_fuzz[GET /api/backtests/{run_id}/result]`
  - `tests/e2e/test_persona_first_use.py::test_step2_assets_api_lists_seed_catalog`

→ TASK-309 로 인한 회귀 **0**. (사전 존재 7건은 별도 태스크에서 처리 대상 — 본 보고 범위 외.)

## 환경 메모

태스크 description 의 venv 경로 `projects/stock-backtest/backend/.venv/bin/python` 는 실측과 불일치. 실제 venv 는 `projects/stock-backtest/.venv` (backend 한 단계 위). 본 보고의 명령은 `../.venv/bin/python` 으로 정정해 실행함. Manager 가 task-board 의 venv 경로 표기를 정정하는 것을 권고 (후속 태스크 영향 방지).

## 후속 / 발견

- `app/domain/themes/__init__.py` 는 entity/normalization/repository/service 를 re-export 하지만 모두 `app.domain.themes.*` 하위 → banned 패턴(`app.domain.engine` 등)과 매칭 안 됨. false positive 위험 없음.
- invariant ③ 의 `app.data.theme_repository` ban 은 TASK-302 산출물(현재 untracked 로 작업 트리에 존재)이 services 에서 직접 사용되지 않음을 박제. services 가 향후 theme 도메인을 다루게 되면 별도 service 모듈(`app/services/theme_*.py` 등)을 두고 domain Protocol 만 의존하도록 가이드 필요.
- 정규식은 `from X import` / `import X` 둘 다 잡지만, `__import__("app.domain.engine")` 같은 동적 import 는 잡지 않음 — 정적 검증의 한계. 일반 import 만 사용하는 프로젝트 컨벤션에서 충분.
- pytest 파라미터화 대신 각 invariant 를 독립 test 함수로 작성 → 실패 메시지가 invariant 별 한국어 docstring/assert message 로 명료히 분리.

## 변경 파일

- `projects/stock-backtest/backend/tests/architecture/__init__.py` (신규, 빈 파일)
- `projects/stock-backtest/backend/tests/architecture/test_no_cross_import.py` (신규)
- 기타 변경 0 (도메인/서비스/API 코드 미수정).
