"""Application"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api.router import router as api_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    """
    Executes start actions
    """
    # add model loading
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Resume Matching",
    version="0.0.1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.include_router(api_router)
