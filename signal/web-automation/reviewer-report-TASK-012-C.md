---
task_id: TASK-012-C
verdict: PASS
---

# Reviewer Report: TASK-012-C (재검증)

## 검증 대상
- 파일:
  - `signal/web-automation/task-board.md` L26 (TASK-012-C 행, Manager 패치 후)
  - `projects/web-automation/src/core/config.py`
  - `projects/web-automation/config/settings.yaml`
  - `projects/web-automation/scripts/smoke_naver_imap.sh`

- Manager 주장 요약 (6건 반영):
  1. PYTHONPATH: `.sh` 에 `PYTHONPATH="$(pwd)" python3 …` + `.py` 상단 방어적 `sys.path.insert` 병행
  2. `.env` 4필드 검증 명시
  3. headful 강제: `export WA_BROWSER_HEADLESS=false` + `_headless` override 금지 명시
  4. playwright 선행 체크: `sync_playwright().start().chromium.executable_path` 실행 → 실패 시 안내 + exit 2
  5. 종료 코드: 0/1/2 3단계 명시
  6. `async def main() -> int` + `sys.exit(asyncio.run(main()))` 명시

## 검증 결과

### 파일 존재
| 경로 | 존재 | 비고 |
|------|------|------|
| `src/core/config.py` | ✅ | `load_site` L74 실존 (재확인) |
| `config/settings.yaml` | ✅ | `headless: false` L12 실존 (재확인) |
| `scripts/smoke_naver_imap.sh` | ✅ | L39-46 2필드 검증 패턴 실존 (재확인) |
| `scripts/smoke_tistory_login.sh` | ❌ | TASK-012-C 산출물 (아직 없음 — 정상) |
| `scripts/smoke_tistory_login.py` | ❌ | TASK-012-C 산출물 (아직 없음 — 정상) |

### 6건 수정 항목 대조

**#1 PYTHONPATH — PASS**
- task-board L26 (B)① 실측: `import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1]))` — `.py` 상단 방어적 sys.path 삽입 명시.
- task-board L26 (A)⑦ 실측: `PYTHONPATH="$(pwd)" python3 scripts/smoke_tistory_login.py` — `.sh` 에서 PYTHONPATH export 명시.
- 병행 구조로 `ModuleNotFoundError: No module named 'src'` 리스크 이중 방어. 이전 보고서의 "PYTHONPATH 설정" 허위 주장 삭제 완료.

**#2 .env 4필드 검증 — PASS**
- task-board L26 (A)③ 실측: "`.env` 4필드 전부 검증: `WA_ACCOUNT_EMAIL`/`WA_ACCOUNT_PASSWORD`/`WA_NAVER_IMAP_EMAIL`/`WA_NAVER_IMAP_PASSWORD` 모두 비어있지 않은지 확인 (기존 `smoke_naver_imap.sh` L39-46 2필드 검증 패턴 확장)".
- 4필드 명시적 나열 + 확장 근거(L39-46 실측 참조) 포함. 이전 보고서 지적 100% 반영.

**#3 headful 강제 — PASS**
- task-board L26 (A)⑤ 실측: "`export WA_BROWSER_HEADLESS=false` — `settings.yaml` 은 이미 `headless: false` (L12) 이나 방어적으로 env override 로 확정. Config.get() 의 WA_ 환경변수 우선권은 `src/core/config.py:101-104` 실측 기준. `BrowserManager._headless` private override 같은 안티패턴 금지."
- 3개 실측 근거(settings.yaml L12, config.py:101-104) 명시 + 안티패턴 금지 명문화.
- 실측 재검증: `config.py:100-104` 에 `env_key = _ENV_PREFIX + key.upper().replace(".", "_"); env_value = os.environ.get(env_key); if env_value is not None: return self._cast_env_value(env_value)` — WA_ 환경변수가 YAML 보다 우선 (L106 이전에 early return). 주장 사실 일치.
- 실측 재검증: `settings.yaml:12` `headless: false                      # 헤드리스 모드 (디버깅 시 false 권장)`. 주장 사실 일치.
- 완료 조건에 `grep -E "_headless" scripts/smoke_tistory_login.py` 0건 검증이 포함 — 안티패턴 유입 차단 장치.

**#4 playwright 선행 체크 — PASS**
- task-board L26 (A)⑥ 실측: "`python3 -c "from playwright.sync_api import sync_playwright; sync_playwright().start().chromium.executable_path" 2>/dev/null` 실행해 비정상 종료 시 "playwright install chromium 을 먼저 실행하세요" echo 후 exit 2."
- import 체크 + 브라우저 바이너리 존재 체크를 한 줄에 결합. 구체적 실행 가능 명령. 이전 보고서의 모호성 해소.

**#5 종료 코드 규칙 — PASS**
- task-board L26 실측: "**종료 코드 규약**: 0=성공 / 1=로그인 실패(verify_logged_in False) / 2=예외·설정 오류".
- 3단계 코드 구분 + 각각의 의미 명시. `echo $?` 로 즉시 구분 가능.

**#6 main() 구조 — PASS**
- task-board L26 (B)③ 실측: `async def main() -> int:` 정의.
- task-board L26 (B)⑤ 실측: `if __name__ == "__main__": sys.exit(asyncio.run(main()))`.
- 반환 int → sys.exit 전달 구조 명확. Coder 가 구조 일관성 있게 구현 가능.

### 추가 검증 항목

**Config.load_site 메서드 — PASS (재확인)**
- `src/core/config.py:74` `def load_site(self, site_name: str) -> None:` 실존.
- 내부 `self._config_dir / f"{site_name}.yaml"` 를 `_load_yaml` 로 deep merge (L80-83).

**settings.yaml L12 `headless: false` — PASS (재확인)**
- `config/settings.yaml:12` `  headless: false                      # 헤드리스 모드 (디버깅 시 false 권장)` 실측 일치.

**smoke_naver_imap.sh L39-46 2필드 검증 패턴 — PASS (재확인)**
- 실측 (L39-46):
  ```bash
  if [ -z "${WA_NAVER_IMAP_EMAIL:-}" ] || [ "${WA_NAVER_IMAP_EMAIL}" = "your_naver_id@naver.com" ]; then
      echo "[ERROR] .env 의 WA_NAVER_IMAP_EMAIL 이 비어있거나 템플릿 값입니다."
      exit 1
  fi
  if [ -z "${WA_NAVER_IMAP_PASSWORD:-}" ] || [ "${WA_NAVER_IMAP_PASSWORD}" = "your_naver_app_password" ]; then
      echo "[ERROR] .env 의 WA_NAVER_IMAP_PASSWORD 이 비어있거나 템플릿 값입니다."
      exit 1
  fi
  ```
- 동일 패턴 × 2 → × 4 확장 가능. Coder 가 2필드 추가(`WA_ACCOUNT_EMAIL`, `WA_ACCOUNT_PASSWORD`)하여 자연스럽게 4필드 검증 가능. 템플릿 기본값(`your_*`)은 `.env.example` 에서 실측 확인 필요하나 bash 패턴 자체는 재사용성 확인됨.

### 태스크 완결성
- ✅ 두 파일 경로 명시 (`scripts/smoke_tistory_login.sh`, `scripts/smoke_tistory_login.py`).
- ✅ 완료 조건 측정 가능:
  - `bash -n scripts/smoke_tistory_login.sh` 문법 체크
  - `python3 -m py_compile scripts/smoke_tistory_login.py`
  - `grep -E "_headless" scripts/smoke_tistory_login.py` 0건 (안티패턴 차단)
  - 4필드 검증 블록 grep 실증
- ✅ sys.path / PYTHONPATH 이중 방어로 런타임 `ModuleNotFoundError` 리스크 해소.
- ✅ headful 강제 방식 단일화 (`WA_BROWSER_HEADLESS=false` env + private override 금지).
- ✅ playwright 체크 구체 명령 명시.
- ✅ 4필드 검증 규칙 명시.
- ✅ 종료 코드 3단계 + main 구조 모두 명시.

### 의존성·순서
- ✅ TASK-012-A, TASK-012-B DONE (task-board L24, L25 재확인).
- ✅ TASK-012-ENV 는 Execution: user 이므로 Coder 실행 무관.
- ✅ 병렬 후보 아님.

### 목적성 · 클린 아키텍처 · 분리 원칙
- ✅ **목적성**: "티스토리 로그인 자동화"에 봉사하는 스모크 러너.
- ✅ **계층 의존 방향**: `scripts/` → `src.*` 정방향.
- ✅ **이름 · 인터페이스**: `smoke_tistory_login.{sh,py}` — `smoke_naver_imap.*` 와 일관.
- ✅ **추후 수정 용이성**: private 속성 override 금지 → 환경변수 표준 준수로 프로젝트 전반의 나쁜 선례 유입 차단.
- ✅ **소스 · 함수 분리**: `main() -> int` 단일 함수로 스모크 러너 단일 관심사 유지. (출력 포맷팅 분리는 선택 품질 향상 — 이번 태스크에서 필수 아님.)

## 판정
**PASS**

이전 6건 수정 요청 모두 task-board L26 에 반영 완료. 추가 검증 항목 3건(config.py:74, settings.yaml:12, smoke_naver_imap.sh L39-46) 모두 실측으로 주장과 일치 확인. Coder 가 외부 질문 없이 실행 가능한 수준으로 Coder 호출 준비 완료.

## Manager에게 전달

TASK-012-C 를 IN_PROGRESS 로 전환하고 Coder 호출 가능. 주의:
- Coder 에게 완료 조건의 4가지 grep/compile 체크를 반드시 실행하도록 지시.
- Coder report 수신 후 DONE 처리 전에 `grep -E "_headless" scripts/smoke_tistory_login.py` 가 실제 0건인지 Manager 가 재확인 권장(안티패턴 유입 최종 방어선).
