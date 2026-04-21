# Coder Report — TASK-031

- Task: Ollama 클라이언트 (영어교사 프롬프트, 캐시 연동, idiom 어원 필수)
- Status: DONE
- Date: 2026-04-14

## 변경 파일

- `projects/abc-english/src/ollama_client.py` (신규)
- `projects/abc-english/config/settings.yaml` (llm.ollama 섹션 확장)
- `projects/abc-english/requirements.txt` (httpx>=0.27.0 추가)

## 구현 내용

### `src/ollama_client.py`

- Pydantic `LookupResult` 모델: `term / term_type / explanation_en / etymology(Optional) / examples[list[str]]`.
- Public API:
  - `async lookup_term(term, context, settings, es=None) -> dict`
  - `lookup_term_sync(term, context, settings, es=None)` — `asyncio.run` 래퍼
  - `async verify_ollama_model(settings) -> {"ok": bool, "warning"?: str}`
  - 보조: `build_system_prompt(settings, prompt_version)` / `build_user_prompt(term, context, settings, prompt_version)`

- 동작:
  1. `llm_cache.get_cached(term, model, prompt_version, es)` 먼저 조회 → hit이면 즉시 반환.
  2. Miss면 `httpx.AsyncClient(timeout=settings.llm.ollama.timeout_seconds or .timeout or 120)`로 `POST {host}/api/generate` 호출. 페이로드에 `format="json"`, `stream=False` 포함.
  3. 응답 JSON을 `_coerce_result`로 `LookupResult` 강제 변환 (term_type alias 보정, examples 문자열도 리스트화).
  4. **Idiom etymology 검증**: `term_type == "idiom"` 인데 etymology가 비어 있으면 프롬프트에 `IDIOM_EMPHASIS`(etymology is REQUIRED for idioms …)를 덧붙여 1회 재질의. 그래도 없으면 `etymology = "(not provided)"`로 채우고 `logger.warning`.
  5. 성공 응답을 `llm_cache.set_cached`로 캐시 후 dict 반환.

- Host 해석 순서: `settings.llm.ollama.host` → `.base_url` → `http://localhost:11434`.
- Timeout 해석 순서: `timeout_seconds` → `timeout` → 120s.
- Prompt 해석 순서: `settings.llm.ollama.prompts.v1.system` / `.user_template` → 내장 기본값.
- `verify_ollama_model`: `GET {host}/api/tags`. 모델 목록에 지정 모델 없거나 네트워크 실패 시 `{"ok": False, "warning": ...}` 반환(예외는 삼키고 경고 로그만). 짧은 이름(`foo`)이 `foo:latest` 식 태그와 매칭되는 경우도 허용.

### `config/settings.yaml`

기존 `llm.ollama` 섹션을 보존하면서 다음을 추가:
- `host: "http://localhost:11434"` (web UI 표준 키)
- `timeout_seconds: 120` (web lookup 기본)
- `prompt_version: "v1"`
- `prompts.v1.system` / `prompts.v1.user_template` (task 사양의 템플릿을 그대로 수록, JSON 중괄호는 `{{` `}}` 로 이스케이프하여 `str.format`과 호환)

기존 키(`base_url`, `timeout: 300`, `model: gemma4:e4b-ctx16384`, `options`)는 `llm_analyzer.py` 배치 호출이 계속 사용하므로 유지했다. 신규 클라이언트는 `host`/`timeout_seconds` 를 우선 참조한다.

### `requirements.txt`

- `httpx>=0.27.0` 추가 (LLM 섹션).

## 검증

```bash
# project root: projects/abc-english
python -m py_compile src/ollama_client.py
python -c "from src.ollama_client import lookup_term, verify_ollama_model, LookupResult"
python -c "import asyncio; from src.ollama_client import lookup_term_sync"
```

모두 통과. 추가로 `build_user_prompt("take the fall", "Will Pete take the fall?", settings)` 호출이 정상 렌더되고 `"idiom"` 규칙 문자열을 포함함을 확인.

실제 Ollama 호출은 환경 의존으로 스킵(서버 필요).

## 참고/결정 사항

- `settings.yaml`의 `model` 기본값은 기존 프로젝트 설정인 `gemma4:e4b-ctx16384`를 유지. 사양 예시의 `gemma4:e2b`는 모듈 상수 `DEFAULT_MODEL`에 기록(settings 누락 시 fallback).
- JSON 파싱 실패/모델 응답 누락은 `ValueError` 로 throw — 웹 API 레이어에서 500 처리하도록 위임.
- 캐시 저장은 `llm_cache.set_cached`의 best-effort 정책을 그대로 사용 (실패해도 상위에 전파하지 않음).
- Idiom 재질의까지 실패해도 호출자는 항상 dict를 받아본다 (`etymology == "(not provided)"`).

## 이슈/블로커

없음.
