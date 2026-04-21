# Coder Report — TASK-151

## 태스크
- ID: TASK-151
- Title: 하이트 데이터 입력 (ES 직접) — 도덕심리학, claims 8+

## 상태
DONE

## 작업 내용

### 작성 파일
- `projects/ethics-study/scripts/insert_haidt.py`

### ES 입력 결과

| 인덱스 | 건수 | 결과 |
|--------|------|------|
| ethics-thinkers | 1 | created |
| ethics-works | 3 | created |
| ethics-claims | 10 | created |
| ethics-keywords | 10 | created |
| ethics-relations | 4 | created |

### 입력 데이터 요약

#### 사상가
- id: `haidt`, 조너선 하이트(Jonathan Haidt), 1963~, field: moral_development, era: 현대

#### 저서
1. `haidt-righteous-mind` — 바른 마음(The Righteous Mind, 2012)
2. `haidt-happiness-hypothesis` — 행복의 가설(The Happiness Hypothesis, 2006)
3. `haidt-coddling-of-american-mind` — 과보호하는 미국의 정신(2018, with Lukianoff)

#### 주장 (10개)
1. `haidt-claim-001`: 사회적 직관주의 모델 — 직관 우선, 추론은 사후 정당화
2. `haidt-claim-002`: 코끼리와 기수 비유 — 직관(코끼리)이 이끌고 추론(기수)이 따름
3. `haidt-claim-003`: 도덕기반이론 — 6가지 도덕 기반 (배려/피해, 공정/속임, 충성/배신, 권위/전복, 신성/타락, 자유/억압)
4. `haidt-claim-004`: 배려/피해(Care/Harm) 기반 상세
5. `haidt-claim-005`: 콜버그·피아제 합리주의 비판
6. `haidt-claim-006`: 도덕성의 선천적 기초(Nativism) — 진화적 준비성
7. `haidt-claim-007`: WEIRD 편향 비판 — 서양 도덕철학의 문화 편향
8. `haidt-claim-008`: 진보와 보수의 도덕 기반 차이
9. `haidt-claim-009`: 도덕은 집단 결속을 위해 진화(Hive Hypothesis)
10. `haidt-claim-010`: 도덕은 미뢰(taste bud)와 같다 — 보편성과 다양성

#### 키워드 (10개)
- 사회적 직관주의 모델, 도덕기반이론, 코끼리와 기수, 도덕적 무성어화, WEIRD 편향,
  배려/피해, 공정/속임, 충성/배신, 권위/전복, 신성/타락

#### 관계 (4개)
- `kohlberg-criticized-haidt`: 콜버그 → 하이트 (비판적 계승)
- `hume-influenced-haidt`: 흄 → 하이트 (감정주의 영향)
- `piaget-criticized-haidt`: 피아제 → 하이트 (비판 받음)
- `haidt-criticized-kohlberg`: 하이트 → 콜버그 (직접 비판)

## 완료 조건 확인
- [x] `projects/ethics-study/scripts/insert_haidt.py` 작성
- [x] 스크립트 실행하여 ES 적재 완료 (전 항목 `created`)
- [x] claims 8개 이상 (10개 입력)
- [x] 6가지 도덕 기반 모두 포함
- [x] 관계 3~4개 입력 (4개)
- [x] 분야(moral_development) 존재 확인

## 비고
- 분야(moral_development)는 이미 존재하여 별도 생성 불필요
- `haidt-claim-003`에 6가지 도덕 기반 전체를 통합 정리하고, `haidt-claim-004`로 배려/피해를 상세화
- 자유/억압(Liberty/Oppression) 기반은 6번째로 추가된 기반으로, keywords 인덱스 항목 추가는 다음 확장 시 고려 가능
