"""e2e 페르소나 + Failure replay harness (TASK-202).

비개발자 첫 사용 시나리오와 2026-04-29 사고 (weights 에 ticker symbol 직접 입력)
회귀 박제. 가동 중인 서버 (systemctl --user quant-lab-{backend,frontend}) 가정,
미가동 시 SOFT skip.
"""
