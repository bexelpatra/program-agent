---
task_id: TASK-045
agent: coder
status: DONE
severity: none
parallel: true
created_at: 2026-04-29
---

# TASK-045 Coder Report — Tax plugin 인터페이스 + NoTaxPlugin

## 요약

architecture.md V3 § "세금 모듈 (Plugin 인터페이스)" L646-657, L669-681 + Q9 결정에 따라 세금 plugin 인터페이스(`TaxPlugin` Protocol)와 MVP 디폴트 빈 구현(`NoTaxPlugin`)을 `backend/app/domain/tax.py` 에 신규 추가. 도메인 레이어 순수성 (dataclass / Decimal / typing.Protocol 만) 유지.

## 변경된 파일

| 파일 | 변경 | 라인 |
|------|------|------|
| `backend/app/domain/tax.py` | **신규** — Tax plugin 인터페이스 + NoTaxPlugin 빈 구현 | 106 |
| `backend/app/domain/__init__.py` | append-only — tax 심볼 6종 import + `__all__` 등록 | +14 |

다른 태스크 (TASK-023/050/053) 영역은 미수정. `__init__.py` 는 기존 metrics import 블록 다음에만 append. 충돌 없음.

## DoD 결과

| # | 검증 | 결과 |
|---|------|------|
| 1 | `python -c "from app.domain.tax import TaxPlugin, NoTaxPlugin, RealizedTrade, DividendIncome, TaxResult, apply_tax_to_portfolio; print('ok')"` | PASS — `ok` |
| 2 | 도메인 순수성 (banned import 0) — 실측: `dataclasses`, `datetime.date`, `decimal.Decimal`, `typing.{Protocol, runtime_checkable}` 4개만 | PASS |
| 3 | NoTaxPlugin 동작 — `tax_amount == Decimal("0")`, `year == 2024`, `breakdown == {}`, `note is None` 모두 단언 통과. 출력: `TaxResult(year=2024, tax_amount=Decimal('0'), breakdown={}, note=None)` | PASS |
| 4 | Protocol 구조적 타이핑 — `isinstance(NoTaxPlugin(), TaxPlugin) == True` (TaxPlugin 에 `@runtime_checkable` 적용). 출력: `NoTaxPlugin satisfies TaxPlugin protocol` | PASS |
| (보너스) | 패키지 re-export — `from app.domain import TaxPlugin, NoTaxPlugin, ...` 통과 | PASS — `package re-export ok` |

## 신규 public API

`backend/app/domain/tax.py` (= `backend/app/domain` 패키지에서 모두 re-export):

| 심볼 | 종류 | 설명 |
|------|------|------|
| `RealizedTrade` | `@dataclass(frozen=True)` | 매도 실현 손익 1건 입력. (`asset_id`, `sold_at`, `qty`, `proceeds`, `cost_basis`, `realized_pnl`, `currency`, `fx_rate_at_sale=None`) |
| `DividendIncome` | `@dataclass(frozen=True)` | 배당 소득 1건 입력. (`asset_id`, `paid_at`, `amount`, `currency`, `fx_rate_at_pay=None`) |
| `TaxResult` | `@dataclass(frozen=True)` | plugin 출력. (`year`, `tax_amount` base_currency 환산, `breakdown` dict, `note=None` 한국어 가능) |
| `TaxPlugin` | `@runtime_checkable Protocol` | plugin 인터페이스. `name: str` + `calculate(realized_trades, dividends, year, base_currency) -> TaxResult` |
| `NoTaxPlugin` | class | MVP 디폴트. `name = "no_tax"`, `calculate()` → `TaxResult(year, Decimal("0"), {}, None)` |
| `apply_tax_to_portfolio` | function | engine 호출 헬퍼. `(plugin, realized_trades, dividends, year, base_currency) -> TaxResult`. 향후 검증/로깅 일원화 지점. |

### 설계 메모

- `TaxPlugin` 에 `@runtime_checkable` 적용 — DoD #4 의 `isinstance()` 검사 통과 + 향후 plugin 등록 시 런타임 검증 가능. 비활성 시 `isinstance` 가 `TypeError` 발생.
- `RealizedTrade.fx_rate_at_sale` / `DividendIncome.fx_rate_at_pay` 는 `Decimal | None` — MVP NoTax 는 무시하지만, Phase 3+ 한국 거주자 plugin 이 base_currency 환산 시 사용. plugin 이 직접 환산하므로 도메인은 환율 정책에 비종속.
- `TaxResult.breakdown` 은 `dict[str, Decimal]` — plugin 별로 키 정의 자유 (예: `"capital_gains"`, `"dividend_tax"`, `"foreign_tax_credit"`). UI 가 표시 시 plugin.name 별 라벨 매핑.
- `apply_tax_to_portfolio` 는 현재 단순 위임이지만 별도 함수로 분리 — 향후 `assert plugin.name in registry` 같은 검증, 로깅, 메트릭 hook 을 한 곳에서 추가하기 위함.

## 클린 코드 체크

- [x] 도메인 순수 — 외부 의존 0 (sqlalchemy/pandas/yfinance 미사용)
- [x] frozen dataclass 로 불변성 강제
- [x] Protocol 로 의존성 역전 — `engine.py` 는 `TaxPlugin` 만 알고 구현체 교체 자유
- [x] NoTaxPlugin 은 빈 구현 — Phase 3+ 에서 `KoreanResidentTaxPlugin` 등 추가 가능 (인터페이스 변경 없이)
- [x] 타입힌트 100% (PEP 604 `Decimal | None` 사용)

## 다음 제안

- **TASK-062 (백테스트 종료 hook)**: `engine.run_backtest()` 가 회계연도 종료 시점 (또는 백테스트 종료 시 마지막 `year`) 에 `apply_tax_to_portfolio(plugin, ...)` 호출 → `tax_amount` 만큼 `portfolio.cash_by_ccy[base_currency]` 에서 차감. MVP 는 `BacktestRunContext` 에 `tax_plugin: TaxPlugin = NoTaxPlugin()` 디폴트 주입. UI 토글 OFF 상태 유지 시 NoTaxPlugin 그대로.
- **TASK-064 (실현 거래/배당 수집)**: `engine.run_backtest()` 가 각 매도 시 `RealizedTrade` 누적, dividend.py 의 `DividendCredit` 발생 시 `DividendIncome` 누적 → 회계연도 종료 시 plugin 으로 전달. 현재 `Portfolio` 에 `realized_trades: list[RealizedTrade]` 필드는 없음 — 누적 구조는 engine 내부 로컬로 두거나 Portfolio 확장 결정 필요.
- **Phase 3+ (KoreanResidentTaxPlugin)**: `architecture.md` L679 항목 (해외 양도세 22% / 250만원 공제 / 배당 15.4% / kr_tax_class 별 차등) 구현. `Asset.kr_tax_class` 필드 (TASK-023 의 asset 모델) 와 결합. `fx_rate_at_sale` / `fx_rate_at_pay` 활용.
