# Tester Report — TASK-009

## 태스크 정보
- Task ID: TASK-009
- Title: Transcriber + Comparator 테스트
- Status: **DONE**
- 실행 일시: 2026-04-13

## 테스트 결과 요약

| 테스트 파일 | 테스트 수 | 통과 | 실패 | 에러 |
|-------------|-----------|------|------|------|
| tests/test_transcriber.py | 19 | 19 | 0 | 0 |
| tests/test_comparator.py | 33 | 33 | 0 | 0 |
| **합계** | **52** | **52** | **0** | **0** |

## 테스트 상세

### test_transcriber.py (19 tests)

**TestLoadModel (4)**
- 정상 로딩 (settings에서 model/device 읽기)
- 싱글톤 캐싱 동작 (동일 모델명이면 재로딩 안 함)
- 모델명 변경 시 재로딩
- whisper.model 미설정 시 기본값 "base" 사용

**TestTranscribeAudio (5)**
- 정상 변환 결과 구조 (full_text, segments)
- 빈/공백 세그먼트 필터링
- 타임스탬프 round(2) 처리
- 빈 segments 처리
- language="en" 파라미터 전달 확인

**TestSaveWhisperTranscript (3)**
- JSON 파일 생성 및 내용 검증
- 디렉토리 자동 생성
- 기존 파일 덮어쓰기

**TestTranscribeEpisode (3)**
- 정상 플로우 (모델 로딩 → 변환 → 저장)
- 기존 transcript 존재 시 skip
- 오디오 파일 없을 때 FileNotFoundError

**TestTranscribeAll (4)**
- 배치 처리 (done + skipped 혼합)
- 오디오 없는 에피소드 error 카운팅
- settings=None 시 load_settings() 호출 확인
- 빈 리스트 처리

### test_comparator.py (33 tests)

**TestCalculateWer (10)**
- 동일 텍스트 (WER=0.0)
- 완전히 다른 텍스트 (WER=1.0)
- 양쪽 빈 문자열 (0.0)
- 참조 빈 + 가설 있음 (1.0)
- 가설 빈 + 참조 있음 (1.0)
- 구두점 차이 무시
- 대소문자 무시
- 부분 일치 (0.5)
- insertion 케이스
- deletion 케이스

**TestCalculateListeningDifficulty (7)**
- easy (0.0~0.05)
- medium (0.06~0.15)
- hard (0.16~0.30)
- very_hard (0.31+)
- easy/medium 경계값
- medium/hard 경계값
- hard/very_hard 경계값

**TestCompareSentences (7)**
- 정상 매칭 (1:1 대응)
- 세그먼트 부족 시 남은 문장 WER=1.0
- 빈 공식 문장 리스트
- 빈 세그먼트 리스트
- 양쪽 빈 리스트
- 마지막 문장이 남은 세그먼트 모두 소비
- start_time/end_time 추출

**TestCompareEpisode (6)**
- 정상 비교 (JSON 로드 → Sentence 모델 반환)
- 공식 transcript 없을 때 FileNotFoundError
- Whisper transcript 없을 때 FileNotFoundError
- 평균 WER 계산
- 빈 문장 리스트 처리
- settings=None 시 load_settings() 호출 확인

**TestCompareAll (3)**
- 배치 처리 (done + skipped 혼합)
- 빈 리스트 처리
- settings=None 시 load_settings() 호출 확인

## 특이사항
- whisper 패키지가 테스트 환경에 미설치 → `sys.modules.setdefault("whisper", MagicMock())`로 모듈 레벨 mock 처리
- transcriber의 _PROJECT_ROOT 패턴: `_patch_project_root(tmp_path)` 컨텍스트 매니저로 Path 서브클래스 사용
- comparator의 _PROJECT_ROOT 패턴: `patch.object(comparator_module, "_PROJECT_ROOT", tmp_path)`로 직접 패치
- 싱글톤 캐시(`_model`, `_model_name`)는 setup_method/teardown_method에서 리셋

## 이슈/블로커
없음.
