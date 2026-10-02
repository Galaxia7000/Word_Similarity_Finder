import re
from typing import List


class TextProcessor:
    """
    Handles basic sentence tokenization and normalization.

    Vocabulary filtering is handled separately by the Vector Engine,
    because whether a word can be analyzed depends on the active model.
    """

    WORD_PATTERN = re.compile(r"[A-Za-z]+")

    @classmethod
    def tokenize(cls, text: str) -> List[str]:
        """
        Extract alphabetic word tokens from input text.
        """

        if not isinstance(text, str):
            raise ValueError("Sentence input must be text.")

        return cls.WORD_PATTERN.findall(text)

    @classmethod
    def normalize_tokens(
        cls,
        tokens: List[str]
    ) -> List[str]:
        """
        Convert tokens to lowercase and remove empty values.
        """

        return [
            token.lower()
            for token in tokens
            if token.strip()
        ]

    @classmethod
    def process(
        cls,
        text: str
    ) -> List[str]:
        """
        Tokenize and normalize the input sentence.
        """

        tokens = cls.tokenize(text)

        return cls.normalize_tokens(tokens)