# Scripts

This directory contains utility scripts for the canonical-grounding project.

## Markdown Converter

Convert Markdown files to professional HTML and PDF formats.

### Quick Start

```bash
# Convert single file (creates HTML and PDF)
./scripts/convert_markdown.sh domains/ddd/docs/ddd-guide.md

# Convert to PDF only
./scripts/convert_markdown.sh --format pdf domains/ddd/docs/ddd-guide.md

# Batch convert all files in directory
./scripts/convert_markdown.sh --all --dir docs/

# Include table of contents
./scripts/convert_markdown.sh --toc README.md
```

### First Time Setup

The shell wrapper automatically:
1. Creates a Python virtual environment (`venv/`)
2. Installs required dependencies
3. Runs the conversion

On macOS, it will also install system dependencies via Homebrew if available.

### Manual Setup (if needed)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r scripts/requirements.txt

# On macOS, install system packages
brew install pango

# On Ubuntu/Debian
sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

### Usage Options

```
./scripts/convert_markdown.sh [options] <file.md>

Options:
  --format html|pdf|both    Output format (default: both)
  --output <dir>            Output directory (default: output/)
  --style <name|file>       Stylesheet: "classic", "modern", or custom CSS file (default: classic)
  --toc                     Include table of contents
  --all                     Convert all .md files
  --dir <path>              Directory to scan (with --all)

Built-in Stylesheets:
  classic - Professional serif style (Georgia font)
  modern  - Clean sans-serif style (Helvetica font)
```

### Examples

**Single file with TOC (classic style):**
```bash
./scripts/convert_markdown.sh --toc --format pdf domains/ddd/docs/ddd-guide.md
```

**Modern style PDF:**
```bash
./scripts/convert_markdown.sh --style modern --format pdf document.md
```

**Batch conversion with modern style:**
```bash
./scripts/convert_markdown.sh --all --dir domains/ddd/docs/ --style modern --output output/docs/
```

**Custom CSS file:**
```bash
./scripts/convert_markdown.sh --style custom.css --format both README.md
```

### Output

Generated files are placed in the `output/` directory by default:
- `output/filename.html` - Standalone HTML with embedded CSS
- `output/filename.pdf` - Professional PDF document

### Features

**HTML Output:**
- Standalone (CSS embedded)
- Syntax highlighted code blocks
- Responsive design
- Clickable links
- Embedded images

**PDF Output:**
- A4 page size
- Page numbers in footer
- Proper margins (2cm)
- Clickable links
- Professional styling
- Code blocks don't break across pages

### Styling

The converter includes two professional built-in stylesheets:

#### Classic Style (Default)
- **Font**: Georgia serif
- **Look**: Traditional, academic, print-ready
- **Best for**: Documentation, books, formal reports
- **File size**: Slightly larger due to serif fonts

#### Modern Style
- **Font**: Helvetica Neue sans-serif
- **Look**: Clean, contemporary, web-native
- **Best for**: Technical docs, presentations, modern guides
- **File size**: Slightly smaller, faster rendering

#### Custom Styling

To use your own stylesheet:

1. Create a CSS file with your styles
2. Use `--style path/to/file.css`

Example custom.css:
```css
body {
    font-family: 'Helvetica', sans-serif;
    max-width: 900px;
}

h1 {
    color: #2c3e50;
    border-bottom: 3px solid #3498db;
}

code {
    background-color: #f8f8f8;
}
```

Custom stylesheets inherit PDF page settings (@page rules) automatically.

### Troubleshooting

**Error: "ModuleNotFoundError: No module named 'weasyprint'"**
- Solution: Delete `venv/` directory and run script again
- Or: Manually activate venv and run `pip install -r scripts/requirements.txt`

**Error: "WeasyPrint failed to generate PDF"**
- macOS: `brew install pango`
- Ubuntu: `sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0`

**Error: "command not found: ./scripts/convert_markdown.sh"**
- Solution: `chmod +x scripts/convert_markdown.sh`

**Images not showing in PDF:**
- Ensure image paths are absolute or relative to the .md file
- Check images are accessible

**Slow conversion:**
- Large files (>100 pages) take 10-30 seconds
- This is normal for PDF generation

### Dependencies

Python packages (installed automatically):
- `markdown` - Markdown to HTML conversion
- `weasyprint` - HTML to PDF rendering
- `pygments` - Syntax highlighting

System packages (install manually):
- macOS: `brew install pango`
- Ubuntu: `sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0`

### GitHub Copilot Integration

This script is integrated with GitHub Copilot:
- Use `@workspace /convert-markdown` in Copilot Chat
- Instructions apply automatically to .md files
- See `.github/prompts/convert-markdown.prompt.md` for details

### Direct Python Usage

If you prefer to use Python directly:

```bash
# Activate venv first
source venv/bin/activate

# Run Python script
python scripts/convert_markdown.py [options] <file.md>

# Deactivate when done
deactivate
```

### CI/CD Integration

Example GitHub Actions workflow:

```yaml
- name: Convert docs
  run: |
    ./scripts/convert_markdown.sh --all --dir docs/

- name: Upload PDFs
  uses: actions/upload-artifact@v4
  with:
    name: documentation
    path: output/*.pdf
```

### Performance

Typical conversion times:
- Small file (1-10 pages): <1 second
- Medium file (10-50 pages): 1-5 seconds
- Large file (50-200 pages): 5-30 seconds
- Batch (10 files): 5-10 seconds

### Support

For issues or questions:
1. Check this README
2. See `.github/prompts/convert-markdown.prompt.md`
3. Check conversion script comments in `convert_markdown.py`
