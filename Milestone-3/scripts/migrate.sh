#!/bin/bash
set -e

# Debugging: Print Python and Flask paths
echo "Python version: $(python --version)"
echo "Flask command location: $(which flask)"

export FLASK_APP=run:app

# Check for existing migrations
if [ ! -d migrations/versions ] || [ -z "$(ls -A migrations/versions 2>/dev/null)" ]; then
    echo "No migrations found. Initializing..."
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
else
    echo "Migrations found. Upgrading..."
    flask db upgrade
fi


