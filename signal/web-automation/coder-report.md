---
agent: coder
task_id: TASK-003
status: DONE
timestamp: 2026-04-13
---

## 결과 요약

`src/core/config.py`에 YAML 설정 로더 `Config` 클래스를 구현했다. 공통 설정(settings.yaml) 자동 로드, 사이트별 설정 병합, 점(.) 표기법 접근, 환경변수 오버라이드를 모두 지원한다.

## 변경된 파일
- projects/web-automation/src/core/config.py (신규)

## 구현 내용

1. **Config 클래스**: 생성자에서 `config/settings.yaml`을 자동 로드
2. **load_site(site_name)**: 사이트별 YAML 파일을 추가로 로드하여 deep merge
3. **get(key, default)**: 점(.) 표기법으로 중첩 설정값 접근 (예: `config.get("browser.viewport.width")`)
4. **환경변수 오버라이드**: `WA_` 접두사 + 키를 대문자/밑줄로 변환 (예: `WA_TELEGRAM_BOT_TOKEN`). 환경변수가 있으면 YAML 값보다 우선
5. **타입 자동 변환**: 환경변수 문자열을 bool/int/float로 자동 캐스팅
6. **deep merge**: 사이트별 설정이 공통 설정과 재귀적으로 병합됨

## 검증

로컬에서 다음을 확인함:
- 공통 설정(settings.yaml) 로드 정상
- tistory.yaml, yanolja.yaml 병합 정상
- 점 표기법 접근 정상 (중첩 키 포함)
- 없는 키에 대한 기본값 반환 정상
- 환경변수 오버라이드 정상 (WA_TELEGRAM_BOT_TOKEN, WA_BROWSER_HEADLESS)

## 이슈/블로커
없음

## 다음 제안
- 다른 Core Toolkit 모듈(browser.py, logger.py, retry.py, telegram.py)에서 Config를 import하여 사용 가능
