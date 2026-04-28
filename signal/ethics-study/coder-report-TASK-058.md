---
agent: coder
task_id: TASK-058
status: DONE
timestamp: 2026-04-13T12:00:00
---

## 결과 요약
공자 데이터 이슈 5건 중 4건 수정 완료, 1건(경미: to_thinker 미등록)은 현재 태스크 범위 외로 기록만 남김. 전체 17건 claims에 verified:true 및 verification_log 추가 완료.

## 수정 내역

### 1. [심각] confucius-claim-010 — 출처 및 내용 수정
- **source_detail**: "양화편(陽貨篇) 17.6, 이인편(里仁篇) 4.2" → "이인편(里仁篇) 4.3, 자한편(子罕篇) 9.29"
  - 이인편 4.2→4.3: "唯仁者能好人 能惡人"의 정확한 편 번호
  - 양화편 17.6→자한편 9.29: "知者不惑 仁者不憂 勇者不懼"의 정확한 편 번호
- **claim 문구 수정**: 마치 공자가 인의예지를 체계적으로 제시한 것처럼 보이던 표현을 "공자는 개별적으로 논했으며, 사단(四端)으로 체계화한 것은 맹자"임을 명시
- **context 수정**: 맹자 체계화 사실을 보다 명확히 기술

### 2. [보통] confucius-claim-006 — 번역 수정
- **original_text**: "백성들이 이를 실천한 지 오래되었다" → "백성들 중에 이를 실천하는 이가 드문 지 오래되었다"
- '鮮(드물 선)' 의미가 누락되어 있던 것을 수정, original_text_ko와 일치시킴

### 3. [보통] confucius-claim-014 — counterpoint 출처 수정
- **counterpoint 내 묵자 출처**: "겸애편" → "비유편(非儒篇)"
- 유가 비판은 비유편이 직접적 출처이므로 수정

### 4. [경미] relation confucius→laozi — 방향 수정
- **from_thinker/to_thinker 교체**: confucius→laozi를 laozi→confucius로 변경
- **doc ID 변경**: relation-confucius-laozi → relation-laozi-confucius (신규 생성 후 구 문서 삭제)
- type은 "criticized" 유지 (노자가 공자를 비판한 내용이 주이므로 방향 규칙과 일치)

### 5. [경미] to_thinker 미등록 가능성 — 미조치
- mencius, xunzi, zhuxi, wangyangming, laozi가 ethics-thinkers에 미등록일 수 있다는 지적
- 각 사상가 데이터 입력 태스크에서 처리될 사안이므로 본 태스크에서는 미조치

## verified 처리
- 전체 17건 confucius claims (confucius-claim-001 ~ confucius-claim-017)에 verified: true 설정
- 수정된 3건(006, 010, 014): 수정 내용이 포함된 verification_log 추가
- 정확 판정 14건: "정확 판정, 이슈 없음" verification_log 추가

## 변경된 ES 문서
- ethics-claims: confucius-claim-006, confucius-claim-010, confucius-claim-014 (수정), 나머지 14건 (verified만 추가)
- ethics-relations: relation-confucius-laozi 삭제, relation-laozi-confucius 생성
