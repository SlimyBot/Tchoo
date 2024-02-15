from datetime import timedelta
from typing import Annotated
from urllib.parse import quote

from cas import CASClient
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from ...model.api.api_models import CasSetup, CasSetupStage, Token
from ...model.api.auth import create_access_token
from ...model.database import get_db
from ...model.database.operations import get_user, register_user
from ...model.config import settings

IS_PROD = settings.DEPLOY_MODE == "prod"

BACKEND_BASE = "https://10.22.27.3" if IS_PROD else "http://localhost:8000"
FRONTEND_BASE = "https://10.22.27.3" if IS_PROD else "http://localhost:5173"

cas_client = CASClient(
    version=3,
    service_url=f"{BACKEND_BASE}/api/cas/verify_ticket",
    server_url="https://10.22.27.7:8443/cas/",
    verify_ssl_certificate=False,
)

router = APIRouter()


@router.get("/login")
def login_step1_route() -> CasSetup:
    """
    Renvoie l'url qui doit être utilisée pour aller sur le CAS.
    """
    return CasSetup(stage=CasSetupStage.must_cas_login, url=cas_client.get_login_url())


@router.post("/login")
def login_route(db: Annotated[Session, Depends(get_db)], ticket: str) -> CasSetup:
    """
    Vérifie le ticket du CAS et authentifie l'utilisateur.
    """
    user, attributes, _ = cas_client.verify_ticket(ticket)

    if not user:
        return CasSetup(stage=CasSetupStage.failed_login)

    # est-ce que l'utilisateur est déjà dans la BDD ?
    user_in_db = get_user(db, attributes["mail"])  # type: ignore

    if not user_in_db:
        user_in_db = register_user(
            db,
            attributes["givenname"],  # type: ignore
            attributes["sn"],  # type: ignore
            attributes["mail"],  # type: ignore
            attributes["edupersonprimaryaffiliation"],  # type: ignore
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_in_db.email, "aff": user_in_db.affiliation.value},  # type: ignore
        expires_delta=access_token_expires,
    )

    return CasSetup(
        stage=CasSetupStage.logged_in,
        token=Token(access_token=access_token, token_type="bearer"),  # nosec hardcoded_password_funcarg
    )


@router.get("/verify_ticket")
def verify_ticket_route(ticket: str):
    """
    Compatibilité avec les SPA.
    """
    return RedirectResponse(f"{FRONTEND_BASE}/casLogin/{quote(ticket)}")


@router.get("/logout_url")
def get_logout_url_route() -> dict[str, str]:
    """
    Renvoie l'url pour la déconnexion.
    """
    return {"url": cas_client.get_logout_url(f"{FRONTEND_BASE}/")}
