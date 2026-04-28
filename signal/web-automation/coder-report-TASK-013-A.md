---
agent: coder
task_id: TASK-013-A
status: DONE
timestamp: 2026-04-22T12:00:00
---

## 결과 요약

`projects/web-automation/src/sites/tistory/writer.py` 신규 파일(388 lines)을 생성했다. `TistoryWriter(config, browser)` 클래스와 6개 async 단계 메서드(`open_newpost` / `fill_title` / `set_body_html` / `add_tags` / `select_category` / `attach_file` / `save_draft`) + 공개 진입점 `run(*, title, body_html, tags, category, category_fallback, attachments, mode="draft") -> bool` 을 login.py 와 동일한 try-except-screenshot-raise 패턴으로 구현했다. Reviewer PASS 보고서(`reviewer-report-TASK-013.md`)의 10건 수정 사항을 모두 반영했다.

## 변경된 파일

- `projects/web-automation/src/sites/tistory/writer.py` (신규, 388 lines)

## 설계 선택

1. **모듈 상단 상수 재정의 (login.py 복제)**: `_STEP_TIMEOUT_MS = 15000` 과 `_screenshot_on_error` 내부 헬퍼를 login.py 에서 그대로 복제했다. 공통 모듈 추출은 별도 리팩터 태스크로 미룸(태스크 범위 외). 스크린샷 prefix 는 `tistory_write_{step}` 로 login 과 구분.
2. **aria-label / 메뉴 텍스트 완전일치 (`re.compile(rf"^{re.escape(...)}$")`)**: 카테고리(`select_category`) 와 첨부 메뉴 kind(`attach_file`) 는 부분일치 시 위험 오매치가 발생할 수 있다(예: "여행" → "해외여행", "파일" → "슬라이드쇼 파일"). `re.escape` 로 동적 입력을 안전하게 이스케이프한 뒤 `^...$` 앵커로 완전일치 강제. save_draft 의 "임시저장" 은 상수이므로 `re.compile(r"^임시저장$")` 로 동일한 효과 달성.
3. **attach kind 상수 dict (`_ATTACH_KIND_TEXT`)**: `{"file": "파일", "image": "사진", "slideshow": "슬라이드쇼"}` 를 모듈 상수로 고정. 알 수 없는 kind 는 `ValueError` 로 조기 차단.
4. **file_chooser 순서 엄수**: `async with page.expect_file_chooser() as fc_info:` 컨텍스트 매니저 내부에서 `menu_item.first.click()` 을 호출하여 chooser 이벤트를 놓치지 않도록 순서 유지. 주석으로 "click 전에 expect_file_chooser 컨텍스트에 진입" 명시.
5. **category_fallback 재시도 로직**: `run()` 에서 `select_category(category)` 가 ValueError 를 던지면 `category_fallback is None` 여부에 따라 재시도 여부 결정. fallback 도 None 이거나 실패하면 최종 raise. 스모크 쪽에서 try/except 처리할 필요 없도록 writer 내부에서 완결.
6. **mode 분기**: `mode == "publish"` 이면 `raise NotImplementedError("publish mode 는 후속 태스크에서 구현")` — silently skip 금지. `mode != "draft"` 인 기타 값도 ValueError 로 빠르게 실패.
7. **set_body_html 검증**: `page.evaluate` 로 `tinymce.activeEditor.setContent(h)` 주입 직후 `wait_for_function` 으로 `getContent().length > 0` 검증. TinyMCE 초기화 전 주입이 silently 삼켜지는 케이스 감지.
8. **open_newpost TinyMCE init 대기**: `wait_for_function("() => window.tinymce && window.tinymce.activeEditor && window.tinymce.activeEditor.getBody()", timeout=_STEP_TIMEOUT_MS)` 로 TinyMCE 인스턴스 준비 완료 확인 후에만 다음 단계로 진행.
9. **add_tags 200ms 확정 대기**: 각 태그 fill+Enter 뒤 `page.wait_for_timeout(200)` — 태그 칩 렌더가 완료되지 않은 채 다음 태그를 입력하면 중복·누락이 발생한다는 실측을 반영.
10. **Unused import 제거**: 초기 작성 시 타입 힌트 용도로 `Locator, Page` 를 import 했으나 실제 시그니처에 사용되지 않아 제거. get_page() 반환값은 지역 변수 타입 추론으로 충분.
11. **Config key fallback**: 10개 Config key 모두 `config.get("selectors.X", "") or "<fallback>"` 패턴으로 빈 문자열 허용 + login.py 와 동일한 방어 코딩. `blog.blog_name` 만 None/빈값이면 ValueError 로 조기 차단(필수값).

## 자기검증 (DoD 9건)

### DoD #1 — 파일 생성
```
$ ls -la projects/web-automation/src/sites/tistory/writer.py
-rw-rw-r-- 1 jai jai 16156 ... writer.py
$ wc -l projects/web-automation/src/sites/tistory/writer.py
388 writer.py
```
클래스 `TistoryWriter` + 6 async 메서드 + `run()` 진입점 모두 포함. PASS.

### DoD #2 — import 통과
```
$ cd projects/web-automation && PYTHONPATH="$(pwd)" python3 -c "from src.sites.tistory.writer import TistoryWriter; print('OK')"
OK
```
PASS.

### DoD #3 — py_compile 통과
```
$ cd projects/web-automation && python3 -m py_compile src/sites/tistory/writer.py && echo "py_compile OK"
py_compile OK
```
PASS.

### DoD #4 — OCR import 0건
```
$ grep -c -E "pytesseract|easyocr" src/sites/tistory/writer.py
0
```
PASS (docstring 에 있던 예시명도 제거함).

### DoD #5 — 완전일치 `re.compile` 패턴 3건 이상 (category / attach kind / save draft 텍스트)
```
$ grep -n 're\.compile(r' src/sites/tistory/writer.py
264:                has_text=re.compile(rf"^{re.escape(name)}$"),        # select_category
317:                has_text=re.compile(rf"^{re.escape(text_for_kind)}$"), # attach_file
359:                has_text=re.compile(r"^임시저장$"),                      # save_draft
$ grep -c 're\.compile(r' src/sites/tistory/writer.py
3
```
`re.escape` 기반 2건(category/attach kind, 동적 입력) + save_draft 고정 문자열 1건 = 3건. 모두 `^...$` 앵커로 완전일치. PASS.

### DoD #6 — `async with page.expect_file_chooser()` 1건
```
$ grep -n "async with page.expect_file_chooser()" src/sites/tistory/writer.py
322:            async with page.expect_file_chooser() as fc_info:
$ grep -c "async with page.expect_file_chooser()" src/sites/tistory/writer.py
1
```
PASS.

### DoD #7 — `NotImplementedError("publish mode 는 후속 태스크에서 구현")` 1건
```
$ grep -n 'NotImplementedError("publish mode 는 후속 태스크에서 구현")' src/sites/tistory/writer.py
104:            raise NotImplementedError("publish mode 는 후속 태스크에서 구현")
$ grep -c 'NotImplementedError("publish mode 는 후속 태스크에서 구현")' src/sites/tistory/writer.py
1
```
PASS.

### DoD #8 — `category_fallback` 키워드 2건 이상
```
$ grep -n 'category_fallback' src/sites/tistory/writer.py
78:        category_fallback: Optional[str] = None,                # run() 인자
89:            category_fallback: `category` 선택이 실패했을 때 재시도할 ...  # docstring
119:                if category_fallback is None:                    # 재시도 판정
124:                    category_fallback,                           # 로깅
126:                await self.select_category(category_fallback)    # 재시도 호출
$ grep -c 'category_fallback' src/sites/tistory/writer.py
5
```
인자 선언 + docstring + 재시도 로직 3곳 = 5건. PASS.

### DoD #9 — 스크린샷 prefix `tistory_write_` 1건 이상
```
$ grep -n 'tistory_write_' src/sites/tistory/writer.py
53:    각 단계 실패 시 `screenshots/tistory_write_{step}.png` 에 스크린샷을 저장한 뒤
378:            path = await self._browser.screenshot(f"tistory_write_{step_name}")
$ grep -c 'tistory_write_' src/sites/tistory/writer.py
2
```
클래스 docstring + `_screenshot_on_error` 호출 = 2건. PASS.

## 이슈/블로커

없음.

## 다음 제안

1. **TASK-013-B 병렬 완료 확인**: 본 writer.py 가 기대하는 10개 Config key (`blog.blog_name` / `selectors.write_title_input` / `selectors.write_body_iframe` / `selectors.tag_input` / `selectors.category_btn` / `selectors.category_list` / `selectors.attach_btn` / `selectors.attach_option_prefix` / `selectors.save_draft_btn` / `selectors.publish_btn`) 가 tistory.yaml 에 원자적으로 반영되었는지 TASK-013-B 결과 확인 후 TASK-013-C 진입.
2. **공통 헬퍼 추출 리팩터 태스크(선택)**: `_STEP_TIMEOUT_MS` 상수와 `_screenshot_on_error` 헬퍼가 login.py / writer.py 에 중복 존재. 향후 `src/sites/tistory/_common.py` 또는 `src/core/workflow_base.py` 로 추출하는 별도 태스크를 만들 수 있음. 현재는 중복 2회로 "2~3회 실제 중복 확인 뒤 추상화" 원칙에 부합하며 성급한 추상화 회피.
3. **publish 모드 후속 태스크**: 현재는 `NotImplementedError` 만 raise. `selectors.publish_btn` yaml 키는 TASK-013-B 에서 `'button#publish-layer-btn'` 으로 예약 주입될 예정이므로, publish 태스크 시 해당 키 재사용 가능.
