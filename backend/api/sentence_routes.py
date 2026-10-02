from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services import model_manager as model_manager_module
from services.sentence_service import SentenceService
from services.similarity_engine import SimilarityEngine
from services.vector_engine import VectorEngine


router = APIRouter(
    prefix="/api/sentences",
    tags=["Sentence Analysis"]
)


class SentenceRequest(BaseModel):
    text: str


def get_sentence_service() -> SentenceService:
    """
    Create a sentence analysis service using the active model.
    """

    if model_manager_module.model_manager is None:
        raise HTTPException(
            status_code=500,
            detail="Word2Vec model manager has not been initialized."
        )

    vector_engine = VectorEngine(
        model_manager=model_manager_module.model_manager
    )

    similarity_engine = SimilarityEngine()

    return SentenceService(
        vector_engine=vector_engine,
        similarity_engine=similarity_engine
    )


@router.post("/analyze")
def analyze_sentence(request: SentenceRequest):
    """
    Analyze a sentence and return:

    - original tokens
    - model-known words
    - words not found in the model library
    - Word2Vec vectors
    - pairwise similarity matrix
    - strongest relationship
    """

    service = get_sentence_service()

    try:

        return service.analyze(
            request.text
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except KeyError as error:

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