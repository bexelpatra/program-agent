---
agent: coder
task_id: TASK-030
status: DONE
timestamp: 2026-04-14T11:20:00Z
---

# 결과 요약

`abc-user-vocabulary`, `abc-llm-cache` 두 ES 인덱스 매핑 및 Pydantic 모델
(`UserVocabularyEntry`, `LlmCacheEntry`, `SourceEpisodeRef`)을 추가하고,
웹 UI에서 사용할 CRUD 헬퍼 모듈(`notebook_store.py`, `llm_cache.py`)을
새로 작성했다. `INDEX_MAPPINGS`에 두 인덱스를 등록하여 기존
`create_indices()` / `delete_indices()` 경로가 변경 없이 그대로
두 신규 인덱스를 관리한다. `settings.yaml`의 `elasticsearch.indices`
맵에도 `user_vocabulary`, `llm_cache` 키를 추가했다.

검증:
- `python -m py_compile src/models.py src/notebook_store.py src/llm_cache.py` 통과.
- `python -c "from src.models import UserVocabularyEntry, LlmCacheEntry"` 성공.
- `python -m src.cli init-indices` 실행 결과 총 6개 인덱스(`abc-episodes`,
  `abc-sentences`, `abc-vocabulary`, `abc-expressions`, `abc-user-vocabulary`,
  `abc-llm-cache`) 모두 PUT 200으로 생성 확인.

# 변경된 파일

- `projects/abc-english/config/settings.yaml`
  - `elasticsearch.indices`에 `user_vocabulary: abc-user-vocabulary`,
    `llm_cache: abc-llm-cache` 추가.
- `projects/abc-english/src/models.py`
  - `SourceEpisodeRef`, `UserVocabularyEntry`, `LlmCacheEntry` Pydantic 모델.
  - `USER_VOCABULARY_MAPPING` (lowercase normalizer + nested source_episodes),
    `LLM_CACHE_MAPPING` 추가.
  - `INDEX_MAPPINGS`에 `user_vocabulary`, `llm_cache` 등록.
- `projects/abc-english/src/notebook_store.py` (신규)
  - `normalize_term`, `upsert_notebook_entry` (added_count++, source_episodes
    append with max 20, first/last_added 관리), `get_notebook_entry`,
    `list_notebook` (filter/sort), `mark_viewed` (painless script),
    `delete_notebook_entry`.
- `projects/abc-english/src/llm_cache.py` (신규)
  - `make_cache_key` (sha1 of normalized term|model|prompt_version),
    `get_cached`, `set_cached`. 예외는 best-effort로 삼켜 캐시 장애가
    상위 흐름을 막지 않도록 처리.

# 이슈/블로커

없음.

# 다음 제안

- TASK-031(예상): FastAPI 앱 스캐폴딩 — `web/app.py`, `web/api/` 라우터
  스텁, Jinja 템플릿 베이스. `notebook_store`/`llm_cache`를 DI로 주입하도록
  `Depends(get_client)` 래퍼를 추가하는 형태가 자연스럽다.
- `upsert_notebook_entry`는 read-modify-write 패턴이므로 동시성 이슈가
  중요해지면 `if_seq_no`/`if_primary_term` 기반 낙관적 락이나 painless
  script upsert로 재작성 고려.
- `llm_cache.set_cached`가 실패를 무시하므로, 운영 시에는 최소한
  디버그 레벨 로깅을 붙이는 것이 이후 관측에 유리하다.
