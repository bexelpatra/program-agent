---
task_id: TASK-025(A0/SETUP/A/B/CAT/C/D/E/F/G)
verdict: PASS
---

# Reviewer Report: TASK-025 Phase 7 재검증 (M1~M10 반영 확인)

## 검증 대상
- 파일:
  - `signal/web-automation/architecture.md` L162-L225 (§7 신규 섹션)
  - `signal/web-automation/task-board.md` L50-L62 (Phase 7 행: TASK-025 umbrella + PROBE + A0/SETUP/A/B/CAT/C/D/E/F/G = 11행)
  - `signal/web-automation/reviewer-report-TASK-025.md` (이전 NEEDS_REVISION 10건)
- Manager 주장 요약: 이전 보고서의 M1~M10 수정 요청을 모두 반영했다고 주장.

## 검증 결과

### 파일 존재

| 경로 | 존재 | 비고 |
|------|------|------|
| `signal/web-automation/architecture.md` | O | 225 lines (158 → 225, Phase 7 섹션 +67 lines) |
| `signal/web-automation/task-board.md` | O | L50-L62 Phase 7 섹션, 11 행 (umbrella + PROBE DONE + 9 하위) |
| `projects/web-automation/src/tistory_post/` | X | 신규 생성 예정 (A0/A/B/CAT/C/D/E 산출) — 정상 |
| `projects/web-automation/posts/` | X | TASK-025-F 에서 샘플 폴더 생성 예정 — 정상 |

### 내용 일치 — M1~M10 항목별 검증

#### M1. architecture.md Phase 7 섹션 추가 — **PASS**
- L162 `## 7. 폴더 기반 임시저장 자동화 (Phase 7)` 신규 섹션 확인.
- 하위 항목 전부 존재: **목적** (L164-L165), **계층 구분** (L167-L170: UI vs API vs 세션 공유), **입력 규격** (L172-L196), **마커 파싱 규칙** (L198-L203), **핵심 결정** (L205-L209), **구현 위치** (L211-L220: models/post_loader/image_uploader/category_fetcher/post_builder/post_saver/post_runner + scripts/posts), **의존성** (L222-L224: Pillow + markdown).
- Reviewer 체크리스트 §5 "클린 아키텍처 — 계층 의존 방향" 충족 (`src/tistory_post/` 가 architecture 디렉토리 구조에 명시적으로 기재됨 — L211-L219).
- 다만 §구조 트리 (L27-L71) 자체에는 `src/tistory_post/` 가 추가되지 않았다. L211-L219 의 "구현 위치" 블록에는 열거되어 있으므로 **기능적으로는 충족**되나, 기존 트리 누락은 경미한 흠결. PASS blocker 는 아님.

#### M2. TASK-025-A0 신규 — **PASS**
- L53 TASK-025-A0 확인. `src/tistory_post/models.py` 선행 태스크.
- dataclass 6종 + 예외 1종 모두 중앙 정의 명시:
  - `LoadedPost` 8 필드 (title, category_name, tags, body_markdown, markers, images, folder, skip) — **이전 누락이던 skip 필드 포함**.
  - `Marker` 4 필드 (raw_token, kind, value, position).
  - `UploadedImage` 7 필드 + macro `&amp;` escape 완료 명시.
  - `DraftPayload` 6 필드 — **probe §2 명명 준수, `content_html` 금지** 명시 (M3 연결).
  - `RunResult` 4 필드 (skipped, draft_sequence, orphan_images, error).
  - `PartialUploadError(Exception)` 3 attribute (uploaded, failed_index, cause) — M7 연결.
- A/B/C/D/E 의존성이 TASK-025-A0 로 수정됨:
  - A (L55): `TASK-025-A0,TASK-025-SETUP`
  - B (L56): `TASK-025-A0,TASK-025-SETUP`
  - CAT (L57): `TASK-025-A0`
  - C (L58): `TASK-025-A0,TASK-025-SETUP`
  - D (L59): `TASK-025-A0`
  - E (L60): `TASK-025-A,TASK-025-B,TASK-025-CAT,TASK-025-C,TASK-025-D`
  - A0 (L53): `TASK-025-PROBE` (선행 PROBE 에 의존 — 적절).
- 이전 리뷰 지적 "D 가 DraftPayload 사용하는데 C 에 의존하지 않음" 문제는 **models.py 분리로 해소** (D 는 A0 만 의존 — DraftPayload 가 A0 에 정의되므로 타입 힌트 가능).

#### M3. TASK-025-C `content_html` → `content` + markdown 라이브러리 채택 — **PASS**
- L58 TASK-025-C 의 (1) 단계: `markdown.markdown(post.body_markdown, extensions=['extra', 'nl2br'])` 채택 확정.
- A0 의 DraftPayload 정의에서 `content_html` 금지 명시적 문구 ("probe §2 명명 준수 — `content_html` 금지") 확인.
- task-board.md 전체에서 `content_html` grep → 0건 (A0 의 negative 언급만, 실제 필드명은 `content`).
- (2) 단계: "이미 `&amp;` escape 완료 상태라 재escape 금지" 명시 → escape 책임이 TASK-025-B (image_uploader) 로 귀속됨 확인.

#### M4. TASK-025-B multipart 필드명 probe 4단계 절차 — **PASS**
- L56 TASK-025-B 에 4단계 절차 구체 명시:
  1. `file` 필드명 시도 → `key`·`url` 필드 존재하면 성공.
  2. 400/500 또는 필드 부재 시 `Filedata` 필드명으로 재시도.
  3. 두 번 모두 실패 시 `page.route("**/attach.json", ...)` 로 브라우저 실제 요청 가로채 필드명 capture 후 재시도.
  4. 최종 실패 → `RuntimeError("multipart field name unknown — probe-tistory-api.md L8 수동 탐색 필요")` raise.
- Coder 가 외부 질문 없이 구현 가능한 수준 — 응답 JSON 의 `key`/`url` 필드 유무로 성공 판정, capture fallback 경로까지 명시.

#### M5. TASK-025-A 마커 edge case 8종 + frontmatter 규칙 — **PASS**
- L55 TASK-025-A 에 아래 edge case 모두 명시:
  - `${}` → ValueError("빈 마커").
  - `${0}`/음수 → ValueError("1-based 양의 정수").
  - `${1.5}`/`${abc}` → filename 취급 (확장자 포함 매칭 시도, 없으면 ValueError).
  - `${filename.png}` 파일 부재 → ValueError (폴더 내 이미지 리스트 노출).
  - 동일 마커 중복 → 허용.
  - 고아 마커 (`${5}` 인데 이미지 4개) → ValueError.
  - 고아 이미지 → warning 로그 + 허용.
- frontmatter 규칙: title 누락 → ValueError. category 누락 → None. tags 누락 → `[]`. body 비어있음 → ValueError.
- 테스트 태스크 산출물 (`tests/test_post_loader.py`) 명시.

#### M6. TASK-025-CAT 분리 — **PASS**
- L57 TASK-025-CAT 신규. `src/tistory_post/category_fetcher.py` 로 분리.
- 괄호 주기 "(M6: post_saver 에서 분리)" 로 의도 추적 가능.
- post_saver (L59 TASK-025-D) 의 내용에 `fetch_category_map` 가 포함되지 않음 — grep 검증: L59 에는 오직 `save_draft` 함수만 정의됨. **SRP 준수 확인**.
- post_runner (L60 TASK-025-E) 흐름 (2) 에서 `category_fetcher.fetch_category_map(page)` 호출 — 호출 순서 정합.

#### M7. TASK-025-E 에러 롤백 계약 — **PASS**
- L60 TASK-025-E 에 계약 상세 기재:
  - `PartialUploadError` catch → `.orphan.log` 에 JSONL append (`{"ts": ISO, "key": ..., "url": ..., "filename": ...}`).
  - `.error` 에 JSON 덮어쓰기 (`{"traceback": str, "phase": "upload"|"build"|"save", "ts": ISO}`).
  - 정상 완료 시 (9) 단계 "기존 `.error`·`.orphan.log` 삭제 (이전 실패 흔적 제거)" 확인.
  - retry 없이 1회만 — raise 후 사용자 재실행 위임.
- PartialUploadError catch 명시 확인 (TASK-025-B 의 raise 대응).

#### M8. TASK-025-F 샘플 폴더 내용 구체 명세 — **PASS**
- L61 TASK-025-F 에 샘플 파일 3개 + 스모크 스크립트 2개 전부 명시:
  - `post.md` 전문 (frontmatter + 본문 + `${1}`/`${hello.png}` 마커 2종) 포함.
  - `image1.png`: 100x100 단색 파랑 PNG (Pillow `Image.new('RGB',(100,100),'blue').save('image1.png')` 생성 명령).
  - `hello.png`: 100x100 단색 빨강 PNG.
  - `.gitignore` 에 `projects/web-automation/posts/*/` 추가.
  - scripts: `smoke_tistory_post.sh` + `smoke_tistory_post.py` — login 구조 재사용.

#### M9. TASK-025-SETUP — **PASS**
- L54 TASK-025-SETUP 신규. `requirements.txt` 에 `Pillow>=10.0.0` + `markdown>=3.5` 추가.
- 설치 검증 명령 구체: `pip install -r requirements.txt` + `python3 -c "import PIL; import markdown; print(PIL.__version__, markdown.__version__)"`.
- 의존성: `-` (선행 없음) — A0 와 병렬 실행 가능 (M9 요건 "A0 + SETUP 병렬").

#### M10. TASK-025-C thumbnail 규칙 — **PASS**
- L58 TASK-025-C (5) 단계: `thumbnail = uploads[0].key if uploads else None` — 첫 이미지 key or None 명시.
- 테스트: "empty uploads 시 thumbnail=None" 커버 명시.

### 태스크 완결성 — 재검토

- **TASK-025-A0**: 6 dataclass + 1 예외 전부 필드·타입 명세 → Coder 가 직접 구현 가능.
- **TASK-025-SETUP**: 라이브러리 버전 + import 검증 명령 → 자립적.
- **TASK-025-A**: 마커 파싱 정규식 + edge case 8종 + frontmatter 규칙 + test_post_loader.py 산출물 → 자립적.
- **TASK-025-B**: multipart probe 4단계 + 매크로 공식 + Pillow 사용 + PartialUploadError 계약 → 자립적.
- **TASK-025-CAT**: selector + aria-label/category-id 매핑 + empty 폴백 → 자립적.
- **TASK-025-C**: markdown lib + 치환 + category_map 조회 + thumbnail + test_post_builder.py → 자립적.
- **TASK-025-D**: `/manage/drafts` POST + 응답 스키마 (`success`, `draft.sequence`) + 오류 메시지 포맷 → 자립적.
- **TASK-025-E**: 9 단계 흐름 + PartialUploadError/일반 예외 분기 + `.error`/`.orphan.log`/`.published`/`.draft_id` 파일 계약 → 자립적.
- **TASK-025-F**: bash wrapper 구조 + python entry + 샘플 폴더 3 파일 구체 명세 → 자립적.
- **TASK-025-G**: user 태스크 — 검증 UI 경로 + 성공 기준 (`.published` 생성 + 재실행 시 skip) → 명확.

### 의존성·순서 — 재검토

- **실행 순서** (Manager 주장):
  - Step 0 (병렬): TASK-025-A0 + TASK-025-SETUP 동시 진행 가능 (A0 depends PROBE only, SETUP depends none, 서로 독립 파일).
  - Step 1 (A0 + SETUP 완료 후 병렬 가능):
    - TASK-025-A (depends A0+SETUP)
    - TASK-025-B (depends A0+SETUP)
    - TASK-025-C (depends A0+SETUP)
    - TASK-025-CAT (depends A0 only) — 실제로는 SETUP 불필요
    - TASK-025-D (depends A0 only)
  - A/B/C/CAT/D 는 서로 다른 파일(`post_loader.py`, `image_uploader.py`, `post_builder.py`, `category_fetcher.py`, `post_saver.py`) 에 작업 → **병렬 안전**.
  - Step 2: TASK-025-E (depends A,B,CAT,C,D 전부)
  - Step 3: TASK-025-F (depends E)
  - Step 4: TASK-025-G (depends F, user)
- **정합성 확인**: D 가 DraftPayload 를 사용하나 A0 에서 이미 정의되므로 C 선행 불필요 — 이전 리뷰의 의존성 오류 해소됨.
- **병렬 안전성**: A/B/CAT/C/D 가 **서로 다른 파일을 생성**하므로 같은 파일 충돌 없음. Manager 판단대로 병렬 가능.

### 목적성·클린 아키텍처·분리 원칙 — 재검토

- **목적성**: architecture.md §7 신설 + 사용자 요구(폴더 기반 임시저장) 와 명시적 연결 (L165 "사용자가 지정된 폴더에 ... 자동으로 티스토리에 임시저장") — OK.
- **계층 의존 방향**: `src/tistory_post/*` 가 `src/sites/tistory/login.py` 의 로그인된 Page 를 상위에서 받는 구조 (L170 "같은 BrowserManager 세션 공유") — OK.
- **소스·함수 분리**: `category_fetcher.py` 분리 (M6) → post_saver SRP 준수. image_uploader 가 macro escape 책임, post_builder 가 단순 치환 책임, post_runner 가 orchestration 책임 — 역할 분리 명확.
- **이름·인터페이스**:
  - `DraftPayload.content` (probe 명명 일치) — OK.
  - `LoadedPost.body_markdown` vs `DraftPayload.content` (markdown → HTML 변환 경계 명확) — OK.
- **추후 수정 용이성**: models.py 단일 source 덕에 향후 발행 API (publish) 추가 시 DraftPayload 재사용 가능. CAT 분리로 카테고리 API 변경 시 국소 수정 가능. OK.

## 판정

**PASS**

## 수정 요청

없음. M1~M10 전부 구체적으로 반영되었다. Coder 호출 가능.

## Manager에게 전달

다음 단계 제안:

1. **병렬 Coder 호출** (권장 순서):
   - **Wave 1 (2건 병렬)**: TASK-025-A0 (models.py) + TASK-025-SETUP (requirements.txt). 서로 다른 파일 + 독립.
   - **Wave 2 (5건 병렬)**: Wave 1 완료 확인 후 TASK-025-A / B / CAT / C / D 병렬 호출. 각 태스크가 독립 파일을 생성하므로 충돌 없음. 다만 coder-report 는 **반드시 태스크별 파일명** (`coder-report-TASK-025-A.md` 등) 사용.
   - **Wave 3 (1건)**: Wave 2 전부 DONE 후 TASK-025-E (post_runner — 5개 모듈 통합).
   - **Wave 4 (1건)**: Wave 3 DONE 후 TASK-025-F (smoke + 샘플 폴더).
   - **Wave 5 (user)**: TASK-025-G 는 Execution=user — Manager 자동 실행 금지, 사용자에게 위임.

2. **경미한 선택적 개선 사항** (PASS blocker 는 아니나 차후 반영 권장):
   - architecture.md §구조 트리 (L27-L71) 에도 `src/tistory_post/` 서브트리를 추가하면 개요 파악 시 더 선명. 현재는 §7 구현 위치 블록(L211-L219)에만 존재.
   - TASK-025-F 의 `.gitignore` 항목 중 "샘플 폴더를 `posts/sample-included/` 같은 약속으로 분리하거나 의도 커밋" 이 모호 — 샘플 폴더(`2026-04-22-sample/`) 는 `git add -f` 또는 `.gitignore exception` (`!posts/2026-04-22-sample/`) 중 어느 쪽을 쓸지 Coder 가 선택하게 해도 무방하나, 추후 Reviewer 가 DONE 검증 시 애매할 수 있음. 차후 Wave 4 호출 시 한 줄 덧붙이면 좋음.

위 2개는 선택 개선으로, 현재 분해는 그대로 Coder 에게 넘겨도 좋다.
