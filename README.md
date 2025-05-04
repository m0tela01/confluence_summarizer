# Confluence Summarizer

A CLI tool for summarizing Confluence documentation using Azure OpenAI and LangChain. This tool allows you to summarize Confluence pages or entire spaces using different personas and additional context to guide the summarization.

## Features

- Summarize individual Confluence pages or entire spaces
- Multiple summarization personas (Technical, Business, Simplified)
- Azure OpenAI integration using Default Azure Credentials
- HTML content cleaning and processing
- Support for tables and images in content
- Additional context parameter for guided summarization
- Caching support for improved performance

## Installation

```bash
pip install confluence-summarizer
```

## Configuration

### Using Secrets File (Recommended)

Create a `secrets` file in your project root with the following variables:

```bash
# Confluence Configuration
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_USERNAME=your-email@example.com
CONFLUENCE_API_TOKEN=your-api-token
CONFLUENCE_SPACE_KEY=TEAM

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com

# Optional Configuration
AZURE_OPENAI_API_VERSION=2024-02-15-preview  # Default
EXPORT_DIR=summaries  # Default
```

Note: Make sure to add `secrets` to your `.gitignore` file to prevent accidentally committing sensitive information.

### Environment Variables

Alternatively, you can set the following environment variables:

```bash
# Confluence settings
export CONFLUENCE_URL="https://your-domain.atlassian.net"
export CONFLUENCE_USERNAME="your-email@example.com"
export CONFLUENCE_API_TOKEN="your-api-token"

# Azure OpenAI settings
export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com"
export AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment-name"
export AZURE_OPENAI_API_VERSION="2024-02-15-preview"  # Optional, defaults to latest
```

## Usage

### Basic Usage

Summarize a specific page:
```bash
confluence-summarizer summarize SPACE_KEY PAGE_ID
```

Summarize an entire space:
```bash
confluence-summarizer summarize SPACE_KEY
```

### Advanced Usage

Summarize with a specific persona:
```bash
confluence-summarizer summarize SPACE_KEY --persona technical
```

Include child pages when summarizing:
```bash
confluence-summarizer summarize SPACE_KEY PAGE_ID --include-children
```

Summarize with additional context:
```bash
# Focus on technical implementation details
confluence-summarizer summarize SPACE_KEY --context "Focus on technical implementation details"
```

## Getting Help

For detailed help and examples:
```bash
confluence-summarizer help
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Available Personas

- `technical`: Detailed technical summaries with code examples and implementation details
- `business`: High-level summaries focusing on business value and impact
- `simplified`: Easy-to-understand summaries with minimal technical jargon

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT License
