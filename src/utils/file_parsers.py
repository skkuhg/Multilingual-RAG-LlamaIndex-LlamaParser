"""
Enhanced File Parsing Utilities

Provides specialized parsers for different file formats with enhanced
metadata extraction and error handling.
"""

import re
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime


class EnhancedFileParser:
    """
    Enhanced file parser with format-specific optimizations.
    
    Provides specialized parsing for educational content with improved
    error handling and metadata preservation.
    """
    
    def __init__(self):
        """Initialize the enhanced file parser."""
        self.supported_formats = {
            '.txt': self.parse_text_file,
            '.md': self.parse_markdown_file,
            '.html': self.parse_html_file,
            '.srt': self.parse_srt_file,
            '.vtt': self.parse_vtt_file,
            '.json': self.parse_json_file,
            '.csv': self.parse_csv_file
        }
    
    def parse_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Parse file based on its extension.
        
        Args:
            file_path: Path to the file to parse
            
        Returns:
            List of parsed content dictionaries
        """
        extension = file_path.suffix.lower()
        
        if extension in self.supported_formats:
            return self.supported_formats[extension](file_path)
        else:
            return self.parse_text_file(file_path)
    
    def parse_text_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Parse plain text files with enhanced sentence detection.
        
        Args:
            file_path: Path to text file
            
        Returns:
            List of parsed sentences with metadata
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Enhanced sentence splitting for multiple languages
            sentences = self._split_sentences(content)
            
            parsed_content = []
            for i, sentence in enumerate(sentences):
                if len(sentence.strip()) > 5:
                    parsed_content.append({
                        'text': sentence.strip(),
                        'sentence_index': i,
                        'file_type': 'text',
                        'parsing_method': 'enhanced_text'
                    })
            
            return parsed_content
            
        except Exception as e:
            print(f"Error parsing text file {file_path}: {e}")
            return []
    
    def parse_markdown_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Parse Markdown files with structure preservation.
        
        Args:
            file_path: Path to Markdown file
            
        Returns:
            List of parsed content with Markdown structure
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parsed_content = []
            lines = content.split('\n')
            current_section = ""
            
            for line_num, line in enumerate(lines):
                line = line.strip()
                
                # Track section headers
                if line.startswith('#'):
                    current_section = line
                    continue
                
                # Process non-empty lines
                if line and not line.startswith('#'):
                    # Remove Markdown formatting for clean text
                    clean_text = re.sub(r'[*_`]', '', line)
                    clean_text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean_text)
                    
                    if len(clean_text) > 5:
                        parsed_content.append({
                            'text': clean_text,
                            'line_number': line_num,
                            'section': current_section,
                            'file_type': 'markdown',
                            'parsing_method': 'markdown_structure'
                        })
            
            return parsed_content
            
        except Exception as e:
            print(f"Error parsing Markdown file {file_path}: {e}")
            return []
    
    def parse_html_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Parse HTML files with tag-aware text extraction.
        
        Args:
            file_path: Path to HTML file
            
        Returns:
            List of parsed content from HTML
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove HTML tags but preserve text
            clean_text = re.sub(r'<[^>]+>', ' ', content)
            clean_text = re.sub(r'\s+', ' ', clean_text)
            
            sentences = self._split_sentences(clean_text)
            
            parsed_content = []
            for i, sentence in enumerate(sentences):
                if len(sentence.strip()) > 5:
                    parsed_content.append({
                        'text': sentence.strip(),
                        'sentence_index': i,
                        'file_type': 'html',
                        'parsing_method': 'html_tag_removal'
                    })
            
            return parsed_content
            
        except Exception as e:
            print(f"Error parsing HTML file {file_path}: {e}")
            return []
    
    def parse_srt_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Parse SRT subtitle files with timestamp preservation.
        
        Args:
            file_path: Path to SRT file
            
        Returns:
            List of subtitle entries with timestamps
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse SRT format
            entries = re.split(r'\n\s*\n', content)
            parsed_content = []
            
            for entry in entries:
                lines = entry.strip().split('\n')
                if len(lines) >= 3:
                    subtitle_id = lines[0]
                    timestamp = lines[1]
                    subtitle_text = ' '.join(lines[2:])
                    
                    if len(subtitle_text) > 5:
                        parsed_content.append({
                            'text': subtitle_text,
                            'subtitle_id': subtitle_id,
                            'timestamp': timestamp,
                            'file_type': 'srt',
                            'parsing_method': 'srt_structure'
                        })
            
            return parsed_content
            
        except Exception as e:
            print(f"Error parsing SRT file {file_path}: {e}")
            return []
    
    def parse_vtt_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Parse VTT subtitle files.
        
        Args:
            file_path: Path to VTT file
            
        Returns:
            List of subtitle entries
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parsed_content = []
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                # Skip VTT headers and timestamps
                if (line and 
                    not line.startswith('WEBVTT') and 
                    '-->' not in line and 
                    not line.isdigit()):
                    
                    if len(line) > 5:
                        parsed_content.append({
                            'text': line,
                            'file_type': 'vtt',
                            'parsing_method': 'vtt_line_extraction'
                        })
            
            return parsed_content
            
        except Exception as e:
            print(f"Error parsing VTT file {file_path}: {e}")
            return []
    
    def parse_json_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Parse JSON files with intelligent text extraction.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            List of extracted text content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return self._extract_text_from_json(data)
            
        except Exception as e:
            print(f"Error parsing JSON file {file_path}: {e}")
            return []
    
    def parse_csv_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Parse CSV files with automatic structure detection.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of extracted content from CSV
        """
        try:
            # Try different encodings
            for encoding in ['utf-8', 'utf-8-sig', 'latin-1']:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                print(f"Could not decode CSV file {file_path}")
                return []
            
            parsed_content = []
            
            # Auto-detect content structure
            text_columns = [col for col in df.columns if df[col].dtype == 'object']
            
            for _, row in df.iterrows():
                for col in text_columns:
                    text = str(row[col])
                    if text and text != 'nan' and len(text) > 5:
                        parsed_content.append({
                            'text': text,
                            'column': col,
                            'file_type': 'csv',
                            'parsing_method': 'csv_column_extraction'
                        })
            
            return parsed_content
            
        except Exception as e:
            print(f"Error parsing CSV file {file_path}: {e}")
            return []
    
    def _split_sentences(self, text: str) -> List[str]:
        """
        Enhanced sentence splitting for multiple languages.
        
        Args:
            text: Input text to split
            
        Returns:
            List of sentences
        """
        # Enhanced pattern for multiple languages
        sentence_endings = r'[.!?。！？]+(?:\s+|$)'
        sentences = re.split(sentence_endings, text)
        
        # Clean and filter sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 5:
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def _extract_text_from_json(self, obj: Any, path: str = "") -> List[Dict[str, Any]]:
        """
        Recursively extract text from JSON structure.
        
        Args:
            obj: JSON object to process
            path: Current path in the JSON structure
            
        Returns:
            List of extracted text entries
        """
        extracted = []
        
        if isinstance(obj, str) and len(obj) > 5:
            extracted.append({
                'text': obj,
                'json_path': path,
                'file_type': 'json',
                'parsing_method': 'json_recursive_extraction'
            })
        
        elif isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}" if path else key
                extracted.extend(self._extract_text_from_json(value, new_path))
        
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                extracted.extend(self._extract_text_from_json(item, new_path))
        
        return extracted