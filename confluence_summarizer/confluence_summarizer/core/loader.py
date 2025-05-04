"""Document loader for Confluence content."""

from typing import List, Optional, Dict
from pathlib import Path
import json
import os

from langchain_core.documents import Document
from atlassian import Confluence

from ..config import Config

class ConfluenceDocumentLoader:
    """Loader for Confluence documents."""
    
    def __init__(self, config: Config):
        """Initialize the document loader.
        
        Args:
            config: Configuration object containing Confluence credentials
        """
        self.config = config
        self.client = Confluence(
            url=config.confluence_url,
            username=config.confluence_username,
            password=config.confluence_api_token,
            cloud=True
        )
    
    def load_content(
        self,
        space_key: str,
        page_id: Optional[str] = None,
        include_children: bool = False
    ) -> List[Document]:
        """Load content from Confluence.
        
        Args:
            space_key: The space key to load content from
            page_id: Optional page ID to load specific page
            include_children: Whether to include child pages
            
        Returns:
            List of Document objects containing the content
        """
        documents = []
        
        try:
            if page_id:
                # Load specific page
                page = self.client.get_page_by_id(
                    page_id=page_id,
                    expand='body.storage,version'
                )
                documents.append(self._create_document(page))
                
                if include_children:
                    # Get child pages
                    children = self.client.get_child_pages(
                        page_id=page_id,
                        expand='body.storage,version'
                    )
                    for child in children:
                        documents.append(self._create_document(child))
            else:
                # Load all pages in space
                pages = self.client.get_all_pages_from_space(
                    space=space_key,
                    expand='body.storage,version'
                )
                for page in pages:
                    documents.append(self._create_document(page))
            
            return documents
            
        except Exception as e:
            raise Exception(f"Error loading content from Confluence: {str(e)}")
    
    def _create_document(self, page: Dict) -> Document:
        """Create a Document object from a Confluence page.
        
        Args:
            page: Confluence page data
            
        Returns:
            Document object containing the page content and metadata
        """
        # Extract content
        content = page.get('body', {}).get('storage', {}).get('value', '')
        
        # Extract metadata
        metadata = {
            'id': page.get('id'),
            'title': page.get('title'),
            'space_key': page.get('space', {}).get('key'),
            'version': page.get('version', {}).get('number'),
            'created': page.get('created'),
            'modified': page.get('version', {}).get('when'),
            'author': page.get('version', {}).get('by', {}).get('displayName'),
            'url': f"{self.config.confluence_url}/wiki/spaces/{page.get('space', {}).get('key')}/pages/{page.get('id')}"
        }
        
        return Document(
            page_content=content,
            metadata=metadata
        ) 