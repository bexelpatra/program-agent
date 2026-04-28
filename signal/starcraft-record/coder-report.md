---
agent: coder
task_id: TASK-008
status: DONE
timestamp: 2026-04-13T19:00:00
---

## 결과 요약
tkinter 기반 GUI 설정 화면을 `gui.py`로 구현했다.

### 클래스: StarRecordGUI
- `__init__`: tk.Tk 생성, config.load()로 설정 로드, _build_ui() 호출
- `run()`: mainloop 실행

### 화면 구성 (어두운 테마 적용)
- 배경 `#1a1a2e`, 프레임 `#16213e`, 텍스트 `#ffffff`, 버튼 `#0f3460`, 활성 `#e94560`

#### 기본 설정 섹션 (LabelFrame)
- 닉네임: Entry + [저장] 버튼 → `config.add_my_name()` 호출
- 리플레이 폴더: readonly Entry + [찾기] 버튼 → `filedialog.askdirectory()` → config.save()
- SC 경로: readonly Entry + [찾기] 버튼 → `filedialog.askopenfilename()` → config.save()

#### 알림 설정 섹션 (LabelFrame)
- Radiobutton 3개 (Toast / Overlay / Both)
- StringVar로 `cfg["notify_mode"]` 바인딩, 변경 시 자동 저장

#### 실행 섹션 (LabelFrame)
- [게임 시작 (Launch)] 버튼 — placeholder (print)
- [데몬 모드 (Daemon)] 버튼 — placeholder (print)

#### 전적 섹션 (LabelFrame)
- [전적 보기] 버튼 — placeholder (print)
- [리플레이 가져오기] 버튼 — placeholder (print)

#### 상태바
- `status_var` StringVar, 초기값 "대기 중"
- 각 동작 시 상태 메시지 갱신

### 진입점
- `if __name__ == "__main__"` 블록으로 직접 실행 가능

## 변경된 파일
- projects/starcraft_match_record/gui.py (신규 생성)

## 이슈/블로커
없음

## 다음 제안
- TASK-009에서 실행/전적 버튼의 실제 기능을 구현할 것
- main.py에 `gui` 서브커맨드를 추가할 것
