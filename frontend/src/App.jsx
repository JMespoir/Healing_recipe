import React, { useState } from 'react';
import './App.css';
import StartScreen from './screens/StartScreen';
import SurveyScreen from './screens/SurveyScreen';
import ResultScreen from './screens/ResultScreen';
import { analyzeStress } from './api/api'; // API 함수 임포트

function App() {
  const [step, setStep] = useState('start'); 
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  
  // API 관련 상태
  const [isLoading, setIsLoading] = useState(false);
  const [serverResult, setServerResult] = useState(null); // 서버에서 받은 결과

  const handleStart = () => {
    if (name && age) setStep('survey');
    else alert('이름과 나이를 입력해주세요.');
  };

  // 설문이 끝났을 때 실행 (API 호출)
  const handleSurveyFinish = async (collectedAnswers) => {
    setIsLoading(true); // 로딩 시작
    
    try {
      // 1. 실제 서버로 요청 보내기
      const result = await analyzeStress(name, age, collectedAnswers);
      setServerResult(result); // 결과 저장
      setStep('result'); // 결과 화면으로 이동
      
    } catch (error) {
      alert("서버 연결에 실패했습니다. (콘솔 확인 필요)\n일단 임시 결과를 보여드립니다.");
      console.error(error);
      
      // 에러 시에도 테스트를 위해 결과 화면으로 이동하고 싶다면:
      setStep('result'); 
    } finally {
      setIsLoading(false); // 로딩 종료
    }
  };

  const handleRestart = () => {
    setStep('start');
    setName('');
    setAge('');
    setServerResult(null);
    setIsLoading(false);
  };

  return (
    <div className="app-container">
      {/* 로딩 화면 오버레이 */}
      {isLoading && (
        <div className="loading-overlay fade-in">
          <div className="spinner"></div>
          <p>AI가 당신의 스트레스를 분석하고 있습니다...🧠</p>
        </div>
      )}

      <div className={`content-box ${step}`}>
        
        {step === 'start' && (
          <StartScreen 
            name={name} 
            setName={setName} 
            age={age} 
            setAge={setAge} 
            onStart={handleStart} 
          />
        )}

        {step === 'survey' && (
          <SurveyScreen 
            onFinish={handleSurveyFinish} 
          />
        )}

        {step === 'result' && (
          <ResultScreen 
            name={name}
            serverResult={serverResult} // 서버 결과를 전달
            onRestart={handleRestart} 
          />
        )}

      </div>
    </div>
  );
}

export default App;