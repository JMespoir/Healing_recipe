# app/services/vectordb.py
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from qdrant_client.http.models import PointStruct
from app.core.config import settings


VECTOR_DIM = settings.EMBEDDING_DIM

#이 client를 통해 insert / search / update 등 모든 동작 수행
client = QdrantClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT,
)


#컬렉션 초기화(콜렉션에 벡터를 저장한다)
def init_collection_if_needed():
    """
    Qdrant collection 생성 (없으면 만들고, 있으면 패스)
    """
    #현재 존재하는 컬렉션 목록 조회
    collections = client.get_collections().collections
    existing = [c.name for c in collections]

    #없다면 컬렉션 생성
    if settings.QDRANT_COLLECTION not in existing:
        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=VECTOR_DIM,
                distance=Distance.COSINE,
            ),
        )
        print("[Qdrant] Collection created")

        # payload 인덱스 생성 => payload 인덱스랑 벡터의 metadata(payload) 빠르게 검색할 수 있게 만드는 검색 최적화 장치
        #cluster_id(정수) ex) KMeans에서 나온 cluster_id 0~7
        client.create_payload_index(
            collection_name=settings.QDRANT_COLLECTION,
            field_name="cluster_id",
            field_schema="integer"
        )

        #symbol_code(문자) ex) "ACT","CAL".. 등등
        client.create_payload_index(
            collection_name=settings.QDRANT_COLLECTION,
            field_name="symbol_code",
            field_schema="keyword"
        )

        #두가지의 인덱스 생성하여 조회할 수 있도록
    else:
        print("[Qdrant] Collection already exists")


#벡터 데이터 삽입 함수
def upsert_reliefs(points: list[PointStruct]):
    client.upsert(
        collection_name=settings.QDRANT_COLLECTION,
        points=points,
        wait=True,
    )


#특정 ID의 해소법을 가져오는 함수
def fetch_by_ids(ids: list[int]):
    """
    선택된 해소법을 가져오기 위해 사용 예정
    """
    return client.retrieve(
        collection_name=settings.QDRANT_COLLECTION,
        ids=ids,
        with_payload=True,
        with_vectors=False,
    )

def search_similar_stress_reliefs(vector: list[float], top_k: int = 10):
    """
    유저 벡터와 유사한 스트레스 해소법 검색
    """
    results = client.search(
        collection_name=settings.QDRANT_COLLECTION,
        query_vector=vector,
        limit=top_k,
        with_payload=True,
    )
    return results