import os


class Settings:
    """
    Central application configuration.
    """

    APP_NAME = "Word Similarity Finder API"

    MODEL_NAME = os.getenv(
        "W2V_MODEL_NAME",
        "word2vec-google-news-300"
    )

    VECTOR_PREVIEW_SIZE = 12

    MAX_SENTENCE_WORDS = 20

    FRONTEND_URL = os.getenv(
        "FRONTEND_URL",
        "http://localhost:5173"
    )

    GENSIM_DATA_DIR = os.getenv(
        "GENSIM_DATA_DIR",
        os.path.expanduser("~/gensim-data")
    )


settings = Settings()