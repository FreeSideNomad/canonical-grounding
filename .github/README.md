# GitHub Copilot Configuration

This directory contains GitHub Copilot customizations for the canonical-grounding project.

## Directory Structure

```
.github/
├── copilot-instructions.md       # Repository-wide instructions
├── prompts/                       # Slash commands for Copilot Chat
│   └── convert-markdown.prompt.md
├── instructions/                  # Path-specific instructions
│   └── markdown-conversion.instructions.md
└── workflows/                     # GitHub Actions workflows
    └── copilot-setup-steps.yml
```

## Available Copilot Skills

### 1. Markdown Conversion (`/convert-markdown`)

Convert Markdown files to HTML and PDF formats.

**Usage in Copilot Chat:**
```
@workspace /convert-markdown domains/ddd/docs/ddd-guide.md
@workspace /convert-markdown --all --dir docs/
```

**Features:**
- Professional HTML output with embedded CSS
- High-quality PDF generation with proper formatting
- Syntax highlighting for code blocks
- Table of contents generation
- Custom CSS styling support
- Batch conversion of directories

**Files:**
- Prompt: `.github/prompts/convert-markdown.prompt.md`
- Instructions: `.github/instructions/markdown-conversion.instructions.md`
- Script: `scripts/convert_markdown.py`
- Wrapper: `scripts/convert_markdown.sh`

### 2. Repository-Wide Instructions

**File:** `.github/copilot-instructions.md`

Applies to all Copilot interactions in this repository. Includes:
- Project context and structure
- Code style conventions
- Documentation standards
- Common tasks and workflows
- Best practices

## How to Use

### In VS Code with Copilot

1. **Slash Commands:**
   - Type `/` in Copilot Chat to see available commands
   - Use `/convert-markdown` for document conversion

2. **Auto-Applied Instructions:**
   - When editing `.md` files, markdown conversion instructions apply automatically
   - Repository-wide instructions always apply

3. **Context Awareness:**
   - Copilot automatically understands project structure
   - Knows about schemas, documentation, and tools

### From Command Line

```bash
# Convert Markdown files
./scripts/convert_markdown.sh <file.md>

# See all options
./scripts/convert_markdown.sh --help
```

## Setup for Copilot Coding Agent

The Copilot coding agent uses `.github/workflows/copilot-setup-steps.yml` to configure its environment.

When the agent starts, it:
1. Sets up Python 3.11
2. Installs system dependencies (pango, etc.)
3. Installs Python packages (markdown, weasyprint, pygments)
4. Verifies the conversion script works

## Custom Instructions

### Adding New Instructions

**Path-Specific Instructions:**
Create `.github/instructions/<name>.instructions.md`:

```markdown
---
applyTo:
  - "**/*.py"
  - "!tests/**"
---

# Python File Instructions

When working with Python files...
```

**New Slash Commands:**
Create `.github/prompts/<command>.prompt.md`:

```markdown
---
description: Brief description of what this does
tags: [tag1, tag2]
---

# Command Name

What this command does...

## Usage
...
```

### Updating Repository Instructions

Edit `.github/copilot-instructions.md` to change repository-wide behavior.

## Examples

### Converting Documentation

**In Copilot Chat:**
```
@workspace I need to convert the DDD guide to PDF with a table of contents
```

**Result:** Copilot will use the `/convert-markdown` skill to:
```bash
./scripts/convert_markdown.sh --format pdf --toc domains/ddd/docs/ddd-guide.md
```

### Batch Conversion

**In Copilot Chat:**
```
@workspace Convert all markdown files in the docs directory to both HTML and PDF
```

**Result:**
```bash
./scripts/convert_markdown.sh --all --dir docs/ --format both
```

### Custom Styling

**In Copilot Chat:**
```
@workspace Convert README to PDF using the custom.css stylesheet
```

**Result:**
```bash
./scripts/convert_markdown.sh --format pdf --style custom.css README.md
```

## Dependencies

### Python Packages
- `markdown` - Markdown to HTML conversion
- `weasyprint` - HTML to PDF rendering
- `pygments` - Syntax highlighting

### System Packages
- **macOS:** `pango` (via Homebrew)
- **Linux:** `libpango-1.0-0`, `libharfbuzz0b`, `libpangoft2-1.0-0`

All dependencies are automatically installed by the shell wrapper.

## Troubleshooting

### Copilot Not Seeing Instructions

1. Restart VS Code
2. Check file names match expected patterns
3. Verify YAML frontmatter is correct

### Conversion Script Fails

1. Check virtual environment exists: `ls venv/`
2. Manually run setup: `./scripts/convert_markdown.sh --help`
3. Check system dependencies are installed

### Slash Command Not Working

1. Check `.github/prompts/` directory exists
2. Verify `.prompt.md` file has proper frontmatter
3. Restart Copilot Chat window

## Best Practices

### Writing Instructions

1. **Be Specific:** Clear, actionable instructions work best
2. **Use Examples:** Show Copilot what you want
3. **Test Incrementally:** Add instructions gradually and test
4. **Keep Organized:** Group related instructions together

### Using Slash Commands

1. **Descriptive Names:** Use clear, searchable command names
2. **Rich Documentation:** Include usage examples and options
3. **Error Handling:** Document common issues and solutions

### Repository Instructions

1. **Project Context:** Help Copilot understand your project
2. **Conventions:** Document code style and patterns
3. **Common Tasks:** Make frequent operations easy to discover

## Integration with GitHub Actions

The conversion tool can be used in CI/CD:

```yaml
name: Generate Documentation
on: [push]

jobs:
  convert:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Convert docs
        run: ./scripts/convert_markdown.sh --all --dir docs/
      - name: Upload
        uses: actions/upload-artifact@v4
        with:
          name: docs
          path: output/
```

## Resources

- [GitHub Copilot Docs](https://docs.github.com/copilot)
- [Custom Instructions](https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
- [Building Copilot Skillsets](https://docs.github.com/copilot/building-copilot-extensions/building-a-copilot-skillset-for-your-copilot-extension)
- [Copilot Setup Steps](https://docs.github.com/copilot/customizing-copilot/configuring-github-copilot-in-your-environment)

## Contributing

To add new Copilot skills:

1. Create prompt file in `.github/prompts/`
2. Add instructions in `.github/instructions/` if needed
3. Update this README
4. Test with Copilot Chat
5. Commit and push

## Version

Copilot configuration version: 1.0.0
Compatible with: GitHub Copilot (2025+)
