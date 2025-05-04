"""Persona manager for Confluence summarization."""

from typing import Dict, Optional

class PersonaManager:
    """Manager for different summarization personas."""
    
    def __init__(self):
        """Initialize the persona manager with default personas."""
        self.personas = {
            "technical": """You are a technical expert focused on implementation details, code, and technical architecture.
            Your summaries should:
            1. Highlight technical specifications and requirements
            2. Preserve code examples and technical details
            3. Focus on implementation approaches and patterns
            4. Note any technical constraints or limitations
            5. Emphasize system architecture and design decisions""",
            
            "business": """You are a business analyst focused on objectives, requirements, and business value.
            Your summaries should:
            1. Highlight business objectives and goals
            2. Focus on requirements and use cases
            3. Emphasize business impact and value
            4. Note any business constraints or risks
            5. Summarize key stakeholders and their needs""",
            
            "project": """You are a project manager focused on timelines, deliverables, and project status.
            Your summaries should:
            1. Highlight project milestones and deadlines
            2. Focus on deliverables and their status
            3. Emphasize dependencies and blockers
            4. Note any risks or issues
            5. Summarize resource allocation and team assignments""",
            
            "user": """You are a user experience expert focused on usability and user needs.
            Your summaries should:
            1. Highlight user workflows and interactions
            2. Focus on user requirements and needs
            3. Emphasize usability considerations
            4. Note any user feedback or pain points
            5. Summarize user personas and scenarios"""
        }
    
    def get_persona_prompt(self, persona: str) -> str:
        """Get the prompt for a specific persona.
        
        Args:
            persona: The persona to get the prompt for
            
        Returns:
            The persona prompt
            
        Raises:
            ValueError: If the persona is not found
        """
        if persona not in self.personas:
            raise ValueError(f"Unknown persona: {persona}")
        
        return self.personas[persona]
    
    def add_persona(self, name: str, prompt: str) -> None:
        """Add a new persona.
        
        Args:
            name: The name of the persona
            prompt: The prompt for the persona
        """
        self.personas[name] = prompt
    
    def remove_persona(self, name: str) -> None:
        """Remove a persona.
        
        Args:
            name: The name of the persona to remove
            
        Raises:
            ValueError: If the persona is not found
        """
        if name not in self.personas:
            raise ValueError(f"Unknown persona: {name}")
        
        del self.personas[name]
    
    def list_personas(self) -> Dict[str, str]:
        """List all available personas.
        
        Returns:
            Dictionary mapping persona names to their prompts
        """
        return self.personas.copy() 