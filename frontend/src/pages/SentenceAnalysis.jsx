import React, {
  useEffect,
  useRef,
  useState
} from "react";

import { useNavigate } from "react-router-dom";

import PixelButton from "../components/PixelButton";
import PixelCard from "../components/PixelCard";
import VectorDisplay from "../components/VectorDisplay";
import SimilarityMatrix from "../components/SimilarityMatrix";

import { analyzeSentence } from "../services/api";


function SentenceAnalysis() {
  const navigate = useNavigate();

  const [text, setText] = useState("");

  const [result, setResult] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const abortControllerRef = useRef(null);


  async function handleAnalyze(event) {
    event.preventDefault();

    setError("");
    setResult(null);

    if (!text.trim()) {
      setError("PLEASE ENTER A SENTENCE.");
      return;
    }

    /*
     * Cancel any previous request before starting
     * a new analysis.
     */
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    const controller = new AbortController();

    abortControllerRef.current = controller;

    setLoading(true);

    try {
      const data = await analyzeSentence(
        text,
        controller.signal
      );

      /*
       * If this request was cancelled, do not
       * display its result.
       */
      if (controller.signal.aborted) {
        return;
      }

      setResult(data);

    } catch (err) {

      /*
       * AbortError is expected when RESET is pressed
       * or when another request replaces this one.
       */
      if (err.name === "AbortError") {
        return;
      }

      setError(
        err.message || "AN ERROR OCCURRED."
      );

    } finally {

      if (!controller.signal.aborted) {
        setLoading(false);
      }
    }
  }


  function resetAnalysis() {

    /*
     * Immediately cancel the active API request.
     */
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();

      abortControllerRef.current = null;
    }

    /*
     * Immediately remove the loading state.
     */
    setLoading(false);

    /*
     * Clear the interface.
     */
    setText("");
    setResult(null);
    setError("");
  }


  /*
   * Cancel any active request when the user
   * leaves the page.
   */
  useEffect(() => {

    return () => {

      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }

    };

  }, []);


  return (
    <main className="analysis-page sentence-page">

      {/* ==========================================
          TOP BAR
      ========================================== */}

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


      {/* ==========================================
          PAGE HEADER
      ========================================== */}

      <section className="analysis-header">

        <div className="hero-badge">
          MODE 02 // SENTENCE → VECTOR
        </div>


        <h1 className="page-title">

          SENTENCE

          <span>
            ANALYSIS
          </span>

        </h1>


        <p className="page-description">

          DROP IN A SENTENCE AND EXPLORE
          THE WORDS LIVING INSIDE ITS VECTOR SPACE.

        </p>

      </section>


      {/* ==========================================
          INPUT
      ========================================== */}

      <section className="sentence-input-section">

        <PixelCard className="sentence-input-card">

          <form onSubmit={handleAnalyze}>

            <div className="sentence-label-row">

              <label htmlFor="sentence-input">
                ENTER SENTENCE
              </label>

              <span>
                MAX 20 UNIQUE WORDS
              </span>

            </div>


            <textarea
              id="sentence-input"
              value={text}
              onChange={(event) =>
                setText(event.target.value)
              }
              placeholder="TYPE YOUR SENTENCE HERE..."
              rows={5}
              disabled={loading}
            />


            {/* Error */}

            {error && (

              <div className="error-message">

                <span>⚠</span>

                {error}

              </div>

            )}


            {/* Actions */}

            <div className="analysis-actions">

              <PixelButton
                type="submit"
                className="start-button"
              >
                {loading
                  ? "ANALYZING..."
                  : "EXPLORE SENTENCE"
                }
              </PixelButton>


              {(result || text || loading) && (

                <button
                  type="button"
                  className="secondary-action"
                  onClick={resetAnalysis}
                >
                  RESET
                </button>

              )}

            </div>

          </form>

        </PixelCard>

      </section>


      {/* ==========================================
          LOADING
      ========================================== */}

      {loading && (

        <section className="loading-panel">

          <div className="loading-pixel">
            ◆ ◆ ◆
          </div>


          <h2>
            MAPPING VECTOR SPACE...
          </h2>


          <p>
            TOKENIZING • CHECKING LIBRARY •
            RETRIEVING VECTORS •
            CALCULATING RELATIONSHIPS
          </p>

        </section>

      )}


      {/* ==========================================
          RESULTS
      ========================================== */}

      {result && !loading && (

        <section className="sentence-results">


          {/* ========================================
              SUMMARY
          ======================================== */}

          <div className="sentence-summary">

            <PixelCard>

              <span className="summary-label">
                WORDS FOUND
              </span>

              <strong>
                {result.unique_valid_word_count}
              </strong>

            </PixelCard>


            <PixelCard>

              <span className="summary-label">
                TOTAL TOKENS
              </span>

              <strong>
                {result.word_count}
              </strong>

            </PixelCard>


            <PixelCard>

              <span className="summary-label">
                VECTOR DIMENSION
              </span>

              <strong>
                300D
              </strong>

            </PixelCard>

          </div>


          {/* ========================================
              STOP WORDS
          ======================================== */}

          {result.stop_words &&
            result.stop_words.length > 0 && (

            <section className="stopword-section">

              <div className="section-heading">

                <span>
                  STOP WORDS
                </span>

                <small>
                   NOT FOUND IN THE MODEL LIBRARY
                </small>

              </div>


              <div className="stopword-chips">

                {result.stop_words.map((word) => (

                  <span
                    className="stopword-chip"
                    key={word}
                  >
                    {word.toUpperCase()}
                  </span>

                ))}

              </div>

            </section>

          )}


          {/* ========================================
              VOCABULARY DETECTED
          ======================================== */}

          <section className="word-discovery">

            <div className="section-heading">

              <span>
                VOCABULARY DETECTED
              </span>

              <small>
                MODEL-KNOWN WORDS
              </small>

            </div>


            <div className="word-chips">

              {result.valid_words.map((word) => (

                <span
                  className="word-chip"
                  key={word}
                >
                  {word.toUpperCase()}
                </span>

              ))}

            </div>

          </section>


          {/* ========================================
              STRONGEST CONNECTION
          ======================================== */}

          {result.strongest_pair && (

            <section className="strongest-pair">

              <div className="result-heading">
                STRONGEST CONNECTION FOUND
              </div>


              <div className="strongest-words">

                <span>
                  {result.strongest_pair.word_a.toUpperCase()}
                </span>


                <span className="strongest-arrow">
                  ↔
                </span>


                <span>
                  {result.strongest_pair.word_b.toUpperCase()}
                </span>

              </div>


              <strong>
                {result.strongest_pair.percentage.toFixed(2)}%
              </strong>


              <small>
                {result.strongest_pair.classification.toUpperCase()}
              </small>

            </section>

          )}


          {/* ========================================
              SIMILARITY MATRIX
          ======================================== */}

          <section className="matrix-section">

            <div className="section-heading">

              <span>
                SEMANTIC RELATIONSHIP MAP
              </span>

              <small>
                PAIRWISE COSINE SIMILARITY
              </small>

            </div>


            <SimilarityMatrix
              matrix={result.similarity_matrix}
            />

          </section>


          {/* ========================================
              VECTOR INSPECTION
          ======================================== */}

          <section className="sentence-vectors">

            <div className="section-heading">

              <span>
                WORD VECTOR INSPECTION
              </span>

              <small>
                300 DIMENSIONS
              </small>

            </div>


            <div className="sentence-vector-grid">

              {result.vectors.map((item) => (

                <PixelCard
                  key={item.word}
                  className="sentence-vector-card"
                >

                  <VectorDisplay
                    word={item.word}
                    vector={item.vector}
                    preview={item.vector_preview}
                  />


                  <div className="vector-stats">

                    <div>

                      <span>
                        MIN
                      </span>

                      <strong>
                        {item.statistics.minimum.toFixed(4)}
                      </strong>

                    </div>


                    <div>

                      <span>
                        MAX
                      </span>

                      <strong>
                        {item.statistics.maximum.toFixed(4)}
                      </strong>

                    </div>


                    <div>

                      <span>
                        MEAN
                      </span>

                      <strong>
                        {item.statistics.mean.toFixed(4)}
                      </strong>

                    </div>


                    <div>

                      <span>
                        L2 NORM
                      </span>

                      <strong>
                        {item.statistics.l2_norm.toFixed(4)}
                      </strong>

                    </div>

                  </div>

                </PixelCard>

              ))}

            </div>

          </section>


        </section>

      )}

    </main>
  );
}


export default SentenceAnalysis;