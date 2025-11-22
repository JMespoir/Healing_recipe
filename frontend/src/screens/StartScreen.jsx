import React from 'react';

function StartScreen({ name, setName, age, setAge, onStart }) {
  return (
    <div className="start-screen fade-in">
      <div className="start-left">
        <div className="icon-container">✨</div>
        <h1 className="main-title">스트레스<br/>해소 가이드</h1>
        <p className="sub-title">당신만을 위한 맞춤 솔루션을<br/>찾아드립니다</p>
      </div>
      
      <div className="start-right">
        <div className="form-box">
          <div className="input-group">
            <label>이름</label>
            <input 
              type="text" 
              placeholder="이름 입력" 
              value={name} 
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <div className="input-group">
            <label>나이</label>
            <input 
              type="number" 
              placeholder="나이 입력" 
              value={age} 
              onChange={(e) => setAge(e.target.value)}
            />
          </div>
          <button className="primary-btn" onClick={onStart}>분석 시작하기</button>
          <p className="footer-text">AI 알고리즘이 당신의 스트레스 패턴을 분석합니다.</p>
        </div>
      </div>
    </div>
  );
}

export default StartScreen;