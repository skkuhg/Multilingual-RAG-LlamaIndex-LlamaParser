# 🌏 Multilingual RAG Language Learning System

A comprehensive Retrieval-Augmented Generation (RAG) system for multilingual language learning built with LlamaIndex, LlamaParser, and OpenAI. This project provides intelligent vocabulary drills, spaced repetition scheduling, and contextual learning from diverse content sources.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-latest-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Features

### 📚 Multi-Format Data Ingestion
- **Text Files**: `.txt`, `.html`, `.md`, `.rtf`
- **Subtitles**: `.srt`, `.vtt` with timestamp parsing
- **Structured Data**: `.json`, `.csv` with intelligent schema detection
- **Enhanced Parsing**: LlamaParser integration for complex document formats

### 🤖 Intelligent RAG System
- **Vector Indexing**: Semantic search across multilingual content
- **Language Detection**: Automatic language identification for 10+ languages
- **CEFR Level Estimation**: Automatic difficulty assessment (A1-C2)
- **Contextual Queries**: File-specific and pattern-based searching
- **Metadata Preservation**: Rich context including source files, timestamps, and structure

### 🧠 Spaced Repetition System (SRS)
- **SM-2 Algorithm**: Anki-style spaced repetition scheduling
- **Adaptive Learning**: Dynamic difficulty adjustment based on recall quality
- **Progress Tracking**: Review intervals, ease factors, and repetition counts
- **Export Integration**: Direct Anki card export functionality

### 🌍 Multilingual Support
- **Supported Languages**: Korean, Japanese, Chinese, Spanish, French, German, English, Italian, Portuguese, Russian
- **Grammar Pattern Detection**: Language-specific pattern recognition
- **Cultural Context**: Emoji integration and cultural markers
- **Translation Integration**: OpenAI-powered translation services

### 📊 Learning Analytics
- **Token Tracking**: Comprehensive API usage monitoring
- **Cost Analysis**: Real-time cost tracking with projections
- **Performance Metrics**: Learning progress visualization
- **Data Insights**: Language distribution and content quality analysis

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- LlamaCloud API key
- Tavily API key (optional, for web search)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/skkuhg/Multilingual-RAG-LlamaIndex-LlamaParser.git
   cd Multilingual-RAG-LlamaIndex-LlamaParser
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Add your learning content**:
   - Place text files in `data/articles/`
   - Add subtitles to `data/subtitles/`
   - Include vocabulary lists in `data/wordlists/`

5. **Run the example**:
   ```bash
   python examples/sample_usage.py
   ```

## 📖 Usage

### Basic RAG System

```python
from src.rag_system import MultilingualRAGSystem
from src.data_processor import DataProcessor

# Initialize components
rag_system = MultilingualRAGSystem()
processor = DataProcessor()

# Process your data
df = processor.ingest_data_files("data/")
documents = processor.create_documents(df)

# Add to RAG system
rag_system.add_documents(documents)

# Query your content
response = rag_system.query("Show me Korean vocabulary examples")
print(response)
```

### Language-Specific Queries

```python
# Filter by language
korean_content = rag_system.query(
    "grammar patterns", 
    language_filter="Korean"
)

# Filter by CEFR level
beginner_content = rag_system.query(
    "basic vocabulary", 
    cefr_level="A1"
)
```

### Spaced Repetition System

```python
from src.srs_scheduler import SRSScheduler

scheduler = SRSScheduler()

# Initialize SRS for your content
df_with_srs = scheduler.initialize_srs_metadata(df)

# Get cards due for review
due_cards = scheduler.get_due_cards(df_with_srs)

# Update after practice
scheduler.update_srs(card_id, quality_score=4)  # 0-5 scale

# Export to Anki
scheduler.export_to_anki_format(df_with_srs, "my_deck.txt")
```

### Cost Tracking

```python
from src.cost_tracker import TokenTracker

tracker = TokenTracker()

# Monitor usage
usage_stats = tracker.get_usage_summary()
print(f"Total cost: ${usage_stats['total_cost']:.4f}")

# Set budget alerts
tracker.set_budget_limit(10.00)  # $10 monthly limit
```

## 📁 Project Structure

```
Multilingual-RAG-LlamaIndex-LlamaParser/
├── src/
│   ├── rag_system.py          # Core RAG functionality
│   ├── data_processor.py      # Multi-format data ingestion
│   ├── language_detector.py   # Language detection & CEFR estimation
│   ├── srs_scheduler.py       # Spaced repetition system
│   ├── cost_tracker.py        # Token usage & cost tracking
│   └── utils/
│       ├── file_parsers.py     # Format-specific parsers
│       ├── pattern_matchers.py # Language pattern detection
│       └── export_helpers.py   # Export utilities
├── data/
│   ├── articles/              # Text content
│   ├── subtitles/             # .srt/.vtt files
│   ├── wordlists/             # .csv vocabulary
│   └── chat_logs/             # Conversation JSON
├── examples/
│   └── sample_usage.py        # Example usage
├── tests/
│   └── test_*.py              # Unit tests
├── .env.example               # Environment template
├── requirements.txt           # Dependencies
├── setup.py                   # Package configuration
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with your API keys:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here
LLAMACLOUD_API_KEY=your_llamacloud_api_key_here

# Optional
TAVILY_API_KEY=your_tavily_api_key_here

# RAG Configuration
CHUNK_SIZE=500
CHUNK_OVERLAP=50
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o-mini

# SRS Settings
INITIAL_INTERVAL=1
EASY_BONUS=1.3
HARD_PENALTY=1.2
```

### Supported File Formats

| Format | Extension | Features |
|--------|-----------|----------|
| Text | `.txt`, `.md`, `.html` | Basic text extraction |
| Subtitles | `.srt`, `.vtt` | Timestamp parsing |
| Structured | `.json`, `.csv` | Schema detection |
| Rich | `.pdf`, `.docx` | LlamaParser integration |

## 📊 Learning Analytics

The system provides comprehensive analytics:

- **Progress Tracking**: Review accuracy and timing
- **Content Analysis**: Language distribution and difficulty
- **Usage Statistics**: API consumption and costs
- **Learning Insights**: Optimal review schedules

## 🌍 Language Support

### Currently Supported Languages

| Language | Code | CEFR Levels | Grammar Patterns |
|----------|------|-------------|------------------|
| Korean | ko | ✅ A1-C2 | ✅ Honorifics, Tenses |
| Japanese | ja | ✅ A1-C2 | ✅ Keigo, Particles |
| Spanish | es | ✅ A1-C2 | ✅ Subjunctive, Ser/Estar |
| French | fr | ✅ A1-C2 | ✅ Genders, Liaisons |
| German | de | ✅ A1-C2 | ✅ Cases, Separable Verbs |
| Chinese | zh | ✅ A1-C2 | ✅ Measure Words, Tones |
| English | en | ✅ A1-C2 | ✅ Phrasal Verbs |
| Italian | it | ✅ A1-C2 | ✅ Conjugations |
| Portuguese | pt | ✅ A1-C2 | ✅ Nasal Sounds |
| Russian | ru | ✅ A1-C2 | ✅ Cases, Aspects |

### Adding New Languages

1. Update `language_detector.py` with new patterns
2. Add grammar rules to `pattern_matchers.py`
3. Include cultural context markers
4. Test with sample content

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and install
git clone https://github.com/skkuhg/Multilingual-RAG-LlamaIndex-LlamaParser.git
cd Multilingual-RAG-LlamaIndex-LlamaParser
pip install -e .

# Run tests
python -m pytest tests/

# Code formatting
black src/ tests/
```

### Roadmap

- [ ] Voice integration for pronunciation practice
- [ ] Mobile app for on-the-go learning
- [ ] Advanced analytics dashboard
- [ ] Community content sharing
- [ ] Offline mode support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LlamaIndex** - For the powerful RAG framework
- **LlamaParser** - For enhanced document processing
- **OpenAI** - For language models and embeddings
- **Anki** - For inspiring the SRS algorithm

## 📞 Support

- 📧 Email: ahczhg@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/skkuhg/Multilingual-RAG-LlamaIndex-LlamaParser/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/skkuhg/Multilingual-RAG-LlamaIndex-LlamaParser/discussions)

---

**Happy Learning! 🎉🌏📚**