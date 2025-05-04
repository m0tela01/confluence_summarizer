# Confluence Summarizer

A command-line tool for generating summaries of Confluence content using Azure OpenAI.

## Features

- Generate summaries of Confluence spaces and pages
- Support for different summarization personas (technical, business, project, user)
- Export summaries to markdown files
- Compare summaries and visualize differences
- Rich console output with tables and syntax highlighting

## Installation

```bash
pip install confluence-summarizer
```

## Configuration

The tool requires the following environment variables:

```bash
# Confluence settings
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_API_TOKEN=your-api-token

# Azure OpenAI settings
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name

# Optional settings
AZURE_OPENAI_API_VERSION=2024-02-15-preview  # Default
EXPORT_DIR=summaries  # Default
```

## Usage

### Generate a Summary

```bash
# Summarize a space
confluence-summarizer summarize SPACE_KEY

# Summarize a specific page
confluence-summarizer summarize SPACE_KEY --page-id PAGE_ID

# Include child pages
confluence-summarizer summarize SPACE_KEY --include-children

# Use a different persona
confluence-summarizer summarize SPACE_KEY --persona business

# Add context
confluence-summarizer summarize SPACE_KEY --context "Focus on implementation details"

# Disable export
confluence-summarizer summarize SPACE_KEY --no-export

# Specify export directory
confluence-summarizer summarize SPACE_KEY --export-dir custom/summaries
```

### Compare Summaries

```bash
# Compare two summary files
confluence-summarizer compare summary1.md summary2.md
```

### List Personas

```bash
# List available personas
confluence-summarizer list-personas
```

## Output Format

Summaries are exported as markdown files with the following structure:

```markdown
# Page Title

## Metadata
- Author: username
- Date: YYYY-MM-DD HH:MM:SS

## Summary
[Generated summary content]

## Comparison Statistics
[If comparing with previous summary]

## Changes from Previous Summary
[If comparing with previous summary]

---
*Generated on: YYYY-MM-DD HH:MM:SS*
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/confluence-summarizer.git
cd confluence-summarizer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Run tests:
```bash
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 