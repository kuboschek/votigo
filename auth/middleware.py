from typing import Annotated, Any, Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from auth.models import User
from .jwks import get_validated_payload


auth = HTTPBearer(bearerFormat="jwt", scheme_name="oidc", description="JWT token for authentication")

async def _get_token_payload(auth = Depends(auth)) -> Optional[dict[str, Any]]:
        try:
            # Verify and decode the JWT token
            return get_validated_payload(auth.credentials)

        except Exception as e:
            return None # Checking the authenticated user is up to the app
    

def _get_current_user(payload = Depends(_get_token_payload)) -> User:
    if not payload:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return User(**payload)

CurrentUser = Annotated[User, Depends(_get_current_user)]


_fake_auth = HTTPBasic()

def _get_fake_user(fake_auth: HTTPBasicCredentials = Depends(_fake_auth)) -> User:
     return User(
            sub=fake_auth.username or "fake_user",
            iss="https://example.com",
            email=f"{fake_auth.username or 'fake_user'}@example.com",
            name=fake_auth.username or "Fake User",
            picture="https://example.com/fake_user.jpg",
     )

FakeUser = Annotated[User, Depends(_get_fake_user)]