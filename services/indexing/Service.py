__author__ = 'Yves Bonjour'

from nltk.tokenize import WordPunctTokenizer
from Indexer import Indexer
from Indexer import MemoryIndexStore

if __name__ == "__main__":
    tokenizer = WordPunctTokenizer()
    store = MemoryIndexStore()
    indexer = Indexer(store, tokenizer)
    indexer.index()



