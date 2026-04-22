---
agent: coder
task_id: TASK-041
status: DONE
timestamp: 2026-04-14T15:19:00
---

## 결과 요약

웹 UX 개선 5개 항목을 모두 반영했다.

1. **홈 페이지 (`/`) 추가**: Dash `register_page(path="/")` 로 새 페이지 생성. 플랫폼 개요, 4개 하위 페이지 카드(이름/경로/1줄설명), DB 상태 요약(자산 수 + 최신 OHLCV 날짜)을 표시. DB 접근은 try/except 로 감싸 실패 시 "확인 불가" fallback.
2. **전략 설명 렌더**: `_strategy_form_fields` 가 전략 클래스의 `description` (ClassVar) 을 폼 필드 위 회색 이탤릭 박스로 표시. MovingAverageCrossover / SeasonalMovingAverage 의 description 을 2~4문장으로 풍부하게 재작성.
3. **Universe 도움말**: `/backtest` 의 Universe Textarea 아래에 3줄 caption (`@시장` 문법, `required_universe()` fallback 설명).
4. **필드 description 한글화**: crossover.py / seasonal.py 의 pydantic Field description 을 사용자 친화적 한국어로 교체 (`risky_symbol`, `safe_symbol`, `fast_window`, `slow_window`, `seasonality_mode`, `combine_mode`, `alpha`, `custom_months`, `election_dates`).
5. **폼 렌더 개선**: 라벨(굵은 필드명) 과 description(회색 작은 글씨)을 별도 줄로 분리해 긴 설명도 깔끔히 표시.

navbar 에도 "홈" 링크를 추가했다. MovingAverage 전략 2개는 이미 `required_universe()` 가 구현돼 있어 추가 작업 불필요.

`rebalance` 필드는 MovingAverage 두 전략의 pydantic schema 에 실제로 존재하지 않음(리밸런싱 주기는 엔진이 `rebalance_dates` 로 주입). 존재하지 않는 필드에 description 추가는 skip.

## 변경된 파일

- `projects/stock-backtest/src/stock_backtest/web/pages/home.py` (신규) — 홈 페이지
- `projects/stock-backtest/src/stock_backtest/web/components/layout.py` (수정) — navbar 에 "홈" 링크 추가
- `projects/stock-backtest/src/stock_backtest/web/pages/backtest.py` (수정) — 전략 설명 박스, 필드 라벨/설명 분리, Universe 도움말 캡션
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/crossover.py` (수정) — description ClassVar 풍부화, Field description 한글화
- `projects/stock-backtest/src/stock_backtest/strategies/dynamic/moving_average/seasonal.py` (수정) — description ClassVar 풍부화, Field description 한글화

## 검증

- **문법 체크**: `ast.parse(home.py)`, `ast.parse(backtest.py)` → `syntax ok`.
- **페이지 레지스트리 체크**: `from stock_backtest.web.app import create_app; create_app()` 후 `dash.page_registry` 가 `['/', '/backtest', '/data', '/history', '/seasonality']` 모두 포함.
- **전략 description 체크**:
  - `cross.desc` = "단기·장기 이동평균선을 이용한 추세추종 전략. fast MA > slow MA..."
  - `seasonal.desc` = "이동평균 크로스오버에 계절성 게이트를 결합한 전략. MA 추세 신호와 계절 신호..."
  - `cross risky_symbol desc` = "상승장/추세장에 보유할 위험자산 심볼 (예: SPY, QQQ)"
  - `required_universe` 메서드 존재 확인 OK.
- **서비스 리스타트**: `ctl restart stock-backtest-web` 성공 (pid 2517531). 로그에 traceback 없이 정상 기동. `Dash is running on http://0.0.0.0:8050/`.
- **HTTP 체크**: `curl /` → 200, `curl /backtest` → 200.

## 이슈/블로커

없음. (로그에 보인 "다음 심볼을 assets 테이블에서 찾을 수 없습니다: ['btc', 'usd']" 은 사용자가 Universe 에 잘못된 심볼을 입력한 런타임 케이스이고, UI 가 정상적으로 ValueError 를 사용자에게 노출하는 동작. 본 태스크 범위 외.)

## 다음 제안

- `dual_momentum`, `momentum`, `vaa`, `risk_parity`, `fixed_weight`, `permanent` 전략의 Field description 도 동일 기준(한글 풀문장, 예시 포함)으로 일괄 정비하는 후속 태스크 권장. 본 태스크에서는 명백한 부족이 없어 스킵.
- `rebalance` 주기를 UI 에서 선택할 수 있도록 BacktestConfig 에 노출하는 기능 제안 (현재 엔진 내부 고정). 별도 태스크.
