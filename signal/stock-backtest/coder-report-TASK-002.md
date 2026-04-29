---
agent: coder
task_id: TASK-002
status: DONE
timestamp: 2026-04-29T08:00
---

## 결과 요약

SQLAlchemy 2.0 + Alembic 초기 설정을 완료했다. `.env` 의 `DATABASE_URL` 을 단일 소스로 삼아 런타임(`app.core.config.Settings`) 과 마이그레이션(`alembic/env.py`) 모두에 주입하도록 구성했다. import 스모크 검증(설정 로드 + Engine/Base/SessionLocal 인스턴스화)은 모두 통과. `alembic current` 는 DB 연결까지 성공했으나 외부 사유(이전 환경 잔존 `alembic_version='0003'`)로 revision lookup 단계에서 실패 — SOFT BLOCKER-001 로 분리 등록.

## 변경된 파일

- `projects/stock-backtest/backend/alembic/` (신규, `alembic init` 결과)
  - `env.py` (커스터마이즈: `app.core.config` / `app.core.db.Base` 주입, `app.models` 자동 import)
  - `script.py.mako` (init 기본값 그대로)
  - `README` (init 기본값 그대로)
  - `versions/` (빈 디렉토리)
- `projects/stock-backtest/backend/alembic.ini` (신규, `sqlalchemy.url` 빈 값으로 변경)
- `projects/stock-backtest/backend/app/core/config.py` (신규)
- `projects/stock-backtest/backend/app/core/db.py` (신규)
- `signal/stock-backtest/blockers.md` (BLOCKER-001 SOFT 추가)

## 모듈 책임 분리

| 파일 | 책임 |
|------|------|
| `app/core/config.py` | `pydantic_settings.BaseSettings` 기반 환경변수 로드만. DB 객체 생성 금지. `get_settings()` 는 `lru_cache(1)`. |
| `app/core/db.py` | `engine` / `SessionLocal` / `Base(DeclarativeBase)` / `get_db()` 제너레이터만. 비즈니스 로직 금지. |
| `alembic/env.py` | `app.core.config.get_settings().database_url` 을 alembic context 에 주입 + `Base.metadata` → `target_metadata`. |

## 공개 API (신규)

`app.core.config`:
- `class Settings(BaseSettings)` — 필드: `database_url: str`, `database_url_test: str | None`, `default_base_currency: str = "KRW"`, `tz: str = "Asia/Seoul"`
- `get_settings() -> Settings` (lru_cache)

`app.core.db`:
- `engine: sqlalchemy.Engine` (`pool_pre_ping=True`, `future=True`)
- `SessionLocal: sessionmaker[Session]` (`autoflush=False`, `autocommit=False`, `expire_on_commit=False`)
- `class Base(DeclarativeBase)` — 모든 모델의 단일 메타데이터 베이스
- `get_db() -> Iterator[Session]` — FastAPI Depends 용

## DoD 검증 결과

### 1) `python -c "from app.core.config import get_settings; print(get_settings().database_url)"`
출력: `postgresql://stock:stock@localhost:5432/stock_backtest` — PASS

### 2) `python -c "from app.core.db import engine, Base, SessionLocal; print(engine.url, Base, SessionLocal)"`
출력: `postgresql://stock:***@localhost:5432/stock_backtest <class 'app.core.db.Base'> sessionmaker(class_='Session', ...)` — PASS

### 3) `alembic current` (또는 `alembic check`)
- DB 연결 성공 (Postgres 도달, `alembic_version` 행 조회까지 진행)
- 그러나 `Can't locate revision identified by '0003'` 로 실패
- 원인: DB(`stock_backtest`)에 이전 환경 잔존 데이터(11개 테이블 + `alembic_version='0003'`) 존재. 새 `versions/` 는 비어 있음 — TASK-002 코드 결함이 아닌 외부 DB 상태 문제.
- 조치: SOFT BLOCKER-001 등록. import 검증(1·2)은 통과하므로 DoD 명세대로 status=DONE 보고.

## 이슈/블로커

- **BLOCKER-001 [SOFT]** (TASK-002): 기존 DB 의 `alembic_version='0003'` 행과 빈 `versions/` 의 불일치. 후속 마이그레이션 태스크(TASK-010+)에서 새 baseline revision 을 만들거나, 사용자가 `drop schema public cascade; create schema public;` 으로 초기화 후 새 revision 적용해야 한다. 자세한 내용은 `signal/stock-backtest/blockers.md` 참조.

## 클린 코드 / 클린 아키텍처 점검

- `config.py` ↔ `db.py` 책임 분리 완료. `config.py` 는 SQLAlchemy import 없음.
- 두 모듈 모두 `app.domain.*` 에 의존하지 않음 (역방향 OK, 단방향 유지).
- `alembic/env.py` 가 `sys.path` 에 backend/ 를 강제 삽입하는 이유는 주석으로 명시 (`alembic` 실행 컨텍스트가 backend/ 외부에서도 동작하도록 보호).
- `alembic.ini` 의 `sqlalchemy.url` 을 빈 값으로 두는 이유는 inline 주석으로 명시 (`.env` 단일 소스 정책).

## 다음 제안

1. **TASK-010 (DB 모델 정의) 진행 시 주의**: `app.models.__init__.py` 에서 모든 모델을 `__all__` 또는 직접 import 로 노출해야 `alembic/env.py` 의 `import app.models` 한 줄로 `Base.metadata` 가 채워진다.
2. **BLOCKER-001 해소 경로 결정 필요** (Manager 판단):
   - (a) 기존 DB 를 drop+recreate 후 `alembic revision --autogenerate -m "init"` 로 새 baseline 생성
   - (b) 기존 DB 스키마를 그대로 두고 0001~0003 더미 revision 파일을 작성해 history 정합성 회복
   - V3 신규 프로젝트라면 (a) 권장.
3. **`Base = DeclarativeBase` 서브클래스** 방식을 택했다 (SQLAlchemy 2.0 권장). 모델 정의 시 `class MyModel(Base): __tablename__ = "..."` 패턴 사용.
