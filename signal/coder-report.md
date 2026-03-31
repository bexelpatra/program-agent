---
agent: coder
task_id: TASK-004
status: DONE
timestamp: 2026-03-25T17:00:00
---

## 결과 요약
백테스팅 엔진 `src/backtester.py` 구현 완료. Backtester 클래스가 전략의 Signal 리스트와 가격 DataFrame을 받아 매매 시뮬레이션을 수행하고, 7종 성과 지표 계산 및 Buy & Hold 벤치마크 비교를 제공한다.

### 구현 기능
- **Backtester 클래스**: initial_capital, commission_rate, slippage, risk_free_rate 설정
- **시뮬레이션**: Signal의 weight 반영 포지션 크기 (BUY: 현금의 weight%, SELL: 보유주식의 weight%)
- **수수료/슬리피지**: 매수 시 가격 상승, 매도 시 가격 하락으로 적용
- **성과 지표 7종**: total_return, cagr, mdd, sharpe_ratio, win_rate, profit_loss_ratio, total_trades
- **Buy & Hold 벤치마크**: 자동 생성 및 alpha 계산
- **run()**: 결과 dict 반환 (metrics, benchmark, portfolio DataFrame, trades list)
- **summary()**: 터미널 출력용 텍스트 리포트

## 변경된 파일
- src/backtester.py (신규)

## 이슈/블로커
없음

## 다음 제안
TASK-004 완료. 테스트(test_backtester.py) 실행으로 검증 가능.
