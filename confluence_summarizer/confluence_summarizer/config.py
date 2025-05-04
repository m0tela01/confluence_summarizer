"""Configuration for the Confluence summarizer."""

from typing import Optional
from pathlib import Path
import os
from dataclasses import dataclass

def load_secrets():
    """Load secrets from the secrets file if it exists."""
    secrets_path = Path("secrets")
    if secrets_path.exists():
        with open(secrets_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

# Load secrets from file if it exists
load_secrets()

@dataclass
class Config:
    """Configuration for the Confluence summarizer."""
    
    # Confluence settings
    confluence_url: str
    confluence_username: str
    confluence_api_token: str
    
    # Azure OpenAI settings
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_deployment_name: str
    azure_openai_api_version: str = "2024-02-15-preview"
    
    # Export settings
    export_dir: str = "summaries"
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create configuration from environment variables.
        
        Required environment variables:
        - CONFLUENCE_URL: The URL of your Confluence instance
        - CONFLUENCE_USERNAME: Your Confluence username
        - CONFLUENCE_API_TOKEN: Your Confluence API token
        - AZURE_OPENAI_API_KEY: Your Azure OpenAI API key
        - AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint
        - AZURE_OPENAI_DEPLOYMENT_NAME: Your Azure OpenAI deployment name
        
        Optional environment variables:
        - AZURE_OPENAI_API_VERSION: Azure OpenAI API version (default: 2024-02-15-preview)
        - EXPORT_DIR: Directory to export summaries to (default: summaries)
        
        Returns:
            Config object initialized from environment variables
            
        Raises:
            ValueError: If required environment variables are missing
        """
        # Check required environment variables
        required_vars = [
            'CONFLUENCE_URL',
            'CONFLUENCE_USERNAME',
            'CONFLUENCE_API_TOKEN',
            'AZURE_OPENAI_API_KEY',
            'AZURE_OPENAI_ENDPOINT',
            'AZURE_OPENAI_DEPLOYMENT_NAME'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                "Please create a 'secrets' file with these variables or set them in your environment."
            )
        
        return cls(
            confluence_url=os.getenv('CONFLUENCE_URL'),
            confluence_username=os.getenv('CONFLUENCE_USERNAME'),
            confluence_api_token=os.getenv('CONFLUENCE_API_TOKEN'),
            azure_openai_api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            azure_openai_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            azure_openai_deployment_name=os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME'),
            azure_openai_api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
            export_dir=os.getenv('EXPORT_DIR', 'summaries')
        )
    
    def validate(self) -> None:
        """Validate the configuration.
        
        Raises:
            ValueError: If the configuration is invalid
        """
        # Validate Confluence URL
        if not self.confluence_url.startswith(('http://', 'https://')):
            raise ValueError("Confluence URL must start with http:// or https://")
        
        # Validate Azure OpenAI endpoint
        if not self.azure_openai_endpoint.startswith(('http://', 'https://')):
            raise ValueError("Azure OpenAI endpoint must start with http:// or https://")
        
        # Validate export directory
        export_path = Path(self.export_dir)
        if export_path.exists() and not export_path.is_dir():
            raise ValueError(f"Export directory {self.export_dir} exists but is not a directory") 