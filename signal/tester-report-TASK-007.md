# Tester Report — TASK-007

## 상태: DONE

## 태스크
- Task ID: TASK-007
- Title: 분석 전략 + 백테스터 테스트

## 작성된 테스트 파일

### 1. `tests/test_strategies.py` (23개 테스트)

| 클래스 | 테스트 수 | 커버리지 |
|--------|-----------|----------|
| TestStrategyRegistry | 4 | register/get/list_all, 커스텀 전략 등록, 미등록 전략 KeyError |
| TestSeasonalityStrategy | 4 | STL 분해 실행(600일), 데이터 부족 처리, 결과 키 검증, 빈 시그널 |
| TestMovingAverageStrategy | 7 | SMA 정확성, 데이터 부족, 크로스오버 탐지, generate_signals() 반환 타입/수, 골든크로스=BUY |
| TestCorrelationStrategy | 6 | 상관관계 행렬, 롤링 상관관계, 데이터 부족, 단일 심볼, 빈 입력, 2심볼 |

### 2. `tests/test_backtester.py` (24개 테스트)

| 클래스 | 테스트 수 | 커버리지 |
|--------|-----------|----------|
| TestBacktesterBasic | 5 | 시그널 없음, BUY→포지션 증가, SELL→감소, 포지션 없이 SELL, HOLD |
| TestBacktesterWeight | 2 | weight=0.5 매수(자본 50%), weight=0.5 매도(절반) |
| TestBacktesterCosts | 3 | 수수료 적용, 슬리피지 적용, Trade 기록 확인 |
| TestBacktesterMetrics | 5 | total_return, MDD, Sharpe, 승률/수익손실비, CAGR |
| TestBacktesterBenchmark | 3 | benchmark 존재, Buy&Hold 수익률, alpha 계산 |
| TestBacktesterSummary | 2 | 문자열 반환, 주요 지표 포함 |
| TestBacktesterEmpty | 4 | 빈 DataFrame, date 누락, close 누락, 1행 데이터 |

## 테스트 결과

```
47 passed in 0.82s
```

- 통과: 47/47 (100%)
- 실패: 0
- 에러: 0

## 비고
- 초기 실행 시 `test_two_symbols`에서 상관관계 임계값이 너무 높아 1건 실패 → 테스트 데이터의 노이즈를 줄여 수정 후 전체 통과.
- `src/` 파일은 수정하지 않았음.
