from fastapi import HTTPException, status, Request
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Optional
import os
from ..core.errors import AuthenticationError


class JWTBearer(HTTPBearer):
    """
    JWT Bearer token authentication middleware
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        # Get the authorization header
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme."
                )

            token = credentials.credentials

            # Verify the token
            user_id = self.verify_jwt(token)

            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token."
                )

            # Add user_id to request state for use in endpoints
            request.state.user_id = user_id
            return token
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authentication credentials were not provided."
            )

    def verify_jwt(self, token: str) -> Optional[str]:
        """
        Verify the JWT token and return the user_id if valid
        """
        try:
            # Get the JWT secret from environment
            jwt_secret = os.getenv("SECRET_KEY")
            if not jwt_secret:
                raise ValueError("SECRET_KEY environment variable not set")

            # Decode the token
            payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])

            # Extract user_id from the payload (stored in 'sub' field)
            user_id = payload.get("sub")

            if user_id:
                return str(user_id)
            else:
                return None

        except InvalidTokenError:
            return None
        except Exception as e:
            return None


def get_current_user_id(request: Request) -> str:
    """
    Helper function to get the current user ID from the request
    """
    if hasattr(request.state, 'user_id'):
        return request.state.user_id
    else:
        raise AuthenticationError("User ID not found in request state")


# Initialize the JWT Bearer scheme
jwt_scheme = JWTBearer()