---
task_id: TASK-175E-2021-B
agent: Coder
status: DONE
date: 2026-04-21
severity: observation
---

# TASK-175E-2021-B Coder Report

## 작업 요약

2021학년도 중등임용 도덕·윤리 전공 B(11문항 40점) 커버리지 맵을 Phase 6 Coder 규칙 1~6 엄격 준수하에 작성 완료.

- **산출물**: `projects/ethics-study/exam-solutions/coverage/2021-B.md` (신규 생성)
- **블로커 로그 append**: `signal/ethics-study/blocker-log.md` BLK-175E-2021B-001~007 (7건)
- **배점 검증**: 기입형 2점×2 + 서술형 4점×9 = 4 + 36 = **40점 PASS** (원문 L7 "11문항 40점" 일치)

## 문항별 사상가/정답 요약

| Q | 유형 | 사상가 | thinker_id | ES 상태 | 정답 핵심 | 원문 line |
|---|------|--------|-----------|--------|----------|-----------|
| Q1 | 기입형 | 갑=의천, 을=지눌 | `uicheon`+`jinul` | **둘 다 미등록** (BLK-001, BLK-002) | 갑=교관겸수(敎觀兼修) / 을=정혜쌍수(定慧雙修) | L14-L20 |
| Q2 | 기입형 | 로크 | `locke` | 등록 | ㉠=재산(property) / ㉢=입법권(legislative power) | L24-L29 |
| Q3 | 서술형 | 갑=튜리엘, 을=하이트 | `turiel`(미등록)+`haidt`(등록) | 갑 **미등록, 2018-B 재발** (BLK-003) | ㉠=관습 / ㉣=직관 + 도덕 영역 2원리(복지·공정성) + ㉢ 부당 이유 | L33-L44 |
| Q4 | 서술형 | 갑=뒤르켐, 을=피아제 | `durkheim`(미등록)+`piaget`(등록) | 갑 **미등록** (BLK-004) | ㉠=자율성 + 도덕 상대주의 단계 + 주관적 책임/평등·공정 정의 | L48-L58 |
| Q5 | 서술형 | 갑=레스트, 을=호프만 | `rest`(등록)+`hoffman`(미등록) | 을 **미등록, 2019-B 재발** (BLK-005) | ㉠=정서/공감적 각성 / ㉡=역할채택 + ㉢=타인의 삶의 조건에 대한 공감 | L62-L72 |
| Q6 | 서술형 | 갑=노자, 을=장자 | `laozi`+`zhuangzi` | 둘 다 등록 | ㉠=현동(玄同) / ㉢=양행(兩行) + 삼보(자·검·불감위천하선 중 2) | L76-L86 |
| Q7 | 서술형 | 갑=율곡, 을=퇴계 | `yiyulgok`+`yihwang` | 둘 다 등록 | ㉠=도심 / ㉡=인심 + 퇴계 이상적 관계(도심위주 인심청명) | L90-L100 |
| Q8 | 서술형 | 갑=사르트르, 을=키르케고르 | `sartre`(등록)+`kierkegaard`(미등록) | 을 **미등록** (BLK-006) | ㉡=휴머니즘 / ㉢=절망 + 주체성 차이(신 유무 + 자기 자신 의미) | L104-L114 |
| Q9 | 서술형 | 갑=아리스토텔레스, 을=밀 | `aristotle`+`mill_js` | 둘 다 등록 | ㉠=목적(telos) / ㉡=편의(expediency) + 덕-행복 관계(구성 vs 내면화) | L118-L128 |
| Q10 | 서술형 | 키케로 | `cicero` | **미등록** (BLK-007) | ㉠=법(ius) / ㉡=이익(utilitas) + ㉢ 혼합정체 | L132-L141 |
| Q11 | 서술형 | 하버마스 | `habermas` | 등록 | ㉠=예/아니오 / ㉢=심의 민주주의 + 3타당성(진리성·정당성·진실성) 중 2 | L145-L153 |

## 블로커 요약 (ES-gap 7건)

| BLK ID | 인물 | 우선순위 | 재출제 여부 |
|--------|------|---------|------------|
| BLK-175E-2021B-001 | 대각국사 의천 (uicheon) | 우선 | 신규 |
| BLK-175E-2021B-002 | 보조국사 지눌 (jinul) | 최우선 | 2020-A 선례 |
| BLK-175E-2021B-003 | 엘리엇 튜리엘 (turiel) | **최우선** | **2018-B 재발** |
| BLK-175E-2021B-004 | 에밀 뒤르켐 (durkheim) | 최우선 | 신규 |
| BLK-175E-2021B-005 | 마틴 호프만 (hoffman) | **최우선** | **2019-B 재발** |
| BLK-175E-2021B-006 | 쇠렌 키르케고르 (kierkegaard) | 최우선 | 신규 |
| BLK-175E-2021B-007 | 마르쿠스 툴리우스 키케로 (cicero) | 최우선 | 신규 |

**2연도 이상 재출제 인물**: turiel(2018-B→2021-B), hoffman(2019-B→2021-B), jinul(2020-A 가능성). TASK-176 등록 시 이 3명이 최최우선.

## 감사 (현 세션 Read/Grep/ES curl 호출 목록)

### Read 호출
1. `signal/ethics-study/architecture.md` offset=485 limit=120 → Phase 6 규칙·thinker_id suffix 규약 확인
2. `/home/jai/잡동사니/임용/md/2021_중등1차_도덕윤리_전공B.md` 전체 (157 lines, offset 0) → 본 태스크 원문 전수 확인
3. `/home/jai/잡동사니/임용/md/2021_중등1차_도덕윤리_전공B.md` offset=90 limit=15 → Q7 ㉠·㉡ 용어 순서 재독
4. `projects/ethics-study/exam-solutions/coverage/2021-A.md` head 20000 bytes + tail 15000 bytes → 선례 포맷·블로커 섹션·감사 구조 확인
5. `projects/ethics-study/exam-solutions/coverage/2020-B.md` head 5000 bytes → 11문항 40점 동일 배점 구조 선례 확인
6. `signal/ethics-study/blocker-log.md` offset=560 limit=60 + offset=610 limit=10 → BLK-175E-202*B-* 블로커 형식 + 마지막 라인 확인
7. `signal/ethics-study/blocker-log.md` wc -l = 616 lines (본 태스크 append 전)

### Grep 호출
- 본 태스크 범위에서 별도 grep 호출 없이 Read 출력으로 원문 전수 확인 가능(157 라인, Read 1회로 완전 확인). Tester 검증 시 권장 키워드는 coverage/2021-B.md 감사 섹션에 명시.

### ES curl 호출
- **1차** (22 id 개별 조회): uicheon·jinul·kihwa·wonhyo·locke·turiel·haidt·durkheim·piaget·rest·hoffman·laozi·zhuangzi·yi_i·yi_hwang·sartre·kierkegaard·aristotle·mill_js·bentham·cicero·habermas
- **2차** (alternate id 22회): yiyi·yulgok·toegye·yihwang·euicheon·uicheonh·chinul·jinul_seon·kihwa_hamheo·hamheo·turiel_e·turiel_elliot·haidt_j·durkheim_e·emile_durkheim·hoffman_m·hoffman_martin·kierkegaard_s·kierkegaard_soren·cicero_m·mill_j_s·lao_tzu·chuang_tzu → 대부분 MISSING, yihwang만 canonical 확인
- **3차** (전체 사상가 목록): `curl -s "http://localhost:9200/ethics-thinkers/_search?size=100&_source=id,name_en" | jq ...` → 55명 전체 목록. Q1~Q11 출제 인물 중 uicheon·jinul·turiel·durkheim·hoffman·kierkegaard·cicero 7명 미등록 확정. yiyulgok(율곡)·yihwang(퇴계) canonical 확정.

### 원문 인용 구절 존재성
본 coverage/2021-B.md 각 row의 "제시문 핵심(원문 복사)" 컬럼은 모두 2021_중등1차_도덕윤리_전공B.md 해당 라인에서 직접 복사된 원문이며, 재서술·요약·창작 없음. line 범위(L14-L20, L24-L29, L33-L44, L48-L58, L62-L72, L76-L86, L90-L100, L104-L114, L118-L128, L132-L141, L145-L153)는 Read 호출 확인 범위와 일치.

### 한자 병기 건수
약 **310+ 건** (row 평균 25~35건). Phase 6 Coder 규칙 4 엄격 준수. 한자 단독 노출 0건(원문 인용구절 내부 한자 표기는 원문 보존 원칙에 따라 유지).

### 배점 검산
- 기입형: Q1 2 + Q2 2 = **4점**
- 서술형: Q3~Q11 각 4점 × 9 = **36점**
- 총합: 4 + 36 = **40점** ✓ (원문 L7 "11문항 40점" 일치)

## 완료 조건 충족 여부

- [x] `projects/ethics-study/exam-solutions/coverage/2021-B.md` 생성 완료
  - [x] 헤더(연도·과목·총배점·문항수·출처 파일:라인·배점 검증 40점) 기재
  - [x] Q1~Q11 각 row에 발문 요약·trademark 원문 2~3구절 복사·canonical thinker_id·한자 병기·유형·해설 포함
  - [x] 블로커 요약 섹션(7건) 포함
  - [x] Read/Grep/ES curl 감사 목록 포함
- [x] `signal/ethics-study/blocker-log.md`에 BLK-175E-2021B-001~007 append 완료
- [x] 본 report(`signal/ethics-study/coder-report-TASK-175E-2021-B.md`) 작성 완료

## 요약 수치

- **블로커 개수**: 7건 (BLK-175E-2021B-001~007)
- **파일 라인 수**: coverage/2021-B.md 생성 후 (헤더+11 rows+블로커 섹션+ES 요약+감사)
- **한자 병기 건수**: ~310+ 건 (row당 평균 25~35건)
- **ES 등록 사상가**: 12 (locke·haidt·piaget·rest·laozi·zhuangzi·yiyulgok·yihwang·sartre·aristotle·mill_js·habermas)
- **ES 미등록 사상가**: 7 (uicheon·jinul·turiel·durkheim·hoffman·kierkegaard·cicero)
- **재출제 인물**: 2 (turiel 2018-B 재발 + hoffman 2019-B 재발) + 1 가능성 (jinul 2020-A)

## 후속 Manager 지시 사항 제안

1. **TASK-176 ES 등록** 우선순위: turiel·hoffman(재출제) → durkheim·cicero·kierkegaard(고빈도 단골) → uicheon·jinul(한국 불교 완성).
2. 다음 커버리지 태스크: 2022-A 또는 2022-B (Phase 6 Coder 규칙 6: 1연도×1과목 배치).
3. Tester 검증 시 감사 섹션의 권장 grep 키워드를 활용하여 3중 일치 기계 검증 수행 권장.
