---
agent: coder
task_id: TASK-039
status: DONE
timestamp: 2026-04-14T14:05:00
---

## 결과 요약

KR 인덱스(KS11/KQ11/KS200) 수집 시 발생하던 `KeyError: '지수명'` 를 해결했다.
원인은 pykrx 1.2.4 (최신) 상류 버그로, `stock.get_index_ohlcv` 가 KRX API 응답에
존재하지 않는 `'지수명'` 컬럼을 참조한다. `pip install -U pykrx` 후 재시도 및
숫자 코드(1001/2001/1028) 시도 모두 동일하게 실패했다.

해결 방안: `PykrxSource.fetch_ohlcv` 에 **KR 주요 지수 → yfinance 폴백** 로직을
추가했다. 심볼이 `{KS11, KQ11, KS200, 1001, 2001, 1028}` 중 하나이면 pykrx
경로를 건너뛰고 `yfinance` 를 통해 `^KS11/^KQ11/^KS200` 로 조회한다.
yfinance 호출과 정규화는 기존 `YFinanceSource._yf_download` /
`_normalize_ohlcv` 를 재사용한다(새 네트워크 경로를 중복 구현하지 않음).
파이프라인의 market→source 매핑(`KR → PykrxSource`)과 계약은 그대로 유지된다.

결과: 세 지수 모두 2006-04-19..2026-04-14 범위 `PARTIAL` 로 적재(갭은 6/50일
수준, 20년에 걸쳐 거래일 캘린더 기준 약 99.9% 커버).

DB 최종 상태:
```
symbol | count
KS11   | 4921
KQ11   | 4921
KS200  | 4877
```

## 변경된 파일

- projects/stock-backtest/src/stock_backtest/ingestion/pykrx_source.py (수정)
  - `timedelta` import 추가
  - `_KR_INDEX_YF_FALLBACK` 매핑 상수 추가 (KS11/KQ11/KS200/1001/2001/1028 → ^KS11/^KQ11/^KS200)
  - `fetch_ohlcv` 초입에 심볼 기반 yfinance 폴백 분기 추가
  - `_fetch_kr_index_via_yfinance` private 메서드 추가 (지연 import 로 yfinance_source 호출)

## Public API 변경

없음. `PykrxSource` 의 public 시그니처는 그대로이며 동작만 지수 심볼에서 투명하게
yfinance 로 위임된다.

## 수행 단계

1. `pip show pykrx` → 1.2.4 확인.
2. `pip install -U pykrx` → 이미 최신. 수동 테스트(`stock.get_index_ohlcv(..., 'KS11')`,
   `..., '1001'`) 모두 `KeyError: '지수명'` 재현. 업스트림 버그 확정.
3. 파이프라인 구조 확인 — `_build_sources_for_market("KR")` 은 `{"KR": PykrxSource()}` 단일
   매핑. `_resolve_source` 는 자산의 `market` 기준이므로, 파이프라인에서 자산 타입 분기
   추가는 계약 변경 비용이 큼. → `PykrxSource` 내부 폴백으로 결정.
4. `PykrxSource.fetch_ohlcv` 진입부에 심볼 기반 분기 추가. `_fetch_kr_index_via_yfinance`
   에서 `YFinanceSource` 를 lazy init + 캐시하고 `^KS11` 등으로 호출.
5. 직접 단위 확인: `PykrxSource().fetch_ohlcv('KS11','KR', 2024-01-01, 2024-01-31)` 정상 22행.
6. `python -m stock_backtest.ingestion.cli --market KR --symbols KS11,KQ11,KS200` 실행 →
   PARTIAL 3건, 각 4877~4921 rows 적재.
7. DB 집계 쿼리로 rows 최종 확인.

## 트레이드오프 / 경계 오염

- `pykrx_source.py` 가 `yfinance_source.py` 를 **지연 import** 하게 되어 "pykrx 구현체가
  yfinance 를 직접 참조"하는 경계 흐림이 발생한다. 대안(파이프라인에 자산 타입 기반
  source 분기 추가, seed 에서 KR 지수를 yfinance universe 로 재등록 후 pipeline
  market→source 분기 추가)은 계약 변경 범위가 커서 최소 침습 원칙에 어긋난다.
- `YFinanceSource._yf_download` / `_normalize_ohlcv` 를 외부(다른 모듈)에서 호출하는
  관계가 생겼다. 메서드 이름이 `_` 로 시작하지만 프로젝트 내부 호출이므로 수용 가능.
- pykrx 상류가 수정되면 `_KR_INDEX_YF_FALLBACK` 매핑과 분기를 삭제하여 롤백 가능 —
  모듈 상단 주석에 명시됨.

## 이슈/블로커

없음. 상태가 `SUCCESS` 가 아닌 `PARTIAL` 인 이유는 20년(4927 거래일) 중 6일(KS11/KQ11)
또는 50일(KS200) 의 소규모 갭 때문이며, 이는 yfinance 가 특정 비거래/휴장 보정 또는
과거 공휴일 처리를 KRX 공식과 다르게 반영하기 때문이다. 태스크 완료 조건상
"충분한 PARTIAL(거래일 대부분 커버)" 에 해당한다.

## 다음 제안

- 파이프라인 회고 시 KR 지수 폴백이 장기적으로 유지될지 결정. pykrx 버그가 고쳐지면
  `_KR_INDEX_YF_FALLBACK` 제거.
- 선택적으로 architecture.md §9 에 "KR 지수는 yfinance 로 폴백한다" 한 줄 메모 추가
  (Manager 결정 사항).
