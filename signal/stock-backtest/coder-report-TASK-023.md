---
agent: coder
task_id: TASK-023
status: DONE
severity: none
parallel: true
date: 2026-04-29
---

# TASK-023: APScheduler cron 잡 (KR 18:00 / US 07:00 / CRYPTO 09:00 KST, 시장별 독립)

## 변경된 파일

### 신규
- `backend/app/scheduler/cron_jobs.py` (122 라인 — `KST_TZ` 상수 + `_run_market_backfill(market)` 잡 콜러블 + `build_scheduler(on_kr=, on_us=, on_crypto=)` 빌더)

### 수정 (append-only)
- `backend/app/scheduler/__init__.py` — 기존 docstring 끝에 TASK-023 한 줄 추가, `BackfillQueue` re-export 블록 아래에 `from app.scheduler.cron_jobs import KST_TZ, build_scheduler` append. `__all__` 에 `KST_TZ`, `build_scheduler` 추가. 기존 BackfillQueue 라인은 무변경 (TASK-031 산출물 보호).

## DoD 결과

모든 검증은 프로젝트 venv (`/home/jai/pa/stock-backtest/projects/stock-backtest/.venv/bin/python`, APScheduler 3.11.2) 로 실행. `cd backend && python -c "..."` 형태.

### 1) Import 검증
```
$ python -c "from app.scheduler.cron_jobs import build_scheduler, _run_market_backfill, KST_TZ; print('ok'); print(KST_TZ)"
DoD-1 import: ok
KST_TZ = Asia/Seoul
```

### 2) Scheduler 빌드 + 잡 등록
```
$ python -c "from app.scheduler.cron_jobs import build_scheduler; s = build_scheduler(); [print((j.id, j.name, str(j.trigger))) for j in s.get_jobs()]"
('backfill_kr',     'KR daily backfill (18:00 KST)',           "cron[hour='18', minute='0']")
('backfill_us',     'US daily backfill (07:00 KST, next day)', "cron[hour='7', minute='0']")
('backfill_crypto', 'Crypto daily backfill (09:00 KST)',       "cron[hour='9', minute='0']")
```

### 3) 3개 잡 등록 + KST timezone assertion
```
DoD-3: 3 jobs registered with KST timezone — ok
```
- `len(jobs) == 3` ✓
- 잡 ID 3종 (`backfill_kr`, `backfill_us`, `backfill_crypto`) 모두 존재 ✓
- 각 잡의 `trigger.timezone == 'Asia/Seoul'` ✓ (KST 자정 경계 버그 방지)

### 4) Mock 콜백 주입 + 발화 검증
```
$ python -c "
calls = []
s = build_scheduler(
    on_kr=lambda: calls.append('KR'),
    on_us=lambda: calls.append('US'),
    on_crypto=lambda: calls.append('CRYPTO'),
)
for j in s.get_jobs():
    j.func()
"
DoD-4 mock-injectable: ok — calls= ['KR', 'US', 'CRYPTO']
```
디폴트 `_run_market_backfill` 대신 mock 콜러블이 정확히 매칭되어 실행됨 (테스트가 백그라운드 워커 / 실제 DB 없이도 잡 와이어링 검증 가능).

### 5) 패키지 re-export
```
$ python -c "from app.scheduler import BackfillQueue, build_scheduler, KST_TZ; print('ok')"
package re-export: ok
KST_TZ via package: Asia/Seoul
```
TASK-031 의 `BackfillQueue` re-export 와 공존 — append-only 원칙 준수.

> 참고: 모든 검증 출력에 보이는 `KRX 로그인 실패: KRX_ID 또는 KRX_PW 환경 변수가 설정되지 않았습니다.` 는 pykrx 패키지가 import 시점에 출력하는 기존 모듈 레벨 경고로, 본 태스크의 cron_jobs 와 무관 (PykrxSource 가 import 되면 무조건 출력됨, 실제 cron 동작에는 영향 없음).

> scheduler.start() 백그라운드 워커 기동은 DoD 에서 제외 — TASK-061 FastAPI lifespan 통합 시 검증.

## 신규 Public API

### `app.scheduler.cron_jobs` (or `app.scheduler` 패키지 경유)

| 심볼 | 종류 | 용도 |
|------|------|------|
| `KST_TZ` | `str` 상수 (`"Asia/Seoul"`) | 잡 / 트리거 timezone 통일 |
| `build_scheduler(on_kr=None, on_us=None, on_crypto=None) -> BackgroundScheduler` | 함수 | 3개 cron 잡 등록된 BackgroundScheduler 빌더. on_* 디폴트 None → `_run_market_backfill(market)` 사용, 테스트는 mock 주입 |
| `_run_market_backfill(market: Market) -> None` | 함수 (내부 디폴트 잡) | 단일 시장 SessionLocal 자체 생성 후 `backfill_active_assets({market: source})` 호출. 시장별 라우팅 + 잡 격리 (try/except + logger.exception) |

잡 ID 규약:
- `backfill_kr`     → CronTrigger(hour=18, minute=0, tz=Asia/Seoul) → pykrx (한국 장 마감 +2.5h 여유)
- `backfill_us`     → CronTrigger(hour=7,  minute=0, tz=Asia/Seoul) → yfinance (US 장 마감 다음 날 KST 오전)
- `backfill_crypto` → CronTrigger(hour=9,  minute=0, tz=Asia/Seoul) → yfinance (24/7 시장, 임의 고정 시각)

`replace_existing=True` 라 lifespan 핫리로드 / 재시작 시 동일 잡 ID 충돌 안전.

## 클린 아키텍처 점검

- **얇은 잡 정의**: `cron_jobs.py` 는 잡 등록 + 시장 라우팅만. 실제 백필 로직은 전부 `app.data.pipeline.backfill_active_assets` 에 위임 (단일 책임 + 재사용).
- **DI**: `on_kr` / `on_us` / `on_crypto` 콜러블 주입으로 mock 가능. 테스트가 BackgroundScheduler 인스턴스 / 트리거 매칭 / 콜백 발화를 검증할 수 있음 (DoD-4).
- **시장별 독립**: 각 잡은 별도 콜러블 + 별도 SessionLocal + 자체 try/except 로 격리. 한 시장의 예외가 다른 시장 잡에 절대 전파되지 않음 (`_run_market_backfill` 의 외부 catch + APScheduler 자체 잡 격리, 이중 안전망).
- **세션 수명**: cron 잡은 FastAPI request scope 외부 → `with SessionLocal() as session:` 으로 잡 단위 자체 관리. `backfill_active_assets` 내부에서 자산 단위 commit/rollback 격리.
- **상수화**: `KST_TZ = "Asia/Seoul"` 모듈 레벨 상수로 BackgroundScheduler / 모든 CronTrigger 가 동일 timezone 공유 (자정 경계 버그 방지).
- **부트스트랩 분리**: `scheduler.start()` 호출은 본 모듈에 두지 않음 → 단위 테스트에서 백그라운드 스레드 없이 빌드만 검증 가능. start/stop 은 TASK-061 lifespan 책임.
- **타입 힌트 + Market literal**: `_run_market_backfill(market: Market)` 가 `app.domain.asset.entity.Market` literal 사용 → KR/US/CRYPTO 외 값이 들어오면 정적 타입 체크에서 차단.

## 다음 제안 (TASK-061 — FastAPI main.py lifespan 통합)

`main.py` 의 lifespan context manager 에서:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.scheduler import build_scheduler, BackfillQueue
from app.data.pipeline import backfill_asset

@asynccontextmanager
async def lifespan(app: FastAPI):
    # cron 잡: 시장별 일일 백필 (KR 18:00 / US 07:00 / CRYPTO 09:00 KST)
    cron_scheduler = build_scheduler()
    cron_scheduler.start()

    # 사용자 자유 추가 자산 백필 큐 (TASK-031)
    backfill_q = BackfillQueue(
        backfill_runner=lambda asset_id: backfill_asset(...),  # session/source 주입 wrapper
        max_workers=1,
    )
    backfill_q.start()
    app.state.cron_scheduler = cron_scheduler
    app.state.backfill_queue = backfill_q

    yield

    # graceful shutdown
    cron_scheduler.shutdown(wait=False)
    backfill_q.stop()

app = FastAPI(lifespan=lifespan)
```

권장:
- `cron_scheduler.shutdown(wait=False)` 로 lifespan 종료 시 빠르게 종료 (실행 중인 백필은 자산 단위 commit 으로 손실 없음).
- 운영 환경 (Docker) 에서 컨테이너 timezone 이 UTC 여도 BackgroundScheduler 와 모든 CronTrigger 가 `Asia/Seoul` 명시이므로 OS timezone 영향 없음.
- 통합 검증은 TASK-061 에서 `app.state.cron_scheduler.get_jobs()` 가 3개 반환하는지 + `next_run_time` 이 KST 기준으로 맞는지 확인.

## 충돌 없음

- 보호 파일 (`backfill_queue.py`, `data/`, `domain/`, `api/`, `models/`) 모두 read-only 로 참조만 함.
- `scheduler/__init__.py` 는 append-only 로 TASK-031 의 `BackfillQueue` re-export 블록 위에 docstring 한 줄 추가 + 아래에 cron_jobs re-export 추가. 기존 라인 무변경.
- 병렬 진행 중인 TASK-045 / TASK-050 / TASK-053 와 파일 교차 없음.
