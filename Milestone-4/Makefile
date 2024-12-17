# Define variables
APP_IMAGE = flask-app
APP_CONTAINER = app
DB_CONTAINER = my-postgres
APP_PORT = 5000
NETWORK = app-network
DB_VOLUME = postgres-data
VERSION = 1.0.0
GITHUB_SHA ?= $(shell git rev-parse HEAD)
GITHUB_ACTOR ?= $(shell echo $$GITHUB_ACTOR)
GITHUB_REGISTRY = ghcr.io

# Pull the Postgres image
db-pull:
	docker pull postgres

# Create a Docker network
network-create:
	docker network create $(NETWORK) || true

# Create a Docker volume for persistent storage
volume-create:
	docker volume create $(DB_VOLUME) || true

# Run the Postgres container in the network with a volume
db-up: network-create volume-create
	@eval $$(cat .env) && docker run --name $(DB_CONTAINER) --network $(NETWORK) \
		-v $(DB_VOLUME):/var/lib/postgresql/data \
		-e POSTGRES_USER=$$DB_USERNAME \
		-e POSTGRES_PASSWORD=$$DB_PASSWORD \
		-e POSTGRES_DB=$$DB_NAME \
		-p 5432:5432 -d postgres

# Build the Flask app image with versioned tagging
app-build:
	app-build:
		@echo "Logging into GitHub Container Registry (GHCR)..."
		echo "${GITHUB_TOKEN}" | docker login $(GITHUB_REGISTRY) -u "${GITHUB_ACTOR}" --password-stdin

		@echo "Building the Docker image..."
		docker build --build-arg VERSION=$(VERSION) -t $(APP_IMAGE):$(VERSION) .

		@echo "Tagging the image with commit SHA..."
		docker tag $(APP_IMAGE):$(VERSION) $(GITHUB_REGISTRY)/$(GITHUB_ACTOR)/$(APP_IMAGE):$(GITHUB_SHA)

		@echo "Pushing the image to GHCR..."
		docker push $(GITHUB_REGISTRY)/$(GITHUB_ACTOR)/$(APP_IMAGE):$(GITHUB_SHA)

# Run the Flask app container in the network, inject environment variables
app-run: network-create
	docker run --name $(APP_CONTAINER) --network $(NETWORK) -p $(APP_PORT):5000 -d $(APP_IMAGE):$(VERSION)

app-migrate:
	# Check if migration files exist; if not, initialize them
	docker exec -it app sh -c "\
		if [ ! -d migrations/versions ] || [ -z \"\`ls migrations/versions 2>/dev/null\`\" ]; then \
			echo 'No migrations found. Initializing...'; \
			python -m flask db init && \
			python -m flask db migrate --message 'Initial migration' && \
			python -m flask db upgrade; \
		else \
			echo 'Migrations found. Upgrading...'; \
			python -m flask db stamp head && \
			python -m flask db upgrade; \
		fi"

# Stop and remove the containers and network (excluding volume)
clean:
	docker stop $(DB_CONTAINER) $(APP_CONTAINER) || true
	docker rm $(DB_CONTAINER) $(APP_CONTAINER) || true
	docker network rm $(NETWORK) || true
	# Uncomment to remove volume only if needed
	# docker volume rm $(DB_VOLUME) || true

# Full setup with backup
setup: clean db-pull db-up app-build app-run app-migrate

# Remove old images that are not in use
prune-old-images:
	docker images -q --filter "dangling=true" | xargs --no-run-if-empty docker rmi
