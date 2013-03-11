__author__ = 'Yves Bonjour'

class IndexStoreMock:
    def posting_list(self, term):
        self._handle_method_call("posting_list", (term,))

    def document_frequency(self, term):
        self._handle_method_call("document_frequency", (term,))

    def num_documents(self):
        self._handle_method_call("num_documents")

    def term_document_frequency(self, document, term):
        self._handle_method_call("term_document_frequency", (document, term))

    def add(self, document, term):
        self._handle_method_call("add", (document, term))


