# Architecture

## 개요

웹 업무 자동화 프레임워크. 사이트별 Workflow를 공통 Core Toolkit 위에 구현한다.

### 대상 사이트
1. **티스토리** - Naver 이메일 인증번호 로그인 → 글 작성 자동화
2. **야놀자** - Cloudflare 우회 → 이메일 로그인 → 숙소 검색 → 예약 버튼 클릭 → 텔레그램 알림

### 기술 스택
- **언어**: Python 3.11+
- **브라우저 자동화**: Playwright
- **Anti-Bot**: playwright-stealth + 필요 시 capsolver API
- **설정**: YAML (사이트별 설정 분리)
- **알림**: 텔레그램 봇 (token + chat_id 설정)
- **코드 주석**: 한국어

### 스코프
- 결제 제외 (예약 직전 단계까지)
- 사용자에게 텔레그램 알림 → 사용자가 직접 결제

---

## 구조

```
projects/web-automation/
├── requirements.txt
├── config/
│   ├── settings.yaml           # 공통 설정 (텔레그램, 브라우저 옵션)
│   ├── tistory.yaml            # 티스토리 전용 설정
│   └── yanolja.yaml            # 야놀자 전용 설정
├── src/
│   ├── __init__.py
│   ├── core/                   # === Core Toolkit (공통) ===
│   │   ├── __init__.py
│   │   ├── browser.py          # Playwright 브라우저 엔진 (시작/종료/대기/스크린샷)
│   │   ├── config.py           # YAML 설정 로더
│   │   ├── telegram.py         # 텔레그램 알림 모듈
│   │   ├── logger.py           # 로깅 + 단계별 스크린샷
│   │   └── retry.py            # 재시도 + 에러 핸들링
│   ├── auth/                   # === 인증 모듈 ===
│   │   ├── __init__.py
│   │   └── naver_imap.py       # Naver IMAP 인증번호 추출
│   ├── antibot/                # === Anti-Bot 모듈 ===
│   │   ├── __init__.py
│   │   ├── stealth.py          # playwright-stealth 설정
│   │   └── cloudflare.py       # Cloudflare 우회 (자체 시도 + capsolver fallback)
│   ├── sites/                  # === 사이트별 Workflow ===
│   │   ├── __init__.py
│   │   ├── base.py             # BaseSiteWorkflow (공통 인터페이스)
│   │   ├── tistory/
│   │   │   ├── __init__.py
│   │   │   ├── login.py        # 티스토리 로그인 (이메일 인증번호 방식)
│   │   │   └── writer.py       # 글 작성 자동화
│   │   └── yanolja/
│   │       ├── __init__.py
│   │       ├── login.py        # 야놀자 로그인
│   │       ├── search.py       # 숙소 검색 (지역, 날짜, 조건)
│   │       └── booking.py      # 예약 버튼 클릭 + 알림
│   └── cli.py                  # CLI 진입점
└── tests/
    ├── __init__.py
    ├── test_browser.py
    ├── test_telegram.py
    ├── test_naver_imap.py
    ├── test_cloudflare.py
    ├── test_tistory.py
    └── test_yanolja.py
```

### 2계층 아키텍처

```
┌─────────────────────────────────────┐
│       사이트별 Workflow              │  ← 사이트마다 다른 비즈니스 흐름
│  (TistoryWorkflow, YanoljaWorkflow) │
├─────────────────────────────────────┤
│          Core Toolkit               │  ← 공통 도구 모음
│  Browser, Config, Telegram,         │
│  Logger, Screenshot, Retry          │
└─────────────────────────────────────┘
```

---

## 설계 결정

### 1. Playwright 채택 (vs Selenium)
- 결정: Playwright를 메인 브라우저 엔진으로 사용
- 이유: Selenium보다 안정적, async 지원, anti-bot 대응 유리, 자동 대기(auto-wait) 내장
- 대안: Selenium (생태계 넓지만 불안정), Puppeteer (Node.js 전용)

### 2. 추상화 범위 제한
- 결정: Core Toolkit(도구)만 공통화하고, 비즈니스 흐름(로그인/검색/예약)은 사이트별 구현
- 이유: 티스토리(이메일 인증 + 글작성)와 야놀자(Cloudflare + 숙소 예약)의 흐름이 근본적으로 다름
- 대안: 완전 추상화(비효율적, 억지 추상화)

### 3. Cloudflare 대응 전략 (**연기됨 — 2026-04-22**)
- 현재 결정: Cloudflare 우회는 capsolver 유료 API 도입 시점까지 보류
- 이유: playwright-stealth 단독으로는 Cloudflare Turnstile 통과 불가함을 사용자가 확인
- 영향:
  - TASK-010 (antibot/cloudflare.py) 제거
  - Phase 4 (야놀자 전체) BLOCKED 상태로 전환
  - Phase 3 (티스토리)는 Cloudflare 없이 동작하므로 독립 진행 가능
- 후속: capsolver 계정/키 확보 시 cloudflare.py 태스크 재등록

### 4. 결제 제외
- 결정: 1차 스코프에서 결제 기능 제외
- 이유: 실제 금전 거래 위험, PG사 보안 복잡
- 대안: 예약 버튼 클릭 후 텔레그램 알림 → 사용자가 직접 결제

### 5. 설정 분리 (Config-driven)
- 결정: 사이트별 YAML 설정 파일 분리
- 이유: 셀렉터/URL 변경 시 코드 수정 없이 설정만 수정
- 구조: settings.yaml(공통) + tistory.yaml + yanolja.yaml

---

## 현재 상태 (2026-04-22)

- Phase 1 (Core Toolkit): TASK-001~006 완료. TASK-007 (테스트) 보류.
- Phase 2 (인증 + Anti-Bot): TASK-008 (Naver IMAP) **최우선**. TASK-010 (Cloudflare) 제거.
- Phase 3 (티스토리): 최상위 우선순위 확정. IMAP 완료 후 로그인 → 글쓰기 순.
- Phase 4 (야놀자): capsolver 도입 시점까지 BLOCKED.
- Phase 6 (글쓰기 에이전트): 아래 §6 스펙 확정. 구현은 Phase 3 로그인 완료 후.

---

## 6. 티스토리 글쓰기 에이전트 (Phase 6)

### 범위
- **이 프로젝트 전용**. 다른 프로젝트나 사이트에서 재사용하지 않는다.
- 독립 에이전트로 분리. (Coder/Tester와 분리된 역할)
- 티스토리 글쓰기 워크플로우에만 호출된다.

### 입력
1. **키워드** (주제 / 포커스 단어들)
2. **작성자 초안 또는 과거 글 샘플** (어투 학습용)
3. **목적** (홍보/정보/리뷰/일기 등)
4. **참조 이미지 파일 경로 리스트** (선택)

### 산출물
- 한 편의 완성된 글 (제목 + 본문 + 태그 + 카테고리 제안)
- 본문 중간중간 이미지 배치 위치 제안 (마크다운 또는 티스토리 HTML 포맷)
- SEO 최적화 (메타 설명, 키워드 밀도, 제목 패턴)

### 안전장치
- **이미지 자동 삽입은 사용자 확인 필수**. 에이전트는 "여기에 이 이미지를 넣으면 좋겠다"만 제안, 실제 삽입 전 사용자 승인 받는다.
- 발행 전에 사용자가 최종 글 미리보기.

### 구현 위치 (예정)
- `src/writer/agent.py` — 글쓰기 에이전트 본체
- `src/writer/style.py` — 어투 학습/재현 모듈
- `src/writer/seo.py` — SEO 최적화
- `src/writer/image_placer.py` — 이미지 배치 제안
- `prompts/writer.md` — 에이전트 프롬프트 템플릿
