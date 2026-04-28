# Done Log

### TASK-001 (DONE) - 2026-04-13T20:35
- title: 프로젝트 초기화 (requirements.txt, 디렉토리 구조, config 템플릿)
- assignee: coder
- summary: 12개 파일 생성. requirements.txt, config YAML 3개(settings/tistory/yanolja), 전체 디렉토리 구조 + __init__.py 완료.
- files: requirements.txt, config/settings.yaml, config/tistory.yaml, config/yanolja.yaml, src/__init__.py 외 7개 __init__.py

### TASK-003 (DONE) - 2026-04-13T20:40
- title: Core - config.py (YAML 설정 로더)
- assignee: coder
- summary: Config 클래스 구현. YAML 로드, 사이트별 병합, 점 표기법 접근, 환경변수 오버라이드(WA_ 접두사), 자동 타입 캐스팅 지원.
- files: src/core/config.py

### TASK-002 (DONE) - 2026-04-13T20:50
- title: Core - browser.py (Playwright 브라우저 엔진)
- assignee: coder
- summary: BrowserManager 클래스 구현. async context manager, start/stop/goto/wait_for/click/fill/screenshot/get_page. Config에서 브라우저 설정 로드.
- files: src/core/browser.py

### TASK-004 (DONE) - 2026-04-13T20:50
- title: Core - telegram.py (텔레그램 봇 알림)
- assignee: coder
- summary: TelegramNotifier 클래스 구현. send_message/send_photo/send_alert. enabled=false 시 no-op, 실패 시 예외 없이 로깅만.
- files: src/core/telegram.py

### TASK-005 (DONE) - 2026-04-13T20:50
- title: Core - logger.py (로깅 + 단계별 스크린샷)
- assignee: coder
- summary: setup_logger/get_logger 구현. 파일+콘솔 핸들러, 디렉토리 자동 생성, 포맷: [날짜] [레벨] [모듈] 메시지.
- files: src/core/logger.py

### TASK-006 (DONE) - 2026-04-13T20:50
- title: Core - retry.py (재시도 데코레이터)
- assignee: coder
- summary: retry/async_retry 데코레이터 구현. 지수 백오프, 예외 타입 필터, Config에서 기본값 로드.
- files: src/core/retry.py

### TASK-008-FIX (DONE) - 2026-04-22T09:50
- title: 스모크 결과 반영 — 정규식 6~8자리 확장 + 카카오/네이버 계정 분리
- assignee: coder
- summary: 실계정 스모크로 카카오 인증번호가 8자리(`55898679`)임을 확인. 정규식 기본값 `\b\d{6}\b` → `\b\d{6,8}\b` 로 확장. Config 키 재설계: `account.*`=카카오(티스토리 로그인), `naver_imap.email`/`naver_imap.password`=네이버(IMAP). `.env.example` 2섹션 분리, 스크립트 검증 로직 업데이트, 기본 sender `noreply@kakaocorp.com`. 테스트 6/6 통과.
- files: src/auth/naver_imap.py (수정), config/tistory.yaml (수정), .env.example (수정), scripts/smoke_naver_imap.sh (수정), tests/test_naver_imap.py (수정)
- public_api_change: `fetch_verification_code(..., code_pattern=r"\b\d{6,8}\b")` 기본값 변경. Config 키 `account.*` → `naver_imap.*` (IMAP 접속용만).

### TASK-008-UX (DONE) - 2026-04-22T01:20
- title: .env 템플릿 + smoke 실행 shell wrapper
- assignee: manager (직접 작성)
- summary: 사용자가 python 명령을 직접 입력하지 않도록 bash wrapper 작성. `.env.example` 템플릿과 `.env` 자동 source, 필수 변수 검증, 예외 처리, 커스텀 sender 인자 지원.
- files: .env.example (신규), scripts/smoke_naver_imap.sh (신규, chmod +x)

### TASK-008 (DONE) - 2026-04-22T00:30
- title: auth/naver_imap.py (Naver IMAP 연결 → 인증번호 자동 추출)
- assignee: coder
- summary: Python 표준 `imaplib`+`email`만으로 `fetch_verification_code(config, sender, within_minutes=5, code_pattern=r"\b\d{6}\b", timeout=30)` 구현. `tistory.yaml`의 기존 `naver_imap`/`account` 블록 재사용 (설정 중복 추가 없음). UID 내림차순 + `Date` 헤더 분 단위 필터. mock 단위 테스트 5개 전부 통과 (0.011s).
- files: src/auth/naver_imap.py (신규), src/auth/__init__.py (수정), tests/test_naver_imap.py (신규)
- public_api: `fetch_verification_code(config, sender, within_minutes=5, code_pattern=r"\b\d{6}\b", timeout=30) -> str | None` — 필수 Config 키 누락 시 ValueError.
- next: TASK-008-SMOKE (사용자 실계정 스모크 테스트), 이후 TASK-012 (티스토리 로그인)에서 이 함수를 polling 루프로 감싸 호출.

- task_id: TASK-012-B
- status: DONE
- completed_at: 2026-04-22T10:45
- assignee: coder
- summary: `config/tistory.yaml` 37→59줄 보강. selectors 섹션에 카카오 로그인 전용 4키 신규(`login_kakao_button`/`kakao_id_input`/`kakao_pw_input`/`email_2fa_button`) 추가, 주석 블록 3개로 그룹 분리. 기존 `auth_code_input` 재사용. 신규 최상위 섹션 `email_2fa` 추가(`sender_patterns` 3개 리스트·`code_length: 8`·`within_minutes: 5`). `kakao_auth` 0건(grep). yaml.safe_load 파싱 성공. 공유 Config key 계약 8개 전수 grep 1 hit 실증.
- report: signal/web-automation/coder-report-TASK-012-B.md

- task_id: TASK-012-A
- status: DONE
- completed_at: 2026-04-22T10:50
- assignee: coder
- summary: `src/sites/tistory/login.py` 신규 466줄. 클래스 `TistoryKakaoLogin(config, browser)` + 6개 단계 async 메서드(`open_login_page`/`fill_kakao_credentials`/`switch_to_email_2fa`/`poll_verification_code`/`submit_code`/`verify_logged_in`) + `run()` 진입점. selectors yaml 우선 → `get_by_role + filter(has_text) + _is_visible_enabled` fallback. `switch_to_email_2fa` "이메일로 인증하기"/"이메일 인증" 완전일치→"이메일" 포함 가시/활성 순. OCR import 0건. `password`/`code` logger format arg 직접 전달 0건(`pw_len=%d`/`code_len=%d` 간접 표현만). `fetch_verification_code(config, sender=s)` 리스트 순회 첫 hit 반환. 관찰: playwright chromium 바이너리(`playwright install chromium`)는 스모크 전 선행 필요.
- report: signal/web-automation/coder-report-TASK-012-A.md

- task_id: TASK-012-C
- status: DONE
- completed_at: 2026-04-22T11:10
- assignee: coder
- summary: `scripts/smoke_tistory_login.sh` (755) + `scripts/smoke_tistory_login.py` 신규 2파일. smoke_naver_imap.sh 2필드 검증을 `missing_fields` 배열로 4필드(`WA_ACCOUNT_EMAIL`/`WA_ACCOUNT_PASSWORD`/`WA_NAVER_IMAP_EMAIL`/`WA_NAVER_IMAP_PASSWORD`) 확장. `WA_BROWSER_HEADLESS=false` env override 로 headful 강제(Config WA_ 우선권 경유, `_headless` private 수정 안티패턴 회피). playwright chromium 바이너리 선행 체크 실패 시 exit 2 + 설치 안내. python 엔트리는 `sys.path.insert` → `src.*` import (`# noqa: E402`), `main() -> int` 종료 코드 0/1/2 구분. DoD 7건 전수 PASS (bash -n / py_compile / _headless 0건 / 4필드 10 hit / HEADLESS=false / playwright install chromium 안내 / 755).
- report: signal/web-automation/coder-report-TASK-012-C.md

- task_id: TASK-012-ENV
- status: DONE
- completed_at: 2026-04-22T11:00
- assignee: user
- summary: `.env`에 `WA_ACCOUNT_EMAIL`/`WA_ACCOUNT_PASSWORD` 2개 추가 완료 (사용자 수동). 스모크 실행 시 Config.get 의 WA_ 환경변수 우선권으로 yaml placeholder 덮어쓰기 확인(email len=15, pw len=12, 'YOUR' 미포함).

- task_id: TASK-012-D
- status: DONE
- completed_at: 2026-04-22T11:20
- assignee: user+manager
- summary: 실계정 스모크 테스트 `xvfb-run -a ./scripts/smoke_tistory_login.sh` 최종 결과 **exit 0**. URL=`https://www.tistory.com/`, `verify_logged_in: True`. 실행 환경: 서버(no DISPLAY) → xvfb-run 가상 X 서버 래핑 필요. 3회차 실행에서 3 bug + 2 fix 발견 → TASK-012-FIX 로 즉시 수정 후 4회차 실행에서 성공.
- report: (스모크 로그 인라인)

- task_id: TASK-012-FIX
- status: DONE
- completed_at: 2026-04-22T11:20
- assignee: coder(manager-inline)
- summary: 스모크에서 발견한 3 bug + 2 fix 일괄 수정.
  * **BUG-1** `login.py:verify_logged_in` URL-encoded redirect 의 `tistory.com` 문자열 포함 substring 매치로 false-positive (`"tistory.com" in url` + `"/auth/login" not in url`) → `urlparse(url).hostname` 기준 판정으로 교체.
  * **BUG-2** `login.py:poll_verification_code` `code_length_hint` 를 로깅만 하고 `fetch_verification_code` 에 `code_pattern` 인자로 전달 안 함 → naver_imap 기본 `\b\d{6,8}\b` 가 메일 본문 6자리 숫자(남은시간/주문번호 등) 먼저 매치 → `code_pattern=rf"\b\d{{{code_length_hint}}}\b"` 전달로 교체.
  * **BUG-3** `login.py:verify_logged_in` submit 직후 카카오→kauth→tistory 리다이렉트 체인 완료 전에 판정 → 1초 간격 10회 폴링 loop 추가.
  * **FIX-4** `login.py:switch_to_email_2fa` fill_kakao 직후 2FA 화면 렌더 완료 전 `get_by_role().count()` 0 반환 → 앞에 `page.wait_for_selector("text=이메일로 인증", timeout=_STEP_TIMEOUT_MS)` 추가.
  * **FIX-5** `config/tistory.yaml` 카카오 실측 셀렉터 주입: `kakao_id_input: 'input[name="loginId"]'` / `kakao_pw_input: 'input[name="password"]'`. 기존 fallback `input[type="email"]` 이 카카오 실제 `input[type="text"][name="loginId"]` 와 불일치.
- report: (manager-inline, smoke 로그·DOM 실측 기반)

- task_id: TASK-013-B
- status: DONE
- completed_at: 2026-04-22T12:00
- assignee: coder
- summary: `config/tistory.yaml` 59→67줄. blog.blog_name "YOUR_BLOG_NAME"→"perlky" 실측 주입. selectors 섹션 재편(Reviewer #1 택B): write_title_input 값 덮어쓰기('textarea#post-title-inp'), write_content_area 삭제, write_publish_button→publish_btn rename + 값 주입. 신규 7키 추가(write_body_iframe/tag_input/category_btn/category_list/attach_btn/attach_option_prefix/save_draft_btn). DoD 7건 PASS: yaml.safe_load 성공, write_content_area grep=0, write_publish_button grep=0, publish_btn grep=1, 공유 10키 각 1 hit, YOUR_BLOG_NAME 0건, TASK-012-FIX kakao_* 셀렉터 보존.
- report: signal/web-automation/coder-report-TASK-013-B.md

- task_id: TASK-013-A
- status: DONE (Coder rate-limit 시점은 보고서 완료 후)
- completed_at: 2026-04-22T11:47
- assignee: coder
- summary: `src/sites/tistory/writer.py` 신규 388줄. 클래스 `TistoryWriter(config, browser)` + 6단계 async 메서드(open_newpost/fill_title/set_body_html/add_tags/select_category/attach_file/save_draft) + `run()` 진입점. TinyMCE setContent 경유 HTML 주입 + getContent().length>0 검증. aria-label 완전일치 `re.compile(rf"^{re.escape(name)}$")` 3건(category L264·attach kind L317·save text L359). file_chooser 컨텍스트 매니저 순서. category_fallback 재시도 로직. mode=publish → NotImplementedError. DoD 9건 전수 통과 (import OK / py_compile OK / OCR 0 / re.compile 완전일치 3건 / expect_file_chooser 3건 / NotImplementedError 3건 / category_fallback 5건 / tistory_write_ 2건).
- report: signal/web-automation/coder-report-TASK-013-A.md

- task_id: TASK-013-C
- status: DONE (manager-inline)
- completed_at: 2026-04-22T12:10
- assignee: manager-inline
- summary: `scripts/smoke_tistory_write.sh` + `smoke_tistory_write.py` 신규 2파일. bash wrapper 는 smoke_tistory_login.sh 구조 재사용 + samples/sample.txt 생성(idempotent). python 엔트리는 로그인→writer.run(제목/본문/태그/카테고리=메모+fallback=카테고리 없음/첨부=samples/sample.txt/mode=draft) 호출. 최종 스모크 exit 0.

- task_id: TASK-013-FIX
- status: DONE (manager-inline)
- completed_at: 2026-04-22T12:10
- assignee: manager-inline
- summary: 스모크 과정에서 writer.py 4건 + yaml 1건 즉시 수정. (1) attach_btn selector title="첨부"→aria-label="첨부" (TinyMCE 속성 차이 실측). (2) Playwright `:visible` pseudo 불안정 → count 루프 + is_visible() 로 변경. (3) 첨부 메뉴 innerText 에 NBSP(\xa0) prefix — Playwright has_text=regex(Python \s) 가 JS regex 변환 과정에서 NBSP 매치 실패 → has_text=substring 으로 전환 (현 UI 대상 문자열 "메모"/"카테고리 없음"/"파일"/"사진"/"슬라이드쇼"/"임시저장" 상호 substring 무충돌 확인). (4) `wait_for_load_state("networkidle")` — 티스토리 자동저장 백그라운드 요청으로 타임아웃 → PlaywrightTimeoutError 흡수 + asyncio.sleep 대체 (attach_file+save_draft 2곳). (5) run() 단계 순서 재조정: open→title→body→attach→tags→category→save (툴바 DOM 안정성).

- task_id: TASK-013-D
- status: WAITING_USER
- assignee: user
- summary: 사용자 육안 검증 대기 — 관리자 페이지 "임시저장된 글" 목록에서 `[스모크] 티스토리 자동화 테스트` 글 확인.

- task_id: TASK-013-IMG-SMOKE
- status: DONE (manager-inline)
- completed_at: 2026-04-22T12:32
- assignee: manager-inline
- summary: 이미지 업로드 스모크 추가 검증. 샘플 파일 `samples/sample.png` 신규 생성 (73 bytes, 2x2 빨간 RGB PNG, Python zlib+struct 로 직접 인코딩). writer.attach_file(path, kind="image") 경로 실행 — 전 단계 로그 정상 완료, 스크린샷에 2x2 빨간 점 본문 삽입 확인, 임시저장 카운트 3 증가 + "자동 저장 완료 12:32:06" 확증. TinyMCE 의 attach 메뉴 "사진" 옵션 경유 경로 정상 동작.

- task_id: TASK-025-PROBE
- status: DONE (manager-inline)
- completed_at: 2026-04-22T15:10
- summary: tistory 관리 API 3종 실측. attach.json(multipart, response key/url), drafts(JSON, draftSequence 멱등), 이미지 삭제 API 부재 확정. probe-tistory-api.md 에 curl 재현 가능한 스펙 기록.
- report: signal/web-automation/probe-tistory-api.md

- task_id: TASK-025-SETUP
- status: DONE (manager-inline)
- completed_at: 2026-04-22T15:35
- summary: requirements.txt 에 Pillow>=10.0.0 + markdown>=3.5 추가. pip install 후 import 검증 완료 (Pillow=12.2.0, markdown=3.10.2).

- task_id: TASK-025-A0
- status: DONE
- completed_at: 2026-04-22T15:45
- assignee: coder
- summary: `src/tistory_post/models.py` + `__init__.py` 신규. 6 dataclass (LoadedPost/Marker/UploadedImage/DraftPayload/RunResult) + PartialUploadError 예외 정의. probe-tistory-api.md 명명 엄격 준수 (content/categoryId/draftSequence camelCase). DoD 7/7 PASS. Python 3.11+ syntax (X|None, Literal[...]).
- report: signal/web-automation/coder-report-TASK-025-A0.md

- task_id: TASK-025-A
- status: DONE
- completed_at: 2026-04-22T15:55
- assignee: coder
- summary: `src/tistory_post/post_loader.py` 268줄 + `tests/test_post_loader.py` 14 함수. load_post() — .published skip, YAML frontmatter, `${N}`·`${filename}` 마커 파싱, 고아 마커/고아 이미지 검증. pytest 16 passed. DoD 7/7 PASS (ValueError raise 10건 ≥7, test 14 ≥10). 주의: `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` 필요 (anaconda base env 의 dash pytest plugin 충돌 — 후속 Tester/CI 태스크에서도 동일 flag 사용).
- report: signal/web-automation/coder-report-TASK-025-A.md

- task_id: TASK-025-B
- status: DONE
- completed_at: 2026-04-22T16:05
- assignee: coder
- summary: `src/tistory_post/image_uploader.py` 290줄. upload_images() 순차 업로드, k번째 실패 시 PartialUploadError(uploaded=k-1개, failed_index=k, cause=exc). page.evaluate + JS FormData + fetch credentials:include. multipart 필드명 probe `file`→`Filedata` + 모듈 전역 _SUCCESSFUL_FIELD_NAME cache. 매크로 조립 `[##_Image|kage@{key}?{escaped_query}|CDM|1.3|{json}_##]` + `&` → `&amp;` escape 1회. DoD 8/8 PASS. 이슈: probe 3단계 page.route 가로채기 MVP 미구현 (file/Filedata 둘 다 실패 시 별도 태스크 필요).
- report: signal/web-automation/coder-report-TASK-025-B.md

- task_id: TASK-025-CAT
- status: DONE (manager-inline)
- completed_at: 2026-04-22T16:10
- summary: `src/tistory_post/category_fetcher.py` 신규. fetch_category_map(page) — #category-btn 클릭 후 #category-list DOM 에서 `[aria-label][category-id]` 순회, `{name: int(id)}` dict 반환. 빈 리스트 폴백 `{"카테고리 없음":0}`. 호출 후 드롭다운 열린 상태 유지 (caller 책임). py_compile + import OK.

- task_id: TASK-025-D
- status: DONE (manager-inline)
- completed_at: 2026-04-22T16:12
- summary: `src/tistory_post/post_saver.py` 신규. save_draft(page, payload) — DraftPayload asdict + draftSequence=None 시 제거 + page.evaluate fetch('/manage/drafts', JSON body, credentials:include). HTTP non-2xx → RuntimeError. JSON parse 실패/success=false → RuntimeError. 응답 draft.sequence int 반환. py_compile + import OK.

- task_id: TASK-025-C
- status: DONE
- completed_at: 2026-04-22T16:25
- assignee: coder
- summary: `src/tistory_post/post_builder.py` 160줄 + `tests/test_post_builder.py` 8 함수. build_payload(post, uploads, category_map) + 3 private helper. Placeholder 우회 기법 (`@@TISTORY_MACRO_{uuid}@@`) 으로 매크로 내 `|`·`{`·`}`·`&amp;` markdown 파서 왜곡 방지. Marker.kind=filename 은 직접 lookup, index 는 sorted(images.keys())[N-1] (post_loader 와 동일 정렬). &amp; 재escape 금지 계약 준수. DoD 9/9 PASS, pytest 8/8.
- report: signal/web-automation/coder-report-TASK-025-C.md

- task_id: TASK-025-E
- status: DONE (manager-inline)
- completed_at: 2026-04-22T16:02
- summary: `src/tistory_post/post_runner.py` 신규. run_post(page, folder, blog_name) — load → category_fetch → image_upload → build → .draft_id 주입 → save_draft → .draft_id/.published 기록 + .error/.orphan.log cleanup. PartialUploadError catch → .orphan.log JSONL append + .error JSON. 다른 예외 → 업로드 완료분 orphan 처리 + .error. 수정: category_fetcher 가 blog_name 필수 인자 받도록 변경 (이전 page.url 파싱 버그 수정).

- task_id: TASK-025-F
- status: DONE (manager-inline)
- completed_at: 2026-04-22T16:02
- summary: `scripts/smoke_tistory_post.sh` + `smoke_tistory_post.py` + `posts/2026-04-22-sample/` (post.md + hello.png + image1.png 100x100). 실제 스모크 결과 **exit 0** (draft_sequence=24), 재실행 시 **exit 1 (.published skip)** 확증. orphan warning (image1.png 마커 미참조) 규칙대로 동작.

- task_id: TASK-025-G
- status: WAITING_USER
- summary: 사용자 육안 검증 대기 — 관리자 임시저장에서 `[Phase 7 스모크] 폴더 기반 자동화 테스트` draft 열기 → 제목·본문·카테고리(메모)·태그 3개·이미지 1개(hello.png 빨강 100x100) 확인.

- task_id: TASK-025-BUG-MACRO-PATH
- status: DONE (manager-inline)
- completed_at: 2026-04-22T16:30
- summary: 이미지 매크로 URL 경로 버그 수정. 원인: attach.json 응답의 `key` 필드에는 CDN 디렉토리 경로만 들어오고 실제 파일 이름(`img.png`)은 별도 `filename` 필드로 반환되는데, image_uploader 의 `_build_macro` 가 `kage@{key}?{query}` 로 파일명 없이 조립해 tistory 에디터가 렌더 실패. 수정: `kage@{key}/{cdn_filename}?{query}` 형태로 변경 (`cdn_filename=response["filename"]` 주입). 추가: autosave race 조사 중 부산물로 `save_draft` 가 fetch 성공 직후 `page.goto("about:blank")` 로 autosave 타이머 차단. **검증**: 스모크 재실행 → draft sequence 27 생성 → `GET /manage/drafts/27` 조회 → content_len=843, 매크로 2개 `kage@.../img.png?credential=...` 형식 확증. Phase 3 autosave 매크로 포맷과 완전 일치.

- task_id: TASK-025-IMGS-DIR
- status: DONE (manager-inline)
- completed_at: 2026-04-22T16:20
- summary: 사용자 요청 반영. `post_loader._collect_images` 가 `{folder}/imgs/` 가 있으면 거기서만, 없으면 기존 `{folder}/` 바로 아래에서 수집 (하위 호환). 샘플 폴더 `posts/2026-04-22-sample/` 도 `imgs/` 구조로 재배치. architecture.md §7 입력 규격 예시도 `imgs/` 서브폴더 권장 방식으로 후속 반영 필요.

- task_id: TASK-025-G
- status: DONE (user verified)
- completed_at: 2026-04-22T16:35
- summary: 사용자 육안 검증 완료. draft sequence 27 확인 — 이미지 2군데 (빨간 100x100 hello.png) 본문 중간 위치에 정상 표시. 제목·본문·카테고리(메모)·태그 3개·굵은/기울임/리스트 포맷 모두 정상. Phase 7 폴더 기반 임시저장 자동화 MVP 전 기능 완성.
