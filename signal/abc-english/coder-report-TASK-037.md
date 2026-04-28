---
task_id: TASK-037
title: Docker Compose 배포 환경 구축 (nginx + gunicorn, HTTP only, host 8081)
agent: coder
status: DONE
date: 2026-04-14
---

## 결과 요약

학습 목적의 HTTP-only 배포 스택을 `projects/abc-english/deploy/`에 추가했다.
구성: **nginx(리버스 프록시, 호스트 8081 → 컨테이너 80)** + **gunicorn(uvicorn worker, 컨테이너 8000)**.
기존 ES+Kibana용 `projects/abc-english/docker-compose.yml`은 건드리지 않았다.
외부에서 `http://localhost:8081`로 접속하면 nginx가 `/static/*`은 직접 서빙하고,
그 외 요청은 `app:8000`의 FastAPI로 proxy한다. 컨테이너는 `host.docker.internal`을 통해
호스트의 Elasticsearch(9200)와 Ollama(11434)에 접근한다 (Linux에서도 작동하도록
`extra_hosts: ["host.docker.internal:host-gateway"]` 지정).

`docker compose config`로 문법 검증 통과 (version 키의 deprecation warning만 발생,
기능에 영향 없음). `nginx -t`는 빈 네트워크에서 실행되어 `upstream "app"` 해석 실패 메시지가
나오지만 이는 DNS 문제이지 syntax 문제가 아니며, 실제 compose 네트워크 내부에서는 해결된다.

## 변경된 파일

### 신규
- `projects/abc-english/deploy/Dockerfile`
  - base `python:3.11-slim`, `pip install -r requirements.txt` + `gunicorn`
  - ENV `ABC_CONFIG=/app/config/settings.docker.yaml`
  - CMD `gunicorn web.app:create_app --factory -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:8000 --access-logfile - --error-logfile -`
  - EXPOSE 8000
- `projects/abc-english/deploy/docker-compose.yml`
  - `app`: build from `..` with `deploy/Dockerfile`, expose only(호스트 미노출),
    `extra_hosts` host-gateway, `../data:/app/data:ro`, `../config:/app/config:ro`, `restart: unless-stopped`.
  - `nginx`: `nginx:1.27-alpine`, `8081:80`, nginx.conf와 `../web/static` 읽기전용 바인드, `depends_on: [app]`.
- `projects/abc-english/deploy/nginx.conf`
  - `client_max_body_size 20m`, `/static/ alias ... expires 7d`,
    `/` → `proxy_pass http://app:8000`, 표준 프록시 헤더 4종,
    `proxy_http_version 1.1`, `proxy_buffering off`, `proxy_request_buffering off`,
    `proxy_read_timeout 300s` (Ollama 질의 대기).
  - access/error log를 `/dev/stdout`/`/dev/stderr`로 돌려 `docker compose logs`와 통합.
- `projects/abc-english/config/settings.docker.yaml`
  - `settings.yaml`의 **전체 복사본** + 아래 override:
    - `elasticsearch.host: host.docker.internal`
    - `llm.ollama.host: http://host.docker.internal:11434`, 동일하게 `base_url`
    - `web.host: 0.0.0.0`, `web.port: 8000` (gunicorn 실제 포트와 맞춤)
  - 파일 상단 주석에 diff 포인트를 명시하여 학습자가 `diff`로 바로 이해 가능.
- `projects/abc-english/.dockerignore`
  - `__pycache__`, `*.pyc`, `.pytest_cache`, `.git`, `data/audio`, `data/transcripts`,
    `archive`, `tests`, `.venv` 등 제외.

### 수정
- `projects/abc-english/README.md`
  - 웹 UI 실행 섹션 뒤에 **"Docker로 배포 (학습용 HTTP 배포)"** 단락 추가:
    실행 명령, 전제 조건(ES/Ollama 호스트에서 실행), `serve`와 **포트 충돌 주의사항**(둘 다 8081) 포함.

## 실행 방법

```bash
cd projects/abc-english/deploy

# 빌드 + 기동 (백그라운드)
docker compose up -d --build

# 로그 follow
docker compose logs -f

# 접속
# http://localhost:8081

# 종료
docker compose down
```

사전 조건:
- 호스트에서 Elasticsearch가 `localhost:9200`으로, Ollama가 `localhost:11434`로 실행 중.
- 개발용 `python -m src.cli serve`(기본 8081)는 반드시 **정지**해야 포트 충돌 없음.

## 이슈/블로커

없음. 실제 빌드/기동은 환경 의존이라 강제하지 않았고, compose config 문법 검증만 통과.

주의점 (블로커는 아님):
- `nginx -t`를 compose 네트워크 바깥에서 단독으로 돌리면 `upstream "app"` DNS 실패가
  뜨지만, 이는 외부 환경에서 `app`이 해석되지 않아서이며 실제 compose up 시에는 정상.
- `docker compose config`에서 `version: '3.8'` 키의 obsolete 경고가 나오지만 호환성 유지를 위해 유지.

## 다음 제안

1. **헬스체크 추가**: `app` 컨테이너에 `/api/health` 기반 healthcheck, nginx에 `depends_on.condition: service_healthy`.
2. **이미지 슬림화**: multi-stage build로 최종 이미지에서 빌드 도구 제거, spaCy 모델 사전 다운로드.
3. **HTTPS 도입**: 로컬 caddy 혹은 nginx + mkcert 사용으로 개발 HTTPS 환경 실습.
4. **데이터 쓰기 경로 분리**: 현재 `config`/`data`를 read-only로 마운트했으나, 향후 런타임
   write가 필요한 디렉토리(예: scheduler 로그)는 별도 볼륨으로 분리.
5. **non-root 유저**: Dockerfile에 `RUN useradd -m app && USER app` 추가로 보안 향상.

## 학습 포인트

### nginx와 gunicorn은 왜 둘 다 필요한가?

- **gunicorn (uvicorn worker)**: 실제 Python(ASGI) 애플리케이션을 돌리는 "앱 서버".
  FastAPI는 ASGI 앱이라 순수 uvicorn만으로도 실행 가능하지만, **프로덕션 관점의 멀티프로세스
  관리/재시작/graceful reload**는 gunicorn이 훨씬 견고하다. `-w 2`는 워커 2개로 CPU를 활용,
  `-k uvicorn.workers.UvicornWorker`는 gunicorn의 프로세스 매니저에 uvicorn의 ASGI 런타임을 얹은 것.

- **nginx**: "웹 서버" 겸 리버스 프록시. 역할이 뚜렷하다.
  1. 정적 파일(CSS/JS) 서빙은 Python 앱이 아니라 nginx가 맡는 게 훨씬 빠르고, 앱 워커 자원을
     아낀다 (`/static/` alias).
  2. 느린 클라이언트/keep-alive를 nginx가 흡수해 주어 gunicorn 워커가 블로킹되지 않는다.
  3. 외부로는 80/443만 열고 앱 포트(8000)는 **내부 네트워크에만 노출**(`expose` vs `ports`의 차이)
     → 공격 표면 축소.
  4. HTTP Range(오디오 seek), 헤더 정규화, gzip, 로그 포맷 통일 등 앱 밖에서 처리할 일이 많다.

### 왜 이렇게 구성했는가?

- **포트 8081**: 기존 `serve` 기본값과 같지만 다른 서비스(Kibana 5601 등)와의 충돌은 피함.
  하나의 호스트에 여러 스택을 돌리는 실전 감각을 위해 굳이 80 대신 8081로 지정.
- **`host.docker.internal` + `host-gateway`**: Mac/Windows만 지원하던 이 호스트명을 리눅스에서도
  쓰려면 `extra_hosts`로 `host-gateway`를 매핑해야 한다. 이렇게 하면 "호스트의 ES/Ollama를
  재빌드·재배포 없이 참조"할 수 있어 학습 환경에서 편하다 (프로덕션이라면 ES/Ollama도 컨테이너에 두고 서비스명으로 연결할 것).
- **settings.docker.yaml 분리(merge 아님)**: 학습자가 `diff settings.yaml settings.docker.yaml`
  한 줄로 "환경별로 바뀌는 값은 무엇인가"를 시각적으로 이해할 수 있게 한 의도적 단순화.
- **proxy_buffering off**: 오디오 Range 요청/스트리밍을 끊김 없이 전달하기 위함.
  일반 JSON 응답이 작으니 이 옵션을 꺼도 손해가 거의 없다.
- **데이터/설정 볼륨을 read-only로**: 배포판 이미지에 무거운 데이터(`data/audio`, `transcripts`)를
  굽지 않고 호스트에서 마운트 → 이미지 경량화 + 데이터/코드 분리 학습 목적.
