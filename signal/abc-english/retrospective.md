# Retrospective — abc-english

## 프로젝트 요약
- 이름: ABC News Daily 영어 학습 시스템
- 최종 태스크 수: 37개 (TASK-001 ~ TASK-037, 모두 DONE)
- Phase 구성:
  - Phase 1~5: 파이프라인 기본 (수집 → 음성 변환 → 비교 → NLP 전처리 → LLM 분석 → ES 적재 → CLI)
  - Phase 6: 통합 테스트 + Kibana 대시보드/스케줄러
  - Phase 7: 웹 학습 UI (FastAPI + Jinja + vanilla JS, 드로어 UX, 자막 싱크, 단어/드래그 lookup, 단어장)
  - Phase 8: 배포 환경 (Docker Compose로 nginx + gunicorn)

## 잘 된 점
- 파이프라인을 **작은 단위**로 분해해 순차 완료 → 회귀 없는 누적.
- LLM 프롬프트에 "idiom이면 etymology 필수"를 규약화 → 학습 가치 상승.
- 캐시(`abc-llm-cache`)와 단어장(`abc-user-vocabulary`)을 **분리**. 캐시는 term 기반 영구, 단어장은 스냅샷 복사 + 추적 메타.
- 자막 싱크에서 `timeupdate` 매 호출 전체 순회가 아니라 **현재 index 캐시 + 인접 확인 + 이진탐색 fallback**으로 최적화.
- 오디오 Range 스트리밍을 **처음부터 명시적으로 설계** (FastAPI 기본 FileResponse의 Range 처리가 일관되지 않음을 알고 선제 대응).
- UI/UX에서 "학습 + 단어장 동시 표시"를 무작정 2컬럼으로 두지 않고 **슬라이드 드로어 + 전용 페이지 이원화**로 합의 → 몰입과 관리 기능을 모두 확보.

## 문제점
- 초기 `web/app.py` 구현 시 Starlette 신규 `TemplateResponse` 시그니처를 몰라 500 에러를 만들었고 바로 수정. 서브에이전트 작업 시작 전 해당 프레임워크의 **현 버전 API 확인 지시**가 있었다면 1회 왕복 감소.
- `gemma4:e2b` 모델명이 오타로 추정되는 상태로 확정됐다 (실제 Ollama 모델명과 불일치 가능). 서버 시작 시 `verify_ollama_model` 경고 로그로 방어했지만 **실제 모델 존재 검증 후 사용자에게 재질의**했다면 더 안전했을 것.
- 배포 구성(Phase 8)은 사용자가 학습 욕구로 추가 요청한 것. 초기 요구사항 분석에서 "로컬 사용" vs "배포 학습"을 명시적으로 물어봤다면 태스크 분해 시점에 포함 가능.

## 학습 메모 — nginx + gunicorn (배포 파이프라인)

### 왜 두 가지를 함께 쓰는가
- **gunicorn**: Python WSGI/ASGI 프로세스 매니저. 워커 N개 포크하여 멀티 프로세스로 요청 처리. 워커 죽으면 자동 재시작. 우리 프로젝트는 `-k uvicorn.workers.UvicornWorker`로 ASGI(FastAPI) 워커 사용.
- **nginx**: 리버스 프록시. TLS 종단, 정적 파일 직접 서빙(C 기반 sendfile, Python보다 수십배 빠름), 연결 버퍼링, 슬로우-클라이언트 방어, HTTP 헤더 조작, 로드밸런싱.
- **둘을 분리하는 이유**: "느린 I/O는 nginx가 받아서 버퍼링 후 gunicorn에 넘긴다" → gunicorn 워커가 느린 클라이언트에 묶이지 않음.

### 현재 구성 (TASK-037)
```
[Host:8081] ──► [nginx:80 (alpine)] ──┬── /static/ → 볼륨 직접 서빙
                                       └── /       → proxy_pass http://app:8000
                                                        [gunicorn + uvicorn workers(2)]
                                                        │
                                                        ├─ host.docker.internal:9200 (ES)
                                                        └─ host.docker.internal:11434 (Ollama)
```

### 학습 제안 (향후)
1. **HTTPS 적용**: 도메인 확보 → `certbot`으로 Let's Encrypt 인증서 발급 → nginx에 `listen 443 ssl;` + 인증서 경로 지정. `certbot renew` 자동 갱신을 cron으로.
2. **자체 서명 인증서**로 로컬에서 HTTPS 체험: `openssl req ...`로 self-signed 생성 → 브라우저 경고 무시하고 동작 확인.
3. **워커 수 튜닝**: CPU 코어 수 × 2 + 1 이 출발점. 메모리/동시 요청 수와 함께 관찰.
4. **로그 분석**: `GoAccess`로 nginx access log 시각화. slow query, 404 비율 등.
5. **VPS 배포 실전**:
   - 업체 선택 (Hetzner, Vultr, DigitalOcean 등, 월 $5~10).
   - SSH 키 등록 → `apt update && apt install docker.io docker-compose-plugin`.
   - 방화벽(ufw): 22/80/443만 개방.
   - 도메인 연결: A 레코드 → VPS IP.
   - 배포: `git clone` → `docker compose up -d --build`.
6. **무중단 배포**: `docker compose up -d --no-deps --build app` 후 gunicorn `--graceful` reload.
7. **모니터링**: Prometheus + Grafana, 혹은 간단히 `healthcheck:` 블록 + `docker events`.
8. **다른 프레임워크와 비교**:
   - Spring Boot의 내장 Tomcat이 gunicorn+uvicorn 역할을 혼자 담당.
   - nginx를 앞단에 두는 것은 Java 세계에서도 동일한 관행.
   - 차이: JVM은 프로세스 하나에 스레드 풀, Python은 GIL 때문에 프로세스 N개로 수평 확장.

### VPS란?
Virtual Private Server. 물리 서버를 가상화해 나눠 쓰는 호스팅. 사용자 입장에서는 "SSH로 접속 가능한 리눅스 머신 1대". AWS EC2의 저렴하고 단순한 버전. 월 $5 수준부터 시작.

## 파이프라인 개선 제안

### 제안 1: 외부 API/모델 검증을 서브에이전트 프롬프트에 기본 포함
- 대상 파일: `agents/coder.md`
- 현재: 외부 서비스(ollama 모델, ES 인덱스, 서드파티 SDK API) 호출 시 모델명/버전/시그니처 검증 책임이 암묵적이다.
- 제안: "외부 의존성이 있는 경우 코드 작성 전 `{도구} --version` 또는 `list` API로 존재/시그니처 확인 후 작업하라"는 항목을 명시.
- 이유: 이번 프로젝트에서 `gemma4:e2b` 모델명 오타 추정, Starlette `TemplateResponse` 신규 시그니처 미숙지 등 1회 왕복 낭비가 있었다.

### 제안 2: 초기 요구사항 분석 시 "배포 시나리오" 질문 템플릿 추가
- 대상 파일: `CLAUDE.md` 세션 재개 프로토콜 Step 1
- 현재: 기능 분해에 집중, 배포/운영 관점은 후순위로 밀림.
- 제안: "이 프로젝트는 (a) 로컬 단일 사용자 (b) 공유 서버 (c) 외부 공개 중 어디에 해당합니까?" 질문을 요구사항 수집 시 포함.
- 이유: 배포 시나리오에 따라 아키텍처 결정(인증, HTTPS, 멀티워커, DB 격리)이 달라진다.

### 제안 3: Web UI 관련 공용 골격(TASK-033 같은 것)을 표준화 (선택적)
- 대상 파일: `agents/coder.md` 또는 템플릿 디렉토리
- 현재: 매 웹 프로젝트마다 base.html / 네비 / common.js / 드로어/토스트 유틸을 처음부터 만듦.
- 제안: 공용 `web-starter/` 템플릿을 두고 새 프로젝트 시작 시 복사.
- 이유: 재사용성. 단, 프로젝트마다 스타일/레이아웃 요구가 다를 수 있어 "선택 가능한 참조"로만 유지.
