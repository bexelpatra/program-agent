---
agent: coder
task_id: TASK-031
status: DONE
severity: none
parallel: true
date: 2026-04-29
---

# TASK-031: 자산 자유 추가 워크플로우 (도메인 서비스 + scheduler 큐잉)

## 변경된 파일

### 신규
- `backend/app/domain/asset/registration.py` (180 라인 — 도메인 서비스 + Protocol + DTO + 예외)
- `backend/app/scheduler/backfill_queue.py` (95 라인 — in-memory queue + threading 워커)

### 수정 (append-only)
- `backend/app/domain/asset/__init__.py` — 끝에 24 라인 append (TASK-031 re-export 블록). 기존 라인 0건 변경.
- `backend/app/scheduler/__init__.py` — 비어있던 파일에 패키지 docstring + `BackfillQueue` re-export 작성.

## DoD 결과

### 1) Import 검증
```
$ cd backend && python -c "from app.domain.asset.registration import register_asset, RegistrationRequest, RegistrationResult, TickerValidationFailed, AlreadyRegistered, TickerValidator, BackfillEnqueuer, ValidationOutcome; from app.scheduler.backfill_queue import BackfillQueue; print('ok')"
ok
```
패키지 경유 import 도 통과: `from app.domain.asset import register_asset, ...` / `from app.scheduler import BackfillQueue`.

### 2) 도메인 순수성 (registration.py)
- banned imports 검색 결과: **0건** (sqlalchemy / fastapi / yfinance / pykrx / app.data / app.models 모두 0).
- 사용 import: `dataclasses.dataclass`, `typing.Protocol`, `app.domain.asset.entity`, `app.domain.asset.repository`. 외부 프레임워크/벤더 의존 없음.
- domain 은 `TickerValidator` / `BackfillEnqueuer` Protocol 만 정의 — data/scheduler 어댑터는 외부에서 주입 (의존성 역전, Reviewer N5).

### 3) registration 단위 검증 (mock — 6 케이스)
```
case 1 pass: 정상 등록 + 큐잉
case 2 pass: 검증 실패 → TickerValidationFailed
case 3 pass: 중복 등록 → AlreadyRegistered
case 4 pass: inactive 자산 재등록 (PK 재사용)
case 5 pass: has_min_history=False → note 안내 ("최소 1년치 데이터 부족 …")
case 6 pass: 큐잉 실패 → 등록 유지 + note ("등록 완료. 백필 큐잉 실패로 …")
ALL registration unit tests pass
```
case 4·5·6 은 명세에 없던 엣지지만, 분기 커버리지 100% 를 위해 자체 추가 검증.

### 4) BackfillQueue 스모크
```
queue ran 3 backfills (calls=[1, 2, 3])           # 정상 enqueue 3건 → 모두 실행
flaky runner test pass: [1, 3]                     # asset_id=2 가 예외 던져도 워커는 살아남아 1·3 처리
```
runner 예외 시 logger.exception 으로 로그 남기고 워커는 계속 살아 있음을 검증 (rate-limit 보호 + 격리).

## 신규 Public API

### `app.domain.asset.registration` (or `app.domain.asset` 패키지 경유)

| 심볼 | 종류 | 용도 |
|------|------|------|
| `register_asset(request, repo, validator, enqueuer) -> RegistrationResult` | 함수 | 자산 자유 추가 도메인 서비스 (메인 진입점) |
| `RegistrationRequest` | frozen dataclass | 사용자 폼 입력 DTO (symbol, market, asset_type, currency, name, meta) |
| `RegistrationResult` | frozen dataclass | 결과 DTO (asset, backfill_enqueued, note) |
| `ValidationOutcome` | frozen dataclass | TickerValidator 반환 (ticker, exists, has_min_history, earliest_date, note) |
| `TickerValidator` | Protocol | data 어댑터 인터페이스 — `validate_ticker(symbol) -> ValidationOutcome` |
| `BackfillEnqueuer` | Protocol | scheduler 어댑터 인터페이스 — `enqueue(asset_id) -> None` |
| `TickerValidationFailed` | Exception | 즉시 검증 실패 (사용자 노출 한국어 message) |
| `AlreadyRegistered` | Exception | 동일 (symbol, market) active 중복 |

### `app.scheduler.backfill_queue` (or `app.scheduler`)

| 심볼 | 종류 | 용도 |
|------|------|------|
| `BackfillQueue(backfill_runner, max_workers=1)` | 클래스 | in-memory queue + threading 백필 워커. `BackfillEnqueuer` Protocol 구현 |
| `.start()` / `.stop()` / `.enqueue(asset_id)` | 메서드 | lifespan 에서 start/stop, 도메인에서 enqueue 호출 |

## 클린 아키텍처 점검

- **레이어 분리**: domain/asset/registration.py 는 data/scheduler 를 직접 import 하지 않고 Protocol 로 의존성 역전. 어댑터 교체 시 domain 코드 수정 불필요.
- **POPO**: 모든 DTO 는 `@dataclass(frozen=True)` — SQLAlchemy/Pydantic 의존 없음.
- **earliest_date 타입**: `ValidationOutcome.earliest_date` 는 `object | None` 으로 받아 datetime.date import 가 도메인 서명에 노출되지 않도록 함 (Protocol 구현체는 date 를 넣어도 OK).
- **한국어 에러 메시지** (UI/UX 원칙 2): `TickerValidationFailed` / `AlreadyRegistered` / `RegistrationResult.note` 모두 한국어. 그대로 토스트/배너에 노출 가능.
- **단순성 우선**: BackfillQueue 는 `queue.Queue` + `threading.Thread` 만 사용 — APScheduler/Celery 의존 0건. Protocol 만 유지하면 향후 자유롭게 교체.
- **워커 격리**: runner 예외는 워커 루프에서 catch + logger.exception. 한 자산 백필 실패가 다른 자산 백필을 막지 않음 (스모크 case 2 로 검증).

## 다음 제안 (TASK-061 자산 API 가 사용할 와이어링)

TASK-061 (POST `/api/assets`) 핸들러에서 다음과 같이 의존성 주입:

```python
# main.py / lifespan
from app.scheduler import BackfillQueue
from app.data.pipeline import backfill_asset  # TASK-022

backfill_q = BackfillQueue(backfill_runner=backfill_asset, max_workers=1)
backfill_q.start()  # lifespan 시작 시
# lifespan 종료 시: backfill_q.stop()

# api/assets.py
from app.domain.asset import register_asset, RegistrationRequest, TickerValidationFailed, AlreadyRegistered

@router.post("/assets")
def post_asset(body: AssetCreateSchema, repo: AssetRepository = Depends(...), validator: TickerValidator = Depends(...)):
    try:
        result = register_asset(
            RegistrationRequest(...body...),
            repo=repo,
            validator=validator,
            enqueuer=backfill_q,   # FastAPI app.state 또는 별도 Depends 로 주입
        )
        return {"asset_id": result.asset.asset_id, "backfill_enqueued": result.backfill_enqueued, "note": result.note}
    except AlreadyRegistered as e:
        raise HTTPException(409, detail=str(e))
    except TickerValidationFailed as e:
        raise HTTPException(422, detail=str(e))
```

권장:
- HTTP 상태 매핑 — `AlreadyRegistered` → 409, `TickerValidationFailed` → 422.
- `TickerValidator` 구현체는 data 레이어에 신규 클래스 (예: `app.data.sources.MarketTickerValidator`) — yfinance/pykrx 어댑터를 market 별 분기. TASK-061 또는 별도 data-side 태스크에서 처리.
- `BackfillQueue` 는 lifespan 시작 시 1회 생성, app.state.backfill_queue 에 보관 후 Depends 로 주입하면 단위 테스트에서도 쉽게 stub 가능.

## 충돌 없음

- TASK-043/044 가 건드리는 `backend/app/domain/__init__.py` 는 이번 변경에서 미접근.
- 기타 보호 파일 (entity/repository/calendar_guard/period_adjustment, data/sources, data/repositories, data/asset_repository, data/pipeline) 모두 read-only 로 참조만 함.
