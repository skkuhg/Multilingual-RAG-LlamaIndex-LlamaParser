"""
Spaced Repetition System (SRS) Scheduler

Implements the SM-2 algorithm for optimal learning scheduling
with Anki-compatible export functionality.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json


class SRSScheduler:
    """
    Implements spaced repetition scheduling using the SM-2 algorithm.
    
    Provides Anki-style learning intervals with adaptive difficulty adjustment
    based on recall quality and performance metrics.
    """
    
    def __init__(self, initial_interval: int = 1, easy_bonus: float = 1.3, hard_penalty: float = 1.2):
        """
        Initialize the SRS scheduler.
        
        Args:
            initial_interval: Initial review interval in days
            easy_bonus: Multiplier for easy responses
            hard_penalty: Penalty factor for hard responses
        """
        self.initial_interval = initial_interval
        self.easy_bonus = easy_bonus
        self.hard_penalty = hard_penalty
        self.min_ease_factor = 1.3
        self.default_ease_factor = 2.5
    
    def initialize_srs_metadata(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Initialize SRS metadata for new cards.
        
        Args:
            df: DataFrame with learning content
            
        Returns:
            DataFrame with SRS metadata added
        """
        df_srs = df.copy()
        
        # Add SRS columns
        df_srs['card_id'] = df_srs.index
        df_srs['interval'] = self.initial_interval
        df_srs['ease_factor'] = self.default_ease_factor
        df_srs['repetitions'] = 0
        df_srs['last_review'] = None
        df_srs['next_review'] = datetime.now().date()
        df_srs['quality_history'] = ''
        df_srs['total_reviews'] = 0
        df_srs['total_time_spent'] = 0.0
        df_srs['avg_quality'] = 0.0
        df_srs['card_status'] = 'new'  # new, learning, review, graduated
        
        return df_srs
    
    def update_srs(self, card_id: int, quality: int, response_time: float = 0.0) -> Dict[str, Any]:
        """
        Update SRS parameters based on review quality.
        
        Args:
            card_id: Unique card identifier
            quality: Quality of response (0-5 scale)
            response_time: Time taken to respond in seconds
            
        Returns:
            Updated SRS parameters
        """
        # Validate quality score
        quality = max(0, min(5, quality))
        
        # Calculate new parameters using SM-2 algorithm
        if quality >= 3:  # Correct response
            if hasattr(self, 'cards') and card_id in self.cards:
                card = self.cards[card_id]
                
                if card['repetitions'] == 0:
                    interval = 1
                elif card['repetitions'] == 1:
                    interval = 6
                else:
                    interval = round(card['interval'] * card['ease_factor'])
                
                repetitions = card['repetitions'] + 1
            else:
                interval = 1
                repetitions = 1
            
            # Update ease factor
            ease_factor = self.default_ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
            ease_factor = max(self.min_ease_factor, ease_factor)
            
        else:  # Incorrect response
            interval = 1
            repetitions = 0
            ease_factor = max(self.min_ease_factor, 
                            self.default_ease_factor - 0.2)
        
        # Calculate next review date
        next_review = datetime.now().date() + timedelta(days=interval)
        
        return {
            'interval': interval,
            'ease_factor': ease_factor,
            'repetitions': repetitions,
            'last_review': datetime.now().date(),
            'next_review': next_review,
            'quality': quality,
            'response_time': response_time
        }
    
    def get_due_cards(self, df_srs: pd.DataFrame, date: datetime.date = None) -> pd.DataFrame:
        """
        Get cards that are due for review.
        
        Args:
            df_srs: DataFrame with SRS metadata
            date: Date to check (default: today)
            
        Returns:
            DataFrame with due cards
        """
        if date is None:
            date = datetime.now().date()
        
        # Convert next_review to date if it's a string
        df_srs['next_review'] = pd.to_datetime(df_srs['next_review']).dt.date
        
        due_cards = df_srs[df_srs['next_review'] <= date]
        
        # Sort by priority (overdue first, then by difficulty)
        due_cards = due_cards.sort_values(['next_review', 'ease_factor'])
        
        return due_cards
    
    def get_learning_statistics(self, df_srs: pd.DataFrame) -> Dict[str, Any]:
        """
        Get comprehensive learning statistics.
        
        Args:
            df_srs: DataFrame with SRS metadata
            
        Returns:
            Dictionary with learning statistics
        """
        total_cards = len(df_srs)
        new_cards = len(df_srs[df_srs['card_status'] == 'new'])
        learning_cards = len(df_srs[df_srs['card_status'] == 'learning'])
        review_cards = len(df_srs[df_srs['card_status'] == 'review'])
        
        due_today = len(self.get_due_cards(df_srs))
        
        # Language statistics
        language_stats = df_srs['language'].value_counts().to_dict() if 'language' in df_srs.columns else {}
        
        # Level statistics
        level_stats = df_srs['cefr_level'].value_counts().to_dict() if 'cefr_level' in df_srs.columns else {}
        
        return {
            'total_cards': total_cards,
            'new_cards': new_cards,
            'learning_cards': learning_cards,
            'review_cards': review_cards,
            'due_today': due_today,
            'languages': language_stats,
            'levels': level_stats,
            'avg_ease_factor': df_srs['ease_factor'].mean() if len(df_srs) > 0 else 0,
            'avg_interval': df_srs['interval'].mean() if len(df_srs) > 0 else 0
        }
    
    def export_to_anki_format(self, df_srs: pd.DataFrame, output_file: str, max_cards: int = None) -> None:
        """
        Export cards to Anki-compatible format.
        
        Args:
            df_srs: DataFrame with cards to export
            output_file: Output file path
            max_cards: Maximum number of cards to export
        """
        export_df = df_srs.copy()
        
        if max_cards:
            export_df = export_df.head(max_cards)
        
        # Create Anki format (tab-separated)
        anki_lines = []
        
        for _, row in export_df.iterrows():
            front = row['text']
            back = f"Language: {row.get('language', 'Unknown')}<br>Level: {row.get('cefr_level', 'Unknown')}"
            
            if 'translation' in row and pd.notna(row['translation']):
                back += f"<br>Translation: {row['translation']}"
            
            if 'context' in row and pd.notna(row['context']):
                back += f"<br>Context: {row['context'][:100]}..."
            
            # Add tags
            tags = []
            if 'language' in row:
                tags.append(row['language'])
            if 'cefr_level' in row:
                tags.append(row['cefr_level'])
            
            tag_string = ' '.join(tags) if tags else ''
            
            anki_line = f"{front}\t{back}\t{tag_string}"
            anki_lines.append(anki_line)
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(anki_lines))
        
        print(f"Exported {len(anki_lines)} cards to {output_file}")
    
    def suggest_study_session(self, df_srs: pd.DataFrame, target_minutes: int = 20) -> Dict[str, Any]:
        """
        Suggest an optimal study session based on due cards and time available.
        
        Args:
            df_srs: DataFrame with SRS metadata
            target_minutes: Target study time in minutes
            
        Returns:
            Study session recommendations
        """
        due_cards = self.get_due_cards(df_srs)
        
        # Estimate time per card (average 30 seconds)
        estimated_time_per_card = 0.5  # minutes
        max_cards = int(target_minutes / estimated_time_per_card)
        
        # Prioritize cards
        session_cards = due_cards.head(max_cards)
        
        return {
            'recommended_cards': len(session_cards),
            'estimated_time': len(session_cards) * estimated_time_per_card,
            'card_breakdown': {
                'new': len(session_cards[session_cards['card_status'] == 'new']),
                'review': len(session_cards[session_cards['card_status'] == 'review']),
                'learning': len(session_cards[session_cards['card_status'] == 'learning'])
            },
            'languages': session_cards['language'].value_counts().to_dict() if 'language' in session_cards.columns else {}
        }