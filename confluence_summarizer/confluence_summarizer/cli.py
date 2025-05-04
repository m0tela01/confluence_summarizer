"""Command-line interface for the Confluence summarizer."""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.text import Text
from rich.style import Style
from rich import box
import os
from pathlib import Path
from datetime import datetime
import json
from typing import Optional, List, Dict
import re

from .config import Config
from .agent.summarizer import ConfluenceSummarizerAgent
from .core.persona import PersonaManager

console = Console()

def extract_metadata_from_file(file_path: Path) -> Dict:
    """Extract metadata from a summary markdown file.
    
    Args:
        file_path: Path to the summary file
        
    Returns:
        Dictionary containing the metadata
    """
    content = file_path.read_text(encoding='utf-8')
    
    # Extract title
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Unknown"
    
    # Extract metadata section
    metadata = {}
    metadata_match = re.search(r'## Metadata\n(.*?)(?=\n\n|\Z)', content, re.DOTALL)
    if metadata_match:
        metadata_text = metadata_match.group(1)
        for line in metadata_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
    
    # Extract generation timestamp
    timestamp_match = re.search(r'Generated on: (.+)$', content, re.MULTILINE)
    if timestamp_match:
        metadata['generated_at'] = timestamp_match.group(1)
    
    return {
        'title': title,
        'metadata': metadata
    }

def display_diff(old_content: str, new_content: str) -> None:
    """Display differences between two pieces of content.
    
    Args:
        old_content: The old content
        new_content: The new content
    """
    # Split content into sections
    old_sections = re.split(r'(?=^#+ )', old_content, flags=re.MULTILINE)
    new_sections = re.split(r'(?=^#+ )', new_content, flags=re.MULTILINE)
    
    # Create a table for section changes
    table = Table(
        title="Section Changes",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("Section", style="cyan")
    table.add_column("Old Lines", justify="right", style="red")
    table.add_column("New Lines", justify="right", style="green")
    table.add_column("Changes", justify="right", style="yellow")
    table.add_column("Summary", style="white")
    
    # Compare sections
    for old_section in old_sections:
        if not old_section.strip():
            continue
            
        # Get section title
        title_match = re.match(r'^(#+ )(.+)$', old_section, re.MULTILINE)
        if not title_match:
            continue
            
        section_title = title_match.group(2).strip()
        
        # Find matching section in new content
        new_section = next(
            (s for s in new_sections if s.strip() and re.match(r'^#+ ' + re.escape(section_title), s, re.MULTILINE)),
            None
        )
        
        if new_section:
            # Section exists in both
            old_lines = len(old_section.splitlines())
            new_lines = len(new_section.splitlines())
            diff_lines = new_lines - old_lines
            
            # Generate diff
            diff = list(unified_diff(
                old_section.splitlines(),
                new_section.splitlines(),
                lineterm=''
            ))
            
            # Summarize changes
            if diff:
                summary = "Content updated"
                if diff_lines > 0:
                    summary += f" (+{diff_lines} lines)"
                elif diff_lines < 0:
                    summary += f" ({diff_lines} lines)"
            else:
                summary = "No changes"
            
            table.add_row(
                section_title,
                str(old_lines),
                str(new_lines),
                f"{diff_lines:+d}",
                summary
            )
        else:
            # Section removed
            old_lines = len(old_section.splitlines())
            table.add_row(
                section_title,
                str(old_lines),
                "0",
                f"-{old_lines}",
                "Section removed"
            )
    
    # Add new sections
    for new_section in new_sections:
        if not new_section.strip():
            continue
            
        # Get section title
        title_match = re.match(r'^(#+ )(.+)$', new_section, re.MULTILINE)
        if not title_match:
            continue
            
        section_title = title_match.group(2).strip()
        
        # Check if section exists in old content
        if not any(re.match(r'^#+ ' + re.escape(section_title), s, re.MULTILINE) for s in old_sections if s.strip()):
            # New section
            new_lines = len(new_section.splitlines())
            table.add_row(
                section_title,
                "0",
                str(new_lines),
                f"+{new_lines}",
                "New section"
            )
    
    # Display the table
    console.print(table)
    
    # Display detailed diff
    console.print("\nDetailed Changes:")
    diff = list(unified_diff(
        old_content.splitlines(),
        new_content.splitlines(),
        lineterm=''
    ))
    
    if diff:
        diff_text = "\n".join(diff)
        syntax = Syntax(diff_text, "diff", theme="monokai", line_numbers=True)
        console.print(syntax)
    else:
        console.print("[green]No changes found[/green]")

@click.group()
def cli():
    """Confluence Summarizer - Generate summaries of Confluence content."""
    pass

@cli.command()
@click.argument('space_key')
@click.option('--page-id', help='Specific page ID to summarize')
@click.option('--include-children/--no-children', default=False, help='Include child pages')
@click.option('--persona', default='technical', help='Persona to use for summarization')
@click.option('--context', help='Additional context for summarization')
@click.option('--export/--no-export', default=True, help='Export summary to markdown file')
@click.option('--export-dir', default='summaries', help='Directory to export summaries to')
def summarize(space_key: str, page_id: Optional[str], include_children: bool,
             persona: str, context: Optional[str], export: bool, export_dir: str):
    """Generate a summary of Confluence content.
    
    SPACE_KEY is the key of the Confluence space to summarize.
    """
    try:
        # Load configuration
        config = Config.from_env()
        config.validate()
        
        # Create agent
        agent = ConfluenceSummarizerAgent(config)
        
        # Generate summary
        result = agent.summarize(
            space_key=space_key,
            page_id=page_id,
            include_children=include_children,
            persona=persona,
            context=context,
            export=export,
            export_dir=export_dir
        )
        
        # Display summary
        if result["summary"]:
            console.print("\n[bold green]Summary Generated:[/bold green]")
            console.print(Markdown(result["summary"]))
            
            if result["export_path"]:
                console.print(f"\n[bold blue]Summary exported to:[/bold blue] {result['export_path']}")
            
            if result.get("diff_result"):
                console.print("\n[bold yellow]Changes from previous summary:[/bold yellow]")
                display_diff(result["previous_summary"], result["summary"])
        
        # Display any messages
        for message in result["messages"]:
            if message.startswith("Error"):
                console.print(f"[red]{message}[/red]")
            else:
                console.print(f"[blue]{message}[/blue]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise click.Abort()

@cli.command()
@click.argument('file1', type=click.Path(exists=True))
@click.argument('file2', type=click.Path(exists=True))
def compare(file1: str, file2: str):
    """Compare two summary files.
    
    FILE1 and FILE2 are paths to the summary files to compare.
    """
    try:
        # Load files
        file1_path = Path(file1)
        file2_path = Path(file2)
        
        # Extract metadata
        metadata1 = extract_metadata_from_file(file1_path)
        metadata2 = extract_metadata_from_file(file2_path)
        
        # Display metadata comparison
        table = Table(
            title="Summary Comparison - Metadata",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("Property", style="cyan")
        table.add_column("File 1", style="red")
        table.add_column("File 2", style="green")
        
        # Add metadata rows
        for key in set(metadata1["metadata"].keys()) | set(metadata2["metadata"].keys()):
            value1 = metadata1["metadata"].get(key, "N/A")
            value2 = metadata2["metadata"].get(key, "N/A")
            table.add_row(key, value1, value2)
        
        console.print(table)
        
        # Display content comparison
        content1 = file1_path.read_text(encoding='utf-8')
        content2 = file2_path.read_text(encoding='utf-8')
        
        display_diff(content1, content2)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise click.Abort()

@cli.command()
def list_personas():
    """List available summarization personas."""
    try:
        persona_manager = PersonaManager()
        personas = persona_manager.list_personas()
        
        table = Table(
            title="Available Personas",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )
        
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="white")
        
        for name, prompt in personas.items():
            # Extract first line of prompt as description
            description = prompt.split('\n')[0].strip()
            table.add_row(name, description)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise click.Abort()

if __name__ == '__main__':
    cli() 