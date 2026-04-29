---
agent: coder
task_id: TASK-030
status: DONE
timestamp: 2026-04-29T08:30:00
---

## 결과 요약

architecture.md V3 § "자산 도메인 모델" L514-555 + § "백엔드 모듈 분할" L646~ 에 따라
Asset / Universe 도메인 모델 + Repository Protocol + 비거래일 방어 + SQLAlchemy 구현체를 작성했다.
domain 레이어는 SQLAlchemy/FastAPI/yfinance/pykrx 의존을 완전히 배제했고
(exchange_calendars 만 도메인 정책상 허용), data 레이어가 Protocol 을 덕 타이핑으로 구현해
의존성 역전을 이룬다.

DoD 1~4 모두 통과했다.

## 변경된 파일

신규:
- `backend/app/domain/asset/__init__.py` — 도메인 패키지 re-export
- `backend/app/domain/asset/entity.py` — `Asset` (frozen dataclass) + `Universe` (common_period, assets_by_currency)
- `backend/app/domain/asset/repository.py` — `AssetRepository` Protocol
- `backend/app/domain/asset/calendar_guard.py` — `is_trading_day`, `guard_trading_day` (XKRX/XNYS/24-7)
- `backend/app/data/asset_repository.py` — `SqlAssetRepository` (SQLAlchemy 구현)

수정 (re-export 추가):
- `backend/app/data/__init__.py` — `SqlAssetRepository` re-export
- `backend/app/domain/__init__.py` — domain.asset 의 모든 공개 심볼 re-export

### 추가된 public API (Repository / 공개 API 변경 보고 규정 준수)

**`AssetRepository` Protocol (`app.domain.asset.repository`)**:
- `find_by_id(asset_id: int) -> Asset | None`
- `find_by_symbol_market(symbol: str, market: Market) -> Asset | None`
- `search(q: str | None = None, market: Market | None = None, asset_type: str | None = None, limit: int = 50, offset: int = 0) -> list[Asset]`
- `list_active() -> list[Asset]`
- `upsert(asset: Asset) -> Asset`  (ON CONFLICT (symbol, market) DO UPDATE)
- `update_ingestion_state(asset_id: int, start_date: date | None, last_ingested_at: datetime | None) -> None`

**`SqlAssetRepository` (`app.data.asset_repository`)**: 위 Protocol 을 모두 동일 시그니처로 구현. `__init__(session: sqlalchemy.orm.Session)` 으로 세션 주입.

**Domain helper (`app.domain.asset.calendar_guard`)**:
- `is_trading_day(market: str, target: date) -> bool`
- `guard_trading_day(market: str, target: date, mode: GuardMode = "snap_previous") -> date`
- `GuardMode = Literal["raise", "snap_previous", "snap_next"]`

**Universe (`app.domain.asset.entity`)**:
- `common_period() -> tuple[date, date] | None`
- `assets_by_currency() -> dict[str, tuple[Asset, ...]]`

## DoD 검증 결과

### 1. import 스모크
```
$ cd backend && python -c "from app.domain.asset import Asset, Universe, AssetRepository; from app.data.asset_repository import SqlAssetRepository; print('ok')"
ok
```

### 2. domain 순수성
AST 기반 import 추출 결과:
- `app/domain/asset/entity.py`: `['__future__', 'dataclasses', 'datetime', 'typing']` — 순수
- `app/domain/asset/repository.py`: `['__future__', 'datetime', 'typing', 'app.domain.asset.entity']` — 순수
- `app/domain/asset/calendar_guard.py`: `['__future__', 'datetime', 'typing', 'exchange_calendars']` — 태스크 스펙상 허용

banned 패턴 (`sqlalchemy / fastapi / yfinance / pykrx / app.models / app.data`) 0건.

### 3. Universe.common_period 단위 동작
- 빈 universe → `None` (assertion pass)
- 일부 자산 start_date=None → `None` (assertion pass)
- 모두 채워진 케이스 (SPY=2010-01-01, BTC=2014-01-01) → `(2014-01-01, 2026-04-29)` — max start 정상
- frozen dataclass: `a.symbol = 'XX'` → `FrozenInstanceError` 정상

추가로 `assets_by_currency()` 그룹핑도 USD 통화 묶음으로 정상 반환 확인.

### 4. calendar_guard 동작
| case | 결과 |
|------|------|
| `is_trading_day('KR', 2024-01-01)` | False (한국 신정) ✓ |
| `is_trading_day('US', 2024-01-01)` | False ✓ |
| `is_trading_day('CRYPTO', 2024-01-01)` | True (24/7) ✓ |
| `is_trading_day('KR', 2024-01-02)` | True ✓ |
| `is_trading_day('US', 2024-01-02)` | True ✓ |
| `guard_trading_day('KR', 2024-01-01, 'snap_previous')` | `2023-12-28` ✓ |
| `guard_trading_day('KR', 2024-01-01, 'snap_next')` | `2024-01-02` ✓ |
| `guard_trading_day('KR', 2024-01-01, 'raise')` | `ValueError: 2024-01-01 is not a trading day for market 'KR'.` ✓ |
| `guard_trading_day('KR', 2024-01-02, 'snap_previous')` | `2024-01-02` (passthrough) ✓ |
| `guard_trading_day('CRYPTO', 2024-01-01, 'raise')` | `2024-01-01` (passthrough) ✓ |
| `is_trading_day('JP', 2024-01-01)` | `ValueError: Unknown market: 'JP'.` ✓ |

exchange_calendars 의 `previous_session`/`next_session` 은 인자 자체가 session 이어야 해서
non-session date 를 입력하면 예외가 난다. 따라서 `cal.date_to_session(target.isoformat(), direction='previous'|'next')` 를 사용했다 — non-session 입력에서도 인접 거래일을 반환한다.

## 클린 아키텍처 / 클린 코드 점검

- ✅ domain 은 ORM/HTTP/Web 프레임워크 의존 0건 (exchange_calendars 만 허용 — 도메인 정책)
- ✅ Asset / Universe 모두 `@dataclass(frozen=True)` 로 불변
- ✅ `AssetRepository` 는 `typing.Protocol` (덕 타이핑) — 구현체 교체 자유
- ✅ `_to_entity` 헬퍼로 ORM↔엔티티 매핑 일원화 (DRY)
- ✅ side-effect 함수는 동사 (`upsert`, `update_ingestion_state`) 로 의도 노출
- ✅ magic string 은 `_MARKET_CALENDARS` 매핑으로 named constant 화
- ✅ `SqlAssetRepository.upsert` 의 PostgreSQL `on_conflict_do_update` 는 (symbol, market) UNIQUE 제약과 일치
- ✅ 함수 분리: 가장 긴 함수가 ~30줄 (upsert), 40줄 이하 유지
- ✅ Single Responsibility: entity / repository protocol / calendar guard / sql 구현 분리

## 이슈/블로커

없음.

## 다음 제안

1. **Tester 호출 권장**: `Universe.common_period`, `assets_by_currency`, `calendar_guard.guard_trading_day` 의
   pytest 기반 단위 테스트 작성. 본 태스크 DoD 에서는 REPL 검증만 했으므로 회귀 방지 차원에서 필요.
   특히 `guard_trading_day` 의 `snap_previous`/`snap_next` 가 연말연초 같은 긴 휴장에서도 올바른
   거래일을 반환하는지 (예: 2023-12-29~31 + 2024-01-01 연속 휴일에서 2024-01-01 → 2023-12-28) 확인 필요.
2. **TASK-031 (비동기 백필)** 에서 `SqlAssetRepository.upsert` + `update_ingestion_state` 를 사용해
   사용자 자유 추가 워크플로우를 구현하면 된다. Repository Protocol 만 의존하면 SQL 결합 없음.
3. **TASK-061 (검색 API)** 에서 `SqlAssetRepository.search(q=, market=, asset_type=)` 를 그대로 활용 가능.
   현재 `q` prefix 매칭은 `ilike("{q}%")` — 한글 입력은 PostgreSQL 의 unicode 정규화에 의존하므로
   필요 시 `unaccent` extension 또는 trigram 인덱스 도입을 추후 고려.
4. **architecture.md 갱신 필요 사항** (Manager 영역): "Repository API" 섹션 (또는 유사 명칭) 에
   위 "추가된 public API" 목록을 누적 반영하면 후속 페이지/서비스 레이어가 ORM 우회 없이 활용 가능.
