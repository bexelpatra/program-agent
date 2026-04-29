"""백필 큐 — domain.asset.registration.BackfillEnqueuer Protocol 구현.

architecture.md V3 § "자산 카탈로그 + 사용자 자유 추가" L536: 검증 통과 시
`assets.active=true` 등록 + 백그라운드 백필 큐잉.

MVP 는 단순 in-memory queue + threading 으로 즉시 백그라운드 실행.
향후 APScheduler / Celery / RQ 로 교체 가능 (Protocol 만 유지하면 됨).

Singleton 인스턴스화는 FastAPI lifespan / main.py (TASK-061) 책임.
"""
from __future__ import annotations

import logging
import threading
from queue import Empty, Queue
from typing import Callable

logger = logging.getLogger(__name__)


class BackfillQueue:
    """asset_id 큐잉 + 백그라운드 워커.

    BackfillEnqueuer Protocol (`enqueue(asset_id) -> None`) 구현.

    MVP 는 max_workers=1 직렬 처리 (yfinance/pykrx rate limit 보호).
    실제 백필 실행자(`backfill_runner`)는 외부 (e.g. TASK-022 의 backfill_asset)
    에서 주입받는다.
    """

    def __init__(
        self,
        backfill_runner: Callable[[int], None],
        max_workers: int = 1,
    ) -> None:
        """
        Args:
            backfill_runner: (asset_id) -> None. 실제 백필 실행 callable.
                예외를 던져도 워커는 계속 살아 있도록 _worker_loop 가 catch.
            max_workers: 동시 실행 워커 스레드 수. MVP 직렬은 1.
        """
        self._queue: Queue[int] = Queue()
        self._runner = backfill_runner
        self._workers: list[threading.Thread] = []
        self._stop_event = threading.Event()
        self._max_workers = max_workers

    def start(self) -> None:
        """워커 스레드를 기동. 이미 시작된 큐에 재호출하면 워커가 추가된다 (MVP 는 단일 호출 가정)."""
        for i in range(self._max_workers):
            t = threading.Thread(
                target=self._worker_loop,
                name=f"backfill-worker-{i}",
                daemon=True,
            )
            t.start()
            self._workers.append(t)
        logger.info("BackfillQueue started with %d worker(s)", self._max_workers)

    def stop(self) -> None:
        """워커 종료 신호. 진행 중인 작업이 끝나면 워커 루프 탈출.

        graceful shutdown (모든 잔여 작업 완료 대기) 은 후속 태스크에서 다룬다.
        """
        self._stop_event.set()

    def enqueue(self, asset_id: int) -> None:
        """BackfillEnqueuer Protocol method — asset_id 를 큐 끝에 추가."""
        self._queue.put(asset_id)
        logger.info(
            "enqueued backfill for asset_id=%d, queue size=%d",
            asset_id,
            self._queue.qsize(),
        )

    def _worker_loop(self) -> None:
        """워커 메인 루프. stop_event 가 set 될 때까지 큐에서 작업 소비."""
        while not self._stop_event.is_set():
            try:
                asset_id = self._queue.get(timeout=1.0)
            except Empty:
                continue
            except Exception:
                # 알 수 없는 큐 예외도 워커는 계속 살아 있어야 함.
                continue
            try:
                self._runner(asset_id)
            except Exception as e:
                logger.exception(
                    "backfill failed for asset_id=%d: %s", asset_id, e
                )
            finally:
                self._queue.task_done()
