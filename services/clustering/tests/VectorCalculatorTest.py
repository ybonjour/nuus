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

        self.indexer_mock.set_terms({document: [term1, term2]})
        self.indexer_mock.set_index({term1: {document: 1}, term2: {document: 1}})

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

    def test_get_tfidf_vector_one_document_one_term_twice(self):
        # Arrange
        document = uuid.uuid4()
        term = "foo"

        self.indexer_mock.set_terms({document: [term]})
        self.indexer_mock.set_index({term: {document: 2}})

        # Act
        v = self.calculator.get_tfidf_vector(document)

        # Assert
        self.assertEqual(1, len(v))

        self.assertIn(term, v)
        tfidf_term1 = (1.0 + log10(2)) * log10(1)
        self.assertEqual(tfidf_term1, v[term])

    def test_get_tfidf_vector_two_documents_one_term_each(self):
        # Arrange
        document1 = uuid.uuid4()
        document2 = uuid.uuid4()
        term1 = "foo"
        term2 = "bar"

        self.indexer_mock.set_terms({document1: [term1], document2: [term2]})
        self.indexer_mock.set_index({term1: {document1: 1}, term2: {document2: 1}})

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

        self.indexer_mock.set_terms({document1: [term], document2: [term]})
        self.indexer_mock.set_index({term: {document1: 1, document2: 1}})

        # Act
        v = self.calculator.get_tfidf_vector(document1)

        # Assert
        self.assertEqual(1, len(v))

        self.assertIn(term, v)
        tfidf_term1 = (1.0 + log10(1)) * log10(1)
        self.assertEqual(tfidf_term1, v[term])

    def test_get_average_vector_two_documents_one_term(self):
        # Arrange
        document1 = uuid.uuid4()
        document2 = uuid.uuid4()

        term = "foo"

        self.indexer_mock.set_terms({document1: [term], document2: [term]})
        self.indexer_mock.set_index({term: {document1: 1, document2: 1}})

        # Act
        average_v = self.calculator.get_average_vector([document1, document2])

        # Assert
        self.assertEqual(1, len(average_v))
        self.assertTrue(term in average_v)
        tfidf_term = (1.0 + log10(1)) * log10(1)
        self.assertEqual(tfidf_term, average_v[term])

    def test_get_average_vector_two_terms(self):
        # Arrange
        document1 = uuid.uuid4()
        document2 = uuid.uuid4()

        term1 = "foo"
        term2 = "bar"

        self.indexer_mock.set_terms({document1: [term1], document2: [term2]})
        self.indexer_mock.set_index({term1: {document1: 1}, term2: {document2: 1}})

        # Act
        average_v = self.calculator.get_average_vector([document1, document2])

        # Assert
        self.assertEqual(2, len(average_v))
        self.assertTrue(term1 in average_v)
        self.assertTrue(term2 in average_v)

        tfidf_terms = (1.0 + log10(1)) * log10(2)

        self.assertEqual(tfidf_terms / 2.0, average_v[term1])
        self.assertEqual(tfidf_terms / 2.0, average_v[term2])

    def test_get_average_vector_three_documents(self):
        # Arrange
        document1 = uuid.uuid4()
        document2 = uuid.uuid4()
        document3 = uuid.uuid4()

        term = "foo"

        self.indexer_mock.set_terms({document1: [term], document2: [term], document3: [term]})
        self.indexer_mock.set_index({term: {document1: 1, document2: 1, document3: 1}})

        # Act
        average_v = self.calculator.get_average_vector([document1, document2, document3])

        # Assert
        self.assertEqual(1, len(average_v))
        self.assertTrue(term in average_v)
        tfidf_term = (1.0 + log10(1)) * log10(1)
        self.assertEqual(tfidf_term, average_v[term])

    def test_get_average_vector_no_documents(self):
        # Act
        average_v = self.calculator.get_average_vector([])

        # Assert
        self.assertEqual(0, len(average_v))

    def test_get_average_vector_one_document(self):
        # Arrange
        document = uuid.uuid4()

        term = "foo"

        self.indexer_mock.set_terms({document: [term]})
        self.indexer_mock.set_index({term: {document: 1}})

        # Act
        average_v = self.calculator.get_average_vector([document])

        # Assert
        self.assertEqual(1, len(average_v))
        self.assertTrue(term in average_v)
        tfidf_term = (1.0 + log10(1)) * log10(1)
        self.assertEqual(tfidf_term, average_v[term])

if __name__ == '__main__':
    unittest.main()
