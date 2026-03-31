# Coder Report — TASK-003

## Status: DONE

## Task
분석 프레임워크 및 전략 플러그인 구현

## 작업 내역

### 1. `src/analyzer/base.py`
- `SignalType` Enum 정의 (BUY, SELL, HOLD)
- `Signal` dataclass 정의 (date, signal_type, weight)
- `BaseStrategy` ABC 정의 (name, description, analyze, generate_signals)
- architecture.md에 정의된 인터페이스를 그대로 구현

### 2. `src/analyzer/seasonality.py` — SeasonalityStrategy
- statsmodels STL 사용하여 종가 시계열을 추세/계절성/잔차로 분해
- period 파라미터 (기본 252 = 연간 거래일)
- 계절성 강도 계산: 1 - Var(Resid) / Var(Seasonal + Resid)
- 추세 방향 판단: 최근 period 구간의 기울기 기반 (up/down/flat)
- 데이터 부족 시 안전하게 빈 결과 반환

### 3. `src/analyzer/moving_average.py` — MovingAverageStrategy
- 단기(50일) / 장기(200일) SMA 계산
- 골든크로스(단기>장기) / 데드크로스(단기<장기) 탐지: diff 부호 전환으로 감지
- analyze(): 크로스오버 이벤트 목록, 현재 상태(bullish/bearish) 반환
- generate_signals(): 골든크로스=BUY, 데드크로스=SELL 시그널 생성 (weight=1.0)

### 4. `src/analyzer/correlation.py` — CorrelationStrategy
- 멀티 심볼 피벗 테이블(인덱스: date, 컬럼: 심볼) 입력
- 일간 수익률 기반 전체 기간 상관관계 행렬 계산
- 롤링 상관관계 (기본 60일 윈도우) — 모든 심볼 쌍
- 주요 상관관계 변화 감지: 최근 vs 전체 평균 차이 > 0.2 시 보고

### 5. `src/analyzer/__init__.py` — StrategyRegistry
- register(), get(), list_all() 클래스 메서드 구현
- 모듈 로드 시 3개 기본 전략 자동 등록: seasonality, moving_average, correlation

## 검증 결과
- 전체 import 성공 확인
- StrategyRegistry.list_all() → ['seasonality', 'moving_average', 'correlation']
- StrategyRegistry.get('seasonality') 정상 동작
- 구문 에러 없음

## 생성/수정 파일
- `src/analyzer/__init__.py` (신규)
- `src/analyzer/base.py` (신규)
- `src/analyzer/seasonality.py` (신규)
- `src/analyzer/moving_average.py` (신규)
- `src/analyzer/correlation.py` (신규)
