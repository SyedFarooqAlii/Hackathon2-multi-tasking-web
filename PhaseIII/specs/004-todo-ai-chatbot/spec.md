# Spec-004: Todo AI Chatbot

## Feature Overview
Enable users to manage todos via a conversational UI by integrating a ChatKit frontend with an AI agent backend using OpenAI Agents SDK and MCP tools.

## Goal
Enable users to manage todos via a conversational UI by integrating a ChatKit frontend with an AI agent backend using OpenAI Agents SDK and MCP tools.

## Scope
- ChatKit-based frontend UI
- FastAPI stateless chat backend
- OpenAI Agents SDK for AI logic
- MCP server exposing task tools
- Persistent conversations in database
- Secure user context via Better Auth

## Out of Scope
- UI theming beyond ChatKit defaults
- Voice, multi-language, reminders
- Advanced task features

## User Scenarios & Testing

### Primary User Scenario
As an authenticated user, I want to interact with a chat interface to manage my tasks using natural language commands, so that I can create, view, update, and delete my tasks without navigating through traditional UI forms.

### User Flows
1. User accesses the chat interface and authenticates via Better Auth
2. User sends a natural language message to add/list/update/complete/delete tasks
3. AI agent interprets the intent and calls appropriate MCP tools
4. MCP tools perform the requested task operations
5. AI agent responds to the user with confirmation and relevant information
6. Conversation is persisted to the database for continuity

### Acceptance Scenarios
- Given an authenticated user, when they send "Add a task to buy groceries", then the AI should create a task titled "buy groceries" and confirm creation
- Given an authenticated user, when they send "Show my tasks", then the AI should list all incomplete tasks
- Given an authenticated user, when they send "Complete task #1", then the AI should mark task #1 as complete and confirm
- Given an authenticated user, when they refresh the page, then their ongoing conversation history should be preserved

## Functional Requirements

### FR-1: Chat Interface Integration
The system shall provide a ChatKit-based frontend UI that allows users to send and receive messages with the AI agent.

**Acceptance Criteria:**
- Users can send text messages to the AI agent
- Users can receive formatted responses from the AI agent
- The chat interface maintains conversation history during the session

### FR-2: Stateless Chat Backend
The system shall provide a FastAPI stateless chat backend that processes user messages and returns AI-generated responses.

**Acceptance Criteria:**
- Each API call contains the conversation context needed to process the request
- The server does not maintain in-memory state between requests
- Requests include user authentication and optional conversation ID

### FR-3: AI Intent Interpretation
The system shall use OpenAI Agents SDK to interpret natural language commands and determine the appropriate action.

**Acceptance Criteria:**
- The AI correctly identifies intent from natural language (add, list, update, complete, delete)
- The AI can extract relevant parameters from user commands
- The AI handles ambiguous or unclear requests gracefully

### FR-4: MCP Tool Integration
The system shall use MCP tools for all task operations, never accessing the database directly.

**Acceptance Criteria:**
- All task creation goes through add_task MCP tool
- All task retrieval goes through list_tasks MCP tool
- All task updates go through update_task MCP tool
- All task completions go through complete_task MCP tool
- All task deletions go through delete_task MCP tool

### FR-5: Conversation Persistence
The system shall persist conversations and messages in the database for continuity.

**Acceptance Criteria:**
- Each conversation has a unique ID
- All messages in a conversation are stored with timestamps
- Conversation history can be retrieved for resumption
- Messages are associated with the correct user

### FR-6: User Authentication & Context
The system shall maintain secure user context via Better Auth throughout the conversation.

**Acceptance Criteria:**
- User authentication is validated on each API call
- Tasks are associated with the correct user ID
- Users can only access their own tasks
- User context is maintained across conversation sessions

## Success Criteria
- 95% of natural language commands are correctly interpreted and result in appropriate tool calls
- Chat responses are delivered within 3 seconds for 90% of requests
- 100% of task operations go through MCP tools rather than direct database access
- Conversations successfully resume after browser refresh
- Users report high satisfaction with natural language task management

## Key Entities
- **User**: An authenticated person using the system
- **Conversation**: A collection of messages between a user and the AI agent
- **Message**: An individual communication from user to AI or AI to user
- **Task**: A user's to-do item with title, description, and completion status
- **AI Agent**: The OpenAI-powered entity that processes natural language and invokes MCP tools

## Assumptions
- MCP tools are properly configured and accessible to the backend
- ChatKit UI provides necessary customization options for the required functionality
- Better Auth provides reliable JWT-based authentication for API endpoints
- The system operates with standard internet connection speeds for AI processing

## Dependencies
- OpenAI Agents SDK availability and reliability
- MCP server with exposed task management tools
- Better Auth integration for user authentication
- Neon PostgreSQL database for conversation persistence