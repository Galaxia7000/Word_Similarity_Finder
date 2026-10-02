from typing import Any, Dict

from services.vector_engine import VectorEngine
from services.similarity_engine import SimilarityEngine


class ComparisonService:
    """
    Coordinates vector retrieval and similarity calculation.

    This is the layer that connects:
    
    User words
        ↓
    Vector Engine
        ↓
    Similarity Engine
    """

    def __init__(
        self,
        vector_engine: VectorEngine,
        similarity_engine: SimilarityEngine
    ):
        self.vector_engine = vector_engine
        self.similarity_engine = similarity_engine

    def compare_words(
        self,
        word_a: str,
        word_b: str
    ) -> Dict[str, Any]:
        """
        Compare two words using their Word2Vec vectors.
        """

        word_a_info = self.vector_engine.get_vector_information(
            word_a
        )

        word_b_info = self.vector_engine.get_vector_information(
            word_b
        )

        similarity_result = self.similarity_engine.compare_vectors(
            self.vector_engine.get_vector(word_a_info["word"]),
            self.vector_engine.get_vector(word_b_info["word"])
        )

        return {
            "word_a": word_a_info,
            "word_b": word_b_info,
            "similarity": similarity_result
        }