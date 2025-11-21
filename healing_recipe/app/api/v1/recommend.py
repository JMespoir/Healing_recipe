# app/api/v1/recommend.py

from fastapi import APIRouter, HTTPException
from app.api.v1.schemas import (
    SurveyAnswers,
    RecommendResponse,
    ReliefItem,
    SymbolResponse,
)
from app.services.profile_builder import build_profile_text
from app.services.embeddings import embed_text
from app.services.vectordb import (
    init_collection_if_needed,
    search_similar_stress_reliefs,
)
from app.services.symboling import decide_symbol_from_results

router = APIRouter()


@router.on_event("startup")
def on_startup():
    # Qdrant 컬렉션 없으면 생성
    init_collection_if_needed()


@router.post("/recommend", response_model=RecommendResponse)
def recommend(answers: SurveyAnswers):
    # 1) 설문 응답 → 프로필 텍스트
    profile_text = build_profile_text(answers)

    # 2) 텍스트 → 임베딩 벡터 (오늘은 더미 임베딩)
    user_vec = embed_text(profile_text)

    # 3) Qdrant에서 유사한 해소법 검색
    results = search_similar_stress_reliefs(user_vec, top_k=10)

    if not results:
        # 아직 DB에 아무 것도 없는 경우
        raise HTTPException(
            status_code=404,
            detail="아직 등록된 스트레스 해소법이 없습니다. 관리자에게 문의해주세요.",
        )

    # 4) 심볼 결정
    symbol_dict = decide_symbol_from_results(results)
    symbol_response = (
        SymbolResponse(**symbol_dict) if symbol_dict is not None else None
    )

    # 5) 해소법 리스트 변환
    relief_items: list[ReliefItem] = []
    for r in results:
        payload = r.payload or {}
        relief_items.append(
            ReliefItem(
                id=r.id,
                title=payload.get("title"),
                description=payload.get("description"),
                persona_label=payload.get("persona_label"),
            )
        )

    return RecommendResponse(
        symbol=symbol_response,
        reliefs=relief_items,
    )