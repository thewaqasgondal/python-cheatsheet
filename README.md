# Python Cheatsheet

A comprehensive collection of Python code examples and tutorials covering various topics from basic concepts to advanced implementations. This repository serves as a practical reference for Python developers of all skill levels.

## 📋 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Examples](#examples)
  - [Concurrency](#concurrency)
  - [File Operations](#file-operations)
  - [OCR Examples](#ocr-examples)
  - [Data Processing](#data-processing)
  - [Natural Language Processing](#natural-language-processing)
  - [TensorFlow Examples](#tensorflow-examples)
- [Requirements](#requirements)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This repository contains organized Python examples demonstrating:
- **Concurrency**: Threading and multiprocessing implementations
- **File Operations**: File handling, metadata extraction, and directory management
- **OCR**: Text extraction from images including multi-language support
- **Data Processing**: Audio processing and YouTube content extraction
- **NLP**: Natural Language Processing with NLTK
- **Machine Learning**: TensorFlow basics and implementations

## 📁 Repository Structure

```
python-cheatsheet/
├── concurrency/               # Threading and multiprocessing examples
│   ├── threading_intro.py
│   └── multiprocessing_intro.py
├── file_operations/           # File handling and OS operations
│   ├── file_analysis.py
│   └── os_example.py
├── ocr_examples/              # Optical Character Recognition
│   ├── ocr_example.py
│   ├── urdu_ocr.py
│   └── table_ext.py
├── data_processing/           # Audio and video processing
│   └── yt_audio.py
├── nlp_examples/              # Natural Language Processing
│   └── my_nltk/
├── tensorflow_examples/       # TensorFlow implementations
│   └── tf.py
├── example_directory/         # Sample data files
│   ├── data.csv
│   ├── data.json
│   └── example.txt
└── images/                    # Sample images for OCR
```

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/thewaqasgondal/python-cheatsheet.git
cd python-cheatsheet
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. For OCR examples, install Tesseract:
- **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

## 📚 Examples

### Concurrency

#### Threading
Demonstrates concurrent task execution using Python's threading module. Ideal for I/O-bound operations.

```bash
python concurrency/threading_intro.py
```

**Key Concepts:**
- Thread creation and management
- Concurrent execution of multiple tasks
- Thread synchronization with `join()`

#### Multiprocessing
Shows how to leverage multiple CPU cores for CPU-bound tasks, bypassing Python's GIL.

```bash
python concurrency/multiprocessing_intro.py
```

**Key Concepts:**
- Process creation and management
- Parallel execution across multiple cores
- Process synchronization

### File Operations

#### File Analysis
Comprehensive file operations including metadata extraction, reading various file formats (text, CSV, JSON), and file manipulation.

```bash
python file_operations/file_analysis.py
```

**Features:**
- File metadata extraction (size, creation time, modification time)
- Multi-format file reading (text, CSV, JSON)
- File copying, moving, and deletion utilities

#### OS Module Examples
Demonstrates operating system interactions using Python's `os` module.

```bash
python file_operations/os_example.py
```

**Features:**
- Directory creation and navigation
- File manipulation (create, rename, delete)
- Path operations
- Environment variable access

### OCR Examples

#### Basic OCR
Extract text from images using Tesseract OCR.

```bash
python ocr_examples/ocr_example.py
```

#### Urdu OCR
Multi-language OCR support for Urdu text extraction.

```bash
python ocr_examples/urdu_ocr.py
```

#### Table Extraction
Extract and parse tabular data from images.

```bash
python ocr_examples/table_ext.py
```

**Note:** Update the Tesseract path in each script according to your installation.

### Data Processing

#### YouTube Audio Extraction
Download and process audio from YouTube videos with speech recognition capabilities.

```bash
python data_processing/yt_audio.py
```

**Features:**
- YouTube audio download
- Audio format conversion
- Speech-to-text conversion
- AI-powered summarization

### Natural Language Processing

Examples using NLTK for text processing tasks:
- Tokenization
- Word and punctuation tokenization
- Named Entity Recognition (NER)

Navigate to `nlp_examples/my_nltk/` to explore various NLTK implementations.

### TensorFlow Examples

Basic TensorFlow operations and setup verification.

```bash
python tensorflow_examples/tf.py
```

## 📦 Requirements

Main dependencies include:
- `pytesseract` - OCR engine wrapper
- `Pillow` - Image processing
- `pandas` - Data manipulation
- `yt-dlp` - YouTube content download
- `pydub` - Audio processing
- `SpeechRecognition` - Speech-to-text
- `transformers` - NLP models
- `tensorflow` - Machine learning
- `nltk` - Natural Language Processing

See [requirements.txt](requirements.txt) for complete list.

## 💻 Usage

Each example is self-contained and can be run independently. Navigate to the specific category directory and run the desired script:

```bash
# Example: Run threading demo
python concurrency/threading_intro.py

# Example: Run file analysis
python file_operations/file_analysis.py
```

Make sure to update file paths and configuration settings in the scripts as needed for your environment.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows Python best practices and includes appropriate documentation.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Waqas Gondal**
- GitHub: [@thewaqasgondal](https://github.com/thewaqasgondal)

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!
