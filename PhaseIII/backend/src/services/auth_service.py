from sqlmodel import Session, select
from uuid import UUID
import logging
from datetime import timedelta
from ..models.user import User, UserCreate, UserRead
from ..core.security import verify_password, get_password_hash, create_access_token

# Set up logging
logger = logging.getLogger(__name__)


class AuthService:
    """
    Service class for handling authentication-related business logic and database operations.
    """

    def register_user(self, db: Session, user_create: UserCreate) -> UserRead:
        """
        Register a new user with the system.
        """
        logger.info(f"Registering new user with email: {user_create.email}")

        # Check if user already exists
        existing_user = self.get_user_by_email(db, user_create.email)
        if existing_user:
            logger.warning(f"Registration attempt for existing email: {user_create.email}")
            raise ValueError("Email already registered")

        try:
            # Hash the password
            hashed_password = get_password_hash(user_create.password)
        except Exception as e:
            logger.error(f"Error hashing password for user {user_create.email}: {str(e)}")
            # Re-raise as a more specific error that can be handled by the controller
            raise e

        # Create the user
        db_user = User(
            email=user_create.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.info(f"Successfully registered user {db_user.id} with email: {user_create.email}")
        return UserRead.from_orm(db_user) if hasattr(UserRead, 'from_orm') else UserRead(
            id=db_user.id,
            email=db_user.email,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )

    def get_user_by_email(self, db: Session, email: str) -> User:
        """
        Get a user by their email address.
        """
        statement = select(User).where(User.email == email)
        result = db.exec(statement)
        return result.first()

    def authenticate_user(self, db: Session, email: str, password: str) -> dict:
        """
        Authenticate user credentials and return JWT token data.
        """
        logger.info(f"Authenticating user with email: {email}")

        # Get user by email
        user = self.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            logger.warning(f"Authentication failed for email: {email}")
            return None

        # Create access token
        access_token_expires = timedelta(minutes=30)  # This should come from settings
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "type": "access"},
            expires_delta=access_token_expires
        )

        logger.info(f"Successfully authenticated user {user.id} with email: {email}")
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    def get_user_by_id(self, db: Session, user_id: UUID) -> UserRead:
        """
        Get a user by their ID.
        """
        logger.debug(f"Retrieving user by ID: {user_id}")

        statement = select(User).where(User.id == user_id)
        result = db.exec(statement)
        user = result.first()

        if user:
            logger.debug(f"Found user {user.id} by ID")
            return UserRead.from_orm(user) if hasattr(UserRead, 'from_orm') else UserRead(
                id=user.id,
                email=user.email,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        else:
            logger.debug(f"User with ID {user_id} not found")
            return None


# Create a singleton instance
auth_service = AuthService()