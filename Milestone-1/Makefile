# Define variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
FLASK = $(PYTHON) -m flask
PYTEST = $(VENV)/bin/pytest
APP = run.py

# Setup target
setup: venv install-dependencies test reset-db migrate upgrade run clean

# Create virtual environment
venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV); \
	fi

# Install dependencies
install-dependencies: venv
	@echo "Installing dependencies..."
	@$(PIP) install -r requirements.txt

# Run tests
test: venv
	@echo "Running tests..."
	@$(PYTEST) ./tests/

# Create new database migrations after resetting DB and migrations
migrate: venv reset-db
	@echo "Creating new database migrations..."
	@if [ ! -d "migrations" ]; then \
		$(FLASK) db init; \
	fi
	@$(FLASK) db migrate -m "Initial migration"

# Apply migrations to the database
upgrade: venv
	@echo "Upgrading database..."
	@$(FLASK) db upgrade

# Run the Flask app
run: venv
	@echo "Starting Flask app..."
	@$(PYTHON) $(APP)

# Reset the database and migrations (deletes students.db and migrations)
reset-db:
	@echo "Resetting database and migrations..."
	@rm -f students.db || true  # Ignore error if students.db doesn't exist
	@rm -rf migrations || true  # Ignore error if migrations doesn't exist

# Clean up environment
clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV)
	@find . -type f -name "*.pyc" -delete || true  # Ignore errors if no .pyc files exist
	@find . -type d -name "__pycache__" -delete || true  # Ignore errors if no __pycache__ directories exist

.PHONY: setup venv install-dependencies test migrate upgrade run clean reset-db
