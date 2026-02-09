from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID
import logging
from src.services.auth_service import auth_service
from src.models.user import UserCreate, UserRead
from src.core.database import get_session
from src.api.deps import get_current_user_from_token

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/users/register", response_model=UserRead)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_session)
):
    """
    Register a new user with the system.
    """
    try:
        logger.info(f"Processing registration request for email: {user.email}")

        # Validate input
        if not user.email or '@' not in user.email:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid email address"
            )

        if not user.password or len(user.password) < 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password is required"
            )

        # Create the user
        created_user = auth_service.register_user(db, user)
        logger.info(f"Successfully registered user {created_user.id} with email: {user.email}")

        return created_user
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        # Handle specific value errors like duplicate emails
        logger.warning(f"Registration failed for email {user.email}: {str(e)}")
        if "already registered" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e)
            )
    except Exception as e:
        logger.error(f"Error registering user with email {user.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while registering the user"
        )


@router.post("/users/login")
def login_user(
    user_credentials: UserCreate,
    db: Session = Depends(get_session)
):
    """
    Authenticate user and return JWT token.
    """
    try:
        logger.info(f"Processing login request for email: {user_credentials.email}")

        # Authenticate the user
        token_data = auth_service.authenticate_user(db, user_credentials.email, user_credentials.password)
        if not token_data:
            logger.warning(f"Failed login attempt for email: {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logger.info(f"Successful login for user with email: {user_credentials.email}")
        return token_data
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error during login for email {user_credentials.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during authentication"
        )


@router.get("/users/me", response_model=UserRead)
def get_current_user_info(
    current_user_id: UUID = Depends(get_current_user_from_token),
    db: Session = Depends(get_session)
):
    """
    Get information about the currently authenticated user.
    """
    try:
        logger.info(f"Retrieving information for user {current_user_id}")

        # Get user information
        user = auth_service.get_user_by_id(db, current_user_id)
        if not user:
            logger.error(f"User {current_user_id} not found in database")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        logger.info(f"Successfully retrieved information for user {current_user_id}")
        return user
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error retrieving user {current_user_id} information: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving user information"
        )