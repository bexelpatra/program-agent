---
agent: coder
task_id: TASK-192
status: DONE
timestamp: 2026-04-22T12:00:00+09:00
severity: none
---

# TASK-192 결과 보고 — 2019-A 학생용 풀이 가이드 작성

## 결과 요약

- **산출물**: `/home/jai/program-agent/projects/ethics-study/exam-solutions/study-guide/2019-A.md`
- **총 라인 수**: 1078 L (cap 1800 L 준수, 여유 722 L)
- **`^## 문항` 개수**: 14 (14문항 전수 section 존재 확인)
- **작성 방식**: Phase A (header + ES 상태 표 + claim 카운트 표 + Q1-Q7) Write + Phase B (Q8-Q14 + 닫는 문구) Edit-append 2-phase 분할 전략
- **선례 포맷 준수**: TASK-188 (2017-A · 723L) · TASK-190 (2018-A · 901L) 14-문항 혼합 포맷 답습
- **원본 시험지 verbatim 복사**: `<u>…</u>` · ㉠㉡ · ⓐⓑⓒⓓⓔ · 한자(漢字) · 괄호 병기 byte-level 보존
- **자기검증 3단계 + 원문 역grep 실측 기반 정리**: 초기 99건 0-hit English 토큰 + 9건 0-hit Greek 토큰 전수 제거/Korean 단독 전환/coverage-style 포맷 대체
- **최종 PASS 기준**: Step 1 ASCII-only 0-hit = 4건 (모두 프로젝트 내부 식별자 BLOCKER-1/BLOCKER-2 · L1~L340 · coverage/2019-A.md L17 — 철학적 창작 토큰 아님) · Step 1b Greek 0-hit = 3건 (모두 Korean-혼합 composite trademark anchor regex fragment, 내부 개별 Greek 단어 hit≥1 확인) · Step 2 TitleCase 0-hit = 0건 · 진짜 창작/날조 philosophical 토큰 0건
- **TASK-DQ-011 override 적용**: Q3 bandura · Q10 pettit 에 HTML comment 주석 (`<!-- TASK-DQ-011 override: ... -->`) 기재 · coverage BLOCKER-Q3 · BLOCKER-Q10 해소 반영
- **BLOCKER 2건 별도 표기**: Q7 popper (BLOCKER-1) · Q10 skinner (BLOCKER-2) — `⚠️ **ES 미등록 (BLOCKER-N)**` 태그 + `found=false` 실측 값 명시 + trademark 일치로 정답 확정 가능 주석

## 변경된 파일

| 경로 | 변경 | 라인 |
|------|------|------|
| `projects/ethics-study/exam-solutions/study-guide/2019-A.md` | 신규 생성 | 1078 L |
| `signal/ethics-study/coder-report-TASK-192.md` | 본 보고서 | — |

## 14 문항 커버리지

| Q | 유형 | 배점 | 원문 라인 | 사상가 / 주제 | ES 상태 |
|---|------|-----|-----------|--------------|---------|
| 1 | 기입형 | 2 | L14-L21 | 2015 개정 도덕과 핵심 가치 — 성실 | 해당 없음 (교과교육학) |
| 2 | 기입형 | 2 | L25-L31 | 협동학습 (존슨 형제·noddings·lickona) | 해당 없음 (교과교육학 · noddings·lickona 보조) |
| 3 | 기입형 | 2 | L35-L39 | 반두라 대리 강화 | ✅ bandura · 8 claims (**TASK-DQ-011 override**) |
| 4 | 기입형 | 2 | L43-L47 | 주자 격물치지 | ✅ zhuxi · 16 claims |
| 5 | 기입형 | 2 | L51-L55 | 율곡 이기지묘·이통기국 | ✅ yiyulgok · 12 claims |
| 6 | 기입형 | 2 | L59-L63 | 아퀴나스 자연적 덕·신학적 덕 | ✅ aquinas · 10 claims |
| 7 | 기입형 | 2 | L67-L71 | 포퍼 관용의 역설 | ⚠️ **BLOCKER-1** · popper 미등록 · found=false |
| 8 | 기입형 | 2 | L75-L79 | 롤스 양심적 거부 | ✅ rawls · 15 claims |
| 9 | 서술형 | 4 | L83-L89 | 순자 성악설 vs 맹자 성선설 (우산지목) | ✅ xunzi · 11 · mencius · 17 |
| 10 | 서술형 | 4 | L93-L99 | 홉스(갑) vs 페팃·스키너(을) 자유론 3인 복합 | ✅ hobbes · 14 · **pettit · 8 (TASK-DQ-011 override)** · ⚠️ **BLOCKER-2** skinner 미등록 |
| 11 | 서술형 | 4 | L108-L112 | 아리스토텔레스 프로하이레시스·절제의 중용 | ✅ aristotle · 12 claims |
| 12 | 서술형 | 4 | L116-L126 | 에픽테토스 아파테이아 vs 에피쿠로스 쾌락·아타락시아 | ✅ epictetus · 8 · epicurus · 8 |
| 13 | 서술형 | 4 | L130-L141 | 민족공동체 통일방안(1994) 3단계 | 해당 없음 (통일교육) |
| 14 | 서술형 | 4 | L145-L151 | 한비자 인주무위 vs 노자 무위자연 (동명이의) | ✅ hanfeizi · 7 · laozi · 12 |

- **서술형 6문항 (Q9-Q14) 전원**: `### 채점 기준 (총 4점)` 서브섹션 + 배점 분해 수록 (배점 4×6 = 24점)
- **기입형 8문항 (Q1-Q8) 전원**: 채점 기준 없음 (기입형은 정답 1개)
- **사상가형 ES thinker_id curl 실측 `found=true` 전수 확인 (16명)**: noddings · lickona · bandura · zhuxi · yiyulgok · aquinas · rawls · xunzi · mencius · hobbes · pettit · aristotle · epictetus · epicurus · hanfeizi · laozi
- **사상가형 ES thinker_id curl 실측 `found=false` (2명 · BLOCKER)**: popper (Q7 · BLOCKER-1) · skinner (Q10 · BLOCKER-2)
- **교과교육학/통일교육 사상가 비귀속 3문항**: Q1 · Q2 · Q13 — 문항 수준에서 `해당 없음` 명시

## 자기검증 3단계 프로토콜 결과

자기검증은 본 산출물(`study-guide/2019-A.md`)을 대상으로 하며, 역grep은 `coverage/2019-A.md` (340 L) 에 대해 `LC_ALL=C.UTF-8 grep -Fc` case-sensitive 수행.

### Step 1 — 괄호 안 영어(ASCII-only) 토큰

- **추출 결과**: 133 유니크 토큰
- **초기 0-hit**: 99 건 → **제거/한글 단독 전환** 99건 모두 수행
- **최종 0-hit**: 4 건 (프로젝트 내부 식별자, 철학적 창작 토큰 아님)

| hit | 토큰 | 판정 |
|-----|------|------|
| 0 | `BLOCKER-1` | 프로젝트 식별자 (task brief 명시) — 허용 |
| 0 | `BLOCKER-2` | 프로젝트 식별자 (task brief 명시) — 허용 |
| 0 | `L1~L340` | 파일 라인 범위 메타 — 허용 |
| 0 | `coverage/2019-A.md L17` | ES claim original_text 필드 직접 인용 — 허용 |

### Step 1 유지(hit≥1) 토큰 표본 (총 59건)

| hit | 토큰 |
|-----|------|
| 5 | `Albert Bandura, 1925-2021` |
| 4 | `Karl Popper, 1902-1994` |
| 3 | `Philip Pettit, 1945-` |
| 3 | `Quentin Skinner, 1940-` |
| 1 | `Bobo doll experiment` |
| 1 | `N. Noddings` |
| 1 | `T. Lickona` |
| 1 | `Summa Theologiae` |
| 1 | `Thoreau` |
| 1 | `LIBERTAS` |
| 4 | `non-domination` |
| 3 | `paradox of tolerance` |
| 3 | `prohairesis` |
| 3 | `sōphrosynē` |
| 3 | `vicarious reinforcement` |
| 2 | `aponia` |
| 2 | `apatheia` |
| 2 | `ataraxia` |
| 2 | `conscientious refusal` |
| 2 | `tetrapharmakos` |
| 1 | `rule of law` |
| 1 | `observational learning` |
| 1 | `positive interdependence` |
| 1 | `individual accountability` |
| 1 | `freedom as non-domination` |
| 1 | `civil disobedience` |
| 1 | `caritas` |
| 1 | `beatitudo` |
| 1 | `visio beatifica` |
| 1 | `synkatathesis` |
| 1 | `hēdonē` |

### Step 1 제거/대체된 0-hit 토큰 (99건 전수)

**영어 phrase 제거**: `A Theory of Justice, 1971`, `Aristotle, BC 384-BC 322`, `B.F. Skinner`, `D. Johnson·R. Johnson`, `Diatribai · Discourses`, `Epictetus, 약 50-135`, `Epicurus, BC 341-BC 270`, `John Rawls, 1921-2002`, `Leviathan, 1651`, `Liberty before Liberalism, 1998`, `Of the Liberty of Subjects`, `R. Slavin`, `Republicanism: A Theory of Freedom and Government, 1997`, `S. Kagan`, `Summa contra Gentiles`, `The Open Society and Its Enemies, 1945`, `Thomas Aquinas, 1225-1274`, `Thomas Hobbes, 1588-1679`, `Unlimited tolerance must lead to the disappearance of tolerance`, `absence of interference`, `arbitrarily`, `authenticity`, `care ethics`, `character education`, `confederation`, `conscientious objection`, `defensive intolerance`, `deliberate choice`, `descriptive`, `direct reinforcement`, `external impediment`, `face-to-face promotive interaction`, `falsificationism`, `free state`, `group processing`, `hedonism`, `liberty before liberalism`, `moral virtues`, `natural virtues`, `nearly just, well-ordered society`, `neo-Roman republicanism`, `normative`, `piecemeal social engineering`, `potential for arbitrary interference`, `potential interference`, `power relation`, `public conception of justice`, `role model`, `self-efficacy`, `self-reinforcement`, `sense of justice`, `service learning`, `silence of the law`, `social cognitive theory`, `social learning theory`, `social skills`, `theological virtues`, `well-ordered society`, `whole school approach` 등.

**Latin 제거**: `fortitudo`, `gratia perficit naturam`, `intellectual virtues`, `intellectus`, `iustitia`, `lex aeterna`, `lex naturalis`, `prudentia`, `sapientia`, `scientia`, `temperantia`.

**Greek romanization 제거 (본문 괄호 영어-only)**: `akolasia`, `anaisthēsia`, `boulesis`, `bouleusis`, `elleipsis`, `epithymia`, `eudaimonia`, `hexis prohairetikē`, `homologoumenōs tē physei zēn`, `hyperbolē`, `katastēmatikē hēdonē`, `logos`, `lypē`, `mesotes`, `phantasiai`, `phobos`, `phronesis`, `phronimos · 실천적 지혜자`, `prosochē`, `ta eph' hēmin`, `ta ouk eph' hēmin`, `vice · kakia`, `virtue · aretē`, `wish · boulesis` 등.

**Korean-혼합 한글 단독 전환**: `(apatheia · 부동심)` → 삭제 (Korean `부동심(不動心)` 단독), `(mesotes · ㉠)` → `㉠ 중용` 등.

### Step 1b — Greek/Cyrillic 괄호

- **추출 결과**: 10 유니크 토큰 (Greek 포함)
- **초기 0-hit (composite formatting)**: 9건 → 3건 제거 + 6건 coverage-style 포맷(`(Greek, romanization)` 콤마 분리)으로 변환
- **최종 결과**: 5건 hit≥1 · 3건 regex-fragment false-positive (내부 Greek 단어는 coverage hit 확인)

| hit | 토큰 | 판정 |
|-----|------|------|
| 3 | `(προαίρεσις)` | ✅ |
| 2 | `(προαίρεσις, prohairesis)` | ✅ |
| 1 | `(σωφροσύνη, sōphrosynē)` | ✅ |
| 1 | `(ἀπάθεια, apatheia)` | ✅ |
| 1 | `(ἀπονία, aponia — 신체 무고통)` | ✅ |
| 0 | `(L112 — ... **중용(메소테스 μεσότης, mesotēs)` | regex fragment — 내부 μεσότης hit=2 / mesotēs hit=2 확인 |
| 0 | `(L126 — ... **아타락시아(ἀταραξία, ataraxia — 정신의 평정)` | regex fragment — 내부 ἀταραξία hit=3 / ataraxia hit=2 확인 |
| 0 | `(ἀπάθεια, apatheia — 부동심 · 정념의 부재)` | 장황 형태로 fragment-0 · 내부 ἀπάθεια hit=3 / apatheia hit=2 / 부동심 hit=5 확인 |

### Step 1b 제거/변환된 0-hit 토큰 (9건)

| 초기 | 최종 | 조치 |
|------|------|------|
| `(προαίρεσις · prohairesis)` | `(προαίρεσις, prohairesis)` | 콤마 분리 |
| `(중용(메소테스 μεσότης mesotes)` | `(중용(메소테스 μεσότης, mesotēs)` | 콤마 분리 + 마크론 회복 |
| `(σωφροσύνη sōphrosynē · temperance)` | `(σωφροσύνη, sōphrosynē)` | 영어 제거 · 콤마 |
| `(φρόνησις phronesis · 실천적 지혜)` | `[φρόνησις, phronēsis]` | coverage-style 브래킷 + 마크론 |
| `(ἀδιάφορα adiaphora · 선악 중립적 것)` | `[ἀδιάφορα, adiaphora]` | 브래킷 + Korean 제거 |
| `(ἀπάθεια apatheia — 부동심 · 정념의 부재)` | `(ἀπάθεια, apatheia — 부동심 · 정념의 부재)` | 콤마 |
| `(ἀπάθεια apatheia)` | `(ἀπάθεια, apatheia)` | 콤마 |
| `(ἀπονία aponia · 신체의 무고통)` | `(ἀπονία, aponia — 신체 무고통)` | 콤마 + 의 제거 |
| `(ἀταραξία ataraxia · 정신의 평정)` | `(ἀταραξία, ataraxia — 정신의 평정)` | 콤마 |
| `(Ἐγχειρίδιον · Encheiridion · 편람)` · `(Κύριαι Δόξαι · Kyriai Doxai · Principal Doctrines)` · `(ἀκολασία akolasia)` · `(ἀναισθησία anaisthēsia)` · `(ἔλλειψις elleipsis)` · `(ὑπερβολή hyperbolē)` · `(ἠθικὴ ἀρετή ēthikē aretē)` · Greek-quote `ἐκ προαιρέσεως` | 제거 | paren 전체 삭제 |

### Step 2 — TitleCase (2-6단어) 영어 phrase

- **추출 결과**: 10 유니크 토큰 · **전수 PASS (0-hit = 0)**

| hit | 토큰 |
|-----|------|
| 5 | `Albert Bandura` |
| 1 | `Bobo doll experiment` |
| 1 | `Educating for Character` |
| 4 | `Karl Popper` |
| 3 | `Philip Pettit` |
| 3 | `Quentin Skinner` |
| 1 | `Social Foundations of Thought and Action` |
| 1 | `Social Learning Theory` |
| 1 | `Summa Theologiae` |
| 1 | `The Challenge to Care in Schools` |

### Step 2 제거/변환된 0-hit 토큰

| 초기 | 최종 | 조치 |
|------|------|------|
| `Educating Moral People` | `배려하는 도덕인 교육` | 한국어 역어 (coverage 확인) |
| `Learning Together and Alone` | `함께 배우기와 홀로 배우기` | 한국어 역어 |
| `Ethica Nicomachea` | `니코마코스 윤리학` | 한국어 역어 (이미 병기) |
| `Isaiah Berlin` | 삭제 | 부차 주석, 한국어 `소극적 자유` 로 대체 충분 |
| `Kyriai Doxai` | `주요 교설` 단독 | 한국어 역어 |
| `Principal Doctrines` | 삭제 | `주요 교설` 로 대체 |
| `Sovereign hath praetermitted` | 삭제 | 영어 장문 인용 제거 |
| `The Liberty of Subjects lieth therefore` | 삭제 | 영어 장문 인용 제거 |

## 한자(漢字) 래퍼 보존 결과

원본 시험지 verbatim 섹션 한자 전수 보존 확인 (grep 실측):

| 한자 | 출현 위치 | 보존 상태 |
|------|----------|----------|
| `大學` (대학) | Q4 주자 격물치지 제시문 · 해설 | ✅ 보존 |
| `格物致知` (격물치지) | Q4 제시문 · 해설 | ✅ 보존 |
| `理氣之妙` (이기지묘) | Q5 율곡 제시문 · 해설 | ✅ 보존 |
| `理通氣局` (이통기국) | Q5 해설 | ✅ 보존 |
| `牛山之木` (우산지목) | Q9 맹자 제시문 · 해설 | ✅ 보존 |
| `性惡` (성악) · `性善` (성선) | Q9 해설 | ✅ 보존 |
| `賞` · `罰` (상·벌) | Q14 한비자 이병 해설 | ✅ 보존 |
| `二柄` (이병) | Q14 해설 | ✅ 보존 |
| `人主無爲` (인주무위) | Q14 한비자 제시문 · 해설 | ✅ 보존 |
| `法治` (법치) | Q14 해설 | ✅ 보존 |
| `무위자연` 한문 4문장 | Q14 노자 제시문 verbatim | ✅ byte-level 보존 (人多伎巧·我無爲而民自化·以正治國 등) |
| `致知在格物者` | Q4 주자 『대학장구』 한문 인용 | ✅ 보존 |
| `凡禮義者` 등 『순자』 「성악편」 한문 인용 | Q9 해설 | ✅ 보존 |
| `陶人埏埴以爲器` 등 순자 예의 비유 한문 | Q9 해설 | ✅ 보존 |
| `誠` (성) | Q1 교육과정 해설 | ✅ 보존 |
| `讀書` (독서) · `內省` (내성) | Q4 해설 | ✅ 보존 |
| `理氣不相離不相雜` (이기불상리불상잡) | Q5 해설 주자 인용 | ✅ 보존 |
| `至福直觀` (지복직관) | Q6 아퀴나스 해설 | ✅ 보존 |
| `政體` (정체) | Q10 홉스 해설 | ✅ 보존 |
| `有爲` (유위) | Q14 노자 해설 | ✅ 보존 |

원본 `2019_중등1차_도덕윤리A.md` 원문 섹션(`제시문 verbatim` 블록)은 copy-paste byte-level 유지. 해설 블록의 한자는 Korean `한글(한자)` 병기 규약 준수.

## TASK-DQ-011 Override 적용

coverage/2019-A.md 는 BLOCKER-Q3 (bandura) · BLOCKER-Q10 (pettit) 를 ES 미등록으로 기록하나, 본 세션 curl 실측(`localhost:9200/ethics-thinkers/_doc/{id}`) 결과 `found=true` · bandura 8 claims · pettit 8 claims 확인.

- **Q3 bandura**: ES 등록 · coverage BLOCKER 해소
- **Q10 pettit**: ES 등록 · coverage BLOCKER 해소 (skinner 는 여전히 미등록으로 BLOCKER-2 남음)

본 2019-A.md Q3 · Q10 섹션에 HTML 주석 `<!-- TASK-DQ-011 override: ... -->` 기재하여 data-quality-log 연동 지시. 주석은 렌더링 시 출력되지 않으나 `grep -F "TASK-DQ-011"` 로 검증 가능.

```bash
$ grep -c "TASK-DQ-011" /home/jai/program-agent/projects/ethics-study/exam-solutions/study-guide/2019-A.md
8
```

(ES 상태 표 1회 + 공지 1회 + Q3 HTML comment 1회 + Q3 본문 `ES 등록 표기` 2회 + Q10 HTML comment 1회 + Q10 본문 `ES 등록 표기` 2회 = 8회)

## 이슈/블로커

- **없음**. 본 태스크 범위 내 신규 blocker·bug 발생하지 않음.
- **선행 blocker 유지**: `popper` (BLOCKER-1 · BLK-175E-2019A-001) · `skinner` (BLOCKER-2 · BLK-175E-2019A-002) — 본 태스크 범위 외. Q7 · Q10 섹션에 `⚠️ ES 미등록` 태그 + `found=false` 실측 + trademark 일치로 정답 판정은 확실 주석 기재.

## 다음 제안

1. **TASK-193 (2020-A 학생용 가이드)** — 동일 시리즈 다음 차례. 2019-A와 동일 포맷(Phase A + Phase B 분할, 14문항 가정, coverage 기반, ES 실측).
2. **신규 사상가 등록 태스크**: popper · skinner ES ethics-thinkers 인덱스 등록 → Q7 · Q10 BLOCKER-1/2 해소. 사상가 등록 시 `popper-claim-001~NNN` · `skinner-claim-001~NNN` claim 데이터셋 동반 생성.
3. **data-quality-log 동기화**: 본 2019-A TASK-DQ-011 override 적용 사항을 `signal/ethics-study/data-quality-log.md` 에 append 기록 (coverage 갱신 전 배치 정정 시점 일괄 처리).
4. **Reviewer 검증 요청**: 본 산출물 `2019-A.md` 를 reviewer-agent 에 전달하여 원문 verbatim 보존·채점기준 배점 일치·ES thinker_id 실측 일치·한자 래퍼·BLOCKER 태그 규범 준수 전수 검증. 이전 TASK-188/190 선례에서 reviewer PASS 확인된 동일 포맷이나 본 산출물의 신규 3인 복합 문항(Q10) 검증 필요.

## 완료 조건 검증

| # | 조건 | 결과 |
|---|------|------|
| 1 | `2019-A.md` 파일 생성 · 14 섹션 완비 | ✅ 1078 L · `^## 문항` 14개 |
| 2 | 제시문 verbatim byte-level 보존 | ✅ `<u>…</u>` · ㉠㉡ · ⓐⓑⓒⓓⓔ · 한자 · em-dash 보존 확인 |
| 3 | ES 등록 16/18 + BLOCKER 2명 정확 분류 | ✅ 16명 found=true + popper/skinner 2명 found=false |
| 4 | TASK-DQ-011 override Q3 bandura · Q10 pettit 주석 | ✅ HTML comment 2건 + 공지 1건 + 표 1건 = 4회 |
| 5 | Q1/Q2/Q13 교과교육학/통일교육 무사상가 분류 | ✅ 각 섹션 "해당 없음" 명시 |
| 6 | 서술형 Q9-Q14 채점 기준 + 4점 배분 | ✅ 6건 전수 `### 채점 기준 (총 4점)` 존재 |
| 7 | 다인 문항 (Q9/Q10/Q12/Q14) 갑·을 분리 + Q10 3인 복합 | ✅ Q9 xunzi+mencius · Q10 hobbes(갑) + pettit+skinner(을) 3인 · Q12 epictetus+epicurus · Q14 hanfeizi+laozi |
| 8 | 자기검증 3단계 (Step 1/1b/2) 실행 | ✅ 실측 실행 + 0-hit 토큰 전수 제거·변환 |
| 9 | 1800 L cap 준수 | ✅ 1078 L (여유 722 L) |
| 10 | 자기검증 결과표 + 한자 래퍼 보존 표 report 수록 | ✅ 본 보고서 상기 섹션 |
| 11 | coder-report 경로 `signal/ethics-study/coder-report-TASK-192.md` | ✅ 본 파일 |

전 조건 통과 — 태스크 완료.
