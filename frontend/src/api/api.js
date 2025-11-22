// src/api/api.js
import axios from 'axios';

// FastAPI 서버 주소 (로컬 테스트용)
const API_BASE_URL = 'http://127.0.0.1:8000';

export const analyzeStress = async (name, age, surveyAnswers) => {
  try {
    // 서버로 보낼 데이터 포맷 구성
    const payload = {
      user_info: {
        name: name,
        age: parseInt(age, 10) // 나이는 숫자로 변환
      },
      answerList: surveyAnswers // [{ question_text: "...", answer: "..." }, ...]
    };

    console.log("📤 서버로 전송하는 데이터:", payload);

    // POST 요청 전송
    const response = await axios.post(`${API_BASE_URL}/analyze`, payload);
    
    console.log("📥 서버 응답 데이터:", response.data);
    return response.data;

  } catch (error) {
    console.error("🚨 API 호출 에러:", error);
    // 에러 발생 시 null을 반환하거나 에러를 throw해서 UI에서 처리
    throw error; 
  }
};