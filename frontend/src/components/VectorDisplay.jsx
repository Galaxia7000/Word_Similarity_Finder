import React, { useState } from "react";


function VectorDisplay({ word, vector, preview }) {
  const [showFullVector, setShowFullVector] = useState(false);

  const valuesToDisplay = showFullVector
    ? vector
    : preview;

  return (
    <div className="vector-display">

      <div className="vector-header">
        <div>
          <span className="vector-label">
            VECTOR DATA
          </span>

          <h3>{word.toUpperCase()}</h3>
        </div>

        <span className="vector-dimension">
          {vector.length}D
        </span>
      </div>


      <div className="vector-values">
        {valuesToDisplay.map((value, index) => (
          <div
            className="vector-value"
            key={`${word}-${index}`}
          >
            <span className="vector-index">
              {index + 1}
            </span>

            <span>
              {Number(value).toFixed(6)}
            </span>
          </div>
        ))}
      </div>


      <button
        className="vector-toggle"
        onClick={() => setShowFullVector(!showFullVector)}
      >
        {showFullVector
          ? "← SHOW PREVIEW"
          : `SHOW ALL ${vector.length} VALUES →`
        }
      </button>

    </div>
  );
}


export default VectorDisplay;