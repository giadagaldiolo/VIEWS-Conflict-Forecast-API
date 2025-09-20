# VIEWS Conflict Forecast API - MVP

This repository implements the MVP of the VIEWS conflict forecasting API.
It exposes 36 months of synthetic raster forecasts (0.5° grid) via FastAPI.
The repository **focuses on the backend API**. An optional frontend viewer (Vite + React) is included for demo/test purposes.

---

## Goals (MVP)
- Serve forecast data (grid cells × months).
- MVP supports grid-cell queries; design remains open to extend with admin identifiers later.
- Support queries by grid id(s), by month or month range, or by country id.
- Allow selecting which metrics (of the 13) to return.
- JSON (or NDJSON for large responses) output.
- Typing (pydantic), linting (ruff), and tests (pytest).

---

## Repo layout (relevant parts)
```
.
├── README.md
├── Makefile
├── docker-compose.yml
├── backend/
│ ├── Dockerfile # backend image
│ ├── requirements.txt
│ └── app/
│ ├── api.py # FastAPI routes
│ ├── schemas.py
│ ├── storage_reader.py
│ └── data/ # sample/tiny test data
└── frontend/
├── Dockerfile # optional frontend image
└── frontend/ # vite app
```
---

## Quick start (15 minutes)

### Backend only (default)

```bash
# 1) clone repo and move to repo root
git clone <repo-url>
cd <repo-root>

# 2) build backend image
docker build -t views-mvp-backend ./backend

# 3) run backend
docker run --rm -p 8000:8000 \
  -e PORT=8000 \
  -e FORECAST_DATA_PATH=/app/data \
  views-mvp-backend
```
### Frontend (optional, local dev)
```bash

cd fastapi_demo/frontend/frontend
npm install
npm run dev
# served at http://localhost:5173
# make sure VITE_API_URL points to backend (default http://localhost:8000)
```
### Backend + Frontend (docker-compose)
```bash
docker-compose up --build
# backend -> http://localhost:8000
# frontend -> http://localhost:5173
```
## Endpoints (MVP)
- GET /months → available months
- GET /cells → available grid cell ids
- GET /forecasts → main query
### Parameters:
- priogrid_id = one or many IDs
- country_id = optional M49 code
- month_id = single or range
- metrics = list of metrics to return
### Example:
```bash
curl "http://localhost:8000/forecasts?priogrid_id=12345&month_id=2025-01&metrics=MAP,pred_ln_sb_best"
```
### Response:
```json
[
  {
    "priogrid_id": 12345,
    "lat": 12.34,
    "lon": 56.78,
    "country_id": 840,
    "MAP": 0.123,
    "pred_ln_sb_best": [0.1,0.2,0.3]
  }
]
```
## Environment variables
### Backend
```ini
PORT=8000
FORECAST_DATA_PATH=/app/data
```
### Frontend
```ini
VITE_API_URL=http://localhost:8000
```
### Makefile commands
```bash
make run-backend   # run backend via docker
make run-frontend  # run frontend via docker
make run-all       # backend + frontend via docker-compose
make test          # run pytest
make lint          # run ruff
make format        # run black
make clean         # remove caches
```
## Notes
- Admin-1 / Admin-2 reserved for later.
- NDJSON streaming planned.
- All forecasts are synthetic MVP data.