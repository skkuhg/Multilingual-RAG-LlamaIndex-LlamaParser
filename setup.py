from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="multilingual-rag-language-learning",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive RAG system for multilingual language learning with LlamaIndex and OpenAI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/multilingual-rag-language-learning",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.2.2",
            "pytest-cov>=5.0.0",
            "black>=24.4.2",
            "flake8>=7.1.0",
            "mypy>=1.10.1",
            "pre-commit>=3.7.1",
        ],
        "viz": [
            "matplotlib>=3.9.0",
            "seaborn>=0.13.2",
            "plotly>=5.22.0",
        ],
        "ml": [
            "scikit-learn>=1.5.0",
            "scipy>=1.13.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "mlrag=src.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
