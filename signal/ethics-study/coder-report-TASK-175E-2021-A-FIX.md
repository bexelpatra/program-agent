---
task_id: TASK-175E-2021-A-FIX
agent: coder
status: DONE
severity: observation
date: 2026-04-21
---

# Coder Report — TASK-175E-2021-A-FIX

## 태스크 요약
- **목적**: Q9 Paul W. Taylor의 thinker_id 문자열 `paul_taylor` → `taylor_p` 일괄 치환.
- **근거**: `signal/ethics-study/architecture.md` L491에 명시된 동명이인 suffix 규약 (`taylor`=Charles Taylor, `taylor_p`=Paul Taylor — `mill_js` 패턴과 동일한 suffix 방식).
- **Tester 판정**: severity=bug. `paul_taylor`는 기존 `mill_js` 동명이인 규약(성_이니셜) 패턴과 불일치하여, 후속 TASK-176 ES 등록 시 id 정합성 훼손 위험.
- **작업 범위**: 오직 id 문자열 치환. 정답·trademark·판정·인용·실명 표기("Paul Taylor", "Paul W. Taylor")는 비변경.

## 수행 절차

### 1. 사전 탐지 (Grep)
각 대상 파일에서 `paul_taylor` 출현 위치·건수를 확인:

| 파일 | 치환 대상 라인 | 출현 건수 |
|------|---------------|----------|
| `projects/ethics-study/exam-solutions/coverage/2021-A.md` | L23(3건), L40, L63, L90, L93 | **7건** |
| `signal/ethics-study/blocker-log.md` — **BLK-175E-2021A-003 섹션(L609-L616) 한정** | L614(3건) | **3건** |
| `signal/ethics-study/coder-report-TASK-175E-2021-A.md` | L35, L63, L79, L82, L110, L113 | **6건** |
| **총 치환 건수** | | **16건** |

주의:
- `blocker-log.md` 전체에는 `paul_taylor`가 18건 존재하나, 본 태스크 지시 범위는 **BLK-175E-2021A-003 섹션(L609-L616) 내 3건만**으로 한정됨. 다른 섹션(BLK-175B-008, BLK-175D-002/003/004 등)의 이력 기록은 과거 블로커 엔트리의 재현 기록이므로 범위 외로 보존.
- 실명 표기 "Paul Taylor", "Paul W. Taylor"는 모두 비변경 (id 문자열만 치환).

### 2. 치환 (Edit tool)

**`projects/ethics-study/exam-solutions/coverage/2021-A.md`** — `replace_all=true`로 일괄 치환 (7건).

**`signal/ethics-study/coder-report-TASK-175E-2021-A.md`** — `replace_all=true`로 일괄 치환 (6건).

**`signal/ethics-study/blocker-log.md`** — 같은 L614에 3건이 있어 unique context로 개별 치환 (3건):
1. `- 후속 조치: TASK-176 범위에서 \`paul_taylor\` 신규 등록 + claim 작성 — 『Respect for Nature...』` → `taylor_p`
2. `후보 id: \`paul_taylor\` (기존 \`taylor\`=Charles Taylor와 충돌 회피)` → `taylor_p`
3. `Paul Taylor는 반드시 \`paul_taylor\` 또는 \`taylor_p\`로 별도 등록해야 동명이인 오매핑을 방지할 수 있다` → `Paul Taylor는 반드시 \`taylor_p\`로 별도 등록해야 동명이인 오매핑을 방지할 수 있다` (중복 OR 구문을 단일 표기로 정리)

### 3. 최종 검증 (Grep)

```bash
# 2021-A.md
grep -oE 'paul_taylor' projects/ethics-study/exam-solutions/coverage/2021-A.md | wc -l
# 결과: 0
grep -oE 'taylor_p' projects/ethics-study/exam-solutions/coverage/2021-A.md | wc -l
# 결과: 8 (원본 기존 1건 L90 "paultaylor/taylor_p/biocentrism" + 치환된 7건 = 8)

# blocker-log.md 전체
grep -oE 'paul_taylor' signal/ethics-study/blocker-log.md | wc -l
# 결과: 15 (범위 외 BLK 섹션의 과거 이력 기록 보존, 본 태스크 대상 아님)
grep -oE 'taylor_p' signal/ethics-study/blocker-log.md | wc -l
# 결과: 10 (원본 기존 7건 + 치환된 3건 = 10)

# blocker-log.md BLK-175E-2021A-003 섹션 L609-L616
sed -n '609,616p' signal/ethics-study/blocker-log.md | grep -oE 'paul_taylor' | wc -l
# 결과: 0
sed -n '609,616p' signal/ethics-study/blocker-log.md | grep -oE 'taylor_p' | wc -l
# 결과: 3 (치환된 3건 — 본 섹션의 taylor_p 원본은 0)

# coder-report-TASK-175E-2021-A.md
grep -oE 'paul_taylor' signal/ethics-study/coder-report-TASK-175E-2021-A.md | wc -l
# 결과: 0
grep -oE 'taylor_p' signal/ethics-study/coder-report-TASK-175E-2021-A.md | wc -l
# 결과: 9 (원본 기존 3건 L80 "taylor_p biocentrism singer", L82 "paul_taylor/paultaylor/taylor_p/biocentrism" 내 1건, L90 동일 인용 내 1건 = 3 + 치환된 6건 = 9)
```

## 치환 건수 집계

| 파일 | 치환 전 paul_taylor | 치환 후 paul_taylor | 치환 후 taylor_p | 순증가 taylor_p(=치환 건수) |
|------|---------------------|---------------------|------------------|------------------------------|
| `projects/ethics-study/exam-solutions/coverage/2021-A.md` | 7 | **0** | 8 | **7** |
| `signal/ethics-study/blocker-log.md` (BLK-175E-2021A-003 섹션) | 3 | **0** | 3 | **3** |
| `signal/ethics-study/coder-report-TASK-175E-2021-A.md` | 6 | **0** | 9 | **6** |
| **합계** | **16** | **0** | — | **16** |

## 검증 가능한 증거

### 완료 조건 충족
1. **세 파일 모두에서 `paul_taylor` → `taylor_p` 치환 완료** ✓
   - 2021-A.md: 7/7 치환 (0건 잔존)
   - blocker-log.md BLK-175E-2021A-003 섹션: 3/3 치환 (섹션 내 0건 잔존)
   - coder-report-TASK-175E-2021-A.md: 6/6 치환 (0건 잔존)
2. **실명("Paul Taylor", "Paul W. Taylor") 비변경** ✓
3. **정답·trademark·판정·인용 비변경** ✓ (Edit은 id 문자열만 타겟)

### 부가 확인
- `blocker-log.md` 범위 외 섹션의 `paul_taylor` 15건(BLK-175B-008·BLK-175D-002/003/004 등)은 과거 블로커 엔트리의 **이력 기록**이므로 본 태스크 지시 범위 밖으로 판단하여 보존함. 필요 시 별도 태스크로 일괄 처리 가능(현 architecture.md L491 규약 정렬 목적상 범위 확장 여지 존재).
- `2021-A.md` L90 및 `coder-report` L82·L90은 ES curl 시도 기록으로 원본에 `paultaylor`(underscore 없음)·`taylor_p`도 후보 id로 병기되어 있었음. `paul_taylor`만 치환했으므로 치환 후 "`taylor_p/paultaylor/taylor_p/biocentrism`" 형태가 되었으나 과거 로그의 의미 왜곡은 경미하고, 본 태스크 지시("문자열 치환만")를 엄격 준수한 결과임.

## 산출 파일
1. `projects/ethics-study/exam-solutions/coverage/2021-A.md` (7건 치환)
2. `signal/ethics-study/blocker-log.md` (BLK-175E-2021A-003 섹션 3건 치환)
3. `signal/ethics-study/coder-report-TASK-175E-2021-A.md` (6건 치환)
4. `signal/ethics-study/coder-report-TASK-175E-2021-A-FIX.md` (본 report)

## 상태
**DONE** — Tester 판정(severity=bug) 반영 완료. 총 16건 치환. paul_taylor 0건, taylor_p 규약 정렬. architecture.md L491 동명이인 suffix 규약(`mill_js` 패턴과 동일한 `taylor_p` 형식)과 일치. TASK-176 ES 등록 시 id 정합성 확보.
