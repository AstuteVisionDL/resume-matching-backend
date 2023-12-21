"""Application"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .models.dependencies import get_actual_model
from src.api.router import router as api_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    """
    Executes start actions
    """
    application.state.model = get_actual_model()
    yield


app = FastAPI(
    title="Resume Matching",
    version="0.0.1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

app.include_router(api_router)
