__author__ = 'Yves Bonjour'

class Indexer:
    def __init__(self, store, tokenizer):
        self.store = store
        self.tokenizer = tokenizer

    def index(self, text, document_id):
        tokens = self.tokenizer.tokenize(text)
        for token in tokens:
            self.store.add(document_id, token)

    def document_frequency_normalized(self, term):
        return float(self.store.document_frequency(term)) / float(self.store.num_documents())

    def term_document_frequency(self, document, term):
        return self.store.term_document_frequency(document, term)

class MemoryIndexStore:
    def __init__(self):
        self.posting_lists = {}
        self.documents = {}

    def posting_list(self, term):
        return self.posting_lists[term]

    def document_frequency(self, term):
        if term not in self.posting_lists: return 0
        return len(self.posting_lists[term])

    def num_documents(self):
        return len(self.documents)

    def term_document_frequency(self, document, term):
        if term not in self.posting_lists or document not in self.posting_lists[term]: return 0

        return self.posting_lists[term][document]

    def add(self, document, term):
        if term not in self.posting_lists:
            self.posting_lists[term] = {}

        if document not in self.posting_lists[term]:
            self.posting_lists[term][document] = 0

        self.posting_lists[term][document] += 1
        self.documents[document] = True
