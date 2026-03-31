---
agent: coder
task_id: TASK-006
status: DONE
timestamp: 2026-03-25T14:00:00
---

## 결과 요약
`src/run_crawler.sh` 셸 스크립트를 신규 작성했다. 프로젝트 루트로 이동 후 `python3 src/main.py`를 실행하며, 로그를 `logs/crawler_YYYY-MM-DD.log`에 날짜별로 저장한다.

구현 내용:
- PROJECT_ROOT, LOG_DIR, TODAY, LOG_FILE 변수 설정
- `mkdir -p`로 logs/ 디렉토리 자동 생성
- `cd`로 프로젝트 루트 이동 후 `python3 src/main.py` 실행
- 실행 시작/종료 시각과 exit code를 로그에 기록
- `chmod +x` 실행 권한 부여 완료

### crontab 등록 안내
아래 두 줄을 `crontab -e`로 등록하면 매일 09:30, 15:30에 자동 실행된다:

```
30 9 * * * /home/jai/program-agent/src/run_crawler.sh >> /home/jai/program-agent/logs/cron.log 2>&1
30 15 * * * /home/jai/program-agent/src/run_crawler.sh >> /home/jai/program-agent/logs/cron.log 2>&1
```

**주의: 실제 crontab 등록은 하지 않았다. Manager가 사용자 확인 후 등록해야 한다.**

## 변경된 파일
- src/run_crawler.sh (신규)

## 이슈/블로커
없음

## 다음 제안
사용자에게 crontab 등록 여부를 확인한 뒤 등록을 진행할 수 있다.
