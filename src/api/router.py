"""Endpoints"""
from fastapi import APIRouter, Body, Request
from src.api.schemas import HealthCheckResponse, MatchingResponse, MatchingRequest
from src.api.service import MatchingService


router = APIRouter()


@router.get("/health", tags=["Health"], response_model=HealthCheckResponse)
async def health_check():
    """
    Checks if the service is working
    """
    return HealthCheckResponse()


@router.post("/api/match", tags=["Matching"], response_model=MatchingResponse)
async def matching(request: Request, data: MatchingRequest = Body(embed=False)):
    resume = data.resume
    vacancy = data.vacancy
    score = MatchingService.match(resume, vacancy, request.app.state.model)
    return MatchingResponse(value=score, message="Привет")
