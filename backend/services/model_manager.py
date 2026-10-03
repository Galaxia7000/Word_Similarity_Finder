from pathlib import Path
from typing import Optional

from gensim.models import KeyedVectors


class ModelManager:
    """
    Loads and manages the local compact Word2Vec model.

    The model is stored with the application so that deployment
    does not require downloading the original multi-gigabyte model.
    """

    def __init__(
        self,
        model_path: str
    ):
        self.model_path = Path(model_path)

        self.model: Optional[KeyedVectors] = None

        self.loading = False

    def load_model(self) -> KeyedVectors:
        """
        Load the local Word2Vec model on demand.
        """

        if self.model is not None:
            return self.model

        if self.loading:
            raise RuntimeError(
                "Word2Vec model is already being loaded."
            )

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Word2Vec model not found at: "
                f"{self.model_path}"
            )

        self.loading = True

        try:

            print(
                f"Loading Word2Vec model from: "
                f"{self.model_path}"
            )

            self.model = (
                KeyedVectors.load_word2vec_format(
                    str(self.model_path),
                    binary=True
                )
            )

            print(
                "Word2Vec model loaded successfully."
            )

            print(
                f"Vocabulary size: "
                f"{len(self.model.key_to_index):,}"
            )

            print(
                f"Vector size: "
                f"{self.model.vector_size}"
            )

            return self.model

        finally:
            self.loading = False

    def is_loaded(self) -> bool:
        return self.model is not None

    def contains_word(
        self,
        word: str
    ) -> bool:

        model = self.load_model()

        return word in model.key_to_index

    def get_vector(
        self,
        word: str
    ):

        model = self.load_model()

        if word not in model.key_to_index:

            raise KeyError(
                f"The word '{word}' is not present "
                f"in the model vocabulary."
            )

        return model[word]

    def get_vector_size(self) -> int:

        model = self.load_model()

        return model.vector_size

    def get_vocabulary_size(self) -> int:

        model = self.load_model()

        return len(model.key_to_index)

    def get_most_similar(
        self,
        word: str,
        top_n: int = 10
    ):

        model = self.load_model()

        if word not in model.key_to_index:

            raise KeyError(
                f"The word '{word}' is not present "
                f"in the model vocabulary."
            )

        return model.most_similar(
            word,
            topn=top_n
        )


model_manager: Optional[ModelManager] = None