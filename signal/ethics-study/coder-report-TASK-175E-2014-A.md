---
agent: coder
task_id: TASK-175E-2014-A
status: DONE
timestamp: 2026-04-20T00:00:00
---

## 결과 요약

2014학년도 중등 임용 도덕·윤리 전공 A(기입형 1~15 + 서술형 1~5, 총 20문항/50점)의 커버리지 표를 architecture.md "Phase 6 기출 작업 규칙"(L523~L581)에 따라 신규 작성하였다.

- 원문(`~/잡동사니/임용/md/2014중등1차-2교시-도덕윤리-전공A-문제지-최종.md`, 263 lines)을 본 세션에서 Read tool로 직접 전수 호출(offset=1, limit 미지정 전체)하여 직독.
- 각 문항 row는 ① 발문 독해 → ② 제시문 독해(고유 trademark 추출) → ③ 사상가/분류 판정의 3단계 절차로 작성하였으며, 각 row 메모 컬럼에 원문 2~3구절을 그대로 복사 인용하고 `원문 line` 컬럼에 file_path:line_range를 병기.
- 모든 인용 구절을 `grep -F`로 자가 검증하여 1건 이상 매칭됨을 확인. (초기 작성 시 `<u>...</u>` 태그·표 셀 접두어 형식으로 인해 0건이 나온 인용 3건을 원문 그대로 형태로 정정함.)
- thinker_id는 ES `ethics-thinkers` 인덱스에서 canonical 55건을 본 세션 curl 1회 + claim 검증 curl 11회로 조회하여 매핑.
- ES에 사상가 자체가 없는 6건(CDP/Bandura/Nāgārjuna/Burke/Machiavelli/Turiel)은 "없음(누락)"으로 표기. 단, 본 태스크 범위에서 신규 사상가 ES 추가는 수행하지 않음(별도 태스크에서 처리).
- "사상가 불명(확인 필요)" row 없음 → blocker-log에 신규 BLK 등록 사항 없음.

## 변경된 파일

- `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2014-A.md` (신규)

## Read 호출 감사 로그 (현 세션 한정)

| # | 파일 경로 | offset | limit | 목적 |
|---|-----------|--------|-------|------|
| 1 | `/home/jai/program-agent/agents/coder.md` | 1 | (전체) | Coder 역할/작업 규칙/금지 사항 재확인 |
| 2 | `/home/jai/program-agent/signal/ethics-study/architecture.md` | 510 | 90 | Phase 6 기출 작업 규칙(L523~L581) 확인 |
| 3 | `/home/jai/잡동사니/임용/md/2014중등1차-2교시-도덕윤리-전공A-문제지-최종.md` | 1 | (전체 263 lines) | 2014-A 원문 직독 (전수) |
| 4 | `/home/jai/program-agent/signal/ethics-study/blocker-log.md` | 1 | 40 | 블로커 형식·기존 항목 확인 |

추가로 자가 grep 검증을 위해 Bash tool로 `sed -n '141,148p'`, `sed -n '165,169p'`, `sed -n '255,261p'`로 원문 일부를 부분 재확인.

## ES canonical thinker_id 조회 결과

조회 명령:
- `curl -s "http://localhost:9200/ethics-thinkers/_search?size=100&_source=id,name,name_en"` (전체 사상가 55건)
- `curl -s -X POST "http://localhost:9200/ethics-claims/_search" -H 'Content-Type: application/json' -d '{...}'` (claim 본문 매칭 검증, thinker_id별 11회: wonhyo, zhuangzi, spinoza, rousseau, dewey, aristotle, yihwang, aquinas, raths, zhuxi, wangyangming, confucius)

ES 등록 사상가 55명 (id 알파벳 순):
`aquinas, arendt, aristotle, augustine, baek_nakcheong, bentham, buddha, confucius, dewey, epictetus, epicurus, galtung, gilligan, habermas, haidt, hanfeizi, hegel, hobbes, huineng, hume, jeongyagyong, kang_mangil, kant, kohlberg, laozi, lickona, locke, macintyre, marcus_aurelius, mencius, mill_js, mozi, nietzsche, noddings, nozick, piaget, plato, raths, rawls, rest, rousseau, sandel, sartre, seneca, socrates, spinoza, taylor, walzer, wangyangming, wonhyo, xunzi, yihwang, yiyulgok, zhuangzi, zhuxi`

본 시험에 등장하나 ES 누락된 사상가 6명:
- Child Development Project 팀 (Solomon, Watson, Battistich) — 인격교육 분파, lickona는 있으나 동일 인물 아님
- Albert Bandura (반두라) — 사회인지이론·도덕적 이탈
- Nāgārjuna (나가르주나/용수) — 중관·중도·팔불중도
- Edmund Burke (에드먼드 버크) — 보수주의
- Niccolò Machiavelli (마키아벨리) — 군주론·논고
- Elliot Turiel (튜리엘) — 사회적 영역 이론

본 시험 등장 사상가의 ES claim 일치 확인 결과(매핑 가능):
- wonhyo: "화쟁(和諍)·일심(一心)·회통(會通)" claim 명시 (기입형 7 trademark 일치)
- zhuangzi: 지인·신인·성인·소요유 claim 존재 (기입형 6 "신인불재" 일치, "무용지용" 직접 claim은 보강 권장)
- aquinas: "자연법·영원법·인정법·신법" claim 존재 (기입형 8 일치)
- dewey: "성장으로서의 교육·경험의 재구성·도덕적 탐구" claim 존재 (기입형 9 일치)
- spinoza: "신=자연·코나투스·자유와 필연성" claim 존재 (기입형 10 일치, "영원의 상" 직접 claim은 보강 권장)
- rousseau: "소극적 교육·시민종교·자기애·일반의지·대의제 비판" claim 존재 (기입형 15 일치, "불평등 기원론 3단계" 직접 claim은 보강 권장)
- zhuxi: "이기·태극(무극이태극)·성즉리·격물치지·거경궁리·이일분수·존천리거인욕" claim 존재 (서술형 2·서술형 4 부분 일치, 신독·대학 성의장은 보강 권장)
- wangyangming: "심즉리·치양지·지행합일·격물=정심·사상마련·만물일체지인·사구교·양지" claim 존재 (서술형 2 일치)
- yihwang: "성학십도·심통성정도·태극도·성학·도설" claim 존재 (서술형 4 일치, 리발설 직접 claim은 보강 권장)
- aristotle: "품성적 덕·에토스·습관·프로네시스·실천적 지혜·소피아·지적 덕" claim 존재 (서술형 5 일치)
- raths: "순위 매기기·가치명료화 전략·콜버그 비판·듀이 영향" claim 존재 (기입형 2 부분 일치, Coombs 가치분석모형 별도 보강 필요)
- confucius: "인=애인·예·덕치" claim 존재 (기입형 4 부분 관련, 『대학』 성의장은 zhuxi 쪽이 직접적)
- habermas: 기입형 11 심의민주주의 부분 관련 (참고)

## 사상가별 분류 카운트

### 사상가형 / 교과교육학 / 경계영역
- 사상가형: **14문항** (기입형 3·5·6·7·8·9·10·13·14·15 + 서술형 1·2·4·5)
- 교과교육학: **3문항** (기입형 1·2·12)
- 경계영역: **3문항** (기입형 4·11 + 서술형 3)
- 합계: 14 + 3 + 3 = **20** ✓

### ES 커버리지 (있음/부족/없음)
- 있음: **6문항** (기입형 7·8·9 + 서술형 2·4·5)
- 부족: **6문항** (기입형 2·4·6·10·11·15)
- 없음(누락): **8문항** (기입형 1·3·5·12·13·14 + 서술형 1·3)
- 합계: 6 + 6 + 8 = **20** ✓

## 블로커 목록 (BLK-XXX 신규 발견분)

본 태스크에서 **신규 BLK 등록 사항 없음**.

근거: 모든 20문항은 제시문의 trademark(고유 개념·인명·저서명·표현)에 의해 사상가가 명확히 식별되었으며, "사상가 불명(확인 필요)" 처리되는 row가 없음. ES 누락 사상가 6명은 "없음(누락)" 표기로 처리하였으며 별도 사상가 추가 태스크에서 다룰 사안이라 BLOCKER가 아님(architecture.md 정책상 ES 신규 사상가 추가는 본 태스크 범위 밖).

## 이슈/불확실

1. **기입형 1의 ㉠ 자체 미상**: (가) 표의 "4가지 우선적 과제" 중 ㉠ 자리는 원문에 비어 있어 외부 지식이 필요. 표준 정답으로 통용되는 것은 "내적 동기/자율성을 키우는 것(developing students' intrinsic motivation / promoting student autonomy)" — CDP의 4기둥 중 하나. 다만 발문은 ㉠ 자체가 아니라 "㉠과 관련하여 ㉡(봉사활동)을 활성화하는 방법"을 묻는 것이므로, 답안 작성에서는 자율성·내적 동기 부여를 통한 봉사활동 활성화 방법을 서술하면 된다.

2. **기입형 11의 빈칸 정답 후보 복수**: 표 구조상 (A)는 자유주의(집합/총합) 민주주의로 (B)는 심의민주주의이며, 빈칸은 (A)의 정당성 근거. 표준 정답은 "다수결" 또는 "선호의 (집합적) 결집/총합"이지만, 정확한 출제자 의도 확인을 위해 사용자 검토 권장(정답 후보를 모두 메모에 기재).

3. **기입형 12 대북정책 시기**: A=김대중(화해협력정책 1998~), D=노무현(평화번영정책 2003~), C=이명박(상생·공영의 대북정책 2008~), B=박근혜(한반도 신뢰프로세스 2013~)로 판정. 출제 당시(2014학년도 임용시험은 2013년 11월 시행) B는 "박근혜 한반도 신뢰프로세스"가 가장 부합. 순서: **A → D → C → B**.

4. **서술형 2 빈칸 정답 후보**: 갑(왕양명)이 묻고 을(주희)이 답하는 맥락에서, 을이 "객관적 궁리의 대상이 되는 영역엔 선지후행, ___ 영역엔 지행병진"이라고 말함. 후보로 "도덕적 본성/심신(心身) 수양/(인간) 본성/(공부의 실천적) 함양 영역" 등이 있으며, 문헌상 명확한 단일 정답어는 출제자 해석에 따라 달라질 수 있음. 메모에는 핵심 의미("주관적·실천적·수양 영역")를 기록.

5. **분류 회색지대**: 기입형 4(『대학』 성의장)은 텍스트 자체가 유교 경전이므로 사상가형(공자/주희)으로도 볼 수 있으나, 임용시험 맥락에서 "어느 사상가의 trademark 사상이라기보다 경전 텍스트와 개념(신독)의 식별"을 묻는 측면이 강해 경계영역으로 분류함. 만약 사상가형으로 재분류하면 분류 카운트가 사상가형 15 / 교과교육학 3 / 경계영역 2로 조정됨.

## 다음 제안

1. **Tester(TASK-175E-2014-A 검증)**: row-by-row 전수 검증을 통해 (a) 인용 구절 grep -F 일치 (b) 사상가-제시문 trademark 일치 (c) ES 매핑 일치 (d) 분류 합리성 점검을 수행 권장.

2. **ES 신규 사상가 추가 태스크 (별도)**: 누락된 6명(CDP팀/Bandura/Nāgārjuna/Burke/Machiavelli/Turiel)은 본 시험뿐 아니라 향후 다른 연도에서도 출제될 가능성이 높으므로 ES `ethics-thinkers`·`ethics-claims`에 신규 등록 태스크를 검토.

3. **ES claim 보강 태스크 (별도)**: "부족" 판정 6문항의 사상가별로 다음 claim 보강 권장:
   - raths: Coombs의 "가치분석모형(value analysis)" claim 또는 별도 사상가 추가
   - zhuangzi: "무용지용(無用之用)·신인불재" claim
   - spinoza: "영원의 상[sub specie aeternitatis]" claim
   - rousseau: "인간 불평등 기원론 3단계 (법·사유재산권 → 위정자 직분 → 전제권력)" claim
   - habermas: "심의민주주의 vs 자유주의 민주주의 비교" claim
   - confucius/zhuxi: "신독(愼獨)·『대학』 성의장" claim
   - yihwang: "리발설(理發說)·리도(理到)" claim

4. **다음 연도 작업 진행**: Tester PASS 후 동일 형식으로 2014-B → 2015-A → 2015-B 순서로 진행 (배치 크기 1연도×1과목 규칙 준수).
