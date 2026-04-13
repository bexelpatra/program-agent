"""YAML 설정 로더 모듈.

공통 설정과 사이트별 설정을 로드하고, 점(.) 표기법 접근 및
환경변수 오버라이드를 지원한다.
"""

import os
from pathlib import Path
from typing import Any

import yaml


# 환경변수 접두사 (예: WA_TELEGRAM_BOT_TOKEN)
_ENV_PREFIX = "WA_"


class Config:
    """YAML 기반 설정 로더.

    공통 설정(settings.yaml)을 기본으로 로드하고,
    사이트별 설정 파일을 추가로 병합할 수 있다.
    """

    def __init__(self, project_root: str = ".") -> None:
        """Config 인스턴스를 생성하고 공통 설정을 로드한다.

        Args:
            project_root: 프로젝트 루트 디렉토리 경로
        """
        self._project_root = Path(project_root)
        self._config_dir = self._project_root / "config"
        self._data: dict[str, Any] = {}
        self._loaded_sites: list[str] = []

        # 공통 설정 자동 로드
        self._load_yaml(self._config_dir / "settings.yaml")

    def _load_yaml(self, path: Path) -> None:
        """YAML 파일을 읽어서 현재 설정에 병합한다.

        Args:
            path: YAML 파일 경로
        """
        if not path.exists():
            raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if data and isinstance(data, dict):
            self._deep_merge(self._data, data)

    def _deep_merge(self, base: dict, override: dict) -> dict:
        """두 딕셔너리를 재귀적으로 병합한다.

        override의 값이 base를 덮어쓴다. 양쪽 모두 dict인 경우
        재귀적으로 병합한다.

        Args:
            base: 기본 딕셔너리 (이 객체가 직접 수정됨)
            override: 덮어쓸 딕셔너리

        Returns:
            병합된 딕셔너리 (base와 동일한 객체)
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    def load_site(self, site_name: str) -> None:
        """사이트별 설정 파일을 추가로 로드하여 병합한다.

        Args:
            site_name: 사이트 이름 (예: "tistory", "yanolja")
        """
        site_path = self._config_dir / f"{site_name}.yaml"
        self._load_yaml(site_path)
        if site_name not in self._loaded_sites:
            self._loaded_sites.append(site_name)

    def get(self, key: str, default: Any = None) -> Any:
        """점(.) 표기법으로 설정값을 가져온다.

        환경변수 오버라이드를 우선 확인한다. 환경변수명은
        접두사 'WA_' + 키를 대문자로 변환하고 점(.)을 밑줄(_)로
        치환한 형태이다.
        예: "telegram.bot_token" → WA_TELEGRAM_BOT_TOKEN

        Args:
            key: 점(.) 구분 키 (예: "telegram.bot_token")
            default: 키가 없을 때 반환할 기본값

        Returns:
            설정값 또는 기본값
        """
        # 환경변수 오버라이드 확인
        env_key = _ENV_PREFIX + key.upper().replace(".", "_")
        env_value = os.environ.get(env_key)
        if env_value is not None:
            return self._cast_env_value(env_value)

        # YAML 설정에서 조회
        keys = key.split(".")
        current: Any = self._data
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        return current

    def _cast_env_value(self, value: str) -> Any:
        """환경변수 문자열을 적절한 타입으로 변환한다.

        Args:
            value: 환경변수 값 (문자열)

        Returns:
            변환된 값 (bool, int, float, 또는 원본 문자열)
        """
        # 불리언 변환
        if value.lower() in ("true", "1", "yes"):
            return True
        if value.lower() in ("false", "0", "no"):
            return False

        # 정수 변환
        try:
            return int(value)
        except ValueError:
            pass

        # 실수 변환
        try:
            return float(value)
        except ValueError:
            pass

        return value

    @property
    def data(self) -> dict[str, Any]:
        """현재 로드된 전체 설정 딕셔너리를 반환한다."""
        return self._data

    @property
    def loaded_sites(self) -> list[str]:
        """로드된 사이트 목록을 반환한다."""
        return list(self._loaded_sites)

    def __repr__(self) -> str:
        sites = ", ".join(self._loaded_sites) if self._loaded_sites else "없음"
        return f"Config(root={self._project_root}, sites=[{sites}])"
