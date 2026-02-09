import logging
import sys
from datetime import datetime
from typing import Any, Dict


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the specified name and level
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding multiple handlers if logger already exists
    if logger.handlers:
        return logger

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    return logger


def log_api_call(endpoint: str, user_id: str, duration: float, status_code: int):
    """
    Log API call information
    """
    logger = setup_logger("api")
    logger.info(f"API Call: {endpoint} | User: {user_id} | Duration: {duration}s | Status: {status_code}")


def log_error(error: Exception, context: str = ""):
    """
    Log error with context
    """
    logger = setup_logger("error")
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)


def log_mcp_tool_call(tool_name: str, user_id: str, params: Dict[str, Any]):
    """
    Log MCP tool call
    """
    logger = setup_logger("mcp")
    logger.info(f"MCP Tool Call: {tool_name} | User: {user_id} | Params: {params}")


def log_chat_interaction(user_id: str, conversation_id: int, user_input: str, ai_response: str):
    """
    Log chat interaction
    """
    logger = setup_logger("chat")
    logger.info(f"Chat Interaction | User: {user_id} | Conv: {conversation_id} | "
                f"Input: {user_input[:50]}... | Response: {ai_response[:50]}...")