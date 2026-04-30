"""e2e 테스트 전용 fixture (TASK-202).

서버 가동(systemctl --user quant-lab-backend.service / quant-lab-frontend.service)을
가정한다. 각 테스트 모듈이 자기 fixture (backend_alive / frontend_alive) 로 SOFT skip
하므로 여기서는 별도 공통 fixture 를 두지 않는다.

상위 backend/tests/conftest.py 의 DATABASE_URL fallback 은 그대로 상속된다 — e2e 는
DB 가 살아있는 환경 (systemd 영속화) 을 가정하므로 fallback 자체가 발동되지 않지만,
import 단계에서 깨지지 않게 안전망이 유지된다.
"""
