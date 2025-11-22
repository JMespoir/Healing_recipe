import React, { useState, useMemo } from 'react';
import { SURVEY_DATA } from '../data/questions'; // 새로 만든 데이터 파일 임포트

function SurveyScreen({ onFinish }) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [collectedAnswers, setCollectedAnswers] = useState([]);

  // 1. 계층 구조의 데이터를 '질문 하나하나의 리스트'로 펼칩니다. (Flatten)
  // 이렇게 하면 "다음 질문" 로직을 그대로 쓸 수 있습니다.
  const allQuestions = useMemo(() => {
    return SURVEY_DATA.flatMap((section) => 
      section.items.map((item) => ({
        ...item,
        category: section.category // 질문마다 카테고리 정보를 심어줍니다.
      }))
    );
  }, []);

  const handleOptionClick = (option) => {
    const currentQuestion = allQuestions[currentQuestionIndex];

    // 2. 답변 저장 포맷 (서버가 좋아할 형태로 저장)
    const newAnswer = { 
      category: currentQuestion.category,
      question_id: currentQuestion.id,
      question_text: currentQuestion.question,
      answer: option 
    };

    const updatedAnswers = [...collectedAnswers, newAnswer];
    setCollectedAnswers(updatedAnswers);

    // 3. 다음 단계 로직
    const nextQuestion = currentQuestionIndex + 1;
    if (nextQuestion < allQuestions.length) {
      setCurrentQuestionIndex(nextQuestion);
    } else {
      onFinish(updatedAnswers);
    }
  };

  const currentQ = allQuestions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / allQuestions.length) * 100;

  return (
    <div className="survey-screen fade-in">
      <div className="progress-area">
        <div className="progress-header">
          {/* 카테고리 이름 표시 (선택 사항) */}
          <span className="category-badge">{currentQ.category}</span>
          <span>{currentQuestionIndex + 1} / {allQuestions.length}</span>
        </div>
        <div className="progress-bar-bg">
          <div className="progress-bar-fill" style={{width: `${progress}%`}}></div>
        </div>
      </div>

      <div className="question-area">
        <h2 className="question-text">{currentQ.question}</h2>
      </div>

      <div className="options-grid">
        {currentQ.options.map((option, index) => (
          <button key={index} className="option-card" onClick={() => handleOptionClick(option)}>
            <span className="option-text">{option}</span>
            <div className="check-icon"></div>
          </button>
        ))}
      </div>
    </div>
  );
}

export default SurveyScreen;