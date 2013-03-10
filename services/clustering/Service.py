__author__ = 'Yves Bonjour'
from Clusterer import Clusterer
from ClusterStore import MemoryClusterStore

if __name__ == "__main__":
    centroid_store = MemoryClusterStore([])
    clusterer = Clusterer(centroid_store)
