---
agent: coder
task_id: TASK-008-FIX
status: DONE
timestamp: 2026-04-22T10:15:00
---

## 결과 요약
사용자 실계정 스모크 결과 반영: 카카오 인증번호가 8자리(실측 `55898679`)이고, 티스토리 로그인 주체가 카카오 계정(네이버는 IMAP 수신 전용)임을 반영해 정규식·Config 키·env 템플릿·스모크 스크립트·테스트를 일괄 정정했다. 기존 5개 테스트 + 신규 8자리 매치 테스트 총 6개 모두 통과.

## 변경된 파일
- projects/web-automation/src/auth/naver_imap.py (수정)
- projects/web-automation/config/tistory.yaml (수정)
- projects/web-automation/.env.example (수정)
- projects/web-automation/scripts/smoke_naver_imap.sh (수정)
- projects/web-automation/tests/test_naver_imap.py (수정: Manager 지시에 의한 예외적 Coder 수정)

## 공개 API

### `src.auth.naver_imap.fetch_verification_code`

시그니처 자체는 변경되지 않았지만 아래 두 가지 계약(Contract)이 바뀌었으므로 호출측에서 주의해야 한다.

1. 기본 정규식 (`code_pattern` 파라미터 default)
   - 이전: `r"\b\d{6}\b"` (정확히 6자리)
   - 변경: `r"\b\d{6,8}\b"` (6~8자리). 카카오 8자리 인증번호(실측 `55898679`) 매치 지원.
   - 호출자가 `code_pattern=`을 명시적으로 전달하면 이전 동작을 유지할 수 있다.

2. Config 키 (IMAP 접속 자격 증명)
   - 이전: `account.email`, `account.password` (네이버 계정 용도로 혼동 사용됨)
   - 변경: `naver_imap.email`, `naver_imap.password`
   - `account.*` 키는 이제 "카카오 계정(티스토리 로그인용)"으로 의미가 재정의됨 → `fetch_verification_code`는 더 이상 `account.*`를 읽지 않는다.
   - ValueError 메시지도 `naver_imap.email` / `naver_imap.password` 기준으로 갱신.

### Config / 환경변수 매핑 (변경 후)

| YAML 키                | 환경변수 오버라이드                | 용도                                 |
|------------------------|-----------------------------------|--------------------------------------|
| `account.email`        | `WA_ACCOUNT_EMAIL`                | 카카오 계정 ID (티스토리 로그인용)   |
| `account.password`     | `WA_ACCOUNT_PASSWORD`             | 카카오 계정 비밀번호                 |
| `naver_imap.email`     | `WA_NAVER_IMAP_EMAIL` (신규)      | 네이버 IMAP 로그인 이메일            |
| `naver_imap.password`  | `WA_NAVER_IMAP_PASSWORD` (신규)   | 네이버 IMAP 앱 비밀번호              |
| `naver_imap.server`    | (기존 유지)                        | `imap.naver.com`                     |
| `naver_imap.port`      | (기존 유지)                        | 993                                  |

### 스모크 스크립트 (`scripts/smoke_naver_imap.sh`)
- 필수 env 변수 검증 대상: `WA_ACCOUNT_EMAIL` / `WA_ACCOUNT_PASSWORD` → `WA_NAVER_IMAP_EMAIL` / `WA_NAVER_IMAP_PASSWORD`.
- 기본 sender 인자: `@tistory.com` → `noreply@kakaocorp.com`.
- 진행 로그 "6자리 인증번호" → "6~8자리 인증번호", 정보 출력 "Naver 계정:" → "Naver IMAP 계정:".

## 검증 결과
- `cd projects/web-automation && python3 -m unittest tests.test_naver_imap -v` → **Ran 6 tests, OK (0 failures, 0 errors)**.
  - 신규 `test_extracts_eight_digit_kakao_code` 통과 (본문 `55898679` → `"55898679"` 반환).
  - 기존 하이픈 분리 전화번호 None 반환 테스트는 이름을 `test_returns_none_when_no_six_to_eight_digit_match` 로 갱신, 동작 유지 (`\b\d{6,8}\b` 에서 4자리 grouping 은 6자리 최소 조건을 못 채움).
- `bash -n scripts/smoke_naver_imap.sh` → syntax OK.
- `python3 -c "from src.auth.naver_imap import fetch_verification_code"` → import OK.

## 이슈/블로커
없음.

참고(observation, 블로커 아님):
- 테스트 파일 `tests/test_naver_imap.py` 는 일반 규정상 Tester 전용이나, Manager 가 본 FIX 태스크의 "변경 사항 5" 로 명시적으로 Coder 수정을 지시했다. 지시에 따라 수정함.
- 기존 `test_extracts_six_digit_code_from_body` 와 `test_picks_latest_mail_among_multiple` 의 sender 인자는 여전히 `noreply@tistory.com` 이다. 이 두 테스트는 FROM 필터 전달 여부와 최신 UID 선택을 검증할 뿐이라 실제 발신자 주소에 의존하지 않아 변경을 최소화했다. (Manager 가 sender 통일을 원하면 추가 지시 요청.)
- `config/tistory.yaml` 의 `account` 블록은 이제 "카카오 계정" 의미로 재정의되었으므로, 후속 모듈(예: `src/sites/tistory/login.py`)이 생길 때 혼동을 줄이려면 `kakao_account:` 같은 명시적 이름으로 리네이밍하는 것도 고려 가능 (현재 태스크 범위 외, Manager 판단).

## 다음 제안
1. `scripts/smoke_naver_imap.sh` 를 `.env` 실계정으로 다시 실행해 8자리 `55898679` 가 정상 추출되는지 재검증 (Execution: user 태스크 권장).
2. 향후 `src/sites/tistory/login.py` 작성 시, 카카오 로그인 단계에서는 `config.get("account.email")` / `config.get("account.password")` 를 사용하고, 인증번호 수신 단계에서만 `fetch_verification_code(config, sender="noreply@kakaocorp.com", ...)` 를 호출하도록 명확히 분리.
3. (선택) 현재 `account.*` 키 이름이 의미상 모호하므로, 후속 리네이밍 태스크(`account.*` → `kakao.*`)를 architecture.md 의 후보 리스트에 남겨두는 것을 권장.
