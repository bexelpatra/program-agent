# Project Registry

각 프로젝트는 `project/{id}` 브랜치와 `/home/jai/pa/{id}` worktree 로 운영된다. archive 개념은 사용하지 않는다 — 더 이상 작업 안 하는 프로젝트는 단순히 worktree 를 만들지 않으면 된다.

| ID | Name | Branch | Worktree | Created |
|----|------|--------|----------|---------|
| ethics-study | 윤리 임용시험 학습 가이드 | `project/ethics-study` | `/home/jai/pa/ethics-study` | 2026-03-25 |
| starcraft-record | 스타크래프트 전적 관리 도구 | `project/starcraft-record` | `/home/jai/pa/starcraft-record` | 2026-04-13 |
| web-automation | 웹 업무 자동화 (티스토리, 야놀자) | `project/web-automation` | `/home/jai/pa/web-automation` | 2026-04-13 |
| abc-english | ABC News Daily 영어 학습 시스템 | `project/abc-english` | `/home/jai/pa/abc-english` | 2026-04-13 |
| stock-backtest | 시계열 기반 자산배분·계절성 백테스팅 플랫폼 | `project/stock-backtest` | `/home/jai/pa/stock-backtest` | 2026-04-14 |
| abc-english-app | ABC English 모바일 앱 (Flutter, Android 주력) | `project/abc-english-app` | `/home/jai/pa/abc-english-app` | 2026-04-22 |
| claude-coach | Claude Coach — 클로드 코드 사용 패턴 메타인지 학습 대시보드 | `project/claude-coach` | `/home/jai/pa/claude-coach` | 2026-04-30 |
| youtube-digest | YouTube 구독 영상 다중 LLM 요약 알림 시스템 | `project/youtube-digest` | `/home/jai/pa/youtube-digest` | 2026-05-06 |
| page-guide | 페이지 가이드 — 서버 실행 서비스/포트 카탈로그 조회 페이지 | `project/page-guide` | `/home/jai/pa/page-guide` | 2026-05-07 |
| podcast-study | 사용자 선택형 podcast 영어학습 (HTML-first adapter + LLM selector cache, abc-english 와 ES 인덱스 공유 예정) | `project/podcast-study` | `/home/jai/pa/podcast-study` | 2026-05-13 |

## Legacy 브랜치 (worktree 없음, 작업 미진행)

| ID | Branch | 비고 |
|----|--------|------|
| asset-price-tracker | `project/asset-price-tracker` | 옛 자산 가격 트래커. 재개 시 `git worktree add` |
| naver-market-crawler | `project/naver-market-crawler` | 옛 네이버 마켓 크롤러. 재개 시 `git worktree add` |

## 안전망 태그

- `pre-split-snapshot-2026-04-28` — 분리 작업 시작 직전 commit (`02ea0b2`)
- `legacy-multi-project-2026-04-28` — 분리 작업 안전망 (uncommitted 포함, `ffaa7a7`)
