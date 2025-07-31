"""
Sample Usage Example for Multilingual RAG Language Learning System

This script demonstrates basic usage of the system with sample data.
"""

import os
import sys
from pathlib import Path

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_system import MultilingualRAGSystem
from data_processor import DataProcessor
from srs_scheduler import SRSScheduler
from cost_tracker import TokenTracker


def main():
    """Main example function."""
    print("🌏 Multilingual RAG Language Learning System - Sample Usage")
    print("=" * 60)
    
    # Check for API keys
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Please set OPENAI_API_KEY environment variable")
        print("   You can create a .env file with your API keys")
        return
    
    # Initialize components
    print("\n🔧 Initializing system components...")
    
    try:
        # Initialize RAG system
        rag_system = MultilingualRAGSystem()
        processor = DataProcessor()
        scheduler = SRSScheduler()
        token_tracker = TokenTracker()
        
        print("✅ System components initialized successfully")
        
        # Process sample data
        print("\n📁 Processing sample data...")
        
        # Create sample data if it doesn't exist
        create_sample_data()
        
        # Ingest data
        df_raw = processor.ingest_data_files("examples/sample_data")
        
        if df_raw.empty:
            print("⚠️ No data found. Creating sample data...")
            create_sample_data()
            df_raw = processor.ingest_data_files("examples/sample_data")
        
        print(f"📊 Processed {len(df_raw)} items")
        
        # Build RAG index
        print("\n🔨 Building RAG index...")
        documents = processor.create_documents(df_raw)
        
        rag_system.add_documents(documents)
        print("✅ RAG index built successfully")
        
        # Demo queries
        print("\n🤖 Running demo queries...")
        
        # General query
        response1 = rag_system.query("Show me Korean examples")
        print(f"\n🇰🇷 Korean Examples Query:")
        print(response1[:200] + "..." if len(response1) > 200 else response1)
        
        # Language-specific query
        response2 = rag_system.query("Spanish grammar patterns", language_filter="Spanish")
        print(f"\n🇪🇸 Spanish Grammar Query:")
        print(response2[:200] + "..." if len(response2) > 200 else response2)
        
        # Initialize SRS
        print("\n🧠 Setting up Spaced Repetition System...")
        df_with_srs = scheduler.initialize_srs_metadata(df_raw)
        
        # Show learning statistics
        stats = scheduler.get_learning_statistics(df_with_srs)
        print(f"\n📊 Learning Statistics:")
        print(f"   • Total cards: {stats['total_cards']}")
        print(f"   • New cards: {stats['new_cards']}")
        print(f"   • Languages: {list(stats.get('languages', {}).keys())}")
        
        # Export sample
        print("\n💾 Exporting sample data...")
        output_dir = Path("examples")
        output_dir.mkdir(exist_ok=True)
        
        scheduler.export_to_anki_format(
            df_with_srs.head(10), 
            str(output_dir / "sample_export.txt"), 
            max_cards=10
        )
        
        # Cost summary
        print("\n💰 Cost Summary:")
        # Note: In real usage, token tracking would be automatic
        print("   • This is a demo - actual costs depend on your usage")
        print("   • Monitor your API usage in the OpenAI dashboard")
        
        print("\n🎉 Sample usage completed successfully!")
        print("\n💡 Next steps:")
        print("   • Add your own data files to the data/ directory")
        print("   • Customize language patterns in pattern_matchers.py")
        print("   • Explore advanced features in the documentation")
        
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        print("💡 Make sure you have:")
        print("   • Valid API keys in your .env file")
        print("   • Required dependencies installed")
        print("   • Sample data in examples/sample_data/")


def create_sample_data():
    """Create sample data for demonstration."""
    sample_dir = Path("examples/sample_data")
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample Korean sentences
    korean_file = sample_dir / "korean_sample.txt"
    if not korean_file.exists():
        korean_sentences = [
            "저는 지금 한국어를 공부하고 있어요.",
            "친구들과 함께 영화를 보고 있어요.",
            "오늘 날씨가 정말 좋아요.",
            "커피를 마시면서 책을 읽고 있어요.",
            "새로운 언어를 배우고 있어요."
        ]
        korean_file.write_text("\n".join(korean_sentences), encoding='utf-8')
        print(f"📝 Created sample Korean file: {korean_file}")
    
    # Create sample Spanish sentences
    spanish_file = sample_dir / "spanish_sample.txt"
    if not spanish_file.exists():
        spanish_sentences = [
            "Espero que tengas un buen día.",
            "Ojalá que llueva mañana.",
            "Es importante que estudies mucho.",
            "Dudo que él venga a la fiesta.",
            "Me alegro de que estés aquí."
        ]
        spanish_file.write_text("\n".join(spanish_sentences), encoding='utf-8')
        print(f"📝 Created sample Spanish file: {spanish_file}")
    
    # Create sample vocabulary CSV
    import pandas as pd
    vocab_file = sample_dir / "sample_vocab.csv"
    if not vocab_file.exists():
        vocab_data = pd.DataFrame({
            'word': ['안녕하세요', 'hola', 'bonjour', 'hello'],
            'translation': ['hello (Korean)', 'hello (Spanish)', 'hello (French)', 'hello (English)'],
            'language': ['Korean', 'Spanish', 'French', 'English'],
            'level': ['A1', 'A1', 'A1', 'A1']
        })
        vocab_data.to_csv(vocab_file, index=False, encoding='utf-8')
        print(f"📊 Created sample vocabulary file: {vocab_file}")


if __name__ == "__main__":
    main()