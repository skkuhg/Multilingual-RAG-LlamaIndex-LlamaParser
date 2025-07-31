"""
Core RAG System Implementation

This module provides the main RAG system functionality for multilingual
language learning, including document indexing, querying, and response generation.
"""

import os
import re
from typing import List, Dict, Optional, Any
from pathlib import Path
import openai
from datetime import datetime

try:
    from llama_parse import LlamaParse
    LLAMA_PARSE_AVAILABLE = True
except ImportError:
    LLAMA_PARSE_AVAILABLE = False

try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False


class Document:
    """Simple document class for storing text and metadata."""
    
    def __init__(self, text: str, metadata: Dict = None):
        self.text = text
        self.metadata = metadata or {}


class MultilingualRAGSystem:
    """
    Main RAG system for multilingual language learning.
    
    Provides document indexing, semantic search, and intelligent query capabilities
    with support for multiple languages and learning contexts.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the RAG system.
        
        Args:
            api_key: OpenAI API key. If None, reads from environment.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
            
        self.client = openai.OpenAI(api_key=self.api_key)
        self.documents = []
        self.embeddings = []
        self.document_metadata = []
        
        # Initialize LlamaParser if available
        llama_key = os.getenv('LLAMACLOUD_API_KEY')
        if LLAMA_PARSE_AVAILABLE and llama_key:
            self.parser = LlamaParse(
                api_key=llama_key,
                result_type="text",
                verbose=False,
                language="mixed"
            )
        else:
            self.parser = None
            
        # Initialize Tavily if available
        tavily_key = os.getenv('TAVILY_API_KEY')
        if TAVILY_AVAILABLE and tavily_key:
            self.tavily_client = TavilyClient(api_key=tavily_key)
        else:
            self.tavily_client = None
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the RAG system.
        
        Args:
            documents: List of Document objects to add
        """
        self.documents.extend(documents)
        
        # Track metadata separately for better querying
        for doc in documents:
            self.document_metadata.append(doc.metadata)
        
        print(f"Added {len(documents)} documents. Total: {len(self.documents)}")
        
        # Show metadata summary
        if self.document_metadata:
            languages = [meta.get('language', 'Unknown') for meta in self.document_metadata]
            from collections import Counter
            lang_counter = Counter(languages)
            print(f"📊 Language distribution in index: {dict(lang_counter)}")
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding for text using OpenAI.
        
        Args:
            text: Text to embed
            
        Returns:
            List of embedding values
        """
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return [0.0] * 1536  # Fallback embedding
    
    def query(self, query_text: str, top_k: int = 5, language_filter: str = None,
              level_filter: str = None, file_filter: str = None) -> str:
        """
        Query the RAG system with optional filtering.
        
        Args:
            query_text: Query string
            top_k: Number of results to return
            language_filter: Filter by language
            level_filter: Filter by CEFR level
            file_filter: Filter by filename
            
        Returns:
            Generated response string
        """
        if not self.documents:
            return "No documents available for querying."
        
        # Filter documents based on criteria
        filtered_docs = []
        filtered_metadata = []
        
        for doc, meta in zip(self.documents, self.document_metadata):
            # Apply filters
            if language_filter and meta.get('language', '').lower() != language_filter.lower():
                continue
            if level_filter and meta.get('cefr_level', '') != level_filter:
                continue
            if file_filter and file_filter.lower() not in meta.get('source_file', '').lower():
                continue
            
            filtered_docs.append(doc)
            filtered_metadata.append(meta)
        
        if not filtered_docs:
            return f"No documents found matching filters (language={language_filter}, level={level_filter}, file={file_filter})"
        
        # Enhanced keyword-based retrieval
        relevant_docs = self._retrieve_relevant_docs(query_text, filtered_docs, filtered_metadata, top_k)
        
        if not relevant_docs:
            relevant_docs = [(filtered_docs[0], filtered_metadata[0])]
        
        # Create context with metadata
        context = self._create_context(relevant_docs)
        
        # Generate response using OpenAI
        return self._generate_response(query_text, context)
    
    def _retrieve_relevant_docs(self, query_text: str, docs: List[Document],
                               metadata: List[Dict], top_k: int) -> List[tuple]:
        """Retrieve most relevant documents based on keyword matching."""
        query_lower = query_text.lower()
        query_words = query_lower.split()
        
        doc_scores = []
        
        for doc, meta in zip(docs, metadata):
            score = 0
            doc_text_lower = doc.text.lower()
            
            # Keyword matching
            for word in query_words:
                if word in doc_text_lower:
                    score += 2
            
            # Boost score for exact phrase matches
            if query_lower in doc_text_lower:
                score += 5
            
            # Metadata-based scoring
            if 'context' in meta and query_lower in meta['context'].lower():
                score += 1
            
            doc_scores.append((score, doc, meta))
        
        # Sort by score and select top documents
        doc_scores.sort(key=lambda x: x[0], reverse=True)
        
        # Return documents with positive scores, or top k if none
        if any(score > 0 for score, _, _ in doc_scores):
            return [(doc, meta) for score, doc, meta in doc_scores[:top_k] if score > 0]
        else:
            return [(doc, meta) for _, doc, meta in doc_scores[:top_k]]
    
    def _create_context(self, relevant_docs: List[tuple]) -> str:
        """Create formatted context from relevant documents."""
        context_parts = []
        
        for doc, meta in relevant_docs:
            context_part = f"Text: {doc.text}\n"
            
            if meta.get('language'):
                context_part += f"Language: {meta['language']}\n"
            if meta.get('cefr_level'):
                context_part += f"Level: {meta['cefr_level']}\n"
            if meta.get('file_name'):
                context_part += f"Source: {meta['file_name']}\n"
            if meta.get('context'):
                context_part += f"Context: {meta['context'][:100]}...\n"
            
            context_part += "---\n"
            context_parts.append(context_part)
        
        return "\n".join(context_parts)
    
    def _generate_response(self, query_text: str, context: str) -> str:
        """Generate response using OpenAI with the provided context."""
        try:
            system_prompt = """You are a helpful multilingual language learning assistant. 
            Use the provided context to answer questions about language learning content.
            Pay attention to the metadata (language, level, source) when providing answers.
            If asking about specific patterns or grammar, provide examples from the context.
            Always be encouraging and educational in your responses."""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query_text}"}
                ],
                temperature=0.2,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {e}"
    
    def get_file_summary(self) -> Dict[str, Any]:
        """Get summary of all files in the RAG system."""
        if not self.document_metadata:
            return {}
        
        from collections import defaultdict, Counter
        
        summary = {
            'total_documents': len(self.documents),
            'files': Counter(),
            'languages': Counter(),
            'levels': Counter(),
            'file_types': Counter()
        }
        
        for meta in self.document_metadata:
            if 'file_name' in meta:
                summary['files'][meta['file_name']] += 1
            if 'language' in meta:
                summary['languages'][meta['language']] += 1
            if 'cefr_level' in meta:
                summary['levels'][meta['cefr_level']] += 1
            if 'file_type' in meta:
                summary['file_types'][meta['file_type']] += 1
        
        return summary
    
    def search_web(self, query: str, max_results: int = 3) -> Dict[str, Any]:
        """
        Search the web for additional language learning content.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            Search results dictionary
        """
        if not self.tavily_client:
            return {"error": "Tavily client not available"}
        
        try:
            results = self.tavily_client.search(
                query=query,
                search_depth="basic",
                max_results=max_results,
                include_answer=True
            )
            return results
        except Exception as e:
            return {"error": f"Web search failed: {e}"}


class SimpleQueryEngine:
    """Simple query engine wrapper for compatibility."""
    
    def __init__(self, rag_system: MultilingualRAGSystem):
        """
        Initialize query engine.
        
        Args:
            rag_system: The RAG system to wrap
        """
        self.rag_system = rag_system
    
    def query(self, prompt: str) -> str:
        """
        Query the RAG system.
        
        Args:
            prompt: Query prompt
            
        Returns:
            Query response
        """
        if self.rag_system:
            return self.rag_system.query(prompt)
        else:
            return "RAG system not available"