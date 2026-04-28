---
agent: coder
task_id: TASK-208
status: DONE
timestamp: 2026-04-27T10:30
---

## 결과 요약
`web/markdown_renderer.py` 신규 작성 (render + verify_verbatim 함수 분리, ES·HTTP·DB 의존 0건). pytest 5종 전수 통과 (한자 보존·5종 ±0·블록 요소·typographer ON 부정 케이스·raw HTML escape).

## 변경된 파일
- `projects/ethics-study/web/markdown_renderer.py` (신규, 95L)
- `projects/ethics-study/tests/test_markdown_renderer.py` (신규, 약 110L)
- `projects/ethics-study/requirements.txt` (수정 — `markdown-it-py>=2.2.0` 라인 추가)

## 라이브러리 선택 근거
**markdown-it-py 채택.**

비교 (1줄+ 근거):
- **markdown-it-py**: CommonMark 준수 · `typographer` 옵션을 명시적으로 토글 가능 (`MarkdownIt({"typographer": False})`) + `replacements`/`smartquotes` rule 을 `disable()` 로 끌 수 있어 byte-level verbatim 가능. `enable("table")` 로 GFM table 활성. 환경에 이미 v2.2.0 설치되어 있어 즉시 import 가능.
- python-markdown: smarty extension 미포함 시 typographic substitution OFF 가능하지만 GFM table 지원이 별도 extension (`tables`) 필요하고 default rule set 이 markdown-it-py 보다 byte-level 제어가 덜 explicit.
- mistune: 빠르지만 typographer rule 의 명시적 토글 API 가 약함.

→ markdown-it-py 가 **typographer 토글의 명시성** + **GFM table 내장** + **이미 설치됨** 3박자로 선정.

설치 버전 caveat: 환경 사전 설치 버전 = **2.2.0** (`python -c "import markdown_it; print(markdown_it.__version__)"` → `2.2.0`). architecture.md L400 / task-board.md TASK-208 row 는 `>=3.0.0` 권장이나, 사용한 API (`MarkdownIt(...).enable("table").disable([...])`) 는 v2.x 부터 동일 동작이라 기능 충족. requirements.txt 는 안전하게 `>=2.2.0` 으로 기재 (실측 import smoke test 통과).

## typographer OFF 검증
`web/markdown_renderer.py` L20-L25 (모듈 레벨 단일 인스턴스):

```python
_MD = (
    MarkdownIt("commonmark", {"typographer": False, "html": False, "linkify": False})
    .enable("table")
    .disable(["replacements", "smartquotes", "linkify"])
)
```

3중 방어선:
1. **`typographer: False`** — markdown-it-py 의 master switch (typographer rule group OFF).
2. **`disable(["replacements", "smartquotes"])`** — 만에 하나 master switch 가 무시되어도 개별 rule 도 명시 비활성. `replacements` 는 `---` → em-dash · `...` → ellipsis 변환 담당, `smartquotes` 는 ASCII quote 의 typographic 변환 담당.
3. **`html: False`** — raw HTML inline OFF (XSS 방어 + escape 후 텍스트 노드로 잡혀 verify_verbatim 카운트 일관).

부정 케이스 검증 (test 4 `test_typographer_on_breaks_verbatim`): `MarkdownIt("commonmark", {"typographer": True}).enable(["replacements", "smartquotes"])` 로 인스턴스화하면 `Hello --- world.` (em-dash 0건) 가 `<p>Hello — world.</p>` (em-dash 1건) 로 렌더되어 md 카운트 0 ≠ html 카운트 1 → 부정 케이스 통과 (불일치 검출 성공).

## 5종 verbatim 카운트 hexdump 샘플
| 클래스 | 대표 문자 | 코드포인트 | UTF-8 byte |
|--------|-----------|------------|------------|
| em_dash | — | U+2014 | `e2 80 94` |
| cjk | 朱 | U+6731 | `e6 9c b1` |
| circled_digits | ㉠ | U+3260 | `e3 89 a0` |
| greek_lower | ν | U+03BD | `ce bd` |
| german | ü | U+00FC | `c3 bc` |

검증 명령 (재현 가능):
```bash
python3 -c "
for name, ch in [('em-dash','—'),('CJK 朱','朱'),('circled ㉠','㉠'),('greek ν','ν'),('german ü','ü')]:
    print(name, ' '.join(f'{b:02x}' for b in ch.encode('utf-8')))
"
```

**원문자 코드포인트 spec 충돌 발견 (이슈로 별도 명시).** architecture.md L420 은 `㉠㉡㉢㉣㉤㉥` 의 codepoint range 를 `U+3220~U+3225` 로 표기하지만, 실제 visible 문자는 **U+3260~U+3265** (CIRCLED HANGUL/KOREAN). study-guide 원본 파일 (`exam-solutions/study-guide/2014-A.md` 등) 실측에서 `㉠` = `U+3260` 확인. spec 의 character literal 의도를 우선해 regex 를 `[\u3220-\u3225\u3260-\u3265]` 양쪽 range 모두 포함하도록 작성 (`web/markdown_renderer.py` L43-46 + 주석). 두 range 동시 커버이므로 spec range 를 좁게 해석한 경우와 visible char 를 넓게 해석한 경우 모두 정합.

## pytest 결과
```
$ PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest tests/test_markdown_renderer.py -v
============================= test session starts ==============================
platform linux -- Python 3.11.3, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/jai/program-agent/projects/ethics-study
collected 5 items

tests/test_markdown_renderer.py::test_render_preserves_cjk_bytes PASSED  [ 20%]
tests/test_markdown_renderer.py::test_verify_verbatim_all_zero_diff PASSED [ 40%]
tests/test_markdown_renderer.py::test_render_block_elements_intact PASSED [ 60%]
tests/test_markdown_renderer.py::test_typographer_on_breaks_verbatim PASSED [ 80%]
tests/test_markdown_renderer.py::test_raw_html_is_escaped_for_security PASSED [100%]

============================== 5 passed in 0.03s ===============================
```

5/5 PASS. (PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 은 conda 환경의 unrelated `dash` plugin 이 ipykernel comm 부재로 collection 단계에서 NotImplementedError 던지기 때문에 우회. 실제 테스트 자체와 무관.)

import smoke test:
```bash
$ python -c "from markdown_it import MarkdownIt; print('import OK, version:', __import__('markdown_it').__version__)"
import OK, version: 2.2.0
```

## 클린 코드 체크
- **단일 책임**: `markdown_renderer.py` 는 markdown 렌더링·verbatim 카운트 검증만 담당. ES·HTTP·DB·파일시스템 의존 0건 (import 라인 = `re` + `markdown_it.MarkdownIt` 만). TASK-209 가 라우트에서 import 해 사용하는 형태로 분리 완료.
- **함수 한 가지 일**: `render()` (md→HTML), `verify_verbatim()` (5종 카운트 비교) 명확 분리. 헬퍼 5개 (`_strip_tags`, `_count_em_dash`, `_count_cjk`, `_count_circled`, `_count_greek_lower`, `_count_german`) 각각 카운트 클래스 1개씩 처리.
- **이름 의도 명확**: 공개 함수는 동사구 (`render`/`verify_verbatim`), 내부 헬퍼는 underscore prefix + `_count_<class>` 또는 `_strip_tags` 패턴.
- **매개변수 ≤ 5**: 두 공개 함수 모두 매개변수 1-2개. dataclass 불필요.
- **주석 = Why**: typographer OFF 의 근거 (architecture.md L412 byte-level verbatim 규약), 원문자 range 양쪽 포함의 근거 (architecture.md L420 spec 과 실제 파일 codepoint 차이) 두 곳에만 주석. `What` 은 함수명·docstring 에서 자명.

## 이슈/블로커
1. **architecture.md L420 spec 충돌 (minor)**: `㉠㉡㉢㉣㉤㉥` 의 codepoint range 를 `U+3220~U+3225` 로 명시했으나 실제 문자는 `U+3260~U+3265`. 본 구현은 양쪽 range 모두 포함해 안전하게 처리했고 fixture/실파일 모두 일치 확인했으나, Manager 가 차후 architecture.md 갱신 사이클에서 spec 정정 권고 (`U+3220~U+3225` → `U+3260~U+3265`).
2. **markdown-it-py 버전 caveat (minor)**: 환경에 v2.2.0 설치, spec 권장 v3.0.0+. 사용 API 가 v2.x 부터 동일이라 기능 영향 없으나, 차후 빌드 환경 표준화 시 일관성 위해 v3.x 업그레이드 또는 spec 의 `>=3.0.0` 을 `>=2.2.0` 으로 완화 둘 중 택 1 권고.
3. **pytest plugin 환경 이슈 (실측, 본 태스크 무관)**: conda 의 `dash` 패키지가 pytest11 entrypoint 에 등록되어 있고 ipykernel comm 부재로 collection 단계에서 NotImplementedError 발생. `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` 환경변수로 우회. TASK-209 / 향후 테스트 실행 시 동일 환경변수 권장.

## 다음 제안 (TASK-209)
- TASK-209 의 `app.py` 라우트에서 import: `from markdown_renderer import render, verify_verbatim`. 모듈 레벨 `_MD` 인스턴스가 한 번만 생성되므로 thread-safe (markdown-it-py `MarkdownIt` 는 stateless render).
- `verify_verbatim()` 의 logging 사용 패턴: `logger.info("verbatim %s: md=%d html=%d", cls, md_n, html_n)` 형태로 5 라인 출력. ±0 일치 시 INFO, 불일치 시 WARNING 으로 분기 권고 (TASK-209 라우트에서 결정).
- Phase A2 의 TOC 정규식 `^## 문항(?:\s+(?:서술형|논술형|기입형))?\s+\d+` 은 본 모듈 무관 (라우트 단의 별도 처리). 본 모듈은 markdown 렌더만 담당.
- raw HTML escape 정책 (`html: False`) 은 study-guide·coverage 본문이 본인 작성 md 라 default OK. 차후 외부 입력 처리 시점에 별도 sanitization 검토.
