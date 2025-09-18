from fastapi import FastAPI
from app.api import forecast

app = FastAPI()
app.include_router(forecast.router)
