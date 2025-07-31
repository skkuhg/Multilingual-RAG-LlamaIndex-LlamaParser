"""
Export Helper Utilities

Provides export functionality for various learning platforms
including Anki, Quizlet, and custom formats.
"""

import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd


class ExportHelper:
    """
    Helper class for exporting learning content to various formats.
    
    Supports multiple learning platforms and custom export formats
    with flexible template systems.
    """
    
    def __init__(self):
        """Initialize the export helper."""
        self.supported_formats = {
            'anki': self.export_to_anki,
            'quizlet': self.export_to_quizlet,
            'csv': self.export_to_csv,
            'json': self.export_to_json,
            'xml': self.export_to_xml,
            'mnemosyne': self.export_to_mnemosyne
        }
    
    def export_data(self, data: pd.DataFrame, format_type: str, output_path: str, **kwargs) -> bool:
        """
        Export data to specified format.
        
        Args:
            data: DataFrame with learning content
            format_type: Export format type
            output_path: Output file path
            **kwargs: Additional format-specific options
            
        Returns:
            Success status
        """
        if format_type not in self.supported_formats:
            print(f"Unsupported format: {format_type}")
            return False
        
        try:
            return self.supported_formats[format_type](data, output_path, **kwargs)
        except Exception as e:
            print(f"Error exporting to {format_type}: {e}")
            return False
    
    def export_to_anki(self, data: pd.DataFrame, output_path: str, 
                      front_field: str = 'text', back_fields: List[str] = None,
                      tag_fields: List[str] = None) -> bool:
        """
        Export to Anki-compatible format.
        
        Args:
            data: DataFrame with learning content
            output_path: Output file path
            front_field: Field to use for card front
            back_fields: Fields to use for card back
            tag_fields: Fields to use for tags
            
        Returns:
            Success status
        """
        if back_fields is None:
            back_fields = ['language', 'cefr_level']
        if tag_fields is None:
            tag_fields = ['language', 'cefr_level']
        
        anki_cards = []
        
        for _, row in data.iterrows():
            # Front of card
            front = str(row.get(front_field, ''))
            
            # Back of card
            back_parts = []
            for field in back_fields:
                if field in row and pd.notna(row[field]):
                    back_parts.append(f"{field.title()}: {row[field]}")
            
            if 'translation' in row and pd.notna(row['translation']):
                back_parts.append(f"Translation: {row['translation']}")
            
            back = '<br>'.join(back_parts)
            
            # Tags
            tags = []
            for field in tag_fields:
                if field in row and pd.notna(row[field]):
                    tag_value = str(row[field]).replace(' ', '_')
                    tags.append(tag_value)
            
            tag_string = ' '.join(tags)
            
            # Create Anki line (tab-separated)
            anki_line = f"{front}\t{back}\t{tag_string}"
            anki_cards.append(anki_line)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(anki_cards))
        
        print(f"Exported {len(anki_cards)} cards to Anki format: {output_path}")
        return True
    
    def export_to_quizlet(self, data: pd.DataFrame, output_path: str,
                         term_field: str = 'text', definition_fields: List[str] = None) -> bool:
        """
        Export to Quizlet-compatible CSV format.
        
        Args:
            data: DataFrame with learning content
            output_path: Output file path
            term_field: Field to use for terms
            definition_fields: Fields to use for definitions
            
        Returns:
            Success status
        """
        if definition_fields is None:
            definition_fields = ['translation', 'language']
        
        quizlet_data = []
        
        for _, row in data.iterrows():
            term = str(row.get(term_field, ''))
            
            # Build definition
            definition_parts = []
            for field in definition_fields:
                if field in row and pd.notna(row[field]):
                    definition_parts.append(str(row[field]))
            
            definition = ' | '.join(definition_parts)
            
            quizlet_data.append({
                'Term': term,
                'Definition': definition
            })
        
        # Write to CSV
        quizlet_df = pd.DataFrame(quizlet_data)
        quizlet_df.to_csv(output_path, index=False, encoding='utf-8')
        
        print(f"Exported {len(quizlet_data)} terms to Quizlet format: {output_path}")
        return True
    
    def export_to_csv(self, data: pd.DataFrame, output_path: str,
                     selected_columns: List[str] = None) -> bool:
        """
        Export to standard CSV format.
        
        Args:
            data: DataFrame with learning content
            output_path: Output file path
            selected_columns: Columns to include in export
            
        Returns:
            Success status
        """
        export_data = data.copy()
        
        if selected_columns:
            available_columns = [col for col in selected_columns if col in export_data.columns]
            export_data = export_data[available_columns]
        
        export_data.to_csv(output_path, index=False, encoding='utf-8')
        
        print(f"Exported {len(export_data)} rows to CSV: {output_path}")
        return True
    
    def export_to_json(self, data: pd.DataFrame, output_path: str,
                      format_type: str = 'records') -> bool:
        """
        Export to JSON format.
        
        Args:
            data: DataFrame with learning content
            output_path: Output file path
            format_type: JSON format ('records', 'index', 'values')
            
        Returns:
            Success status
        """
        # Add export metadata
        export_structure = {
            'metadata': {
                'export_date': datetime.now().isoformat(),
                'total_entries': len(data),
                'languages': data['language'].value_counts().to_dict() if 'language' in data.columns else {},
                'format_version': '1.0'
            },
            'data': data.to_dict(orient=format_type)
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_structure, f, ensure_ascii=False, indent=2)
        
        print(f"Exported {len(data)} entries to JSON: {output_path}")
        return True
    
    def export_to_xml(self, data: pd.DataFrame, output_path: str,
                     root_element: str = 'language_learning_data') -> bool:
        """
        Export to XML format.
        
        Args:
            data: DataFrame with learning content
            output_path: Output file path
            root_element: Root XML element name
            
        Returns:
            Success status
        """
        root = ET.Element(root_element)
        
        # Add metadata
        metadata = ET.SubElement(root, 'metadata')
        ET.SubElement(metadata, 'export_date').text = datetime.now().isoformat()
        ET.SubElement(metadata, 'total_entries').text = str(len(data))
        
        # Add entries
        entries = ET.SubElement(root, 'entries')
        
        for _, row in data.iterrows():
            entry = ET.SubElement(entries, 'entry')
            
            for column, value in row.items():
                if pd.notna(value):
                    element = ET.SubElement(entry, column.replace(' ', '_'))
                    element.text = str(value)
        
        # Write to file
        tree = ET.ElementTree(root)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)
        
        print(f"Exported {len(data)} entries to XML: {output_path}")
        return True
    
    def export_to_mnemosyne(self, data: pd.DataFrame, output_path: str) -> bool:
        """
        Export to Mnemosyne format.
        
        Args:
            data: DataFrame with learning content
            output_path: Output file path
            
        Returns:
            Success status
        """
        mnemosyne_cards = []
        
        for _, row in data.iterrows():
            question = str(row.get('text', ''))
            answer = f"Language: {row.get('language', '')}, Level: {row.get('cefr_level', '')}"
            
            if 'translation' in row and pd.notna(row['translation']):
                answer += f", Translation: {row['translation']}"
            
            # Mnemosyne format: question<tab>answer
            mnemosyne_line = f"{question}\t{answer}"
            mnemosyne_cards.append(mnemosyne_line)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(mnemosyne_cards))
        
        print(f"Exported {len(mnemosyne_cards)} cards to Mnemosyne format: {output_path}")
        return True
    
    def create_study_package(self, data: pd.DataFrame, output_dir: str,
                           package_name: str = 'language_learning_package') -> bool:
        """
        Create a comprehensive study package with multiple formats.
        
        Args:
            data: DataFrame with learning content
            output_dir: Output directory
            package_name: Name of the package
            
        Returns:
            Success status
        """
        output_path = Path(output_dir) / package_name
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Export to multiple formats
        formats_to_export = {
            'anki': f"{package_name}_anki.txt",
            'quizlet': f"{package_name}_quizlet.csv",
            'json': f"{package_name}_data.json",
            'csv': f"{package_name}_full.csv"
        }
        
        success_count = 0
        for format_type, filename in formats_to_export.items():
            file_path = output_path / filename
            if self.export_data(data, format_type, str(file_path)):
                success_count += 1
        
        # Create package info file
        package_info = {
            'package_name': package_name,
            'creation_date': datetime.now().isoformat(),
            'total_entries': len(data),
            'exported_formats': list(formats_to_export.keys()),
            'languages': data['language'].value_counts().to_dict() if 'language' in data.columns else {},
            'levels': data['cefr_level'].value_counts().to_dict() if 'cefr_level' in data.columns else {}
        }
        
        with open(output_path / 'package_info.json', 'w', encoding='utf-8') as f:
            json.dump(package_info, f, ensure_ascii=False, indent=2)
        
        print(f"Created study package '{package_name}' with {success_count} formats in {output_path}")
        return success_count > 0