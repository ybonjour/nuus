__author__ = 'Yves Bonjour'

import unittest
from IndexerMock import IndexerMock
from VectorCalculator import VectorCalculator
import uuid
from math import log10

class VectorCalculatorTest(unittest.TestCase):
    def setUp(self):
        self.indexer_mock = IndexerMock()
        self.calculator = VectorCalculator(self.indexer_mock)

    def test_get_tfidf_vector_one_document_two_terms(self):
        # Arrange
        document = uuid.uuid4()
        term1 = "foo"
        term2 = "bar"

        self.indexer_mock.set_terms({document:[term1, term2]})
        self.indexer_mock.set_index({term1:{document:1}, term2:{document:1}})

        # Act
        v = self.calculator.get_tfidf_vector(document)

        # Assert
        self.assertEqual(2, len(v))

        self.assertIn(term1, v)
        tfidf_term1 = (1.0 + log10(1)) * log10(1)
        self.assertEqual(tfidf_term1, v[term1])

        self.assertIn(term2, v)
        tfidf_term2 = (1 + log10(1)) * log10(1)
        self.assertEqual(tfidf_term2, v[term2])

    def test_get_tfidf_vector_two_documents_one_term_each(self):
        # Arrange
        document1 = uuid.uuid4()
        document2 = uuid.uuid4()
        term1 = "foo"
        term2 = "bar"

        self.indexer_mock.set_terms({document1:[term1], document2:[term2]})
        self.indexer_mock.set_index({term1:{document1:1}, term2:{document2:1}})

        # Act
        v = self.calculator.get_tfidf_vector(document1)

        # Assert
        self.assertEqual(1, len(v))

        self.assertIn(term1, v)
        tfidf_term1 = (1.0 + log10(1)) * log10(2)
        self.assertEqual(tfidf_term1, v[term1])

    def test_get_tfidf_vector_two_documents_one_term(self):
        # Arrange
        document1 = uuid.uuid4()
        document2 = uuid.uuid4()
        term = "foo"

        self.indexer_mock.set_terms({document1:[term], document2:[term]})
        self.indexer_mock.set_index({term:{document1:1, document2:1}})

        # Act
        v = self.calculator.get_tfidf_vector(document1)

        # Assert
        self.assertEqual(1, len(v))

        self.assertIn(term, v)
        tfidf_term1 = (1.0 + log10(1)) * log10(1)
        self.assertEqual(tfidf_term1, v[term])

    def test_get_average_vector(self):
        # Arrange
        document1 = uuid.uuid4()
        document2 = uuid.uuid4()

        term1 = "foo"
        term2 = "bar"

        self.indexer_mock.set_terms({document1:[term1], document2:[term2]})
        self.indexer_mock.set_index({term1:{document1:1}})

        # Act

        # Assert


if __name__ == '__main__':
    unittest.main()
