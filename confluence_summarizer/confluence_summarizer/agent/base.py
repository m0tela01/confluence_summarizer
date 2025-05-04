"""Base agent implementation for Confluence summarization."""

from typing import Dict, List, Optional, TypedDict, Annotated, Sequence
from pathlib import Path
from datetime import datetime
import json
from difflib import unified_diff
import os
import re

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import AzureOpenAI
from langchain.schema import Document
from langgraph.graph import StateGraph, END

from ..config import Config
from ..core.document_loader import ConfluenceDocumentLoader
from ..core.personas import PersonaManager

# Define state types
class AgentState(TypedDict):
    """State for the summarization agent."""
    messages: Annotated[Sequence[BaseMessage], "Chat messages"]
    documents: Annotated[List[Document], "Loaded documents"]
    summary: Annotated[Optional[str], "Generated summary"]
    metadata: Annotated[Dict, "Document metadata"]
    export_path: Annotated[Optional[Path], "Path to exported summary"]
    previous_summary: Annotated[Optional[str], "Previous summary for comparison"]
    diff_result: Annotated[Optional[str], "Diff between current and previous summary"]
    comparison_stats: Annotated[Optional[Dict], "Statistics about the comparison"]

class BaseConfluenceAgent:
    """Base agent for Confluence content operations."""
    
    def __init__(self, config: Config):
        """Initialize the base agent."""
        self.config = config
        self.persona_manager = PersonaManager()
        
        # Initialize components
        self.llm = AzureOpenAI(
            deployment_name=config.azure_openai.deployment_name,
            openai_api_version=config.azure_openai.api_version,
            temperature=0.7
        )
        self.document_loader = ConfluenceDocumentLoader(config)
    
    def _analyze_section_changes(self, old_section: str, new_section: str) -> str:
        """Analyze the contextual changes in a section."""
        try:
            # Create prompt for change analysis
            prompt = ChatPromptTemplate.from_messages([
                ("system", """Analyze the changes between two versions of a section and provide a brief summary.
                Focus on meaningful changes and ignore minor formatting differences.
                If the changes are purely formatting or very minor, state that explicitly.
                Otherwise, summarize the key changes in 1-2 sentences."""),
                ("human", "Old version:\n{old}\n\nNew version:\n{new}")
            ])
            
            # Create chain
            chain = prompt | self.llm | StrOutputParser()
            
            # Generate analysis
            analysis = chain.invoke({
                "old": old_section,
                "new": new_section
            })
            
            return analysis.strip()
            
        except Exception as e:
            return f"Error analyzing changes: {str(e)}"
    
    def _calculate_comparison_stats(self, old_content: str, new_content: str) -> Dict:
        """Calculate statistics about the comparison."""
        old_lines = old_content.splitlines()
        new_lines = new_content.splitlines()
        
        # Calculate basic stats
        stats = {
            "old_line_count": len(old_lines),
            "new_line_count": len(new_lines),
            "line_difference": len(new_lines) - len(old_lines),
            "changed_sections": 0,
            "added_sections": 0,
            "removed_sections": 0,
            "section_changes": []
        }
        
        # Split into sections
        old_sections = re.split(r"(?=## )", old_content)
        new_sections = re.split(r"(?=## )", new_content)
        
        # Compare sections
        old_section_titles = {s.split("\n")[0].strip("# ") for s in old_sections if s.strip()}
        new_section_titles = {s.split("\n")[0].strip("# ") for s in new_sections if s.strip()}
        
        # Calculate section changes
        stats["added_sections"] = len(new_section_titles - old_section_titles)
        stats["removed_sections"] = len(old_section_titles - new_section_titles)
        stats["changed_sections"] = len(old_section_titles & new_section_titles)
        
        # Analyze section changes
        for section in old_section_titles & new_section_titles:
            old_section = next(s for s in old_sections if s.split("\n")[0].strip("# ") == section)
            new_section = next(s for s in new_sections if s.split("\n")[0].strip("# ") == section)
            
            old_lines = old_section.split("\n")[1:]
            new_lines = new_section.split("\n")[1:]
            
            diff = list(unified_diff(old_lines, new_lines, lineterm=''))
            if diff:
                # Analyze contextual changes
                change_summary = self._analyze_section_changes(
                    "\n".join(old_lines),
                    "\n".join(new_lines)
                )
                
                stats["section_changes"].append({
                    "section": section,
                    "old_line_count": len(old_lines),
                    "new_line_count": len(new_lines),
                    "diff_line_count": len(diff),
                    "change_summary": change_summary
                })
        
        return stats 