from fastapi import FastAPI
from app.api import forecast

app = FastAPI(
    title="VIEWS Forecast API",
    description="Hackathon MVP – conflict forecasts via FastAPI",
    version="0.1.0",
)

app.include_router(forecast.router)
