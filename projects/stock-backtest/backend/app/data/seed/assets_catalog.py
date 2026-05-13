"""자산 카탈로그 시드 데이터.

architecture.md V3 § "자산 카탈로그 + 사용자 자유 추가" (L528-533) 의 큐레이션 카탈로그.

- KR: pykrx 가 처리 가능한 한국거래소 등록 ETF (6자리 ticker). kr_tax_class meta 부착.
- US: yfinance 처리 가능 ticker. 광역 지수 / 채권 / 원자재 / 부동산 / 해외 분산.
- CRYPTO: yfinance 의 "XXX-USD" 포맷.

- name 은 한글 우선 (UI/UX 원칙 2: 비개발자 친화). 미국 자산은 영어 공식명 + 한글 부가설명 어색하면 영어 유지.
- meta JSONB 는 KR 자산에서 kr_tax_class ("domestic_equity" / "overseas_equity" / "bond" / "commodity") 표기.
  Phase 2 세금 계산기 도입 시 활용 예정.
"""
from typing import Literal, TypedDict

Market = Literal["KR", "US", "CRYPTO"]
# STOCK = Phase 2 테마주 트랙 (개별주) — domain.asset.entity / schemas.asset 과 1:1 동기.
AssetType = Literal["EQUITY_INDEX", "ETF", "BOND", "COMMODITY", "CRYPTO", "STOCK"]


class SeedAsset(TypedDict):
    """단일 카탈로그 자산 행. Asset 모델 (backend/app/models/asset.py) 컬럼과 1:1 대응."""

    symbol: str
    market: Market
    asset_type: AssetType
    currency: str
    name: str
    meta: dict


# fmt: off
CATALOG: list[SeedAsset] = [
    # =========================================================================
    # KR — 한국거래소 상장 ETF (총 20개)
    # =========================================================================
    # --- 국내 주식형 (kr_tax_class=domestic_equity, 매매차익 비과세) ---
    {"symbol": "069500", "market": "KR", "asset_type": "ETF", "currency": "KRW", "name": "KODEX 200", "meta": {"kr_tax_class": "domestic_equity"}},
    {"symbol": "102110", "market": "KR", "asset_type": "ETF", "currency": "KRW", "name": "TIGER 200", "meta": {"kr_tax_class": "domestic_equity"}},
    {"symbol": "148020", "market": "KR", "asset_type": "ETF", "currency": "KRW", "name": "KBSTAR 200", "meta": {"kr_tax_class": "domestic_equity"}},
    {"symbol": "278530", "market": "KR", "asset_type": "ETF", "currency": "KRW", "name": "KODEX 200TR", "meta": {"kr_tax_class": "domestic_equity"}},
    {"symbol": "229200", "market": "KR", "asset_type": "ETF", "currency": "KRW", "name": "KODEX 코스닥150", "meta": {"kr_tax_class": "domestic_equity"}},
    {"symbol": "232080", "market": "KR", "asset_type": "ETF", "currency": "KRW", "name": "TIGER 코스닥150", "meta": {"kr_tax_class": "domestic_equity"}},
    {"symbol": "117460", "market": "KR", "asset_type": "ETF", "currency": "KRW", "name": "KODEX 에너지화학", "meta": {"kr_tax_class": "domestic_equity"}},
    {"symbol": "091160", "market": "KR", "asset_type": "ETF", "currency": "KRW", "name": "KODEX 반도체", "meta": {"kr_tax_class": "domestic_equity"}},
    # --- 해외 주식형 (kr_tax_class=overseas_equity, 매매차익 배당소득세 15.4%) ---
    {"symbol": "360750", "market": "KR", "asset_type": "ETF", "currency": "KRW", "name": "TIGER 미국S&P500", "meta": {"kr_tax_class": "overseas_equity"}},
    {"symbol": "379800", "market": "KR", "asset_type": "ETF", "currency": "KRW", "name": "KODEX 미국S&P500TR", "meta": {"kr_tax_class": "overseas_equity"}},
    {"symbol": "381180", "market": "KR", "asset_type": "ETF", "currency": "KRW", "name": "TIGER 미국필라델피아반도체나스닥", "meta": {"kr_tax_class": "overseas_equity"}},
    {"symbol": "133690", "market": "KR", "asset_type": "ETF", "currency": "KRW", "name": "TIGER 미국나스닥100", "meta": {"kr_tax_class": "overseas_equity"}},
    {"symbol": "192090", "market": "KR", "asset_type": "ETF", "currency": "KRW", "name": "TIGER 차이나CSI300", "meta": {"kr_tax_class": "overseas_equity"}},
    # --- 채권형 (kr_tax_class=bond) ---
    {"symbol": "148070", "market": "KR", "asset_type": "BOND", "currency": "KRW", "name": "KOSEF 국고채10년", "meta": {"kr_tax_class": "bond"}},
    {"symbol": "114820", "market": "KR", "asset_type": "BOND", "currency": "KRW", "name": "TIGER 국채3년", "meta": {"kr_tax_class": "bond"}},
    {"symbol": "153130", "market": "KR", "asset_type": "BOND", "currency": "KRW", "name": "KODEX 단기채권", "meta": {"kr_tax_class": "bond"}},
    {"symbol": "136340", "market": "KR", "asset_type": "BOND", "currency": "KRW", "name": "KBSTAR 중기우량회사채", "meta": {"kr_tax_class": "bond"}},
    # --- 원자재 (kr_tax_class=commodity) ---
    {"symbol": "132030", "market": "KR", "asset_type": "COMMODITY", "currency": "KRW", "name": "KODEX 골드선물(H)", "meta": {"kr_tax_class": "commodity"}},
    {"symbol": "130680", "market": "KR", "asset_type": "COMMODITY", "currency": "KRW", "name": "TIGER 원유선물Enhanced(H)", "meta": {"kr_tax_class": "commodity"}},
    {"symbol": "139660", "market": "KR", "asset_type": "COMMODITY", "currency": "KRW", "name": "KODEX 미국채울트라30년선물(H)", "meta": {"kr_tax_class": "bond"}},

    # =========================================================================
    # US — 미국 시장 ETF (총 35개)
    # =========================================================================
    # --- 광역 지수 ---
    {"symbol": "SPY", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "SPDR S&P 500 ETF Trust", "meta": {}},
    {"symbol": "VOO", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "Vanguard S&P 500 ETF", "meta": {}},
    {"symbol": "IVV", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "iShares Core S&P 500 ETF", "meta": {}},
    {"symbol": "QQQ", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "Invesco QQQ Trust (나스닥100)", "meta": {}},
    {"symbol": "VTI", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "Vanguard Total Stock Market ETF", "meta": {}},
    {"symbol": "IWM", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "iShares Russell 2000 ETF", "meta": {}},
    {"symbol": "DIA", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "SPDR Dow Jones Industrial Average ETF", "meta": {}},
    # --- 섹터 (대표 일부) ---
    {"symbol": "XLK", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "Technology Select Sector SPDR", "meta": {}},
    {"symbol": "XLF", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "Financial Select Sector SPDR", "meta": {}},
    {"symbol": "XLE", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "Energy Select Sector SPDR", "meta": {}},
    {"symbol": "XLV", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "Health Care Select Sector SPDR", "meta": {}},
    {"symbol": "SOXX", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "iShares Semiconductor ETF", "meta": {}},
    # --- 채권 ---
    {"symbol": "TLT", "market": "US", "asset_type": "BOND", "currency": "USD", "name": "iShares 20+ Year Treasury Bond ETF", "meta": {}},
    {"symbol": "IEF", "market": "US", "asset_type": "BOND", "currency": "USD", "name": "iShares 7-10 Year Treasury Bond ETF", "meta": {}},
    {"symbol": "SHY", "market": "US", "asset_type": "BOND", "currency": "USD", "name": "iShares 1-3 Year Treasury Bond ETF", "meta": {}},
    {"symbol": "AGG", "market": "US", "asset_type": "BOND", "currency": "USD", "name": "iShares Core U.S. Aggregate Bond ETF", "meta": {}},
    {"symbol": "BND", "market": "US", "asset_type": "BOND", "currency": "USD", "name": "Vanguard Total Bond Market ETF", "meta": {}},
    {"symbol": "TIP", "market": "US", "asset_type": "BOND", "currency": "USD", "name": "iShares TIPS Bond ETF (인플레이션 연동)", "meta": {}},
    {"symbol": "LQD", "market": "US", "asset_type": "BOND", "currency": "USD", "name": "iShares iBoxx Investment Grade Corporate Bond ETF", "meta": {}},
    {"symbol": "HYG", "market": "US", "asset_type": "BOND", "currency": "USD", "name": "iShares iBoxx High Yield Corporate Bond ETF", "meta": {}},
    # --- 원자재 ---
    {"symbol": "GLD", "market": "US", "asset_type": "COMMODITY", "currency": "USD", "name": "SPDR Gold Trust", "meta": {}},
    {"symbol": "IAU", "market": "US", "asset_type": "COMMODITY", "currency": "USD", "name": "iShares Gold Trust", "meta": {}},
    {"symbol": "SLV", "market": "US", "asset_type": "COMMODITY", "currency": "USD", "name": "iShares Silver Trust", "meta": {}},
    {"symbol": "DBC", "market": "US", "asset_type": "COMMODITY", "currency": "USD", "name": "Invesco DB Commodity Index Tracking Fund", "meta": {}},
    {"symbol": "USO", "market": "US", "asset_type": "COMMODITY", "currency": "USD", "name": "United States Oil Fund", "meta": {}},
    {"symbol": "DBA", "market": "US", "asset_type": "COMMODITY", "currency": "USD", "name": "Invesco DB Agriculture Fund", "meta": {}},
    # --- 부동산 ---
    {"symbol": "VNQ", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "Vanguard Real Estate ETF", "meta": {}},
    {"symbol": "SCHH", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "Schwab U.S. REIT ETF", "meta": {}},
    # --- 해외 (선진국/신흥국) ---
    {"symbol": "VEA", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "Vanguard FTSE Developed Markets ETF", "meta": {}},
    {"symbol": "VWO", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "Vanguard FTSE Emerging Markets ETF", "meta": {}},
    {"symbol": "EFA", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "iShares MSCI EAFE ETF", "meta": {}},
    {"symbol": "EEM", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "iShares MSCI Emerging Markets ETF", "meta": {}},
    {"symbol": "ACWI", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "iShares MSCI ACWI ETF (전세계)", "meta": {}},
    {"symbol": "EWJ", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "iShares MSCI Japan ETF", "meta": {}},
    {"symbol": "MCHI", "market": "US", "asset_type": "ETF", "currency": "USD", "name": "iShares MSCI China ETF", "meta": {}},

    # =========================================================================
    # CRYPTO — yfinance "XXX-USD" 포맷 (총 12개)
    # =========================================================================
    {"symbol": "BTC-USD", "market": "CRYPTO", "asset_type": "CRYPTO", "currency": "USD", "name": "비트코인", "meta": {}},
    {"symbol": "ETH-USD", "market": "CRYPTO", "asset_type": "CRYPTO", "currency": "USD", "name": "이더리움", "meta": {}},
    {"symbol": "SOL-USD", "market": "CRYPTO", "asset_type": "CRYPTO", "currency": "USD", "name": "솔라나", "meta": {}},
    {"symbol": "XRP-USD", "market": "CRYPTO", "asset_type": "CRYPTO", "currency": "USD", "name": "리플", "meta": {}},
    {"symbol": "BNB-USD", "market": "CRYPTO", "asset_type": "CRYPTO", "currency": "USD", "name": "바이낸스코인", "meta": {}},
    {"symbol": "ADA-USD", "market": "CRYPTO", "asset_type": "CRYPTO", "currency": "USD", "name": "에이다", "meta": {}},
    {"symbol": "DOGE-USD", "market": "CRYPTO", "asset_type": "CRYPTO", "currency": "USD", "name": "도지코인", "meta": {}},
    {"symbol": "MATIC-USD", "market": "CRYPTO", "asset_type": "CRYPTO", "currency": "USD", "name": "폴리곤", "meta": {}},
    {"symbol": "DOT-USD", "market": "CRYPTO", "asset_type": "CRYPTO", "currency": "USD", "name": "폴카닷", "meta": {}},
    {"symbol": "AVAX-USD", "market": "CRYPTO", "asset_type": "CRYPTO", "currency": "USD", "name": "아발란체", "meta": {}},
    {"symbol": "LINK-USD", "market": "CRYPTO", "asset_type": "CRYPTO", "currency": "USD", "name": "체인링크", "meta": {}},
    {"symbol": "LTC-USD", "market": "CRYPTO", "asset_type": "CRYPTO", "currency": "USD", "name": "라이트코인", "meta": {}},
]
# fmt: on
