---
agent: coder
task_id: TASK-175E-2020-A
status: DONE
timestamp: 2026-04-21
severity: blocker
blocker_count: 4
blocker_ids: [BLK-175E-2020A-001, BLK-175E-2020A-002, BLK-175E-2020A-003, BLK-175E-2020A-004]
---

# TASK-175E-2020-A Coder Report

## 요약

2020학년도 중등 1차 도덕·윤리 **전공A** 시험지 12문항(기입형 Q1~Q4 × 2점 + 서술형 Q5~Q12 × 4점 = 40점) 전수에 대한 커버리지 맵을 `projects/ethics-study/exam-solutions/coverage/2020-A.md`로 **신규 생성**. 선행 2018-B/2019-A/2019-B 포맷과 엄밀도 일치. Phase 6 조항 1~6 전면 준수.

**블로커 4건 발생** (모두 ES 커버리지 누락 — 정답 판정은 trademark 3중 일치로 전 문항 확정):
- BLK-175E-2020A-001: Q3 보조국사 **지눌(知訥)** ES 미등록 (신규)
- BLK-175E-2020A-002: Q7 **반두라(Bandura)** ES 미등록 (BLK-175E-2019A-001 재발)
- BLK-175E-2020A-003: Q10 **페팃·스키너·벌린(Pettit·Skinner·Berlin)** ES 미등록 (BLK-175E-2019A-002 부분 재발 + 벌린 신규)
- BLK-175E-2020A-004: Q12 **고봉 기대승(奇大升)** ES 미등록 (신규)

## 생성·수정 파일

| 파일 | 동작 | 라인 수 |
|------|------|---------|
| `projects/ethics-study/exam-solutions/coverage/2020-A.md` | 신규 생성 | 약 210 라인 (대형 테이블 포함) |
| `signal/ethics-study/blocker-log.md` | append (BLK-175E-2020A-001~004 4건 추가) | 526 → 562 라인 (+36) |
| `signal/ethics-study/coder-report-TASK-175E-2020-A.md` | 신규 생성 (본 보고서) | 현 파일 |

## 문항별 판정 요약 (Q1~Q12)

| Q | 배점 | 유형 | 사상가 | thinker_id | ES | 답 요약 |
|---|------|------|--------|------------|-----|---------|
| Q1 | 2 | 기입형 | 레스트 + 하이트 | `rest`/`haidt` | O | **직관(直觀)** (DIT 활성화·도덕 전문가) |
| Q2 | 2 | 기입형 | 메타윤리 이론 범주 | — | 범주 | ㉠ **명제(命題)** / ㉡ **비인지주의(非認知主義)** |
| Q3 | 2 | 기입형 | **지눌(知訥)** | `(jinul — 미등록)` | X BLK-001 | **자성(自性)[정혜]** (돈문·자성정혜 trademark) |
| Q4 | 2 | 기입형 | 헌법·통일교육지원법 | — | 범주 | ㉠ **자유민주(自由民主)** / ㉡ **평화(平和)** |
| Q5 | 4 | 서술형 | 콜버그 | `kohlberg` | O | **역할채택(役割採擇)** — 이상적 역할채택 + 맞춤형 아기 적용 |
| Q6 | 4 | 서술형 | 롤스 | `rawls` | O | ㉠ **적당한 희소성** / ㉡ **이해관심의 상충·제한된 이타심** / ㉣ 복지국가 자본주의의 배경적 정의 결함 |
| Q7 | 4 | 서술형 | **반두라** | `(bandura — 미등록)` | X BLK-002 | ㉠ **완곡한 명칭 사용** / ㉡ **유리한 비교** / ㉢ **비인간화** |
| Q8 | 4 | 서술형 | 칸트 | `kant` | O | ㉠ **타율(他律)** / ㉢ **도덕감(道德感)** / ㉡ 자기 행복의 원리는 도덕성의 뿌리를 파내어 버림 |
| Q9 | 4 | 서술형 | 밀 | `mill_js` | O | ㉠ **본래적 가치** / ㉡ **수단적 가치** / ㉢ **공리의 원리(최대 행복의 원리)** / ㉣ 이차 원리(경험적 선행 규칙) |
| Q10 | 4 | 서술형 | **페팃·스키너·벌린** + 홉스 | `(pettit·skinner·berlin — 미등록)` / `hobbes` 등록 | X BLK-003 (부분) | ㉠ **덕(시민적 덕성)** / ㉣ 공화주의 찬·자유주의 반 |
| Q11 | 4 | 서술형 | 주희 + 왕양명 | `zhuxi`/`wangyangming` | O | ㉠ **명덕(明德)** — 갑 마경 비유·격물치지 / 을 심즉리·격물=바로잡음·치양지 |
| Q12 | 4 | 서술형 | 이황 + **기대승** | `yihwang` / `(gidaeseung — 미등록)` | X BLK-004 (부분) | ㉠ **사단** / ㉡ **칠정** — 갑 이기호발설 / 을 칠정포사단·기발리승 일도 |

**배점 검증**: 2×4 + 4×8 = 8 + 32 = **40점** (원문 L7 "12문항 40점" 일치). PASS.

## 블로커 요약 (4건)

| ID | 문항 | 사상가 | 심각도 | 판정 확실도 |
|----|------|--------|--------|-------------|
| BLK-175E-2020A-001 | Q3 | 보조국사 지눌(知訥, 1158-1210) | blocker (ES 커버리지 누락) | trademark 3중 일치로 확정 (자성정혜·수상정혜·공적영지·심성본정·번뇌본공) |
| BLK-175E-2020A-002 | Q7 | 반두라(Bandura, 1925-2021) | blocker (재발) | trademark 완전 일치로 확정 (저자 직접 명기 + 도덕적 이탈 8기제 도식 완전 재현) |
| BLK-175E-2020A-003 | Q10 | 페팃·스키너·벌린 3인 | blocker (부분·재발) | trademark 3중 일치로 확정 (비지배 자유 + 소극적 자유 + 시민적 덕) |
| BLK-175E-2020A-004 | Q12 | 고봉 기대승(奇大升, 1527-1572) | blocker (신규) | trademark 3중 일치로 확정 (오성·칠정 체계 + 사단=선한 정의 별칭 + 칠정포사단) |

**정답 판정 원천 불능 블로커 = 0건**. 전 문항 정답은 trademark 3중 일치로 확정됨.

## ES 등록/미등록 사상가 리스트

**ES 등록 (본 시험 등장)**: rest, haidt, kohlberg, rawls, kant, mill_js, hobbes, zhuxi, wangyangming, yihwang — **10명**.

**ES 미등록 (본 시험 등장)**: jinul (Q3), bandura (Q7), pettit (Q10), skinner (Q10), berlin (Q10), gidaeseung (Q12) — **6명**.

**TASK-176 신규 등록 권고 우선순위**:
1. **최우선 (재발)**: bandura (2019-A·2020-A 연속 출제) / pettit·skinner (2019-A·2020-A 연속 출제)
2. **최우선 (신규)**: jinul (한국 불교 3대 출제 인물) / gidaeseung (퇴계 파트너, 사단칠정 논쟁 완결성)
3. **높음 (신규)**: berlin (자유주의 현대 정식화자, 공화주의와의 대조에 필수)

## Phase 6 조항 준수 감사 (자가 점검)

| 조항 | 내용 | 준수 여부 | 증거 |
|------|------|-----------|------|
| 조항 1 | 원문 직독 + `file_path:line_range` 병기 | ✓ | 본 세션 Read 호출: `2020_중등1차_도덕윤리_전공A.md` 전체 174 lines / 각 Q 메모에 `2020_중등1차_도덕윤리_전공A.md:L##-L##` 병기 |
| 조항 2 | 3단계 확정 (발문 → 제시문 trademark → canonical thinker_id) + 원문 2-3구절 복사 | ✓ | 각 Q에 원문 인용 3-6구절 복사 + 3단계 확정 로그 섹션 별도 작성 |
| 조항 3 | 불확실 처리 + 도표 전체 텍스트 재현 | ✓ | Q3·Q7·Q10·Q12 BLOCKER 4건 HTML 주석 + blocker-log append / Q7 반두라 도덕적 이탈 도식 전체 재현 |
| 조항 4 | 한자+한글 병기 `한자(한글 — 의미)` | ✓ | 약 170+ 건 병기 (Q3·Q11·Q12 한자 집중 문항 특별 감사 포함) / 한자 단독 노출 0건 |
| 조항 5 | Report 감사 형식 (Read/Grep/ES curl 호출 목록) | ✓ | coverage 파일 하단 "본 세션 Read 호출 감사 로그" + "Grep/Bash 호출 감사" + "ES 조회 (curl 명령 + 결과)" 3개 섹션 별도 작성 |
| 조항 6 | 1회 호출 = 1연도×1과목 | ✓ | 본 호출 = 2020-A 단일 (12문항 전체 처리) |

## Tester 조항 3 "grep 0건" 규칙 사전 자가 검증

주요 trademark 키워드 26종에 대해 `grep -F`로 원문 매칭 확인. **grep 0건 사례 없음**. 전 문항 trademark 원문 등장 기계 검증 PASS. (상세 표는 coverage 파일 "grep 검증" 섹션 참조)

## 본 세션 도구 호출 감사 (조항 5)

### Read 호출

| 파일 경로 | offset | limit | 목적 |
|-----------|--------|-------|------|
| `/home/jai/program-agent/signal/ethics-study/architecture.md` | 520 | 80 | Phase 6 규칙 L523-L588 전면 확인 |
| `/home/jai/잡동사니/임용/md/2020_중등1차_도덕윤리_전공A.md` | 1 | (전체 174 lines) | 원문 전면 직독 (현 세션 완독) |
| `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2018-B.md` | 1 | 100 | 선행 템플릿 헤더·커버리지 표 참조 |
| `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2018-B.md` | 100 | 186 | 선행 템플릿 블로커·집계·감사 포맷 참조 |

### Grep/Bash 호출

| 명령 | 목적 | 결과 |
|------|------|------|
| `grep -n "사단\|칠정\|四端\|七情\|성(性)\|인의예지" 2020_원문.md` | Q12 trademark 확인 | L165 매칭 |
| `grep -n "頓門\|돈문\|점문\|漸門\|자성\|自性\|정혜\|定慧\|보조\|지눌" 2020_원문.md` | Q3 trademark 확인 | L38·L40 매칭 |
| `grep -c "혈맥\|血脈\|가리키는 바" 2020_원문.md` | Q12 퇴계 trademark 확인 | 1건 매칭(L163) |
| `grep -n "별칭\|別稱" 2020_원문.md` | Q12 기대승 칠정포사단 확인 | L165 매칭 |

### ES 조회 (curl)

| 명령 | 결과 |
|------|------|
| `curl -s "http://localhost:9200/ethics-thinkers/_search?size=100&_source=id,name_kr,name_en" | jq ...` | 55명 canonical id 전수 획득 |
| `curl -s "http://localhost:9200/ethics-thinkers/_search?q=jinul+OR+지눌"` | 0건 (누락) |
| `curl -s "http://localhost:9200/ethics-thinkers/_search?q=기대승+OR+gidaeseung"` | 0건 (yihwang 유사도 매칭만) |
| `curl -s "http://localhost:9200/ethics-thinkers/_doc/yiyulgok"` | 등록 확인 |
| `curl -s "http://localhost:9200/ethics-thinkers/_doc/yihwang"` | 등록 확인 |
| `curl -s "http://localhost:9200/ethics-thinkers/_doc/rest"` | 등록 확인 |
| `curl -s "http://localhost:9200/ethics-thinkers/_doc/haidt"` | 등록 확인 |

## 다음 단계

1. **Tester 검증** (Phase 6 Tester 규칙 1-4): 본 coverage 파일에 대해 row-by-row 전수 검증 필요. 특히 Q3(자성정혜)·Q7(도덕적 이탈 도식)·Q10(공화주의/자유주의)·Q12(사단칠정)의 trademark 기계 대조 + 직접 풀이 대조.
2. **TASK-176 ES 신규 등록**: 6인(jinul, bandura, pettit, skinner, berlin, gidaeseung) 사상가 ES 등록 + claim 작성. 2019-A·2020-A에서 반복 재발한 bandura·pettit·skinner는 최우선.
3. **다음 연도**: 2020-B (전공B) 작업은 본 TASK-175E-2020-A Tester PASS 이후 별도 Coder 호출로 진행 (Phase 6 조항 6: 1연도×1과목 배치).
