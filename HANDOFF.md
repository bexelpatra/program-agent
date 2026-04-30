# Claude Coach — 핸드오프 문서

다른 세션에서 이 프로젝트를 이어서 진행할 때 이 문서 하나만 읽으면 100% 복원 가능하도록 작성됨.

## 사용자 목표 (원문)
> "claude를 보고 사용자의 특성 및 사용방법 기타 등등을 정리해서 보여주는 학습형 자료를 만들거야. 클로드 훅으로 사용자의 작업이 끝나면 ai 및 에이전트 활용 능력에 대해서 피드백을 주는거지. 사실 ai가 어떤 사고 과정을 거쳤는지 모르니까 프롬프터 짜고 활용하는데 어려웠거든."

→ **클로드 코드 / 에이전트 활용에 대한 메타인지 학습 웹 대시보드.**
사용자는 더 이상 의견을 묻지 말고 최선의 결정으로 실행해 달라고 했음.

## 작업 디렉토리
- Primary: `/home/jai/pa/temp` (이 worktree에서 작업)
- 클로드 트랜스크립트 원본: `/home/jai/.claude/projects/<프로젝트별>/<sessionId>.jsonl`
  - 21개 프로젝트, 약 24만 줄. 충분한 백필 데이터 존재.
- 클로드 설정: `/home/jai/.claude/settings.json` (전역), `settings.local.json` (프로젝트)

## 환경 정보 (검증됨)
- Python 3.11.3 @ `/home/jai/anaconda3/bin/python3`
- Node v24.14.0 @ nvm
- Claude Code 2.1.123
- OS: Linux, Shell: bash

## 트랜스크립트 JSONL 스키마 (검증됨)
한 줄 = 하나의 이벤트. 주요 type 분포 (한 세션 예시):
```
{'permission-mode': 113, 'file-history-snapshot': 94, 'user': 513,
 'attachment': 66, 'assistant': 829, 'last-prompt': 112, 'system': 74,
 'queue-operation': 4}
```

핵심 필드:
- `type`: `user` / `assistant` / `attachment` / `system` / 기타
- `timestamp`: ISO8601
- `sessionId`, `cwd`, `gitBranch`, `version`
- `isSidechain`: true 면 서브에이전트(Agent) 호출의 내부 흐름
- `message.content`:
  - user: 보통 문자열 (가끔 배열). 단, `tool_result`는 user 메시지의 content 배열에 들어옴
  - assistant: 배열 — 각 원소가 `{type:"thinking|text|tool_use", ...}`
- assistant 메시지의 `tool_use`: `{name, input, id}` 포함. **여러 tool_use가 한 메시지에 같이 있으면 병렬 호출**
- user 메시지에 `{type:"tool_result", tool_use_id, content, is_error}` 포함될 수 있음

## 설계 (확정)

### 파일 구조
```
/home/jai/pa/temp/
├── HANDOFF.md              ← 이 문서
├── analyzer.py             [TODO] 트랜스크립트 1개 → 세션 메트릭 JSON
├── ingest.py               [TODO] ~/.claude/projects 전체 백필
├── server.py               [TODO] http.server + /api/sessions
├── install.sh              [TODO] ~/.claude/settings.json에 Stop 훅 추가
├── data/
│   └── sessions.jsonl      [생성] 세션별 메트릭 누적
└── web/
    ├── index.html          [TODO] 대시보드
    ├── app.js              [TODO]
    └── style.css           [TODO]
```

### analyzer.py가 추출할 메트릭 (per session)
**기본**
- `session_id`, `cwd`, `git_branch`, `version`, `start_ts`, `end_ts`, `duration_sec`
- `user_turns`, `assistant_turns`

**프롬프트 품질**
- `first_prompt_chars`, `avg_prompt_chars`, `median_prompt_chars`
- `prompt_specificity`: 코드 토큰 비율 (백틱·경로·함수명 등)
- `correction_signals`: "no", "stop", "don't", "actually", "not that", "아니야", "다시", "잘못" 등 카운트

**툴 사용**
- `tool_calls_total`, `tool_calls_by_name`: {Bash:N, Read:N, ...}
- `parallel_tool_calls`: 한 assistant 메시지에 ≥2 tool_use 인 횟수
- `parallel_rate`: parallel / 전체 assistant 메시지 중 tool_use 포함된 것
- `subagent_invocations`: name=="Agent" tool_use 카운트
- `subagent_types`: 어떤 subagent_type을 썼는지 분포
- `plan_tool_used`: EnterPlanMode/ExitPlanMode/TodoWrite/TaskCreate 등

**효율/실패 시그널**
- `bash_failures`: tool_result.is_error=true 이고 도구가 Bash 인 것
- `edit_string_not_found`: tool_result content에 "string not found" 같은 에러
- `file_reread_count`: 같은 file_path 를 Read 로 N>1 번 읽은 횟수
- `redundant_search`: 비슷한 grep/find 반복

**사고 깊이**
- `thinking_chars_total`, `thinking_chars_avg_per_turn`
- `assistant_text_chars_total`

### 점수 산출 (Coach Score 0–100)
가중치 합산 — 5축 각 0–20점:
1. **Prompt clarity** (구체성, 평균 길이, 보정 빈도 적음)
2. **Tool efficiency** (병렬 비율, 실패율 낮음)
3. **Context economy** (서브에이전트 활용, 중복 read 적음)
4. **Planning** (Plan/TaskCreate 사용)
5. **Iteration health** (correction_signals 적고 세션이 길게 발산 안함)

세션별 점수 + 최근 N=10 이동 평균 트렌드.

### 피드백 규칙 엔진 (예시)
- `parallel_rate < 0.2` → "독립적인 read/grep을 병렬로 묶어보세요. 같은 메시지에 여러 tool_use를 두면 시간·토큰 절약됩니다."
- `subagent_invocations == 0 && total_reads > 30` → "코드베이스 탐색이 많네요. Explore 서브에이전트를 쓰면 메인 컨텍스트를 보호할 수 있어요."
- `edit_string_not_found > 3` → "Edit 실패가 잦습니다. old_string에 더 많은 주변 컨텍스트(3-5줄)를 포함해 보세요."
- `correction_signals / user_turns > 0.2` → "되돌리는 빈도가 높습니다. 첫 프롬프트에 제약·예시·기대 출력 형식을 한 번에 적어두면 왕복이 줄어요."
- `first_prompt_chars < 80` → "초기 프롬프트가 짧습니다. 상위 효과적 세션 평균은 250자+ 입니다."
- `file_reread_count > 5` → "동일 파일을 반복 read 했습니다. 줄 번호·심볼명을 미리 알려주면 한 번에 끝납니다."
- `bash_failures / total_bash > 0.15` → "Bash 실패율이 높습니다. 명령 실행 전 ls/which 등으로 사전 확인을 권장합니다."

### 웹 대시보드 섹션 (단일 HTML)
1. **헤더**: 사용자명, 총 세션, 총 시간, 현재 Coach Score
2. **5축 레이더 차트** (Chart.js CDN)
3. **트렌드 라인**: 최근 30 세션 점수
4. **툴 사용 도넛**: 전체 툴 분포
5. **세션 타임라인 테이블**: 시간순 — cwd, 점수, 주요 메트릭
6. **개인 맞춤 팁 카드들**: 위 규칙 엔진의 활성 팁 (우선순위 정렬)
7. **세션 드릴다운 모달**: 행 클릭 시 그 세션의 자세한 메트릭

스타일: 다크 테마, 모노스페이스 강조 부분, 한국어 라벨.

### 훅 설정 (Stop 이벤트)
`~/.claude/settings.json` 에 추가:
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "/home/jai/anaconda3/bin/python3 /home/jai/pa/temp/analyzer.py --hook"
          }
        ]
      }
    ]
  }
}
```
훅 입력은 stdin JSON: `{session_id, transcript_path, cwd, hook_event_name}` 등.
`analyzer.py --hook` 모드에서:
1. stdin 파싱 → transcript_path 획득
2. 메트릭 추출 → `/home/jai/pa/temp/data/sessions.jsonl` 에 append (이미 같은 session_id 가 있으면 갱신)
3. `exit 0` (블로킹 금지)

### 서버
`python3 /home/jai/pa/temp/server.py [port=8765]`:
- `/` → web/index.html
- `/app.js`, `/style.css` → 정적
- `/api/sessions` → sessions.jsonl 전체 JSON 배열로 반환
- `/api/session/<id>` → 단일 세션 상세

## 현재 진행 상태
- [x] 환경 조사 완료
- [x] 트랜스크립트 스키마 분석 완료
- [x] 디렉토리 (`web/`, `data/`) 생성됨
- [x] 설계 확정 (이 문서)
- [ ] **analyzer.py 작성** ← 다음 작업 시작점
- [ ] ingest.py 작성
- [ ] 백필 실행 (`python3 ingest.py`)
- [ ] web/* 작성 (Chart.js CDN 사용)
- [ ] server.py 작성
- [ ] install.sh 작성
- [ ] ~/.claude/settings.json 에 Stop 훅 등록
- [ ] 서버 띄워서 브라우저에서 동작 확인

## 다음 세션 시작 시 할 일
1. 이 HANDOFF.md 를 Read 로 다시 읽기
2. `/home/jai/.claude/projects/-home-jai-pa-temp/memory/` 도 확인 (project 메모리 저장됨)
3. TaskList 로 잔여 태스크 확인
4. analyzer.py 부터 작성 시작
5. 작은 한 트랜스크립트로 단위 테스트 후 ingest.py 로 전체 백필
6. 백필 결과를 보면서 웹 UI 작성 (실데이터 보면서 만드는게 좋음)

## 디자인 원칙 (잊지 말 것)
- 빌드 스텝 없음. 순수 HTML/JS/CSS + Chart.js CDN.
- Python 표준 라이브러리만. pip install 금지.
- 훅은 비차단(빠르고 조용히 실패).
- 한국어 UI.
- "AI 사고 과정 가시화"가 핵심 가치 — thinking 토큰량, 툴 체이닝 패턴, 정정 빈도 등을 보여줘서 사용자가 자기 프롬프트가 클로드를 어떻게 움직였는지 이해하게 함.
