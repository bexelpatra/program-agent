---
agent: coder
task_id: TASK-003
status: DONE
timestamp: 2026-04-29T08:15:00
---

## 결과 요약

자산 카탈로그 시드 데이터 67개 (KR 20 / US 35 / CRYPTO 12) 을 TypedDict 기반 Python 모듈로 정의하고, DB UPSERT CLI 스크립트를 작성했다. 4가지 DoD 검증 모두 통과 (총 개수 50~100 범위, 필수 필드 충족, 분포 출력, 중복 0).

## 변경된 파일

- `projects/stock-backtest/backend/app/data/seed/__init__.py` (신규) — 패키지 마커
- `projects/stock-backtest/backend/app/data/seed/assets_catalog.py` (신규) — 67개 SeedAsset CATALOG 정의
- `projects/stock-backtest/backend/scripts/seed_catalog.py` (신규) — Postgres UPSERT CLI

## 카탈로그 통계 (실측)

검증 명령:
```
python -c "from app.data.seed.assets_catalog import CATALOG; from collections import Counter; print(Counter(a['market'] for a in CATALOG)); print(Counter(a['asset_type'] for a in CATALOG))"
```

- **총 개수**: 67 (요구 범위 50~100 ✅)
- **시장(market) 분포**:
  - KR: 20
  - US: 35
  - CRYPTO: 12
- **asset_type 분포**:
  - ETF: 34
  - BOND: 12
  - CRYPTO: 12
  - COMMODITY: 9
  - EQUITY_INDEX: 0 (KR/US 모두 ETF 추적 형태로 표현 — 순수 지수형 자산은 시드에 포함하지 않음)
- **KR 세부 (kr_tax_class meta)**:
  - domestic_equity: 8 (KODEX 200, TIGER 200, 코스닥150, 섹터 ETF 등)
  - overseas_equity: 5 (TIGER 미국S&P500, KODEX 미국S&P500TR, 미국나스닥100, 차이나CSI300 등)
  - bond: 5 (KOSEF 국고채10년, TIGER 국채3년, KODEX 단기채권, KBSTAR 중기우량회사채, KODEX 미국채울트라30년선물(H))
  - commodity: 2 (KODEX 골드선물(H), TIGER 원유선물Enhanced(H))
- **중복 0**: `(symbol, market)` pair 67개 모두 unique 검증 통과

## DoD 검증 결과

| # | 검증 | 결과 |
|---|------|------|
| 1 | 총 개수 50~100 + KR/US/CRYPTO 비중 출력 | `67 KR: 20 US: 35 CRYPTO: 12` ✅ |
| 2 | 모든 필수 필드 채워짐 (symbol/market/currency/name) | `all valid` ✅ |
| 3 | market·asset_type 분포 출력 | 위 통계 표 참조 ✅ |
| 4 | `(symbol, market)` 중복 0 | `no duplicates` ✅ |

## 이슈/블로커

없음 (코드 결함 영역).

참고 (SOFT, BLOCKER-001 잔재):
- `scripts/seed_catalog.py` 직접 import 는 환경 의존성(pydantic_settings 등 미설치)으로 현재 셸에서 실패. 카탈로그 데이터 모듈 자체(`app.data.seed.assets_catalog`)는 외부 의존이 0이라 import·검증 모두 통과. 실제 DB INSERT 는 사용자가 DB 초기화 + venv 셋업 후 `python -m scripts.seed_catalog` 로 수행.

## 클린 코드 점검

- 시드 데이터는 `app/data/seed/` 격리 (도메인 로직 0).
- DB UPSERT 로직은 `scripts/seed_catalog.py` 분리 (CLI 도구).
- `SeedAsset(TypedDict)` 으로 schema 강제 — IDE 자동완성 + 타입 힌트.
- `Literal["KR","US","CRYPTO"]`, `Literal["EQUITY_INDEX","ETF","BOND","COMMODITY","CRYPTO"]` 으로 enum 강제.
- 한글 표시명 우선 (CRYPTO 12개 모두 "비트코인/이더리움/..." 한글, KR 20개 모두 거래소 한글명, US 는 영어 공식명 + 일부 한글 부가설명).

## 다음 제안

1. **TASK-011 완료 후**: alembic 마이그레이션이 적용되어 assets 테이블이 생성되면, `python -m scripts.seed_catalog` 멱등 실행 검증을 user-execution 태스크로 등록 권장 (Execution: user, BLOCKER-001 영향).
2. **kr_tax_class 활용 태스크**: Phase 2 세금 시뮬레이터 도입 시 KR 자산 meta 의 `kr_tax_class` 필드를 enum 으로 도메인 모델에 매핑하는 별도 태스크 추천. 현재는 raw string.
3. **카탈로그 확장 태스크 (Phase 1.5)**: 사용자 자유 추가 워크플로우(architecture L534-537) 구현 시, 본 시드와의 충돌 처리(이미 시드된 ticker 를 사용자가 다시 추가 시도) 정책을 architecture.md 에 명문화 필요.
