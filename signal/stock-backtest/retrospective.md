# Retrospective — stock-backtest

## 프로젝트 요약
- 이름: stock-backtest (시계열 기반 자산배분·계절성 백테스팅 플랫폼)
- 태스크 수: 38 등록 / 37 DONE / 1 TODO(TASK-014, 실 DB+네트워크 필요로 사용자 몫)
- 첫 시도 성공: 35, 재시도/후속 태스크 생성: 2 (TASK-019 회귀 테스트에서 발견된 엔진 버그 → TASK-037/038 자동 생성)
- 세션 수: 2 (중간 context compaction 1회)

## 잘 된 점
- **태스크 분해 품질**: 초기 38개 분해가 대부분 파일 수준에서 독립적이어서 한 라운드에 3~5 태스크를 병렬 실행할 수 있었다. 특히 ingestion(007/008/009), strategies(020/021/022), web pages(028~031) 묶음은 충돌 없이 병렬 완주.
- **Tester → Coder 자동 연결**: TASK-019가 발견한 FX 스프레드 부호 버그와 50bps 하드코딩 쿠션을 즉시 TASK-037/038로 등록해 수정. 회귀 테스트가 설계 결함(architecture 결정 #4 위반)을 실제로 잡아낸 케이스.
- **Pydantic params_schema → 자동 UI 폼**: 전략 등록 패턴이 가볍고 확장 비용이 사실상 0이다. 백테스트 페이지가 새 전략을 코드 수정 없이 바로 노출.
- **환경 이슈의 국소화**: numpy<2 pin, PYTEST_DISABLE_PLUGIN_AUTOLOAD, ast.parse 검증 대안 등 환경 문제를 코드 변경 없이 우회.

## 문제점
1. **repository 계층의 빠진 메서드를 태스크 진행 중에야 발견** — TASK-018/031에서 `list_runs`가 없다는 것을 구현 직전에야 알고 scalars 직접 쿼리로 우회. 설계 단계에서 repository 공개 API를 열거하지 않은 탓.
2. **REJECTED 재수집 미구현**: TASK-033 E2E에서 `MAX(time)+1` 전략이 중간 REJECTED row를 커버하지 못함을 확인. 갭 스캐너가 별도로 필요하나 현재 태스크 보드에는 등록되지 않음.
3. **TASK-014 미실행**: 실 DB·외부 소스 호출이 필요해 에이전트가 실행할 수 없는 태스크가 보드에 남음. 사용자-실행 태스크와 에이전트-실행 태스크를 분리했으면 흐름이 더 깨끗했을 것.
4. **Dash pytest 플러그인 이슈**로 일부 테스트 실행에 `-p no:dash` 필요. 환경 의존이라 코드 책임은 아니지만 README에 흡수.

## 파이프라인 개선 제안

### 제안 1: repository 공개 API 명세를 architecture.md에 고정
- 대상 파일: `signal/{project-id}/architecture.md` 템플릿 또는 프로젝트별 architecture 작성 가이드
- 현재: architecture.md는 스키마/디렉토리/의사결정까지만 기재. 레포지토리 public 메서드 시그니처는 코드 작성 시점에 임기응변.
- 제안: architecture.md에 "Repository API Contract" 절을 필수 섹션으로 추가. 각 레포의 public 메서드 시그니처(타입 포함)를 설계 단계에 미리 열거하고, 이후 태스크들이 이 계약에 맞춰 코드를 작성.
- 이유: 이번 프로젝트에서 `list_runs`, `get_max_ohlcv_time` 등 누락을 태스크 진행 중에 발견해 방어 쿼리/우회 쿼리가 난립. 계약을 먼저 박아두면 누락 발견이 Step 1(설계)로 앞당겨진다.

### 제안 2: "사용자-실행 태스크"와 "에이전트-실행 태스크" 구분 표시
- 대상 파일: `signal/schema.md`, `CLAUDE.md`
- 현재: task-board의 Assignee 컬럼에 coder/tester만 있음. TASK-014처럼 실 인프라가 필요한 작업을 같은 보드에 섞어두면 세션 종료 조건이 애매해진다.
- 제안: `Assignee`에 `user` 값을 허용(또는 별도 `Execution: agent | user` 컬럼 추가). Manager는 `Assignee=user` 태스크를 자동 실행하지 않고, Step 6(회고) 진입 전에 사용자에게 명시 알림.
- 이유: 에이전트 세션이 완료해야 하는 범위와 사람이 해야 하는 범위가 보드 위에서 명확히 분리됨. 회고 타이밍이 깔끔해진다.

### 제안 3: 테스터가 발견한 "코드 이슈"의 자동 태스크화 규칙을 더 엄격히
- 대상 파일: `agents/tester.md`, `CLAUDE.md`
- 현재: CLAUDE.md Step 4.3가 Tester report의 `## 이슈/블로커` 또는 `## 코드 이슈`에서 새 태스크를 만들도록 지시. 하지만 Tester report가 "관찰/참고 — 수정 강제 없음"으로 토을 낮추면 Manager가 태스크 생성을 미룰 가능성.
- 제안: Tester report 스키마에 `severity: [blocker | bug | observation]` 필드를 필수로 넣고, `blocker/bug`는 Manager가 자동으로 태스크를 등록, `observation`만 판단에 맡김. 이번 TASK-033에서 REJECTED 재수집 이슈가 "observation"으로 남았으나, 명시적 severity가 있었다면 의사결정이 더 빨랐다.
- 이유: Tester의 정성적 서술에 의존하지 않고, 구조화된 심각도로 Manager가 일관된 결정을 내릴 수 있다.

### 제안 4: 환경 이슈 체크리스트를 프로젝트 초기화 태스크에 포함
- 대상 파일: `agents/coder.md` 또는 프로젝트 초기화 템플릿
- 현재: TASK-001~002에서 docker/requirements를 구성하지만, numpy/pandas ABI 호환, pytest 플러그인 자동로드 충돌 등 환경 감수성은 사후 발견.
- 제안: 초기화 태스크에 "smoke import 체크" (requirements 설치 직후 `python -c "import pandas, numpy, exchange_calendars; import pytest"` 실행) + 실패 시 즉시 고정(pin) 계획 수립을 DoD로 추가.
- 이유: 이번에 numpy<2 pin을 TASK-009 도중에 알아낸 만큼, 초기 단계로 앞당기면 후속 태스크가 깨끗해진다.

## 남은 후속 작업 (TODO)
- **TASK-014 (사용자 몫)**: Postgres+Timescale 기동 → `docker compose up -d` → Alembic → `scripts/seed_universe.py` + `scripts/seed_market_events.py` → `python -m stock_backtest.ingestion.cli --market ALL` → 커버리지/이상치 리포트 작성.
- **후속 제안 태스크**: "갭 스캐너 (트레이딩 캘린더 ↔ ohlcv 실측 diff → REJECTED/PARTIAL 구간 재요청)" — TASK-033 report의 관찰 반영.
