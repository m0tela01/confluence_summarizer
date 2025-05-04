"""Summarizer agent implementation for Confluence content."""

from typing import Dict, Optional
from pathlib import Path
from datetime import datetime
import json

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

from ..config import Config
from .base import BaseConfluenceAgent, AgentState

class ConfluenceSummarizerAgent(BaseConfluenceAgent):
    """Agent for summarizing Confluence content."""
    
    def __init__(self, config: Config):
        """Initialize the summarization agent."""
        super().__init__(config)
        self.graph = self._create_agent_graph()
    
    def _create_agent_graph(self) -> StateGraph:
        """Create the agent workflow graph."""
        # Define the nodes
        workflow = StateGraph(AgentState)
        
        # Add nodes for each step
        workflow.add_node("load_content", self._load_content)
        workflow.add_node("prepare_documents", self._prepare_documents)
        workflow.add_node("generate_summary", self._generate_summary)
        workflow.add_node("compare_summaries", self._compare_summaries)
        workflow.add_node("export_summary", self._export_summary)
        
        # Define the edges
        workflow.add_edge("load_content", "prepare_documents")
        workflow.add_edge("prepare_documents", "generate_summary")
        workflow.add_edge("generate_summary", "compare_summaries")
        workflow.add_edge("compare_summaries", "export_summary")
        workflow.add_edge("export_summary", END)
        
        # Set the entry point
        workflow.set_entry_point("load_content")
        
        return workflow
    
    def _load_content(self, state: AgentState) -> AgentState:
        """Load content from Confluence."""
        try:
            # Extract parameters from messages
            messages = state["messages"]
            last_message = messages[-1]
            params = json.loads(last_message.content)
            
            # Load documents
            documents = self.document_loader.load_content(
                space_key=params["space_key"],
                page_id=params.get("page_id"),
                include_children=params.get("include_children", False)
            )
            
            # Update state
            state["documents"] = documents
            if documents:
                state["metadata"] = documents[0].metadata
            
            return state
            
        except Exception as e:
            state["messages"].append(AIMessage(content=f"Error loading content: {str(e)}"))
            return state
    
    def _prepare_documents(self, state: AgentState) -> AgentState:
        """Prepare documents for summarization."""
        try:
            documents = state["documents"]
            state["messages"].append(AIMessage(content="Documents loaded successfully. Preparing for summarization..."))
            return state
            
        except Exception as e:
            state["messages"].append(AIMessage(content=f"Error preparing documents: {str(e)}"))
            return state
    
    def _generate_summary(self, state: AgentState) -> AgentState:
        """Generate summary using the LLM."""
        try:
            # Extract parameters
            messages = state["messages"]
            last_message = messages[-1]
            params = json.loads(last_message.content)
            
            # Get persona prompt
            persona = params.get("persona", "technical")
            context = params.get("context")
            persona_prompt = self.persona_manager.get_persona_prompt(persona)
            
            # Create summary prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", f"""You are a {persona} tasked with summarizing Confluence documentation.
                
                {persona_prompt}
                
                {f'Additional context: {context}' if context else ''}
                
                Please provide a comprehensive summary that:
                1. Captures the key points and main ideas
                2. Maintains the technical accuracy of the content
                3. Is organized in a clear, logical structure
                4. Highlights any important warnings, notes, or critical information
                5. Preserves any code examples or technical details"""),
                MessagesPlaceholder(variable_name="messages"),
                ("human", "{input}")
            ])
            
            # Create chain
            chain = prompt | self.llm | StrOutputParser()
            
            # Generate summary
            summary = chain.invoke({
                "messages": state["messages"],
                "input": "\n".join(doc.page_content for doc in state["documents"])
            })
            
            # Update state
            state["summary"] = summary
            state["messages"].append(AIMessage(content="Summary generated successfully."))
            
            return state
            
        except Exception as e:
            state["messages"].append(AIMessage(content=f"Error generating summary: {str(e)}"))
            return state
    
    def _compare_summaries(self, state: AgentState) -> AgentState:
        """Compare current summary with previous summary if available."""
        try:
            # Extract parameters
            messages = state["messages"]
            last_message = messages[-1]
            params = json.loads(last_message.content)
            
            # Look for previous summary file
            export_dir = Path(params.get("export_dir", "summaries"))
            space_key = state["metadata"].get("space_key", "unknown")
            page_id = state["metadata"].get("id")
            
            # Find the most recent summary file
            pattern = f"{space_key}_{page_id}_*.md" if page_id else f"{space_key}_space_*.md"
            previous_files = sorted(export_dir.glob(pattern), reverse=True)
            
            if len(previous_files) > 1:  # Skip the current file
                previous_file = previous_files[1]
                previous_summary = previous_file.read_text(encoding='utf-8')
                
                # Extract the summary section
                if "## Summary" in previous_summary:
                    previous_summary = previous_summary.split("## Summary")[1].split("##")[0].strip()
                    
                    # Calculate comparison stats
                    state["comparison_stats"] = self._calculate_comparison_stats(
                        previous_summary,
                        state["summary"]
                    )
                    
                    # Generate diff
                    diff = list(unified_diff(
                        previous_summary.splitlines(),
                        state["summary"].splitlines(),
                        lineterm=''
                    ))
                    
                    if diff:
                        state["diff_result"] = "\n".join(diff)
                        state["messages"].append(AIMessage(content="Differences from previous summary found."))
                    else:
                        state["messages"].append(AIMessage(content="No differences from previous summary."))
            
            return state
            
        except Exception as e:
            state["messages"].append(AIMessage(content=f"Error comparing summaries: {str(e)}"))
            return state
    
    def _export_summary(self, state: AgentState) -> AgentState:
        """Export summary to a markdown file."""
        try:
            # Extract parameters
            messages = state["messages"]
            last_message = messages[-1]
            params = json.loads(last_message.content)
            
            if not params.get("export", False):
                return state
            
            # Create export directory
            export_dir = Path(params.get("export_dir", "summaries"))
            export_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            space_key = state["metadata"].get("space_key", "unknown")
            page_id = state["metadata"].get("id")
            filename = f"{space_key}_{page_id}_{timestamp}.md" if page_id else f"{space_key}_space_{timestamp}.md"
            
            # Create markdown content
            content = f"""# {state["metadata"].get("title", "Confluence Content")}

## Metadata
- Author: {os.getlogin()}
- Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary
{state["summary"]}

"""
            
            # Add comparison stats if available
            if state.get("comparison_stats"):
                stats = state["comparison_stats"]
                content += f"""
## Comparison Statistics

### Overview
| Metric | Value |
|--------|-------|
| Total Lines | {stats["new_line_count"]} (Change: {stats["line_difference"]:+d}) |
| Changed Sections | {stats["changed_sections"]} |
| Added Sections | {stats["added_sections"]} |
| Removed Sections | {stats["removed_sections"]} |

### Section Changes
| Section | Lines | Change | Summary |
|---------|-------|--------|---------|
"""
                for change in stats["section_changes"]:
                    content += f"""| {change['section']} | {change['new_line_count']} | {change['diff_line_count']:+d} | {change['change_summary']} |
"""
            
            # Add diff section if available
            if state.get("diff_result"):
                content += f"""
## Changes from Previous Summary

```diff
{state["diff_result"]}
```
"""
            
            content += f"""
---
*Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
            
            # Write to file
            file_path = export_dir / filename
            file_path.write_text(content, encoding='utf-8')
            
            # Update state
            state["export_path"] = file_path
            state["messages"].append(AIMessage(content=f"Summary exported to: {file_path}"))
            
            return state
            
        except Exception as e:
            state["messages"].append(AIMessage(content=f"Error exporting summary: {str(e)}"))
            return state
    
    def summarize(
        self,
        space_key: str,
        page_id: Optional[str] = None,
        include_children: bool = False,
        persona: str = "technical",
        context: Optional[str] = None,
        export: bool = False,
        export_dir: str = "summaries"
    ) -> Dict:
        """Run the summarization workflow.
        
        Args:
            space_key: The space key to summarize
            page_id: Optional page ID to summarize
            include_children: Whether to include child pages
            persona: The persona to use
            context: Optional additional context
            export: Whether to export the summary
            export_dir: Directory to export to
            
        Returns:
            Dictionary containing the results
        """
        # Create initial state
        initial_state = {
            "messages": [
                HumanMessage(content=json.dumps({
                    "space_key": space_key,
                    "page_id": page_id,
                    "include_children": include_children,
                    "persona": persona,
                    "context": context,
                    "export": export,
                    "export_dir": export_dir
                }))
            ],
            "documents": [],
            "summary": None,
            "metadata": {},
            "export_path": None,
            "previous_summary": None,
            "diff_result": None,
            "comparison_stats": None
        }
        
        # Run the workflow
        final_state = self.graph.invoke(initial_state)
        
        return {
            "summary": final_state["summary"],
            "export_path": str(final_state["export_path"]) if final_state["export_path"] else None,
            "messages": [msg.content for msg in final_state["messages"]],
            "diff_result": final_state.get("diff_result"),
            "comparison_stats": final_state.get("comparison_stats")
        } 