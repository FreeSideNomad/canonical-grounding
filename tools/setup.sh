#!/bin/bash
# Setup script for validation tool

set -e

echo "Setting up Canonical Grounding validation tool..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "To run validation:"
echo "  1. source venv/bin/activate"
echo "  2. python validate-schemas.py"
echo ""
echo "Or run directly:"
echo "  ./run-validation.sh"
