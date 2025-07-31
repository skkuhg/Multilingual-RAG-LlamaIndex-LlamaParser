"""
Unit tests for the language detector module.

Tests language detection and CEFR level estimation functionality.
"""

import unittest
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from language_detector import LanguageDetector


class TestLanguageDetector(unittest.TestCase):
    """Test cases for LanguageDetector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = LanguageDetector()
    
    def test_initialization(self):
        """Test detector initialization."""
        self.assertIsNotNone(self.detector)
        self.assertIn('Korean', self.detector.language_patterns)
        self.assertIn('English', self.detector.language_patterns)
    
    def test_detect_english(self):
        """Test English language detection."""
        text = "Hello world, this is a test sentence in English."
        result = self.detector.detect_language(text)
        self.assertEqual(result, 'English')
    
    def test_detect_korean(self):
        """Test Korean language detection."""
        text = "안녕하세요. 저는 한국어를 공부하고 있습니다."
        result = self.detector.detect_language(text)
        self.assertEqual(result, 'Korean')
    
    def test_detect_spanish(self):
        """Test Spanish language detection."""
        text = "Hola mundo, esta es una oración de prueba en español."
        result = self.detector.detect_language(text)
        self.assertEqual(result, 'Spanish')
    
    def test_estimate_cefr_level_simple(self):
        """Test CEFR level estimation for simple text."""
        simple_text = "Hello. My name is John."
        result = self.detector.estimate_cefr_level(simple_text)
        self.assertIn(result, ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])
    
    def test_estimate_cefr_level_complex(self):
        """Test CEFR level estimation for complex text."""
        complex_text = "Notwithstanding the comprehensive analysis, the methodology remains sophisticated."
        result = self.detector.estimate_cefr_level(complex_text)
        self.assertIn(result, ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'])
    
    def test_analyze_text_features(self):
        """Test text feature analysis."""
        text = "This is a test sentence for analysis."
        result = self.detector.analyze_text_features(text)
        
        self.assertIn('word_count', result)
        self.assertIn('sentence_count', result)
        self.assertIn('avg_word_length', result)
        self.assertGreater(result['word_count'], 0)
    
    def test_unknown_language_defaults_to_english(self):
        """Test that unknown languages default to English."""
        # Use text that doesn't match any specific patterns
        text = "xyz abc def"
        result = self.detector.detect_language(text)
        self.assertEqual(result, 'English')


if __name__ == '__main__':
    unittest.main()