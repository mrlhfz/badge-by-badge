import uuid
from collections.abc import Callable
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient, PyJWKClientConnectionError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.enums import Role
from app.models.people import Profile

# Reads the Authorization header
bearer_scheme = HTTPBearer()

# Fetches Supabase's public keys
jwks_client = PyJWKClient(f"{settings.supabase_url}/auth/v1/.well-known/jwks.json")


# Checks the token and returns the user ID
def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> str:
    token = credentials.credentials
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256", "ES256"],
            audience="authenticated",
            options={"require": ["exp", "sub"]},
        )
    # Supabase's key server is unreachable: ask the user to retry
    except PyJWKClientConnectionError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Sign-in service unavailable, try again",
        )
    # Any other failed check ends here
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return payload["sub"]


# Looks up the user's role in the profiles table
def get_current_role(
    user_id: Annotated[str, Depends(get_current_user_id)],
    db: Annotated[Session, Depends(get_db)],
) -> Role:
    # Reject a user ID that isn't a UUID instead of crashing
    try:
        profile_id = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    role = db.scalar(select(Profile.role).where(Profile.id == profile_id))
    # Signed in, but no profile row exists
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No profile found for this user",
        )
    return role


# Builds a dependency that only lets the listed roles through
def require_role(*allowed: Role) -> Callable[..., Role]:
    # The dependency FastAPI runs before the route
    def check_role(role: Annotated[Role, Depends(get_current_role)]) -> Role:
        # Signed in, but this role isn't on the list: 403
        if role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your role cannot do this",
            )
        return role

    return check_role
