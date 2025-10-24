---
description: Convert Markdown files to HTML and PDF formats with customization options
tags: [documentation, conversion, markdown, pdf, html]
---

# Convert Markdown to HTML and PDF

Convert Markdown documents to professional HTML and PDF formats using Python's markdown and weasyprint libraries.

## What This Does

This prompt helps you convert Markdown files to:
- **HTML**: Styled, standalone HTML files with CSS
- **PDF**: Professional PDF documents with proper formatting
- **Both**: Generate both formats simultaneously

## Usage

Use this prompt by typing:
```
@workspace /convert-markdown <filename.md>
```

Or for batch conversion:
```
@workspace /convert-markdown --all --dir docs/
```

## Options

- `--format html` - Generate HTML only
- `--format pdf` - Generate PDF only
- `--format both` - Generate both (default)
- `--output <dir>` - Output directory (default: `output/`)
- `--style <css>` - Custom CSS file for styling
- `--toc` - Include table of contents
- `--all` - Convert all .md files in directory
- `--dir <path>` - Directory to scan for .md files

## Examples

### Single file conversion
```bash
python scripts/convert_markdown.py domains/ddd/docs/ddd-guide.md
```

### Convert with custom styling
```bash
python scripts/convert_markdown.py --style custom.css --format both myfile.md
```

### Batch conversion
```bash
python scripts/convert_markdown.py --all --dir docs/ --output output/
```

### HTML only with TOC
```bash
python scripts/convert_markdown.py --format html --toc README.md
```

## What Gets Generated

For a file `document.md`, you'll get:
- `output/document.html` - Standalone HTML with embedded CSS
- `output/document.pdf` - Professional PDF document

Both files include:
- Proper heading hierarchy (H1-H6)
- Code syntax highlighting
- Tables with borders
- Images (embedded or linked)
- Hyperlinks (preserved in PDF)
- Custom styling from CSS

## Dependencies

The conversion script requires:
```bash
pip install markdown weasyprint pygments
```

These are automatically installed if you use the Copilot setup workflow.

## Customization

### CSS Styling

Create a custom CSS file to style your output:
```css
body {
    font-family: 'Georgia', serif;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

h1 { color: #2c3e50; }
h2 { color: #34495e; }

code {
    background: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
}
```

Then use:
```bash
python scripts/convert_markdown.py --style mystyle.css document.md
```

### PDF Options

The PDF generator supports:
- A4 page size (configurable)
- Page numbers
- Headers/footers
- Margins
- Links (clickable in PDF)

## Troubleshooting

**Error: "No module named 'markdown'"**
Run: `pip install markdown weasyprint pygments`

**Error: "WeasyPrint failed"**
- Install system dependencies: `brew install pango` (macOS) or `apt-get install libpango-1.0-0` (Linux)

**PDF links not working**
- Ensure you're using the latest weasyprint version
- Use absolute URLs for external links

**Images not showing**
- Use absolute paths for images
- Or place images relative to the .md file

## Script Location

The conversion script is located at: `scripts/convert_markdown.py`

## Integration with Git Workflows

You can automate conversions on commit:
```yaml
# .github/workflows/convert-docs.yml
name: Convert Documentation
on:
  push:
    paths:
      - 'docs/**/*.md'
jobs:
  convert:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install markdown weasyprint pygments
      - name: Convert docs
        run: python scripts/convert_markdown.py --all --dir docs/
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: converted-docs
          path: output/
```

## Tips

1. **Large files**: For documents >100 pages, PDF generation may take 10-30 seconds
2. **Math support**: Install `python-markdown-math` for LaTeX math rendering
3. **Mermaid diagrams**: Use `mermaid.js` in HTML or rasterize for PDF
4. **Performance**: Converting 10 files takes ~5-10 seconds

## Related Commands

- `/generate-toc` - Generate table of contents for Markdown
- `/validate-markdown` - Check Markdown syntax and links
- `/preview-html` - Quick HTML preview without saving
