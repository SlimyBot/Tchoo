"""
Backend de l'application SAE.
"""

from fastapi import FastAPI
from socketio import ASGIApp, AsyncServer
from starlette.middleware.cors import CORSMiddleware

from .controller import api_router
from .controller.socket.session import SessionNamespace
from .model.config import settings
from .model.database import init_db
from .model.socket_manager import manager

init_db()


# Serveur HTTP
app = FastAPI(
    title=settings.PROJECT_NAME,
    summary="API de l'application SAE.",
    license_info={"name": "AGPLv3", "url": "https://www.gnu.org/licenses/agpl-3.0.fr.html"},
    openapi_tags=[
        {
            "name": "users",
            "description": "Opérations relatives aux utilisateurs, à l'authentification et à la déconnexion.",
        },
    ],
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Autoriser les CORS depuis les url de developement
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "https://localhost:8443"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

# Serveur Socket.IO
_sio = AsyncServer(client_manager=manager, async_mode="asgi", cors_allowed_origins=[])  # FastAPI s'occupe des Cors
_sio_app = ASGIApp(_sio, socketio_path="")

_sio.register_namespace(SessionNamespace("/session"))

app.mount("/ws", _sio_app)


def dev_run():
    """
    Pour pouvoir lancer l'application en mode développement avec Poetry.
    """
    import sys

    import uvicorn

    uvicorn.run("sae_backend:app", reload=True)
    sys.exit()
