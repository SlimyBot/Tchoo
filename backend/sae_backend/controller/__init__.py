"""
Controlleur de l'API.

Interface de communication de l'API avec le frontend.
"""

from fastapi import APIRouter

from .routes import end_survey, groups, question, sessions, users, results, sso_cas

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(question.router, prefix="/question", tags=["question"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(end_survey.router, prefix="/endSurvey", tags=["endSurvey"])
api_router.include_router(results.router, prefix="/results", tags=["results"])
api_router.include_router(sso_cas.router, prefix="/cas", tags=["cas"])
