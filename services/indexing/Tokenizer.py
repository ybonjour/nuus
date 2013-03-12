__author__ = 'Yves Bonjour'
from nltk.tokenize import WordPunctTokenizer

def create_tokenizer():
    tokenizer = WordPunctTokenizer()
    return LowerCaseTokenizer(tokenizer)

class LowerCaseTokenizer(object):
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def tokenize(self, text):
        return [t.lower() for t in self.tokenizer.tokenize(text)]