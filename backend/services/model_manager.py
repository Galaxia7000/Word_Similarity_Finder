from typing import Optional

import gensim.downloader as api


class ModelManager:
    """
    Handles loading and accessing the configured
    Word2Vec model.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.loading = False

    def load_model(self):
        """
        Load the Word2Vec model on demand.

        Gensim caches the downloaded model locally,
        so subsequent loads can reuse the cached file.
        """

        if self.model is not None:
            return self.model

        if self.loading:
            raise RuntimeError(
                "Word2Vec model is already being loaded."
            )

        self.loading = True

        try:
            print(
                f"Loading Word2Vec model: "
                f"{self.model_name}"
            )

            self.model = api.load(
                self.model_name
            )

            print(
                "Word2Vec model loaded successfully."
            )

            return self.model

        finally:
            self.loading = False

    def is_loaded(self) -> bool:
        """
        Check whether the model is currently loaded.
        """

        return self.model is not None

    def contains_word(
        self,
        word: str
    ) -> bool:
        """
        Check whether the word exists in
        the model vocabulary.
        """

        model = self.load_model()

        return word in model.key_to_index

    def get_vector(
        self,
        word: str
    ):
        """
        Retrieve the vector associated with a word.
        """

        model = self.load_model()

        if word not in model.key_to_index:
            raise KeyError(
                f"The word '{word}' is not present "
                f"in the model vocabulary."
            )

        return model[word]

    def get_vector_size(self) -> int:
        """
        Return vector dimensionality.
        """

        model = self.load_model()

        return model.vector_size

    def get_vocabulary_size(self) -> int:
        """
        Return vocabulary size.
        """

        model = self.load_model()

        return len(model.key_to_index)

    def get_most_similar(
        self,
        word: str,
        top_n: int = 10
    ):
        """
        Retrieve semantically similar words.
        """

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