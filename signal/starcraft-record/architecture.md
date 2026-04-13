# Architecture

## 개요

StarCraft BW/Remastered 리플레이 자동 파싱 → 상대별 전적 관리 → 실시간 알림 도구.
기존 코드베이스(`projects/starcraft_match_record/`)를 기반으로 기능을 추가/개선한다.

- **언어**: Python 3.12+
- **DB**: SQLite (sqlite3)
- **알림**: Windows 토스트(plyer/PowerShell) + tkinter 오버레이
- **파일 감시**: watchdog
- **리플레이 파싱**: 자체 바이너리 파서 (sc_replay_parser.py)

## 프로젝트 구조 (기존 코드, flat 레이아웃)

```
projects/starcraft_match_record/
├── main.py                  # CLI 진입점
├── config.py                # 설정 로드/저장
├── db.py                    # SQLite 래퍼
├── record_manager.py        # 리플레이 파싱→DB 저장, 전적 조회
├── sc_replay_parser.py      # .rep 바이너리 파서
├── notifier.py              # 알림 (toast + overlay)
├── watcher.py               # watchdog 폴더 감시
├── launcher.py              # SC 실행/감지
├── config.json              # 사용자 설정
├── star_record.db           # SQLite DB
├── requirements.txt         # 의존성
├── replays/samples/          # 샘플 리플레이
└── docs/                    # 문서
```

**주의**: 이 프로젝트는 `src/` 하위가 아닌 루트에 .py 파일이 위치한다.

## 현재 Phase 2 작업

### 작업 1: 알림 동작 확인 및 개선
- 현재 overlay/toast 알림이 정상 동작하는지 검증
- 알림에 표시할 정보 구조 개선 (메모 포함)

### 작업 2: 채팅 메모 기능
- 인게임 채팅에서 특정 접두사 명령어로 메모 저장
- DB에 player_memos 테이블 추가
- 리플레이 파싱 시 채팅에서 메모 명령어 감지 → DB 저장
- 다음 대전 시 알림에 메모 표시

### 채팅 메모 명령어 설계

```
!memo <내용>         → 마지막 상대에 대한 메모 저장
!memo clear          → 마지막 상대 메모 삭제
```

리플레이 파싱 시 본인 채팅 중 `!memo`로 시작하는 메시지를 감지하여 처리한다.

### DB 변경: player_memos 테이블

```sql
CREATE TABLE IF NOT EXISTS player_memos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id   INTEGER NOT NULL,
    memo        TEXT NOT NULL,
    source_game_id INTEGER,
    created_at  TEXT DEFAULT (datetime('now', 'localtime')),
    updated_at  TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE,
    FOREIGN KEY (source_game_id) REFERENCES games(id) ON DELETE SET NULL
);
```

### 알림 구조 개선

overlay에 메모 정보를 추가 표시:

```
┌──────────────────────────────┐
│  StarRecord - 전적 알림       │
├──────────────────────────────┤
│  vs PlayerName (Protoss)     │
│  3승 2패                     │
│  메모: 초반 러시 주의          │
└──────────────────────────────┘
```

### 작업 3: GUI 설정 화면 (tkinter)

tkinter 기반 설정/관리 GUI. 추가 의존성 없음 (표준 라이브러리).

#### 파일: `gui.py` (신규)

#### 화면 구성

```
┌──────────────────────────────────────────────┐
│  StarRecord                            [─][X] │
├──────────────────────────────────────────────┤
│                                              │
│  ── 기본 설정 ──                              │
│  닉네임:       [kimsabuho          ] [저장]   │
│  리플레이 폴더: [C:\...\Replays     ] [찾기]   │
│  SC 경로:      [C:\...\StarCraft.exe] [찾기]   │
│                                              │
│  ── 알림 설정 ──                              │
│  알림 방식:  ○ Toast  ● Overlay  ○ Both       │
│                                              │
│  ── 실행 ──                                   │
│  [ 게임 시작 (Launch) ]  [ 데몬 모드 (Daemon) ] │
│                                              │
│  ── 전적 ──                                   │
│  [ 전적 보기 ]  [ 리플레이 가져오기 ]            │
│                                              │
│  상태: 대기 중                                 │
└──────────────────────────────────────────────┘
```

#### 기능 요구사항
1. **설정 섹션**: config.json 값을 로드/표시/저장
   - 닉네임 입력 + 저장 버튼
   - 리플레이 폴더 경로 + 찾기 버튼 (filedialog.askdirectory)
   - SC 경로 + 찾기 버튼 (filedialog.askopenfilename)
   - 알림 방식 라디오 버튼 (toast/overlay/both)
   - 변경 시 자동 저장 또는 저장 버튼
2. **실행 섹션**: 버튼으로 모드 시작
   - Launch 버튼 → 별도 스레드에서 launch_mode 실행
   - Daemon 버튼 → 별도 스레드에서 daemon_mode 실행
   - 실행 중이면 버튼 비활성화 + "실행 중" 표시
3. **전적 섹션**:
   - 전적 보기 → 새 창에 records 표시
   - 리플레이 가져오기 → 폴더 선택 후 import 실행
4. **상태바**: 현재 동작 상태 표시

#### 진입점: `main.py`에 `gui` 서브커맨드 추가
```
python main.py gui
```
또는 `gui.py` 직접 실행도 가능하게 `if __name__ == "__main__"` 포함.

## 현재 상태
- Phase 1 완료 (리플레이 파싱, DB, 전적 조회, 알림, CLI 모두 구현됨)
- Phase 2 작업 1, 2 완료 (알림 검증, 채팅 메모 기능)
- Phase 2 작업 3 진행 중 (GUI 설정 화면)
