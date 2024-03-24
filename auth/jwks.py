import os
from typing import Any
from fastapi import HTTPException
import jwt
import requests_cache

JWKS_URI = os.getenv("JWKS_URL", "")
ALGORITHMS = ["RS256"]

session = requests_cache.CachedSession('jwks-cache', cache_control=True)

def get_jwks(url: str):
    jwks_response = session.get(url)
    return jwks_response.json()

def get_validated_payload(token: str) -> Any:
    """
    This function validates the jwt token and extracts
    the payload from it.

    Args:
        token (str): A valid JWT token

    Raises:
        HTTPException: The token uses an unknown algorithm.
        HTTPException: The token uses an unknown key.
        HTTPException: The token has expired.
        HTTPException: The token is invalid.

    Returns:
        Any: The payload of the validated JWT token.
    """
    jwks = get_jwks(JWKS_URI)
    public_key = None
    try:
        header = jwt.get_unverified_header(token)
        kid = header["kid"]
        if header["alg"] not in ALGORITHMS:
            raise HTTPException(status_code=401, detail="Invalid token")
        for key in jwks["keys"]:
            if key["kid"] == kid:
                public_key = jwt.algorithms.get_default_algorithms()[
                    header["alg"]
                ].from_jwk(key)
                break
        if public_key is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return jwt.decode(token, public_key, algorithms=[header["alg"]])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")