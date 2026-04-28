---
task_id: TASK-012(A/B/C/D 세분화군) — 재검증
verdict: PASS
---

# Reviewer Report: TASK-012 (A/B/C/D/ENV) — 재검증 (2nd pass)

## 검증 대상
- 파일:
  - `signal/web-automation/task-board.md` L22-L28 (TASK-012 SPLIT, TASK-012-ENV/A/B/C/D)
- Manager 주장 요약 (직전 NEEDS_REVISION 5건에 대한 패치):
  1. `kakao_auth` → `email_2fa` 로 전면 교체.
  2. TASK-012-A 에 "kakao 전용 5키만 사용, 기존 login_email_input 등은 사용 안 함" 명시.
  3. TASK-012-A `poll_verification_code` 가 리스트 순회 + 단일 str `sender` 인자 호출임을 명시 + `naver_imap.py:162-168` 시그니처 실측 인용.
  4. TASK-012-A Depends On 을 `TASK-012-ENV` → `-` 로 완화.
  5. TASK-012-A / TASK-012-B 설명 끝에 **동일 공유 key 8개** (selectors 5 + email_2fa 3) 리스트를 복붙.

## 검증 결과

### 파일 존재
| 경로 | 존재 | 비고 |
|------|------|------|
| `signal/web-automation/task-board.md` | O | L22-L27 TASK-012-* 전 행 확인 |
| `projects/web-automation/src/auth/naver_imap.py` | O | L162-L168 시그니처 재확인 (`sender: str`) |
| 기타 browser.py / tistory.yaml / .env.example | O | 1차 리뷰에서 실존 검증 완료 — 본 재검증에서는 생략 |

### 내용 일치 — 5개 수정 항목 개별 판정

- **[#1 네이밍: kakao_auth → email_2fa]**
  - 근거: `grep -n "kakao_auth" signal/web-automation/task-board.md` → **NO MATCH**.
  - TASK-012-B 본문에 "신규 최상위 섹션 `email_2fa` 추가 (`kakao_auth` 아님)" 문구로 네거티브 가드까지 포함.
  - TASK-012-A/B 양쪽 공유 key 리스트가 `email_2fa.sender_patterns` / `email_2fa.code_length` / `email_2fa.within_minutes` 로 통일.
  - **판정: 완전 반영 ✓**

- **[#2 selectors 범위 모호 해소]**
  - TASK-012-A 말미: "**기존 yaml 의 selectors.login_email_input/login_password_input/login_submit_button 은 이 흐름에서 사용 안 함** (티스토리 자체 로그인용 키 — 유지만)".
  - TASK-012-B 본문: "**기존 7키(login_email_input·login_password_input·login_submit_button·auth_code_input·write_title_input·write_content_area·write_publish_button) 는 유지** (write 계열은 TASK-013 에서 사용, 기존 login_* 은 티스토리 자체 로그인 경로 예비)".
  - 추가로 `auth_code_input` 중복 키 처리도 명시("기존 값 그대로 사용 — 신규 키 아님, yaml L34 에 존재").
  - **판정: 완전 반영 ✓**

- **[#3 sender 타입]**
  - TASK-012-A 본문: "`poll_verification_code(sender_patterns: list[str], max_attempts=20, interval=3)` → **리스트 순회**하며 각 sender 문자열을 `naver_imap.fetch_verification_code(config, sender=s, within_minutes=email_2fa.within_minutes)` 로 호출 (단일 str 인자 — `fetch_verification_code` 시그니처는 `naver_imap.py:162-168` 기준 `sender: str`). 첫 hit 반환."
  - 실측 대조: `projects/web-automation/src/auth/naver_imap.py` L162-L168 `def fetch_verification_code(config: Config, sender: str, within_minutes: int = 10, ...)` 와 정확히 일치.
  - **판정: 완전 반영 ✓** (Coder 가 리스트를 통째로 `sender=`에 넘길 가능성 차단됨)

- **[#4 Depends On 완화]**
  - task-board.md L24 TASK-012-A 의 "Depends On" 컬럼 값 = `-` (6번째 컬럼 실측).
  - 대조: TASK-012-C 의 Depends On 은 여전히 `TASK-012-A,TASK-012-B` 로 타당하게 유지 (C 단계에서 런타임 결합이 발생).
  - TASK-012-ENV 의 Depends On 도 `-` (사용자 독립 실행).
  - 결과적으로 A 와 B 가 ENV 대기 없이 병렬 IN_PROGRESS 가능.
  - **판정: 완전 반영 ✓**

- **[#5 공유 Config key 계약]**
  - TASK-012-A 공유 key 리스트: `selectors.login_kakao_button` / `selectors.kakao_id_input` / `selectors.kakao_pw_input` / `selectors.email_2fa_button` / `selectors.auth_code_input` / `email_2fa.sender_patterns` (list[str]) / `email_2fa.code_length` (int, default 8) / `email_2fa.within_minutes` (int, default 5). → **8개**.
  - TASK-012-B 공유 key 리스트: `selectors.login_kakao_button` / `selectors.kakao_id_input` / `selectors.kakao_pw_input` / `selectors.email_2fa_button` / `selectors.auth_code_input` / `email_2fa.sender_patterns` / `email_2fa.code_length` / `email_2fa.within_minutes`. → **8개**.
  - 키 집합·순서 완전 동일. A 는 타입·기본값까지 덧붙여 더 상세하지만, B 는 yaml 쪽이라 타입을 yaml 본문에 쓰므로 누락 아님.
  - 양쪽에 "[공유 Config key 계약]" 라벨 + 상호 참조("TASK-012-B 와 원자적 일치 필요" / "TASK-012-A 와 동일") 박아둠.
  - **판정: 완전 반영 ✓**

### 태스크 완결성
- TASK-012-A: 클래스명·6메서드 분해·fallback 순서·단일 str sender 호출 규약·스크린샷 경로·공유 key 계약 모두 명시 → Coder 가 외부 질문 없이 구현 가능.
- TASK-012-B: 신규 5키 + email_2fa 3필드 + 기존 7키 유지 + 중복 key 처리까지 명시 → yaml 수정 범위가 원자적으로 정의됨.
- TASK-012-C/D/ENV: 1차 리뷰에서 이미 PASS — 본 재검증에서 회귀 변경 없음 확인.

### 의존성·순서
- TASK-012-A Depends On: `-` (수정 완료).
- TASK-012-B Depends On: `-` (기존 그대로).
- 공유 key 계약이 양쪽에 복붙되어 있어 **병렬 실행 시에도 key 엇갈림 위험이 0으로 수렴**.
- TASK-012-C Depends On: `TASK-012-A,TASK-012-B` — 합류 시점 정상.
- TASK-012-D Depends On: `TASK-012-C` — 스모크는 코드+스크립트 완성 후.
- 병렬 가능 쌍: (A, B) / (B, ENV) / (A, ENV) 전부 파일 충돌 없음.

### 목적성·클린 아키텍처·분리 원칙
- 1차 리뷰에서 이미 PASS. 본 패치는 task-board.md 텍스트 수정만으로 변경 없음. 회귀 없음 확인.

## 판정
**PASS**

직전 NEEDS_REVISION 5건이 모두 task-board.md L24-L25 패치로 정확히 반영되었다. 잔여 kakao_auth 문자열 없음(grep no-match), sender str 인자 명시, Depends On `-` 전환, 공유 8-key 계약이 A/B 양쪽에 동일 박음. Coder 호출 가능.

## 수정 요청
없음.

## Manager에게 전달
- **Coder 호출 준비 완료 선언.**
- 권장 호출 순서:
  - **병렬 배치**: TASK-012-A (login.py 신규) + TASK-012-B (tistory.yaml 보강) 동시 호출. 파일 겹침 0, key 계약 일치함.
  - 각 태스크 report 는 `coder-report-TASK-012-A.md` / `coder-report-TASK-012-B.md` 로 분리 (병렬 관행).
  - 두 태스크 DONE 후 TASK-012-C (스모크 러너) 순차 진행.
  - TASK-012-D / TASK-012-ENV 는 Execution=user 이므로 C 완료 시점에 사용자에게 manual 전달.
- ENV 값 채우기는 Coder 작업과 병렬로 사용자가 진행 가능 — 대기 시간 숨기기 효과 확보.
