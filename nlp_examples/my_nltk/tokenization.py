"""
NLTK Tokenization Examples

This module demonstrates text tokenization using NLTK (Natural Language Toolkit).
Tokenization is the process of breaking text into smaller units like words or sentences.
"""

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Download required NLTK data
nltk.download('punkt', quiet=True)


def sentence_tokenization_example():
    """Demonstrate sentence tokenization."""
    print("=== Sentence Tokenization ===")

    example_text = """Muad'Dib learned rapidly because his first training was in how to learn. And the first lesson of all was the basic trust that he could learn. It's shocking to find how many people do not believe they can learn, and how many more believe learning to be difficult."""

    print("Original text:")
    print(example_text)
    print()

    sentences = sent_tokenize(example_text)
    print(f"Tokenized into {len(sentences)} sentences:")
    for i, sentence in enumerate(sentences, 1):
        print(f"{i}. {sentence}")
    print()


def word_tokenization_example():
    """Demonstrate word tokenization."""
    print("=== Word Tokenization ===")

    example_sentences = [
        "Hello, world!",
        "I'm learning Python programming.",
        "Tokenization is an important NLP task.",
        "Dr. Smith went to Washington, D.C. last summer."
    ]

    for sentence in example_sentences:
        print(f"Original: {sentence}")
        words = word_tokenize(sentence)
        print(f"Tokens: {words}")
        print(f"Word count: {len(words)}")
        print()


def analyze_tokenization():
    """Analyze tokenization behavior with different text types."""
    print("=== Tokenization Analysis ===")

    test_cases = [
        "I can't believe it's working!",
        "The U.S.A. is a country.",
        "Price is $10.99.",
        "Email: user@example.com",
        "Visit https://www.python.org/",
    ]

    for text in test_cases:
        print(f"Text: {text}")
        words = word_tokenize(text)
        print(f"Word tokens: {words}")
        sentences = sent_tokenize(text)
        print(f"Sentence tokens: {sentences}")
        print()


def main():
    """Run all tokenization examples."""
    print("NLTK Tokenization Examples")
    print("=" * 40)
    print()

    sentence_tokenization_example()
    word_tokenization_example()
    analyze_tokenization()


if __name__ == "__main__":
    main()





