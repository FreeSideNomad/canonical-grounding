# Repository-Wide Copilot Instructions

This repository contains Domain-Driven Design (DDD) schemas, documentation, and analysis tools.

## Project Context

- **Primary Language**: YAML schemas, Markdown documentation, Python scripts
- **Purpose**: Canonical grounding framework for DDD concepts with machine-readable schemas
- **Version**: 2.0.0 (with root objects, flat structure, ID type extraction)

## Code Style and Conventions

### YAML Schemas
- Use `lower_snake_case` for all IDs
- ID prefixes: `sys_`, `dom_`, `bc_`, `agg_`, `ent_`, `vo_`, etc.
- Root objects: `System`, `BoundedContext`, `DomainStory`
- Always include `description` fields for clarity
- Version all schemas using semantic versioning

### Markdown Documentation
- Use ATX-style headers (`#`, `##`, `###`)
- Code blocks must have language tags
- Target 6-8 sentences per paragraph
- Use Title Case for DDD pattern names (Domain Event, Bounded Context)
- Use lowercase for generic usage (when a domain event occurs)
- Code examples use `// Good:` and `// Bad:` notation

### Python Scripts
- Follow PEP 8 style guide
- Use type hints for function signatures
- Include docstrings for all public functions
- Use pathlib for file operations
- Handle errors gracefully with informative messages

## Available Tools

### Markdown Conversion
Use `/convert-markdown` slash command or run:
```bash
python scripts/convert_markdown.py [options] <file.md>
```

Options:
- `--format html|pdf|both` - Output format
- `--output <dir>` - Output directory
- `--toc` - Include table of contents
- `--all --dir <path>` - Batch convert directory

### Dependencies
- markdown
- weasyprint
- pygments

## Project Structure

```
.
├── domains/
│   └── ddd/
│       ├── strategic-ddd-schema.yaml
│       ├── tactical-ddd-schema.yaml
│       ├── domain-stories-schema.yaml
│       └── docs/
│           └── ddd-guide.md
├── scripts/
│   └── convert_markdown.py
├── output/
│   └── (generated HTML/PDF files)
├── .github/
│   ├── copilot-instructions.md
│   ├── prompts/
│   │   └── convert-markdown.prompt.md
│   ├── instructions/
│   │   └── markdown-conversion.instructions.md
│   └── workflows/
│       └── copilot-setup-steps.yml
└── analysis-outputs/
    └── (critique reports, plans)
```

## Documentation Standards

When creating or editing documentation:

1. **Readability First**:
   - Break long paragraphs (max 8 sentences)
   - Add transitions between sections
   - Use visual hierarchy (headings, lists, code blocks)

2. **Consistency**:
   - Follow established terminology conventions
   - Use consistent code notation (Good/Bad)
   - Maintain heading hierarchy (no skipping levels)

3. **Quality**:
   - Include examples for complex concepts
   - Add table of contents for long documents
   - Verify all links and cross-references

## Common Tasks

### Generate Documentation PDF
```bash
python scripts/convert_markdown.py --format pdf --toc domains/ddd/docs/ddd-guide.md
```

### Validate Schema
```bash
python tools/validate-v2.py domains/ddd/strategic-ddd-schema.yaml
```

### Create Release
```bash
git tag -a v2.0.0 -m "Release notes"
git push origin v2.0.0
gh release create v2.0.0 output/ddd-guide.pdf --title "Release v2.0.0"
```

## Best Practices

### When Working with Schemas
- Validate against JSON Schema Draft 2020-12
- Test schema changes with actual YAML documents
- Update documentation when schema changes
- Version bump appropriately (SemVer)

### When Writing Documentation
- Use e-commerce examples (Order, Customer, Product) for consistency
- Include code examples with syntax highlighting
- Add "What's Next" transitions between major sections
- Generate both HTML and PDF for distribution

### When Converting Markdown
- Always include table of contents for documents >20 pages
- Use custom CSS for branded documents
- Verify images are properly embedded
- Check PDF page breaks for readability

## Error Handling

If conversion fails:
1. Check dependencies are installed
2. Verify system packages (libpango, etc.)
3. Check image paths are valid
4. Ensure Markdown syntax is correct

## Git Workflow

- Main branch: `main`
- Feature branches: `feature/<name>`
- Releases: SemVer tags (v2.0.0)
- Commit messages: Descriptive with context

## Quality Metrics

Target quality levels:
- Documentation readability: 9/10
- Schema completeness: 100%
- Test coverage: >80%
- Link validity: 100%

## Support and Resources

- DDD Guide: `domains/ddd/docs/ddd-guide.md`
- Schema Reference: Section 9 of DDD Guide
- Conversion Help: `.github/prompts/convert-markdown.prompt.md`
- Critique Framework: `analysis-outputs/ddd-guide-comprehensive-critique.md`
