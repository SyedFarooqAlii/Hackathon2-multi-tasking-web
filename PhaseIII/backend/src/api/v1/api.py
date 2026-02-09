from fastapi import APIRouter
from . import auth, todos
from .chat_endpoints import router as chat_router

# Main API router that includes all version 1 endpoints
router = APIRouter()

# Include the auth, todos, and chat routers
router.include_router(auth.router, prefix="", tags=["auth"])
router.include_router(todos.router, prefix="", tags=["todos"])
router.include_router(chat_router, prefix="/chat", tags=["chat"])