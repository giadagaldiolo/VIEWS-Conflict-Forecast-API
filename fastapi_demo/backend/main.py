from fastapi import FastAPI
from app.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="VIEWS Forecasts API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev serverのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(api_router, prefix="/api")

