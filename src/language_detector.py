"""
Language Detection and CEFR Level Estimation Module

Provides automatic language identification and complexity assessment
for multilingual language learning content.
"""

import re
from typing import Dict, List, Optional, Tuple
from collections import Counter


class LanguageDetector:
    """
    Detects language and estimates CEFR levels for text content.
    
    Uses pattern-based detection for accurate multilingual support
    with educational context awareness.
    """
    
    def __init__(self):
        """Initialize the language detector with pattern rules."""
        self.language_patterns = {
            'Korean': [
                r'[가-힣]+',  # Hangul characters
                r'\b(은|는|이|가|을|를|에|에서|으로|로)\b',  # Common particles
                r'\b(입니다|습니다|해요|이에요|예요)\b',  # Polite endings
            ],
            'Japanese': [
                r'[ひらがな-ゟ]+|[カタカナ-ヿ]+',  # Hiragana and Katakana
                r'[一-龯]+',  # Kanji
                r'\b(です|ます|だ|である)\b',  # Common endings
            ],
            'Chinese': [
                r'[一-龯]+',  # Chinese characters
                r'\b(的|是|在|了|和|有)\b',  # Common particles
            ],
            'Spanish': [
                r'\b(el|la|los|las|un|una|de|en|y|que|a|por|para)\b',
                r'\b(estoy|está|están|soy|es|son|tengo|tiene|tienen)\b',
                r'[ñáéíóúü]',  # Spanish accented characters
            ],
            'French': [
                r'\b(le|la|les|un|une|de|du|des|et|à|dans|pour|avec)\b',
                r'\b(je|tu|il|elle|nous|vous|ils|elles)\b',
                r'[àâäéèêëïîôöùûüÿç]',  # French accented characters
            ],
            'German': [
                r'\b(der|die|das|ein|eine|und|mit|zu|von|für|auf)\b',
                r'\b(ich|du|er|sie|es|wir|ihr|sie)\b',
                r'[äöüß]',  # German special characters
            ],
            'English': [
                r'\b(the|a|an|and|or|but|in|on|at|to|for|of|with)\b',
                r'\b(I|you|he|she|it|we|they|am|is|are|was|were)\b',
            ],
            'Italian': [
                r'\b(il|la|lo|gli|le|un|una|di|da|in|con|su|per)\b',
                r'\b(io|tu|lui|lei|noi|voi|loro|sono|è|siamo|siete)\b',
                r'[àèéìíîòóù]',  # Italian accented characters
            ],
            'Portuguese': [
                r'\b(o|a|os|as|um|uma|de|em|para|com|por|do|da)\b',
                r'\b(eu|tu|ele|ela|nós|vós|eles|elas|sou|é|somos)\b',
                r'[ãâáàêéíóôõúç]',  # Portuguese accented characters
            ],
            'Russian': [
                r'[а-яё]+',  # Cyrillic characters
                r'\b(и|в|на|с|по|за|к|от|для|что|как|это)\b',
                r'\b(я|ты|он|она|мы|вы|они|есть|быть)\b',
            ]
        }
        
        self.cefr_patterns = {
            'A1': [
                r'\b(hello|good|yes|no|please|thank you)\b',  # Basic words
                r'\b(I am|my name|how are you)\b',  # Basic phrases
            ],
            'A2': [
                r'\b(because|when|where|why|how)\b',  # Question words
                r'\b(yesterday|today|tomorrow)\b',  # Time expressions
            ],
            'B1': [
                r'\b(although|however|therefore|furthermore)\b',  # Connectors
                r'\b(opinion|experience|advantage|disadvantage)\b',  # Abstract concepts
            ],
            'B2': [
                r'\b(nevertheless|consequently|moreover|furthermore)\b',  # Advanced connectors
                r'\b(hypothesis|analysis|evaluation|implementation)\b',  # Academic vocabulary
            ],
            'C1': [
                r'\b(notwithstanding|albeit|henceforth|whereby)\b',  # Complex connectors
                r'\b(paradigm|methodology|comprehensive|sophisticated)\b',  # Advanced vocabulary
            ],
            'C2': [
                r'\b(quintessential|ubiquitous|perspicacious|inexorable)\b',  # Very advanced vocabulary
                r'\b(juxtaposition|dichotomy|paradigmatic|epistemological)\b',  # Academic/literary terms
            ]
        }
    
    def detect_language(self, text: str) -> str:
        """
        Detect the primary language of the given text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Detected language name
        """
        text_lower = text.lower()
        language_scores = {}
        
        for language, patterns in self.language_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches
            
            language_scores[language] = score
        
        # Return language with highest score, default to English
        if not language_scores or max(language_scores.values()) == 0:
            return 'English'
        
        return max(language_scores, key=language_scores.get)
    
    def estimate_cefr_level(self, text: str, language: str = None) -> str:
        """
        Estimate CEFR level based on text complexity.
        
        Args:
            text: Input text to analyze
            language: Language of the text (optional)
            
        Returns:
            Estimated CEFR level (A1-C2)
        """
        # Basic complexity metrics
        word_count = len(text.split())
        sentence_count = len(re.split(r'[.!?]+', text))
        avg_word_length = sum(len(word) for word in text.split()) / max(word_count, 1)
        
        # Pattern-based level detection
        level_scores = {}
        text_lower = text.lower()
        
        for level, patterns in self.cefr_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches
            level_scores[level] = score
        
        # Complexity-based adjustment
        complexity_score = 0
        
        if avg_word_length > 6:
            complexity_score += 2
        if word_count > 20:
            complexity_score += 1
        if sentence_count > 3:
            complexity_score += 1
        
        # Determine level based on patterns and complexity
        if level_scores and max(level_scores.values()) > 0:
            pattern_level = max(level_scores, key=level_scores.get)
        else:
            pattern_level = 'A2'  # Default
        
        # Adjust based on complexity
        levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
        current_index = levels.index(pattern_level)
        
        if complexity_score >= 3:
            current_index = min(current_index + 1, len(levels) - 1)
        elif complexity_score <= 1:
            current_index = max(current_index - 1, 0)
        
        return levels[current_index]
    
    def analyze_text_features(self, text: str) -> Dict[str, any]:
        """
        Analyze various linguistic features of the text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with text analysis features
        """
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        return {
            'word_count': len(words),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'avg_word_length': sum(len(word) for word in words) / max(len(words), 1),
            'avg_sentence_length': len(words) / max(len([s for s in sentences if s.strip()]), 1),
            'unique_words': len(set(word.lower() for word in words)),
            'lexical_diversity': len(set(word.lower() for word in words)) / max(len(words), 1),
            'character_count': len(text),
            'contains_numbers': bool(re.search(r'\d', text)),
            'contains_punctuation': bool(re.search(r'[!?.,;:]', text)),
        }