"""
Unit tests for the RAG system module.

Tests core RAG functionality including document management,
querying, and response generation.
"""

import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_system import MultilingualRAGSystem, Document


class TestMultilingualRAGSystem(unittest.TestCase):
    """Test cases for MultilingualRAGSystem class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock the OpenAI client to avoid API calls during testing
        with patch('rag_system.openai.OpenAI'):
            self.rag_system = MultilingualRAGSystem(api_key="test_key")
    
    def test_initialization(self):
        """Test system initialization."""
        self.assertIsNotNone(self.rag_system)
        self.assertEqual(self.rag_system.api_key, "test_key")
        self.assertEqual(len(self.rag_system.documents), 0)
    
    def test_add_documents(self):
        """Test adding documents to the system."""
        # Create test documents
        doc1 = Document("Hello world", {"language": "English", "level": "A1"})
        doc2 = Document("Bonjour monde", {"language": "French", "level": "A1"})
        
        self.rag_system.add_documents([doc1, doc2])
        
        self.assertEqual(len(self.rag_system.documents), 2)
        self.assertEqual(len(self.rag_system.document_metadata), 2)
    
    @patch('rag_system.openai.OpenAI')
    def test_query_no_documents(self, mock_openai):
        """Test querying with no documents."""
        result = self.rag_system.query("test query")
        self.assertEqual(result, "No documents available for querying.")
    
    def test_query_with_language_filter(self):
        """Test querying with language filter."""
        # Add test documents
        doc1 = Document("Hello world", {"language": "English"})
        doc2 = Document("Bonjour monde", {"language": "French"})
        self.rag_system.add_documents([doc1, doc2])
        
        # Mock the response generation
        with patch.object(self.rag_system, '_generate_response', return_value="Mocked response"):
            result = self.rag_system.query("test", language_filter="French")
            self.assertIsNotNone(result)
    
    def test_file_summary(self):
        """Test getting file summary."""
        # Add test documents with metadata
        doc1 = Document("Test 1", {"language": "English", "file_name": "test1.txt"})
        doc2 = Document("Test 2", {"language": "French", "file_name": "test2.txt"})
        self.rag_system.add_documents([doc1, doc2])
        
        summary = self.rag_system.get_file_summary()
        
        self.assertEqual(summary['total_documents'], 2)
        self.assertIn('English', summary['languages'])
        self.assertIn('French', summary['languages'])


class TestDocument(unittest.TestCase):
    """Test cases for Document class."""
    
    def test_document_creation(self):
        """Test document creation."""
        doc = Document("Test text", {"key": "value"})
        
        self.assertEqual(doc.text, "Test text")
        self.assertEqual(doc.metadata["key"], "value")
    
    def test_document_empty_metadata(self):
        """Test document creation with empty metadata."""
        doc = Document("Test text")
        
        self.assertEqual(doc.text, "Test text")
        self.assertEqual(doc.metadata, {})


if __name__ == '__main__':
    unittest.main()