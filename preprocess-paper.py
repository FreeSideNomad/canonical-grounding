#!/usr/bin/env python3
"""
Preprocess markdown for LaTeX PDF conversion.
- Remove manual numbering from section headers (LaTeX will auto-number)
- Replace special Unicode symbols with LaTeX equivalents
- Fix table formatting for 2-column layout
"""

import re
import sys

def preprocess_markdown(content):
    """Preprocess markdown content for LaTeX conversion."""

    # Convert long inline math formulas to display formulas for better 2-column rendering
    # Find inline math formulas longer than 45 characters and convert to display math
    import re

    # First, protect display math by temporarily replacing $$...$$ with placeholders
    display_math = []
    def save_display_math(match):
        display_math.append(match.group(0))
        return f'<<<DISPLAYMATH{len(display_math)-1}>>>'

    content = re.sub(r'\$\$.*?\$\$', save_display_math, content, flags=re.DOTALL)

    # Now convert long inline math (single $)
    def convert_long_inline_math(match):
        formula = match.group(1)
        # Only convert if it's a long formula (>45 chars for narrow 2-column)
        if len(formula) > 45:
            return '\n$$' + formula + '$$\n'
        else:
            return match.group(0)

    # Match single $ ... $ (not preceded or followed by another $)
    content = re.sub(r'(?<![\\$])\$([^$\n]+?)\$(?![\\$])', convert_long_inline_math, content)

    # Restore display math
    for i, dm in enumerate(display_math):
        content = content.replace(f'<<<DISPLAYMATH{i}>>>', dm)

    # Scale down long display math formulas to fit column width
    def scale_long_display_math(match):
        formula = match.group(1).strip()
        # Skip if already multi-line or has special environments
        if '\n' in formula or '\\\\' in formula or '\\begin' in formula:
            return match.group(0)

        # Scale based on length - only scale if it's actually long
        # Use proportional scaling to avoid making short formulas huge
        formula_len = len(formula)

        if formula_len > 100:
            # Very long: scale to 0.7 of column width
            return '$$\\resizebox{0.7\\columnwidth}{!}{$' + formula + '$}$$'
        elif formula_len > 80:
            # Long: scale to 0.8 of column width
            return '$$\\resizebox{0.8\\columnwidth}{!}{$' + formula + '$}$$'
        elif formula_len > 60:
            # Medium-long: scale to 0.9 of column width
            return '$$\\resizebox{0.9\\columnwidth}{!}{$' + formula + '$}$$'
        # Otherwise leave as-is (normal size)
        return match.group(0)

    content = re.sub(r'\$\$(.*?)\$\$', scale_long_display_math, content, flags=re.DOTALL)

    # Break long code lines at ~48 chars with spaces
    def break_long_code_lines(match):
        code = match.group(1)
        lines = code.split('\n')
        new_lines = []
        for line in lines:
            if len(line) > 48:
                # Break at spaces, keeping indentation
                indent = len(line) - len(line.lstrip())
                words = line.split(' ')
                current = ' ' * indent
                for word in words:
                    if len(current + ' ' + word) > 48 and current.strip():
                        new_lines.append(current.rstrip())
                        current = ' ' * (indent + 2) + word  # Extra indent for continuation
                    else:
                        current += (' ' if current.strip() else '') + word
                if current.strip():
                    new_lines.append(current)
            else:
                new_lines.append(line)
        return '```' + match.group(0).split('```')[0].split('\n')[0].replace('```', '') + '\n' + '\n'.join(new_lines) + '\n```'

    # Match code blocks
    content = re.sub(r'```[^\n]*\n(.*?)```', break_long_code_lines, content, flags=re.DOTALL)

    # Replace Unicode symbols with LaTeX equivalents
    symbol_replacements = {
        '✓': r'\checkmark',
        '✗': r'\times',
        '≥': r'$\geq$',
        '≤': r'$\leq$',
        '≈': r'$\approx$',
        '→': r'$\rightarrow$',
        '←': r'$\leftarrow$',
        '↔': r'$\leftrightarrow$',
        '∈': r'$\in$',
        '∉': r'$\notin$',
        '∀': r'$\forall$',
        '∃': r'$\exists$',
        '¬': r'$\neg$',
        '∧': r'$\wedge$',
        '∨': r'$\vee$',
        '⟹': r'$\implies$',
        '⟺': r'$\iff$',
        '⊇': r'$\supseteq$',
        '⊆': r'$\subseteq$',
        '×': r'$\times$',
        '∪': r'$\cup$',
        '∩': r'$\cap$',
        '⊕': r'$\oplus$',
        '∅': r'$\emptyset$',
        '⟨': r'$\langle$',
        '⟩': r'$\rangle$',
        '⋯': r'$\cdots$',
        '…': r'\ldots',
    }

    for symbol, latex in symbol_replacements.items():
        content = content.replace(symbol, latex)

    # Extract and preserve title metadata
    title_match = re.search(r'^#\s+(.+?)$', content, flags=re.MULTILINE)
    author_match = re.search(r'^\*\*Author:\*\*\s+(.+?)$', content, flags=re.MULTILINE)
    affiliation_match = re.search(r'^\*\*Affiliation:\*\*\s+(.+?)$', content, flags=re.MULTILINE)
    contact_match = re.search(r'^\*\*Contact:\*\*\s+(.+?)$', content, flags=re.MULTILINE)

    # Add YAML metadata block at the top if title found
    if title_match:
        yaml_block = "---\n"
        yaml_block += f'title: "{title_match.group(1)}"\n'
        if author_match:
            yaml_block += f'author: "{author_match.group(1)}"\n'
        if affiliation_match and contact_match:
            yaml_block += f'institute: "{affiliation_match.group(1)}"\n'
            yaml_block += f'email: "{contact_match.group(1)}"\n'
            # Add formatted author line
            yaml_block += f'date: ""\n'
        yaml_block += "---\n\n"

        # Remove the manual title, author, affiliation lines
        content = re.sub(r'^#\s+.+?$', '', content, count=1, flags=re.MULTILINE)
        content = re.sub(r'^\*\*Author:\*\*\s+.+?$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\*\*Affiliation:\*\*\s+.+?$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\*\*Contact:\*\*\s+.+?$', '', content, flags=re.MULTILINE)

        # Remove ALL horizontal rules (---) that separate sections
        # These confuse Pandoc's section numbering
        content = re.sub(r'^---+\s*$', '', content, flags=re.MULTILINE)

        # Prepend YAML block
        content = yaml_block + content.strip() + "\n"

    # Remove manual numbering from section headers
    # Pattern: ## 1. Introduction -> ## Introduction
    # Pattern: ### 1.1 Motivation -> ### Motivation
    # Pattern: #### 1.1.1 Background -> #### Background

    # Main sections (## 1. Title)
    content = re.sub(r'^(#{2,})\s+\d+\.\s+', r'\1 ', content, flags=re.MULTILINE)

    # Subsections (### 1.1 Title, ### 1.1.1 Title, etc.)
    content = re.sub(r'^(#{2,})\s+\d+\.\d+(\.\d+)*\s+', r'\1 ', content, flags=re.MULTILINE)

    # Mark Abstract, References, and Appendices as unnumbered sections
    content = re.sub(r'^##\s+Abstract\s*$', r'## Abstract {-}', content, flags=re.MULTILINE)

    # Force section counter to 0 right before Introduction so it becomes section 1
    content = re.sub(r'^##\s+Introduction\s*$', r'\\setcounter{section}{0}\n\n## Introduction', content, flags=re.MULTILINE)

    content = re.sub(r'^##\s+References\s*$', r'## References {-}', content, flags=re.MULTILINE)
    content = re.sub(r'^##\s+Appendices\s*$', r'## Appendices {-}', content, flags=re.MULTILINE)

    return content

def main():
    """Main preprocessing function."""

    if len(sys.argv) < 2:
        print("Usage: python3 preprocess-paper.py <input.md> [output.md]", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.md', '-processed.md')

    # Read input
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found", file=sys.stderr)
        sys.exit(1)

    # Preprocess
    processed_content = preprocess_markdown(content)

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(processed_content)

    print(f"✓ Preprocessed: {input_file} -> {output_file}")
    print(f"  Symbols replaced, section numbering removed")

if __name__ == '__main__':
    main()
