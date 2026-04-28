---
agent: coder
task_id: TASK-012-A
status: DONE
timestamp: 2026-04-22T10:45:00
---

## 결과 요약

티스토리 카카오 로그인 + 이메일 2FA 워크플로우 `TistoryKakaoLogin` 클래스를 `projects/web-automation/src/sites/tistory/login.py` 에 신규 구현했다. 총 466줄, 6개 async 단계 메서드 + `run()` 진입점 포함. 모든 DOM 탐색은 `selectors.*` yaml 우선 → `page.get_by_role` / `get_by_text` fallback 전략으로 구성했으며, OCR 의존성·비밀번호 직접 로깅은 0건이다.

### 공개 API
- `TistoryKakaoLogin(config: Config, browser: BrowserManager)`
- `async run() -> bool` — 6단계 순차 실행 + 최종 `verify_logged_in()` 반환
- `async open_login_page()` — 티스토리 로그인 페이지 방문 + 카카오 버튼 클릭
- `async fill_kakao_credentials()` — 카카오 ID/PW 입력 + 제출
- `async switch_to_email_2fa()` — "이메일로 인증하기" / "이메일 인증" 클릭 (DOM 텍스트 파싱 fallback)
- `async poll_verification_code(sender_patterns: list[str], max_attempts=20, interval=3.0) -> str`
- `async submit_code(code: str)` — 인증번호 입력 + Enter/submit 버튼 제출
- `async verify_logged_in() -> bool` — URL · `a[href*="manage"]` 기반 성공 판정

## 변경된 파일

- `projects/web-automation/src/sites/tistory/login.py` (신규, 466줄)

기타: `src/sites/tistory/__init__.py`, `__init__.py` 류 건드리지 않음. `tests/` 미수정 (Tester 전용 영역). `config/tistory.yaml` 미수정 (TASK-012-B 범위).

## 설계 선택

### 1. fallback 전략: yaml 셀렉터 우선 → DOM role/텍스트 검색
- `selectors.*` 가 빈 문자열이면 `page.get_by_role("button"|"link")` + `.filter(has_text=…)` 로 후보 수집.
- `_is_visible_enabled()` 헬퍼로 `is_visible() and is_enabled()` 검증 후 첫 매치 선택.
- 이유: 스모크 전까지 실측 셀렉터가 없어 공란이지만, yaml 이 갱신되면 즉시 우선 경로로 전환되도록 원자적 계약을 구성.

### 2. `switch_to_email_2fa` 의 텍스트 우선순위
- 1차: `get_by_role("button"|"link", name="이메일로 인증하기")` / 동일한 이름 `"이메일 인증"` 완전일치
- 2차: `get_by_role(role).filter(has_text="이메일")` 가시/활성 첫 매치
- 이유: 스펙상 "완전일치 우선, 없으면 visible+enabled 중 첫 매치" 요구.

### 3. `poll_verification_code` 리스트 순회 + 단일 str 전달
- `for sender in sender_patterns:` 루프 내에서 `fetch_verification_code(self._config, sender=sender, within_minutes=within_minutes)` 호출.
- `naver_imap.py:162-168` 시그니처가 `sender: str` 이므로 리스트 전달 시 `imaplib SEARCH FROM` 쪽에서 TypeError 가 터진다 — 주석으로 명시.
- `max_attempts` 초과 시 `TimeoutError(f"인증번호 수신 실패 (max_attempts={max_attempts})")` raise.

### 4. `submit_code` 제출 방식
- 기본 `page.press(selector, "Enter")` 시도 후 실패하면 `button[type="submit"]` / `input[type="submit"]` fallback.
- 다양한 폼이 Enter 만으로 제출되는 일반 패턴을 1차로 잡고, 그래도 막히면 명시적 submit 버튼.

### 5. `verify_logged_in` 이 False 만 반환 (raise 금지)
- 스펙상 caller 가 판단하도록 False 반환. 내부 예외도 `try/except` 로 삼켜 False 로 치환 (경고 로그만).
- 다른 단계(open/fill/switch/submit)는 스크린샷 저장 후 예외 재raise.

### 6. 비밀번호/인증번호 로깅 금지
- `account.password` 는 `pw_len=%d` 로만 간접 노출. `code` 는 `code_len=%d` 로만 로깅.
- 입력 단계에서 값 자체가 `logger` format arg 로 건네지는 경로 0건.

### 7. 스크린샷 저장 규칙
- 단계 이름(메서드명) 그대로 `BrowserManager.screenshot(f"tistory_login_{step_name}")` 호출.
- `screenshots/tistory_login_open_login_page.png` 와 같이 파일 생성 (BrowserManager 가 `.png` 붙임).

### 8. 기존 yaml 셀렉터 미사용
- `selectors.login_email_input / login_password_input / login_submit_button` 은 로드하지 않음 (티스토리 자체 로그인 예비 경로용). 이 워크플로우는 카카오 경로 전용.

## 자기검증 (DoD 5개 항목)

### DoD 1: 파일 생성 + 클래스/메서드 정의 완료
```
$ wc -l projects/web-automation/src/sites/tistory/login.py
466 projects/web-automation/src/sites/tistory/login.py
```
공개 메서드(dir 결과, `_` 제외):
`['fill_kakao_credentials', 'open_login_page', 'poll_verification_code', 'run', 'submit_code', 'switch_to_email_2fa', 'verify_logged_in']` — 6 단계 + `run()` 총 7개 확인.

### DoD 2: import 통과
```
$ cd projects/web-automation && python3 -c "from src.sites.tistory.login import TistoryKakaoLogin; print('OK:', TistoryKakaoLogin)"
OK: <class 'src.sites.tistory.login.TistoryKakaoLogin'>
```
(참고: 현재 환경에 playwright 가 누락되어 있어 `pip install playwright` 로 설치 후 검증. requirements.txt 에는 명시되어 있음. 이 설치는 태스크 수행을 위한 단발 조치로 프로젝트 구성은 변경하지 않았다.)

### DoD 3: `fetch_verification_code` 가 단일 sender 문자열로 호출되는지
```
$ grep -n -B2 -A4 "fetch_verification_code(" src/sites/tistory/login.py
302:                code = fetch_verification_code(
303-                    self._config,
304-                    sender=sender,     # ← 단일 str (for sender in sender_patterns: 내부)
305-                    within_minutes=within_minutes,
306-                )
```
`sender=sender` 는 루프 `for sender in sender_patterns:` 의 각 원소(str)이며, 리스트 자체를 넘기는 호출은 0건.

### DoD 4: 비밀번호/인증번호가 logger 에 직접 전달 0건
```
$ grep -n "logger\." src/sites/tistory/login.py | grep -iE "password|pw|passwd"
(없음)

$ grep -n "logger\." src/sites/tistory/login.py | grep -E "\bcode\b"
(없음)
```
모든 logger 호출은 `len=%d` / `url=%s` / `selector=%s` / `attempt=%d` 같은 간접 표현만 사용. `password` / `code` 변수를 format arg 위치에 직접 넣은 경로 0건 실증.

### DoD 5: OCR 관련 import 0건
```
$ grep -nE "pytesseract|easyocr|paddleocr|tesseract|ocr\.|import.*[Oo][Cc][Rr]" src/sites/tistory/login.py
14:    - OCR (pytesseract, easyocr 등) 은 사용하지 않는다. DOM 텍스트와
```
L14 는 docstring 의 **금지 선언** 문장 안에서 OCR 단어가 노출된 것뿐이며 실제 import 문은 아니다. 실제 `import .*ocr.*` / `pytesseract` / `easyocr` 는 0건.

Import 문 전체:
```
18: from __future__ import annotations
20: import asyncio
21: from typing import Optional
23: from playwright.async_api import Locator, Page
25: from src.auth.naver_imap import fetch_verification_code
26: from src.core.browser import BrowserManager
27: from src.core.config import Config
28: from src.core.logger import get_logger
```

## 이슈/블로커

없음. 다만 **관찰 사항**으로 남긴다:
- 현재 개발 환경(`/home/jai/anaconda3`)에 playwright 패키지가 설치되어 있지 않았다. 이번 태스크 수행 중 `pip install playwright` 로 설치했으나, Playwright 브라우저 바이너리(`playwright install chromium`)는 별도 설치가 필요하다. TASK-012-C (스모크 러너) 단계에서 사용자가 실제로 실행하려면 `playwright install chromium` 이 선행되어야 한다.
- `email_2fa.sender_patterns` / `selectors.*` 5개 키는 아직 yaml 에 없으나 TASK-012-B 범위로 분리되어 있으며, `login.py` 는 Config 조회 시 공란/누락을 모두 방어(ValueError 또는 fallback 경로)한다.

## 다음 제안

1. **TASK-012-B (yaml 보강)**: `email_2fa.sender_patterns` / `email_2fa.code_length` / `email_2fa.within_minutes` / `selectors.{login_kakao_button,kakao_id_input,kakao_pw_input,email_2fa_button,auth_code_input}` 5 셀렉터 키 추가. `sender_patterns` 가 비어 있으면 `_get_sender_patterns()` 가 ValueError 로 조기 실패하므로 **반드시 1개 이상 값 필요**.
2. **TASK-012-C (스모크 러너)**: `scripts/smoke_tistory_login.sh` + `.py` 작성. `BrowserManager(headless=False)` 로 실행 후 각 단계 스크린샷 경로 로그 출력.
3. **Tester 범위**: 단위 테스트는 현재 범위 외. TASK-011 또는 TASK-015 에서 (a) `_get_sender_patterns` ValueError 분기, (b) `poll_verification_code` 가 리스트 순회하며 첫 hit 에 즉시 반환하는지 (fetch_verification_code mock), (c) `poll_verification_code` TimeoutError 경로 — 3개 단위 테스트 권장.
