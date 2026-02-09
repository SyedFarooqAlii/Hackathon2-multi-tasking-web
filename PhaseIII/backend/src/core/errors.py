from fastapi import HTTPException, status


class ChatBotError(Exception):
    """Base exception class for chatbot-related errors"""
    pass


class TaskNotFoundError(ChatBotError):
    """Raised when a task is not found"""
    pass


class ConversationNotFoundError(ChatBotError):
    """Raised when a conversation is not found"""
    pass


class AuthenticationError(ChatBotError):
    """Raised when authentication fails"""
    pass


class AuthorizationError(ChatBotError):
    """Raised when user is not authorized to access a resource"""
    pass


class MCPToolError(ChatBotError):
    """Raised when an MCP tool operation fails"""
    pass


def raise_http_exception(status_code: int, detail: str):
    """Utility function to raise HTTP exceptions"""
    raise HTTPException(status_code=status_code, detail=detail)


def raise_not_found(detail: str = "Resource not found"):
    """Utility function to raise a 404 error"""
    raise_http_exception(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def raise_unauthorized(detail: str = "Not authenticated"):
    """Utility function to raise a 401 error"""
    raise_http_exception(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


def raise_forbidden(detail: str = "Access denied"):
    """Utility function to raise a 403 error"""
    raise_http_exception(status_code=status.HTTP_403_FORBIDDEN, detail=detail)