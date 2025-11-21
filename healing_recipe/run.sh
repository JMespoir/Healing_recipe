#!/bin/bash
set -e

echo "🚀 Healing Recipe Backend Starting..."

# 0) 가상환경 활성화 (필요한 경우)
# source venv/bin/activate

# 1) Qdrant 상태 체크
echo "🔍 Checking Qdrant status..."
if curl -s http://host.docker.internal:6333/ > /dev/null ; then
    echo "🟢 Qdrant is running."
else
    echo "❌ Qdrant is not running!"
    echo "➡ docker run -p 6333:6333 -v \$(pwd)/qdrant_data:/qdrant/storage qdrant/qdrant"
    exit 1
fi

# 2) Qdrant 컬렉션 생성
echo "📦 Initializing Qdrant collection..."
python3 - << 'EOF'
from app.services.vectordb import init_collection_if_needed
init_collection_if_needed()
print("✔ Collection initialized.")
EOF

# 3) 더미 해소법 로딩
echo "📚 Loading stress relief items..."
python3 app/scripts/load_dummy_reliefs.py
echo "✔ Relief items uploaded."

# 4) 클러스터링 실행
echo "🧠 Running KMeans clustering..."
python3 - << 'EOF'
from app.services.clustering import StressClusteringService
service = StressClusteringService()
service.cluster(8)
print("✔ Clustering done.")
EOF

# 5) FastAPI 실행
echo "🌐 Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
