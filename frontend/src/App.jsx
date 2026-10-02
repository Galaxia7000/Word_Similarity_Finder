import React from "react";
import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Home from "./pages/Home";
import ModeSelect from "./pages/ModeSelect";
import TwoWordAnalysis from "./pages/TwoWordAnalysis";
import SentenceAnalysis from "./pages/SentenceAnalysis";

function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/modes"
          element={<ModeSelect />}
        />

        <Route
          path="/two-word"
          element={<TwoWordAnalysis />}
        />
        <Route
         path="/sentence"
        element={<SentenceAnalysis />}
        />
      </Routes>

    </BrowserRouter>
  );
}


export default App;