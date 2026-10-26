import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient
from sqlalchemy import text

from app.config import settings
from app.database import engine
from app.enums import Role

# Reads the Authorization header
bearer_scheme = HTTPBearer()

# Fetches Supabase's public keys
jwks_client = PyJWKClient(f"{settings.supabase_url}/auth/v1/.well-known/jwks.json")


# Checks the token and returns the user ID
def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    token = credentials.credentials
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256", "ES256"],
            audience="authenticated",
        )
    # Any failed check ends here
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return payload["sub"]


# Looks up the user's role in the profiles table
def get_current_role(user_id: str = Depends(get_current_user_id)) -> Role:
    with engine.connect() as conn:
        row = conn.execute(
            text("select role::text from profiles where id = :id"),
            {"id": user_id},
        ).first()
    # Signed in, but no profile row exists
    if row is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No profile found for this user",
        )
    return Role(row[0])


# Builds a dependency that only lets the listed roles through
def require_role(*allowed: Role):
    # The dependency FastAPI runs before the route
    def check_role(role: Role = Depends(get_current_role)) -> Role:
        # Signed in, but this role isn't on the list: 403
        if role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your role cannot do this",
            )
        return role

    return check_role
