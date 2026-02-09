import httpx
import os
from typing import Dict, Any, Optional
from ..core.errors import MCPToolError
from ..core.logging import log_mcp_tool_call


class MCPClient:
    """
    Client for communicating with the MCP server
    """

    def __init__(self):
        self.base_url = os.getenv("MCP_SERVER_URL", "http://localhost:8080")

    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call an MCP tool with the provided parameters
        """
        try:
            # Log the tool call
            user_id = params.get("user_id", "unknown")
            log_mcp_tool_call(tool_name, user_id, params)

            # Construct the URL for the tool
            url = f"{self.base_url}/tools/{tool_name}"

            # Make the async HTTP request
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=params,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {os.getenv('MCP_API_TOKEN', '')}"  # If needed
                    },
                    timeout=30.0  # 30 second timeout
                )

                # Check if the request was successful
                if response.status_code != 200:
                    raise MCPToolError(f"MCP tool call failed with status {response.status_code}: {response.text}")

                # Return the response
                return response.json()

        except httpx.RequestError as e:
            raise MCPToolError(f"Request error during MCP tool call: {str(e)}")
        except Exception as e:
            raise MCPToolError(f"Error calling MCP tool {tool_name}: {str(e)}")

    async def add_task(self, user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Call the add_task MCP tool
        """
        params = {
            "user_id": user_id,
            "title": title
        }
        if description:
            params["description"] = description

        return await self.call_tool("add_task", params)

    async def list_tasks(self, user_id: str, status: Optional[str] = "all") -> Dict[str, Any]:
        """
        Call the list_tasks MCP tool
        """
        params = {
            "user_id": user_id,
            "status": status
        }

        return await self.call_tool("list_tasks", params)

    async def update_task(self, user_id: str, task_id: str, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Call the update_task MCP tool
        """
        params = {
            "user_id": user_id,
            "task_id": task_id
        }

        if title is not None:
            params["title"] = title
        if description is not None:
            params["description"] = description

        return await self.call_tool("update_task", params)

    async def complete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """
        Call the complete_task MCP tool
        """
        params = {
            "user_id": user_id,
            "task_id": task_id
        }

        return await self.call_tool("complete_task", params)

    async def delete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """
        Call the delete_task MCP tool
        """
        params = {
            "user_id": user_id,
            "task_id": task_id
        }

        return await self.call_tool("delete_task", params)


# Global instance of the MCP client
mcp_client = MCPClient()