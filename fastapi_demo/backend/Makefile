# Run FastAPI app with hot reload (development mode)
run:
	uvicorn app.main:app --reload

# Run tests with pytest and show coverage report
test:
	pytest --cov=app --cov-report=term-missing

# Run ruff linter and fix issues automatically
lint:
	ruff --fix app tests

# Build Docker image tagged as views-mvp
docker-build:
	docker build -t views-mvp .

# Run Docker container with port 8000 exposed
docker-run:
	docker run -p 8000:8000 views-mvp
