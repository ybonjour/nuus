__author__ = 'Yves Bonjour'


class Clusterer:
    def __init__(self, cluster_store, vector_calculator, threshold):
        self.store = cluster_store
        self.vector_calculator = vector_calculator
        self.threshold = threshold

    def similarity(self, v1, v2):
        return 0

    def calculate_centroid(self, cluster_id):
        return self.vector_calculator.get_average_vector(self.store.get_documets(cluster_id))

    def add_document(self, document_id):
        vector = self.vector_calculator.get_tfidf_vecto(document_id)
        cluster_similarites = [(idx, self.similarity(vector, centroid))
                               for idx, centroid in enumerate(self.store.get_centroids())]

        min_cluster = min(cluster_similarites, key=lambda x: x[1])

        if min_cluster[1] <= self.store.get_similarity_threshold():
            cluster_id = min_cluster[0]
        else:
            cluster_id = self.store.add_cluster(vector)

        self.store.add_to_cluster(document_id, cluster_id)
        self.store.set_centroid(self.calculate_centroid(cluster_id))


class MemoryClusterStore:
    def __init__(self, centroids, documents, threshold):
        if len(centroids) != len(documents):
            raise RuntimeError("centoids and documents must have same length")

        self.centroids = centroids
        self.documents = documents
        self.threshold = threshold

    def get_documents(self, cluster_id):
        return self.documents[cluster_id]

    def get_centroids(self):
        return self.centroids

    def set_centroid(self, cluster_id, centroid):
        if cluster_id >= len(self.documents):
            raise RuntimeError("Invalid cluster id")

        self.centroids[cluster_id] = centroid

    def add_cluster(self, centroid):
        self.centroids.append(centroid)
        self.documents.append([])
        return len(self.documents) - 1

    def add_to_cluster(self, document_id, cluster_id):
        if cluster_id >= len(self.documents):
            raise RuntimeError("Invalid cluster id")

        self.documents[cluster_id].append(document_id)

    def get_similarity_threshold(self):
        return self.threshold