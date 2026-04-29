# Alembic Migrations

V3 baseline 으로 시작하는 단일 revision 트리. V1/V2 의 11개 테이블 + `alembic_version='0003'`
잔재가 DB 에 남아 있다면 alembic 이 새 baseline 과 sync 되지 못하므로 아래 초기화 절차를 먼저 수행한다.

## 처음 시작 / 기존 DB 초기화

### 옵션 A: Docker volume 자체를 삭제 (가장 깔끔)

```bash
cd projects/stock-backtest
docker compose down -v   # postgres volume 까지 제거
docker compose up -d
cd backend
alembic upgrade head
```

### 옵션 B: volume 보존 + schema 만 초기화

운영 환경 등 컨테이너 재기동이 부담스러우면:

```bash
psql "$DATABASE_URL" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
cd backend
alembic upgrade head
```

## 새 모델 추가 시

1. `backend/app/models/your_model.py` 작성
2. `backend/app/models/__init__.py` 에 import 추가 (alembic 이 metadata 인식)
3. `cd backend && alembic revision --autogenerate -m "add your_model"`
4. 생성된 `versions/*.py` 검토 (불필요한 drop/create 제거, 인덱스/제약 보강)
5. `alembic upgrade head`

## 검증 명령

- `alembic current` — 현재 DB revision 확인
- `alembic heads` — script tree 의 head revision 확인 (단일 head 유지)
- `alembic check` — metadata 와 DB 가 일치하는지 확인 (drift 감지)

## 주의

- `alembic_version` 테이블은 alembic 이 자체 관리한다. 수동 INSERT/UPDATE 금지.
- baseline revision id (`0001_v3_baseline`) 는 변경 금지. down_revision 체인 끊김 방지.
