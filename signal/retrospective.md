# Retrospective

## 프로젝트 요약
- 이름: Asset Price Tracker & Analyzer
- 태스크 수: 7개 (첫 시도 성공: 7, 재시도 필요: 0)
- 세션 수: 1
- 테스트: 85개 전체 통과 (1.01초)

## 잘 된 점
- 모든 태스크가 첫 시도에 성공 — 설계 단계에서 충분히 논의한 효과
- 병렬 실행 효율적 활용 (TASK-002+003, TASK-005+006+007)
- 병렬 report 파일 분리로 충돌 없이 진행
- 플러그인 아키텍처(BaseStrategy)가 깔끔하게 구현됨
- 백테스터의 성과 지표 7종 + 벤치마크 비교가 완성도 높음

## 문제점
- TASK-006 Tester가 _normalize_dataframe()의 방어적 코딩 부족을 발견 (close 컬럼 완전 부재 시 KeyError). 사소하지만 collector 안정성에 영향 가능.
- pandas 1.x 호환 경고 발생 (clickhouse-connect). 실행에는 영향 없으나 향후 pandas 버전 업그레이드 권장.

## 파이프라인 개선 제안

### 제안 1: Tester 발견 이슈 자동 태스크화
- 대상 파일: CLAUDE.md (오케스트레이션 루프 Step 4)
- 현재: Tester가 발견한 코드 이슈는 report에만 기록되고, Manager가 수동으로 판단
- 제안: Tester report에 `## 코드 이슈` 섹션이 있고 내용이 있으면, Manager가 자동으로 수정 태스크를 생성하여 Coder에게 할당하는 규칙 추가
- 이유: 이번에도 _normalize_dataframe 이슈가 발견되었지만 별도 수정 태스크가 생성되지 않았음. 테스트에서 발견한 이슈가 누락되지 않도록.

### 제안 2: requirements.txt 검증 태스크 자동 추가
- 대상 파일: CLAUDE.md (태스크 분해 규칙)
- 현재: 의존성 설치 및 검증은 암묵적으로 진행
- 제안: TASK-001 이후에 `pip install -r requirements.txt && python -c "import src"` 같은 의존성 검증 단계를 표준화
- 이유: 이번에는 모든 패키지가 이미 설치되어 있었지만, 새 환경에서는 설치 실패가 발생할 수 있음
