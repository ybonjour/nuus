__author__ = 'Yves Bonjour'
from Mock import Mock

class IndexStoreMock(Mock):

    def __init__(self):
        super(IndexStoreMock, self).__init__()

    def set_document_frequency(self, doc_frequency):
        self.doc_frequency = doc_frequency

    def set_num_documents(self, num_docs):
        self.num_docs = num_docs

    def document_frequency(self, term):
        self._handle_method_call("document_frequency", (term,))
        return self.doc_frequency

    def num_documents(self):
        self._handle_method_call("num_documents")
        return self.num_docs


