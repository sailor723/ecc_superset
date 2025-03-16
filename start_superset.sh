#!/bin/bash

# Change to the Superset directory
cd ~/dev/Learn/superset

# Set environment variables
export PYTHONPATH=$PYTHONPATH:$PWD
export SUPERSET_CONFIG_PATH=superset_config.py
export FLASK_APP=superset

# Generate random secrets
export SUPERSET_SECRET_KEY=$(openssl rand -base64 42)
export SUPERSET_JWT_SECRET=$(openssl rand -base64 32)

# Activate virtual environment
source venv/bin/activate

# Kill any existing Superset processes
pkill -f superset

# Initialize Superset
superset init

# Start Superset
superset run -h 0.0.0.0 -p 8088 --with-threads --reload --debugger