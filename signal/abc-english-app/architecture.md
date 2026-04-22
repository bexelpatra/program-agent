# Architecture: abc-english-app

## 개요

`abc-english` 프로젝트의 웹 UI(FastAPI + 서버 렌더링 + 바닐라 JS)를 **모바일 앱(Flutter)** 으로 이식하는 프로젝트. 백엔드는 기존 FastAPI 서버를 재사용하되, 앱 전용 `/api/v1/` 엔드포인트를 신규 추가한다.

### 목적
- ABC News Daily 에피소드를 모바일에서 청취하며 학습
- 백그라운드 재생 (화면 꺼짐·다른 앱 전환 중에도 재생 지속)
- 오프라인 재생 (에피소드 선택 다운로드 후 네트워크 없이 청취)
- 재생 중 스크립트 동기화 표시 + 토글
- 단어장(notebook) CRUD, 온라인 복귀 시 사전 의미 자동 채움

### 범위 (MVP v0.1)
- Android 주력 (iOS는 v0.2 이후)
- 에피소드 목록 / 상세 / 재생 / 스크립트 동기화 / 단어장 / 오프라인 다운로드
- 제외 (v0.2+): LLM 어휘 분석 표시, CEFR 레벨 필터, 푸시 알림, 백그라운드 다운로드, 태블릿 2pane 레이아웃 분기(기본 단일 pane으로 먼저)

### 비범위 (영구 제외)
- 웹 UI 대체: 웹은 그대로 유지. 앱은 별도 클라이언트.
- 크롤러/분석기: 모두 기존 abc-english 서버에서 동작.

---

## 기술 스택

| 영역 | 기술 | 이유 |
|------|------|------|
| 프레임워크 | Flutter (stable channel) | 백그라운드 오디오 성숙도(just_audio_background), 단일 코드베이스 Android 우선 + iOS 이식 가능 |
| 언어 | Dart 3.x | Flutter 표준 |
| 상태관리 | Riverpod 2.x | 테스트 용이, 코드 제너레이션 최소화, AsyncValue로 네트워크 상태 표현 |
| 라우팅 | go_router 14.x | 선언형, 딥링크 대비 |
| 오디오 | just_audio + just_audio_background | 백그라운드 재생, Android MediaSession, 락스크린 컨트롤 |
| HTTP | dio 5.x | 인터셉터(Bearer 자동 첨부), 캐시, 재시도 |
| 로컬 DB | drift (SQLite) | 타입 세이프, 마이그레이션 지원, stream 기반 반응형 쿼리 |
| 파일 저장 | path_provider + 내부 앱 디렉토리 | MP3 오프라인 캐시 |
| 직렬화 | freezed + json_serializable | 불변 모델, Union type, toJson/fromJson 자동 |
| 테스트 | flutter_test + mocktail + integration_test | 단위/위젯/통합 3단 |
| 빌드 | Android Gradle + Flutter build apk | 추후 aab(Play Store) 대비 |
| 로깅 | logger 2.x | 레벨별 출력, 릴리스 빌드에서 자동 축소 |

### 빌드 타겟
- Android minSdk 21 (Android 5.0+), targetSdk 34 → 향후 36
- iOS는 MVP 제외

---

## 백엔드 연동 전략

### `/api/v1/` 프리픽스 신설
- 기존 웹은 `/api/*` 그대로 유지 (웹 UI 호환성 유지)
- 앱은 **신규** `/api/v1/*` 를 호출
- `web/api/v1/` 디렉토리 신설 (FastAPI APIRouter 분리)
- v1은 "앱에 필요한 최소 계약"만 제공. 웹 전용 엔드포인트(렌더링용)는 v1에 포함하지 않음.

### v1 엔드포인트 (초안)
| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/v1/episodes` | 에피소드 목록 (page, size, since_modified) |
| GET | `/api/v1/episodes/{id}` | 에피소드 상세 + 문장 리스트 (타임스탬프 포함) |
| GET | `/api/v1/episodes/{id}/audio` | MP3 스트리밍 (HTTP Range 지원, 기존 audio API 재사용) |
| GET | `/api/v1/episodes/{id}/manifest` | 오프라인 다운로드에 필요한 파일 목록·체크섬 |
| GET | `/api/v1/lookup` | 단어 사전 조회 (term 쿼리) |
| GET | `/api/v1/notebook` | 단어장 목록 (since_modified 증분 sync) |
| POST | `/api/v1/notebook` | 단어 추가 |
| PATCH | `/api/v1/notebook/{id}` | 단어 수정 (last_modified 포함 → LWW) |
| DELETE | `/api/v1/notebook/{id}` | 단어 삭제 (soft delete, deleted_at) |
| POST | `/api/v1/notebook/sync` | 오프라인 중 쌓인 변경 배치 업로드 |

### 인증
- **Static Bearer Token** (`ABC_API_TOKEN`): 환경변수로 서버에 배포, 앱 빌드 시 `--dart-define=ABC_API_TOKEN=...` 주입.
- MVP에서는 단일 토큰. 다중 사용자 지원 시 JWT로 마이그레이션.
- FastAPI 측: `/api/v1/*` 에만 의존성(Depends)으로 Bearer 검증. `/api/*`(웹 레거시)는 영향 없음.

### 네트워크 계층
- 현재: WireGuard VPN으로 집 PC → 외부에서 접근
- 향후: AWS 배포, Ollama → 저렴한 LLM API (Claude Haiku 후보) + 사용량 제한

### 환경 설정 (dev/staging/prod 분기)
- 앱 실행 시 `--dart-define` 으로 런타임 환경 주입:
  - `ABC_API_BASE_URL` (예: `http://10.0.0.5:8000` dev, `https://abc.example.com` prod)
  - `ABC_API_TOKEN` (Static Bearer Token)
  - `ABC_ENV` (`dev` | `staging` | `prod`)
- `lib/core/config/app_config.dart` 에서 `String.fromEnvironment` 로 읽어 싱글턴으로 보관
- 환경별 기본값은 코드에 하드코딩하지 않고 `--dart-define` 없으면 assert 실패
- 로컬 개발 편의: `scripts/run_dev.sh` 에 기본 dev 값 포함

### 웹 레퍼런스 경로 (App Porter용)
- `WEB_REFERENCE_ROOT`: `projects/abc-english/web/`
  - HTML 템플릿: `web/templates/*.html`
  - 정적 에셋(CSS/JS): `web/static/`
  - 라우트 핸들러: `web/routes/pages.py` (어떤 템플릿이 어떤 페이지에 매핑되는지 확인)
  - API 계약: `web/api/*.py` (앱이 호출할 엔드포인트 참고용. 앱은 `/api/v1/*` 사용하지만 기존 `/api/*` 시그니처 참고 가능)

---

## 오프라인 전략

### 저장 대상
| 종류 | 용량 | 캐시 정책 |
|------|------|-----------|
| 에피소드 메타데이터 | ~수 KB/건 | 전부 로컬 (drift 테이블) |
| 문장·타임스탬프 | ~수십 KB/건 | 전부 로컬 |
| MP3 오디오 | ~15MB/건 | **선택 다운로드** (전체 ~250개 = 3.75GB 일괄 금지) |
| 단어장 | ~수 KB/건 | 전부 로컬, 서버와 양방향 동기화 |
| 사전 조회 결과 | ~수 KB/건 | 조회한 것만 캐시, TTL 없음 (안정적 데이터) |

### 동기화 방식
- **Last-Write-Wins** + `last_modified` timestamp
- 오프라인 중 쓴 변경은 로컬에 `pending_sync=true` 플래그로 저장
- 온라인 복귀 감지 (connectivity_plus) → `/api/v1/notebook/sync` 배치 업로드
- 서버 응답으로 최신 last_modified 수신 → 로컬 갱신

### 오프라인 사전 조회 정책
- **오프라인 중**: 사용자 요청 → 로컬 DB 검색 → 없으면 "나중에 채움" 플래그로 단어장에 저장 (한국어 뜻 = null)
- **온라인 복귀**: null 뜻이 있는 단어를 배치 조회 → 업데이트

---

## 앱 아키텍처 (Clean Architecture + Feature Slicing)

```
projects/abc-english-app/
├── android/                 # Android 플랫폼 설정
├── ios/                     # (v0.2 이후)
├── lib/
│   ├── main.dart            # 엔트리, DI 루트
│   ├── app.dart             # MaterialApp, 라우팅, 테마
│   ├── core/                # 프로젝트 전역 공용
│   │   ├── network/         # Dio 클라이언트, 인터셉터
│   │   ├── storage/         # drift DB 정의, 마이그레이션
│   │   ├── audio/           # just_audio 서비스
│   │   ├── sync/            # 동기화 엔진
│   │   └── theme/           # Material 테마, 색상/폰트
│   ├── features/
│   │   ├── episode_list/
│   │   │   ├── data/        # Repository 구현, DTO, datasource
│   │   │   ├── domain/      # Entity, UseCase
│   │   │   └── presentation/ # Screen, Widget, Riverpod Provider
│   │   ├── episode_detail/
│   │   ├── player/          # 플레이어 + 스크립트 동기화 (핵심 feature)
│   │   ├── notebook/        # 단어장
│   │   └── settings/
│   └── shared/              # features 간 공용 위젯/유틸
├── test/                    # 단위/위젯 테스트
├── integration_test/        # 통합 테스트
├── scripts/
│   └── setup.sh             # Flutter+Android SDK 설치 (이미 존재)
├── pubspec.yaml
└── README.md
```

### 레이어 규칙
- `presentation` → `domain` 만 의존 (Widget은 UseCase를 통해 데이터 접근)
- `data` → `domain` 구현 (Repository 인터페이스는 domain에 정의)
- `core/`는 features 의존 금지 (반대는 허용)
- features 간 직접 의존 금지. 필요 시 `shared/` 를 거쳐 사용.

### 오류 전파 정책
- **data 계층**: 외부 원인(HTTP, DB, IO)으로 발생한 raw 예외를 잡아 `core/errors/app_exception.dart` 의 도메인 전용 예외로 변환해 throw.
  - 예: `NetworkException`, `NotFoundException`, `UnauthorizedException`, `StorageException`, `SyncConflictException`
- **domain 계층**: UseCase 는 **`Result<T, AppException>`** 를 반환한다 (sealed class: `Success<T>` / `Failure<AppException>`).
  - try/catch 를 UseCase 내부에 두고, data 예외 → Result.Failure 로 포장.
  - UseCase 는 절대 예외를 throw 하지 않는다.
- **presentation 계층**: `AsyncValue<Result<T, AppException>>` 를 Riverpod Provider 로 노출.
  - Widget 은 `when(data: (r) => r.when(success: ..., failure: ...), loading: ..., error: ...)` 패턴으로 표시.
  - 네트워크 오류는 SnackBar, 인증 오류는 로그인 가이드 화면, 예상 외는 ErrorBoundary.

### 로깅 전략
- `core/logging/app_logger.dart` 에 싱글턴 logger (패키지: `logger`).
- 레벨: `debug` / `info` / `warning` / `error`.
- **릴리스 빌드** (`kReleaseMode`): `warning` 이상만 출력.
- **디버그 빌드**: 전체 출력.
- 민감 정보(`ABC_API_TOKEN`, 사용자 입력 원문) 로깅 금지 — 토큰은 길이만(`token_len=32`) 기록.
- 구조화: 각 로그는 `{feature, action, context}` 형태. 예: `log.info('notebook.add', context: {'term': term})` (`term` 은 괜찮지만 뜻/해석처럼 덩어리 큰 건 제외).

### 빌드 환경변수 주입
- `flutter run --dart-define=ABC_API_BASE_URL=... --dart-define=ABC_API_TOKEN=... --dart-define=ABC_ENV=dev`
- `flutter build apk --dart-define=...`
- CI/CD 에서는 secrets 로 주입 (향후 과제)
- 로컬 편의 스크립트:
  ```bash
  # scripts/run_dev.sh
  flutter run \
    --dart-define=ABC_API_BASE_URL=$ABC_API_BASE_URL \
    --dart-define=ABC_API_TOKEN=$ABC_API_TOKEN \
    --dart-define=ABC_ENV=dev
  ```
- `.env` 파일 같은 패키지(`flutter_dotenv`) 는 사용하지 않음 — 런타임 로드는 빌드타임 주입보다 유출 위험↑.

---

## 핵심 feature 상세: `player`

웹 UI에서 가장 복잡하고 이식이 까다로운 부분. App Porter의 주요 대상.

### 요구사항
- 재생/일시정지/빨리감기(+15s)/되감기(-15s)
- 재생 속도 조절 (0.75x / 1.0x / 1.25x / 1.5x)
- 시크바 (탐색)
- **스크립트 동기화 표시**: 현재 재생 시점의 문장을 자동 하이라이트 + 가운데 스크롤
- **스크립트 토글**: 전체 스크립트 보기/숨기기
- 문장 탭 → 해당 타임스탬프로 점프
- 단어 롱프레스 → 사전 조회 + 단어장 추가 모달
- 백그라운드 재생 (화면 꺼짐 중에도 재생 지속)
- 락스크린/알림창 컨트롤 (just_audio_background)

### 상태관리
- Riverpod `StreamProvider` 로 just_audio의 `positionStream` 구독
- 현재 position → 문장 index 계산 (binary search on timestamps)
- 현재 문장 index가 변하면 ScrollController.scrollTo 호출

### 위젯 분해
```
PlayerScreen (Scaffold)
├── AppBar (뒤로 가기, 에피소드 제목)
├── Body
│   ├── AlbumArt (에피소드 썸네일, 상단 1/3)
│   ├── ProgressBar (시크바 + 시간 표시)
│   ├── ControlBar (재생/빨리감기/되감기/속도)
│   ├── ScriptToggle (아이콘 버튼)
│   └── ScriptList (Expanded, 스크립트 보기 시)
│       └── SentenceTile × N (하이라이트, 탭, 단어 롱프레스)
└── BottomBar (단어장 바로가기, etc.)
```

---

## 설계 결정

### Flutter 선택 (RN 대비)
- **결정**: Flutter
- **이유**:
  1. `just_audio_background` 가 `react-native-track-player` 보다 Android 백그라운드 재생 안정성 우수
  2. 단일 언어(Dart)로 전 계층 작성 → 포팅 속도
  3. 모바일 UI 컴포넌트(Material/Cupertino) 기본 제공
- **대안**: React Native — 웹 개발자와 JS 생태계 공유의 이점은 있으나, 오디오 백그라운드 이슈가 반복 보고됨

### Clean Architecture + Feature Slicing
- **결정**: `core/` + `features/{f}/{data,domain,presentation}/`
- **이유**: feature 단위 테스트 격리, feature 추가/삭제 시 파일 이동 최소화
- **대안**: MVVM 단일 계층 → 초기는 빨라도 기능 추가 시 파일 혼잡

### 오프라인 선택 다운로드 (전체 다운로드 금지)
- **결정**: 사용자가 에피소드 리스트에서 "다운로드" 버튼 누를 때만 MP3 저장
- **이유**: 250 × 15MB = 3.75GB. 대부분 사용자 스토리지에 부담.
- **대안**: 전체 다운로드 with 설정 토글 → 기본값 off. v0.2 이후 검토.

### Static Bearer Token (JWT 아님)
- **결정**: 환경변수 기반 단일 토큰, 빌드 시 주입
- **이유**: MVP는 개인용(본인 1명). JWT 인증 플로우 UI 불필요.
- **대안**: 공개 배포 시 이메일+OTP 기반 JWT로 전환. 스키마는 v2에서.

### Last-Write-Wins (서버 타임스탬프 기준)
- **결정**: 클라이언트·서버 양쪽 `last_modified` 비교, 큰 쪽 채택
- **이유**: 단어장은 충돌 시 손실 감수 가능한 영역. 3-way merge 복잡도 대비 가치 낮음.
- **대안**: CRDT — 오버엔지니어링.

### 오프라인 사전 조회 "나중에 채움" 패턴
- **결정**: 오프라인 중 단어 저장 시 뜻 null, 온라인 복귀 시 배치 조회
- **이유**: 오프라인 사전 DB 동봉 금지 (앱 용량·라이선스). 단어장은 core 기능이라 오프라인에도 저장 가능해야 함.
- **대안**: 오프라인 불가 에러 표시 — UX 저하.

---

## 배포 전략

### Android APK 배포 (MVP)
- GitHub Release에 APK 업로드 → 사용자가 직접 설치 (개인용)
- 서명: debug keystore (MVP) → v0.2부터 release keystore

### 버전 관리
- Semver: `MAJOR.MINOR.PATCH+BUILD` (예: `0.1.0+1`)
- 빌드 번호는 CI 자동 증가 (후속 과제)

### API 버전 호환성
- `/api/v1/*` 로 고정
- 앱은 앱 버전 헤더(`X-App-Version`)를 항상 전송
- 서버가 구 버전 차단 필요 시 403 반환

---

## 에이전트 역할 분담 (이 프로젝트 한정)

| 에이전트 | 주 담당 |
|---------|---------|
| Manager (PM) | 태스크 분해, 에이전트 조율, Reviewer 게이팅, 완료 판정 |
| Coder | `core/` (네트워크, 저장소, 오디오, 동기화), `features/*/data/` `features/*/domain/` 구현, 백엔드 `/api/v1/` 추가 |
| App Porter | `features/*/presentation/` (화면, 위젯), 웹 UI 레퍼런스 → 모바일 UX 매핑, 스크립트 동기화 등 핵심 상호작용 |
| Tester | 단위·위젯·통합 테스트 작성·실행, 실기기 스모크 태스크 정의(Execution=user) |
| Reviewer | Manager 산출물 검증 (task 설명의 웹 레퍼런스 경로가 실제 있는지, 타임스탬프 계산 로직 설명이 맞는지 등) |

---

## 현재 상태
- 2026-04-22: 아키텍처 초안 작성. Flutter 설치 스크립트(scripts/setup.sh) 선제 적용 완료.
- 다음 단계: App Porter 프롬프트 작성 → 태스크 분해 → Phase 0 (프로젝트 초기화) 착수
