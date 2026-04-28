---
task_id: TASK-176-07
verdict: PASS
reviewer: reviewer-agent
reviewed_at: 2026-04-22T04:25
target: Manager-authored task-board.md rows TASK-176-07 + TASK-176-07-T (singer ES 등록 + 검증)
---

# Reviewer Report — TASK-176-07 (singer ES 등록)

## 최종 판정: **PASS**

Manager가 task-board.md에 등록한 TASK-176-07 / TASK-176-07-T 스펙은 14개 검증 항목에서 모두 현실 일치. Coder가 외부 질의 없이 실행 가능한 수준으로 명세가 완결되어 있음. 몇 건의 Manager 주장에는 해석상 해소 가능한 ambiguity가 남아있어 observation으로 기록하되, 판정에 영향 없음.

---

## 검증 근거 (항목별)

### 1. 출제횟수 재집계 (PASS)
- `exam-coverage-map.md` L35 singer row 실측: `4 | 2015-B, 2019-B, 2022-B, 2024-B | BLK-175E-2019B-001, BLK-175E-2022B-005, BLK-175E-2024B-005, BLK-175E-2024B-006`
- Manager 주장과 완전 일치. 2019-B→2022-B 2연속 + 2024-B 4회째 재출제 정확.

### 2. coverage grep 12파일 67건 합산 (PASS)
파일별 `grep -cE "singer|싱어|Peter Singer"` 실측:
```
2015-B.md: 11   2018-A.md: 3   2019-B.md: 9
2020-B.md: 2   2021-A.md: 3   2021-B.md: 1
2022-B.md: 20  2023-A.md: 1   2023-B.md: 1
2024-A.md: 1   2024-B.md: 13  2025-A.md: 2
```
합계 = 11+3+9+2+3+1+20+1+1+1+13+2 = **67**. Manager 주장과 파일별·합계 전건 일치. 12파일 맞음.

### 3. 2024-B.md L354 verbatim (PASS)
실측: "갑 = **피터 싱어(Peter Singer, 1946~, 호주 프린스턴대 공리주의·응용윤리학자)** — 『동물 해방(Animal Liberation, 1975)』 trademark: **이익 평등 고려의 원칙(principle of equal consideration of interests)** + **종차별주의(speciesism)** 비판 + 벤담의 "고통을 느낄 수 있는 능력" 기준 계승"
- "1946~, 호주 프린스턴대 공리주의·응용윤리학자" 실존 ✓

### 4. 2022-B.md L410 verbatim (PASS)
실측: "**갑 = 피터 싱어(Peter Singer, 1946~) — 오스트레일리아·프린스턴대 실천윤리·공리주의. 『실천윤리학(Practical Ethics, 1979)』 제8장 "부자와 가난한 자"·『기아, 풍요, 도덕(Famine, Affluence, and Morality, 1972)』**. … "익사하는 아이"(drowning child) 사고 실험."
- "오스트레일리아·프린스턴대 실천윤리·공리주의" ✓
- "『실천윤리학(Practical Ethics, 1979)』" ✓
- "『기아, 풍요, 도덕(Famine, Affluence, and Morality, 1972)』" ✓
- "익사하는 아이(drowning child)" ✓

### 5. 2019-B.md L47 verbatim (PASS)
Q3 row 본문(L17)에서 "이익평등고려 원칙"·"쾌고감수능력"·"종차별주의"·"Animal Liberation, 1975" 모두 확증. L47은 원문 인용부로, `2019-B.md`의 원문(L47 근거 셀)에서 "종차별주의"·"이익평등고려 원칙" 인용 확인.

### 6. 2015-B.md L17 verbatim (PASS)
실측: "**갑 = 피터 싱어(Peter Singer)** — 『동물 해방(Animal Liberation, 1975)』. Trademark: … "문제는 … 고통을 느낄 수 있는가이다""
- "갑 = 피터 싱어" ✓
- "동물 해방" ✓
- "고통을 느낄 수 있는가" ✓

### 7. 영어 trademark 역grep 확증
`cd coverage/ && grep -r "..." . | wc -l` 실측:
| 키워드 | files | hits | Manager 주장 | 판정 |
|---|---|---|---|---|
| `Peter Singer` | 4 | 16 | ≥1 | PASS |
| `Animal Liberation` | 3 | 5 | ≥1 | PASS |
| `Practical Ethics` | 2 | 2 | ≥1 | PASS |
| `Famine, Affluence, and Morality` | 1 | 2 | ≥1 | PASS |
| `speciesism` | 5 | 7 | ≥1 | PASS |
| `sentience` | 3 | 3 | "≥1 hit (Manager 주장 7 hits 4 files)" | PASS-with-note |
| `drowning child` | 1 | 2 (2022-B only) | 2 hits 2022-B | PASS |
| `preference utilitarianism` | 1 | 1 (2019-B only) | "3 hits 2019-B" | PASS-with-note |
| `principle of equal consideration of interests` | 3 | 5 | ≥1 | PASS |

**Note sentience**: 순수 영어 `sentience` 단독 grep = 3 hits 3 files. Manager "7 hits 4 files" 주장은 한글 "쾌고감수능력/쾌고 감수 능력"까지 통합한 개념 빈도로 해석하면 7 hits 4 files(2019-B:3, 2015-B:1, 2024-B:2, 2021-A:1) 정확. 검증 항목은 "`sentience` ≥1 hit" 이므로 PASS. Task description에 "영어 병기는 coverage grep hit된 것만" 규정이 포함되어 있으므로 Coder 판단에 충분.

**Note preference utilitarianism**: 순수 영어 단독 grep = 1 hit 2019-B. Manager "3 hits 2019-B" 주장은 한글 "선호 공리주의" + 영어까지 합쳐서 grep하면 2019-B.md 내 3 hits 실측. 해석 범위 차이로, 검증 항목은 "≥1 hit" 이므로 PASS.

### 7b. 0-hit 부정 리스트 확증 (PASS)
| 키워드 | 실측 hits | Manager 주장 | 판정 |
|---|---|---|---|
| `The Life You Can Save` | 0 | 0 | PASS |
| `효율적 이타주의` | 0 | 0 | PASS |
| `Princeton University` | 0 | 0 | PASS |
| `효과적 이타주의` | 1 (2019-B) | 1 | PASS (observation: 제한 사용 권고 포함) |

Manager 부정 리스트(Task description 말미)는 pettit TASK-176-06 Tester bug 3건 교훈을 정확히 반영하여 regex-verifiable 수준으로 명세됨. Coder가 독립 판단 가능.

### 8. ES singer 미등록 재확인 (PASS)
```
curl -s http://localhost:9200/ethics-thinkers/_doc/singer
→ {"_index":"ethics-thinkers","_id":"singer","found":false}
```
Manager 주장 일치.

### 9. ES field=western_ethics 실사용 확인 (PASS)
- `bentham` field=`western_ethics` era=`근대 영국` ✓
- `mill_js` field=`western_ethics` era=`근대 영국` ✓
- ethics-thinkers 내 `field:western_ethics` count=17 (spinoza/seneca/epicurus/epictetus/hegel/marcus_aurelius/hume/aristotle/aquinas/kant/mill_js/bentham/plato/socrates/augustine/sartre/nietzsche) — Manager "17명" 주장 정확 일치.
- singer에 field=`western_ethics` 배정은 bentham·mill_js 선례와 공리주의 계보 일관성상 타당.

### 10. ES ethics-fields 인덱스 western_ethics 누락 (observation)
ethics-fields 인덱스 6개 등재: eastern_ethics / political_philosophy / moral_development / peace_studies / unification_edu / civic_edu
- `western_ethics` 미등재 — Manager가 이미 observation으로 기재 + 기존 bentham/mill_js/kant 등 17명이 동일 상황으로 운영 중인 기존 data-quality issue. 본 태스크 PASS 판정에 영향 없음. (Manager: "data-quality issue, Manager 기록만" — 적절.)

### 11. BLK 실존 확인 (PASS)
- **BLK-175E-2019B-001**: `blocker-log.md:510` "Q3 피터 싱어(Peter Singer) ES 미등록" ✓
- **BLK-175E-2022B-005**: `blocker-log.md:769` + `2022-B.md:581` "피터 싱어 … 2연속 재출제 최우선" ✓ Manager 주장 L581 정확.
- **BLK-175E-2024B-005**: `blocker-log.md:938` + `2024-B.md:541/588` "(갑) 피터 싱어 ES 미등록 (4회째 출제)" ✓ L541/L588 정확.
- **BLK-175E-2024B-006**: `blocker-log.md:946` + `2024-B.md:384/554/589` "Q8 (을) 톰 리건(Tom Regan) ES 미등록 (2회째 출제)" ✓ — regan 전용, singer 등록과 독립. Manager "미해소 1건 = regan 전용" 주장 정확.

### 12. 선행 태스크 DONE (PASS)
task-board.md 실측:
- TASK-176-06: status=DONE ✓
- TASK-176-06-T: status=DONE ✓
- TASK-176-06-FIX: status=DONE ✓ (Manager inline FIX: Pettit 후기 저서 3건 + 영어 병기 3건 제거)

### 13. 의존성·순서 (PASS)
TASK-176-07의 Depends On = TASK-176-06-FIX. 현재 task-board.md 순서도 06-FIX 이후 07이 배치. 충돌 없음.

### 14. 태스크 완결성 (PASS)
- 사상가 메타: id/name/name_en/field/era/birth/death 완비 ✓
- 핵심 저서 3종 각각 coverage 출처 인용 (파일·라인 번호 포함) ✓
- 핵심 주장 7개 각각 verbatim source 지시 (2019-B L47, 2022-B L139/L410/L417, 2024-B L348/L354/L365, 2015-B L17) ✓
- claims ≥6·works ≥2·keywords ≥6 하한선 명시 (Tester row) ✓
- **★ 원문 인용 규정 재강조**: pettit Tester bug 3건 교훈을 반영해 "영어 병기는 coverage grep hit된 것만" 조항 + 0-hit 부정 리스트(`The Life You Can Save`·`효율적 이타주의` vs `효과적 이타주의`·`Princeton University` 단독) 구체 명시 — 재발 방지 효과 기대 가능.
- Tester 체크 9개 항목 각각 측정 가능 (found·카운트 하한·verbatim grep·trademark 역grep·BLK 해소).

---

## Observations (판정 무영향)

1. **O-1 sentience hit 수치 ambiguity**: Manager가 영어 `sentience` 단독과 한글 "쾌고감수능력"을 합쳐 "7 hits 4 files"로 제시. 검증에는 문제 없으나, 향후 명세 시 "영·한 합산 N hits" 형식으로 명시하면 해석 노이즈 감소.
2. **O-2 preference utilitarianism hit 수치 ambiguity**: 동일 사유. 영어 단독 1 hit / 영·한 합산 3 hits. Coder에게는 "3 hits 2019-B" 언급만으로 충분한 수준.
3. **O-3 ethics-fields 인덱스 western_ethics 누락**: 기존 data-quality issue 지속. 17명 western_ethics thinker 전수가 이 상태로 운영 중이므로 singer도 동일 처리 자연스러움. Manager observation 처리 적절.

---

## 결론

TASK-176-07 / TASK-176-07-T 스펙은 실측 기반으로 완결되어 있고, pettit Tester bug 3건 교훈이 "영어 병기 coverage grep 역확증" 조항으로 명시되어 재발 방지 장치까지 갖춤. **Coder 호출 진행 가능**.

**판정: PASS**
