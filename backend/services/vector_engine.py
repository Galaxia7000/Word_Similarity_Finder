from typing import Any, Dict

import numpy as np

from core.config import settings
from services.model_manager import ModelManager


class VectorEngine:
    """
    Handles all operations related to retrieving and presenting
    Word2Vec vectors.

    This module does not calculate word similarity.
    Similarity will be handled by the Similarity Engine.
    """

    def __init__(
        self,
        model_manager: ModelManager,
        preview_size: int = settings.VECTOR_PREVIEW_SIZE
    ):
        self.model_manager = model_manager
        self.preview_size = preview_size

    def normalize_word(self, word: str) -> str:
        """
        Clean user input and find the corresponding vocabulary word.

        The model is case-sensitive for some entries, so we first
        try the exact input and then a lowercase version.
        """

        if not isinstance(word, str):
            raise ValueError("Word must be a string.")

        cleaned_word = word.strip()

        if not cleaned_word:
            raise ValueError("Word cannot be empty.")

        candidates = [
            cleaned_word,
            cleaned_word.lower()
        ]

        for candidate in candidates:
            if self.model_manager.contains_word(candidate):
                return candidate

        raise KeyError(
            f"'{cleaned_word}' was not found in the Word2Vec vocabulary."
        )

    def get_vector(self, word: str) -> np.ndarray:
        """
        Retrieve the numerical vector for a validated word.
        """

        normalized_word = self.normalize_word(word)

        return self.model_manager.get_vector(normalized_word)

    def get_vector_information(self, word: str) -> Dict[str, Any]:
        """
        Retrieve a complete, structured representation of a word vector.

        Includes:
        - normalized word
        - vector dimensions
        - full vector
        - vector preview
        - numerical statistics
        """

        normalized_word = self.normalize_word(word)

        vector = self.model_manager.get_vector(normalized_word)

        # Convert explicitly to a NumPy array so numerical operations
        # are handled consistently.
        vector_array = np.asarray(vector, dtype=np.float32)

        vector_list = vector_array.tolist()

        return {
            "word": normalized_word,

            "vector_size": int(vector_array.size),

            "vector_preview": vector_list[:self.preview_size],

            "vector": vector_list,

            "statistics": {
                "minimum": float(np.min(vector_array)),
                "maximum": float(np.max(vector_array)),
                "mean": float(np.mean(vector_array)),
                "l2_norm": float(np.linalg.norm(vector_array)),
            }
        }

    def get_vector_preview(self, word: str) -> Dict[str, Any]:
        """
        Retrieve only a compact vector preview.

        Useful when the frontend does not need all 300 values.
        """

        normalized_word = self.normalize_word(word)

        vector = self.model_manager.get_vector(normalized_word)

        vector_array = np.asarray(vector, dtype=np.float32)

        return {
            "word": normalized_word,
            "vector_size": int(vector_array.size),
            "vector_preview": vector_array[:self.preview_size].tolist()
        }