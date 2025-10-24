#!/usr/bin/env python3
"""
Markdown to HTML and PDF Converter

Converts Markdown documents to professionally styled HTML and PDF formats.

Usage:
    python convert_markdown.py [options] <file.md>
    python convert_markdown.py --all --dir docs/

Dependencies:
    pip install markdown weasyprint pygments
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


DEFAULT_CSS = """
/* Professional Document Styling */
@page {
    size: A4;
    margin: 2cm;
    @bottom-right {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 9pt;
        color: #666;
    }
}

body {
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #333;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    color: #2c3e50;
    font-size: 28pt;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
    margin-top: 0;
    margin-bottom: 20px;
    page-break-after: avoid;
}

h2 {
    color: #34495e;
    font-size: 22pt;
    border-bottom: 2px solid #95a5a6;
    padding-bottom: 8px;
    margin-top: 30px;
    margin-bottom: 15px;
    page-break-after: avoid;
}

h3 {
    color: #34495e;
    font-size: 18pt;
    margin-top: 25px;
    margin-bottom: 12px;
    page-break-after: avoid;
}

h4 {
    color: #555;
    font-size: 14pt;
    margin-top: 20px;
    margin-bottom: 10px;
    page-break-after: avoid;
}

h5, h6 {
    color: #666;
    font-size: 12pt;
    margin-top: 15px;
    margin-bottom: 8px;
}

p {
    margin-bottom: 12px;
    text-align: justify;
    orphans: 3;
    widows: 3;
}

a {
    color: #3498db;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

code {
    background-color: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: 'Monaco', 'Courier New', monospace;
    font-size: 10pt;
    color: #c7254e;
}

pre {
    background-color: #f8f8f8;
    border: 1px solid #ddd;
    border-left: 4px solid #3498db;
    padding: 15px;
    overflow-x: auto;
    border-radius: 4px;
    margin: 15px 0;
    page-break-inside: avoid;
}

pre code {
    background-color: transparent;
    padding: 0;
    color: #333;
    font-size: 9pt;
    line-height: 1.4;
}

blockquote {
    border-left: 4px solid #3498db;
    padding-left: 20px;
    margin-left: 0;
    color: #555;
    font-style: italic;
    background-color: #f9f9f9;
    padding: 10px 20px;
    margin: 15px 0;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
    page-break-inside: avoid;
}

th, td {
    border: 1px solid #ddd;
    padding: 12px;
    text-align: left;
}

th {
    background-color: #3498db;
    color: white;
    font-weight: bold;
}

tr:nth-child(even) {
    background-color: #f2f2f2;
}

ul, ol {
    margin: 12px 0;
    padding-left: 30px;
}

li {
    margin-bottom: 6px;
}

img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 20px auto;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

hr {
    border: none;
    border-top: 2px solid #e0e0e0;
    margin: 30px 0;
}

.toc {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 20px;
    margin: 30px 0;
    page-break-inside: avoid;
}

.toc h2 {
    margin-top: 0;
    border-bottom: none;
}

.toc ul {
    list-style-type: none;
    padding-left: 0;
}

.toc li {
    margin-bottom: 8px;
}

.toc a {
    color: #2c3e50;
}

/* Syntax highlighting for code blocks */
.codehilite {
    background: #f8f8f8;
    border-radius: 4px;
}

.codehilite .hll { background-color: #ffffcc }
.codehilite .c { color: #408080; font-style: italic } /* Comment */
.codehilite .k { color: #008000; font-weight: bold } /* Keyword */
.codehilite .o { color: #666666 } /* Operator */
.codehilite .cm { color: #408080; font-style: italic } /* Comment.Multiline */
.codehilite .s { color: #BA2121 } /* String */
.codehilite .na { color: #7D9029 } /* Name.Attribute */
.codehilite .nb { color: #008000 } /* Name.Builtin */
.codehilite .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.codehilite .nf { color: #0000FF } /* Name.Function */

/* Print-specific styles */
@media print {
    body {
        font-size: 10pt;
    }

    a {
        color: #000;
        text-decoration: underline;
    }

    pre, blockquote {
        page-break-inside: avoid;
    }
}
"""


class MarkdownConverter:
    """Convert Markdown files to HTML and PDF formats."""

    def __init__(self, custom_css: Optional[str] = None):
        """Initialize converter with optional custom CSS."""
        self.custom_css = custom_css or DEFAULT_CSS
        self.md = markdown.Markdown(
            extensions=[
                'extra',           # Tables, fenced code blocks
                'codehilite',      # Syntax highlighting
                'toc',             # Table of contents
                'nl2br',           # Newline to <br>
                'sane_lists',      # Better list handling
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'codehilite',
                    'linenums': False,
                },
                'toc': {
                    'permalink': True,
                    'toc_depth': 6,
                }
            }
        )

    def convert_to_html(
        self,
        md_file: Path,
        output_file: Path,
        include_toc: bool = False
    ) -> bool:
        """
        Convert Markdown to standalone HTML.

        Args:
            md_file: Input Markdown file path
            output_file: Output HTML file path
            include_toc: Whether to include table of contents

        Returns:
            True if successful, False otherwise
        """
        try:
            # Read Markdown content
            md_content = md_file.read_text(encoding='utf-8')

            # Convert to HTML
            html_content = self.md.convert(md_content)

            # Get TOC if requested
            toc_html = ""
            if include_toc and hasattr(self.md, 'toc'):
                toc_html = f"""
                <div class="toc">
                    <h2>Table of Contents</h2>
                    {self.md.toc}
                </div>
                """

            # Create full HTML document
            full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{md_file.stem}</title>
    <style>
{self.custom_css}
    </style>
</head>
<body>
{toc_html}
{html_content}
</body>
</html>
"""

            # Write HTML file
            output_file.write_text(full_html, encoding='utf-8')
            print(f"✓ HTML generated: {output_file}")

            # Reset markdown processor for next file
            self.md.reset()

            return True

        except Exception as e:
            print(f"✗ Error converting {md_file} to HTML: {e}", file=sys.stderr)
            return False

    def convert_to_pdf(
        self,
        md_file: Path,
        output_file: Path,
        include_toc: bool = False
    ) -> bool:
        """
        Convert Markdown to PDF via HTML.

        Args:
            md_file: Input Markdown file path
            output_file: Output PDF file path
            include_toc: Whether to include table of contents

        Returns:
            True if successful, False otherwise
        """
        try:
            # First convert to HTML (in memory)
            md_content = md_file.read_text(encoding='utf-8')
            html_content = self.md.convert(md_content)

            # Get TOC if requested
            toc_html = ""
            if include_toc and hasattr(self.md, 'toc'):
                toc_html = f"""
                <div class="toc">
                    <h2>Table of Contents</h2>
                    {self.md.toc}
                </div>
                """

            # Create HTML string
            html_string = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{md_file.stem}</title>
</head>
<body>
{toc_html}
{html_content}
</body>
</html>
"""

            # Convert HTML to PDF using WeasyPrint
            font_config = FontConfiguration()
            html_doc = HTML(string=html_string, base_url=str(md_file.parent))
            css = CSS(string=self.custom_css, font_config=font_config)

            html_doc.write_pdf(
                output_file,
                stylesheets=[css],
                font_config=font_config
            )

            print(f"✓ PDF generated: {output_file}")

            # Reset markdown processor
            self.md.reset()

            return True

        except Exception as e:
            print(f"✗ Error converting {md_file} to PDF: {e}", file=sys.stderr)
            return False

    def convert_file(
        self,
        md_file: Path,
        output_dir: Path,
        format: str = 'both',
        include_toc: bool = False
    ) -> tuple[bool, bool]:
        """
        Convert a single Markdown file to specified format(s).

        Args:
            md_file: Input Markdown file
            output_dir: Output directory
            format: 'html', 'pdf', or 'both'
            include_toc: Include table of contents

        Returns:
            Tuple of (html_success, pdf_success)
        """
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate output paths
        html_output = output_dir / f"{md_file.stem}.html"
        pdf_output = output_dir / f"{md_file.stem}.pdf"

        html_success = True
        pdf_success = True

        # Convert based on format
        if format in ('html', 'both'):
            html_success = self.convert_to_html(md_file, html_output, include_toc)

        if format in ('pdf', 'both'):
            pdf_success = self.convert_to_pdf(md_file, pdf_output, include_toc)

        return html_success, pdf_success

    def convert_directory(
        self,
        input_dir: Path,
        output_dir: Path,
        format: str = 'both',
        include_toc: bool = False
    ) -> tuple[int, int, int]:
        """
        Convert all Markdown files in a directory.

        Args:
            input_dir: Directory containing .md files
            output_dir: Output directory
            format: 'html', 'pdf', or 'both'
            include_toc: Include table of contents

        Returns:
            Tuple of (total_files, successful, failed)
        """
        md_files = list(input_dir.glob('**/*.md'))

        if not md_files:
            print(f"No Markdown files found in {input_dir}")
            return 0, 0, 0

        print(f"Found {len(md_files)} Markdown file(s) to convert...")

        successful = 0
        failed = 0

        for md_file in md_files:
            print(f"\nConverting: {md_file.name}")
            html_ok, pdf_ok = self.convert_file(md_file, output_dir, format, include_toc)

            if (format == 'html' and html_ok) or \
               (format == 'pdf' and pdf_ok) or \
               (format == 'both' and html_ok and pdf_ok):
                successful += 1
            else:
                failed += 1

        return len(md_files), successful, failed


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to HTML and PDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert single file to both formats
  python convert_markdown.py document.md

  # Convert to PDF only
  python convert_markdown.py --format pdf document.md

  # Batch convert all files in directory
  python convert_markdown.py --all --dir docs/

  # Use custom CSS
  python convert_markdown.py --style custom.css document.md

  # Include table of contents
  python convert_markdown.py --toc document.md
        """
    )

    parser.add_argument(
        'input_file',
        nargs='?',
        type=Path,
        help='Input Markdown file (required unless using --all)'
    )

    parser.add_argument(
        '--format',
        choices=['html', 'pdf', 'both'],
        default='both',
        help='Output format (default: both)'
    )

    parser.add_argument(
        '--output',
        type=Path,
        default=Path('output'),
        help='Output directory (default: output/)'
    )

    parser.add_argument(
        '--style',
        type=Path,
        help='Custom CSS file for styling'
    )

    parser.add_argument(
        '--toc',
        action='store_true',
        help='Include table of contents'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Convert all .md files in directory'
    )

    parser.add_argument(
        '--dir',
        type=Path,
        help='Directory to scan for .md files (requires --all)'
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.all and not args.input_file:
        parser.error('Input file required unless using --all')

    if args.all and not args.dir:
        parser.error('--dir required when using --all')

    # Load custom CSS if provided
    custom_css = None
    if args.style:
        if not args.style.exists():
            print(f"Error: CSS file not found: {args.style}", file=sys.stderr)
            return 1
        custom_css = args.style.read_text(encoding='utf-8')

    # Create converter
    converter = MarkdownConverter(custom_css)

    # Convert files
    if args.all:
        total, successful, failed = converter.convert_directory(
            args.dir,
            args.output,
            args.format,
            args.toc
        )

        print(f"\n{'='*60}")
        print(f"Conversion complete!")
        print(f"Total files: {total}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Output directory: {args.output.absolute()}")

        return 0 if failed == 0 else 1

    else:
        if not args.input_file.exists():
            print(f"Error: File not found: {args.input_file}", file=sys.stderr)
            return 1

        html_ok, pdf_ok = converter.convert_file(
            args.input_file,
            args.output,
            args.format,
            args.toc
        )

        success = (args.format == 'html' and html_ok) or \
                  (args.format == 'pdf' and pdf_ok) or \
                  (args.format == 'both' and html_ok and pdf_ok)

        if success:
            print(f"\n✓ Conversion complete! Output: {args.output.absolute()}")
            return 0
        else:
            print(f"\n✗ Conversion failed", file=sys.stderr)
            return 1


if __name__ == '__main__':
    sys.exit(main())
