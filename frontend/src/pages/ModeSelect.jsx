import React from "react";
import { useNavigate } from "react-router-dom";
import PixelButton from "../components/PixelButton";
import PixelCard from "../components/PixelCard";

function ModeSelect() {
  const navigate = useNavigate();

  return (
    <main className="mode-page">

      <button
        className="back-button"
        onClick={() => navigate("/")}
      >
        ← BACK
      </button>

      <section className="mode-header">

        <div className="hero-badge">
          SELECT YOUR QUEST
        </div>

        <h1 className="page-title">
          CHOOSE
          <span>ANALYSIS MODE</span>
        </h1>

        <p className="page-description">
          HOW DO YOU WANT TO EXPLORE THE VECTOR SPACE?
        </p>

      </section>

      <section className="mode-grid">

        <PixelCard className="mode-card">

          <div className="mode-icon">
            ↔
          </div>

          <div className="mode-number">
            MODE 01
          </div>

          <h2>TWO WORDS</h2>

          <p>
            ENTER TWO WORDS AND CALCULATE THEIR
            SEMANTIC SIMILARITY.
          </p>

          <div className="mode-flow">
            WORD 01
            <span>→</span>
            VECTOR
            <span>→</span>
            SCORE
            <span>←</span>
            VECTOR
            <span>←</span>
            WORD 02
          </div>

          <PixelButton onClick={() => navigate("/two-word")}>
            ENTER MODE
          </PixelButton>

        </PixelCard>

        <PixelCard className="mode-card">

          <div className="mode-icon green-icon">
            ▦
          </div>

          <div className="mode-number">
            MODE 02
          </div>

          <h2>SENTENCE</h2>

          <p>
            ENTER A SENTENCE AND EXPLORE THE WORD
            VECTORS INSIDE IT.
          </p>

          <div className="mode-flow">
            SENTENCE
            <span>→</span>
            WORDS
            <span>→</span>
            VECTORS
            <span>→</span>
            ANALYSIS
          </div>

          <PixelButton
            className="green-button"
            onClick={() => navigate("/sentence")}
          >
            ENTER MODE
          </PixelButton>

        </PixelCard>

      </section>

    </main>
  );
}

export default ModeSelect;