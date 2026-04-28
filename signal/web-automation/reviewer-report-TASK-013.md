---
task_id: TASK-013(A/B/C/D 세분화군)
verdict: PASS
---

# Reviewer Report: TASK-013 (writer.py 글쓰기 자동화 세분화) — 재검증 2회차

## 검증 대상
- `signal/web-automation/task-board.md` L31-L35 (TASK-013 SPLIT / TASK-013-A / TASK-013-B / TASK-013-C / TASK-013-D) — Manager 가 직전 10건 NEEDS_REVISION 을 반영해 패치한 뒤 재검증 요청
- 참조(수정 불필요): `projects/web-automation/src/sites/tistory/login.py` / `config/tistory.yaml` / `scripts/smoke_tistory_login.sh`
- 이전 보고서: 이 파일의 직전 버전 (NEEDS_REVISION, 10건)

### Manager 주장 요약 (패치 후)
1. yaml 기존 3키 처리 택B 확정 (덮어쓰기/삭제/rename) + 5개 grep 완료 조건 명시
2. attach_file kind 매칭 `re.compile(rf"^{re.escape(...)}$")` 완전일치
3. file_chooser `async with page.expect_file_chooser()` 컨텍스트 매니저 순서 본문 삽입
4. save_draft 판정 택B 단순화 (networkidle + sleep(2), 예외 없으면 True)
5. set_body_html 후 `wait_for_function("() => window.tinymce.activeEditor.getContent().length > 0")` 검증 추가
6. `_STEP_TIMEOUT_MS = 15000` + `_screenshot_on_error` writer.py 에 login.py 복제 명시
7. add_tags `await page.wait_for_timeout(200)` 확정 대기
8. mode=publish → `NotImplementedError("publish mode 는 후속 태스크에서 구현")`
9. samples/sample.txt 생성 책임을 bash wrapper 에 고정 (mkdir -p samples + echo 1줄)
10. category_fallback 을 writer.run() 인자로 추가, 스모크 entry 에서 전달

---

## 검증 결과 (10건 grep 실증)

### #1 yaml 기존 3키 처리 (택B 확정) — 반영 확인
- `write_title_input: ""` 의 **값**을 `'textarea#post-title-inp'` 로 **덮어쓰기** → 문자열 일치 확인.
  - grep `write_title_input.*덮어쓰기` → 1 hit.
- `write_content_area: ""` **삭제** → 문자열 일치 확인.
  - grep `write_content_area.*삭제` → 1 hit.
- `write_publish_button` 의 **key 이름을 `publish_btn` 으로 rename** → 문자열 일치 확인.
  - grep `publish_btn.*rename` → 1 hit (rename** + 값 `'button#publish-layer-btn'` 주입).
- 완료 조건 5개 grep 명시 전부 확인:
  - (1) `python3 -c "import yaml; yaml.safe_load(open('config/tistory.yaml'))"` 파싱 성공 — grep `yaml.safe_load` → 1 hit
  - (2) `grep -cE '^\s*write_content_area:' config/tistory.yaml` → **0** — 본문 내 "**0** (삭제" 문자열 포함 확인
  - (3) `grep -cE '^\s*write_publish_button:' config/tistory.yaml` → **0** — "**0** (rename" 문자열 포함 확인
  - (4) `grep -cE '^\s*publish_btn:' config/tistory.yaml` → **1** — "**1**" 문자열 포함 확인
  - (5) "공유 10개 key 각각 grep 으로 1 hit 실증" — grep `10.{0,4}key.{0,4}grep` → `10개 key 각각 grep` 1 hit
- **#1 PASS**.

### #2 attach_file kind 매칭 완전일치 — 반영 확인
- `re.compile(rf"^{re.escape(text_for_kind)}$")` 문자열 정확 일치 (grep 결과 1 hit).
- "substring 오매치 방지 — `:has-text("파일")` 은 '슬라이드쇼 파일' 같은 조합에 오매치 가능" 경고 문구 본문 삽입 확인 (grep 1 hit).
- `select_category` 에서도 동일 패턴(`re.compile(rf"^{re.escape(name)}$")`) + "aria-label 부분일치 위험 차단" 적용 — 추가 강화.
- **#2 PASS**.

### #3 file_chooser 컨텍스트 매니저 순서 본문 삽입 — 반영 확인
- `async with page.expect_file_chooser() as fc_info` 문자열 1 hit.
- `chooser = await fc_info.value` 문자열 1 hit.
- `chooser.set_files` 문자열 1 hit.
- 본문 코드 순서: `menu_item = page.locator(...)` → `async with page.expect_file_chooser() as fc_info: await menu_item.first.click()` → `chooser = await fc_info.value` → `await chooser.set_files(str(Path(path).resolve()))` 로 정확히 기재.
- "**file_chooser 순서 중요** — 아래 코드 블록 순서 그대로 구현" 경고 문구 포함.
- **#3 PASS**.

### #4 save_draft 판정 (택B 단순화) — 반영 확인
- "성공 판정 단순화 (Reviewer #4 택B)" 문자열 명시.
- 클릭 → `wait_for_load_state("networkidle", timeout=_STEP_TIMEOUT_MS)` → `asyncio.sleep(2)` 순서 본문 포함 (grep `networkidle.*asyncio.sleep\(2\)` 1 hit).
- "예외 없이 종료되면 True 반환" 명시 (grep 1 hit).
- "실제 임시저장 성공 여부는 TASK-013-D (사용자 육안 검증) 에서 확인" 명시 (grep `사용자 육안 검증` 2 hit — TASK-013-A 본문 + TASK-013-D 타이틀).
- **#4 PASS**.

### #5 set_body_html 후 검증 — 반영 확인
- `wait_for_function("() => window.tinymce.activeEditor.getContent().length > 0", timeout=_STEP_TIMEOUT_MS)` 정확 삽입 (grep 1 hit).
- "실측: 티스토리 스킨이 `data-ke-size` 등 속성 자동 추가하나 HTML 구조/텍스트 보존" 근거 포함.
- **#5 PASS**.

### #6 `_STEP_TIMEOUT_MS` + `_screenshot_on_error` writer.py 재정의 — 반영 확인
- "모듈 상단 상수/헬퍼 재정의 (login.py 복제, 간단 경로)" 명시.
- `_STEP_TIMEOUT_MS = 15000` 정의 grep 1 hit.
- `_screenshot_on_error(self, step: str)` 와 "login.py 의 동일 로직 복제, 향후 공통 모듈 추출은 별도 리팩터 태스크" 문자열 포함.
- grep `login\.py 복제` → 1 hit.
- **#6 PASS**.

### #7 add_tags 확정 대기 — 반영 확인
- `await page.wait_for_timeout(200)` + "(태그 칩 렌더 대기)" 본문 포함 (grep `page.wait_for_timeout\(200\)` 1 hit).
- **#7 PASS**.

### #8 mode="publish" → NotImplementedError — 반영 확인
- `raise NotImplementedError("publish mode 는 후속 태스크에서 구현")` 정확 문자열 (grep `NotImplementedError\("publish mode` 1 hit).
- "(silently skip 금지)" 경고 포함.
- **#8 PASS**.

### #9 samples/sample.txt 생성 책임 (bash wrapper 고정) — 반영 확인
- TASK-013-C 본문 "샘플 파일 생성은 bash wrapper 책임 (Reviewer #9 확정)" 명시 (grep 1 hit).
- `.env` 로드 직후 `mkdir -p samples && [ -f samples/sample.txt ] || echo '테스트 첨부파일 — 티스토리 스모크' > samples/sample.txt` 한 줄 명시 (grep `mkdir -p samples` 1 hit).
- **#9 PASS**.

### #10 카테고리 fallback 위치 확정 — 반영 확인
- TASK-013-A `run()` 시그니처: `async def run(self, *, title, body_html, tags=None, category=None, category_fallback: str | None = None, attachments=None, mode="draft") -> bool` 에서 `category_fallback: str \| None = None` 확인 (grep 1 hit — md 파이프 이스케이프 `\|` 포함).
- "**category_fallback 동작** (Reviewer #10): `select_category(category)` 가 ValueError 시 `category_fallback` 이 None 이 아니면 `select_category(category_fallback)` 재시도, 그것도 실패면 최종 raise" 본문 명시 (grep `select_category\(category_fallback\)` 1 hit).
- TASK-013-C 스모크 entry 가 `category="메모"` + `category_fallback="카테고리 없음"` 전달만 수행 (try/except 금지) 명시 — "스모크 자체에 try/except 금지" 문구 확인.
- **#10 PASS**.

---

## 의존성·순서·범위 재확인

- TASK-013 SPLIT 상태. 하위 4개 태스크 (013-A/B/C/D) 의존 관계:
  - 013-A (writer.py) — Depends: (없음, TASK-012 는 상위 TASK-013 에 있으며 DONE)
  - 013-B (tistory.yaml) — Depends: (없음)
  - 013-C (스모크 스크립트) — Depends: TASK-013-A, TASK-013-B
  - 013-D (사용자 육안) — Depends: TASK-013-C
- 013-A 와 013-B 는 **다른 파일**(writer.py vs tistory.yaml) 수정이므로 **병렬 실행 가능**.
- **Config key 계약 10개가 양쪽에 원자적으로 동일 명시**됨 — 병렬 실행 시 정합 리스크 없음.
- 013-C 는 반드시 A+B DONE 후 실행.
- 013-D 는 사용자 Execution (manager 자동 실행 금지).

## 판정
**PASS**

10건 수정 요청 모두 task-board.md L31~L35 에 구체·정확 반영됨. grep 으로 핵심 문자열(`re.compile(rf"^{re.escape(...)}$")`, `async with page.expect_file_chooser() as fc_info`, `NotImplementedError("publish mode`, `category_fallback: str \| None = None`, `mkdir -p samples`, `_STEP_TIMEOUT_MS = 15000`, `page.wait_for_timeout(200)`, `networkidle.*asyncio.sleep(2)`, `wait_for_function` getContent, yaml 5개 완료 조건) 전부 일치 확인.

## Manager에게 전달

**Coder 호출 전략 권장**:
1. **TASK-013-A 와 TASK-013-B 를 병렬 호출** (서로 다른 파일, 공유 Config key 계약이 이미 원자적으로 동기화됨). 각 태스크별 report 파일 사용:
   - `signal/web-automation/coder-report-TASK-013-A.md`
   - `signal/web-automation/coder-report-TASK-013-B.md`
2. 두 태스크 모두 DONE 확인 후 **TASK-013-C 를 순차 호출** (`signal/web-automation/coder-report-TASK-013-C.md`). TASK-013-C 는 TASK-013-A 가 생성한 writer.py 와 TASK-013-B 가 갱신한 tistory.yaml 에 의존하므로 반드시 선행 태스크 DONE 후 실행.
3. TASK-013-C DONE 후 **TASK-013-D 는 사용자에게 manual 실행 가이드 전달** (Execution=user). `./scripts/smoke_tistory_write.sh` 실행 + 관리 페이지 '임시저장된 글' 목록 확인 안내.

**추가 조언**: TASK-013-A/B/C 는 지시가 매우 조밀하므로 Coder 가 중간에 모호한 부분을 만나면 즉시 리포트 + 중단하도록 coder.md 의 기본 원칙(임의 추측 금지)을 한 번 더 강조할 것.
