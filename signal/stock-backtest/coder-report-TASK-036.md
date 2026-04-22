# Coder Report — TASK-036

## 태스크
- ID: TASK-036
- Title: 한국 거주자 세금 모듈 + 엔진 연동 훅 + 단위 테스트
- Status: DONE

## 작업 요약

백테스트 엔진이 호출할 한국 거주자 세금 정책 모듈을 신규 구현하고 단위 테스트로 동작을 검증했다. 엔진 통합(TASK-016)에서 바로 꽂아 쓸 수 있도록 세 개의 훅(`apply_realized_gain`, `apply_dividend`, `on_year_end`)만 공개하는 얇은 인터페이스로 정리했다.

## 산출물

### 신규 파일
- `projects/stock-backtest/src/stock_backtest/backtest/tax.py`
  - 값 객체: `RealizedTrade` (frozen dataclass), `TaxYearState` (mutable dataclass).
  - 정책: `KrResidentTax`, `NoopTax` (공통 베이스 `_TaxPolicy`).
  - 팩토리: `KrResidentTax.from_config(settings)`, `build_tax_policy(settings)`.
  - 금액은 전부 `decimal.Decimal`, 최종 KRW 정수 라운딩 (`ROUND_HALF_UP`).
- `projects/stock-backtest/tests/test_tax.py`
  - 태스크에 명시된 9개 시나리오 + 보조 케이스 총 16개 테스트.

### 과세 규칙 구현
- `overseas_equity`, `overseas_etf`, `kr_overseas_etf` → 공용 연간 버킷. 누적 실현익 − 250만원 공제 후 22%. 음수 손실은 같은 해 이익과 상계(이전에 과세된 몫은 음수 `tax_delta`로 환원 반영).
- `kr_equity_etf`, `commodity` → 비과세 (보고용 bucket에만 누적).
- `kr_bond_etf`, `kr_mixed_etf` → 실현익이 양수일 때만 15.4% (손실은 미환급).
- `crypto` → `crypto_enabled=true`면 overseas와 동일한 250만원 공제 + 22%. false면 과세 0.
- 배당 (`is_dividend=True`) → class 무관 15.4% 원천징수. 한계는 모듈 docstring에 명시.
- 연말 `on_year_end` → 다음 해 연도로 새 `TaxYearState` 반환 (손실 carry-over 없음, 단순화 문서화).

### 설정 연계
- `KrResidentTax.from_config(settings)` — `settings.tax.profiles[settings.tax.profile]`을 `model_dump(exclude_none=True)`로 뽑아 생성.
- `build_tax_policy(settings)` — `tax.enabled=false` 또는 미지정/비어있는 프로파일이면 `NoopTax` 반환. `profile == "kr_resident"`이면 `KrResidentTax`.

## 테스트 실행 결과

```
$ python -m pytest tests/test_tax.py -v
============================= test session starts ==============================
platform linux -- Python 3.11.3, pytest-9.0.2, pluggy-1.6.0
collected 16 items

tests/test_tax.py::test_overseas_gain_below_deduction_is_untaxed PASSED
tests/test_tax.py::test_overseas_gain_above_deduction_uses_22pct PASSED
tests/test_tax.py::test_overseas_loss_then_gain_nets_within_year PASSED
tests/test_tax.py::test_kr_equity_etf_capital_gain_is_tax_free PASSED
tests/test_tax.py::test_kr_bond_etf_capital_gain_taxed_at_15_4 PASSED
tests/test_tax.py::test_kr_bond_etf_loss_is_not_refundable PASSED
tests/test_tax.py::test_dividend_withholds_15_4 PASSED
tests/test_tax.py::test_apply_dividend_rejects_non_dividend_trade PASSED
tests/test_tax.py::test_apply_realized_gain_rejects_dividend_trade PASSED
tests/test_tax.py::test_crypto_disabled_does_not_tax PASSED
tests/test_tax.py::test_crypto_enabled_uses_22pct_with_deduction PASSED
tests/test_tax.py::test_on_year_end_resets_state PASSED
tests/test_tax.py::test_noop_tax_charges_nothing PASSED
tests/test_tax.py::test_build_tax_policy_respects_enabled_flag PASSED
tests/test_tax.py::test_build_tax_policy_returns_kr_resident_when_enabled PASSED
tests/test_tax.py::test_unknown_asset_class_raises PASSED

============================== 16 passed in 0.07s ==============================
```

숫자 검증 하이라이트:
- 해외 실현익 200만 → 0원.
- 해외 실현익 500만 → 550,000원.
- 해외 −100만 후 +400만 누적 +300만 → 110,000원.
- 국내 채권 ETF 실현익 100만 → 154,000원.
- 배당 100만 → 154,000원.

## 설계 메모 / 한계 (보고)

- **손실 carry-over 미구현**: 해외/크립토 버킷은 같은 해 내 상계만 지원. 연도 경계에서 상태를 리셋한다. 법/설계 확장이 필요하면 `TaxYearState`에 `carry_over_loss` 필드를 추가하고 `on_year_end`에서 이월하도록 고치면 된다.
- **외국납부세액공제 / 종합과세 미반영**: 배당 15.4% 일괄 적용. docstring 명시.
- **국내 상장 해외형 ETF 분배금**: 배당 hook에서 동일 15.4% 처리. 필요 시 자산별 rate override가 가능하도록 확장 여지 남겨둠 (현재는 프로파일 단일 rate).
- **자산 매핑 책임**: `assets.meta.kr_tax_class` → `AssetClass` 매핑은 엔진/리포지토리 레이어의 몫. 이 모듈은 문자열로 받은 class를 신뢰한다. `commodity`는 추상화상 포함하되 현재 비과세 처리 (향후 파생형 과세 도입 시 갱신).
- **엔진 연동 훅**: TASK-016에서 리밸런싱 매도 발생 시 `RealizedTrade`를 구성해 `apply_realized_gain`을 호출하고, 해당 tax_delta만큼 portfolio 현금에서 차감하면 된다. 연도가 바뀌는 거래일을 감지했을 때 `on_year_end`로 state를 갱신.

## 변경된 파일
- `projects/stock-backtest/src/stock_backtest/backtest/tax.py` (신규)
- `projects/stock-backtest/tests/test_tax.py` (신규)

## 상태: DONE
