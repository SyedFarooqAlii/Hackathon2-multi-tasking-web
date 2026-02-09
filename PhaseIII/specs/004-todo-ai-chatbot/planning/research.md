# Implementation Plan: Todo AI Chatbot (Spec-001)

## Technical Context

### Known Elements
- **Frontend**: Existing Next.js application in `/frontend` directory
- **Backend**: Existing FastAPI application in `/backend` directory
- **Database**: SQLModel with Neon PostgreSQL (existing schema includes User, Task models)
- **Authentication**: Better Auth integration
- **Target Architecture**: ChatKit frontend + FastAPI stateless backend + OpenAI Agents SDK + MCP tools

### Unknown Elements
- Specific ChatKit integration approach and configuration
- OpenAI Agents SDK setup and configuration
- MCP server implementation details
- Conversation and Message model definitions
- Exact API contract for chat endpoint

### Dependencies
- OpenAI API access and credentials
- OpenAI Agents SDK library
- MCP SDK/library for tool integration
- ChatKit React component library
- Neon PostgreSQL connection details

## Constitution Check

### Compliance Assessment
- ✅ **Agentic Dev Stack**: Following Spec → Plan → Tasks → Claude Code workflow
- ✅ **MCP Tool Enforcement**: AI agent will use MCP tools for all task operations (not direct DB access)
- ✅ **Stateless Architecture**: FastAPI backend will fetch conversation history per request, not maintain in-memory state
- ✅ **DB-Persisted Conversation State**: Conversations and messages stored in database for continuity
- ✅ **No Business Logic in Frontend**: Frontend will be UI-only with ChatKit integration
- ✅ **Spec-Driven Development**: Building according to established spec requirements

### Potential Violations
None identified - all requirements align with constitutional principles.

### Gate Evaluations
- ✅ **GATE-1 (Architecture)**: Planned architecture supports constitutional requirements
- ✅ **GATE-2 (MCP Enforcement)**: Agent will exclusively use MCP tools for task operations
- ✅ **GATE-3 (Statelessness)**: Backend designed to be stateless per constitutional mandate

## Phase 0: Research & Clarification

### Research Objectives

#### R1: ChatKit Integration Research
**Decision**: Determine optimal approach for integrating ChatKit with Next.js frontend
**Rationale**: Need to understand ChatKit installation, configuration, and integration patterns
**Alternatives considered**:
- Direct ChatKit component integration
- Custom wrapper around ChatKit
- Alternative chat UI libraries

#### R2: OpenAI Agents SDK Setup Research
**Decision**: Determine how to configure OpenAI Agents with custom MCP tools
**Rationale**: Need to understand Agent creation, tool definition, and execution patterns
**Alternatives considered**:
- OpenAI Assistant API vs. Agents SDK
- Different tool definition approaches
- Various integration patterns

#### R3: MCP Server Implementation Research
**Decision**: Determine MCP server architecture and tool implementation patterns
**Rationale**: Need to understand MCP protocol and how to expose task operations
**Alternatives considered**:
- Standalone MCP server vs. integrated in FastAPI
- Different MCP SDK/library options
- Tool registration patterns

#### R4: Conversation Data Model Research
**Decision**: Determine optimal database schema for conversation and message storage
**Rationale**: Need to align with constitutional data model requirements
**Alternatives considered**:
- Different relationship patterns between Conversation, Message, and Task
- Various indexing strategies
- Different timestamp approaches

## Phase 1: Design & Contracts

### Data Model Design

#### Conversation Entity
- `id`: Integer, primary key, auto-generated
- `user_id`: String, foreign key to User, required
- `created_at`: DateTime, timestamp when conversation started
- `updated_at`: DateTime, timestamp of last activity

#### Message Entity
- `id`: Integer, primary key, auto-generated
- `conversation_id`: Integer, foreign key to Conversation, required
- `role`: String, enum ('user'|'assistant'), required
- `content`: String, message content, required
- `created_at`: DateTime, timestamp when message was created

#### Task Entity (Existing)
- `id`: Integer, primary key, auto-generated
- `user_id`: String, foreign key to User, required
- `title`: String, task title, required
- `description`: String, task description, optional
- `completed`: Boolean, completion status, default false
- `created_at`: DateTime, timestamp when task was created
- `updated_at`: DateTime, timestamp of last update

### API Contracts

#### POST /api/{user_id}/chat
**Description**: Process user message and return AI response with conversation context

**Request Parameters**:
- `user_id`: String, authenticated user ID from JWT (required)

**Request Body**:
- `message`: String, user's natural language message (required)
- `conversation_id`: Integer, optional conversation identifier for continuation

**Response Body**:
- `conversation_id`: Integer, identifier for the conversation
- `response`: String, AI-generated response
- `tool_calls`: Array, list of tools called during processing

**Authentication**: JWT token required, user_id extracted from token and validated

**Success Codes**: 200 OK
**Error Codes**: 401 Unauthorized, 400 Bad Request, 500 Internal Server Error

#### Error Response Format:
```json
{
  "error": "error_message",
  "details": "detailed_error_info"
}
```

### Quickstart Guide

#### Prerequisites
- Node.js 18+ for frontend
- Python 3.9+ for backend
- OpenAI API key
- MCP server running
- Neon PostgreSQL database access

#### Setup Instructions
1. **Frontend Setup**:
   ```bash
   cd frontend
   npm install @openai/chatkit # Install ChatKit
   npm install # Install other dependencies
   npm run dev # Start development server
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   pip install openai openai-agents # Install OpenAI libraries
   pip install # Install other dependencies
   uvicorn src.main:app --reload # Start server
   ```

3. **Environment Configuration**:
   - Set OPENAI_API_KEY in both frontend and backend
   - Configure database connection strings
   - Set MCP server endpoint

## Phase 2: Implementation Architecture

### Frontend Architecture
- **Components**: ChatKit integration components
- **Pages**: Chat interface page
- **Services**: API client for chat endpoint communication
- **State Management**: Conversation context and ID management

### Backend Architecture
- **Routes**: Chat endpoint at `/api/{user_id}/chat`
- **Services**: Conversation history management, agent orchestration
- **Models**: Conversation and Message SQLAlchemy models
- **Integration**: OpenAI Agents SDK with MCP tools

### Agent Architecture
- **Intent Recognition**: Natural language processing for task operations
- **Tool Selection**: Dynamic selection of appropriate MCP tools
- **Response Generation**: Natural language responses with confirmation

## Validation Criteria

### Primary Validation Points
- [ ] Chat session survives server restart (statelessness confirmed)
- [ ] Tasks created exclusively via chat and MCP tools (no direct DB access)
- [ ] Proper tool selection based on user intent
- [ ] Frontend-backend integration works end-to-end
- [ ] Authentication and user isolation maintained

### Secondary Validation Points
- [ ] Error handling for invalid requests
- [ ] Proper error responses returned to frontend
- [ ] Conversation history correctly persisted and retrieved
- [ ] AI responses are natural and informative