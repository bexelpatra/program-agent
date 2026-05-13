# Architecture (초기 스켈레톤)

> 본 파일은 `project/podcast-study` 분기 시점의 **핵심 결정 메모**다. 본격 architecture 작성·Reviewer 검증·task-board 분해는 새 세션 (`cd /home/jai/pa/podcast-study && claude`) 에서 진행한다.

## 프로젝트 정체성

- **목적**: 영어 학습. 팟캐스트는 도구이고, ES + DB 에 학습 자료(어휘/숙어/구동사/관용어)를 축적·조회하는 게 본질.
- **abc-english 와의 차별점**: abc-english 는 자동 큐레이션, podcast-study 는 **사용자가 URL 을 직접 입력해 듣고 싶은 source/episode 를 선택**.
- **abc-english 와의 관계**: 표준 화면 reference 로 차용 (`projects/abc-english/web/`). 데이터 모델·ES 인덱스는 후일 통합 (B2 점진 통합 정책).

## 확정된 핵심 결정 (2026-05-13 사용자 확정)

1. **ES 인덱스 공유 — 옵션 B2 (점진 통합)**:
   - podcast-study 는 처음부터 source-agnostic 인덱스 (`podcasts-episodes`, `podcasts-sentences`, `podcasts-vocabulary`, `podcasts-expressions`) 에 적재.
   - `source` 필드 1급 (예: `"abc-news-daily"`, `"cbc-front-burner"`).
   - abc-english 의 기존 `abc-*` 인덱스 운영은 **그대로 유지**. 통합 reindex 는 별도 마일스톤으로 분리.
2. **Selector cache 저장소 — SQLite** (`data/adapters.db`):
   - 추후 사용자/로그인 기능 추가 시 RDB(MySQL 등) 이전 가능하도록 가벼운 추상화 레이어 유지.
   - 현재 다른 용도 계획 없음.
3. **RSS 보류**:
   - 이유: RSS 에는 transcript 가 없는 경우가 많음 (사용자 실측: CBC Front Burner, NYT The Daily — RSS 부재이나 웹페이지엔 있음).
   - HTML 페이지 직접 방문 → LLM selector discovery → 캐시 가 1순위.
4. **JS 렌더링 — Playwright 폴백**:
   - 캡차/로그인 막는 사이트는 한계 인정.
   - requests 로 HTML 받았을 때 body 길이 빈약하거나 transcript/audio selector miss 면 Playwright 로 재시도.
5. **Series vs single 판별 — URL 휴리스틱**:
   - 도메인별 정규식 패턴으로 시작. 모호한 경우만 LLM 보조.
6. **흐름**:
   ```
   URL → series? single? → domain adapter cache 조회
     hit: selectors 그대로 사용
     miss: requests 시도 → 부족하면 Playwright → LLM 으로 selector 추출 → DB UPSERT
   → audio + transcript + 메타 추출
   → (기존 abc 파이프라인 재사용) transcriber → comparator → analyzer → llm_analyzer → loader (podcasts-* 인덱스)
   → abc 의 study.html 차용한 학습 UI
   ```
7. **Transcript-optional 모드**:
   - transcript 없는 source (예: BBC) 는 Whisper-only.
   - WER 기반 listening_difficulty 산출 불가 → 해당 필드 비움.

## 1차 검증 마일스톤 (Phase 1)

- **Source A**: ABC News Daily — 기존 collector.py 로직을 새 adapter interface 의 한 구현체로 재구현. 기존 abc-english 운영은 무중단 유지.
- **Source B**: CBC Front Burner — 사용자 선택. 새 adapter interface 검증.
- 두 source 가 같은 adapter interface 로 동작 → 추상화 검증 성공 기준.

## 차후 결정 (지금 결정 안 함)

- 통합 reindex 시점 (abc-* → podcasts-*).
- 신규 web UI 통합 디자인 (다양한 source 를 한 화면에서 묶어 보기).
- 다른 source 확장 (BBC, NPR, NYT 등).
- 모바일 앱 연계 (현 abc-english-app 과의 관계).

## 디렉토리 (예정)

```
projects/podcast-study/
├── config/
│   └── settings.yaml
├── data/
│   ├── adapters.db          # SQLite selector cache
│   ├── audio/               # source 무관 통합
│   └── transcripts/
├── src/
│   ├── adapter/             # source 어댑터 (interface + impls)
│   │   ├── __init__.py
│   │   ├── base.py          # SourceAdapter (Protocol/ABC)
│   │   ├── discovery.py     # LLM selector discovery
│   │   ├── cache.py         # SQLite cache wrapper
│   │   ├── abc_news_daily.py
│   │   └── cbc_front_burner.py
│   ├── fetcher.py           # requests / Playwright 폴백
│   ├── url_router.py        # series vs single URL 휴리스틱
│   ├── pipeline/            # abc 의 transcriber/comparator/analyzer/llm_analyzer/loader 재사용
│   └── cli.py
├── tests/
└── web/                     # abc 의 web/ 차용 (초기엔 단순 복제, 차후 통합 디자인)
```

(본격 작성은 새 세션에서)
