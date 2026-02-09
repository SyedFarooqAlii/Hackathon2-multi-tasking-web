"""
MCP Server Implementation for Todo AI Chatbot

This module implements the MCP (Model Context Protocol) server that exposes
task management tools for the AI agent to use.
"""

from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
import os
from contextlib import asynccontextmanager
from .core.database import create_db_and_tables
from .core.mcp_client import mcp_client
from .services.mcp_services import mcp_task_service


class MCPTaskRequest(BaseModel):
    """
    Request model for MCP task operations
    """
    user_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    task_id: Optional[str] = None
    status: Optional[str] = "all"


class MCPTaskResponse(BaseModel):
    """
    Response model for MCP task operations
    """
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None
    task: Optional[Dict[str, Any]] = None
    tasks: Optional[list] = None


# Create the MCP server application
mcp_app = FastAPI(
    title="Todo AI Chatbot MCP Server",
    description="Model Context Protocol server for todo management tools",
    version="1.0.0"
)


@asynccontextmanager
async def mcp_lifespan(app: FastAPI):
    """
    Lifespan event handler for MCP server
    """
    # Startup: Initialize any required resources
    print("MCP Server starting up...")
    yield
    # Shutdown: Cleanup operations
    print("MCP Server shutting down...")


mcp_app = FastAPI(
    title="Todo AI Chatbot MCP Server",
    description="Model Context Protocol server for todo management tools",
    version="1.0.0",
    lifespan=mcp_lifespan
)


@mcp_app.post("/tools/add_task")
async def mcp_add_task(request: MCPTaskRequest) -> MCPTaskResponse:
    """
    MCP tool: Add a new task for a user
    """
    try:
        # Get database session
        from .core.database import engine
        from sqlmodel import Session

        with Session(engine) as db_session:
            result = mcp_task_service.add_task(
                db_session=db_session,
                user_id=request.user_id,
                title=request.title or "",
                description=request.description
            )

            return MCPTaskResponse(**result)

    except Exception as e:
        return MCPTaskResponse(
            success=False,
            error=str(e)
        )


@mcp_app.post("/tools/list_tasks")
async def mcp_list_tasks(request: MCPTaskRequest) -> MCPTaskResponse:
    """
    MCP tool: List tasks for a user
    """
    try:
        # Get database session
        from .core.database import engine
        from sqlmodel import Session

        with Session(engine) as db_session:
            result = mcp_task_service.list_tasks(
                db_session=db_session,
                user_id=request.user_id,
                status=request.status
            )

            return MCPTaskResponse(**result)

    except Exception as e:
        return MCPTaskResponse(
            success=False,
            error=str(e)
        )


@mcp_app.post("/tools/update_task")
async def mcp_update_task(request: MCPTaskRequest) -> MCPTaskResponse:
    """
    MCP tool: Update an existing task for a user
    """
    try:
        # Get database session
        from .core.database import engine
        from sqlmodel import Session

        with Session(engine) as db_session:
            result = mcp_task_service.update_task(
                db_session=db_session,
                user_id=request.user_id,
                task_id=request.task_id or "",
                title=request.title,
                description=request.description
            )

            return MCPTaskResponse(**result)

    except Exception as e:
        return MCPTaskResponse(
            success=False,
            error=str(e)
        )


@mcp_app.post("/tools/complete_task")
async def mcp_complete_task(request: MCPTaskRequest) -> MCPTaskResponse:
    """
    MCP tool: Mark a task as completed for a user
    """
    try:
        # Get database session
        from .core.database import engine
        from sqlmodel import Session

        with Session(engine) as db_session:
            result = mcp_task_service.complete_task(
                db_session=db_session,
                user_id=request.user_id,
                task_id=request.task_id or ""
            )

            return MCPTaskResponse(**result)

    except Exception as e:
        return MCPTaskResponse(
            success=False,
            error=str(e)
        )


@mcp_app.post("/tools/delete_task")
async def mcp_delete_task(request: MCPTaskRequest) -> MCPTaskResponse:
    """
    MCP tool: Delete a task for a user
    """
    try:
        # Get database session
        from .core.database import engine
        from sqlmodel import Session

        with Session(engine) as db_session:
            result = mcp_task_service.delete_task(
                db_session=db_session,
                user_id=request.user_id,
                task_id=request.task_id or ""
            )

            return MCPTaskResponse(**result)

    except Exception as e:
        return MCPTaskResponse(
            success=False,
            error=str(e)
        )


@mcp_app.get("/health")
async def mcp_health_check():
    """
    Health check endpoint for the MCP server
    """
    return {"status": "healthy", "service": "MCP Server"}


# For backward compatibility, also expose the functions directly
__all__ = [
    "mcp_app",
    "MCPTaskRequest",
    "MCPTaskResponse",
    "mcp_add_task",
    "mcp_list_tasks",
    "mcp_update_task",
    "mcp_complete_task",
    "mcp_delete_task"
]