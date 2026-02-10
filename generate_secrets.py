import os
import base64
from pathlib import Path

# Load .env
from dotenv import load_dotenv
load_dotenv()

def b64_encode(s):
    return base64.b64encode(s.encode()).decode()

gemini_key = os.getenv("GEMINI_API_KEY", "your-gemini-key-here")
db_url = os.getenv("DATABASE_URL", "postgresql://todo_user:todo_password@postgres:5432/todo_db")
jwt_secret = os.getenv("JWT_SECRET_KEY", "your-jwt-secret")
postgres_password = os.getenv("POSTGRES_PASSWORD", "todo_password")

yaml_content = f"""apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets
type: Opaque
data:
  GEMINI_API_KEY: {b64_encode(gemini_key)}
  DATABASE_URL: {b64_encode(db_url)}
  JWT_SECRET_KEY: {b64_encode(jwt_secret)}
  POSTGRES_PASSWORD: {b64_encode(postgres_password)}
"""

path = Path("Phase-IV/k8s/secrets.yaml")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(yaml_content)
print(f"Generated {path} with GEMINI_API_KEY present.")
