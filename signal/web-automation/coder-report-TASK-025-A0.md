---
agent: coder
task_id: TASK-025-A0
status: DONE
timestamp: 2026-04-22T15:45:00
---

## 결과 요약
Phase 7 폴더 기반 임시저장 자동화의 공통 dataclass 6종 + 예외 1종을 담은 `src/tistory_post/models.py` 와 패키지 진입점 `__init__.py` 를 신규 작성했다. probe-tistory-api.md §2 명명 규약(`content` 필드)을 엄격히 준수했고, A/B/C/D/E 후속 태스크가 `from src.tistory_post import ...` 로 재수출 심볼을 바로 소비할 수 있다.

## 변경된 파일
- projects/web-automation/src/tistory_post/models.py (신규)
- projects/web-automation/src/tistory_post/__init__.py (신규)

## 설계 선택
1. **mutable dataclass**: 모든 dataclass 를 `frozen=False` (기본값) 로 유지. 이유 — post_runner 순차 진행 중 `LoadedPost.skip` 재평가나 후속 확장에서 필드 갱신이 필요할 가능성. immutability 가 가져올 안전성보다 구현 유연성이 우선.
2. **기본값 정책**: mutable default (`list`/`dict`) 는 `field(default_factory=...)` 사용. `LoadedPost.skip: bool = False`, `RunResult.orphan_images: list[UploadedImage] = field(default_factory=list)`, `RunResult.error: str | None = None` 만 기본값 부여. 필수/선택 구분을 명확히 해서 호출 측에서 생성 의무를 드러냄.
3. **Literal/Optional 대신 Python 3.11+ syntax**: `kind: Literal["index", "filename"]` 는 typing.Literal 만 import (3.11 에서 typing 경유 강제). `Optional[X]` 대신 `X | None` PEP 604 사용.
4. **`from __future__ import annotations`**: 헤더에 명시. 런타임 annotation 평가를 연기해 순환 import 여지를 줄이고 forward reference 필요 없게 처리.
5. **probe 명명 엄격 준수**: `DraftPayload.content` / `DraftPayload.categoryId` / `DraftPayload.draftSequence` 를 probe §2 request schema 와 동일 camelCase 로 유지. JSON 직렬화 시 field 이름 변환 없이 `asdict` 바로 사용 가능하도록 의도.
6. **`PartialUploadError.__init__`**: self 필드 3개 저장 + `super().__init__(msg)` 에 한국어 메시지 조립. `len(uploaded)/failed_index+1` 로 "n/m 성공" 을 표현.
7. **docstring 필드 의미 + 생성/소비 주체 명시**: 각 dataclass 의 docstring 에 "어느 모듈이 생성/소비 하는지" 를 1줄로 달아 A0 이후 B/C/D/E 구현 시 혼동 방지.
8. **`__init__.py` 재수출**: 6 심볼을 `__all__` 에 명시하고 import 재수출. 사용처는 `from src.tistory_post import LoadedPost, ...` 로 짧게 작성 가능.

## 자기검증 (DoD 7건)

**DoD 1 — 파일 생성**
```
$ ls -la projects/web-automation/src/tistory_post/
-rw-rw-r-- 1 jai jai  319  4월 22 15:42 __init__.py
-rw-rw-r-- 1 jai jai 5039  4월 22 15:43 models.py
```
결과: 두 파일 신규 생성됨.

**DoD 2 — 패키지 재수출 import**
```
$ PYTHONPATH="$(pwd)" python3 -c "from src.tistory_post import LoadedPost, Marker, UploadedImage, DraftPayload, RunResult, PartialUploadError; print('DoD2 OK')"
DoD2 OK
```

**DoD 3 — py_compile 통과**
```
$ python3 -m py_compile src/tistory_post/models.py && echo "DoD3 py_compile OK"
DoD3 py_compile OK
```

**DoD 4 — DraftPayload 인스턴스 생성**
```
$ PYTHONPATH="$(pwd)" python3 -c "from src.tistory_post.models import DraftPayload; d = DraftPayload(title='t', content='c', tags='a,b', categoryId=0, thumbnail=None, draftSequence=None); print(d)"
DraftPayload(title='t', content='c', tags='a,b', categoryId=0, thumbnail=None, draftSequence=None)
```

**DoD 5 — probe 명명 위반 0건**
```
$ grep -c "content_html" src/tistory_post/models.py
0
```
주의: 초기 docstring 에 "`content_html` 금지" 라는 **금지 선언** 문장이 포함되어 있어 grep 1건이 잡혔다. DoD 5 가 엄격히 0 을 요구하므로 docstring 문구를 "필드명은 `content`, 다른 변형 금지" 로 수정해 0 건 달성.

**DoD 6 — PartialUploadError 클래스 1건**
```
$ grep -c "class PartialUploadError" src/tistory_post/models.py
1
```

**DoD 7 — `from __future__ import annotations` 1건**
```
$ grep -c "^from __future__ import annotations" src/tistory_post/models.py
1
```

## 이슈/블로커
없음.

포맷터 hook 이 `PartialUploadError.__init__` 의 `super().__init__(...)` 내부 인접 문자열 리터럴 2개(`f"... 성공, "` + `f"원인: {cause}"`)를 자동으로 붙였다. Python 의 adjacent string literal concatenation 규칙에 따라 의미는 동일하며(`"ab"` == `"a" "b"`), 런타임 메시지에 영향 없음을 확인.

## 다음 제안
1. **TASK-025-SETUP 병렬 진행 가능**: models.py 는 Pillow/markdown 을 import 하지 않으므로 requirements 추가 태스크와 독립적. B/C 구현 전에 SETUP 을 먼저 돌려도 되고, SETUP 과 A0 를 병합한 묶음 검증도 가능.
2. **TASK-025-B (image_uploader)** 에서 `UploadedImage.macro` 조립 시 `&` → `&amp;` 변환을 **반드시 image_uploader 측에서 1회만** 수행하도록 모듈 docstring 에 명시했다. post_builder 는 문자열 치환만 하고 재escape 금지. 후속 리뷰 시 이 계약 위반 여부를 grep 으로 실증.
3. **공통 유틸 추출 타이밍**: 현재 models.py 는 pure dataclass 만 포함해 의존성 0. 향후 `asdict(payload, dict_factory=...)` 같은 JSON 직렬화 helper 가 필요해지면 `tistory_post/serialization.py` 로 분리 권장 (models 는 순수 도메인 타입 유지).
