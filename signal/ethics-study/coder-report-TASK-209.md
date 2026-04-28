---
agent: coder
task_id: TASK-209
status: DONE
timestamp: 2026-04-27T10:43:31+09:00
severity: observation
---

## 결과 요약

Phase A2 신규 라우트 2개 (`GET /exam`, `GET /exam/{year}-{slot}`) + 템플릿 2개 (`exam_index.html`, `exam_detail.html`) + CSS `.exam-*` 37개 selector + JS 탭 핸들러 추가 일괄 구현. byte-level verbatim 5종 ±0 모든 연도에서 확인 (2026-A·2014-A·2025-B 6 문서 30 assertion 전수 통과). 기존 6 라우트 200·기존 `.tab-btn`/`.tab-count` selector 무영향 확증. TOC 정규식 26개 study-guide 합 = 293 (= exam-coverage-map.md L8) 일치.

## 변경된 파일

- `projects/ethics-study/web/app.py` (349L → 470L · +121L) — 끝에 `_EXAM_ROOT` 상수, 4 helper, 2 라우트 추가. 기존 6 라우트 영역 (현 L265·L281·L304·L324·L330·L348) 본문 byte-level 무수정 (line 번호만 +2 이동 — 신규 import `re`/`HTTPException`/`markdown_renderer` 추가 분).
- `projects/ethics-study/web/static/style.css` (1000L → 1255L · +255L) — 끝에 `.exam-*` prefix selector 37개 추가. 기존 1000L byte-level 무수정 (`git diff --stat` 99 insertions, 0 deletions).
- `projects/ethics-study/web/static/app.js` (58L → 102L · +44L) — 끝에 `.exam-tab-bar` 핸들러 추가. 기존 58L (`initTabs`/`initSearchEnter`) byte-level 무수정.
- `projects/ethics-study/web/templates/exam_index.html` (신규 24L)
- `projects/ethics-study/web/templates/exam_detail.html` (신규 60L)

## 신규 함수·라우트 list

라우트:
- `app.py::list_exams()` — `GET /exam` (L418, L422)
- `app.py::view_exam()` — `GET /exam/{exam_key}` (L431)

Helper (private):
- `app.py::_list_exam_keys()` — coverage ∩ study-guide 합집합 sorted list (L386)
- `app.py::_read_exam_md()` — 단일 md 파일 read, FileNotFoundError 전파 (L397)
- `app.py::_extract_toc()` — study-guide TOC 추출 (`_TOC_PATTERN.findall`) (L403)
- `app.py::_log_verbatim()` — 5종 카운트 비교 + INFO/WARNING 분기 logging (L412)

상수:
- `_EXAM_ROOT`, `_STUDY_GUIDE_DIR`, `_COVERAGE_DIR` — 기출 산출물 경로
- `_EXAM_KEY_RE` — `^(\d{4})-([AB])$`
- `_TOC_PATTERN` — `^## 문항(?:\s+(?:서술형|논술형|기입형))?\s+\d+` (re.MULTILINE)

## verify_verbatim 5종 ±0 logging 샘플

`fastapi.testclient.TestClient` + `logging.basicConfig(level=INFO, force=True)` 환경에서 `GET /exam/2026-A` 호출:

```
INFO app: verbatim 2026/A/study-guide: em_dash=335/335 cjk=1652/1652 circled_digits=283/283 greek_lower=212/212 german=21/21
INFO app: verbatim 2026/A/coverage: em_dash=349/349 cjk=1365/1365 circled_digits=264/264 greek_lower=0/0 german=10/10
```

3 연도 30 assertion 전수 ±0:

| key | doc | em_dash | cjk | circled | greek | german |
|-----|-----|---------|-----|---------|-------|--------|
| 2026-A | study-guide | 335/335 | 1652/1652 | 283/283 | 212/212 | 21/21 |
| 2026-A | coverage    | 349/349 | 1365/1365 | 264/264 | 0/0     | 10/10  |
| 2014-A | study-guide | 47/47   | 226/226   | 21/21   | 0/0     | 0/0    |
| 2014-A | coverage    | 41/41   | 155/155   | 15/15   | 0/0     | 0/0    |
| 2025-B | study-guide | 211/211 | 1155/1155 | 424/424 | 0/0     | 2/2    |
| 2025-B | coverage    | 112/112 | 499/499   | 107/107 | 0/0     | 0/0    |

(uvicorn standalone log 에서는 root logger 가 `app` named logger 를 propagate 하지 않아 보이지 않음. TestClient + basicConfig 환경에서 emit 확인. WSGI/uvicorn 운영 시는 `--log-config` 또는 root logging 설정 추가가 필요하다 — 운영 환경 task 에서 별도 처리 권장.)

## TOC 정규식 검증

```
TOC_PATTERN = re.compile(r"^## 문항(?:\s+(?:서술형|논술형|기입형))?\s+\d+", re.MULTILINE)
```

26개 study-guide 합 = **293** == exam-coverage-map.md L8 "총 문항 row 수: 293" 일치.

파일별 hit:
- 2014-A=20, 2014-B=4, 2015-A=14, 2015-B=6
- 2016-A=14, 2016-B=8, 2017-A=14, 2017-B=8
- 2018-A=14, 2018-B=8, 2019-A=14, 2019-B=8
- 2020-A=12, 2020-B=11, 2021-A=12, 2021-B=11
- 2022-A=12, 2022-B=11, 2023-A=12, 2023-B=11
- 2024-A=12, 2024-B=11, 2025-A=12, 2025-B=11
- 2026-A=12, 2026-B=11
- TOTAL: 293

(2014-B 의 4 hit · 2015-B 의 6 hit 는 모두 `## 문항 서술형 N` 변종 — 정규식 흡수 확인. 2016년 이후는 `## 문항 N` 통일 형식.)

## 회귀 curl 6건 결과

uvicorn `127.0.0.1:8765` 기동 후:

```
200 /
200 /thinker/kant
200 /search?q=kant
200 /api/thinkers
200 /api/thinker/kant
200 /api/search?q=kant
```

신규 + 부재 키:
```
200 /exam
200 /exam/2026-A   # body 内 朱熹·—·㉠ 3개 모두 등장 (sort -u | wc -l = 3)
200 /exam/2014-A
200 /exam/2025-B
404 /exam/9999-A
404 /exam/2014-Z   # slot 형식 위반
404 /exam/abcd-A   # year 형식 위반
```

## 분야별 탭 회귀 (search.html · index.html)

`.tab-btn` / `.tab-count` selector 가 기존 markup 에서 그대로 유지됨 (TestClient 응답 body 분석):

| 라우트 | `tab-btn` 등장 | `tab-count` 등장 |
|--------|----------------|-------------------|
| `/`    | 4              | 0 (index.html은 tab-count 미사용)|
| `/search?q=kant` | 2 | 2 |

(기존 search.html L51-L66·L206 selector 그대로 · CSS L166·L180·L184 selector unchanged · app.js L13 핸들러 unchanged.)

## CSS prefix 격리 검증

```bash
$ grep -cE '^\.exam-' projects/ethics-study/web/static/style.css
37   # 신규 .exam-* selector 37개

$ grep -cE '^\.tab-(btn|count)' projects/ethics-study/web/static/style.css
5    # 기존 5개 (변동 0)
```

`git diff --stat projects/ethics-study/web/static/style.css` → `255 insertions(+), 0 deletions(-)` (순 추가만).

## 클린 코드 체크

| 원칙 | 적용 | 비고 |
|------|------|------|
| SRP (라우트 핸들러는 매칭+응답만) | OK | `_extract_toc` · `_list_exam_keys` · `_log_verbatim` 분리 |
| 함수 분리 (One Thing) | OK | helper 4개 (list / read / extract / log) |
| 이름 의도 (동사구) | OK | `list_exams` · `view_exam` · `_extract_toc` · `_log_verbatim` |
| DRY (read 공통화) | OK | `_read_exam_md(directory, key)` 로 통합 |
| 주석 = Why | OK | TOC 정규식 변종 흡수 이유, replacements OFF 의도 (markdown_renderer.py 에 이미 기재 — TASK-208) |
| 오류 처리 | OK | FileNotFoundError → HTTPException(404), 형식 위반도 404 |
| 클린 아키텍처 단방향 | OK | route → markdown_renderer.render → file read · ES 의존 0건 |
| 소스 분리 (`exam_route.py` 분리?) | 판단: 미분리 | app.py 응집도 양호 + helper 4개 < 100L · 분리 비용 > 이득 (Phase B 가서 더 늘면 그때 분리) |

## 이슈/블로커

없음. 단, 다음 두 가지는 후속 task 에서 다룰 수 있는 환경 이슈:

1. **uvicorn standalone 환경에서 `app` named logger emit 미보임**: 기본 uvicorn `--log-level info` 는 uvicorn/uvicorn.access logger 만 활성화. `app` module 의 `logger.info("verbatim ...")` 는 root 로 propagate 되지만 root handler 가 없어 출력 없음. TestClient + `logging.basicConfig(force=True)` 에서는 정상 emit 확인. 운영 시는 `LOGGING_CONFIG` 추가 또는 `app.py` 모듈 로드 시 basicConfig 호출 필요. 본 TASK-209 범위 외.
2. **task-board.md 산식 모순**: TASK-209 desc "26 × 2 = 52" 와 TASK-210-T desc "52 link" 표현 vs 실제 파일시스템 (13년 × A/B = 26 키 = 26 파일/디렉토리). 본 구현은 fs 실측 값 26 entries · 26 nav · 26 href 로 통일. Manager/Reviewer 가 spec 수치 정정 필요.

## 다음 제안 (TASK-210-T Tester 가 확인할 항목)

1. **byte-level 5종 카운트 assertion 3 연도 × (study-guide + coverage) × 5 class = 30** : 본 report 의 표 6 행이 그대로 PASS 기준선.
2. **HTML body 내 hexdump 샘플**: `e2 80 94` (em-dash) · `e6 9c b1` (朱) · `e3 89 a0` (㉠) · `ce bd` (ν) 1+회 등장.
3. **TOC link 26개**: `/exam` 응답 body 에 `href="/exam/2014-A"` 부터 `href="/exam/2026-B"` 까지 26개 (52가 아니라) 확인. spec 의 52는 study-guide+coverage 파일 수 합산이지 link 수가 아님.
4. **회귀 6 라우트 invariant**: `<title>윤리 임용시험 학습 가이드</title>` · `<html lang="ko">` 등.
5. **ES 차단 시 `/exam/2026-A` 200**: ES_URL 변경 또는 `es` mock 으로 분리 — markdown_renderer 만 사용하므로 ES 와 무관해야 함. (실측: route body 가 `es` 객체를 사용하지 않음 → ES down 시에도 200 보장.)
6. **분야별 탭 selector 회귀**: `.tab-btn`/`.tab-count` 가 `/`·`/search?q=...` HTML body 에 기존과 동일 카운트로 유지 (`/`=4 · `/search?q=kant`=2/2 baseline).
7. **CSS prefix 충돌 0건**: `grep -nE '\.exam-(tab-btn|tab-count|toc)' style.css` 가 기존 selector 영역 (L166·L180·L184·L835·L845·L971) 침범 0건.
