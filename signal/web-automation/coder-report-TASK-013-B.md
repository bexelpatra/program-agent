---
agent: coder
task_id: TASK-013-B
status: DONE
timestamp: 2026-04-22T11:55
---

## 결과 요약
`projects/web-automation/config/tistory.yaml` 을 Reviewer #1 택B 경로대로 보강했다. (a) `blog.blog_name` placeholder → `perlky` 실측 주입, (b) 셀렉터 섹션 재조직: `write_title_input` 값 덮어쓰기, `write_content_area` 키 삭제, `write_publish_button` → `publish_btn` key rename + 값 주입, 신규 키 7개 추가(`write_body_iframe`/`tag_input`/`category_btn`/`category_list`/`attach_btn`/`attach_option_prefix`/`save_draft_btn`). 기존 `site`/`account`/`naver_imap`/`email_2fa` 섹션과 TASK-012 주입 `kakao_id_input`/`kakao_pw_input` 실측값은 그대로 유지했다. 공유 Config key 계약 10개(TASK-013-A 와 원자적 일치)가 모두 1 hit 로 실증되었다.

## 변경된 파일
- projects/web-automation/config/tistory.yaml (수정)

### 변경 diff 요약
1. L25 `blog_name: "YOUR_BLOG_NAME"` → `blog_name: "perlky"` (+주석 갱신 "실측 주입")
2. L44 `write_title_input: ""` → `write_title_input: 'textarea#post-title-inp'` (값 덮어쓰기, key 유지)
3. **L45 `write_content_area: ""` 행 삭제** (신규 계약에 해당 이름 없음 — TinyMCE API 경유)
4. **L46 `write_publish_button: ""` → `publish_btn: 'button#publish-layer-btn'`** (key rename + 값 주입)
5. 신규 추가: `write_body_iframe`, `tag_input`, `category_btn`, `category_list`, `attach_btn`, `attach_option_prefix`, `save_draft_btn` (각각 주석 포함)
6. 섹션 헤더 주석 재정리: `=== 인증번호 (TASK-012 공용) ===` / `=== 글 작성 (TASK-013 구현 대상) ===` 로 분리

최종 파일 67 lines, 단일 trailing newline (`tail -c 1 | xxd` → `0a` 확인).

## DoD 검증 결과 (grep·파싱 실증)

### (1) yaml 파싱 성공
```
$ python3 -c "import yaml; d=yaml.safe_load(open('config/tistory.yaml')); print('PARSE_OK keys:', list(d.keys()))"
PARSE_OK keys: ['site', 'account', 'naver_imap', 'blog', 'selectors', 'email_2fa']
```
→ 동일 key 중복 없음, safe_load 성공.

### (2) write_content_area 삭제 확인
```
$ grep -cE '^\s*write_content_area:' config/tistory.yaml
0
```
→ 기대값 0 일치.

### (3) write_publish_button rename 확인
```
$ grep -cE '^\s*write_publish_button:' config/tistory.yaml
0
```
→ 기대값 0 일치.

### (4) publish_btn 존재 확인
```
$ grep -cE '^\s*publish_btn:' config/tistory.yaml
1
```
→ 기대값 1 일치.

### (5) 공유 10개 key 1 hit 실증
```
blog_name                 => 1
write_title_input         => 1
write_body_iframe         => 1
tag_input                 => 1
category_btn              => 1
category_list             => 1
attach_btn                => 1
attach_option_prefix      => 1
save_draft_btn            => 1
publish_btn               => 1
```
모두 1 hit (loop: `for key in ...; do grep -cE "^\s*${key}:" config/tistory.yaml; done`). blog_name 값은 `blog_name: "perlky"` 로 확인.

### (6) YOUR_BLOG_NAME placeholder 제거 확인
```
$ grep -cE "YOUR_BLOG_NAME" config/tistory.yaml
0
```
→ 기대값 0 일치 (선행 `^\s*` 없는 전역 grep 이지만 결과 동일 0 — 파일 어디에도 남지 않음을 확정).

### (7) TASK-012 실측값 유지 확인
```
$ grep -cE "^\s*kakao_id_input:" config/tistory.yaml
1
$ grep -cE "^\s*kakao_pw_input:" config/tistory.yaml
1
$ grep -E "kakao_id_input|kakao_pw_input" config/tistory.yaml
  kakao_id_input: 'input[name="loginId"]'      # 실측: type=text, id=loginId--1
  kakao_pw_input: 'input[name="password"]'     # 실측: type=password, id=password--2
```
→ TASK-012-FIX 에서 주입된 실측 셀렉터 원문 보존.

## 이슈/블로커
없음.

## 다음 제안
- TASK-013-A (writer.py 구현) 와 본 태스크는 Config key 계약 10개가 원자적으로 동기화되어 있어 병렬 실행해도 정합 리스크 없음. 두 태스크 DONE 확인 후 TASK-013-C (스모크 러너) 순차 호출 권장.
- `selectors.login_email_input` / `login_password_input` / `login_submit_button` 3개는 현재 미사용 상태로 유지 중이다 (티스토리 자체 로그인 경로 예비). 장기적으로 카카오 로그인만 지속할 것이 확실해지면 정리 태스크로 분리 가능.
