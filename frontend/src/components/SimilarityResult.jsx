import React from "react";


function SimilarityResult({ similarity, wordA, wordB }) {
  const score = similarity.cosine_similarity;
  const percentage = similarity.percentage;


  return (
    <section className="similarity-result">

      <div className="result-heading">
        <span>SEMANTIC CONNECTION</span>
      </div>


      <div className="connection-words">
        <span>{wordA.toUpperCase()}</span>

        <div className="connection-line">
          <span>✦</span>
          <span>↔</span>
          <span>✦</span>
        </div>

        <span>{wordB.toUpperCase()}</span>
      </div>


      <div className="score-box">

        <div className="score-number">
          {percentage.toFixed(2)}
          <small>%</small>
        </div>

        <div className="score-title">
          {similarity.classification.toUpperCase()}
        </div>

      </div>


      <div className="similarity-meter">

        <div
          className="similarity-fill"
          style={{
            width: `${percentage}%`
          }}
        />

      </div>


      <div className="raw-score">

        <span>
          COSINE SIMILARITY
        </span>

        <strong>
          {score.toFixed(6)}
        </strong>

      </div>

    </section>
  );
}


export default SimilarityResult;