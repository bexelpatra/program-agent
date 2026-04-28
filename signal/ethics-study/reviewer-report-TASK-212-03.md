---
task_id: TASK-212-03
agent: reviewer
verdict: NEEDS_REVISION
session: 2026-04-28
target: signal/ethics-study/task-board.md L378 (TASK-212-03 regan ES 등록)
---

# Reviewer Report — TASK-212-03 (regan ES 등록)

## 검증 결과 요약

Manager 주장 13건 중 **11건 PASS · 2건 NEEDS_REVISION**. 핵심 결함 2건:
1. **2018-A study-guide BLOCKER 라인 명세 부정확** — Manager spec "L19·L40·L597·L598·L599·L629" 중 **L597·L599 는 BLOCKER 표기 라인 아님** (사상가 확정/trademark 라인). 실제 BLOCKER-tagged 라인은 **L19·L40·L598·L629** 4곳.
2. **2024-B study-guide BLOCKER 라인 enumeration 미완** — Manager spec 이 "regan BLOCKER 라인 grep 후 enumerate" 라고 TODO 로 남김. Reviewer 가 grep 실행 결과 **10개 라인** 확증 (아래 §6).
3. **blocker-log 라인 참조 부정확** — Manager spec "blocker-log L585-L595 부근 (BLK-175E-2024B-006)" 은 **잘못됨**. L585-L595 은 BLK-175E-2020B-003 (fazang) 영역. **BLK-175E-2024B-006 실제 위치 = L946-L952** (헤더 L946).

이 3건은 Coder 호출 전 Manager 가 task-board L378 description 을 정정해야 한다 (모호한 line 표기는 Coder 가 잘못된 라인을 수정·생성할 위험).

---

## 항목별 검증

### 1. ES 누락 확증 (PASS)
- `curl http://localhost:9200/ethics-thinkers/_doc/regan` → **HTTP 404** 실측.
- `curl http://localhost:9200/ethics-claims/_search?q=thinker_id:regan` → `total.value=0` 실측.
- ES indices 실측: `ethics-thinkers` (69 docs)·`ethics-claims` (1058 docs)·`ethics-fields` (7 docs)·`ethics-keywords` (616 docs)·`ethics-relations` (231 docs)·`ethics-works` (272 docs).

### 2. 출제 row 2회 (PASS)
- 2018-A Q11 BLK-175E-2018A-001: coverage/2018-A.md L25 row + L159-L162 분석 + L286-L297 통계 + L306 ES-gap 표 + study-guide/2018-A.md L19·L40·L598·L629.
- 2024-B Q8 (을) BLK-175E-2024B-006: coverage/2024-B.md L350-L385 분석 + L541 row + L554 + L570 + L589 BLOCKER row · study-guide/2024-B.md L19·L51·L53 등.
- coverage 11파일 grep 합계 정확히 **2회** — Manager 의 "spec 3회 → 2회 정정" 판단은 정확. 다만 task-board L378 본문에 "blocker-log L168 false-positive 무효 처리" 언급이 있는데, 본 Reviewer 는 L168 직접 미검증 (검증 가치 낮음 — 핵심 결과는 2회 확증). PASS.

### 3. field=`western_ethics` (PASS)
- `ethics-fields` 실측 7건 only: `eastern_ethics`·`political_philosophy`·`moral_development`·`peace_studies`·`unification_edu`·`civic_edu`·`western_ethics`. **응용윤리·동물윤리 별도 field 없음** → western_ethics 채택 정확.
- 동물윤리 동등 사상가 `singer` (field=`western_ethics`) 및 환경윤리 `taylor_p` (field=`western_ethics`) 실측 일치 → 패턴 답습.

### 4. era=`현대` (PASS)
- ES `ethics-thinkers` 1900년대 출생 western_ethics 인물 era 실측: `singer`(1946)=현대 / `taylor_p`(1923)=현대 / `rawls`(1921)=현대 / `taylor` Charles(1931)=현대. regan(1938) 동일 era=현대 채택 정확.

### 5. 메타 (PASS)
- id=`regan` / name="톰 리건 (Tom Regan)" / name_en="Tom Regan" / birth=1938 / death=2017 / 미국 노스캐롤라이나주립대 — coverage/2024-B.md L354 + study-guide/2024-B.md L496 + blocker-log L949 verbatim 일치.

### 6. trademark 6종 verbatim 출처 (PASS · 단 #6 출처 명시 필요)
- ① 내재적 가치 — coverage/2018-A.md L161 + study-guide/2018-A.md L599·L603 + blocker-log L478·L950 verbatim.
- ② 삶의 주체 7기준 — coverage/2018-A.md L161 + study-guide/2018-A.md L599·L607 + blocker-log L478·L950 verbatim.
- ③ 존중의 원리 — coverage/2018-A.md L161·L162 + study-guide/2018-A.md L617·L629 + blocker-log L478 verbatim.
- ④ 해악의 원리 — coverage/2018-A.md L161·L162 + study-guide/2018-A.md L620·L629 + blocker-log L478 verbatim.
- ⑤ 의무론적 동물권 (싱어 비판) — coverage/2018-A.md L162 + study-guide/2018-A.md L621-L623 + blocker-log L478·L949 verbatim.
- ⑥ **권리 행사자(moral agents) vs 권리 보유자(moral patients)** — grep 결과 **blocker-log L479 단일 verbatim 출처**: "**권리 행사자[moral agents]/권리 보유자[moral patients] 구분**" (L479 후속 조치 항). coverage/study-guide 본문에는 없음. **Reviewer 권고**: task-board L378 trademark #6 설명에 출처 라인 "blocker-log L479" 를 명기하면 fabrication 의심을 사전 차단할 수 있음. 다만 verbatim 출처가 1곳이라도 존재하므로 **PASS** (제거·축소 불필요).

### 7. 저서 (PASS)
- 『동물권 옹호 (The Case for Animal Rights, 1983)』 7-9장 — coverage/2018-A.md L161·L306 + study-guide/2018-A.md L597·L599 + blocker-log L478 verbatim.

### 8. 선행 자료 line 정확 (PARTIAL PASS)
- coverage/2018-A.md L143-L165 (Q11 row + 분석) ✓ 정확 (L143 = 통일교육 Q8 시작이지만 Manager 는 일관되게 광역 범위 표기 — L159-L165 가 정확하지만 L143 부터 잡아도 무방).
- coverage/2018-A.md L286-L323 (ES-gap 표·BLOCKER 통계·한자 병기 예시) ✓ 정확.
- coverage/2024-B.md L354-L385 ✓ 정확.
- study-guide/2018-A.md L597-L629 ✓ 정확.
- blocker-log.md L474-L484 ✓ 정확 (BLK-175E-2018A-001 영역).
- **blocker-log.md "L585-L595 부근 (BLK-175E-2024B-006)" — INCORRECT.** 실제 BLK-175E-2024B-006 은 **L946-L952** (헤더 L946). L585-L595 은 BLK-175E-2020B-003 fazang. → **NEEDS_REVISION (line ref 정정 필요).**

### 9. BLOCKER 정정 대상 2 파일 (PARTIAL PASS · enumerate 미완)
- **2018-A study-guide regan BLOCKER 라인 (grep 실측)**:
  - L19 — `⚠️ ES 미등록 (1명 · BLOCKER) | regan (Q11) | BLOCKER-1(BLK-175E-2018A-001).`
  - L40 — 공지문 "Q11 regan (톰 리건) 만 ⚠️ES 미등록(BLOCKER-1)" 문구.
  - L598 — `⚠️ **ES 미등록(BLOCKER-1 · BLK-175E-2018A-001)**: regan canonical thinker_id 가 ES ethics-thinkers 인덱스에 미등록.`
  - L629 — `⚠️ **ES 미등록 (BLOCKER-1 · BLK-175E-2018A-001)**: regan canonical thinker_id 가 ES ethics-thinkers 인덱스에 미등록. curl 실측 found=false (404 NOT_FOUND). TASK-176 후속 등록 대기.`
  - **= 4 라인**. Manager spec 이 "L19·L40·L597·L598·L599·L629 부근 + 추가 grep 정확화 필요" 라고 적은 것은 부정확. **L597 (사상가 확정 줄)·L599 (Trademark 3중 일치) 는 BLOCKER 표기 라인 아님** — 정정 시 손대지 말 것 (단순 사상가 정보·trademark 출처 줄). **NEEDS_REVISION**.
- **2024-B study-guide regan BLOCKER 라인 (grep 실측 — Manager 가 미완)**:
  - L19 — 표 row "⚠️ ES 미등록 (1건 — BLOCKER 유지) | regan (Q8 을 · BLK-175E-2024B-006)"
  - L45 — 공지문 "regan 1명 BLOCKER 유지"
  - L51 — 섹션 heading `### Q8 (을) regan BLOCKER 유지`
  - L53 — `**Q8 (을)**: 리건 ... BLK-175E-2024B-006 등록 · trademark 직접 인용 금지.`
  - L496 — `⚠️ES 미등록 · BLOCKER-1 · BLK-175E-2024B-006` (을 사상가 줄)
  - L509 — `⚠️**ES 미등록 (BLOCKER-1 · BLK-175E-2024B-006)** ... 교과서 표준 해설로 일반 개념 제시`
  - L736 — Q8 row 표 `regan ⚠️BLOCKER-1 유지`
  - L743 — ES 상태 요약 "BLOCKER 1명 (regan)"
  - L745 — `regan(Q8 을 · BLK-175E-2024B-006)만 BLOCKER 유지`
  - L755 — `블로커 등록: ... (BLK-175E-2024B-006 regan 유지)`
  - **= 10 라인**. → Coder 가 정정해야 할 line 수 **2018-A 4 + 2024-B 10 = 14 라인**. Manager spec 의 "BLOCKER 표기 7 곳" (cho_sik/schumpeter 사례 답습한 표현) 은 본 태스크에선 부정확 — **2 파일 합 14 라인** 으로 정정 필요. **NEEDS_REVISION**.

### 10. claim_id ≥6 권장 (PASS)
- 6종 trademark 모두 출처 확보됨 (§6). claim_id ≥6 적정 (cho_sik=5·schumpeter=6 선례 일치).
- **trademark #6 권리 행사자 vs 권리 보유자**: 출처가 blocker-log L479 단일 verbatim 이지만 fabrication 아님. 다만 task-board description 에 "blocker-log L479 verbatim" 출처를 명기하면 안전.

### 11. DQ-027 next-numbered (PASS)
- data-quality-log.md 실측: L448 `## DQ-025 · cho_sik post-registration override` · L511 `## DQ-026 · schumpeter post-registration override` · DQ-027 부재. → **DQ-027** 채택 정확.

### 12. 스크립트 패턴 (PASS)
- `projects/ethics-study/scripts/` 실측: `insert_pettit.py` · `insert_singer.py` · `insert_cho_sik.py` · `insert_schumpeter.py` 모두 존재. 답습 가능.

### 13. 태스크 완결성·목적성·클린 아키텍처 (PARTIAL · §1·§8·§9 정정 후 PASS 가능)
- **목적성**: 1 사상가 1 ES 등록 + claim_id ≥6 + study-guide 14 라인 정정 + DQ-027 등록. ✓
- **완결성**: ES POST + 검증 + 정정 + DQ 등록 — Coder 가 외부 질문 없이 실행 가능 (line 정정 후).
- **클린 아키텍처**: scripts/ 분리 · ES 인덱스 정확 (`ethics-thinkers`·`ethics-claims`·`ethics-keywords`·`ethics-relations`·`ethics-works`) · 원본 (coverage 본문) 무수정·DQ override 만 — 규정 준수.

---

## 종합 판정

**verdict: NEEDS_REVISION**

### 정정 요구 사항 (Manager 가 task-board L378 description 수정)

1. **선행 자료 — blocker-log line 정정**:
   - 현재: "`blocker-log.md` **L474-L484** (BLK-175E-2018A-001) + L585-L595 부근 (BLK-175E-2024B-006)"
   - 정정: "`blocker-log.md` **L474-L481** (BLK-175E-2018A-001 · 헤더 L474) + **L946-L952** (BLK-175E-2024B-006 · 헤더 L946)"

2. **완료 조건 (2) 2 파일 BLOCKER 정정 enumerate 명시**:
   - 현재: "`study-guide/2018-A.md` (L19·L40·L597·L598·L599·L629 부근 + 추가 grep 정확화 필요) + `study-guide/2024-B.md` (regan BLOCKER 라인 grep 후 enumerate)"
   - 정정: 
     - `study-guide/2018-A.md` BLOCKER 라인 **4 곳**: **L19** 표 row · **L40** 공지 · **L598** ES 미등록 본문 · **L629** ES 미등록 footer. (L597 사상가 확정·L599 Trademark 출처 줄은 손대지 말 것)
     - `study-guide/2024-B.md` BLOCKER 라인 **10 곳**: **L19** 표 row · **L45** 공지 · **L51** 섹션 heading · **L53** 본문 BLOCKER 설명 · **L496** 을 사상가 줄 · **L509** ES 미등록 footer · **L736** Q8 표 row · **L743** ES 요약 · **L745** override 요약 · **L755** 블로커 등록 행.
     - **합계 14 라인 정정**.

3. **trademark #6 출처 라인 명기 (선택 권고)**:
   - 현재: "권리 행사자(moral agents) vs 권리 보유자(moral patients) 구분 — 도덕 주체와 도덕 환자의 권리 보유 평등성"
   - 권고: 끝에 "(blocker-log L479 verbatim 출처)" 추가 — Coder 가 fabrication 의심 없이 claim 작성 가능.

### 정정 후 즉시 PASS 가능 영역
§1·§2·§3·§4·§5·§6·§7·§10·§11·§12 — Manager 가 §1·§8·§9 (선행자료·완료조건) line refs 만 정정하면 §13 Clean Arch 도 PASS.

### Coder 호출 시점
위 3건 정정 후 Reviewer 재검증(R2) 없이도 Coder 발주 가능 — 정정 사항이 모두 line 번호 명세 (의미 변경 0건). 단, Manager 가 task-board L378 정정 commit 을 한 뒤 호출.
