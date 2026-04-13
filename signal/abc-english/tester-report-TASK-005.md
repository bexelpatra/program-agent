# Tester Report — TASK-005

## 태스크 정보
- Task ID: TASK-005
- Title: Collector 테스트
- 대상 파일: `projects/abc-english/src/collector.py`
- 테스트 파일: `projects/abc-english/tests/test_collector.py`

## 결과: DONE

## 테스트 실행 결과

```
48 passed in 0.35s
```

- 전체: 48개
- 통과: 48개
- 실패: 0개

## 테스트 커버리지 상세

| 클래스 | 테스트 수 | 대상 함수/로직 |
|--------|-----------|----------------|
| TestExtractNextData | 3 | `_extract_next_data` — 정상 파싱, 태그 없음, 빈 스크립트 |
| TestExtractItemsFromNextData | 5 | `_extract_items_from_next_data` — 3가지 JSON 경로, 빈 dict, 빈 리스트 |
| TestExtractEpisodeId | 5 | `_extract_episode_id` — id/episodeId 키, URL 파싱, None 반환, 정수 ID |
| TestBuildEpisodeUrl | 4 | `_build_episode_url` — 절대/상대 URL, slug+id, 빈 item |
| TestExtractAudioUrl | 3 | `_extract_audio_url` — 직접 키, nested media, 없는 경우 |
| TestDeepGet | 3 | `_deep_get` — camelCase, snake_case 폴백, 기본값 |
| TestRequestWithRetry | 3 | `_request_with_retry` — 성공, 재시도 후 성공, 전부 실패 |
| TestFetchEpisodeList | 3 | `fetch_episode_list` — 단일 페이지, 중복 제거, 빈 첫 페이지 |
| TestFetchEpisodeDetail | 3 | `fetch_episode_detail` — transcript 있음/없음, URL 폴백 ID |
| TestParseTranscript | 5 | `parse_transcript` — 정상, 없음, 빈 텍스트, 여러 문단, 공백 정규화 |
| TestSaveTranscript | 2 | `save_transcript` — 파일 생성, 덮어쓰기 |
| TestDownloadMp3 | 4 | `download_mp3` — 성공, 중복 스킵, 빈 URL, 네트워크 오류 정리 |
| TestCollectAll | 5 | `collect_all` — 전체 파이프라인(transcript 있음), transcript 없음 스킵, 상세 실패 폴백, URL 없음 스킵, 빈 목록 |

## 테스트 방법
- HTTP 요청: `unittest.mock.patch`로 mock 처리 (실제 네트워크 호출 없음)
- 파일 I/O: `tmp_path` fixture + `_patch_project_root` context manager로 프로젝트 루트를 tmp 디렉토리로 리다이렉트
- `time.sleep`: mock 처리하여 테스트 지연 없음

## 이슈/블로커
- 없음
