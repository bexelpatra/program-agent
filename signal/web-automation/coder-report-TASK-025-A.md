---
agent: coder
task_id: TASK-025-A
status: DONE
timestamp: 2026-04-22T15:50:00
---

## 결과 요약
Phase 7 폴더 기반 임시저장 자동화의 로더 모듈 `src/tistory_post/post_loader.py` 와 pytest 기반 단위 테스트 `tests/test_post_loader.py` 를 신규 작성했다. `load_post(folder) -> LoadedPost` 는 `.published` skip, YAML frontmatter 파싱, 이미지 사전순 수집, `${N}`/`${filename}` 마커 추출 및 파일 매핑, 고아 마커·고아 이미지·빈 마커·0/음수 인덱스·누락 파일의 edge case 7종을 모두 ValueError 로 방어한다. 테스트는 14개 함수(parametrize 포함 실제 16 run) 전부 PASS.

## 변경된 파일
- projects/web-automation/src/tistory_post/post_loader.py (신규, 268 lines)
- projects/web-automation/tests/test_post_loader.py (신규, 14 test functions / 16 runs)

## 설계 선택

### 1. 정규식 — `r"\$\{([^}]*)\}"`
- `[^}]*` 로 중첩/미닫힘 케이스 차단. 빈 마커 `${}` 는 의도적으로 **정규식에서는 매치시키고** 후처리에서 ValueError 로 돌린다. 이유: "빈 마커" 라는 명확한 사용자 오류 메시지를 제공하려면 정규식 단계에서 match 되어야 한다 (`[^}]+` 로 바꾸면 그냥 매치 실패로 조용히 삼켜진다).
- `finditer` + `match.start()` 로 position offset 을 보존해 Marker.position 에 저장.

### 2. frontmatter 파싱 방식 — 수동 split + `yaml.safe_load`
- 첫 줄이 `---` 인지 확인 → 두 번째 `---` 라인 위치 탐색 → 그 사이 블록만 `yaml.safe_load`. python-frontmatter 같은 외부 라이브러리 의존성 추가를 피하고 requirements.txt 변동 없이 구현.
- `splitlines(keepends=True)` + `rstrip("\r\n")` 로 Windows 줄바꿈(CRLF) 섞인 입력도 방어.
- `yaml.safe_load` 가 `None` (빈 frontmatter) 반환 시 `{}` 로 정규화.
- `tags`: list 아니면 ValueError 로 거부. str 1개는 `[str]` 로 자동 승격하지 **않는다** — 사용자 의도 모호성 배제.

### 3. images dict 구성 정책
- `images` dict 에는 **마커에 의해 실제로 참조된** 이미지만 포함. 고아 이미지는 warning 으로만 기록하고 dict 에 넣지 않는다. 이유: image_uploader 가 이 dict 를 순회해 업로드할 것이므로, 참조 없는 이미지를 업로드해 orphan 로그만 남기는 비용을 차단.
- key 는 파일명(`1.png`), value 는 `path.resolve()` 로 절대경로. 동일 파일이 중복 마커로 참조되면 같은 key 로 덮어쓰기 (허용 — 동일 절대경로라 멱등).
- `markers` list 는 중복 마커를 모두 보존 (본문 내 각 치환 지점을 post_builder 가 순회해야 하므로).

### 4. 정수 판별 — `_looks_like_integer` 헬퍼
- `str.isdigit()` 만 쓰면 `-1` 을 filename 으로 오분류. `+`/`-` 선행 부호 1개 허용 후 나머지를 `isdigit()` 로 검사해 `-1`, `-5`, `0`, `+5` 를 전부 정수로 잡고 `≤0` 은 ValueError, `≥1` 은 index 로 분류.
- `1.5`, `abc`, `hello.png` 는 filename 으로 떨어지며 파일 매칭 단계에서 부재 시 ValueError.

### 5. 함수 분해
- `load_post` (진입점) / `_split_frontmatter` / `_collect_images` / `_extract_markers` / `_classify_marker_content` / `_looks_like_integer` / `_resolve_markers` / `_resolve_single_marker` / `_warn_orphan_images` 로 Single Responsibility 유지.
- 모든 private helper 는 `_` prefix. 테스트는 public entry point `load_post` 만 호출해 black-box 로 검증.

## 자기검증 (DoD 7건)

### DoD 1 — 파일 생성
```
$ ls -la projects/web-automation/src/tistory_post/post_loader.py projects/web-automation/tests/test_post_loader.py
-rw-rw-r-- 1 jai jai  8471  4월 22 15:47 .../src/tistory_post/post_loader.py
-rw-rw-r-- 1 jai jai 11075  4월 22 15:48 .../tests/test_post_loader.py
```
결과: 두 파일 신규 생성됨.

### DoD 2 — 테스트 함수 10개 이상
```
$ grep -c "^def test_" tests/test_post_loader.py
14
```
14 함수 (그중 하나는 `@pytest.mark.parametrize` 로 3 케이스 전개 → pytest 수집 기준 16 run). DoD ≥10 충족.

### DoD 3 — import 검증
```
$ PYTHONPATH="$(pwd)" python3 -c "from src.tistory_post.post_loader import load_post; print('OK')"
OK
```

### DoD 4 — py_compile
```
$ python3 -m py_compile src/tistory_post/post_loader.py && echo "py_compile OK"
py_compile OK
```

### DoD 5 — pytest 전부 PASS
실행 환경 주의: anaconda base env 에 `dash` 패키지 plugin 이 pytest entrypoint 로 등록되어 있어 `pytest` 를 그대로 실행하면 collection 단계에서 `NotImplementedError` (jupyter comm). `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` 환경변수로 우회.

```
$ PYTHONPATH="$(pwd)" PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest tests/test_post_loader.py -v
============================= test session starts ==============================
platform linux -- Python 3.11.3, pytest-9.0.2, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: /home/jai/program-agent/projects/web-automation
collecting ... collected 16 items

tests/test_post_loader.py::test_load_post_happy_path PASSED              [  6%]
tests/test_post_loader.py::test_load_post_skip_when_published_marker_exists PASSED [ 12%]
tests/test_post_loader.py::test_load_post_raises_when_title_missing PASSED [ 18%]
tests/test_post_loader.py::test_load_post_raises_when_body_empty PASSED  [ 25%]
tests/test_post_loader.py::test_load_post_raises_on_empty_marker PASSED  [ 31%]
tests/test_post_loader.py::test_load_post_raises_on_non_positive_index[0] PASSED [ 37%]
tests/test_post_loader.py::test_load_post_raises_on_non_positive_index[-1] PASSED [ 43%]
tests/test_post_loader.py::test_load_post_raises_on_non_positive_index[-5] PASSED [ 50%]
tests/test_post_loader.py::test_load_post_raises_on_orphan_index_marker PASSED [ 56%]
tests/test_post_loader.py::test_load_post_raises_on_missing_filename PASSED [ 62%]
tests/test_post_loader.py::test_load_post_warns_on_orphan_image PASSED   [ 68%]
tests/test_post_loader.py::test_load_post_duplicate_marker_keeps_both_markers_single_image PASSED [ 75%]
tests/test_post_loader.py::test_load_post_raises_when_post_md_missing PASSED [ 81%]
tests/test_post_loader.py::test_load_post_raises_when_no_frontmatter_opening PASSED [ 87%]
tests/test_post_loader.py::test_load_post_raises_when_tags_not_list PASSED [ 93%]
tests/test_post_loader.py::test_load_post_no_images_no_markers PASSED    [100%]

============================== 16 passed in 0.03s ==============================
```

### DoD 6 — ValueError raise 7건 이상
```
$ grep -cE "raise ValueError" src/tistory_post/post_loader.py
10
```
10건 (DoD ≥7 충족). edge case 커버: (1) 첫 줄 `---` 아님 / (2) 닫는 `---` 없음 / (3) frontmatter 가 dict 아님 / (4) title 누락 / (5) tags list 아님 / (6) 본문 비어있음 / (7) 빈 마커 `${}` / (8) 0 또는 음수 인덱스 / (9) 고아 인덱스 마커 / (10) filename 마커 파일 부재.

### DoD 7 — models import 1건
```
$ grep -c "from src.tistory_post.models import" src/tistory_post/post_loader.py
1
```

## 이슈/블로커

**pytest 플러그인 autoload 이슈 (환경 문제, 코드 문제 아님)**
- anaconda base env 에 설치된 `dash` 가 pytest11 entrypoint 로 등록되어 있고, `dash._jupyter` import 시 jupyter comm 이 비-Jupyter 환경에서 `NotImplementedError` 를 던진다.
- 해결: `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` 환경변수로 third-party plugin autoload 차단 후 실행. 후속 스모크/CI 에서도 동일 flag 를 쓰면 되므로 블로커 아님.
- 향후 CI 환경 구축 시 `.envrc` 또는 `pytest.ini` 의 `addopts`/`disable_plugins` 대안 검토 가능.

포맷터 hook 이 일부 long line 을 재배치(L117 의 `body_markdown = "".join(lines[closing_index + 1 :])` 등) 했으나 의미 변화 없이 줄길이 정렬만 된 것으로 확인.

## 다음 제안

1. **TASK-025-C (post_builder)** 가 `LoadedPost.markers` 리스트를 순회하면서 `raw_token` 을 `UploadedImage.macro` 로 치환할 때, **중복 마커의 모든 occurrence 를 한 번에 치환**해야 한다 (`body.replace(raw_token, macro)` 는 전역 치환이라 OK — 굳이 marker.position 으로 순회할 필요 없음). post_builder 구현 시 position 필드는 "디버깅용" 정도로만 쓰이고 실제 치환은 `str.replace` 면 충분.

2. **tags 타입 정규화 정책**: 현재 로더는 `tags: "스모크"` (단일 문자열) 를 ValueError 로 거부한다. 만약 사용자 편의상 "문자열 1개면 `[문자열]` 로 승격" 이 필요해지면 `_split_frontmatter` 의 tags 처리 블록만 바꾸면 된다. 현재는 명시적 리스트 문법을 강제해 오타 조기 발견 효과가 크다고 판단.

3. **Pillow 이미지 검증 연기**: 로더는 이미지 확장자만 보고 실제로 파일을 열지 않는다 (테스트에서 0-byte fake PNG 사용). Pillow 로 실제 width/height 를 측정하는 것은 `image_uploader.py` (TASK-025-B) 의 책임이며, 그 단계에서 손상 이미지를 걸러낸다. 로더에서 미리 Pillow 로 검증하면 책임 혼재 + SETUP 태스크 (Pillow 의존성) 와의 순서 결합이 생김.

4. **import 경로 정책**: `from src.tistory_post.models import ...` 절대 임포트를 사용 (PYTHONPATH=PROJECT_ROOT 가정). `from .models import ...` 상대 임포트가 더 견고하지만 기존 auth/naver_imap.py·tests/test_naver_imap.py 패턴(절대 임포트)과 일관성 유지 차원에서 절대 임포트 유지.
