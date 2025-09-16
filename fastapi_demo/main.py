from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/forecast/{grid_id}")
async def get_forecast(grid_id: int):
    # ダミーデータ返すだけ
    return {"grid_id": grid_id, "forecast": "Sunny"}
