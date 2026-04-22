# Coder Report — TASK-011

- Task: 수집 CLI 엔트리포인트 + cron 예제
- Status: **DONE**
- Date: 2026-04-14

## 산출물

1. `projects/stock-backtest/src/stock_backtest/ingestion/cli.py` (신규)
   - 엔트리: `python -m stock_backtest.ingestion.cli`
   - argparse 기반 옵션:
     - `--market {KR,US,CRYPTO,ALL}` (필수)
     - `--symbols SYM1,SYM2` (선택, 해당 시장 active 자산 중 심볼 필터)
     - `--dry-run` (선택, 대상 자산 열거만 하고 쓰기 없음)
     - `--log-level {DEBUG,INFO,WARNING,ERROR}` (기본 INFO)
   - 동작:
     1. `logging.basicConfig` 를 CLI 에서만 설정 (라이브러리 측 미설정)
     2. `load_config()` 로 설정 로드
     3. market→DataSource 매핑:
        - KR → `PykrxSource`
        - US/CRYPTO → `YFinanceSource` (보조로 `FX` 키에도 동일 인스턴스 등록)
     4. `session_factory` 로 `stock_backtest.data.db.get_session` 컨텍스트 매니저를
        그대로 주입 (`IngestionPipeline` 이 `__enter__/__exit__` 패턴 지원)
     5. `IngestionPipeline.run_for_market(market)` 호출; 심볼 필터가 있으면
        `AssetRepository.list_active` 로 사전 필터 후 `run_for_asset` 루프
     6. 각 자산의 `IngestionResult` 를 info 레벨 로그로 출력
        (asset_id, status, rows_inserted, rows_rejected, error)
     7. market 별 + 전체 요약 로그 (SUCCESS/PARTIAL/FAILED/SKIPPED 카운트)
   - ALL: `("KR", "US", "CRYPTO")` 순차 실행 (매 시장마다 독립 DataSource 인스턴스)
   - Exit code:
     - 0 = 전체 성공 (SUCCESS + SKIPPED 만) 또는 대상 자산 없음
     - 1 = 일부 실패 또는 PARTIAL 존재
     - 2 = 전체 FAILED 또는 내부 예외

2. `projects/stock-backtest/docker/cron/crontab.example` (신규)
   - `CRON_TZ=Asia/Seoul` 로 호스트 TZ 영향 제거
   - KR 18:00 / US 07:00 / Crypto 09:00 (KST)
   - 실행 형식:
     `cd /path/to/projects/stock-backtest && /path/to/venv/bin/python -m stock_backtest.ingestion.cli --market KR >> /var/log/stock_backtest/kr.log 2>&1`
   - 주석으로 PROJECT_DIR/VENV/LOG_DIR 수정 가이드, `.env` 자동 로드 설명 포함
   - 주말 갭 복구용 `--market ALL` 항목은 주석으로 옵션 제시

## 검증

```
$ PYTHONPATH=src DATABASE_URL=postgresql://dummy:dummy@localhost/dummy \
    python -m stock_backtest.ingestion.cli --help
usage: python -m stock_backtest.ingestion.cli [-h] --market {ALL,CRYPTO,KR,US}
                                              [--symbols SYMBOLS] [--dry-run]
                                              [--log-level {DEBUG,INFO,WARNING,ERROR}]
...
```

- `python -c "import stock_backtest.ingestion.cli"` → OK
- `--help` 정상 출력 및 옵션/choices 모두 스펙과 일치

## 설계 메모

- `IngestionPipeline` 은 session_factory 가 반환하는 객체가 컨텍스트
  매니저(`__enter__/__exit__`)면 이를 인식해 세션 생성/종료를 담당한다.
  `db.get_session` 자체가 `@contextmanager` 데코레이터로 감싼 함수라
  그대로 주입 가능하다.
- `--symbols` 는 심볼 화이트리스트로 해석되며, DB 에 등록되지 않은 심볼은
  무시된다 (신규 자산 등록은 DB 측 책임 — architecture.md §9).
- US 시장에서 FX 자산(예: USDKRW) 이 섞여 들어올 가능성을 대비해
  YFinance 인스턴스를 `FX` 키로도 등록. `IngestionPipeline._resolve_source`
  는 `asset.market` 우선이므로 일반 US 자산은 `US` 키로 매칭된다.

## 금지 사항 준수

- `task-board.md`, `architecture.md`, `tests/` 미수정
- `src/stock_backtest/data/repository.py`, `analysis/political_cycle.py`,
  비거래일 방어 신규 모듈 미변경
- `ingestion/` 하위에서 `cli.py` 만 신규 작성
