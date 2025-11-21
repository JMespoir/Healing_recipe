from qdrant_client import QdrantClient
from sklearn.cluster import KMeans
import joblib
from .embeddings import embed_text
from .clustering import StressClusteringService
from .clustering import CLUSTER_SYMBOLS

class StressRecommender:
    """
    사용자 텍스트 → 벡터 → KMeans로 클러스터 예측 → 해당 클러스터 해소법 추천
    """

    def __init__(self, host="localhost", port=6333, collection="stress_reliefs", kmeans_model_path="kmeans_model.pkl"):
        self.collection = collection
        self.client = QdrantClient(host=host, port=port)

        # KMeans 모델 로드
        try:
            self.kmeans: KMeans = joblib.load(kmeans_model_path)
        except Exception:
            raise RuntimeError("kmeans_model.pkl 파일을 찾을 수 없습니다. clustering.py에서 모델을 저장해야 합니다.")

        # 클러스터 아이템 조회 서비스
        self.cluster_service = StressClusteringService(host=host, port=port, collection_name=collection)

    def recommend(self, user_text: str):
        """
        1) 텍스트 임베딩
        2) KMeans.predict()로 사용자 벡터의 클러스터 예측
        3) 해당 클러스터의 해소법 전체 반환
        """
        # 1) 사용자 텍스트 → 벡터
        user_vector = embed_text(user_text)

        # 2) KMeans로 사용자 벡터가 속한 클러스터 예측
        cluster_id = int(self.kmeans.predict([user_vector])[0])

        # 3) 해당 cluster_id의 모든 해소법 가져오기
        items = self.cluster_service.get_cluster_items(cluster_id)

        return {
            "user_text": user_text,
            "cluster_id": cluster_id,
            "symbol" : CLUSTER_SYMBOLS[cluster_id],
            "recommendations": items
        }


if __name__ == "__main__":
    rec = StressRecommender()
    result = rec.recommend("요즘 머리도 아프고 피곤하고 스트레스가 많아")
    print(result)