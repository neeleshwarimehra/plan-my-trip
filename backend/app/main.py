import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.trips import router as trips_router

app = FastAPI(
    title="PlanMyTrip API",
    description="AI-powered multi-agent travel planning platform",
    version="1.0.0",
)

extra_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://plan-my-trip-bice.vercel.app",
        "https://plan-my-trip-igazf805t-theindiedeveloper.vercel.app",
        "https://plan-my-trip-ai-multi-agent-travel-planner.vercel.app",
        *extra_origins,
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to PlanMyTrip API",
        "status": "running",
    }


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "application": "PlanMyTrip",
        "version": "1.0.0",
    }


app.include_router(trips_router)