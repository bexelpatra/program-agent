---
task_id: TASK-008-FIX
verdict: PASS
---

# Reviewer Report: TASK-008-FIX

## 검증 대상
- 파일:
  - `projects/web-automation/src/auth/naver_imap.py`
  - `projects/web-automation/config/tistory.yaml`
  - `projects/web-automation/tests/test_naver_imap.py`
  - `projects/web-automation/.env.example`
  - `projects/web-automation/scripts/smoke_naver_imap.sh`
- Manager 주장 요약:
  1. 카카오 인증번호는 8자리 숫자. 현재 기본 regex `\b\d{6}\b` 로는 매치 불가 → `\b\d{6,8}\b` 로 변경.
  2. 실 로그인 계정은 카카오. 네이버는 IMAP 수신 전용. `account.*` 주석/Config 키 분리 필요.
  3. 기존 파일 상태(함수 시그니처, mock config 키, .env 변수, smoke 스크립트 검증).

## 검증 결과

### 파일 존재
| 경로 | 존재 | 비고 |
|------|------|------|
| src/auth/naver_imap.py | O | 275 lines |
| config/tistory.yaml | O | 36 lines |
| tests/test_naver_imap.py | O | 199 lines |
| .env.example | O | 19 lines |
| scripts/smoke_naver_imap.sh | O | 75 lines |

### 내용 일치

**주장 1: 기본 regex `\b\d{6}\b`, 카카오 코드 8자리 미스매치**
- `src/auth/naver_imap.py:35` `_DEFAULT_CODE_PATTERN = r"\b\d{6}\b"` — 일치.
- `src/auth/naver_imap.py:164` `fetch_verification_code(..., code_pattern: str = _DEFAULT_CODE_PATTERN, ...)` — 기본값으로 사용. 일치.
- `\b\d{6}\b` 는 단어 경계 내 정확히 6자리만 매치하므로 8자리 `55898679` 은 매치 불가(확인). 변경안 `\b\d{6,8}\b` 로 6/7/8 모두 커버됨. 합당.
- 실제 메일 내용(`55898679`, 2026-04-22 09:30)은 Reviewer 가 메일함 접근 불가 — Manager 스모크 증언 신뢰.

**주장 2: tistory.yaml 주석 "Naver 이메일 주소", 계정 분리 필요**
- `config/tistory.yaml:11-13`:
  ```
  account:
    email: "YOUR_EMAIL_HERE"             # Naver 이메일 주소
    password: "YOUR_PASSWORD_HERE"       # Naver 이메일 비밀번호
  ```
  Manager 주장 라인 범위 L10-13 은 근사치(실제 L11-13). 주석 내용 정확 일치 — "Naver 이메일" 로 표기되어 있어 카카오 로그인 사실과 불일치. 수정 필요 확인.
- `config/tistory.yaml:15-19` `naver_imap:` 블록에는 `server`/`port`/`use_ssl` 만 존재하고 `email`/`password` 필드 없음 — 신규 필드 추가 전제 일치.

**주장 3: 기존 파일 상태**
- `src/auth/naver_imap.py:190-193`: `config.get("naver_imap.server")`, `config.get("naver_imap.port", 993)`, `config.get("account.email")`, `config.get("account.password")` — 정확 일치.
- `src/auth/naver_imap.py:197` ValueError 메시지에 `naver_imap.server, account.email, account.password` 문구 포함 — 키 교체 시 함께 갱신 대상.
- `tests/test_naver_imap.py:42-47` mock config 키 `naver_imap.server`/`naver_imap.port`/`account.email`/`account.password` — 정확 일치.
- `.env.example:12-13` `WA_ACCOUNT_EMAIL`, `WA_ACCOUNT_PASSWORD` 만 있음 — 일치.
- `scripts/smoke_naver_imap.sh:35-42` `WA_ACCOUNT_EMAIL`, `WA_ACCOUNT_PASSWORD` 두 변수만 검증 — 일치.

### 태스크 완결성
- 기본 regex 단일 토큰 교체(`\b\d{6}\b` → `\b\d{6,8}\b`): 명확, 단일 줄.
- Config 키 분리: `account.email`/`account.password` (카카오 로그인) ↔ `naver_imap.email`/`naver_imap.password` (IMAP 수신). naver_imap 블록은 이미 존재하므로 필드 추가가 자연스러움.
- 연쇄 수정 포인트 5곳(코드, yaml, 테스트, .env.example, smoke 스크립트) 모두 실측으로 확정 — Coder 가 외부 질문 없이 실행 가능.

### 의존성·순서
- 단일 수정 태스크, 의존 없음.
- 동일 함수·파일 내 수정이라 병렬 충돌 없음.

## 판정
**PASS**

## Manager에게 전달

Manager 주장 3건 모두 파일 실측과 일치. Coder 호출 진행 가능.

Coder 지시서에 아래 5개 수정 포인트를 완료 조건으로 명시 권장:

1. **`src/auth/naver_imap.py`**
   - L35: `_DEFAULT_CODE_PATTERN = r"\b\d{6,8}\b"`
   - L169-173 docstring 키 업데이트: `account.email`/`account.password` → `naver_imap.email`/`naver_imap.password`
   - L192-193 Config 키 교체: `config.get("naver_imap.email")`, `config.get("naver_imap.password")`
   - L197 ValueError 메시지도 신규 키로 업데이트
2. **`config/tistory.yaml`**
   - L11-13 `account:` 주석을 "카카오(티스토리 로그인) 계정" 으로 교체
   - L15-19 `naver_imap:` 블록에 `email: ""` / `password: ""` 신규 필드 추가 (주석: Naver 메일 IMAP 수신 계정)
3. **`tests/test_naver_imap.py`** L42-47: mock values 키를 `naver_imap.email`/`naver_imap.password` 로 교체. `test_raises_when_config_missing_password` 도 동일 키 기준 유지.
4. **`.env.example`**
   - `WA_ACCOUNT_EMAIL`/`WA_ACCOUNT_PASSWORD` 주석을 "카카오 계정(티스토리 로그인)" 으로 변경
   - `WA_NAVER_IMAP_EMAIL`/`WA_NAVER_IMAP_PASSWORD` 신규 항목 추가 (주석: Naver 메일 IMAP 수신)
5. **`scripts/smoke_naver_imap.sh`** L35-42: 검증 대상 변수를 `WA_NAVER_IMAP_EMAIL`/`WA_NAVER_IMAP_PASSWORD` 로 교체 (IMAP 접속이 목적이므로 네이버 계정만 있으면 충분).

보조 권장:
- 신규 regex 기본값 `\b\d{6,8}\b` 로 6/7/8 자리 모두 매치되는 유닛테스트 케이스 1~2건 추가(또는 기존 `test_extracts_six_digit_code_from_body` 옆에 `test_extracts_eight_digit_code`).
- Reviewer 가 카카오 메일 실물(`55898679`) 직접 확인 불가 — Manager 스모크 로그 증언 기반 신뢰.
