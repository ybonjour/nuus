__author__ = 'Yves Bonjour'

import unittest

from Indexer import MemoryIndexStore
from Indexer import RedisIndexStore
import uuid
from IndexStoreMock import IndexStoreMock
from TokenizerMock import TokenizerMock
from Indexer import Indexer
import redis

class StoreIndexTest(object):
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

    def test_term_posting_list_not_existing_term(self):
        # Act
        posting_list = self.store.posting_list("foo")

        # Assert
        self.assertEqual(0, len(posting_list))

    def test_get_terms_not_existing_document(self):
        # Arrange
        document = uuid.uuid4()

        # Act
        terms = self.store.get_terms(document)

        # Assert
        self.assertEqual(0, len(terms))

    def test_get_terms_one_term(self):
        # Arrange
        document = uuid.uuid4()
        term = "foo"
        self.store.add(document, term)

        # Act
        terms = self.store.get_terms(document)

        # Assert
        self.assertEqual(1, len(terms))
        self.assertIn(term, terms)

    def test_get_terms_one_term_with_other_document(self):
        # Arrange
        document1 = uuid.uuid4()
        document2 = uuid.uuid4()
        term1 = "foo"
        term2 = "bar"

        self.store.add(document1, term1)
        self.store.add(document2, term2)

        # Act
        terms = self.store.get_terms(document1)

        # Assert
        self.assertEqual(1, len(terms))
        self.assertIn(term1, terms)

    def test_get_terms_two_terms(self):
        # Arrange
        document = uuid.uuid4()
        term1 = "foo"
        term2 = "bar"

        self.store.add(document, term1)
        self.store.add(document, term2)

        # Act
        terms = self.store.get_terms(document)

        # Assert
        self.assertEqual(2, len(terms))
        self.assertIn(term1, terms)
        self.assertIn(term2, terms)

    def test_get_terms_same_term_twice(self):
        # Arrange
        document = uuid.uuid4()
        term = "foo"

        self.store.add(document, term)
        self.store.add(document, term)

        # Act
        terms = self.store.get_terms(document)

        # Assert
        self.assertEqual(1, len(terms))
        self.assertIn(term, terms)

class MemoryIndexStoreTest(StoreIndexTest, unittest.TestCase):
    def setUp(self):
        self.store = MemoryIndexStore()

class RedisIndexStoreTest(StoreIndexTest, unittest.TestCase):
    def setUp(self):
        self.redis = redis.Redis("localhost", 6379, db=2)
        self.redis.flushdb()
        self.store = RedisIndexStore(self.redis)

    def tearDown(self):
        self.redis.flushdb()

class IndexerTest(unittest.TestCase):
    def setUp(self):
        self.store_mock = IndexStoreMock()
        self.tokenizer_mock = TokenizerMock()
        self.indexer = Indexer(self.store_mock, self.tokenizer_mock)

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

    def test_index_empty_text(self):
        # Arrange
        document = uuid.uuid4()
        text = ""
        self.tokenizer_mock.set_tokens([])

        # Act
        self.indexer.index(text, document)

        # Assert
        self.assertEqual(1, self.tokenizer_mock.num_method_calls("tokenize"))
        tokenize_arguments = self.tokenizer_mock.get_arguments("tokenize")
        self.assertEqual(text, tokenize_arguments[0])

        self.assertFalse(self.store_mock.was_called("add"))

    def test_index_one_token(self):
        # Arrange
        document = uuid.uuid4()
        text = "foo"
        self.tokenizer_mock.set_tokens([text])

        # Act
        self.indexer.index(text, document)

        # Assert
        self.assertEqual(1, self.tokenizer_mock.num_method_calls("tokenize"))
        tokenize_arguments = self.tokenizer_mock.get_arguments("tokenize")
        self.assertEqual(text, tokenize_arguments[0])

        self.assertEqual(1, self.store_mock.num_method_calls("add"))
        add_arguments = self.store_mock.get_arguments("add")
        self.assertEqual(document, add_arguments[0])
        self.assertEqual(text, add_arguments[1])

    def test_index_two_tokens(self):
        # Arrange
        document = uuid.uuid4()
        tokens = ["foo", "bar"]
        text = " ".join(tokens)
        self.tokenizer_mock.set_tokens(tokens)

        # Act
        self.indexer.index(text, document)

        # Assert
        self.assertEqual(1, self.tokenizer_mock.num_method_calls("tokenize"))
        tokenize_arguments = self.tokenizer_mock.get_arguments("tokenize")
        self.assertEqual(text, tokenize_arguments[0])

        self.assertEqual(2, self.store_mock.num_method_calls("add"))

        add_arguments1 = self.store_mock.get_arguments("add", 1)
        self.assertEqual(document, add_arguments1[0])
        self.assertEqual(tokens[0], add_arguments1[1])

        add_arguments2 = self.store_mock.get_arguments("add", 2)
        self.assertEqual(document, add_arguments2[0])
        self.assertEqual(tokens[1], add_arguments2[1])

    def test_get_posting_list(self):
        # Arrange
        term = "foo"

        # Act
        self.indexer.get_posting_list(term)

        # Assert
        self.assertEqual(1, self.store_mock.num_method_calls("posting_list"))
        arguments = self.store_mock.get_arguments("posting_list")
        self.assertEqual(term, arguments[0])

    def test_get_terms(self):
        # Arrange
        terms = {"foo", "bar"}
        document = uuid.uuid4()

        self.store_mock.set_terms(terms)

        # Act
        result = self.indexer.get_terms(document)

        # Assert
        self.assertEqual(1, self.store_mock.num_method_calls("get_terms"))
        arguments = self.store_mock.get_arguments("get_terms")
        self.assertEqual(document, arguments[0])
        self.assertEqual(terms, result)

if __name__ == '__main__':
    unittest.main()
