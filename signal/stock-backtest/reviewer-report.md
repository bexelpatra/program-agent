---
task_id: TASK-001~TASK-100 (재검증, 36개)
verdict: PASS
---

# Reviewer Report: V3 Phase 1 task-board 재검증

## 검증 대상
- 파일:
  - `/home/jai/pa/stock-backtest/signal/stock-backtest/task-board.md` (36 행, `grep -cE '^\| TASK-' = 36`)
  - `/home/jai/pa/stock-backtest/signal/stock-backtest/architecture.md` (796 lines, V3 백엔드 모듈 분할 섹션 L646~L666 신설)
- Manager 주장 요약: 직전 7건 + 사소 1건 모두 반영. architecture.md 에 "V3 백엔드 모듈 분할 (engine 분리 정책)" 섹션 추가 + task-board.md 의 11개 태스크 description 수정.

## 직전 7건 처리 결과

| 항목 | 차단 강도 | 처리 결과 | 근거 |
|------|----------|----------|------|
| N1 | HARD | RESOLVED | task-board.md L19: `**market_events 는 Phase 2 로 이월 (architecture.md L732)** — Phase 1 에서는 생성하지 않음.` 명시. architecture.md `grep -n market_events` 결과 → L755 (Phase 2 정의) 와 일관. Phase 1 마이그레이션 대상에서 market_events 제거 확인. |
| N2 | SOFT | RESOLVED | task-board.md L29 (TASK-022): `비거래일 다층 방어 4단계 중 **수집/캘린더 레이어** ... 조회 레이어는 TASK-030, 엔진 레이어는 TASK-041/043 에서.` 명시. 추가로 TASK-030 L36, TASK-041 L45, TASK-043 L47 모두 해당 레이어 책임 명시 확인 → 4단계 모두 책임 태스크 식별 가능. |
| N3 | HARD | RESOLVED | architecture.md L646~L666 "V3 백엔드 모듈 분할 (engine 분리 정책)" 섹션 신설 (8개 파일 + 2개 서브디렉토리 매핑표). CLAUDE.md L39 "단일 파일 유지" 표현을 "메인 루프 분산 금지" 로 재해석한다는 명시 (V3 우선 원칙 L486 인용). task-board.md TASK-040~045 description 모두 `**파일: backend/app/domain/{xxx}.py**` 굵은 글씨로 파일 경로 명시. 파일 경로 1:1 매핑 검증 결과 모두 일치. |
| N4 | SOFT | RESOLVED | TASK-060 L65 끝부분: `**backend/app/schemas/ 공통 base 스키마**: ErrorResponse, PaginatedResponse, TimestampedModel 등 cross-endpoint base.` TASK-061 L66: `**스키마 모듈**: backend/app/schemas/asset.py (...), backend/app/schemas/strategy.py (...)`. TASK-062 L67: `**스키마 모듈**: backend/app/schemas/backtest.py (...)`. 3개 태스크 모두 schemas 모듈 책임 명시. |
| N5 | SOFT | RESOLVED | TASK-031 L37: `**레이어 분리**: ① domain 서비스 (backend/app/domain/asset/registration.py) 가 비즈니스 로직 담당, data 어댑터 (TASK-020/021) 를 의존성 주입으로 호출 (직접 import 금지) ② 즉시 검증 ③ 백필 큐잉은 scheduler 모듈 (backend/app/scheduler/backfill_queue.py) 에 위임 ④ 부분 백필.` 3 레이어 (domain/data/scheduler) 책임이 명시적으로 분리됨 + 의존 방향 (도메인→데이터 DI) 강제 표현 포함. |
| N6 | SOFT | RESOLVED | TASK-001 L11: `**완료 검증**: pip install -r backend/requirements.txt 성공 + python -c 'import app' (backend/app 패키지) 성공 + cd frontend && npm install 성공 + npm run build 성공. 4개 모두 통과해야 DONE.` 4개 검증 명령 모두 명시. |
| N7 | SOFT | RESOLVED | TASK-094 L85: `**화면 귀속**: TASK-092 (백테스트 생성) 화면 내에서 폼 제출 후 진행률 표시 (in-place 패널), 완료 시 TASK-093 결과 화면으로 라우팅. **별도 진행 화면 만들지 않음 (UI/UX 원칙 6 점진적 노출 — 화면 3개 한도 유지)**.` MVP 화면 3개 원칙 명시적 확인. |
| N8 | 사소 | NOTED | task-board.md 본문에는 숫자 명시 없음 (`grep -c "35개\|36개" task-board.md = 0`). 정정 대상 없음. (보고용 숫자라 본문 갱신 불필요.) |

## 새로 발견된 이슈

없음. 추가 점검 항목:

### task-board.md 행 수 유지
- `grep -cE '^\| TASK-' task-board.md` → **36** (직전 검증과 동일, 누락/중복 없음)
- 중복 ID: 0 (`uniq -c` 검증)
- TASK-001~003, 010~012, 020~023, 030~032, 040~045, 050~054, 060~062, 080~082, 090~094, 100 = 36개 모두 존재 확인

### architecture.md 모듈 분할표 vs task-board 파일 경로 1:1 매핑

| architecture L654-663 파일 | architecture 담당 태스크 | task-board 파일 경로 | 일치 |
|---------------------------|-------------------------|---------------------|------|
| `engine.py` | TASK-043 | TASK-043 L47: `strategy.py + engine.py` | OK |
| `portfolio.py` | TASK-040 | TASK-040 L44: `portfolio.py` | OK |
| `trade.py` | TASK-041 | TASK-041 L45: `trade.py` | OK |
| `calendar.py` | TASK-042 | TASK-042 L46: `calendar.py` | OK |
| `strategy.py` | TASK-043 | TASK-043 L47: `strategy.py + engine.py` | OK |
| `allocators/{fixed,all,equal}.py` | TASK-050,051,052 | TASK-050~052 L55-57 (파일 경로 명시 없으나 architecture 분할표로 식별 가능) | OK (소프트) |
| `filters/{moving,momentum}.py` | TASK-053,054 | TASK-053~054 L58-59 (동일) | OK (소프트) |
| `metrics.py` | TASK-044 | TASK-044 L48: `dividend.py + metrics.py` | OK |
| `dividend.py` | TASK-044 | TASK-044 L48: `dividend.py + metrics.py` | OK |
| `tax.py` | TASK-045 | TASK-045 L49: `tax.py` | OK |

→ TASK-040~045 (엔진 코어 6개) 는 모두 서로 다른 파일을 수정하므로 의존성 순서만 지키면 동일 파일 충돌 없음. TASK-050~054 도 allocators/filters 서브디렉토리로 분리되어 충돌 없음. **병렬 안전성 확인**.

## 의존성 그래프 무결성 재확인

Python 자동 점검 결과:
- 총 태스크: 36
- 중복 ID: 0
- 누락 의존: 0 (모든 Depends On 이 board 에 존재)
- 위상 단계: 14 (순환 없음)

위상 단계 (직전 검증과 동일):
```
L0  001
L1  002, 060
L2  010
L3  003, 011, 012, 030
L4  020, 032, 040
L5  021, 041, 042
L6  022, 043, 044
L7  023, 031, 045, 050, 053
L8  051, 052, 054, 061
L9  062, 090
L10 080, 082, 091
L11 081, 092
L12 093, 094
L13 100
```

→ 그래프 무결성 유지. N3 처리 (engine.py 모듈 분할) 가 의존성 그래프를 변화시키지 않음 (Depends On 관계 변경 없음, 파일 경로만 명시 추가).

## 클린 아키텍처 부합 재확인

| 디렉토리 | 담당 태스크 | 평가 |
|----------|-----------|------|
| backend/app/api | TASK-060, 061, 062 | OK |
| backend/app/core | TASK-001 (스캐폴드) | OK |
| backend/app/domain/portfolio.py | TASK-040 | OK (명시) |
| backend/app/domain/trade.py | TASK-041 | OK (명시) |
| backend/app/domain/calendar.py | TASK-042 | OK (명시) |
| backend/app/domain/strategy.py + engine.py | TASK-043 | OK (명시) |
| backend/app/domain/dividend.py + metrics.py | TASK-044 | OK (명시) |
| backend/app/domain/tax.py | TASK-045 | OK (명시) |
| backend/app/domain/allocators/ | TASK-050, 051, 052 | OK (architecture 매핑) |
| backend/app/domain/filters/ | TASK-053, 054 | OK (architecture 매핑) |
| backend/app/domain/asset/registration.py | TASK-031 | OK (명시) |
| backend/app/data | TASK-020, 021, 022 | OK |
| backend/app/scheduler/backfill_queue.py | TASK-023, TASK-031 위임 | OK (명시) |
| backend/app/models | TASK-010, 011, 012 | OK |
| backend/app/schemas | TASK-060 (base), 061 (asset/strategy), 062 (backtest) | OK (명시) |
| frontend/* | TASK-090~094 | OK |
| docker-compose.yml | TASK-001 | OK |

→ 직전 검증의 약점 (N3, N4, N5) 모두 해결.

## 판정

**PASS**

근거: 직전 NEEDS_REVISION 7건 (HARD 2 + SOFT 5) + 사소 1건 모두 RESOLVED. architecture.md V3 모듈 분할표와 task-board.md 의 파일 경로가 1:1 일치하며 의존성 그래프 무결성 유지. 새로 발견된 이슈 없음. 병렬 안전성 확보 (TASK-040~045 가 서로 다른 파일 수정).

## Manager 에게 전달

다음 단계:
1. **TASK-001 부터 Coder 호출 시작 권고**. 위상 정렬 L0 = TASK-001 (선행 의존 없음).
2. TASK-001 완료 후 **L1 병렬** 가능: TASK-002 (DB 초기화) + TASK-060 (FastAPI 스캐폴드) — 서로 다른 파일 영역 (alembic vs FastAPI/schemas) 이므로 안전.
3. TASK-001 완료 시 description 의 4개 검증 명령 (pip install / python -c 'import app' / npm install / npm run build) 모두 성공해야 DONE 처리.
4. TASK-040~045 진행 시 architecture.md L650-665 모듈 분할표를 Coder 에게 함께 전달해 파일 경로 혼동 방지.
5. TASK-031 진행 시 의존성 주입 패턴 (data 어댑터 직접 import 금지) Reviewer 가 코드 단계에서 재검증 권고.
