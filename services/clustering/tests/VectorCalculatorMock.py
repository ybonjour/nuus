__author__ = 'Yves Bonjour'

from Mock import Mock


class VectorCalculatorMock(Mock):
    def set_vectors(self, vectors):
        self.vectors = vectors

    def set_average_vector(self, average_vector):
        self.average_vector = average_vector

    def get_average_vector(self, document_ids):
        self._handle_method_call("get_average_vector", (document_ids,))
        return self.average_vector

    def get_tfidf_vector(self, document_id):
        self._handle_method_call("get_tfidf_vector", (document_id,))
        return self.vectors[document_id]

