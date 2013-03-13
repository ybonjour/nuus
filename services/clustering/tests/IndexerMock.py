__author__ = 'Yves Bonjour'

from Mock import Mock

class IndexerMock(Mock):

    def set_terms(self, terms):
        self.terms = terms

    def set_index(self, index):
        self.index = index

    def get_terms(self, document):
        self._handle_method_call("get_terms", (document,))
        return self.terms[document]

    def term_document_frequency(self, document, term):
        self._handle_method_call("term_document_frequency", (document, term))
        return self.index[term][document]

    def document_frequency_normalized(self, term):
        self._handle_method_call("document_frequency_normalized", (term,))
        return float(len(self.index[term])) / float(len(self.terms))