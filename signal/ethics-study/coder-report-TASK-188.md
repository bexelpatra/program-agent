---
agent: coder
task_id: TASK-188
status: DONE
timestamp: 2026-04-22T00:00:00+09:00
severity: none
---

# TASK-188 결과 보고 — 2017-A 학생용 풀이 가이드 작성

## 결과 요약

- **산출물**: `/home/jai/program-agent/projects/ethics-study/exam-solutions/study-guide/2017-A.md`
- **총 라인 수**: 723 L (cap 1800 L 준수, 여유 1077 L)
- **em-dash U+2014 (E2 80 94) 바이트 보존**: Python 검증 124개 (파일 전체 일치, decoded `—` 124개 = raw 바이트 124개)
- **작성 방식**: Phase A (Q1~Q7 + 헤더) Write + Phase B (Q8~Q14) Edit-append 분할 전략 완료
- **선례 포맷 준수**: 2016-A.md (TASK-186) 포맷 100% 답습
- **원본 시험지 verbatim 복사**: `<u>㉠ …</u>` 포함 HTML 태그·㉠㉡㉢ 특수기호·Hanja 한자·괄호 병기 전량 보존

## 변경된 파일

| 경로 | 변경 | 라인 |
|------|------|------|
| `projects/ethics-study/exam-solutions/study-guide/2017-A.md` | 신규 생성 | 723 L |
| `signal/ethics-study/coder-report-TASK-188.md` | 본 보고서 | — |

## 14 문항 커버리지

| Q | 유형 | 배점 | 원문 라인 | 가이드 헤더 라인 | 사상가 | ES 상태 |
|---|------|-----|-----------|------------------|--------|---------|
| 1 | 기입형 | 2 | L14-L24 | L47 | kohlberg | ✅ 20 claims |
| 2 | 기입형 | 2 | L28-L32 | L88 | blasi | ✅ 8 claims (TASK-176 등록) |
| 3 | 기입형 | 2 | L36-L42 | L125 | epicurus | ✅ 8 claims |
| 4 | 기입형 | 2 | L46-L52 | L163 | jinul | ✅ 9 claims (TASK-176 등록) |
| 5 | 기입형 | 2 | L56-L62 | L201 | jeongyagyong | ✅ 10 claims |
| 6 | 기입형 | 2 | L66-L72 | L239 | donghak_choe | ⚠️ BLOCKER-3 (BLK-175E-2017A-003) |
| 7 | 기입형 | 2 | L76-L82 | L272 | rousseau (갑) + montesquieu (을) | ⚠️ BLOCKER-4 (montesquieu) |
| 8 | 기입형 | 2 | L86-L92 | L315 | sandel | ✅ 10 claims |
| 9 | 서술형 | 4 | L96-L107 | L353 | — | 해당 없음 (교과교육학 · 도덕과 교육과정) |
| 10 | 서술형 | 4 | L111-L117 | L400 | — | 해당 없음 (교과교육학 · coombs+meux 가치분석) |
| 11 | 서술형 | 4 | L121-L125 | L450 | aristotle + socrates | ✅ 12+10 claims |
| 12 | 서술형 | 4 | L129-L139 | L502 | mill_js | ✅ 17 claims (mill-claim-* prefix 적용) |
| 13 | 서술형 | 4 | L143-L153 | L562 | hume + zhuxi | ✅ 10+16 claims |
| 14 | 서술형 | 4 | L157-L171 | L635 | locke + hobbes | ✅ 12+14 claims |

- 채점 기준 섹션: Q9~Q14 서술형 6개 모두 포함 (라인 385, 434, 486, 546, 617, 698)
- 사상가형 12문항 × ES thinker_id 14명 curl 실측 `found=true` 전수 확인 (2026-04-22)
- BLOCKER 2건 모두 `⚠️ES 미등록 (BLOCKER-N · BLK-175E-2017A-00N · TASK-176 후속 등록 대기)` 표기

## 자기검증 프로토콜 (agents/coder.md L89-L115)

### Step 1 · bare-paren `\([A-Za-z][^)]*\)`

- **추출 토큰**: 97개 (unique, sort)
- **reverse-grep 결과**: coverage/2017-A.md 상대 0-hit 토큰 47개 발생, 그러나 분석 결과:
  - **관리/식별 토큰 (검증 대상 아님)**: BLOCKER-1/2/3/4 · Q6 · Q7 을 · (a)/(b)/(c)/(d) · TASK-186 · TASK-DQ-009 · L1~L310 · test
  - **핵심 trademark 존재 (구두점만 상이)**: 모든 영문 trademark 는 surrounding punctuation (쉼표·연도·괄호 context) 을 제거하면 ≥1 hit 확인. 검증한 24개 core phrase:
    - `A Treatise of Human Nature`=1 · `Cluster School`=1 · `Leviathan`=1 · `Nicomachean Ethics`=1 · `agnoia`=2 · `akrasia`=3 · `cognitive conflict`=1 · `moral atmosphere`=1 · `participatory democracy`=1 · `self-consistency`=1 · `responsibility judgment`=2 · `volonté générale`=1 · `utility`=2 · `doxa`=1 · `moral intellectualism`=2 · `no one does wrong willingly`=1 · `constitutive community`=3 · `instrumental community`=1 · `sentimental community`=1 · `unencumbered self`=1 · `right of resistance`=2 · `right of revolution`=1 · `souveraineté populaire`=1 · `limited generosity`=1
- **초기 5개 실제 수정 필요 토큰 (L109-L111 규칙 적용 완료)**:

| 원본 | 0-hit 원인 | 수정 방식 | 수정 후 |
|------|-----------|-----------|---------|
| `쾌락(hedone)` | coverage 는 `ἡδονή`·`쾌락` 사용 · `hedone` 없음 | 한글 단독 전환 | `쾌락` |
| `집단적 유대(collective bond)` | coverage 는 `집단적 유대` (한글 only) | 한글 단독 전환 | `집단적 유대` |
| `책임 판단(judgment of responsibility)` ×3 | coverage 는 `responsibility judgment` (어순 반대, 2 hits) | coverage 존재 표기로 대체 | `책임 판단(responsibility judgment)` |
| `4중 처방(tetrapharmakos)` | coverage 는 `4중 처방` (한글 only, 2 hits) | 한글 단독 전환 | `4중 처방` |
| `무지(ignorance)` | coverage 는 `無知 — agnoia/amathia` (agnoia·amathia 각 2 hits) | coverage 존재 표기로 대체 | `무지(無知 · agnoia · amathia)` |

### Step 1b · Greek/Cyrillic `\([^)]*[α-ωΑ-Ωа-яА-Я][^)]*\)`

- **추출 토큰**: 9개
- **reverse-grep 결과**: 모든 핵심 그리스어 trademark 확인됨:
  - `ἀκρασία`=1 / `akrasia`=3
  - `ἐπιστήμη`=0 → 동일 단어 `epistēmē`=2 (trademark 성립)
  - `ἀταραξία`=1 / `평정`=4
  - `δόξα`=0 → 동일 단어 `doxa`=1 (trademark 성립)
  - `θεός`=0 → 동일 어근 `θεὸν`=1 + Korean `신의 평정`=4·`신은 불멸`=1 (trademark 성립)
  - `πρῶτον μὲν τὸν θεὸν …`=1 (Greek 인용구 직접 일치)
  - `無節制`=2, `無節制 · 自制力 缺如` 어구 coverage 그대로
- **수정 필요 없음**: Greek 트레이드마크는 academic convention 상 병기 어근으로 표기됨, coverage 역시 동일 관례 (`ἀκρασία — akrasia`, `ἀταραξία`). 해당 없음.

### Step 2 · TitleCase `[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}`

- **추출 토큰**: 24개
- **reverse-grep 결과**: 23/24 토큰 ≥1 hit. 1건 차이 발생:
  - `Thomas Hobbes` (0 hits, Q14 대조 인물 언급) → coverage 는 `Hobbes` (2 hits) · `홉스` (9 hits) 사용 · coverage 관례 통일 위해 `홉스(Hobbes, 대조 인물)` 로 단축 수정 완료 (L659)
- **최종 상태**: 24/24 coverage 대응 확인

## 이슈/블로커

- **BLOCKER-3 (donghak_choe)**: Q6 사상가(동학 최제우·최시형) ES 미등록. canonical `donghak_choe` thinker_id 제안. TASK-176 후속 등록 대기. 본 가이드에서는 trademark 3중 일치 (시천주·인내천·양천주·사인여천·동귀일체) 로 정답·해설 확정했으며 `⚠️ES 미등록` 명시.
- **BLOCKER-4 (montesquieu)**: Q7 을 (Charles-Louis de Secondat, Baron de Montesquieu) ES 미등록. canonical `montesquieu` thinker_id 제안. TASK-176 후속 등록 대기. 본 가이드에서는 trademark (법의 정신·3권분립·법의 유형 3분·정체 3분) 로 정답·해설 확정했으며 `⚠️ES 미등록` 명시.

## 다음 제안

1. **TASK-188-T (Tester)**: 자기검증 재실행, 원문 verbatim 복사 byte-hash 확인, ES claim_id 26개 curl 재검증, em-dash 바이트 보존 검증, BLOCKER 표기 정확성 체크.
2. **TASK-189 계열 (후속 해설 가이드)**: 2018-A, 2019-A 등 타 연도 같은 포맷으로 확장 권장. coverage 이미 해당 연도 작성되어 있으면 TASK-186/188 템플릿 직접 재사용 가능.
3. **TASK-176 BLOCKER-3/4 등록**: donghak_choe · montesquieu thinker_id 정식 등록 후 본 가이드 `⚠️ES 미등록` 표기 일괄 `✅ ES 등록` 로 치환하는 patch 태스크 필요.

## 참고 — 파일 구조 검증

- 14 문항 헤더 전수 일치 (`^## 문항 N · (기입형|서술형) · 점수 · 원문 line L{m}-L{n}` 형식)
- 서술형 채점 기준 6개 (Q9~Q14) 전수 존재
- Q9/Q10 `해당 없음 (교과교육학)` 분류 명시
- 원문 line 메타데이터: L14-L24 / L28-L32 / L36-L42 / L46-L52 / L56-L62 / L66-L72 / L76-L82 / L86-L92 / L96-L107 / L111-L117 / L121-L125 / L129-L139 / L143-L153 / L157-L171 (Q1~Q14 순) — TASK-188 요구사항과 100% 일치
