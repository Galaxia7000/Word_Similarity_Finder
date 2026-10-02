import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import PixelButton from "../components/PixelButton";
import PixelCard from "../components/PixelCard";
import VectorDisplay from "../components/VectorDisplay";
import SimilarityResult from "../components/SimilarityResult";

import { compareWords } from "../services/api";


function TwoWordAnalysis() {

  const navigate = useNavigate();

  const [wordA, setWordA] = useState("");
  const [wordB, setWordB] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");


  async function handleCompare(event) {
    event.preventDefault();

    setError("");
    setResult(null);


    if (!wordA.trim() || !wordB.trim()) {
      setError("PLEASE ENTER BOTH WORDS.");
      return;
    }


    if (wordA.trim().split(/\s+/).length > 1) {
      setError("WORD 01 SHOULD CONTAIN ONLY ONE WORD.");
      return;
    }


    if (wordB.trim().split(/\s+/).length > 1) {
      setError("WORD 02 SHOULD CONTAIN ONLY ONE WORD.");
      return;
    }


    setLoading(true);


    try {
      const data = await compareWords(
        wordA,
        wordB
      );

      setResult(data);

    } catch (err) {
      setError(
        err.message || "AN ERROR OCCURRED."
      );

    } finally {
      setLoading(false);
    }
  }


  function handleReset() {
    setWordA("");
    setWordB("");
    setResult(null);
    setError("");
  }


  return (
    <main className="analysis-page">

      <header className="analysis-topbar">

        <button
          className="back-button"
          onClick={() => navigate("/modes")}
        >
          ← MODES
        </button>

        <div className="analysis-logo">
          W2V // LAB
        </div>

      </header>


      <section className="analysis-header">

        <div className="hero-badge">
          MODE 01 // WORD ↔ WORD
        </div>

        <h1 className="page-title">
          TWO WORD
          <span>ANALYSIS</span>
        </h1>

        <p className="page-description">
          ENTER TWO WORDS AND DISCOVER HOW CLOSELY
          THEIR VECTOR SPACES ALIGN.
        </p>

      </section>


      <section className="input-section">

        <PixelCard className="word-input-card">

          <form onSubmit={handleCompare}>

            <div className="word-input-grid">

              <div className="word-input-group">

                <label htmlFor="word-a">
                  WORD 01
                </label>

                <input
                  id="word-a"
                  type="text"
                  value={wordA}
                  onChange={(event) =>
                    setWordA(event.target.value)
                  }
                  placeholder="TYPE A WORD..."
                  autoComplete="off"
                />

              </div>


              <div className="versus">

                <span>AND</span>

              </div>


              <div className="word-input-group">

                <label htmlFor="word-b">
                  WORD 02
                </label>

                <input
                  id="word-b"
                  type="text"
                  value={wordB}
                  onChange={(event) =>
                    setWordB(event.target.value)
                  }
                  placeholder="TYPE A WORD..."
                  autoComplete="off"
                />

              </div>

            </div>


            {error && (
              <div className="error-message">
                <span>⚠</span>
                {error}
              </div>
            )}


            <div className="analysis-actions">

              <PixelButton
                type="submit"
                className="start-button"
              >
                {loading
                  ? "ANALYZING..."
                  : "COMPARE WORDS"
                }
              </PixelButton>


              {(result || wordA || wordB) && (
                <button
                  type="button"
                  className="secondary-action"
                  onClick={handleReset}
                >
                  RESET
                </button>
              )}

            </div>

          </form>

        </PixelCard>

      </section>


      {loading && (
        <section className="loading-panel">

          <div className="loading-pixel">
            ◆ ◆ ◆
          </div>

          <h2>
            SEARCHING VECTOR SPACE...
          </h2>

          <p>
            RETRIEVING WORD EMBEDDINGS
          </p>

        </section>
      )}


      {result && !loading && (

        <section className="results-section">

          <SimilarityResult
            similarity={result.similarity}
            wordA={result.word_a.word}
            wordB={result.word_b.word}
          />


          <div className="vectors-heading">

            <span>
              VECTOR INSPECTION
            </span>

            <small>
              300 DIMENSIONS EACH
            </small>

          </div>


          <div className="vector-grid">

            <PixelCard className="vector-card">

              <VectorDisplay
                word={result.word_a.word}
                vector={result.word_a.vector}
                preview={result.word_a.vector_preview}
              />

              <div className="vector-stats">

                <div>
                  <span>MIN</span>
                  <strong>
                    {result.word_a.statistics.minimum.toFixed(4)}
                  </strong>
                </div>

                <div>
                  <span>MAX</span>
                  <strong>
                    {result.word_a.statistics.maximum.toFixed(4)}
                  </strong>
                </div>

                <div>
                  <span>MEAN</span>
                  <strong>
                    {result.word_a.statistics.mean.toFixed(4)}
                  </strong>
                </div>

                <div>
                  <span>L2 NORM</span>
                  <strong>
                    {result.word_a.statistics.l2_norm.toFixed(4)}
                  </strong>
                </div>

              </div>

            </PixelCard>


            <PixelCard className="vector-card green-card">

              <VectorDisplay
                word={result.word_b.word}
                vector={result.word_b.vector}
                preview={result.word_b.vector_preview}
              />

              <div className="vector-stats">

                <div>
                  <span>MIN</span>
                  <strong>
                    {result.word_b.statistics.minimum.toFixed(4)}
                  </strong>
                </div>

                <div>
                  <span>MAX</span>
                  <strong>
                    {result.word_b.statistics.maximum.toFixed(4)}
                  </strong>
                </div>

                <div>
                  <span>MEAN</span>
                  <strong>
                    {result.word_b.statistics.mean.toFixed(4)}
                  </strong>
                </div>

                <div>
                  <span>L2 NORM</span>
                  <strong>
                    {result.word_b.statistics.l2_norm.toFixed(4)}
                  </strong>
                </div>

              </div>

            </PixelCard>

          </div>

        </section>

      )}

    </main>
  );
}


export default TwoWordAnalysis;