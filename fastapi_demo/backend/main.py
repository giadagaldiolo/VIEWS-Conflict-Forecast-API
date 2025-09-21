"""
VIEWS Forecasts API - FastAPI application entry point.

This module initializes the FastAPI app, sets up CORS middleware,
and mounts the API router under the '/api' prefix.

Attributes:
    app (FastAPI): The FastAPI application instance.
"""

from fastapi import FastAPI
from application.router_application import router as api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="VIEWS Forecasts API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes under /api prefix
app.include_router(api_router, prefix="/api")

