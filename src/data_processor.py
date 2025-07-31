"""
Data Processing Module

Handles ingestion and processing of various file formats for language learning content.
Supports text files, subtitles, structured data, and more.
"""

import os
import re
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

from .language_detector import LanguageDetector
from .rag_system import Document


class DataProcessor:
    """
    Handles data ingestion and processing for multilingual content.
    
    Supports multiple file formats and preserves contextual information
    for enhanced language learning experiences.
    """
    
    def __init__(self):
        """Initialize the data processor."""
        self.language_detector = LanguageDetector()
        self.supported_extensions = {'.txt', '.html', '.md', '.srt', '.vtt', '.json', '.csv', '.rtf'}
    
    def ingest_data_files(self, data_folder: str = "data") -> pd.DataFrame:
        """
        Ingest data files from the specified folder.
        
        Args:
            data_folder: Path to the data folder
            
        Returns:
            DataFrame containing processed sentences with metadata
        """
        sentences_data = []
        data_path = Path(data_folder)
        
        if not data_path.exists():
            print(f"❌ Data folder '{data_folder}' not found!")
            return pd.DataFrame()
        
        # Find all supported files
        files_found = []
        for ext in self.supported_extensions:
            files_found.extend(data_path.rglob(f"*{ext}"))
        
        print(f"📁 Found {len(files_found)} files to process...")
        
        total_chars_processed = 0
        for file_path in files_found:
            print(f"\\n📄 Processing: {file_path.name} ({file_path.stat().st_size:,} bytes)")
            
            try:
                # Get file-level metadata
                file_metadata = self._get_file_metadata(file_path, data_path)
                
                # Process file based on type
                documents = self._process_file(file_path)
                
                # Process all documents from this file
                file_sentences_count = 0
                for doc_data in documents:
                    if not isinstance(doc_data, dict) or 'text' not in doc_data:
                        continue
                    
                    text = doc_data['text'].strip()
                    if len(text) < 5:  # Skip very short texts
                        continue
                    
                    # Detect language and estimate level
                    language = self.language_detector.detect_language(text)
                    cefr_level = self.language_detector.estimate_cefr_level(text, language)
                    
                    # Create comprehensive sentence data
                    sentence_data = {
                        'text': text,
                        'language': language,
                        'cefr_level': cefr_level,
                        'emoji': self._get_language_emoji(language),
                        **file_metadata,
                        **doc_data
                    }
                    
                    sentences_data.append(sentence_data)
                    file_sentences_count += 1
                    total_chars_processed += len(text)
                
                print(f"   ✅ Extracted {file_sentences_count} sentences/entries")
                
            except Exception as e:
                print(f"❌ Error processing {file_path.name}: {str(e)}")
                continue
        
        df_raw = pd.DataFrame(sentences_data)
        self._print_ingestion_summary(df_raw, files_found, total_chars_processed)
        return df_raw
    
    def _get_file_metadata(self, file_path: Path, data_path: Path) -> Dict[str, Any]:
        """Get metadata for a file."""
        file_stats = file_path.stat()
        return {
            'source_file': str(file_path),
            'file_name': file_path.name,
            'file_size': file_stats.st_size,
            'file_type': file_path.suffix.lower(),
            'relative_path': str(file_path.relative_to(data_path)),
            'folder': file_path.parent.name,
            'modified_time': datetime.fromtimestamp(file_stats.st_mtime).isoformat()
        }
    
    def _process_file(self, file_path: Path) -> List[Dict]:
        """Process a file based on its type."""
        if file_path.suffix == '.csv':
            return self._parse_csv(file_path)
        elif file_path.suffix == '.json':
            return self._parse_json(file_path)
        elif file_path.suffix in {'.srt', '.vtt'}:
            return self._parse_subtitles(file_path)
        else:
            return self._parse_text(file_path)
    
    def _parse_text(self, file_path: Path) -> List[Dict]:
        """Parse text files (txt, html, md, rtf)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = content.strip()
            if not content:
                return []
            
            # Split into paragraphs first to preserve structure
            paragraphs = [p.strip() for p in content.split('\\n\\n') if p.strip()]
            if not paragraphs:
                paragraphs = [p.strip() for p in content.split('\\n') if p.strip()]
            
            documents = []
            for para_idx, paragraph in enumerate(paragraphs):
                # Enhanced sentence splitting for multiple languages
                sentence_endings = r'[.!?。¡¿]+(?:\\s+|$)'
                sentences = re.split(sentence_endings, paragraph)
                
                for sent_idx, sentence in enumerate(sentences):
                    sentence = sentence.strip()
                    if len(sentence) < 5:
                        continue
                    
                    doc_data = {
                        'text': sentence,
                        'paragraph_index': para_idx,
                        'sentence_index': sent_idx,
                        'paragraph_context': paragraph[:200] + '...' if len(paragraph) > 200 else paragraph,
                        'file_size': len(content),
                        'total_paragraphs': len(paragraphs)
                    }
                    documents.append(doc_data)
            
            return documents
            
        except Exception as e:
            print(f"Error parsing text file {file_path}: {e}")
            return []
    
    def _parse_csv(self, file_path: Path) -> List[Dict]:
        """Parse CSV files with various structures."""
        try:
            # Try different encodings
            encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                print(f"Could not read CSV file {file_path} with any encoding")
                return []
            
            documents = []
            
            # Handle different CSV structures
            if 'word' in df.columns and 'translation' in df.columns:
                # Vocabulary list format
                for idx, row in df.iterrows():
                    word = str(row.get('word', ''))
                    translation = str(row.get('translation', ''))
                    
                    if word and word != 'nan':
                        doc_data = {
                            'text': f"{word} - {translation}",
                            'word': word,
                            'translation': translation,
                            'row_index': idx,
                            'csv_type': 'vocabulary'
                        }
                        documents.append(doc_data)
                        
            elif 'text' in df.columns or 'sentence' in df.columns:
                # Sentence list format
                text_col = 'text' if 'text' in df.columns else 'sentence'
                
                for idx, row in df.iterrows():
                    text = str(row.get(text_col, ''))
                    if text and text != 'nan' and len(text) > 5:
                        doc_data = {
                            'text': text,
                            'row_index': idx,
                            'csv_type': 'sentences'
                        }
                        
                        # Add any additional columns as metadata
                        for col in df.columns:
                            if col != text_col:
                                doc_data[col] = row.get(col)
                        
                        documents.append(doc_data)
            else:
                # Generic CSV - use first text-like column
                for col in df.columns:
                    if df[col].dtype == 'object':  # Text column
                        for idx, row in df.iterrows():
                            text = str(row.get(col, ''))
                            if text and text != 'nan' and len(text) > 5:
                                doc_data = {
                                    'text': text,
                                    'row_index': idx,
                                    'csv_type': 'generic',
                                    'source_column': col
                                }
                                documents.append(doc_data)
                        break
            
            return documents
            
        except Exception as e:
            print(f"Error parsing CSV file {file_path}: {e}")
            return []
    
    def _parse_json(self, file_path: Path) -> List[Dict]:
        """Parse JSON files with various structures."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            documents = []
            
            if isinstance(data, list):
                # List of objects/messages
                for idx, item in enumerate(data):
                    if isinstance(item, dict):
                        # Extract text from various possible fields
                        text_fields = ['content', 'text', 'message', 'sentence', 'body']
                        text = None
                        
                        for field in text_fields:
                            if field in item and item[field]:
                                text = str(item[field])
                                break
                        
                        if text and len(text) > 5:
                            doc_data = {
                                'text': text,
                                'json_index': idx,
                                'json_type': 'list_item'
                            }
                            
                            # Add other fields as metadata
                            for key, value in item.items():
                                if key not in text_fields:
                                    doc_data[key] = value
                            
                            documents.append(doc_data)
                            
                    elif isinstance(item, str) and len(item) > 5:
                        # Simple string list
                        doc_data = {
                            'text': item,
                            'json_index': idx,
                            'json_type': 'string_list'
                        }
                        documents.append(doc_data)
                        
            elif isinstance(data, dict):
                # Dictionary structure
                documents = self._extract_from_dict(data)
            
            return documents
            
        except Exception as e:
            print(f"Error parsing JSON file {file_path}: {e}")
            return []
    
    def _extract_from_dict(self, obj: Dict, prefix: str = "") -> List[Dict]:
        """Extract text from nested dictionary structure."""
        texts = []
        
        for key, value in obj.items():
            current_key = f"{prefix}.{key}" if prefix else key
            
            if isinstance(value, str) and len(value) > 5:
                texts.append({
                    'text': value,
                    'json_key': current_key,
                    'json_type': 'dict_value'
                })
            elif isinstance(value, dict):
                texts.extend(self._extract_from_dict(value, current_key))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, str) and len(item) > 5:
                        texts.append({
                            'text': item,
                            'json_key': f"{current_key}[{i}]",
                            'json_type': 'dict_list_item'
                        })
        
        return texts
    
    def _parse_subtitles(self, file_path: Path) -> List[Dict]:
        """Parse subtitle files (SRT, VTT)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            documents = []
            
            if file_path.suffix == '.srt':
                # SRT format parsing
                blocks = re.split(r'\\n\\s*\\n', content)
                
                for block_idx, block in enumerate(blocks):
                    lines = block.strip().split('\\n')
                    if len(lines) >= 3:  # Index, time, text
                        subtitle_text = ' '.join(lines[2:])  # Join all text lines
                        
                        if len(subtitle_text) > 5:
                            documents.append({
                                'text': subtitle_text,
                                'subtitle_index': block_idx,
                                'timestamp': lines[1] if len(lines) > 1 else None,
                                'subtitle_format': 'srt'
                            })
            else:
                # VTT format - simpler parsing
                lines = content.split('\\n')
                
                for line_idx, line in enumerate(lines):
                    line = line.strip()
                    if line and not line.startswith('WEBVTT') and '-->' not in line and not line.isdigit():
                        if len(line) > 5:
                            documents.append({
                                'text': line,
                                'subtitle_index': line_idx,
                                'subtitle_format': 'vtt'
                            })
            
            return documents
            
        except Exception as e:
            print(f"Error parsing subtitle file {file_path}: {e}")
            return []
    
    def _get_language_emoji(self, language: str) -> str:
        """Get appropriate emoji for language."""
        emoji_map = {
            'Korean': '🇰🇷',
            'Japanese': '🇯🇵',
            'Chinese': '🇨🇳',
            'Spanish': '🇪🇸',
            'French': '🇫🇷',
            'German': '🇩🇪',
            'English': '🇺🇸',
            'Italian': '🇮🇹',
            'Portuguese': '🇵🇹',
            'Russian': '🇷🇺'
        }
        return emoji_map.get(language, '📄')
    
    def _print_ingestion_summary(self, df_raw: pd.DataFrame, files_found: List[Path],
                                total_chars_processed: int) -> None:
        """Print summary of data ingestion."""
        print(f"\\n🎉 Processing complete!")
        print(f"📊 Total sentences/entries: {len(df_raw):,}")
        print(f"📝 Total characters processed: {total_chars_processed:,}")
        print(f"📁 Files processed: {len(files_found)}")
        
        if not df_raw.empty:
            print(f"\\n📊 Language distribution:")
            lang_counts = df_raw['language'].value_counts()
            for lang, count in lang_counts.items():
                print(f"  • {lang}: {count:,} sentences")
            
            print(f"\\n📊 CEFR level distribution:")
            level_counts = df_raw['cefr_level'].value_counts()
            for level, count in level_counts.items():
                print(f"  • {level}: {count:,} sentences")
            
            print(f"\\n📊 File type distribution:")
            type_counts = df_raw['file_type'].value_counts()
            for file_type, count in type_counts.items():
                print(f"  • {file_type}: {count:,} entries")
    
    def create_documents(self, df: pd.DataFrame) -> List[Document]:
        """
        Convert DataFrame to Document objects for RAG system.
        
        Args:
            df: DataFrame with processed text data
            
        Returns:
            List of Document objects
        """
        documents = []
        
        for _, row in df.iterrows():
            # Create metadata from all columns except text
            metadata = {key: value for key, value in row.items() if key != 'text'}
            
            # Create Document object
            doc = Document(text=row['text'], metadata=metadata)
            documents.append(doc)
        
        return documents