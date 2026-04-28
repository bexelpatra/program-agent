---
agent: coder
task_id: TASK-012-C
status: DONE
timestamp: 2026-04-22T10:37:00+09:00
---

## 결과 요약

티스토리 카카오 로그인 스모크 러너를 bash wrapper + python 엔트리 2파일로 신규 작성했다.
`smoke_naver_imap.sh` 의 .env 로드/필드 검증 패턴을 재사용하되 카카오 2필드 + 네이버 IMAP 2필드 (총 4필드)로 확장했고,
playwright chromium 바이너리 선행 체크와 `WA_BROWSER_HEADLESS=false` env override 로 headful 강제를 추가했다.
`BrowserManager._headless` private 속성 직접 수정 안티패턴은 쓰지 않고 공식 `Config.get` 의 WA_ 환경변수 우선권만 사용했다.

## 변경된 파일

- `projects/web-automation/scripts/smoke_tistory_login.sh` (신규, 권한 755)
- `projects/web-automation/scripts/smoke_tistory_login.py` (신규)

## DoD 7건 검증 결과

### DoD 1. 두 파일 신규 생성 + bash 실행 권한 755

명령:
```
ls -l projects/web-automation/scripts/smoke_tistory_login.{sh,py}
```
결과:
```
-rw-rw-r-- 1 jai jai 2628  4월 22 10:36 .../smoke_tistory_login.py
-rwxr-xr-x 1 jai jai 3488  4월 22 10:36 .../smoke_tistory_login.sh
```
→ bash wrapper `rwxr-xr-x` = 755 확인. python 엔트리는 바이너리가 아니라 `python3` 으로 실행하므로 x 비트 불필요.

### DoD 2. `bash -n` 문법 체크 통과

명령:
```
bash -n projects/web-automation/scripts/smoke_tistory_login.sh
```
결과: exit code 0, 출력 없음 (echo "OK: bash -n passed" 이어서 찍힘). → PASS.

### DoD 3. `python3 -m py_compile` 통과

명령:
```
python3 -m py_compile projects/web-automation/scripts/smoke_tistory_login.py
```
결과: exit code 0, 출력 없음 (echo "OK: py_compile passed" 이어서 찍힘). → PASS.

### DoD 4. `grep -E "_headless" scripts/smoke_tistory_login.py` 0건

명령:
```
grep -E "_headless" projects/web-automation/scripts/smoke_tistory_login.py
```
결과: 매치 없음, grep exit code 1. 검증 스크립트의 `|| echo "OK: no _headless ..."` 분기 진입 확인. → PASS (private 속성 우회 안티패턴 없음).

### DoD 5. bash wrapper 4필드 검증 grep 최소 4 hit

명령:
```
grep -cE "WA_ACCOUNT_EMAIL|WA_ACCOUNT_PASSWORD|WA_NAVER_IMAP_EMAIL|WA_NAVER_IMAP_PASSWORD" \
  projects/web-automation/scripts/smoke_tistory_login.sh
```
결과: `10` (주석 문서화 + `missing_fields` 검증 배열 4줄 + 명시 export 4줄 = 10 hit). 최소 4 hit 요구 대비 충분. → PASS.

### DoD 6. `WA_BROWSER_HEADLESS=false` export grep 1 hit

명령:
```
grep -n "WA_BROWSER_HEADLESS=false" projects/web-automation/scripts/smoke_tistory_login.sh
```
결과:
```
70:export WA_BROWSER_HEADLESS=false
71:echo "[스모크] headful 강제: WA_BROWSER_HEADLESS=false"
```
L70 에 export 존재. L71 은 echo 로그 라인이며 동일 키워드를 포함. 요구 "1 hit 이상" 충족. → PASS.

### DoD 7. playwright chromium 선행 체크 블록 존재

명령:
```
grep -n "playwright install chromium" projects/web-automation/scripts/smoke_tistory_login.sh
```
결과:
```
12:#   3. playwright chromium 바이너리 설치: `playwright install chromium`
77:    echo "                먼저 실행하세요: playwright install chromium"
```
L77 에 설치 안내 echo 존재 (L73-79 블록: `python3 -c "... sync_playwright().start().chromium.executable_path"` 선행 체크 → 실패 시 `exit 2`). → PASS.

## 구현 세부 (참고)

### bash wrapper (`smoke_tistory_login.sh`)

주요 단계:
1. `set -euo pipefail` + `SCRIPT_DIR`/`PROJECT_ROOT` 계산 후 `cd "$PROJECT_ROOT"`.
2. `.env` 존재 확인 → 없으면 안내 후 `exit 1`.
3. `set -a; source .env; set +a` 로 .env 자동 export (기존 `smoke_naver_imap.sh` L33-36 패턴 재사용).
4. `missing_fields` 배열로 4개 키 각각 `-z` 검증 → 누락된 필드명을 목록 출력 후 `exit 1`.
5. 명시 `export` (가독성용 — `set -a` 로 이미 export 되어 있음).
6. `export WA_BROWSER_HEADLESS=false` 로 headful 강제. `Config.get` 의 WA_ 환경변수 우선권 (`src/core/config.py:101-104`) 덕분에 `settings.yaml:12 headless: false` 값을 런타임에 명시적으로 override.
7. playwright chromium 바이너리 선행 체크: `python3 -c "from playwright.sync_api import sync_playwright; sync_playwright().start().chromium.executable_path"` 실패 시 `exit 2`.
8. `PYTHONPATH="$(pwd)" python3 scripts/smoke_tistory_login.py` 실행 → 종료 코드 그대로 전파 (`set -e` + 마지막 명령).

### python 엔트리 (`smoke_tistory_login.py`)

- 파일 상단 docstring 에 종료 코드 규약(0/1/2) 명시.
- `sys.path.insert(0, str(Path(__file__).resolve().parents[1]))` 를 src.* import 앞에 배치, 모든 import 라인에 `# noqa: E402`.
- `Config()` → `config.load_site("tistory")` (실측: `config.py:74` 시그니처).
- `async with BrowserManager(config) as browser:` 컨텍스트 내부에서 `TistoryKakaoLogin(config, browser).run()` 호출.
- 예외 분기 2개: Config 로드 실패 / BrowserManager·run 내부 예외 — 둘 다 `return 2` + `logger.exception` + stderr 안내.
- 성공: `return 0`, 로그인 실패: `return 1`.
- 비밀번호/인증번호 출력 없음 (stdout/stderr 에 계정 관련 원문 일절 미노출).

## 이슈/블로커

없음.

## 다음 제안

- TASK-012-D (user 실행): `cp .env.example .env` → 카카오 2필드 + 네이버 IMAP 2필드 입력 → `./scripts/smoke_tistory_login.sh` 실행. 단계별 스크린샷은 `projects/web-automation/screenshots/tistory_login_*.png` 로 저장된다. 실패 시 셀렉터·fallback 키워드 교정 태스크 등록 필요.
- Playwright headful 환경은 GUI 세션이 필요하다 (WSL/원격 SSH 에서는 `DISPLAY` 또는 X 포워딩 설정 선행). 사용자에게 실행 환경 사전 안내가 유용할 것.
