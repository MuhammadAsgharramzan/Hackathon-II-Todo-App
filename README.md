# Todo App - Phase II (Full-Stack Web Application)

This is the Phase II implementation of the Todo App, transforming the CLI application into a secure, multi-user, full-stack web application using Spec-Driven Development.

## Vision
Phase-II transforms the Phase-I CLI Todo App into a secure, multi-user, full-stack web application using Spec-Driven Development.

## Technology Stack

### Frontend
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth (for authentication)

### Backend
- FastAPI (Python)
- SQLModel (ORM)
- JWT (Authentication)

### Database
- PostgreSQL (Neon)

## Features

### User Management
- User registration and login
- JWT-based authentication
- Secure token management

### Task Management
- Create, Read, Update, Delete (CRUD) operations for tasks
- Mark tasks as complete/incomplete
- User-specific task isolation
- Data validation and error handling

### Security
- JWT token verification on every request
- User data isolation (users can only access their own tasks)
- Secure API endpoints

## Architecture

### Frontend Structure
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

### Backend Structure
```
backend/
├── main.py              # Main FastAPI application
├── models/              # Database models (SQLModel)
├── api/                 # API routes
├── auth/                # Authentication utilities
└── db/                  # Database configuration
```

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Tasks
- `GET /tasks` - Get all tasks for authenticated user
- `POST /tasks` - Create a new task
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task
- `PATCH /tasks/{id}/toggle-complete` - Toggle task completion status

## Security Rules
- Every API request requires a valid JWT token
- Users can only access their own tasks
- Backend verifies token on every request
- Invalid or missing tokens return 401 Unauthorized

## Setup Instructions

### Prerequisites
- Node.js (for frontend)
- Python 3.13+ (for backend)
- PostgreSQL (or Neon database)

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables:
   ```bash
   export DATABASE_URL="postgresql://username:password@localhost/todo_db"
   export JWT_SECRET_KEY="your-secret-key-change-in-production"
   ```
4. Run the server: `python main.py`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Set environment variables in `.env.local`:
   ```bash
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```
4. Run the development server: `npm run dev`

## Environment Variables

### Backend
- `DATABASE_URL`: PostgreSQL database connection string
- `JWT_SECRET_KEY`: Secret key for JWT signing
- `PORT`: Port for the FastAPI server (default: 8000)

### Frontend
- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API

## Running the Application

1. Start the backend server
2. Start the frontend development server
3. Access the application at `http://localhost:3000`

## Quality Standards
- Clean folder structure
- Clear separation of concerns
- Predictable API responses
- Graceful error handling
- Type safety with TypeScript

## Development Guidelines
- Follow the Spec-Driven Development approach
- Maintain data isolation between users
- Implement proper error handling
- Use environment variables for configuration
- Follow security best practices