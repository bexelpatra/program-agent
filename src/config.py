"""
config.py - 프로젝트 설정 및 상수 정의

네이버증권 금융 지표 크롤러의 설정값을 관리한다.
"""

import os

# === 프로젝트 경로 ===
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# === 데이터베이스 ===
DB_PATH = os.path.join(PROJECT_ROOT, "data", "market_data.db")

# === 크롤링 URL ===
EXCHANGE_RATE_URL = "https://finance.naver.com/marketindex/"
WORLD_INDEX_URL = "https://finance.naver.com/world/"

# === HTTP 요청 설정 ===
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
REQUEST_TIMEOUT = 10  # seconds

# === 크롤링 대상: 환율 ===
TARGET_CURRENCIES = [
    "USD",  # 미국 달러
    "EUR",  # 유로
    "JPY",  # 일본 엔
    "CNY",  # 중국 위안
]

# === 크롤링 대상: 세계 지수 ===
TARGET_INDICES = [
    "코스피",
    "코스닥",
    "나스닥",
    "S&P 500",
    "다우존스",
    "니케이225",
    "상해종합",
    "항셍",
]
