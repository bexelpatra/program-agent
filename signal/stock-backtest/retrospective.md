# Retrospective — V3 Phase 1 MVP

## 프로젝트 요약

- **이름**: stock-backtest (Quant Lab) V3 Phase 1 MVP
- **태스크 수**: 36개 (모두 DONE, 첫 시도 성공률 100%)
- **세션 수**: 1 세션 (2026-04-29 새벽 ~ 정오)
- **재시도**: 0 — Reviewer NEEDS_REVISION 1회 (사전 검증 단계, Coder 호출 전 해결됨)
- **Blocker 잔여**: 2개 (둘 다 SOFT, 사용자 액션 필요 영역)
  - BLOCKER-001 PARTIAL: DB V1/V2 잔재 → 사용자가 `docker compose down -v && alembic upgrade head` 실행 필요
  - BLOCKER-002 TODO: pykrx 한국 ETF 분배금 미지원 (MVP 한계, Phase 2 외부 데이터 소스 도입 검토)

## 산출물

### 백엔드 (Python / FastAPI)
- 9 SQLAlchemy 모델 + 3 alembic revisions
- 도메인 11 모듈 (asset entity/repository/calendar_guard/period_adjustment/registration, portfolio, trade, calendar, strategy, engine, dividend, metrics, tax + 5 allocators/filters)
- 7 API 엔드포인트 (assets 4 + strategies 1 + backtests 5 + health) + 비동기 job 모델
- 데이터 어댑터 2개 (yfinance, pykrx) + 증분 파이프라인 + APScheduler cron 3 잡
- 백그라운드 백테스트 runner + Tax plugin 인터페이스

### 프런트 (Next.js 14 / TypeScript)
- 화면 3개 (UI/UX 원칙 6 화면 한도 유지): /assets, /backtests/new, /backtests/[run_id]
- 컴포넌트 13개 (ui 7 + asset 2 + backtest 6) + Zod schemas + i18n 한국어
- 진행률 폴링 hook + in-place 패널 (화면 추가 없이)

### 테스트
- 골든 스냅샷 9 케이스 + 3 invariant
- 회귀 테스트 50 케이스 (look-ahead + 비거래일 4단계 + cash_by_ccy 환전)
- API 계약 (schemathesis) + 비동기 job 통합 스모크
- 총 67 PASS / 16 SOFT skip (BLOCKER-001 영향) / 0 실패

## 잘 된 점

### 1. 사용자 결정 → 코드 충실도
사용자와 16 라운드 Q&A (Q1~Q16) 로 자산/도메인 + 현금/FX 핵심을 사전 합의 → architecture.md V3 섹션 → task-board → 에이전트 위임 흐름이 매끄러웠음. 특히 V1→V2 에서 고생했던 "현금/FX" 영역을 사전 결정으로 묶어 재실행 0회.

### 2. 모델 A 구조적 차단
"D 일 종가 시그널 → D+1 일 시가 체결" 정책을 `engine.py` L209 `prices_until_d = ctx.prices_aligned.loc[:d]` 한 줄로 구조적 차단. SpyAllocator/SpyFilter 회귀 테스트로 D+1 노출 0건 검증. look-ahead bias 가 코드 수준에서 불가능하게 됨.

### 3. 클린 아키텍처 일관성
도메인 11 모듈 모두 banned imports 0 (sqlalchemy/fastapi/yfinance/pykrx/app.data/app.models 미참조). Repository Protocol 로 의존성 역전. Coder 가 자체 검증 (AST grep) 으로 위반 발견 시 즉시 정정.

### 4. 병렬 실행 안전성
8 라운드 병렬 Agent 호출 (총 24 호출) 동안 파일 충돌 0건. Reviewer N3 (engine.py 단일 파일 vs 6 태스크 충돌 위험) 을 사전 발견 → architecture.md V3 § "백엔드 모듈 분할" 으로 8개 파일 분할 명시 + 각 태스크에 파일 경로 명시 → 병렬 안전성 확보.

### 5. UI/UX 원칙 6대 강제
"화면 3개 한도" 가 TASK-094 (진행률 폴링) 의 in-place 패널 결정으로 자연스럽게 지켜짐. JSON 노출 금지는 TASK-092 의 dict 파라미터 임시 우회 발견 → 후속 AssetWeightMap 위젯 권장으로 명시.

### 6. 한국어 일관성
모든 UI 라벨 / 에러 메시지 / 한국어 통지 (ko.ts dict 기반). 사용자 (한국 거주자, 비개발자 친화 미션) 와 정렬.

## 문제점 및 개선 제안

### 문제 1 — 데이터 로더 placeholder 가 통합 단계까지 미뤄짐

**무엇이 문제였나**: TASK-062 (백테스트 API) 가 backtest_runner 의 데이터 로더를 placeholder (`pd.DataFrame()`) 로 작성. TASK-100 통합 단계까지 placeholder 가 유지되어 모든 e2e 시나리오가 NotImplemented 로 실패.

**왜 발생했나**: TASK-062 의 spec 이 "API 라우터 + 비동기 job" 에 집중하면서 "엔진에 데이터를 어떻게 공급할지" 가 별개 책임으로 분리되었어야 함. task-board 분해 시 "데이터 로더" 를 별도 태스크 (TASK-070 등) 로 두지 않음.

**개선 제안**: 향후 task-board 분해 시 "공급/소비 경계" 를 명시적 태스크로 분리. API/UI 가 도메인 함수를 직접 호출하기 전 "ETL/어댑터 태스크" 가 선행 의존성에 들어가야 함.

### 문제 2 — Tester severity=blocker 가 코드 결함이 아닌 환경 영향에도 부여됨

**무엇이 문제였나**: TASK-080+082 Tester 가 BLOCKER-001 (DB 잔재) 영향으로 16 케이스 SOFT skip 한 후 frontmatter severity=blocker 표기. CLAUDE.md Step 4 자동 처리 규칙은 blocker → 후속 코드 수정 태스크 등록인데, 이 경우는 사용자 환경 액션이라 코드 수정 불가능. Manager 가 별도 판단으로 신규 태스크 등록 안 함.

**왜 발생했나**: agents/tester.md 의 severity 규칙 (L83-89) 이 "코드 결함 vs 환경 결함" 을 명시적으로 구분하지 않음.

**개선 제안**: agents/tester.md 의 severity 부여 규칙에 "환경/인프라 미적용 (사용자 액션 필요) 인 경우 severity 미부여 또는 별도 'environment' 카테고리" 추가. Manager 의 자동 후속 태스크 생성 규칙도 환경 결함은 제외 명시.

### 문제 3 — pydantic JSON Schema → React 폼 자동 생성의 한계

**무엇이 문제였나**: TASK-092 의 StrategyParamsForm 이 dict 타입 파라미터 (FixedWeight.weights) 를 JSON-string 입력으로 우회. UI/UX 원칙 1 (JSON 노출 금지) 잠재 위반.

**왜 발생했나**: pydantic JSON Schema 는 고도화되어 있지만, React 폼 자동 생성기 (react-jsonschema-form) 도입 없이 수동 매핑으로 시작. dict/array 같은 복합 타입은 전용 위젯이 필요한데 MVP 에서 구현 못 함.

**개선 제안**: Phase 2 초기에 `AssetWeightMap` (asset_id → 비중 슬라이더 + 합 100% 자동 검증) 위젯 신규. 또는 react-jsonschema-form + 커스텀 위젯 매핑.

### 문제 4 — Reviewer 호출 횟수 부족 (사전 검증 1회만)

**무엇이 문제였나**: CLAUDE.md "Manager의 사용 규칙" 은 "Coder/Tester report 수신 후, 태스크를 DONE으로 마감하기 전 (선택) — 보고서 주장과 실제 코드/테스트 결과가 일치하는지" 도 권장. 이번 프로젝트는 사전 검증 (task-board 분해 후) 1회만. 매 Coder 결과 검증은 생략.

**왜 발생했나**: 시간 효율 + 자율 진행 모드에서 Reviewer 호출 비용 부담. 결과적으로 Coder 의 "DONE" 주장만 신뢰.

**개선 제안**: 큰 마일스톤 (예: 도메인 코어 완료, 통합 직전) 에는 Reviewer 호출 권장. 또는 Manager 가 Coder report 의 핵심 주장 (예: "import 검증 PASS") 을 직접 grep/run 으로 확인.

### 문제 5 — 데이터 로더의 forward-fill 경계 미검증

**무엇이 문제였나**: TASK-100 의 data_loader 가 forward-fill 로 비base 시장 가격을 정렬하지만, 자산의 데이터 시작일 이전 (lookback 부족) 처리는 None 반환. engine 이 None 받으면 어떻게 되는지 단위 테스트 없음.

**개선 제안**: Phase 2 진입 전 data_loader 단위 테스트 (TASK-100 권장 사항) 작성.

## 파이프라인 개선 제안

### 제안 1: agents/tester.md 의 severity 규칙에 'environment' 카테고리 추가

- **대상 파일**: `agents/tester.md`
- **현재**: severity ∈ {blocker, bug, observation}. 환경/인프라 미적용도 blocker 로 분류 가능.
- **제안**:
  ```
  - blocker: 코드 결함으로 기능 자체 동작 불가 — 후속 코드 수정 태스크 필요
  - bug: 코드 결함, 사양 위반 — 후속 코드 수정 태스크 필요
  - observation: 관찰/개선 포인트 — 코드 결함이지만 후속 태스크는 Manager 판단
  - environment: 사용자 액션 필요 (DB 초기화, 환경 변수 설정 등) — 코드 수정 불필요. blockers.md 갱신만.
  ```
- **이유**: Manager 의 Step 4 자동 후속 태스크 생성 규칙이 환경 결함에도 트리거되지 않도록 명확화. 이번 프로젝트의 BLOCKER-001 영향 보고가 정확히 분류됨.

### 제안 2: task-board 분해 시 "데이터 공급/소비 경계" 명시적 태스크화

- **대상 파일**: `CLAUDE.md` Step 2 (태스크 분해 섹션)
- **현재**: "작업을 구체적이고 독립적인 태스크로 분해한다" 만 명시.
- **제안**: 추가 가이드 — "API/UI 태스크가 도메인 함수를 호출하기 전 데이터 공급 (ETL/어댑터/로더) 태스크를 의존성에 명시한다. 임시 placeholder 우회는 별도 후속 태스크로 분리하지 말고, 공급 태스크의 일부로 통합한다."
- **이유**: 이번 프로젝트의 TASK-062 placeholder 가 TASK-100 까지 미뤄진 문제 방지.

### 제안 3: Reviewer 호출 마일스톤 명시

- **대상 파일**: `CLAUDE.md` Step 3 (Reviewer 검증 섹션)
- **현재**: "Coder/Tester를 호출하기 전, Reviewer를 먼저 호출" 만 명시.
- **제안**: 추가 — "도메인 코어 완료 (예: engine.py 와 모든 의존 모듈) 또는 통합 직전 (예: 마지막 통합 태스크 시작 전) 에는 Reviewer 재호출을 권장한다. Coder report 의 'DONE' 주장만 신뢰하지 말고, Reviewer 가 코드/테스트 결과의 일관성 검증."
- **이유**: 자율 진행 모드에서도 핵심 마일스톤은 독립 검증 받기.

### 제안 4: 프런트 폼 자동 생성 위젯 라이브러리 도입 권장

- **대상 파일**: `agents/coder.md` 또는 새 파일 `agents/frontend-coder.md`
- **현재**: 프런트 코더가 pydantic JSON Schema 를 수동으로 React 폼으로 변환.
- **제안**: 향후 프런트 태스크에서 dict/array/nested object 파라미터 발견 시 react-jsonschema-form 또는 커스텀 위젯 (AssetWeightMap 등) 사용을 명시.
- **이유**: UI/UX 원칙 1 (JSON 노출 금지) 의 잠재 위반 방지.

## 사용자에게 보고 후 결정 받을 사항

- 위 4개 파이프라인 개선 제안 중 어느 것을 적용할지
- BLOCKER-001/002 처리 우선순위 (사용자 환경에서 docker compose down -v + alembic upgrade head 실행 / pykrx 분배금 외부 소스 도입 시점)
- Phase 2 시작 시점 + 범위 (계절성 분석 우선 vs 다른 영역)

## 다음 단계 (Phase 2 후보)

1. **계절성 분석** (V3 architecture L729): 미국 정치 사이클·FOMC·Sell-in-May·실적 시즌·한국 정치. market_events 테이블 + 분석 페이지.
2. **한국 거주자 세금 plugin** (V3 § Tax 모듈 L646): 해외 양도세 22% / 배당 15.4% / 한국 상장 해외 ETF.
3. **AssetWeightMap 위젯** + 다중 전략 합성 (composer) UI.
4. **워커 크래시 복구** (Celery/Redis 기반 큐 도입).
