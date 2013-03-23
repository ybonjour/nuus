__author__ = 'Yves Bonjour'

from math import sqrt


def l2norm(v):
    return sqrt(sum([x*x for x in v.items()]))

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
        cluster_similarities = [(idx, self._similarity(vector, centroid))
                               for idx, centroid in enumerate(self.store.get_centroids())]

        min_cluster = min(cluster_similarities, key=lambda x: x[1]) if cluster_similarities else None

        if min_cluster and min_cluster[1] <= self.store.get_similarity_threshold():
            cluster_id = min_cluster[0]
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
        self.centroids = []
        self.documents = []
        self.threshold = threshold

    def get_documents(self, cluster_id):
        if cluster_id >= len(self.documents):
            raise RuntimeError("Invalid cluster id")

        return self.documents[cluster_id]

    def get_centroids(self):
        return self.centroids

    def set_centroid(self, cluster_id, centroid):
        if cluster_id >= len(self.documents):
            raise RuntimeError("Invalid cluster id")

        self.centroids[cluster_id] = centroid

    def add_cluster(self, centroid):
        self.centroids.append(centroid)
        self.documents.append(set([]))
        return len(self.documents) - 1

    def add_to_cluster(self, document_id, cluster_id):
        if cluster_id >= len(self.documents):
            raise RuntimeError("Invalid cluster id")

        self.documents[cluster_id].add(document_id)

    def get_similarity_threshold(self):
        return self.threshold