---
agent: tester
task_id: TASK-210-T
status: DONE
timestamp: 2026-04-27T11:40:00+09:00
severity: observation
---

## 결과 요약

Phase A (`/exam`, `/exam/{year}-{slot}`) 통합 + 회귀 테스트 33건을 `tests/test_web_exam.py` 신규 작성하여 전수 PASS (33/33). TASK-208 markdown_renderer 5/5 회귀 PASS 동시 확증 (총 38 PASS). byte-level verbatim 5종 ±0 (3 연도 × 2 docs × 5 클래스 = 30 assertion) 무위반. 회귀 6 라우트 200 + invariant 무영향. ES 차단 시에도 `/exam` 200 (route ES 의존 0건 확증). 클린 코드 관점에서는 `view_exam` 함수 길이 (40L) 와 `<title>` baseline 의 spec 표현 부정확 등 minor observation 만 있고 blocker/bug 없음.

## 변경된 파일

- `projects/ethics-study/tests/test_web_exam.py` (신규 332L · pytest 33 테스트 · FastAPI TestClient + BeautifulSoup4 + monkeypatch)

## 테스트 결과

```
$ PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_web_exam.py -v
============================= test session starts ==============================
platform linux -- Python 3.11.3, pytest-9.0.2, pluggy-1.6.0
collected 33 items

tests/test_web_exam.py::test_exam_index_200_and_26_links PASSED          [  3%]
tests/test_web_exam.py::test_exam_detail_200[2014-A] PASSED              [  6%]
tests/test_web_exam.py::test_exam_detail_200[2025-B] PASSED              [  9%]
tests/test_web_exam.py::test_exam_detail_200[2026-A] PASSED              [ 12%]
tests/test_web_exam.py::test_exam_detail_404[9999-A] PASSED              [ 15%]
tests/test_web_exam.py::test_exam_detail_404[2014-Z] PASSED              [ 18%]
tests/test_web_exam.py::test_exam_detail_404[abcd-A] PASSED              [ 21%]
tests/test_web_exam.py::test_verbatim_zero_diff_per_year[2014-A] PASSED  [ 24%]
tests/test_web_exam.py::test_verbatim_zero_diff_per_year[2025-B] PASSED  [ 27%]
tests/test_web_exam.py::test_verbatim_zero_diff_per_year[2026-A] PASSED  [ 30%]
tests/test_web_exam.py::test_hexdump_em_dash_present PASSED              [ 33%]
tests/test_web_exam.py::test_hexdump_cjk_zhu_present PASSED              [ 36%]
tests/test_web_exam.py::test_hexdump_circled_present PASSED              [ 39%]
tests/test_web_exam.py::test_regression_route_200[/] PASSED              [ 42%]
tests/test_web_exam.py::test_regression_route_200[/thinker/kant] PASSED  [ 45%]
tests/test_web_exam.py::test_regression_route_200[/thinker/aristotle] PASSED [ 48%]
tests/test_web_exam.py::test_regression_route_200[/search?q=kant] PASSED [ 51%]
tests/test_web_exam.py::test_regression_route_200[/api/thinkers] PASSED  [ 54%]
tests/test_web_exam.py::test_regression_route_200[/api/thinker/kant] PASSED [ 57%]
tests/test_web_exam.py::test_regression_route_200[/api/search?q=kant] PASSED [ 60%]
tests/test_web_exam.py::test_regression_html_invariants[/] PASSED        [ 63%]
tests/test_web_exam.py::test_regression_html_invariants[/thinker/kant] PASSED [ 66%]
tests/test_web_exam.py::test_regression_html_invariants[/thinker/aristotle] PASSED [ 69%]
tests/test_web_exam.py::test_regression_html_invariants[/search?q=kant] PASSED [ 72%]
tests/test_web_exam.py::test_api_thinkers_total_baseline PASSED          [ 75%]
tests/test_web_exam.py::test_index_tab_btn_baseline PASSED               [ 78%]
tests/test_web_exam.py::test_search_tab_btn_baseline PASSED              [ 81%]
tests/test_web_exam.py::test_exam_route_works_when_es_blocked PASSED     [ 84%]
tests/test_web_exam.py::test_css_exam_prefix_count_37 PASSED             [ 87%]
tests/test_web_exam.py::test_css_tab_btn_baseline_count_5 PASSED         [ 90%]
tests/test_web_exam.py::test_css_existing_first_1000_lines_unchanged PASSED [ 93%]
tests/test_web_exam.py::test_toc_regex_total_293 PASSED                  [ 96%]
tests/test_web_exam.py::test_task_208_markdown_renderer_regression PASSED [100%]

============================== 33 passed in 1.72s ==============================
```

- 통과: 33
- 실패: 0
- 실패 상세: 없음

병합 실행 (TASK-208 회귀 동시):
```
$ PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_web_exam.py tests/test_markdown_renderer.py -v
============================== 38 passed in 1.72s ==============================
```

## 항목별 PASS/FAIL (11항)

| # | 항목 | 결과 | 비고 |
|---|------|------|------|
| 1 | GET `/exam` 200 + 26 link | PASS | 13 년 × A/B = 26 unique href, expected set 일치 |
| 2 | GET `/exam/{2026-A,2014-A,2025-B}` 각 200 | PASS | 3/3 200 |
| 3 | GET `/exam/{9999-A,2014-Z,abcd-A}` 404 | PASS | 9999 (포맷 OK · 파일 부재) → FileNotFoundError 404, 2014-Z (slot 위반) → regex 404, abcd-A (year 위반) → regex 404 |
| 4 | byte-level verbatim 3 연도 × 2 docs × 5 클래스 = 30 assertion ±0 | PASS | `<article class="exam-tab-content">` 추출 후 `verify_verbatim()` ±0 일치 (BeautifulSoup) |
| 5 | hexdump em-dash `e2 80 94` · 朱 `e6 9c b1` · ㉠ `e3 89 a0` /exam/2026-A body 1+ 회 | PASS | em-dash 685 회 · 朱 2 회 · ㉠ 197 회 등장 |
| 6 | 회귀 7 라우트 200 + invariant | PASS | 7 라우트 모두 200, 4 HTML 라우트 `lang="ko"` + `<title>` 에 `윤리`·`가이드` 포함 |
| 7 | 분야별 탭 회귀 `/`=4btn/0cnt · `/search?q=kant`=2btn/2cnt | PASS | BeautifulSoup `select('button.tab-btn')`/`.tab-count` 카운트 baseline 일치 |
| 8 | ES 차단 시 `/exam/2026-A` 200 | PASS | `monkeypatch.setattr(app, 'es', _BrokenES())` 적용 후 `/exam/2026-A` · `/exam` 모두 200 |
| 9 | CSS prefix 격리 (.exam=37, .tab-(btn\|count)=5, exam selectors 모두 >L1000) | PASS | 실측 37/5 + min exam line=1004>1000 |
| 10 | TOC 정규식 26 study-guide 합 = 293 | PASS | `re.MULTILINE` `^## 문항(?:\s+(?:서술형\|논술형\|기입형))?\s+\d+` 합 293 일치 |
| 11 | TASK-208 회귀 (test_markdown_renderer 5/5) | PASS | subprocess 격리 실행 5/5 PASS · 통합 실행에서도 5/5 |

## byte-level 5종 카운트 표 (3 연도)

각 행 `M/H` 표기 (M=md count, H=html article body count, ±0).

| 연도 | doc | em_dash | cjk | circled | greek | german |
|------|-----|---------|-----|---------|-------|--------|
| 2014-A | study-guide | 47/47 | 226/226 | 21/21 | 0/0 | 0/0 |
| 2014-A | coverage    | 41/41 | 155/155 | 15/15 | 0/0 | 0/0 |
| 2025-B | study-guide | 211/211 | 1155/1155 | 424/424 | 0/0 | 2/2 |
| 2025-B | coverage    | 112/112 | 499/499 | 107/107 | 0/0 | 0/0 |
| 2026-A | study-guide | 335/335 | 1652/1652 | 283/283 | 212/212 | 21/21 |
| 2026-A | coverage    | 349/349 | 1365/1365 | 264/264 | 0/0 | 10/10 |

총 30 assertion 모두 ±0. (Coder report 표와 일치.)

## hexdump 샘플

`/exam/2026-A` 응답 raw bytes (TestClient `r.content`) 검사:

| 클래스 | UTF-8 byte | 등장 횟수 | 비고 |
|--------|------------|-----------|------|
| em-dash (U+2014) | `e2 80 94` | 685 | study-guide 335 + coverage 349 + base.html footer `&mdash;` 1 |
| CJK 朱 (U+6731) | `e6 9c b1` | 2 | 朱熹 (2026-A coverage) |
| 원문자 ㉠ (U+3260) | `e3 89 a0` | 197 | 원문자 6 종 합산 일부 |

bytes-in 검증식 (재현 가능):
```python
r = client.get("/exam/2026-A")
assert b"\xe2\x80\x94" in r.content  # em-dash
assert b"\xe6\x9c\xb1" in r.content  # 朱
assert b"\xe3\x89\xa0" in r.content  # ㉠
```

## 회귀 7 라우트 invariant 결과

| 라우트 | status | `<title>` (실측) | `<html lang>` | 핵심 baseline |
|--------|--------|-------------------|----------------|----------------|
| `/` | 200 | `사상가 목록 — 윤리 학습 가이드` | ko | tab-btn buttons=4, tab-count=0 |
| `/thinker/kant` | 200 | `임마누엘 칸트 — 윤리 학습 가이드` | ko | (탭 미사용) |
| `/thinker/aristotle` | 200 | `아리스토텔레스 — 윤리 학습 가이드` | ko | (탭 미사용) |
| `/search?q=kant` | 200 | `kant 검색 결과 — 윤리 학습 가이드` (개행 포함) | ko | tab-btn buttons=2, tab-count=2 |
| `/api/thinkers` | 200 | (JSON) | (n/a) | total = 67 (≥60 baseline) |
| `/api/thinker/kant` | 200 | (JSON) | (n/a) | thinker · works · claims · keywords · relations 키 5종 |
| `/api/search?q=kant` | 200 | (JSON) | (n/a) | results 구조 무변동 |

**중요 정정**: TASK-210-T spec 본문 "`<title>윤리 임용시험 학습 가이드</title>` 무변동" 은 **부정확**. 모든 페이지가 base.html 의 `{% block title %}` 을 override 하므로 정확한 invariant 는 (a) `<html lang="ko">` 존재, (b) title 에 `윤리` 와 `가이드` 토큰 포함. 본 테스트는 이 invariant 로 검증.

## 분야별 탭 회귀

| 라우트 | `button.tab-btn` selector | `.tab-count` selector | baseline 일치 |
|--------|---------------------------|------------------------|---------------|
| `/` (index.html) | 4 | 0 | OK |
| `/search?q=kant` (search.html) | 2 | 2 | OK |

(BeautifulSoup `soup.select(...)` 사용 — Coder report 의 raw-string 카운트는 JS 코드 안의 `.tab-btn` literal selector 1건을 포함해 3 으로 잡혔으나, **DOM 요소 카운트** 는 2 가 정확. baseline 일치 확인.)

## ES 차단 시나리오

```python
class _BrokenES:
    def __getattr__(self, name):
        def _raise(*a, **kw):
            raise ConnectionError(f"ES is down (mock); called .{name}")
        return _raise

def test_exam_route_works_when_es_blocked(monkeypatch):
    monkeypatch.setattr(app_module, "es", _BrokenES())
    local = TestClient(app)
    assert local.get("/exam/2026-A").status_code == 200  # PASS
    assert local.get("/exam").status_code == 200          # PASS
```

`/exam` 라우트 2종 모두 ES 의존 0건 확증. `view_exam`/`list_exams` body 가 `es` 객체를 한 번도 참조하지 않음 (Coder report 다음 제안 §5 와 일치).

## CSS prefix 격리

| 검증 | 명령/결과 |
|------|------------|
| 신규 `.exam-` selector 카운트 | `grep -cE '^\.exam-' style.css` → **37** |
| 기존 `.tab-(btn\|count)` baseline | `grep -cE '^\.tab-(btn\|count)' style.css` → **5** (변동 0) |
| `.exam-*` selector 모두 line >1000 | min(`.exam-` 시작 line) = **L1004** > 1000 |
| 기존 1000L 영역 byte-level 무수정 | Coder report 인용: `git diff --stat` 99/255 insertions, 0 deletions (style.css) |

**spec 표현 정정**: TASK-210-T spec 의 `grep -nE '\.exam-(tab-btn|tab-count|toc)' style.css # 0-hit expected` 는 **모순**. 신규 클래스 `.exam-tab-btn`·`.exam-toc*` 자체가 정상적으로 존재해야 하므로 (Coder 가 만든 신규 selector) 0-hit 일 수 없음. 실측 11 hit (L1139·L1153·L1157·L1205·L1216·L1220·L1227·L1233·L1239·L1250 — 모두 L1000+ 신규 영역). 본 의도는 "기존 `.tab-btn`/`.tab-count` selector 영역 침범 0건" 이며, 이는 (a) baseline 5 unchanged + (b) 신규 selector 가 모두 L1000+ 두 검증으로 충분히 보장. → severity=observation, spec 문구 수정 권고.

## TOC 정규식 검증 재현

```python
pat = re.compile(r"^## 문항(?:\s+(?:서술형|논술형|기입형))?\s+\d+", re.MULTILINE)
files = sorted(SG_DIR.glob("*.md"))
assert len(files) == 26
total = sum(len(pat.findall(p.read_text(encoding="utf-8"))) for p in files)
assert total == 293  # PASS
```

26 study-guide 파일, hit 합 = **293** (= `exam-coverage-map.md` L8 "총 문항 row 수: 293" 일치). PASS.

## TASK-208 회귀

```
$ PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_markdown_renderer.py -v
tests/test_markdown_renderer.py::test_render_preserves_cjk_bytes PASSED
tests/test_markdown_renderer.py::test_verify_verbatim_all_zero_diff PASSED
tests/test_markdown_renderer.py::test_render_block_elements_intact PASSED
tests/test_markdown_renderer.py::test_typographer_on_breaks_verbatim PASSED
tests/test_markdown_renderer.py::test_raw_html_is_escaped_for_security PASSED
============================== 5 passed in 0.02s ===============================
```

5/5 PASS. test_web_exam.py 의 `test_task_208_markdown_renderer_regression` 도 subprocess 격리 실행으로 동일 결과 확증.

## 클린 코드/아키텍처 관점 평가 (Coder TASK-209 산출물 대상)

| 원칙 | 평가 | 비고 |
|------|------|------|
| 1. 계층 의존 (route → markdown_renderer → file read 단방향) | OK | `view_exam`/`list_exams` body 가 `es` 객체 참조 0건 (ES mock test PASS 로 실증). `markdown_renderer.py` import 라인은 `re` + `markdown_it.MarkdownIt` 만. |
| 2. 단일 책임 (helper 분리) | OK | `_list_exam_keys` (디렉토리 fs scan) · `_read_exam_md` (단일 파일 read) · `_extract_toc` (정규식 추출) · `_log_verbatim` (logging 분기) · 각각 1 가지 책임. |
| 3. 함수 과대 (40L 초과 시 observation) | observation | `view_exam` 본문 = 38 statement (L432-L470, 39L) — 임계값 40 미만이지만 인접. 라우트 핸들러가 (a) regex 매칭, (b) md 2 회 read, (c) 2 회 render, (d) 2 회 verbatim log, (e) toc 추출, (f) nav list, (g) template 응답 7 단계를 한 함수에서 처리. 향후 Phase B (검색 통합) 추가 시 분리 권고. blocker 아님. |
| 4. 이름·주석 (의도 드러내기, magic constant 처리) | OK | `_log_verbatim` 분기 (mismatch → WARNING, OK → INFO) 의도 명확. `_TOC_PATTERN` 의 변종 흡수 의도 (서술형/논술형/기입형) 주석 명시. magic constant `_EXAM_KEY_RE` 모듈 상수로 분리. |
| 5. DTO ↔ Entity 분리 | n/a | Phase A 는 dict 기반 응답 (entries · nav_keys · toc) 이라 DTO 분리 의무 약함. Coder report §클린 코드 체크 와 동일 판정. |

총평: blocker/bug 없음. observation 1건 (`view_exam` 함수 길이 임계 근접) — Phase B 진입 시 검토 권고.

## 이슈/블로커

**없음** (severity=observation 만 해당).

세부 observation:

1. **spec 문구 부정확** (severity=observation): TASK-210-T 스펙 본문의 두 표현이 실제 구현과 부합하지 않음.
   (a) "`<title>윤리 임용시험 학습 가이드</title>` 무변동" — 모든 페이지가 block title 을 override 함. 본 테스트는 더 정확한 invariant (`<html lang="ko">` + title 에 `윤리`·`가이드` 포함) 로 대체.
   (b) "`grep -nE '\.exam-(tab-btn|tab-count|toc)' style.css # 0-hit expected`" — 신규 클래스 `.exam-tab-btn`/`.exam-toc*` 자체가 정상 존재해야 하므로 0-hit 일 수 없음. 실측 11 hit (모두 L1000+ 신규 영역 · 충돌 없음). 본 테스트는 (a) `.exam-` 카운트 == 37, (b) `.tab-(btn|count)` baseline == 5, (c) min(`.exam-` line) > 1000 세 가지로 격리 실증.
   → Manager 가 architecture/task-board spec 갱신 사이클에서 문구 정정 권고.

2. **`view_exam` 함수 길이 39L** (severity=observation): SRP 임계 근접. Phase B 검색 통합 시 `_resolve_exam_payload(year, slot)` helper 분리 권고. 현 단계에서는 helper 4 개 + 라우트 핸들러 응집도 양호로 유지 가능.

3. **uvicorn standalone logger 미보임** (severity=observation, Coder report §1 와 동일): TASK-209 Coder report 의 운영 환경 로깅 이슈. Phase A 범위 외이며 본 테스트(TestClient)에서는 무관. 운영 단계 별도 task 권고.

## 다음 제안 (TASK-211 Manual UX)

1. **브라우저 확인 항목** (TASK-211 Execution=user):
   - `cd projects/ethics-study/web && uvicorn app:app --host 0.0.0.0 --port 8000`
   - `http://localhost:8000/exam` 카드 그리드 26 entry 시각 확인.
   - 한 카드 (예: 2026-A) click → `/exam/2026-A` 진입.
   - study-guide ↔ coverage 탭 전환 매끄러움 확인 (JS `.exam-tab-bar` 핸들러 동작).
   - TOC `목차 (12)` 영역 study-guide 활성 시만 표시 · coverage 활성 시 숨김 동작 확인 (JS toc visibility 동기).
   - 사이드바 다른 연도 click → 페이지 전환 (a tag link 이므로 server-side render).
   - 한자 `朱熹` · em-dash `—` · 원문자 `㉠~㉥` · 독일어 `Würde` 시각 정상 (typographer OFF 효과).
   - `/`, `/thinker/kant`, `/search?q=kant` 시각 회귀 없음 (이미 본 테스트로 라우트 200 + invariant 확증).

2. **Phase B 진입 전 권고**:
   - `view_exam` 함수 분리 검토 (≥40L 임계 진입 가능성).
   - 운영 환경 logging 설정 추가 (`uvicorn --log-config` 또는 `app.py` basicConfig 호출).
   - 본 테스트의 `test_task_208_markdown_renderer_regression` subprocess 호출 패턴은 추후 conftest 또는 CI fixture 로 추출 가능.

3. **spec 문구 정정** (Manager 처리 권고):
   - architecture.md / task-board.md 의 `<title>윤리 임용시험 학습 가이드</title>` 무변동 문구 → "모든 HTML 라우트 `<html lang="ko">` 유지 + `<title>` 에 `윤리`·`가이드` 토큰 포함" 으로 수정.
   - `\.exam-(tab-btn|tab-count|toc)` 0-hit 표현 → "`.exam-` 신규 selector 모두 L1000+ 영역 + 기존 `.tab-(btn|count)` baseline 5 unchanged" 로 수정.
