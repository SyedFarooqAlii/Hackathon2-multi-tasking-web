# Todo AI Chatbot Quickstart Guide

## Overview
This guide will help you set up and run the Todo AI Chatbot with ChatKit frontend and FastAPI backend using OpenAI Agents SDK and MCP tools.

## Prerequisites
- Node.js 18+ installed
- Python 3.9+ installed
- OpenAI API key
- MCP server running locally or remotely
- Database (Neon PostgreSQL) connection

## Environment Setup

### Frontend Setup
1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file with the following content:
```env
NEXT_PUBLIC_OPENAI_API_KEY=your_openai_api_key_here
NEXT_PUBLIC_CHAT_ENDPOINT=http://localhost:8000/api
NEXT_PUBLIC_MCP_SERVER_URL=your_mcp_server_url
```

### Backend Setup
1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following content:
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://username:password@localhost/dbname
MCP_SERVER_URL=your_mcp_server_url
JWT_SECRET=your_jwt_secret
```

## Running the Applications

### Starting the MCP Server
Before starting the backend, ensure your MCP server is running:
```bash
# Run your MCP server implementation
```

### Starting the Backend
From the backend directory:
```bash
uvicorn src.main:app --reload
```
The backend will start on `http://localhost:8000`.

### Starting the Frontend
From the frontend directory:
```bash
npm run dev
```
The frontend will start on `http://localhost:3000`.

## Architecture Components

### Frontend (Next.js + ChatKit)
- Located in `/frontend` directory
- Uses ChatKit for the chat interface
- Communicates with backend via API calls
- Stores conversation ID in browser session/local storage

### Backend (FastAPI)
- Located in `/backend` directory
- Provides stateless chat endpoint
- Integrates with OpenAI Agents SDK
- Connects to MCP server for task operations
- Persists conversations and messages to database

### MCP Server
- Implements the required task management tools:
  - `add_task(user_id, title, description?)`
  - `list_tasks(user_id, status?)`
  - `update_task(user_id, task_id, title?, description?)`
  - `complete_task(user_id, task_id)`
  - `delete_task(user_id, task_id)`

## API Endpoints

### POST /api/{user_id}/chat
Processes user messages and returns AI responses.

Request:
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": 123
}
```

Response:
```json
{
  "conversation_id": 123,
  "response": "I've created a task 'buy groceries' for you.",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "parameters": {
        "user_id": "user123",
        "title": "buy groceries"
      }
    }
  ]
}
```

## Troubleshooting

### Common Issues
1. **OpenAI API errors**: Verify your API key is correct and has sufficient quota
2. **Database connection issues**: Check your DATABASE_URL configuration
3. **MCP server unreachable**: Ensure the MCP server is running and accessible
4. **Authentication errors**: Verify JWT token format and secret key

### Development Tips
- Use the backend's reload feature during development (`--reload` flag)
- Enable verbose logging in the backend for debugging
- Monitor the MCP server logs to verify tool calls are working correctly