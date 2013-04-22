__author__ = 'Yves Bonjour'

from math import log10
from Proxies import IndexProxy

def create_vector_calculator(index_url):
    index_service = IndexProxy(index_url)
    return VectorCalculator(index_service)


class VectorCalculator:

    def __init__(self, index_service):
        self.index_service = index_service

    def get_average_vector(self, document_ids):
        if not document_ids:
            return {}

        vectors = [self.get_tfidf_vector(doc_id) for doc_id in document_ids]
        avg_vector = {}
        f = 1.0 / float(len(document_ids))
        for v in vectors:
            for t, v in v.iteritems():
                avg_vector[t] = avg_vector.get(t, 0.0) + f * float(v)

        return avg_vector

    def get_tfidf_vector(self, document_id):
        terms = self.index_service.get_terms(document_id)

        return {t: self._calculate_tfidf(document_id, t) for t in terms}

    def _calculate_tfidf(self, document_id, term):
        tf = self.index_service.term_document_frequency(document_id, term)
        tf_log = 1.0 + log10(tf) if tf > 0 else 0

        df_log = log10(1.0 / float(self.index_service.document_frequency_normalized(term)))

        return tf_log*df_log