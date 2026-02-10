"""Configuration module for the Todo App backend"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-secret-key-for-development")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30

# AI Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
AI_MODEL_PROVIDER = os.getenv("AI_MODEL_PROVIDER", "gemini")