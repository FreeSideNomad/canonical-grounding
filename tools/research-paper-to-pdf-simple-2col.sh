#!/bin/bash

# Simplified 2-column PDF conversion for research paper
# Preprocesses markdown then uses standard Pandoc with 2-column layout

set -e

INPUT_FILE="canonical-grounding-paper.md"
PROCESSED_FILE="canonical-grounding-paper-processed.md"
OUTPUT_FILE="canonical-grounding-paper.pdf"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Research Paper PDF Conversion (Simplified 2-Column) ===${NC}"

# Check files
if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}Error: $INPUT_FILE not found${NC}"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 not installed${NC}"
    exit 1
fi

if ! command -v pandoc &> /dev/null; then
    echo -e "${RED}Error: pandoc not installed${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Preprocessing markdown...${NC}"
python3 preprocess-paper.py "$INPUT_FILE" "$PROCESSED_FILE"

echo -e "${YELLOW}Step 2: Converting to 2-column PDF...${NC}"

# Simple 2-column conversion with proper academic styling
# No TOC, 2-column layout, smaller margins for conference style
# Using preamble file to redefine longtable to work in 2-column mode
# Using narrow columns setting to help with code/formula wrapping
pandoc "$PROCESSED_FILE" \
    -o "$OUTPUT_FILE" \
    --pdf-engine=xelatex \
    --number-sections \
    --syntax-highlighting=none \
    -H preamble-2col.tex \
    --columns=50 \
    -V geometry:margin=0.75in \
    -V geometry:columnsep=0.33in \
    -V fontsize=9pt \
    -V documentclass=article \
    -V classoption=twocolumn \
    -V linkcolor=blue \
    -V urlcolor=blue \
    2>&1

if [ $? -eq 0 ] && [ -f "$OUTPUT_FILE" ]; then
    echo -e "${GREEN}✓ PDF created: $OUTPUT_FILE${NC}"

    FILE_SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
    if command -v mdls &> /dev/null; then
        PAGE_COUNT=$(mdls -name kMDItemNumberOfPages "$OUTPUT_FILE" 2>/dev/null | awk '{print $3}')
        echo -e "${GREEN}  Size: $FILE_SIZE, Pages: $PAGE_COUNT${NC}"
    fi

    # Open PDF
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$OUTPUT_FILE"
    fi
else
    echo -e "${RED}✗ Conversion failed${NC}"
    exit 1
fi

echo -e "${GREEN}=== Complete ===${NC}"
