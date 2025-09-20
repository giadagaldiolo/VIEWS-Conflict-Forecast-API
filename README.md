# VIEWS Conflict Forecast API - MVP

This is the MVP version of the VIEWS conflict forecasting API.  
It exposes 36 months of global raster forecasts (0.5° grid) via FastAPI.

## Quick Start

### 1. Clone the repository
```bash
git clone <repo-url>
cd JunctionHack/fastapi_demo
```
### 2. Build Docker image
```bash
docker build -t views-mvp .
```
### 3. Run the API
```bash
docker run -p 8000:8000 views-mvp
```
The API will be available at http://localhost:8000.
### 4. Run tests
```bash
make test
```
### 5. Lint and type checks
```bash
make lint
mypy app/main.py
```
## API Endpoints
/forecasts

Query forecasts by grid cell, month, or country.

### Parameters:
priogrid_id: single ID or list of IDs
month_id: single month or range
country_id: optional
metrics: list of metrics to return (MAP, HDIs, threshold probabilities)
### Example Request:
```bash
curl "http://localhost:8000/forecasts?priogrid_id=12345&month_id=1&metrics=MAP,pred_ln_sb_best"
```
### Response:
```bash
[
  {
    "priogrid_id": 12345,
    "lat": 12.34,
    "lon": 56.78,
    "country_id": 840,
    "MAP": 0.123,
    "pred_ln_sb_best": [0.1, 0.2, 0.3],
    ...
  }
]
```
## Makefile Commands
```bash
make run       # Run API locally
make test      # Run pytest
make lint      # Run ruff
make format    # Run black formatter
make clean     # Clean caches
```
## Notes
- Admin-1 / Admin-2 IDs are not yet implemented.
- NDJSON / streaming responses for large datasets are planned for next iteration.
- All forecasts are synthetic test data for MVP purposes.