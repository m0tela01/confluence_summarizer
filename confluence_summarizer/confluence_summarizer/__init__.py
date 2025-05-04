"""Confluence Summarizer - Generate summaries of Confluence content."""

from .config import Config
from .agent.summarizer import ConfluenceSummarizerAgent
from .core.persona import PersonaManager
from .core.loader import ConfluenceDocumentLoader

__version__ = "0.1.0"
__all__ = ["Config", "ConfluenceSummarizerAgent", "PersonaManager", "ConfluenceDocumentLoader"] 