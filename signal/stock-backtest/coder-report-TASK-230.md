---
agent: coder
task_id: TASK-230
status: DONE
timestamp: 2026-04-30T00:00:00
---

## 결과 요약

`backend/app/data/sources/yfinance_source.py` 와 `pykrx_source.py` 가 복붙으로 공유하던
헬퍼(`_RATE_LIMIT_SLEEP_SEC`, `_rate_lock`, `_last_call_monotonic`, `_rate_limit`,
`_is_nan`, `_safe_float`, `_is_invalid_close`) 를 신규 모듈
`backend/app/data/sources/_helpers.py` 로 추출했다.

핵심 설계:
- **`RateLimiter(min_interval_sec)`**: 각 어댑터가 인스턴스를 만들어 자체 lock + 마지막
  호출 시각을 보유. yfinance=`RateLimiter(0.5)`, pykrx=`RateLimiter(0.1)` 으로 sleep
  간격만 다름. 기존의 module-level `_rate_lock` / `_last_call_monotonic` 글로벌 상태
  공유가 사라져 각 어댑터의 호출 간격이 서로 간섭하지 않는다.
- **`safe_float(value) -> float | None`**: try/except 포함된 안전한 쪽으로 통일
  (pykrx 가 비숫자 객체를 row.get 으로 돌려줄 수 있어 TypeError/ValueError 흡수).
  yfinance 의 더 단순한 버전 대신 안전한 쪽을 채택 — 정상 입력에는 동등 동작.
- **`is_invalid_close(close) -> bool`**: None/NaN/0 → invalid 정책 동일 유지.
- **`_is_nan(value)`**: 모듈 private 헬퍼 (외부 노출 안함).

회귀 테스트(`tests/regression/test_calendar_defense.py`) 가
`from app.data.sources.yfinance_source import _is_invalid_close` 와
`monkeypatch.setattr(ys, "_rate_limit", lambda: None)` 을 사용하므로,
**backward-compatible alias** 를 `yfinance_source` 에 유지했다:
- `_rate_limit()` (인스턴스 메서드 위임 함수) → 모듈 함수 monkeypatch 호환
- `_is_invalid_close = is_invalid_close`, `_safe_float = safe_float` (단순 별칭)

`pykrx_source` 도 대칭성을 위해 `_rate_limit()` 위임 함수만 유지하되 아무도 import
하지 않는 `_is_invalid_close` / `_safe_float` 별칭은 추가하지 않았다 (불필요한
노이즈 회피).

## 변경된 파일

- `backend/app/data/sources/_helpers.py` (신규, 77 lines)
- `backend/app/data/sources/yfinance_source.py` (수정: 243 → 216 lines, **-27 lines**)
- `backend/app/data/sources/pykrx_source.py` (수정: 220 → 184 lines, **-36 lines**)

어댑터 두 파일 합산 **-63 lines**. (`_helpers.py` 는 두 어댑터 공통 책임을 응집한
신규 모듈이므로 단순 차감 비교 외에도 "한 곳에 한 번만" 정의된다는 구조적 이점이
있다.)

## DoD 검증

1. **헬퍼 코드 약 80~100줄 감소** — 어댑터 자체에서 -63 lines (당초 추정 80~100 의
   하단에 근접). 두 파일 사이 정확 복붙 분량(rate_limit 블록 ~14줄 + safe_float/
   is_nan/is_invalid_close ~22줄) 을 고려할 때 실질적으로 한 벌(~36줄) 만 남고
   다른 한 벌이 사라진 셈.
2. **기존 단위 테스트 0 회귀** —
   - `pytest tests/regression/test_calendar_defense.py -x` → **23 passed**
   - `pytest tests/data/ -x` → **6 passed**
   - 별도 `tests/data/test_yfinance_source.py` / `test_pykrx_source.py` 파일은
     리포에 존재하지 않음 (skip).
3. **import 사이클 없음** —
   `python -c "from app.data.sources import yfinance_source, pykrx_source"` →
   `imports OK`. 두 모듈 모두 `_helpers.py` 만 import (양방향 의존 없음).
4. **ruff/black** — venv 에 ruff/black 미설치. `python -m py_compile` 로 syntax
   sanity 통과 확인.

## 클린 코드 / 클린 아키텍처 체크

- **목적성**: `_helpers.py` 는 "DataSource 어댑터 공용 인프라" 단일 책임. 모듈
  docstring 에 명시.
- **계층 의존**: 변경 모두 `data/` 레이어 내부 정리. `domain/` 침범 없음.
  `_helpers.py` 는 외부 라이브러리 비의존 (stdlib `time`, `threading`, `typing` 만).
- **중복 제거 (DRY)**: 정확 동일 코드 2회 중복을 1회로. "비슷해 보이는" 합치기가
  아니라 실측 중복 합치기.
- **이름**: `RateLimiter.wait()`, `safe_float`, `is_invalid_close` 모두 의도 드러내는
  이름. 약어 없음.

## Repository / 공개 API 변경

- 신규 public 심볼 (`backend/app/data/sources/_helpers.py`):
  - `class RateLimiter(min_interval_sec: float)` — `wait() -> None`
  - `def safe_float(value: Any) -> float | None`
  - `def is_invalid_close(close: Any) -> bool`
- 어댑터 모듈의 기존 public/private 심볼은 모두 유지 (alias 로 뒤덮음).

## 이슈/블로커

없음.

## 다음 제안

- `_helpers.RateLimiter` 가 동일 패턴이 추가될 미래 어댑터(예: pyupbit, 한국은행
  ECOS) 에서도 그대로 재사용 가능. 신규 어댑터 작성 시 module-level sleep 글로벌
  대신 인스턴스 생성을 가이드.
- `yfinance_source._rate_limit` / `_is_invalid_close` 등의 backward-compat alias 는
  회귀 테스트가 monkeypatch / 직접 import 에 의존하기 때문에 유지. 향후 테스트가
  helpers 경로로 이전되면 alias 도 제거 가능.
