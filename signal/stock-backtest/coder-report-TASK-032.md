---
agent: coder
task_id: TASK-032
status: DONE
timestamp: 2026-04-29T15:00:00
---

## 결과 요약
universe 자산 데이터 가용 구간과 사용자 요청 백테스트 기간을 비교해 자동 조정 + 한국어 통지 메시지를 생성하는 도메인 서비스 추가. `PeriodAdjustment` (frozen dataclass) + `adjust_period_for_universe()` 함수 + `AdjustmentReason` Literal 을 도메인 레이어에 신설하고 `app.domain.asset` 패키지에서 re-export.

## 변경된 파일
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/domain/asset/period_adjustment.py (신규)
- /home/jai/pa/stock-backtest/projects/stock-backtest/backend/app/domain/asset/__init__.py (수정 — re-export 3개 추가)

## 도메인 순수성
AST 분석 결과 import 모듈: `__future__`, `dataclasses`, `datetime`, `typing`, `entity` (상대 import).
SQLAlchemy / FastAPI / yfinance / pykrx / app.models / app.data 의존 0건. 도메인 순수 통과.

## 6개 케이스 검증 결과

| # | 케이스 | reason | adjusted_start | adjusted_end | affected | 결과 |
|---|--------|--------|----------------|--------------|----------|------|
| 1 | 빈 universe | `no_data` | 요청 그대로 | 요청 그대로 | () | PASS — "universe 가 비어 있습니다. 자산을 1개 이상 추가하세요." |
| 2 | start_date None 자산 포함 (SPY 정상 + QQQ 미백필) | `no_data` | 요청 그대로 | 요청 그대로 | (`QQQ`,) | PASS — "다음 자산의 데이터가 아직 백필되지 않았습니다: QQQ. 백필 완료 후 백테스트를 시도하세요." |
| 3 | 사용자 요청 기간이 universe 안에 완전히 포함 | `ok` | 2015-01-01 | 2024-12-31 | () | PASS — was_adjusted=False, "기간이 사용자 요청대로 적용됐습니다." |
| 4 | 사용자 요청 시작일이 universe 시작일보다 이름 (SPY 2018-01-01 > req 2015-01-01) | `universe_start_later` | 2018-01-01 | 2024-12-31 | (`SPY`,) | PASS — "시작일이 2018-01-01 로 자동 조정됐습니다. SPY 의 데이터 시작일이 2018-01-01 이기 때문입니다." |
| 5 | 사용자 요청 종료일이 universe last_ingested_at 보다 늦음 (SPY 2024-06-30 < req 2024-12-31) | `universe_end_earlier` | 2015-01-01 | 2024-06-30 | (`SPY`,) | PASS — "종료일이 2024-06-30 로 자동 조정됐습니다. SPY 의 마지막 백필일이 2024-06-30 이기 때문입니다." |
| 6 | 양쪽 다 조정 (SPY start 2018-01-01 + last_ingested 2024-06-30) | `universe_start_later` (통합) | 2018-01-01 | 2024-06-30 | (`SPY`, `SPY`) | PASS — "기간이 자동 조정됐습니다: 2018-01-01 ~ 2024-06-30. 시작일은 SPY, 종료일은 SPY 의 데이터 가용 구간 때문입니다." |

전 케이스 한국어 메시지 + frozen dataclass 불변성 + `was_adjusted` 속성 동작 확인.

추가 DoD 체크:
- import 검증: `from app.domain.asset import PeriodAdjustment, adjust_period_for_universe, AdjustmentReason` → ok.
- 도메인 순수성 AST 검증: banned import 0개.

## 이슈/블로커
없음.

다만 한 가지 설계 관찰 (블로커 아님, observation 수준):
- Case 6 처럼 시작·종료 둘 다 동일 자산이 원인이면 `affected_assets` 가 `('SPY', 'SPY')` 처럼 중복으로 들어간다. 호출자가 UI 노출 시 `set` 으로 dedup 해도 무방하나, 도메인에서 중복 제거를 했어야 할지는 토론 여지가 있다. 현재는 "어느 쪽 영향인지 추적 가능" 을 우선해 중복 허용. UI 가 dedup 하길 원하면 후속 태스크에서 `affected_start_assets`, `affected_end_assets` 분리 고려.

## 다음 제안

TASK-031 (자유 추가 워크플로우 / 백테스트 실행 폼) 에서 본 서비스 활용 권고:

1. **API 레이어 통합** — 사용자가 백테스트 폼 제출 시 (universe + 시작/종료일 선택), API 핸들러는:
   ```python
   adjustment = adjust_period_for_universe(universe, req_start, req_end)
   if adjustment.reason == "no_data":
       return 400, {"error": adjustment.message}  # 사용자에게 백필 안내
   if adjustment.was_adjusted:
       # 조정된 기간으로 진행 + UI 에 message 노출 (toast/banner)
       run_backtest(universe, adjustment.adjusted_start, adjustment.adjusted_end)
       return 200, {"adjusted": True, "message": adjustment.message, ...}
   ```
2. **프론트 Pydantic/Zod 스키마** — `PeriodAdjustment` 를 그대로 직렬화 가능하므로 응답 envelope 에 `period_adjustment: {...}` 필드 추가. 프론트는 `was_adjusted` 분기로 banner 표시.
3. **테스트 (TASK-032-T 권고)** — Tester 가 본 서비스에 대한 단위 테스트 6개 케이스를 별도 작성 (`tests/domain/asset/test_period_adjustment.py`). 본 작업에서는 도메인 코드만 작성했고 정식 pytest 모듈은 추후 Tester 가 처리.
4. **calendar_guard 통합 옵션** — `adjusted_start`/`adjusted_end` 가 거래일이 아닐 수 있다 (주말/공휴일). API 핸들러에서 `guard_trading_day(..., mode="next")` / `mode="prev")` 로 한 번 더 보정해 백테스트 엔진에 전달하는 흐름 권장.