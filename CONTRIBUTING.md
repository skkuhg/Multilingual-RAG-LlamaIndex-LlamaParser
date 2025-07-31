# Contributing to Multilingual RAG Language Learning System

We welcome contributions from the community! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Issues

1. **Search Existing Issues**: Before creating a new issue, please search existing issues to avoid duplicates.

2. **Create Detailed Issues**: When reporting bugs or requesting features, please include:
   - Clear description of the issue/request
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details (Python version, OS, etc.)
   - Relevant code snippets or error messages

### Pull Requests

1. **Fork the Repository**: Create a fork of the repository on GitHub.

2. **Create a Feature Branch**: 
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**: 
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

4. **Test Your Changes**: 
   ```bash
   python -m pytest tests/
   ```

5. **Commit Changes**: 
   ```bash
   git commit -m "Add: descriptive commit message"
   ```

6. **Push to Your Fork**: 
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**: Open a pull request against the main branch.

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Include docstrings for all classes and functions
- Keep line length under 100 characters
- Use meaningful variable and function names

### Code Formatting

We use `black` for code formatting:

```bash
# Format code
black src/ tests/

# Check formatting
black --check src/ tests/
```

### Testing

- Write unit tests for new functionality
- Maintain test coverage above 80%
- Use pytest for testing framework
- Include integration tests for major features

### Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions and classes
- Include code examples in documentation
- Update changelog for notable changes

## 🏗️ Project Structure

```
src/
├── rag_system.py          # Core RAG functionality
├── data_processor.py      # File ingestion and processing
├── language_detector.py   # Language detection and CEFR estimation
├── srs_scheduler.py       # Spaced repetition system
├── cost_tracker.py        # API usage and cost tracking
└── utils/
    ├── file_parsers.py     # Enhanced file parsing
    ├── pattern_matchers.py # Language pattern detection
    └── export_helpers.py   # Export functionality
```

## 🌍 Adding New Languages

To add support for a new language:

1. **Update Language Detector**: Add patterns to `language_detector.py`
   ```python
   self.language_patterns['NewLanguage'] = [
       r'pattern1',
       r'pattern2'
   ]
   ```

2. **Add Grammar Patterns**: Update `pattern_matchers.py`
   ```python
   self.grammar_patterns['NewLanguage'] = {
       'category1': [r'pattern1', r'pattern2'],
       'category2': [r'pattern3', r'pattern4']
   }
   ```

3. **Add Cultural Markers**: Include common expressions
   ```python
   self.cultural_markers['NewLanguage'] = ['hello', 'thank_you', 'please']
   ```

4. **Update Tests**: Add test cases for the new language
5. **Update Documentation**: Add language to supported languages list

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/test_language_detector.py
```

### Test Structure

- Unit tests: Test individual functions and classes
- Integration tests: Test component interactions
- End-to-end tests: Test complete workflows

### Writing Tests

```python
import pytest
from src.language_detector import LanguageDetector

def test_language_detection():
    detector = LanguageDetector()
    result = detector.detect_language("Hello world")
    assert result == "English"
```

## 📦 Adding New Features

### Feature Requests

1. Open an issue describing the feature
2. Discuss implementation approach
3. Get approval from maintainers
4. Implement with tests and documentation

### API Design Principles

- Keep interfaces simple and intuitive
- Use consistent naming conventions
- Provide sensible defaults
- Include comprehensive error handling
- Support both beginner and advanced use cases

## 🔧 Development Setup

### Local Development

```bash
# Clone repository
git clone https://github.com/skkuhg/Multilingual-RAG-LlamaIndex-LlamaParser.git
cd Multilingual-RAG-LlamaIndex-LlamaParser

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
```

### Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
# OPENAI_API_KEY=your_key_here
# LLAMACLOUD_API_KEY=your_key_here
```

## 📋 Code Review Process

1. **Automated Checks**: All PRs must pass:
   - Code formatting (black)
   - Linting (flake8)
   - Type checking (mypy)
   - Unit tests (pytest)

2. **Manual Review**: Maintainers will review:
   - Code quality and design
   - Test coverage
   - Documentation completeness
   - Performance implications

3. **Feedback**: Address reviewer feedback promptly

4. **Approval**: At least one maintainer approval required

## 🎯 Contribution Ideas

### Good First Issues

- Add new language patterns
- Improve error messages
- Add more file format support
- Enhance documentation
- Fix typos or formatting

### Advanced Contributions

- Performance optimizations
- New export formats
- Advanced language features
- Machine learning improvements
- Integration with other tools

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and community chat
- **Email**: ahczhg@gmail.com for maintainer contact

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to the Multilingual RAG Language Learning System! 🌟**