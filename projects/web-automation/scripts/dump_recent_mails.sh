#!/usr/bin/env bash
# Naver 메일함 최근 N개 메일의 from/subject/body를 출력한다.
# 사용법: ./scripts/dump_recent_mails.sh [개수, 기본 3]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

if [ ! -f ".env" ]; then
    echo "[ERROR] .env 없음. cp .env.example .env 후 값 채우기."
    exit 1
fi

set -a
# shellcheck disable=SC1091
source .env
set +a

N="${1:-3}"

python3 - <<PYEOF
import imaplib, email, sys
from email.header import decode_header

EMAIL = "${WA_ACCOUNT_EMAIL}"
PW = "${WA_ACCOUNT_PASSWORD}"
N = ${N}

def decode(s):
    if s is None:
        return ""
    parts = decode_header(s)
    out = []
    for txt, enc in parts:
        if isinstance(txt, bytes):
            out.append(txt.decode(enc or "utf-8", errors="replace"))
        else:
            out.append(txt)
    return "".join(out)

def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype in ("text/plain", "text/html"):
                payload = part.get_payload(decode=True)
                if payload:
                    charset = part.get_content_charset() or "utf-8"
                    return payload.decode(charset, errors="replace")
        return ""
    payload = msg.get_payload(decode=True)
    if payload is None:
        return ""
    charset = msg.get_content_charset() or "utf-8"
    return payload.decode(charset, errors="replace")

imap = imaplib.IMAP4_SSL("imap.naver.com", 993)
imap.login(EMAIL, PW)
imap.select("INBOX")

typ, data = imap.search(None, "ALL")
ids = data[0].split()
recent = ids[-N:][::-1]  # 최신순

print(f"=== 최근 {len(recent)}개 메일 ===\n")
for idx, mid in enumerate(recent, 1):
    typ, msg_data = imap.fetch(mid, "(RFC822)")
    msg = email.message_from_bytes(msg_data[0][1])
    print(f"--- [{idx}] ---")
    print(f"From   : {decode(msg.get('From'))}")
    print(f"Subject: {decode(msg.get('Subject'))}")
    print(f"Date   : {msg.get('Date')}")
    body = get_body(msg)
    # 앞부분 1000자만 보여준다 (HTML 길면 시끄러움)
    preview = body[:1000]
    print(f"Body (first 1000 chars):\n{preview}")
    print()

imap.logout()
PYEOF
