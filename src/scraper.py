"""
scraper.py - 네이버증권 크롤링 모듈

aiohttp + BeautifulSoup4 + lxml을 사용하여
네이버증권에서 환율과 세계 지수를 크롤링한다.
"""

import json
import logging
import re

import aiohttp
from bs4 import BeautifulSoup

from config import (
    EXCHANGE_RATE_URL,
    REQUEST_TIMEOUT,
    TARGET_CURRENCIES,
    TARGET_INDICES,
    USER_AGENT,
    WORLD_INDEX_URL,
)

logger = logging.getLogger(__name__)

# 환율 페이지의 통화 코드 → CSS 클래스 매핑
# 네이버 환율 페이지에서 각 통화의 <a> 태그에 부여된 클래스명
_CURRENCY_CLASS_MAP = {
    "USD": "usd",
    "EUR": "eur",
    "JPY": "jpy",
    "CNY": "cny",
}

# 세계 지수 페이지의 TARGET_INDICES 한글명 → JS 데이터의 knam 매핑
# (일부 이름이 다를 수 있으므로 유연하게 매칭)
_INDEX_KNAM_MAP = {
    "코스피": "코스피",
    "나스닥": "나스닥 종합",
    "S&P 500": "S&P 500",
    "다우존스": "다우 산업",
    "니케이225": "니케이225",
    "상해종합": "상해종합",
    "항셍": "항셍",
}

# 코스닥은 세계지수 페이지에 포함되지 않으므로 별도 페이지에서 크롤링한다
_KOSDAQ_URL = "https://finance.naver.com/sise/sise_index.naver?code=KOSDAQ"


async def _fetch_html(url: str) -> str | None:
    """주어진 URL에서 HTML을 가져온다.

    Args:
        url: 요청할 URL

    Returns:
        HTML 문자열. 실패 시 None.
    """
    timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
    headers = {"User-Agent": USER_AGENT}

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                # 네이버증권은 EUC-KR 인코딩을 사용한다
                raw = await response.read()
                return raw.decode("euc-kr", errors="replace")
    except Exception as e:
        logger.error("HTML 가져오기 실패 (%s): %s", url, e)
        return None


def _parse_direction(class_list: list[str]) -> int:
    """head_info div의 CSS 클래스에서 등락 방향을 판별한다.

    point_up → +1 (상승), point_dn → -1 (하락), 그 외 → 0 (보합)
    """
    if "point_up" in class_list:
        return 1
    elif "point_dn" in class_list:
        return -1
    return 0


def _parse_number(text: str) -> float:
    """숫자 문자열에서 쉼표를 제거하고 float으로 변환한다."""
    if not text:
        return 0.0
    cleaned = text.strip().replace(",", "").replace(" ", "")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


async def fetch_exchange_rates() -> list[dict]:
    """네이버증권 환율 페이지에서 주요 환율을 크롤링한다.

    HTML 구조:
        div.market_include > div.market_data > div.market1 > ul#exchangeList > li
        각 li 안에:
          - a.head.{통화코드소문자} (예: a.head.usd)
            - h3.h_lst > span.blind : 통화명
            - div.head_info.point_up|point_dn
              - span.value : 환율 값
              - span.change : 변동값

    Returns:
        list[dict]: 각 dict는 {currency, rate, change_value, change_percent} 형태.
        에러 발생 시 빈 리스트 반환.
    """
    html = await _fetch_html(EXCHANGE_RATE_URL)
    if html is None:
        return []

    try:
        soup = BeautifulSoup(html, "lxml")
        exchange_list = soup.find("ul", id="exchangeList")
        if not exchange_list:
            logger.error("exchangeList를 찾을 수 없음")
            return []

        results = []
        items = exchange_list.find_all("li")

        for item in items:
            a_tag = item.find("a", class_="head")
            if not a_tag:
                continue

            # 통화 코드 판별: a 태그의 class에서 통화 클래스를 찾는다
            a_classes = a_tag.get("class", [])
            currency_code = None
            for code, css_class in _CURRENCY_CLASS_MAP.items():
                if css_class in a_classes:
                    currency_code = code
                    break

            if currency_code is None:
                continue

            if currency_code not in TARGET_CURRENCIES:
                continue

            # 환율 값 추출
            head_info = a_tag.find("div", class_="head_info")
            if not head_info:
                continue

            value_span = head_info.find("span", class_="value")
            change_span = head_info.find("span", class_="change")

            rate = _parse_number(value_span.get_text()) if value_span else 0.0
            change_val = _parse_number(change_span.get_text()) if change_span else 0.0

            # 등락 방향 반영
            direction = _parse_direction(head_info.get("class", []))
            change_val = abs(change_val) * direction

            # 변동률 계산 (환율 페이지에는 변동률이 직접 표시되지 않으므로 계산)
            if rate != 0:
                # 전일 종가 = 현재 환율 - 변동값
                prev_rate = rate - change_val
                change_pct = (change_val / prev_rate * 100) if prev_rate != 0 else 0.0
            else:
                change_pct = 0.0

            results.append(
                {
                    "currency": currency_code,
                    "rate": rate,
                    "change_value": round(change_val, 2),
                    "change_percent": round(change_pct, 2),
                }
            )

        logger.info("환율 크롤링 완료: %d건", len(results))
        return results

    except Exception as e:
        logger.error("환율 파싱 실패: %s", e)
        return []


async def _fetch_kosdaq_index() -> dict | None:
    """네이버증권 국내 시세 페이지에서 코스닥 지수를 크롤링한다.

    코스닥은 세계지수 페이지(finance.naver.com/world/)에 포함되지 않으므로
    별도의 국내 시세 페이지에서 가져온다.

    HTML 구조:
        div#quotient > em#now_value : 현재값
        span#change_value_and_rate > span : 변동값, 변동률(%)

    Returns:
        dict | None: {index_name, country, value, change_value, change_percent} 또는 None.
    """
    html = await _fetch_html(_KOSDAQ_URL)
    if html is None:
        return None

    try:
        soup = BeautifulSoup(html, "lxml")

        # 현재값: <em id="now_value">1,146.28</em>
        now_value_el = soup.find("em", id="now_value")
        if not now_value_el:
            logger.warning("코스닥 now_value를 찾을 수 없음")
            return None

        value = _parse_number(now_value_el.get_text())

        # 변동값 및 변동률: <span id="change_value_and_rate"><span>24.84</span> +2.22%</span>
        change_el = soup.find("span", id="change_value_and_rate")
        change_val = 0.0
        change_pct = 0.0

        if change_el:
            # 변동값은 내부 첫 번째 <span>에 있다
            inner_span = change_el.find("span")
            if inner_span:
                change_val = _parse_number(inner_span.get_text())

            # 변동률은 전체 텍스트에서 %가 포함된 부분을 추출
            full_text = change_el.get_text()
            pct_match = re.search(r"([+-]?\d+\.?\d*)%", full_text)
            if pct_match:
                change_pct = float(pct_match.group(1))

            # 등락 방향 판별: 부모 div#quotient의 class에 "dn"이 있으면 하락
            quotient_div = soup.find("div", id="quotient")
            if quotient_div:
                q_classes = quotient_div.get("class", [])
                if any("dn" in c for c in q_classes):
                    change_val = -abs(change_val)
                    change_pct = -abs(change_pct)
                elif any("up" in c for c in q_classes):
                    change_val = abs(change_val)
                    change_pct = abs(change_pct)

        return {
            "index_name": "코스닥",
            "country": "한국",
            "value": value,
            "change_value": round(change_val, 2),
            "change_percent": round(change_pct, 2),
        }

    except Exception as e:
        logger.error("코스닥 파싱 실패: %s", e)
        return None


async def fetch_market_indices() -> list[dict]:
    """네이버증권에서 주요 세계 지수를 크롤링한다.

    세계지수 페이지(finance.naver.com/world/)의 JavaScript 변수
    (americaData, asiaData, europeAfricaData)에서 JSON 데이터를 추출하고,
    코스닥은 별도 국내 시세 페이지에서 가져온다.

    각 지수 항목의 JSON 구조:
        {
            "knam": "나스닥 종합",
            "natcKnam": "미국",
            "last": 21761.89,
            "diff": -184.87,
            "rate": -0.84,
            "symb": "NAS@IXIC",
            ...
        }

    Returns:
        list[dict]: 각 dict는 {index_name, country, value, change_value, change_percent} 형태.
        에러 발생 시 빈 리스트 반환.
    """
    html = await _fetch_html(WORLD_INDEX_URL)
    if html is None:
        return []

    try:
        # JavaScript 변수에서 JSON 데이터 추출
        # 패턴: var americaData = jindo.$H({...});
        pattern = re.compile(
            r"var\s+(?:americaData|asiaData|europeAfricaData)\s*="
            r"\s*jindo\.\$H\((\{.*?\})\);",
            re.DOTALL,
        )

        all_indices: dict[str, dict] = {}
        for match in pattern.finditer(html):
            try:
                data = json.loads(match.group(1))
                all_indices.update(data)
            except json.JSONDecodeError as e:
                logger.warning("JSON 파싱 실패: %s", e)
                continue

        if not all_indices:
            logger.error("세계지수 데이터를 찾을 수 없음")
            return []

        # TARGET_INDICES에 해당하는 지수만 추출
        results = []
        for target_name in TARGET_INDICES:
            # 코스닥은 별도로 처리
            if target_name == "코스닥":
                continue

            knam_to_find = _INDEX_KNAM_MAP.get(target_name, target_name)

            found = False
            for _symb, info in all_indices.items():
                if info.get("knam") == knam_to_find:
                    results.append(
                        {
                            "index_name": target_name,
                            "country": info.get("natcKnam", ""),
                            "value": float(info.get("last", 0)),
                            "change_value": round(float(info.get("diff", 0)), 2),
                            "change_percent": round(float(info.get("rate", 0)), 2),
                        }
                    )
                    found = True
                    break

            if not found:
                logger.warning("지수를 찾을 수 없음: %s (knam=%s)", target_name, knam_to_find)

        # 코스닥을 별도 페이지에서 크롤링하여 추가
        if "코스닥" in TARGET_INDICES:
            kosdaq = await _fetch_kosdaq_index()
            if kosdaq:
                results.append(kosdaq)
            else:
                logger.warning("코스닥 크롤링 실패")

        logger.info("세계지수 크롤링 완료: %d건", len(results))
        return results

    except Exception as e:
        logger.error("세계지수 파싱 실패: %s", e)
        return []
