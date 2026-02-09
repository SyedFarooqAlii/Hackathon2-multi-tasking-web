# Todo AI Chatbot Technology Context

## Frontend Technologies
- Next.js 16+ (App Router)
- OpenAI ChatKit (chat interface component)
- React for UI components
- TypeScript for type safety

## Backend Technologies
- Python 3.9+
- FastAPI for web framework
- OpenAI Agents SDK for AI functionality
- SQLModel for ORM
- Neon PostgreSQL for database

## MCP Technologies
- MCP Server protocol/SDK for tool integration
- Tool definitions for task operations
- State management via database persistence

## Architecture Patterns
- Stateless backend design (no in-memory persistence)
- Database-persisted conversation history
- Authentication via Better Auth and JWT tokens
- Separation of concerns between UI, AI logic, and data operations

## Key Entities
- Conversation: Contains a series of messages between user and AI
- Message: Individual communication (user or assistant role)
- Task: User's todo item managed through MCP tools
- User: Authenticated user with associated tasks and conversations

## API Patterns
- POST /api/{user_id}/chat for chat interactions
- JWT token authentication for all endpoints
- MCP tools for all task operations (add, list, update, complete, delete)
- Response includes conversation context and tool call information