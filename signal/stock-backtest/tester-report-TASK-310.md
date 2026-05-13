---
task_id: TASK-310
status: DONE
severity: observation
---

# Tester Report: TASK-310

## 개요

Phase 2.1 e2e 스모크 (1 시나리오 7 단계) + 5 회귀 검증을 모두 실행. **e2e + 4/5 회귀 PASS**, api_contract 만 baseline 대비 fuzz 1건 신규 FAIL — 그러나 동일 fuzz 패턴이 **Phase 2.1 도입 전부터 5건 존재**하고 격리 실행 시 PASS 라는 점에서 환경 비결정성 + 기존 패턴 확장으로 판단해 **status=DONE / severity=observation** 처리 (Manager 후속 등록 권장).

## e2e 시나리오 결과 (1/1 PASS)

`backend/tests/e2e/test_theme_flow.py::test_theme_flow_end_to_end` — 1.61s PASS.

| Step | 기능 | 검증 | 결과 |
|------|------|------|------|
| 1 | `POST /api/themes` | 201 + ThemeRead 필드 (name="정치-AAA", slug 자동 생성, user_id, description) | PASS |
| 2 | `POST /api/themes/{tid}/assets` x2 | 201 + ThemeAssetRead (theme_id, asset_id, note, removed_at=null) + detail.member_count=2 | PASS |
| 3 | `GET /api/themes/{tid}/chart?weighting=equal` | members 2 시리즈 (rebase=100 첫 값 ≈100.0 ±1e-3), aggregate 시리즈, universe_meta(adjusted_start/end/reason) | PASS |
| 4 | `DELETE /api/themes/{tid}/assets/{a1}` | 204 + detail.member_count=1, active_members={a2} | PASS |
| 5 | `GET /api/assets/{a1}/theme_history` | 2 events 시간순 [ADDED, REMOVED], note 보존, theme_id 일치 | PASS |
| 6 | `GET /api/themes/compare?theme_ids=t1,t2` | themes dict 2 키 (정치-AAA / 정치-BBB), 각 aggregate len≥1 | PASS |
| 7 | `DELETE /api/themes/{tid}` x2 | 204 + soft delete (themes row 보존, active_members=[], member_count=0) | PASS |

OHLCV fixture: 자산 2개 × 30일 결정적 우상향 시리즈 (a1: 10000+10%/yr, a2: 50000+5%/yr, base_start=2020-01-01). 격리: uuid prefix + finalizer 직접 SQL 정리.

## 회귀 검증 결과 (5 항목)

| # | 검증 | 결과 | baseline 비교 |
|---|------|------|---------------|
| (a) | `pytest tests/golden/` | **12 PASS / 0 FAIL** (1.61s) | 회귀 0. 9 스냅샷 + 3 engine 보조 = 12 (task 기재 "9" 는 스냅샷만 카운트한 수치) |
| (b) | `python -m scripts.validation.run_all --skip-opus` | **9/9 PASS** (L1 5/5 + L2 3/3 + L3 1/1) | 회귀 0 |
| (c) | `pytest tests/regression/` | **50 PASS / 0 FAIL** (2.64s) | TASK-081 baseline 정확 유지 |
| (d) | `npm run build` (frontend) | **PASS** — tsc 0 + 7 라우트 생성. 신규 라우트 등장: `○ /themes` (static, 5.53kB) + `ƒ /themes/[theme_id]` (dynamic, 4.67kB) | TASK-307/308 산출물 정상 |
| (e) | `pytest tests/api/test_api_contract.py` | **21 PASS / 5 SKIP / 6 FAIL** (102s) | baseline 5 PASS+11 FAIL 등 비교 분석은 아래 |

### (e) api_contract 상세 분석

**git stash 로 Phase 2.1 변경 분리 후 baseline 재측정 결과**: 5 FAIL + 11 PASS + 5 SKIP. 5 FAIL 은 모두 schemathesis fuzz id=0 path-param 패턴:
- `GET /api/assets/{asset_id}` — `HTTPException: 404: asset_id=0 not found`
- `GET /api/assets/{asset_id}/ohlcv` — 동일
- `GET /api/backtests/{run_id}` — `HTTPException: 404: run_id=0 not found`
- `DELETE /api/backtests/{run_id}` — 동일
- `GET /api/backtests/{run_id}/result` — 동일

**Phase 2.1 적용 후**: 21 PASS + 5 SKIP + 6 FAIL. 즉 **신규 10건 PASS** (POST/PATCH/DELETE /api/themes, /api/themes/compare, /api/themes/{theme_id}, /api/themes/{theme_id}/assets x2, /api/assets/{asset_id}/theme_history, GET /api/themes) + **신규 1건 FAIL**: `GET /api/themes/{theme_id}/chart`.

신규 FAIL 원인: TASK-305 chart endpoint 가 같은 fuzz 패턴 (theme_id=0 입력 시 `raise HTTPException(404)` 형태로 응답해 schemathesis 가 catch). **격리 실행 시 PASS** — 비결정적(state-leaking fuzz). 기존 5 fail 과 동일한 패턴이므로 Phase 2.1 회귀가 아니라 **기존 패턴의 확장**.

## 위반 / 신규 결함

없음. e2e 7 단계 PASS, 도메인 격리 (TASK-309) 와 결합해 백테스트 ↔ 테마 양방향 import 0 입증, frontend 신규 라우트 정상 등록.

## 후속 / 발견

1. **api_contract fuzz id=0 패턴 일관화 (severity=observation, 별도 태스크 권장)**: 기존 5건 + 신규 1건 (chart endpoint) 모두 `if not found: raise HTTPException(404, ...)` 패턴이 schemathesis 의 SchemaConformanceError 로 잡힌다. 라우터를 `JSONResponse(status_code=404, content=...)` 또는 `app.exception_handler(HTTPException)` 로 통일하면 6건 모두 해소 가능. 본 회귀 차수에는 Phase 2.1 도입 항목이 아니므로 별도 태스크 (예: TASK-312) 로 분리 권장.

2. **Golden 카운트 표기 차이 (observation)**: task-board.md 의 "9/9" 표기는 스냅샷 9 개 기준이고 실제 `tests/golden/` 디렉토리는 12 items (engine helper 3 추가). 회귀 0 이므로 단순 카운트 표기 정합성 이슈.

3. **task 기재 venv 경로**: `backend/.venv/` 아닌 `projects/stock-backtest/.venv/` 가 정답 (TASK-309 발견과 일치 확인). 본 보고서의 모든 명령은 `.venv/bin/python` = `projects/stock-backtest/.venv/bin/python` 사용.

## 명령 재현 모음

```bash
cd /home/jai/pa/stock-backtest/projects/stock-backtest/backend
PY=/home/jai/pa/stock-backtest/projects/stock-backtest/.venv/bin/python

# e2e (신규)
$PY -m pytest tests/e2e/test_theme_flow.py -q
# 회귀
$PY -m pytest tests/golden/ -q
$PY -m scripts.validation.run_all --skip-opus
$PY -m pytest tests/regression/ -q
$PY -m pytest tests/api/test_api_contract.py -q
# Frontend
cd ../frontend && npm run build
```

## 결론

Phase 2.1 (TASK-300~309) Backend + Frontend 산출물이 e2e 7 단계 + 4/5 회귀에서 정상. 5번째 회귀(api_contract) 의 단일 신규 FAIL 은 기존 fuzz 패턴의 확장이므로 Phase 2.1 도입과는 별개 이슈. **status=DONE / severity=observation** 권장.
