# Coder Report — TASK-080

## 태스크
- Task ID: TASK-080
- Title: 이이(율곡) 데이터 입력 (ES 직접)

## 상태
DONE

## 작업 내용

### 1. 사전 확인
- yiyulgok ID 기존 relations 확인: `relation-zhuxi-yiyulgok`, `relation-yihwang-yiyulgok-debate` 2건 확인
- yihwang 데이터 패턴(thinker, works, claims) 참조하여 스키마 파악

### 2. 입력 데이터 요약

#### Thinker (1건)
- ID: `yiyulgok`
- 이름: 이이 (李珥, 율곡) / Yi I (Yulgok)
- 분야: eastern_ethics, 조선, 1536~1584
- background: 강릉 오죽헌 출생, 신사임당, 구도장원공(九度壯元公), 기호학파 종조
- core_philosophy: 기발이승일도설, 이통기국, 이기지묘, 교기질, 경장론
- keywords: 12개

#### Works (4건)
| ID | 제목 | 연도 |
|----|------|------|
| yiyulgok-seonghak-jipyo | 성학집요(聖學輯要) | 1575 |
| yiyulgok-gyeongmong-yogyeol | 격몽요결(擊蒙要訣) | 1577 |
| yiyulgok-yulgok-jeonseo | 율곡전서(栗谷全書) | null |
| yiyulgok-maneon-bongsa | 만언봉사(萬言封事) | 1574 |

#### Claims (12건)
| ID | 핵심 주장 |
|----|-----------|
| yiyulgok-claim-001 | 기발이승일도설(氣發理乘一途說) — 발하는 것은 오직 기 |
| yiyulgok-claim-002 | 이통기국(理通氣局) — 이는 통하고 기는 국한 |
| yiyulgok-claim-003 | 이기지묘(理氣之妙) — 비일비이(非一非二) |
| yiyulgok-claim-004 | 이(理)의 무위(無爲) — 이는 스스로 작용 못 함 |
| yiyulgok-claim-005 | 기질변화론 — 교기질(矯氣質)로 본연지성 회복 |
| yiyulgok-claim-006 | 성학집요 수기치인(修己治人) 체계 |
| yiyulgok-claim-007 | 경장론(更張論) — 시대에 맞는 제도 개혁 |
| yiyulgok-claim-008 | 입지론(立志論) — 학문의 출발점 |
| yiyulgok-claim-009 | 이기불상리(理氣不相離) — 이기 불가분 |
| yiyulgok-claim-010 | 격물치지(格物致知) — 사물 이치 궁구 |
| yiyulgok-claim-011 | 인심도심론(人心道心論) — 모두 기발, 도심이 인심 주재 |
| yiyulgok-claim-012 | 십만양병설(十萬養兵說) — 국방 대비 |

각 claim 공통 필드: claim, original_text(한문), original_text_ko, explanation, argument, counterpoint(이황·왕양명·법가 등 구체적 사상가+저서 명시), context, source_detail, work_id, verified: false, verification_log: []

#### Keywords (12건)
- kw-yiyulgok-gibal-iseung-ildo: 기발이승일도설(氣發理乘一途說)
- kw-yiyulgok-itong-giguk: 이통기국(理通氣局)
- kw-yiyulgok-igi-jimyo: 이기지묘(理氣之妙)
- kw-yiyulgok-gyeongjang: 경장론(更張論)
- kw-yiyulgok-ibji: 입지(立志)
- kw-yiyulgok-gyogijil: 교기질(矯氣質)
- kw-yiyulgok-giho-hakpa: 기호학파(畿湖學派)
- kw-yiyulgok-insim-dosim: 인심도심(人心道心)
- kw-yiyulgok-igi-bulsangni: 이기불상리(理氣不相離)
- kw-yiyulgok-seonghak-jipyo: 성학집요(聖學輯要)
- kw-yiyulgok-gyeongmong-yogyeol: 격몽요결(擊蒙要訣)
- kw-yiyulgok-simmunjeong: 심성론(心性論) — 이이의 입장

#### Relations (기존 확인)
- `relation-zhuxi-yiyulgok`: zhuxi --(influenced)--> yiyulgok ✓ (이미 존재)
- `relation-yihwang-yiyulgok-debate`: yihwang --(influenced)--> yiyulgok ✓ (이미 존재)

### 3. 이황(퇴계)와의 대비 반영
모든 주요 claim의 counterpoint에 이황(퇴계)의 이기호발설·이기불상잡·이발기수 등을 명시적으로 비교·대비하여 사단칠정 논쟁의 맥락이 자연스럽게 반영됨.

## 최종 확인 (ES 조회)
- ethics-thinkers/yiyulgok: ✓ 1건
- ethics-works (yiyulgok): ✓ 4건
- ethics-claims (yiyulgok): ✓ 12건
- ethics-keywords (yiyulgok): ✓ 12건
- ethics-relations (yiyulgok 관련): ✓ 2건 (기존)

## 이슈/블로커
없음
