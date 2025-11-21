# app/services/symboling.py
#심볼릭 코드 담당
from collections import Counter

SYMBOL_DISPLAY = {
    "QUIET_HEALER": {
        "name": "조용한 회복러",
        "description": "조용하고 안정적인 환경에서 혼자 회복하는 것을 선호하는 타입이에요.",
    },
    "ACTIVE_DRAINER": {
        "name": "액티브 방전형",
        "description": "몸을 움직이거나 활동적인 경험을 통해 스트레스를 해소하는 타입이에요.",
    },
    "MIND_PLANNER": {
        "name": "마음정리 플래너",
        "description": "정리·기록·계획 등을 통해 머릿속을 정돈하며 해소하는 타입이에요.",
    },
}


def decide_symbol_from_results(results):
    """
    Qdrant search 결과에서 persona_label을 모아서,
    가장 많이 나온 레이블을 심볼로 결정.
    """
    labels = []
    for r in results:
        payload = r.payload or {}
        label = payload.get("persona_label")
        if label:
            labels.append(label)

    if not labels:
        return None  # fallback은 라우터에서 처리

    most_common = Counter(labels).most_common(1)[0][0]
    symbol_info = SYMBOL_DISPLAY.get(most_common)

    if not symbol_info:
        return {
            "code": most_common,
            "name": most_common,
            "description": "타입 설명이 아직 등록되지 않았어요.",
        }

    return {
        "code": most_common,
        "name": symbol_info["name"],
        "description": symbol_info["description"],
    }