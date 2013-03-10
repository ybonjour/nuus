__author__ = 'Yves Bonjour'

class Indexer:
    def __init__(self, store, tokenizer):
        self.store = store
        self.tokenizer = tokenizer

    def index(self, text, document_id):
        tokens = self.tokenizer.tokenize(text)
        for token in tokens:
            self.store.add(document_id, token)


class MemoryIndexStore:
    def __init__(self):
        self.posting_lists = {}

    def posting_list(self, term):
        return self.posting_lists[term]

    def document_frequency(self, term):
        if term not in self.posting_lists: return 0
        return len(self.posting_lists[term])

    def term_document_frequency(self, document, term):
        if term not in self.posting_lists or document not in self.posting_lists[term]: return 0

        return self.posting_lists[term][document]

    def add(self, document, term):
        if term not in self.posting_lists:
            self.posting_lists[term] = {}

        if document not in self.posting_lists[term]:
            self.posting_lists[term][document] = 0

        self.posting_lists[term][document] += 1
