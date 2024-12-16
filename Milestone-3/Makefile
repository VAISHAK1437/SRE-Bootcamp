DB_CONTAINER = my-postgres
APP_SERVICE = app
COMPOSE_FILE = docker-compose.yaml
# Build the Docker Compose setup
compose-build:
	docker compose -f $(COMPOSE_FILE) build

# Start the Docker Compose setup
compose-up:
	docker compose -f $(COMPOSE_FILE) up -d

# Run migrations inside the app container
compose-migrate:
	docker compose -f $(COMPOSE_FILE) exec $(APP_SERVICE) sh -c "\
		if [ ! -d migrations/versions ] || [ -z \"\`ls migrations/versions 2>/dev/null\`\" ]; then \
			echo 'No migrations found. Initializing...'; \
			python -m flask db init > /dev/null 2>&1 && \
			python -m flask db migrate --message 'Initial migration' > /dev/null 2>&1 && \
			python -m flask db upgrade > /dev/null 2>&1; \
		else \
			echo 'Migrations found. Upgrading...'; \
			python -m flask db stamp head > /dev/null 2>&1 && \
			python -m flask db upgrade > /dev/null 2>&1; \
		fi"

# Stop and remove the containers (excluding volumes)
compose-down:
	docker compose -f $(COMPOSE_FILE) down

# Remove all containers, volumes, and networks
compose-clean:
	docker compose -f $(COMPOSE_FILE) down -v

# Completely clean the environment
clean:
	@docker compose -f $(COMPOSE_FILE) down
	# @echo "Removing the persistent volume for the database..."
	# @docker volume rm -f postgres-data || true
	@docker volume prune -f
	@docker network prune -f
	@docker rmi -f $$(docker images -q) || true
	@docker container prune -f || true
	@docker system prune -f || true
	@echo "All containers, images, volumes, and networks have been removed."

# Full setup (clean, build, run, migrate)
setup: clean compose-build compose-up compose-migrate

# Prune unused images
prune-old-images:
	docker images -q --filter "dangling=true" | xargs --no-run-if-empty docker rmi
