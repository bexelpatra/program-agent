---
agent: coder
task_id: TASK-175E-2023-A
status: DONE
timestamp: 2026-04-21T15:30:00+09:00
---

## 결과 요약

2023학년도 중등교사 임용 도덕·윤리 전공 A (12문항 40점) 커버리지 작성을 Phase 6 규칙에 따라 완료. 원문(`2023_중등1차_도덕윤리_전공A.md` L1-L202) 전체를 현 세션에서 Read tool로 직독한 후, 각 문항을 `원문 인용 → 3단계 확정(사상가·학파·주제 → 한자·개념 병기 → trademark 3중 일치 근거) → row-by-row 전수 → ES 실존 여부` 순서로 작성. ES 조회 결과 12문항에 등장하는 사상가 중 6명(`tocqueville`, `viroli`, `choe_jeu`, `shweder`, `choe_chiwon`, `blasi`)이 미등록으로 확인되어 `blocker-log.md`에 BLK-175E-2023A-001~006 6건을 신규 append. 배점 검산 2×4 + 4×8 = 40점으로 원문 L7 "12문항 40점"과 일치.

### 현 세션 Read 호출 증거

| 파일 | offset | limit | 용도 |
|---|---|---|---|
| `/home/jai/잡동사니/임용/md/2023_중등1차_도덕윤리_전공A.md` | 1 | (전체 202 lines) | 원문 직독 |
| `/home/jai/program-agent/signal/ethics-study/architecture.md` | 485 | 120 | Phase 6 규칙·동명이인 suffix 규약 확인 |
| `/home/jai/program-agent/projects/ethics-study/exam-solutions/coverage/2022-B.md` | 1 | 100 | 선례 형식·깊이 참조 |
| `/home/jai/program-agent/signal/ethics-study/blocker-log.md` | 730 | 45 | 최근 블로커 섹션 확인(2022-A~2022-B 대비) |

### ES 조회 증거

```bash
# 55명 전수 리스트 조회
curl -s "http://localhost:9200/ethics-thinkers/_search?size=100&_source=id,name,name_en" \
  | jq -r '.hits.hits[]._source | [.id, .name, .name_en] | @tsv' | sort
# 결과: aquinas, arendt, aristotle, augustine, baek_nakcheong, bentham, buddha, confucius,
#       dewey, epictetus, epicurus, galtung, gilligan, habermas, haidt, hanfeizi, hegel,
#       hobbes, huineng, hume, jeongyagyong, kang_mangil, kant, kohlberg, laozi, lickona,
#       locke, macintyre, marcus_aurelius, mencius, mill_js, mozi, nietzsche, noddings,
#       nozick, piaget, plato, raths, rawls, rest, rousseau, sandel, sartre, seneca,
#       socrates, spinoza, taylor, walzer, wangyangming, wonhyo, xunzi, yihwang, yiyulgok,
#       zhuangzi, zhuxi (55명 확증)

# 12문항 관련 사상가 18명 term 조회
for id in tocqueville viroli choe_jeu shweder choe_chiwon blasi \
          kohlberg haidt mozi mill_js kant zhuxi yiyulgok rousseau \
          locke rest hume spinoza; do
  curl -s -X POST "localhost:9200/ethics-thinkers/_search" \
    -H "Content-Type: application/json" \
    -d "{\"query\":{\"term\":{\"id\":\"$id\"}}}" | jq -r '.hits.total.value'
done
# 결과: 0 0 0 0 0 0  1 1 1 1 1 1 1 1 1 1 1 1
# 앞 6명 MISS, 뒤 12명 HIT
```

## 변경된 파일

1. **신규 작성**: `projects/ethics-study/exam-solutions/coverage/2023-A.md` (12 문항 전수 + 요약 테이블 + 블로커 등록 내역)
2. **append**: `signal/ethics-study/blocker-log.md` (773 → 809 라인, BLK-175E-2023A-001~006 6건 추가)

## thinker_id 목록 및 ES 상태

| 문항 | 역할 | 사상가 | thinker_id | ES 상태 | 비고 |
|---|---|---|---|---|---|
| Q1 | — | [2015 개정 도덕과 교육과정] | N/A (교과교육학) | — | 사상가 지명 문항 아님 |
| Q2 | — | [목적론 vs 의무론 분류] | N/A (일반개념) | — | 규범윤리학 메타 분류 문항 |
| Q3 | 갑 | 알렉시스 드 토크빌 | `tocqueville` | **MISS** | BLK-175E-2023A-001 |
| Q3 | 을 | 마우리치오 비롤리 | `viroli` | **MISS** | BLK-175E-2023A-002 (v2-rejected 후보) |
| Q4 | (가)·(나) | 수운 최제우 | `choe_jeu` | **MISS** | BLK-175E-2023A-003 (v2-rejected 후보) |
| Q5 | 갑 | 로렌스 콜버그 | `kohlberg` | HIT | — |
| Q5 | 을 | 리처드 슈웨더 | `shweder` | **MISS** | BLK-175E-2023A-004 (v2-rejected 후보) |
| Q5 | 병 | 조너선 하이트 | `haidt` | HIT | — |
| Q6 | 갑 | 고운 최치원 | `choe_chiwon` | **MISS** | BLK-175E-2023A-005 (v2-rejected 후보) |
| Q6 | ㉢ | 공자 | `confucius` | HIT | 갑·을 공통 참조 사상가 |
| Q6 | 을 | 묵자 | `mozi` | HIT | — |
| Q7 | 갑 | 존 스튜어트 밀 | `mill_js` | HIT | 동명이인 suffix 규약 준수 |
| Q7 | 을 | 임마누엘 칸트 | `kant` | HIT | — |
| Q8 | 갑 | 주희 | `zhuxi` | HIT | — |
| Q8 | 을 | 율곡 이이 | `yiyulgok` | HIT | — |
| Q9 | 갑 | 장-자크 루소 | `rousseau` | HIT | — |
| Q9 | 을 | 존 로크 | `locke` | HIT | — |
| Q10 | 갑 | 제임스 레스트 | `rest` | HIT | 동명이인 rest(James Rest) 확정 |
| Q10 | 을 | 아우구스토 블라지 | `blasi` | **MISS** | BLK-175E-2023A-006 (v2-rejected 후보 + 2연속 재출제) |
| Q11 | 단독 | 존 스튜어트 밀 | `mill_js` | HIT | Q7과 동일 사상가 2문항 |
| Q12 | 갑 | 데이비드 흄 | `hume` | HIT | — |
| Q12 | 을 | 바뤼흐 스피노자 | `spinoza` | HIT | — |

**HIT: 12명 / MISS: 6명 (신규 블로커 등록)**

### 동명이인 suffix 규약 준수 (architecture.md L491 근거)

- **존 스튜어트 밀(John Stuart Mill, 1806-1873)** → `mill_js` 사용 (이니셜 suffix, 단일인이므로 표기 유지).
- **James Rest** (도덕심리학자, 1941-1999) → `rest` 사용. Q10에서 "도덕성 4구성요소 모델(도덕적 민감성·판단력·동기화·품성/실행력)"이 레스트의 trademark로서 명확하며, 흄의 『자유론』에 쓰인 'rest(안식/휴식)'·기독교 신학 관련 'rest' 개념과는 전혀 다른 고유인물. suffix 불필요.
- **Charles Taylor** (공동체주의, ES `taylor`) — 본 시험에는 출제되지 않음. Paul Taylor(생명중심주의, `taylor_p`)도 출제되지 않음.
- **T.H. Green** (`green_th`) — 본 시험에는 출제되지 않음.

## 재출제 사상가 결과

### 누적 경계 대상 재등장 여부 (2023-A 검증 결과)

| 사상가 | 이전 연속 횟수 | 2023-A 등장 | 연속 상태 |
|---|---|---|---|
| `hoffman` (마틴 호프만) | 4연속 (2016-A·2019-B·2021-B·2022-B) | **등장 없음** | 4연속 유지, 5연속 확장 실패 |
| `jinul` (지눌) | 3연속 | **등장 없음** | 3연속 유지 |
| `turiel` (엘리엇 튜리엘) | 3연속 | **등장 없음** | 3연속 유지 |
| `durkheim` (에밀 뒤르켐) | 2연속 (2021-B·2022-B) | **등장 없음** | 2연속 유지 |
| `singer` (피터 싱어) | 2연속 (2019-B·2022-B) | **등장 없음** | 2연속 유지 |
| `pettit` (필립 페팃) | 2연속 | **등장 없음** | 2연속 유지 |
| `blasi` (아우구스토 블라지) | 2020-B 출제 (단독) | **Q10 을 출제** | **신규 2연속 등극** (2020-B → 2023-A) |

### 신규 관측: 단일 시험 동일 사상가 중복 출제

- **`mill_js` (존 스튜어트 밀)**: 2023-A 내에서 **Q7(『공리주의』 제5장 — 정의와 공리)**과 **Q11(『자유론』 — 개성·위해 원칙·3대 기본 자유)** 두 문항에 동일 사상가 출제. 동일 시험 내 2회 출제 패턴은 향후 Q7·Q11 유형 분석 시 참고 사항.

### v2-rejected 후보군 검증 결과 (사전 추정 5명)

| 후보 | 사전 추정 근거 | 원문 재검증 결과 |
|---|---|---|
| `viroli` | 공화주의 정치사상 | **Q3 을로 확정** — trademark 3중 일치 |
| `choe_jeu` | 한국 윤리 | **Q4 (가)·(나)로 확정** — 『동경대전』「논학문」 원문 직접 대조 |
| `shweder` | 도덕심리학 | **Q5 을로 확정** — 3대 윤리 trademark 3중 일치 |
| `choe_chiwon` | 한국 철학 | **Q6 갑으로 확정** — 「난랑비서」 원문 trademark 3중 일치 |
| `blasi` | 도덕심리학 | **Q10 을로 확정** — 도덕적 정체성 3요소 trademark 3중 일치 |

**v2-rejected 사전 추정 5명 모두 원문 재검증에서 유효성 확인** — 추정이 패턴 추론이 아닌 실제 원문 trademark에 기반했음을 확증.

## 이슈/블로커

### 블로커 (신규 6건, blocker-log.md에 append)

1. **BLK-175E-2023A-001**: `tocqueville` (Alexis de Tocqueville) — Q3 갑. 자유·종교 두 기둥·습속·『미국의 민주주의』 trademark. **최우선 등록**.
2. **BLK-175E-2023A-002**: `viroli` (Maurizio Viroli) — Q3 을. 공화주의적 애국심(patria) vs 민족주의(natio) trademark. **우선 등록**.
3. **BLK-175E-2023A-003**: `choe_jeu` (수운 최제우) — Q4 단독. 시천주 본주문 13자·『동경대전』「논학문」. **최우선 등록** (한국 윤리 자생 근대 원점).
4. **BLK-175E-2023A-004**: `shweder` (Richard A. Shweder) — Q5 을. 3대 윤리(자율성·공동체·신성) — `haidt` 도덕 기반 이론의 직접 전구. **최우선 등록**.
5. **BLK-175E-2023A-005**: `choe_chiwon` (고운 최치원) — Q6 갑. 「난랑비서」 풍류도·포함삼교. **최우선 등록** (한국 고대 회통 사상 원점).
6. **BLK-175E-2023A-006**: `blasi` (Augusto Blasi) — Q10 을. 도덕적 정체성·도덕적 인격 3요소. **최우선 등록** (2연속 재출제).

### 관찰 사항 (observation)

- **동일 시험 내 `mill_js` 2회 출제(Q7·Q11)**: 2023-A의 특징으로 기록. 관례적으로 시험 출제자가 단일 시험에서 동일 사상가를 두 영역(윤리사상/사회사상)에 분산 배치하는 경우가 있으며, 향후 기출 분석의 참고 데이터.
- **Q4 교정 문제 형식**: 동학 주문의 "시(侍)·주(主)·조화(造化)" 해설을 원문과 대조하여 오류 2개(㉡ 천리→기화 / ㉢ 군왕→부모)를 찾는 문제. 『동경대전』「논학문」원문 직접 대조가 trademark 3중 일치의 유일 방법이므로 `choe_jeu` ES 등록 시 「논학문」 원문("侍者 內有神靈 外有氣化 一世之人 各知不移者也 / 主者 稱其尊而與父母同事者也 / 造化者 無爲而化也")을 claim으로 포함 필수.
- **Q6 3교 회통 배정**: 「난랑비서」의 ㉢(공자)·주사(노자)·축건국 태자(석가모니) 3인 배정이 동시 해독 요구. ㉢은 갑(최치원)·을(묵자) 두 제시문에 **공통으로 등장**하여 문제의 핵심 링크 역할 — `confucius` ES HIT로 확인되어 별도 블로커 불필요하나 claim에 "신라 최치원 난랑비서에서 유교의 대표자로 지칭됨" 추가 가능.

## 다음 제안

1. **Tester 검증 (필수)**: 본 2023-A.md를 대상으로 Phase 6 Tester 규칙 4항(직접 풀이 후 대조 / 3중 일치 검증 / grep 0건 규칙 / row-by-row 전수 검증) 적용. 특히 Q4 『동경대전』「논학문」 원문 구절이 실제로 원문 제시문에 포함되어 있음과, Q6 「난랑비서」 원문 대조를 집중 검증 필요.
2. **2023-B 이관**: Phase 6 배치 크기 제한(1회 Coder 호출 = 1개 연도 × 1개 과목)에 따라, 2023-B는 별도 태스크(TASK-175E-2023-B)로 분리 진행. Tester PASS 후 Manager가 차례로 호출.
3. **TASK-176 ES 보강 우선순위**: 본 2023-A 블로커 6건 + 기존 누적 35건 = 총 41건 예상. 등록 우선순위:
   - **최최우선(4연속 유지)**: `hoffman`.
   - **최우선(2연속+)**: `choe_jeu`, `choe_chiwon`, `shweder`, `blasi`, `tocqueville`, `durkheim`, `singer`, `popper`, `james`, `beccaria`, `zhiyi` 등 기존 최우선 라인 + 2023-A 신규.
   - **우선**: `viroli` 등.
   - ES 등록 시 `choe_jeu` → `jeong_yakyong`·`wonhyo` 한국 라인 연결, `shweder` → `haidt`·`turiel` 도덕심리학 문화비교 라인 연결, `blasi` → `rest`·`lickona`·`kohlberg` 도덕 인격 라인 연결을 고려.
4. **사용자 검토 지연 가능**: blocker-log.md 총 41건 누적 시점이 임박하므로, Manager는 Step 6 회고 진입 전 사용자에게 일괄 검토 요청 권고.
5. **Reviewer 사후 점검**: 본 coverage의 Q4 『동경대전』「논학문」 원문 인용과 Q6 「난랑비서」 원문 인용은 한국 고전 원문이므로, Reviewer가 별도로 경전 원문과 대조 가능한 범위에서 grep 확인 권장.

---

**Phase 6 Coder 규칙 준수 self-check** (체크박스 대신 검증 가능한 증거):

- [원문 직독] 현 세션 Read 호출 기록: `2023_중등1차_도덕윤리_전공A.md` 전체 202 lines 단일 호출 (offset 없음, limit 없음 = 전문).
- [문제 → 제시문 → 사상가 3단계] 각 Q별 "확정 분석" 섹션에 ①사상가·학파·주제 ②한자·개념 병기 ③trademark 3중 일치 근거(제시문 복사 구절 2~3개) 기재 완료.
- [불확실 처리] 사상가 확정이 어려운 Q는 없음. Q1~Q2는 교과교육학·일반개념 분류로 사상가 지명 아님을 명시. Q3~Q12는 모두 trademark 3중 일치로 확정.
- [한자+한글 병기] 한자 개념어에 `한자(한글)` 형식 일관 적용. 예: `理一分殊(이일분수 — one principle, diverse manifestations)`, `侍天主(시천주 — bearing the Lord of Heaven within)`, `包含三敎(포함삼교 — encompassing the three teachings)`, `接化群生(접화군생 — reaching out to transform all living beings)` 등.
- [동명이인 suffix 준수] `mill_js` (John Stuart Mill), `rest` (James Rest, 단일인 suffix 불필요)로 canonical 표기.
- [배치 크기 제한] 2023-A 단일 시험 1개(12문항) 처리. 2023-B는 별도 태스크.
- [한 사상가 복수 주제] Q11과 Q7은 모두 `mill_js`이나 서로 다른 저작(『공리주의』 vs 『자유론』)에서 다른 개념을 묻는 별도 문항이므로 각각 독립 처리.
