"""텔레그램 봇 알림 모듈.

텔레그램 Bot API를 직접 호출하여 텍스트, 사진, 포맷된 알림을
전송한다. 자동화 흐름을 중단하지 않도록 전송 실패 시 예외를
던지지 않고 로깅만 수행한다.
"""

import logging
from pathlib import Path
from typing import Optional

import requests

from .config import Config

logger = logging.getLogger(__name__)

# 텔레그램 Bot API 기본 URL
_API_BASE = "https://api.telegram.org/bot{token}"


class TelegramNotifier:
    """텔레그램 봇을 통해 알림을 전송하는 클래스.

    Config에서 telegram 관련 설정(bot_token, chat_id, enabled)을
    읽어 초기화한다. enabled가 False이면 모든 메서드가 아무 동작도
    하지 않는다 (silent no-op).
    """

    def __init__(self, config: Config) -> None:
        """TelegramNotifier 인스턴스를 생성한다.

        Args:
            config: Config 인스턴스 (telegram.bot_token, telegram.chat_id,
                    telegram.enabled 설정 필요)
        """
        self._enabled: bool = bool(config.get("telegram.enabled", False))
        self._bot_token: str = config.get("telegram.bot_token", "")
        self._chat_id: str = str(config.get("telegram.chat_id", ""))
        self._timeout: int = int(config.get("telegram.timeout", 10))

        if self._enabled and not self._bot_token:
            logger.warning("텔레그램 알림이 활성화되었으나 bot_token이 설정되지 않았습니다.")
            self._enabled = False

        if self._enabled and not self._chat_id:
            logger.warning("텔레그램 알림이 활성화되었으나 chat_id가 설정되지 않았습니다.")
            self._enabled = False

    @property
    def enabled(self) -> bool:
        """알림 활성화 여부를 반환한다."""
        return self._enabled

    @property
    def api_base(self) -> str:
        """현재 토큰에 대한 API 기본 URL을 반환한다."""
        return _API_BASE.format(token=self._bot_token)

    def send_message(self, text: str) -> bool:
        """텍스트 메시지를 전송한다.

        Args:
            text: 전송할 메시지 텍스트

        Returns:
            전송 성공 여부 (비활성화 상태면 True 반환)
        """
        if not self._enabled:
            return True

        url = f"{self.api_base}/sendMessage"
        payload = {
            "chat_id": self._chat_id,
            "text": text,
            "parse_mode": "HTML",
        }

        return self._post(url, data=payload)

    def send_photo(self, photo_path: str, caption: str = "") -> bool:
        """사진(스크린샷)을 전송한다.

        Args:
            photo_path: 전송할 사진 파일 경로
            caption: 사진에 첨부할 캡션 (선택)

        Returns:
            전송 성공 여부 (비활성화 상태면 True 반환)
        """
        if not self._enabled:
            return True

        path = Path(photo_path)
        if not path.exists():
            logger.error("사진 파일이 존재하지 않습니다: %s", photo_path)
            return False

        url = f"{self.api_base}/sendPhoto"
        payload = {
            "chat_id": self._chat_id,
        }
        if caption:
            payload["caption"] = caption
            payload["parse_mode"] = "HTML"

        try:
            with open(path, "rb") as photo_file:
                files = {"photo": (path.name, photo_file, "image/png")}
                response = requests.post(
                    url, data=payload, files=files, timeout=self._timeout
                )
                response.raise_for_status()

                result = response.json()
                if not result.get("ok"):
                    logger.error(
                        "텔레그램 사진 전송 실패 (API 응답): %s",
                        result.get("description", "알 수 없는 오류"),
                    )
                    return False

                logger.info("텔레그램 사진 전송 성공: %s", photo_path)
                return True

        except requests.RequestException as e:
            logger.error("텔레그램 사진 전송 중 네트워크 오류: %s", e)
            return False
        except OSError as e:
            logger.error("사진 파일 읽기 오류: %s", e)
            return False

    def send_alert(self, title: str, body: str) -> bool:
        """포맷된 알림 메시지를 전송한다.

        제목을 굵게 표시하고 이모지를 포함한 형식으로 전송한다.

        Args:
            title: 알림 제목
            body: 알림 본문

        Returns:
            전송 성공 여부 (비활성화 상태면 True 반환)
        """
        if not self._enabled:
            return True

        # 포맷된 알림 메시지 구성 (HTML 파싱 모드)
        message = f"🔔 <b>{title}</b>\n\n{body}"
        return self.send_message(message)

    def _post(
        self,
        url: str,
        data: Optional[dict] = None,
    ) -> bool:
        """텔레그램 API에 POST 요청을 보낸다.

        전송 실패 시 예외를 던지지 않고 로깅만 수행한다.

        Args:
            url: 요청할 API URL
            data: POST 요청 데이터

        Returns:
            요청 성공 여부
        """
        try:
            response = requests.post(url, data=data, timeout=self._timeout)
            response.raise_for_status()

            result = response.json()
            if not result.get("ok"):
                logger.error(
                    "텔레그램 API 응답 오류: %s",
                    result.get("description", "알 수 없는 오류"),
                )
                return False

            logger.info("텔레그램 메시지 전송 성공")
            return True

        except requests.RequestException as e:
            logger.error("텔레그램 메시지 전송 중 네트워크 오류: %s", e)
            return False
