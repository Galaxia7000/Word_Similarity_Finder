import React from "react";


function SimilarityMatrix({ matrix }) {

  if (!matrix || matrix.length === 0) {
    return null;
  }


  return (
    <div className="similarity-matrix-wrapper">

      <div className="matrix-scroll">

        <table className="similarity-matrix">

          <thead>
            <tr>

              <th className="matrix-corner">
                WORD
              </th>

              {matrix.map((row) => (
                <th key={row.word}>
                  {row.word.toUpperCase()}
                </th>
              ))}

            </tr>
          </thead>


          <tbody>

            {matrix.map((row) => (

              <tr key={row.word}>

                <th className="matrix-row-label">
                  {row.word.toUpperCase()}
                </th>

                {row.values.map((cell) => {

                  const intensity = Math.round(
                    cell.percentage
                  );

                  return (
                    <td
                      key={`${row.word}-${cell.word}`}
                      className="matrix-cell"
                      style={{
                        "--cell-intensity": `${intensity}%`,
                      }}
                      title={
                        `${row.word} ↔ ${cell.word}: ` +
                        `${cell.cosine_similarity.toFixed(6)}`
                      }
                    >
                      {cell.percentage.toFixed(0)}%
                    </td>
                  );

                })}

              </tr>

            ))}

          </tbody>

        </table>

      </div>


      <div className="matrix-legend">

        <span>
          SEMANTIC SIMILARITY
        </span>

        <div className="legend-scale">

          <span>LOW</span>

          <div className="legend-bar"></div>

          <span>HIGH</span>

        </div>

      </div>

    </div>
  );
}


export default SimilarityMatrix;