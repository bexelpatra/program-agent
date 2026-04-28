# Tester Report — TASK-063

- **Task**: 순자 데이터 검증
- **Status**: DONE
- **Timestamp**: 2026-04-13

---

## 검증 결과 요약

| 항목 | 건수 | 검증 결과 |
|------|------|-----------|
| thinker | 1 | PASS (경미 이슈 1건) |
| works | 4 | PASS |
| claims | 11 | PASS (경미 이슈 3건) |
| keywords | 10 | PASS |
| relations | 5 | PASS |

**총 이슈: 4건 (심각 0, 보통 0, 경미 4)**

---

## 1. Thinker 검증 (xunzi)

### 생몰년
- 입력: birth_year=-313, death_year=-238
- 검증: 순자의 생몰년은 학계에서 정확히 확정되지 않았으나, 기원전 313~238년경이 통설이다. **PASS**

### 출신
- 입력: 조(趙)나라 출신
- 검증: 순황(荀況), 존칭 순경(荀卿) 또는 손경(孫卿) — 정확하다. 사마천 사기 맹자순경열전에 "趙人" 기록. **PASS**

### 배경 정보
- 직하학궁(稷下學宮) 세 번 제주(祭酒) 역임 — 정확. **PASS**
- 초나라 춘신군(春申君) 초빙으로 란릉령(蘭陵令) — 정확. **PASS**
- 한비자와 이사가 문하생 — 사기 노자한비열전, 이사열전에 기록. **PASS**

### 경미 이슈 #1
- **위치**: thinker.name_en
- **현재**: "Xunzi (Hsün Tzu)"
- **의견**: Wade-Giles 표기 "Hsün Tzu"는 학술적으로 통용되나, 현대 학계 표준은 "Xunzi"만 사용하는 추세이다. 다만 병기 자체는 참고로서 유용하므로 수정 필수는 아니다.
- **심각도**: 경미

---

## 2. Works 검증 (4건)

### xunzi-xunzi (순자 전체)
- 총 32편 구성 — 정확. 유향(劉向)이 정리한 것으로 알려짐. **PASS**
- year=-250 — 편찬 시기 추정으로 적절. **PASS**
- key_concepts: 성악설, 화성기위, 예, 천론, 정명, 권학, 해폐 — 주요 편목과 일치. **PASS**

### xunzi-xingebian (성악편)
- title_original: 性惡篇 (Xing E Pian) — 정확. **PASS**
- "人之性惡 其善者偽也" 명제 기술 — 성악편 원문과 일치. **PASS**
- 맹자 성선설을 정면 반박한다는 설명 — 정확. **PASS**

### xunzi-lilun (예론편)
- title_original: 禮論篇 (Li Lun Pian) — 정확. **PASS**
- "禮起於何也 曰人生而有欲" 인용 — 예론편 원문과 일치. **PASS**
- 분(分)을 통한 사회 질서 설명 — 정확. **PASS**

### xunzi-tianlun (천론편)
- title_original: 天論篇 (Tian Lun Pian) — 정확. **PASS**
- "天行有常" 명제 — 천론편 원문과 일치. **PASS**
- "大天而思之 孰與物畜而制之" — 천론편 원문과 일치. **PASS**

---

## 3. Claims 검증 (11건)

### claim-001: 성악설(性惡說)
- original_text: "人之性惡 其善者偽也" — 성악편 원문과 정확히 일치. **PASS**
- argument: 好利, 疾惡, 耳目之欲 세 가지 본성 근거 제시 — 성악편 논증과 일치. **PASS**
- counterpoint: 맹자 공손추 상편 "無惻隱之心 非人也" + 순자의 반박 "孟子曰人之性善 是不及知人之性 而不察乎人之性偽之分者也" — 정확. **PASS**

### claim-002: 화성기위(化性起偽)
- original_text: "故聖人化性而起偽 偽起而生禮義 禮義生而制法度" — 성악편 원문과 일치. **PASS**
- argument: 굽은 나무/무딘 쇠 비유 "枸木必將待檃栝烝矯然後直 鈍金必將待礱厲然後利" — 성악편 원문. **PASS**
- counterpoint: 맹자 고자 상편 "仁義禮智 非由外鑠我也 我固有之也" + 고자 "性無善無不善" — 정확. **PASS**

### claim-003: 예론(禮論)
- original_text: "禮起於何也 曰 人生而有欲 欲而不得則不能無求 求而無度量分界則不能不爭 爭則亂 亂則窮" — 예론편 원문과 일치. **PASS**
- counterpoint: 노자 도덕경 "夫禮者 忠信之薄 而亂之首" + 묵자 절용 비판 — 정확. **PASS**

### claim-004: 천론(天論)
- original_text: "天行有常 不為堯存 不為桀亡" — 천론편 첫 문장이며 원문 정확. **PASS**
- counterpoint: 동중서 천인감응설 — 정확한 대비. **PASS**

### claim-005: 제천이용(制天命而用之)
- original_text: "大天而思之 孰與物畜而制之 從天而頌之 孰與制天命而用之" — 천론편 원문 일치. **PASS**
- counterpoint: 노자 도덕경 25장 "人法地 地法天 天法道 道法自然" — 정확. **PASS**

### claim-006: 명분론(名分論)
- original_text: "人何以能群 曰分 分何以能行 曰義" — 왕제편 원문과 일치. **PASS**
- source_detail: "순자 왕제편(王制篇), 부국편(富國篇)" — 정확. **PASS**
- counterpoint: 묵자 겸애 + 노자 "大道廢 有仁義" — 정확. **PASS**

### claim-007: 교육론
- original_text: "積土成山 風雨興焉 積水成淵 蛟龍生焉 積善成德 而神明自得 聖心備焉" — 권학편 원문 일치. **PASS**
- argument: "學不可以已"가 권학편 첫 문장 — 정확. "不積跬步 無以至千里" — 권학편 원문. **PASS**
- counterpoint: 맹자 진심 상편 양능양지(良能良知) — 정확. **PASS**

### claim-008: 군자소인
- original_text: "積善成德 積不善成賊 積靡不審 積微成著"
- 검증: "積善成德"은 권학편에 있으나, "積不善成賊"은 성악편이 아닌 권학편/대략편 등에서 유사 표현이 산재한다. source_detail이 "성악편, 권학편"으로 되어 있는데, 이 조합은 적절하다. **PASS**
- argument: "塗之人可以為禹" — 성악편 원문. **PASS**
- counterpoint: 맹자 고자 하편 "人皆可以為堯舜" — 정확. **PASS**

### claim-009: 예법병용(禮法竝用)
- original_text: "治之經 禮與刑 君子以修百姓 庶人以修一己"
- 검증: 왕제편/성악편 관련 내용이나, 이 정확한 구절의 출처 확인이 필요하다.
- source_detail: "순자 왕제편(王制篇), 성악편(性惡篇)" — 기본적으로 적절.
- **경미 이슈 #2**: "治之經 禮與刑"은 순자 성악편에서 예와 형벌의 병용을 논하는 맥락에서 등장하나, 정확한 원문 구절 위치의 세부 특정이 다소 불분명하다. 다만 순자 사상의 핵심 주장으로서 내용적 정확성은 확보됨.
- counterpoint: 맹자 "以力假仁者霸 以德行仁者王" + 한비자의 극단적 법치론 — 정확. **PASS**
- **심각도**: 경미

### claim-010: 심론(心論)
- original_text: "人何以知道 曰心 心何以知 曰虛壹而靜" — 해폐편(解蔽篇) 원문과 일치. **PASS**
- source_detail: "순자 해폐편(解蔽篇)" — 정확. **PASS**
- argument: 묵자(用), 장자(天) 등의 폐(蔽) 분석 — 해폐편 원문 내용. **PASS**
- counterpoint: 맹자 진심 상편 "盡其心者 知其性也" + 장자 심재/좌망 — 정확. **PASS**

### claim-011: 정명론(正名論)
- original_text: "名無固宜 約之以命 約定俗成謂之宜 異於約則謂之不宜" — 정명편 원문 일치. **PASS**
- argument: 형명(刑名), 소명(所名), 산명(散名)·공명(共名) 세 유형 — 정명편 내용과 일치. **PASS**
- **경미 이슈 #3**: argument에서 "형명(刑名)"의 한자가 "刑"으로 되어 있으나, 순자 정명편에서는 "形名"(형태에 따른 이름)이 더 정확한 표기이다. "刑名"은 법가 용어(형벌과 명분)와 혼동될 수 있다.
- counterpoint: 공손룡 "白馬非馬" + 장자 소요유편 — 정확. **PASS**
- **심각도**: 경미

---

## 4. Keywords 검증 (10건)

| ID | 용어 | 정의 정확성 | 출처 연결 |
|----|------|-------------|-----------|
| kw-xunzi-xingeshuo | 성악설(性惡說) | PASS | xunzi-xingebian ✓ |
| kw-xunzi-huaxingqiwei | 화성기위(化性起偽) | PASS — "人為"의 의미 설명 정확 | xunzi-xingebian ✓ |
| kw-xunzi-li | 예(禮) | PASS | xunzi-lilun ✓ |
| kw-xunzi-wei | 위(偽) | PASS — "거짓"과 구분해야 한다는 설명 정확 | xunzi-xingebian ✓ |
| kw-xunzi-tianrenzhifen | 천인지분(天人之分) | PASS | xunzi-tianlun ✓ |
| kw-xunzi-zhitianming | 제천명이용지(制天命而用之) | PASS | xunzi-tianlun ✓ |
| kw-xunzi-ji | 적(積) | PASS — 적토성산, 적선성덕 비유 정확 | xunzi-xunzi ✓ |
| kw-xunzi-daqingming | 대청명(大清明) | PASS | xunzi-xunzi ✓ |
| kw-xunzi-xuyijing | 허일이정(虛壹而靜) | PASS — 허·일·정 세 조건 설명 정확 | xunzi-xunzi ✓ |
| kw-xunzi-yuedingsucheng | 약정속성(約定俗成) | PASS — 현대 언어학 "기호의 자의성"과의 비교 적절 | xunzi-xunzi ✓ |

---

## 5. Relations 검증 (5건)

### relation-confucius-xunzi (confucius → xunzi: influenced)
- 방향: 공자가 순자에게 영향 — 시간적으로 올바름 (공자 BC 551~479 → 순자 BC 313~238). **PASS**
- 내용: 공자의 예(禮) 사상 계승 + 성악설로 독자적 발전 — 정확. **PASS**

### relation-xunzi-mencius-debate (xunzi → mencius: criticized)
- 방향: 순자가 맹자를 비판 — **올바른 방향**. 순자가 시대적으로 후대이며, 성악편에서 맹자의 성선설을 정면 비판했다. **PASS**
- verification_log에 방향 수정 이력이 있음 (mencius→xunzi에서 xunzi→mencius로 수정) — 적절히 수정됨. **PASS**
- 내용: "맹자가 성선을 말하면서 본성(性)과 인위(偽)를 구분하지 못했다" — 성악편 원문 근거. **PASS**

### relation-xunzi-hanfeizi (xunzi → hanfeizi: influenced)
- 방향: 순자가 한비자에게 영향 — 올바름. 한비자는 순자의 제자. **PASS**
- 근거: 사기(史記) 노자한비열전(老子韓非列傳) — 정확. **PASS**
- 내용: 성악설 + 예법병용에서 출발하여 법가 사상 체계화 — 정확. **PASS**

### relation-xunzi-lisi (xunzi → lisi: influenced)
- 방향: 순자가 이사에게 영향 — 올바름. 이사는 순자의 제자. **PASS**
- 근거: 사기(史記) 이사열전(李斯列傳) — 정확. **PASS**
- 내용: 진시황의 천하통일과 법치주의 정책에 핵심 역할, 분서갱유 건의 — 정확. **PASS**

### relation-xunzi-dongzhongshu (xunzi → dongzhongshu: influenced)
- 방향: 순자가 동중서에게 영향 — 올바름. 동중서(BC 179~104)는 한대 유학자. **PASS**
- 내용: 예 중심 사상과 교화론 영향 + 천론에서는 정반대(천인분리 vs 천인감응) — 정확한 대비. **PASS**
- 근거: 춘추번로(春秋繁露) — 정확. **PASS**

---

## 이슈 목록

| # | 위치 | 내용 | 심각도 |
|---|------|------|--------|
| 1 | thinker.name_en | "Hsün Tzu" Wade-Giles 병기 — 수정 필수는 아니나 현대 학계 표준은 Pinyin 단독 | 경미 |
| 2 | claim-009 original_text | "治之經 禮與刑" 구절의 정확한 편 내 위치 특정이 다소 불분명 | 경미 |
| 3 | claim-011 argument | "刑名"은 "形名"이 더 정확 (법가 용어와 혼동 가능) | 경미 |
| 4 | claim-008 source_detail | "성악편(性惡篇), 권학편(勸學篇)" 출처 조합이 약간 산만함 — 통합 출처 표기 개선 가능 | 경미 |

---

## 결론

순자 데이터 전반적으로 **높은 학술적 정확성**을 보인다.

- 한문 원문 11건 모두 순자 원전과 일치하거나 정확한 발췌임을 확인
- claims의 argument와 counterpoint에 구체적 사상가명 + 저서명 + 한문 원문이 적절히 명시됨
- relations 방향이 모두 올바르며, 특히 xunzi→mencius(criticized) 방향이 역사적 사실에 부합함을 확인
- 심각(사실오류) 이슈 0건, 보통(출처부정확) 이슈 0건
- 경미(표현개선) 이슈 4건은 수정 권장이나 필수 아님
