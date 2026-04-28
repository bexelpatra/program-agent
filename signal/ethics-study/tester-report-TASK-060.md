---
agent: tester
task_id: TASK-060
status: DONE
timestamp: 2026-04-13T14:30:00+09:00
---

## 결과 요약

맹자 데이터 전수 검증 완료. thinker 1건, works 4건, claims 17건, keywords 12건, relations 5건을 검증했다.

- **thinker**: 합격 (정확)
- **works**: 합격 (정확)
- **claims**: 조건부 합격 (심각 이슈 1건, 보통 이슈 2건)
- **keywords**: 합격 (정확)
- **relations**: 조건부 합격 (심각 이슈 2건, 보통 이슈 1건)

전체 판정: **조건부 합격** — 심각 이슈 3건 수정 필요

---

## 검증 상세

### 1. thinker -- 합격

| 항목 | 값 | 검증 |
|------|-----|------|
| id | mencius | OK |
| name | 맹자 | OK |
| birth_year | -372 | OK (기원전 372년, 통설) |
| death_year | -289 | OK (기원전 289년, 통설) |
| era | 중국 전국시대 | OK |
| background | 추(鄒)나라 출신, 맹모삼천지교, 자사 문인, 아성 등 | OK - 정확하고 풍부함 |
| core_philosophy | 성선설, 사단, 호연지기, 왕도정치, 역성혁명, 항산항심 | OK - 핵심 개념 포괄 |
| philosophical_journey | 초기/중기/말기 구분, 구체적 시기와 일화 | OK |
| keywords | 10개 | OK |

소견: background에 '맹가(孟軻)'라는 본명, 맹모삼천지교/단기지교 일화, 자사 문인 계통, 여러 나라 유세 경험, 사서 편입 과정 등이 정확하게 기술되어 있다. 생몰년은 학계 통설과 일치한다.

### 2. works -- 합격

| id | 제목 | 원제 | year | 검증 |
|----|------|------|------|------|
| mencius-mencius | 맹자 | 孟子 | -300 | OK - 7편 14편 구성 정확 |
| mencius-gongsunchou | 맹자 공손추편 | 孟子 公孫丑篇 | -300 | OK - 사단설/호연지기 설명 정확 |
| mencius-gaozi | 맹자 고자편 | 孟子 告子篇 | -300 | OK - 성선설 논변 설명 정확 |
| mencius-jinxin | 맹자 진심편 | 孟子 盡心篇 | -300 | OK - 진심/양지양능/민본 설명 정확 |

소견: 4건 모두 제목, 원제, significance, key_concepts가 정확하다. year -300은 맹자 저술 시기의 추정치로 적절하다.

### 3. claims -- 조건부 합격

17건 전수 검증 결과:

| claim ID | 주제 | 원문 정확성 | 출처 정확성 | work_id 정합성 | 판정 |
|----------|------|------------|------------|---------------|------|
| claim-001 | 성선설 | OK | OK (고자 6.2, 6.6) | OK (mencius-gaozi) | 합격 |
| claim-002 | 사단 | OK | OK (공손추 2.6) | OK (mencius-gongsunchou) | 합격 |
| claim-003 | 불인인지심 | OK | OK (공손추 2.6) | OK (mencius-gongsunchou) | 합격 |
| claim-004 | 인의예지 내재 | OK | **보통 이슈** | **보통 이슈** | 조건부 |
| claim-005 | 호연지기 | OK | OK (공손추 2.2) | OK (mencius-gongsunchou) | 합격 |
| claim-006 | 왕도정치 | OK | OK | OK (mencius-mencius) | 합격 |
| claim-007 | 역성혁명 | OK | OK (양혜왕 하 1.8) | OK (mencius-mencius) | 합격 |
| claim-008 | 항산항심 | OK | OK (양혜왕 1.7) | OK (mencius-mencius) | 합격 |
| claim-009 | 의리지변 | OK | OK (양혜왕 1.1) | OK (mencius-mencius) | 합격 |
| claim-010 | 민위귀 | OK | OK (진심 하 7.14) | OK (mencius-jinxin) | 합격 |
| claim-011 | 대장부 | OK | OK (등문공 하 3.2) | **심각 이슈** | 불합격 |
| claim-012 | 부동심/양기 | OK | OK (공손추 2.2) | OK (mencius-gongsunchou) | 합격 |
| claim-013 | 인정 | OK | OK (양혜왕 1.3, 1.7) | OK (mencius-mencius) | 합격 |
| claim-014 | 천인합일 | OK | OK (진심 7.1) | OK (mencius-jinxin) | 합격 |
| claim-015 | 양지양능 | OK | OK (진심 7.15) | OK (mencius-jinxin) | 합격 |
| claim-016 | 우산지목 비유 | OK | OK (고자 6.8) | OK (mencius-gaozi) | 합격 |
| claim-017 | 확충 | OK | OK (공손추 2.6) | OK (mencius-gongsunchou) | 합격 |

#### claim-004 상세 (보통 이슈)
- **문제**: `work_id`가 `mencius-gongsunchou`(공손추편)이지만, 원문 "仁義禮智 非由外鑠我也 我固有之也 弗思耳矣"는 **고자편(告子篇) 상 6.6**의 문장이다. source_detail에도 "공손추편 상 2.6"이 첫 번째 출처로 기재되어 있으나, 이 원문은 공손추편이 아닌 고자편에 있다.
- **권장 수정**: `work_id`를 `mencius-gaozi`로, source_detail의 첫 번째 출처를 "고자편(告子篇) 상 6.6"으로 변경

#### claim-011 상세 (심각 이슈)
- **문제**: `work_id`가 `mencius-jinxin`(진심편)이지만, `source_detail`은 "등문공편(滕文公篇) 하 3.2"이다. 대장부 구절("居天下之廣居...")은 등문공편 하 3.2의 내용이며, 진심편이 아니다. work_id와 source_detail이 불일치하며, 올바른 것은 등문공편이다.
- **필수 수정**: `work_id`를 `mencius-mencius`(전체 맹자)로 변경하거나, 등문공편을 별도 works로 추가해야 함. 현재 등문공편이 독립 works 문서로 존재하지 않으므로, `mencius-mencius`로 변경하는 것이 현실적.

#### 원문(original_text) 정합성

17건 모든 한문 원문을 검증한 결과:
- claim-001: "人性之善也 猶水之就下也 人無有不善 水無有不下" — 고자편 상 6.2 원문과 일치 ✓
- claim-002: "惻隱之心 仁之端也..." — 공손추편 상 2.6 원문과 일치 ✓
- claim-003: "人皆有不忍人之心..." — 공손추편 상 2.6 원문과 일치 ✓
- claim-004: "仁義禮智 非由外鑠我也 我固有之也 弗思耳矣" — **고자편** 상 6.6 원문과 일치 ✓ (단, 출처 표기 오류)
- claim-005: "其爲氣也 至大至剛..." — 공손추편 상 2.2 원문과 일치 ✓
- claim-006: "以力假仁者覇..." — 공손추편 상 2.3 원문과 일치 ✓
- claim-007: "賊仁者謂之賊 賊義者謂之殘..." — 양혜왕편 하 1.8 원문과 일치 ✓
- claim-008: "無恒産而有恒心者 惟士爲能..." — 양혜왕편 상 1.7 원문과 일치 ✓
- claim-009: "王何必曰利 亦有仁義而已矣" — 양혜왕편 상 1.1 원문과 일치 ✓
- claim-010: "民爲貴 社稷次之 君爲輕" — 진심편 하 14장 원문과 일치 ✓
- claim-011: "居天下之廣居..." — 등문공편 하 3.2 원문과 일치 ✓
- claim-012: "我四十不動心..." — 공손추편 상 2.2 원문과 일치 ✓
- claim-013: "五畝之宅 樹之以桑..." — 양혜왕편 상 1.3 원문과 일치 ✓
- claim-014: "盡其心者 知其性也..." — 진심편 상 7.1 원문과 일치 ✓
- claim-015: "人之所不學而能者 其良能也..." — 진심편 상 7.15 원문과 일치 ✓
- claim-016: "牛山之木嘗美矣..." — 고자편 상 6.8 원문과 일치 ✓
- claim-017: "凡有四端於我者 知皆擴而充之矣..." — 공손추편 상 2.6 원문과 일치 ✓

#### counterpoint 검증
17건 모두 구체적인 사상가명 + 저서명이 명시되어 있다. (순자/성악편, 고자/고자편, 한비자/난세편, 묵자/겸애, 양주/위아설, 장자 등) — 합격

### 4. keywords -- 합격

12건 전수 검증:

| id | term | definition 정확성 | related_claims 매핑 | source 정확성 |
|----|------|-------------------|---------------------|---------------|
| kw-001 | 성선설 | OK | [claim-001, claim-016] OK | OK |
| kw-002 | 사단 | OK | [claim-002, claim-017] OK | OK (공손추 2.6) |
| kw-003 | 인의예지 | OK | [claim-004] OK | OK |
| kw-004 | 호연지기 | OK | [claim-005, claim-012] OK | OK (공손추 2.2) |
| kw-005 | 왕도정치 | OK | [claim-006, claim-013] OK | OK |
| kw-006 | 역성혁명 | OK | [claim-007] OK | OK (양혜왕 하 1.8) |
| kw-007 | 항산항심 | OK | [claim-008, claim-013] OK | OK (양혜왕 1.7) |
| kw-008 | 의리지변 | OK | [claim-009] OK | OK (양혜왕 1.1) |
| kw-009 | 불인인지심 | OK | [claim-003, claim-002] OK | OK (공손추 2.6) |
| kw-010 | 대장부 | OK | [claim-011] OK | OK (등문공 하 3.2) |
| kw-011 | 민위귀 | OK | [claim-010] OK | OK (진심 하 7.14) |
| kw-012 | 양지양능 | OK | [claim-015] OK | OK (진심 7.15) |

소견: 정의, 관련 claims 매핑, 출처 모두 정확하다.

### 5. relations -- 조건부 합격

5건 검증:

| id | from → to | type | 방향 정확성 | 내용 정확성 | 참조 무결성 |
|----|-----------|------|------------|------------|------------|
| confucius→mencius | confucius → mencius | influenced | OK (공자가 맹자에게 영향) | OK | OK (confucius 존재) |
| mencius→xunzi | mencius → xunzi | criticized | **심각 이슈** | OK (내용 자체는 정확) | **보통 이슈** |
| mencius→gaozi | mencius → gaozi | criticized | **심각 이슈** | OK (내용 자체는 정확) | **보통 이슈** |
| mencius→zhuxi | mencius → zhuxi | influenced | OK (맹자가 주희에게 영향) | OK | **보통 이슈** |
| mencius→wangyangming | mencius → wangyangming | influenced | OK (맹자가 왕양명에게 영향) | OK | **보통 이슈** |

---

## 이슈 목록

### 심각 (3건)

**S-1. claim-011 work_id 오류**
- claim-011(대장부)의 `work_id`가 `mencius-jinxin`(진심편)으로 되어 있으나, 실제 출처는 등문공편(滕文公篇) 하 3.2이다. source_detail은 올바르게 "등문공편 하 3.2"로 기재되어 있어 work_id와 불일치.
- 수정: `work_id`를 `mencius-mencius`로 변경 (등문공편은 독립 works로 등록되어 있지 않으므로)

**S-2. relation mencius→xunzi 방향 오류**
- `from_thinker: mencius, to_thinker: xunzi, type: criticized` — "from이 to를 criticized" 규칙상 "맹자가 순자를 비판했다"는 의미가 된다. 그러나 description 내용은 **순자가 맹자의 성선설을 비판했다**는 것이다. 맹자(기원전 372~289)가 순자(기원전 313~238경)보다 선배이므로, 맹자가 순자를 직접 비판한 것이 아니라 순자가 맹자를 비판한 것이다.
- 수정: `from_thinker`를 `xunzi`, `to_thinker`를 `mencius`로 변경하거나, 양방향 논쟁으로 description을 수정

**S-3. relation mencius→gaozi 방향 오류**
- `from_thinker: mencius, to_thinker: gaozi, type: criticized` — "맹자가 고자를 비판했다"는 의미. description에서는 고자가 먼저 성무선악을 주장하고 맹자가 이를 논박한 것으로 기술되어 있다. 이 경우 양측이 상호 비판한 것이므로 단일 방향 표현이 부정확하다. 다만 맹자가 고자를 논박(criticized)했다는 해석도 가능하므로 방향 자체가 완전히 틀린 것은 아니나, description의 초점이 "고자가 맹자와 논쟁했다"로 시작하여 방향과 어긋난다.
- 수정 권장: description의 서술을 "맹자는 고자의 성무선악설을 비판했다"로 시작하도록 변경하여 from→to 방향과 일치시킴

### 보통 (2건)

**M-1. claim-004 출처 및 work_id 부정확**
- 원문 "仁義禮智 非由外鑠我也 我固有之也 弗思耳矣"는 **고자편(告子篇) 상 6.6**의 문장이다. 그러나 `work_id`는 `mencius-gongsunchou`(공손추편), source_detail의 첫 번째 출처는 "공손추편 상 2.6"으로 되어 있다.
- 수정: `work_id`를 `mencius-gaozi`로, source_detail을 "고자편(告子篇) 상 6.6"으로 변경

**M-2. relations의 참조 무결성 문제**
- mencius→xunzi, mencius→gaozi, mencius→zhuxi, mencius→wangyangming 관계에서 to_thinker(xunzi, gaozi, zhuxi, wangyangming)가 ethics-thinkers 인덱스에 존재하지 않는다. 해당 사상가들이 아직 입력되지 않은 상태이므로, 향후 해당 사상가 데이터 입력 시 참조 무결성이 확보될 것이다.
- 조치: 향후 해당 사상가 입력 태스크에서 자동 해결. 현재로서는 기록만 해둠.

### 경미 (2건)

**L-1. claim-006 복수 출처 표기**
- source_detail이 "양혜왕편 상 1.7, 공손추편 상 2.3"인데, 핵심 원문("以力假仁者覇...")은 공손추편 상 2.3에 해당한다. 양혜왕편 1.7은 왕도의 구체적 내용이 나오는 곳이므로 보조 출처로는 적절하나, 주 출처와 보조 출처의 구분이 없다.

**L-2. claim-004 source_detail의 진심편 참조**
- source_detail에 "진심편(盡心篇) 상 7.21"이 보조 출처로 기재되어 있다. 진심편 7.21은 "만물이 모두 나에게 갖추어져 있다(萬物皆備於我矣)"로, 인의예지 내재와 관련은 있으나 직접 출처는 아니다. 오해의 소지가 있으므로 삭제하거나 "참고" 표시 권장.

---

## 다음 제안

1. **심각 이슈 3건 즉시 수정**: claim-011 work_id 변경, relation mencius→xunzi 방향 수정, relation mencius→gaozi description 수정
2. **보통 이슈 2건 수정**: claim-004 work_id/source_detail 변경
3. 참조 무결성(M-2)은 순자·고자·주희·왕양명 데이터 입력 시 자동 해결
