import React from "react";
import { useNavigate } from "react-router-dom";
import PixelButton from "../components/PixelButton";
import PixelCard from "../components/PixelCard";

function Home() {
  const navigate = useNavigate();

  return (
    <main className="home-page">
      <div className="pixel-stars">
        <span className="star star-one">✦</span>
        <span className="star star-two">✦</span>
        <span className="star star-three">✦</span>
        <span className="star star-four">✦</span>
      </div>

      <section className="hero">

        <div className="hero-badge">
          WORD2VEC // NLP ENGINE
        </div>

        <h1 className="hero-title">
          WORD
          <span>SIMILARITY</span>
          FINDER
        </h1>

        <p className="hero-subtitle">
          EXPLORE WORDS. DISCOVER CONNECTIONS.
          <br />
          LET THE VECTOR SPACE DO THE TALKING.
        </p>

        <PixelButton
          className="start-button"
          onClick={() => navigate("/modes")}
        >
          START ANALYSIS
        </PixelButton>

        <div className="hero-decoration">
          <div className="pixel-orb pink-orb"></div>
          <div className="pixel-orb green-orb"></div>
          <div className="pixel-orb cream-orb"></div>
        </div>
      </section>

      <section className="feature-section">

        <PixelCard>
          <div className="card-number">01</div>
          <div className="card-icon">↔</div>
          <h2>TWO WORDS</h2>
          <p>
            Enter two English words and discover how closely
            their meanings are related.
          </p>
        </PixelCard>

        <PixelCard>
          <div className="card-number">02</div>
          <div className="card-icon">▦</div>
          <h2>SENTENCE MODE</h2>
          <p>
            Break sentences into words, inspect their vectors
            and explore semantic relationships.
          </p>
        </PixelCard>

        <PixelCard>
          <div className="card-number">03</div>
          <div className="card-icon">◆</div>
          <h2>VECTOR VIEW</h2>
          <p>
            See the numerical representation behind the words
            powering the similarity calculations.
          </p>
        </PixelCard>

      </section>

      <footer className="pixel-footer">
        <span>W2V FINDER</span>
        <span>•</span>
        <span>SEMANTIC LAB</span>
      </footer>

    </main>
  );
}

export default Home;