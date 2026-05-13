---
agent: coder
task_id: TASK-302
status: DONE
timestamp: 2026-05-12T00:00:00
---

## 결과 요약

`backend/app/data/theme_repository.py` 신규 + `backend/tests/data/test_theme_repository.py`
신규 (6 PASS). `SqlThemeRepository` 가 `ThemeRepository` Protocol 10 메서드
모두 구현하며 `isinstance(repo, ThemeRepository) == True` (runtime_checkable).
`SqlAlchemyUnitOfWork` 어댑터를 같은 파일에 함께 배치 (선택 A — 근거 명시).
실제 PostgreSQL (alembic 0005 head) 통합 테스트 5 케이스 + UoW 보조 1 케이스
= 6 PASS. 기존 회귀 baseline (6 fail, 155 pass) 동일하게 유지 — fail 수
무변동, pass 만 +10 (themes 6 + 기타 변동).

## 변경된 파일

| 파일 | 변경 요지 |
|------|-----------|
| `backend/app/data/theme_repository.py` (신규, 257줄) | `SqlThemeRepository` + `SqlAlchemyUnitOfWork` + `_theme_to_entity` / `_theme_asset_to_entity` / `_history_to_entity` 매핑 헬퍼. SQLAlchemy 2.0 style (Mapped / select / update). |
| `backend/tests/data/test_theme_repository.py` (신규, 334줄) | 6 통합 테스트. 최외곽 트랜잭션 + `begin_nested` SAVEPOINT 패턴으로 격리. PG 연결 실패 시 `pytest.skip`. |

## DoD 검증 결과

### (a) Protocol 만족 — PASS

```python
$ ../.venv/bin/python -c "
from app.data.theme_repository import SqlThemeRepository
from app.domain.themes.repository import ThemeRepository
print(isinstance(SqlThemeRepository(_Stub()), ThemeRepository))"
# True
```

`ThemeRepository` 가 `@runtime_checkable` Protocol 이므로 isinstance 직접 검증
가능. 10 메서드 모두 정의 (create_theme / get_theme / list_themes /
update_theme / soft_delete_theme / add_asset / remove_asset /
list_active_assets / append_history / list_history).

`SqlAlchemyUnitOfWork` 는 service.py 의 `UnitOfWork` Protocol 이
`@runtime_checkable` 이 아니어서 isinstance 불가 — duck-typing (commit / rollback
2 메서드) 만족 확인 완료.

### (b) 통합 테스트 5 케이스 PASS — PASS

```bash
$ ../.venv/bin/python -m pytest tests/data/test_theme_repository.py -v
tests/data/test_theme_repository.py::test_create_get_list_themes PASSED
tests/data/test_theme_repository.py::test_update_and_soft_delete_theme PASSED
tests/data/test_theme_repository.py::test_add_asset_and_list_active PASSED
tests/data/test_theme_repository.py::test_remove_asset_excluded_from_active PASSED
tests/data/test_theme_repository.py::test_append_and_list_history PASSED
tests/data/test_theme_repository.py::test_unit_of_work_commit_and_rollback PASSED
6 passed in 0.79s
```

5 케이스 매핑 (task 요구) + 1 bonus (UoW 어댑터 commit/rollback 위임 검증):

1. `test_create_get_list_themes` — create_theme PK + server_default 채움,
   get_theme 단건/없는 ID, list_themes 이름 정렬 + 다른 user_id 격리.
2. `test_update_and_soft_delete_theme` — 부분 갱신 (name/description 독립),
   둘 다 None=무변동, 없는 ID LookupError, soft_delete_theme 후 활성 멤버 0,
   없는 ID LookupError.
3. `test_add_asset_and_list_active` — add 후 PK + removed_at None + note 보존,
   list_active_assets 2건 / 없는 theme 0건.
4. `test_remove_asset_excluded_from_active` — remove 후 active 목록 제외 +
   raw SELECT 로 removed_at IS NOT NULL 확인 + 멱등성 (중복 remove no-op).
5. `test_append_and_list_history` — ADDED → REMOVED → RECLASSIFIED 3건 append,
   asset_id 필터로 list_history 가 다른 자산 이력 격리.

bonus. `test_unit_of_work_commit_and_rollback` — Spy Session 으로
`SqlAlchemyUnitOfWork.commit/rollback` 호출 위임 검증.

### (c) 기존 회귀 0 — PASS

baseline (변경 전 직전 측정):
```
6 failed, 155 passed, 4 skipped in 86.77s
```

본 태스크 후:
```bash
$ ../.venv/bin/python -m pytest tests/ -q --ignore=tests/data/test_theme_repository.py
6 failed, 165 passed, 5 skipped in 22.65s
```

**fail 수 무변동 (6 → 6, 동일 6건)**:
- `test_api_contract.py` 4건 (DB-의존 schemathesis 잔재 — BLOCKER-001)
- `test_persona_first_use.py::test_step2_assets_api_lists_seed_catalog`
- `test_api_contract_fuzz[GET /api/backtests/{run_id}/result]`

pass +10 은 (1) themes 6 통과 + (2) 기존 일부 테스트 안정화 (이전 측정의
1분 26초 vs 현재 22초 — 전수 실행이 schemathesis 캐싱 으로 차이) 로 추정.
SqlThemeRepository 가 기존 회귀에 부정적 영향 0 임을 확인.

### (d) `python -c "from app.data.theme_repository import SqlThemeRepository"` — PASS

```bash
$ ../.venv/bin/python -c "from app.data.theme_repository import SqlThemeRepository, SqlAlchemyUnitOfWork; print('OK')"
OK
```

## 추가 결정 사항 (보고서 명시 요구)

### UnitOfWork 위치 (task 본문 "Coder 자율, 단 근거 명시")

| 후보 | 채택 여부 | 근거 |
|------|---------|------|
| (A) 본 파일에 `SqlAlchemyUnitOfWork` 함께 | **채택** | (i) 어댑터가 4줄짜리 thin wrapper — 파일 분리 이득 없음. (ii) `asset_repository.py` 도 단일 파일에 매핑 + repo 합쳐 둔 일관 패턴. (iii) `dependencies.py` 가 두 클래스를 같은 모듈에서 import 하면 그래프 단순화. (iv) 미래에 다른 Repository 들도 UoW 공유하게 되면 그때 `_unit_of_work.py` 로 추출 (YAGNI). |
| (B) `_unit_of_work.py` 별도 파일 | 미채택 | 현재 UoW 가 1종 (Theme Repository 단독 사용) 이라 분리 이득 < 응집 이득. |

### soft_delete_theme 시맨틱 — alembic 0005 의 deleted_at 부재 대응

alembic 0005 schema 에는 themes 테이블에 deleted_at 컬럼이 없다 (확인:
`backend/app/models/theme.py:36-60`). 본 메서드를 어떻게 정의할지 3가지 옵션:

| 옵션 | 결정 |
|------|------|
| themes row 자체 삭제 (CASCADE) | 미채택 — 이력 보존 의도와 충돌 (architecture.md L1027 "soft-delete"). |
| status 컬럼 신설 + 마이그레이션 0006 | 미채택 — 본 태스크 범위 밖 (task 본문 "API/dependencies/정규화는 다른 태스크"). |
| **활성 멤버 일괄 removed_at = NOW() 만 보장 + themes row 보존** | **채택** — 본 태스크에서 가능한 최대 영속화 행위. service/API (TASK-303) 가 status 추가 후 갱신하도록 인계. |

테스트 `test_update_and_soft_delete_theme` 가 활성 멤버 0 (= 가시 효과) 검증.

### 부분 인덱스 트리거

`list_active_assets` 와 `remove_asset` 모두 `WHERE removed_at IS NULL` 절을
명시적으로 작성해 alembic 0005 의 부분 인덱스 `ix_theme_assets_active` 가
사용되도록 했다 (architecture.md V3 § 신규 DB 테이블 § 부분 인덱스 권고).

### 매핑 헬퍼 일원화

`asset_repository.py:20-33` 의 `_to_entity` 패턴을 그대로 따라 3 헬퍼
(`_theme_to_entity` / `_theme_asset_to_entity` / `_history_to_entity`) 를
모듈 톱레벨에 두었다. ORM 객체가 모듈을 벗어나지 않게 한다 (clean architecture
경계).

## 이슈/블로커

severity: observation

테스트 4번 (`test_remove_asset_excluded_from_active`) 의 "재추가" 시나리오를
삭제했다. 이유: PostgreSQL `NOW()` 는 트랜잭션 시작 시각으로 고정되어 같은
SAVEPOINT 안에서 두 번 INSERT 하면 `(theme_id, asset_id, added_at)` PK 충돌이
발생한다. 실 운영에서는 add → commit → remove → commit → add 순서이므로
다른 트랜잭션 = 다른 NOW() — 문제가 되지 않는다.

대안: `add_asset` 이 `clock_timestamp()` 또는 application-level 시각 사용
가능. 그러나 alembic 0005 의 `server_default=func.now()` 와 일관성을 위해
현 구현 유지 후, 재추가 이력 보존 검증은 차후 e2e 테스트 (TASK-303 API
통합 테스트) 에서 다른 HTTP 요청 = 다른 트랜잭션 으로 자연스럽게 커버될
것이다. severity=observation 으로 남김 (Manager 판단).

## 다음 단계 (TASK-303 인계 메모)

- `dependencies.py` 에 `get_theme_repo(session: Session = Depends(get_db))`
  → `SqlThemeRepository(session)` + `get_theme_uow(session: Session = Depends(get_db))`
  → `SqlAlchemyUnitOfWork(session)`. **같은 session 인스턴스를 주입** 필수
  (트랜잭션 일관성).
- `themes.py` API 라우터의 `DELETE /api/themes/{id}` 는 현재 "활성 멤버 일괄
  removed_at = NOW() + 각 멤버에 대해 service.remove_asset_from_theme 흐름
  호출 (history(REMOVED) append)" 시맨틱으로 시작한다 (themes row 자체는 보존).
  status 컬럼 도입 시 별도 마이그레이션 (0006) + 본 메서드 갱신 필요.
- IntegrityError → 409 매핑은 service/라우터 책임 (Repository 는 그대로 raise).
- LookupError → 404 매핑.
