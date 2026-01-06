# Natural Language Processing Examples

This directory contains NLTK (Natural Language Toolkit) examples for text processing.

## Files Overview

The `my_nltk` directory contains various NLP examples:

### Available Examples:
- **test_setup.py** - Basic NLTK setup and testing
- **tokenization.py** - Text tokenization examples
- **custom_tokenization.py** - Custom tokenizers
- **word_punct_tokenization.py** - Word and punctuation tokenization
- **05_named_entity_recognition.py** - Named Entity Recognition (NER)

## Getting Started

### Install NLTK:
```bash
pip install nltk
```

### Download required data:
```python
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
```

## Key Concepts

### Tokenization
Breaking text into words, sentences, or other meaningful units.

**Types:**
- **Word Tokenization**: Split text into words
- **Sentence Tokenization**: Split text into sentences
- **Custom Tokenization**: Define your own rules

### Named Entity Recognition (NER)
Identify and classify named entities in text (people, organizations, locations, etc.)

**Example entities:**
- PERSON: Names of people
- ORGANIZATION: Companies, agencies, institutions
- LOCATION: Cities, countries, regions
- DATE: Temporal expressions
- GPE: Geopolitical entities

## Common NLP Tasks

1. **Text Preprocessing**
   - Tokenization
   - Lowercasing
   - Removing punctuation
   - Stop word removal

2. **Part-of-Speech Tagging**
   - Identify word types (noun, verb, adjective, etc.)
   - Grammatical analysis

3. **Named Entity Recognition**
   - Extract entities from text
   - Entity classification

4. **Text Analysis**
   - Frequency analysis
   - Collocation detection
   - Sentiment analysis

## Usage Examples

### Basic Tokenization:
```python
import nltk
from nltk.tokenize import word_tokenize

text = "Hello, world! This is NLTK."
tokens = word_tokenize(text)
print(tokens)
```

### Named Entity Recognition:
```python
from nltk import ne_chunk, pos_tag
from nltk.tokenize import word_tokenize

text = "Apple Inc. is located in California."
tokens = word_tokenize(text)
tagged = pos_tag(tokens)
entities = ne_chunk(tagged)
print(entities)
```

## Resources

- [NLTK Documentation](https://www.nltk.org/)
- [NLTK Book](https://www.nltk.org/book/)
- [NLTK Data](https://www.nltk.org/data.html)
