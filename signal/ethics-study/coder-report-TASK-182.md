---
task_id: TASK-182
status: DONE
agent: coder(opus)
date: 2026-04-22
target_file: projects/ethics-study/exam-solutions/study-guide/2014-A.md
---

# TASK-182 · 2014-A 학생용 study-guide 신규 작성 · Coder Report

## 1. 작업 요약

- 대상 파일: `/home/jai/program-agent/projects/ethics-study/exam-solutions/study-guide/2014-A.md` (신규 생성)
- 디렉토리: `projects/ethics-study/exam-solutions/study-guide/` (이전에 존재하지 않던 디렉토리 신규 생성)
- 라인 수: **655 lines** (상한 3000 이내, 분량 여유 충분)
- 문항 구성: 기입형 15문항 + 서술형 5문항 = 20문항 (각 섹션 헤더 `## 문항 N · (기입형/서술형) · N점 · 원문 line L{m}-L{n}`)
- 서술형 5문항 전원 `### 채점 기준` 서브섹션 실재 (655 라인 파일 내 L470·L504·L542·L582·L622 — 5건 확인)
- 각 문항에 `원문 line L{m}-L{n}` 메타데이터 기재 (20건 확인 · `grep -c "원문 line L"` = 20)

## 2. 입력 원천 실측 Read 감사 로그

| 파일 | offset | limit | 비고 |
|------|--------|-------|------|
| `projects/ethics-study/exam-solutions/coverage/2014-A.md` | 1 | 103 | 전체 (103 lines) |
| `/home/jai/잡동사니/임용/md/2014중등1차-2교시-도덕윤리-전공A-문제지-최종.md` | 1 | (전체 263 lines) | 원문 line range 인용·`<u>` 태그 byte-level 확인용 |
| `projects/ethics-study/exam-solutions/exam-coverage-map.md` | grep | — | BLK-175E-2014A 미배정 확인 (결과: 0건, 따라서 "BLK 미배정" 표기) |
| `signal/ethics-study/architecture.md` | 523 | 115 | Phase 6 기출 작업 규칙 (Coder 규칙 5항 포함) 재확인 |
| `signal/ethics-study/task-board.md` | 284 | 2 | TASK-182 전체 스펙 재확인 |

## 3. ES 실재 검증 (본 세션 curl 실측)

```
curl -s http://localhost:9200/ethics-claims/_search?size=15&q=thinker_id:{id}
```

| thinker_id | claim count | 대표 claim_id | 상태 | 본 시험 사용 문항 |
|------------|-------------|---------------|------|-------------------|
| `confucius` | 15 | confucius-claim-001 | ✅ 등록 | Q4 |
| `wonhyo` | 3 | wonhyo-claim-001 | ✅ 등록 | Q7 |
| `aquinas` | 10 | aquinas-claim-001 | ✅ 등록 | Q8 |
| `dewey` | 9 | dewey-claim-001 | ✅ 등록 | Q9 |
| `spinoza` | 6 | spinoza-claim-001 | ✅ 등록 | Q10 |
| `rousseau` | 13 | rousseau-claim-001 | ✅ 등록 | Q15 |
| `zhuxi` | 15 | zhuxi-claim-001 | ✅ 등록 | Q4·S2 |
| `wangyangming` | 10 | wangyangming-claim-001 | ✅ 등록 | S2 |
| `yihwang` | 12 | yihwang-claim-001 | ✅ 등록 | S4 |
| `aristotle` | 12 | aristotle-claim-001 | ✅ 등록 | S5 |
| `zhuangzi` | 10 | zhuangzi-claim-001 | ✅ 등록 | Q6 |
| `habermas` | 8 | habermas-claim-001~008 | ✅ 등록 (부분 관련) | Q11 (심의민주주의 간접) |
| `bandura` | 8 | bandura-claim-001 | ✅ 등록 | Q3 (★ coverage override) |
| `turiel` | 8 | turiel-claim-001 | ✅ 등록 | S1 (★ coverage override) |
| `raths` | 10 | raths-claim-001 | ✅ 등록 (부분 관련) | Q2 (가치명료화) |
| `lickona` | 10 | lickona-claim-001 | ✅ 등록 (대안 참고) | Q1 (CDP 대안) |
| `nagarjuna` | 0 | found=false | ⚠️ 미등록 | Q5 |
| `burke` | 0 | found=false | ⚠️ 미등록 | Q13 |
| `machiavelli` | 0 | found=false | ⚠️ 미등록 | Q14 |
| `cdp`/`child_development_project` | 0 | found=false | ⚠️ 미등록 | Q1 |

## 4. coverage 정정 규정 적용 (TASK-DQ-006 override)

- coverage/2014-A.md L37~L45 "ES 사상가 누락" 목록에 bandura(L40) · turiel(L44) 2건이 잘못 포함되어 있으나, 본 세션 curl 실측상 **둘 다 ES 실재**.
- 본 가이드에서는 coverage override 규정에 따라 **bandura(Q3)·turiel(S1)을 ✅ ES 등록으로 표기**.
- 실제 ⚠️ ES 미등록은 coverage L39(CDP)·L41(Nāgārjuna)·L42(Burke)·L43(Machiavelli) 4건에 한정.

## 5. BLK id 처리

- `projects/ethics-study/exam-solutions/exam-coverage-map.md` 에서 `BLK-175E-2014A` 접두어 검색 → 0건.
- 2014-A 문항에는 canonical BLK id가 배정되어 있지 않음.
- 따라서 ⚠️ ES 미등록 4건 (Q1·Q5·Q13·Q14) 에 대해 `[BLK 미배정]` 표기로 통일.

## 6. 자기검증 2단계 결과 표

### Step 1 · 괄호 안 영어 토큰 전수 역검색

명령: `grep -oE '\([A-Za-z][^)]*\)' 2014-A.md | sort -u` → 각 토큰 `grep -cF -- "$inner" coverage/2014-A.md`

| # | 토큰 | coverage hit | 판정 | 비고 |
|---|------|---------------|------|------|
| 1 | (A) | 13 | PASS | 지시자 |
| 2 | (B) | 15 | PASS | 지시자 |
| 3 | (BLK 미배정) | 0 | OK(framework) | 프레임워크 상태 라벨 |
| 4 | (CDP) | 2 | PASS | 사상가·개념 실재 |
| 5 | (Child Development Project) | 3 | PASS | 이론명 실재 |
| 6 | (L1~L103) | 0 | OK(meta) | 자기 파일 메타 라인 참조 |
| 7 | (L1~L263) | 1 | PASS | 원본 exam 라인 참조 |
| 8 | (L40) | 0 | OK(meta) | coverage 라인 참조 |
| 9 | (L44) | 0 | OK(meta) | coverage 라인 참조 |
| 10 | (L523~L638) | 0 | OK(meta) | architecture.md 라인 참조 |
| 11 | (Nāgārjuna, 龍樹) | 1 | PASS | 사상가명 실재 |
| 12 | (Q3) | 0 | OK(meta) | 문항 참조 약칭 |
| 13 | (TASK-DQ-006 기록) | 0 | OK(framework) | 태스크 ID 참조 |
| 14 | (a)·(b)·(c)·(d) | 49·10·41·28 | PASS | 열거 지시자 |
| 15 | (coverage L17 / L64) | 0 | OK(meta) | coverage 라인 참조 |
| 16 | (coverage L19) | 0 | OK(meta) | coverage 라인 참조 |
| 17 | (coverage L23) | 0 | OK(meta) | coverage 라인 참조 |
| 18 | (coverage L24) | 0 | OK(meta) | coverage 라인 참조 |
| 19 | (coverage L28) | 0 | OK(meta) | coverage 라인 참조 |
| 20 | (coverage L32) | 0 | OK(meta) | coverage 라인 참조 |
| 21 | (coverage 정정 규정) | 0 | OK(framework) | 프레임워크 라벨 |
| 22 | (coverage/2014-A.md L91~L97 근거) | 0 | OK(meta) | coverage 라인 참조 |
| 23 | (coverage/2014-A.md L99~L103 근거; 본 가이드 정정 규정 반영) | 0 | OK(meta) | coverage 라인 참조 |
| 24 | (moral disengagement) | 1 | PASS | 사상가 개념 실재 |
| 25 | (sub specie aeternitatis — 원문 라틴어 표현이나 한국어 번역은 '영원의 상') | 0 | FRAG-PASS | 핵심 어구 "sub specie aeternitatis" 단독 검색 시 coverage hit=2, 주석 한국어 부가 때문에 전체 문자열은 unique |
| 26 | (thinker 실재·claim 보강 필요) | 0 | OK(framework) | 프레임워크 상태 라벨 |

- **실질적 사상가·개념 관련 영어 토큰 (항목 4·5·11·24·25)은 전부 coverage hit ≥ 1** — 할루시네이션 없음.
- 0-hit 토큰은 전부 프레임워크 메타데이터 (라인 참조·태스크 ID·상태 라벨) 로, 사상가 이론에 대한 영어 주장을 담지 않음.

핵심 어구 `sub specie aeternitatis` 재검증:

```
$ grep -cF "sub specie aeternitatis" coverage/2014-A.md
2
```

→ PASS.

### Step 2 · 괄호 밖 TitleCase phrase (2-6 words) 전수 역검색

명령: `grep -oE '[A-Z][a-z]+(\s+[A-Za-z][a-z]+){1,5}' 2014-A.md | sort -u`

| # | 토큰 | coverage hit | 판정 |
|---|------|---------------|------|
| 1 | Albert Bandura | 3 | PASS |
| 2 | Child Development Project | 3 | PASS |
| 3 | Edmund Burke | 3 | PASS |

- 괄호 밖 TitleCase phrase는 3건이며 모두 coverage에 실재.
- 이는 "coverage override 로 bandura 는 ES 등록이지만 영어 병기는 coverage 존재" 규칙에 부합.

## 7. 원본 exam md 대비 `<u>` byte-level 보존 확인

TASK-178-FIX 선례 준수 — HTML `<u>` 태그가 포함된 7개 밑줄 구간 전수 원본 대비 `grep -cF` byte-level 일치 확인:

| # | `<u>` 구간 | 원본 exam hit |
|---|------------|---------------|
| 1 | `<u>오직 우리 해동의 보살만이...한 시대의 지극히 공정한 논의를 얻었다.</u>` | 1 |
| 2 | `<u>이로부터 생겨난 법 또한 영원하다....자연적 성향을 갖고 있다.</u>` | 1 |
| 3 | `<u>편견</u>` | 1 |
| 4 | `㉠ <u>3가지 정치체제</u>` | 1 |
| 5 | `㉠ <u>태극</u>` | 1 |
| 6 | `㉠ <u>욕구적인 것</u>` | 1 |
| 7 | `㉡ <u>일차적인 의미에서 이성을 자체 안에 가지고 있는 것</u>` | 1 |

전 7개 구간 원본 exam md 대비 **byte-level 일치** 확인. 임의 "정규화" 없음.

## 8. 핵심 verbatim 구간 coverage 대비 byte-level 일치 spot-check

`grep -cF` 결과 coverage hit ≥ 1 확인된 대표 구간:

| 구간 | coverage hit |
|------|---------------|
| 아동 발달 프로젝트(Child Development Project)를 통해 학생들이... | 1 |
| 나가르주나(Nāgārjuna, 龍樹)이다. | 1 |
| 공의 세계는 생겨[生]나지도 소멸[滅]하지도 않으며 | 1 |
| 오직 우리 해동의 보살만이 성(性)과 상(相)을 융화해 밝히고 | 1 |
| 지적 피조물인 인간이 공유하고 있는 영원한 법을 자연법이라 부르며 | 1 |
| 참된 자유를 얻기 위해서, 우리의 정신은 자신과 신체를 | 1 |
| 이는 공자가 남긴 글이니 처음 배우는 이가 덕(德)으로 들어가는 문이다. | 1 |
| 더 오래 지속된 편견일수록 | 1 |

참고: coverage 셀 자체에는 `<u>` 태그가 없으나 원본 exam md에는 있음. TASK-178-FIX 선례에 따라 `<u>` 태그는 원본 exam md 기준으로 **임의 정규화 금지(보존)** 적용 — 학생이 "밑줄 친" 발문 지시와 대응되는 구간을 식별하기 위해 교육적으로도 필요.

## 9. 완료 조건 체크

| # | 완료 조건 | 결과 |
|---|-----------|------|
| 1 | `study-guide/2014-A.md` 파일 생성 | ✅ 655 lines |
| 2 | 20문항 전부 섹션 실재 (기입형 15 + 서술형 5) | ✅ `grep ^## 문항` = 20 |
| 3 | 각 문항 섹션 헤더 `원문 line L{m}-L{n}` 실재 | ✅ `grep -c 원문 line L` = 20 |
| 4 | 각 문항 제시문 verbatim byte-level 일치 | ✅ spot-check 8/8 + `<u>` 7/7 |
| 5 | ES 근거 id 실존 확증 (`curl` 결과 기반) — 문항당 thinker≥1·claim≥1 (사상가형 기준) | ✅ 14명 thinker·120+ claims 실측 매핑 |
| 6 | 미등록 4건 `⚠️ES 미등록 [BLK 미배정]` 실재 | ✅ Q1·Q5·Q13·Q14 표기 |
| 7 | 서술형 5문항 전원 `### 채점 기준` 서브섹션 실재 | ✅ `grep -c ^### 채점 기준` = 5 |
| 8 | 자기검증 2단계 결과 표 coder report 수록 | ✅ 본 report §6 |

## 10. 주의·특이사항

1. **`<u>` 태그 정책 결정** — coverage 셀에는 `<u>` 없으나 원본 exam md에는 있음. TASK-178-FIX 선례 `HTML <u> byte-level 보존` 해석을 원본 exam 기준으로 적용. 학생용 가이드의 "밑줄 친" 발문 대응 효용과 byte-level 보존 원칙 모두 만족.
2. **habermas 부분 커버** — Q11(심의민주주의 vs 자유주의 민주주의 비교)은 habermas 담론이론의 심의민주주의 측면과 관련. habermas ES에 claim 8건 실재하나 "(A)와 (B) 대조" 직접 claim은 coverage 판정상 보강 필요. 본 가이드에서는 "ES 등록 (부분 관련)" 으로 표기하고 habermas 참조만 제시. claim_id 8개 중 특정 매칭이 본 시험 문항에 1:1 대응하지 않아 "habermas-claim-001 ~ habermas-claim-008 실재" 범위로 기재.
3. **Q1 CDP 처리** — CDP 팀(솔로몬·왓슨·바티스티치)은 ES 미등록. 인격교육 분파로 lickona 와 인접하나 동일인 아님. 본 가이드에서는 ⚠️ ES 미등록 + 대안 참고로 lickona 명시.
4. **Q2 모형 A/B 처리** — 모형 B(래스, 가치명료화) 는 raths ES 등록. 모형 A(쿰즈·뮤 가치분석모형) 은 coverage-map 상 `coombs_meux` id 할당되어 있으나 ES 실재 `found=false` (보강 필요 영역). 본 가이드에서는 Q2 ES 근거에 raths만 인용하고 coombs_meux는 "보강 필요"로 명시.
5. **사용자 한자 가독성 규정 준수** — 『대학』·성의장·신독·무용지용·화쟁·회통·홍익인간·재세이화·태극·무극이태극·에토스·품성적 덕·지적 덕 등 한자 개념어·핵심 trademark에 한글 병기 또는 괄호 설명 부착.
6. **분량** — 655 lines / 상한 3000 lines. 평균 ~33 lines/문항. 각 문항 6개 서브섹션(발문/제시문/정답/ES 근거/채점 기준[서술형]/풀이 과정) 전개.

## 11. 후속 작업 제안 (Manager 참고)

- **TASK-182-T** (Tester 검증) 등록 권장 — spec에 명시된 바와 같이 문항 수·verbatim·ES link·영어 0-hit·⚠️ES 미등록 정합성·채점 기준 실재·원문 line metadata 전수 체크.
- **TASK-183 이후** (연도별 study-guide 시리즈) — 본 파일의 섹션 포맷·자기검증 표 포맷을 템플릿으로 재사용.
- **claim 보강 후보 리스트** (coverage 판정상 "보강 필요" 영역):
  - zhuxi "신독·대학 성의장" 직접 claim
  - zhuangzi "무용지용" 직접 claim
  - spinoza "영원의 상 sub specie aeternitatis" 직접 claim
  - habermas "심의민주주의 vs 자유주의 민주주의 비교" 직접 claim
  - rousseau "인간 불평등 기원론 3단계" 직접 claim
  - yihwang "리발설" 직접 claim
- **ES 신규 등록 후보 리스트**:
  - CDP(Solomon·Watson·Battistich 또는 cdp 통합 id)
  - nagarjuna (용수)
  - burke (에드먼드 버크)
  - machiavelli (니콜로 마키아벨리)
  - coombs_meux (쿰즈·뮤 가치분석모형) — exam-coverage-map 에는 id 할당되어 있으나 실제 ES 실재 아님
