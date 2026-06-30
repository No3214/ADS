from fastapi import FastAPI
from kads.api.routes_approval import router as approval_router
from kads.observability.health import audit_tracking_health

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="KADS Autonomous Advertising API",
    description="Backend API for managing KADS v2.0 AI Advertising Agent Council, approvals, and tracking health.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "https://kozbeylikonagi.com",
        "https://www.kozbeylikonagi.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(approval_router)

@app.get("/health")
def health_check():
    """
    Returns API status combined with the current Tracking Health audit.
    """
    tracking = audit_tracking_health()
    return {
        "status": "online",
        "tracking_health": tracking
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("kads.api.main:app", host="127.0.0.1", port=8000, reload=True)
