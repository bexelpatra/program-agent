# Quant Lab — 비개발자 친화 퀀트 투자 웹앱

V3 Phase 1 MVP. 정적/동적 자산 배분(SAA/DAA) 백테스팅 플랫폼.

자세한 미션·원칙은 `CLAUDE.md` 참조. 설계 결정 누적은 `signal/stock-backtest/architecture.md`.

---

## 빠른 시작 (3분)

### 사전 요구
- Python 3.11+
- Node.js 20+ (npm 10+)
- Docker + Docker Compose

### 1. 환경 변수

```bash
cp .env.example .env
# .env 의 DATABASE_URL / POSTGRES_* / 포트 등을 필요시 편집 (디폴트 사용 가능)
```

### 2. PostgreSQL + TimescaleDB 기동

```bash
docker compose up -d
docker compose ps   # postgres healthy 확인
```

### 3. 백엔드 가상환경 + 의존성

```bash
cd backend
python3 -m venv ../.venv
source ../.venv/bin/activate
pip install -r requirements.txt
```

스모크 체크:

```bash
python scripts/smoke_imports.py
```

### 4. DB 마이그레이션

```bash
# BLOCKER-001 잔재 (실패한 마이그레이션 흔적) 가 있으면 먼저 볼륨 초기화:
# docker compose down -v && docker compose up -d
alembic upgrade head
```

### 5. 자산 카탈로그 시드 (KR/US/CRYPTO 67개)

```bash
python scripts/seed_catalog.py
```

### 6. 백엔드 기동

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### 7. 프런트엔드 기동 (별도 터미널)

```bash
cd frontend
npm install
npm run dev   # http://localhost:3000
```

브라우저에서 `http://localhost:3000` 접속.

end-to-end 데이터 적재 검증 (선택):

```bash
cd backend && python scripts/smoke_e2e.py
```

---

## 화면 (UI/UX 원칙 6 — 화면 3개 한도)

1. **자산 카탈로그** (`/assets`) — 시장 필터 + 검색 + 자산 추가
2. **백테스트 생성** (`/backtests/new`) — 전략 선택 + universe + 기간 + 진행률 폴링 (in-place)
3. **백테스트 결과** (`/backtests/[run_id]`) — equity/drawdown/지표/월별 히트맵/거래 내역

---

## 전략 (MVP 5종)

- **Allocator 3종**: FixedWeight, AllWeather (주식 30 / 장기채 40 / 중기채 15 / 금 7.5 / 원자재 7.5), EqualWeight (1/N)
- **Filter 2종**: MovingAverage (가격 > MA 면 PASS), Momentum (lookback 수익률 > 임계값)

---

## 핵심 정책

- **현금/FX**: 통화별 잔고 (`cash_by_ccy`), 자산은 native currency 보유, 매일 base_currency 환산 (B 모델)
- **환전**: 단계 분리 + native 잔고 우선 (Q3 C + Q5 B), `fx_spread` 20bp 디폴트
- **거래 모델 A**: D 일 종가 시그널 → D+1 일 시가 체결 (look-ahead 0)
- **Long-only, 정수 주, 가능한 만큼 체결**

---

## 디렉토리 한눈에

```
backend/
  app/
    api/          FastAPI 라우터 (assets / backtests / strategies)
    core/         설정, DB engine/SessionLocal, 로깅
    domain/       allocators / filters / engine.py / metrics / portfolio / trade
    data/         repositories (assets/ohlcv/backtest), sources (yfinance/pykrx/upbit)
    models/       SQLAlchemy ORM 모델
    scheduler/    APScheduler cron (KR 18:00 / US 07:00 / Crypto 09:00 KST)
    services/     backtest_runner / data_loader (백그라운드 job + 입력 데이터)
    schemas/      Pydantic 경계 스키마
  alembic/        DB 마이그레이션
  scripts/        smoke_imports / smoke_e2e / seed_catalog
  tests/          regression / golden / api
frontend/
  app/            Next.js App Router
  components/     shadcn/ui + strategy / backtest / asset
  lib/            API 클라이언트 + Zod 스키마
docker-compose.yml  Postgres + TimescaleDB
```

자세한 책임·계층 분리는 `signal/stock-backtest/architecture.md` V3 섹션 참조.

---

## 알려진 제한

- **pykrx 한국 ETF 분배금 미지원** (BLOCKER-002, MVP) — KR 자산 백테스트 결과에 배당 누락 가능
- **워커 크래시 후 pending/running 복구 미구현** (Phase 2)
- **데이터 로더는 ohlcv/fx_rates 가 백필되어 있다는 전제** — 백필 미완 자산은 prices_aligned 에 NaN 컬럼으로 반영, engine 이 ValueError 로 종료 (status='failed')

---

## Phase

- **Phase 1 (현재)**: SAA/DAA/백테스팅 + 5 전략 + 화면 3개
- **Phase 2**: 계절성 분석 (정치 사이클·FOMC·Sell-in-May·실적시즌·한국 정치)
- **Phase 3+**: 한국 거주자 세금 plugin, asset_type UI 세분화, 다중 전략 합성 composer

---

## 개발 워크플로우

1. `signal/stock-backtest/task-board.md` 의 다음 태스크 확인
2. 도메인 → API → 프런트 순으로 구현
3. 모든 변경은 `signal/stock-backtest/` 의 시그널 보드를 통해 보고

---

## 문서

- `signal/stock-backtest/architecture.md` — V3 설계 결정 (V1/V2 히스토리 포함)
- `signal/stock-backtest/task-board.md` — Phase 1 태스크 진행
- `signal/stock-backtest/blockers.md` — 사용자 액션 필요 항목
- `signal/stock-backtest/done-log.md` — 완료 기록
