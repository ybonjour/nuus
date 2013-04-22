__author__ = 'Yves Bonjour'

from Tokenizer import create_tokenizer
import redis
import uuid


def create_indexer(redis_host, redis_port):
    tokenizer = create_tokenizer()
    redis_db = redis.Redis(redis_host, redis_port)
    store = RedisIndexStore(redis_db)
    return Indexer(store, tokenizer)


class Indexer:
    def __init__(self, store, tokenizer):
        self.store = store
        self.tokenizer = tokenizer

    def index(self, text, document_id):
        tokens = self.tokenizer.tokenize(text)
        for token in tokens:
            self.store.add(document_id, token)

    def document_frequency_normalized(self, term):
        return float(self.store.document_frequency(term)) / float(self.store.num_documents())

    def term_document_frequency(self, document, term):
        return self.store.term_document_frequency(document, term)

    def get_posting_list(self, term):
        return self.store.posting_list(term)

    def get_terms(self, document):
        return self.store.get_terms(document)


class MemoryIndexStore(object):
    def __init__(self):
        self.posting_lists = {}
        self.documents = {}

    def posting_list(self, term):
        if term not in self.posting_lists:
            return {}

        return self.posting_lists[term]

    def get_terms(self, document):
        if document not in self.documents:
            return []

        return self.documents[document]

    def document_frequency(self, term):
        if term not in self.posting_lists:
            return 0

        return len(self.posting_lists[term])

    def num_documents(self):
        return len(self.documents)

    def term_document_frequency(self, document, term):
        if term not in self.posting_lists or document not in self.posting_lists[term]:
            return 0

        return self.posting_lists[term][document]

    def add(self, document, term):
        if term not in self.posting_lists:
            self.posting_lists[term] = {}

        if document not in self.posting_lists[term]:
            self.posting_lists[term][document] = 0

        self.posting_lists[term][document] += 1

        if document not in self.documents:
            self.documents[document] = set()

        self.documents[document].add(term)


class RedisIndexStore(object):
    def __init__(self, redis):
        self.redis = redis

    def posting_list(self, term):
        return {uuid.UUID(document): int(self.redis.get(self._posting_key(term, document)))
                for document in self.redis.smembers(self._term_key(term))}

    def document_frequency(self, term):
        return len(self.redis.smembers(self._term_key(term)))

    def get_terms(self, document):
        return self.redis.smembers(self._document_key(document))

    def num_documents(self):
        return len(self.redis.smembers(self._documents_key()))

    def term_document_frequency(self, document, term):
        tdf = self.redis.get(self._posting_key(term, document))
        return int(tdf) if tdf else 0

    def add(self, document, term):
        self.redis.sadd(self._documents_key(), document)
        self.redis.sadd(self._term_key(term), document)
        self.redis.sadd(self._document_key(document), term)
        self.redis.setnx(self._posting_key(term, document), 0)
        self.redis.incr(self._posting_key(term, document))

    def _documents_key(self):
        return "documents"

    def _document_key(self, document):
        return "document:{document}".format(document=document)

    def _term_key(self, term):
        return "term:{term}".format(term=term)

    def _posting_key(self, term, document):
        return "posting:{term}:{document}".format(term=term, document=document)