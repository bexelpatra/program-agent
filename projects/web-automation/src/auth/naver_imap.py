"""Naver IMAP 인증번호 추출 모듈.

Naver 메일함에 IMAP(SSL)로 접속해 특정 발신자가 최근에 보낸 메일을
조회하고, 제목/본문에서 6~8자리 인증번호를 추출한다.

주요 용도:
    티스토리가 카카오 로그인 시 Naver 이메일로 인증번호(실측 8자리)를
    보내면, 이 모듈이 해당 메일을 찾아 인증번호를 반환한다.
    Naver 계정은 인증번호 수신용 IMAP 접속에만 사용된다.

보안 주의:
    비밀번호/토큰은 로그에 출력하지 않는다. IMAP 로그인 실패 등
    예외 메시지에도 민감정보를 포함하지 않는다.
"""

from __future__ import annotations

import email
import imaplib
import re
import socket
from contextlib import contextmanager
from datetime import datetime, timedelta
from email.header import decode_header, make_header
from email.message import Message
from typing import Iterator, Optional

from ..core.config import Config
from ..core.logger import get_logger


# 기본 타임아웃 (초). 연결·검색·fetch 모두 이 값을 사용한다.
_DEFAULT_TIMEOUT = 30

# 기본 인증번호 정규식 (단어 경계로 6~8자리 숫자 매치).
# 카카오 인증번호는 실측 8자리(예: 55898679). 과거 6자리 공급자도 지원.
_DEFAULT_CODE_PATTERN = r"\b\d{6,8}\b"

logger = get_logger("auth.naver_imap")


def _decode_mime_header(value: str | None) -> str:
    """MIME 인코딩된 헤더 값을 사람이 읽을 수 있는 문자열로 변환한다.

    Args:
        value: 헤더 원본 값 (예: "=?utf-8?B?...?=")

    Returns:
        디코딩된 문자열. 입력이 None이면 빈 문자열 반환.
    """
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:  # noqa: BLE001 - 헤더 포맷이 깨진 경우 안전하게 원본 반환
        return value


def _extract_text_parts(msg: Message) -> str:
    """메일 메시지에서 text/plain 및 text/html 파트를 모두 추출해 합친다.

    Args:
        msg: 파싱된 email.message.Message 인스턴스

    Returns:
        본문 텍스트(파트 구분 없이 이어붙임). 디코딩 실패 시 해당 파트는 건너뛴다.
    """
    chunks: list[str] = []

    if msg.is_multipart():
        parts: Iterator[Message] = msg.walk()
    else:
        parts = iter([msg])

    for part in parts:
        content_type = part.get_content_type()
        if content_type not in ("text/plain", "text/html"):
            continue

        payload = part.get_payload(decode=True)
        if payload is None:
            continue

        charset = part.get_content_charset() or "utf-8"
        try:
            text = payload.decode(charset, errors="replace")
        except (LookupError, AttributeError):
            # 알 수 없는 charset 은 utf-8 로 재시도
            try:
                text = payload.decode("utf-8", errors="replace")
            except Exception:  # noqa: BLE001
                continue

        chunks.append(text)

    return "\n".join(chunks)


@contextmanager
def _imap_session(
    server: str,
    port: int,
    email_addr: str,
    password: str,
    timeout: int = _DEFAULT_TIMEOUT,
) -> Iterator[imaplib.IMAP4_SSL]:
    """IMAP4_SSL 세션을 열고 반환한 뒤, 종료 시 logout을 보장한다.

    Args:
        server: IMAP 서버 호스트 (예: imap.naver.com)
        port: IMAP 포트 (기본 993)
        email_addr: 로그인 이메일
        password: 로그인 비밀번호(앱 비밀번호 권장)
        timeout: 소켓 타임아웃 (초)

    Yields:
        로그인된 IMAP4_SSL 클라이언트

    주의:
        비밀번호는 로깅하지 않는다. 로그인 실패 시에도 원문 메시지만 기록.
    """
    # 소켓 타임아웃은 모듈 전역으로 설정 (imaplib 은 자체 timeout 옵션이
    # Python 3.9+ 에서만 가용하여, 호환성을 위해 socket 전역값을 사용)
    original_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)

    client: Optional[imaplib.IMAP4_SSL] = None
    try:
        client = imaplib.IMAP4_SSL(server, port)
        client.login(email_addr, password)
        logger.info("IMAP 로그인 성공 (server=%s, port=%s)", server, port)
        yield client
    finally:
        if client is not None:
            try:
                # 메일함이 선택된 상태라면 close 후 logout
                try:
                    client.close()
                except Exception:  # noqa: BLE001 - select 안 된 경우 등
                    pass
                client.logout()
            except Exception as exc:  # noqa: BLE001
                logger.warning("IMAP logout 중 경고: %s", exc)
        socket.setdefaulttimeout(original_timeout)


def _build_search_criteria(sender: str, since: datetime) -> list[str]:
    """IMAP SEARCH 조건을 구성한다.

    Args:
        sender: 발신자 이메일(부분 매치 가능)
        since: 이 시각 이후 수신된 메일만 검색 (IMAP SINCE 는 날짜 단위)

    Returns:
        IMAP search 인자 리스트 (예: ["FROM", "noreply@tistory.com", "SINCE", "22-Apr-2026"])
    """
    # IMAP SINCE 는 DD-Mon-YYYY 포맷 (날짜 단위). 시간 필터는 사후 처리.
    since_str = since.strftime("%d-%b-%Y")
    return ["FROM", sender, "SINCE", since_str]


def fetch_verification_code(
    config: Config,
    sender: str,
    within_minutes: int = 10,
    code_pattern: str = _DEFAULT_CODE_PATTERN,
    timeout: int = _DEFAULT_TIMEOUT,
) -> Optional[str]:
    """Naver IMAP에서 최근 메일을 조회해 6~8자리 인증번호를 추출한다.

    Config 에서 아래 키를 사용한다:
        - naver_imap.server   (str)
        - naver_imap.port     (int)
        - naver_imap.email    (str)  # WA_NAVER_IMAP_EMAIL 환경변수 오버라이드 가능
        - naver_imap.password (str)  # WA_NAVER_IMAP_PASSWORD 환경변수 오버라이드 가능

    Args:
        config: 로드된 Config 인스턴스. 이 함수는 `config.load_site("tistory")`가
            이미 호출되었다고 가정한다.
        sender: 발신자 이메일 주소 또는 부분 문자열 (IMAP FROM 필터)
        within_minutes: 최근 N분 이내 수신 메일만 대상. 기본 10분 (일반적인 인증번호 유효 시간).
        code_pattern: 인증번호 정규식. 기본은 `\\b\\d{6,8}\\b`.
        timeout: 소켓 타임아웃 (초)

    Returns:
        추출된 인증번호 문자열 또는 None (일치 메일이 없거나 6~8자리 매치 실패 시).

    Raises:
        ValueError: Config 에 필수 키가 누락된 경우.
        imaplib.IMAP4.error: IMAP 로그인/검색 실패 등.
    """
    server = config.get("naver_imap.server")
    port = config.get("naver_imap.port", 993)
    email_addr = config.get("naver_imap.email")
    password = config.get("naver_imap.password")

    if not server or not email_addr or not password:
        raise ValueError(
            "Config에 naver_imap.server, naver_imap.email, naver_imap.password 가 모두 필요합니다."
        )

    pattern = re.compile(code_pattern)
    # SINCE 는 날짜 단위이므로 하루 여유를 두고 필터. 시간 단위 필터는 internaldate 로 사후 수행.
    now = datetime.now()
    since_date = now - timedelta(minutes=within_minutes) - timedelta(days=1)
    cutoff = now - timedelta(minutes=within_minutes)

    logger.info("인증번호 조회 시작 (sender=%s, within_minutes=%d)", sender, within_minutes)

    with _imap_session(
        server, int(port), email_addr, password, timeout=timeout
    ) as client:
        client.select("INBOX", readonly=True)

        criteria = _build_search_criteria(sender, since_date)
        status, data = client.search(None, *criteria)
        if status != "OK":
            logger.warning("IMAP search 실패: status=%s", status)
            return None

        # data[0] 는 공백 구분 UID 문자열 (bytes)
        raw_ids = data[0] if data else b""
        if not raw_ids:
            logger.info("조건에 맞는 메일 없음")
            return None

        ids = raw_ids.split()
        # 최신순으로 순회 (IMAP 은 오름차순 ID → 뒤집어 사용)
        for mail_id in reversed(ids):
            status, msg_data = client.fetch(mail_id, "(RFC822)")
            if status != "OK" or not msg_data:
                continue

            # msg_data 는 [(b'1 (RFC822 {size}', b'<raw bytes>'), b')'] 형태
            raw_bytes: Optional[bytes] = None
            for part in msg_data:
                if (
                    isinstance(part, tuple)
                    and len(part) >= 2
                    and isinstance(part[1], (bytes, bytearray))
                ):
                    raw_bytes = bytes(part[1])
                    break
            if raw_bytes is None:
                continue

            msg = email.message_from_bytes(raw_bytes)

            # internaldate 기반 시간 필터 (within_minutes 정밀 적용)
            date_header = msg.get("Date")
            if date_header:
                try:
                    received = email.utils.parsedate_to_datetime(date_header)
                    # naive/aware 정규화
                    if received.tzinfo is not None:
                        received = received.astimezone().replace(tzinfo=None)
                    if received < cutoff:
                        continue
                except Exception:  # noqa: BLE001 - 파싱 실패 시 통과시킴
                    pass

            subject = _decode_mime_header(msg.get("Subject"))
            body = _extract_text_parts(msg)
            haystack = f"{subject}\n{body}"

            match = pattern.search(haystack)
            if match:
                code = match.group(0)
                logger.info("인증번호 추출 성공 (len=%d)", len(code))
                return code

        logger.info("메일은 있었으나 6~8자리 숫자 매치 없음")
        return None


__all__ = ["fetch_verification_code"]
