import os
from pathlib import Path


BASE_DIR = Path(
    __file__
).resolve().parent.parent


class Settings:
    """
    Central application configuration.
    """

    APP_NAME = "Word Similarity Finder API"

    MODEL_PATH = os.getenv(
        "W2V_MODEL_PATH",
        str(
            BASE_DIR
            / "models"
            / "word2vec-google-news-50k.bin"
        )
    )

    VECTOR_PREVIEW_SIZE = 12

    MAX_SENTENCE_WORDS = 20

    FRONTEND_URL = os.getenv(
        "FRONTEND_URL",
        "http://localhost:5173"
    )


settings = Settings()