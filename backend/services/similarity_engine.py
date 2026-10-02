from typing import Any, Dict

import numpy as np


class SimilarityEngine:
    """
    Performs mathematical comparisons between word vectors.

    This module is independent of the Word2Vec model itself.
    It only needs numerical vectors.
    """

    @staticmethod
    def cosine_similarity(
        vector_a: np.ndarray,
        vector_b: np.ndarray
    ) -> float:
        """
        Calculate cosine similarity between two vectors.

        Returns a value between -1 and 1.
        """

        vector_a = np.asarray(vector_a, dtype=np.float64)
        vector_b = np.asarray(vector_b, dtype=np.float64)

        if vector_a.ndim != 1 or vector_b.ndim != 1:
            raise ValueError(
                "Both vectors must be one-dimensional."
            )

        if vector_a.shape != vector_b.shape:
            raise ValueError(
                "Both vectors must have the same dimensions."
            )

        norm_a = np.linalg.norm(vector_a)
        norm_b = np.linalg.norm(vector_b)

        if norm_a == 0 or norm_b == 0:
            raise ValueError(
                "Cosine similarity cannot be calculated for a zero vector."
            )

        similarity = np.dot(vector_a, vector_b) / (
            norm_a * norm_b
        )

        # Protect against tiny floating-point errors.
        similarity = np.clip(similarity, -1.0, 1.0)

        return float(similarity)

    @staticmethod
    def similarity_percentage(
        similarity: float
    ) -> float:
        """
        Convert cosine similarity into a percentage-style value.

        A raw cosine score ranges from -1 to 1.
        This maps that interval to 0% to 100%.
        """

        percentage = ((similarity + 1) / 2) * 100

        return float(np.clip(percentage, 0, 100))

    @staticmethod
    def classify_similarity(
        similarity: float
    ) -> str:
        """
        Provide a descriptive category for a similarity score.

        These categories are descriptive UI labels rather than
        machine-learning predictions.
        """

        if similarity >= 0.80:
            return "Very Similar"

        if similarity >= 0.60:
            return "Highly Related"

        if similarity >= 0.40:
            return "Related"

        if similarity >= 0.20:
            return "Somewhat Related"

        if similarity >= 0:
            return "Weakly Related"

        return "Opposite / Unrelated"

    @classmethod
    def compare_vectors(
        cls,
        vector_a: np.ndarray,
        vector_b: np.ndarray
    ) -> Dict[str, Any]:
        """
        Perform a complete vector comparison.
        """

        similarity = cls.cosine_similarity(
            vector_a,
            vector_b
        )

        return {
            "cosine_similarity": similarity,
            "percentage": cls.similarity_percentage(
                similarity
            ),
            "classification": cls.classify_similarity(
                similarity
            )
        }