"""naver_imap.fetch_verification_code 단위 테스트.

네트워크 I/O 가 포함된 모듈이므로 imaplib.IMAP4_SSL 을 mock 으로
치환한다. 실제 Naver 서버에 접속하지 않는다.

실행:
    python3 -m unittest projects.web-automation.tests.test_naver_imap
    # 또는 pytest 있으면:
    pytest projects/web-automation/tests/test_naver_imap.py -v
"""

from __future__ import annotations

import email
import sys
import unittest
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from unittest.mock import MagicMock, patch

# 프로젝트 src 를 import path 에 추가 (pytest/unittest 양쪽 지원)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.auth.naver_imap import fetch_verification_code  # noqa: E402


# ---------------------------------------------------------------------------
# 헬퍼
# ---------------------------------------------------------------------------


def _make_config(
    server: str = "imap.naver.com",
    port: int = 993,
    email_addr: str = "tester@naver.com",
    password: str = "app-password",
):
    """Config 최소 모킹 객체. get(key, default=None) 만 지원한다.

    신규 규약: IMAP 접속용 naver_imap.email / naver_imap.password 사용.
    """
    values = {
        "naver_imap.server": server,
        "naver_imap.port": port,
        "naver_imap.email": email_addr,
        "naver_imap.password": password,
    }
    cfg = MagicMock()
    cfg.get.side_effect = lambda key, default=None: values.get(key, default)
    return cfg


def _build_mail_bytes(
    subject: str,
    body: str,
    sender: str = "noreply@kakaocorp.com",
    receiver: str = "tester@naver.com",
    date: datetime | None = None,
) -> bytes:
    """테스트용 메일 RFC822 바이트를 생성한다.

    최근 시각을 기본값으로 두어 within_minutes 필터를 통과하게 한다.
    """
    if date is None:
        date = datetime.now(timezone.utc).astimezone()

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    msg["Date"] = email.utils.format_datetime(date)
    msg.set_content(body)
    return msg.as_bytes()


def _make_mock_imap(search_ids: list[bytes], mails: dict[bytes, bytes]) -> MagicMock:
    """imaplib.IMAP4_SSL 을 흉내내는 MagicMock 을 만든다.

    Args:
        search_ids: search() 가 반환할 UID 리스트 (오름차순 기대)
        mails: UID → RFC822 바이트 매핑
    """
    mock_client = MagicMock()
    mock_client.login.return_value = ("OK", [b"Logged in"])
    mock_client.select.return_value = ("OK", [b"1"])

    joined = b" ".join(search_ids) if search_ids else b""
    mock_client.search.return_value = ("OK", [joined])

    def _fetch(mail_id, parts):
        if mail_id in mails:
            return ("OK", [(b"%s (RFC822 {size}" % mail_id, mails[mail_id]), b")"])
        return ("NO", [None])

    mock_client.fetch.side_effect = _fetch
    mock_client.close.return_value = ("OK", [b"Closed"])
    mock_client.logout.return_value = ("BYE", [b"Logout"])
    return mock_client


# ---------------------------------------------------------------------------
# 테스트 케이스
# ---------------------------------------------------------------------------


class FetchVerificationCodeTests(unittest.TestCase):
    """fetch_verification_code 의 주요 분기를 검증한다."""

    def test_extracts_six_digit_code_from_body(self):
        """정상 케이스: 본문에 '인증번호는 123456 입니다' → '123456' 반환."""
        mail_bytes = _build_mail_bytes(
            subject="[티스토리] 로그인 인증번호 안내",
            body="인증번호는 123456 입니다. 5분 내로 입력해주세요.",
        )
        mock_client = _make_mock_imap(search_ids=[b"1"], mails={b"1": mail_bytes})

        with patch("src.auth.naver_imap.imaplib.IMAP4_SSL", return_value=mock_client):
            code = fetch_verification_code(
                _make_config(),
                sender="noreply@tistory.com",
                within_minutes=5,
            )

        self.assertEqual(code, "123456")
        mock_client.login.assert_called_once()
        mock_client.select.assert_called_once_with("INBOX", readonly=True)
        # FROM 필터가 실제로 전달되었는지 확인
        args, _ = mock_client.search.call_args
        self.assertIn("FROM", args)
        self.assertIn("noreply@tistory.com", args)
        # logout 이 반드시 호출되어야 함
        mock_client.logout.assert_called_once()

    def test_returns_none_when_no_mail_matches(self):
        """메일 없음: search() 빈 결과 → None 반환."""
        mock_client = _make_mock_imap(search_ids=[], mails={})

        with patch("src.auth.naver_imap.imaplib.IMAP4_SSL", return_value=mock_client):
            code = fetch_verification_code(
                _make_config(),
                sender="noreply@tistory.com",
                within_minutes=5,
            )

        self.assertIsNone(code)
        mock_client.fetch.assert_not_called()
        mock_client.logout.assert_called_once()

    def test_returns_none_when_no_six_to_eight_digit_match(self):
        """6~8자리 숫자가 없는 메일: 전화번호 '02-1234-5678' 같은 하이픈 분리 숫자만 존재 → None.

        \\b\\d{6,8}\\b 는 단어 경계 기반이므로 하이픈이 경계로 작동,
        '1234' / '5678' / '2345' / '6789' 모두 4자리라서 6자리 최소 조건을 못 채움.
        """
        mail_bytes = _build_mail_bytes(
            subject="안내 메일",
            body="문의는 02-1234-5678 또는 010-2345-6789 로 연락주세요.",
        )
        mock_client = _make_mock_imap(search_ids=[b"1"], mails={b"1": mail_bytes})

        with patch("src.auth.naver_imap.imaplib.IMAP4_SSL", return_value=mock_client):
            code = fetch_verification_code(
                _make_config(),
                sender="noreply@kakaocorp.com",
                within_minutes=5,
            )

        self.assertIsNone(code)
        mock_client.logout.assert_called_once()

    def test_picks_latest_mail_among_multiple(self):
        """여러 메일이 있을 때 최신(UID 큰 값)에서 먼저 추출한다."""
        old_mail = _build_mail_bytes(subject="예전 인증", body="인증번호는 111111 입니다.")
        new_mail = _build_mail_bytes(subject="최신 인증", body="인증번호는 999999 입니다.")
        mock_client = _make_mock_imap(
            search_ids=[b"1", b"2"],
            mails={b"1": old_mail, b"2": new_mail},
        )

        with patch("src.auth.naver_imap.imaplib.IMAP4_SSL", return_value=mock_client):
            code = fetch_verification_code(
                _make_config(),
                sender="noreply@tistory.com",
                within_minutes=5,
            )

        # 최신 메일(UID 2) 이 먼저 조회되어 999999 가 반환되어야 함
        self.assertEqual(code, "999999")

    def test_raises_when_config_missing_password(self):
        """Config 에 naver_imap.password 가 없으면 ValueError 발생."""
        cfg = _make_config(password="")  # 빈 문자열 → falsy

        with self.assertRaises(ValueError):
            fetch_verification_code(
                cfg, sender="noreply@kakaocorp.com", within_minutes=5
            )

    def test_extracts_eight_digit_kakao_code(self):
        """실측 카카오 인증번호(8자리) 추출: 본문의 '55898679' 를 그대로 반환한다."""
        mail_bytes = _build_mail_bytes(
            subject="[Kakao] 로그인 인증번호",
            body="인증번호는 55898679 입니다. 5분 내로 입력해주세요.",
            sender="noreply@kakaocorp.com",
        )
        mock_client = _make_mock_imap(search_ids=[b"1"], mails={b"1": mail_bytes})

        with patch("src.auth.naver_imap.imaplib.IMAP4_SSL", return_value=mock_client):
            code = fetch_verification_code(
                _make_config(),
                sender="noreply@kakaocorp.com",
                within_minutes=5,
            )

        self.assertEqual(code, "55898679")
        mock_client.logout.assert_called_once()


if __name__ == "__main__":
    unittest.main()
