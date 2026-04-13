---
agent: coder
task_id: TASK-004
status: DONE
timestamp: 2026-04-13T14:00:00
---

## 결과 요약
collector.py에 공식 transcript 파싱 + MP3 다운로드 기능을 추가했다. 기존 구조를 유지하면서 3개 함수(parse_transcript, save_transcript, download_mp3)를 신규 작성하고, fetch_episode_detail과 collect_all을 수정하여 전체 파이프라인을 통합했다.

### 신규 함수
1. **parse_transcript(html_content) -> dict**: div#transcript에서 텍스트 추출, HTML 태그 제거, 공백 정규화, 문장 단위 분리 (.!? 기준)
2. **save_transcript(episode_id, transcript_data, settings) -> str**: data/transcripts/{episode_id}_official.json으로 저장 (episode_id, sentences, full_text 포함)
3. **download_mp3(episode_id, audio_url, settings) -> str**: data/audio/{episode_id}.mp3로 저장, tqdm 진행률 표시, 중복 방지(파일 존재 시 skip), 스트리밍 다운로드(8KB 청크), 임시파일(.mp3.tmp) 사용 후 rename

### 수정 함수
4. **fetch_episode_detail**: `_html` 키로 원본 HTML 반환 추가 (이중 요청 방지)
5. **collect_all**: has_transcript=True인 에피소드에 대해 transcript 파싱 → JSON 저장 → MP3 다운로드 단계를 통합. 각 단계 예외 시 로그 후 계속 진행.

### 추가 import
- os, re, Path(pathlib), tqdm - 모두 requirements.txt에 이미 포함

## 변경된 파일
- projects/abc-english/src/collector.py (수정)

## 이슈/블로커
없음

## 다음 제안
- Tester에게 parse_transcript, save_transcript, download_mp3의 단위 테스트 작성을 권장 (HTML fixture 기반 transcript 파싱 검증, 중복 방지 로직 검증, 스트리밍 다운로드 mock 검증)
