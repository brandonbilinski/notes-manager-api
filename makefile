DOCKER_COMPOSE = docker-compose
ALEMBIC_CMD = alembic
DB_NAME = notes_db
USER = testuser

.PHONY: up wait-db migrate api

up:
	$(DOCKER_COMPOSE) up

down:
	$(DOCKER_COMPOSE) down

migrate:
	$(ALEMBIC_CMD) upgrade head

wait-db:
	@echo "Waiting for DB to start"
	@until docker exec $(DB_NAME) pg_isready -U $(USER) -h localhost; do \
		@echo "Still waiting..."; \
		sleep 1; \
	done
	@echo "Postgres DB is ready"
api:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run: up wait-db migrate api

