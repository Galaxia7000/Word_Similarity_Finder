const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";


export async function compareWords(wordA, wordB) {
  const encodedWordA = encodeURIComponent(
    wordA.trim()
  );

  const encodedWordB = encodeURIComponent(
    wordB.trim()
  );

  const response = await fetch(
    `${API_BASE_URL}/api/words/compare/${encodedWordA}/${encodedWordB}`
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Unable to compare the words."
    );
  }

  return data;
}


export async function analyzeSentence(
  text,
  signal
) {
  const response = await fetch(
    `${API_BASE_URL}/api/sentences/analyze`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        text: text.trim(),
      }),

      signal,
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail ||
      "Unable to analyze the sentence."
    );
  }

  return data;
}