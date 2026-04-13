"""TASK-103: locke-claim-005 수정 및 claim-005/011 verified 설정.

Tester 검증(TASK-102) 결과 반영:
- 이슈 1: claim-005의 original_text를 §149에서 §143-144(권력 분립 자체)로 변경하여
  claim-011(인민주권론, §149)과의 중복을 해소.
- claim-005, claim-011 모두 verified: true 설정.
"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.es_client import get_client, close_client
from src.config import INDEX_CLAIMS


def fix_claim_005(client):
    """claim-005를 권력 분립론에 집중하도록 수정."""

    update_body = {
        "doc": {
            "source_detail": "Second Treatise, Chapters 11-14, §134, §143-148, §159-168",
            "claim": (
                "정부의 권력은 입법권(legislative power), 집행권(executive power), "
                "동맹권/연합권(federative power)으로 분립되어야 한다. "
                "입법권과 집행권은 분리되어야 하며, 동맹권은 집행권과 함께 같은 수중에 놓이는 것이 "
                "자연스럽다. 또한 집행부에는 공공선을 위한 재량적 대권(prerogative)이 인정된다."
            ),
            "original_text": (
                "The legislative and executive power come often to be separated... "
                "and because it may be too great a temptation to human frailty, apt to grasp at power, "
                "for the same persons, who have the power of making laws, to have also in their hands "
                "the power to execute them, whereby they may exempt themselves from obedience to the laws "
                "they make, and suit the law, both in its making, and execution, to their own private advantage."
            ),
            "original_text_ko": (
                "입법권과 집행권은 자주 분리되게 된다... "
                "법을 만드는 권한을 가진 사람들이 동시에 그 법을 집행할 권한도 가지는 것은 "
                "인간의 나약함에 대한 너무 큰 유혹이 될 수 있기 때문이다. "
                "그들은 자신이 만든 법에 대한 복종에서 스스로를 면제하고, "
                "법의 제정과 집행 모두를 자신의 사적 이익에 맞출 수 있게 될 것이다."
            ),
            "explanation": (
                "로크의 권력 분립론은 몽테스키외의 삼권분립론의 선구이다. "
                "입법권은 법률 제정, 집행권은 법률의 지속적 시행, "
                "동맹권은 외교·전쟁 등 대외 관계를 담당한다. "
                "로크는 사법권을 별도로 분리하지 않았으며(이는 몽테스키외의 기여), "
                "집행권과 동맹권은 성질은 다르지만 실제로 같은 수중(보통 군주)에 있는 것이 편리하다고 보았다(§148). "
                "핵심 논거는 입법권과 집행권의 분리이다: 같은 사람이 법을 만들고 집행하면 "
                "자신을 법의 적용에서 면제하는 유혹에 빠진다(§143). "
                "또한 로크는 대권(prerogative)을 인정했다(Chapter 14, §159-168): "
                "집행부가 공공선을 위해 법률의 규정 없이 또는 법률에 반하여 행위하는 재량권이다."
            ),
            "argument": (
                "(1) 인간은 자연 상태에서 두 가지 권력을 가진다: "
                "자기보존을 위해 자연법의 범위 안에서 행동하는 권력, "
                "자연법 위반자를 처벌하는 집행 권력. "
                "(2) 정치 사회에 들어가면서 첫 번째는 입법권으로, 두 번째는 집행권으로 공동체에 양도된다. "
                "(3) 입법권과 집행권의 분리가 필요한 이유: "
                "같은 사람이 법을 만들고 집행하면 사적 이익에 법을 맞추는 유혹에 빠진다(§143). "
                "(4) 입법부는 상시 존재할 필요가 없으나, 집행권은 항상 활동해야 하므로 "
                "두 권력은 자연히 다른 수중에 놓인다(§144). "
                "(5) 동맹권(외교·전쟁)은 집행권과 성질이 다르지만, "
                "무력의 사용이 수반되므로 같은 수중에 두는 것이 실제적이다(§147-148). "
                "(6) 대권(prerogative): 법률이 예측하지 못한 상황에서 공공선을 위한 "
                "집행부의 재량권이 정당화된다(§159-160)."
            ),
            "verified": True,
            "verification_log": [
                {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "result": "verified",
                    "method": "tester-agent-opus",
                    "task_id": "TASK-103",
                    "note": (
                        "Tester 검증(TASK-102) 결과 반영. "
                        "original_text를 §149(인민주권론, claim-011과 중복)에서 "
                        "§143(권력 분립의 근거)로 변경. "
                        "source_detail, claim, explanation, argument를 "
                        "권력 분립론(입법·집행·동맹권의 구분, 분리의 근거, 대권)에 집중하도록 수정."
                    ),
                }
            ],
        }
    }

    result = client.update(index=INDEX_CLAIMS, id="locke-claim-005", body=update_body)
    print(f"[claim-005] update: {result['result']}")
    return result


def verify_claim_011(client):
    """claim-011에 verified: true 설정."""

    update_body = {
        "doc": {
            "verified": True,
            "verification_log": [
                {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "result": "verified",
                    "method": "tester-agent-opus",
                    "task_id": "TASK-103",
                    "note": (
                        "Tester 검증(TASK-102) 결과: 내용 정확. "
                        "인민주권론(인민 > 입법부 > 집행부 위계, 신탁 위반 시 권력 귀속, 저항권 연결)에 집중. "
                        "claim-005와의 중복은 claim-005 측을 수정하여 해소."
                    ),
                }
            ],
        }
    }

    result = client.update(index=INDEX_CLAIMS, id="locke-claim-011", body=update_body)
    print(f"[claim-011] update: {result['result']}")
    return result


def verify_results(client):
    """수정 결과 확인."""
    print("\n=== 수정 결과 확인 ===\n")

    for claim_id in ["locke-claim-005", "locke-claim-011"]:
        res = client.get(index=INDEX_CLAIMS, id=claim_id)
        src = res["_source"]
        print(f"--- {claim_id} ---")
        print(f"  verified: {src.get('verified')}")
        print(f"  source_detail: {src.get('source_detail')}")
        print(f"  original_text (first 80 chars): {src.get('original_text', '')[:80]}...")
        print(f"  verification_log: {src.get('verification_log', 'N/A')}")
        print()


def main():
    client = get_client()
    try:
        print("=== TASK-103: 로크 데이터 이슈 수정 ===\n")

        print("1. claim-005 수정 (권력 분립론 집중, original_text §143으로 변경)")
        fix_claim_005(client)

        print("\n2. claim-011 verified 설정")
        verify_claim_011(client)

        verify_results(client)

        print("=== 완료 ===")
    finally:
        close_client(client)


if __name__ == "__main__":
    main()
