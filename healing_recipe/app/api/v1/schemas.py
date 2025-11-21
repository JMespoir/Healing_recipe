# app/api/v1/schemas.py
from pydantic import BaseModel


class SurveyAnswers(BaseModel):
    q1: str
    q2: str
    q3: str
    q4: str
    q5: str
    q6: str
    q7: str
    q8: str
    q9: str
    q10: str
    q11: str
    q12: str


class SymbolResponse(BaseModel):
    code: str
    name: str
    description: str


class ReliefItem(BaseModel):
    id: str | int
    title: str | None = None
    description: str | None = None
    persona_label: str | None = None


class RecommendResponse(BaseModel):
    symbol: SymbolResponse | None
    reliefs: list[ReliefItem]