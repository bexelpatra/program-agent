# Blockers

작업 중 사용자 판단이 필요한 차단 사유 append-only 로그.

## 형식

```markdown
## BLOCKER-NNN [HARD|SOFT] (TASK-XXX)
- 발견 시점: YYYY-MM-DDTHH:MM
- 차단 영역: (DB 스키마 / API / 프런트 / ...)
- 사유: (왜 사용자 판단이 필요한가)
- 우회 방안: (SOFT 일 때만 - mock/빈 구현으로 진행할 방법)
- 처리 결과: TODO | RESOLVED (날짜)
```

## 정책 (architecture.md V3 § "Blocker 정책" 참조)

- **HARD**: 선결되지 않으면 진행 불가능 → 즉시 멈추고 Manager 가 사용자 보고
- **SOFT**: mock/빈 구현으로 우회 가능 → 우회 + 해당 task-board 에 후속 TODO 등록 + 계속 진행
- 모든 태스크 완료 후 Manager 가 blockers 재독 → 자체 처리 시도 → 잔여 blocker 만 사용자 보고

---

## BLOCKER-001 [SOFT] (TASK-002)
- 발견 시점: 2026-04-29T08:00
- 차단 영역: DB / Alembic 마이그레이션 정합성
- 사유: TASK-002 의 `alembic check` 가 `Can't locate revision identified by '0003'` 로 실패. DB(`stock_backtest`)에 이전 환경에서 적재된 11개 테이블과 `alembic_version='0003'` 행이 이미 존재하나, 새 `backend/alembic/versions/` 는 비어 있어 revision 0003 을 찾을 수 없음. 코드 결함이 아니라 외부 DB 상태 문제.
- 우회 방안: TASK-002 DoD 의 import 검증(1·2번)은 통과. 후속 마이그레이션 태스크(TASK-010+) 에서 baseline revision 을 새로 만들거나 기존 DB 를 drop+recreate 하여 정리 필요. (사용자가 수동으로 `psql -c "drop schema public cascade; create schema public;"` 실행해도 됨.)
- 처리 결과: RESOLVED — 2026-04-29T12:30 사용자 동의 후 V1/V2 잔재 stock-backtest-db 컨테이너 + volume 삭제 → 새 quant-lab-postgres 컨테이너 가동 → alembic upgrade head (3 마이그 적용: 0001_v3_baseline → 0002_timeseries_tables → 0003_backtest_tables) → seed_catalog.py 67 자산 적재 → smoke_e2e PASS (data_loader 122 영업일 fx 정상). 잔여 작업: ohlcv 백필 (사용자 cron 시작 또는 backfill_active_assets 수동 호출).

## BLOCKER-002 [SOFT] (TASK-021)
- 발견 시점: 2026-04-29T09:00
- 차단 영역: 데이터 수집 / 한국 ETF 배당 (분배금)
- 사유: pykrx 1.2.7 이 ETF 분배금 / 주식 배당을 종합 API 로 제공하지 않아 `PykrxSource.fetch_dividends` 가 빈 리스트를 반환한다 (실측 확인: `069500` 1년 구간 `[]`). 한국 ETF 백테스트 결과에서 배당 수익이 누락된다.
- 우회 방안: MVP 는 빈 구현으로 진행 (KR 자산 사용자가 배당 가정 없이 비교 가능). 향후 KRX 정보시스템 분배금 API 또는 별도 데이터 소스(예: FinanceDataReader, KRX OpenAPI) 도입 필요. UI 에 "KR 자산은 배당 미반영" 명시 (UI/UX 원칙 2 — 사용자 직접 노출).
- 처리 결과: TODO
