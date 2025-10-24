#!/bin/bash
#
# Markdown to HTML/PDF Converter - Shell Wrapper
#
# This script sets up a Python virtual environment and runs the conversion tool.
#
# Usage:
#   ./scripts/convert_markdown.sh <file.md>
#   ./scripts/convert_markdown.sh --all --dir docs/
#

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$PROJECT_ROOT/venv"
PYTHON_SCRIPT="$SCRIPT_DIR/convert_markdown.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Markdown Converter${NC}"
echo "=================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or later"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Check if dependencies are installed
if ! python -c "import markdown, weasyprint, pygments" 2>/dev/null; then
    echo -e "${YELLOW}Installing dependencies...${NC}"

    # Install system dependencies on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            echo "Installing system dependencies via Homebrew..."
            brew install pango || true
        else
            echo -e "${YELLOW}Warning: Homebrew not found. WeasyPrint may not work without pango.${NC}"
            echo "Install Homebrew from https://brew.sh/ and run: brew install pango"
        fi
    fi

    # Install Python packages
    pip install --upgrade pip setuptools wheel
    pip install -r "$SCRIPT_DIR/requirements.txt"
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
fi

# Run the Python script with all arguments
echo ""
echo "Running conversion..."
python "$PYTHON_SCRIPT" "$@"

# Capture exit code
EXIT_CODE=$?

# Deactivate virtual environment
deactivate

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "\n${GREEN}✓ Conversion completed successfully${NC}"
else
    echo -e "\n${RED}✗ Conversion failed with exit code $EXIT_CODE${NC}"
fi

exit $EXIT_CODE
