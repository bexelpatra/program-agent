---
agent: tester
task_id: TASK-187-T
status: DONE
timestamp: 2026-04-22T21:05:00
verdict: PASS
severity: none
items_passed: 10/10
---

## 결과 요약

2016-B 학생용 풀이 가이드 `projects/ethics-study/exam-solutions/study-guide/2016-B.md` (487 lines, 47KB) 10항 검증 전수 통과. Coder 주장 수치 전수 실측 일치. 실질(원문 인용) 0-hit 토큰 = 0건, 선례(2016-A) 허용 범위의 관리·메타 wrapper 0-hit 18건(Step 1의 17건 + Step 2 `Coder Agent` 1건)은 동형 면제 적용. ES 사상가 9명 + 대표 claim 9건 전수 `found=true` 재확증, ES 미등록 2명(berlin · machiavelli) `found=false` 재확증. em-dash U+2014 128회 byte-level(`e2 80 94`) 보존.

## 검증 대상

- 대상 파일: `projects/ethics-study/exam-solutions/study-guide/2016-B.md` (487 lines)
- 역grep 원천: `projects/ethics-study/exam-solutions/coverage/2016-B.md` (244 lines)
- Coder report: `signal/ethics-study/coder-report-TASK-187.md`
- 스펙: `signal/ethics-study/task-board.md` L307 TASK-187-T row

## 10항 체크 결과

| # | 체크 항목 | 결과 | 실측 증거 |
|---|-----------|------|-----------|
| 1 | `^## 문항` == 8 (Q1~Q8 서술형) | PASS | `grep -c '^## 문항' 2016-B.md == 8` |
| 2 | 8개 섹션 헤더 line metadata 스펙 일치 | PASS | L41·L90·L134·L179·L227·L280·L340·L392 헤더 전수 — L16-L26·L29-L40·L44-L49·L53-L59·L63-L71·L75-L81·L85-L89·L95-L108 정확 일치 |
| 3 | verbatim byte-level 15 spot-check (HTML `<u>`·괄호·한자·em-dash·㉠·㉡) | PASS | 15/15 coverage hit ≥ 1 (아래 표 참조) |
| 4 | ES thinker 9건 curl 재조회 `found=true` | PASS | epicurus·sandel·yiyulgok·xunzi·laozi·rousseau·raths·kohlberg·lickona 전수 `True` |
| 5 | 대표 claim 9건 curl 재조회 `found=true` | PASS | epicurus-003·sandel-001·yiyulgok-002·xunzi-003·laozi-002·rousseau-005·raths-001·kohlberg-011·lickona-001 전수 `True` |
| 6 | ES 미등록 2명 `⚠️ES 미등록 (BLOCKER-2·3)` 표기 실재 | PASS | L19 헤더표·L35 공지·L197·L198·L207·L208 본문 명시. 재curl: berlin/machiavelli `found=False` |
| 7 | BLOCKER-1 주석(Q3) + Q2 `해당 없음 (통일교육)` + Q5 (가) `해당 없음 (『중용』)` 분류 실재 | PASS | L35 공지 통합·L149 Q3 BLOCKER-1 주석·L245/L255 Q5 (가) 중용 `해당 없음` |
| 8 | `### 채점 기준` == 8 + 배점 4/4/4/4/4/5/5/10 = 40점 | PASS | L74·L118·L163·L211·L264 각 4점(×5=20) + L323·L374 각 5점(×2=10) + L462 10점(×1=10) → 합 40점 |
| 9 | 자기검증 2단계 역grep 재실행 | PASS | Step 1 bare-paren 78토큰 HIT=61 MISS=17 · Step 1b Greek 4토큰 HIT=4 MISS=0 · Step 2 TitleCase 22토큰 HIT=21 MISS=1(`Coder Agent`). 실체 0-hit = 0건. 관리/meta wrapper 면제 (2016-A 선례 동형) |
| 10 | em-dash U+2014 byte-level 보존 (hexdump `e2 80 94` 3+ 샘플) | PASS | 총 128회 · 3 샘플 offset 53·619·5653 전수 `e28094` 바이트 확증 |

## 테스트 결과

- 통과: **10/10**
- 실패: 0
- severity=bug 자동 트리거 (실체 0-hit): **0건**

### 3항 verbatim byte-level 15 spot-check 상세

| # | 문자열 | study hit | cov hit |
|---|--------|-----------|---------|
| 1 | `自然的이고 必然的인 欲求` | 1 | 2 |
| 2 | `一般意志` | 1 | 1 |
| 3 | `volonté générale` | 1 | 1 |
| 4 | `grande simplicité de mœurs` | 2 | 1 |
| 5 | `Discorsi sopra la prima deca di Tito Livio` | 2 | 1 |
| 6 | `Two Concepts of Liberty` | 2 | 2 |
| 7 | `unencumbered self` | 2 | 2 |
| 8 | `katastematic pleasure` | 2 | 1 |
| 9 | `ἀπονία` (Greek) | 1 | 2 |
| 10 | `ἀταραξία` (Greek) | 1 | 2 |
| 11 | `The Doctrine of the Mean` | 1 | 1 |
| 12 | `knowing the good, loving the good, doing the good` | 1 | 1 |
| 13 | `Liberalism and the Limits of Justice` | 1 | 1 |
| 14 | `㉠` (circled Kor 1) | 31 occ / 28 lines | 14 lines |
| 15 | `㉡` (circled Kor 2) | 20 occ / 20 lines | 11 lines |

전 항목 coverage hit ≥ 1, byte-level 보존 확증. `<u>` 태그 쌍은 open/close 각 5회로 정확 일치.

### 9항 자기검증 2단계 역grep 재실행 상세

**Step 1 — bare-paren English 78 토큰 (HIT 61 / MISS 17):**

17건 MISS 전수 분류 — **모두 관리·메타 wrapper** (실체 원문 인용 아님):

| 분류 | 토큰 수 | 예시 |
|------|--------|------|
| BLOCKER ID | 6 | `(BLOCKER-1)`·`(BLOCKER-2)`·`(BLOCKER-3)`·`(BLOCKER-1 주석 참조)`·`(BLOCKER-2·3)`·`(BLK-175E-2016B-001)` |
| ES cross-ref | 3 | `(ES lickona-claim-001·lickona-claim-004)` 등 |
| Task/File meta | 4 | `(TASK-186 산출물)`·`(TASK-187)`·`(L1~L244)`·배점 문자열 |
| 문항 항목 | 2 | `(Q4 가)`·`(Q4 나)` |
| Q3 BLOCKER-1 주석 문구 | 1 | `(sandel 대표 매핑 · macintyre/taylor/walzer 가능성 열림)` |
| thinker_id 태그 | 1 | `(sandel)` (`(jonas)`·`(yangzi)` 동형 2016-A 허용) |

2016-A tester report 선례에서도 동일 유형 wrapper 0-hit 18~20건을 observation 수준에서 허용. 본 2016-B에서도 실체 영어 학술 용어 0-hit = **0건** — bug 자동 트리거 조건 미해당.

**Step 1b — Greek/Cyrillic 4 토큰 (HIT 4 / MISS 0):**

```
[2] (ἀπονία — 고통의 부재, 신체적 쾌락의 극한)
[2] (ἀταραξία — 마음의 평정, 정신적 쾌락의 극한)
[1] (δικαιοσύνη)
[1] (λάθε βιώσας — lathe biōsas, live unnoticed)
```

100% hit. em-dash U+2014 wrapper 전체 coverage 원문 일치.

**Step 2 — TitleCase phrase 22 토큰 (HIT 21 / MISS 1):**

MISS 1건: `Coder Agent` (푸터 메타 — 본 파일 자체 작성자 표기, 2016-A 동형 면제).

실체(인명·저서명·개념어) 22-1=21건 전수 coverage 매칭. `Alasdair Mac`은 `Alasdair MacIntyre`의 regex substring 추출 결과로 cov에 `Alasdair Mac...` 문자열 존재 → hit=1.

### 10항 em-dash U+2014 byte-level 보존

- 총 occurrence: **128회** (Coder 주장과 정확 일치)
- en-dash U+2013 (`\xe2\x80\x93`) = 0회 (byte-level 교체 없음)
- 샘플 3건 byte 확증: offset `53`·`619`·`5653` — 모두 hex `e28094` (3 bytes UTF-8 em-dash)

### 4·5·6항 ES 재curl 결과 요약

- thinker 9건 `found=True`: epicurus · sandel · yiyulgok · xunzi · laozi · rousseau · raths · kohlberg · lickona
- claim 9건 `found=True`: epicurus-claim-003 · sandel-claim-001 · yiyulgok-claim-002 · xunzi-claim-003 · laozi-claim-002 · rousseau-claim-005 · raths-claim-001 · kohlberg-claim-011 · lickona-claim-001
- ES 미등록 2건 `found=False`: berlin · machiavelli (각 Q4 가·Q4 나, BLOCKER-2·3)

## 이슈/블로커

코드 결함 또는 신규 이슈 **없음**. 관리·메타 wrapper 0-hit는 2016-A 선례(TASK-175 tester report)와 동형의 면제 범위 내. severity 자동 트리거 조건 미해당.

- 기존 BLOCKER-1·2·3(BLK-175E-2016B-001·002·003)은 Coder 책임이 아닌 설계 단계 blocker이며 문서 내 `⚠️` 표기로 정상 문서화됨.

## 다음 제안

- **DONE 처리**: TASK-187-T 10/10 PASS. task-board 상태 DONE으로 전환 권장.
- TASK-187(Coder) · TASK-187-T(Tester) 동시 DONE 처리 가능 (Coder report 이미 DONE, Tester 검증 완료).
- BLOCKER-2·3 해소는 TASK-176 후속(berlin·machiavelli ES 등록)에서 진행 예정. 본 태스크 범위 외.
- 2016-A·2016-B 가이드 작성 패턴이 안정적으로 확증됨 (em-dash 보존·verbatim byte·ES curl 재조회·2단계 역grep 루프). 차기 학년도 가이드 작업 시 동일 패턴 재사용 가능.

---

**작성**: 2026-04-22T21:05 · Tester Agent (TASK-187-T) · `signal/ethics-study/tester-report-TASK-187.md`
