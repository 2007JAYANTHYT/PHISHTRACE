import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SAMPLES_DIR = BASE_DIR.parent / "samples"
DATA_DIR.mkdir(parents=True, exist_ok=True)
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

# Load local .env if present
env_file = BASE_DIR / ".env"
if env_file.exists():
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if k and k not in os.environ:
                        os.environ[k] = v
    except Exception:
        pass

class Settings(BaseModel):
    PROJECT_NAME: str = "PhishTrace"
    VERSION: str = "1.0.0"
    HOST: str = os.getenv("PHISHTRACE_HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PHISHTRACE_PORT", "8000"))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "phishtrace-super-secret-key-hacktober-2026")
    
    # Open-Source AI Configuration (NVIDIA NIM / Groq / Deterministic NLP)
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "nvidia") # nvidia, groq, fallback
    OPENSOURCE_MODEL_NAME: str = os.getenv("OPENSOURCE_MODEL_NAME", "meta/llama-3.2-11b-vision-instruct")
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    
    # Gmail OAuth Settings (Read-Only)
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://127.0.0.1:8000/api/integrations/gmail/callback")
    GMAIL_READ_ONLY_SCOPE: str = "https://www.googleapis.com/auth/gmail.readonly"
    
    # Database
    DATABASE_URL: str = f"sqlite:///{DATA_DIR / 'phishtrace.db'}"
    
    # Geolocation Cache
    IP_GEO_CACHE_FILE: Path = DATA_DIR / "ip_geo_cache.json"

settings = Settings()
