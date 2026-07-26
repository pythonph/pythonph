#!/bin/bash

# Render build script for pythonph
# Runs on each deploy to set up the environment

# Upgrade pip and install UV
pip install --upgrade pip
pip install uv

# Install dependencies
echo "Installing dependencies..."
uv sync

# Apply database migrations
echo "Applying database migrations..."
uv run manage.py migrate --noinput

# Create cache table
echo "Creating cache table..."
uv run manage.py createcachetable

# Build Tailwind CSS
echo "Building Tailwind CSS..."
uv run manage.py tailwind build

# Collect static files
echo "Collecting static files..."
uv run manage.py collectstatic --noinput
