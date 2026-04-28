---
agent: coder
task_id: TASK-012-B
status: DONE
timestamp: 2026-04-22T10:15:00
---

## 결과 요약
`projects/web-automation/config/tistory.yaml` 를 보강해 카카오 로그인 경로에 필요한 신규 셀렉터 4키(`login_kakao_button`/`kakao_id_input`/`kakao_pw_input`/`email_2fa_button`)를 `selectors` 섹션에 추가하고, 신규 최상위 섹션 `email_2fa`(sender_patterns·code_length·within_minutes)를 추가했다. 기존 7개 셀렉터 키는 전부 유지했고, `auth_code_input`은 중복 추가 없이 기존 키를 재사용한다. 네이밍은 `kakao_auth`가 아닌 `email_2fa`로 지어 향후 다른 사이트 email 2FA 재사용이 가능하게 했다.

## 변경된 파일
- projects/web-automation/config/tistory.yaml (수정, 37→59 줄)

## 변경 diff 요약
### `selectors` 섹션 (L30-L47)
기존 7키(L31-L37)를 유지하되, 그룹 주석으로 3블록 분리 + 신규 4키 추가:
- 블록 1 "티스토리 자체 로그인 (현재 미사용, 예비)": `login_email_input`/`login_password_input`/`login_submit_button` (기존 유지)
- 블록 2 "카카오 로그인 경로 (TASK-012 구현 대상)" (신규): `login_kakao_button` / `kakao_id_input` / `kakao_pw_input` / `email_2fa_button`
- 블록 3 "인증번호 / 글쓰기 (공용)": `auth_code_input` (기존 재사용) / `write_title_input` / `write_content_area` / `write_publish_button`

### 신규 최상위 섹션 `email_2fa` (L49-L59)
```yaml
email_2fa:
  sender_patterns:
    - "noreply@kakaocorp.com"
    - "accounts.kakao.com"
    - "kakao.com"
  code_length: 8
  within_minutes: 5
```

## DoD 검증 (grep·python3 실측)

### DoD 1: 8개 공유 Config key 존재 (명령·결과 인용)
실행 위치: `projects/web-automation/`

| 명령 | 결과 (1 hit 기대) |
|---|---|
| `grep -E "^\s+login_kakao_button:" config/tistory.yaml` | `  login_kakao_button: ""               # 티스토리 로그인 페이지의 "카카오 계정으로 로그인" 버튼` |
| `grep -E "^\s+kakao_id_input:" config/tistory.yaml` | `  kakao_id_input: ""                   # 카카오 로그인 폼 ID 입력` |
| `grep -E "^\s+kakao_pw_input:" config/tistory.yaml` | `  kakao_pw_input: ""                   # 카카오 로그인 폼 비밀번호 입력` |
| `grep -E "^\s+email_2fa_button:" config/tistory.yaml` | `  email_2fa_button: ""                 # 2차 인증 화면 "이메일로 인증하기" 버튼 (DOM 텍스트 fallback 있음)` |
| `grep -E "^\s+auth_code_input:" config/tistory.yaml` | `  auth_code_input: ""                  # 인증번호 입력 필드 (TASK-012-A poll_verification_code 흐름에서 사용)` |
| `grep -E "^email_2fa:" config/tistory.yaml` | `email_2fa:` |
| `grep -E "^\s+sender_patterns:" config/tistory.yaml` | `  sender_patterns:` |
| `grep -E "^\s+code_length:" config/tistory.yaml` | `  code_length: 8` |
| `grep -E "^\s+within_minutes:" config/tistory.yaml` | `  within_minutes: 5` |

9개 grep 모두 정확히 1 hit. (`auth_code_input`은 기존 키 재사용이므로 중복 없음 — python 파싱 결과 `selectors` 딕셔너리에 단 한 번만 등장 확인.)

### DoD 2: `kakao_auth` 0건 실증
```
$ grep -c "kakao_auth" config/tistory.yaml
0
$ grep -n "kakao_auth" config/tistory.yaml ; echo "exit=$?"
exit=1                # grep이 매치 없을 때 반환하는 exit 1
```
→ `kakao_auth` 문자열 완전 부재 확인.

### DoD 3: yaml 파싱 성공
```
$ python3 -c "import yaml; c=yaml.safe_load(open('config/tistory.yaml')); print('parse OK'); print('top-level keys:', list(c.keys())); print('selectors keys:', list(c['selectors'].keys())); print('email_2fa:', c['email_2fa'])"
parse OK
top-level keys: ['site', 'account', 'naver_imap', 'blog', 'selectors', 'email_2fa']
selectors keys: ['login_email_input', 'login_password_input', 'login_submit_button', 'login_kakao_button', 'kakao_id_input', 'kakao_pw_input', 'email_2fa_button', 'auth_code_input', 'write_title_input', 'write_content_area', 'write_publish_button']
email_2fa: {'sender_patterns': ['noreply@kakaocorp.com', 'accounts.kakao.com', 'kakao.com'], 'code_length': 8, 'within_minutes': 5}
```
→ 파싱 성공. 최상위 6키(site/account/naver_imap/blog/selectors/email_2fa) 구조 유지. selectors는 총 11개 키(기존 7 + 신규 4). email_2fa는 의도한 dict shape 그대로.

### DoD 4: 기존 7개 selector 키 유지 실증
```
$ grep -E "^\s+login_email_input:" config/tistory.yaml     → 1 hit (빈 문자열 값, 기존 주석 유지)
$ grep -E "^\s+login_password_input:" config/tistory.yaml  → 1 hit
$ grep -E "^\s+login_submit_button:" config/tistory.yaml   → 1 hit
$ grep -E "^\s+auth_code_input:" config/tistory.yaml       → 1 hit (기존 키, 주석 업데이트 — TASK-012-A 맥락 반영)
$ grep -E "^\s+write_title_input:" config/tistory.yaml     → 1 hit
$ grep -E "^\s+write_content_area:" config/tistory.yaml    → 1 hit
$ grep -E "^\s+write_publish_button:" config/tistory.yaml  → 1 hit
```
→ 7개 모두 삭제 없이 보존. 값은 공란 유지(변경 없음). 주석은 `auth_code_input`만 TASK-012-A poll 흐름 명시로 업데이트, 나머지는 원문 유지.

### 추가: 파일 끝 개행 확인
```
$ tail -c 5 config/tistory.yaml | od -c
0000000   s   :       5  \n
```
→ 파일 끝 `within_minutes: 5\n` 형태로 개행 1개 정상.

## TASK-012-A 와의 계약 정합성 확인
task-board.md L24 TASK-012-A 가 명시한 "공유 Config key 계약" 8개 키와 yaml 내 실제 키 경로를 대조:

| 계약 key 경로 | yaml 내 실측 위치 |
|---|---|
| `selectors.login_kakao_button` | selectors dict에 존재 (DoD 1·3) |
| `selectors.kakao_id_input` | selectors dict에 존재 |
| `selectors.kakao_pw_input` | selectors dict에 존재 |
| `selectors.email_2fa_button` | selectors dict에 존재 |
| `selectors.auth_code_input` | selectors dict에 존재 (기존 재사용) |
| `email_2fa.sender_patterns` | `['noreply@kakaocorp.com', 'accounts.kakao.com', 'kakao.com']` (list[str], 3개) |
| `email_2fa.code_length` | `8` (int) |
| `email_2fa.within_minutes` | `5` (int) |

8개 모두 `Config.get()` 으로 도트 경로 접근 가능한 구조로 존재. 타입도 TASK-012-A 명세(`sender_patterns: list[str]`, `code_length: int default 8`, `within_minutes: int default 5`)와 일치.

## 이슈/블로커
없음.

## 다음 제안
- TASK-012-C (스모크 러너) 작성 시점에 `config/tistory.yaml` 의 5개 신규 selector 값이 공란이어도 `login.py` DOM fallback 경로로 최초 실행이 가능하도록 설계되어 있음(TASK-012-A 명세 기반). 실측 후 셀렉터 채움은 TASK-012-D 사용자 스모크 결과를 받아 후속 FIX 태스크로 처리하는 것이 자연스럽다.
- `email_2fa.sender_patterns` 3개 후보(`noreply@kakaocorp.com`/`accounts.kakao.com`/`kakao.com`)도 스모크에서 실제 카카오 발신 주소 확인 후 좁힐 것을 권장. 현재는 도메인 suffix 매치까지 허용하는 넓은 기본값.
