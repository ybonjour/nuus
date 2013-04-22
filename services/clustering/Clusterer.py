__author__ = 'Yves Bonjour'

from math import sqrt
from VectorCalculator import create_vector_calculator
import uuid
import redis

def create_clusterer(redis_host, redis_port, clustering_threshold, index_url):
    redis_db = redis.Redis(redis_host, redis_port)
    store = RedisClusterStore(redis_db, clustering_threshold)
    vector_calculator = create_vector_calculator(index_url)
    return Clusterer(store, vector_calculator)

def l2norm(v):
    return sqrt(sum([x*x for x in v.values()]))

def vector_product(v1, v2):
    all_keys = set(v1.keys()) | set(v2.keys())
    sum = 0
    for key in all_keys:
        sum += v1.get(key, 0)*v2.get(key, 0)

    return sum

class Clusterer:
    def __init__(self, cluster_store, vector_calculator):
        self.store = cluster_store
        self.vector_calculator = vector_calculator

    def add_document(self, document_id):
        vector = self.vector_calculator.get_tfidf_vector(document_id)
        cluster_similarities = [(cluster_id, self._similarity(vector, centroid))
                               for cluster_id, centroid in self.store.get_centroids().iteritems()]

        max_cluster = max(cluster_similarities, key=lambda x: x[1]) if cluster_similarities else None

        if max_cluster and max_cluster[1] >= self.store.get_similarity_threshold():
            cluster_id = max_cluster[0]
        else:
            cluster_id = self.store.add_cluster(vector)

        self.store.add_to_cluster(document_id, cluster_id)
        centroid = self._calculate_centroid(cluster_id)
        self.store.set_centroid(cluster_id, centroid)

    def _similarity(self, v1, v2):
        return float(vector_product(v1, v2)) / (float(l2norm(v1))*float(l2norm(v2)))

    def _calculate_centroid(self, cluster_id):
        document_ids = self.store.get_documents(cluster_id)
        return self.vector_calculator.get_average_vector(document_ids)


class MemoryClusterStore:
    def __init__(self,threshold):
        self.centroids = {}
        self.documents = {}
        self.threshold = threshold

    def get_documents(self, cluster_id):
        if cluster_id not in self.documents:
            raise RuntimeError("Invalid cluster id")

        return self.documents[cluster_id]

    def get_centroids(self):
        return self.centroids

    def set_centroid(self, cluster_id, centroid):
        if cluster_id not in self.documents:
            raise RuntimeError("Invalid cluster id")

        self.centroids[cluster_id] = centroid

    def add_cluster(self, centroid):
        cluster_id = len(self.documents)
        self.centroids[cluster_id] = centroid
        self.documents[cluster_id] = set([])
        return cluster_id

    def add_to_cluster(self, document_id, cluster_id):
        if cluster_id not in self.documents:
            raise RuntimeError("Invalid cluster id")

        self.documents[cluster_id].add(document_id)

    def get_similarity_threshold(self):
        return self.threshold


class RedisClusterStore:
    def __init__(self, redis, threshold):
        self.redis = redis
        self.redis.set(self._key_threshold(), threshold)

    def get_similarity_threshold(self):
        return int(self.redis.get(self._key_threshold()))

    def add_to_cluster(self, document_id, cluster_id):
        if not self._exists_cluster(cluster_id):
            raise RuntimeError("Invalid cluster id")

        self.redis.sadd(self._key_cluster(cluster_id), document_id)

    def get_documents(self, cluster_id):
        if not self._exists_cluster(cluster_id):
            raise RuntimeError("Invalid cluster id")

        return [uuid.UUID(doc_id) for doc_id in self.redis.smembers(self._key_cluster(cluster_id))]

    def add_cluster(self, centroid):
        cluster_id = uuid.uuid4()

        self.redis.sadd(self._key_all_clusters(), cluster_id)
        self.redis.hmset(self._key_centroid(cluster_id), centroid)

        return cluster_id

    def get_centroids(self):
        centroids = {}
        for cluster_id in self.redis.smembers(self._key_all_clusters()):
            d = self.redis.hgetall(self._key_centroid(cluster_id))
            centroid = {term: float(value) for term, value in d.iteritems()}
            centroids[uuid.UUID(cluster_id)] = centroid
        return centroids

    def set_centroid(self, cluster_id, centroid):
        if not self._exists_cluster(cluster_id):
            raise RuntimeError("Invalid cluster id")

        for term in self.redis.hkeys(self._key_centroid(cluster_id)):
            self.redis.hdel(self._key_centroid(cluster_id), term)

        self.redis.hmset(self._key_centroid(cluster_id), centroid)

    def _exists_cluster(self, cluster_id):
        return self.redis.sismember(self._key_all_clusters(), cluster_id)

    def _key_all_clusters(self):
        return "clustering:all_clusters"

    def _key_cluster(self, cluster_id):
        return "clustering:cluster:{cluster_id}".format(cluster_id=cluster_id)

    def _key_threshold(self):
        return "clustering:threshold"

    def _key_centroid(self, cluster_id):
        return "clustering:centroid:{cluster_id}".format(cluster_id=cluster_id)
