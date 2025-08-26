
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import TreebankWordTokenizer

tokenizer = TreebankWordTokenizer()

example_string = "The quick (brown) fox doesn't jump over lazy dogs."

# Tokenize the string
tokens = tokenizer.tokenize(example_string)

print("Tokens:", tokens)


# Create a regular expression tokenizer
tokenizer = RegexpTokenizer(r'\w+')

example_string = "Hello there! How's it going? Welcome to NLP."

# Tokenize the string using regex
tokens = tokenizer.tokenize(example_string)
print("Tokens:", tokens)

