from datetime import timedelta
from sae_backend.model.api.auth import create_access_token
from sae_backend.model.config import settings


def get_token_for(email):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": email, "aff": None}, expires_delta=access_token_expires)

    return access_token
