from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.tasks import router as tasks_router
from api.conversations import router as conversations_router
from api.chat import router as chat_router
from db.database import create_db_and_tables
import uvicorn
import os


app = FastAPI(title="Todo App API", version="1.0.0")

# CORS middleware - adjust origins as needed for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(tasks_router)
app.include_router(conversations_router)
app.include_router(chat_router)


@app.on_event("startup")
def on_startup():
    """Initialize database tables on startup"""
    create_db_and_tables()


@app.get("/")
def read_root():
    """Root endpoint for health check"""
    return {"message": "Todo App API is running!"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)