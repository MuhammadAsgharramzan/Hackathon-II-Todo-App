# Todo App Hackathon - Phase II (Multi-Phase Todo Application)

This is the Todo App Hackathon project, a multi-phase development initiative to build a comprehensive todo application with progressive enhancements. The project consists of four distinct phases, each building upon the previous one to create a sophisticated, AI-integrated todo application deployed on Kubernetes.

## Vision
The Todo App Hackathon is a multi-phase development initiative that transforms a simple CLI todo application into a sophisticated, AI-integrated, cloud-native application deployed on Kubernetes. Each phase builds upon the previous one with progressive enhancements:

- **Phase I**: CLI-based todo application with specification-driven foundation
- **Phase II**: Full-stack web application with authentication and database integration
- **Phase III**: AI agent integration with LangGraph for intelligent task processing
- **Phase IV**: Containerization and Kubernetes deployment with AI-assisted DevOps

## Technology Stack

### Phase I: CLI Foundation
- Python 3.8+
- Specification-driven development tools

### Phase II: Full-Stack Web Application
- **Frontend**: Next.js 14+ (App Router), TypeScript, Tailwind CSS, Better Auth
- **Backend**: FastAPI (Python), SQLModel (ORM), JWT Authentication
- **Database**: PostgreSQL (Neon)

### Phase III: AI Integration
- **AI Orchestration**: LangGraph
- **AI Models**: Various LLMs for task processing
- **Integration**: AI agent workflows

### Phase IV: Containerization and Deployment
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Deployment**: AI-assisted DevOps tools

## Features

### Phase I: CLI Foundation
- Core todo functionality
- Command-line interface
- Specification-driven development

### Phase II: Full-Stack Web Application
- **User Management**: User registration and login, JWT-based authentication, secure token management
- **Task Management**: Create, Read, Update, Delete (CRUD) operations for tasks, mark tasks as complete/incomplete, user-specific task isolation, data validation and error handling
- **Security**: JWT token verification on every request, user data isolation (users can only access their own tasks), secure API endpoints

### Phase III: AI Integration
- **AI Agents**: Intelligent task processing and automation
- **Workflow Orchestration**: LangGraph for managing AI agent workflows
- **Enhanced Capabilities**: Natural language task creation and management

### Phase IV: Containerization and Deployment
- **Containerization**: Docker containers for all services
- **Orchestration**: Kubernetes deployment and management
- **DevOps**: AI-assisted operations and maintenance

## Architecture

### Phase I: CLI Foundation
```
Phase-I/
├── specs/               # Specification files
├── src/                 # CLI application source code
└── tests/               # Unit tests
```

### Phase II: Full-Stack Web Application

#### Frontend Structure
```
frontend/
├── app/                 # Next.js app router pages
│   ├── login/           # Login page
│   ├── register/        # Registration page
│   ├── tasks/           # Main tasks dashboard
│   └── page.tsx         # Home page (redirects based on auth status)
├── components/          # Reusable React components
├── lib/                 # Utility functions (API client)
└── public/              # Static assets
```

#### Backend Structure
```
backend/
├── main.py              # Main FastAPI application
├── models/              # Database models (SQLModel)
├── api/                 # API routes
├── auth/                # Authentication utilities
└── db/                  # Database configuration
```

### Phase III: AI Integration
```
Phase-III/
├── agents/              # AI agent implementations
├── workflows/           # LangGraph workflow definitions
├── integrations/        # AI service integrations
└── specs/               # AI integration specifications
```

### Phase IV: Containerization and Deployment
```
Phase-IV/
├── docker/              # Docker configurations
├── k8s/                 # Kubernetes manifests
├── infrastructure/      # Infrastructure as code
└── deployment/          # Deployment configurations
```

## Phase-Specific Components

### Phase I: CLI Foundation
- Command-line interface for todo management
- Specification-driven development workflow

### Phase II: Full-Stack Web Application

#### API Endpoints
##### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

##### Tasks
- `GET /tasks` - Get all tasks for authenticated user
- `POST /tasks` - Create a new task
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task
- `PATCH /tasks/{id}/toggle-complete` - Toggle task completion status

### Phase III: AI Integration
- AI agent endpoints for intelligent task processing
- Natural language task creation and management
- Workflow orchestration APIs

### Phase IV: Containerization and Deployment
- Containerized services for all components
- Kubernetes-native deployment configurations
- AI-assisted DevOps operations

## Security Rules

### Phase II Security
- Every API request requires a valid JWT token
- Users can only access their own tasks
- Backend verifies token on every request
- Invalid or missing tokens return 401 Unauthorized

### Phase III Security
- AI agent authentication and authorization
- Secure API communication between components
- Protected AI model endpoints

### Phase IV Security
- Kubernetes security best practices
- Network policies and service mesh security
- Container runtime security

## Setup Instructions

### Prerequisites
- Python 3.8+ (for all phases)
- Node.js 16+ (for Phase II frontend)
- Docker (for Phase IV)
- Kubernetes tools (for Phase IV)
- PostgreSQL (or Neon database)
- SpecifyPlus framework: `pip install specifyplus`

### Phase I Setup
1. Navigate to Phase I directory: `cd Phase-I`
2. Follow CLI application setup instructions in Phase-I/README.md

### Phase II Setup
1. Navigate to the backend directory: `cd Phase-II/backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables:
   ```bash
   export DATABASE_URL="postgresql://username:password@localhost/todo_db"
   export JWT_SECRET_KEY="your-secret-key-change-in-production"
   ```
4. Run the server: `python main.py`
5. Navigate to the frontend directory: `cd ../frontend`
6. Install dependencies: `npm install`
7. Set environment variables in `.env.local`:
   ```bash
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```
8. Run the development server: `npm run dev`

### Phase III Setup
1. Navigate to Phase III directory: `cd Phase-III`
2. Install AI dependencies: `pip install -r requirements.txt`
3. Configure AI model access
4. Run AI agent services

### Phase IV Setup
1. Navigate to Phase IV directory: `cd Phase-IV`
2. Build Docker images: `docker build -t todo-app .`
3. Deploy to Kubernetes cluster using provided manifests

## Environment Variables

### Phase II
#### Backend
- `DATABASE_URL`: PostgreSQL database connection string
- `JWT_SECRET_KEY`: Secret key for JWT signing
- `PORT`: Port for the FastAPI server (default: 8000)

#### Frontend
- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API

### Phase III
- `AI_MODEL_PROVIDER`: AI model provider (e.g., OpenAI, Anthropic)
- `AI_API_KEY`: API key for AI service
- `LANGGRAPH_API_KEY`: API key for LangGraph (if using hosted service)

### Phase IV
- `DOCKER_REGISTRY`: Container registry for image storage
- `KUBECONFIG`: Path to Kubernetes configuration file
- `CLUSTER_NAME`: Name of the Kubernetes cluster

## Running the Application

### Phase I
1. Navigate to Phase I directory: `cd Phase-I`
2. Run the CLI application: `python main.py`

### Phase II
1. Start the Phase II backend server: `cd Phase-II/backend && python main.py`
2. Start the Phase II frontend development server: `cd Phase-II/frontend && npm run dev`
3. Access the application at `http://localhost:3000`

### Phase III
1. Start the AI agents: `cd Phase-III && python -m agents.run`
2. Connect to the AI-enhanced application

### Phase IV
1. Build and deploy to Kubernetes: `cd Phase-IV && kubectl apply -f k8s/`
2. Access the application via the exposed service

## Quality Standards

### Phase I
- Clean CLI interface design
- Specification-driven development
- Comprehensive unit tests

### Phase II
- Clean folder structure
- Clear separation of concerns
- Predictable API responses
- Graceful error handling
- Type safety with TypeScript

### Phase III
- Responsible AI implementation
- Proper error handling for AI services
- Ethical AI usage guidelines
- Clear AI interaction patterns

### Phase IV
- Production-ready containerization
- Scalable Kubernetes configurations
- Observability and monitoring
- Disaster recovery procedures

## Development Guidelines

### Multi-Phase Development
- Follow the sequential phase development approach
- Build upon previous phases with iterative enhancements
- Maintain backward compatibility where possible
- Follow the Specification Driven Development (SDD) approach across all phases

### Phase-Specific Guidelines

#### Phase I
- Focus on CLI interface design
- Implement core functionality
- Establish specification-driven foundation

#### Phase II
- Maintain data isolation between users
- Implement proper error handling
- Use environment variables for configuration
- Follow security best practices
- Ensure clean separation of frontend and backend

#### Phase III
- Implement AI features responsibly
- Follow ethical AI usage guidelines
- Maintain security with AI integration
- Design clear AI interaction patterns

#### Phase IV
- Create production-ready containerization
- Implement scalable Kubernetes configurations
- Set up comprehensive monitoring and observability
- Ensure disaster recovery procedures

### Cross-Phase Guidelines
- Use environment variables for configuration
- Follow security best practices in all phases
- Maintain consistent coding standards
- Document architectural decisions using ADRs
- Follow the SpecifyPlus framework and SDD methodology