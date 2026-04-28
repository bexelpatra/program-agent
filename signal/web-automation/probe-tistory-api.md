# Tistory Manage API Probe (2026-04-22)

Playwright Network 트레이싱으로 perlky.tistory.com 관리 API 3종 실측.

## 1. `POST /manage/post/attach.json`

- **Content-Type**: `multipart/form-data; boundary=...`
- **Request**: 이미지 파일 1개 (필드명 — **Playwright 가 multipart body 를 capture 못 함**. 구현 시 추가 probe 필요. 추정 `file` 또는 `Filedata`)
- **Response** (JSON):
  ```json
  {
    "name": "sample_large.png",
    "url": "https://blog.kakaocdn.net/dna/CL9bz/dJMcahc5bwS/AAAAAAAAAAAAAAAAAAAAAP4QlFzyshoH3tt9mELswv7i_KkdDsofYICgT9XhCgzz/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1777561199&allow_ip=&allow_referer=&signature=lzYdrFPHpdfdvzCL%2Bh%2FKA9yR2yQ%3D",
    "key": "CL9bz/dJMcahc5bwS/AAAAAAAAAAAAAAAAAAAAAP4QlFzyshoH3tt9mELswv7i_KkdDsofYICgT9XhCgzz/img.png",
    "filename": "img.png",
    "size": 63269
  }
  ```

### 매크로 조립 공식
```
[##_Image|kage@{key}?{URL_params}|CDM|1.3|{"originWidth":W,"originHeight":H,"style":"alignCenter","filename":"{name}"}_##]
```
- `{key}` = response `key` 필드 (끝에 `/img.png` 붙음)
- `{URL_params}` = response `url` 의 query string (`credential=...&expires=...&allow_ip=&allow_referer=&signature=...`)
- `&` → `&amp;` HTML-escape (autosave/drafts body 에서 확인)
- originWidth/originHeight = 실제 이미지 픽셀 크기 (로컬 파일에서 계산)
- style = `alignCenter`/`alignLeft`/`alignRight`/`alignNone`

## 2. `POST /manage/drafts`

- **Content-Type**: `application/json`
- **Request body 스키마**:
  ```json
  {
    "title": "PROBE TEST",
    "content": "<p>[##_Image|...]</p><p>...</p>",
    "tags": "",
    "categoryId": 0,
    "thumbnail": "kage@CL9bz/.../img.png",
    "draftSequence": 23
  }
  ```
  - `title`: 문자열
  - `content`: HTML 문자열 (tistory 매크로 포함 가능, `&` → `&amp;` escape)
  - `tags`: 쉼표 구분 문자열 (`"자동화,테스트"`)
  - `categoryId`: 숫자 (0=카테고리 없음, 944981=메모, ...)
  - `thumbnail`: 대표 이미지 key (선택, 매크로에서 `kage@` 부분)
  - `draftSequence`: **기존 draft 의 sequence id — 있으면 업데이트, 없으면 새 draft 생성**
- **Response**: `{"success": true, "total": 7, "draft": {"sequence": 23}}`
  - `draft.sequence` 를 `.draft_id` 파일에 저장 → 재실행 시 동일 draft 업데이트 가능

## 3. 이미지 삭제 API

- **NOT FOUND** (probe 범위 내).
- 에디터에서 `tinymce.execCommand('Delete')` 로 이미지를 제거해도 별도 DELETE HTTP 요청이 발생하지 않음. autosave 만 호출되어 content 에서 매크로가 제거될 뿐 CDN 파일은 orphan 으로 남음.
- **대응**: 업로드 실패 / 롤백 필요 시 `.orphan.log` 에 URL/key 기록 + 사용자 수동 정리 안내.

## 4. 카테고리 ID 매핑 (perlky 실측)

| 이름 | categoryId |
|------|-----------|
| 카테고리 없음 | 0 |
| 차트공부 | 944980 |
| 메모 | 944981 |
| 분석 연습하기 | 945580 |
| 여행 기록 | 1148780 |
| 영화감상 | 1216557 |
| 잡념 상자 | 1216558 |

실행 시 `#category-btn` → `#category-list` DOM 에서 `[category-id]` 속성과 `aria-label` 매핑 동적 추출.

## 5. 쿠키/인증

- 로그인 후 BrowserContext 의 세션 쿠키로 모든 API 호출 인증됨.
- 권장 호출 방식: `page.evaluate("""() => fetch(url, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(...)}).then(r=>r.json())""")` — 쿠키/CSRF 자동.

## 6. 멱등성 + 롤백 설계 반영

- **멱등성**: `.draft_id` 에 `draftSequence` 저장 → 재실행 시 update
- **완료 마커**: `.published` — 있으면 runner 가 skip
- **에러 롤백**: 
  - 이미지 n 장 중 k 장 성공 후 실패 → 이미 올라간 k 장의 URL 을 `.orphan.log` 에 append
  - draft 생성 실패 → draft 미생성이므로 draft 자체 롤백 불필요
  - draft 업데이트 실패 → 기존 draft 유지 (부분 업데이트 방지 위해 atomic 처리)
