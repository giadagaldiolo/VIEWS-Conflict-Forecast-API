# VIEWS Conflict Forecast API
> 3rd Place at JunctionXOulu 2025 Hackathon, *VIEWS Challenge*

## Overview

This project implements a public API for the next iteration of the **VIEWS armed conflict forecasting system**, exposing **36 months of global raster forecasts** on a 0.5° decimal grid. Each grid cell per month provides **13 forecast values**, including:

- **MAP** (Most Accurate Prediction)  
- **HDI** (50%, 90%, 99%)  
- **Six threshold probabilities**  

Each cell is uniquely identified by:

- **PRIO-Grid ID**  
- **Centroid latitude/longitude**  
- **Country ID (UN M49)**  

Optional extensions include **Admin-1 / Admin-2 IDs** and **actor-level information**, allowing future aggregation and linking to administrative units.

The project consists of:

- **Backend:** Python + FastAPI, layered architecture for clean separation of concerns  
- **Frontend:** React + TypeScript, MVC structure  
- **Data:** Synthetic `.parquet` files included  
- **Containerized:** Docker Compose for reproducible setup  

---

## Architecture

### Backend (Layered Architecture)

- `application/` – API routes and FastAPI router  
- `business/` – Business logic and service layer  
- `dataAccess/` – Reading/parsing `.parquet` files, data retrieval  
- `test/` – Pytest tests for API endpoints  
- `main.py` – FastAPI application entry point  

This layered approach ensures:

- Separation of concerns  
- Easy testability  
- Future extensibility (Admin/Actor-level aggregation)  

### Frontend (MVC)

- `src/controller/`  
- `src/view/` – React components (Views)  
- `src/model/` – TypeScript interfaces for ForecastData, Country, Month  
- `src/App.tsx` – Main application orchestrating query and viewer components  

---

## Features

- Retrieve available months, countries, and grid cells  
- Query forecast values by month, country, or cell ID  
- Select specific metrics (MAP, HDIs, thresholds)  
- Supports line-by-line JSON for large datasets  
- Modular, typed Python with **pydantic**  
- Dockerized for fast local setup  
- Tests included (**pytest**) and linting with **ruff**  

---

## Prerequisites

- **Docker Desktop** (recommended)  
- Alternatively: **Python 3.11+**, **Node.js 20+**, **npm**  
- Synthetic data allows running the full system **in under 15 minutes**


## Quick Start

### Using Docker Compose (Recommended)

Navigate to the project folder: cd fastapi_demo
Build and run containers: docker compose up --build
Access services:
- Backend API: http://127.0.0.1:8000/docs
- Frontend: http://localhost:5173

Everything runs with the synthetic data included.

## Running Locally Without Docker
### Backend

cd fastapi_demo/backend
python -m venv venv

Activate virtual environment:
- Linux/macOS: source venv/bin/activate
- Windows: venv\Scripts\activate

Install dependencies: pip install -r requirements.txt
Run the backend: uvicorn main:app --reload
API Docs: http://127.0.0.1:8000/docs

### Frontend

cd fastapi_demo/frontend
npm install --legacy-peer-deps
npm run dev
Frontend: http://localhost:5173

Testing & Linting
Run backend tests: cd fastapi_demo/backend
pytest
Linting:
ruff .


## File Structure
```
fastapi_demo/
├─ backend/             # FastAPI backend
│  ├─ application/     # Routes
│  ├─ business/        # Services
│  ├─ dataAccess/      # Data loading/parsing
│  ├─ test/            # Pytest tests
│  ├─ Dockerfile
│  ├─ main.py
│  ├─ requirements.txt
│  ├─ Makefile
├─ frontend/            # React frontend (MVC)
│  ├─ src/
│  │  ├─ controller/
│  │  ├─ view/
│  │  ├─ model/
│  │  ├─ App.tsx
│  ├─ package.json
│  ├─ Dockerfile
│  ├─ vite.config.ts
├─ data/                # Synthetic .parquet files
├─ docker-compose.yml
├─ README.md
```
## Notes
- Backend is typed with pydantic and optionally checked with mypy
- Modular and clean design following Clean Architecture principles
- Synthetic data allows running the full system in under 15 minutes
