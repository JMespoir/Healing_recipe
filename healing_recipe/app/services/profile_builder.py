# app/services/profile_builder.py
# 프론트로부터 받아서 프롬프트로 묶기
from app.api.v1.schemas import SurveyAnswers


def build_profile_text(answers: SurveyAnswers) -> str:
    """
    12개 문항 응답을 하나의 텍스트로 합쳐서
    임베딩에 넣기 좋은 "프로필 설명"으로 만든다.
    실제 서비스에서는 문항 내용에 맞춰 더 자연스럽게 바꿔도 됨.
    """
    lines = [
        "사용자의 스트레스/라이프스타일 응답 요약:",
        f"Q1: {answers.q1}",
        f"Q2: {answers.q2}",
        f"Q3: {answers.q3}",
        f"Q4: {answers.q4}",
        f"Q5: {answers.q5}",
        f"Q6: {answers.q6}",
        f"Q7: {answers.q7}",
        f"Q8: {answers.q8}",
        f"Q9: {answers.q9}",
        f"Q10: {answers.q10}",
        f"Q11: {answers.q11}",
        f"Q12: {answers.q12}",
    ]
    return "\n".join(lines)