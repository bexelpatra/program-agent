---
agent: tester
task_id: TASK-222
status: DONE
timestamp: 2026-04-30T19:30:00
severity: environment
---

## 결과 요약

`tests/e2e/test_persona_first_use.py` 의 allocator 3종 하드코딩을 4종 + ma_signal
포함 단언으로 갱신. **테스트 코드 자체는 PASS 동등 (syntax OK + 단언 패턴이
TASK-221 와 동형) 이지만, 살아있는 backend 서비스 (systemd unit, started
Apr 29 20:52 — TASK-219 commit 이전) 가 TASK-219 의 새 allocator 등록을 아직
load 하지 못해 e2e 가 fail**. 이는 코드 결함이 아니라 서비스 재시작 미적용
(environment) 으로, 사용자가 `systemctl --user restart quant-lab-backend.service`
실행만 하면 PASS. severity=environment.

테스트 코드 변경 정확성: ① docstring + 함수명을 4종으로 동기, ② set 단언에
`"ma_signal"` 추가, ③ `assert "ma_signal" in allocator_names` 명시 추가
(TASK-221 패턴 답습). filter set 단언은 무변경 유지.

## 변경된 파일

- `projects/stock-backtest/backend/tests/e2e/test_persona_first_use.py`
  - **L9** docstring step3 한 줄: `"allocator 3 + filter 2"` → `"allocator 4 + filter 2 (MVP 3 + 사용자 명시 ma_signal, TASK-219)"` (2 줄로 wrap).
  - **L92 함수명**: `test_step3_strategies_api_exposes_allocator3_filter2` → `test_step3_strategies_api_exposes_allocator4_filter2`.
  - **L93-99 docstring**: `"MVP 프리셋: allocator 3 + filter 2 = 5 모두 노출"` → `"allocator 4 (MVP 3 + 사용자 명시 ma_signal, TASK-219) + filter 2"` + TASK-222 갱신 근거 주석.
  - **L102-110 set 단언**: `{"fixed_weight","all_weather","equal_weight"}` →
    `{"fixed_weight","all_weather","equal_weight","ma_signal"}`.
  - **L111 (신규)**: `assert "ma_signal" in allocator_names` 명시 안전망 (TASK-221 패턴).
  - filter set 단언 무변경. 다른 step 함수 무변경.

### 정확한 diff (수정 부분)

```python
# L7-13 docstring header (step3 한 줄)
- step3. /api/strategies 가 allocator 3 + filter 2 + JSON Schema 노출
+ step3. /api/strategies 가 allocator 4 + filter 2 + JSON Schema 노출
+        (MVP 3 + 사용자 명시 ma_signal, TASK-219)

# L92 함수명 + L93-99 docstring + L102-111 단언
- def test_step3_strategies_api_exposes_allocator3_filter2(backend_alive: None) -> None:
-     """MVP 프리셋: allocator 3 + filter 2 = 5 모두 노출 + JSON Schema 포함.
-
-     Quant Lab CLAUDE.md L26 (MVP 3종 + 시그널 필터 2종).
-     """
+ def test_step3_strategies_api_exposes_allocator4_filter2(backend_alive: None) -> None:
+     """allocator 4 (MVP 3 + 사용자 명시 ma_signal, TASK-219) + filter 2 + JSON Schema 포함.
+
+     Quant Lab CLAUDE.md L26 (MVP 3종 + 시그널 필터 2종) 에 ma_signal 추가.
+     TASK-222: ma_signal 추가 (TASK-219) 로 allocator 카운트가 3 → 4 로 의도 증가.
+     set-based 단언으로 추후 추가 회귀 (allocator 5 번째) 도 명시적으로 잡힘.
+     """
      r = requests.get(f"{BACKEND}/api/strategies", timeout=5)
      assert r.status_code == 200
      data = r.json()
      allocator_names = {a["name"] for a in data["allocators"]}
      filter_names = {f["name"] for f in data["filters"]}
      assert allocator_names == {
          "fixed_weight",
          "all_weather",
          "equal_weight",
+         "ma_signal",
      }, f"allocator set drift: {allocator_names}"
+     assert "ma_signal" in allocator_names
      assert filter_names == {
          "moving_average",
          "momentum",
      }, f"filter set drift: {filter_names}"
```

## 테스트 결과

```
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest tests/e2e/test_persona_first_use.py -v
6 collected — 1 failed, 5 passed in 0.62s

PASSED test_step1_assets_page_renders
PASSED test_step2_assets_api_lists_seed_catalog
FAILED test_step3_strategies_api_exposes_allocator4_filter2  ← environment 원인
PASSED test_step4_backtest_create_with_asset_id_keys
PASSED test_step5_backtest_status_pollable
PASSED test_step6_frontend_backtests_new_renders_widgets
```

**실패 진단** (environment, NOT code bug):

1. 디스크 코드는 ma_signal 등록 완료 — 3 등록 사이트 모두 populated:
   - `app/api/strategies.py:21,22,69,71` (import + list_strategies 응답)
   - `app/services/backtest_runner.py:36,37,59` (_ALLOCATORS dict)
   - `app/domain/allocators/__init__.py:11,23,39` (re-export)

2. **살아있는 backend 서비스가 stale**:
   ```
   systemctl --user status quant-lab-backend.service
   → Active: active (running) since Wed 2026-04-29 20:52:04 KST
   → Main PID: 150526 (uvicorn ... .venv/bin/uvicorn app.main:app --port 8001)
   ```
   서비스 시작 시각 (4/29 20:52) < TASK-219 commit (4/30) → uvicorn 워커가
   import time 에 ma_signal 미존재 코드를 load 한 상태로 잔류 중.

3. 직접 검증:
   ```
   $ curl -s http://127.0.0.1:8001/api/strategies | jq -r '.allocators[].name'
   fixed_weight
   all_weather
   equal_weight        ← ma_signal 누락 (서비스 stale)
   ```

4. **해결 액션** (사용자):
   ```
   systemctl --user restart quant-lab-backend.service
   ```
   재시작 후 step3 자동 PASS (코드/단언 모두 일치).

코드 결함 0. severity=environment.

### 컴파일 검증 (보조)

```
python -m py_compile tests/e2e/test_persona_first_use.py
→ syntax OK
```

### 클린 아키텍처 검증 (Tester 표준 절차)

테스트 파일 자체에 위반 없음:
- 계층 의존: requests → public API endpoint 만 호출 (BACKEND/FRONTEND 환경변수
  주입 가능) → OK
- 단일 책임: step1~step6 각각 단일 시나리오 단위 → OK
- 함수 과대: step3 = 22 lines (40 미만), 매개변수 1개 → OK
- 이름·주석: `r/data/allocator_names/filter_names` 의미 명확. `r` 은 requests
  관용 (지역 단발) 허용 → OK
- DTO ↔ Entity: 외부 HTTP JSON 만 dict 로 핸들 → OK

## 이슈/블로커

### environment 1 — backend 서비스 재시작 필요

위 "실패 진단" 4 단계. 사용자가 1회 `systemctl --user restart
quant-lab-backend.service` 실행 후 같은 pytest 명령으로 6 passed 확인 가능.

### observation 1 — `tests/golden/test_golden_scenarios.py:377` 매트릭스는
**갱신 안 함** (TASK-219 tester report 관찰 3 동일 결정 유지).

```
@pytest.mark.parametrize("strategy_name",
    ["fixed_weight", "all_weather", "equal_weight"])
```

9 골든 baseline 의 의도적 락. ma_signal 골든 추가는 별건 (BTC 100% +
window=120 + quarterly 등 새 fixture 필요). 본 태스크 범위 밖.

## 다음 제안

1. **사용자 액션 필요**: `systemctl --user restart quant-lab-backend.service`
   실행 후 재검증 (`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest
   tests/e2e/test_persona_first_use.py -v` → 6 passed 기대).

2. **Manager 처리**: severity=environment 이므로 후속 코드 수정 태스크 생성
   안 함. `signal/stock-backtest/blockers.md` 에 "TASK-219 적용 시 backend
   서비스 재시작 필요" 한 줄 기록 권고 (TASK-220 의 Literal 변경도 같은 영향
   받으므로 묶어서). TASK-222 자체는 DONE 처리 가능 (코드 변경 정확).

3. **재시작 후 검증 시 영향 범위 점검** — TASK-220 (semi_annual) 도 같은
   서비스 재시작에 의존. 재시작 한 번으로 두 태스크 e2e 동시 검증 가능.

## 환경 노트

- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` 사용 (TASK-219 동일 — host anaconda
  의 `dash` pytest 플러그인이 jupyter comm 미초기화로 collection 실패하는
  문제 회피).
- `BACKEND=http://127.0.0.1:8001` (env default), backend_alive fixture 가
  health check 200 통과 → SOFT skip 미발생, 실제 e2e 실행됨.
- `FRONTEND=http://127.0.0.1:3001` 도 200 (frontend_alive 통과).
- 따라서 6 케이스 모두 실제 실행됐고, 5 PASS / 1 FAIL = 의미 있는 결과.
- 백엔드 재시작은 사용자 권한 (Tester 가 임의로 systemctl 호출 안 함).
