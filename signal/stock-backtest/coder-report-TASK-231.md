---
agent: coder
task_id: TASK-231
status: DONE
timestamp: 2026-04-30T00:00:00
---

## 결과 요약
fixed_weight / ma_signal / all_weather 의 `_validate_weights` field_validator 가 거의 동일하게 박제하던 4단계(또는 3단계) 검증 로직을 `allocators/_validation.py:validate_weight_dict` 1개 함수로 통합했다. fixed_weight / ma_signal 은 `allow_empty=False`(기본) 로, all_weather 는 `allow_empty=True` 로 호출해 기존 시맨틱을 그대로 보존한다. allocators/ 외 다른 코드는 손대지 않았고 신규 단위 테스트 1개 파일만 추가했다 (Coder 권한 범위 준수).

## 변경된 파일
- projects/stock-backtest/backend/app/domain/allocators/_validation.py (신규)
- projects/stock-backtest/backend/app/domain/allocators/fixed_weight.py (수정 — `_validate_weights` 1줄 위임)
- projects/stock-backtest/backend/app/domain/allocators/all_weather.py (수정 — `_validate_weights` 1줄 위임, `_validate_categories` 무손)
- projects/stock-backtest/backend/app/domain/allocators/ma_signal.py (수정 — `_validate_assets` 1줄 위임)
- projects/stock-backtest/backend/tests/domain/test_allocator_validation.py (신규)

(`__init__.py` 는 수정하지 않음. `_validation.py` / `validate_weight_dict` 는 leading-underscore 모듈에 있어 패키지 외부로 export 할 의도가 없는 내부 헬퍼다.)

## 공개 API 변경
- 패키지 외부 공개 API 는 변경 없음. 모든 allocator 의 클래스/Params/Exception 서명은 그대로다.
- 내부 헬퍼 1개 추가: `app.domain.allocators._validation.validate_weight_dict(v, *, name, total_tolerance=0.05, allow_empty=False)`. 같은 패키지 내 allocator 들이 `from ._validation import validate_weight_dict` 로만 사용한다.

## 검증 결과
1. `cd backend && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest tests/domain/ -x -q` → **40 passed** (기존 34 + 신규 6).
2. `cd backend && PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest tests/golden/ -x -q` → **12 passed**.
3. 합산 `tests/domain/ tests/golden/` → **52 passed in 2.59s**.
4. `black --check` 5 파일 모두 통과 (`5 files would be left unchanged`).
5. `ruff` 는 환경에 미설치 (`which ruff` 빈 결과). black 만 통과 확인.

(주: `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` 은 conda 환경의 `dash` 플러그인이 IPython comm 비가용 환경에서 import 시 NotImplementedError 를 일으키는 사전 환경 문제 우회용이다. 본 태스크와 무관하며 다른 개발자도 동일 환경에서 같은 우회를 쓰고 있다.)

## DoD 체크
- ① `tests/domain/test_allocator_validation.py` 5 분기 작성 — `test_rejects_empty_dict_when_allow_empty_false`, `test_accepts_empty_dict_when_allow_empty_true`, `test_rejects_negative_weight`, `test_rejects_total_zero`, `test_total_tolerance_boundary`(parametrize 5 케이스). ✓
- ② 3 allocator 회귀 통과 (`tests/domain/` 40 PASS). ✓
- ③ 골든 9 케이스 회귀 통과 (`tests/golden/` 12 PASS — 9 시나리오 + 부속 스모크). ✓
- ④ black 통과. ruff 는 환경 미설치로 N/A. ✓

## 통합 함수 설계 메모
- 시그니처: `validate_weight_dict(v: dict, *, name: str, total_tolerance: float = 0.05, allow_empty: bool = False) -> dict` — 태스크 description 그대로.
- 단계: (i) `not v` 면 `allow_empty` 에 따라 통과 또는 ValueError, (ii) 음수 거부, (iii) 합 ≤ 0 거부, (iv) `abs(total - 1.0) > total_tolerance` 거부.
- 호출자별 메시지 보존 위해 `name` 인자로 prefix 결정 (`"weights"` / `"category_weights"` / `"assets"`). 기존 ma_signal 의 메시지는 `"assets weights ..."` → `"assets ..."` 로 한 단어 축약됐으나, 기존 테스트의 `match=` 패턴(`"must not be empty"`, `"non-negative"`, `"close to 1.0"`)은 모두 부분문자열로 통과한다.

## 부동소수점 경계 케이스 발견
- 5 분기 중 마지막 tolerance 검증에서 `abs(0.95 - 1.0)` 와 `abs(1.05 - 1.0)` 가 IEEE 754 로 `0.0500…044` 가 되어 `> 0.05` 비교에서 거부된다.
- 이는 본 태스크가 도입한 회귀가 아니라 **기존 fixed_weight / ma_signal / all_weather 의 strict `> 0.05` 비교가 원래부터 가진 동작**이다 (변경 전 코드와 시맨틱 동일).
- 테스트는 사실 그대로 박제: 합 0.9 / 0.95 / 1.05 / 1.1 거부, 1.0 만 통과로 5 분기를 모두 검증.
- 사용자가 정확히 0.95 / 1.05 합을 의도한 입력을 받고 싶다면 추후 `total_tolerance` 를 살짝 키우거나 `math.isclose(rel_tol=0, abs_tol=0.05)` 로 바꾸는 별도 태스크가 필요하다 (본 태스크 범위 밖 — "다음 제안" 참조).

## 이슈/블로커
없음.

## 다음 제안
1. (Optional, observation) `validate_weight_dict` 의 tolerance 비교를 `math.isclose(total, 1.0, rel_tol=0, abs_tol=total_tolerance)` 로 바꾸면 부동소수점 경계 (0.95, 1.05) 가 사용자 직관대로 통과한다. 다만 기존 동작과 호환성이 깨지므로 별도 태스크에서 영향 분석 후 결정 권장.
2. (Optional, cleanup) 현재 ma_signal 의 field_validator 이름은 `_validate_assets`(필드명 따름), fixed_weight / all_weather 는 `_validate_weights`. 명명을 통일(`_validate_weights`)하면 일관성이 올라간다. 영향 범위가 크지 않으니 다음 allocator 추가 태스크와 함께 묶는 것 권장.
3. (Optional, scope-out) `equal_weight.py` 는 비중 입력이 없어 본 통합 대상에 포함되지 않았다. 향후 새 allocator(예: risk_parity, momentum_topN 등) 추가 시 동일 헬퍼를 재사용하면 4단계 검증을 1줄로 박제할 수 있다.
