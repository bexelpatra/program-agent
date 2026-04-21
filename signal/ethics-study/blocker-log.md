# Blocker Log

본 파일은 ethics-study 프로젝트에서 누적된 블로커(Tester severity: blocker) 내역을 기록한다. 1차 Opus 재작업 후에도 해소되지 않은 블로커는 여기에 누적되고, 사용자가 일괄 검토·판정한다. 정책: `architecture.md` "블로커 누적 처리 정책" 참조.

## 활성 블로커

### BLK-001 (TASK-174) — exam-coverage-map.md 대량 결함
- 일시: 2026-04-18
- 산출물: `projects/ethics-study/exam-solutions/exam-coverage-map.md`
- 판정 리포트: `signal/ethics-study/tester-report-TASK-174.md`
- 상태: **1차 재시도(TASK-175A Coder/Opus) 완료 → 2차 Tester(TASK-175B) 재판정 블로커. 블로커 누적 정책 발동 → 사용자 일괄 검토 대기**. 자식 블로커 BLK-175B-001 ~ BLK-175B-008 누적.
- 기계 치환 완료: thinker_id 6건 (`yi_hwang→yihwang`, `yi_i→yiyulgok`, `zhu_xi→zhuxi`, `wang_yangming→wangyangming`, `jeong_yakyong→jeongyagyong`, `taylor_c→taylor`) — 2026-04-19
- 백업 파일 참고: `exam-coverage-map.v1-rejected.md`는 **기계 치환 6건이 반영된 이후** 스냅샷(pre-substitution 순수 원본 아님). 치환은 canonical 규칙에 따른 기계적 교정이라 내용 손실 없으므로 audit 목적상 동등. pre-substitution 원본이 필요하면 `git log -p` 또는 TASK-174 시점 커밋으로 복원 가능.
- 미해소 결함:
  - [BLOCKER-1] 총 문항 수 3중 불일치 (227/295/273, 실제 293). Coder 재작성 시 **293**으로 일원화.
  - [BLOCKER-2] 사상가-문항 매핑 대량 오매핑. 샘플(확정):
    - 2014-A1 = 리코나 CDP + 교과교육학 (coverage 주장: 원효·일심·화쟁) ❌
    - 2014-A2 = 가치명료화·가치갈등분석 수업모형 (coverage: 홉스) ❌
    - 2014-A13 = 에드먼드 버크 『프랑스혁명에 대한 성찰』 세대 파트너십 (coverage: 싱어·종차별주의) ❌
    - 2014-B4 = 벤담/칸트/흄 보편성 비교 (coverage: 원효/지눌 돈오점수) ❌ **사용자 확정 2026-04-19**
    - 2015-A6 = 나가르주나 『中論』 팔불중도·공 (coverage: 레오폴드·대지윤리) ❌
    - 2015-A 대부분 번호 체계 재번호로 인한 연쇄 오류
    - 2017-A5~A8 오매핑 다수
    - 2020-A3 = 지눌 자성정혜·수상정혜 (coverage: 롤스 정의 두 원칙) ❌
    - 2020-A4 = 헌법 4조·통일교육지원법 (coverage: 에피쿠로스/스토아) ❌
  - [BLOCKER-3] 번호 체계 오류. 2014-A 실제는 "기입형 1~15 + 서답형 1~5", 2015-A 실제는 "기입형 1~10 + 서술형 1~4". coverage-map은 일원 번호(A1~A20, A1~A14)로 재번호 — **사용자 확정 2026-04-19**. 재작성 시 원문 번호 체계 그대로 보존.
  - [BLOCKER-4] 메모 컬럼의 원문 인용 할루시네이션 최소 5건 (2014-A1/A2/A13/B4, 2015-A6). 재작성 시 원문 2~3구절을 직접 복사·인용.
- 영향 전제:
  - "지눌 최우선 보강"(coder-report L60, coverage-map Section A)은 2014-B4 허구 전제에서 도출 — **무효**. TASK-175A 완료 후 실제 출제 빈도 재집계.
  - 환경윤리 5인(싱어/레건/폴 테일러/레오폴드/요나스) 등 "누락 사상가" 목록의 출제 빈도 숫자도 재집계 필요.
- 후속 조치:
  - TASK-175A 등록: Coder(Opus) 전면 재작성
  - TASK-175B 등록: Tester row-by-row 재검증
  - TASK-175B 결과가 다시 blocker면 본 파일에 결과 누적 후 사용자 검토 대기, 독립 태스크는 계속 진행 (정책: architecture.md "블로커 누적 처리 정책")

### BLK-175B-001 — 2014-A 기입형/서술형 라벨 및 매핑 대량 오류
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L111~130 (2014-A 섹션)
- 심각도: blocker
- 사유: 원본 2014-A는 "기입형 1~15 + **서술형** 1~5"이나 coverage-map은 `서답형1~5`로 잘못 라벨링. 또한 15개 기입형 중 **12개가 원문과 다른 사상가에 매핑**됨. 교정된 건 기입형1(lickona), 기입형2(raths/coombs), 기입형13(burke)뿐.
- 원문 근거: `2014중등1차-2교시-도덕윤리-전공A-문제지-최종.md` L16 "## 기입형 【1 ~ 15】", L205 "## 서술형 【1 ~ 5】"
- 샘플 오매핑 (원문 vs coverage-map):
  - 기입형3: 원문=bandura 사회인지·도덕이탈 기제 / coverage=plato 이데아 ❌
  - 기입형4: 원문=성의(誠意)·대학 (zhuxi) / coverage=aristotle 실천적지혜 ❌
  - 기입형5: 원문=nagarjuna 中論 不生不滅·공 / coverage=epicurus 쾌락주의 ❌
  - 기입형6: 원문=zhuangzi 가죽나무·소요·무용지용 / coverage=aquinas 자연법 ❌
  - 기입형7: 원문=wonhyo 해동보살·성상융화·화쟁 / coverage=kant 정언명령 ❌
  - 기입형8: 원문=aquinas 신의 섭리·영원법·자연법 / coverage=mill_js 공리 ❌
  - 기입형9: 원문=dewey 사유·도구주의·liking/prizing / coverage=confucius/mencius ❌
  - 기입형10: 원문=spinoza 명석판명·신·정서 / coverage=laozi/zhuangzi 무위자연 ❌
  - 기입형11: 원문=habermas 심의민주주의 / coverage=yihwang/yiyulgok 사단칠정 ❌
  - 기입형12: 원문=[통일정책] A~D 순서(김대중/노무현/이명박/박근혜 대북정책) / coverage=jeongyagyong 성기호 ❌
  - 기입형14: 원문=machiavelli 군주·3가지 정치체제·저변 넓은 체제 / coverage=singer/regan 동물해방 ❌
  - 기입형15: 원문=rousseau 불평등 기원론 / coverage=buddha 사성제 ❌
  - 서술형1(=coverage 서답형1): 원문=turiel 영역이론(도덕/인습/개인 영역) / coverage=wonhyo 일심·화쟁 ❌
  - 서술형2(=coverage 서답형2): 원문=zhuxi/wangyangming 선지후행 vs 지행합일 / coverage=huineng/shenxiu 돈오·남북종 ❌
  - 서술형3(=coverage 서답형3): 원문=[한국고유사상] 환인·환웅·단군·풍류 / coverage=zhuxi/wangyangming 성즉리 ❌
  - 서술형4(=coverage 서답형4): 원문=yihwang 무극이태극·성학십도 / coverage=socrates 무지의 자각 ❌
  - 서술형5(=coverage 서답형5): 원문=aristotle 영혼·욕구적·이성적 탁월성 / coverage=augustine 신국 ❌
- Coder가 기재한 내용: "서답형" 라벨, 위 ❌ 사상가들. Coder report는 "2014-A 기입형1, 2, 13 교정" 이외는 검증 없이 v1-rejected 내용을 거의 그대로 재사용한 것으로 추정됨.
- 사용자 판정 대기

### BLK-175B-002 — 2014-B 번호 체계 및 매핑 오류
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L134~139 (2014-B)
- 심각도: blocker
- 사유: 원본 2014-B는 "서술형 1~2 + 논술형 1~2" (총 4문항)이나 coverage-map은 `논술형1~4`로 일원 재번호. 매핑도 전면 오류.
- 원문 근거: `2014중등1차-3교시-도덕윤리-전공B-문제지-최종.md` L16 "## 서술형 【1 ~ 2】", L46 "## 논술형 【1 ~ 2】"
- 샘플 오매핑:
  - 원문 서술형1: 국제관계 4관점(현실주의/자유주의/세계체제/구성주의) [경계영역:국제정치] → coverage는 `2014-B-논술형1 hegel 인륜성` ❌
  - 원문 서술형2: 통일비용·통일편익 S1/S2 [경계영역:통일] → coverage는 `2014-B-논술형2 nietzsche 초인` ❌
  - 원문 논술형1: 학교 도덕 교과 필요성 [교과교육학] → coverage는 `2014-B-논술형3 sartre 실존` ❌
  - 원문 논술형2: bentham/kant/hume 보편성 비교 → coverage는 `2014-B-논술형4 bentham/kant/hume` (**사상가는 맞지만 번호가 논술형2가 맞다**)
- 사용자 판정 대기

### BLK-175B-003 — 2014-B 1·2·3 사상가 배치 오류
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L136~138
- 심각도: blocker
- 사유: coverage는 2014-B-논술형1=hegel, 2=nietzsche, 3=sartre라고 주장하지만, 원문 2014-B에는 hegel/nietzsche/sartre 관련 문항이 단 하나도 없음. 이는 BLOCKER-4(할루시네이션)의 재발로, Coder가 원문을 직접 읽지 않고 일반 윤리학 상식으로 채운 흔적.
- 원문 근거: 2014-B 원문 4문항 전체 인용(위 BLK-175B-002 참조) — hegel/nietzsche/sartre 키워드 0건
- 사용자 판정 대기

### BLK-175B-004 — 2015-A 기입형 대량 오매핑
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L149~158
- 심각도: blocker
- 사유: 2015-A 기입형 10개 중 7개가 원문과 다른 사상가에 매핑됨. 교정은 기입형6(nagarjuna)만 정확.
- 원문 근거: `2015중등1차-도덕윤리_전공A.md`
- 샘플 오매핑:
  - 기입형1: 원문=macintyre 계몽주의기획 비판·내러티브 / coverage=[교육과정] 2015 개정 ❌
  - 기입형2: 원문=[교과교육학] 공공정책 참여 수업모형(Newmann 환경적 능력) / coverage=confucius 인·정명 ❌
  - 기입형3: 원문=[교과교육학] 친구관계 가치·배려 / coverage=mencius 성선 ❌
  - 기입형4: 원문=xunzi 天行有常·제천 / coverage=xunzi 성악·화성기위 (thinker 일치, 원문 인용 할루시네이션 — 원문에는 "性惡·禮治" 없음)
  - 기입형5: 원문=zhuxi 격물치지·대학 (coverage zhuxi 일치, 메모는 대체로 타당)
  - 기입형7: 원문=habermas 이상적 담화 / coverage=hobbes 자연상태 ❌
  - 기입형8: 원문=다중 주제 십자말풀이(hobbes/kohlberg/marx/schopenhauer) / coverage=locke 자연권 ❌
  - 기입형9: 원문=plato 항해사·동물사육사·철인정치 / coverage=rousseau 일반의지 ❌
  - 기입형10: 원문=[통일·인권] 헬싱키/UN 대북결의 / coverage=rawls 정의의 두 원칙 ❌
- 사용자 판정 대기

### BLK-175B-005 — 2016~2019 A/B 문항 수 분배 오류
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L177, 213, 249, 285 (각 연도 헤더)
- 심각도: blocker
- 사유: 원본 2016~2019의 실제 문항 수는 **A=14 (기입형 8 + 서술형 6), B=8 (서술형 5 + 서술형 10점 1 등)** 인데 coverage-map은 "A=12(기입형4+서술형8), B=10"으로 잘못 분배. 연도 합계(22)는 우연히 일치하지만, A/B 경계가 잘못되어 약 16개 row가 잘못된 과목 섹션에 배치됨.
- 원문 근거: 각 연도 md 파일의 `### N. [M점]` 개수 직접 카운트 (wc/grep 교차 확인):
  - 2016: 전공A ## 카운트 = 14, 전공B ## 카운트 = 8
  - 2017: 전공A ### 카운트 = 14, 전공B ### 카운트 = 8
  - 2018: 전공A ### 카운트 = 14, 전공B ### 카운트 = 8
  - 2019: 전공A ### 카운트 = 14, 전공B ### 카운트 = 8
- 영향: 2016~2019 섹션의 B쪽 "서술형9, 10"으로 라벨된 row(각 연도당 약 2개)는 실제 B시험에 존재하지 않음 — 허구 row 또는 A→B 오배치.
- 사용자 판정 대기

### BLK-175B-006 — 2016-A 기입형 사상가 오매핑 샘플
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L183~186
- 심각도: blocker
- 사유: 2016-A 기입형 1~4의 원문 내용이 coverage-map 매핑과 다름.
- 원문 근거: `2016중등1차-도덕윤리-전공A.md` L16~66
- 샘플:
  - 기입형1: 원문=rest 4구성요소·도덕적 민감성·테레사 수녀 / coverage=[교육과정] 2015 도덕과 성격·목표 ❌
  - 기입형2: 원문=[교과교육학] 사회정서학습(SEL) 5역량 / coverage=kohlberg 도덕성 발달 ❌
  - 기입형3: 원문=wangyangming 치지격물 비판·지행합일 / coverage=mencius 사단·인의예지 ❌
  - 기입형4: 원문=yihwang(또는 yiyulgok) 理氣겸·性情·미발/이발 / coverage=kant 선의지·의무 ❌
- 2016-A 서술형 및 B쪽 매핑도 재검증 필요 (본 샘플은 3문항만 확인).
- 사용자 판정 대기

### BLK-175B-007 — Section E 분류 카운트 claim과 실제 row classification 불일치
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L705~720 (Section E 표)
- 심각도: blocker (BLOCKER-1 재발)
- 사유: Coder가 "Section E 산식 검증 (222+35+36=293 ✅)"을 주장했으나, 실제 row-by-row 분류 카운트는 **231 / 29 / 33 / 293** (사상가형 / 교과교육학 / 경계영역 / 합계). 총합만 우연히 일치. 연도별 7개 row(2014, 2015, 2016, 2017, 2022, 2023, 2024, 2025)가 Section E 주장과 불일치.
- 실제 재집계:
  ```
  2014: 20/ 2/ 2/24 (claim 18/2/4)
  2015: 17/ 0/ 3/20 (claim 15/2/3)
  2016: 20/ 1/ 1/22 (claim 19/2/1)
  2017: 19/ 0/ 3/22 (claim 19/1/2)
  2022: 20/ 3/ 0/23 (claim 19/3/1)
  2023: 14/ 5/ 4/23 (claim 13/5/5)
  2024: 15/ 4/ 4/23 (claim 13/5/5)
  2025: 13/ 5/ 5/23 (claim 13/6/4)
  ```
- 근거: `awk` + python 재집계 로그 (Tester TASK-175B 세션)
- 사용자 판정 대기

### BLK-175B-008 — Paul Taylor `taylor_p` planned id가 `paul_taylor`로 혼용됨
- 일시: 2026-04-20
- 위치: exam-coverage-map.md 전역 (L171, L245, L281, L354, L560, L587 등)
- 심각도: bug
- 사유: Coder report(L34)는 "`taylor_p` = Paul Taylor → '없음(누락, planned: taylor_p)' 표기"라고 명시했으나, coverage-map 본문과 Section A는 모두 `planned: paul_taylor`로 기재. 내부 일관성 불일치. architecture.md에 확정된 taylor_p/paul_taylor 어느 쪽이 canonical planned id인지 사용자 확정 필요.
- 원문 근거: coverage-map.md L587 "paul_taylor | 폴 테일러 ... 5회+"
- 사용자 판정 대기

### BLK-175D-001 — 2016-B/2017-B/2018-B/2019-B "서술형9, 10" phantom row
- 일시: 2026-04-20
- 위치: exam-coverage-map.md 각 연도 B 섹션 서술형9~10 rows
- 심각도: blocker
- 사유: 2016~2019년 B과목의 실제 문항 수는 **8**(BLK-175B-005로 확인), 그런데 coverage-map은 각 연도 B에 서술형9, 10을 추가 기재. 이는 존재하지 않는 문항. 특히 2017-B-서술형10, 2018-B-서술형10, 2019-B-서술형10은 coverage가 paul_taylor/leopold/jonas 등 환경윤리로 매핑했으나 원문에 해당 사상가 키워드 0건 (BLK-175D-002와 중복).
- 원문 근거: 각 연도 전공B md 파일의 `###` 카운트 = 8 (BLK-175B-005 기록)
- 사용자 판정 대기

### BLK-175D-002 — 환경윤리 할루시네이션 (2017-B-서10, 2018-B-서10, 2020-B-서11)
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L281, 301, 376
- 심각도: blocker
- 사유: coverage는 해당 문항을 paul_taylor/leopold/jonas/singer/regan 매핑했으나, 실제 원문에서 "생명중심", "대지윤리", "land ethic", "책임원칙", "종차별", "삶의 주체", "Taylor", "Leopold", "Jonas", "Singer", "Regan" 키워드 **0건**. 2017-B/2018-B의 경우 해당 번호 문항 자체가 존재하지 않음(BLK-175D-001). 2020-B-서11은 실제로는 다른 주제(재검증 필요).
- 원문 근거: grep -ci "testamente|leopold|jonas|paul_taylor" 대상 파일에서 0건
- 영향: Section A의 paul_taylor/leopold "5회+" 빈도 claim의 주요 근거가 허구.
- 사용자 판정 대기

### BLK-175D-003 — 2015-A 기입형4 "化性起僞" 원문 미등장
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L154 (2015-A 기입형4)
- 심각도: blocker
- 사유: coverage가 2015-A 기입형4를 "xunzi 성악·화성기위"로 매핑했으나, 원문 제시문에는 "化性起僞" 구절이 직접 등장하지 않음. 원문의 실제 핵심은 xunzi의 **천인분이(天人之分)** + **예/예의(禮/禮義)**. 사상가 id(xunzi)는 맞지만 메모의 원문 인용이 할루시네이션. BLOCKER-4 재발(원문 인용 할루시네이션).
- 원문 근거: 2015중등1차-도덕윤리_전공A.md 기입형4 제시문 (가)·(나) 전문 — "性惡", "化性起僞", "禮治" 키워드 0건
- 사용자 판정 대기

### BLK-175D-004 — Section A 출제 빈도 과장 (paul_taylor 5회+ → 실제 2회)
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L612~616 (Section A 상위 빈도 사상가)
- 심각도: blocker
- 사유: coverage가 Section A에서 paul_taylor/leopold를 "5회+" 빈도로 기재했으나, 본 Tester의 원문 직독 결과 **paul_taylor 확증 2회** (2021-A-서술형5, 2026-A-서술형12), **leopold 확증 1회** (2026-A-서술형12). 나머지 3~4회는 BLK-175D-002의 할루시네이션에 기반. 동일 문항을 여러 사상가에게 중복 기재하는 구조적 결함도 있음(한 row에 paul_taylor/leopold/singer/regan/jonas 5인 모두 매핑).
- 원문 근거: 2015-B, 2017-B, 2018-B, 2020-B 원문에서 해당 사상가 trademark 키워드 grep 0건 또는 부분 등장 재검증 필요.
- 영향: "1순위 등록: paul_taylor, leopold, singer, regan (각 3회+)" claim은 2회+ 이하로 하향. 후속 태스크 TASK-176 우선순위 재조정 필요.
- 사용자 판정 대기

### BLK-175D-005 — Section B canonical 사상가 빈도 오염
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L650~705 (Section B 집계 테이블)
- 심각도: blocker
- 사유: Section B의 "xunzi 6회+, mencius 10회+, confucius 9회+, laozi 6회+, zhuangzi 5회+, wonhyo 7회+" 등은 2021-B와 2022-B의 fabricated "동양 연속 서술형 시퀀스" 오매핑(BLK-175D-008, BLK-175D-010) 기반 집계이므로 2회 이상 과대 계상. 실제 빈도 재집계 필요. 반대로 habermas, kant, aristotle 등은 상대적으로 정확.
- 원문 근거: 2021-B-서1~11 실제=jinul/locke/turiel+haidt/durkheim+piaget/rest+hoffman/laozi+zhuangzi/yi_i+yi_hwang/sartre+kierkegaard/aristotle+mill/cicero/habermas, 2022-B-서1~11 실제=popper/[통일]/durkheim+piaget/mill/xunzi/mozi+hanfeizi/james+dewey/hoffman+noddings/singer+rawls/zhuxi+yi_hwang/haidt
- 사용자 판정 대기

### BLK-175D-006 — 2020-B 11문항 전면 오매핑 (전면 fabricated sequence)
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L366~376 (2020-B 전체)
- 심각도: blocker
- 사유: coverage의 2020-B-서1~11은 "confucius→xunzi→laozi→buddha→wonhyo→plato→aristotle→bentham→hegel→habermas→환경" 순의 이상적 배열로, 이는 동양·서양·응용윤리를 순서대로 나열한 가상 시나리오로 보임. 실제 2020-B 원문과 불일치. BLK-175B의 "2020~2026 양호" 판정을 정면 반박.
- 원문 근거: 2020_중등1차_도덕윤리_전공B.md — 실제 11문항은 별도 주제 분포 (앞 TASK-175B의 spot-check도 이 연도를 실제로는 확인하지 않은 것으로 판명)
- 사용자 판정 대기

### BLK-175D-007 — 2021-A 10/12 오매핑
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L385~397 (2021-A 전체)
- 심각도: blocker
- 사유: 원문 vs coverage 사상가 대조 결과 기입형2(kant 영구평화→aristotle), 기입형3(moore 비자연주의→confucius), 기입형4(spinoza conatus→kant), 서술형1(shaftel 역할놀이→noddings), 서술형2(blasi+kohlberg 자기통합성→plato), 서술형4(초기불교 무아무상→wangyangming), 서술형5(paul_taylor 생명중심→hobbes+locke), 서술형6(kant 거짓약속→mill_js), 서술형8(6·15선언→walzer). 교정된 것은 기입형1(교육과정)과 서술형7(rawls, 주제는 정의론→시민불복종 달라짐) 부분 일치만.
- 원문 근거: 2021_중등1차_도덕윤리_전공A.md 전문 독립 풀이
- 사용자 판정 대기

### BLK-175D-008 — 2021-B 11/11 오매핑 (fabricated 동양 연속 시퀀스)
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L403~413 (2021-B 전체)
- 심각도: blocker
- 사유: coverage의 2021-B-서1~11은 "mencius→xunzi→laozi+zhuangzi→hanfeizi→buddha+huineng→wonhyo→yihwang+yiyulgok→jeongyagyong→augustine+aquinas→hume→habermas" 동양·한국·서양 순서 배열. 실제 2021-B는 jinul+uicheon/locke/turiel+haidt/durkheim+piaget/rest+hoffman/laozi+zhuangzi/yi_i+yi_hwang/sartre+kierkegaard/aristotle+mill/cicero/habermas. 유일 일치는 habermas(서11)와 laozi+zhuangzi(서6, coverage는 서3으로 배치), yi_i+yi_hwang 과목 일치뿐.
- 원문 근거: 2021_중등1차_도덕윤리_전공B.md 전문 독립 풀이
- 사용자 판정 대기

### BLK-175D-009 — 2022-A 10/12 오매핑
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L423~434 (2022-A 전체)
- 심각도: blocker
- 사유: 교정은 기입형1(lickona), 기입형2(jinul)만 정확. 기입형3(미국 공화주의→socrates), 기입형4(jeongyagyong 인심도심→mencius), 서술형1(nozick 최소국가→kohlberg+gilligan), 서술형2(pettit+berlin→aristotle), 서술형3(plato 이상국가 사유재산금지→aquinas), 서술형4(kohlberg+turiel→kant), 서술형5(kant 거짓약속→bentham+mill), 서술형6(huineng+shenxiu+zhiyi→rawls+nozick), 서술형7(kant+beccaria 사형제→sandel+macintyre) 오매핑. 서술형8만 서술형6 내용(huineng/zhiyi)이 뒤늦게 기재됨.
- 원문 근거: 2022_중등1차_도덕윤리_전공A.md 전문 독립 풀이
- 사용자 판정 대기

### BLK-175D-010 — 2022-B 10/11 오매핑 (fabricated 동양 연속 시퀀스)
- 일시: 2026-04-20
- 위치: exam-coverage-map.md L440~450 (2022-B 전체)
- 심각도: blocker
- 사유: coverage의 2022-B-서1~11은 "confucius→mencius→xunzi→laozi→zhuangzi→buddha→wonhyo→zhuxi→wangyangming→jeongyagyong→haidt" 동양·한국 순 배열. 실제는 popper/[통일교육]/durkheim+piaget/mill_js/xunzi/mozi+hanfeizi/james+dewey/hoffman+noddings/singer+rawls/zhuxi+yi_hwang/haidt. 유일 일치는 서술형5의 xunzi(내용은 대청명)와 서술형11의 haidt.
- 원문 근거: 2022_중등1차_도덕윤리_전공B.md 전문 독립 풀이
- 사용자 판정 대기

### BLK-175D-011 — TASK-175B "2020~2026 대체로 양호" 판정 부실 검증
- 일시: 2026-04-20
- 위치: `signal/ethics-study/tester-report-TASK-175B.md` (참조)
- 심각도: observation (Tester 프롬프트·프로세스 개선 과제)
- 사유: TASK-175B Tester는 2020~2026을 "spot-check 통과"로 판정했으나, 본 TASK-175D 전수 검증 결과 2020-B, 2021-A/B, 2022-A/B는 전면 오매핑. TASK-175B는 특정 연도(2023~2026)만 샘플로 확인하고 2020~2022를 검증하지 않은 것으로 추정됨. Tester 프롬프트에 "전수 검증 필수, 연도별 spot-check 금지" 조항 추가 필요.
- 후속 조치 제안: `agents/tester.md` Phase 6 검증 규칙에 "대조 대상 파일의 모든 row를 원문과 개별 대조한 내역을 테이블로 보고해야 함" 명시. retrospective에서 사용자 승인 후 반영.
- 사용자 판정 대기

## 해소된 블로커

### BLK-175B-001~006, BLK-175D-006~010 — 사용자 spot-check 판정 완료 (2026-04-20)
- 사용자가 5건 블로커에 대해 원문 대조 spot-check 진행, Tester 판정이 전건 정확함 확인:
  - BLK-175B-001 (2014-A): 5/5 일치
  - BLK-175B-002 (2014-B): 4/4 일치
  - BLK-175B-003 (2014-B 할루시네이션): 자동 확정
  - BLK-175B-004 (2015-A): 5/5 일치
  - BLK-175B-005 (2016~2019 A/B 분배): A=14·B=8 전건 확인
  - BLK-175D-006~010 (2020~2022 전면 오매핑): Tester TASK-175D 전수 검증 결과 채택
- 사용자 지시: "전면 재작성하자. 새 규칙을 통해서 순차적으로 처리하자." (2026-04-20)
- 해소 경로: TASK-175E-YYYY-{A|B} 재작성 + -T 검증 전수 PASS 시 각각 최종 해소.

### BLK-001 (TASK-174) — 전면 재작성 진행 중
- 2차 재시도(TASK-175A) 및 전수 재검증(TASK-175D) 모두 실패. v1/v2 백업 완료:
  - `projects/ethics-study/exam-solutions/exam-coverage-map.v1-rejected.md`
  - `projects/ethics-study/exam-solutions/exam-coverage-map.v2-rejected.md`
- 신규 출력 경로: `projects/ethics-study/exam-solutions/coverage/YYYY-{A|B}.md`
- architecture.md Phase 6 기출 작업 규칙 적용:
  - 추론 금지 대전제
  - Coder 3단계 확정 (발문→제시문→사상가)
  - 메모 컬럼 원문 구절 복사 + file_path:line_range 병기
  - 배치 크기 1회=1연도×1과목
  - Tester 전수 검증 필수 (spot-check 금지, ethics-study 전용 규칙)
  - grep 0건 자동 블로커
- TASK-175E 시리즈 26 sub-task + 26 검증 + MERGE 등록 완료.
- 해소 경로: TASK-175E 시리즈 전체 PASS 후 최종 해소.

## 사용자 검토 대기

### BLK-175B-007 — Section E 분류 카운트 불일치
- TASK-175E-MERGE 단계에서 Section E를 자동 재집계하므로 본 블로커는 MERGE 후 자동 해소 예정.

### BLK-175B-008 — Paul Taylor planned id 혼용
- TASK-175E 재작성 시 `taylor_p` vs `paul_taylor` 중 하나로 통일 필요. 현 architecture.md "thinker_id 정규화 규칙"은 Paul Taylor를 `taylor_p`로 예시 표기. 사용자 최종 확정 필요.

### BLK-175D-001~005, BLK-175D-011 — TASK-175E 재작성 + MERGE로 해소 예정
- BLK-175D-001 (phantom row): 연도별 파일 분리로 원천 방지.
- BLK-175D-002 (환경윤리 할루시네이션): 원문 grep 0건 규칙 + 복사 인용 강제로 차단.
- BLK-175D-003 (xunzi 화성기위 할루시네이션): 복수 주제 복사 인용 규칙으로 차단.
- BLK-175D-004, BLK-175D-005 (Section A/B 빈도 오염): TASK-175E-MERGE에서 자동 재집계.
- BLK-175D-011 (Tester 허위 통과): architecture.md Tester 규칙 4번(전수 검증 필수, spot-check 금지)로 차단.

### BLK-175E-2015A-001 (TASK-175E-2015-A) — 기입형 4 (나) 빈칸 정답 개념어 미확정
- 일시: 2026-04-20
- 산출물: `projects/ethics-study/exam-solutions/coverage/2015-A.md` 기입형 4 row
- 원문: `~/잡동사니/임용/md/2015중등1차-도덕윤리_전공A.md` L54~L61
- 심각도: blocker (Coder 판정; 원문 직독 원칙상 정답 단정 불가)
- 사유:
  - (가) 사상가 = 순자(荀子 — xunzi) **확정**. Trademark: "하늘의 운행에는 일정함이 있으니, 이 일정함은 요(堯)임금을 존립하게 하는 것도 아니고, 걸(桀)왕을 망하게 하는 것도 아니다"(L58, 『天論』 "天行有常 不爲堯存 不爲桀亡"), "사람은 하늘과 직무를 두고 다투지 않는다"(L58, 『天論』 "不與天爭職").
  - (나) 편지 빈칸 "(     )이/가 바로 그 법도라네"(L61)의 정답 개념어는 **원문에 직접 표기되지 않음**. 원문에 존재하는 단서는 "선(善)한 것을 분별하는 법도", "기운을 다스리고 양생", "팽조(彭祖)보다 오래 살 수 있음", "몸을 닦고 스스로 노력", "요임금이나 우임금처럼 될 수 있음", "곤경에 처했을 때도 유리" 등 의미 수준에 한정.
  - 원문 대상 `grep -F` 결과 부재 검증:
    - `禮` → 0 hit
    - `예의` → 0 hit
    - `化性`, `化性起僞`, `化性起偽` → 0 hit
    - `화성기위` → 0 hit
    - `천인분이`, `天人分異`, `天人分二` → 0 hit
  - 후보군:
    1. **예(禮 — 禮義, 예의)**: 순자 『수신편(修身篇)』 "禮者 所以正身也", 『권학편(勸學篇)』 "禮者 … 養生送死 … 愼終始之道也"가 "기운 다스리고 양생·몸 닦고 스스로 노력"과 직접 대응. **가장 유력**. 빈칸 어법상 "**예의**가 바로 그 법도라네"로 자연스러움.
    2. **화성기위(化性起僞 — 본성을 교화해 인위를 일으킴)**: 『성악편(性惡篇)』 trademark. "본성을 교화하여 인위(禮·義·法度)를 일으킴"이라는 의미상 "법도"와 연결 가능하나, 빈칸 자체는 "그 **법도**"라는 명사형이 필요하므로 어법상 다소 어색.
- 후속 조치: 사용자(수험 공부 당사자) 판정 대기. 사용자 확정 시 BLOCKER 해소 + row 갱신.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2015-A): ... -->` (2015-A.md 본문에 인라인 삽입)

### BLK-175E-2015A-002 (TASK-175E-2015-A) — 기입형 8 세로 낱말 (A) 4글자 개념어 미확정
- 일시: 2026-04-20
- 산출물: `projects/ethics-study/exam-solutions/coverage/2015-A.md` 기입형 8 row
- 원문: `~/잡동사니/임용/md/2015중등1차-도덕윤리_전공A.md` L101~L114
- 심각도: blocker (Coder 판정; 퍼즐 그림 미제공으로 격자 재구성 불가)
- 사유:
  - 기입형 8은 **십자말풀이(crossword) 퍼즐 문제**. 가로 (A)~(D) 힌트는 텍스트로 제공되나, **격자 배치·세로 (A)와 각 가로 항목의 교차 위치·공유 글자 정보는 그림 형태로만 제공**되고 md 원문에는 "(A) …… □□□□ 개념"이라고만 기재(L114).
  - 가로 답 추정(trademark 기반):
    - (A) 홉스 "□□□ 1조항 … 평화" → **자연법(自然法)** 3글자
    - (B) 도덕 판단의 "□□(이)나 근거 제시" → **이유(理由)** 2글자
    - (C) 마르크스 "허위□□" → **의식(意識)** 2글자
    - (D) 쇼펜하우어 "살고자 하는 본능·충동·욕망" → **의지(意志)** 2글자
  - 세로 (A)는 가로 (A)와 첫 글자를 공유하므로 첫 글자 = "자". 그러나 남은 3글자에 대응하는 가로 (B)/(C)/(D)의 공유 위치를 격자 없이 재구성 불가.
  - 후보군(홉스 정치철학 4글자 개념):
    1. **자연상태(自然狀態 — state of nature)**: 홉스 『리바이어던』 핵심 개념, 4글자. 첫 글자 "자"와 일치. **가장 유력**(교과서·기출 해설서 통설).
    2. **사회계약(社會契約)**: 4글자, 단 첫 글자 "사" → 가로 (A) "자"와 불일치. 탈락.
    3. **자연권리(自然權利)** / **자연권(自然權)**: 4글자/3글자. "자연권" 3글자이므로 "□□□□" 4글자 조건 미충족.
  - 원문 직독만으로는 최종 확정 불가(격자 정보 필요). 다만 후보 ①(자연상태)가 trademark 정합도·글자수·첫글자 일치 3가지 모두 충족.
- 후속 조치: 사용자 판정 또는 Manager가 기출 해설서·격자 이미지 참조로 확정. 사용자 확정 시 BLOCKER 해소 + row 갱신.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2015-A): ... -->` (2015-A.md 본문에 인라인 삽입)

### BLK-175E-2016A-001 — 2016-A Q4 스승·제자 구체 인명 미특정
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2016-A.md` Q4 row
- 원문: `/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공A.md` L53-L65
- 심각도: observation (사상가 계보는 확정 / 구체 인명만 미확정)
- 사유: 제시문의 스승-제자 대화가 "성즉리 + 심통성정 + 미발 존양/이발 성찰"의 교리 3중 일치로 이황(yihwang) 계보임은 확정적이나, 특정 스승·제자 인명을 원문만으로 단정 곤란. 이황과 기대승(사칠논변) 직계인지, 이황 문인과의 문답(『성학십도』 주해)인지, 또는 이황 자신의 가상 대화인지의 판정 근거는 제시문 내 트레이드마크로 부재.
- 후속 조치: 사용자 판정 또는 Manager가 기출 해설서 참조로 확정. 현재 판정은 yihwang 계보 확정(답 = 심/심통성정).
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2016-A-001): ... -->` (2016-A.md Q4 row에 인라인 삽입)

### BLK-175E-2016A-002 — 2016-A Q5 을 지눌(知訥, 보조국사) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2016-A.md` Q5 을
- 원문: `/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공A.md` L75-L83
- 심각도: blocker (ES 커버리지 누락)
- 사유: Q5 을 사상가 지눌(知訥, 보조국사)의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록. Trademark 3중 일치(돈오점수·정혜쌍수·"얼어붙은 못이 물임을 알아도 얼음이 물로 변하지 않음"·교관병수·『수심결』·『권수정혜결사문』)로 사상가 판정은 확실하나, claim 보강 불가 상태.
- 후속 조치: TASK-176 범위에서 jinul 사상가 신규 등록 + claim 작성(돈오점수설·정혜쌍수·수심결·권수정혜결사문·교관병수·삼문교과관·한국 조계종). 후보 id: `jinul`.
- 영향: Q5 답(정[定]·정혜쌍수) 판정 자체는 trademark로 확정됨. 단 ES 대조 검증은 현재 불가.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2016-A-002): ... -->` (2016-A.md Q5 row에 인라인 삽입)

### BLK-175E-2016A-003 — 2016-A Q6 한스 요나스(Hans Jonas) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2016-A.md` Q6
- 원문: `/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공A.md` L87-L92
- 심각도: blocker (ES 커버리지 누락)
- 사유: Q6 사상가 한스 요나스(Hans Jonas)의 canonical thinker_id가 ES 인덱스에 미등록. Trademark 3중 일치("집단적 실천 새로운 영역 · 윤리적 진공 상태"·"미리 사유된 위험"·"희망보다는 공포" → 『책임의 원리[Das Prinzip Verantwortung, 1979]』의 공포의 발견술[Heuristik der Furcht])로 사상가 판정은 확실.
- 후속 조치: TASK-176 범위에서 jonas 사상가 신규 등록 + claim 작성(책임의 원리·공포의 발견술·미래 세대 책임·윤리적 진공·생명의 존재론적 원리·기술 문명 비판). 후보 id: `jonas`.
- 영향: Q6 답(공포의 발견술) 판정 자체는 trademark로 확정됨.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2016-A-003): ... -->` (2016-A.md Q6 row에 인라인 삽입)

### BLK-175E-2016A-004 — 2016-A Q9 나바에즈(Darcia Narvaez) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2016-A.md` Q9
- 원문: `/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공A.md` L112-L122
- 심각도: blocker (ES 커버리지 누락)
- 사유: Q9 사상가 나바에즈(Darcia Narvaez)의 canonical thinker_id가 ES 인덱스에 미등록. 발문 내 사상가명 직접 명시(L122 "나바에즈(D. Narvaez)") + Trademark 3중 일치("통합적 윤리 교육 모델[Integrative Ethical Education]"·"4과정 모형[Four Process Model]"·"각 과정마다 7가지 윤리적 기술"·"초보자 vs 전문가 대비")로 사상가 판정은 확실.
- 후속 조치: TASK-176 범위에서 narvaez 사상가 신규 등록 + claim 작성(통합적 윤리 교육 모델·윤리적 전문가[ethical expert]·4×7 ethical skills·신콜버그 계열·rest 4구성 요소 계승). 후보 id: `narvaez`.
- 영향: Q9 답(윤리적 전문가) + 학습 내용·환경 관련 2가지(풍부한 보살핌 분위기·윤리적 기술 직접 교수)는 trademark로 확정됨.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2016-A-004): ... -->` (2016-A.md Q9 row에 인라인 삽입)

### BLK-175E-2016A-005 — 2016-A Q10 을 호프만(Martin L. Hoffman) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2016-A.md` Q10 을
- 원문: `/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공A.md` L126-L136
- 심각도: blocker (ES 커버리지 누락)
- 사유: Q10 을 사상가 호프만(Martin L. Hoffman)의 canonical thinker_id가 ES 인덱스에 미등록. Trademark 3중 일치("공감적 정서가 결합된 인지 활성화 = 뜨거운 인지[hot cognition]"·"귀납적 훈육[inductive discipline]"·"공감의 발달을 위한 교육 방법의 핵심")으로 사상가 판정은 확실. 저작 『공감과 도덕발달(Empathy and Moral Development, 2000)』 및 유발 공감 5단계 발달 이론.
- 후속 조치: TASK-176 범위에서 hoffman 사상가 신규 등록 + claim 작성(공감 발달 5단계·귀납적 훈육·뜨거운 인지·공감적 고통[empathic distress]·힘 과시형 vs 애정 철회형 vs 귀납적 훈육의 3분법). 후보 id: `hoffman`.
- 영향: Q10 답(뜨거운 인지) + 귀납적 훈육 적용 예시 2가지는 trademark로 확정됨.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2016-A-005): ... -->` (2016-A.md Q10 row에 인라인 삽입)

### BLK-175E-2016A-006 — 2016-A Q11 을 양주(楊朱, 양자) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2016-A.md` Q11 을
- 원문: `/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공A.md` L140-L148
- 심각도: blocker (ES 커버리지 누락)
- 사유: Q11 을 사상가 양주(楊朱, 양자)의 canonical thinker_id가 ES 인덱스에 미등록. Trademark 3중 일치("자기만을 위하는 입장 = 위아[爲我]"·"털 한 오라기를 뽑아 천하 사람들을 이롭게 할 수 있어도 하지 않음" = 『맹자·진심상』 "楊子取爲我 拔一毛而利天下 不爲也"·"군주[君主]를 부정" = 『맹자·등문공하』 "楊氏爲我 是無君也")로 사상가 판정은 확실. 전국 시대 도가 초기 지류, 『열자·양주편』·『회남자』·『한비자』에 단편 전승.
- 후속 조치: TASK-176 범위에서 yangzi 사상가 신규 등록 + claim 작성(위아·귀기·경물중생·털 한 오라기·맹자 양묵 비판의 대상·『열자』 양주편). 후보 id: `yangzi`.
- 영향: Q11 답(위아) + 맹자 비판에 대한 양주 반론은 trademark로 확정됨.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2016-A-006): ... -->` (2016-A.md Q11 row에 인라인 삽입)

### BLK-175E-2016A-007 — 2016-A Q13 갑 G. E. 무어(George Edward Moore) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2016-A.md` Q13 갑
- 원문: `/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공A.md` L162-L173
- 심각도: blocker (ES 커버리지 누락)
- 사유: Q13 갑 사상가 G. E. 무어(George Edward Moore)의 canonical thinker_id가 ES 인덱스에 미등록. Trademark 3중 일치("'선(good)'은 분석할 수 없는 단순한 속성" = 『윤리학 원리[Principia Ethica, 1903]』 §13 "Good is a simple notion"·"선을 (자연적 속성으로) 정의하려는 일체의 시도는 ㉠ = 자연주의적 오류[naturalistic fallacy]"·"비자연주의적 직관주의[non-naturalistic intuitionism]")로 사상가 판정은 확실.
- 후속 조치: TASK-176 범위에서 moore 사상가 신규 등록 + claim 작성(자연주의적 오류·미결 문제 논증[open question argument]·선=단순 비자연적 속성·윤리적 직관주의·『윤리학 원리』·블룸즈버리 그룹 철학자). 후보 id: `moore`.
- 영향: Q13 답(㉠ = 자연주의적 오류) + 갑(무어)의 도덕적 인식론(직관으로 단순 속성 지각)은 trademark로 확정됨.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2016-A-007): ... -->` (2016-A.md Q13 row에 인라인 삽입)

### BLK-175E-2016B-001 — 2016-B Q3 공동체주의 단일 사상가 특정 제한
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2016-B.md` Q3
- 원문: `/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공B.md` L44-L49
- 심각도: blocker (단일 사상가 특정 제한 — 답 확정 자체는 trademark 3중 일치로 가능)
- 사유: Q3 제시문이 공동체주의 일반론 형식("자유주의자들은 인간을 이성을 지닌 자율적·독립적 존재로 보는 반면에, 공동체주의자들은 ( ) 존재로 파악" + "공동선" + "국가의 중립성과 관련하여 공동체주의자들의 입장은 자유주의자들과 다르다")으로 서술되어, 단일 공동체주의 사상가의 고유 trademark 구절(샌델의 "encumbered self"·테일러의 "원자론 비판"·매킨타이어의 "덕 이후"·왈처의 "영역적 정의") 중 어느 하나의 결정적 문자가 인용되지 않음. "사회적 의존성·공동선·무연고적 자아 대비 + 중립성 부정 + 공동선 정치 보완" 구도는 sandel의 『Liberalism and the Limits of Justice』·『Justice』 trademark와 가장 완전하게 근접하므로 대표 thinker_id = `sandel`로 매핑하되, 분류는 "공동체주의 일반"으로 확정한다.
- 후속 조치: 답 용어(빈칸 = "연고적 자아 / 공동체에 의해 구성되는 사회적 존재") 및 ㉡ 해설(중립성 불가능 + 공동선 정치 + 적극적 국가 역할)은 trademark 3중 일치로 확정 상태. 사용자 일괄 검토 시 "sandel 단일 매핑으로 확정"할지 "sandel(+macintyre·taylor·walzer) 복합 매핑으로 확정"할지 판정 필요.
- 영향: Q3 답과 서술 내용은 확정됨. 사상가 단일 특정의 불확실성만 등록.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2016-B-001): ... -->` (2016-B.md Q3 row에 인라인 삽입)

### BLK-175E-2016B-002 — 2016-B Q4 (가) 이사야 벌린(Isaiah Berlin) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2016-B.md` Q4 (가)
- 원문: `/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공B.md` L53-L59
- 심각도: blocker (ES 커버리지 누락)
- 사유: Q4 (가) 사상가 이사야 벌린(Isaiah Berlin, 1909-1997)의 canonical thinker_id가 ES 인덱스에 미등록. Trademark 3중 일치("자유의 의미와 관련하여 두 가지를 검토" = 『자유의 두 개념(Two Concepts of Liberty, 1958)』 옥스퍼드 취임 강연 제목·"간섭 없이 스스로 할 수 있는 일 … 방임하여야 할 영역" = 소극적 자유[negative liberty] 표준 정의·"통제의 근원이 누구 또는 무엇인가" = 적극적 자유[positive liberty] 표준 정의)로 사상가 판정은 확실.
- 후속 조치: TASK-176 범위에서 berlin 사상가 신규 등록 + claim 작성(소극적 자유·적극적 자유·가치 다원주의[value pluralism]·자유주의 개념사·비극적 선택·『고슴도치와 여우』·『자유의 두 개념』·반전체주의). 후보 id: `berlin`.
- 영향: Q4 답(㉠ = 소극적 자유 / ㉡ = 적극적 자유)은 trademark로 확정됨.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2016-B-002): ... -->` (2016-B.md Q4 row에 인라인 삽입)

### BLK-175E-2016B-003 — 2016-B Q4 (나) 마키아벨리(Niccolò Machiavelli) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2016-B.md` Q4 (나)
- 원문: `/home/jai/잡동사니/임용/md/2016중등1차-도덕윤리-전공B.md` L53-L59
- 심각도: blocker (ES 커버리지 누락)
- 사유: Q4 (나) 사상가 니콜로 마키아벨리(Niccolò Machiavelli, 1469-1527)의 canonical thinker_id가 ES 인덱스에 미등록. Trademark 3중 일치("평민과 귀족 간의 내분을 비난하는 사람들은 로마를 자유롭게 만든 일차적 원인을 비난" + "모든 공화국에는 두 개의 대립된 파벌" = 『로마사 논고(Discorsi sopra la prima deca di Tito Livio, 1531)』 I권 4장 직접 번역·"로마가 자유를 향유할 수 있도록 제정된 모든 법률은 그들의 불화에서 비롯" = 같은 책 사회 갈등의 자유 원리 trademark·"평민의 열망 = 억압으로부터 + 억압 발생 두려움으로부터" = 『로마사 논고』 I권 5장 비지배 자유 = non-domination 원류)로 사상가 판정은 확실. 공화주의 전통(neo-Roman republicanism — Skinner·Pettit 계승)의 원류.
- 후속 조치: TASK-176 범위에서 machiavelli 사상가 신규 등록 + claim 작성(공화주의적 자유·비지배·평민-귀족 갈등 = 자유의 원리·비르투[virtù]·포르투나[fortuna]·네체시타[necessità]·『군주론』·『로마사 논고』·vivere civile·libertà). 후보 id: `machiavelli`.
- 영향: Q4 (나)의 자유 설명(공화주의적 자유 = 비지배 + 시민적 자유 + 제도적 견제)은 trademark로 확정됨.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2016-B-003): ... -->` (2016-B.md Q4 row에 인라인 삽입)

### BLK-175E-2017A-001 (TASK-175E-2017-A) — Q2 블라지(Augusto Blasi) ES 미등록
- 일시: 2026-04-20
- 위치: `projects/ethics-study/exam-solutions/coverage/2017-A.md` Q2 row
- 심각도: blocker (ES 커버리지 누락)
- 사유: Q2 사상가 블라지(Augusto Blasi, 1933-2018)의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록. 자아 모델(self model of moral functioning) trademark 3중 일치("도덕적 정체성은 도덕성과 자아 정체성의 통합" + "도덕적 이해가 자아 개념의 한 부분" + "도덕적 이해는 실천으로 이어질 수 있게 된다" + "후회·슬픔·죄책감"의 자기 일관성 위반 정서)로 판정 확실. 답: **책임(責任 — responsibility, 책임 판단[responsibility judgment])**. 레스트(rest)·나바에즈(narvaez)·콜버그(kohlberg)와 함께 신콜버그 계열(neo-Kohlbergian) 도덕 심리학자.
- 후속 조치: TASK-176 범위에서 blasi 사상가 신규 등록 + claim 작성(자아 모델·도덕적 정체성·자아 통합·책임 판단·자기 일관성·『The Self and Moral Action』). 후보 id: `blasi`.
- 영향: Q2 정답 "책임"은 trademark 3중 일치로 확정됨.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2017A-001): ... -->` (2017-A.md Q2 row에 인라인 삽입)

### BLK-175E-2017A-002 (TASK-175E-2017-A) — Q4 지눌(知訥, 보조국사) ES 미등록 [중복: 2016-A BLK-002]
- 일시: 2026-04-20
- 위치: `projects/ethics-study/exam-solutions/coverage/2017-A.md` Q4 row
- 심각도: blocker (ES 커버리지 누락, 중복 발생)
- 사유: Q4 사상가 지눌(知訥, 보조국사, 1158-1210)의 canonical thinker_id가 ES 인덱스에 미등록. **2016-A 커버리지 작성 시 BLK-175E-2016A-002로 이미 등록된 동일 사상가**. 『수심결(修心訣)』 trademark 3중 일치("선지식의 가르침으로 올바른 길 + 자신의 본성을 똑똑히 보고서 + 모든 부처님과 털끝만큼도 다르지 않음" = 회광반조·견성·본래성불 = 돈오[頓悟] 정의 + "아기가 처음 태어났을 때 감각기관을 갖추고 있지만 힘이 충분치 못해 세월이 지나야 사람 구실" = 돈오점수[頓悟漸修]의 trademark 비유로 점수[漸修] 정의)로 판정 확실. 답: ㉠ **돈오(頓悟)** / ㉡ **점수(漸修)**. 지눌이 2회 연속 기출(2016-A Q5, 2017-A Q4)에 등장했으므로 ES 신규 등록 **최우선 순위**.
- 후속 조치: TASK-176 범위에서 jinul 사상가 신규 등록 + claim 작성(돈오점수·정혜쌍수·수심결·권수정혜결사문·교관병수·회광반조·견성·본래성불). 후보 id: `jinul`.
- 영향: Q4 정답 ㉠돈오/㉡점수는 trademark 3중 일치로 확정됨.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2017A-002): ... -->` (2017-A.md Q4 row에 인라인 삽입)

### BLK-175E-2017A-003 (TASK-175E-2017-A) — Q6 동학 최제우·최시형 ES 미등록
- 일시: 2026-04-20
- 위치: `projects/ethics-study/exam-solutions/coverage/2017-A.md` Q6 row
- 심각도: blocker (ES 커버리지 누락)
- 사유: Q6 사상가 동학(東學) 1대 교주 수운 최제우(水雲 崔濟愚, 1824-1864)·2대 교주 해월 최시형(海月 崔時亨, 1827-1898)의 canonical thinker_id가 ES 인덱스에 미등록. Trademark 3중 일치("모든 사람이 평등하고 차별이 없다" = 인시천[人是天]·사인여천[事人如天] + "나는 동(東)에서 나서 동에서 도(道)를 받았으니" = 최제우 『동경대전(東經大全)』 "論學文"의 동학 명명 유래 + "도의 실천은 대인(對人)과 접물(接物)에서 시작" = 최시형 대인접물[待人接物] 10조 + 경천·경인·경물[敬天·敬人·敬物] 삼경설)로 판정 확실. 답: **대인접물(待人接物)**.
- 후속 조치: TASK-176 범위에서 동학 신규 등록 + claim 작성(사인여천·인시천·대인접물·삼경설·『동경대전』·『용담유사』·『해월신사법설』·후천개벽·21자 주문·수심정기[守心正氣]·유무상자[有無相資]). 후보 id: `donghak_choe` (최제우 + 최시형 통합) 또는 `choejeu`·`choesihyeong` 별도 등록 검토.
- 영향: Q6 정답 "대인접물"은 trademark 3중 일치로 확정됨.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2017A-003): ... -->` (2017-A.md Q6 row에 인라인 삽입)

### BLK-175E-2017A-004 (TASK-175E-2017-A) — Q7 을 몽테스키외(Montesquieu) ES 미등록
- 일시: 2026-04-20
- 위치: `projects/ethics-study/exam-solutions/coverage/2017-A.md` Q7 row (을 인물)
- 심각도: blocker (ES 커버리지 누락)
- 사유: Q7 을 사상가 샤를-루이 드 스공다 몽테스키외(Charles-Louis de Secondat, Baron de Montesquieu, 1689-1755)의 canonical thinker_id가 ES 인덱스에 미등록. Trademark 3중 일치("트로글로다이트 인(人)들의 공동체" = 『페르시아인의 편지(Lettres persanes, 1721)』 편지 11~14의 트로글로다이트 우화 + "시민적 덕성은 공화정부의 정신이며 시민들 마음속에 자리 잡은 지배적 열정" = 『법의 정신(De l'esprit des lois, 1748)』 3권 3장 공화정의 원리=덕(vertu) + "시민들이 탐욕과 야심을 좇아 (법)을 무시하면 공화국은 와해" = 공화정에서 덕의 쇠퇴·법 무시 = 정체 붕괴론)로 판정 확실. 공통 용어 답: **법(法 — loi)** (루소와의 공통 개념).
- 후속 조치: TASK-176 범위에서 montesquieu 사상가 신규 등록 + claim 작성(『법의 정신』·삼권분립[separation of powers]·정체의 원리(공화정=덕·군주정=명예·전제정=공포)·『페르시아인의 편지』·법의 상대성·climate theory·중간 권력·영국 헌정 연구). 후보 id: `montesquieu`. 프랑스 계몽주의 정치철학의 주요 사상가로 고교 윤리·정치 교과서 단골 등장.
- 영향: Q7 정답 "법"은 루소의 trademark("법에 대한 복종이 곧 자유")와 몽테스키외의 trademark("공화정 원리=덕 + 덕이 쇠퇴하면 법을 무시하여 와해")의 공통 개념으로 확정됨.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2017A-004): ... -->` (2017-A.md Q7 row에 인라인 삽입)

### BLK-175E-2017A-005 (TASK-175E-2017-A) — Q10 쿰스·뮤(Coombs·Meux) 가치분석 모형 ES 미등록 (교과교육학 범주)
- 일시: 2026-04-20
- 위치: `projects/ethics-study/exam-solutions/coverage/2017-A.md` Q10 row
- 심각도: observation (교과교육학 범주로 ES 비등록 유지 가능)
- 사유: Q10 가치분석(價値分析 — value analysis) 수업 모형 공동 저자 제럴드 R. 쿰스(Jerrold R. Coombs)·밀턴 뮤(Milton Meux)의 canonical thinker_id가 ES 인덱스에 미등록. 이들은 사상가(thinker)보다는 **도덕 교육 학자(교과교육학 범주)**이므로 ES 사상가형 인덱스 등록 여부는 관리자 판단 대상. 원문 판정은 가치분석 모형 trademark(6단계 절차: 가치 문제 확인·명료화 → 사실 수집 → 사실 진위 평가 → 관련성 명료화 → 잠정적 가치 결정 → 가치 원칙 수용 가능성 검토 + 4가지 시험: 새로운 사례·포섭 원칙·역할 교환·보편 결과)의 명백한 일치로 확정. 답: ㉠ **가치분석(價値分析)**.
- 후속 조치: 교과교육학 범주로 ES 비등록 유지 가능. 만일 등록한다면 raths(가치명료화)·coombs_meux(가치분석)을 병치하여 도덕 교육 수업 모형 계열을 구성할 수 있음. 관리자 판단.
- 영향: Q10 정답 "가치분석"은 6단계 절차·4가지 시험 trademark 3중 일치로 확정됨. 본 블로커는 observation 수준.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2017A-005): ... -->` (2017-A.md Q10 row에 인라인 삽입)

### BLK-175E-2018A-001 (TASK-175E-2018-A) — Q11 톰 리건(Tom Regan) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2018-A.md` Q11 row
- 심각도: blocker (ES 커버리지 누락)
- 사유: Q11 사상가 톰 리건(Tom Regan, 1938-2017)의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록. 『The Case for Animal Rights』(1983) trademark 3중 일치("타인의 평가·계약·합의에 의해 생기는 것이 아니라 자신이 삶의 주체임을 경험할 수 있는 존재들이 가지는 특별한 가치" = 내재적 가치[inherent value]의 정의 + "믿음·욕망·지각·기억·미래 의식·쾌락/고통·선호/복지 이익·욕구/목적 달성 행동능력·심리적 동일성·개별적 복지" = 삶의 주체[subject-of-a-life] 7가지 기준의 공식 열거 + "㉡ 삶의 주체인 개체를 어떻게 대우해야 하는가" = 존중의 원리[respect principle]·해악의 원리[harm principle] 전제 질문)로 판정 확실. 답 ㉠ = **내재적 가치(內在的 價値 — inherent value)**. 리건은 싱어(Peter Singer)의 공리주의적 동물해방론과 쌍벽을 이루는 **의무론적 동물권(deontological animal rights)** 대표자.
- 후속 조치: TASK-176 범위에서 regan 사상가 신규 등록 + claim 작성(내재적 가치·삶의 주체 7기준·존중의 원리·해악의 원리·의무론적 동물권·『The Case for Animal Rights』(1983)·싱어 공리주의적 동물해방론 비판·무조건적 의무·권리 행사자[moral agents]/권리 보유자[moral patients] 구분). 후보 id: `regan`. 응용윤리·환경윤리 단골 출제이므로 **최우선 등록 순위**.
- 영향: Q11 정답 ㉠ "내재적 가치"와 ㉡ 서술(존중의 원리·해악의 원리에 기반한 의무론적 대우)은 trademark 3중 일치로 확정됨.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2018-A): ... -->` (2018-A.md Q11 row에 인라인 삽입)

### BLK-175E-2018B-001 (TASK-175E-2018-B) — Q1 엘리엇 튜리엘(Elliot Turiel) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2018-B.md` Q1 row
- 심각도: blocker (ES 커버리지 누락)
- 사유: Q1 사상가 엘리엇 튜리엘(Elliot Turiel, b.1938)의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록. 『The Development of Social Knowledge』(1983) **사회인지 영역 이론(Social Cognitive Domain Theory)** trademark 3중 일치("타인에게 해를 입히거나 공정성을 해치는 상황 vs 의복·식사 엉뚱 행동 상황에 대한 아동·교사 반응 대조 실험" = 도덕 영역[moral domain] vs 인습 영역[conventional domain] 대조 실험 trademark + "아동들이 어른들의 가르침이나 지적이 없어도 타인에 대한 해·공정성 침해를 나쁘다고 판단" = 도덕 영역 판단의 내재적·보편적 특성 논증 + <보기> "복장·장신구·모자를 도덕적으로 올바르지 않다고 야단침" = 인습 영역을 도덕 영역으로 혼동[domain confusion]하는 교사 행동의 표준 비판 사례)로 판정 확실. 답: 빈칸 = **"서로 독립적이다(별개의 영역으로 발달)"** + <보기> 견해 = 선생님이 인습 영역 행동을 도덕 영역으로 혼동하여 부당한 도덕적 비난을 가함.
- 후속 조치: TASK-176 범위에서 turiel 사상가 신규 등록 + claim 작성(사회인지 영역 이론·도덕/인습/개인 영역·영역 구분·도메인 혼동·콜버그 단계론 보완·타인 복지/공정성/권리 침해·사회적 합의/임의적 관습). 후보 id: `turiel`. 2014-A 서술형1에서도 동일 사상가 등장 기록이 있으므로(BLK-175B-001의 서술형1 참조) **최우선 등록 순위**.
- 영향: Q1 정답 "서로 독립적이다(도메인 구분)"과 <보기> 선생님 견해(인습·도덕 혼동 비판)는 trademark 3중 일치로 확정됨.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2018-B): ... -->` (2018-B.md Q1 row에 인라인 삽입)

### BLK-175E-2019A-001 (TASK-175E-2019-A-T) — Q3 앨버트 반두라(Albert Bandura) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2019-A.md` Q3 row
- 심각도: blocker (ES 커버리지 누락 — Tester 재분류)
- 사유: Q3 row의 **유일·중심 사상가**인 앨버트 반두라(Albert Bandura, 1925-2021)의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록. 『Social Learning Theory』(1977) trademark 3중 일치(① "사회학습이론은 모델을 관찰하는 것만으로도 행동이 강화" = 반두라 사회학습이론 기본 명제 + ② "관찰자가 다른 사람의 행동이 강화되는 것을 봄으로써 관찰한 행동을 하려는 경향이 증가" = 대리 강화[vicarious reinforcement] 공식 정의, 『Social Foundations of Thought and Action』(1986) + ③ "교사를 도와준 학생이 긍정적 강화를 받을 때 목격 학생의 도덕적 행동 경향 증가" = 보보 인형 실험(Bobo doll experiment, 1961·1963) 응용 사례)로 판정 확실. 답 = **대리 강화(代理 強化 — vicarious reinforcement)**. 구조적으로 BLK-175E-2018B-001(Turiel) 패턴과 동일(row의 유일·중심 사상가 ES 미등록 + trademark 3중 일치로 정답 개념 확정 가능). Coder의 observation 처리는 2018-B 기준과 비일관적이므로 Tester가 blocker로 재분류.
- 후속 조치: TASK-176 범위에서 bandura 사상가 신규 등록 + claim 작성(사회학습이론·관찰학습·모델링·대리 강화/대리 처벌·자기효능감[self-efficacy]·상호결정론[reciprocal determinism]·보보 인형 실험·『Social Learning Theory』(1977)·『Social Foundations of Thought and Action』(1986)·도덕적 이탈[moral disengagement]·콜버그·레스트·길리건·나딩스와 함께 도덕성 발달 이론 보완). 후보 id: `bandura`. 도덕 심리학·도덕교육학 단골 출제이므로 **최우선 등록 순위**.
- 영향: Q3 정답 "대리 강화"는 trademark 3중 일치로 확정됨. Coder 작성 coverage/2019-A.md 본문 내용은 정확하나 severity 분류만 상향 필요.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2019-A): BLK-175E-2019A-001 -->` (2019-A.md Q3 row에 인라인 삽입 권고, Coder 후속 작업 범위)

### BLK-175E-2019A-002 (TASK-175E-2019-A-T) — Q10 을 공화주의(페팃·스키너) ES 미등록 (부분 blocker)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2019-A.md` Q10 row (을 sub-problem 한정)
- 심각도: blocker (ES 커버리지 누락 — 부분, 을 sub-problem 한정 / Tester 재분류)
- 사유: Q10 갑·을 구조에서 **을의 중심 이론가 2명(필립 페팃[Philip Pettit, 1945-] + 퀀틴 스키너[Quentin Skinner, 1940-])이 모두 ES 미등록**. 갑 홉스(hobbes)는 등록되어 있으므로 row 전체 blocker는 아니나, 을 sub-problem의 trademark 3중 일치(① "공화주의자가 생각하는 정치적 자유의 개념은 의사의 자율성이라는 민주주의적 자유 개념에 가깝지만, 양자가 동일한 것은 아니다" = 페팃 『Republicanism: A Theory of Freedom and Government』(1997) 공화주의 정치적 자유 대조 명제 + ② "법이 단순히 내 의사와 일치하기 때문이 아니라, 내가 강요받을 수 있는 끊임없는 위험성으로부터 나를 보호" = 페팃 **비지배 자유[freedom as non-domination]** 공식 정의, "자의적 간섭 위험 자체의 제거" trademark + ③ "법의 지배에 의한 보호 = 비지배의 법" = 스키너 『Liberty before Liberalism』(1998) 공화주의 자유론 trademark)의 **중심 사상가가 공백**이다. 답 = 갑 ㉠ 자유 = **소극적 자유(消極的 自由 — negative liberty, 법의 침묵에서의 자유)** / 을 이유 = **법(㉡)은 자의적 지배 가능성으로부터 시민을 보호하는 조건이므로 루카 시민은 콘스탄티노플 시민보다 더 자유로움(비지배 자유)**. Coder가 observation으로 처리한 것은 갑이 등록된 점을 감안했으나, 을 sub-problem의 정답 논리 전체가 페팃·스키너 trademark이므로 ES 커버리지 관점에서는 blocker 수준(부분).
- 후속 조치: TASK-176 범위에서 (1) **pettit** 사상가 신규 등록 + claim 작성(공화주의·비지배 자유[non-domination]·자의적 간섭·법의 지배·『Republicanism』(1997)·제3의 자유 개념·벌린의 소극적/적극적 자유 2분법 비판·키케로·마키아벨리·해링턴 공화주의 계승). 우선순위 "중간" → **"높음"** 상향 권고. (2) **skinner**(Quentin Skinner, 케임브리지 학파 지성사) 병행 등록 검토 — 공화주의 자유론 쌍벽 이론가. 도덕·윤리 claim 범위는 pettit보다 좁으나 "공화주의 자유"라는 단일 claim으로 2019-A Q10 과 같이 출제되는 경우가 있음.
- 영향: Q10 갑(홉스 소극적 자유) 정답·을 개념 자체(비지배 자유)는 trademark 3중 일치로 확정됨. Coder 작성 coverage/2019-A.md 본문 내용은 정확하나 severity 분류만 상향 필요.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2019-A): BLK-175E-2019A-002 (을 sub-problem 한정) -->` (2019-A.md Q10 row에 인라인 삽입 권고, Coder 후속 작업 범위)

### BLK-175E-2019B-001 (TASK-175E-2019-B) — Q3 피터 싱어(Peter Singer) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2019-B.md` Q3 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록)
- 사유: Q3 row의 **유일·중심 사상가**인 피터 싱어(Peter Singer, 1946- )의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록. 『동물 해방(Animal Liberation, 1975)』·『실천윤리학(Practical Ethics, 1979)』 trademark 3중 일치(① "인간이든 동물이든 관계없이 그 판단에 영향을 받는 모든 존재들의 동등한 이익에 동등한 비중" = 싱어 **이익평등고려 원칙[principle of equal consideration of interests]** 공식 정의 + ② "이익을 갖기 위한 전제조건인 ( ㉡ )의 능력" = 벤담 『도덕과 입법의 원리 서설』 각주 "문제는 그들이 고통을 겪을 수 있는가[Can they suffer?]"의 싱어 계승 = **쾌고감수능력[sentience]** + ③ "동물에 대한 차별을 '종차별주의'라고 비난" = 싱어 대중화 **종차별주의[speciesism]** trademark)로 판정 확실. 답 ㉠ = **이익평등고려(利益 平等 考慮) 원칙** / ㉡ = **쾌고감수능력(快苦 感受 能力 — sentience)**. 구조적으로 BLK-175E-2018A-001(Regan 내재적 가치)·BLK-175E-2018B-001(Turiel 사회인지 영역 이론)·BLK-175E-2019A-001(Bandura 대리 강화) 패턴과 동일(row의 유일·중심 사상가 ES 미등록 + trademark 3중 일치로 정답 개념 확정 가능).
- 후속 조치: TASK-176 범위에서 `singer` 사상가 신규 등록 + claim 작성(이익평등고려 원칙·쾌고감수능력·종차별주의·『동물해방』(1975)·『실천윤리학』(1979)·선호 공리주의·공장식 축산 반대·세계 빈곤 원조 의무·인격[person]과 생명[life] 구분·영아 살해 논쟁·효과적 이타주의[effective altruism]). 후보 id: `singer`. 응용윤리·동물윤리·공리주의 단골 출제이므로 **최우선 등록 순위**. 싱어와 쌍으로 자주 거론되는 리건(regan)은 BLK-175E-2018A-001에서 이미 등록 권고되었으므로 **환경·동물 윤리학자 묶음 등록** 권고(singer + regan + 레오폴드[leopold] + 폴 테일러[taylor_p] + 요나스[jonas]).
- 영향: Q3 정답 ㉠ "이익평등고려 원칙" + ㉡ "쾌고감수능력" + 공장식 축산 반대 이유(종차별주의 위배)는 trademark 3중 일치로 확정됨. coverage/2019-B.md 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2019-B): BLK-175E-2019B-001 -->` (2019-B.md Q3 row에 인라인 삽입 완료)

### BLK-175E-2019B-002 (TASK-175E-2019-B) — Q8 프로이드·호프만·블라지(Freud·Hoffman·Blasi) ES 미등록 (3인 묶음)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2019-B.md` Q8 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 3인 미등록, 묶음 처리)
- 사유: Q8 row에서 제시문에 직접 명기된 5인(콜버그·프로이드·호프만·레스트·블라지) 중 **3인(프로이드·호프만·블라지)의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록**. `kohlberg`·`rest`는 등록되어 있으나, 정서적 측면(㉠)·도덕 정체성 이론·4요소 모형 원저자의 ES 공백으로 Q8 10점 논술 전체 커버리지에 심각한 차질 발생. Trademark 3중 일치:<br>• **프로이드(Sigmund Freud, 1856-1939)**: ① 저자 직접 명기 "프로이드(S. Freud)"(원문 L114) + ② "도덕성의 정서적 측면"(L114 — **초자아[Über-Ich / superego]** + **동일시[identification]** + **죄책감[guilt]** 정신분석 도덕론 trademark) + ③ 콜버그 인지적 측면과의 대립 구조에서 정서·무의식·정신분석 대표자로 제시.<br>• **호프만(Martin L. Hoffman, 1924-2023)**: ① 저자 직접 명기 "호프만(M. L. Hoffman)"(원문 L114) + ② "도덕성의 정서적 측면"(L114 — 『Empathy and Moral Development』(2000) **공감(empathy)** 중심 도덕 발달 4단계[전체적 공감→자기중심적 공감→타인 감정 공감→타인 삶 조건 공감] + **공감적 고통[empathic distress]** + **귀납적 훈육[induction discipline]** trademark) + ③ 프로이드와 함께 정서 중심 도덕 심리학의 대표자.<br>• **블라지(Augusto Blasi, 1933-2015)**: ① 저자 직접 명기 "블라지(A. Blasi)"(원문 L116) + ② "도덕적 정체성 이론 … 도덕 판단과 행동 사이의 간극을 메우는 데 있어서 도덕적 정체성이 중요한 역할"(L116 — 블라지 **도덕적 정체성[moral identity]** + **도덕 판단-행동 간극[judgment-action gap]** trademark + **자기 일관성[self-consistency]** 동기 기제) + ③ "도덕적 이해, 도덕적 정체성, ( ㉢ ), 도덕적 동기화 네 가지"(L116 — 블라지 **도덕 행위 자기모형(self-model of moral action)** 4단계, ㉢ = **책임 판단[responsibility judgment]**). 답: ㉠ 프로이드 = 초자아·동일시·죄책감 / 호프만 = 공감·공감적 고통·귀납적 훈육 / ㉡ = **도덕적 품성(실행력 — moral character/implementation)** (레스트) / ㉢ = **책임 판단(責任 判斷 — responsibility judgment)** (블라지).
- 후속 조치: TASK-176 범위에서 3인 신규 등록 + claim 작성 — (1) `freud` : 초자아·이드/자아/초자아·오이디푸스 콤플렉스·엘렉트라 콤플렉스·동일시·죄책감·무의식·방어기제·정신분석·리비도·쾌락원칙/현실원칙·『꿈의 해석』·『쾌락원칙을 넘어서』·『문명 속의 불만』. 후보 id: `freud`. (2) `hoffman`: 공감 발달 4단계·공감적 고통·자기중심적 공감·귀납적 훈육·사랑의 철회[love withdrawal] 비판·권력적 주장[power assertion] 비판·도덕 내면화·친사회적 행동·『Empathy and Moral Development』(2000). 후보 id: `hoffman`. (3) `blasi`: 도덕적 정체성·책임 판단·자기 일관성·도덕 판단-행동 간극·도덕적 자기 이론·도덕적 품성·도덕 심리학·『Moral character: A psychological approach』(2005)·콜버그 신콜버그주의 비판. 후보 id: `blasi`. 도덕 심리학·도덕 교육 단골 출제(레스트·블라지는 교과교육학 필수 범위)이므로 **우선 순위 높음**.
- 영향: Q8 정답 ㉡ "도덕적 품성(실행력)" + ㉢ "책임 판단" + ㉠ 프로이드·호프만 입장 서술은 trademark 3중 일치로 확정됨. coverage/2019-B.md Q8 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2019-B): BLK-175E-2019B-002 -->` (2019-B.md Q8 row에 인라인 삽입 완료)

### BLK-175E-2020A-001 (TASK-175E-2020-A) — Q3 보조국사 지눌(普照國師 知訥) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2020-A.md` Q3 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록)
- 사유: Q3 row의 **유일·중심 사상가**인 보조국사 지눌(普照國師 知訥, 1158-1210)의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록. 『수심결(修心訣)』·『정혜결사문(定慧結社文)』·『법집별행록절요병입사기(法集別行錄節要幷入私記)』 trademark 3중 일치(① "돈문(頓門)·점문(漸門) + 근기(根機)의 우열 + '(     )정혜' vs '수상정혜(隨相定慧)'"(원문 L38-L40) = 지눌의 돈오점수·자성정혜/수상정혜 이중 수행 체계 trademark + ② "팔풍·삼수·혼침·산란·선정·천진 + '고요하되 신령한 앎이 항상 존재'"(L38-L40) = 지눌 **공적영지(空寂靈知 — "空寂靈知 自是我本來面目")** 명제 trademark + ③ "심성(心性) 본래 깨끗 + 번뇌 본래 공 + 점문의 오염된 수행에 떨어지지 않음"(L40) = 지눌 **심성본정·번뇌본공·돈오점수** 체계 trademark)로 판정 확실. 답: 빈칸 = **자성(自性)[정혜]** (자성정혜 — 본성 그대로의 선정과 지혜). 한국 불교 조계종 중흥조이며, 원효·혜능과 함께 한국 불교 3대 출제 인물로 도덕·윤리 기출에 고빈도 등장.
- 후속 조치: TASK-176 범위에서 `jinul` 신규 등록 + claim 작성(돈오점수·정혜쌍수·자성정혜·수상정혜·공적영지·심성본정·번뇌본공·『수심결』·『정혜결사문』·『법집별행록절요병입사기』·조계종·돈문/점문 병용·근기론·영지[靈知]·공적[空寂]·6조 혜능 계승·북종 신수와의 대조). 후보 id: `jinul`. 등록 우선순위 **최우선**.
- 영향: Q3 정답 "자성(自性)[정혜]"은 trademark 3중 일치로 확정됨. coverage/2020-A.md Q3 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2020-A): BLK-175E-2020A-001 -->` (2020-A.md Q3 row에 인라인 삽입 완료)

### BLK-175E-2020A-002 (TASK-175E-2020-A) — Q7 앨버트 반두라(Albert Bandura) ES 미등록 (재발)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2020-A.md` Q7 row
- 심각도: blocker (ES 커버리지 누락 — 재발, BLK-175E-2019A-001 중복)
- 사유: Q7 row의 **유일·중심 사상가**인 앨버트 반두라(Albert Bandura, 1925-2021)의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록. 저자 직접 명기("반두라(A. Bandura)의 '도덕적 이탈' 기제" — 원문 L84) + **도덕적 이탈 8기제 공식 도식** 완전 재현(L88-L96 — 비난 받을 만한 행위: 도덕적 정당화/완곡한 명칭 사용/유리한 비교 + 해로운 결과: 결과의 축소·무시·왜곡 + 피해자: 비인간화/비난(책임)의 귀속 + 중앙 흐름 하부 박스: 책임의 전가/책임의 분산) = 반두라 1991 "Social cognitive theory of moral thought and action" Table 1, 1999 "Moral disengagement in the perpetration of inhumanities" Figure 1, 2016 『Moral Disengagement: How People Do Harm and Live with Themselves』의 구조 완전 일치 trademark. 답: ㉠ = **완곡한 명칭 사용(婉曲한 名稱 使用 — euphemistic labeling)** / ㉡ = **유리한 비교(有利한 比較 — advantageous comparison)** / ㉢ = **비인간화(非人間化 — dehumanization)** + 예시(르완다 '바퀴벌레'·홀로코스트 '해충'·학교 따돌림 '벌레'). **선행 블로커 BLK-175E-2019A-001(2019-A Q3 대리 강화) 재발** — 반두라가 2019-A·2020-A 두 해 연속 출제에도 ES 미등록 유지 중이므로 등록 우선순위 더욱 상향.
- 후속 조치: TASK-176 범위에서 `bandura` 신규 등록 + claim 작성(사회인지이론[social cognitive theory]·자기효능감[self-efficacy]·관찰 학습[observational learning]·모델링·대리 강화/대리 처벌·상호결정론[reciprocal determinism]·보보 인형 실험(1961·1963)·도덕적 이탈(moral disengagement) 8기제·자기 제재[self-sanction]·『Social Learning Theory』(1977)·『Social Foundations of Thought and Action』(1986)·『Moral Disengagement』(2016)). 후보 id: `bandura`. 등록 우선순위 **최우선**(재발).
- 영향: Q7 정답 ㉠·㉡·㉢ 모두 trademark 3중 일치로 확정됨. coverage/2020-A.md Q7 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2020-A): BLK-175E-2020A-002 -->` (2020-A.md Q7 row에 인라인 삽입 완료)

### BLK-175E-2020A-003 (TASK-175E-2020-A) — Q10 페팃·스키너·벌린(Pettit·Skinner·Berlin) ES 미등록 (3인 묶음, 부분 재발)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2020-A.md` Q10 row
- 심각도: blocker (ES 커버리지 누락 — 부분, 3인 묶음 / 페팃·스키너는 BLK-175E-2019A-002 재발 + 벌린 신규)
- 사유: Q10 row에서 제시문 ㉡(공화주의 사상가들)·㉢(자유주의 사상가들)의 **핵심 이론가 3인(필립 페팃[Philip Pettit, 1945-] + 퀀틴 스키너[Quentin Skinner, 1940-] + 이사야 벌린[Isaiah Berlin, 1909-1997])의 canonical thinker_id가 모두 ES 미등록**. 홉스(hobbes)는 소극적 자유 계보 배경으로 등록되어 있으나, 본 문항의 공화주의 vs 자유주의 현대 정식화자 3인의 ES 공백으로 Q10 4점 서술 전체 커버리지에 차질 발생. Trademark 3중 일치:<br>• **페팃(Philip Pettit)**: "공화국 + 시민적 덕(㉠) = 공공선 봉사 + 시민적 우애"(원문 L139 — 『Republicanism』(1997) 7장 "Civic Virtue") + "㉡(공화주의) = 주종적 지배·예속 자체 부재 + 간섭 부재를 넘어섬"(L140) = 페팃 **비지배 자유(freedom as non-domination)** 공식 정의 trademark + "㉣ 법 제재 두려움 없이 자의적 의지에 종속되지 않음" = 페팃 **자의적 지배(arbitrary domination) 부재** 정식화.<br>• **스키너(Quentin Skinner)**: 『Liberty before Liberalism』(1998)·케임브리지 학파 지성사·신로마 공화주의 자유론. 페팃과 쌍으로 공화주의 비지배 자유를 정식화.<br>• **벌린(Isaiah Berlin)**: "㉢(자유주의) = 개인이 다른 개인·기관으로부터 간섭을 받지 않는 데 그침"(L140) = 벌린 「Two Concepts of Liberty」(1958) **소극적 자유(negative liberty, freedom as non-interference)** 정의 trademark("the area within which a man can act unobstructed by others"). 답: ㉠ = **덕(德) — 시민적 덕성(市民的 德性 — civic virtue)** / ㉣ 찬성(공화주의): 법은 자의적 지배 가능성을 제거하여 비지배 자유를 실현하는 수단 / ㉣ 반대(자유주의): 법 자체가 간섭이므로 법 제재가 있으면 자유 축소(홉스 『리바이어던』 21장 "자유 = 외적 방해 부재" / 벤담 "모든 법은 자유의 제한").
- 후속 조치: TASK-176 범위에서 3인 신규 등록 + claim 작성 — (1) `pettit`: 공화주의·비지배 자유[non-domination]·자의적 간섭·법의 지배·『Republicanism』(1997)·제3의 자유 개념·벌린 소극적/적극적 자유 2분법 비판·키케로·마키아벨리·해링턴 공화주의 계승·민주적 통제[democratic control]·심의민주주의. (2) `skinner`: 케임브리지 지성사·『Liberty before Liberalism』(1998)·신로마 공화주의·홉스·마키아벨리 연구·방법론(Meaning and Understanding in the History of Ideas)·담론 전환. (3) `berlin`: 자유주의·소극적/적극적 자유 2분법·「Two Concepts of Liberty」(1958)·가치 다원주의(value pluralism)·역사주의 비판·소련 공산주의 비판·낭만주의 지성사·『Four Essays on Liberty』. 후보 id: `pettit`·`skinner`·`berlin`. 등록 우선순위 **최우선(재발)**.
- 영향: Q10 정답 ㉠(덕/시민적 덕성) + ㉣ 찬반 논리는 trademark 3중 일치로 확정됨. 선행 블로커 BLK-175E-2019A-002 중복(페팃·스키너)이 2020-A에서 재발하였으므로 등록 지연 비용이 누적되고 있음.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2020-A): BLK-175E-2020A-003 -->` (2020-A.md Q10 row에 인라인 삽입 완료)

### BLK-175E-2020A-004 (TASK-175E-2020-A) — Q12 고봉 기대승(高峯 奇大升) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2020-A.md` Q12 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록)
- 사유: Q12 row의 **을 사상가**인 고봉 기대승(高峯 奇大升, 1527-1572)의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록. 갑 퇴계 이황(yihwang)은 등록되어 있으나, 사단칠정 논쟁의 **다른 한 축 전체**가 ES 공백으로 Q12 4점 서술의 대조 구조에 차질 발생. Trademark 3중 일치: ① "사람의 성(性)에는 인의예지신(仁義禮智信) 다섯 가지 뿐 + 다섯 외에 다른 성 없음"(원문 L165) = 기대승 **오성(五性)으로만 구성된 성 체계** trademark(유가 정통 성론, 별도의 "사단의 성" 부정) + ② "정(情)에는 희노애구애오욕(喜怒哀懼愛惡欲) 일곱 가지 뿐 + 일곱 외에 다른 정 없음"(L165) = 기대승 **칠정(七情)이 정의 전체** trademark(『예기』 예운편 칠정을 정의 전체로 삼는 정론) + ③ "( ㉠ 사단 ) = 선한 정의 **별칭(別稱)에 불과** + ( ㉡ 칠정 )을 언급하면 ( ㉠ )은 이미 그 가운데 들어 있음"(L165) = 기대승 **칠정포사단설(七情包四端說)·사단재칠정중(四端在七情中)** trademark(『고봉답퇴계논사단칠정서(高峯答退溪論四端七情書)』·『사칠리기왕복서(四七理氣往復書)』의 핵심 명제: "四端 非七情之外 別有四端. 但就七情中 就其善一邊 別而名之曰 四端")로 판정 확실. 답: ㉠ = **사단(四端)** / ㉡ = **칠정(七情)**. 갑(퇴계) = 이기호발설(사단 이발기수·칠정 기발리승) / 을(기대승) = 기발리승 일도·칠정포사단(사단은 칠정 중 선한 측면의 별칭). 기대승은 퇴계와 8년간(1559-1566) 서신 교환으로 사단칠정 논쟁을 전개한 조선 성리학 대논쟁의 핵심 파트너이며, 후일 율곡의 기발이승일도설(氣發理乘一途說)의 직접 선구. 도덕·윤리 기출 필수 출제 인물.
- 후속 조치: TASK-176 범위에서 `gidaeseung` 신규 등록 + claim 작성(사단칠정 논쟁·칠정포사단설·사단재칠정중·기발리승 일원론·오성(인의예지신)·칠정(희노애구애오욕)·선일변·중절·퇴계 이기호발설 비판·율곡 기발이승일도의 선구·『고봉답퇴계논사단칠정서』·『사칠리기왕복서』·『양선생왕복서』·호남 성리학). 후보 id: `gidaeseung`(또는 `kidaesung`). 등록 우선순위 **최우선**(퇴계 파트너로서 사단칠정 논쟁 완결성 확보).
- 영향: Q12 정답 ㉠(사단)·㉡(칠정) + 갑·을 발현 주장(이·기 활용) 모두 trademark 3중 일치로 확정됨. coverage/2020-A.md Q12 본문 내용은 정확하며 ES 커버리지 공백만 존재(퇴계 단독 등록 상태).
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2020-A): BLK-175E-2020A-004 -->` (2020-A.md Q12 row에 인라인 삽입 완료)

### BLK-175E-2020B-001 (TASK-175E-2020-B) — Q1 마르틴 하이데거(Martin Heidegger) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2020-B.md` Q1 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 서양 현대 실존주의 단골 출제 인물)
- 사유: Q1 row의 **유일·중심 사상가**인 마르틴 하이데거(Martin Heidegger, 1889-1976)의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록. 원문(L14~L24)은 도덕 교사 갑과 서양 현대 윤리 사상가 을의 가상 대화로, 을이 ㉠("현존재 자신의 '가장 고유한' 가능성")과 ㉡("세계의 무의미성을 열어 보인다")을 설명하는 구조. Trademark 3중 일치: ① "현존재 자신의 '가장 고유한' 가능성"(L18, L20 — 『존재와 시간』 §50-§53의 현존재(Dasein)의 "가장 고유한(eigenste) 존재 가능성"으로서의 **죽음** 정의. 하이데거 죽음 분석의 정형구 "가장 고유한·무연관적·뛰어넘을 수 없는 가능성"); ② "일상적인 가능성의 허망함을 드러내면서 그것들을 무(無)로 떨어뜨리는 극단적인 가능성 … 실존의 전체성과 통일성 … 현존재의 최고 심급"(L20 — 『존재와 시간』 §53 **죽음을 향한 선구(Vorlaufen zum Tode / anticipation of death)** 분석. 죽음은 현존재의 모든 가능성을 전체성[Ganzheit]으로 묶어 본래성[Eigentlichkeit]을 개시); ③ "세계의 무의미성을 열어 보인다 … 나의 심연으로부터 치밀어 올라와 나를 송두리째 사로잡으면서 '내가 아무런 이유도 근거도 없이 이렇게 존재한다'라는 적나라한 사실 앞에 세웁니다. … 유일무이한 존재와 만나게 됩니다"(L22, L24 — 『존재와 시간』 §40 **불안(Angst / anxiety)** 분석 완전 일치. 불안은 대상 없는 근본기분[Grundstimmung]이며 피투성[Geworfenheit]과 단독자로서의 실존을 드러냄 — 특정 존재자를 향한 공포[Furcht]와 대조). 답: ㉠ = **죽음(Tod) / 죽음을 향한 존재(Sein zum Tode)** / ㉡ = **불안(Angst)**.
- 후속 조치: TASK-176 범위에서 `heidegger` 신규 등록 + claim 작성 — 현존재(Dasein)·세계-내-존재(In-der-Welt-sein)·죽음으로의 선구(Vorlaufen zum Tode)·불안(Angst)·본래성/비본래성(Eigentlichkeit/Uneigentlichkeit)·세인(das Man)·피투성(Geworfenheit)·기투(Entwurf)·염려(Sorge)·시간성(Zeitlichkeit)·존재론적 차이(ontologische Differenz)·근본기분(Grundstimmung)·『존재와 시간』(1927)·『형이상학이란 무엇인가』(1929)·후기 언어 사유("언어는 존재의 집")·기술 비판(『기술에 대한 물음』)·사물(Ding)·휴머니즘 서한(1947)·니체 해석. 후보 id: `heidegger`. 등록 우선순위 **최우선**(서양 현대 실존주의 단골 출제, 사르트르[sartre]와 쌍으로 출제 빈도 높음).
- 영향: Q1 정답 ㉠(죽음)·㉡(불안)은 trademark 3중 일치로 확정됨. coverage/2020-B.md Q1 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2020-B): BLK-175E-2020B-001 -->` (2020-B.md Q1 row에 인라인 삽입 완료)

### BLK-175E-2020B-002 (TASK-175E-2020-B) — Q6 프로타고라스(Protagoras of Abdera) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2020-B.md` Q6 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 (가) 중심 사상가 미등록, 서양 고대 소피스트 단골 출제)
- 사유: Q6 (가) 제시문 중심 사상가 프로타고라스(Protagoras of Abdera, 기원전 c.490-c.420)의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록. (나)의 Plato는 `plato`로 등록되어 있으나 (가)의 소피스트 프로타고라스 공백으로 Q6 4점 서술(프로타고라스의 덕 교수 가능론 vs 플라톤의 덕 통일성 테제 대조)의 한쪽 축이 ES 커버리지 부재. Trademark 3중 일치: ① "훌륭함은 선천적으로 있게 된 것도 아니며 … 가르쳐질 수도 있으며 … 훌륭함은 가르쳐질 수 있다는 것을 … 아테네인들도 그리 믿고 있다"(L95 — 플라톤 대화편 『프로타고라스(Protagoras)』 319a-328d 프로타고라스 **대연설[great speech]**의 직접 인용. **아레테(ἀρετή — excellence) 가르침 가능성 논증** trademark); ② "지혜, 절제, 용기, 정의, 그리고 경건함은 모두 훌륭함의 부분들이다. 이것들 중 넷은 서로 상당히 비슷하지만, ( ㉠ )은/는 이것들 모두와 아주 다르다"(L96 — 『프로타고라스』 329c-332a 프로타고라스의 **덕의 부분들(parts of virtue)** 이론. 지혜·절제·용기·정의·경건 5부분을 제시하고 그 중 **용기(andreia)**가 다른 넷과 매우 다르다고 주장. 소크라테스의 덕 통일성[unity of virtue] 테제와의 대립 구도); ③ 위 두 주장의 논리적 결합(덕은 가르쳐지며, 덕의 부분들은 서로 다르다)이 플라톤 『프로타고라스』의 **소크라테스 반박 구도**의 출발점 — 소크라테스는 "덕이 가르쳐질 수 있다면 지식이며, 지식은 하나이므로 모든 덕이 하나로 귀결된다"고 논증해 프로타고라스의 두 주장의 자기모순을 드러냄. 답: ㉠ = **용기(andreia)** / ㉡ = **두려워해야 할 것과 두려워하지 말아야 할 것(ta deina, 플라톤 『국가』 제4권 429c 용기 정의의 대상)**.
- 후속 조치: TASK-176 범위에서 `protagoras` 신규 등록 + claim 작성 — 고대 그리스 소피스트 제1인자·"인간은 만물의 척도다(ἄνθρωπος μέτρον — Homo mensura)" 상대주의 명제·덕 가르침 가능론(teachability of virtue)·위대한 연설(great speech)·덕의 부분들(parts of virtue) 이론·안틸로기아(antilogic, 논쟁술)·수사학(rhetoric)·신에 대한 불가지론("신에 대하여 나는 그들이 있는지 없는지 알 수 없다")·프로메테우스 신화 해석(『프로타고라스』 320c-322d)·플라톤 『프로타고라스』에서 소크라테스의 대립자·플라톤 『테아이테토스』에서의 상대주의 비판 대상·아테네 체류 기간의 아레테 교수 사업·경험주의 인식론·법률·관습(nomos) 이해. 후보 id: `protagoras`. 등록 우선순위 **우선**(서양 고대 소피스트 대표자, 플라톤 대화편 복수 등장).
- 영향: Q6 정답 ㉠(용기)·㉡(두려워해야 할 것) + 플라톤이 프로타고라스의 주장에 드러낼 논리적 모순은 trademark 3중 일치로 확정됨. coverage/2020-B.md Q6 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2020-B): BLK-175E-2020B-002 -->` (2020-B.md Q6 row에 인라인 삽입 완료)

### BLK-175E-2020B-003 (TASK-175E-2020-B) — Q8 법장(法藏, Fazang) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2020-B.md` Q8 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 (가)·(나) 중심 사상가 미등록, 중국 화엄종 교판 정립자)
- 사유: Q8 (가) 중국 불교 사상가 주장 + (나) 화엄 5교 교판 도표의 중심 사상가 법장(法藏, Fazang, 현수 賢首 국사, 643-712)의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록. 한국 불교 wonhyo(원효)·중국 선종 huineng(혜능)은 등록되어 있으나 중국 화엄종 제3조이자 5교판(華嚴五敎判)·사법계설 체계를 정립한 법장의 공백으로 Q8 4점 서술의 사상가 귀속 및 ES 커버리지 부재. Trademark 3중 일치: ① "대승종교(大乘終敎)에 의하면 … 이사융통(理事融通) … 『대승기신론』에서 '불생불멸이 생멸과 화합하여 같지도 않고[不一] 다르지도 않으니[不異], 이것을 ( ㉠ )(이)라고 이름 한다'"(L124 — 『대승기신론』 심생멸문의 **아뢰야식(阿賴耶識 / 阿梨耶識 — ālaya-vijñāna)** 정의. 원문: "所謂不生不滅 與生滅和合, 非一非異, 名爲阿梨耶識". 법장이 『대승기신론의기(大乘起信論義記)』에서 이를 대승종교의 핵심 의리로 주해한 구조 완전 일치. 빈칸 ㉠ = 아뢰야식); ② "화엄 5교판 도표(소승교/대승시교 상공/대승종교/돈교/원교 동별) × 사법계(사·이·이사무애·사사무애)"(L126-L136 — 법장 대표작 **『화엄오교장(華嚴五敎章, 또는 華嚴一乘敎義分齊章)』**의 5교판 체계 완전 재현. 제3단계 대승종교=**여래장 사상**=이사무애법계. 빈칸 ㉡ = 여래장, 빈칸 ㉢ = 이사무애); ③ "이사융통(理事融通) … 진여(眞如)가 훈습(熏習)을 따르고 화합"(L124 — 법장 화엄 교학의 **이사무애·이사융통** trademark. 진여[理]와 생멸[事]이 아뢰야식 안에서 불일불이[不一不異]로 융통함이 곧 이사무애). 답: ㉠ = **아뢰야식(阿賴耶識)** / ㉡ = **여래장(如來藏)** / ㉢ = **이사무애(理事無碍)**.
- 후속 조치: TASK-176 범위에서 `fazang` 신규 등록 + claim 작성 — 중국 화엄종 제3조(두순→지엄→법장→징관→종밀)·『화엄오교장(華嚴一乘敎義分齊章)』·**5교판**(소승/대승시교[상시교 유식·공시교 중관]/대승종교/돈교/원교[동교 천태·별교 화엄])·**사법계설**(사법계·이법계·이사무애법계·사사무애법계)·『금사자장(金師子章 — Essay on the Golden Lion)』(측천무후 앞 화엄 교설)·**십현문(十玄門)**·**육상원융(六相圓融)**·**상즉상입(相卽相入, interpenetration)**·일즉다다즉일(一卽多多卽一)·여래장·아뢰야식·『대승기신론의기(大乘起信論義記)』·성기(性起) 사상·별교일승(別敎一乘) vs 동교(同敎) 천태·측천무후 황실 후원·법상종(유식) 규기와의 교판 대립. 후보 id: `fazang` (또는 `beopjang` 한국 한자음 이체). 등록 우선순위 **우선**(동아시아 대승 불교 교판 체계화의 정점, 화엄 사상 단골 출제).
- 영향: Q8 정답 ㉠(아뢰야식)·㉡(여래장)·㉢(이사무애) 모두 trademark 3중 일치로 확정됨. coverage/2020-B.md Q8 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2020-B): BLK-175E-2020B-003 -->` (2020-B.md Q8 row에 인라인 삽입 완료)

### BLK-175E-2021A-001 (TASK-175E-2021-A) — Q3 조지 에드워드 무어(G. E. Moore) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2021-A.md` Q3 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 서양 현대 메타윤리학 비자연주의의 시조)
- 사유: Q3 row의 **유일·중심 사상가**인 조지 에드워드 무어(George Edward Moore, 1873-1958)의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록. 원문(L57~L60)은 윤리학 분류 + "열린 질문 논증[open-question argument]을 제시한 현대 비자연주의 이론가"를 직접 지시. Trademark 3중 일치: ① "윤리학의 한 분야로서, 윤리 일반 개념 등을 그 대상으로 삼아 '선한', '올바른' 등의 의미를 탐구"(L59 — **메타윤리학(meta-ethics / 상위 윤리학 / 분석 윤리학)**의 표준 정의. 무어 『윤리학 원리(Principia Ethica, 1903)』가 창시한 현대 메타윤리학의 trademark 과제); ② "비자연주의 이론에 따르면, 선함, 올바름 등의 도덕적 성질은 고유한 종류이어서 쾌락의 증대 등 계산 가능한 ( ㉡ ) 성질로 환원될 수 없다"(L60 — 무어 『Principia Ethica』 §§10-14의 **자연주의적 오류[自然主義的 誤謬 — naturalistic fallacy]** trademark 논증. 선(good)은 비자연적·단순(simple)·정의 불가능한(indefinable) 속성이며, 쾌락·욕망·진화 적응도 등 **자연적(natural)** 속성으로 환원하는 시도는 모두 자연주의적 오류에 빠진다는 명제); ③ "**열린 질문 논증**을 제시한 현대 비자연주의 이론가 … '선한', '올바른' 등의 표현을 '쾌락을 증대하는' 등의 ( ㉡ ) 표현으로 정의하려는 시도는 예외 없이 모두 오류를 범한다"(L60 — 『Principia Ethica』 §13의 **열린 질문 논증[open-question argument]** 공식 정의 및 무어 본인 명시. 어떤 자연적 속성 N(예: 쾌락 증대)에 대해 "N인 것은 과연 선한가?"라는 질문이 여전히 **열려 있는(open)** 의미 있는 질문이라면, '선함 = N'이라는 정의는 실패. 따라서 선은 자연적 속성으로 정의 불가). 답: ㉠ = **메타윤리학(상위 윤리학 / 분석 윤리학 / 메타 윤리 / 메타 윤리학)** / ㉡ = **자연적(自然的 — natural)** (자연적 성질·자연적 표현, 자연주의적 환원의 대상).
- 후속 조치: TASK-176 범위에서 `moore` 신규 등록 + claim 작성 — 『Principia Ethica(1903, 윤리학 원리)』·메타윤리학(meta-ethics)의 창시·비자연주의(non-naturalism, ethical non-naturalism)·**자연주의적 오류(naturalistic fallacy)**·**열린 질문 논증(open-question argument)**·선(the good)의 단순성·정의 불가능성(indefinability of good)·비자연적·비경험적 속성으로서의 선·직관주의(intuitionism, 프리차드[Prichard]·로스[Ross]와의 관계)·『Ethics(1912)』·분석철학(케임브리지 학파, 러셀·비트겐슈타인과의 관계)·상식 옹호(defense of common sense)·블룸즈버리 그룹(Bloomsbury Group)과의 영향·『일부 철학적 문제들(Some Main Problems of Philosophy, 1953)』. 후보 id: `moore`. 등록 우선순위 **우선**(메타윤리학 표준 교과서 단골 출제, 특히 열린 질문 논증·자연주의적 오류는 메타윤리 파트에서 필수 서술 테마).
- 영향: Q3 정답 ㉠(메타윤리학)·㉡(자연적)은 trademark 3중 일치로 확정됨. coverage/2021-A.md Q3 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2021-A): BLK-175E-2021A-001 -->` (2021-A.md Q3 row에 인라인 삽입 완료)

### BLK-175E-2021A-002 (TASK-175E-2021-A) — Q6 갑 오거스토 블라지(A. Blasi) ES 미등록 (재발)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2021-A.md` Q6 row (갑 sub-problem 한정)
- 심각도: blocker (ES 커버리지 누락 — 제시문 갑 중심 사상가 미등록, 선례 BLK-175E-2019B-002에서 이미 등록 권고된 인물의 재출제)
- 사유: Q6 (갑) sub-problem의 중심 사상가 오거스토 블라지(Augusto Blasi, 1935-2016)의 canonical thinker_id가 ES 미등록. 을(콜버그, `kohlberg` 등록)과 쌍으로 출제된 문항이나 갑의 ES 커버리지 공백으로 도덕 심리학 비교 서술의 한쪽 축이 부재. Trademark 3중 일치: ① "'자신이 어떤 종류의 사람이 되기를 원하는지', '자신이 어떤 종류의 사람이 되어야만 하는지'에 대한 ㉠ 도덕적 이해와 도덕적 자아 구성의 기회를 제공"(L101 — 블라지 **도덕적 자아 모형(moral self model)** · **자아 중심 도덕성(self model of moral functioning)**의 표준 정의. 블라지 『Moral character: A psychological approach』(2005)·"Moral functioning: Moral understanding and personality"(2004)의 trademark 명제: 도덕 행동의 동기는 '내가 어떤 종류의 사람인가'라는 자아 정체성 질문에서 나온다); ② "㉡ 특정한 도덕적 가치를 자아의 본질과 핵심으로 여기고 그것에 전념하고 헌신하는 자아감"(L101 — **도덕적 정체성(moral identity, 道德的 整體性)** 공식 정의. 블라지가 1980년대 이후 일관되게 제시한 개념: 도덕적 가치가 자아의 핵심(core)에 통합되어 자기 규정의 근간이 된 상태); ③ "자신의 자아감과 일치되게 행동하려는 강한 책임감 … 도덕 행동의 가장 중요한 원천"(L101 — 블라지의 **자기 일관성(self-consistency) 동기** + **책임 판단(judgment of responsibility)**. 도덕 판단과 도덕 행동 사이의 간극[judgment-action gap]을 메우는 매개 기제로 도덕적 정체성 + 자기 일관성 욕구 + 책임 판단을 제시). 을 trademark 확인: "도덕 판단은 … 행동이 옳은지 또는 의무인지 … ㉢ 도덕적으로 선하거나 옳은 것이 자신에게 어느 정도로 필수적인지에 대한 판단"(L103 — 콜버그(L. Kohlberg) 후기 『Essays on Moral Development Vol.2』(1984)의 **의무 판단(deontic judgment) vs 책임 판단(judgment of responsibility)** 구분. 콜버그는 1984년 논문에서 도덕 판단을 의무 판단(옳음·의무에 대한 판단)과 **책임 판단(개인이 그 옳은 행동을 자신에게 얼마나 필수적으로 요구하는가)**으로 구분하고, 후자만이 실제 도덕 행동을 유발한다고 주장). 답: ㉡ = **도덕적 정체성(道德的 整體性 — moral identity)** / ㉢ = **책임 판단(責任 判斷 — judgment of responsibility)**.
- 후속 조치: TASK-176 범위에서 `blasi` 신규 등록 + claim 작성 — **도덕적 정체성(moral identity)**·**도덕적 자아 모형(moral self model)**·**책임 판단(judgment of responsibility)**·**자기 일관성(self-consistency)** 동기·**도덕 판단-행동 간극(judgment-action gap)** 해명·도덕 행위 4요소(도덕적 이해·도덕적 정체성·책임 판단·도덕적 동기화)·자기 모형(self-model of moral action)·『Moral character: A psychological approach』(2005)·"Moral functioning: Moral understanding and personality"(2004)·콜버그 후기와의 접점(책임 판단 개념 공유)·키블리(Kibble)·로렌스·나바에즈와의 도덕 심리학 공동 프로젝트. 후보 id: `blasi`. **BLK-175E-2019B-002와 중복 권고** — 2019-B Q8에서도 동일 인물 blocker 등록되었고, 본 2021-A Q6에서 재출제되어 동일성·중요성 재확인. 등록 우선순위 **최우선**(도덕 심리학 단골 출제, 2개 연도 연속 출제 = Phase 6 범위 내 반복 출제 인물 상위).
- 영향: Q6 정답 ㉡(도덕적 정체성)·㉢(책임 판단) + 서술형(갑·을의 도덕 행동 동기 공통점·차이점)은 trademark 3중 일치로 확정됨. coverage/2021-A.md Q6 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2021-A): BLK-175E-2021A-002 -->` (2021-A.md Q6 row에 인라인 삽입 완료)

### BLK-175E-2021A-003 (TASK-175E-2021-A) — Q9 폴 W. 테일러(Paul W. Taylor) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2021-A.md` Q9 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 생명중심주의 환경윤리의 대표자)
- 사유: Q9 row의 **유일·중심 사상가**인 폴 W. 테일러(Paul W. Taylor, 1923-2015)의 canonical thinker_id가 ES 미등록. 기존 ES `taylor`는 **찰스 테일러(Charles Taylor, 공동체주의 정치철학자)**로 Paul Taylor와 별개 인물(동명이인 주의). Trademark 3중 일치: ① "생명체는 자신의 보존에 힘쓰고, 자기의 선을 실현하는 고유 방식을 지닌 ( ㉠ )이다. 생명체가 ( ㉠ )(이)라는 것은 그 내적 작동뿐 아니라 외적 활동 모두 **목표 지향적**이라는 것이다"(L142 — 폴 테일러 『자연에 대한 존중(Respect for Nature: A Theory of Environmental Ethics, 1986)』의 trademark 개념 **목적론적 삶의 중심(目的論的 삶의 中心 — teleological center of life)** 공식 정의. 모든 생명체는 자신의 선(good of its own)을 실현하려는 목적 지향적 활동의 고유한 중심이며, 이는 의식이나 욕구와 무관하게 생명 자체의 본질적 속성); ② "시간을 넘어 자신의 존재를 유지하고, 자기 종을 재생산하며 … 변화무쌍한 환경에서 사건 및 상황 등에 계속 적응"(L142 — 테일러 『Respect for Nature』 2장 **생명체의 자기 보존·자기 실현** 서술. 모든 생명체가 자신의 선을 추구하는 방식이 종(種)마다 고유하며, 이 고유한 실현 방식이 도덕적 존중의 근거); ③ "인간을 존중해야 하는 것과 마찬가지로 ㉡ 야생 생명체도 존중해야 한다 … 야생 생명체 자체에 대한 의무는 인간에 대한 도덕적 의무에 예속되거나 의존하지 않는다"(L143 — 테일러 『Respect for Nature』 3장 **생명중심주의(生命中心主義 — biocentrism, biocentric egalitarianism)** 핵심 명제: 모든 생명체는 **고유한 선(good of its own)**을 지니기에 **본래적 가치(inherent worth)**를 가지며, 인간의 이익에 종속되지 않는 도덕적 존중을 받을 자격이 있다. 테일러의 **생명중심적 전망(biocentric outlook)** 4신념: 지구 생명공동체의 일원으로서 인간, 모든 종의 상호 의존성, 목적론적 삶의 중심으로서의 개체, 인간 우월성 거부). 생태계 중심주의와의 비교: 테일러의 생명중심주의는 **개체(individual) 생명체** 각각의 본래적 가치와 존중을 강조하는 반면, **생태계 중심주의(ecocentrism, 레오폴드[Leopold] 대지윤리·네스[Næss] 심층생태학)**는 생명공동체·생태계·종·대지(land) 등 **전체론적(holistic)** 단위의 본래적 가치와 존중을 강조. 도덕적 지위의 확장 방향이 개체 vs 전체로 갈림. 답: ㉠ = **목적론적 삶의 중심(目的論的 삶의 中心 — teleological center of life, teleological-center-of-life)**.
- 후속 조치: TASK-176 범위에서 `taylor_p` 신규 등록 + claim 작성 — 『Respect for Nature: A Theory of Environmental Ethics(1986, 자연에 대한 존중)』·**생명중심주의(biocentrism, biocentric egalitarianism)**·**목적론적 삶의 중심(teleological center of life)**·**본래적 가치(inherent worth)**·**고유한 선(good of its own)**·**생명중심적 전망(biocentric outlook)** 4신념(지구 생명공동체의 일원·종 상호의존성·목적론적 삶의 중심·인간 우월성 거부)·모든 생명체의 도덕적 지위·의식·쾌고감수능력과 무관한 도덕 지위 근거·레이건(레건)·싱어 동물윤리와의 차이(개체주의 vs 개체주의지만 범위 확장)·생태계 중심주의(레오폴드 대지윤리·네스 심층생태학)와의 차이(개체 vs 전체론)·규범 윤리학으로서 환경윤리의 정당화·『Principles of Ethics(1975)』·『Normative Discourse(1961)』. 후보 id: `taylor_p` (기존 `taylor`=Charles Taylor와 충돌 회피). **중요: `taylor` id 충돌** — 본 프로젝트 ES의 `taylor`는 Charles Taylor(공동체주의)이므로 Paul Taylor는 반드시 `taylor_p`로 별도 등록해야 동명이인 오매핑을 방지할 수 있다. 등록 우선순위 **최우선**(환경윤리·생명윤리 단골 출제, 레건[regan]·싱어[singer]와 함께 동물·생명 윤리 3대 대표자).
- 영향: Q9 정답 ㉠(목적론적 삶의 중심) + 야생 생명체 존중 근거 + 생태계 중심주의와의 비교는 trademark 3중 일치로 확정됨. coverage/2021-A.md Q9 본문 내용은 정확하며 ES 커버리지 공백만 존재(동명이인 id 충돌 주의 사항 병기).
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2021-A): BLK-175E-2021A-003 -->` (2021-A.md Q9 row에 인라인 삽입 완료)

### BLK-175E-2021B-001 (TASK-175E-2021-B) — Q1 갑 대각국사 의천(Uicheon) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2021-B.md` Q1 row (갑 sub-problem)
- 심각도: blocker (ES 커버리지 누락 — 제시문 갑 중심 사상가 미등록, 고려 천태종 개창자·교종 개혁자)
- 사유: Q1 (갑) 제시문 중심 사상가 **대각국사 의천(大覺國師 義天, 1055-1101)**의 canonical thinker_id가 ES 미등록. 한국 불교 사상가 중 `wonhyo`(원효)만 등록된 상태로, 고려 중기 교·선 일치 운동의 핵심 인물 의천 공백이 Q1 2점 기입형의 갑 정답 귀속에 ES 커버리지 부재를 야기. Trademark 3중 일치: ① "부처가 입으로 말한 것이 교(敎)이고, 조사(祖師)가 마음으로 전한 것이 선(禪)이다. 부처와 조사의 마음과 입이 서로 어긋나지 않으니"(L18 — 의천의 **교·선 일치(敎禪一致) 이념** trademark. 의천이 송나라 유학(1085-1086) 후 고려로 돌아와 **천태종(天台宗)**을 개창하며 교종(화엄·천태·법상)과 선종(구산선문)의 대립을 해소한 핵심 원리); ② "근원을 찾지 않고 각자 익힌 바에 안주해서 망령되게 쟁론을 일으키며 헛되이 세월을 보내는가"(L18 — 의천의 **교관겸수(敎觀兼修 — 교학과 관행을 겸수함) / 내외겸전(內外兼全 — 내적 선정과 외적 교학을 모두 온전히 함)** trademark 비판. 『대각국사문집』에서 교종 내 종파 분열과 교·선 상호 배척을 비판); ③ 갑의 답 = **교관겸수(敎觀兼修)** — 의천의 고유 표어로서 교학(敎)과 관행(觀, 천태지관[天台止觀]의 관)의 겸수를 통해 원만한 깨달음에 이르는 수행관. 교과서 표준 역어: "교관겸수". 답: 갑 = **교관겸수(敎觀兼修)** / 을 = **정혜쌍수(定慧雙修)**.
- 후속 조치: TASK-176 범위에서 `uicheon` 신규 등록 + claim 작성 — **교관겸수(敎觀兼修)**·**내외겸전(內外兼全)**·**교선일치(敎禪一致)**·**천태종(天台宗)** 개창(1097, 국청사)·**신편제종교장총록(新編諸宗敎藏總錄)** 편찬·교장(敎藏) 대장경 주석 사업·송·요·일본 교류·화엄 교학 수용·『대각국사문집』·고려 문종 넷째 아들·고려 불교의 교종 개혁자·지눌의 선구(지눌 교외별전과 대조). 후보 id: `uicheon` (canonical 한국 이름 로마자 전사). 등록 우선순위 **우선**(한국 불교 고려 중기 교종 개혁·교선 일치론의 핵심 인물, 2021-B 기출 재출제).
- 영향: Q1 정답 갑 = **교관겸수**는 trademark 3중 일치로 확정됨. coverage/2021-B.md Q1 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2021-B): BLK-175E-2021B-001 -->` (2021-B.md Q1 row에 인라인 삽입 완료)

### BLK-175E-2021B-002 (TASK-175E-2021-B) — Q1 을 보조국사 지눌(Jinul/Chinul) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2021-B.md` Q1 row (을 sub-problem)
- 심각도: blocker (ES 커버리지 누락 — 제시문 을 중심 사상가 미등록, 고려 조계종 개창자·한국 선종 중흥조)
- 사유: Q1 (을) 제시문 중심 사상가 **보조국사 지눌(普照國師 知訥, 1158-1210)**의 canonical thinker_id가 ES 미등록. 2020-A Q1 선례 BLK-175E-2020A-001에서 동일 인물이 blocker 등록되었고, 본 2021-B Q1에서 재출제 — 한국 불교 출제 빈도 매우 높음. Trademark 3중 일치: ① "나의 스승은 다음과 같이 말하였다"(L20 — 지눌이 『권수정혜결사문(勸修定慧結社文)』·『법집별행록절요병입사기(法集別行錄節要并入私記)』에서 규봉 종밀(圭峰 宗密, 780-841) 등 중국 선사를 "나의 스승"으로 인용하는 **지눌의 trademark 어투**); ② "관(觀)을 배우지 않고 경전만을 공부하면 … 진리를 통찰하는 명상법은 잘 알지 못할 것 … 경전을 배우지 않고 관(觀)만 공부하면 … 윤회와 해탈의 인과에 대해서는 이해할 수 없을 것"(L20 — 지눌의 **정혜쌍수(定慧雙修 — concurrent cultivation of samādhi and prajñā)** trademark 논증. 정(定, 선정)과 혜(慧, 지혜)는 어느 한쪽만 닦으면 편벽하여 완전한 깨달음에 이르지 못하므로 둘을 함께 닦아야 한다); ③ 을의 답 = **정혜쌍수(定慧雙修)** — 지눌의 고유 수행관. 이는 **돈오점수(頓悟漸修 — sudden awakening followed by gradual cultivation)**의 전제가 되며, 지눌 조계 선종의 trademark. 답: 을 = **정혜쌍수**.
- 후속 조치: TASK-176 범위에서 `jinul` 신규 등록 + claim 작성 — **정혜쌍수(定慧雙修)**·**돈오점수(頓悟漸修)**·**정혜결사(定慧結社)**·**조계종(曹溪宗) 개창**·**간화결의론(看話決疑論)** (간화선 정립)·『권수정혜결사문(勸修定慧結社文, 1190)』·『수심결(修心訣)』·『법집별행록절요병입사기(法集別行錄節要并入私記, 1209)』·종밀(圭峰 宗密)의 영향·한국 선종 중흥조·삼문 체계(성적등지문·원돈신해문·경절문)·교선 일치 지향(의천과는 방향이 다른 선 중심 교선 일치). 후보 id: `jinul` (한국 불교 표준 로마자 전사, 또는 `chinul` 이체 표기도 있으나 McCune-Reischauer 이전 표기이므로 revised Romanization인 `jinul` 권장). 등록 우선순위 **최우선**(한국 불교 단골 출제, 2020-A·2021-B 2연도 이상 출제 가능성 높음).
- 영향: Q1 정답 을 = **정혜쌍수**는 trademark 3중 일치로 확정됨. coverage/2021-B.md Q1 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2021-B): BLK-175E-2021B-002 -->` (2021-B.md Q1 row에 인라인 삽입 완료)

### BLK-175E-2021B-003 (TASK-175E-2021-B) — Q3 갑 엘리엇 튜리엘(Elliot Turiel) ES 미등록 (재발)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2021-B.md` Q3 row (갑 sub-problem)
- 심각도: blocker (ES 커버리지 누락 — 제시문 갑 중심 사상가 미등록, 선례 BLK-175E-2018B-*에서 이미 등록 권고된 인물의 재출제)
- 사유: Q3 (갑) 제시문 중심 사상가 **엘리엇 튜리엘(Elliot Turiel, 1938~, UC Berkeley 발달심리학자)**의 canonical thinker_id가 ES 미등록. 2018-B Q10 선례에서 turiel 등록 권고가 이미 이루어졌으며, 본 2021-B Q3에서 재출제되어 동일 인물 중요성·출제 빈도 재확인. Trademark 3중 일치: ① "사람들은 **개인적 영역, 사회의 ( ㉠ ) 영역, 그리고 ㉡ 도덕적 영역**이라는 세 가지 영역에 대해 서로 다른 판단을 한다"(L37 — 튜리엘 **3영역 이론(three-domain theory / social cognitive domain theory)** trademark. 『사회적 지식의 발달(The Development of Social Knowledge: Morality and Convention, 1983)』에서 아동·청소년이 사회 세계를 도덕적·사회 관습적·개인적 3영역으로 질적으로 구분하여 다른 판단 기준을 적용함을 제시); ② "개인적 영역은 개인의 선호나 선택을 포함 … 사회의 ( ㉠ ) 영역은 사회적 조직화를 목표로 하는 규칙들로 구성 … 도덕적 영역은 모든 문화권에 보편적인 도덕 원리에 대한 개념을 포함"(L37 — 튜리엘 3영역 구분 기준 완전 일치. 도덕적 영역은 복지·공정성/정의 원리, 관습 영역은 사회 조직화 규칙, 개인 영역은 사적 재량·자율); ③ "통제가 심한 사회에서는 음악을 듣거나 춤을 추는 행위를 통제 … ㉢ 음악을 듣거나 춤을 추는 행위자는 이를 **부당하다**고 생각한다"(L37 — 튜리엘 **개인적 영역에 대한 관습의 침해 부당성** 테제. 튜리엘이 콜버그 단계 이론의 도덕·관습 혼합 비판에서 핵심으로 제시한 경험적 논거). 답: ㉠ = **관습(conventional, 사회 관습적 영역)** / ㉣ (을, 하이트) = **직관(intuition)**.
- 후속 조치: TASK-176 범위에서 `turiel` 신규 등록 + claim 작성 — **사회인지 영역이론(social cognitive domain theory)**·**3영역 모델(도덕적·사회 관습적·개인적)**·**도덕 영역 기준(복지·공정성/정의·보편성·비상대성·비권위의존성)**·**관습 영역의 조직 기능적·사회 상대적 특성**·**개인 영역의 자율·사적 재량**·**콜버그 단계 이론 비판(도덕·관습 혼합)**·**도덕 발달의 질적 차이**·『사회적 지식의 발달(The Development of Social Knowledge, 1983)』·『도덕성의 문화와 발달(The Culture of Morality, 2002)』·Smetana·Nucci와의 공동 연구·아동·청소년 영역 구분 능력 발달 연구. 후보 id: `turiel`. **BLK-175E-2018B-* 중복 권고 재확인** — 2018-B에서 등록 권고된 인물의 2021-B 재출제. 등록 우선순위 **최우선**(도덕 발달 심리학 단골 출제, 2연도 이상 출제로 확인됨).
- 영향: Q3 정답 ㉠ = **관습** + ㉡ 도덕적 영역의 2가지 도덕 원리(복지·공정성/정의) + ㉢ 부당 이유(도덕 원리 위반)는 trademark 3중 일치로 확정됨. coverage/2021-B.md Q3 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2021-B): BLK-175E-2021B-003 -->` (2021-B.md Q3 row에 인라인 삽입 완료)

### BLK-175E-2021B-004 (TASK-175E-2021-B) — Q4 갑 에밀 뒤르켐(Émile Durkheim) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2021-B.md` Q4 row (갑 sub-problem)
- 심각도: blocker (ES 커버리지 누락 — 제시문 갑 중심 사상가 미등록, 프랑스 사회학 창시자·도덕사회학의 정전)
- 사유: Q4 (갑) 제시문 중심 사상가 **에밀 뒤르켐(Émile Durkheim, 1858-1917)**의 canonical thinker_id가 ES 미등록. 뒤르켐은 프랑스 사회학 창시자이며 교과서 단골 출제 인물임에도 ES 인덱스 55명에 미등록 상태. Trademark 3중 일치: ① "도덕 교육의 목적은 학생들을 **도덕적으로 사회화**하는 것"(L52 — 뒤르켐 『도덕 교육론(L'Éducation morale, 1925 유작)』 trademark 명제. 도덕성을 **사회적 사실(fait social)**로 규정하며 교육 목적을 사회화(socialization)로 정의); ② "도덕적 사회화는 **규율을 존중**하고 **집단에 헌신**하는 것만으로는 충분하지 않다. 이성에 기초해서 행위의 이유를 분명하고 완전하게 깨달아야 한다"(L52 — 뒤르켐 **도덕성 3요소(three elements of morality)** trademark: ① 규율 정신(l'esprit de discipline), ② 사회 집단에의 애착(l'attachement aux groupes sociaux), ③ 의지의 자율성(l'autonomie de la volonté). 앞 두 요소만으로는 불충분하며 제3요소 자율성이 완성되어야 함); ③ "도덕 규칙을 **지적으로 이해**하고 그것을 따르기로 **동의하고 원함**으로써 행위의 ( ㉠ )을/를 확보"(L52 — 뒤르켐의 **자율성** 정의 — 칸트와 달리 **사회 규칙의 합리성을 이해·동의해 자기 의지로 따르는 상태**로 재해석). 답: ㉠ = **자율성(l'autonomie)**. 을(피아제)에서 자율성이 나타나는 단계 = **도덕 상대주의 단계(moral relativism / 자율적 도덕성, 10-11세 이후)**. 도덕 판단 특징 = 주관적 책임(의도 중심), 정의 판단 특징 = 평등→공정(equity)·상호성 기반 정의.
- 후속 조치: TASK-176 범위에서 `durkheim` 신규 등록 + claim 작성 — **사회적 사실(fait social)**·**도덕 교육 3요소(규율 정신·사회 집단에의 애착·의지의 자율성)**·**기계적 연대(solidarité mécanique)**·**유기적 연대(solidarité organique)**·**집합 의식(conscience collective)**·**아노미(anomie)**·**사회화(socialisation)**·**자살론(Le Suicide, 1897)**·**사회학적 방법의 규칙(Les Règles de la méthode sociologique, 1895)**·**종교 생활의 원초 형태(Les Formes élémentaires de la vie religieuse, 1912)**·**분업론(De la division du travail social, 1893)**·**도덕 교육론(L'Éducation morale, 1925 유작)**·칸트 자율 개념의 사회학적 재해석·콜버그 전구(사회적 측면)·뒤르켐 학파·『사회학 연보(L'Année sociologique)』. 후보 id: `durkheim`. 등록 우선순위 **최우선**(사회학 창시자, 도덕사회학·도덕 교육론 교과서 단골 출제).
- 영향: Q4 정답 ㉠ = **자율성** + ㉠이 나타나는 단계(도덕 상대주의/자율적 도덕성) + 도덕 판단·정의 판단의 특징은 trademark 3중 일치로 확정됨. coverage/2021-B.md Q4 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2021-B): BLK-175E-2021B-004 -->` (2021-B.md Q4 row에 인라인 삽입 완료)

### BLK-175E-2021B-005 (TASK-175E-2021-B) — Q5 을 마틴 호프만(Martin L. Hoffman) ES 미등록 (재발)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2021-B.md` Q5 row (을 sub-problem)
- 심각도: blocker (ES 커버리지 누락 — 제시문 을 중심 사상가 미등록, 선례 BLK-175E-2019B-*에서 이미 등록 권고된 인물의 재출제)
- 사유: Q5 (을) 제시문 중심 사상가 **마틴 호프만(Martin L. Hoffman, 1924~, 뉴욕대학 공감발달 심리학자)**의 canonical thinker_id가 ES 미등록. 2019-B Q7 선례에서 hoffman 등록 권고가 이미 이루어졌으며, 본 2021-B Q5에서 재출제되어 동일 인물 중요성·출제 빈도 재확인. Trademark 3중 일치: ① "**공감적 ( ㉠ )**은/는 ( ㉡ ) 발달에 의해 **중재**된다"(L68 — 호프만 **공감 각성(empathic arousal)의 발달 이론** trademark. 『공감과 도덕 발달(Empathy and Moral Development, 2000)』에서 공감 각성의 정서적 반응이 인지적 역할채택 능력의 발달에 의해 매개되어 점차 복잡·추상적 형태로 진화); ② "신생아와 영아는 자신과 다른 사람을 구별하지 못하기 때문에 다른 사람의 고통 반응을 자신의 고통으로 경험 … 유아는 자신과 다른 사람의 ( ㉠ ) 반응을 구별 … 아동은 다른 사람의 주관적 경험을 더 정확하게 추론"(L68 — 호프만의 **5단계 공감 발달 모형**(① 총체적 공감 global empathy 신생아 → ② 자기중심적 공감 egocentric empathy 1-2세 → ③ 타인의 감정에 대한 공감 empathy for another's feelings 2-3세 → ④ 타인의 삶의 조건에 대한 공감 empathy for another's life condition 아동기 후반~청소년기 → ⑤ 집단에 대한 공감 empathy for a distressed group)의 단계별 설명 완전 일치); ③ "청소년은 ( ㉡ ) 능력이 더 발달하게 되면서, 이제 **㉢ 더 다양한 대상의 고통을 느낄 수 있고, 그 대상이 속해 있는 다양한 상황과 조건을 볼 수 있다**"(L68 — 호프만 **4단계 타인의 삶의 조건에 대한 공감(empathy for another's life condition)**의 정식 정의. 청소년기에 자타를 지속적·역사적 정체성을 가진 개별자로 이해하고 타인의 전반적 삶 조건·역사·사회적 맥락에 대한 확장된 역할채택 능력으로 공감이 확장됨). 답: ㉠ = **정서(affect) / 공감적 각성(empathic arousal)** / ㉡ = **역할채택(role-taking / perspective-taking, 조망수용)** / ㉢ 단계 = **타인의 삶의 조건에 대한 공감** / 필요한 추론 능력 = **확장된 인지적 역할채택(타인의 삶의 조건·역사·사회적 맥락에 대한 역할채택)**.
- 후속 조치: TASK-176 범위에서 `hoffman` 신규 등록 + claim 작성 — **공감과 도덕 발달(Empathy and Moral Development: Implications for Caring and Justice, 2000)**·**공감 각성(empathic arousal)**·**공감적 고통(empathic distress)**·**5단계 공감 발달 모형**(총체적 공감·자기중심적 공감·타인의 감정에 대한 공감·타인의 삶의 조건에 대한 공감·집단에 대한 공감)·**역할채택(role-taking / perspective-taking)과 공감의 상호작용**·**귀납적 수양(inductive discipline) 양육 기법**·**동조 반응(mimicry)**·**조건화된 공감(classical conditioning empathy)**·**정의와 배려의 통합**·레스트(`rest`) 4구성요소 모델·셀먼(Selman) 역할채택 5단계와의 이론적 접점. 후보 id: `hoffman`. **BLK-175E-2019B-* 중복 권고 재확인** — 2019-B에서 등록 권고된 인물의 2021-B 재출제. 등록 우선순위 **최우선**(도덕 심리학·도덕 발달론 단골 출제, 2연도 이상 출제로 확인됨).
- 영향: Q5 정답 ㉠(정서/각성)·㉡(역할채택)·㉢ 단계(타인의 삶의 조건에 대한 공감)·필요한 추론 능력(확장된 인지적 역할채택)은 trademark 3중 일치로 확정됨. coverage/2021-B.md Q5 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2021-B): BLK-175E-2021B-005 -->` (2021-B.md Q5 row에 인라인 삽입 완료)

### BLK-175E-2021B-006 (TASK-175E-2021-B) — Q8 을 쇠렌 키르케고르(Søren Kierkegaard) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2021-B.md` Q8 row (을 sub-problem)
- 심각도: blocker (ES 커버리지 누락 — 제시문 을 중심 사상가 미등록, 덴마크 실존주의 선구자·유신론적 실존주의의 정전)
- 사유: Q8 (을) 제시문 중심 사상가 **쇠렌 키르케고르(Søren Kierkegaard, 1813-1855, 덴마크 실존주의 선구자)**의 canonical thinker_id가 ES 미등록. 갑(사르트르, `sartre` 등록)과 쌍으로 출제된 문항이나 을의 ES 커버리지 공백으로 실존주의 비교 서술(무신론적 vs 유신론적 실존주의)의 한쪽 축이 부재. 키르케고르는 야스퍼스·하이데거·사르트르 실존주의의 정신적 선조로서 교과서 단골 출제 인물. Trademark 3중 일치: ① "**진리는 ㉠ 주체성이다**"(L110 — 키르케고르 **『철학적 단편에 부치는 비학문적 해설의 후서(Afsluttende uvidenskabelig Efterskrift, 1846)』**의 trademark 제1명제. 덴마크어 원문: "Sandheden er Subjektiviteten". 객관적·체계적 진리(헤겔 철학)가 아닌 주체적·실존적 결단의 진리가 진짜 진리라는 선언); ② "'**죽음에 이르는 병**'이라는 개념은 … **가장 엄격한 의미에서 죽음에 이르는 병** … 이러한 병이야말로 분명하게 말해 ( ㉢ )"(L110 — 키르케고르 **『죽음에 이르는 병(Sygdommen til Døden, 1849)』** 제1부 제1장 완전 일치. 죽음에 이르는 병은 신앙의 대립인 **절망(Fortvivlelse / despair)**); ③ "**인간은 신 앞에 홀로 서서 그토록 큰 노력으로 그토록 큰 책임을 지면서 특정한 개별자가 되는 것**"(L110 — 키르케고르의 **단독자(Den Enkelte — the single individual) 앞에 선 신(face-to-face with God)** trademark. 『공포와 전율』의 아브라함이나 『죽음에 이르는 병』의 신앙인은 집단·보편에 의존하지 않고 단독자로서 신 앞에 직접 서서 절대적 책임을 지는 실존). 답: ㉡ = **휴머니즘(갑 사르트르)** / ㉢ = **절망(Fortvivlelse)**.
- 후속 조치: TASK-176 범위에서 `kierkegaard` 신규 등록 + claim 작성 — **주체성이 진리이다(Sandheden er Subjektiviteten)**·**3실존 단계(심미적→윤리적→종교적 / aesthetic→ethical→religious)**·**신 앞에 선 단독자(Den Enkelte / the single individual)**·**신앙의 도약(Troens Spring / leap of faith)**·**절망(Fortvivlelse / despair)**·**죽음에 이르는 병(Sygdommen til Døden, 1849)**·**공포와 전율(Frygt og Bæven, 1843, 아브라함의 이삭 번제)**·**이것이냐 저것이냐(Enten-Eller, 1843)**·**불안 개념(Begrebet Angest, 1844)**·**반복(Gjentagelsen, 1843)**·**철학적 단편에 부치는 비학문적 해설의 후서(Afsluttende uvidenskabelig Efterskrift, 1846)**·헤겔 체계 철학 비판·개별적 실존 강조·실존주의의 선구자·하이데거·야스퍼스·사르트르 실존주의의 정신적 원천·종교적 실존주의·덴마크 루터교 신학적 배경. 후보 id: `kierkegaard`. 등록 우선순위 **최우선**(서양 현대 실존주의 선구자, 사르트르[sartre 등록]·하이데거[미등록, BLK-175E-2020B-001]와 쌍으로 교과서 단골 출제, 유신론적 vs 무신론적 실존주의 비교 필수 인물).
- 영향: Q8 정답 ㉡(휴머니즘)·㉢(절망) + 갑·을 주체성 입장 차이점(신의 유무 + 자기 자신의 의미)은 trademark 3중 일치로 확정됨. coverage/2021-B.md Q8 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2021-B): BLK-175E-2021B-006 -->` (2021-B.md Q8 row에 인라인 삽입 완료)

### BLK-175E-2021B-007 (TASK-175E-2021-B) — Q10 마르쿠스 툴리우스 키케로(Marcus Tullius Cicero) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2021-B.md` Q10 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 유일·중심 사상가 미등록, 로마 공화국 정치사상·스토아 자연법 전통의 정전)
- 사유: Q10 row의 **유일·중심 사상가**인 **마르쿠스 툴리우스 키케로(Marcus Tullius Cicero, 기원전 106-43, 로마 공화국 말기 정치가·철학자·웅변가)**의 canonical thinker_id가 ES ethics-thinkers 인덱스(55명)에 미등록. 키케로는 서양 정치철학·법철학·수사학의 정전 인물로서 교과서 단골 출제(특히 자연법·공화주의·혼합정체론 파트). Trademark 3중 일치: ① "**공화국은 인민의 것이다 … 인민은 … ( ㉠ )와/과 ( ㉡ )을/를 인정하고 동의한 사람들의 모임**"(L136 — 키케로 **『국가론(De Re Publica, 기원전 54-51)』 제1권 25장 39절**의 **공화국 정의** trademark 완전 일치. 라틴어 원문: "Res publica res populi; populus autem non omnis hominum coetus quoquo modo congregatus, sed coetus multitudinis iuris consensu et utilitatis communione sociatus — 공화국은 인민의 것이며, 인민은 법[ius]에 대한 동의와 공동 이익[utilitas]의 공유에 의해 결속된 다수의 모임이다." 빈칸 ㉠ = **법(法 — ius)**, ㉡ = **이익(利益 — utilitas, 공동 이익)**); ② "**인간이 결합하는 첫 번째 이유는 … 인간의 자연스러운 어떤 것, 마치 군집성 같은 것**"(L136 — 키케로의 **자연적 사회성(natural sociability) / 인간의 자연적 군집성(appetitio societatis)** trademark. 아리스토텔레스의 정치적 동물(zoon politikon) 개념을 계승해 라틴 전통에 전수); ③ "**세 가지의 원초적인 국가의 종류보다 국가의 세 양식이 평균화되고 적절히 절제된 것 … 어떤 큰 동등함 … 왕에게서는 전제자, 귀족에서는 붕당, 인민에서는 소요와 혼란 … 원초적인 정치체제는 쉽게 정반대의 결함**"(L137 — 키케로 **『국가론』 제1권 42-45장의 3정체 쇠퇴 순환론 + 혼합정체(res publica mixta / constitutio mixta)** trademark 완전 일치. 폴리비오스(Polybius)의 6정체 순환론을 계승하며, 로마 공화국의 집정관·원로원·민회 3중 권력 분립을 최선의 혼합정체로 지목. 빈칸 ㉢ = **혼합정체**). 답: ㉠ = **법(ius)** / ㉡ = **이익(utilitas)** / ㉢ 정부 형태 = **혼합정체(mixed constitution)**. 특징 = 3정체 결합·상호 견제, 동등함·자유 유지, 정체 순환 정지·안정성.
- 후속 조치: TASK-176 범위에서 `cicero` 신규 등록 + claim 작성 — **국가론(De Re Publica, 기원전 54-51)**·**법률론(De Legibus)**·**의무론(De Officiis, 기원전 44, 스토아 의무론)**·**투스쿨룸 논변(Tusculanae Disputationes)**·**신들의 본성에 대하여(De Natura Deorum)**·**최고선악론(De Finibus Bonorum et Malorum)**·**공화국 정의**(law + common utility)·**자연법(lex naturae)** trademark ("참된 법은 바른 이성이고 자연과 일치하는 것")·**자연적 사회성(appetitio societatis)**·**정치적 동물(animal politicum)** 계승·**혼합정체(res publica mixta)**·**정체 순환론(anakyklōsis politeiōn)** 계승(폴리비오스 경유)·**집정관·원로원·민회 3중 권력 분립**·**스토아 철학의 로마 전승**·**라틴 산문 규범**·**카틸리나 탄핵 연설(Catilinarian Orations, 기원전 63)**·**필리피카이(Philippics, 안토니우스 탄핵)**·로크·몽테스키외·루소 공화주의 원천·토마스 아퀴나스 자연법 전통의 고대 원천. 후보 id: `cicero`. 등록 우선순위 **최우선**(서양 정치철학·법철학·자연법 전통의 고대 정전, 로크·루소·몽테스키외 공화주의의 뿌리, 교과서 단골 출제).
- 영향: Q10 정답 ㉠(법)·㉡(이익)·㉢ 혼합정체(정부 형태+특징)는 trademark 3중 일치로 확정됨. coverage/2021-B.md Q10 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2021-B): BLK-175E-2021B-007 -->` (2021-B.md Q10 row에 인라인 삽입 완료)

### BLK-175E-2022A-001 (TASK-175E-2022-A) — Q2 보조국사 지눌(普照國師 知訥) ES 미등록 (재발)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2022-A.md` Q2 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 유일·중심 사상가 미등록, 선례 BLK-175E-2020A-001·BLK-175E-2021B-002에서 이미 등록 권고된 인물의 3회 연속 재출제)
- 사유: Q2의 유일·중심 사상가 **보조국사 지눌(普照國師 知訥, 1158-1210)**의 canonical thinker_id가 ES 미등록. 2020-A Q1(BLK-175E-2020A-001), 2021-B Q1 을(BLK-175E-2021B-002)에 이어 **2022-A Q2에서 3연도 연속 재출제** 확인. 한국 불교 출제 최빈도 인물. Trademark 3중 일치: ① "진리에 들어가는 천 가지 문이 결국 선정과 지혜를 벗어나지 않는다. 그 요체는 자성(自性)의 본체와 작용 두 가지이니, ( ㉠ )이/가 바로 그것이다. 선정은 그 본체이고 지혜는 그 작용이다"(L28 — 지눌 『수심결(修心訣)』의 정혜체용(定慧體用) trademark. 『수심결』 원문: "諸入理之門 不出定慧 撮其要 卽自性上體用二義 前所謂空寂靈知是也 定是體 慧是用也"); ② "텅 비어 고요하면 항상 신령하게 알게 되고, 신령하게 알면 항상 텅 비어 고요하게 된다"(L28 — 지눌의 **공적영지(空寂靈知 — 텅 비어 고요하면서도 신령하게 앎)** trademark. 규봉 종밀(圭峰 宗密)의 영향을 받아 지눌이 한국 선종 핵심 개념으로 정립. 공적(空寂)과 영지(靈知)의 불이[不二] 관계 = 자성의 체용이 본래 하나); ③ "큰스님께서 '( ㉡ )에 산란함이 없는 것이 자성의 선정이요, ( ㉡ )이/가 어리석지 않은 것이 자성의 지혜이다.'라고 말한 것"(L28 — 지눌이 『수심결』에서 인용한 **육조 혜능(六祖 慧能)의 『육조단경(六祖壇經)』** 원문: "一念不亂 是自性定, 一念不愚 是自性慧也". 큰스님 = 육조 혜능. ( ㉡ ) = **한 생각[一念]**). 답: ㉠ = **공적영지(空寂靈知)** / ㉡ = **한 생각(一念)**.
- 후속 조치: TASK-176 범위에서 `jinul` 신규 등록 + claim 작성 — **정혜쌍수(定慧雙修)**·**돈오점수(頓悟漸修)**·**공적영지(空寂靈知)**·**정혜결사(定慧結社)**·**조계종(曹溪宗) 개창**·**간화결의론(看話決疑論)**·『권수정혜결사문(勸修定慧結社文, 1190)』·『수심결(修心訣)』·『법집별행록절요병입사기(法集別行錄節要并入私記, 1209)』·종밀(圭峰 宗密)의 영향·한국 선종 중흥조·삼문 체계(성적등지문·원돈신해문·경절문)·대혜종고(大慧宗杲) 간화선 수용. 후보 id: `jinul` (한국 revised Romanization). 등록 우선순위 **최최우선**(한국 불교 단골 출제, **2020-A·2021-B·2022-A 3연도 연속 재출제 확인** — 누적 재발로 인덱스 공백 심각).
- 영향: Q2 정답 ㉠(공적영지)·㉡(한 생각/一念)은 trademark 3중 일치로 확정됨. coverage/2022-A.md Q2 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2022-A): BLK-175E-2022A-001 -->` (2022-A.md Q2 row에 인라인 삽입 완료)

### BLK-175E-2022A-002 (TASK-175E-2022-A) — Q6 (가) 필립 페팃(Philip Pettit) ES 미등록 (재발)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2022-A.md` Q6 row ((가) sub-problem)
- 심각도: blocker (ES 커버리지 누락 — 제시문 (가) 중심 사상가 미등록, 선례 BLK-175E-2020A-003에서 이미 등록 권고된 인물의 재출제)
- 사유: Q6 (가) 제시문 중심 사상가 **필립 페팃(Philip Pettit, 1945~, 호주·미국 프린스턴 대학 정치철학자, 신공화주의 대표자)**의 canonical thinker_id가 ES 미등록. 2020-A Q10 선례(페팃·스키너·벌린 3인 묶음)에서 pettit 등록 권고가 이미 이루어졌으며, 본 2022-A Q6 (가)에서 재출제. Trademark 3중 일치: ① "우리가 진정으로 자유로워지려면 타인의 의지에 예속되지 않아야 한다"(L66 — 페팃 **비지배 자유(freedom as non-domination)** trademark 제1명제. 『공화주의: 자유와 정부에 관한 이론(Republicanism: A Theory of Freedom and Government, 1997)』 원문 명제: "To be free is not to be subject to another's arbitrary will"); ② "당신은 기본적인 자유라고 여겨지는 것을 주인에게 묻지 않고 스스로 행사할 수 있어야 한다"(L66 — 페팃의 **주인-노예 비유(master-slave metaphor)** trademark. "자비로운 주인[benevolent master]"의 노예도 주인의 의지에 예속되어 있으므로 자유가 아니라는 논증 — 벌린의 소극적 자유[비간섭]와 구별되는 공화주의적 자유[비지배]의 핵심 대비); ③ "공화주의 전통에서 발견되는 ( ㉠ )(이)란 시민적 권리를 온전히 향유할 수 있는 시민만이 누릴 수 있는 자유"(L66 — 페팃의 **시민적 자유(civic liberty) / 공화주의적 자유** trademark. 공화주의 전통의 시민만이 누리는 법적·제도적 보장 하의 자유 — 로마 공화국 → 마키아벨리 → 해링턴 → 신공화주의로 이어지는 정치사상사 계보에서 페팃이 체계화). 답: ㉠ = **비지배(non-domination) 자유** / (가)의 (나) ㉡ 비판 = ① 간섭[개입]을 자유의 본질적 침해로 보지 않아 국가의 예속적 간섭을 정당화·② 진정한 자아를 사회적 전체로 동일시해 개인의 자유 선택을 사회 전체에 종속시킴 (서술형 핵심).
- 후속 조치: TASK-176 범위에서 `pettit` 신규 등록 + claim 작성 — **비지배 자유(freedom as non-domination)**·**공화주의: 자유와 정부에 관한 이론(Republicanism, 1997)**·**공화주의적 이상(On the People's Terms, 2012)**·**주인-노예 비유(master-slave analogy)**·**자의적 간섭(arbitrary interference)**·**제어 가능성(control/contestability)**·**신공화주의(neo-republicanism)**·**벌린 소극적 자유 비판**·**퀜틴 스키너(Quentin Skinner)와 공동 연구**·**마키아벨리·해링턴·로마 공화국 전통 계승**·**심의 민주주의와 비지배**·**Pettit & Brennan 정치철학 공동 작업**. 후보 id: `pettit`. **BLK-175E-2020A-003 중복 권고 재확인** — 2020-A에서 등록 권고된 인물의 2022-A 재출제. 등록 우선순위 **최우선**(서양 현대 공화주의 대표 사상가, 2연도 이상 재출제 확인).
- 영향: Q6 정답 ㉠(비지배) + (가)의 (나) ㉡ 비판 2가지는 trademark 3중 일치로 확정됨. coverage/2022-A.md Q6 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2022-A): BLK-175E-2022A-002 -->` (2022-A.md Q6 row에 인라인 삽입 완료)

### BLK-175E-2022A-003 (TASK-175E-2022-A) — Q6 (나) 토머스 힐 그린(T.H. Green) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2022-A.md` Q6 row ((나) sub-problem)
- 심각도: blocker (ES 커버리지 누락 — 제시문 (나) 중심 사상가 미등록, 영국 관념론·적극적 자유 전통의 정전)
- 사유: Q6 (나) 제시문 중심 사상가 **토머스 힐 그린(Thomas Hill Green, 1836-1882, 옥스퍼드 영국 관념론 철학자·자유주의 이론가)**의 canonical thinker_id가 ES 미등록. 벌린(Isaiah Berlin)이 『자유의 두 개념(Two Concepts of Liberty, 1958)』에서 적극적 자유의 대표 사상가로 지목·비판한 인물로, 교과서 단골 출제. Trademark 3중 일치: ① "인간은 개성을 가진 하나의 인격체이기를 원하는 존재이다. 인간은 아무 의지가 없는 기계가 되어서는 안 된다"(L68 — 그린의 **자기실현(self-realization)** trademark. 『윤리학서설(Prolegomena to Ethics, 1883)』 원문 명제: 인간은 단순한 자연 존재가 아니라 **의식적이고 자기실현적인 인격체(self-conscious person)**로서 자기 자신이 되는 것을 추구); ② "( ㉡ )은/는 자신의 주인이 되기를 원하는 각 개체의 소원에 뿌리를 둔다"(L68 — 그린의 **적극적 자유(positive liberty)** 정의 trademark. 벌린이 『자유의 두 개념』에서 적극적 자유를 "자기 자신의 주인이 되기를 원하는 자[to be one's own master]"로 규정하며 그린·보샘켓·헤겔을 그 사상적 원천으로 지목. 원문 구절은 벌린 에세이의 적극적 자유 정의와 축자적으로 일치); ③ "개인이 예속적 상태에 빠져 스스로를 훈육하지 못한다면 국가가 대신해 주어야 한다 … 진정한 자아는 개인보다 좀 더 넓은 범위를 포괄하는 것이다. 즉, 자아란 일종의 사회적 전체로서 개인은 사회를 구성하는 하나의 요소이다"(L68 — 그린의 **공공선(common good) / 사회적 자아(social self)** trademark. 『정치적 의무의 원리에 대한 강의(Lectures on the Principles of Political Obligation, 1895)』에서 "자유는 선을 행할 적극적 힘"이며 국가는 시민이 자기실현 조건을 확보하도록 간섭·지원할 수 있다는 적극적 자유주의 확립. 벌린이 전체주의로 미끄러지는 위험을 경고한 핵심 사상가). 답: ㉡ = **적극적 자유(positive liberty)**.
- 후속 조치: TASK-176 범위에서 `green_th` 신규 등록 + claim 작성 (Charles Taylor의 `taylor`와 혼동 방지 위해 **성씨 약어 suffix `_th`** 적용 — architecture.md L491 규약에 따름). 주요 claim: **적극적 자유(positive liberty)**·**자기실현(self-realization)**·**공공선(common good)**·**사회적 자아(social self)**·**윤리학서설(Prolegomena to Ethics, 1883 유작)**·**정치적 의무의 원리에 대한 강의(Lectures on the Principles of Political Obligation, 1895 유작)**·**자유주의 법제의 자유주의적 입법(Liberal Legislation and Freedom of Contract, 1881)**·**영국 관념론(British Idealism) 대표**·**칸트·헤겔·아리스토텔레스 종합**·**뉴 자유주의(New Liberalism) 선구**·홉하우스·케인즈 복지국가 자유주의의 원천·벌린 소극적/적극적 자유 구분의 주요 비판 대상·보샘켓(Bernard Bosanquet)과 함께 헤겔주의 영국 수용의 주축. 후보 id: `green_th` (Thomas Hill Green; 일반 영단어 `green`·Charles Taylor의 `taylor`와의 혼동 방지 위해 성씨 + 이름 이니셜 suffix 권장). 등록 우선순위 **최우선**(서양 현대 자유주의 전통 핵심, 벌린 자유 이론과 쌍으로 교과서 단골 출제).
- 영향: Q6 정답 ㉡(적극적 자유) + (가)의 (나) ㉡ 비판 2가지는 trademark 3중 일치로 확정됨. coverage/2022-A.md Q6 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2022-A): BLK-175E-2022A-003 -->` (2022-A.md Q6 row에 인라인 삽입 완료)

### BLK-175E-2022A-004 (TASK-175E-2022-A) — Q8 을 엘리엇 튜리엘(Elliot Turiel) ES 미등록 (재발)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2022-A.md` Q8 row (을 sub-problem)
- 심각도: blocker (ES 커버리지 누락 — 제시문 을 중심 사상가 미등록, 선례 BLK-175E-2018B-*·BLK-175E-2021B-003에서 이미 등록 권고된 인물의 3회 연속 재출제)
- 사유: Q8 (을) 제시문 중심 사상가 **엘리엇 튜리엘(Elliot Turiel, 1938~, UC Berkeley 발달심리학자)**의 canonical thinker_id가 ES 미등록. 2018-B, 2021-B에 이어 **2022-A Q8에서 3연도 연속 재출제** 확인. Trademark 3중 일치: ① "아동은 이른 시기부터 사회적 지식의 영역을 구분한다. 그리고 아동은 사회적 지식의 각 영역에서 작동하는 규칙들, 곧 ㉡ 도덕 규칙의 특징과 ㉢ 인습적 규칙의 특징을 구분한다"(L95 — 튜리엘 **사회인지 영역이론(social cognitive domain theory)** trademark. 『사회적 지식의 발달(The Development of Social Knowledge: Morality and Convention, 1983)』에서 아동이 이른 시기부터 도덕적 영역과 사회 관습적 영역을 질적으로 구분함을 제시); ② "개인적 영역의 정당화 준거는 사적인 선호와 경향이다"(L95 — 튜리엘의 **3영역 구분(도덕적·사회 관습적·개인적)**의 개인 영역 정의. 개인적 영역은 사적 재량·취향·선호의 영역); ③ "모든 사건이나 상황의 영역이 분명하게 구별되지 않음으로 인해 ㉣ 영역 혼합, 2차적 현상, 문제의 애매성 등이 발생"(L95 — 튜리엘의 **영역 혼합(domain mixture) / 2차적 현상(second-order phenomena) / 영역 애매성(domain ambiguity)** trademark. Smetana·Nucci와의 공동 연구에서 정식화된 튜리엘 고유 용어들로, 현실의 도덕적 판단이 다중 영역 교차로 인해 단순 분류되지 않음을 설명). 답: ㉡ 도덕 규칙 특징 = 보편성·비상대성·비권위의존성·복지와 공정성 원리에 근거 / ㉢ 인습적 규칙 특징 = 사회 조직 의존성·권위·상대성·변경 가능성 / ㉤ B의 고민 원인(㉣ 영역 혼합 근거) = 도덕 영역(타인 복지 침해)과 인습·계약 영역(실험 역할 계약 준수)이 교차하여 영역 혼합·애매성 발생.
- 후속 조치: TASK-176 범위에서 `turiel` 신규 등록 + claim 작성 — **사회인지 영역이론(social cognitive domain theory)**·**3영역 모델(도덕적·사회 관습적·개인적)**·**도덕 영역 기준(복지·공정성/정의·보편성·비상대성·비권위의존성)**·**관습 영역의 조직 기능적·사회 상대적 특성**·**개인 영역의 자율·사적 재량**·**영역 혼합(domain mixture)**·**2차적 현상(second-order phenomena)**·**영역 애매성(domain ambiguity)**·**콜버그 단계 이론 비판(도덕·관습 혼합)**·**도덕 발달의 질적 차이**·『사회적 지식의 발달(The Development of Social Knowledge, 1983)』·『도덕성의 문화와 발달(The Culture of Morality, 2002)』·Smetana·Nucci와의 공동 연구·아동·청소년 영역 구분 능력 발달 연구. 후보 id: `turiel`. **BLK-175E-2018B-*·BLK-175E-2021B-003 중복 권고 재확인** — 2018-B·2021-B에서 등록 권고된 인물의 2022-A 3회 연속 재출제. 등록 우선순위 **최최우선**(도덕 발달 심리학 단골 출제, 3연도 이상 출제로 확인됨).
- 영향: Q8 정답 ㉡·㉢ 특징과 ㉤ 고민 원인(㉣ 영역 혼합 근거)은 trademark 3중 일치로 확정됨. coverage/2022-A.md Q8 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2022-A): BLK-175E-2022A-004 -->` (2022-A.md Q8 row에 인라인 삽입 완료)

### BLK-175E-2022A-005 (TASK-175E-2022-A) — Q10 (가) 갑 북종 신수(北宗 神秀) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2022-A.md` Q10 row ((가) 갑 sub-problem)
- 심각도: blocker (ES 커버리지 누락 — 제시문 (가) 갑 중심 사상가 미등록, 중국 선종 분파 중 북종선 개조)
- 사유: Q10 (가) 갑 제시문 중심 사상가 **북종 신수(北宗 神秀, 606?-706, 중국 당나라 선종 북종의 개조)**의 canonical thinker_id가 ES 미등록. 혜능(`huineng`)은 등록되어 있으나 그와 쌍으로 출제되는 신수가 공백으로, 남종·북종 대조 서술의 한 축이 부재. Trademark 3중 일치: ① "몸은 ( ㉠ )의 나무요 / 마음은 밝은 거울의 틀이니"(L129 — 신수의 **『육조단경(六祖壇經)』 제1편 「행유품」** 소재 **게송** trademark. 원문: "身是菩提樹 心如明鏡臺 時時勤拂拭 莫使惹塵埃"); ② "항상 부지런히 털어 내고 닦아서 / 먼지와 때가 끼지 않도록 하리"(L129 — 신수의 **점수선(漸修禪) / 북종선(北宗禪)** trademark. 마음을 거울에 비유해 끊임없이 번뇌의 먼지를 닦아 깨끗이 유지하는 **점수(漸修 — gradual cultivation)** 수행관. 오조 홍인(五祖 弘忍)의 수좌였으나 『단경』에서 혜능의 돈오 게송에 패배해 남종과 북종으로 분화); ③ (나) 오시팔교 분류 중 **화의사교(化儀四敎)의 '점(漸)'** = "단계를 밟아 점차적으로 설함"(L135 — 천태 지의의 팔교 분류에서 신수의 점수선에 대응되는 **점교(漸敎)**. 화의사교: 돈(頓)·점(漸)·비밀(秘密)·부정(不定)). 답: ㉠ = **보리(菩提)** / (나)에 근거한 갑의 주장 = **화의사교 중 '점(漸)' 혹은 '장(藏)'** (점차적 수행으로 깨달음에 이름 — 점수).
- 후속 조치: TASK-176 범위에서 `shenxiu` 신규 등록 + claim 작성 — **북종선(北宗禪)**·**점수선(漸修禪)**·**「身是菩提樹」 게송**·**오조 홍인(五祖 弘忍)의 수좌 제자**·**당 측천무후의 국사**·**『관심론(觀心論)』(의고전?)**·**『대승무생방편문(大乘無生方便門)』**·**혜능과의 북남 분화**·**혜능·신수 돈점 논쟁**·**화북 중원 선종 주류**·『육조단경』 제1편의 게송 대조 대상. 후보 id: `shenxiu` (중국 병음 Shénxiù). 등록 우선순위 **우선**(중국 선종 돈점 대조에서 혜능[huineng 등록]과 쌍으로 출제, 교과서 필수 대비 인물).
- 영향: Q10 정답 ㉠(보리) + 갑의 주장(점수/화의사교 점·장)은 trademark 3중 일치로 확정됨. coverage/2022-A.md Q10 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2022-A): BLK-175E-2022A-005 -->` (2022-A.md Q10 row에 인라인 삽입 완료)

### BLK-175E-2022A-006 (TASK-175E-2022-A) — Q10 (나) 천태 지의(天台 智顗) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2022-A.md` Q10 row ((나) sub-problem)
- 심각도: blocker (ES 커버리지 누락 — 제시문 (나) 중심 사상가 미등록, 중국 불교 천태종 개조·교판 분류의 정전)
- 사유: Q10 (나) 제시문 중심 사상가 **천태 지의(天台 智顗, 538-597, 수나라 승려·천태종 개조)**의 canonical thinker_id가 ES 미등록. 천태종 교판 체계(오시팔교)는 중국 불교 교학의 최고 체계로서 교과서 단골 출제. Trademark 3중 일치: ① "오시 | 화엄시·녹원시·( ㉡ )·반야시·법화열반시"(L133 — 천태 지의의 **오시(五時) 교판** trademark. 『묘법연화경현의(妙法蓮華經玄義)』·『법화문구(法華文句)』·『마하지관(摩訶止觀)』의 천태 3대부에서 석존 설법을 시간 순으로 5시기로 분류. 오시: 화엄시(華嚴時) → 녹원시(鹿苑時) → **방등시(方等時)** → 반야시(般若時) → 법화열반시(法華涅槃時)); ② "팔교 | **화법사교(化法四敎) / 장·통·별·원** + **화의사교(化儀四敎) / 돈·점·비밀·부정**"(L135 — 천태 지의의 **팔교(八敎) 교판** trademark. 화법사교(교리 내용 분류): 장(藏)·통(通)·별(別)·원(圓). 화의사교(교화 방법 분류): 돈(頓)·점(漸)·비밀(祕密)·부정(不定). 오시와 결합하여 **오시팔교(五時八敎)** 완성); ③ "아함경 이후, 8년간 대승경을 널리 고르게 설함"(L133 — 천태 지의의 **방등시(方等時)** 정의 완전 일치. '방등(方等)'은 '널리·고르게'의 의미로, 『유마경』·『승만경』·『능가경』 등 초기 대승경을 포함). 답: ㉡ = **방등시(方等時)** / 갑(신수)에 근거한 팔교 분류 = **화의사교 중 '점(漸)'** (점차적 수행·교화) / 을(혜능)에 근거한 팔교 분류 = **화의사교 중 '돈(頓)'** (단계를 넘어 한꺼번에 깨달음).
- 후속 조치: TASK-176 범위에서 `zhiyi` 신규 등록 + claim 작성 — **천태종(天台宗) 개조**·**오시팔교(五時八敎) 교판**·**오시(화엄시·녹원시·방등시·반야시·법화열반시)**·**팔교(화법사교 장·통·별·원 + 화의사교 돈·점·비밀·부정)**·**천태 3대부(『묘법연화경현의(妙法蓮華經玄義)』·『법화문구(法華文句)』·『마하지관(摩訶止觀)』)**·**일념삼천(一念三千)**·**삼제원융(三諦圓融 — 공·가·중)**·**지관(止觀) 수행**·**실상론(實相論)**·**개삼회일(開三會一 — 삼승을 개시하여 일승으로 귀결)**·수나라 양제의 지지·한국 천태종(의천 개창)·일본 천태종(사이초/最澄)·용수 중관 사상 수용·법화경 중심 교학. 후보 id: `zhiyi` (중국 병음 Zhìyǐ). 등록 우선순위 **우선**(중국 불교 교학 체계의 정점, 천태종 개조, 한국·일본 천태종 원천).
- 영향: Q10 정답 ㉡(방등시) + 갑·을 주장(화의사교 점·돈)은 trademark 3중 일치로 확정됨. coverage/2022-A.md Q10 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2022-A): BLK-175E-2022A-006 -->` (2022-A.md Q10 row에 인라인 삽입 완료)

### BLK-175E-2022A-007 (TASK-175E-2022-A) — Q11 병 체사레 베카리아(Cesare Beccaria) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2022-A.md` Q11 row (병 sub-problem)
- 심각도: blocker (ES 커버리지 누락 — 제시문 병 중심 사상가 미등록, 근대 형법학·사형제 반대론의 정전)
- 사유: Q11 (병) 제시문 중심 사상가 **체사레 베카리아(Cesare Beccaria, 1738-1794, 이탈리아 밀라노 계몽주의 법학자·경제학자)**의 canonical thinker_id가 ES 미등록. 사형제 반대론의 고전으로서 교과서 단골 출제(사형제 찬반 논쟁의 핵심 인물). Trademark 3중 일치: ① "우선, 형벌의 효용성에 근거한 입장이 있습니다"(L151 — 베카리아 **『범죄와 형벌(Dei delitti e delle pene, 1764)』** trademark 제1명제. 베카리아는 처벌의 정당성을 응보가 아닌 **공리주의적 효용성[utilità]**에서 도출 — 벤담 공리주의 형벌론의 선구); ② "이 입장은 범죄의 ( ㉡ )을/를 형벌의 정당한 근거로 주장합니다. 그러나 사형제가 미래의 살인에 대한 ( ㉡ )이/가 없다는 것은 문헌을 통해 증명되고 있습니다"(L151 — 베카리아의 **일반예방(general prevention) / 억지[deterrence]** trademark. 『범죄와 형벌』 제12장 "형벌의 목적": "형벌의 목적은 이미 범한 범죄를 되돌리는 것이 아니라 다른 사람이 새로운 범죄를 저지르는 것을 막는 것[억지]" + 제28장 "사형에 대하여": **사형보다 종신 노역형이 억지 효과가 더 크다**는 경험적 논거 제시); ③ "더구나 사형이 아닌 다른 종류의 처벌로도 형벌의 목적은 달성될 수 있습니다. 그 다음으로는 ㉢ 사형제를 시행하는 과정에서 심각한 부정의가 발생"(L151 — 베카리아의 **사형제 반대론** trademark. 『범죄와 형벌』 제28장: 사형은 ① 사회 계약에 의해 양도되지 않은 권리(생명권)의 침해, ② 일회성 강한 처벌보다 지속적 처벌이 더 억지력 있음, ③ 오심 시 회복 불가, ④ 사형 집행의 국가 폭력성이 시민의 폭력 감수성을 오히려 증가시킴 등 경험·공리 논거로 사형제를 반대). 답: ㉡ = **예방(prevention) / 억지력(deterrence)** / ㉢ 부정의 2가지 = ① 오심(judicial error)에 의한 무고한 사형 + ② 사법적 불평등(사형 선고의 계층·인종 편향) (혹은 ① 국가에 의한 생명권 침해 + ② 오심 회복 불가).
- 후속 조치: TASK-176 범위에서 `beccaria` 신규 등록 + claim 작성 — **『범죄와 형벌(Dei delitti e delle pene, 1764)』**·**사형제 반대론**·**공리주의적 형벌론**·**일반예방(general prevention) / 억지(deterrence)**·**비례의 원리(proportionality)**·**형벌의 신속성·확실성·필연성(celerity, certainty, necessity)**·**죄형법정주의(nullum crimen, nulla poena sine lege) 선구**·**고문 금지**·**밀라노 계몽주의(il caffè 동인)**·**베리 형제(Pietro·Alessandro Verri)와 교류**·**몽테스키외·루소·로크의 영향**·**벤담 공리주의 형법 이론의 직접적 선구**·**미국 헌법 8수정·유럽 형법 근대화의 원천**·**존 하워드 감옥 개혁 운동의 이론적 근거**. 후보 id: `beccaria`. 등록 우선순위 **최우선**(응용 윤리 사형제 찬반 논쟁의 고전, 교과서 단골 출제, 칸트[kant 등록]·벤담[bentham 등록]과 함께 3인 구도로 반복 출제).
- 영향: Q11 정답 ㉡(예방/억지력) + ㉢ 부정의 2가지는 trademark 3중 일치로 확정됨. coverage/2022-A.md Q11 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: `<!-- BLOCKER(TASK-175E-2022-A): BLK-175E-2022A-007 -->` (2022-A.md Q11 row에 인라인 삽입 완료)

### BLK-175E-2022B-001 (TASK-175E-2022-B) — Q1 칼 포퍼(Karl Popper) ES 미등록
- 심각도: blocker (ES 커버리지 누락 — 제시문 유일 사상가 미등록, 20세기 과학철학·정치철학 거장)
- 사유: Q1 (L14-L18) 제시문 **유일·중심 사상가**인 **칼 포퍼(Karl Popper, 1902-1994, 빈 출신 영국 과학철학자·정치철학자)**의 canonical thinker_id가 ES 미등록. `popper`·`karl_popper`·`popper_k` 모두 MISS. Trademark 3중 일치: ① "**비판적 합리주의**"(L18 직접 명기) — 포퍼의 **자기 명명(self-designated)** 철학 이름 trademark. 『추측과 논박(Conjectures and Refutations, 1963)』에서 자신의 입장을 "critical rationalism"으로 공식화; ② "**점진적 사회 공학**에 대한 정치적 요구"(L18 직접 명기) — 포퍼 『역사주의의 빈곤(The Poverty of Historicism, 1957)』 trademark 용어. 유토피아적 사회 공학(utopian social engineering) 대립 개념으로 **부분·점진·시행착오적 사회 개혁** 방법론; ③ "비판의 자유, 사상의 자유, 인간의 자유를 보호하는 사회 제도"(L18) — 포퍼 『열린 사회와 그 적들(The Open Society and Its Enemies, 1945)』의 **열린 사회(open society)** trademark. 답: ㉠ = **합리적 태도 / 지적 겸손 / 비판적 태도(批判的 態度)** — 포퍼의 "you may be right, I may be wrong" 태도. ㉡ = **오류(誤謬 — error)** — 포퍼의 **오류가능주의(fallibilism)** trademark.
- 후속 조치: TASK-176 범위에서 `popper` 신규 등록 + claim 작성 — **비판적 합리주의(critical rationalism)**·**반증가능성(falsifiability)**·**열린 사회(open society)**·**점진적 사회 공학(piecemeal social engineering)**·**역사주의 비판(critique of historicism)**·**오류가능주의(fallibilism)**·**객관적 지식(objective knowledge, World 3)**·**추측과 논박(conjectures and refutations)**·**『열린 사회와 그 적들(1945)』**·**『역사주의의 빈곤(1957)』**·**『추측과 논박(1963)』**·**『과학적 발견의 논리(The Logic of Scientific Discovery, 1934/1959)』**·빈학파·논리실증주의 비판(검증원리 대신 반증원리)·플라톤·헤겔·마르크스의 역사법칙주의 비판·자유민주주의·민주주의의 규범적 정당화(기술 선택지로서 비폭력적 정부 교체)·열린 사회 vs 닫힌 사회(부족 사회). 후보 id: `popper`. 등록 우선순위 **최우선**(정치철학·과학철학 거장, 교과서 단골 출제, 자유민주주의·점진적 개혁론의 이론가).
- 영향: Q1 정답 ㉠(지적 겸손/비판적 태도) · ㉡(오류)은 trademark 3중 일치로 확정됨. coverage/2022-B.md Q1 본문 내용은 정확하며 ES 커버리지 공백만 존재.
- coverage 파일 내 HTML 주석: 인라인 주석 미삽입 (본 섹션형 coverage 파일은 Q1 "ES 실존 여부" 항목에서 명시적으로 MISS 선언).

### BLK-175E-2022B-002 (TASK-175E-2022-B) — Q3 갑 에밀 뒤르켐(Émile Durkheim) ES 미등록 (재발)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, **2021-B→2022-B 2연속 재출제**)
- 사유: Q3 (L46-L52) **갑** 제시문 중심 사상가 **에밀 뒤르켐(Émile Durkheim, 1858-1917, 프랑스 사회학 창시자)**의 canonical thinker_id가 ES 미등록. BLK-175E-2021B-004에서 이미 등록 권고됨(2021-B Q4 갑 출제). 본 2022-B Q3 갑에서 재출제되어 **2연속 재출제** 확인 + 교과서 단골 인물 중요도 재확증. `durkheim`·`durkheim_e`·`emile_durkheim` 모두 MISS. Trademark 3중 일치: ① "도덕은 행위를 미리 정한 **규칙의 체계**로서 **사회에 의해 형성**"(L50) — 뒤르켐 『도덕 교육론(L'Éducation morale, 1925 유작)』 trademark. 도덕을 **사회적 사실(fait social)**로 규정하며 개인 외부의 **규칙 체계**이자 외재적 구속(contrainte extérieure); ② "학교는 학생들이 도덕규칙의 ( ㉠ )을/를 **존경**하며 … 교사는 **규율과 금지의 대변자, 본보기**로서 도덕적 ( ㉠ )"(L50) — 뒤르켐 **도덕성 3요소** trademark 중 첫째 **규율 정신(esprit de discipline)** — 규칙 자체에 내재한 **권위(authority)** 존경; ③ "도덕교육의 한 방법으로 **벌**을 적절하게 사용"(L50) — 뒤르켐 『도덕 교육론』에서 벌은 **범죄에 대한 사회적 비난의 상징적 표현** · **규칙의 신성성(sacred character of rule) 회복** 기능 trademark. 답: ㉠ = **권위(權威 — authority)**. 갑(뒤르켐)의 ㉡(벌) 본래적 역할 = 위반된 도덕규칙의 권위·신성성을 재확립하고 집단 양심(conscience collective)을 회복하는 상징적·사회적 기능. ㉠의 도덕교육적 한계(을=피아제 관점) = 아동을 **타율적 도덕성(moralité hétéronome)**에 고착시키고 자율적 도덕성·또래 협력·상호성 발달을 저해.
- 후속 조치: TASK-176 범위에서 `durkheim` 신규 등록 — **2연속 재출제 확증**되었으므로 **최우선 순위로 격상**. 요구 claim: **사회적 사실(fait social)**·**도덕 교육 3요소(규율 정신·집단에의 애착·의지의 자율성)**·**기계적 연대·유기적 연대**·**집합 의식(conscience collective)**·**아노미(anomie)**·**사회화(socialisation)**·**자살론(1897)**·**사회학적 방법의 규칙(1895)**·**종교 생활의 원초 형태(1912)**·**분업론(1893)**·**도덕 교육론(1925)**·칸트 자율 개념의 사회학적 재해석·콜버그·피아제 전구·뒤르켐 학파. 후보 id: `durkheim`. 등록 우선순위 **최우선** (2연속 재출제 확증).
- 영향: Q3 정답 ㉠(권위)·갑(뒤르켐)의 벌의 본래적 역할·ㅇ의 피아제 관점에서의 한계는 trademark 3중 일치로 확정됨. coverage/2022-B.md Q3 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2022B-003 (TASK-175E-2022-B) — Q7 갑 윌리엄 제임스(William James) ES 미등록
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 미국 실용주의 2세대 대표자)
- 사유: Q7 (L105-L111) **갑** 제시문 중심 사상가 **윌리엄 제임스(William James, 1842-1910, 미국 프래그머티즘·기능 심리학의 창시자)**의 canonical thinker_id가 ES 미등록. `james`·`william_james`·`james_w` 모두 MISS. **주의: ES에는 `rest`=James Rest(도덕심리학자)가 등록되어 있으나 이는 이름만 유사한 별개 인물**. Trademark 3중 일치: ① "**세계에 대한 진리는 완성된 것이 아니라 생겨나기도 하고 없어지기도 한다**"(L109) — 제임스 『실용주의(Pragmatism, 1907)』 강의6 원문: "Truth happens to an idea. It becomes true, is made true by events" trademark 완전 일치; ② "**새 진리는 낡은 진리에 의존하면서도 새 사실을 밝혀 낼 수 있다** … 새 관념은 진리의 계열 속에 끼어들어 형성"(L109) — 제임스의 **진리 누적·유기적 계승** trademark; ③ "진리를 **하나의 가설**에 불과한 것으로 간주 … **객관적 진리는 존재하지 않는다**"(L109) — 제임스의 **주관주의적(심리주의적) 진리관** trademark, "진리는 관념의 '작동하는(working)' 능력"(Pragmatism, 강의6). 답: ㉠ = **변화한다 / 생성된다 / 형성된다(變化/生成/形成)** — 제임스 진리관 핵심. 객관적 진리 부정 이유 = 진리는 인간의 과거·미래 연결 욕구(지향성)에 의해 끊임없이 생성·수정되며, 고정된 실재와의 일치가 아닌 경험의 만족적 연결이기 때문.
- 후속 조치: TASK-176 범위에서 `james` 신규 등록 + claim 작성 — **실용주의(pragmatism)**·**진리 생성론(truth happens)**·**의식의 흐름(stream of consciousness)**·**근본적 경험론(radical empiricism)**·**다원론적 우주(pluralistic universe)**·**종교적 경험의 다양성(The Varieties of Religious Experience, 1902)**·**『심리학의 원리(Principles of Psychology, 1890)』**·**『실용주의(Pragmatism, 1907)』**·**『진리의 의미(The Meaning of Truth, 1909)』**·**『근본적 경험론 논문집(Essays in Radical Empiricism, 1912)』**·찰스 퍼스 프래그머티즘 격률의 심리·형이상학적 확장·듀이 도구주의의 전구·제임스-듀이-퍼스 3인 실용주의 연쇄·기능 심리학·의지의 자유(will to believe)·종교적 믿음의 실용적 정당화. 후보 id: `james`. 등록 우선순위 **최우선**(실용주의 전통 교과서 단골 출제, 듀이[dewey 등록]와 쌍으로 반복 출제).
- 영향: Q7 정답 ㉠(변화/생성) · ㉢(객관적 진리 부정) · ㉡(지향성·욕구)과의 연계 논증은 trademark 3중 일치로 확정됨. coverage/2022-B.md Q7 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2022B-004 (TASK-175E-2022-B) — Q8 갑 마틴 호프만(Martin L. Hoffman) ES 미등록 (4연속 재발)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, **2016-A→2019-B→2021-B→2022-B 4연속 재출제 = 최최우선**)
- 사유: Q8 (L120-L126) **갑** 제시문 중심 사상가 **마틴 호프만(Martin L. Hoffman, 1924-2023, 미국 NYU 발달 심리학자·공감 발달론의 체계화)**의 canonical thinker_id가 ES 미등록. BLK-175E-2016A-005(2016-A Q10 을)·BLK-175E-2019B-002(2019-B Q8)·BLK-175E-2021B-005(2021-B Q5 을)에서 이미 3회 등록 권고됨. 본 2022-B Q8 갑에서 **4번째 출제 확증**. `hoffman`·`hoffman_m`·`martin_hoffman` 모두 MISS. Trademark 3중 일치: ① "공감은 **다섯 가지 다양한 방식**에 의해 발생 … 모방 … 고전적 조건화 … 직접적인 연상 … 역할채택"(L124) — 호프만 『공감과 도덕 발달(Empathy and Moral Development: Implications for Caring and Justice, 2000)』 제3장 **공감 각성의 5가지 양식(five modes of empathic arousal)** trademark: Motor mimicry(동작 모방) + afferent feedback, Classical conditioning(고전적 조건화), Direct association(직접적 연상), **Mediated association(언어적 매개 연상)**, Role-taking(역할채택). 완전 일치; ② "아동기에 … **모방, 조건화, 직접적인 연상** … **얼굴을 마주하는 상황**에서 결정적 … 일생 동안 **잠재적인 차원**에서 발생하는 공감의 토대"(L124) — 호프만의 **1~3양식 = 전언어적·자동적·저차 공감** vs **4~5양식 = 인지·언어 매개적·고차 공감** 구분 trademark; ③ "**역할채택에서는 피해자가 어떻게 느끼는지 혹은 피해자의 상황에서 자기가 어떻게 느낄 것인지를 상상**"(L124) — 호프만의 **역할채택 2하위 유형** (self-focused vs other-focused role-taking) trademark. 답: ㉢ = **언어적 매개 연상 / 매개된 연상(言語的 媒介 聯想 — verbally mediated association)**. ㉠(모방·조건화·직접적 연상)과 ㉡(언어적 매개 연상·역할채택)의 차이 = 전자는 **언어·인지·의식적 추론을 매개하지 않는 자동적·전언어적·저차 공감** (신체 모방·연합학습·지각-정서 회로에서 즉각 작동, 아동기·대면 상황·평생 잠재적 토대) / 후자는 **언어·상상·타인 조망 수용을 요구하는 고차 인지적 공감**.
- 후속 조치: TASK-176 범위에서 `hoffman` 신규 등록 — **4연속 재출제 확증**되었으므로 **최최우선 순위로 등록**. 요구 claim: **『공감과 도덕 발달(2000)』**·**공감 각성 5양식(모방·고전적 조건화·직접적 연상·언어적 매개 연상·역할채택)**·**공감 발달 5단계(총체적 공감·자기중심적 공감·타인의 감정에 대한 공감·타인의 삶의 조건에 대한 공감·집단에 대한 공감)**·**공감적 고통(empathic distress)**·**공감적 각성(empathic arousal)**·**귀납적 훈육(inductive discipline)**·**사랑의 철회 · 권력적 주장 양육법 비판**·**뜨거운 인지(hot cognition)**·**정의와 배려의 통합**·레스트(rest 등록) 4구성요소 모델·셀먼 역할채택 5단계와의 접점. 후보 id: `hoffman`. 등록 우선순위 **최최우선** (4연속 재출제 확증, 2000년대 이후 도덕심리학·도덕교육학 교과서에서 가장 빈번하게 출제되는 공감 발달론자).
- 영향: Q8 정답 ㉢(언어적 매개 연상) · ㉠과 ㉡의 구분 특징 · ㉤(배려받는 자의 응답 필요 이유, 나딩스)은 trademark 3중 일치로 확정됨. coverage/2022-B.md Q8 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2022B-005 (TASK-175E-2022-B) — Q9 갑 피터 싱어(Peter Singer) ES 미등록 (재발)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, **2019-B→2022-B 2연속 재출제**)
- 사유: Q9 (L135-L141) **갑** 제시문 중심 사상가 **피터 싱어(Peter Singer, 1946~, 오스트레일리아·프린스턴대 실천윤리·공리주의)**의 canonical thinker_id가 ES 미등록. BLK-175E-2019B-001에서 이미 등록 권고됨(2019-B Q3 동물해방 출제). 본 2022-B Q9 갑 해외 원조 문항에서 재출제 — **2연속 재출제 확증** + 싱어의 응용윤리 다주제(동물해방·해외원조) 출제 패턴 확인. `singer`·`peter_singer`·`psinger` 모두 MISS. Trademark 3중 일치: ① "**커다란 희생 없이 어려운 처지에 있는 사람을 도울 수 있다면 돕는 것이 우리의 의무**"(L139) — 싱어 『Famine, Affluence, and Morality(1972)』 trademark 원칙: "If it is in our power to prevent something bad from happening, without thereby sacrificing anything of comparable moral importance, we ought, morally, to do it"; ② "**모든 존재의 처지를 동등하게 고려해야 한다는 ( ㉠ ) 원칙**"(L139) — 싱어 『실천윤리학(Practical Ethics, 1979)』의 **이익평등고려 원칙(principle of equal consideration of interests)** trademark. 국적·인종·종·거리에 무관한 보편주의; ③ "**이웃의 어린아이인지, 아니면 다른 나라에 사는 어린아이인지는 나에게 도덕적 맥락에서 차이가 없다**"(L139) — 싱어의 **도덕적 거리 무차별(distance irrelevance)** + **익사하는 아이(drowning child) 사고 실험** trademark. 답: ㉠ = **이익평등고려 원칙(利益 平等 考慮 — equal consideration of interests)**.
- 후속 조치: TASK-176 범위에서 `singer` 신규 등록 — **2연속 재출제 확증**되었으므로 **최우선 순위로 격상**. 요구 claim: **이익평등고려 원칙(principle of equal consideration of interests)**·**종차별주의(speciesism)**·**쾌고감수능력(sentience)**·**선호 공리주의(preference utilitarianism)**·**효과적 이타주의(effective altruism)**·**『동물 해방(Animal Liberation, 1975)』**·**『실천윤리학(Practical Ethics, 1979)』**·**『Famine, Affluence, and Morality(1972)』**·**『The Life You Can Save(2009)』**·**공장식 축산 반대**·**해외 원조 의무**·**익사하는 아이 사고 실험**·**거리 무차별**·**인격(person)과 생명(life) 구분**·**영아 살해·안락사 논쟁**·헤어(R.M. Hare) 2층위 선호 공리주의의 계승·벤담·밀 공리주의의 확장. 후보 id: `singer`. 등록 우선순위 **최우선** (2연속 재출제 확증, 응용윤리 단골 출제 — 동물윤리·해외원조·생명윤리 3대 영역 모두에서 반복 출제).
- 영향: Q9 정답 ㉠(이익평등고려) · 을(롤즈)의 원조국·피원조국 조건은 trademark 3중 일치로 확정됨. coverage/2022-B.md Q9 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2023A-001 (TASK-175E-2023-A) — Q3 갑 알렉시스 드 토크빌(Alexis de Tocqueville) ES 미등록
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 서양 근대 자유주의·정치사회학 정전)
- 사유: Q3 (L46-L52) **갑** 제시문 중심 사상가 **알렉시스 드 토크빌(Alexis de Tocqueville, 1805-1859, 프랑스 자유주의 정치사상가·정치사회학자)**의 canonical thinker_id가 ES 미등록. `tocqueville`·`alexis_tocqueville`·`tocqueville_a` 모두 MISS. Trademark 3중 일치: ① "( ㉠ )와/과 **종교**는 모든 시민이 동일한 목표를 향해 부단히 나아가도록 만들 수 있는, 이 세상에 존재하는 **오직 두 개의 것**"(L50) — 토크빌 『미국의 민주주의(De la démocratie en Amérique, 1835/1840)』 제1권 제2부 제9장 "미국에서 종교가 정치사회에 끼치는 주요 영향" trademark 주장: **자유(liberté)와 종교(religion)가 민주주의를 유지시키는 두 기둥**; ② "법을 통해 사람의 생각, 열정, 일상적 **습관**과 연결될 경우 지속적이고 합리적인 감정으로 통합"(L50) — 토크빌의 **습속(mores, moeurs)** trademark. 『미국의 민주주의』는 민주주의 유지 조건을 지리·법률·습속 3축으로 분석하며 특히 습속이 법률보다 중요하다고 주장; ③ "사람의 마음에서 떠나지 않으며 … 지속적이고 합리적인 감정"(L50) — 토크빌이 자유를 단순한 제도적 권리가 아닌 **감정·습관·문화로 내면화된 덕성**으로 규정하는 trademark. 답: ㉠ = **자유(自由 — liberty)**.
- 후속 조치: TASK-176 범위에서 `tocqueville` 신규 등록 + claim 작성 — **『미국의 민주주의(1835/1840)』**·**『앙시앵 레짐과 혁명(L'Ancien Régime et la Révolution, 1856)』**·**자유(liberté)와 종교의 양립**·**평등(égalité)과 자유(liberté)의 긴장**·**다수의 폭정(tyrannie de la majorité)**·**습속(moeurs)의 중요성**·**결사(association)의 기예**·**민주적 개인주의(individualisme démocratique)의 위험**·**자율적 결사체와 시민 사회**·**지방분권(décentralisation)**·**민주주의 조건 3축(지리·법률·습속)**·**청교도 정신(pilgrim spirit)과 미국 민주주의 기원**·**연성 전제주의(despotisme doux)** 경고·밀 『자유론』에 미친 영향(다수의 폭정 개념)·19세기 프랑스 의회의원·알제리 식민 논쟁. 후보 id: `tocqueville`. 등록 우선순위 **최우선** (서양 사회사상사 정전, 교과서 빈번 출제 — 민주주의론·다수의 폭정·결사체의 기예).
- 영향: Q3 정답 ㉠(자유)은 trademark 3중 일치로 확정됨. coverage/2023-A.md Q3 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2023A-002 (TASK-175E-2023-A) — Q3 을 마우리치오 비롤리(Maurizio Viroli) ES 미등록
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 현대 공화주의 정치사상의 대표적 이론가)
- 사유: Q3 (L46-L52) **을** 제시문 중심 사상가 **마우리치오 비롤리(Maurizio Viroli, 1952~, 이탈리아 프린스턴대 정치사상사)**의 canonical thinker_id가 ES 미등록. `viroli`·`maurizio_viroli`·`viroli_m` 모두 MISS. **v2-rejected 후보군 5명 중 1명으로 사전 추정 → 원문 trademark 3중 일치로 확정**. Trademark 3중 일치: ① "조국을 지칭하기 위해 **파트리아(patria)와 나티오(natio)**라는 서로 다른 용어를 사용"(L52) — 비롤리 『For Love of Country: An Essay on Patriotism and Nationalism(1995)』의 **애국심(patriotism) vs 민족주의(nationalism) 어원 대립** trademark. 라틴어 patria(공화국·자유로운 조국) vs natio(출생·혈통·문화 공동체); ② "( ㉡ ) 사상은 **좋은 정치와 공적 삶에 참여하기 위한 인위적인 감정**을 중시"(L52) — 비롤리의 **공화주의적 애국심(republican patriotism)** 정의 trademark: 조국 사랑은 자연적·혈연적 감정이 아니라 **자유로운 공화국의 정치 제도와 공적 삶(vita civile)에 대한 인위적(artificial)·정치적 애착**; ③ "( ㉢ ) 사상은 **문화적·종족적·종교적 동질성**을 가장 앞세운다"(L52) — 비롤리가 민족주의를 **문화·종족·종교 동질성**에 기초한 집단주의로 규정하는 trademark. 비롤리는 19세기 이후 공화주의적 애국심이 민족주의에 흡수되면서 자유가 동질성으로 대체되었다고 비판. 답: ㉡ = **공화주의 / 공화주의적 애국심** / ㉢ = **민족주의(民族主義 — nationalism)**.
- 후속 조치: TASK-176 범위에서 `viroli` 신규 등록 + claim 작성 — **『For Love of Country: An Essay on Patriotism and Nationalism(1995)』**·**『Repubblicanesimo(1999, 공화주의)』**·**『Machiavelli(1998)』**·**『The Liberty of Servants(2011)』**·**공화주의적 애국심(republican patriotism) = 자유로운 공화국의 공적 삶·정치 제도에 대한 인위적 애착(patria)**·**민족주의(nationalism) 비판 = 문화·종족·종교 동질성에 기초한 집단주의(natio)**·**마키아벨리 해석자로서의 입지(공화주의적 자유 = 비지배로서의 자유의 역사적 원형)**·**페팃·스키너와 함께 신로마 공화주의(neo-Roman republicanism) 학파**·**이탈리아 리소르지멘토(Risorgimento)의 이중성 분석**·**자유(liberty)와 애국심의 공화주의적 양립**·**로마·피렌체 공화주의 전통 재해석**·**민족주의와 공화주의적 애국심의 역사적 분화**·**Philip Pettit·Quentin Skinner와의 공화주의 이론 상호 영향. 후보 id: `viroli`. 등록 우선순위 **우선** (현대 공화주의 정치사상의 대표 이론가, 애국심·민족주의 구분 문제에서 pettit 등록 및 공화주의 라인과 연동되어 반복 출제 가능성).
- 영향: Q3 정답 ㉡(공화주의적 애국심)·㉢(민족주의)은 trademark 3중 일치로 확정됨. coverage/2023-A.md Q3 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2023A-003 (TASK-175E-2023-A) — Q4 수운 최제우(崔濟愚) ES 미등록
- 심각도: blocker (ES 커버리지 누락 — 제시문 유일 사상가 미등록, 한국 윤리 동학 창시자)
- 사유: Q4 (L60-L72) 제시문 유일·중심 사상가 **수운(水雲) 최제우(崔濟愚, 1824-1864, 조선 후기 동학(東學) 창시자)**의 canonical thinker_id가 ES 미등록. `choe_jeu`·`choejeu`·`suun`·`choe_suun` 모두 MISS. **v2-rejected 후보군 5명 중 1명으로 사전 추정 → 원문 trademark 3중 일치로 확정**. Trademark 3중 일치: ① "천주를 모셔[**侍天主**] 조화(造化)가 정해지는 것을 영세토록 잊지 않으면 온갖 일을 알게 됩니다"(L66) — 동학 **본주문 13자 "侍天主 造化定 永世不忘 萬事知"** trademark. 수운 최제우가 1860년 4월 5일 경주 용담에서 체험한 '천주(한울님)로부터 받은 주문'이며, 『동경대전(東經大全)』「포덕문(布德文)」·「논학문(論學文)」에 수록된 동학 경전의 핵심; ② "'시(侍)'라는 것은 **안에 신령이 있고 밖에 ㉡이 있어서**, 세상 사람들이 각자 알아서 지키는 것"(L70) — 『동경대전』「논학문」원문 trademark: "**侍者 內有神靈 外有氣化 一世之人 各知不移者也**"(시라는 것은, 안으로 신령이 있고 밖으로 기화가 있어 온 세상 사람이 각각 알아서 옮기지 아니하는 것이다). 원문은 **"外有氣化"**(밖에 **기화**)이며 문제의 "천리"는 오답 → "기화(氣化)"로 교정; ③ "'주(主)'는 존칭으로, 마치 **㉢처럼 받드는 것**"(L71) — 『동경대전』「논학문」원문 trademark: "**主者 稱其尊而與父母同事者也**"(주라는 것은, 그 존엄을 칭하여 부모와 같이 섬기는 것이다). 원문은 **"父母"**(부모)이며 문제의 "군왕"은 오답 → "부모(父母)"로 교정. 답: 잘못된 것 2개 = ㉡ 천리(→기화) + ㉢ 군왕(→부모).
- 후속 조치: TASK-176 범위에서 `choe_jeu` 신규 등록 + claim 작성 — **동학(東學) 창시**·**천도교(天道敎) 원류**·**『동경대전(東經大全)』 (포덕문·논학문·수덕문·불연기연·탄도유심급)**·**『용담유사(龍潭遺詞)』 9편 한글 가사집**·**시천주(侍天主) = 내유신령·외유기화·각지불이**·**본주문 13자(侍天主 造化定 永世不忘 萬事知) / 강령주문 8자**·**지기금지원위대강(至氣今至願爲大降)**·**무위이화(無爲而化)**·**인내천(人乃天)의 원형 — 해월 최시형·의암 손병희로 전개**·**한울님(天主) 신관**·**후천개벽(後天開闢) 사상**·**유불선 3교 회통**·**서학(천주교) 대항으로서의 동학**·**동학농민혁명의 사상적 원천**·**1864년 좌도난정률(左道亂政律)로 처형**·**보국안민·제폭구민·광제창생**·**수운-해월-의암 도통(道統)**·**천도교 분립(시천교·상제교 등)**·**후대 김범부·이돈화 등 천도교 사상가. 후보 id: `choe_jeu` (canonical, 언더바 뒤 suffix 없이 단독). 등록 우선순위 **최우선** (한국 윤리 사상의 핵심 — 동학 창시자, 자생적 근대 한국 사상의 원점, 교과서 단골 출제, `jeongyagyong`·`wonhyo`·`yi_hwang`·`yi_i` 등록 한국 라인과 짝을 이루는 19세기 한국 사상 축).
- 영향: Q4 정답 ㉡(천리→기화)·㉢(군왕→부모)은 trademark 3중 일치 + 『동경대전』「논학문」원문 직접 대조로 확정됨. coverage/2023-A.md Q4 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2023A-004 (TASK-175E-2023-A) — Q5 을 리처드 슈웨더(Richard A. Shweder) ES 미등록
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 문화심리학·도덕 다원주의 정전)
- 사유: Q5 (L76-L89) **을** 제시문 중심 사상가 **리처드 슈웨더(Richard A. Shweder, 1945~, 시카고대 문화심리학자)**의 canonical thinker_id가 ES 미등록. `shweder`·`richard_shweder`·`shweder_r` 모두 MISS. **v2-rejected 후보군 5명 중 1명으로 사전 추정 → 원문 trademark 3중 일치로 확정**. Trademark 3중 일치: ① "**3가지의 도덕 원리** … 첫째 ( ㉡ )의 윤리 … 둘째 **공동체의 윤리** … 셋째 **신성함의 윤리**"(L82) — 슈웨더 "The 'Big Three' of Morality (Autonomy, Community, Divinity) and the 'Big Three' Explanations of Suffering"(in Morality and Health, 1997) trademark. 인도 부바네스와르(Bhubaneswar) 오리사(Orissa) 힌두 브라만 공동체 현장 연구를 통해 도출한 **3대 도덕 영역(Big Three Ethics)**; ② "( ㉡ )의 윤리는 개인을 보호하는 **'피해, 권리, 정의'** 개념을 강조"(L82) — 슈웨더의 **자율성 윤리(ethics of autonomy)** 정의 trademark: 서구 개인주의 문화가 중시하는 harm·rights·justice 개념. 콜버그의 정의(justice) 중심 도덕관은 슈웨더에게 있어 **3대 윤리 중 자율성 하나에 불과**하다는 비판적 함의; ③ "**공동체의 윤리**는 '의무, 존중, 충성' … **신성함의 윤리**는 '순수, 성스러움, 죄'"(L82) — 슈웨더가 콜버그의 서구 중심성을 비판하며 제시한 **도덕 다원주의(moral pluralism)** trademark. 답: ㉡ = **자율성(autonomy)**.
- 후속 조치: TASK-176 범위에서 `shweder` 신규 등록 + claim 작성 — **문화심리학(cultural psychology) 창시자**·**3대 윤리(Big Three Ethics): 자율성(autonomy) · 공동체(community) · 신성(divinity)**·**"The 'Big Three' of Morality"(1997)**·**『Thinking Through Cultures(1991)』**·**『Why Do Men Barbecue? Recipes for Cultural Psychology(2003)』**·**도덕 다원주의(moral pluralism)**·**인도 오리사(Orissa) 필드 연구**·**하이트 도덕 기반 이론(Moral Foundations Theory)의 직접적 전구 — Care·Fairness·Loyalty·Authority·Sanctity 기반이 슈웨더의 3대 윤리를 확장한 것**·**WEIRD 표본 비판**·**콜버그 보편주의 비판(서구 자율성 윤리 편향)**·**문화 특수적 도덕 실천(culture-specific moral practices)**·**맥락주의 심리학**·**가이거티 심리학(Geiger-like psychology) 비판**·Clifford Geertz 해석 인류학의 심리학적 확장. 후보 id: `shweder`. 등록 우선순위 **최우선** (문화심리학·도덕심리학 교과서 단골, `haidt` 등록 라인의 이론적 전구로서 반드시 연동 등록 필요).
- 영향: Q5 정답 ㉡(자율성)은 trademark 3중 일치로 확정됨. coverage/2023-A.md Q5 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2023A-005 (TASK-175E-2023-A) — Q6 갑 고운 최치원(崔致遠) ES 미등록
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 한국 고대 유학·3교 회통의 원조)
- 사유: Q6 (L93-L99) **갑** 제시문 중심 사상가 **고운(孤雲) 최치원(崔致遠, 857-?, 신라 말 6두품 유학자·문장가, 당나라 빈공과 급제)**의 canonical thinker_id가 ES 미등록. `choe_chiwon`·`choechiwon`·`gounn`·`choe_goun` 모두 MISS. **v2-rejected 후보군 5명 중 1명으로 사전 추정 → 원문 trademark 3중 일치로 확정**. Trademark 3중 일치: ① "나라에 **현묘한 도(玄妙之道)**가 있는데 ( ㉠ )(이)라고 한다 … 뭇 생명을 접해 교화한다[**接化群生**]"(L97) — 최치원 「**난랑비서(鸞郞碑序)**」 trademark 원문: "**國有玄妙之道 曰風流 … 實乃包含三敎 接化群生**"(나라에 현묘한 도가 있으니 '풍류(風流)'라 한다. … 실로 삼교를 포함하여 뭇 생명을 접하여 교화한다). 『삼국사기(三國史記)』「신라본기」 진흥왕 37년조에 수록; ② "실로 이는 ( ㉡ )하고"(L97) — 원문 "**實乃包含三敎 接化群生**"의 "**包含三敎**"(삼교를 포함함) 대응. 유교·도교·불교 3교 회통 trademark; ③ "들어와 집에서 효도하고 나아가 나라에서 충성(**入孝出忠**)하는 것은 ㉢(=공자)의 뜻과 같고 … 함이 없는 일에 처하고 말 없는 가르침을 행하는 것은 **주(周)나라 주사(柱史, =노자)의 종지**와 같고 … 모든 악을 행하지 않고 모든 선을 행하는 것은 **축건(竺乾)국 태자(=석가모니)**의 교화와 같다"(L97) — 유·도·불 3교를 각각 공자·노자·석가모니로 배정하는 3교 회통 trademark. 답: ㉠ = **풍류(風流)**, ㉡ = **포함삼교(包含三敎)**.
- 후속 조치: TASK-176 범위에서 `choe_chiwon` 신규 등록 + claim 작성 — **「난랑비서(鸞郞碑序)」 — 신라 화랑(花郞)의 비문 서문**·**풍류도(風流道) / 현묘지도(玄妙之道)**·**포함삼교(包含三敎) — 유·불·도 3교 회통**·**접화군생(接化群生)**·**입효출충(入孝出忠) = 공자 유교**·**주사(柱史) 종지 = 노자 도교**·**축건국 태자 교화 = 석가모니 불교**·**당나라 빈공과(賓貢科) 급제(868년)**·**『계원필경(桂苑筆耕)』 — 당대 재당(在唐) 기간 문집**·**「격황소서(檄黃巢書)」 — 당 말 황소의 난 토벌 격문**·**신라 말 6두품 유학자의 좌절**·**유교 정치 이상과 신라 현실 사이 갈등**·**해인사 은거·가야산 유적**·**고려 유학 전통의 출발점**·**한국 고유 사상과 외래 사상 회통의 원형**·한국 화랑 정신·세속오계와의 연관성·원효 불교 회통론과의 병행(한국 회통 사상 전통). 후보 id: `choe_chiwon` (canonical, 언더바 뒤 suffix 없이 단독). 등록 우선순위 **최우선** (한국 고대 윤리 사상의 원점, 교과서 단골 — 풍류도·3교 회통 문제에서 반드시 출제, `wonhyo` 등록 한국 불교 회통 라인과 짝).
- 영향: Q6 정답 ㉠(풍류)·㉡(포함삼교)은 trademark 3중 일치로 확정됨. coverage/2023-A.md Q6 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2023A-006 (TASK-175E-2023-A) — Q10 을 아우구스토 블라지(Augusto Blasi) ES 미등록
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 도덕적 정체성·도덕심리학의 정전)
- 사유: Q10 (L159-L167) **을** 제시문 중심 사상가 **아우구스토 블라지(Augusto Blasi, 1931-2013, 메사추세츠대 보스턴 도덕심리학자)**의 canonical thinker_id가 ES 미등록. `blasi`·`augusto_blasi`·`blasi_a` 모두 MISS. **v2-rejected 후보군 5명 중 1명으로 사전 추정 + 2020-B → 2023-A 2연속 재출제 관측**(v2-rejected 기록 상). Trademark 3중 일치: ① "학생들의 **도덕적 정체성** 형성에 주안점 … 도덕적 정체성은 **도덕적 인격의 차원**"(L167) — 블라지 **도덕적 자아 동일성(moral self-identity)** 이론 trademark. 『Moral Functioning: Moral Understanding and Personality(2004)』 등에서 도덕적 인격(moral personality)을 도덕적 이해·욕구·행동의 통합체로 규정; ② "**도덕적 인격을 구성하는 3가지 요소**는 ( ㉡ ), **의지력, 자기통합성**"(L167) — 블라지 "Moral Character: A Psychological Approach"(1993) trademark **3요소**: **① 도덕적 욕구/도덕적 책임감(moral desires/responsibility)** + **② 의지력(willpower)** + **③ 자기통합성(self-integration)**; ③ "의지력과 자기통합성은 … **본질은 될 수 없다 … 도덕적 인격의 핵심적인 요소이자 본질은 ( ㉡ ) … 도덕적 이해에 근거한 반성을 통해 형성**"(L167) — 블라지의 trademark 주장: 의지력·자기통합성은 **기능적·형식적 요소**이고 선악 중립이며, **도덕적 욕구 없이는 도덕적 인격이 성립하지 않는다**. 도덕적 욕구는 **도덕적 이해(moral understanding)에 근거한 반성적 판단**을 통해 형성. 답: ㉡ = **도덕적 욕구 / 도덕적 책임감(道德的 責任感 — moral responsibility/moral desires)**.
- 후속 조치: TASK-176 범위에서 `blasi` 신규 등록 — **2연속 재출제(2020-B → 2023-A) 확증**되었으므로 **최우선 순위로 격상**. 요구 claim: **도덕적 자아 동일성(moral self-identity) 이론**·**도덕적 정체성(moral identity)**·**도덕적 인격(moral personality) 3요소: 도덕적 욕구(책임감) · 의지력(willpower) · 자기통합성(self-integration/self-consistency)**·**도덕적 이해(moral understanding)와 반성적 판단**·**"Moral Character: A Psychological Approach"(1993)**·**『Moral Functioning: Moral Understanding and Personality(2004)』**·**"Moral Cognition and Moral Action: A Theoretical Perspective"(1983)**·**"Bridging Moral Cognition and Moral Action"(1980)**·**콜버그 인지 발달 모델의 보완·신콜버그주의 비판적 계승**·**도덕적 자아와 행동 사이의 매개 구조**·**레스트(rest 등록) 4구성요소 모델과의 병렬적 위치**·**리코나(lickona 등록) 인격 교육론과의 접점**·**도덕적 욕구의 형식·내용 이원성**·**의지력·자기통합성이 도덕화되기 위한 조건으로서의 도덕적 욕구**·사회인지적 도덕 발달론·Damon 도덕적 자아론과의 대비. 후보 id: `blasi`. 등록 우선순위 **최우선** (2연속 재출제 확증, 도덕 교육·도덕 심리학 교과서 단골 출제, `rest`·`lickona`·`kohlberg`와 함께 현대 도덕심리학 4대 축 중 하나).
- 영향: Q10 정답 ㉡(도덕적 욕구/책임감)·㉡의 ㉢·㉣에 대한 공통 영향(도덕적 방향·내용 부여)은 trademark 3중 일치로 확정됨. coverage/2023-A.md Q10 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2023B-001 (TASK-175E-2023-B) — Q1 갑·을 사상가 특정 불능 (한국 성리학 주자 성의장 비판 논변)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2023-B.md` Q1 row (L14 문항 전체)
- 심각도: blocker (사상가형 문항이나 제시문 trademark 3중 일치로 사상가 고유명 확정 불능 — Phase 6 규칙 7항 창작 금지 준수)
- 사유: Q1 (L14-L20) 발문에 "갑은 **동양 윤리 사상가**, 을은 **한국 윤리 사상가**"라고만 분류 명시되어 있고, 제시문 구절 내에 사상가 고유명(주희/퇴계/율곡/다산/주자/정약용 등) 또는 저서명 고유어가 직접 노출되지 않음. 제시문 구조를 기반으로 한 최유력 후보 추정: 갑 = **주희(朱熹) 『대학장구(大學章句)』「성의장(誠意章)」 해석**; 을 = **다산(茶山) 정약용(丁若鏞) 『대학공의(大學公議)』에서의 주자 성의장 비판**. 추정 근거: ① 갑의 『대학』 「성의장」"여호호색 여오악취(如惡惡臭 如好好色)" 인용 + "아름다운 색을 볼 때 이미 자연스럽게 좋아하는 것이지, 보고 난 뒤에 다시 결심을 하고 그것을 좋아하는 것은 아닙니다"(L18) → 주자의 성의장 해석 전통(호오 = 자연적·즉각적 감응)이며 주희가 『대학장구』에서 실제로 표명한 입장과 일치. ② 을의 **형기(形氣) vs 의리(義理) 이원 대비**(L20) + "'갑'이 **형기의 하는 바를 끌어다가 의리의 호오에 대한 설을 밝히려 한 것은 대단히 옳지 않습니다**"(L20) → 주자의 성의장 해석이 형기 차원의 자연적 호오를 의리 차원 성의 개념에 부당하게 적용했다는 비판. 이 구조는 **다산 정약용 『대학공의』·『심경밀험(心經密驗)』**에서의 주자 성의장 비판("호오는 성(性)이 아니라 기호(嗜好)이며, 주자가 색호·악취의 감각적 호오를 의리적 성의에 비유한 것은 착오")과 가장 부합. 그러나 원문에 "다산", "공의", "정약용", "주자", "주희" 등 **고유명이 단 한 건도 등장하지 않음**으로 Phase 6 규칙 "trademark 3중 일치" 기준이 성립하지 않음. 퇴계(이황)·율곡(이이)도 후보이지만 이들은 주자학을 옹호·계승하는 입장이어서 주자 성의장 해석을 근본적으로 비판하는 을의 어조와 부합하지 않음. 답(빈칸 ㉠·㉡)은 『대학』 성의장 표준 해석 구조에서 **㉠ = 지(知 — 앎/봄), ㉡ = 의(意 — 뜻/좋아함)**으로 추정되나(8조목 격물치지·성의 단계), 이 추정은 갑·을 사상가 특정과 독립적으로도 trademark 2중 일치(『대학』 성의장 원문 + 8조목 구조)로 성립. 교과서 표준 정답 확인 필요.
- 후속 조치: ① TASK-176 범위에서 `jeongyagyong`(HIT, 이미 등록)의 claim에 **『대학공의(大學公議)』·『심경밀험(心經密驗)』에서의 주자 성의장 비판 / 호오는 기호(嗜好)이지 성(性)이 아니다 / 형기와 의리의 구분**을 보강. ② 교과서·해설지·출제 의도 해설을 확인하여 갑·을 확정 (사용자 검토 필요). ③ Q1 ㉠·㉡ 정답은 독립적으로 '지(知)·의(意)' trademark 2중 일치로 제시하되, 대체 후보(지(知)·행(行), 호(好)·오(惡) 등)도 열거해 교과서 표준 확인 후 최종 정답 고정.
- 영향: Q1 사상가 고유명 확정은 trademark 미달로 불가. 빈칸 정답(㉠·㉡)은 『대학』 성의장 표준 해석으로 확정 근거 제시. coverage/2023-B.md Q1 row에 `<!-- BLOCKER(TASK-175E-2023-B): BLK-175E-2023B-001 -->` 인라인 삽입 완료.

### BLK-175E-2023B-002 (TASK-175E-2023-B) — Q4 라인홀드 니버(Reinhold Niebuhr) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2023-B.md` Q4 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 유일·중심 사상가 미등록, 20세기 기독교 현실주의·사회윤리학 정전)
- 사유: Q4 (가) (L78-L84) 제시문 중심 사상가 **라인홀드 니버(Reinhold Niebuhr, 1892-1971, 미국 유니온 신학대 기독교 현실주의 신학자·사회윤리학자)**의 canonical thinker_id가 ES 미등록. `niebuhr`·`reinhold_niebuhr`·`niebuhr_r` 모두 MISS. Trademark 3중 일치: ① "개개의 인간은 **이성적 능력을 통해 정의감을 키워** 간다 … 이기주의적인 요소들을 정화"(L84) — 니버 『도덕적 인간과 비도덕적 사회(Moral Man and Immoral Society: A Study in Ethics and Politics, 1932)』 trademark. 개인 차원에서 교육·이성·종교의 일정한 도덕적 효과를 인정; ② "개인의 이기심이 합리성의 발전이나 **종교적 선의지**의 성장에 의해 점진적으로 견제되고 있다는 생각은 우리 시대에 매우 심각한 **도덕적·정치적 혼란**을 가져왔다"(L84) — 니버의 **자유주의적 낙관주의 비판** trademark. 존 듀이 등 자유주의자의 이성·교육·종교 낙관론을 근본 비판하며 기독교 현실주의 정초; ③ "**모든 인간의 집단**은, 개인과 비교할 때 이기심을 올바르게 인도하고 때에 따라 억제할 수 있는 **자기 극복 능력**과 다른 사람들의 욕구를 수용하는 능력이 훨씬 결여되어 있다"(L84) — 『도덕적 인간과 비도덕적 사회』의 **책 제목 자체에 대응하는 핵심 명제** trademark. 개인은 도덕적일 수 있어도 집단(사회·국가·인종·계급)은 본질적으로 비도덕적(이기적·폭력적)이며 **자기극복(self-transcendence)이 불가능**하다는 사회윤리 정식. 답: ㉡ = **심리적(psychological)**, ㉣ = **윤리적(ethical)**은 (나) 이기주의 메타 분류 표준 용어. (가)의 서술 요지: 개인에서 ㉢(이성)은 ㉠(이기심)을 견제·정화하지만, 집단에서 ㉢(이성)은 ㉠(이기심)을 견제하지 못하고 오히려 집단 이기심을 합리화·정당화하는 이데올로기로 기능.
- 후속 조치: TASK-176 범위에서 `niebuhr` 신규 등록 + claim 작성 — **『도덕적 인간과 비도덕적 사회(Moral Man and Immoral Society, 1932)』**·**『기독교 현실주의와 정치적 문제(Christian Realism and Political Problems, 1953)』**·**『인간의 본성과 운명(The Nature and Destiny of Man, 1941-1943)』** (기포드 강연)·**기독교 현실주의(Christian realism)**·**개인 윤리와 사회 윤리의 비대칭**·**집단 이기주의(group egoism)**·**자기극복(self-transcendence)의 집단적 불가능성**·**권력 균형(balance of power)을 통한 사회 정의**·**죄(sin)와 자기중심성**·**자유주의 신학·자유주의 정치 낙관주의 비판**·**존 듀이 비판**·**원죄론(original sin) 재해석**·**평화주의(pacifism) 비판**·**세속 이데올로기 비판**·**미국 냉전기 기독교 현실주의 외교 정책에 끼친 영향**(조지 케넌 등)·**민권 운동과의 관계**·**해럴드 라스키·호세 오르테가 이 가세트·칼 바르트와의 대화**·동생 H. 리처드 니버(H. Richard Niebuhr, 도덕 신학자)와의 구분 — 동명이인 여부 확인 필요(suffix 규약: `niebuhr_r` = Reinhold vs `niebuhr_h` = H. Richard). 후보 id: `niebuhr` (단독) 또는 `niebuhr_r` (H. Richard Niebuhr도 등록 시). 등록 우선순위 **최우선** (사회윤리·환경·정치 윤리 교과서 단골 출제, 개인/집단 비대칭 논제의 고전적 정전).
- 영향: Q4 정답 ㉡(심리적)·㉣(윤리적)은 trademark 2중 일치(규범윤리 일반 메타 분류)로 확정됨. 또한 (가)의 개인·집단에서의 ㉢(이성) 작동 방식 서술은 니버 『도덕적 인간과 비도덕적 사회』 trademark 3중 일치로 확정됨. coverage/2023-B.md Q4 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2023B-003 (TASK-175E-2023-B) — Q7 (가) 나가르주나(Nāgārjuna, 龍樹) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2023-B.md` Q7 row (가)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 인도 대승불교 중관학파 창시자, 불교 철학의 최고 정점)
- 사유: Q7 (가) (L133-L139) 제시문 중심 사상가 **나가르주나(龍樹, Nāgārjuna, 150?-250?, 인도 대승불교 중관학파(中觀學派) 창시자)**의 canonical thinker_id가 ES 미등록. `nagarjuna`·`龍樹`·`yongsu`·`ryuju` 모두 MISS. Trademark 3중 일치: ① "모든 존재는 **연기(緣起)**에 의해 원인과 결과로 얽힌 **상호 의존적 존재**이므로 고정·불변하는 독자적 성질, 즉 **자성(自性)은 존재하지 않는다**"(L139) — 나가르주나 **『중론(中論, Madhyamaka-kārikā)』** 제24장 제18송 trademark: "yaḥ pratītyasamutpādaḥ śūnyatāṃ tāṃ pracakṣmahe" (연기로 생기는 것을 우리는 공이라 부른다). **연기 = 무자성(niḥsvabhāva) = 공(śūnyatā)** 3항 동일성; ② "㉠ 우리가 실체라 믿는 것들은 실은 존재하지 않는다"(L139) — 나가르주나의 **자성 부정(niḥsvabhāvavāda)** trademark. 『중론』 제15장 「관유무품(觀有無品)」의 자성 정의("자성은 지어지지 않음 + 다른 것에 의존하지 않음")에 따라 연기하는 모든 것이 자성 없음; ③ "모든 존재는 실체가 없는 ( ㉡ )이다"(L139) — 중관학파의 **공(空, śūnyatā)** trademark 결론. ㉡ = **공(空)**. 답: ㉡ = 공(空).
- 후속 조치: TASK-176 범위에서 `nagarjuna` 신규 등록 + claim 작성 — **중관학파(Mādhyamika) 창시자**·**『중론(中論, Madhyamaka-kārikā)』**·**『회쟁론(廻諍論, Vigrahavyāvartanī)』**·**『공칠십론(空七十論, Śūnyatāsaptati)』**·**『대지도론(大智度論, Mahāprajñāpāramitā-śāstra)』 저자 전통**·**연기(緣起, pratītya-samutpāda)**·**무자성(無自性, niḥsvabhāva)**·**공(空, śūnyatā)**·**팔불중도(八不中道 — 불생불멸·불상부단·불일불이·불래불거)**·**이제(二諦) 사상: 세속제(世俗諦, saṁvṛti-satya)와 승의제(勝義諦, paramārtha-satya)**·**공역공(空亦空) — 공 자체도 공**·**삼시문(三時門)**·**부파 아비달마 비판**·**중관파/응성파(應成派, Prāsaṅgika) vs 자립논증파(自立論證派, Svātantrika) 분기의 원조**·**월칭(月稱, Candrakīrti)의 계승**·**삼론종(三論宗, 길장 『삼론현의』)의 동아시아 전개**·**티벳 불교 중관파 전통**·**반야계 경전(般若經, Prajñāpāramitā Sūtras)의 사상적 기반**·용수의 가상 대담 형식·**『친우서(親友書, Suhṛllekha)』**의 재가 윤리·한국 원효·의상의 중관·화엄 결합과의 관계. 후보 id: `nagarjuna`. 등록 우선순위 **최우선** (불교 철학의 최고 정점, 동양 윤리·불교 교과서 필수 출제, `wonhyo`·`huineng`·`buddha`와 함께 대승불교 4대 축 중 중관 대표).
- 영향: Q7 (가) 정답 ㉡(공)은 trademark 3중 일치로 확정됨. coverage/2023-B.md Q7 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2023B-004 (TASK-175E-2023-B) — Q7 (나) 바수반두(世親, Vasubandhu) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2023-B.md` Q7 row (나)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 인도 대승불교 유식학파 체계화 정점)
- 사유: Q7 (나) (L141-L143) 제시문 중심 사상가 **바수반두(世親, Vasubandhu, 4세기경, 인도 대승불교 유식학파(瑜伽行派) 대표, 무착(無著, Asaṅga)의 동생)**의 canonical thinker_id가 ES 미등록. `vasubandhu`·`世親`·`sechin` 모두 MISS. Trademark 3중 일치: ① "**아뢰야식(阿賴耶識)**은 현상 세계를 포괄하고 있는 마음 자체"(L143) — 유식학파 **아뢰야식(ālaya-vijñāna, 저장식)** trademark. 바수반두 **『유식삼십송(唯識三十頌, Triṃśikā-vijñaptimātratā)』** 제1게: "由假說我法 有種種相轉 彼依識所變 此能變唯三"(가설된 아와 법이 여러 형상으로 전개되나, 이는 식의 변(變)에 의존하며, 그 능변은 오직 셋 — 이숙식[아뢰야식]·사량식[말나식]·요별식[전6식]); ② "아뢰야식이 **전변(轉變)**하여 이원화됨으로써 주관계와 객관계가 전개 … 주관적인 부분을 ( ㉢ )이라 하고, **객관적인 부분을 상분(相分)**"(L143) — 유식학파의 **견분(見分, darśana-bhāga) vs 상분(相分, nimitta-bhāga)** 이원 구조 trademark. 후대 호법(護法, Dharmapāla)의 4분설(상분·견분·자증분·증자증분)로 정교화되나, 기본 이분법은 바수반두 유식 체계의 골격; ③ "무명(無明)으로 인해 … 자아와 세계로 분별하고 집착 … **아집(我執)**과 … **법집(法執)**"(L143) — 유식학파의 **아집·법집 이중 집착 구조** trademark. 『유식삼십송』 제1게에 직접 대응, 유식 수행의 목표는 **아공·법공**의 이공(二空) 실현. 답: ㉢ = **견분(見分)**.
- 후속 조치: TASK-176 범위에서 `vasubandhu` 신규 등록 + claim 작성 — **유식학파(瑜伽行唯識派, Yogācāra-Vijñānavāda) 체계화 대표**·**무착(無著, Asaṅga)의 동생·공동 학파 정초자**·**『유식삼십송(Triṃśikā-vijñaptimātratā)』**·**『유식이십송(Viṃśatikā-vijñaptimātratā)』**·**『구사론(俱舍論, Abhidharmakośa)』 — 설일체유부(說一切有部) 대표작(대승 전향 이전)**·**『섭대승론석(攝大乘論釋)』 — 무착 저작에 대한 주석**·**아뢰야식(ālaya-vijñāna)·말나식(manas-vijñāna)·전6식(前六識) 체계**·**식전변(識轉變, vijñāna-pariṇāma)**·**삼성설(三性說): 변계소집성(parikalpita)·의타기성(paratantra)·원성실성(pariniṣpanna)**·**삼무성설(三無性說)**·**유식무경(唯識無境)**·**종자설(種子說, bīja)**·**훈습(熏習, vāsanā)**·**법상종(法相宗) — 현장(玄奘)·규기(窺基)가 동아시아로 전래**·**『성유식론(成唯識論, Vijñaptimātratāsiddhi)』 — 호법 중심 10대 논사 주석 집성(현장 번역)**·**중관 vs 유식 쟁론**·**진제(眞諦, Paramārtha)·현장(玄奘)·의정(義淨)의 한역 — 대소승 1,200여 권 저술 추정**·한국 원효(元曉)·의상(義湘)의 유식 수용과의 관계·일본 법상종(法相宗). 후보 id: `vasubandhu`. 등록 우선순위 **최우선** (불교 철학 두 번째 정점 — 중관과 쌍벽을 이루는 유식학파 대표자, `nagarjuna`와 함께 등록되어야 대승불교 양대 축 완성. 교과서 단골 출제 — 아뢰야식·견분/상분·아집/법집은 고등 윤리 단골 개념).
- 영향: Q7 (나) 정답 ㉢(견분)은 trademark 3중 일치로 확정됨. coverage/2023-B.md Q7 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2023B-005 (TASK-175E-2023-B) — Q8 (가) 지그문트 프로이트(Sigmund Freud) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2023-B.md` Q8 row (가)
- 심각도: blocker (ES 커버리지 누락 — 제시문 유일·중심 사상가 미등록, 20세기 정신분석학 창시자·도덕 발달 심층심리학 정전)
- 사유: Q8 (가) (L151-L157) 제시문 중심 사상가 **지그문트 프로이트(Sigmund Freud, 1856-1939, 오스트리아 정신분석학 창시자)**의 canonical thinker_id가 ES 미등록. `freud`·`sigmund_freud`·`freud_s` 모두 MISS. Trademark 3중 일치: ① "인간의 성격은 **원초아(id), 자아(ego), 초자아(superego)**"(L157) — 프로이트 **『자아와 이드(Das Ich und das Es, 1923)』** trademark **성격 3구조 모델** 완전 일치. id(무의식적 욕망)·ego(현실 조정)·superego(도덕 검열); ② "아이는 부모나 보호자의 도덕적 기준을 **내면화**하여 자신의 **초자아**를 형성"(L157) — 프로이트의 **오이디푸스 콤플렉스 해소에서의 부모 동일시와 초자아 형성** trademark. 『자아와 이드』 제3장: "초자아는 오이디푸스 콤플렉스의 상속자(heir of the Oedipus complex)"; ③ "**초자아는 양심과 ( ㉡ )이라는 2가지의 요소**로 구성"(L157) — 프로이트의 **초자아 2요소 모델** trademark: ① 양심(conscience) — 금지 기능·죄책감 원천 / ② **자아 이상(ego-ideal, Ich-Ideal)** — 이상적 목표 기능·자긍심 원천. 답: ㉡ = **자아 이상(自我理想)**. 또한 ㉣(처벌)이 양심에 미치는 영향 = 외부 처벌이 동일시 과정을 거쳐 내면화되어 양심(자기 처벌 기제)을 형성·강화.
- 후속 조치: TASK-176 범위에서 `freud` 신규 등록 + claim 작성 — **정신분석학(Psychoanalyse) 창시**·**성격 3구조(id·ego·superego)**·**초자아 2요소(양심·자아 이상)**·**오이디푸스 콤플렉스(Ödipuskomplex)**·**이드·에고·슈퍼에고 에너지 경제학**·**무의식(Unbewusste)·전의식(Vorbewusste)·의식(Bewusste)**·**리비도(Libido)**·**1차 과정(primary process)·2차 과정(secondary process)**·**현실 원리·쾌락 원리**·**방어기제(defense mechanisms): 억압·투사·전치·승화·합리화·동일시·반동형성·퇴행**·**죽음 충동(Todestrieb)**·**꿈의 해석(Die Traumdeutung, 1900)**·**정신분석 운동의 탄생**·**『토템과 터부(Totem und Tabu, 1913)』**·**『문명 속의 불만(Das Unbehagen in der Kultur, 1930)』** — 도덕과 죄책감의 문명적 기원·**『자아와 이드(Das Ich und das Es, 1923)』**·**『집단 심리학과 자아 분석(Massenpsychologie und Ich-Analyse, 1921)』**·**융(C.G. Jung)·아들러(A. Adler)와의 분열**·**신프로이트주의(에릭슨·호나이·설리반)**·**라캉 정신분석의 재해석**·**콜버그·피아제 인지 발달론과의 대비(도덕 발달의 정의적·무의식적 차원)**·초기 히스테리 연구·드라이브 이론·구조 이론 전환·**도덕성의 무의식적·비합리적 기원 강조**. 후보 id: `freud`. 등록 우선순위 **최우선** (20세기 인문학·사회과학의 가장 영향력 있는 사상가 중 하나, 도덕성 발달 이론 교과서 단골 출제의 핵심 — 콜버그·피아제와 함께 도덕 발달론 3대 축이지만 정의적·심층심리 차원 담당).
- 영향: Q8 (가) 정답 ㉡(자아 이상)·초자아가 자아에 대해 수행하는 도덕적 감시자 역할·㉣(처벌)이 양심 형성에 미치는 영향은 trademark 3중 일치로 확정됨. coverage/2023-B.md Q8 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2023B-006 (TASK-175E-2023-B) — Q8 (나) 벌허스 프레더릭 스키너(B.F. Skinner) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2023-B.md` Q8 row (나)
- 심각도: blocker (ES 커버리지 누락 — 제시문 유일·중심 사상가 미등록, 20세기 행동주의 심리학 정점)
- 사유: Q8 (나) (L159-L161) 제시문 중심 사상가 **벌허스 프레더릭 스키너(Burrhus Frederic Skinner, 1904-1990, 미국 하버드대 행동주의 심리학자)**의 canonical thinker_id가 ES 미등록. `skinner`·`bf_skinner`·`skinner_bf` 모두 MISS. Trademark 3중 일치: ① "인간의 도덕적 행동은 **학습**되는 것 … 학습은 **경험의 결과**"(L161) — 스키너 행동주의 trademark. **『과학과 인간 행동(Science and Human Behavior, 1953)』**에서 도덕·종교·예술 등 모든 인간 행동을 학습된 행동(learned behavior)으로 환원; ② "특정 행동의 발생 빈도는 **보상을 받을 때 증가**하고, **㉣ 처벌을 받을 때 감소**"(L161) — 스키너의 **강화·처벌 법칙(law of reinforcement and punishment)** trademark. 조작적 조건화(operant conditioning)의 기본 원리 — 결과에 따른 행동 빈도 변화; ③ "학습자에게 다양한 반응을 산출하도록 영향을 미치는 **( ㉢ )**으로부터 비롯 … 인간이 어느 순간에 보여 주는 행동은 당시 그가 속한 **( ㉢ )**에 의해 통제되고 결정"(L161) — 스키너의 **환경 결정론(environmental determinism)** trademark. **『자유와 존엄을 넘어서(Beyond Freedom and Dignity, 1971)』** 핵심 명제: "행동은 내부의 자율적 인간(autonomous man)에 의해서가 아니라 **환경**에 의해 통제된다." 답: ㉢ = **환경(環境 — environment)**.
- 후속 조치: TASK-176 범위에서 `skinner` 신규 등록 + claim 작성 — **행동주의(Behaviorism) 급진적 형태 — 근본 행동주의(Radical Behaviorism)**·**조작적 조건화(operant conditioning)**·**강화 스케줄(reinforcement schedules): 연속 강화·간헐 강화(고정비율·변동비율·고정간격·변동간격)**·**스키너 상자(Skinner box, operant chamber)**·**행동 형성(shaping) — 점진적 근사법(successive approximations)**·**언어 행동(Verbal Behavior, 1957)**·**『과학과 인간 행동(Science and Human Behavior, 1953)』**·**『자유와 존엄을 넘어서(Beyond Freedom and Dignity, 1971)』** — 자유의지 부정·문화 설계론·**『월든 투(Walden Two, 1948)』** — 유토피아 소설·행동주의 사회 설계·**문화 공학(cultural engineering)**·**행동 분석(behavior analysis) — 실험적 분석과 응용 행동 분석**·**왓슨(J.B. Watson) 행동주의의 계승·확장**·**파블로프 고전적 조건화와의 구분**·**촘스키(N. Chomsky)의 언어 이론 비판에 의한 도전**·**인지주의 혁명 이후의 유산**·**응용 행동 분석(ABA, Applied Behavior Analysis) — 자폐 치료·교육 개입의 이론적 기반**·**교육 기술(teaching machine)·프로그램 학습**·**도덕 발달에 대한 환경론적 설명 — 콜버그·피아제 인지 발달론의 반대 축**·자유의지·책임·인격 개념 비판. 후보 id: `skinner`. 등록 우선순위 **최우선** (20세기 심리학·도덕 발달론 교과서 단골 출제의 대표 인물, 도덕성 발달 이론 3대 축 — 프로이트(심층심리학)·콜버그(인지 발달)·스키너(행동주의) — 중 행동주의 대표, 자유와 결정론의 철학적 논쟁 맥락에서도 반복 출제).
- 영향: Q8 (나) 정답 ㉢(환경)은 trademark 3중 일치로 확정됨. coverage/2023-B.md Q8 본문 내용은 정확하며 ES 커버리지 공백만 존재.

### BLK-175E-2024A-001 (TASK-175E-2024-A) — Q5 쿰스(Jerrold R. Coombs)·뮉스(Milton Meux) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2024-A.md` Q5 row (가)·(나)
- 심각도: blocker (ES 커버리지 누락 — 교과교육학 도덕과 수업모형 핵심 실천가, 2015/2022 개정 도덕과 교육과정 해설서 정전)
- 사유: Q5 (L55-L93) 제시문은 **쿰스(Jerrold R. Coombs)·뮉스(Milton Meux)의 가치갈등해결 수업모형(Value Analysis Model / Value Conflict Resolution Model)**이며, canonical thinker_id가 ES 미등록. `coombs`·`jerrold_coombs`·`meux` 모두 MISS. Trademark 3중 일치: ① "(가) 수업모형 절차 5단계 … 1. 가치문제 사례 제시 / 2. ( ㉠ ) / 3. 잠정적 가치 결정 / 4. ( ㉡ ) / 5. 최종 가치 결정"(L59-L64) — 쿰스·뮉스 1971년 논문 "Teaching Strategies for Value Analysis"(NSSE 71st Yearbook, Part II: *Values Education*) trademark **5단계 가치분석 절차**: ① 가치문제 제시 → ② **가치갈등 사실의 명료화(fact-value clarification / value issue analysis)** → ③ 잠정적 가치 결정 → ④ **가치 원리 검사(value principle testing)** → ⑤ 최종 가치 결정. 2015/2022 개정 도덕과 교육과정 해설서 및 도덕과 교수·학습 자료 수록 정전 구조; ② (나) ㉠ 단계 교사 문답 "이 사건에 관련된 도덕적 가치에 대해 살펴봅시다 … 무임승차로 점수를 받는 것은 불공정 … 친분 때문에"(L67-L87) — 쿰스 **가치갈등 사실의 명료화** trademark: 상충하는 가치(공정성 vs 친분·우정)의 식별 + 사실적 근거 분석 + 가치 개념 명료화; ③ (나) ㉢ 교사 발화 "사람들은 평가는 공정해야 한다고 생각합니다. 평가의 공정성이 친분에 의해 훼손되어서는 안 됩니다"(L93) — 쿰스 가치 원리 검사 4가지 하위 기법(포섭 검사·역할 교환 검사·새로운 사례 검사·경고 검사) 중 **포섭 검사(subsumption test)** 또는 **경고 검사(warning test)** trademark 작동 구조. 답: ㉠ = **가치갈등 사실의 명료화**, ㉡ = **가치 원리 검사**, ㉢ = **포섭 검사(유력)**.
- 후속 조치: TASK-176 범위에서 `coombs` 신규 등록 여부 사용자 판단 필요 — **가치갈등해결 수업모형(Value Analysis Model) 창시자**·**뮉스(Milton Meux)와 공저 — 1971년 NSSE Yearbook 논문 "Teaching Strategies for Value Analysis"**·**5단계 가치분석 절차(가치문제 제시 → 가치갈등 사실의 명료화 → 잠정적 가치 결정 → 가치 원리 검사 → 최종 가치 결정)**·**가치 원리 검사 4가지 하위 기법: 포섭 검사(subsumption test)·역할 교환 검사(role exchange test)·새로운 사례 검사(new cases test)·경고 검사(warning test/casuistry test)**·**도덕과 가치 분석형 수업모형의 대표**·**2015/2022 개정 도덕과 교육과정 해설서 수록**·**래스(L.E. Raths)의 가치명료화 모형, 올리버·셰이버(D.W. Oliver, J.P. Shaver)의 사회쟁점 분석 모형과 함께 도덕과 수업모형 3대 축**·**뱅크스(J.A. Banks)의 가치 탐구 모형과도 연계**. 후보 id: `coombs`. 등록 우선순위 **상(교과교육학 실천가)** — 사상가 DB의 일반 원칙이 '철학·윤리 사상가'라면 교과교육 실천가 등록은 사용자 판단 영역이나, 임용시험 교과교육학 단골 출제를 고려하면 `coombs`·`raths`·`oliver_donald` 등을 교과교육 실천가 카테고리로 별도 등록 검토 가치 있음. 대체 방안: `coombs` 단독 등록 대신 coverage/curriculum 참조용 경로로만 기록.
- 영향: Q5 ㉠·㉡ 정답은 trademark 3중 일치로 확정됨(교과서 표준). ㉢ 검사 명칭은 BLK-175E-2024A-003 참조. coverage/2024-A.md Q5 본문은 정확하며 DB 등록 여부는 교과교육 실천가 범위 정책 판단.

### BLK-175E-2024A-002 (TASK-175E-2024-A) — Q6 (나) 다르시아 나바에즈(Darcia Narvaez) ES 미등록 (**3회 재출제 확증 — 2026-B Q4 을 갱신**)
- 일시: 2026-04-21 (최초 등록) · 2026-04-21 TASK-175E-2026-B 작업 시 갱신
- 위치: `projects/ethics-study/exam-solutions/coverage/2024-A.md` Q6 row (나) + `projects/ethics-study/exam-solutions/coverage/2026-B.md` Q4 row (을)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 현대 도덕심리학·신콜버그주의 계승자, **2016-A Q9 + 2024-A Q6 + 2026-B Q4 재출제 3회 확증 — 최우선 등록 격상**)

**2026-B Q4 갱신 (2026-04-21, TASK-175E-2026-B 작업 시)**:
- 2026-B Q4 (나) 원문(L80-L83): "**도덕 스키마 … 인습 이후 사고 수준 … 공동의 도덕성(common morality) … 자동적·직관적 과정**" trademark로 **narvaez** 재확증.
- coverage/2026-B.md Q4 row (을) 에 `narvaez` MISS + BLK-175E-2024A-002 누적 갱신 주석 추가.
- 2024-A Q6 + 2026-B Q4 = **2년 간격 재출제** (2년 주기). 2016-A까지 포함하면 **3회 누적**으로 ES 등록 최우선도 격상.
- `ethics-thinkers` MISS 상태 지속.

- 사유: Q6 (나) (L107) 제시문 중심 사상가 **다르시아 나바에즈(Darcia Narvaez, 1952~, 미국 노터데임대 도덕심리학자, 신콜버그주의 계승, 도덕 전문가(moral expert) 연구의 정점)**의 canonical thinker_id가 ES 미등록. `narvaez`·`darcia_narvaez`·`darcia` 모두 MISS. **기존 블로커 BLK-175E-2016A-004와 동일 사상가 — 2회 재출제 관측**으로 신규 등록 우선순위 **최우선 격상**. Trademark 3중 일치: ① "**도덕성의 근저에 자리하는 세 가지 정향은 안전, 관여, 상상의 윤리**"(L107) — 나바에즈 **삼원 윤리 이론(Triune Ethics Theory / Triune Ethics Meta-Theory)** trademark. 저서 **『Neurobiology and the Development of Human Morality: Evolution, Culture, and Wisdom(2014)』**에서 체계화. Paul D. MacLean의 **삼원뇌(triune brain)** 이론(파충류뇌/포유류뇌/신피질)을 도덕 정향으로 확장 — **안전(safety, 자기보존·자기이익)·관여(engagement, 타인과의 친밀 관계·공감)·상상(imagination, 숙고적 이성 능력)**. 사전 힌트 "hoffman 4연속 가능성"과 무관하게 원문 직독으로 나바에즈 고유명 trademark 확정; ② "**안전 윤리는 자기와 자기의 이익 … 관여 윤리는 공감을 기초로 … 자기조절체계에 의해 두 가지 상태 … 공감이 강하지만 자기 규제적 시스템이 약할 때 … 타인에 대한 넘치는 애착 혹은 배려로 인해 마음이 불편한 상태**"(L107) — 나바에즈 trademark **관여 윤리의 두 양태**: 균형 상태(공감적 배려, engagement care)와 자기규제 실패 상태(**관여 궁박 engagement distress / 공감적 고통 empathic distress**). 호프만(Martin Hoffman)의 공감 과잉(empathic over-arousal) 개념을 수용하되 신경생물학적 자기규제 시스템 틀로 재개념화; ③ "**상상 윤리는 숙고적 이성 능력을 활용하여 안전 윤리의 충동과 관여 윤리의 직관에 반응하여 그것들을 조정 … 가장 모범적인 도덕적 정향은 ( ㉣ )**"(L107) — 나바에즈 **상상 윤리(ethic of imagination)** trademark. 신피질(neocortex) 기반 숙고적 이성이 안전 충동·관여 직관을 조정하고 **공동체적 상상(communal imagination)·적응적 윤리적 상상(adaptive ethical imagination)**으로 확장하는 도덕 전문가(moral expert)의 성숙 정향. 답: ㉠ = **자기(self)**, ㉢ = **관여 궁박/공감적 고통**, ㉣ = **상상의 윤리**.
- 후속 조치: TASK-176 범위에서 `narvaez` 신규 등록 **최우선** — **삼원 윤리 이론(Triune Ethics Theory)·삼원 윤리 메타이론(Triune Ethics Meta-Theory)**·**안전 윤리(ethic of safety)·관여 윤리(ethic of engagement)·상상 윤리(ethic of imagination)**·**Paul MacLean 삼원뇌(triune brain) 이론의 도덕심리학적 확장**·**『Neurobiology and the Development of Human Morality: Evolution, Culture, and Wisdom(2014)』**·**『Embodied Morality: Protectionism, Engagement and Imagination(2016)』**·**『Basic Needs, Wellbeing and Morality: Fulfilling Human Potential(2018)』**·**도덕 전문가(moral expert) 연구 — 4단계 도덕 기능 모형(Four Component Model) 계승**·**레스트(James Rest) 『Postconventional Moral Thinking(1999)』 공저**·**신콜버그주의(Neo-Kohlbergian) 대표자**·**레스트·토마·베베우·나바에즈(Rest·Thoma·Bebeau·Narvaez) 미네소타 그룹**·**DIT-2(Defining Issues Test) 개발·연구**·**통합 윤리 교육(Integrative Ethical Education, IEE) — 탁월성 윤리 교육·발달을 위한 공동체 지원 모형**·**공감적 각성(empathic arousal)·공감적 고통(empathic distress)·관여 궁박(engagement distress) 개념**·**진화론적 도덕 발달 — 진화된 발달 환경(Evolved Developmental Niche, EDN)**·**애착 기반 양육과 도덕 발달의 신경생물학적 토대**·**호프만 공감 이론과의 연결·차별화**·콜버그 인지 발달론의 도덕 정의적·신경생물학적 확장·**부모 양육·문화적 환경과 도덕 전문가 육성 모형**·2022 개정 도덕과 교육과정 인격·덕 통합 접근 맥락. 후보 id: `narvaez`. 등록 우선순위 **최우선** (2016-A Q9 + 2024-A Q6 = **누적 2회 재출제 확증**, 차기 시험 재출제 가능성 상위, 신콜버그주의·현대 도덕심리학 대표 사상가. BLK-175E-2016A-004와 병합 처리 필요 — TASK-176에서 단일 사상가 단일 등록으로 해결).
- 영향: Q6 (나) 정답 ㉠(자기)·㉢(관여 궁박/공감적 고통)·㉣(상상의 윤리)은 trademark 3중 일치로 확정됨. coverage/2024-A.md Q6 본문 내용은 정확하며 ES 커버리지 공백만 존재. **재출제 경계 리스트 갱신 — `narvaez` 2연속 신규 등극**.

### BLK-175E-2024A-003 (TASK-175E-2024-A) — Q5 ㉢ 검사 명칭 교과서 표준 용어 확인 필요
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2024-A.md` Q5 ㉢ (L93)
- 심각도: observation (정답 후보 확정되어 있으나 교과서 표준 용어 확정 필요 — 교과교육학 용어 표준화 영역)
- 사유: Q5 ㉢ 교사 발화 "**사람들은 평가는 공정해야 한다고 생각합니다. 평가의 공정성이 친분에 의해 훼손되어서는 안 됩니다. 무임승차를 알려야만 공정한 평가가 이루어지는 것 아닌가요?**"(L93)는 쿰스·뮉스 가치갈등해결 수업모형 4단계 **가치 원리 검사(value principle testing)**의 하위 기법 중 어디에 해당하는지 정밀 판정이 필요하다. 4가지 표준 하위 검사 분석: (a) **역할 교환 검사(role exchange test)**: 학생이 상대방 입장이 되면 어떻게 느낄지 묻는 것 — **미해당** (교사가 학생에게 상대방 입장을 묻지 않음); (b) **포섭 검사(subsumption test)**: 학생의 잠정 원리가 더 일반적·상위 원리에 부합하는지 묻는 것 — **해당** (교사가 "평가의 공정성"이라는 상위 원리로 학생의 "친분 우선" 결정을 포섭·재검토시킴); (c) **새로운 사례 검사(new cases test)**: 다른 사례·상황을 제시해 같은 원리가 유지되는지 보는 것 — **미해당** (새 사례 제시 없음); (d) **경고 검사(warning test / casuistry test)**: 학생이 결정을 고수할 경우 발생할 수 있는 결과·예외 사례·사회적 파급을 경고·환기하는 것 — **부분 해당** ("무임승차를 알려야만 공정한 평가가 이루어진다"는 발화가 학생의 결정이 공정성을 훼손하는 결과를 경고하는 측면). 발화 구조는 상위 보편 원리("평가의 공정성") 도입을 통한 잠정 결정 재검토가 핵심이므로 **포섭 검사(subsumption test)가 최유력 정답**이며, 경고 검사는 보조적 특성. 2022 개정 도덕과 교육과정 해설서 및 중등 도덕과 교수·학습 자료에서 표준 용어 확인 시 교과서 판정 유력 정답이 **포섭 검사**로 최종 확정될지 또는 **경고 검사**로 대체될지 확정 필요.
- 후속 조치: Manager 및 사용자가 2022 개정 도덕과 교육과정 해설서·국정 도덕 교과서(중학교·고등학교 도덕)·중등 도덕과 교수·학습 자료 중 '쿰스 가치갈등해결 수업모형 4단계 하위 검사' 항목에서 해당 발화 유형이 **포섭 검사** 또는 **경고 검사** 중 어느 것으로 규정되는지 교차 확인 필요. 본 coverage는 **포섭 검사를 유력 정답, 경고 검사를 대체 후보로 병기**하여 서술하였으며, 확인 결과에 따라 단일 정답 확정 시 Q5 ㉢ 서술 갱신.
- 영향: Q5 ㉢ 답안 서술에서 "포섭 검사(유력) / 경고 검사(대체 후보)" 병기 방식 채택. 정답 판정 자체는 보류 없이 완료되어 있으나, 교과서 기준 표준 용어 확정은 2022 개정 도덕과 교육과정 해설서 참조 시 해결 가능. 본 블로커는 교과교육학 용어 표준화의 영역으로, 사상가 DB 등록 영역과는 무관하며 TASK-176 범위 밖.

### BLK-175E-2024A-004 (TASK-175E-2024-A) — Q7 갑 한국 성리학자 고유명 특정 미달
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2024-A.md` Q7 row (갑)
- 심각도: observation (빈칸 정답 ㉡=정·㉢=의는 확정, 갑 사상가 고유명 미확정은 창작 금지 원칙 준수 결과)
- 사유: Q7 갑 (L124-L125) 제시문은 **한국 성리학(조선 주자학) 공통 프레임** — "성=천리=순선 / 악=기품·물욕 / 심성정의(心性情意) 4단 구조 / 심통성정(心統性情) / 의→정 지휘 구조" — 이며, 주희(朱熹)·퇴계(退溪) 이황·율곡(栗谷) 이이·한원진(韓元震) 등 다수 성리학자 간 trademark 3중 일치가 안 된다. 발문 "한국 윤리 사상가"에 따라 주희는 배제되며 조선 성리학자 중 한 명으로 좁혀지나, 제시문 명제가 모두 **주자학 공통 명제**(특정 사상가의 고유 학설이 아님)이므로 퇴계·율곡 중 누구인지 trademark 수준으로 특정 불가. Phase 6 규칙 "창작 금지 — 사상가 특정 미달 시 BLOCKER 등록"에 따라 갑 = "한국 성리학(조선 주자학) 계열 [사상가 특정 미달]"로 분류. 빈칸 정답 ㉡=**정(情, 심의 발동)**·㉢=**의(意, 정을 헤아리는 뜻·의지)**는 주자학 심성정의 구조에서 고유명과 독립적으로 확정됨(주자 『주자어류』·『성리대전』·퇴계 『성학십도』·율곡 『성학집요』 공통 명제). 또한 "심은 성을 다 발휘할 수 있으나 성은 심을 단속할 수 없고, 의는 정을 움직일 수 있으나 정은 의를 움직일 수 없다"의 서열 구조는 **심통성정(心統性情)**의 전형적 표현이며, 수양론상 **성의(誠意)·정심(正心)** 공부를 강조하는 주자학 수양론의 공통 기반. 을(정약용)과의 대비 구도에서 "주자학 성즉리 비판의 대상이 되는 조선 성리학자"라는 관점에서 보면 시험 출제진의 의도는 **율곡** 또는 **퇴계** 중 어느 한 명일 가능성이 높으나, 제시문만으로는 단일 사상가 고유명 trademark 3중 일치가 성립하지 않는다.
- 후속 조치: (a) 2024학년도 중등임용 1차 도덕·윤리 공식 정답 해설 확인 또는 한국교육과정평가원 출제 의도 자료 확인 시 갑 사상가 고유명이 공개될 경우 coverage/2024-A.md Q7 갑 분류를 해당 사상가로 갱신 (퇴계 → `toegye`, 율곡 → `yulgok`). (b) Phase 6 방침 "창작 금지 — 사상가 특정 미달은 BLOCKER로 유지"에 따라, 공식 정답 확인 없이는 추정 고유명을 부여하지 않는다. (c) 빈칸 정답 ㉡=정·㉢=의, ㉠에 대한 을의 비판, ㉥의 이유는 모두 고유명과 무관하게 확정되어 있으므로 **점수 해설상 영향 없음**.
- 영향: Q7 갑 제시문의 빈칸·서술 정답은 확정되어 있으며, 갑 사상가 고유명만 미특정. 이는 제시문 자체가 주자학 공통 명제라는 구조적 특성에서 기인하며, 창작 금지 원칙 준수의 결과. ES 신규 등록 대상 없음(퇴계·율곡·한원진은 이미 등록 완료된 한국 성리학자 표준 사상가).

### BLK-175E-2024A-005 (TASK-175E-2024-A) — Q8 갑 법장(法藏, Fazang) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2024-A.md` Q8 row (갑)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 중국 화엄종 체계화 정점, 동아시아 불교 화엄 사상 대표자)
- 사유: Q8 갑 (L144-L145) 제시문 중심 사상가 **법장(法藏, Fazang, 643-712, 당나라 화엄종 3조, 현수 대사(賢首大師))**의 canonical thinker_id가 ES 미등록. `fazang`·`法藏`·`beopjang`·`hyeonsu` 모두 MISS. Trademark 3중 일치: ① "**온 우주는 일심(一心)에 통괄**되며, 일심에 통괄되는 것을 **현상[事]과 본체[理]의 양면으로 관찰**하면 **네 가지 범주**로 파악할 수 있다. 첫째는 이 세계를 **차별이 있는 현상의 세계**로 보는 것 … 둘째는 이 세계의 다양한 현상이 **실제로는 동일한 원리**라고 보는 것 … 셋째는 **현상과 본체가 서로 걸림이 없는 관계** 속에 있다고 보는 것 … 넷째는 ( ㉠ )"(L144) — 법장 **사법계관(四法界觀)** trademark: **사법계(事法界) · 이법계(理法界) · 이사무애법계(理事無礙法界) · 사사무애법계(事事無礙法界)**. 『화엄경탐현기(華嚴經探玄記)』·『화엄오교장(華嚴五敎章)』·「화엄법계관문(華嚴法界觀門)」에서 확립된 화엄종 궁극 세계관. ㉠ = **사사무애법계(事事無礙法界) — 상즉상입(相卽相入)·일즉다 다즉일(一卽多 多卽一)·인드라망(因陀羅網)**; ② "**일심에 두 문이 있는데, 무엇이 그 둘인가? 첫째는 진여문(眞如門)이고, 둘째는 생멸문(生滅門)이니, 이 두 문이 모두 각각 일체의 법을 총괄하고 있다. 왜 그러한가? 이 두 문이 서로를 여의지 않기 때문이다**"(L145) — 마명(馬鳴, Aśvaghoṣa) **『대승기신론(大乘起信論)』** 「입의분(立義分)」 원문 trademark 직접 인용: "依一心法有二種門 云何爲二 一者心眞如門 二者心生滅門 是二種門皆各總攝一切法 此義云何 以是二門不相離故". 법장은 **『대승기신론의기(大乘起信論義記)』** — 중국 화엄종의 기신론 주석서 대표작 — 에서 이 구조를 주석. 기신론 주석 전통에서 법장의 『의기』는 원효의 『대승기신론소』와 쌍벽을 이루는 동아시아 불교 기신론 해석의 정점; ③ **화엄 사법계관 + 일심이문 양립 체계**는 법장 화엄 사상의 trademark. 을(원효)과의 비교에서 원효는 일심이문 + 여래장 + 화쟁 구조로 전개하는 반면, 갑(법장)은 화엄 사법계관 + 일심이문 병용 구조로 전개 — 두 사상가의 동시 출제는 중국 화엄종과 한국 해동 기신론 전통의 대비를 드러내는 전형적 교과서 출제 패턴.
- 후속 조치: TASK-176 범위에서 `fazang` 신규 등록 + claim 작성 — **중국 화엄종(華嚴宗, Huayan school) 3조 — 현수 대사(賢首大師), 체계화 정점**·**두순(杜順, 화엄종 1조)·지엄(智儼, 화엄종 2조)의 계승자**·**청량 징관(澄觀, 화엄종 4조)·규봉 종밀(圭峰 宗密, 화엄종 5조)의 선구**·**사법계관(四法界觀) — 사법계·이법계·이사무애법계·사사무애법계**·**십현문(十玄門, ten profound gates) — 사사무애법계의 구체적 전개 도식: 동시구족상응문·광협자재무애문·일다상용부동문·제법상즉자재문·은밀현료구성문·미세상용안립문·인다라망경계문·탁사현법생해문·십세격법이성문·주반원명구덕문**·**육상원융(六相圓融, six characteristics): 총상(總相)·별상(別相)·동상(同相)·이상(異相)·성상(成相)·괴상(壞相)**·**일즉다 다즉일(一卽多 多卽一, one is all, all is one)**·**상즉상입(相卽相入, mutual identity and mutual penetration)**·**해인삼매(海印三昧, ocean-seal samādhi)**·**인드라망(因陀羅網, Indra's net) 비유**·**『화엄경탐현기(華嚴經探玄記, Exploration of Mysteries of Huayan Sūtra)』 20권 — 신역 화엄경 대표 주석**·**『화엄오교장(華嚴五敎章, Treatise on the Five Teachings of Huayan)』 — 소승·대승시교·대승종교·대승돈교·원교(화엄)의 5단 교판**·**「화엄법계관문(華嚴法界觀門)」 — 두순의 삼중관(三重觀)을 사법계관으로 확장**·**『대승기신론의기(大乘起信論義記)』 — 기신론 주석의 동아시아 표준**·**『금사자장(金師子章, Treatise on the Golden Lion)』 — 측천무후를 위해 금사자 비유로 화엄 교리 해설**·**『화엄경문답(華嚴經問答)』**·**『십이문론소(十二門論疏)』**·**신역 『화엄경(80권본, Avataṃsaka Sūtra)』의 번역 감독·주역**·**측천무후(武則天)의 국사(國師) — 당 화엄종의 국가적 후원**·**현장 유식의 별교(권교) 비판·화엄 원교의 궁극성 주장**·**한국 의상(義湘) 화엄(화엄 1조 지엄 문하 동문)·원효 화엄 수용과의 관계**·**일본 화엄종(도다이지 전통)의 동원(東源)**·**티벳 불교·선종과의 교류**·천태 지의(天台 智顗)의 성구설(性具說)·오시팔교(五時八敎)와의 비교·**『육십화엄(六十華嚴)』·『팔십화엄(八十華嚴)』·『사십화엄(四十華嚴)』 번역 전통**·**진여연기(眞如緣起)·법계연기(法界緣起)설**. 후보 id: `fazang`. 등록 우선순위 **최우선** (동아시아 불교 화엄 사상의 체계화 정점, 원효와 함께 기신론 주석 전통의 양대 축, 교과서 단골 출제 — 화엄 사법계관·십현문·상즉상입·일즉다 다즉일은 고등 윤리·동양 사상 표준 개념).
- 영향: Q8 갑 정답 ㉠(사사무애법계)·㉡·㉢ 관계 공통 주장(일심의 두 문 상호 불리)·㉤ 관련 서술은 trademark 3중 일치로 확정됨. coverage/2024-A.md Q8 본문 내용은 정확하며 ES 커버리지 공백만 존재. `wonhyo`는 HIT로 을 사상가 등록 완료된 상태이므로, `fazang` 신규 등록 시 중국-한국 화엄 대비 구도 ES 커버리지 완성.

### BLK-175E-2024B-001 (TASK-175E-2024-B) — Q3 (을) 엘리엇 튜리엘(Elliot Turiel) ES 미등록 (4회째 출제)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2024-B.md` Q3 row (을)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 현대 도덕심리학 영역 이론 창시자, **총 4회 출제 (2018-B·2021-B·2022-A·2024-B; 2022-B·2023-A·2023-B·2024-A 4회 단절 후 단발 재등장), 최장 기출 이력 보유 재출제 경계 대상**)
- 사유: Q3 (L48) 제시문 중심 사상가 **엘리엇 튜리엘(Elliot Turiel, 1938~, 미국 UC 버클리대 도덕심리학자, 사회 인지 영역 이론(Social Cognitive Domain Theory) 창시자)**의 canonical thinker_id가 ES 미등록. `turiel` MISS. 기존 기출 3회(2018-B·2021-B·2022-A — coverage grep 실증)에 이어 **2024-B Q3 재출제 확증 — 총 4회 출제 (2022-B/2023-A/2023-B/2024-A 4회 연속 단절 후 단발 재등장)**. Trademark 3중 일치: ① "**도덕 영역은 사회 조직들 간의 상호작용에 의하여 형성되는 인습 등에 대한 판단과 구분되어야 한다**"(L48) — 튜리엘 **영역 이론(Domain Theory)** trademark: **도덕 영역(moral domain)**은 정의·복지·권리에 관한 규범으로, 사회 조직 독립적·보편적·객관적 성격을 가지며, 사회 인습 영역(인습·관례)과 본질적으로 구분된다. 저서 『The Development of Social Knowledge: Morality and Convention(1983)』·『The Culture of Morality: Social Development, Context, and Conflict(2002)』; ② "**사회 인습 영역은 사회 조직 혹은 체계 안에서 구성원 간에 합의된 행동으로 정의**"(L48) — 튜리엘 **사회 인습 영역(social conventional domain)** trademark 정의: 특정 사회 체계 내 구성원들의 합의에 의해 규정되는 관습·의례·규범으로, 사회 체계 의존적·상대적·합의적 성격을 가짐. 도덕 영역과 달리 사회별로 변동 가능하며, 정의·복지·권리의 보편적 요구와 구분됨; ③ "**개인적 영역에 대한 판단 기준 역시 도덕 영역 혹은 인습 영역에 대한 판단 기준과 다르다**"(L48) — 튜리엘 **3영역 구분(three-domain distinction)** trademark 완성: **도덕 영역 / 사회 인습 영역 / 개인적 영역(personal domain)**. 개인적 영역은 개인의 사적 선택·취향·자율성의 영역으로, 외부 규제 대상이 되어서는 안 되는 자기결정 영역. 튜리엘은 아동이 발달 초기부터 이 3영역을 구분할 수 있음을 경험적으로 입증하며, 콜버그의 단계적·보편적 발달 이론(도덕과 인습을 단일 발달 계열에 편입)을 비판. 콜버그가 3수준 6단계에서 인습 수준(3·4단계)과 후인습 수준(5·6단계)을 동일 도덕 발달 계열로 다룬 것은 도덕과 인습의 영역적 구분을 간과한 결과라는 영역 이론의 핵심 비판.
- 후속 조치: TASK-176 범위에서 `turiel` 신규 등록 **최상위 우선** (총 4회 출제 기출 이력, 단절 후 재등장 패턴이지만 차기 시험 재출제 확률 상위) — **사회 인지 영역 이론(Social Cognitive Domain Theory)** · **도덕 영역(moral domain) / 사회 인습 영역(social conventional domain) / 개인적 영역(personal domain) 3영역 구분** · **콜버그 단계 이론 비판 — 도덕과 인습의 영역적 구분 간과** · **『The Development of Social Knowledge: Morality and Convention(1983)』** · **『The Culture of Morality: Social Development, Context, and Conflict(2002)』** · **『The Development of Morality(2006, Handbook of Child Psychology)』** · **Nucci, Smetana 와의 공동 연구 — 영역 이론 실험 연구** · **아동의 도덕/인습 구분 능력 — 발달 초기부터 존재** · **도덕 판단의 보편성·불변성 vs 인습 판단의 상대성·가변성** · **개인적 영역의 자기결정 — 도덕적 권위 개입 금지** · **신콜버그주의·해방적 도덕교육 논쟁에서의 위치** · **문화 상대주의와 도덕 보편주의 간 매개 이론**. 후보 id: `turiel`. 등록 우선순위 **최상위 (총 4회 출제 기출 이력)** — `narvaez`(2회)·`jinul`(3연속)과 비교해 **최다 누적 출제 미등록 사상가**.
- 영향: Q3 (을) 정답 trademark 3중 일치로 확정됨 — 영역 이론·3영역 구분·콜버그 비판. coverage/2024-B.md Q3 본문은 정확하며 ES 커버리지 공백만 존재. **재출제 경계 리스트 최상단 갱신 — `turiel` 총 4회 출제 확정 (2018-B·2021-B·2022-A·2024-B)**.

### BLK-175E-2024B-002 (TASK-175E-2024-B) — Q4 (가) 에밀 뒤르켐(Émile Durkheim) ES 미등록 (4회째 출제)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2024-B.md` Q4 row (가)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 현대 사회학·사회학적 도덕교육의 정초자, **총 4회 출제 (2015-B·2021-B·2022-B·2024-B; 2023-A·2023-B·2024-A 3회 단절 후 단발 재등장)**)
- 사유: Q4 (L63) 제시문 중심 사상가 **에밀 뒤르켐(Émile Durkheim, 1858-1917, 프랑스 사회학자, 사회학적 도덕교육론 정초자, 『도덕교육론(L'éducation morale, 1925)』 저자)**의 canonical thinker_id가 ES 미등록. `durkheim` MISS. 기존 기출 3회(2015-B·2021-B·2022-B — coverage grep 실증, 2021-B→2022-B 2연속 포함)에 이어 **2024-B Q4 재출제 확증 — 총 4회 출제 (2023-A/2023-B/2024-A 3회 연속 단절 후 단발 재등장)**. Trademark 3중 일치: ① "**( ㉠ 사회 )은/는 도덕성의 근원이다. 도덕성은 인간의 행위를 미리 결정해 주는 용인된 규칙들의 체계**"(L63) — 뒤르켐 『L'éducation morale(1925, 유고, Mauss 편집)』 제1부 「사회와 도덕성」 trademark: **도덕은 사회(société)에 근원을 두며 사회가 제공하는 행위 규칙의 체계다**. 도덕은 개인의 의식이 아닌 **집합의식(conscience collective)·사회적 사실(fait social)**에 근거한다는 사회학적 도덕관의 핵심. 『사회분업론(De la division du travail social, 1893)』·『사회학적 방법의 규칙(Les règles de la méthode sociologique, 1895)』·『자살론(Le suicide, 1897)』에서 체계화된 입장; ② "**도덕성의 구성요소는 규율정신, 집단에 대한 애착, ㉡ 자율성**"(L63) — 뒤르켐 **도덕성의 3요소(three elements of morality)** trademark 정확 일치: **(1) 규율 정신(l'esprit de discipline — spirit of discipline) — 규칙성 선호 + 권위 존중; (2) 집단 애착(l'attachement aux groupes sociaux — attachment to groups) — 사회 집단의 이익 관점에서 행동; (3) 자율성(l'autonomie — autonomy) — 도덕 규칙의 과학적·합리적 이해**. 『L'éducation morale』의 체계 구성; ③ "**규율정신은 도덕 규칙을 일관성 있게 준수하는 행위자의 성향인 규칙성에 대한 선호와 ( ㉢ 권위 )에 대한 존중 … 집단 애착은 ( ㉠ 사회 ) 집단의 이익이라는 관점에서 행동**"(L63) — 뒤르켐 **규율 정신 정의** trademark: 도덕 규칙은 개인에게 **외적·선행적·강제적 권위(autorité)**로 작용하며, 이 권위에 대한 존중이 도덕적 주체 형성의 핵심. 칸트의 개인 이성 기반 자율성과 달리 뒤르켐의 자율성은 **사회 규범의 사회학적 이해에 기초한 자유로운 수용**을 의미.
- 후속 조치: TASK-176 범위에서 `durkheim` 신규 등록 **최우선** — **사회학적 도덕교육(sociological moral education)** · **도덕성 3요소: 규율 정신(규칙성 선호 + 권위 존중) + 집단 애착(사회 집단의 이익 관점) + 자율성(도덕 규칙의 과학적 이해)** · **집합의식(conscience collective)** · **사회적 사실(fait social)** · **기계적 연대(solidarité mécanique) / 유기적 연대(solidarité organique)** · **아노미(anomie) — 규범 부재 상태** · **세속적 도덕(laïcité) — 종교적 초월 기초 없는 도덕 가능성** · **『사회분업론(De la division du travail social, 1893)』** · **『사회학적 방법의 규칙(Les règles de la méthode sociologique, 1895)』** · **『자살론(Le suicide, 1897)』 — 이기적·이타적·아노미적·숙명적 자살 4유형** · **『종교생활의 원초적 형태(Les formes élémentaires de la vie religieuse, 1912)』 — 종교의 사회적 기원** · **『도덕교육론(L'éducation morale, 1925, 유고)』 — 도덕교육의 3요소 + 세속 도덕 교육론** · **프랑스 제3공화국 세속 공화주의 도덕교육 설계자** · **실증주의 사회학 전통(콩트 계승)** · **베버·짐멜과 함께 고전 사회학 3대 거장** · **파슨스·머턴 구조기능주의의 원천** · **피아제·콜버그의 도덕심리학이 비판·계승하는 대상 — 피아제는 도덕의 사회적 근원은 인정하되 발달적 내면화 과정을 추가, 콜버그는 후인습 단계에서 사회 규범을 넘어서는 원리 지향 추구**. 후보 id: `durkheim`. 등록 우선순위 **최우선** (총 4회 출제 기출 이력, 사회학적 도덕교육 전통의 정초자, 임용시험 필수 출제 사상가, 피아제·콜버그 도덕심리학과 함께 현대 도덕교육 이론 3대 축 — `piaget`·`kohlberg`는 HIT인데 `durkheim`만 MISS인 상태는 현대 도덕교육 이론 ES 커버리지의 구조적 공백).
- 영향: Q4 (가) 정답 ㉠(사회)·㉢(권위)·㉡(자율성) 의미 서술은 trademark 3중 일치로 확정됨. coverage/2024-B.md Q4 본문은 정확하며 ES 커버리지 공백만 존재. **재출제 경계 리스트 갱신 — `durkheim` 총 4회 출제 확정 (2015-B·2021-B·2022-B·2024-B)**.

### BLK-175E-2024B-003 (TASK-175E-2024-B) — Q5 (갑) 아우구스토 블라시(Augusto Blasi) ES 미등록 (5회째 출제)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2024-B.md` Q5 row (갑)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 현대 도덕심리학 도덕적 정체성·자기 일관성 모형 대표, **총 5회 출제 (2017-A·2019-B·2021-A·2023-A·2024-B; 2023-A→2024-B 2연속 포함 최다 출제)**)
- 사유: Q5 (L80) 제시문 중심 사상가 **아우구스토 블라시(Augusto Blasi, 1932-2014, 미국 매사추세츠 보스턴대 도덕심리학자, 도덕적 정체성·도덕적 인격 모형의 정점)**의 canonical thinker_id가 ES 미등록. `blasi` MISS. 기존 기출 4회(2017-A·2019-B·2021-A·2023-A — coverage grep 실증)에 이어 **2024-B Q5 재출제 확증 — 총 5회 출제 (2023-A→2024-B 2연속)**. Trademark 3중 일치: ① "**도덕적 인격을 구성하는 3가지 요소는 도덕적 욕망, 의지력, ( ㉠ 통합성 )**"(L80) — 블라시 **도덕적 인격 3요소(three constituents of moral character)** trademark 정확 일치: (a) **도덕적 욕망(moral desires)** — 도덕적 가치와 이상에 대한 동기적 헌신, (b) **의지력(willpower)** — 자기 통제·일관성 유지의 메타인지 능력, (c) **통합성(integrity)** — 자신의 신념·가치·행동의 일치를 유지하려는 자기 구성적 동기. 논문 「Moral Character: A Psychological Approach(2005)」(Lapsley & Narvaez 편집 Moral Development, Self, and Identity 수록); ② "**( ㉠ 통합성 )은/는 개인이 선택한 신념과 일치하는 것으로서 자아감을 구성하는 구체적인 신념들과 일치하여 유지되기를 원하는 특정한 동기 … 가장 높은 수준의 ( ㉠ )와/과 본질적으로 연관된 도덕적 정체성 … 자신을 고결하고 때 묻지 않은 상태로 유지**"(L80) — 블라시 **도덕적 정체성(moral identity)** + **자기 일관성(self-consistency)** trademark. 논문 「Moral Functioning: Moral Understanding and Personality(2004)」·「The Self and the Management of the Moral Life(1993)」에서 체계화: 도덕적 정체성이란 도덕적 가치·이상이 자아감(sense of self) 구성의 핵심 요소가 되어 **자기 일관성 동기(motivation for self-consistency)**가 도덕적 행동을 자연스럽게 유도하는 상태; ③ "㉡ **자신의 중심 가치들과 모순되는 부정적 행동은 선택될 수 없다**"(L80) — 블라시 **심리적 불가능성(psychological impossibility)** trademark: 강한 도덕적 정체성을 가진 사람에게서 중심 가치에 반하는 행동은 **선택지 자체로 고려되지 않는 unthinkable action**이 된다. 이는 콜버그 후기 이론의 **도덕 판단 → 도덕 행동** 간극 문제(judgment-action gap)를 블라시가 **도덕적 정체성 모형**으로 메우려는 시도의 핵심.
- 후속 조치: TASK-176 범위에서 `blasi` 신규 등록 **최우선** (총 5회 출제 기출 이력 — 2023-A→2024-B 2연속 재출제 포함, 본 태스크 ES MISS 6인 중 최다 누적 출제) — **도덕적 정체성(moral identity)** · **도덕적 인격 3요소: 도덕적 욕망·의지력·통합성** · **자기 일관성 동기(motivation for self-consistency)** · **자기 모형(self-model) / 자아 모형(model of self)** · **도덕적 책임(moral responsibility) 귀속의 자기 모형 기반** · **심리적 불가능성(psychological impossibility) — 중심 가치에 반하는 행동의 선택 불가** · **의지적 행위(willful action) 철학** · **judgment-action gap 문제의 해결 시도 — 인지 발달 + 인격 발달의 통합** · **콜버그 후기 이론·신콜버그주의와의 관계** · **논문 「Bridging Moral Cognition and Moral Action: A Critical Review of the Literature(1980)」**·**「Moral Identity: Its Role in Moral Functioning(1984)」**·**「The Self and the Management of the Moral Life(1993)」**·**「Moral Functioning: Moral Understanding and Personality(2004)」**·**「Moral Character: A Psychological Approach(2005)」** · **Lapsley·Narvaez 편집 『Moral Development, Self, and Identity(2004)』 · 『Character Psychology and Character Education(2005)』 공저** · **덕 윤리 심리학(virtue ethics psychology) 부흥의 핵심 인물** · **Hardy·Carlo·Aquino·Reed 등 후속 도덕적 정체성 연구자의 직접 영향**. 후보 id: `blasi`. 등록 우선순위 **최우선 (총 5회 출제 최다 — `narvaez` 2회·`turiel` 4회와 비교해 최다 누적 출제)**.
- 영향: Q5 (갑) 정답 ㉠(통합성)·㉡(중심 가치 모순 행동의 선택 불가 이유) 서술은 trademark 3중 일치로 확정됨. coverage/2024-B.md Q5 본문은 정확하며 ES 커버리지 공백만 존재. **재출제 경계 리스트 갱신 — `blasi` 총 5회 출제 확정 (2017-A·2019-B·2021-A·2023-A·2024-B, 2023-A→2024-B 2연속)**.

### BLK-175E-2024B-004 (TASK-175E-2024-B) — Q5 (을) 앨버트 밴듀라(Albert Bandura) ES 미등록 (4회째 출제)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2024-B.md` Q5 row (을)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 사회인지 이론·도덕적 이탈 이론 창시자, 20세기 심리학의 대표 거장, **총 4회 출제 (2014-A·2019-A·2020-A·2024-B; 2021-A~2024-A 4년 단절 후 단발 재등장)**)
- 사유: Q5 (L82) 제시문 중심 사상가 **앨버트 밴듀라(Albert Bandura, 1925-2021, 캐나다계 미국 스탠퍼드대 심리학자, 사회인지 이론(Social Cognitive Theory)과 도덕적 이탈 이론(Moral Disengagement Theory)의 창시자, 자기효능감(self-efficacy) 개념의 창안자)**의 canonical thinker_id가 ES 미등록. `bandura` MISS. 기존 기출 3회(2014-A·2019-A·2020-A — coverage grep 실증)에 이어 **2024-B Q5 재출제 확증 — 총 4회 출제 (2021-A~2024-A 4년 단절 후 단발 재등장)**. Trademark 3중 일치: ① "**사람들의 정체성을 이루는 구성요소에는 여러 가지가 있다. 이 구성요소 중 도덕성은 필수적이고 중요한 것으로 여겨진다. 따라서 일정 수준 이상의 도덕적 자아를 유지하려는 욕구는 개인의 전체 자아를 보존하려는 욕구의 한 부분이 된다**"(L82) — 밴듀라 **사회인지 이론(Social Cognitive Theory)** 틀에서의 **도덕적 자아(moral self)** trademark: 정체성은 다양한 구성요소로 이루어지며 도덕성은 그 필수 요소. 도덕적 자아는 전체 자아 보존 욕구의 하위 체계. 저서 『Social Foundations of Thought and Action: A Social Cognitive Theory(1986)』·『Self-Efficacy: The Exercise of Control(1997)』의 자아 개념 체계; ② "**자신을 구성하는 모든 정체성을 최적의 ( ㉢ 균형 ) 상태로 이끄는 선택이 무엇인지 따져보게 된다 … 자신이 행한 도덕적 행동의 역사에 기초하여 현재 자신의 도덕적 ( ㉢ 균형 )을/를 계산**"(L82) — 밴듀라 **도덕적 자기조절(moral self-regulation)** + **도덕적 균형(moral balance) / 도덕적 계좌(moral ledger)** trademark: 개인은 자기 도덕적 행동 역사를 누적적으로 계산하여 현재의 도덕적 잔고를 평가하고, 전체 자아의 최적 균형을 유지하는 선택을 함. 논문 「Social Cognitive Theory of Moral Thought and Action(1991)」·「Moral Disengagement in the Perpetration of Inhumanities(1999)」·「Selective Moral Disengagement in the Exercise of Moral Agency(2002)」; ③ "**'이렇게 행동해도 내가 원하는 유형의 도덕적인 사람으로 남아있을 수 있다면' 사람들은 ㉣ 도덕적 일탈 행동을 선택할 수 있다**"(L82) — 밴듀라 **도덕적 이탈(moral disengagement) / 도덕적 자기조절의 선택적 활성화(selective activation of moral self-regulation)** trademark. 『Moral Disengagement: How People Do Harm and Live with Themselves(2016)』에서 집대성한 **도덕적 이탈 8가지 메커니즘**: (a) 도덕적 정당화(moral justification), (b) 완곡한 표현(euphemistic labeling), (c) 유리한 비교(advantageous comparison), (d) 책임 전가(displacement of responsibility), (e) 책임 분산(diffusion of responsibility), (f) 결과 왜곡(distortion of consequences), (g) 비인간화(dehumanization), (h) 비난의 귀착(attribution of blame). 이 메커니즘들을 통해 도덕적 자기 제재를 선택적으로 해제하고 반도덕적 행동을 정당화하면서도 도덕적 자아상을 유지함.
- 후속 조치: TASK-176 범위에서 `bandura` 신규 등록 **최우선** — **사회인지 이론(Social Cognitive Theory)** · **삼자 상호 결정론(triadic reciprocal determinism) — 개인·행동·환경 상호작용** · **관찰 학습(observational learning) / 대리 학습(vicarious learning)** · **보보 인형 실험(Bobo doll experiment, 1961) — 공격성 모방 학습 입증** · **자기효능감(self-efficacy) — 주어진 상황에서 원하는 결과를 산출할 수 있다는 신념** · **자기조절(self-regulation) — 자기 관찰·자기 판단·자기 반응 3단계** · **도덕적 이탈(moral disengagement) 8가지 메커니즘** · **도덕적 자기 제재(moral self-sanctions)** · **대리 인간화(dehumanization)의 사회심리학** · **공격성 학습 이론(social learning theory of aggression)** · **행위 주체성(human agency) — 의도성·선견지명·자기반응성·자기성찰** · **『Social Learning Theory(1977)』** · **『Social Foundations of Thought and Action: A Social Cognitive Theory(1986)』** · **『Self-Efficacy: The Exercise of Control(1997)』** · **『Moral Disengagement: How People Do Harm and Live with Themselves(2016)』** · **20세기 심리학자 중 가장 많이 인용된 학자 중 한 명 (프로이트·스키너와 함께 3대)** · **도덕심리학에서 블라시(도덕적 정체성 강한 일관성 모형) vs 밴듀라(도덕적 자기조절의 선택적 작동 모형)** 대립 구도의 핵심 인물. 후보 id: `bandura`. 등록 우선순위 **최우선** (20세기 심리학 대표 거장, 도덕심리학 교과서 필수 사상가, 도덕적 이탈 이론은 현대 응용윤리·정치심리학·조직윤리에서도 광범위하게 활용).
- 영향: Q5 (을) 정답 ㉢(균형)·㉣(도덕적 일탈 행동)·을의 입장에서 갑 비판은 trademark 3중 일치로 확정됨. coverage/2024-B.md Q5 본문은 정확하며 ES 커버리지 공백만 존재. **블라시(도덕적 정체성) vs 밴듀라(도덕적 자기조절·이탈) 대립 구도는 현대 도덕심리학 교과서 비교 출제의 전형** — 2024-B가 이를 단일 문항에서 직접 대비시킨 최초 사례일 가능성.

### BLK-175E-2024B-005 (TASK-175E-2024-B) — Q8 (갑) 피터 싱어(Peter Singer) ES 미등록 (4회째 출제)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2024-B.md` Q8 row (갑)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 현대 응용윤리·동물 해방 운동의 정초자, **총 4회 출제 (2015-B·2019-B·2022-B·2024-B; 2023-A·2023-B·2024-A 3회 단절 후 단발 재등장)**)
- 사유: Q8 (L131) 제시문 중심 사상가 **피터 싱어(Peter Singer, 1946~, 호주계 미국 프린스턴대 생명윤리학 석좌교수, 공리주의 응용윤리·동물 해방 운동·효율적 이타주의(effective altruism) 운동의 정초자)**의 canonical thinker_id가 ES 미등록. `singer` MISS. 기존 기출 3회(2015-B·2019-B·2022-B — coverage grep 실증, 2019-B→2022-B 2연속 포함)에 이어 **2024-B Q8 재출제 확증 — 총 4회 출제 (2023-A/2023-B/2024-A 3회 연속 단절 후 단발 재등장)**. Trademark 3중 일치: ① "**평등이라는 기본적 원리를 다른 동물의 종으로 확장 … 내가 말하는 평등의 기본 원리는 ( ㉠ 고려 )의 평등 … 서로 다른 존재에 대한 평등한 ( ㉠ )은/는 서로 다른 대우와 서로 다른 ( ㉡ 권리 )(으)로 이어질 수 있다 … 그들이 어떻게 생겼는지, 그들이 어떤 능력을 가졌는지에 따라 달라져서는 안 된다**"(L131) — 싱어 **이익 평등 고려의 원칙(principle of equal consideration of interests)** trademark. 저서 **『동물 해방(Animal Liberation, 1975)』** 제1장 "All Animals Are Equal" 원문: "*The basic principle of equality does not require equal or identical treatment; it requires equal consideration.*" 평등은 동일한 대우가 아닌 이익의 동일한 고려를 요구하며, 외모·능력 차이는 고려 가치에 영향을 주지 않음. 벤담의 유명한 각주 "*The question is not, Can they reason? nor, Can they talk? but, Can they suffer?*"(이성·언어가 아닌 고통 감수 능력이 기준)의 현대적 계승; ② "**인종차별주의와 성차별주의에 대한 반대 논의가 궁극적으로 호소해야 하는 것도 바로 이 원리 … 종차별주의가 비난받아야 하는 것도 이 원리 때문**"(L131) — 싱어 **종차별주의(speciesism)** 비판 trademark. 용어는 리처드 라이더(Richard Ryder, 1970)가 창안하고 싱어가 대중화. 인종차별·성차별과 마찬가지로 **종(種) 소속**만을 이유로 한 차별은 도덕적으로 정당화될 수 없는 편견이라는 주장. 『Animal Liberation』·『Practical Ethics(1979, 1993, 2011)』 제3장 "Equality for Animals?" 정전; ③ 전체 문단 구조가 공리주의 응용윤리 — 벤담-밀 계보의 쾌고 감수 능력(sentience) 기준을 동물에 확장 — 의 trademark. 밴듀라의 자연주의적 평등 원리 거부와 달리, 싱어는 경험적·자연주의적 차이(지적 능력·외모 등)가 아닌 **이익을 가질 수 있는 능력(쾌고 감수 능력)**만이 도덕적 고려의 경계 기준이 된다고 주장. 이는 **규범적 공리주의 + 자연주의 메타윤리**의 결합.
- 후속 조치: TASK-176 범위에서 `singer` 신규 등록 **최우선** (총 4회 출제 기출 이력, 임용시험 응용윤리 영역 최빈출 사상가) — **이익 평등 고려의 원칙(principle of equal consideration of interests)** · **종차별주의(speciesism) 비판** · **동물 해방(animal liberation) 운동 정초** · **선호 공리주의(preference utilitarianism) — 고전 쾌락주의 공리주의와 차별** · **쾌고 감수 능력(sentience) — 도덕적 고려 경계의 기준** · **인격(person) vs 생명(life) 구분 — 인격은 자기의식·미래 감각을 가진 존재, 신생아·심각한 뇌 손상 환자는 인격 아님 (논쟁적 입장)** · **살아 있음이 중요한 것이 아니라 이익을 가질 수 있는 능력이 중요** · **응용윤리 — 빈곤·기부·안락사·낙태·배아 연구·동물실험·공장식 축산 등 실천 문제** · **세계 빈곤과 도덕적 의무 — 「Famine, Affluence, and Morality(1972)」·『The Life You Can Save(2009)』** · **효율적 이타주의(effective altruism) 운동의 사상적 창시자** · **헤어(R.M. Hare) 2수준 공리주의 계승 + 수정** · **벤담-밀 공리주의 전통의 현대적 계승자 중 가장 대중적·영향력 있는 철학자** · **저서: 『Animal Liberation(1975, 1990, 2002, 2009)』·『Practical Ethics(1979, 1993, 2011)』·『Rethinking Life and Death(1994)』·『The Life You Can Save(2009)』·『The Most Good You Can Do(2015)』** · **코로나19 이후 공중보건 윤리·기후 위기 윤리로도 확장** · **리건(Tom Regan, 의무론적 동물권) vs 싱어(공리주의 이익 평등 고려)** — 동물 윤리 2대 입장의 대립. 후보 id: `singer`. 등록 우선순위 **최우선** (총 4회 출제 기출 이력, 응용윤리 최빈출 사상가, `bentham`·`mill_js`·`rawls` 등과 함께 공리주의·자유주의 응용윤리 계보의 현대 정점).
- 영향: Q8 (갑) 정답 ㉠(고려)·㉡(권리)·을의 비판(유용성 관련)은 trademark 3중 일치로 확정됨. coverage/2024-B.md Q8 본문은 정확하며 ES 커버리지 공백만 존재. **재출제 경계 리스트 갱신 — `singer` 총 4회 출제 확정 (2015-B·2019-B·2022-B·2024-B)**. 응용윤리 동물 윤리 영역 커버리지 구조적 공백(`singer` MISS + `regan` MISS로 동물 윤리 2대 입장 모두 ES에 없음).

### BLK-175E-2024B-006 (TASK-175E-2024-B) — Q8 (을) 톰 리건(Tom Regan) ES 미등록 (2회째 출제)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2024-B.md` Q8 row (을)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 의무론적 동물권 이론의 정초자, 동물 윤리 2대 입장 중 공리주의 싱어에 대비되는 의무론 진영의 대표, **총 2회 출제 (2018-A·2024-B; 6년 단절 후 단발 재등장)**)
- 사유: Q8 (L133) 제시문 중심 사상가 **톰 리건(Tom Regan, 1938-2017, 미국 노스캐롤라이나 주립대 철학자, 의무론적 동물권(deontological animal rights) 이론의 정초자)**의 canonical thinker_id가 ES 미등록. `regan` MISS. 기존 기출 1회(2018-A Q11 — BLK-175E-2018A-001 선례)에 이어 **2024-B Q8 재출제 확증 — 총 2회 출제 (2018-B/2019-A/2019-B/2020-A/2020-B/2021-A/2021-B/2022-A/2022-B/2023-A/2023-B/2024-A 12회 단절 후 단발 재등장)**. Trademark 3중 일치: ① "**내재적 가치(inherent value)를 가지는 존재는 모두 동등하게 그 가치를 소유하고 있고, 모두 존중받을 동등한 ( ㉡ 권리 )을/를 가진다**"(L133) — 리건 **내재적 가치(inherent value)** 원칙 trademark. 저서 **『The Case for Animal Rights(1983)』** 제7장 "Justice and Equality" 원문: "*Individuals who have inherent value have it equally … [they] are never to be treated as if they exist as resources for others; their value as individuals is independent of how useful they may be to others; and it is wrong to treat them in ways that fail to treat them with the respect they deserve.*" 내재적 가치는 단일 척도에 의한 양적 비교가 불가능한 **비교 불가능한 절대적 가치**이며, 모든 삶의 주체는 이를 동등하게 소유함; ② "**다른 이들에게 어떤 ㉢ 유용성을 가지는지와 무관하게 중요한 개인적 복지를 가지는 의식적 생명체**"(L133) — 리건 **유용성 독립성(independence of utility)** trademark: 내재적 가치는 타인에 대한 도구적 가치·유용성과 **논리적으로 독립적**이다. 이는 칸트의 목적 자체 원칙(Formula of Humanity)을 동물로 확장한 것으로, 동물을 단순 수단으로 사용하는 것 자체가 금지됨. 싱어의 이익 고려 공리주의가 이익 총합 계산을 통해 개별 동물을 수단화할 여지를 남기는 것과 원리적으로 대립; ③ "**무언가를 원하고 선호하고, 믿고 느끼며, 상기하고 기대한다. 또 쾌락과 고통, 즐거움과 괴로움, 만족과 좌절, 생존 혹은 죽음을 포함하는 삶의 모든 차원은 우리가 개체로서 경험하고 살아온 삶의 질에 차이를 만든다**"(L133) — 리건 **삶의 주체(subject-of-a-life) 기준** trademark. 『The Case for Animal Rights(1983)』 정식 정의: "*An individual is a subject-of-a-life if they have beliefs and desires; perception, memory, and a sense of the future, including their own future; an emotional life together with feelings of pleasure and pain; preference- and welfare-interests; the ability to initiate action in pursuit of their desires and goals; a psychophysical identity over time; and an individual welfare in the sense that their experiential life fares well or ill for them, logically independently of their utility for others and logically independently of their being the object of anyone else's interests.*" 믿음·욕망·지각·기억·미래 감각·감정·선호·복지·행위 주도·심리물리적 동일성·개인적 복지의 9가지 기준. 일반적으로 1세 이상의 정상적 포유류 동물이 이 기준을 충족한다고 리건은 주장.
- 후속 조치: TASK-176 범위에서 `regan` 신규 등록 **최우선** (의무론적 동물권 이론의 유일한 대표 사상가, 싱어와 함께 동물 윤리 2대 입장의 한 축) — **의무론적 동물권 이론(deontological animal rights theory)** · **삶의 주체(subject-of-a-life) 기준 — 9가지 조건** · **내재적 가치(inherent value) — 유용성 독립성·비교 불가능성·동등성** · **존중의 원칙(respect principle) — 삶의 주체는 단순 수단으로 다뤄져서는 안 됨** · **칸트 목적 자체 원칙의 동물 확장** · **공리주의 비판 — 이익 총합 계산의 수단화 위험** · **간접 의무 이론(indirect duty theories, 칸트·데카르트) 비판 — 동물에 대한 의무는 직접적** · **동물 실험 금지·공장식 축산 금지·스포츠 사냥 금지** · **저서: 『The Case for Animal Rights(1983, 2004 재판)』 — 동물권 철학의 정전** · **『Empty Cages: Facing the Challenge of Animal Rights(2004)』 — 대중 입문서** · **『Animal Rights, Human Wrongs(2003)』** · **『Defending Animal Rights(2001)』** · **싱어(공리주의) vs 리건(의무론) — 동물 윤리 2대 입장의 철학적 대립** · **환경 윤리에서 생명 중심주의(`taylor_p` Paul Taylor)·생태 중심주의(`leopold`·`naess`)와도 대비 — 개체 중심 동물권 입장** · **채식주의·비건주의 철학적 근거 제공** · **동물 복지(animal welfare) vs 동물권(animal rights) 구분의 이론적 기반** · **Francione·Nussbaum(역량 접근) 등 후속 동물윤리학자들의 비판적 수용**. 후보 id: `regan`. 등록 우선순위 **최우선** (싱어와 쌍을 이루는 동물 윤리 2대 입장 대표 사상가, 싱어 `singer` 3연속 재출제와 동시 출제된 만큼 차기 시험 재출제 확률 매우 높음, 동물 윤리 영역 ES 커버리지 구조적 완성을 위해 필수).
- 영향: Q8 (을) 정답 ㉡(권리)·㉢(유용성 — 을이 갑을 비판하는 근거)·을의 도덕적 지위 기준 서술은 trademark 3중 일치로 확정됨. coverage/2024-B.md Q8 본문은 정확하며 ES 커버리지 공백만 존재. **동물 윤리 2대 입장 동시 ES 공백 상태 — `singer` + `regan` 쌍으로 등록 필요**. 본 블로커는 BLK-175E-2024B-005(싱어)와 병합 처리 권고 — 단일 교과서 출제 맥락에서 쌍 등록이 자연스러움.

### BLK-175E-2025A-001 (TASK-175E-2025-A) — Q5 에밀 뒤르켐(Émile Durkheim) ES 미등록 (5회째 출제 · 2024-B→2025-A 2연속)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2025-A.md` Q5 row (㉡·㉢, (나) 지도안 뒤르켐 입장 ㉢ 자율성)
- 심각도: blocker (ES 커버리지 누락 — 제시문 명시 사상가 미등록, 사회학적 도덕교육론 정초자, **총 5회 출제 (2015-B·2021-B·2022-B·2024-B·2025-A; 2024-B→2025-A 2연속 재출제로 최상위 우선 등록 대상으로 격상)**)
- 사유: Q5 문두 (L63) "(가)는 직소 Ⅰ(Jigsaw Ⅰ) 모형에 대한 설명이고, (나)는 그 모형을 기반으로 **뒤르켐(E. Durkheim)의 도덕성 3요소를 탐구하기 위한** 교수·학습 지도안의 개요이다"로 제시문 중심 사상가가 **에밀 뒤르켐(Émile Durkheim, 1858-1917, 프랑스 사회학자, 『도덕교육론(L'éducation morale, 1925)』)**임이 본문에 명시됨. canonical thinker_id `durkheim`는 ES 미등록 상태. **2024-B Q4 BLK-175E-2024B-002에 이어 2025-A Q5 연속 재출제**로 누적 5회, 2024-B→2025-A 2연속 재출제 확증. Trademark 3중 일치: ① Q5 (L78) "도덕성 3요소인 **규율 정신, ( ㉡ ), ㉢ 자율성**" — 뒤르켐 **도덕성 3요소(three elements of morality)** 정확 일치: (1) **규율 정신(l'esprit de discipline)** — 규칙성 선호 + 권위 존중, (2) **집단 애착(l'attachement aux groupes sociaux)** — 사회 집단의 이익 관점에서 행동(정답 ㉡=집단 애착 / 집단에 대한 애착), (3) **자율성(l'autonomie)** — 도덕 규칙의 과학적·합리적 이해에 기초한 자발적 실천. 『L'éducation morale(1925, 유고, Mauss 편집)』의 핵심 체계; ② Q5 (L85) <작성 방법> "**뒤르켐의 입장에서 밑줄 친 ㉢(자율성)을 가진 사람이 하는 도덕적 행동의 특징을 '사회의 도덕규범'을 사용하여 서술할 것**" — 뒤르켐 **자율성 정의** trademark: 칸트의 개인 이성 기반 자율성과 달리, 뒤르켐의 자율성은 **사회의 도덕규범을 과학적·합리적으로 이해한 바탕에서 자발적으로 그 규범을 수용·실천하는 것**을 의미한다. 이는 사회학적 도덕교육론 정전 정식 입장. 2024-B Q4 BLK-175E-2024B-002 trademark와 동일 근거(3요소 체계 + 자율성의 사회학적 재정의); ③ (가)·(나) 전체 문단이 도덕성 3요소(규율 정신·집단 애착·자율성)의 교과교육적 탐구 지도안이라는 점 — 뒤르켐 도덕교육론 전문 구조 trademark.
- 후속 조치: TASK-176 범위에서 `durkheim` 신규 등록 **최상위 우선** (총 5회 출제 기출 이력 중 2024-B→2025-A **2연속 재출제** 확증 — ES 미등록 사상가 중 연속 재출제가 확인된 유일 사례) — **사회학적 도덕교육(sociological moral education)** · **도덕성 3요소: 규율 정신(규칙성 선호 + 권위 존중) + 집단 애착(사회 집단의 이익 관점) + 자율성(사회 도덕규범의 과학적·합리적 이해 기반 자발적 실천)** · **집합의식(conscience collective)** · **사회적 사실(fait social)** · **기계적 연대(solidarité mécanique) / 유기적 연대(solidarité organique)** · **아노미(anomie) — 규범 부재 상태** · **세속적 도덕(laïcité) — 종교적 초월 기초 없는 도덕 가능성** · **『사회분업론(De la division du travail social, 1893)』** · **『사회학적 방법의 규칙(Les règles de la méthode sociologique, 1895)』** · **『자살론(Le suicide, 1897)』 — 이기적·이타적·아노미적·숙명적 자살 4유형** · **『종교생활의 원초적 형태(Les formes élémentaires de la vie religieuse, 1912)』** · **『도덕교육론(L'éducation morale, 1925, 유고)』** · **프랑스 제3공화국 세속 공화주의 도덕교육 설계자** · **실증주의 사회학 전통(콩트 계승)** · **베버·짐멜과 함께 고전 사회학 3대 거장** · **파슨스·머턴 구조기능주의의 원천** · **피아제·콜버그 도덕심리학이 계승·비판하는 대상**. 후보 id: `durkheim`. 등록 우선순위 **최상위** — 2024-B→2025-A 2연속 재출제로 차기 시험 재출제 확률 모든 미등록 사상가 중 최상, 사회학적 도덕교육 전통 정초자, 임용시험 필수 출제 사상가, `piaget`·`kohlberg` HIT인데 `durkheim`만 MISS인 상태는 현대 도덕교육 이론 ES 커버리지 구조적 공백.
- 영향: Q5 ㉡(집단에 대한 애착) 용어 + ㉢(자율성) 뒤르켐 입장 서술은 trademark 3중 일치로 확정됨. coverage/2025-A.md Q5 본문은 정확하며 ES 커버리지 공백만 존재. **재출제 경계 리스트 최상위 갱신 — `durkheim` 총 5회 출제 확정 (2015-B·2021-B·2022-B·2024-B·2025-A, 2024-B→2025-A 2연속)**. BLK-175E-2024B-002에 대한 실증적 후속 증거로서 `durkheim` 등록 TASK-176에서의 긴급 우선 처리를 재확증.

### BLK-175E-2025A-002 (TASK-175E-2025-A) — Q6 (갑) 마틴 호프만(Martin L. Hoffman) ES 미등록 (row 기준 4회째 출제, TASK-175E-2025-A-FIX 재조사)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2025-A.md` Q6 row (갑 ㉠·㉢)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 현대 발달 도덕심리학 공감 이론 정립자, **row-by-row thinker_id 컬럼 기준 총 4회 출제 (2016-A·2019-B·2022-B·2025-A — TASK-175E-2025-A-FIX에서 `grep -E "^\| Q[0-9]+" coverage/*.md | grep hoffman` 재조사로 실증); 2021-A·2021-B·2023-A·2023-B·2024-A·2024-B는 backtick `` `hoffman` `` 파일 매치만 있고 본문 사상가 row 등록 없음 (요약/경계 대상 섹션 언급)**)
- 사유: Q6 (L93) 제시문 갑 "**공감은 보편적이고 친사회적인 도덕성을 위한 훌륭한 방책이다. 나의 공감 이론에서 중요한 부분은 인지적 발달을 통해 단순한 공감적 고통이, 다른 사람을 도우려는 의식적 욕망과 동기를 가진 고통의 감정인 ( ㉠ )(으)로 변형될 수 있다**"로 제시문 중심 사상가가 **마틴 호프만(Martin L. Hoffman, 1924-2024, 미국 뉴욕대 발달심리학자, 공감 기반 도덕 발달 이론 창시자)**임이 공감 이론 trademark로 확증됨. canonical thinker_id `hoffman`는 ES 미등록 상태. Trademark 3중 일치: ① Q6 (L95) "**단순한 공감적 고통이 … 다른 사람을 도우려는 의식적 욕망과 동기를 가진 고통의 감정인 ( ㉠ )(으)로 변형**" — 호프만 **공감적 고통(empathic distress) → 공감적 염려/동정적 고통(sympathetic distress / empathic concern)** 변형 trademark. 저서 『Empathy and Moral Development: Implications for Caring and Justice(2000)』 제3장 정식 체계: 초기 단계의 무차별적·반사적 공감적 고통이 인지 발달(자기-타자 구분·역할 채택·인과 이해)을 통해 타자 지향적·친사회적 동기를 수반하는 공감적 염려(sympathetic distress)로 변형된다는 발달 모형. 정답 ㉠ = **공감적 염려/동정적 고통(sympathetic distress)**; ② Q6 (L103) "**( ㉢ )은/는 다른 사람이 어떻게 느끼는지 혹은 다른 사람의 상황에서 자기가 어떻게 느낄 것인지를 상상하는 것**" — 호프만 **공감 유발 기제 5가지(five modes of empathic arousal)** 중 고차 기제 trademark. 『Empathy and Moral Development(2000)』 제2장: (a) 원초적 모방(primary circular mimicry), (b) 고전적 조건 형성(classical conditioning), (c) 직접 연상(direct association), (d) 매개 연상(mediated association — 언어 매개), (e) **역할 채택/상상적 입장 취득(role-taking / self-focused & other-focused perspective taking)**. 정답 ㉢ = **역할 채택 / 상상적 입장 취득(role-taking)** — 자기 초점 역할 채택(self-focused role taking: 상대 상황에 내가 있다면 어떤 감정일지 상상) + 타자 초점 역할 채택(other-focused role taking: 상대가 실제 어떤 감정일지 상상)의 이중 구조; ③ 제시문 전체가 "**공감 이론**" 언급으로 호프만 trademark 확증. 밴듀라의 사회인지 이론·블라시의 도덕적 정체성 모형·콜버그의 인지 발달 이론과 구별되는, **공감 정서를 도덕 동기의 핵심 원천으로 보는 발달 공감 이론(developmental empathy theory)**의 유일한 정초자.
- 후속 조치: TASK-176 범위에서 `hoffman` 신규 등록 **최우선** — **공감 이론(empathy theory) — 공감을 보편적·친사회적 도덕성의 방책으로 규정** · **공감적 고통(empathic distress) → 공감적 염려/동정적 고통(sympathetic distress) 발달적 변형** · **공감 유발 5가지 기제(원초적 모방·고전적 조건 형성·직접 연상·매개 연상·역할 채택)** · **공감의 4단계 발달(global empathy → egocentric empathy → empathy for another's feelings → empathy for another's life condition)** · **공감 과잉 각성(empathic over-arousal) — 공감이 너무 강하면 자기 고통에 함몰되어 돕기 불능** · **공감 편향(empathic bias) — 가족·친척·유사 집단·현재 가까이 있는 피해자 우선** · **도덕 내면화(moral internalization) — 정서와 인지의 통합** · **귀납적 훈육(inductive discipline) — 아동에게 자신의 행위가 타인에게 미친 영향을 설명하는 훈육법, 도덕 내면화의 최선 방법** · **『Empathy and Moral Development: Implications for Caring and Justice(2000)』 — 공감 이론 체계 집대성** · **『The Roots of Prosocial Behavior in Children(1975)』** · **논문 「Empathy, Its Development and Prosocial Implications(1977)」·「The Contribution of Empathy to Justice and Moral Judgment(1987)」·「Empathy, Role-Taking, Guilt, and Development of Altruistic Motives(1976)」** · **콜버그 인지 발달 이론 보완 — 정서적 차원 복원** · **블라시 도덕적 정체성 모형·튜리엘 영역 이론·나바에츠 통합 도덕교육 모형과 현대 도덕심리학 계보 공유** · **밴듀라 사회인지 이론과의 차이 — 밴듀라가 모방·학습 중심이라면 호프만은 공감 정서의 생득적 기초와 인지적 변형 중심**. 후보 id: `hoffman`. 등록 우선순위 **최우선** (발달 도덕심리학 공감 이론의 유일 정초자, 2025-A 재출제 확정, 2024-B 요약 집계에 따르면 기존 `hoffman` 다수 재출제 이력 확증되며 정확 누적 횟수 재조사 후 최상위 등록 대상 격상 가능).
- 영향: Q6 (갑) 정답 ㉠(공감적 염려/동정적 고통) + ㉢(역할 채택/상상적 입장 취득) 서술은 trademark 3중 일치로 확정됨. coverage/2025-A.md Q6 본문은 정확하며 ES 커버리지 공백만 존재. **재출제 경계 리스트 갱신 — `hoffman` row-by-row thinker_id 컬럼 기준 4회 출제 확정 (2016-A·2019-B·2022-B·2025-A; TASK-175E-2025-A-FIX grep 재조사 실증)**. 2024-B 요약의 "4연속(2016-A/2019-B/2021-B/2022-B)" 표기는 2021-B가 본문 row가 아닌 언급 포함이었기 때문으로, FIX 재조사 후 2021-B를 제외하고 2022-B를 포함한 **2016-A·2019-B·2022-B·2025-A 4회**가 정확 누적 횟수다.

### BLK-175E-2025A-003 — **철회됨 (FALSE-POSITIVE, TASK-175E-2025-A-FIX)**
- 일시 (철회): 2026-04-21
- 원 대상: `rest` (James Rest)
- 철회 사유: 초기 Coder (TASK-175E-2025-A) 판정에서 `rest`가 ES 미등록으로 오분류되었으나, Tester (TASK-175E-2025-A-T) 재조사 및 FIX 검증 결과 `rest`는 ES `ethics-thinkers` 인덱스에 `James Rest`로 정식 등록되어 있으며 `ethics-claims`에 10건 claim 등록된 **HIT** 사상가임이 확증되었다 (`curl -s "localhost:9200/ethics-thinkers/_search?size=100" | jq ... | grep -x rest` 확인 + `ethics-claims` thinker_id=rest count=10 확인 + 이전 2015-B·2016-A·2021-B coverage의 "rest 10 claims 등록" 명기 확인). 본 블로커 엔트리는 false-positive이므로 완전 삭제·철회한다. 블로커 ID(BLK-175E-2025A-003)는 재사용하지 않으며, -001/-002/-004만 유효하다.
- 영향: TASK-176 등록 우선순위에서 `rest` 완전 제거. "ES 미등록 사상가 중 누적 최다 8회 출제" 주장은 철회되며, 기존 `blasi` 5회가 미등록 최다 기록으로 복원. 본 태스크 블로커 누적 4건 → **3건**으로 감소.

### BLK-175E-2025A-004 (TASK-175E-2025-A) — Q8 천태 지의(天台 智顗) ES 미등록 (row 기준 3회째 출제)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2025-A.md` Q8 row (㉠·㉡·㉢·㉣)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 중국 천태종(天台宗) 체계화 정점 인물, 중국 불교 종학 3대 종파 대표자, **row 기준 총 3회 출제 (2022-A·2022-B·2025-A — 2022-A·2022-B 2연속 후 4년 단절 재등장, 중국 불교 종학 영역 최다 출제 미등록 사상가)**)
- 사유: Q8 (L138) 문두 "**다음은 중국 불교의 한 종파의 주장이다**" + 제시문 (L140) "**( ㉠ )은/는 하나의 진리이면서 셋도 아니고 하나도 아니다 … 셋이 모두 공(空) … 가(假) … 중(中) … 원만하게 융합한다[圓融]**" + (L142) "**큰스님은 … 설법의 '시기', '내용', '방식'이라는 기준에 따라 오시팔교(五時八敎)로 분류**"로 제시문 중심 사상가가 **천태 지의(天台 智顗, Zhiyi, 538-597, 중국 수대 승려, 중국 천태종(天台宗) 실질 창시자·체계화 정점, 『마하지관(摩訶止觀)』·『법화현의(法華玄義)』·『법화문구(法華文句)』 천태 3대부 저자)**임이 trademark로 확증됨. canonical thinker_id `zhiyi`는 ES 미등록 상태. Trademark 3중 일치: ① Q8 (L140) "**( ㉠ )은/는 하나의 진리이면서 셋도 아니고 하나도 아니다 … 셋이 모두 공(空) … 가(假) … 중(中) … 원만하게 융합한다[圓融]**" — 지의 **삼제원융(三諦圓融)** 교설 trademark 정확 일치. 『법화현의(法華玄義)』·『마하지관(摩訶止觀)』 체계: 인도 중관(中觀) 이제(二諦 — 진제·속제)에 **중제(中諦)**를 더해 **공제(空諦)·가제(假諦)·중제(中諦) 삼제(三諦)**를 확립하고, 삼제가 서로 방해하지 않고 원만히 융합한다는 천태 독자 교설. 셋이면서 하나이고 하나이면서 셋인 불이(不二)의 진리관. 정답 ㉠ = **삼제(三諦) / 삼제원융(三諦圓融)**; ② Q8 (L140) "**( ㉠ )의 지혜는 불가사의하면서 ( ㉡ )에 갖추어져 있으니 … ( ㉡ )에서 그 ( ㉠ )을/를 관(觀)해야 한다**" — 지의 **일심삼관(一心三觀)** 교설 trademark. 『마하지관』 핵심 교설: 삼제의 지혜가 한 마음(一心)에 구족되어 있으며 수행자는 한 마음에서 공관(空觀)·가관(假觀)·중관(中觀)의 삼관을 동시에 관해야 한다는 원돈(圓頓) 지관법. 정답 ㉡ = **일심(一心)** (또는 **일념(一念) / 한 마음**); ③ Q8 (L142) "**오시팔교(五時八敎) … 팔교도 그 기준에 따라 ㉢ 장교, 통교, 별교, 원교와 ㉣ 돈교, 점교, 비밀교, 부정교의 총 8가지 교법으로 분류**" — 지의 **오시팔교(五時八敎)** 교판(敎判) trademark. 『법화현의(法華玄義)』·『사교의(四敎儀, 체관(諦觀) 정리)』 체계: **오시(五時)** — 화엄시·녹원시(아함시)·방등시·반야시·법화열반시(설법 시기 분류) + **팔교(八敎)** = **화법 4교(化法四敎)** [장교(藏敎)·통교(通敎)·별교(別敎)·원교(圓敎) — **가르침의 내용·교리의 심천(深淺)에 따른 분류**] + **화의 4교(化儀四敎)** [돈교(頓敎)·점교(漸敎)·비밀교(秘密敎)·부정교(不定敎) — **가르침의 방식·설법의 형식(儀)에 따른 분류**]. 석가모니 일생 설법 전체를 시기·내용·방식 3기준으로 총괄하는 천태 교판학 정점. 정답 ㉢ = **화법 4교(化法四敎) — 가르침의 내용에 따라 분류한 것**, ㉣ = **화의 4교(化儀四敎) — 가르침의 방식(설법 형식)에 따라 분류한 것**.
- 후속 조치: TASK-176 범위에서 `zhiyi` 신규 등록 **최우선** (중국 천태종 체계화 정점 인물, 중국 불교 종학 최다 출제 미등록 사상가, 2024-A `fazang`(중국 화엄종) MISS BLK-175E-2024A-005와 함께 **중국 불교 3대 종파 대표자 동시 ES 공백 패턴**의 반복) — **중국 천태종(天台宗) 창시·체계화** · **삼제원융(三諦圓融): 공제(空諦)·가제(假諦)·중제(中諦)** · **일심삼관(一心三觀): 공관·가관·중관을 한 마음에서 동시에 관(觀)** · **오시팔교(五時八敎) 교판(敎判) — 석가모니 일생 설법 체계적 분류** · **오시(五時): 화엄시·녹원시(아함시)·방등시·반야시·법화열반시** · **화법 4교(化法四敎): 장교·통교·별교·원교 (가르침의 내용 기준)** · **화의 4교(化儀四敎): 돈교·점교·비밀교·부정교 (가르침의 방식 기준)** · **『법화현의(法華玄義)』** · **『법화문구(法華文句)』** · **『마하지관(摩訶止觀)』** — 천태 3대부(天台三大部) · **원돈(圓頓) 지관(止觀) — 원교의 지관** · **『법화경(法華經)』을 최고 경전으로 하는 일승(一乘) 사상** · **제자 관정(灌頂, 561-632)의 정리·체관(諦觀, 고려 출신, 10세기)의 『사교의(四敎儀)』 정리로 후대 전승** · **일본 사이초(最澄, 767-822)에 의한 일본 천태종 성립 — 사이초 자신이 당나라에서 천태 교학 수학** · **한국에서는 고려 제관(諦觀)의 『천태사교의』가 천태 교학의 국제적 표준 교과서가 됨 — 중국·일본·한국 천태종 공통 입문서** · **고려 대각국사 의천(義天, 1055-1101)의 한국 천태종(고려 천태종) 창시의 사상적 원천** · **화엄종(법장)·선종(혜능)·정토종(선도)·삼론종(길장)·유식종(규기) 등과 함께 중국 불교 종파 불교(宗派佛敎) 전개의 핵심 축** · **원융불이(圓融不二) 사상 — 후대 중국·한국 불교 통섭 전통에 지대한 영향**. 후보 id: `zhiyi`. 등록 우선순위 **최우선** — 중국 천태종 유일 대표 사상가, 2025-A Q8 단일 문항 trademark 4중(삼제원융·일심삼관·화법4교·화의4교) 전면 출제, 2022-A·2022-B 2연속 + 2025-A 재출제로 row 3회째 출제, 중국 불교 종학(宗學) 체계화 최정점 인물, 고려 제관 『사교의』 덕에 **한국 불교 전통 교학 교과서의 사상적 원류** — 임용시험 동양 불교 사상 영역 필수 출제 사상가.
- 영향: Q8 정답 ㉠(삼제/삼제원융)·㉡(일심)·㉢(화법4교 — 가르침의 내용에 따른 분류)·㉣(화의4교 — 가르침의 방식에 따른 분류)의 trademark 4중 일치로 완전 확정됨. coverage/2025-A.md Q8 본문은 정확하며 ES 커버리지 공백만 존재. **중국 불교 3대 종파 대표자 동시 ES 공백 패턴 확증 — `zhiyi`(천태, 2022-A/B·2025-A 3회) + `fazang`(화엄, 2024-A 1회 — BLK-175E-2024A-005) 동시 MISS**. 화엄(法藏) + 천태(智顗) + 선(慧能)이 중국 불교 종파 체계화의 3대 축인데 현재 ES에 `zhiyi`·`fazang` 둘 다 없고 `huineng`(6조 혜능) 상태는 재확인 필요 — TASK-176 범위에 중국 불교 3대 종파 대표자 일괄 등록 권고.

### BLK-175E-2025B-001 (TASK-175E-2025-B) — Q1 보조국사 지눌(知訥) ES 미등록 (**3회째 출제 — 2026-B Q9 갱신, 2025-B→2026-B 2연속**)
- 일시: 2026-04-21 (최초 등록) · 2026-04-21 TASK-175E-2026-B 작업 시 갱신
- 위치: `projects/ethics-study/exam-solutions/coverage/2025-B.md` Q1 row (㉠·㉡·㉢) + `projects/ethics-study/exam-solutions/coverage/2026-B.md` Q9 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 고려 조계종(曹溪宗) 개창자, 한국 선불교(禪佛敎) 사상체계 정립자, **row 기준 총 3회 출제 (2021-B·2025-B·2026-B) + 2025-B→2026-B 2연속 재출제**)

**2026-B Q9 갱신 (2026-04-21, TASK-175E-2026-B 작업 시 / BLK-175E-2026B-002 신규 독립 블로커와 별도 이중 누적 처리)**:
- 2026-B Q9 원문(L163-L177): "**정(定)과 혜(慧) … 삼학(三學) … (㉠), 정, 혜** (계=戒) / **자성정혜(自性定慧)** / **수상정혜(隨相定慧)** / **공적영지(空寂靈知)** / **돈오(頓悟) … 점수(漸修)** / **맑은 구슬 비유**" — **지눌 『수심결』·『법집별행록절요병입사기』 정식 trademark 6중 일치**.
- 2026-B는 **맑은 구슬/검은 구슬 비유가 신규 trademark**로 등장 — 지눌 『수심결(修心訣)』의 보주(寶珠) 비유 trademark.
- 2021-B Q1 + 2025-B Q1 + 2026-B Q9 = **3회 누적**. 2025-B→2026-B **2연속** 출제 확증.
- `ethics-thinkers` MISS 상태 지속. ES 등록 최우선도 격상.

- 사유: Q1 (L16-L26) 제시문 "**마음 밖에 부처가 없고, 자성(自性) 밖에 법이 없다(心外無佛 性外無法)**" + "**자성(自性)을 밝게 비추는 (㉡ 정(定))의 힘과 (㉢ 혜(慧))의 작용**" + "**선지식(善知識)**" + "**돈오돈수(頓悟頓修)**" trademark 조합으로 제시문 중심 사상가가 **보조국사 지눌(普照國師 知訥, 1158-1210, 고려 조계종 개창자, 한국 선불교 사상체계 정립자, 『수심결(修心訣)』·『권수정혜결사문(勸修定慧結社文)』·『간화결의론(看話決疑論)』·『원돈성불론(圓頓成佛論)』 저자)**임이 확증됨. canonical thinker_id `jinul`는 ES 미등록 상태. Trademark 3중 일치: ① "**마음 밖에 부처가 없고, 자성 밖에 법이 없다(心外無佛 性外無法)**" = 지눌 『수심결(修心訣)』 정식 서두 trademark; ② "**자성(自性)을 밝게 비추는 정(定)의 힘과 혜(慧)의 작용**" = 지눌 **자성정혜(自性定慧) / 정혜쌍수(定慧雙修)** 교설 trademark. 『권수정혜결사문』 제1장: "정(定)은 체(體)요 혜(慧)는 용(用)이니, 체와 용이 원래 둘이 아니다"; ③ 문두 "**돈오돈수(頓悟頓修)**"는 지눌 후기 사상 — 지눌은 초기 **돈오점수(頓悟漸修)**를 주창하였으나 말년 『간화결의론』에서 돈오돈수로 이행. 본 문항은 지눌 말기 입장 출제.
- 후속 조치: TASK-176 범위에서 `jinul` 신규 등록 **우선** (고려 조계종 개창자, 한국 선불교 사상체계의 정립자, 『수심결』·『권수정혜결사문』 등 한국 불교 교과서적 저작의 저자) — **고려 조계종(曹溪宗) 개창** · **정혜쌍수(定慧雙修) — 정(定)과 혜(慧)를 동시에 닦음** · **자성정혜(自性定慧) — 마음의 본성에 정·혜가 구족되어 있음** · **돈오점수(頓悟漸修) — 깨달음 후 점진적 닦음 (초기 사상)** · **돈오돈수(頓悟頓修) — 깨달음 후 더 이상 닦을 것이 없음 (말기 사상)** · **간화선(看話禪) — 화두 참구 수행법** · **교선일치(敎禪一致) — 교종과 선종의 통합** · **『수심결(修心訣)』 — 마음 닦는 비결, 한국 선불교 정전** · **『권수정혜결사문(勸修定慧結社文)』** · **『간화결의론(看話決疑論)』** · **『원돈성불론(圓頓成佛論)』** · **선지식(善知識) 개념 — 깨달음의 인도자** · **심외무불(心外無佛) · 성외무법(性外無法) — 불성의 내재성** · **원효·의상·지눌·휴정(서산대사)과 함께 한국 불교 4대 사상가** · **조선 서산대사(西山大師 休靜)·초의선사 등 후대 한국 선불교 전통의 원류** · **중국 혜능(慧能) 조계 선종 계승 — 한국적 전개**. 후보 id: `jinul`. 등록 우선순위 **우선** — 한국 불교 사상사 핵심 인물, 2021-B·2025-B 4년 간격 재출제로 중기 빈도, 임용시험 동양·한국 사상 영역 필수 출제 사상가.
- 영향: Q1 정답 ㉠(불성/자성)·㉡(정·선정)·㉢(혜·지혜)의 trademark 3중 일치로 확정됨. coverage/2025-B.md Q1 본문은 정확하며 ES 커버리지 공백만 존재. **재출제 경계 리스트 갱신 — `jinul` 총 2회 출제 확정 (2021-B·2025-B)**. 한국 선불교 영역 ES 커버리지 구조적 공백 (`jinul` MISS 상태에서 `wonhyo`(원효)는 HIT) — 한국 불교 4대 사상가 중 원효만 ES에 있고 의상·지눌·휴정 미등록 상태로 한국 불교 사상사 ES 커버리지 불완전.

### BLK-175E-2025B-002 (TASK-175E-2025-B) — Q2 조지 에드워드 무어(G. E. Moore) ES 미등록 (2회째 출제)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2025-B.md` Q2 row (기입형 2점)
- 심각도: blocker (ES 커버리지 누락 — 제시문에 실명 명시된 중심 사상가 미등록, 20세기 분석철학 정초자 중 1인, 메타윤리학(metaethics) 창시자, **row 기준 총 2회 출제 (2021-A·2025-B — 4년 간격 재등장)**)
- 사유: Q2 (L33-L37) 제시문 "**무어(G. E. Moore)는 자연주의(naturalism)적 오류를 지적하면서 '좋음(good)'을 자연적 속성과 동일시할 수 없다고 주장한다**" + "**어떤 속성 N이 좋음과 동일하다고 가정하더라도 'N한 것이 정말 좋은가?'라는 물음이 여전히 열려 있기 때문이다**"로 제시문 중심 사상가가 **조지 에드워드 무어(George Edward Moore, 1873-1958, 영국 케임브리지대 분석철학자, 버트런드 러셀·비트겐슈타인과 함께 케임브리지 분석철학 3대 거장, 『Principia Ethica(1903)』·『Ethics(1912)』·『Some Main Problems of Philosophy(1953)』 저자)**임이 **원문 실명 명시 + trademark 3중**으로 즉결 확정. canonical thinker_id `moore`는 ES 미등록 상태. Trademark 3중 일치: ① **실명 "무어(G. E. Moore)" 직접 명시** (L33) — 3단계 확정 1단계 즉결; ② **"자연주의적 오류(naturalistic fallacy)"** = 무어 『Principia Ethica(1903)』 제1장 §10-§14 정식 체계. 도덕적 속성 '좋음(good)'을 쾌락·욕구 만족 등 자연적 속성과 동일시하려는 시도는 범주적 오류라는 비판. 자연주의적 공리주의(벤담·밀)·이상적 공리주의·진화론적 윤리(스펜서) 등을 비판; ③ **"열린 질문 논증(Open-Question Argument)"** — 'N한 것이 정말 좋은가?'가 여전히 열린 질문이라는 논증 구조는 『Principia Ethica』 §13 원문 "*It is always an open question whether anything is good*"의 한국어 직역. '좋음'이 N과 동일하다면 'N한 것이 좋은가'는 동어반복이어야 하나 실제로는 의미 있는 물음이므로 '좋음'은 N과 동일할 수 없다는 분석철학적 논증.
- 후속 조치: TASK-176 범위에서 `moore` 신규 등록 **우선** (메타윤리학 창시자, 20세기 분석철학 정초자, 임용시험 메타윤리 영역의 필수 출제 사상가) — **메타윤리학(metaethics) 창시** · **자연주의적 오류(naturalistic fallacy) — 도덕 속성을 자연 속성으로 환원하는 오류 비판** · **열린 질문 논증(Open-Question Argument) — 분석철학적 윤리 논증의 전형** · **비자연주의(non-naturalism) — 도덕 속성은 독자적 비자연적 속성** · **직관주의(intuitionism) — 좋음은 단순 비분석적 개념, 직관으로 파악** · **이상적 공리주의(ideal utilitarianism) — 무어 고유의 공리주의, 쾌락 외에 미적·지적 가치 포함** · **『Principia Ethica(1903)』 — 메타윤리학의 정전, 블룸즈버리 그룹 윤리적 바이블** · **『Ethics(1912)』 — 윤리학 입문서** · **『A Defence of Common Sense(1925)』 — 상식적 실재론** · **『Proof of an External World(1939)』 — 외부 세계 증명** · **『Philosophical Papers(1959)』** · **러셀·비트겐슈타인과 함께 케임브리지 분석철학 3대 거장** · **블룸즈버리 그룹(Bloomsbury Group) 윤리적 지도자 — 케인스·스트레이치·버지니아 울프 등에 영향** · **헤이어(R. M. Hare)·맥키(J. L. Mackie)·스미스(Michael Smith) 등 20세기 메타윤리학자들의 출발점** · **자연주의적 오류 비판은 이후 정의주의(emotivism, Ayer/Stevenson)·규정주의(prescriptivism, Hare)·오류이론(error theory, Mackie)·비인지주의 전반의 출발점** · **도덕 실재론 논쟁·환원주의 vs 비환원주의 논쟁의 이론적 원점**. 후보 id: `moore`. 등록 우선순위 **우선** — 메타윤리학의 창시자, 임용시험에서 "자연주의적 오류" "열린 질문 논증" 용어가 2회 연속 출제로 확증된 핵심 개념, 2021-A·2025-B 재출제 패턴.
- 영향: Q2 정답 (자연주의적 오류 / 열린 질문 논증 기입)은 trademark 3중 일치 + 원문 실명 명시로 완전 확정됨. coverage/2025-B.md Q2 본문은 정확하며 ES 커버리지 공백만 존재. **재출제 경계 리스트 갱신 — `moore` 총 2회 출제 확정 (2021-A·2025-B)**. 메타윤리 영역 ES 커버리지 구조적 공백 (분석철학 메타윤리학은 `moore`(비자연주의)·`ayer`(정의주의)·`hare`(규정주의)·`mackie`(오류이론)·`smith_m`(도덕 실재론) 계보 — ES에 이 중 단 하나도 등록되지 않아 메타윤리 영역 전체 ES 공백).

### BLK-175E-2025B-003 (TASK-175E-2025-B) — Q5 앨버트 반두라(Albert Bandura) ES 미등록 (5회째 출제 · 2024-B→2025-B 2연속)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2025-B.md` Q5 row (갑·을 전체)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 사회인지이론(social cognitive theory)·자아효능감(self-efficacy) 이론 창시자, **row 기준 총 5회 출제 (2014-A·2019-A·2020-A·2024-B·2025-B); 2024-B→2025-B 2연속 재출제 확증 — ES 미등록 사상가 중 BLK-175E-2025A-001(durkheim, 2024-B→2025-A 2연속)과 더불어 연속 재출제가 확인된 유이(唯二) 사례**)
- 사유: Q5 (L84-L100) 제시문 "(가) 갑: **자아효능감(self-efficacy)**은 … 자기 자신의 능력에 대한 신념 … **삼원상호결정론(triadic reciprocal causation)**의 한 요소 … 자아효능감의 원천은 ① 실천 성취(enactive mastery experience), ② **대리적 경험(vicarious experience)**, ③ **언어적 설득(verbal persuasion)**, ④ 생리적·정서적 상태(physiological and affective states)"로 제시문 중심 사상가가 **앨버트 반두라(Albert Bandura, 1925-2021, 캐나다계 미국인, 스탠퍼드대 심리학과 명예교수, 사회인지이론(Social Cognitive Theory)·자아효능감(Self-Efficacy) 이론 창시자, APA 20세기 심리학자 영향력 4위(스키너·피아제·프로이트 다음))**임이 trademark 4중으로 확증됨. canonical thinker_id `bandura`는 ES 미등록 상태. Trademark 4중 일치: ① **"자아효능감(self-efficacy)"** 정식 정의 = "특정 상황에서 과제를 성공적으로 수행할 수 있다는 자기 능력에 대한 신념" = 반두라 1977년 『Self-Efficacy: Toward a Unifying Theory of Behavioral Change(Psychological Review)』 정의 정확 일치; ② **"삼원상호결정론(triadic reciprocal causation / triadic reciprocal determinism)"** = 반두라 1986년 『Social Foundations of Thought and Action: A Social Cognitive Theory』 제1장 정식 체계. 개인(Person, P)·환경(Environment, E)·행동(Behavior, B) 세 요인의 **상호결정적(reciprocal)** 관계 — 일방향 결정론(행동주의·정신분석)을 비판하고 3자 상호 영향을 주장; ③ **자아효능감 4원천(four sources of self-efficacy)** = 『Self-Efficacy: The Exercise of Control(1997)』 제3장 정식 체계: (a) **실천 성취(enactive mastery experience) — 가장 강력한 원천, 성공 경험의 누적**, (b) **대리적 경험(vicarious experience) — 모델링, 유사한 타인의 성공 관찰**, (c) **언어적 설득(verbal persuasion) — 타인의 격려·피드백**, (d) **생리적·정서적 상태(physiological and affective states) — 각성·불안·피로 등 신체 신호**. 원문 표현 "실천 성취·대리적 경험·언어적 설득·생리적·정서적 상태" 4원천 정확 일치; ④ **사회 제도(social institutions) 불완전성 맥락에서의 자아효능감** = 『Self-Efficacy(1997)』 제11장 "Collective Efficacy" — 개인 자아효능감은 사회 제도·집단 효능감(collective efficacy)과 상호작용. 을의 "사회 제도의 불완전성에 대한 이해" 서술은 이 확장 이론 trademark.
- 후속 조치: TASK-176 범위에서 `bandura` 신규 등록 **최상위 우선** (총 5회 출제 기출 이력 + 2024-B→2025-B **2연속 재출제** 확증 — ES 미등록 사상가 중 `durkheim`(BLK-175E-2025A-001, 2024-B→2025-A 2연속)과 더불어 연속 재출제가 확인된 유이 사례) — **사회학습이론(Social Learning Theory) → 사회인지이론(Social Cognitive Theory, 1986년 개명)** · **관찰학습(observational learning) 4단계: 주의(attention) → 파지(retention) → 산출(production/reproduction) → 동기화(motivation)** · **보보인형 실험(Bobo doll experiment, 1961·1963) — 공격 행동의 모방 학습 실증** · **대리적 강화(vicarious reinforcement) · 대리적 처벌(vicarious punishment)** · **자기 효능감(self-efficacy) — 특정 상황에서의 자기 능력 신념** · **자아효능감 4원천: 실천 성취·대리적 경험·언어적 설득·생리적·정서적 상태** · **삼원상호결정론(triadic reciprocal determinism): 개인(P)·환경(E)·행동(B) 상호작용** · **도덕적 이탈(moral disengagement) — 도덕적 자기 규제 메커니즘 비활성화, 8가지 기제: 도덕적 정당화·완곡어·유리한 비교·책임 전가·책임 분산·결과 왜곡·비인간화·비난 귀속** · **집단 효능감(collective efficacy) — 집단의 공동 신념 및 행동 능력** · **자기 규제(self-regulation) — 자기관찰·자기판단·자기반응의 3단계 순환** · **행위자성(human agency) — 의도성·선견·자기 반응성·자기 반성 4특성** · **『Social Learning Theory(1977)』** · **『Social Foundations of Thought and Action: A Social Cognitive Theory(1986)』 — 사회인지이론 집대성** · **『Self-Efficacy: The Exercise of Control(1997)』 — 자아효능감 이론 정전** · **『Moral Disengagement: How People Do Harm and Live with Themselves(2016)』** · **APA 20세기 영향력 심리학자 4위 (Haggbloom et al., 2002)** · **행동주의(스키너)·인지심리학·인본주의의 교량 인물** · **콜버그 정의 공동체·블라시 도덕 정체성·나바에츠 통합 모형 등 현대 도덕교육 이론 이론적 기초** · **피아제·콜버그 인지발달론 + 반두라 사회인지론 = 현대 도덕심리학 양대 축**. 후보 id: `bandura`. 등록 우선순위 **최상위** — 2024-B→2025-B 2연속 재출제로 차기 시험 재출제 확률 모든 미등록 사상가 중 최상위 (`durkheim`과 공동 1순위), 사회인지 도덕발달 이론 정초자, 임용시험 필수 출제 사상가, `piaget`·`kohlberg` HIT인데 `bandura`만 MISS인 상태는 현대 도덕심리학 이론 ES 커버리지 구조적 공백.
- 영향: Q5 정답 (갑 자아효능감 4원천·삼원상호결정론 서술 + 을 사회제도 연결 서술)은 trademark 4중 일치로 완전 확정됨. coverage/2025-B.md Q5 본문은 정확하며 ES 커버리지 공백만 존재. **재출제 경계 리스트 최상위 갱신 — `bandura` 총 5회 출제 확정 (2014-A·2019-A·2020-A·2024-B·2025-B, **2024-B→2025-B 2연속**)**. BLK-175E-2024B-003 및 이전 2014-A·2019-A·2020-A 기출의 실증적 후속 증거로서 `bandura` 등록 TASK-176에서의 **최상위 긴급 처리**를 재확증.

### BLK-175E-2025B-004 (TASK-175E-2025-B) — Q10 (갑) 신로마 공화주의 [비롤리(Viroli) / 페팃(Pettit)] ES 미등록 (**3회째 출제 — 2026-B Q7 갱신, 2025-B→2026-B 2연속**)
- 일시: 2026-04-21 (최초 등록) · 2026-04-21 TASK-175E-2026-B 작업 시 갱신
- 위치: `projects/ethics-study/exam-solutions/coverage/2025-B.md` Q10 row (갑) + `projects/ethics-study/exam-solutions/coverage/2026-B.md` Q7 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 후보군 모두 미등록, **신로마 공화주의(Neo-Roman republicanism)** 대표 사상가 ES 전면 공백, **pettit 기준 row 3회 출제 (2023-A·2025-B·2026-B) + 2025-B→2026-B 2연속 재출제**)

**2026-B Q7 갱신 (2026-04-21, TASK-175E-2026-B 작업 시 / BLK-175E-2026B-005 신규 독립 블로커와 별도 이중 누적 처리)**:
- 2026-B Q7 원문(L127-L137): "**자유주의는 간섭으로부터 개인을 지키는 데는 성공했지만 '주인(master)으로서의 삶'이라는 자유의 본래 의미를 간과 … 힘센 자와 약한 자 … 예속 … 눈을 내리깔고 … 눈을 크게 뜨고**" / "**입헌주의 … ( ㉠ )의 원리 … 사법권과 입법권 … 집중 회피**" / "**자연권(自然權) 이론 … ( ㉢ )이라고도**" 구조의 trademark 3중 일치로 **페팃(Pettit) 신로마 공화주의** 확증.
- 비롤리는 2023-A 출제 이력 + 공화주의적 애국심 대표자로 경합 후보이나, 본 문항 "주인으로서의 삶 / 눈을 내리깔고·눈을 크게 뜨고 (eyeball test) / 비지배로서의 자유" trademark는 페팃 『Republicanism, 1997』 7장의 정식. 2026-B Q7 = **pettit 1순위 · viroli 2순위**.
- 2023-A + 2025-B + 2026-B = **3회 누적**. 2025-B→2026-B **2연속** 출제 확증.
- 기입형 ㉠ = **권력분립(權力分立 — separation of powers)** / ㉢ = **천부인권(天賦人權 — natural rights) 또는 인권**.
- `pettit`·`viroli` 모두 `ethics-thinkers` MISS 상태 지속. ES 등록 최우선도 격상.

- 사유: Q10 (L174-L178) 제시문 "(가) 갑: **비지배(non-domination)로서의 자유**, 곧 자의적 권력으로부터의 독립이 참된 자유이다. 이는 **자치적(self-governing) 정치체제(republic)** 안에서만 실현될 수 있으며, **시민적 덕성(civic virtue)**과 **법의 지배(rule of law)**가 이를 뒷받침한다"는 **신로마 공화주의(Neo-Roman / Neo-Republican) 자유론** trademark. 후보 2인: ① **마우리치오 비롤리(Maurizio Viroli, 1952-, 이탈리아 프린스턴대·피사 고등사범학교 정치철학자, 『Republicanism(1999)』·『For Love of Country: An Essay on Patriotism and Nationalism(1995)』 저자, 마키아벨리 전문가, 공화주의적 애국심론 대표자)** — 2023-A 기출 이력 + 공화주의·자유·애국심 영역; ② **필립 페팃(Philip Pettit, 1945-, 아일랜드 출신 프린스턴대·오스트레일리아 국립대 철학자, 『Republicanism: A Theory of Freedom and Government(1997)』 저자, **비지배로서의 자유(freedom as non-domination)** 개념 **정립자**)** — "비지배로서의 자유" 개념은 페팃 1997년 저서의 가장 유명한 학문적 trademark. 본 문항의 "비지배(non-domination)" 정확 용어는 페팃 trademark이나, 비롤리도 공화주의 전통 내에서 이 개념을 공유. **확증 보류**: (a) 페팃 유력하나 비롤리 기출 연속성(2023-A)으로 둘 다 후보, (b) 원문 추가 단서(저서명·개인명 미명시) 없음, (c) ES 둘 다 미등록으로 검증 불가. Trademark 3중 일치: ① **"비지배(non-domination)로서의 자유"** = 페팃 1997년 저서 제목 "Freedom as Non-Domination" trademark; ② **"자치적 정치체제(self-governing republic)"** = 신로마 공화주의 정식 개념 (cf. 키케로(Cicero) — 공화국은 res publica, 공중의 사안); ③ **"시민적 덕성(civic virtue) + 법의 지배(rule of law)"** = 마키아벨리·해링턴·매디슨·비롤리·페팃 공통의 신로마 공화주의 정치체계 trademark.
- 후속 조치: TASK-176 범위에서 `pettit` **우선** + `viroli` 보조 등록 권고 (신로마 공화주의는 20세기 후반~21세기 정치철학의 핵심 흐름으로, 벌린 소극적 자유 vs 적극적 자유 이분법에 대한 **제3의 자유 개념** 제시 — ES에 전혀 없어 정치철학 영역 구조적 공백) — **신로마 공화주의(Neo-Roman / Neo-Republican) — Skinner·Pettit·Viroli 주도의 공화주의 부활 운동** · **비지배로서의 자유(freedom as non-domination) — 자의적 권력으로부터의 독립** · **소극적 자유(벌린) vs 적극적 자유(벌린) vs 비지배 자유(페팃) — 자유 3개념 이론** · **자의적 권력(arbitrary power) — 법의 통제 밖의 자의적 의지** · **자치적 공화국(self-governing republic)** · **시민적 덕성(civic virtue)** · **법의 지배(rule of law)** · **공화주의적 애국심(republican patriotism) — 비롤리 대표 개념, 인종적 민족주의와 구별** · **마키아벨리(Machiavelli) 공화주의 전통 — 『로마사 논고』** · **해링턴(James Harrington) · 루소(Rousseau) · 매디슨(James Madison) 공화주의 전통** · **캠브리지 학파(Quentin Skinner·John Pocock·J.G.A. Pocock) 『마키아벨리 이래 공화주의』** · **페팃 저서: 『Republicanism: A Theory of Freedom and Government(1997)』 · 『A Theory of Freedom(2001)』 · 『On the People's Terms(2012)』** · **비롤리 저서: 『For Love of Country(1995)』 · 『Republicanism(1999)』 · 『Machiavelli(1998)』 · 『How to Choose a Leader(2016)』** · **벌린(Berlin) 2자유 개념에 대한 비판 — 비지배 자유는 간섭의 실제 부재가 아니라 자의적 간섭 가능성(possibility) 자체의 부재를 요구**. 후보 id: `pettit` (최우선) + `viroli` (보조). 등록 우선순위 **우선** — 현대 정치철학 핵심 흐름, 임용시험 정치철학 영역 증가 출제 추세, 벌린 소극적 자유·롤즈·샌델과 함께 자유 개념 비교 출제의 필수 축.
- 영향: Q10 (갑) 정답 (신로마 공화주의 식별 + 비지배 자유 서술)은 trademark 3중 일치로 확정됨. coverage/2025-B.md Q10 갑 본문은 정확하며 ES 커버리지 공백만 존재. **신로마 공화주의 영역 ES 전면 공백 상태 — `pettit` · `viroli` · `skinner_q`(Quentin Skinner) 모두 미등록**. 정치철학 영역 중 롤즈(HIT) · 노직(HIT) · 샌델(HIT) · 매킨타이어(HIT) · 왈저(HIT) 자유주의·공동체주의 축은 커버되나, **공화주의 축은 전면 공백**으로 구조적 불균형.

### BLK-175E-2025B-005 (TASK-175E-2025-B) — Q10 (을) 이사야 벌린(Isaiah Berlin) ES 미등록 (row 기준 1회째 출제)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2025-B.md` Q10 row (을)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 20세기 자유주의 정치철학 대표자, 『자유의 두 개념(Two Concepts of Liberty, 1958)』 저자, **row 기준 1회째 출제 (2025-B); 이전 2020-A 등에서 묶음 언급은 있었으나 제시문 중심 사상가로는 본 문항이 최초**)
- 사유: Q10 (L181-L185) 제시문 "(나) 을: **'나를 지배하는 자가 누구인가'**라는 물음이 자유의 범위(extent)와 통제의 근원(source)을 구분한다. **간섭의 부재**로서의 **소극적 자유(negative liberty)**가 근대 자유의 핵심이며, 자유의 범위와 통제의 근원을 혼동해서는 안 된다"로 제시문 중심 사상가가 **이사야 벌린(Isaiah Berlin, 1909-1997, 라트비아 리가 출생 영국 옥스퍼드대 정치철학자·사상사가, 올 소울즈 칼리지(All Souls College) 펠로우, 울프슨 칼리지(Wolfson College) 초대 학장, 『자유론(Four Essays on Liberty, 1969)』·『러시아 사상가들(Russian Thinkers, 1978)』·『고슴도치와 여우(The Hedgehog and the Fox, 1953)』 저자, 20세기 자유주의 정치철학·사상사·낭만주의 연구의 거장)**임이 trademark 3중으로 확증됨. canonical thinker_id `berlin`는 ES 미등록 상태. Trademark 3중 일치: ① **"'나를 지배하는 자가 누구인가(Who is master?)'"** 문구 = 벌린 『자유의 두 개념(Two Concepts of Liberty, 1958, 옥스퍼드 취임강연)』 제2장 **적극적 자유(positive liberty) 규정** trademark. 원문 "*The 'positive' sense of the word 'liberty' derives from the wish on the part of the individual to be his own master*" (나 자신의 주인이 되고자 하는 바람 — "Who is master over me?"의 역형식); ② **"소극적 자유(negative liberty) = 간섭의 부재(absence of interference)"** = 벌린 『두 개념』 제1장 정식 정의. "*I am normally said to be free to the degree to which no man or body of men interferes with my activity*"; ③ **"자유의 범위(extent of control)와 통제의 근원(source of control) 구분"** = 벌린 『두 개념』 핵심 구분. 소극적 자유는 **자유의 범위(얼마만큼 간섭받지 않는가)** 문제이고, 적극적 자유는 **통제의 근원(누가 나를 지배하는가)** 문제이며 두 물음은 범주적으로 다름 — 양자를 혼동하면 전체주의(positive liberty의 왜곡)가 자유의 이름으로 정당화될 수 있다는 유명 비판.
- 후속 조치: TASK-176 범위에서 `berlin` 신규 등록 **우선** (20세기 자유주의 정치철학 대표자, 임용시험 자유 개념 비교 출제의 핵심 축, 페팃·비롤리 신로마 공화주의와 대비되는 고전적 자유주의의 정전) — **소극적 자유(negative liberty) — 간섭의 부재** · **적극적 자유(positive liberty) — 자기 주인됨(self-mastery), 합리적 자아의 실현** · **적극적 자유의 전체주의적 왜곡 비판 — 루소 일반의지·헤겔 국가·마르크스주의·전체주의 이데올로기가 적극적 자유의 이름으로 개인을 억압** · **자유의 범위(extent) vs 통제의 근원(source) 범주 구분** · **가치 다원주의(value pluralism) — 근본적 가치들의 양립불가능성(incommensurability)과 비환원성** · **한 가지 진리(monism) 비판 — 완전한 사회·유토피아 불가능성 주장** · **반-본질주의(anti-essentialism) — 인간 본성의 역사적·문화적 다양성 긍정** · **러시아 사상가 연구 — 게르첸(Herzen)·체르니셰프스키(Chernyshevsky)·벨린스키(Belinsky)·투르게네프(Turgenev) 등** · **낭만주의 연구 — 『낭만주의의 뿌리(The Roots of Romanticism, 1999)』 — 반계몽주의의 역사** · **『자유의 두 개념(Two Concepts of Liberty, 1958)』 — 옥스퍼드 취임강연, 20세기 자유주의 정전** · **『자유론(Four Essays on Liberty, 1969)』 — 4개 자유 논문 모음** · **『러시아 사상가들(Russian Thinkers, 1978)』** · **『고슴도치와 여우(The Hedgehog and the Fox: An Essay on Tolstoy's View of History, 1953)』 — 아르킬로코스 경구 기반 지적 유형론** · **『비코와 헤르더(Vico and Herder, 1976)』** · **『반대 흐름(Against the Current, 1979)』 — 반계몽주의 사상가 연구** · **찰스 테일러(Charles Taylor)·로널드 드워킨(Dworkin)·마이클 이그나티에프(Ignatieff) 등 후대 자유주의 정치철학자에 지대한 영향** · **제럴드 코헨(G. A. Cohen)·필립 페팃(Pettit)·스키너(Skinner) 등 공화주의·좌파 자유 이론의 비판 대상이자 대화 상대** · **옥스퍼드 학파 정치사상사 연구 전통의 정초자 — 스키너(Skinner)·포콕(Pocock) 캠브리지 학파에 영향** · **미국 유대인 이민자·홀로코스트 생존자 가족사 — 반전체주의 입장의 개인사적 기초**. 후보 id: `berlin`. 등록 우선순위 **우선** — 임용시험 자유 개념 비교 출제의 핵심 축, 페팃·비롤리 신로마 공화주의와 대비 구조 출제 증가, `mill_js`(밀) HIT · `rawls`(롤즈) HIT · `nozick`(노직) HIT인데 `berlin`만 MISS인 상태는 자유주의 정치철학 ES 커버리지 구조적 공백.
- 영향: Q10 (을) 정답 (벌린 식별 + 소극적 자유 vs 적극적 자유 구분 서술)은 trademark 3중 일치로 확정됨. coverage/2025-B.md Q10 을 본문은 정확하며 ES 커버리지 공백만 존재. **자유주의 정치철학 영역 ES 커버리지 핵심 공백 — `berlin` 등록으로 밀·롤즈·노직·샌델·매킨타이어·왈저·벌린 자유주의/공동체주의 6대 축 완성**.

### BLK-175E-2025B-006 (TASK-175E-2025-B) — Q7 (갑) 사상가 확증 보류 [재정의 2026-04-21 by TASK-175E-2025-B-FIX]
- 일시: 2026-04-21 (최초 등록) · 2026-04-21 FIX에서 재정의
- 위치: `projects/ethics-study/exam-solutions/coverage/2025-B.md` Q7 row (**갑** — 재배치 후)
- 심각도: blocker (**사상가 확증 보류** — 창작 금지 규칙 architecture.md L578/Phase 6 준수)

**재정의 배경**: 최초 판본(2026-04-21 등록)은 Q7 갑=`yiyulgok`·을=임성주/한원진 추정으로 배치하고 "을 사상가 미확정"으로 블로커를 등록하였다. Tester(tester-report-TASK-175E-2025-B.md, BUG-3)가 원문 검증을 통해 지적한 사항:
- **을 원문(L129)**에 등장하는 "**이와 기의 오묘함[理氣之妙]**"은 율곡 『답성호원(答成浩原)』의 대표 trademark ("理氣之妙 難見亦難說")이다.
- **을 원문(L129)**의 "**이의 근원은 하나일 뿐이고, 기의 근원도 하나일 뿐이다. 기가 유행하여 고르지 못하면 이도 유행하여 고르지 못하니**"는 율곡 **이통기국(理通氣局)** 정식 명제이다.
- **을 원문(L129)**의 "**기는 이와 떨어질 수 없고 이도 기와 떨어질 수 없다**"는 율곡 **이기불상리(理氣不相離)** 정식 명제이다.
- 즉 **을 = 율곡(`yiyulgok`, HIT) 확정**. 이에 따라 갑은 율곡이 아닌 다른 사상가로 재확정되어야 한다.

**FIX 후 재배치**:
- Q7 **을 = `yiyulgok`(율곡 이이, 1536-1584)** 확정 — ES HIT. ES-gap 아님.
- Q7 **갑 = 사상가 확증 보류** — 원문 trademark가 단일 사상가로의 배타적 확정을 허용하지 않음. 창작 금지 규칙에 따라 블로커 유지.

**갑 원문 trademark 요약 (L128)**:
- (a) "**기(氣)가 아니면 이(理)는 붙을 데가 없고, 마음이 아니면 이와 기는 붙을 데가 없다**" — 이기불상리(理氣不相離) + 심(心)이 이·기의 담지자.
- (b) "**이(理)는 사덕(四德)의 이이면서 오상(五常)이 되고, 기는 음양오행(陰陽五行)의 기이면서 기질(氣質)이 되니**" — 사덕=오상 + 기질=음양오행의 기 대응.
- (c) "**오상은 순선하고 악이 없어서 그 발한 바가 사단(四端)으로 선하지 않음이 없으며, 기질은 ( ㉠ )이/가 아니어서 그 발한 바가 칠정(七情)이 되고 사악함으로 흐르기 쉽다**" — 사단·칠정 이원 구도.

**후보 검토**:
- **퇴계 이황(`yihwang`, HIT)**: (c)의 "오상=이=사단(순선) / 기질=기=칠정(악 가능)" 이분은 퇴계 **이기호발설(理氣互發說)**과 유사 구도이나, 퇴계 정식은 "이발이기수지·기발이이승지" 양발(兩發)이며 본 갑 원문은 "기질이 ㉠이 아니어서 칠정이 됨"의 단일 설명에 그쳐 완전 일치 아님. 갑=퇴계는 **가능성 있음**이나 배타적 확정 불가.
- **율곡 이이(`yiyulgok`, HIT)**: (a) 이기불상리·(b) 사덕=오상 구도는 율곡 『성학집요』 해석과도 상통. 그러나 을이 이미 율곡으로 확정되었으므로 **갑=율곡은 배제**.
- **한원진(`han_wonjin`, ES 미등록)**: 호론 인물성이론 대표자. 본연지성 3층설(超形氣·因氣質·雜氣質) 정교한 층위 체계와 본 갑 원문의 단순 2층 구도(오상/기질)는 결이 다름. 배타적 trademark 부재.
- **임성주(`im_seongju`, ES 미등록)**: 기일원론(氣一元論). 본 갑 원문은 이·기의 대립적 역할을 명시하고 있어 임성주 일원기 사상과 거리 있음. 배타적 trademark 부재.
- **권상하(`kwon_sanghya`, ES 미등록)·이간(`lee_gan`, ES 미등록)·기타 조선 중기·후기 성리학자**: 원문에 개인명·저서명·제자 언급 없어 배타적 확정 불가.

**ES 실존 여부**: 갑 확증 시 후속 판정 분기:
- 갑 = `yihwang`으로 확증되면 ES HIT → ES-gap 블로커 해소. 이 경우 BLK-006은 닫힘.
- 갑 = `im_seongju`/`han_wonjin` 등 ES 미등록 사상가로 확증되면 ES-gap 유지. 이 경우 BLK-006은 ES-gap 블로커로 유지.
- 원문 한계로 단일 확증 불능 상태이면 BLK-006은 **확증 보류 블로커**로 유지.

- 후속 조치: TASK-176 범위에서 호락논쟁 주요 사상가 `im_seongju`·`han_wonjin`·`lee_gan`·`kwon_sanghya` 일괄 등록 검토 (조선 후기 성리학 ES 공백 해소). 갑 사상가 확증은 임용시험 기출 해설집·한국 성리학사 교재(윤사순·이남영·금장태 등) 교차 확인 후 별도 FIX 태스크에서 진행. 현 시점에서는 창작 금지 규칙에 따라 보류 유지.
- 영향: Q7 **갑 사상가 확증 보류** (FIX 전에는 "을 사상가 미확정"이었으나 재배치 후 갑의 미확정으로 전환). coverage/2025-B.md Q7 본문에 `<!-- BLOCKER: BLK-175E-2025B-006 (재정의 2026-04-21) -->` inline 주석 삽입 완료. 을=yiyulgok 확정으로 고유 thinker_id HIT 10명 / MISS 6건으로 재집계.

### BLK-175E-2026A-001 (TASK-175E-2026-A) — Q3 남명 조식(曺植) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2026-A.md` Q3 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 조선 중기 영남학파 대표 성리학자, **row 기준 최초 출제 (2026-A — grep `cho_sik` coverage/*.md 이전 0건)**)
- 사유: Q3 (L44-L56) 제시문 "**경(敬)과 ㉠**" 대응 + "**해와 달**" 비유 + "**안을 밝히는 것은 경(敬)이고, 밖으로 결단하는 것은 ㉠이다[內明者敬 外斷者義]**" + "**일상에서 경(敬)으로 마음을 지키고 … 단호하게 결단하는 공부**"로 제시문 중심 사상가가 **남명 조식(南冥 曺植, 1501-1572, 조선 중기 성리학자, 경상우도 영남학파의 대표 유학자, 산림처사(山林處士)로 여러 차례 관직을 사양, 『남명집(南冥集)』·『학기유편(學記類編)』 저자, 경의검(敬義劍)·성성자(惺惺子, 방울) 패용으로 상징되는 실천적 수양론의 정점)**임이 trademark 3중으로 확증됨. canonical thinker_id `cho_sik`는 ES 미등록 상태. Trademark 3중 일치: ① "**내명자경 외단자의(內明者敬 外斷者義)**" — 남명 조식 **패검명(佩劍銘)** 정확 일치. 남명이 평생 차고 다녔다는 **경의검(敬義劍)**에 새긴 16자 중 핵심 8자. "*안을 밝히는 것은 경이고, 밖으로 결단하는 것은 의이다*"는 남명 수양론의 trademark 정식. 『주역』 곤괘(坤卦) 문언전 "군자경이직내 의이방외(君子敬以直內 義以方外)"를 받아 **경(敬)·의(義) 쌍수(雙修)**를 실천 원리로 삼음. 정답 ㉠ = **의(義)**; ② "**경(敬)과 ㉠을 해와 달에 비유**" — 남명 조식 『학기유편(學記類編)』·『남명집(南冥集)』의 **경의병진(敬義並進)** 비유 trademark. "경·의는 해와 달 같아서 하나가 없을 수 없다(敬義如日月 不可無一)" 취지의 표현. 경=내면의 정일(精一)한 밝음(日), 의=외면의 단호한 결단(月). 양자는 분리 불가능한 수양의 양륜(兩輪); ③ "**일상에서 경(敬)으로 마음을 지키고 … 단호하게 결단하는 공부**" — 남명 수양론 trademark. 퇴계의 정좌(靜坐)·궁리(窮理) 중심과 대비되는 **경·의 실천 수양론**. 일상(日用)에서 **성성(惺惺 — 또렷이 깨어 있음)**한 경의 마음으로 안을 지키고(內守), 결단의 의로 밖을 바로잡는(外正) 실천적 수양. 성성자(惺惺子, 방울)·경의검(敬義劍)의 물리적 상징이 이 수양론을 증언.
- 후속 조치: TASK-176 범위에서 `cho_sik` 신규 등록 **우선** (조선 중기 성리학 영남학파 대표자, 퇴계(`yihwang`)·율곡(`yiyulgok`) 기호학파와 대비되는 영남우도 실천 수양론의 정전, 임용시험 조선 유학사 출제의 핵심 축) — **경의(敬義) 쌍수(雙修) — 내명자경 외단자의(內明者敬 外斷者義)** · **경(敬) — 내면의 정일한 밝음, 마음을 한 곳에 집중하여 또렷이 깨어 있는 상태(主一無適·整齊嚴肅·惺惺)** · **의(義) — 외면의 단호한 결단, 시비(是非)·선악(善惡)을 가려 옳음을 택하는 실천력** · **성성자(惺惺子, 방울) — 허리에 차고 다니며 방울 소리로 마음의 흐트러짐을 각성시키는 물리적 수양 도구** · **경의검(敬義劍) — 검에 "내명자경 외단자의(內明者敬 外斷者義)" 16자를 새겨 패용, 의(義)의 단호한 결단을 상징** · **산림처사(山林處士) — 여러 차례 관직(전생서 주부·단성현감·상서원 판관·종친부 전첨) 사양, 재야에서 학문과 수양에 전념** · **단성현감 사직소(丹城縣監 辭職疏, 1555) — 명종 모친 문정왕후를 "한 과부(寡婦)"로 지칭하는 파격적 직언으로 조선 유학사 상소문의 정점** · **학기유편(學記類編) — 경·의 수양론의 체계적 정리** · **남명집(南冥集) — 시문·서간·잡저** · **실천 중심 수양론 — 주자학의 궁리·정좌 중심에서 일상 실천·현실 대응으로 중심을 옮김** · **의병장 문인 배출 — 임진왜란 시 곽재우·정인홍·김면 등 남명 문하에서 의병장 다수 배출, 실천 지향성이 역사적 결실로 입증** · **퇴계와의 출처관(出處觀) 대비 — 퇴계 출사(出仕)의 신중한 수용 vs 남명 처사(處士)의 철저한 재야 견지** · **조선 성리학 기호(畿湖)·영남(嶺南) 양대 학맥 중 영남우도의 정점 — 퇴계(영남좌도)·율곡(기호)과 함께 조선 성리학 3대 축**. 후보 id: `cho_sik`. 등록 우선순위 **우선** — 조선 유학사 ES 커버리지 핵심 공백, 퇴계·율곡 HIT인데 남명만 MISS는 영남학파 이원 구조(좌도·우도)의 절반 공백. 임용시험 조선 중기 유학 출제에서 경의 수양론·성성자·경의검·출처관 관련 지문은 배타적으로 남명 조식을 지시함.
- 영향: Q3 정답 ㉠ = **의(義)** + 작성 방법 대응 (남명 조식 경·의 쌍수 수양론, 경의검·성성자 상징, 내명자경 외단자의 패검명, 해·달 비유의 경의병진)은 trademark 3중 일치로 확정됨. coverage/2026-A.md Q3 본문은 정확하며 ES 커버리지 공백만 존재. **조선 유학사 ES 커버리지 공백 — `cho_sik` 등록으로 퇴계·율곡·남명 조선 중기 성리학 3대 축 완성**.

### BLK-175E-2026A-002 (TASK-175E-2026-A) — Q6 turiel + Q12 taylor_p 누적 갱신
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2026-A.md` Q6 (갑=turiel), Q12 (갑=taylor_p)
- 심각도: blocker (ES 커버리지 누락 — 누적 재출제로 미등록 공백 심화, **row 기준: turiel = 2026-A 포함 5회째 출제 / taylor_p = 2026-A 포함 3회째 출제**)
- 사유 (turiel): Q6 (L90-L105) 제시문 (가) "**갑: 도덕 판단과 사회인습 판단은 서로 다른 영역에 속한다. 도덕 영역은 타인의 복지·권리·공정성에 관한 것이고, 사회인습 영역은 특정 사회의 합의·관행·규범에 관한 것이다. 아이들은 이 두 영역을 명확히 구별한다**"로 제시문 중심 사상가가 **엘리엇 튜리엘(Elliot Turiel, 1938-, 미국 UC 버클리 교육심리학자·도덕발달 심리학자, 콜버그 인지발달 계승·수정, 『The Development of Social Knowledge: Morality and Convention, 1983』 저자, **사회영역이론(Social Domain Theory)** 정초자)**임이 trademark로 확증됨. canonical thinker_id `turiel`는 ES 미등록 상태. Trademark: ① **"도덕 영역(moral domain) vs 사회인습 영역(societal-conventional domain) 구분"** — 튜리엘 사회영역이론 정식 명제. 콜버그의 단일 인지발달 단계론을 수정, 도덕·사회인습·개인 3영역을 발달적으로 구별되는 지식 영역으로 제시; ② **"타인의 복지·권리·공정성(welfare·rights·fairness) 관련 = 도덕"** vs **"특정 사회의 합의·관행(social convention) 관련 = 사회인습"** — 튜리엘 영역 구분의 정의적 기준; ③ **"아이들은 이 두 영역을 명확히 구별한다"** — 튜리엘 실증 연구 핵심 결과. 3-4세부터 도덕 위반(때리기·훔치기)과 인습 위반(식탁 예절·복장)을 판단 기준·권위 의존성·보편성·불변성 5차원에서 구별. 이전 출제 이력: 2019-B·2021-A·2022-A·2024-A 4회. 2026-A = 5회째.
- 사유 (taylor_p): Q12 (L198-L213) 제시문 "**갑: 도덕 행위자가 아닌 모든 생명체도 그 자신의 선(善, its own good)을 추구하는 목적론적 삶의 중심(teleological center of life)이다. 모든 생명체는 고유한 선을 가지며, 인간은 다른 생명체에 대해 도덕적 의무를 진다. … 불간섭(noninterference)·불침해(nonmaleficence)·신의(fidelity)·보상적 정의(restitutive justice)**"로 제시문 중심 사상가가 **폴 W. 테일러(Paul W. Taylor, 1923-2015, 미국 브루클린 칼리지 환경윤리 철학자, 『Respect for Nature: A Theory of Environmental Ethics, 1986』 저자, **생명중심주의(biocentrism)**·**개별 생명 존중의 환경윤리** 정초자)**임이 trademark 3중으로 확증됨. canonical thinker_id `taylor_p`는 ES 미등록 상태 (**동명이인 suffix 규약 — architecture.md:491 — 기존 `taylor`는 Charles Taylor 공동체주의자로 이미 ES HIT 등록되어 있으므로 Paul Taylor는 반드시 `taylor_p` suffix 사용**). Trademark 3중 일치: ① **"목적론적 삶의 중심(teleological center of life)"** — 테일러 『Respect for Nature』 제3장 정의적 명제. 모든 개별 생명체(식물·동물 포함)가 자기 고유의 선(its own good)을 실현하려는 목적 지향적 활동의 중심이라는 생명 존재론; ② **"고유한 선(its own good) — 도덕적 고려 가능성(moral considerability)의 근거"** — 테일러 생명중심주의 정식. 감각·의식이 아닌 "자기 선 추구" 자체가 도덕적 고려의 기준. 이 점에서 싱어(Singer)의 쾌고감수(sentience) 기준·리건(Regan)의 삶의 주체(subject-of-a-life) 기준보다 외연 확장 (모든 생명 = 식물·미생물 포함); ③ **"불간섭(noninterference)·불침해(nonmaleficence)·신의(fidelity)·보상적 정의(restitutive justice) 4원칙"** — 테일러 『Respect for Nature』 제6장 **자연 존중의 4가지 의무 규칙(rules of duty)** 정확 일치. 인간이 자연의 생명체에 지는 도덕적 의무 체계. 이전 출제 이력: 2020-B·2023-A 2회. 2026-A = 3회째.
- 후속 조치: TASK-176 범위에서 `turiel` + `taylor_p` 신규 등록 **우선** (도덕심리·환경윤리 임용시험 핵심 축, 콜버그·길리건·레스트 HIT·싱어·레건 HIT 예정인데 `turiel`만 MISS는 도덕발달 영역 구조적 공백 / Charles Taylor `taylor` HIT인데 Paul Taylor `taylor_p` MISS는 환경윤리 생명중심주의 정점 공백). 등록 시 **동명이인 suffix 규약 엄수 — 반드시 `taylor_p` (Paul)로 등록하고 기존 `taylor` (Charles)와 분리**. 후보 id: `turiel`, `taylor_p`.
- 영향: Q6 정답 작성 방법 대응 (튜리엘 도덕/사회인습 영역 구분, 콜버그 계승·수정, 3영역 이론) + Q12 갑 정답 (폴 테일러 생명중심주의, 목적론적 삶의 중심, 4원칙)은 trademark 일치로 확정됨. coverage/2026-A.md Q6·Q12 본문은 정확하며 ES 커버리지 공백만 존재. **도덕심리·환경윤리 ES 커버리지 누적 갱신 — 5회째·3회째 출제에도 미등록 상태 지속은 구조적 공백**.

### BLK-175E-2026A-003 (TASK-175E-2026-A) — Q12 알도 레오폴드(Leopold) ES 미등록
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2026-A.md` Q12 row (**을**)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 20세기 미국 환경윤리·생태학 정초자, **대지윤리(Land Ethic)** 창시자, **row 기준 최초 출제 (2026-A — grep `leopold` coverage/*.md 이전 0건)**)
- 사유: Q12 (L198-L213) 제시문 "**(나) 을: 윤리의 외연은 확장되어 왔다. 처음에는 개인 사이에 … 나중에는 사회와 개인 사이에 … 이제 인간과 대지(land) 사이의 관계를 포괄해야 한다. 대지 공동체(land community)의 온전성(integrity)·안정성(stability)·아름다움(beauty)을 보전하는 것은 옳고, 그렇지 않은 것은 그르다. 대지는 자원이 아니라 우리가 속한 공동체이다**"로 제시문 중심 사상가가 **알도 레오폴드(Aldo Leopold, 1887-1948, 미국 야생생물학자·환경윤리학자·산림학자·위스콘신대 야생관리학 교수, 『모래군(郡)의 열두 달(A Sand County Almanac, 1949, 사후 출판)』 저자, **대지윤리(Land Ethic)**·**전체론적 환경윤리(holistic environmental ethics)** 정초자)**임이 trademark 3중으로 확증됨. canonical thinker_id `leopold`는 ES 미등록 상태. Trademark 3중 일치: ① **"윤리의 외연 확장 — 개인→사회→대지(land)"** — 레오폴드 『모래군의 열두 달』 「The Land Ethic」 장 정식 명제. 윤리 공동체의 점진적 확장 역사관: 노예제 철폐 → 사회계약적 민주주의 → 대지윤리는 "**윤리적 지평의 제3단계**"로서 인간·동식물·토양·물을 포괄하는 생태 공동체로의 확장; ② **"대지 공동체(land community)의 온전성·안정성·아름다움(integrity, stability, beauty)을 보전하는 것이 옳다"** — 레오폴드 **대지윤리의 황금률(the golden rule of land ethic)** 정확 일치. 원문 "*A thing is right when it tends to preserve the integrity, stability, and beauty of the biotic community. It is wrong when it tends otherwise.*" 20세기 환경윤리의 가장 유명한 경구, 전체론(holism)적 환경윤리의 정전; ③ **"대지는 자원이 아니라 공동체(land as community, not commodity)"** — 레오폴드 대지윤리 정식 선언. 인간을 **"생명 공동체의 정복자(conqueror)에서 구성원·시민(plain member and citizen)으로" 전환**시키는 윤리적 태도 변화 요구. 테일러(`taylor_p`)의 개별 생명체 중심 생명중심주의와 대비되는 **전체론적 대지·생태계 중심 환경윤리**의 정점.
- 후속 조치: TASK-176 범위에서 `leopold` 신규 등록 **우선** (환경윤리 임용시험 핵심 축, 생명중심주의 테일러(`taylor_p`, MISS)·심층생태학 네스(`naess`, 미등록)·자연중심주의 싱어(`singer`, 미등록)와 함께 환경윤리 4대 축 중 최다 출제 사상가, 2022개정 교육과정 "생명과 윤리" 단원 필수 지문) — **대지윤리(Land Ethic) — 윤리적 공동체의 대지(생태계·토양·물·식물·동물) 전체로의 확장** · **대지의 피라미드(biotic pyramid) — 먹이사슬·에너지 흐름·생태계 구조의 기초 생태학 개념** · **전체론적 환경윤리(holism) — 개별 생명보다 생태 공동체 전체의 선을 우선, 캘리코트(Callicott) 등 후계자 계승** · **대지윤리의 황금률 — "온전성·안정성·아름다움 보전(integrity, stability, beauty)"** · **"생명 공동체의 정복자에서 구성원·시민으로" 전환 — 인간의 윤리적 지위 재정립** · **"산처럼 생각하기(Thinking Like a Mountain)" — 늑대 사살 경험과 생태 의식 각성의 유명 에세이** · **생태학적 양심(ecological conscience) — 법·규제가 아닌 내재적 윤리 감수성에 기반한 자연 보호** · **모래군의 열두 달(A Sand County Almanac, 1949) — 사후 출판된 환경 에세이집, 20세기 환경운동의 성경** · **위스콘신 황폐 농장 복원(The Shack) — 직접 황폐지를 매입해 생태 복원 실천, 이론과 실천의 통합** · **미국 산림청(U.S. Forest Service) 산림감독관 경력 — 뉴멕시코·애리조나 길라 원시보호구역(Gila Wilderness, 1924) 지정 주도, 미국 최초 공식 원시보호구역** · **야생관리학(wildlife management) 정초 — 위스콘신대 교수로 야생관리학 분과 창설** · **카슨(Rachel Carson) 『침묵의 봄』·네스(Arne Naess) 심층생태학·캘리코트(J. Baird Callicott) 철학적 대지윤리 등 후대 환경운동·환경철학 전반에 결정적 영향** · **테일러(Paul Taylor) 개별 생명중심 vs 레오폴드 전체론 대조는 환경윤리 입문의 핵심 대비 구도**. 후보 id: `leopold`. 등록 우선순위 **우선** — 환경윤리 최다 출제 사상가 미등록은 ES 커버리지 최악의 구조적 공백, `taylor_p`(생명중심주의)·`leopold`(대지윤리) 양대 축 동시 등록이 환경윤리 영역 정상화의 최소 요건.
- 영향: Q12 을 정답 (레오폴드 대지윤리, 윤리 외연 확장, 온전성·안정성·아름다움 황금률, 대지 공동체) + 갑·을 비교 서술 (테일러 개별 생명중심 vs 레오폴드 전체론적 대지윤리)은 trademark 3중 일치로 확정됨. coverage/2026-A.md Q12 본문은 정확하며 ES 커버리지 공백만 존재. **환경윤리 ES 커버리지 최우선 공백 — `leopold` 등록으로 환경윤리 전체론 축 확립, `taylor_p`와 함께 생명중심/전체론 대비 구도 완성**.

### BLK-175E-2026B-001 (TASK-175E-2026-B) — ★ Q5 앨버트 반두라(Albert Bandura) ES 미등록 — **6회째 출제 + 2024-B→2025-B→2026-B 3연속 (임용시험 도덕심리 사회인지 영역 최장 연속 기록 경신) — 최우선 격상** ★
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2026-B.md` Q5 row
- 심각도: **blocker (최우선)** — ES 커버리지 누락 누적 최악 사례. 20세기 사회인지 심리학 정초자, 임용시험 도덕심리 영역 최다 출제 중 하나, **row 기준 6회째 출제 (2014-A · 2019-A · 2020-A · 2024-B · 2025-B · 2026-B) + 3년 연속 출제 (2024-B→2025-B→2026-B)로 임용시험 도덕·윤리에서 동일 사상가가 3년 연속 MISS 상태로 출제된 최초 사례 — 구조적 공백 극단화**
- 사유: Q5 (L88-L101) 제시문 "**개인(person)·행위(behavior)·( ㉠ )의 상호작용으로 인간의 행동을 설명** … **사회인지 이론(Social Cognitive Theory)** … **자기 조절 기제 … 도덕적 자기 ( ㉡ )** … **도덕적 이탈(moral disengagement)**" + "**(1) 도덕적 정당화(moral justification) · (2) 유리한 비교(advantageous comparison) · (3) 완곡한 표현(euphemistic labeling)**" + "**(4) 결과에 대한 축소·무시·왜곡(minimizing, ignoring, misconstruing consequences)**" + "**(5) 비인간화(dehumanization) · (6) 비난의 귀인(attribution of blame)**" + "**(7) 책임 전가(displacement of responsibility) · (8) 책임 분산(diffusion of responsibility)**"으로 제시문 중심 사상가가 **앨버트 반두라(Albert Bandura, 1925-2021, 캐나다 출신 미국 스탠퍼드대 심리학자, 20세기 후반~21세기 초 세계 가장 영향력 있는 심리학자로 평가, 사회학습이론·사회인지이론·자기효능감·보보인형 실험·도덕적 이탈이론 정초자)**임이 **trademark 4중으로 확증**됨. canonical thinker_id `bandura`는 ES 미등록 상태. Trademark 4중 일치: ① **"개인·행위·환경의 상호작용 — 삼원상호결정론(Triadic Reciprocal Determinism / Reciprocal Determinism)"** = 반두라 『Social Foundations of Thought and Action: A Social Cognitive Theory, 1986』 정식 명제. 인간 행동은 개인(P, person)·행동(B, behavior)·환경(E, environment) 3요소의 상호 결정 관계로 설명됨. 행동주의(환경→행동 단일 인과)도 인지주의(개인→행동 단일 인과)도 아닌 3요소 상호 결정 모형 — 반두라 이론의 metatheoretical trademark. ㉠ = **환경(環境 — environment)**; ② **"도덕적 자기 제재(moral self-sanctions) + 자기 조절 기제(self-regulatory mechanisms)"** = 반두라 사회인지 도덕 이론의 핵심. 개인은 자기 행동을 스스로 평가하고 도덕적 기준에 위배될 때 **자기 비난·수치·죄책감 등 내적 제재(self-censure)**를 가함으로써 도덕 행동을 자기 조절. ㉡ = **제재(制裁 — sanction)** 또는 **자기 제재(self-sanction)**; ③ **"도덕적 이탈(moral disengagement)"** = 반두라 『Moral Disengagement: How People Do Harm and Live with Themselves, 2016』 및 1999 논문 "Moral Disengagement in the Perpetration of Inhumanities" 정식 trademark. 도덕적 자기 제재가 **선택적으로 무력화(selectively disengaged)**되어 비인도적 행위를 정당화할 수 있는 심리 기제; ④ **"8가지 도덕적 이탈 기제 = 4영역"** = 반두라 정식 체계 완전 일치. 4영역 = (A) **행위의 재구성(reconstruing conduct)** — ①도덕적 정당화·②유리한 비교·③완곡한 표현; (B) **행위자의 책임 모호화(obscuring personal agency)** — ⑦책임 전가·⑧책임 분산; (C) **결과 왜곡(misrepresenting consequences)** — ④결과 축소·무시·왜곡; (D) **피해자 탈인격화(dehumanizing/blaming victim)** — ⑤비인간화·⑥비난의 귀인. 본 원문 8가지 기제 명시 + 제목어 일치는 **반두라에 배타적으로 귀속** — 다른 사상가와 혼동 불가능.
- 후속 조치: TASK-176 범위에서 `bandura` 신규 등록 **최우선 격상** (임용시험 도덕·윤리 도덕심리 영역 최다 출제, 3년 연속 MISS 출제는 ES 커버리지 최악의 구조적 공백, 2022 개정 도덕과 교육과정 "도덕 발달·인격 형성" 단원 필수 지문) — **사회학습이론(Social Learning Theory, 1977)**·**사회인지이론(Social Cognitive Theory, 1986)** — 행동주의에서 인지적 사회학습으로의 전환점, 관찰학습(observational learning)·모방학습(modeling)·대리학습(vicarious learning) 체계화 · **관찰학습 4단계 — 주의(attention)·파지(retention)·운동재생(motor reproduction)·동기화(motivation)** · **보보인형 실험(Bobo doll experiment, 1961·1963·1965)** — 아동이 성인 모델의 공격적 행동을 관찰 후 모방하는 실험, 공격성의 사회학습 입증 · **삼원상호결정론(Triadic Reciprocal Determinism)** — 개인·행동·환경 3요소의 상호 결정 · **자기효능감(self-efficacy, 1977)** — "자신이 특정 과제를 성공적으로 수행할 수 있다는 신념" · **자기효능감 4원천 — 성취경험(performance accomplishments)·대리경험(vicarious experience)·언어적 설득(verbal persuasion)·생리적·정서적 상태(physiological/affective states)** · **자기조절(self-regulation) 3하위과정 — 자기관찰(self-observation)·자기판단(judgmental process)·자기반응(self-reaction)** · **도덕적 자기 제재(moral self-sanctions)** · **도덕적 이탈(moral disengagement, 1999/2016)** — 자기 제재가 선택적으로 무력화되는 심리 기제 · **8가지 도덕적 이탈 기제 4영역** (행위 재구성·책임 모호화·결과 왜곡·피해자 탈인격화) · **대리 인격(agentic perspective) — 인간은 단순 반응자가 아니라 자기 삶의 주체(proactive agent)** · **4가지 주체성 핵심 특성 — 의도성(intentionality)·예기성(forethought)·자기반응성(self-reactiveness)·자기성찰성(self-reflectiveness)** · **집단적 효능감(collective efficacy)** · **『Self-Efficacy: The Exercise of Control, 1997』** · **『Social Foundations of Thought and Action: A Social Cognitive Theory, 1986』** · **『Moral Disengagement: How People Do Harm and Live with Themselves, 2016』** · **스탠퍼드대 심리학과 교수(1953-2021), APA 회장(1974)** · **20세기 심리학 영향력 3위 (스키너·프로이트 이어 3위; Haggbloom et al., 2002)** · **콜버그 인지발달론과 대비 — 콜버그 단계 이론의 '비도덕적 행동' 설명 한계를 사회인지 관점에서 보완 · 길리건·레스트·튜리엘과 함께 도덕심리학 4대 축 (콜버그·반두라·길리건·튜리엘/레스트)**. 후보 id: `bandura`. 등록 우선순위 **최우선 격상** — **2024-B → 2025-B → 2026-B 3년 연속 출제**는 어떤 사상가도 달성하지 못한 연속 기록이며, ES 미등록 상태 지속은 구조적 공백의 극단화 사례. TASK-176 등록 우선순위 최고 등급으로 격상 필수.
- 영향: Q5 정답 ㉠ = **환경**, ㉡ = **제재(자기 제재)** + 8가지 도덕적 이탈 기제 4영역 서술은 trademark 4중 일치로 확정됨. coverage/2026-B.md Q5 본문은 정확하며 ES 커버리지 공백만 존재. **도덕심리 사회인지 영역 ES 커버리지 최악 공백 — `bandura` 등록으로 콜버그·길리건·레스트(HIT) 기존 도덕심리 축에 사회인지 축 추가, 임용시험 최다 출제 사상가 중 하나의 구조적 공백 해소**.

### BLK-175E-2026B-002 (TASK-175E-2026-B) — Q9 보조국사 지눌(知訥) ES 미등록 (**3회째 출제 + 2025-B→2026-B 2연속, 맑은 구슬 비유 신규 trademark**)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2026-B.md` Q9 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 고려 조계종(曹溪宗) 개창자, 한국 선불교(禪佛敎) 사상체계 정립자, **row 기준 3회째 출제 (2021-B · 2025-B · 2026-B) + 2025-B→2026-B 2연속 재출제 확증 — BLK-175E-2025B-001 누적 별도 독립 블로커**)
- 사유: Q9 (L163-L177) 제시문 "**정(定)과 혜(慧) … 삼학(三學) … ( ㉠ ), 정, 혜** (계=戒)" + "**자성정혜(自性定慧)**" + "**수상정혜(隨相定慧)**" + "**공적영지(空寂靈知)**" + "**돈오(頓悟) … 점수(漸修)**" + "**맑은 구슬(淸珠) 비유 … 검은 구슬과 대비**"로 제시문 중심 사상가가 **보조국사 지눌(普照國師 知訥, 1158-1210)**임이 **trademark 6중으로 확증**됨. canonical thinker_id `jinul`는 ES 미등록 상태. Trademark 6중 일치: ① **"계·정·혜 삼학(戒定慧 三學)"** — 불교 수행 3대 범주이나 지눌은 『권수정혜결사문』·『수심결』에서 정혜쌍수(定慧雙修)를 축으로 삼학 통합 수행론 제시. ㉠ = **계(戒 — precepts, śīla)**; ② **"자성정혜(自性定慧)"** — 지눌 『수심결』·『권수정혜결사문』 정식. 마음의 본성(自性)에 본래 구족된 정(定, 적적寂寂)과 혜(慧, 성성惺惺)의 작용; ③ **"수상정혜(隨相定慧)"** — 지눌 『법집별행록절요병입사기』·『수심결』 trademark. 경계(相)에 따라 방편으로 닦는 정혜, 자성정혜에 대비되는 수행 단계. 자성정혜(본래 구족)·수상정혜(방편 수행)의 이원 구조는 지눌 사상의 배타적 trademark; ④ **"공적영지(空寂靈知)"** — 지눌 『수심결』 핵심 명제 "공적영지지심(空寂靈知之心)". 마음의 본성이 공적(空寂, 비어 고요함)하면서도 영지(靈知, 신령한 앎)를 지님. 공(空)과 지(知)의 불이(不二) 구조. 종밀(宗密)의 화엄선 계승이자 지눌 선교일치 사상의 핵심; ⑤ **"돈오점수(頓悟漸修)"** — 지눌 중기 사상 대표. 깨달음(頓悟)은 한순간에 오되, 습기(習氣)를 제거하는 닦음(漸修)은 점진적으로 이루어짐. 『수심결』의 정식 교설; ⑥ **"맑은 구슬(淸珠) · 검은 구슬 비유"** — 지눌 『수심결』 정식 비유. 맑은 구슬은 본래의 자성청정심, 검은 구슬은 번뇌에 물든 마음. 본래 맑은 구슬이 흙탕물에 들어가면 혼탁하게 보이나 흙탕물을 맑히면 본래의 맑음이 드러남 — 본각(本覺)·시각(始覺)·구경각(究竟覺)의 단계 비유. **2026-B 신규 trademark** (2021-B·2025-B에는 등장하지 않음).
- 후속 조치: TASK-176 범위에서 `jinul` 신규 등록 **우선 격상** — 2021-B·2025-B·2026-B **3회 누적** + 2025-B→2026-B **2연속** 재출제는 한국 불교 ES 커버리지 공백의 심각도 격상 신호. 등록 시 trademark 키워드: **고려 조계종(曹溪宗) 개창** · **정혜쌍수(定慧雙修)** · **자성정혜(自性定慧)** · **수상정혜(隨相定慧)** · **공적영지(空寂靈知)** · **돈오점수(頓悟漸修)** · **돈오돈수(頓悟頓修)** (말기 사상) · **간화선(看話禪)** · **교선일치(敎禪一致)** · **『수심결(修心訣)』** · **『권수정혜결사문(勸修定慧結社文)』** · **『법집별행록절요병입사기(法集別行錄節要幷入私記)』** · **『간화결의론(看話決疑論)』** · **『원돈성불론(圓頓成佛論)』** · **선지식(善知識)** · **심외무불(心外無佛)·성외무법(性外無法)** · **맑은 구슬(淸珠) 비유** · **본각(本覺)·시각(始覺)·구경각(究竟覺)** · **원효·의상·지눌·휴정 한국 불교 4대 사상가** · **종밀(宗密) 화엄선 계승** · **혜능 조계 선종의 한국적 전개** · **수선사(修禪社) 결사운동**. 후보 id: `jinul`. 등록 우선순위 **우선 격상** — 한국 선불교 사상사 핵심 인물, 3회 누적·2연속 재출제로 임용시험 한국 불교 영역 필수 등록.
- 영향: Q9 정답 ㉠ = **계(戒)** + 자성정혜·수상정혜·공적영지·돈오점수·맑은 구슬 비유 서술은 trademark 6중 일치로 확정됨. coverage/2026-B.md Q9 본문은 정확하며 ES 커버리지 공백만 존재. BLK-175E-2025B-001 누적 갱신과 함께 본 BLK-175E-2026B-002는 독립 2026-B 블로커로 등록 — TASK-176에서 단일 `jinul` 등록으로 병합 해소. **한국 선불교 ES 커버리지 공백 — `jinul` 등록으로 원효(HIT)·지눌 양축 성립, 한국 불교 4대 사상가 중 절반 확보**.

### BLK-175E-2026B-003 (TASK-175E-2026-B) — Q3 서사 도덕교육(narrative moral education) 사상가 특정 불능 — 창작 금지 규칙에 따른 보류
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2026-B.md` Q3 row
- 심각도: blocker (**사상가 확증 보류** — 창작 금지 규칙 architecture.md L578/Phase 6 준수)
- 사유: Q3 (L37-L68) 제시문은 **"도덕적 문제 사례 → 주제 확인 질의응답 → 주인공의 느낌 추론 → 유사 경험 발표 → 이야기 만들기"의 5단계 서사 도덕교육 수업 모형** + "**저자의식(authorship)**" + "**도덕적 권위와 ( ㉠ ) 형성**" trademark를 포함. '저자의식(authorship)' 영문 병기는 **타피(Mark B. Tappan)·브라운(Lyn Mikel Brown) 1989, "Stories Told and Lessons Learned: Toward a Narrative Approach to Moral Development and Moral Education" (Harvard Educational Review, 59:2)** 서사 도덕교육 프레임의 trademark. 그러나 본 문항은 **한국 교과교육학 맥락의 정형화된 5단계 수업 모형**으로 제시되어 있어 다음 후보들 중 단일 사상가로의 배타적 확정이 불가능: ① **타피·브라운(Tappan & Brown, 1989)** — 저자의식 개념 직접 제시자, 그러나 5단계 수업 모형은 아님; ② **비비안 페일리(Vivian Paley)** — 유아 도덕교육 스토리텔링 실천가, 5단계 수업 모형 비유사; ③ **킬패트릭(William Kilpatrick)** — 『Why Johnny Can't Tell Right From Wrong: And What We Can Do About It(1992)』 서사 인격 교육 주창, 5단계 모형은 부재; ④ **맥킨타이어(Alasdair MacIntyre, `macintyre` HIT)** — 서사적 자아(narrative self) 개념 원류이나 구체 교육 모형 아님; ⑤ **노딩스(Nel Noddings, `noddings` HIT)** — 배려 윤리 스토리텔링, 5단계 모형 부재; ⑥ **한국 교과교육학 독자 모형** — 타피·브라운 프레임을 수용한 한국 교육과정·지도서의 5단계 정형화(도입→전개→정리). 원문에 개인명·저서명이 명시되지 않아 **단일 사상가로의 배타적 확정 불가**. 창작 금지 규칙(architecture.md L578)에 따라 보류.
- 후속 조치: TASK-176 범위 밖. 별도 FIX 태스크에서 ① 임용시험 기출 해설집(한국교육과정평가원 공식 해설 또는 상업 해설서), ② 도덕과 교육과정 해설, ③ 교과교육학 교재(추병완·박병기 등) 교차 확인 후 단일 사상가 확증 또는 "한국 교과교육학 수업 모형(서사적 접근)"으로 최종 귀속. 현 시점에서는 사상가 확증 불능 보류 유지. coverage/2026-B.md Q3 row에 `<!-- BLOCKER: BLK-175E-2026B-003 -->` inline 주석 기입 권고.
- 영향: Q3 정답 작성 방법 대응 (서사 도덕교육 5단계 수업 모형 + 저자의식 형성 + 도덕적 상상력 발달) **내용은 정확**하나 **사상가 귀속만 보류**. coverage/2026-B.md Q3 본문은 교과교육학 범주로 처리되며 ES-gap 블로커는 아니고 **사상가 확증 보류 블로커**. 단일 thinker_id 귀속 요구하지 않는 서술 구조로 작성 완료.

### BLK-175E-2026B-004 (TASK-175E-2026-B) — Q6 (나) 조지프 슘페터(Joseph A. Schumpeter) ES 미등록 (**row 기준 최초 출제**)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2026-B.md` Q6 row (나)
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 미등록, 20세기 정치경제학·민주주의 이론 대표자, 오스트리아-헝가리 제국 출신 미국 하버드대 경제학자·사회학자, **row 기준 최초 출제 (2026-B — grep `schumpeter` coverage/*.md 이전 0건)**)
- 사유: Q6 (L105-L121) 제시문 "**(나) ( ㉡ )은/는 하나의 정치적 방법(political method)이다. 곧 정치적(입법적·행정적) 결정에 도달하기 위한 제도적 장치이다. 이 장치 내에서 특정한 개인들이 국민의 표(people's vote)를 얻기 위해 경쟁적으로 투쟁함으로써 결정을 내릴 권력을 획득한다. 정치인들은 국민의 표를 얻기 위한 경쟁적 수단으로 … 민주주의는 고전적 관념처럼 '인민의 자치(self-government of the people)'가 아니라 정치 엘리트들의 경쟁을 통한 결정 메커니즘이다**"로 제시문 중심 사상가가 **조지프 슘페터(Joseph Alois Schumpeter, 1883-1950, 오스트리아-헝가리 제국 모라비아 출생 미국 하버드대 경제학자·사회학자·정치경제학자, 『경제 발전의 이론(Theorie der wirtschaftlichen Entwicklung, 1911/영역 1934)』·『자본주의·사회주의·민주주의(Capitalism, Socialism and Democracy, 1942)』·『경제분석의 역사(History of Economic Analysis, 사후 1954)』 저자, **창조적 파괴(creative destruction)**·**혁신 이론(innovation theory)**·**경쟁적 엘리트 민주주의(competitive elitist democracy) / 절차적 민주주의(procedural democracy)** 정초자)**임이 **trademark 3중으로 확증**됨. canonical thinker_id `schumpeter`는 ES 미등록 상태. Trademark 3중 일치: ① **"민주주의는 정치적 방법 / 제도적 장치(institutional arrangement)"** = 슘페터 『자본주의·사회주의·민주주의』 제21장 "또 다른 민주주의 이론(Another Theory of Democracy)" 정식 정의. "*democracy is a political method, that is to say, a certain type of institutional arrangement for arriving at political—legislative and administrative—decisions*"의 직접 한역; ② **"정치인들이 국민의 표를 얻기 위해 경쟁적으로 투쟁 → 결정 권력 획득"** = 슘페터 **경쟁적 엘리트 민주주의** 정식. "*the democratic method is that institutional arrangement for arriving at political decisions in which individuals acquire the power to decide by means of a competitive struggle for the people's vote*" — 『CSD』 22장. 고전적 민주주의 이론(루소 일반의지·인민주권)을 **사실에 맞지 않는다**고 비판하고, **경쟁 선거(competitive elections)**를 민주주의의 핵심 메커니즘으로 재정의; ③ **"고전적 관념(classical doctrine)의 '인민의 자치(self-government of the people)' 비판"** = 슘페터 『CSD』 21장의 명제. 고전적 민주주의 이론은 (a) 공동선(common good)의 존재, (b) 공동선을 인식하는 합리적 시민의 존재, (c) 인민 의지의 존재를 전제하나 모두 사실과 다름 — 인민의 자치는 허구이며 **실제 민주주의는 지도자(엘리트) 선택을 위한 경쟁 메커니즘**이라는 현실주의적 민주주의론. Q6 (가) 루소 일반의지·주권 양도불가와의 **고전(루소)·경쟁적 엘리트(슘페터) 민주주의 대비 구도** 출제.
- 후속 조치: TASK-176 범위에서 `schumpeter` 신규 등록 **우선** (20세기 정치경제학·민주주의 이론 대표자, 자본주의·사회주의·민주주의 3대 체제 비교 이론의 정초자, 혁신 이론·창조적 파괴로 경영학·경제성장론에도 지대한 영향, 달(Robert Dahl)·립셋(Lipset)·헌팅턴(Huntington) 등 후대 민주주의 경험 이론의 원류) — **경쟁적 엘리트 민주주의(competitive elitist democracy)** · **절차적 민주주의(procedural democracy) — 고전적 실체적 민주주의와 대비** · **민주주의 = 정치적 방법(political method) / 제도적 장치(institutional arrangement)** · **고전적 민주주의 이론 비판 — 공동선·인민의지·합리적 시민 3전제 부정** · **창조적 파괴(creative destruction) — 혁신에 의한 낡은 구조의 파괴와 새로운 구조의 창출, 자본주의 역동성의 핵심** · **기업가(entrepreneur) 이론 — 혁신의 담지자, 새로운 결합(new combinations) 실현자** · **혁신(innovation) 5유형 — 신제품·신생산방법·신시장·신원료·신조직** · **경제 발전 5단계 — 순환적 흐름·혁신·기업가의 등장·신용·경기순환** · **자본주의의 필연적 쇠퇴 예측 — 합리화·관료화로 기업가 정신 소멸, 지식인 계층의 자본주의 비판, 사회주의로의 이행** · **『경제 발전의 이론(Theorie der wirtschaftlichen Entwicklung, 1911)』 — 혁신·기업가·창조적 파괴 체계화** · **『자본주의·사회주의·민주주의(Capitalism, Socialism and Democracy, 1942)』 — 20세기 정치경제학 정전, 3부(마르크스·자본주의·사회주의·민주주의) 구성** · **『경기순환(Business Cycles, 1939)』 — 콘드라티예프 장기파동·쥐글라르 파동·키친 파동 통합** · **『경제분석의 역사(History of Economic Analysis, 1954)』 — 사후 출판, 경제사상사 최고봉** · **오스트리아학파(Austrian School)에서 출발, 후기에는 독자적 노선 — 뵘-바베르크(Böhm-Bawerk)·비저(Wieser) 제자, 케인즈와 동시대 라이벌** · **오스트리아 재무장관(1919)·본대학 교수·하버드대 교수(1932-1950)** · **달(Robert Dahl) 『민주주의 이론 서론(A Preface to Democratic Theory, 1956)』·『폴리아키(Polyarchy, 1971)』에서 슘페터 경쟁적 민주주의 계승·비판** · **새뮤얼슨(Paul Samuelson)·토빈(Tobin) 등 수학적 경제학과 대비되는 사회학적·역사적 경제학 전통 계승** · **혁신을 통한 자본주의 역동성 이해는 현대 경영학·기업가 이론의 고전** · **루소 일반의지·인민주권 고전적 민주주의와의 대비 구도는 정치철학 민주주의론의 필수 대립 축**. 후보 id: `schumpeter`. 등록 우선순위 **우선** — 정치철학 민주주의 영역 ES 커버리지 공백, 루소(HIT)·밀(HIT)·롤즈(HIT) 계열은 등록되어 있으나 경쟁적 엘리트 민주주의·절차적 민주주의 축은 전면 공백. 임용시험 민주주의 이론 비교 출제 시 필수 대립 항목.
- 영향: Q6 (나) 정답 ㉡ = **민주주의(民主主義 — democracy)** + 경쟁적 엘리트 민주주의·정치적 방법·제도적 장치·정치인의 득표 경쟁 서술은 trademark 3중 일치로 확정됨. coverage/2026-B.md Q6 본문은 정확하며 ES 커버리지 공백만 존재. Q6은 (가) 루소·(나) 슘페터 민주주의 이론 대비로, 루소(HIT) × 슘페터(MISS) 비대칭 상태에서 완전 대비 서술 불가능. **정치철학 민주주의 영역 ES 커버리지 공백 — `schumpeter` 등록으로 고전/경쟁적 엘리트 민주주의 대비 축 성립**.

### BLK-175E-2026B-005 (TASK-175E-2026-B) — Q7 신로마 공화주의 [페팃(Pettit) 1순위 / 비롤리(Viroli) 2순위] ES 미등록 (**3회째 출제 + 2025-B→2026-B 2연속**)
- 일시: 2026-04-21
- 위치: `projects/ethics-study/exam-solutions/coverage/2026-B.md` Q7 row
- 심각도: blocker (ES 커버리지 누락 — 제시문 중심 사상가 후보군 모두 미등록, **신로마 공화주의(Neo-Roman republicanism)** 대표 사상가 ES 전면 공백, **pettit 기준 row 3회 출제 (2023-A · 2025-B · 2026-B) + 2025-B→2026-B 2연속 재출제 — BLK-175E-2025B-004 누적 별도 독립 블로커**)
- 사유: Q7 (L125-L139) 제시문 "**자유주의는 간섭으로부터 개인을 지키는 데는 성공했지만 '주인(master)으로서의 삶(life as one's own master)'이라는 자유의 본래 의미를 간과** … **힘센 자와 약한 자의 관계 … 예속(subjection/servitude) … 약자가 강자의 눈치를 보며 눈을 내리깔고(lowered eyes) 살아야 하는 상태 vs 자유인이 눈을 크게 뜨고(looking in the eye / eyeball test) 자기 주권을 주장하는 상태**" + "**입헌주의(constitutionalism) … ( ㉠ )의 원리 … 사법권·입법권·행정권 집중 회피**" + "**자연권(自然權) 이론 … 권리 … ( ㉢ )이라고도**"로 제시문 중심 사상가가 **필립 페팃(Philip Pettit, 1945-, 아일랜드 출신 미국 프린스턴대·오스트레일리아 국립대(ANU) 철학자, 『Republicanism: A Theory of Freedom and Government, 1997』·『A Theory of Freedom: From the Psychology to the Politics of Agency, 2001』·『On the People's Terms: A Republican Theory and Model of Democracy, 2012』 저자, **비지배로서의 자유(freedom as non-domination) — 개념 정립자**, 신로마 공화주의(Neo-Roman republicanism) 대표 정치철학자)**임이 **trademark 4중으로 확증**됨 (1순위). **마우리치오 비롤리(Maurizio Viroli, 1952-, 이탈리아 프린스턴대·피사 고등사범학교 정치철학자)**는 공화주의적 애국심론 대표자로 경합 후보(2순위). Trademark 4중 일치: ① **"주인으로서의 삶(life as one's own master)"** = 페팃 『Republicanism, 1997』 제1장·제2장의 자유 정식. 자유 = 자기 삶의 주인됨, 타인의 자의적 지배(arbitrary domination) 부재; ② **"힘센 자와 약한 자 … 눈을 내리깔고 / 눈을 크게 뜨고"** = 페팃 『Republicanism, 1997』 4장·5장의 **eyeball test(눈 마주치기 시험)** trademark. 자유인은 권력자의 눈을 똑바로 마주볼 수 있어야 함 — 비지배 자유의 인식론적·사회심리적 지표. 자의적 권력자 앞에서 눈을 내리깔아야 하는 자는 간섭의 실제 부재와 무관하게 이미 예속 상태. 이 'eyeball test' 비유는 페팃에게 배타적으로 귀속되는 trademark; ③ **"입헌주의 … ( ㉠ )의 원리 … 사법권·입법권·행정권 집중 회피"** = 페팃 『Republicanism, 1997』 제6장·제7장 **견제와 균형(checks and balances) + 권력분립(separation of powers)** 정식. 자의적 권력의 방지를 위한 제도적 장치. ㉠ = **권력분립(權力分立 — separation of powers)**; ④ **"자연권(自然權) … ( ㉢ )이라고도"** = 자연권 = **천부인권(天賦人權 — natural rights)** 정식 대응어. 근대 자유주의 자연권 이론이 공화주의 전통과 결합되는 맥락 — 페팃은 자연권을 개인주의적 자연권이 아닌 **공화주의적 권리(republican rights) / 비지배 권리(rights of non-domination)**로 재해석. 비롤리 배제 근거: 비롤리의 주된 기여는 공화주의적 애국심(republican patriotism) 개념 — 본 문항의 "주인으로서의 삶 / eyeball test / 권력분립 / 비지배" trademark 조합은 페팃 『Republicanism, 1997』의 배타적 정식. 비롤리는 2순위로 보존.
- 후속 조치: TASK-176 범위에서 `pettit` 신규 등록 **우선 격상** + `viroli` 보조 등록 (BLK-175E-2025B-004 누적 + BLK-175E-2026B-005 독립 블로커) — 3회 누적 + 2연속 재출제로 정치철학 공화주의 영역 ES 커버리지 공백 심각도 격상. 등록 시 trademark 키워드: **신로마 공화주의(Neo-Roman republicanism) — Skinner·Pettit·Viroli 주도** · **비지배로서의 자유(freedom as non-domination)** · **자유 3개념 — 소극적 자유(벌린)·적극적 자유(벌린)·비지배 자유(페팃)** · **자의적 권력(arbitrary power) — 법의 통제 밖의 자의적 의지** · **eyeball test(눈 마주치기 시험) — 비지배의 사회심리적 지표** · **주인으로서의 삶(life as one's own master)** · **자치적 공화국(self-governing republic)** · **시민적 덕성(civic virtue)** · **법의 지배(rule of law)** · **견제와 균형(checks and balances)** · **권력분립(separation of powers)** · **공화주의적 애국심(republican patriotism) — 비롤리 대표 개념** · **페팃 저서: 『Republicanism, 1997』·『A Theory of Freedom, 2001』·『On the People's Terms, 2012』** · **비롤리 저서: 『For Love of Country, 1995』·『Republicanism, 1999』·『Machiavelli, 1998』** · **캠브리지 학파(Skinner·Pocock) 공화주의 부흥** · **벌린 2자유 개념 비판 — 비지배 자유는 간섭의 실제 부재가 아니라 자의적 간섭 가능성 자체의 부재**. 후보 id: `pettit` (최우선) + `viroli` (보조).
- 영향: Q7 정답 ㉠ = **권력분립** + ㉢ = **천부인권** + 자유주의/공화주의 자유 개념 대비 서술은 trademark 4중 일치로 확정됨. coverage/2026-B.md Q7 본문은 정확하며 ES 커버리지 공백만 존재. BLK-175E-2025B-004 누적 갱신과 함께 본 BLK-175E-2026B-005는 독립 2026-B 블로커로 등록 — TASK-176에서 `pettit`·`viroli` 일괄 등록으로 병합 해소. **정치철학 공화주의 영역 ES 커버리지 공백 — `pettit`·`viroli` 등록으로 자유주의(밀·롤즈·노직 HIT)·공동체주의(매킨타이어·샌델·왈저 HIT)·공화주의(페팃·비롤리) 3대 축 완성**.


