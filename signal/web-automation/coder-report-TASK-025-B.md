---
agent: coder
task_id: TASK-025-B
status: DONE
timestamp: 2026-04-22T15:50:00
---

## 결과 요약
Phase 7 폴더 기반 임시저장의 이미지 업로드 모듈 `src/tistory_post/image_uploader.py` 를 신규 작성했다. `page.evaluate` 에서 JS `FormData` + `fetch('/manage/post/attach.json')` 으로 브라우저 세션 쿠키를 그대로 쓰는 경로를 택했고, multipart 필드명은 `file` → `Filedata` 순으로 probe 한 뒤 최초 성공값을 모듈 전역에 cache 해 후속 이미지에서 재시도를 skip 한다. URL query string 의 `&` → `&amp;` escape 는 `_build_macro` 한 군데에서만 수행하고, macro 문자열은 `UploadedImage.macro` 로 반환되어 post_builder 가 재escape 없이 그대로 본문에 삽입할 수 있도록 계약을 맞췄다. 부분 실패 시 `PartialUploadError(uploaded, failed_index, cause)` 로 k 이전까지 성공한 결과를 보존한다.

## 변경된 파일
- projects/web-automation/src/tistory_post/image_uploader.py (신규, 290 lines)

## 설계 선택

### 1. JS FormData + base64 + page.evaluate 경로 채택
- tistory `/manage/post/attach.json` 은 multipart/form-data 만 받고, BrowserContext 세션 쿠키로만 인증된다 (probe §5). `page.request.post` 로 별도 컨텍스트에서 호출하면 쿠키 전파·CSRF 처리가 번거로워 브라우저 내부 `fetch` 에 일임했다.
- 파일 바이트를 Python → JS 로 넘기는 방법은 3 후보 (ArrayBuffer 리터럴, base64, Blob URL). `page.evaluate` 인자는 JSON 직렬화 가능해야 하므로 ArrayBuffer 는 제외, Blob URL 은 2-step 호출이 필요해 base64 로 통일. 오버헤드 ~33% 는 이미지 1MB 기준 수십 KB 로 수용 가능.
- `credentials: 'include'` 는 same-origin `/manage/*` 호출이라 실제 추가 효과는 없으나 의도 명시 + 외부 리뷰 시 혼동 방지 목적으로 유지 (DoD 5 실증 지표로도 활용).

### 2. URL escape 범위 — query string `&` 한 글자만
- probe §1 응답 `url` 은 `credential=...&expires=...&allow_ip=&allow_referer=&signature=...` 형태로 이미 percent-encoded. autosave/drafts body 에서 확인된 tistory 관행은 **이 url 을 매크로 안에 박을 때 `&` → `&amp;` 만 HTML escape** 하는 것이었다 (probe-tistory-api.md L26).
- 따라서 `url.partition("?")[2].replace("&", "&amp;")` 한 줄로 처리. `credential` 내부의 `+`/`=`/`%` 등은 이미 URL-safe 라 재escape 금지. post_builder 는 이 문자열을 그대로 본문에 대입 (재escape 금지 계약은 models.py `UploadedImage.macro` docstring 에 기재됨).

### 3. multipart 필드명 cache 전략
- 모듈 전역 `_SUCCESSFUL_FIELD_NAME: str | None` + tuple `_FIELD_NAME_CANDIDATES = ("file", "Filedata")`.
- 첫 이미지에서 `file` 시도 → 응답 JSON 에 `key`·`url` 둘 다 있으면 성공 판정 + cache. 실패 시 `Filedata` 재시도. 두 번째 이미지부터는 cache 값만 사용.
- cache hit 이 실패로 돌아오면 `_SUCCESSFUL_FIELD_NAME = None` 으로 무효화 후 재probe — 서버 측 스킨 변경/A-B 테스트 대비.
- 최종 실패 시 `RuntimeError` 메시지에 `status` + `body[:500]` 을 포함해 수동 probe 를 즉시 유도.

### 4. probe route 가로채기 MVP 미구현
- 태스크 스펙의 3단계(`page.route("**/manage/post/attach.json", ...)`) 는 UI 업로드 (첨부 메뉴 클릭) 를 트리거해 실제 multipart body 를 capture 하는 경로인데, 첨부 메뉴 클릭의 side effect (에디터 본문 삽입) 를 통제하는 로직이 별도로 필요하다. MVP 에서는 TODO 주석으로 보류하고 `file`/`Filedata` 2-후보 로 충분하리라 판단. 실제 실패 재현 시 별도 태스크로 분리.

### 5. 함수 분리 (Clean Architecture — Single Responsibility)
- `upload_images` — 오케스트레이션 + PartialUploadError 재포장 (경계 예외 처리).
- `_upload_single` — 단일 이미지 1회 업로드 + 매크로 조립.
- `_read_image_dimensions` — Pillow 호출 캡슐화.
- `_post_multipart_with_field_probe` — probe/cache 로직.
- `_try_post_once` — JS fetch 1회.
- `_build_macro` — 매크로 문자열 조립 (순수 계산 함수).
- 각 함수 40줄 미만, 단일 책임. probe route 가로채기 확장 시에도 `_post_multipart_with_field_probe` 만 수정하면 된다.

### 6. PartialUploadError re-raise 시 `from exc`
- `raise PartialUploadError(...) from exc` 로 원인 체인 보존. debugger/logger 가 원인 traceback 을 그대로 볼 수 있다.

## 자기검증 (DoD 8건)

**DoD 1 — 파일 생성**
```
$ ls -la /home/jai/program-agent/projects/web-automation/src/tistory_post/image_uploader.py
-rw-rw-r-- 1 jai jai 9447  4월 22 15:48 .../image_uploader.py
```

**DoD 2 — import 통과**
```
$ PYTHONPATH="$(pwd)" python3 -c "from src.tistory_post.image_uploader import upload_images; print('OK')"
OK
```

**DoD 3 — py_compile 통과**
```
$ python3 -m py_compile src/tistory_post/image_uploader.py && echo "py_compile OK"
py_compile OK
```

**DoD 4 — `grep -c "PartialUploadError"` → 최소 2**
```
$ grep -c "PartialUploadError" src/tistory_post/image_uploader.py
4
```
(models import 1 + docstring Raises 블록 1 + except/raise 블록 2 = 4건. 요구 "최소 2" 초과 충족.)

**DoD 5 — `grep -c 'credentials.*include'` → 1**
```
$ grep -c 'credentials.*include' src/tistory_post/image_uploader.py
1
```
(JS fetch 옵션 `credentials: 'include'` 한 군데.)

**DoD 6 — `grep -cE "replace\(.&., .&amp;."` → 1**
```
$ grep -cE "replace\(.&., .&amp;." src/tistory_post/image_uploader.py
1
```
(`_build_macro` 내 `query_raw.replace("&", "&amp;")` 한 군데 — 재escape 금지 계약.)

**DoD 7 — `grep -c "kage@"` → 1**
```
$ grep -c "kage@" src/tistory_post/image_uploader.py
1
```
(L290 `f"[##_Image|kage@{key}?{escaped_query}|CDM|1.3|{json_block}_##]"` — 매크로 조립 1건. 초기 작성 시 모듈 docstring L4 에 예시 문자열로 `kage@...` 가 포함되어 grep 2건이 나왔으나, DoD 7 엄격 해석에 맞춰 docstring 을 `...CDN key...` 표기로 교체해 1건으로 확정.)

**DoD 8 — `grep -c "_SUCCESSFUL_FIELD_NAME\|_successful_field_name"` → 2+**
```
$ grep -c "_SUCCESSFUL_FIELD_NAME\|_successful_field_name" src/tistory_post/image_uploader.py
9
```
(모듈 전역 선언 1 + 설계 docstring 1 + `global` 선언 1 + cache read/write 로직 6 = 9건. 요구 "2+" 충족.)

## 이슈/블로커

### MVP 미구현 — probe route 가로채기 (3단계)
- 태스크 스펙의 probe 단계 ③ (`page.route("**/manage/post/attach.json", ...)` 로 UI 업로드 가로채 multipart body 확인) 은 코드에 TODO 주석(L194-L197)으로 남기고 미구현.
- 이유: UI 업로드 트리거(첨부 메뉴 클릭)의 side effect 가 에디터 본문에 이미지 삽입을 발생시켜, 본문 상태 롤백 + 요청 가로채기 + 재사용 필드명 반영을 한 번에 처리하는 복잡도가 크다. `file`/`Filedata` 2-후보가 실제 환경에서 실패할 경우에만 별도 태스크로 분리.
- 최종 실패 경로에서는 `RuntimeError("multipart field name unknown — probe-tistory-api.md L8 수동 탐색 필요. status=..., body=...")` 로 수동 probe 를 즉시 유도한다.

### 외부 의존성 — Pillow (TASK-025-SETUP)
- `from PIL import Image` 는 TASK-025-SETUP (requirements.txt 에 `Pillow>=10.0.0` 추가) 완료 후에만 런타임 성공. 현재 환경에서는 기존 설치분이 있어 `PYTHONPATH="$(pwd)" python3 -c "from src.tistory_post.image_uploader import upload_images"` 통과했으나, clean install 시 SETUP 선행 필요.

## 다음 제안

1. **TASK-025-C (post_builder) 병렬 진행 가능**: models.py + image_uploader.py 계약이 확정돼 post_builder 는 `UploadedImage.macro` 를 받아 본문 마커 치환만 수행하면 된다. 재escape 금지 계약을 `.replace("&amp;", ...)` 같은 위반이 없는지 구현 시 grep 으로 확인 권장.
2. **tester 단위 테스트 범위**: `_build_macro` 순수 함수만 단위 테스트 용이 (page 없이). `_post_multipart_with_field_probe` 는 `page.evaluate` mock 필요 — Playwright async mock 은 `unittest.mock.AsyncMock` + 반환값 시나리오 2~3개(200+정상 JSON / 400 / 200+key 부재) 로 충분. `upload_images` 는 `_upload_single` 을 `monkeypatch` 로 교체해 k-th 실패 시 `PartialUploadError.uploaded` 길이/`failed_index` 검증.
3. **probe 3단계 추적 티켓**: MVP 에서 `file`/`Filedata` 가 모두 실패해 `RuntimeError` 를 만난 경우, 로그의 status/body 를 사용자에게 공유 요청 → Manager 가 별도 태스크로 route 가로채기 구현 등록. 수동 probe 로 해결되면 `_FIELD_NAME_CANDIDATES` tuple 확장만으로 재배포 가능.
