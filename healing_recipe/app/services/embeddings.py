"""
개발용 더미 임베딩 버전.
Google Gemini API 대신 로컬 해시 기반 벡터를 생성한다.
테스트/개발 단계에서는 이 버전을 권장한다.
"""

import hashlib
from app.core.config import settings


def _hash_to_vector(text: str, dim: int) -> list[float]:
    """
    텍스트를 해시 기반으로 [dim] 길이의 벡터로 변환.
    완전 랜덤 아님 → 같은 텍스트는 항상 같은 벡터 생성.
    """
    if not text:
        text = " "

    seed = text.encode("utf-8")
    digest = hashlib.sha256(seed).digest()

    floats: list[float] = []
    idx = 0

    while len(floats) < dim:
        chunk = digest[idx: idx + 4]
        if len(chunk) < 4:
            seed = digest
            digest = hashlib.sha256(seed).digest()
            idx = 0
            continue

        int_val = int.from_bytes(chunk, byteorder="big", signed=False)
        float_val = (int_val / 2**32) * 2.0 - 1.0
        floats.append(float_val)

        idx += 4
        if idx >= len(digest):
            seed = digest
            digest = hashlib.sha256(seed).digest()
            idx = 0

    return floats


def embed_text(text: str) -> list[float]:
    """
    개발용 더미 임베딩 함수.
    settings.EMBEDDING_DIM 차원의 벡터를 반환.
    """
    dim = settings.EMBEDDING_DIM
    return _hash_to_vector(text, dim)
