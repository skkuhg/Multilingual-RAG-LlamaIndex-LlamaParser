"""
Multilingual RAG Language Learning System

A comprehensive system for processing multilingual content and creating
intelligent language learning experiences using RAG technology.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .rag_system import MultilingualRAGSystem
from .data_processor import DataProcessor
from .srs_scheduler import SRSScheduler
from .language_detector import LanguageDetector
from .cost_tracker import TokenTracker

__all__ = [
    "MultilingualRAGSystem",
    "DataProcessor", 
    "SRSScheduler",
    "LanguageDetector",
    "TokenTracker",
]