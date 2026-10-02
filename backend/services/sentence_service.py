from typing import Any, Dict, List, Tuple

import numpy as np

from core.config import settings
from services.similarity_engine import SimilarityEngine
from services.text_processor import TextProcessor
from services.vector_engine import VectorEngine


class SentenceService:
    """
    Coordinates sentence tokenization, vocabulary checking,
    vector retrieval, and pairwise similarity analysis.
    """

    def __init__(
        self,
        vector_engine: VectorEngine,
        similarity_engine: SimilarityEngine
    ):
        self.vector_engine = vector_engine
        self.similarity_engine = similarity_engine

    def _find_valid_words(
        self,
        tokens: List[str]
    ) -> Tuple[List[str], List[str]]:
        """
        Separate words according to whether they exist in the
        active Word2Vec vocabulary.

        Words found in the model:
            → analyzed

        Words not found in the model:
            → labeled as stop words by this application's UI
        """

        valid_words = []
        stop_words = []

        for token in tokens:

            try:
                normalized = self.vector_engine.normalize_word(token)

                if normalized not in valid_words:
                    valid_words.append(normalized)

            except KeyError:

                if token not in stop_words:
                    stop_words.append(token)

        return valid_words, stop_words

    def _build_vector_information(
        self,
        words: List[str],
        vectors: Dict[str, np.ndarray]
    ) -> List[Dict[str, Any]]:
        """
        Build vector information from vectors that have already
        been retrieved from the model.

        This avoids loading/retrieving the same vector repeatedly.
        """

        vector_information = []

        for word in words:

            vector_array = np.asarray(
                vectors[word],
                dtype=np.float32
            )

            vector_list = vector_array.tolist()

            preview_size = settings.VECTOR_PREVIEW_SIZE

            vector_information.append({
                "word": word,

                "vector_size": int(vector_array.size),

                "vector_preview": (
                    vector_list[:preview_size]
                ),

                "vector": vector_list,

                "statistics": {
                    "minimum": float(
                        np.min(vector_array)
                    ),

                    "maximum": float(
                        np.max(vector_array)
                    ),

                    "mean": float(
                        np.mean(vector_array)
                    ),

                    "l2_norm": float(
                        np.linalg.norm(vector_array)
                    )
                }
            })

        return vector_information

    def _build_similarity_matrix(
        self,
        words: List[str],
        vectors: Dict[str, np.ndarray]
    ) -> List[Dict[str, Any]]:
        """
        Build a pairwise cosine similarity matrix.

        The diagonal is always 1.0 because a word compared with
        itself has cosine similarity of 1.
        """

        matrix = []

        for row_word in words:

            row_values = []

            for column_word in words:

                if row_word == column_word:

                    score = 1.0

                else:

                    score = (
                        self.similarity_engine.cosine_similarity(
                            vectors[row_word],
                            vectors[column_word]
                        )
                    )

                row_values.append({
                    "word": column_word,

                    "cosine_similarity": float(
                        score
                    ),

                    "percentage": float(
                        self.similarity_engine.similarity_percentage(
                            score
                        )
                    )
                })

            matrix.append({
                "word": row_word,
                "values": row_values
            })

        return matrix

    def _find_strongest_pair(
        self,
        words: List[str],
        matrix: List[Dict[str, Any]]
    ):
        """
        Find the strongest relationship between two different words.
        """

        if len(words) < 2:
            return None

        strongest_pair = None
        highest_score = float("-inf")

        for row in matrix:

            for cell in row["values"]:

                # Ignore diagonal values.
                if row["word"] == cell["word"]:
                    continue

                score = cell["cosine_similarity"]

                if score > highest_score:

                    highest_score = score

                    strongest_pair = {
                        "word_a": row["word"],

                        "word_b": cell["word"],

                        "cosine_similarity": float(
                            score
                        ),

                        "percentage": float(
                            cell["percentage"]
                        ),

                        "classification": (
                            self.similarity_engine.classify_similarity(
                                score
                            )
                        )
                    }

        return strongest_pair

    def analyze(
        self,
        text: str
    ) -> Dict[str, Any]:
        """
        Complete sentence-analysis pipeline.
        """

        if not isinstance(text, str):
            raise ValueError(
                "Sentence input must be text."
            )

        if not text.strip():
            raise ValueError(
                "Sentence cannot be empty."
            )

        # ----------------------------------------
        # TOKENIZATION
        # ----------------------------------------

        tokens = TextProcessor.process(text)

        if not tokens:
            raise ValueError(
                "No recognizable words were found in the input."
            )

        # ----------------------------------------
        # VOCABULARY CHECK
        # ----------------------------------------

        valid_words, stop_words = (
            self._find_valid_words(tokens)
        )

        if not valid_words:

            raise ValueError(
                "None of the input words were found in "
                "the Word2Vec library."
            )

        if len(valid_words) > settings.MAX_SENTENCE_WORDS:

            raise ValueError(
                f"Please use no more than "
                f"{settings.MAX_SENTENCE_WORDS} "
                f"unique vocabulary words."
            )

        # ----------------------------------------
        # RETRIEVE VECTORS ONCE
        # ----------------------------------------

        vectors = {
            word: self.vector_engine.get_vector(word)
            for word in valid_words
        }

        # ----------------------------------------
        # VECTOR INFORMATION
        # ----------------------------------------

        vector_information = (
            self._build_vector_information(
                valid_words,
                vectors
            )
        )

        # ----------------------------------------
        # SIMILARITY MATRIX
        # ----------------------------------------

        similarity_matrix = (
            self._build_similarity_matrix(
                valid_words,
                vectors
            )
        )

        # ----------------------------------------
        # STRONGEST CONNECTION
        # ----------------------------------------

        strongest_pair = (
            self._find_strongest_pair(
                valid_words,
                similarity_matrix
            )
        )

        # ----------------------------------------
        # RESPONSE
        # ----------------------------------------

        return {
            "input_text": text,

            "original_tokens": tokens,

            "tokens": tokens,

            "stop_words": stop_words,

            "valid_words": valid_words,

            "word_count": len(tokens),

            "processed_word_count": len(valid_words),

            "unique_valid_word_count": len(valid_words),

            "vectors": vector_information,

            "similarity_matrix": similarity_matrix,

            "strongest_pair": strongest_pair
        }