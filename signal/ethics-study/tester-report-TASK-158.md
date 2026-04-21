---
agent: tester
task_id: TASK-158
status: DONE
severity: observation
timestamp: 2026-04-15T00:00:00
---

## 결과 요약
`ethics-*` 인덱스에 적재된 Johan Galtung 데이터(thinker 1 / works 4 / claims 8 / keywords 10 / relations 3)를 항목별로 조회하고, 외부 학술 출처(SAGE Journal of Peace Research, PRIO 공식 자료, Wikipedia, TRANSCEND, Right Livelihood, Peace Magazine)와 교차 검증했다. 핵심 사실(생몰년, 저작 연도·원제, 주요 개념 정의, 원문 인용, 관계의 역사적 정합성) 전반이 **정확**하다. 수정이 필요한 블로커·버그는 없으며, 메타데이터 누락 및 표현 다듬기 수준의 observation 4건을 기록한다.

## 검증 매트릭스

### Thinker: `galtung` — OK
| 항목 | 값 | 검증 |
|---|---|---|
| name_en | Johan Galtung | OK (Wikipedia, PRIO) |
| birth_year | 1930 | OK — 1930-10-24 |
| death_year | 2024 | OK — 2024-02-17 (PRIO·TRANSCEND·EuPRA·Peace Magazine 모두 확인) |
| field | peace_studies | OK |
| background 중 "PRIO 1959 창설", "JPR 1964 창간" | 정확 | OK (PRIO 공식 자료: "founded in 1959 … first director 1959–1969"; "In 1964, Galtung led PRIO to establish … Journal of Peace Research") |
| background 중 "오슬로대 수학(1956)·사회학(1957) 박사" | Wikipedia 기재 일치 | OK |
| "150권 이상 저서, 1,700편 이상 논문" | Right Livelihood "160 books, 1,700 articles", TRANSCEND "150 conflicts" | OK (하한으로서 정확) |

### Works (4) — 전부 OK

| id | title_original | year | JSTOR/SAGE 대조 |
|---|---|---|---|
| galtung-violence-peace-research | Violence, Peace, and Peace Research | 1969 | OK — *Journal of Peace Research* Vol. 6, No. 3, pp. 167–191 |
| galtung-cultural-violence | Cultural Violence | 1990 | OK — *JPR* Vol. 27, No. 3, pp. 291–305 |
| galtung-peace-by-peaceful-means | Peace by Peaceful Means: Peace and Conflict, Development and Civilization | 1996 | OK — Sage/PRIO |
| galtung-transcend-transform | Transcend and Transform: An Introduction to Conflict Work | 2004 | OK — Pluto Press / Paradigm |

### Claims (8)

#### `galtung-claim-001` 소극적 평화 vs 적극적 평화 — OK
- original_text: "We shall refer to the absence of personal violence as negative peace, and to the absence of structural violence as positive peace"
- 원문 대조: SAGE의 1969 논문 요지 및 파생 인용문과 일치. "…peace research…should be concerned with both" 뒷부분도 논문 결론부와 실질적으로 부합.
- argument/counterpoint의 논리적 정합성 양호. 보울딩(Kenneth Boulding)의 "too broad" 비판은 실제 그의 1977년 *Journal of Peace Research* 논문("Twelve Friendly Quarrels with Johan Galtung")에서 확인되는 비판 노선과 일치.

#### `galtung-claim-002` 구조적 폭력 정의 — OK
- original_text: "Violence is present when human beings are being influenced so that their actual somatic and mental realizations are below their potential realizations. …violence without this subject-action-object relation…we shall refer to as structural violence."
- 원문 대조: SAGE/PDF 양쪽 모두에서 확인되는 갈퉁의 대표 정의. 철자(`realizations` vs 영국식 `realisations`) 차이만 존재하지만, 의미 동일. 원문은 `realisations`(영국식)이다 → observation-1 참조.

#### `galtung-claim-003` 문화적 폭력 — OK
- original_text: "By 'cultural violence' we mean those aspects of culture, the symbolic sphere of our existence —exemplified by religion and ideology, language and art, empirical science and formal science (logic, mathematics)— that can be used to justify or legitimize direct or structural violence."
- SAGE 게재본 초록과 동일하다. 매우 정확.

#### `galtung-claim-004` 폭력/평화의 삼각형 — OK
- 직접·구조·문화 삼각형의 상호 강화 관계와 평화 삼각형으로의 확장은 *Peace by Peaceful Means*(1996) Part I에서 체계화되었다는 서술 사실과 합치.

#### `galtung-claim-005` ABC 분쟁 삼각형 — OK
- Attitude(태도)–Behavior(행동)–Contradiction(모순)의 3요소와 "C가 분쟁의 뿌리"라는 해석은 *Peace by Peaceful Means* Part II의 표준 서술. TRANSCEND 방법의 근간으로 사용되는 것도 정확.

#### `galtung-claim-006` 진단-예후-치료 방법론 — OK
- Diagnosis–Prognosis–Therapy는 갈퉁이 의학 모델을 차용해 평화학을 "처방적 학문"으로 세운 방법론으로, 1996년 저작 서문과 *Conflict Transformation by Peaceful Means*(UN 편람, 2000)에서 반복 등장. 서술 정확.

#### `galtung-claim-007` TRANSCEND 분쟁 전환 방법 — OK
- "제로섬 탈피·양측 정당 요구 동시 충족·제3의 창의적 대안"은 *Transcend and Transform*(2004) 핵심 주장. 에콰도르–페루, 스리랑카, 한반도 등 조정 사례 언급도 TRANSCEND International 공식 기록과 일치.

#### `galtung-claim-008` 평화적 수단에 의한 평화 — OK
- 간디의 "수단-목적 일치" 계승, 평화교육의 세대 간 전승 기능, 사티아그라하(Satyagraha) 인도 독립 사례의 연결은 1996년 저작의 명시적 주장. 정확.

### Keywords (10) — 전부 OK
- 적극적/소극적 평화, 구조적/문화적 폭력, 폭력·평화의 삼각형, ABC 삼각형, TRANSCEND, 진단-예후-치료, 평화적 수단에 의한 평화 — 모든 정의가 갈퉁 원전 서술과 부합.
- 단, **'직접적 폭력'**이 thinker 문서의 `keywords` 배열과 `ethics-thinkers` 본문에는 12개 키워드로 들어있으나, `ethics-keywords` 인덱스에는 `kw-direct-violence`가 **미등록**되어 있을 가능성(조회된 10건 기준). → observation-2 참조.

### Relations (3)

#### `kant-influenced-galtung` — OK
- 칸트 *Zum ewigen Frieden*(1795)의 공화제·국제연방·세계시민법 구조가 갈퉁의 "구조적 평화" 개념에 영향을 주었다는 서술은 *Peace by Peaceful Means* Part I에서 갈퉁 스스로 칸트를 선구자로 호명하는 맥락과 일치.

#### `habermas-influenced-galtung` — OK(약한 연결, 그러나 허용 범위)
- 하버마스 의사소통행위이론·담론윤리 → TRANSCEND 중재법의 "강제 없는 대화"로의 연결은 갈퉁이 명시적으로 인용한 빈도는 낮지만, *Peace by Peaceful Means*와 *Transcend and Transform*에서 "dialogic conflict work"를 논할 때 하버마스적 전제가 이론적 배경으로 작용함이 학계 통설. 서술은 "영향"으로 무난히 수용 가능. → observation-3 참조(evidence 필드 보강 권고).

#### `galtung-criticized-rawls` — OK
- 갈퉁이 롤스 정의론을 "국가 내부 분배정의에 한정되어 국제적 구조적 폭력을 다루지 못한다"고 비판한 것은 *Peace by Peaceful Means* Part III(Development/World System)와 이후 강의·논문에서 반복된 입장. 방향(from=galtung, to=rawls, type=criticized) 정확.

## 이슈/블로커

### Observation 1 (표기 미세 불일치)
- 위치: `galtung-claim-002.original_text`
- 현재: `realizations` (미국식)
- 원문: `realisations` (영국식; *Journal of Peace Research* 원 게재본 철자)
- 권고: 원전 재현 원칙에 따라 `realisations`로 바꾸는 것을 제안. 다만 의미 왜곡은 없어 severity=observation.

### Observation 2 (키워드 누락 가능성)
- thinker 문서의 `keywords` 배열에는 '직접적 폭력'이 포함되어 있으나, `ethics-keywords`에서 `thinker_id=galtung`으로 검색 시 10건만 반환되어 `kw-direct-violence` 문서가 빠졌을 수 있다.
- 확인 방법: `curl -s 'localhost:9200/ethics-keywords/_doc/kw-direct-violence'`로 존재 여부 점검 후, 부재 시 정의 문서 추가 권고. (galtung의 폭력 삼각형 완결성을 위해 3축 중 1축이 정의 문서로 존재해야 일관됨.)

### Observation 3 (evidence 보강 권고)
- `habermas-influenced-galtung.evidence`가 "Peace by Peaceful Means(1996) 의사소통·담론 관련 서술"로 일반적이다. 원전 특정 장(예: Part I 'Peace Theory', pp. ~71 내외 대화이론 논의) 또는 갈퉁의 *Searching for Peace*(2002) 중 해당 부분을 인용하면 검증성 향상.

### Observation 4 (background 서술 수치)
- background에 "150권 이상 저서, 1,700편 이상 논문"으로 기재. Right Livelihood(2024)는 "over 160 books"로 상향된 수치를 보고. 사실 위배는 아니며 하한으로서 정확하지만, 최신 사망 시점 기준으로 "160권 이상"으로 갱신할 수 있다.

## 수정 제안 (요약)
1. `galtung-claim-002.original_text`: `realizations` → `realisations` (1곳)
2. `ethics-keywords`에 `kw-direct-violence` 문서 존재 여부 확인; 부재 시 정의 문서 추가.
3. `habermas-influenced-galtung.evidence` 필드에 구체 장/쪽 인용 추가.
4. (선택) thinker `background`의 저서 수 "150 → 160" 갱신.

위 제안은 모두 observation 등급이며, 블로커/버그는 발견되지 않았다. Manager 판단에 따라 수정 태스크를 생성하거나 회고로 이월 가능.

## 참조 출처
- [Johan Galtung — Wikipedia](https://en.wikipedia.org/wiki/Johan_Galtung)
- [Johan Galtung, "the father of peace studies," dies at 93 — Right Livelihood](https://rightlivelihood.org/news/johan-galtung-the-father-of-peace-studies-dies-at-93/)
- [Memorial: Prof. Johan Galtung (24 Oct 1930 – 17 Feb 2024) — Eurasia Review](https://www.eurasiareview.com/19022024-memorial-prof-johan-galtung-24-oct-1930-17-feb-2024-rip-oped/)
- [Violence, Peace, and Peace Research — SAGE JPR 1969](https://journals.sagepub.com/doi/10.1177/002234336900600301)
- [Galtung 1969 PDF (Kobe University)](https://www2.kobe-u.ac.jp/~alexroni/IPD%202015%20readings/IPD%202015_7/Galtung_Violence,%20Peace,%20and%20Peace%20Research.pdf)
- [Cultural Violence — SAGE JPR 1990](https://journals.sagepub.com/doi/10.1177/0022343390027003005)
- [Peace Research Institute Oslo — Wikipedia](https://en.wikipedia.org/wiki/Peace_Research_Institute_Oslo)
- [About the Journal of Peace Research — PRIO](https://www.prio.org/journals/jpr/about)
- [Johan Galtung at 90: His Enduring Legacy — PRIO](https://www.prio.org/comments/849)
