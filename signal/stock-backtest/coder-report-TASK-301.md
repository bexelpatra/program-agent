---
agent: coder
task_id: TASK-301
status: DONE
timestamp: 2026-05-12T00:00:00
---

## 결과 요약

`backend/app/domain/themes/` 신규 패키지 4 파일 + 단위 테스트 1 파일을 추가했다.
도메인 entity 3종 (frozen+slots dataclass) + ThemeRepository Protocol
(`@runtime_checkable`, 10 메서드) + 멤버십 트랜잭션 박제 service (add/remove +
list_history) + service 단위 테스트 6건 (요구 5건 + frozen smoke 1건). 도메인
순수성 grep 0 hit, 기존 회귀 0 (`tests/domain/` --ignore themes = 44 PASS),
import smoke 통과.

## 변경된 파일

| 파일 | 변경 요지 |
|------|-----------|
| `backend/app/domain/themes/__init__.py` (신규) | public API re-export (entity/repository/service 12개 심볼). |
| `backend/app/domain/themes/entity.py` (신규) | Theme/ThemeAsset/AssetThemeHistory frozen+slots dataclass + EventType/AttentionSource/HistorySource Literal. stdlib (dataclasses/datetime/typing) 만 import. |
| `backend/app/domain/themes/repository.py` (신규) | `ThemeRepository` Protocol — `@runtime_checkable` + 10 메서드 (create_theme/get_theme/list_themes/update_theme/soft_delete_theme/add_asset/remove_asset/list_active_assets/append_history/list_history). entity 만 import. |
| `backend/app/domain/themes/service.py` (신규) | `UnitOfWork` Protocol + `add_asset_to_theme` / `remove_asset_from_theme` / `list_asset_history` + 예외 3종 (ThemeMembershipError / DuplicateActiveMember / InactiveMember). 단일 트랜잭션 흐름: 사전 검증 → repo.add/remove → repo.append_history → uow.commit. 예외 시 uow.rollback. |
| `backend/tests/domain/themes/__init__.py` (신규) | 패키지 마커. |
| `backend/tests/domain/themes/test_theme_service.py` (신규) | `_FakeThemeRepository` (snapshot/restore 로 rollback 모사) + `_FakeUnitOfWork` + 6 테스트. |

## DoD 검증 결과

### (a) 도메인 순수성 — PASS

```bash
$ grep -rn "^from sqlalchemy\|^import sqlalchemy\|^from fastapi\|^import fastapi\
\|^from app.data\|^from app.api\|^from app.services\|^from app.domain.engine\
\|^from app.domain.strategy\|^from app.domain.allocators\|^from app.domain.filters\
\|^from app.domain.trade\|^from app.domain.portfolio" \
  projects/stock-backtest/backend/app/domain/themes/
# 출력 없음 (exit=1) — 0 hit
```

themes 패키지 4 파일 (entity/repository/service/__init__) 모두 stdlib + entity
+ repository 만 import.

### (b) Protocol 메서드 + frozen dataclass — PASS

- `entity.py`: 3 dataclass 모두 `@dataclass(frozen=True, slots=True)`. 변경 시도
  → FrozenInstanceError (test_theme_dataclass_is_frozen 에서 검증).
- `repository.py`: `ThemeRepository` Protocol 메서드 **10개** 정의 (task 본문
  "9 메서드" 요구 = create_theme/get_theme/list_themes/update_theme/
  soft_delete_theme/add_asset/remove_asset/list_active_assets/list_history).
  추가 1개 = `append_history` — service 가 멤버십 변경과 history append 를
  같은 unit-of-work 안에서 직접 호출해야 하는 task 본문 요구 ("theme_assets
  INSERT + asset_theme_history INSERT 단일 트랜잭션") 를 만족시키기 위해
  필수 (없으면 service 가 SQLAlchemy 를 직접 호출해야 해서 도메인 순수성 (a)
  위반). dir(ThemeRepository) 로 10 메서드 확인 완료.

### (c) service 트랜잭션 단위 테스트 5건 PASS — PASS

```bash
$ ../.venv/bin/python -m pytest tests/domain/themes/ -v
tests/domain/themes/test_theme_service.py::test_add_asset_to_theme_normal PASSED
tests/domain/themes/test_theme_service.py::test_remove_asset_from_theme_normal PASSED
tests/domain/themes/test_theme_service.py::test_add_asset_duplicate_active_raises_and_no_writes PASSED
tests/domain/themes/test_theme_service.py::test_remove_asset_not_active_raises_and_no_writes PASSED
tests/domain/themes/test_theme_service.py::test_add_rolls_back_when_history_insert_fails PASSED
tests/domain/themes/test_theme_service.py::test_theme_dataclass_is_frozen PASSED
6 passed in 0.31s
```

5건 (task 요구) + 1 bonus (frozen dataclass smoke). 5 케이스 매핑:
1. `test_add_asset_to_theme_normal` — theme_assets row 1건 + history(ADDED) 1건 + commit 1회.
2. `test_remove_asset_from_theme_normal` — removed_at 갱신 + history(REMOVED) 1건 + commit 1회.
3. `test_add_asset_duplicate_active_raises_and_no_writes` — DuplicateActiveMember + history append 0건 + commit 0회 (사전 검증에서 차단).
4. `test_remove_asset_not_active_raises_and_no_writes` — InactiveMember + history append 0건.
5. `test_add_rolls_back_when_history_insert_fails` — append_history 강제 실패 → uow.rollback 1회 호출 + Repository state restored (members/history 둘 다 빈 상태로 복원).

### (d) 기존 회귀 0 — PASS

```bash
$ ../.venv/bin/python -m pytest tests/domain/ -q --ignore=tests/domain/themes
44 passed in 0.50s
```

### (e) import smoke — PASS

```bash
$ ../.venv/bin/python -c "from app.domain.themes import Theme, ThemeAsset, \
  AssetThemeHistory, ThemeRepository, add_asset_to_theme, remove_asset_from_theme"
IMPORT OK
```

## 추가 결정 사항 (보고서 명시 요구)

**UnitOfWork Protocol 채택 근거** (task 본문 "Coder 자율, 단 선택 근거를 report
에 명시"):

세 후보 비교:

| 후보 | 장점 | 단점 |
|------|------|------|
| `commit_unit_of_work: Callable[[], None]` | 인자 1개로 단순 | 실패 시 rollback 분기를 service 가 직접 try/except 안에서 처리하기 어렵다 — Callable 1개로는 rollback 까지 강제 불가. |
| Repository `__enter__/__exit__` 컨텍스트 매니저 | with 블록 1개로 묶임 | (a) Repository 가 트랜잭션을 인지하게 되어 책임 분리 위반 ↔ task 본문 "Repository Protocol 자체는 트랜잭션 인지하지 않음" 요구와 충돌. (b) 컨텍스트 매니저는 도메인 위반 예외와 영속화 예외를 같은 분기로 처리해 흐름이 모호. |
| **UnitOfWork Protocol (commit/rollback 2 메서드) ← 채택** | (a) Repository ↔ 트랜잭션 책임 완전 분리. (b) service 가 try/except 안에서 두 분기 명시 — 흐름 가독성 최상. (c) TASK-302 의 SqlThemeRepository 는 SQLAlchemy `Session.commit/rollback` 을 그대로 어댑팅하는 thin wrapper 1개만 추가하면 됨. | service 가 인자를 1개 더 받음 (uow). |

채택 결과 service 시그니처:
```python
def add_asset_to_theme(repo: ThemeRepository, uow: UnitOfWork,
                       theme_id: int, asset_id: int, note: str | None = None) -> ThemeAsset
def remove_asset_from_theme(repo: ThemeRepository, uow: UnitOfWork,
                            theme_id: int, asset_id: int, note: str | None = None) -> None
```

## 이슈/블로커

없음.

## 다음 단계 (TASK-302 인계 메모)

- `SqlThemeRepository` 는 `ThemeRepository` Protocol 10 메서드 모두 구현.
- SQLAlchemy `Session` 을 `UnitOfWork` 로 감싸는 어댑터를 함께 제공 (예:
  `SessionUnitOfWork(session)` 클래스 — `commit() -> session.commit()` /
  `rollback() -> session.rollback()`). FastAPI dependency 가 Session + UoW +
  Repo 를 한 번에 주입하도록 `dependencies.py` 보강.
- `append_history` 는 service 가 호출하는 별도 메서드 — TASK-302 통합 테스트
  에서 add_asset / remove_asset 의 동일 트랜잭션 안에서 호출 검증 필수.
- `update_theme` / `soft_delete_theme` 의 "없는 theme_id" 처리 정책은
  TASK-302 에서 결정 (도메인 예외 또는 LookupError) — TASK-303 의 404 매핑과
  맞춰야 함.
