---
agent: coder
task_id: TASK-236
status: DONE
timestamp: 2026-04-30T11:35:00
---

## 결과 요약
`backend/app/domain/asset/registration.py` 의 `register_asset` 백필 큐잉 단계에서
`except Exception: enqueued = False` 의 silent swallow 를 제거했다. V3 silent
fallback 금지 원칙에 따라 `logger.warning("backfill enqueue failed asset_id=%d
symbol=%s: %s", ...)` 으로 자산 식별자·심볼·예외 메시지를 함께 emit 하고, 등록
자체는 그대로 성공시킨다 (다음 cron 주기 자동 수집). `BaseException` 분리는
`Exception` 으로 잡으므로 `KeyboardInterrupt` / `SystemExit` 가 자연 re-raise
되어 별도 처리 불필요. 코드 코멘트로 명시.

신규 단위 테스트 3건 (`backend/tests/domain/test_registration.py`) 작성 — Protocol
스텁 + `caplog` fixture 로 다음을 검증:
1. `enqueue` 가 `RuntimeError` raise → WARNING 1건 emit (asset_id=42 / SPY /
   "scheduler down" 모두 메시지 포함), `result.backfill_enqueued is False`,
   `result.note` 에 "백필 큐잉 실패" 문구.
2. 정상 enqueue 케이스 — WARNING emit 없음, `enqueued is True`.
3. `ValueError` 케이스 — RuntimeError 외 다른 Exception 도 동일하게 로깅 (회귀 방지).

## 변경된 파일
- projects/stock-backtest/backend/app/domain/asset/registration.py (수정)
  - `import logging` 추가 (line 14)
  - `logger = logging.getLogger(__name__)` 추가 (line 22)
  - L164-178: enqueue try/except 블록 수정 — `except Exception as exc:` 로 변경,
    `logger.warning(...)` 호출 추가, 정책 코멘트 보강.
- projects/stock-backtest/backend/tests/domain/test_registration.py (신규)

## 검증 결과
- `pytest tests/domain/test_registration.py -v`: 3 passed (0.29s)
- `pytest tests/domain/ --ignore=tests/domain/test_allocator_validation.py`:
  31 passed (test_calendar_guard, test_engine, test_ma_signal_allocator,
  test_registration, test_trade 전부 통과).
- `tests/domain/test_allocator_validation.py` 1건 실패 — TASK-236 범위 밖
  (다른 동시 Coder 작업의 allocator `_validation.py` 변경에서 유래한
  pre-existing 결함). git stash 후 HEAD 에서도 동일 실패 재현 가능 — 본 태스크
  와 무관함을 확인.
- `black --check tests/domain/test_registration.py`: 통과.
- `black --check app/domain/asset/registration.py`: 본 태스크 변경 라인은
  black 호환. 다른 부분 (DTO/Protocol 사이 빈 줄) 의 reformat 요구는 HEAD
  baseline 에서도 동일 (git stash 검증). TASK-236 변경 라인은 100% 호환이며
  파일 전체 reformat 은 별도 태스크 범위.
- `ruff` 는 venv 미설치로 스킵 (Manager 환경 정책 확인 필요. 신규 import 는
  `import logging` 한 건이라 unused import 등 위반 없음).

## 이슈/블로커
없음. 단, 위 검증 결과 항목의 `test_allocator_validation.py` 실패는 동일
세션의 다른 동시 Coder 작업 산출물에서 유래하므로 Manager 가 별개로 추적
필요.

## 다음 제안
- (선택) `app/domain/asset/registration.py` 전체에 black 적용 — 본 태스크 변경
  라인은 깨끗하지만 파일 baseline 이 black 미적용 상태. 별도 lint 정리 태스크로
  분리 권장.
- 다른 silent fallback 경로 — 동일한 V3 원칙 위반이 다른 모듈에 있는지 audit
  하는 grep 태스크 (예: `grep -rn "except Exception:\s*$\|except Exception:\s*\w\+\s*=\s*False" backend/app/`).
