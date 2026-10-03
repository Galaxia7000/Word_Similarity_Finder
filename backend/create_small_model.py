from pathlib import Path

import gensim.downloader as api
from gensim.models import KeyedVectors


MODEL_NAME = "word2vec-google-news-300"

# Number of vocabulary entries to keep.
VOCAB_SIZE = 50000

OUTPUT_DIR = Path("models")
OUTPUT_FILE = OUTPUT_DIR / "word2vec-google-news-50k.bin"


def main():
    print("=" * 60)
    print("WORD2VEC MODEL COMPRESSION")
    print("=" * 60)

    print("\nLoading original Google News Word2Vec model...")
    print("This may take some time.\n")

    original_model = api.load(MODEL_NAME)

    print("Original model loaded.")
    print(
        f"Original vocabulary size: "
        f"{len(original_model.key_to_index):,}"
    )

    print(
        f"Creating compact model with top "
        f"{VOCAB_SIZE:,} words..."
    )

    # Keep the most frequent vocabulary entries.
    words = original_model.index_to_key[:VOCAB_SIZE]

    # Retrieve vectors for those words.
    vectors = original_model.get_normed_vectors()[:VOCAB_SIZE]

    # Create a new KeyedVectors object.
    small_model = KeyedVectors(
        vector_size=original_model.vector_size
    )

    small_model.add_vectors(
        words,
        vectors
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        f"\nSaving compact model to:\n"
        f"{OUTPUT_FILE}"
    )

    # Save in standard word2vec binary format.
    small_model.save_word2vec_format(
        str(OUTPUT_FILE),
        binary=True
    )

    file_size_mb = (
        OUTPUT_FILE.stat().st_size
        / (1024 * 1024)
    )

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)

    print(
        f"Vocabulary: {len(words):,} words"
    )

    print(
        f"Vector dimensions: "
        f"{small_model.vector_size}"
    )

    print(
        f"Model size: "
        f"{file_size_mb:.2f} MB"
    )

    print(
        f"Saved to: "
        f"{OUTPUT_FILE.resolve()}"
    )


if __name__ == "__main__":
    main()