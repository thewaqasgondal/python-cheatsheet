import nltk
from nltk import pos_tag, word_tokenize, ne_chunk

# Example sentence
example_string = "Barack Obama was born in Hawaii and served as the 44th president of the United States."

# Tokenize the string
tokens = word_tokenize(example_string)

# Perform POS tagging
tagged_tokens = pos_tag(tokens)

# Perform Named Entity Recognition (NER)
named_entities = ne_chunk(tagged_tokens)

# Display the result
print(named_entities)
