__author__ = 'Yves Bonjour'

from Mock import Mock


class ClusterStoreMock(Mock):

    def set_centroids(self, centroids):
        self.centroids = centroids

    def set_documents(self, documents):
        self.documents = documents

    def set_threshold(self, threshold):
        self.threshold = threshold

    def set_cluster_id(self, cluster_id):
        self.cluster_id = cluster_id

    def get_documents(self, cluster_id):
        self._handle_method_call("get_documents", (cluster_id,))
        return self.documents[cluster_id]

    def get_centroids(self):
        self._handle_method_call("get_centroids")
        return self.centroids

    def get_similarity_threshold(self):
        self._handle_method_call("get_similarity_threshold")
        return self.threshold

    def add_cluster(self, vector):
        self._handle_method_call("add_cluster", (vector,))
        return self.cluster_id
