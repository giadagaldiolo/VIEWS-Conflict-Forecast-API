from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(title="VIEWS Forecasts API")

# Mount API routes
app.include_router(api_router, prefix="/api")

