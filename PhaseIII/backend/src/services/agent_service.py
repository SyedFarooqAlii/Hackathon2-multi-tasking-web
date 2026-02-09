import openai
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import json
import os
from ..core.errors import MCPToolError
import uuid


class MCPToolDefinition(BaseModel):
    """
    Definition of an MCP tool that can be called by the agent
    """
    name: str
    description: str
    parameters: Dict[str, Any]


class AgentService:
    """
    Service class for interacting with LLM agents and MCP tools
    """

    def __init__(self):
        # Store the API key but don't initialize the client yet (lazy initialization)
        self._api_key = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not self._api_key:
            raise ValueError("GROQ_API_KEY or OPENAI_API_KEY environment variable not set")
        self._client = None

    @property
    def client(self):
        # Initialize the client only when first accessed
        if self._client is None:
            self._client = openai.OpenAI(
                api_key=self._api_key,
                base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")  # Groq-compatible endpoint
            )
        return self._client

    mcp_tools = [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Add a new task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "title": {"type": "string", "description": "The task title"},
                        "description": {"type": "string", "description": "Optional task description"}
                    },
                    "required": ["user_id", "title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List tasks for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "status": {"type": "string", "enum": ["all", "active", "completed"], "description": "Filter tasks by status"}
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update an existing task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "task_id": {"type": "string", "description": "The task ID"},
                        "title": {"type": "string", "description": "New task title (optional)"},
                        "description": {"type": "string", "description": "New task description (optional)"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as completed for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "task_id": {"type": "string", "description": "The task ID"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user ID"},
                        "task_id": {"type": "string", "description": "The task ID"}
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        }
    ]

    def process_conversation(self,
                           user_id: str,
                           user_message: str,
                           conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Process a user message in the context of a conversation and return AI response
        """
        try:
            # Prepare the messages for the API
            messages = []

            # Add system message to guide the agent's behavior
            messages.append({
                "role": "system",
                "content": "You are a helpful AI assistant that helps users manage their tasks. "
                          "Use the available tools to add, list, update, complete, or delete tasks. "
                          "Always confirm important actions before executing them. "
                          "Be friendly and helpful in your responses."
            })

            # Add conversation history
            for msg in conversation_history:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

            # Add the current user message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Call the API with the tools
            response = self.client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", "llama3-8b-8192"),  # Use Groq model
                messages=messages,
                tools=self.mcp_tools,
                tool_choice="auto"
            )

            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # If the agent wants to call tools
            if tool_calls:
                # Execute the tool calls
                tool_results = []
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Add user_id to function arguments if not present
                    if "user_id" not in function_args:
                        function_args["user_id"] = user_id

                    # Execute the tool and get result
                    result = self._execute_tool(function_name, function_args)

                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "content": json.dumps(result)
                    })

                # Get final response after tool execution
                second_response = self.client.chat.completions.create(
                    model=os.getenv("GROQ_MODEL", "llama3-8b-8192"),
                    messages=messages + [response_message] + tool_results,
                )

                final_content = second_response.choices[0].message.content
                return {
                    "response": final_content,
                    "tool_calls": [{"name": tc.function.name, "arguments": json.loads(tc.function.arguments)} for tc in tool_calls if tc.function.name and tc.function.arguments],
                    "tool_results": tool_results
                }
            else:
                # No tools needed, just return the content
                response_message = response.choices[0].message
                return {
                    "response": response_message.content,
                    "tool_calls": [],
                    "tool_results": []
                }

        except Exception as e:
            raise MCPToolError(f"Error processing conversation: {str(e)}")

    def _execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an MCP tool call (this is a simulation - in a real implementation,
        this would call the actual MCP server)
        """
        try:
            # In a real implementation, this would make an HTTP call to the MCP server
            # For now, we'll simulate the response

            # Log the tool call
            from ..core.logging import log_mcp_tool_call
            log_mcp_tool_call(tool_name, args.get("user_id", "unknown"), args)

            # Simulate the tool call
            if tool_name == "add_task":
                # Simulate adding a task
                return {
                    "success": True,
                    "message": f"Task '{args.get('title')}' added successfully",
                    "task_id": str(uuid.uuid4())  # Simulated task ID
                }
            elif tool_name == "list_tasks":
                # Simulate listing tasks
                return {
                    "success": True,
                    "tasks": [
                        {"id": str(uuid.uuid4()), "title": "Sample task", "completed": False},
                        {"id": str(uuid.uuid4()), "title": "Another task", "completed": True}
                    ]
                }
            elif tool_name == "update_task":
                # Simulate updating a task
                return {
                    "success": True,
                    "message": f"Task '{args.get('task_id')}' updated successfully"
                }
            elif tool_name == "complete_task":
                # Simulate completing a task
                return {
                    "success": True,
                    "message": f"Task '{args.get('task_id')}' marked as completed"
                }
            elif tool_name == "delete_task":
                # Simulate deleting a task
                return {
                    "success": True,
                    "message": f"Task '{args.get('task_id')}' deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}"
                }

        except Exception as e:
            raise MCPToolError(f"Error executing tool {tool_name}: {str(e)}")


# Global instance of the agent service (moved to be initialized inside functions to avoid module-level execution)
# agent_service is created inside the endpoint function