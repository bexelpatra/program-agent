# Coder Report: TASK-062

## 태스크
- **ID**: TASK-062
- **Title**: 순자 데이터 입력 (ES 직접)
- **Status**: DONE

## 작업 결과

### 생성된 파일
- `projects/ethics-study/scripts/insert_xunzi.py`

### ES 입력 결과

| 항목 | 건수 | 비고 |
|------|------|------|
| field | 1 | eastern_ethics (이미 존재) |
| thinker | 1 | xunzi (순자, 荀子) |
| works | 4 | 순자, 성악편, 예론편, 천론편 |
| claims | 11 | 성악설, 화성기위, 예론, 천론, 제천이용, 명분론, 교육론, 군자소인, 예법병용, 심론, 정명론 |
| keywords | 10 | 성악설, 화성기위, 예, 위, 천인지분, 제천명이용지, 적, 대청명, 허일이정, 약정속성 |
| relations | 5 | 아래 상세 |

### Relations 상세

| ID | 방향 | 상태 |
|----|------|------|
| relation-confucius-xunzi | confucius --[influenced]--> xunzi | 기존 (skip) |
| relation-xunzi-mencius-debate | xunzi --[criticized]--> mencius | 기존 (skip) |
| relation-xunzi-hanfeizi | xunzi --[influenced]--> hanfeizi | 신규 |
| relation-xunzi-lisi | xunzi --[influenced]--> lisi | 신규 |
| relation-xunzi-dongzhongshu | xunzi --[influenced]--> dongzhongshu | 신규 |

### 중복 처리
- `relation-confucius-xunzi` (confucius→xunzi influenced): 기존 존재 확인, skip
- `relation-xunzi-mencius-debate` (xunzi→mencius criticized): 기존 존재 확인, skip
- 초기에 `relation-mencius-xunzi-debate` (mencius→xunzi criticized)를 잘못 생성했으나, 방향 규칙(from이 to를 [type]한 것)에 따라 부정확하므로 삭제 처리함

### 필수 필드 확인
- 모든 claim(11건)에 argument, counterpoint, original_text, original_text_ko 포함: OK
- 모든 claim의 verified: false

## 이슈/블로커
- 없음
