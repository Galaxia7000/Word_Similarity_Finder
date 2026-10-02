from fastapi import APIRouter, HTTPException
from services.comparison_service import ComparisonService
from services.similarity_engine import SimilarityEngine
from services import model_manager as model_manager_module
from services.vector_engine import VectorEngine


router = APIRouter(
    prefix="/api/words",
    tags=["Word Analysis"]
)


def get_vector_engine() -> VectorEngine:
    """
    Create a VectorEngine using the currently initialized model manager.
    """

    if model_manager_module.model_manager is None:
        raise HTTPException(
            status_code=500,
            detail="Word2Vec model manager has not been initialized."
        )

    return VectorEngine(
        model_manager=model_manager_module.model_manager
    )


@router.get("/compare/{word_a}/{word_b}")
def compare_two_words(
    word_a: str,
    word_b: str
):
    """
    Compare two words using cosine similarity between
    their Word2Vec vectors.
    """

    vector_engine = get_vector_engine()

    comparison_service = ComparisonService(
        vector_engine=vector_engine,
        similarity_engine=SimilarityEngine()
    )

    try:
        return comparison_service.compare_words(
            word_a,
            word_b
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except KeyError as error:
        # Avoid the ugly extra quotation marks produced by KeyError.
        message = str(error)

        if (
            message.startswith("'")
            and message.endswith("'")
        ):
            message = message[1:-1]

        raise HTTPException(
            status_code=404,
            detail=message
        )

@router.get("/{word}")
def get_word_information(word: str):
    """
    Return complete Word2Vec vector information for one word.
    """

    vector_engine = get_vector_engine()

    try:
        return vector_engine.get_vector_information(word)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except KeyError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.get("/{word}/similar")
def get_similar_words(
    word: str,
    top_n: int = 10
):
    """
    Return words that are semantically similar to the supplied word.

    Similarity calculation itself will eventually move into the
    Similarity Engine module. For now, this route continues using
    Gensim's built-in nearest-neighbor functionality.
    """

    if top_n < 1 or top_n > 50:
        raise HTTPException(
            status_code=400,
            detail="top_n must be between 1 and 50."
        )

    if model_manager_module.model_manager is None:
        raise HTTPException(
            status_code=500,
            detail="Word2Vec model manager has not been initialized."
        )

    vector_engine = get_vector_engine()

    try:
        normalized_word = vector_engine.normalize_word(word)

        results = model_manager_module.model_manager.get_most_similar(
            normalized_word,
            top_n=top_n
        )

        return {
            "word": normalized_word,
            "results": [
                {
                    "word": similar_word,
                    "similarity": float(score)
                }
                for similar_word, score in results
            ]
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except KeyError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )