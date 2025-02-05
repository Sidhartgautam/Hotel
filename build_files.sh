#!/bin/bash

# Create necessary directories
mkdir -p static media

# Export static root for collectstatic
export STATIC_ROOT=static

# Install dependencies
pip3 install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput

# Create migrations (optional, if needed)
python3 manage.py migrate
