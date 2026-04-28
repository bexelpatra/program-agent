# Coder Report — TASK-007

## 태스크
- ID: TASK-007
- Title: Transcriber 구현 - Whisper 연동 (모델 선택, 타임스탬프 추출, 문장 분리)

## 상태: DONE

## 작업 내용

`projects/abc-english/src/transcriber.py`를 신규 작성하였다.

### 구현된 함수

| 함수 | 설명 |
|------|------|
| `load_model(settings)` | settings.yaml의 whisper 섹션에서 모델명/디바이스를 읽어 Whisper 모델 로딩. 모듈 수준 싱글톤으로 캐싱. |
| `transcribe_audio(audio_path, model)` | 단일 MP3 파일을 Whisper로 변환. segments(text, start, end)와 full_text 반환. |
| `save_whisper_transcript(episode_id, result, settings)` | 변환 결과를 `data/transcripts/{episode_id}_whisper.json`으로 저장. |
| `transcribe_episode(episode_id, settings)` | 단건 파이프라인: 모델 로딩 → MP3 탐색 → 변환 → JSON 저장. 이미 존재하면 skip. |
| `transcribe_all(episode_ids, settings)` | 배치 처리: 전체 에피소드 순회. skip/done/failed 카운트 로깅. |

### 주요 설계 결정

1. **싱글톤 모델**: `_model`, `_model_name` 모듈 변수로 캐싱. 모델명이 바뀌면 재로딩.
2. **중복 방지**: `_whisper_transcript_exists()`로 JSON 파일 존재 여부 확인 후 skip.
3. **설정 읽기**: `settings.yaml`의 `whisper.model`, `whisper.language`, `whisper.device` 사용.
4. **JSON 출력 형식**: `{"episode_id": "...", "segments": [{"text": "...", "start": 0.0, "end": 5.2}], "full_text": "..."}` — architecture.md 스펙 준수.
5. **에러 처리**: `transcribe_all`에서 개별 에피소드 실패 시 error 필드 포함하고 계속 진행.
6. **경로 해석**: collector.py와 동일한 패턴 (`Path(__file__).resolve().parent.parent` 기준 상대 경로).

## 생성/수정 파일
- `projects/abc-english/src/transcriber.py` (신규)

## 이슈/블로커
- 없음
