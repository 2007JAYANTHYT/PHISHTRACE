from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db.seed import seed_database_and_samples
from .api.routes import health, emails, analysis, campaigns, evidence, ai, integrations

app = FastAPI(
    title="PhishTrace API",
    description="AI Email Threat Detection, Geolocation & Forensic Intelligence Platform",
    version=settings.VERSION
)

# Restrictive CORS configuration for local SOC frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(emails.router, prefix="/api", tags=["Emails"])
app.include_router(analysis.router, prefix="/api", tags=["Analysis"])
app.include_router(campaigns.router, prefix="/api", tags=["Campaigns"])
app.include_router(evidence.router, prefix="/api", tags=["Evidence"])
app.include_router(ai.router, prefix="/api", tags=["Open-Source AI"])
app.include_router(integrations.router, prefix="/api", tags=["Integrations"])

@app.on_event("startup")
def startup_event():
    seed_database_and_samples()

@app.get("/")
def root():
    return {
        "platform": "PhishTrace",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
