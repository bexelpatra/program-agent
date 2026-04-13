# Coder Report: TASK-059

## 상태: DONE

## 태스크
- Task ID: TASK-059
- Title: 맹자 데이터 입력 (ES 직접)

## 작업 내용

### 1. 스크립트 작성
- 파일: `projects/ethics-study/scripts/insert_mencius.py`
- `insert_confucius.py`의 패턴을 따름 (동양윤리 동일 구조)

### 2. ES 입력 결과

| 항목 | 건수 | 상세 |
|------|------|------|
| field | 1건 | eastern_ethics (이미 존재, 재사용) |
| thinker | 1건 | mencius (맹자, 기원전 372~289, 중국 전국시대) |
| works | 4건 | 맹자(전체), 공손추편, 고자편, 진심편 |
| claims | 17건 | 아래 목록 참조 |
| keywords | 12건 | 아래 목록 참조 |
| relations | 4건 | 아래 목록 참조 (confucius→mencius는 기존 등록분) |

### 3. Claims 목록 (17건)
| ID | 주제 | work_id |
|----|------|---------|
| mencius-claim-001 | 성선설(性善說) | mencius-gaozi |
| mencius-claim-002 | 사단(四端) | mencius-gongsunchou |
| mencius-claim-003 | 불인인지심(不忍人之心) | mencius-gongsunchou |
| mencius-claim-004 | 인의예지(仁義禮智) 내재 | mencius-gongsunchou |
| mencius-claim-005 | 호연지기(浩然之氣) | mencius-gongsunchou |
| mencius-claim-006 | 왕도정치(王道政治) | mencius-mencius |
| mencius-claim-007 | 역성혁명(易姓革命) | mencius-mencius |
| mencius-claim-008 | 항산항심(恒産恒心) | mencius-mencius |
| mencius-claim-009 | 의리지변(義利之辨) | mencius-mencius |
| mencius-claim-010 | 민본(民爲貴) | mencius-jinxin |
| mencius-claim-011 | 대장부(大丈夫) | mencius-jinxin |
| mencius-claim-012 | 양기/부동심(不動心) | mencius-gongsunchou |
| mencius-claim-013 | 인정(仁政) 구체적 내용 | mencius-mencius |
| mencius-claim-014 | 천인합일(盡心知性知天) | mencius-jinxin |
| mencius-claim-015 | 양지양능(良知良能) | mencius-jinxin |
| mencius-claim-016 | 우산지목(牛山之木) 비유 | mencius-gaozi |
| mencius-claim-017 | 확충(擴充) | mencius-gongsunchou |

### 4. Keywords 목록 (12건)
성선설, 사단, 인의예지, 호연지기, 왕도정치, 역성혁명, 항산항심, 의리지변, 불인인지심, 대장부, 민위귀, 양지양능

### 5. Relations 목록 (4건, 신규 등록분)
- mencius --[criticized]--> xunzi (성선설 vs 성악설)
- mencius --[criticized]--> gaozi (성선설 vs 성무선악)
- mencius --[influenced]--> zhuxi (사서 체계, 성리학)
- mencius --[influenced]--> wangyangming (양지양능 → 치양지)
- (기존) confucius --[influenced]--> mencius (공자 → 맹자 계승, insert_confucius.py에서 등록)

### 6. 필수 필드 검증
- 모든 17건 claim에 argument + counterpoint + original_text + original_text_ko 포함: OK
- counterpoint: 모두 특정 사상가+저서 근거 포함 (순자 성악설, 고자 성무선악, 한비자, 노자, 묵자, 장자 등)
- original_text: 맹자 원전 한문 원문 직접 인용
- verified: 모두 false (Tester 검증 대기)

## 비고
- 중복 relation(relation-mencius-confucius) 발견하여 삭제함. confucius→mencius 관계는 insert_confucius.py에서 이미 relation-confucius-mencius로 등록되어 있었음.
- verify_data()에 index refresh 추가하여 입력 직후 검증이 정확히 동작하도록 개선함.
