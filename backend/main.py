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

if settings.FRONTEND_URL not in allowed_origins:

    allowed_origins.append(
        settings.FRONTEND_URL
    )


app.add_middleware(
    CORSMiddleware,

    allow_origins=allowed_origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# --------------------------------------------------
# MODEL
# --------------------------------------------------

model_manager_module.model_manager = (
    ModelManager(
        settings.MODEL_PATH
    )
)


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

app.include_router(
    word_router
)

app.include_router(
    sentence_router
)


# --------------------------------------------------
# BASIC ENDPOINTS
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "message":
            "Word Similarity Finder API is running.",

        "model":
            "word2vec-google-news-50k"
    }


@app.get("/health")
def health_check():

    return {
        "status":
            "online",

        "service":
            "word-similarity-finder",

        "model_loaded":
            model_manager_module
            .model_manager
            .is_loaded()
    }