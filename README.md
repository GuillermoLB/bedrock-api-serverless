# AWS Bedrock Agent API

A FastAPI-based service that provides a secure API for interacting with AWS Bedrock Agents, enabling conversational AI capabilities without requiring a separate database for conversation history.

## Architecture

This project is structured as a modern Python web application using FastAPI with the following key components:

### Core Components

- **FastAPI Application**: The main entry point that registers all routes and middleware
- **AWS Bedrock Integration**: Services for interacting with AWS Bedrock API
- **Authentication**: JWT-based authentication system
- **PostgreSQL Database**: Database for user management only (not for conversation storage)

### Key Design Features

1. **Stateless Conversation Storage**: 
   - All conversation history and context are stored directly in AWS Bedrock sessions
   - No need for a separate database to manage conversation state
   - Leverages Bedrock's built-in session and memory management capabilities

2. **Clean Dependency Injection**:
   - Uses FastAPI's dependency injection system for services and configuration
   - Centralized dependency definitions
   - Type-annotated dependencies for better code clarity and IDE support

3. **Layered Architecture**:
   - **Routers**: API endpoints and request handling
   - **Services**: Business logic and external service integration
   - **Schemas**: Data validation and serialization with Pydantic
   - **Models**: Database models (for user management only)
   - **Repositories**: Database access layer

4. **API Structure**:
   - User management (`/users/`)
   - Authentication (`/tokens/`)
   - Copilot AI conversation (`/api/copilot/sessions/`)

## Data Flow

1. User authenticates with username/password to receive a JWT token
2. Using the token, the client can:
   - Create a new Bedrock session
   - Send messages to an existing session
   - Retrieve session history
   - Delete sessions

3. **Key Benefit**: Since conversation history is stored in AWS Bedrock, there's no need to:
   - Create database tables for messages
   - Implement pagination or querying for conversation history
   - Worry about database scaling for high-volume conversations

## Running the Project

### Local Development

1. Set up environment variables in `.env` file
2. Start the PostgreSQL database:
3. GitHub Copilot
Here's the content in proper Markdown format with all the necessary formatting annotations:

docker-compose up -d db

3. Run the application:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


### Docker Deployment

docker-compose up -d


## API Endpoints

### Authentication

- `POST /tokens/token` - Obtain a JWT token with username and password
- `GET /tokens` - Get current token details

### User Management

- `POST /users/` - Create a new user
- `GET /users/me` - Get current user details 

### Copilot AI

- `POST /api/copilot/sessions/` - Create a new conversation session
- `GET /api/copilot/sessions/` - List available sessions
- `POST /api/copilot/sessions/{session_id}/messages` - Send a message to a session and get AI response
- `GET /api/copilot/sessions/{session_id}/messages` - Get message history for a session
- `DELETE /api/copilot/sessions/{session_id}` - Delete a session

## Notes on AWS Bedrock Integration

This API leverages AWS Bedrock's features:
- Session creation and management
- Invocation tracking for messages
- Memory capabilities for maintaining history and context
- Knowledge base integration for retrieving information

By storing conversations directly in AWS Bedrock sessions, this architecture:
- Simplifies the backend design
- Reduces database costs and complexity
- Takes advantage of AWS's infrastructure for storing and processing conversation data