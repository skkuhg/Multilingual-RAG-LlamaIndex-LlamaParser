"""
Unit tests for the data processor module.

Tests file ingestion, parsing, and data processing functionality.
"""

import unittest
from unittest.mock import patch, mock_open
import pandas as pd
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = DataProcessor()
    
    def test_initialization(self):
        """Test processor initialization."""
        self.assertIsNotNone(self.processor)
        self.assertIsNotNone(self.processor.language_detector)
        self.assertIn('.txt', self.processor.supported_extensions)
        self.assertIn('.csv', self.processor.supported_extensions)
    
    @patch('data_processor.Path')
    def test_ingest_data_files_no_folder(self, mock_path):
        """Test ingesting data when folder doesn't exist."""
        mock_path.return_value.exists.return_value = False
        
        result = self.processor.ingest_data_files("nonexistent")
        
        self.assertTrue(result.empty)
    
    def test_parse_text_simple(self):
        """Test parsing simple text content."""
        test_content = "Hello world. This is a test. Another sentence."
        
        with patch('builtins.open', mock_open(read_data=test_content)):
            with patch('data_processor.Path'):
                result = self.processor._parse_text(Path("test.txt"))
        
        self.assertGreater(len(result), 0)
        self.assertIn('text', result[0])
    
    def test_parse_csv_vocabulary(self):
        """Test parsing CSV vocabulary format."""
        csv_content = "word,translation\nhello,hola\nworld,mundo"
        
        with patch('builtins.open', mock_open(read_data=csv_content)):
            with patch('pandas.read_csv') as mock_read_csv:
                mock_df = pd.DataFrame({
                    'word': ['hello', 'world'],
                    'translation': ['hola', 'mundo']
                })
                mock_read_csv.return_value = mock_df
                
                result = self.processor._parse_csv(Path("test.csv"))
        
        self.assertGreater(len(result), 0)
        self.assertIn('word', result[0])
        self.assertIn('translation', result[0])
    
    def test_create_documents(self):
        """Test creating Document objects from DataFrame."""
        test_df = pd.DataFrame({
            'text': ['Hello', 'World'],
            'language': ['English', 'English'],
            'level': ['A1', 'A1']
        })
        
        documents = self.processor.create_documents(test_df)
        
        self.assertEqual(len(documents), 2)
        self.assertEqual(documents[0].text, 'Hello')
        self.assertEqual(documents[0].metadata['language'], 'English')


if __name__ == '__main__':
    unittest.main()