import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.word_routes import router as word_router
from api.sentence_routes import router as sentence_router

from core.config import settings

from services.model_manager import ModelManager
from services import model_manager as model_manager_module


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Backend API for the Word2Vec-based "
        "Word Similarity Finder."
    ),
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

allowed_origins = [
    "http://localhost:5173"
]

if settings.FRONTEND_URL:
    allowed_origins.append(
        settings.FRONTEND_URL
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Model initialization
# --------------------------------------------------

# Make the Gensim cache location configurable.
# On Render we will point this to the persistent disk.
os.environ["GENSIM_DATA_DIR"] = (
    settings.GENSIM_DATA_DIR
)


model_manager_module.model_manager = (
    ModelManager(settings.MODEL_NAME)
)


# --------------------------------------------------
# Routes
# --------------------------------------------------

app.include_router(word_router)

app.include_router(sentence_router)


# --------------------------------------------------
# Basic endpoints
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": (
            "Word Similarity Finder API is running."
        ),
        "model": settings.MODEL_NAME
    }


@app.get("/health")
def health_check():
    return {
        "status": "online",
        "service": "word-similarity-finder",
        "model_loaded": (
            model_manager_module
            .model_manager
            .is_loaded()
        )
    }