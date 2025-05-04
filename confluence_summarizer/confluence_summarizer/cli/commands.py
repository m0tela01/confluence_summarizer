"""CLI commands for the Confluence Summarizer."""

import os
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from confluence_summarizer.agent.summarizer import ConfluenceSummarizerAgent
from confluence_summarizer.config import Config

console = Console()

@click.group()
def cli():
    """Confluence Summarizer - Generate AI-powered summaries of Confluence content."""
    pass

@cli.command()
@click.argument('page_id')
@click.option('--persona', '-p', help='Persona to use for summarization (e.g., technical, business)')
@click.option('--context', '-c', help='Additional context for the summary')
@click.option('--include-children/--no-children', default=True, help='Include child pages in the summary')
def summarize(page_id: str, persona: Optional[str], context: Optional[str], include_children: bool):
    """Generate a summary of a Confluence page."""
    try:
        config = Config()
        agent = ConfluenceSummarizerAgent(config)
        
        # Run the summarization workflow
        result = agent.run(
            page_id=page_id,
            persona=persona,
            context=context,
            include_children=include_children
        )
        
        if result.get('error'):
            console.print(f"[red]Error: {result['error']}[/red]")
            return
        
        # Display the summary
        console.print("\n[bold green]Summary Generated Successfully![/bold green]")
        console.print(f"\n[bold]Summary:[/bold]\n{result['summary']}")
        
        # Display metadata
        if result.get('metadata'):
            console.print("\n[bold]Metadata:[/bold]")
            for key, value in result['metadata'].items():
                console.print(f"{key}: {value}")
        
        # Display export path
        if result.get('export_path'):
            console.print(f"\n[bold]Exported to:[/bold] {result['export_path']}")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@cli.command()
@click.argument('file1', type=click.Path(exists=True))
@click.argument('file2', type=click.Path(exists=True))
def compare(file1: str, file2: str):
    """Compare two summary files and show differences."""
    try:
        config = Config()
        agent = ConfluenceSummarizerAgent(config)
        
        # Run the comparison
        result = agent.compare_summaries(file1, file2)
        
        if result.get('error'):
            console.print(f"[red]Error: {result['error']}[/red]")
            return
        
        # Display comparison results
        console.print("\n[bold green]Comparison Results:[/bold green]")
        
        # Display metadata comparison
        if result.get('metadata_diff'):
            console.print("\n[bold]Metadata Changes:[/bold]")
            for key, (old, new) in result['metadata_diff'].items():
                if old != new:
                    console.print(f"{key}:")
                    console.print(f"  - Old: {old}")
                    console.print(f"  + New: {new}")
        
        # Display content differences
        if result.get('content_diff'):
            console.print("\n[bold]Content Changes:[/bold]")
            console.print(result['content_diff'])
        
        # Display statistics
        if result.get('stats'):
            console.print("\n[bold]Comparison Statistics:[/bold]")
            for key, value in result['stats'].items():
                console.print(f"{key}: {value}")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@cli.command()
def help():
    """Show detailed help and examples for using the Confluence Summarizer."""
    console.print("\n[bold blue]Confluence Summarizer - Help Guide[/bold blue]")
    console.print("\n[bold]Overview:[/bold]")
    console.print("The Confluence Summarizer is a powerful tool that uses AI to generate summaries of Confluence content.")
    console.print("It can analyze pages, compare summaries, and export results in a structured format.")
    
    # Configuration Section
    console.print("\n[bold]1. Configuration[/bold]")
    console.print("Before using the tool, ensure you have set up the following environment variables:")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Variable")
    table.add_column("Description")
    table.add_column("Example")
    
    table.add_row(
        "AZURE_OPENAI_API_KEY",
        "Your Azure OpenAI API key",
        "sk-...",
    )
    table.add_row(
        "AZURE_OPENAI_DEPLOYMENT_NAME",
        "Your Azure OpenAI deployment name",
        "gpt-4",
    )
    table.add_row(
        "AZURE_OPENAI_ENDPOINT",
        "Your Azure OpenAI endpoint URL",
        "https://your-resource.openai.azure.com",
    )
    table.add_row(
        "CONFLUENCE_URL",
        "Your Confluence instance URL",
        "https://your-domain.atlassian.net",
    )
    table.add_row(
        "CONFLUENCE_USERNAME",
        "Your Confluence username/email",
        "user@example.com",
    )
    table.add_row(
        "CONFLUENCE_API_TOKEN",
        "Your Confluence API token",
        "ATATT...",
    )
    table.add_row(
        "CONFLUENCE_SPACE_KEY",
        "Your Confluence space key",
        "TEAM",
    )
    
    console.print(table)
    
    # Usage Examples Section
    console.print("\n[bold]2. Usage Examples[/bold]")
    
    # Summarize Examples
    console.print("\n[bold]Generating Summaries:[/bold]")
    examples = [
        ("Basic summary", "confluence-summarizer summarize 123456"),
        ("Technical summary", "confluence-summarizer summarize 123456 --persona technical"),
        ("Business-focused summary", "confluence-summarizer summarize 123456 --persona business --context \"Focus on business objectives\""),
        ("Summary without child pages", "confluence-summarizer summarize 123456 --no-children"),
        ("Summary with custom context", "confluence-summarizer summarize 123456 --context \"Focus on implementation details and technical debt\""),
    ]
    
    for desc, cmd in examples:
        console.print(f"\n[bold]{desc}:[/bold]")
        console.print(f"  [green]$ {cmd}[/green]")
    
    # Compare Examples
    console.print("\n[bold]Comparing Summaries:[/bold]")
    examples = [
        ("Compare two summaries", "confluence-summarizer compare summary1.md summary2.md"),
        ("Compare summaries in different directories", "confluence-summarizer compare ./old/summary.md ./new/summary.md"),
    ]
    
    for desc, cmd in examples:
        console.print(f"\n[bold]{desc}:[/bold]")
        console.print(f"  [green]$ {cmd}[/green]")
    
    # Output Format Section
    console.print("\n[bold]3. Output Format[/bold]")
    console.print("Summaries are exported as markdown files with the following structure:")
    console.print("""
    # Page Title
    
    ## Metadata
    - Space: TEAM
    - Page ID: 123456
    - URL: https://your-domain.atlassian.net/wiki/spaces/TEAM/pages/123456
    - Author: John Doe
    - Created: 2024-03-15
    - Modified: 2024-03-16
    
    ## Summary
    [Generated summary content]
    
    ## Changes from Previous Summary
    [If applicable, shows differences from the previous summary]
    """)
    
    # Tips Section
    console.print("\n[bold]4. Tips for Best Results[/bold]")
    tips = [
        "Use specific context to guide the summary generation",
        "Choose the appropriate persona for your audience",
        "Include child pages for comprehensive summaries",
        "Compare summaries to track changes over time",
        "Check the exported markdown files for detailed metadata",
    ]
    
    for tip in tips:
        console.print(f"• {tip}")
    
    # Troubleshooting Section
    console.print("\n[bold]5. Troubleshooting[/bold]")
    issues = [
        ("Authentication Error", "Verify your Confluence credentials and API token"),
        ("API Connection Error", "Check your network connection and Confluence URL"),
        ("Summary Generation Failed", "Ensure your Azure OpenAI configuration is correct"),
        ("File Not Found", "Verify the file paths and permissions"),
    ]
    
    for issue, solution in issues:
        console.print(f"\n[bold]{issue}:[/bold]")
        console.print(f"  {solution}")

if __name__ == '__main__':
    cli() 