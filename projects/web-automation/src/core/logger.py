"""로깅 모듈.

Config 기반으로 Python logging을 설정하고,
모듈별 로거를 제공한다. 파일 핸들러와 콘솔 핸들러를 동시에 지원한다.
"""

import logging
import os
from pathlib import Path
from typing import Optional

from .config import Config


# 루트 로거 이름 (프로젝트 전역)
_ROOT_LOGGER_NAME = "web-automation"

# 로그 포맷: [2026-04-13 20:00:00] [INFO] [모듈명] 메시지
_LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 설정 완료 여부 추적
_initialized = False


def setup_logger(config: Config) -> None:
    """Config의 logging 섹션을 기반으로 Python logging을 설정한다.

    설정 키:
        - logging.level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR)
        - logging.file: 로그 파일 경로
        - logging.console: 콘솔 출력 여부 (bool)

    Args:
        config: Config 인스턴스
    """
    global _initialized

    # 로그 레벨 결정
    level_str = config.get("logging.level", "INFO")
    level = getattr(logging, str(level_str).upper(), logging.INFO)

    # 루트 로거 가져오기
    root_logger = logging.getLogger(_ROOT_LOGGER_NAME)
    root_logger.setLevel(level)

    # 기존 핸들러 제거 (중복 방지)
    root_logger.handlers.clear()

    # 포매터 생성
    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    # 파일 핸들러 설정
    log_file: Optional[str] = config.get("logging.file")
    if log_file:
        log_path = Path(log_file)
        # 로그 파일 디렉토리가 없으면 자동 생성
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(str(log_path), encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # 콘솔 핸들러 설정
    console_enabled = config.get("logging.console", True)
    if console_enabled:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    _initialized = True


def get_logger(name: str) -> logging.Logger:
    """모듈별 로거를 반환한다.

    루트 로거의 자식 로거를 생성하여 반환한다.
    setup_logger()가 호출되지 않은 경우에도 동작하지만,
    기본 Python logging 설정이 적용된다.

    Args:
        name: 모듈 이름 (예: "tistory.login", "yanolja.search")

    Returns:
        해당 모듈의 Logger 인스턴스
    """
    return logging.getLogger(f"{_ROOT_LOGGER_NAME}.{name}")
