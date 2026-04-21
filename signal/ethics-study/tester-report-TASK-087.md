# Tester Report — TASK-087

## 태스크
붓다(석가모니) 데이터 검증

## 상태
DONE

## 검증 요약

| 인덱스 | 건수 | 결과 |
|--------|------|------|
| ethics-thinkers | 1 | PASS |
| ethics-works | 4 | PASS |
| ethics-claims | 10 | PASS (이슈 2건 — 경미) |
| ethics-keywords | 10 | PASS |
| ethics-relations | 4 (+1 외부) | PASS (이슈 1건 — 경미) |

**종합 판정: PASS** — 수정 필수 사항 없음. 아래 경미 이슈는 개선 권고.

---

## 1. Thinker 검증

### 기본 정보
- id: `buddha` / name: 붓다 (석가모니, 고타마 싯다르타) / name_en: Buddha (Siddhartha Gautama) — **정확**
- field: `eastern_ethics` — **정확**
- era: 고대 인도 — **정확**
- birth_year: -563 / death_year: -483 — **전통적 연대 채택, 허용 범위 내**
  - 학계에서는 전통 연대(BC 563~483)와 수정 연대(BC 480~400 전후) 양설이 있다. 전통 연대를 채택한 것은 한국 윤리교육 교재의 일반적 기술과 부합한다.
  - **권고**: background 또는 별도 필드에 "수정 연대설(BC 480~400 전후)도 있음"을 한 줄 언급하면 더 완전하겠으나, 현재 상태로도 시험 준비에 문제없음.

### 배경·핵심사상·사상형성 서술
- **background**: 사문유관(四門遊觀), 29세 출가, 6년 고행, 35세 성도(부다가야 보리수), 45년 교화, 80세 쿠시나가라 입멸 — **정확**. 팔리 전승 및 한국 교재 기술과 부합.
- **core_philosophy**: 사성제·팔정도·연기·삼법인·무아·중도·자비/사무량심·오온·십이연기 — **핵심 교리 모두 포함, 서술 정확**.
- **philosophical_journey**: 시기별(출가 이전→고행기→성도기→교화기→입멸) 구분이 명확하고 정확. 알라라 칼라마·웃다카 라마풋타 언급도 적절.
- **keywords**: 10개 — 사성제, 팔정도, 연기, 삼법인, 중도, 무아, 자비, 사무량심, 오온, 십이연기 — **핵심 개념 모두 포함**.

## 2. Works 검증

### buddha-dhammapada (법구경)
- title_original: "Dhammapada (팔리어)" — **정확**
- year: -300 — 현존 팔리어 본의 편찬 시기로 적절 (붓다의 직접 저술이 아니라 편찬 경전)
- significance: 423게송, 소부 소속, 26주제 — **정확**
- key_concepts: 마음, 덕, 팔정도, 업, 열반 — **적절**

### buddha-sutta-nipata (숫타니파타)
- title_original: "Sutta Nipāta (팔리어)" — **정확**
- year: -400 — 아타카바가·파라야나바가의 고층을 감안하면 적절
- significance: 가장 오래된 경전층, 아타카바가·파라야나바가 언급, "무소의 뿔" 이미지 — **정확**
- key_concepts: 집착 없음, 중도, 수행자의 길, 무아, 열반 — **적절**

### buddha-majjhima-nikaya (중아함경)
- title_original: "Majjhima Nikāya (팔리어) / 中阿含經 (한역)" — **정확** (팔리어 원제와 한역 병기)
- year: -300 — 편찬 시기로 적절
- significance: 152편 설법, 사부 니카야 — **정확**
- key_concepts: 사성제, 무아, 연기, 팔정도, 중도 — **적절**
- **경미 참고**: significance에서 "아낫타락카나 경(無我相經)이 중요하다"고 했는데, 이 경은 SN 22.59로 상윳따 니카야(SN) 소속이다. 다만 무아의 교리 자체는 MN에도 풍부하므(MN 35, MN 22 등) 문맥상 큰 오류는 아님.

### buddha-digha-nikaya (장아함경)
- title_original: "Dīgha Nikāya (팔리어) / 長阿含經 (한역)" — **정확**
- year: -300 — 편찬 시기로 적절
- significance: 34편, 대반열반경 포함, 마하니다나 경, 사무량심 — **정확**
- key_concepts: 열반, 연기, 자비, 사무량심, 마지막 가르침 — **적절**

## 3. Claims 검증

### claim-001: 사성제 (四聖諦)
- **출처**: SN 56.11 (Dhammacakkappavattana Sutta) + MN 141 — **정확**. 초전법륜경은 SN 56.11이 맞고, MN 141(사성제분별경)도 사성제 상세 설명 경전으로 적합.
- **팔리어 원문**: `idaṃ dukkhaṃ ariyasaccaṃ...` — **정확**. SN 56.11의 실제 팔리어 구절과 일치.
- **설명**: 고·집·멸·도 네 가지 정식화 정확. 갈애(taṇhā) 세 종류(감각적·존재·소멸) 언급도 정확.
- **counterpoint**: 니체 비판 언급 + 서양 철학적 치료법 비교 — 적절. 다만 니체의 비판은 『도덕의 계보』보다 『반그리스도(Der Antichrist)』가 더 직접적 출처. 하지만 도덕의 계보에서도 금욕적 이상 비판 맥락에서 불교를 언급하므로 완전히 틀리지는 않음.
- **판정: PASS**

### claim-002: 팔정도 (八正道)
- **출처**: SN 56.11 + MN 44 — **정확**.
- **팔리어 원문**: `ayameva ariyo aṭṭhaṅgiko maggo, seyyathidaṃ: sammādiṭṭhi...` — **정확**.
- **설명**: 여덟 가지 구성 정확, 계·정·혜 삼학 분류 정확.
  - 정견·정사유 = 혜(慧) — **정확**
  - 정어·정업·정명 = 계(戒) — **정확**
  - 정정진·정념·정정 = 정(定) — **정확**
- **counterpoint**: 비구 중심 설법의 재가자 적용 한계 — 적절한 비판점.
- **판정: PASS**

### claim-003: 연기 (緣起)
- **출처**: DN 15 (Mahānidāna Sutta) + MN 38 — **정확**. DN 15는 연기의 핵심 경전.
- **팔리어 원문**: `imasmiṃ sati idaṃ hoti...` — **정확**. 이 정식(此有故彼有 공식)은 초기불교의 가장 핵심적인 연기 정식으로, SN 12.61 등에서도 반복됨.
- **설명**: 상호의존적 발생, 고정 실체 부정, 무아와의 연결 — **정확**.
- **counterpoint**: 나가르주나의 공(śūnyatā) 발전 언급 — **정확하고 적절**.
- **판정: PASS**

### claim-004: 무아 (無我)
- **출처**: SN 22.59 (Anattalakkhaṇa Sutta) + MN 35 — **정확**. SN 22.59는 무아상경의 정확한 위치.
- **팔리어 원문**: `rūpaṃ, bhikkhave, anattā...` — **정확**.
- **설명**: 오온 분석, 우파니샤드 아트만과 대립, 허무주의가 아닌 집착 해소 — **정확**.
- **counterpoint**: 무기(avyākata) 전략과의 긴장, 학파 간 해석 차이 — **적절하고 정확**.
- **판정: PASS**

### claim-005: 중도 (中道)
- **출처**: SN 56.11 + MN 36 — SN 56.11은 정확. **MN 36은 Mahāsaccaka Sutta(큰 삭까 경)** — 이 경은 붓다의 고행 체험과 중도 전환을 다루므로 출처로 적합.
- **팔리어 원문**: `ete te, bhikkhave, ubho ante anupagamma majjhimā paṭipadā...` — **정확**. SN 56.11의 실제 구절.
- **설명**: 쾌락주의·고행주의 양극단, 거문고 줄 비유 — **정확**.
- **counterpoint**: 절충주의와의 차이, 형이상학적 확장(有無·常斷) — **적절**.
- **판정: PASS**

### claim-006: 삼법인 (三法印)
- **출처**: AN 3.136; SN 22.59; SN 22.16 — **적절**. 삼법인의 출처 지정이 까다로운데, 여러 경전에서 반복 설해지므로 복수 출처 기재가 적합.
- **팔리어 원문**: `sabbe saṅkhārā aniccā ti, sabbe saṅkhārā dukkhā ti, sabbe dhammā anattā ti.` — **정확**. 세 번째 법인에서 saṅkhārā가 아닌 dhammā(법)를 사용한 것이 정확한 구분 (제법무아는 조건 지어진 것뿐 아니라 모든 법에 적용).
- **설명**: 무상·고·무아 각각 정확. 위빠사나 관찰 대상 언급도 적절.
- **counterpoint**: 사법인(四法印) 언급, 대승의 열반적정 대체 — **정확**.
- **판정: PASS**

### claim-007: 자비·사무량심
- **출처**: Sn 1.8 (Karaṇīya Mettā Sutta) + DN 13 + AN 4.125 — **정확**. Sn 1.8은 자비경의 정확한 위치. DN 13(Tevijja Sutta, 삼명경)은 사무량심 핵심 경전.
- **팔리어 원문**: `mettaṃ ca sabbalokasmiṃ, mānasaṃ bhāvaye aparimāṇaṃ...` — **정확**. Karaṇīya Mettā Sutta의 실제 게송.
- **설명**: 사무량심 네 가지(자·비·희·사) 정확, brahma-vihāra 용어 사용 정확.
- **counterpoint**: 공리주의와의 비교, 사(upekkhā)의 오해 방지 — **적절**.
- **판정: PASS**

### claim-008: 오온 (五蘊)
- **출처**: SN 22.59 + SN 22 (Khandhasaṃyutta) — **정확**.
- **팔리어 원문**: `rūpaṃ, bhikkhave, anattā. rūpañca h'idaṃ...` — **정확**. SN 22.59의 실제 구절.
- **설명**: 색·수·상·행·식 각각의 팔리어와 설명 정확. 아견(sakkāyadiṭṭhi) 언급 정확.
- **counterpoint**: 설일체유부 극미설, 유식학파 재해석 — **정확**.
- **판정: PASS**

### claim-009: 십이연기 (十二緣起)
- **출처**: DN 15 (Mahānidāna Sutta) + SN 12 (Nidānasaṃyutta) — **정확**.
- **팔리어 원문**: `avijjāpaccayā saṅkhārā; saṅkhārapaccayā viññāṇaṃ...` — **정확**. 십이연기 정식의 표준 팔리어.
- **설명**: 12지 순서 정확 (무명→행→식→명색→육처→촉→수→애→취→유→생→노사). 환멸연기 언급 정확.
- **counterpoint**: 삼생 해석 vs 찰나연기 해석 차이 — **정확**.
- **경미 이슈**: claim의 산스크리트어 표기 `dvādasāṅga-pratītyasamutpāda`는 맞지만, keyword에서는 `dvādaśāṅga-pratītyasamutpāda`로 되어 있다. 둘 다 사용되는 표기이므로 심각한 오류는 아니나 통일이 바람직함.
- **판정: PASS (경미 이슈)**

### claim-010: 마음(心)이 모든 법의 선두
- **출처**: Dhammapada v.1-2 + v.183-185 — **정확**. 법구경 첫 게송(v.1-2)은 가장 유명한 구절.
- **팔리어 원문**: `manopubbagamā dhammā, manoseṭṭhā manomayā...` — **정확**. 법구경 제1게송의 정확한 팔리어.
- **설명**: 의도(cetanā) 중심 윤리, AN 6.63 인용(cetanāhaṃ, bhikkhave, kammaṃ vadāmi) — **정확**.
- **counterpoint**: 결과주의와의 대비 — **적절**.
- **판정: PASS**

## 4. Keywords 검증

10개 키워드 모두 검증:

| ID | term | term_en | 팔리어 포함 | 정확성 |
|----|------|---------|------------|--------|
| buddha-kw-four-noble-truths | 사성제 | Four Noble Truths (cattāri ariyasaccāni) | O | PASS |
| buddha-kw-eightfold-path | 팔정도 | Noble Eightfold Path (ariyo aṭṭhaṅgiko maggo) | O | PASS |
| buddha-kw-pratityasamutpada | 연기 | Dependent Origination (pratītyasamutpāda / paṭicca-samuppāda) | O | PASS |
| buddha-kw-anatta | 무아 | Non-self (anattā / anātman) | O | PASS |
| buddha-kw-middle-way | 중도 | Middle Way (majjhimā paṭipadā) | O | PASS |
| buddha-kw-three-marks | 삼법인 | Three Marks of Existence (ti-lakkhaṇa) | O | PASS |
| buddha-kw-metta-karuna | 자비 | Loving-kindness and Compassion (mettā-karuṇā) | O | PASS |
| buddha-kw-five-aggregates | 오온 | Five Aggregates (pañcakkhandhā) | O | PASS |
| buddha-kw-twelve-links | 십이연기 | Twelve Links of Dependent Origination | O | PASS |
| buddha-kw-nibbana | 열반 | Nibbāna / Nirvāṇa | O | PASS |

- definition 내용이 각 claim의 explanation과 일관되며 정확함
- related_terms가 적절하게 상호 참조됨
- 팔리어/산스크리트어 표기가 전반적으로 정확

## 5. Relations 검증

### buddha-rel-001: buddha → nagarjuna (influenced)
- **방향**: 붓다가 나가르주나에게 영향 → **정확** (시간순으로도 맞음: BC 5세기 → CE 2~3세기)
- **설명**: 연기→공(śūnyatā), 중론(Mūlamadhyamakakārikā) 제24장 — **정확**
- **판정: PASS**

### buddha-rel-002: buddha → wonhyo (influenced)
- **방향**: 붓다가 원효에게 영향 → **정확** (BC 5세기 → CE 7세기)
- **설명**: 화쟁 사상, 일심 사상, 중도 정신 계승 — **정확**
- **판정: PASS**

### buddha-rel-003: buddha → confucius (influenced)
- **방향/타입**: `type: influenced`이지만 description에 "직접적 교류 없음", "비교·대화의 관계"라고 명시
- **경미 이슈**: `type: influenced`가 실제 관계(비교·대화)와 맞지 않는다. `type: compared_with` 또는 다른 관계 타입이 더 적합할 수 있다. 다만 현 스키마의 type 선택지(influenced_by, developed, criticized, synthesized)에 비교 관계 타입이 없으므로, description에서 보충 설명한 현재 방식은 차선으로 수용 가능.
- **추가 참고**: from: buddha → to: confucius 방향에서 "influenced"는 "붓다가 공자에게 영향을 주었다"인데, 실제로는 두 사람이 동시대이고 직접 교류가 없었으므로 이 방향이 어색하다. description에서 이를 보완하고 있으나 구조적으로는 부정확.
- **판정: PASS (경미 이슈 — description 보완으로 수용 가능)**

### buddha-rel-004: upanishad → buddha (influenced)
- **방향**: 우파니샤드가 붓다에게 영향 → **정확** (우파니샤드 전통이 선행)
- **설명**: 아트만 비판적 계승, 해탈·윤회 개념 수용, 무아 주장 — **정확**
- **참고**: from_thinker가 `upanishad`인데, 이는 실제 사상가가 아닌 사상 전통. coder report에서 이를 인지하고 있음.
- **판정: PASS**

### huineng-rel-001 (외부 — 혜능 데이터에서 생성)
- 이 관계는 buddha 데이터 입력이 아닌 혜능(huineng) 데이터에서 생성된 것으로, buddha TASK의 검증 범위에는 포함하지 않음. 다만 내용은 정확함(붓다→혜능 영향, 금강경·돈오·무념).

## 경미 이슈 정리

| # | 영역 | 내용 | 심각도 | 수정 필요 |
|---|------|------|--------|----------|
| 1 | claim-009 / kw-twelve-links | 산스크리트어 표기 불일치 (dvādasāṅga vs dvādaśāṅga) | 낮음 | 권고 (통일) |
| 2 | rel-003 | buddha→confucius의 type: influenced가 비교/대화 관계와 불일치 | 낮음 | 권고 (description 보완으로 현재 수용 가능) |

## 학술적 정확성 총평

1. **사성제·팔정도**: 초전법륜경(SN 56.11) 출처 정확, 팔리어 원문 정확, 고·집·멸·도와 팔정도 8지 구성 모두 정확.
2. **연기·무아**: 팔리어 정식(imasmiṃ sati idaṃ hoti...) 정확, 무아상경(SN 22.59) 출처 정확, 우파니샤드 아트만 비판 맥락 정확.
3. **중도·삼법인**: 중도의 양극단(kāmasukhallikānuyoga / attakilamathānuyoga) 정확, 삼법인에서 제법무아의 dhammā 사용 정확(saṅkhārā가 아닌 dhammā — 중요한 구분).
4. **팔리어 원문**: 10건 모든 claim에 팔리어 원문 포함. 표기의 정확성이 전반적으로 높음(diacritics 포함).
5. **counterpoint**: 모든 claim에 반론/한계/후대 비판 포함. 사상가+저서 지정이 명확한 경우(니체, 나가르주나 중론 등)가 있고 일반적 학파 수준의 언급도 있어 전체적으로 양호.
6. **생몰년**: 전통 연대(-563/-483) 채택은 한국 윤리교육 맥락에서 적절.
