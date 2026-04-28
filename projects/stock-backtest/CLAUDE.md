# Quant Lab — Project Instructions

## 미션
비개발자 금융 사용자를 위한 퀀트 투자 웹앱. 핵심 기능은 **정적 자산 배분(SAA)**, **동적 자산 배분(DAA)**, **백테스팅** 세 가지이며 이 세 가지는 어떤 변경에도 항상 동작해야 한다.

## 절대 원칙 (NEVER VIOLATE)

1. **사용자에게 JSON/코드를 노출하지 않는다.** 모든 전략 구성은 UI 폼으로. JSON은 내부 저장 형식일 뿐.

2. **모든 전략은 3요소 조합으로 표현한다.**
   - `allocator`: 비중 결정 규칙 (예: FixedWeight, AllWeather, EqualWeight)
   - `signal_filters[]`: 보유 자격 필터 (예: MovingAverage, Momentum). 여러 필터는 AND로 결합. 비어 있을 수 있음.
   - `rebalance_schedule`: `daily` | `weekly` | `monthly` | `quarterly` | `yearly` | `signal_event` 중 하나

   새 전략 추가 = 새 allocator 클래스 또는 새 filter 클래스. 이 구조를 깨는 제안은 거부하고 대안을 제시하라.

3. **백테스팅 실거래 반영도 최소 70%.**
   - 거래 수수료 반영 (기본: 한국 0.015%, 미국 0.005%, 암호화폐 0.1%)
   - 슬리피지 반영 (기본 0.1%, 사용자 조정 가능)
   - Look-ahead bias 금지: 시그널은 당일 종가 기준 판정, 체결은 다음 거래일 시가
   - 배당은 현금으로 수령하여 다음 리밸런싱에 편입
   - 환율은 해외 자산 매수 시점 환율로 고정 (FX 거래는 별도로 취급하지 않음)

4. **결과 지표는 항상 다음을 계산한다**: CAGR, MDD, Sharpe, Sortino, Calmar, 승률, 연/월 수익률 테이블.

5. **MVP 프리셋 3종만 구현**: FixedWeight, AllWeather, EqualWeight. 시그널 필터 2종: MovingAverage, Momentum. 추가는 명시적 요청 시에만.

## 디렉토리 구조

```
projects/stock-backtest/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI 라우터
│   │   ├── core/             # 설정, 로깅, 보안
│   │   ├── domain/
│   │   │   ├── allocators/   # FixedWeight, AllWeather, EqualWeight
│   │   │   ├── filters/      # MovingAverage, Momentum
│   │   │   ├── engine.py     # 백테스팅 엔진 (단일 파일 유지)
│   │   │   └── metrics.py    # CAGR, MDD, Sharpe 등
│   │   ├── data/             # yfinance, pykrx, pyupbit 어댑터
│   │   ├── scheduler/        # APScheduler 일일 업데이트 잡
│   │   ├── models/           # SQLAlchemy 모델
│   │   └── schemas/          # Pydantic 스키마
│   ├── tests/
│   └── alembic/
├── frontend/
│   ├── app/                  # Next.js App Router
│   ├── components/
│   │   ├── ui/               # shadcn/ui 생성물
│   │   ├── strategy/         # 전략 빌더 UI
│   │   ├── backtest/         # 결과 차트·지표
│   │   └── asset/            # 자산 검색·선택
│   ├── lib/
│   └── hooks/
├── docker-compose.yml
└── CLAUDE.md
```

## 코드 규칙

- **Python**: Ruff + Black, 타입힌트 필수, Pydantic으로 경계 검증. 함수형 우선, 클래스는 상태/다형성이 필요할 때만.
- **TypeScript**: strict 모드, `any` 금지, Zod로 API 응답 런타임 검증.
- 도메인 로직은 프레임워크 독립. FastAPI 핸들러는 얇게, 로직은 `domain/`에.

## 테스트 규칙

- 백테스팅 엔진 변경 시 **골든 테스트** 필수: 유명 전략(올웨더 2010-2020) 결과를 고정값으로 스냅샷.
- 새 allocator/filter 추가 시 수학적 성질 단위 테스트 (비중 합 = 1, 필터 결과 boolean 시리즈 등).
- API 변경 시 프론트 Zod 스키마 동기 갱신.

## 작업 흐름

1. 기능 추가 시 먼저 `domain/` 레이어 구현 + 테스트
2. API 노출
3. 프론트 연결
4. 모든 단계에서 `reviewer` 서브에이전트에 리뷰 요청 (PR 머지 전)

## 금지 사항

- 테스트 없이 백테스팅 엔진 수정 금지
- 시장 데이터를 엔진 내부에서 직접 fetch 금지 (항상 저장된 DB에서 읽기)
- 프리셋 3종 외 추가 요청 시 사용자 확인 없이 추가 금지
