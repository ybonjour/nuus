__author__ = 'Yves Bonjour'
from Mock import Mock

class IndexStoreMock(Mock):

    def __init__(self):
        super(IndexStoreMock, self).__init__()

    def set_document_frequency(self, doc_frequency):
        self.doc_frequency = doc_frequency

    def set_num_documents(self, num_docs):
        self.num_docs = num_docs

    def set_terms(self, terms):
        self.terms = terms

    def document_frequency(self, term):
        self._handle_method_call("document_frequency", (term,))
        return self.doc_frequency

    def num_documents(self):
        self._handle_method_call("num_documents")
        return self.num_docs

    def get_terms(self, document):
        self._handle_method_call("get_terms", (document,))
        return self.terms


