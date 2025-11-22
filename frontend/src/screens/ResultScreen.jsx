import React from 'react';
import { recommendations } from '../data/mockDatas'; // 나중에는 API 응답으로 대체

function ResultScreen({ name, onRestart }) {
  // 나중에 recommendations 대신 props로 serverResult를 받을 예정입니다.
  
  return (
    <div className="result-screen fade-in">
      <div className="result-header">
        <div className="icon-container small">🏆</div>
        <div className="header-text">
          <h2>{name}님을 위한 처방전</h2>
          <p>분석된 스트레스 유형에 따른 최적의 솔루션입니다.</p>
        </div>
      </div>

      <div className="cards-grid">
        {recommendations.map((item, index) => (
          <div key={index} className="result-card">
            <div className="card-icon-box">{item.icon}</div>
            <h3>{item.title}</h3>
            <p>{item.desc}</p>
          </div>
        ))}
      </div>

      <button className="restart-btn" onClick={onRestart}>다시 검사하기</button>
    </div>
  );
}

export default ResultScreen;