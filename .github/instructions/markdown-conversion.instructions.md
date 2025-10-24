---
applyTo:
  - "**/*.md"
  - "!node_modules/**"
  - "!.git/**"
---

# Markdown Conversion Instructions

These instructions apply when working with Markdown files in this repository.

## Conversion Capabilities

When a user asks to convert, export, or generate HTML/PDF from Markdown files:

1. **Use the conversion script**: `scripts/convert_markdown.py`
2. **Default output location**: `output/` directory
3. **Supported formats**: HTML (standalone), PDF (professional)

## Default Behavior

- Generate both HTML and PDF unless specified otherwise
- Include syntax highlighting for code blocks
- Preserve all links and images
- Apply repository's standard styling

## Quality Standards

When converting Markdown to HTML/PDF:

### HTML Output
- Generate standalone HTML (CSS embedded)
- Include meta tags for proper encoding
- Add syntax highlighting for code blocks
- Preserve document structure (headings, lists, tables)
- Make links clickable and styled

### PDF Output
- Use A4 page size
- Include page numbers in footer
- Preserve clickable links
- Apply proper margins (2cm all sides)
- Ensure code blocks don't break across pages
- Include document title in header

## File Naming Convention

For input file `document.md`:
- HTML output: `output/document.html`
- PDF output: `output/document.pdf`

## Special Handling

### Large Documents
- For files >50KB, warn user about processing time
- Suggest splitting if >500KB

### Images
- Embed images in HTML using base64 when <100KB
- Link to image files when >100KB
- For PDF, always embed images

### Code Blocks
- Apply syntax highlighting based on language tag
- If no language specified, use plain text formatting
- Preserve indentation and line breaks

### Tables
- Apply borders and cell padding
- Make tables responsive in HTML
- Ensure tables fit page width in PDF

## Common Use Cases

### Documentation Generation
When user says "generate docs" or "create documentation":
```bash
python scripts/convert_markdown.py --all --dir docs/ --format both
```

### Single File Quick Preview
When user says "preview" or "show me the HTML":
```bash
python scripts/convert_markdown.py --format html README.md
```

### Release-Ready PDF
When user says "create release PDF" or "publication-ready":
```bash
python scripts/convert_markdown.py --format pdf --toc domains/ddd/docs/ddd-guide.md
```

## Error Handling

### Missing Dependencies
If conversion fails, suggest:
```bash
pip install markdown weasyprint pygments
```

### WeasyPrint Installation Issues
On macOS:
```bash
brew install pango
```

On Ubuntu/Debian:
```bash
apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

## Integration Points

### With Git Workflow
- Suggest adding converted files to `.gitignore` if not already
- Recommend creating `output/` directory in project root
- For documentation, suggest automating conversion on push

### With Release Process
- When creating releases, recommend including PDF in release assets
- Suggest using `gh release create` with PDF attachment

## Best Practices

1. **Before Conversion**:
   - Validate Markdown syntax
   - Check all images exist and are accessible
   - Verify internal links point to valid sections

2. **After Conversion**:
   - Open HTML in browser to verify rendering
   - Check PDF page breaks are sensible
   - Verify all links are clickable
   - Confirm images are displaying

3. **Optimization**:
   - For batch conversions, use `--all` flag
   - For large repos, specify `--dir` to limit scope
   - Use `--format` to generate only needed format

## Example Conversations

**User**: "Convert the DDD guide to PDF"
**Assistant**: I'll convert domains/ddd/docs/ddd-guide.md to PDF using our conversion script:
```bash
python scripts/convert_markdown.py --format pdf domains/ddd/docs/ddd-guide.md
```

**User**: "Generate HTML for all markdown files in docs/"
**Assistant**: I'll batch convert all Markdown files in the docs directory:
```bash
python scripts/convert_markdown.py --all --dir docs/ --format html
```

**User**: "Create a styled PDF with table of contents"
**Assistant**: I'll generate a PDF with TOC and custom styling:
```bash
python scripts/convert_markdown.py --format pdf --toc --style custom.css your-file.md
```

## Troubleshooting Guide

### Issue: PDF generation fails
**Solution**: Check WeasyPrint dependencies, suggest system package installation

### Issue: Images not showing in PDF
**Solution**: Verify image paths are absolute or relative to .md file location

### Issue: Code blocks poorly formatted
**Solution**: Ensure language tag is specified in Markdown (```python, ```java, etc.)

### Issue: Conversion very slow
**Solution**: Large file detected, suggest running in background or splitting document

## Configuration Files

The conversion system uses:
- `scripts/convert_markdown.py` - Main conversion script
- `.github/prompts/convert-markdown.prompt.md` - User-facing documentation
- Default CSS embedded in script, custom CSS via `--style` flag

## Future Enhancements

Suggest to users if they need:
- Custom page headers/footers
- Different page sizes (Letter, Legal)
- Multi-column layouts
- Math formula rendering
- Mermaid diagram support
- Dark mode styling
