run:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	ruff app tests

docker-build:
	docker build -t views-mvp .

docker-run:
	docker run -p 8000:8000 views-mvp
