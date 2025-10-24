# Stylesheet Comparison

This document compares the two built-in stylesheets available in the Markdown converter.

## Overview

The Markdown converter includes two professional built-in stylesheets, each optimized for different use cases.

| Feature | Classic | Modern |
|---------|---------|--------|
| **Font Family** | Georgia, Times New Roman (serif) | Helvetica Neue, Helvetica, Segoe UI (sans-serif) |
| **Base Font Size** | 11pt | 16px |
| **H1 Size** | 28pt | 2.25em (36px) |
| **H1 Weight** | 600 | 300 |
| **H2 Size** | 22pt | 1.75em (28px) |
| **H2 Weight** | 600 | 400 |
| **Design** | Traditional, academic | Contemporary, web-native |
| **Best For** | Printed documents, books, formal reports | Online docs, presentations, technical guides |
| **PDF Size (DDD Guide)** | 999KB | 916KB |

## Visual Differences

### Classic Style

**Characteristics:**
- Serif typography for better readability in print
- Traditional heading hierarchy with consistent weights (600)
- Blue accent borders on H1/H2 headings (#3498db)
- Code blocks with blue left border accent
- Elegant, formal appearance

**When to Use:**
- ✅ Academic papers
- ✅ Books and long-form documentation
- ✅ Formal business reports
- ✅ Print publications
- ✅ Documents requiring traditional appearance

**Sample Code:**
```bash
./scripts/convert_markdown.sh --style classic --format pdf document.md
```

### Modern Style

**Characteristics:**
- Sans-serif typography for screen readability
- Progressive heading weights (300 → 600 from H1 to H6)
- Clean, minimal design without heavy borders
- Light gray backgrounds for code (#f0f0f0)
- Contemporary, tech-forward aesthetic

**When to Use:**
- ✅ Technical documentation
- ✅ API documentation
- ✅ Modern web content
- ✅ Presentations and slides
- ✅ Developer guides
- ✅ Screen-first reading experiences

**Sample Code:**
```bash
./scripts/convert_markdown.sh --style modern --format pdf document.md
```

## Detailed Comparison

### Typography

#### Classic
```
Body: Georgia 11pt
H1: Georgia 28pt, weight 600, border-bottom 3px solid #3498db
H2: Georgia 22pt, weight 600, border-bottom 2px solid #95a5a6
H3: Georgia 18pt, weight 600
Code: Monaco 10pt, #c7254e on #f4f4f4
```

#### Modern
```
Body: Helvetica Neue 16px
H1: Helvetica Neue 2.25em (36px), weight 300
H2: Helvetica Neue 1.75em (28px), weight 400
H3: Helvetica Neue 1.5em (24px), weight 500
Code: Menlo 0.85em, #000 on #f0f0f0
```

### Code Blocks

#### Classic
- Background: #f8f8f8
- Border: 1px solid #ddd + 4px left border #3498db
- Code color: Syntax-highlighted via Pygments
- Accent: Blue left border creates visual hierarchy

#### Modern
- Background: #f5f5f5
- Border: 1px solid #d6d6d6
- Code color: Syntax-highlighted via Pygments
- Accent: Minimal, clean borders

### Tables

#### Classic
- Header: #3498db background, white text
- Borders: #ddd
- Zebra striping: Even rows #f2f2f2

#### Modern
- Header: Bold (#000), no background color
- Borders: #d6d6d6
- Zebra striping: Even rows #f2f2f2

### Blockquotes

#### Classic
- Border: 4px left, #3498db
- Background: #f9f9f9
- Text: #555

#### Modern
- Border: 4px left, #d6d6d6
- Background: #f0f0f0
- Text: #5c5c5c

## File Size Impact

Based on conversion of the DDD Guide (10,234 lines, 39,904 words):

- **Classic**: 999KB
- **Modern**: 916KB (8.3% smaller)

The modern style produces slightly smaller PDFs due to:
- Sans-serif fonts have simpler glyph shapes
- Less border styling and decorative elements
- More efficient font embedding

## Performance

Both stylesheets have equivalent conversion times:
- Small docs (<5,000 words): <1 second
- Medium docs (5,000-20,000 words): 2-5 seconds
- Large docs (20,000-50,000 words): 5-15 seconds

Font rendering performance is nearly identical.

## Accessibility

### Classic
- High contrast text (serif improves readability in print)
- Traditional hierarchy familiar to academic readers
- Excellent for printed documents

### Modern
- High contrast text (sans-serif improves screen readability)
- Progressive weight hierarchy guides visual scanning
- Optimized for digital consumption

## Recommendations

### Choose Classic When:
1. Primary distribution is **print**
2. Audience expects **traditional formatting**
3. Document is **academic or formal**
4. Content is **long-form** (books, guides >100 pages)
5. Need **maximum readability in print**

### Choose Modern When:
1. Primary distribution is **digital/screen**
2. Audience is **technical or design-focused**
3. Document is **contemporary or technical**
4. Content includes **code-heavy documentation**
5. Need **web-native appearance**
6. Want **smaller file sizes**

## Custom Styling

Both stylesheets can be used as templates for custom designs:

1. Export the built-in stylesheet:
```bash
# Classic
cat scripts/convert_markdown.py | grep -A 200 "^DEFAULT_CSS" > my-classic.css

# Modern
cp scripts/styles/modern.css my-modern.css
```

2. Modify the CSS to match your brand
3. Use with `--style`:
```bash
./scripts/convert_markdown.sh --style my-custom.css document.md
```

## Examples

### Generate Both Styles
```bash
# Classic version
./scripts/convert_markdown.sh --style classic --format pdf document.md
mv output/document.pdf output/document-classic.pdf

# Modern version
./scripts/convert_markdown.sh --style modern --format pdf document.md
mv output/document.pdf output/document-modern.pdf
```

### Sample Documents

See `output/` directory for examples:
- `ddd-guide-classic.pdf` - Classic serif style
- `ddd-guide-modern.pdf` - Modern sans-serif style

## Conclusion

Both stylesheets produce professional, high-quality output. Your choice depends on:

- **Audience**: Academic vs. Technical
- **Medium**: Print vs. Screen
- **Content**: Formal vs. Contemporary
- **Distribution**: Physical vs. Digital

When in doubt:
- Use **classic** for formal, print-first documents
- Use **modern** for technical, screen-first documents
