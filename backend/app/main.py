from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import analytics, auth, cameras, notifications, occupancy, seats

app = FastAPI(title=settings.project_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(cameras.router)
app.include_router(seats.router)
app.include_router(occupancy.router)
app.include_router(analytics.router)
app.include_router(notifications.router)


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "service": settings.project_name}
