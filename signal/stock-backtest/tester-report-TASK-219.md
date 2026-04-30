---
agent: tester
task_id: TASK-219
status: DONE
timestamp: 2026-04-30T18:05:00
severity: observation
---

## 결과 요약

TASK-219 (ma_signal allocator) 검증 완료 + TASK-221 (test_api_contract.py 의
하드코딩 카운트 갱신) 동시 처리.

- **단위 테스트 8/8 PASS** (`tests/domain/test_ma_signal_allocator.py`).
- **9 골든 회귀 0** (`tests/golden/test_golden_scenarios.py` → 12 passed,
  ma_signal 추가가 fixed_weight/all_weather/equal_weight 스냅샷에 영향 없음).
- **API 계약 갱신 후 PASS** (`test_strategies_endpoint_returns_mvp_presets`
  → len==4 + ma_signal in name set).
- **클린 아키텍처 무결** — ma_signal.py import 셋이 fixed_weight.py 와
  완전히 일치 (`pandas` + `pydantic` + `from .base`). 도메인 순수, HTTP/DB/UI
  의존 0.
- **AllocatorBase 패턴 정합** — `name: ClassVar[str]`, `params_schema:
  ClassVar[type[BaseModel]]`, `__init__(params: P)`, `required_universe`
  override, `generate_weights` 구현 + 끝에서 `normalize_weights(filtered,
  allow_cash_slot=True)` 호출 모두 FixedWeight 와 동일 형식.

코드 결함 0. severity=observation (관찰 사항만).

## 변경된 파일

- `projects/stock-backtest/backend/tests/api/test_api_contract.py:78-94`
  - `test_strategies_endpoint_returns_mvp_presets` 갱신:
    - `assert len(body["allocators"]) == 3` → `== 4`
    - `assert names == {"fixed_weight","all_weather","equal_weight"}`
      → `== {..., "ma_signal"}` + `assert "ma_signal" in names` 명시 추가
    - docstring "(MVP)" → "(MVP 3 + 사용자 명시 ma_signal, TASK-219)"
    - 갱신 근거 주석 추가 (TASK-221).

## 테스트 결과

### (1) 단위 테스트 — `tests/domain/test_ma_signal_allocator.py`

8 passed in 0.45s. 케이스별:

| # | 케이스 | 결과 | 비고 |
|---|--------|------|------|
| 1 | test_all_assets_above_ma_returns_input_weights (case a) | PASS | 단조증가 시퀀스 → 합 1.0 그대로 (normalize_weights L109 단락 검증) |
| 2 | test_all_assets_below_ma_returns_empty_dict (case b) | PASS | 단조감소 → 빈 dict (cash-only) |
| 3 | test_partial_above_below_normalizes_remaining (case c) | PASS | BTC 만 살아남고 0.6 → 1.0 재정규화 (normalize 합으로 나눔) |
| 4 | test_per_asset_fallback_skips_short_history (case d) | PASS | **자산 단위 fallback 명시 검증** — BTC 130일·ETH 50일·window=120 → BTC 만 평가, ETH skip 후 0.5 → 1.0 정규화 |
| 5 | test_params_reject_empty_assets | PASS | 빈 dict 거부 (FixedWeightParams 와 동일 정책) |
| 6 | test_params_reject_negative_weight | PASS | 음수 비중 거부 |
| 7 | test_params_reject_weights_far_from_one | PASS | 합 1.0 ± 5% 밖 거부 |
| 8 | test_params_default_window | PASS | window 디폴트 120 (task-board ① ge=2/le=500/default=120) |

case (d) 는 task-board ④ 에서 "자산 단위 fallback (BTC window 충분, ETH 부족) →
BTC 만 평가" 로 명세된 항목을 정확히 검증. `len(series) < window` 체크가
prices_until_d 의 자산별 dropna() 후 길이 평가로 동작하는지를 단위 수준에서
명시적으로 확인 (filters/moving_average.py:52-54 동일 패턴 답습).

### (2) 9 골든 회귀 — `tests/golden/test_golden_scenarios.py`

12 passed in 2.48s. 9 (3 시나리오 × 3 전략) + 3 보조 (cancel_check / progress
callback / empty period). ma_signal 추가가 _ALLOCATORS dict 키만 늘려서 기존
3 전략 등록·소비 경로에 영향 0 — 골든 스냅샷 일치.

### (3) API 계약 갱신 (TASK-221) + DB 무관 contract 트리오

3 passed in 1.12s:
- `test_strategies_endpoint_returns_mvp_presets` (갱신 후) — PASS
- `test_health_endpoint` — PASS
- `test_openapi_endpoint` — PASS

DB 의존 테스트 (`test_backtest_lifecycle_*` 등 7 케이스) 는 fixture
`db_alive` 가 환경 분리 전제로 SOFT skip 동작이라 본 검증에서 실행하지 않음
(Coder report 에서 "fuzz 6건 실패는 사전 존재" 명시 + 본 태스크와 무관).

### (4) 클린 아키텍처 검증 (Tester 표준 절차)

`grep -nE "^(import|from)" app/domain/allocators/ma_signal.py` 와 동일 grep
on `fixed_weight.py` 비교:

```
ma_signal.py        | fixed_weight.py
────────────────────┼────────────────────
__future__          | __future__
datetime.date       | datetime.date
decimal.Decimal     | decimal.Decimal
typing.ClassVar     | typing.ClassVar
pandas              | pandas
pydantic.BaseModel  | pydantic.BaseModel
  Field, validator  |   Field, validator
.base.AllocatorBase | .base.AllocatorBase
  normalize_weights |   normalize_weights
```

→ **import 셋 100% 일치** (관찰 1). 도메인 순수성 위반 0.

체크리스트:
- 계층 의존 방향: 도메인 코드가 HTTP/DB/UI 미참조 → OK
- 단일 책임: `MaSignalParams` 검증 / `MaSignal.required_universe` /
  `MaSignal.generate_weights` 가 각각 단일 책임 → OK
- 함수 과대: `generate_weights` = 22 lines (40 미만), 매개변수 3개 → OK
- 이름·주석: `aid`/`v` 는 dict 순회 인덱스성 약어로 허용, `target_weight`/
  `last_price`/`recent` 등 의미 명확 → OK
- DTO ↔ Entity: 별도 DTO 없이 Pydantic params + Decimal 도메인 결과 → OK
- AllocatorBase 패턴: name/params_schema ClassVar + `__init__(params)` +
  `required_universe` override + `generate_weights` 구현 + 끝의
  `normalize_weights(..., allow_cash_slot=True)` 호출이 FixedWeight
  L79-85 와 동일 → OK

### (5) 다른 하드코딩 카운트 grep 점검 (TASK-221 보강)

```
grep -rnE 'allocators.*== *3|len.*body\["allocators"\]|MVP 프리셋 3종|
          allocator 3 |allocators\) == 3' tests/
```

3 hit:
1. `tests/api/test_api_contract.py:79,83` → **본 태스크에서 갱신 완료**.
2. `tests/e2e/test_persona_first_use.py:9, 92-110` → 갱신 안 함 (관찰 2 참조).
3. `tests/golden/test_golden_scenarios.py:377` `["fixed_weight","all_weather",
   "equal_weight"]` 매트릭스 → 갱신 안 함 (관찰 3 참조). 9 골든 baseline 의
   의도적 락이지 하드코딩 회귀 아님.

추가 grep `'fixed_weight'.*'all_weather'.*'equal_weight'` 으로 하드코딩 set
2 hit 확인 — 위 (2),(3) 항목과 동일 위치.

## 이슈/블로커

코드 결함 0. 아래는 관찰 (severity 가 observation 인 이유).

### 관찰 1 — FixedWeight ↔ MaSignal 코드 중복

`MaSignalParams._validate_assets` (ma_signal.py:53-67) 와 `FixedWeightParams.
_validate_weights` (fixed_weight.py:38-52) 가 거의 동일 (필드 이름만 weights
↔ assets 다름):
- 빈 dict 거부 / 음수 비중 거부 / 합 ≤ 0 거부 / 합 1.0 ± 5% 거부.

Coder report "다음 제안 4" 에서 본 사항 명시 — "3회째 구현체 추가 시
utils 추출 검토". 본 태스크 시점에서는 **수정 권장 안 함** (2 회 중복).

### 관찰 2 — `tests/e2e/test_persona_first_use.py:92-110` 의 동일 회귀 패턴

```
allocator_names == {"fixed_weight", "all_weather", "equal_weight"}
```

이 테스트는 persona harness (Quant Lab CLAUDE.md L26 "MVP 프리셋 3종" 검증
용). task-board TASK-219 ⑥ 에서 명시:

> "L499 MVP 프리셋 카운트 갱신 안 함 (Quant Lab CLAUDE.md L26 = 사용자 명시
> 추가 결정 영역)."

→ ma_signal 은 사용자 명시 추가지 MVP 프리셋이 아니므로 persona harness
정책상 **그대로 유지가 옳음**. e2e 가 persona 환경 (실 backend 띄운 상태)
에서만 도는 별도 라이프사이클이라 일반 CI 에서는 영향 0. 단 BACKEND 띄워
실행 시 `allocator_names == {3종}` 단언이 4종 응답을 받아 fail 함을 인지
필요. 결정 필요 시점은 persona harness 재실행 시점에 Manager 가 정책 재고:
- 옵션 A (현재): persona = MVP 정의 그대로 → ma_signal 응답이 와도
  "subset 검증" 으로 변경 (`{"fixed_weight","all_weather","equal_weight"}
  ⊆ allocator_names`).
- 옵션 B: persona 도 4종 strict 검증으로 격상 (= L499 MVP 카운트도 4 로).

본 태스크 범위 밖이라 갱신 안 함. **Manager 후속 결정 권고** (severity=
observation).

### 관찰 3 — `tests/golden/test_golden_scenarios.py:377` 의 baseline 매트릭스

```
@pytest.mark.parametrize("strategy_name",
    ["fixed_weight", "all_weather", "equal_weight"])
```

9 골든 스냅샷 (3 시나리오 × 3 전략) 의 **의도적 baseline 락**. ma_signal
은 별도 시나리오로 추가하려면 새 스냅샷 픽스처 (BTC 100% + window=120 +
quarterly 등) 가 필요해 별건 태스크. 회귀 0 보호 목적이지 하드코딩 누락 아님.

### 관찰 4 — Coder report 의 fuzz 6 실패 (본 태스크 무관)

`test_api_contract_fuzz[*]` 6 건은 ma_signal 추가 전부터 실패 (DB 의존 +
schemathesis 비결정성). 본 태스크 미영향. 별건 처리 권고.

## 다음 제안

1. **TASK-221 처리 완료** — `tests/api/test_api_contract.py:78-94` 갱신 +
   PASS 확인. Manager 가 task #11 [pending] → DONE 으로 마감.

2. **persona e2e 처리** (관찰 2) — 옵션 A/B 중 결정 필요. 권장: 옵션 A
   (subset 검증). 근거: L499 MVP 정의를 보존하면서 사용자 추가 항목과
   분리, 추후 새 allocator 추가에도 회귀 안 남김. 별도 짧은 태스크로 등록
   가능 (예: `TASK-222 Tester: test_persona_first_use.py allocator subset
   화`).

3. **utils 추출 시점 (관찰 1)** — Coder report 다음 제안 4 와 동일. 5 번째
   allocator 추가 시점에 `_validate_weight_dict(...)` helper 분리 권고.

4. **frontend 수동 검증** — Coder report 가 명시한 DoD-d 보강. /backtests/new
   의 전략 드롭다운에 ma_signal 표시 + AssetWeightMap 자동 렌더 확인.
   Tester 권한 밖 (Manager/사용자 수동).

## TASK-221 처리 결과 (별도 섹션)

- **수정 파일**: `tests/api/test_api_contract.py:78-94` (1 함수 갱신).
- **변경 내용**:
  - `len(body["allocators"]) == 3` → `== 4`
  - `names == {3종}` → `== {4종}` + `assert "ma_signal" in names` 추가
  - docstring 갱신 + TASK-221 근거 주석.
- **검증**: `pytest test_strategies_endpoint_returns_mvp_presets -v` → PASS.
  형제 `test_health_endpoint`, `test_openapi_endpoint` 도 함께 PASS (회귀 0).
- **set-based 단언 채택 근거**: Coder report 다음 제안 1 권고 + "추후
  allocator 5 번째 추가 시 set 의 strict equality 가 즉시 fail 해 회귀
  알림" → 카운트 단언 + set 단언 둘 다 유지가 안전망 최대.
- **다른 동일 패턴 grep**: `tests/e2e/test_persona_first_use.py` 와
  `tests/golden/test_golden_scenarios.py` 에서 hit 2 건 → 관찰 2/3 참조,
  본 태스크 범위 밖으로 분리.

## 환경 노트

본 검증은 `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` 로 실행 — host anaconda
환경의 `dash` pytest 플러그인이 jupyter comm 미초기화로
`NotImplementedError` 를 던져 collection 자체가 실패하기 때문 (코드 결함
아닌 환경 의존). docker compose 에는 backend 컨테이너가 없어 host python
직접 실행이 정책. host 에 schemathesis/pydantic-settings 등 backend
의존성이 없어 본 검증 중 anaconda 환경에 추가 설치 (test_api_contract
collection 가능 상태로 만든 것) — 영구 영향 무. severity=environment 도
아닌 단순 환경 노트 (Tester 가 자체 해결 가능 영역).
