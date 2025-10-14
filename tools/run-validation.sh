#!/bin/bash
# Run validation tool with virtual environment

set -e

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    ./setup.sh
fi

# Activate and run
source venv/bin/activate
python validate-schemas.py
