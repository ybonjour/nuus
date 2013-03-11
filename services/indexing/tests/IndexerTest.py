__author__ = 'Yves Bonjour'

import unittest

from Indexer import MemoryIndexStore
import uuid
from IndexStoreMock import IndexStoreMock
from Indexer import Indexer
from nltk.tokenize import WordPunctTokenizer

class MemoryIndexStoreTest(unittest.TestCase):

    def setUp(self):
        self.store = MemoryIndexStore()

    def test_add_new_term_new_document(self):
        # Arrange
        term = "foo"
        document = uuid.uuid4()

        # Act
        self.store.add(document, term)

        # Assert
        docs = self.store.posting_list(term)
        self.assertEqual(1, len(docs))
        self.assertIn(document, docs)
        self.assertEqual(1, docs[document])

        self.assertEqual(1, self.store.num_documents())

    def test_add_existing_term_new_document(self):
        # Arrange
        term = "foo"
        document1 = uuid.uuid4()
        document2 = uuid.uuid4()
        self.store.add(document1, term)

        # Act
        self.store.add(document2, term)

        # Assert
        docs = self.store.posting_list(term)
        self.assertEqual(2, len(docs))
        self.assertIn(document2, docs)
        self.assertEqual(1, docs[document2])

        self.assertEqual(2, self.store.num_documents())

    def test_add_existing_term_existing_document(self):
        # Arrange
        term = "foo"
        document = uuid.uuid4()
        self.store.add(document, term)

        # Act
        self.store.add(document, term)

        # Assert
        docs = self.store.posting_list(term)
        self.assertEqual(1, len(docs))
        self.assertIn(document, docs)
        self.assertEqual(2, docs[document])

        self.assertEqual(1, self.store.num_documents())

    def test_add_new_term_existing_document(self):
        # Arrange
        term1 = "foo"
        term2 = "bar"
        document = uuid.uuid4()
        self.store.add(document, term1)

        # Act
        self.store.add(document, term2)

        # Assert
        docs = self.store.posting_list(term1)
        self.assertEqual(1, len(docs))
        self.assertIn(document, docs)
        self.assertEqual(1, docs[document])

        self.assertEqual(1, self.store.num_documents())


    def test_document_frequency_not_existing_term(self):
        # Act
        df = self.store.document_frequency("foo")

        # Assert
        self.assertEqual(0, df)

    def test_document_frequency_multiple_terms_in_store(self):
        # Arrange
        term1 = "foo"
        term2 = "bar"
        document = uuid.uuid4()

        self.store.add(document, term1)
        self.store.add(document, term2)

        # Act
        df = self.store.document_frequency("foo")

        # Assert
        self.assertEqual(1, df)

    def test_document_frequency_two_documents(self):
        # Arrange
        term = "foo"
        document1 = uuid.uuid4()
        document2 = uuid.uuid4()

        self.store.add(document1, term)
        self.store.add(document2, term)

        # Act
        df = self.store.document_frequency("foo")

        # Assert
        self.assertEqual(2, df)

    def test_term_document_frequency_not_existing_term(self):
        # Arrange
        term1 = "foo"
        term2 = "bar"
        document = uuid.uuid4()

        self.store.add(document, term1)

        # Act
        tf = self.store.term_document_frequency(document, term2)

        # Assert
        self.assertEquals(0, tf)

    def test_term_document_frequency_not_existing_document(self):
        # Arrange
        term = "foo"
        document1 = uuid.uuid4()
        document2 = uuid.uuid4()

        self.store.add(document1, term)

        # Act
        tf = self.store.term_document_frequency(document2, term)

        # Assert
        self.assertEquals(0, tf)

    def test_term_document_frequency_not_existing_document_and_term(self):
        # Act
        tf = self.store.term_document_frequency(uuid.uuid4(), "foo")

        # Assert
        self.assertEquals(0, tf)

    def test_term_document_frequency_term_in_multiple_documents(self):
        # Arrange
        term = "foo"
        document1 = uuid.uuid4()
        document2 = uuid.uuid4()

        self.store.add(document1, term)
        self.store.add(document2, term)

        # Act
        tf = self.store.term_document_frequency(document1, term)

        # Assert
        self.assertEquals(1, tf)

    def test_term_document_frequency_multiple_terms_in_document(self):
        # Arrange
        term1 = "foo"
        term2 = "bar"
        document = uuid.uuid4()

        self.store.add(document, term1)
        self.store.add(document, term2)

        # Act
        tf = self.store.term_document_frequency(document, term1)

        # Assert
        self.assertEquals(1, tf)

    def test_term_document_frequency_term_multiple_times_in_document(self):
        # Arrange
        term = "foo"
        document = uuid.uuid4()

        self.store.add(document, term)
        self.store.add(document, term)

        # Act
        tf = self.store.term_document_frequency(document, term)

        # Assert
        self.assertEquals(2, tf)

class IndexerTest(unittest.TestCase):
    def setUp(self):
        self.store_mock = IndexStoreMock()
        self.indexer = Indexer(self.store_mock, WordPunctTokenizer())


    def test_term_document_frequency(self):
        # Arrange
        term = "foo"
        document = uuid.uuid4()

        # Act
        self.indexer.term_document_frequency(document, term)

        # Assert
        self.assertEqual(1, self.store_mock.num_method_calls("term_document_frequency"))
        arguments =  self.store_mock.get_arguments("term_document_frequency")
        self.assertEqual(document, arguments[0])
        self.assertEqual(term, arguments[1])

    def test_document_frequency_normalized(self):
        # Arrange
        term = "foo"
        document_frequency = 22
        num_documents = 100
        self.store_mock.set_document_frequency(document_frequency)
        self.store_mock.set_num_documents(num_documents)

        # Act
        result = self.indexer.document_frequency_normalized(term)

        # Assert
        self.assertEqual(1, self.store_mock.num_method_calls("document_frequency"))
        document_frequency_args = self.store_mock.get_arguments("document_frequency")
        self.assertEqual(term, document_frequency_args[0])

        self.assertEqual(1, self.store_mock.num_method_calls("num_documents"))

        self.assertEqual(result, 0.22)


if __name__ == '__main__':
    unittest.main()