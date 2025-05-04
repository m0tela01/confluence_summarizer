"""
Example usage of the Confluence Summarizer tool.

This script demonstrates various ways to use the Confluence Summarizer to generate
and compare summaries of Confluence content.
"""

import os
import time
from pathlib import Path
from datetime import datetime

from confluence_summarizer.agent.summarizer import ConfluenceSummarizerAgent
from confluence_summarizer.config import Config

def setup_environment():
    """Set up environment variables for the examples."""
    os.environ["AZURE_OPENAI_API_KEY"] = "your-api-key"
    os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "your-deployment-name"
    os.environ["AZURE_OPENAI_ENDPOINT"] = "your-endpoint-url"
    os.environ["CONFLUENCE_URL"] = "https://your-domain.atlassian.net"
    os.environ["CONFLUENCE_USERNAME"] = "your-email@example.com"
    os.environ["CONFLUENCE_API_TOKEN"] = "your-api-token"
    os.environ["CONFLUENCE_SPACE_KEY"] = "TEAM"

def example_1_basic_summary(agent):
    """Generate a basic summary of a Confluence page."""
    print("\n=== Example 1: Basic Summary Generation ===")
    
    result = agent.run(
        page_id="123456",
        include_children=True
    )
    
    print("Summary:")
    print(result['summary'])
    print("\nMetadata:")
    for key, value in result['metadata'].items():
        print(f"{key}: {value}")

def example_2_technical_summary(agent):
    """Generate a technical-focused summary with context."""
    print("\n=== Example 2: Technical Summary with Context ===")
    
    result = agent.run(
        page_id="123456",
        persona="technical",
        context="Focus on implementation details, technical architecture, and code examples",
        include_children=True
    )
    
    print("Technical Summary:")
    print(result['summary'])
    print("\nExport Path:")
    print(result['export_path'])

def example_3_business_summary(agent):
    """Generate a business-focused summary."""
    print("\n=== Example 3: Business-Focused Summary ===")
    
    result = agent.run(
        page_id="123456",
        persona="business",
        context="Focus on business objectives, ROI, and strategic implications",
        include_children=False
    )
    
    print("Business Summary:")
    print(result['summary'])

def example_4_compare_summaries(agent):
    """Compare different types of summaries."""
    print("\n=== Example 4: Comparing Summaries ===")
    
    # Generate two different summaries
    technical_summary = agent.run(
        page_id="123456",
        persona="technical",
        context="Focus on technical implementation"
    )
    
    business_summary = agent.run(
        page_id="123456",
        persona="business",
        context="Focus on business value"
    )
    
    # Compare the summaries
    comparison = agent.compare_summaries(
        technical_summary['export_path'],
        business_summary['export_path']
    )
    
    print("Comparison Statistics:")
    for key, value in comparison['stats'].items():
        print(f"{key}: {value}")
    
    print("\nContent Differences:")
    print(comparison['content_diff'])

def example_5_track_changes(agent):
    """Track changes in a page over time."""
    print("\n=== Example 5: Tracking Changes Over Time ===")
    
    # Generate initial summary
    initial_summary = agent.run(
        page_id="123456",
        persona="technical"
    )
    
    # Wait for some time (simulating page updates)
    time.sleep(5)
    
    # Generate updated summary
    updated_summary = agent.run(
        page_id="123456",
        persona="technical"
    )
    
    # Compare the summaries
    changes = agent.compare_summaries(
        initial_summary['export_path'],
        updated_summary['export_path']
    )
    
    print(f"Changes detected between {initial_summary['metadata']['generated_at']} and {updated_summary['metadata']['generated_at']}:")
    print("\nMetadata Changes:")
    for key, (old, new) in changes['metadata_diff'].items():
        if old != new:
            print(f"{key}:")
            print(f"  - Old: {old}")
            print(f"  + New: {new}")

def example_6_custom_persona(agent):
    """Create and use a custom persona."""
    print("\n=== Example 6: Custom Persona Summary ===")
    
    # Define a custom persona for security-focused summaries
    security_persona = {
        "name": "security",
        "description": "Security-focused summary emphasizing security implications and best practices",
        "instructions": "Focus on security aspects, vulnerabilities, and compliance requirements"
    }
    
    # Generate a security-focused summary
    result = agent.run(
        page_id="123456",
        persona="security",
        context="Analyze security implications and compliance requirements",
        include_children=True
    )
    
    print("Security-Focused Summary:")
    print(result['summary'])

def example_7_batch_processing(agent):
    """Process multiple pages in batch."""
    print("\n=== Example 7: Batch Processing Multiple Pages ===")
    
    # List of page IDs to process
    page_ids = ["123456", "789012", "345678"]
    
    # Process each page
    results = {}
    for page_id in page_ids:
        try:
            result = agent.run(
                page_id=page_id,
                persona="technical",
                include_children=True
            )
            results[page_id] = result
            print(f"Successfully processed page {page_id}")
        except Exception as e:
            print(f"Error processing page {page_id}: {str(e)}")
    
    # Display results
    for page_id, result in results.items():
        print(f"\nPage {page_id}:")
        print(f"Summary: {result['summary'][:200]}...")  # Show first 200 characters
        print(f"Exported to: {result['export_path']}")

def main():
    """Run all examples."""
    # Set up environment
    setup_environment()
    
    # Initialize the agent
    config = Config()
    agent = ConfluenceSummarizerAgent(config)
    
    # Run examples
    example_1_basic_summary(agent)
    example_2_technical_summary(agent)
    example_3_business_summary(agent)
    example_4_compare_summaries(agent)
    example_5_track_changes(agent)
    example_6_custom_persona(agent)
    example_7_batch_processing(agent)

if __name__ == "__main__":
    main() 