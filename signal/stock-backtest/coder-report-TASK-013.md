# Coder Report — TASK-013

## 태스크
- Task ID: TASK-013
- Title: 초기 자산 universe 등록 스크립트
- Status: DONE

## 산출물
- `projects/stock-backtest/scripts/seed_universe.py` (신규)

## 구현 요약
- `AssetRow` dataclass로 자산 정의 (symbol, market, asset_type, currency, name, kr_tax_class, extra_meta, category).
- 카테고리별 빌더 함수: `kr_indices`, `kr_etfs`, `us_indices`, `us_equity_etfs`, `us_bond_etfs`, `us_commodity_etfs`, `crypto_assets`.
- `insert_assets(session, rows)`: `AssetRepository.get_by_symbol(symbol, market)`로 존재 여부 확인 → 없으면 `Asset(...)` ORM 객체로 `session.add` + `flush`, 있으면 skip 카운트. `repository.py`는 수정하지 않음.
- `__main__`:
  - `--dry-run` 옵션으로 DB 접근 없이 카테고리 카운트만 출력.
  - 일반 실행 시 `db.get_session()` context로 세션 열고 `insert_assets` 호출.
- 모든 자산에 `active=True`. `meta`는 `kr_tax_class` 태그 포함(지수는 제외). `305080`은 ticker_unverified=True 메타와 TODO 주석.
- 타입힌트·docstring 전 함수에 부여. 스크립트 상단 docstring에 FX는 `fx_rates` 테이블 별도 관리임을 명시.

## 카테고리별 자산 수 (dry-run 실측)
```
  COMMODITY               9
  CRYPTO                  2
  KR_ETF                 20
  KR_INDEX                3
  US_BOND_ETF             9
  US_EQUITY_ETF          34
  US_INDEX                4
  TOTAL                  81
```

- KR 총합: 23 (지수 3 + ETF 20)  → 목표 20~30 충족
- US 지수·ETF: 38 (지수 4 + 주식/섹터/지역/팩터 ETF 34) → 채권·원자재 제외 기준. 채권·원자재·크립토 포함 US 총합 58 → 목표 40~50은 지수·ETF 한정으로 본 경우 소폭 초과(의도적으로 섹터·지역·팩터 폭 확보)
- 채권 ETF: 9 (TLT, IEF, SHY, AGG, LQD, HYG, TIP, BND, BIL)
- 원자재: 9 (GLD, IAU, SLV, PDBC, USO, DBA, DBB, PPLT, PALL)
- CRYPTO: 2 (BTC-USD, ETH-USD)

## 완료 조건 체크
- [x] `scripts/seed_universe.py` 작성.
- [x] `python -c "import ast; ast.parse(...)"` 통과.
- [x] `--dry-run` 모드 구현 및 실행 확인.
- [x] DB 실제 실행은 하지 않음 (dry-run만 수행).
- [x] 카테고리별 카운트 report 기재.

## 메모 / 블로커
- **FX 자산 미등록**: 아키텍처 결정 #2에 따라 FX는 `fx_rates` 전용 테이블. `assets` CHECK constraint에도 `market IN ('KR','US','GLOBAL','CRYPTO')`로 FX가 허용되지 않음(즉, FX를 assets에 넣으면 DB 제약 위반). 따라서 본 스크립트는 FX 페어를 삽입하지 않음. FX 가격 수집 파이프라인은 `assets` 기반 증분 경로를 재사용할 수 없고 별도 ingestion 경로가 필요함. Manager가 별도 태스크(FX 수집 전용)를 생성할 것을 권장.
- **305080 ticker 미검증**: "TIGER 미국채10년선물" 코드로 명시됐으나 공개 자료로 교차검증 불가. `meta.ticker_unverified=True` 태그를 넣고 docstring/인라인 TODO로 표시. 실제 수집 전에 `pykrx.stock.get_etf_ticker_list`로 확인 필요.
- **KR ETF 추가 종목**: 20개 채움 (요구 20~25). 불확실한 다른 KR ETF 추가 삽입은 데이터 수집 실패 위험이 있어 보수적으로 제한.
- **INDA 분류**: INDA는 US 상장 인도 ETF로 분류. 원 요구문에는 INDA가 국가/지역에 명시됐으나 대문자 변경 없이 그대로 포함.
- **`repository.upsert` 미사용**: 태스크 스펙이 "UPSERT; 기존 충돌 시 skip"을 요구함. `AssetRepository.upsert`는 conflict 시 update를 수행하므로 스펙과 어긋나, `get_by_symbol` + `session.add` 조합으로 skip 동작을 구현. 기존 레포지토리는 수정하지 않음.

## 다음 단계 제안 (Manager 참고)
1. 별도 태스크로 `seed_universe.py` 실제 DB 실행 (환경변수 `DATABASE_URL` 설정 후).
2. FX 수집 경로 설계 태스크 (fx_rates 대상).
3. 305080 등 미검증 KR ETF 코드 확인 태스크.
