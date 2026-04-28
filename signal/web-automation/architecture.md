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

---

## 7. 폴더 기반 임시저장 자동화 (Phase 7)

### 목적
사용자가 지정된 폴더(`posts/{YYYY-MM-DD}-{slug}/`) 에 마크다운 글과 이미지를 넣어두면, 자동으로 티스토리에 임시저장(`/manage/drafts`) 한다. 사용자는 관리자 페이지에서 draft 를 열어 확인하고 직접 '완료'(발행) 한다.

### 계층 구분 (중요)
- Phase 3 `src/sites/tistory/writer.py` 는 **UI 기반** (Playwright 가 TinyMCE 에디터에 직접 타이핑/클릭). 단일 글 수동 조작에 적합.
- Phase 7 `src/tistory_post/*` 는 **API 기반** (page.evaluate + fetch 로 `/manage/post/attach.json` + `/manage/drafts` 직접 호출). 대량/반복 자동화에 적합하며 이미지 중간 위치 배치가 자유로움.
- 두 계층은 **같은 BrowserManager 세션**을 공유 (로그인 1회 → 양쪽 사용).

### 입력 규격
```
posts/2026-04-22-hello-world/
├── post.md              # YAML frontmatter + 본문 (with ${N}/${filename} 마커)
├── imgs/                # 이미지 전용 서브폴더 (권장). 있으면 loader 는 여기만 읽는다.
│   ├── 1.png            # ${1} 로 참조 (imgs/ 내 사전순 1번째)
│   ├── 2.png
│   └── hero.jpg         # ${hero.jpg} 로 파일명 직접 참조
├── .draft_id            # runtime: tistory draftSequence 저장 (재실행 시 업데이트)
├── .published           # runtime: 완료 마커 (존재하면 skip)
├── .orphan.log          # runtime: 업로드 실패로 남은 orphan 이미지 JSONL
└── .error               # runtime: 최근 실패 traceback + phase JSON
```

**이미지 수집 규칙**: `{folder}/imgs/` 가 존재하면 **그 안의 이미지만**, 없으면 `{folder}/` 바로 아래 (하위 호환).

**post.md 포맷** (YAML frontmatter + markdown body):
```markdown
---
title: "제목"
category: "메모"              # tistory 카테고리명 (실측 존재해야)
tags: ["태그1", "태그2"]
---

본문 첫 문단. 이미지는 ${1}

다음 사진: ${hero.jpg}
```

### 마커 파싱 규칙
- `${N}` (양의 정수, 1-based) → 폴더 내 이미지 사전순 N번째.
- `${filename.ext}` → 해당 이름 파일.
- `${}` / `${0}` / 음수 / 부재 파일 → ValueError.
- 동일 마커 중복 허용 (같은 이미지 재사용).
- 고아 이미지 (마커 미참조) 허용 (warning 로그).

### 핵심 결정
- **이미지 먼저 업로드** → 매크로 수집 → 본문 마커 치환 → draft 생성 순 (atomic).
- **멱등성**: `.draft_id` 저장 후 재실행 시 `draftSequence` 로 덮어쓰기 (API 지원 실측 — probe §2).
- **이미지 삭제 API 부재** 확정 (probe §3). 실패 시 orphan 은 `.orphan.log` 기록 + 사용자 수동 정리.
- `&` → `&amp;` HTML escape 는 UploadedImage.macro 조립 시점 (image_uploader) 에서 완료.

### 구현 위치
- `src/tistory_post/models.py` — 공통 dataclass (LoadedPost, Marker, UploadedImage, DraftPayload, RunResult, PartialUploadError)
- `src/tistory_post/post_loader.py` — 폴더 파싱 (frontmatter + body + 마커 매핑)
- `src/tistory_post/image_uploader.py` — `/manage/post/attach.json` 직접 호출 + 매크로 조립
- `src/tistory_post/category_fetcher.py` — `#category-list` DOM 에서 name↔id 맵 추출
- `src/tistory_post/post_builder.py` — 마커 치환 + markdown→HTML + DraftPayload 조립
- `src/tistory_post/post_saver.py` — `/manage/drafts` 직접 호출
- `src/tistory_post/post_runner.py` — end-to-end orchestration + 에러 롤백 + 마커 파일 관리
- `scripts/smoke_tistory_post.sh` / `.py` — E2E 스모크 러너
- `posts/{YYYY-MM-DD}-{slug}/` — 사용자 입력 폴더 (git-ignore 권장)

### 의존성
- `Pillow>=10.0.0` — 이미지 width/height 추출 + 샘플 PNG 생성.
- `markdown>=3.5` — 마크다운 → HTML 변환 (extensions=[extra, nl2br]).
