# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 오늘은 Gemini 안 쓰지만, 나중을 위해 남겨두는 정도
    GEMINI_API_KEY: str | None = "AIzaSyDKl-tMSoSvP2jH2t9jRDah1pBII3Rl9QU"
    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-001"

    # ✅ 임베딩 벡터 차원 (더미/실제 공통)
    EMBEDDING_DIM: int = 128

    # Qdrant 설정
    QDRANT_HOST: str = "host.docker.internal"   # 도커 compose 쓸 땐 "vectordb" 로 바꿀 예정
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "stress_reliefs"

    class Config:
        env_file = ".env"


settings = Settings()