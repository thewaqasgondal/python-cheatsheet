# import nltk
# print(nltk.__version__)

# import sys
# print(sys.version)


# import nltk
# nltk.data.clear_cache()

# import nltk
# nltk.download('punkt')


import nltk
from nltk.tokenize import sent_tokenize

# Only needed the first time
nltk.download('punkt')

example_string = """Muad'Dib learned rapidly because his first training was in how to learn. And the first lesson of all was the basic trust that he could learn. It's shocking to find how many people do not believe they can learn, and how many more believe learning to be difficult."""

print(sent_tokenize(example_string))


