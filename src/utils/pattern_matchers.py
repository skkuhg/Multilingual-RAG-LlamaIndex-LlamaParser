"""
Language Pattern Matching Utilities

Provides advanced pattern matching for multilingual content
with grammar-specific detection and cultural markers.
"""

import re
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict


class LanguagePatternMatcher:
    """
    Advanced pattern matcher for multilingual language learning content.
    
    Provides grammar pattern detection, cultural markers, and linguistic
    feature extraction for enhanced learning experiences.
    """
    
    def __init__(self):
        """Initialize the pattern matcher with language-specific rules."""
        self.grammar_patterns = {
            'Korean': {
                'honorifics': [r'습니다$', r'세요$', r'께서', r'님'],
                'particles': [r'은$', r'는$', r'이$', r'가$', r'을$', r'를$', r'에$', r'에서$'],
                'verb_endings': [r'아요$', r'어요$', r'해요$', r'ㅂ니다$', r'습니다$'],
                'tense_markers': [r'었', r'았', r'겠', r'을 것'],
                'connectives': [r'그리고', r'하지만', r'그러나', r'따라서']
            },
            'Japanese': {
                'keigo': [r'いらっしゃ', r'ござい', r'申し', r'存じ'],
                'particles': [r'は$', r'が$', r'を$', r'に$', r'で$', r'と$', r'の$'],
                'verb_forms': [r'ます$', r'だ$', r'である$', r'った$', r'いる$'],
                'adjectives': [r'い$', r'な$'],
                'counters': [r'人', r'個', r'匹', r'本', r'枚']
            },
            'Spanish': {
                'subjunctive': [r'que.*[aeiou]ra$', r'que.*[aeiou]se$', r'ojalá'],
                'ser_estar': [r'\bsoy\b', r'\beres\b', r'\bes\b', r'\bestoy\b', r'\bestás\b', r'\bestá\b'],
                'articles': [r'\bel\b', r'\bla\b', r'\blos\b', r'\blas\b'],
                'reflexive': [r'\bme\b', r'\bte\b', r'\bse\b', r'\bnos\b'],
                'diminutives': [r'ito$', r'ita$', r'illo$', r'illa$']
            },
            'French': {
                'genders': [r'\ble\b', r'\bla\b', r'\bun\b', r'\bune\b'],
                'liaisons': [r'\bt\'', r'\bd\'', r'\bn\'', r'\bs\''],
                'verb_groups': [r'er$', r'ir$', r're$'],
                'pronouns': [r'\bje\b', r'\btu\b', r'\bil\b', r'\belle\b', r'\bnous\b', r'\bvous\b'],
                'negation': [r'ne.*pas', r'ne.*jamais', r'ne.*rien']
            },
            'German': {
                'cases': [r'\bder\b', r'\bdie\b', r'\bdas\b', r'\bdem\b', r'\bden\b'],
                'separable_verbs': [r'\ban.*\b', r'\bauf.*\b', r'\baus.*\b', r'\bein.*\b'],
                'modal_verbs': [r'\bkann\b', r'\bmuss\b', r'\bwill\b', r'\bsoll\b'],
                'compound_words': [r'\w{10,}'],  # Long compound words
                'umlaut': [r'ä', r'ö', r'ü', r'ß']
            }
        }
        
        self.cultural_markers = {
            'Korean': ['안녕하세요', '감사합니다', '죄송합니다', '반갑습니다'],
            'Japanese': ['こんにちは', 'ありがとう', 'すみません', 'はじめまして'],
            'Spanish': ['hola', 'gracias', 'por favor', 'lo siento'],
            'French': ['bonjour', 'merci', 's\'il vous plaît', 'excusez-moi'],
            'German': ['hallo', 'danke', 'bitte', 'entschuldigung'],
            'Chinese': ['你好', '谢谢', '请', '对不起'],
            'Italian': ['ciao', 'grazie', 'prego', 'scusa'],
            'Portuguese': ['olá', 'obrigado', 'por favor', 'desculpa'],
            'Russian': ['привет', 'спасибо', 'пожалуйста', 'извините']
        }
    
    def find_grammar_patterns(self, text: str, language: str) -> Dict[str, List[str]]:
        """
        Find grammar patterns specific to a language.
        
        Args:
            text: Text to analyze
            language: Target language
            
        Returns:
            Dictionary of found patterns by category
        """
        if language not in self.grammar_patterns:
            return {}
        
        found_patterns = defaultdict(list)
        text_lower = text.lower()
        
        for category, patterns in self.grammar_patterns[language].items():
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                if matches:
                    found_patterns[category].extend(matches)
        
        return dict(found_patterns)
    
    def find_cultural_markers(self, text: str, language: str) -> List[str]:
        """
        Find cultural markers and common expressions.
        
        Args:
            text: Text to analyze
            language: Target language
            
        Returns:
            List of found cultural markers
        """
        if language not in self.cultural_markers:
            return []
        
        found_markers = []
        text_lower = text.lower()
        
        for marker in self.cultural_markers[language]:
            if marker.lower() in text_lower:
                found_markers.append(marker)
        
        return found_markers
    
    def analyze_sentence_structure(self, text: str, language: str) -> Dict[str, any]:
        """
        Analyze sentence structure for educational insights.
        
        Args:
            text: Text to analyze
            language: Target language
            
        Returns:
            Dictionary with structural analysis
        """
        analysis = {
            'grammar_patterns': self.find_grammar_patterns(text, language),
            'cultural_markers': self.find_cultural_markers(text, language),
            'complexity_indicators': self._assess_complexity(text, language),
            'learning_focus': self._suggest_learning_focus(text, language)
        }
        
        return analysis
    
    def _assess_complexity(self, text: str, language: str) -> Dict[str, any]:
        """
        Assess grammatical complexity of the text.
        
        Args:
            text: Text to analyze
            language: Target language
            
        Returns:
            Complexity assessment
        """
        complexity = {
            'word_count': len(text.split()),
            'sentence_length': 'short' if len(text.split()) < 10 else 'medium' if len(text.split()) < 20 else 'long',
            'grammar_density': 0,
            'cultural_content': 0
        }
        
        # Count grammar patterns
        grammar_patterns = self.find_grammar_patterns(text, language)
        complexity['grammar_density'] = sum(len(patterns) for patterns in grammar_patterns.values())
        
        # Count cultural markers
        cultural_markers = self.find_cultural_markers(text, language)
        complexity['cultural_content'] = len(cultural_markers)
        
        return complexity
    
    def _suggest_learning_focus(self, text: str, language: str) -> List[str]:
        """
        Suggest learning focus areas based on text content.
        
        Args:
            text: Text to analyze
            language: Target language
            
        Returns:
            List of suggested focus areas
        """
        suggestions = []
        grammar_patterns = self.find_grammar_patterns(text, language)
        
        # Language-specific suggestions
        if language == 'Korean':
            if 'honorifics' in grammar_patterns:
                suggestions.append('Korean honorific system')
            if 'particles' in grammar_patterns:
                suggestions.append('Korean particles usage')
        
        elif language == 'Japanese':
            if 'keigo' in grammar_patterns:
                suggestions.append('Japanese keigo (polite language)')
            if 'particles' in grammar_patterns:
                suggestions.append('Japanese particle system')
        
        elif language == 'Spanish':
            if 'subjunctive' in grammar_patterns:
                suggestions.append('Spanish subjunctive mood')
            if 'ser_estar' in grammar_patterns:
                suggestions.append('Ser vs. Estar distinction')
        
        elif language == 'French':
            if 'genders' in grammar_patterns:
                suggestions.append('French gender agreement')
            if 'liaisons' in grammar_patterns:
                suggestions.append('French liaison rules')
        
        elif language == 'German':
            if 'cases' in grammar_patterns:
                suggestions.append('German case system')
            if 'separable_verbs' in grammar_patterns:
                suggestions.append('German separable verbs')
        
        return suggestions
    
    def extract_vocabulary_items(self, text: str, language: str) -> List[Dict[str, str]]:
        """
        Extract vocabulary items with context for learning.
        
        Args:
            text: Text to analyze
            language: Target language
            
        Returns:
            List of vocabulary items with metadata
        """
        vocab_items = []
        words = text.split()
        
        for i, word in enumerate(words):
            # Clean word
            clean_word = re.sub(r'[^\w]', '', word.lower())
            
            if len(clean_word) > 2:  # Skip very short words
                context_start = max(0, i - 3)
                context_end = min(len(words), i + 4)
                context = ' '.join(words[context_start:context_end])
                
                vocab_item = {
                    'word': clean_word,
                    'original_form': word,
                    'context': context,
                    'position': i,
                    'language': language
                }
                
                # Add grammar information if available
                grammar_info = self._get_word_grammar_info(word, language)
                if grammar_info:
                    vocab_item.update(grammar_info)
                
                vocab_items.append(vocab_item)
        
        return vocab_items
    
    def _get_word_grammar_info(self, word: str, language: str) -> Dict[str, str]:
        """
        Get grammatical information about a word.
        
        Args:
            word: Word to analyze
            language: Target language
            
        Returns:
            Grammar information dictionary
        """
        grammar_info = {}
        word_lower = word.lower()
        
        if language == 'Korean':
            if any(re.search(pattern, word_lower) for pattern in ['습니다$', '세요$']):
                grammar_info['form'] = 'polite_ending'
            elif any(re.search(pattern, word_lower) for pattern in ['아요$', '어요$']):
                grammar_info['form'] = 'informal_polite'
        
        elif language == 'Spanish':
            if word_lower.endswith(('ar', 'er', 'ir')):
                grammar_info['form'] = 'infinitive'
            elif word_lower.endswith(('ando', 'iendo')):
                grammar_info['form'] = 'gerund'
        
        elif language == 'French':
            if word_lower.endswith('er'):
                grammar_info['form'] = 'infinitive_1st_group'
            elif word_lower.endswith('ir'):
                grammar_info['form'] = 'infinitive_2nd_group'
        
        return grammar_info