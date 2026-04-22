# Cron 스케줄 설치 가이드

데이터 수집(`stock_backtest.ingestion.cli`)을 시장별로 정기 실행하기 위한 가이드다. 설계 근거는 `signal/stock-backtest/architecture.md` §9 참조.

## 1. 개요 - 시장별 스케줄 (KST)

| 시장 | 스케줄 (KST) | 근거 |
|------|--------------|------|
| KR | 매일 18:00 | 한국 거래소 장 마감(15:30) 이후 종가 확정 여유 포함, 당일 데이터 수집 |
| US | 매일 07:00 | 전일 미국 장 마감(EST 16:00 ≒ KST 06:00) 이후, 익일 새벽에 전일치 수집 |
| Crypto | 매일 09:00 | UTC 00:00 일봉 캔들 확정 시점 = KST 09:00 |

모든 스케줄은 호스트 타임존과 무관하게 `CRON_TZ=Asia/Seoul`을 사용해 KST 기준으로 고정한다.

## 2. 사전 조건

1. **가상환경 활성화 및 의존성 설치**
   ```bash
   cd /path/to/projects/stock-backtest
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **DB 기동** (Docker Compose)
   ```bash
   docker compose up -d
   docker compose ps   # healthy 확인
   ```
3. **.env 설정**: `.env.example`을 복사해 `.env`를 만들고 DB 접속 정보를 채운다. `stock_backtest.data.db`가 `load_dotenv`로 자동 로드한다.
4. **`assets` 테이블에 수집 대상 자산이 등록되어 있어야 한다** (§9: DB 기반 증분 수집).

## 3. crontab 편집 방법

사용자 crontab에 등록:

```bash
crontab -e
```

시스템 전역 cron으로 등록하려면 `/etc/cron.d/stock-backtest` 경로에 파일을 복사한다 (이 경우 user 컬럼 필요).

crontab 상단에 반드시 아래를 포함한다:

```
CRON_TZ=Asia/Seoul
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

`CRON_TZ`가 없으면 호스트 타임존을 따르게 되어 의도한 KST 스케줄에서 벗어날 수 있다.

## 4. 샘플 crontab

`docker/cron/crontab.example` 파일에 전체 예시가 있다. 핵심 라인:

```cron
CRON_TZ=Asia/Seoul
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# KR: 매일 18:00 KST (장 마감 이후)
0 18 * * * cd /path/to/projects/stock-backtest && /path/to/venv/bin/python -m stock_backtest.ingestion.cli --market KR >> /var/log/stock_backtest/kr.log 2>&1

# US: 매일 07:00 KST (전일 미 장 종료 후)
0 7 * * * cd /path/to/projects/stock-backtest && /path/to/venv/bin/python -m stock_backtest.ingestion.cli --market US >> /var/log/stock_backtest/us.log 2>&1

# Crypto: 매일 09:00 KST (UTC 00:00 캔들 확정)
0 9 * * * cd /path/to/projects/stock-backtest && /path/to/venv/bin/python -m stock_backtest.ingestion.cli --market CRYPTO >> /var/log/stock_backtest/crypto.log 2>&1

# (선택) 주말 오전 전체 재수집 - 갭 복구용
# 0 10 * * 6 cd /path/to/projects/stock-backtest && /path/to/venv/bin/python -m stock_backtest.ingestion.cli --market ALL >> /var/log/stock_backtest/all.log 2>&1
```

`/path/to/projects/stock-backtest`, `/path/to/venv/bin/python`은 실제 환경 경로로 치환한다.

## 5. 로그 디렉토리 생성

표준 로그 경로는 `/var/log/stock_backtest/`를 권장한다. cron을 실행할 사용자에게 쓰기 권한이 있어야 한다.

```bash
sudo mkdir -p /var/log/stock_backtest
sudo chown "$USER":"$USER" /var/log/stock_backtest
sudo chmod 755 /var/log/stock_backtest
```

시스템 디렉토리 권한 변경이 부담스러우면 홈 디렉토리(`~/.local/var/log/stock_backtest/`) 등을 사용해도 무방하다. crontab 라인의 리디렉션 경로도 동일하게 변경한다.

로그 로테이션은 `logrotate`로 별도 구성한다 (예시 생략).

## 6. 문제 해결

### 6.1 실행 여부·종료 코드 확인

```bash
# 로그에 남은 "exit" 이나 traceback 확인
grep -iE "exit|error|traceback" /var/log/stock_backtest/*.log

# 최근 cron 실행 로그 (systemd 기반 배포판)
journalctl -u cron --since "today"
# 또는
grep CRON /var/log/syslog | tail
```

### 6.2 수동 실행 (cron 없이 동작 확인)

```bash
cd /path/to/projects/stock-backtest
source .venv/bin/activate
python -m stock_backtest.ingestion.cli --market KR --dry-run
```

`--dry-run` 으로 실제 DB 기록 없이 수집 대상 자산·기간을 확인할 수 있다. 정상 동작을 본 뒤 플래그를 제거해 본 실행한다.

### 6.3 yfinance rate limit / 네트워크 오류

- `config/defaults.yaml` (또는 ingestion 설정)의 `min_interval_seconds`(초당 요청 간격)를 늘려 rate limit을 완화한다. yfinance는 통상 1~2 req/s 이하가 안전하다.
- 자산 단위로 3회 지수백오프(1s→2s→4s) 재시도가 이미 구현되어 있으며, 최종 실패 자산은 `ingestion_log` 테이블에 `FAILED`로 기록되고 잡은 계속 진행한다. 다음 실행 주기에서 갭 감지로 자동 재수집된다.

### 6.4 SIGPIPE / 비정상 종료

크론 환경에서 stdout/stderr 리디렉션 없이 실행하면 SIGPIPE로 조기 종료될 수 있다. 샘플처럼 `>> ...log 2>&1`을 반드시 사용한다.

### 6.5 TZ 불일치

`date`로 호스트 TZ와 cron 실행 시각을 비교한다. crontab 상단 `CRON_TZ=Asia/Seoul`이 누락되면 UTC로 해석될 수 있다.

## 7. (선택) systemd timer 대안

cron 대신 systemd timer를 선호하는 경우의 예시. 서비스 + 타이머 한 쌍씩 시장별로 작성한다. 아래는 KR 기준.

### `/etc/systemd/system/stock-backtest-kr.service`

```ini
[Unit]
Description=stock-backtest KR ingestion
After=network-online.target docker.service
Wants=network-online.target

[Service]
Type=oneshot
User=stock
WorkingDirectory=/path/to/projects/stock-backtest
Environment=PYTHONUNBUFFERED=1
ExecStart=/path/to/venv/bin/python -m stock_backtest.ingestion.cli --market KR
StandardOutput=append:/var/log/stock_backtest/kr.log
StandardError=append:/var/log/stock_backtest/kr.log
```

### `/etc/systemd/system/stock-backtest-kr.timer`

```ini
[Unit]
Description=stock-backtest KR ingestion (daily 18:00 KST)

[Timer]
OnCalendar=*-*-* 18:00:00 Asia/Seoul
Persistent=true
Unit=stock-backtest-kr.service

[Install]
WantedBy=timers.target
```

활성화:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now stock-backtest-kr.timer
systemctl list-timers | grep stock-backtest
```

US/Crypto도 동일한 구조로 `stock-backtest-us.{service,timer}` (07:00), `stock-backtest-crypto.{service,timer}` (09:00)를 작성한다. `OnCalendar`의 `Asia/Seoul` 접미사로 DST 변경·호스트 TZ 변경과 무관하게 KST 기준이 유지된다 (systemd 242+).

`Persistent=true` 는 기기 다운타임으로 실행을 놓친 경우 부팅 후 즉시 한 번 실행해 갭을 줄인다.
