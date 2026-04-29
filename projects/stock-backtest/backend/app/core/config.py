"""애플리케이션 환경 설정.

DB 객체 생성은 db.py 책임 — 본 모듈은 환경변수 로드/검증만 한다.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """`.env` 또는 OS 환경변수에서 주입되는 런타임 설정."""

    database_url: str
    database_url_test: str | None = None
    default_base_currency: str = "KRW"
    tz: str = "Asia/Seoul"

    # `.env` 파일은 backend/ 또는 프로젝트 루트(상위)에서 모두 발견되도록 둘 다 시도한다.
    # case_sensitive=False 로 DATABASE_URL == database_url 매핑 허용.
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """전 프로세스 단일 인스턴스. lru_cache 로 .env 재파싱 비용 제거."""
    return Settings()
