__author__ = 'Yves Bonjour'

import unittest
import uuid
from Clusterer import MemoryClusterStore
from VectorCalculatorMock import VectorCalculatorMock
from ClusterStoreMock import ClusterStoreMock
from Clusterer import Clusterer

class ClustererTest(unittest.TestCase):

    def setUp(self):
        self.store_mock = ClusterStoreMock()
        self.calculator_mock = VectorCalculatorMock()
        self.clusterer = Clusterer(self.store_mock, self.calculator_mock)

    def test_add_document_no_cluster(self):
        # Arrange
        document_id = uuid.uuid4()
        cluster_id = 1
        doc_vector = {"foo": 0.5, "bar": 0.5}
        self.store_mock.set_cluster_id(cluster_id)
        self.calculator_mock.set_vectors({document_id: doc_vector})
        self.calculator_mock.set_average_vectors({(document_id,):doc_vector})
        self.store_mock.set_centroids({})
        self.store_mock.set_documents({cluster_id:[document_id]})

        # Act
        self.clusterer.add_document(document_id)

        # Assert
        self.assertEqual(1, self.calculator_mock.num_method_calls("get_tfidf_vector"))
        vector_arguments = self.calculator_mock.get_arguments("get_tfidf_vector")
        self.assertEqual(document_id, vector_arguments[0])

        self.assertEqual(1, self.store_mock.num_method_calls("get_centroids"))

        self.assertEqual(1, self.store_mock.num_method_calls("add_cluster"))
        add_cluster_arguments = self.store_mock.get_arguments("add_cluster")
        self.assertEqual(doc_vector, add_cluster_arguments[0])

        self.assertEqual(1, self.store_mock.num_method_calls("add_to_cluster"))
        add_to_cluster_arguments = self.store_mock.get_arguments("add_to_cluster")
        self.assertEqual(document_id, add_to_cluster_arguments[0])
        self.assertEqual(cluster_id, add_to_cluster_arguments[1])

        self.assertEqual(1, self.calculator_mock.num_method_calls("get_average_vector"))
        get_average_vector_arguments = self.calculator_mock.get_arguments("get_average_vector")
        self.assertEqual([document_id], get_average_vector_arguments[0])

        self.assertEqual(1, self.store_mock.num_method_calls("set_centroid"))
        set_centroid_arguments = self.store_mock.get_arguments("set_centroid")
        self.assertEqual(cluster_id, set_centroid_arguments[0])
        self.assertEqual(doc_vector, set_centroid_arguments[1])


    def test_add_document_to_existing_cluster(self):
        # Arrange
        cluster_id = uuid.uuid4()
        document_id_1 = uuid.uuid4()
        doc_vector_1 = {"foo": 0.5, "bar": 0.5}

        document_id_2 = uuid.uuid4()
        doc_vector_2 = {"foo": 0.5, "bar": 0.5}

        avg_vector = {"foo": 0.5, "bar": 0.5}

        self.calculator_mock.set_vectors({document_id_1: doc_vector_1, document_id_2: doc_vector_2})
        self.calculator_mock.set_average_vectors({(document_id_1, document_id_2): avg_vector})

        self.store_mock.set_centroids({cluster_id:doc_vector_1})
        self.store_mock.set_documents({cluster_id:[document_id_1, document_id_2]})
        self.store_mock.set_threshold(0.9)

        # Act
        self.clusterer.add_document(document_id_2)

        # Assert
        self.assertEqual(1, self.calculator_mock.num_method_calls("get_tfidf_vector"))
        vector_arguments = self.calculator_mock.get_arguments("get_tfidf_vector")
        self.assertEqual(document_id_2, vector_arguments[0])

        self.assertEqual(1, self.store_mock.num_method_calls("get_centroids"))

        self.assertEqual(1, self.store_mock.num_method_calls("get_similarity_threshold"))

        self.assertEqual(0, self.store_mock.num_method_calls("add_cluster"))

        self.assertEqual(1, self.store_mock.num_method_calls("add_to_cluster"))
        add_to_cluster_arguments = self.store_mock.get_arguments("add_to_cluster")
        self.assertEqual(document_id_2, add_to_cluster_arguments[0])
        self.assertEqual(cluster_id, add_to_cluster_arguments[1])

        self.assertEqual(1, self.calculator_mock.num_method_calls("get_average_vector"))
        get_average_vector_arguments = self.calculator_mock.get_arguments("get_average_vector")
        self.assertEqual([document_id_1, document_id_2], get_average_vector_arguments[0])

        self.assertEqual(1, self.store_mock.num_method_calls("set_centroid"))
        set_centroid_arguments = self.store_mock.get_arguments("set_centroid")
        self.assertEqual(cluster_id, set_centroid_arguments[0])
        self.assertEqual(avg_vector, set_centroid_arguments[1])

    def test_add_document_to_new_cluster(self):
        # Arrange
        cluster_id_1 = uuid.uuid4()
        cluster_id_2 = uuid.uuid4()
        document_id_1 = uuid.uuid4()
        doc_vector_1 = {"foo": 0.5, "bar": 0.5}

        document_id_2 = uuid.uuid4()
        doc_vector_2 = {"foo": 1.0, "bar": 0.5}

        self.calculator_mock.set_vectors({document_id_1: doc_vector_1, document_id_2: doc_vector_2})
        self.calculator_mock.set_average_vectors({(document_id_2,): doc_vector_2})

        self.store_mock.set_centroids({cluster_id_1:doc_vector_1})
        self.store_mock.set_documents({cluster_id_1:[document_id_1], cluster_id_2:[document_id_2]})
        self.store_mock.set_cluster_id(cluster_id_2)

        # cosine_similarity = 0.75 / (sqrt(0.5) * sqrt(1.25)) = 0.948...
        self.store_mock.set_threshold(0.95)

        # Act
        self.clusterer.add_document(document_id_2)

        # Assert
        self.assertEqual(1, self.calculator_mock.num_method_calls("get_tfidf_vector"))
        vector_arguments = self.calculator_mock.get_arguments("get_tfidf_vector")
        self.assertEqual(document_id_2, vector_arguments[0])

        self.assertEqual(1, self.store_mock.num_method_calls("get_centroids"))

        self.assertEqual(1, self.store_mock.num_method_calls("get_similarity_threshold"))

        self.assertEqual(1, self.store_mock.num_method_calls("add_cluster"))
        add_cluster_arguments = self.store_mock.get_arguments("add_cluster")
        self.assertEqual(doc_vector_2, add_cluster_arguments[0])

        self.assertEqual(1, self.store_mock.num_method_calls("add_to_cluster"))
        add_to_cluster_arguments = self.store_mock.get_arguments("add_to_cluster")
        self.assertEqual(document_id_2, add_to_cluster_arguments[0])
        self.assertEqual(cluster_id_2, add_to_cluster_arguments[1])

        self.assertEqual(1, self.calculator_mock.num_method_calls("get_average_vector"))
        get_average_vector_arguments = self.calculator_mock.get_arguments("get_average_vector")
        self.assertEqual([document_id_2], get_average_vector_arguments[0])

        self.assertEqual(1, self.store_mock.num_method_calls("set_centroid"))
        set_centroid_arguments = self.store_mock.get_arguments("set_centroid")
        self.assertEqual(cluster_id_2, set_centroid_arguments[0])
        self.assertEqual(doc_vector_2, set_centroid_arguments[1])

    def test_add_document_to_nearer_cluster(self):
        # Arrange
        cluster_id_1 = uuid.uuid4()
        cluster_id_2 = uuid.uuid4()

        document_id_1 = uuid.uuid4()
        doc_vector_1 = {"foo": 0.5, "bar": 0.5}

        document_id_2 = uuid.uuid4()
        doc_vector_2 = {"foo": 1.0, "bar": 0.5}

        document_id_3 = uuid.uuid4()
        doc_vector_3 = {"foo": 1.0, "bar": 0.5}

        self.calculator_mock.set_vectors({document_id_3: doc_vector_3})
        self.calculator_mock.set_average_vectors({(document_id_2, document_id_3): doc_vector_2})

        self.store_mock.set_centroids({cluster_id_1: doc_vector_1, cluster_id_2: doc_vector_2})
        self.store_mock.set_documents({cluster_id_1:[document_id_1], cluster_id_2:[document_id_2, document_id_3]})

        # cosine_similarity = 0.75 / (sqrt(0.5) * sqrt(1.25)) = 0.948...
        self.store_mock.set_threshold(0.9)

        # Act
        self.clusterer.add_document(document_id_3)

        # Assert
        self.assertEqual(1, self.calculator_mock.num_method_calls("get_tfidf_vector"))
        vector_arguments = self.calculator_mock.get_arguments("get_tfidf_vector")
        self.assertEqual(document_id_3, vector_arguments[0])

        self.assertEqual(1, self.store_mock.num_method_calls("get_centroids"))

        self.assertEqual(1, self.store_mock.num_method_calls("get_similarity_threshold"))

        self.assertEqual(0, self.store_mock.num_method_calls("add_cluster"))

        self.assertEqual(1, self.store_mock.num_method_calls("add_to_cluster"))
        add_to_cluster_arguments = self.store_mock.get_arguments("add_to_cluster")
        self.assertEqual(document_id_3, add_to_cluster_arguments[0])
        self.assertEqual(cluster_id_2, add_to_cluster_arguments[1])

        self.assertEqual(1, self.calculator_mock.num_method_calls("get_average_vector"))
        get_average_vector_arguments = self.calculator_mock.get_arguments("get_average_vector")
        self.assertEqual([document_id_2, document_id_3], get_average_vector_arguments[0])

        self.assertEqual(1, self.store_mock.num_method_calls("set_centroid"))
        set_centroid_arguments = self.store_mock.get_arguments("set_centroid")
        self.assertEqual(cluster_id_2, set_centroid_arguments[0])
        self.assertEqual(doc_vector_2, set_centroid_arguments[1])


class MemoryClusterStoreTest(unittest.TestCase):

    def setUp(self):
        self.store = MemoryClusterStore(2)

    def test_get_documents_not_existing_cluster_id(self):
        self.assertRaises(RuntimeError, self.store.get_documents, 1)

    def test_add_cluster_first_cluster(self):
        # Arrange
        centroid = {"foo": 0.5, "bar": 0.5}

        # Act
        cluster_id = self.store.add_cluster(centroid)

        # Assert
        centroids = self.store.get_centroids()
        self.assertEqual(1, len(centroids))
        self.assertEqual(centroid, centroids[cluster_id])
        self.assertEqual(0, len(self.store.get_documents(cluster_id)))

    def test_add_cluster_with_existing_cluster(self):
        # Arrange
        centroid1 = {"foo": 0.5, "bar": 0.5}
        centroid2 = {"foo": 0.5, "bar": 0.5}
        self.store.add_cluster(centroid1)

        # Act
        cluster_id = self.store.add_cluster(centroid2)

        # Assert
        centroids = self.store.get_centroids()
        self.assertEqual(2, len(centroids))
        self.assertEqual(centroid2, centroids[cluster_id])
        self.assertEqual(0, len(self.store.get_documents(cluster_id)))

    def test_add_to_cluster_non_existing_cluster_id(self):
        self.assertRaises(RuntimeError, self.store.add_to_cluster, uuid.uuid4(), 1)

    def test_add_cluster_empty_cluster(self):
        # Arrange
        doc_id = uuid.uuid4()
        doc_vector = {"foo": 0.5, "bar": 0.5}
        cluster_id = self.store.add_cluster(doc_vector)

        # Act
        self.store.add_to_cluster(doc_id, cluster_id)

        # Assert
        documents = self.store.get_documents(cluster_id)
        self.assertEqual(1, len(documents))
        self.assertIn(doc_id, documents)

    def test_add_cluster_with_other_documents_in_cluster(self):
        # Arrange
        doc_id1 = uuid.uuid4()
        doc_id2 = uuid.uuid4()
        centroid = {"foo": 0.5, "bar": 0.5}
        cluster_id = self.store.add_cluster(centroid)
        self.store.add_to_cluster(doc_id1, cluster_id)

        # Act
        self.store.add_to_cluster(doc_id2, cluster_id)

        # Assert
        documents = self.store.get_documents(cluster_id)
        self.assertEqual(2, len(documents))
        self.assertIn(doc_id1, documents)
        self.assertIn(doc_id2, documents)

    def test_add_cluster_same_document_already_in_cluster(self):
        # Arrange
        doc_id = uuid.uuid4()
        doc_vector = {"foo": 0.5, "bar": 0.5}
        cluster_id = self.store.add_cluster(doc_vector)
        self.store.add_to_cluster(doc_id, cluster_id)

        # Act
        self.store.add_to_cluster(doc_id, cluster_id)

        # Assert
        documents = self.store.get_documents(cluster_id)
        self.assertEqual(1, len(documents))
        self.assertIn(doc_id, documents)

    def test_set_centroid_not_existing_cluster_id(self):
        self.assertRaises(RuntimeError, self.store.set_centroid, 1, {})

    def test_set_centroid(self):
        # Arrange
        centroid_initial = {"foo": 0.5, "bar": 0.5}
        centroid = {"foo": 0.5, "bar": 1.0}

        cluster_id = self.store.add_cluster(centroid_initial)

        # Act
        self.store.set_centroid(cluster_id, centroid)

        # Assert
        centroids = self.store.get_centroids()
        self.assertEqual(centroid, centroids[cluster_id])

    def test_set_centroid_other_centroids_untouched(self):
        # Arrange
        cenroid_untouched = {"foo": 1.0, "bar": 0.5}
        centroid_initial = {"foo": 0.5, "bar": 0.5}
        centroid = {"foo": 0.5, "bar": 1.0}

        cluster_id_untouched = self.store.add_cluster(cenroid_untouched)
        cluster_id = self.store.add_cluster(centroid_initial)

        # Act
        self.store.set_centroid(cluster_id, centroid)

        # Assert
        centroids = self.store.get_centroids()
        self.assertEqual(cenroid_untouched, centroids[cluster_id_untouched])
        self.assertEqual(centroid, centroids[cluster_id])



if __name__ == '__main__':
    unittest.main()
