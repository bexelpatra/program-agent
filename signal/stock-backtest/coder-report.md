---
agent: coder
task_id: TASK-100
status: DONE
timestamp: 2026-04-29T00:57:00
---

## 결과 요약

Phase 1 MVP 의 마지막 통합 태스크 (TASK-100) 를 완료했다.

1. **데이터 로더 모듈 신규** — `app/services/data_loader.py` 작성. ohlcv → prices_aligned (base 캘린더 정렬 + 비base 시장 forward-fill), fx_rates → fx_rates_to_base (date → {ccy → base_per_ccy}, base 환율 = 1, 비base 통화 forward-fill), assets → universe_market_meta 일괄 로딩.
2. **`backtest_runner.execute_backtest_job` placeholder 해소** — universe_market_meta=`("US", base_currency)` placeholder + prices_aligned=`pd.DataFrame()` placeholder + fx_rates_to_base=`{}` placeholder 를 `services.data_loader.build_backtest_context` 호출로 교체. stage 추적도 `load_market_data` 단계 추가.
3. **README 전면 개편** — 7단계 빠른 시작 + 화면 3개 + 전략 5종 + 핵심 정책 + 디렉토리 트리 + Phase 분리 + 알려진 제한 + 문서 링크. 한국어 우선 (UI/UX 원칙 2 일관).
4. **smoke_e2e.py 신규** — BLOCKER-001 해소 후 사용자가 수동 실행 가능한 end-to-end 데이터 적재 검증 스크립트.

## FxRate 의미 검증 (구현 전 확인)

`models/fx_rates.py` L18: `USDKRW=1300 → row(base_ccy=USD, quote_ccy=KRW, rate=1300)`. 즉 `rate = quote_per_base = "1 base 단위가 quote 통화로 얼마"`.

백테스트 base_currency=KRW, 자산통화=USD 일 때 도메인 컨벤션 (`engine.py` L75-76, `portfolio.py` L89) 은 `fx_rates_to_base["USD"] = KRW per USD = 1300` 을 요구한다. 따라서 lookup 은 `FxRate(base_ccy=ccy, quote_ccy=base_currency).rate` 가 정확히 `base_per_ccy`. (data_loader.py L11-23 docstring 에 근거 명시)

## 변경된 파일

- `projects/stock-backtest/backend/app/services/data_loader.py` (신규, 215 라인)
- `projects/stock-backtest/backend/app/services/backtest_runner.py` (수정, 332 라인 — placeholder 해소, pd import 제거, stage 'load_market_data' 추가, ValueError 메시지 갱신)
- `projects/stock-backtest/backend/scripts/smoke_e2e.py` (신규, 79 라인)
- `projects/stock-backtest/README.md` (전면 갱신, 90 라인 → 163 라인)

## 신규 public API

`app/services/data_loader.py`:
- `load_universe_market_meta(session, asset_ids: list[int]) -> dict[int, tuple[str, str]]` — asset_id → (market, currency)
- `load_prices_aligned(session, asset_ids, base_currency, period_start, period_end, asset_meta=None) -> pd.DataFrame` — index=date, columns=asset_id, values=float|NaN
- `load_fx_rates_to_base(session, base_currency, period_start, period_end, needed_currencies: set[str]) -> dict[date, dict[str, Decimal]]` — base 자체는 1, 비base 는 forward-fill
- `build_backtest_context(session, asset_ids, base_currency, period_start, period_end) -> tuple[pd.DataFrame, dict[int, tuple[str, str]], dict[date, dict[str, Decimal]]]` — backtest_runner 가 호출

기존 도메인/리포지토리 public API 변경 없음 (data_loader 는 ohlcv/fx_rates 모델을 직접 read-only 로 select — 신규 repository 클래스는 만들지 않았다. 단일 호출처 + Service 계층이라 Repository 추상화 비용 vs 가치를 따져 직접 select 채택. 다음 제안 참조).

## DoD 검증

| # | 검증 | 결과 |
|---|------|------|
| 1 | `python -c "from app.services.data_loader import load_universe_market_meta, load_prices_aligned, load_fx_rates_to_base, build_backtest_context; print('ok')"` | PASS (`data_loader ok`) |
| 2 | backtest_runner 가 placeholder 대신 data_loader 호출 | PASS (코드 리뷰 완료, `from app.services.data_loader import build_backtest_context`, L272-281 호출) |
| 3 | README 7단계 명령 출력 | PASS (`grep -nE "^### [1-7]\."` → 7행 모두 매치) |
| 4 | smoke_e2e.py import 가능 | PASS (`ast.parse` ok, 실제 실행은 BLOCKER-001 후) |
| 5 | 회귀 테스트: `pytest tests/regression/ tests/golden/ -v` | PASS (62 passed, 2 warnings, 2.98s) |

## 클린 코드/아키텍처 점검

- **계층 의존**: `services.data_loader` → `domain.calendar` (정렬 함수) + `models.*` (ORM read-only) + `sqlalchemy`. domain 으로의 역방향 의존 없음. Service 계층이라 SQLAlchemy 의존 허용 범위 안.
- **단일 책임**: 한 파일 = 입력 데이터 로딩 한 가지. `load_prices_aligned` / `load_fx_rates_to_base` / `_load_asset_close_series` / `_load_fx_pair_series` / `build_backtest_context` 함수 5개로 적정 분해.
- **함수 길이**: 모두 40 라인 이하. 가장 긴 `load_prices_aligned` 도 30 라인.
- **이름**: `_load_asset_close_series` / `_load_fx_pair_series` 등 동사+대상 명확. boolean 사용 없음.
- **주석**: docstring 은 의도/계약, 인라인 주석은 "왜" (lookback 이유, FxRate 의미, ORM 봉인) 위주.
- **backtest_runner 변경 범위 최소화**: import 1행 추가, pd import 제거, stage='load_market_data' 추가, 4행 ctx 구성 변경. 다른 로직 (progress callback, cancel check, persist_results, error handling) 모두 보존.
- **README 한국어 우선**: 명령은 영문 그대로, 설명은 한국어.

## 이슈/블로커

없음. BLOCKER-001 (마이그레이션 실패) 은 사용자 액션 (`docker compose down -v && alembic upgrade head`) 필요한 외부 차단으로 본 태스크 범위 외.

## 다음 제안 (Phase 1 마무리 + retrospective.md)

1. **OhlcvRepository / FxRepository read-only 메서드 추가 (Phase 2)** — data_loader 가 `select(Ohlcv.time, Ohlcv.close)` / `select(FxRate.time, FxRate.rate)` 를 직접 작성한다. 단일 호출처라 추상화 비용을 미뤘으나, scheduler 백필 코드와 일부 중복. Phase 2 진입 시 `OhlcvRepository.read_close_series(asset_id, start, end) -> dict[date, Decimal]`, `FxRepository.read_pair_series(base, quote, start, end) -> dict[date, Decimal]` 로 추출 검토.
2. **데이터 로더 단위 테스트 (Tester)** — pytest fixture (in-memory SQLite 또는 docker postgres) 로 ohlcv/fx 시드 후 `load_prices_aligned` forward-fill 동작·`load_fx_rates_to_base` base=1 보장·이종통화 forward-fill·NaN 컬럼 처리 케이스를 회귀 보호. 현재는 도메인 calendar 함수만 단위 테스트 보호, data_loader 자체는 smoke_e2e 의존.
3. **smoke_e2e 자동화 옵션** — `make e2e` Makefile 타겟이나 GitHub Actions step. 사용자 실행 부담 감소.
4. **retrospective.md 작성 (Manager 권장)** — Phase 1 MVP 36 태스크 완료. FAILED → 재시도 통계 + Reviewer NEEDS_REVISION 빈도 + 태스크 분해 크기 적정성 + BLOCKER 해결률 등 회고 후 Phase 2 진입 결정.
5. **BLOCKER-001 사용자 보고** — Manager 가 retrospective 발사 전에 "마이그레이션 잔재 → docker compose down -v 한 번 필요" 를 명시 보고.
